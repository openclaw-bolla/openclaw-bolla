---
name: wartungsfenster-surfaces
description: Nächtliches Wartungsfenster 0:15–7:00 — Bolla darf/soll kritische & hardwarenahe Aktionen auf allen 3 Surfaces in diese Zeit legen
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 4bb965e7-b100-401a-9083-3690916dadb6
---

# Wartungsfenster 0:15–7:00 Uhr auf allen 3 Surfaces

**Stehende Freigabe (23.06.2026):** Bolla darf — und soll — **kritische, hardwarenahe oder störende Aktionen** auf allen drei Surface-Geräten in das Zeitfenster **0:15 bis 7:00 Uhr** verschieben:

- **Studio** (Surface Laptop Studio, Bolla-Host)
- **Book** (Surface Book, SSH :2222)
- **Pro** (Surface Pro, Renis Gerät, SSH :2223)

Dazu zählen u.a.: Windows-Updates (Download + Install + Reboot), Treiber-Updates, Neustarts, Energie-/Registry-Eingriffe, Defender-Scans, größere Wartung.

**Why:**
- Tagsüber sind die Geräte im Einsatz (Schule, Unterricht, Reni) — Chris will dort **Ruhe und keine Überraschungen** (kein Update-Reboot, keine CPU-Last).
- Speziell **Book:** Akku 1 defekt → Update-Reboot unterwegs/im Rucksack = Hitze-/Boot-Risiko ([[book-akku-defekt]], [[project_surface_book]]).
- Chris will **selbst die Kontrolle** wann etwas passiert; nachts stört nichts.

**How to apply:**
- Updates & Wartung per Scheduled Task ins Fenster 0:15–7:00 legen, nicht tagsüber.
- Active Hours (Nutzungszeit) auf 7:00–0:00 setzen, damit tagsüber keine Auto-Neustarts kommen (blockt aber NICHT die Hintergrund-Downloads — dafür braucht es den nächtlichen Install-Task).
- Geräte müssen zur Laufzeit AN sein (Book/Studio nachts am Netz ok; Pro evtl. aus → verpasste Nächte holen später nach).
- Bei eigenen geplanten Eingriffen (z.B. Diagnose, Reboot-Tests) ebenfalls dieses Fenster bevorzugen.
