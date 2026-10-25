#!/usr/bin/env bash
# Régénère toute la bande-son puis l'intègre aux vidéos.
# Prérequis : python3 (mido, piper-tts, soundfile, numpy), fluidsynth + soundfont FluidR3_GM, ffmpeg
# Usage : tools/mixage.sh <modèle fr_FR-tom-medium.onnx> [soundfont.sf2]
set -euo pipefail
cd "$(dirname "$0")/.."
MODEL="$1"; SF2="${2:-/usr/share/sounds/sf2/FluidR3_GM.sf2}"
TMP="$(mktemp -d)"

# 1. Voix off
python3 tools/voix-off/voix.py "$MODEL" tools/voix-off/script.json "$TMP/voix.wav"
ffmpeg -v error -y -i "$TMP/voix.wav" -af "aresample=48000,highpass=f=75,equalizer=f=160:t=q:w=1:g=1.5,equalizer=f=3200:t=q:w=1.4:g=2,acompressor=threshold=-22dB:ratio=3:attack=6:release=150:makeup=2,loudnorm=I=-16:TP=-2:LRA=7,aresample=48000" -ac 2 -t 30 audio/voix-off.wav

# 2. Musique (composition MIDI → FluidSynth)
python3 tools/musique/compose.py audio/musique.mid
fluidsynth -ni -q -F "$TMP/musique.wav" -r 48000 -g 0.55 -R 1 -C 1 "$SF2" audio/musique.mid
ffmpeg -v error -y -i "$TMP/musique.wav" -af "atrim=0:30,loudnorm=I=-26:TP=-6:LRA=11,aresample=48000,afade=t=in:st=0:d=1.2,afade=t=out:st=27.6:d=2.4" -ac 2 audio/musique.wav

# 3. Mixage : la musique baisse automatiquement sous la voix (ducking)
ffmpeg -v error -y -i audio/voix-off.wav -i audio/musique.wav -filter_complex \
  "[0:a]asplit=2[v][sc];[1:a][sc]sidechaincompress=threshold=0.025:ratio=7:attack=60:release=650:makeup=1[duck];[v][duck]amix=inputs=2:duration=longest:normalize=0,alimiter=limit=0.89:level=false[out]" \
  -map "[out]" -ar 48000 -t 30 audio/bande-son.wav

# 4. Remplace l'audio des vidéos existantes (sans réencoder l'image)
for f in 16x9 9x16; do
  ffmpeg -v error -y -i "out/lugassy-$f.mp4" -i audio/bande-son.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest -movflags +faststart "$TMP/$f.mp4"
  mv "$TMP/$f.mp4" "out/lugassy-$f.mp4"
done
echo "OK : out/lugassy-16x9.mp4 et out/lugassy-9x16.mp4"
