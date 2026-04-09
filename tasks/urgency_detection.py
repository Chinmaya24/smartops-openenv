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



