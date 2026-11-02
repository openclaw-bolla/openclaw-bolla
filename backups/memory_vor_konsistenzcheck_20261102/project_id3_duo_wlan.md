---
name: project-id3-duo-wlan
description: "Offen — ID.3/Duo WLAN-Konflikt (My VW6351 vs. P20-Hotspot), nächster Schritt: App-Connect-Einstellung im ID.3 selbst prüfen"
metadata: 
  node_type: memory
  type: project
  originSessionId: ddc28e86-5ad8-4f8d-ab00-1ad3fbeaf08e
  modified: 2026-08-21T08:07:50.827Z
---

Chris' Duo (Surface Duo, keine SIM) nutzt im Auto den P20-Mobile-Hotspot für Internet, aber das automatisch verbindende Auto-WLAN "My VW 6351" (nötig für kabelloses Android Auto) wirft die Hotspot-Verbindung sofort wieder raus, sobald das Duo in Reichweite des ID.3 ist.

**Warum (per ADB direkt am Duo verifiziert, 21.08.2026 vormittags, Duo war per ADB erreichbar unter 192.168.178.20):**
- "My VW 6351" ist NICHT einfach ein gespeichertes Netzwerk mit Auto-Connect-Schalter — es erscheint gar nicht in `cmd wifi list-networks`. Stattdessen legt die Android-Auto-App (`com.google.android.projection.gearhead`, uid 10118) die Netzwerk-Config bei jeder Verbindung per `WifiNetworkFactory`-Specific-Request dynamisch an (`addOrUpdateNetworkInternal`) und löscht sie danach wieder (`removeNetworkInternal`) — bestätigt an 3 Zyklen allein am 21.08. vormittags (07:29, 08:45×2). Verbindung läuft dabei immer als `ROLE_CLIENT_PRIMARY`, verdrängt also zwangsläufig die primäre P20-Hotspot-Verbindung.
- Chip-Fähigkeit geprüft: `dumpsys wifi` zeigt "STA + STA Concurrency Supported: true" — Hardware könnte also gleichzeitige WLAN-Verbindungen. Aber: Duo läuft auf Android 12 (SDK 32), das Android-Feature "Multi Internet Connectivity" (das STA+STA für zwei gleichzeitige Internet-Verbindungen nutzbar macht) gibt's erst ab Android 14 — auf dem Duo technisch nicht verfügbar. Damit sind beide ursprünglich angedachten Lösungswege (Auto-Connect abschalten / Dual-WLAN nutzen) dicht.
- "My VW 6351" ist zusätzlich als Bluetooth-Gerät fest gebondet (`Bonded devices` in `dumpsys bluetooth_manager`) — die WLAN-Verbindung wird vermutlich über diese Bluetooth-Kopplung getriggert (Auto erkennt Duo per BT, schickt WLAN-Zugangsdaten), **unabhängig davon ob ein USB-Kabel steckt**. Kabel-Anschluss allein löst das Problem also aller Wahrscheinlichkeit nach NICHT.
- Chris hat auf dem Duo in der Android-Auto-App unter "Verbundene Autos" nachgesehen: dort steht **kein Auto**, nur ein "+" zum Hinzufügen. Die App verwaltet also gar kein dauerhaftes Fahrzeugprofil — die Steuerung für kabellos/kabelgebunden liegt daher vermutlich nicht im Duo, sondern im ID.3-Infotainment selbst (App-Connect-Geräteverwaltung).

Zusatzkontext aus derselben Diagnose-Session (21.08.2026): ID.3 zeigte bei P20 nur unzuverlässige Audio-Wiedergabe (aktives Mediengerät war Duo, nicht P20 — Umschalten über Telefon-Bildschirm/Pfeil-Symbol), und Android Auto lief nur mit Duo, obwohl auch auf P20 installiert (P20 war nie als AA-Gerät im Auto registriert, nur normal per Bluetooth gekoppelt).

**Wie anwenden — nächster Schritt (nicht mehr am Duo, sondern im Auto):** Bei nächster Fahrt gemeinsam im ID.3-Infotainment unter Einstellungen → "App-Connect" bzw. "Telefon" nachsehen, ob es dort pro gekoppeltem Gerät einen Schalter für kabellose Verbindung gibt, den man fürs Duo deaktivieren kann (würde erzwingen, dass AA nur per Kabel läuft und WLAN frei für den P20-Hotspot bleibt). Genaue Menüführung im VW-Menü noch nicht verifiziert — ungeprüfte Vermutung, vor Ort schauen. Alternative falls das nicht klappt: mit der kurzen WLAN-Lücke während aktiver kabelloser AA-Nutzung leben (Duo braucht dann eh kein Internet, da kein Streaming während AA-Session nötig ist).
