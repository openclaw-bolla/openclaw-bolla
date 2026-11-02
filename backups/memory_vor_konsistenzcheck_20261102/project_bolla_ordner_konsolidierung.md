---
name: project-bolla-ordner-konsolidierung
description: "Offene Aufgabe — alle Bolla-Dateien in OneDrive in EINEN Ordner \"Bolla\" konsolidieren, Duplikate weg"
metadata: 
  node_type: memory
  type: project
  originSessionId: d6d4a31d-366a-483e-a4a1-e9b064b9cbb7
  modified: 2026-08-23T08:43:41.509Z
---

# Projekt: OneDrive-Konsolidierung „Bolla" (offen, gewünscht 28.06.2026)

**Ziel:** Alle Bolla-bezogenen Dateien/Ordner in OneDrive (AURORA, Suno/Bollawave, MP/Mission Possible, Claude-Code-Doku, Recovery, BildGen …) in **einen Ordner „Bolla"** zusammenführen, gründlich aufräumen, **Duplikate entfernen**. Randthemen ausgenommen (siehe [[feedback_ablage_bolla_vs_randthemen]]).

**Status:** ✅ ETAPPE 1 ERLEDIGT 29.06.2026. Zentraler Ordner = `D:\OneDrive\Dokumente\Bolla\`.
- AURORA eingesammelt: `Dokumente\AURORA` → `Dokumente\Bolla\AURORA` (Backup: `workspace/backups/AURORA_vor_konsolidierung_20260629.tar.gz`).
- ⚠️ Klappentexte (`Klappentext_DE/EN.txt`) lagen NUR in der Desktop-Arbeitskopie „AURORA Google Play" → vor dem Löschen ins Archiv `Bolla\AURORA\5_Veroeffentlichung_Doku\` gerettet (Lehre: vor Löschen IMMER reinschauen).
- Desktop-Arbeitskopie „AURORA Google Play" gelöscht. Lose Desktop-epubs (`AURORA_deutsch/english.epub`) BLEIBEN (Chris braucht sie zum Verschenken).
- KI-Bild `Bilder\KI Bilder\bildgen_*.png` → `Bolla\KI Bilder\`, alter Ordner gelöscht.
- Alte OpenClaw-Phase `openclaw-backup\` (683 Dateien) → `openclaw-phase_archiv_2026.tar.gz` (47M) archiviert, Ordner weg.
- **Backups bewusst UNANGETASTET** (Chris wählte konservativ): `claude-code\` (595M, Live-rsync) + `backups\` (940M, weekly) überlappen bei ~/.claude, aber das ist GEWOLLTE Backup-Redundanz, kein Müll → nicht entdoppeln.

**✅ ETAPPE 2 ERLEDIGT 22.08.2026.**
- `Dokumente\Sicherungen\` geprüft — rein privates Zeug (msecure-Backups, Stammbaum, Robins Segenswünsche, Yourwallet), KEIN Bolla-Bezug → bewusst unangetastet, kein Randthema-Fall.
- **Stale `.claude`-Kopie gefunden & entfernt:** In `Bolla\claud code - openclaw Doku\.claude` lag eine 325 MB alte, verwaiste Kopie von `~/.claude` (letzter Stand 23.05.26) — Reliquie aus der Zeit vor Umbenennung des eigentlichen Live-Spiegels zu `Bolla\claude-code\`. Backup vorher nach `workspace/backups/bolla_stale_claude_kopie_vor_konsolidierung_20260822.tar.gz` (89M komprimiert), dann gelöscht. Doku-Ordner (PDFs/docx, die eigentlich drin gehören) schrumpfte dadurch von 328M auf 3,2M.
- **Bit-identisches Duplikat** `claud code - openclaw Doku\openclaw\openclaw-zusammenfassung.pdf` (= Top-Level-Datei im selben Ordner) gelöscht, per md5 verifiziert.
- **6 verstreute `crontab_backup_*.txt`** (aus `Bolla\` und `Bolla\claude-code\`) in neuen Unterordner `Bolla\crontab_backups\` gebündelt.
- Avatar-Dateien (`bolla_avatar*.png`) per Hash geprüft — **keine** Duplikate, alles unterschiedliche Versionen, unangetastet gelassen.
- Bolla-Ordner: 4,6G → 4,3G.

**Erledigt/abgehakt (23.08.2026):** weekly_backup.sh-Entdopplung auf Chris' Wunsch fallengelassen, kein offener Punkt mehr.

**Sicherer Plan (so angehen):**
1. **Bestandsaufnahme (read-only):** OneDrive nach Bolla-bezogenem durchsuchen — Stichworte AURORA, Suno, Bollawave, DistroKid, Mission, Claude, OpenClaw, BildGen. Aktuell bekannte Streuung u.a.:
   - `D:\OneDrive\Dokumente\AURORA\` (1_Manuskript… bis 5_Veroeffentlichung, _archiv)
   - `D:\OneDrive\Dokumente\Bolla\` (Suno_DistroKid, claud code - openclaw Doku, …)
   - evtl. Desktop-Reste, Bilder-Ordner (Cover/BildGen), weitere.
2. **Duplikat-Analyse:** per Größe+Hash (md5) echte Bit-Duplikate finden — nicht nach Name raten.
3. **Plan vorlegen:** Zielstruktur `D:\OneDrive\…\Bolla\` + Liste was verschoben/gelöscht wird → **Chris-Freigabe**.
4. **Backup vor dem Eingriff** (tar nach workspace/backups/), dann verschieben + Duplikate weg.

**⚠️ Vorsicht:** OneDrive-9p-Mount, case-insensitives NTFS-Ziel. Dateien schwer wiederherstellbar. „Duplikat" erst nach Hash-Vergleich löschen, nie nach Namen. Verschieben statt kopieren+löschen wo möglich.
