from env.models import Observation, Action
from env.graders import multi_agent_grade
from env.tasks import TASKS
import random


class SmartOpsEnv:

    def __init__(self):
        self.task = None
        self.email = None
        self.shared_memory = None
        self.current_agent = None
        self.step_count = 0

    # =========================
    # 🔄 RESET
    # =========================
    def reset(self, custom_email=None):

        self.task = random.choice(TASKS)

        # ✅ Initialize state properly
        self.step_count = 0
        self.shared_memory = {}
        self.current_agent = "triage"

        # ✅ Use custom input if provided
        if custom_email:
            self.email = custom_email
        else:
            self.email = self.task["initial_state"]

        return self._obs()

    # =========================
    # ▶️ STEP
    # =========================
    def step(self, action: Action):

        self.step_count += 1

        # ❌ Wrong agent turn
        if action.agent != self.current_agent:
            return self._obs(), -0.2, False, {"error": "Wrong agent turn"}

        # =========================
        # 🤖 AGENT LOGIC
        # =========================
        if action.agent == "triage":
            from env.agents import triage_agent
            result = triage_agent(self.email)
            self.shared_memory.update(result)
            self.current_agent = "response"

        elif action.agent == "response":
            from env.agents import response_agent
            result = response_agent(self.shared_memory)
            self.shared_memory["response"] = result
            self.current_agent = "escalation"

        elif action.agent == "escalation":
                from env.agents import escalation_agent
                result = escalation_agent(self.shared_memory)
                self.shared_memory.update(result)   # ✅ VERY IMPORTANT
                self.current_agent = "manager"

        elif action.agent == "manager":
            # Final step
            pass

        # =========================
        # 🎯 GRADING
        # =========================
        score, feedback, done = multi_agent_grade(
            self.task,
            self.shared_memory,
            self.step_count
        )

        return self._obs(), score, done, {"feedback": feedback}

    # =========================
    # 👁 OBSERVATION
    # =========================
    def _obs(self):
        return Observation(
            email=self.email,
            current_agent=self.current_agent,
            shared_memory=self.shared_memory,
            step_count=self.step_count
        )

    # =========================
    # 📦 STATE (Optional)
    # =========================
    def state(self):
        return {
            "email": self.email,
            "memory": self.shared_memory,
            "agent": self.current_agent,
            "step": self.step_count
        }