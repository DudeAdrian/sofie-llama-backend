import sounddevice as sd
try:
    with sd.RawInputStream(samplerate=48000, blocksize=48000, device=1,
                          dtype="int16", channels=1):
        print("STREAM OPENED – mic is live, press Ctrl-C")
        sd.sleep(5000)
except Exception as e:
    print("STREAM FAILED:", e)