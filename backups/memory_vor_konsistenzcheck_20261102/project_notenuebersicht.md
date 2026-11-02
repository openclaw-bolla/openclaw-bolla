---
name: project-notenuebersicht
description: Notenübersicht 7a-7d aus School-SH-Export erstellt (12.08.2026) — Skript + Annahmen für künftige Wiederholungen
metadata: 
  node_type: memory
  type: project
  originSessionId: 69a38b8d-d60d-499e-89a9-4518940336fa
  modified: 2026-08-12T16:08:49.306Z
---

Chris hat School-SH-Notenexporte (`export_schueler_*.xls`, je Klassenordner unter `D:\OneDrive\
Dokumente\Office\7. Klassen\7x\`) zu kompakten Notenübersichten verdichten lassen — eine
`Notenuebersicht_7x.xlsx` pro Klasse, im jeweiligen Klassenordner, mit 4 Spalten: Nachname, Vorname,
Durchschnitt (gewichtet), Auffällige Noten.

**Skript:** `scripts/schuljahr2627_notenuebersicht.py` — liest die alten `.xls`-Exporte (BIFF-Format,
braucht `xlrd`, war per `pip3 install --user --break-system-packages xlrd` nachzuinstallieren, `openpyxl`
war schon da), parst Fach-Spalten dynamisch aus der Kopfzeile (Fächer unterscheiden sich zwischen
Klassen — 7a/7b haben zusätzlich Französisch+Physik, 7c/7d nicht), nutzt die letzte verfügbare Note
(2. HJ des Vorjahres, das laufende Schuljahr ist ja noch leer).

**Von Chris bestätigte Annahmen (12.08.2026, gilt als Standard für Wiederholungen):**
- **Hauptfächer 3-fach gewichtet:** Deutsch, Mathematik, Englisch. Alle anderen Fächer (inkl.
  Französisch/Physik, wo vorhanden) zählen einfach.
- **"Auffällige Noten"** = Note 1 ODER Note ≥5 (2er/4er gelten nicht als auffällig). Sortierung: erst
  die 1er, dann die schlechtesten zuerst. Maximal 3 pro Schüler, Format `"Kurzname Note"` (z.B. „Bio 1"),
  Kurznamen-Mapping steht im Skript (`KURZNAMEN`-Dict).
- **Eine Ausgabedatei pro Klasse** (nicht eine kombinierte Liste über alle 4 Klassen).
- Stichproben-Rechnung von Hand nachvollzogen und bestätigt korrekt (Amoabing 7a: 47/16 = 2,94).

**How to apply bei Wiederholung** (z.B. nächstes Halbjahr/Schuljahr): neue Export-Datei ins jeweilige
Klassenordner legen (Namensmuster `export_schueler_*.xls` bleibt gleich), Skript einfach erneut laufen
lassen — überschreibt die alte `Notenuebersicht_7x.xlsx`. Keine Rückfrage zu den Annahmen mehr nötig,
sind jetzt Standard.
