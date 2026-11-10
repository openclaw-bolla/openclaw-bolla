#!/usr/bin/env python3
"""Englisch-Trainer (MP Familie + mmp Einstiegsseite) - Backend-Logik.

Wird von mission_control_api.py importiert (Routen /api/englisch/*).
Daten:  data/englisch/YYYY-MM-DD.json   Tages-Set (vom Cron englisch_generate.py)
        data/englisch/img/*             Bilder (Cloudflare Workers AI)
        data/englisch_fortschritt.json  Fortschritt/Streak/Statistik (geraeteuebergreifend)
"""
import datetime as dt
import fcntl
import glob
import json
import os
import re
import subprocess
import sys
import threading

WS = os.path.expanduser("~/workspace")
DIR = os.path.join(WS, "data", "englisch")
IMG = os.path.join(DIR, "img")
FORT = os.path.join(WS, "data", "englisch_fortschritt.json")
LOCK = FORT + ".lock"
CLAUDE = os.path.expanduser("~/.local/bin/claude")
ZIEL_MIN = 12
FEEDBACK_MAX_PRO_TAG = 8
_mem = threading.Lock()


def heute_str():
    return dt.date.today().isoformat()


def _lade_fort():
    try:
        with open(FORT, encoding="utf-8") as f:
            d = json.load(f)
    except Exception:
        d = {}
    d.setdefault("tage", {})
    d.setdefault("woerter", {})
    return d


def _speichere_fort(d):
    tmp = FORT + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=1)
    os.replace(tmp, FORT)


class _Sperre:
    """Prozessuebergreifende Sperre (Server + Cron lesen/schreiben dieselbe JSON)."""
    def __enter__(self):
        _mem.acquire()
        self.f = open(LOCK, "w")
        fcntl.flock(self.f, fcntl.LOCK_EX)
        return self

    def __exit__(self, *a):
        fcntl.flock(self.f, fcntl.LOCK_UN)
        self.f.close()
        _mem.release()


def sets_vorhanden():
    return sorted(os.path.basename(p)[:-5] for p in glob.glob(os.path.join(DIR, "????-??-??.json")))


def lade_set(datum):
    p = os.path.join(DIR, datum + ".json")
    if not os.path.isfile(p):
        return None
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def _generator_anstossen():
    """Fehlt das Tages-Set, im Hintergrund erzeugen (hoechstens alle 20 min)."""
    marker = os.path.join(DIR, ".generator_start")
    try:
        if os.path.exists(marker) and dt.datetime.now().timestamp() - os.path.getmtime(marker) < 1200:
            return False
        open(marker, "w").close()
        subprocess.Popen([sys.executable, os.path.join(WS, "scripts", "englisch_generate.py"), "--heute"],
                         stdout=open(os.path.join(WS, "logs", "englisch_generate.log"), "a"),
                         stderr=subprocess.STDOUT, start_new_session=True)
        return True
    except Exception:
        return False


WOERTER = os.path.join(WS, "data", "englisch_woerter.json")
GELERNT_AB = 3        # so oft in Folge gewusst -> "gelernt"


def _lade_w():
    try:
        with open(WOERTER, encoding="utf-8") as f:
            d = json.load(f)
        return d if isinstance(d, list) else []
    except Exception:
        return []


def _speichere_w(d):
    tmp = WOERTER + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=1)
    os.replace(tmp, WOERTER)


TRANS_CACHE = os.path.join(DIR, "trans_cache.json")


def _cf_translate(text):
    import urllib.request
    try:
        c = json.load(open(os.path.join(WS, "config", "cloudflare_token.json")))
        url = f"https://api.cloudflare.com/client/v4/accounts/{c['account_id']}/ai/run/@cf/meta/m2m100-1.2b"
        r = urllib.request.Request(url, data=json.dumps({"text": text, "source_lang": "english", "target_lang": "german"}).encode(),
                                   headers={"Authorization": "Bearer " + c["api_token"], "Content-Type": "application/json"})
        j = json.loads(urllib.request.urlopen(r, timeout=30).read())
        return (j.get("result") or {}).get("translated_text") or ""
    except Exception:
        return ""


def uebersetzen(body):
    """Fallback-Uebersetzung EN->DE (Cloudflare m2m100, kostenlos), mit Cache. body: {text}"""
    text = re.sub(r"\s+", " ", str(body.get("text") or "")).strip()[:600]
    if not text:
        return {"error": "kein Text"}
    try:
        cache = json.load(open(TRANS_CACHE, encoding="utf-8"))
    except Exception:
        cache = {}
    if text in cache:
        return {"ok": True, "de": cache[text], "maschinell": True}
    de = _cf_translate(text)
    if not de:
        return {"error": "Übersetzung gerade nicht möglich"}
    cache[text] = de
    try:
        with open(TRANS_CACHE, "w", encoding="utf-8") as f:
            json.dump(cache, f, ensure_ascii=False)
    except Exception:
        pass
    return {"ok": True, "de": de, "maschinell": True}


def _beispiel_haiku(en):
    """1 kurzer Beispielsatz zu einem Wort (nur wenn Chris ein Wort von Hand eintraegt). Leer bei Limit/Fehler."""
    try:
        sys.path.insert(0, os.path.join(WS, "scripts"))
        import limit_gate
        r = limit_gate.run([CLAUDE, "-p", "--model", "haiku", "Schreibe genau EINEN natürlichen englischen Beispielsatz (max. 15 Wörter, Niveau B2) mit dem Ausdruck: " + en + " . Antworte NUR mit dem Satz."],
                           capture_output=True, text=True, timeout=60, wait=False, cwd=WS)
        if r.returncode == 0:
            return (r.stdout or "").strip().split("\n")[0][:300]
    except Exception:
        pass
    return ""


def woerter_liste():
    with _Sperre():
        w = _lade_w()
    return {"woerter": w, "offen": sum(1 for x in w if x.get("streak", 0) < GELERNT_AB), "gelernt": sum(1 for x in w if x.get("streak", 0) >= GELERNT_AB)}


def wort_add(body):
    """Wort merken. body: {en, de?, bsp?, bild?}. Dubletten (gleiches en) werden zurueckgesetzt statt doppelt."""
    en = str(body.get("en") or "").strip()[:80]
    if not en:
        return {"error": "Wort fehlt"}
    de = str(body.get("de") or "").strip()[:300]
    bsp = str(body.get("bsp") or "").strip()[:400]
    bild = os.path.basename(str(body.get("bild") or ""))[:80]
    if not de:
        de = _cf_translate(en)[:300]          # kostenlos (Cloudflare); bei Phrasen/Saetzen ok
    if not bsp and len(en.split()) <= 6:
        bsp = _beispiel_haiku(en)             # kleiner Zusatz-Call, nur fuer von Hand eingetragene Woerter
    with _Sperre():
        w = _lade_w()
        for x in w:
            if x["en"].lower() == en.lower():
                x["streak"] = 0
                if de and not x.get("de"):
                    x["de"] = de
                if bsp and not x.get("bsp"):
                    x["bsp"] = bsp
                _speichere_w(w)
                return {"ok": True, "neu": False, "anzahl": len(w)}
        w.append({"id": "w" + dt.datetime.now().strftime("%y%m%d%H%M%S%f")[:15], "en": en, "de": de, "bsp": bsp, "bild": bild,
                  "streak": 0, "gesehen": 0, "gewusst": 0, "letzte": "", "hinzu": heute_str()})
        _speichere_w(w)
    return {"ok": True, "neu": True, "anzahl": len(w)}


def wort_ergebnis(body):
    wid = str(body.get("id") or "")
    gewusst = bool(body.get("gewusst"))
    with _Sperre():
        w = _lade_w()
        for x in w:
            if x["id"] == wid:
                x["gesehen"] = x.get("gesehen", 0) + 1
                x["letzte"] = heute_str()
                if gewusst:
                    x["gewusst"] = x.get("gewusst", 0) + 1
                    x["streak"] = x.get("streak", 0) + 1
                else:
                    x["streak"] = 0
                _speichere_w(w)
                return {"ok": True, "gelernt": x["streak"] >= GELERNT_AB}
    return {"error": "unbekannt"}


def wort_loeschen(body):
    wid = str(body.get("id") or "")
    with _Sperre():
        w = [x for x in _lade_w() if x["id"] != wid]
        _speichere_w(w)
    return {"ok": True}


def _woerter_aufgabe(d, n=5):
    import random
    with _Sperre():
        w = _lade_w()
    offen = [x for x in w if x.get("streak", 0) < GELERNT_AB]
    if not offen:
        return None
    frisch = [x for x in offen if x.get("letzte") != d] or []
    if not frisch:
        return None
    # je weniger Streak, desto oefter (Gewicht 3,2,1)
    pool, pick = list(frisch), []
    while pool and len(pick) < n:
        g = [GELERNT_AB - x.get("streak", 0) for x in pool]
        x = random.choices(pool, weights=g)[0]
        pool.remove(x)
        pick.append(x)
    return {"id": "aW", "slot": "karten", "typ": "karten", "kat": "Meine Wörter", "titel": "Meine Wörter (Karteikarten)",
            "min": round(0.4 * len(pick) + 0.4, 1), "anweisung": "Wörter, die du dir gemerkt hast. 3× in Folge gewusst = gelernt, sonst kommen sie wieder.",
            "items": [{"wid": x["id"], "en": x["en"], "de": x.get("de", ""), "bsp": x.get("bsp", ""), "bild": x.get("bild", ""), "streak": x.get("streak", 0)} for x in pick]}


def heute():
    """Tages-Set + Stand von heute. Fehlt es, kommt das juengste Set als Wiederholung und der Generator startet."""
    d = heute_str()
    s = lade_set(d)
    hinweis = None
    if not s:
        alle = [x for x in sets_vorhanden() if x < d]
        gestartet = _generator_anstossen()
        if alle:
            s = lade_set(alle[-1])
            s["wiederholung_von"] = alle[-1]
            hinweis = "Heute ist noch kein neues Set da – Wiederholung vom " + alle[-1] + (". Frisches Set wird gerade erzeugt." if gestartet else ".")
        else:
            return {"fehler": "Noch kein Tages-Set vorhanden. Es wird gerade erzeugt – in ein bis zwei Minuten neu laden." if gestartet else "Noch kein Tages-Set vorhanden."}
    with _Sperre():
        fort = _lade_fort()
    tag = fort["tage"].get(d, {})
    try:
        kw = _woerter_aufgabe(d) if not s.get("wiederholung_von") or True else None
        if kw:
            s = dict(s)
            s["aufgaben"] = [kw] + [a for a in s["aufgaben"] if a.get("id") != "aW"]
    except Exception:
        pass
    return {"datum": d, "set": s, "hinweis": hinweis, "heute": tag, "ziel_min": s.get("ziel_min", ZIEL_MIN)}


def _tag_geschafft(tag, n_aufgaben):
    n = len(tag.get("ergebnisse", {}))
    return n_aufgaben > 0 and (n / n_aufgaben >= 0.7 or tag.get("sek", 0) >= 600)


def statistik(fort=None):
    if fort is None:
        with _Sperre():
            fort = _lade_fort()
    heute_d = dt.date.today()
    tage = fort["tage"]
    # Streak: aufeinanderfolgende "geschaffte" Tage, endend heute oder gestern
    def geschafft(dstr):
        t = tage.get(dstr)
        if not t:
            return False
        s = lade_set(dstr)
        n = len(s["aufgaben"]) if s else max(1, len(t.get("ergebnisse", {})))
        return _tag_geschafft(t, n)
    streak, bester = 0, 0
    d = heute_d
    if not geschafft(d.isoformat()):
        d -= dt.timedelta(days=1)
    while geschafft(d.isoformat()):
        streak += 1
        d -= dt.timedelta(days=1)
    # bester Streak
    lauf, prev = 0, None
    for ds in sorted(tage):
        if geschafft(ds):
            dd = dt.date.fromisoformat(ds)
            lauf = lauf + 1 if prev and (dd - prev).days == 1 else 1
            bester = max(bester, lauf)
            prev = dd
    # letzte 7 Tage
    woche = []
    for i in range(6, -1, -1):
        ds = (heute_d - dt.timedelta(days=i)).isoformat()
        t = tage.get(ds, {})
        er = t.get("ergebnisse", {})
        sc = [e["score"] for e in er.values()]
        woche.append({"datum": ds, "min": round(t.get("sek", 0) / 60, 1), "aufgaben": len(er),
                      "score": round(100 * sum(sc) / len(sc)) if sc else None, "geschafft": geschafft(ds)})
    # Kategorien (14 Tage)
    kat = {}
    grenze = (heute_d - dt.timedelta(days=14)).isoformat()
    for ds, t in tage.items():
        if ds < grenze:
            continue
        for e in t.get("ergebnisse", {}).values():
            k = kat.setdefault(e.get("kat", "?"), [0.0, 0])
            k[0] += e["score"]
            k[1] += 1
    kategorien = sorted(({"kat": k, "score": round(100 * s / n), "n": n} for k, (s, n) in kat.items()), key=lambda x: x["score"])
    pron = [e["score"] for t in tage.values() for e in t.get("ergebnisse", {}).values() if e.get("typ") in ("read", "speak")]
    schwach = sorted(({"wort": w, "n": v["n"], "acc": round(v["acc"])} for w, v in fort["woerter"].items() if v["acc"] < 75),
                     key=lambda x: (x["acc"], -x["n"]))[:10]
    gesamt_min = round(sum(t.get("sek", 0) for t in tage.values()) / 60)
    return {"streak": streak, "bester_streak": bester, "woche": woche, "kategorien": kategorien,
            "aussprache_schnitt": round(100 * sum(pron) / len(pron)) if pron else None,
            "schwache_woerter": schwach, "tage_gesamt": len([1 for t in tage.values() if t.get("ergebnisse")]),
            "minuten_gesamt": gesamt_min}


def fortschritt():
    with _Sperre():
        fort = _lade_fort()
    return {"stat": statistik(fort), "heute": fort["tage"].get(heute_str(), {})}


def ergebnis(body):
    """Ein Aufgaben-Ergebnis speichern. body: {datum?, id, typ, kat, titel, score(0..1), sek, woerter?:[{w,acc}]}"""
    try:
        aid = str(body["id"])[:20]
        score = max(0.0, min(1.0, float(body["score"])))
    except Exception:
        return {"error": "id/score fehlen"}
    d = str(body.get("datum") or heute_str())
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", d):
        return {"error": "Datum ungueltig"}
    sek = max(0, min(600, int(body.get("sek") or 0)))
    with _Sperre():
        fort = _lade_fort()
        tag = fort["tage"].setdefault(d, {"ergebnisse": {}, "sek": 0, "feedback_n": 0})
        alt = tag["ergebnisse"].get(aid)
        if alt:                       # Wiederholung derselben Aufgabe: Zeit addieren, bester Score zaehlt
            tag["sek"] = tag.get("sek", 0) + sek
            alt["score"] = max(alt["score"], score)
            alt["sek"] = alt.get("sek", 0) + sek
        else:
            tag["ergebnisse"][aid] = {"typ": str(body.get("typ", ""))[:12], "kat": str(body.get("kat", ""))[:40],
                                       "titel": str(body.get("titel", ""))[:60], "score": round(score, 3), "sek": sek,
                                       "ts": dt.datetime.now().strftime("%H:%M")}
            tag["sek"] = tag.get("sek", 0) + sek
        for w in (body.get("woerter") or [])[:30]:
            try:
                wort = re.sub(r"[^a-z']", "", str(w["w"]).lower())[:30]
                acc = float(w["acc"])
            except Exception:
                continue
            if not wort:
                continue
            v = fort["woerter"].setdefault(wort, {"n": 0, "acc": acc})
            v["acc"] = round(0.6 * v["acc"] + 0.4 * acc, 1) if v["n"] else acc   # gleitender Mittelwert
            v["n"] += 1
        _speichere_fort(fort)
        st = statistik(fort)
    return {"ok": True, "stat": st, "heute": tag}


def zeit_addieren(body):
    """Reine Lern-/Sichtzeit (z. B. beim Lesen von Erklaerungen) gutschreiben."""
    d = heute_str()
    sek = max(0, min(300, int(body.get("sek") or 0)))
    with _Sperre():
        fort = _lade_fort()
        tag = fort["tage"].setdefault(d, {"ergebnisse": {}, "sek": 0, "feedback_n": 0})
        tag["sek"] = tag.get("sek", 0) + sek
        _speichere_fort(fort)
    return {"ok": True}


FEEDBACK_PROMPT = """Du bist ein erfahrener, freundlicher Englischlehrer (C1-Niveau) für einen deutschsprachigen Lerner (Chris, IT-Profi/Lehrer, fortgeschritten).
Aufgabe an den Lerner: {aufgabe}
Sein Text:
\"\"\"{text}\"\"\"
Bewerte knapp und konkret. Antworte AUSSCHLIESSLICH mit einem JSON-Objekt, ohne Markdown-Zaun:
{{"korrigiert": "korrigierte, natürlichere Version des Textes (Englisch, Inhalt beibehalten)",
 "fehler": [{{"falsch": "Original-Ausschnitt", "richtig": "Korrektur", "erklaerung": "kurze Erklärung auf Deutsch"}}],
 "stark": "ein konkreter Satz auf Deutsch, was gut war",
 "tipp": "ein konkreter Tipp auf Deutsch fürs nächste Mal (z. B. eine bessere Formulierung/Collocation)",
 "note": 0.0}}
note = Zahl 0.0-1.0 (Grammatik, Wortschatz, Natürlichkeit). Maximal 6 Fehler, nur echte; wenn nichts falsch ist: leere Liste. Nichts erfinden."""


def feedback(body):
    text = str(body.get("text") or "").strip()[:2500]
    aufgabe = str(body.get("aufgabe") or "")[:600]
    if len(text) < 8:
        return {"error": "Text zu kurz für Feedback."}
    with _Sperre():
        fort = _lade_fort()
        tag = fort["tage"].setdefault(heute_str(), {"ergebnisse": {}, "sek": 0, "feedback_n": 0})
        if tag.get("feedback_n", 0) >= FEEDBACK_MAX_PRO_TAG:
            return {"error": f"Für heute sind {FEEDBACK_MAX_PRO_TAG} Feedbacks aufgebraucht (Limit-Schutz). Morgen wieder!"}
        tag["feedback_n"] = tag.get("feedback_n", 0) + 1
        _speichere_fort(fort)
    sys.path.insert(0, os.path.join(WS, "scripts"))
    try:
        import limit_gate
        r = limit_gate.run([CLAUDE, "-p", "--model", "sonnet", FEEDBACK_PROMPT.format(aufgabe=aufgabe, text=text)],
                           capture_output=True, text=True, timeout=120, wait=False, cwd=WS)
    except Exception as e:
        return {"error": "Feedback nicht möglich: " + str(e)[:150]}
    if r.returncode == 75:
        return {"error": "Gerade ist das Claude-Limit knapp – Feedback später nochmal versuchen. Dein Text ist trotzdem gespeichert."}
    out = (r.stdout or "").strip()
    m = re.search(r"\{.*\}", out, re.S)
    if r.returncode != 0 or not m:
        return {"error": "Feedback leer/fehlerhaft (" + (r.stderr or out)[:120] + ")"}
    try:
        j = json.loads(m.group(0))
        j["note"] = max(0.0, min(1.0, float(j.get("note", 0.6))))
        return {"ok": True, "feedback": j}
    except Exception:
        return {"error": "Feedback nicht lesbar."}


def bild_pfad(name):
    name = os.path.basename(name)
    p = os.path.join(IMG, name)
    return p if os.path.isfile(p) else None
