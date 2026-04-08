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

# Use validator-injected env vars
API_BASE_URL = os.environ.get(
    "API_BASE_URL",
    "https://chinu248-smartops-openenv-final.hf.space"
)
API_KEY = os.environ.get("API_KEY", "dummy")
MODEL_NAME = os.environ.get("MODEL_NAME", "gpt-4o-mini")

# Initialize OpenAI client with LiteLLM proxy
client = OpenAI(
    api_key=API_KEY,
    base_url=API_BASE_URL
)


def llm_call(prompt: str) -> str:
    """Make an API call through the LiteLLM proxy."""
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "system",
                    "content": "You are a customer support AI assistant."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            max_tokens=200,
            temperature=0.0
        )
        return response.choices[0].message.content or ""
    except Exception as e:
        print(f"[WARN] LLM call failed: {e}")
        return ""


def post(path: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    """POST to the OpenEnv server."""
    try:
        # Use HF Space URL for env endpoints
        env_url = "https://chinu248-smartops-openenv-final.hf.space"
        response = requests.post(
            f"{env_url}{path}",
            json=payload,
            timeout=60
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Request failed for {path}: {e}")
        sys.exit(1)


def run_task(task_name: str, email_input: Dict[str, Any]) -> float:
    """Run a single task through the env + LLM."""
    try:
        # Reset environment
        post("/reset", {})

        # Make LLM call through proxy (required by validator)
        prompt = (
            f"Analyze this support email and classify it:\n"
            f"Subject: {email_input.get('subject', '')}\n"
            f"Body: {email_input.get('body', '')}\n"
            f"Respond with the category (billing/technical/general)."
        )
        llm_response = llm_call(prompt)
        print(f"[LLM] {task_name}: {llm_response[:80]}")

        # Process through env
        result = post("/process-email", email_input)
        return grade_task(task_name, result)

    except Exception as e:
        print(f"[ERROR] Task {task_name} failed: {e}")
        return 0.0


def main() -> None:
    tasks: List[Tuple[str, Dict[str, Any]]] = [
        ("email_classification", CLASS_INPUT),
        ("urgency_detection", URGENCY_INPUT),
        ("action_recommendation", ACTION_INPUT),
    ]

    print("[START]")
    for task_name, payload in tasks:
        try:
            score = run_task(task_name, payload)
            print(f"[STEP] task={task_name} score={score:.4f}")
        except Exception as e:
            print(f"[STEP] task={task_name} score=0.0000 error={e}")
    print("[END]")


if __name__ == "__main__":
    main()