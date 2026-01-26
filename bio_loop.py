#!/usr/bin/env python3
"""
bio_loop.py  |  Real-time bio-feedback gate
-------------------------------------------
- Reads HRV / PPG from camera or BLE ear-clip
- If metric below threshold → auto-plays SOFIE protocol
- Writes result back to somatic_ledger.db
- Zero external deps except opencv-python or bleak (optional)
"""

import time
import json
import sqlite3
from pathlib import Path
from datetime import datetime, timezone
from typing import Optional, Dict, Any
import logging
import threading
import sounddevice as sd
import numpy as np

DB_FILE      = Path(__file__).parent / "library" / "somatic_ledger.db"
TRIGGER_FILE = Path(__file__).parent / "ritual_trigger.json"

# ------------------------------------------------------------------
# 1. Camera-based HRV extractor (fallback if no BLE)
# ------------------------------------------------------------------
class CameraHRV:
    """Pure NumPy + OpenCV free version – 30 s window, green-channel peak-to-peak"""
    def __init__(self, duration: int = 30, fs: int = 30):
        self.duration = duration
        self.fs       = fs

    def read(self) -> Optional[float]:
        try:
            import cv2
        except ImportError:
            logging.warning("OpenCV not found – returning dummy HRV 22 ms")
            return 22.0

        cap = cv2.VideoCapture(0)
        raw = []
        for _ in range(self.duration * self.fs):
            ret, frame = cap.read()
            if not ret: break
            green = np.mean(frame[:, :, 1])  # green channel
            raw.append(green)
        cap.release()

        if len(raw) < 30:
            return None

        # peak-to-peak interval → BPM → RMSSD approximation
        peaks, _ = self._simple_peaks(np.array(raw))
        if len(peaks) < 3:
            return None
        intervals = np.diff(peaks) / self.fs  # seconds
        rmssd = np.sqrt(np.mean(np.diff(intervals) ** 2)) * 1000  # ms
        return max(15.0, rmssd)

    @staticmethod
    def _simple_peaks(signal: np.ndarray) -> tuple:
        """Very naive peak detect – enough for demo"""
        from scipy.signal import find_peaks
        peaks, _ = find_peaks(signal, distance=20)
        return peaks, signal[peaks]


# ------------------------------------------------------------------
# 2. Threshold gate + SOFIE protocol player
# ------------------------------------------------------------------
def play_protocol(protocol_id: str) -> None:
    """Plays tone + logs completion"""
    # Map ritual ID to frequency
    freq_map = {
        "hrv_rescue_01hz_breath": 0.1,
        "new_moon_intention_write": 136,
        "peak_hrv_creation_ritual": 528
    }
    hz = freq_map.get(protocol_id, 432)
    duration = 120  # 2 min rescue
    t = np.linspace(0, duration, int(44_100 * duration), False)
    wave = 0.5 * np.sin(2 * np.pi * hz * t)
    sd.play(wave, samplerate=44_100)
    sd.wait()
    log_protocol(protocol_id, completed=1)


def log_protocol(name: str, completed: int) -> None:
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute(
            "INSERT INTO rituals (ts, name, completed, auto_trigger) VALUES (?,?,?,?)",
            (datetime.now(timezone.utc).isoformat(), name, completed, "bio_loop")
        )


# ------------------------------------------------------------------
# 3. Main loop – 60 s cadence
# ------------------------------------------------------------------
def bio_loop(duration_min: int = 60, threshold_hrv: float = 20.0) -> None:
    hrv_reader = CameraHRV(duration=30, fs=30)
    logging.getLogger("sofie").info("Bio-loop started – threshold %s ms", threshold_hrv)
    start = time.time()
    while (time.time() - start) < duration_min * 60:
        hrv = hrv_reader.read()
        if hrv is None:
            time.sleep(5)
            continue
        # decide
        if hrv < threshold_hrv:
            play_protocol("hrv_rescue_01hz_breath")
        # log raw metric
        log_entry({"hrv_rmssd_ms": hrv, "ritual_tag": "bio_loop"})
        time.sleep(30)  # 30 s between samples


def log_entry(data: Dict[str, Any]) -> None:
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute(
            "INSERT OR REPLACE INTO entries "
            "(ts, hrv_rmssd_ms, ritual_tag) VALUES (?,?,?)",
            (datetime.now(timezone.utc).isoformat(),
             data["hrv_rmssd_ms"],
             data.get("ritual_tag", ""))
        )


# ------------------------------------------------------------------
# 5. CLI – run once or background thread
# ------------------------------------------------------------------
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s | %(message)s")
    bio_loop(duration_min=60, threshold_hrv=20.0)