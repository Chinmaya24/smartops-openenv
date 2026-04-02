from __future__ import annotations

from typing import Any, Dict

TASK_NAME = "email_classification"

INPUT_EXAMPLE: Dict[str, Any] = {
    "subject": "Refund needed for duplicate charge",
    "body": "I was charged twice for my subscription.",
    "customer_tier": "user",
}

EXPECTED_OUTPUT: Dict[str, Any] = {
    "category": "billing",
}


def grade(output: Dict[str, Any]) -> float:
    category = str(output.get("category", "")).lower()
    return 1.0 if category == "billing" else 0.0
