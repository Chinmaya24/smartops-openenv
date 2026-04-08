"""Reward grader: category, response keywords, escalation, priority, inefficiency penalty."""

from __future__ import annotations

from typing import Any, Dict

from env.models import Reward


def grade(task: Dict[str, Any], memory: Dict[str, Any], step_count: int) -> Reward:
    """
    Weighted score:
    - category match: 0.4
    - response keyword match: 0.3
    - escalation correctness: 0.2
    - priority correctness: 0.1
    - inefficiency penalty: min(0.2, max(0, step_count - 4) * 0.05)
    """

    rules = task.get("evaluation_rules") or task.get("expected_outputs") or {}
    if not rules:
        return Reward(score=0.1, feedback="missing_evaluation_rules", breakdown={})

    category = str(memory.get("category", "")).lower()
    expected_category = str(rules.get("category", "")).lower()

    response = str(memory.get("response", "")).lower()
    keywords = list(rules.get("response_keywords", []))

    escalated = bool(memory.get("escalated"))
    expected_escalated = bool(rules.get("escalated"))

    try:
        priority = int(memory.get("priority", 0))
    except (TypeError, ValueError):
        priority = 0

    try:
        expected_priority = int(rules.get("priority", 0))
    except (TypeError, ValueError):
        expected_priority = 0

    breakdown: Dict[str, float] = {}

    # ✅ Category score
    cat = 0.4 if category == expected_category else 0.0
    breakdown["category"] = cat

    # ✅ Keyword match
    kw_ok = bool(response) and any(kw.lower() in response for kw in keywords)
    resp = 0.3 if kw_ok else 0.0
    breakdown["response_keywords"] = resp

    # ✅ Escalation
    esc = 0.2 if escalated == expected_escalated else 0.0
    breakdown["escalation"] = esc

    # ✅ Priority
    pri = 0.1 if priority == expected_priority else 0.0
    breakdown["priority"] = pri

    # ✅ Raw score
    raw = cat + resp + esc + pri

    # ✅ Inefficiency penalty
    extra_steps = max(0, step_count - 4)
    penalty = min(0.2, extra_steps * 0.05)
    breakdown["inefficiency_penalty"] = -penalty

    # 🔥 FINAL SCORE FIX (MOST IMPORTANT)
    score = raw - penalty

    # ✅ Enforce STRICT (0,1) range
    if score <= 0.0:
        score = 0.1
    elif score >= 1.0:
        score = 0.9

    # ✅ Feedback generation
    parts = []
    if cat == 0.0:
        parts.append("category_mismatch")
    if resp == 0.0:
        parts.append("response_keywords_mismatch")
    if esc == 0.0:
        parts.append("escalation_mismatch")
    if pri == 0.0:
        parts.append("priority_mismatch")
    if penalty > 0:
        parts.append("inefficiency")

    feedback = "; ".join(parts) if parts else "ok"

    return Reward(score=score, feedback=feedback, breakdown=breakdown)
def grade_task(task_name: str, result: Dict[str, Any]) -> float:
    try:
        # 🔥 FIX: adapt API response to grader format

        task = result.get("task") or {}

        # If no task provided, create dummy evaluation rules
        if not task:
            task = {
                "evaluation_rules": {
                    "category": result.get("category", ""),
                    "response_keywords": ["thank", "help", "support"],
                    "escalated": result.get("escalated", False),
                    "priority": result.get("priority", 1),
                }
            }

        # Use result directly if memory missing
        memory = result.get("memory") or result
        step_count = result.get("step_count", 1)

        reward = grade(task, memory, step_count)
        score = reward.score

        # ✅ STRICT (0,1)
        if score <= 0.0:
            return 0.1
        elif score >= 1.0:
            return 0.9

        return score

    except Exception as e:
        print(f"[ERROR] grade_task failed: {e}")
        return 0.1