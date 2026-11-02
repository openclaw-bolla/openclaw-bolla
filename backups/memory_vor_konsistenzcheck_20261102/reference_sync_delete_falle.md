---
name: reference-sync-delete-falle
description: Kontakt nur einseitig gelöscht? Bidir. Outlook↔Gmail-Sync holt ihn zurück — beidseitig löschen
metadata: 
  node_type: memory
  type: reference
  originSessionId: 4e4e8d14-aa99-43a5-afe3-2226074f212b
---

# Sync-Lösch-Falle (Outlook ↔ Gmail)

Der bidirektionale Kontakt-Sync (`scripts/outlook_gmail_sync.py`, Cron So 18:00) propagiert **keine Löschungen**. Wird ein Kontakt nur in EINEM System gelöscht, sieht der nächste Sync „existiert drüben, fehlt hier" und legt ihn **neu an** — die Löschung ist rückgängig.

**Beobachtet 18.06.2026:** Jochen Seybold + Imke u. Peter Mehlhorn nur in Outlook gelöscht → Sync holte beide aus Gmail zurück.

**Wie richtig:** Kontakte IMMER beidseitig löschen mit `scripts/delete_contacts_both.py` (DRY-RUN default, `apply` zum Ausführen — löscht per displayName in Gmail via People-API `:deleteContact` UND in Outlook via Graph). Erst danach ggf. syncen.

Verwandt: [[reference-bolla-docs]] · Telefon-Normalisierung: `scripts/phone_normalize.py`.
