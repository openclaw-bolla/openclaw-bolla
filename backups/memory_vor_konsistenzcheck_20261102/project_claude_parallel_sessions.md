---
name: Parallele Claude-Instanzen — Hänger-Ursache
description: Telegram-Bot startet claude -p als Subprocess, kollidiert mit interaktiver Session
type: project
originSessionId: 9e265b90-8a7b-4aa0-beb8-e3662b86254a
---
Wenn der Telegram-Bot gleichzeitig mit einer interaktiven Claude-Session läuft, greifen beide auf dieselben `~/.claude/` State-Dateien zu → interaktive Session hängt, danach ist `claude` im PATH nicht mehr gefunden.

**Why:** Passiert am 03.05.2026 — Chris arbeitete interaktiv, schickte vom Sofa Telegram-Aufträge.

**How to apply:** Bot (`~/workspace/scripts/telegram_bot.py`) prüft jetzt via `interactive_claude_running()` ob eine interaktive Session läuft und lehnt ab. Wenn Hänger berichtet wird, zuerst fragen ob Telegram-Aufträge gleichzeitig liefen.

## Variante 2: MP-Bolla-Chat zäh während Workflow in Terminal-Session (17.06.2026)
Wenn in der **interaktiven Terminal-Session** ein **Workflow mit vielen Agenten** läuft (Chris hatte 119 Agenten / 25 fertig), wird der **MP-Bolla-Chat in der eigenen UI schubweise träge** — „mal hängt's, mal läuft's".

**Ursache — zwei Ebenen, beide wichtig:**
1. **Rate-Sharing:** Beide Claude-Instanzen (Terminal-Session + der pro MP-Nachricht frisch gestartete `claude -p --resume`) nutzen denselben Anthropic-Account. Die vielen Agenten fluten die **Requests-pro-Minute-Rate** (nicht das Quota-Volumen — das kann bei 31 % stehen!), MP-Chat-Requests werden mit 429/Retry gedrosselt → Trägheit. Lokal ist nichts überlastet (Load < 0,3, RAM frei).
2. **Workflow-Agenten sind KEINE OS-Prozesse.** Sie laufen als interne async-Tasks INNERHALB des einen Node-Claude-Prozesses (z.B. 13 Threads, ~4 HTTPS-Verbindungen, Concurrency-Cap ~10-16 gleichzeitig). Darum findet `ps | grep agent/workflow` NICHTS — auf Prozessebene gibt es sie nicht. In `ps` sieht man nur „ein langlaufender claude mit ~15 % CPU".

**Why:** Ich (Bolla im MP-Chat) bin ein komplett separater Prozess (über `mission_control_api.py` gestartet) — kein gemeinsamer Speicher/Agent-State mit der Terminal-Session. Ich kann in deren internen Workflow-Stand NICHT reinschauen.

**How to apply:** Wenn Chris im MP-Chat zügig arbeiten/etwas zeigen will → Terminal-Session ruhen lassen (keinen großen Workflow parallel laufen lassen). Läuft schon ein gewollter Workflow: NICHT eingreifen/killen (fertige Agenten-Ergebnisse gingen verloren) — einfach abwarten, MP-Chat wird wieder flüssig sobald der Workflow durch ist.
