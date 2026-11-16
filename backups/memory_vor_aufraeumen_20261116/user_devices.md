---
name: Chris' Hardware
description: Surface Laptop Studio (Haupt-PC, WSL2), Surface Book 1, Surface Pro (Reni), Surface Duo 2, Huawei P20 — nur News zu diesen Geräten
type: user
originSessionId: fb08c238-bdfe-4c80-ad9f-bbb99e7c8b12
modified: 2026-09-28T14:17:24.265Z
---
## Computer
- **Surface Laptop Studio** (Chris sagt: "Studio") — Haupt-Arbeitsgerät, hier läuft Bolla. WSL2, Hostname `ChrisSurfaceLS`, Intel Core i7-13700H (13. Gen). IP: 192.168.178.29
- **Surface Book** (Chris sagt: "Book") — Schulgerät (Studio ist zu wertvoll, Book soll noch mind. 1 weiteres Schuljahr halten). Surface Book 1. Gen, Intel Core i7-6600U @ 2,60 GHz, 8 GB RAM, Windows 11 Pro. IP zuhause: 192.168.178.38. Reverse-SSH-Tunnel eingerichtet (Port 2222)
  - **Tablet-Akku (Akku 1) defekt** — dauerhaft 0%, Tausch zu teuer/nicht geplant
  - **Problem:** Wenn komplett ausgeschaltet, dauert Einschalten 30+ Sek (wartet auf Mindestladung im Tablet-Akku)
  - **Lösung:** Nie herunterfahren — Windows-Einstellung "Deckel schließen" auf **Standby** (nicht Ruhezustand!). Ruhezustand/Hibernate löst intern dennoch einen Firmware-Check auf Tablet-Akku aus → selbes Problem wie Kaltstart. Hybrid Sleep auf dem Book nicht verfügbar (Surface sperrt das). Standby bei 95% Keyboard-Akku überlebt jeden Schulweg problemlos. Falls doch mal aus: 2-3 Min am Strom warten vor Einschalten.
- **Surface Pro** (Chris sagt: "Pro") — Renis Gerät (Renate Mandel). IP: 192.168.178.41, Windows-User: `renat`. Reverse-SSH-Tunnel Port 2223 eingerichtet, analog Surface Book. Zwei Benutzer (`ernst`+`renat`), beide Admins — SSH-Befehle laufen als `ernst`, GUI-Aktionen erscheinen aber in Renates Session. Verknüpfungen für beide sichtbar ablegen: `C:\Users\Public\Desktop\` (nicht den privaten Desktop-Ordner)

## Handys
- **Surface Duo 2** — Haupthandy, "bestes Handy ever". WLAN-Debugging (ADB) aktiviert
- **Huawei P20** — ⚠️ **außer Betrieb** (Chris-Bestätigung 28.09.2026), abgelöst durch das Pixel 8 (s. u.). Android 9, kein WLAN-ADB (erst ab Android 11), nur USB-ADB möglich. Nicht mehr als aktives Handy behandeln/vorschlagen.
- **Google Pixel 8** (refurb „Wie neu", Akku ≥80 %, 269 €), Codename `shiba` — angekommen + Ersteinrichtung am 23.09.2026 (Google-Konten, SIM, Apps vom Duo kopiert, Edge als Standardbrowser). **Aktives Handy, hat das Huawei P20 abgelöst** (28.09.2026 von Chris bestätigt). WLAN-Debugging (ADB) seit 23.09.2026 eingerichtet, analog Duo/Z Flip (IP/Port dynamisch, nach Reboot/WLAN-Wechsel neu koppeln über Entwickleroptionen → Kabelloses Debugging). Chat-Alias „p8". Noch offen: Akku-Check-Bestätigung, restliche Wallet-Karten, IONOS-Authenticator, Banking-Apps, MP-Verbindungsfeld. Details: [[project_pixel8_p20_ersatz]]
- **Samsung Galaxy Z Flip 3 (SM-F711B), Renis Handy** — Android 15, WLAN-Debugging (ADB) aktiviert seit 10.07.2026, analog zum Duo. IP zum Zeitpunkt der Einrichtung `192.168.178.57` (dynamisch, Port ändert sich — nach Reboot/WLAN-Wechsel neu koppeln/verbinden über Entwickleroptionen → Kabelloses Debugging).

ADB-Zugriff eingerichtet seit 2026-04-15 (Duo), 10.07.2026 (Z Flip).

## Hinweis
- **News-Filter:** Nur Surface/Microsoft-News für tatsächlich besessene Geräte bringen: Laptop Studio, Book 1, Pro, Duo 2. Kein Surface Book 2/3, kein Surface Go, kein Surface Neo, etc.
- **Großer Microsoft-Fan** — bevorzugt Microsoft-Produkte und -Ökosystem
