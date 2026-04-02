"""Triage agent: category + urgency (deterministic rules, no external API)."""

from __future__ import annotations

from typing import Any, Dict


def triage_agent(email: Dict[str, Any]) -> Dict[str, Any]:
    subject = str(email.get("subject", ""))
    body = str(email.get("body", ""))
    text = f"{subject} {body}".lower()

    if any(
        k in text
        for k in (
            "system down",
            "outage",
            "offline",
            "not working",
            "losing money",
            "production",
            "completely down",
            "platform is down",
        )
    ):
        return {"category": "technical", "urgency": 5}

    if any(k in text for k in ("refund", "charged", "billing", "payment", "overcharge", "double")):
        return {"category": "billing", "urgency": 2}

    if any(k in text for k in ("login", "password", "sign in", "access", "account", "locked")):
        return {"category": "technical", "urgency": 3}

    return {"category": "general", "urgency": 1}
