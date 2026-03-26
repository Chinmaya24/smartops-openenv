from fastapi import FastAPI
from pydantic import BaseModel
from env.multi_agent_env import SmartOpsEnv
from env.models import Action

app = FastAPI(title="SmartOps AI API")


# =========================
# 📩 Request Model
# =========================
class EmailRequest(BaseModel):
    subject: str
    body: str
    customer_tier: str = "user"


# =========================
# ❤️ Health Check
# =========================
@app.get("/")
def root():
    return {"message": "SmartOps API is running 🚀"}


# =========================
# 🤖 Process Email Endpoint
# =========================
@app.post("/process-email")
def process_email(data: EmailRequest):

    env = SmartOpsEnv()

# 🔥 FORCE correct task (no randomness)
    env.task = {
        "name": "system_outage",
        "expected": {
            "category": "technical",
            "response_contains": "fix",
            "escalated": True,
            "priority": 5
        }
    }

    obs = env.reset(custom_email={
        "subject": data.subject,
        "body": data.body,
        "customer_tier": data.customer_tier
    })

    done = False
    step = 0

    # 🔄 Run agent pipeline
    while not done and step < 6:
        step += 1

        if step == 1:
            action = Action(agent="triage", action_type="route")

        elif step == 2:
            action = Action(agent="response", action_type="respond")

        elif step == 3:
            action = Action(agent="escalation", action_type="escalate")

        else:
            action = Action(agent="manager", action_type="finalize")

        obs, reward, done, info = env.step(action)

    # =========================
    # 📤 Response
    # =========================
    return {
        "category": env.shared_memory.get("category"),
        "urgency": env.shared_memory.get("urgency"),
        "response": env.shared_memory.get("response"),
        "escalated": env.shared_memory.get("escalated"),
        "priority": env.shared_memory.get("priority"),
        "score": reward
    }