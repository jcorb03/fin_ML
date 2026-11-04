import pandas as pd

from .rolling_volatility import rolling_volatility

def momentum(prices: pd.Series, lookback: int) -> pd.Series:

    previous_prices= prices.shift(lookback)

    momentum = pd.Series(prices/previous_prices -1 )

    return momentum

if __name__ == "__main__":
    prices = pd.Series([100, 102, 105, 103])
    lookback =2

    print(momentum(prices,lookback))