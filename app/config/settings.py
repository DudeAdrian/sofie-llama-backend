"""
Configuration module for S.O.F.I.E. Backend.
Loads settings from environment variables with sensible defaults.
"""

from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application settings with privacy and consent enforcement."""
    
    # Server Configuration
    host: str = "0.0.0.0"
    port: int = 8000
    environment: str = "development"
    
    # LLaMA Configuration
    llama_model_path: str = "models/llama-2-7b-chat.gguf"
    llama_n_ctx: int = 2048
    llama_n_threads: int = 4
    llama_temperature: float = 0.7
    
    # Privacy & Consent - Regulation Before Reasoning
    require_consent: bool = True
    consent_expiry_hours: int = 24
    
    # Logging
    log_level: str = "INFO"
    
    # CORS Configuration
    allowed_origins: List[str] = ["http://localhost:3000", "http://localhost:5173"]
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()
