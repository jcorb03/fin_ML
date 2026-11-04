import pandas as pd

def cusum_events(returns: pd.Series, threshold: float) -> list[int]:
    s_plus, s_minus = 0.0,0.0
    rows = []

    if threshold <= 0:
        raise ValueError("threshold must be positive")
    
    for i,r in enumerate(returns):

        if pd.isna(r):
            continue

        s_plus = max(0.0, s_plus + r)
        s_minus = min(0.0, s_minus + r)

        if (s_plus> threshold):
            rows.append(i)
            s_plus = 0
        elif (s_minus< -threshold):
            rows.append(i)
            s_minus = 0
        
    return rows


if __name__ == "__main__":
    returns = pd.Series([+0.01, +0.01, -0.005, +0.02])

    threshold = 0.03

    print(cusum_events(returns=returns, threshold=threshold))

    assert cusum_events(
        pd.Series([0.01, 0.01, -0.005, 0.02]), 0.03
    ) == [3]