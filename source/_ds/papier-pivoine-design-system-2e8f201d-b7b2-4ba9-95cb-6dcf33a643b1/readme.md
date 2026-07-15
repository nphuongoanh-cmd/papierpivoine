# Papier Pivoine — Design System

> *Un moment à toi.*

Papier Pivoine (French: *peony paper*) is a French-language well-being brand making **printable journals and activity books** for highly sensitive, introverted women. It is the calm alternative to two things that drain its reader: the endless screen, and the optimise-yourself noise of modern wellness. The brand tends to what she feels rather than fixing who she is.

This is **not** a personal-development brand. There is no program, no "better self," no hustle. There is a quiet place to feel and be understood, and a gentle practice (the PIVOINE method) she can pick up whenever she needs it.

The author signs everything under the pen name **Camélia Nguyen**. The brand never shows a face or a voice — only the written word and a strong, soft visual world built around the peony.

---

## Sources

This design system was built entirely from the brand's own documents (no codebase, no Figma):

- **`uploads/Papier_Pivoine_Brand_Bible_v0.11.docx`** — master brand bible (canonical). Positioning, the reader, the PIVOINE method, voice charter, naming, business model, locked colour palette and fonts. Extracted to `uploads/_brandbible.txt`.
- **`uploads/Voice Charter.docx`** — the voice in depth, writing canon, sample sentences, drift checks. Extracted to `uploads/_voice.txt`.
- **`uploads/My story.docx`** — the founder's raw lived experience in her own words (the emotional source material). Extracted to `uploads/_mystory.txt`.
- **`uploads/Aboreto-Regular.ttf`**, **`uploads/AlbertSans-Regular.ttf`** — the two brand fonts.
- **`uploads/Capture d'écran 2026-06-21 à 22.22.26.png`** — a screenshot reference. ⚠️ The file tools reject this filename (accented characters + apostrophe). Re-upload it with a plain ASCII name (e.g. `reference.png`) if you'd like it incorporated.

The two products are: **the flagship journal** (Journal 1: *Quand ma tête est pleine* — "Pour femmes hypersensibles et introverties") and **the activity-book series** (seasonal/nature themes: Garden, Floral Bouquet, Autumn Harvest, Christmas, …). One website, one newsletter, one Pinterest, one method, one reader.

---

## CONTENT FUNDAMENTALS

The voice is the most defined part of this brand. Treat the Voice Charter as law. Reader-facing copy is **French only** (use `tu`, never `vous`, never `ladies`/`everyone`). The summary below preserves the English rules too, for the day English is added (currently dormant).

**The voice in one line.** A kind friend who has quietly been where you are. She speaks softly, one to one, never above you. She sits beside the reader, not in front of her. She is not a coach, expert, or cheerleader. She has nothing to sell about becoming a better version of yourself.

**Tone & casing.** Sentence case everywhere. No ALL-CAPS shouting (small-caps eyebrow labels are fine as a quiet visual device). No exclamation marks. Warm, tender, unhurried. Always `tu`. Speaks to *one* woman.

**Core attributes:** Simple · Natural · Conversational · Clear · Concise · Warm · Validating · Permission-giving · Unhurried. Elegant **through restraint** — grace comes from a plain word chosen well, not a pretty balanced sentence. *Simplicity is the elegance.*

**Rhythm.** Short sentences. Room to breathe between them. Reads slowly, like a letter or a low voice in a quiet room. Sensory and concrete (tea, light, evening, breath) over abstract.

**Moves to USE (FR):**
- Gentle invitations: *si tu veux, tu peux, quand tu te sens prête, rien ne presse, tu as le droit, prends ton temps.*
- Naming feelings plainly: *fatiguée, lourde, à vif, soulagée, assez.*
- Reassurance that normalises: *c'est normal, tu n'es pas la seule, il n'y a rien qui ne va pas chez toi.*

**The writing canon (hard rules — "drift checks"):**
1. Never open with a generality ("À l'ère de…", "Dans un monde où…", "In today's fast-paced world…").
2. **Never use an em dash** (—) for a pause. Use a full stop, comma, colon, parentheses, or split the sentence.
3. No false abstract depth. Every abstract idea is tied to a concrete scene or detail.
4. Banned structures (unless explicitly asked): *"Pas X. Pas Y. Z."* · *"Tu n'es pas X, tu es Y."* · *"Ce n'est pas X. C'est Y."* · three-fragment triads · poetic lists · wise conclusions.
5. **Avoid false-depth words.** FR: *invisible, essentiel, profond, puissant, authentique, aligné, vivant, durable, résonance, émerger, incarner, transformer, révéler, se reconnecter à soi, changer de regard.* EN (dormant): *authentic, deeply, powerful, essential, invisible, alive, aligned, sustainable, resonate, emerge, embody, transform, reveal, reconnect with yourself, journey, unlock, nurture, intentional, holistic, hold space, lean into, show up.*
6. Never chase elegance at the cost of truth. A simple specific sentence beats a balanced generic one.
7. No brand-tone / LinkedIn-coach / consultant voice. Write like one person talking to another.
8. No emoji in reader-facing copy.

**Sample sentences (the test — does it sound like her?):**
> Bonjour, et bienvenue. Je suis contente que tu sois là. Tu n'as rien à faire ni à réparer ce soir. C'est seulement un endroit calme pour déposer ce que tu portes.

> Prends ton temps. Écris seulement ce qui te semble vrai, et laisse le reste. Il n'y a pas de bonne réponse ici, seulement la tienne.

> Si la journée a été lourde, tu n'as pas à expliquer pourquoi. Certains jours demandent plus que d'autres, et se sentir fatiguée n'est pas un échec.

**Legal / safety (always):** Avoid the words *thérapie* and *thérapeutique* in public copy. Never promise mental-health outcomes — offer a practice and a place, not a cure. Include a gentle note that this is not a substitute for professional care.

**The PIVOINE method** — the named, repeatable practice (seven gentle permissions, never a checklist, never performed in order):
- **P · Poser** — you put down your phone, and what you carry.
- **I · Intimité** — it's yours, only yours. Nothing to prove, nothing to show.
- **V · Vérité** — you feel what you feel, without judging it.
- **O · Observer** — you notice the small things. A colour, the changing light.
- **I · Imperfection** — nothing to get right. Out of the lines is fine.
- **N · Nature** — you let the season in.
- **E · Émerveillement** — you find a little softness again, a small wonder.

---

## VISUAL FOUNDATIONS

The look signals a calm, safe, private space at a glance — the opposite of the loud wellness shelf. Matte, tactile, paper-like. Never glossy, never neon.

**Colour (locked palette — five colours).** Muted and desaturated. Soft pinks for warmth, two greens to ground it so it never turns saccharine.
- `--blush #F8E7E1` — lightest; page tints, soft card fills, "paper" warmth.
- `--pale-rose #EDC2BE` — gentle secondary fills, soft dividers.
- `--sage #B2BD88` — the soft green; hairline rules, small botanical accents.
- `--rose #C47A78` — the signature warm accent; the peony, a key word, small emphasis.
- `--deep-olive #656D44` — darkest; headings, strong accents, grounding.
- Added (the documented gap): a warm olive-charcoal `--ink #33321E` for body text, plus warm off-white `--paper-warm #FCF6F2`. **Keep large areas light** (white + blush) so printables stay light on ink. Colour is used sparingly, as accent — never large saturated fields.

**Type.** *Aboreto* (display, single weight) for the wordmark, book titles, page titles — set with a little letter-spacing so it breathes. *Albert Sans* for body and everything else — keeps reading calm and clear. Generous line-height (1.6 body, 1.85 for letters). Restrained sizes; never below 12px in print. Small-caps eyebrow labels (`.pp-eyebrow`) are a recurring quiet device.

**Spacing & layout.** Generous white space is part of the calm and keeps the printable light on ink. 4px base step. Comfortable reading measure ~60ch; intimate/letter copy ~42ch, often centred. Lots of breathing room around single elements. No dense dashboards.

**Backgrounds.** Mostly plain warm white or a flat blush tint. No gradients (warm two-tone washes only if very subtle). The brand's imagery is **watercolour peonies/botanicals on covers** and **fine line-art on interiors** — soft, warm, hand-illustrated, never stocky or cool/blue. ⚠️ No illustration assets were supplied; see Iconography. Coloring line-art also doubles as borders, frames, and spot illustration to unify a spread.

**Corner radii.** Gentle, never sharp, never pill-everywhere. Cards ~14px, large sheets ~22px, small tags/buttons pill.

**Cards.** Warm white fill, very soft warm shadow (olive-tinted, low), often a hairline sage or faint warm border. Quiet, resting on the page rather than floating.

**Shadows.** Warm-tinted (built from olive, never grey-blue), very low opacity — "paper resting on paper." A soft inner shadow for inset/inputs. No hard drop shadows, no glow.

**Borders.** Hairline. Sage for botanical/structural rules, pale-rose for soft dividers, a near-invisible warm `--border-faint` for quiet separation.

**Motion.** Unhurried. Gentle fades and soft eases only. **No bounce, no spring, no parallax.** Durations 140–420ms. Respect `prefers-reduced-motion`.

**Hover states.** Soft: a slight warm tint deepening (blush → blush-deep), accent rose → rose-deep, or a gentle opacity shift. Never a colour pop or scale-up jump.

**Press states.** A subtle deepening of colour and/or a barely-there settle (translateY 1px). No hard shrink, no aggressive scale.

**Transparency & blur.** Used sparingly — a soft translucent sheet over blush for overlays, light blur on a scrim behind a dialog. Never frosted-glass-everywhere.

**Imagery vibe.** Warm, soft, matte, hand-illustrated. Botanical and seasonal. Pinks and greens. Never cool, never high-contrast, never grainy-dark, never corporate stock.

---

## ICONOGRAPHY

The brand has **no documented icon system** and no icon assets were supplied. Its visual language is *botanical line-art*, not UI iconography. Two guidelines:

1. **Decorative / botanical marks** (peony, leaf, sprig, seasonal motifs) are the brand's true "icons." These should be **real hand-illustrated watercolour/line-art assets** from the founder's licensed coloring library. ⚠️ **None were provided** — this is the biggest gap in the system. The wordmark is currently set in type (Aboreto), which is legitimate, but the peony illustration that anchors the brand is missing. **Please supply** the peony motif and a few botanical line elements (PNG or SVG).
2. **Functional UI icons** (for the website: cart, menu, arrow, mail, check). No set is specified. The system uses **Lucide** (`https://unpkg.com/lucide@latest`) loaded from CDN as a substitute — its thin, rounded, single-stroke style is the closest match to the delicate, soft aesthetic. ⚠️ **This is a substitution, flagged for your approval.** If you prefer another set, say so.
- **Emoji: never** in reader-facing copy. (Used only as quick status markers inside this internal document.)
- **Unicode glyphs** are used minimally and tastefully (e.g. a middot `·` separator, a small `✦`/leaf for ornament) — kept rare.

---

## Index — what's in this system

**Foundations**
- `styles.css` — global entry point (consumers link this one file; `@import` lines only).
- `tokens/colors.css` · `typography.css` · `spacing.css` · `effects.css` · `fonts.css` · `base.css` — all CSS custom properties + `@font-face`.
- `assets/fonts/` — Aboreto & Albert Sans `.ttf` binaries.
- `guidelines/*.card.html` — foundation specimen cards (Type, Colors, Spacing, Brand) shown in the Design System tab.

**Components** (`components/`) — reusable React primitives, namespace `window.PapierPivoineDesignSystem_2e8f20`:
- `core/Button`, `core/Tag`, `core/Divider`
- `forms/TextField`, `forms/Textarea`, `forms/Checkbox`
- `surfaces/Card`, `surfaces/LetterBlock`, `surfaces/PivoineBadge`

**UI kits** (`ui_kits/`)
- `website/` — the storefront: homepage hero, product detail, freebie email capture (the marketing world).
- `journal/` — printable journal interior: welcome letter, the PIVOINE method page, a writing-prompt spread, a daily page.

**Meta**
- `SKILL.md` — makes this folder usable as a downloadable Claude Code / Agent Skill.
- `readme.md` — this file.

> Compiler-generated (do not edit): `_ds_bundle.js`, `_ds_manifest.json`, `_adherence.oxlintrc.json`.
