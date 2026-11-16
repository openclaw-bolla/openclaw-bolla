#!/usr/bin/env python3
"""Fable-Lektorat AURORA II - v2 (umgebaut 14.11.2026 nach verbranntem Riesenlauf).

Lehre: EIN Aufruf ueber das ganze Buch (~230k Token) verbrannte 5h 17->91 %, Woche +14 Pp, kein Ergebnis.
Neue Regeln (Plan: project_aurora_ii_endspurt_plan.md, 'Neuplanung 14.11.'):
  1. Haeppchen: Stufe 1 = je 1-4 Kapitel pro Aufruf, jedes Kapitel-Ergebnis SOFORT als eigene Datei (Checkpoint).
  2. Vorab-Budgetpruefung: nur starten, wenn 5h-Stand + geschaetzte Kosten <= Obergrenze. Kostenmodell lernt mit (state.json).
  3. Nach Abbruch NIE denselben Aufruf wiederholen: Schaetzung steigt, Haeppchen schrumpft; fertige Kapitel bleiben erhalten.
  4. Fable-Balken (weekly_scoped) wird mitgelesen; bei >= FABLE_STOP % pausiert der Lauf und Chris bekommt die Meldung
     'Fable-Zuruecksetzung klicken' (MC-Jobs oben). Das Skript wartet danach selbst weiter (Poll alle 10 Min).
  5. Nichts startet von allein: --auto nur manuell / per ausdruecklich freigegebenem Cron. --dry-run zeigt Plan ohne Verbrauch.

Aufrufe:
  --dry-run            Plan + Kostenschaetzung, KEIN Fable-Aufruf (kostet nichts)
  --auto [--jetzt]     Stufe 1 (alle Kapitel in Haeppchen) -> Merge -> Stufe 2 fuer Top-N Humorkapitel; wartet bis START_AFTER
  --stufe1 | --stufe2 [liste|top] | --merge | --einbauen | --test N   (Einzelschritte)
Notbremse: touch /tmp/aurora_samstag_stop          Ende: Di 17.11. 08:30 (Fable-Reset-Angebot laeuft 08:59 ab)
aurora2.json wird NUR von --einbauen veraendert (blaue Vorschlaege, Status 'wartet', Chris entscheidet im Reader).
"""
import argparse
import datetime as dt
import json
import math
import os
import re
import shutil
import sys
import time
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import limit_gate  # noqa: E402
import limit_policy  # noqa: E402

W = "/home/bolla/workspace"
JSON = f"{W}/data/aurora2.json"
OUT = f"{W}/scratch/fable_lektorat"
S1 = f"{OUT}/stufe1"
S2 = f"{OUT}/stufe2"
STATE = f"{OUT}/state.json"
LOG = f"{W}/logs/fable_lektorat.log"
STOP = "/tmp/aurora_samstag_stop"
START_AFTER = dt.datetime(2026, 11, 14, 23, 3)     # nach Wochen-/Fable-Reset (Sa 23:00)
DEADLINE = dt.datetime(2026, 11, 17, 8, 30)         # Fable-Angebot laeuft Di 17.11. 08:59 ab
MODEL = os.environ.get("FABLE_MODEL", "claude-fable-5-2")
WEEK_STOP = float(os.environ.get("FABLE_WEEK_STOP", "96"))
FABLE_STOP = float(os.environ.get("FABLE_BAR_STOP", "88"))   # % des Fable-Balkens -> pausieren + Reset melden
MAX_CHUNK = 4
EST_START = 12.0          # Pp 5h je Kapitel (Startschaetzung, wird nach jedem Haeppchen nachgemessen)
SAFETY = 1.3
TOP_N = int(os.environ.get("FABLE_TOP_N", "12"))
CL = shutil.which("claude") or os.path.expanduser("~/.local/bin/claude")
M = "~/.claude/projects/-home-bolla/memory"
AUFTR = f"{W}/scratch/aurora2_lektorat_auftraege.md"
for p in (OUT, S1, S2):
    os.makedirs(p, exist_ok=True)

CHARTA = f"""Grundregeln (AURORA II, Roman von Chris Mandel): Arbeite selbststaendig, keine Rueckfragen. Aendere NICHTS in {JSON} (nur lesen).
Lies zuerst {M}/feedback_aurora_ii_humor_standard.md (Humor-Maßstab = Kap. 10), {M}/feedback_kreative_individualitaet.md, {M}/feedback_aurora_zahlen_exakt.md,
{M}/feedback_blaue_markierung_vorschlaege.md, {M}/feedback_aurora_zielgruppe_kein_spoiler.md, {AUFTR} (Pflicht-Auftraege, v. a. Kap. 9-11, 14, 16) und in {JSON} die Felder 'kanon', 'kriterien', 'satz_markierungen', 'lesemarken'.
Chris' markierte Saetze (satz_markierungen) bleiben woertlich. Keine neuen Fakten/Zahlen/Daten, Band-I-Zahlen exakt. Tochter-Wendung nie spoilern.
Ziel der Politur: Chris will deutlich mehr schmunzeln: Humor gleichrangig mit Spannung. Situationskomik, trockene Beobachtung, Figuren-Running-Gags, Wortwitz - nie aufgesetzt/albern, ernste Szenen bleiben ernst, kein Gag ohne Figurenbezug. Stil der starken Szenen, nicht generisch."""

# P1 wird nur per .replace befuellt (keine format-Klammern noetig)
P1 = CHARTA + """

STUFE 1 - GUTACHTEN, NUR die Kapitel @LISTE@ (read-only). Lies NUR diese Kapitel, nicht das ganze Buch. Pro Kapitel genau so vorgehen:
  python3 -c "import json;k=json.load(open('@JSON@'))['kapitel'][KAPITELNUMMER-1];print(k['titel']);print(k['text'])"
Schreibe SOFORT NACH JEDEM Kapitel (nicht erst am Ende!) die Datei @S1@/kapNN.json (NN zweistellig) mit genau diesem JSON-Objekt:
{"n": <Nr>, "titel": "...", "humor_dichte": <0-5>, "spannung": <0-5>, "uebergang": "<1 Satz zum Anschluss>",
 "starke_szenen": ["<woertlich die ersten 12 Woerter>"], "schwache_szenen": [{"anfang": "<woertlich die ersten 12 Woerter>", "grund": "<kurz>"}],
 "befunde": ["<max. 3 Befunde, je 1 Zeile: Spannung/Figuren/Stil/Schachtelsaetze/Konsistenz>"]}
Antwort am Ende: max. 2 Zeilen."""

P2 = CHARTA + """

STUFE 2 - Kapitel {n} ({titel}). Lies Gutachten/Humorkarte falls vorhanden ({OUT}/gutachten.md, {OUT}/humor_karte.md) und das Kapitel {n} (Kapitel-Index {i} in 'kapitel').
Finde HOECHSTENS 3 humorschwache (nur die wirklich besten Stellen; lieber 1-2 gute als 5 mittlere) oder sprachlich verbesserbare Stellen und schreibe je Stelle einen EINSCHUB (neuer eigener Absatz/kurzer Dialog, 20-120 Woerter), der nach einem woertlichen ANKER-Satz eingefuegt wird.
Schreibe NUR die Datei {S2}/kap{n:02d}.json (Liste von Objekten): {{"anker": "<woertlicher, im Kapitel EINMALIG vorkommender Satz, hinter dessen Absatz eingefuegt wird>", "text": "<Einschub>", "label": "Humor|Politur|Schachtelsatz", "begruendung": "<1 Satz>"}}.
Der Anker darf KEIN markierter Satz sein und muss exakt (Zeichen fuer Zeichen) im Kapitel stehen. Keine Aenderung bestehender Saetze - nur Zusaetze. Leere Liste [] ist ok, wenn das Kapitel stark ist.
Antwort: 2 Zeilen."""


# ---------------------------------------------------------------- Hilfen
def log(msg):
    line = f"[{dt.datetime.now().strftime('%d.%m. %H:%M:%S')}] {msg}"
    print(line, flush=True)
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(line + "\n")


def melde(job_id, titel, text, status=None):
    """Meldung ganz oben in MC-Jobs (nie Telegram, Chris 03.11.2026)."""
    try:
        from job_status import mc_meldung
        mc_meldung(job_id, titel, text, status)
    except Exception as e:
        log(f"Meldung fehlgeschlagen: {e!r}")


def state_load():
    try:
        st = json.load(open(STATE, encoding="utf-8"))
    except Exception:
        st = {}
    st.setdefault("done", [])
    st.setdefault("est_pp_je_kap", EST_START)
    st.setdefault("est_s2_pp", 14.0)
    st.setdefault("abbrueche", 0)
    return st


def state_save(st):
    json.dump(st, open(STATE, "w", encoding="utf-8"), ensure_ascii=False, indent=1)


def kap_liste():
    d = json.load(open(JSON, encoding="utf-8"))
    return [(i + 1, k["titel"]) for i, k in enumerate(d["kapitel"])]


def s1_fertig(n):
    try:
        d = json.load(open(f"{S1}/kap{n:02d}.json", encoding="utf-8"))
        return isinstance(d, dict) and "humor_dichte" in d
    except Exception:
        return False


def s2_fertig(n):
    return os.path.exists(f"{S2}/kap{n:02d}.json") or os.path.exists(f"{S2}/kap{n:02d}.json.eingebaut")


_raw = {"t": 0, "d": None}


def usage_raw():
    """Anthropic-Usage-Rohdaten (kostet keine Token). Hoechstens alle 120 s; Fehler -> letzter Wert/None."""
    if time.time() - _raw["t"] < 120 and _raw["d"]:
        return _raw["d"]
    try:
        t = json.load(open(os.path.expanduser("~/.claude/.credentials.json")))["claudeAiOauth"]["accessToken"]
        r = urllib.request.Request("https://api.anthropic.com/api/oauth/usage", headers={
            "Authorization": "Bearer " + t, "anthropic-beta": "oauth-2025-04-20", "Accept": "application/json"})
        _raw["d"] = json.load(urllib.request.urlopen(r, timeout=10))
        _raw["t"] = time.time()
    except Exception as e:
        log(f"   (Usage-Rohdaten nicht lesbar: {e!r})")
    return _raw["d"]


def fable_pct():
    d = usage_raw() or {}
    for lim in d.get("limits", []):
        sc = (lim.get("scope") or {}).get("model") or {}
        if (sc.get("display_name") or "").lower() == "fable":
            return float(lim.get("percent") or 0)
    return None


def snap():
    q = limit_gate.quota() or {}
    return {"h5": float(q.get("five_hour_pct") or 0), "wk": float(q.get("seven_day_pct") or 0),
            "fb": fable_pct(), "q": q}


def sekunden_bis_5h_reset(q):
    return max(60, int(q.get("five_hour_reset_hours", 0)) * 3600 + int(q.get("five_hour_reset_minutes", 0)) * 60 + 90)


def stop_reason():
    if os.path.exists(STOP):
        return "Notbremse-Datei"
    if dt.datetime.now() >= DEADLINE:
        return "Ende Di 17.11. 08:30 (Fable-Angebot)"
    s = snap()
    if s["wk"] >= WEEK_STOP:
        return f"Woche {s['wk']} % >= {WEEK_STOP}"
    return None


def fable_balken_ok():
    """True = weiter; False = Fable-Balken voll -> Reset-Hinweis an Chris (MC-Jobs) und pausieren."""
    fb = fable_pct()
    if fb is None or fb < FABLE_STOP:
        return True
    melde("fable-reset-hinweis", "🔄 Fable-Zurücksetzung jetzt klicken",
          f"Fable-Balken bei {fb:.0f} %. Bitte in Claude → Einstellungen → Nutzung „Fable-Zurücksetzung → Kostenlos zurücksetzen“ klicken "
          f"(läuft Di 17.11. 08:59 ab). Der Lauf pausiert und macht danach automatisch weiter.", "aktion")
    return False


# ---------------------------------------------------------------- ein Fable-Aufruf mit Vorab-Budget
def run_fable(name, prompt, est_pp, timeout=2400):
    """Gibt (ok, delta5h) zurueck. Wartet selbst, bis Budget reicht. Nie blind wiederholen."""
    while True:
        why = stop_reason()
        if why:
            log(f"STOPP vor {name}: {why}")
            return False, 0.0
        if not fable_balken_ok():
            log(f"PAUSE vor {name}: Fable-Balken >= {FABLE_STOP:.0f} % - warte auf Zuruecksetzung/Reset (Poll 10 Min)")
            _raw["t"] = 0
            time.sleep(600)
            continue
        gate, hard = limit_policy.limits()
        s = snap()
        brauche = est_pp * SAFETY
        if s["h5"] + brauche > hard - 3 and s["h5"] > 8:
            sec = sekunden_bis_5h_reset(s["q"])
            log(f"WARTE vor {name}: 5h {s['h5']:.0f} % + Schaetzung {brauche:.0f} Pp > Obergrenze {hard:.0f} % -> Reset in {sec // 60} Min")
            time.sleep(min(sec, 3600))
            continue
        break
    log(f"-> {name} ({MODEL}) vorher 5h {s['h5']:.0f} %, Woche {s['wk']:.0f} %, Fable {s['fb']}, Schaetzung {est_pp:.1f} Pp")
    ok = False
    try:
        r = limit_gate.run([CL, "-p", "--model", MODEL, "--allowedTools", "Read,Write,Bash,Glob,Grep"],
                           input=prompt, capture_output=True, text=True, timeout=timeout, wait=False, heavy=True)
        ok = r.returncode == 0
        log(f"   {name}: rc={r.returncode} {(r.stdout or '')[-250:].strip()!r} {(r.stderr or '')[-200:].strip()!r}")
        err = (r.stderr or "")
        if r.returncode == 75 and "abgebrochen" not in err:
            # Gate hat gar nicht gestartet (Alltagsreserve Woche >= 60 % Mo-Fr / 5h-Gate): kein Verbrauch, keine Strafe -> spaeter neu
            log(f"   {name}: nicht gestartet (Gate) - kein Verbrauch, warte 30 Min und pruefe neu")
            time.sleep(1800)
            return run_fable(name, prompt, est_pp, timeout)
    except Exception as e:
        log(f"   {name}: Fehler {e!r}")
    _raw["t"] = 0
    s1 = snap()
    d5 = s1["h5"] - s["h5"]
    log(f"   nachher 5h {s1['h5']:.0f} % (Δ {d5:+.0f}), Woche {s1['wk']:.0f} % (Δ {s1['wk'] - s['wk']:+.0f}), Fable {s1['fb']}")
    return ok, d5


# ---------------------------------------------------------------- Stufe 1 in Haeppchen
def chunk_groesse(st):
    gate, hard = limit_policy.limits()
    s = snap()
    est = st["est_pp_je_kap"] * SAFETY
    if not st.get("s1_gemessen"):
        return 1          # erstes Haeppchen = 1 Kapitel, bis die echten Kosten gemessen sind
    return max(1, min(MAX_CHUNK, int((hard - 3 - s["h5"]) // est)))


def stufe1(st, dry=False):
    offen = [n for n, _ in kap_liste() if not s1_fertig(n)]
    log(f"Stufe 1: {len(offen)} Kapitel offen, Schaetzung {st['est_pp_je_kap']:.1f} Pp/Kap")
    if dry:
        print(f"  Stufe 1: {len(offen)} Kapitel in >= {math.ceil(len(offen) / MAX_CHUNK)} Haeppchen (max {MAX_CHUNK}), ca. {len(offen) * st['est_pp_je_kap']:.0f} Pp 5h gesamt "
              f"(~{len(offen) * 1.5:.0f} Pp Woche), also ca. {math.ceil(len(offen) * st['est_pp_je_kap'] / 65)} 5h-Fenster")
        return True
    while offen:
        k = chunk_groesse(st)
        teil = offen[:k]
        liste = ", ".join(str(n) for n in teil)
        prompt = P1.replace("@LISTE@", liste).replace("@JSON@", JSON).replace("@S1@", S1)
        ok, d5 = run_fable("s1_kap_" + liste.replace(", ", "_"), prompt, st["est_pp_je_kap"] * len(teil))
        neu_fertig = [n for n in teil if s1_fertig(n)]
        if neu_fertig and d5 > 0:
            gemessen = d5 / len(neu_fertig)
            st["s1_gemessen"] = True
            st["est_pp_je_kap"] = round(max(gemessen, 0.5 * st["est_pp_je_kap"] + 0.5 * gemessen), 1)
        if not ok or len(neu_fertig) < len(teil):
            if stop_reason():          # geplanter Stopp (Woche/Deadline/Notbremse) ist KEIN Abbruch: keine Strafe
                state_save(st)
                return False
            st["abbrueche"] += 1
            st["est_pp_je_kap"] = round(st["est_pp_je_kap"] * 1.3, 1)
            log(f"   Haeppchen {liste}: {len(neu_fertig)}/{len(teil)} fertig -> Schaetzung hoch auf {st['est_pp_je_kap']} Pp/Kap, naechstes Haeppchen kleiner")
            if st["abbrueche"] >= 6:
                melde("fable-lektorat", "⚠️ Fable-Lektorat: zu viele Abbrüche",
                      "6 Abbrüche in Stufe 1 – Lauf gestoppt, nichts wird mehr verbrannt. Bolla prüft Logs (logs/fable_lektorat.log).", "fehler")
                state_save(st)
                return False
        state_save(st)
        offen = [n for n in offen if not s1_fertig(n)]
    return True


def merge():
    """Setzt gutachten.md + humor_karte.md aus den Kapitel-Checkpoints zusammen (ohne Fable, kostet nichts)."""
    teile = []
    for n, _ in kap_liste():
        p = f"{S1}/kap{n:02d}.json"
        if os.path.exists(p):
            try:
                teile.append(json.load(open(p, encoding="utf-8")))
            except Exception:
                pass
    if not teile:
        log("Merge: keine Kapitel-Checkpoints")
        return []
    g = ["# Gutachten AURORA II (Stufe 1, Fable, aus Kapitel-Checkpoints)", ""]
    for t in teile:
        g.append(f"## Kap. {t['n']} - {t.get('titel', '')}  (Spannung {t.get('spannung', '?')}/5, Humor {t.get('humor_dichte', '?')}/5)")
        for b in t.get("befunde", []):
            g.append(f"- {b}")
        if t.get("uebergang"):
            g.append(f"- Anschluss: {t['uebergang']}")
        g.append("")
    open(f"{OUT}/gutachten.md", "w", encoding="utf-8").write("\n".join(g))
    h = ["# Humor-Karte AURORA II", ""]
    for t in teile:
        h.append(f"## Kap. {t['n']} - {t.get('titel', '')}: Humor-Dichte {t.get('humor_dichte', '?')}/5")
        for s in t.get("starke_szenen", []):
            h.append(f"- stark (Vorbild): {s}")
        for s in t.get("schwache_szenen", []):
            h.append(f"- schwach: {s.get('anfang', '')} - {s.get('grund', '')}" if isinstance(s, dict) else f"- schwach: {s}")
        h.append("")
    # Ranking: wenig Humor + viele schwache Szenen = groesstes Potenzial
    rang = sorted(teile, key=lambda t: (t.get("humor_dichte", 5) - 0.4 * len(t.get("schwache_szenen", [])), t["n"]))
    top = [t["n"] for t in rang[:TOP_N]]
    h.append(f"## Ranking Humor-Potenzial (Top {TOP_N}): " + ", ".join(str(n) for n in top))
    open(f"{OUT}/humor_karte.md", "w", encoding="utf-8").write("\n".join(h))
    json.dump(top, open(f"{OUT}/top_humor.json", "w"))
    log(f"Merge: {len(teile)} Kapitel -> gutachten.md, humor_karte.md, Top {TOP_N}: {top}")
    return top


# ---------------------------------------------------------------- Stufe 2
def stufe2_prompt(n, titel):
    return P2.format(n=n, i=n - 1, titel=titel, OUT=OUT, S2=S2)


def stufe2(st, nums, dry=False):
    kaps = dict(kap_liste())
    todo = [n for n in nums if n in kaps and not s2_fertig(n)]
    if dry:
        print(f"  Stufe 2: {len(todo)} Kapitel, je ca. {st['est_s2_pp']:.0f} Pp 5h / ~2 Pp Woche -> ca. {len(todo) * st['est_s2_pp']:.0f} Pp 5h, ~{len(todo) * 2} Pp Woche")
        return True
    for n in todo:
        ok, d5 = run_fable(f"stufe2_kap{n:02d}", stufe2_prompt(n, kaps[n]), st["est_s2_pp"])
        if ok and s2_fertig(n):
            if d5 > 0:
                st["est_s2_pp"] = round(max(d5, 0.5 * st["est_s2_pp"] + 0.5 * d5), 1)
        else:
            st["abbrueche"] += 1
            st["est_s2_pp"] = round(st["est_s2_pp"] * 1.3, 1)
            if stop_reason():
                break
        state_save(st)
    log("Stufe 2 Ende; Einbau mit --einbauen (nach Sichtung der JSONs in scratch/fable_lektorat/stufe2)")
    return True


def top_liste():
    try:
        return json.load(open(f"{OUT}/top_humor.json"))
    except Exception:
        return []


# ---------------------------------------------------------------- Einbau (unveraendert, nur blaue Vorschlaege)
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
                "id": f"ei-fable-{i}-{__import__('uuid').uuid4().hex[:6]}", "stufe": 3, "label": it.get("label", "Humor") + " (Fable)",
                "kapitel_titel": k["titel"], "text": it["text"].strip(), "begruendung": it.get("begruendung", ""),
                "status": "wartet", "erstellt_am": dt.datetime.now().strftime("%Y-%m-%d %H:%M")})
            ok += 1
        os.rename(p, p + ".eingebaut")
    d["statistik"]["woerter_gesamt"] = sum(len(x["text"].split()) for x in d["kapitel"])
    json.dump(d, open(JSON, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    log(f"Einbau: {ok} blaue Einschuebe, {skip} uebersprungen")


# ---------------------------------------------------------------- Dry-Run + Auto
def dry_run(st):
    gate, hard = limit_policy.limits()
    s = snap()
    print(f"IST: 5h {s['h5']:.0f} %, Woche {s['wk']:.0f} %, Fable-Balken {s['fb']} % | Grenzen jetzt: Gate {gate:.0f} / Max {hard:.0f} | {limit_policy.describe()}")
    print(f"Zeitfenster: Start fruehestens {START_AFTER:%a %d.%m. %H:%M}, Ende {DEADLINE:%a %d.%m. %H:%M}; Fable-Stopp bei Balken >= {FABLE_STOP:.0f} %, Woche >= {WEEK_STOP:.0f} %")
    print(f"Haeppchen: bei Schaetzung {st['est_pp_je_kap']:.0f} Pp/Kap und jetzigem 5h-Stand {chunk_groesse(st)} Kapitel pro Aufruf (max {MAX_CHUNK}); Budgetpruefung wartet selbst auf 5h-Reset")
    stufe1(st, dry=True)
    top = top_liste()
    if top:
        stufe2(st, top, dry=True)
    else:
        print(f"  Stufe 2: Top-{TOP_N}-Kapitel nach Stufe 1, je ca. {st['est_s2_pp']:.0f} Pp 5h -> ca. {TOP_N * st['est_s2_pp']:.0f} Pp 5h, ~{TOP_N * 2} Pp Woche")
    print("Es wird KEIN Fable-Aufruf ausgefuehrt (Dry-Run).")


LOCK = "/tmp/fable_lektorat.lock"


def auto(st, jetzt=False):
    import fcntl
    lock = open(LOCK, "w")
    try:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except OSError:
        log("AUTO: laeuft bereits (Lock) - beende diese Instanz")
        return
    if st.get("fertig"):
        log("AUTO: bereits fertig")
        return
    log(f"=== AUTO Start (jetzt={jetzt}) ===")
    while not jetzt and dt.datetime.now() < START_AFTER:
        if stop_reason():
            return
        time.sleep(min(600, max(30, (START_AFTER - dt.datetime.now()).total_seconds())))
    melde("fable-lektorat", "Fable-Lektorat läuft", f"Stufe 1 in Häppchen gestartet ({dt.datetime.now():%a %H:%M}). Fortschritt: logs/fable_lektorat.log", "laeuft")
    if not stufe1(st):
        melde("fable-lektorat", "Fable-Lektorat pausiert/beendet", "Stufe 1 nicht komplett (Grund siehe logs/fable_lektorat.log). Fertige Kapitel bleiben erhalten.", "aktion")
        return
    top = merge()
    stufe2(st, top)
    st = state_load()
    st["fertig"] = True
    state_save(st)
    melde("fable-lektorat", "✅ Fable-Lektorat durch", f"Stufe 1 komplett, Stufe 2 für {len(top)} Kapitel – Vorschläge in scratch/fable_lektorat/stufe2. Einbau als blaue Einschübe auf Zuruf.", "ok")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--auto", action="store_true")
    ap.add_argument("--jetzt", action="store_true")
    ap.add_argument("--ensure", action="store_true")
    ap.add_argument("--test", type=int)
    ap.add_argument("--stufe1", action="store_true")
    ap.add_argument("--stufe2", nargs="?", const="top")
    ap.add_argument("--merge", action="store_true")
    ap.add_argument("--einbauen", action="store_true")
    a = ap.parse_args()
    st = state_load()
    if a.dry_run:
        return dry_run(st)
    if a.einbauen:
        return einbauen()
    if a.merge:
        return merge()
    if a.ensure:      # Cron alle 30 Min: nach Absturz/Reboot automatisch wieder aufnehmen (Zustand liegt in Dateien)
        if st.get("fertig") or os.path.exists(STOP) or not (START_AFTER <= dt.datetime.now() < DEADLINE):
            return
        return auto(st, True)
    if a.auto:
        return auto(st, a.jetzt)
    if a.test:
        t = dict(kap_liste())[a.test]
        run_fable(f"test_kap{a.test:02d}", stufe2_prompt(a.test, t), st["est_s2_pp"])
        return
    if a.stufe1:
        return stufe1(st)
    if a.stufe2:
        nums = top_liste() if a.stufe2 == "top" else [int(x) for x in re.split(r"[,\s]+", a.stufe2) if x]
        return stufe2(st, nums)
    ap.print_help()


if __name__ == "__main__":
    main()
