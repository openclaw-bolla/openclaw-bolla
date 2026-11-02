---
name: project-qr-landingpage-trailer-muster
description: "Bewährtes Muster für jedes Buchprojekt: QR-Code (Cover/Buch) → Landingpage auf chrismandel.de mit Trailer + eigenem Song, DE+EN; plus Verbreitungs-Kanäle-Plan (Zeitplan bis Launch ~Weihnachten 2026)"
metadata:
  type: project
---

Chris 26.10.2026 („sehr stark, hat geklappt, unbedingt merken und zukünftigen Projekten zuordnen"): Das Muster **Trailer + eigener Song + Landingpage hinter einem QR-Code** hat bei AURORA II komplett funktioniert und gilt als **Standard für künftige Buchprojekte** (AURORA III, Sekretariat-Buch [[project_buch_sekretariat]] u. a.) — und soll **auf den Covern** der jeweiligen Bücher stehen (ev. auch rückwirkend AURORA I → nur fragen, nicht ungefragt, [[project_aurora_ii_song_qr]]).

**Der Ablauf (so wie 21.–26.10.2026 gebaut):**
1. Blender-Quervideo (3 min, ohne Ton) → [[project_aurora_ii_trailer_blender]]
2. Song in Suno: Lyrics/Style/Exclude/Titel **schrittweise per Windows-Zwischenablage** an Chris (Style → Exclude → Lyrics → Titel, jeweils „weiter"); EN-Fassung = sinngemäße Neudichtung, nicht wörtlich; Entwurfs-TXT in `7_Trailer\Song\`
3. Trailer per ffmpeg bauen (`workspace/scratch/trailer_zt/build*.sh`): Video auf Songlänge + ~3,7 s Nachlauf kürzen, **Song ab 1 s (nicht 12 s!)**, Fade-in/out; Web-Version 720p **unter 25 MB** (Cloudflare-Pages-Limit pro Datei)
4. Landingpage: `workspace/chrismandel-neu-2026/build_aurora2.py` (`vid=` pro Sprache) → `/aurora2/` + `/en/aurora2/`; Deploy per `kif_publish_site.deploy_production()`
5. **Cache-Falle:** Videos auf Pages haben `max-age=14400` (4 h) → bei jeder Änderung `?v=N` am Video-Link hochzählen, sonst sieht Chris/Besucher stundenlang die alte Version
6. Ablage: volle 1080p in `Bolla\AURORA II\7_Trailer\Trailer_fertig\`, LIES_MICH.txt pflegen (war einmal veraltet → Fehlinfo)

**Verbreitung des QR-Codes / der Landingpage — später gemeinsam prüfen (Chris will diskutieren):**
- E-Mail an KI-Ethikerinnen/-Ethiker, Buchclubs ([[feedback_aurora_mail_bester_kanal]] — Direkt-Mail ist der beste Kanal, Website-Link immer rein: [[feedback_aurora_mail_website_immer]])
- LinkedIn: nur als **eigener aktiver Post** mit Trailer (kein Kontakt-Outreach, [[feedback_linkedin_kein_kanal]])
- weitere Ideen offen: Goodreads/LovelyBooks ([[project_aurora_goodreads_lovelybooks]]), Autoren-Bio, Newsletter, Social-Clips aus dem Trailer

**Zeitplan-Empfehlung (Chris: AURORA II fertig bis ca. Weihnachten 2026):**
- Bis Ende Nov: nichts Ausgehendes; Song über DistroKid einreichen (Vorlauf 1–2 Wochen, [[project_distrokid_desktop_staging]]); QR-Platzierung festlegen
- Anfang/Mitte Dez: QR final ins Cover II (Rückseite) + Buch einbauen, **Probedruck-/Scan-Test**; Landingpage-Texte final
- Launch-Woche (nach KDP-Freigabe ~72 h): Mails an Ethikerinnen/Buchclubs, LinkedIn-Eigenpost, Goodreads
- Realistisch Januar-Soft-Launch statt Weihnachtsgeschäft, falls Buch erst um Weihnachten fertig (Paperback-Weihnachtslieferung braucht Veröffentlichung bis ~15. Dez.)

## YouTube (26.10.2026 erledigt) — Kanal @chrisman… (Chris Mandel, Konto chrismandel13@gmail.com)
- Live (öffentlich): DE https://youtu.be/yxVho5QYpYY · EN https://youtu.be/mHssAaEraGg (1080p-Fassungen aus `Trailer_fertig`, Beschreibung mit Landingpage-Link, KI-Transparenz-Zeile, „nicht für Kinder“)
- **Methode (funktioniert, Auto-Mode-konform):** Windows-Edge mit eigenem Profil starten (`msedge.exe --remote-debugging-port=9336 --user-data-dir=C:\Users\ernst\bolla_tools\yt_profile`, Chris war dort schon eingeloggt) und Playwright **mit WINDOWS-Python 3.13** (`C:\Users\ernst\AppData\Local\Programs\Python\Python313\python.exe`, playwright per pip installiert) per `connect_over_cdp("http://127.0.0.1:9336")` steuern — NICHT aus WSL (CDP-Port nicht erreichbar; Port-Relay ins Netz blockt der Classifier zu Recht). Dateien >50 MB nur via CDP `DOM.setFileInputFiles` mit Pfad, nicht `set_input_files`. Skripte `yt_step1/2/3.py`, `yt_pub.py` in `C:\Users\ernst\bolla_tools\`. Studio-Selektoren: `#title-textarea #textbox`, `#description-textarea #textbox`, `[name="VIDEO_MADE_FOR_KIDS_NOT_MFK"]`, `#next-button`, `[name="PUBLIC"]`, `#done-button`.
- Tab darf erst nach Upload/Verarbeitung schließen. Chris will TikTok/Insta ab ~Mitte/Ende Nov. (Hochkant-Clip 15–30 s nötig, Konten vorhanden).
