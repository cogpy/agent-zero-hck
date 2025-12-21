"""
Avatar API Tests

Comprehensive tests for the Avatar API endpoints.
"""

import pytest
import asyncio
from datetime import datetime, timedelta
from unittest.mock import AsyncMock, MagicMock, patch

# Test imports
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))


class TestSessionModels:
    """Tests for session models."""

    def test_personality_config_defaults(self):
        """Test PersonalityConfig default values."""
        from python.api.avatar.models.session import PersonalityConfig

        config = PersonalityConfig()
        assert config.chaos_level == 0.7
        assert config.playfulness == 0.9
        assert config.curiosity == 0.85
        assert config.affection_tendency == 0.8
        assert config.mischief_factor == 0.75

    def test_personality_config_validation(self):
        """Test PersonalityConfig validation."""
        from python.api.avatar.models.session import PersonalityConfig
        from pydantic import ValidationError

        # Valid config
        config = PersonalityConfig(chaos_level=0.5, playfulness=0.8)
        assert config.chaos_level == 0.5

        # Invalid config (out of range)
        with pytest.raises(ValidationError):
            PersonalityConfig(chaos_level=1.5)

        with pytest.raises(ValidationError):
            PersonalityConfig(playfulness=-0.1)

    def test_session_create_model(self):
        """Test SessionCreate model."""
        from python.api.avatar.models.session import SessionCreate, PersonalityConfig

        # Minimal creation
        session = SessionCreate()
        assert session.user_id is None
        assert session.lifetime_hours == 24

        # Full creation
        config = PersonalityConfig(chaos_level=0.5)
        session = SessionCreate(
            user_id="test-user",
            personality_config=config,
            lifetime_hours=48,
        )
        assert session.user_id == "test-user"
        assert session.lifetime_hours == 48
        assert session.personality_config.chaos_level == 0.5


class TestEmotionModels:
    """Tests for emotion models."""

    def test_emotion_state_defaults(self):
        """Test EmotionState default values."""
        from python.api.avatar.models.emotion import EmotionState, EmotionType

        state = EmotionState()
        assert state.primary == EmotionType.NEUTRAL
        assert state.secondary is None
        assert state.intensity == 0.5

    def test_emotion_state_to_live2d_params(self):
        """Test conversion to Live2D parameters."""
        from python.api.avatar.models.emotion import EmotionState, EmotionType

        # Happy emotion
        state = EmotionState(primary=EmotionType.HAPPY, intensity=0.8)
        params = state.to_live2d_params()
        assert "ParamMouthForm" in params
        assert params["ParamMouthForm"] > 0  # Smile

        # Excited emotion
        state = EmotionState(primary=EmotionType.EXCITED, intensity=0.9)
        params = state.to_live2d_params()
        assert params["ParamMouthForm"] == 1.0

    def test_emotion_trigger_validation(self):
        """Test EmotionTrigger validation."""
        from python.api.avatar.models.emotion import EmotionTrigger, EmotionType

        trigger = EmotionTrigger(
            session_id="sess-123",
            emotion=EmotionType.EXCITED,
            intensity=0.8,
            duration_ms=3000,
        )
        assert trigger.emotion == EmotionType.EXCITED
        assert trigger.duration_ms == 3000


class TestAnimationModels:
    """Tests for animation models."""

    def test_animation_trigger_defaults(self):
        """Test AnimationTrigger default values."""
        from python.api.avatar.models.animation import (
            AnimationTrigger,
            AnimationType,
            AnimationEasing,
        )

        trigger = AnimationTrigger(type=AnimationType.BOUNCE)
        assert trigger.intensity == 0.5
        assert trigger.duration_ms == 500
        assert trigger.easing == AnimationEasing.EASE_IN_OUT
        assert trigger.loop is False

    def test_animation_to_live2d_motion(self):
        """Test conversion to Live2D motion data."""
        from python.api.avatar.models.animation import AnimationTrigger, AnimationType

        trigger = AnimationTrigger(
            type=AnimationType.HEAD_TILT,
            intensity=0.7,
            duration_ms=600,
            parameters={"direction": "right"},
        )
        motion = trigger.to_live2d_motion()
        assert motion["type"] == "head_tilt"
        assert motion["duration"] == 0.6
        assert "param_angle_z" in motion

    def test_animation_sequences(self):
        """Test pre-defined animation sequences."""
        from python.api.avatar.models.animation import ANIMATION_SEQUENCES

        assert "greeting" in ANIMATION_SEQUENCES
        assert "thinking" in ANIMATION_SEQUENCES
        assert "excited" in ANIMATION_SEQUENCES

        greeting = ANIMATION_SEQUENCES["greeting"]
        assert len(greeting.animations) > 0
        assert greeting.total_duration_ms > 0


class TestVoiceModels:
    """Tests for voice models."""

    def test_voice_config_defaults(self):
        """Test VoiceConfig default values."""
        from python.api.avatar.models.voice import VoiceConfig, VoiceId

        config = VoiceConfig()
        assert config.voice_id == VoiceId.TOGA_DEFAULT
        assert config.pitch == 1.0
        assert config.rate == 1.0
        assert config.volume == 1.0

    def test_voice_config_apply_emotion(self):
        """Test applying emotion modifiers to voice config."""
        from python.api.avatar.models.voice import VoiceConfig
        from python.api.avatar.models.emotion import EmotionType

        config = VoiceConfig()
        excited_config = config.apply_emotion(EmotionType.EXCITED)

        # Excited should increase pitch and rate
        assert excited_config.pitch > config.pitch
        assert excited_config.rate > config.rate

    def test_lip_sync_data_to_live2d(self):
        """Test LipSyncData conversion to Live2D params."""
        from python.api.avatar.models.voice import LipSyncData, VisemeData, Viseme

        lip_sync = LipSyncData(
            visemes=[
                VisemeData(viseme=Viseme.A, start_ms=0, end_ms=100, intensity=0.8),
                VisemeData(viseme=Viseme.M, start_ms=100, end_ms=200, intensity=0.9),
            ],
            duration_ms=200,
        )
        keyframes = lip_sync.to_live2d_params()
        assert len(keyframes) == 2
        assert "time" in keyframes[0]
        assert "params" in keyframes[0]


class TestChatModels:
    """Tests for chat models."""

    def test_chat_request_validation(self):
        """Test ChatRequest validation."""
        from python.api.avatar.models.chat import ChatRequest
        from pydantic import ValidationError

        # Valid request
        request = ChatRequest(
            session_id="sess-123",
            message="Hello Toga!",
        )
        assert request.message == "Hello Toga!"
        assert request.request_emotion is True

        # Empty message should fail
        with pytest.raises(ValidationError):
            ChatRequest(session_id="sess-123", message="")

    def test_chat_stream_event_to_sse(self):
        """Test ChatStreamEvent SSE conversion."""
        from python.api.avatar.models.chat import ChatStreamEvent, ChatStreamEventType

        event = ChatStreamEvent(
            event_type=ChatStreamEventType.TOKEN,
            data={"token": "Hello"},
            sequence=1,
        )
        sse = event.to_sse()
        assert "event: token" in sse
        assert "data:" in sse
        assert "Hello" in sse


class TestSessionManager:
    """Tests for SessionManager service."""

    @pytest.fixture
    def session_manager(self):
        """Create a session manager for testing."""
        from python.api.avatar.services.session_manager import SessionManager

        return SessionManager()

    @pytest.mark.asyncio
    async def test_create_session(self, session_manager):
        """Test session creation."""
        from python.api.avatar.models.session import SessionCreate

        request = SessionCreate(user_id="test-user")
        response = await session_manager.create_session(request)

        assert response.session_id.startswith("sess-")
        assert response.context_id.startswith("ctx-")
        assert response.personality.name == "Toga"

    @pytest.mark.asyncio
    async def test_get_session(self, session_manager):
        """Test session retrieval."""
        from python.api.avatar.models.session import SessionCreate

        # Create session
        request = SessionCreate()
        response = await session_manager.create_session(request)

        # Get session
        session = await session_manager.get_session(response.session_id)
        assert session is not None
        assert session.session_id == response.session_id

    @pytest.mark.asyncio
    async def test_delete_session(self, session_manager):
        """Test session deletion."""
        from python.api.avatar.models.session import SessionCreate

        # Create session
        request = SessionCreate()
        response = await session_manager.create_session(request)

        # Delete session
        deleted = await session_manager.delete_session(response.session_id)
        assert deleted is True

        # Verify deleted
        session = await session_manager.get_session(response.session_id)
        assert session is None

    @pytest.mark.asyncio
    async def test_increment_message_count(self, session_manager):
        """Test message count incrementing."""
        from python.api.avatar.models.session import SessionCreate

        request = SessionCreate()
        response = await session_manager.create_session(request)

        count = await session_manager.increment_message_count(response.session_id)
        assert count == 1

        count = await session_manager.increment_message_count(response.session_id)
        assert count == 2


class TestWebSocketHandler:
    """Tests for WebSocket handler."""

    def test_websocket_message_serialization(self):
        """Test WebSocketMessage JSON serialization."""
        from python.api.avatar.websocket.handler import WebSocketMessage, MessageType

        message = WebSocketMessage(
            type=MessageType.CHAT,
            data={"message": "Hello"},
            session_id="sess-123",
        )

        json_str = message.to_json()
        assert "chat" in json_str
        assert "Hello" in json_str

        # Parse back
        parsed = WebSocketMessage.from_json(json_str)
        assert parsed.type == MessageType.CHAT
        assert parsed.data["message"] == "Hello"

    def test_connection_manager(self):
        """Test ConnectionManager basic operations."""
        from python.api.avatar.websocket.handler import ConnectionManager

        manager = ConnectionManager()
        assert manager.get_connection_count() == 0


class TestDependencies:
    """Tests for API dependencies."""

    def test_rate_limiter(self):
        """Test rate limiter functionality."""
        from python.api.avatar.dependencies import RateLimiter

        limiter = RateLimiter()

        # Should allow initial requests
        assert limiter.check("test-key", "default") is True

        # Simulate many requests (98 more to reach 99 total)
        for _ in range(98):
            limiter.check("test-key", "default")

        # Should still allow (100 limit, we've used 99)
        assert limiter.check("test-key", "default") is True

        # Now at 100, next should be blocked
        assert limiter.check("test-key", "default") is False


# Run tests
if __name__ == "__main__":
    pytest.main([__file__, "-v"])
