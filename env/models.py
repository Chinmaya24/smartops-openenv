from pydantic import BaseModel
from typing import Dict, Any, Optional


class Observation(BaseModel):
    email: Dict[str, Any]
    current_agent: str
    shared_memory: Dict[str, Any]
    step_count: int


class Action(BaseModel):
    agent: str
    action_type: str

    category: Optional[str] = None
    response_text: Optional[str] = None
    priority: Optional[int] = None


class Reward(BaseModel):
    score: float
    feedback: str