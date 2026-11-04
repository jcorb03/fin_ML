import pandas as pd
import math

prices = pd.Series(
    [100.0, 105.0, 102.0, 108.0],
    index=pd.date_range("2026-01-01", periods=4, freq="D"),
)

def simple_returns(prices: pd.Series) -> pd.Series:
    previous_prices = prices.shift(1)
    return (prices - previous_prices)/previous_prices

def compounded_return(returns: pd.Series) -> float:
    result = 1
    for i in returns:
        result *= (1+i)
    result -= 1
    return result

returns = pd.Series(
    [0.10, -0.10]
)

if __name__ == "__main__":
    daily_returns = simple_returns(prices).dropna()
    final_return = compounded_return(daily_returns)

    print(round(final_return,2))

    assert math.isclose(
        compounded_return(pd.Series([0.10, -0.10])),
        -0.01,
        abs_tol=1e-12,
    )