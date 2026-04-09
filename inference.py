from __future__ import annotations

import os
from typing import List, Optional

from openai import OpenAI

from env.models import Action
from env.smart_ops_env import SmartOpsEnv
from tasks import TASKS

# Required env vars (with safe defaults for local execution)
API_BASE_URL = os.getenv("API_BASE_URL", "https://router.huggingface.co/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "meta-llama/Llama-3.3-70B-Instruct")
HF_TOKEN = os.getenv("HF_TOKEN", "")
LOCAL_IMAGE_NAME = os.getenv("LOCAL_IMAGE_NAME", "")
BENCHMARK = os.getenv("MY_ENV_V4_BENCHMARK", "smartops-openenv")

_EPS = 1e-3
_ACTION_ORDER = ["triage", "response", "escalation", "manager"]


def _strict_score(value: float) -> float:
    return max(_EPS, min(1.0 - _EPS, float(value)))


def _done_bool(value: bool) -> str:
    return "true" if bool(value) else "false"


def log_start(task: str, env: str, model: str) -> None:
    print(f"[START] task={task} env={env} model={model}", flush=True)


def log_step(step: int, action: str, reward: float, done: bool, error: Optional[str]) -> None:
    err = error if error else "null"
    print(
        f"[STEP] step={step} action={action} reward={reward:.2f} done={_done_bool(done)} error={err}",
        flush=True,
    )


def log_end(success: bool, steps: int, score: float, rewards: List[float]) -> None:
    rewards_text = ",".join(f"{r:.2f}" for r in rewards)
    print(
        f"[END] success={_done_bool(success)} steps={steps} score={score:.2f} rewards={rewards_text}",
        flush=True,
    )


def choose_action_with_llm(
    client: OpenAI,
    task_name: str,
    step: int,
    memory: dict,
) -> str:
    """
    Select the next agent name. Uses OpenAI client when available,
    then falls back to deterministic action order for robustness.
    """
    fallback = _ACTION_ORDER[min(step - 1, len(_ACTION_ORDER) - 1)]
    if not HF_TOKEN:
        return fallback

    prompt = (
        "Choose one action from: triage, response, escalation, manager. "
        f"Task={task_name}. Step={step}. "
        f"SharedMemoryKeys={list(memory.keys())}. "
        "Return only the action string."
    )
    try:
        completion = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "You select the next control action."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=8,
            temperature=0.0,
        )
        text = (completion.choices[0].message.content or "").strip().lower()
        if text in _ACTION_ORDER:
            return text
    except Exception:
        pass
    return fallback


def run_one_task(client: OpenAI, task: dict) -> None:
    env = SmartOpsEnv()
    rewards: List[float] = []
    steps_taken = 0
    success = False
    score = _strict_score(0.5)

    task_name = str(task.get("name", "unknown"))
    log_start(task=task_name, env=BENCHMARK, model=MODEL_NAME)

    try:
        _ = env.reset(task=task)
        done = False
        last_error: Optional[str] = None

        for step in range(1, 9):
            action_name = choose_action_with_llm(client, task_name, step, env.shared_memory)
            action = Action(agent=action_name, action_type="auto")
            _, reward_obj, done, info = env.step(action)

            reward = float(reward_obj.score)
            rewards.append(reward)
            steps_taken = step
            last_error = info.get("error") if isinstance(info, dict) else None
            log_step(step=step, action=action_name, reward=reward, done=done, error=last_error)

            if done:
                break

        raw_score = float(env.shared_memory.get("score", rewards[-1] if rewards else 0.5))
        score = _strict_score(raw_score)
        success = bool(done) and score > 0.0 and score < 1.0
    except Exception as exc:
        log_step(step=steps_taken + 1, action="manager", reward=0.00, done=False, error=str(exc))
        success = False
        score = _strict_score(0.5)
    finally:
        log_end(success=success, steps=steps_taken, score=score, rewards=rewards)


def main() -> None:
    client = OpenAI(base_url=API_BASE_URL, api_key=HF_TOKEN)
    for task in TASKS:
        run_one_task(client, task)


if __name__ == "__main__":
    main()