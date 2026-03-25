"""
Gate 2 — Behavioral Velocity Check (Isolation Forest).

Detects per-movie bursts of rapid-fire reviews using
time-delta analysis and Isolation Forest anomaly scoring.
"""

from collections import defaultdict

import numpy as np
from sklearn.ensemble import IsolationForest


def run_velocity_gate(
    timestamps: list[float],
    movies: list[str] | None = None,
    burst_threshold: int = 10,
    min_gap: float = 2.0,
) -> list[int]:
    """
    Detect anomalous posting velocity.

    When movie titles are provided, performs per-movie burst detection:
    movies with many reviews arriving faster than min_gap seconds
    are flagged as a coordinated attack.

    Parameters
    ----------
    timestamps      : list of float (epoch seconds)
    movies          : optional list of movie titles (same length as timestamps)
    burst_threshold : min reviews per movie before burst detection kicks in
    min_gap         : minimum seconds between reviews to be considered normal

    Returns
    -------
    list of int : 1 = normal velocity, -1 = anomalous (too fast)
    """
    n = len(timestamps)
    if n < 5:
        return [1] * n

    labels = [1] * n

    if movies is not None and len(movies) == n:
        # ── Per-movie burst detection ──
        movie_groups: dict[str, list[tuple[int, float]]] = defaultdict(list)
        for i, (ts, movie) in enumerate(zip(timestamps, movies)):
            movie_groups[movie.strip().lower()].append((i, ts))

        for movie, entries in movie_groups.items():
            if len(entries) <= burst_threshold:
                # Small batch — not enough to be a coordinated attack
                continue

            indices, ts_values = zip(*entries)
            ts_arr = np.array(ts_values)
            ts_sorted = np.sort(ts_arr)

            # Compute inter-review deltas for this movie
            deltas = np.diff(ts_sorted)
            if len(deltas) == 0:
                continue

            median_delta = float(np.median(deltas))

            if median_delta < min_gap:
                # Median gap is very small → coordinated rapid-fire attack
                # Use Isolation Forest to find any that might be legitimate
                deltas_full = np.concatenate([[median_delta], deltas])
                X = deltas_full.reshape(-1, 1)

                model = IsolationForest(
                    n_estimators=100,
                    contamination="auto",
                    random_state=42,
                )
                model.fit(X)
                scores = model.decision_function(X)

                # Sort entries by timestamp to align with deltas
                sorted_entry_indices = np.argsort(ts_arr)
                for j, sorted_idx in enumerate(sorted_entry_indices):
                    orig_idx = indices[sorted_idx]
                    delta = deltas_full[j]
                    # Flag if delta is below the minimum gap
                    if delta < min_gap:
                        labels[orig_idx] = -1
                    # Otherwise keep as 1 (normal)
            # else: median gap is healthy — reviews are well-spaced, pass all

    else:
        # ── Fallback: global timestamp analysis (sorted) ──
        ts = np.array(timestamps)
        sorted_indices = np.argsort(ts)
        ts_sorted = ts[sorted_indices]

        deltas = np.diff(ts_sorted)
        median_delta = float(np.median(deltas)) if len(deltas) > 0 else 1.0
        deltas_full = np.concatenate([[median_delta], deltas])

        X = deltas_full.reshape(-1, 1)
        model = IsolationForest(
            n_estimators=100,
            contamination="auto",
            random_state=42,
        )
        model.fit(X)

        sorted_labels = np.where(deltas_full >= min_gap, 1, -1)

        for i, orig_idx in enumerate(sorted_indices):
            labels[orig_idx] = int(sorted_labels[i])

    return labels
