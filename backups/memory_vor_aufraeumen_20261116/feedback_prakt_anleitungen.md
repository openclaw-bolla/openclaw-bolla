---
name: feedback-prakt-anleitungen
description: "Trigger \"prakt XXX\" in MP-Chat → interaktive .html-Praktikumsanleitung für EDV 7. Klasse erzeugen, in 7er-Ordner speichern"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 285a3c63-b3c2-4390-8ef7-25284266bf0a
  modified: 2026-09-30T08:20:55.137Z
---

Wenn Chris in der MP-Chat (Bolla-Chat) einfach **"prakt [Thema]"** hinwirft, ist das die Kurzform für: erstelle eine **interaktive .html-Datei** mit einer **Schritt-für-Schritt-Praktikumsanleitung** zu diesem Thema.

**⚠️ Format-Update 13.07.2026:** Früher war das Format reines `.txt` — Chris hat am 13.07.2026 einen ersten HTML-Prototyp (`1-Praktikum.html`) gesehen und ausdrücklich gesagt: **"sehr starke Seite, super, bitte merken ab jetzt immer so"**. Ab sofort also IMMER `.html` statt `.txt` für Praktikumsanleitungen, im gleichen Stil wie `1-Praktikum.html` (liegt als Referenz/Vorlage im 7er-Ordner). Der Wechsel kam aus einer Diskussion um papierloses Unterrichten + Dateiverwaltungs-Übung, Details: [[project_schuljahr2627]].

**Inhaltsquelle (Klarstellung 09.07.2026, weiter gültig):** Der Inhalt wird **aus der zum Thema gehörigen .pptx-Datei im 7er-Ordner abgeleitet** — nicht frei erfunden. Also erst die passende .pptx (Namensmuster `N-Thema.pptx`, N = Kurstag-Nummer) suchen/lesen und die Praktikumsaufgaben daraus destillieren (die wichtigsten/praktisch übbaren Inhalte der Folien als Übungsschritte), nicht am Foliensatz vorbei ein eigenes Thema erfinden.

**Stil-Vorlage `1-Praktikum.html` — konkret nachbauen:**
- Einzelne, in sich geschlossene HTML-Datei (kein Server, keine externen Bilder/Fonts/CDN-Links) — muss vom USB-Stick aus offline funktionieren.
- Großzügige Schriftgrade (Fließtext ~20px, Überschriften 22-30px) — vgl. [[feedback_ppt_schriftgroesse]], gilt hier genauso.
- Jeder Schritt als eigene "Karte" mit nummeriertem Kreis-Icon, klar abgesetzt.
- **Wichtig-Hinweise** (z.B. "immer auf dem Stick arbeiten") als auffällige rote/farbige Box oben, nicht im Fließtext versteckt.
- Lückentext-Stellen als echte `<input type="text">`-Felder zum Ausfüllen.
- Jeder Schritt-Karte eine **Häkchen-Box "Erledigt"** + eine Fortschrittsleiste oben, die live mitzählt.
- Ganz unten ein **"🖨️ Antworten als PDF speichern"-Knopf** (`window.print()`, mit `@media print`-Regel die Häkchen/Fortschrittsleiste ausblendet) — einzige Möglichkeit, ausgefüllte Textfelder dauerhaft zu sichern, da eine lokal geöffnete HTML-Seite selbst nichts speichern kann (kein Server dahinter).
- **⚠️⚠️ Korrektur 14.09.2026 — KEINE PDF-Version für `NN-Praktikum.html` mehr:** Die Vorgabe vom
  24.08.2026 (unten, durchgestrichen) ist aufgehoben. Chris: "wir hatten vereinbart das ich die
  xx-Praktikum dateien nicht als pdf benötige." Grund: der eingebaute "🖨️ Antworten als PDF
  speichern"-Knopf deckt das für die Schüler schon ab, eine zusätzliche leere Vorlagen-PDF von mir ist
  überflüssig. Ab jetzt: **nur noch die HTML-Datei**, keine begleitende `NN-Praktikum.pdf` mehr erzeugen
  oder in `Praktikum/` ablegen. ~~Zusätzlich zur `NN-Praktikum.html` IMMER direkt auch eine leere
  `NN-Praktikum.pdf` erzeugen und ebenfalls in `Praktikum/` ablegen (WeasyPrint,
  [[feedback_html_pdf_weasyprint]]).~~ Gilt NICHT für das Folien-PDF (PPTX→PDF, s.u.) — das bleibt.
- Farbschema/Look: helles iOS-artiges Design (siehe Code in `1-Praktikum.html` für exakte Farbwerte/CSS).

**⚠️ Umfang bei Erstkontakt-Mechaniken: KÜRZEN statt mehr Text (Entscheidung 27.08.2026):** Wenn ein
Praktikum eine Handbewegung/Mechanik einführt, die die Klasse noch nie gemacht hat (z. B. das allererste
Ordner-/Datei-Praktikum, bevor Rechtsklick→Neu, Doppelklick, Stick-Navigation sitzen) — Umfang von
vornherein kleiner ansetzen als beim Standard-40-Minuten-Maß, NICHT durch noch mehr erklärenden Text
kompensieren. Hintergrund: Am 27.08.2026 schaffte die Mehrzahl einer Klasse bei `01-Praktikum.html` in
einer vollen Stunde nur Schritt 0-4 von 12 (siehe [[feedback_praktikum_vorkenntnisse_accounts]]) — der
Engpass war reine Ungeübtheit mit Maus/Menü, kein Textverständnisproblem. Mehr Text würde schwächere
Leser zusätzlich bremsen, ohne die Klickgeschwindigkeit zu erhöhen.
- Konkret: Bei Erstkontakt-Themen die Kernschritte auf ca. die Hälfte des sonst üblichen Umfangs planen,
  den Rest wie in `02-`/`03-Praktikum.html` bereits vorgemacht als <span class="opt-badge">optional</span>
  markieren, statt sie verpflichtend zu machen.
- Sobald eine Mechanik in einem späteren Praktikum wiederholt wird (nicht mehr Erstkontakt), gilt das
  NICHT mehr — dort darf/soll wie bisher kompakter zusammengefasst werden (bestätigt durch Review von 02/03
  am 27.08.2026 — dort kein Änderungsbedarf).
- Gilt nur für künftig NEU erzeugte Anleitungen, keine rückwirkende Änderung an bereits ausgeteilten
  `01/02/03-Praktikum.html`.

**⚠️ Nur schüler-relevante Inhalte üben (Chris-Vorgabe 31.08.2026):** Ein Praktikum soll die
Handgriffe/Shortcuts drillen, die die Schüler:innen im Alltag **tatsächlich regelmäßig brauchen**
(Strg+C/V/X/Z, Strg+S, Strg+A, Strg+F, F2, Entf, Doppelklick, Rechtsklick→Neu). Selten genutzte
Spezial-Shortcuts **raus** — konkret gestrichen: `Strg + Umschalt + N` (neuer Ordner per Tastatur;
Ordner legt man realistisch per Rechtsklick→Neu an). Und: was eine vorgeschaltete Anleitung/Vorübung
schon abdeckt (z. B. „Textdatei anlegen" aus `03-Textdatei-Anleitung.html`), im Praktikum selbst
**nicht nochmal als eigenen Schritt** bringen — höchstens ein Ein-Zeilen-Fallback-Hinweis im
`zusatz`-Kasten für den Fall, dass die Datei fehlt. Beispiel-Umbau: `03-Praktikum.html` am 31.08.2026
von 11 auf 10 Schritte gekürzt (alter Schritt 0 „Ordner vorbereiten" mit Strg+Umschalt+N raus, alter
Schritt 1 „Textdatei anlegen" raus, Rest baut jetzt auf `Voruebung\Notiz` aus der Vorübung auf).

**⌨️ Tastenname „Shift", nie „Umschalttaste"/„Umschalt" (Chris 02.09.2026):** In allen Anleitungen und
Folien die Shift-Taste so schreiben — auch in Kombis (`⊞ Windows + Shift + S`). Details/Geltungsbereich:
[[feedback_taste_shift_nicht_umschalt]].

**⚠️⚠️ PDFs erzeugt IMMER Bolla — endgültig gemerkt (Chris 31.08.2026):** JEDES PDF für einen
Kurstag ist meine Aufgabe, nie Chris'. Das gilt ausdrücklich auch für das **Folien-PDF** (PPTX→PDF,
z. B. `03-Basics Office - Tastatur.pdf` aus der gleichnamigen .pptx) — NICHT „mach das in PowerPoint"
zurückgeben. Methode steht schon bereit: `powershell.exe -File
'C:\...\workspace\scripts\pptx_to_pdf.ps1' -PptxPath <pptx> -PdfPath <pdf>` (PowerPoint-COM,
`SaveAs(...,32)` = ppSaveAsPDF; MS-Qualität, siehe [[project_schuljahr2627]]). Ablage: das erzeugte
Folien-PDF nach `Handouts/Praktikum/` (damit `discover_files` im Post-Skript es beim Präfix findet).
Für die HTML-Praktikums-PDFs weiterhin WeasyPrint ([[feedback_html_pdf_weasyprint]]).

**⚠️ Verweise auf Ordner/Dateien aus früheren Praktika IMMER auf Zugriffbarkeit prüfen (Chris-Korrektur 30.09.2026):**
`03-Praktikum.html` verwies auf Ordner/Dateien, die Schüler in vorherigen Praktika (Kurstag 1/2) hatten
anlegen sollen — die aber laut Anleitung am Ende des jeweiligen Praktikums wieder gelöscht wurden. Beim
Aufbau von `03` war der Verweis dadurch ins Leere: die Schüler hatten die referenzierten Ordner/Dateien
gar nicht mehr im Zugriff. Chris hat es diesmal selbst gerichtet, für `03` muss ich nichts mehr ändern.
- **How to apply:** Vor JEDER neu gebauten Praktikums-HTML alle Verweise auf Ordner/Dateien aus
  früheren oder vorbereitenden Praktika/Vorübungen einzeln durchgehen und prüfen: (a) wurde dieser
  Ordner/diese Datei in einem früheren Schritt überhaupt angelegt (noch nicht existent, wenn zu früh
  referenziert), und (b) wurde er/sie in einem späteren Schritt desselben oder eines dazwischenliegenden
  Praktikums wieder gelöscht (nicht mehr existent, wenn zu spät referenziert). Nur Verweise auf Stand
  verwenden, der zum Zeitpunkt des NEUEN Praktikums nachweislich noch vorhanden ist — im Zweifel den
  vorherigen `NN-Praktikum.html`-Text konkret nachlesen statt aus dem Gedächtnis/der Annahme heraus zu
  referenzieren.
- **Why:** Löschen am Ende eines Praktikums (z.B. Aufräum-Schritt) ist normale Praxis — aber macht
  Referenzen aus späteren Anleitungen auf genau diese Ordner/Dateien automatisch ungültig, wenn nicht
  gegengecheckt wird.

**Weiter geltende Vorgaben (unverändert):**
- Umfang eng halten: nur die reine Bedienung/Übung, kein unnötiger Drumherum-Kontext (vgl. [[feedback_schueler_anleitungen_format]])
- **KEINE Abschlusszeile** wie „Fertig! Melde dich, wenn du durch bist." o. ä. (Chris-Korrektur 09.07.2026) — Anleitung endet einfach mit dem letzten Arbeitsschritt (ggf. mit dem PDF-Speichern-Knopf als natürlichem Abschluss).
- **Immer auf dem USB-Stick arbeiten, NIE auf dem Desktop** (Chris-Vorgabe 09.07.2026) — bei jeder Übung, die Ordner/Dateien anlegt, als erste(n) Schritt(e) explizit zum Stick wechseln lassen (Explorer > Dieser PC > Stick-Laufwerk) und als Warnhinweis-Box hervorheben.
- **Zielgruppe hat kaum Vorerfahrung** (Chris-Einschätzung 09.07.2026, ~60% der Klasse): Schritte extrem kleinteilig, Begriffe wie Rechtsklick/Doppelklick/Adressleiste ausschreiben statt voraussetzen. Details: [[project_schuljahr2627]].
- Dauer: Inhalt für **ca. 40 Minuten** praktisches Arbeiten dimensionieren (Chris-Vorgabe 24.08.2026, vorher 35 — gilt ab jetzt als Standard-Vorlage, außer Chris nennt für einen konkreten Kurstag explizit eine andere Zahl)
- Zielgruppe: **7. Klasse** — Altersgruppe beachten (Sprache einfach/klar halten, vgl. [[feedback_schueler_texte_ton]] für Ton bei Schüler-Texten)
- Speicherort: **`Handouts/Praktikum/`-Unterordner** (KEIN Klassenordner wie 7a/7b/7c/7d) = `D:\OneDrive\Dokumente\Office\7. Klassen\Handouts\Praktikum` (WSL: `/mnt/d/OneDrive/Dokumente/Office/7. Klassen/Handouts/Praktikum`) — ⚠️ **Korrektur 11.08.2026:** Nur die `NN-Thema.pptx`-Arbeitsdatei bleibt flach in `Handouts/`. `NN-Praktikum.html` UND das zugehörige `NN-....pdf` gehören BEIDE in `Praktikum/` (Chris: "die pdfs gehören da auch rein" — Trennung ist "Chris' Arbeitsdatei" vs. "was an Schüler geht"). `itslearning_post_kurstag.py` durchsucht beide Orte automatisch, unabhängig vom Dateityp. Details: [[project_schuljahr2627]].
- **Dateiname-Konvention:** `NN-Praktikum.html`, wobei NN die **zweistellige Nummer des Kurstages** ist, mit führender Null bei 0-9 (passend zur bestehenden Nummerierung der .pptx-Dateien im Ordner, z.B. `01-Praktikum.html` für Kurstag 1, `12-Praktikum.html` für Kurstag 12) — Grund für die führende Null: [[project_schuljahr2627]] (Windows sortiert alphabetisch, nicht numerisch)

**Why:** Chris will bei Bedarf schnell eine einsatzfertige, papierlose Praktikumsanleitung ohne jedes Mal die Vorgaben neu erklären zu müssen — "prakt XXX" soll als Kurzbefehl reichen. HTML statt .txt, weil es genauso überall (auch vom Stick) offline läuft, aber deutlich besser lesbar/formatierbar ist und sich fürs papierlose Unterrichtsjahr 26/27 anbietet.

**How to apply:** Sobald eine Chris-Nachricht mit "prakt" + Thema reinkommt (auch wenn diktiert/mit Tippfehlern), sofort die `.html` nach obigem Muster (Stil von `1-Praktikum.html` kopieren) erzeugen und im 7er-Ordner ablegen, ohne erst nachzufragen — nur bei echter Unklarheit zum genauen Thema/Unterordner kurz nachhaken.
