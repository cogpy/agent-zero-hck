"""
Main Entry Point for Agent Zero daedalOS Integration API

Starts the FastAPI server with WebSocket support.
"""

import uvicorn
import logging
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware

from api.server import create_app
from websocket.handlers import register_default_handlers, get_manager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_application() -> FastAPI:
    """
    Create and configure the application.
    
    Returns:
        Configured FastAPI application
    """
    app = create_app()
    
    # Register default WebSocket handlers
    register_default_handlers()
    
    # Add WebSocket endpoint
    ws_manager = get_manager()
    
    @app.websocket("/ws/agent/{agent_id}")
    async def websocket_endpoint(websocket: WebSocket, agent_id: str):
        """WebSocket endpoint for agent communication."""
        await ws_manager.connect(agent_id, websocket)
        
        try:
            while True:
                data = await websocket.receive_json()
                response = await ws_manager.handle_message(agent_id, data)
                await ws_manager.send_personal(agent_id, websocket, response)
        except Exception as e:
            logger.error(f"WebSocket error: {e}")
        finally:
            await ws_manager.disconnect(agent_id, websocket)
    
    # Add management endpoints
    @app.get("/agents")
    async def get_active_agents():
        """Get list of active agents."""
        agents = ws_manager.get_active_agents()
        return {
            "agents": agents,
            "count": len(agents),
        }
    
    @app.get("/agents/{agent_id}/connections")
    async def get_agent_connections(agent_id: str):
        """Get connection count for an agent."""
        count = ws_manager.get_connection_count(agent_id)
        return {
            "agent_id": agent_id,
            "connections": count,
        }
    
    return app


def main():
    """Main entry point."""
    app = create_application()
    
    logger.info("Starting Agent Zero daedalOS Integration API")
    logger.info("Server running on http://0.0.0.0:8000")
    logger.info("WebSocket endpoint: ws://0.0.0.0:8000/ws/agent/{agent_id}")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info",
    )


if __name__ == "__main__":
    main()
