"""Session middleware."""

import uuid
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from sap_discovery.utils.logging import setup_logger

logger = setup_logger(__name__)

COOKIE_NAME = "session_id"
SESSION_EXPIRY = 86400  # 24 hours


class SessionMiddleware(BaseHTTPMiddleware):
    """Middleware to manage user sessions via cookies."""

    async def dispatch(self, request: Request, call_next):
        """Process request and ensure session exists.

        Args:
            request: Incoming HTTP request
            call_next: Next middleware or endpoint

        Returns:
            Response with session cookie set if needed
        """
        if request.url.path == "/health":
            return await call_next(request)
        session_id = request.cookies.get(COOKIE_NAME)

        if session_id:
            request.state.session_id = session_id
            logger.debug(f"Existing session: {session_id[:8]}...")
            return await call_next(request)

        # New session
        session_id = str(uuid.uuid4())
        request.state.session_id = session_id
        logger.info(f"New session created: {session_id[:8]}...")

        response = await call_next(request)
        response.set_cookie(
            key=COOKIE_NAME,
            value=session_id,
            httponly=True,
            secure=False,
            samesite="lax",
            max_age=SESSION_EXPIRY
        )
        return response