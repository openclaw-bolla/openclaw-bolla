#!/usr/bin/env python3
"""
AURORA Satz-Kur — Resume-Wächter (Cron-Fallback).

Zieht die restlichen Fable-Batches, sobald das Budget es erlaubt (der Batch-Runner
hat eine eigene Ampel: 5h < FIVEH_MAX, Woche >= 25% Reserve). Idempotent:
fertige Batches werden übersprungen. Wenn ALLE 8 Batches vorliegen, baut er einmalig
das Review-Word-Dokument, macht einen Apply-Dry-Run und meldet Chris per Telegram —
dann deaktiviert er sich (DONE_FLAG).

Gedacht als Cron alle 20 Min ab ~14:20 (nach dem 5h-Reset 14:09). Läuft nichts,
wenn das Budget zu voll ist oder schon alles fertig ist. Kostet dann ~nichts.
"""
import os, sys, json, subprocess, datetime, urllib.request, fcntl, glob

HOME = "/home/bolla"
os.environ.setdefault("HOME", HOME)
PY = "/usr/bin/python3"
WS = f"{HOME}/workspace"
SCRIPTS = f"{WS}/scripts"
OUTDIR = f"{WS}/data/satzkur"
DONE_FLAG = f"{OUTDIR}/.satzkur_resume_done"
LOCK_FILE = f"{OUTDIR}/.satzkur_resume.lock"
LOG = f"{OUTDIR}/batch_log.txt"
TG_CFG = f"{WS}/config/telegram_bot.json"
N_BATCHES = 8  # 47 Kapitel / 6

def log(msg):
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] [resume] {msg}"
    print(line, flush=True)
    try:
        open(LOG, "a", encoding="utf-8").write(line + "\n")
    except Exception:
        pass

def tg(text):
    try:
        c = json.load(open(TG_CFG))
        urllib.request.urlopen(urllib.request.Request(
            f"https://api.telegram.org/bot{c['bot_token']}/sendMessage",
            data=json.dumps({"chat_id": c["chris_id"], "text": text,
                             "parse_mode": "Markdown", "disable_web_page_preview": True}).encode(),
            headers={"Content-Type": "application/json"}), timeout=20)
    except Exception as e:
        log(f"Telegram-Fehler: {e}")

def all_done():
    return all(os.path.exists(f"{OUTDIR}/batch_{i:02d}.json") for i in range(N_BATCHES))

def main():
    if os.path.exists(DONE_FLAG):
        return
    lf = open(LOCK_FILE, "w")
    try:
        fcntl.flock(lf, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        log("Anderer Resume-Lauf aktiv — überspringe.")
        return

    if not all_done():
        log("Ziehe restliche Batches (--from 4 --to 7, idempotent)…")
        subprocess.run([PY, f"{SCRIPTS}/aurora_satzkur_batch.py", "--from", "4", "--to", "7"],
                       env=os.environ, timeout=9000)

    if not all_done():
        log("Noch nicht alle Batches fertig (Budget/Reset abwarten) — nächster Cron versucht erneut.")
        return

    # Alles da → Review-Dokument + Dry-Run + Telegram, dann self-disable
    log("Alle 8 Batches vorhanden → Review-Dokument bauen…")
    doc = subprocess.run([PY, f"{SCRIPTS}/aurora_satzkur_review_doc.py"],
                         capture_output=True, text=True, env=os.environ, timeout=300)
    dry = subprocess.run([PY, f"{SCRIPTS}/aurora_satzkur_apply.py"],
                         capture_output=True, text=True, env=os.environ, timeout=300)
    # Zahlen einsammeln
    nrw = nks = 0
    for p in sorted(glob.glob(f"{OUTDIR}/batch_*.json")):
        d = json.load(open(p, encoding="utf-8"))
        nrw += sum(len(k.get("rewrites", [])) for k in d.get("kapitel", []))
        nks += len(d.get("konsistenz", []))
    dry_line = next((l for l in dry.stdout.splitlines() if "anwendbar" in l), "").strip()
    open(DONE_FLAG, "w").write(datetime.datetime.now().isoformat())
    log(f"FERTIG. {nrw} Umbauten, {nks} Konsistenz-Funde. Doc: {doc.returncode==0}. Dry: {dry_line}")
    tg(f"🎩 *AURORA Satz-Kur fertig!*\n\nFable ist durch alle 47 Kapitel: "
       f"*{nrw} Satz-Umbauten* + *{nks} Konsistenz-Funde*.\n"
       f"Review-Dokument liegt auf dem Desktop: *AURORA_Satzkur_Review.docx*.\n"
       f"Einspiel-Check: {dry_line or 'siehe Log'}.\n\n"
       f"Noch NICHTS am Buch geändert — wenn du zurück bist, gehen wir das Dokument durch "
       f"und ich spiele deine Auswahl ein. Viel Spaß beim Fest! 🐾")

if __name__ == "__main__":
    main()
