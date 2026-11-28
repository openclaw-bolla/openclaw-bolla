#!/usr/bin/env python3
"""Ausreizen Sa 28.11.2026 (Chris "go"): AURORA II -> amerikanisches Englisch mit Opus, NUR Entwuerfe in scratch.
Phase 1: 14:15-18:45, Woche hoechstens 88 %. Pause bis 20:00 (Chris hat Vorrang). Phase 2: 20:00-22:50, bis 98 %.
5h-Fenster nie ueber 80 %. Resume: Ausgabedatei vorhanden = fertig. Notbremse: touch /tmp/aurora_samstag_stop"""
import datetime as dt
import fcntl
import hashlib
import json
import os
import subprocess
import sys
import time
import urllib.request

W = "/home/bolla/workspace"
OUT = f"{W}/scratch/aurora2_en/kapitel"
LOG = f"{W}/logs/ausreizen_en_sa28.log"
STOP = "/tmp/aurora_samstag_stop"
CL = "/home/bolla/.local/bin/claude"
HARD_5H, EST = 80.0, 12.0


def at(h, m):
    return dt.datetime(2026, 11, 28, h, m)


# (Start, letzter Schrittbeginn, hartes Ende, Wochengrenze)
PHASEN = [(at(14, 15), at(18, 45), at(19, 0), 88.0), (at(20, 0), at(22, 40), at(22, 50), 98.0)]


def log(m):
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(f"[{dt.datetime.now():%d.%m. %H:%M:%S}] {m}\n")


def quota():
    try:
        with urllib.request.urlopen("http://127.0.0.1:18790/api/claudequota", timeout=20) as r:
            q = json.load(r)
        return float(q["five_hour_pct"]), float(q["seven_day_pct"])
    except Exception as e:
        log(f"Quota nicht lesbar: {e}")
        return None


def read(p):
    with open(p, encoding="utf-8") as f:
        return f.read()


def write(p, t):
    with open(p + ".tmp", "w", encoding="utf-8") as f:
        f.write(t)
    os.replace(p + ".tmp", p)


def wait(letzter, cap):
    while dt.datetime.now() < letzter and not os.path.exists(STOP):
        q = quota()
        if q:
            if q[1] + 1.5 > cap:
                log(f"Wochengrenze der Phase erreicht: {q[1]} / {cap}")
                return False
            if q[0] + EST <= HARD_5H:
                return True
        time.sleep(180)
    return False


def call(prompt, ende, name):
    before = quota() or (0, 0)
    t0 = time.time()
    p = subprocess.Popen([CL, "-p", "--model", "opus", "--output-format", "json", "--tools", "", "--strict-mcp-config",
                          "--setting-sources", "", "--system-prompt",
                          "You are an experienced literary translator, German to American English. Output only what is asked."],
                         stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, cwd=f"{OUT}/leer")
    inp, out, killed = prompt, "", False
    while True:
        try:
            out, _ = p.communicate(inp, timeout=45)
            break
        except subprocess.TimeoutExpired:
            inp = None
            q = quota()
            if os.path.exists(STOP) or (q and q[0] >= HARD_5H) or dt.datetime.now() >= ende or time.time() - t0 > 1500:
                p.kill()
                p.communicate()
                killed = True
                break
    after = quota() or before
    log(f"{name} {int(time.time() - t0)} s, 5h {before[0]}->{after[0]}, Woche {before[1]}->{after[1]}"
        + (" ABGEBROCHEN" if killed else ""))
    if killed:
        return None
    try:
        res = json.loads(out)
        if not res.get("is_error"):
            return res["result"]
        log(f"{name}: Fehler {str(res.get('result'))[:200]}")
    except Exception as e:
        log(f"{name}: keine lesbare Antwort ({e})")
    time.sleep(600)
    return None


def prompt_for(d, k):
    names = read(f"{W}/scratch/aurora2_en/namensliste_entwurf.md")
    kultur = read(f"{W}/scratch/aurora2_en/kulturcheckliste.md")
    gl = f"{OUT}/glossar_zusatz.txt"
    extra = read(gl) if os.path.exists(gl) else "(none yet)"
    kanon = json.dumps(d.get("kanon"), ensure_ascii=False)
    return f"""Translate this chapter of the German novel AURORA II into American English AND localize it.
Rules: keep the literary register, rhythm and humor at the same level (do not flatten or simplify); write idiomatic English, not word-for-word; translate every paragraph, keep the paragraph breaks, add and omit nothing; keep all facts, numbers and dates consistent. Use the fixed names and places and the cultural checklist; where an item is undecided use the proposal. AURORA is "she".
=== NAMES ===
{names}
=== CULTURE ===
{kultur}
=== CHOICES MADE IN EARLIER CHAPTERS (stay consistent) ===
{extra}
=== CANON (German, must stay true) ===
{kanon}
Output: the chapter title as first line, then the chapter text. Then a line containing only ###NOTES### followed by at most 10 short lines "German term -> English choice" for NEW names, places or recurring terms not covered above.
=== CHAPTER ===
{k['titel']}

{k['text']}"""


def paras(t):
    return len([z for z in t.split("\n") if z.strip()])


def main():
    os.makedirs(f"{OUT}/leer", exist_ok=True)
    lock = open("/tmp/ausreizen_en_sa28.lock", "w")
    try:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except OSError:
        return
    if os.path.exists(f"{OUT}/fertig") or os.path.exists(STOP):
        return
    now = dt.datetime.now()
    phase = next((p for p in PHASEN if p[0] <= now < p[1]), None)
    if phase:
        _, letzter, ende, cap = phase
        log(f"START Phase bis {ende:%H:%M}, Wochengrenze {cap} %, Quota {quota()}")
        with open(f"{W}/data/aurora2.json", encoding="utf-8") as f:
            d = json.load(f)
        fehl = {}
        for n, k in enumerate(d["kapitel"], 1):
            ziel = f"{OUT}/kap{n:02d}.txt"
            while not os.path.exists(ziel) and fehl.get(n, 0) < 2:
                if not wait(letzter, cap):
                    break
                r = call(prompt_for(d, k), ende, f"EN Kap {n}")
                if r is None:
                    fehl[n] = fehl.get(n, 0) + 1
                    continue
                text, _, notes = r.partition("###NOTES###")
                text = text.strip()
                v = len(text.split()) / max(1, len(k["text"].split()))
                pv = paras(text) / max(1, paras(k["text"]) + 1)
                if not (0.9 <= v <= 1.35 and 0.9 <= pv <= 1.1):
                    log(f"EN Kap {n}: unplausibel (Woerter x{v:.2f}, Absaetze x{pv:.2f})")
                    write(ziel + ".verworfen", text)
                    fehl[n] = fehl.get(n, 0) + 1
                    continue
                write(ziel, text + "\n")
                write(f"{OUT}/kap{n:02d}.quelle", hashlib.sha1(k["text"].encode()).hexdigest() + "\n")
                if notes.strip():
                    with open(f"{OUT}/glossar_zusatz.txt", "a", encoding="utf-8") as f:
                        f.write(notes.strip() + "\n")
                log(f"EN Kap {n}: fertig (Woerter x{v:.2f}, Absaetze x{pv:.2f})")
            q = quota()
            if dt.datetime.now() >= letzter or os.path.exists(STOP) or (q and q[1] + 1.5 > cap):
                break
        log(f"ENDE Phase, Quota {quota()}")
    if dt.datetime.now() >= PHASEN[1][1] or (phase and phase[3] == 98.0 and (quota() or (0, 0))[1] + 1.5 > 98):
        anz = len([f for f in os.listdir(OUT) if f.endswith(".txt") and f.startswith("kap")])
        text = f"EN-Entwuerfe: {anz} Kapitel in scratch/aurora2_en/kapitel; Quota 5h/Woche {quota()}."
        write(f"{OUT}/fertig", text)
        log("FERTIG " + text)
        sys.path.insert(0, f"{W}/scripts")
        from job_status import report
        report("ausreizen_en_sa28", "AURORA II Englisch (Ausreizen 28.11.)", "ok", text)


if __name__ == "__main__":
    main()
