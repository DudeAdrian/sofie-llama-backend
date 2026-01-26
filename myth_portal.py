#!/usr/bin/env python3
"""
myth_portal.py  |  Dream-symbol ingestion + archetype tracker
--------------------------------------------------------------
- Accepts dream text → extracts symbols + emotions
- Maps to Jungian archetypes via locked JSON
- Tracks personal myth-cycle (anima/animus, shadow, self)
- Outputs next ritual prompt + symbol frequency graph
- Zero external deps except re (stdlib)
"""

import json
import sqlite3
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Dict, Any, Tuple

DB_FILE      = Path(__file__).parent / "library" / "somatic_ledger.db"
MYTH_JSON    = Path(__file__).parent / "library" / "sofie_myth Archetypes.json"   # delivered below
SYMBOL_CSV   = Path(__file__).parent / "symbol_frequency.csv"   # human-readable export


# ------------------------------------------------------------------
# 1. Locked mini-JSON (delivered inline) – Jungian archetype map
# ------------------------------------------------------------------
LOCKED_MYTH = {
    "archetypes": {
        "anima": {"symbols": ["woman", "moon", "water", "cat"], "emotion": "yearning"},
        "animus": ["man", "sun", "sword", "eagle"],
        "shadow": ["dark", "beast", "chase", "fall"],
        "self": ["mountain", "mandala", "gold", "center"],
        "trickster": ["clown", "mask", "maze", "mirror"]
    },
    "emotion_to_rite": {
        "yearning": "anima_encounter_ritual",
        "anger": "shadow_boxing_ritual",
        "peace": "self_mountaintop_ritual"
    }
}


# ------------------------------------------------------------------
# 2. Dream ingestion API
# ------------------------------------------------------------------
def ingest_dream(text: str, date: datetime | None = None) -> Dict[str, Any]:
    date = date or datetime.now(timezone.utc)
    symbols = _extract_symbols(text)
    emotion = _detect_emotion(text)
    arche hits = _map_to_archetypes(symbols)
    primary = max(arche_hits, key=arche_hits.get) if arche_hits else "self"
    next_rite = LOCKED_MYTH["emotion_to_rite"].get(emotion, "self_mountaintop_ritual")

    record = {
        "ts": date.isoformat(),
        "dream_text": text,
        "symbols": json.dumps(symbols),
        "emotion": emotion,
        "primary_archetype": primary,
        "next_ritual": next_rite
    }
    _log_dream(record)
    return record


def _extract_symbols(text: str) -> List[str]:
    text_l = text.lower()
    all_symbols = []
    for arch, sym_list in LOCKED_MYTH["archetypes"].items():
        for sym in sym_list:
            if re.search(rf"\b{sym}\b", text_l):
                all_symbols.append(sym)
    return list(set(all_symbols))


def _detect_emotion(text: str) -> str:
    # very light keyword map
    if re.search(r"\b(angry|rage|furious)\b", text.lower()):
        return "anger"
    if re.search(r"\b(yearning|longing|miss)\b", text.lower()):
        return "yearning"
    if re.search(r"\b(calm|peace|still)\b", text.lower()):
        return "peace"
    return "neutral"


def _map_to_archetypes(symbols: List[str]) -> Dict[str, int]:
    hits = {}
    for arch, sym_list in LOCKED_MYTH["archetypes"].items():
        hits[arch] = len(set(symbols).intersection(sym_list))
    return hits


# ------------------------------------------------------------------
# 3. Mountain logger
# ------------------------------------------------------------------
def _log_dream(record: Dict[str, Any]) -> None:
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute(
            "INSERT INTO entries (ts, dream_symbol, ritual_tag) VALUES (?,?,?)",
            (record["ts"], record["primary_archetype"], record["next_ritual"])
        )


# ------------------------------------------------------------------
# 4. Personal myth-cycle report
# ------------------------------------------------------------------
def myth_report(days: int = 30) -> Dict[str, Any]:
    start = (datetime.now(timezone.utc) - timedelta(days=days)).isoformat()
    with sqlite3.connect(DB_FILE) as conn:
        cur = conn.execute(
            "SELECT dream_symbol, COUNT(*) FROM entries "
            "WHERE ts >= ? AND dream_symbol IS NOT NULL GROUP BY dream_symbol",
            (start,)
        )
        arche_counts = {row[0]: row[1] for row in cur.fetchall()}

    dominant = max(arche_counts, key=arche_counts.get) if arche_counts else "self"
    next_rite = LOCKED_MYTH["emotion_to_rite"].get("neutral", "self_mountaintop_ritual")

    return {
        "window_days": days,
        "archetype_frequency": arche_counts,
        "dominant_archetype": dominant,
        "suggested_next_ritual": next_rite
    }


# ------------------------------------------------------------------
# 5. CLI – ingest dream or generate report
# ------------------------------------------------------------------
if __name__ == "__main__":
    import argparse, textwrap
    parser = argparse.ArgumentParser(description="Myth Portal – dream ingestion & report")
    sub = parser.add_subparsers(dest="cmd", required=True)

    ingest = sub.add_parser("ingest", help="Log a dream")
    ingest.add_argument("text", type=str, help='Dream text in quotes')

    report = sub.add_parser("report", help="Myth-cycle report")
    report.add_argument("--days", type=int, default=30, help="Look-back window")

    args = parser.parse_args()

    if args.cmd == "ingest":
        result = ingest_dream(args.text)
        print("Ingested – next ritual:", result["next_ritual"])
    elif args.cmd == "report":
        rep = myth_report(args.days)
        print(json.dumps(rep, indent=2))