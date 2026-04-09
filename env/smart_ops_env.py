"""OpenEnv-style SmartOpsEnv: reset, step, state with shared_memory and step_count."""

from __future__ import annotations

import random
from typing import Any, Dict, Optional

from agents import escalation_agent, response_agent, triage_agent
from env.graders import grade
from env.models import Action, Observation, Reward
from tasks import TASKS, resolve_task_for_email


class SmartOpsEnv:
    """Multi-agent customer-support environment with deterministic API mode."""

    def __init__(self) -> None:
        self.task: Optional[Dict[str, Any]] = None
        self.email: Optional[Dict[str, Any]] = None
        self.shared_memory: Dict[str, Any] = {}
        self.current_agent: str = "triage"
        self.step_count: int = 0

    def reset(
        self,
        task: Optional[Dict[str, Any]] = None,
        *,
        custom_email: Optional[Dict[str, Any]] = None,
        seed: Optional[int] = None,
    ) -> Observation:
        """
        Initialize episode.
        - If `task` is set, use it; email = custom_email or task's email_input.
        - Elif `custom_email` is set (API / deterministic): resolve task from content.
        - Else: random benchmark task (optional `seed` for reproducibility).
        """
        self.step_count = 0
        self.shared_memory = {}
        self.current_agent = "triage"

        if task is not None:
            self.task = task
            self.email = dict(custom_email) if custom_email is not None else dict(task["email_input"])
        elif custom_email is not None:
            self.task = resolve_task_for_email(custom_email)
            self.email = dict(custom_email)
        else:
            if seed is not None:
                random.seed(seed)
            self.task = random.choice(TASKS)
            self.email = dict(self.task["email_input"])

        return self._obs()

    def step(self, action: Action) -> tuple[Observation, Reward, bool, Dict[str, Any]]:
        self.step_count += 1

        if action.agent != self.current_agent:
            r = Reward(score=0.01, feedback="wrong_agent_turn", breakdown={})
            return self._obs(), r, False, {"error": "wrong_agent_turn"}

        if action.agent == "triage":
            self.shared_memory.update(triage_agent(self.email))
            self.current_agent = "response"
        elif action.agent == "response":
            self.shared_memory["response"] = response_agent(self.shared_memory)
            self.current_agent = "escalation"
        elif action.agent == "escalation":
            self.shared_memory.update(escalation_agent(self.shared_memory))
            self.current_agent = "manager"
        elif action.agent == "manager":
            assert self.task is not None
            final = grade(self.task, self.shared_memory, self.step_count)
            self.shared_memory["score"] = final.score
            return self._obs(), final, True, {"feedback": final.feedback}

        r = Reward(score=0.01, feedback="in_progress", breakdown={})
        return self._obs(), r, False, {}

    def state(self) -> Observation:
        return self._obs()

    def _obs(self) -> Observation:
        task_name = self.task["name"] if self.task else None
        return Observation(
            email=self.email or {},
            current_agent=self.current_agent,
            shared_memory=self.shared_memory,
            step_count=self.step_count,
            task_name=task_name,
        )
