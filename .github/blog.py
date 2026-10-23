"""
Le blog de papierpivoine.fr (depuis le 2026-10-14), construit à la publication.

Les articles s'écrivent dans blog/, à la racine du dépôt, jamais dans source/ :
un dossier par article, avec un fichier article.md et ses images. Ce module
fabrique dans _site/ :

  /blog/                      la liste des articles (12 par page, puis /blog/page/2/…)
  /blog/<article>/            chaque article, avec « À lire aussi »
  /blog/theme/<thème>/        un thème, et tous ses articles
  /blog/flux.xml              le flux RSS (Pinterest, Kit…)
  /blog/apercu/<article>/     les brouillons et les articles programmés, pour les
                              relire : invisibles de Google et liés nulle part

Il ajoute aussi les articles au sitemap, et le lien « Blog » au menu et au pied
de page de chaque page du site, dès qu'un premier article est en ligne.

Un article dont la date est dans le futur reste en aperçu jusqu'à ce jour-là :
la publication tourne chaque matin (voir publier.yml), il paraît tout seul.

L'en-tête et le pied de page sont repris de /apropos/ (livré par l'outil de
design) : quand le menu change dans l'outil, le blog suit sans rien toucher.
"""

import html
import json
import os
import re
import shutil
import unicodedata
from datetime import date, datetime, time
from email.utils import format_datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import markdown
from PIL import Image, ImageOps

RACINE = Path(__file__).resolve().parent.parent
ARTICLES = Path(os.environ.get("BLOG_DOSSIER", RACINE / "blog"))
STYLE = RACINE / "ajouts" / "blog" / "blog.css"
PAGE_MODELE = "apropos/index.html"   # page dont on reprend l'en-tête et le pied de page

SITE = "https://papierpivoine.fr"
PARIS = ZoneInfo("Europe/Paris")
HEURE_DE_PARUTION = time(7, 0)        # heure affichée aux robots (RSS, Google)
PAR_PAGE = 12
THEME_MIN = 3                          # en dessous, une page de thème répète /blog/ : visible, mais pas dans Google
A_LIRE_AUSSI = 3

# Textes de la page /blog/ : à modifier ici.
BLOG_TITRE = "Blog · écriture douce et hypersensibilité · Papier Pivoine"
BLOG_DESCRIPTION = (
    "Chaque semaine, une idée simple pour écrire, souffler et vivre ta sensibilité "
    "plus légèrement. Par Camélia, de Papier Pivoine."
)
BLOG_SURTITRE = "Le blog"
BLOG_H1 = "Des mots doux pour les esprits <mark>pleins</mark>"
BLOG_INTRO = (
    "Chaque semaine, une idée simple pour écrire, souffler et vivre ta sensibilité "
    "plus légèrement."
)

IMAGES_ACCEPTEES = {".jpg", ".jpeg", ".png", ".webp"}
LARGEURS = (800, 1600)                 # tailles produites pour chaque image
LARGEUR_PARTAGE = 1200                 # image de partage et Google Discover
MOIS = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août",
        "septembre", "octobre", "novembre", "décembre"]

ORGANISATION = {
    "@type": "Organization", "@id": f"{SITE}/#organization", "name": "Papier Pivoine",
    "url": f"{SITE}/", "logo": {"@type": "ImageObject", "url": f"{SITE}/assets/favicon.png"},
}
AUTEUR = {
    "@type": "Person", "@id": f"{SITE}/#camelia", "name": "Camélia Nguyen",
    "alternateName": "Camélia", "url": f"{SITE}/apropos/",
}

LIEN_A_PROPOS = re.compile(r'<a href="/apropos/"([^>]*)>À propos</a>')
LIEN_BLOG = re.compile(r'<a href="/blog/"[^>]*>Blog</a>')
blog_en_ligne = False  # le lien « Blog » n'apparaît qu'avec un premier article en ligne

e = html.escape


# ── Petits outils ──────────────────────────────────────────────────────────

def en_slug(texte):
    t = unicodedata.normalize("NFKD", texte).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", t.lower()).strip("-")


def typo_fr(texte_html):
    """Espace insécable avant : ; ! ? » et après « (hors balises) : jamais de « ? » seul en début de ligne."""
    def corriger(m):
        t = re.sub(r"[ \u00a0]([:;!?»])", "\u00a0\\1", m.group(0))
        return re.sub(r"«[ \u00a0]?", "«\u00a0", t)
    return re.sub(r"(?<=>)[^<]+|^[^<]+", corriger, texte_html)


def date_fr(d):
    return f"{'1er' if d.day == 1 else d.day} {MOIS[d.month - 1]} {d.year}"


def horodatage(d):
    return datetime.combine(d, HEURE_DE_PARUTION, PARIS)


def aujourdhui():
    forcee = os.environ.get("BLOG_AUJOURDHUI")  # pour tester une date de parution
    return date.fromisoformat(forcee) if forcee else datetime.now(PARIS).date()


def lire_entete(texte):
    """Sépare l'en-tête (entre deux lignes ---) du texte de l'article."""
    m = re.match(r"﻿?\s*---[ \t]*\n(.*?)\n---[ \t]*\n(.*)", texte, re.S)
    if not m:
        return None, texte
    champs = {}
    for ligne in m.group(1).splitlines():
        if not ligne.strip() or ligne.lstrip().startswith("#"):
            continue
        cle, _, valeur = ligne.partition(":")
        champs[en_slug(cle).replace("-", "_")] = valeur.strip().strip('"').strip()
    return champs, m.group(2)


# ── Images ─────────────────────────────────────────────────────────────────

def ouvrir_image(chemin):
    img = Image.open(chemin)
    img = ImageOps.exif_transpose(img)  # photos de téléphone : bon sens
    if img.mode not in ("RGB", "RGBA"):
        img = img.convert("RGBA" if "transparency" in img.info or img.mode in ("LA", "P") else "RGB")
    return img


def redimensionner(img, largeur):
    if img.width <= largeur:
        return img
    return img.resize((largeur, round(img.height * largeur / img.width)), Image.LANCZOS)


def en_jpeg(img, largeur, cible):
    img = redimensionner(img, largeur)
    if img.mode == "RGBA":  # fond papier sous les dessins transparents
        fond = Image.new("RGB", img.size, (252, 246, 242))
        fond.paste(img, mask=img.split()[3])
        img = fond
    img.save(cible, "JPEG", quality=85, optimize=True, progressive=True)  # sans EXIF ni GPS
    return img.size


def produire_image(source, dossier, nom, url_dossier):
    """WebP en 800 et 1600 px de large (sans métadonnées). Renvoie de quoi écrire <img>."""
    img = ouvrir_image(source)
    variantes = []
    for largeur in sorted({min(l, img.width) for l in LARGEURS}):
        version = redimensionner(img, largeur)
        fichier = f"{nom}-{version.width}.webp"
        version.save(dossier / fichier, "WEBP", quality=82, method=6)
        variantes.append((version.width, version.height, fichier))
    w, h, principal = variantes[-1]
    return {
        "src": f"{url_dossier}{principal}",
        "srcset": ", ".join(f"{url_dossier}{f} {vw}w" for vw, _, f in variantes),
        "w": w, "h": h, "largeur_origine": img.width, "img": img,
    }


def balise_img(im, alt, sizes, classe="", paresseuse=True, pin=None):
    attributs = [
        f'src="{im["src"]}"', f'srcset="{im["srcset"]}"', f'sizes="{sizes}"',
        f'width="{im["w"]}"', f'height="{im["h"]}"', f'alt="{e(alt)}"',
    ]
    if classe:
        attributs.insert(0, f'class="{classe}"')
    attributs.append('loading="lazy" decoding="async"' if paresseuse else 'fetchpriority="high"')
    if pin:
        attributs.append(f'data-pin-media="{pin}"')
    return f"<img {' '.join(attributs)}>"


# ── Lecture des articles ───────────────────────────────────────────────────

class Article:
    pass


def lire_articles(erreurs, avertissements):
    articles = []
    if not ARTICLES.is_dir():
        return articles
    vus = {}
    for dossier in sorted(ARTICLES.iterdir()):
        if not dossier.is_dir() or dossier.name.startswith(("_", ".")):
            continue
        nom = f"blog/{dossier.name}"
        fichier = dossier / "article.md"
        if not fichier.exists():
            erreurs.append(f"{nom} : pas de fichier article.md dans ce dossier")
            continue
        champs, texte = lire_entete(fichier.read_text(encoding="utf-8"))
        if champs is None:
            erreurs.append(f"{nom}/article.md : l'en-tête doit commencer et finir par une ligne ---")
            continue

        a = Article()
        a.dossier, a.nom = dossier, nom
        a.slug = en_slug(re.sub(r"^\d{4}-\d{2}-\d{2}-?", "", dossier.name))
        manque = [c for c in ("titre", "date", "description", "couverture", "couverture_alt") if not champs.get(c)]
        if manque:
            erreurs.append(f"{nom}/article.md : il manque {', '.join(manque)} dans l'en-tête")
            continue
        if not a.slug:
            erreurs.append(f"{nom} : le nom du dossier doit contenir des mots (il donne l'adresse de l'article)")
            continue
        if a.slug in vus:
            erreurs.append(f"{nom} et {vus[a.slug]} donneraient la même adresse /blog/{a.slug}/")
            continue
        vus[a.slug] = nom
        try:
            a.date = date.fromisoformat(champs["date"])
            a.maj = date.fromisoformat(champs["mis_a_jour"]) if champs.get("mis_a_jour") else a.date
        except ValueError:
            erreurs.append(f"{nom}/article.md : date à écrire sous la forme 2026-10-20")
            continue

        a.titre = typo_fr(champs["titre"])
        a.description = typo_fr(champs["description"])
        a.couverture, a.couverture_alt = champs["couverture"], champs["couverture_alt"]
        a.vignette_alt_texte = champs.get("vignette_alt")
        a.pin = champs.get("pin")
        a.vignette = champs.get("vignette")            # image des cartes et du partage (3:2), sinon la couverture
        a.surligne = champs.get("titre_surligne")      # morceau du titre surligné, comme sur le site
        a.corps_html = champs.get("corps")             # corps déjà mis en page (HTML), au lieu du texte
        a.style = champs.get("style")                  # sa feuille de style, limitée à .briche
        for f in [x for x in (a.corps_html, a.style) if x]:
            if not (dossier / f).exists():
                erreurs.append(f"{nom} : fichier introuvable -> {f}")
        a.brouillon = champs.get("brouillon", "").lower() in ("oui", "yes", "true", "1")
        a.themes = []
        for t in re.split(r"[,;]", champs.get("themes", "")):
            if t.strip() and en_slug(t) not in [en_slug(x) for x in a.themes]:
                a.themes.append(t.strip())
        a.texte = texte

        if len(a.titre) > 60:
            avertissements.append(f"{nom} : titre long ({len(a.titre)} caractères), Google le coupera vers 60")
        if not 70 <= len(a.description) <= 160:
            avertissements.append(
                f"{nom} : description de {len(a.description)} caractères (idéal : 70 à 160, "
                "c'est le texte sous le lien dans Google)")
        if not a.themes:
            avertissements.append(f"{nom} : aucun thème (ligne themes:), « À lire aussi » sera moins juste")
        for image in [a.couverture] + [x for x in (a.pin, a.vignette) if x]:
            verifier_fichier_image(dossier / image, nom, erreurs)
        articles.append(a)
    return articles


def verifier_fichier_image(chemin, nom, erreurs):
    if not chemin.exists():
        erreurs.append(f"{nom} : image introuvable -> {chemin.name} (est-elle bien dans le dossier de l'article ?)")
        return False
    if chemin.suffix.lower() in (".heic", ".heif"):
        erreurs.append(f"{nom} : {chemin.name} est au format HEIC (iPhone). Exporte-la en JPEG.")
        return False
    if chemin.suffix.lower() not in IMAGES_ACCEPTEES:
        erreurs.append(f"{nom} : {chemin.name} n'est pas une image JPEG, PNG ou WebP")
        return False
    return True


# ── Rendu du texte ─────────────────────────────────────────────────────────

IMAGE_MD = re.compile(r'!\[([^\]]*)\]\(\s*<?([^)\s>]+)>?(?:\s+"([^"]*)")?\s*\)')


IMG_HTML = re.compile(r'<img\b[^>]*>')


def rendre_html(a, dossier_sortie, url_dossier, erreurs):
    """Corps déjà mis en page : les images du dossier deviennent des WebP allégés."""
    corps = (a.dossier / a.corps_html).read_text(encoding="utf-8")
    compteur = 0

    def image(m):
        nonlocal compteur
        balise = m.group(0)
        src = re.search(r'\ssrc="([^"]+)"', balise)
        if not src or src.group(1).startswith(("http://", "https://", "/", "data:")):
            return balise
        alt = re.search(r'\salt="([^"]*)"', balise)
        classe = re.search(r'\sclass="([^"]*)"', balise)
        if not verifier_fichier_image(a.dossier / src.group(1), a.nom, erreurs):
            return ""
        compteur += 1
        im = produire_image(a.dossier / src.group(1), dossier_sortie, f"{a.slug}-{compteur}", url_dossier)
        return balise_img(im, html.unescape(alt.group(1)) if alt else "", "(max-width: 760px) 100vw, 700px",
                          classe=classe.group(1) if classe else "")

    corps = IMG_HTML.sub(image, corps)
    corps = re.sub(r"<(/?)h1\b", r"<\1h2", corps)
    texte = re.sub(r"<(style|script)\b.*?</\1>", " ", corps, flags=re.S)
    a.mots = len(html.unescape(re.sub(r"<[^>]+>", " ", texte)).split())
    a.lecture = max(1, round(a.mots / 200))
    return corps


def rendre_texte(a, dossier_sortie, url_dossier, erreurs):
    if a.corps_html:
        return rendre_html(a, dossier_sortie, url_dossier, erreurs)
    compteur = 0

    def image(m):
        nonlocal compteur
        alt, fichier, legende = m.group(1).strip(), m.group(2), m.group(3)
        if fichier.startswith(("http://", "https://", "/")):
            erreurs.append(f"{a.nom} : l'image {fichier} doit être un fichier du dossier de l'article")
            return ""
        if not alt:
            erreurs.append(f"{a.nom} : l'image {fichier} n'a pas de description entre les [ ]")
            return ""
        if not verifier_fichier_image(a.dossier / fichier, a.nom, erreurs):
            return ""
        compteur += 1
        im = produire_image(a.dossier / fichier, dossier_sortie, f"{a.slug}-{compteur}", url_dossier)
        img = balise_img(im, alt, "(max-width: 760px) 100vw, 700px", pin=a.url_pin)
        cap = f"<figcaption>{e(legende)}</figcaption>" if legende else ""
        return f"\n\n<figure class=\"bfig\">{img}{cap}</figure>\n\n"

    texte = IMAGE_MD.sub(image, a.texte)
    corps = markdown.markdown(
        texte,
        extensions=["extra", "sane_lists", "smarty"],
        extension_configs={"smarty": {"substitutions": {
            "left-double-quote": "«&nbsp;", "right-double-quote": "&nbsp;»",
            "left-single-quote": "‘", "right-single-quote": "’",
        }}},
    )
    corps = typo_fr(corps)
    # Le titre de l'article est le seul <h1> de la page.
    corps = re.sub(r"<(/?)h1\b", r"<\1h2", corps)
    a.mots = len(re.sub(r"<[^>]+>", " ", corps).split())
    a.lecture = max(1, round(a.mots / 200))
    return corps


# ── Morceaux de page ───────────────────────────────────────────────────────

def lire_habillage(entree, erreurs):
    """En-tête et pied de page du site, repris de la page modèle."""
    modele = (entree / PAGE_MODELE).read_text(encoding="utf-8") if (entree / PAGE_MODELE).exists() else ""
    haut = re.search(r'<a class="skip".*?</header>', modele, re.S)
    bas = re.search(r'<footer class="site">.*?</footer>', modele, re.S)
    if not (haut and bas):
        erreurs.append(
            f"source/{PAGE_MODELE} : en-tête ou pied de page introuvable. Le blog reprend "
            "le menu de cette page : si l'outil a changé sa structure, adapter PAGE_MODELE dans .github/blog.py")
        return None, None
    entete = haut.group(0).replace(" aria-current=page", "").replace(' aria-current="page"', "")
    return entete, bas.group(0)


def ajouter_lien_blog(page_html, page_courante=False):
    """Ajoute « Blog » après « À propos », dans les menus et le pied de page."""
    if LIEN_BLOG.search(page_html):
        return page_html, False

    def lien(m):
        attrs = m.group(1).replace(" aria-current=page", "").replace(' aria-current="page"', "")
        courant = " aria-current=page" if page_courante and "style=" not in attrs else ""
        return f'{m.group(0)}<a href="/blog/"{attrs}{courant}>Blog</a>'

    nouveau, n = LIEN_A_PROPOS.subn(lien, page_html)
    return nouveau, n > 0


def page(habillage, titre, description, url, contenu, *, image=None, type_og="website",
         jsonld=None, noindex=False, extra_head=""):
    entete, pied = habillage
    if blog_en_ligne:
        entete, _ = ajouter_lien_blog(entete, page_courante=True)
        pied, _ = ajouter_lien_blog(pied)
    meta = [
        '<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">',
        f"<title>{e(titre)}</title>",
        f'<meta name="description" content="{e(description)}">',
    ]
    if noindex:
        # aperçu : rien à suivre ; page de thème trop petite : liens suivis quand même
        meta.append(f'<meta name="robots" content="noindex,{"follow" if noindex == "follow" else "nofollow"}">')
    else:
        meta.append(f'<link rel="canonical" href="{url}">')
    meta += [
        f'<meta property="og:type" content="{type_og}"><meta property="og:site_name" content="Papier Pivoine">',
        f'<meta property="og:title" content="{e(titre)}"><meta property="og:description" content="{e(description)}">',
        f'<meta property="og:url" content="{url}">'
        + (f'<meta property="og:image" content="{image}">' if image else ""),
        '<meta property="og:locale" content="fr_FR">',
        '<meta name="twitter:card" content="summary_large_image">',
        '<link rel="icon" type="image/png" sizes="48x48" href="/assets/favicon-48.png">',
        '<link rel="icon" type="image/png" sizes="512x512" href="/assets/favicon.png">',
        '<link rel="apple-touch-icon" sizes="180x180" href="/assets/apple-touch-icon.png">',
        '<link rel="preload" href="/assets/pp-2026/fonts/Fraunces.woff2" as="font" type="font/woff2" crossorigin>',
        '<link rel="stylesheet" href="/assets/pp-2026/site.css">',
        '<link rel="stylesheet" href="/assets/blog/blog.css">',
        f'<link rel="alternate" type="application/rss+xml" title="Le blog de Papier Pivoine" href="{SITE}/blog/flux.xml">',
    ]
    if extra_head:
        meta.append(extra_head)
    if jsonld:
        donnees = json.dumps({"@context": "https://schema.org", "@graph": jsonld}, ensure_ascii=False)
        donnees = donnees.replace("</", "<\\/")
        meta.append(f'<script type="application/ld+json">{donnees}</script>')
    return (
        '<!doctype html>\n<html lang="fr"><head>\n' + "\n".join(meta) + "\n</head><body>\n"
        + entete + '\n<main id="contenu">\n' + contenu + "\n</main>\n" + pied + "\n</body></html>\n"
    )


def ariane(*niveaux):
    elements = [{"@type": "ListItem", "position": i + 1, "name": nom, "item": url}
                for i, (nom, url) in enumerate([("Accueil", f"{SITE}/")] + list(niveaux))]
    return {"@type": "BreadcrumbList", "itemListElement": elements}


def lien_theme(nom):
    return f'<a href="/blog/theme/{en_slug(nom)}/">{e(nom)}</a>'


def carte(a, titre="h2", grande=False):
    sizes = "(max-width: 900px) 100vw, 560px" if grande else "(max-width: 900px) 100vw, 340px"
    img = balise_img(a.image_carte, a.vignette_alt, sizes, classe="bimg")
    meta = date_fr(a.date) + (f" · {e(a.themes[0])}" if a.themes else "")
    return (
        f'<a class="bcard{" bfeat" if grande else ""}" href="{a.chemin}">{img}<span class="bbody">'
        f'<span class="bmeta">{meta}</span><{titre}>{e(a.titre)}</{titre}>'
        f'<span class="bdesc">{e(a.description)}</span><span class="bmore">Lire la suite →</span>'
        f"</span></a>"
    )


BLOC_LETTRE = """<section class="tight"><div class="wrap"><div class="nl">
 <div>
  <p class="eyebrow">La lettre · gratuite</p>
  <h2>Tu aimes ces mots&nbsp;? Reçois la suite</h2>
  <p>Chaque premier dimanche du mois, je t’écris une lettre : un thème de saison, un exercice d’écriture douce de dix minutes, et mes nouvelles (Bao compris). En cadeau, tu reçois tout de suite la première semaine de Mental Léger.</p>
  <a class="btn" href="/newsletter/">Recevoir ma semaine offerte</a>
  <p class="fine">C’est gratuit. Tu te désinscris en un clic, quand tu veux.</p>
 </div>
 <img src="/assets/pp-2026/img/mental-leger-semaine-offerte.webp" alt="La première semaine de Mental Léger, offerte : la couverture et deux pages" width="1000" height="640" loading="lazy" decoding="async">
</div></div></section>"""

AUTRICE = """<aside class="bauthor">
 <img src="/assets/pp-2026/img/camelia-et-bao-dessin.webp" alt="Dessin de Camélia et de son chat Bao" width="740" height="750" loading="lazy" decoding="async">
 <div><p class="bwho">Écrit par Camélia</p>
 <p>Hypersensible et introvertie, je crée Papier Pivoine : des carnets et un programme d’écriture douce pour celles qui ressentent tout et se rechargent au calme. <a href="/apropos/">Mon histoire</a></p></div>
</aside>"""


# ── Les pages ──────────────────────────────────────────────────────────────

def page_article(a, publies, habillage, apercu):
    # un thème sans article en ligne n'a pas encore de page (cas d'un brouillon)
    en_ligne = {en_slug(t) for b in publies for t in b.themes}
    themes_ok = [t for t in a.themes if en_slug(t) in en_ligne]
    themes = "".join(lien_theme(t) for t in themes_ok)
    chemin_theme = [(themes_ok[0], f"{SITE}/blog/theme/{en_slug(themes_ok[0])}/")] if themes_ok else []
    fil = '<a href="/blog/">Blog</a>' + (f" › {lien_theme(themes_ok[0])}" if themes_ok else "")
    bandeau = ""
    if apercu:
        quand = "brouillon : ne paraîtra pas tant que la ligne brouillon: oui est là" if a.brouillon \
            else f"paraîtra le {date_fr(a.date)}"
        bandeau = f'<p class="bapercu">Aperçu, invisible du public ({quand}).</p>'
    maj = f" · mis à jour le {date_fr(a.maj)}" if a.maj > a.date else ""

    lies = sorted(
        (b for b in publies if b.slug != a.slug),
        key=lambda b: (len({en_slug(t) for t in a.themes} & {en_slug(t) for t in b.themes}), b.date),
        reverse=True,
    )[:A_LIRE_AUSSI]
    aussi = ""
    if lies:
        aussi = ('<section class="band"><div class="wrap"><h2 class="center">À lire aussi</h2>'
                 '<div class="bcards">' + "".join(carte(b, "h3") for b in lies) + "</div></div></section>")

    titre_h1 = e(a.titre)
    if a.surligne and e(a.surligne) in titre_h1:
        titre_h1 = titre_h1.replace(e(a.surligne), f"<mark>{e(a.surligne)}</mark>", 1)
    if a.corps_html:
        texte = f'<div class="briche">\n{a.corps}\n</div>\n<div class="bpost narrow">'
    else:
        texte = f'<div class="bpost narrow">\n{a.corps}'
    couverture = balise_img(a.image, a.couverture_alt, "(max-width: 960px) 100vw, 920px",
                            classe="bcover", paresseuse=False, pin=a.url_pin)
    contenu = f"""{bandeau}<article class="bpost-page">
<header class="bhead narrow">
 <p class="bcrumb">{fil}</p>
 <h1>{titre_h1}</h1>
 <p class="bmeta"><time datetime="{a.date.isoformat()}">{date_fr(a.date)}</time> · {a.lecture} min de lecture · par <a href="/apropos/">Camélia</a>{maj}</p>
</header>
<div class="bcover-wrap">{couverture}</div>
{texte}
{f'<p class="bthemes">{themes}</p>' if themes else ""}
{AUTRICE}
</div>
</article>
{BLOC_LETTRE}
{aussi}"""

    jsonld = [
        {
            "@type": "BlogPosting", "@id": f"{a.url}#article", "mainEntityOfPage": a.url,
            "headline": a.titre, "description": a.description,
            "image": [a.url_partage, SITE + a.image["src"]],
            "datePublished": horodatage(a.date).isoformat(), "dateModified": horodatage(a.maj).isoformat(),
            "author": AUTEUR, "publisher": ORGANISATION, "inLanguage": "fr-FR",
            "wordCount": a.mots, "isPartOf": {"@type": "Blog", "@id": f"{SITE}/blog/#blog", "url": f"{SITE}/blog/"},
            **({"keywords": ", ".join(a.themes), "articleSection": a.themes[0]} if a.themes else {}),
        },
        ariane(("Blog", f"{SITE}/blog/"), *chemin_theme, (a.titre, a.url)),
    ]
    extra = (f'<meta property="article:published_time" content="{horodatage(a.date).isoformat()}">'
             f'<meta property="article:modified_time" content="{horodatage(a.maj).isoformat()}">'
             '<meta name="author" content="Camélia Nguyen">')
    if a.style:
        extra += f'<link rel="stylesheet" href="{a.chemin}{a.slug}.css">'
    return page(habillage, f"{a.titre} · Papier Pivoine", a.description, a.url, contenu,
                image=a.url_partage, type_og="article", jsonld=jsonld, noindex=apercu, extra_head=extra)


def pages_liste(articles, themes, habillage, base, titre, description, surtitre, h1, intro,
                theme_courant=None, nom_theme=None, noindex=False):
    """Une liste d'articles, découpée en pages de PAR_PAGE. Renvoie {chemin: html}."""
    paquets = [articles[i:i + PAR_PAGE] for i in range(0, len(articles), PAR_PAGE)] or [[]]
    tous = '<a href="/blog/"' + ("" if theme_courant else " aria-current=page") + ">Tous les articles</a>"
    puces = tous + "".join(
        f'<a href="/blog/theme/{s}/"' + (" aria-current=page" if s == theme_courant else "") + f">{e(n)}</a>"
        for s, (n, _) in sorted(themes.items(), key=lambda x: (-len(x[1][1]), x[1][0])))
    resultat = {}
    for numero, paquet in enumerate(paquets, start=1):
        chemin = base if numero == 1 else f"{base}page/{numero}/"
        url = SITE + chemin
        une = paquet[0] if numero == 1 and paquet and not theme_courant else None
        reste = paquet[1:] if une else paquet
        cartes = (f'<div class="bune">{carte(une, grande=True)}</div>' if une else "") + (
            '<div class="bcards">' + "".join(carte(a) for a in reste) + "</div>" if reste else "")
        suite = []
        if numero > 1:
            precedente = base if numero == 2 else f"{base}page/{numero - 1}/"
            suite.append(f'<a class="btn ghost small" href="{precedente}" rel="prev">← Articles plus récents</a>')
        if numero < len(paquets):
            suite.append(f'<a class="btn ghost small" href="{base}page/{numero + 1}/" rel="next">Articles plus anciens →</a>')
        pagination = f'<nav class="bpages" aria-label="Pages">{"".join(suite)}</nav>' if suite else ""
        en_titre = titre if numero == 1 else f"{titre} · page {numero}"
        # aligné à gauche comme les autres pages du site, sans dessin : la carte du
        # premier article, juste en dessous, apporte déjà l'illustration (choix de Camélia)
        contenu = f"""<section class="bhero"><div class="wrap">
 <p class="eyebrow">{surtitre}</p><h1>{h1}</h1><p class="lead">{e(intro)}</p>
 <nav class="chips bchips" aria-label="Thèmes">{puces}</nav>
</div></section>
<section class="tight blist"><div class="wrap">{cartes}{pagination}</div></section>
{BLOC_LETTRE}"""
        niveaux = [("Blog", f"{SITE}/blog/")] + ([(nom_theme, SITE + base)] if theme_courant else [])
        jsonld = [
            {"@type": "Blog" if not theme_courant else "CollectionPage",
             "@id": f"{SITE}/blog/#blog" if not theme_courant else url,
             "name": en_titre, "description": description, "url": url, "inLanguage": "fr-FR",
             "publisher": ORGANISATION,
             "blogPost" if not theme_courant else "hasPart": [
                 {"@type": "BlogPosting", "headline": a.titre, "url": a.url,
                  "datePublished": horodatage(a.date).isoformat(), "image": a.url_partage, "author": AUTEUR}
                 for a in paquet]},
            ariane(*niveaux),
        ]
        image = paquet[0].url_partage if paquet else None
        resultat[chemin] = page(habillage, en_titre, description, url, contenu, image=image, jsonld=jsonld,
                                noindex=noindex)
    return resultat


def flux_rss(publies):
    def cdata(texte):
        return "<![CDATA[" + texte.replace("]]>", "]]]]><![CDATA[>") + "]]>"

    items = []
    for a in publies[:30]:
        absolu = re.sub(r'\s(srcset|sizes|loading|decoding|data-pin-media)="[^"]*"', "", a.corps)
        absolu = re.sub(r'(src|href)="/', rf'\1="{SITE}/', absolu)
        image = a.url_pin or a.url_partage
        taille = (a.fichier_pin or a.fichier_partage).stat().st_size
        items.append(f"""  <item>
   <title>{e(a.titre)}</title>
   <link>{a.url}</link>
   <guid isPermaLink="true">{a.url}</guid>
   <pubDate>{format_datetime(horodatage(a.date))}</pubDate>
   <dc:creator>Camélia</dc:creator>
{"".join(f"   <category>{e(t)}</category>{chr(10)}" for t in a.themes)}   <description>{e(a.description)}</description>
   <content:encoded>{cdata(f'<p><img src="{a.url_partage}" alt="{e(a.couverture_alt)}"></p>' + absolu)}</content:encoded>
   <enclosure url="{image}" length="{taille}" type="image/jpeg"/>
  </item>""")
    derniere = format_datetime(horodatage(publies[0].maj if publies else date.today()))
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:content="http://purl.org/rss/1.0/modules/content/" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:atom="http://www.w3.org/2005/Atom">
 <channel>
  <title>Le blog de Papier Pivoine</title>
  <link>{SITE}/blog/</link>
  <atom:link href="{SITE}/blog/flux.xml" rel="self" type="application/rss+xml"/>
  <description>{e(BLOG_DESCRIPTION)}</description>
  <language>fr-FR</language>
  <lastBuildDate>{derniere}</lastBuildDate>
  <image><url>{SITE}/assets/favicon.png</url><title>Le blog de Papier Pivoine</title><link>{SITE}/blog/</link></image>
{chr(10).join(items)}
 </channel>
</rss>
"""


def completer_sitemap(sortie, entrees, erreurs):
    fichier = sortie / "sitemap.xml"
    if not fichier.exists():
        return  # signalé par les vérifications générales
    xml = fichier.read_text(encoding="utf-8")
    if "</urlset>" not in xml:
        erreurs.append("sitemap.xml : balise </urlset> introuvable, impossible d'y ajouter le blog")
        return
    ajout = "".join(
        f"  <url>\n    <loc>{SITE}{chemin}</loc>\n    <lastmod>{quand.isoformat()}</lastmod>\n"
        f"    <changefreq>{freq}</changefreq>\n    <priority>{prio}</priority>\n  </url>\n"
        for chemin, quand, freq, prio in entrees if f"<loc>{SITE}{chemin}</loc>" not in xml)
    fichier.write_text(xml.replace("</urlset>", ajout + "</urlset>"), encoding="utf-8")


def ecrire(sortie, chemin, contenu):
    cible = sortie / chemin.strip("/") / "index.html"
    cible.parent.mkdir(parents=True, exist_ok=True)
    cible.write_text(contenu, encoding="utf-8")


# ── Point d'entrée ─────────────────────────────────────────────────────────

def construire(entree, sortie, erreurs):
    """Construit le blog dans sortie/. Renvoie le nombre d'articles en ligne."""
    avertissements = []
    articles = lire_articles(erreurs, avertissements)
    if not articles:
        return 0
    habillage = lire_habillage(entree, erreurs)
    if habillage[0] is None:
        return 0

    global blog_en_ligne
    jour = aujourdhui()
    for a in articles:
        a.apercu = a.brouillon or a.date > jour
        a.chemin = f"/blog/apercu/{a.slug}/" if a.apercu else f"/blog/{a.slug}/"
        a.url = SITE + a.chemin
    publies = sorted((a for a in articles if not a.apercu), key=lambda a: (a.date, a.titre), reverse=True)
    blog_en_ligne = bool(publies)

    # images (avant le texte : le texte en a besoin pour Pinterest)
    for a in articles:
        dossier = sortie / a.chemin.strip("/")
        dossier.mkdir(parents=True, exist_ok=True)
        a.image = produire_image(a.dossier / a.couverture, dossier, a.slug, a.chemin)
        a.image_carte, a.vignette_alt = a.image, a.couverture_alt
        if a.vignette and (a.dossier / a.vignette).exists():
            a.image_carte = produire_image(a.dossier / a.vignette, dossier, f"{a.slug}-vignette", a.chemin)
            a.vignette_alt = a.vignette_alt_texte or a.couverture_alt
            l, h = a.image_carte["img"].size
            if abs(l / h - 1.5) > 0.03:
                avertissements.append(f"{a.nom} : vignette de {l} × {h} px, pas au format 3:2 (1800 × 1200 conseillé) : elle sera recadrée")
        elif a.image["img"].width / a.image["img"].height > 1.8:
            avertissements.append(f"{a.nom} : couverture très allongée et pas de vignette : les cartes la recadreront fort")
        a.fichier_partage = dossier / f"{a.slug}-partage.jpg"
        largeur, _ = en_jpeg(a.image_carte["img"], LARGEUR_PARTAGE, a.fichier_partage)
        a.url_partage = f"{a.url}{a.fichier_partage.name}"
        if a.image_carte["largeur_origine"] < LARGEUR_PARTAGE:
            avertissements.append(
                f"{a.nom} : {'vignette' if a.vignette else 'couverture'} de {a.image_carte['largeur_origine']} px de large. "
                f"Google Discover et les grands aperçus de partage demandent au moins {LARGEUR_PARTAGE} px")
        a.url_pin = a.fichier_pin = None
        if a.pin and (a.dossier / a.pin).exists():
            a.fichier_pin = dossier / f"{a.slug}-pin.jpg"
            en_jpeg(ouvrir_image(a.dossier / a.pin), 1000, a.fichier_pin)
            a.url_pin = f"{a.url}{a.fichier_pin.name}"
        a.corps = rendre_texte(a, dossier, a.chemin, erreurs)
        if a.style and (a.dossier / a.style).exists():
            shutil.copy2(a.dossier / a.style, dossier / f"{a.slug}.css")

    # thèmes : {slug: (nom affiché, [articles])}, le nom vient de l'article le plus récent
    themes = {}
    for a in publies:
        for t in a.themes:
            themes.setdefault(en_slug(t), (t, []))[1].append(a)

    for a in articles:
        ecrire(sortie, a.chemin, page_article(a, publies, habillage, a.apercu))

    if publies:
        for chemin, contenu in pages_liste(
                publies, themes, habillage, "/blog/", BLOG_TITRE, BLOG_DESCRIPTION,
                BLOG_SURTITRE, BLOG_H1, BLOG_INTRO).items():
            ecrire(sortie, chemin, contenu)
        for slug, (nom, liste) in themes.items():
            for chemin, contenu in pages_liste(
                    liste, themes, habillage, f"/blog/theme/{slug}/", f"{nom} · Blog Papier Pivoine",
                    f"Tous les articles du blog de Papier Pivoine sur le thème « {nom} ».",
                    "Le blog · thème", e(nom), f"{len(liste)} article{'s' if len(liste) > 1 else ''} sur ce thème.",
                    theme_courant=slug, nom_theme=nom,
                    noindex="follow" if len(liste) < THEME_MIN else False).items():
                ecrire(sortie, chemin, contenu)
        (sortie / "blog" / "flux.xml").write_text(flux_rss(publies), encoding="utf-8")
        completer_sitemap(sortie, [("/blog/", max(a.maj for a in publies), "weekly", "0.8")]
                          + [(a.chemin, a.maj, "monthly", "0.7") for a in publies]
                          + [(f"/blog/theme/{s}/", max(a.maj for a in l), "weekly", "0.5")
                             for s, (_, l) in themes.items() if len(l) >= THEME_MIN], erreurs)

    (sortie / "assets" / "blog").mkdir(parents=True, exist_ok=True)
    shutil.copy2(STYLE, sortie / "assets" / "blog" / "blog.css")

    print(f"   {len(publies)} article(s) en ligne, {len(articles) - len(publies)} en aperçu"
          + (f", {len(themes)} thème(s)" if themes else ""))
    for a in articles:
        etat = "brouillon" if a.brouillon else (f"programmé le {date_fr(a.date)}" if a.apercu else "en ligne")
        print(f"   {a.chemin:52} {etat}")
    for avertissement in avertissements:
        print(f"   ⚠ {avertissement}")
    return len(publies)
