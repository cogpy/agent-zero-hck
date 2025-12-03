"""
FastAPI Server for daedalOS Integration

Provides REST API for Agent Zero operations.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging

logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    """
    Create and configure FastAPI application.
    
    Returns:
        Configured FastAPI application
    """
    app = FastAPI(
        title="Agent Zero daedalOS API",
        description="API for Agent Zero integration with daedalOS",
        version="1.0.0",
    )
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Health check endpoint
    @app.get("/health")
    async def health_check():
        """Health check endpoint."""
        return {
            "status": "healthy",
            "service": "Agent Zero daedalOS API",
        }
    
    # Error handlers
    @app.exception_handler(Exception)
    async def general_exception_handler(request, exc):
        """Handle general exceptions."""
        logger.error(f"Unhandled exception: {exc}")
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal server error"},
        )
    
    return app


def get_app() -> FastAPI:
    """
    Get or create FastAPI application.
    
    Returns:
        FastAPI application instance
    """
    app = create_app()
    
    # Import and include routers
    from .routes import router
    app.include_router(router, prefix="/api", tags=["agent"])
    
    return app
