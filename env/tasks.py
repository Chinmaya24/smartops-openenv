TASKS = [
    # 🟢 EASY TASK
    {
        "id": "easy_spam",
        "initial_state": {
            "subject": "Win FREE iPhone",
            "body": "Click to claim reward",
            "customer_tier": "free"
        },
        "expected": {
            "category": "spam"
        }
    },

    # 🟡 MEDIUM TASK
    {
        "id": "medium_refund",
        "initial_state": {
            "subject": "Refund needed",
            "body": "I was charged twice",
            "customer_tier": "premium"
        },
        "expected": {
            "category": "billing",
            "response_contains": "refund"
        }
    },

    # 🔴 HARD TASK
    {
        "id": "hard_enterprise",
        "initial_state": {
            "subject": "System DOWN",
            "body": "We are losing money",
            "customer_tier": "enterprise"
        },
        "expected": {
            "escalated": True,
            "priority": 5
        }
    }
]