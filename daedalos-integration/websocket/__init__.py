"""
WebSocket Integration Module

Provides real-time communication between Agent Zero and daedalOS.
"""

from .manager import WebSocketManager
from .handlers import create_websocket_handler

__all__ = [
    'WebSocketManager',
    'create_websocket_handler',
]
