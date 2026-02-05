"""
Sofie-LLaMA Backend v6.0.0 — Main Entry Point
Quantum-Ready Wellness Intelligence
"""

import asyncio
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from dotenv import load_dotenv

from core.architecture import SofieCore, SofieConfig, DeploymentTier
from quantum.literal_quantum import QuantumOptimizer
from quantum.metaphorical_quantum import MetaphoricalQuantumEngine
from quantum.quantum_security import WellnessDataVault
from jarvis.capabilities import JarvisSystem
from wellness.function_library import WellnessLibrary
from tiered.access_control import TieredAccessControl
from integration.terracare_bridge import TerracareBridge, QuantumOracle, PostQuantumRegistry

# Load environment variables
load_dotenv()

# Global instances
sofie_core: SofieCore = None
quantum_optimizer: QuantumOptimizer = None
jarvis: JarvisSystem = None
wellness_library: WellnessLibrary = None
access_control: TieredAccessControl = None
terracare: TerracareBridge = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    global sofie_core, quantum_optimizer, jarvis, wellness_library, access_control, terracare
    
    print("🌸 Initializing Sofie-LLaMA v6.0.0-quantum...")
    print("=" * 60)
    
    # Determine deployment tier
    tier_str = os.getenv("DEPLOYMENT_TIER", "architect")
    tier = DeploymentTier(tier_str)
    
    # Initialize core
    config = SofieConfig(
        deployment_tier=tier,
        enable_quantum=os.getenv("ENABLE_QUANTUM_OPTIMIZATION", "true").lower() == "true",
        context_window=int(os.getenv("CONTEXT_WINDOW", "128000")),
        local_path=os.getenv("MODEL_PATH")
    )
    
    sofie_core = SofieCore(config)
    await sofie_core.initialize()
    
    # Initialize quantum layer
    quantum_optimizer = QuantumOptimizer()
    
    # Initialize quantum providers if configured
    if os.getenv("IBM_QUANTUM_TOKEN"):
        from quantum.literal_quantum import IBMQuantumBackend
        ibm = IBMQuantumBackend(os.getenv("IBM_QUANTUM_TOKEN"))
        await quantum_optimizer.add_backend("ibm", ibm)
    
    print("🔷 Quantum layer initialized")
    
    # Initialize wellness library
    wellness_library = WellnessLibrary()
    print(f"📚 Wellness library loaded: {len(wellness_library.functions)} functions")
    
    # Initialize tiered access
    access_control = TieredAccessControl()
    print("🔐 Access control initialized")
    
    # Initialize Terracare bridge
    terracare = TerracareBridge(
        network=os.getenv("TERRACARE_NETWORK", "testnet"),
        private_key=os.getenv("ARCHITECT_PRIVATE_KEY")
    )
    await terracare.connect()
    print("⛓️ Terracare Ledger connected")
    
    # Initialize JARVIS
    jarvis_config = {
        "voice_enabled": os.getenv("ENABLE_VOICE_INTERFACE", "true").lower() == "true",
        "autonomous_enabled": os.getenv("ENABLE_JARVIS_AUTONOMOUS", "true").lower() == "true",
        "holographic_enabled": os.getenv("ENABLE_HOLOGRAPHIC", "false").lower() == "true"
    }
    jarvis = JarvisSystem(jarvis_config)
    
    if jarvis_config["autonomous_enabled"]:
        await jarvis.start()
    print("🤖 JARVIS system activated")
    
    print("=" * 60)
    print("✅ Sofie-LLaMA v6.0.0-quantum ready!")
    print(f"   Tier: {tier.value}")
    print(f"   Quantum: {'enabled' if config.enable_quantum else 'disabled'}")
    print(f"   JARVIS: {'autonomous' if jarvis_config['autonomous_enabled'] else 'manual'}")
    print("=" * 60)
    
    yield
    
    # Cleanup
    print("\n🛑 Shutting down Sofie-LLaMA...")
    if jarvis:
        jarvis.is_running = False
    print("👋 Goodbye!")


# Create FastAPI app
app = FastAPI(
    title="Sofie-LLaMA Backend",
    description="Quantum-Ready Wellness Intelligence v6.0.0",
    version="6.0.0-quantum",
    lifespan=lifespan
)

# Import and include routes
from api.routes import app as routes_app

# Copy routes from routes.py
for route in routes_app.routes:
    app.routes.append(route)


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": "Sofie-LLaMA Backend",
        "version": "6.0.0-quantum",
        "status": "operational",
        "quantum_ready": True,
        "documentation": "/docs"
    }


if __name__ == "__main__":
    import uvicorn
    
    host = os.getenv("API_HOST", "0.0.0.0")
    port = int(os.getenv("API_PORT", "8000"))
    workers = int(os.getenv("API_WORKERS", "1"))
    
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        workers=workers,
        reload=os.getenv("DEBUG", "false").lower() == "true"
    )
