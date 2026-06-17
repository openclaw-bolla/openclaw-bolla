# Buchprojekt → EPUB → Veröffentlichung — Prozess & Lehren (Playbook)

> Erstellt 17.06.2026 nach dem AURORA-Projekt. Damit wir beim **nächsten Buch** nicht wieder in dieselben Fallen laufen.
> Gilt für AURORA und jedes künftige Buchprojekt mit demselben Toolchain.

---

## 1. Architektur-Grundregel (WICHTIGSTE LEHRE)

**Die JSON ist die EINZIGE Wahrheitsquelle. Im Build-Skript steht KEIN Buchinhalt.**

- Alles, was im Buch als Text erscheint, lebt in der JSON-Quelle:
  `kapitel`, `vorspann` (Epigraph/Definition), `vorwort`, `impressum`, `epilog`, `epilog_untertitel`, `ueber_autor`, `danksagung`, `rezensions_bitte`.
- Im Build-Skript ist nur noch **Code + CSS** hartkodiert — kein Fließtext.
- Fehlt ein Pflichtfeld in der JSON, **bricht der Build mit Fehler ab** (kein stiller Fallback auf alten Text).

**Warum diese Regel existiert (der AURORA-Vorfall):**
Beim ersten Anlauf waren Epilog, Vorspann-Definition, Impressum und Backmatter als String-Konstanten IM Skript hartkodiert. Folge:
- Die englische **kulturelle Adaption** (Hamburg→Boston etc.) lief nur über die JSON-Kapitel → der hartkodierte **Epilog blieb deutsch** ("Marlie Braun", "Lübeck") und landete so im ausgelieferten Buch.
- Die **Vorspann-Funktion** warf den (verbesserten) JSON-Text weg und nutzte eine alte, schlechte Konstante.
- → Man konnte sich NICHT darauf verlassen, dass im Buch die freigegebene Version steht. Genau das darf nie wieder passieren.

---

## 2. Dateien & Pfade (AURORA)

| Zweck | Pfad |
|---|---|
| DE-Quelle | `workspace/data/ki_buch.json` |
| EN-Quelle (US-adaptiert) | `workspace/data/ki_buch_en_adapted.json` |
| DE-Build-Skript | `workspace/scripts/aurora_epub_gen.py` |
| EN-Build-Skript | `workspace/scripts/aurora_epub_en.py` |
| Finale EPUBs | `D:\OneDrive\Dokumente\AURORA\AURORA_deutsch.epub` / `AURORA_english.epub` |
| Cover | `D:\OneDrive\Dokumente\AURORA\cover_v6_portrait.png` (EPUB) · `cover_kdp.jpg` (KDP, kein PNG!) |
| Kindle-Versand | `workspace/scripts/kindle_send.py` → `ernstmandel_MnAuOy@kindle.com` (via Graph/Outlook) |
| KDP/D2D-Materialien | `D:\OneDrive\Dokumente\AURORA\AURORA_KDP_Materialien.md` / `AURORA_D2D_Materialien.md` |

---

## 3. Standard-Ablauf (jede Änderung am Buch)

1. **Ändern** → immer in der JSON-Quelle (nie im Skript).
2. **Bauen** → `python3 scripts/aurora_epub_gen.py` (DE) bzw. `aurora_epub_en.py` (EN).
3. **Verifizieren** (PFLICHT, siehe Checkliste §4).
4. **Kindle-Test** → `kindle_send.py` (zum Korrekturlesen). Amazon-Verifikationsmail klicken.
5. **Veröffentlichen** → KDP (Amazon) + D2D (alle anderen Shops, Amazon dort abwählen).

---

## 4. Verifikations-Checkliste nach JEDEM Build

- [ ] **Restmarker-Scan** EN: keine deutschen Namen/Orte im Text —
      `Marlie`, `Braun`, `Lübeck`, `Leni`, `Kiel`, `Hamburg` (Hamburg nur in Autoren-Bio erlaubt).
- [ ] **Restmarker-Scan** DE: keine englischen Namen/Orte — `Marley`, `Boston`, `Providence`, `Cambridge`.
- [ ] **Vorspann** prüfen (richtige Definition/Epigraph, nicht alte Fassung).
- [ ] **Epilog** prüfen (richtige Namen/Orte).
- [ ] **Backmatter** prüfen (Über den Autor / Danksagung / Rezensions-Bitte).
- [ ] EPUB-Integrität: `mimetype` als erste Datei + unkomprimiert; `zipfile.testzip()` = None.
- [ ] Optional Gegenbeweis: Text-Snapshot vor/nach diffen (muss bei reinen Strukturänderungen identisch sein).

Scan-Einzeiler (EN): EPUB entpacken, dann pro xhtml `grep` auf die Markerliste. (Achtung: `und `/`der ` sind False Positives durch englische Wörter wie "around"/"wonder".)

---

## 5. Kulturelle Adaption DE → EN (US-Markt) — Mapping

| Deutsch | Englisch (US) |
|---|---|
| Hamburg | Boston |
| (Uni/Tech-Standort) | Cambridge / Kendall Square |
| Lübeck (2. Standort/Bunker) | Providence, RI (~1 h südlich) |
| Marlie Braun | Marley Brown |
| Leni | Ellie (Yilmaz) |
| Noah / Theo Dreyer / Howell | bleiben (bzw. Khoury/Dreyer) |
| m² / °C / Komma-Dezimal | sq ft / °F / Punkt-Dezimal |
| »…« (Guillemets) | "…" (US-Quotes) |

Bewusste Plot-Geheimnisse NICHT "korrigieren" (z. B. "four letters, lowercase" = tote Tochter Aurora).

---

## 6. Veröffentlichungs-Strategie (kurz)

- **KDP** (Amazon): kein KDP Select (sonst Exklusivität → D2D verboten). 35 % Royalty bei 4,99 €.
- **D2D** (Draft2Digital): alle Shops AUSSER Amazon (Amazon beim Upload abwählen). Tolino = wichtig für DE.
- DE + EN je bei KDP **und** D2D = 4 Einreichungen, jeder Shop genau einmal.

---

## 7. Lehren in einem Satz

> **Build-Skripte enthalten Logik, keine Prosa.** Jeder Buchtext lebt in der JSON, der Build bricht bei fehlendem Feld ab, und nach jedem Build wird mit einem Restmarker-Scan geprüft — erst dann gilt eine EPUB als final.
