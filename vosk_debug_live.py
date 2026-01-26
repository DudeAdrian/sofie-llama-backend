import sounddevice as sd
import queue
import json
from vosk import Model, KaldiRecognizer

SAMPLE_RATE = 16000
BLOCKSIZE = 4000
DEVICE_INDEX = 1  # Brio

model = Model(r"C:\llama\vosk\vosk-model-small-en-us-0.15")
rec = KaldiRecognizer(model, SAMPLE_RATE)
rec.SetWords(True)

audio_q = queue.Queue()

def callback(indata, frames, time_info, status):
    audio_q.put(bytes(indata))

with sd.RawInputStream(
    samplerate=SAMPLE_RATE,
    blocksize=BLOCKSIZE,
    device=DEVICE_INDEX,
    dtype="int16",
    channels=1,
    callback=callback
):
    print("🎤 Listening... Say anything.")
    while True:
        data = audio_q.get()
        if rec.AcceptWaveform(data):
            result = json.loads(rec.Result())
            print("HEARD:", result.get("text", ""))
