---
name: reference-heimnetz-kamera-blockade
description: Heim-WLAN blockiert Kamera-/Video-Verbindungen zu externen Verifizierungs-Diensten — bei Handy-Kamera-Problemen als Ursache prüfen
metadata:
  type: reference
  originSessionId: current
  modified: 2026-07-23T16:41:28.216Z
---

**Bestätigt 23.07.2026:** LinkedIn-Ausweisverifizierung (Perso-Scan per Kamera) hing auf P20 UND Duo
identisch fest (blauer Ladebalken, kein Fortschritt trotz erteilter Kamera-Berechtigung). Fix: WLAN aus,
mobile Daten an → Verifizierung lief sofort durch. Also eindeutig das Heim-WLAN/Router, nicht Gerät oder App.

**Verdacht (noch nicht verifiziert):** Passt zum bekannten Muster bei [[user_fsecure]] — F-Secure hat schon
mal die Kamera in Bolla (Edge-Browserschutz) blockiert und musste per Website-Ausnahme freigeschaltet werden.
Falls F-Secure auch am Router/Netzwerk ansetzt (z.B. F-SECURE SENSE oder eine Netzwerk-Schutzfunktion), wäre
das dieselbe Ursache nur auf Netzwerkebene. Noch nicht geprüft, ob es sowas im Haushalt gibt — falls das
Problem nochmal auftritt, dort nachsehen.

**How to apply:** Bei jedem "Kamera/Video startet nicht, hängt beim Laden"-Problem auf Handys im Heim-WLAN
→ zuerst mobile Daten testen (schneller Ausschlusstest). Wenn das den Unterschied macht, ist es das Netzwerk,
nicht die App/Berechtigung — F-Secure-Netzwerkschutz oder Router-Firewall als nächstes prüfen.
