---
name: reference-graph-capabilities
description: Was das MS-Graph/Azure-Token in MP DARF — Scopes von ms_token vs. outlook_token (gegen wiederholte Fehlannahmen)
metadata: 
  node_type: memory
  type: reference
  originSessionId: 4fda8dd4-4f6e-4ebf-a0bc-cbf57822bf25
---

# MS Graph / Azure — was geht, was nicht (MP)

Es gibt in MP **ZWEI** Microsoft-Token mit UNTERSCHIEDLICHEN Scopes. Das ist die Quelle wiederholter Verwirrung — vor Behauptungen „geht nicht" IMMER hier nachschauen.

## `config/ms_token.json` (genutzt von `mission_control_api.py` → `get_token()`)
Scope: `Mail.Read Mail.ReadWrite Calendars.Read Contacts.Read offline_access`
→ Kalender nur **lesen**, Kontakte nur lesen. Kein Schreiben.

## `config/outlook_token.json` (+ `config/outlook_oauth2.json`, consumers-Endpoint)
Scope: `Mail.ReadWrite Mail.Send Calendars.ReadWrite Contacts.ReadWrite Tasks.ReadWrite offline_access`
→ **Kalender SCHREIBEN geht!** Termine anlegen/ändern/löschen, Mail senden, Kontakte+Tasks schreiben.
- Vorbild: `scripts/mail_to_calendar.py` legt damit täglich Termine an (`POST /me/calendar/events`).
- In `mission_control_api.py` gekapselt als `_graph_calendar_token()` (refresh) → benutzt von `reise_calendar_storno()`.
- Kategorien IMMER als Name übergeben („Termin", „Wichtig" …), nie als preset-Wert — siehe [[feedback_graph_calendar_categories]].

## Merksatz
„Kalender/Kontakte schreiben?" → **outlook_token.json** nimmt (Calendars.ReadWrite), NICHT ms_token.json.
Nur weil `get_token()` read-only ist, heißt das NICHT, dass MP nicht schreiben kann.

Siehe auch [[reference_mc]], [[reference_technical]].
