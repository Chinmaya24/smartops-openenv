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


def _safe_clamp(score: float) -> float:
    return max(0.001, min(0.999, float(score)))


def _extract_task_and_output(*args: Any, **kwargs: Any) -> tuple[Dict[str, Any], Dict[str, Any]]:
    task = kwargs.get("task")
    output = kwargs.get("output")
    if len(args) >= 2:
        task, output = args[0], args[1]
    elif len(args) == 1:
        maybe = args[0]
        if isinstance(maybe, dict) and any(k in maybe for k in ("priority", "escalated", "response")):
            output = maybe
        else:
            task = maybe
    task_dict = task if isinstance(task, dict) else {}
    output_dict = output if isinstance(output, dict) else {}
    return task_dict, output_dict


def grade(*args: Any, **kwargs: Any) -> float:
    try:
        task, output = _extract_task_and_output(*args, **kwargs)
        rules = task.get("evaluation_rules", {}) if isinstance(task, dict) else {}

        def _safe_int(value: Any, default: int = 0) -> int:
            try:
                return int(value)
            except (TypeError, ValueError):
                return default

        expected_escalated = bool(rules.get("escalated", False))
        expected_priority = _safe_int(rules.get("priority", 0))
        actual_escalated = bool(output.get("escalated", False))
        actual_priority = _safe_int(output.get("priority", 0))
        response = str(output.get("response", "")).lower()
        raw_keywords = rules.get("response_keywords", [])
        keywords = [str(k).lower() for k in raw_keywords] if isinstance(raw_keywords, list) else []
        has_keywords = any(keyword in response for keyword in keywords)

        if actual_escalated == expected_escalated and actual_priority == expected_priority and has_keywords:
            score = 0.9
        elif actual_escalated == expected_escalated and actual_priority == expected_priority:
            score = 0.7
        elif actual_escalated == expected_escalated or actual_priority == expected_priority:
            score = 0.5
        else:
            score = 0.2

        return _safe_clamp(score)
    except Exception:
        return 0.5



