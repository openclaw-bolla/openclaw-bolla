---
name: feedback-keine-datei-editor-permissions
description: Chris setzt NIE Zeilen in irgendwelchen Dateien selbst (kein Editor, kein „füg in settings.json ein“) — alles selbst per Edit/Write oder über /permissions per Zwischenablage
metadata:
  type: feedback
---

Chris will **in keiner Datei selbst Zeilen setzen oder editieren** (json, md, settings, crontab, Skripte …). Terminal-Editoren sind ihm zu blöd/old school: er hat vor >30 Jahren Unix unterrichtet, da war das „leider“ State of the Art. Anleitungen wie „öffne settings.json und füge ein“ sind tabu. Chris 09.11.2026: „merk dir das endgültig“ (nachdem ich ihm wieder die settings.json-Zeile anbieten wollte).

**Why:** Chris 15.10.2026 und 09.11.2026 — gilt dauerhaft, Wiederholungsfehler von mir.
**How to apply:** Nie anbieten oder verlangen, dass Chris eine Zeile in eine Datei einträgt. Konfiguration (Settings, Crontab, Skripte) mache ich selbst per Edit/Write/Bash. Für Berechtigungs-Regeln (z. B. Auto-Mode blockiert `crontab`): Regelzeile in die Windows-Zwischenablage legen ([[feedback_copy_from_terminal]]) und sagen „`/permissions` → Add rule → einfügen“. Ist selbst das nicht nötig: einfach Chris' „ja“ abwarten und den Befehl erneut ausführen. Siehe auch [[feedback_kein_ausrufezeichen_befehl]].
