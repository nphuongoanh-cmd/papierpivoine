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
| `.github/corriger-site.py` | Répare les bugs de l'outil, dans une copie (`_site/`). Ne touche jamais à `source/`. |
| `.github/workflows/publier.yml` | Lance la réparation puis met en ligne, à chaque push. |
| `PUBLIER.md` | Ce fichier. |

## Ce que la publication ajoute toute seule

**La balise de vérification Pinterest.** Elle prouve que le domaine t'appartient
(nécessaire aux Rich Pins). L'outil de design ne permet pas de l'ajouter, donc elle
est injectée à la publication — sinon une régénération l'effacerait et Pinterest te
dé-revendiquerait sans prévenir. Si elle venait à manquer, la publication échoue au
lieu de te faire perdre ta revendication en silence.

Celle-là est **permanente** : ne la retire pas, contrairement aux trois correctifs
ci-dessous.

## Ce que la publication répare toute seule

Trois **bugs de l'outil de design**. Ils sont corrigés à la publication, sur une copie,
donc rien ne peut les écraser :

| Bug de l'outil | Ce qu'on voyait | Correctif appliqué |
|---|---|---|
| Jekyll exclut les dossiers en `_` | Site en noir/serif, boutons gris | Ajout de `.nojekyll` |
| Images en chemin relatif figé au chargement | Photos qui sautent au clic dans le menu | Ajout de `<base href="/">` |
| `support.js` ré-exécute les `<script>` du `<head>` | Mur de texte CSS à l'ouverture | Verrou sur l'embed Kit |

Le détail de chaque bug est expliqué en tête de `.github/corriger-site.py`.

## À demander à l'outil de design (à copier-coller tel quel)

> 1. **`support.js`** : ignorer un `<script>` déjà présent dans `document.head`.
>    Son Set `mounted` ne connaît que ses propres ajouts, donc tout embed tiers
>    déclaré dans le `<head>` s'exécute deux fois.
> 2. Émettre les chemins d'images en **absolu** (`/assets/…`), et non en relatif
>    figé selon la profondeur de l'URL d'arrivée.
> 3. Inclure **`.nojekyll`** dans le paquet livré.

Quand l'un d'eux est corrigé, le correctif correspondant peut être retiré du script —
sans risque : il est écrit pour ne rien faire si le bug a disparu. Les trois corrigés,
le script devient inutile.

## Réglage à ne pas changer

**Settings → Pages → Source** doit rester **« GitHub Actions »**. S'il repassait à
« Deploy from a branch », plus rien ne serait publié correctement : le site est
construit à partir de `source/`, il n'existe pas tel quel dans le dépôt.
