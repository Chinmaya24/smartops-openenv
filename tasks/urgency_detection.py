from __future__ import annotations

from typing import Any, Dict

TASK_NAME = "urgency_detection"

INPUT_EXAMPLE: Dict[str, Any] = {
    "subject": "URGENT: System outage in production",
    "body": "Our platform is down and customers cannot pay.",
    "customer_tier": "premium",
}

EXPECTED_OUTPUT: Dict[str, Any] = {
    "urgency_min": 4,
}


def grade(output: Dict[str, Any]) -> float:
    urgency = int(output.get("urgency", 0) or 0)
    if urgency >= 5:
        return 1.0
    if urgency >= 4:
        return 0.9
    if urgency >= 3:
        return 0.5
    return 0.0
