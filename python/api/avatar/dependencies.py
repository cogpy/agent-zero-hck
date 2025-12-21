"""
Avatar API Dependencies

Shared dependencies for authentication, session management, and rate limiting.
"""

import os
import time
from typing import Optional, Dict, Any
from collections import defaultdict
from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, Header, Request, status
from fastapi.security import APIKeyHeader

from .services.session_manager import SessionManager


# API Key authentication
API_KEY_HEADER = APIKeyHeader(name="X-API-Key", auto_error=False)


class RateLimiter:
    """Simple in-memory rate limiter."""

    def __init__(self):
        self.requests: Dict[str, list] = defaultdict(list)
        self.limits = {
            "chat": (60, 60),  # 60 requests per 60 seconds
            "voice": (10, 60),  # 10 requests per 60 seconds
            "default": (100, 60),  # 100 requests per 60 seconds
        }

    def check(self, key: str, endpoint_type: str = "default") -> bool:
        """Check if request is allowed."""
        now = time.time()
        limit, window = self.limits.get(endpoint_type, self.limits["default"])

        # Clean old requests
        self.requests[key] = [t for t in self.requests[key] if now - t < window]

        if len(self.requests[key]) >= limit:
            return False

        self.requests[key].append(now)
        return True

    def get_retry_after(self, key: str, endpoint_type: str = "default") -> int:
        """Get seconds until next request is allowed."""
        if not self.requests[key]:
            return 0

        _, window = self.limits.get(endpoint_type, self.limits["default"])
        oldest = min(self.requests[key])
        return max(0, int(window - (time.time() - oldest)))


# Global rate limiter instance
rate_limiter = RateLimiter()


async def get_api_key(
    api_key: Optional[str] = Depends(API_KEY_HEADER),
    authorization: Optional[str] = Header(None),
) -> str:
    """Validate API key from header."""

    # Check X-API-Key header first
    if api_key:
        if await validate_api_key(api_key):
            return api_key

    # Check Authorization: Bearer header
    if authorization and authorization.startswith("Bearer "):
        token = authorization[7:]
        if await validate_api_key(token):
            return token

    # Check environment for development mode
    if os.getenv("AVATAR_API_DEV_MODE", "").lower() == "true":
        return "dev-key"

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or missing API key",
        headers={"WWW-Authenticate": "ApiKey"},
    )


async def validate_api_key(api_key: str) -> bool:
    """Validate the provided API key."""

    # Check against configured API keys
    valid_keys = os.getenv("AVATAR_API_KEYS", "").split(",")
    if api_key in valid_keys:
        return True

    # Check against Agent-Zero API key
    agent_zero_key = os.getenv("AGENT_ZERO_API_KEY", "")
    if agent_zero_key and api_key == agent_zero_key:
        return True

    # Development mode allows any key
    if os.getenv("AVATAR_API_DEV_MODE", "").lower() == "true":
        return True

    return False


async def get_session_manager(request: Request) -> SessionManager:
    """Get the session manager from app state."""
    return request.app.state.session_manager


async def rate_limit_chat(
    request: Request,
    api_key: str = Depends(get_api_key),
):
    """Rate limit for chat endpoints."""
    if not rate_limiter.check(api_key, "chat"):
        retry_after = rate_limiter.get_retry_after(api_key, "chat")
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"Rate limit exceeded. Retry after {retry_after} seconds.",
            headers={"Retry-After": str(retry_after)},
        )


async def rate_limit_voice(
    request: Request,
    api_key: str = Depends(get_api_key),
):
    """Rate limit for voice synthesis endpoints."""
    if not rate_limiter.check(api_key, "voice"):
        retry_after = rate_limiter.get_retry_after(api_key, "voice")
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"Rate limit exceeded. Retry after {retry_after} seconds.",
            headers={"Retry-After": str(retry_after)},
        )


async def rate_limit_default(
    request: Request,
    api_key: str = Depends(get_api_key),
):
    """Default rate limit for other endpoints."""
    if not rate_limiter.check(api_key, "default"):
        retry_after = rate_limiter.get_retry_after(api_key, "default")
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"Rate limit exceeded. Retry after {retry_after} seconds.",
            headers={"Retry-After": str(retry_after)},
        )


class SessionDependency:
    """Dependency for validating and retrieving sessions."""

    def __init__(self, require_active: bool = True):
        self.require_active = require_active

    async def __call__(
        self,
        session_id: str,
        session_manager: SessionManager = Depends(get_session_manager),
    ):
        """Validate session and return session state."""
        session = await session_manager.get_session(session_id)

        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Session not found: {session_id}",
            )

        if self.require_active and session.status != "active":
            if session.status == "expired":
                raise HTTPException(
                    status_code=status.HTTP_410_GONE,
                    detail=f"Session expired: {session_id}",
                )
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Session not active: {session_id} (status: {session.status})",
                )

        return session


# Pre-configured dependency instances
require_session = SessionDependency(require_active=True)
get_session = SessionDependency(require_active=False)
