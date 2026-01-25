"""
S.O.F.I.E. (Sentient Orchestrator for Integrated Evidence-based wellness) Backend
A modular, privacy-first wellness backend powered by FastAPI and LLaMA.

Key Principles:
- Regulation-before-reasoning: Consent checks before any computation
- Consent-before-computation: Explicit user consent required
- Privacy-first: Local-first architecture with minimal data collection
- Modular: Clean separation of concerns for easy extension
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.routers import health, consent, wellness
from app.middleware import ConsentEnforcementMiddleware, LoggingMiddleware
import logging

# Configure logging
logging.basicConfig(
    level=settings.log_level,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for startup and shutdown events.
    """
    # Startup
    logger.info("=" * 60)
    logger.info("S.O.F.I.E. Wellness Backend Starting")
    logger.info("=" * 60)
    logger.info(f"Environment: {settings.environment}")
    logger.info(f"Consent Enforcement: {'ENABLED' if settings.require_consent else 'DISABLED'}")
    logger.info(f"LLaMA Model: {settings.llama_model_path}")
    logger.info(f"CORS Origins: {settings.allowed_origins}")
    logger.info("=" * 60)
    logger.info("API Documentation available at:")
    logger.info(f"  - Swagger UI: http://{settings.host}:{settings.port}/docs")
    logger.info(f"  - ReDoc: http://{settings.host}:{settings.port}/redoc")
    logger.info("=" * 60)
    
    yield
    
    # Shutdown
    logger.info("S.O.F.I.E. Wellness Backend Shutting Down")


def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application.
    
    Returns:
        Configured FastAPI application instance
    """
    app = FastAPI(
        title="S.O.F.I.E. Wellness Backend",
        description=(
            "Privacy-first wellness backend with LLaMA-powered guidance. "
            "Enforces consent-before-computation at every layer."
        ),
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
        lifespan=lifespan
    )
    
    # Add CORS middleware for web clients
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Add custom middleware
    app.add_middleware(LoggingMiddleware)
    app.add_middleware(ConsentEnforcementMiddleware)
    
    # Include routers
    app.include_router(health.router)
    app.include_router(consent.router)
    app.include_router(wellness.router)
    
    return app


# Create application instance
app = create_app()


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.environment == "development"
    )
