from __future__ import annotations
from typing import Any, Dict

TASK_NAME = "urgency_detection"

INPUT_EXAMPLE: Dict[str, Any] = {
    "subject": "Server down",
    "body": "My website is down, fix ASAP!",
    "customer_tier": "premium",
    "evaluation_rules": {
        "category": "technical",
        "response_keywords": ["urgent", "asap", "immediately"],
        "escalated": True,
        "priority": 5,
    }
}

EXPECTED_OUTPUT: Dict[str, Any] = {
    "priority": 5,
}

def grade(result: Dict[str, Any]) -> float:
    """Delegate to centralized grader in tasks/graders.py"""
    from tasks.graders import grade_urgency_detection
    return grade_urgency_detection(result)
