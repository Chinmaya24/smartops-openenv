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

# ✅ IMPORTANT: never return 0 or 1
def grade(output: Dict[str, Any]) -> float:
    category = str(output.get("category", "")).lower()

    if category == "billing":
        return 0.9
    else:
        return 0.1