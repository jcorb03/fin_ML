import pandas as pd
import numpy as np

def bootstrap_scores(
    events: pd.DataFrame,
    selected_counts: pd.Series,
) -> pd.Series:
    """
    Score each candidate event by its uniqueness if selected next.
    """

    scores = pd.Series(0, index = events.index, dtype = float)

    for entry, event in events.iterrows():
        exit_position = int(event["exit_position"])

        event_counts = selected_counts.iloc[entry+1:exit_position+1]

        scores.loc[entry] = (1 / (event_counts + 1)).mean()

    return scores

def choose_entry(scores: pd.Series, rng: np.random.Generator) -> int:
     
    probabilities = scores/scores.sum()
    chosen_entry = rng.choice(
        probabilities.index.to_numpy(),
        p=probabilities.to_numpy(),
        )

    return int(chosen_entry)

def sequential_bootstrap(
    events: pd.DataFrame,
    n_prices: int,
    sample_size: int,
    seed: int = 42,
) -> list[int]:
    """
    Sample event entries with replacement, favouring less overlap.

    Recalculate candidate uniqueness scores after every selection.
    """

    selected_counts = pd.Series(0,index = range(n_prices) , dtype=int )

    rows = []

    rng = np.random.default_rng(seed)

    for i in range(sample_size):
        scores = bootstrap_scores(events=events,selected_counts=selected_counts)

        chosen_entry = choose_entry(scores=scores, rng=rng)

        rows.append(chosen_entry)

        exit_position = int(events.loc[chosen_entry, "exit_position"])

        selected_counts.iloc[chosen_entry+1:exit_position+1]+=1

    return rows

def events_overlap(
    entry_a: int,
    exit_a: int,
    entry_b: int,
    exit_b: int,
) -> bool:
    """
    Return whether two event label intervals share any return positions.

    Each interval covers entry + 1 through exit, inclusive.
    Assume each exit is strictly greater than its entry.
    """
    ...

    return not(exit_a <= entry_b or exit_b <= entry_a)


        
