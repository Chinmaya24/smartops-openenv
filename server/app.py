"""FastAPI application for OpenEnv / Hugging Face Spaces (spec: server/app.py)."""

from __future__ import annotations

from typing import Any, Dict

from fastapi import FastAPI
from pydantic import BaseModel

from agents import escalation_agent, response_agent, triage_agent


class StepAction(BaseModel):
    action: str


class EmailRequest(BaseModel):
    subject: str
    body: str
    customer_tier: str = "user"


class RuntimeEnv:
    def __init__(self) -> None:
        self.observation = ""
        self.reward = 0.0
        self.done = False
        self.step_count = 0
        self.shared_memory: Dict[str, Any] = {}
        self.email: Dict[str, Any] = {}
        self.reset()

    def reset(self) -> Dict[str, Any]:
        self.observation = "ready"
        self.reward = 0.0
        self.done = False
        self.step_count = 0
        self.shared_memory = {}
        self.email = {}
        return {
            "observation": self.observation,
            "reward": float(self.reward),
            "done": bool(self.done),
        }

    def step(self, action: str) -> Dict[str, Any]:
        self.step_count += 1
        act = action.lower().strip()

        if act == "triage":
            result = triage_agent(self.email)
            self.shared_memory.update(result)
            self.observation = f"triage:{result.get('category', 'general')}"
            self.reward = 0.3
            self.done = False
        elif act == "respond":
            text = response_agent(self.shared_memory)
            self.shared_memory["response"] = text
            self.observation = "response_generated"
            self.reward = 0.3
            self.done = False
        elif act == "escalate":
            result = escalation_agent(self.shared_memory)
            self.shared_memory.update(result)
            self.observation = f"escalated:{self.shared_memory.get('escalated', False)}"
            self.reward = 0.2
            self.done = False
        elif act in {"finalize", "manager"}:
            self.reward = max(0.0, min(1.0, 1.0 - max(0, self.step_count - 4) * 0.05))
            self.shared_memory["score"] = self.reward
            self.observation = "complete"
            self.done = True
        else:
            self.reward = 0.0
            self.observation = "invalid_action"
            self.done = False

        return {
            "observation": self.observation,
            "reward": float(max(0.0, min(1.0, self.reward))),
            "done": bool(self.done),
        }

    def process_email(self, payload: EmailRequest) -> Dict[str, Any]:
        self.email = {
            "subject": payload.subject,
            "body": payload.body,
            "customer_tier": payload.customer_tier,
        }
        self.shared_memory = {}
        self.step_count = 0
        self.done = False

        self.step("triage")
        self.step("respond")
        self.step("escalate")
        final = self.step("finalize")

        return {
            "category": self.shared_memory.get("category", "general"),
            "urgency": int(self.shared_memory.get("urgency", 1)),
            "response": self.shared_memory.get("response", ""),
            "escalated": bool(self.shared_memory.get("escalated", False)),
            "priority": int(self.shared_memory.get("priority", 1)),
            "score": float(final["reward"]),
        }

    def state(self) -> Dict[str, Any]:
        return {
            "observation": self.observation,
            "reward": float(self.reward),
            "done": bool(self.done),
            "step_count": int(self.step_count),
            "shared_memory": self.shared_memory,
            "email": self.email,
        }


runtime = RuntimeEnv()
app = FastAPI(title="SmartOps OpenEnv")


@app.get("/")
def root() -> Dict[str, Any]:
    return {
        "status": "ok",
        "endpoints": ["/", "/reset", "/step", "/state", "/process-email"],
    }


@app.post("/reset")
def reset() -> Dict[str, Any]:
    return runtime.reset()


@app.post("/step")
def step(action: StepAction) -> Dict[str, Any]:
    return runtime.step(action.action)


@app.get("/state")
def state() -> Dict[str, Any]:
    return runtime.state()


@app.post("/process-email")
def process_email(payload: EmailRequest) -> Dict[str, Any]:
    return runtime.process_email(payload)
