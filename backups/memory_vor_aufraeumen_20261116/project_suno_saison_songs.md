---
name: project-suno-saison-songs
description: "Suno-Saisonsongs mit Klassen-Kürzel (7A/7B/7C) — vor Ostern 2027 allgemeiner neu machen, dann erst DistroKid"
metadata: 
  node_type: memory
  type: project
  originSessionId: f4c404b5-dea8-4a98-926b-fa6161421b84
---

# Suno Saison-Songs neu machen (allgemeiner) — vor Ostern 2027

5 Songs im `Suno_DistroKid`-Ordner nennen im **Text** eine Klassenbezeichnung (7A/7B/7C) → für einen anonymen Künstler-Release unpassend (zu schul-/klassenspezifisch). Chris (23.06.2026): **nicht löschen** — die sind saisonal eh erst zur jeweiligen Jahreszeit gut, er macht sie dann **nochmal allgemeiner** (ohne Klassen-Kürzel) und bringt sie erst dann raus.

## Betroffene Songs
- **Oster-Songs (3):** Bunny Hop Hustle (7b) · Der verrückte Hasenhüpfer (7b) · Hoppin' Into Easter (7C)
- **Sommer-Songs (2):** Sommerleuchten (7A) · Sommerstrahl (7C)

## ⏰ ERINNERUNG
- **Anfang Februar 2027 (~01.02., ca. 8 Wochen vor Ostersonntag 28.03.2027):** Chris erinnern, die 3 Oster-Songs allgemeiner neu zu generieren (Klassen-Kürzel raus) → dann DistroKid. Reichlich Vorlauf wegen Vertrieb-Review (Wochen) + Neugenerierung. (Chris will die Erinnerung bewusst ein paar Wochen früher als knapp-vor-Ostern.)
- **Anfang April 2027 (~01.04., ca. 8 Wochen vor Sommerferien SH):** dasselbe für die 2 Sommer-Songs.

## ✅ Reminder aktiv — ZWEI Kanäle (Gürtel + Hosenträger, 06.07.2026)
1. **Lokaler Cron** (ausführlich): `scripts/suno_ostern_reminder.py` + Crontab `0 9 * * *` — feuert ab 01.02.2027, alle 3 Tage per Telegram (max 6×), datumsbasiert (übersteht aus-PC). Stoppen: Chris sagt „Oster-Songs sind erledigt" → `config/suno_ostern_reminder_state.json` `done:true`. Nachteil: **nur wenn Home-Server läuft**.
2. **Cloud-Trigger (Failsafe, neu 06.07.)**: `trig_01LEvt17hHS4QDxYyeH1pvs1` (Claude-Code-Remote), one-shot **2027-02-02 08:00 UTC** (=09:00 CET), fresh Session, Push aufs Handy + E-Mail. Kommt auch, wenn der PC aus ist. Löschen via `delete_trigger`.
(Alter Hinweis „Cloud-/schedule ging NICHT" bezog sich auf den `/schedule`-Weg; der neue create_trigger mit eigener Session funktioniert.) Sommer-Songs: bei Bedarf zweiten Reminder ~01.04.2027 analog anlegen.

## Bezug
Diese 5 sind NICHT Teil des Cleanstart-Erstrelease (8 Tracks). Sie bleiben im Ordner als „später überarbeiten". Blockliste/Whitelist-System: [[project-suno-distrokid-blocklist]].
