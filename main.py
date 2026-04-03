"""Backward-compatible entrypoint: ``uvicorn main:app`` (OpenEnv canonical: ``server.app:app``)."""

from server.app import app

__all__ = ["app"]
