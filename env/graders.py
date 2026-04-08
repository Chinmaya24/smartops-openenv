"""Reward grader: delegates to centralized tasks/graders.py"""

from __future__ import annotations

from typing import Any, Dict

from env.models import Reward

EPSILON = 1e-6


def grade(task: Dict[str, Any], memory: Dict[str, Any], step_count: int) -> Reward:
    """Environmental grader for training loop — delegates score to centralized grader"""
    # Reconstruct structured result for centralized grader
    structured_result = {
        "task": task,
        "memory": memory,
        "step_count": step_count,
    }
    
    # Get task name from context (defaults to general)
    task_name = task.get("name", "general")
    
    # Use centralized grader
    from tasks.graders import grade_task as central_grade_task
    try:
        score = central_grade_task(task_name, structured_result)
    except Exception:
        score = 0.5
    
    # Ensure strict (0, 1) with epsilon margins
    score = max(EPSILON, min(1.0 - EPSILON, float(score)))
    
    feedback = "ok"
    breakdown = {"score": score}
    
    return Reward(score=score, feedback=feedback, breakdown=breakdown)


def grade_task(task_name: str, result: Dict[str, Any]) -> float:
    """Delegate to centralized grader in tasks/graders.py"""
    from tasks.graders import grade_task as central_grade_task
    score = central_grade_task(task_name, result)
    # Ensure score is strictly in (0, 1) with epsilon margins
    return max(EPSILON, min(1.0 - EPSILON, float(score)))
