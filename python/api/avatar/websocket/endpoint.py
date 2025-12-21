"""
WebSocket Endpoint

FastAPI WebSocket endpoint for avatar real-time communication.
"""

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, Query
from typing import Optional

from .handler import (
    connection_manager,
    AvatarWebSocketHandler,
    WebSocketMessage,
    MessageType,
)
from ..services.session_manager import SessionManager
from ..dependencies import get_session_manager


router = APIRouter()


@router.websocket("/ws/{session_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    session_id: str,
    api_key: Optional[str] = Query(None),
):
    """
    WebSocket endpoint for real-time avatar communication.

    Connect to this endpoint to receive streaming responses,
    emotion updates, and animation triggers in real-time.

    ## Connection

    ```
    ws://host/api/avatar/ws/{session_id}?api_key={your_api_key}
    ```

    ## Message Format

    All messages are JSON with the following structure:

    ```json
    {
        "type": "message_type",
        "data": { ... },
        "session_id": "sess-xxx",
        "timestamp": "2025-12-21T00:00:00Z"
    }
    ```

    ## Client -> Server Messages

    - `ping`: Keep-alive ping
    - `chat`: Send a chat message
    - `emotion_trigger`: Trigger an emotion
    - `animation_trigger`: Trigger an animation

    ## Server -> Client Messages

    - `connected`: Connection confirmed
    - `pong`: Response to ping
    - `chat_token`: Streaming chat token
    - `chat_response`: Complete chat response
    - `emotion_update`: Emotion state changed
    - `animation_play`: Animation to play
    - `heartbeat`: Keep-alive heartbeat
    - `error`: Error message
    """
    # Get session manager from app state
    session_manager = websocket.app.state.session_manager

    # Validate session exists
    session = await session_manager.get_session(session_id)
    if not session:
        await websocket.close(code=4004, reason="Session not found")
        return

    # Validate API key (optional in dev mode)
    import os

    if not os.getenv("AVATAR_API_DEV_MODE", "").lower() == "true":
        if not api_key:
            await websocket.close(code=4001, reason="API key required")
            return

        valid_keys = os.getenv("AVATAR_API_KEYS", "").split(",")
        if api_key not in valid_keys:
            await websocket.close(code=4003, reason="Invalid API key")
            return

    # Accept connection
    connected = await connection_manager.connect(websocket, session_id)
    if not connected:
        return

    # Create handler
    handler = AvatarWebSocketHandler(
        websocket=websocket,
        session_id=session_id,
        session_manager=session_manager,
    )

    # Start heartbeat
    await handler.start_heartbeat()

    try:
        while True:
            # Receive message
            data = await websocket.receive_text()

            try:
                message = WebSocketMessage.from_json(data)
                message.session_id = session_id
                await handler.handle_message(message)
            except Exception as e:
                await connection_manager.send_personal(
                    websocket,
                    WebSocketMessage(
                        type=MessageType.ERROR,
                        data={"error": str(e)},
                        session_id=session_id,
                    ),
                )

    except WebSocketDisconnect:
        pass
    finally:
        await handler.stop_heartbeat()
        await connection_manager.disconnect(websocket)


@router.get("/ws/stats")
async def websocket_stats():
    """Get WebSocket connection statistics."""
    return {
        "total_connections": connection_manager.get_connection_count(),
        "sessions_with_connections": len(connection_manager.active_connections),
    }
