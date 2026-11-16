---
name: reference-chrismandel-de-design
description: "chrismandel.de: statische Cloudflare-Pages-Seite, Quellcode LIEGT lokal in workspace/chrismandel-site/ — Design-Tokens + Deploy-Weg hier notiert"
metadata: 
  node_type: memory
  type: reference
  originSessionId: 6fe18dab-d09b-406c-898c-38d23a5ae009
  modified: 2026-08-21T16:09:28.416Z
---

**⚠️ Korrektur 21.08.2026:** Ordner wurde umbenannt — heißt jetzt `chrismandel-site/`, nicht mehr `aurora-story/` (Umbenennung fand irgendwann zwischen 16.08. und 21.08. statt, ohne dass diese Notiz aktualisiert wurde → erst per `find workspace -maxdepth 2 -type d` gefunden). Bei Website-Fragen künftig IMMER zuerst per `find` den aktuellen Ordnernamen verifizieren statt sich auf den hier notierten Pfad zu verlassen — Ordnernamen können sich ändern.

**⚠️ Ältere Korrektur 16.08.2026 abends:** Frühere Version dieser Notiz behauptete fälschlich, chrismandel.de liefe auf WordPress ohne lokalen Quellcode — das war falsch. Richtig: **chrismandel.de ist eine reine statische Seite (Handschrift-HTML mit Web Components, kein Framework), gehostet auf Cloudflare Pages.** Der Essay auf `/geschichte/` sagt es sogar wörtlich: „Ich habe mir gerade meine eigene Website gebaut, und zwar ohne WordPress".

**Quellcode:** `/home/bolla/workspace/chrismandel-site/` — Struktur: `index.html` (Startseite), `aurora/index.html`, `geschichte/index.html`, `ki-forum/index.html`, `en/index.html` (EN-Startseite/Essay), `impressum/index.html`, `assets/` (Icons, Bilder), `functions/index.js` (Cloudflare-Pages-Function, nur für `/` — Geo-Redirect EN-Länder → `/en/`, per Cookie gemerkt). Jede Unterseite ist ein eigenständiges, komplett inline-gestyltes HTML-File (kein Build-Schritt, kein Bundler).

**Deploy:** Cloudflare Pages, Projekt-Name `chrismandel` (siehe `scripts/cf_pages_domain.py`, verwaltet DNS + Custom-Domain-Bindung `chrismandel.de`/`www.chrismandel.de` → `chrismandel.pages.dev`). Token liegt in `config/cloudflare_token.json` (chmod 600). Deploy selbst läuft aus `chrismandel-site/` heraus über `npx wrangler pages deploy . --project-name=chrismandel --branch=main` (ohne `--branch=main` landet's nur als Preview-Build auf einer `*.pages.dev`-Subdomain, ohne die Live-Domain zu berühren — guter Zwischenschritt). **Auto-Mode-Classifier blockiert den Deploy-Befehl standardmäßig** (Zugriff auf den Cloudflare-Token) — seit 21.08.2026 per fest umrissener Regel in `~/.claude/settings.json` (`autoMode.allow`) freigegeben, eng auf genau diesen Befehl/dieses Projekt begrenzt.

**Startseiten-Karten:** Kein "Browser-Mockup" von Hand gebaut, sondern eine Web-Component `<preview-card href="..." kicker="..." heading="..." desc="..." emoji="..." preview-kicker="..." preview-line="..." preview-url="...">` innerhalb von `<card-stack>` (auch eine Web-Component, macht Swipe/Scroll-Karussell + Dots). Neue Karte hinzufügen = einfach ein weiteres `<preview-card>`-Tag in `index.html` einfügen, direkt vor `</card-stack>`.

**Design-Tokens (CSS-Variablen, identisch in allen Seiten):**
```css
--nacht:#0d1b3d; --daemmer:#3a2b5c; --glut:#8a4a6b; --morgen:#e8896b;
--licht:#ffd9a8; --creme:#fdf6ee; --tinte:#1a1524; --grau:#6b6478;
```
Hero-Gradient: `linear-gradient(160deg, var(--nacht) 0%, var(--daemmer) 42%, var(--glut) 78%, var(--morgen) 100%)`. Fließtext-Größe auf Subpages 20-22px (großzügig, passt zu [[user_sehvermoegen]]). Schriftfamilie: System-Stack (`-apple-system, "Segoe UI", Roboto, Helvetica, Arial, sans-serif`). Subpage-Muster: `<header class="hero">` (Sprachumschalter oben rechts, `<a class="back">← zurück zur Startseite</a>`, `<div class="kicker">`, `<h1>`), dann `<article>` mit Fließtext, `<hr class="rule">` + `.bio`-Absatz, dann `.cta`-Karte mit `.btn.primary`/`.btn.ghost`-Buttons, `<footer>© Chris Mandel · chrismandel.de</footer>`.

**⚠️ Dauerregel seit 21.08.2026 — EN-Parität IMMER vor jedem Deploy prüfen:** Chris fand am 21.08. eine
Lücke (2 von 3 Dialogen auf `/ki-forum/` fehlten komplett auf `/en/dialogue/`, dazu fehlendes
Archiv-Akkordeon-CSS + falsches Datum in EN). Behoben, und als Dauerregel festgelegt: **vor jedem
`wrangler pages deploy` erst `bash scripts/check_en_parity.sh` aus `chrismandel-site/` laufen lassen.**
Das Skript vergleicht jede DE-Seite mit ihrem registrierten EN-Pendant (Zeilenzahl, mtime) und schlägt
laut fehl, wenn eine DE-Seite kein (aktuelles) EN-Pendant hat. **Bei jeder neuen Seite/Sektion, die zu
chrismandel.de hinzukommt:** sofort auch eine EN-Version anlegen UND den neuen DE-Ordner ins `MAPPING`
in `scripts/check_en_parity.sh` eintragen — sonst bricht der Check beim nächsten Deploy bewusst ab
(genau das ist der Sinn: neue Seite ohne EN darf nicht durchrutschen). Aktuelle Zuordnung: `aurora`→
`en/aurora`, `geschichte`→`en/essay`, `impressum`→`en/impressum`, `ki-forum`→`en/dialogue`, Startseite
ist als Sonderfall im Skript fest verdrahtet.

Verwandt: [[feedback_aurora_mail_website_immer]], [[reference_bolla_docs]].
