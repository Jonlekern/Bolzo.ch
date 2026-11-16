# Bolzo.ch sur Shopify

Ce dossier contient le site prêt pour un thème Shopify :
- **l'accueil Bolzo.ch** (`sections/bolzo-accueil.liquid`)
- **la page produit KLARSICHT** (`sections/klarsicht-produit.liquid`)
- **les pages À propos, Contact, Livraison et retours** (`sections/bolzo-*.liquid`)
- **les textes légaux** Impressum, CGV et Protection des données (`politiques/`)

Les quatre produits d'exemple (Kettenfreund, Siebfein, Rillenrein, Sohlenfit)
n'ont pas de page dans Shopify. Sur l'accueil, ils sont cachés par défaut.

L'en-tête, le bandeau et le pied de page sont ceux du thème : mets-y le logo
Bolzo.ch (`fichiers/logo-bolzo-rouge.png`) et le favicon
(`fichiers/favicon-180.png`, dans Personnaliser → Paramètres du thème → Logo).

## Contenu du dossier

| Dossier | Où ça va dans Shopify |
|---|---|
| `sections/` | Thème → Modifier le code → **Sections** |
| `templates/` | Thème → Modifier le code → **Templates** |
| `assets/` | Thème → Modifier le code → **Assets** (les 3 polices) |
| `fichiers/` | Contenu → **Fichiers** (images, vidéo, logos) |
| `politiques/` | Paramètres → **Politiques** (textes à coller, en DE et en FR) |
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

**6. Pages** : Boutique en ligne → Pages → Ajouter une page, trois fois. Le
contenu reste vide, c'est le modèle qui affiche la page.

| Titre | Adresse (handle) | Modèle de thème |
|---|---|---|
| Über uns | `a-propos` | `page.a-propos` |
| Kontakt | `contact` | `page.contact` |
| Versand und Rückgabe | `livraison-retours` | `page.livraison-retours` |

Les modèles `templates/page.*.json` et les sections `bolzo-a-propos`,
`bolzo-contact`, `bolzo-livraison-retours` s'ajoutent comme aux étapes 4 et 5.

**7. Politiques** : Paramètres → Politiques. Coller le texte de `politiques/` :

| Politique Shopify | Fichier |
|---|---|
| Mentions légales | `impressum-de.html` |
| Conditions générales de vente | `cgv-de.html` |
| Politique de confidentialité | `protection-des-donnees-de.html` |

Les versions `-fr.html` se collent dans la traduction française
(application Translate & Adapt). **Avant** : remplir les passages entre
crochets `[...]` et faire vérifier les textes par un juriste. Le mieux est de
les remplir dans les pages du repo, puis de relancer la construction.

**8. Menus** : Navigation → ajouter Über uns, Kontakt, Versand und Rückgabe et
les trois politiques au menu du pied de page.

**9. Réglages** (Personnaliser) :
- Accueil : choisir le produit KLARSICHT et l'adresse e-mail. Laisser **les
  produits d'exemple décochés**.
- KLARSICHT : coller le lien de la vidéo, l'adresse e-mail, et laisser **les
  avis d'exemple décochés** pour une vraie boutique.

**10. Langues** : la boutique est en allemand par défaut. Paramètres → Langues →
ajouter et publier le français.

## Vérifier

- [ ] Accueil : la carte KLARSICHT mène au produit et affiche « Dès CHF 29.90 ».
- [ ] Produit : chaque lot met le bon prix, « Ajouter au panier » met le bon
      lot dans le panier.
- [ ] Les photos, la vidéo et les polices s'affichent.
- [ ] En allemand, tous les textes sont en allemand ; en français, en français.
- [ ] Les liens entre les pages (Contact, Livraison, FAQ) fonctionnent.
- [ ] Plus aucun passage surligné en jaune ni entre crochets.
- [ ] Sur téléphone, rien ne dépasse.

Détails sur la page produit : `klarsicht/shopify/SHOPIFY.md`.

## Modifier une page ensuite

Modifier la page dans le repo (`index.html`, `klarsicht/index.html`,
`a-propos/`, `contact/`, `livraison-retours/`, `impressum/`, `cgv/`,
`protection-des-donnees/`), puis lancer :

```
python3 shopify/outils/construire.py
```

et recoller les sections dans Shopify. Ne pas modifier les fichiers de
`shopify/` à la main : ils sont écrasés à chaque construction.
