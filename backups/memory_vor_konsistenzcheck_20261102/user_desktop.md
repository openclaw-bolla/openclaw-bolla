---
name: Windows Desktop-Pfad
description: Chris' Desktop liegt in OneDrive auf Laufwerk D — IMMER /mnt/d/OneDrive/Desktop/ verwenden
type: user
originSessionId: 392e2e08-0564-42ef-9c3b-3e90798109e6
---
Chris' Windows-Desktop ist OneDrive-synchronisiert und liegt auf **Laufwerk D:**

- Windows: `D:\OneDrive\Desktop\`
- WSL2: `/mnt/d/OneDrive/Desktop/`

**FALSCH (nie verwenden):**
- `/mnt/c/Users/ernst/Desktop` — leer
- `/mnt/c/Users/ernst/OneDrive/Desktop` — auch C:, falsch

⚠ Ich habe das mehrfach falsch gemacht. Beim Speichern von PDFs, Bildern, Dokumenten auf den Desktop IMMER `/mnt/d/OneDrive/Desktop/` verwenden — nie raten, nie C:.
