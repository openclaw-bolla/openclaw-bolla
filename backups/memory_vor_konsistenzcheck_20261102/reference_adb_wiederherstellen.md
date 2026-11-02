---
name: reference-adb-wiederherstellen
description: ADB zu Duo/Pixel 8/Z Flip nach Reboot wieder herstellen (Port 5555 weg, mDNS in WSL2 geht nicht) — Ablauf mit Portscan + Kopplungscode
metadata:
  type: reference
---

Feste Verbindung = `adb connect <IP>:5555` (nach `adb tcpip 5555`). Der Listener stirbt bei Reboot/WLAN-Wechsel → "Connection refused". `adb mdns services` ist in WSL2 (NAT) leer, Auto-Discovery geht NICHT.

**Wiederherstellung (Duo 01.11.2026 bestätigt):**
1. Chris am Handy: Entwickleroptionen → **„Debugging über WLAN"** (Duo-Name für Kabelloses Debugging, unter „USB-Debugging-Autorisierungen widerrufen") → Text antippen → „Gerät mit Kopplungscode koppeln" → Code nennen, Dialog offen lassen.
2. Portscan 30000–50000 auf die Handy-IP (Python-Socket, 400 Threads, ~30 s); mit Code `adb pair IP:port` auf jeden offenen Port probieren — der Kopplungs-Port nimmt den Code an.
3. Der andere offene Port = Connect-Port: `adb connect IP:port`, dann `adb -s IP:port tcpip 5555`, `adb connect IP:5555`.
Wenn Connect-Port nur `offline` zeigt = Schlüssel nicht gekoppelt → Schritt 1–3.
IPs: Duo 192.168.178.20, Z Flip 192.168.178.57; Pixel 8 192.168.178.36 (Stand 01.11.2026, ebenfalls wieder auf :5555; Pixel-Pairing-Dialog wechselt Port/Code bei jedem Öffnen → Portscan wiederholen, je Scan neue Ports). Siehe [[user_devices]].
