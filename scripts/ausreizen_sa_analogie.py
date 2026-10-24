#!/usr/bin/env python3
"""Sa 24.10.2026 Ausreizen (Chris-Freigabe 19:30): Analogie-Check AURORA II Kap. 31-36 + Tonie-Entwuerfe.
Nur Opus, EIN Prozess, Gating 5h<=75 %, Woche < 95 %, Deadline 23:50. Notbremse: touch /tmp/aurora_samstag_stop
Resume-faehig (state.json). Reihenfolge: Tonies (kurz) zuerst, dann Analogie-Check Kap. 31-36 in 3 Foki-Runden."""
import datetime as dt, fcntl, json, os, shutil, sys, time, urllib.request
W = "/home/bolla/workspace"
sys.path.insert(0, f"{W}/scripts")
os.environ["SAMSTAG_TAG"] = "sa_analogie_20261024"
os.makedirs(f"{W}/scratch/aurora_samstag_sa_analogie_20261024", exist_ok=True)
import samstag_ausreizen as s
s.WEEK_STOP = float(os.environ.get("AUSREIZEN_WEEK_STOP", "95"))
s.DEADLINE = dt.datetime.fromisoformat(os.environ.get("AUSREIZEN_DEADLINE", "2026-10-24T23:50:00"))
log, Stop = s.log, s.Stop
API = "http://127.0.0.1:18790"
FOKI = ["Fehlerklassen aus Chris' Korrekturen: unklarer Bezug/fehlendes Bezugswort; Figur/Vorwissen nicht eingefuehrt; elliptische Saetze/fehlende Woerter; Grammatik/indirekte Rede; schiefe Bilder; Pointe nicht verstaendlich",
        "Zahlen-/Zaehl-/Timing-Fehler; Logikbruch; abrupter Szenen-/Zeitwechsel; Detail-Kontinuitaet gegen Kap. 1-30; AURORA-Logik; Sprecher unklar",
        "abgenutzter Running Gag; mehrdeutige Wortwahl; Wortwiederholungen, Fuellsaetze, Business-Jargon; Humor-Dichte wie Kap. 10"]

def post(path, body):
    r = urllib.request.Request(API + path, data=json.dumps(body).encode(), headers={"Content-Type": "application/json"})
    return json.load(urllib.request.urlopen(r, timeout=30))

def tonies():
    todo = [("marie", "song"), ("marie", "lied"), ("marie", "geschichte"), ("anton", "lied"), ("mia", "song"), ("mia", "lied"), ("mia", "geschichte")]
    for kind, teil in todo:
        key = f"tonie:{kind}:{teil}"
        if s.is_done(key):
            continue
        s.gate()
        t = json.load(urllib.request.urlopen(API + "/api/tonies", timeout=30))["kinder"][kind][teil]
        if t.get("ergebnis"):
            s.mark(key); continue
        log(f"Tonie {kind}/{teil} erzeugen")
        post("/api/tonies/generate", {"kind": kind, "teil": teil, "wunsch": ""})
        for _ in range(60):
            time.sleep(10)
            t = json.load(urllib.request.urlopen(API + "/api/tonies", timeout=30))["kinder"][kind][teil]
            if not t.get("busy"):
                break
        if t.get("ergebnis"):
            s.mark(key)
        else:
            log(f"Tonie {kind}/{teil}: kein Ergebnis ({t.get('fehler')})")

def analogie():
    for r, focus in enumerate(FOKI, 1):
        for n in range(31, 37):
            s.gate()
            s.review_chapter(n, mode=f"analogie{r}", focus=focus)

def main():
    lock = open(f"{s.OUT}/.lock", "w")
    try:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except OSError:
        print("laeuft bereits"); return
    grund = "fertig"
    try:
        if os.path.exists(s.STOP):
            os.remove(s.STOP)
        if not s.is_done("backup"):
            shutil.copy(s.DATA, f"{W}/backups/aurora2_vor_sa_analogie_{dt.datetime.now():%Y%m%d_%H%M}.json")
            shutil.copy(f"{W}/data/tonies.json", f"{W}/backups/tonies_vor_sa_analogie_{dt.datetime.now():%Y%m%d_%H%M}.json")
            s.mark("backup")
        q = s.quota() or {}
        log(f"START Sa-Analogie — 5h {q.get('five_hour_pct')} %, Woche {q.get('seven_day_pct')} %")
        tonies()
        analogie()
    except Stop as e:
        grund = f"gestoppt: {e}"; log(f"STOP: {e}")
    except Exception:
        import traceback; grund = "Fehler"; log("FEHLER: " + traceback.format_exc())
    finally:
        q = s.quota() or {}
        open(f"{s.OUT}/ABSCHLUSSBERICHT.md", "w", encoding="utf-8").write(
            f"# Sa-Ausreizen Analogie+Tonies\nEnde {dt.datetime.now():%H:%M} · {grund}\nLimits: 5h {q.get('five_hour_pct')} % · Woche {q.get('seven_day_pct')} %\n"
            f"Statistik: {json.dumps(s.ST['stats'], ensure_ascii=False)}\nProtokoll: changes.md, uebersicht.md\n")
        log("ABSCHLUSSBERICHT geschrieben")

if __name__ == "__main__":
    main()
