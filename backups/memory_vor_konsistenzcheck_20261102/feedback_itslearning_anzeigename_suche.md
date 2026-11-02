---
name: feedback_itslearning_anzeigename_suche
description: itslearning-Nachrichtensuche findet Schüler nur über den KURZEN Anzeigenamen (Nachname, erster Vorname) – vor jedem Geburtstagssong-Versand per Suche verifizieren
metadata:
  type: feedback
---

Am 07.10.2026 scheiterte der Versand an Emma Sophia Michel (Timeout/"Keine Ergebnisse"), weil das Skript den vollen Listennamen suchte. In itslearning heißt sie nur "Michel, Emma"; Henny Jasmin Zock heißt "Zock, Henny" (Eva Wassermann = "Wassermann, Eva", passte). Die Schülerlisten ([[reference_schuelerlisten_7abcd]]) enthalten dagegen alle Vornamen.

**Why:** `send_private_message` in itslearning_send_private_song.py sucht per startswith() auf den Dropdown-Text; zweiter Vorname im Suchstring = kein Treffer.

**How to apply:** Für jeden neuen Geburtstagssong-Empfänger den Namen als "Nachname, Erstvorname" eintragen und VORHER per Suche ohne Senden prüfen (Screenshot des Dropdowns; Probe-Skript workspace/scripts/emma_suche_probe.py, Namen in der `for q in [...]`-Liste anpassen). Die Batch-Skripte (itslearning_geburtstagssong_batch_*.py) erst nach dieser Prüfung scharf lassen. Verwandt: [[feedback_befehl_in_zwischenablage]].
