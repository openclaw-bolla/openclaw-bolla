#!/usr/bin/env python3
"""Samstags-Ausreizung (Chris, 03.10.2026): Wochenkontingent bis 0:00 sinnvoll verbrauchen.

AURORA II:  Phase 1  Kap. 1-18 prüfen (Fehler / Humor / Spannung / Konsistenz)
            Phase 2  Korrekturen als exakte Textersetzungen (mit Protokoll)
            Phase 3  Bogenplan (privat) + Kap. 19-27 schreiben
            Phase 4  Restkontingent: Zweitleser, Band-I-Gegencheck, Lesebegleiter, Fehlerjagd
Alles Opus, EIN Prozess zur Zeit, Limit-Gating vor jedem Lauf. Notbremse: touch /tmp/aurora_samstag_stop
Resume-fähig über state.json. Nur dieser Prozess schreibt Kapitel in aurora2.json.
"""
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

W = "/home/bolla/workspace"
HOME = os.path.expanduser("~")
DATA = f"{W}/data/aurora2.json"
TAG = os.environ.get("SAMSTAG_TAG") or dt.date.today().strftime("%Y%m%d")
OUT = f"{W}/scratch/aurora_samstag_{TAG}"
LOG = f"{W}/logs/aurora_samstag.log"
STATE = f"{OUT}/state.json"
STOP = "/tmp/aurora_samstag_stop"
MODEL = "opus"
CL = shutil.which("claude") or f"{HOME}/.local/bin/claude"
DEADLINE = dt.datetime.combine(dt.date.today(), dt.time(23, 50))
NEU_VON, NEU_BIS = 19, 27
os.makedirs(OUT, exist_ok=True)


class Stop(Exception):
    pass


# ---------------------------------------------------------------- Infrastruktur
def log(msg):
    line = f"[{dt.datetime.now().strftime('%H:%M:%S')}] {msg}"
    print(line, flush=True)
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(line + "\n")


def state_load():
    try:
        return json.load(open(STATE, encoding="utf-8"))
    except Exception:
        return {"done": [], "stats": {}}


ST = state_load()


def is_done(key):
    return key in ST["done"]


def mark(key):
    if key not in ST["done"]:
        ST["done"].append(key)
    json.dump(ST, open(STATE, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    write_status()


def stat_add(k, n=1):
    ST["stats"][k] = ST["stats"].get(k, 0) + n


def quota():
    try:
        with urllib.request.urlopen("http://127.0.0.1:18790/api/claudequota", timeout=15) as r:
            return json.load(r)
    except Exception:
        return None


def write_status(extra=""):
    q = quota() or {}
    done = ST["done"]
    lines = [f"# Samstags-Ausreizung {TAG} — Status {dt.datetime.now().strftime('%H:%M:%S')}", "",
             f"Limits: 5h {q.get('five_hour_pct')} % (Reset {q.get('five_hour_reset_label')}) · Woche {q.get('seven_day_pct')} % (Reset {q.get('reset_label')})",
             f"Schritte erledigt: {len(done)}", "", "```", ", ".join(done[-40:]), "```", "",
             "Statistik: " + json.dumps(ST["stats"], ensure_ascii=False), extra,
             "", "Notbremse: `touch /tmp/aurora_samstag_stop`  ·  Log: workspace/logs/aurora_samstag.log"]
    open(f"{OUT}/STATUS.md", "w", encoding="utf-8").write("\n".join(lines))


def sleep_chunks(sec):
    end = time.time() + sec
    while time.time() < end:
        if os.path.exists(STOP):
            raise Stop("Stopdatei")
        time.sleep(min(30, max(1, end - time.time())))


def gate():
    fails = 0
    while True:
        if os.path.exists(STOP):
            raise Stop("Stopdatei")
        now = dt.datetime.now()
        if now >= DEADLINE:
            raise Stop("Deadline 23:50")
        q = quota()
        if not q:
            fails += 1
            if fails >= 5:
                return None
            time.sleep(60)
            continue
        wk, fh = q.get("seven_day_pct") or 0, q.get("five_hour_pct") or 0
        if wk >= 98.5:
            raise Stop(f"Wochenkontingent ausgereizt ({wk} %)")
        lim = 92   # Chris: 5h-Fenster bis ~92 % ausreizen, nie weiter — er soll immer Luft haben
        if fh >= lim:
            wait = (q.get("five_hour_reset_hours") or 0) * 3600 + (q.get("five_hour_reset_minutes") or 5) * 60 + 90
            if now + dt.timedelta(seconds=wait) > DEADLINE:
                raise Stop(f"5h-Fenster {fh} % und Reset nach Deadline")
            log(f"Gate: 5h {fh} % >= {lim} % — pausiere {wait // 60} Min bis Reset")
            sleep_chunks(wait)
            continue
        return q


def claude(prompt, tag, timeout=1800, model=MODEL):
    for attempt in range(4):
        gate()
        t0 = time.time()
        try:
            r = subprocess.run([CL, "-p", "--output-format", "json", "--model", model], input=prompt,
                               capture_output=True, text=True, timeout=timeout, cwd=HOME)
        except subprocess.TimeoutExpired:
            log(f"Timeout {tag} (Versuch {attempt + 1})")
            continue
        try:
            j = json.loads(r.stdout)
        except Exception:
            j = None
        text = (j or {}).get("result", "") or ""
        if r.returncode != 0 or (j or {}).get("is_error") or not text.strip():
            msg = (text or r.stderr or r.stdout)[:300].replace("\n", " ")
            log(f"Fehler {tag}: {msg}")
            if re.search(r"limit|usage|quota|rate|overload|reset", msg, re.I):
                sleep_chunks(300)
            else:
                sleep_chunks(60 * (attempt + 1))
            continue
        stat_add("claude_calls")
        log(f"ok {tag}: {int(time.time() - t0)} s, {len(text)} Zeichen")
        return text
    log(f"AUFGEGEBEN {tag}")
    return None


def jparse(text):
    if not text:
        return None
    m = re.search(r"\{.*\}", text, re.S)
    if not m:
        return None
    try:
        return json.loads(m.group(0))
    except Exception:
        return None


def claude_json(prompt, tag, **kw):
    t = claude(prompt, tag, **kw)
    j = jparse(t)
    if j is None and t is not None:
        log(f"JSON-Parse fehlgeschlagen {tag} — Wiederholung mit Nur-JSON-Hinweis")
        t = claude(prompt + "\n\nWICHTIG: Antworte AUSSCHLIESSLICH mit einem gültigen JSON-Objekt, ohne Text davor/danach, ohne Codeblock.", tag + "-retry", **kw)
        j = jparse(t)
    return j


# ---------------------------------------------------------------- Daten
def load():
    with open(DATA, encoding="utf-8") as f:
        return json.load(f)


def save(d):
    tmp = DATA + ".tmp_samstag"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)
    os.replace(tmp, DATA)


def wc(t):
    return len(t.split())


def bible_load():
    try:
        return json.load(open(f"{OUT}/bible.json", encoding="utf-8"))
    except Exception:
        return {}


def bible_set(n, fakten):
    b = bible_load()
    b[str(n)] = fakten
    json.dump(b, open(f"{OUT}/bible.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)


def kapnum(titel):
    m = re.match(r"Kapitel\s+(\d+)", titel or "")
    return int(m.group(1)) if m else None


def kap_by_nr(d, n):
    for k in d["kapitel"]:
        if kapnum(k["titel"]) == n:
            return k
    return None


def summaries(d, bis=None):
    out = []
    for k in d["kapitel"]:
        n = kapnum(k["titel"])
        if bis and n and n > bis:
            continue
        head = k["text"].strip().split("\n")[0][:160]
        out.append(f"- {k['titel']} | {head} | {k.get('zusammenfassung', '')}")
    return "\n".join(out)


def figuren_ctx(d):
    return json.dumps({"protagonisten": d.get("protagonisten"), "antagonisten": d.get("antagonisten"),
                       "nebenfiguren": d.get("nebenfiguren")}, ensure_ascii=False)


def rote_linien(d):
    return "\n".join("- " + x for x in d.get("steuerung", {}).get("rote_linien", []))


def bible_txt(bis=None):
    b = bible_load()
    out = []
    for n in sorted(b, key=int):
        if bis and int(n) > bis:
            continue
        out.append(f"Kap. {n}: " + " | ".join(b[n]))
    return "\n".join(out) or "(noch keine)"


def read_trunc(path, n):
    try:
        return open(path, encoding="utf-8").read()[:n]
    except Exception:
        return ""


def stil_hygiene():
    return (read_trunc(f"{W}/scratch/aurora2_analoge_fehler_bericht.md", 5000) + "\n---\n" +
            read_trunc(f"{W}/scratch/aurora2_humor_audit.md", 4000))


CHANGES = f"{OUT}/changes.md"


def apply_patches(n, patches, kind, allow):
    """Wendet exakte Ersetzungen auf Kapitel n an. allow(p) -> bool (Policy). Gibt (angewandt, abgelehnt) zurück."""
    if not patches:
        return 0, 0
    d = load()
    k = kap_by_nr(d, n)
    if not k:
        return 0, len(patches)
    text, ok, bad = k["text"], 0, 0
    for p in patches:
        z, e = (p.get("zitat") or ""), (p.get("ersatz") or "")
        if not z or not e or z == e:
            bad += 1
            continue
        if not allow(p):
            bad += 1
            with open(f"{OUT}/vorschlaege_fuer_chris.md", "a", encoding="utf-8") as f:
                f.write(f"\n### Kap. {n} · {kind} · {p.get('art', '')} · {p.get('schwere', '')}  (NICHT angewandt — Kapitel von Chris gegengelesen)\n"
                        f"Grund: {p.get('problem', '')}\n\nSTELLE: {z}\n\nVORSCHLAG: {e}\n")
            stat_add("vorschlaege_fuer_chris")
            continue
        if text.count(z) != 1 or abs(len(e) - len(z)) > 1200:
            bad += 1
            log(f"  Patch abgelehnt Kap {n} ({kind}): Treffer={text.count(z)}")
            continue
        text = text.replace(z, e, 1)
        ok += 1
        with open(CHANGES, "a", encoding="utf-8") as f:
            f.write(f"\n### Kap. {n} · {kind} · {p.get('art', '')} · {p.get('schwere', '')}\n"
                    f"Grund: {p.get('problem', '')}\n\nVORHER: {z}\n\nNACHHER: {e}\n")
    if ok:
        k["text"] = text
        d["statistik"]["woerter_gesamt"] = sum(wc(x["text"]) for x in d["kapitel"])
        save(d)
    stat_add("patches_ok", ok)
    stat_add("patches_abgelehnt", bad)
    return ok, bad


HARD_ARTS = ("grammatik", "tippfehler", "logik", "zahl", "name", "zeit")


def make_allow(n, kind, mode):
    def allow(p):
        if n <= 8 and mode != "neu":          # Kap. 1-8 hat Chris Satz für Satz gegengelesen: NUR Grammatik/Tippfehler, alles Inhaltliche geht als Vorschlag an Chris
            return kind == "fehler" and p.get("schwere") in ("hoch", "mittel") and p.get("art") in ("grammatik", "tippfehler")
        return True
    return allow


# ---------------------------------------------------------------- Prüfung eines Kapitels
SCHEMA = """{
 "fehler":[{"zitat":"...","ersatz":"...","art":"grammatik|tippfehler|logik|zahl|name|zeit|wiederholung|stil","schwere":"hoch|mittel|niedrig","problem":"..."}],
 "konsistenz":[{"zitat":"...","ersatz":"...","art":"zahl|name|zeit|logik","schwere":"hoch|mittel|niedrig","problem":"... (gegen welches Kapitel)"}],
 "humor":{"momente":0,"pro_1000_woerter":0.0,"wuesten":["Beschreibung der Strecke"],"patches":[{"zitat":"...","ersatz":"...","art":"humor","schwere":"mittel","problem":"..."}]},
 "spannung":{"bewertung_1_10":0,"cliffhanger_1_10":0,"schwaechen":["..."],"patches":[{"zitat":"...","ersatz":"...","art":"spannung","schwere":"mittel","problem":"..."}]},
 "fakten":["knappe konkrete Fakten dieses Kapitels: Zahlen, Uhrzeiten, Daten, Tageszähler, Namen, Orte, wer weiß was, Gegenstände, offene Fäden"],
 "gesamt":"3-5 Sätze Urteil"
}"""


def review_chapter(n, mode="normal", focus=None):
    key = f"1a:{n}" if mode == "normal" else f"rev:{mode}:{focus or ''}:{n}"
    if is_done(key):
        return
    d = load()
    k = kap_by_nr(d, n)
    if not k:
        return
    prev = kap_by_nr(d, n - 1)
    nxt = kap_by_nr(d, n + 1)
    prev_end = prev["text"][-1800:] if prev else "(kein Vorkapitel)"
    nxt_start = nxt["text"][:900] if nxt else "(kein Folgekapitel)"
    krit_h = d["kriterien"].get("humor", "")
    fokus = f"\nSONDERFOKUS DIESES DURCHGANGS: {focus}. Suche besonders gründlich danach, die übrigen Kategorien nur bei offensichtlichen Funden.\n" if focus else ""
    persona = ("Du bist ein unabhängiger Zweitleser mit frischem Blick (Thriller-Lektor)." if mode == "zweit"
               else "Du bist das Lektoratsteam (Korrektorat, Humor-Lektorat, Spannungs-Lektorat, Kontinuität).")
    n_h = 12 if n >= 9 or mode == "neu" else 8
    prompt = f"""{persona} Buch: AURORA II (deutscher KI-Thriller, Fortsetzung, Ken-Follett-Stil, warmherziger Humor, KEIN Slapstick, jugendfrei).
Du prüfst Kapitel {n} des Buches. Ziel: ein fehlerfreies, konsistentes, spannendes, humorvolles Fundament.
{fokus}
FIGUREN: {figuren_ctx(d)}

ROTE LINIEN:
{rote_linien(d)}

HUMOR-MASSSTAB (Kapitel 10 = Referenz, Chris-bestätigt):
{krit_h}

ZAHLEN-KANON: AURORA ist als Entwicklungsalter-Stempel bewusst auf „4 Jahre, 7 Monate" eingefroren (Todesalter der realen Tochter in Band I). Zahlen/Tageszähler müssen exakt stimmen und über Kapitel hinweg zusammenpassen.

ZUSAMMENFASSUNGEN ALLER KAPITEL:
{summaries(d)}

BEKANNTE FAKTEN-BIBEL:
{bible_txt()}

STIL-HYGIENE (bekannte Fehlermuster dieses Buches):
{stil_hygiene()}

ENDE VORKAPITEL: ...{prev_end}
ANFANG FOLGEKAPITEL: {nxt_start}...

=== ZU PRÜFENDES KAPITEL: {k['titel']} ({wc(k['text'])} Wörter) ===
{k['text']}
=== ENDE KAPITEL ===

AUFGABE: Antworte AUSSCHLIESSLICH mit einem JSON-Objekt exakt nach diesem Schema (kein Text drumherum):
{SCHEMA}

REGELN FÜR ALLE PATCHES (zitat/ersatz):
- "zitat" muss WÖRTLICH und EINDEUTIG im Kapitel stehen (genau einmal vorkommen), 8-30 Wörter, Zeichen exakt kopiert (»«, —, *, Kursiv-Sternchen, Zeilenumbrüche vermeiden). "ersatz" ersetzt das komplette Zitat.
- Nichts erfinden, was dem Kapitel/Kanon widerspricht. Chris' Stimme erhalten; so wenig ändern wie nötig. Keine neuen Figuren/Plotpunkte.
- Höchstens {n_h} Einträge bei fehler+konsistenz zusammen, höchstens 6 humor-patches, höchstens 4 spannung-patches. Nur echte Funde — lieber weniger, dafür sicher. Geschmackssachen weglassen.
- Humor-Patches nur dort, wo wirklich eine Humor-Wüste (>900 Wörter) oder Dichte <5/1000 vorliegt; im Ton von Kapitel 10 (trocken, aus Figur/Situation, sofort verständlich). Die letzten 400-600 Wörter vor dem Cliffhanger bleiben humorfrei.
- Spannungs-Patches nur wenn eine Szene wirklich schwächelt (Erklär-Dump, fehlender Einsatz, Vorhersehbarkeit); sparsam, nie den Cliffhanger-Schluss abschwächen.
- "fakten": 15-30 knappe, konkrete Fakten (für die Fakten-Bibel)."""
    j = claude_json(prompt, f"Review Kap {n} [{mode}{'/' + focus if focus else ''}]")
    if j is None:
        log(f"Review Kap {n} ohne Ergebnis")
        return
    json.dump(j, open(f"{OUT}/review_{mode}_{n}.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    if j.get("fakten") and mode in ("normal", "neu"):
        bible_set(n, j["fakten"])
    tot_ok = tot_bad = 0
    groups = [("fehler", j.get("fehler") or [], "fehler"), ("konsistenz", j.get("konsistenz") or [], "konsistenz")]
    if n >= 9 or mode == "neu":
        groups += [("humor", (j.get("humor") or {}).get("patches") or [], "humor"),
                   ("spannung", (j.get("spannung") or {}).get("patches") or [], "spannung")]
    for name, ps, kind in groups:
        ok, bad = apply_patches(n, ps, f"{mode}:{name}", make_allow(n, kind, mode))
        tot_ok += ok
        tot_bad += bad
    hum = (j.get("humor") or {}).get("pro_1000_woerter")
    sp = (j.get("spannung") or {}).get("bewertung_1_10")
    cl = (j.get("spannung") or {}).get("cliffhanger_1_10")
    with open(f"{OUT}/uebersicht.md", "a", encoding="utf-8") as f:
        f.write(f"- Kap {n} [{mode}{'/' + focus if focus else ''}]: Humor {hum}/1000 · Spannung {sp}/10 · Cliffhanger {cl}/10 · Patches ok {tot_ok} / abgelehnt {tot_bad} — {j.get('gesamt', '')}\n")
    log(f"Kap {n}: Patches angewandt {tot_ok}, abgelehnt {tot_bad} (Humor {hum}/1000, Spannung {sp}, Cliffhanger {cl})")
    mark(key)


# ---------------------------------------------------------------- Phase 1b: Gesamt-Konsistenz
BAND1_ANKER = """- Todesalter der realen Tochter (Band I, Kap. 46, kanonisch): 4 Jahre, 7 Monate. (Kap. 35 in Band I nennt „sechs Jahre vier Monate" — bekannter Versprecher, wird NICHT korrigiert.)
- Theo Dreyer stirbt zu Beginn von Band II (Kap. 1). Hauptfiguren: Marlie Braun (Heldin, reflexhaftes „ja"), Noah, Leni, Jonas Brenner (neu), AURORA; Basti & Frauke Harms.
- Antagonisten: Dr. Ingrid Falkner (EU-Aufsicht, Angst statt Bosheit), Julian Ashworth (Broker, der anonyme Käufer aus Band I). Elias Roth (Verräter aus Band I), Milan Kreft (der „Räumer")."""


def phase_1b():
    if not is_done("1b"):
        d = load()
        headers = "\n".join(f"{k['titel']} || {' / '.join(k['text'].strip().split(chr(10))[:1])}" for k in d["kapitel"])
        prompt = f"""Du bist Kontinuitäts-Lektor für AURORA II. Unten stehen Kapitelköpfe (mit Datum und Tageszähler), Zusammenfassungen und die Fakten-Bibel ALLER Kapitel 1-18, dazu Band-I-Anker.
Finde echte WIDERSPRÜCHE (Zahlen, Uhrzeiten, Daten, Tageszähler „unverändert seit N Tagen", Wochentage/Datum-Zuordnung, Namen, Orte, wer-weiß-was-wann, Gegenstände, Figuren-Eigenschaften, Ablauf-Logik) und Running-Gag-Überstrapazierung.
Nur echte, belegbare Widersprüche — keine Spekulation, keine Geschmacksfragen.

BAND-I-ANKER:
{BAND1_ANKER}

KAPITELKÖPFE:
{headers}

ZUSAMMENFASSUNGEN:
{summaries(d)}

FAKTEN-BIBEL:
{bible_txt()}

Antworte NUR mit JSON:
{{"widersprueche":[{{"beschreibung":"...","kanon":"was ist richtig/welche Fassung gilt (mit Begründung)","falsch_in":[Kapitelnummern, die geändert werden müssen],"belege":"Kapitel + Faktum"}}],
 "gag_hygiene":[{{"gag":"...","kapitel":[...],"empfehlung":"..."}}],
 "luecken":["offene Fäden/Logiklöcher, die später aufgelöst werden müssen"]}}"""
        j = claude_json(prompt, "Gesamt-Konsistenz 1b")
        if j is not None:
            json.dump(j, open(f"{OUT}/konsistenz_gesamt.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
            mark("1b")
    try:
        j = json.load(open(f"{OUT}/konsistenz_gesamt.json", encoding="utf-8"))
    except Exception:
        return
    todo = {}
    for w in j.get("widersprueche", []):
        for n in w.get("falsch_in", []):
            if isinstance(n, int):
                todo.setdefault(n, []).append(w)
    for n, ws in sorted(todo.items()):
        key = f"1b-fix:{n}"
        if is_done(key):
            continue
        d = load()
        k = kap_by_nr(d, n)
        if not k:
            continue
        prompt = f"""Behebe in AURORA-II-Kapitel {n} die folgenden belegten Kontinuitätswidersprüche mit möglichst kleinen Eingriffen.
WIDERSPRÜCHE (inkl. kanonischer Fassung):
{json.dumps(ws, ensure_ascii=False, indent=1)}

=== {k['titel']} ===
{k['text']}
=== ENDE ===

Antworte NUR mit JSON: {{"patches":[{{"zitat":"...","ersatz":"...","art":"zahl|name|zeit|logik","schwere":"hoch","problem":"..."}}]}}
"zitat" muss WÖRTLICH und EINDEUTIG im Kapitel stehen (genau einmal, 8-30 Wörter, Zeichen exakt), "ersatz" ersetzt es. Wenn das Kapitel in Wahrheit gar nicht betroffen ist: leere Liste."""
        r = claude_json(prompt, f"Konsistenz-Fix Kap {n}")
        if r is not None:
            apply_patches(n, r.get("patches") or [], "1b", make_allow(n, "konsistenz", "normal"))
            mark(key)


# ---------------------------------------------------------------- Phase 3
def bogenplan():
    if is_done("3a"):
        return
    d = load()
    letzte = d["kapitel"][-1]
    prompt = f"""Du bist Bolla, Co-Autor von AURORA II (deutscher KI-Thriller, Ken-Follett-Stil). Entwirf den privaten BOGENPLAN für die Kapitel {NEU_VON}-{NEU_BIS}.

BUCHKRITERIEN: {json.dumps(d['kriterien'], ensure_ascii=False)}
FIGUREN: {figuren_ctx(d)}
STEUERUNG: {json.dumps(d.get('steuerung'), ensure_ascii=False)}
GEHEIME MASTER-WENDUNG (nur für dich, nie an Chris): {d['geheim'].get('wendung', '')}
BEREITS GESÄTE HINWEISE (privat): {json.dumps(d['geheim'].get('hinweise_gesaet'), ensure_ascii=False)}
ZEITREGIME-ABGLEICH (privat): {json.dumps(d['geheim'].get('zeitregime_abgleich'), ensure_ascii=False)}
FÄHIGKEITEN-ABGLEICH (privat): {json.dumps(d['geheim'].get('faehigkeiten_stufen_abgleich'), ensure_ascii=False)}
GEPLANTER NÄCHSTER SCHRITT (Stand Kap. 18): {d.get('naechsterSchritt')}

ZUSAMMENFASSUNGEN KAP. 1-18:
{summaries(d)}
FAKTEN-BIBEL:
{bible_txt()}
LETZTES KAPITEL VOLLTEXT ({letzte['titel']}):
{letzte['text']}

VORGABEN:
- Höhepunkt gemäß Buchstruktur: der extrem überraschende Höhepunkt (die Master-Wendung) tritt in Kapitel 20-22 ein, nicht vorhersehbar, und gerade die Auflösung/Folge muss noch einmal überraschen (nicht die naheliegendste Erklärung). Kapitel 19 = Nacht/Morgen vor der Entscheidung (Marlies teuerstes Ja kommt in Kap. 20).
- Kapitel 23-{NEU_BIS}: Nachspiel, Konsequenzen, Gegenzüge von Falkner/Ashworth, nächste Entwicklungsstufe AURORAs (Plateaus-und-Sprünge-Zeitregime), Marlies „Nein"-Bogen weiterführen. Das Buch ist mit Kap. {NEU_BIS} NICHT zu Ende (Gesamtumfang 35-55 Kapitel): Kap. {NEU_BIS} endet mit einem starken offenen Cliffhanger.
- JEDES Kapitel endet mit Cliffhanger/Sog-Satz. Humor-Standard Kap. 10 (6-9 Momente/1000 Wörter), warmherzig, kein Slapstick, jugendfrei.
- Erzählkamera dicht bei Marlie; sparsame POV-Ausflüge (Leni Humor, Falkner Bedrohung, AURORA Zwischenspiele).
- Kopfzeile jedes Kapitels im bisherigen Format: *Datum, Uhrzeit — AURORA: geschätzt 4 Jahre, 7 Monate (…)* — wie in Kap. 17/18 (Tageszähler fortführen oder bewusst brechen, wenn die Handlung es trägt; dann Entwicklungsalter-Sprung als Stilmittel). Kapitel dürfen Zeitsprünge enthalten.
- Neue Fähigkeiten-Stufen/Plot-Weichen nur, wenn sie aus der Master-Wendung folgen. Keine Widersprüche zu den Fakten.

Antworte NUR mit JSON:
{{"gesamtbogen":"...","kapitel":[{{"nr":{NEU_VON},"titel":"Kapitel {NEU_VON}: ...","kopfzeile":"*...*","pov":"...","beats":["..."],"cliffhanger":"...","humor_schwerpunkte":["..."],"saat_oder_aufloesung":"...","weiche":"ja/nein + was (Plot-Weichen, die Chris vor Freigabe sehen sollte)"}}]}}"""
    j = claude_json(prompt, "Bogenplan 3a")
    if not j or len(j.get("kapitel", [])) < (NEU_BIS - NEU_VON + 1):
        log("Bogenplan unvollständig — Abbruch Phase 3")
        raise Stop("Bogenplan fehlgeschlagen")
    json.dump(j, open(f"{OUT}/bogenplan_PRIVAT.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    os.chmod(f"{OUT}/bogenplan_PRIVAT.json", 0o600)
    d = load()
    d["geheim"]["bogenplan_19_27"] = j
    save(d)
    mark("3a")


def parse_marked(raw, tags):
    out = {}
    for i, t in enumerate(tags):
        nxt = tags[i + 1] if i + 1 < len(tags) else None
        pat = re.escape(t) + r"(.*?)" + (re.escape(nxt) if nxt else r"$")
        m = re.search(pat, raw, re.S)
        out[t] = m.group(1).strip() if m else ""
    return out


TAGS = ["###TITEL###", "###INHALT###", "###ZUSAMMENFASSUNG###", "###FAKTEN###", "###GLOSSAR###", "###ENDE###"]


def write_chapter(n):
    key = f"3b:{n}"
    if is_done(key):
        return
    d = load()
    if kap_by_nr(d, n):
        mark(key)
        return
    plan = json.load(open(f"{OUT}/bogenplan_PRIVAT.json", encoding="utf-8"))
    pk = next(x for x in plan["kapitel"] if x.get("nr") == n)
    voll_ab = n - 4
    teile = []
    for k in d["kapitel"]:
        kn = kapnum(k["titel"])
        if kn and kn >= voll_ab:
            teile.append(f"=== {k['titel']} (VOLLTEXT) ===\n{k['text']}")
    k10 = kap_by_nr(d, 10)
    steuer = json.dumps(d.get("steuerung"), ensure_ascii=False)
    prompt = f"""Du bist Bolla und schreibst gemeinsam mit Chris Mandel die Fortsetzung des deutschen KI-Thrillers AURORA. Schreibe jetzt KAPITEL {n} von AURORA II.

BUCHKRITERIEN (unbedingt beachten): {json.dumps(d['kriterien'], ensure_ascii=False)}
FIGUREN (Ken-Follett-Prinzip: aussehen, detail, macke, wunde, stimme in Handlung und Dialog zeigen): {figuren_ctx(d)}
STEUERUNG & ROTE LINIEN: {steuer}
GEHEIME MASTER-WENDUNG (nur für dich, Chris darf sie nicht erfahren; nichts davon im Text vorwegnehmen, ausser wie im Plan vorgesehen): {d['geheim'].get('wendung', '')}
BEREITS GESÄTE HINWEISE: {json.dumps(d['geheim'].get('hinweise_gesaet'), ensure_ascii=False)}

PRIVATER BOGENPLAN FÜR DIESES KAPITEL (verbindlich, Feinheiten darfst du dramaturgisch verbessern):
{json.dumps(pk, ensure_ascii=False, indent=1)}
GESAMTBOGEN 19-27: {plan.get('gesamtbogen', '')}

ZUSAMMENFASSUNGEN ALLER BISHERIGEN KAPITEL:
{summaries(d)}

FAKTEN-BIBEL (Zahlen/Uhrzeiten/Namen — NICHT widersprechen):
{bible_txt()}

STIL-HYGIENE (bekannte Fehlermuster, vermeiden):
{stil_hygiene()}

HUMOR-TONPROBE (Kapitel 10, Anfang):
{k10['text'][:4200] if k10 else ''}

{chr(10).join(teile)}

AUFGABE:
- Kapitel {n}, Länge 5.500-7.500 Wörter, Titel exakt „Kapitel {n}: <Titel>".
- Erste Textzeile ist die Kopfzeile im Format der letzten Kapitel (kursiv in Sternchen: *Datum, Uhrzeit — AURORA: geschätzt 4 Jahre, 7 Monate (…)*). Tageszähler/Zahlen exakt gegen die Fakten-Bibel und die Vorkapitel rechnen und fortführen.
- Humor-Standard Kapitel 10 (6-9 Momente je 1000 Wörter, warmherzig, trocken, aus Figur/Situation, sofort verständlich, KEIN Slapstick, jugendfrei). Keine Humor-Wüste über 900 Wörter; letzte 400-600 Wörter vor dem Cliffhanger humorfrei.
- Spannungstiefe wie Ken Follett: echte Einsätze, Gegenspieler mit Plan, Zeitdruck, überraschende Wendungen innerhalb der Szenen. Das Kapitel endet mit einem Cliffhanger/Sog-Satz.
- Zahlen/Zeiten exakt konsistent. Keine Plot-Weichen außerhalb des Plans. Anschluss nahtlos an das Ende des Vorkapitels.

Antworte AUSSCHLIESSLICH in diesem Format (keine Erklärungen, kein Markdown drumherum):
###TITEL###
Kapitel {n}: ...
###INHALT###
(vollständiger Kapiteltext inkl. Kopfzeile, Absätze durch Leerzeilen)
###ZUSAMMENFASSUNG###
(2-3 Sätze, Spoiler erlaubt, wie die bisherigen Zusammenfassungen)
###FAKTEN###
(15-30 knappe Fakten, ein Fakt pro Zeile, mit "- ")
###GLOSSAR###
(max. 6 neue merkenswerte Personen/Objekte/Orte/Begriffe, je Zeile NAME|KATEGORIE|BESCHREIBUNG, oder KEINE)
###ENDE###"""
    for versuch in range(2):
        raw = claude(prompt, f"Kapitel {n} schreiben (Versuch {versuch + 1})", timeout=2400)
        if not raw:
            continue
        p = parse_marked(raw, TAGS)
        titel, text = p["###TITEL###"].strip().split("\n")[0].strip(), p["###INHALT###"].strip()
        problems = []
        if not re.match(rf"^Kapitel {n}: .+", titel):
            problems.append("Titelformat")
        if wc(text) < 4300:
            problems.append(f"zu kurz ({wc(text)} Wörter)")
        if not text.lstrip().startswith("*"):
            problems.append("Kopfzeile fehlt")
        if problems:
            log(f"Kap {n} Validierung: {problems}")
            prompt += f"\n\nKORREKTUR: Der letzte Versuch hatte Mängel: {', '.join(problems)}. Halte Format und Länge (5.500-7.500 Wörter) exakt ein."
            continue
        d = load()
        if kap_by_nr(d, n):
            mark(key)
            return
        now = dt.datetime.now().strftime("%Y-%m-%d %H:%M")
        d["kapitel"].append({"titel": titel, "text": text, "datum": now, "zusammenfassung": p["###ZUSAMMENFASSUNG###"].strip(), "modell": "opus"})
        d["statistik"]["kapitel_gesamt"] = len(d["kapitel"])
        d["statistik"]["woerter_gesamt"] = sum(wc(x["text"]) for x in d["kapitel"])
        d["statistik"]["letzte_session"] = now
        d["letzteAktion"] = now
        d["naechsterSchritt"] = f"Kapitel {n + 1} folgt (Bogenplan liegt privat vor)."
        known = {e.get("name", "").lower() for e in d.get("glossar", [])}
        for line in p["###GLOSSAR###"].splitlines():
            line = line.strip().lstrip("-").strip()
            parts = [x.strip() for x in line.split("|", 2)]
            if len(parts) == 3 and parts[0] and parts[0].lower() not in known and not line.upper().startswith("KEINE"):
                import uuid
                d.setdefault("glossar", []).append({"id": uuid.uuid4().hex[:8], "name": parts[0], "kategorie": parts[1] or "Sonstiges",
                                                    "beschreibung": parts[2], "kapitel_titel": titel, "datum": now})
                known.add(parts[0].lower())
        save(d)
        fakten = [x.strip().lstrip("-").strip() for x in p["###FAKTEN###"].splitlines() if x.strip()]
        if fakten:
            bible_set(n, fakten)
        stat_add("kapitel_geschrieben")
        log(f"Kapitel {n} geschrieben: {titel} ({wc(text)} Wörter)")
        mark(key)
        return
    log(f"Kapitel {n} nicht erzeugt — Phase 3 bricht ab")
    raise Stop(f"Kapitel {n} fehlgeschlagen")


# ---------------------------------------------------------------- Phase 4
def t4_band1():
    if is_done("4:band1"):
        return
    d = load()
    bd = f"{W}/data/aurora_chapters_aktuell"
    files = sorted(f for f in os.listdir(bd) if re.match(r"kap_\d+\.json", f))
    sel = [f for f in files if f in ("kap_35.json", "kap_46.json")] + files[-3:]
    teile = []
    for f in dict.fromkeys(sel):
        try:
            jj = json.load(open(f"{bd}/{f}", encoding="utf-8"))
            teile.append(f"=== BAND I · {jj.get('titel')} ===\n{jj.get('text', '')[:14000]}")
        except Exception:
            pass
    prompt = f"""Prüfe die Anschlussstellen von AURORA II (Band II) an Band I. Unten Auszüge der Schluss-/Schlüsselkapitel von Band I und die Zusammenfassungen/Fakten von Band II.
Finde echte Widersprüche zu Band I (Zahlen, Zeitabstände, Figuren-Status, Ereignisse, Namen, Orte). Zahlen-Kanon: Todesalter der Tochter = 4 Jahre 7 Monate (Kap. 46); Kap. 35 Versprecher bleibt.
{chr(10).join(teile)}

BAND II ZUSAMMENFASSUNGEN:
{summaries(d)}
FAKTEN:
{bible_txt()}

Antworte NUR mit JSON: {{"widersprueche":[{{"beschreibung":"...","kanon":"...","falsch_in":[Band-II-Kapitelnummern],"belege":"..."}}]}}
Nur belegbare Widersprüche; leere Liste ist ein gutes Ergebnis."""
    j = claude_json(prompt, "Band-I-Gegencheck")
    if j is None:
        return
    json.dump(j, open(f"{OUT}/band1_gegencheck.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    todo = {}
    for w in j.get("widersprueche", []):
        for n in w.get("falsch_in", []):
            if isinstance(n, int):
                todo.setdefault(n, []).append(w)
    for n, ws in sorted(todo.items()):
        d = load()
        k = kap_by_nr(d, n)
        if not k:
            continue
        r = claude_json(f"""Behebe in AURORA-II-Kapitel {n} diese belegten Widersprüche zu Band I mit minimalen Eingriffen:
{json.dumps(ws, ensure_ascii=False, indent=1)}
=== {k['titel']} ===
{k['text']}
=== ENDE ===
Antworte NUR mit JSON: {{"patches":[{{"zitat":"...","ersatz":"...","art":"zahl|name|zeit|logik","schwere":"hoch","problem":"..."}}]}} — zitat WÖRTLICH, EINDEUTIG, 8-30 Wörter. Leere Liste, wenn nicht betroffen.""", f"Band-I-Fix Kap {n}")
        if r:
            apply_patches(n, r.get("patches") or [], "band1", make_allow(n, "konsistenz", "normal"))
    mark("4:band1")


def t4_lesebegleiter():
    if is_done("4:lesebegleiter"):
        return
    d = load()
    prompt = f"""Erstelle für Chris (Autor, liest das Buch über Wochen verteilt) einen LESEBEGLEITER zu AURORA II, Kapitel 1-{NEU_BIS}, auf Deutsch, Markdown.
Inhalt: (1) Figurenregister (Name, Rolle, 1-2 Sätze, erstes Auftreten), (2) Zeitleiste Kapitel → Datum/Uhrzeit, AURORA-Entwicklungsalter-Stempel und Tageszähler, (3) Offene Fäden und Fragen (was ist noch ungeklärt), (4) Running Gags und wo sie vorkommen, (5) kurze Kapitelübersicht (2 Sätze je Kapitel).
Nutze NUR die Informationen unten; verrate keine Wendungen, die nicht im Text/den Zusammenfassungen stehen. Kopfzeile: „Achtung: enthält Handlungsdetails bis Kapitel {NEU_BIS} (Spoiler für noch ungelesene Kapitel)“.
FIGUREN: {figuren_ctx(d)}
ZUSAMMENFASSUNGEN UND KÖPFE:
{summaries(d)}
FAKTEN:
{bible_txt()}"""
    t = claude(prompt, "Lesebegleiter")
    if t:
        os.makedirs(f"{W}/docs", exist_ok=True)
        open(f"{W}/docs/AURORA_II_Lesebegleiter_{TAG}.md", "w", encoding="utf-8").write(t)
        mark("4:lesebegleiter")


def t4_memory():
    if is_done("4:memory"):
        return
    mem = open(f"{HOME}/.claude/projects/-home-bolla/memory/MEMORY.md", encoding="utf-8").read()
    prompt = f"""Du prüfst den Index (MEMORY.md) eines persönlichen Assistenten auf Hygiene. NUR BERICHT, nichts wird gelöscht.
Finde: (a) inhaltliche Dubletten/Überschneidungen, (b) offensichtlich veraltete Einträge (Datum in der Vergangenheit, abgeschlossene Fälle), (c) zu lange/unübersichtliche Abschnitte mit Verbesserungsvorschlag zur Gruppierung, (d) Einträge ohne klaren Nutzen. Kurz, als Markdown-Liste mit Priorität (hoch/mittel/niedrig). Heutiges Datum: {TAG}.
{mem}"""
    t = claude(prompt, "Memory-Hygiene", model="sonnet")
    if t:
        open(f"{OUT}/memory_hygiene_bericht.md", "w", encoding="utf-8").write(t)
        mark("4:memory")


FOKI = ["Grammatik, Interpunktion, Tippfehler, Satzbau-Holprigkeit",
        "Wortwiederholungen, Füllsätze, Business-Jargon, abgegriffene Formulierungen",
        "Dialoge: Sprechweise je Figur konsistent, AURORAs Kleinkind-Logik, Glaubwürdigkeit",
        "Logik, Technik- und Ablauf-Plausibilität, Zeit-/Ortsangaben",
        "Humor: Wüsten, Pointen-Verständlichkeit (keine erklärungsbedürftigen Witze), Running-Gag-Dosis"]


def phase4():
    for n in range(NEU_VON, NEU_BIS + 1):
        review_chapter(n, mode="zweit")
    t4_band1()
    t4_lesebegleiter()
    t4_memory()
    r = 1
    while True:
        focus = FOKI[(r - 1) % len(FOKI)]
        d = load()
        for k in d["kapitel"]:
            review_chapter(kapnum(k["titel"]), mode=f"jagd{r}", focus=focus)
        r += 1
        if r > 12:
            break


# ---------------------------------------------------------------- Abschluss
def abschlussbericht(grund):
    q = quota() or {}
    d = load()
    txt = f"""# Samstags-Ausreizung {TAG} — Abschlussbericht
Ende: {dt.datetime.now().strftime('%H:%M')} · Grund: {grund}
Limits jetzt: 5h {q.get('five_hour_pct')} % · Woche {q.get('seven_day_pct')} %
Kapitel im Buch: {len(d['kapitel'])} · Wörter gesamt: {d['statistik'].get('woerter_gesamt')}
Statistik: {json.dumps(ST['stats'], ensure_ascii=False)}
Erledigte Schritte: {len(ST['done'])}

Dateien in {OUT}: changes.md (alle Textänderungen Vorher/Nachher), uebersicht.md (Humor/Spannung je Kapitel), konsistenz_gesamt.json,
band1_gegencheck.json, memory_hygiene_bericht.md, review_*.json. Backup vor Start: workspace/backups/aurora2_backup_vor_samstag_*.json
Lesebegleiter: workspace/docs/AURORA_II_Lesebegleiter_{TAG}.md
"""
    open(f"{OUT}/ABSCHLUSSBERICHT.md", "w", encoding="utf-8").write(txt)
    try:
        p = f"{HOME}/.claude/projects/-home-bolla/memory/aktuell.md"
        s = open(p, encoding="utf-8").read()
        note = (f"## ✅ {dt.date.today().strftime('%d.%m.%Y')} — Samstags-Ausreizung AURORA II beendet ({grund})\n\n"
                f"Kap. 1–18 geprüft/korrigiert, Kap. {NEU_VON}–{NEU_BIS} geschrieben soweit Kontingent reichte (Buch jetzt {len(d['kapitel'])} Kapitel). "
                f"Details: `{OUT}/ABSCHLUSSBERICHT.md`, Änderungsprotokoll `changes.md`. Bogenplan privat in aurora2.json → geheim.bogenplan_19_27 (nie zeigen). "
                f"**Chris: ab Kap. 19 sind Plot-Weichen möglich (siehe `weiche` im Bogenplan) — beim Lesen von Kap. 19+ nachfragen, was gefällt.**\n\n---\n\n")
        open(p, "w", encoding="utf-8").write(note + s)
    except Exception as e:
        log(f"aktuell.md nicht aktualisiert: {e}")
    log("ABSCHLUSSBERICHT geschrieben")


def main():
    lock = open(f"{OUT}/.lock", "w")
    try:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except OSError:
        print("läuft bereits")
        return
    grund = "fertig"
    try:
        q0 = quota() or {}
        log(f"START Samstags-Ausreizung — 5h {q0.get('five_hour_pct')} %, Woche {q0.get('seven_day_pct')} %")
        if os.path.exists(STOP):
            os.remove(STOP)
        # Phase 1a
        d = load()
        for k in d["kapitel"]:
            n = kapnum(k["titel"])
            if n and n <= 18:
                review_chapter(n)
        # Phase 1b + 2-Fixes
        phase_1b()
        # Phase 3
        bogenplan()
        for n in range(NEU_VON, NEU_BIS + 1):
            write_chapter(n)
            review_chapter(n, mode="neu")
        # Phase 4
        phase4()
    except Stop as e:
        grund = f"gestoppt: {e}"
        log(f"STOP: {e}")
    except Exception as e:
        import traceback
        grund = f"Fehler: {e}"
        log("FEHLER: " + traceback.format_exc())
    finally:
        abschlussbericht(grund)


if __name__ == "__main__":
    main()
