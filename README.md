# Financial machine learning

Python implementations and experiments based on *Advances in Financial Machine Learning*.

| Package | Contents |
| --- | --- |
| `afml.features` | Returns, rolling volatility, momentum, and moving-average signals |
| `afml.sampling` | CUSUM event selection, event concurrency and uniqueness, and sequential bootstrap |
| `afml.labeling` | Triple-barrier labeling with fixed percentage or volatility-scaled barriers |
| `afml.validation` | Purged cross-validation with embargo and RMSE |
| `afml.backtesting` | Strategy returns, transaction costs, equity curves, and drawdown |
| `examples` | Runnable examples using synthetic prices or Yahoo Finance |
| `TWS_API` | Interactive Brokers connection code |

From the repository root, install the dependencies and run the synthetic examples.

```shell
python -m pip install -r requirements.txt
python -m examples.event_labeling
python -m examples.purged_decision_tree
```

The Yahoo Finance examples also need `yfinance` and network access.

```shell
python -m pip install yfinance
python -m examples.yahoo_moving_average_signal
python -m examples.yahoo_moving_average_backtest
```

To reuse a function, import it from its module. For example, use
`from afml.labeling.volatility_barriers import label_events` for volatility-scaled
event labels or `from afml.labeling.fixed_barriers import triple_barrier` for
fixed percentage barriers. The two functions accept different inputs and return
different outputs.
