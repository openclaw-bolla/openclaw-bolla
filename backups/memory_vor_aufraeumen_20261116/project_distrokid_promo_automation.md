---
name: project-distrokid-promo-automation
description: Auto-Watcher — neue DistroKid-Promo-Card-Mail → TikTok- + Instagram-Material auf Desktop + Telegram-Bescheid
metadata: 
  node_type: memory
  type: project
  originSessionId: 1b6b2f57-06a1-4af7-8297-7aa3e429fd49
  modified: 2026-08-11T15:09:40.388Z
---

Seit 25.06.2026 läuft ein Wächter, der **neue DistroKid-Promo-Card-Mails** ("Here's a photo of …") automatisch verarbeitet.

**Script:** `/home/bolla/workspace/scripts/distrokid_promo_watcher.py`
**Cron:** `20 7-21/2 * * *` (alle 2 Std., 7–21 Uhr) → Log `logs/distrokid_promo.log`
**Processed-Tracking:** `state/distrokid_promo_processed.json` (verhindert Doppel-Posts; aktuelle Pausenklingel-Magie-Mail ist „geseedet" = erledigt)

**Was es tut:** Promo-Card-Bild aus dem Mailanhang holen → 12s-TikTok-Video bauen (ffmpeg, 1080×1920, weil TikTok-Desktop nur Video nimmt) → Caption-.txt (nur einfügbarer Text: HyperFollow-Link + KI-/Suno-Hinweis + #distrokid & Hashtags) → alles auf den **OneDrive-Desktop** → **Telegram-Bescheid** „posten".

**Technik:** importiert `get_token`/`telegram`/`GRAPH` aus `mail_to_calendar.py` (Outlook Graph). HyperFollow-Link wird per Mail-Suche über den Release-Slug gefunden. Künstler-Slug `bollawave` ist hartkodiert (ARTIST_SLUG) — bei neuem DistroKid-Künstlernamen anpassen. Caption ist ein festes Template (kein LLM → robust für Cron).

**Posten macht Chris selbst** in den Desktop-Apps — **BEIDE Plattformen** gehören zum Ablauf: **TikTok** (Video hochladen via TikTok Studio + KI-Label AN) **und Instagram** (Bild direkt posten, kein Video nötig — Erstellen → Beitrag → Bild → Caption → Teilen). Das vom Watcher erzeugte Bild dient beidem (Insta direkt, TikTok als Video-Quelle). Wenn er „fertig" meldet → Desktop-Dateien löschen. Siehe [[feedback_desktop_apps_social]].
Modi: `--test` (nur erkennen), `--seed` (vorhandene Mails als erledigt markieren).

## ⭐⭐ STANDARD-AKTION ab 02.07.2026 — ein Skript pro neuem Song

**Chris' Wunsch:** Bei JEDEM neuen Song automatisch das komplette Social-Paket bauen. Umgesetzt als wiederverwendbares Skript:
**`scripts/distrokid_social_paket.py "<Songname im Archiv>" [--title "Anzeige-Titel"]`**

Baut nach `/mnt/d/OneDrive/Desktop/DistroKid/Social Media/<Song>/`:
1. `<Song>_PromoCard.jpg` = Cover (= das „Promo-Bild"; Insta direkt). **DistroKid liefert kein separates Promo-Bild ohne Login/Promo-Card-Mail (Cloudflare blockt curl) → Cover IST das Promo-Bild.**
2. `<Song>_TikTok-Video.mp4` = Cover 1080×1920 + **15 s Song-Ausschnitt MIT TON** (ab Sek. 30; besser als das stumme Watcher-Standbild). Fallback stumm, falls MP3 fehlt.
3. `<Song>_Insta-Caption.txt` + `_TikTok-Caption.txt` = lebendige Caption via `claude -p` (Sonnet, kein €, Template-Fallback) + **Streaming-Hinweis** (Spotify/Apple/YouTube Music/Amazon + nach „Bollawave" suchen) + Suno-Hinweis, UTF-8-BOM. **⚠️ KEIN DistroKid-Link in der Caption** (Chris 02.07.: in TikTok/Insta-Captions nicht klickbar + Song nicht abspielbar → nutzlos). Link höchstens für Insta-BIO (steht noch in der Anleitung.docx).
4. `ANLEITUNG_<Song>_Posten.docx` (Aptos, KI-Label-Warnung fett).

**⚠️ NIE als „ersten/Debut-Song" framen!** Bollawave hat schon mehrere Releases (Summertime's Callin' etc.). „Läuft, Sommer!" war Chris' erster SELBST hochgeladener Upload — NICHT sein erster Song. Der LLM-Prompt enthält diese Sperre explizit. (Fehler 02.07. gemacht + korrigiert.)

HyperFollow-Slug = `slugify(Titel)` (ä→ae, Komma/Space→„-"): „Läuft, Sommer" → `laeuft-sommer`. Per curl nicht verifizierbar (Cloudflare „Just a moment…") → Slug-Konvention vertrauen, beim Posten kurz gegenchecken. **Unterwegs:** Video + Captions zusätzlich ins mmp legen ([[reference_mmp_media_handoff]]).

## ⭐ NEU 29.06.2026 — Cover-first statt auf Mail warten (Chris' Standardwunsch)

DistroKid schickt die Promo-Card-Mail NICHT zuverlässig pro Song. **Deshalb nicht mehr darauf warten:** Sobald ein Song live ist, baue ich das Social-Media-Paket **direkt aus dem Song-Cover** — manuell, ohne DistroKid-Login. (Die „Card" ist im Kern eh das Cover.) Der Mail-Watcher bleibt als Fallback bestehen.

**Quelle:** Cover + MP3 liegen unter `/mnt/d/OneDrive/Dokumente/Bolla/Suno_DistroKid/<Songname>.jpg` (Cover ist 3000×3000, quadratisch).

**Was ich baue (4 Dateien)** → Zielordner **`/mnt/d/OneDrive/Desktop/DistroKid/Social Media/`**:
1. `<Song>_PromoCard.jpg` — = das Cover (quadratisch, für **Instagram**).
2. `<Song>_TikTok-Video.mp4` — 12 s, 1080×1920, Cover zentriert + schwarze Balken (gleicher ffmpeg-Befehl wie `make_video` im Watcher; TikTok-Desktop nimmt nur Video).
3. `<Song>_Caption.txt` — UTF-8-**BOM** (Notepad-Umlaute), HyperFollow-Link + KI/Suno-Hinweis + **saubere** Hashtags (ohne Bindestrich-Murks aus slugify).
4. `ANLEITUNG_<Song>_Posten.docx` — kurze Schritt-für-Schritt-Anleitung, **Aptos**, kompakt (TikTok → KI-Label AN; Instagram → Bild; danach Ordner löschbar).

**HyperFollow-Link NICHT raten:** Muster `https://distrokid.com/hyperfollow/bollawave/<slug>`. Slug ist meist der entschärfte Titel OHNE Apostroph (z.B. `summertimes-callin`, nicht `summertime-s-callin`). Kandidaten per `curl -s -o /dev/null -w "%{http_code}"` testen → der mit **200** ist echt (403 = existiert nicht). Alternativ aus „Spotify pre-save"-Mail des Songs ziehen.

**Arbeitsteilung:** ICH baue alles. **Chris postet** in den Desktop-Apps (TikTok + Instagram), KI-Label bei TikTok AN. Siehe [[feedback_desktop_apps_social]], [[feedback_word_schriftart]].

**⚠️ TikTok KI-Label MUSS beim Upload gesetzt werden — geht NIE nachträglich!** (Verifiziert 29.06.2026 per TikTok-Support + Screenshot von Chris' Bearbeiten-Menü.) Im nachträglichen „Bearbeiten" gibt es KEINEN KI-Schalter — nur Beschreibung/Cover/Standort/Privatsphäre + „Beitragsinhalt offenlegen → Deine Marke/Markeninhalt" (= Werbe-/Branded-Content-Kennzeichnung, NICHT KI!). Wer den Schalter beim Upload vergisst, kann das offizielle Badge nur durch **Löschen + Neu-Hochladen** nachholen (so bei „Summertime's Callin'" am 29.06.2026 gemacht — Chris hat neu hochgeladen, Label sitzt jetzt). Fallback ohne Neu-Upload: Der Suno-Hinweis steht eh in der Caption → Transparenz ist gegeben.

**📍 WO ist der KI-Schalter beim TikTok-Upload (Studio Web)?** Er ist standardmäßig EINGEKLAPPT! Reihenfolge im Upload-Dialog: Standort → Einstellungen (Wann veröffentlichen / Wer kann sehen / „Uploads von hoher Qualität") → **„Mehr anzeigen ⌄"** anklicken → dort erscheint **„KI-generierte Inhalte"** → Schalter AN → erst dann **„Veröffentlichen"**. Genau dieses „Mehr anzeigen" war der Stolperstein — ohne Aufklappen sieht man den Schalter nicht. In der Word-Anleitung den KI-Schalter-Schritt IMMER fett, mit dem „Mehr anzeigen"-Hinweis und als „vor dem Posten, unwiderruflich" markieren. Siehe [[user_ki_transparenz]].

## ⭐ NEU 11.08.2026 — DistroKid-Promo-Cards für TikTok-Videos nutzen statt Cover+ffmpeg

Chris' Fund: Im DistroKid-Dashboard kann man pro Song aus **mehreren fertigen Promo-Cards** auswählen — er
findet die Qualität "sehr gut". **Ab sofort (künftige Releases):** vor dem TikTok-Video-Bau erst in
DistroKid nachschauen, ob für den Song Promo-Cards zur Auswahl stehen, eine passende auswählen und DIESE als
Basis fürs TikTok-Video nehmen — statt (oder zusätzlich zu) dem bisherigen `distrokid_social_paket.py`-Weg,
der nur das quadratische Cover per ffmpeg auf 1080×1920 zieht (schwarze Balken, kein eigenständiges
Promo-Motiv). Der bestehende `distrokid_promo_watcher.py` reagiert zwar schon auf Promo-Card-**Mails**, aber
das ist unzuverlässig (siehe oben: "DistroKid schickt die Mail NICHT zuverlässig pro Song") — die Auswahl
direkt im Dashboard ist der robustere Weg.

**Noch offen/zu klären beim nächsten Release:** wo genau im DistroKid-Dashboard die Promo-Card-Auswahl liegt
(Login-Zugang siehe [[feedback_website_schreibzugriff]]-Muster), ob die Cards als Bild oder fertiges Video
kommen, und ob `distrokid_social_paket.py` entsprechend angepasst werden soll (Promo-Card statt Cover als
Quelle fürs `ffmpeg`-Video) oder ob Chris die Card manuell auswählt und mir das Bild/Video gibt. Beim
nächsten neuen Song das DistroKid-Dashboard gezielt danach absuchen, bevor der bisherige Cover-Weg
automatisch losläuft.

## ⭐ NEU 10.08.2026 — Instagram-Reel dauerhaft dazu (Chris' Wunsch, zusätzlich zum Bildpost)

Ab sofort baut `distrokid_social_paket.py` **5 statt 4 Dateien**: zusätzlich `<Song>_Instagram-Reel.mp4` — eine reine 1:1-Kopie von `_TikTok-Video.mp4` (eigener Dateiname, damit beim Hochladen in der Insta-App kein "TikTok" im Namen verwirrt). Grund: Instagram spielt Reels algorithmisch deutlich reichweitenstärker aus als reine Bildposts, das Video-Material war eh schon da (kein Mehraufwand). `make_anleitung()` hat jetzt einen dritten Abschnitt **"🎬 Instagram (Reel)"** zwischen Bildpost und Link — Chris postet also künftig 3 statt 2 Inhalte pro Song: TikTok-Video, Insta-Bild, Insta-Reel (gleiche Caption wie beim Bildpost).
