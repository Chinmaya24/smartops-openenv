def multi_agent_grade(task, memory, step_count):
    expected = task["expected"]

    score = 0.0
    feedback = ""
    done = False

    # 🎯 Category correctness
    if "category" in expected:
        if memory.get("category") == expected["category"]:
            score += 0.4
        else:
            feedback += "Wrong category. "

    # 💬 Response quality
    if "response_contains" in expected:
        if memory.get("response") and expected["response_contains"] in memory["response"].lower():
            score += 0.3
        else:
            feedback += "Poor response. "

    # 🚨 Escalation
    if "escalated" in expected:
        if memory.get("escalated") == expected["escalated"]:
            score += 0.2

    # ⚡ Priority
    if "priority" in expected:
        if memory.get("priority") == expected["priority"]:
            score += 0.1

    # 🔄 Intermediate rewards
    if memory.get("category"):
        score += 0.05

    if memory.get("response"):
        score += 0.05

    if memory.get("escalated"):
        score += 0.05

    # ⏱ Step penalty
    if step_count > 4:
        score -= 0.1

    # Clamp score
    score = max(0.0, min(score, 1.0))

    # ✅ Done condition
    if score >= 0.8:
        done = True
        feedback += "Task success."

    return score, feedback, done