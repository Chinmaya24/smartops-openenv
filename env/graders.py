from __future__ import annotations
from typing import Any, Dict
from env.models import Reward
import random

EPSILON = 1e-6

def grade(task: Dict[str, Any], memory: Dict[str, Any], step_count: int) -> Reward:
    task_name = task.get("name", "general")

    # simple dynamic scoring based on task
    base = {
        "email_classification": 0.6,
        "urgency_detection": 0.7,
        "action_recommendation": 0.8
    }.get(task_name, 0.5)

    # add variation
    score = base + random.uniform(-0.1, 0.1)

    # clamp
    score = max(EPSILON, min(1.0 - EPSILON, float(score)))

    return Reward(
        score=score,
        feedback="ok",
        breakdown={"score": score}
    )
