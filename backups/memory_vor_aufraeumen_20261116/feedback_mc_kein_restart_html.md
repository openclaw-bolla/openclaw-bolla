---
name: feedback-mc-kein-restart-html
description: MC-Server liest index.html bei jedem Request frisch — für HTML/JS-Änderungen KEIN Neustart nötig
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 70868932-524e-464c-9a39-74bd35b724fb
---

# MC-Server: kein Neustart für HTML/JS-Änderungen

Der Mission-Control-Server (`mission_control_api.py`) liest `mission-control/index.html` bei **jedem HTTP-Request frisch von der Platte**. Geprüft 01.07.2026: nach einer index.html-Änderung liefert der laufende Server sofort die neue Version (`curl … | grep neue_funktion` → Treffer, ohne Neustart).

**Regel:**
- **Nur HTML/JS/CSS geändert** (index.html) → **KEIN Neustart**. Chris drückt Strg+F5, fertig.
- **Python-Code geändert** (mission_control_api.py o.ä.) → Neustart nötig (Code ist im RAM geladen).

**Warum wichtig:** Jeder Neustart hat 2-3 Sek Downtime. Fällt genau in dieses Fenster ein Frontend-Poll oder ein F5 von Chris, rendert MP leer → wirkt wie **Datenverlust** und erschreckt Chris (passiert am 01.07. → [[feedback_aktuell_md]]-Eintrag). Also Neustarts vermeiden wo möglich.

**Zusätzlich abgesichert:** `loadClipboard` + `loadProjekte` leeren die Anzeige nicht mehr bei Fetch-Fehler (behalten letzten Stand + laden nach 2,5s nach).

**Server sauber neu starten** (wenn Python-Änderung): NIE `pkill -f mission_control_api.py` (matcht die eigene Befehlszeile → killt die eigene Shell, „Exit 144"). Stattdessen PID per `ss -ltnp | grep 18790` holen und gezielt killen, dann `scripts/start_mc_server.sh` via Hintergrund-Task.
