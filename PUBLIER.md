# Publier une mise à jour de papierpivoine.fr

## La marche à suivre

1. Écris ton article (ou ton produit) **dans l'outil de design**. Jamais ici : les
   fichiers de ce dépôt sont régénérés par l'outil, toute modification faite à la
   main y serait écrasée sans prévenir.
2. Régénère le paquet depuis l'outil. Tu obtiens un dossier `site/` ou `publish/`.
3. Copie son **contenu** à la racine de ce dépôt (les fichiers ET les dossiers).
4. Dans GitHub Desktop : écris un petit message, **Commit to main**, puis **Push origin**.
5. C'est tout. Le site est en ligne au bout d'une minute environ.

Tu peux suivre la publication dans l'onglet **Actions** du dépôt sur github.com.
Pastille verte = en ligne. Pastille rouge = rien n'a été publié, le site reste sur
sa version précédente (voir plus bas).

## Si tu supprimes quelque chose

Copier un nouveau paquet **ajoute et remplace, mais n'efface rien**. Si tu retires
un article ou une image dans l'outil, son fichier restera ici, orphelin. Supprime-le
à la main dans le Finder avant de committer — GitHub Desktop te montrera la
suppression.

(Le README du paquet de déploiement affirme que « git gère la suppression
automatiquement ». C'est faux.)

## Ce que la publication répare toute seule

Le site est publié par `.github/workflows/publier.yml`, qui lance
`.github/corriger-site.py`. Ce script recopie le site dans `_site/` et y applique
trois correctifs à des **bugs de l'outil de design**. Tes fichiers ne sont jamais
modifiés : une régénération n'écrase donc plus rien, et il n'y a plus aucune
rustine à réappliquer.

| Bug de l'outil | Ce qu'on voyait | Correctif appliqué à la publication |
|---|---|---|
| Jekyll exclut les dossiers en `_` | Site en noir/serif, boutons gris | Ajout de `.nojekyll` |
| Images en chemin relatif figé au chargement | Photos qui sautent au clic dans le menu | Ajout de `<base href="/">` |
| `support.js` ré-exécute les `<script>` du `<head>` | Mur de texte CSS à l'ouverture | Verrou sur l'embed Kit |

Le détail de chaque bug est expliqué en tête de `.github/corriger-site.py`.

## À demander à l'outil de design

Ces trois correctifs disparaîtront le jour où l'amont réglera ses bugs :

1. **`support.js`** : ignorer un `<script>` déjà présent dans `document.head`.
   Son Set `mounted` ne connaît que ses propres ajouts, donc tout embed tiers
   déclaré dans le `<head>` s'exécute deux fois. *C'est le plus rentable : une ligne.*
2. Émettre les chemins d'images en **absolu** (`/assets/…`), pas en relatif figé
   selon la profondeur de l'URL d'arrivée.
3. Inclure **`.nojekyll`** dans le paquet livré.

Quand l'un d'eux est corrigé, le correctif correspondant peut être retiré du
script — sans risque : il est déjà écrit pour ne rien faire si le bug a disparu.

## Si la publication échoue (pastille rouge)

Le script refuse de publier plutôt que de mettre un site cassé en ligne. Il vérifie
que chaque image référencée existe, que `<base>` est bien posé une seule fois par
page, que l'embed Kit est verrouillé, et que `CNAME`, `index.html`, `sitemap.xml`,
`robots.txt` et `.nojekyll` sont présents.

Clique sur la publication échouée dans l'onglet **Actions** : la raison est écrite
en clair. Le cas le plus probable est une image supprimée de `assets/` mais encore
référencée par une page.

## Réglage à ne pas changer

Dans **Settings → Pages**, la source doit rester **« GitHub Actions »**. Si elle
repasse à « Deploy from a branch », les correctifs ne seront plus appliqués et les
trois bugs reviendront d'un coup.
