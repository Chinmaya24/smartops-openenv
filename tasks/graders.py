from __future__ import annotations
from typing import Any, Dict


def _clamp(score: float) -> float:
    return max(0.1, min(0.9, score))


def grade_task(task_name: str, result: Dict[str, Any]) -> float:
    """Generic dispatcher — called by validator as grade_task(task_name, result)."""
    if task_name == "email_classification":
        return grade_email_classification(result)
    if task_name == "urgency_detection":
        return grade_urgency_detection(result)
    if task_name == "action_recommendation":
        return grade_action_recommendation(result)
    raise ValueError(f"Unknown task: {task_name}")


def grade_email_classification(result: Dict[str, Any]) -> float:
    memory = result.get("memory", result)
    task_input = result.get("task", {})
    rules = task_input.get("evaluation_rules", {})
    expected = str(rules.get("category", "billing")).lower()
    actual = str(memory.get("category", "")).lower()
    return _clamp(0.8 if actual == expected else 0.2)


def grade_urgency_detection(result: Dict[str, Any]) -> float:
    memory = result.get("memory", result)
    task_input = result.get("task", {})
    rules = task_input.get("evaluation_rules", {})
    expected_priority = int(rules.get("priority", 0))
    actual_priority = int(memory.get("priority", 0))
    return _clamp(0.8 if actual_priority == expected_priority else 0.2)


def grade_action_recommendation(result: Dict[str, Any]) -> float:
    memory = result.get("memory", result)
    task_input = result.get("task", {})
    rules = task_input.get("evaluation_rules", {})
    expected_escalated = bool(rules.get("escalated", False))
    actual_escalated = bool(memory.get("escalated", False))
    response = str(memory.get("response", "")).lower()
    keywords = [str(k).lower() for k in rules.get("response_keywords", [])]
    has_keyword = any(kw in response for kw in keywords)
    if actual_escalated == expected_escalated and has_keyword:
        return _clamp(0.8)
    if actual_escalated == expected_escalated:
        return _clamp(0.6)
    return _clamp(0.2)