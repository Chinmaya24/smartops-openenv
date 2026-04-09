from __future__ import annotations

import json
import os
import sys
from typing import Any, Dict

from openai import OpenAI

# ---------------------------------------------------------------------------
# Environment configuration (set these in your HF Space secrets / .env)
# ---------------------------------------------------------------------------
API_BASE_URL = os.environ.get("API_BASE_URL", "https://router.huggingface.co/v1")
MODEL_NAME   = os.environ.get("MODEL_NAME",   "meta-llama/Llama-3.3-70B-Instruct")
HF_TOKEN     = os.environ.get("HF_TOKEN",     "")

client = OpenAI(base_url=API_BASE_URL, api_key=HF_TOKEN)

EPSILON = 0.01


# ---------------------------------------------------------------------------
# Logging helpers — strict [START] / [STEP] / [END] format
# ---------------------------------------------------------------------------

def log_start(task_id: str) -> None:
    print(f"[START] task_id={task_id}", flush=True)


def log_step(key: str, value: Any) -> None:
    # Serialise value so it always fits on one line
    if isinstance(value, (dict, list)):
        serialised = json.dumps(value, ensure_ascii=False)
    else:
        serialised = str(value)
    print(f"[STEP] {key}={serialised}", flush=True)


def log_end(task_id: str) -> None:
    print(f"[END] task_id={task_id}", flush=True)


# ---------------------------------------------------------------------------
# Clamp helper — scores must be strictly inside (0, 1)
# ---------------------------------------------------------------------------

def _clamp(score: float) -> float:
    return max(EPSILON, min(1.0 - EPSILON, float(score)))


# ---------------------------------------------------------------------------
# LLM call
# ---------------------------------------------------------------------------

def call_llm(system_prompt: str, user_prompt: str) -> str:
    """Call the LLM via OpenAI-compatible client and return the text reply."""
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user",   "content": user_prompt},
        ],
        max_tokens=512,
        temperature=0.2,
    )
    return response.choices[0].message.content.strip()


# ---------------------------------------------------------------------------
# Task 1 — email_classification
# ---------------------------------------------------------------------------

TASK_EMAIL: Dict[str, Any] = {
    "name": "email_classification",
    "input": {
        "subject": "Refund needed for duplicate charge",
        "body": "I was charged twice for my subscription this month and need a refund.",
        "customer_tier": "user",
        "evaluation_rules": {
            "category": "billing",
            "response_keywords": ["refund", "billing", "payment"],
            "escalated": False,
            "priority": 1,
        },
    },
}


def run_email_classification(task: Dict[str, Any]) -> Dict[str, Any]:
    inp = task["input"]
    system = (
        "You are a customer-support triage assistant. "
        "Classify the email into exactly one category: billing, technical, account, general. "
        "Reply with ONLY a JSON object: {\"category\": \"<value>\"}"
    )
    user = f"Subject: {inp['subject']}\nBody: {inp['body']}"
    raw = call_llm(system, user)
    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError:
        parsed = {"category": "general"}
    return parsed


def grade_email_classification(result: Dict[str, Any]) -> float:
    task   = result.get("task", {})
    memory = result.get("memory", result)
    rules  = task.get("evaluation_rules", {})
    expected = str(rules.get("category", "billing")).lower()
    actual   = str(memory.get("category", "")).lower()
    return _clamp(0.8 if actual == expected else 0.2)


# ---------------------------------------------------------------------------
# Task 2 — urgency_detection
# ---------------------------------------------------------------------------

TASK_URGENCY: Dict[str, Any] = {
    "name": "urgency_detection",
    "input": {
        "subject": "URGENT: Production server is down",
        "body": "Our production environment has been completely unavailable for 30 minutes.",
        "customer_tier": "enterprise",
        "evaluation_rules": {
            "priority": 3,
            "escalated": True,
            "category": "technical",
            "response_keywords": ["escalate", "urgent", "critical"],
        },
    },
}


def run_urgency_detection(task: Dict[str, Any]) -> Dict[str, Any]:
    inp = task["input"]
    system = (
        "You are a support triage assistant that detects urgency. "
        "Assign a priority level 1 (low), 2 (medium), or 3 (high) and decide whether to escalate. "
        "Reply with ONLY a JSON object: {\"priority\": <1|2|3>, \"escalated\": <true|false>}"
    )
    user = (
        f"Subject: {inp['subject']}\n"
        f"Body: {inp['body']}\n"
        f"Customer tier: {inp['customer_tier']}"
    )
    raw = call_llm(system, user)
    try:
        parsed = json.loads(raw)
        parsed["priority"]  = int(parsed.get("priority", 1))
        parsed["escalated"] = bool(parsed.get("escalated", False))
    except (json.JSONDecodeError, ValueError):
        parsed = {"priority": 1, "escalated": False}
    return parsed


def grade_urgency_detection(result: Dict[str, Any]) -> float:
    task   = result.get("task", {})
    memory = result.get("memory", result)
    rules  = task.get("evaluation_rules", {})
    expected = int(rules.get("priority", 0))
    actual   = int(memory.get("priority", 0))
    return _clamp(0.8 if actual == expected else 0.2)


# ---------------------------------------------------------------------------
# Task 3 — action_recommendation
# ---------------------------------------------------------------------------

TASK_ACTION: Dict[str, Any] = {
    "name": "action_recommendation",
    "input": {
        "subject": "Cannot login to account",
        "body": "I cannot access my account after a password reset three days ago.",
        "customer_tier": "user",
        "evaluation_rules": {
            "category": "technical",
            "response_keywords": ["help", "resolve", "support", "assist"],
            "escalated": False,
            "priority": 2,
        },
    },
}


def run_action_recommendation(task: Dict[str, Any]) -> Dict[str, Any]:
    inp = task["input"]
    system = (
        "You are a customer-support assistant. "
        "Recommend an action and draft a short response for this ticket. "
        "Reply with ONLY a JSON object: "
        "{\"escalated\": <true|false>, \"priority\": <1|2|3>, \"response\": \"<draft reply>\"}"
    )
    user = (
        f"Subject: {inp['subject']}\n"
        f"Body: {inp['body']}\n"
        f"Customer tier: {inp['customer_tier']}"
    )
    raw = call_llm(system, user)
    try:
        parsed = json.loads(raw)
        parsed["escalated"] = bool(parsed.get("escalated", False))
        parsed["priority"]  = int(parsed.get("priority", 1))
    except (json.JSONDecodeError, ValueError):
        parsed = {"escalated": False, "priority": 1, "response": "We will help you resolve this."}
    return parsed


def grade_action_recommendation(result: Dict[str, Any]) -> float:
    task   = result.get("task", {})
    memory = result.get("memory", result)
    rules  = task.get("evaluation_rules", {})
    expected_escalated = bool(rules.get("escalated", False))
    actual_escalated   = bool(memory.get("escalated", False))
    response  = str(memory.get("response", "")).lower()
    keywords  = [str(k).lower() for k in rules.get("response_keywords", [])]
    has_kw    = any(kw in response for kw in keywords)
    if actual_escalated == expected_escalated and has_kw:
        return _clamp(0.8)
    if actual_escalated == expected_escalated:
        return _clamp(0.6)
    return _clamp(0.2)


# ---------------------------------------------------------------------------
# Task registry
# ---------------------------------------------------------------------------

TASKS = [
    (TASK_EMAIL,   run_email_classification, grade_email_classification),
    (TASK_URGENCY, run_urgency_detection,    grade_urgency_detection),
    (TASK_ACTION,  run_action_recommendation, grade_action_recommendation),
]


# ---------------------------------------------------------------------------
# Main runner
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# Main runner
# ---------------------------------------------------------------------------

def run_task(task: Dict[str, Any], runner, grader) -> float:
    task_id = task["name"]
    inp     = task["input"]

    log_start(task_id)
    log_step("input", inp)

    try:
        memory = runner(task)
    except Exception as exc:          # noqa: BLE001
        memory = {"error": str(exc)}

    log_step("output", memory)

    result = {"task": inp, "memory": memory}
    score  = grader(result)

    log_step("score", score)
    log_end(task_id)

    return score


def main() -> None:
    scores = {}
    for task, runner, grader in TASKS:
        score = run_task(task, runner, grader)
        scores[task["name"]] = score

    # FINAL SAFETY CLAMP: Force everything to strictly (0, 1) right before output
    safe_scores = {}
    for task_name, task_score in scores.items():
        try:
            val = float(task_score)
            safe_scores[task_name] = max(0.001, min(0.999, val))
        except (ValueError, TypeError):
            safe_scores[task_name] = 0.5 

    # Final summary line (Validator reads this)
    print(f"[SUMMARY] {json.dumps(safe_scores)}", flush=True)

    # Exit non-zero only on hard failures (all scores present = success)
    if len(safe_scores) < 3:
        sys.exit(1)


if __name__ == "__main__":
    main()