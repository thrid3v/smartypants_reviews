"""Defense gates sub-package."""

from gates.nlp_gate import run_nlp_gate
from gates.velocity_gate import run_velocity_gate
from gates.duplication_gate import run_duplication_gate

__all__ = ["run_nlp_gate", "run_velocity_gate", "run_duplication_gate"]
