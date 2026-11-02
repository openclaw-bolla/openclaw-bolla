---
name: Code aus Terminal kopieren
description: Chris kann Code nicht aus dem Terminal kopieren — immer clip.exe nutzen
type: feedback
originSessionId: dfa8875a-0ac2-4b8c-bbe7-b04d2c559b7d
modified: 2026-08-14T18:25:33.357Z
---
Chris arbeitet im Terminal und kann Code nicht einfach aus der Ausgabe kopieren.

**Why:** Terminal-Selektion ist in WSL/Claude Code unpraktisch, besonders bei längeren Code-Blöcken.

**How to apply:** Wenn Chris Code braucht um ihn irgendwo einzufügen (Browser-Konsole, Notepad, etc.) → immer direkt mit `clip.exe` in die Windows-Zwischenablage kopieren, dann kann er einfach Strg+V nutzen.

⚠️ **PFLICHT — voller Pfad, SOFORT beim ersten Mal:** `clip.exe` ist NICHT im PATH des Bash-Tools → `clip.exe` allein gibt **immer** „command not found". Direkt den vollen Pfad nutzen: **`/mnt/c/Windows/System32/clip.exe`**. (Chris hat 24.06.2026 explizit angemerkt, dass ich das jedes Mal am Anfang falsch mache — nie wieder erst `clip.exe` probieren.)

**Standard-Snippet (mit UTF-16LE wegen Umlaute/Apostrophe, siehe [[feedback_clip_utf16]]):**
```
iconv -f UTF-8 -t UTF-16LE datei.txt | /mnt/c/Windows/System32/clip.exe
```

**⚠️ Chris' Kurzwort "zw" = Zwischenablage (Lehre 13.08.2026):** Wenn Chris im Chat einfach nur "zw" schreibt (auch mitten im Satz, z.B. "gut in zw bei X gibt es Y"), meint er die Windows-Zwischenablage — er will, dass der gerade besprochene Text/Code dorthin kopiert wird. NICHT als "Zwischenzeit" o.ä. missverstehen (genau das ist mir am 13.08. passiert). Bei "zw" im Chat sofort das Snippet oben anwenden.

**⚠️ Proaktiv bei langen Befehlen, die Chris selbst ausführen muss (Lehre 14.08.2026):** Wenn ich Chris bitte, einen (insbesondere längeren) Shell-Befehl selbst mit `!`-Präfix einzutippen (z.B. `sudo`-Befehle, bei denen ich kein Passwort eingeben kann), IMMER SOFORT und ungefragt den Befehl per `clip.exe` in die Zwischenablage legen — nicht erst warten, bis Chris "zw" sagt. Chris hat den Befehl beim ersten Mal per Hand zurückgeschickt statt ihn auszuführen, weil er nicht gleich in der Zwischenablage lag. Gilt für JEDEN Befehl, den Chris manuell ausführen soll, nicht nur auf Nachfrage.
