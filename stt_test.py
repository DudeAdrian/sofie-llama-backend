import sounddevice as sd
import numpy as np
from faster_whisper import WhisperModel
import tempfile
import scipy.io.wavfile as wav
import os

# -----------------------
# CONFIG
# -----------------------
DURATION = 5            # seconds to listen
SAMPLE_RATE = 16000    # whisper requirement
AUDIO_DEVICE_INDEX = 2 # confirmed working device ("default")

# -----------------------
# AUDIO SETUP
# -----------------------
sd.default.device = AUDIO_DEVICE_INDEX
sd.default.samplerate = SAMPLE_RATE

print("=== SOFIE STT TEST ===")
print("Recording for 5 seconds...")
print("Speak now.")

# -----------------------
# RECORD AUDIO
# -----------------------
audio = sd.rec(
    int(DURATION * SAMPLE_RATE),
    samplerate=SAMPLE_RATE,
    channels=1,
    dtype=np.int16
)
sd.wait()

print("Recording complete.")
print("Saving temporary WAV file...")

# -----------------------
# SAVE TEMP WAV
# -----------------------
with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
    wav.write(f.name, SAMPLE_RATE, audio)
    wav_path = f.name

print(f"WAV saved to: {wav_path}")
print("Loading Whisper model...")

# -----------------------
# LOAD MODEL
# -----------------------
model = WhisperModel(
    "base",
    device="cpu",
    compute_type="int8"
)

print("Transcribing...")

# -----------------------
# TRANSCRIBE
# -----------------------
segments, info = model.transcribe(wav_path)

print("\n=== TRANSCRIPTION RESULT ===")

found_text = False
for segment in segments:
    print(segment.text.strip())
    found_text = True

if not found_text:
    print("[No speech detected]")

# -----------------------
# CLEANUP
# -----------------------
try:
    os.remove(wav_path)
except Exception:
    pass

print("\n=== STT TEST COMPLETE ===")
