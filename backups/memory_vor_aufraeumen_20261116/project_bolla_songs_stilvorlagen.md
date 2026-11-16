---
name: project-bolla-songs-stilvorlagen
description: MP „Bolla Songs": Ausklappfeld „🎛️ Stil-Vorlagen" neben Hit-Orientierung; Vorlage Phonk fertig, weitere auf Zuruf
metadata:
  type: project
---

**Stand 06.11.2026:** Rechts neben „Hit-Orientierung" gibt es ein Ausklappfeld **🎛️ Stil-Vorlagen** (Chip pro Vorlage). Chip wählen = Sprache EN, Style + Exclude werden nach der Generierung FEST gesetzt, Zusatzregeln für Text/Tags/Titel gehen in den Songwriter-Prompt. Erste Vorlage: **🔥 Phonk** (Philip + Morten, 06.11.).

**Neue Vorlage einbauen (nur auf Zuruf von Chris):** Eintrag in `SUNO_VORLAGEN` in `scripts/mission_control_api.py` (label, style, exclude, inst) UND gleicher Schlüssel in `SUNO_VORLAGEN` in `mission-control/index.html` (label, info). MC-Server danach neu starten (`kill` + `scripts/start_mc_server.sh`), JS mit `node --check` prüfen. Backups: `workspace/backups/stilvorlagen_20261106/`.

**Phonk-Eckdaten:** Style „Drift phonk, 140 BPM, double-time hi-hats, sharp metallic cowbell hits leading the melody, heavy distorted 808 bass …"; Exclude 6 Begriffe; Regie-Tags pro Abschnitt mit Cowbell-Cues erlaubt (Ausnahme zur „keine Instrumente im Lyrics-Feld"-Regel), Wort „cowbell" nie im gesungenen Text; Titel 🔥🎂 … 🔔🎧. Messung der fertigen Songs: Tempo 140 stimmt, Cowbell ~500–560 Hz kurz-perkussiv. Siehe [[feedback_kuerzel_sfs_w]], [[feedback_suno_style_no_names]], [[reference_bolla_songs]].

**Offen/Hinweis:** Namen wie „Anna" werden durch die bestehende Phonetik-Regel zu „Ah-nah" (bei englischem Text) — bei deutschen Namen ggf. für Vorlagen abschalten, falls Chris es will. Lasse (Bott 7b / Herweg 7c) kommt erst nächstes Jahr.
