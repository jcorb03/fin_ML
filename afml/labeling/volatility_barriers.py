import pandas as pd

def price_barriers(
    entry_price: float,
    volatility: float,
    multiplier: float,
) -> tuple[float, float]:
    return (entry_price * (1 +volatility*multiplier),
            entry_price * (1 -volatility*multiplier))



def first_barrier_hit(
    future_prices: pd.Series,
    upper: float,
    lower: float,
) -> tuple[int, str]:

    if future_prices.empty:
        raise ValueError("future_prices must contain at least one observation")

    for i,num in enumerate(future_prices):
        if num >= upper:
            return (i+1,"upper")
        if num <= lower:
            return (i+1, "lower")
    return (future_prices.size,"time")

def label_event(
    prices: pd.Series,
    entry_position: int,
    volatility: float,
    multiplier: float,
    max_holding: int,
) -> tuple[int, str, float]:
    """
    Return the exit position in the original Series and the barrier type.

    returns day, barrier hit and realised return
    """
    if (entry_position+max_holding > len(prices) -1):
        raise ValueError("Window exceeds prices length")
    
    entry_price = prices.iloc[entry_position]

    upper,lower = price_barriers(entry_price = entry_price,
                                   volatility=volatility,
                                   multiplier=multiplier)

    future_prices = prices.iloc[entry_position+1:entry_position+max_holding+1]

    (index,barrier) = first_barrier_hit(
        future_prices,
        upper,
        lower
    )

    realised_return = (future_prices.iloc[index-1]-entry_price)/entry_price

    return (index+entry_position, barrier, realised_return)

def is_profit(
    realised_return : float
) -> int:
    if realised_return > 0:
        return 1
    elif realised_return < 0:
        return -1
    else:
        return 0


def label_events(
    prices: pd.Series,
    entry_positions: list[int],
    volatility: pd.Series,
    multiplier: float,
    max_holding: int,
) -> pd.DataFrame:
    rows = []
    
    for position in entry_positions:

        vol = volatility.iloc[position]
        if pd.isna(vol):
            continue

        
        exit_position, barrier, realised_return = label_event(prices,position,volatility=vol,multiplier=multiplier,max_holding=max_holding)

        if pd.isna(realised_return):
            raise ValueError("Cannot label a missing return")

        rows.append({"entry_position": position,
                     "exit_position": exit_position,
                     "barrier": barrier,
                     "realised_return": realised_return,
                     "label": is_profit(realised_return)})

        
    columns = ["entry_position", "exit_position", "barrier", "realised_return", "label"]

    return pd.DataFrame(rows, columns=columns).set_index("entry_position")
    



