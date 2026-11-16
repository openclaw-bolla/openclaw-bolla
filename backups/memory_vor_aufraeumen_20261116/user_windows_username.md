---
name: Windows Username Surface Book
description: Windows-Username auf dem Surface Book ist "ernst", nicht "chris" — wichtig für Pfade
type: user
originSessionId: e270f89d-4073-4435-8244-026e8d351b86
---
Der Windows-Benutzername auf dem Surface Book ist **ernst**, nicht chris.

Korrekte Pfade:
- SSH: `C:\Users\ernst\.ssh\`
- authorized_keys: `C:\Users\ernst\.ssh\authorized_keys`

**Why:** Mehrfach falsch gemacht (chris statt ernst) — Chris musste selbst korrigieren.
**How to apply:** Immer wenn Pfade für das Surface Book generiert werden, `ernst` verwenden.
