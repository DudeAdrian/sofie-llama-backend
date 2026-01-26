import sounddevice as sd
import queue
import json
from vosk import Model, KaldiRecognizer

# === Configuration ===
SAMPLE_RATE = 48000
BLOCKSIZE = 8000
DEVICE_INDEX = None  # Default mic
MODEL_PATH = r"C:\llama\vosk\vosk-model-small-en-us-0.15"

# === Load Vosk ===
print("Loading model...")
model = Model(MODEL_PATH)
recognizer = KaldiRecognizer(model, SAMPLE_RATE)

# === Audio Queue ===
audio_q = queue.Queue()

def callback(indata, frames, time_info, status):
    if status:
        print("Status:", status)
    audio_q.put(bytes(indata))

# === Stream ===
print("Speak into the microphone...")
with sd.RawInputStream(samplerate=SAMPLE_RATE, blocksize=BLOCKSIZE,
                       device=DEVICE_INDEX, dtype='int16', channels=1,
                       callback=callback):
    while True:
        data = audio_q.get()
        if recognizer.AcceptWaveform(data):
            result = json.loads(recognizer.Result())
            text = result.get("text", "").strip()
            if text:
                print("You said:", text)
