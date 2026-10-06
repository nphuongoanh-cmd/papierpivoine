#!/usr/bin/env python3
"""
Prépare la version publiée de papierpivoine.fr.

Ce script NE MODIFIE PAS source/. Il recopie le site de source/ vers _site/ et y
ajoute la seule chose que l'outil de design ne produit pas : la balise de
vérification Pinterest. source/ reste exactement ce que l'outil livre : on le
remplace en bloc à chaque mise à jour, sans rien à réappliquer ni à nettoyer.

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

import re
import shutil
import sys
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
ENTREE = RACINE / "source"   # le paquet de l'outil, tel quel
SORTIE = RACINE / "_site"    # la copie publiée
EXCLUS = {".DS_Store"}

# Preuve de propriété du domaine pour Pinterest. Ce n'est pas un secret : la
# balise est publique, visible dans le source de chaque page. Ne pas la retirer
# sans dé-revendiquer le domaine côté Pinterest d'abord.
PINTEREST_META = '<meta name="p:domain_verify" content="65335738f5dcb1dd57bb33a15d99e30a"/>'

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

    for essentiel in ["CNAME", "index.html", "sitemap.xml", "robots.txt"]:
        if not (SORTIE / essentiel).exists():
            erreurs.append(f"fichier essentiel manquant : {essentiel}")


def main():
    print("→ copie du site vers _site/")
    copier_le_site()

    pages = sorted(SORTIE.rglob("*.html"))
    print(f"→ {len(pages)} pages HTML")
    bloc = POPUP_BLOC.read_text(encoding="utf-8")
    copier_images_popup()
    for page in pages:
        pose = injecter_pinterest(page)
        popup = ajouter_popup(page, bloc)
        faits = [n for n, f in (("pinterest", pose), ("pop-up", popup)) if f]
        print(f"   {str(page.relative_to(SORTIE)):32} {' + '.join(faits) or 'rien à faire'}")

    print("→ vérifications")
    verifier(pages)

    if erreurs:
        print("\n✗ ÉCHEC — le site ne sera pas publié :")
        for e in erreurs:
            print(f"   - {e}")
        sys.exit(1)

    print(f"\n✓ _site/ prêt : {sum(1 for _ in SORTIE.rglob('*') if _.is_file())} fichiers")


if __name__ == "__main__":
    main()
