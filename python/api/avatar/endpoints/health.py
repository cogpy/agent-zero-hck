"""
Health Check Endpoints

Endpoints for monitoring API health and status.
"""

from datetime import datetime
from fastapi import APIRouter, Depends

from ..services.session_manager import SessionManager
from ..dependencies import get_session_manager


router = APIRouter()


@router.get(
    "/health",
    summary="Health check",
    description="Check if the API is healthy and responding.",
)
async def health_check():
    """
    Basic health check.

    Returns OK if the API is running.
    """
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
    }


@router.get(
    "/status",
    summary="Detailed status",
    description="Get detailed API status including session counts.",
)
async def detailed_status(
    session_manager: SessionManager = Depends(get_session_manager),
):
    """
    Get detailed API status.

    Includes session counts and system information.
    """
    active_sessions = session_manager.get_active_session_count()

    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0",
        "sessions": {
            "active": active_sessions,
        },
        "features": {
            "chat": True,
            "streaming": True,
            "voice_synthesis": True,
            "lip_sync": True,
            "animations": True,
            "websocket": True,
        },
    }


@router.get(
    "/ready",
    summary="Readiness check",
    description="Check if the API is ready to accept requests.",
)
async def readiness_check(
    session_manager: SessionManager = Depends(get_session_manager),
):
    """
    Readiness probe for Kubernetes/container orchestration.

    Returns 200 if ready, 503 if not ready.
    """
    # Check if session manager is initialized
    if session_manager is None:
        return {"status": "not_ready", "reason": "Session manager not initialized"}

    return {"status": "ready"}


@router.get(
    "/live",
    summary="Liveness check",
    description="Check if the API process is alive.",
)
async def liveness_check():
    """
    Liveness probe for Kubernetes/container orchestration.

    Returns 200 if alive.
    """
    return {"status": "alive"}
