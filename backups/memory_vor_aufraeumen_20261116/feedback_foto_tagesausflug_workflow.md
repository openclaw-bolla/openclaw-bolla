---
name: feedback-foto-tagesausflug-workflow
description: Fester Workflow für Urlaubs-/Tagesausflug-Fotos vom Duo — Ordner pro Ort, umbenennen, danach löschen (Duo+OneDrive)
metadata:
  node_type: memory
  type: feedback
  originSessionId: current
  modified: 2026-07-26T20:21:33.333Z
---

Chris will diesen Workflow **grundsätzlich bei jeder Reise UND bei einzelnen Tagesausflügen**, nicht nur
bei der Sommerreise 2026 — als Standard-Vorgehen von mir aus anbieten/anwenden, sobald er unterwegs fotografiert
und abends darüber spricht.

## Ablauf
1. **Quelle:** Fotos vom Duo landen automatisch in `OneDrive/Bilder/Eigene Aufnahmen_Backup` (Root-Ebene,
   Dateinamen `IMG_YYYYMMDD_HHMMSS...` bzw. `video_YYYYMMDD_HHMMSS...` — Datum/Uhrzeit steht im Namen,
   kein EXIF-Parsing nötig).
2. **Zielstruktur:** ein Trip-Ordner in OneDrive (Name je nach Anlass, z.B. `Süddeutschland 2026`), darin
   pro Tag ein Unterordner benannt nach dem/den besuchten Ort(en).
3. **Mehrere Orte am selben Tag:** Chris nennt abends eine ungefähre Uhrzeit-Grenze zwischen den Orten.
   Dateien werden dann einzeln nach dem jeweiligen Ort benannt (nicht nach dem kombinierten Ordnernamen),
   chronologisch nummeriert: `Ort (1)`, `Ort (2)` ...
4. **Nicht-Reise-Tage ausschließen:** Tage, die nicht zur eigentlichen Reise/zum Ausflug zählen (z.B. ein
   Familienbesuch unterwegs), werden vom Workflow nicht angefasst — Chris sagt vorher, was zählt.
5. **Reihenfolge:** erst nur kopieren+umbenennen (nicht-destruktiv) → Chris zur Kontrolle zeigen → **erst
   nach explizitem OK** die Originale löschen, und zwar sowohl in `Eigene Aufnahmen_Backup` als auch direkt
   auf dem Duo (`/sdcard/DCIM/Camera/`, per ADB).
6. **Kein Cron/Automatik:** Chris stößt das jeweils abends bewusst im Chat an, weil die ADB-Verbindung bei
   jedem Netzwerkwechsel neu verbunden werden muss (Pairing bleibt bestehen, Connect-Port ändert sich aber
   jedes Mal) — siehe [[user_duo2]] für den genauen Reconnect-Ablauf.

## Technische Fallen (gelernt 26.07.2026)
- OneDrive-Pfade mit Leerzeichen im `for f in $(find ...)` brechen durch Bash-Wortsplitting — immer
  `find ... -print0 | while IFS= read -r -d '' f` verwenden.
- Große Dateien über den OneDrive-9p-Mount können den 2-Minuten-Bash-Timeout reißen — bei Videos/vielen
  Fotos in Batches arbeiten und Zwischenstand (0-Byte-Reste) prüfen, bevor man weitermacht.
- `adb shell` **innerhalb** einer `while read`-Schleife, die selbst aus einem anderen `adb shell`-Aufruf
  gespeist wird (Pipe oder Process-Substitution), frisst das stdin der Schleife und bricht nach der ersten
  Iteration ab. Fix: `adb shell "..." < /dev/null`.
- Nach jedem Schritt (Kopieren, Löschen) die Gegenprobe machen: Byte-Summe Quelle=Ziel beim Kopieren,
  leere Kontroll-Suche beim Löschen — Chris legt großen Wert darauf, dass hier nichts schiefgeht
  ("damit mein Chaos nicht noch größer wird").

**Why:** Chris fotografiert unterwegs ausschließlich mit dem Duo, will aber sofort geordnete Reise-Ordner
statt alles unsortiert in `Eigene Aufnahmen_Backup` liegen zu lassen — bewusst getrennt vom größeren,
noch ungelösten Foto-Chaos-Thema ([[project_foto_organisation]]).

**How to apply:** Sobald Chris von einer Reise/einem Tagesausflug erzählt und Fotos gemacht hat, diesen
Workflow proaktiv anbieten — Ordnerstruktur + Ablauf, nicht erst warten bis er es im Detail vorgibt.
