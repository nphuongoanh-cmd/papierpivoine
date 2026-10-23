#!/usr/bin/env python3
"""
Prépare la version publiée de papierpivoine.fr.

Ce script NE MODIFIE PAS source/. Il recopie le site de source/ vers _site/ et y
ajoute ce que l'outil de design ne produit pas : la balise de vérification
Pinterest, le favicon là où il manque, et la pop-up « La lettre ». source/
reste exactement ce que l'outil livre : on le remplace en bloc à chaque mise
à jour, sans rien à réappliquer ni à nettoyer.

── Ajout permanent : balise de vérification Pinterest ───────────────────────
Pinterest exige un <meta name="p:domain_verify"> dans le <head> pour prouver que
le domaine appartient bien à Camélia (nécessaire aux Rich Pins). L'outil de
design ne l'ajoute pas ; on l'injecte ici pour qu'une régénération ne la
supprime pas — ce qui dé-revendiquerait le domaine silencieusement.

── Ajout permanent : pop-up « La lettre » (depuis le 2026-10-06) ─────────────
Pop-up d'inscription conçue à part (ajouts/popup-lettre/popup-lettre.html,
formulaire Kit 9685937), collée juste avant </body> sur chaque page, avec son
illustration copiée dans /assets/ppl/. Elle se tient elle-même à l'écart de
/newsletter/ (PAGES_SANS_POPUP dans le bloc). L'ancienne pop-up Kit
automatique (27c8b8373b), que le code des pages charge au démarrage, est
désactivée en posant window.__ppKit27Loaded=true avant ce code : il ne la charge
que si ce drapeau est absent. Les blocs « Recevoir le cadeau » écrits dans les
pages (Kit 638990c016, ouverts au clic) ne sont pas touchés.

── Ajout permanent : favicon (depuis le 2026-10-08) ─────────────────────────
Certaines pages livrées par l'outil (pages autonomes comme /newsletter/ ou
/semaine-offerte/, 404, redirections) ne déclarent pas le favicon : l'onglet
affichait alors l'icône par défaut du navigateur. Les balises de l'accueil
(FAVICON_BALISES) sont ajoutées dans le <head> de toute page qui n'a aucun
<link rel="icon">. Une page qui a déjà le sien n'est pas touchée.

── Ajout permanent : le blog (depuis le 2026-10-14) ──────────────────────────
Les articles s'écrivent dans blog/ (un dossier par article, voir PUBLIER.md) et
sont construits par .github/blog.py : pages des articles, liste, thèmes, flux
RSS, sitemap. Dès qu'un article est en ligne, « Blog » est ajouté après
« À propos » dans le menu et le pied de page de chaque page.

── Historique : trois correctifs retirés le 2026-07-18 ──────────────────────
L'outil de design a corrigé trois bugs à la source (vérifié en ligne), rendant
inutiles les rustines que ce script appliquait auparavant. Retirées :
  1. .nojekyll     — désormais fourni dans le paquet (et sans objet en mode
                     GitHub Actions, qui ne lance pas Jekyll).
  2. <base href>   — les chemins d'images sont maintenant absolus (/assets/…).
  3. verrou Kit    — support.js vérifie désormais document.head avant de
                     remonter un <script>, donc plus de pop-up en double.
Si l'un de ces bugs réapparaissait, voir l'historique git (commit 320fa0e et
avant) pour le correctif correspondant.
"""

import html
import re
import shutil
import sys
from pathlib import Path

import blog

RACINE = Path(__file__).resolve().parent.parent
ENTREE = RACINE / "source"   # le paquet de l'outil, tel quel
SORTIE = RACINE / "_site"    # la copie publiée
EXCLUS = {".DS_Store"}

# Preuve de propriété du domaine pour Pinterest. Ce n'est pas un secret : la
# balise est publique, visible dans le source de chaque page. Ne pas la retirer
# sans dé-revendiquer le domaine côté Pinterest d'abord.
PINTEREST_META = '<meta name="p:domain_verify" content="65335738f5dcb1dd57bb33a15d99e30a"/>'

# Favicon du site, tel que déclaré sur l'accueil. Les fichiers sont dans
# source/assets/ (fournis par l'outil) ; la vérification des fichiers cités
# fait échouer le build s'ils disparaissaient.
FAVICON_BALISES = (
    '<link rel="icon" type="image/png" sizes="48x48" href="/assets/favicon-48.png">\n'
    '<link rel="icon" type="image/png" sizes="512x512" href="/assets/favicon.png">\n'
    '<link rel="apple-touch-icon" sizes="180x180" href="/assets/apple-touch-icon.png">'
)
FAVICON_PRESENT = re.compile(r'<link[^>]+rel="(?:shortcut )?icon"', re.IGNORECASE)

# Pop-up « La lettre » : le bloc à coller avant </body>, et son illustration.
POPUP_DOSSIER = RACINE / "ajouts" / "popup-lettre"
POPUP_BLOC = POPUP_DOSSIER / "popup-lettre.html"
POPUP_IMAGES = {"lettre-the-vert-serre.webp": "assets/ppl/lettre-the-vert-serre.webp"}
# Empêche le code des pages de charger l'ancienne pop-up Kit automatique.
KIT_POPUP_UID = "27c8b8373b"
KIT_POPUP_GARDE = "!window.__ppKit27Loaded"
KIT_POPUP_STOP = "<script>window.__ppKit27Loaded=true;/* ancienne pop-up Kit désactivée : voir corriger-site.py */</script>"

erreurs = []

# Chemin assets/… entre guillemets, parenthèses ou après un « / », tel qu'il
# apparaît dans le HTML, le CSS ou le code JavaScript des pages.
ASSET_CITE = re.compile(
    r"""(?<![\w.-])/?(assets/[\w./-]+?\.(?:jpe?g|png|webp|avif|gif|svg|woff2?|mp4|webm|pdf))(?=["')\s?#,])""",
    re.IGNORECASE,
)


def copier_le_site():
    if not ENTREE.is_dir():
        print("✗ ÉCHEC : le dossier source/ est introuvable.")
        print("  Il doit contenir le paquet produit par l'outil de design")
        print("  (index.html, assets/, _ds/, …). Voir PUBLIER.md.")
        sys.exit(1)
    if not (ENTREE / "index.html").exists():
        print("✗ ÉCHEC : source/index.html est absent.")
        print("  Le contenu du paquet a-t-il bien été déposé DANS source/,")
        print("  plutôt que le dossier du paquet lui-même ? Voir PUBLIER.md.")
        sys.exit(1)

    if SORTIE.exists():
        shutil.rmtree(SORTIE)
    # _site est reconstruit de zéro à chaque publication : un fichier retiré de
    # source/ disparaît donc du site tout seul, sans nettoyage manuel.
    shutil.copytree(
        ENTREE, SORTIE,
        ignore=shutil.ignore_patterns(*EXCLUS),
    )


def injecter_pinterest(chemin):
    html = chemin.read_text(encoding="utf-8")
    if 'name="p:domain_verify"' in html:
        return False  # déjà présente (si l'outil finit par l'inclure)
    nouveau, n = re.subn(r"<head>", "<head>\n" + PINTEREST_META, html, count=1)
    if not n:
        erreurs.append(f"{chemin.relative_to(SORTIE)} : aucune balise <head> trouvée")
        return False
    chemin.write_text(nouveau, encoding="utf-8")
    return True


def ajouter_favicon(chemin):
    html = chemin.read_text(encoding="utf-8")
    if FAVICON_PRESENT.search(html):
        return False  # la page déclare déjà son favicon
    nouveau, n = re.subn(r"<head>", "<head>\n" + FAVICON_BALISES, html, count=1)
    if not n:
        erreurs.append(f"{chemin.relative_to(SORTIE)} : aucune balise <head> pour le favicon")
        return False
    chemin.write_text(nouveau, encoding="utf-8")
    return True


def ajouter_lien_blog(chemin):
    html = chemin.read_text(encoding="utf-8")
    nouveau, fait = blog.ajouter_lien_blog(html)
    if fait:
        chemin.write_text(nouveau, encoding="utf-8")
    return fait


def est_redirection(html):
    return 'http-equiv="refresh"' in html


def ajouter_popup(chemin, bloc):
    """Désactive l'ancienne pop-up Kit et colle la nouvelle avant </body>."""
    html = chemin.read_text(encoding="utf-8")
    if est_redirection(html) or 'id="ppl-overlay"' in html:
        return False
    if KIT_POPUP_UID in html:
        html, n = re.subn(r"<head>", "<head>\n" + KIT_POPUP_STOP, html, count=1)
        if not n:
            erreurs.append(f"{chemin.relative_to(SORTIE)} : aucune balise <head> pour désactiver la pop-up Kit")
    i = html.rfind("</body>")
    if i < 0:
        erreurs.append(f"{chemin.relative_to(SORTIE)} : aucune balise </body> pour la pop-up")
        return False
    chemin.write_text(html[:i] + bloc + "\n" + html[i:], encoding="utf-8")
    return True


# Aucun défilement horizontal : certaines illustrations dépassent volontairement
# de leur cadre (photo de l'accueil à 108 %) et faisaient glisser la page de
# quelques pixels entre 900 et 1080 px. « clip » coupe au bord de l'écran sans
# rien changer d'autre (les bandeaux qui défilent ont leur propre conteneur).
ANTI_DEBORD = "<style>html{overflow-x:clip}</style>"


def ajouter_anti_debord(chemin):
    html = chemin.read_text(encoding="utf-8")
    if est_redirection(html) or ANTI_DEBORD in html:
        return False
    nouveau, n = re.subn(r"</head>", ANTI_DEBORD + "\n</head>", html, count=1)
    if not n:
        erreurs.append(f"{chemin.relative_to(SORTIE)} : aucune balise </head> pour le style anti-débordement")
        return False
    chemin.write_text(nouveau, encoding="utf-8")
    return True


# Descriptions raccourcies pour Google (environ 150 caractères : au-delà, la fin
# est coupée dans les résultats). Accord de Camélia du 2026-10-19. Remplacent
# celles des paquets, pour la recherche (description) et le partage (og:).
DESCRIPTIONS = {
    "index.html": "Exercices d’écriture douce pour femmes hypersensibles et introverties : "
                  "une lettre gratuite chaque mois, une semaine offerte et Mental Léger.",
    "7-permissions-pivoine/index.html": "Les sept petites permissions de Papier Pivoine : Poser, Intimité, "
                                        "Vérité, Observer, Imperfection, Nature, Émerveillement. "
                                        "Pour chaque page que tu écris.",
    "apropos/index.html": "Camélia, hypersensible et introvertie, née au Vietnam : son histoire, les livres "
                          "qui l’accompagnent et pourquoi elle a choisi l’écriture douce.",
    "newsletter/index.html": "Une lettre douce le premier dimanche du mois : un thème de saison, un exercice "
                             "d’écriture, les nouvelles de Camélia. En cadeau, une semaine offerte.",
}


def raccourcir_description(chemin):
    texte = DESCRIPTIONS.get(str(chemin.relative_to(SORTIE)))
    if not texte:
        return False
    html = chemin.read_text(encoding="utf-8")
    nouveau, n = re.subn(r'(<meta (?:name="description"|property="og:description"|name="twitter:description") content=")[^"]*"',
                         lambda m: m.group(1) + texte + '"', html)
    if not n:
        erreurs.append(f"{chemin.relative_to(SORTIE)} : aucune balise description à raccourcir")
        return False
    chemin.write_text(nouveau, encoding="utf-8")
    return nouveau != html


# Semaine offerte : le dessin du haut (tete-pleine.webp) n'avait pas de taille
# avant d'arriver. Sur téléphone et tablette il est au-dessus du texte : à son
# arrivée, tout descendait de 190 px (CLS 0,19 sur connexion lente). On réserve
# sa place (190 px de haut, et 800 x 568 pour l'ordinateur). Rendu final identique.
DESSIN_SO = "/assets/landing/semaine-offerte/tete-pleine.webp"
STYLE_DESSIN_SO = "<style>@media (max-width:860px){.hero-art img{height:190px;object-fit:contain}}</style>"


def reserver_dessin_semaine_offerte(chemin):
    if str(chemin.relative_to(SORTIE)) != "semaine-offerte/index.html":
        return False
    html = chemin.read_text(encoding="utf-8")
    m = re.search(r'<img\b[^>]*src="' + re.escape(DESSIN_SO) + r'"[^>]*>', html)
    if not m or "hero-art" not in html:
        print("   (semaine offerte : dessin du haut introuvable, rien à réserver)")
        return False
    balise = m.group(0)
    if "width=" not in balise:
        balise = balise.replace(f'src="{DESSIN_SO}"', f'src="{DESSIN_SO}" width="800" height="568"')
    html = html.replace(m.group(0), balise, 1)
    if STYLE_DESSIN_SO not in html:
        html = html.replace("</head>", STYLE_DESSIN_SO + "\n</head>", 1)
    chemin.write_text(html, encoding="utf-8")
    return True


# Mentions légales : informations données par Camélia le 2026-10-19. Elles
# remplacent les cases « à compléter » des paquets, même si un nouveau paquet
# les remet.
# Retouches de texte demandées par Camélia : appliquées aussi si un nouveau
# paquet ramène l'ancienne formulation.
RETOUCHES = [
    ("apropos/index.html", "ensuite je m’installe à mon bureau pour Papier Pivoine.",
     "ensuite je m’installe à mon bureau pour travailler sur Papier Pivoine."),
]


def appliquer_retouches(chemin):
    html = chemin.read_text(encoding="utf-8")
    nouveau = html
    for page, avant, apres in RETOUCHES:
        if str(chemin.relative_to(SORTIE)) == page:
            nouveau = nouveau.replace(avant, apres)
    if nouveau == html:
        return False
    chemin.write_text(nouveau, encoding="utf-8")
    return True


# Pas d'adresse ni de téléphone sur le site : choix de Camélia (elle travaille
# chez elle), informée de l'obligation légale le 2026-10-19.
INFOS_LEGALES = [
    (r'<p>Camélia Nguyen, <span class="todo">\[statut[^<]*</span>',
     "<p>Papier Pivoine<br>Camélia Nguyen, entrepreneuse individuelle (micro-entreprise)"),
    (r'<span class="todo">\[adresse postale\]</span><br>', ""),
    (r'<span class="todo">\[numéro SIRET\]</span>', "945 316 016 00019"),
    # Confidentialité : durée de conservation dans Kit (option A)
    (r'Après ta désinscription[^<]*<span class="todo">\[à vérifier[^\]]*Kit\]</span>',
     "Si tu te désinscris, ton adresse est gardée uniquement pour ne plus t’écrire."),
]


def completer_mentions(chemin):
    html = chemin.read_text(encoding="utf-8")
    nouveau = html
    for motif, texte in INFOS_LEGALES:
        nouveau = re.sub(motif, texte, nouveau)
    if nouveau == html:
        return False
    chemin.write_text(nouveau, encoding="utf-8")
    return True


# Barre du haut (ordinateur et menu mobile) : lien « 7 permissions PIVOINE »
# juste avant « À propos », et « La lettre » devient « La lettre, gratuite ».
# Fait ici pour survivre aux nouveaux paquets.
PERMISSIONS_URL = "/7-permissions-pivoine/"
NAV_HAUT = re.compile(r'<nav class="m?nav"[^>]*>.*?</nav>', re.S)
# Six liens : sur petite tablette (701 à 920 px, menu sous le logo), on resserre
# l'espace entre eux pour qu'ils tiennent sur une ligne ; de 701 à 760 px, le
# texte passe aussi de 14 à 13 px.
STYLE_MENU = ("<style>@media (min-width:701px) and (max-width:920px){nav.nav{column-gap:"
              "clamp(12px,calc((100vw - 684px) / 5),24px)}}"
              "@media (min-width:701px) and (max-width:760px){nav.nav,nav.nav a{font-size:13px}}"
              # sept liens, avec « Blog » (la marge latérale de l'en-tête vaut 5 % de l'écran)
              "@media (min-width:701px) and (max-width:920px){nav.nav:has(a[href=\"/blog/\"]){column-gap:"
              "clamp(12px,calc((90vw - 628px) / 6),24px)}}"
              "@media (min-width:701px) and (max-width:777px){nav.nav:has(a[href=\"/blog/\"]),"
              "nav.nav:has(a[href=\"/blog/\"]) a{font-size:13px}nav.nav:has(a[href=\"/blog/\"]){column-gap:"
              "clamp(12px,calc((90vw - 584px) / 6),24px)}}"
              "@media (min-width:701px) and (max-width:728px){nav.nav:has(a[href=\"/blog/\"]),"
              "nav.nav:has(a[href=\"/blog/\"]) a{font-size:12.5px}nav.nav:has(a[href=\"/blog/\"]){column-gap:10px}}"
              # jamais deux lignes : avant l'arrivée de Nunito Sans, la police de secours, plus large,
              # faisait passer le menu sur deux lignes un instant, et toute la page sautait (CLS 0,65)
              "@media (min-width:701px) and (max-width:920px){nav.nav{flex-wrap:nowrap}}</style>")
# Nunito Sans chargée en priorité sur les pages qui l'utilisent pour le menu
PRECHARGE_NUNITO = '<link rel="preload" href="/assets/pp-2026/fonts/NunitoSans.woff2" as="font" type="font/woff2" crossorigin>'


def ajouter_lien_permissions(chemin):
    html = chemin.read_text(encoding="utf-8")
    courant = ' aria-current="page"' if chemin.parent.name == PERMISSIONS_URL.strip("/") else ""
    lien = f'<a href="{PERMISSIONS_URL}"{courant}>7 permissions PIVOINE</a>'

    def poser(m):
        nav = re.sub(r'(<a href="/newsletter/"[^>]*>)La lettre</a>', r"\1La lettre, gratuite</a>", m.group(0))
        if f'href="{PERMISSIONS_URL}"' in nav:
            return nav
        i = nav.find('<a href="/apropos/"')
        i = i if i >= 0 else nav.rfind("</nav>")
        return nav[:i] + lien + nav[i:]

    nouveau = NAV_HAUT.sub(poser, html)
    if '<nav class="nav"' in nouveau and STYLE_MENU not in nouveau:
        nouveau = nouveau.replace("</head>", STYLE_MENU + "\n</head>", 1)
    if "/assets/pp-2026/site.css" in nouveau and PRECHARGE_NUNITO not in nouveau:
        nouveau = nouveau.replace("</head>", PRECHARGE_NUNITO + "\n</head>", 1)
    if nouveau == html:
        return False
    chemin.write_text(nouveau, encoding="utf-8")
    return True


def copier_images_popup():
    for nom, cible in POPUP_IMAGES.items():
        (SORTIE / cible).parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(POPUP_DOSSIER / nom, SORTIE / cible)


def verifier(pages):
    """Garde-fous : on préfère un build qui échoue à un site cassé en ligne."""
    for page in pages:
        html = page.read_text(encoding="utf-8")
        if html.count('name="p:domain_verify"') != 1:
            erreurs.append(
                f"{page.relative_to(SORTIE)} : balise Pinterest absente ou en double "
                "(sans elle, le domaine serait dé-revendiqué)"
            )
        if not FAVICON_PRESENT.search(html):
            erreurs.append(f"{page.relative_to(SORTIE)} : favicon absent")

    # toute image référencée doit exister
    for page in pages:
        base = page.parent
        for src in re.findall(r'<img[^>]*src="([^"]*)"', page.read_text(encoding="utf-8")):
            if src.startswith(("http", "//", "data:")):
                continue
            cible = (SORTIE / src.lstrip("/")) if src.startswith("/") else (base / src)
            if not cible.resolve().exists():
                erreurs.append(f"{page.relative_to(SORTIE)} : image introuvable -> {src}")

    # tout fichier assets/… cité ailleurs (code JavaScript des pages, gabarits
    # _app/*.json) doit exister aussi. Le contrôle <img> ci-dessus ne voit pas
    # les images qu'une galerie charge au clic : le 2026-09-30, un paquet citait
    # 8 aperçus .webp absents, que le build aurait laissé passer.
    manquants = {}
    for fichier in pages + sorted((SORTIE / "_app").glob("*.json")):
        texte = fichier.read_text(encoding="utf-8").replace("\\/", "/")
        for chemin in set(ASSET_CITE.findall(texte)):
            if not (SORTIE / chemin).exists():
                manquants.setdefault(chemin, []).append(str(fichier.relative_to(SORTIE)))
    for chemin, ou in sorted(manquants.items()):
        erreurs.append(f"fichier cité introuvable -> /{chemin} (dans {len(ou)} fichier(s), ex. {ou[0]})")

    # pop-up « La lettre » : une seule fois par page, et jamais l'ancienne pop-up Kit
    for page in pages:
        html = page.read_text(encoding="utf-8")
        nom = page.relative_to(SORTIE)
        if est_redirection(html):
            continue
        if html.count('id="ppl-overlay"') != 1:
            erreurs.append(f"{nom} : pop-up « La lettre » absente ou en double")
        if KIT_POPUP_UID in html and (KIT_POPUP_GARDE not in html or KIT_POPUP_STOP not in html):
            erreurs.append(
                f"{nom} : l'ancienne pop-up Kit ({KIT_POPUP_UID}) n'est plus désactivable "
                "(le code des pages a changé) : il y aurait deux pop-ups"
            )
        if re.search(r"<script[^>]+src=[^>]*(kit\.com|convertkit\.com|ck\.page)", html):
            erreurs.append(f"{nom} : un script Kit est chargé directement (pop-up en double ?)")
        if "fonts.googleapis" in html:
            erreurs.append(f"{nom} : Google Fonts est chargé (le site héberge ses polices)")

    # barre du haut : le lien « 7 permissions PIVOINE » dans chaque menu
    for page in pages:
        for nav in NAV_HAUT.findall(page.read_text(encoding="utf-8")):
            if f'href="{PERMISSIONS_URL}"' not in nav:
                erreurs.append(f"{page.relative_to(SORTIE)} : lien 7 permissions absent de la barre du haut")
            if "La lettre, gratuite</a>" not in nav:
                erreurs.append(f"{page.relative_to(SORTIE)} : « La lettre, gratuite » absent de la barre du haut")

    for essentiel in ["CNAME", "index.html", "sitemap.xml", "robots.txt"]:
        if not (SORTIE / essentiel).exists():
            erreurs.append(f"fichier essentiel manquant : {essentiel}")


# Pied de page : les réseaux en icônes (trait encre dans un rond, pivoine au survol)
# au lieu de six liens en texte. Le nom reste lu par les lecteurs d'écran (aria-label)
# et s'affiche au survol (title).
_T = 'fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"'
ICONES = {
    "pinterest": ("Pinterest", f'<path {_T} d="M12.9 9.4 10.4 21M8.4 15.2C7.5 14.3 7 13.1 7 11.7 7 8.4 9.7 5.8 13.2 5.8c3.2 0 5.3 2.2 5.3 5.1 0 3.2-1.9 5.5-4.4 5.5-1.1 0-2-.5-2.4-1.3"/>'),
    "youtube": ("YouTube", f'<rect x="2.5" y="5.5" width="19" height="13" rx="4" {_T}/><path {_T} d="M10.2 9.3v5.4l4.6-2.7z"/>'),
    "tiktok": ("TikTok", f'<path {_T} d="M13.5 3.5v11a3.2 3.2 0 1 1-3.2-3.2M13.5 3.5c.4 2.4 2.1 4 4.5 4.2"/>'),
    "instagram": ("Instagram", f'<rect x="3.2" y="3.2" width="17.6" height="17.6" rx="5" {_T}/><circle cx="12" cy="12" r="4" {_T}/><circle cx="17.1" cy="6.9" r=".6" fill="currentColor"/>'),
    "facebook": ("Facebook", f'<path {_T} d="M15.5 3.5h-2.2A3.8 3.8 0 0 0 9.5 7.3v13.2M7 11h7"/>'),
    "threads": ("Threads", f'<path {_T} d="M16.6 10.8c-.5-2.4-2.2-3.6-4.6-3.6-3 0-4.9 2.1-4.9 4.9s1.9 4.9 4.9 4.9c2.2 0 3.7-1.1 3.7-2.8 0-2-2.2-2.6-4-2.2-1.4.3-2.1 1-2 2 .1 1.1 1.2 1.6 2.3 1.5 1.9-.2 2.8-1.8 2.8-4M19.5 12a7.5 7.5 0 1 1-2.2-5.3"/>'),
}
RESEAU = re.compile(r'<a href="(https://(?:fr\.|www\.)?(pinterest|youtube|tiktok|instagram|facebook|threads)\.com[^"]*)"([^>]*)>[^<]*</a>')
SUITE_RESEAUX = re.compile(r'(?:\s*' + RESEAU.pattern + r')+')
STYLE_RESEAUX = ("<style>.fsocial{display:flex;flex-wrap:wrap;gap:10px;margin-top:6px}"
                 ".fsocial a{display:grid;place-items:center;width:40px;height:40px;border-radius:50%;"
                 "background:#fff;border:1.5px solid var(--border-faint,#EDE1D6);color:var(--ink-soft,#46452F)!important;"
                 "transition:color .2s,border-color .2s,background .2s,transform .2s}"
                 ".fsocial a:hover,.fsocial a:focus-visible{color:var(--peony-dk,#BF5548)!important;"
                 "border-color:var(--peony,#E26D5F);background:var(--rose-l,#FBEDEA);transform:rotate(-6deg) translateY(-1px)}"
                 ".fsocial svg{width:20px;height:20px}"
                 # sur téléphone, le site agrandit les liens du pied de page (44 px de haut) : les ronds restent ronds
                 "footer .fcol .fsocial a{display:grid;min-height:0;padding:0;flex:none}"
                 "@media (max-width:700px){footer .fcol .fsocial a{width:44px;height:44px}}"
                 "@media (max-width:360px){.fsocial{gap:8px}footer .fcol .fsocial a{width:40px;height:40px}}</style>")


def icones_reseaux(chemin):
    html_page = chemin.read_text(encoding="utf-8")
    debut = html_page.rfind("<footer")
    if debut < 0 or 'class="fsocial"' in html_page:
        return False

    def remplacer_suite(m):
        liens = []
        for lien in RESEAU.finditer(m.group(0)):
            url, reseau, attrs = lien.groups()
            nom, svg = ICONES[reseau]
            attrs = re.sub(r'\s*style="[^"]*"', "", attrs)
            liens.append(f'<a href="{url}"{attrs} aria-label="{nom}" title="{nom}">'
                         f'<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false">{svg}</svg></a>')
        return '<div class="fsocial">' + "".join(liens) + "</div>"

    pied, n = SUITE_RESEAUX.subn(remplacer_suite, html_page[debut:])
    if not n:
        return False
    nouveau = (html_page[:debut] + pied).replace("</head>", STYLE_RESEAUX + "\n</head>", 1)
    chemin.write_text(nouveau, encoding="utf-8")
    return True


# /llms.txt : résumé du site pour les assistants IA (ChatGPT, Claude, Perplexity…),
# au format proposé sur llmstxt.org. Fait à chaque publication à partir du sitemap :
# les nouvelles pages et les articles du blog y entrent tout seuls.
LLMS_INTRO = (
    "# Papier Pivoine\n\n"
    "> Papier Pivoine, de Camélia Nguyen : des pages d’écriture douce pour les femmes "
    "hypersensibles et introverties, qui ressentent tout et se rechargent au calme. "
    "Une lettre gratuite chaque premier dimanche du mois, la première semaine de Mental Léger "
    "offerte, Mental Léger (six semaines d’écriture douce, 5 à 10 minutes par jour) et un blog.\n\n"
    "C’est une pratique douce, pas un soin : elle ne remplace ni un avis médical ni un suivi "
    "psychologique. En France, le 3114 répond 24 h/24, gratuitement.\n"
)


def ecrire_llms():
    sitemap = (SORTIE / "sitemap.xml").read_text(encoding="utf-8")
    pages, articles = [], []
    for url in re.findall(r"<loc>([^<]+)</loc>", sitemap):
        chemin = url.replace("https://papierpivoine.fr", "")
        fichier = SORTIE / chemin.lstrip("/") / "index.html" if chemin.endswith("/") else SORTIE / chemin.lstrip("/")
        if not fichier.exists():
            continue
        tete = fichier.read_text(encoding="utf-8").split("</head>")[0]
        titre = re.search(r"<title>(.*?)</title>", tete, re.S)
        desc = re.search(r'<meta name="description" content="([^"]*)"', tete)
        if not titre:
            continue
        ligne = f"- [{html.unescape(titre.group(1)).strip()}]({url})" + (
            f" : {html.unescape(desc.group(1)).strip()}" if desc else "")
        (articles if chemin.startswith("/blog/") and chemin != "/blog/" else pages).append(ligne)
    texte = LLMS_INTRO + "\n## Pages\n\n" + "\n".join(pages) + "\n"
    if articles:
        texte += "\n## Articles du blog\n\n" + "\n".join(articles) + "\n"
    (SORTIE / "llms.txt").write_text(texte, encoding="utf-8")


def main():
    print("→ copie du site vers _site/")
    copier_le_site()

    print("→ blog")
    blog_en_ligne = blog.construire(ENTREE, SORTIE, erreurs)

    pages = sorted(SORTIE.rglob("*.html"))
    print(f"→ {len(pages)} pages HTML")
    bloc = POPUP_BLOC.read_text(encoding="utf-8")
    copier_images_popup()
    for page in pages:
        pose = injecter_pinterest(page)
        icone = ajouter_favicon(page)
        popup = ajouter_popup(page, bloc)
        perm = ajouter_lien_permissions(page)
        bord = ajouter_anti_debord(page)
        desc = raccourcir_description(page)
        dessin = reserver_dessin_semaine_offerte(page)
        legal = completer_mentions(page)
        retouche = appliquer_retouches(page)
        menu = blog_en_ligne and ajouter_lien_blog(page)
        reseaux = icones_reseaux(page)
        faits = [n for n, f in (("pinterest", pose), ("favicon", icone), ("pop-up", popup),
                                ("menu 7 permissions", perm), ("sans débordement", bord),
                                ("description", desc), ("place du dessin", dessin),
                                ("mentions", legal), ("retouche", retouche),
                                ("lien blog", menu), ("icônes réseaux", reseaux)) if f]
        print(f"   {str(page.relative_to(SORTIE)):32} {' + '.join(faits) or 'rien à faire'}")

    for page in pages:
        if 'class="todo"' in page.read_text(encoding="utf-8"):
            print(f"   ⚠ il reste une case « à compléter » dans {page.relative_to(SORTIE)}")
    ecrire_llms()
    print("→ vérifications")
    verifier(pages)
    if blog_en_ligne:
        if not (SORTIE / "blog" / "index.html").exists():
            erreurs.append("blog : la page /blog/ n'a pas été construite")
        if "/blog/</loc>" not in (SORTIE / "sitemap.xml").read_text(encoding="utf-8"):
            erreurs.append("blog : /blog/ absent du sitemap")
        if not any(blog.LIEN_BLOG.search((SORTIE / p).read_text(encoding="utf-8"))
                   for p in ("index.html", "apropos/index.html")):
            erreurs.append("blog : le lien « Blog » n'a pas pu être ajouté au menu "
                           "(le lien « À propos » a changé dans l'outil ?)")

    if erreurs:
        print("\n✗ ÉCHEC — le site ne sera pas publié :")
        for e in erreurs:
            print(f"   - {e}")
        sys.exit(1)

    print(f"\n✓ _site/ prêt : {sum(1 for _ in SORTIE.rglob('*') if _.is_file())} fichiers")


if __name__ == "__main__":
    main()
