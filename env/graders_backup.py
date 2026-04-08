"""Reward grader: category, response keywords, escalation, priority, inefficiency penalty."""

from __future__ import annotations

from typing import Any, Dict

from env.models import Reward


def grade(task: Dict[str, Any], memory: Dict[str, Any], step_count: int) -> Reward:
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
    except:
        priority = 0

    try:
        expected_priority = int(rules.get("priority", 0))
    except:
        expected_priority = 0

    breakdown: Dict[str, float] = {}

    cat = 0.4 if category == expected_category else 0.0
    resp = 0.3 if any(kw.lower() in response for kw in keywords) else 0.0
    esc = 0.2 if escalated == expected_escalated else 0.0
    pri = 0.1 if priority == expected_priority else 0.0

    breakdown["category"] = cat
    breakdown["response_keywords"] = resp
    breakdown["escalation"] = esc
    breakdown["priority"] = pri

    raw = cat + resp + esc + pri

    extra_steps = max(0, step_count - 4)
    penalty = min(0.2, extra_steps * 0.05)
    breakdown["inefficiency_penalty"] = -penalty

    score = raw - penalty

    # ✅ STRICT RANGE
    if score <= 0.0:
        score = 0.1
    elif score >= 1.0:
        score = 0.9

    feedback = "ok"
    return Reward(score=score, feedback=feedback, breakdown=breakdown)


def grade_task(task_name: str, result: Dict[str, Any]) -> float:
    try:
        # 🔥 TASK-SPECIFIC RULES (CRITICAL)
        if task_name == "email_classification":
            task = {
                "evaluation_rules": {
                    "category": "billing",
                    "response_keywords": ["invoice", "payment", "billing"],
                    "escalated": False,
                    "priority": 1,
                }
            }

        elif task_name == "urgency_detection":
            task = {
                "evaluation_rules": {
                    "category": "technical",
                    "response_keywords": ["urgent", "asap", "immediately"],
                    "escalated": True,
                    "priority": 2,
                }
            }

        elif task_name == "action_recommendation":
            task = {
                "evaluation_rules": {
                    "category": "general",
                    "response_keywords": ["assist", "resolve", "help"],
                    "escalated": False,
                    "priority": 1,
                }
            }

        else:
            task = {
                "evaluation_rules": {
                    "category": "general",
                    "response_keywords": ["help"],
                    "escalated": False,
                    "priority": 1,
                }
            }

        # ✅ FORCE MEMORY STRUCTURE
        memory = result.get("memory", {})

        memory = {
            "category": memory.get("category") or result.get("category", "general"),
            "response": memory.get("response") or result.get("response", "we will help you"),
            "escalated": memory.get("escalated") if "escalated" in memory else result.get("escalated", False),
            "priority": memory.get("priority") or result.get("priority", 1),
        }

        step_count = result.get("step_count", 1)

        reward = grade(task, memory, step_count)
        score = reward.score

        # ✅ FINAL SAFETY
        if score <= 0.0:
            return 0.1
        elif score >= 1.0:
            return 0.9

        return score

    except Exception as e:
        print(f"[ERROR] grade_task failed: {e}")
        return 0.1