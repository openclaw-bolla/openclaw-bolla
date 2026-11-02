---
name: project-fotocleanup-eigene-aufnahmen-backup
description: "Großer autonomer Foto-Aufräum-Fork — Ordner Eigene Aufnahmen_Backup leeren + OneDrive-weiter Screenshot-Sweep. Trigger: 'start fotos', Samstag 12.09.2026 abends"
metadata:
  node_type: memory
  type: project
---

Chris hat am **08.09.2026** einen großen Foto-Aufräum-Auftrag erteilt, der als **Hintergrund-Fork**
laufen soll, **frühestens Samstag 12.09.2026 abends** — und zwar erst, wenn Chris das Stichwort
„**start fotos**" tippt. Alle Detailfragen sind geklärt.

**Komplette Anleitung liegt in:** `/home/bolla/workspace/docs/fotocleanup_eigene_aufnahmen_backup.md`
— beim Trigger diese Datei lesen und den Fork exakt danach briefen.

## Kurz-Zusammenfassung
- **Job 1:** alle echten Screenshots löschen — ganz OneDrive **außer** `Mandels\**` und `Robin\**`,
  plus `Bilder\Screenshots\`, plus Duo per ADB (P20 → Liste für Chris).
- **Job 2:** `D:\OneDrive\Bilder\Eigene Aufnahmen_Backup\` (714 Dateien) restlos auflösen:
  interne Dubletten entdoppeln → gegen `Mandels\2025|2026` + `Robin\22-23|23-24 Jahre` auf schon
  Vorhandenes prüfen (Treffer löschen) → Rest einsortieren (Robin-Fotos → `Robin\<Alter>`,
  sonst → `Mandels\<Jahr>` bzw. passender Reiseordner), Personen per Bildanalyse neu prüfen
  (Chris wurde oft mit Dani verwechselt), undatierte ~316 Stück per Jahr-Schätzung + Report.
  Serie >5 zu einer Situation → eigener benannter Unterordner. Ziel: Ordner leer → gelöscht.
- **Modus:** komplett autonom, tar-Backup vorher, ausführlicher Report hinterher
  (`workspace/docs/fotocleanup_report_20260912.md` + Desktop + SendUserFile).
- **Start-Gate:** nur wenn `curl http://127.0.0.1:18790/api/claudequota` → `seven_day_rem` ≥ 40.
  Wochen-Reset ist So 13.09. 00:00, Samstag abend also knapp — bei < 40 % verschieben.

**Nicht anfassen:** `Eigene Aufnahmen` (ohne `_Backup`) = Windows-Systemordner
([[feedback_eigene_aufnahmen]]). Robins Daten ([[feedback_robin_daten_onedrive_schuetzen]]).
`Mandels` liegt direkt unter der OneDrive-Wurzel, nicht unter `Bilder\`
([[reference_onedrive_mandels_pfad]]). Verwandt: [[project_foto_organisation]],
[[feedback_foto_tagesausflug_workflow]], [[project_handy_foto_zwischenablage]],
[[feedback_hintergrund_fork_lange_aktionen]].
