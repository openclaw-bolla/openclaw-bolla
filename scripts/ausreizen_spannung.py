#!/usr/bin/env python3
"""AURORA II - Spannungs-/Wendungs-/Humor-Ueberarbeitung Kap. 25-38 (Chris-Auftrag 07.11.2026, 'massiv reingehen').

Phase 0  Konzept (Opus): Diagnose + Wendungsplan + Humorplan + Saat-Vorschlaege fuer Kap. 1-24 -> konzept.md, saat.md
Phase 1  Kap. 25-38 nacheinander neu schreiben (je Kapitel ein Opus-Lauf) -> kap/NN.txt (+ NN_bericht.md)
Phase 2  Konsistenzpass ueber neue Kap. 25-38 gegen Original 1-24 -> konsistenz.md (darf kap/NN.txt direkt korrigieren)
Phase 3  Rechnung -> bericht.md
data/aurora2.json wird NICHT angefasst. Chris liest die neue Fassung spaeter, spoilerfrei; Uebernahme nur mit seiner Freigabe + Backup.
Chris' Markierungen (satz_markierungen + lesemarken) bleiben woertlich erhalten und werden live aus aurora2.json gelesen.
Notbremse: touch /tmp/aurora_spannung_stop   Resume ueber state.json.
"""
import datetime as dt
import json
import os
import shutil
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import limit_gate  # noqa: E402

W = "/home/bolla/workspace"
OUT = f"{W}/scratch/spannung_20261107"
KAP = f"{OUT}/kap"
LOG = f"{W}/logs/ausreizen_spannung.log"
STATE = f"{OUT}/state.json"
STOP = "/tmp/aurora_spannung_stop"
CL = shutil.which("claude") or os.path.expanduser("~/.local/bin/claude")
START = dt.datetime(2026, 11, 7, 23, 5)
WEEK_STOP = float(os.environ.get("SPANNUNG_WEEK_STOP", "92"))
for p in (OUT, KAP):
    os.makedirs(p, exist_ok=True)

M = "~/.claude/projects/-home-bolla/memory"
LESEN = (f"Lies zuerst: {M}/feedback_aurora_ii_humor_standard.md, {M}/feedback_aurora_ii_zielumfang_450.md, "
         f"{M}/feedback_aurora_zahlen_exakt.md, {M}/feedback_aurora_zielgruppe_kein_spoiler.md, {M}/feedback_blaue_markierung_vorschlaege.md, "
         f"{M}/feedback_mp_satzuebernahme_nie_verlust.md, {W}/scratch/aurora2_kuerzung/chris_korrekturprofil.md, "
         f"das 'kanon'-Feld und alle 'zusammenfassung'-Felder in {W}/data/aurora2.json sowie {W}/scratch/aurora2_kuerzung/welle7/konsistenz_notizen_32_38.md.")

AUFTRAG = ("AUFTRAG VON CHRIS (Autor): Die zweite Haelfte (Kap. 25-38) soll SPANNUNG MAXIMAL, ECHTE UNGEAHNTE UEBERRASCHUNGEN/WENDUNGEN und schoenen, viel HUMOR "
           "(Niveau Kap. 10 = Humor-Standard) haben - alle drei gleich wichtig. Er will sich NICHT spoilern lassen und liest spaeter die fertige Fassung; "
           "du hast kreative Vollmacht. Diagnose aus der Durchsicht: Der Teil ist ueberwiegend reaktiv (Antrag - Gegenantrag - Beschluss); das Muster 'freundliches "
           "Angebot - Nein - neuer Anlauf' (Ashworth/Lavelle/Wessel) wiederholt sich vier-, fuenfmal und ist ab dem dritten Mal vorhersehbar; handfeste Gefahr/Zeitdruck "
           "ist selten; stark sind bisher nur zwei Wendungen (Kap. 34 'jemand hat mein foto angefasst', Kap. 37 Ashworths 'ich habe das Foto behalten' ist ein Bluff).")

FIX = ("UNVERAENDERLICHE FIXPUNKTE (Ergebnisse, nicht Wege): AURORA ist 'sie'; Zustandssicherung existiert in Rotterdam, ist eingefroren/nicht lauffaehig und wird nie "
       "zur Ersatz-AURORA; AURORA wird am Ende vom Gericht als volljaehrig/18 anerkannt, Falkner nimmt Antrag zurueck, Sicherung bleibt versiegelt unter Behoerdenaufsicht; "
       "Marlie sagt dem Ashworth-Angebot (Begleitperson, unentziehbar) Nein; Noah-Antrag 'Tisch einraeumen' + Marlies Ja nach 0,4 s; Schluss-Haken (Pruefsumme der Sicherung veraendert, "
       "Frage 'welche waerst du' / 'beide') fuehrt zu Band III. Kanon-Feld, Kalender 2026, Band-I-Zahlen (Noah 43, Marlie 37, gut drei Jahre; Aurora Santos vor 25 Jahren), "
       "Ethikrat 'gut drei Jahre', Vantage 38 % Lavelle/42 % Rheintal/20 % Kleinanleger, 'der Sommer' = Band I, Kreft-Erstkontakt 28.08. bleiben. Foto-Klarheit (Sicherung = Auslesen der Zahlen, "
       "'der Zustand ist das Laufen', Netz/Seiltaenzer, Besitz-Hebel, aufwachendes Kind) darf nicht widersprochen werden. Noahs Saalsatz Kap. 19 ist NICHT 'der schlaeft'; "
       "'ein Foto von jemandem, der schlaeft' fiel nur im Monitorraum (Kap. 5). Alle Markierungen (satz_markierungen/lesemarken zu dem Kapitel) bleiben WOERTLICH an ihrer Position.")


KONZEPT = f"""AURORA II (Roman, Chris Mandel) - KONZEPT fuer die Ueberarbeitung von Kap. 25-38. Arbeite selbststaendig, keine Rueckfragen, aendere NICHTS in data/aurora2.json.
{AUFTRAG}
{FIX}
{LESEN}
Lies dann den GESAMTEN Text von Kap. 24-38 (python3 -c "import json;[print(k['titel'],chr(10),k['text']) for k in json.load(open('{W}/data/aurora2.json'))['kapitel'][23:]]") und ueberfliege Kap. 1-23 ueber die Zusammenfassungen.
Entwirf in {OUT}/konzept.md (max. ca. 4.500 Woerter):
1) Diagnose (knapp): wo ist es vorhersehbar/reaktiv/flau? Welche Muster wiederholen sich?
2) WENDUNGSPLAN fuer jedes Kapitel 25-38: (a) Spannungsziel des Kapitels, (b) mindestens EINE echte Ueberraschung pro Kapitel, davon insgesamt mindestens 4 'Boden weg'-Wendungen (Umdeutung von etwas, das der Leser sicher zu wissen glaubte, fair vorbereitet), die aus den vorhandenen Fakten ableitbar sind, aber nicht erratbar; keine Deus-ex-machina; Figuren handeln konsequent; (c) Cliffhanger-Satz am Kapitelende, (d) Humor-Beats (konkret, figurengetreu: Leni/Jonas/Petrova/Weidenbach/Vermeer/Haverkamp, trockener Humor, Kap.-10-Niveau), (e) Gefahr/Zeitdruck/physische Stakes: mindestens 4 Szenen, in denen es handfest brenzlig wird (nicht nur juristisch), (f) das Antrag/Gegenantrag-Muster aufbrechen: Gegner variieren Taktik, mindestens einmal wendet sich ein 'Angebot' gegen den Anbieter.
3) KETTE: wie die Wendungen aufeinander aufbauen, damit sich die Spannung steigert (Spannungskurve) und trotzdem die FIXPUNKTE erreicht werden. Neue Fakten sofort in einer Liste 'KANON-NEU' (wer weiss was wann), damit die Folgekapitel konsistent bleiben.
4) SAAT: {OUT}/saat.md - max. 10 winzige Einschuebe (je max. 40 Woerter) fuer Kap. 1-24 (genauer woertlicher Ankersatz + neuer Satz), die die neuen Wendungen fair vorbereiten, ohne etwas zu verraten. Nie markierte Saetze aendern.
5) Wortbudget: jedes Kapitel +-5 % der Originalwoerter (Buchziel ~510 Seiten, nicht laenger werden!).
Antwort: max. 4 Zeilen (ohne Spoiler-Details)."""

KAPITEL = f"""AURORA II (Roman, Chris Mandel) - UEBERARBEITUNG von Kapitel {{n}} (Spannung/Wendung/Humor). Arbeite selbststaendig, keine Rueckfragen, aendere NICHTS in data/aurora2.json.
{AUFTRAG}
{FIX}
{LESEN}
Vorgehen:
1) Lies {OUT}/konzept.md (verbindlich fuer dieses Kapitel; bei Konflikt mit Fixpunkten gelten die Fixpunkte) und, soweit vorhanden, alle {KAP}/NN_bericht.md der bereits neu geschriebenen Kapitel (Abschnitt KANON-NEU gilt) sowie die letzten ca. 1.500 Woerter von {KAP}/{{p}}.txt (Anschluss!). Kap. 24 und frueher gelten im Original.
2) Lies das Original-Kapitel {{n}}: python3 -c "import json;print(json.load(open('{W}/data/aurora2.json'))['kapitel'][{{i}}]['text'])" und die Eintraege aus 'satz_markierungen' und 'lesemarken' dieses Kapitels (Titel beginnt mit 'Kapitel {{n}}:') - diese Saetze LIVE aus der Datei lesen (Chris markiert parallel weiter). ALLE bleiben woertlich und moeglichst an ihrer Position.
3) Schreibe das Kapitel NEU: Spannung hoch, mindestens die laut Konzept geplante Ueberraschung(en), Humor auf Kap.-10-Niveau, starker Cliffhanger/Schluss. Behalte, was gut ist (Pointen, Figurenstimmen, Motive wie Pinguindecke, Gummibaerchen, Socken, Nein-Zeit, Kaffeemann), schreibe schwache/reaktive Stellen um. Format wie Original (Kapitelkopf-Kursivzeile, Szenentrenner ---, AURORAs Fett-Zeilen, Anfuehrungszeichen »«). Keine Kapitelueberschrift mitschreiben. Wortzahl +-5 % des Originals.
4) Pruefe per Python: jeder markierte Satz steht exakt im neuen Text; Wortzahl im Rahmen. Behebe Verstoesse.
5) Schreibe das Ergebnis nach {KAP}/{{n}}.txt und einen Bericht {KAP}/{{n}}_bericht.md mit: KANON-NEU (alle neuen Fakten, wer weiss was), Liste der Wendungen/Humor-Beats (je 1 Zeile), Woerter alt/neu, Bestaetigung markierte Saetze.
6) Antwort: max. 3 Zeilen (nur Woerter alt/neu, ob Pruefung ok; keine Spoiler-Details)."""

KONS = f"""AURORA II - KONSISTENZPASS fuer die neu geschriebenen Kapitel 25-38. Arbeite selbststaendig, aendere NICHTS in data/aurora2.json.
{FIX}
{LESEN}
Basis: Kap. 1-24 = Original (data/aurora2.json), Kap. 25-38 = {KAP}/NN.txt (NN=25..38) plus {OUT}/konzept.md und {KAP}/NN_bericht.md (KANON-NEU).
Pruefe: Zahlen/Daten/Uhrzeiten/Wochentage (Kalender 2026), wer weiss was wann, Namen/Listen, Anschluesse der Kapitelenden/-anfaenge, Widersprueche zu Kap. 1-24 und zu den Fixpunkten, offene Faeden, Logik der Wendungen (fair vorbereitet? Figuren konsequent?), Wiederholungen von Formeln, Tonfall/Humor, ob die Foto-Klarheit stimmt. Behebe gefundene Fehler DIREKT in {KAP}/NN.txt (markierte Saetze nie aendern; Wortzahl +-5 %) und protokolliere jeden Eingriff in {OUT}/konsistenz.md (Kapitel, alt -> neu, Grund). Wo eine Wendung logisch nicht traegt, ueberarbeite die Stelle so, dass sie traegt.
Antwort: max. 3 Zeilen, keine Spoiler-Details."""

TASKS = [("konzept", KONZEPT, "opus")]
for n in range(25, 39):
    TASKS.append((f"kap_{n}", KAPITEL.format(n=n, i=n - 1, p=(n - 1)), "opus"))
TASKS.append(("konsistenz", KONS, "opus"))


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
    q = limit_gate.quota() or {}
    if float(q.get("seven_day_pct") or 0) >= WEEK_STOP:
        return f"Woche {q.get('seven_day_pct')} % >= {WEEK_STOP}"
    return None


def rechnung():
    d = json.load(open(f"{W}/data/aurora2.json", encoding="utf-8"))
    zeilen, alt, neu = [], 0, 0
    for n in range(25, 39):
        a = len(d["kapitel"][n - 1]["text"].split())
        p = f"{KAP}/{n}.txt"
        b = len(open(p, encoding="utf-8").read().split()) if os.path.exists(p) else a
        alt += a
        neu += b
        zeilen.append(f"| {n} | {a} | {b} | {b - a:+d} |")
    ges = sum(len(k["text"].split()) for k in d["kapitel"]) - alt + neu
    txt = (f"# Spannungs-Ueberarbeitung Kap. 25-38 - Rechnung\n\nKap. 25-38: alt {alt} W, neu {neu} W ({neu - alt:+d}). Buch gesamt ca. {ges} W (~{ges / 250:.0f} S. bei 11 pt).\n\n"
           "| Kap. | alt | neu | Diff |\n|---|---|---|---|\n" + "\n".join(zeilen) + "\n")
    open(f"{OUT}/bericht.md", "w", encoding="utf-8").write(txt)
    return alt, neu


def status(st, detail):
    try:
        from job_status import report
        report("aurora2-spannung", "AURORA II Spannung/Wendungen Kap. 25-38", st, detail)
    except Exception as e:
        log(f"job_status fehlgeschlagen: {e}")


def main():
    now = dt.datetime.now()
    if now < START:
        w = (START - now).total_seconds()
        log(f"warte {int(w)} s bis {START:%d.%m. %H:%M}")
        time.sleep(w)
    st = state_load()
    q0 = limit_gate.quota() or {}
    log(f"START 5h {q0.get('five_hour_pct')} %, Woche {q0.get('seven_day_pct')} %")
    status("laeuft", f"{len(st['done'])}/{len(TASKS)} fertig")
    allowed = "Read,Write,Edit,Bash,Glob,Grep"
    for name, prompt, model in TASKS:
        if name in st["done"]:
            continue
        why = stop_reason()
        if why:
            log(f"STOPP vor {name}: {why}")
            break
        log(f"-> {name} ({model})")
        try:
            r = limit_gate.run([CL, "-p", "--model", model, "--allowedTools", allowed], input=prompt,
                               capture_output=True, text=True, timeout=5400)
            ok = r.returncode == 0
            log(f"   {name}: rc={r.returncode} {(r.stdout or '')[-300:].strip()!r}")
        except Exception as e:
            ok = False
            log(f"   {name}: Fehler {e!r}")
        if ok:
            st["done"].append(name)
            json.dump(st, open(STATE, "w", encoding="utf-8"))
            status("laeuft", f"{len(st['done'])}/{len(TASKS)} fertig")
    alt, neu = rechnung()
    left = [n for n, _, _ in TASKS if n not in st["done"]]
    qe = limit_gate.quota() or {}
    summ = f"AURORA II Spannung: fertig {len(st['done'])}/{len(TASKS)}, offen {left}; Kap. 25-38 {alt} -> {neu} W; Woche {qe.get('seven_day_pct')} %"
    log("ENDE " + summ)
    status("ok" if not left else "aktion", summ + " (Bericht scratch/spannung_20261107/bericht.md)")


if __name__ == "__main__":
    main()
