def multi_agent_grade(task, memory, step_count):
    expected = task["expected"]

    score = 0.0
    feedback = ""
    done = False

    # ✅ SAFE NORMALIZATION
    category = str(memory.get("category", "")).lower()
    expected_category = str(expected.get("category", "")).lower()

    response = str(memory.get("response", "")).lower()

    escalated = bool(memory.get("escalated"))
    expected_escalated = bool(expected.get("escalated"))

    priority = int(memory.get("priority", 0))
    expected_priority = int(expected.get("priority", 0))

    # =========================
    # 🎯 Category
    # =========================
    if category == expected_category:
        score += 0.4
    else:
        score -= 0.05
        feedback += "Wrong category. "

    # =========================
    # 💬 Response
    # =========================
    keywords = ["fix", "fixing", "resolve", "working", "investigating"]

    if response and any(word in response for word in keywords):
        score += 0.3
    else:
        score -= 0.05
        feedback += "Weak response. "

    # =========================
    # 🚨 Escalation
    # =========================
    if escalated == expected_escalated:
        score += 0.2
    else:
        score -= 0.05

    # =========================
    # ⚡ Priority
    # =========================
    if priority == expected_priority:
        score += 0.1

    # =========================
    # ⚠️ Step penalties
    # =========================
    if step_count > 4:
        score -= 0.1
    if step_count > 6:
        score -= 0.2

    # =========================
    # 🏆 BONUS
    # =========================
    if (
        category == expected_category
        and any(word in response for word in keywords)
        and escalated == expected_escalated
        and priority == expected_priority
    ):
        score += 0.2

    # =========================
    # 🔒 Clamp
    # =========================
    score = max(0.0, min(score, 1.0))

    # =========================
    # ✅ Done
    # =========================
    if score >= 0.7:
        done = True
        feedback += "Task success."

    return score, feedback, done