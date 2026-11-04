import pandas as pd

A = pd.Series([0.01, 0.01, 0.01, 0.01]) 
B = pd.Series([0.04, -0.02, 0.03, -0.01])

def rolling_volatility(returns: pd.Series, window: int) -> pd.Series:
    return returns.rolling(window=window).std()


