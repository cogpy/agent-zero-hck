"""
Animation Endpoints

Endpoints for controlling avatar animations.
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status

from ..models.animation import (
    AnimationTrigger,
    AnimationQueue,
    AnimationType,
    AnimationSequence,
    ANIMATION_SEQUENCES,
)
from ..services.session_manager import SessionManager
from ..dependencies import (
    get_api_key,
    get_session_manager,
    rate_limit_default,
)


router = APIRouter()


@router.get(
    "/types",
    response_model=List[str],
    summary="List animation types",
    description="Get all available animation types.",
)
async def list_animation_types(
    api_key: str = Depends(get_api_key),
    _: None = Depends(rate_limit_default),
):
    """
    List all available animation types.

    Returns the names of all animations that can be triggered.
    """
    return [anim.value for anim in AnimationType]


@router.get(
    "/sequences",
    summary="List animation sequences",
    description="Get all pre-defined animation sequences.",
)
async def list_sequences(
    api_key: str = Depends(get_api_key),
    _: None = Depends(rate_limit_default),
):
    """
    List pre-defined animation sequences.

    Returns sequences like 'greeting', 'thinking', etc.
    """
    return {
        name: {
            "name": seq.name,
            "animation_count": len(seq.animations),
            "total_duration_ms": seq.total_duration_ms,
            "interruptible": seq.interruptible,
        }
        for name, seq in ANIMATION_SEQUENCES.items()
    }


@router.get(
    "/sequences/{name}",
    response_model=AnimationSequence,
    summary="Get animation sequence",
    description="Get details of a specific animation sequence.",
)
async def get_sequence(
    name: str,
    api_key: str = Depends(get_api_key),
    _: None = Depends(rate_limit_default),
):
    """
    Get a specific animation sequence by name.
    """
    if name not in ANIMATION_SEQUENCES:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Sequence not found: {name}",
        )
    return ANIMATION_SEQUENCES[name]


@router.post(
    "/trigger",
    response_model=AnimationTrigger,
    summary="Trigger animation",
    description="Trigger a specific animation on the avatar.",
)
async def trigger_animation(
    trigger: AnimationTrigger,
    session_id: str,
    api_key: str = Depends(get_api_key),
    session_manager: SessionManager = Depends(get_session_manager),
    _: None = Depends(rate_limit_default),
):
    """
    Trigger a specific animation.

    The animation will be queued and played on the avatar.
    """
    session = await session_manager.get_session_internal(session_id)
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Session not found: {session_id}",
        )

    # In a real implementation, this would add to an animation queue
    # For now, we just return the trigger as confirmation
    return trigger


@router.post(
    "/sequence/{name}",
    summary="Play animation sequence",
    description="Play a pre-defined animation sequence.",
)
async def play_sequence(
    name: str,
    session_id: str,
    api_key: str = Depends(get_api_key),
    session_manager: SessionManager = Depends(get_session_manager),
    _: None = Depends(rate_limit_default),
):
    """
    Play a pre-defined animation sequence.

    Sequences are collections of animations that play in order.
    """
    session = await session_manager.get_session_internal(session_id)
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Session not found: {session_id}",
        )

    if name not in ANIMATION_SEQUENCES:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Sequence not found: {name}",
        )

    sequence = ANIMATION_SEQUENCES[name]

    return {
        "status": "playing",
        "sequence": name,
        "animations": [a.model_dump() for a in sequence.animations],
        "total_duration_ms": sequence.total_duration_ms,
    }


@router.get(
    "/{session_id}/queue",
    response_model=AnimationQueue,
    summary="Get animation queue",
    description="Get the current animation queue for a session.",
)
async def get_animation_queue(
    session_id: str,
    api_key: str = Depends(get_api_key),
    session_manager: SessionManager = Depends(get_session_manager),
    _: None = Depends(rate_limit_default),
):
    """
    Get the current animation queue.

    Shows pending animations and the currently playing animation.
    """
    session = await session_manager.get_session_internal(session_id)
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Session not found: {session_id}",
        )

    # Return default queue state
    return AnimationQueue(
        queue=[],
        current_animation=AnimationType.IDLE_BREATHE,
        loop_animations=[AnimationType.IDLE_BREATHE, AnimationType.IDLE_BLINK],
        is_talking=False,
    )
