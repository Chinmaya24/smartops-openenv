from __future__ import annotations
from typing import Any, Dict

TASK_NAME = "urgency_detection"

INPUT_EXAMPLE: Dict[str, Any] = {
    "subject": "Server down",
    "body": "My website is down, fix ASAP!",
    "customer_tier": "premium",

    # ✅ REQUIRED
    "evaluation_rules": {
        "category": "technical",
        "response_keywords": ["urgent", "asap", "immediately"],
        "escalated": True,
        "priority": 2,
    }
}

EXPECTED_OUTPUT: Dict[str, Any] = {
    "priority": 2,
}
