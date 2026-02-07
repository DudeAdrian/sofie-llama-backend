"""
Sofie-LLaMA Backend v6.0.0 — Main Entry Point
Quantum-Ready Wellness Intelligence with Production Jarvis
"""

import os
import sys

# CRITICAL: Check USE_OLLAMA before ANY imports that might trigger HuggingFace
USE_OLLAMA = os.getenv("USE_OLLAMA", "").lower() == "true"

if USE_OLLAMA:
    print("=" * 60)
    print("🔧 USE_OLLAMA=true detected")
    print("   Will use local Ollama - NO HuggingFace authentication required")
    print("=" * 60)
    print()

import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI
from dotenv import load_dotenv

# Load environment variables (again, to ensure they're available)
load_dotenv()

# Re-check after load_dotenv
USE_OLLAMA = os.getenv("USE_OLLAMA", "").lower() == "true"

from core.architecture import SofieCore, SofieConfig, DeploymentTier, create_sofie_core_from_env
from quantum.literal_quantum import QuantumOptimizer
from quantum.metaphorical_quantum import MetaphoricalQuantumEngine
from quantum.quantum_security import WellnessDataVault
from jarvis.capabilities import JarvisSystem
from wellness.function_library import WellnessLibrary
from tiered.access_control import TieredAccessControl
from integration.terracare_bridge import TerracareBridge, QuantumOracle, PostQuantumRegistry

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
    
    # Check for Ollama mode (re-check from environment)
    use_ollama = os.getenv("USE_OLLAMA", "").lower() == "true"
    
    if use_ollama:
        print("🔧 Ollama mode - using local LLM (no HuggingFace auth)")
        print(f"   Ollama URL: {os.getenv('OLLAMA_HOST', 'http://localhost:11434')}")
        print(f"   Model: {os.getenv('OLLAMA_MODEL', 'llama3.1:8b')}")
        print()
        
        # Initialize with Ollama only
        sofie_core = create_sofie_core_from_env()
        
        try:
            await sofie_core.initialize()
        except Exception as e:
            print(f"❌ Ollama initialization failed: {e}")
            print(f"   Ensure Ollama is running: ollama serve")
            print(f"   And model is pulled: ollama pull {os.getenv('OLLAMA_MODEL', 'llama3.1:8b')}")
            raise
            
    else:
        print("🔧 HuggingFace mode - will attempt to load transformers model")
        print("   (Requires HuggingFace token for gated models like Llama-3.1-70B)")
        print()
        
        # Determine deployment tier
        tier_str = os.getenv("DEPLOYMENT_TIER", "architect")
        tier = DeploymentTier(tier_str)
        
        # Initialize core with HuggingFace
        config = SofieConfig(
            deployment_tier=tier,
            enable_quantum=os.getenv("ENABLE_QUANTUM_OPTIMIZATION", "true").lower() == "true",
            context_window=int(os.getenv("CONTEXT_WINDOW", "128000")),
            local_path=os.getenv("MODEL_PATH")
        )
        
        sofie_core = SofieCore(config)
        
        try:
            await sofie_core.initialize()
        except Exception as e:
            print(f"⚠️ HuggingFace initialization failed: {e}")
            print("🔄 Falling back to Ollama mode...")
            print()
            
            # Auto-fallback to Ollama
            os.environ["USE_OLLAMA"] = "true"
            sofie_core = create_sofie_core_from_env()
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
    print("🤖 JARVIS Production System activated")
    print("   Components:")
    print("   - Voice Biometric Auth (Resemblyzer)")
    print("   - Speech-to-Text (faster-whisper)")
    print("   - Intent Engine (NLP)")
    print("   - GitHub Integration (PyGithub)")
    print("   - Code Generation (Ollama/LLaMA)")
    print("   - Safety Guardian (Syntax/Secret checks)")
    
    print("=" * 60)
    
    final_ollama_mode = os.getenv("USE_OLLAMA", "").lower() == "true" or (sofie_core and sofie_core.use_ollama)
    
    if final_ollama_mode:
        print("✅ Sofie-LLaMA v6.0.0-quantum + Production Jarvis ready!")
        print(f"   Mode: Ollama (Local)")
        print(f"   Model: {os.getenv('OLLAMA_MODEL', 'llama3.1:8b')}")
    else:
        print("✅ Sofie-LLaMA v6.0.0-quantum + Production Jarvis ready!")
        print(f"   Mode: HuggingFace Transformers")
    
    print(f"   Quantum: {'enabled' if sofie_core and sofie_core.config.enable_quantum else 'disabled'}")
    print(f"   JARVIS: {'autonomous' if jarvis_config['autonomous_enabled'] else 'manual'} (Production)")
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
    use_ollama = os.getenv("USE_OLLAMA", "").lower() == "true"
    return {
        "name": "Sofie-LLaMA Backend",
        "version": "6.0.0-quantum",
        "status": "operational",
        "quantum_ready": True,
        "ollama_mode": use_ollama,
        "model": os.getenv("OLLAMA_MODEL", "llama3.1:8b") if use_ollama else "Llama-3.1-70B",
        "documentation": "/docs"
    }


@app.get("/health")
async def health():
    """Health check endpoint"""
    use_ollama = os.getenv("USE_OLLAMA", "").lower() == "true"
    return {
        "status": "healthy",
        "sofie_core": "loaded" if sofie_core else "not_loaded",
        "ollama_mode": use_ollama,
        "jarvis": "active" if jarvis and jarvis.is_running else "inactive"
    }


if __name__ == "__main__":
    import uvicorn
    
    host = os.getenv("API_HOST", "0.0.0.0")
    port = int(os.getenv("API_PORT", "8000"))
    workers = int(os.getenv("API_WORKERS", "1"))
    
    print(f"Starting Sofie-LLaMA on {host}:{port}")
    print(f"USE_OLLAMA={os.getenv('USE_OLLAMA', 'false')}")
    print()
    
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        workers=workers,
        reload=os.getenv("DEBUG", "false").lower() == "true"
    )
