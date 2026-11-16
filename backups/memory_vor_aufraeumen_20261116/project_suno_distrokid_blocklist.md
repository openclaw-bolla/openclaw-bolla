---
name: project-suno-distrokid-blocklist
description: Suno-Songs für DistroKid filtern — dauerhafte Blockliste + Lyrics-Scan-Pflicht (Titel allein reicht NICHT)
metadata: 
  node_type: memory
  type: project
  originSessionId: f4c404b5-dea8-4a98-926b-fa6161421b84
---

# Suno → DistroKid: Blockliste & Lyrics-Scan

Welche der ~393 Suno-Songs auf DistroKid dürfen — und welche NIE (Schüler-Geburtstagslieder, Glücksrad-Klone, Songs mit Namen/„Herr Mandel"/„Lessing-Gymnasium" im **Text**).

## ⚠️ Kernlehre (23.06.2026)
**Titel-Filterung reicht NICHT.** Songs mit harmlosem Titel („Bits and Bytes", „Digital Dreams", „Sonnenzeit") enthalten im **Songtext** Namen wie „Mr Mandel", „Lessing-Gymnasium", Schülernamen (Anisa, Tim, Mino…) oder Geburtstags-Zeilen. Die müssen RAUS. → Vor jeder DistroKid-Auswahl die **Lyrics** prüfen, nicht nur den Titel.

## Lyrics holen (kostenlos, eigener Account)
- `GET https://studio-api-prod.suno.com/api/clip/{id}` mit Bearer-Token aus `config/suno_token.json`
- Songtext steht in `metadata.prompt`. Das Feed-Endpoint (`/api/feed/`) liefert KEINE Lyrics — nur id/title/audio_url.
- Scan-Skript-Vorlage liegt in scratchpad (`scan_lyrics.py`): mappt Ordner-MP3s → id, holt prompt, flaggt Namen/Geburtstag/Glücksrad.

## Dauerhafte Dateien
- **`/home/bolla/workspace/data/suno_blocklist.json`** — 364 Einträge, keyed by Suno-id: `{title, reason, source, since}`. `source:titel` (350, aus Buckets) + `source:lyrics` (14, mit harmlosem Titel aber Name/Geb. im Text). **Bei jedem neuen Filterlauf diese ids subtrahieren** → kein erneutes Sichten.
- **`/home/bolla/workspace/data/suno_distrokid_approved.json`** — 16 geprüft saubere Keeper (Stand 23.06.).
- Buckets/Roh: `data/suno_filter_result.json`, `data/suno_all_songs.json`; Skripte `scripts/suno_fetch_filter.py`, `suno_reclassify.py`.

## Ordner-Stand 23.06.2026
`/mnt/d/OneDrive/Dokumente/Bolla/Suno_DistroKid`: 16 saubere oben (upload-fertig), 14 mit Namen/Geb. im Text nach `_aussortiert/` verschoben (reversibel, nicht gelöscht).
- 14 RAUS: Binary Dreams, Bit by Bit, Bits and Bytes (+Blues/Dreams), Bits und Bytes im Karneval, Cyber Teen Dreamland, Digital Dreams, Hippity Hoppity Chaos, Look at me now, Old Messages, Sonnenzeit, The Kid And The Bytes, 🎶 Titel Zwischen Pixeln und Papier.
- ~~3 Keeper enthalten generisches „classroom/gymnasium/Schulbücher" OHNE Name/Schulname (Bunny Hop Hustle, Hoppin' Into Easter, Sommerstrahl) → bleiben verteilbar.~~ **KORRIGIERT 10.07.2026, s.u. — das war falsch, alle drei RAUS.**

## ⚠️ Dritte Falle: Klassen-Kurzform „7a/7b/7c" (Lehre 10.07.2026, GRAVIEREND)
Der ursprüngliche Scan von 23.06. suchte nur `klasse\s*\d` (ausgeschriebenes Wort „Klasse") und Namen — die viel häufigere **Kurzform „7a"/„7b"/„7c"** (echte Klassenbezeichnungen am Lessing-Gymnasium) wurde NICHT erkannt. Beim Nachprüfen am 10.07. waren dadurch **5 von 15 als „sauber" freigegebene Songs tatsächlich kontaminiert**: Sommerleuchten (7A), Sommerstrahl (7C), Bunny Hop Hustle (7b), Der verrückte Hasenhüpfer (7b), Hoppin' Into Easter (7C). Alle 5 jetzt in `suno_blocklist.json` (reason „Klassen-Kürzel im Text") + nach `_aussortiert/` verschoben + aus `suno_distrokid_approved.json` entfernt.
**Fix:** `SCAN_PATTERNS` in `scripts/distrokid_publish.py` um `r"\b[5-9][a-dA-D]\b"` ergänzt (fängt 5a–9d, case-insensitive-ish für a-d). Gilt ab sofort automatisch bei jedem `distrokid_publish.py`-Lauf.
**⚠️ NOCH OFFEN — dringend:** Die schon LIVE veröffentlichten Songs „Läuft, Sommer!" und „Summertime's Callin'" konnten NICHT nachgeprüft werden (Suno-Feed-Token abgelaufen, `/api/clip/{id}` ging noch, `/api/feed/` gab 401 — brauchte die ID aus dem Feed, da beide nach dem 23.06.-Snapshot entstanden sind). „Pausenklingel-Magie" und „Sun, Sand & Baluhai!" wurden geprüft und sind sauber (nur „die siebte Klasse" ausgeschrieben, kein Kürzel). **Sobald Chris einen frischen Suno-Token holt** ([[reference_suno_token]]): Läuft-Sommer + Summertime's-Callin'-IDs im Feed suchen, Lyrics holen, mit dem neuen Regex prüfen. Falls kontaminiert → echtes Live-Problem, Rücksprache mit Chris nötig (Takedown-Frage).
**Restbestand für künftige on-brand Sommer-Slots:** Nach dieser Bereinigung bleibt nur noch „Prairie Moonlight Waltz" übrig (textlos/instrumental, aber Western-Folk-Stil, off-brand, noch nicht als MP3 im Archiv) — für Slot #5 (14.07., vorher „Seven More Weeks") aktuell **kein sauberer on-brand Kandidat verfügbar**. Braucht entweder neue Suno-Generierung (kostenpflichtig, Freigabe nötig) oder Slot verschieben.

## ⚠️ Zweite Falle: Soundalike / Stil-Imitation (NICHT per Text fangbar!)
Manche Suno-Tracks **klingen** absichtlich nach einem realen Star (z.B. „Lights Fade Slowly" = Billie-Eilish-Soundalike — war so beim Generieren geplant). Das ist auf DistroKid ein **Rechte-Risiko** (Persönlichkeitsrecht an Stimme/Stil) → RAUS. Lässt sich nur durchs **Hören** erkennen, kein Lyrics-Scan. Wenn Chris sowas meldet: id in Blockliste mit `reason:"Stil-/Stimm-Imitation … — Rechte-Risiko"`, `source:"chris"`.

## Regel für künftige Trash-Songs
Wenn Chris weitere Songs aussortiert: id in `suno_blocklist.json` mit `source:"chris"` ergänzen — siehe [[reference_suno]].

## ⚠️ Anti-Spam-Takt beim Releasen (Konto-Schutz)
Artist „Bollawave" (Künstlername seit 23.06.2026, ≠ Suno-Altname StingingWallOfSounds). **NIE viele KI-Songs im Akkord hochladen** (Chris fragte „2/Tag?"): neuer Artist + KI-Musik + 0 Hörer = exakt das Spam-Muster, das DistroKid (Distrolock) + Spotify sperren — vermutlich die RouteNote-Sperr-Ursache. **Takt: ~1 Single alle 4 Tage** (Kalender `config/bollawave_release_schedule.json`, Reminder-Cron `bollawave_release_reminder.py`). Tracking: `spotify_watcher.py` (Apple/iTunes gratis; Spotify, wenn `config/spotify_credentials.json` da). Erste Single „Pausenklingel-Magie" live-eingereicht 23.06.

## Suno kann jetzt Chris' eigene Stimme (Voice, neu 06/2026)
„Pausenklingel-Magie" ist mit Chris' echter Stimme gesungen → unverwechselbar eigene DNA, starker Cleanstart-Kandidat (anders als Genre-Klone). Bei künftiger Produktion: „mit Chris' Stimme" ist eine Option.

## DistroKid Release-Mechanik (aus Mails 23./24.06.2026)
- **Pre-save / Hyperfollow-Link** (zum Bewerben, Leute speichern Song vorab): Muster `https://distrokid.com/hyperfollow/bollawave/<song-slug>`. Pausenklingel-Magie: `…/pausenklingel-magie`. DistroKid erstellt die Seite automatisch pro Release.
- **Stores (23):** Amazon, Anghami, Apple Music, MediaNet, Boomplay, Deezer, Instagram/Facebook, Adaptr, Flo, YouTube Music, iHeartRadio, Claro Música, iTunes, Joox, Kuack Media, NetEase, Qobuz, Pandora, Saavn, Spotify, Tencent, Tidal, TikTok/ByteDance.
- **Typische Live-Zeiten:** Apple/iTunes 1–7 Tage (oft selber Tag; selten +manuelle Prüfung), Spotify bis 5 Tage, YouTube Music ~3 Tage, Amazon 2–4 Tage, Deezer 1–2 Wochen, Pandora 1–2 Wochen (kuratiert).
- Release-Dashboard pro Album: `distrokid.com/dashboard/album/?albumuuid=…` (Pausenklingel-Magie UUID 1CBE0EC6-B3B0-4910-956DE65E84F6A8F4).
- Mails kommen von `mailbot@distrokid.com` + `dk@hello.distrokid.com`.
