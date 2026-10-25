"""Coupe les silences de chaque segment, les place sur la timeline et assemble la piste voix (30 s)."""
import json, subprocess, sys
import numpy as np
import soundfile as sf

seg_dir, script, out = sys.argv[1], sys.argv[2], sys.argv[3]
TOTAL = 30.0
segs = json.load(open(script))
sr = None
track = None
prev_end = 0.0
plan = []
for s in segs:
    a, r = sf.read(f"{seg_dir}/{s['id']}.wav")
    sr = sr or r
    if track is None:
        track = np.zeros(int(TOTAL * sr) + sr)
    thr = 0.01 * np.abs(a).max()
    idx = np.where(np.abs(a) > thr)[0]
    a = a[max(0, idx[0] - int(.03 * sr)): idx[-1] + int(.08 * sr)]
    start = max(s['at'], prev_end + 0.12)
    i = int(start * sr)
    track[i:i + len(a)] += a
    prev_end = start + len(a) / sr
    plan.append((s['id'], round(start, 2), round(prev_end, 2), s['text']))
for p in plan:
    print(f"{p[1]:6.2f} → {p[2]:6.2f}  {p[0]}")
if prev_end > TOTAL - 0.1:
    print('!! dépasse 30 s')
sf.write(out, track[:int(TOTAL * sr)], sr)
json.dump(plan, open(out + '.json', 'w'), ensure_ascii=False, indent=1)
