"""
Gate 1 — Contextual NLP Check (Ollama / Llama 3).

Sends a movie review to a locally-running Llama 3 model and receives
a structured JSON verdict: Verified or Quarantined.
"""

import json
import re

try:
    import ollama as ollama_lib
    OLLAMA_AVAILABLE = True
except ImportError:
    OLLAMA_AVAILABLE = False

from config import SYSTEM_PROMPT


def call_ollama(movie_title: str, review_text: str) -> dict:
    """Send a review through Gate 1 (Ollama / Llama 3) and return parsed JSON."""
    if not OLLAMA_AVAILABLE:
        return {
            "status": "Error",
            "confidence_score": 0,
            "reason": "Ollama Python library is not installed. Run: pip install ollama",
        }

    user_message = f'Movie: "{movie_title}"\nReview: "{review_text}"'

    try:
        response = ollama_lib.chat(
            model="llama3",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message},
            ],
        )
        raw = response["message"]["content"].strip()

        # Attempt to extract JSON from response (handle markdown wrapping)
        json_match = re.search(r'\{.*\}', raw, re.DOTALL)
        if json_match:
            parsed = json.loads(json_match.group())
        else:
            parsed = json.loads(raw)

        # Validate required keys
        for key in ("status", "confidence_score", "reason"):
            if key not in parsed:
                raise ValueError(f"Missing key: {key}")

        # Normalize status
        status = parsed["status"].strip().capitalize()
        if status not in ("Verified", "Quarantined"):
            status = "Quarantined"
        parsed["status"] = status
        parsed["confidence_score"] = int(parsed["confidence_score"])

        return parsed

    except Exception as e:
        err_str = str(e).lower()
        if "connect" in err_str or "refused" in err_str or "unreachable" in err_str:
            return {
                "status": "Error",
                "confidence_score": 0,
                "reason": "Cannot connect to Ollama. Is 'ollama serve' running?",
            }
        return {
            "status": "Error",
            "confidence_score": 0,
            "reason": f"NLP Gate error: {str(e)[:200]}",
        }


def run_nlp_gate(movie_title: str, review_text: str) -> dict:
    """Gate 1 wrapper. Returns dict with status, confidence_score, reason."""
    return call_ollama(movie_title, review_text)
