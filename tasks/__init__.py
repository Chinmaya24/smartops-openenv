from tasks.action_recommendation import (
    EXPECTED_OUTPUT as ACTION_RECOMMENDATION_EXPECTED_OUTPUT,
)
from tasks.action_recommendation import INPUT_EXAMPLE as ACTION_RECOMMENDATION_INPUT
from tasks.action_recommendation import TASK_NAME as ACTION_RECOMMENDATION_TASK
from tasks.email_classification import EXPECTED_OUTPUT as EMAIL_CLASSIFICATION_EXPECTED_OUTPUT
from tasks.email_classification import INPUT_EXAMPLE as EMAIL_CLASSIFICATION_INPUT
from tasks.email_classification import TASK_NAME as EMAIL_CLASSIFICATION_TASK
from tasks.urgency_detection import EXPECTED_OUTPUT as URGENCY_DETECTION_EXPECTED_OUTPUT
from tasks.urgency_detection import INPUT_EXAMPLE as URGENCY_DETECTION_INPUT
from tasks.urgency_detection import TASK_NAME as URGENCY_DETECTION_TASK

TASKS = [
    {
        "name": EMAIL_CLASSIFICATION_TASK,
        "email_input": EMAIL_CLASSIFICATION_INPUT,
        "expected_output": EMAIL_CLASSIFICATION_EXPECTED_OUTPUT,
    },
    {
        "name": URGENCY_DETECTION_TASK,
        "email_input": URGENCY_DETECTION_INPUT,
        "expected_output": URGENCY_DETECTION_EXPECTED_OUTPUT,
    },
    {
        "name": ACTION_RECOMMENDATION_TASK,
        "email_input": ACTION_RECOMMENDATION_INPUT,
        "expected_output": ACTION_RECOMMENDATION_EXPECTED_OUTPUT,
    },
]


def resolve_task_for_email(email: dict) -> dict:
    text = f"{email.get('subject', '')} {email.get('body', '')}".lower()
    if any(k in text for k in ("urgent", "outage", "down", "production")):
        return TASKS[1]
    if any(k in text for k in ("login", "password", "access", "account")):
        return TASKS[2]
    return TASKS[0]
