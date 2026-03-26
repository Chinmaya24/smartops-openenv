TASKS = [

    # 🟢 EASY
    {
        "name": "refund_request",
        "initial_state": {
            "subject": "Refund needed",
            "body": "I was charged twice",
            "customer_tier": "user"
        },
        "expected": {
            "category": "billing",
            "response_contains": "refund",
            "escalated": False,
            "priority": 2
        }
    },

    # 🟡 MEDIUM
    {
        "name": "login_issue",
        "initial_state": {
            "subject": "Cannot login",
            "body": "I am unable to access my account",
            "customer_tier": "user"
        },
        "expected": {
            "category": "technical",
            "response_contains": "help",
            "escalated": False,
            "priority": 3
        }
    },

    # 🔴 HARD (YOUR CASE)
    {
        "name": "system_outage",
        "initial_state": {
            "subject": "System down urgently",
            "body": "Our production system is down and we are losing money",
            "customer_tier": "premium"
        },
        "expected": {
            "category": "technical",
            "response_contains": "fix",   # ✅ matches "fixing"
            "escalated": True,
            "priority": 5
        }
    }

]