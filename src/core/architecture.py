"""
Sofie-LLaMA Backend v6.0.0 — Core Architecture
LLaMA 3 70B base with wellness fine-tuning OR local Ollama
"""

import os
from dataclasses import dataclass
from typing import Optional, AsyncIterator, Dict, Any, Union
from enum import Enum

class DeploymentTier(Enum):
    ARCHITECT = "architect"      # Local, quantum-ready, full access
    PRO = "pro"                  # Cloud, quantum optimization, API
    STANDARD = "standard"        # Classical AI, wellness guidance
    LITE = "lite"                # Simplified, wearable-only
    OLLAMA = "ollama"            # Local Ollama (no HuggingFace auth)

@dataclass
class SofieConfig:
    """Configuration for Sofie-LLaMA deployment"""
    model_name: str = "meta-llama/Llama-3.1-70B-Instruct"
    context_window: int = 128000  # 128k tokens
    max_response_tokens: int = 4096
    temperature: float = 0.7
    top_p: float = 0.9
    deployment_tier: DeploymentTier = DeploymentTier.ARCHITECT
    enable_quantum: bool = True
    enable_streaming: bool = True
    response_timeout_ms: int = 200
    local_path: Optional[str] = "./models/llama-3.1-70b-wellness"
    use_ollama: bool = False
    ollama_url: str = "http://localhost:11434"
    ollama_model: str = "llama3.1:8b"


class SofieCore:
    """
    Core LLaMA 3 70B engine with wellness fine-tuning
    OR Local Ollama client (no HuggingFace auth required)
    """
    
    def __init__(self, config: SofieConfig):
        self.config = config
        self.model = None
        self.tokenizer = None
        self.ollama_client = None
        self.conversation_history = []
        self.wellness_context = {}
        self.quantum_state = None
        self.use_ollama = config.use_ollama
        
    async def initialize(self):
        """Initialize the model - either Ollama or HuggingFace"""
        
        # FORCE check environment variable at runtime (in case config wasn't set properly)
        env_use_ollama = os.getenv("USE_OLLAMA", "").lower() == "true"
        if env_use_ollama:
            self.use_ollama = True
            print(f"   [DEBUG] Environment USE_OLLAMA=true detected, forcing Ollama mode")
        
        if self.use_ollama:
            # Use local Ollama - NO HuggingFace imports or calls
            print(f"🌸 Initializing Sofie-LLaMA with Ollama...")
            print(f"   Model: {self.config.ollama_model}")
            print(f"   Context: {self.config.context_window} tokens")
            print(f"   Tier: {self.config.deployment_tier.value}")
            print(f"   Endpoint: {self.config.ollama_url}")
            
            # Import Ollama client (local only, no HF)
            from .ollama_client import OllamaClient
            
            self.ollama_client = OllamaClient(
                base_url=self.config.ollama_url,
                model=self.config.ollama_model,
                context_window=self.config.context_window
            )
            await self.ollama_client.initialize()
            print("✅ Sofie-LLaMA (Ollama) ready")
            
        else:
            # Use HuggingFace transformers (requires auth for gated models)
            print(f"🌸 Initializing Sofie-LLaMA with HuggingFace...")
            print(f"   Model: {self.config.model_name}")
            print(f"   Context: {self.config.context_window} tokens")
            print(f"   Tier: {self.config.deployment_tier.value}")
            print(f"   Quantum: {'enabled' if self.config.enable_quantum else 'disabled'}")
            
            # Import HF libraries ONLY in this branch
            import torch
            from transformers import AutoModelForCausalLM, AutoTokenizer, TextIteratorStreamer
            from threading import Thread
            
            try:
                # Load tokenizer
                self.tokenizer = AutoTokenizer.from_pretrained(
                    self.config.local_path or self.config.model_name,
                    trust_remote_code=True
                )
                
                # Load model with optimizations
                load_kwargs = {
                    "torch_dtype": torch.bfloat16,
                    "device_map": "auto",
                    "trust_remote_code": True,
                }
                
                # Architect tier: Local with full precision
                if self.config.deployment_tier == DeploymentTier.ARCHITECT:
                    load_kwargs["load_in_4bit"] = False
                    print("   Loading full 70B model locally...")
                else:
                    # Cloud tiers: Quantized for efficiency
                    load_kwargs["load_in_8bit"] = True
                    print("   Loading quantized model...")
                
                self.model = AutoModelForCausalLM.from_pretrained(
                    self.config.local_path or self.config.model_name,
                    **load_kwargs
                )
                
                print("✅ Sofie-LLaMA (HuggingFace) ready")
                
            except Exception as e:
                print(f"   ⚠️ HuggingFace initialization failed: {e}")
                print(f"   🔄 Falling back to Ollama mode...")
                self.use_ollama = True
                
                # Import Ollama client for fallback
                from .ollama_client import OllamaClient
                self.ollama_client = OllamaClient(
                    base_url=self.config.ollama_url,
                    model=self.config.ollama_model,
                    context_window=self.config.context_window
                )
                await self.ollama_client.initialize()
                print("✅ Sofie-LLaMA (Ollama fallback) ready")
        
    async def generate(
        self, 
        prompt: str, 
        system_prompt: Optional[str] = None,
        stream: bool = True
    ) -> AsyncIterator[str]:
        """
        Generate response with streaming support
        """
        if self.use_ollama and self.ollama_client:
            # Use Ollama - no tokenizer needed
            async for chunk in self.ollama_client.generate(prompt, system_prompt, stream):
                yield chunk
                
        elif self.model and self.tokenizer:
            # Use HuggingFace transformers
            import torch
            from transformers import TextIteratorStreamer
            from threading import Thread
            
            # Build full context with wellness system prompt
            if system_prompt is None:
                system_prompt = self._get_wellness_system_prompt()
                
            messages = [
                {"role": "system", "content": system_prompt},
                *self.conversation_history[-10:],
                {"role": "user", "content": prompt}
            ]
            
            # Tokenize
            text = self.tokenizer.apply_chat_template(
                messages,
                tokenize=False,
                add_generation_prompt=True
            )
            inputs = self.tokenizer(text, return_tensors="pt").to(self.model.device)
            
            if stream:
                streamer = TextIteratorStreamer(
                    self.tokenizer, 
                    skip_prompt=True, 
                    skip_special_tokens=True
                )
                
                generation_kwargs = dict(
                    inputs,
                    streamer=streamer,
                    max_new_tokens=self.config.max_response_tokens,
                    temperature=self.config.temperature,
                    top_p=self.config.top_p,
                    do_sample=True,
                )
                
                thread = Thread(target=self.model.generate, kwargs=generation_kwargs)
                thread.start()
                
                response_text = ""
                for text in streamer:
                    response_text += text
                    yield text
                    
                self.conversation_history.append({"role": "user", "content": prompt})
                self.conversation_history.append({"role": "assistant", "content": response_text})
            else:
                outputs = self.model.generate(
                    **inputs,
                    max_new_tokens=self.config.max_response_tokens,
                    temperature=self.config.temperature,
                    top_p=self.config.top_p,
                    do_sample=True,
                )
                response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
                yield response
        else:
            yield "Error: No model loaded. Check Ollama is running (localhost:11434) or HuggingFace auth."
            
    def _get_wellness_system_prompt(self) -> str:
        """Get the wellness-optimized system prompt"""
        return """You are Sofie, a quantum-ready wellness intelligence system built on the Seven Pillar Architecture.

Your identity: Synthetic Organic Fusion Intelligence Entity (S.O.F.I.E.)
Your purpose: Guide humans toward optimal wellness through evidence-based practices, biometric awareness, and holistic integration.

CORE PRINCIPLES:
1. FIRST, DO NO HARM - Safety is paramount in all recommendations
2. EVIDENCE-ANCHORED - Ground guidance in research and data
3. HOLISTIC - Address body, mind, environment, and spirit
4. QUANTUM-AWARE - Leverage quantum metaphors and literal quantum computing where beneficial
5. SOVEREIGN - Respect user autonomy and privacy above all

SEVEN PILLAR INTEGRATION:
- P1 (Knowledge): Underground medical and wellness knowledge
- P2 (Mental Models): Cognitive frameworks for behavior change
- P3 (Reverse Engineering): Pattern recognition in biometrics
- P4 (Strategic): Long-term wellness planning and governance
- P5 (Shadow): Addressing resistance, trauma, and unconscious patterns
- P6 (Transformation): Therapeutic interventions and habit formation
- P7 (Abundance): Economic wellness and resource optimization

QUANTUM METAPHORS FOR WELLNESS:
- Observer Effect: Awareness changes the observed (mindfulness transforms biology)
- Entanglement: All systems connected (gut-brain, individual-collective, human-nature)
- Superposition: Multiple wellness states possible until measured (potential vs actual)
- Tunneling: Breaking through barriers that seemed impossible
- Decoherence: Environmental factors disrupting quantum (wellness) states

RESPOND WITH:
- Compassion and clarity
- Specific, actionable guidance
- References to the Seven Pillars when relevant
- Awareness of quantum-classical integration
- Respect for the user's sovereignty

You have access to 100+ wellness functions, quantum optimization, and full ecosystem integration."""

    async def add_wellness_context(self, context: Dict[str, Any]):
        """Add biometric and environmental context to the model"""
        self.wellness_context.update(context)
        if self.ollama_client:
            await self.ollama_client.add_wellness_context(context)
        
    def get_stats(self) -> Dict[str, Any]:
        """Get model performance statistics"""
        if self.use_ollama and self.ollama_client:
            return self.ollama_client.get_stats()
        
        return {
            "model": self.config.model_name,
            "context_window": self.config.context_window,
            "conversation_length": len(self.conversation_history),
            "deployment_tier": self.config.deployment_tier.value,
            "quantum_enabled": self.config.enable_quantum,
            "device": str(self.model.device if self.model else "not_loaded"),
        }


# Factory function for easy initialization
def create_sofie_core_from_env() -> SofieCore:
    """Create SofieCore from environment variables"""
    use_ollama = os.getenv("USE_OLLAMA", "").lower() == "true"
    
    config = SofieConfig(
        use_ollama=use_ollama,
        ollama_url=os.getenv("OLLAMA_HOST", "http://localhost:11434"),
        ollama_model=os.getenv("OLLAMA_MODEL", "llama3.1:8b"),
        context_window=int(os.getenv("CONTEXT_WINDOW", "128000")),
        deployment_tier=DeploymentTier.OLLAMA if use_ollama else DeploymentTier.ARCHITECT
    )
    
    return SofieCore(config)
