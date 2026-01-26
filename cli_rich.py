#!/usr/bin/env python3
"""
cli_rich.py  |  Pretty terminal for SOFIE
------------------------------------------
pip install rich
"""

from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from rich.text import Text
from core_sofie import SofieCore
from llama_bridge import LlamaBridge
from audio_engine import play_tone
import logging

logging.basicConfig(level=logging.INFO, format="%(levelname)s | %(message)s")
console = Console()


def main():
    core = SofieCore()
    llama = LlamaBridge()
    console.print(Panel("🌿  SOFIE  –  Evidence-Based Wellness Companion", style="green bold"))

    while True:
        user = Prompt.ask("\n[bold cyan]You[/]")
        if user.lower() in {"exit", "quit"}:
            break

        # ----- evidence summary (crash-proof) -----
        hits = core.query(user, top_k=2)
        if hits:
            ev_text = "\n".join(
                f"• {h['data'].get('label', h['data'].get('name', ''))}  "
                f"PMID:{h['data']['evidence'][0]['studyId']}"
                for h in hits if 'evidence' in h['data']   # safety filter
            ) if any('evidence' in h['data'] for h in hits) else "• No peer-reviewed data – general wellness advice"
            console.print(Panel(ev_text, title="Evidence", border_style="dim"))

        # ----- LLM reply -----
        with console.status("[bold green]Thinking...") as status:
            reply = llama.chat(user)
        console.print(Panel(reply, title="SOFIE", border_style="green"))

        # ----- optional tone -----
        if any("tone" in user.lower() or "frequency" in user.lower() for h in hits):
            hz = hits[0]["data"]["hz"]
            console.print(f"[dim]Playing {hz} Hz for 10 s...[/dim]")
            play_tone({"hz": hz, "duration_s": 10, "volume_db": -25})


if __name__ == "__main__":
    main()