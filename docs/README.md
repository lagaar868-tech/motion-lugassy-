# Site vitrine — Lugassy Expertise

Site statique (HTML/CSS/JS, sans dépendance), prêt pour GitHub Pages.

```
docs/
├── index.html              Page unique : accueil, cabinet, expertises, pour qui, contact, pied de page
├── mentions-legales.html   Mentions légales, professions réglementées, RGPD
├── 404.html                Page « introuvable »
├── robots.txt, sitemap.xml Référencement
└── assets/
    ├── css/style.css       Styles (couleurs en haut du fichier)
    ├── js/main.js          Menu mobile, animations d'apparition, formulaire
    ├── img/                Logo SVG, favicon, image de partage, vignette vidéo
    └── video/              Vidéo de présentation (30 s)
```

## À compléter avant publication

Rechercher et remplacer dans `index.html`, `mentions-legales.html` et `assets/js/main.js` :

- `[TÉLÉPHONE]` et `[EMAIL]` (pour le lien `tel:`, écrire le numéro sans espaces : `tel:+33100000000`)
- Dans `mentions-legales.html`, les champs surlignés : forme juridique, capital, RCS, SIRET, TVA,
  n° d'inscription à l'Ordre, n° d'inscription H2A, assureur RCP
- Le **mot du dirigeant** (section « Le cabinet ») est une proposition à faire relire et valider par Judah Lugassy
- Option : remplacer le monogramme « JL » par une photo

## Formulaire de contact

GitHub Pages n'exécute pas de code serveur. Deux modes sont prévus :

1. **Par défaut** : à l'envoi, la messagerie du visiteur s'ouvre avec le message pré-rempli vers `[EMAIL]`.
2. **Recommandé** : envoi direct avec [Formspree](https://formspree.io), gratuit jusqu'à 50 messages par mois.
   Créer un formulaire sur Formspree, copier l'adresse fournie (`https://formspree.io/f/xxxx`) et la coller
   dans `index.html` : `<form … data-endpoint="https://formspree.io/f/xxxx">`.

## Mettre le site en ligne avec GitHub Pages (gratuit)

1. Fusionner la branche de travail dans `main` (ou utiliser directement la branche de travail à l'étape 3).
2. Sur GitHub, ouvrir le dépôt puis **Settings → Pages**.
3. **Source** : « Deploy from a branch ». **Branch** : `main` (ou la branche de travail), dossier **`/docs`**, puis **Save**.
4. Après 1 à 2 minutes, le site est en ligne à l'adresse affichée par GitHub
   (`https://<compte>.github.io/<dépôt>/`).

> GitHub Pages est gratuit pour un dépôt **public**. Pour un dépôt privé, il faut un compte GitHub Pro.

### Utiliser le nom de domaine www.lugassy-expertise.fr

1. **Settings → Pages → Custom domain** : saisir `www.lugassy-expertise.fr`, puis **Save**.
2. Chez le registraire du domaine (OVH, Gandi, IONOS…), créer un enregistrement DNS
   `CNAME` : `www` → `<compte>.github.io`.
3. Une fois le domaine validé, cocher **Enforce HTTPS**.

Les balises de référencement (canonique, sitemap, données structurées) pointent déjà vers
`https://www.lugassy-expertise.fr/`. Si le site reste sur l'adresse `github.io`, remplacer ce domaine
dans `index.html`, `mentions-legales.html`, `robots.txt` et `sitemap.xml`.

## Référencement local

- Titre et description ciblés « expert-comptable Paris 16 »
- Données structurées `AccountingService` (adresse, zone desservie, fondateur, services)
- Balises Open Graph pour un aperçu soigné sur LinkedIn et WhatsApp
- Conseil : créer ou mettre à jour la **fiche Google Business Profile** du cabinet avec la même adresse,
  le même téléphone et le lien vers le site. C'est le levier le plus fort pour apparaître sur
  « expert-comptable Paris 16 » dans Google Maps.
