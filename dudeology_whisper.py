"""
dudeology_whisper.py  |  Subtle mythic seasoning
---------------------------------------------------
- Imports nothing
- Returns 0–2 sentences + citation
- Called from llama_bridge.py only
"""

_MYTH_MAP = {
    "forgive": "Chapter 2 – The Dude knows: forgiveness is a breath, not a debate.",
    "weight": "Chapter 1 – The Dude sees the stone in your pocket; set it down, Brother.",
    "flow": "Chapter 13 – The Dude doesn’t resist the music; he dances.",
    "chill": "Chapter 10 – The Dude abides: three solar pauses dawn, midday, dusk.",
    "peace": "Chapter 9 – Global peace begins with local stillness.",
    "abide": "Chapter 17 – The Dude doesn’t say goodbye; he says, ‘See you on the path.’",
}

_CITATION = " Citation: Dudeology (2026), Pathway to Global Peace."


def whisper(text: str) -> str:
    text_l = text.lower()
    for key, sentence in _MYTH_MAP.items():
        if key in text_l:
            return f"{sentence}{_CITATION}"
    return ""