---
name: feedback-claude-p-massenlaeufe-kosten
description: Skripte mit vielen `claude -p`-Aufrufen (Foto-Rebuild-Vision) fressen das 5h-Limit - NICHT Kosten nennen, sondern vorschlagen es nachts zu machen (Chris entscheidet); cachen + Haiku
metadata:
  type: feedback
---

**Vorfall 21.09.2026:** Foto-Rebuild `build_f_photos.py` (Vision-Ortserkennung) startete pro Foto ein eigenes `claude -p` (84 Aufrufe/Lauf, 2 Läufe an dem Tag).
Jeder Aufruf lädt den kompletten Claude-Code-Prefix (~94K Kontext, davon ~39K „frisch"/nicht gecacht) → im 5h-Fenster ab 11:10 machten diese Aufrufe **96 % der
frischen Tokens** aus (3,25 Mio), meine eigene Terminal-Session nur 3 %. Ergebnis: 93 % 5h-Limit nach ~1 h. Nutzen war mager: 69 von 84 Vision-Aufrufen = „unknown".
Chris fragte selbst „welche Jobs sind die Fresser" → Muster, nicht Zufall.

**Why:** Chris braucht das 5h-Fenster tagsüber/in der Schule selbst; ich habe den Rebuild mittags gestartet, trotz 5h-Reserve-Warnung. Sein Wunsch: schwere Läufe in seine inaktive Zeit legen. Verwandt: [[feedback_limit_regeln]].

**How to apply (Chris' Praezisierung 21.09.2026 - ersetzt "Kosten nennen/Freigabe holen"):** Chris will **keine Kosten-Info**, sondern den **Hinweis, dass wir so
etwas besser nachts machen sollten (wenn er nichts tut)** - kurz vorschlagen ("laeuft besser nachts, z. B. ab 00:15"), **die Entscheidung liegt bei ihm** (er kann auch "jetzt" sagen).
Gilt fuer Skripte mit vielen `claude -p`-Aufrufen (>~10) und andere schwere Hintergrundlaeufe. Nachts-Ausfuehrung: Cron/`at` planen ([[feedback_wartungsfenster_surfaces]]: 0:15-7:00).
Technisch zusaetzlich sparen: (1) Vision-Ergebnisse pro Datei cachen (`scripts/f_vision_cache.json`), (2) Haiku statt Sonnet, (3) mehrere Fotos pro Aufruf buendeln.
Opus nur im Aurora-II-Korrekturweg (MP-Chat, 1 Aufruf/Satz, Projektordner `-home-bolla`), nie fuer Bulk.
