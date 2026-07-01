#!/usr/bin/env python3
"""
AURORA Fable-Wächter (Cron, alle 20 Min).
Testet, ob Claude Fable 5 über die CLI verfügbar ist. Sobald ja UND das Budget
gesund ist, startet er EINMALIG die AURORA-Konsultation (read-only Diagnose),
schreibt den Bericht als Datei, meldet Chris per Telegram und deaktiviert sich.

Budget-Disziplin (feedback_fable_budget_disziplin): 5h-Fenster <60 %, Woche >=40 % Reserve.
Fällt beides nicht → diesen Durchlauf überspringen, später neu versuchen.

Solange Fable NICHT verfügbar ist, kostet der Test praktisch nichts (0 Tokens).
"""
import json, os, sys, subprocess, datetime, urllib.request

HOME = "/home/bolla"
os.environ.setdefault("HOME", HOME)
CLAUDE = f"{HOME}/.local/bin/claude"
MODEL = "claude-fable-5"
DATADIR = f"{HOME}/workspace/data"
PROMPT_FILE = f"{DATADIR}/aurora_fable_prompt.txt"
DONE_FLAG = f"{DATADIR}/.aurora_fable_konsultation_done"
OUT_FILE = f"{DATADIR}/aurora_fable_konsultation.md"
TG_CFG = f"{HOME}/workspace/config/telegram_bot.json"
QUOTA_URL = "http://127.0.0.1:18790/api/claudequota"

def log(msg):
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{ts}] {msg}", flush=True)

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

def quota_ok():
    try:
        q = json.load(urllib.request.urlopen(QUOTA_URL, timeout=10))
    except Exception as e:
        log(f"Quota nicht lesbar ({e}) → sicherheitshalber warten.")
        return False
    fh, rem = q.get("five_hour_pct", 0), q.get("seven_day_rem", 0)
    if fh > 60:
        log(f"5h-Fenster bei {fh}% (>60) → warten."); return False
    if rem < 40:
        log(f"Wochen-Reserve nur {rem}% (<40) → warten."); return False
    log(f"Budget ok: 5h {fh}%, Woche {rem}% frei.")
    return True

def fable_available():
    """Mini-Testcall. True nur wenn Fable klar antwortet."""
    try:
        r = subprocess.run([CLAUDE, "-p", "--model", MODEL,
                            "Antworte ausschliesslich mit dem einzelnen Wort: BEREIT"],
                           capture_output=True, text=True, timeout=180, env=os.environ)
    except Exception as e:
        log(f"Testcall-Fehler: {e}"); return False
    out = (r.stdout or "") + (r.stderr or "")
    low = out.lower()
    if "unavailable" in low or "not available" in low or "unknown model" in low or "does not exist" in low:
        log(f"Fable noch nicht verfügbar: {out.strip()[:120]}"); return False
    if "BEREIT" in out.upper():
        log("Fable ist VERFÜGBAR (Testcall ok)."); return True
    log(f"Testcall unklar (kein BEREIT): {out.strip()[:120]}"); return False

def run_consultation():
    prompt = open(PROMPT_FILE, encoding="utf-8").read()
    log("Starte Fable-Konsultation (kann einige Minuten dauern)…")
    r = subprocess.run([CLAUDE, "-p", "--model", MODEL,
                        "--dangerously-skip-permissions", prompt],
                       capture_output=True, text=True, timeout=2400, env=os.environ)
    report = (r.stdout or "").strip()
    if not report or "unavailable" in report.lower():
        log(f"Konsultation lieferte kein Ergebnis (rc={r.returncode}). stderr: {(r.stderr or '')[:200]}")
        return False
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    with open(OUT_FILE, "w", encoding="utf-8") as f:
        f.write(f"# AURORA — Fable-5-Konsultation ({ts})\n\n{report}\n")
    log(f"Bericht geschrieben: {OUT_FILE} ({len(report)} Zeichen)")
    return True

def main():
    if os.path.exists(DONE_FLAG):
        return  # schon erledigt, still beenden
    if not quota_ok():
        return
    if not fable_available():
        return
    # Fable ist da und Budget ok → jetzt der eigentliche Lauf
    if run_consultation():
        open(DONE_FLAG, "w").write(datetime.datetime.now().isoformat())
        tg("🎩 *Fable ist da!* Die AURORA-Konsultation ist automatisch durchgelaufen — "
           "der Diagnose- & Vorschlagsbericht liegt fertig in `data/aurora_fable_konsultation.md`. "
           "Sag Bescheid, dann bereite ich ihn dir auf und wir entscheiden die nächsten Häppchen. 🐾")
        log("FERTIG — Wächter deaktiviert (done-Flag gesetzt).")
    else:
        tg("⚠️ Fable war verfügbar, aber die AURORA-Konsultation lieferte kein sauberes Ergebnis. "
           "Ich schau mir das an, sobald du da bist.")
        log("Konsultation fehlgeschlagen — done-Flag NICHT gesetzt, nächster Cron versucht erneut.")

if __name__ == "__main__":
    main()
