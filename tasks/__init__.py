"""Task registry for SmartOps OpenEnv."""

from .definitions import TASKS, get_task_by_name, resolve_task_for_email

__all__ = ["TASKS", "get_task_by_name", "resolve_task_for_email"]
