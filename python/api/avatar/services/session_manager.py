"""
Session Manager Service

Manages avatar sessions and their lifecycle.
"""

import asyncio
import uuid
from datetime import datetime, timedelta
from typing import Dict, Optional
from dataclasses import dataclass, field

from ..models.session import SessionCreate, SessionInfo, RelationshipState
from ..models.emotion import EmotionState, EmotionType


@dataclass
class Session:
    """Internal session representation."""

    session_id: str
    user_id: Optional[str]
    created_at: datetime
    last_activity: datetime
    message_count: int
    current_emotion: EmotionState
    relationship_state: RelationshipState
    metadata: Dict = field(default_factory=dict)
    status: str = "active"  # active, inactive, expired

    def to_info(self) -> SessionInfo:
        """Convert to SessionInfo model."""
        return SessionInfo(
            session_id=self.session_id,
            user_id=self.user_id,
            created_at=self.created_at,
            last_activity=self.last_activity,
            message_count=self.message_count,
            current_emotion=self.current_emotion,
            relationship_state=self.relationship_state,
            metadata=self.metadata,
        )


class SessionManager:
    """Manages avatar sessions."""

    def __init__(self, session_timeout_minutes: int = 60):
        self.sessions: Dict[str, Session] = {}
        self.session_timeout = timedelta(minutes=session_timeout_minutes)
        self._cleanup_task: Optional[asyncio.Task] = None
        self._lock = asyncio.Lock()

    async def initialize(self):
        """Initialize the session manager."""
        print("📝 Initializing Session Manager...")
        # Start cleanup task
        self._cleanup_task = asyncio.create_task(self._cleanup_loop())
        print("✅ Session Manager initialized")

    async def cleanup(self):
        """Cleanup resources."""
        print("🧹 Cleaning up Session Manager...")
        if self._cleanup_task:
            self._cleanup_task.cancel()
            try:
                await self._cleanup_task
            except asyncio.CancelledError:
                pass
        print("✅ Session Manager cleaned up")

    async def _cleanup_loop(self):
        """Periodically clean up expired sessions."""
        while True:
            try:
                await asyncio.sleep(60)  # Check every minute
                await self._cleanup_expired()
            except asyncio.CancelledError:
                break
            except Exception as e:
                print(f"Error in cleanup loop: {e}")

    async def _cleanup_expired(self):
        """Remove expired sessions."""
        async with self._lock:
            now = datetime.utcnow()
            expired = [
                sid
                for sid, session in self.sessions.items()
                if now - session.last_activity > self.session_timeout
            ]

            for sid in expired:
                self.sessions[sid].status = "expired"
                del self.sessions[sid]

            if expired:
                print(f"🗑️  Cleaned up {len(expired)} expired sessions")

    async def create_session(self, request: SessionCreate) -> SessionInfo:
        """Create a new session."""
        session_id = f"sess-{uuid.uuid4().hex}"

        # Create initial emotion state
        initial_emotion = EmotionState(
            primary=request.initial_emotion or EmotionType.PLAYFUL,
            intensity=0.7,
            valence=0.6,
            arousal=0.5,
        )

        # Create initial relationship state
        relationship = RelationshipState()

        # Create session
        session = Session(
            session_id=session_id,
            user_id=request.user_id,
            created_at=datetime.utcnow(),
            last_activity=datetime.utcnow(),
            message_count=0,
            current_emotion=initial_emotion,
            relationship_state=relationship,
            metadata=request.metadata or {},
        )

        async with self._lock:
            self.sessions[session_id] = session

        print(f"✨ Created new session: {session_id}")
        return session.to_info()

    async def get_session(self, session_id: str) -> Optional[SessionInfo]:
        """Get session info by ID."""
        session = await self.get_session_internal(session_id)
        if session:
            return session.to_info()
        return None

    async def get_session_internal(self, session_id: str) -> Optional[Session]:
        """Get internal session object."""
        async with self._lock:
            session = self.sessions.get(session_id)
            if session:
                # Update last activity
                session.last_activity = datetime.utcnow()
            return session

    async def delete_session(self, session_id: str) -> bool:
        """Delete a session."""
        async with self._lock:
            if session_id in self.sessions:
                del self.sessions[session_id]
                print(f"🗑️  Deleted session: {session_id}")
                return True
            return False

    async def list_sessions(
        self,
        user_id: Optional[str] = None,
        status: Optional[str] = None,
    ) -> list[SessionInfo]:
        """List all sessions, optionally filtered."""
        async with self._lock:
            sessions = list(self.sessions.values())

        # Apply filters
        if user_id:
            sessions = [s for s in sessions if s.user_id == user_id]
        if status:
            sessions = [s for s in sessions if s.status == status]

        return [s.to_info() for s in sessions]

    async def increment_message_count(self, session_id: str) -> int:
        """Increment message count and return new count."""
        async with self._lock:
            session = self.sessions.get(session_id)
            if session:
                session.message_count += 1
                session.last_activity = datetime.utcnow()
                return session.message_count
            return 0

    async def update_emotion(
        self,
        session_id: str,
        emotion: EmotionState,
    ) -> bool:
        """Update the current emotion state."""
        async with self._lock:
            session = self.sessions.get(session_id)
            if session:
                session.current_emotion = emotion
                session.last_activity = datetime.utcnow()
                return True
            return False

    async def update_relationship(
        self,
        session_id: str,
        relationship: RelationshipState,
    ) -> bool:
        """Update the relationship state."""
        async with self._lock:
            session = self.sessions.get(session_id)
            if session:
                session.relationship_state = relationship
                session.last_activity = datetime.utcnow()
                return True
            return False

    async def increment_familiarity(
        self,
        session_id: str,
        amount: float = 0.01,
    ) -> bool:
        """Increment familiarity level."""
        async with self._lock:
            session = self.sessions.get(session_id)
            if session:
                session.relationship_state.familiarity = min(
                    1.0, session.relationship_state.familiarity + amount
                )
                session.last_activity = datetime.utcnow()
                return True
            return False

    def get_active_session_count(self) -> int:
        """Get count of active sessions."""
        return len([s for s in self.sessions.values() if s.status == "active"])

    def get_total_session_count(self) -> int:
        """Get total session count."""
        return len(self.sessions)
