---
name: feedback_wtnet_gleichwertig
description: chrismandel@wtnet.de gleichwertig zu ernstmandel@outlook.de behandeln — bei Mail-Wächtern/-Suche nie nur Outlook prüfen
metadata: 
  node_type: memory
  type: feedback
  originSessionId: e584c3d0-1265-4feb-a057-39d5eeaba9d2
---

Chris nutzt aktiv zwei eigene Mail-Konten: **ernstmandel@outlook.de** (Haupt-Mail) UND **chrismandel@wtnet.de**
(IMAP, Zugang in `config/wtnet_account.json`, chmod 600). Beide sind gleichwertig zu behandeln, nicht nur Outlook.

**Why:** Am 14.07.2026 fragte Chris nach einer "ADAC Kartenservice"-Mail. Ich hatte nur Outlook durchsucht (Graph
API) und nichts gefunden. Die Mail war tatsächlich da — aber im wtnet-Postfach, weil Chris seine eigene Anfrage
zur ADAC-Kreditkarte (13.07.2026) von chrismandel@wtnet.de aus verschickt hatte, nicht von Outlook. Der
automatische Wächter `adac_kreditkarte_watcher.py` prüfte bis dahin nur Outlook/Graph und hätte die Antwort nie
gemeldet. Chris' Reaktion: "die solltest du aber bitte gleichertig zu outlook verwenden (hatten wir vereinbart)" —
das war schon einmal Thema, ist also eine bestehende, aber nicht konsequent umgesetzte Abmachung.

**How to apply:**
- Bei jeder Mail-Suche/-Diagnose ("hast du die Mail gesehen?", "ist da was angekommen?") IMMER beide Postfächer
  prüfen — Outlook via Graph (`outlook_token.json`/`ms_token.json`) UND wtnet via IMAP (`wtnet_account.json`,
  Pattern siehe `spam_watcher.py::clean_wtnet()` oder `adac_kreditkarte_watcher.py::check_wtnet()`).
- Bei neuen oder bestehenden Mail-Wächter-Skripten (watcher, die auf eine bestimmte Antwort warten) IMMER beide
  Konten abdecken, nicht nur Outlook als Default annehmen. `adac_kreditkarte_watcher.py` wurde am 14.07.2026
  entsprechend erweitert — als Vorlage für ähnliche Fälle nutzen.
- Reni's Mail-Konto (renatemandel@wtnet.de, `reni_smtp.json`) ist ein drittes, separates Konto — nicht verwechseln.
