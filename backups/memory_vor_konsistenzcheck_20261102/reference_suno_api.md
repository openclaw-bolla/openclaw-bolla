---
name: suno-api-endpoint
description: Aktuelle Suno API Base-URL und Token-Methode (Stand Mai 2026)
metadata: 
  node_type: memory
  type: reference
  originSessionId: d6d4a31d-366a-483e-a4a1-e9b064b9cbb7
---

# Suno API (Stand 2026-05-15)

## Base URL
`https://studio-api-prod.suno.com` ← NEU! (alte `.ai` Domain ist suspended)

## Wichtige Endpoints
- Songs liste: `GET /api/feed/?page=0&page_size=20`
- Einzelner Clip + Metadaten/Lyrics: `GET /api/clip/{id}` → `metadata.prompt` = Lyrics (gratis, für Blocklist-Scan)
- Cover groß: Feld `image_large_url` (1024×1024) statt `image_url` (nur 360×360 Thumbnail!)
- Audio: Feld `audio_url` (sonst `https://cdn1.suno.ai/{id}.mp3`)

## ⭐ Fertigen Song SELBER ziehen (Chris-Wunsch 28.06.2026 — NICHT nach Link/Download fragen)
Wenn Chris sagt „Song ist fertig bei Suno": Token liegt in `config/suno_token.json` (Feld `token`, Chris schickt ihn frisch via Telegram). Flow:
1. `GET /api/feed/?page=0&page_size=20` → neuesten Treffer per Titel finden (created_at = heute).
2. `audio_url` laden → `ffmpeg -i raw.mp3 -b:a 320k "Titel.mp3"` (DistroKid will 320 kbps).
3. `image_large_url` laden (1024²) → **DistroKid braucht ≥1400², empf. 3000²** → mit PIL `resize((3000,3000), LANCZOS)` hochskalieren, JPEG q92. KI-Cover ohne Fotodetail verträgt das verlustarm.
4. **Archiv = einzige Dauer-Ablage:** Song nach `D:\OneDrive\Dokumente\Bolla\Suno_DistroKid\Titel.mp3` + `.jpg`. Das ist das EINZIGE permanente Archiv.
5. **Desktop = nur TEMPORÄRE Arbeitskopie fürs Hochladen** (Chris-Regel 28.06.2026, korrigiert): Für den Browser-Upload den ganzen Ordner griffbereit auf den Desktop spiegeln (`cp -rf "/mnt/d/OneDrive/Dokumente/Bolla/Suno_DistroKid" "/mnt/d/OneDrive/Desktop/"`). **NACH dem Release/erfolgreichen Upload die Desktop-Kopie WIEDER LÖSCHEN** (`rm -rf "/mnt/d/OneDrive/Desktop/Suno_DistroKid"`) — Desktop ist nur Kopie, keine dauerhaften Duplikate (243 MB). Vor dem Löschen kurz prüfen, dass das Archiv im Doku-Ordner vollständig ist. Upload macht Chris im Browser, Settings stehen in der Songdatei.
- Suno liefert pro Generierung 2 Versionen; wenn im Feed nur 1 Treffer → Chris hat die anderen Takes schon gelöscht, dann ist die Wahl eindeutig. Sonst Treffer mit Dauer auflisten und Chris wählen lassen.

## Auth
Bearer Token (Clerk JWT) aus Browser-Konsole auf suno.com:
```javascript
fetch('https://auth.suno.com/v1/client',{credentials:'include'}).then(r=>r.json()).then(d=>{const sess=d.response?.sessions||[];sess.forEach(s=>{const tok=s.last_active_token?.jwt||'';if(tok)console.log('TOKEN:'+tok)});})
```
→ Token in `/tmp/suno_token.txt` speichern

## Token Gültigkeit
~1 Stunde (Clerk JWT)

## Hinweis
`studio-api.suno.ai` (alt) → "Service Suspended" (Cloudflare)
`studio-api-prod.suno.com` (neu) → funktioniert ✅
Rate Limit: ~17 Seiten à 20 Songs ohne Pause → danach 429
Mit 0.3s Pause: ~13 Seiten zuverlässig
