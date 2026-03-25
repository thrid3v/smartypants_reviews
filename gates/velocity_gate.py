"""
Gate 2 — Behavioral Velocity Check (Isolation Forest).

Detects anomalous posting velocity by analysing inter-review
time-deltas with an Isolation Forest model.
"""

import numpy as np
from sklearn.ensemble import IsolationForest


def run_velocity_gate(timestamps: list[float]) -> list[int]:
    """
    Analyse inter-review time-deltas with Isolation Forest.

    Parameters
    ----------
    timestamps : list of float (epoch seconds)

    Returns
    -------
    list of int : 1 = normal velocity, -1 = anomalous (too fast)
    """
    if len(timestamps) < 5:
        # Not enough data to run anomaly detection — pass all
        return [1] * len(timestamps)

    ts = np.array(timestamps)
    deltas = np.diff(ts)
    # Pad first element with median delta so arrays align
    median_delta = np.median(deltas) if len(deltas) > 0 else 1.0
    deltas = np.concatenate([[median_delta], deltas])

    # Feature matrix: each review gets its own delta
    X = deltas.reshape(-1, 1)

    model = IsolationForest(
        n_estimators=100,
        contamination=0.3,  # expect ~30% anomalies in attack scenario
        random_state=42,
    )
    labels = model.fit_predict(X)
    return labels.tolist()
