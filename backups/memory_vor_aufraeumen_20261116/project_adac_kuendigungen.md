---
name: project-adac-kuendigungen
description: "ADAC-Kündigungen Chris + Reni, Wächter-Status und bestätigte Termine"
metadata: 
  node_type: memory
  type: project
  originSessionId: d36aa8ac-6129-4b5c-98af-77f58cd34d18
  modified: 2026-08-01T19:35:53.475Z
---

Chris und Reni haben beide ihre ADAC-Mitgliedschaft gekündigt. Reni war als "Partner" auf Chris' Mitgliedsnummer 098585320 mitversichert (keine eigene Nummer — die einzige zweite im Postfach, 495444538, gehört Robin).

**Chris:** Kündigung bestätigt, wirksam zum 30.09.2027 (PDF-Anhang, S/MIME-signiert, Mail vom 22.07.2026).

**Reni:** Kündigung am 22.07.2026 selbst per Mail geschickt (renatemandel@wtnet.de → service@adac.de, Betreff „Kündigung Partner-Mitgliedschaft zu Mitgliedsnummer 098585320"). Bestätigung kam am 31.07.2026 (Vorgang 36662290, Sachbearbeiterin Regina Nissen): Kündigung ebenfalls wirksam zum **30.09.2027** (deckt sich mit Chris' Termin). Auffällig: ADAC führt sie im Bestätigungsschreiben unter einer **eigenen, neuen Mitgliedsnummer 254125601** (nicht mehr unter Chris' Nummer) — falls das überrascht, kurz ansprechen. ADAC kündigt zusätzlich an, bei bestehenden ADAC-**Versicherungen** (nicht nur der reinen Mitgliedschaft) noch ein gesondertes Schreiben zu schicken — es kann also noch mehr Post kommen. Übliches Retention-Angebot (kostenlose Hotline für Kündigungsgrund, Online-Rücknahme-Option) ignoriert, kein Interesse geäußert.

**ADAC-Kreditkarte:** separat per Kontaktformular gekündigt/angefragt (`adac_kreditkarte_watcher.py`, meldet seit 23.07.2026) — Status zuletzt unklar, bei Gelegenheit Log/State prüfen.

**Watcher-Status (Stand 01.08.2026):**
- `adac_kuendigung_watcher.py` (Chris, Graph/Outlook) — erledigt
- `reni_adac_kuendigung_watcher.py` (Reni, IMAP renatemandel@wtnet.de, Cron alle 4h) — erledigt, state `done:true`, Telegram-Alarm ging schon raus
- `adac_kreditkarte_watcher.py` — Status bei Bedarf separat prüfen

**Why:** Beide wollten austreten, Kündigungsgrund nicht weiter dokumentiert.
**How to apply:** Bei künftiger ADAC-Post/-Fragen diese Datei als Kontext nutzen statt neu zu recherchieren. Falls ein Schreiben zu "weiteren Versicherungen" bei Reni eintrifft, das ist die hier angekündigte Folge-Post, kein neuer Vorgang.
