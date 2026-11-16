---
name: reference-release-assets
description: Cover + MP3 released Songs — Quelle ist IMMER das lokale Archiv Suno_DistroKid, nicht extern holen
metadata:
  node_type: memory
  type: reference
  originSessionId: current
---

**Regel (Chris, 02.07.2026):** Cover (.jpg) und MP3 aller **released** Bollawave-Songs liegen im lokalen Archiv
`/mnt/d/OneDrive/Dokumente/Bolla/Suno_DistroKid/` (Windows: `D:\OneDrive\Dokumente\Bolla\Suno_DistroKid\`),
Dateiname = Songtitel. **Von dort nehmen** — NICHT aufwändig von Spotify/iTunes/DistroKid-Login holen. Das ist unser Original in voller Auflösung (Cover meist 3000×3000).

## Die zwei Orte (Chris' Workflow, präzisiert 02.07.2026)
- **Desktop-Ordner `D:\OneDrive\Desktop\DistroKid\`** = Veröffentlichungs-**Bühne**, TEMPORÄR. Bolla legt dort **Cover-Auswahlmöglichkeiten** + das **finale** Cover/Song/Anleitung ab. **Chris löscht den Inhalt, sobald Spotify „alles klar" meldet.**
- **`Suno_DistroKid\`** = **finaler, dauerhafter Archivplatz.** Alles Erledigte (finales Cover + finaler Song) bleibt hier für immer, Dateiname = Songtitel.
- **⚠️ PFLICHT bei Release-Abschluss:** Das **finale** Cover (das, das bei DistroKid/Spotify live geht — oft die neueste 3000er-jpg im Desktop-Staging) MUSS ins Suno_-Archiv übernommen werden und dort ein evtl. älteres/verworfenes gleichen Namens **überschreiben**. Genau das ging bei „Läuft, Sommer" schief (Archiv behielt das verworfene, finales lag nur im — dann gelöschten — Desktop-Ordner). Bei „Summertime's Callin'" hatte es korrekt geklappt.
- Aussortierte/alte Cover → `Suno_DistroKid/_aussortiert/`.

**⚠️ ABER — Archiv kann veraltet sein (Fall „Läuft, Sommer" 02.07.2026):** Die Datei `Läuft, Sommer.jpg` im Archiv war noch das **alte, verworfene** Cover (orange Sonnenbrille über Holzsteg mit Palmen). Das **echte Release-Cover** (comic-artige Sonne mit Sonnenbrille am Strand) war zwar auf Spotify live, aber NICHT unter dem Namen im Archiv. Ursache: Cover nach dem 29.06. geändert, Archiv-jpg nicht mitaktualisiert.
→ **Lehre:** Wenn Zweifel am Cover, per Spotify gegenprüfen (`config/spotify_credentials.json`, client_credentials-Flow, `search?q=<Titel> Bollawave` → `album.images` max 640×640). Bei Abweichung: Chris das richtige HiRes-Cover ins Archiv legen lassen, dann Archiv-Datei = wieder Quelle der Wahrheit.

Genutzt von `scripts/distrokid_social_paket.py` ([[project_distrokid_promo_automation]]). Siehe auch [[project_distrokid_desktop_staging]].
