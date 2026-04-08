from __future__ import annotations
from typing import Any, Dict

TASK_NAME = "email_classification"

INPUT_EXAMPLE: Dict[str, Any] = {
    "subject": "Refund needed for duplicate charge",
    "body": "I was charged twice for my subscription.",
    "customer_tier": "user",

    # ✅ REQUIRED
    "evaluation_rules": {
        "category": "billing",
        "response_keywords": ["refund", "billing", "payment"],
        "escalated": False,
        "priority": 1,
    }
}

EXPECTED_OUTPUT: Dict[str, Any] = {
    "category": "billing",
}


def grade(result: Dict[str, Any]) -> float:
    """Delegate to centralized grader in tasks/graders.py"""
    from tasks.graders import grade_email_classification
    return grade_email_classification(result)
