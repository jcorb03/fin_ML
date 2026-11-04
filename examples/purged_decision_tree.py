import numpy as np
import pandas as pd

from afml.features.momentum import momentum
from afml.features.returns import simple_returns
from afml.features.volatility import rolling_volatility
from afml.labeling.volatility_barriers import label_events
from afml.sampling.cusum import cusum_events
from afml.sampling.sequential_bootstrap import sequential_bootstrap
from afml.validation.purged_cv import purged_kfold
from sklearn.tree import DecisionTreeClassifier

def main():
    rng = np.random.default_rng(42)
    log_returns = rng.normal(loc=0.0, scale=0.01, size=2000)

    prices = pd.Series(
        100.0 * np.exp(np.concatenate(([0.0], np.cumsum(log_returns))))
    )

    window =20
    threshold = 0.02
    max_holding = 10
    multiplier = 2.0

    daily_returns = simple_returns(prices)
    volatility = rolling_volatility(daily_returns, window=window).shift(1)

    entry_positions = cusum_events(daily_returns,threshold)
    entry_positions = [x for x in entry_positions if x < len(prices) - max_holding]

    # 2. Create events using label_events(...).
    events = label_events(
        prices=prices,
        entry_positions=entry_positions,
        volatility=volatility,
        multiplier=multiplier,
        max_holding=max_holding,
    )

    # 3. Build features from the same prices.
    features = pd.DataFrame({
        "momentum": momentum(prices, lookback=5),
        "volatility_20": rolling_volatility(simple_returns(prices), window=20),
    })

    # 4. Select event rows and combine with outcomes.
    event_features = features.iloc[events.index].copy()
    event_features.index = events.index
    dataset = event_features.join(events)

    folds = purged_kfold(
        dataset,
        n_splits=5,
        embargo_size=2,
    )

    print(dataset.shape)
    print(dataset["label"].value_counts())

    for number, (train, test) in enumerate(folds, start=1):
        print(f"Fold {number}: {len(train)} train, {len(test)} test")

    #6 Get test and train sets

    train, test = folds[0]

    sampled_entries = sequential_bootstrap(
        events=train,
        n_prices=len(prices),
        sample_size=len(train),
        seed=42,
    )

    sampled_train = train.loc[sampled_entries]

    #7 Get model data

    X_train = sampled_train[["momentum","volatility_20"]]
    Y_train = sampled_train["label"]

    X_test = test[["momentum","volatility_20"]]
    Y_test = test["label"]

    print(X_train.shape, Y_train.shape)
    print(X_test.shape, Y_test.shape)

    # decision tree classifier

    majority_label = train["label"].mode().iloc[0]
    baseline_accuracy = np.mean(Y_test.to_numpy() == majority_label)

    results = []
    oof_predictions = pd.Series(index=dataset.index, dtype=float)

    for fold_number, (train, test) in enumerate(folds, start=1):

        sampled_entries = sequential_bootstrap(
            events=train,
            n_prices=len(prices),
            sample_size=len(train),
            seed=42,
        )

        sampled_train = train.loc[sampled_entries]

        assert sampled_train.index.intersection(test.index).empty

        X_train = sampled_train[["momentum","volatility_20"]]
        Y_train = sampled_train["label"]

        X_test = test[["momentum","volatility_20"]]
        Y_test = test["label"]

        model = DecisionTreeClassifier(
            max_depth=3,
            min_samples_leaf=20,
            random_state=42,
        )

        model.fit(X_train,Y_train)   # Learn from labelled examples
        y_pred = model.predict(X_test)       # Predict labels for supplied features

        accuracy = np.mean(y_pred == Y_test.to_numpy())
        print(f"Accuracy: {accuracy:.1%}")

        majority_label = train["label"].mode().iloc[0]
        baseline_accuracy = np.mean(Y_test.to_numpy() == majority_label)

        print(f"Majority label: {majority_label}")
        print(f"Baseline accuracy: {baseline_accuracy:.1%}")
        results.append({
            "fold": fold_number,
            "n_test": len(test),
            "accuracy": accuracy,
            "baseline_accuracy": baseline_accuracy,
        })

        oof_predictions.loc[test.index] = y_pred


if __name__ == "__main__":
    main()
