import pandas as pd

def drawdown(equity: pd.Series, initial_value: float = 1.0) -> pd.Series:
    """
    Calculate fractional drawdown from the running portfolio peak.

    equity contains end-of-period values with no missing observations.
    Include initial_value as a peak before the first observation.
    Return zero at a peak and negative values below it.
    """

    max_so_far = equity.cummax().clip(lower=initial_value)

    drawdown = equity/max_so_far -1

    return drawdown

initial_val = 100
equity = pd.Series([90, 110, 99, 121])

print(drawdown(equity,initial_val))