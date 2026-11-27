#!/usr/bin/env python3
"""Ausreizen AURORA II Fr 27.11. -> Sa 28.11.2026 22:50 (Chris "go" 27.11.).
Regeln: 5h-Fenster NIE ueber 80 % (auch nachts), Wochen-Zwischenziele je Fenster, Stopp bei 98 %, ein Prozess zur Zeit,
nie Fable. Straffung 19-28 NUR als Entwurf (scratch). Analogie/Fehler als blaue Vorschlaege; Kap. 38 und (wegen der
Straffungsentwuerfe) Kap. 19-28 werden nicht angefasst, Funde dort nur gesammelt. Resume: fertig = Ausgabedatei da.
Notbremse: touch /tmp/aurora_samstag_stop"""
import datetime as dt
import fcntl
import json
import os
import re
import shutil
import subprocess
import sys
import time
import urllib.request
import uuid

W = "/home/bolla/workspace"
OUT = f"{W}/scratch/ausreizen_20261127"
BUCH = f"{W}/data/aurora2.json"
LOG = f"{W}/logs/ausreizen_fr27.log"
STOP = "/tmp/aurora_samstag_stop"
CL = "/home/bolla/.local/bin/claude"
DEADLINE = dt.datetime(2026, 11, 28, 22, 50)
HARD_5H = 80.0
SLOTS = [(dt.datetime(2026, 11, 27, 23, 10), 67), (dt.datetime(2026, 11, 28, 4, 10), 74),
         (dt.datetime(2026, 11, 28, 9, 10), 80), (dt.datetime(2026, 11, 28, 14, 10), 86),
         (dt.datetime(2026, 11, 28, 19, 10), 92), (DEADLINE, 98)]
for sub in ("straffung", "analogie", "fehler", "leer"):
    os.makedirs(f"{OUT}/{sub}", exist_ok=True)
SYS = "Du bist ein sorgfaeltiger, zurueckhaltender Lektor fuer deutsche Romane. Antworte genau im verlangten Format, ohne Vorrede."


def log(m):
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(f"[{dt.datetime.now():%d.%m. %H:%M:%S}] {m}\n")


def load():
    with open(BUCH, encoding="utf-8") as f:
        return json.load(f)


def quota():
    try:
        with urllib.request.urlopen("http://127.0.0.1:18790/api/claudequota", timeout=20) as r:
            q = json.load(r)
        return float(q["five_hour_pct"]), float(q["seven_day_pct"])
    except Exception as e:
        log(f"Quota nicht lesbar: {e}")
        return None


def stopped():
    return os.path.exists(STOP) or dt.datetime.now() >= DEADLINE


def wait_budget(est):
    """Wartet, bis 5h und Wochen-Zwischenziel einen Schritt erlauben. False = Ende."""
    last = None
    while not stopped():
        q = quota()
        cap = next((c for t, c in SLOTS if dt.datetime.now() < t), 98)
        if q:
            five, week = q
            if week >= 98:
                log(f"Wochenstopp {week} %")
                return False
            if five + est <= HARD_5H and week < cap:
                return True
            why = f"5h {five} % (+{est}), Woche {week} % / Ziel {cap} %"
            if why != last:
                log("Pause: " + why)
                last = why
        time.sleep(240)
    return False


def claude(prompt, model, est, name):
    """Ein schlanker Aufruf mit 5h-Watchdog. Gibt Text, None (Fehlschlag) oder False (Ende) zurueck."""
    for versuch in range(3):
        if not wait_budget(est):
            return False
        before = quota() or (0, 0)
        t0 = time.time()
        p = subprocess.Popen([CL, "-p", "--model", model, "--output-format", "json", "--tools", "", "--strict-mcp-config",
                              "--setting-sources", "", "--system-prompt", SYS], stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, cwd=f"{OUT}/leer")
        inp, killed, out = prompt, False, ""
        while True:
            try:
                out, _ = p.communicate(inp, timeout=60)
                break
            except subprocess.TimeoutExpired:
                inp = None
                q = quota()
                if os.path.exists(STOP) or (q and q[0] >= HARD_5H) or time.time() - t0 > 2400:
                    p.kill()
                    p.communicate()
                    killed = True
                    break
        after = quota() or before
        log(f"{name} ({model}) {int(time.time() - t0)} s, 5h {before[0]}->{after[0]}, Woche {before[1]}->{after[1]}"
            + (" ABGEBROCHEN" if killed else ""))
        if killed:
            est = min(est + 10, 60)
            continue
        try:
            res = json.loads(out)
            if not res.get("is_error"):
                return res["result"]
            log(f"{name}: Fehler {str(res.get('result'))[:200]}")
        except Exception as e:
            log(f"{name}: keine lesbare Antwort ({e})")
        if time.time() - t0 < 180:   # schneller Abbruch = meist Limit, nicht weiterrasen
            time.sleep(1800)
    return None


def as_json(t):
    try:
        return json.loads(t[t.index("{"):t.rindex("}") + 1])
    except Exception:
        return None


def write(path, text):
    with open(path + ".tmp", "w", encoding="utf-8") as f:
        f.write(text)
    os.replace(path + ".tmp", path)


def titel_marks(d, titel, status="uebernommen"):
    return [m for m in d["satz_markierungen"] if m.get("kapitel_titel") == titel and m.get("status") == status]


def muster(d, n=70):
    alle = [m for m in d["satz_markierungen"] if m.get("status") == "uebernommen" and m.get("vorschlag")]
    return "\n".join(f"- VORHER: {m['satz'][:260]}\n  NACHHER: {m['vorschlag'][:260]}" for m in alle[-n:])


def kontext(d):
    kanon = "\n".join(f"- {x}" for x in d.get("kanon", []))
    summ = "\n".join(f"Kap. {i}: {(k.get('zusammenfassung') or '')[:600]}" for i, k in enumerate(d["kapitel"], 1))
    return f"KANON (verbindlich):\n{kanon}\n\nZUSAMMENFASSUNGEN ALLER KAPITEL:\n{summ}"


STIL = ("Stilregel des Autors: verstaendlich, aber auf hohem literarischem Niveau; nichts glaetten. Umformulieren nur, was auch "
        "nach aufmerksamem Lesen nicht aufgeht (raetselhafte Bildsprueche, Halbsaetze ohne Gemeintes, Fadenverlust).")


def straffung(n):
    f = f"{OUT}/straffung/kap{n:02d}.txt"
    if os.path.exists(f) or os.path.exists(f + ".verworfen"):
        return True
    d = load()
    k = d["kapitel"][n - 1]
    text = k["text"]
    alt = len(text.split())
    schutz = [m["vorschlag"] for m in titel_marks(d, k["titel"]) if m.get("vorschlag") and m["vorschlag"] in text]
    schutz += [e["text"] for e in d["einschub_vorschlaege"] if e.get("kapitel_titel") == k["titel"] and e["text"] in text]
    extra = ""
    if n >= 25:
        extra = ("\nZusaetzlich: Behebe dabei Stellen derselben Fehlerklassen wie in diesen Korrekturen des Autors:\n" + muster(d, 40))
    prompt = f"""STRAFFUNG von {k['titel']} (Roman AURORA II). Kuerze um etwa 10 % (jetzt {alt} Woerter; lieber weniger als Substanz verlieren).
Kuerze nur: Nacherzaehlungen bekannter Fakten, Nachdenk-Schleifen, doppelt erklaerte Pointen, Kulissen, abgenutzte Formeln,
Rechts-Exposition. Humor und Spannung bleiben. Keine neuen Fakten, keine Zahlen/Daten/Namen aendern, Szenentrenner und
Kapitelkopf-Zeitangaben bleiben, die letzten zwei Absaetze bleiben woertlich. {STIL}
Chris-Streichungen bleiben gestrichen (Pieper, Reifenhaendler, Kollmann).
Diese Stellen bleiben WOERTLICH:
{chr(10).join('* ' + s for s in schutz) or '(keine)'}{extra}

{kontext(d)}

=== TEXT ===
{text}
=== ENDE ===

Gib NUR den vollstaendigen neuen Kapiteltext aus (Format wie Original, ohne Ueberschrift, die nicht im Original steht)."""
    fehler = ""
    for _ in range(2):
        t = claude(prompt + fehler, "opus", 25, f"straffung {n}")
        if t is False:
            return False
        if not t:
            return True
        t = t.strip()
        neu = len(t.split())
        fehlt = [s for s in schutz if s not in t]
        ende = text.rstrip().split("\n\n")[-2:]
        if 0.80 * alt <= neu <= 0.99 * alt and not fehlt and all(a.strip() in t for a in ende):
            write(f, t)
            log(f"straffung {n}: Entwurf {alt} -> {neu} W")
            return True
        fehler = f"\n\nDEIN ERSTER VERSUCH war ungueltig ({neu} Woerter, {len(fehlt)} geschuetzte Stellen fehlen oder Ende veraendert). Halte alle Regeln ein."
    write(f + ".verworfen", t)
    log(f"straffung {n}: zweimal ungueltig, verworfen")
    return True


def einbauen(n, patches, art, label):
    """Blaue Vorschlaege einbauen; liefert Zahl. Laedt frisch (Chris arbeitet parallel)."""
    if n == 38 or 19 <= n <= 28:
        return 0
    d = load()
    k = d["kapitel"][n - 1]
    text = k["text"]
    tabu = len(text) - len("\n\n".join(text.rstrip().split("\n\n")[-2:]))
    belegt = [e["text"] for e in d["einschub_vorschlaege"] if e.get("kapitel_titel") == k["titel"] and e.get("status") == "wartet"]
    belegt += [m["vorschlag"] for m in titel_marks(d, k["titel"]) if m.get("vorschlag")]
    count = 0
    for p in patches:
        z, e = (p.get("zitat") or "").strip(), (p.get("ersatz") or "").strip()
        if not z or not e or z == e or text.count(z) != 1 or e in text or text.index(z) + len(z) > tabu:
            continue
        if any(z in b or b in z for b in belegt):
            continue
        if not set(re.findall(r"\d+", z)) <= set(re.findall(r"\d+", e)) and art != "fehler":
            continue
        text = text.replace(z, e, 1)
        belegt.append(e)
        d["einschub_vorschlaege"].append({
            "id": f"ei-{art}-{n}-{uuid.uuid4().hex[:6]}", "label": label, "art_lauf": f"{art}_20261127",
            "kapitel_titel": k["titel"], "text": e, "ersetzt": z, "begruendung": p.get("begruendung", ""),
            "status": "wartet", "erstellt_am": dt.datetime.now().strftime("%Y-%m-%d %H:%M")})
        count += 1
    if count:
        shutil.copy2(BUCH, f"{W}/backups/aurora2_vor_{art}_kap{n}_{dt.datetime.now():%Y%m%d_%H%M%S}.json")
        k["text"] = text
        write(BUCH, json.dumps(d, ensure_ascii=False, indent=2))
    return count


FORMAT = ('Antworte NUR als JSON: {"funde":[{"kapitel":Kapitelnummer,"zitat":"woertlich, genau einmal im Kapitel, ganzer Satz",'
          '"ersatz":"korrigierte Fassung derselben Stelle","begruendung":"1 Satz","sicherheit":"hoch|mittel"}]} - '
          "im Zweifel nichts melden, leere Liste ist ein gutes Ergebnis.")


def analogie(n):
    f = f"{OUT}/analogie/kap{n:02d}.json"
    if os.path.exists(f):
        return True
    d = load()
    k = d["kapitel"][n - 1]
    prompt = f"""ANALOGIE-CHECK {k['titel']} (Roman AURORA II). Der Autor hat anderswo die folgenden Stellen korrigiert. Leite daraus die
Fehlerklassen ab und finde im Kapitel Stellen derselben Klasse. {STIL} Hoechstens 8 Funde.

KORREKTUREN DES AUTORS:
{muster(d)}

{kontext(d)}

=== {k['titel']} ===
{k['text']}
=== ENDE ===

{FORMAT}"""
    t = claude(prompt, "opus", 20, f"analogie {n}")
    if t is False:
        return False
    j = as_json(t) if t else None
    if j is None:
        return True
    hoch = [p for p in j.get("funde", []) if p.get("sicherheit") == "hoch"]
    c = einbauen(n, hoch, "analogie", "Analogie-Check")
    j["eingebaut"] = c
    write(f, json.dumps(j, ensure_ascii=False, indent=1))
    log(f"analogie {n}: {len(j.get('funde', []))} Funde, {c} blau")
    return True


def vorwort():
    f = f"{OUT}/vorwort_check.json"
    if os.path.exists(f):
        return True
    d = load()
    t = claude(f"""Pruefe, ob das Vorwort (inkl. 'Was bisher geschah') noch zum fertigen Roman AURORA II passt: Widersprueche,
falsche Versprechen, Spoiler. Nichts am Buch aendern.\n\n{kontext(d)}\n\n=== VORWORT ===\n{d['vorwort']}\n\n{FORMAT}""",
               "opus", 12, "vorwort")
    if t is False:
        return False
    if t:
        write(f, t)
    return True


LINSEN = {
    "zeit": "Zeitlinie, Daten, Wochentage, Uhrzeiten, Dauern, Alter, Zahlen (Tag 0 = 16. Oktober)",
    "wissen": "Wissensstaende: wer weiss wann was, wer war wo, wer kann das ueberhaupt wissen",
    "namen": "Namen, Rollen, Titel, Orte, Gegenstaende, Dokumente (verwechselt oder wechselnd bezeichnet)",
    "logik": "Handlungslogik: Gegenstaende oder Personen, die verschwinden oder auftauchen, unmoegliche Ablaeufe, Widerspruch zu frueheren Kapiteln",
    "sprache": "echte Sprachfehler: Grammatik, Rechtschreibung, fehlende oder doppelte Woerter, falscher Bezug (KEINE Stilfragen)",
}
BLOECKE = [(1, 8), (9, 16), (17, 24), (25, 32), (33, 40)]


def fehler(linse, a, b):
    base = f"{OUT}/fehler/{linse}_{a:02d}"
    if os.path.exists(base + ".json"):
        return True
    d = load()
    text = "\n\n".join(f"=== {k['titel']} ===\n{k['text']}" for k in d["kapitel"][a - 1:b])
    if os.path.exists(base + "_kandidaten.json"):
        kand = json.load(open(base + "_kandidaten.json", encoding="utf-8"))
    else:
        t = claude(f"FEHLERJAGD Kap. {a}-{b} (Roman AURORA II). Suche nur: {LINSEN[linse]}.\n\n{kontext(d)}\n\n{text}\n\n{FORMAT}",
                   "sonnet", 15, f"fehler {linse} {a}")
        if t is False:
            return False
        kand = as_json(t) if t else None
        if kand is None:
            return True
        write(base + "_kandidaten.json", json.dumps(kand, ensure_ascii=False, indent=1))
    funde = []
    if kand.get("funde"):
        nrs = sorted({int(x["kapitel"]) for x in kand["funde"] if str(x.get("kapitel", "")).isdigit() and a <= int(x["kapitel"]) <= b})
        teil = "\n\n".join(f"=== {d['kapitel'][i - 1]['titel']} ===\n{d['kapitel'][i - 1]['text']}" for i in nrs)
        t = claude(f"""Gegenpruefung. Ein erster Leser meldet moegliche Fehler. Bestaetige NUR, was am Text wirklich ein Fehler ist
(keine absichtlichen Raetsel, keine Stilfragen). {STIL}\n\n{kontext(d)}\n\n{teil}\n\nMELDUNGEN:\n{json.dumps(kand, ensure_ascii=False)}\n\n{FORMAT}""",
                   "opus", 20, f"pruefung {linse} {a}")
        if t is False:
            return False
        j = as_json(t) if t else None
        if j is None:
            return True
        funde = j.get("funde", [])
    c = 0
    for n in range(a, b + 1):
        ps = [p for p in funde if str(p.get("kapitel")) == str(n) and p.get("sicherheit") == "hoch"]
        if ps:
            c += einbauen(n, ps, "fehler", f"Fehlerjagd ({linse})")
    write(base + ".json", json.dumps({"funde": funde, "eingebaut": c}, ensure_ascii=False, indent=1))
    log(f"fehler {linse} {a}-{b}: {len(funde)} bestaetigt, {c} blau")
    return True


def tasks():
    for n in range(19, 29):
        yield lambda n=n: straffung(n)
    for n in (34, 35, 36, 37, 38, 39, 40, 29, 30, 31, 32, 33):
        yield lambda n=n: analogie(n)
    yield vorwort
    for linse in LINSEN:
        for a, b in BLOECKE:
            yield lambda x=linse, a=a, b=b: fehler(x, a, b)


def main():
    lock = open("/tmp/ausreizen_fr27.lock", "w")
    try:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except OSError:
        return
    if stopped() or os.path.exists(f"{OUT}/fertig"):
        return
    log(f"START quota {quota()}")
    komplett = True
    for t in tasks():
        try:
            if stopped() or t() is False:
                komplett = False
                break
        except Exception as e:
            log(f"Fehler: {e!r}")
    q = quota()
    text = f"{'Alle Pakete durch' if komplett else 'Beendet (Deadline/Wochenstopp/Notbremse)'}; Quota 5h/Woche {q}. Ordner scratch/ausreizen_20261127."
    log("ENDE " + text)
    write(f"{OUT}/fertig", text)
    try:
        sys.path.insert(0, f"{W}/scripts")
        from job_status import report
        report("ausreizen_fr27", "AURORA II Ausreizen 27./28.11.", "ok", text)
    except Exception as e:
        log(f"job_status: {e}")


if __name__ == "__main__":
    main()
