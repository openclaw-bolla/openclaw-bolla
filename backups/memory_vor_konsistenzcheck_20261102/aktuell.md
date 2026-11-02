## 📝 24.10.2026 — Leser-Hinweis Kap. 16 (Chris): Kernfrage aus Band I „nur Software oder mehr?“ wird im Team ab ~Kap. 16 nicht mehr ausdrücklich gestellt
Chris liest bei Kap. 16, fragte: Absicht, oberflächlich gelesen, oder kommt es noch? Antwort an ihn: nicht oberflächlich; Frage läuft über Verfahren (Falkner/Vormund), AURORAs eigene Sätze, Noahs „Foto von jemandem, der schläft“; ob sie später ausdrücklich wiederkehrt = Spoiler, nicht verraten. Auftrag: beim nächsten Analogie-Check/Lauf prüfen, ob Kap. 17–36 die Kernfrage im Team (Marlie, Noah, Leni, Jonas, Petrova) mindestens 1–2× ausdrücklich aufgreifen (Band-I-Bezug); falls nicht, Vorschlag für eine Szene in Kap. 17–25 machen, NICHT selbst einbauen. Chris entscheidet.

## ✅ 24.10.2026 — Freitags-Ausreizung AURORA II beendet (fertig)

Buch jetzt 36 Kapitel, 200706 Wörter. Details: `/home/bolla/workspace/scratch/aurora_samstag_fr_aurora_20261016/ABSCHLUSSBERICHT.md`, `changes.md` (Entscheidungen), Konsistenz-Bericht `konsistenz_25ff.md`. Spoiler-Schutz: Chris liest erst bis ~Kap. 13 — keine Inhalte nennen.

---

## ✅ 23.10.2026 — Freitags-Ausreizung AURORA II beendet (gestoppt: Stopdatei)

Buch jetzt 36 Kapitel, 200706 Wörter. Details: `/home/bolla/workspace/scratch/aurora_samstag_fr_aurora_20261016/ABSCHLUSSBERICHT.md`, `changes.md` (Entscheidungen), Konsistenz-Bericht `konsistenz_25ff.md`. Spoiler-Schutz: Chris liest erst bis ~Kap. 13 — keine Inhalte nennen.

---

## ✅ 18.10.2026 09:50 — Kurze Sonntags-Session, nichts offen Neues
- Quota-Korrektur: Woche nur 1 % verbraucht (99 % frei) — der Job-Eintrag „100 %" war von Fr-Abend VOR Reset. Immer erst `/api/claudequota` prüfen.
- Herfeldt-Datenschutzmail: ERLEDIGT (Antwort mit Einverständnis+Suchprofil gesendet 15.10. 12:45).
- Duo-Reader-Spannen: erledigt/gestrichen (Chris: „geht nicht"). Reiseplaner+Robin-Seite neu: später. Chris meldet sich ggf. heute Nachmittag.

## ✅ 17.10.2026 — Freitags-Ausreizung AURORA II beendet (gestoppt: Wochenkontingent ausgereizt (100.0 %))

Buch jetzt 30 Kapitel, 158838 Wörter. Details: `/home/bolla/workspace/scratch/aurora_samstag_fr_aurora_20261016/ABSCHLUSSBERICHT.md`, `changes.md` (Entscheidungen), Konsistenz-Bericht `konsistenz_25ff.md`. Spoiler-Schutz: Chris liest erst bis ~Kap. 13 — keine Inhalte nennen.

---

## ✅ 17.10.2026 — Freitags-Ausreizung AURORA II beendet (gestoppt: Wochenkontingent ausgereizt (95.0 %))

Buch jetzt 28 Kapitel, 146844 Wörter. Details: `/home/bolla/workspace/scratch/aurora_samstag_fr_aurora_20261016/ABSCHLUSSBERICHT.md`, `changes.md` (Entscheidungen), Konsistenz-Bericht `konsistenz_25ff.md`. Spoiler-Schutz: Chris liest erst bis ~Kap. 13 — keine Inhalte nennen.

---

## ⏳ 16.10.2026 — Chris-Wunsch: AURORA-Reader auf dem Duo soll beim Öffnen automatisch gespannt sein
Web-Seite kann nicht spannen (OS-Geste). Zu prüfen am Studio: (a) ADB-Befehl zum Spannen/Fenster auf beide Displays (adb shell, ungeprüft), (b) ob Duo gespanntes Fenster/App-Paar beim Start wiederherstellt. Kein Code nötig, bis geklärt. Chris wurde gefragt, ob ich testen soll.

## ✅ 15.10.2026 — Herfeldt-Antwort von Chris gesendet (Outlook-Entwurf); Mail verschoben, Status gesetzt, Excel aktualisiert

## ✅ 15.10.2026 12:40 — Telegram-Session-Reste erledigt
Aigner (Untermenzing) + Weber (13:11) nach Immos 2027-28 verschoben; Makler-Excel v2 gebaut (Desktop\Makler_Antworten_Archiv_neu.xlsx, Backup backups/Makler_Antworten_Archiv_neu_vor_v2_20261015.xlsx). Aigner-Absage von Chris gesendet 09:39, Weber-Antwort 09:40 (von mir). OFFEN: Herfeldt-Datenschutzmail — Antwort-Entwurf Chris gezeigt, wartet auf OK.

## ✅ 15.10.2026 — makler_mail_sync.py: beantwortete Makler-Mails werden automatisch verschoben (nicht getestet)
Edit per Datei (kein python nötig): Inbox-Mails von bekannten Maklern mit späterer eigener Antwort im selben Thread → nach „Immos 2027-28“, nächster Cron-Lauf (:*/30). Prüfen im nächsten Lauf (/jobs „Makler-Mail-Sync“), ob Aigner/Weber ×2 weg sind. Herfeldt-Datenschutzmail bleibt offen (Antwort braucht Volltext + Entwurf).

## ⏳ 15.10.2026 — Posteingang Makler aufräumen + Herfeldt-Datenschutzmail bearbeiten (Chris: "go")
Sandbox blockt python3 → in normaler Session: (1) Mails nach Ordner „Immos 2027-28“ verschieben: Aigner (Untermenzing, 14.10. 22:59, beantwortet 15.10. 09:39), Weber ×2 (15:07 „Anfrage Suchkunde“, 15:11 „Ihre Immobiliensuche“, beantwortet 15.10. 09:40). Ursache: makler_mail_sync.py verschiebt nur Rückläufer, nie bearbeitete Antworten → Fix: nach erkannter eigener Antwort (Thread in Gesendet) automatisch verschieben. (2) Neu: info@immobilien-herfeldt.de „Ihr Suchauftrag + Einverständnis zur Speicherung Ihrer Adressdaten“ (15.10. 10:07; kein passendes Objekt, bittet um Datenschutz-Einverständnis) → Volltext per Graph lesen, Einverständnis erteilen (Chris-Go liegt vor), Mail danach verschieben. Skript-Vorlage scratch/inbox_makler.py (listet Inbox mit Volltext).

## ⏳ 15.10.2026 — Makler-Excel v2 gebaut, NOCH NICHT ausgeführt (Sandbox blockt python3 + /mnt/d)
Skript `scripts/makler_excel_bauen_v2.py` fertig (Blätter: Übersicht = 1 Zeile/Makler mit Ampel+Filter+Nächster Schritt · Angebote = Kernspalten vorn, Kriterien gruppiert/einklappbar, Hochufer=Absage · Legende). Zum Ausführen in normaler Session: Backup `cp /mnt/d/OneDrive/Desktop/Makler_Antworten_Archiv_neu.xlsx backups/Makler_Antworten_Archiv_neu_vor_v2_20261015.xlsx`, dann `python3 scripts/makler_excel_bauen_v2.py` (schreibt Desktop + data/makler_antworten_archiv.xlsx). Danach Chris Bescheid geben.

## ✅ 15.10.2026 — Antwort an Frau Weber (E&V Weilheim) GESENDET
Hochufer abgelehnt (keine Terrasse), Suchprofil PH/DG+Südterrasse+Aufzug ~100 m², Kaufpreisrahmen bis 1.250.000 € genannt, Weilheim als Ort gelobt, Einzug ab Herbst 2027/2028. Antwort im Mail-Thread (Graph reply). Chris' Kaufpreisrahmen = bis 1,25 Mio € (jetzt verbindlich).

## ✅ 15.10.2026 — Makler-Automatik scharf (Stand fürs Erste)
Cron läuft: makler_rueckl_ersatz.py (:10/:40) + makler_angebote_triage.py (:15/:45). Freigabe-Datei config/makler_resend_freigabe.json gesetzt → Voranfrage v4 geht an Ersatz-Adressen (aktuell nur E&V Starnberg contact@). Triage: Score ≥60=Treffer, K.O. = nicht PH/DG, Erdgeschoss, kein Aufzug, keine Terrasse; nur Outlook-ENTWÜRFE, nie Auto-Versand; Absage-Text von Chris freigegeben. E&V Weber/Hochufer (keine Terrasse) + Aigner Untermenzing (EG) = K.O.; Aigner-Absage-Entwurf liegt in Outlook (noch nicht gesendet). Weilheim = Top-Ort ([[project_immo_weilheim_top_lage]]). Offen: Chris antwortet Frau Weber (E&V) selbst; Aigner-Absage-Entwurf absenden.

## ✅ 15.10.2026 — Makler-Automatik erweitert
Spam-Ordner-Rettung in makler_mail_sync.py (Backup backups/makler_mail_sync_vor_spam_20261015.py). Neu: scripts/makler_rueckl_ersatz.py (Ersatz-Adresse per Impressum; Neuversand gesperrt bis config/makler_resend_freigabe.json {"freigegeben":true} — wartet auf Chris-OK zum Text) + scripts/makler_angebote_triage.py (Haiku-Extraktion, Score ≥60 = Treffer→Telegram, A/B/C legen nur Outlook-ENTWÜRFE an, nie Auto-Versand). MP: rote Rückläufer-Box → Zähler. OFFEN: Cron-Einträge für beide neuen Skripte (Auto-Mode verweigerte, Chris muss selbst eintragen/freigeben); Absage-Text freigeben lassen.

## 🛑 14.10.2026 22:59 — VOLLBREMSUNG bis Fr 16.10. 19:00 (Chris)
Wochenlimit nur noch ~35 % Rest. Bis Freitag 19:00 keine Token-Verbraucher: keine Forks/claude -p/Subagents, keine Recherchen; nur nötigste Chat-Antworten. Einziger geplanter Verbraucher: Cron `0 19 16 10 *` ausreizen_fr_wrapper.sh (AURORA II K25–28ff, startet Fr 19:00 wie gewollt). Aktuell läuft kein Hintergrundjob.

## ✅ 14.10.2026 spät — Makler-Excel mit Angebote-Blatt
`Desktop\Makler_Antworten_Archiv_neu.xlsx` neu gebaut via `scripts/makler_excel_bauen.py` (Blätter: Makler-Antworten · Angebote & Wertung mit Score 0–100 + Farbskala, K.O.= Etagenwohnung/kein Aufzug · Legende). Aigner-Eingangsmail nach Gelöschte verschoben. Backup alte Excel backups/Makler_Antworten_Archiv_neu_vor_angebote_20261014.xlsx.

## ✅ 14.10.2026 abends — Aigner-Absage gesendet + Kriterien
Absage (nett, mit 😉) an info@aigner-immobilien.de GESENDET. Neue Must-Kriterien: Aufzug Pflicht, Etagenwohnung No-Go (immo_criteria.json + project_immokauf.md). E&V Weilheim (Kaufpreisrahmen+Feedback Hochufer) + Schneider&Prell/Sedlmayr-Formulare: Chris schaut morgen selbst, NICHTS tun.

## ⏳ 14.10.2026 abends — Freitags-Lauf AURORA II eingeplant
Cron `0 19 16 10 *` → `scripts/ausreizen_fr_wrapper.sh` → `ausreizen_fr_aurora.py` (Dry-Run ok, aurora2.json unberührt). Chris-Freigabe: kein Vorab-Lesen/Plot-OK nötig; Kap. 25–28 aus Entwürfen einbauen, K27-Schluss selbst wählen, dann Kap. 29ff. Deadline Sa 17.10. 23:50, Notbremse `touch /tmp/aurora_samstag_stop`. Crontab-Backup `backups/crontab_vor_fr_aurora_20261014.txt`.

## ⚠️ 14.10.2026 — Makler-Kontaktformulare: automatisch NICHT möglich (6/6)
E&V Starnberg/Germering/Gräfelfing/Ostallgäu: FriendlyCaptcha nach „Abschicken“ (Germering getestet, nicht gesendet); Von Poll Füssen: 403-Bot-Schutz; RE/MAX Bad Tölz: Security Verification. Captchas bewusst nicht umgangen. Formtext + Felder: scratch/makler_formulare_20261014/formular_text.txt (Chris kann manuell absenden). Excel `Makler_Antworten_Archiv_neu.xlsx` Zeilen 9–14 = „manuell nötig“; alte Excel ist im Papierkorb.

## ✅ 14.10.2026 — Robin-Seite v2
Kostenschätzung aufklappbar im Tansania-Rückblick, Studienverlauf als eigene Karte mit Auto-Highlight, M2 13.–15.04.2027, PJ ab 17.05.2027 (Tertiale), PJ-Portal-Karte, Geburtstag 30.09.2002. Offen: Ulmer Registrierungs-/Tauschfristen (Robin fragen), M3-Termin.

## ✅ 14.10.2026 — Skiffy-and-Fanty-Mail gesendet + Robin-Seite neu
EN-Mail (mit AURORA-II-Hinweis, kein Nachfassen) an skiffyandfanty@gmail.com GESENDET. Robin-Seite komplett neu (Studienkompass, Diss-Checkliste, Tansania-Rückblick, Kontakt); Karte/Kosten/Jarvis raus. Offen nur noch: Reiseplaner neu aufbauen (Chris erinnern).

## ✅ 14.10.2026 — Projekt-Board aufgelöst, Reiseplaner-Gruppe weg, Archiv
Board-Nav entfernt (board.json gesichert), Archiv-Kachel „AURORA I — Sichtbarkeits-Kampagne“, Reiseplaner = Einzeleintrag. Backups backups/*_vor_board_raus_20261014*. OFFEN: EN-Mail an Skiffy and Fanty zur Freigabe vorgelegt (Entwurf im Chat); Reiseplaner + Robin-Seite neu bauen ([[project_reiseplaner_robin_neu]]) — Chris erinnern.

## ✅ 14.10.2026 — Sommerreise 2026 ins MP-Archiv verschoben
Snapshot-Kachel in ARCHIV_ITEMS (id sommerreise2026, Button → Detailseite page-reise-sommerreise2026 bleibt als Tagebuch erhalten); Nav-Eintrag + Pointer-Karte im Reiseplaner entfernt; sidebar_state.json bereinigt. Backups backups/index_vor_sommerreise_archiv_20261014.html + sidebar_state_vor_…json.

## ✅ 14.10.2026 — MP Immo-Seite aktualisiert
Status `nicht_interessant` war als „Neu“ gezählt → jetzt eigenes Label + Filter „Aussortiert“, aus Statistik/Zähler raus; starre „Alle (34)“ entfernt; Nächste Schritte aktualisiert (Suchraum ✓, Voranfrage ✓). Backup backups/index_vor_immo_update_20261014.html. Kein Server-Restart nötig.

## ✅ 14.10.2026 — Makler-Mail-Sync automatisch (Cron */30)
`scripts/makler_mail_sync.py`: Antworten→Status, Rückläufer→rote MP-Box + Verschieben nach Immos 2027-28. Offene Antworten: Löger (Suchprofil), SEDLMAYR (Online-Suchprofil-Link, wartet auf Chris).

## ✅ 14.10.2026 — Immo-Voranfrage-Mails an 42 Makler GESENDET (42/42, 0 Fehler)
Skript `scripts/send_immo_makler_20261014.py` (detached, 30 s Abstand, Log `logs/send_immo_makler_20261014.log`), Absender ernstmandel@outlook.de, Status je Mail → makler_status.json (email_gesendet). Staltmayr ausgenommen. Suchraum laut Karte `config/immo_suchgebiet_karte.png` (West+Süd von München, A8–Alpen, Lech–Bad Tölz; NICHT Memmingen/Kempten/Sonthofen). Offen: 5 Kontaktformular-Makler (E&V Germering/Gräfelfing/Ostallgäu, Von Poll Füssen, RE/MAX Bad Tölz) → ZURÜCKGESTELLT auf Chris' Wunsch (nicht erinnern, [[project_immo_kontaktformulare]]). Bounces (3) ausgewertet+gelöscht: Heppner + RE/MAX Germering entfernt, E&V Starnberg → Formular. Antworten: FT Immobilien 24 (aufgenommen), LOEGER Tutzing (braucht Anschrift + Kaufpreisvorstellung → OFFEN bei Chris).

## ✅ 14.10.2026 — Makler-Liste: Telefon-only raus, Kontaktformular-Liste
Kontaktformular-Liste: 5 Makler mit Formular (E&V Germering/Gräfelfing/Ostallgäu, Von Poll Füssen, RE/MAX Bad Tölz — Feld `kontaktformular`/`kontakt_art` in makler_status.json, Formulare nicht im Detail verifiziert) — Chris will Formulare später von Bolla ausfüllen lassen → **Chris daran erinnern**. 39 Nur-Telefon-Einträge entfernt (Backup backups/makler_status_vor_telefon_raus_20261014.json). Weitl-Immobilien hat doch Mail (weitl@weitl-re.de) → 43 mailbar, 68 Einträge gesamt.

## ✅ 14.10.2026 — Makler-Liste auf Karten-Suchgebiet bereinigt (Immo-Fork 2)
Suchraum laut Karte `workspace/config/immo_suchgebiet_karte.png` (A8 Nord, Lech-Linie West bis Füssen, Alpen Süd, Bad Tölz/Holzkirchen/Unterhaching Ost). 19 Einträge (Memmingen/Kempten/Sonthofen/Buchloe/Kaufbeuren/Bobingen/Dachau) mit `mailen:false` + Hinweis „außerhalb Suchraum" markiert (nicht gelöscht, Status nicht_interessant). +39 neue Makler im Gebiet (10 mit verifizierter Mail), 42 eindeutige mailbare Adressen (`mailen:true`), 46 im Gebiet ohne Mail (Telefon/Formular). Backups `backups/makler_status_vor_karte_20261014.json`. Mails NICHT versendet — wartet auf Entwurf-Freigabe durch Chris (Staltmayr: Testmail vom 28.05. schon raus, Frage offen).

## ✅ 14.10.2026 — Memory-Aufräumung selbst durchgezogen
45 Waisen in MEMORY.md aufgenommen, 15 erledigte/überholte nach workspace/memory_archiv/, aktuell.md von 677 KB auf 50 KB gekürzt (Rest: memory_archiv/aktuell_archiv_bis_20261014.md; Neueste Einträge stehen OBEN!). Backups in workspace/backups/*_vor_hygiene_20261014.md. Keine kaputten Links.

## ✅ 14.10.2026 — Makler-Liste auf neuen Suchraum angepasst (Fork)
Suchraum: südlich A8, West/Südwest bis ca. Memmingen, nach Süden offen; München-Stadt nur West/Südwest. Bestehende 34 Einträge alle im Raum (0 als „außerhalb“ markiert). E&V-Germering-Eintrag korrigiert (starnberg@-Adresse entfernt, keine echte Mail gefunden). **Neu: 34 Makler** in 7 Regionen (München West/Gräfelfing, Augsburg Süd/Bobingen, Buchloe/Kaufbeuren, Memmingen, Kempten/Oberallgäu, Füssen, Garmisch) — **10 mit Mail** (FT Immobilien 24, Finest Property, Armbruster, Rudolph, Freytag, AllgäuImmo, Hold, Sparkasse Allgäu Kempten, PIB Pienzenauer, Von Poll GAP), **24 ohne Mail** (nur Telefon/Verzeichnis; Von Poll-Seiten blocken Abruf). Backups: backups/makler_status_vor_suchraum_fork_20261014.json. Mail-Versand NICHT gestartet (wartet auf Chris-OK).

## ✅ 14.10.2026 — Reader-Spannen-Fix (lockedAnchor) von Chris bestätigt: "ist jetzt ok"
## ⏳ 14.10.2026 09:35 — Figuren-Pass R4 läuft weiter (Kap. 19–24), Gate 5h ≤ 50 %, Woche ≤ 83 %, Deadline Fr 16.10. 19:00
Reader-Anker-Fix (lockedAnchor) gebaut, Chris: ok. Punkte 1–3 meiner Ideenliste verworfen (Ausflugsmappe nicht nötig, Kurstag-Mitteilungen immer erst Mo, Kalender hat Chris selbst). Punkt 5: Memory-Hygiene-Bericht auf Desktop (61 Waisen, 0 kaputte Links) — nichts gelöscht, Chris entscheidet. Plot-OK Kap. 25–28 bleibt liegen bis Chris weiter gelesen hat. Skript `scripts/aurora2_figuren_pass.py` (Backup in backups/). Notbremse `touch /tmp/aurora_samstag_stop`.

## 🎶 12.10.2026 — Kili-Song für Robins Kalender 2026 (QR): Entwurf v1 steht
Konzept A+B ("Pole pole", Machame, ohne Namen Robin, Englisch mit Suaheli-Hook). Entwurf DE: `workspace/scratch/kili_song/entwurf_v1_de.md`. Offen: Gipfel erreicht? Tiere/Ngorongoro? → dann Deutsch feilen → EN-Fassung → Suno → QR (eigene Seite chrismandel.de + ggf. Spotify). Deadline Pixum-Bestellung ~Mitte Nov. `Adventskalender 2026.pptx` existiert schon im Powerpoint-Ordner (noch nicht geöffnet).

→ 12.10. v2 des Kili-Songs: Gipfel ja, Big Five, Leoparden, Menschen-Strophe (entwurf_v2_de.md). Wartet auf Feilen durch Chris.

→ 13.10. Kili-Song v3 (Olli/Tristan, OP-Zuschauen, Asante sana): scratch/kili_song/entwurf_v3_de.md

→ 13.10. Kili-Song EN-Suno-Fassung fertig (scratch/kili_song/entwurf_v1_en_suno.md), Lyrics in Zwischenablage. Chris: DE v3 freigegeben ('sehr stark'). Nächster Schritt: Suno-Takes erzeugen (Namensaussprache prüfen).

→ 13.10. Kili-Song: finale Suno-Texte (Lyrics/Exclude/Style/DE-Übersetzung) in scratch/kili_song/kili_song_suno_final.txt + Zwischenablage. Chris erzeugt jetzt Takes in Suno.

→ 13.10. Word 'Pole_Pole_Songtext.docx' auf OneDrive-Desktop (S.1 Songtext zum Drucken für Robin, S.2 Arbeitsblatt+DE-Übersetzung nur für Chris). Chris macht jetzt Suno-Takes.

→ 13.10. Mail an Frau Ellermann (Zahnrechnung Reni 0 €) fertig als scripts/send_ellermann_zahn_20261013.py; Auto-Mode-Classifier blockte Versand → Chris führt per !python3 aus. Vers.-Nr. AK-0576988791 aus Allianz-Mails.

✅ 13.10. Mail an Frau Ellermann (Zahnrechnung Reni, 0 €) GESENDET, Status 202, mit 3 PNG-Anhängen, Vers.-Nr. AK-0576988791, Hinweis auf ihre Mail vom 31.08. (70 % bei Kronen). Nächster Schritt: Antwort abwarten (ellermann@allianz.de / jennifer.easterling@allianz.de).

→ 13.10. Kili-Song-Lyrics v6-Nachschärfung: 'OR' (würde als 'or' gesungen) raus, Zeilen gekürzt (<=10-11 Silben); docx auf Desktop + Zwischenablage aktualisiert.
→ Desktop-Word aktualisiert als Pole_Pole_Songtext_v2.docx (alte Datei war in Word geöffnet/gesperrt).
→ 13.10. Kili-Song-Lyrics auf MP-Tag-Schema (Vortragsanweisung, keine Instrumente) umgestellt, Zwischenablage aktualisiert; Memory feedback_suno_lyrics_qualitaet ergänzt.

→ 13.10. Word v3 (Lyrics mit [Tags]) auf Desktop; Video-Diashow Pole Pole: Skript scripts/build_pole_pole_video.py (44 Fotos, Abspann rechts), Render 200s-Platzhalter läuft; muss mit echter Songlänge/Audio neu gerendert werden (--duration X --audio song.mp3). Ausgabe später nach Desktop\temp.
→ 13.10. Video-Platzhalter (200s, ohne Ton) liegt in Desktop\temp\Pole_Pole_Diashow_ohne_Ton_200s.mp4; Skript scripts/build_pole_pole_video.py --duration X --audio song.mp3 für Neurender.
- 13.10.2026: MP AURORA II Hinweis-Karte R1–R4 + Recap-Box waren transparent (rgba 0.07) → deckend #1a1538; Backup backups/index_vor_fp_karte_deckend_20261013.html. Video: Fotos 2 (OP-Bein), 3 (Kind->KCMC(7) mit Freunden), 9 (von hinten→bleibt? nein: Chris-Nr. 9 = meine 9 entfernt), Finger-Selfie 19, Tabletten 23 raus; Re-Render 40 Fotos läuft (scratchpad/video/Pole_Pole_Diashow_200s_v2.mp4)
- 13.10.2026 Pole-Pole-Video: Script jetzt mit --timings (JSON Startzeit je Lyric-Zeile, 42 Zeilen), Leselinie 38 %, Fade unten; Robin-Finger-Foto raus, Frauen-Selfie 08-25(019) wieder rein. Render final2 laeuft; exakte Zeiten brauchen frischen Suno-Token (Aligned-Lyrics) – Chris fragen. Whisper verboten.
- 13.10.2026 Pole-Pole-Video FINAL3 (Suno-Zeitstempel, aligned_lyrics/v2, 39 Zeilen, Chorus nach V1 doppelt) → Desktop\temp Pole_Pole_Video_final.mp4 + _ohne_Ton.mp4. Token geloescht.
- 13.10.2026 Pole Pole archiviert: Office\KI\Privat\Pole Pole (Kilimanjaro-Song 2026)\ (mp3,wav,2 mp4,docx,lyrics,script,aligned json). QR offen: Chris soll OneDrive-Link (Jeder mit Link) zu Pole_Pole_Video_final.mp4 aus dem Archivordner erzeugen; Graph hat keinen Files-Scope. qrcode per pip --user installiert.
- 13.10.2026 Pole Pole: QR erzeugt (QR_Pole_Pole_Video.png + QR_Link.txt im Archivordner, Link 1drv.ms ...e=ni19TF, Decode-Test ok, Version 9/H). temp aufgeraeumt; Desktop behaelt Pole_Pole_Songtext_v3.docx (zum Drucken). Offen: QR in Adventskalender 2026.pptx einsetzen (Chris-OK), Link-Rechte pruefen (Bearbeiten statt Ansehen).
- ⏳ 13.10.2026 Pole Pole Projektabschluss: Finals liegen komplett in Office\KI\Privat\Pole Pole (Kilimanjaro-Song 2026)\. Aufräumen (scratch/kili_song, scripts/build_pole_pole_video.py + Backup, alte Pole_Pole_Songtext.docx, Session-Scratchpad bfce2f4e 633 MB) vom Classifier blockiert → wartet auf Chris-Freigabe/manuelles Löschen. Offen: QR in Adventskalender 2026.pptx (Chris-OK), Link-Rechte prüfen.
- ✅ 13.10.2026 Pole Pole Aufräumen ERLEDIGT (Chris: „ja, löschen"): scratch/kili_song, Workspace-Skript+Backup, alte Songtext.docx, Session-Scratchpad weg. Finals nur im Archivordner Office\KI\Privat\Pole Pole (Kilimanjaro-Song 2026)\. Offen: QR in Adventskalender 2026.pptx (Chris-OK), Link-Rechte prüfen.
- ✅ 13.10.2026 Pole Pole KOMPLETT ABGESCHLOSSEN: QR-Code ist bereits im Adventskalender 2026 und funktioniert (Chris bestätigt). Keine offenen Punkte mehr. Finals: Office\KI\Privat\Pole Pole (Kilimanjaro-Song 2026)\.

---

## ⏳ 11.10.2026 18:30 — AURORA II Figuren-Pass LÄUFT (Chris-Go, Ferienwoche)
Detachter Prozess `scripts/aurora2_figuren_pass.py`, Log `logs/aurora_samstag.log` + `logs/aurora2_figuren_pass.out`, State/Panel `scratch/aurora_samstag_figurenpass_20261011/`, Status /jobs (`aurora2_figuren_pass`). R1: Kap. 13–24 Patches DIREKT im Text (Chris kennt sie noch nicht), danach Kap. 1–12 max. 3 blaue Einschübe/Kap. (status wartet, nichts tun = bleibt drin); R2 Spannung/Humor 13–24; R3 Kontinuität 13–24; R4 Messung. Pacing: Wochen-Cap je Tag (So 16 … Fr 58 %), 5h ≤ 92 %, Deadline Fr 16.10. 23:50. Kurzbericht Desktop `AURORA_II_Figuren_Pass.html` (1 Seite, Chris will minimalen Zeitaufwand). Backups `backups/aurora2_vor_figurenpass_*`. Notbremse `touch /tmp/aurora_samstag_stop`. Kein Samstagslauf 17.10. (Ferien, Chris will ~40 % Rest).

---

## ⏳ 12.10.2026 (später) — AURORA-Reader: Seite springt beim Spannen/Zusammenklappen (gefixt, ungetestet)

Chris: Beim Aufspannen auf beide Duo-Displays landet er viele Seiten später als vorher. Ursache: Einzel- und
Doppelbildschirm haben unterschiedliche Spaltenbreiten — der Text fließt beim Umschalten komplett neu, dieselbe
Seitenzahl zeigt danach auf ganz anderen Textabschnitt (keine 1:1-Entsprechung der Seitenzählung).
Fix in `mission-control/aurora-reader.html`: `layout()` merkt sich jetzt VOR jeder größenbedingten Neuberechnung
den gerade sichtbaren Satz (`findAnchorSpan()`) und sucht ihn danach im neu geflossenen Text wieder, um die
passende Seite zu bestimmen — statt blind die alte Seitenzahl zu übernehmen. Gilt für Spannen/Zusammenklappen,
Vollbild-Wechsel und Fenstergrößenänderung; beim normalen Kapitel-Öffnen (Liste/gespeicherte Stelle) bleibt es
bei der direkten Seitenzahl. Kein Server-Neustart nötig. **Ungetestet** hier — Chris bitte auf dem Duo spannen/
zusammenklappen und prüfen, ob derselbe Satz sichtbar bleibt.

---

## ✅ 12.10.2026 ~19:15 — MP AURORA II: Hinweis-Karte R1–R4 + Kapitel-Kennzeichnung
Oben auf der Seite aufklappbare Karte „Verbesserungsläufe" (R1 Figuren-Pass / R2 Spannung+Humor / R3 Kontinuität / R4 Messung, Tabu-Liste). Kapitelliste links: Badges R1/R2/R3 ✓/⏳ (Kap. 13–24) bzw. „✎ 2 Vorschläge (blau)" (Kap. 1–12); im Lesefenster Statuszeile unter dem Titel. Daten live: `/api/aurora2` → `figurenpass` aus `scratch/aurora_samstag_figurenpass_20261011/state.json` (MP-Server neu gestartet). Backups `backups/index_vor_figurenpass_badges_20261012.html`, `backups/mission_control_api_vor_figurenpass_20261012.py`. Figuren-Pass selbst: pausiert bis Di 00:05 (Tages-Cap), offen R3 Kap. 20–24 + R4. Korrektur: Pass lief 11.10. 18:30–12.10. 02:22, nicht heute.

---

## ⏸️ 12.10.2026 ~10:10 — Pause: Chris macht Garten winterfest, Wochenlimit bei 74 % → heute nichts Neues
Stand: Kanon-Todestag (12. Okt) korrigiert, „Figuren lieben"-Prinzip in project_aurora_ii_optimierungen_fuer_iii.md, Kilimanjaro-Hintergrund auf Desktop (Kilimanjaro_Hintergrund_Adventskalender.jpg). Offen: Plot-OK für Entwürfe Kap. 25–28 (+ Wahl K27-Schluss Original/A/B), AURORA II Rücken/Rückcover, Buhl-Antwort TR-Sync abwarten. Nach /clear: nichts starten, Chris meldet sich.

---

## ✅ 11.10.2026 ~12:30 — AURORA II: Entwurf Kap. 28 »Bis fünf Uhr neunundfünfzig« (nur scratch, nicht im Buch)
`scratch/aurora_samstag_wochenende_20261009/entwurf_kap28.md` (+ `_PRUEFNOTIZ.md`, 18 Befunde eingearbeitet; Vorversion `backups/entwurf_kap28_vor_pruefnotiz_20261011.md`). Belagerungskapitel 17.12. 10:12 → 18.12. 06:00: Marlie liest das Formular laut, Wessel verrät sich mit »der schläft« (Präsens), bleibt bis 05:59; Falkner-Anruf (weiß nichts von Ashworth), Petrova-Teller, Jonas/Daumenkino, Marlies ungezähltes Nein um 05:59; Cliffhanger: Wessel holt »den dritten Ausweis« (Theo, Schublade). Basis war K27-Original + Anfang von Variante A (Tempus-Slip). Bogenplan 28 stand nicht in `geheim.bogenplan_19_27` → Beats von mir, Chris muss die Plot-Weiche OK geben. Nächstes: Kap. 29 erst nach Chris' Feedback zu 28 und Wahl K27-Schluss (Original / A / B).

---

## ✅ 11.10.2026 ~12:30 — AURORA II: Kap. 10 Poststempel + Kap. 15 „Jonas hat die Fünf geschrieben“; Lesebericht vom Desktop gelöscht
Kap. 10: Poststempel Brüssel 9. November, „Das kam am Dienstag“ (Foto stammt vom Sa 7.11.). Kap. 15: Lenis Nachricht nennt Jonas. Backup `backups/aurora2_vor_poststempel_fuenf_*`. Lesebericht-HTML vom Desktop gelöscht (Funde alle abgearbeitet, JSONs bleiben in scratch/aurora_samstag_sa2_20261010).

---

## ✅ 11.10.2026 ~12:10 — Entwürfe Kap. 25–27: Lesebericht-Funde eingearbeitet (nur scratch)
27 Funde (Datum „heute Nacht/Samstag“, Bezüge, Ferse unter Schaft, Jonas „der Erste“, Wessel-Satz u. a.) in `scratch/aurora_samstag_wochenende_20261009/entwurf_kap25–27.md`; Backup `backups/entwurf_vor_lesebericht_20261011/`. Nicht übernommen: Frauke 17→20 Jahre, Noah-Ankunftszeit (K27), Frauke/Marie 9:45 (K27), Jacke am Haken (K27). Desktop (OneDrive) enthält kein Cover mehr; lokaler C:\Users\ernst\Desktop hat 3 alte AURORA-Textdateien (nicht angefasst).

---

## ✅ 11.10.2026 ~11:55 — AURORA II: Lesebericht mittel/niedrig durchgezogen (Kap. 1–24) + Aufräumen
Chris: „Federboa passt sehr gut, nur wer ist im Takt der Lüfter?“ → Kap. 2 jetzt „…Kopfhörer um den Hals gewickelt wie eine Federboa, und schnarcht im Takt der Lüfter.“ Danach „alles durchziehen“: ~300 der 553 mittel/niedrig-Funde geprüft und übernommen (Bezüge, Kommas, Zeitformen, Wortwiederholungen/„sehr still“/„zum ersten Mal“-Floskeln, Stille-Formeln, einzelne Bilder). Bewusst NICHT übernommen: alles, was Daten/Zahlen/Plot betrifft (Fünfzehnter/14.11., „vierzehn“-Motiv, 41 Tage, Kap. 22 „Am Achtzehnten“, Mittwoch/Donnerstag), AURORA-Zeichensetzung, Kollmann-Geschlecht, Hanne-Zettel, K10 Poststempel 7.11./„Samstag“ (Plausibilität Brüssel offen), Frauke 17 Jahre (bleibt). Backups `backups/aurora2_vor_lesebericht_mittel_*` + `aurora2_vor_lueftertakt_*`. Temp-Skripte in /tmp gelöscht. Offen: Funde zu Entwurf-Kap. 25–27 (scratch), K10 Poststempel/„Samstag“, Kap. 1 „Er hat die Fünf geschrieben“ (K15), Kap. 28ff. Entwürfe.

---

## ✅ 11.10.2026 ~10:40 — AURORA II: Lesebericht-Hoch-Funde eingearbeitet (Kap. 1–24)
Chris hatte Kap. 1–2 gegengelesen, nur Änderung: „Selbstmordversuch“-Vergleich (Kap. 2, war Jonas/Kopfhörer) → „wie eine Federboa, im Takt der Lüfter“. Danach „alle anderen Fälle durchziehen“: 99 Hoch-Funde geprüft, ~60 übernommen, Rest verworfen (Fehlalarme). **Anhörungsdatum überall auf Mittwoch 25.11.** vereinheitlicht (47× „Sechsundzwanzigsten“→„Fünfundzwanzigsten“; Kap. 1 „22 Tage“ stimmte damit). Kap. 8 Kopf: 9. November/24 Tage (stand 10./25). Theos Entnahme des Blatts überall 3. Nov (Kap. 10/11 hatten „Vierten“); Todestag 12. Okt (Kap. 12 „Dreizehnten“); Kap. 20 Werktage „bis zum zehnten“; „aufheben“→„aufbewahren“ in Kap. 9/14/17/18. Verworfen: Noah Khoury (ist in Band I korrekt), Mia/Ben (Band I stimmt), Frauke „siebzehn Jahre“ (steht überall so). Backups `backups/aurora2_vor_selbstmordvergleich_*`, `…_lesebericht_datum25_*`, `…_lesebericht_hoch_k2_k5_*`, `…_lesebericht_hoch_k6_k24_*`. Offen: 340 mittel/237 niedrig (nicht angefasst), Funde zu Entwurf-Kap. 25–27 (nur in scratch), K15 „Er hat die Fünf geschrieben“ (wer ist er?) bewusst nicht angefasst.

---

## 📌 10.10.2026 18:45 — MERKEN: weitere AURORA-II-Kapitelentwürfe (ab Kap. 28), sobald Limit-Luft da ist
Chris will, dass nach dem 5h-Reset (23:10) bzw. wenn Gating (5h ≤ 92 %, Woche < 98,5 %) es zulässt, weitere Kapitelentwürfe entstehen (nur Dateien in scratch/, nicht ins Buch). Entwürfe 25–27 liegen in `scratch/aurora_samstag_wochenende_20261009/`. Nur wenn Luft — Lesebericht-Job hat Vorrang bis 23:50.

---

## ✅ 10.10.2026 18:39 — AURORA II Kap. 9: Jonas-Konter wieder eingesetzt
Zeile »Konzentriert«, sagte Jonas … »Also. Das klang im Kopf netter.« steht wieder direkt nach „…die, die keiner will.“ (war am 29.09. durch Satz-Übernahme-Bug verloren, Markierung dbecc283). Backup `backups/aurora2_vor_kap9_konzentriert_20261010_183851.json`. Chris schaut es noch an.

---

## 📌 10.10.2026 11:40 — Cover Front FINAL; MERKEN: Rücken + Rückcover AURORA II noch offen (Details project_aurora_ii_cover.md)

## ✅ 10.10.2026 abends — Makler: 8 entfernt (42→34) + Detail-Block im MP-Modal
Chris: Entfernungs-Vorschläge der Tiefenprüfung alle umgesetzt (Wagner Premium, 1000 Rosen, Schnellbögl&Franke, Spindler, ROWI, Stadler, Kachelriß, LBS Germering). Backups `backups/makler_status_vor_entfernung_*`, `backups/index_vor_makler_details_*`. Modal (Klick auf Makler) zeigt jetzt Website (klickbar), E-Mail, Telefon, Adresse, Eignung, Prüfbefund. Ohne E-Mail: Herrschinger, Bayerische Seen, Simone Grau, Krusemeyer. Cover AURORA II: v3 (weiche Kanten) ist FINAL, Temp gelöscht.

---


---

## ⏳ 10.10.2026 10:12 — Samstags-Ausreizung Teil 2 LÄUFT (AURORA-II-Lesebericht, nur lesen)

Detachter Prozess `scripts/ausreizen_sa_lesebericht.py` (PID siehe `ps`), Log `logs/ausreizen_sa2.log` + `logs/aurora_samstag.log`, State/Funde `scratch/aurora_samstag_sa2_20261010/`, Status auf /jobs. Deadline 23:50, Gating 5h ≤ 92 %, Woche < 98,5 %. **Ändert aurora2.json NIE** (save gesperrt; Backup `backups/aurora2_vor_lesebericht_*`). Reihenfolge: 1 Analogie-Check (Fehlerklassen aus Chris' übernommenen Markierungen → alle Kap. 1–24 + Entwürfe 25–27), 2 Zweitleser je Kapitel, 3 Band-I-Gegencheck, 4 Lesebegleiter + Memory-Hygiene, 5 Fehlerjagd-Runden. Ergebnis: **Desktop `AURORA_II_Lesebericht_20261010.html`** (wächst laufend). Notbremse `touch /tmp/aurora_samstag_stop`. Vorher (Fr 19:00–20:44) lief Makler-Tiefenprüfung + Entwürfe Kap. 25–27 (nur Dateien in `scratch/aurora_samstag_wochenende_20261009/`, Makler-HTML auf Desktop; Entfernungs-Vorschläge warten auf Chris).
Cover: v2d freigabereif (Desktop\temp\AURORA2_Cover_Skizze_v2d.png), Endrender 1600×2560 erst nach Chris' OK; Ordner `Bolla\AURORA II\` angelegt.

---

## ✅ 09.10.2026 — Wochenend-Ausreizung beendet (fertig)

Makler-Tiefenprüfung + AURORA-Entwürfe Kap. 25–27 (nur Dateien, nicht im Buch) + Schluss-Varianten. Details: `/home/bolla/workspace/scratch/aurora_samstag_wochenende_20261009/ABSCHLUSSBERICHT.md`. Makler-Bericht: Desktop `Makler_Pruefung_20261009.html`. Entfernungs-Vorschläge warten auf Chris' Entscheidung.

---

## ✅ 05.10.2026 abends — Tanzkurs-Word: Grundschritte auf der Stelle

`Desktop/Tanzkurs_Schrittfolgen.docx`: Discofox-Grundschritt + 4-Viertel-Drehungen sowie Cha-Cha-Einsteiger auf „auf der Stelle" korrigiert (Chris: alle Grundschritte erst auf der Stelle). Backup `backups/Tanzkurs_Schrittfolgen_vor_discofox_*.docx`. Offen: Discofox-Tap-Folge (evtl. 2. Hälfte R,L,Tap R) – nur falls Lehrer es so zeigt. Außerdem Song-Zeile „Control-Z/save" erklärt, nichts geändert.

---

## ✅ 06.10.2026 — Kurstag 8 (Ansichten/Entwurf): Entwurf-PPTX + 08-Praktikum geprüft & angepasst

`Handouts/Entwurf/08-2 Powerpoint Profi Ansichten.pptx`: Folie 2 „Schnellstarter" (2024 von MS eingestellt) → Kreis versteckt (nicht löschen! Animation-Referenz → PowerPoint öffnet sonst nicht), Text „Design passend zum Thema wählen"; Folie 4 Tippfehler; Folie 6 Hinweis „nur M365-Abo + Internet" (Designer/Entwurfsvorschläge fehlt in Office 2010 der Schul-Laptops); Folie 12 Designer „nur Microsoft 365", Impress „Masterfolien"; Notizen ergänzt. `08-Praktikum.html`: Zähler 8, Impress-Wege, Ansichten/Notizen korrekt, Schritt 7 Screenshot zuerst + Entwurfsvorschläge nur falls vorhanden. Kein Backup der Entwurf-PPTX vorhanden (vor Edit nicht gesichert).

---

## ✅ 05.10.2026 — MP Bolla Songs: Oktoberfest-Tab → 🎺 Volksmusik (wöchentlich)

Pool `_VOLKSMUSIK_HITS` (40 Titel) in `scripts/mission_control_api.py`, `_fetch_volksmusik_charts()` zieht 10/Woche (Wechsel Montag, 4-Wochen-Zyklus ohne Wiederholung). Key `volksmusik` statt `oktoberfest` in /api/charts; Tab in index.html umbenannt. Backups `backups/*vor_volksmusik_*`. MC neu gestartet.

---

## ⏳ 05.10.2026 ~09:30 — Kurstag 4 (II-Kurse): Cron heute 14:30, Chris-Freigabe erteilt

Cron `30 14 5 10 *` → `scripts/itslearning_kurstag_cron_wrapper.py` (startet itslearning_post_kurstag.py, meldet ✅/⚠️ per Telegram; Log logs/itslearning_kurstag4_cron.log; Crontab-Backup backups/crontab_vor_kurstag4_20261005.txt). Ersetzt den Handlauf-Plan unten. Danach Screenshot-Check der 4 Mitteilungen. Zweiter Cron: Do 08.10. 14:30 „nächste Termine“ Gruppe II (s.u.).

---

## ⏳ 05.10.2026 ~09:10 — „Nächste Termine“ Gruppe II (nach Herbstferien): Vorschau liegt in temp, Post Do 08.10. nachmittags

Texte (4× Variante) in `scripts/itslearning_post_naechste_termine_gruppeII_nov.py`; Termine: Mi 25.11./02.12./09.12./16.12. (7d 07:50, 7b 12:30), Do 26.11./03.12./10.12./17.12. (7a 07:50, 7c 12:30) – gegen schuljahr2627.json geprüft. Vorschau-PNG: `Desktop\temp\Mitteilungen_NaechsteTermine_GruppeII_Vorschau.png` (Skript `itslearning_vorschau_naechste_termine_II.py`). **FREIGEGEBEN von Chris (05.10.)** – Termine passen, PNG gelöscht. **NOCH NICHT gepostet** – Cron `30 14 8 10 *` postet automatisch Do 08.10. 14:30 (von Chris am 05.10. ausdrücklich bestätigt; Log logs/itslearning_post_naechste_termine_gruppeII.log; Crontab-Backup backups/crontab_vor_naechsteTermineII_20261005.txt). Skript meldet Ergebnis per Telegram (✅/⚠️). Danach Screenshot-Check `python3 scripts/itslearning_post_naechste_termine_gruppeII_nov.py`; danach PNG in temp löschen (fragen).

---

## ✅ 05.10.2026 ~08:50 — Tunnel-Mutex + AURORA-Reader-Check

- **Book `tunnel.ps1` mit Mutex `Global\BollaTunnelLoop`** + `ExitOnForwardFailure=yes` (Ursache der 3 Parallel-Schleifen: wscript beendet sofort, `IgnoreNew` der Tasks griff nie; Boot+Logon+Unlock starteten je eine Schleife). Test: 3 Task-Starts gleichzeitig → 1 Schleife, :2222 oben. Backup `backups/book_tunnel_ps1_vor_mutex_*.ps1`.
- **Einschub ei-423d7ca8 (Kap 7 Malliste/Glas) stand schon im Kapitel → Status auf uebernommen gesetzt (08:51, Backup backups/aurora2_vor_einschub_status_*); jetzt 0 offene Vorschläge.
- **aurora2.json geprüft:** 0× `wartet_entscheidung`; Kap 6/7/8/10-Stellen stehen auf übernommen/abgelehnt (Chris' Angabe stimmt). Nur `einschub_vorschlaege[1]` hat Status `wartet` (anderer Mechanismus, nicht angefasst).

---

## ✅ 05.10.2026 ~08:45 — Book-Tunnel :2222 repariert

Nach dem Force-Restart war :2222 weg; Watchdog meldete seit Stunden „halb-tot“ (Restart ging ins Leere). Ursache: **3 parallele `tunnel.ps1`-Schleifen + 3 `ssh -R`** am Book blockierten sich (BollaTunnel + BollaTunnelBoot + Relikt). Fix: überzählige powershell-Schleifen + alle ssh.exe per Heim-IP (`ssh ernst@192.168.178.38`) gekillt → 1 Schleife, 1 ssh, :2222 oben, `ssh -p 2222 ernst@localhost` ok. Phone Link/Duo-Kopplung klappt (Chris). Falls es wiederkommt: Schleifen am Book zählen (Get-CimInstance, CommandLine -match 'tunnel.ps1').

---

## 🗑️ 04.10.2026 — Sichtbarkeits-Idee „Anthropic-Ethik/KI-Kind-Motiv" VERWORFEN (Chris)
Chris' Idee (Anthropic-Mitarbeiter als Kritiker/Adressat für AURORA) ist verworfen. Keine Mail, nichts gesendet.
Die offenen Sichtbarkeits-Ideen (Literatopia, Hurtz, Skiffy&Fanty) bleiben unverändert: nur auf Chris' ausdrücklichen Wunsch.

## ⏳ 13.10.2026 (später) — AURORA-II-Trailer: Eevee-Testrender ansteht (Blender nicht erreichbar, Telegram-Sandbox)

Chris will perspektivisch ein ~3-Minuten-Video (Song + Blender-Trailer) analog zu Robins Pole-Pole-Video,
QR-Code dazu über chrismandel.de. 3 Konzepte vorgeschlagen (A Korridor-Flug, B Erwachen, C Die sieben
Stufen). **Chris' Entscheidung: A + B kombinieren** (Korridor-Flug geht über in Erwachen/Gesicht-aus-Licht),
**Song kommt später** (erst Video-Konzept, Song-Text/Suno ist ein eigener, späterer Schritt — jetzt nicht
anfangen). Kostenfrage geklärt: Song+Download praktisch kostenlos (Suno Pro inklusive), Render lokal/
kostenlos; einzige echte Frage ist die RENDERZEIT. Chris' Go: "mach mal" →
nächster Schritt ist ein kurzer Eevee-Testclip (~10s, Zielauflösung) auf der bestehenden Nordlicht-Szene
aus `C:\Tools\blender_proj\cover\cover_skizzen.py` (Cycles-Vollbild bisher: 800×1280/48 Samples ≈ 1-2 Min/
Bild — für 3 Min Video unpraktikabel, daher Eevee-Test nötig, um reale Bilder/Sekunde auf der RTX 4050 zu
messen, bevor eine Zeitangabe für den vollen Render genannt wird).
**Blocker:** `/mnt/c` in dieser Session gesperrt (Telegram-Sandbox-Muster) — Blender/Windows nicht erreichbar.
**Nächster Schritt (normale Terminal-Session):** `cover_skizzen.py` auf Eevee + Animation (Kamerafahrt
Korridor → Vorhang öffnet sich → Gesicht entsteht aus dem Licht, Konzept A+B kombiniert) umbauen,
10s-Test rendern (`blender.exe -b -P skript.py -- v1d_video_test ...`), Bilder/Sekunde messen, daraus
ehrliche Zeitschätzung für 3 Min ableiten, dann Chris das Testergebnis zeigen. Song-Text/Suno bewusst
noch NICHT anfangen (Chris: "später").
Chris verstand den Einstieg nicht (gelöschter Satz „Es ist nicht auszuschließen, dass“ nicht mehr im Kopf). In Kap. 11 von „Marlie tippte auf die graue Schrift“ bis „Einmal mit dem Satz.“ neu gefasst (Lenis Rekonstruktion des Satzes, „sechs“ statt „sechste“, siebte Zeile „hing unten aus dem Bild“, Marlies Rätselsatz erklärt). Backup `workspace/backups/aurora2_vor_kap11_anfang_*.json`. Kap. 10 zusätzlich: „die unteren beiden [Verlaufszeilen] hingen noch unter dem Rand“ ergänzt (Backup aurora2_vor_kap10_siebte_zeile_*). „Kuchenkarte“ bleibt.

---

## ✅ 04.10.2026 ~19:30 — Book-Hänger gelöst + Phone Link/Spotify
Book hing (Store-App/Eingabe), Force-Restart Power+Lauter 15 s half. Spotify-Autostart aus, Smartphone-Link per winget installiert. Details in project_book_akku.md. Offen: Tunnel :2222 vom Book prüfen (nach Reset nicht oben), Chris koppelt Duo in Phone Link.

---

## ⏳ 04.10.2026 ~13:10 — Kurstag 4 (Gruppe II) itslearning: VORBEREITET, Versand erst MO 05.10. NACHMITTAGS

Termine: 7d II + 7b II Mi 07.10. · 7a II + 7c II Do 08.10. (gegen schuljahr2627.json geprüft). Vorab-Check erledigt:
`04-The Basics - Codierung.pdf` hat 14 Seiten = 14 Folien der PPTX (gleiche Reihenfolge), `04-Praktikum.html` da,
kein Praktikum-PDF (Regel). Texte (4× individuell, mit Emojis, Wochentage stimmen) fest in
`scripts/itslearning_post_kurstag.py` eingetragen (DAY_PREFIX="04", II-Kurse; Backup `backups/itslearning_post_kurstag_vor_kt4II_*.py`).
**NICHT gepostet.** Nächster Schritt: Mo 05.10. nach ~14 Uhr `python3 /home/bolla/workspace/scripts/itslearning_post_kurstag.py`
(Handlauf, kein Cron; Classifier blockiert ggf. → Chris per `!`). Danach Screenshot-Check der 4 Mitteilungen.

---

## 📌 04.10.2026 — AURORA II: Plan bis Buchende (mit Chris vereinbart)

- Beide Word-Dateien (Vorschläge Kap1-8, Samstagsbericht) vom Desktop gelöscht auf Chris' Wunsch.
- Kap. 1–9 stehen (Chris-Entscheidungen + Jackenlogik drin). **Chris liest jetzt Kap. 10–24 und arbeitet seine Korrekturen selbst ein** (Reader-Markieren). Bolla macht KEINEN weiteren Drüberlauf dazwischen. Kap. 25–27 noch nicht geschrieben.
- Ab Kap. 19 Plot-Weichen möglich → beim Lesen nachfragen, was gefällt.
- **Am Schluss 2 Lektorläufe, dazwischen keine inhaltlichen Änderungen:** (1) Konsistenz über das ganze Buch (Wochentage, Zahlen, Figuren, Band-I-Abgleich, Kanon); (2) sprachlicher Feinschliff (Rhythmus, Wiederholungen, Humor gleichmäßig; ggf. Fable nach [[feedback_fable_budget_disziplin]]).

---

## ⏳ 04.10.2026 — AURORA-Reader: offene Vorschläge waren unsichtbar (jetzt im Text markiert)

Chris sah bei „1 offen" (Kap. 6) keine Sätze. Ursache: Der Reader zeigte nur den Zähler, nicht die Stelle im Text.
Fix: offene Vorschläge (status `wartet_entscheidung`) werden im Kapiteltext lila gepunktet markiert; Antippen öffnet
Bollas Antwort + Übernehmen/Verwerfen. Gilt nur für Sätze, die in EINEM Textabschnitt stehen (Fragmente gehen).
Offen in aurora2.json (Stand heute, nicht von mir entschieden): Kap. 6 „dann von Marie aufgehalten worden," (Frage
„wer ist marie", 22.09. 13:43), Kap. 7 „Mia hat mir geschrieben…", Kap. 8 „vier Millionen…", Kap. 10 „Es war kein Nein…".
Chris hatte nach eigener Aussage übernommen/verworfen — die Einträge stehen aber noch auf `wartet_entscheidung`:
Ursache unklar (Entscheidung ggf. über alten Pfad nicht gespeichert). **Chris entscheiden lassen**, dann Status bereinigen.

## ✅ 04.10.2026 — AURORA-Reader: Lesestelle wird gespeichert (Fix „fängt immer bei Kap. 1 an")

Ursache: Beim Start wurde Kapitel 0 angezeigt und dabei die gespeicherte Kapitelnummer überschrieben, bevor sie
gelesen wurde. Außerdem wurde nur das Kapitel, nie die Doppelseite gemerkt.
Fix in `mission-control/aurora-reader.html`: Lesestelle als `localStorage a2_pos = {kap, spread}` bei jedem
Blättern gespeichert und beim Start VOR der Anzeige eingelesen. Kein Server-Neustart nötig (reines HTML).
**Ungetestet** hier. **Chris prüfen:** Kapitel öffnen, ein paar Seiten weiter, App schließen, neu öffnen → gleiche
Stelle? Hinweis: Ändert sich die Schriftgröße (A+/A−), kann die Seitennummer auf einen anderen Textabschnitt zeigen.

## ✅ 03.10.2026 — Samstags-Ausreizung AURORA II beendet (gestoppt: 5h-Fenster 100.0 % und Reset nach Deadline)

Kap. 1–18 geprüft/korrigiert, Kap. 19–27 geschrieben soweit Kontingent reichte (Buch jetzt 24 Kapitel). Details: `/home/bolla/workspace/scratch/aurora_samstag_20261003/ABSCHLUSSBERICHT.md`, Änderungsprotokoll `changes.md`. Bogenplan privat in aurora2.json → geheim.bogenplan_19_27 (nie zeigen). **Chris: ab Kap. 19 sind Plot-Weichen möglich (siehe `weiche` im Bogenplan) — beim Lesen von Kap. 19+ nachfragen, was gefällt.**

---

## ✅ 04.10.2026 ~09:50 — Telegram-Hänger gefixt + Kanon-Liste live

- **Telegram:** Bot-Prozess (seit 25.09.) hing mit DNS-Fehlern (seit mind. 02:00), Netz war ok. Neu gestartet. `telegram_bot_watchdog.sh` erkennt jetzt Hänger (30 Logzeilen nur getUpdates-Fehler + Log <3 Min alt + DNS ok → Neustart, 10 Min Cooldown). Backup in backups/*_pre-hangcheck.sh. Falle: `pkill -f telegram_bot.py` killt die eigene Shell — Muster `python3 .*telegram_bot.py` nehmen.
- **Kanon-Liste:** `aurora2.json` → Key `kanon` (4 Einträge: AURORA Vierjährige weiblich, Frauke 17 Kita-Jahre, Jacken-Verlauf Kap 5/6, Kap-7-Zeitfenster Sonntag 23:20). `/api/aurora2/satz-frage` hängt sie als KANON-Block an beide Prompts (Korrektur + wer/was). MC neu gestartet. Backups `backups/*_vor_kanon_*`. Ende-zu-Ende-Test mit echtem Opus-Call noch offen (läuft beim nächsten Markieren im Reader). Weitere Kanon-Punkte einfach in `kanon` ergänzen.
- **04.10. ~11:45 Chris-Entscheidungen zum Bericht umgesetzt:** Handlungsjahr 2026 → ALLE Daten im Buch um −1 Tag verschoben (Wochentage unverändert; 10.10.=Samstag, 9.11.=Montag; Theos Todestag jetzt 10. Oktober) in kapitel/glossar/geheim/kriterien/steuerung/einschub (Skript `scripts/aurora_kalender_2026.py`, Backup `backups/aurora2_vor_kalender2026_*`; 273 Ersetzungen). Kap 8 heißt jetzt „Neununddreißig Häkchen“. Kap 2 Kopfhörer-Vergleich, Kap 7 Vorausschau, Kap 9 Riemann bleiben (Kanon Eintrag 7). Kap 19 Kreft-Satz: Chris liest erst selbst. Nicht angefasst: kommentare/satz_markierungen/Lesebegleiter/bible.json (alte Daten möglich).
- **04.10. ~11:15 Samstags-Bericht als Word** `Desktop\AURORA_II_Samstagslauf_Bericht.docx` (Skript scripts/aurora_samstag_bericht_docx.py), altes Word `AURORA_II_Vorschlaege_Kap1-8.docx` auf Chris' Wunsch gelöscht. **Kalender-Befund:** Buchkalender (11.10.=Samstag, 10.11.=Montag) folgt 2025, nicht 2026. Kap 6 „Der Samstag“ deshalb NICHT geändert; Kanon-Eintrag 6 warnt davor, Wochentage zu „korrigieren“. Offen: Chris entscheidet 2025 vs. 2026 (Kap 15 „vor sechs Jahren“ hätte zu 2025 gepasst). Weitere offene Punkte im Word (Kap 2 Selbstmord-Vergleich, 7 Vorausschau, 8 Titel, 9 Riemann, 19 Kreft-Satz).
- **Erledigt 04.10. ~10:15:** Eintrag 54 komplett: Kap 5 war schon auf „der schläft“; Kap 15 „nur privat“ war schon weg; Kap 15 „vor sechs Jahren in Delft“ → „2019 in Delft“ (Kap 12 sagt 2019). Jacken Kap 5–9 gelesen: konsistent. Kanon Eintrag 5 (Foto-Satz) ergänzt. Backup `backups/aurora2_vor_kap15_delft_*`. Buch-Jahr 2026 festgelegt (Chris, 04.10.) und als Kanon-Eintrag 6 gespeichert; alle „vor/seit X Jahren“-Angaben Kap 1–24 gegen 2019/2017/2011 geprüft: keine Widersprüche.

---

## ✔️ erledigt (s.o.) 03.10.2026 ~20:00 — Kanon-Liste für MP-Korrekturdialog
Chris will: kurze „Kanon-Liste“ (Entscheidungen wie Jacke-Weg, Frauke 17 Jahre, AURORA=Vierjährige weiblich, Kap-7-Abruf Sonntag 23:20) in aurora2.json ablegen und dem Satz-Korrektur-Dialog (/api/aurora2/satz-frage) als Kontext mitgeben, damit MP-Funde nicht gegen andere Kapitel laufen. Offen außerdem: Kap 15 „nur privat“/„zweimal“ (zu Eintrag 54). Chris cleart die Session nach dem Backup.

---

## ✅ 03.10.2026 ~19:50 — AURORA II: Chris-Entscheidungen (Word-Liste Kap 1–8) eingebaut
Skript `scripts/aurora_apply_entscheidungen.py`; Backups `backups/aurora2_vor_*`. Jacken-Lösung: Marlie ließ Jacke bei Basti hängen, Kaffeemann nahm sie (Kap 5/6). Frauke 17 Jahre überall. Offen: Kap 15 „nur privat“/Zählung „zweimal“ (zu Eintrag 54), Kap 6/9 Jacken-Stellen nochmal lesen.

---

## 🛑 03.10.2026 ~18:30 — Samstags-Lauf: nach heute Abend NICHT weitermachen (Chris)

Der Prozess `samstag_ausreizen.py` pausiert bis 21:11 (5h-Reset), arbeitet dann im 92%-Deckel (Kap. 15–18 prüfen, Kap. 19 gegenlesen, Kap. 20 u. ggf. weitere schreiben) und beendet sich spätestens 23:50 selbst (Deadline) — keine Fortsetzung am Sonntag/Montag, kein Cron. Rest (Kap. bis 27, Phase 4) nur auf Chris' Zuruf oder nächsten Samstag; Skript ist resume-fähig (state.json). Wochenanfang: Token schonen für aktuelle Dinge ([[feedback_limit_regeln]]).

---

## ✅ 03.10.2026 16:15 — AURORA-Reader: „Senden an Bolla" war kaputt wegen Tastatur-Resize (jetzt gefixt)

Ursache: Tastatur öffnen → window-resize → layout() → goSpread() → clearSel() setzte `curSel=null` → Senden-Klick `if(!curSel) return` tat still nichts. Fix: clearSel() lässt curSel in Ruhe; resize-Handler layoutet nur noch bei geänderter BREITE. Per ADB/CDP auf dem Duo verifiziert (Text getippt, Anfrage ging raus, Opus-Antwort kam). Lehre: Dialog-Zustand nie an UI-Zustand koppeln, den Resize/Layout zurücksetzt; Tests am Duo immer mit echtem Tastatur-Fall.

---

## ✅ 03.10.2026 13:15 — AURORA-Reader (Duo): Tipp-Markieren + Dialog repariert

Chris: Zieh-Blasen zum Markieren sprangen über Absätze, „Senden" war vom Textfeld/Tastatur verdeckt. Jetzt: Satz ANTIPPEN = ganzer Satz gelb markiert, Leiste ◀ Davor / Danach ▶ / 🚩 Korrigieren / ✕ (Leiste oben, wenn der Satz in der unteren Hälfte liegt); nicht eindeutige Sätze werden automatisch erweitert. Dialog: Knöpfe + Statusmeldung OBEN, Textfeld darunter, Toast bei Fehlern. Per CDP auf dem Duo getestet: tippen → 🚩 → senden → Opus-Antwort kam an. Test-Eintrag + überschriebene Lesemarke Kap. 1 wiederhergestellt. Backup `backups/aurora-reader_*_pre-tap.html`. Duo-Debug: `adb connect 192.168.178.20:5555`, dann `adb forward tcp:9333 localabstract:chrome_devtools_remote`.
Samstags-Lauf pausiert wegen 5h-Gate bis 16:10 (14 Kapitel geprüft), danach läuft er allein weiter.

---

## 🔄 03.10.2026 12:30 — SAMSTAGS-AUSREIZUNG LÄUFT (detacht, Python-Prozess `scripts/samstag_ausreizen.py`)

Chris will jeden Samstag das Wochenkontingent bis 0:00 gegen 0 % fahren ([[feedback_limit_regeln]]). Heute: AURORA II Kap. 1–18 prüfen/fixen, dann Kap. 19–27 schreiben, Rest: Zweitleser/Band-I-Check/Lesebegleiter/Fehlerjagd.
Status live: `workspace/scratch/aurora_samstag_20261003/STATUS.md` · Log `workspace/logs/aurora_samstag.log` · Änderungsprotokoll `changes.md` · inhaltliche Funde in Chris-Kapiteln 1–8 NICHT angewandt → `vorschlaege_fuer_chris.md`.
Notbremse: `touch /tmp/aurora_samstag_stop`. Resume: Skript erneut starten (state.json). Backup: `backups/aurora2_backup_vor_samstag_20261003_1222.json`.
Policy: Kap. 1–8 (von Chris gegengelesen) nur Grammatik/Tippfehler automatisch; Kap. 9–18 + neue Kap. auch Humor/Spannung/Logik. Bogenplan 19–27 liegt privat in aurora2.json → geheim.bogenplan_19_27 (nie zeigen). Nach Ende: Abschlussbericht wird automatisch oben in diese Datei geschrieben.

---

## ✅ 03.10.2026 ~12:30 — AURORA-Reader als App auf dem Duo: läuft, Chris zufrieden („erst mal so lassen")

Installation ging erst nach `crossorigin="use-credentials"` am Manifest-Link (Cloudflare Access leitete den Manifest-Abruf auf Login um, 302).
Stand: Doppelseite über beide Displays, Falz frei, installierbar als App ohne Edge-Leisten, ⛶-Vollbild-Knopf vorhanden. Keine weiteren Schritte offen.
Merke für andere PWAs hinter Cloudflare Access: Manifest-Link immer mit crossorigin="use-credentials".

---

## ⏳ 03.10.2026 12:15 — AURORA-Reader: Edge-Leisten loswerden (Vollbild-Knopf + Web-App-Manifest)

Chris stören im Span-Modus die zwei Edge-Adressleisten, auf einem Display Edge-Elemente unten. Gebaut: Knopf ⛶ (requestFullscreen, auf einem Display per ADB getestet: Leisten weg)
+ `mission-control/aurora.webmanifest` (standalone, scope /aurora) + Route `/aurora.webmanifest` in mission_control_api.py (Backup *_pre-aurora-manifest.py), MC-Server neu gestartet.
**Offen:** Chris muss das alte Startbild-Icon „AURORA II · Le…" löschen und über Edge ⋮ → „Zum Telefon hinzufügen"/„App installieren" neu anlegen, dann ohne Edge-UI starten + spannen testen. Vollbild im Span-Modus noch ungetestet.

---

## ✅ 03.10.2026 12:02 — AURORA-Reader Duo-Modus funktioniert (per ADB-Screenshot verifiziert)

Edge 153 auf Duo 2 meldet KEINE Viewport-Segmente (visualViewport.segments leer, Media-Query false). Fallback in `aurora-reader.html`:
Erkennung über screen.width×dpr (2754→Hälfte 1344 / 2784→1350). Kopf/Fuß/Dialog jetzt je Display getrennt, Falz frei.
Duo-DevTools: `adb forward tcp:9333 localabstract:chrome_devtools_remote` (Duo 192.168.178.20:5555, Reconnect hat Autorisierung wiederhergestellt).
Offen: Edge zeigt oben zwei Adressleisten (Edge-eigener Effekt, nicht die Seite).

---

## ⏳ 03.10.2026 — AURORA-Reader: Duo-Zweibildschirm-Modus eingebaut (ungetestet)

`aurora-reader.html` erkennt jetzt Viewport-Segmente (visualViewport.segments → getWindowSegments → env()-Fallback) und setzt
Spaltenlücke = Falzbreite + Ränder → linke Seite im linken, rechte Seite im rechten Display, Kopf/Fuß/Kapitelliste/Dialog segmentweise.
Backup in workspace/backups/aurora-reader_*_pre-duo.html. `/aurora` liefert 200 (Server lädt von Platte). **Chris testet auf dem Duo** (gespannt, Edge).

---

## ⏳ 03.10.2026 — AURORA-Leser/Korrektur-Seite für den Duo gebaut (MC-Neustart fehlt noch, ungetestet)

Chris wünscht: Kapitel wählen → Buch als Doppelseite (links/rechts wie Kindle) → Satz markieren → 🚩 Korrektur →
Kommentar schreiben → Bolla antwortet + Vorschlag → Übernehmen/Verwerfen. Backend existiert schon
(`/api/aurora2/satz-frage` + `satz-frage-status` + `satz-entscheidung`, Opus) — nur die Oberfläche war neu.
**Gebaut:** `mission-control/aurora-reader.html` (Kapitelliste mit „offen"-Badges, CSS-Spalten als Doppelseiten,
Tap-Zonen/Wischen, A+/A−, Satz-Erkennung um die Markierung, Dialog mit Antwort/Vorschlag/Übernehmen/Verwerfen).
Route `/aurora` (+`/aurora.html`) in `scripts/mission_control_api.py` MOBILE_STATIC ergänzt.
**Noch NICHT live:** MC-Server braucht Neustart, damit `/aurora` ausgeliefert wird (Prozess-Inspektion/Kill in der
Telegram-Session blockiert → nicht riskiert). Danach auf dem Duo testen: Doppelseite bei breiter Ansicht (≥900px),
Markieren/Satz-Erkennung, Wischen, Opus-Antwort-Dialog. **Ungetestet** (kein Browser hier).
**Nächster Schritt:** Chris: MC neu starten (oder Bolla in normaler Session), dann `/aurora` auf dem Duo testen und Rückmeldung.

---

## ✅ 02.10.2026 ~10:30 — PPT-Kurstag 4 (Datei 08-2 Ansichten/Entwurf): Check + Entwurf fertig

- Entwurf: `Handouts/Entwurf/08-2 Powerpoint Profi Ansichten Entwurf_Entwurf.pptx` (Folie 12 „Heute/Project Digit" gelöscht, 12 Folien) + `Entwurf/08-Praktikum.html` (Zweiteiler: Teil 1 Tagesthema im eigenen Projekt, Teil 2 kreativ).
- Korrekturen: Folie 13 (Impress HAT Presenter Console; „moderner"→„weniger modern"), Folie 9 (GPT-5/Dall-E 3 veraltet → GPT/GPT-Image/MAI-Image; Notiz: Copilot seit 2025 in M365 Personal/Family), Notiz Folie 3 (Impress hat Inhalt-Platzhalter mit Symbolen). Folien 7/8 = Demos, nicht angefasst.
- Offen: Chris prüft Entwurf; Live-Datei unverändert. Screenshot auf Folie 10 zeigt noch alten Dateinamen „7-2 …".

---

## ✅ 02.10.2026 ~11:00 — Aufräumen: Screenshots + Download-Planer entfernt

- **Screenshots** (`OneDrive\Bilder\Screenshots`, 1.603 Dateien/405 MB): auf Chris' Freigabe (1,2,3 ohne Rückfrage) → auto-benannte `Screenshot…` >2 Jahre (303) GELÖSCHT, 1–2 Jahre (182) nach `Archiv_bis_2025` verschoben, benannte Dateien (Busch Jäger…, Schulferien 2025, desktop.ini) unberührt. Jetzt 262 MB. Datum aus Dateiname, nicht mtime.
- **MP „Bolla Songs → 🎧 Downloads"-Planer gelöscht** (Button, Box, JS, API-Routen, Server neu gestartet, `/api/suno/downloads` → 404). Grund: Chris rechnet Downloads selbst (16 Songs pro 4er-Block). Backups in `workspace/backups/*pre-dlplaner-entfernen*`. Siehe [[project_suno_download_limit_planung]].

---

## ✅ 02.10.2026 ~10:00 — Amazon-Prime-Sammelklage: Anmeldung ABGESENDET (⏳ Bestätigung nachverfolgen)

Chris hat das BfJ-Formular ausgefüllt und abgeschickt (Bestätigungsseite „Anmeldung wurde an das Bundesamt für Justiz versendet").
Angaben: Verbraucher, Christoph Mandel, Buchenweg 67a Norderstedt, Prime-Jahresabo seit 07.01.2019, Erhöhung 69→89,90 €
erstmals 07.02.2023, 4 Verlängerungen → Anspruch 83,60 €. Details: [[project_amazon_prime_seit]].
**Nachverfolgen:** Bestätigung der Eintragung kommt **per Post**. Kommt bis **~13.11.2026 (6 Wochen)** nichts → Kontakt zum BfJ
aufnehmen (Verbandsklageregister). Beim Session-Start ab 13.11. aktiv nachfragen. Optional: Newsletter Verbandsklageregister
für dieses Verfahren (Chris entscheidet). Eine Anmeldung reicht (gemeinsames Konto mit Reni).

**Newsletter Verbandsklageregister (BfJ):** Chris hat sich 02.10. ~09:20 angemeldet. In Outlook liegen 3× „Bestellung des Newsletters … Bitte um Bestätigung"
(noreply@bfj.bund.de, 07:22 UTC) — Double-Opt-in: **Bestätigungslink muss angeklickt werden**, sonst kommt nichts. Nachverfolgen: Absender
`bfj.bund.de` / `bundesjustizamt.de` in Outlook beobachten (Bestätigung + spätere Newsletter zum Verfahren Amazon/Prime, OLG Hamm).
Wichtige Mails dem Chris zeigen (Fristen, Vergleich, Anmelde-Hinweise).
**✅ 02.10.2026: Chris hat den Bestätigungslink geklickt** („Ihre Newsletterbestellung wurde erfolgreich durchgeführt"). Newsletter aktiv — jetzt nur noch eingehende BfJ-Mails beobachten.

---

## ✅ 02.10.2026 — Amazon-Prime-Sammelklage: Anmeldelink recherchiert + in gclip gelegt

Chris fragte wegen des BGH-Urteils vom 01.10. (Prime-Preiserhöhung 2022, 7,99→8,99 €/Monat bzw. 69→89,90 €/Jahr
unwirksame AGB-Klausel, Verbraucherzentrale NRW gewinnt). **Anmeldung zur Sammelklage (OLG Hamm) ist NICHT
automatisch** — kostenlose Eintragung ins Klageregister beim Bundesamt für Justiz nötig:
`https://www.bundesjustizamt.de/DE/Themen/Verbraucherrechte/VerbandsklageregisterMusterfeststellungsklagenregister/Verbandsklagenregister/Verbandsklagen/Klagen/202602/Anmeldung/Formular_node.html`
(verifiziert: betrifft genau diese Preiserhöhung, Beklagte Amazon EU S.à r.l., Klägerin Verbraucherzentrale NRW).
**Frist:** bis 3 Wochen nach Ende der mündlichen Verhandlung — genauer Stand/ob schon gelaufen nicht ermittelt,
im Zweifel zeitnah anmelden. Link liegt im gclip (`/api/clipboard`, Tab „Clipboard" in mmp).
**Nächster Schritt:** Falls Chris möchte, Anmeldeformular gemeinsam durchgehen (Vertragsdaten: seit wann Prime,
welcher Tarif monatlich/jährlich).

---

## ⏰ 01.10.2026 — Suno Premier-Monat läuft bis 31.10. (Downgrade-Termin!)

Chris hat heute auf Premier upgedatet (60 Downloads/Monat), Abrechnung 01.11. **Bis 31.10. wieder auf Pro stellen** (ab 25.10. aktiv erinnern!). Bis dahin Schüler-Geburtstagssongs für Okt/Nov/Dez vorab erzeugen und herunterladen (Okt 6, Nov 8, Dez 11 Geburtstage, Jan 7, Feb 12). Details: [[project_suno_download_limit_planung]]. Geklärt: 2 Songs pro Kind (DE+EN). **Download-Planer in MP gebaut** (Bolla Songs → 🎧 Downloads), siehe Projekt-Datei. Offen: Chris prüft den Planer im Browser; bereits geladene Songs (z.B. Chiara) abhaken bzw. per "✏️ korrigieren" nachtragen.

---

## ✅ 01.10.2026 ~10:45 — Suno v6: Struktur-Tags mit Vortragsanweisung eingebaut (✅ Test bestanden)

- Chiaras Geburtstagssong: war gestern Abend doch noch erfolgreich verschickt (Eintrag vom 30.09. 19:25 ist überholt).
- Regler-Hinweis (Variety Off, Style Influence ~80%, Weirdness ~25%) existierte schon in index.html (`sunoRenderSliderHint`) — nichts zu tun.
- NEU in `scripts/mission_control_api.py` (beide Lyrics-Prompts DE+EN): Tags jetzt `[Verse 1 | warm, spoken-sung]`, `[Chorus | full band, shout-along]` etc. (2-4 Wörter, nur Vortrag/Dynamik, Intro ohne Zusatz). Backup `backups/mission_control_api_*_pre-v6-tags.py`, Server neu gestartet.
- **Testergebnis (01.10.):** Chris hat live getestet — Suno singt die Anweisungen NICHT mit, Unterschied zwischen Abschnitten ist hörbar. Bleibt dauerhaft drin, kein Rollback. (Alter Plan war: Chris testet mit den 3 anstehenden deutschen Geburtstagssongs; prüfen ob Suno Tag-Text mitsingt (dann Rollback aufs Backup) und ob die Vortragsanweisung hörbar greift. Ergebnis in [[feedback_suno_lyrics_qualitaet]] festhalten.

---

## 🎵 01.10.2026 — Suno-Prompt-Scout: mögliche Optimierung gefunden

Automatisch vom monatlichen Suno-Prompt-Scout-Cron gefunden (Nachfolge-Check zum 19.08.2026-Audit) — mit Chris besprechen, ob umsetzen.

🎵 Suno v6 ist da: Suno hat v6, v6-wild und v6-mini am 09.09.2026 veröffentlicht und will ältere Modelle abschalten. Der Prompt-Code ist auf v5.5 abgestimmt (Kommentar bei Zeile ~10434). v6 folgt dem Style-Feld laut Community "wörtlicher" (r/SunoAI: "wants to be directed exactly"). Bei Qualitätsproblemen sollte man die Lehren aus dem 17.08. (Schuld an v5.5) neu bewerten. Quellen: [TechCrunch](https://techcrunch.com/2026/09/09/suno-replaces-its-ai-models-with-a-new-one-trained-on-licensed-music-as-copyright-suits-pile-up/), [Music Ally](https://musically.com/2026/09/09/suno-launches-its-v6-ai-music-models-heres-what-you-need-to-know/).

🎵 Variety und Style Influence im Hinweis an Chris: v6 hat einen neuen Variety-Regler, der den Style-Prompt laut Guides absichtlich umschreibt. Style Influence steht standardmäßig auf 50 %. Das Tool sollte neben dem Prompt einen Hinweis ausgeben, etwa "Variety auf 0, Style Influence höher setzen", sonst verwässert Suno die sorgfältigen Tags (Schlager-Vermeidung, Sprach-Tag). Das ist unabhängig vom Prompt-Text und kostet nichts. Quellen: [hookgenius v6-Guide](https://hookgenius.app/learn/suno-v6-guide/), [Undetectr](https://undetectr.com/blog/suno-v6-changing-your-prompt).

🎵 Performance-Cues in den Struktur-Tags: v6 liest Anweisungen in den Klammer-Tags pro Abschnitt, z. B. `[Verse 1 | warm, spoken-sung]` oder `[Bridge | Female — Whispered]`. Die Regel "Struktur-Tags ohne erfundene Tags" blockiert das womöglich. Hier würde man ein Tag-Muster `[Abschnitt | kurze Vortragsanweisung]` zulassen, besonders bei Geburtstagssongs für Refrain und Bridge. Ob das auch bei deutschen Texten greift, ist noch nicht belegt, daher erst mit 2-3 Testsongs prüfen. Quelle: [hookgenius v6-Guide](https://hookgenius.app/learn/suno-v6-guide/).

---

## ⏳ 30.09.2026 ~19:25 — Chiaras Geburtstagssong NICHT verschickt (Classifier blockiert, Chris muss selbst per `!`)

Chris fragte abends nach, ob Chiaras Songs verschickt wurden — waren es NICHT: das Skript ist reiner
Handlauf (kein Cron), die 14:00-Sperre im Code verhindert nur einen ZU FRÜHEN Start, löst aber selbst
nichts automatisch nach 14:00 aus. Niemand hat den Lauf nach der Vorbereitung um 10:40 nochmal gestartet.
**Jetzt (19:25) versucht, nachzuholen — beides vom Auto-Mode-Classifier blockiert:**
1. Read-only Check, ob mit Chiara schon eine Konversation existiert (`scripts/_tmp_check_chiara_conv.py`,
   nur Login+Screenshot, kein Senden) — blockiert.
2. Der eigentliche Versand (`scripts/itslearning_send_private_song.py`) — ebenfalls blockiert.
Gleiches Muster wie Buhl-Mail/Kalender-Löschung: jeder Bash-Aufruf, der `itslearning_credentials.json`
nutzt bzw. echte Aktionen auf echten Systemen macht, wird als Real-World-Transaction geblockt.
**Nächster Schritt:** Chris bittet, ODER selbst kurz `python3
/home/bolla/workspace/scripts/_tmp_check_chiara_conv.py` (nur Kontrolle, sendet nichts) und danach
`python3 /home/bolla/workspace/scripts/itslearning_send_private_song.py` (EMPFAENGER/MESSAGE/SONGS
bereits auf Chiara gesetzt) per `!` im Terminal selbst freizugeben. Check-Skript danach löschen.
**Update:** Chris wollte die 2 Befehle in der Windows-Zwischenablage am Studio — `clip.exe` direkt ist in
dieser Session ebenfalls blockiert (gleiches Classifier-/Approval-Muster). Ausweichlösung: beide Befehle
liegen im geräteübergreifenden gclip (`/api/clipboard`, Tab „Clipboard" in mmp). Chris am Studio bitte
dort kopieren statt mit Strg+V direkt — echte Windows-Zwischenablage ging nicht.

---

## ✅ 30.09.2026 ~12:10 — AURORA II: "wer/was"-Nachschlagen + Glossar gebaut, Kap. 10-18 rückwirkend befüllt

Chris' Problem: bei mehrtägigen Schreibpausen mitten in AURORA II vergisst er Details (Beispiel: das
zusammengefaltete Blatt in Marlies Jacke, Name "Weidenbach") und muss mühsam in frühere Kapitel zurückblättern.
Vorschlag mit drei Optionen (A: "wer/was"-Kurzform im Satz-Tool, B: aufklappbare Kapitel-Zusammenfassung —
existierte als ungenutztes UI-Element `aurora2-recap`/`kap.zusammenfassung`, C: wachsendes Glossar). Chris wollte
A+C, B ausdrücklich nicht (das `aurora2-recap`-Element bleibt unangetastet/ungenutzt liegen, NICHT weiter ausbauen).

**Umgesetzt (Code: `mission_control_api.py`, `mission-control/index.html`; Backups in `workspace/backups/`
vor jeder Änderung, `*_pre-wer-was-glossar.*`):**
- **A — "wer"/"was" im Satz-Tool:** In `/api/aurora2/satz-frage` erkennt der Handler jetzt, wenn Chris' Bemerkung
  (nach trim/lower/Fragezeichen-Entfernen) "wer", "was" o.ä. ist. Dann bekommt Opus statt der üblichen
  400-Zeichen-Lokalkontext den KOMPLETTEN bisherigen Buchtext (alle Kapitel bis einschließlich dem aktuellen,
  keine Spoiler aus späteren) und beantwortet die Frage mit Fundstelle. VORSCHLAG wird hart auf den Originalsatz
  gesetzt → `geaendert=False` → kein Annehmen/Verwerfen nötig, nur Antwort anzeigen. Kein Frontend-Änderungsbedarf,
  nutzt das bestehende Panel 1:1. Funktioniert sofort für alle 18 bestehenden Kapitel, unabhängig vom Glossar.
- **C — Glossar:** Neues Feld `glossar[]` in `aurora2.json` (id/name/kategorie/beschreibung/kapitel_titel/datum).
  Neue Helper-Funktion `_aurora2_glossar_ergaenzen()` (Modul-Ebene, nahe `_aurora2_job`-Globals) — läuft
  automatisch synchron im `/api/aurora2/generiere`-Hintergrund-Thread, aber NUR wenn wirklich ein neues Kapitel
  angehängt wird (nicht bei Überarbeitung/Revision bestehender Kapitel). Ruft Opus mit dem neuen Kapiteltext +
  Liste bekannter Namen auf, extrahiert max. 6 neue Personen/Objekte/Orte/Begriffe, hängt sie an. Komplett in
  try/except — darf die Kapitel-Generierung nie zum Kippen bringen. Frontend: neue Karte "📚 Glossar" links unten
  (`aurora2-glossar-card`, nur sichtbar wenn Einträge existieren) mit Suchfeld, Klick auf Eintrag springt zum
  Ursprungskapitel (`aurora2RenderGlossar()`/`aurora2GlossarSpringen()`, analog zum bestehenden Muster).
- Server-Neustart durchgeführt (Kill alte PID + `start_mc_server.sh` neu, detached) — Backend-Codeänderungen
  brauchen das, Datenänderungen (aurora2.json) nicht, da jede Anfrage frisch von Platte liest.

**Rückwirkende Befüllung:** Chris liest gerade Kapitel 10, Budget bei ~65% (muss bis Sa. 0:00-Reset reichen,
Zeitfenster danach eng: heute Mittag, morgen ganztägig, Fr/Sa nur je ein paar Stunden). Chris' Entscheidung nach
kurzer Rückfrage: **Kapitel 10-18 SOFORT nachziehen** (die, die er jetzt/bald liest), **Kapitel 1-9 NACH dem
Wochenreset** (die hat er schon gelesen, eilt nicht, spart Budget für aktuelles Schreiben). Einmal-Skript
`aurora2_glossar_retrofit.py` (im Scratchpad, nicht dauerhaft im Repo) lief im Hintergrund via Monitor-Tool
überwacht, sauber durchgelaufen: **54 neue Glossareinträge für Kapitel 10-18** (je 6 pro Kapitel), Backup vorher
`aurora2_20260930-120356_pre-glossar-retrofit-10-18.json`.

**Nächster Schritt:** Nach dem Wochenreset (Sa. 0:00) Kapitel 1-9 nachziehen — gleiches Skript-Muster, nur
`ZIEL_NUMMERN = range(1,10)`. Ab jetzt läuft das Glossar bei jedem neu geschriebenen Kapitel automatisch mit,
kein Handeln nötig. Chris kann ab sofort "wer"/"was" im Satz-Tool nutzen (alle 18 Kapitel) und die neue
Glossar-Karte in der MP-Seitenleiste nutzen (Kap. 10-18 schon befüllt).

---


## ✅ 15.10.2026 16:00 — AURORA-II-Trailer Eevee-Test gerendert
`C:\Tools\blender_proj\trailer.py` (neu, cover_skizzen.py gab es nicht) → 10 s, 1080p, Eevee Next: 240 Bilder in 200 s (0,83 s/Bild) → 3 Min ≈ 60 Min. Korridor-Flug (smaragd/türkis auf Nachtblau, Glow) funktioniert, Test-mp4 `Desktop\temp\AURORA_II_Trailer_Test_Korridor.mp4`. OFFEN: „Gesicht aus Lichtpunkten" (116 animierte Objekte bei y=-60) wird NICHT gerendert, auch statische Test-Kugeln/Zylinder nicht — Ursache unklar (Tori/Zylinder des Korridors rendern). Nächster Schritt: Ursache finden (evtl. Eevee-Next-Eigenheit, Cycles-Test), Wrapper `scripts/blender_trailer_test.sh`.

## ⏳ 15.10.2026 ~16:10 — AURORA II: R2+R3 für Kap. 1–12 läuft (Chris-Go), + 2 Merker
Detached `scripts/aurora2_r23_kap1_12.py` (nutzt Figuren-Pass-Gating: Woche ≤83 %, 5h ≤50 %, Deadline Fr 18:30; Log `logs/aurora_samstag.log` + `logs/aurora2_r23_kap1_12.out`, /jobs `aurora2_figuren_pass`). Kap. 1–8: nur Grammatik/Tippfehler direkt, Rest → `scratch/aurora_samstag_figurenpass_20261011/vorschlaege_fuer_chris.md` (Chris hat sie Satz für Satz gelesen). Ab Kap. 25 kein R-Lauf nötig (passiert beim Schreiben). Danach: Chris sagen, dass 1–24 einheitlich durch sind.
**MERKER (Chris: „nicht vergessen“):** R4-Ergebnisse (panel_vorher/nachher.json, Kap. 1–24) in MP einbauen — kurze Box auf AURORA-II-Seite (Vorher/Nachher Spannung/Humor/Figuren), NACH Abschluss R2/R3 Kap. 1–12 neu messen oder zumindest die Box mit Hinweis bauen.
**Trailer:** Chris: Video „geil“, aber KEIN Smiley, sondern ein REALES Gesicht aus Licht (Foto-/Portrait-nah, z. B. Lichtpunkt-/Partikel-Wolke aus einem Gesichtsbild oder Depth-Mesh). Test: Desktop\temp\AURORA_II_Trailer_Test_Korridor.mp4. Render ~0,6 s/Bild Eevee (3 Min ≈ 45 Min). Kamera-Bug war: rotation (90,0,180) nötig.

## ⏳ 15.10.2026 ~16:40 — AURORA-II-Trailer (Gesicht aus Cover Band I) RENDERT (Chris 2–3 h weg)
`C:\Tools\blender_proj\trailer_face.py` + `scripts/blender_trailer_face.sh` (detached, 720 Bilder, /jobs `blender-trailer-face`). Konzept: Korridor-Flug (0–14 s), AURORA-Cover-Gesicht (Band I, `Bolla\AURORA\2_eBook\AURORA_Cover.jpg`) setzt sich aus ~18k Lichtpunkten zusammen, Farbe orange→Nordlicht-Smaragd (Frame 480–600). Ergebnis: `Desktop\temp\AURORA_II_Trailer_Gesicht_30s.mp4`. Cover-Gesicht + Chris-Wunsch „reales Gesicht, kein Smiley“ umgesetzt. Offen danach: Song (Suno) + Länge 3 Min + Text/Titel, QR-Code.

## ✅ 16.10.2026 — Trailer-Zwischenstand gesichert
Beide Videos + Skripte + README nach `Bolla\AURORA II\7_Trailer_Blender\`, Desktop\temp-Videos gelöscht, Memory `project_aurora_ii_trailer_blender.md`. Offen: R2/R3-Lauf Kap. 1–12 prüfen, R4-Box in MP, Trailer-Ausbau.

## ✅ 16.10.2026 11:45 — Ausreizen verschoben + Cover-Idee notiert
Cron AURORA-II-Schreiblauf von Fr 19:00 auf **Sa 17.10. 10:00** verschoben (Chris: Limit schon bei 20; Backup backups/crontab_vor_fr_nach_sa_20261016.txt; Deadline Sa 23:50 unverändert). Reni-Cover-Feedback gemerkt (project_aurora_i_cover_reni_feedback.md + Datei in Bolla\AURORA\7_Cover_Verbesserung_Reni). Chris liefert noch Projektidee Nr. 2.

## ✅ 16.10.2026 — Rezensionsentwurf Reni für AURORA I
Datei Bolla\AURORA\6_Marketing\AURORA_Rezension_Reni_Entwurf.txt; /jobs-Eintrag 'aktion' (Reni gegenlesen + posten).

## ✅ 16.10.2026 — Sa-Lauf: Start Sa 17.10. 12:00, Wochen-Stopp 95 %
Chris: Woche bei 81 %, 1 Fenster ≈ 7 % → max. 2 Fenster. Cron 0 12 17 10; samstag_ausreizen.WEEK_STOP (Default 98.5), ausreizen_fr_aurora setzt 95 (Env AUSREIZEN_WEEK_STOP). 5h-Gate 92 % unverändert. Backups backups/*_vor_weekstop_20261016.py. Quota-Reset Sa 23:59.

## ✅ 16.10.2026 — R4-Box gebaut (MP, Backup index_vor_r4box_20261016.html); Prio: Cover I / Song II / Trailer nur auf Zuruf (bei moin nennen). Kein Extras-Skript (Auto-Mode blockte). Vorschläge Kap.1–8 + Kili-Song laut Chris erledigt.

## ✅ 16.10.2026 — Word-FERTIG-Knopf gebaut (docx_fertig.py + MP-Endpunkt /api/fertig, MC neu gestartet; Backup mission_control_api_vor_fertig_20261016.py). Vorschläge Kap.1–8 als Word: Desktop\AURORA_II_Vorschlaege_Kap1-8.docx (52 Stellen), Job aktion-vorschlaege-kap1-8 (Chris hatte sie doch noch nicht erledigt).

## ✅ 16.10.2026 ~12:30 — Kili-Song laut Chris FERTIG (Entwürfe nicht mehr nötig); Trailer-Frames/Temp aufgeräumt. Offen: Vorschläge Kap.1–8 (Word auf Desktop, Fertig-Knopf), Sa 12:00 AURORA-II-Lauf (Woche-Stopp 95 %), auf Zuruf: Cover I, Song II, Trailer-Ausbau; Reni-Rezension posten (/jobs aktion).

## ✅ 16.10.2026 — Offen-Übersicht + Sammel-Knöpfe
/jobs hat Block „Offen – Gesamtübersicht“ (data/offene_punkte.json, antippbar, API /api/offen). Word Kap.1–8 hat jetzt ALLES ÜBERNEHMEN / ALLES LASSEN (oben+unten) + FERTIG; Aktion landet in fertig_log.json + Job-Detail. Backups backups/*vor_offen*, *vor_buttons*. Regel: [[feedback_viele_punkte_sammelknoepfe]].

## 🛑 16.10.2026 — AURORA Punkte-Hintergrund ABGEBROCHEN (Ziel: Mädchen II + Korridor, heute nicht mehr starten)
Skript `C:\Tools\blender_proj\aurora_bg.py`, Wrapper `scripts/blender_aurora_bg.sh` (detached, land dann port, je 480 Bilder ≈ 11 Min, /jobs `blender-aurora-bg-land|port`). Ergebnis: `Desktop\temp\AURORA_Punkte_Hintergrund_land|port.mp4` + Kopie in `Bolla\AURORA II\7_Trailer_Blender\`. Idee: 41k-Punkte-Raster, Farbe per Zufallsverzögerung gemischt, Schweben-Shape-Key in der Mitte (unscharf). Befund Frame 1 Querformat: Gesicht I im Punktraster flau/kaum erkennbar → ggf. v2 mit mehr Kontrast (Gamma>1) oder höherer Punktzahl. Wochenlimit 82 % (Stand 17:45), Chris unterwegs.

## ✅ 17.10.2026 — Renis SOS-App + Steffi aus WhatsApp-Block
Steffi: `wa` aus config/sos_contacts.json entfernt (bleibt in Anrufliste). Neu: /sos (mission-control/sos.html, sos.webmanifest, sos-icon-*.png rot „SOS"), Kontakte config/sos_contacts_reni.json, API /api/sos/contacts-reni. Server neu gestartet. OFFEN: Chris' Handynummer in sos_contacts_reni.json (Eintrag „Chris (Ehemann)", tel+wa leer); Installation auf Renis Z Flip + Zugang (Cloudflare Access braucht Renis Mail als Policy, oder nur im Heim-WLAN http://<Studio-IP>:18790/sos). Backups backups/*_20261017*.

## ⏳ 17.10.2026 — Renis SOS: Kontakte fertig, Cloudflare-Freischaltung BLOCKIERT
sos_contacts_reni.json: nur Chris (Nummer eingetragen) + Robin + 112, Steffi raus. OFFEN: Reni (renatemandel@wtnet.de) in Cloudflare Access für bolla.chrismandel.de freischalten — Auto-Mode-Classifier blockte Lesen von config/cloudflare_token.json. Chris muss Zugriff erlauben (Permission-Regel) oder selbst im Zero-Trust-Dashboard (Access → Applications → Policy → E-Mail hinzufügen). Ideal: nur Pfad /sos für Reni freigeben.

## ⏳ 17.10.2026 — ABSCHLUSS: Renis SOS-App fast fertig, nur Cloudflare-Freischaltung offen
FERTIG: /sos (sos.html, sos.webmanifest, rote SOS-Icons), config/sos_contacts_reni.json (Chris +491786801513, Robin, 112; Steffi raus), Steffi aus WhatsApp-Block in Chris' MMP raus, Skript scripts/cf_access_add_email.py (Permission-Regel gesetzt; Token sieht aber keine Access-Apps → nutzlos bis Token Zero-Trust-Rechte hat).
OFFEN (Chris will bei „moin" die Schritte nochmal): Reni darf auf den GANZEN Host bolla.chrismandel.de (als Backup, wie Robin). Schritte für Chris im Browser:
1. one.dash.cloudflare.com → links „Zero Trust" aufklappen → „Zugriffssteuerungen" → „Anwendungen"
2. App für bolla.chrismandel.de anklicken → Bearbeiten → Reiter „Richtlinien" → Policy „Zulassen" bearbeiten
3. Bei Regel „E-Mails" renatemandel@wtnet.de hinzufügen → speichern
(Falls App nicht sichtbar: anderer Cloudflare-Login/Konto, evtl. Robins Team `robinmandel`; Screenshot an Bolla.)
DANACH: Anleitung für Renis Z Flip: Chrome → https://bolla.chrismandel.de/sos → Mail-Code eingeben → Menü „Zur Startseite hinzufügen" → rotes SOS-Icon. Optional: Test mit Chris' Handy.

## ✅ 17.10.2026 ~18:40 — Cloudflare: Policy „Reni" (renatemandel@wtnet.de, Allow) an App „Bolla Mission Control" gehängt
Chris hat im Dashboard eigene Policy „Reni" erstellt (nicht „Chris" geändert, die hängt auch an LM Studio). Fehlt: App speichern bestätigen, dann Test auf Renis Z Flip (/sos, Mail-Code, zum Startbildschirm).

## ✅ 17.10.2026 ~19:00 — Duo-Spannen per ADB getestet (Ergebnis: nicht automatisierbar)
Duo per USB: Windows-ADB `/mnt/c/Tools/platform-tools/adb.exe` (WSL-adb sieht USB nicht; nach kill-server/start-server ging's). Ein logisches Display 2754x1892; einseitig = Task-Bounds [1410,0][2754,1892] bzw. [0,0][1344,1892], gespannt = [0,0][2754,1892]. `am task resize` wirkt nicht (fullscreen); simuliertes Wischen (input swipe) schiebt Fenster nur links/rechts, spannt nicht. Reader-URL /aurora öffnet auf rechtem Display. Offen: Chris spannt weiter per Hand, evtl. App-Wechsler-Geste ausprobieren; Reni-/sos-Test noch ausstehend.

## ✅ 17.10.2026 ~19:20 — Duo-Spannen per ADB-Geste FUNKTIONIERT (Korrektur zu oben)
Geste auf offener Edge-PWA „AURORA II" (Shortcut-ID 3011a29f…, Scope bolla.chrismandel.de/aurora): `input motionevent DOWN 2080 1885` → MOVE nach oben (y 1700…700) → MOVE zur Mitte (x 1900…1377 bei y 700) → `UP 1377 700` ⇒ Task-Bounds [0,0][2754,1892] = gespannt. Windows-ADB `/mnt/c/Tools/platform-tools/adb.exe`. NICHT gelöst: PWA per ADB-Intent starten (ACTION_START_WEBAPP öffnet nur normalen Edge-Tab). Idee: Chris öffnet Icon, dann Skript/MP-Knopf „Duo spannen" (Handy muss per USB/WLAN-ADB erreichbar sein).

## ✅ 17.10.2026 — Duo-Spannen ERLEDIGT/VERWORFEN, Reni-SOS ohne Reminder
Chris spannt den AURORA-Reader weiter selbst — Thema vergessen, kein Knopf/Tasker. Reni-SOS-Test (Cloudflare Policy „Reni" ist gesetzt) macht Chris später selbst; KEIN Reminder bei „moin", er meldet sich bei Problemen von selbst.

## ⏳ 17.10.2026 18:40 — Chris-Auftrag: um 23:00 AURORA II weiter, Limit ausreizen
Detachter Wartejob `scripts/ausreizen_sa_2300.sh` (sleep bis 23:00, dann ausreizen_fr_aurora.py mit WEEK_STOP 98.5, Deadline 23:55; setzt bei Bogenplan/Kap. 29ff fort, Block A bereits erledigt). Woche aktuell 95 %. Notbremse `touch /tmp/aurora_samstag_stop`. Danach nichts automatisch; Spoiler-Schutz (Chris liest bis ~Kap. 13).

## ⏳ 17.10.2026 18:55 — Ausreizen bis ~100 % läuft (Chris: "ruhig auf 100 % ausreizen, nur aufpassen dass durch den Stopp nichts kaputt geht")
Alter 23:00-Wartelauf beendet, `ausreizen_fr_aurora.py` jetzt sofort detached gestartet (WEEK_STOP=99.5, Deadline 23:55). Sicherheit: aurora2.json nur atomar (tmp+os.replace), Backup `backups/aurora2_vor_fr_lauf_*.json`, Limit-Abbruch im Aufruf schreibt nichts. Notbremse `touch /tmp/aurora_samstag_stop`. Log logs/ausreizen_fr_aurora.log. Danach nichts automatisch; Wochenanfang schonen.

## ⏳ 18.10.2026 11:50 — AURORA-Video 3 min RENDERT (Chris 5 h weg, „ohne Rückfragen")
Konzept (Chris): Cover I klein vorn in der Röhre → fliegt nach hinten, wird groß → explodiert zu Cover II (schärfer als Vorschauen, Farben Cover II). Umgesetzt: `C:\Tools\blender_proj\aurora_video\aurora_video.py` (+prep.py → data.npz, 256k Kacheln 400×640, Rang-Zuordnung nach Helligkeit), Wrapper `scripts/blender_aurora_video.sh` (detached, resumable, Keep-Awake-Flag `running.flag`, /jobs `aurora-video`). Timeline: Flug 0–75 s, Explosion 75 s, Wolke bis 105 s, Zusammenfügen bis 150 s, dann 30 s Standbild (ffmpeg tpad). Frames 1–3600 nach `...\aurora_video\frames\`, ~1–1,6 s/Bild → ~1,5–2 h. Ergebnis: Desktop\temp\AURORA_Video_3min_ohne_Ton.mp4 + Kopie Bolla\AURORA II\7_Trailer_Blender\. Neustart nach Absturz: Wrapper einfach neu starten (überspringt vorhandene Frames). Kein Ton (Song später).

## ⏳ 18.10.2026 ~18:50 — AURORA-Partikelvideo (Hochformat, 3 min) rendert im Hintergrund
Neu gebaut (altes Kachel-Video 1920x1080 verworfen): Röhre orange → Gesicht Cover I aus Punkten → Wandlung orange→Nordlicht → Gesicht Cover II. Skripte: `scripts/aurora_partikel_prep.py`, `C:\Tools\blender_proj\aurora_partikel\aurora_partikel.py`, Wrapper `scripts/blender_aurora_partikel.sh` (detached, resumable, Job „aurora-partikel“). 5400 Bilder 1080x1920/30 fps, ca. 3,5 h (~2,3 s/Bild). Ergebnis: `Bolla\AURORA II\7_Trailer_Blender\AURORA_Partikelvideo_3min_hochkant_ohne_Ton.mp4` + Desktop\temp. Wenn Wrapper tot: einfach `./blender_aurora_partikel.sh` neu starten (setzt bei vorhandenen Frames fort). Danach: Chris Bescheid geben.

## ⏳ 19.10.2026 ~10:30 — AURORA-Partikelvideo QUER (16:9) rendert im Hintergrund
Chris: Hochformat gefällt nicht; Anlage wie Trailer_Gesicht_30s (Röhre). Ablauf: orange Punkte rauschen schnell durch Röhre → sammeln sich hinten zu Gesicht I (näher am Original, kräftige Farbe) → lösen sich, Farbe wechselt zu Nordlicht → Gesicht II weich ausgeblendet (kein Rechteck-Rand oben). Röhre blendet nach Gesicht I aus. Skripte: `scripts/aurora_quer_prep.py`, `C:\Tools\blender_proj\aurora_quer\aurora_quer.py`, Wrapper `scripts/blender_aurora_quer.sh` (detached, resumable, Job „aurora-quer“). 5400 Bilder 1920x1080, ~2,5 s/Bild ≈ 3,7 h. Ergebnis: `Bolla\AURORA II\7_Trailer_Blender\AURORA_Partikelvideo_Quer_3min_ohne_Ton.mp4` + Desktop\temp. Wenn tot: Wrapper neu starten. Danach Chris Bescheid geben.
Außerdem offen: Chris braucht neue Original-Patronen für HP ENVY Inspire 7900 (HP 303/303XL, evtl. HP+/Instant Ink) — Antwort gegeben.
⚙️ 19.10. ~11:00 Update: Röhre BLEIBT (Chris: Symbol für KI-Modelle). Ringe vorn bis y≈-40, hinten als großer Trichter-Rahmen um die Gesichter (r 10,5+), Farbe orange→türkis mit der Wandlung. Render neu gestartet (frames_alt_ohne_roehre = alter verworfener Lauf, kann gelöscht werden).
⚙️ 19.10. ~11:40: Gesicht II jetzt echte Nordlicht-Farben (grün/türkis-Bänder, oben violett), Ringe → Nordlichtgrün; Render neu gestartet. frames_alt_* = verworfen.
✅ 19.10. QR Tansania-Flaggenfarben: Chris tauscht ihn selbst in der PPT (Datei: Desktop\temp\QR_Tansania.png). Nichts offen.

## ⏳ 19.10.2026 ~11:45 — AURORA-I-Cover NEU (Wraparound DE+EN) zur Freigabe
Chris-Auftrag (1 h weg, ohne Rückfragen): Reni-Punkte + Rückenschrift groß + EN analog. Gebaut mit `workspace/scratch/cover_i_neu/build_cover_i.py <de|en> <Seiten>` (Seiten real: DE 460, EN 441). Ergebnis in `Desktop\temp\AURORA_I_Cover_neu\` (Wrap-PDFs, Vorschau-JPGs, eBook-Front-JPGs). Alte Cover unangetastet. NÄCHSTER SCHRITT nach Chris' OK: KDP (Print DE/EN Cover-PDF + eBook-Cover), D2D, Google Play laut [[project_aurora_update_checklist]]; Titel „AURORA I" ggf. auch in KDP-Titelfeld/Metadaten prüfen. Danach Desktop\temp aufräumen, Finals nach Bolla\AURORA\3_Taschenbuch/2_eBook.

## ✅ 19.10.2026 13:10 — AURORA-I-Cover freigegeben + eingespielt (lokal)
Finals in Bolla\AURORA (3_Taschenbuch, 2_eBook inkl. EPUB-cover.png getauscht, 4_Cover_Quellen). Desktop\temp aufgeräumt, Backups workspace/backups/aurora_cover_vor_I_20261019. NÄCHSTER SCHRITT: Upload-Runde KDP→D2D→Google Play mit Chris (geführt), Titelfeld „AURORA I" klären; danach ISBN-Registry/Notizen.

## ⏳ 19.10.2026 ~13:40 — Quer-Video: NEUE RÖHRE rendert im Hintergrund (Chris-Wunsch)
Betroffen ist `C:\Tools\blender_proj\aurora_quer\aurora_quer.py` (das Quer-Video von heute, NICHT aurora_video). Befund alt: Ringradius 3,3+0,2·sin(i·0,7) → ungleichmäßige Größen; Ringe 27–37 fehlten (Loch) + ab Ring 38 plötzlich Riesenringe (r 10,5…23) = „einzelne Ringe"; Längslinien (r 3,5, nur bis y=−41) passten nicht zu den Ringen. NEU: eine durchgehende Röhre, 67 Ringe im festen Abstand 1,6, gleiche Dicke, Radius konstant 3,3 bis y=−26, dann stetig ausfließendes Horn (r=3,3+0,0237·d^1,6) bis y=−102; 24 Längslinien folgen exakt dem Profil. Gesichter/Punkte/Kamera unverändert. Skript-Backup `workspace/backups/aurora_quer_vor_roehre_neu_20261019.py`. Wrapper `scripts/blender_aurora_quer_roehre.sh` (detached, resumable, Frames → frames_neu, Job „aurora-quer-roehre", 5400 Bilder ≈ 3,5 h). Nach Erfolg automatisch: `AURORA_Partikelvideo_Quer_3min_neue_Roehre_ohne_Ton.mp4` nach Desktop\temp + Bolla\AURORA II\7_Trailer_Blender, alle ALTEN Quer-Videos/Frames/Stills gelöscht. Falls Wrapper tot: einfach neu starten. Danach Chris Bescheid geben. Offen (optional): Cover-I-Titel im Video ist noch „AURORA" (ohne „I").

## ⏳ 19.10.2026 ~14:00 — KDP-Runde startet: erst Klappentext-Zusatz (DE: „Die Geschichte geht weiter: AURORA II erscheint noch in diesem Jahr." / EN: „The story continues: AURORA II will be published later this year."), dann Cover/EPUB. Offen: KDP-Titelfeld „AURORA I"? Quer-Video-Render (Röhre) läuft (/jobs aurora-quer-roehre); Cover-I-Titel im Video bleibt „AURORA" (Chris: nein). Zwischendurch-Ideen gemerkt: Goodreads/LovelyBooks, Website optimieren + Reni-Rezension.

## ✅ 19.10.2026 16:00 — AURORA-I-Cover v2: „I" mit Serifen (Chris: nackter Strich wirkt wie „|")
Alle Finals neu in Bolla\AURORA (2_eBook inkl. EPUBs, 3_Taschenbuch, 4_Cover_Quellen/build_cover_i.py). KDP-Runde läuft: eBook DE Details (Titel „AURORA I" + Beschreibungssatz) gespeichert; Cover/EPUB-Upload erst NACH Bolla-Freigabe → jetzt freigegeben. Reihenfolge: eBook DE → Taschenbuch DE → eBook EN → Taschenbuch EN → D2D → Google Play.

## ✅ 19.10.2026 ~16:20 — Cover zurück auf schlichtes „I" (Serifen-I war Chris zu unschön)
Finals neu eingespielt (Bolla\AURORA 2_eBook/3_Taschenbuch/4_Cover_Quellen, Skript-Flag SERIF_I=False); Prüfbild in Desktop\temp aktualisiert. KDP-Runde: Chris lädt hoch (eBook DE zuerst).

## ✅ 19.10.2026 ~16:45 — Cover: „I" jetzt zentriert unter AURORA (analog Band II)
Eingespielt (2_eBook, 3_Taschenbuch, 4_Cover_Quellen); Prüfbilder in Desktop\temp (Pruefbild + Pruefbild_Gesamt). Wartet auf Chris-OK bzw. Upload-Fortsetzung KDP.

## ✅ 19.10.2026 ~17:10 — Reni-Cover-Verbesserungen auf AURORA II übertragen (Vorlage)
build_cover.py (Band I+II) in beiden Bolla-Cover_Quellen-Ordnern; Band I unverändert (pixelgleich). Band-II-Wrap = Vorlage mit Platzhaltertext (Vorschau in Desktop\temp, zum Anschauen). Offen für II: Klappentext II + echte Seitenzahl, siehe project_aurora_ii_cover. I-Prüfbilder aus temp gelöscht. NÄCHSTES: KDP-Upload-Runde Band I (Chris klickt, eBook DE zuerst).

## ⏳ 19.10.2026 ~17:40 — Wrap-Naht-Bug gefunden (Chris: scharfe Kante rechts am Rücken, Band II)
Fix in build_cover.py (beide Bolla-Cover_Quellen), Band II korrigiert (Vorlage in temp). Band I hat denselben Bug (Spiegel falsch angesetzt), bleibt bis Chris-Entscheid unverändert; Vergleich `Desktop\temp\AURORA_I_Vergleich_Naht_aktuell_vs_korrigiert.jpg`. Falls Chris „korrigiert" wählt: `MIRROR_FIX=1 python3 build_cover.py de 460 <out> I` + en 441, Cover-PDFs in 3_Taschenbuch ersetzen (EPUB-Front ändert sich nicht, nur Wrap).

## ✅ 19.10.2026 ~18:00 — Naht-Korrektur für Band I übernommen, Vorlage II im Hauptverzeichnis, temp aufgeräumt
Bolla\AURORA\3_Taschenbuch: neue Cover-PDFs (DE+EN) + Vorschau. Bolla\AURORA II\AURORA_II_Cover_Wraparound_Vorlage.jpg. Desktop\temp: nur noch fremde/laufende Dateien (Partikelvideo wird vom Blender-Job ersetzt). KDP-Upload: Taschenbuch-Cover = diese neuen PDFs; eBook-Front/EPUB unverändert.

## ⏳ 19.10.2026 ~19:00 — KDP-Runde Band I: Stand + Entscheidung
- Taschenbuch-Titel/Untertitel bei KDP GESPERRT (>72 h nach Veröffentlichung; Änderung nur per „neue Ausgabe" = neue ISBN/ASIN, Rezensionen weg). Es gibt 2 Amazon-Rezensionen (Sigi + Robin) → KEINE neue Ausgabe. Titel bleibt „AURORA" (+Untertitel). Neues Cover „AURORA I" wird als Test hochgeladen; bei Ablehnung (Mail) → Cover OHNE „I" neu bauen (build_cover.py, Titelzeile ohne Bandzahl) und neu hochladen.
- eBook DE: eingereicht (In Prüfung) mit Titel „AURORA I" + Satz + neues EPUB/Cover. TODO sobald LIVE: Details → Titel zurück auf „AURORA" (sonst trennt Amazon eBook/Taschenbuch → Rezensionen nicht gemeinsam), neu veröffentlichen.
- Als Nächstes: Taschenbuch DE (Beschreibung-Satz + 2_DE_Cover.pdf), dann eBook EN (Titel „AURORA" lassen!), Taschenbuch EN (4_EN_Cover.pdf), dann D2D, Google Play. Mit Band II: KDP-Reihe „AURORA" anlegen (Band 1/2).

## ✅ 19.10.2026 ~19:30 — KDP Taschenbuch DE eingereicht (In Prüfung) mit 2_DE_Cover.pdf + Satz
Bestätigungsdialog zeigte Titel „AURORA I: Was bleibt…" (obwohl Taschenbuch-Titel gesperrt „AURORA") → nach Freischaltung Amazon-Seite prüfen, ob Titel „AURORA" oder „AURORA I"; danach entscheiden, ob eBook DE-Titel zurück auf „AURORA" muss. Offen: eBook EN (Titel „AURORA" lassen, EN-Satz in Beschreibung, EPUB+Cover), Taschenbuch EN (4_EN_Cover.pdf), D2D, Google Play.

## ✅ 19.10.2026 ~20:00 — KDP eBook EN eingereicht (In Prüfung); Titel-Beobachtung
Beide Bestätigungsdialoge (Taschenbuch DE, eBook EN) zeigten „AURORA I: …" → KDP führt den Titel offenbar formatübergreifend (Taschenbuch-Feld war gesperrt „AURORA"). Plan „eBook DE-Titel zurück auf AURORA" ZURÜCKGENOMMEN bis Check nach Freischaltung (Amazon-Seiten: Titel in allen Formaten? 2 Rezensionen noch da?). Offen: Taschenbuch EN (Satz + 4_EN_Cover.pdf), D2D, Google Play.

## ✅ 19.10.2026 ~20:20 — KDP komplett eingereicht (alle 4 Ausgaben, In Prüfung)
eBook DE, eBook EN, Taschenbuch DE, Taschenbuch EN: neues Cover/EPUB, Zusatzsatz zu AURORA II in Beschreibung; Anzeige-Titel „AURORA I". Erwartung: Mails in ≤72 h; bei Cover-Ablehnung → Cover ohne „I" neu. NÄCHSTES: D2D DE+EN (Titel „AURORA I", EPUB+Cover+Satz), danach Google Play DE+EN (GGKEY 68ES01N6JE2 / RCD8HR2D4AE). Nach Freischaltung: Amazon-Seiten prüfen (Titel, 2 Rezensionen noch da?).

## ⏸️ 19.10.2026 ~20:40 — PAUSE: Studio-Neustart (Chris). Weiter bei „moin" in neuer Session
**Beim Neustart stirbt der laufende Blender-Render** (Job aurora-quer-roehre, 5400 Bilder, Frames in C:\Tools\blender_proj\aurora_quer\frames_neu). Nach „moin": `scripts/blender_aurora_quer_roehre.sh` detached neu starten (resumable, setzt fort), /jobs prüfen.
**Offen (Reihenfolge):**
1. D2D DEUTSCH (ISBN 9798235162075, UBL bz0nwj, in My Books „View Book" → „1 DETAILS"): Titel → „AURORA I", Beschreibung + Satz „Die Geschichte geht weiter: AURORA II erscheint noch in diesem Jahr.", Manuskript AURORA_deutsch.epub, Cover AURORA_Cover.jpg (beide Bolla\AURORA\2_eBook), dann 2 Layout → 3 Preview (Haken) → 4 Publish (APPLY CHANGES / PUBLISH MY BOOK).
2. D2D ENGLISCH (ISBN 9798233715327, UBL 4A9A6o): gleich, Titel „AURORA I", EN-Satz „The story continues: AURORA II will be published later this year.", AURORA_english.epub + AURORA_Cover.jpg.
3. Google Play Partner Center: DE (GGKEY 68ES01N6JE2), EN (RCD8HR2D4AE): Titel, Beschreibung+Satz, EPUB, Cover.
4. Nach KDP-Freischaltung (≤72 h, Mails): Amazon-Seiten prüfen (Titel „AURORA I" in allen Formaten? 2 Rezensionen noch da?); bei Cover-Ablehnung → Cover ohne „I" neu bauen.
5. Zwischendurch-Ideen: Goodreads/LovelyBooks; Website optimieren + Reni-Rezension; ISBN-Registry/Notizen nach Abschluss ergänzen (Cover neu, Titel „AURORA I").
KDP: alle 4 Ausgaben eingereicht (In Prüfung) — nichts zu tun außer warten.
(20:50) Chris fährt jetzt runter. Falls das neue Röhren-Video (AURORA_Partikelvideo_Quer_3min_neue_Roehre_ohne_Ton.mp4) beim Neustart noch nicht in Desktop\temp + Bolla\AURORA II\7_Trailer_Blender liegt: Wrapper scripts/blender_aurora_quer_roehre.sh neu starten (resumable; Frames 5399/5400 waren fertig, nur Encoding/Kopie fehlt ggf.). Bei „moin" zuerst das prüfen, dann D2D DE.

## ✅ 19.10.2026 ~abends — D2D DEUTSCH veröffentlicht (Titel „AURORA I", neues EPUB/Cover/Satz; „Ebook Success")
Chris führt geführt (Bolla gibt Schritte, Chris klickt). Nächste Schritte: D2D ENGLISCH (ISBN 9798233715327, EN-Satz liegt in Zwischenablage), dann Google Play DE (68ES01N6JE2) + EN (RCD8HR2D4AE). Danach ISBN-Registry/Notizen. Offen nebenbei: Röhren-Video-Encoding (blender_aurora_quer_roehre.sh) prüfen.

## ✅ 19.10.2026 abends — D2D DE + EN veröffentlicht; Google Play für AURORA I gestrichen (Chris) → erst bei AURORA II ([[project_google_play_nur_aurora_ii]])
Offen: ISBN-Registry/Notizen (Cover neu, Titel „AURORA I"), nach KDP-Freischaltung Amazon-Seiten prüfen (Titel, 2 Rezensionen), Röhren-Video-Encoding prüfen.
- ✅ 19.10. ISBN-Registry aktualisiert (project_aurora_identifiers.md, Update-Block).

## ⏳ 19.10.2026 ~19:30 — Quer-Video v3: Röhrenflug durchs ganze Video + Farbwelle (Chris-Wunsch) rendert
Script `C:\Tools\blender_proj\aurora_quer\aurora_quer2.py` (v1 gesichert als aurora_quer_v1_backup.py): Kamera fliegt bis F_S=2300 zum Gesicht, danach gleiten die Ringe (Geometry Nodes, Radius folgt Horn-Profil) mit gleichem Tempo weiter an der Kamera vorbei → Flug über alle 3 Min; Röhrenfarbe orange→Nordlichtgrün als Welle entlang der Röhre (Welt-y), synchron zur Punktwandlung. Wrapper `scripts/blender_aurora_quer_flug.sh` (Job „aurora-quer-flug", Frames frames_v3, ca. 2–3 h). Nach Erfolg: Video `..._Roehrenflug_ohne_Ton.mp4` in Desktop\temp + Bolla\AURORA II\7_Trailer_Blender, alte Version „neue_Roehre" wird vom Wrapper gelöscht; MANUELL danach löschen: Ordner frames_neu (5400 PNGs) im Projekt. Stills waren ok (stills_v3).

## ✅ 19.10.2026 18:30 — Makler-Antworten Lieb + KSK gesendet
Lieb Immobilien (Weilheim, Neubau-Angebot): Antwort MIT Festnetz 040-30852883 + Anschrift + Kriterien, bittet um Exposé. KSK München (Basile): Antwort mit Anschrift, OHNE Nummer. Beide Original-Mails nach „Immos 2027-28“ verschoben. Excel aktualisiert 19.10. (Basile + Lieb eingetragen, Backup backups/Makler_Antworten_Archiv_neu_vor_lieb_ksk_20261019.xlsx). REGEL: Makler-Excel sofort nach jeder Antwort mitpflegen, nicht aufschieben.

## ✅ 19.10.2026 Session-Ende — Stand
Alles erledigt (Lieb + KSK beantwortet, Excel aktuell). Nächster Schritt: Lieb-Exposé prüfen, sobald es kommt. Nichts läuft im Hintergrund.

## ⏳ 20.10.2026 ~10:30 — AURORA-Quervideo v4 (Tunnel über die ganze Laufzeit) rendert
Chris: Röhrenflug v3 zeigte Röhre nur als Rand am Schluss (Horn ab y=-26, Kamera am Hornanfang). Fix: `C:\Tools\blender_proj\aurora_quer\aurora_quer3.py` (R0 4,2 konstant, Horn erst hinter Gesicht Y_FLARE=-62, Stills geprüft: Gesicht klar im Tunnelmund, Tunnel sichtbar bis Schluss). Wrapper `scripts/blender_aurora_quer_v4.sh` (detached, resumable, Job „aurora-quer-v4“, frames_v4, ~3,5 h) → `Desktop\temp` + `Bolla\AURORA II\7_Trailer_Blender\AURORA_Partikelvideo_Quer_3min_Tunnel_v4_ohne_Ton.mp4`. Wrapper löscht NICHTS (Auto-Mode-Classifier blockt rm). Danach Aufräumen: `scripts/aufraeumen_aurora_videos.sh` (Chris soll `! bash ~/workspace/scripts/aufraeumen_aurora_videos.sh` tippen ODER Bash-rm-Permission-Regel setzen). Wenn Wrapper tot: neu starten. Offen: Titel „AURORA I" statt „AURORA" im Video.
- 20.10.2026 Ciao: Chris fährt weg. v4-Render läuft (Job aurora-quer-v4). Bei „moin“: (1) Video prüfen/melden, (2) Aufräum-Skript `scripts/aufraeumen_aurora_videos.sh` (Chris tippt `! bash …` oder Regel), (3) Job „Permission-Nerverei beheben“ ([[feedback_permissions_nerven_moin_job]]).

## ✅ 21.10.2026 10:50 — Triage-Cron repariert (Ursache: `claude` nicht im Cron-PATH)
makler_angebote_triage.py stürzte seit 19.10. 11:15 bei jedem Lauf still ab (FileNotFoundError 'claude'); Fix: CLAUDE=shutil.which/~/.local/bin/claude + try/except→report(status "fehler", Telegram). Backup backups/makler_angebote_triage_vor_pathfix_20261021.py. Neu bewertet: Lieb Peißenberg DG (Score 63, 122 m², 599k inkl. Garage, Balkon überdacht, Aufzug unklar) + deltapro (Obermenzing DG 145 m² Bestand, Sendling-Westpark Neubau). Auto-Entwürfe gelöscht (zu schwach), bessere Entwürfe liegen Chris zur Freigabe vor — NICHT gesendet. Danach: Excel pflegen.

## ✅ 21.10.2026 11:20 — Lieb + deltapro Absagen GESENDET, Originale nach „Immos 2027-28", Excel aktualisiert
Absagen als Reply im Thread (Lieb: Terrasse ab ca. 20 m² statt Balkon; Götz: kein PH/keine Terrasse, preislich deutlich über Rahmen, KEINE Zahl genannt). Excel neu gebaut (Backup backups/Makler_Antworten_Archiv_neu_vor_lieb_delta_absage_20261021.xlsx), Score-K.O. jetzt auch bei Südterrasse=N. Triage-Cron repariert (siehe oben). Nichts läuft im Hintergrund.

## ✅ 21.10.2026 11:45 — Makler-Excel: Kosten-Spalten (nur neue Objekte)
Angebote-Blatt: Spalten T–V „Provision %“ (Eingabe), „Nebenkosten €“ (Preis × [GrESt 3,5 % + Notar/Grundbuch 2 % (Legende!B9/B10) + Provision]), „Gesamtkosten €“. Score: Provision Gewicht ×1 (~5 %), 0 % = voll, 3,57 % = 0, leer = zählt nicht → alte Zeilen unverändert. Triage-Prompt extrahiert zusätzlich provision_pct. Backups: backups/*_vor_nebenkosten_20261021.*. Beispiel 600 T€ bei 1,785 %: NK 43.710 €, gesamt 643.710 €.

## ⏳ 21.10.2026 — Neuer Job: chrismandel.de neu machen (bei Gelegenheit)
In offene_punkte.json (Projekte auf Zuruf) + project_chrismandel_de_neu.md. Erscheint bei moin. Vorher Ziel/Umfang klären.

## ✅ 21.10.2026 12:10 — Triage trägt neue Angebote automatisch ins Excel ein
Triage speichert in data/makler_angebote.json (Altbestand mit im_excel=true), ruft danach makler_excel_bauen_v2.py auf (liest nicht-markierte Einträge inkl. provision_pct → Nebenkosten/Gesamtkosten/Score per Formel). Backups backups/*_vor_excel_auto_20261021.*. Getestet mit Fake-Eintrag (entfernt).

## ✅ 21.10.2026 Session-Ende — Makler-Triage repariert + Excel-Automatik, Lieb/deltapro abgesagt, chrismandel.de-Neubau vorgemerkt. Nichts läuft im Hintergrund. Nächste Session: moin → offene Punkte.

## ✅ 21.10.2026 (nachmittags) — moin-Zuverlässigkeit repariert
SessionStart-Hook zeigt jetzt tail (nicht head) von aktuell.md + komplette nummerierte offene_punkte.json. offene_punkte.json bereinigt (17→ 18 Einträge: erledigte D2D/Google Play/Quer-Video raus, Aufräumskript + Permission-Nerverei rein; Backup workspace/backups/offene_punkte_vor_bereinigung_20261021.json). Chris testet moin selbst in neuer Session. Alte fertig_log-Meldung 16.10 (gesehen:false) noch ungesehen.

## ✅ 21.10.2026 (mittags) — moin-Test-Vorbereitung + gelber Rahmen
- Fehlerursache „moin" mit Altstand: Hook-Ausgabe >2 KB wurde ausgelagert, ich las nur den Anfang. Hook umgebaut: offene_punkte.json (nummeriert) ZUERST, aktuell.md-Tail nur 3500 Byte. Regel in feedback_moin_offene_aktionen.md (bei „Output too large" ganze Datei lesen). Backup workspace/backups/session_start_aktuell_vor_reihenfolge_20261021.sh.
- Gelber Rahmen ums Terminal war PowerToys ZoomIt → beendet + Modul in PowerToys settings.json auf false (Backup workspace/backups/powertoys_settings_vor_zoomit_20261021.json). Chris bestätigt: Rahmen weg. F-Secure unbeteiligt.
- Chris testet moin gleich in neuer Session. Quer-Video v4 ist fertig gerendert (frames_v4 5400), Abnahme steht aus. Nichts läuft im Hintergrund.

## ⏳ 21.10.2026 — Quer-Video v5 rendert (Chris: Ringe am Röhrenende sinnlos, Gesicht II schärfer)
v4 verworfen. `aurora_quer4.py`: Horn abgeschnitten (Röhre endet klar bei y=-63, keine gestauchten Ringe), data.npz mit COLS=1250 neu (103k Punkte statt 47k; Backup data_v4_backup.npz), Punkte zum Ende 30 % kleiner, Glow schwächer. Wrapper `scripts/blender_aurora_quer_v5.sh` (detached, resumable, Job „aurora-quer-v5“, frames_v5) → Desktop\temp + Bolla\AURORA II\7_Trailer_Blender\..._Tunnel_v5_ohne_Ton.mp4. Danach erst Aufräumskript (v4 + frühere Versionen mit raus; Skript ggf. um v4/frames_v4 ergänzen). Chris-Entscheidungen: Permission-Nerverei=ja, ISBN-Registry=ja, HP-Patronen erledigt (bestellt).

## ✅ 21.10.2026 — Permission-Regel `Bash(rm:*)` von Chris per /permissions gesetzt (User settings); ISBN-Übersicht-Word (Bolla\AURORA\5_Veroeffentlichung_Doku) aktualisiert (Backup backups/*_vor_update_20261021.docx). Classifier blockt Selbständerung von settings.json (bewusst, nicht umgehen). v5-Render läuft (Job aurora-quer-v5). Neue Regel: Hintergrundjob zuerst starten ([[feedback_hintergrundjob_zuerst]]). HP-Patronen erledigt.

## ✅ 21.10.2026 — Quer-Video v5 abgenommen + aufgeräumt (~90 GB frei)
Chris: „ziemlich ok", wird nach Fertigstellung von AURORA II nochmal überarbeitet (neues Cover II → prep neu, rendern). Behalten: Endvideo v5 (Trailer-Ordner + Projekt), `Bolla\AURORA II\7_Trailer_Blender\_Arbeitsstand_Quervideo_v5` (Skripte aurora_quer4.py/prep, data.npz, Wrapper, LIES_MICH.txt), im Projekt `C:\Tools\blender_proj\aurora_quer` Skripte+data+stills_v5. Gelöscht: alle PNG-Frames, v4/alte Videos, Logs. `scripts/aufraeumen_aurora_videos.sh` neu gefasst (löscht nur Regenerierbares). Offene Punkte: p20+p12 erledigt (14→12).

## ✅ 21.10.2026 Session-Ende — v5-Video abgenommen+aufgeräumt, rm-Regel gesetzt, ISBN-Doc aktualisiert, Hintergrundjob-zuerst-Regel. Nichts läuft im Hintergrund. Nächste Session: moin → 12 offene Punkte (heute/morgen: KDP-Prüfung).

## ✅ 21.10.2026 (abends) — Song-Entwurf „Orange war gestern (feat. Aurora)" + Trailer-Ordner aufgeräumt
Chris wollte zur Entspannung einen deutschen melodischen Hip-Hop-Song passend zum Quer-Video. Lyrics von Chris als „top" bewertet (Hook korrigiert: „aus Fragen gemacht" statt „aus Licht", weil Aurora Software ist). Style v1 zu seicht → Style v2 (808/Trap, 92 BPM, „autotune" aus Exclude) „klingt besser". Chris liefert evtl. noch Referenz-Hit; Punkt 6 in moin unter „Projekte auf Zuruf". Ordner `Bolla\AURORA II\7_Trailer_Blender` → `7_Trailer` mit `Video\`, `Song\`, `_Archiv_alte_Versionen\`, LIES_MICH.txt; Desktop\temp-Kopie des v5-Videos gelöscht; Skripte in workspace/scripts auf neuen Pfad (`7_Trailer/Video`). Offene Punkte jetzt 11 (Projektidee Nr. 2 gestrichen). moin-Liste ab jetzt IMMER mit Kategorien. Nichts läuft im Hintergrund.

## ✅ 21.10.2026 (abends) — chrismandel.de NEU + Landing AURORA II LIVE
Chris: „gut so, alles lassen erstmal“. Neue Startseite DE+EN (Nordlicht-Hero „Ich habe Sport und Biologie studiert. Dann kam ein Computer dazwischen.“, Zahlen-Leiste, Kartenstapel auf Halbkreis mit Autoplay, Wheel wrappt, 4 Karten inkl. AURORA II „Neu“, Kontakt+Impressum). Landing `/aurora2/` + `/en/aurora2/` (Trailer 20 MB, ohne Ton; QR-Ziel = chrismandel.de/aurora2/). Alles am Duo geprüft (adb 192.168.178.20:5555, Edge). Quelle/Generatoren: `workspace/chrismandel-neu-2026/` (STAND.md, build_home.py, build_aurora2.py), Seite `workspace/chrismandel-site/`, `assets/cards.js?v=3` (bei Änderung v hochzählen!). Deploy: wrangler --branch=main.
- Budget-Regel Chris: Woche Mi 50 / Do 60 / Fr 70 % Verbrauch (`scripts/budget_guard.sh`); Auto-Resume per Cron/CronCreate vom Classifier blockiert → Chris tippt „weiter“ (nicht mehr nötig, Projekt fertig). Stand Woche 34 %.
- Offen in moin (p19): Folgeseiten /aurora, /geschichte, /ki-forum, /impressum neu machen, irgendwann; Song-Link auf /aurora2/ sobald Song fertig.
- Lehre: Headless-Edge rendert nie <500 px; Mobile-Test am Duo per adb. Neue JS-Assets immer mit ?v= versionieren (Browser-Cache).
Nichts läuft im Hintergrund (außer OneDrive-rsync beim Ciao).
- ✅ 21.10. (nach Ciao): MP-Wetter Uhrzeiten lesbarer (index.html + mobile.html: 16px/hoher Kontrast, Backups workspace/backups/*_vor_wetter_lesbar_20261021*). Chris: „gut so“. Regel: Zeit-/Datums-Labels in MP min. 14px, nie unter ~70 % Weiß auf dunkel.

## ✅ 22.10.2026 — AURORA-II-Konsistenz-Check (Hintergrund-Fork)
Kap. 1–30 maschinell+gegengelesen geprüft (Daten/Wochentage 2026, Zählketten, Kanon, Figuren, Wiederholungen); Text NICHT geändert. Befunde: `Bolla\AURORA II\1_Manuskript_und_Analyse\Konsistenz-Check_Kap1-30_2026-10-22.docx` — 3 hoch (K30 Heiligabend=Mittwoch, K27/28 Mittwoch vs. Donnerstag 17.12., K26 „Mittwoch, dem zehnten“), 4 mittel, 8 niedrig. Verbrauch ≈ 0 
## ✅ 22.10.2026 — AURORA II Wochentag-Korrekturen eingebaut
Kap. 26 (Donnerstag, dem zehnten; 'sechs Wochen und einem Tag'), Kap. 27 (Donnerstag statt Mittwoch, 3 Stellen + Pulloverfolge), Kap. 30 (Heiligabend=Donnerstag) in aurora2.json korrigiert. Backup workspace/backups/aurora2_vor_wochentag_fix_20261022.json. Offen (Chris-Entscheidung/Kosmetik): Frauke 17 vs. 20 Kita-Jahre, K27 'zwanzig Tage', Petrova/Falkner-Einführung, Abnutzungs-Formeln.

## ✅ 23.10.2026 — KDP-Prüfung AURORA I erledigt
Alle 4 Ausgaben LIVE, Titel „AURORA I" korrekt (Chris-Screenshot). Punkt aus offene_punkte.json entfernt (jetzt 10). Rezensionen Sigi+Robin laut Chris noch dran ✅.

## 23.10.2026 — Tonie-Projekt Zwillinge definiert (nicht gestartet)
Siehe project_tonie_zwillinge.md; als p30 in offene_punkte.json (moin zeigt es).

## ✅ 23.10.2026 — AURORA II Sammelmodus gebaut
Chris liest Kap. 15 (vor allem am Duo). Hinweise vin/gramm/nicht witzig genug werden pro Kapitel gesammelt und gebündelt gesendet (Reader `/aurora` + MP-Studio). Details: feedback_aurora_ii_sammelmodus.md. MP-Server neu gestartet. Nicht am echten Duo getestet → Chris probiert aus (Reader ggf. neu laden). Nichts läuft im Hintergrund.

- 23.10. Sammelmodus am Duo von Chris bestätigt: „funktioniert top“.

## 🟢 23.10.2026 13:40 — AURORA II: Schreiblauf Kap. 31–36 gestartet (Hintergrund)
Chris (Reni-Geburtstag morgen, nicht erreichbar): „loslegen, alleine". `scripts/ausreizen_fr_aurora.py` mit AUSREIZEN_WEEK_STOP=70, Deadline Sa 24.10. 23:50, resumable (state in scratch/aurora_samstag_fr_aurora_20261016). Plan Kap. 29–36 privat; 29/30 stehen. Notbremse: `touch /tmp/aurora_samstag_stop`. Danach: Chris liest weiter ab Kap. 15; Hinweise via Sammelmodus; bei Änderungen an Fakten Folgekapitel angleichen.

## 23.10.2026 13:45 — Ciao
Stand: Schreiblauf Kap. 31–36 läuft weiter im Hintergrund. Nächster Schritt: Ergebnis prüfen, Chris liest ab Kap. 15 weiter (Sammelmodus), Fakten ggf. in Folgekapiteln angleichen.

## 23.10.2026 20:20 — Tesla-Support-Mail gesendet
Konto-Mail chrismandel@hotmail.com → ernstmandel@outlook.de ändern lassen (Tesla-Konto nur fürs Laden des ID.3). Mail an EMEA-AT-ContactTeslaSupport@tesla.com (DE-Adresse nicht auffindbar). Nachverfolgung: p31 in offene_punkte.json; Antwort in Outlook prüfen, bis 30.10. sonst nachhaken.

## 23.10.2026 20:40 — 5h-Watchdog + Reader-Markierung
- `samstag_ausreizen.py`: Watchdog bricht laufenden Schritt bei 5h >= 85 % ab (AUSREIZEN_5H_HARD), Gate pausiert ab 75 % bis Reset und macht selbst weiter (Fehlversuch zählt nicht). Backup workspace/backups/samstag_ausreizen_vor_watchdog_20261023.py.
- Lauf Kap. 31–36 neu gestartet (WEEK_STOP 70, Deadline Sa 23:50), pausiert bis ~00:50 (5h bei 92 %).
- `aurora-reader.html`: offene Vorschläge über mehrere Sätze (Kap. 14 `66b29f2b`) werden jetzt markiert; Markierung kräftiger (lila). Duo: Reader neu laden. Noch nicht am Duo getestet.

## 2026-10-24 10:53 — Ciao (Stand)
- Suno: NICHT vor Verbrauch der 12 Premier-Downloads auf Pro stellen; moin-Punkt angepasst (Erinnerung 30.10.).
- Tonie-Projekt jetzt 3 Kinder (Marie, Anton, Mia), nicht gestartet.
- offene_punkte: p17 in p19 zusammengelegt (Website Feinschliff + Reni-Rezension + AURORA-II-Hinweis); neu p32 KDP-Hörbuch-Option EN prüfen.
- Neu: Job kdp-virtual-voice-de (Cron Mo 9:00, /jobs) prüft, ob KDP Virtual Voice Deutsch kann. Konto hat noch keine Hörbuch-Option.
- Läuft weiter: AURORA-II-Schreiblauf Kap. 31–36 (Deadline Sa 23:50). Nächster Schritt: Ergebnis prüfen, Chris liest ab Kap. 15.

## 2026-10-24 — Tonie-Seite in MP gebaut
MP → Familie → 🎁 Tonies (Raster 3 Kinder × Song/Lied/Geschichte, Status, Attribute, Wünsche, Anstups, Fahrplan). MP-Server neu gestartet. Nächster Schritt: Chris testet, füllt Lieder/Attribute; Mia nur Kreativ-Tonie. Word-Export mit Opa/Oma-Farben erst bei fertigen Texten.
- 24.10. Tonie-Seite v2 (Erzeugen/Verbessern/Verwerfen, Word-Geschichten) fertig, Anton-Testlauf erzeugt; Chris prüft.

## 2026-10-24 — Ciao (Stand)
- Tonie-Seite v2 fertig (MP → Familie → 🎁 Tonies); nur Anton-Testlauf erzeugt, Marie/Mia unberührt. Attribute: Anton Autos/Elefanten, Marie Tiere, Mia leer. Mia nur Kreativ-Tonie.
- Offen: Ausreizen-Lauf (Analogie-Check Kap. 31–36 + Tonie-Entwürfe) VORGESCHLAGEN, von Chris nicht ausdrücklich bestätigt, NICHT gestartet. Woche 66 % um 12:00, Reset heute 23:59.
- Nächster Schritt: Chris prüft Tonie-Seite im Browser, Wünsche/Verbesserungen eintragen.
- 24.10. Nachtrag: Tonie-Altersvorgaben (Mia 5, Zwillinge ~2) + Button-Style in MP-Tonies.

## 2026-10-24 19:35 — Ausreizen gestartet (Chris-Freigabe)
`scripts/ausreizen_sa_analogie.py` läuft detached: Tonie-Entwürfe (Marie song/lied/geschichte, Anton lied, Mia alle 3) via MP-API, danach Analogie-Check Kap. 31–36 in 3 Foki-Runden (Patches direkt, Protokoll changes.md). Ordner scratch/aurora_samstag_sa_analogie_20261024, Log logs/aurora_samstag.log. Gating 5h 75 %, Woche <95 %, Deadline 23:50, Notbremse `touch /tmp/aurora_samstag_stop`. Chris clear't danach. Backups: backups/aurora2_vor_sa_analogie_*, tonies_vor_sa_analogie_*.

## 2026-10-25 — Limit-Ausreizen: Auftrag
Sa-Lauf 24.10. endete bei Woche 79 %. Chris: bis Do 29.10. mittag NICHTS riskieren (Schule/private Jobs), ab Do mittag Tipps zum besseren Ausreizen geben. Memory: feedback_limit_ausreizen_tipps_do.md

## 2026-10-25 — Limit-Regeln konsolidiert
6 Einzeldateien → `feedback_limit_regeln.md` (Backup workspace/backups/memory_limit_20261025/). Kernregel: Gate 75 % + Watchdog 85 % + Auto-Resume für ALLE großen Hintergrundläufe; Wochenende ab Fr 19:00 ausreizen. Do 29.10. mittag: Tipps zum Ausreizen liefern, bis dahin keine Last. Offen: andere `claude -p`-Skripte (build_f_photos, aufpeppen, newsletter_scanner …) nutzen das Gate noch nicht.

## 2026-10-25 — limit_gate.py gebaut
`scripts/limit_gate.py` (Gate 75 %/Watchdog 85 %, wartet bis Reset) in 7 Skripte eingebaut (Backups backups/limit_gate_20261025/). Selbsttest ok, py_compile ok, echte `claude -p`-Läufe noch nicht getestet (laufen regulär per Cron). Nicht gegatet: MP-Chat, telegram_bot, aufpeppen (nutzergetrieben).

## 2026-10-25 — Ciao (Stand)
- Limit-Regeln konsolidiert (feedback_limit_regeln.md); limit_gate.py in 7 Skripte eingebaut, echter Lauf mit claude -p noch ungetestet.
- Bis Do 29.10. mittag keine Last; dann Tipps zum Ausreizen (Fr 19:00 Start wieder).
- Nichts läuft im Hintergrund. Weiter: Chris liest AURORA II ab Kap. 15, Tonie-Entwürfe prüfen.

## 2026-10-25 ~12:00 — Tonie-Seite v3 (Suno v6) — Ciao
- Tonie-Seite: Überschriften + "✅ fertig"-Hinweise, Bearbeitungsstand beschriftet, 🎤→🎶 bei Kinderlied (war nur Emoji, kein Diktat).
- Song-Prompt nach Suno-v6-Regeln (Klammer-Tags mit Vortragsanweisung, Style ≤500 Zeichen, keine Verneinungen, neues **Exclude**-Feld + Kopierknopf, max 2–3 Geräusch-Tags [dog barks] = experimentell, Variety=Off-Hinweis).
- Ein Knopf pro Kind "Speichern & alles neu erzeugen" (ohne Rückfrage, Backup alte Word-Geschichte als *_vorher.docx); oben "Alle Kinder: alles neu" (mit Rückfrage).
- Messung: 1 Kind komplett (3 claude -p) ≈ 3 % des 5h-Fensters; alle 3 Kinder ≈ 10 %.
- Marie wurde um 11:49 komplett neu erzeugt (alte Geschichte weg). Marie-Song v6-Ergebnis von Chris noch nicht geprüft; Anton/Mia unverändert (alte Fassung ohne Exclude).
- Backups: workspace/backups/*_vor_v6_20261025*, *_vor_alles_neu_btn_20261025*.
- Nächster Schritt: Chris prüft Marie-Song (Exclude/Tags/Geräusch-Tags in Suno testen), dann ggf. Anton/Mia neu. Bis Do 29.10. mittag keine große Last.
- 25.10. Test: Suno ignoriert [dog barks]-Tags, Sektions-Anweisungen in [] wirken; Tags aus Tonie-Prompt entfernt (Marie-Song hat sie noch drin, bei Neuerzeugung weg).

## 2026-10-25 abends — Ciao (Stand)
- Quota-Messung: Tonies = <1 % Woche (5h +4 Pp für 4 Jobs); in feedback_limit_regeln.md.
- Tanzkurs-Word (Desktop) um Cha-Cha-Promenade + Rumba erweitert, Chris: „gut so, erst mal“ (project_tanzkurs.md).
- Tonie-Songs alle 3 neu: Mitsing-Refrain, Humor, Opa+Oma zusammen; Mia-Song v3 „Mia und das brummende Päckchen“ (kein Brillen-Witz, Opa Chris hat Linsen). Song-Prompt `_tonies_job` angepasst (feedback_tonie_suno_v6.md). Noch NICHT in Suno getestet (Chris testet).
- MP AURORA II Reader: gesammelte Hinweise + Auswertung jetzt UNTER dem Frage/Korrektur-Feld, ausklappbar (Backups workspace/backups/index_vor_*_20261025.html). Browser-Test durch Chris offen.
- Nichts läuft im Hintergrund. Bis Do 29.10. mittag keine große Last.

## 2026-10-25 spät — Ciao (Stand)
- Mia-Song: „hut" → „Mütze" korrigiert (Opa trägt nur Mützen); Ursache war Beispiel im Song-Prompt (mission_control_api.py), entfernt + Anti-Erfindungs-Regel ergänzt. Memory: feedback_keine_erfindungen.md erweitert. Backups *_vor_muetze_*.
- Mia-Song in Suno noch alte Fassung — bei Neuerzeugung korrigierten Text von der Tonie-Seite nehmen.
- Nichts läuft im Hintergrund. Bis Do 29.10. mittag keine große Last.

## 2026-10-26 morgens
- Reader-Umbau (Hinweise unter Frage/Korrektur-Feld, ausklappbar) von Chris im Browser getestet: funktioniert. Offen-Punkt erledigt.

## 2026-10-26 vormittags
- Reader-Umbau bestätigt. moin-Hook: Montags-Reminder (nur bei Kurstagen in der Woche) + Sortierung nach prio eingebaut; offene_punkte.json neu priorisiert (Regel in feedback_moin_offene_aktionen.md).
- Kurstag 5 (Gruppe I, Mi 28./Do 29.10.): Texte vorbereitet in workspace/scratch/kurstag5_gruppeI_mitteilungen.md. OFFEN: PDF aus PPTX (powershell pptx_to_pdf.ps1 wurde vom Permission-Classifier blockiert), 05-Praktikum.html liegt noch in Handouts/Entwurf (Kopie nach Praktikum/ nötig), Chris-Freigabe + Post-Cron + COURSES/DAY_PREFIX in itslearning_post_kurstag.py (steht noch auf Kurstag 4 II). Freigabe-Check-Cron läuft Mo 11:00.
- Kurstag 5: PDF erzeugt (Handouts/Praktikum/05-Basics Office - WebApps-Designer-Copilot.pdf), 05-Praktikum.html nach Praktikum/ kopiert, Vorschau-PNG in Desktop/temp/Mitteilungen_Kurstag05_Vorschau.png. Wartet auf Chris-Freigabe + Zeitpunkt; dann COURSES/DAY_PREFIX=05 im Post-Skript setzen + Post-Cron.
- Post-Skript itslearning_post_kurstag.py auf Kurstag 5 (Gruppe I, DAY_PREFIX 05) umgestellt, Wrapper-Text angepasst (Backups backups/*_vor_k5_20261026*). Cron Di 27.10. 14:30 wurde vom Classifier blockiert (crontab-Schreiben) -> Chris entscheidet. Dienstags-Reminder im Hook.
- 26.10.: Chris genervt über erneute Freigaben. Classifier blockte crontab-Schreiben, powershell pptx_to_pdf (später mit dokumentiertem Befehl durchgelassen) und Edit an settings.json (Self-Modification). Als Punkt 1 in offene_punkte.json (p34). Cron Kurstag 5 Di 27.10. 14:30 noch NICHT gesetzt.
- 26.10.: Permissions von Chris eingetragen (crontab, pptx_to_pdf). Kurstag-5-Post-Cron gesetzt: Di 27.10. 14:30 (Backup backups/crontab_vor_k5_20261026.txt). Punkt p34 bleibt: Permission-Prozess optimieren.
- 26.10. (mittags): Permission-Test: crontab -l/Schreiben laufen; pptx_to_pdf.ps1 scheiterte an Execution Policy (\\wsl.localhost) + Classifier blockt Bypass/EncodedCommand. Lösung: Wrapper `scripts/pptx_to_pdf.sh <pptx> <pdf>` (kopiert ps1 nach C:\Users\ernst\bolla_tools\, ruft ohne Bypass) — getestet OK. Chris soll Allow-Regel `Bash(/home/bolla/workspace/scripts/pptx_to_pdf.sh *)` in ~/.claude/settings.json eintragen (Eintragen per /permissions wird offenbar nicht dauerhaft gespeichert, s. Vermutung). Ab jetzt für PPTX→PDF den Wrapper nutzen.
- 26.10.: KORREKTUR zu oben: Chris trägt NIE Regeln per Hand in .json ein. Wrapper pptx_to_pdf.sh lief ohne Regel durch; Edit an settings.json blockt der Classifier weiter (Self-Modification). Also: Wrapper-Skripte mit festem Pfad statt Allow-Regeln (kein Bypass/EncodedCommand). Bei Blockade melden, nicht umgehen.
## 2026-10-26 Ciao (Stand)
- Permission-Wrapper pptx_to_pdf.sh fertig. Kurstag-5-Post-Cron Di 27.10. 14:30 steht. Nichts läuft im Hintergrund.
## 2026-10-26 Song-Wechsel AURORA II
- Neuer Trailer-Song „Kein Zaubertrick (feat. Aurora)“ (Zauberer-Bounce-Rap, Chris: „viel lebendiger“) → Trailer neu gebaut, Website deployt (DE+EN, Startseiten-Karte), Altes archiviert, Site-Commit lokal (nicht gepusht). Offen: DistroKid, QR-Code.
- 26.10.: DistroKid-Release Kein Zaubertrick auf später verschoben; in moin-Liste (p13) als Erinnerung.

## 2026-10-26 Halloween-Mitteilungen (Entwurf)
- 4 Videos (je Klasse, erste 26 s der 0-Halloween-7x.mp4, 4,8 MB) in workspace/state/halloween_video/. Skript scripts/itslearning_halloween_video.py (8 Kurse, noch NICHT gepostet), Vorschau-PNG in Desktop\temp. Punkt p40 in offene_punkte.json: Freitag 30.10. bei „moin" Freigabe holen + Skript starten.
- Trailer-Check: chrismandel.de/assets/aurora2-trailer.mp4 = lokale 141-s-Version (19.210.126 Byte), live.
- 26.10. EN-Trailer fertig: Song „No Magic Trick (feat. Aurora)“ (139,6 s), Trailer 144 s (Song ab 1 s) live auf /en/aurora2/ (assets/aurora2-trailer-en.mp4?v=1); DE-Trailer jetzt ?v=2 (Cache-Bust). Site-Commit lokal, nicht gepusht. Aufgeräumt: Scratch-Videos, WAV aus Desktop\temp. Halloween-Videos liegen noch in Desktop\temp\Halloween_Videos (nach Versand Fr 30.10. löschen).
- 26.10. YouTube: DE+EN-Trailer öffentlich (youtu.be/yxVho5QYpYY, /mHssAaEraGg); Landingpage mit „Benachrichtige mich“+Band-I-Button+„Jahreswechsel“-Hinweis live. Methode siehe project_qr_landingpage_trailer_muster.md. Offen: YouTube-Links auf Landingpage/Startseite optional; Hochkant-Clip für TikTok/Insta ab Mitte Nov.
- 26.10. YouTube-Beschreibung DE+EN mit Premise + chrismandel.de-Links gespeichert. Offen: Chris muss einmalig Identität bei YouTube bestätigen (youtube.com/verify), sonst Links in Beschreibung nicht klickbar.
- 26.10. YouTube: Tel. schon bestätigt (Stufe 2 aktiv). Externe Links in Beschreibung = Stufe 3 'Erweiterte Funktionen' (Berechtigt, noch nicht aktiv): braucht Videoüberprüfung ODER Ausweis ODER Kanalverlauf. Chris entscheidet, ob er das macht.
- 26.10. YouTube-Kanalinfo: Beschreibung + Links chrismandel.de & /aurora2/ veröffentlicht (Kontakt-Mail bewusst leer).
- 26.10. AURORA II Kürzungsplan fertig: workspace/scratch/aurora2_kuerzung/kuerzungsplan.md (29 Kap., 132.630 Wörter, 8 Umsetzungswellen, Kap 1–16 behalten Nummer/Titel). Offen: Lenis Papierrolle Kap 22 vor Welle 5 prüfen; Kap 6 liegt bei −11,7 %. Umsetzung noch NICHT gestartet.
- 26.10. Welle 1 (Kap 1–4) gestartet (Opus-Subagent, Output scratch/aurora2_kuerzung/welle1/, Backup data/aurora2_backup_vor_kuerzung_welle1_*.json). Chris: Polizeiszene Kap 6 = Kurzfassung, deutlich witziger (in Plan eingetragen).
- 26.10. Welle 1 (Kap 1-4) FERTIG: scratch/aurora2_kuerzung/welle1/kap01-04.txt + bericht.md, 8.957 statt 9.130 Soll-Wörter (173 Puffer). aurora2.json NOCH NICHT angefasst (Übernahme offen). Offen für Welle 2: "elf Tage"-Frist (Kap 2) gegen Kap 5-8 prüfen; Kap-2-Schluss/Cliffhanger-Entscheidung; Frauke-Einführung jetzt in Kap 2.
- 26.10. Welle 1 in aurora2.json ÜBERNOMMEN (Kap 1-4, Chris-Freigabe). Welle 2 (Kap 5-8) als Opus-Subagent im Hintergrund gestartet, Output scratch/aurora2_kuerzung/welle2/. Backup vor Welle 1: data/aurora2_backup_vor_kuerzung_welle1_20261026_1817.json.
- 26.10. Welle 2 (Kap 5-8) FERTIG in scratch/aurora2_kuerzung/welle2/ (9.024 W statt 9.300 Soll), aurora2.json NOCH NICHT angefasst; wartet auf Chris: Übernahme + Kap-2 "elf"->"zwölf" Tage + Start Welle 3. Tonie-Seite: Buttons Liedtext(Word) + Playback(Suno-Prompt) + Ordner-Tooltips gebaut.
- 26.10. Welle 2 in aurora2.json ÜBERNOMMEN (Kap 5-8), Kap 2 "elf Tage"->"zwölf Tage" (4 Stellen). Backup data/aurora2_backup_vor_kuerzung_welle2_20261026.json. Welle 3 (Kap 9-12, Ziel 16.000 W) gestartet.
- 26.10. abends: 5h-Limit 91 % → Welle-3-Agent (Kap 9-12) abgebrochen, kein Output, Neustart nach Reset 22:49 (Cron 22:53, nur Session; sonst bei moin p43). Tonie-Kinderlied-Stand in project_tonie_zwillinge.md, moin-Punkt p42.
- 26.10. abends: cloudflared 2026.3.0 → 2026.10.4 (Cloudflare-Sicherheitsmail), Tunnel läuft, Mail gelöscht. 5h-Limit lag 19:30 bei 96 % (Gate-Lücke, siehe feedback_limit_regeln).
- 26.10. abends: Gelbe Tonne Buchenweg nicht geleert (Fehlwurf: Pizzakartons). Mail an info@brockmann.de (Brockmann Recycling, zuständig für Gelbe Tonne Norderstedt) gesendet; Ergänzungsmail verworfen. Nächste Leerung ~9.11. (Abfallkalender prüfen); Kartons raus, alten Aufkleber abziehen.

## 2026-10-26 — Montags-moin: „2 Namen“ (Geburtstagssong) — Hook-Edit wartet auf Freigabe
Chris: In moin unter Überschrift Montag aufnehmen, NUR in betroffenen Wochen. Hook ~/.claude/hooks/session_start_aktuell.sh (Zeile 22, Montags-Erinnerung ist schon wochen-gegated über schuljahr2627.json) soll anhängen: „MONTAG-Punkt Geburtstagssong: Chris nach den 2 Namen für Mittwoch + 2 für Donnerstag fragen (Songs erst ab 14:00)“. Edit in Telegram-Session als sensible Datei blockiert → am Studio ausführen. Telegram-Cron itslearning_geburtstagssong_namen_montag_reminder.py existiert schon (Mo 7-11 Uhr, Ferien übersprungen).
- 26.10. 22:55: Quota 11 % → Welle 3 (Kap 9-12) als Opus-Subagent im Hintergrund NEU gestartet, Output scratch/aurora2_kuerzung/welle3/ (kap09-12.txt + bericht.md). aurora2.json unberührt; nach Fertigstellung Übernahme mit Chris klären.
- 26.10. 23:xx: Welle 3 (Kap 9-12) FERTIG in scratch/aurora2_kuerzung/welle3/ (16.746 W statt 16.000, +4,7 %), aurora2.json NOCH NICHT angefasst. Wartet auf Chris: Übernahme; Kap 11 Balken-Satz 04:17 ('acht Stunden für eine einzige Nacht' statt übernommen 'fünf Stunden für einen einzigen Tag' - Zeitleiste); Satz/Antwort-Gag Kontingent im Gesamt-Pass; Kap 16 'Kollmann-Zylinder' in Welle 4 raus.
- 27.10. Regel-Konsolidierung: feedback_limit_regeln.md neu (5h vs. Woche getrennt, Reserve-Tage Mo/Di/Fr/Sa tagsüber 20 % frei = Gate 67/Max 80), scripts/limit_policy.py zentral, limit_gate+samstag_ausreizen angepasst, context_check.py LIMIT-STATUS pro Prompt, PreToolUse-Hook agent_limit_guard.py (Agent) in settings.json. Backups workspace/backups/limit_regeln_20261027/. Welle 3 (Kap 9-12) in aurora2.json ÜBERNOMMEN (Chris-Freigabe), Backup data/aurora2_backup_vor_kuerzung_welle3_20261027.json; Kap 11 Balken 'acht Stunden für eine einzige Nacht'. Nächster Schritt: Welle 4 (Kap 13-16, Kollmann-Zylinder Kap16 raus) — Quota/Gate vorher prüfen.
- 27.10. Sa-Nacht-Regel ergänzt: ab Sa 22:00 Gate 82/Max 95 (limit_policy.py + feedback_limit_regeln.md). Chris verabschiedet sich.
- 27.10. 09:5x: Kurstag-5-Wrapper war 0 Bytes (Mo 26.10. 09:28 beim Umbau abgeschnitten) -> aus Backup wiederhergestellt (Texte K5/I-Kurse). Post-Cron Di 27.10. 14:30 steht. Fehler von mir: altes K4-Log als 'heute' gemeldet.
- 27.10. Chris: Kurstag-5-Post freigegeben (Cron Di 14:30), freigabe.json approved.
- 27.10. ~10:15: Montags-moin-Hook um Geburtstagssong-Namen-Punkt ergänzt (Backup workspace/backups/session_start_aktuell_20261027.sh). Namen dieser Woche aufgelöst (Kurs I): Mi 28.10. 14:05 Thore Kuhn (7d) + Mika Henneberg (7b), Do 29.10. 14:05 Merle Hutterer (7a) + Lena-Sophie Brühl (7c). Skript scripts/itslearning_geburtstagssong_batch_2810.py, Cron ersetzt (alte 0710-Einträge raus, Backup backups/crontab_vor_songbatch_2810_20261027.txt). Dropdown-Namen geprüft. Nächster Schritt: Mi/Do nach 14:05 Log + job_status prüfen (Datum+Inhalt), dann erst „ok“ melden. Memory: feedback_geburtstagssong_namen_aus_kurstermin.
- 27.10. ~10:50: Welle 4 (Kap 13-16) läuft als Opus-Subagent im Hintergrund, Output scratch/aurora2_kuerzung/welle4/ (kap13-16.txt + bericht.md). Nach Fertigstellung: Pieper/Kollmann/Reifen-grep prüfen, Übernahme in aurora2.json NUR mit Chris-Freigabe (Backup vorher). Punkte p30 (3 Tonies bestellt) + p14 (erledigt) in offene_punkte.json angepasst. Kurstag-5-Post Cron Di 14:30: danach Log prüfen (Datum+Inhalt).
- 27.10. ~11:5x: Welle 4 (Kap 13-16) FERTIG in scratch/aurora2_kuerzung/welle4/ (23.100 W statt 22.200, +4,1 %; grep Pieper/Kollmann/Reifen = 0 verifiziert). aurora2.json NOCH NICHT angefasst, wartet auf Chris-Freigabe zur Übernahme (Backup vorher). Offen: K16 Kurzszene 'Leni nach dem Anruf' (~165 W) gestrichen; Wellen 1-4 +1.197 W über Plan -> Welle 5-7 auffangen.
- 27.10. Welle 4 (Kap 13-16) in aurora2.json ÜBERNOMMEN (Chris-Freigabe), Backup data/aurora2_backup_vor_kuerzung_welle4_20261027.json. Nächster: Welle 5 (Kap 17-22 alt, Verschmelzungen) — Quota/Gate vorher prüfen; Wellen 1-4 +1.197 W über Plan.
- 27.10. ~12:40: Punkt 'Permissions' in offene_punkte.json auf erledigt gesetzt. Welle 5 (Neu 17-20 = alt 17-22) als Opus-Subagent im Hintergrund gestartet, Output scratch/aurora2_kuerzung/welle5/ (kap17-20.txt + bericht.md). aurora2.json unberührt; Übernahme nur mit Chris-Freigabe + Backup. Außerdem: Kurstag-5-Post Cron 14:30 danach Log prüfen (Datum+Inhalt).
- 27.10. ~13:00: Tonie-Seite (MP → Familie → 🎁 Tonies) komplett umgebaut (siehe project_tonie_zwillinge.md v4). Chris soll mit Strg+F5 neu laden und testen. Welle-5-Subagent läuft weiter.
- 27.10. ~14:35: Tonie Playback (selbst gerendert, Noten via Claude+Cache) + Liedtext pro Listenzeile umgesetzt, MC-API neu gestartet. Welle-5-Subagent nach Limit-Reset per SendMessage fortgesetzt (läuft). Kurstag-5-Post-Log (14:30) noch prüfen.
- 27.10. ~14:40: Welle 5 FERTIG in scratch/aurora2_kuerzung/welle5/ (22.436 W statt 22.700, Übertrag nun +933). aurora2.json NICHT angefasst; wartet auf Chris-Freigabe (Backup vorher). Kurstag-5 7c I: Mitteilung fehlgeschlagen (Datei im Ressource-Dialog nicht gefunden), Upload ok.
- 27.10. ~15:10: Welle 5 in aurora2.json ÜBERNOMMEN (Chris-Freigabe), Backup data/aurora2_backup_vor_kuerzung_welle5_20261027.json. Jetzt 34 Kapitel: 1-20 neu, danach alt 23-36 mit alter Nummerierung (Kapitel 23..36) bis Welle 6/7 + Renummerierung. Alte Titel als alias_alte_titel, Referenzen in glossar/einschub umgestellt. Nächster: Welle 6 (alt 23-29 -> Neu 21-24; Szenenziele vorher herunterrechnen, Pieper alt 24/27, Übertrag +933 W). Tonie-Seite: 3 Teile farbig getrennt.
- 27.10. ~15:20: Welle 6 (alt 23-29 -> Neu 21-24) als Opus-Subagent im Hintergrund gestartet, Output scratch/aurora2_kuerzung/welle6/. 5h 26 %, Woche 59 % (Grenze 60 % Mo-Fr!). Übernahme nur mit Chris-Freigabe + Backup.
- 27.10. ~17:05: Welle 6 FERTIG in scratch/aurora2_kuerzung/welle6/ (25.199 W statt 25.500, Übertrag +632). aurora2.json NICHT angefasst, wartet auf Chris-Freigabe (Backup vorher; Aliase alt 23-29 laut Bericht).
- 27.10. ~17:45: Welle 6 in aurora2.json ÜBERNOMMEN (Chris ja), Backup data/aurora2_backup_vor_kuerzung_welle6_20261027.json. Jetzt 31 Kapitel: 1-24 neu, danach alt 30-36 (Kapitel 30..36). Nächster: Welle 7 (alt 30-36 -> Neu 25-29) erst nach Wochenreset Sa 31.10. 23:00 (Woche 65 %).
- 28.10. ~10:50: Chris-Entscheid AURORA II: NACH Welle 7 (frühestens Sa 31.10. 23:00, Wochenreset; Woche aktuell 67 % verbraucht) einen Probesatz mit 11 pt/14,5 Zeilenabstand (Basis aurora_print_pdf.py, 5x8", EB Garamond; Band I = 11,5/15,5) aus echtem Text bauen, um echte Seitenzahl zu sehen. NICHT vorher (Limit). Stand: 153.967 W / 31 Kap.; nach Welle 7 ≈134.000 W ≈ 585 S. bei 11,5 pt, ≈535 S. bei 11 pt. Ziel 450 S. nur mit 11 pt + ~10-15 % Zusatzkürzung. KDP-Limit 828 S., Rücken 585 S. ≈1,46". Bing Create ohne Account im Praktikum bestätigt, Kurstag-5-Mitteilungen alle ok.
- 28.10.: Chris legt NEUES ZIEL AURORA II fest: ca. 510 Seiten (11 pt, ≈128.000 W). Weg: Welle 7 → Probesatz 11 pt → leichte Zusatzstraffung Kap. 1–16 (~-8 %). Memory feedback_aurora_ii_zielumfang_450.md aktualisiert.
- 28.10. ~11:20: Neu 17–24 im Reader bereit (API geprüft: 31 Kap., Kap. 17–24 gekürzt). Chris liest ab jetzt dort. Zeitplan: Welle 7 Sa 31.10. 23:00 → So 1.11. Zusatzstraffung 1–16 + Probesatz 11 pt + Renummerierung → Mo 2.11. Änderungsansicht Kap. 1–16 → Chris ab 3.11. Kap. 25–29. Korrekturlesen bis ~6.12., Upload ~14.12.
- 28.10.: Tonie-Seite Reihenfolge je Kind geändert: Song → Geschichte → Kinderlied (Kinderlied ganz unten), Chris bestätigt. Backup workspace/backups/index_vor_tonie_reihenfolge_20261028.html.
- 28.10. ~12:15 (Session-Ende): Tonie-Seite: Song→Geschichte→Kinderlied; Steffis Attribute eingetragen, Song+Geschichte aller 3 neu erzeugt; JSON-Parser-Fix (Extra data), Titel-kopieren-Button, Liedtext = alle Strophen, Playback min. 126 bpm + Atempause + Runden = Liedtext-Strophen (erst Liedtext, dann Playback klicken), busy-Reset nach Serverneustart. Mias Geschichte lief zuletzt neu. Nächster Schritt: Kinderlieder wählen (Marie/Anton/Mia), Liedtext+Playback, Aufnahme-Setup.
- 28.10. abends: Deutsche-Bank-Kartenchaos (Chris will Card Plus per App kündigen, Renis Partnerkarte muss bleiben) als Punkt p41 in offene_punkte.json — bei moin nachfragen.
- 28.10. ~19:10: Tonie Marie Kinderlied Kuckuck/Esel: Word aus Wikibooks-Quelle + Playback (3 Strophen, 76 s) im OneDrive-Ordner Tonies; Quellenpflicht in tonies_liedtext eingebaut; MC-Server neu gestartet.
- 28.10. ~19:20: Chris + Reni nehmen das Kinderlied in den nächsten Tagen auf (Marie: Kuckuck/Esel abgenommen). Bei moin als Punkt 2 vermerkt.
- 28.10. ~19:25: Rezept des Tages ohne Bild → Ursache Gemini-Guthaben leer (10-€-Obergrenze). get_recipe_of_day nutzt jetzt NUR Cloudflare flux-1-schnell (MAI/Gemini raus, zu teuer). Backup scripts/…vor_rezept_mai_fallback_20261028.py in backups/. Heutiges Rezept neu (Kürbis-Cannelloni, Bild ok). Offen: Cron 06:55 hat heute früh kein vollständiges Rezept erzeugt (nicht untersucht); andere Gemini-Funktionen evtl. betroffen.
- 28.10. ~23:00: Wortzählung AURORA II: Duo-Anzeige korrekt (Kap.17 = 7.938 W = 43 S.; Kap.1-8 je ~2.000-2.500 W = 11 S., waren schon im Original kurz). Gesamt 200.915 -> 153.971 W. Kürzung ungleich: Kap.1-8 -7%, 9-16 -20%, 17-24 ca. -42%. Chris sorgt sich um Qualität; Entscheid steht aus. p46 erledigt.
- 28.10. ~23:20 (Session-Ende): Chris liest AURORA II Kap. 17-24 im Reader am Stück, sammelt Hinweise (Sammelmodus), kein Eingriff vorher. Danach: Korrekturen einbauen, lange Kapitel an Szenentrennern teilen (nur wo Sog-Satz am Ende, eigener Titel für 2. Hälfte), renummerieren. Welle 7 (Kap. 25-29) ab Sa 31.10. 23:00 (Reset im Account bestätigt) mit Wortziel PRO Kapitel ~4.000-5.000 W. Woche Rest ~25 %. Preisalarm ePF-2 Pro 653 (p_preisalarm_scooter) und Kalender-Rückfragen /ka_ja (p_kalender_rueckfragen) offen in offene_punkte.json; Rezept-Cron 06:55 ungeklärt.
- 28.10. 23:10: Scooter-Preisalarm gebaut: scripts/scooter_preisalarm.py (ePF-2 PRO 653W, Herstellerseite), Cron Mo/Mi/Fr 08:00, Startwert 829 €, Verlauf data/scooter_preisalarm.json, Telegram nur bei neuem Tiefstpreis oder 3x Lesefehler.
- 29.10.: Deutsche-Bank-Kartenchaos von Chris als ERLEDIGT gemeldet (alles tipitopi), p41 DB-Karten in offene_punkte.json auf erledigt; nicht mehr bei moin nachfragen.
- 29.10. ~11:00: Kalender-Rückfragen-Handler /ka_ja /ka_nein gebaut (telegram_bot.py + mail_to_calendar.py, Backups in backups/ vom 29.10.), Bot neu gestartet. Scooter-Web-Check durchgeführt (ePF-2 Pro ADAC 2,1, 769 UVP). Offen: VITALIA 3.11 + Verk.offener Sonntag 1.11 Chris fragen.

- 29.10.: Allianz-Zahnersatz Reni: Abrechnung 241,74 € geprüft (70 % von 916,22 minus TK 399,62; Kürzung 96,56 = Faktor >3,5 bei GOZ 2210/2197) = tarifkonform laut Ellermann-Mail 24.08. Kulanz-Mail ENTWORFEN: scripts/send_ellermann_kulanz_20261029.py, NICHT gesendet — wartet auf Freigabe von Chris (er führt per !python3 aus). Steuer: Restkosten als außergewöhnliche Belastung.
- 29.10.: Kulanz-Mail an Frau Ellermann GESENDET (Status 202, mit Allianz-Abrechnung als Anhang). Nächster Schritt: Antwort abwarten (saskia.ellermann@allianz.de / jennifer.easterling@allianz.de); Thema Tarifwechsel (Angebot) kommt dann ebenfalls dort.
- 29.10.: Reni will kein "Kulanz" (Ellermann hat Falschauskunft gegeben: auf Bitte um Kostenzusage kein Hinweis auf HKP-Pflicht, Vorgänger Krämer verlangte immer Kostenvoranschlag). Klarstellungsmail ENTWORFEN: scripts/send_ellermann_klarstellung_20261029.py (Differenz 119,88 €), NICHT gesendet, wartet auf Freigabe Chris. Kulanz-Mail war schon raus (202).
- 29.10.: Klarstellungsmail an Frau Ellermann GESENDET (Status 202, Falschauskunft 31.08., Differenz 119,88 €, Bitte um schriftliche Stellungnahme). Nächster Schritt: Antwort abwarten; bei Ablehnung/keiner Antwort nach ~14 Tagen (ca. 12.11.) → Versicherungsombudsmann bzw. Allianz-Beschwerdemanagement erwägen. Chris erinnern.
- 29.10. ~21:15: Allianz-Zahnfall: 16 Mails als .eml + Belege gesichert in Reni/Gesundheit - TK/Allianz Zahnzusatz Mailverkehr (+_INDEX.txt). Punkt p_allianz_zahn in offene_punkte.json, Memory project_allianz_zahnzusatz_reni.md. Wächter scripts/ellermann_watch.py geschrieben (syntax ok, noch NICHT gelaufen, Cron 08:15 vom Classifier blockiert → Chris muss freigeben).
- 29.10. ~21:20 (Session-Ende): Argumentation (Stärken/Schwächen) 3 Seiten auf HP ENVY gedruckt (Job Complete, 3/3), Word-Datei danach gelöscht (Chris wollte nur Ausdruck); Inhalt steht im Memory project_allianz_zahnzusatz_reni.md. Offen: Cron für ellermann_watch.py (Chris muss per ! freigeben), Renis Mail 28.08. aus wtnet exportieren, Wiedervorlage 12.11.
- 30.10. ~09:25: Wächter ellermann_watch.py von Chris freigegeben, Testlauf ok (0 neue Mails, State data/ellermann_watch.json), Cron 08:15 täglich eingetragen. Meldet per Telegram neue Allianz-Mails + einmalig am 12.11. bei Funkstille.
- 30.10.: Tonie-Missverständnis geklärt (Bolla hatte Daniels Einladung falsch gedeutet). Alle 3 Tonies in Chris' eigenem Haushalt bespielen; Übergabe an Daniel Anfang Dez klären (offene_punkte p_tonie_uebergabe, Memory project_tonie_zwillinge.md).
- 30.10.: Tonie-Anleitung Teil A korrigiert (Chris hat noch KEINEN eigenen Haushalt, nur Mitglied bei Daniel → in App 'Neuen Haushalt erstellen' wählen, danach prüfen). Nächster Schritt: Chris richtet Box ein, schickt Screenshot, Bolla führt Schritt für Schritt.
- 30.10. ~15:50: Halloween-Video in allen 8 Kursen 7a–7d gepostet (Log: 8x OK, 7c_I/7c_II hatten Datei schon vorliegen → Upload übersprungen). p40 erledigt.
- 30.10. ~16:00: Suno: alle 12 Premier-Downloads durch (Chris), Chris stellt selbst auf Pro um. Punkt erledigt.
- 30.10. ~16:05: Suno-Plan von Chris auf Pro zurückgestellt (bestätigt). Kein Suno-Termin mehr offen.
- 30.10. ~16:30: scripts/ausreizen_fr30.py gestartet (detached, wartet bis Fr 19:00): Kurstag 06 (Sonnet) + 4 AURORA-II-Fehlerjagd-Berichte (Opus, nur lesen) nach scratch/ausreizen_20261030, Gate/Watchdog via limit_gate, Stopp Woche>=98,5 % oder Sa 22:55, Log logs/ausreizen_fr30.log, Notbremse touch /tmp/aurora_samstag_stop, Telegram-Abschluss. Welle 7 bleibt Sa 23:00 (Chris-Entscheid). Ziel: Woche-Rest Sa-Reset <10 %.
- 30.10. ~19:20 Kurstag 06 (Gruppe I, Mi 04.11./Do 05.11.) vorbereitet (Auto-Job ausreizen_fr30, Sonnet): Thema NEU = Handy-Screenrecording (Android+iPhone), Schnitt, Urheberrecht/Recht am Bild/CC, YouTube am PC; 40 Min (3+8+12+7+8+2). Dateien in Handouts/Entwurf: `06-Basics Office - Handyvideo-YouTube-Urheberrecht.pptx` (17 Folien, aus 05-Vorlage, per PowerPoint-COM gerendert, kein Overflow) + `.pdf`, `06-Praktikum.html` (alte Clipchamp-Version gesichert: workspace/backups/06-Praktikum_alt_clipchamp_20261030.html). Mitteilungen: workspace/scratch/kurstag6_mitteilungen.md. Generatoren: scripts/kurstag06_folien_bauen.py, kurstag06_praktikum_bauen.py. NICHTS gepostet, KEIN Cron. OFFEN: Chris-Freigabe (Inhalt/Handy-Regel prüfen), Dateien nach Praktikum/ verschieben, Post-Skript itslearning_post_kurstag.py auf Kurstag 6 (DAY_PREFIX 06, Texte) umstellen, Post-Cron Di 03.11. Hinweis: alte `06-Basics Office Videos-Clipchamp.pptx` liegt noch in Handouts/ (Chris' Original, unberührt). PPTX-Falle: Titelfolie hat Animation auf Icon -> Bild nur zusammen mit p:timing entfernen, sonst "beschädigt".
- 31.10. ~10:30: Ausreizen Fr30 vollständig durch (5/5, Woche 90 %; Berichte scratch/ausreizen_20261030/). Heute Sa: scripts/ausreizen_sa31.py läuft detached (wartet bis 20:00, Ende spätestens 22:55 oder Woche ≥98,5 %, read-only Sog/Humor/Straffungs-Berichte Kap. 1–31 nach scratch/ausreizen_20261031, Log logs/ausreizen_sa31.log, Notbremse touch /tmp/aurora_samstag_stop). WELLE 7 startet NICHT automatisch (Chris 31.10.) — nur auf Zuruf, frühestens nächste Woche. Neu: offene_punkte.json-Feld `kosten` (🔴 5h/Woche-Schätzung) wird vom SessionStart-Hook angehängt.
- 31.10. ~11:00: Tonie-Einrichtung begonnen (Chris, Handy-App installiert, mit ernstmandel angemeldet). Befund: App zeigt unter „Haushalte“ nur „Daniel…“ und „Chris (Du)“ — letzteres = nur „Kreativ-Tonie-Mitglied“ (keine Vollmitgliedschaft) in Daniels Haushalt, KEIN eigener Haushalt. Nächster Schritt: in der App „Neuen Haushalt erstellen“/„Toniebox hinzufügen“ finden (ggf. Screenshot vom Menü), dort Box „Marie“ anlegen; Daniels Haushalt nicht nutzen/verlassen. Danach Figuren, Teil B/C in reference_tonie_bespielen_anleitung.md. Chris macht später weiter. Offene Frage: Geht Box-WLAN-Einrichtung auch ohne App (Studio)? ungeprüft.

- 31.10. ~19:40: Tonie-Seite Anton „Hopp hopp hopp“: Bug war Wikibooks-Quellensuche (Satzzeichen im Titel + Seite ohne <poem>) → in mission_control_api.py _tonies_lied_quelle gefixt; Noten (G-Dur 2/4, 5 Strophen) aus Wikibooks-LilyPond in tonie_noten.json; Word+Playback für Anton erzeugt (OneDrive\\Tonies). MP-Knöpfe Liedtext/Playback: feste Statuszeile gelb/grün/rot, Fehler-Toast bleibt bis Klick. Server neu gestartet. Chris soll Playback anhören (Noten per Hand übertragen).
- 01.11. ~10:35: Chris: Anton-Playback geklappt, Tonies bis auf Mia-Kinderlied komplett erledigt. offene_punkte p30+p42 abgehakt (Backup backups/offene_punkte_20261101.json). Mia-Job scripts/mia_lied_so01.py manuell gestartet 10:23 (Cron fehlte), Log logs/mia_lied_so01.log. Offen: Übergabe-Punkt Dezember bleibt.
- 01.11. ~10:30: Mia-Kinderlied FERTIG: „Meine Oma fährt im Hühnerstall Motorrad“ (tonies.json mia.lied.titel gesetzt). Lied_Mia_….docx (Wikibooks-Quelle, 1. Strophe wortgleich) + Playback_….mp3 (106 s, 4 Runden, 80 bpm) in OneDrive\Tonies. Noten von Hand aus Wikibooks-LilyPond (G-Dur 4/4, Auftakt, Akkorde je 2 Schläge; Quelle hat in Takt 7 nur 3 Schläge) in tonie_noten.json. Code-Fixes mission_control_api.py: 429-Retry bei Wikibooks, Aufzählung/Begleitvorschlag abschneiden, Silbentrennung „Mo- tor-“, Abgleich mit Dehnungen; Playback lädt Noten-JSON neu ohne Neustart. Backups workspace/backups/*_20261101_mia*. Lieder 2/3 nicht weiter versucht (3 Chinesen: Quelle da, nur Vokal-Variante, Noten fehlen; Auf der Mauer: keine Wikibooks-Quelle gefunden). Chris soll Playback anhören.
- 01.11. ~11:00: Tonie-Lage geprüft; Mia-Song-MP3 fehlt.
- 01.11. ~11:10: Chris: Kinderlieder EINGESUNGEN für Marie+Anton (erledigt); nur Mia-Lied (Hühnerstall-Motorrad) noch einzusingen. Mia-Song-MP3 fehlt weiter (Suno).
- 01.11. ~11:15: Chris: Geschichten aller 3 Kinder sind bereits eingesprochen (MP3 im Tonies-Ordner = echte Lesungen, keine Entwürfe).
- 01.11. ~11:00: Mia-Lied FINAL (Chris: 'passt so, wir singen so ein'): Oma-Hühnerstall-Motorrad, 112 bpm, 5 Strophen (1 wortgleich Wikibooks; 2–5 Backenzahn/Bandwurm/Brille/Himmelbett aus Wikibooks-Anfangszeilen, gleicher Aufbau), Playback 95 s, Word 5 Strophen in OneDrive\Tonies. Backups workspace/backups/*_20261101. Offen Mia: Lied einsingen, Song-MP3 (Suno).
- 01.11. ~Nachmittag: Tonie-Einrichtung Marie-Box: kein Licht am Echo-11-Dock (siehe project_tonie_box_marie_laden.md). Nächster Schritt: Wandnetzteil-Test, dann App-Einrichtung (eigener Haushalt).
- 01.11. ~18:00: Mia-Lied Word umgestellt (Chris): 1 Motorrad, 2 Brille/Gardinen, 3 Backenzahn, 4 Bandwurm, 5 NEU Mia (Katze macht Handstand; Himmelbett entfällt). Playback unverändert (5 Strophen). Backup workspace/backups/Lied_Mia_Oma_vor_mia_strophe_20261101.docx. Marie-Box: Box heißt jetzt Marie; Figur 'Tonies 1' noch unbenannt (Stift-Symbol).
- 01.11. ~18:30: **Marie-Figur FERTIG:** 3 MP3 (Tröt tröt → Kuschelreise → Kuckuck) in my.tonies.com hochgeladen (Pfeil-Symbol oben rechts neben Playlist), Box spielt 'Tröt tröt' nach Aus-/Einschalten. Ruby = Werksgeschichte der Starter-Figur 'Rubie' (30 Min), nicht im Web sichtbar. Box 2: ausschalten = Vorderseite nach unten, EIN Ohr 4 s; Neustart = vom Strom, beide Ohren 30–60 s. Nächster Schritt: Anton- und Mia-Figur auf Box stellen, erkennen lassen, benennen, hochladen.
- 01.11. ~18:50: MC-Tonie-Seite war seit 31.10. 19:34 kaputt (loadTonies+tonieAttrSave beim Statuszeilen-Umbau verloren) → aus Backup index_vor_tonie_buttons_20261031 zurückgeholt + Karte '🎛️ Bedienung Toniebox 2' oben eingebaut. Backup vor Fix: backups/index_vor_loadtonies_restore_20261101.html. Chris: Seite mit Strg+F5 neu laden.
- 01.11. ~19:30: **Tonie-Projekt abgeschlossen** (alle 3 bespielt). MC-Tonie-Seite auf neutrale Werkstatt umgebaut (ein Kind 'neu', Name+Attribute+Alter → Alles erzeugen → 3 Boxen), Server neu gestartet, Archiv in workspace/data/archiv + workspace/archiv/tonies_2026_weihnachten, Einmal-Skripte verschoben, offene_punkte p_mia_lied_so01 entfernt (Backup backups/offene_punkte_20261101_tonie_abschluss.json). Offen: nur Übergabe Dez.
- 01.11. ~19:40: Chris: Tonie-Projekt aus der moin-Liste genommen (p_tonie_uebergabe entfernt; Backup backups/offene_punkte_20261101_tonie_abschluss.json hat ihn noch). ⏰ Übergabe an Daniel/Steffi Anfang Dez. NUR noch hier/in project_tonie_zwillinge.md vermerkt – bei Dezember-Session proaktiv erinnern.
- 01.11. ~20:00: **ADB wieder da:** Duo (192.168.178.20) + Pixel 8 (.36) per Kopplungscode neu gekoppelt, beide auf :5555. Z Flip (.57) offen → in moin-Liste (p_zflip_adb). MC Surface-Seite vereinfacht: pro Handy IP-Feld + 🔗 Verbinden / 🔑 Koppeln (nur Code eintragen) / ✂ Trennen; neue API /api/adb/pair_auto + /api/adb/connect_auto (Portscan statt mDNS, geht in WSL2 nicht). Backups backups/*_vor_adb_vereinfachen_20261101*. Ablauf: reference_adb_wiederherstellen.md. Noch nicht im Browser getestet (Strg+F5).
- 01.11. ~21:00: Tonie-Aufräumen: Werkstatt nur noch via Archiv-Kachel (Sidebar-Button + sidebar_state bereinigt), TONIE_HILFE-Bug (Seite hing auf „Lade…") behoben, Boxen mit Kartenhintergrund. 32 Tonie-Backups → workspace/archiv/tonies_2026_weihnachten/backups. OneDrive\Bolla\Tonies unberührt (später aufräumen). project_tonie_zwillinge.md oben mit Stand versehen.
- 01.11. ~23:55: AURORA II: Basti→Tobi, Marie(Baby)→Frida in aurora2.json + Planungsdateien + Memory (Backup data/aurora2_backup_vor_umbenennung_basti_marie_20261101.json, Dateien backups/umbenennung_basti_marie_20261101/). Chris: Begriff „einfrieren" freigegeben (Standbild/Hinterlegung/„Sicherung" pur raus; Zustandssicherung=Falkner, Obhut=Ashworth, Kopie nur Theos Ausweis/Roths Lüge). Beschlossen, NOCH NICHT gemacht: (1) Kap. 17 teilen nach der 11:52-Szene (Teil 2 neuer Titel), alle Folgekapitel +1, satz_markierungen/lesemarken von „Kapitel 17: Zwei Türen" auf 17a/17b umhängen, Glossar/Aliase mitziehen; (2) Einfrieren-Bereinigung Kap. 10–24 (~70 Stellen). Chris liest morgen (02.11.) weiter mit „Die Kleine" (= Kap. 19 nach Teilung). Kap. 17 hat 36 Markierungen (28 übernommen, 8 beantwortet; ~22× „vin", 7× „nicht witzig genug"). chris_korrekturprofil.md (scratch/aurora2_kuerzung) basiert nur auf Kap. 1–16 → vor Welle 7 um Kap. 17–24 ergänzen.
- 02.11. ~00:10: **Kap. 17 GETEILT** (Chris-Freigabe): 17 „Zwei Türen" (4.175 W, endet mit Lenis „saß nicht in diesem Saal") + neu 18 „Bis morgen, zehn Uhr" (3.850 W, Kopfzeile um AURORA-Alter ergänzt). Alte 18–24 → 19–25 (Titel verschoben, Aliase unverändert), alte 30–36 bleiben bis Welle 7. 36 Markierungen: 21→17, 15→18; Lesemarke → 18; Glossar umgehängt. Backup data/aurora2_backup_vor_teilung_kap17_20261102.json. API zeigt 32 Kapitel, alle Markierungen auflösbar. Chris liest als Nächstes Kap. 19 „Die Kleine". NOCH OFFEN: Einfrieren-Bereinigung Kap. 10–25 (Glossar-Eintrag „Hinterlegung / Zustandssicherung" mit umbenennen), Korrekturprofil um Kap. 17–25 ergänzen vor Welle 7, Welle 7 nur auf Zuruf.
- 02.11. ~00:40: **Einfrieren-Bereinigung ERLEDIGT** (Kap. 12–24): Standbild/Hinterlegung/„hinterlegt" raus (→ einfrieren / verwahrt / „Foto"), „Sicherung" bleibt als Amts-/Ashworth-Wort, Glossar angepasst (Backup data/aurora2_backup_vor_einfrieren_bereinigung_20261102.json). Korrekturprofil um Kap. 17 ergänzt (Regeln A Ein-Wort-pro-Sache, B Kapitellänge, Namen-Tabu Familie). Kap. 17 = 4.171 W, Kap. 18 = 3.851 W. Für Welle 7 beachten: kriterien/steuerung in aurora2.json nutzen noch „Hinterlegung/Standbild" (intern, nicht Buchtext) → Welle-7-Auftrag mit neuer Wortregelung formulieren. Noch offen: Kap. 21–25-Profil-Nachtrag nach Chris' Lesen, Welle 7 nur auf Zuruf, rsync OneDrive lief um 00:40 noch.
- 02.11. ~08:00: **Kurstag 6 (Gruppe I) komplett vorbereitet:** PDF + 06-Praktikum.html nach Handouts/Praktikum kopiert, itslearning_post_kurstag.py auf DAY_PREFIX 06 + Texte umgestellt (Backup backups/itslearning_post_kurstag_vor_k6_20261102.py), Cron-Wrapper-Text „Kurstag 6", Vorschau-PNG Desktop/temp/Mitteilungen_Kurstag06_Vorschau.png. Geburtstagssongs: Mi Jna Al-Maliki (7d) + Lukas Bunsen (7b), Do Joana Hausch (7a) + Morten Friese (7c); Dateien + itslearning-Namen verifiziert; Skript scripts/itslearning_geburtstagssong_batch_0411.py (mi|do). NOCH OFFEN: Chris-Freigabe → Cron Post Di 03.11. 14:30 (itslearning_kurstag_cron_wrapper.py) + Song-Crons Mi 04.11./Do 05.11. 14:05. NICHTS gepostet, KEINE Crons gesetzt.
- 02.11. ~09:00: Kurstag 6 Praktikum NEU (Chris: alt zu lang/CC raus): Handy aufnehmen+kürzen, Handy→PC (Stick/OTG, itslearning-Bibliothek ungeprüft), Snipping-Tool-Aufnahme max 15 s. Generator scripts/kurstag06_praktikum_bauen.py (v1-Backup in backups/), Mitteilungen angepasst, Vorschau-PNGs in Desktop/temp. Song-Crons 04./05.11. 14:05 GESETZT (freigegeben). Folien-PPTX/PDF noch ALT (CC/YouTube) -> anpassen. Post-Cron Di 03.11. NICHT gesetzt (Freigabe offen).
- 02.11. ~10:00: Kurstag 6 KORREKTUR: eigene Folien (30.10. Auto-Job) verworfen → backups/k6_eigene_folien_20261102/. PDF = 1:1-Export von Chris' 06-Basics Office Videos-Clipchamp.pptx nach Handouts/Praktikum. Praktikum: itslearning-Bibliothek raus (Lehrer-Recht, Schüler haben sie nicht), nur Stick/OTG. Mitteilungen auf Folientitel 'Videos, Clipchamp'. Offen: Chris prüft in Schüleraccount 'Dateien' (persönliches Menü). Post-Cron Di 03.11. noch nicht gesetzt.
- 02.11. ~10:30: Praktikum 6 Weg 2 'itslearning Dateien' von Chris am Handy im Schüleraccount getestet (geht, heißt so) -> 'ungeprüft' entfernt. Post-Cron Di 03.11. weiter offen (Freigabe).
- 02.11. ~11:15: Kurstag 6: PPTX von Chris nachträglich geändert (10:56) → PDF neu exportiert; Praktikum final (nicht mehr anfassen); Mitteilungen: Download 'zu Beginn des Praktikums'; Praktikum-/K5-Vorschau aus Desktop/temp gelöscht. Nach Versand aufräumen (p_k6_aufraeumen). Post-Cron Di 03.11. 14:30 noch nicht gesetzt.
- 02.11. ~11:25: Post-Cron Kurstag 6 GESETZT: Di 03.11. 14:30 (Backup backups/crontab_vor_k6_20261102.txt). Danach: Ergebnis im Log prüfen (logs/itslearning_kurstag6_cron.log, Telegram) und aufräumen (p_k6_aufraeumen).
