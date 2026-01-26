import sounddevice as sd, queue, json
from vosk import Model, KaldiRecognizer

MODEL_PATH = r"C:\llama\vosk\vosk-model-small-en-us-0.15"
SAMPLE_RATE = 48000          # device-friendly rate
DEVICE = 15
BLOCK = 48000                # 1 s blocks
model = Model(MODEL_PATH)
rec   = KaldiRecognizer(model, SAMPLE_RATE)

q = queue.Queue()
def cb(indata, frames, time, status):
    q.put(bytes(indata))

print("Listening… shout something now.")
with sd.RawInputStream(samplerate=SAMPLE_RATE, blocksize=BLOCK, device=DEVICE,
                       dtype="int16", channels=1, callback=cb):
    while True:
        data = q.get()
        if rec.AcceptWaveform(data):
            print("FINAL ->", json.loads(rec.Result())["text"])
        else:
            print("PARTIAL ->", json.loads(rec.PartialResult())["partial"])