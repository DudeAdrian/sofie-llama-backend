"""
Wellness guidance router for S.O.F.I.E. Backend.
Provides LLaMA-powered wellness guidance with strict consent enforcement.
"""

from fastapi import APIRouter, HTTPException, status
from app.models.schemas import WellnessRequest, WellnessResponse, ConsentType
from app.services import consent_manager, llama_service
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/wellness", tags=["wellness"])


@router.post("/guidance", response_model=WellnessResponse)
async def get_wellness_guidance(request: WellnessRequest) -> WellnessResponse:
    """
    Get context-aware wellness guidance from LLaMA.
    
    CRITICAL: This endpoint enforces consent-before-computation.
    Users must grant wellness_guidance consent before receiving guidance.
    
    Args:
        request: WellnessRequest with user_id, query, and optional context
        
    Returns:
        WellnessResponse with AI-generated guidance
        
    Raises:
        HTTPException 403: If consent is not granted or has expired
        HTTPException 500: If guidance generation fails
    """
    logger.info(f"Wellness guidance request from user={request.user_id}")
    
    # REGULATION BEFORE REASONING: Verify consent first
    consent_valid = consent_manager.verify_or_deny(
        user_id=request.user_id,
        consent_type=ConsentType.WELLNESS_GUIDANCE
    )
    
    if not consent_valid:
        logger.error(
            f"CONSENT DENIED: Wellness guidance blocked for user={request.user_id}"
        )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=(
                "Consent required. Please grant 'wellness_guidance' consent "
                "before requesting wellness guidance. "
                "Use POST /api/v1/consent/grant to provide consent."
            )
        )
    
    # Consent verified - proceed with computation
    logger.info(f"Consent verified for user={request.user_id}. Generating guidance...")
    
    try:
        # Generate wellness guidance using LLaMA
        guidance = llama_service.generate_wellness_guidance(
            query=request.query,
            context=request.context
        )
        
        response = WellnessResponse(
            guidance=guidance,
            context_used=request.context is not None,
            consent_verified=True,
            timestamp=datetime.utcnow()
        )
        
        logger.info(
            f"Wellness guidance generated successfully for user={request.user_id}, "
            f"length={len(guidance)} chars"
        )
        
        return response
        
    except Exception as e:
        logger.error(f"Failed to generate wellness guidance: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate wellness guidance"
        )
