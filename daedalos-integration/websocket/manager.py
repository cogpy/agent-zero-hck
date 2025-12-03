"""
WebSocket Manager for Real-time Communication

Manages WebSocket connections and message routing.
"""

from typing import Dict, Set, Callable, Any
from fastapi import WebSocket
import logging
import json

logger = logging.getLogger(__name__)


class WebSocketManager:
    """
    Manages WebSocket connections for real-time communication.
    """
    
    def __init__(self):
        """Initialize WebSocket manager."""
        self.active_connections: Dict[str, Set[WebSocket]] = {}
        self.message_handlers: Dict[str, Callable] = {}
    
    async def connect(self, agent_id: str, websocket: WebSocket) -> None:
        """
        Connect a WebSocket client.
        
        Args:
            agent_id: Agent identifier
            websocket: WebSocket connection
        """
        await websocket.accept()
        
        if agent_id not in self.active_connections:
            self.active_connections[agent_id] = set()
        
        self.active_connections[agent_id].add(websocket)
        logger.info(f"Client connected to agent {agent_id}")
    
    async def disconnect(self, agent_id: str, websocket: WebSocket) -> None:
        """
        Disconnect a WebSocket client.
        
        Args:
            agent_id: Agent identifier
            websocket: WebSocket connection
        """
        if agent_id in self.active_connections:
            self.active_connections[agent_id].discard(websocket)
            
            if not self.active_connections[agent_id]:
                del self.active_connections[agent_id]
        
        logger.info(f"Client disconnected from agent {agent_id}")
    
    async def broadcast(self, agent_id: str, message: Dict[str, Any]) -> None:
        """
        Broadcast message to all clients of an agent.
        
        Args:
            agent_id: Agent identifier
            message: Message to broadcast
        """
        if agent_id not in self.active_connections:
            return
        
        disconnected = set()
        
        for websocket in self.active_connections[agent_id]:
            try:
                await websocket.send_json(message)
            except Exception as e:
                logger.error(f"Error sending message: {e}")
                disconnected.add(websocket)
        
        # Clean up disconnected clients
        for websocket in disconnected:
            await self.disconnect(agent_id, websocket)
    
    async def send_personal(
        self,
        agent_id: str,
        websocket: WebSocket,
        message: Dict[str, Any]
    ) -> None:
        """
        Send message to specific client.
        
        Args:
            agent_id: Agent identifier
            websocket: WebSocket connection
            message: Message to send
        """
        try:
            await websocket.send_json(message)
        except Exception as e:
            logger.error(f"Error sending personal message: {e}")
            await self.disconnect(agent_id, websocket)
    
    def register_handler(self, message_type: str, handler: Callable) -> None:
        """
        Register message handler.
        
        Args:
            message_type: Type of message to handle
            handler: Handler function
        """
        self.message_handlers[message_type] = handler
        logger.info(f"Registered handler for message type: {message_type}")
    
    async def handle_message(
        self,
        agent_id: str,
        message_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Handle incoming message.
        
        Args:
            agent_id: Agent identifier
            message_data: Message data
            
        Returns:
            Response data
        """
        message_type = message_data.get("type", "unknown")
        handler = self.message_handlers.get(message_type)
        
        if handler:
            try:
                response = await handler(agent_id, message_data)
                return response
            except Exception as e:
                logger.error(f"Error handling message: {e}")
                return {
                    "type": "error",
                    "error": str(e),
                }
        else:
            logger.warning(f"No handler for message type: {message_type}")
            return {
                "type": "error",
                "error": f"Unknown message type: {message_type}",
            }
    
    def get_active_agents(self) -> list:
        """
        Get list of active agents.
        
        Returns:
            List of agent IDs with active connections
        """
        return list(self.active_connections.keys())
    
    def get_connection_count(self, agent_id: str) -> int:
        """
        Get number of active connections for an agent.
        
        Args:
            agent_id: Agent identifier
            
        Returns:
            Number of connections
        """
        return len(self.active_connections.get(agent_id, set()))
