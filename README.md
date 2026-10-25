# Lugassy Expertise — motion design (15 s)

Animation sobre en HTML/CSS/JS + GSAP, en deux formats :
**16:9 (1920×1080)** pour le site et LinkedIn, **9:16 (1080×1920)** pour les réseaux.

| Fichier | Rôle |
|---|---|
| `index.html` | L'animation (aperçu avec lecture, curseur et choix du format) |
| `logo.png` | **À ajouter** — le logo officiel (PNG, fond transparent de préférence) |
| `render.js` | Export MP4 image par image (Puppeteer ou Playwright + ffmpeg) |
| `vendor/`, `fonts/` | GSAP 3.12.5 et Montserrat embarqués : fonctionne hors ligne |
| `out/` | Vidéos exportées |

## Storyboard

| Temps | Scène | Mouvement |
|---|---|---|
| 0,0 – 2,9 s | **1. Révélation du logo** | Fond blanc. Une fine ligne rouge se trace depuis le centre, puis descend comme un scanner et révèle le logo (fondu + zoom 95 % → 100 %). La ligne se resserre en petit trait d'accent. |
| 2,9 – 5,9 s | **2. Identité** | Le logo remonte en en-tête. Une grille de lignes très fines se dessine. « LUGASSY EXPERTISE » sort d'un masque, l'interlettrage se resserre ; trait rouge ; « Expert-comptable & Commissaire aux comptes ». |
| 5,8 – 9,9 s | **3. Les 4 métiers** | Un par un (toutes les 0,7 s), icônes au trait rouge qui se dessinent : Expertise comptable (calculatrice) · Fiscalité (document %) · Audit & Commissariat aux comptes (loupe validée) · Juridique (balance). En ligne en 16:9, en liste en 9:16. |
| 5,0 – 12 s | **4. Éléments discrets** | En fond : une courbe rouge qui monte doucement avec des points-repères, une courbe grise en écho, des barres fines, des chiffres de type écriture comptable qui défilent (gris, faible opacité). |
| 9,9 – 12,6 s | **5. Accroche** | « Depuis **2010** » (l'année défile de 2000 à 2010), trait rouge, « aux côtés des entreprises d'Île-de-France ». |
| 12,6 – 15 s | **6. Signature** | Le logo revient au centre, le décor s'estompe. Trait rouge, `www.lugassy-expertise.fr`, « PARIS 16e ». Plan tenu ~1,5 s. |

Easing : `power2/power3` uniquement (pas de rebond sauf un très léger sur les points de la courbe).
Palette : rouge du logo · blanc · anthracite `#232528` · gris `#8A8D91`.

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
   → `out/lugassy-16x9.mp4` et `out/lugassy-9x16.mp4` (H.264, 30 i/s, ~1 min de calcul)

Options : `node render.js --format 916` (un seul format), `--fps 60`.

**Principe :** le script ouvre la page dans un Chrome sans fenêtre, met la timeline GSAP en pause,
puis avance image par image (`seek(t)`), fait une capture et l'envoie à ffmpeg.
Résultat fluide et identique à chaque export, quelle que soit la puissance de la machine.

**Alternative sans code :** ouvrir l'aperçu en plein écran et l'enregistrer avec OBS ou
l'enregistreur d'écran du Mac — plus simple, mais moins net et parfois saccadé.

## Modifier

- Textes : directement dans `index.html` (sections commentées 1 à 6).
- Rythme : les temps (en secondes) sont le dernier argument de chaque `tl.to(...)`.
- Durée totale : `DURATION = 15`.
- Pas de musique : à ajouter au montage, ou `ffmpeg -i out/lugassy-16x9.mp4 -i musique.mp3 -shortest -c:v copy -c:a aac out/final.mp4`.
