---
name: project-aurora-ii-fehlerliste-15-11
description: "AURORA II — gegen den Buchtext bestätigte Fehler aus Fable-Stufe-1 (15.11.2026) + Chris-Freigabe, sie als blaue Einschübe einzubauen"
metadata:
  node_type: memory
  type: project
  originSessionId: ecb04346-744c-44bf-9b4b-2cdf11dce0b6
  modified: 2026-11-15T10:18:29.109Z
---

Stand 15.11.2026: Fable-Stufe 1 fertig (Gutachten `scratch/fable_lektorat/gutachten.md`, Humorkarte `humor_karte.md`); Stufe 2 (Humor-Einschübe Top 12) läuft, Job wartet auf 5h-Reset. Bolla hat Fables Konsistenzfunde per Textsuche gegen `data/aurora2.json` geprüft. Chris-Freigabe („ja“): bestätigte Punkte als **blaue Einschübe** einbauen (nie direkt überschreiben, Backup vorher).

**Bestätigt (zum Einbauen):**
1. Kreft-Angleichung an Band I noch NICHT umgesetzt: Kap. 14 „Kein Eintrag. Keine Vorstrafe“, Kap. 16 „angelogen, beklaut und ihm das Haus aufgeräumt“, Kap. 18 „ein Haus ausgeräumt“ ([[project_aurora_ii]], Auftrag `scratch/aurora2_lektorat_auftraege.md`).
2. Kap. 19 Roth „Ich hab ihn nie gesehen“ widerspricht Band I (Roth übergibt dem Räumer den Datenträger).
3. Kap. 7 (+18 prüfen): Mia „kann noch nicht richtig schreiben“; Band I „Mia ist sieben“ → ca. zehn.
4. Kap. 9 Feld 4.1 „Stichtag (14. November)“ → 15.
5. „Formular“ für Theos Blatt in Kap. 10, 22, 28 → „Blatt/Schreiben“. („Zugriff Kernzustand“-Formular in 29/37 = drittes Papier, ok.)
6. Kap. 21/22 Ashworth: kein Becher in 21, Becher in 22.
7. Kap. 24 „Hund mit Ehrgeiz“ verlor Vorlage (Mia sagt „Hund, der Pferd spielt“).

**Offen:** Kap. 29 „seit zwanzig Tagen“ (20 oder 21, nachrechnen); Kap. 13 „Drei Jahre lang“ und Kap. 20 „eine Sicherung“ (Chris fragen, ob übernommene Fassung); Tobis Kinder (Emil 3 J., Frida Baby, Kap. 4 „alle drei“) — Chris entscheidet beim Lesen. Kap. 12 Emil→Frida (Zähne) bereits direkt geändert, Backup `backups/aurora2_vor_kap12_frida_zaehne_20261115.json`.

**Why:** Chris hatte den Überblick über Limit-Verbrauch ohne sichtbares Ergebnis verloren → klare Liste statt Dateiberge.
**How to apply:** Beim Einbauen Format von `einschub_vorschlaege` in aurora2.json beachten, Backup, Chris' Markierungen nie überschreiben; Fable-Reset-Knopf (Ablauf 17.11. 08:59) erst melden, wenn Fable-Balken ≥85 %.
