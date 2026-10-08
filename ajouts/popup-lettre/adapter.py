#!/usr/bin/env python3
"""
Adapte une nouvelle version de la pop-up « La lettre » au site.

Usage : python3 ajouts/popup-lettre/adapter.py [fichier livré]
  (sans argument : repart de popup-lettre-original.html)

Le fichier livré est copié en popup-lettre-original.html (référence), puis
popup-lettre.html est régénéré avec, et seulement, ces ajustements :
  1. polices : fichiers du site (/assets/fonts/) au lieu de Google Fonts,
     sous des noms préfixés « ppl » ;
  2. illustration : copie locale /assets/ppl/ au lieu de Netlify ;
  3. fermeture : retour à la position sans animation sur les pages en
     défilement doux (scroll-behavior: smooth) ;
  4. PAGES_SANS_POPUP : aussi /semaine-offerte/, /mental-leger/suite/, /liens/, /boutique/
     (accord du 2026-10-06).
Le design, le texte et le reste du comportement ne sont pas touchés. Le script
s'arrête si un repère attendu a disparu du fichier livré.
"""

import re
import shutil
import sys
from pathlib import Path

ICI = Path(__file__).resolve().parent
ORIGINAL = ICI / "popup-lettre-original.html"
SORTIE = ICI / "popup-lettre.html"

NETLIFY = "https://phenomenal-sunshine-50fca1.netlify.app/lettre/lettre-the-vert-serre.webp"
IMAGE_LOCALE = "/assets/ppl/lettre-the-vert-serre.webp"
PAGES = "['/newsletter/', '/semaine-offerte/', '/mental-leger/suite/', '/liens/', '/boutique/']"

LATIN = ("U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+0304, "
         "U+0308, U+0329, U+2000-206F, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD")
LATIN_EXT = ("U+0100-02BA, U+02BD-02C5, U+02C7-02CC, U+02CE-02D7, U+02DD-02FF, U+0304, U+0308, "
             "U+0329, U+1D00-1DBF, U+1E00-1E9F, U+1EF2-1EFF, U+2020, U+20A0-20AB, U+20AD-20C0, "
             "U+2113, U+2C60-2C7F, U+A720-A7FF")
POLICES = [("Fraunces", "800", "fraunces-800"), ("Caveat", "700", "caveat-700"),
           ("Nunito Sans", "300 700", "nunito-sans")]


def remplacer(texte, avant, apres, nom, regex=False):
    nouveau, n = (re.subn(avant, apres, texte, flags=re.S) if regex
                  else (texte.replace(avant, apres), texte.count(avant)))
    if not n:
        sys.exit(f"✗ repère introuvable dans le fichier livré : {nom}")
    return nouveau


def main():
    if len(sys.argv) > 1:
        shutil.copy2(sys.argv[1], ORIGINAL)
    t = ORIGINAL.read_text(encoding="utf-8")

    # 1. polices
    t = remplacer(t, r'<link rel="preconnect" href="https://fonts\.googleapis\.com">.*?rel="stylesheet">\n',
                  "", "liens Google Fonts", regex=True)
    faces = "\n".join(
        "@font-face{font-family:'ppl %s';font-style:normal;font-weight:%s;font-display:swap;"
        "src:url(/assets/fonts/%s-%s.woff2) format('woff2');unicode-range:%s}" % (fam, poids, base, sous, plage)
        for fam, poids, base in POLICES for sous, plage in (("latin", LATIN), ("latin-ext", LATIN_EXT)))
    t = remplacer(t, "<style>\n", "<style>\n/* ---------- Polices (fichiers du site) ---------- */\n" + faces + "\n",
                  "balise <style>")
    for fam, _, _ in POLICES:
        t = remplacer(t, f"font-family:'{fam}',", f"font-family:'ppl {fam}','{fam}',", f"police {fam}")
    if "googleapis" in t or "gstatic" in t:
        sys.exit("✗ il reste une référence à Google Fonts")

    # 2. illustration
    t = remplacer(t, NETLIFY, IMAGE_LOCALE, "illustration Netlify")

    # 3. retour sans saut
    t = remplacer(t, "    b.position = b.top = b.left = b.right = b.width = '';\n    window.scrollTo(0, savedY);",
                  "    b.position = b.top = b.left = b.right = b.width = '';\n"
                  "    // retour instantané, même si la page a « scroll-behavior: smooth » (sinon elle remonterait puis redescendrait)\n"
                  "    var h = document.documentElement.style, sb = h.scrollBehavior; h.scrollBehavior = 'auto';\n"
                  "    window.scrollTo(0, savedY);\n"
                  "    h.scrollBehavior = sb;", "fonction unlock()")

    # 4. pages sans pop-up
    t = remplacer(t, r"var PAGES_SANS_POPUP = \[[^\]]*\];[^\n]*",
                  f"var PAGES_SANS_POPUP = {PAGES}; // formulaire déjà là, abonnées, ou lien en bio",
                  "PAGES_SANS_POPUP", regex=True)

    note = ("     Adaptation pour papierpivoine.fr (générée par adapter.py, seuls changements) :\n"
            "     · polices : les fichiers du site (/assets/fonts/) au lieu de Google Fonts,\n"
            "       sous des noms préfixés « ppl » pour ne rien mélanger avec la page ;\n"
            "     · illustration : copie locale /assets/ppl/ au lieu de Netlify ;\n"
            "     · fermeture : retour à la position sans animation sur les pages en défilement doux ;\n"
            "     · PAGES_SANS_POPUP : aussi /semaine-offerte/, /mental-leger/suite/, /liens/, /boutique/.\n"
            "     Ajouté à chaque page par .github/corriger-site.py au moment de la publication.\n")
    t = remplacer(t, "     ============================================================ -->\n",
                  note + "     ============================================================ -->\n", "en-tête")
    SORTIE.write_text(t, encoding="utf-8")
    print(f"✓ {SORTIE.name} régénéré depuis {ORIGINAL.name}")


if __name__ == "__main__":
    main()
