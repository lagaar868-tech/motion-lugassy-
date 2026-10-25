"""Génère les segments de voix off (Kokoro, voix française ff_siwis) et affiche leur durée."""
import json, sys
import soundfile as sf
from kokoro_onnx import Kokoro

D = sys.argv[1]
OUT = sys.argv[2]
segs = json.load(open(sys.argv[3]))
speed = float(sys.argv[4]) if len(sys.argv) > 4 else 1.0
k = Kokoro(f"{D}/kokoro-v1.0.onnx", f"{D}/voices-v1.0.bin")
for s in segs:
    ph = k.tokenizer.phonemize(s["text"], "fr-fr")
    audio, sr = k.create(s["text"], voice="ff_siwis", speed=s.get("speed", speed), lang="fr-fr")
    sf.write(f"{OUT}/{s['id']}.wav", audio, sr)
    print(f"{s['id']}: {len(audio)/sr:.2f}s  slot {s['slot']}s  | {ph}")
