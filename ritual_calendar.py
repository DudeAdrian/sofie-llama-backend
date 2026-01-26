#!/usr/bin/env python3
"""
ritual_calendar.py  |  Auto-scheduler for peace-architecture rites
--------------------------------------------------------------------
- Lunar-phase, solar-season, geomagnetic & personal-memory triggers
- Outputs JSON trigger ready for cli_rich.py or any scheduler
- No external deps except Python stdlib
"""

import json
import sqlite3
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import List, Dict, Any

DB_FILE   = Path(__file__).parent / "library" / "somatic_ledger.db"
CAL_OUTPUT= Path(__file__).parent / "ritual_trigger.json"  # file watcher target


# ------------------------------------------------------------------
# 1. Astronomical & geophysical helpers
# ------------------------------------------------------------------
def lunar_phase(date: datetime) -> str:
    """0 = new, 7 = first, 14 = full, 21 = last"""
    days = (date.date() - datetime(2000, 1, 6).date()).days % 29.53
    if days < 3.5:   return "new"
    if days < 10.5:  return "waxing"
    if days < 17.5:  return "full"
    if days < 24.5:  return "waning"
    return "new"


def solar_season(date: datetime) -> str:
    m = date.month
    if m in [12, 1, 2]:   return "winter"
    if m in [3, 4, 5]:    return "spring"
    if m in [6, 7, 8]:    return "summer"
    return "autumn"


def geomag_kp_est() -> float:
    """Simplified: fetch from API in real impl; here return 2.5 (quiet)"""
    return 2.5


def personal_hrv_7day_avg() -> float:
    """Read last 7 days HRV from ledger; fallback 25 ms"""
    try:
        with sqlite3.connect(DB_FILE) as conn:
            cur = conn.execute(
                "SELECT AVG(hrv_rmssd_ms) FROM entries WHERE ts >= datetime('now','-7 days')"
            )
            row = cur.fetchone()
            return row[0] if row[0] is not None else 25.0
    except Exception:
        return 25.0


# ------------------------------------------------------------------
# 2. Rule engine – returns list of ritual IDs
# ------------------------------------------------------------------
def generate_triggers(now: datetime) -> List[Dict[str, Any]]:
    triggers = []
    phase  = lunar_phase(now)
    season = solar_season(now)
    kp     = geomag_kp_est()
    hrv    = personal_hrv_7day_avg()

    # ----------- lunar -----------
    if phase == "new":
        triggers.append({"ritual": "new_moon_intention_write", "reason": "Lunar new phase"})
    if phase == "full":
        triggers.append({"ritual": "full_moon_gratitude_release", "reason": "Lunar full phase"})

    # ----------- solar -----------
    if season == "spring" and now.day <= 7:
        triggers.append({"ritual": "spring_equinox_fast", "reason": "Solar spring gate"})
    if season == "autumn" and now.day <= 7:
        triggers.append({"ritual": "autumn_equinox_reflection", "reason": "Solar autumn gate"})

    # ----------- geomagnetic -----------
    if kp > 5.0:
        triggers.append({"ritual": "geomag_storm_breath_01hz", "reason": "Kp > 5 geomagnetic storm"})

    # ----------- personal memory -----------
    if hrv < 20:
        triggers.append({"ritual": "hrv_rescue_01hz_breath", "reason": "7-day HRV < 20 ms"})
    if hrv > 40 and phase == "waxing":
        triggers.append({"ritual": "peak_hrv_creation_ritual", "reason": "High HRV + waxing moon"})

    return triggers


# ------------------------------------------------------------------
# 3. Public API – write JSON trigger file
# ------------------------------------------------------------------
def update_calendar() -> None:
    now   = datetime.now(timezone.utc)
    triggers = generate_triggers(now)
    payload = {
        "generated_at": now.isoformat(),
        "triggers": triggers
    }
    with CAL_OUTPUT.open("w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
    logging.getLogger("sofie").info("Ritual calendar updated – %s triggers", len(triggers))


# ------------------------------------------------------------------
# 4. CLI – run once or schedule via Windows Task Scheduler / cron
# ------------------------------------------------------------------
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s | %(message)s")
    update_calendar()