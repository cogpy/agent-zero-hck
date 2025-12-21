"""
Chat Endpoints

Endpoints for chat interactions with the Toga avatar.
"""

import uuid
import time
import asyncio
from datetime import datetime
from typing import AsyncGenerator

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse

from ..models.chat import (
    ChatRequest,
    ChatResponse,
    ChatStreamEvent,
    ChatStreamEventType,
    ResponseContent,
    ChatContext,
    VoiceResponse,
)
from ..models.emotion import EmotionState, EmotionType
from ..models.animation import AnimationTrigger, AnimationType
from ..services.session_manager import SessionManager
from ..dependencies import (
    get_api_key,
    get_session_manager,
    rate_limit_chat,
)


router = APIRouter()


# Import NPU for response generation
try:
    from python.helpers.cognitive.npu import NPUCoprocessor, initialize_npu

    _npu = None

    def get_npu() -> NPUCoprocessor:
        global _npu
        if _npu is None:
            _npu = initialize_npu()
        return _npu

except ImportError:

    def get_npu():
        return None


# Import Toga personality
try:
    from python.helpers.toga_personality import (
        TogaPersonality,
        initialize_toga_personality,
    )

    _personality = None

    def get_personality() -> TogaPersonality:
        global _personality
        if _personality is None:
            _personality = initialize_toga_personality()
        return _personality

except ImportError:

    def get_personality():
        return None


def analyze_emotion_from_response(text: str) -> EmotionState:
    """Analyze response text to determine appropriate emotion."""
    text_lower = text.lower()

    # Check for emotion indicators
    if any(w in text_lower for w in ["hey hey", "yay", "excited", "!"]):
        return EmotionState(
            primary=EmotionType.EXCITED,
            intensity=0.8,
            valence=0.9,
            arousal=0.85,
        )
    elif any(w in text_lower for w in ["hmm", "wonder", "curious", "?"]):
        return EmotionState(
            primary=EmotionType.CURIOUS,
            intensity=0.7,
            valence=0.6,
            arousal=0.5,
        )
    elif any(w in text_lower for w in ["hehe", "tee-hee", "mischief"]):
        return EmotionState(
            primary=EmotionType.MISCHIEVOUS,
            intensity=0.75,
            valence=0.7,
            arousal=0.6,
        )
    elif any(w in text_lower for w in ["aww", "sweet", "love", "cutie"]):
        return EmotionState(
            primary=EmotionType.AFFECTIONATE,
            intensity=0.7,
            valence=0.8,
            arousal=0.4,
        )
    elif any(w in text_lower for w in ["oh!", "wow", "really"]):
        return EmotionState(
            primary=EmotionType.SURPRISED,
            intensity=0.8,
            valence=0.7,
            arousal=0.8,
        )
    elif any(w in text_lower for w in ["happy", "great", "wonderful"]):
        return EmotionState(
            primary=EmotionType.HAPPY,
            intensity=0.75,
            valence=0.85,
            arousal=0.6,
        )
    else:
        return EmotionState(
            primary=EmotionType.PLAYFUL,
            intensity=0.6,
            valence=0.6,
            arousal=0.5,
        )


def get_animation_triggers(emotion: EmotionState, text: str) -> list:
    """Get animation triggers based on emotion and response."""
    triggers = []

    # Base animation based on emotion
    emotion_animations = {
        EmotionType.EXCITED: AnimationType.BOUNCE,
        EmotionType.CURIOUS: AnimationType.HEAD_TILT,
        EmotionType.MISCHIEVOUS: AnimationType.WINK,
        EmotionType.AFFECTIONATE: AnimationType.LEAN_FORWARD,
        EmotionType.SURPRISED: AnimationType.LEAN_BACK,
        EmotionType.HAPPY: AnimationType.GIGGLE,
        EmotionType.PLAYFUL: AnimationType.BOUNCE,
    }

    anim_type = emotion_animations.get(emotion.primary, AnimationType.NOD)
    triggers.append(
        AnimationTrigger(
            type=anim_type,
            intensity=emotion.intensity,
            duration_ms=int(500 * emotion.intensity),
        )
    )

    # Add specific triggers based on text content
    if "*bounces*" in text.lower() or "*bounce*" in text.lower():
        triggers.append(
            AnimationTrigger(
                type=AnimationType.BOUNCE,
                intensity=0.8,
                duration_ms=600,
            )
        )

    if "*wink*" in text.lower():
        triggers.append(
            AnimationTrigger(
                type=AnimationType.WINK,
                intensity=0.9,
                duration_ms=400,
                parameters={"eye": "left"},
            )
        )

    if "*giggles*" in text.lower() or "*laughs*" in text.lower():
        triggers.append(
            AnimationTrigger(
                type=AnimationType.GIGGLE,
                intensity=0.7,
                duration_ms=800,
            )
        )

    return triggers


@router.post(
    "",
    response_model=ChatResponse,
    summary="Send chat message",
    description="Send a message to Toga and receive a response.",
)
async def send_message(
    request: ChatRequest,
    api_key: str = Depends(get_api_key),
    session_manager: SessionManager = Depends(get_session_manager),
    _: None = Depends(rate_limit_chat),
):
    """
    Send a message to Toga.

    Returns Toga's response along with emotion data,
    animation triggers, and optional voice synthesis parameters.
    """
    start_time = time.time()

    # Validate session
    session = await session_manager.get_session_internal(request.session_id)
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Session not found: {request.session_id}",
        )

    # Generate response using NPU
    npu = get_npu()
    personality = get_personality()

    if npu and npu.is_available():
        # Use NPU for response generation
        response_text = npu.generate(
            request.message,
            max_tokens=500,
        )
    elif personality:
        # Use personality engine
        framed = personality.frame_input(request.message)
        response_text = personality.add_commentary(framed)
    else:
        # Fallback response
        response_text = f"Hey hey! *bounces excitedly* Oh, you said '{request.message}'! That's so interesting~ Tell me more!"

    # Analyze emotion
    emotion = analyze_emotion_from_response(response_text)

    # Get animation triggers
    animations = []
    if request.request_animations:
        animations = get_animation_triggers(emotion, response_text)

    # Prepare voice data
    voice = None
    if request.request_voice:
        voice = VoiceResponse(
            text=response_text.replace("*", ""),  # Remove action markers
            emotion=emotion.primary,
            pitch_modifier=1.1 if emotion.arousal > 0.7 else 1.0,
            rate_modifier=1.15 if emotion.arousal > 0.7 else 1.0,
        )

    # Update session
    message_count = await session_manager.increment_message_count(request.session_id)
    await session_manager.update_emotion(request.session_id, emotion)

    # Build response
    processing_time = int((time.time() - start_time) * 1000)

    return ChatResponse(
        response=ResponseContent(
            text=response_text,
            emotion=emotion if request.request_emotion else None,
            animation_triggers=animations,
            voice=voice,
        ),
        context=ChatContext(
            turn_count=message_count,
            relationship_level=session.relationship_state.familiarity,
            topics_discussed=[],
        ),
        session_id=request.session_id,
        message_id=f"msg-{uuid.uuid4().hex[:12]}",
        timestamp=datetime.utcnow(),
        processing_time_ms=processing_time,
    )


@router.post(
    "/stream",
    summary="Stream chat response",
    description="Send a message and receive streaming response via SSE.",
)
async def stream_message(
    request: ChatRequest,
    api_key: str = Depends(get_api_key),
    session_manager: SessionManager = Depends(get_session_manager),
    _: None = Depends(rate_limit_chat),
):
    """
    Stream Toga's response using Server-Sent Events.

    Events include:
    - `token`: Individual response tokens
    - `emotion`: Emotion state updates
    - `animation`: Animation triggers
    - `complete`: Final response data
    """
    # Validate session
    session = await session_manager.get_session_internal(request.session_id)
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Session not found: {request.session_id}",
        )

    async def generate_stream() -> AsyncGenerator[str, None]:
        sequence = 0
        full_response = ""

        # Get NPU for streaming
        npu = get_npu()

        if npu and npu.is_available():
            # Stream from NPU
            async def token_callback(token: str):
                nonlocal sequence, full_response
                full_response += token
                event = ChatStreamEvent(
                    event_type=ChatStreamEventType.TOKEN,
                    data={"token": token},
                    sequence=sequence,
                )
                sequence += 1
                return event.to_sse()

            # Generate with streaming
            for token in npu.generate(
                request.message,
                max_tokens=500,
                stream=True,
            ):
                full_response += token
                event = ChatStreamEvent(
                    event_type=ChatStreamEventType.TOKEN,
                    data={"token": token},
                    sequence=sequence,
                )
                sequence += 1
                yield event.to_sse()
                await asyncio.sleep(0.01)  # Small delay for streaming effect
        else:
            # Fallback: simulate streaming
            response = (
                f"Hey hey! *bounces* Oh, you said '{request.message}'! That's fun~"
            )
            for word in response.split():
                full_response += word + " "
                event = ChatStreamEvent(
                    event_type=ChatStreamEventType.TOKEN,
                    data={"token": word + " "},
                    sequence=sequence,
                )
                sequence += 1
                yield event.to_sse()
                await asyncio.sleep(0.05)

        # Analyze emotion
        emotion = analyze_emotion_from_response(full_response)

        # Send emotion event
        event = ChatStreamEvent(
            event_type=ChatStreamEventType.EMOTION,
            data=emotion.model_dump(),
            sequence=sequence,
        )
        sequence += 1
        yield event.to_sse()

        # Send animation events
        if request.request_animations:
            animations = get_animation_triggers(emotion, full_response)
            for anim in animations:
                event = ChatStreamEvent(
                    event_type=ChatStreamEventType.ANIMATION,
                    data=anim.model_dump(),
                    sequence=sequence,
                )
                sequence += 1
                yield event.to_sse()

        # Update session
        await session_manager.increment_message_count(request.session_id)
        await session_manager.update_emotion(request.session_id, emotion)

        # Send complete event
        event = ChatStreamEvent(
            event_type=ChatStreamEventType.COMPLETE,
            data={
                "full_response": full_response.strip(),
                "message_id": f"msg-{uuid.uuid4().hex[:12]}",
            },
            sequence=sequence,
        )
        yield event.to_sse()

    return StreamingResponse(
        generate_stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        },
    )
