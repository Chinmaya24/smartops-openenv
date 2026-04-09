from __future__ import annotations
from typing import Any, Dict

TASK_NAME = "action_recommendation"

INPUT_EXAMPLE: Dict[str, Any] = {
    "subject": "Cannot login to account",
    "body": "I cannot access my account after password reset.",
    "customer_tier": "user",

    # ✅ REQUIRED
    "evaluation_rules": {
        "category": "technical",
        "response_keywords": ["help", "resolve", "support", "assist"],
        "escalated": False,
        "priority": 2,
    }
}

EXPECTED_OUTPUT: Dict[str, Any] = {
    "escalated": False,
}



