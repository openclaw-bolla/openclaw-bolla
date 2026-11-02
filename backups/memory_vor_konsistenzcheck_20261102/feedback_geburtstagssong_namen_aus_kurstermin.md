---
name: feedback-geburtstagssong-namen-aus-kurstermin
description: Geburtstagssong-Namen (Mo-Reminder) selbst auflösen über Kurstermin-Liste (Klassen der Woche + Gruppe I/II → Ordner Kurs I/II), keine Rückfragen
metadata:
  type: feedback
---

Chris nennt montags nur Vornamen (2 für Mi, 2 für Do). Ich löse sie SELBST auf, ohne Rückfrage (27.10.2026, nach Fehler: Songs in „Kurs II“ gesucht statt „Kurs I“, Mika-Rückfrage unnötig).

**Why:** `data/schuljahr2627.json` termine[] liefert pro Datum die Klassen + Gruppe (I/II). Mi-Paar = Klassen vom Mittwoch, Do-Paar = Klassen vom Donnerstag; Vorname gegen `data/schueler_stammdaten.json` nur in diesen Klassen suchen → praktisch immer eindeutig (27.10.: Mi 7d+7b → Thore Kuhn, Mika Henneberg; Do 7a+7c → Merle Hutterer, Lena-Sophie Brühl). Gruppe I → Ordner `7x/Kurs I/`, Gruppe II → `Kurs II`.

**How to apply:** Reihenfolge der Namen = Mi, Mi, Do, Do. Dann Songs in `…/7. Klassen/7x/Kurs <Gruppe>/` suchen (Suche per Vorname, rekursiv), itslearning-Anzeigename „Nachname, Erstvorname“ per Dropdown-Probe prüfen ([[feedback_itslearning_anzeigename_suche]]; Doppelvornamen wie „Lena-Sophie“ voll), Batch-Skript nach Vorlage `itslearning_geburtstagssong_batch_2810.py` + Cron 14:05. Nur bei echter Mehrdeutigkeit in den Klassen der Woche nachfragen.
