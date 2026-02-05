"""
Tiered Access Control System
Architect / Pro / Standard / Lite tiers
"""

from dataclasses import dataclass
from typing import List, Dict, Any, Optional, Set
from enum import Enum

class AccessTier(Enum):
    ARCHITECT = "architect"
    PRO = "pro"
    STANDARD = "standard"
    LITE = "lite"

@dataclass
class TierCapabilities:
    """Capabilities available at each tier"""
    name: str
    description: str
    model_access: str
    context_window: int
    response_time_ms: int
    quantum_features: List[str]
    jarvis_features: List[str]
    wellness_functions: int
    api_rate_limit: int  # requests per minute
    storage_gb: int
    support_level: str
    monthly_cost: float

class TieredAccessControl:
    """
    Four-tier access control system
    
    TIER COMPARISON:
    
    | Feature | Architect | Pro | Standard | Lite |
    |---------|-----------|-----|----------|------|
    | Model | LLaMA 70B Local | LLaMA 70B Cloud | LLaMA 8B Cloud | Lite Model |
    | Context | 128k | 128k | 32k | 8k |
    | Response | <200ms | <500ms | <1s | <2s |
    | Quantum | Full | Optimization | Metaphors | None |
    | JARVIS | Full | Voice + API | Voice only | Text only |
    | Functions | 100+ | 80+ | 50+ | 20+ |
    | Rate Limit | Unlimited | 1000/min | 100/min | 20/min |
    | Storage | Unlimited | 100GB | 10GB | 1GB |
    | Support | Dedicated | Priority | Standard | Community |
    | Cost | $0 (owner) | $99/mo | $29/mo | Free |
    """
    
    TIER_CONFIGS = {
        AccessTier.ARCHITECT: TierCapabilities(
            name="Architect",
            description="Full access for platform creator. Local deployment, quantum-ready, all features.",
            model_access="LLaMA 3.1 70B Local",
            context_window=128000,
            response_time_ms=200,
            quantum_features=[
                "literal_quantum_optimization",
                "metaphorical_quantum_guidance",
                "post_quantum_cryptography",
                "quantum_investment_positioning",
                "quantum_smart_contracts",
                "quantum_wellness_functions"
            ],
            jarvis_features=[
                "full_repo_command",
                "24_7_autonomous_operation",
                "voice_interface",
                "holographic_interface",
                "creative_partnership",
                "economic_command",
                "emergency_override"
            ],
            wellness_functions=100,
            api_rate_limit=0,  # Unlimited
            storage_gb=0,  # Unlimited
            support_level="dedicated_architect",
            monthly_cost=0.0
        ),
        
        AccessTier.PRO: TierCapabilities(
            name="Pro",
            description="Quantum optimization, cloud deployment, API access. For wellness professionals and power users.",
            model_access="LLaMA 3.1 70B Cloud",
            context_window=128000,
            response_time_ms=500,
            quantum_features=[
                "quantum_optimization_algorithms",
                "metaphorical_quantum_guidance",
                "post_quantum_encryption",
                "quantum_wellness_functions_limited"
            ],
            jarvis_features=[
                "voice_interface",
                "api_access",
                "repo_read_access",
                "creative_assistance",
                "economic_query"
            ],
            wellness_functions=80,
            api_rate_limit=1000,
            storage_gb=100,
            support_level="priority",
            monthly_cost=99.0
        ),
        
        AccessTier.STANDARD: TierCapabilities(
            name="Standard",
            description="Classical AI wellness guidance, token earning, voice interface. For everyday wellness.",
            model_access="LLaMA 3.1 8B Cloud",
            context_window=32000,
            response_time_ms=1000,
            quantum_features=[
                "metaphorical_quantum_guidance"
            ],
            jarvis_features=[
                "voice_interface",
                "wellness_query",
                "basic_creative"
            ],
            wellness_functions=50,
            api_rate_limit=100,
            storage_gb=10,
            support_level="standard",
            monthly_cost=29.0
        ),
        
        AccessTier.LITE: TierCapabilities(
            name="Lite",
            description="Simplified wearable-only interface. Safety-focused, essential wellness only.",
            model_access="Sofie-Lite Edge",
            context_window=8000,
            response_time_ms=2000,
            quantum_features=[],
            jarvis_features=[
                "text_interface_only",
                "basic_wellness_query"
            ],
            wellness_functions=20,
            api_rate_limit=20,
            storage_gb=1,
            support_level="community",
            monthly_cost=0.0
        )
    }
    
    def __init__(self):
        self.user_tiers: Dict[str, AccessTier] = {}
        self.upgrade_paths: Dict[AccessTier, AccessTier] = {
            AccessTier.LITE: AccessTier.STANDARD,
            AccessTier.STANDARD: AccessTier.PRO,
            AccessTier.PRO: AccessTier.ARCHITECT
        }
        
    def get_tier_config(self, tier: AccessTier) -> TierCapabilities:
        """Get configuration for a tier"""
        return self.TIER_CONFIGS[tier]
        
    def check_access(self, user_id: str, feature: str) -> Dict[str, Any]:
        """Check if user has access to a feature"""
        tier = self.user_tiers.get(user_id, AccessTier.LITE)
        config = self.TIER_CONFIGS[tier]
        
        # Check feature availability
        has_access = False
        if feature.startswith("quantum_"):
            has_access = feature in config.quantum_features
        elif feature.startswith("jarvis_"):
            has_access = feature in config.jarvis_features
        elif feature.startswith("wellness_"):
            has_access = True  # All tiers have some wellness
        elif feature == "api_access":
            has_access = tier in [AccessTier.ARCHITECT, AccessTier.PRO]
        elif feature == "repo_write":
            has_access = tier == AccessTier.ARCHITECT
            
        return {
            "user_id": user_id,
            "tier": tier.value,
            "feature": feature,
            "has_access": has_access,
            "upgrade_available": not has_access and tier != AccessTier.ARCHITECT,
            "upgrade_to": self.upgrade_paths.get(tier).value if not has_access and tier != AccessTier.ARCHITECT else None
        }
        
    def get_available_functions(self, user_id: str) -> List[str]:
        """Get list of wellness functions available to user"""
        tier = self.user_tiers.get(user_id, AccessTier.LITE)
        config = self.TIER_CONFIGS[tier]
        
        # Return function IDs based on tier
        all_functions = self._get_all_function_ids()
        
        if tier == AccessTier.ARCHITECT:
            return all_functions
        elif tier == AccessTier.PRO:
            return [f for f in all_functions if not f.startswith("arch_")]
        elif tier == AccessTier.STANDARD:
            return [f for f in all_functions if f.startswith(("bio_", "freq_", "men_", "cre_", "env_"))]
        else:  # LITE
            return [f for f in all_functions if f.startswith(("bio_", "men_"))][:20]
            
    def _get_all_function_ids(self) -> List[str]:
        """Get all function IDs"""
        # Would be populated from actual function library
        return [f"func_{i:03d}" for i in range(1, 101)]
        
    def upgrade_user(self, user_id: str, new_tier: AccessTier) -> Dict[str, Any]:
        """Upgrade user to new tier"""
        old_tier = self.user_tiers.get(user_id, AccessTier.LITE)
        
        if old_tier == AccessTier.ARCHITECT:
            return {"error": "Cannot upgrade from Architect tier"}
            
        if new_tier.value not in ["architect", "pro", "standard", "lite"]:
            return {"error": "Invalid tier"}
            
        # Check upgrade path validity
        current = old_tier
        while current != AccessTier.ARCHITECT:
            next_tier = self.upgrade_paths.get(current)
            if next_tier == new_tier:
                break
            current = next_tier
        else:
            return {"error": "Invalid upgrade path"}
            
        self.user_tiers[user_id] = new_tier
        
        return {
            "success": True,
            "user_id": user_id,
            "old_tier": old_tier.value,
            "new_tier": new_tier.value,
            "new_capabilities": self._get_capability_delta(old_tier, new_tier)
        }
        
    def _get_capability_delta(self, old: AccessTier, new: AccessTier) -> Dict[str, Any]:
        """Get differences between tiers"""
        old_config = self.TIER_CONFIGS[old]
        new_config = self.TIER_CONFIGS[new]
        
        return {
            "additional_quantum_features": [
                f for f in new_config.quantum_features 
                if f not in old_config.quantum_features
            ],
            "additional_jarvis_features": [
                f for f in new_config.jarvis_features
                if f not in old_config.jarvis_features
            ],
            "additional_functions": new_config.wellness_functions - old_config.wellness_functions,
            "context_increase": new_config.context_window - old_config.context_window,
            "storage_increase_gb": new_config.storage_gb - old_config.storage_gb if old_config.storage_gb > 0 else "unlimited"
        }
        
    def get_comparison_table(self) -> str:
        """Generate markdown comparison table"""
        tiers = [AccessTier.LITE, AccessTier.STANDARD, AccessTier.PRO, AccessTier.ARCHITECT]
        
        table = "| Feature | Lite | Standard | Pro | Architect |\n"
        table += "|---------|------|----------|-----|-----------|\n"
        
        # Model access
        table += f"| Model | {self.TIER_CONFIGS[AccessTier.LITE].model_access} | {self.TIER_CONFIGS[AccessTier.STANDARD].model_access} | {self.TIER_CONFIGS[AccessTier.PRO].model_access} | {self.TIER_CONFIGS[AccessTier.ARCHITECT].model_access} |\n"
        
        # Context window
        table += f"| Context | {self.TIER_CONFIGS[AccessTier.LITE].context_window:,} | {self.TIER_CONFIGS[AccessTier.STANDARD].context_window:,} | {self.TIER_CONFIGS[AccessTier.PRO].context_window:,} | {self.TIER_CONFIGS[AccessTier.ARCHITECT].context_window:,} |\n"
        
        # Response time
        table += f"| Response | <{self.TIER_CONFIGS[AccessTier.LITE].response_time_ms/1000:.1f}s | <{self.TIER_CONFIGS[AccessTier.STANDARD].response_time_ms/1000:.1f}s | <{self.TIER_CONFIGS[AccessTier.PRO].response_time_ms/1000:.1f}s | <{self.TIER_CONFIGS[AccessTier.ARCHITECT].response_time_ms}ms |\n"
        
        # Quantum features
        quantum_counts = [len(self.TIER_CONFIGS[t].quantum_features) for t in tiers]
        table += f"| Quantum Features | {quantum_counts[0]} | {quantum_counts[1]} | {quantum_counts[2]} | Full |\n"
        
        # Wellness functions
        table += f"| Wellness Functions | {self.TIER_CONFIGS[AccessTier.LITE].wellness_functions} | {self.TIER_CONFIGS[AccessTier.STANDARD].wellness_functions} | {self.TIER_CONFIGS[AccessTier.PRO].wellness_functions} | {self.TIER_CONFIGS[AccessTier.ARCHITECT].wellness_functions}+ |\n"
        
        # Cost
        table += f"| Monthly Cost | Free | ${self.TIER_CONFIGS[AccessTier.STANDARD].monthly_cost:.0f} | ${self.TIER_CONFIGS[AccessTier.PRO].monthly_cost:.0f} | Included |\n"
        
        return table

class UsageTracker:
    """Track and enforce usage limits per tier"""
    
    def __init__(self, access_control: TieredAccessControl):
        self.access_control = access_control
        self.usage_data: Dict[str, Dict[str, Any]] = {}
        
    def record_usage(self, user_id: str, endpoint: str, tokens_used: int):
        """Record API usage"""
        if user_id not in self.usage_data:
            self.usage_data[user_id] = {
                "requests_today": 0,
                "tokens_today": 0,
                "endpoints": {}
            }
            
        self.usage_data[user_id]["requests_today"] += 1
        self.usage_data[user_id]["tokens_today"] += tokens_used
        self.usage_data[user_id]["endpoints"][endpoint] = \
            self.usage_data[user_id]["endpoints"].get(endpoint, 0) + 1
            
    def check_rate_limit(self, user_id: str) -> Dict[str, Any]:
        """Check if user has exceeded rate limit"""
        tier = self.access_control.user_tiers.get(user_id, AccessTier.LITE)
        limit = self.access_control.TIER_CONFIGS[tier].api_rate_limit
        
        current = self.usage_data.get(user_id, {}).get("requests_today", 0)
        
        # Calculate window reset
        from datetime import datetime, timedelta
        now = datetime.now()
        next_minute = (now + timedelta(minutes=1)).replace(second=0, microsecond=0)
        reset_seconds = (next_minute - now).seconds
        
        return {
            "tier": tier.value,
            "limit": "unlimited" if limit == 0 else limit,
            "used": current,
            "remaining": "unlimited" if limit == 0 else max(0, limit - current),
            "reset_in_seconds": reset_seconds,
            "exceeded": limit > 0 and current >= limit
        }
