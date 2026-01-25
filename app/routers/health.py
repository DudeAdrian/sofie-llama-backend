"""
Health check router for S.O.F.I.E. Backend.
"""

from fastapi import APIRouter
from app.models.schemas import HealthCheckResponse
from app.services import llama_service
from app.config import settings

router = APIRouter(prefix="/api/v1", tags=["health"])


@router.get("/health", response_model=HealthCheckResponse)
async def health_check() -> HealthCheckResponse:
    """
    Health check endpoint to verify service status.
    
    Returns:
        HealthCheckResponse with service status and capabilities
    """
    return HealthCheckResponse(
        status="healthy",
        version="1.0.0",
        llama_available=llama_service.is_available(),
        consent_enforcement=settings.require_consent
    )
