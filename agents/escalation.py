"""Escalation agent: escalation flag + priority (deterministic rules)."""

from __future__ import annotations

from typing import Any, Dict


def escalation_agent(memory: Dict[str, Any]) -> Dict[str, Any]:
    urgency = int(memory.get("urgency", 1))

    if urgency >= 4:
        return {"escalated": True, "priority": 3}   # ✅ fixed: was 5

    if urgency >= 3:
        return {"escalated": False, "priority": 2}  # ✅ fixed: was 3

    return {"escalated": False, "priority": 1}      # ✅ fixed: was 2