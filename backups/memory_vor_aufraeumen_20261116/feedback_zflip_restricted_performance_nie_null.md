---
name: feedback-zflip-restricted-performance-nie-null
description: Z Flip 3 (Reni) — restricted_device_performance NIEMALS auf 0 setzen, Handy stürzt ab
metadata:
  type: feedback
---

`settings put global restricted_device_performance 0` am Z Flip 3 löst Absturz/Neustart aus (2× reproduziert, 13.+14.11.2026, Chris hat es bestätigt).

**Why:** Gestern hielten wir ADB insgesamt für schuldig; tatsächlich ist es genau dieser Befehl.
**How to apply:** Wert bleibt `1`. Am Z Flip nie schreibend an diesem Schalter; lesende ADB-Abfragen sind ok. Siehe [[project_zflip_ruckeln]].
