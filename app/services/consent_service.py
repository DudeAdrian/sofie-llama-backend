"""
Consent Management Service - Regulation Before Reasoning.
Enforces consent-before-computation at every layer.
"""

from datetime import datetime, timedelta
from typing import Dict, Optional
from app.models.schemas import ConsentType, ConsentStatus, ConsentResponse
from app.config import settings
import logging

logger = logging.getLogger(__name__)


class ConsentManager:
    """
    Manages user consent with strict enforcement.
    Implements 'consent-before-computation' principle.
    """
    
    def __init__(self):
        """
        Initialize consent storage (in-memory for demo, use DB in production).
        
        WARNING: In-memory storage means all consent data is lost on restart.
        For production, replace with a persistent database (PostgreSQL, Redis, etc.)
        """
        self._consents: Dict[str, Dict[ConsentType, ConsentResponse]] = {}
        logger.info("ConsentManager initialized with strict enforcement enabled")
        logger.warning(
            "Using in-memory consent storage. Consent data will be lost on restart. "
            "For production, implement persistent storage."
        )
    
    def grant_consent(
        self, 
        user_id: str, 
        consent_type: ConsentType,
        purpose: str
    ) -> ConsentResponse:
        """
        Grant consent for a user and consent type.
        
        Args:
            user_id: Unique user identifier
            consent_type: Type of consent being granted
            purpose: Purpose description for transparency
            
        Returns:
            ConsentResponse with granted status and expiry
        """
        now = datetime.utcnow()
        expires_at = now + timedelta(hours=settings.consent_expiry_hours)
        
        consent_response = ConsentResponse(
            user_id=user_id,
            consent_type=consent_type,
            status=ConsentStatus.GRANTED,
            granted_at=now,
            expires_at=expires_at
        )
        
        if user_id not in self._consents:
            self._consents[user_id] = {}
        
        self._consents[user_id][consent_type] = consent_response
        
        logger.info(
            f"Consent granted: user={user_id}, type={consent_type}, "
            f"expires={expires_at}, purpose={purpose}"
        )
        
        return consent_response
    
    def check_consent(
        self, 
        user_id: str, 
        consent_type: ConsentType
    ) -> ConsentResponse:
        """
        Check if user has valid consent for a specific type.
        CRITICAL: This must be called before ANY computation.
        
        Args:
            user_id: Unique user identifier
            consent_type: Type of consent to check
            
        Returns:
            ConsentResponse with current status
        """
        # User not found
        if user_id not in self._consents:
            logger.warning(f"Consent check failed: user={user_id} not found")
            return ConsentResponse(
                user_id=user_id,
                consent_type=consent_type,
                status=ConsentStatus.DENIED
            )
        
        # Consent type not granted
        if consent_type not in self._consents[user_id]:
            logger.warning(
                f"Consent check failed: user={user_id}, type={consent_type} not granted"
            )
            return ConsentResponse(
                user_id=user_id,
                consent_type=consent_type,
                status=ConsentStatus.DENIED
            )
        
        consent = self._consents[user_id][consent_type]
        
        # Check if expired
        if consent.expires_at and datetime.utcnow() > consent.expires_at:
            logger.warning(
                f"Consent expired: user={user_id}, type={consent_type}, "
                f"expired_at={consent.expires_at}"
            )
            consent.status = ConsentStatus.EXPIRED
        
        logger.info(f"Consent checked: user={user_id}, type={consent_type}, status={consent.status}")
        return consent
    
    def revoke_consent(
        self, 
        user_id: str, 
        consent_type: ConsentType
    ) -> ConsentResponse:
        """
        Revoke consent for a user and consent type.
        
        Args:
            user_id: Unique user identifier
            consent_type: Type of consent to revoke
            
        Returns:
            ConsentResponse with revoked status
        """
        if user_id in self._consents and consent_type in self._consents[user_id]:
            consent = self._consents[user_id][consent_type]
            consent.status = ConsentStatus.REVOKED
            logger.info(f"Consent revoked: user={user_id}, type={consent_type}")
            return consent
        
        logger.warning(f"Consent revoke failed: user={user_id}, type={consent_type} not found")
        return ConsentResponse(
            user_id=user_id,
            consent_type=consent_type,
            status=ConsentStatus.DENIED
        )
    
    def verify_or_deny(
        self, 
        user_id: str, 
        consent_type: ConsentType
    ) -> bool:
        """
        Strict consent verification - returns True only if consent is granted and valid.
        REGULATION BEFORE REASONING: Call this before any AI computation.
        
        Args:
            user_id: Unique user identifier
            consent_type: Type of consent required
            
        Returns:
            True if consent is valid, False otherwise
        """
        if not settings.require_consent:
            logger.warning("Consent requirement disabled - this should only be for testing")
            return True
        
        consent = self.check_consent(user_id, consent_type)
        is_valid = consent.status == ConsentStatus.GRANTED
        
        if not is_valid:
            logger.error(
                f"CONSENT DENIED: Computation blocked for user={user_id}, "
                f"type={consent_type}, status={consent.status}"
            )
        
        return is_valid


# Global consent manager instance
consent_manager = ConsentManager()
