---
name: feedback-itslearning-workflow-bewaehrt
description: "itslearning-Post-Workflow (Mitteilung+Anhänge an 4 I/II-Kurse) am 23.07.2026 live getestet und von Chris als \"perfekt\" bestätigt — Standard für 19 Kurstage im Schuljahr 26/27"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 14c2129c-e27a-4adc-aece-dbffd934513e
  modified: 2026-08-31T11:10:17.913Z
---

Der End-zu-Ende-Workflow über `/home/bolla/workspace/scripts/itslearning_post_kurstag.py` (Standard-Paket
automatisch aus Handouts-Ordner sammeln, individuelle Mitteilungstexte pro Kurs, Veröffentlichen) wurde am
23.07.2026 live an den 4 "I"-Kursen getestet und von Chris explizit als "sensationell... perfekt... top"
bestätigt — genau wie es sein soll.

**Warum wichtig:** Chris braucht diesen Workflow laut eigener Ansage **19 Mal im Schuljahr 26/27**
(passend zu den 19 Themen aus [[project_schuljahr2627]]). Das ist kein Einmal-Test, sondern DER
Standard-Ablauf für jeden Kurstag.

**How to apply:** Bei jedem künftigen "itslearning + Kurstag N"-Auftrag genau dieses Skript als Basis
nehmen (siehe [[project_itslearning_automation]] für alle DOM-Fallstricke/Selektoren) — nur `DAY_PREFIX`
und die 4 Mitteilungstexte pro Lauf anpassen (Texte immer neu formulieren, nie kopieren, siehe
[[feedback_ki_texte_natuerlich]]). Nicht das Rad neu erfinden oder Struktur in Frage stellen, das Muster
ist geprüft und funktioniert.

**🐞 Zwei Skript-Bugs gefixt (31.08.2026, Kurstag 3):**
1. **Gleicher Basename → Anhang wird wieder abgewählt.** `03-Praktikum.html` + `03-Praktikum.pdf` haben
   im Ressource-Anhang-Dialog denselben sichtbaren Namen „03-Praktikum". Die alte Schleife klickte
   dieselbe Checkbox 2× → toggelt sie wieder AUS → Praktikum-Link fehlte in 3 Mitteilungen (mussten
   gelöscht + neu gepostet werden). Fix in `post_message()`: `seen_basenames`-Set, pro Basename nur
   1× anhängen. Konsequenz: bei zwei Dateien mit gleichem Namen wird nur EINE als Mitteilungs-Link
   verlinkt (die erste = i.d.R. .html), die andere liegt trotzdem in den Ressourcen. Wenn beide als
   Link gebraucht werden → eine Datei umbenennen (z. B. `NN-Praktikum-interaktiv.html`).
2. **Lange Ressourcenliste → Zieldatei außerhalb des gerenderten Bereichs.** In Kursen mit vielen
   Ressourcen (7a I: Halloween, Black Stories, Memory, Sound-Ordner …) fand `get_by_text(basename)`
   die Datei nicht (`count()==0`), Post schlug fehl. Fix: im Anhang-Dialog bis zu 20× per
   `mouse.wheel(0,500)` nach unten scrollen und erneut suchen, dann `scroll_into_view_if_needed`.
   Beide Fixes am 31.08. live an allen 4 „I"-Kursen bestätigt (4× OK, Screenshots gegengeprüft).

**Löschen einzelner Mitteilungen:** `itslearning_delete_latest_message.py` löscht die JEWEILS NEUESTE
Mitteilung pro Kurs — `COURSES` VOR jedem Lauf explizit auf die richtigen Kurse setzen (am 31.08. auf
3 Kurse gesetzt, damit die fehlgeschlagene 7a I NICHT ihre legitime Kurstag-2-Mitteilung verliert).

**✅ Erweiterung bestätigt (17.08.2026):** Vor dem eigentlichen Live-Post-Lauf zusätzlich IMMER einen
kurzen Vorab-Check der Inhalte machen — Daten gegen `data/schuljahr2627.json` (`termine[]`) verifizieren,
Texte auf Tippfehler/falsche Wochentage lesen, `discover_files()` einmal separat aufrufen und die
gefundene Dateiliste gegenchecken, BEVOR das Post-Skript live läuft. Hat bei diesem Lauf einen echten
Fehler gefunden (falsches Datum "19.08." bei 7a I/7c I statt korrekt 20.08.) — Chris hat explizit danach
gefragt ("kannst du vorher die Inhalte kurz auf Fehler checken") und das Ergebnis + den Ablauf
insgesamt als "passt alles, soll jetzt erst mal so bleiben" bestätigt. Dieser Vorab-Check ist damit
fester Bestandteil des Standard-Workflows, nicht nur eine Ausnahme für diesen einen Lauf.
