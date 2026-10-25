# Lugassy Expertise — vidéo de présentation (30 s)

Vidéo rythmée en HTML/CSS/JS + GSAP, en deux formats :
**16:9 (1920×1080)** pour le site et LinkedIn, **9:16 (1080×1920)** pour Instagram, TikTok et les Shorts.

| Fichier | Rôle |
|---|---|
| `index.html` | L'animation (aperçu avec lecture, curseur et choix du format) |
| `logo.png`, `brand/` | Logo redessiné en vectoriel |
| `audio/voix-off.wav` | Voix off française, ajoutée automatiquement à l'export |
| `render.js` | Export MP4 image par image (Puppeteer ou Playwright + ffmpeg) |
| `vendor/`, `fonts/` | GSAP 3.12.5 et Montserrat embarqués : fonctionne hors ligne |
| `out/` | Vidéos exportées |

## Storyboard

| Temps | Scène | Ce qu'on voit |
|---|---|---|
| 0 – 4 s | **Le problème** | « Factures. TVA. Bilan. Paie. URSSAF. » tombent à l'écran comme des tampons, puis s'effacent : « Vous avez créé votre entreprise pour **ça** ? » |
| 4 – 7 s | **La promesse** | Un volet rouge balaie l'écran : « Concentrez-vous sur votre métier. On s'occupe du reste. » |
| 6,5 – 9,5 s | **Le cabinet** | Le volet repart et découvre le logo, révélé par une ligne rouge. « Expert-comptable & Commissaire aux comptes · Paris 16e · Île-de-France » |
| 9,3 – 19,4 s | **Comment ça marche ?** | Les 4 étapes du travail d'un cabinet, avec une barre de progression et une illustration animée par étape :<br>**01 Vous transmettez** (les documents tombent dans le dossier) · **02 On tient vos comptes** (les 12 mois se cochent) · **03 On analyse** (graphique qui monte, « Rentable ✓ ») · **04 On vous conseille** (marches + flèche, Fiscalité / Juridique / Croissance) |
| 19,4 – 26,7 s | **Pourquoi Lugassy Expertise ?** | Fond anthracite, 4 arguments qui se cochent : double qualification expert-comptable **et** commissaire aux comptes · un expert qui connaît votre dossier · depuis 2010 en Île-de-France · comptable, fiscal, audit, juridique sous un même toit |
| 26,7 – 30 s | **Appel à l'action** | Ouverture en cercle sur fond blanc : logo, « Vos chiffres en ordre. **Votre esprit libre.** », bouton « Prenons rendez-vous », site et adresse |

### Textes à valider par le cabinet

Les phrases s'appuient sur des faits connus (création en 2010, double qualification, 4 métiers,
Paris 16e). Deux formulations sont des **promesses de service** à confirmer avant diffusion :

- « Un interlocuteur direct, qui décroche et vous répond. »
- « Zéro retard, zéro pénalité. »

Tous les textes se modifient directement dans `index.html`.

## Logo redessiné

Le logo d'origine (carré rouge et « L » calligraphié blanc) était pixelisé. Il a été **vectorisé** :
mêmes proportions (95 × 88), même tracé, même rouge **#EF4035**, mais net à toutes les tailles.

| Fichier | Usage |
|---|---|
| `brand/logo-lugassy.svg` | Version vectorielle (site, impression, signature mail) |
| `brand/logo-lugassy-2000.png` | PNG haute définition (2000 px) |
| `logo.png` | Version utilisée par la vidéo |

Dans la vidéo, le symbole est accompagné du nom « LUGASSY EXPERTISE ». Toute l'animation reprend
automatiquement le rouge mesuré dans `logo.png`. Pour forcer une autre couleur : `&red=EF4035` dans
l'URL, ou `--red` en haut de `index.html`.

## Voix off

`audio/voix-off.wav` contient la voix off en français, calée sur l'animation. `render.js` l'ajoute
automatiquement aux MP4.

Texte lu (minutage dans `tools/voix-off/script.json`) :

> Factures, TVA, bilan, paie, URSSAF… Vous avez créé votre entreprise pour ça ?
> Concentrez-vous sur votre métier. On s'occupe du reste.
> Lugassy Expertise, à Paris.
> Comment ça marche ? Vous nous transmettez vos pièces. On tient vos comptes, et on déclare à temps.
> On analyse vos chiffres. Et on vous conseille, à chaque décision.
> Pourquoi Lugassy Expertise ? Expert-comptable et commissaire aux comptes.
> Un expert qui connaît votre dossier. Depuis deux mille dix.
> Vos chiffres, en ordre. Votre esprit, libre.

Voix de synthèse gratuite (Kokoro, voix française « siwis », licence Apache 2.0).
**Pour un rendu plus haut de gamme**, faire enregistrer ce texte par un comédien voix-off ou une
voix de synthèse premium (ElevenLabs, Runway…), puis remplacer `audio/voix-off.wav` (30 s) et
relancer `npm run render`.

Pour régénérer la voix de synthèse : `pip install kokoro-onnx soundfile`, télécharger
`kokoro-v1.0.onnx` et `voices-v1.0.bin` (releases GitHub de *thewh1teagle/kokoro-onnx*), puis :

```bash
python3 tools/voix-off/vo.py <dossier-modèle> <dossier-sortie> tools/voix-off/script.json
python3 tools/voix-off/mix.py <dossier-sortie> tools/voix-off/script.json voix.wav
ffmpeg -i voix.wav -af "highpass=f=70,acompressor=threshold=-20dB:ratio=3:makeup=3,loudnorm=I=-16:TP=-1.5" -ar 48000 -ac 2 audio/voix-off.wav
```

## Aperçu

```bash
npm run preview          # puis http://localhost:8080  (ou ?format=916 pour le vertical)
```
Barre de contrôle : 16:9 / 9:16, pause, rejouer, curseur. Espace = lecture/pause.

## Export MP4 — étapes

1. Installer **Node.js 18+** et **ffmpeg**
   - macOS : `brew install node ffmpeg`
   - Windows : `winget install OpenJS.NodeJS Gyan.FFmpeg`
2. Dans le dossier du projet : `npm install` (installe Puppeteer et son Chromium)
3. `npm run render`
   → `out/lugassy-16x9.mp4` et `out/lugassy-9x16.mp4` (H.264, 30 i/s, ~2 min de calcul)

Options : `node render.js --format 916` (un seul format), `--fps 60`.

**Principe :** le script ouvre la page dans un Chrome sans fenêtre, met la timeline GSAP en pause,
puis avance image par image (`seek(t)`), fait une capture et l'envoie à ffmpeg.
Résultat fluide et identique à chaque export, quelle que soit la puissance de la machine.

**Alternative sans code :** ouvrir l'aperçu en plein écran et l'enregistrer avec OBS ou
l'enregistreur d'écran du Mac — plus simple, mais moins net et parfois saccadé.

## Modifier

- Textes : directement dans `index.html` (sections commentées).
- Rythme : les temps (en secondes) sont le dernier argument de chaque `tl.to(...)`.
- Durée totale : `DURATION = 30`.
- Musique : pas encore de fond musical. Pour en mixer un sous la voix : `ffmpeg -i out/lugassy-16x9.mp4 -i musique.mp3 -filter_complex "[1:a]volume=0.18[m];[0:a][m]amix=inputs=2:duration=first" -c:v copy out/final.mp4`.
