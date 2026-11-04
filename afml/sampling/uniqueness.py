import pandas as pd
import numpy as np

def count_concurrency(events: pd.DataFrame, n_prices: int) -> pd.Series:

    counts = pd.Series(0, index = range(n_prices),dtype = int)

    for entry, event in events.iterrows():
        exit_position = int(event["exit_position"])

        counts.iloc[entry+1:exit_position+1] += 1

    return counts

def uniqueness_of_events(events: pd.DataFrame, counts: pd.Series) -> pd.Series:

    uniqueness = pd.Series(0, index = events.index, dtype = float)

    for entry, event in events.iterrows():
            exit_position = int(event["exit_position"])

            event_counts = counts.iloc[entry+1:exit_position+1]
            uniqueness.loc[entry] = (1/event_counts).mean()

    return uniqueness





