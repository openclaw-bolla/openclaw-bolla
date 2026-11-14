#!/usr/bin/env python3
"""Fable-Lektorat AURORA II (Plan: project_aurora_ii_endspurt_plan.md, Chris-Freigabe 13.11.2026).

Aufrufe (jeweils ein Prozess, limit_gate + Notbremse):
  --test N        Stufe 2 fuer EIN Kapitel (Kostenmessung 5h/Woche vorher/nachher), nur scratch, nichts eingebaut
  --stufe1        Gesamtgutachten (Fable liest das ganze Buch, READ-ONLY): gutachten.md + humor_karte.md
  --stufe2 [a-b]  je Kapitel Humor-/Politur-Vorschlaege als JSON nach scratch (read-only); Resume ueber state.json
  --einbauen      Vorschlaege aus scratch als BLAUE Einschuebe in aurora2.json (Backup, Anker eindeutig, nie ueberschreiben)
Notbremse: touch /tmp/aurora_samstag_stop       Deadline: Sa 14.11. 22:55 (Fable-Wochenbalken-Reset Sa 23:00)
aurora2.json wird NUR von --einbauen veraendert (blaue Vorschlaege, Status 'wartet', Chris entscheidet im Reader).
"""
import argparse
import datetime as dt
import json
import os
import re
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import limit_gate  # noqa: E402

W = "/home/bolla/workspace"
JSON = f"{W}/data/aurora2.json"
OUT = f"{W}/scratch/fable_lektorat"
S2 = f"{OUT}/stufe2"
STATE = f"{OUT}/state.json"
LOG = f"{W}/logs/fable_lektorat.log"
STOP = "/tmp/aurora_samstag_stop"
DEADLINE = dt.datetime(2026, 11, 14, 22, 55)
MODEL = os.environ.get("FABLE_MODEL", "claude-fable-5-2")
WEEK_STOP = float(os.environ.get("FABLE_WEEK_STOP", "98.5"))
CL = shutil.which("claude") or os.path.expanduser("~/.local/bin/claude")
M = "~/.claude/projects/-home-bolla/memory"
AUFTR = f"{W}/scratch/aurora2_lektorat_auftraege.md"
for p in (OUT, S2):
    os.makedirs(p, exist_ok=True)

CHARTA = f"""Grundregeln (AURORA II, Roman von Chris Mandel): Arbeite selbststaendig, keine Rueckfragen. Aendere NICHTS in {JSON} (nur lesen).
Lies zuerst {M}/feedback_aurora_ii_humor_standard.md (Humor-Maßstab = Kap. 10), {M}/feedback_kreative_individualitaet.md, {M}/feedback_aurora_zahlen_exakt.md,
{M}/feedback_blaue_markierung_vorschlaege.md, {M}/feedback_aurora_zielgruppe_kein_spoiler.md, {AUFTR} (Pflicht-Auftraege, v. a. Kap. 9-11, 14, 16) und in {JSON} die Felder 'kanon', 'kriterien', 'satz_markierungen', 'lesemarken'.
Chris' markierte Saetze (satz_markierungen) bleiben woertlich. Keine neuen Fakten/Zahlen/Daten, Band-I-Zahlen exakt. Tochter-Wendung nie spoilern.
Ziel der Politur: Chris will deutlich mehr schmunzeln: Humor gleichrangig mit Spannung. Situationskomik, trockene Beobachtung, Figuren-Running-Gags, Wortwitz - nie aufgesetzt/albern, ernste Szenen bleiben ernst, kein Gag ohne Figurenbezug. Stil der starken Szenen, nicht generisch."""

P1 = CHARTA + f"""

STUFE 1 - GESAMTGUTACHTEN (read-only). Lies das ganze Buch: python3 -c "import json;[print(k['titel'],'\\n',k['text'],'\\n') for k in json.load(open('{JSON}'))['kapitel']]".
Schreibe 1) {OUT}/gutachten.md: Gesamteindruck, Spannungsbogen, Figuren, Stil, Schachtelsaetze/Verdichtung, Probleme je Kapitel (max. 1 Zeile je Befund), Reihenfolge der Dringlichkeit.
2) {OUT}/humor_karte.md: je Kapitel Humor-Dichte 0-5, starke Szenen (woertliches Zitat der Anfangszeile) = Vorbild, schwache Szenen = Kandidaten (Kurzbegruendung), am Ende Ranking der 12 Kapitel mit dem groessten Humor-Potenzial.
Antwort: max. 5 Zeilen."""

P2 = CHARTA + """

STUFE 2 - Kapitel {n} ({titel}). Lies Gutachten/Humorkarte falls vorhanden ({OUT}/gutachten.md, {OUT}/humor_karte.md) und das Kapitel {n} (Kapitel-Index {i} in 'kapitel').
Finde HOECHSTENS 3 humorschwache (nur die wirklich besten Stellen; lieber 1-2 gute als 5 mittlere) oder sprachlich verbesserbare Stellen und schreibe je Stelle einen EINSCHUB (neuer eigener Absatz/kurzer Dialog, 20-120 Woerter), der nach einem woertlichen ANKER-Satz eingefuegt wird.
Schreibe NUR die Datei {S2}/kap{n:02d}.json (Liste von Objekten): {{"anker": "<woertlicher, im Kapitel EINMALIG vorkommender Satz, hinter dessen Absatz eingefuegt wird>", "text": "<Einschub>", "label": "Humor|Politur|Schachtelsatz", "begruendung": "<1 Satz>"}}.
Der Anker darf KEIN markierter Satz sein und muss exakt (Zeichen fuer Zeichen) im Kapitel stehen. Keine Aenderung bestehender Saetze - nur Zusaetze. Leere Liste [] ist ok, wenn das Kapitel stark ist.
Antwort: 2 Zeilen."""


def log(msg):
    line = f"[{dt.datetime.now().strftime('%d.%m. %H:%M:%S')}] {msg}"
    print(line, flush=True)
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(line + "\n")


def state_load():
    try:
        return json.load(open(STATE, encoding="utf-8"))
    except Exception:
        return {"done": []}


def stop_reason():
    if os.path.exists(STOP):
        return "Notbremse-Datei"
    if dt.datetime.now() >= DEADLINE:
        return "Deadline Sa 22:55"
    q = limit_gate.quota() or {}
    if float(q.get("seven_day_pct") or 0) >= WEEK_STOP:
        return f"Woche {q.get('seven_day_pct')} % >= {WEEK_STOP}"
    return None


def run_fable(name, prompt, timeout=5400):
    why = stop_reason()
    if why:
        log(f"STOPP vor {name}: {why}")
        return False
    q0 = limit_gate.quota() or {}
    log(f"-> {name} ({MODEL}) vorher 5h {q0.get('five_hour_pct')} %, Woche {q0.get('seven_day_pct')} %")
    try:
        r = limit_gate.run([CL, "-p", "--model", MODEL, "--allowedTools", "Read,Write,Bash,Glob,Grep"],
                           input=prompt, capture_output=True, text=True, timeout=timeout, heavy=True)
        ok = r.returncode == 0
        log(f"   {name}: rc={r.returncode} {(r.stdout or '')[-300:].strip()!r} {(r.stderr or '')[-200:].strip()!r}")
    except Exception as e:
        ok = False
        log(f"   {name}: Fehler {e!r}")
    q1 = limit_gate.quota() or {}
    try:
        log(f"   nachher 5h {q1.get('five_hour_pct')} % (Δ {float(q1.get('five_hour_pct') or 0) - float(q0.get('five_hour_pct') or 0):+.1f}), "
            f"Woche {q1.get('seven_day_pct')} % (Δ {float(q1.get('seven_day_pct') or 0) - float(q0.get('seven_day_pct') or 0):+.1f})")
    except Exception:
        pass
    return ok


def kap_liste():
    d = json.load(open(JSON, encoding="utf-8"))
    return [(i + 1, k["titel"]) for i, k in enumerate(d["kapitel"])]


def stufe2_prompt(n, titel):
    return P2.format(n=n, i=n - 1, titel=titel, OUT=OUT, S2=S2)


def einbauen():
    d = json.load(open(JSON, encoding="utf-8"))
    ts = dt.datetime.now().strftime("%Y%m%d_%H%M")
    shutil.copy(JSON, f"{W}/backups/aurora2_vor_fable_einbau_{ts}.json")
    log(f"Backup backups/aurora2_vor_fable_einbau_{ts}.json")
    import uuid
    marks = [m.get("satz") or m.get("text") or "" for m in d.get("satz_markierungen", []) if isinstance(m, dict)]
    ok = skip = 0
    for i, k in enumerate(d["kapitel"], 1):
        p = f"{S2}/kap{i:02d}.json"
        if not os.path.exists(p):
            continue
        try:
            items = json.load(open(p, encoding="utf-8"))
        except Exception as e:
            log(f"Kap. {i}: JSON unlesbar {e!r}")
            continue
        for it in items:
            text, anker = k["text"], it.get("anker", "")
            if not anker or text.count(anker) != 1 or any(anker in m for m in marks if m) or it["text"] in text:
                skip += 1
                log(f"Kap. {i}: Anker nicht eindeutig/geschuetzt - uebersprungen: {anker[:50]!r}")
                continue
            idx = text.index(anker) + len(anker)
            end = text.find("\n\n", idx)
            end = len(text) if end == -1 else end
            k["text"] = text[:end] + "\n\n" + it["text"].strip() + text[end:]
            d.setdefault("einschub_vorschlaege", []).append({
                "id": f"ei-fable-{i}-{uuid.uuid4().hex[:6]}", "stufe": 3, "label": it.get("label", "Humor") + " (Fable)",
                "kapitel_titel": k["titel"], "text": it["text"].strip(), "begruendung": it.get("begruendung", ""),
                "status": "wartet", "erstellt_am": dt.datetime.now().strftime("%Y-%m-%d %H:%M")})
            ok += 1
        os.rename(p, p + ".eingebaut")
    d["statistik"]["woerter_gesamt"] = sum(len(x["text"].split()) for x in d["kapitel"])
    json.dump(d, open(JSON, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    log(f"Einbau: {ok} blaue Einschuebe, {skip} uebersprungen")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--test", type=int)
    ap.add_argument("--stufe1", action="store_true")
    ap.add_argument("--stufe2", nargs="?", const="all")
    ap.add_argument("--einbauen", action="store_true")
    a = ap.parse_args()
    kaps = kap_liste()
    st = state_load()
    if a.einbauen:
        return einbauen()
    if a.test:
        n, t = next(x for x in kaps if x[0] == a.test)
        run_fable(f"test_kap{n:02d}", stufe2_prompt(n, t), timeout=1800)
        return
    if a.stufe1:
        if "stufe1" not in st["done"] and run_fable("stufe1_gutachten", P1.replace("{OUT}", OUT)):
            st["done"].append("stufe1")
            json.dump(st, open(STATE, "w"))
        return
    if a.stufe2:
        lo, hi = (1, len(kaps))
        if "-" in a.stufe2:
            lo, hi = map(int, a.stufe2.split("-"))
        for n, t in kaps:
            if not lo <= n <= hi or f"s2_{n}" in st["done"]:
                continue
            if not run_fable(f"stufe2_kap{n:02d}", stufe2_prompt(n, t), timeout=1800):
                if stop_reason():
                    break
                continue
            st["done"].append(f"s2_{n}")
            json.dump(st, open(STATE, "w"))
        log("Stufe 2 Ende; Einbau mit --einbauen (nach Sichtung der JSONs in scratch/fable_lektorat/stufe2)")
        return
    ap.print_help()


if __name__ == "__main__":
    main()
