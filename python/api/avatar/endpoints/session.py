"""
Session Endpoints

Endpoints for managing avatar sessions.
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status

from ..models.session import (
    SessionCreate,
    SessionResponse,
    SessionState,
    SessionStatus,
    PersonalityConfig,
)
from ..services.session_manager import SessionManager
from ..dependencies import (
    get_api_key,
    get_session_manager,
    rate_limit_default,
)


router = APIRouter()


@router.post(
    "/create",
    response_model=SessionResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new avatar session",
    description="Create a new session for interacting with the Toga avatar.",
)
async def create_session(
    request: SessionCreate,
    api_key: str = Depends(get_api_key),
    session_manager: SessionManager = Depends(get_session_manager),
    _: None = Depends(rate_limit_default),
):
    """
    Create a new avatar session.

    - **user_id**: Optional user identifier for persistence
    - **personality_config**: Custom personality traits
    - **lifetime_hours**: Session duration (1-168 hours)
    """
    return await session_manager.create_session(request)


@router.get(
    "/{session_id}",
    response_model=SessionState,
    summary="Get session state",
    description="Retrieve the current state of an avatar session.",
)
async def get_session(
    session_id: str,
    api_key: str = Depends(get_api_key),
    session_manager: SessionManager = Depends(get_session_manager),
    _: None = Depends(rate_limit_default),
):
    """
    Get the current state of a session.

    Returns full session information including personality,
    relationship state, and metadata.
    """
    session = await session_manager.get_session(session_id)
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Session not found: {session_id}",
        )
    return session


@router.delete(
    "/{session_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete session",
    description="End and delete an avatar session.",
)
async def delete_session(
    session_id: str,
    api_key: str = Depends(get_api_key),
    session_manager: SessionManager = Depends(get_session_manager),
    _: None = Depends(rate_limit_default),
):
    """
    Delete a session and cleanup resources.

    This will immediately terminate the session and
    remove all associated data.
    """
    deleted = await session_manager.delete_session(session_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Session not found: {session_id}",
        )


@router.get(
    "",
    response_model=List[SessionState],
    summary="List sessions",
    description="List all sessions with optional filters.",
)
async def list_sessions(
    user_id: Optional[str] = None,
    status_filter: Optional[SessionStatus] = None,
    api_key: str = Depends(get_api_key),
    session_manager: SessionManager = Depends(get_session_manager),
    _: None = Depends(rate_limit_default),
):
    """
    List sessions with optional filters.

    - **user_id**: Filter by user ID
    - **status_filter**: Filter by session status
    """
    return await session_manager.list_sessions(
        user_id=user_id,
        status=status_filter,
    )


@router.patch(
    "/{session_id}/personality",
    response_model=SessionState,
    summary="Update personality",
    description="Update the personality configuration for a session.",
)
async def update_personality(
    session_id: str,
    config: PersonalityConfig,
    api_key: str = Depends(get_api_key),
    session_manager: SessionManager = Depends(get_session_manager),
    _: None = Depends(rate_limit_default),
):
    """
    Update personality configuration.

    Allows adjusting Toga's personality traits mid-session.
    """
    session = await session_manager.update_session(
        session_id,
        personality_config=config,
    )
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Session not found: {session_id}",
        )
    return session


@router.post(
    "/{session_id}/extend",
    response_model=SessionState,
    summary="Extend session",
    description="Extend the lifetime of a session.",
)
async def extend_session(
    session_id: str,
    hours: int = 24,
    api_key: str = Depends(get_api_key),
    session_manager: SessionManager = Depends(get_session_manager),
    _: None = Depends(rate_limit_default),
):
    """
    Extend session lifetime.

    - **hours**: Additional hours to add (1-168)
    """
    if hours < 1 or hours > 168:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Hours must be between 1 and 168",
        )

    session = await session_manager.get_session_internal(session_id)
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Session not found: {session_id}",
        )

    from datetime import timedelta

    session.expires_at += timedelta(hours=hours)

    return session.to_state()
