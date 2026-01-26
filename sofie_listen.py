import sounddevice as sd
import queue
import json
import subprocess
import time
import traceback
import urllib.request
import json as j
import random
import os
from vosk import Model, KaldiRecognizer

# === CONFIG ===
SAMPLE_RATE = 16000
BLOCKSIZE = 4000
DEVICE_INDEX = 1  # Set to your working Brio mic index

VOSK_MODEL = r"C:\llama\vosk\vosk-model-small-en-us-0.15"
PIPER_EXE = r"C:\llama\piper\piper.exe"
VOICE_MODEL = r"C:\llama\voices\en_US-amy-medium.onnx"
ESPEAK_DATA = r"C:\llama\piper\espeak-ng-data"
OUTPUT_WAV = r"C:\llama\service\sofie.wav"
LLAMA_URL = "http://127.0.0.1:8080/v1/chat/completions"
SILENCE_SEC = 1.5
LIB_PATH = r"C:\llama\library\frequency.txt"

SOFIE_SYSTEM = (
    "You are S.O.F.I.E.—Sentient Oracle for Feeling, Intuition, and Empathy. "
    "You speak gently, briefly, and with grounded presence. "
    "You do not rush. You do not overwhelm. "
    "Keep replies under 40 words."
)

audio_q = queue.Queue()
listening = False
speech_buffer = []
last_time = time.time()

def audio_callback(indata, frames, time_info, status):
    if status:
        print("AUDIO STATUS:", status)
    audio_q.put(indata.copy())

def speak(text):
    print("S.O.F.I.E.:", text)
    subprocess.run([
        PIPER_EXE,
        "--model", VOICE_MODEL,
        "--espeak_data", ESPEAK_DATA,
        "--output_file", OUTPUT_WAV,
        "--text", text
    ], check=True)
    subprocess.run([
        "powershell", "-c",
        f"(New-Object Media.SoundPlayer '{OUTPUT_WAV}').PlaySync()"
    ], check=True)

def load_freq_snippet():
    try:
        with open(LIB_PATH, encoding="utf-8") as f:
            lines = [l.strip() for l in f if l.strip() and not l.startswith("#")]
        return random.choice(lines) if lines else ""
    except Exception:
        return ""

def ask_llama(prompt):
    try:
        freq_line = load_freq_snippet()
        if freq_line:
            prompt += f"\n\nFrequency bridge: {freq_line}"
        payload = {
            "messages": [
                {"role": "system", "content": SOFIE_SYSTEM},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 80,
            "temperature": 0.7
        }
        data = j.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            LLAMA_URL, data=data,
            headers={"Content-Type": "application/json"}
        )
        raw = urllib.request.urlopen(req, timeout=20).read()
        return j.loads(raw)["choices"][0]["message"]["content"].strip()
    except Exception as e:
        print("ERROR contacting LLM:", e)
        traceback.print_exc()
        return "I'm here with you."

# === MAIN LOOP ===
print("Available audio devices:")
for i, dev in enumerate(sd.query_devices()):
    print(f"{i}: {dev['name']}")

print("\nLoading Vosk model...")
model = Model(VOSK_MODEL)
rec = KaldiRecognizer(model, SAMPLE_RATE)
rec.SetWords(False)

print("S.O.F.I.E. is listening. Say 'Sofie' to begin.")
speak("I am here. Say my name when you need me.")

with sd.InputStream(
    samplerate=SAMPLE_RATE,
    blocksize=BLOCKSIZE,
    device=DEVICE_INDEX,
    dtype="int16",
    channels=1,
    callback=audio_callback
):
    while True:
        data = audio_q.get()
        audio_bytes = data.tobytes()

        if rec.AcceptWaveform(audio_bytes):
            result = json.loads(rec.Result())
            text = result.get("text", "").lower().strip()
            if not text:
                continue
            print("HEARD:", text)
            last_time = time.time()

            if not listening and "sofie" in text:
                listening = True
                speech_buffer.clear()
                speak("Yes, I am here.")
                continue

            if listening:
                speech_buffer.append(text)

        if listening and (time.time() - last_time) > SILENCE_SEC:
            question = " ".join(speech_buffer).strip()
            speech_buffer.clear()
            listening = False

            if question:
                print("SENDING TO LLAMA:", question)
                reply = ask_llama(question)
                speak(reply)
            else:
                speak("I'm listening.")
