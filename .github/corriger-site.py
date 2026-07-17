#!/usr/bin/env python3
"""
Prépare la version publiée de papierpivoine.fr.

Ce script NE MODIFIE PAS source/. Il recopie le site de source/ vers _site/ et
applique là, et là seulement, ce que l'outil de design ne sait pas produire.
source/ reste donc exactement ce que l'outil produit : on peut le remplacer en
bloc à chaque mise à jour, sans rien à réappliquer ni à nettoyer.

Deux catégories, à ne pas confondre.

═══ A. Ajouts permanents ═══════════════════════════════════════════════════
À garder tant que l'outil ne les intègre pas.

0. Balise de vérification Pinterest — Pinterest exige un <meta> dans le <head>
   pour prouver que le domaine appartient bien à Camélia (nécessaire aux Rich
   Pins). L'outil de design ne permet pas de l'ajouter ; on l'injecte ici pour
   qu'une régénération ne la supprime pas — ce qui dé-revendiquerait le domaine
   silencieusement.

═══ B. Correctifs temporaires ══════════════════════════════════════════════
Bugs de l'outil de design. À supprimer un par un dès que l'amont les aura
réglés (chacun est écrit pour ne rien faire si le bug a disparu) :

1. .nojekyll — GitHub Pages lançait Jekyll, qui exclut du site publié tout
   dossier commençant par un underscore. La charte vit dans _ds/ : polices et
   couleurs renvoyaient 404, le site s'affichait en noir/serif.

2. <base href="/"> — l'appli fige le préfixe de ses images au chargement selon
   la profondeur de l'URL ("assets/" sur l'accueil, "../assets/" ailleurs). Avec
   la navigation React sans rechargement, arriver sur l'accueil puis cliquer dans
   le menu produisait /blog/assets/... -> 404. Correctif amont : émettre des
   chemins absolus (/assets/...).

3. Verrou sur l'embed Kit — support.js remonte les <script> du <head> pré-rendu
   sans vérifier qu'ils y sont déjà (son Set "mounted" ne connaît que ses propres
   ajouts). L'embed Kit s'exécutait deux fois : deux pop-ups, et selon la course
   l'une perdait son <style>, s'affichant alors en clair par-dessus le site.
   Correctif amont : ignorer un script déjà présent dans document.head.
"""

import re
import shutil
import sys
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
ENTREE = RACINE / "source"   # le paquet de l'outil, tel quel
SORTIE = RACINE / "_site"    # la copie corrigée qui part en ligne
EXCLUS = {".DS_Store"}

# ── A. Ajout permanent ───────────────────────────────────────────────────────
# Preuve de propriété du domaine pour Pinterest. Ce n'est pas un secret : la
# balise est publique, visible dans le source de chaque page. Ne pas la retirer
# sans dé-revendiquer le domaine côté Pinterest d'abord.
PINTEREST_META = '<meta name="p:domain_verify" content="65335738f5dcb1dd57bb33a15d99e30a"/>'

# ── B. Correctifs temporaires ────────────────────────────────────────────────
KIT_UID = "27c8b8373b"
KIT_BALISE = re.compile(
    r'<script\s+async\s+data-uid="' + KIT_UID + r'"\s+'
    r'src="https://camelianguyen\.kit\.com/' + KIT_UID + r'/index\.js"></script>'
)
KIT_VERROU = (
    "<script>/* PP: verrou anti-doublon Kit — voir .github/corriger-site.py */"
    "if(!window.__ppKitAuto){window.__ppKitAuto=1;"
    'var s=document.createElement("script");s.async=true;'
    's.setAttribute("data-uid","' + KIT_UID + '");'
    's.src="https://camelianguyen.kit.com/' + KIT_UID + '/index.js";'
    "document.head.appendChild(s);}</script>"
)

erreurs = []


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


def poser_nojekyll():
    f = SORTIE / ".nojekyll"
    if not f.exists():
        f.touch()
        return "créé"
    return "déjà présent"


def corriger_page(chemin):
    html = chemin.read_text(encoding="utf-8")
    avant = html
    notes = []

    # A. Vérification Pinterest (permanent)
    if 'name="p:domain_verify"' not in html:
        html, n = re.subn(r"<head>", "<head>\n" + PINTEREST_META, html, count=1)
        if n:
            notes.append("pinterest")

    # B. Correctifs temporaires
    if '<base href="/">' not in html:
        html, n = re.subn(r"<head>", '<head>\n<base href="/">', html, count=1)
        if n:
            notes.append("base")
        else:
            erreurs.append(f"{chemin.name} : aucune balise <head> trouvée")

    if KIT_BALISE.search(html):
        html = KIT_BALISE.sub(KIT_VERROU, html, count=1)
        notes.append("verrou-kit")

    if html != avant:
        chemin.write_text(html, encoding="utf-8")
    return notes


def verifier(pages):
    """Garde-fous : on préfère un build qui échoue à un site cassé en ligne."""
    for page in pages:
        html = page.read_text(encoding="utf-8")
        if html.count('name="p:domain_verify"') != 1:
            erreurs.append(
                f"{page.relative_to(SORTIE)} : balise Pinterest absente ou en double "
                "(sans elle, le domaine serait dé-revendiqué)"
            )
        if html.count('<base href="/">') != 1:
            erreurs.append(f"{page.relative_to(SORTIE)} : <base> absent ou en double")
        if f'src="https://camelianguyen.kit.com/{KIT_UID}/index.js"></script>' in html:
            erreurs.append(f"{page.relative_to(SORTIE)} : balise Kit non verrouillée")

    # toute image référencée doit exister
    for page in pages:
        base = page.parent
        for src in re.findall(r'<img[^>]*src="([^"]*)"', page.read_text(encoding="utf-8")):
            if src.startswith(("http", "//", "data:")):
                continue
            cible = (SORTIE / src.lstrip("/")) if src.startswith("/") else (base / src)
            if not cible.resolve().exists():
                erreurs.append(f"{page.relative_to(SORTIE)} : image introuvable -> {src}")

    for essentiel in ["CNAME", "index.html", "sitemap.xml", "robots.txt", ".nojekyll"]:
        if not (SORTIE / essentiel).exists():
            erreurs.append(f"fichier essentiel manquant : {essentiel}")


def main():
    print("→ copie du site vers _site/")
    copier_le_site()

    print(f"→ .nojekyll : {poser_nojekyll()}")

    pages = sorted(SORTIE.rglob("*.html"))
    print(f"→ {len(pages)} pages HTML à corriger")
    for page in pages:
        notes = corriger_page(page)
        etiquette = ", ".join(notes) if notes else "rien à faire"
        print(f"   {str(page.relative_to(SORTIE)):32} {etiquette}")

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
