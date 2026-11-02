---
name: project-distrokid-desktop-staging
description: DistroKid-Release-Workflow — Desktop-Staging-Ordner pro Song; Spotify-Listing geht sehr schnell
metadata: 
  node_type: memory
  type: project
  originSessionId: 3f696bca-1fae-44a2-97bf-c746cbc047c1
  modified: 2026-08-11T08:11:20.458Z
---

# DistroKid Release-Staging (ab 29.06.2026)

## 🔒 09/2026 — Suno hat den automatischen MP3-Download gesperrt
Seit ~01.09.2026 kann der 🚀-Knopf die MP3 **nicht mehr selbst aus Suno ziehen**:
- `audio_url` im Feed = `https://studio-api.prod.suno.com/api/forbidden` (Platzhalter)
- `cdn1.suno.ai/{id}.mp3` → HTTP 403
- die m4a-Opus-URL aus `media_urls[]` (Cloudfront) liefert einen **verschlüsselten Blob**
  (`encoding: "1.0.0"`, Magic `1f 03 ea 9d`) → ffmpeg scheitert.
UI-Fehler war: „MP3-Download Fehler: HTTP Error 403: Forbidden".

**Workaround (in `_suno_fetch_assets` eingebaut 01.09.):**
1. Song in Suno öffnen → **··· → Download** (bezahlter Plan darf eigene Songs laden).
2. Datei als **`<Titel>.mp3`** (Titel = alphanum + Leer/`_`/`-`) nach
   `D:\OneDrive\Dokumente\Bolla\Suno_DistroKid\` legen.
3. In Bolla Songs Titel eingeben, Haken „MP3+Cover holen" **gesetzt lassen**, 🚀 drücken.
   → Helper erkennt die vorhandene MP3 (>100 KB), überspringt den Download, erzeugt Cover
   (Pollinations) + Ordner + Checkliste + Video + Captions wie gehabt.
Fehlt die MP3 → klare Fehlermeldung mit genau dieser Anleitung statt kryptischem 403.
Wenn Suno wieder öffnet / ein Entschlüssel-Weg bekannt wird → Direkt-Download reaktivieren.

## 🎨 01.09.2026 — Bolla Songs umgebaut: 3-Cover-Auswahl statt Einzel-Cover
Chris fand die einzeln erzeugten Cover „merkwürdig / ganz schlecht" (das ULTRA-SPECTACULAR-Prompt
nahm den Titel wörtlich → „Knöpfe als EKG-Linie" o.ä.). **Neuer Ablauf auf der Bolla-Songs-Seite:**
- Knopf **„🎨 3 Cover-Vorschläge"** (`/api/suno/covers`, ~€0,30 = 3× MAI): Claude macht EINEN
  Stimmungssatz zum Titel (Farbe/Gefühl, keine wörtlichen Motive), daraus 3 Bilder in 3 Stilen —
  „Atmospheric photo" / „Abstract colour & light" / „Minimal graphic poster". 512er-Previews als
  data-URI zurück, 3000er als `<Titel>_cover_1..3.jpg` im Archiv.
- Vorschau anklicken → `/api/suno/pick-cover` kopiert den nach `<Titel>_cover.jpg`, löscht die Kandidaten.
- **`/api/suno/publish` erzeugt KEIN Cover mehr** — verlangt ein vorher ausgewähltes `_cover.jpg`,
  sonst klare Fehlermeldung. Kosten-Confirm-Dialoge im Publish-Schritt raus (Kosten fallen im Cover-Schritt an).
- Direkt-Einzelcover geht noch über `/api/suno/download-cover` (nutzt Stil 0).
- Helfer modul-global: `_suno_cover_concepts`, `_suno_cover_prompt`, `_suno_render_cover_bytes` (MAI→Gemini,
  nie Pollinations außer explizit), `_suno_save_cover_jpg`.

## 🎨 02.09.2026 — Cover-Rework v2: 3 gratis (Pollinations) + „+1 mit MAI", song-bezogener Prompt
Chris' erster 3er-Lauf mit MAI: alle 3 „Schrott", €0,30 versenkt, hatten **nichts mit dem Song zu tun**.
**Ursache = mein Prompt** (Selbst-Einschätzung, von Chris so bestätigt): die v1 ließ Claude nur eine
abstrakte **Farb-„mood"** beschreiben, EXPLIZIT ohne Objekte aus dem Song → für jeden Feel-Good-Song kam
dasselbe „warm/golden/hopeful"-Wallpaper raus. Überkorrektur vom vorherigen Fehler (zu wörtlich →
„Knöpfe als EKG").
**Fix:** `_suno_cover_concepts(titel, lyrics, n)` → Claude bekommt **Titel + Liedtext** und liefert n
**konkrete Bild-Ideen** (je 1 Satz: Szene/Motiv/Symbol, das die Story trägt — aber KEINE wörtliche
Titel-Bebilderung). Getestet: Ideen sitzen jetzt am Song (Tonband, „one shot", Plattenknopf …).
**Ablauf neu:**
- „🎨 3 Cover-Vorschläge" → `/api/suno/covers`, Standard **Pollinations = gratis**, sendet Lyrics mit.
- Reicht keins → Button „🌟 Keins passt? +1 mit MAI (~€0,10)" → `/api/suno/cover-extra` (Slot 4, MAI 2.5).
- Vorschau anklicken → `/api/suno/pick-cover` (räumt Slots 1..4).
- Engine-Umschalter (Poll/Gem/MAI) aus der Seite raus — war nach dem Umbau tot.

## 🔑 01.09.2026 — Suno-Token-Widget aus Bolla Songs entfernt
Chris: „bringt die api zu suno überhaupt noch was? … suno token sache raus." Stimmt — die
DistroKid-Vorbereitung braucht **kein Suno-Token mehr** (MP3 = manuell abgelegte Datei, Cover = MAI,
kein Feed-Call). HTML-`<details>` „🔑 Suno-Token aktualisieren" + `sunoTokenCopyScript`/`sunoTokenSave`/
`SUNO_FETCH_SCRIPT` aus `index.html` raus. **Backend bleibt** (`config/suno_token.json`,
`_suno_token()`, `/api/suno/token`) — der **Blocklist-Lyrics-Scan** `scripts/suno_fetch_filter.py`
liest die Datei noch und `/api/clip/{id}` funktioniert weiter (nur Audio ist gesperrt). Token bei
Bedarf künftig von Hand in die Datei schreiben. `reference_suno_token.md` = nur noch für den Scan relevant.

**Spotify-Tempo:** "Summertime's Callin'" (Bollawave) war **viel schneller live auf Spotify als gedacht** —
DistroKid-Listing geht zügig durch. Also bei Releases nicht lange auf Sichtbarkeit warten, schneller nachschieben planen.

## ⚠️ Update 11.08.2026 — seit dem 🚀-Knopf (11.07.2026) EIGENER UNTERORDNER pro Song, nicht mehr flach
Der „🚀 Alles für DistroKid vorbereiten"-Knopf in Bolla Songs (MP, `/api/suno/publish` → `scripts/distrokid_publish.py`)
legt bewusst `Desktop/DistroKid/<Titel>/` an (nicht mehr flach in `Desktop/DistroKid/`) — so können mehrere Songs
parallel gestaged werden. `scripts/distrokid_staging_cleanup.py` (täglich 9:45) archiviert nur **Unterordner**,
deren Titel im Release-Kalender `done:true` ist — lose Dateien direkt in `Desktop/DistroKid/` (z.B. aus älterer
manueller Vorbereitung ohne den Knopf, wie bei „Back In Session" am 10.08.) werden vom Cleanup-Skript NICHT erkannt
(`folder.is_dir()`-Filter) und bleiben ewig liegen → müssen von Hand ins Backup-Archiv verschoben werden
(passiert bei „Back In Session" am 11.08. manuell). Der separate „Herunterladen & Cover"-Knopf (`/api/suno/download-cover`)
ist NICHT nötig vor dem 🚀-Knopf — der holt MP3+Cover standardmäßig selbst aus Suno (Häkchen an), der andere Knopf
ist nur optional zum Vorab-Reinschauen/Cover-Wechseln.
Der Text unten (EIN flacher Ordner) ist die ALTE Konvention von vor dem Knopf — technisch überholt, nur als Hintergrund stehen gelassen.

## Staging-Ordner-Workflow (Chris' Wunsch, VERALTET seit 11.07.2026 — s.o.)
- Pro Release ein Ordner **`D:\OneDrive\Desktop\DistroKid\`** (= `/mnt/d/OneDrive/Desktop/DistroKid/`) als „Bühne".
- Inhalt: **Song-MP3 + Cover** (Kopie aus dem Archiv `D:\OneDrive\Dokumente\Bolla\Suno_DistroKid\`)
  + die **allgemeine** `DistroKid_Upload_Checkliste.docx` (Kopie)
  + die **song-spezifische Anwendungsdatei** (`_ANWENDUNG_<Titel>.md`: Lyrics, Suno-Style, DistroKid-Settings)
  + ⭐ **IMMER die song-spezifische Upload-Anleitung mit ausgefüllten Feldinhalten** (`Anleitung_Upload_<Titel>.md`):
    fertig zum Abtippen — Künstler/Titel/Sprache/Genre/Stadt/Explicit/KI-Deklaration/Credits/Stores +
    Gegencheck-Liste. Reihenfolge analog `DistroKid_Upload_Checkliste.docx`, aber mit den KONKRETEN Werten dieses Songs.
- **Anwendungsdatei + Upload-Anleitung nur im Desktop-Ordner, NICHT in Bolla/Suno_DistroKid** ablegen.
- Sobald der Song online ist → **Desktop-Ordner einfach komplett löschen.** Wiederverwendbar für jeden nächsten Song.
- Quell-/Archiv-Ordner `Suno_DistroKid` behält MP3 + Cover dauerhaft.

## Stand 29.06.2026
- EN "Summertime's Callin'" = LIVE auf Spotify.
- DE-Version final = "**Läuft, Sommer**" (Summer-Deutschrap; Pop-Version "Der Sommer ruft" war zu schlagerhaft → verworfen).
  ✅ MP3 (320k) + Cover (3000²) gezogen → Archiv + Desktop-Ordner. Desktop hat: MP3, Cover, allg. Checkliste.docx,
  `_ANWENDUNG_Laeuft-Sommer.md`, `Anleitung_Upload_Laeuft-Sommer.md`.
  **Noch zu tun:** DistroKid-Upload am **02.07.** (Slot 2 im neuen Kalender, ≥4 Tage Abstand zu Summertime's Callin'). Danach Desktop-Ordner löschen.

## Release-Kalender neu durchgerechnet 29.06.2026
4-Tage-Floor BLEIBT (Anti-Spam) — schnelles Spotify-Listing ändert den Einreich-Takt NICHT. Sommer-Songs vorgezogen (Saison), DE/EN abwechselnd. Ab 02.07: Läuft Sommer · Sun Sand & Baluhai · Mein Hund · Seven More Weeks · KI-Wunder · Blazing Waves Match · Die Zukunft ist Jetzt · AI Symphony (alle 4 Tage). Straffung auf 3 Tage erst nach 3–4 eingelaufenen Releases. Quelle: `config/bollawave_release_schedule.json`.

## ⭐ Update 06.07.2026 (Chris)
- **Social Media IMMER gleich mitliefern:** Bei JEDEM Release im Staging einen Unterordner `Social Media/<Titel>/` mit **Insta-Caption.txt + TikTok-Caption.txt** (Stil wie „Läuft, Sommer": Feel-Good-Zeile + Hashtags + „überall streamen, nach Bollawave suchen" + 🤖 KI-/Suno-Hinweis). PromoCard-Bild + TikTok-Video kommen automatisch per `distrokid_promo_watcher.py` nach dem Publish (Promo-Card-Mail) — Captions macht Bolla vorab.
- **Cover: IMMER neu via Pollinations generieren, NIE das Suno-Cover nehmen!** (Lehre 06.07.: Suno-`image_large` = das Auto-Cover MIT eingebranntem, verhunztem Titel-Text drauf, z.B. „BALUHAI" + Gekrakel → verstößt gegen „kein Text aufs Cover" + DistroKid lehnt ab.) Also: textfreies Marken-Cover via Pollinations ([[feedback_bildgenerierung]], „no text/letters/words" in den Prompt!), knallig/verspielt/sommerlich → PIL auf **3000²** q92. Archiv-Cover (360²-Thumbs) sind eh zu klein. **Audio** dagegen frisch von Suno als 320 kbps ist ok. ⚠️ **Cover ersetzen → NEUER Dateiname** (sonst Explorer-Thumbnail-Cache zeigt altes Bild, [[reference_thumbnail_cache_falle]]).
- **Lineup markengerecht kuratieren (Chris-Entscheid „kuratieren + Cover neu"):** Die hintere Kalenderhälfte #6–#9 (KI-Wunder, Blazing Waves Match, Die Zukunft ist Jetzt, AI Symphony) sind alte „Cleanstart_8"-KI-Novelty-Songs → passen NICHT zum Feel-Good-Pop-Profil → sollen gegen Feel-Good/Sommer-Tracks getauscht werden; jeder kommende Release bekommt ein markengerechtes Cover (Pollinations, [[feedback_bildgenerierung]], 3000²). ⏳ OFFEN: konkrete Song-Auswahl braucht Suno-Style-Check (Token kurzlebig → Chris holt frischen JWT [[reference_suno_token]]); Archiv hat evtl. zu wenige on-brand Songs → ggf. neue generieren (kostet, Freigabe).

- **FESTE REGEL — Auto-Aufräumen (Chris 06.07.):** Sobald ein Song im Kalender `done:true` ist, wandert sein Desktop-Staging automatisch ins Backup-Archiv → `Desktop/DistroKid/` bleibt immer sauber. Umgesetzt als `scripts/distrokid_staging_cleanup.py` (Cron `45 9 * * *`, täglich kurz nach dem Release-Reminder), matcht Ordnername↔Titel normalisiert, verschiebt nach `backups/distrokid_desktop_archiv/<Ordner>_<ts>/`, meldet per Telegram. Verschiebt NICHT (kein Hard-Delete) → jederzeit wiederherstellbar.
- **MASTER-ARCHIV = `D:\OneDrive\Dokumente\Bolla\Suno_DistroKid\` (Chris „sonst Chaos", 06.07.):** Hauptordner = nur aktuelle/on-brand + released Songs. `_aussortiert/`-Unterordner = Papierkorb für Songs (soft-delete) → off-brand/„passt nicht" dorthin verschieben, NICHT hart löschen. **Sync-Regel:** Jeder Song, der auf dem Desktop im Staging liegt, muss sein finales Release-Asset (mp3 + das FINALE bollawave-Cover, nicht das alte Suno-Text-Thumbnail!) auch im Master-Archiv haben → beim Cover-Tausch IMMER auch das Archiv-Cover aktualisieren. `Cleanstart_8/`-Unterordner = alter Dubletten-Batch (löschbar).

Siehe auch [[project_distrokid_release_profil]], [[project_suno_distrokid_blocklist]].
