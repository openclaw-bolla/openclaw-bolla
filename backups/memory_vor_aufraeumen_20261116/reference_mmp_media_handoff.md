---
name: reference-mmp-media-handoff
description: Caption/Bild/Video unterwegs aufs Handy via mmp — der mobile Posting-Weg
metadata: 
  node_type: memory
  type: reference
  originSessionId: 675369e7-6200-4b37-b8f0-91ad6a1cb560
---

Wenn Chris **unterwegs** ist, nützt der OneDrive-Desktop nichts ([[feedback_desktop_apps_social]] gilt nur zuhause). Mobiler Weg läuft über **mmp** (Chris' bevorzugter Kanal, besser als Telegram für ihn):

**Text/Caption:** ins geräteübergreifende Clipboard legen — `POST /api/clipboard {text, append:true, source}`. In mmp Tab „Clipboard" → „📋 Kopieren".

**Bild/Video:** Datei nach `config/clipboard_images/` legen, dann die **URL** (z.B. `https://bolla.chrismandel.de/api/clipboard/image/<datei>`) als Clipboard-Eintrag posten. mmp linkified das seit 02.07.2026:
- `.mp4/.mov/.m4v/.avi` → `<video>`-Player + grüner „⬇ Auf Handy speichern"-Knopf
- `.png/.jpg/...` → Vorschau + „⬇ Auf Handy speichern"
- Serving-Endpoint liefert unbekannte Endungen als `application/octet-stream` → Android lädt runter → landet in Galerie → in TikTok/Insta auswählbar.
(Änderung war frontend-only in `mobile.html`, kein Server-Neustart nötig.)

**Video aus Chris' eigenem Fest-Foto:** Foto an den Bolla-Telegram-Bot → Bolla baut Video+Caption → legt Video in mmp + Caption ins Clipboard.

**Umgekehrte Richtung — Handy-Foto direkt in Windows-Zwischenablage (14.07.2026):** mmp → Tab Clipboard → Bild-Clipboard-Karte → Knopf „📷 Foto aufnehmen → auch Windows-Zwischenablage". Öffnet die Kamera direkt (File-Input mit `capture="environment"`), Foto landet im Bild-Clipboard UND (via `to_windows:true` an `/api/clipboard/image`, gleiche PowerShell-Technik wie der ADB-Weg) sofort in der Windows-Zwischenablage — Strg+V am Studio geht direkt danach. Kein ADB/USB-Debugging nötig, funktioniert von jedem Handy im Browser. Ergänzt den älteren ADB-Pull-Weg ([[project_handy_foto_zwischenablage]]), der "neuestes MediaStore-Bild" holt statt einer gezielten Aufnahme.
- **Chris-Feedback (14.07.2026): "hat super geklappt, genauso wollte ich das"** — Kamera-Knopf ist bestätigt und bleibt Standard-Weg für Handy→Windows-Zwischenablage-Fotos.
- **EXIF-Rotations-Bug gefixt (14.07.2026):** Erster Test zeigte Foto in Word 90° gedreht — Ursache: `.NET Image.FromFile` ignoriert das EXIF-Orientation-Tag (0x0112), das Handykameras statt echter Pixel-Rotation setzen. Fix in `_set_windows_clipboard_image()` (mission_control_api.py): liest Tag 0x0112, wendet vor dem Clipboard-Transfer `RotateFlip` an (Werte 3/6/8 → 180°/90°/270°). Verifiziert mit synthetischem Testbild (40×20 mit Orientation=6 → Clipboard zeigt korrekt 20×40). Gilt für BEIDE Wege (ADB-Pull und mmp-Kamera-Knopf), da beide dieselbe Funktion nutzen.
- **Bekannte Grenze, akzeptiert (14.07.2026):** Löschen aus dem Server-Bild-Clipboard löscht NICHT automatisch das Original in der Handy-Galerie — Browser-Sicherheitssandbox erlaubt Websites keinen Zugriff auf beliebige Galerie-Dateien zum Löschen. Wäre nur über den ADB-Weg (nur Duo, nicht P20) lösbar gewesen, Chris hat das aber explizit NICHT gewünscht ("nein, alles gut erstmal so") — nicht von selbst nachbauen, außer er fragt nochmal danach.

**Posten am Handy (Android, Duo2/P20):**
- *Instagram:* „+" → Beitrag → Medium aus Galerie → Weiter → Caption ins Feld „Bildunterschrift" einfügen → Teilen.
- *TikTok:* „+" → „Hochladen" → Medium wählen → Weiter → Caption ins Beschreibungsfeld einfügen → bei KI-Inhalt „Mehr anzeigen ⌄" → „KI-generierte Inhalte" AN (nur beim Upload möglich!) → Posten. Siehe [[user_ki_transparenz]].
