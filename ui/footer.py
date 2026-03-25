"""
Footer UI component.
"""

import streamlit as st


def render_footer():
    """Render the application footer."""
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; padding: 1rem; font-family: 'JetBrains Mono', monospace; font-size: 0.7rem; color: var(--text-muted);">
        SMARTY PANTS REVIEWS v2.0 · Three-Gate AI Defense Pipeline · Llama 3 + Isolation Forest + Duplication Detection<br/>
        Built for demonstration purposes · Not for production use
    </div>
    """, unsafe_allow_html=True)
