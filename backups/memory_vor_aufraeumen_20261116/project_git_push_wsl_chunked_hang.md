---
name: project-git-push-wsl-chunked-hang
description: "GELÖST 13.09.2026: git push hing wochenlang — Ursache war kein Netzwerkbug, sondern 1,8GB versehentlich committete tar-Backups"
metadata: 
  node_type: memory
  type: project
  originSessionId: 18d987b6-66af-4bd0-a349-8cd6d4d89474
  modified: 2026-09-13T18:10:00.000Z
---

## ✅ GELÖST (13.09.2026) — es war nie ein Netzwerkproblem

Nach Wochen Fehlersuche und diversen Windows/WSL-Netzwerk-Fixes (Checksum-Offload, LSO, RSC,
TSO/GSO/GRO — alle unten dokumentierten Maßnahmen durchgeführt, alle ergebnislos) die tatsächliche
Ursache gefunden: Die automatische Nachtsicherung hatte am 09.09.2026 trotz vorhandener
`.gitignore`-Regel zwei riesige Backup-tar-Dateien (zusammen ~1,8GB, Tansania-Reise-Fotos/WhatsApp)
mit in einen Commit gezogen. Jeder Push seitdem versuchte, diese 1,8GB hochzuladen — sah bei
15-30s-Testtimeouts wie ein Hänger aus, war aber schlicht eine sehr lange Übertragung. Fix: Rebase
auf den betroffenen (noch ungepushten) Commit, Dateien per `git rm --cached` entfernt (bleiben auf
der Platte), `nacht_backup.sh` gehärtet (Pathspec-Ausschluss für `backups/*.tar` + generisches
20MB-Sicherheitsnetz vor jedem Commit). Push danach: 9KB, 4 Sekunden. Alle Netzwerk-Einstellungen
unten wieder auf Windows-Standard zurückgesetzt, da nachweislich nicht die Ursache.

**Lehre:** Vor jeder Netzwerk-Ferndiagnose bei "git push hängt" ZUERST prüfen, wie groß der
tatsächliche Payload ist: `git rev-list origin/master..HEAD --objects | git cat-file --batch-check='%(objecttype) %(objectsize) %(rest)' | sort -k2 -n -r | head` —
zeigt sofort, ob ein Riesen-Blob im Spiel ist. Hätte die komplette folgende Odyssee erspart.
Details der (nutzlosen) Netzwerk-Fehlersuche unten als Referenz, falls doch mal ein echter
Netzwerkbug auftritt.

---

## Historie der (letztlich falschen) Netzwerk-Fehlersuche

Am 10.09.2026 hing `git push origin master` im workspace-Repo (github.com/openclaw-bolla/openclaw-bolla) drei Versuche in Folge mit `HTTP 408` / "unexpected disconnect while reading sideband packet". `curl` zu github.com/api.github.com war sofort erreichbar (200, <200ms), `git ls-remote origin` (reiner GET) auch sofort ok. Mit `GIT_CURL_VERBOSE=1` sichtbar: Die ersten beiden GET-Requests (`info/refs`) laufen sauber und schnell durch, aber der dritte Request — der eigentliche `POST .../git-receive-pack` mit `Transfer-Encoding: chunked` — hängt nach dem Senden der Header komplett, keine Server-Antwort, bis Timeout.

**Versuchte Fixes ohne Erfolg:** `git config http.postBuffer 524288000` (500MB) und `http.version HTTP/1.1` gesetzt — Push nutzt danach immer noch chunked Transfer-Encoding und hängt weiterhin. Repo ist klein (~1,8MB gepackt), also kein Größenproblem.

**Verdacht:** Bekanntes WSL2-Netzwerk-Problem mit chunked/großen Uploads über die virtuelle NIC (TCP-Segmentation-Offload-Bug) — Fix wäre vermutlich auf Windows-Seite (`Set-NetAdapterChecksumOffload` o.ä. auf dem vEthernet(WSL)-Adapter, braucht Admin-PowerShell), nicht von innen aus WSL lösbar. NICHT selbst versucht, da Eingriff in Windows-Netzwerkadapter-Einstellungen außerhalb sicherem autonomem Rahmen liegt.

**Status:** Lokaler Commit (Tagesnotiz 10.09.) bleibt unshoved auf dem Rechner, geht nicht verloren. Nächster automatischer nächtlicher Sicherungslauf (siehe "Automatische Nachtsicherung"-Commits in der Historie) könnte es klappen, falls das Netzwerkproblem nur vorübergehend war — falls es beim nächsten Mal wieder auftritt, ist es kein Zufall mehr, sondern strukturell, und dann mit Chris die Windows-NIC-Einstellung angehen.

**🔁 Bestätigt strukturell (13.09.2026):** Erneut aufgetreten am 12. UND 13.09., mehrere Versuche über zwei Tage. Sogar der **automatische nächtliche Cron-Sicherungslauf** ("Automatische Nachtsicherung 2026-09-13"-Commit existiert lokal) konnte nicht pushen — lokales `master` liegt 17 Commits vor `origin/master`. Damit klar kein Zufall mehr. Nächster Schritt laut obigem Plan: mit Chris die Windows-NIC-Einstellung angehen. Verdächtiger Befehl (Admin-PowerShell auf Windows-Host, NICHT von Bolla selbstständig ausführen):
```
Get-NetAdapter | Where-Object {$_.InterfaceDescription -like "*WSL*"} | Disable-NetAdapterChecksumOffload
```
Sicherer zum Diagnostizieren zuerst: `Get-NetAdapterChecksumOffload -Name "vEthernet (WSL)"` — dann gezielt einzelne Optionen (`-TcpIPv4`, `-UdpIPv4`) statt pauschal alles deaktivieren. Bis dahin: alle Commits bleiben lokal sicher, Push manuell nachholen wenn's zufällig klappt (Netzzustand scheint zu schwanken, nicht dauerhaft komplett tot).

**Update 13.09.2026 abends — Offload-Fix durchgeführt, aber (noch) ohne Erfolg:** Erster Versuch filterte auf `InterfaceDescription -like "*WSL*"` — traf nichts, weil der echte Adapter `vEthernet (WSL (Hyper-V firewall))` als Description nur "Hyper-V Virtual Ethernet Adapter" trägt (kein "WSL" drin). Korrigiert auf `Get-NetAdapter -Name "*WSL*" | Disable-NetAdapterChecksumOffload -Confirm:$false` — hat funktioniert, `Get-NetAdapterChecksumOffload` zeigt danach alle Felder (IpIPv4/TcpIPv4/TcpIPv6/UdpIPv4/UdpIPv6) auf "Disabled". **`git push` hing trotzdem weiter** (Timeout, exit 124) — direkt danach getestet, OHNE WSL-Neustart dazwischen. Vermutung: WSL baut seine virtuelle NIC beim Hochfahren auf, eine Host-seitige Adapter-Änderung greift bei einer bereits laufenden WSL-Instanz oft erst nach `wsl --shutdown` + Neustart. **Wichtig: `wsl --shutdown` NIE von Bolla selbst anstoßen** — würde die eigene laufende Session sofort beenden (Bolla läuft in WSL). Chris hatte ohnehin einen Windows-Update-Neustart vor — Push-Test verschoben auf die nächste Session NACH diesem Neustart. Falls es dann immer noch hängt: war wohl doch nicht (nur) die Checksum-Offload-Theorie, dann andere Ursachen prüfen (MTU, Antivirus/Firewall-Deep-Packet-Inspection auf große chunked POSTs, IPv6-Routing).
