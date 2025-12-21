"""
Voice Endpoints

Endpoints for voice synthesis and lip sync.
"""

import uuid
import os
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status

from ..models.voice import (
    VoiceConfig,
    VoiceSynthesisRequest,
    VoiceSynthesisResponse,
    LipSyncData,
    VisemeData,
    Viseme,
    VoiceId,
    PHONEME_TO_VISEME,
)
from ..models.emotion import EmotionType
from ..services.session_manager import SessionManager
from ..dependencies import (
    get_api_key,
    get_session_manager,
    rate_limit_voice,
)


router = APIRouter()


def generate_mock_lip_sync(text: str, duration_ms: int) -> LipSyncData:
    """Generate mock lip sync data based on text."""
    visemes = []
    words = text.replace("*", "").split()

    if not words:
        return LipSyncData(visemes=[], duration_ms=0)

    time_per_word = duration_ms / len(words)
    current_time = 0

    for word in words:
        # Simple viseme assignment based on first letter
        first_char = word[0].upper() if word else "A"

        if first_char in "AEIOU":
            viseme = Viseme.A if first_char in "AO" else Viseme.E
        elif first_char in "MBP":
            viseme = Viseme.M
        elif first_char in "FV":
            viseme = Viseme.F
        elif first_char in "WQ":
            viseme = Viseme.W
        elif first_char in "LN":
            viseme = Viseme.L
        else:
            viseme = Viseme.TH

        visemes.append(
            VisemeData(
                viseme=viseme,
                start_ms=int(current_time),
                end_ms=int(current_time + time_per_word * 0.8),
                intensity=0.8,
            )
        )

        # Add silence between words
        visemes.append(
            VisemeData(
                viseme=Viseme.SILENCE,
                start_ms=int(current_time + time_per_word * 0.8),
                end_ms=int(current_time + time_per_word),
                intensity=1.0,
            )
        )

        current_time += time_per_word

    return LipSyncData(
        visemes=visemes,
        duration_ms=duration_ms,
    )


@router.get(
    "/voices",
    response_model=List[str],
    summary="List available voices",
    description="Get all available voice presets.",
)
async def list_voices(
    api_key: str = Depends(get_api_key),
):
    """
    List all available voice presets.
    """
    return [v.value for v in VoiceId]


@router.get(
    "/config/{session_id}",
    response_model=VoiceConfig,
    summary="Get voice config",
    description="Get the voice configuration for a session.",
)
async def get_voice_config(
    session_id: str,
    api_key: str = Depends(get_api_key),
    session_manager: SessionManager = Depends(get_session_manager),
):
    """
    Get current voice configuration.
    """
    session = await session_manager.get_session_internal(session_id)
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Session not found: {session_id}",
        )

    # Return default config (could be stored in session metadata)
    return VoiceConfig()


@router.post(
    "/synthesize",
    response_model=VoiceSynthesisResponse,
    summary="Synthesize speech",
    description="Generate speech audio from text with optional lip sync.",
)
async def synthesize_speech(
    request: VoiceSynthesisRequest,
    api_key: str = Depends(get_api_key),
    session_manager: SessionManager = Depends(get_session_manager),
    _: None = Depends(rate_limit_voice),
):
    """
    Synthesize speech from text.

    Returns audio URL and lip sync data for avatar animation.

    Note: This is a mock implementation. In production,
    this would integrate with a TTS service like:
    - ElevenLabs
    - Azure Speech
    - Google Cloud TTS
    - OpenAI TTS
    """
    session = await session_manager.get_session_internal(request.session_id)
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Session not found: {request.session_id}",
        )

    # Get voice config
    voice_config = request.voice_config or VoiceConfig()

    # Apply emotion modifiers
    voice_config = voice_config.apply_emotion(request.emotion)

    # Calculate estimated duration (rough estimate: 150ms per word)
    words = len(request.text.split())
    duration_ms = int(words * 150 / voice_config.rate)

    # Generate audio ID
    audio_id = uuid.uuid4().hex[:12]

    # Generate lip sync data if requested
    lip_sync = None
    if request.generate_lip_sync:
        lip_sync = generate_mock_lip_sync(request.text, duration_ms)

    # In production, this would:
    # 1. Call TTS API to generate audio
    # 2. Save audio to cache directory
    # 3. Generate accurate lip sync from audio analysis

    return VoiceSynthesisResponse(
        audio_url=f"/api/avatar/audio/{audio_id}.{request.output_format}",
        audio_id=audio_id,
        duration_ms=duration_ms,
        phonemes=[],  # Would be populated from TTS service
        lip_sync=lip_sync,
        voice_config_used=voice_config,
    )


@router.post(
    "/lip-sync",
    response_model=LipSyncData,
    summary="Generate lip sync",
    description="Generate lip sync data from text without audio.",
)
async def generate_lip_sync(
    text: str,
    duration_ms: int = 0,
    api_key: str = Depends(get_api_key),
):
    """
    Generate lip sync data from text.

    Useful for pre-generating lip sync for known text,
    or for client-side TTS where audio is generated locally.
    """
    if duration_ms <= 0:
        # Estimate duration
        words = len(text.split())
        duration_ms = words * 150

    return generate_mock_lip_sync(text, duration_ms)


@router.get(
    "/viseme-map",
    summary="Get viseme mapping",
    description="Get the phoneme to viseme mapping table.",
)
async def get_viseme_map(
    api_key: str = Depends(get_api_key),
):
    """
    Get phoneme to viseme mapping.

    Useful for client-side lip sync generation.
    """
    return {
        "mapping": {k: v.value for k, v in PHONEME_TO_VISEME.items()},
        "visemes": [v.value for v in Viseme],
    }
