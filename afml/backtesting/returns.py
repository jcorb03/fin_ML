import pandas as pd

def strategy_gross_returns(
    adjusted_open: pd.Series,
    adjusted_close: pd.Series,
    position_at_open: pd.Series,
) -> pd.Series:
    """
    Calculate close-to-close strategy returns with trading at each open.

    position_at_open is the holding after the opening trade, either 0 or 1.
    Positions remain unchanged until the following session's open.

    Apply the previous position to overnight returns and the current
    position to intraday returns, compounding the two growth factors.

    Assume aligned indexes, initially no holding, zero cash interest,
    and no transaction costs. Leave the first return missing.
    """
    ...

    previous_close = adjusted_close.shift(1)

    overnight_returns = adjusted_open / previous_close -1

    intraday_returns = adjusted_close / adjusted_open - 1

    old_position  = position_at_open.shift(1).fillna(0)

    strategy_return = (1 + old_position * overnight_returns)*(1 + position_at_open* intraday_returns) - 1

    return strategy_return


def apply_transaction_costs(
    gross_returns: pd.Series,
    position_at_open: pd.Series,
    cost_rate: float,
) -> pd.Series:
    """
    Deduct proportional opening-trade costs from gross strategy returns.

    Positions must be 0 or 1, with aligned indexes.
    Turnover is the absolute change from the previous position,
    assuming an initial position of zero.

    cost_rate is the fraction of opening portfolio value charged
    for a full entry or exit. For example, 0.0005 means 5 basis points.

    Return net returns with the original index and missing values.
    Assume 0 <= cost_rate < 1.
    """

    old_position  = position_at_open.shift(1).fillna(0)
    turnover = (position_at_open - old_position).abs()

    net_returns = (1+gross_returns)*(1-cost_rate*turnover)-1

    return net_returns

def equity_curve(returns: pd.Series, initial_value: float = 1.0) -> pd.Series:
    """
    Compound periodic returns into end-of-period portfolio values.

    Each value includes that row's return. Preserve the input index.
    Assume nonmissing returns greater than or equal to -1.
    """

    return initial_value * (1+returns).cumprod()

    


if __name__ == "__main__":
    gross_returns =  pd.Series([0.0,0.0,0.0,0.0])
    costrate = 0.0005
    position_at_open = pd.Series([0,1,1,0])

    result = apply_transaction_costs(gross_returns,position_at_open,costrate)
    expected_result =  pd.Series([0.0, -0.0005, 0.0, -0.0005])

    pd.testing.assert_series_equal(
        result,
        expected_result,
        check_exact=False,
        rtol=1e-10,
        atol=1e-12,
    )
    print("results as expected")

    print(equity_curve(pd.Series([0.10, -0.10]), 100.0))


