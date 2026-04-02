from __future__ import annotations

from typing import Any, Dict

TASK_NAME = "action_recommendation"

INPUT_EXAMPLE: Dict[str, Any] = {
    "subject": "Cannot login to account",
    "body": "I cannot access my account after password reset.",
    "customer_tier": "user",
}

EXPECTED_OUTPUT: Dict[str, Any] = {
    "escalated": False,
    "priority_max": 3,
}


def grade(output: Dict[str, Any]) -> float:
    score = 0.0
    escalated = bool(output.get("escalated", False))
    priority = int(output.get("priority", 0) or 0)
    response = str(output.get("response", "")).lower()

    if not escalated:
        score += 0.4
    if priority <= 3 and priority > 0:
        score += 0.3
    if any(k in response for k in ("help", "resolve", "support", "assist")):
        score += 0.3
    return max(0.0, min(1.0, score))
