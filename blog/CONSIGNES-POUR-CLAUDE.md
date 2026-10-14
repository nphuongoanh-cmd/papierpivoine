# Consignes pour écrire un article du blog Papier Pivoine

À lire en entier avant d'écrire. Ces consignes servent à Claude (Cowork ou Chat)
quand Camélia lui demande un article pour papierpivoine.fr/blog/.

## Ce que tu produis

Un dossier dans `blog/`, contenant un fichier `article.md` et les images de l'article.

- **Nom du dossier** : la date de parution puis 2 à 5 mots-clés, en minuscules, sans
  accents, séparés par des tirets : `2026-10-18-ecrire-quand-on-est-fatiguee`.
  Les mots après la date deviennent l'adresse : `papierpivoine.fr/blog/ecrire-quand-on-est-fatiguee/`.
  Ne jamais renommer le dossier d'un article déjà en ligne.
- **Le fichier** suit exactement le modèle `blog/_modele/article.md` (en-tête entre
  deux lignes `---`, puis le texte).
- **Dans Cowork** : crée le dossier et le fichier directement. Ne touche à rien
  d'autre dans le dépôt (surtout pas à `source/`, `.github/` ni aux autres articles).
- **Dans Chat** : réponds avec le contenu complet de `article.md` dans un seul bloc
  de code, puis le nom du dossier à créer et la liste des images à y déposer.

## L'en-tête

```
---
titre: …
date: AAAA-MM-JJ
description: …
couverture: couverture.jpg
couverture_alt: …
themes: …, …
---
```

- `titre` : 60 caractères maximum. Il reprend les mots qu'une lectrice taperait dans
  Google (« comment arrêter de ruminer le soir », « journaling débutante »…).
- `date` : le jour de parution. Une date future programme l'article : il paraît
  seul ce matin-là.
- `description` : 70 à 160 caractères, une ou deux phrases. C'est l'aperçu affiché
  sur la page du blog et sous le lien dans Google. Elle donne envie, sans rien promettre de trop.
- `couverture` : le nom exact du fichier image, présent dans le dossier.
- `couverture_alt` : ce que montre l'image, en une phrase simple et concrète.
- `themes` : 1 ou 2 thèmes, séparés par une virgule. **Réutilise les thèmes déjà
  utilisés** par les autres articles de `blog/` (même orthographe) : chaque thème
  devient une page, il en faut peu et bien remplies. N'en crée un nouveau que si
  aucun ne convient.
- Facultatif : `pin: pin.jpg` (image verticale 1000 × 1500 pour Pinterest),
  `mis_a_jour: AAAA-MM-JJ`, `brouillon: oui` (l'article reste caché).

## Le texte

**Forme**
- Jamais de titre `#` dans le texte : le titre de l'en-tête suffit. Intertitres en `##`, sous-intertitres en `###`.
- 800 à 1 500 mots. Paragraphes courts (2 à 4 phrases).
- Images : seule sur sa ligne, `![description de l'image](nom-du-fichier.jpg "légende facultative")`.
  La description entre crochets est obligatoire. Le fichier doit être dans le dossier.
  Formats acceptés : JPEG, PNG ou WebP (pas de HEIC).
- Guillemets français « … ». Les espaces avant `: ; ! ?` sont gérés à la publication.
- `---` seul sur une ligne devient une petite pivoine : pour séparer la fin de l'article.

**Pour Google**
- Le premier paragraphe répond tout de suite à la question du titre, avec ses mots-clés.
- Les intertitres disent ce que contient la partie (pas de jeux de mots obscurs).
- 1 à 3 liens vers le site, là où ils aident vraiment :
  `/ecriture/` (Mental Léger, le programme d'écriture), `/semaine-offerte/` (la première
  semaine offerte), `/activites/` (les carnets), `/7-permissions-pivoine/`, `/apropos/`,
  ou un autre article : `/blog/<adresse>/`.
- Finir par une invitation douce, jamais insistante (souvent : la semaine offerte).

**La voix de Camélia**
- Elle écrit à la première personne et **tutoie** sa lectrice.
- Pour des femmes hypersensibles et introverties, qui ressentent tout et se rechargent au calme.
- Douceur, liberté, honnêteté : pas de pression, pas de « il faut », pas de compte à
  rebours, rien à réussir ni à finir. Des petits pas, à son rythme.
- Phrases simples et concrètes. Des exemples du quotidien (thé vert le matin, tisane
  le soir, le carnet, Bao son chat), sans en inventer : n'écris pas de souvenir ou de
  détail personnel que Camélia ne t'a pas donné. Demande-lui plutôt.
- C'est une pratique douce, pas un soin : aucune promesse de guérison, aucun conseil
  médical. Si le sujet touche à la souffrance psychique, rappeler qu'en France le
  3114 répond 24 h/24, gratuitement.

## Avant de rendre l'article

- [ ] Le dossier porte la date de parution et des mots-clés sans accents.
- [ ] L'en-tête a ses six lignes, entre deux `---`.
- [ ] Titre ≤ 60 caractères, description entre 70 et 160.
- [ ] Chaque image citée existe dans le dossier et a sa description.
- [ ] Les thèmes reprennent ceux des articles existants.
- [ ] Aucun `#` seul en début de ligne dans le texte.
- [ ] Rien d'inventé sur la vie de Camélia.

Ensuite, Camélia publie avec GitHub Desktop : Commit to main, puis Push origin.
