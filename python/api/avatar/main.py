"""
Avatar API - FastAPI Application

Main entry point for the Live2D Avatar API server.
"""

import os
import sys
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

# Add parent directories to path for imports
sys.path.insert(
    0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
)

from .router import router as avatar_router
from .websocket import websocket_router
from .services.session_manager import SessionManager


# Global session manager instance
session_manager: SessionManager = None


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    """Application lifespan manager."""
    global session_manager

    # Startup
    print("🎭 Starting Avatar API server...")
    session_manager = SessionManager()
    await session_manager.initialize()
    app.state.session_manager = session_manager

    print("✅ Avatar API server ready!")
    print("📚 API docs available at /docs")

    yield

    # Shutdown
    print("🛑 Shutting down Avatar API server...")
    await session_manager.cleanup()
    print("👋 Avatar API server stopped")


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""

    app = FastAPI(
        title="Agent-Zero Avatar API",
        description="""
# Live2D Avatar API for Agent-Zero

This API provides endpoints for controlling the Live2D avatar of Agent-Toga,
including chat interactions, emotion management, animations, and voice synthesis.

## Features

- **Session Management**: Create and manage avatar sessions
- **Chat**: Send messages and receive personality-driven responses
- **Emotions**: Query and trigger emotional states
- **Animations**: Control avatar animations and expressions
- **Voice**: Text-to-speech with lip sync support
- **WebSocket**: Real-time bidirectional communication

## Authentication

All endpoints require an API key passed via the `X-API-Key` header.

## Rate Limits

- Chat endpoints: 60 requests/minute
- Voice synthesis: 10 requests/minute
- Other endpoints: 100 requests/minute
        """,
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
        lifespan=lifespan,
    )

    # Configure CORS
    origins = [
        "http://localhost:3000",
        "http://localhost:5173",  # Vite dev server
        "http://localhost:8080",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:8080",
    ]

    # Add production origins from environment
    if os.getenv("CORS_ORIGINS"):
        origins.extend(os.getenv("CORS_ORIGINS").split(","))

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include routers
    app.include_router(avatar_router, prefix="/api/avatar", tags=["Avatar"])
    app.include_router(websocket_router, prefix="/api/avatar", tags=["WebSocket"])

    # Mount static files for audio
    audio_dir = os.path.join(os.path.dirname(__file__), "audio_cache")
    os.makedirs(audio_dir, exist_ok=True)
    app.mount("/api/avatar/audio", StaticFiles(directory=audio_dir), name="audio")

    return app


# Create the application instance
app = create_app()


# Health check at root
@app.get("/", tags=["Root"])
async def root():
    """Root endpoint with API information."""
    return {
        "name": "Agent-Zero Avatar API",
        "version": "1.0.0",
        "status": "online",
        "docs": "/docs",
        "health": "/api/avatar/health",
    }


if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("AVATAR_API_PORT", "8000"))
    host = os.getenv("AVATAR_API_HOST", "0.0.0.0")

    uvicorn.run(
        "python.api.avatar.main:app",
        host=host,
        port=port,
        reload=True,
        log_level="info",
    )
