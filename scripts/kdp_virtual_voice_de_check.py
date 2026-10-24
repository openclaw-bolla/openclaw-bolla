#!/usr/bin/env python3
"""Wöchentlicher Check: unterstützt Amazon KDP "Virtual Voice" (KI-Hörbuch aus eBook) inzwischen
Deutsch (und deutschen Marktplatz)? Stand 24.10.2026: nein (nur EN/ES/FR/IT, US-Markt, Beta).
Meldet nur bei Treffer ('aktion'), sonst ok. Cron: 0 9 * * 1 (montags)."""
import subprocess, sys
from pathlib import Path
from datetime import datetime
sys.path.insert(0, "/home/bolla/workspace/scripts")
from job_status import report

WORKSPACE = Path("/home/bolla/workspace")
CLAUDE_BIN = Path("/home/bolla/.local/bin/claude")
AKTUELL_MD = Path("/home/bolla/.claude/projects/-home-bolla/memory/aktuell.md")
JOB = "kdp-virtual-voice-de"

PROMPT = """Prüfe per WebSearch/WebFetch (aktuelle Quellen), ob Amazon KDP "Virtual Voice"
(KI-Hörbuch-Erstellung aus eBooks, kostenlos für Autoren) inzwischen DEUTSCH als Sprache unterstützt.
Primärquellen: die KDP-Hilfeseiten zu "Hörbücher mit virtueller Stimme"
(kdp.amazon.com/de_DE/help/topic/GMPQGZAZJH6FF456 und kdp.amazon.com/en_US/help/topic/G3QRL9HQNF273Q2H),
dazu aktuelle News. Stand der letzten Prüfung (24.10.2026): nur US-/UK-/AU-Englisch, Spanisch (2),
Französisch, Italienisch; Deutsch NICHT dabei; nur US-Marktplatz, Beta.
Antworte in der ERSTEN Zeile exakt mit JA (Deutsch ist jetzt offiziell unterstützt oder
angekündigt mit Termin) oder NEIN. Bei JA danach 2-3 Sätze mit Quelle/URL, inkl. Marktplatz-
Beschränkungen und Kosten. Nichts erfinden; im Zweifel NEIN."""

def main():
    report(JOB, "KDP Virtual Voice: Deutsch?", "laeuft")
    try:
        r = subprocess.run([str(CLAUDE_BIN), "-p", PROMPT], capture_output=True, text=True,
                           timeout=420, cwd=str(WORKSPACE))
        a = r.stdout.strip()
        if not a:
            report(JOB, "KDP Virtual Voice: Deutsch?", "fehler", (r.stderr or "leere Antwort")[:300]); return
        if a.splitlines()[0].strip().upper().startswith("JA"):
            heute = datetime.now().strftime("%d.%m.%Y")
            old = AKTUELL_MD.read_text(encoding="utf-8") if AKTUELL_MD.exists() else ""
            AKTUELL_MD.write_text(f"## 🎧 {heute} — KDP Virtual Voice: DEUTSCH möglich?\n\n{a}\n\n---\n\n" + old, encoding="utf-8")
            report(JOB, "KDP Virtual Voice: Deutsch JETZT möglich?", "aktion", a[:400])
        else:
            report(JOB, "KDP Virtual Voice: Deutsch?", "ok", "Noch kein Deutsch (" + datetime.now().strftime("%d.%m.") + ")")
    except Exception as e:
        report(JOB, "KDP Virtual Voice: Deutsch?", "fehler", str(e)[:300])

if __name__ == "__main__":
    main()
