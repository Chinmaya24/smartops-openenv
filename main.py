"""Application entrypoint for Docker and Hugging Face Spaces (python -m uvicorn main:app)."""

from api.main import app

__all__ = ["app"]
