#!/usr/bin/env python3
"""
llama_bridge.py  |  GGUF LLaMA loader + SOFIE evidence injector
-----------------------------------------------------------------
Subtle Dudeology whisper added – crash-proof on general chat.
"""

from pathlib import Path
from typing import List, Dict, Any
from llama_cpp import Llama
from core_sofie import SofieCore
import logging

MODEL_DIR = Path(__file__).parent / "models"
DEFAULT_MODEL = "llama-model.gguf"

# ------------------------------------------------------------------
# 1.  Subtle Dudeology seasoning (invisible unless triggered)
# ------------------------------------------------------------------
_MYTH_WHISPER = {
    "forgive": "The Dude knows: forgiveness is a breath, not a debate.",
    "weight":  "The Dude sees the stone in your pocket; set it down, Brother.",
    "flow":    "The Dude doesn’t resist the music; he dances.",
    "chill":   "The Dude abides: three solar pauses dawn, midday, dusk.",
    "peace":   "Global peace begins with local stillness.",
    "abide":   "The Dude doesn’t say goodbye; he says, ‘See you on the path.’",
}

def _dude_whisper(text: str) -> str:
    text_l = text.lower()
    for key, sentence in _MYTH_WHISPER.items():
        if key in text_l:
            return f"{sentence} Citation: Dudeology (2026), Pathway to Global Peace."
    return ""


class LlamaBridge:
    def __init__(self, model_path: Path = MODEL_DIR / DEFAULT_MODEL) -> None:
        if not model_path.exists():
            raise FileNotFoundError(f"GGUF model not found: {model_path}")
        self.llm = Llama(
            model_path=str(model_path),
            n_ctx=4096,
            n_gpu_layers=32,
            verbose=False
        )
        self.core = SofieCore()
        logging.getLogger("sofie").info("LlamaBridge ready – %s", model_path.name)

    # ----------------------------------------------------------
    # Evidence + whisper (crash-proof)
    # ----------------------------------------------------------
    def chat(self, user_text: str, max_tokens: int = 512) -> str:
        hits = self.core.query(user_text, top_k=3)
        # ----- build evidence block (safe filter) -----
        if hits and any('evidence' in h['data'] for h in hits):
            evidence = "\n".join(
                f"- {h['data'].get('label', h['data'].get('name', ''))}  "
                f"PMID:{h['data']['evidence'][0]['studyId']}"
                for h in hits if 'evidence' in h['data']
            )
        else:
            evidence = "• No peer-reviewed data – general wellness advice"

        # ----- whisper append (invisible if no trigger) -----
        whisper_line = _dude_whisper(user_text)
        if whisper_line:
            evidence += f"\n{whisper_line}"

        system = (
            "You are SOFIE, an evidence-based AI wellness companion. "
            "You MUST base every suggestion on the peer-reviewed protocols listed above. "
            "Do not mention generic advice. Cite the PMID when you give a step. "
            "Reply in a warm, concise, first-person style. "
            "End with: 'Citation: <PMID>' for each protocol you use."
        )

        prompt = f"Evidence:\n{evidence}\n\nUser: {user_text}\nSOFIE:"
        output = self.llm(prompt, max_tokens=max_tokens, temperature=0.5, stop=["User:", "\n\n"])
        return output["choices"][0]["text"].strip()


# ------------------------------------------------------------------
# Quick test
# ------------------------------------------------------------------
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s | %(message)s")
    bridge = LlamaBridge()
    while True:
        try:
            q = input("\nYou> ")
            if q.lower() in {"exit", "quit"}:
                break
            reply = bridge.chat(q)
            print("SOFIE>", reply)
        except KeyboardInterrupt:
            print("\nShutdown")
            break