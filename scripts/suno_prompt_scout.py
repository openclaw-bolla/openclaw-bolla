#!/usr/bin/env python3
"""Periodischer Suno-Prompt-Scout: prüft ob eine Optimierung an Chris' Suno-Songtext-Generator
(Style-Tags + Lyrics-Regeln, DE+EN) lohnt — neue Suno-Versionen/Features oder neue, öffentlich
dokumentierte Community-Best-Practices, die wir noch nicht umgesetzt haben.

Hintergrund: 19.08.2026 wurde /api/suno/generate in mission_control_api.py per Opus-Audit
komplett durchoptimiert (siehe aktuell.md-Eintrag vom selben Tag). Dieses Script hält den
Stand danach automatisch aktuell, statt dass Chris/Bolla das manuell wieder anstoßen muss.

Meldet nur, wenn wirklich etwas Neues/Substanzielles gefunden wird (wie hardware_tips.py) —
sonst bleibt es still, kein Rauschen.

Cron: 0 9 1 * *  (1. jedes Monats, 9:00)
"""
import json, subprocess
from pathlib import Path
from datetime import datetime

WORKSPACE = Path("/home/bolla/workspace")
CLAUDE_BIN = Path("/home/bolla/.local/bin/claude")
CODE_FILE = WORKSPACE / "scripts/mission_control_api.py"
AKTUELL_MD = Path("/home/bolla/.claude/projects/-home-bolla/memory/aktuell.md")  # kanonischer Pfad, nicht der Symlink

TG_CFG = json.loads((WORKSPACE / "config/telegram_bot.json").read_text())
BOT_TOKEN = TG_CFG["bot_token"]
CHRIS_ID = TG_CFG["chris_id"]

PROMPT = f"""Du prüfst, ob sich eine Optimierung an Chris Mandels Suno-AI-Songtext-Generator lohnt
(Geburtstagssongs für Schüler + Release-Songs, Deutsch UND Englisch).

HINTERGRUND: Am 19.08.2026 wurde das komplette Prompt-System in {CODE_FILE}
(Handler /api/suno/generate, suche nach 'elif self.path == "/api/suno/generate"') per
Audit durchoptimiert. Bereits umgesetzt (NICHT nochmal vorschlagen, das ist schon drin):
- Tag-Reihenfolge (Genre+Mood zuerst, Rest trailing), Redundanz-Regel (1 Genre-Anker, kein
  Tag-Widerspruch, genau 1 BPM-Tag), Zeichenlimit 250 statt altem 120/160
- DE: Pflicht-Vokal-Sprach-Tag ("vocals in German" etc.), Schlager-Vermeidung mit nicht-
  schlagerhaften Beispielen, Suno-"Exclude"-Feld (4. JSON-Key) mit Default
  "schlager, accordion, oompah brass" wenn Schlager nicht gewollt
- Lyrics: Zahlen immer ausschreiben (nie Ziffern im gesungenen Text), 6-10 Silben/Zeile,
  Strophe 4-6 Zeilen, Refrain 2-4 kurze Zeilen wortgleich wiederholt (nur letzter Chorus darf
  1 Zeile abweichen), Struktur mit Schluss-Refrain vor Outro, Struktur-Tags nur auf eigener
  Zeile ohne erfundene Tags, Pflichtinhalte (Schule/Kurs/Alter) raus aus dem Refrain,
  Stil-Harmonie-Regel gilt immer (auch ohne Referenz-Song)
- Kuratierte Song-Style-Maps (_DE_SONG_STYLE_MAP/_EN_SONG_STYLE_MAP) für bekannte Hits,
  Künstlernamen nie im Style-Prompt

DEINE AUFGABE: Lies den aktuellen Code-Abschnitt selbst (Read-Tool), dann recherchiere mit
WebSearch (aktuelles Jahr) nach:
(a) neuen Suno-Modellversionen/Feature-Announcements seit ca. August 2026, die diese Prompts
    veralten lassen könnten
(b) neuen, öffentlich dokumentierten Community-Best-Practices (Reddit/Guides) für Style-Prompts
    oder Lyrics-Formatierung — DE und EN — die oben NICHT bereits aufgeführt sind

Antworte NUR, wenn du eine ECHTE, KONKRETE, neue Verbesserung findest, die über das oben
Gelistete hinausgeht UND einen spürbaren Effekt auf die Songqualität hätte. Erfinde keine
künstlichen Funde nur um etwas zu liefern — wenn nichts Substanzielles neu ist (sehr
wahrscheinlich der Normalfall bei monatlicher Prüfung), antworte EXAKT mit dem Wort NICHTS.

Falls doch etwas gefunden: max. 3 Punkte, Format pro Punkt:
🎵 [Kurztitel]: [1-2 Sätze was konkret geändert werden sollte und warum, mit Quelle/URL falls vorhanden]"""


def telegram(msg):
    import requests
    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        json={"chat_id": CHRIS_ID, "text": msg, "parse_mode": "HTML"},
        timeout=10,
    )


def main():
    try:
        result = subprocess.run(
            [str(CLAUDE_BIN), "-p", PROMPT],
            capture_output=True, text=True, timeout=300,
            cwd=str(WORKSPACE),
        )
        antwort = result.stdout.strip()

        if not antwort or antwort.upper() == "NICHTS":
            print("Suno-Prompt-Scout: nichts Neues diesen Monat.")
            return

        today = datetime.now().strftime("%d.%m.%Y")
        eintrag = (
            f"## 🎵 {today} — Suno-Prompt-Scout: mögliche Optimierung gefunden\n\n"
            f"Automatisch vom monatlichen Suno-Prompt-Scout-Cron gefunden (Nachfolge-Check zum "
            f"19.08.2026-Audit) — mit Chris besprechen, ob umsetzen.\n\n"
            f"{antwort}\n\n---\n\n"
        )
        old = AKTUELL_MD.read_text(encoding="utf-8") if AKTUELL_MD.exists() else ""
        AKTUELL_MD.write_text(eintrag + old, encoding="utf-8")

        telegram(
            "🎵 <b>Suno-Prompt-Scout</b>\n"
            "Hab beim monatlichen Check eine mögliche Optimierung für die Songtext-Generierung "
            "gefunden — steht in aktuell.md, schauen wir uns in der nächsten Session an."
        )
        print(f"Gefunden und in aktuell.md eingetragen:\n{antwort}")

    except Exception as e:
        print(f"Fehler: {e}")


if __name__ == "__main__":
    main()
