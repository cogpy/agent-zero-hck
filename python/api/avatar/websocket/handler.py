"""
WebSocket Handler for Avatar API

Real-time bidirectional communication for avatar interactions.
"""

import json
import asyncio
from datetime import datetime
from typing import Dict, Set, Optional, Any
from dataclasses import dataclass, field
from enum import Enum

from fastapi import WebSocket, WebSocketDisconnect


class MessageType(str, Enum):
    """WebSocket message types."""

    # Client -> Server
    CONNECT = "connect"
    DISCONNECT = "disconnect"
    CHAT = "chat"
    EMOTION_TRIGGER = "emotion_trigger"
    ANIMATION_TRIGGER = "animation_trigger"
    PING = "ping"

    # Server -> Client
    CONNECTED = "connected"
    CHAT_RESPONSE = "chat_response"
    CHAT_TOKEN = "chat_token"
    EMOTION_UPDATE = "emotion_update"
    ANIMATION_PLAY = "animation_play"
    ERROR = "error"
    PONG = "pong"
    HEARTBEAT = "heartbeat"


@dataclass
class WebSocketMessage:
    """A WebSocket message."""

    type: MessageType
    data: Dict[str, Any]
    timestamp: datetime = field(default_factory=datetime.utcnow)
    session_id: Optional[str] = None
    message_id: Optional[str] = None

    def to_json(self) -> str:
        """Convert to JSON string."""
        return json.dumps(
            {
                "type": self.type.value,
                "data": self.data,
                "timestamp": self.timestamp.isoformat(),
                "session_id": self.session_id,
                "message_id": self.message_id,
            }
        )

    @classmethod
    def from_json(cls, json_str: str) -> "WebSocketMessage":
        """Parse from JSON string."""
        data = json.loads(json_str)
        return cls(
            type=MessageType(data.get("type", "ping")),
            data=data.get("data", {}),
            session_id=data.get("session_id"),
            message_id=data.get("message_id"),
        )


class ConnectionManager:
    """Manages WebSocket connections."""

    def __init__(self):
        # session_id -> set of WebSocket connections
        self.active_connections: Dict[str, Set[WebSocket]] = {}
        # WebSocket -> session_id
        self.connection_sessions: Dict[WebSocket, str] = {}
        # Lock for thread safety
        self._lock = asyncio.Lock()

    async def connect(
        self,
        websocket: WebSocket,
        session_id: str,
    ) -> bool:
        """Accept a new WebSocket connection."""
        try:
            await websocket.accept()

            async with self._lock:
                if session_id not in self.active_connections:
                    self.active_connections[session_id] = set()

                self.active_connections[session_id].add(websocket)
                self.connection_sessions[websocket] = session_id

            # Send connected confirmation
            await self.send_personal(
                websocket,
                WebSocketMessage(
                    type=MessageType.CONNECTED,
                    data={
                        "session_id": session_id,
                        "message": "Connected to Avatar WebSocket",
                    },
                    session_id=session_id,
                ),
            )

            return True
        except Exception as e:
            print(f"WebSocket connection error: {e}")
            return False

    async def disconnect(self, websocket: WebSocket):
        """Remove a WebSocket connection."""
        async with self._lock:
            session_id = self.connection_sessions.pop(websocket, None)
            if session_id and session_id in self.active_connections:
                self.active_connections[session_id].discard(websocket)
                if not self.active_connections[session_id]:
                    del self.active_connections[session_id]

    async def send_personal(
        self,
        websocket: WebSocket,
        message: WebSocketMessage,
    ):
        """Send message to a specific connection."""
        try:
            await websocket.send_text(message.to_json())
        except Exception as e:
            print(f"Error sending to WebSocket: {e}")
            await self.disconnect(websocket)

    async def broadcast_to_session(
        self,
        session_id: str,
        message: WebSocketMessage,
    ):
        """Broadcast message to all connections in a session."""
        async with self._lock:
            connections = self.active_connections.get(session_id, set()).copy()

        for websocket in connections:
            await self.send_personal(websocket, message)

    async def broadcast_all(self, message: WebSocketMessage):
        """Broadcast message to all connections."""
        async with self._lock:
            all_connections = [
                ws
                for connections in self.active_connections.values()
                for ws in connections
            ]

        for websocket in all_connections:
            await self.send_personal(websocket, message)

    def get_connection_count(self, session_id: Optional[str] = None) -> int:
        """Get number of active connections."""
        if session_id:
            return len(self.active_connections.get(session_id, set()))
        return sum(len(conns) for conns in self.active_connections.values())


# Global connection manager
connection_manager = ConnectionManager()


class AvatarWebSocketHandler:
    """Handles WebSocket messages for avatar interactions."""

    def __init__(
        self,
        websocket: WebSocket,
        session_id: str,
        session_manager,
    ):
        self.websocket = websocket
        self.session_id = session_id
        self.session_manager = session_manager
        self._heartbeat_task: Optional[asyncio.Task] = None

    async def start_heartbeat(self, interval: int = 30):
        """Start heartbeat to keep connection alive."""

        async def heartbeat_loop():
            while True:
                try:
                    await asyncio.sleep(interval)
                    await connection_manager.send_personal(
                        self.websocket,
                        WebSocketMessage(
                            type=MessageType.HEARTBEAT,
                            data={"timestamp": datetime.utcnow().isoformat()},
                            session_id=self.session_id,
                        ),
                    )
                except asyncio.CancelledError:
                    break
                except Exception:
                    break

        self._heartbeat_task = asyncio.create_task(heartbeat_loop())

    async def stop_heartbeat(self):
        """Stop heartbeat task."""
        if self._heartbeat_task:
            self._heartbeat_task.cancel()
            try:
                await self._heartbeat_task
            except asyncio.CancelledError:
                pass

    async def handle_message(self, message: WebSocketMessage):
        """Handle incoming WebSocket message."""
        handlers = {
            MessageType.PING: self._handle_ping,
            MessageType.CHAT: self._handle_chat,
            MessageType.EMOTION_TRIGGER: self._handle_emotion_trigger,
            MessageType.ANIMATION_TRIGGER: self._handle_animation_trigger,
        }

        handler = handlers.get(message.type)
        if handler:
            await handler(message)
        else:
            await self._send_error(f"Unknown message type: {message.type}")

    async def _handle_ping(self, message: WebSocketMessage):
        """Handle ping message."""
        await connection_manager.send_personal(
            self.websocket,
            WebSocketMessage(
                type=MessageType.PONG,
                data={"echo": message.data},
                session_id=self.session_id,
            ),
        )

    async def _handle_chat(self, message: WebSocketMessage):
        """Handle chat message with streaming response."""
        user_message = message.data.get("message", "")

        if not user_message:
            await self._send_error("Empty message")
            return

        # Import NPU for response generation
        try:
            from python.helpers.cognitive.npu import initialize_npu

            npu = initialize_npu()
        except ImportError:
            npu = None

        # Generate response
        if npu and npu.is_available():
            # Stream tokens
            full_response = ""
            for token in npu.generate(user_message, max_tokens=500, stream=True):
                full_response += token
                await connection_manager.send_personal(
                    self.websocket,
                    WebSocketMessage(
                        type=MessageType.CHAT_TOKEN,
                        data={"token": token},
                        session_id=self.session_id,
                    ),
                )
                await asyncio.sleep(0.01)
        else:
            # Fallback response
            full_response = f"Hey hey! *bounces* You said '{user_message}'! That's fun~"

            # Simulate streaming
            for word in full_response.split():
                await connection_manager.send_personal(
                    self.websocket,
                    WebSocketMessage(
                        type=MessageType.CHAT_TOKEN,
                        data={"token": word + " "},
                        session_id=self.session_id,
                    ),
                )
                await asyncio.sleep(0.05)

        # Send complete response
        await connection_manager.send_personal(
            self.websocket,
            WebSocketMessage(
                type=MessageType.CHAT_RESPONSE,
                data={
                    "response": full_response,
                    "emotion": "excited",
                },
                session_id=self.session_id,
            ),
        )

        # Update session
        await self.session_manager.increment_message_count(self.session_id)

    async def _handle_emotion_trigger(self, message: WebSocketMessage):
        """Handle emotion trigger."""
        from ..models.emotion import EmotionState, EmotionType

        emotion_name = message.data.get("emotion", "neutral")
        intensity = message.data.get("intensity", 0.7)

        try:
            emotion_type = EmotionType(emotion_name)
        except ValueError:
            await self._send_error(f"Invalid emotion: {emotion_name}")
            return

        emotion = EmotionState(
            primary=emotion_type,
            intensity=intensity,
        )

        await self.session_manager.update_emotion(self.session_id, emotion)

        # Broadcast emotion update to all session connections
        await connection_manager.broadcast_to_session(
            self.session_id,
            WebSocketMessage(
                type=MessageType.EMOTION_UPDATE,
                data={
                    "emotion": emotion_type.value,
                    "intensity": intensity,
                    "parameters": emotion.to_live2d_params(),
                },
                session_id=self.session_id,
            ),
        )

    async def _handle_animation_trigger(self, message: WebSocketMessage):
        """Handle animation trigger."""
        animation_type = message.data.get("animation", "bounce")
        intensity = message.data.get("intensity", 0.5)
        duration_ms = message.data.get("duration_ms", 500)

        # Broadcast animation to all session connections
        await connection_manager.broadcast_to_session(
            self.session_id,
            WebSocketMessage(
                type=MessageType.ANIMATION_PLAY,
                data={
                    "animation": animation_type,
                    "intensity": intensity,
                    "duration_ms": duration_ms,
                },
                session_id=self.session_id,
            ),
        )

    async def _send_error(self, error_message: str):
        """Send error message."""
        await connection_manager.send_personal(
            self.websocket,
            WebSocketMessage(
                type=MessageType.ERROR,
                data={"error": error_message},
                session_id=self.session_id,
            ),
        )
