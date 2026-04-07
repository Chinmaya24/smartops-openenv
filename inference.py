from __future__ import annotations

import os
from typing import Any, Dict, List, Tuple

import requests

from tasks.action_recommendation import INPUT_EXAMPLE as ACTION_INPUT
from tasks.email_classification import INPUT_EXAMPLE as CLASS_INPUT
from tasks.graders import grade_task
from tasks.urgency_detection import INPUT_EXAMPLE as URGENCY_INPUT


API_BASE_URL = os.getenv(
    "API_BASE_URL",
    "https://chinu248-smartops-openenv-final.hf.space"
)


# ---------------- SAFE POST ----------------
def post(path: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    try:
        url = f"{API_BASE_URL}{path}"
        print(f"[DEBUG] POST {url}")

        response = requests.post(url, json=payload, timeout=60)

        print(f"[DEBUG] Status: {response.status_code}")
        print(f"[DEBUG] Body: {response.text}")

        response.raise_for_status()

        return response.json()

    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Request failed for {path}: {e}")
        return {"error": str(e)}

    except ValueError:
        print("[ERROR] Invalid JSON response")
        return {"error": "Invalid JSON"}


# ---------------- RUN TASK ----------------
def run_task(task_name: str, email_input: Dict[str, Any]) -> float:
    try:
        reset_res = post("/reset", {})
        if "error" in reset_res:
            print(f"[WARN] Reset failed")
            return 0.0

        result = post("/process-email", email_input)

        if "error" in result:
            print(f"[WARN] Skipping {task_name}")
            return 0.0

        return grade_task(task_name, result)

    except Exception as e:
        print(f"[ERROR] Task {task_name} crashed: {e}")
        return 0.0


# ---------------- MAIN ----------------
def main() -> None:
    tasks: List[Tuple[str, Dict[str, Any]]] = [
        ("email_classification", CLASS_INPUT),
        ("urgency_detection", URGENCY_INPUT),
        ("action_recommendation", ACTION_INPUT),
    ]

    print("[START]")

    total_score = 0.0

    for task_name, payload in tasks:
        try:
            score = run_task(task_name, payload)
            total_score += score
            print(f"[STEP] task={task_name} score={score:.4f}")
        except Exception as e:
            print(f"[STEP] task={task_name} score=0.0000 error={e}")

    print(f"[TOTAL] {total_score:.4f}")
    print("[END]")


# ---------------- ENTRY ----------------
if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"[FATAL] {e}")