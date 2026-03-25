"""
Session state initialization for the Streamlit app.
"""

import pandas as pd
import streamlit as st


def init_session_state():
    """Initialize session state variables if they don't exist."""
    if "verified_db" not in st.session_state:
        st.session_state.verified_db = pd.DataFrame(
            columns=["timestamp", "movie", "review", "rating", "confidence", "reason", "source"]
        )
    if "quarantine_db" not in st.session_state:
        st.session_state.quarantine_db = pd.DataFrame(
            columns=["timestamp", "movie", "review", "rating", "confidence", "reason", "gate_failed", "source"]
        )
    if "sim_running" not in st.session_state:
        st.session_state.sim_running = False
