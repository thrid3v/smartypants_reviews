"""
Switchboard — Routes reviews to Verified_DB or Quarantine_DB.

A review must pass all three gates to be verified; failing any
gate sends it to quarantine.
"""

from datetime import datetime

import pandas as pd
import streamlit as st


def process_review(
    movie_title: str,
    review_text: str,
    rating: int,
    nlp_result: dict,
    velocity_flag: int,
    duplication_result: dict | None = None,
    source: str = "manual",
    ts: str | None = None,
) -> str:
    """
    Route a review to the correct database.
    A review must pass ALL three gates to be verified.

    Returns
    -------
    str : "Verified" or "Quarantined"
    """
    if duplication_result is None:
        duplication_result = {"passed": True, "count": 0, "reason": ""}
    timestamp = ts or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    nlp_passed = nlp_result.get("status") == "Verified"
    velocity_passed = velocity_flag == 1
    duplication_passed = duplication_result.get("passed", True)

    if nlp_passed and velocity_passed and duplication_passed:
        new_row = pd.DataFrame([{
            "timestamp": timestamp,
            "movie": movie_title,
            "review": review_text,
            "rating": rating,
            "confidence": nlp_result.get("confidence_score", 0),
            "reason": nlp_result.get("reason", ""),
            "source": source,
        }])
        st.session_state.verified_db = pd.concat(
            [st.session_state.verified_db, new_row], ignore_index=True
        )
        return "Verified"
    else:
        gate_failed = []
        if not nlp_passed:
            gate_failed.append("NLP")
        if not velocity_passed:
            gate_failed.append("Velocity")
        if not duplication_passed:
            gate_failed.append("Duplication")

        new_row = pd.DataFrame([{
            "timestamp": timestamp,
            "movie": movie_title,
            "review": review_text,
            "rating": rating,
            "confidence": nlp_result.get("confidence_score", 0),
            "reason": nlp_result.get("reason", "Velocity anomaly detected"),
            "gate_failed": " + ".join(gate_failed),
            "source": source,
        }])
        st.session_state.quarantine_db = pd.concat(
            [st.session_state.quarantine_db, new_row], ignore_index=True
        )
        return "Quarantined"
