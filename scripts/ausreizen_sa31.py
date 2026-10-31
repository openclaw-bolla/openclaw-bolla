#!/usr/bin/env python3
"""Samstags-Ausreizung 31.10.2026 (Chris: "am Sa. zum Limit-Ende wieder gegen 0 % landen").

Start Sa 20:00 (Alltagsreserve Mo-Fr endet 19:00), Ende spaetestens Sa 22:55 oder Woche >= WEEK_STOP.
Ein Prozess zur Zeit, jede Aufgabe = ein `claude -p` ueber limit_gate (5h-Gate/Watchdog, wartet auf Reset).
Aufgaben schreiben nur in eigene Ausgabedateien (scratch/ausreizen_20261031 bzw. Handouts/Entwurf), aendern
KEINE Produktivdaten (aurora2.json), posten/senden nichts. Resume ueber state.json. Notbremse: touch /tmp/aurora_samstag_stop
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
OUT = f"{W}/scratch/ausreizen_20261031"
LOG = f"{W}/logs/ausreizen_sa31.log"
STATE = f"{OUT}/state.json"
STOP = "/tmp/aurora_samstag_stop"
CL = shutil.which("claude") or os.path.expanduser("~/.local/bin/claude")
START = dt.datetime(2026, 10, 31, 20, 0)
DEADLINE = dt.datetime(2026, 10, 31, 22, 55)
WEEK_STOP = float(os.environ.get("AUSREIZEN_WEEK_STOP", "98.5"))
os.makedirs(OUT, exist_ok=True)

KURSTAG = """Kurstag 06 (Praktikum 7. Klassen) vorbereiten. Arbeite selbststaendig, keine Rueckfragen, NICHTS in itslearning posten, KEINEN Cron setzen.
Thema 06: Screen Recording + Video-Bearbeitung AM HANDY, plus ein YouTube-Video am PC (einbinden/hochladen/teilen sinnvoll gestalten).
Pflicht: Abschnitt Copyright/Urheberrecht (Bild/Ton/Video, YouTube, Musik, Recht am eigenen Bild, CC-Lizenzen, altersgerecht, deutsches Recht).
Max. 40 Minuten (Zeitplan im Handout/den Folien, Summe <= 40). Screen Recording muss fuer unterschiedliche Handys/OS funktionieren:
Android (Samsung/Pixel/Xiaomi u. a., Schnelleinstellungen 'Bildschirmaufnahme', Herstellervarianten) UND iPhone (Kontrollzentrum), Hinweise zu Ton/Mikro/Berechtigungen,
Fallback falls Funktion fehlt (Partner-Handy). Video-Bearbeitung mit kostenlosen Apps fuer beide OS (z. B. CapCut, YouTube Create, InShot, Google Fotos/iOS-Fotos-Schnitt); Verfuegbarkeit/Kosten/Datenschutz nur mit hoher Sicherheit behaupten, sonst allgemein formulieren.
Vorgehen: 1) Lies in ~/.claude/projects/-home-bolla/memory/ aktuell.md (Abschnitte 'Kurstag 5'), project_itslearning_automation.md, feedback_itslearning_workflow_bewaehrt.md, feedback_praktikum_nuetzliche_funktionen.md, feedback_prakt_anleitungen.md, feedback_illustrationen_entwurf_praktikum.md, feedback_ppt_folien_overflow.md, feedback_html_pdf_weasyprint.md, feedback_pptx_entwurf_workflow.md, feedback_schueler_texte_ton.md.
2) Sieh dir an, wie Kurstag 05 gebaut wurde: /mnt/d/OneDrive/Dokumente/Office/7. Klassen/Handouts/ (Entwurf/, Praktikum/, 05-Praktikum.html, PPTX/PDF 05-...) und Generatorskripte in /home/bolla/workspace/scripts. Nimm dasselbe Format/Layout/Namensschema fuer 06.
3) Erzeuge die Dateien in Handouts/Entwurf (NICHT nach Praktikum/ kopieren). 4) Mitteilungstexte analog Kurstag 5 als /home/bolla/workspace/scratch/kurstag6_mitteilungen.md.
5) Qualitaetscheck: Folien rendern und auf Overflow pruefen, Zeitplan <= 40 min. 6) Haenge an ~/.claude/projects/-home-bolla/memory/aktuell.md einen kurzen Eintrag an (Dateipfade; offen: Chris-Freigabe, Post-Skript auf Kurstag 6, Cron). Antwort: max. 8 Zeilen."""

AUR = """AURORA II (Band II, deutsch): Fehlerjagd, NUR LESEN. Lies /home/bolla/workspace/data/aurora2.json (Python/Bash nutzen), Kapitel {kaps} der aktuellen Fassung.
Zum Abgleich Band I: suche Band-I-Daten im workspace (data/, grep nach 'aurora' json) und beachte ~/.claude/projects/-home-bolla/memory/feedback_aurora_zahlen_exakt.md, feedback_aurora_ii_analogie_check.md, feedback_aurora_ii_humor_standard.md.
Suche: Widersprueche zu Band I und innerhalb Band II (Namen, Zahlen, Orte, Zeitabfolge), Analogie-/Bildfehler, Logik- und Kontinuitaetsfehler, Tippfehler, doppelte Formulierungen, schwache Sog-Satz-Enden.
Schreibe das Ergebnis als Markdown nach {out} (pro Fund: Kapitel, wortgenaue Fundstelle als Zitat, Problem, konkreter Verbesserungsvorschlag; priorisiert hoch/mittel/niedrig). AENDERE KEINE Daten, schreibe nur diese eine Datei. Antwort: 3 Zeilen."""

SOG = """AURORA II (Band II, deutsch): Kapitelende- und Humor-Check, NUR LESEN. Lies /home/bolla/workspace/data/aurora2.json (Python/Bash), Kapitel {kaps}.
Beachte ~/.claude/projects/-home-bolla/memory/feedback_aurora_ii_humor_standard.md und feedback_aurora_ii_analogie_check.md.
Bewerte pro Kapitel: Staerke des letzten Absatzes (Sog), Humor-Dichte gegenueber Kap. 10, Stellen mit Leerlauf/Wiederholung (Straffungskandidaten mit wortgenauem Zitat und Ersparnis in Woertern), Klappentext-taugliche Schluesselszenen ohne Spoiler.
Schreibe das Ergebnis als Markdown nach {out}. AENDERE KEINE Daten, schreibe nur diese Datei. Antwort: 3 Zeilen."""

TASKS = []
for name, kaps in [("sog_k01_08", "1-8"), ("sog_k09_16", "9-16"), ("sog_k17_24", "17-24"), ("sog_k25_31", "25-31")]:
    out = f"{OUT}/{name}.md"
    TASKS.append((name, SOG.format(kaps=kaps, out=out), "opus"))


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
    if dt.datetime.now() >= DEADLINE:
        return "Deadline Sa 22:55"
    q = limit_gate.quota() or {}
    if float(q.get("seven_day_pct") or 0) >= WEEK_STOP:
        return f"Woche {q.get('seven_day_pct')} % >= {WEEK_STOP}"
    return None


def telegram(text):
    try:
        import requests
        c = json.load(open(f"{W}/config/telegram_bot.json"))
        requests.post(f"https://api.telegram.org/bot{c['bot_token']}/sendMessage",
                      json={"chat_id": c["chris_id"], "text": text}, timeout=10)
    except Exception as e:
        log(f"Telegram fehlgeschlagen: {e}")


def main():
    now = dt.datetime.now()
    if now < START:
        wait = (START - now).total_seconds()
        log(f"warte {int(wait)} s bis Sa 20:00")
        time.sleep(wait)
    st = state_load()
    q0 = limit_gate.quota() or {}
    log(f"START 5h {q0.get('five_hour_pct')} %, Woche {q0.get('seven_day_pct')} %")
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
                               capture_output=True, text=True, timeout=3600)
            ok = r.returncode == 0
            log(f"   {name}: rc={r.returncode} {(r.stdout or '')[-300:].strip()!r}")
        except Exception as e:
            ok = False
            log(f"   {name}: Fehler {e!r}")
        if ok:
            st["done"].append(name)
            json.dump(st, open(STATE, "w", encoding="utf-8"))
    qe = limit_gate.quota() or {}
    left = [n for n, _, _ in TASKS if n not in st["done"]]
    summ = f"Ausreizen Fr/Sa: fertig {st['done']}, offen {left}; Woche jetzt {qe.get('seven_day_pct')} %"
    log("ENDE " + summ)
    telegram("🐾 " + summ)


if __name__ == "__main__":
    main()
