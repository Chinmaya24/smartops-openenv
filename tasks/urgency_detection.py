from __future__ import annotations
from typing import Any, Dict

TASK_NAME = "urgency_detection"

INPUT_EXAMPLE: Dict[str, Any] = {
    "subject": "URGENT: Production server is down",
    "body": "Our production environment has been completely unavailable for 30 minutes. All users are affected.",
    "customer_tier": "enterprise",

    # ✅ REQUIRED
    "evaluation_rules": {
        "category": "technical",
        "response_keywords": ["escalate", "urgent", "critical"],
        "escalated": True,
        "priority": 3,
    }
}

EXPECTED_OUTPUT: Dict[str, Any] = {
    "priority": 3,
    "escalated": True,
}


def _safe_clamp(score: float) -> float:
    return max(0.001, min(0.999, float(score)))


def _extract_task_and_output(*args: Any, **kwargs: Any) -> tuple[Dict[str, Any], Dict[str, Any]]:
    task = kwargs.get("task")
    output = kwargs.get("output")
    if len(args) >= 2:
        task, output = args[0], args[1]
    elif len(args) == 1:
        maybe = args[0]
        if isinstance(maybe, dict) and any(k in maybe for k in ("priority", "escalated")):
            output = maybe
        else:
            task = maybe
    return (task or {}, output or {})


def grade(*args: Any, **kwargs: Any) -> float:
    task, output = _extract_task_and_output(*args, **kwargs)
    rules = task.get("evaluation_rules", {})
    expected_priority = int(rules.get("priority", 0))
    expected_escalated = bool(rules.get("escalated", False))
    actual_priority = int(output.get("priority", 0))
    actual_escalated = bool(output.get("escalated", False))

    if actual_priority == expected_priority and actual_escalated == expected_escalated:
        score = 0.9
    elif actual_priority == expected_priority or actual_escalated == expected_escalated:
        score = 0.6
    else:
        score = 0.2

    return _safe_clamp(score)



