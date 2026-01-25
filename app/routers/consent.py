"""
Consent management router for S.O.F.I.E. Backend.
Implements regulation-before-reasoning by managing user consent.
"""

from fastapi import APIRouter, HTTPException, status
from app.models.schemas import ConsentRequest, ConsentResponse, ConsentType
from app.services import consent_manager
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/consent", tags=["consent"])


@router.post("/grant", response_model=ConsentResponse)
async def grant_consent(request: ConsentRequest) -> ConsentResponse:
    """
    Grant consent for a specific operation.
    
    This endpoint allows users to explicitly grant consent before any
    computation or data processing occurs (consent-before-computation).
    
    Args:
        request: ConsentRequest with user_id, consent_type, and purpose
        
    Returns:
        ConsentResponse with granted status and expiry time
    """
    logger.info(f"Consent grant request: user={request.user_id}, type={request.consent_type}")
    
    try:
        response = consent_manager.grant_consent(
            user_id=request.user_id,
            consent_type=request.consent_type,
            purpose=request.purpose
        )
        return response
        
    except Exception as e:
        logger.error(f"Failed to grant consent: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to grant consent"
        )


@router.get("/check/{user_id}/{consent_type}", response_model=ConsentResponse)
async def check_consent(user_id: str, consent_type: ConsentType) -> ConsentResponse:
    """
    Check consent status for a user and consent type.
    
    Args:
        user_id: Unique user identifier
        consent_type: Type of consent to check
        
    Returns:
        ConsentResponse with current consent status
    """
    logger.info(f"Consent check request: user={user_id}, type={consent_type}")
    
    try:
        response = consent_manager.check_consent(
            user_id=user_id,
            consent_type=consent_type
        )
        return response
        
    except Exception as e:
        logger.error(f"Failed to check consent: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to check consent"
        )


@router.delete("/revoke/{user_id}/{consent_type}", response_model=ConsentResponse)
async def revoke_consent(user_id: str, consent_type: ConsentType) -> ConsentResponse:
    """
    Revoke consent for a user and consent type.
    
    Users can revoke consent at any time, immediately stopping
    any further computation or data processing.
    
    Args:
        user_id: Unique user identifier
        consent_type: Type of consent to revoke
        
    Returns:
        ConsentResponse with revoked status
    """
    logger.info(f"Consent revoke request: user={user_id}, type={consent_type}")
    
    try:
        response = consent_manager.revoke_consent(
            user_id=user_id,
            consent_type=consent_type
        )
        return response
        
    except Exception as e:
        logger.error(f"Failed to revoke consent: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to revoke consent"
        )
