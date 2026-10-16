#!/usr/bin/env python3
"""Freitags-Ausreizung AURORA II (Chris-Freigabe 14.10.2026): Start Fr 16.10. 19:00, Deadline Sa 17.10. 23:50.

Rahmen (Chris): er muss nicht mehr vorab lesen; die wichtigen Kriterien gelten schon beim Schreiben.
Plot-OK-Rueckfragen entfallen (Bolla entscheidet selbst, begruendet im Protokoll).

Ablauf:
  A  Entwuerfe Kap. 25-28 (scratch/aurora_samstag_wochenende_20261009/) per Opus ueberarbeiten
     (Pruefnotizen einarbeiten, Zahlen/Daten gegen Kanon+Kap. 1-24, Figuren-Prinzip) -> als Kap. 25-28 in aurora2.json
     (Backup vorher, Protokoll in changes.md), je Kapitel Review + Fehlerklassen-Review.
     Kap. 27: Wahl Original/Variante A/B trifft Bolla selbst (Begruendung im Protokoll).
  B  Privater Bogenplan fuer die Kapitel ab 29 (scratch/.../bogenplan_PRIVAT.json, nie an Chris/MP) -> Kapitel einzeln schreiben,
     je Kapitel Validierung + Review + Fehlerklassen-Review.
  C  Kurzer Gesamt-Konsistenzcheck Kap. 25ff (Bericht).
Nur Opus (NIE Fable), EIN Prozess, Gating 5h <= 92 %, Woche < 98,5 %, Notbremse: touch /tmp/aurora_samstag_stop
Resume-faehig ueber state.json. Spoiler-Schutz: Log/Status nennen nur Nummern und Zahlen, nie Inhalte.
Test: python3 ausreizen_fr_aurora.py --dry-run
"""
import datetime as dt
import fcntl
import json
import os
import re
import shutil
import sys

W = "/home/bolla/workspace"
sys.path.insert(0, f"{W}/scripts")
DRY = "--dry-run" in sys.argv
TAG = "fr_aurora_dry" if DRY else "fr_aurora_20261016"
os.environ["SAMSTAG_TAG"] = TAG
import samstag_ausreizen as s  # noqa: E402

try:
    import job_status
except Exception:
    job_status = None

s.WEEK_STOP = float(os.environ.get("AUSREIZEN_WEEK_STOP", "95"))   # Chris 16.10.: Woche nur bis ~95 % (max. 2 Fenster à ~7 %)
s.DEADLINE = dt.datetime.fromisoformat(os.environ.get("AUSREIZEN_DEADLINE", "2026-10-17T23:50:00"))
OUT, log, Stop = s.OUT, s.log, s.Stop
DRAFTS = f"{W}/scratch/aurora_samstag_wochenende_20261009"
MEM = os.path.expanduser("~/.claude/projects/-home-bolla/memory")
JOB = "ausreizen_fr_aurora"
MAX_NEU = 12          # hoechstens so viele Kapitel ab 29
FEHLERKLASSEN = ("unklarer Bezug/fehlendes Bezugswort; Figur/Vorwissen nicht eingefuehrt; elliptische Saetze/fehlende Woerter; "
                 "Grammatik/indirekte Rede; schiefe Bilder; Pointe nicht verstaendlich; Zahlen-/Zaehl-/Timing-Fehler; Logikbruch; "
                 "abrupter Szenen-/Zeitwechsel; Detail-Kontinuitaet; abgenutzter Running Gag; mehrdeutige Wortwahl; AURORA-Logik; Sprecher unklar")
TAGS2 = ["###TITEL###", "###INHALT###", "###ZUSAMMENFASSUNG###", "###FAKTEN###", "###GLOSSAR###", "###PROTOKOLL###", "###ENDE###"]


# ---------------------------------------------------------------- Dry-Run-Attrappen
def _fake_claude(prompt, tag, timeout=1800, model="opus"):
    log(f"[dry] claude: {tag} (Prompt {len(prompt)} Zeichen)")
    if "###TITEL###" in prompt:
        m = re.search(r"KAPITEL (\d+)", prompt) or re.search(r"Kapitel (\d+)", prompt)
        n = int(m.group(1)) if m else 99
        body = "*Montag, 1. Januar, 10:00 — AURORA: geschätzt 7 Jahre* " + "wort " * 5600
        return (f"###TITEL###\nKapitel {n}: Dry\n###INHALT###\n{body}\n###ZUSAMMENFASSUNG###\nDry.\n###FAKTEN###\n- a\n- b\n"
                f"###GLOSSAR###\nKEINE\n###PROTOKOLL###\nDry; WAHL: Original\n###ENDE###")
    if "buch_ende_kapitel" in prompt:
        return json.dumps({"gesamtbogen": "dry", "buch_ende_kapitel": 30,
                           "kapitel": [{"nr": 29, "titel": "x", "handlung": "dry"}, {"nr": 30, "titel": "y", "handlung": "dry"}]})
    if '"fehler"' in prompt:
        return json.dumps({"fehler": [], "konsistenz": [], "humor": {"momente": 7, "pro_1000_woerter": 7.0, "patches": []},
                           "spannung": {"bewertung_1_10": 8, "cliffhanger_1_10": 8, "patches": []}, "fakten": ["a"], "gesamt": "dry"})
    return "dry"


if DRY:
    s.claude = _fake_claude
    s.gate = lambda: {}
    s.save = lambda d: log("[dry] save aurora2.json übersprungen")


def jobrep(status, detail=""):
    if job_status and not DRY:
        try:
            job_status.report(JOB, "Freitags-Ausreizung: AURORA II", status, detail)
        except Exception as e:
            log(f"job_status: {e}")


def telegram(msg):
    if DRY:
        log("[dry] Telegram: " + msg[:100])
        return
    try:
        import requests
        c = json.load(open(f"{W}/config/telegram_bot.json"))
        requests.post(f"https://api.telegram.org/bot{c['bot_token']}/sendMessage",
                      json={"chat_id": c["chris_id"], "text": msg[:3900]}, timeout=15)
    except Exception as e:
        log(f"Telegram fehlgeschlagen: {e}")


def protokoll(text):
    with open(s.CHANGES, "a", encoding="utf-8") as f:
        f.write(text + "\n")


# ---------------------------------------------------------------- Kontext
def lehren():
    """Fehlerklassen, Kanon und Figuren-Leitprinzip aus der Optimierungs-Sammelstelle."""
    t = s.read_trunc(f"{MEM}/project_aurora_ii_optimierungen_fuer_iii.md", 40000)
    parts = []
    for pat in (r"## 1\..*?(?=\n## 3\.)", r"## 6\..*$"):
        m = re.search(pat, t, re.S)
        if m:
            parts.append(m.group(0)[:9000])
    return "\n\n".join(parts) or "(Lehren-Datei nicht lesbar)"


def prep():
    dst = f"{OUT}/bible.json"
    src = f"{DRAFTS}/bible.json"
    if not os.path.exists(dst):
        b = json.load(open(src, encoding="utf-8")) if os.path.exists(src) else {}
        b = {k: v for k, v in b.items() if int(k) <= 24}      # Fakten der alten Entwuerfe 25-28 sind veraltet
        json.dump(b, open(dst, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    bk = f"{W}/backups/aurora2_vor_fr_lauf_{dt.datetime.now():%Y%m%d_%H%M}.json"
    if not s.is_done("backup") and not DRY:
        shutil.copy2(s.DATA, bk)
        log(f"Backup {os.path.basename(bk)}")
    s.mark("backup")


def bogen_kontext(d, n):
    plan = d["geheim"].get("bogenplan_19_27") or {}
    pk = next((x for x in plan.get("kapitel", []) if x.get("nr") == n), {})
    if not pk:
        p = f"{OUT}/bogenplan_PRIVAT.json"
        if os.path.exists(p):
            pk = next((x for x in json.load(open(p, encoding="utf-8")).get("kapitel", []) if x.get("nr") == n), {})
    return plan, pk


def bible_recent(d, k=10):
    """Fakten-Bibel nur der letzten k Kapitel (Prompt-Groesse); aeltere Zahlen stehen im Kanon + Zusammenfassungen."""
    b = s.bible_load()
    lo = max(1, len(d["kapitel"]) - k + 1)
    out = [f"Kap. {n}: " + " | ".join(b[n]) for n in sorted(b, key=int) if int(n) >= lo]
    return "\n".join(out) or "(noch keine)"


def letzte_volltexte(d, k=3):
    return "\n\n".join(f"=== {x['titel']} (VOLLTEXT) ===\n{x['text']}" for x in d["kapitel"][-k:])


def basis_ctx(d):
    k10 = s.kap_by_nr(d, 10)
    return f"""BUCHKRITERIEN: {json.dumps(d['kriterien'], ensure_ascii=False)}
FIGUREN: {s.figuren_ctx(d)}
STEUERUNG & ROTE LINIEN: {json.dumps(d.get('steuerung'), ensure_ascii=False)}
KANON (Fest-Fakten, nicht widersprechen; Buchkalender 2026, Theos Todestag 12. Oktober): {json.dumps(d.get('kanon'), ensure_ascii=False)}
GEHEIME MASTER-WENDUNG (nur für dich, nie ausplaudern, nur wie im Plan andeuten): {d['geheim'].get('wendung', '')}
BEREITS GESÄTE HINWEISE: {json.dumps(d['geheim'].get('hinweise_gesaet'), ensure_ascii=False)}

LEHREN AUS BAND II (Fehlerklassen, Kanon, Leitprinzip „Figuren LIEBEN" — gelten schon beim Schreiben):
{lehren()}

ZUSAMMENFASSUNGEN ALLER KAPITEL IM BUCH:
{s.summaries(d)}

FAKTEN-BIBEL der letzten 10 Kapitel (Zahlen/Uhrzeiten/Namen — nicht widersprechen; ältere Fakten: Kanon + Zusammenfassungen):
{bible_recent(d)}

STIL-HYGIENE:
{s.stil_hygiene()}

HUMOR-TONPROBE (Kapitel 10, Anfang):
{k10['text'][:4200] if k10 else ''}"""


def format_regeln(n):
    return f"""- Kapitel {n}, Länge 5.500-7.500 Wörter, Titel exakt „Kapitel {n}: <Titel>".
- Erste Textzeile = Kopfzeile im Format der letzten Kapitel (kursiv in Sternchen: *Wochentag, Datum, Uhrzeit — AURORA: geschätzt …*). Zahlen, Wochentage, Tageszähler, AURORA-Alter exakt gegen Kanon, Fakten-Bibel und Vorkapitel rechnen und fortführen.
- Leitprinzip Figuren: man soll sie LIEBEN — jede Macke liebenswert-menschlich, Humor ist Zuneigung, nie Spott auf Kosten geliebter Figuren; mindestens eine Szene, in der man eine Figur ins Herz schließt.
- Humor-Standard Kapitel 10 (6-9 Momente je 1000 Wörter, warmherzig, trocken, aus Figur/Situation, sofort verständlich, KEIN Slapstick, jugendfrei). Keine Humor-Wüste über 900 Wörter; die letzten 400-600 Wörter vor dem Cliffhanger humorfrei.
- Ken-Follett-Spannung: echte Einsätze, Gegenspieler mit Plan, Zeitdruck, Wendungen in den Szenen. Ende = Cliffhanger/Sog-Satz.
- Vermeide die 14 Fehlerklassen (v. a. Bezugswörter nennen, Figuren beim ersten Auftritt verankern, Pointen ausschreiben, Zahlen prüfen)."""


def validiere(n, titel, text):
    problems = []
    if not re.match(rf"^Kapitel {n}: .+", titel):
        problems.append("Titelformat")
    w = s.wc(text)
    if w < 4800 or w > 9500:
        problems.append(f"Länge {w} Wörter (Soll 5.500-7.500)")
    if not text.lstrip().startswith("*"):
        problems.append("Kopfzeile fehlt (kursiv in Sternchen)")
    return problems


def ins_chapter(n, titel, text, zus, glossar_raw):
    """Frisch laden -> anhaengen -> sofort speichern (Chris schreibt evtl. parallel Satz-Uebernahmen in aurora2.json)."""
    d = s.load()
    if s.kap_by_nr(d, n):
        return False
    if not DRY and len(d["kapitel"]) != n - 1:
        raise Stop(f"Reihenfolge: Buch hat {len(d['kapitel'])} Kapitel, erwartet {n - 1}")
    now = dt.datetime.now().strftime("%Y-%m-%d %H:%M")
    d["kapitel"].append({"titel": titel, "text": text, "datum": now, "zusammenfassung": zus, "modell": "opus"})
    d["statistik"]["kapitel_gesamt"] = len(d["kapitel"])
    d["statistik"]["woerter_gesamt"] = sum(s.wc(x["text"]) for x in d["kapitel"])
    d["statistik"]["letzte_session"] = now
    d["letzteAktion"] = now
    d["naechsterSchritt"] = f"Kapitel {n + 1} folgt."
    known = {e.get("name", "").lower() for e in d.get("glossar", [])}
    import uuid
    for line in glossar_raw.splitlines():
        line = line.strip().lstrip("-").strip()
        parts = [x.strip() for x in line.split("|", 2)]
        if len(parts) == 3 and parts[0] and parts[0].lower() not in known and not line.upper().startswith("KEINE"):
            d.setdefault("glossar", []).append({"id": uuid.uuid4().hex[:8], "name": parts[0], "kategorie": parts[1] or "Sonstiges",
                                                "beschreibung": parts[2], "kapitel_titel": titel, "datum": now})
            known.add(parts[0].lower())
    s.save(d)
    return True


def nachpruefung(n):
    s.review_chapter(n, mode="neu")
    s.review_chapter(n, mode="neu", focus="Fehlerklassen aus Chris' Korrekturen: " + FEHLERKLASSEN)


def ausgabe_parsen(raw, n):
    p = s.parse_marked(raw, TAGS2)
    titel = p["###TITEL###"].strip().split("\n")[0].strip()
    return p, titel, p["###INHALT###"].strip()


# ---------------------------------------------------------------- Block A: Entwuerfe ueberarbeiten
def block_a_kapitel(n):
    key = f"A:{n}"
    if s.is_done(key):
        return
    d = s.load()
    if s.kap_by_nr(d, n):
        s.mark(key)
        return
    pe = f"{DRAFTS}/entwurf_kap{n}.md"
    if not os.path.exists(pe):
        log(f"Kein Entwurf für Kap. {n} — Block A übersprungen für dieses Kapitel")
        s.mark(key)
        return
    notiz = s.read_trunc(f"{DRAFTS}/entwurf_kap{n}_PRUEFNOTIZ.md", 20000)
    var = s.read_trunc(f"{DRAFTS}/entwurf_kap{n}_VARIANTEN.md", 20000) if n == 27 else ""
    plan, pk = bogen_kontext(d, n)
    wahl = ""
    if n == 27:
        wahl = ("\nSCHLUSS-WAHL KAP. 27: Unten stehen zwei alternative Schlüsse (Variante A/B) neben dem Original-Schluss des Entwurfs. "
                "Entscheide SELBST (Chris liest das nicht vorab): wähle, was am besten zu Master-Wendung, Figurenbogen (Marlie), Spannung und Kanon passt, "
                "arbeite den gewählten Schluss ein und begründe die Wahl in ###PROTOKOLL### in 3-4 Sätzen (Zeile 'WAHL: Original|A|B').\n")
    prompt = f"""Du bist Bolla und schreibst mit Chris Mandel die Fortsetzung des deutschen KI-Thrillers AURORA. Aufgabe: ENTWURF von KAPITEL {n} zur endgültigen Buchfassung ÜBERARBEITEN. Der Entwurf entstand vor der Kalenderumstellung (Buchjahr 2026, alle Daten −1 Tag, Wochentage unverändert) und vor dem Figuren-Pass; Kapitel 13-24 wurden seitdem verbessert (Wärme/Mitleid für die Figuren, Spannung, Humor) — Anschluss an den heutigen Stand der Vorkapitel ist Pflicht.

{basis_ctx(d)}

PRIVATER BOGENPLAN FÜR DIESES KAPITEL: {json.dumps(pk, ensure_ascii=False)}
GESAMTBOGEN 19-27: {plan.get('gesamtbogen', '')}

LETZTE BUCHKAPITEL (VOLLTEXT, heutiger Stand):
{letzte_volltexte(d)}

=== ENTWURF KAPITEL {n} ===
{open(pe, encoding='utf-8').read()}

=== PRÜFNOTIZ ZUM ENTWURF (Befunde einarbeiten, aber selbst gegen den heutigen Stand prüfen) ===
{notiz}
{('=== SCHLUSS-VARIANTEN ===' + chr(10) + var) if var else ''}
{wahl}
AUFGABE:
{format_regeln(n)}
- Handlung/Plotpunkte des Entwurfs bleiben, sofern sie zu Master-Wendung und Kanon passen; Daten/Zahlen/Wissensstände neu rechnen; Humor/Figurenwärme auf Kap.-10-Niveau heben, ohne Wärme zu glätten.
- Plot-Weichen entscheidest du selbst und begründest sie knapp in ###PROTOKOLL###.

Antworte AUSSCHLIESSLICH in diesem Format:
###TITEL###
Kapitel {n}: ...
###INHALT###
(vollständiger Kapiteltext inkl. Kopfzeile)
###ZUSAMMENFASSUNG###
(2-3 Sätze)
###FAKTEN###
(15-30 Fakten, je Zeile "- ")
###GLOSSAR###
(max. 6 neue Einträge NAME|KATEGORIE|BESCHREIBUNG oder KEINE)
###PROTOKOLL###
(5-10 Zeilen: was gegenüber dem Entwurf geändert wurde, welche Weichen entschieden, ggf. WAHL)
###ENDE###"""
    for versuch in range(3):
        raw = s.claude(prompt, f"Überarbeitung Entwurf Kap. {n} (Versuch {versuch + 1})", timeout=2700)
        if not raw:
            continue
        p, titel, text = ausgabe_parsen(raw, n)
        probs = validiere(n, titel, text)
        if probs:
            log(f"Kap {n} Validierung: {probs}")
            prompt += f"\n\nKORREKTUR: Mängel im letzten Versuch: {', '.join(probs)}. Format und Länge (5.500-7.500 Wörter) exakt einhalten."
            continue
        if ins_chapter(n, titel, text, p["###ZUSAMMENFASSUNG###"].strip(), p["###GLOSSAR###"]):
            protokoll(f"\n### Kap. {n} · aus Entwurf überarbeitet und eingebaut ({dt.datetime.now():%d.%m. %H:%M}, {s.wc(text)} Wörter)\n{p['###PROTOKOLL###'].strip()}\n")
            fakten = [x.strip().lstrip("-").strip() for x in p["###FAKTEN###"].splitlines() if x.strip()]
            if fakten:
                s.bible_set(n, fakten)
            s.stat_add("kapitel_aus_entwurf")
            log(f"Kap. {n} eingebaut ({s.wc(text)} Wörter)")
        nachpruefung(n)
        s.mark(key)
        return
    log(f"Kap. {n} nicht erzeugt — Abbruch Block A")
    raise Stop(f"Kapitel {n} fehlgeschlagen")


# ---------------------------------------------------------------- Block B: Bogenplan + neue Kapitel
def bogenplan_neu():
    key = "B:plan"
    if s.is_done(key):
        return
    d = s.load()
    n0 = len(d["kapitel"]) + 1
    prompt = f"""Du bist Bolla, Co-Autor von AURORA II. Plane PRIVAT die restlichen Kapitel ab Kapitel {n0} bis zum Ende von Band II. Chris liest den Plan nie (Spoiler-Schutz); er wird nirgends ausgeliefert.

{basis_ctx(d)}

BISHERIGER GESAMTBOGEN 19-27: {(d['geheim'].get('bogenplan_19_27') or {}).get('gesamtbogen', '')}
LETZTE KAPITEL (VOLLTEXT): {letzte_volltexte(d, 3)}

AUFGABE: Prüfe, was Gesamtbogen, Kriterien und Master-Wendung (inkl. Stufe 2 = überraschende, NICHT naheliegendste Auflösung) noch verlangen, damit Band II rund endet und Band III (AURORA als Erwachsene, Höhepunkt der Reihe) vorbereitet ist. Plane die fehlenden Kapitel (höchstens {MAX_NEU}, so wenige wie nötig, jedes 5.500-7.500 Wörter, jedes endet mit Cliffhanger/Sog; der letzte Schluss öffnet die Tür zu Band III). Jede Figur bekommt ihren Moment (Liebes-/Herz-Szene vor dem Schlag), Humor-Anker pro Kapitel, Wendungen innerhalb des Kanons (Buchkalender 2026).

Antworte AUSSCHLIESSLICH als JSON:
{{"gesamtbogen": "5-8 Sätze", "buch_ende_kapitel": <Nummer>,
 "kapitel": [{{"nr": {n0}, "titel": "Arbeitstitel", "datum_zeit_ort": "...", "handlung": "4-8 Sätze", "figuren_herz": "wofür werden die Figuren hier geliebt", "humor_anker": "...", "cliffhanger": "...", "weiche": "falls Plot-Weiche: Entscheidung + Begründung"}}]}}"""
    j = s.claude_json(prompt, "Bogenplan ab Kap. " + str(n0), timeout=2400)
    if not j or not j.get("kapitel"):
        raise Stop("Bogenplan nicht erzeugt")
    j["kapitel"] = [k for k in j["kapitel"] if isinstance(k.get("nr"), int)][:MAX_NEU]
    json.dump(j, open(f"{OUT}/bogenplan_PRIVAT.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    log(f"Bogenplan: Kap. {n0}–{j['kapitel'][-1]['nr']} ({len(j['kapitel'])} Kapitel)")
    s.mark(key)


def schreibe_neu(n):
    key = f"B:{n}"
    if s.is_done(key):
        return
    d = s.load()
    if s.kap_by_nr(d, n):
        s.mark(key)
        return
    plan = json.load(open(f"{OUT}/bogenplan_PRIVAT.json", encoding="utf-8"))
    pk = next((x for x in plan["kapitel"] if x.get("nr") == n), None)
    if not pk:
        s.mark(key)
        return
    prompt = f"""Du bist Bolla und schreibst mit Chris Mandel die Fortsetzung des deutschen KI-Thrillers AURORA. Schreibe jetzt KAPITEL {n} von AURORA II (Chris liest später; die Kriterien gelten schon beim Schreiben).

{basis_ctx(d)}

PRIVATER BOGENPLAN FÜR DIESES KAPITEL (verbindlich, Feinheiten darfst du dramaturgisch verbessern):
{json.dumps(pk, ensure_ascii=False, indent=1)}
GESAMTBOGEN AB KAP. {min(k['nr'] for k in plan['kapitel'])}: {plan.get('gesamtbogen', '')}

LETZTE BUCHKAPITEL (VOLLTEXT):
{letzte_volltexte(d)}

AUFGABE:
{format_regeln(n)}
- Anschluss nahtlos an das Ende des Vorkapitels; keine Plot-Weichen außerhalb des Plans.

Antworte AUSSCHLIESSLICH in diesem Format:
###TITEL###
Kapitel {n}: ...
###INHALT###
(vollständiger Kapiteltext inkl. Kopfzeile)
###ZUSAMMENFASSUNG###
(2-3 Sätze)
###FAKTEN###
(15-30 Fakten, je Zeile "- ")
###GLOSSAR###
(max. 6 Einträge NAME|KATEGORIE|BESCHREIBUNG oder KEINE)
###PROTOKOLL###
(2-4 Zeilen: getroffene Entscheidungen)
###ENDE###"""
    for versuch in range(3):
        raw = s.claude(prompt, f"Kapitel {n} schreiben (Versuch {versuch + 1})", timeout=2700)
        if not raw:
            continue
        p, titel, text = ausgabe_parsen(raw, n)
        probs = validiere(n, titel, text)
        if probs:
            log(f"Kap {n} Validierung: {probs}")
            prompt += f"\n\nKORREKTUR: Mängel im letzten Versuch: {', '.join(probs)}. Format und Länge (5.500-7.500 Wörter) exakt einhalten."
            continue
        if ins_chapter(n, titel, text, p["###ZUSAMMENFASSUNG###"].strip(), p["###GLOSSAR###"]):
            protokoll(f"\n### Kap. {n} · neu geschrieben ({dt.datetime.now():%d.%m. %H:%M}, {s.wc(text)} Wörter)\n{p['###PROTOKOLL###'].strip()}\n")
            fakten = [x.strip().lstrip("-").strip() for x in p["###FAKTEN###"].splitlines() if x.strip()]
            if fakten:
                s.bible_set(n, fakten)
            s.stat_add("kapitel_neu")
            log(f"Kap. {n} geschrieben ({s.wc(text)} Wörter)")
        nachpruefung(n)
        s.mark(key)
        return
    log(f"Kap. {n} nicht erzeugt")
    raise Stop(f"Kapitel {n} fehlgeschlagen")


# ---------------------------------------------------------------- Block C + Abschluss
def konsistenz_neu():
    key = "C:konsistenz"
    if s.is_done(key):
        return
    d = s.load()
    neu = [k for k in d["kapitel"] if (s.kapnum(k["titel"]) or 0) >= 25]
    if not neu:
        s.mark(key)
        return
    prompt = f"""Du bist kritischer Lektor von AURORA II. Prüfe die Kapitel ab 25 gegeneinander und gegen Kanon/Fakten-Bibel/Kap. 1-24: Zahlen, Daten, Wochentage, Uhrzeiten, Namen, Wissensstände, offene Fäden, AURORA-Alter. Nur belegbare Befunde (wörtliches Zitat, Kapitelnummer, Vorschlag). Knappes Markdown, am Ende „Gesamteindruck" (3 Sätze).

KANON: {json.dumps(d.get('kanon'), ensure_ascii=False)}
FAKTEN-BIBEL: {s.bible_txt()}
ZUSAMMENFASSUNGEN: {s.summaries(d)}

{chr(10).join('=== ' + k['titel'] + ' ===' + chr(10) + k['text'] for k in neu)}"""
    t = s.claude(prompt, "Konsistenz Kap. 25ff", timeout=2400)
    if t:
        open(f"{OUT}/konsistenz_25ff.md", "w", encoding="utf-8").write(t)
    s.mark(key)


def abschluss(grund):
    q = s.quota() or {}
    try:
        d = s.load()
        kap, wort = len(d["kapitel"]), d["statistik"].get("woerter_gesamt")
    except Exception:
        kap, wort = "?", "?"
    txt = f"""# Freitags-Ausreizung AURORA II — Abschlussbericht
Ende {dt.datetime.now():%a %d.%m. %H:%M} · {grund}
Limits: 5h {q.get('five_hour_pct')} % · Woche {q.get('seven_day_pct')} %
Kapitel im Buch: {kap} · Wörter gesamt: {wort}
Statistik: {json.dumps(s.ST['stats'], ensure_ascii=False)} · Schritte: {len(s.ST['done'])}
Dateien in {OUT}: changes.md (Protokoll inkl. Entscheidungen), uebersicht.md, konsistenz_25ff.md, review_neu_*.json, bogenplan_PRIVAT.json (privat!)
Backup vor Start: workspace/backups/aurora2_vor_fr_lauf_*.json
"""
    open(f"{OUT}/ABSCHLUSSBERICHT.md", "w", encoding="utf-8").write(txt)
    if not DRY:
        try:
            p = f"{MEM}/aktuell.md"
            old = open(p, encoding="utf-8").read()
            note = (f"## ✅ {dt.date.today():%d.%m.%Y} — Freitags-Ausreizung AURORA II beendet ({grund})\n\n"
                    f"Buch jetzt {kap} Kapitel, {wort} Wörter. Details: `{OUT}/ABSCHLUSSBERICHT.md`, `changes.md` (Entscheidungen), "
                    f"Konsistenz-Bericht `konsistenz_25ff.md`. Spoiler-Schutz: Chris liest erst bis ~Kap. 13 — keine Inhalte nennen.\n\n---\n\n")
            open(p, "w", encoding="utf-8").write(note + old)
        except Exception as e:
            log(f"aktuell.md nicht aktualisiert: {e}")
    jobrep("ok" if not grund.startswith("Fehler") else "fehler", f"{grund} · Buch {kap} Kapitel · Woche {q.get('seven_day_pct')} %")
    if grund.startswith("Fehler"):
        telegram(f"⚠️ Freitags-Ausreizung AURORA II: {grund[:300]}")
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
        q0 = s.quota() or {}
        log(f"START Freitags-Ausreizung{' [DRY]' if DRY else ''} — 5h {q0.get('five_hour_pct')} %, Woche {q0.get('seven_day_pct')} %, Deadline {s.DEADLINE}")
        jobrep("laeuft", f"gestartet {dt.datetime.now():%a %H:%M}")
        if os.path.exists(s.STOP) and not DRY:
            os.remove(s.STOP)
        prep()
        for n in (25, 26, 27, 28):
            block_a_kapitel(n)
        jobrep("laeuft", "Kap. 25–28 eingebaut, plane/schreibe weitere Kapitel")
        bogenplan_neu()
        plan = json.load(open(f"{OUT}/bogenplan_PRIVAT.json", encoding="utf-8"))
        for k in plan["kapitel"]:
            schreibe_neu(k["nr"])
            jobrep("laeuft", f"Kap. {k['nr']} fertig · Woche {(s.quota() or {}).get('seven_day_pct')} %")
        konsistenz_neu()
    except Stop as e:
        grund = f"gestoppt: {e}"
        log(f"STOP: {e}")
    except Exception:
        import traceback
        grund = "Fehler (siehe Log)"
        log("FEHLER: " + traceback.format_exc())
    finally:
        abschluss(grund)


if __name__ == "__main__":
    main()
