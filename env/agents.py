def triage_agent(email):
    text = (email["subject"] + " " + email["body"]).lower()

    if "free" in text or "win" in text:
        return {"category": "spam", "urgency": 1}

    if "refund" in text or "charged" in text:
        return {"category": "billing", "urgency": 4}

    if "down" in text or "error" in text:
        return {"category": "technical", "urgency": 5}

    return {"category": "general", "urgency": 2}


def response_agent(memory):
    if memory.get("category") == "billing":
        return "We apologize. Your refund is being processed."

    if memory.get("category") == "technical":
        return "We are fixing the issue urgently."

    return "Thank you for contacting support."


def escalation_agent(memory):
    if memory.get("urgency", 1) >= 5:
        return {"escalated": True, "priority": 5}
    return {"escalated": False, "priority": 2}