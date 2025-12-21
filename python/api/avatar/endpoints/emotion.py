"""
Emotion Endpoints

Endpoints for managing avatar emotional states.
"""

from fastapi import APIRouter, Depends, HTTPException, status

from ..models.emotion import (
    EmotionState,
    EmotionHistory,
    EmotionTrigger,
    EmotionType,
)
from ..services.session_manager import SessionManager
from ..dependencies import (
    get_api_key,
    get_session_manager,
    rate_limit_default,
)


router = APIRouter()


@router.get(
    "/{session_id}",
    response_model=EmotionHistory,
    summary="Get emotional state",
    description="Get the current emotional state and history for a session.",
)
async def get_emotion(
    session_id: str,
    api_key: str = Depends(get_api_key),
    session_manager: SessionManager = Depends(get_session_manager),
    _: None = Depends(rate_limit_default),
):
    """
    Get current emotional state.

    Returns the current emotion along with recent history
    and available emotion types.
    """
    session = await session_manager.get_session_internal(session_id)
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Session not found: {session_id}",
        )

    return EmotionHistory(
        current=session.emotion_state,
        history=[],  # TODO: Implement emotion history tracking
        available_emotions=list(EmotionType),
    )


@router.post(
    "/trigger",
    response_model=EmotionState,
    summary="Trigger emotion",
    description="Manually trigger an emotion change.",
)
async def trigger_emotion(
    trigger: EmotionTrigger,
    api_key: str = Depends(get_api_key),
    session_manager: SessionManager = Depends(get_session_manager),
    _: None = Depends(rate_limit_default),
):
    """
    Manually trigger an emotion.

    This is primarily for testing and admin purposes.
    Normal emotion changes happen automatically during chat.
    """
    session = await session_manager.get_session_internal(trigger.session_id)
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Session not found: {trigger.session_id}",
        )

    # Create new emotion state
    new_emotion = EmotionState(
        primary=trigger.emotion,
        intensity=trigger.intensity,
        valence=0.5,  # Default valence
        arousal=trigger.intensity,
    )

    # Update session
    await session_manager.update_emotion(trigger.session_id, new_emotion)

    return new_emotion


@router.get(
    "/{session_id}/live2d-params",
    summary="Get Live2D parameters",
    description="Get emotion state as Live2D parameter values.",
)
async def get_live2d_params(
    session_id: str,
    api_key: str = Depends(get_api_key),
    session_manager: SessionManager = Depends(get_session_manager),
    _: None = Depends(rate_limit_default),
):
    """
    Get Live2D parameters for current emotion.

    Returns parameter values that can be directly applied
    to the Live2D model for facial expressions.
    """
    session = await session_manager.get_session_internal(session_id)
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Session not found: {session_id}",
        )

    return {
        "emotion": session.emotion_state.primary.value,
        "parameters": session.emotion_state.to_live2d_params(),
    }
