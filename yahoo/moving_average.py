import pandas as pd

def moving_average(prices: pd.Series, window: int) -> pd.Series:
    """
    Calculate the trailing mean over window price observations.

    Include the current observation and preserve the original index.
    Return NaN until a full window is available.
    """
    
    return prices.rolling(window=window).mean()

def above_mov_avg_signal(prices: pd.Series, window: int) -> pd.Series:
    """
    Returns a signal of whether a stock's close is trading above its
    moving average of a user defined window size
    """

    mov_avg = moving_average(prices, window)

    return (prices > mov_avg).astype(int)
        