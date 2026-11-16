---
name: project_reni_handy_watch_sync
description: "Reni's Galaxy Watch 7 synct nicht zuverlässig mit ihrem Handy"
metadata: 
  node_type: memory
  type: user
  originSessionId: f88c698b-ab8b-4202-88d3-d86478ae6180
  modified: 2026-07-31T20:47:17.182Z
---

Reni hat eine **Galaxy Watch 7**. Google-Account auf Handy + Watch: **renat.mandel13@gmail.com**.

## Vorfall 31.07.2026: Bluetooth-Kopplung komplett weg
Schritte/Schlaf wurden nicht mehr angezeigt. Ursache war NICHT nur Hintergrund-Sync, sondern die
**Bluetooth-Kopplung selbst war weg** — die Watch tauchte in der Galaxy Wearable App gar nicht mehr auf
(nur die Buds waren dort gelistet). Bestätigt über Handy-Einstellungen → Verbindungen → Bluetooth: Watch
fehlte auch dort komplett aus der Geräteliste.

**Fix:** Über Bluetooth-Einstellungen (nicht über die Wearable-App) neu koppeln — "Neues Gerät koppeln",
Watch muss dabei eingeschaltet/in Reichweite sein, Android leitet dann automatisch zur Wearable-App für
den letzten Schritt weiter. Hat funktioniert, Daten (Schritte/Schlaf-Historie) waren nicht verloren, da
diese am Google-Konto hängen, nicht an der lokalen Bluetooth-Kopplung.

**Mögliche Ursachen für eine komplett verschwundene Kopplung** (nicht nur "getrennt", sondern der Bond
selbst weg) — konnte nicht abschließend verifiziert werden, da keine Logs verfügbar waren, aber das sind
die wahrscheinlichsten Kandidaten:
- Ein Software-Update auf Handy oder Watch (setzt den Bluetooth-Stack manchmal zurück)
- Ein "Speicher/Cache leeren" für Bluetooth-Systemkomponenten, z.B. durch eine Akku-/Speicher-Optimierer-App
  (Samsung Device Care "erweiterte Bereinigung" kann sowas mit erledigen)
- Versehentliches "Kopplung aufheben" beim Antippen in den Einstellungen
- Sehr seltener Fall: Bond-Speicher-Limit, falls viele andere Bluetooth-Geräte gekoppelt wurden

**Zur Stabilisierung/Vorbeugung (Empfehlung, keine Garantie):**
- Watch und Handy auf aktuellem Software-Stand halten (Updates zeitnah installieren, nicht ewig aufschieben)
- Bei "Speicher bereinigen"/Cleaner-Apps vorsichtig sein, keine System-Cache-Bereinigung für Bluetooth/
  Connectivity-Komponenten laufen lassen
- Watch nicht zwischendurch an ein anderes Handy/Tablet koppeln (verdrängt ggf. die bestehende Kopplung)
- Falls es wieder passiert: gleiche Anleitung wie oben (Bluetooth-Einstellungen → neu koppeln), Daten bleiben
  erhalten.
