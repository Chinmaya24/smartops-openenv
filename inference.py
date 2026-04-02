from __future__ import annotations

import os
from typing import Any, Dict, List, Tuple

import requests
from openai import OpenAI

from tasks.action_recommendation import INPUT_EXAMPLE as ACTION_INPUT
from tasks.email_classification import INPUT_EXAMPLE as CLASS_INPUT
from tasks.graders import grade_task
from tasks.urgency_detection import INPUT_EXAMPLE as URGENCY_INPUT


API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:7860")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini")
HF_TOKEN = os.getenv("HF_TOKEN", "")


def post(path: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    response = requests.post(f"{API_BASE_URL}{path}", json=payload, timeout=30)
    response.raise_for_status()
    return response.json()


def run_task(task_name: str, email_input: Dict[str, Any]) -> float:
    post("/reset", {})
    result = post("/process-email", email_input)
    return grade_task(task_name, result)


def main() -> None:
    _client = OpenAI(api_key=HF_TOKEN or "dummy", base_url=os.getenv("OPENAI_BASE_URL"))
    _ = MODEL_NAME

    tasks: List[Tuple[str, Dict[str, Any]]] = [
        ("email_classification", CLASS_INPUT),
        ("urgency_detection", URGENCY_INPUT),
        ("action_recommendation", ACTION_INPUT),
    ]

    print("[START]")
    for task_name, payload in tasks:
        score = run_task(task_name, payload)
        print(f"[STEP] task={task_name} score={score:.1f}")
    print("[END]")


if __name__ == "__main__":
    main()
