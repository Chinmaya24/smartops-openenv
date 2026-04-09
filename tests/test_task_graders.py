import unittest

from tasks.action_recommendation import INPUT_EXAMPLE as ACTION_INPUT, grade as grade_action
from tasks.email_classification import INPUT_EXAMPLE as EMAIL_INPUT, grade as grade_email
from tasks.urgency_detection import INPUT_EXAMPLE as URGENCY_INPUT, grade as grade_urgency


class TestTaskGraders(unittest.TestCase):
    def assert_strict_score(self, value: float) -> None:
        self.assertGreater(value, 0.0)
        self.assertLess(value, 1.0)

    def test_email_classification_correct(self) -> None:
        score = grade_email(EMAIL_INPUT, {"category": "billing"})
        self.assert_strict_score(score)
        self.assertGreater(score, 0.5)

    def test_email_classification_incorrect(self) -> None:
        score = grade_email(EMAIL_INPUT, {"category": "technical"})
        self.assert_strict_score(score)
        self.assertLess(score, 0.5)

    def test_urgency_detection_perfect(self) -> None:
        score = grade_urgency(URGENCY_INPUT, {"priority": 3, "escalated": True})
        self.assert_strict_score(score)
        self.assertGreater(score, 0.5)

    def test_urgency_detection_partial(self) -> None:
        score = grade_urgency(URGENCY_INPUT, {"priority": 3, "escalated": False})
        self.assert_strict_score(score)
        self.assertLess(score, 0.7)

    def test_urgency_detection_wrong(self) -> None:
        score = grade_urgency(URGENCY_INPUT, {"priority": 1, "escalated": False})
        self.assert_strict_score(score)
        self.assertLess(score, 0.3)

    def test_action_recommendation_perfect(self) -> None:
        score = grade_action(
            ACTION_INPUT,
            {
                "escalated": False,
                "priority": 2,
                "response": "I will help resolve your problem and support you.",
            },
        )
        self.assert_strict_score(score)
        self.assertGreater(score, 0.6)

    def test_action_recommendation_partial(self) -> None:
        score = grade_action(
            ACTION_INPUT,
            {
                "escalated": False,
                "priority": 1,
                "response": "I can help with this.",
            },
        )
        self.assert_strict_score(score)
        self.assertLess(score, 0.6)

    def test_action_recommendation_wrong(self) -> None:
        score = grade_action(
            ACTION_INPUT,
            {
                "escalated": True,
                "priority": 3,
                "response": "We will not help you.",
            },
        )
        self.assert_strict_score(score)
        self.assertLess(score, 0.3)


if __name__ == "__main__":
    unittest.main()
