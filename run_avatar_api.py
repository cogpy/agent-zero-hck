#!/usr/bin/env python3.11
"""
Avatar API Server Runner

Starts the Avatar API server for Agent-Toga Live2D avatar.
"""

import os
import sys

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    import uvicorn
    from python.api.avatar.main import app

    port = int(os.getenv("AVATAR_API_PORT", "8000"))
    host = os.getenv("AVATAR_API_HOST", "0.0.0.0")

    print(f"🎭 Starting Avatar API server on {host}:{port}")
    print(f"📚 API docs will be available at http://{host}:{port}/docs")

    uvicorn.run(
        app,
        host=host,
        port=port,
        log_level="info",
    )
