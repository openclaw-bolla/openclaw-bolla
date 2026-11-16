---
name: Windows Desktop-Pfad
description: Chris' Desktop = /mnt/d/OneDrive/Desktop/ (D:\OneDrive\Desktop\) — einzige Quelle, per Hook erzwungen
type: user
---
Chris' Desktop liegt auf **D:** (OneDrive): WSL `/mnt/d/OneDrive/Desktop/`, Windows `D:\OneDrive\Desktop\`.

Der Desktop unter `C:\Users\ernst\...` ist leer/falsch. Seit 03.11.2026 blockiert der PreToolUse-Hook `~/.claude/hooks/desktop_path_guard.py` (in settings.json) jeden Bash/Write/Edit/Read-Aufruf mit einem C:-Desktop-Pfad (exit 2 + Hinweis). Ursache der Fehler vorher: reine Textregel, mehrfach (3×) gespeichert, trotzdem geraten.
**Why:** Chris war mehrfach verärgert (3. Verstoß 02.11., 4. am 03.11.). **How to apply:** Direkt `/mnt/d/OneDrive/Desktop/` schreiben, nie raten/globben.
- Chris' „temp“ = Ordner **D:\OneDrive\Desktop\temp** (/mnt/d/OneDrive/Desktop/temp/), NICHT C:\temp (Verwechslung 15.11.2026: Z-Flip-Datei dort abgelegt).
