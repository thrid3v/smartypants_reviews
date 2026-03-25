"""Defense gates sub-package."""

from smartypants_reviews.gates.nlp_gate import run_nlp_gate
from smartypants_reviews.gates.velocity_gate import run_velocity_gate
from smartypants_reviews.gates.duplication_gate import run_duplication_gate

__all__ = ["run_nlp_gate", "run_velocity_gate", "run_duplication_gate"]
