"""
Gate 3 — Content Duplication Detection (Time-Window Based).

Detects coordinated campaigns where many users post identical
(or near-identical) review text for the same movie within a
short time window. Even if the content sounds authentic,
abnormal repetition in a burst is a red flag.
"""

from datetime import datetime, timedelta

import pandas as pd
import streamlit as st


def _normalize(text: str) -> str:
    """Lowercase, strip, collapse whitespace for fuzzy matching."""
    return " ".join(text.strip().lower().split())


def run_duplication_gate(
    movie_title: str,
    review_text: str,
    threshold: int = 5,
    window_minutes: int = 30,
) -> dict:
    """
    Gate 3: Check if the same review text has appeared too many times
    for the same movie **within a rolling time window**.

    Parameters
    ----------
    movie_title    : str
    review_text    : str
    threshold      : int – max allowed identical reviews within the window
    window_minutes : int – size of the rolling time window in minutes

    Returns
    -------
    dict with keys: passed (bool), count (int), reason (str)
    """
    normalized = _normalize(review_text)
    movie_lower = movie_title.strip().lower()
    cutoff = datetime.now() - timedelta(minutes=window_minutes)

    count = 0
    for db in [st.session_state.verified_db, st.session_state.quarantine_db]:
        if len(db) == 0:
            continue

        # Filter by movie and matching review text
        text_match = db[
            (db["movie"].str.strip().str.lower() == movie_lower)
            & (db["review"].str.strip().str.lower().apply(
                lambda r: " ".join(r.split())
            ) == normalized)
        ]

        if len(text_match) == 0:
            continue

        # Filter by time window
        try:
            timestamps = pd.to_datetime(text_match["timestamp"])
            recent = timestamps[timestamps >= cutoff]
            count += len(recent)
        except Exception:
            # If timestamp parsing fails, fall back to counting all matches
            count += len(text_match)

    if count >= threshold:
        preview = review_text[:40] + ("..." if len(review_text) > 40 else "")
        return {
            "passed": False,
            "count": count,
            "reason": (
                f"Duplicate content spike — \"{preview}\" appeared "
                f"{count}× in the last {window_minutes} min "
                f"(threshold: {threshold})"
            ),
        }

    return {
        "passed": True,
        "count": count,
        "reason": f"Content frequency normal ({count} in last {window_minutes} min)",
    }
