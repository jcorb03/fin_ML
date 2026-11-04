import warnings

import pandas as pd
import yfinance as yf

from afml.features.moving_average import above_mov_avg_signal

def main():
    if hasattr(pd.errors, "Pandas4Warning"):
        warnings.filterwarnings(
            "ignore",
            category=pd.errors.Pandas4Warning,
            module=r"yfinance\..*",
        )

    data = yf.download(
        "SPY",
        start="2000-01-01",
        end="2026-01-01",
        interval="1d",
        auto_adjust=False,
        actions=True,
        multi_level_index=False,
        progress=False,
    )

    if data.empty:
        raise ValueError("No price data downloaded")

    development = data.loc[:"2015-12-31"].copy()
    prices = development["Adj Close"]

    prices_test = pd.Series([100, 102, 104, 99])
    print(above_mov_avg_signal(prices_test, window=3))

    shifted_signal = above_mov_avg_signal(prices_test, window=3).shift(1).fillna(0).astype(int)
    print(shifted_signal)


if __name__ == "__main__":
    main()
