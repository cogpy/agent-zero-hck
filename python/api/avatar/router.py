"""
Avatar API Router

Combines all endpoint routers into a single router.
"""

from fastapi import APIRouter

from .endpoints.session import router as session_router
from .endpoints.chat import router as chat_router
from .endpoints.emotion import router as emotion_router
from .endpoints.animation import router as animation_router
from .endpoints.voice import router as voice_router
from .endpoints.health import router as health_router
from .endpoints.transform import router as transform_router

# Main router
router = APIRouter()

# Include all sub-routers
router.include_router(health_router, tags=["Health"])
router.include_router(session_router, prefix="/session", tags=["Session"])
router.include_router(chat_router, prefix="/chat", tags=["Chat"])
router.include_router(emotion_router, prefix="/emotion", tags=["Emotion"])
router.include_router(animation_router, prefix="/animation", tags=["Animation"])
router.include_router(voice_router, prefix="/voice", tags=["Voice"])
router.include_router(transform_router, prefix="/transform", tags=["Transform Quirk"])
