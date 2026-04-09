"""Strict Pydantic models for OpenEnv observation, action, and reward."""

from __future__ import annotations

import math
from typing import Any, Dict, Literal, Optional

from pydantic import BaseModel, Field, field_validator

_SCORE_EPSILON = 1e-3


class Observation(BaseModel):
    """Environment observation after reset or step."""

    model_config = {"extra": "forbid"}

    email: Dict[str, Any] = Field(description="Current email payload (subject, body, customer_tier).")
    current_agent: str = Field(description="Agent whose turn it is.")
    shared_memory: Dict[str, Any] = Field(default_factory=dict, description="Cross-agent working state.")
    step_count: int = Field(ge=0, description="Number of steps taken this episode.")
    task_name: Optional[str] = Field(default=None, description="Active benchmark task id, if any.")


class Action(BaseModel):
    """Agent action."""

    model_config = {"extra": "forbid"}

    agent: Literal["triage", "response", "escalation", "manager"]
    action_type: Literal["route", "respond", "escalate", "finalize", "auto"] = "auto"
    category: Optional[str] = None
    response_text: Optional[str] = None
    priority: Optional[int] = None


class Reward(BaseModel):
    """Scalar reward with optional breakdown for debugging."""

    model_config = {"extra": "forbid"}

    score: float = Field(description="Total score strictly in (0, 1).")
    feedback: str = ""
    breakdown: Dict[str, float] = Field(default_factory=dict, description="Per-component contributions.")

    @staticmethod
    def _strict_score(value: Any) -> float:
        """Normalize scores so they are always finite and strictly inside (0, 1)."""
        try:
            score = float(value)
        except (TypeError, ValueError):
            return 0.5

        if not math.isfinite(score):
            return 0.5

        return max(_SCORE_EPSILON, min(1.0 - _SCORE_EPSILON, score))

    @field_validator("score", mode="before")
    @classmethod
    def validate_score(cls, value: Any) -> float:
        return cls._strict_score(value)

    @field_validator("breakdown", mode="before")
    @classmethod
    def validate_breakdown(cls, value: Any) -> Dict[str, float]:
        if not isinstance(value, dict):
            return {}
        return {str(k): cls._strict_score(v) for k, v in value.items()}
