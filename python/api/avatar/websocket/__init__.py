"""
Avatar WebSocket Package

Real-time WebSocket communication for avatar interactions.
"""

from .handler import (
    connection_manager,
    ConnectionManager,
    AvatarWebSocketHandler,
    WebSocketMessage,
    MessageType,
)
from .endpoint import router as websocket_router

__all__ = [
    "connection_manager",
    "ConnectionManager",
    "AvatarWebSocketHandler",
    "WebSocketMessage",
    "MessageType",
    "websocket_router",
]
