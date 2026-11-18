#!/usr/bin/env python3
"""AURORA II Plot-Umbau, Umsetzung mit OPUS (17.11.2026, Chris: "prüf die briefings und leg los").
Schreibt die neuen Kapitelfassungen NUR nach scratch/plot_umbau/neu/kapNN.md. aurora2.json wird hier NIE veraendert.
Der Einbau ins Buch (Kapitel 38/39 neu, 40 statt 38, Renummerierung) ist ein eigener Schritt nach Gegenlesen und Chris-Freigabe.
Inhalte sind spoilergesperrt: Logs/MP-Jobs enthalten nur Status. Notbremse: touch /tmp/aurora_samstag_stop
Aufruf: plot_umsetzung_opus.py [--dry] [--nur 37,38]"""
import datetime as dt, fcntl, json, os, re, sys, time

W = "/home/bolla/workspace"
OUT = f"{W}/scratch/plot_umbau/neu"
BR = f"{W}/scratch/plot_umbau/b4_briefings"
LOG = f"{W}/logs/plot_umsetzung.log"
STOP = "/tmp/aurora_samstag_stop"
MODEL = "claude-opus-5"
CL = "/home/bolla/.local/bin/claude"
M = "~/.claude/projects/-home-bolla/memory"
JSON = f"{W}/data/aurora2.json"
JOB = "plot-umsetzung"
sys.path.insert(0, f"{W}/scripts")
os.makedirs(OUT, exist_ok=True)
# Chris 17.11.2026 (10:54 ausgebremst): Opus-Kapitelschritt kostet ~40 Pp im 5h-Fenster (gemessen: 11 -> 51 %), nicht 13.
# -> NUR nachts starten (22:00-03:00; nach 03:00 wuerde ein neues Fenster bis in den Morgen reichen), Start nur bei 5h <= 55 %.
STEP_KOSTEN = 40
os.environ["LIMIT_GATE_5H"] = "55"      # 55 + 40 = 95
os.environ["LIMIT_GATE_HARD"] = "98"


def ausnahme():
    """Chris-Ausnahme von der 5h-Regel (data/limit_ausnahme.json: {"von","bis","gate","hard","grund"}), nur im Zeitraum gueltig."""
    try:
        e = json.load(open(f"{W}/data/limit_ausnahme.json"))
        if dt.datetime.fromisoformat(e["von"]) <= dt.datetime.now() <= dt.datetime.fromisoformat(e["bis"]):
            return e
    except Exception:
        pass
    return None


def nacht_fenster():
    # Start nur bis 02:00: ein dann geoeffnetes Fenster endet spaetestens 07:00 (Schule/Morgen frei)
    h = dt.datetime.now().hour
    return h >= 22 or h < 2


def regeln_setzen():
    e = ausnahme()
    os.environ["LIMIT_GATE_5H"] = str(e.get("gate", 60)) if e else "55"
    os.environ["LIMIT_GATE_HARD"] = str(e.get("hard", 99)) if e else "98"
    return e

# Reihenfolge laut b3 Abschnitt 7: Ernte (37-39), Schluss (40), Saat+Straffung 29-36 nach Ertrag, dann 19-28
ORDER = [37, 38, 39, 40, 30, 32, 35, 29, 33, 34, 31, 36, 24, 28, 19, 20, 26, 21, 22, 23, 25, 27]
ZIEL = {37: (3800, 6000), 38: (3800, 5600), 39: (3900, 5800), 40: (1300, 2200)}   # sonst: 70-110 % des alten Kapitels
BLOCKS = {40: "Schluss (37-40)", 36: "Saat + Straffung 29-36", 27: "Straffung 19-28"}


def log(m):
    open(LOG, "a").write(f"[{dt.datetime.now():%d.%m. %H:%M:%S}] {m}\n")


def melde(text, status=None):
    try:
        from job_status import mc_meldung
        mc_meldung(JOB, "✍️ AURORA II Umbau: Kapitel mit Opus", text, status)
    except Exception as e:
        log(f"Meldung fehlgeschlagen: {e!r}")


def alt_index(n):          # Index des heutigen Kapitels, das als Grundlage dient (38/39 neu: keins; 40 = altes 38)
    return None if n in (38, 39) else (37 if n == 40 else n - 1)


def norm(s):
    return re.sub(r"\s+", "", s or "")


def buch():
    return json.load(open(JSON, encoding="utf-8"))


def pflicht(n, d):
    """Texte, die wörtlich im neuen Kapitel stehen müssen: markierte Sätze, Einschübe, Schutzliste des Briefings."""
    muss = []
    i = alt_index(n)
    if i is not None:
        titel = d["kapitel"][i]["titel"]; heute = norm(d["kapitel"][i]["text"])
        muss += [("Markierung", m.get("satz") or m.get("text")) for m in d.get("satz_markierungen", []) if isinstance(m, dict) and m.get("kapitel_titel") == titel]
        muss += [("Einschub", e["text"]) for e in d.get("einschub_vorschlaege", []) if e.get("kapitel_titel") == titel and e.get("text")]
        muss = [(k, x) for k, x in muss if x and norm(x) in heute]          # nur, was im heutigen Kapitel tatsächlich steht
    b = open(f"{BR}/kap{n}.md", encoding="utf-8").read()
    m = re.search(r"##\s*\d+\.\s*Schutzliste.*?\n(.*?)(?=\n##\s|\Z)", b, re.S)
    if m:
        muss += [("Schutzliste", q) for q in re.findall(r"»([^»«]{18,}?)«", m.group(1))]
    return [(k, t) for k, t in muss if t and len(t.strip()) >= 12]


def pruefen(n, d):
    f = f"{OUT}/kap{n:02d}.md"
    if not os.path.exists(f):
        return False, "Datei fehlt", []
    t = open(f, encoding="utf-8").read()
    w = len(t.split())
    if n in ZIEL:
        lo, hi = ZIEL[n]
    else:
        alt = len(d["kapitel"][alt_index(n)]["text"].split()); lo, hi = int(alt * 0.70), int(alt * 1.10)
    fehlt = [(k, x) for k, x in pflicht(n, d) if norm(x) not in norm(t)]
    ok = lo <= w <= hi and not [x for x in fehlt if x[0] in ("Markierung", "Einschub")]
    return ok, f"{w} Wörter (Soll {lo}-{hi}), fehlende Pflichttexte: {len(fehlt)}", fehlt


def prompt(n, fehlt=None):
    i = alt_index(n)
    quelle = (f"Lies das heutige Kapitel (Grundlage für Straffung/Umbau) mit:\n  python3 -c \"import json;k=json.load(open('{JSON}'))['kapitel'][{i}];print(k['titel']);print(k['text'])\""
              if i is not None else "Dieses Kapitel ist NEU; es gibt keinen heutigen Text. Lies stattdessen den Text des Anschlusskapitels (Kap. 37 neu: s. u.).")
    vorher = [x for x in (37, 38, 39) if x < n and os.path.exists(f"{OUT}/kap{x:02d}.md")]
    anschl = ("Lies zuerst die bereits geschriebenen NEUEN Fassungen " + ", ".join(f"{OUT}/kap{x:02d}.md" for x in vorher) + " (Anschluss, Stil, Zahlen müssen passen).\n") if vorher and n >= 38 else ""
    korrektur = ""
    if fehlt:
        korrektur = ("\nKORREKTUR (2. Versuch): In deiner ersten Fassung fehlten wörtlich diese Pflichttexte bzw. die Wortzahl stimmte nicht. Überarbeite die Datei so, dass alles stimmt:\n" +
                     "\n".join(f"- [{k}] {t[:200]}" for k, t in fehlt[:25]) + "\n")
    return f"""Du bist Opus, Romanautor und Lektor für AURORA II (Roman von Chris Mandel). Arbeite selbstständig, keine Rückfragen.
AUFGABE: Schreibe die vollständige NEUE Fassung von Kapitel {n} nach {OUT}/kap{n:02d}.md. Ändere NICHTS in {JSON} und schreibe keine andere Datei.
1. Lies das Briefing {BR}/kap{n}.md vollständig (Vorgabe, Beats, Schutzliste, Humor, Zahlen und Daten sind bindend).
2. {quelle}
{anschl}3. Lies zusätzlich: {M}/feedback_aurora_ii_leicht_lesbar.md, {M}/feedback_aurora_ii_humor_standard.md, {M}/feedback_aurora_zahlen_exakt.md, {M}/feedback_kreative_individualitaet.md, {M}/feedback_aurora_ii_zwei_papiere_benennung.md und in {JSON} die Felder 'kanon', 'kriterien'. Das Feld 'geheim' ist für dich zugänglich (Spoiler, nur zur Konsistenz).
REGELN: Schutzliste wörtlich stehen lassen. Alle Sätze, die Chris markiert hat (satz_markierungen) und alle Einschübe (einschub_vorschlaege) des Kapitels bleiben wörtlich im Text, auch wenn sie gekürzt werden müssten. Keine neuen Fakten, Zahlen oder Daten gegenüber dem Briefing. Wortziel gemäß Briefing. Stil: verständlich, aber auf hohem literarischem Niveau, kein Groschenroman, nichts glätten, Humor nach Maßstab Kap. 10, Rhythmus und kurze Sätze als Pointen bleiben.
FORMAT der Datei: erste Zeile 'TITEL: Kapitel {n}: <Titel>', dann eine Leerzeile, dann der reine Kapiteltext im Format der anderen Kapitel (Kopfzeile in Kursiv, Absätze durch Leerzeile, Szenentrenner ---, Dialog mit »…«, AURORA-Zeilen fett). Kein Kommentar, keine Anmerkungen in der Datei.{korrektur}
Antwort im Chat: nur 'fertig'."""


def main():
    nur = None
    if "--nur" in sys.argv:
        nur = [int(x) for x in sys.argv[sys.argv.index("--nur") + 1].split(",")]
    if "--dry" in sys.argv:
        d = buch()
        for n in ORDER:
            print(n, len(prompt(n)), "Zeichen | Pflichttexte:", len(pflicht(n, d)), "| Soll:", ZIEL.get(n) or "70-110 %")
        return
    lock = open("/tmp/plot_umsetzung.lock", "w")
    try:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except OSError:
        return
    import limit_gate
    melde("Umsetzung der neuen Kapitelfassungen gestartet (Opus). Ergebnisse nur in scratch/plot_umbau/neu/, nichts im Buch geändert, keine Inhalte hier.", "aktion")
    for n in ORDER:
        if nur and n not in nur:
            continue
        if os.path.exists(f"{OUT}/_ok_{n}"):
            continue
        for versuch in (1, 2):
            fehlt = None
            if versuch == 2:
                fehlt = pruefen(n, buch())[2]
            for _ in range(400):                                   # Gate-/Nacht-Warten
                if os.path.exists(STOP):
                    log("Notbremse"); melde("⚠️ Notbremse gesetzt, Umsetzung gestoppt. Neustart: Datei /tmp/aurora_samstag_stop löschen, dann „plot weiter“.", "aktion"); return
                ex = regeln_setzen()
                if not ex and not nacht_fenster():
                    log("Tagsüber/Morgenschutz: kein Start (Fenster 22:00-03:00), warte 15 Min"); time.sleep(900); continue
                q = limit_gate.quota() or {}
                log(f"Kap. {n} (Versuch {versuch}){' [Chris-Ausnahme bis '+ex['bis']+']' if ex else ''}: 5h {q.get('five_hour_pct')} %, Woche {q.get('seven_day_pct')} %")
                t0 = time.time()
                r = limit_gate.run([CL, "-p", "--model", MODEL, "--allowedTools", "Read,Write,Bash,Glob,Grep"],
                                   input=prompt(n, fehlt), capture_output=True, text=True, timeout=3300, wait=False, heavy=not (ex and ex.get('woche_frei')))
                if r.returncode == 75:
                    log("Gate: nicht gestartet, warte 30 Min"); time.sleep(1800); continue
                if r.returncode != 0 and time.time() - t0 < 180 and not os.path.exists(f"{OUT}/kap{n}.md"):
                    log(f"Kap. {n}: sofortiger Abbruch rc={r.returncode} (vermutlich Session-Limit, Quota-Anzeige evtl. veraltet) - kein Fehlversuch, warte 30 Min"); time.sleep(1800); continue
                break
            q2 = limit_gate.quota() or {}
            log(f"Kap. {n}: rc={r.returncode} | nachher 5h {q2.get('five_hour_pct')} %, Woche {q2.get('seven_day_pct')} %")
            ok, info, fehlt2 = pruefen(n, buch())
            log(f"Kap. {n}: Prüfung {'OK' if ok else 'FEHLER'}: {info}")
            if ok:
                open(f"{OUT}/_ok_{n}", "w").write(f"{time.ctime()} {info}\n")
                melde(f"Kap. {n} fertig ({info}). 5h {q2.get('five_hour_pct')} %, Woche {q2.get('seven_day_pct')} %.", "ok")
                break
            if versuch == 2 or r.returncode not in (0,):
                if versuch == 2:
                    open(f"{OUT}/_pruefen_{n}", "w").write(info + "\n")
                    melde(f"⚠️ Kap. {n}: Prüfung nach 2 Versuchen nicht bestanden ({info}). Datei liegt in scratch/plot_umbau/neu/, braucht Sichtung. Lauf geht weiter.", "aktion")
        if n in BLOCKS and (not nur or n == nur[-1]):
            melde(f"Block „{BLOCKS[n]}“ abgeschlossen.", "ok")
    melde("✅ Alle geplanten Kapitelfassungen geschrieben (scratch/plot_umbau/neu/). Nächster Schritt: Gegenlesen, dann Einbau ins Buch nach deiner Freigabe.", "ok")


if __name__ == "__main__":
    main()
