#!/usr/bin/env python3
"""
Schuljahr-Modul-Wächter (Cron, alle 5 Min).

Chris trägt in mp (Seite Schuljahr 26/27, Box "Module aus dem Vorjahr") bei einem
Modul einen freien Auftragstext ein und drückt 📌. Dieser Wächter erkennt neue,
noch nicht bearbeitete Aufträge (module_vorjahr[].auftrag nicht leer) und lässt sie
automatisch von headless `claude -p` (Sonnet, volle Tool-Rechte) erledigen — ohne
dass Chris extra nachfragen muss ("wann startest du das").

Nach Abschluss: Auftragsfeld wird automatisch geleert (API), Chris bekommt eine
kurze Telegram-Meldung. Kann der Agent den Auftrag nicht eindeutig zuordnen/lösen,
bleibt das Feld stehen (für Rückfrage) und Chris bekommt stattdessen die Rückfrage
per Telegram.

Idempotent + serialisiert über Exklusiv-Lock (kein Parallellauf bei Overlap).
"""
import os, json, subprocess, datetime, urllib.request, fcntl

HOME = "/home/bolla"
os.environ.setdefault("HOME", HOME)
CLAUDE = f"{HOME}/.local/bin/claude"
MODEL = "claude-sonnet-5"
WS = f"{HOME}/workspace"
API = "http://127.0.0.1:18790"
TG_CFG = f"{WS}/config/telegram_bot.json"
LOCK_FILE = f"{WS}/data/.schuljahr_modul_watcher.lock"
LOG = f"{WS}/data/schuljahr_modul_watcher.log"


def log(msg):
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line, flush=True)
    try:
        open(LOG, "a", encoding="utf-8").write(line + "\n")
    except Exception:
        pass


def tg(text):
    try:
        c = json.load(open(TG_CFG))
        urllib.request.urlopen(urllib.request.Request(
            f"https://api.telegram.org/bot{c['bot_token']}/sendMessage",
            data=json.dumps({"chat_id": c["chris_id"], "text": text,
                             "parse_mode": "Markdown", "disable_web_page_preview": True}).encode(),
            headers={"Content-Type": "application/json"}), timeout=20)
    except Exception as e:
        log(f"Telegram-Fehler: {e}")


def api_get(path):
    return json.load(urllib.request.urlopen(f"{API}{path}", timeout=10))


def api_post(path, payload):
    req = urllib.request.Request(f"{API}{path}",
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"})
    return json.load(urllib.request.urlopen(req, timeout=15))


PROMPT_TMPL = """Du bist Bolla und bearbeitest einen Auftrag, den Chris (Lehrer, EDV 7. Klassen,
Lessing-Gymnasium Norderstedt) über das Auftragsfeld zu einem PowerPoint-Modul aus dem Vorjahr
eingetragen hat. Führe den Auftrag jetzt SELBSTÄNDIG UND VOLLSTÄNDIG aus (nicht nur planen).

Modul: {titel}
Auftrag von Chris: {auftrag}

Kontext & Regeln:
- Die Unterrichts-PPTs liegen unter /mnt/d/OneDrive/Dokumente/Office/7. Klassen/ (Dateiname beginnt meist
  mit der Modulnummer, z.B. "2-The Basics - Grundbegriffe - II.pptx"). Suche dort die passende Datei.
- Bezieht sich der Auftrag auf Folieninhalt: Änderungen wenn möglich DIREKT in der PPTX umsetzen
  (z.B. mit python-pptx), KEINE zusätzliche Word-Datei anlegen — außer der Auftrag verlangt ausdrücklich
  ein separates Dokument (z.B. Ausdruck/Handout zum Verteilen).
- Bevor du eine echte Unterrichts-PPTX überschreibst: IMMER zuerst eine Backup-Kopie im selben Ordner
  anlegen (Suffix .bak_JJJJMMTT_HHMMSS).
- Achte auf Formatierung/Layout der Folie (Textboxen, Schriftgrößen) — nicht wahllos überschreiben,
  sondern sinnvoll in die bestehende Struktur einpassen.
- Bei Aufgaben-/Instruktionsfolien, die Schüler selbständig ohne mündliche Zusatzerklärung lesen sollen:
  großzügige Schriftgrade ansetzen (Chris ist 70, künstliche Linsen) — Richtwerte: Überschrift ~32pt,
  Haupttext/Schritte ~26pt, Hervorhebungs-/Wichtig-Zeile ~28pt, Kleingedrucktes ~22-24pt. Mehrere separate
  Textfelder zu einer Aussage lieber zu EINEM zusammenhängenden Textfeld zusammenfassen statt verstreut zu lassen.
- Wenn der Auftrag mehrdeutig ist, sich keiner Folie eindeutig zuordnen lässt, oder du eine wichtige
  Rückfrage hast: NICHT raten und NICHT blind umsetzen, sondern das unten im Format als RÜCKFRAGE melden.

Gib als LETZTES in deiner Antwort GENAU diese zwei Zeilen aus (sonst nichts mehr danach):
STATUS: ERLEDIGT
ZUSAMMENFASSUNG: <2-4 Sätze, was konkret gemacht wurde, für eine Telegram-Meldung an Chris>

ODER, falls Rückfrage nötig:
STATUS: RUECKFRAGE
ZUSAMMENFASSUNG: <kurze, konkrete Rückfrage an Chris>
"""


def process_modul(m):
    titel, auftrag = m.get("titel", ""), m.get("auftrag", "")
    log(f"Neuer Auftrag zu Modul '{titel}': {auftrag[:100]}")
    prompt = PROMPT_TMPL.format(titel=titel, auftrag=auftrag)
    try:
        r = subprocess.run([CLAUDE, "-p", "--model", MODEL,
                            "--dangerously-skip-permissions", prompt],
                           capture_output=True, text=True, timeout=2400, env=os.environ)
    except Exception as e:
        log(f"claude-Aufruf fehlgeschlagen: {e}")
        tg(f"⚠️ Modul-Auftrag zu *{titel}* konnte nicht gestartet werden ({e}). Bleibt im Feld stehen.")
        return
    out = (r.stdout or "").strip()
    if not out or "unavailable" in out.lower():
        log(f"Kein sauberes Ergebnis (rc={r.returncode}): {(r.stderr or '')[:200]}")
        tg(f"⚠️ Auftrag zu *{titel}* ist ohne sauberes Ergebnis durchgelaufen. Ich schau's mir an, sobald wir chatten.")
        return
    erledigt = "STATUS: ERLEDIGT" in out
    rueckfrage = "STATUS: RUECKFRAGE" in out
    summary = out
    if "ZUSAMMENFASSUNG:" in out:
        summary = out.split("ZUSAMMENFASSUNG:", 1)[1].strip()
    summary = summary.splitlines()[0][:500] if summary else "(keine Zusammenfassung)"
    if erledigt:
        try:
            api_post("/api/schuljahr2627/modul-update", {"titel": titel, "auftrag": ""})
        except Exception as e:
            log(f"Konnte Auftragsfeld nicht leeren: {e}")
        tg(f"✅ Erledigt: *{titel}*\n{summary}")
        log(f"Fertig + Feld geleert: {titel}")
    elif rueckfrage:
        tg(f"❓ Rückfrage zu *{titel}*:\n{summary}")
        log(f"Rückfrage, Feld bleibt stehen: {titel} — {summary}")
    else:
        tg(f"⚠️ Unklares Ergebnis zu *{titel}*, schau's dir bitte kurz an:\n{summary}")
        log(f"Unklares Ergebnis (kein STATUS-Marker): {titel}")


def main():
    lf = open(LOCK_FILE, "w")
    try:
        fcntl.flock(lf, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        return  # anderer Lauf noch aktiv
    try:
        data = api_get("/api/schuljahr2627")
    except Exception as e:
        log(f"schuljahr2627 nicht lesbar: {e}")
        return
    for m in data.get("module_vorjahr", []):
        if isinstance(m, dict) and (m.get("auftrag") or "").strip():
            process_modul(m)


if __name__ == "__main__":
    main()
