"""FastAPI app for n8n (Gmail → HTTP → response). API contract is stable."""

from __future__ import annotations

from typing import Dict, Union

from fastapi import FastAPI
from pydantic import BaseModel

from env.models import Action
from env.smart_ops_env import SmartOpsEnv

app = FastAPI(title="SmartOps AI API")


class EmailRequest(BaseModel):
    subject: str
    body: str
    customer_tier: str = "user"


@app.get("/")
def root() -> Dict[str, str]:
    return {"message": "SmartOps API is running 🚀"}


@app.post("/process-email")
def process_email(data: EmailRequest) -> Dict[str, Union[str, int, float, bool]]:
    """
    Process one email through triage → response → escalation → manager.
    Response shape is fixed for n8n automation.
    """
    env = SmartOpsEnv()
    env.reset(custom_email={
        "subject": data.subject,
        "body": data.body,
        "customer_tier": data.customer_tier,
    })

    done = False
    step = 0
    final_reward: float = 0.0

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
        final_reward = float(reward.score)

    sm = env.shared_memory
    return {
        "category": sm.get("category"),
        "urgency": sm.get("urgency"),
        "response": sm.get("response"),
        "escalated": bool(sm.get("escalated", False)),
        "priority": sm.get("priority"),
        "score": final_reward,
    }
