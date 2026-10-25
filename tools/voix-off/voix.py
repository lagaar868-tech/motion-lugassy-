"""Génère la voix off (Piper, voix française masculine « tom », débit -5 %) et la place sur la timeline.

Prérequis : pip install piper-tts soundfile numpy
Modèle : vits-piper-fr_FR-tom-medium (releases GitHub de k2-fsa/sherpa-onnx, dossier « tts-models »)

Usage : python3 voix.py <fichier .onnx> script.json voix_brute.wav
"""
import json, os, sys, tempfile, wave
from piper import PiperVoice, SynthesisConfig

model, script, out = sys.argv[1:4]
voice = PiperVoice.load(model)
cfg = SynthesisConfig(length_scale=1.05, noise_scale=0.6, noise_w_scale=0.7)  # 1.05 = débit -5 %
tmp = tempfile.mkdtemp()
for line in json.load(open(script)):
    with wave.open(os.path.join(tmp, line['id'] + '.wav'), 'wb') as w:
        voice.synthesize_wav(line['text'], w, syn_config=cfg)
here = os.path.dirname(os.path.abspath(__file__))
os.system(f'python3 "{here}/mix.py" "{tmp}" "{script}" "{out}"')
