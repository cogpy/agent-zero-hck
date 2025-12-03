"""
daedalOS API Integration Module

Provides HTTP API for Agent Zero within daedalOS environment.
"""

from .server import create_app
from .routes import router

__all__ = [
    'create_app',
    'router',
]
