"""
Hero banner and status bar UI component.
"""

import streamlit as st

from smartypants_reviews.gates.nlp_gate import OLLAMA_AVAILABLE


def render_hero():
    """Render the hero banner and system status bar."""
    st.markdown("""
    <div class="hero-banner">
        <div class="hero-title">🛡️ SMARTY PANTS</div>
        <div class="hero-subtitle">AI Review Defender · Three-Gate Defense Pipeline</div>
        <div class="hero-badge">▸ GATE 1: NLP (Llama 3) &nbsp;·&nbsp; GATE 2: Velocity (Isolation Forest) &nbsp;·&nbsp; GATE 3: Duplication</div>
    </div>
    """, unsafe_allow_html=True)

    # ── Status Bar ──
    ollama_status = "online" if OLLAMA_AVAILABLE else "offline"
    ollama_label = "OLLAMA CONNECTED" if OLLAMA_AVAILABLE else "OLLAMA OFFLINE"
    st.markdown(f"""
    <div class="status-bar">
        <span class="status-dot {ollama_status}"></span>
        <span>{ollama_label}</span>
        <span style="margin-left: auto; color: var(--text-muted);">
            Verified: {len(st.session_state.verified_db)} &nbsp;│&nbsp; Quarantined: {len(st.session_state.quarantine_db)}
        </span>
    </div>
    """, unsafe_allow_html=True)
