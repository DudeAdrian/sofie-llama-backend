#!/usr/bin/env python3
"""
core_sofie.py  |  Central brain of SOFIE AI Companion
----------------------------------------------------
- Loads every JSON in /library
- Exposes a single query() interface
- Returns evidence-anchored answers + optional tone-play commands
- Keeps LLM outside this file (passed in as callback)
"""

import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any

LIB_DIR = Path(__file__).parent / "library"

# ------------------------------------------------------------------
# Logging
# ------------------------------------------------------------------
log = logging.getLogger("sofie")
if not log.handlers:
    logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)s | %(message)s"
    )


# ------------------------------------------------------------------
# Central Evidence Engine
# ------------------------------------------------------------------
class SofieCore:
    """Loads and queries the locked JSON knowledge library"""

    def __init__(self, lib_dir: Path = LIB_DIR) -> None:
        self.lib: Dict[str, Any] = {}
        self._load_library(lib_dir)
        log.info("SofieCore ready – %s modules loaded", len(self.lib))

    # ----------------------------------------------------------
    # Library loader (continues on bad file, logs culprit)
    # ----------------------------------------------------------
    def _load_library(self, lib_dir: Path) -> None:
        if not lib_dir.exists():
            raise FileNotFoundError(f"Library folder not found: {lib_dir}")

        for json_path in lib_dir.glob("*.json"):
            key = json_path.stem.replace("sofie_", "").replace("sofia_", "")
            try:
                with json_path.open(encoding="utf-8") as f:
                    self.lib[key] = json.load(f)
            except json.JSONDecodeError as e:
                log.error("Invalid JSON %s: %s", json_path.name, e)
                continue   # keep going
            except Exception as e:
                log.error("Unexpected error loading %s: %s", json_path.name, e)
                continue

    # ----------------------------------------------------------
    # Single-query API
    # ----------------------------------------------------------
    def query(self, user_intent: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """Return ranked evidence blocks ready for LLM prompt injection"""
        hits: List[Dict[str, Any]] = []
        intent_lower = user_intent.lower()

        for module, content in self.lib.items():
            for proto in content.get("protocols", []):
                score = self._relevance_score(intent_lower, proto)
                if score > 0:
                    hits.append({"module": module, "score": score, "data": proto})

            for sys in content.get("systems", []):
                score = self._relevance_score(intent_lower, sys)
                if score > 0:
                    hits.append({"module": module, "score": score, "data": sys})

            for rit in content.get("rituals", []):
                score = self._relevance_score(intent_lower, rit)
                if score > 0:
                    hits.append({"module": module, "score": score, "data": rit})

        hits.sort(key=lambda x: x["score"], reverse=True)
        return hits[:top_k]

    # ----------------------------------------------------------
    # Relevance scorer (0-1)
    # ----------------------------------------------------------
    def _relevance_score(self, intent: str, block: Dict[str, Any]) -> float:
        text = " ".join(
            block.get("purpose", "").split()
            + block.get("label", "").split()
            + block.get("name", "").split()
        ).lower()
        words = set(intent.split())
        overlap = len(words.intersection(text.split()))
        return overlap / max(len(words), 1)

    # ----------------------------------------------------------
    # Tone generator command (for future audio engine)
    # ----------------------------------------------------------
    def tone_command(self, protocol_id: str) -> Optional[Dict[str, Any]]:
        """Return JSON blob for pydub / pygame tone generator"""
        for mod, content in self.lib.items():
            for p in content.get("measuredRegistry", []):
                if p["id"] == protocol_id:
                    return {
                        "hz": p["hz"],
                        "duration_s": 600,   # 10 min default
                        "volume_db": -20,
                        "waveform": "sine"
                    }
        return None


# ------------------------------------------------------------------
# Quick CLI test loop (only when run directly)
# ------------------------------------------------------------------
if __name__ == "__main__":
    core = SofieCore()
    print("Sofie>  (type 'exit' to quit)")
    while True:
        try:
            q = input("Sofie> ").strip()
            if q in {"exit", "quit"}:
                break
            hits = core.query(q)
            for h in hits:
                print(f"[{h['module']}] {h['data'].get('label', h['data'].get('name', ''))}  score={h['score']:.2f}")
                print("  PMID:", h['data']['evidence'][0]['studyId'])
        except KeyboardInterrupt:
            print("\nShutdown")
            break