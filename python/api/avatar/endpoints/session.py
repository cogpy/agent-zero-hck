"""
Session Endpoints

Endpoints for managing avatar sessions.
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status

from ..models.session import SessionCreate, SessionInfo
from ..services.session_manager import SessionManager
from ..dependencies import (
    get_api_key,
    get_session_manager,
    rate_limit_default,
)


router = APIRouter()


@router.post(
    "",
    response_model=SessionInfo,
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
    - **initial_emotion**: Starting emotion state
    - **metadata**: Additional session metadata
    """
    return await session_manager.create_session(request)


@router.get(
    "/{session_id}",
    response_model=SessionInfo,
    summary="Get session info",
    description="Retrieve information about an avatar session.",
)
async def get_session(
    session_id: str,
    api_key: str = Depends(get_api_key),
    session_manager: SessionManager = Depends(get_session_manager),
    _: None = Depends(rate_limit_default),
):
    """
    Get session information.

    Returns full session details including current emotion,
    relationship state, and message count.
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
    response_model=List[SessionInfo],
    summary="List sessions",
    description="List all sessions with optional filters.",
)
async def list_sessions(
    user_id: Optional[str] = None,
    status: Optional[str] = None,
    api_key: str = Depends(get_api_key),
    session_manager: SessionManager = Depends(get_session_manager),
    _: None = Depends(rate_limit_default),
):
    """
    List sessions with optional filters.

    - **user_id**: Filter by user ID
    - **status**: Filter by session status (active, inactive, expired)
    """
    return await session_manager.list_sessions(
        user_id=user_id,
        status=status,
    )
