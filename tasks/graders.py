from __future__ import annotations

from typing import Any, Dict


def _clamp_score(score: float) -> float:
    return max(0.1, min(0.9, score))


def grade_task(task_name: str, structured_result: Dict[str, Any]) -> float:
    task_input = structured_result.get("task", {}) or {}
    memory = structured_result.get("memory", {}) or {}
    evaluation_rules = task_input.get("evaluation_rules", {}) or {}

    if task_name == "email_classification":
        expected_category = str(evaluation_rules.get("category", "")).lower()
        actual_category = str(memory.get("category", "")).lower()
        return _clamp_score(0.8 if actual_category == expected_category else 0.2)

    if task_name == "urgency_detection":
        expected_priority = int(evaluation_rules.get("priority", 0))
        actual_priority = int(memory.get("priority", 0))
        return _clamp_score(0.8 if actual_priority == expected_priority else 0.2)

    if task_name == "action_recommendation":
        expected_escalated = bool(evaluation_rules.get("escalated", False))
        actual_escalated = bool(memory.get("escalated", False))
        response = str(memory.get("response", "")).lower()
        keywords = [str(k).lower() for k in evaluation_rules.get("response_keywords", []) if isinstance(k, str)]
        has_keyword = any(keyword in response for keyword in keywords)

        if actual_escalated == expected_escalated and has_keyword:
            return _clamp_score(0.8)
        if actual_escalated == expected_escalated:
            return _clamp_score(0.7)
        return _clamp_score(0.2)

    raise ValueError(f"Unknown task: {task_name}")
