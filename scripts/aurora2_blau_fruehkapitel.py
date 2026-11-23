#!/usr/bin/env python3
"""AURORA II — blaue Verbesserungs-Vorschlaege fuer Kap. 1-8, 16, 17 (Chris 23.11.2026).

Ziel: Einstieg/Humor/Spannung/Wendungen der fruehen Kapitel auf das Niveau von Kap. 30-35 heben,
damit Leser das Buch nicht wegle gen (Fokus Kap. 1 + 2). Nur Opus (Chris: Opus bleibt). Alles BLAU im Reader:
  Eintrag in einschub_vorschlaege (status 'wartet', text=Neufassung, ersetzt=Originalstelle) + Neufassung steht schon im Kapiteltext.
  Ablehnen im Reader stellt das Original wieder her (Endpunkt einschub-entscheidung).
Sicherungen: Backup vor jedem Kapitel, Zitat muss genau 1x vorkommen, Zahlen/Daten aus dem Zitat muessen im Ersatz bleiben,
letzte 2 Absaetze (Cliffhanger) tabu, 5h-Gate ueber limit_gate (wartet bei Limit).
Aufruf: python3 aurora2_blau_fruehkapitel.py   (detached starten)
"""
import datetime as dt
import json
import os
import re
import shutil
import sys
import uuid

W = "/home/bolla/workspace"
sys.path.insert(0, f"{W}/scripts")
import limit_gate  # noqa: E402

BUCH = f"{W}/data/aurora2.json"
LOG = f"{W}/logs/aurora2_blau_fruehkapitel.log"
STUFE1 = f"{W}/scratch/fable_lektorat/stufe1"
CLAUDE = shutil.which("claude") or os.path.expanduser("~/.local/bin/claude")
ORDER = [1, 2, 3, 4, 5, 6, 7, 8, 16, 17]
MAXP = {1: 6, 2: 6}
STOP = "/tmp/aurora_blau_stop"


def log(m):
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(f"[{dt.datetime.now():%Y-%m-%d %H:%M:%S}] {m}\n")


def load():
    with open(BUCH, encoding="utf-8") as f:
        return json.load(f)


def save(d):
    tmp = BUCH + ".tmp_blau"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)
    os.replace(tmp, BUCH)


def kap(d, n):
    return next((k for k in d["kapitel"] if re.match(rf"Kapitel {n}:", k["titel"])), None)


def nums(t):
    return set(re.findall(r"\d+", t))


def prompt(d, n):
    k = kap(d, n)
    kanon = "\n".join(f"- {x}" for x in d.get("kanon", []))
    summ = "\n".join(f"Kap. {i}: {(x.get('zusammenfassung') or '')[:380]}" for i, x in enumerate(d["kapitel"], 1))
    try:
        f1 = json.load(open(f"{STUFE1}/kap{n:02d}.json", encoding="utf-8"))
        fable = json.dumps({"humor": f1.get("humor_dichte"), "schwache_szenen": f1.get("schwache_szenen"),
                            "befunde": f1.get("befunde")}, ensure_ascii=False)[:5000]
    except Exception:
        fable = "(keins)"
    vor = kap(d, n - 1)["text"][-700:] if n > 1 and kap(d, n - 1) else "(Buchanfang)"
    nach = kap(d, n + 1)["text"][:700] if kap(d, n + 1) else ""
    maxp = MAXP.get(n, 4)
    extra = ""
    if n in (1, 2):
        extra = (f"\nBESONDERS WICHTIG (Kap. {n}): Das sind die ersten Seiten. Ein Leser entscheidet hier, ob er weiterliest. "
                 "Der Einstieg muss sofort greifen: früh eine konkrete Frage/Spannung, schnell ein erstes Schmunzeln, Figuren, die man "
                 "gleich mag, und keine dichten Schachtelsatz-Blöcke oder Erklärstrecken ohne Pointe. Prüfe besonders den ersten "
                 "Absatz und die längsten Erklär- und Dialogstrecken. Bis zu " + str(maxp) + " Patches.")
    return f"""Du bist Lektor UND ein Panel aus drei Lesern (Thriller-Fan, Neuleser ohne Band I, kritische Leserin, die Figuren lieben will) für AURORA II (deutscher KI-Thriller, Ken-Follett-Stil, warmherziger Humor, kein Slapstick).
Der Autor findet: Die späten Kapitel (30-35) sind genau richtig, in Humor, Spannung UND Wendungen. Die frühen Kapitel sollen auf dieses Niveau, ohne ihre Handlung zu ändern.

AUFGABE: Schlage für {k['titel']} bis zu {maxp} gezielte Verbesserungen vor (Patches: zitat -> ersatz), die
(a) Spannung steigern (offene Fragen früher setzen, Tempo, Uhr/Frist, Unbehagen, bessere Verdichtung von Erklärstrecken),
(b) Wendungen/Überraschungen schärfen (ohne spätere Auflösungen zu verraten, ohne etwas zu ändern, was später gebraucht wird),
(c) warmherzigen, sofort verständlichen Humor einbauen (Charakter/Situation, trockene Beobachtungen, Pointe zündet beim ersten Lesen),
(d) Figuren mögen lassen.
Nur echte Verbesserungen, lieber weniger und starke. Nichts glätten: literarisches Niveau halten, aber ganze, klare Sätze; keine rätselhaften Bildsprüche.
{extra}

HARTE REGELN:
- 'zitat': WÖRTLICH aus dem Kapitel kopiert (jedes Zeichen identisch, inkl. » « ** *), kommt im Kapitel GENAU EINMAL vor, 8-45 Wörter.
- 'ersatz': ersetzt das komplette Zitat; darf den Originalsatz enthalten und um 1-6 Sätze erweitern oder ihn straffen. Markdown (**, *) wie im Original.
- Alle Zahlen, Uhrzeiten, Daten, Namen und Fakten aus dem Zitat bleiben unverändert erhalten. Plot, Reihenfolge der Ereignisse und Kanon sind tabu.
- Die letzten zwei Absätze des Kapitels (Cliffhanger) nicht anfassen.
- Kein Slapstick, keine Anspielungen auf Suizid/Gewalt/Krankheit als Pointe, Gegenspieler nie witzig auf Kosten von AURORA oder Kindern.
- Vorschläge dürfen sich nicht überlappen.

KANON (gilt buchweit, nie widersprechen):
{kanon}

ZUSAMMENFASSUNGEN ALLER KAPITEL (damit du weißt, was später kommt, nichts davon verraten oder verbauen):
{summ}

FABLE-BEFUNDE zu diesem Kapitel (von einer älteren Fassung, prüfe gegen den echten Text unten; die Kapitel wurden seitdem teils überarbeitet):
{fable}

ENDE VORKAPITEL: ...{vor}
ANFANG FOLGEKAPITEL: {nach}...

=== {k['titel']} ===
{k['text']}
=== ENDE ===

Antworte AUSSCHLIESSLICH mit einem JSON-Objekt, kein Text drumherum:
{{"bewertung": "2-3 Sätze: Stärken und Schwächen des Kapitels (Spannung, Wendung, Humor)",
  "patches": [{{"art": "einstieg|humor|spannung|wendung|figur", "zitat": "...", "ersatz": "...", "begruendung": "ein Satz"}}]}}"""


def call(p, n):
    for versuch in range(3):
        if os.path.exists(STOP):
            raise SystemExit("Notbremse")
        r = limit_gate.run([CLAUDE, "-p", "--model", "opus"], input=p, capture_output=True, text=True, timeout=900)
        if r.returncode == 0 and r.stdout.strip():
            m = re.search(r"\{.*\}", r.stdout, re.S)
            if m:
                try:
                    return json.loads(m.group(0))
                except Exception as e:
                    log(f"Kap {n}: JSON-Fehler {e} (Versuch {versuch + 1})")
        else:
            log(f"Kap {n}: claude rc={r.returncode} {r.stderr[:200]} (Versuch {versuch + 1})")
    return None


def bearbeite(n):
    d = load()
    k = kap(d, n)
    if not k:
        log(f"Kap {n}: nicht gefunden")
        return 0
    if any(e.get("art_lauf") == "blau_frueh_20261123" and e["kapitel_titel"] == k["titel"] for e in d.get("einschub_vorschlaege", [])):
        log(f"Kap {n}: schon bearbeitet, uebersprungen")
        return 0
    j = call(prompt(d, n), n)
    if not j:
        log(f"Kap {n}: kein Ergebnis")
        return 0
    log(f"Kap {n} Bewertung: {j.get('bewertung', '')}")
    d = load()  # frisch laden direkt vor dem Schreiben (Chris liest parallel)
    k = kap(d, n)
    text = k["text"]
    absaetze = text.rstrip().split("\n\n")
    tabu_ab = len(text) - len("\n\n".join(absaetze[-2:])) if len(absaetze) > 2 else len(text)
    angewandt = 0
    shutil.copy2(BUCH, f"{W}/backups/aurora2_vor_blau_kap{n}_{dt.datetime.now():%Y%m%d_%H%M%S}.json")
    for p in (j.get("patches") or [])[:MAXP.get(n, 4)]:
        z, e = (p.get("zitat") or "").strip(), (p.get("ersatz") or "").strip()
        if not z or not e or z == e:
            continue
        if text.count(z) != 1:
            log(f"Kap {n}: verworfen (Zitat Treffer={text.count(z)}): {z[:60]}")
            continue
        if text.index(z) + len(z) > tabu_ab:
            log(f"Kap {n}: verworfen (Cliffhanger-Bereich): {z[:60]}")
            continue
        if not nums(z) <= nums(e):
            log(f"Kap {n}: verworfen (Zahl/Datum faellt weg): {z[:60]}")
            continue
        if e in text:
            continue
        text = text.replace(z, e, 1)
        d.setdefault("einschub_vorschlaege", []).append({
            "id": f"ei-blau-{n}-{uuid.uuid4().hex[:6]}",
            "label": f"Spannung/Humor-Feinschliff ({p.get('art', '')})",
            "art_lauf": "blau_frueh_20261123",
            "kapitel_titel": k["titel"],
            "text": e,
            "ersetzt": z,
            "begruendung": p.get("begruendung", ""),
            "status": "wartet",
            "erstellt_am": dt.datetime.now().strftime("%Y-%m-%d %H:%M"),
        })
        angewandt += 1
    if angewandt:
        k["text"] = text
        d.setdefault("statistik", {})["woerter_gesamt"] = sum(len(x["text"].split()) for x in d["kapitel"])
        save(d)
    log(f"Kap {n}: {angewandt} blaue Vorschlaege eingebaut")
    return angewandt


def main():
    log("=== Start ===")
    gesamt = {}
    for n in ORDER:
        try:
            gesamt[n] = bearbeite(n)
        except SystemExit as e:
            log(f"Abbruch: {e}")
            break
        except Exception as e:
            log(f"Kap {n}: Fehler {e!r}")
    log(f"=== Fertig: {gesamt} ===")
    try:
        sys.path.insert(0, f"{W}/scripts")
        from job_status import report
        report("aurora_blau_frueh", "AURORA II: blaue Vorschlaege Kap. 1-8/16/17", "ok", "fertig, bereit zum Lesen im Reader: " + ", ".join(f"K{a}:{b}" for a, b in gesamt.items()))
    except Exception as e:
        log(f"job_status: {e}")


if __name__ == "__main__":
    main()
