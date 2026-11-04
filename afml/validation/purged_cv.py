import pandas as pd
import numpy as np

from afml.sampling.sequential_bootstrap import events_overlap

def purge_training_events(
    train_events: pd.DataFrame,
    test_events: pd.DataFrame,
) -> pd.DataFrame:
    """
    Remove training events whose label intervals overlap any test event.

    Both DataFrames use unique entry positions as their index and contain
    an 'exit_position' column. Intervals cover entry + 1 through exit.

    Return a copy of the retained training rows, preserving their columns
    and order. This checks label overlap only; it does not apply an embargo.
    """
    keep_entries = []

    for entry,event in train_events.iterrows():
        train_exit = int(event["exit_position"])
        overlaps = False

        for test_entry, test_event in test_events.iterrows():
            test_exit = int(test_event["exit_position"])

            if events_overlap(entry, train_exit, test_entry, test_exit):
                overlaps = True
                break

        if not(overlaps):
            keep_entries.append(entry)

    return train_events.loc[keep_entries].copy()

def purge_with_embargo(
    train_events: pd.DataFrame,
    test_events: pd.DataFrame,
    embargo_size: int,
) -> pd.DataFrame:

    if embargo_size <= 0:
        raise ValueError("embargo must be positive")

    if test_events.empty:
        return train_events.copy()

    extended_events = test_events.copy()
    last_exit_entry = extended_events["exit_position"].idxmax()
    extended_events.loc[last_exit_entry, "exit_position"] += embargo_size

    return purge_training_events(train_events,extended_events)

def purged_kfold(
    events: pd.DataFrame,
    n_splits: int,
    embargo_size: int = 0,
) -> list[tuple[pd.DataFrame, pd.DataFrame]]:
    """
    Create chronological test folds with purged training sets.

    Sort events by their entry-position index, then divide them into
    n_splits consecutive groups without shuffling. For each group,
    use it as the test set and the remaining events as candidate training
    data. Apply the existing purge-with-embargo function.

    Return a list of (train_events, test_events) pairs.

    Training may include events later than the test block. This is
    purged K-fold validation, not a walk-forward deployment simulation.
    """

    sets = []
    if n_splits<2 or n_splits>len(events):
        raise ValueError("Invalid number of folds")

    ordered_events = events.sort_index()
    test_groups = np.array_split(ordered_events.index.to_numpy(), n_splits)

    for i in test_groups:
        test_set = ordered_events.loc[i]
        train_set = ordered_events.drop(index = i)

        train_set = purge_with_embargo(train_set,test_set,embargo_size=embargo_size)
        
        sets.append((train_set,test_set))

    return sets


if __name__ == "__main__":
    events = pd.DataFrame({
        "entry_position": [2, 5, 8, 11, 14, 17],
        "exit_position": [6, 9, 12, 15, 18, 21],
    }).set_index("entry_position")

    folds = purged_kfold(events, n_splits=3, embargo_size=2)

    expected_test = [[2, 5], [8, 11], [14, 17]]
    expected_train = [[11, 14, 17], [2, 17], [2, 5, 8]]

    for fold_number, (train, test) in enumerate(folds):
        assert test.index.tolist() == expected_test[fold_number]
        assert train.index.tolist() == expected_train[fold_number]

        print(
            f"Fold {fold_number + 1}: "
            f"train={train.index.tolist()}, "
            f"test={test.index.tolist()}"
        )
    shuffled_events = events.sample(frac=1, random_state=42)
    shuffled_folds = purged_kfold(
        shuffled_events, n_splits=3, embargo_size=2
    )

    for (train, test), (shuffled_train, shuffled_test) in zip(
        folds, shuffled_folds
    ):
        pd.testing.assert_frame_equal(train, shuffled_train)
        pd.testing.assert_frame_equal(test, shuffled_test)