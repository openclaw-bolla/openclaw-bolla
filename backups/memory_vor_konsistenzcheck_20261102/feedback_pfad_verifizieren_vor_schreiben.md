---
name: feedback-pfad-verifizieren-vor-schreiben
description: "Vor jedem Datei-Schreiben in einen 'logisch klingenden' Zielordner erst prüfen, dass er der ECHTE, bereits genutzte Ordner ist — falscher Pfad ist ein No-Go"
metadata:
  node_type: memory
  type: feedback
  originSessionId: current
  modified: 2026-09-07T07:54:26.214Z
---

Falscher Zielordner/-pfad beim Ablegen von Dateien ist ein **No-Go** — das hatten Chris und ich schon
mal vereinbart, ist aber am 06./07.09.2026 trotzdem passiert (Lüneburg-Fotos landeten in
`D:\OneDrive\Bilder\Mandels\2026\` statt im echten, aktiv genutzten `D:\OneDrive\Mandels\2026\` —
siehe [[reference_onedrive_mandels_pfad]]). Kostete danach ~90 Minuten Fehlersuche in die falsche
Richtung (Modern-Standby-Theorie, OneDrive-Sync-Engine-Restart, natives Rename/Copy, Explorer.exe-Neustart),
bevor der eigentliche Fehler (zwei parallele "Mandels"-Ordner) auffiel.

**Why:** Ein plausibel klingender Pfad (`Bilder\Mandels\2026` für Familienfotos) ist NICHT dasselbe wie
der tatsächlich von Chris genutzte Pfad. Wenn ich einen Zielordner nicht aus einer vorherigen, verifizierten
Aktion kenne, sondern ihn aus der Anfrage ableite/konstruiere, ist die Wahrscheinlichkeit für genau diesen
Fehler hoch — und die Folgeschäden (Chris sucht, ich suche in die falsche Richtung) sind teuer.

**How to apply — VOR jedem Schreiben in einen abgeleiteten/konstruierten Zielpfad:**
1. `ls`/`find` auf den Zielordner (und ggf. Geschwisterordner) VOR dem Schreiben — sieht der Inhalt
   plausibel nach "das ist Chris' aktiv genutzter Ordner" aus (Datumsspanne, Dateitypen, Themen passend)?
   Ein leerer oder fast leerer Ordner an einer Stelle, wo Chris seit Jahren Inhalte ablegt, ist ein
   Warnsignal, nicht ein Freifahrtschein zum Anlegen.
2. Bei Unsicherheit: lieber einmal `find /mnt/d/OneDrive -type d -iname "<zielordnername>"` über den
   ganzen Baum laufen lassen, um Parallel-/Alternativordner zu entdecken, BEVOR geschrieben wird — nicht
   erst danach, wenn Chris sich meldet.
3. Bei mehrdeutigen Treffern: Chris kurz fragen statt zu raten (Ausnahme zu "einfach machen, nicht
   fragen" — die gilt für risikolose technische Aktionen, nicht für "in welchen von zwei plausiblen
   Ordnern soll ich schreiben").

**Verwandt (WSL-Schreibproblematik, separates aber am selben Tag verschärftes Thema):** Dateien, die
per WSL/DrvFs (`/mnt/d/...`) geschrieben werden, lösen NICHT zuverlässig die Windows-Benachrichtigungen
aus, auf die Explorer UND OneDrive's Sync-Engine hören ([[reference_wsl_explorer_refresh]]). Bei
Dateien, die in einen OneDrive-synchronisierten Ordner sollen und ZEITNAH sichtbar/hochgeladen sein
müssen: nach dem WSL-Schreiben sofort mit einer nativen Windows-Operation "anfassen" (z.B.
`powershell.exe -Command "Copy-Item"` statt nur `cp` über den WSL-Mount, oder zumindest ein natives
Rename/Touch direkt danach) — nicht erst warten und hoffen, dass Explorer/OneDrive es von selbst merkt.
Ein späteres Nachbessern (Neustart OneDrive, Explorer-Neustart) hat sich hier NICHT als zuverlässig
gezeigt.
