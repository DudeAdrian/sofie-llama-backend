from vosk import Model, KaldiRecognizer
import wave, json

wf = wave.open(r"C:\llama\service\mic_test.wav", "rb")
model = Model(r"C:\llama\vosk\vosk-model-small-en-us-0.15")
rec = KaldiRecognizer(model, wf.getframerate())

text = ""

while True:
    data = wf.readframes(4000)
    if len(data) == 0:
        break
    if rec.AcceptWaveform(data):
        text += json.loads(rec.Result()).get("text", "") + " "

text += json.loads(rec.FinalResult()).get("text", "")
print(text)
