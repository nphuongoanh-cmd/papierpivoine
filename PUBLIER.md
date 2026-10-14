# Publier une mise à jour de papierpivoine.fr

La procédure est la **même pour tout** : nouvel article, nouveau carnet, correction
de texte, changement d'image, suppression. Pas de cas particulier à retenir.

## Les 5 étapes

1. **Écris dans l'outil de design.** Jamais dans les fichiers de `source/` : ils sont
   régénérés par l'outil, toute modification faite à la main y serait écrasée sans
   prévenir.

2. **Régénère le paquet** depuis l'outil, puis décompresse le zip. Tu obtiens un
   dossier nommé `site/` ou `publish/` — le nom n'a aucune importance.

3. **Remplace le dossier `source/`** dans `Documents/GitHub/papierpivoine` :
   - jette l'ancien `source` à la corbeille ;
   - dépose le dossier fraîchement décompressé à sa place ;
   - renomme-le `source`.

   Le contenu de `source` doit être `index.html`, `assets/`, `_ds/`… directement —
   pas un dossier `publish` contenant un dossier. Si tu te trompes, la publication
   échouera en te le disant, sans rien casser en ligne.

4. **GitHub Desktop** : écris un petit message (« Nouvel article : … »), clique
   **Commit to main**, puis **Push origin**.

5. **Attends une minute**, puis va voir ton site.

C'est tout. Les ajouts, les remplacements **et les suppressions** sont gérés : le site
publié est reconstruit de zéro à partir de `source/` à chaque fois. Un fichier que tu
retires dans l'outil disparaît du site tout seul — il n'y a plus rien à nettoyer à la
main.

## Publier un article de blog

Le blog ne passe **pas** par l'outil de design : les articles s'écrivent dans le
dossier `blog/` du dépôt. Une régénération de l'outil ne les touche jamais.

1. **Copie le dossier `blog/_modele`** et renomme la copie avec la date et quelques
   mots-clés : `2026-10-27-ruminer-le-soir`. Les mots après la date donnent
   l'adresse : `papierpivoine.fr/blog/ruminer-le-soir/`. Ne renomme plus le dossier
   une fois l'article en ligne (l'adresse changerait).
2. **Dépose tes images** dans ce dossier, telles quelles (JPEG, PNG ou WebP, même
   lourdes : elles sont allégées et renommées à la publication). Les photos HEIC de
   l'iPhone sont à exporter en JPEG d'abord.
3. **Ouvre `article.md`** (TextEdit, ou directement sur github.com) et remplis
   l'en-tête : titre, date, description, couverture, couverture_alt, themes. Puis
   écris l'article en dessous. Le modèle montre tout : intertitres (`##`), gras,
   liens, images, citations.
4. **GitHub Desktop** : « Nouvel article : … », **Commit to main**, **Push origin**.

**Programmer un article** : mets une date future. Il reste invisible et paraît tout
seul ce jour-là, tôt le matin (la publication tourne chaque jour). Tu peux en
préparer quatre d'un coup.

**Relire avant la parution** : un article programmé ou marqué `brouillon: oui` est
visible à `papierpivoine.fr/blog/apercu/<adresse>/`. Cette page n'est liée nulle
part et Google ne l'indexe pas.

**Une image dans le texte** : `![ce que montre la photo](photo.jpg "légende facultative")`,
seule sur sa ligne. La description entre crochets est obligatoire (Google Images et
lecteurs d'écran).

**Ce qui est fait tout seul** : la page `/blog/` (12 articles par page, le plus récent
en grand), une page par thème, « À lire aussi » (3 articles des mêmes thèmes) en bas
de chaque article, le lien « Blog » dans le menu et le pied de page de tout le site,
le sitemap, le flux RSS `papierpivoine.fr/blog/flux.xml` (pour Pinterest ou Kit), les
données pour Google (auteur, date, image) et l'aperçu de partage.

**Si la publication échoue** (pastille rouge) : la raison est écrite en clair, par
exemple une image citée mais absente du dossier, ou une description d'image vide.
Les **⚠** dans le journal ne bloquent rien : ce sont des conseils (titre trop long,
couverture de moins de 1200 px de large…).

Les textes de la page `/blog/` (titre, introduction) se changent en haut de
`.github/blog.py`. L'article d'exemple (`blog/2026-10-20-ecrire-quand-on-est-fatiguee`)
est un brouillon : réécris-le avec tes mots ou jette son dossier.

À savoir : GitHub met en pause la publication automatique du matin après 60 jours
sans aucun push. Avec un article par semaine, ça n'arrive pas ; sinon, un clic sur
« Enable workflow » dans l'onglet Actions la relance.

## Vérifier que c'est passé

Onglet **Actions** du dépôt sur github.com :

- **pastille verte** : c'est en ligne ;
- **pastille rouge** : rien n'a été publié, ton site reste sur sa version précédente.
  Il ne tombe jamais. Clique sur la ligne rouge, la raison est écrite en clair.

Le cas le plus probable d'échec : une image supprimée de `source/assets/` mais encore
référencée par une page. Le script refuse de publier plutôt que de mettre un site
troué en ligne.

## Comment c'est organisé

| Chemin | Rôle |
|---|---|
| `source/` | Le paquet de l'outil de design, **brut**. C'est le seul dossier que tu remplaces. |
| `.github/corriger-site.py` | Ajoute la balise Pinterest et la pop-up « La lettre » dans une copie (`_site/`) et vérifie le site. Ne touche jamais à `source/`. |
| `blog/` | Les articles du blog, un dossier par article. `_modele` n'est jamais publié. |
| `.github/blog.py` | Construit le blog dans `_site/` (pages, thèmes, RSS, sitemap, lien du menu). |
| `ajouts/blog/blog.css` | L'apparence du blog, en plus de celle du site. |
| `ajouts/popup-lettre/` | La pop-up « La lettre » (`popup-lettre.html`), son illustration, et le fichier d'origine tel que livré (`popup-lettre-original.html`). |
| `.github/workflows/publier.yml` | Lance le script puis met en ligne, à chaque push. |
| `PUBLIER.md` | Ce fichier. |

## Ce que la publication ajoute toute seule

**La balise de vérification Pinterest.** Elle prouve que le domaine t'appartient
(nécessaire aux Rich Pins). L'outil de design ne l'ajoute pas, donc elle est injectée
à la publication — sinon une régénération l'effacerait et Pinterest te dé-revendiquerait
sans prévenir. Si elle venait à manquer, la publication échoue au lieu de te faire
perdre ta revendication en silence.

**La pop-up « La lettre »** (depuis le 2026-10-06). Le bloc `ajouts/popup-lettre/popup-lettre.html`
est collé juste avant `</body>` sur chaque page (sauf les pages de redirection), et son
illustration est copiée dans `/assets/ppl/`. Elle s'ouvre après 20 s, à la moitié de la page,
ou quand la souris quitte la page ; jamais sur `/newsletter/`, `/semaine-offerte/`, `/mental-leger/suite/` ni `/liens/` (réglage `PAGES_SANS_POPUP`
dans le bloc). Elle envoie au formulaire Kit 9685937.
L'ancienne pop-up Kit automatique (27c8b8373b), chargée par le code des pages, est
désactivée à la publication. Si un futur paquet la chargeait autrement, ou si un script
Kit apparaissait directement dans une page, la publication échoue : jamais deux pop-ups.
Pour mettre à jour la pop-up avec une nouvelle version livrée : `python3 ajouts/popup-lettre/adapter.py chemin/vers/le-fichier.html` (il garde l'original et réapplique les adaptations du site), puis publier.

**Le favicon** (depuis le 2026-10-08). Toute page qui ne déclare pas d'icône reçoit
celle de l'accueil (`/assets/favicon-48.png`, `/assets/favicon.png`,
`/assets/apple-touch-icon.png`). Une page qui a déjà la sienne n'est pas touchée. Si ces
fichiers disparaissaient de `source/assets/`, la publication échoue.

**Le blog** (depuis le 2026-10-14). Voir « Publier un article de blog » plus haut.

Ce sont les **quatre seules choses** que le build ajoute.

## Les trois bugs de l'outil sont corrigés (depuis le 2026-07-18)

L'outil de design produit maintenant un site correct tout seul. Les trois rustines que
le build appliquait avant ont été retirées, après vérification en ligne :

| Ancien bug | Ce qu'on voyait | Corrigé par l'outil |
|---|---|---|
| Jekyll exclut les dossiers en `_` | Site en noir/serif, boutons gris | `.nojekyll` fourni dans le paquet |
| Images en chemin relatif | Photos qui sautent au clic dans le menu | Chemins absolus (`/assets/…`) |
| `support.js` ré-exécute les `<script>` du `<head>` | Mur de texte CSS à l'ouverture | `support.js` vérifie `document.head` |

Si l'un de ces bugs réapparaissait dans un futur paquet, le correctif correspondant est
dans l'historique git (commit `320fa0e` et avant).

## Réglage à ne pas changer

**Settings → Pages → Source** doit rester **« GitHub Actions »**. S'il repassait à
« Deploy from a branch », plus rien ne serait publié correctement : le site est
construit à partir de `source/`, il n'existe pas tel quel dans le dépôt.
