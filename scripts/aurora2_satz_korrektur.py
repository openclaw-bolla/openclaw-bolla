#!/usr/bin/env python3
"""
AURORA II — Satz-Markierungs-Wächter (12.09.2026, Chris' Wunsch)
Chris markiert in MP einen Satz im Kapitel-Lesetext als schwach/fehlerhaft.
Dieses Skript (Cron, alle paar Minuten) prueft offene Markierungen und
korrigiert sie automatisch, ohne dass Chris nochmal nachfragen muss.
"""
import json, os, re, subprocess, sys
import urllib.request
from datetime import datetime
from pathlib import Path

WORKSPACE = "/home/bolla/workspace"
BUCH_FILE = os.path.join(WORKSPACE, "data/aurora2.json")
LOG_FILE = os.path.join(WORKSPACE, "logs/aurora2_satz_korrektur.log")
CLAUDE_BIN = "/home/bolla/.local/bin/claude"


def log(msg):
    line = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}"
    print(line, flush=True)


def telegram(msg):
    try:
        cfg = json.loads(Path(f"{WORKSPACE}/config/telegram_bot.json").read_text())
        import urllib.parse
        data = urllib.parse.urlencode({"chat_id": cfg["chris_id"], "text": msg, "parse_mode": "HTML"}).encode()
        urllib.request.urlopen(f"https://api.telegram.org/bot{cfg['bot_token']}/sendMessage", data=data, timeout=10)
    except Exception as ex:
        log(f"Telegram-Fehler (ignoriert): {ex}")


def extract(raw, tag):
    m = re.search(re.escape(f"{tag}:") + r"\s*(.*?)(?=\n[A-Z_]+:|\Z)", raw, re.DOTALL)
    return m.group(1).strip() if m else ""


def main():
    with open(BUCH_FILE) as f:
        buch = json.load(f)
    marks = buch.get("satz_markierungen", [])
    offene = [m for m in marks if m.get("status") == "offen"]
    if not offene:
        return

    for m in offene:
        kap = next((k for k in buch.get("kapitel", []) if k.get("titel") == m["kapitel_titel"]), None)
        satz = m["satz"]
        if not kap or kap["text"].count(satz) != 1:
            m["status"] = "manuell_pruefen"
            m["notiz"] = "Satz nicht (mehr) eindeutig im Kapitel gefunden — Kapitel wurde evtl. seither verändert."
            log(f"Markierung {m['id']}: nicht eindeutig, manuell prüfen.")
            continue

        text = kap["text"]
        idx = text.find(satz)
        vor = text[max(0, idx - 400):idx]
        nach = text[idx + len(satz):idx + len(satz) + 400]

        prompt = f"""Du bist Lektor für den deutschen KI-Thriller "AURORA II". Chris (der Autor) hat einen Satz im
Kapitel "{m['kapitel_titel']}" markiert, weil er ihn für möglicherweise schwach, unsauber oder fehlerhaft hält.

KONTEXT DAVOR:
…{vor}

MARKIERTER SATZ:
{satz}

KONTEXT DANACH:
{nach}…

Prüfe NUR den markierten Satz (Grammatik, Stil, Wortwiederholung, Klischee, Unklarheit, Bruch mit dem
sonstigen trockenen/lakonischen Erzählton). Wenn er wirklich schwach oder fehlerhaft ist: verbessere ihn,
behalte Inhalt, Fakten, Ton und Erzählperspektive exakt bei, ändere nur so viel wie nötig. Wenn er eigentlich
schon gut ist, lass ihn unverändert.

Antworte AUSSCHLIESSLICH in diesem Format:
STATUS: PROBLEM oder OK
VERSION: <verbesserter Satz oder unveränderter Originalsatz>
BEGRUENDUNG: <ein kurzer Satz>"""

        try:
            r = subprocess.run(
                [CLAUDE_BIN, "-p", "--output-format", "json", "--model", "claude-sonnet-5"],
                input=prompt, capture_output=True, text=True, timeout=180,
            )
            if r.returncode != 0:
                raise RuntimeError(r.stderr[:200])
            raw = json.loads(r.stdout).get("result", "")
            status = extract(raw, "STATUS").upper()
            version = extract(raw, "VERSION").strip()
            begruendung = extract(raw, "BEGRUENDUNG")
        except Exception as ex:
            log(f"Markierung {m['id']}: Fehler bei Claude-Aufruf: {ex}")
            continue

        if version and version != satz and "PROBLEM" in status:
            kap["text"] = kap["text"].replace(satz, version, 1)
            m["status"] = "erledigt"
            m["alt"] = satz
            m["neu"] = version
            m["begruendung"] = begruendung
            m["erledigt_am"] = datetime.now().strftime("%Y-%m-%d %H:%M")
            log(f"Markierung {m['id']}: korrigiert. {begruendung}")
            telegram(
                f"🚩 <b>AURORA II — Satz korrigiert</b>\n"
                f"Kapitel: {m['kapitel_titel']}\n"
                f"Alt: {satz[:150]}\n"
                f"Neu: {version[:150]}\n"
                f"Grund: {begruendung}"
            )
        else:
            m["status"] = "geprueft_ok"
            m["begruendung"] = begruendung or "War schon in Ordnung."
            m["erledigt_am"] = datetime.now().strftime("%Y-%m-%d %H:%M")
            log(f"Markierung {m['id']}: für ok befunden. {begruendung}")
            telegram(
                f"🚩 <b>AURORA II — Satz geprüft</b>\n"
                f"Kapitel: {m['kapitel_titel']}\n"
                f"Satz: {satz[:150]}\n"
                f"Ergebnis: schon in Ordnung ({begruendung})"
            )

        buch.setdefault("statistik", {})["woerter_gesamt"] = sum(len(k["text"].split()) for k in buch["kapitel"])
        with open(BUCH_FILE, "w") as f:
            json.dump(buch, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
