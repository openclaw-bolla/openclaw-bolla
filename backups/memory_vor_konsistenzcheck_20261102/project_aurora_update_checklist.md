---
name: project-aurora-update-checklist
description: "Master-Checkliste — eine AURORA-Textänderung sauber über ALLE 8 Kanäle (KDP + D2D + Google Play, eBook + Print, DE + EN) verteilen"
metadata: 
  node_type: memory
  type: project
  originSessionId: 067a9113-a744-43b4-a874-a76ba70d7554
---

# AURORA — Master-Update-Checkliste (alle Kanäle)

Wenn der Buchtext geändert wird (z.B. Fable-5-Optimierung aller Kapitel), muss die neue Fassung an **8 Distributionspunkte** — sonst kursieren verschiedene Versionen. Es gibt KEINE Zentrale, die automatisch verteilt; jeder Kanal braucht einen eigenen Re-Upload.

⚠️ **Drei unabhängige Schienen — Google Play ist DIREKT, nicht über D2D:** (1) **KDP** = Amazon, (2) **D2D** = Apple/Kobo/B&N etc. (D2D verteilt NICHT an Google Play!), (3) **Google Play Books** = eigenes Partner-Konto, manuell befüllt. GGKEYs in [[project-aurora-identifiers]].

## Single Source of Truth
Die **JSON ist die Quelle der Wahrheit**, alles wird daraus gebaut:
- DE: `workspace/data/ki_buch.json`
- EN: `workspace/data/ki_buch_en_adapted.json`
- ⚠️ Vor dem Ändern IMMER Backup nach `workspace/backups/` (Datum im Namen).
- ⚠️ Hartkodierte Blöcke beachten: [[project-aurora-hardcoded-blocks]] (Epilog/Vorspann/Bio teils in Build-Skripten, nicht JSON).

## Schritt 1 — Bauen (aus geänderter JSON)
- **EPUB DE+EN:** `scripts/aurora_epub_gen.py` (DE) · `scripts/aurora_epub_en.py` (EN) → `AURORA_deutsch.epub` / `AURORA_english.epub`
- **Print-Innenteil DE+EN:** `scripts/aurora_print_pdf.py` (Param de/en) → `AURORA_innenteil_{de,en}.pdf`
- **⚠️ Print-Cover NEU bauen, wenn sich die Seitenzahl geändert hat** (Rückenbreite ändert sich!): `scripts/aurora_cover_wrap.py lang pages` → `AURORA_cover_{de,en}.pdf`
- Alle Master liegen in `D:/OneDrive/Dokumente/AURORA/`. EPUB-Restscan auf alte Reste, visuell prüfen.

## Schritt 2 — Hochladen (8 Kanäle)
| # | Kanal | Was hochladen | Wie |
|---|---|---|---|
| 1 | **KDP eBook Englisch** | `AURORA_english.epub` (+ ggf. Cover `cover_kdp.jpg`) | KDP Bücherregal → eBook → Inhalt → Datei ersetzen → Veröffentlichen |
| 2 | **KDP eBook Deutsch** | `AURORA_deutsch.epub` | dito |
| 3 | **KDP Print Englisch** | `AURORA_innenteil_en.pdf` + (bei Seitenzahländerung) `AURORA_cover_en.pdf` | KDP → Taschenbuch → Inhalt → ersetzen → Veröffentlichen |
| 4 | **KDP Print Deutsch** | `AURORA_innenteil_de.pdf` + ggf. neues Cover | dito |
| 5 | **D2D Englisch** | `AURORA_english.epub` (+ ggf. Cover) | My Books → Titel → **1 Details** (Manuskript „BROWSE" / Cover „Edit shared metadata and cover") → **2 Layout** Save&Continue → **3 Preview** Haken + Save&Continue → **4 Publish** „APPLY CHANGES" → Rights → „PUBLISH MY BOOK!" |
| 6 | **D2D Deutsch** | `AURORA_deutsch.epub` (+ ggf. Cover) | dito |
| 7 | **Google Play Englisch (DIREKT)** | `AURORA_english.epub` (+ ggf. Cover) | Google Play Books Partner Center → Titel (GGKEY `RCD8HR2D4AE`) → Inhalt/Cover ersetzen → speichern. Eigenes Konto, nicht D2D! |
| 8 | **Google Play Deutsch (DIREKT)** | `AURORA_deutsch.epub` (+ ggf. Cover) | dito (GGKEY `68ES01N6JE2`) |

## Wichtige Regeln
- **ISBN bleibt gleich** bei Textkorrektur/Optimierung derselben Ausgabe — KEINE neue ISBN. (Nur echte „2. Auflage" mit großen Änderungen rechtfertigt neue ISBN.) Registry: [[project-aurora-identifiers]].
- **Verteilung dauert:** D2D pusht an die Shops, jeder Shop (Apple, Kobo, B&N…) liest die neue Datei in SEINE eigene DB ein (1–3 Tage, teils länger). Kein Live-Abruf. Kurzzeitig kann die alte Version online bleiben.
- **Bestehende Käufer** bekommen Updates NICHT automatisch (Apple/Amazon „aktualisierter Inhalt"-Mechanismus ist optional/nicht garantiert). Neue Käufer kriegen die neue Fassung.
- **Versionskennung pflegen:** kleine „Stand: MM/JJJJ"-Zeile im Impressum (DE+EN, JSON) → man sieht, welche Fassung wo live ist.
- **Fable 5** für die Optimierung: einmaliger Hochqualitäts-Task, lohnt sich — aber ~2× Opus gegen Wochenlimit, gezielt einplanen (nicht nebenbei). [[feedback-modell-auswahl]]

## Gerettete Nuggets (aus den aufgelösten Publish-Dateien)
- **Print-Format (fix):** Trim 5×8″, cremefarbenes Papier, S/W-Innenteil, Matt-Cover, EB Garamond 11,5pt Blocksatz. Seitenzahl DE 459 / EN 443 → Rückenbreite hängt daran, bei Innenteil-Änderung Cover neu via `scripts/aurora_cover_wrap.py de|en <seiten>`.
- **⚠️ UK-Mindestpreis-Falle (KDP Print):** Amazon.co.uk hat eigenen Mindestpreis (~13,60 £). UK-Preis muss aktiv darüber liegen (z.B. 13,99 £), sonst roter Validierungsfehler und Veröffentlichung blockiert.
- **Autorenexemplare nachbestellen (Geschenke):** KDP-Bücherregal → TB-Ausgabe → „…" → *Autorenexemplar bestellen* → Marktplatz **Amazon.de** → Menge. Nur Druckkosten+Versand, keine Marge (≈ 6,11 € DE / 5,92 € EN + Versand). **Prime gilt NICHT** (separater POD-Weg). Mehrere Bücher in EINER Bestellung → Versand pro Bestellung, nicht pro Buch.

Siehe auch: [[project-aurora-englisch]].
