---
name: feedback-aurora-ii-sammelmodus
description: AURORA II Lesen — Hinweise (vin/gramm/nicht witzig genug) werden pro Kapitel gesammelt und gebündelt gesendet; Duo-Reader + MP-Studio
metadata:
  type: feedback
---

Chris (23.10.2026, bei Kap. 15): Er kommt mit dem Lesen nicht hinterher und liest vor allem am **Duo** (`/aurora` = `aurora-reader.html`). Sofort-Fragen pro Satz bremsen ihn. Lösung: **Sammelmodus** — Satz markieren, Kürzel antippen (vin / gramm / nicht witzig genug, optional Freitext), „📝 Merken"; nach dem Kapitel gebündelt „📤 senden". Bolla-Vorfilter-Idee hat er verworfen (sein Lesen bleibt die Instanz).

**Technik:** Daten `workspace/data/aurora2_sammel.json` (getrennt von aurora2.json, kein Schreib-Race). Endpunkte in `mission_control_api.py`: GET `/api/aurora2/sammel`, POST `sammel-merken` / `sammel-loeschen` / `sammel-senden`. Senden = Worker-Thread, der die Hinweise in Textreihenfolge nacheinander durch die bestehende `/api/aurora2/satz-frage`-Pipeline schickt (Opus, ~30 s je Hinweis); Kürzel werden serverseitig zu vollen Anweisungen ausgeschrieben (`_a2_frage_expand`, „nicht witzig genug" = pointierter, trocken, kein Slapstick, Niveau Kap. 10). Danach „Auswertung" (Antwort + Vorschlag, Übernehmen/Verwerfen je Hinweis, „Fertig" blendet aus). Reader: gemerkte Sätze orange gepunktet, antippbar zum Bearbeiten/Löschen, Kopfzeilen-Button 📤 N / ⏳ / 📋. MP-Studio: Chips + Merken im Satz-Panel, Box „gesammelte Hinweise" + Auswertung (keine Markierung im Fließtext). „Sofort fragen" bleibt als Zweitweg.

**Why:** Lesetempo; Chris will nur lesen und markieren, nicht nach jedem Satz warten.
**How to apply:** Neue Kürzel in `_a2_frage_expand` + Chips (Reader `#chips`, MP `.a2sm-chip`) ergänzen. Bei Änderungen am Reader: Backups `workspace/backups/*vor_sammelmodus_20261023*`. Server-Neustart nötig bei Python-Änderungen (setsid nohup scripts/start_mc_server.sh). Am Duo von Chris getestet: funktioniert top (23.10.2026). Siehe [[project_aurora_ii]], [[feedback_aurora_ii_verstehe_ich_nicht]], [[feedback_blaue_markierung_vorschlaege]].
