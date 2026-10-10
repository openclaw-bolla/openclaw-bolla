#!/usr/bin/env python3
"""Samstags-Ausreizung Teil 2 (Chris-Freigabe 10.10.2026): AURORA II NUR LESEN + BERICHTEN, nie am Buch ändern.

Hintergrund: Chris liest Kap. 10-24 selbst und arbeitet Korrekturen selbst ein (Plan 04.10.). Deshalb KEINE Patches in aurora2.json
(s.save wird gesperrt). Alle Funde landen als JSON in scratch/aurora_samstag_sa2_<Tag>/ und am Ende/zwischendurch als EIN HTML-Bericht
auf dem Desktop (Vormerkliste für die zwei Lektorläufe am Schluss).

Reihenfolge (wichtigstes zuerst, falls Kontingent endet):
  1 Analogie-Check  — Fehlerklassen aus Chris' übernommenen Satz-Korrekturen ableiten, alle Kapitel (1-24 + Entwürfe 25-27) danach durchsuchen
  2 Zweitleser      — Verständlichkeit/Tempo/Spannung/Humor je Kapitel aus Lesersicht (+ Entwürfe 25-27)
  3 Band-I-Gegencheck (nur Bericht)
  4 Lesebegleiter + Memory-Hygiene-Bericht
  5 Fehlerjagd-Runden mit wechselndem Fokus (Kap. 1-24), bis Deadline / Limit
Gating wie samstag_ausreizen.py: 5h <= 92 %, Woche < 98,5 %. Nur Opus/Sonnet — NIE Fable. Keine Mails, nichts löschen.
Notbremse: touch /tmp/aurora_samstag_stop
"""
import datetime as dt
import fcntl
import glob
import html
import json
import os
import re
import shutil
import sys

W = "/home/bolla/workspace"
sys.path.insert(0, f"{W}/scripts")
TAG = os.environ.get("AUSREIZEN_TAG") or dt.date.today().strftime("%Y%m%d")
os.environ["SAMSTAG_TAG"] = "sa2_" + TAG
import samstag_ausreizen as s  # noqa: E402

s.NEU_BIS = 24  # Lesebegleiter nur bis zum letzten Buchkapitel
if os.environ.get("AUSREIZEN_DEADLINE"):
    s.DEADLINE = dt.datetime.fromisoformat(os.environ["AUSREIZEN_DEADLINE"])


def _no_save(*a, **k):
    raise RuntimeError("Lesebericht-Lauf darf aurora2.json NICHT schreiben")


s.save = _no_save  # Sicherung: schreibender Zugriff unmöglich

OUT = s.OUT
log = s.log
Stop = s.Stop
DESKTOP = "/mnt/d/OneDrive/Desktop"
REPORT = f"{DESKTOP}/AURORA_II_Lesebericht_{TAG}.html"
JOB = "ausreizen_sa2_lesebericht"

try:
    import job_status
except Exception:
    job_status = None


def jobrep(status, detail=""):
    if job_status:
        try:
            job_status.report(JOB, "Samstags-Ausreizung: AURORA-II-Lesebericht", status, detail)
        except Exception as e:
            log(f"job_status: {e}")


# ------------------------------------------------------------------ Kapitel-Zugriff (read-only)
def chapters():
    """[(nr, titel, text, quelle)] — Buchkapitel + Entwürfe 25-27 aus dem Vortag (nur Datei)."""
    d = s.load()
    out = []
    for k in d["kapitel"]:
        n = s.kapnum(k["titel"])
        if n:
            out.append((n, k["titel"], k["text"], "buch"))
    dr = sorted(glob.glob(f"{W}/scratch/aurora_samstag_wochenende_*/entwurf_kap2[5-7].md"))
    latest = {}
    for p in dr:
        latest[int(re.search(r"kap(\d+)", p).group(1))] = p
    for n in sorted(latest):
        if n > max([c[0] for c in out] or [0]):
            t = open(latest[n], encoding="utf-8").read()
            out.append((n, f"Kapitel {n} (ENTWURF, nicht im Buch)", t, "entwurf"))
    return out


def neighbors(chs, n):
    prev = next((c for c in chs if c[0] == n - 1), None)
    nxt = next((c for c in chs if c[0] == n + 1), None)
    return (prev[2][-1500:] if prev else "(kein Vorkapitel)", nxt[2][:800] if nxt else "(kein Folgekapitel)")


def save_json(name, j):
    json.dump(j, open(f"{OUT}/{name}", "w", encoding="utf-8"), ensure_ascii=False, indent=1)


# ------------------------------------------------------------------ 1 Analogie-Check
def analogie():
    d = s.load()
    cls_path = f"{OUT}/analogie_klassen.json"
    if not s.is_done("1:klassen"):
        mk = [m for m in d.get("satz_markierungen", []) if m.get("status") == "uebernommen" and m.get("vorschlag")]
        ab = [m for m in d.get("satz_markierungen", []) if m.get("status") == "abgelehnt"]
        def fmt(m):
            return (f"- [{m.get('kapitel_titel', '')[:22]}] Satz: {m.get('satz', '')[:220]} | Chris: {m.get('frage', '')[:200]} "
                    f"| übernommen als: {m.get('vorschlag', '')[:220]}")
        prompt = f"""Du bist Lektor von AURORA II. Chris (Autor) hat im Buch Sätze markiert und Korrekturen übernommen. Leite daraus die FEHLERKLASSEN ab, die er als störend empfindet (z.B. Bezug unklar, Witz nicht verständlich, Wortwiederholung, Business-Jargon, Füllsatz, Zahlen-/Timing-Ungenauigkeit, zu lange Satzketten, ...).

ÜBERNOMMENE KORREKTUREN ({len(mk)}):
{chr(10).join(fmt(m) for m in mk[:170])}

ABGELEHNTE VORSCHLÄGE (Gegenprobe: das will Chris NICHT geändert haben, {len(ab)}):
{chr(10).join('- ' + m.get('satz', '')[:160] + ' | Chris: ' + m.get('frage', '')[:120] for m in ab[:60])}

Antworte AUSSCHLIESSLICH mit JSON: {{"klassen":[{{"name":"...","beschreibung":"woran man den Fehler erkennt, in 1-2 Sätzen","beispiel_vorher":"...","beispiel_nachher":"...","haeufigkeit":0}}],"nicht_aendern":["Muster, die Chris bewusst behalten will (aus den abgelehnten Vorschlägen)"]}}
Maximal 14 Klassen, nur belegbare."""
        j = s.claude_json(prompt, "Analogie: Fehlerklassen")
        if j is None:
            return
        save_json("analogie_klassen.json", j)
        s.mark("1:klassen")
    kl = json.load(open(cls_path, encoding="utf-8"))
    chs = chapters()
    for n, titel, text, quelle in chs:
        key = f"1:ana:{n}"
        if s.is_done(key):
            continue
        pv, nx = neighbors(chs, n)
        prompt = f"""Du bist Lektor von AURORA II (deutscher KI-Thriller, warmer Humor). Suche in diesem Kapitel Stellen, die zu den FEHLERKLASSEN passen, die Chris in anderen Kapiteln bereits korrigiert hat (Analogie-Check). NUR BERICHT — nichts wird geändert.

FEHLERKLASSEN:
{json.dumps(kl.get('klassen'), ensure_ascii=False)}
CHRIS WILL BEWUSST BEHALTEN (nicht anmahnen): {json.dumps(kl.get('nicht_aendern'), ensure_ascii=False)}

ENDE VORKAPITEL: ...{pv}
ANFANG FOLGEKAPITEL: {nx}...

=== {titel} ===
{text}
=== ENDE ===

Antworte AUSSCHLIESSLICH mit JSON: {{"funde":[{{"klasse":"...","zitat":"WÖRTLICH aus dem Kapitel, 8-30 Wörter","problem":"...","vorschlag":"konkrete Ersatzformulierung","sicherheit":"hoch|mittel"}}]}}
Nur echte, belegbare Funde, höchstens 12; leere Liste ist ein gutes Ergebnis. Keine Geschmacksfragen."""
        j = s.claude_json(prompt, f"Analogie Kap {n}")
        if j is not None:
            j["kapitel"] = n
            j["quelle"] = quelle
            save_json(f"analogie_kap{n}.json", j)
            s.mark(key)
            build_report()


# ------------------------------------------------------------------ 2 Zweitleser
def zweitleser():
    chs = chapters()
    for n, titel, text, quelle in chs:
        key = f"2:zl:{n}"
        if s.is_done(key):
            continue
        pv, nx = neighbors(chs, n)
        prompt = f"""Du bist ein kluger Erstleser (kein Autor) von AURORA II, einem deutschen KI-Thriller mit warmem, trockenem Humor (kein Slapstick). Der Autor ist 70, lernt Schreiben im Lauf des Buchs und will wissen, wo ein Leser stolpert. NUR BERICHT, es wird nichts geändert.

Beurteile Kapitel {n} aus Leserperspektive:
1. VERSTÄNDLICHKEIT: Stellen, an denen ein Leser nicht versteht, worauf sich etwas bezieht (Pronomen, Zeitsprung ohne Anker, Fachbegriff ohne Erklärung, Witz, der Vorwissen braucht).
2. TEMPO/SPANNUNG: Wo zieht es sich, wo fehlt der Einsatz, wo funktioniert der Cliffhanger nicht?
3. HUMOR: Pointen, die nicht zünden oder erklärt werden müssen; Humor-Wüsten (> 900 Wörter ohne Lächeln).
4. FIGUREN: Verhält sich jemand untypisch? Wissensstand-Fehler (weiß etwas, was er noch nicht wissen kann)?
5. Was hat besonders gut funktioniert (3 Stellen mit kurzem Zitat)?

KANON/FAKTEN: {json.dumps(s.load().get('kanon'), ensure_ascii=False)[:3500]}
ENDE VORKAPITEL: ...{pv}
ANFANG FOLGEKAPITEL: {nx}...

=== {titel} ({s.wc(text)} Wörter) ===
{text}
=== ENDE ===

Antworte AUSSCHLIESSLICH mit JSON: {{"stolpersteine":[{{"zitat":"WÖRTLICH, 8-30 Wörter","problem":"...","vorschlag":"..."}}],"tempo":{{"bewertung_1_10":0,"zaeh_stellen":["..."],"cliffhanger_1_10":0}},"humor":{{"pro_1000_woerter":0.0,"wuesten":["..."],"schwache_pointen":[{{"zitat":"...","problem":"..."}}]}},"figuren":["..."],"gelungen":[{{"zitat":"...","warum":"..."}}],"gesamt":"3-4 Sätze"}}
Höchstens 10 Stolpersteine, nur belegbare."""
        j = s.claude_json(prompt, f"Zweitleser Kap {n}")
        if j is not None:
            j["kapitel"] = n
            j["quelle"] = quelle
            save_json(f"zweitleser_kap{n}.json", j)
            s.mark(key)
            build_report()


# ------------------------------------------------------------------ 3 Band-I-Gegencheck (nur Bericht)
def band1():
    if s.is_done("3:band1"):
        return
    d = s.load()
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
    prompt = f"""Prüfe die Anschlussstellen von AURORA II (Band II) an Band I. NUR BERICHT. Unten Auszüge der Schluss-/Schlüsselkapitel von Band I und die Zusammenfassungen/Fakten von Band II.
Finde echte Widersprüche zu Band I (Zahlen, Zeitabstände, Figuren-Status, Ereignisse, Namen, Orte). Zahlen-Kanon: Todesalter der Tochter = 4 Jahre 7 Monate (Kap. 46); Kap. 35 Versprecher bleibt.
{chr(10).join(teile)}

BAND II ZUSAMMENFASSUNGEN:
{s.summaries(d)}
FAKTEN:
{s.bible_txt()}

Antworte NUR mit JSON: {{"widersprueche":[{{"beschreibung":"...","kanon":"...","falsch_in":[Band-II-Kapitelnummern],"belege":"..."}}]}}
Nur belegbare Widersprüche; leere Liste ist ein gutes Ergebnis."""
    j = s.claude_json(prompt, "Band-I-Gegencheck (Bericht)")
    if j is not None:
        save_json("band1_gegencheck.json", j)
        s.mark("3:band1")
        build_report()


# ------------------------------------------------------------------ 5 Fehlerjagd-Runden (Bericht)
def jagd():
    chs = [c for c in chapters() if c[3] == "buch"]
    r = 1
    while r <= 5:
        focus = s.FOKI[(r - 1) % len(s.FOKI)]
        for n, titel, text, quelle in chs:
            key = f"5:jagd{r}:{n}"
            if s.is_done(key):
                continue
            pv, nx = neighbors(chs, n)
            prompt = f"""Du bist Korrektor/Lektor von AURORA II. SONDERFOKUS: {focus}. NUR BERICHT, es wird nichts geändert.
ENDE VORKAPITEL: ...{pv}
ANFANG FOLGEKAPITEL: {nx}...
=== {titel} ===
{text}
=== ENDE ===
Antworte AUSSCHLIESSLICH mit JSON: {{"funde":[{{"zitat":"WÖRTLICH, 8-30 Wörter, genau einmal im Kapitel","problem":"...","vorschlag":"Ersatzformulierung","art":"...","schwere":"hoch|mittel|niedrig"}}]}}
Höchstens 8 Funde, nur echte; leere Liste ist ein gutes Ergebnis."""
            j = s.claude_json(prompt, f"Jagd{r} Kap {n}")
            if j is not None:
                j["kapitel"] = n
                j["fokus"] = focus
                save_json(f"jagd{r}_kap{n}.json", j)
                s.mark(key)
        build_report()
        r += 1


# ------------------------------------------------------------------ Bericht (HTML auf Desktop)
def esc(t):
    return html.escape(str(t or ""))


def build_report():
    parts = []
    def section(title, body):
        if body:
            parts.append(f"<h2>{esc(title)}</h2>{body}")
    # Analogie
    body = ""
    for p in sorted(glob.glob(f"{OUT}/analogie_kap*.json"), key=lambda x: int(re.search(r"kap(\d+)", x).group(1))):
        j = json.load(open(p, encoding="utf-8"))
        if not j.get("funde"):
            continue
        body += f"<h3>Kapitel {j['kapitel']}{' (Entwurf)' if j.get('quelle') == 'entwurf' else ''}</h3>"
        for f in j["funde"]:
            body += (f"<div class='f'><span class='k'>{esc(f.get('klasse'))} · {esc(f.get('sicherheit'))}</span>"
                     f"<p class='z'>„{esc(f.get('zitat'))}“</p><p>{esc(f.get('problem'))}</p>"
                     f"<p class='v'>→ {esc(f.get('vorschlag'))}</p></div>")
    section("1 · Analogie-Check (Muster aus deinen Korrekturen, in anderen Kapiteln)", body)
    # Zweitleser
    body = ""
    for p in sorted(glob.glob(f"{OUT}/zweitleser_kap*.json"), key=lambda x: int(re.search(r"kap(\d+)", x).group(1))):
        j = json.load(open(p, encoding="utf-8"))
        t = j.get("tempo") or {}
        h = j.get("humor") or {}
        body += (f"<h3>Kapitel {j['kapitel']}{' (Entwurf)' if j.get('quelle') == 'entwurf' else ''}"
                 f" <small>Spannung {esc(t.get('bewertung_1_10'))}/10 · Cliffhanger {esc(t.get('cliffhanger_1_10'))}/10 · Humor {esc(h.get('pro_1000_woerter'))}/1000 Wörter</small></h3>"
                 f"<p><i>{esc(j.get('gesamt'))}</i></p>")
        for f in j.get("stolpersteine") or []:
            body += (f"<div class='f'><span class='k'>Stolperstein</span><p class='z'>„{esc(f.get('zitat'))}“</p>"
                     f"<p>{esc(f.get('problem'))}</p><p class='v'>→ {esc(f.get('vorschlag'))}</p></div>")
        for w in (t.get("zaeh_stellen") or []) + (h.get("wuesten") or []):
            body += f"<p class='w'>⏳ {esc(w)}</p>"
        for f in h.get("schwache_pointen") or []:
            body += f"<div class='f'><span class='k'>Pointe</span><p class='z'>„{esc(f.get('zitat'))}“</p><p>{esc(f.get('problem'))}</p></div>"
        for fg in j.get("figuren") or []:
            body += f"<p class='w'>👤 {esc(fg)}</p>"
        for g in (j.get("gelungen") or [])[:3]:
            body += f"<p class='g'>✅ „{esc(g.get('zitat'))}“ — {esc(g.get('warum'))}</p>"
    section("2 · Zweitleser (Verständlichkeit · Tempo · Humor)", body)
    # Band I
    p = f"{OUT}/band1_gegencheck.json"
    if os.path.exists(p):
        j = json.load(open(p, encoding="utf-8"))
        ws = j.get("widersprueche") or []
        body = "".join(f"<div class='f'><p>{esc(w.get('beschreibung'))}</p><p class='z'>Band I: {esc(w.get('kanon'))}</p>"
                       f"<p>Betrifft Kap. {esc(w.get('falsch_in'))} · {esc(w.get('belege'))}</p></div>" for w in ws) or "<p>Keine belegbaren Widersprüche gefunden. ✅</p>"
        section("3 · Anschluss an Band I", body)
    # Jagd
    body = ""
    seen = set()
    for p in sorted(glob.glob(f"{OUT}/jagd*_kap*.json"), key=lambda x: (int(re.search(r"kap(\d+)", x).group(1)), x)):
        j = json.load(open(p, encoding="utf-8"))
        fs = [f for f in (j.get("funde") or []) if (j["kapitel"], (f.get("zitat") or "")[:50]) not in seen]
        if not fs:
            continue
        body += f"<h3>Kapitel {j['kapitel']} <small>{esc(j.get('fokus'))}</small></h3>"
        for f in fs:
            seen.add((j["kapitel"], (f.get("zitat") or "")[:50]))
            body += (f"<div class='f'><span class='k'>{esc(f.get('art'))} · {esc(f.get('schwere'))}</span><p class='z'>„{esc(f.get('zitat'))}“</p>"
                     f"<p>{esc(f.get('problem'))}</p><p class='v'>→ {esc(f.get('vorschlag'))}</p></div>")
    section("5 · Fehlerjagd (wechselnder Fokus)", body)
    if os.path.exists(f"{W}/docs/AURORA_II_Lesebegleiter_sa2_{TAG}.md"):
        section("4 · Lesebegleiter / Memory-Hygiene", f"<p>Lesebegleiter: <code>workspace/docs/AURORA_II_Lesebegleiter_sa2_{TAG}.md</code> · "
                f"Memory-Bericht: <code>{esc(OUT)}/memory_hygiene_bericht.md</code></p>")
    now = dt.datetime.now().strftime("%d.%m.%Y %H:%M")
    doc = f"""<!doctype html><html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>AURORA II Lesebericht {TAG}</title><style>
body{{font:18px/1.55 Segoe UI,Arial,sans-serif;max-width:900px;margin:0 auto;padding:16px;background:#101820;color:#e6f2ef}}
h1{{color:#7fe8cf}} h2{{color:#7fe8cf;border-bottom:1px solid #2a4a50;padding-top:18px}} h3{{margin-bottom:4px}} small{{color:#8fb;font-weight:normal;font-size:15px}}
.f{{background:#18262e;border-left:4px solid #3cc9b0;padding:6px 12px;margin:10px 0;border-radius:4px}} .k{{font-size:15px;color:#9ad}}
.z{{color:#fff;font-style:italic}} .v{{color:#a6f0c6}} .w{{color:#f0d890}} .g{{color:#9be}} p{{margin:5px 0}}
</style></head><body>
<h1>AURORA II — Lesebericht</h1>
<p>Stand {now}. <b>Nichts im Buch wurde geändert.</b> Das ist eine Vormerkliste für die Lektorläufe; du entscheidest je Fund.
Zitate stammen aus dem Stand von heute. Wenn du Stellen schon selbst geändert hast, einfach überspringen.</p>
{''.join(parts) or '<p>Noch keine Ergebnisse.</p>'}
</body></html>"""
    tmp = f"{OUT}/lesebericht.html"
    open(tmp, "w", encoding="utf-8").write(doc)
    try:
        shutil.copy2(tmp, REPORT)
    except Exception as e:
        log(f"Desktop-Kopie fehlgeschlagen: {e}")


# ------------------------------------------------------------------ Lauf
def main():
    lock = open(f"{OUT}/.lock", "w")
    try:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except OSError:
        print("läuft bereits")
        return
    grund = "fertig"
    try:
        os.makedirs(f"{W}/backups", exist_ok=True)
        shutil.copy2(s.DATA, f"{W}/backups/aurora2_vor_lesebericht_{dt.datetime.now():%Y%m%d_%H%M}.json")
        q0 = s.quota() or {}
        log(f"START Lesebericht-Lauf — 5h {q0.get('five_hour_pct')} %, Woche {q0.get('seven_day_pct')} %, Deadline {s.DEADLINE}")
        jobrep("laeuft", f"gestartet {dt.datetime.now():%H:%M}, Deadline {s.DEADLINE:%H:%M}")
        if os.path.exists(s.STOP):
            os.remove(s.STOP)
        analogie()
        zweitleser()
        band1()
        s.t4_lesebegleiter()
        s.t4_memory()
        jobrep("laeuft", "Phase 1-4 fertig, Fehlerjagd-Runden")
        jagd()
    except Stop as e:
        grund = f"gestoppt: {e}"
        log(f"STOP: {e}")
    except Exception:
        import traceback
        grund = "Fehler (siehe Log)"
        log("FEHLER: " + traceback.format_exc())
    finally:
        try:
            build_report()
        except Exception as e:
            log(f"Bericht-Bau fehlgeschlagen: {e}")
        q = s.quota() or {}
        txt = (f"# Lesebericht-Lauf {TAG}\nEnde {dt.datetime.now():%H:%M} · {grund}\nLimits: 5h {q.get('five_hour_pct')} % · Woche {q.get('seven_day_pct')} %\n"
               f"Statistik: {json.dumps(s.ST['stats'], ensure_ascii=False)}\nBericht: {REPORT}\nErledigt: {', '.join(s.ST['done'])}\n")
        open(f"{OUT}/ABSCHLUSSBERICHT.md", "w", encoding="utf-8").write(txt)
        jobrep("ok" if grund == "fertig" else ("fehler" if grund.startswith("Fehler") else "ok"),
               f"{grund} · Woche {q.get('seven_day_pct')} % · Bericht: Desktop\\AURORA_II_Lesebericht_{TAG}.html")
        log("ABSCHLUSSBERICHT geschrieben")


if __name__ == "__main__":
    main()
