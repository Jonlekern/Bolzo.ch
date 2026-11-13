# Brancher ChatGPT sur Bolzo.ch

Pour le pote de Johnny : comment relier ta session ChatGPT à ce repo, puis
quoi lui dire au début.

Les menus de ChatGPT changent souvent. Si un nom ne correspond pas exactement,
cherche le plus proche.

## 1. Avoir accès au repo

Johnny t'invite sur GitHub (Settings → Collaborators → Add people sur
`Jonlekern/Bolzo.ch`). Accepte l'invitation reçue par e-mail.

## 2. Relier ChatGPT à GitHub

**Pour lire le repo et en discuter**
1. Dans ChatGPT : Paramètres → Applications / Connecteurs → **GitHub** →
   Connecter.
2. Autorise l'accès à ton compte GitHub.
3. Dans une conversation, active GitHub et demande-lui de lire
   `Jonlekern/Bolzo.ch`.

**Pour qu'il modifie les fichiers lui-même : Codex**
1. Va sur https://chatgpt.com/codex et connecte GitHub.
2. Choisis le repo `Jonlekern/Bolzo.ch`.
3. Codex travaille sur une branche et propose ses changements en pull request.
   Johnny valide.

**Le repo n'apparaît pas dans la liste ?** C'est le repo de Johnny : il doit
autoriser l'application ChatGPT sur son compte GitHub, dans
https://github.com/settings/installations, en lui donnant accès à `Bolzo.ch`.

## 3. Message à coller au début de chaque session

> Tu travailles sur le repo GitHub `Jonlekern/Bolzo.ch`, une boutique suisse en
> français et en allemand. Avant toute chose, lis `README.md` à la racine, puis
> `klarsicht/README.md` (charte graphique et règles de la page produit). Pour
> Shopify, lis `klarsicht/shopify/SHOPIFY.md`.
> Règles : ne change que ce que je te demande, garde chaque texte en FR et en
> DE, pas d'emoji, n'enlève pas l'étiquette « Exemple » des avis, ne mets
> jamais d'infos fournisseur ni de prix d'achat (le repo est public).
> Travaille sur une branche et ouvre une pull request. Dis-moi en une liste ce
> que tu as changé.

## 4. Sans connecteur

Copie le fichier à modifier dans ChatGPT, avec le message ci-dessus et le
README concerné. Recolle le résultat sur GitHub avec le crayon (Edit), puis
« Commit changes » sur une nouvelle branche.

## Où sont les choses

| Chemin | Contenu |
|---|---|
| `index.html` | Page d'accueil Bolzo.ch |
| `klarsicht/` | Page produit KLARSICHT, images, vidéo, polices |
| `klarsicht/shopify/` | Version Shopify et son guide |
| `marque/` | Logo Bolzo.ch |
| `assets/` | Polices et images de la page d'accueil |
