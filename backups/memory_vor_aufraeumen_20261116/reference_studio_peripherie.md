---
name: reference-studio-peripherie
description: Surface Studio Peripherie-Verkabelung — Sonnet Echo 11 TB4-Dock vs. direkt am Studio; DVB-T-Stick-Problem
metadata: 
  node_type: memory
  type: reference
  originSessionId: 369a0f35-7e58-4fc2-8453-ebcc633db2e7
  modified: 2026-08-10T13:44:11.272Z
---

# Surface Studio — Peripherie & Verkabelung

Stand 26.06.2026, von Chris bestätigt.

Topologie per System verifiziert (Get-PnpDeviceProperty Parent): **Echo 11 und ACASIS hängen BEIDE am selben USB4-Root-Router** = zwei getrennte TB-Ports direkt am Studio. **KEINE Dock-Kette/Verkettung.**

## Am Sonnet Echo 11 Thunderbolt-4-Dock (eigener TB-Port am Studio)
- **Monitor** — HDMI über USB-C
- **Ethernet** — Studio hängt fest per Kabel/LAN am Dock, **kein WLAN**. Bei Netzwerk-Fehlersuche (z.B. hängende Uploads) also nicht auf WLAN-Ursachen tippen, sondern LAN/Router/Provider-seitig denken.
- **Loses USB-C-Ladekabel** — Chris lädt darüber periodisch sein Handy (aktuell **Huawei P20 Pro**). ⚡ Zieht beim Laden über USB-PD aus dem Dock-Strombudget → **mitverdächtig fürs DVB-Enumerationsproblem**! Beim Tuner-Test das Handy abstecken.
- (früher hing hier auch der DVB-T-Stick → wird nicht mehr erkannt, siehe unten)
- KEINE Festplatte am Dock!

## Direkt am Studio (eigene Ports, bewusst NICHT über Dock)
- **WinTV DualHD DVB-T-Stick (Hauppauge)** — USB-A, läuft hier tadellos
- **ACASIS TBU405 M.2-Gehäuse → D:** = **Crucial P5 Plus 2 TB NVMe-SSD** (1863 GB), eigener TB-Port. = OneDrive-Sicherung, rsync-Backup-Ziel für `~/.claude/`. SSD wird über TB als NVMe durchgereicht (taucht nicht als USB-Disk auf). Bewusst direkt am Studio, „kein Risiko eingehen".

## C: = Disk 0, Samsung MZ9L4512 512 GB NVMe, interne Systemplatte

## DVB-T-Stick am Dock — bekanntes Problem
Der WinTV DualHD wird **am Sonnet-Dock nicht mehr erkannt** (ging früher zuverlässig).
Geräte-Manager zeigt „Unbekanntes USB-Gerät (Fehler beim Anfordern einer Gerätebeschreibung)" = `VID_0000/PID_0002` → klassisches **Device-Descriptor-Failed** (Enumeration scheitert).

**Wahrscheinlichste Ursache:** USB-Pfad/Strom am Echo 11 — der Tuner (USB-2.0-High-Speed, hoher Einschaltstrom) muss am Dock durch eine interne Hub-Ebene und scheitert beim Enumerieren. Am Dock hängt nur Monitor + Ethernet (keine Platte), also weniger Last als zunächst angenommen — Signalintegrität/Inrush am internen Dock-Hub bleibt aber plausibel.

**Durchgetestet 26.06.2026 — alles ohne Effekt:** USB Selective Suspend aus (0x0, AC+DC) · Handy abgesteckt (Strom frei) · Power-Cycle + anderer Dock-Port. Stick wird am Dock weiterhin NICHT erkannt; Error-Gerät `VID_0000/PID_0002` Instanz `5&2CDBCAF7&0&5` bleibt konstant hängen. Direkt am Studio = sofort OK.
**Sackgasse:** Es gibt für den Echo 11 **kein Windows-Firmware-Tool** (nur macOS); TB-Firmware läuft unter Windows über Windows Update / Surface-Firmware. TB-Stack ist Status OK.

**ABSCHLUSS-FAZIT:** Nicht Strom/Einstellung — der Echo 11 bekommt den USB-Datenstrom des Hauppauge („Bulk Mode") nicht sauber durch interne Hub-Ebene + TB-Tunnel. Bekanntes DVB-Tuner-an-TB-Dock-Problem, softwareseitig nicht erzwingbar. NICHT weiter dran rumdoktern.
**Dauerlösung:** Stick am Studio-USB-A lassen (läuft tadellos) = Favorit. Alternativ aktiver USB-2.0-Hub mit eigenem Netzteil zwischen Dock und Tuner (~15 €, keine Garantie).

Verwandt: [[user_devices]]
