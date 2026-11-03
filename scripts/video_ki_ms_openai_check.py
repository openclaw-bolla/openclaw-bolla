#!/usr/bin/env python3
"""Wöchentlicher Check: bringen Microsoft (MAI) oder OpenAI wieder ein eigenes Video-KI-Modell?
Stand 03.11.2026: Sora 2 abgekündigt (API-Ende 24.09.2026), MAI hat nur Bild/Sprache/Transkription.
Meldet nur bei Treffer als 'aktion' (steht ganz oben in MC-Jobs), kein Telegram. Cron: montags 09:20."""
import subprocess, sys
from pathlib import Path
from datetime import datetime
sys.path.insert(0, "/home/bolla/workspace/scripts")
from job_status import report

WORKSPACE = Path("/home/bolla/workspace")
CLAUDE_BIN = Path("/home/bolla/.local/bin/claude")
AKTUELL_MD = Path("/home/bolla/.claude/projects/-home-bolla/memory/aktuell.md")
JOB = "video-ki-ms-openai"
TITEL = "Video-KI: Microsoft/OpenAI wieder dabei?"

PROMPT = """Prüfe per WebSearch/WebFetch (aktuelle Quellen), ob Microsoft (MAI-Familie, Azure Foundry, Bing Video Creator)
oder OpenAI (Nachfolger von Sora 2, neues Videomodell, Video in der API oder in ChatGPT) inzwischen ein EIGENES
Videogenerierungs-Modell anbieten oder verbindlich mit Termin angekündigt haben.
Stand 03.11.2026: OpenAI hat Sora 2 abgekündigt (API-Ende 24.09.2026), kein Nachfolger bekannt; Microsoft MAI hat
nur Bild-, Sprach- und Transkriptionsmodelle (MAI-Image-2.x), KEIN Videomodell. Reine Drittanbieter-Hosting
(z. B. Veo/Kling/Runway über Azure) zählt NICHT. Gerüchte zählen nicht.
Erste Zeile exakt JA oder NEIN. Bei JA danach 2-3 Sätze: welches Modell, wer, Preis/Zugang (API?), Quelle/URL.
Nichts erfinden; im Zweifel NEIN."""

def main():
    report(JOB, TITEL, "laeuft")
    try:
        r = subprocess.run([str(CLAUDE_BIN), "-p", PROMPT], capture_output=True, text=True,
                           timeout=420, cwd=str(WORKSPACE))
        a = r.stdout.strip()
        if not a:
            report(JOB, TITEL, "fehler", (r.stderr or "leere Antwort")[:300]); return
        if a.splitlines()[0].strip().upper().startswith("JA"):
            heute = datetime.now().strftime("%d.%m.%Y")
            old = AKTUELL_MD.read_text(encoding="utf-8") if AKTUELL_MD.exists() else ""
            AKTUELL_MD.write_text(f"## 🎬 {heute} — Video-KI: Microsoft/OpenAI jetzt dabei?\n\n{a}\n\n---\n\n" + old, encoding="utf-8")
            report(JOB, TITEL.replace("wieder dabei?", "JETZT dabei!"), "aktion", a[:400])
        else:
            report(JOB, TITEL, "ok", "Noch nichts (" + datetime.now().strftime("%d.%m.") + ")")
    except Exception as e:
        report(JOB, TITEL, "fehler", str(e)[:300])

if __name__ == "__main__":
    main()
