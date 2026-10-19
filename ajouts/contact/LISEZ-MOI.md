# Formulaire de contact (page À propos)

Le formulaire de la page À propos remplace Tally. Chaque message :
- est enregistré dans un tableau Google Sheets à ton nom (onglet « Messages ») ;
- t'arrive par e-mail sur camelia@camelianguyen.fr. Tu cliques sur « Répondre » et tu écris directement à la personne.

Le fichier `Code.gs` est le petit programme qui tourne chez Google. Tu l'installes une seule fois (environ 5 minutes).

## Installation

1. Sur https://sheets.google.com, crée un tableau vide et nomme-le par exemple « Messages du site ».
2. Dans le tableau, ouvre le menu **Extensions › Apps Script**.
3. Efface le contenu de `Code.gs`, colle tout le contenu du fichier `Code.gs` d'ici, puis clique sur l'icône de disquette (Enregistrer).
4. En haut à droite, clique sur **Déployer › Nouveau déploiement**.
   - Roue dentée « Sélectionner le type » : **Application Web**.
   - Exécuter en tant que : **Moi**.
   - Qui a accès : **Tout le monde**.
   - Clique sur **Déployer**.
5. Google demande une autorisation. Clique sur **Autoriser l'accès** et choisis ton compte.
   Si un écran affiche « Google n'a pas validé cette application », clique sur **Paramètres avancés**, puis sur **Accéder à … (non sécurisé)**. C'est normal : l'application est la tienne et seule toi l'utilises.
6. Copie l'**URL de l'application Web**. Elle commence par `https://script.google.com/macros/s/` et se termine par `/exec`.
7. Envoie-moi cette adresse. Je la mets dans la page (`CONTACT_URL` dans `source/apropos/index.html`).

Pour vérifier, ouvre l'adresse dans ton navigateur. Elle doit afficher « Formulaire de contact Papier Pivoine : en ligne. ».

## Si tu modifies Code.gs plus tard

Va dans **Déployer › Gérer les déploiements**, clique sur le crayon, puis choisis Version : **Nouvelle version** et clique sur **Déployer**. Comme ça, l'adresse ne change pas.

## Protections

- Un champ piège, invisible pour les gens, arrête la plupart des robots.
- Une même adresse e-mail peut envoyer au maximum 5 messages par heure.
- Les longueurs sont limitées : prénom 80 caractères, e-mail 200, message 5 000.
- Si un texte commence par `=`, `+`, `-` ou `@`, il est enregistré comme du simple texte, jamais comme une formule.
