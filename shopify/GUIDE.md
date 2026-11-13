# Bolzo.ch sur Shopify

Ce dossier contient les deux pages prêtes pour un thème Shopify :
- **l'accueil Bolzo.ch** (`sections/bolzo-accueil.liquid`)
- **la page produit KLARSICHT** (`sections/klarsicht-produit.liquid`)

L'en-tête, le bandeau et le pied de page sont ceux du thème : mets-y le logo
Bolzo.ch (`fichiers/logo-bolzo-rouge.png`).

## Contenu du dossier

| Dossier | Où ça va dans Shopify |
|---|---|
| `sections/` | Thème → Modifier le code → **Sections** |
| `templates/` | Thème → Modifier le code → **Templates** |
| `assets/` | Thème → Modifier le code → **Assets** (les 3 polices) |
| `fichiers/` | Contenu → **Fichiers** (images, vidéo, logos) |
| `outils/construire.py` | Refait tout ce dossier depuis les pages du repo |

## Étapes

**0. Sauvegarde** : Boutique en ligne → Thèmes → ⋯ → **Dupliquer** le thème.
On travaille sur la copie.

**1. Produit** : créer le produit **KLARSICHT** (adresse `/products/klarsicht`)
avec l'option `Offre` et 3 variantes dans cet ordre :

| Ordre | Valeur | Prix | Prix avant réduction |
|---|---|---|---|
| 1 | `1 + 1` | 29.90 | vide |
| 2 | `4×` | 49.90 | 59.80 |
| 3 | `6×` | 64.90 | 89.70 |

**2. Fichiers** : téléverser tout `fichiers/` dans Contenu → Fichiers, **sans
changer les noms**. Copier le lien de `demo.mp4`.

**3. Polices** : téléverser les 3 fichiers de `assets/` dans le dossier Assets
du thème.

**4. Sections** : dans Sections, créer `bolzo-accueil` et `klarsicht-produit`,
et coller le contenu des fichiers du même nom.

**5. Modèles** :
- `templates/index.json` → remplace le modèle `index.json` du thème. C'est
  la page d'accueil : l'ancienne disparaît (d'où la sauvegarde de l'étape 0).
- `templates/product.klarsicht.json` → nouveau modèle produit `klarsicht`, puis
  dans la fiche du produit : Modèle de thème → `klarsicht`.

**6. Réglages** (Personnaliser) :
- Accueil : choisir le produit KLARSICHT et l'adresse e-mail.
- KLARSICHT : coller le lien de la vidéo, l'adresse e-mail, et laisser **les
  avis d'exemple décochés** pour une vraie boutique.

**7. Allemand** : Paramètres → Langues → ajouter et publier l'allemand.

## Vérifier

- [ ] Accueil : la carte KLARSICHT mène au produit et affiche « Dès CHF 29.90 ».
- [ ] Produit : chaque lot met le bon prix, « Ajouter au panier » met le bon
      lot dans le panier.
- [ ] Les photos, la vidéo et les polices s'affichent.
- [ ] En allemand, tous les textes sont en allemand.
- [ ] Sur téléphone, rien ne dépasse.

Détails sur la page produit : `klarsicht/shopify/SHOPIFY.md`.

## Modifier une page ensuite

Modifier `index.html` (accueil) ou `klarsicht/index.html` (produit), puis
lancer :

```
python3 shopify/outils/construire.py
```

et recoller les sections dans Shopify. Ne pas modifier les fichiers de
`shopify/` à la main : ils sont écrasés à chaque construction.
