"""
╔══════════════════════════════════════════════════════════════════╗
║   SMARTY PANTS REVIEWS — AI Review Defender                     ║
║   Three-Gate Defense Pipeline Against Data Poisoning             ║
║   Gate 1: Contextual NLP (Llama 3 via Ollama)                   ║
║   Gate 2: Behavioral Velocity Check (Isolation Forest)           ║
║   Gate 3: Content Duplication Detection (Time-Window)            ║
╚══════════════════════════════════════════════════════════════════╝

Entry point — run with: streamlit run app.py
"""

import streamlit as st

from config import PAGE_CONFIG
from state import init_session_state
from styles import CUSTOM_CSS
from ui.hero import render_hero
from ui.sandbox import render_sandbox_tab
from ui.simulator import render_simulator_tab
from ui.footer import render_footer

# ── Page Config ──
st.set_page_config(**PAGE_CONFIG)

# ── Inject CSS ──
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ── Session State ──
init_session_state()

# ── Hero Banner & Status Bar ──
render_hero()

# ── Tabs ──
tab1, tab2 = st.tabs(["🔬  MANUAL SANDBOX", "⚡  LIVE ATTACK SIMULATOR"])

with tab1:
    render_sandbox_tab()

with tab2:
    render_simulator_tab()

# ── Footer ──
render_footer()
