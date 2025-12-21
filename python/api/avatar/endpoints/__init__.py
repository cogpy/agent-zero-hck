"""
Avatar API Endpoints

All endpoint routers for the Avatar API.
"""

from .session import router as session_router
from .chat import router as chat_router
from .emotion import router as emotion_router
from .animation import router as animation_router
from .voice import router as voice_router
from .health import router as health_router
from .transform import router as transform_router

__all__ = [
    "session_router",
    "chat_router",
    "emotion_router",
    "animation_router",
    "voice_router",
    "health_router",
    "transform_router",
]
