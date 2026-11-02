---
name: reference_kindle
description: Kindle Send-to-Kindle E-Mail-Adresse und Lieferhinweise
metadata:
  node_type: memory
  type: reference
---

# Kindle Lieferung

## Richtige Send-to-Kindle-Adresse
`ernstmandel_MnAuOy@kindle.com`

**WICHTIG:** Diese Adresse ist für die Legacy PC-App (Kindle for Windows alt).
Die falsche Adresse `ernstmandel_PdNwzC@kindle.com` existiert NICHT in der Geräteliste.

## Versand
- Absender: `ernstmandel@outlook.de` (Microsoft Graph API)
- Nach Versand kommt eine Verifikations-Mail von Amazon → Chris muss innerhalb 48h klicken
- Verifikation kommt "ruckzuck" (< 1 Minute)

## Versand-Skript ✅ (Stand 16.06.2026 — funktioniert)
**`python3 /home/bolla/workspace/scripts/kindle_send.py`** — sendet beide AURORA-EPUBs an die Kindle-Adresse. Pfade/Subjects oben im Skript anpassbar.
- **WICHTIG — warum Upload-Session statt einfachem sendMail:** Graph `/me/sendMail` hat ein **4-MB-Limit fürs gesamte Request** (base64-Anhang inkl.). Die AURORA-EPUBs sind ~3 MB → base64 ~4,1 MB → sendMail scheitert (413). Lösung: **Draft anlegen (`POST /me/messages`) → `createUploadSession` für den Anhang → Datei in 1,25-MiB-Chunks per `PUT` mit `Content-Range` hochladen → `POST /me/messages/{id}/send`**. So gehen beliebig große EPUBs.
- **Token:** nutzt `outlook_oauth2.refresh_access_token()` → `config/outlook_token.json`. Dessen Scope enthält **Mail.ReadWrite** (nötig für Draft+Upload-Session; reines Mail.Send reicht NICHT). `ms_token.json` (MC-Server) hätte auch Mail.ReadWrite + Files.ReadWrite.
- Beim Senden landet kurz ein Draft im Postfach, wandert nach Versand in „Gesendet".

## Kindle-App Verhalten
- Persönliche Dokumente erscheinen unter **"Dokumente"**, nicht "Bibliothek"
- Cover erscheinen erst nach App-Neustart vollständig
- Desktop-App (Windows) hat Bugs — neue Version kommt 30.06.2026

## EPUB-Cover für Kindle

### Cover-Bild: Portrait direkt mit MAI generieren ✅ BEVORZUGT
`/api/bildgen` mit `model: "mai-image-2.5"` und `aspect_ratio: "3:4"` → liefert 768×1024 Portrait nativ.
Das ist der richtige Weg für neue Bücher — kein Post-Processing nötig.
aurora_epub_gen.py macht das bereits so (wenn kein LOCAL_COVER gesetzt ist).

### Cover-Bild: Portrait-Format nachträglich erzwingen (Fallback)
Wenn Ausgangs-Cover quadratisch ist (z.B. cover_v6 von früher):
1. Auf 1600×1600 skalieren
2. **Decke:** obere 200px spiegeln, auf 480px strecken, Gauss-Blur r=18, dunkel-Fade (5%→85%)
3. **Boden:** untere 200px spiegeln, auf 480px strecken, Gauss-Blur r=18, hell-Fade (80%→5%)
4. Canvas 1600×2560: top (0–479) + bild (480–2079) + bottom (2080–2559)
→ Sieht atmosphärisch aus, nicht wie Padding. Chris: "sehr gut" ✓

### EPUB-XHTML Cover-Seite
- **Kein SVG** — Kindle rendert `height="100%"` unzuverlässig (bleibt quadratisch)
- **Kein CSS `position:absolute`** — Kindle ignoriert das
- **Richtig:** `<img style="display:block;width:100%;">` — universell, alle Kindle-Versionen
```xml
<body style="margin:0;padding:0;background:#000;">
  <img src="../images/cover.png" alt="Cover" style="display:block;width:100%;"/>
</body>
```

### Text auf Cover
- Font: Orbitron Bold (aus Variable-TTF mit fonttools extrahieren, wght=700)
- Farbe: Gold TITLE_GOLD=(210,155,30), 7° Neigung, Gauss-Schatten
- Text als Bild einbacken (nicht als CSS-Overlay)
