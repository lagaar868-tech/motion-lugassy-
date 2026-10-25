"""
Musique originale « Lugassy Expertise » — 30 s, 80 BPM, Do majeur.

1 mesure = 3 s, 10 mesures = 30 s, calées sur l'animation :
  m1-2  (0-6 s)    accroche     : piano seul, puis entrée des cordes
  m3    (6-9 s)    logo         : la mineur
  m4-6  (9-18 s)   fonctionnement : progression qui avance
  m7-8  (18-24 s)  pourquoi     : violoncelle + cordes plus présentes
  m9    (24-27 s)  montée       : ré m7 → sol sus4 → sol, arpège ascendant
  m10   (27-30 s)  logo final   : résolution sur do (add9), qui s'éteint

Usage : python3 compose.py musique.mid
"""
import sys
import mido

BPM = 80
TPB = 480                       # ticks par noire
BAR = 4 * TPB
E = TPB // 2                    # croche

# Accords : (nom, basse, notes d'arpège, voicing cordes)
C   = ('C',   36, [48, 55, 60, 64, 67, 64, 60, 55], [60, 64, 67, 72])
G   = ('G',   43, [43, 50, 55, 59, 62, 59, 55, 50], [59, 62, 67, 71])
Am  = ('Am',  45, [45, 52, 57, 60, 64, 60, 57, 52], [60, 64, 69, 72])
F   = ('F',   41, [41, 48, 53, 57, 60, 57, 53, 48], [57, 60, 65, 69])
Dm7 = ('Dm7', 38, [38, 45, 50, 53, 57, 60], [57, 60, 62, 65])
Gs  = ('Gsus', 43, [43, 50, 55, 60, 62, 67], [60, 62, 67, 72])
Cf  = ('Cadd9', 36, [36, 43, 48, 55, 62, 64, 67, 72], [60, 62, 64, 67, 72])

PLAN = [C, G, Am, F, C, G, Am, F, None, Cf]   # la mesure 9 est écrite à part

# Mélodie du piano (haute, très clairsemée) : (mesure, temps, note, durée en noires, vélocité)
MELODY = [
    (0, 2, 76, 2, 48), (1, 0, 74, 4, 46),
    (2, 0, 72, 2, 46), (2, 2, 76, 2, 46), (3, 0, 77, 3, 46), (3, 3, 76, 1, 42),
    (6, 0, 76, 2, 46), (6, 2, 72, 2, 44), (7, 0, 77, 2, 48), (7, 2, 81, 2, 50),
    (8, 0, 79, 4, 54),
    (9, 0, 79, 2, 56), (9, 2, 76, 6, 50),
]


def build(path):
    mid = mido.MidiFile(ticks_per_beat=TPB)
    ev = {k: [] for k in ('piano', 'strings', 'cello')}

    def note(tr, t, n, d, v, ch):
        ev[tr].append((t, mido.Message('note_on', note=n, velocity=v, channel=ch)))
        ev[tr].append((t + d, mido.Message('note_off', note=n, velocity=0, channel=ch)))

    def cc(tr, t, c, v, ch):
        ev[tr].append((t, mido.Message('control_change', control=c, value=int(max(0, min(127, v))), channel=ch)))

    # Réglages des instruments : piano (0), cordes lentes (49), violoncelle (42)
    for tr, ch, prog, vol, rev, cho in (('piano', 0, 0, 100, 72, 10), ('strings', 1, 49, 92, 95, 30), ('cello', 2, 42, 80, 80, 20)):
        ev[tr].append((0, mido.Message('program_change', program=prog, channel=ch)))
        cc(tr, 0, 7, vol, ch); cc(tr, 0, 91, rev, ch); cc(tr, 0, 93, cho, ch); cc(tr, 0, 10, {0: 60, 1: 70, 2: 56}[ch], ch)

    # Dynamique globale du piano par mesure (petite montée jusqu'au logo final)
    pv = [44, 46, 48, 50, 50, 52, 54, 57, 62, 58]

    for m, chord in enumerate(PLAN):
        t0 = m * BAR
        # Pédale de sustain renouvelée à chaque mesure
        cc('piano', t0, 64, 0, 0); cc('piano', t0 + 10, 64, 127, 0)
        if chord is None:
            continue
        name, bass, arp, voicing = chord
        if m < 9:
            for i, n in enumerate(arp):
                acc = 6 if i % 4 == 0 else 0
                note('piano', t0 + i * E, n, E * 3, pv[m] + acc, 0)
        else:
            # Accord final égrené puis tenu
            for i, n in enumerate(arp):
                note('piano', t0 + i * (TPB // 6), n, BAR * 2, 54 - i, 0)
        # Cordes : nappe tenue sur toute la mesure (entrée à la mesure 2)
        if m >= 1:
            for n in voicing:
                note('strings', t0, n, BAR - 20 if m < 9 else BAR + TPB * 2, 70, 1)
        # Violoncelle discret à partir de « Pourquoi Lugassy » (mesure 7)
        if m >= 6:
            note('cello', t0, bass if bass >= 36 else bass + 12, BAR - 30 if m < 9 else BAR * 2, 58 if m < 9 else 54, 2)

    # Mesure 9 (24-27 s) : ré m7 (2 temps) → sol sus4 (1 temps) → sol (1 temps), arpège ascendant
    t0 = 8 * BAR
    seq = [(Dm7, 0, 2), (Gs, 2, 2)]
    for (name, bass, arp, voicing), beat, beats in seq:
        n_notes = beats * 2
        for i in range(n_notes):
            note('piano', t0 + beat * TPB + i * E, arp[i % len(arp)] + (12 if i >= len(arp) else 0), E * 3, 58 + i * 2, 0)
        for n in voicing:
            note('strings', t0 + beat * TPB, n, beats * TPB - 20, 76, 1)
        note('cello', t0 + beat * TPB, bass, beats * TPB - 30, 62, 2)
    # Résolution sus4 → tierce sur le dernier temps (sol)
    note('strings', t0 + 3 * TPB, 71, TPB - 20, 72, 1)

    for m, beat, n, d, v in MELODY:
        note('piano', m * BAR + beat * TPB, n, int(d * TPB), v, 0)

    # Expression des cordes (CC11) : entrée douce, crescendo vers le logo, fondu final
    for i in range(0, 10 * BAR + 1, TPB // 4):
        bar = i / BAR
        if bar < 1:
            x = 0
        elif bar < 2.5:
            x = 25 + (bar - 1) / 1.5 * 50          # entrée
        elif bar < 6:
            x = 75
        elif bar < 9:
            x = 75 + (bar - 6) / 3 * 35            # montée
        else:
            x = 110 - (bar - 9) * 70               # s'éteint
        cc('strings', i, 11, x, 1)
        cc('cello', i, 11, 60 + (35 if 6 <= bar < 9 else 10), 2)

    for name in ('piano', 'strings', 'cello'):
        tr = mido.MidiTrack(); mid.tracks.append(tr)
        if name == 'piano':
            tr.append(mido.MetaMessage('set_tempo', tempo=mido.bpm2tempo(BPM), time=0))
            tr.append(mido.MetaMessage('time_signature', numerator=4, denominator=4, time=0))
        last = 0
        for t, msg in sorted(ev[name], key=lambda x: (x[0], x[1].type == 'note_on')):
            tr.append(msg.copy(time=t - last)); last = t
    mid.save(path)
    print('OK', path, f'{mid.length:.2f}s')


if __name__ == '__main__':
    build(sys.argv[1] if len(sys.argv) > 1 else 'musique.mid')
