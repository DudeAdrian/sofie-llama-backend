#!/usr/bin/env python3
"""
audio_engine.py  |  SOFIE tone generator (sounddevice + numpy)
pip install sounddevice numpy
"""
import numpy as np
import sounddevice as sd
from typing import Dict, Any


def play_tone(cmd: Dict[str, Any]) -> None:
    hz = float(cmd["hz"])
    duration = int(cmd.get("duration_s", 600))
    vol_db = float(cmd.get("volume_db", -25))  # dB FS
    fs = 44_100
    t = np.linspace(0, duration, int(fs * duration), False)
    wave = 0.8 * (10 ** (vol_db / 20)) * np.sin(2 * np.pi * hz * t)
    sd.play(wave, samplerate=fs)
    sd.wait()


if __name__ == "__main__":
    play_tone({"hz": 432, "duration_s": 5, "volume_db": -25})