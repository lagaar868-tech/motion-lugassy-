# Lugassy Expertise — vidéo de présentation (30 s)

Vidéo rythmée en HTML/CSS/JS + GSAP, en deux formats :
**16:9 (1920×1080)** pour le site et LinkedIn, **9:16 (1080×1920)** pour Instagram, TikTok et les Shorts.

| Fichier | Rôle |
|---|---|
| `index.html` | L'animation (aperçu avec lecture, curseur et choix du format) |
| `logo.png` | **À ajouter** — le logo officiel (PNG, fond transparent de préférence) |
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

## Le logo et le rouge exact

1. Dépose le logo à la racine sous le nom **`logo.png`**.
2. Le rouge est **mesuré automatiquement dans le logo** (pixel rouge dominant) et appliqué à toute
   l'animation — la console de `render.js` affiche la valeur trouvée (`rouge: #…`).
3. Pour forcer une couleur : ajoute `&red=C8102E` à l'URL, ou modifie `--red` en haut de `index.html`.

Sans `logo.png`, un logo de remplacement (carré rouge « L » + LUGASSY EXPERTISE) s'affiche.
Les vidéos actuelles de `out/` ont été générées avec ce logo de remplacement.

> La mesure automatique demande que la page soit servie en http (c'est le cas avec `render.js`
> et `npm run preview`). En ouvrant `index.html` par double-clic, la couleur par défaut est utilisée.

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
- Pas de musique : à ajouter au montage, ou `ffmpeg -i out/lugassy-16x9.mp4 -i musique.mp3 -shortest -c:v copy -c:a aac out/final.mp4`.
