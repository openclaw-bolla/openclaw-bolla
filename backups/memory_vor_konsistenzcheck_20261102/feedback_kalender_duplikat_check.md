---
name: feedback-kalender-duplikat-check
description: Vor jedem neuen Outlook-Kalendereintrag ERST prüfen ob er schon existiert — nicht doppelt eintragen
metadata:
  node_type: memory
  type: feedback
  originSessionId: ddc28e86-5ad8-4f8d-ab00-1ad3fbeaf08e
  modified: 2026-09-23T10:26:36.163Z
---

Chris (23.09.2026, Telegram): "Prüfe das nächste mal ob es schon einen Eintrag gibt, dann bitte nicht
nochmal eintragen" — bezog sich auf einen **Outlook-Kalendereintrag** (nicht auf aktuell.md, das war
ein Missverständnis meinerseits in derselben Session).

**Why:** Ein doppelter Kalendereintrag ist für Chris nervig (taucht zweimal im Tagesplan auf, verwirrt) und
schwerer zu bereinigen als ihn vorher zu vermeiden.

**Bestätigter Fall (23.09.2026):** Der Don-Giovanni-Termin (24.09., Hamburgische Staatsoper) stand
tatsächlich **3×** im Kalender — Chris hat bestätigt, dass ich alle drei selbst angelegt habe (vermutlich
beim wiederholten "Termin suchen/anlegen" am 13.09., weil die Original-Mail nirgends auffindbar war und
ich offenbar nicht erkannt habe, dass ein vorheriger Versuch schon geklappt hatte). Chris lässt die drei
Duplikate jetzt bewusst stehen (nicht mehr löschen), aber: **das darf nicht nochmal passieren.**

**How to apply:** Bevor ich einen neuen Termin per Graph-API (`/api/calendar` bzw. `outlook_token.json`-
Skripte wie `mail_to_calendar.py`, `schuljahr2627_calendar_import.py`) anlege, erst gegenchecken, ob am
selben Tag/zur selben Zeit mit ähnlichem Betreff schon ein Eintrag existiert. Gilt AUCH und GERADE dann,
wenn ich selbst kurz zuvor schon einen Anlege-Versuch gemacht habe und mir nicht sicher bin, ob er
durchgegangen ist — dann lieber erst `/api/calendar` (volle Liste, nicht die unzuverlässige Suche) prüfen,
bevor ich es "sicherheitshalber" nochmal anlege.
**⚠️ `/api/calendar/search?q=...` hat sich schon mal als unzuverlässig erwiesen** (fand einen tatsächlich
vorhandenen Termin nicht, s. [[project_mail_urlaub]]/04.09.2026-Vorfall mit Robins Rückflug) — lieber
`/api/calendar` komplett abrufen und selbst nach Datum/Betreff filtern, statt der Server-seitigen Suche
blind zu vertrauen. Bei Zweifel/Unklarheit lieber kurz nachfragen statt zu raten oder einfach anzulegen.

Verwandt: [[feedback_pfad_verifizieren_vor_schreiben]] (gleiches Prinzip: vor dem Schreiben verifizieren),
[[reference_graph_capabilities]].
