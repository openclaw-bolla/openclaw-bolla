---
name: ""
metadata: 
  node_type: memory
  originSessionId: 1e001c27-2d2c-401b-a148-b79bae6b2bf7
---

Bei Handy-Speicher-Aufräumaktionen (Duo, Z Flip, jedes ADB-verbundene Android-Gerät): `adb shell pm trim-caches <ziel>` räumt System-App-Caches (auch die internen, nicht über /storage/emulated sichtbaren) — 100% sicher, keine Logins/Daten verloren, da Caches per Definition jederzeit regenerierbar sind.

**Why:** Erster Versuch mit `pm trim-caches 4G` brachte NICHTS, weil bereits mehr als 4G frei war — der Parameter ist keine "räum X GB weg"-Anweisung, sondern "sorg dafür dass MINDESTENS X GB frei sind". Erst mit einem Zielwert deutlich ÜBER dem aktuellen freien Speicher (z.B. `pm trim-caches 25G` bei 6,5G frei) trimmt das System wirklich — brachte bei Renis Z Flip 3 sofort 2,2 GB.

**How to apply:** Immer ZUERST `df -h /storage/emulated/0` für den Ist-Stand, dann `pm trim-caches` mit einem Zielwert deutlich darüber (z.B. Gesamtgröße der Partition oder Ist-Stand + 20G) aufrufen, danach nochmal `df -h` zum Vergleich. Kann mehrfach mit steigendem Zielwert wiederholt werden, bis sich nichts mehr ändert (= Cache-Untergrenze erreicht). Ergänzt die exakte Datei-Duplikat-Suche (Hash-Vergleich) als zweiten Cleanup-Hebel — beides zusammen ist der volle "Handy aufräumen"-Workflow.

**Dritter Hebel fürs Duo 2, bei Bedarf (Chris-Wunsch 14.07.2026):** Beim Sicherheits-Check des Duo (siehe [[user_duo2]]) aufgefallen — 156 installierte Drittanbieter-Apps (alle sauber aus dem Play Store, `pm list packages -3`). Falls Chris nochmal Speicherprobleme auf dem Duo hat: die App-Liste mit ihm durchgehen und ungenutzte Apps zum Deinstallieren vorschlagen (mehr Speicher + kleinere Angriffsfläche, da OS-Support seit Okt. 2024 ausgelaufen). War 14.07. explizit noch nicht gewünscht ("aktuell nicht") — erst bei nächstem Speicherproblem von selbst ansprechen, nicht vorher.
