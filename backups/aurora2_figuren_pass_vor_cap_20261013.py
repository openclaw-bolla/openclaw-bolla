#!/usr/bin/env python3
"""AURORA II — Figuren-Pass (Chris-Freigabe 11.10.2026, Ferienwoche).

Ziel: Leser sollen mit ALLEN Figuren mitleiden / sich mitfreuen (Renis Kritik an Band I: Marlie/Leni schwer zu mögen),
dazu Spannung + Humor. Nur Opus, nie Fable. Detachter Prozess, Notbremse: touch /tmp/aurora_samstag_stop

Runden (Reihenfolge = Chris liest gerade Kap. 12, deshalb 13-24 zuerst):
  R1  Figuren-Pass je Kapitel: Kap. 13-24 -> Patches DIREKT im Text (Chris kennt sie noch nicht, keine Markierung);
      Kap. 1-12 -> max. 3 Einschuebe je Kapitel als blau markierte Vorschlaege (status 'wartet'; nichts tun = bleibt drin)
  R2  Spannung/Humor/Cliffhanger-Feinschliff Kap. 13-24
  R3  Kontinuitaets-Check nach Ueberarbeitung Kap. 1-24 (nur Fehler/Zahlen/Daten)
  R4  Re-Panel (nur messen) -> Vorher/Nachher im Kurzbericht
Pacing: Wochen-% darf je Tag eine Obergrenze nicht ueberschreiten (Ziel: Sa 17.10. noch ~40 % uebrig); 5h-Fenster <= 92 %.
Aenderungen nur mit Backup + Protokoll (changes.md). Plot/Zahlen/Daten/Cliffhanger-Enden tabu.
"""
import datetime as dt
import fcntl
import html
import json
import os
import shutil
import sys
import time
import uuid

W = "/home/bolla/workspace"
sys.path.insert(0, f"{W}/scripts")
os.environ["SAMSTAG_TAG"] = "figurenpass_20261011"
import samstag_ausreizen as s  # noqa: E402

try:
    import job_status
except Exception:
    job_status = None

OUT = s.OUT
log = s.log
Stop = s.Stop
DESKTOP = "/mnt/d/OneDrive/Desktop"
REPORT = f"{DESKTOP}/AURORA_II_Figuren_Pass.html"
JOB = "aurora2_figuren_pass"
s.DEADLINE = dt.datetime(2026, 10, 16, 23, 50)
s.CHANGES = f"{OUT}/changes.md"

# kumulative Wochen-% Obergrenze je Tag (Ende des Tages). Chris will Sa 17.10. noch ~40 % uebrig haben.
CAPS = {"2026-10-11": 16, "2026-10-12": 25, "2026-10-13": 34, "2026-10-14": 43, "2026-10-15": 51, "2026-10-16": 58}


def jobrep(status, detail=""):
    if job_status:
        try:
            job_status.report(JOB, "AURORA II: Figuren-Pass", status, detail)
        except Exception as e:
            log(f"job_status: {e}")


def gate():
    """Eigenes Gating: 5h <= 92 %, Wochen-% unter Tages-Cap, Deadline Fr 23:50, Stopdatei."""
    fails = 0
    while True:
        if os.path.exists(s.STOP):
            raise Stop("Stopdatei")
        now = dt.datetime.now()
        if now >= s.DEADLINE:
            raise Stop("Deadline Fr 23:50")
        q = s.quota()
        if not q:
            fails += 1
            if fails >= 5:
                return None
            time.sleep(60)
            continue
        wk, fh = q.get("seven_day_pct") or 0, q.get("five_hour_pct") or 0
        cap = CAPS.get(now.strftime("%Y-%m-%d"), 58)
        if wk >= 58:
            raise Stop(f"Wochen-Obergrenze 58 % erreicht ({wk} %)")
        if wk >= cap:
            nxt = (now + dt.timedelta(days=1)).replace(hour=0, minute=5, second=0, microsecond=0)
            sec = (nxt - now).total_seconds()
            log(f"Gate: Woche {wk} % >= Tages-Cap {cap} % — pausiere bis {nxt:%a %H:%M}")
            s.sleep_chunks(min(sec, 3600))
            continue
        if fh >= 92:
            wait = (q.get("five_hour_reset_hours") or 0) * 3600 + (q.get("five_hour_reset_minutes") or 5) * 60 + 90
            log(f"Gate: 5h {fh} % >= 92 % — pausiere {wait // 60} Min bis Reset")
            s.sleep_chunks(wait)
            continue
        return q


s.gate = gate

PRINZIP = """DAS ZIEL DIESES DURCHGANGS (Figuren-Pass):
Leser (Thriller-Enthusiasten, auch solche ohne Band I) sollen mit ALLEN Figuren mitleiden und sich mitfreuen — nicht nur ihnen
folgen. Konkrete Kritik einer Leserin an Band I: es fiel schwer, sich mit Marlie und Leni zu identifizieren und sie lieb zu gewinnen.
Handwerk dafür:
- Jede Figur zeigt in jeder ihrer Szenen mindestens eine menschliche Regung: Wunsch, Angst, Peinlichkeit, Stolz, Zärtlichkeit,
  kleine Schwäche — nicht nur Funktion (Plot vorantreiben, Information liefern).
- Kleine Freundlichkeiten/Gesten (jemandem etwas Gutes tun, das keiner sieht), kleine Siege, Anerkennung, ein Lachen füreinander.
- Mitleid: Missverstandenwerden, Müdigkeit, Verlust, stilles Aushalten, etwas, das man gern sagen würde und nicht sagt —
  gezeigt in Körpersprache/Detail, nie erklärt oder pathetisch.
- Mitfreude: gelingende Momente, die der Leser sich gewünscht hat; Zuneigung zwischen Figuren, die man ihnen ansieht.
- Humor als Zuneigung (Figuren sind WARM zueinander witzig; Pointe aus Charakter/Situation), KEIN Slapstick, kein Spott auf Kosten
  einer Figur, die wir lieben sollen.
- Marlie: ihre Macke (reflexhaftes »Ja«) ist liebenswert-menschlich zu zeigen, nicht nur ärgerlich. Leni: Witz + sichtbare
  Verletzlichkeit darunter. Noah: unbeholfen-liebevoll. Jonas: unbefangen, wird geliebt. Basti/Frauke: echte Eltern-Wärme.
- Antagonisten (Falkner, Ashworth) bleiben nachvollziehbar, werden aber nicht »lieb«; Falkner darf Angst/Müdigkeit zeigen.
UNANTASTBAR: Handlung, Plotpunkte, Zahlen, Daten, Uhrzeiten, Namen, wer-weiß-was-wann, Cliffhanger-Schlusssatz jedes Kapitels,
Erzählperspektive. Keine neuen Figuren, keine neuen Plotpunkte, keine Auflösung offener Fäden. Chris' Stimme (trocken, präzise,
warm) erhalten; so wenig ändern wie nötig, aber dort, wo es zündet, ruhig 2-6 Sätze ergänzen. Jugendfrei."""

SCH_DIREKT = """{
 "panel":{"thriller_fan":"1 Satz: Spannung/Sog dieses Kapitels","neuleser":"1 Satz: Verständlichkeit/Bindung ohne Band I","reni_typ":"1 Satz: wen mag/liebt man hier, wen nicht — und warum"},
 "figuren":{"<Name>":{"zuneigung":1,"mitleid":1,"mitfreude":1}},
 "spannung":1,"humor_pro_1000":0.0,
 "schwaechster_punkt":"ein Satz",
 "patches":[{"zitat":"...","ersatz":"...","art":"zuneigung|mitleid|mitfreude|humor|spannung","problem":"warum (kurz)"}]
}"""

SCH_EINSCHUB = """{
 "panel":{"thriller_fan":"1 Satz","neuleser":"1 Satz","reni_typ":"1 Satz"},
 "figuren":{"<Name>":{"zuneigung":1,"mitleid":1,"mitfreude":1}},
 "spannung":1,"humor_pro_1000":0.0,
 "schwaechster_punkt":"ein Satz",
 "einschuebe":[{"anker":"WÖRTLICHER, eindeutiger Satz (8-30 Wörter) — direkt nach dem Absatz, der ihn enthält, wird eingefügt","text":"neuer Absatz/neue Absätze, 2-8 Sätze, fertig formuliert im Ton des Kapitels","art":"zuneigung|mitleid|mitfreude|humor","begruendung":"1 Satz: was der Leser dadurch fühlt"}]
}"""


def context(d, n):
    prev = s.kap_by_nr(d, n - 1)
    nxt = s.kap_by_nr(d, n + 1)
    return (prev["text"][-1500:] if prev else "(kein Vorkapitel)",
            nxt["text"][:800] if nxt else "(kein Folgekapitel)")


def backup(tag):
    os.makedirs(f"{W}/backups", exist_ok=True)
    shutil.copy2(s.DATA, f"{W}/backups/aurora2_vor_figurenpass_{tag}_{dt.datetime.now():%Y%m%d_%H%M%S}.json")


def panel_log(n, j, phase):
    p = f"{OUT}/panel_{phase}.json"
    try:
        allp = json.load(open(p, encoding="utf-8"))
    except Exception:
        allp = {}
    allp[str(n)] = {k: j.get(k) for k in ("panel", "figuren", "spannung", "humor_pro_1000", "schwaechster_punkt")}
    json.dump(allp, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)


def base_prompt(d, n, k, schema, modus):
    pe, ns = context(d, n)
    return f"""Du bist ein Panel aus drei Lesern (Thriller-Enthusiast, Neuleser ohne Band I, eine kritische Leserin die Figuren lieben will)
UND zugleich der Lektor, der das Kapitel gezielt verbessert. Buch: AURORA II (deutscher KI-Thriller, Fortsetzung, Ken-Follett-Stil,
warmherziger Humor, kein Slapstick).

{PRINZIP}

FIGUREN: {s.figuren_ctx(d)}

ROTE LINIEN:
{s.rote_linien(d)}

HUMOR-MASSSTAB (Kap. 10 = Referenz): 6-9 Humor-Momente pro 1000 Wörter, aus Charakter/Situation, sofort verständlich.

ZUSAMMENFASSUNGEN ALLER KAPITEL:
{s.summaries(d)}

FAKTEN-BIBEL:
{s.bible_txt()}

ENDE VORKAPITEL: ...{pe}
ANFANG FOLGEKAPITEL: {ns}...

=== {k['titel']} ({s.wc(k['text'])} Wörter) ===
{k['text']}
=== ENDE ===

AUFGABE: {modus}
Antworte AUSSCHLIESSLICH mit einem JSON-Objekt nach diesem Schema (kein Text drumherum):
{schema}
Punktwerte 1-10, ehrlich (7 = gut, 9+ = herausragend). "figuren": nur Figuren, die im Kapitel wirklich vorkommen."""


def r1_direkt(n):
    key = f"R1:{n}"
    if s.is_done(key):
        return
    d = s.load()
    k = s.kap_by_nr(d, n)
    if not k:
        return
    modus = ("Bewerte das Kapitel und liefere bis zu 8 Patches (zitat->ersatz), die Zuneigung/Mitleid/Mitfreude, Humor oder Spannung "
             "gezielt heben. Prioritaet: Figuren, die im Kapitel flach/funktional wirken. 'zitat' WÖRTLICH und EINDEUTIG im Kapitel "
             "(genau einmal, 8-30 Wörter, Zeichen exakt kopiert), 'ersatz' ersetzt das komplette Zitat (darf den Originalsatz "
             "enthalten und um 1-6 Sätze erweitern). Nicht die letzten 3 Absätze (Cliffhanger) anfassen. Nur echte Verbesserungen.")
    j = s.claude_json(base_prompt(d, n, k, SCH_DIREKT, modus), f"R1 Kap {n}")
    if j is None:
        return
    panel_log(n, j, "vorher")
    patches = []
    for p in (j.get("patches") or []):
        p = dict(p)
        p["schwere"] = "mittel"
        patches.append(p)
    if patches:
        backup(f"k{n}")
    ok, bad = s.apply_patches(n, patches, "figurenpass", lambda p: True)
    log(f"R1 Kap {n}: {ok} Patches angewandt, {bad} abgelehnt")
    s.mark(key)


def r1_einschub(n):
    key = f"R1e:{n}"
    if s.is_done(key):
        return
    d = s.load()
    k = s.kap_by_nr(d, n)
    if not k:
        return
    modus = ("Bewerte das Kapitel und schlage HÖCHSTENS 3 Einschübe vor — nur dort, wo Zuneigung/Mitleid/Mitfreude oder Humor "
             "wirklich fehlen und ein kurzer neuer Absatz viel bewirkt. Lieber 0-2 starke als 3 mittelmäßige. Der Leser (Chris) hat dieses "
             "Kapitel bereits gelesen und für gut befunden: nichts Bestehendes ändern, nur ergänzen; Plot/Ton exakt halten.")
    j = s.claude_json(base_prompt(d, n, k, SCH_EINSCHUB, modus), f"R1e Kap {n}")
    if j is None:
        return
    panel_log(n, j, "vorher")
    d = s.load()  # frisch laden, direkt vor dem Schreiben (Chris liest/markiert parallel)
    k = s.kap_by_nr(d, n)
    text = k["text"]
    added = 0
    for e in (j.get("einschuebe") or [])[:3]:
        anker, neu = (e.get("anker") or "").strip(), (e.get("text") or "").strip()
        if not anker or not neu or text.count(anker) != 1 or neu in text:
            log(f"R1e Kap {n}: Einschub verworfen (Anker Treffer={text.count(anker) if anker else 0})")
            continue
        idx = text.index(anker)
        end = text.find("\n\n", idx)
        if end == -1:
            end = len(text)
        text = text[:end] + "\n\n" + neu + text[end:]
        d.setdefault("einschub_vorschlaege", []).append({
            "id": f"ei-fp-{n}-{uuid.uuid4().hex[:6]}",
            "label": f"Figuren-Pass: {e.get('art', 'Figur')}",
            "kapitel_titel": k["titel"],
            "text": neu,
            "begruendung": e.get("begruendung", ""),
            "status": "wartet",
            "erstellt_am": dt.datetime.now().strftime("%Y-%m-%d %H:%M"),
        })
        with open(s.CHANGES, "a", encoding="utf-8") as f:
            f.write(f"\n### Kap. {n} · Einschub (blau) · {e.get('art', '')}\nNach: {anker}\n\n{neu}\n")
        added += 1
    if added:
        backup(f"k{n}_einschub")
        k["text"] = text
        d["statistik"]["woerter_gesamt"] = sum(s.wc(x["text"]) for x in d["kapitel"])
        s.save(d)
    log(f"R1e Kap {n}: {added} Einschübe (blau) eingefügt")
    s.stat_add("einschuebe", added)
    s.mark(key)


def r2(n):
    s.review_chapter(n, mode="fp2", focus="Spannungsbogen im Kapitel, Humor-Wüsten, Cliffhanger-Sog, Tempo (nach dem Figuren-Pass: nichts "
                     "wieder glätten, was Wärme/Mitleid erzeugt)")


def r3(n):
    s.review_chapter(n, mode="fp3", focus="Kontinuität nach Überarbeitung: Zahlen, Daten, Uhrzeiten, Namen, wer-weiß-was, Zeitformen, "
                     "Bezüge zwischen eingefügten Sätzen und Umgebung; Wortwiederholungen in den neu eingefügten Stellen")


def r4(n):
    key = f"R4:{n}"
    if s.is_done(key):
        return
    d = s.load()
    k = s.kap_by_nr(d, n)
    if not k:
        return
    modus = "Nur messen: bewerte das Kapitel in seinem jetzigen Zustand. Keine Patches, keine Einschübe — 'patches' leer lassen."
    j = s.claude_json(base_prompt(d, n, k, SCH_DIREKT, modus), f"R4 Kap {n}")
    if j is None:
        return
    panel_log(n, j, "nachher")
    s.mark(key)


# ---------------------------------------------------------------- Kurzbericht (1 Seite)
def ampel(v):
    try:
        v = float(v)
    except Exception:
        return "·"
    return "🟢" if v >= 7.5 else ("🟡" if v >= 6 else "🔴")


def build_report():
    def lj(p):
        try:
            return json.load(open(p, encoding="utf-8"))
        except Exception:
            return {}
    vor, nach = lj(f"{OUT}/panel_vorher.json"), lj(f"{OUT}/panel_nachher.json")
    # Figuren aggregieren (Mittel aus zuneigung/mitleid/mitfreude, je Kapitel-Auftritt)
    def agg(pan):
        acc = {}
        for n, p in pan.items():
            for name, sc in (p.get("figuren") or {}).items():
                try:
                    v = (float(sc["zuneigung"]) + float(sc["mitleid"]) + float(sc["mitfreude"])) / 3
                except Exception:
                    continue
                acc.setdefault(name, []).append(v)
        return {k: sum(v) / len(v) for k, v in acc.items() if len(v) >= 2}
    av, an = agg(vor), agg(nach)
    rows = ""
    for name in sorted(av, key=lambda x: av[x]):
        b = an.get(name)
        rows += f"<tr><td>{html.escape(name)}</td><td>{ampel(av[name])} {av[name]:.1f}</td><td>{(ampel(b) + ' ' + format(b, '.1f')) if b else '…'}</td></tr>"
    kap = ""
    for n in sorted(vor, key=int):
        a, b = vor[n], nach.get(n, {})
        kap += (f"<tr><td>{n}</td><td>{a.get('spannung')}</td><td>{b.get('spannung', '…')}</td>"
                f"<td>{a.get('humor_pro_1000')}</td><td>{b.get('humor_pro_1000', '…')}</td></tr>")
    st = s.ST["stats"]
    q = s.quota() or {}
    page = f"""<!doctype html><meta charset="utf-8"><title>AURORA II – Figuren-Pass</title>
<style>body{{font:17px/1.5 Aptos,Segoe UI,sans-serif;max-width:760px;margin:24px auto;padding:0 16px;color:#222}}
table{{border-collapse:collapse;width:100%;margin:8px 0 20px}}td,th{{border-bottom:1px solid #ddd;padding:6px 8px;text-align:left}}h2{{margin-top:24px}}</style>
<h1>AURORA II – Figuren-Pass</h1>
<p>Stand {dt.datetime.now():%d.%m. %H:%M} · Kap. 13–24 direkt überarbeitet (kein Markieren nötig) · Kap. 1–12: {st.get('einschuebe', 0)} blaue Einschläge in MP ·
Woche {q.get('seven_day_pct')} %</p>
<h2>Figuren (Zuneigung · Mitleid · Mitfreude, Schnitt 1–10)</h2>
<table><tr><th>Figur</th><th>vorher</th><th>nachher</th></tr>{rows}</table>
<h2>Kapitel: Spannung &amp; Humor/1000 Wörter</h2>
<table><tr><th>Kap.</th><th>Spannung vorher</th><th>nachher</th><th>Humor vorher</th><th>nachher</th></tr>{kap}</table>
<p><b>Was du tun musst:</b> nichts. Blaue Stellen in Kap. 1–12 bleiben drin, wenn du nichts klickst; ❌ nur wenn eine Stelle stört.</p>"""
    open(REPORT, "w", encoding="utf-8").write(page)


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
        log(f"START Figuren-Pass — 5h {q0.get('five_hour_pct')} %, Woche {q0.get('seven_day_pct')} %, Deadline {s.DEADLINE}")
        jobrep("laeuft", f"gestartet {dt.datetime.now():%a %H:%M}")
        if os.path.exists(s.STOP):
            os.remove(s.STOP)
        for n in range(13, 25):
            r1_direkt(n)
        build_report()
        jobrep("laeuft", "R1 Kap. 13–24 fertig, jetzt Einschübe Kap. 1–12")
        for n in list(range(1, 12)) + [12]:
            r1_einschub(n)
        build_report()
        jobrep("laeuft", "R1 fertig; R2 Spannung/Humor 13–24")
        for n in range(13, 25):
            r2(n)
        jobrep("laeuft", "R2 fertig; R3 Kontinuität 13–24")
        for n in range(13, 25):
            r3(n)
        jobrep("laeuft", "R3 fertig; R4 Messung")
        for n in range(1, 25):
            r4(n)
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
        open(f"{OUT}/ABSCHLUSSBERICHT.md", "w", encoding="utf-8").write(
            f"# Figuren-Pass\nEnde {dt.datetime.now():%a %H:%M} · {grund}\nWoche {q.get('seven_day_pct')} %\n"
            f"Statistik: {json.dumps(s.ST['stats'], ensure_ascii=False)}\nErledigt: {', '.join(s.ST['done'])}\n")
        jobrep("ok" if not grund.startswith("Fehler") else "fehler", f"{grund} · Woche {q.get('seven_day_pct')} % · Bericht: Desktop\\AURORA_II_Figuren_Pass.html")


if __name__ == "__main__":
    main()
