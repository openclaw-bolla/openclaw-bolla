#!/usr/bin/env python3
"""Erzeugt Englisch-Trainer-Tagessets (data/englisch/YYYY-MM-DD.json) + Cloudflare-Bilder.

Aufruf:  englisch_generate.py            -> heute + 2 Folgetage auffuellen (Cron nachts)
         englisch_generate.py --heute    -> nur heute (wenn es fehlt)
         englisch_generate.py --datum 2026-11-12 [--force]
Pro Tag EIN `claude -p --model sonnet` (ueber limit_gate, wait=False -> bei knappem Limit ueberspringen,
naechster Cron-Lauf holt es nach). Bilder: Cloudflare Workers AI flux-1-schnell (kostenlos).
"""
import argparse
import base64
import datetime as dt
import json
import os
import random
import re
import sys

WS = os.path.expanduser("~/workspace")
sys.path.insert(0, os.path.join(WS, "scripts"))
import limit_gate  # noqa: E402
from job_status import report  # noqa: E402
import englisch_api as api  # noqa: E402

CLAUDE = os.path.expanduser("~/.local/bin/claude")
JOB = "englisch-tagesset"
TITEL = "Englisch-Trainer: Tagesset"

# slot: (typ, kategorie, anzeigetitel, minuten, anzahl_items)
POOL = {
    "colloc":    ("mc", "Wortschatz", "Collocations", 1.3, 4),
    "nuance":    ("mc", "Wortschatz", "Nuancen & Wortwahl", 1.3, 4),
    "register":  ("mc", "Stil", "Formal vs. informell", 1.3, 4),
    "phrasal":   ("input", "Phrasal Verbs", "Phrasal Verbs", 1.5, 4),
    "idiom":     ("input", "Idiome", "Idioms & Redewendungen", 1.5, 4),
    "grammar":   ("input", "Grammatik", "Advanced Grammar", 1.5, 4),
    "wordform":  ("input", "Wortbildung", "Word Formation", 1.3, 4),
    "fehler":    ("fehler", "Fehlerjagd", "Fehlerjagd", 1.3, 4),
    "listen":    ("listen", "Hörverstehen", "Listening", 2.2, 3),
    "rewrite":   ("selfcheck", "Umformulieren", "Sentence Transformation", 2.0, 3),
    "translate": ("selfcheck", "Übersetzen", "Deutsch → Englisch", 2.0, 3),
    "bild":      ("selfcheck", "Bildbeschreibung", "Describe the Picture", 2.5, 1),
    "write":     ("selfcheck", "Schreiben", "Kurz schreiben (mit Bolla-Feedback)", 2.5, 1),
    "read":      ("read", "Aussprache", "Laut lesen", 1.5, 2),
    "speak":     ("speak", "Sprechen", "Frei sprechen", 1.5, 1),
}

THEMEN = [
    "a chaotic business trip", "negotiating a rental contract", "tech support at the worst possible moment",
    "a small-town festival", "cooking disasters and triumphs", "remote work and its side effects",
    "train travel in Europe", "a hiking trip that went sideways", "school life and teaching", "healthy habits and sport",
    "electric cars and charging", "neighbours and noise", "a job interview", "the weather and small talk",
    "online shopping gone wrong", "a family reunion", "museum and exhibition visit", "smart-home gadgets",
    "a city break in London or Edinburgh", "customer complaints", "learning a new skill late in life",
    "photography and travel memories", "a power cut at work", "the news: a local scandal",
    "airport delays", "a surprise birthday party", "AI at work and in schools", "moving house",
    "a restaurant with a mixed-up order", "volunteering and community",
]
STIMMEN = ["en-GB-SoniaNeural", "en-GB-RyanNeural", "en-US-AriaNeural", "en-US-GuyNeural", "en-US-JennyNeural"]


def waehle_slots(datum):
    rng = random.Random(datum)
    s = ["read"]
    s += rng.sample(["colloc", "nuance", "register"], rng.choice([1, 2]))
    s += rng.sample(["phrasal", "idiom", "grammar", "wordform"], 2)
    if rng.random() < 0.55:
        s.append("fehler")
    if rng.random() < 0.6:
        s.append("listen")
    s.append(rng.choice(["rewrite", "translate"]))
    s.append("bild" if rng.random() < 0.5 else "write")
    if rng.random() < 0.65:
        s.append("speak")

    def summe():
        return sum(POOL[k][3] for k in s)
    reihenfolge_vorzug = ["colloc", "nuance", "register", "fehler", "phrasal", "idiom"]
    while summe() > 14.0:                       # zu lang: letzte "Extra"-Aufgabe raus
        for k in ("write", "bild", "speak", "listen", "nuance", "register", "fehler"):
            if k in s:
                s.remove(k)
                break
    for k in reihenfolge_vorzug:                # zu kurz: auffuellen
        if summe() >= 11.0:
            break
        if k not in s:
            s.append(k)
    # Lernreihenfolge: leicht -> schwer -> sprechen am Ende
    ordnung = ["colloc", "nuance", "register", "phrasal", "idiom", "grammar", "wordform", "fehler", "listen",
               "rewrite", "translate", "bild", "write", "read", "speak"]
    return sorted(s, key=ordnung.index), round(summe(), 1)


def verlauf(datum, n=30):
    lem, themen = [], []
    for d in api.sets_vorhanden()[-n:]:
        if d >= datum:
            continue
        s = api.lade_set(d) or {}
        lem += s.get("lemmas", [])
        if s.get("thema"):
            themen.append(s["thema"])
    return lem[-200:], themen[-8:]


def baue_prompt(datum, slots, thema):
    stat = api.statistik()
    lem, alte_themen = verlauf(datum)
    schwach_kat = [k["kat"] for k in stat["kategorien"][:3] if k["score"] < 80]
    schwach_w = [w["wort"] for w in stat["schwache_woerter"][:8]]
    liste = []
    for i, k in enumerate(slots, 1):
        typ, kat, titel, minu, n = POOL[k]
        liste.append(f'  a{i}: Slot "{k}" -> typ "{typ}", kat "{kat}", titel "{titel}", {n} Item(s)')
    return f"""Du erzeugst das heutige Tagesset ({datum}) für einen Englisch-Trainer. Lerner: Chris, Deutsch als Muttersprache, IT-erfahren, Lehrer, Niveau B2→C1 (Cambridge Advanced). Ziel: täglich 10–15 Minuten, abwechslungsreich, anspruchsvoll aber fair. Aufgabentexte Englisch; Anweisungen und Erklärungen auf DEUTSCH (kurz, freundlich, ein Hauch trockener Humor erlaubt).
Tagesthema (lose Klammer für Sätze und Texte, nicht stur): {thema}.
Bereits abgefragt (NICHT wiederholen): {", ".join(lem[-120:]) or "–"}. Letzte Themen: {", ".join(alte_themen) or "–"}.
Schwerpunkte des Lerners (gerne etwas häufiger bedienen): {", ".join(schwach_kat) or "keine"}; Aussprache-Problemwörter (in 'read' einbauen, falls sinnvoll): {", ".join(schwach_w) or "keine"}.

Erzeuge GENAU diese Aufgaben in dieser Reihenfolge:
{chr(10).join(liste)}

Formatvorgaben je typ (alle Felder Pflicht, nur ein JSON-Objekt, KEIN Markdown-Zaun, keine Kommentare):
- mc: "anweisung" (de), "items": [{{"frage": "Satz mit ___ oder Frage (en)", "optionen": ["..","..","..",".."], "richtig": Index 0-3, "erklaerung": "de, 1–2 Sätze, nenne den Unterschied"}}]. Optionen plausibel, nur eine korrekt; Richtig-Position variieren.
- input: "anweisung" (de), "items": [{{"frage": "englischer Satz mit ___ (oder Wort/Impuls bei Word Formation, z. B. 'He showed great ___ (DETERMINE)')", "antworten": ["akzeptierte Lösung", "weitere akzeptierte Variante"], "hinweis": "kurzer Hinweis de oder leer", "erklaerung": "de"}}]. Lösung = genau das einzutippende Wort/Wortgruppe (klein, ohne Satzzeichen), alle gängigen korrekten Varianten in "antworten".
- fehler: "anweisung" (de), "items": [{{"teile": ["Satz","in","3–7","Teile","zerlegt"], "falsch": Index des Teils mit dem Fehler, "korrektur": "korrekter Ausdruck für diesen Teil", "erklaerung": "de, typischer Fehler Deutschsprachiger (z. B. false friends, Präpositionen, Zeitformen)"}}]. Genau EIN Fehler pro Satz.
- listen: "text": "60–90 Wörter, ein Sprecher oder kurzer Dialog als Fließtext (ohne Sprechernamen)", "anweisung": "de", "items": 3x mc-Item (Verständnisfragen, die man nur mit Zuhören beantwortet).
- selfcheck: "anweisung" (de), "items": [{{"aufgabe": "...", "loesungen": ["Musterlösung 1", "Variante 2"], "hinweis": "optional de", "feedback": false}}].
    rewrite: aufgabe = Originalsatz + Vorgabe (z. B. 'Rewrite using an inversion: ...'). translate: aufgabe = deutscher Satz (idiomatisch, nicht wörtlich übersetzbar). write: 1 Item, aufgabe = kleine Schreibaufgabe (40–70 Wörter, Alltag/Beruf), "feedback": true, loesungen = 1 gute Beispielantwort.
    bild: 1 Item mit zusätzlich "bild_prompt": "englischer Prompt für ein Bild-Modell, eine konkrete, detailreiche Alltagsszene, KEIN Text im Bild, fotorealistisch", "aufgabe": "Describe the picture in 4–5 sentences. (Hinweise)", "vokabeln": ["5–6 Schlüsselwörter/Phrasen"], "loesungen": ["Musterbeschreibung 60–80 Wörter, passt exakt zum bild_prompt"], "feedback": true.
- read: "fokus": "Laut/Thema (de, z. B. 'stimmloses th, w/v')", "tipp": "de, 1–2 Sätze Aussprachetipp", "saetze": [2 Sätze, je 12–18 Wörter, natürlich klingend, viele knifflige Laute für Deutschsprachige: th, w/v, -ed-Endungen, Wortbetonung, Verbindungen].
- speak: "frage": "offene Frage/Szenario (en), Antwort ca. 30–45 s", "min_sek": 30, "hilfen": [4 nützliche Phrasen/Redemittel (en)], "anweisung": "de".

Zusätzlich auf oberster Ebene: "thema": "{thema}" (oder verfeinert, en), "gruss": "1 kurzer launiger Satz auf Deutsch von Bolla zum heutigen Tag (max. 140 Zeichen)", "lemmas": ["20–30 Schlüsselbegriffe/Phrasen dieses Sets, englisch, für die Wiederholungsvermeidung"], "aufgaben": [ {{"id": "a1", "slot": "<slot>", ...Felder gemäß typ...}}, ... ].
Qualität: korrektes, natürliches britisches/amerikanisches Englisch, keine erfundenen Redewendungen; Erklärungen sachlich richtig. Nur JSON."""


def parse_json(text):
    m = re.search(r"\{.*\}", text, re.S)
    if not m:
        raise ValueError("kein JSON in der Antwort")
    return json.loads(m.group(0))


def pruefe_und_normalisiere(j, slots, datum):
    if not isinstance(j.get("aufgaben"), list):
        raise ValueError("aufgaben fehlt")
    by_slot = {}
    for a in j["aufgaben"]:
        by_slot[a.get("slot")] = a
    ergebnis = []
    for i, k in enumerate(slots, 1):
        a = by_slot.get(k) or (j["aufgaben"][i - 1] if len(j["aufgaben"]) >= i else None)
        if not a:
            raise ValueError(f"Aufgabe {k} fehlt")
        typ, kat, titel, minu, n = POOL[k]
        a.update({"id": f"a{i}", "slot": k, "typ": typ, "kat": kat, "titel": titel, "min": minu})
        items = a.get("items") or []
        if typ in ("mc", "listen"):
            for it in items:
                if not (isinstance(it.get("optionen"), list) and len(it["optionen"]) >= 2 and isinstance(it.get("richtig"), int)
                        and 0 <= it["richtig"] < len(it["optionen"]) and it.get("frage")):
                    raise ValueError(f"{k}: mc-Item kaputt")
        if typ == "input":
            for it in items:
                if not (it.get("frage") and isinstance(it.get("antworten"), list) and it["antworten"]):
                    raise ValueError(f"{k}: input-Item kaputt")
        if typ == "fehler":
            for it in items:
                t = it.get("teile")
                if not (isinstance(t, list) and len(t) >= 3 and isinstance(it.get("falsch"), int) and 0 <= it["falsch"] < len(t) and it.get("korrektur")):
                    raise ValueError(f"{k}: fehler-Item kaputt")
        if typ == "selfcheck":
            for it in items:
                if not (it.get("aufgabe") and isinstance(it.get("loesungen"), list) and it["loesungen"]):
                    raise ValueError(f"{k}: selfcheck-Item kaputt")
        if typ in ("mc", "input", "fehler", "listen", "selfcheck") and not items:
            raise ValueError(f"{k}: keine Items")
        if typ == "listen" and len(a.get("text", "")) < 120:
            raise ValueError("listen: Text zu kurz")
        if typ == "read" and not (isinstance(a.get("saetze"), list) and len(a["saetze"]) >= 1):
            raise ValueError("read: saetze fehlen")
        if typ == "speak" and not a.get("frage"):
            raise ValueError("speak: frage fehlt")
        ergebnis.append(a)
    j["aufgaben"] = ergebnis
    j["datum"] = datum
    j["ziel_min"] = max(10, min(15, round(sum(a["min"] for a in ergebnis))))
    j.setdefault("lemmas", [])
    j.setdefault("gruss", "")
    return j


def bilder(j, datum):
    """Bild-Aufgaben: Cloudflare-Bild erzeugen; schlaegt es fehl, wird die Aufgabe ersatzlos gestrichen."""
    import mission_control_api as m
    neu = []
    for a in j["aufgaben"]:
        if a["slot"] != "bild":
            neu.append(a)
            continue
        it = a["items"][0]
        prompt = it.get("bild_prompt")
        if not prompt:
            print("bild ohne bild_prompt -> gestrichen")
            continue
        b64, mime = m.cf_workers_ai_generate(prompt + ", natural light, photo", 1024, 768, cf_model="flux-1-schnell")
        if not b64:
            print("Bild fehlgeschlagen:", mime, "-> Aufgabe gestrichen")
            continue
        ext = "png" if "png" in (mime or "") else "jpg"
        fn = f"{datum}_{a['id']}.{ext}"
        os.makedirs(api.IMG, exist_ok=True)
        with open(os.path.join(api.IMG, fn), "wb") as f:
            f.write(base64.b64decode(b64))
        a["bild"] = fn
        neu.append(a)
    j["aufgaben"] = neu
    for i, a in enumerate(neu, 1):         # ids stabil halten (nach Streichung neu nummerieren)
        a["id"] = f"a{i}"
        if a.get("bild"):
            old = os.path.join(api.IMG, a["bild"])
            newfn = f"{datum}_{a['id']}." + a["bild"].rsplit(".", 1)[1]
            if old != os.path.join(api.IMG, newfn) and os.path.exists(old):
                os.replace(old, os.path.join(api.IMG, newfn))
                a["bild"] = newfn
    j["ziel_min"] = max(10, min(15, round(sum(a["min"] for a in neu))))
    return j


def erzeuge(datum, force=False):
    ziel = os.path.join(api.DIR, datum + ".json")
    if os.path.exists(ziel) and not force:
        return "vorhanden"
    slots, minuten = waehle_slots(datum)
    rng = random.Random("thema" + datum)
    thema = rng.choice(THEMEN)
    prompt = baue_prompt(datum, slots, thema)
    letzter = ""
    for versuch in (1, 2):
        r = limit_gate.run([CLAUDE, "-p", "--model", "sonnet", prompt], capture_output=True, text=True,
                           timeout=600, wait=False, cwd=WS)
        if r.returncode == 75:
            return "limit"
        try:
            j = pruefe_und_normalisiere(parse_json(r.stdout), slots, datum)
            j = bilder(j, datum)
            j["thema"] = j.get("thema") or thema
            j["erzeugt"] = dt.datetime.now().strftime("%Y-%m-%d %H:%M")
            tmp = ziel + ".tmp"
            with open(tmp, "w", encoding="utf-8") as f:
                json.dump(j, f, ensure_ascii=False, indent=1)
            os.replace(tmp, ziel)
            return f"ok ({len(j['aufgaben'])} Aufgaben, ~{j['ziel_min']} min, Thema: {j['thema']})"
        except Exception as e:
            letzter = f"Versuch {versuch}: {e}"
            print(letzter, (r.stderr or "")[:200])
    return "fehler: " + letzter


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--heute", action="store_true")
    ap.add_argument("--datum")
    ap.add_argument("--tage", type=int, default=3)
    ap.add_argument("--force", action="store_true")
    a = ap.parse_args()
    heute = dt.date.today()
    if a.datum:
        daten = [a.datum]
    elif a.heute:
        daten = [heute.isoformat()]
    else:
        daten = [(heute + dt.timedelta(days=i)).isoformat() for i in range(a.tage)]
    report(JOB, TITEL, "laeuft")
    res = {}
    for d in daten:
        res[d] = erzeuge(d, a.force)
        print(d, res[d], flush=True)
    fehl = {d: r for d, r in res.items() if r.startswith("fehler")}
    # Beleg: Dateien wirklich da und parsebar?
    ok_dateien = []
    for d in daten:
        p = os.path.join(api.DIR, d + ".json")
        try:
            json.load(open(p, encoding="utf-8"))
            ok_dateien.append(d)
        except Exception:
            pass
    detail = "; ".join(f"{d[5:]}: {r.split(' (')[0]}" for d, r in res.items())
    if fehl:
        report(JOB, TITEL, "fehler", detail[:300])
    elif any(r == "limit" for r in res.values()) and not ok_dateien:
        report(JOB, TITEL, "ok", "Limit knapp, später erneut (" + detail + ")")
    else:
        report(JOB, TITEL, "ok", detail + f" | Dateien da: {len(ok_dateien)}/{len(daten)}")


if __name__ == "__main__":
    main()
