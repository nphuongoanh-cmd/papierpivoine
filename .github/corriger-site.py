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

    for essentiel in ["CNAME", "index.html", "sitemap.xml", "robots.txt"]:
        if not (SORTIE / essentiel).exists():
            erreurs.append(f"fichier essentiel manquant : {essentiel}")


def main():
    print("→ copie du site vers _site/")
    copier_le_site()

    pages = sorted(SORTIE.rglob("*.html"))
    print(f"→ {len(pages)} pages HTML")
    for page in pages:
        pose = injecter_pinterest(page)
        print(f"   {str(page.relative_to(SORTIE)):32} {'pinterest' if pose else 'rien à faire'}")

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
