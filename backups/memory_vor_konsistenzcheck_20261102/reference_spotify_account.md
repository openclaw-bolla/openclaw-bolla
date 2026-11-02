---
name: reference-spotify-account
description: Spotify — welcher Account Premium hat (wtnet) und unter welchem die Developer-App liegen MUSS
metadata: 
  node_type: memory
  type: reference
  originSessionId: cefdd4d2-b0a9-489d-9281-20fe4a8e6ffc
---

# Spotify-Accounts — der wichtige Unterschied (geklärt 25.06.2026)

Chris hat **zwei** Spotify-Accounts — das war die Ursache für den blockierten Developer-Key:

| Rolle | Account / Login | Status |
|---|---|---|
| 🎧 **Hör-Account (Premium)** | **chrismandel@wtnet.de** (E-Mail + Passwort) | Premium — verifiziert übers Geburtsdatum 21.12.1955 |
| 🛠️ falsch genutzt fürs Dashboard | **Google-Login** (chrismandel13@gmail.com, „Mit Google") | gratis → Web API blockiert |

**Kernregel:** Die **Spotify-Developer-App MUSS unter dem wtnet-Premium-Account** angelegt sein, NICHT über den Google-Login. Spotify blockiert die Web API komplett (403 „you do not have a Spotify Premium subscription"), wenn der **App-Owner-Account** kein aktives Premium hat — der Hör-Account zählt nicht, nur der Account der die App besitzt.

**Login fürs Developer-Dashboard:** developer.spotify.com → NICHT „Mit Google", sondern **„Mit E-Mail einloggen" → chrismandel@wtnet.de** + Passwort.

**✅ GELÖST 25.06.2026:** Neue App „Bolla Monitor" unter wtnet angelegt, client_id `eaf06cbcef4341758a46d08460bddb5e` (Secret in `config/spotify_credentials.json`, chmod 600). Web API liefert jetzt 200 — **`spotify_watcher.py` lebt wieder** (Release-Erkennung Spotify+Apple). Alte Google-App ist obsolet.

**Schnellzugriff (Client-Credentials, kein €):** Token via `POST accounts.spotify.com/api/token` (grant_type=client_credentials, auth=client_id/secret aus `config/spotify_credentials.json`) → `GET api.spotify.com/v1/search`. Vorlage: `spotify_watcher.py`. **bollawave Artist-URL:** `https://open.spotify.com/artist/36PaSH7OH8FfuFXsSBmlxV` (ID `36PaSH7OH8FfuFXsSBmlxV`, gefunden 05.07.2026 via `type=artist`). Siehe [[reference_bollawave_kuenstlername]].

**Was mit Client-Credentials geht / nicht geht (getestet 25.06.):** ✅ Search (artist, `genre:dance`). ❌ Editorial-Playlists, Browse-Kategorien, New-Releases (alle 403 — Spotify-Regel seit Nov 2024, NICHT Premium-abhängig). Spotify hat zudem keine offizielle Charts-API. → **Dance-Tab in Bolla Songs bleibt bewusst auf Apple/iTunes RSS** (echte Charts-Reihenfolge, Mainstream-Pop); Spotifys `genre:dance` ist Club/EDM ohne Charts-Sortierung. Bezug: [[project_distrokid_release_profil]], [[reference_bolla_songs]].
