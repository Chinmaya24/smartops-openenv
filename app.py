import streamlit as st
from env.multi_agent_env import SmartOpsEnv
from env.models import Action

# Page config
st.set_page_config(page_title="SmartOps AI Dashboard", layout="wide")

st.title("🤖 SmartOps AI - Multi-Agent Dashboard")

# =========================
# 📩 Input Section
# =========================
st.header("📩 Enter Customer Email")

subject = st.text_input("Subject", "Refund needed")
body = st.text_area("Body", "I was charged twice")

# =========================
# ▶️ Run Button
# =========================
if st.button("Run Agents"):

    # ✅ Initialize environment properly
    env = SmartOpsEnv()

    obs = env.reset(custom_email={
        "subject": subject,
        "body": body,
        "customer_tier": "user"
    })

    done = False
    step = 0

    st.subheader("🧠 Agent Execution")

    # =========================
    # 🔄 Agent Loop
    # =========================
    while not done and step < 6:
        step += 1

        # ✅ Use Action model (NOT dict)
        if step == 1:
            action = Action(agent="triage", action_type="route")

        elif step == 2:
            action = Action(agent="response", action_type="respond")

        elif step == 3:
            action = Action(agent="escalation", action_type="escalate")

        else:
            action = Action(agent="manager", action_type="finalize")

        # ✅ Step environment
        obs, reward, done, info = env.step(action)

        # =========================
        # 📊 Display Output
        # =========================
        st.markdown(f"### Step {step}: {action.agent.upper()}")

        if "category" in env.shared_memory:
            st.write("📂 Category:", env.shared_memory.get("category"))

        if "urgency" in env.shared_memory:
            st.write("⚡ Urgency:", env.shared_memory.get("urgency"))

        if "response" in env.shared_memory:
            st.write("💬 Response:", env.shared_memory.get("response"))

        if "escalated" in env.shared_memory:
            st.write("🚨 Escalated:", env.shared_memory.get("escalated"))

        if "priority" in env.shared_memory:
            st.write("📊 Priority:", env.shared_memory.get("priority"))

        st.write("🎯 Reward:", reward)
        st.divider()

    # =========================
    # ✅ Done
    # =========================
    st.success("✅ Process Complete")