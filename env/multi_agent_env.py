import random
from env.models import Observation, Action, Reward
from env.tasks import TASKS
from env.graders import multi_agent_grade
from env.agents import triage_agent, response_agent, escalation_agent


class SmartOpsEnv:

    def __init__(self):
        self.task = None
        self.email = None
        self.memory = None
        self.current_agent = None
        self.step_count = 0

    def reset(self, task_id=None):
        self.task = random.choice(TASKS) if task_id is None else TASKS[task_id]
        self.email = self.task["initial_state"]

        self.memory = {
            "category": None,
            "urgency": None,
            "response": None,
            "escalated": False,
            "priority": None
        }

        self.current_agent = "triage"
        self.step_count = 0

        return self._obs()

    def state(self):
        return {
            "email": self.email,
            "memory": self.memory
        }

    def step(self, action: Action):
        self.step_count += 1

        # ❌ Wrong agent turn
        if action.agent != self.current_agent:
            return self._obs(), Reward(score=-0.2, feedback="Wrong agent turn"), False, {}

        # 🤖 Agent logic
        if action.agent == "triage":
            result = triage_agent(self.email)
            self.memory.update(result)
            self.current_agent = "manager"

        elif action.agent == "response":
            self.memory["response"] = response_agent(self.memory)
            self.current_agent = "manager"

        elif action.agent == "escalation":
            result = escalation_agent(self.memory)
            self.memory.update(result)
            self.current_agent = "manager"

        elif action.agent == "manager":
            if self.memory["category"] is None:
                self.current_agent = "triage"
            elif self.memory["urgency"] >= 5:
                self.current_agent = "escalation"
            elif self.memory["response"] is None:
                self.current_agent = "response"
            else:
                self.current_agent = "done"

        # 🏆 Reward
        score, feedback, done = multi_agent_grade(
            self.task, self.memory, self.step_count
        )

        return self._obs(), Reward(score=score, feedback=feedback), done, {}

    def _obs(self):
        return Observation(
            email=self.email,
            current_agent=self.current_agent,
            shared_memory=self.memory,
            step_count=self.step_count
        )