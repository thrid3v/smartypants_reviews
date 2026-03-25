"""
Custom CSS for the Streamlit UI.
"""

CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;500;600;700&family=Inter:wght@300;400;500;600;700&display=swap');

/* ── Root Variables ── */
:root {
    --bg-primary: #0a0e17;
    --bg-secondary: #111827;
    --bg-card: #1a1f2e;
    --bg-card-hover: #222838;
    --neon-green: #00ff88;
    --neon-green-dim: #00cc6a;
    --neon-red: #ff3366;
    --neon-red-dim: #cc2952;
    --neon-blue: #00d4ff;
    --neon-purple: #a855f7;
    --neon-amber: #ffaa00;
    --text-primary: #e2e8f0;
    --text-secondary: #94a3b8;
    --text-muted: #64748b;
    --border-color: #1e293b;
    --border-glow-green: rgba(0, 255, 136, 0.25);
    --border-glow-red: rgba(255, 51, 102, 0.25);
}

/* ── Global Overrides ── */
.stApp {
    background: var(--bg-primary) !important;
    color: var(--text-primary) !important;
    font-family: 'Inter', sans-serif !important;
}

header[data-testid="stHeader"] {
    background: transparent !important;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: var(--bg-primary); }
::-webkit-scrollbar-thumb { background: var(--text-muted); border-radius: 3px; }

/* ── Hero Banner ── */
.hero-banner {
    background: linear-gradient(135deg, #0a0e17 0%, #111827 40%, #0f172a 100%);
    border: 1px solid var(--border-color);
    border-radius: 16px;
    padding: 2.5rem 2rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}
.hero-banner::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, var(--neon-green), var(--neon-blue), var(--neon-purple));
}
.hero-title {
    font-family: 'JetBrains Mono', monospace;
    font-size: 2.2rem;
    font-weight: 700;
    background: linear-gradient(135deg, var(--neon-green) 0%, var(--neon-blue) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0 0 0.5rem 0;
    letter-spacing: -1px;
}
.hero-subtitle {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.95rem;
    color: var(--text-secondary);
    letter-spacing: 2px;
    text-transform: uppercase;
}
.hero-badge {
    display: inline-block;
    background: rgba(0, 255, 136, 0.1);
    border: 1px solid rgba(0, 255, 136, 0.3);
    color: var(--neon-green);
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.7rem;
    padding: 4px 10px;
    border-radius: 20px;
    margin-top: 0.8rem;
    letter-spacing: 1px;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    gap: 0;
    background: var(--bg-secondary);
    border-radius: 12px;
    padding: 4px;
    border: 1px solid var(--border-color);
}
.stTabs [data-baseweb="tab"] {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.85rem;
    font-weight: 500;
    color: var(--text-secondary);
    border-radius: 8px;
    padding: 0.6rem 1.5rem;
    letter-spacing: 0.5px;
}
.stTabs [aria-selected="true"] {
    background: var(--bg-card) !important;
    color: var(--neon-green) !important;
    border: 1px solid rgba(0, 255, 136, 0.2) !important;
}
.stTabs [data-baseweb="tab-highlight"] { display: none; }
.stTabs [data-baseweb="tab-border"] { display: none; }

/* ── Cards ── */
.gate-card {
    background: var(--bg-card);
    border: 1px solid var(--border-color);
    border-radius: 12px;
    padding: 1.5rem;
    margin-bottom: 1rem;
    transition: all 0.3s ease;
}
.gate-card:hover {
    border-color: rgba(0, 212, 255, 0.3);
    box-shadow: 0 0 20px rgba(0, 212, 255, 0.05);
}

/* ── Result Boxes ── */
.result-verified {
    background: linear-gradient(135deg, rgba(0, 255, 136, 0.05) 0%, rgba(0, 255, 136, 0.02) 100%);
    border: 1px solid rgba(0, 255, 136, 0.3);
    border-left: 4px solid var(--neon-green);
    border-radius: 12px;
    padding: 1.5rem;
    margin: 1rem 0;
}
.result-verified .result-header {
    font-family: 'JetBrains Mono', monospace;
    color: var(--neon-green);
    font-size: 1.1rem;
    font-weight: 600;
    margin-bottom: 0.8rem;
}

.result-quarantined {
    background: linear-gradient(135deg, rgba(255, 51, 102, 0.05) 0%, rgba(255, 51, 102, 0.02) 100%);
    border: 1px solid rgba(255, 51, 102, 0.3);
    border-left: 4px solid var(--neon-red);
    border-radius: 12px;
    padding: 1.5rem;
    margin: 1rem 0;
}
.result-quarantined .result-header {
    font-family: 'JetBrains Mono', monospace;
    color: var(--neon-red);
    font-size: 1.1rem;
    font-weight: 600;
    margin-bottom: 0.8rem;
}

.result-score {
    font-family: 'JetBrains Mono', monospace;
    font-size: 2rem;
    font-weight: 700;
    margin: 0.5rem 0;
}
.result-reason {
    font-family: 'Inter', sans-serif;
    color: var(--text-secondary);
    font-size: 0.9rem;
    line-height: 1.6;
    margin-top: 0.5rem;
}

/* ── Metric Cards ── */
.metric-card {
    background: var(--bg-card);
    border: 1px solid var(--border-color);
    border-radius: 12px;
    padding: 1.5rem;
    text-align: center;
}
.metric-card.verified {
    border-color: rgba(0, 255, 136, 0.3);
    box-shadow: 0 0 30px rgba(0, 255, 136, 0.08);
}
.metric-card.quarantined {
    border-color: rgba(255, 51, 102, 0.3);
    box-shadow: 0 0 30px rgba(255, 51, 102, 0.08);
}
.metric-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.75rem;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 0.5rem;
}
.metric-value {
    font-family: 'JetBrains Mono', monospace;
    font-size: 3rem;
    font-weight: 700;
    line-height: 1;
}
.metric-delta {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.85rem;
    margin-top: 0.3rem;
}

/* ── Status Bar ── */
.status-bar {
    background: var(--bg-secondary);
    border: 1px solid var(--border-color);
    border-radius: 8px;
    padding: 0.6rem 1rem;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.75rem;
    color: var(--text-muted);
    display: flex;
    align-items: center;
    gap: 0.5rem;
    margin-bottom: 1.5rem;
}
.status-dot {
    width: 8px; height: 8px;
    border-radius: 50%;
    display: inline-block;
    animation: pulse 2s infinite;
}
.status-dot.online { background: var(--neon-green); }
.status-dot.offline { background: var(--neon-red); }

@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.4; }
}

/* ── Dataframe styling ── */
.stDataFrame {
    border: 1px solid var(--border-color) !important;
    border-radius: 8px !important;
}

/* ── Log line ── */
.log-line {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.78rem;
    color: var(--text-secondary);
    padding: 2px 0;
    border-bottom: 1px solid rgba(255,255,255,0.03);
}
.log-line .ts {
    color: var(--text-muted);
}
.log-line .ok {
    color: var(--neon-green);
}
.log-line .fail {
    color: var(--neon-red);
}
.log-line .warn {
    color: var(--neon-amber);
}

/* ── Buttons ── */
.stButton > button {
    font-family: 'JetBrains Mono', monospace !important;
    font-weight: 600 !important;
    letter-spacing: 0.5px !important;
    border-radius: 8px !important;
    transition: all 0.3s ease !important;
}
div[data-testid="stFormSubmitButton"] > button,
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, var(--neon-green), var(--neon-green-dim)) !important;
    color: #0a0e17 !important;
    border: none !important;
}
div[data-testid="stFormSubmitButton"] > button:hover,
.stButton > button[kind="primary"]:hover {
    box-shadow: 0 0 25px rgba(0, 255, 136, 0.3) !important;
    transform: translateY(-1px) !important;
}

/* ── Section headers ── */
.section-header {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.8rem;
    color: var(--text-muted);
    letter-spacing: 3px;
    text-transform: uppercase;
    margin: 1.5rem 0 1rem 0;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid var(--border-color);
}

/* ── Input styling ── */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
    background: var(--bg-secondary) !important;
    border: 1px solid var(--border-color) !important;
    color: var(--text-primary) !important;
    font-family: 'Inter', sans-serif !important;
    border-radius: 8px !important;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: var(--neon-blue) !important;
    box-shadow: 0 0 10px rgba(0, 212, 255, 0.15) !important;
}

/* ── Progress bar ── */
.stProgress > div > div > div {
    background: linear-gradient(90deg, var(--neon-green), var(--neon-blue)) !important;
}

/* ── Simulation stream label ── */
.stream-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.75rem;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    padding: 4px 10px;
    border-radius: 4px;
    display: inline-block;
    margin-bottom: 0.5rem;
}
.stream-label.authentic {
    color: var(--neon-green);
    background: rgba(0,255,136,0.08);
    border: 1px solid rgba(0,255,136,0.2);
}
.stream-label.hater {
    color: var(--neon-red);
    background: rgba(255,51,102,0.08);
    border: 1px solid rgba(255,51,102,0.2);
}
.stream-label.astroturf {
    color: var(--neon-amber);
    background: rgba(255,170,0,0.08);
    border: 1px solid rgba(255,170,0,0.2);
}
</style>
"""
