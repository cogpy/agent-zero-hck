"""
Session Manager Service

Manages avatar sessions and their lifecycle.
"""

import asyncio
import uuid
from datetime import datetime, timedelta
from typing import Dict, Optional, List
from dataclasses import dataclass, field

from ..models.session import (
    SessionCreate,
    SessionResponse,
    SessionState,
    SessionStatus,
    PersonalityConfig,
    PersonalityState,
    RelationshipState,
)
from ..models.emotion import EmotionState, EmotionType


@dataclass
class Session:
    """Internal session representation."""

    session_id: str
    context_id: str
    user_id: Optional[str]
    personality_config: PersonalityConfig
    personality_state: PersonalityState
    relationship_state: RelationshipState
    emotion_state: EmotionState
    status: SessionStatus
    message_count: int
    created_at: datetime
    expires_at: datetime
    last_activity: datetime
    metadata: Dict = field(default_factory=dict)

    def to_state(self) -> SessionState:
        """Convert to SessionState model."""
        return SessionState(
            session_id=self.session_id,
            context_id=self.context_id,
            status=self.status,
            user_id=self.user_id,
            personality=self.personality_state,
            personality_config=self.personality_config,
            relationship=self.relationship_state,
            message_count=self.message_count,
            created_at=self.created_at,
            expires_at=self.expires_at,
            last_activity=self.last_activity,
            metadata=self.metadata,
        )

    def to_response(self) -> SessionResponse:
        """Convert to SessionResponse model."""
        return SessionResponse(
            session_id=self.session_id,
            context_id=self.context_id,
            personality=self.personality_state,
            relationship=self.relationship_state,
            created_at=self.created_at,
            expires_at=self.expires_at,
        )


class SessionManager:
    """Manages avatar sessions."""

    def __init__(self):
        self.sessions: Dict[str, Session] = {}
        self._cleanup_task: Optional[asyncio.Task] = None
        self._lock = asyncio.Lock()

    async def initialize(self):
        """Initialize the session manager."""
        # Start cleanup task
        self._cleanup_task = asyncio.create_task(self._cleanup_loop())

    async def cleanup(self):
        """Cleanup resources."""
        if self._cleanup_task:
            self._cleanup_task.cancel()
            try:
                await self._cleanup_task
            except asyncio.CancelledError:
                pass

    async def _cleanup_loop(self):
        """Periodically clean up expired sessions."""
        while True:
            try:
                await asyncio.sleep(60)  # Check every minute
                await self._cleanup_expired()
            except asyncio.CancelledError:
                break
            except Exception as e:
                print(f"Session cleanup error: {e}")

    async def _cleanup_expired(self):
        """Remove expired sessions."""
        async with self._lock:
            now = datetime.utcnow()
            expired = [
                sid
                for sid, session in self.sessions.items()
                if session.expires_at < now
            ]
            for sid in expired:
                del self.sessions[sid]
                print(f"Cleaned up expired session: {sid}")

    async def create_session(
        self,
        request: SessionCreate,
    ) -> SessionResponse:
        """Create a new avatar session."""
        async with self._lock:
            session_id = f"sess-{uuid.uuid4().hex[:12]}"
            context_id = f"ctx-{uuid.uuid4().hex[:12]}"

            now = datetime.utcnow()
            expires_at = now + timedelta(hours=request.lifetime_hours)

            # Use provided config or defaults
            personality_config = request.personality_config or PersonalityConfig()

            # Initialize personality state based on config
            personality_state = PersonalityState(
                name="Toga",
                current_emotion="excited",  # Start excited to meet new friend
                energy_level=0.8,
                mood_valence=0.7,
            )

            # Initialize relationship state
            relationship_state = RelationshipState(
                familiarity=0.0,
                trust_level=0.5,
                affection=0.0,
                interaction_count=0,
            )

            # Initialize emotion state
            emotion_state = EmotionState(
                primary=EmotionType.EXCITED,
                secondary=EmotionType.CURIOUS,
                intensity=0.7,
                valence=0.8,
                arousal=0.7,
            )

            session = Session(
                session_id=session_id,
                context_id=context_id,
                user_id=request.user_id,
                personality_config=personality_config,
                personality_state=personality_state,
                relationship_state=relationship_state,
                emotion_state=emotion_state,
                status=SessionStatus.ACTIVE,
                message_count=0,
                created_at=now,
                expires_at=expires_at,
                last_activity=now,
            )

            self.sessions[session_id] = session

            return session.to_response()

    async def get_session(self, session_id: str) -> Optional[SessionState]:
        """Get session state by ID."""
        async with self._lock:
            session = self.sessions.get(session_id)
            if not session:
                return None

            # Check if expired
            if session.expires_at < datetime.utcnow():
                session.status = SessionStatus.EXPIRED

            return session.to_state()

    async def get_session_internal(self, session_id: str) -> Optional[Session]:
        """Get internal session object."""
        return self.sessions.get(session_id)

    async def update_session(
        self,
        session_id: str,
        **updates,
    ) -> Optional[SessionState]:
        """Update session properties."""
        async with self._lock:
            session = self.sessions.get(session_id)
            if not session:
                return None

            # Update allowed fields
            if "personality_config" in updates:
                session.personality_config = updates["personality_config"]
            if "personality_state" in updates:
                session.personality_state = updates["personality_state"]
            if "relationship_state" in updates:
                session.relationship_state = updates["relationship_state"]
            if "emotion_state" in updates:
                session.emotion_state = updates["emotion_state"]
            if "metadata" in updates:
                session.metadata.update(updates["metadata"])

            session.last_activity = datetime.utcnow()

            return session.to_state()

    async def increment_message_count(self, session_id: str) -> int:
        """Increment message count and return new value."""
        async with self._lock:
            session = self.sessions.get(session_id)
            if session:
                session.message_count += 1
                session.last_activity = datetime.utcnow()

                # Update relationship based on interaction
                session.relationship_state.interaction_count += 1
                session.relationship_state.familiarity = min(
                    1.0, session.relationship_state.familiarity + 0.01
                )

                return session.message_count
            return 0

    async def update_emotion(
        self,
        session_id: str,
        emotion: EmotionState,
    ) -> bool:
        """Update session emotion state."""
        async with self._lock:
            session = self.sessions.get(session_id)
            if session:
                session.emotion_state = emotion
                session.personality_state.current_emotion = emotion.primary.value
                session.last_activity = datetime.utcnow()
                return True
            return False

    async def delete_session(self, session_id: str) -> bool:
        """Delete a session."""
        async with self._lock:
            if session_id in self.sessions:
                del self.sessions[session_id]
                return True
            return False

    async def list_sessions(
        self,
        user_id: Optional[str] = None,
        status: Optional[SessionStatus] = None,
    ) -> List[SessionState]:
        """List sessions with optional filters."""
        async with self._lock:
            sessions = []
            for session in self.sessions.values():
                if user_id and session.user_id != user_id:
                    continue
                if status and session.status != status:
                    continue
                sessions.append(session.to_state())
            return sessions

    async def get_active_count(self) -> int:
        """Get count of active sessions."""
        async with self._lock:
            return sum(
                1 for s in self.sessions.values() if s.status == SessionStatus.ACTIVE
            )
