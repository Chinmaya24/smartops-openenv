import streamlit as st
import time
from env.smart_ops_env import SmartOpsEnv
from env.models import Action

st.set_page_config(page_title="SmartOps AI Dashboard", layout="wide")

st.title("🤖 SmartOps AI - Multi-Agent Dashboard")
st.caption("🧠 AI Multi-Agent System with Reinforcement Learning")

st.markdown("### ⚡ Quick Test Scenarios")

colA, colB = st.columns(2)

with colA:
    if st.button("🚨 System Outage"):
        st.session_state.subject = "URGENT: System down"
        st.session_state.body = "Our platform is completely down. Fix ASAP!"

with colB:
    if st.button("💳 Refund Issue"):
        st.session_state.subject = "Refund needed"
        st.session_state.body = "I was charged twice for my order."

st.header("📩 Enter Customer Email")

subject = st.text_input(
    "Subject",
    value=st.session_state.get("subject", "Refund needed")
)

body = st.text_area(
    "Body",
    value=st.session_state.get("body", "I was charged twice")
)

if st.button("Run Agents"):

    env = SmartOpsEnv()

    obs = env.reset(custom_email={
        "subject": subject,
        "body": body,
        "customer_tier": "user"
    })

    done = False
    step = 0

    st.markdown("### 🔄 Agent Flow")
    st.write("📩 Email → 🧠 Triage → 💬 Response → 🚨 Escalation → 📊 Manager")

    st.subheader("🧠 Agent Execution")

    progress_bar = st.progress(0)

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

        with st.spinner(f"Running {action.agent} agent..."):
            time.sleep(0.6)

        obs, reward, done, _ = env.step(action)

        with st.expander(f"Step {step}: {action.agent.upper()}"):
            st.json(env.shared_memory)

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("📂 Category", env.shared_memory.get("category", "-"))
            st.metric("⚡ Urgency", env.shared_memory.get("urgency", "-"))

        with col2:
            st.metric("🚨 Escalated", env.shared_memory.get("escalated", "-"))
            st.metric("📊 Priority", env.shared_memory.get("priority", "-"))

        with col3:
            st.metric("🎯 Reward", round(float(reward.score), 4))

        progress_bar.progress(min(step / 6, 1.0))
        st.divider()

    st.subheader("📊 Final Decision")

    st.success(f"""
    **Category:** {env.shared_memory.get("category")}  
    **Urgency:** {env.shared_memory.get("urgency")}  
    **Escalated:** {env.shared_memory.get("escalated")}  
    **Priority:** {env.shared_memory.get("priority")}
    """)

    st.progress(float(env.shared_memory.get("score", 0.0)))

    with st.expander("🔍 Debug / Full Memory"):
        st.json(env.shared_memory)

    st.success("✅ Process Complete")
