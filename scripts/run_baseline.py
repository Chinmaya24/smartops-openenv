"""Baseline: fixed policy over all benchmark tasks; prints per-task scores and average."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from env.models import Action
from env.smart_ops_env import SmartOpsEnv
from tasks import TASKS


def run_fixed_policy(env: SmartOpsEnv) -> float:
    done = False
    step = 0
    final = 0.0
    while not done and step < 8:
        step += 1
        if step == 1:
            action = Action(agent="triage", action_type="route")
        elif step == 2:
            action = Action(agent="response", action_type="respond")
        elif step == 3:
            action = Action(agent="escalation", action_type="escalate")
        else:
            action = Action(agent="manager", action_type="finalize")
        _obs, reward, done, _info = env.step(action)
        final = float(reward.score)
    return final


def main() -> None:
    scores: list[float] = []
    for task in TASKS:
        env = SmartOpsEnv()
        env.reset(task=task)
        s = run_fixed_policy(env)
        scores.append(s)
        print(f"task={task['name']:<16} difficulty={task.get('difficulty','?'):<8} score={s:.4f}")

    avg = sum(scores) / len(scores) if scores else 0.0
    print(f"\naverage_score={avg:.4f}")


if __name__ == "__main__":
    main()
