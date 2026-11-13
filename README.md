# Bolzo.ch

<img src="marque/logo-bolzo-rouge.svg" alt="Bolzo.ch" width="320">

Boutique en ligne suisse, en français et en allemand, prix en CHF.

## Produits

| Produit | Dossier | Statut |
|---|---|---|
| **KLARSHIT** : brosse anti-film gras pour vitres de voiture | [`klarshit/`](klarshit/) | Page de démonstration prête, version Shopify prête |

## En ligne

https://jonlekern.github.io/Bolzo.ch/ : la page d'accueil de la boutique.
La page KLARSHIT est sur https://jonlekern.github.io/Bolzo.ch/klarshit/

## Marque

Le logo et ses règles sont dans [`marque/`](marque/) : Overshoot Gentle Breeze,
en rouge `#d3121b`.

## Organisation

- **Un dossier par produit.** Chaque produit a sa page (`index.html`), ses images,
  ses polices et sa version Shopify (`shopify/`).
- **Les règles et la charte graphique de chaque produit** sont dans le README de
  son dossier. Pour KLARSHIT : [`klarshit/README.md`](klarshit/README.md).
- **Mettre une page sur Shopify** : suivre le guide du produit, par exemple
  [`klarshit/shopify/SHOPIFY.md`](klarshit/shopify/SHOPIFY.md).

## Fichiers à la racine

| Fichier | Rôle |
|---|---|
| `index.html` | Page d'accueil de la boutique (FR/DE) : présentation, produits, pourquoi Bolzo, FAQ |
| `assets/` | Polices (Overshoot, Malabard et leurs licences) et images de la page d'accueil |
| `.nojekyll` | Réglage technique pour GitHub Pages |
| `.gitignore` | Fichiers système à ne pas envoyer sur GitHub |

## À ne jamais mettre ici

Ce repo est public. Pas de nom de fournisseur, de prix d'achat, de marge, de mot
de passe ni de clé d'accès.
