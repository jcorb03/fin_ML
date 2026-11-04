import pandas as pd


import yfinance as yf
from yahoo.moving_average import *
import warnings
from strategy.strategy_gross_returns import *
from strategy.metrics import drawdown

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

adjusted_close = development["Adj Close"]
adjustment = adjusted_close / development["Close"]
adjusted_open = development["Open"] * adjustment

signal = above_mov_avg_signal(adjusted_close, window=200)
position_at_open = signal.shift(1).fillna(0)

gross_returns = strategy_gross_returns(
    adjusted_open, adjusted_close, position_at_open
)

net_returns = apply_transaction_costs(
    gross_returns, position_at_open, cost_rate=0.0005
)

# First valid signal is at position 199; first execution is at 200.
evaluation_returns = net_returns.iloc[200:]

##Benchmark
benchmark_position = pd.Series(0.0, index=adjusted_close.index)
benchmark_position.iloc[200:] = 1.0

benchmark_gross = strategy_gross_returns(
    adjusted_open, adjusted_close, benchmark_position
)

benchmark_net = apply_transaction_costs(
    benchmark_gross, benchmark_position, cost_rate=0.0005
)

benchmark_curve = equity_curve(
    benchmark_net.iloc[200:], initial_value=100.0
)


direct_curve = 100.0 * (1 + benchmark_net.iloc[200:]).cumprod()

print("Direct calculation:")
print(direct_curve.tail())

print("Function result:")
print(benchmark_curve.tail())

print("Function imported from:", equity_curve.__module__)

comparison = pd.DataFrame({
    "strategy": equity_curve(evaluation_returns, initial_value=100.0),
    "buy_and_hold": equity_curve(
        benchmark_net.iloc[200:], initial_value=100.0
    ),
})


for name in comparison.columns:
    curve = comparison[name]

    total_return = curve.iloc[-1] / 100.0 - 1
    max_drawdown = drawdown(curve, initial_value=100.0).min()

    print(
        f"{name}: "
        f"total return={total_return:.1%}, "
        f"maximum drawdown={max_drawdown:.1%}"
    )
