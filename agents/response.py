"""Response agent: draft reply from shared memory (deterministic templates)."""

from __future__ import annotations

from typing import Any, Dict


def response_agent(memory: Dict[str, Any]) -> str:
    category = str(memory.get("category", "general"))
    urgency = int(memory.get("urgency", 1))

    if category == "billing":
        return "We are processing your refund and will confirm once the adjustment is complete."

    if category == "technical" and urgency >= 4:
        return "We are aware of the issue and fixing it urgently."

    if category == "technical":
        return "We will help you resolve this issue with your account."

    return "Thank you for contacting support; we will respond shortly."
