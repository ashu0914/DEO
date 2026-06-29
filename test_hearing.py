import queue
import sounddevice as sd
import json
from vosk import Model, KaldiRecognizer

# Load the model locally
model = Model("model")
rec = KaldiRecognizer(model, 16000)
q = queue.Queue()

def callback(indata, frames, time, status):
    q.put(bytes(indata))

print("\n🎤 TALK NOW! Say anything into your microphone...")
with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16',
                       channels=1, device=1, callback=callback):
    while True:
        data = q.get()
        if rec.AcceptWaveform(data):
            result = json.loads(rec.Result())
            print(f"👉 Text Detected: {result.get('text')}")
        else:
            partial = json.loads(rec.GetPartialResult())
            if partial.get("partial"):
                print(f"👂 Hearing partial: {partial.get('partial')}")