"""
Avatar API Package

FastAPI-based API for Live2D avatar communication with Agent-Zero.
"""

from .main import app, create_app

__all__ = ["app", "create_app"]
