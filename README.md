# 🛡️ Smarty Pants Reviews

**Three-Gate AI Defense Pipeline Against Review Data Poisoning**

Smarty Pants Reviews is a Streamlit application that defends movie-review databases against coordinated data-poisoning attacks (review-bombing & astroturfing) using a three-gate AI pipeline.

## Architecture

```
Gate 1 — Contextual NLP          →  Llama 3 via Ollama (authenticity analysis)
Gate 2 — Behavioral Velocity     →  Isolation Forest (timestamp anomaly detection)
Gate 3 — Content Duplication     →  Time-window duplicate detection (campaign flagging)
Switchboard                      →  Routes to Verified_DB or Quarantine_DB
```

### Project Structure

```
smartypants_reviews/            # Core package
├── __init__.py                 # Package metadata (v2.0.0)
├── config.py                   # Page config & system prompt
├── styles.py                   # Custom CSS
├── state.py                    # Session state initialization
├── gates/                      # Defense pipeline
│   ├── nlp_gate.py             # Gate 1: Ollama / Llama 3
│   ├── velocity_gate.py        # Gate 2: Isolation Forest
│   └── duplication_gate.py     # Gate 3: Time-window duplication
├── pipeline.py                 # Switchboard routing (all 3 gates)
├── mock_data.py                # Sample reviews & stream generators
└── ui/                         # Streamlit UI components
    ├── hero.py                 # Hero banner & status bar
    ├── sandbox.py              # Manual review evaluator
    ├── simulator.py            # Live attack simulator
    └── footer.py               # Footer
```

## Prerequisites

- **Python 3.10+**
- **Ollama** — must be installed and running locally (Gate 1 depends on it)

## Setup

### 1. Install Ollama

Download and install Ollama for your platform:

| Platform | Install |
|---|---|
| **Windows** | `irm https://ollama.com/install.ps1 \| iex` (PowerShell) or download from [ollama.com](https://ollama.com/download) |
| **macOS** | Download from [ollama.com](https://ollama.com/download) |
| **Linux** | `curl -fsSL https://ollama.com/install.sh \| sh` |

After installing, verify Ollama is running:
```bash
ollama --version
```

### 2. Pull the Llama 3 model

```bash
ollama pull llama3
```

> **Note:** The first pull downloads ~4.7 GB. Ollama must be running in the background (`ollama serve`) for the app to work.

### 3. Install Python dependencies

```bash
# Create a virtual environment (recommended)
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # macOS/Linux

# Install dependencies
pip install -r requirements.txt
```

### 4. Run the app

```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`. The status bar at the top shows whether Ollama is connected.

## Features

| Feature | Description |
|---|---|
| **Manual Sandbox** | Submit individual reviews for Gate 1 (NLP) and Gate 3 (duplication) analysis |
| **Live Attack Simulator** | Simulate attacks with selectable streams and custom target movie |
| **Stream Selection** | Toggle authentic, hater mob, and astroturf bot streams independently |
| **Stop Simulation** | Halt a running simulation and keep all data processed so far |
| **Real-time Tables** | Database tables refresh every 10 reviews during simulation |
| **Three-Gate Pipeline** | Reviews must pass NLP, velocity, and duplication checks to be verified |
| **Time-Window Duplication** | Flags identical reviews only when they spike within a rolling window |

## How the Gates Work

| Gate | What It Detects | Method |
|---|---|---|
| **Gate 1: NLP** | Inauthentic content (generic rage, astroturf buzzwords) | Llama 3 contextual analysis |
| **Gate 2: Velocity** | Abnormal posting speed (bots posting in milliseconds) | Isolation Forest on time-deltas |
| **Gate 3: Duplication** | Coordinated identical reviews within a time window | Content dedup with rolling window |

## License

MIT
