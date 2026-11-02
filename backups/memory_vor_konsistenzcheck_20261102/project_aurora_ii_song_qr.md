---
name: project-aurora-ii-song-qr
description: "AURORA II — geplanter bollawave-Song zum Buch + QR-Code im Buch mit Link zu Spotify/Apple Music. Jetzt nur merken, in der Buch-Endphase aktiv erinnern."
metadata:
  node_type: memory
  type: project
  originSessionId: current
  modified: 2026-09-07T16:47:13.056Z
---

# AURORA II — Song zum Buch + QR-Code

Chris' Wunsch (07.09.2026): Zu [[project_aurora_ii]] soll es einen eigenen **bollawave-Song** geben,
und im gedruckten/digitalen Buch einen **QR-Code mit Link** zum Song (Spotify / Apple Music / o.ä.).

**Status: nur vormerken.** Details bewusst noch NICHT entschieden — wird besprochen, wenn das Buch
in der Endphase ist.

## Warum jetzt schon notieren
Chris hat es explizit als "jetzt schon mal merken und in der Endphase erinnern" formuliert. Ohne
Merker geht es im laufenden Kapitel-Betrieb unter, und ein Song-Release + QR-Code-Integration will
zeitlich zum Buch-Launch passen (Song sollte live sein, wenn das Buch erscheint).

## How to apply — Trigger: AURORA II ist in der Endphase
"Endphase" = letzte Kapitel stehen / Lektorat läuft / KDP-Metadaten & Build werden vorbereitet
(analog zum Ablauf in [[project_aurora_update_checklist]]). Dann proaktiv ansprechen:

1. **Song erstellen** — über den MP-Song-Generator im `profil`-Modus (bollawave-Stimme), Thema/Ton
   passend zu AURORA II (KI wächst zur Volljährigkeit; Marlie als Heldin; Staunen + Warnung).
   Sprache klären (DE, EN, oder beides — Buch gibt es in DE und EN).
2. **Release** über DistroKid → Spotify/Apple/etc. ([[reference_bollawave_kuenstlername]],
   [[reference_suno]], [[project_distrokid_desktop_staging]]). Muss VOR Buch-Launch live sein.
3. **QR-Code ins Buch** — noch offen zu klären mit Chris:
   - Wohin im Buch? (eigene Seite hinten / im Impressum / bei der Autoren-Bio)
   - DE- und EN-Ausgabe je eigener QR? Print UND eBook?
   - Ziel des Links: direkter Spotify-Link vs. Apple vs. **eine Landing-Page auf chrismandel.de**
     (Landing-Page ist robuster: wenn sich Streaming-URLs ändern, muss nicht das Buch neu gebaut
     werden — nur die Weiterleitung. Empfehlung, aber Chris entscheidet.)
   - QR-Code-Erzeugung + Platzierung im Build (`scripts/aurora_print_pdf.py` / EPUB-Generatoren),
     [[project_aurora_hardcoded_blocks]] beachten (Bio/Vorspann teils in Build-Skripten).
4. Prüfen, ob Chris denselben Song-/QR-Ansatz **rückwirkend auch für AURORA I** möchte (nur fragen,
   nicht ungefragt umsetzen — Buch I ist live, [[project_aurora_identifiers]]).

## ✍️ Song-Entwurf v1 steht (21.10.2026)
Chris wollte „zur Entspannung" einen Versuch: deutscher melodischer Hip-Hop passend zum Quer-Video. Titel **„Orange war gestern (feat. Aurora)"** (Chris: „Aus Licht gemacht" war zu esoterisch; Titelstil aus aktuellen DE-Rap-Charts abgeleitet). Lyrics + Style + Exclude + Regler liegen in `Bolla\AURORA II\7_Trailer\Song\Song_Orange_war_gestern_Entwurf_v1.txt`. Noch NICHT in Suno generiert. Spoilerfrei (nur Stoff bis Kap. 12, siehe [[feedback_aurora_ii_chris_lesestand]]). Zum Weiterbauen: Text feilen, nicht den Style ([[feedback_suno_lyrics_qualitaet]], [[feedback_suno_deutsch_genre]]).
**Korrektur 21.10.:** Hook „Ich bin aus Licht gemacht" ersetzt durch „Ich bin aus Fragen gemacht" — Aurora ist im Buch Software, nicht Licht (Video-Bild ≠ Aussage über die KI; Leser-Stolperstein). Lehre: Song-Aussagen über Aurora müssen zur Buchlogik passen, Video-Metaphern nur als Bild.
**Suno-Test 21.10. (erste 4 Songs):** „ganz ok", Lyrics top → unverändert lassen. Style v1 war zu seicht (Chillout) → Style v2 mit 808/Trap-Drums/92 BPM, „autotune" aus dem Exclude. Lehre: „melodisch" nicht mit „sanft" gleichsetzen; modernen DE-Hip-Hop mit Drum-/Bass-Druck beschreiben.
**Stand 21.10. abends:** Style v2 „klingt besser" (Chris). Chris liefert evtl. noch einen aktuellen Hit als Referenz → dann Style daran schärfen (name-frei beschreiben, [[feedback_suno_style_no_names]]). In moin unter „Projekte auf Zuruf" geführt.

## ✅ 24.10.2026: Song fertig + im Trailer + live
Chris' Song `Bolla\AURORA II\7_Trailer\Song\Orange_war_gestern_feat_Aurora.wav` (2:36). Trailer mit Ton: `7_Trailer\Trailer_fertig\AURORA_II_Trailer_Orange_war_gestern.mp4` (1080p, 850 MB; Song ab 0:12, Fades). Web-Version 720p 20,8 MB (Pages-Limit 25 MB/Datei!) liegt als assets/aurora2-trailer.mp4 live auf chrismandel.de/aurora2/ (DE+EN, Texte "ohne Ton" angepasst). Offen: Song über DistroKid veröffentlichen, QR-Code ins Buch.

## 26.10.2026: Neuansatz v2 (Chris: Style v1 zu langweilig, Text nicht 100 %)
Chris schlug Zauber-/Houdini-Bounce-Style vor (hat bei Schülersongs mehrfach funktioniert). Bolla-Vorschlag: ja, aber dunkel/theatralisch + Motiv „Kein Zaubertrick (Abrakadabra)". Entwurf: `7_Trailer\Song\Song_Abrakadabra_Entwurf_v2.txt`. Noch nicht in Suno. Der fertige Song v1 „Orange war gestern" bleibt im Trailer, bis v2 besser ist.

## ✅ 26.10.2026: Song v2 „Kein Zaubertrick (feat. Aurora)“ ersetzt „Orange war gestern“ überall
Chris: „sehr gute song geworden, viel lebendiger“. WAV (2:17): `7_Trailer\Song\Kein_Zaubertrick_feat_Aurora.wav`. Trailer: `Trailer_fertig\AURORA_II_Trailer_Kein_Zaubertrick.mp4` (1080p, 152 s; Video gekürzt, Song ab 0:12, Fades). Web 720p (20,6 MB) live als assets/aurora2-trailer.mp4; Notiztexte auf /aurora2/ DE+EN + Startseiten-Karte (DE/EN) angepasst, build_aurora2.py/build_home.py nachgezogen, deployt per `kif_publish_site.deploy_production()` (reines `npx wrangler` scheitert ohne Token-Env). Alter Song + alte Trailer-MP4s + Entwürfe liegen in `_Archiv_alte_Versionen\Song_v1_Orange_war_gestern\`. OFFEN: DistroKid-Release (Titel „Kein Zaubertrick (feat. Aurora)“), QR-Code ins Buch.
