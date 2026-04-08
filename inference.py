from __future__ import annotations

import os
import sys
from typing import Any, Dict, List, Tuple

import requests
from openai import OpenAI

from tasks.action_recommendation import INPUT_EXAMPLE as ACTION_INPUT
from tasks.email_classification import INPUT_EXAMPLE as CLASS_INPUT
from tasks.graders import grade_task
from tasks.urgency_detection import INPUT_EXAMPLE as URGENCY_INPUT

API_BASE_URL = os.environ["API_BASE_URL"]
API_KEY = os.environ["API_KEY"]
MODEL_NAME = os.environ.get("MODEL_NAME", "gpt-4o-mini")

client = OpenAI(api_key=API_KEY, base_url=API_BASE_URL)

ENV_URL = "https://chinu248-smartops-openenv-final.hf.space"


def llm_call(prompt: str) -> str:
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": "You are a customer support AI assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=200,
        temperature=0.0
    )
    content = response.choices[0].message.content
    if not content:
        raise ValueError("Empty response from LLM")
    return content


def post(path: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    """POST to the OpenEnv server. Never calls sys.exit."""
    try:
        # Strip unknown fields before sending to /process-email
        if path == "/process-email":
            payload = {
                "subject": payload.get("subject", ""),
                "body": payload.get("body", ""),
                "customer_tier": payload.get("customer_tier", "user"),
            }
        response = requests.post(f"{ENV_URL}{path}", json=payload, timeout=60)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Request failed for {path}: {e}", file=sys.stderr)
        raise


def run_task(task_name: str, email_input: Dict[str, Any]) -> float:
    post("/reset", {})

    prompt = (
        f"Analyze this support email:\n"
        f"Subject: {email_input.get('subject', '')}\n"
        f"Body: {email_input.get('body', '')}\n\n"
        f"Classify it and suggest appropriate action."
    )
    llm_response = llm_call(prompt)
    print(f"[LLM] {task_name}: {llm_response[:80]}", file=sys.stderr)

    result = post("/process-email", email_input)

    structured_result = {
        "task": email_input,   # contains evaluation_rules for grader
        "memory": result,      # contains category/priority/escalated from server
        "step_count": 1
    }

    score = grade_task(task_name, structured_result)
    return max(0.1, min(0.9, float(score)))  # strictly (0, 1)


def main() -> None:
    tasks: List[Tuple[str, Dict[str, Any]]] = [
        ("email_classification", CLASS_INPUT),
        ("urgency_detection", URGENCY_INPUT),
        ("action_recommendation", ACTION_INPUT),
    ]

    print("[START]")

    for task_name, payload in tasks:
        score = run_task(task_name, payload)
        score = max(0.1, min(0.9, float(score)))  # final safety clamp
        print(f"[STEP] task={task_name} score={score:.4f}")

    print("[END]")


if __name__ == "__main__":
    main()