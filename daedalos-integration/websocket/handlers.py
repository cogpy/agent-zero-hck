"""
WebSocket Message Handlers

Defines handlers for different types of WebSocket messages.
"""

from typing import Dict, Any, Callable
from fastapi import WebSocket
import logging

from .manager import WebSocketManager
from ..filesystem import FileSystemManager

logger = logging.getLogger(__name__)

# Global manager instance
ws_manager = WebSocketManager()
fs_manager = FileSystemManager()


async def handle_message(agent_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Handle agent message.
    
    Args:
        agent_id: Agent identifier
        data: Message data
        
    Returns:
        Response data
    """
    content = data.get("content", "")
    logger.info(f"Agent {agent_id} message: {content}")
    
    return {
        "type": "message_response",
        "agent_id": agent_id,
        "status": "received",
        "content": f"Message received: {content}",
    }


async def handle_status(agent_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Handle agent status request.
    
    Args:
        agent_id: Agent identifier
        data: Request data
        
    Returns:
        Status data
    """
    storage_info = fs_manager.get_storage_info()
    
    return {
        "type": "status_response",
        "agent_id": agent_id,
        "status": "active",
        "storage": storage_info,
    }


async def handle_file_operation(agent_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Handle file operation.
    
    Args:
        agent_id: Agent identifier
        data: Operation data
        
    Returns:
        Operation result
    """
    operation = data.get("operation")
    path = data.get("path")
    
    try:
        if operation == "read":
            content = fs_manager.adapter.read_file(path)
            return {
                "type": "file_response",
                "operation": "read",
                "path": path,
                "content": content,
                "status": "success",
            }
        
        elif operation == "write":
            content = data.get("content", "")
            fs_manager.adapter.write_file(path, content)
            return {
                "type": "file_response",
                "operation": "write",
                "path": path,
                "status": "success",
            }
        
        elif operation == "list":
            files = fs_manager.adapter.list_directory(path)
            return {
                "type": "file_response",
                "operation": "list",
                "path": path,
                "files": files,
                "status": "success",
            }
        
        else:
            return {
                "type": "error",
                "error": f"Unknown operation: {operation}",
            }
    
    except Exception as e:
        logger.error(f"File operation error: {e}")
        return {
            "type": "error",
            "error": str(e),
        }


async def handle_memory_operation(agent_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Handle memory operation.
    
    Args:
        agent_id: Agent identifier
        data: Operation data
        
    Returns:
        Operation result
    """
    operation = data.get("operation")
    
    try:
        if operation == "save":
            memory_data = data.get("data", {})
            fs_manager.save_memory(memory_data)
            return {
                "type": "memory_response",
                "operation": "save",
                "status": "success",
            }
        
        elif operation == "load":
            memory_data = fs_manager.load_memory()
            return {
                "type": "memory_response",
                "operation": "load",
                "data": memory_data,
                "status": "success",
            }
        
        else:
            return {
                "type": "error",
                "error": f"Unknown operation: {operation}",
            }
    
    except Exception as e:
        logger.error(f"Memory operation error: {e}")
        return {
            "type": "error",
            "error": str(e),
        }


def create_websocket_handler(agent_id: str) -> Callable:
    """
    Create WebSocket handler for an agent.
    
    Args:
        agent_id: Agent identifier
        
    Returns:
        Handler function
    """
    async def handler(websocket: WebSocket) -> None:
        """
        Handle WebSocket connection.
        
        Args:
            websocket: WebSocket connection
        """
        await ws_manager.connect(agent_id, websocket)
        
        try:
            while True:
                # Receive message
                data = await websocket.receive_json()
                
                # Route to appropriate handler
                response = await ws_manager.handle_message(agent_id, data)
                
                # Send response
                await ws_manager.send_personal(agent_id, websocket, response)
        
        except Exception as e:
            logger.error(f"WebSocket error: {e}")
        
        finally:
            await ws_manager.disconnect(agent_id, websocket)
    
    return handler


def register_default_handlers() -> None:
    """Register default message handlers."""
    ws_manager.register_handler("message", handle_message)
    ws_manager.register_handler("status", handle_status)
    ws_manager.register_handler("file", handle_file_operation)
    ws_manager.register_handler("memory", handle_memory_operation)
    logger.info("Default WebSocket handlers registered")


def get_manager() -> WebSocketManager:
    """
    Get WebSocket manager instance.
    
    Returns:
        WebSocket manager
    """
    return ws_manager
