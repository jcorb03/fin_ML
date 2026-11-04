import pandas as pd

from afml.features.momentum import momentum
from afml.features.returns import simple_returns
from afml.features.volatility import rolling_volatility
from afml.labeling.volatility_barriers import label_events
from afml.sampling.cusum import cusum_events

if __name__ == "__main__":
    # 1. Calculate returns, volatility and entry positions.
    prices = pd.Series(
        [90, 95, 100, 101, 103, 95, 105, 102, 108, 104, 110, 107],
        dtype=float,
    )
    window = 3
    daily_returns = simple_returns(prices)
    volatility = rolling_volatility(daily_returns, window=window).shift(1)

    entry_positions = cusum_events(daily_returns,0.03)  
    max_holding = 4
    entry_positions = [x for x in entry_positions if x < len(prices) - max_holding]

    # 2. Create events using label_events(...).
    events = label_events(
        prices=prices,
        entry_positions=entry_positions,
        volatility=volatility,
        multiplier=2.0,
        max_holding=max_holding,
    )
    # 3. Build features from the same prices.
    features = pd.DataFrame({
        "momentum_2": momentum(prices, lookback=2),
        "volatility_3": rolling_volatility(simple_returns(prices), window=3),
    })

    # 4. Select event rows and combine with outcomes.
    event_features = features.iloc[events.index].copy()
    event_features.index = events.index
    dataset = event_features.join(events)

    print(dataset)