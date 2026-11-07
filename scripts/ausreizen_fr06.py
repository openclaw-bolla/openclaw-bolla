#!/usr/bin/env python3
"""Ausreizen Fr 06.11. 19:00 -> Sa 07.11. 22:55 (Reset Sa 22:59). Chris-Freigabe 06.11.2026.

Phase A  Straffung Kap. 1-18 (= altes 1-16, Ziel ca. -4.800 W gesamt), je Kapitel ein Opus-Lauf, Ausgabe NUR in scratch.
Phase B  Gesamt-Konsistenzpass ueber den Text MIT Straffungsentwuerfen, drei Bloecke, Ausgabe = Vorschlagslisten (keine Aenderung).
Phase C  Rechnung (ohne Tokens): neue Wortsumme, Seitenabschaetzung -> bericht.md
aurora2.json wird NICHT angefasst. Uebernahme nur mit Chris-Freigabe + Backup. Ein Prozess zur Zeit, limit_gate.
Notbremse: touch /tmp/aurora_samstag_stop   Resume ueber state.json.
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
OUT = f"{W}/scratch/ausreizen_20261106"
STR = f"{OUT}/straffung"
KON = f"{OUT}/konsistenz"
LOG = f"{W}/logs/ausreizen_fr06.log"
STATE = f"{OUT}/state.json"
STOP = "/tmp/aurora_samstag_stop"
CL = shutil.which("claude") or os.path.expanduser("~/.local/bin/claude")
START = dt.datetime(2026, 11, 6, 19, 0)
DEADLINE = dt.datetime(2026, 11, 7, 22, 55)
WEEK_STOP = float(os.environ.get("AUSREIZEN_WEEK_STOP", "98.5"))
for p in (OUT, STR, KON):
    os.makedirs(p, exist_ok=True)

# Kapitel: Ziel-Kuerzung in Woertern (Summe ~4.800). Kap. 1-8 kaum, 9-18 vorsichtig, 10 = Humor-Standard.
ZIEL = {1: 50, 2: 50, 3: 50, 4: 50, 5: 40, 6: 50, 7: 80, 8: 80,
        9: 300, 10: 300, 11: 600, 12: 500, 13: 550, 14: 700, 15: 350, 16: 100, 17: 500, 18: 400}

M = "~/.claude/projects/-home-bolla/memory"
STRAFF = """AURORA II (Roman, Chris Mandel) - STRAFFUNG von Kapitel {n}. Arbeite selbststaendig, keine Rueckfragen, aendere NICHTS in data/aurora2.json.
Ziel: Kapitel {n} um ca. {z} Woerter kuerzen (Toleranz +-30 %; lieber weniger kuerzen als Substanz verlieren). Buchziel ist ca. 510 Seiten (~128.000 W).
Vorgehen:
1) Lies {M}/feedback_aurora_ii_zielumfang_450.md, {M}/feedback_aurora_ii_humor_standard.md, {M}/feedback_blaue_markierung_vorschlaege.md, {M}/feedback_mp_satzuebernahme_nie_verlust.md,
   {W}/scratch/aurora2_kuerzung/kuerzungsplan.md (Abschnitt 0 'Spielregeln' gilt voll), {W}/scratch/aurora2_kuerzung/chris_korrekturprofil.md, {W}/scratch/aurora2_kuerzung/inventur_kap{n:02d}.md (Abschnitt geschuetzte Saetze; Hinweis: Inventur nutzt ggf. alte Nummer, Kap. 15-18 neu = alt 15/16 bzw. 16 geteilt - gleiche Kapitelinhalte anhand Titel zuordnen).
2) Lies den Kapiteltext: python3 -c "import json;print(json.load(open('{W}/data/aurora2.json'))['kapitel'][{i}]['text'])" und die Eintraege aus 'satz_markierungen' und 'lesemarken' dieses Kapitels (Titel beginnt mit 'Kapitel {n}:'). ALLE markierten Saetze (v.a. Chris' blaue Vorbild-Markierungen) und geschuetzten Saetze bleiben WOERTLICH und an ihrer Position.
3) Kuerze nur: Nacherzaehlungen bekannter Fakten, Nachdenk-Schleifen, doppelte Pointen-Erklaerungen, Kulissen, abgenutzte Formeln ('Marlie sass sehr still', 'Die Pause dauerte' max. 2x), Rechts-Exposition. Humor- und Spannungsmomente bleiben; Wendungs-relevantes nicht anfassen; Cliffhanger unveraendert. Keine neuen Fakten, keine Zahlen/Daten aendern (Band-I-Zahlen exakt!). Chris-Streichungen (Pieper, Reifenhaendler, Kollmann) bleiben gestrichen.
4) Schreibe den GESAMTEN neuen Kapiteltext (ohne Kapiteluberschrift-Aenderung, Format wie Original inkl. Szenentrenner) nach {STR}/kap{n:02d}.txt und einen kurzen Bericht {STR}/kap{n:02d}_bericht.md: Woerter alt/neu, Liste der Kuerzungen (je 1 Zeile), Bestaetigung dass alle markierten Saetze unveraendert sind (Pruefe per Python: jeder markierte Satz muss exakt im neuen Text vorkommen).
5) Antwort: max. 4 Zeilen (alt/neu Woerter, Auffaelligkeiten)."""

KONS = """AURORA II (Roman, Chris Mandel) - GESAMT-KONSISTENZPASS Block {name} (Kapitel {a}-{b}). Arbeite selbststaendig, aendere NICHTS in data/aurora2.json und nichts in {STR}.
Basis ist der Text MIT Straffungsentwuerfen: fuer Kapitel 1-18 gilt {STR}/kapNN.txt (falls vorhanden, sonst Original aus data/aurora2.json: python3 -c "import json;print(json.load(open('{W}/data/aurora2.json'))['kapitel'][i]['text'])"), fuer 19-38 das Original.
Lies zuerst {M}/feedback_aurora_zahlen_exakt.md, {W}/scratch/aurora2_kuerzung/welle7/konsistenz_notizen_32_38.md (15 Punkte, bekannte Widersprueche), das 'kanon'-Feld in data/aurora2.json und die Kap.-Zusammenfassungen. Pruefe Kapitel {a}-{b} auf: Zahlen/Daten/Uhrzeiten, Namen und Listen (z. B. Falkners Namensliste Kap. 24 vs. Kap. 34/35), Orte/Zimmer, wer weiss was wann, Passwoerter, Rollenbezeichnungen, Zeitlinie (Tag 0 = 16.10.; Theo im Haus 10.10., Todestag 12.10.), Bezuege auf Band I, Anschluss an Kapitelenden/-anfaenge, durch die Straffung entstandene Loecher (Bezuege auf gestrichene Stellen).
Ausgabe NUR als Vorschlagsliste nach {KON}/block_{name}.md: je Befund Kapitel, Fundstelle (woertliches Zitat), Problem, Gegenstelle, Vorschlag als exakte Ersetzung (alt -> neu) mit Wortzahl-Differenz; Sicherheit hoch/mittel/gering; markierte Saetze (satz_markierungen) nie veraendern. Am Ende eine Zusammenfassung 'sicher zu uebernehmen' vs. 'Chris entscheiden'.
Antwort: max. 4 Zeilen."""

TASKS = []
for n, z in ZIEL.items():
    TASKS.append((f"straffung_{n:02d}", STRAFF.format(n=n, i=n - 1, z=z, M=M, W=W, STR=STR), "opus"))
for name, a, b in (("A", 1, 13), ("B", 14, 26), ("C", 27, 38)):
    TASKS.append((f"konsistenz_{name}", KONS.format(name=name, a=a, b=b, M=M, W=W, STR=STR, KON=KON), "opus"))


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
    cap = WEEK_STOP if dt.datetime.now().hour >= 20 else float(os.environ.get("AUSREIZEN_WEEK_STOP_TAG", "90"))
    if float(q.get("seven_day_pct") or 0) >= cap:
        return f"Woche {q.get('seven_day_pct')} % >= {cap}"
    return None


def rechnung():
    d = json.load(open(f"{W}/data/aurora2.json", encoding="utf-8"))
    alt = neu = 0
    zeilen = []
    for i, c in enumerate(d["kapitel"], 1):
        a = len(c["text"].split())
        alt += a
        p = f"{STR}/kap{i:02d}.txt"
        b = len(open(p, encoding="utf-8").read().split()) if os.path.exists(p) else a
        neu += b
        if b != a:
            zeilen.append(f"| {i} | {a} | {b} | {b - a} |")
    txt = (f"# Ausreizen 06./07.11. - Rechnung\n\nGesamt alt {alt} W, mit Straffungsentwuerfen {neu} W ({neu - alt:+d}).\n"
           f"Seitenabschaetzung 11 pt (~250 W/S.): {alt / 250:.0f} -> {neu / 250:.0f} Seiten (Ziel ~510).\n\n"
           "| Kap. | alt | neu | Diff |\n|---|---|---|---|\n" + "\n".join(zeilen) + "\n")
    open(f"{OUT}/bericht.md", "w", encoding="utf-8").write(txt)
    return alt, neu


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
        w = (START - now).total_seconds()
        log(f"warte {int(w)} s bis Fr 19:00")
        time.sleep(w)
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
    alt, neu = rechnung()
    qe = limit_gate.quota() or {}
    left = [n for n, _, _ in TASKS if n not in st["done"]]
    summ = (f"Ausreizen Fr/Sa AURORA II: fertig {len(st['done'])}/{len(TASKS)}, offen {left}; "
            f"Text {alt} -> {neu} W ({neu - alt:+d}); Woche jetzt {qe.get('seven_day_pct')} %. Bericht: scratch/ausreizen_20261106/bericht.md")
    log("ENDE " + summ)
    telegram("🐾 " + summ)


if __name__ == "__main__":
    main()
