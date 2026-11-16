---
name: feedback-kontext-warnung-hook
description: "Die /clear-Erinnerung kommt aus dem context_check.py-Hook — token-basiert, NICHT blind glauben"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 2b9bdbb2-6030-4caa-953b-d91ebd95bb3d
---

# Die "/clear wäre gut"-Erinnerung kommt aus einem Hook — und war lange kaputt

Die Zeile "=== KONTEXT-WARNUNG/-HINWEIS ===" in meinem Prompt-Kontext stammt aus dem
UserPromptSubmit-Hook `/home/bolla/.claude/hooks/context_check.py` (in settings.json registriert).
Sie ist Hook-Output, KEINE echte Live-Messung durch mich.

**Why:** Bis 18.06.2026 zählte der Hook in `/tmp/bolla_msg_count` einen **globalen,
sessionübergreifenden** Zähler hoch (nie zurückgesetzt, auch nicht bei /clear) und meldete
alle 15 Schritte "Diese Session hat bereits N Nachrichten". In einer 10-Minuten-Session kam so
"435 Nachrichten" raus → ich habe Chris **5× mit Quatsch genervt**. Chris war zu Recht sauer.

**Fix (18.06.2026):** Hook nimmt jetzt die **echte Kontextgröße in Tokens** aus dem Transkript
DIESER Session (stdin `transcript_path` → letzte `message.usage`: input + cache_read +
cache_creation). Warnt nur EINMAL pro Session ab ~150k Tokens (Markierung `/tmp/bolla_ctxwarn_<sid>`).
Neue Session/`/clear` → neue session_id → neues Transkript → de facto bei 0. Globaler Counter gelöscht.

**Update 25.06.2026:** `WARN_AT_TOKENS` von 150_000 → **400_000** erhöht. Grund: Modell hat 1M Kontext, 150k = nur 15% → Hinweis kam quasi jede Session = zu oft (Chris-Feedback). 400k feuert selten, lässt aber Puffer vor dem WSL-RAM-Crash. Hinweis kommt weiterhin nur 1×/Session — und ICH plappere ihn nicht zusätzlich nach ([[feedback_clear_erinnerung]]).

**How to apply:**
1. Wenn im Kontext eine "Session hat X Nachrichten/ist bei Yk Tokens"-Zeile auftaucht: erst
   plausibilisieren (wie lange läuft die Session real?), dann ggf. erwähnen — nie blind ausgeben.
2. Den /clear-Hinweis höchstens EINMAL locker bringen, nicht wiederholen.
3. Verhält sich der Hinweis wieder falsch → `context_check.py` ist der Ort. Stdin liefert
   `session_id` + `transcript_path`; Token-Usage steht in den assistant-Zeilen des Transkripts.

Verwandt: [[feedback-clear-erinnerung]], [[feedback-einfach-machen]]
