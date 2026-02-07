"""
Ollama Client Wrapper
Local LLM integration using Ollama API
"""

import os
import asyncio
from typing import Optional, AsyncIterator, Dict, Any
import aiohttp


class OllamaClient:
    """
    Client for local Ollama API
    Compatible with SofieCore interface
    """
    
    def __init__(
        self,
        base_url: str = "http://localhost:11434",
        model: str = "llama3.1:8b",
        context_window: int = 128000
    ):
        self.base_url = base_url
        self.model = model
        self.context_window = context_window
        self.conversation_history = []
        self.wellness_context = {}
        self.device = "ollama-local"
        
    async def initialize(self):
        """Initialize Ollama connection"""
        print(f"🌸 Initializing Sofie-LLaMA with Ollama...")
        print(f"   Model: {self.model}")
        print(f"   Context: {self.context_window} tokens")
        print(f"   Endpoint: {self.base_url}")
        
        # Test connection
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.base_url}/api/tags") as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        models = [m.get('name') for m in data.get('models', [])]
                        if self.model in models:
                            print(f"   ✓ Model {self.model} available")
                        else:
                            print(f"   ⚠️ Model {self.model} not found. Available: {models}")
                            print(f"   Run: ollama pull {self.model}")
                    else:
                        print(f"   ⚠️ Ollama returned status {resp.status}")
        except Exception as e:
            print(f"   ⚠️ Could not connect to Ollama: {e}")
            print(f"   Ensure Ollama is running: ollama serve")
        
        print("✅ Sofie-LLaMA (Ollama) ready")
        
    async def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        stream: bool = True
    ) -> AsyncIterator[str]:
        """
        Generate response using Ollama API
        """
        if system_prompt is None:
            system_prompt = self._get_wellness_system_prompt()
        
        # Build messages
        messages = [
            {"role": "system", "content": system_prompt},
            *self.conversation_history[-10:],
            {"role": "user", "content": prompt}
        ]
        
        # Convert to prompt for Ollama
        full_prompt = self._format_messages(messages)
        
        if stream:
            async for chunk in self._generate_stream(full_prompt):
                yield chunk
        else:
            response = await self._generate_single(full_prompt)
            yield response
    
    def _format_messages(self, messages: list) -> str:
        """Format messages for Ollama"""
        formatted = []
        for msg in messages:
            role = msg.get("role", "user")
            content = msg.get("content", "")
            if role == "system":
                formatted.append(f"System: {content}")
            elif role == "assistant":
                formatted.append(f"Assistant: {content}")
            else:
                formatted.append(f"User: {content}")
        formatted.append("Assistant:")
        return "\n\n".join(formatted)
    
    async def _generate_stream(self, prompt: str) -> AsyncIterator[str]:
        """Stream generation from Ollama"""
        url = f"{self.base_url}/api/generate"
        
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": True,
            "options": {
                "temperature": 0.7,
                "top_p": 0.9,
                "num_predict": 4096
            }
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=payload) as resp:
                    if resp.status != 200:
                        yield f"Error: Ollama returned {resp.status}"
                        return
                    
                    response_text = ""
                    async for line in resp.content:
                        if line:
                            try:
                                data = line.decode('utf-8').strip()
                                if data:
                                    import json
                                    chunk = json.loads(data)
                                    if "response" in chunk:
                                        text = chunk["response"]
                                        response_text += text
                                        yield text
                                    if chunk.get("done"):
                                        break
                            except:
                                pass
                    
                    # Store in history
                    # Extract user prompt from the formatted prompt
                    user_prompt = prompt.split("User:")[-1].split("Assistant:")[0].strip()
                    self.conversation_history.append({"role": "user", "content": user_prompt})
                    self.conversation_history.append({"role": "assistant", "content": response_text})
                    
        except Exception as e:
            yield f"Error connecting to Ollama: {str(e)}"
    
    async def _generate_single(self, prompt: str) -> str:
        """Non-streaming generation"""
        url = f"{self.base_url}/api/generate"
        
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.7,
                "top_p": 0.9,
                "num_predict": 4096
            }
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=payload) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        return data.get("response", "")
                    else:
                        return f"Error: Ollama returned {resp.status}"
        except Exception as e:
            return f"Error: {str(e)}"
    
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
        """Add biometric and environmental context"""
        self.wellness_context.update(context)
        
    def get_stats(self) -> Dict[str, Any]:
        """Get model performance statistics"""
        return {
            "model": self.model,
            "context_window": self.context_window,
            "conversation_length": len(self.conversation_history),
            "deployment_tier": "ollama-local",
            "quantum_enabled": True,
            "device": self.device,
        }


# Factory function for easy initialization
def create_ollama_client() -> OllamaClient:
    """Create Ollama client from environment"""
    base_url = os.getenv("OLLAMA_HOST", "http://localhost:11434")
    model = os.getenv("OLLAMA_MODEL", "llama3.1:8b")
    context = int(os.getenv("CONTEXT_WINDOW", "128000"))
    
    return OllamaClient(
        base_url=base_url,
        model=model,
        context_window=context
    )
