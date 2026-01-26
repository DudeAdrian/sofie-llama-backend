#!/usr/bin/env python3
"""
somatic_ledger.py  |  Living memory of peace
----------------------------------------------------
SQLite schema + importer for:
- HRV, lux-minutes, nitrate mg, forest-minutes, mood, dream-symbol
- Auto-ritual triggers (lunar, solar, geomagnetic)
- Peace-curve prediction (HRV → frequency prescription)
"""

import sqlite3
import json
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, Any, List

DB_FILE = Path(__file__).parent / "library" / "somatic_ledger.db"


# ----------------------------------------------------------
# 1. Mountain schema (locked)
# ----------------------------------------------------------
SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS entries (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    ts            TEXT NOT NULL UNIQUE,          -- ISO-8601
    hrv_rmssd_ms  REAL,
    lux_minutes   REAL,
    nitrate_mg    REAL,
    forest_min    REAL,
    mood_1_10     REAL,
    dream_symbol  TEXT,
    geomag_kp     REAL,
    lunar_phase   TEXT,
    ritual_tag    TEXT
);

CREATE TABLE IF NOT EXISTS rituals (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    ts            TEXT NOT NULL UNIQUE,
    name          TEXT NOT NULL,
    completed     INTEGER DEFAULT 0,
    auto_trigger  TEXT
);

CREATE VIEW peace_curve AS
SELECT date(ts) as day,
       AVG(hrv_rmssd_ms)  as avg_hrv,
       SUM(lux_minutes)   as total_lux,
       SUM(nitrate_mg)    as total_nitrate,
       SUM(forest_min)    as total_forest
FROM entries
GROUP BY day;
"""


# ----------------------------------------------------------
# 2. Mountain initialiser
# ----------------------------------------------------------
def init_ledger() -> None:
    with sqlite3.connect(DB_FILE) as conn:
        conn.executescript(SCHEMA_SQL)
    print("Mountain memory initialised –", DB_FILE)


# ----------------------------------------------------------
# 3. Peace-entry importer
# ----------------------------------------------------------
def log_entry(data: Dict[str, Any]) -> None:
    keys = ["ts", "hrv_rmssd_ms", "lux_minutes", "nitrate_mg",
            "forest_min", "mood_1_10", "dream_symbol",
            "geomag_kp", "lunar_phase", "ritual_tag"]
    ts = data.get("ts", datetime.now(timezone.utc).isoformat())
    row = [ts] + [data.get(k) for k in keys[1:]]
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute(
            "INSERT OR REPLACE INTO entries "
            "(ts, hrv_rmssd_ms, lux_minutes, nitrate_mg, forest_min, "
            "mood_1_10, dream_symbol, geomag_kp, lunar_phase, ritual_tag) "
            "VALUES (?,?,?,?,?,?,?,?,?,?)", row
    )


# ----------------------------------------------------------
# 4. Auto-ritual scheduler (example: HRV < 20 ms → 0.1 Hz breath)
# ----------------------------------------------------------
def auto_ritual(hrv: float) -> str:
    if hrv < 20:
        return "0.1_hz_breath"
    if hrv < 25 and lunar_phase() == "new":
        return "new_moon_intention_write"
    return ""


# ----------------------------------------------------------
# 5. Peace-curve predictor (simple linear)
# ----------------------------------------------------------
def predict_hrv(lux: float, nitrate: float, forest: float) -> float:
    # coefficients from meta-regression on locked JSON
    beta_lux = 0.12
    beta_nit = 0.08
    beta_for = 0.15
    intercept = 25
    return max(15, intercept + beta_lux * lux + beta_nit * nitrate + beta_for * forest)


# ----------------------------------------------------------
# 6. Lunar helper
# ----------------------------------------------------------
def lunar_phase() -> str:
    # simplified: 0 = new, 7 = first, 14 = full, 21 = last
    from datetime import date
    days = (date.today() - date(2000, 1, 6)).days % 29.53
    if days < 3.5:
        return "new"
    if days < 10.5:
        return "waxing"
    if days < 17.5:
        return "full"
    if days < 24.5:
        return "waning"
    return "new"


# ----------------------------------------------------------
# 7. CLI test
# ----------------------------------------------------------
if __name__ == "__main__":
    init_ledger()
    log_entry({
        "hrv_rmssd_ms": 18,
        "lux_minutes": 30,
        "nitrate_mg": 400,
        "forest_min": 120,
        "mood_1_10": 7,
        "dream_symbol": "mountain",
        "geomag_kp": 3.2,
        "ritual_tag": auto_ritual(18)
    })
    print("Peace-curve prediction:", predict_hrv(30, 400, 120))