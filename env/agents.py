# =========================
# 📦 IMPORTS
# =========================
from transformers import pipeline
import json
import re

# =========================
# 🤖 LOAD LLM (ONCE)
# =========================
llm = pipeline("text-generation", model="google/flan-t5-small")


# =========================
# 🧠 HELPER: EXTRACT JSON
# =========================
def extract_json(text):
    try:
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if match:
            return json.loads(match.group())
    except:
        pass
    return None


# =========================
# 🧠 TRIAGE AGENT (LLM + FALLBACK)
# =========================
def triage_agent(email):

    subject = email.get("subject", "")
    body = email.get("body", "")

    prompt = f"""
    Classify this customer support email.

    Email: {subject} {body}

    Return ONLY JSON:
    {{
        "category": "billing | technical | general",
        "urgency": 1-5
    }}
    """

    try:
        output = llm(prompt, max_new_tokens=50)[0]["generated_text"]
        result = extract_json(output)

        if result:
            return result

    except:
        pass

    # 🔁 FALLBACK (RULE-BASED)
    text = (subject + " " + body).lower()

    if "refund" in text or "charged" in text:
        return {"category": "billing", "urgency": 2}

    elif "login" in text or "password" in text:
        return {"category": "technical", "urgency": 3}

    elif "down" in text or "urgent" in text or "losing money" in text:
        return {"category": "technical", "urgency": 5}

    else:
        return {"category": "general", "urgency": 1}


# =========================
# 💬 RESPONSE AGENT (LLM + FALLBACK)
# =========================
def response_agent(memory):

    prompt = f"""
    Customer support reply for a {memory.get("category")} issue with urgency {memory.get("urgency")}.
    Keep it short and professional.
    """

    try:
        output = llm(prompt, max_new_tokens=100)[0]["generated_text"]

        # Remove prompt echo
        response = output.replace(prompt, "").strip()

        # ✅ HANDLE BAD OUTPUTS
        if not response or len(response) < 10:
            raise ValueError("Bad LLM output")

        return response

    except:
        # 🔁 fallback (VERY IMPORTANT)
        category = memory.get("category", "")
        urgency = memory.get("urgency", 1)

        if category == "billing":
            return "We are processing your refund."

        elif category == "technical" and urgency >= 4:
            return "We are aware of the issue and fixing it urgently."

        elif category == "technical":
            return "We will help you resolve this issue."

        else:
            return "Thank you for contacting support."


# =========================
# 🚨 ESCALATION AGENT
# =========================
def escalation_agent(memory):

    urgency = memory.get("urgency", 1)

    if urgency >= 4:
        return {
            "escalated": True,
            "priority": 5
        }
    else:
        return {
            "escalated": False,
            "priority": 2
        }


# =========================
# 🔄 MAIN PIPELINE FUNCTION
# =========================
def process_email(email):

    memory = {}

    # Step 1: Triage
    triage_result = triage_agent(email)
    memory.update(triage_result)

    # Step 2: Response
    response = response_agent(memory)
    memory["response"] = response

    # Step 3: Escalation
    escalation_result = escalation_agent(memory)
    memory.update(escalation_result)

    return memory


# =========================
# 🧪 TEST RUN
# =========================
if __name__ == "__main__":

    test_email = {
        "subject": "URGENT: Website is down",
        "body": "We are losing money, fix this immediately!"
    }

    result = process_email(test_email)

    print("\n✅ FINAL OUTPUT:\n")
    print(json.dumps(result, indent=2))