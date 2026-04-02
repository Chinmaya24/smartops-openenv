"""Strict Pydantic models for OpenEnv observation, action, and reward."""

from __future__ import annotations

from typing import Any, Dict, Literal, Optional

from pydantic import BaseModel, Field


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

    score: float = Field(ge=0.0, le=1.0, description="Total score in [0, 1].")
    feedback: str = ""
    breakdown: Dict[str, float] = Field(default_factory=dict, description="Per-component contributions.")
