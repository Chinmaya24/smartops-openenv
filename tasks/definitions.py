"""Benchmark tasks: email input, expected outputs, and evaluation rules."""

from __future__ import annotations

from typing import Any, Dict, List

# Each task includes email_input, expected_outputs, and evaluation_rules for grading.

TASKS: List[Dict[str, Any]] = [
    {
        "name": "refund_request",
        "difficulty": "easy",
        "email_input": {
            "subject": "Refund needed",
            "body": "I was charged twice for my order.",
            "customer_tier": "user",
        },
        "expected_outputs": {
            "category": "billing",
            "urgency_min": 1,
            "urgency_max": 3,
            "escalated": False,
            "priority": 2,
        },
        "evaluation_rules": {
            "category": "billing",
            "response_keywords": ["refund", "processing", "charge"],
            "escalated": False,
            "priority": 2,
        },
    },
    {
        "name": "login_issue",
        "difficulty": "medium",
        "email_input": {
            "subject": "Cannot login",
            "body": "I am unable to access my account.",
            "customer_tier": "user",
        },
        "expected_outputs": {
            "category": "technical",
            "urgency": 3,
            "escalated": False,
            "priority": 3,
        },
        "evaluation_rules": {
            "category": "technical",
            "response_keywords": ["help", "resolve", "issue", "account"],
            "escalated": False,
            "priority": 3,
        },
    },
    {
        "name": "system_outage",
        "difficulty": "hard",
        "email_input": {
            "subject": "URGENT: System down",
            "body": "Our production system is down and we are losing money.",
            "customer_tier": "premium",
        },
        "expected_outputs": {
            "category": "technical",
            "urgency": 5,
            "escalated": True,
            "priority": 5,
        },
        "evaluation_rules": {
            "category": "technical",
            "response_keywords": ["fix", "fixing", "urgent", "aware", "issue"],
            "escalated": True,
            "priority": 5,
        },
    },
]


def get_task_by_name(name: str) -> Dict[str, Any]:
    for t in TASKS:
        if t["name"] == name:
            return t
    raise KeyError(f"Unknown task: {name}")


def resolve_task_for_email(email: Dict[str, Any]) -> Dict[str, Any]:
    """Deterministic task selection for API / production (no randomness)."""
    text = f"{email.get('subject', '')} {email.get('body', '')}".lower()
    outage_kw = (
        "system down",
        "outage",
        "offline",
        "not working",
        "losing money",
        "production",
        "completely down",
        "platform is down",
    )
    if any(k in text for k in outage_kw):
        return get_task_by_name("system_outage")
    refund_kw = ("refund", "charged twice", "double charge", "billing", "payment error", "overcharge")
    if any(k in text for k in refund_kw):
        return get_task_by_name("refund_request")
    login_kw = ("login", "password", "sign in", "access my account", "cannot access", "locked out")
    if any(k in text for k in login_kw):
        return get_task_by_name("login_issue")
    return get_task_by_name("refund_request")
