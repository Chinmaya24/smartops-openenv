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


def _safe_clamp(score: float) -> float:
    return max(0.001, min(0.999, float(score)))


def _extract_task_and_output(*args: Any, **kwargs: Any) -> tuple[Dict[str, Any], Dict[str, Any]]:
    task = kwargs.get("task")
    output = kwargs.get("output")
    if len(args) >= 2:
        task, output = args[0], args[1]
    elif len(args) == 1:
        maybe = args[0]
        if isinstance(maybe, dict) and "category" in maybe:
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
        expected = str(rules.get("category", "")).lower()
        actual = str(output.get("category", "")).lower()
        score = 0.9 if actual == expected else 0.2
        return _safe_clamp(score)
    except Exception:
        return 0.5



