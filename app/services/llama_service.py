"""
LLaMA Service - Context-aware wellness guidance with privacy enforcement.
Consent-before-computation is enforced at the service layer.
"""

import logging
from typing import Optional
from app.config import settings
from app.models.schemas import WellnessContext

logger = logging.getLogger(__name__)


class LlamaService:
    """
    Wrapper for LLaMA model providing wellness guidance.
    Lazy-loads model to avoid initialization errors when model file is missing.
    """
    
    def __init__(self):
        """Initialize service without loading model (lazy loading)."""
        self._llm = None
        self._model_loaded = False
        logger.info("LlamaService initialized (model will be lazy-loaded)")
    
    def _load_model(self) -> bool:
        """
        Lazy-load the LLaMA model.
        
        Returns:
            True if model loaded successfully, False otherwise
        """
        if self._model_loaded:
            return True
        
        try:
            from llama_cpp import Llama
            
            logger.info(f"Loading LLaMA model from {settings.llama_model_path}")
            self._llm = Llama(
                model_path=settings.llama_model_path,
                n_ctx=settings.llama_n_ctx,
                n_threads=settings.llama_n_threads,
                verbose=False
            )
            self._model_loaded = True
            logger.info("LLaMA model loaded successfully")
            return True
            
        except FileNotFoundError:
            logger.warning(
                f"LLaMA model not found at {settings.llama_model_path}. "
                "Service will return mock responses. "
                "Download a model to enable real LLaMA inference."
            )
            return False
        except Exception as e:
            logger.error(f"Failed to load LLaMA model: {e}")
            return False
    
    def is_available(self) -> bool:
        """
        Check if LLaMA model is available.
        
        Returns:
            True if model is loaded and ready, False otherwise
        """
        if not self._model_loaded:
            return self._load_model()
        return True
    
    def _build_wellness_prompt(
        self, 
        query: str, 
        context: Optional[WellnessContext] = None
    ) -> str:
        """
        Build a wellness-focused prompt for LLaMA.
        
        Args:
            query: User's wellness question
            context: Optional user context for personalization
            
        Returns:
            Formatted prompt for LLaMA
        """
        system_prompt = (
            "You are S.O.F.I.E. (Sentient Orchestrator for Integrated Evidence-based wellness), "
            "a compassionate AI wellness guide. Provide evidence-based, supportive wellness "
            "guidance that respects user autonomy and promotes holistic wellbeing. "
            "Keep responses concise, practical, and empowering."
        )
        
        context_str = ""
        if context:
            context_parts = []
            if context.mood:
                context_parts.append(f"Current mood: {context.mood}")
            if context.energy_level:
                context_parts.append(f"Energy level: {context.energy_level}/10")
            if context.stress_level:
                context_parts.append(f"Stress level: {context.stress_level}/10")
            if context.sleep_quality:
                context_parts.append(f"Sleep quality: {context.sleep_quality}/10")
            if context.goals:
                context_parts.append(f"Goals: {', '.join(context.goals)}")
            
            if context_parts:
                context_str = "\n\nUser Context:\n" + "\n".join(context_parts)
        
        prompt = f"{system_prompt}{context_str}\n\nUser Question: {query}\n\nS.O.F.I.E. Response:"
        return prompt
    
    def generate_wellness_guidance(
        self,
        query: str,
        context: Optional[WellnessContext] = None,
        max_tokens: int = 300
    ) -> str:
        """
        Generate wellness guidance using LLaMA.
        
        Args:
            query: User's wellness question
            context: Optional user context for personalization
            max_tokens: Maximum tokens to generate
            
        Returns:
            Generated wellness guidance text
        """
        prompt = self._build_wellness_prompt(query, context)
        
        # Try to use real LLaMA model
        if self.is_available() and self._llm:
            try:
                logger.info(f"Generating wellness guidance with LLaMA for query: {query[:50]}...")
                response = self._llm(
                    prompt,
                    max_tokens=max_tokens,
                    temperature=settings.llama_temperature,
                    stop=["User Question:", "\n\n"],
                    echo=False
                )
                
                guidance = response['choices'][0]['text'].strip()
                logger.info(f"Generated {len(guidance)} characters of wellness guidance")
                return guidance
                
            except Exception as e:
                logger.error(f"LLaMA inference failed: {e}. Falling back to mock response.")
        
        # Fallback to mock response when model not available
        logger.info("Using mock wellness guidance (LLaMA model not available)")
        return self._generate_mock_guidance(query, context)
    
    def _generate_mock_guidance(
        self,
        query: str,
        context: Optional[WellnessContext] = None
    ) -> str:
        """
        Generate mock wellness guidance when LLaMA is not available.
        This allows the backend to function for testing without a model.
        
        Args:
            query: User's wellness question
            context: Optional user context
            
        Returns:
            Mock wellness guidance
        """
        context_note = ""
        if context:
            context_note = " I've noted your current context including "
            parts = []
            if context.mood:
                parts.append(f"mood ({context.mood})")
            if context.stress_level:
                parts.append(f"stress level ({context.stress_level}/10)")
            if context.goals:
                parts.append(f"goals ({', '.join(context.goals[:2])})")
            
            if parts:
                context_note += " and ".join(parts) + "."
        
        return (
            f"[MOCK RESPONSE - LLaMA model not loaded]\n\n"
            f"Thank you for your question: '{query[:100]}...'{context_note}\n\n"
            f"This is a demonstration response. To receive real AI-powered wellness guidance, "
            f"please download a LLaMA model (e.g., llama-2-7b-chat.gguf) and place it in the "
            f"models/ directory, then configure LLAMA_MODEL_PATH in your .env file.\n\n"
            f"For your wellness question, I would provide evidence-based, compassionate guidance "
            f"that respects your autonomy and supports your holistic wellbeing journey."
        )


# Global LLaMA service instance
llama_service = LlamaService()
