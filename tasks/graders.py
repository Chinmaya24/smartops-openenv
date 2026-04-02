from __future__ import annotations

from typing import Any, Dict

from tasks.action_recommendation import grade as grade_action_recommendation
from tasks.email_classification import grade as grade_email_classification
from tasks.urgency_detection import grade as grade_urgency_detection


def grade_task(task_name: str, output: Dict[str, Any]) -> float:
    if task_name == "email_classification":
        return grade_email_classification(output)
    if task_name == "urgency_detection":
        return grade_urgency_detection(output)
    if task_name == "action_recommendation":
        return grade_action_recommendation(output)
    return 0.0
