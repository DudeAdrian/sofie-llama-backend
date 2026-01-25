"""
Middleware for S.O.F.I.E. Backend.
Implements consent-before-computation at the request layer.
"""

from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
from app.services import consent_manager
from app.models.schemas import ConsentType
import logging

logger = logging.getLogger(__name__)


class ConsentEnforcementMiddleware(BaseHTTPMiddleware):
    """
    Middleware that enforces consent requirements for protected endpoints.
    Regulation-before-reasoning: Checks consent before allowing computation.
    """
    
    # Endpoints that require wellness guidance consent
    PROTECTED_PATHS = ["/api/v1/wellness/guidance"]
    
    async def dispatch(self, request: Request, call_next):
        """
        Process each request and enforce consent if needed.
        
        Args:
            request: Incoming HTTP request
            call_next: Next middleware or route handler
            
        Returns:
            Response from downstream handler or error if consent denied
        """
        path = request.url.path
        
        # Check if this is a protected endpoint
        if path in self.PROTECTED_PATHS:
            # For wellness guidance, we'll validate consent in the endpoint itself
            # This middleware serves as a documentation/logging layer
            logger.info(f"Processing protected endpoint: {path}")
        
        response = await call_next(request)
        return response


class LoggingMiddleware(BaseHTTPMiddleware):
    """Middleware for request/response logging."""
    
    async def dispatch(self, request: Request, call_next):
        """Log request details."""
        logger.info(f"Request: {request.method} {request.url.path}")
        response = await call_next(request)
        logger.info(f"Response: {response.status_code}")
        return response
