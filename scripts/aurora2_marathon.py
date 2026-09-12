#!/usr/bin/env python3
"""
AURORA II — Vollgas-Marathon-Modus (12.09.2026, Chris' Wunsch)
Schreibt am Stueck mehrere Kapitel mit Opus 5, bis das Wochenkontingent knapp
wird oder eine Obergrenze erreicht ist. Nutzt exakt dieselbe Prompt-/Schreiblogik
wie der "generiere"-Endpoint in mission_control_api.py (/api/aurora2/generiere),
nur mit waehlbarem Modell und als eigenstaendige Schleife statt Web-Button.
"""
import json, os, re, subprocess, sys, time
import urllib.request
from datetime import datetime
from pathlib import Path

WORKSPACE = "/home/bolla/workspace"
BUCH_FILE = os.path.join(WORKSPACE, "data/aurora2.json")
AKTUELL_FILE = "/home/bolla/.claude/projects/-home-bolla/memory/aktuell.md"
LOG_FILE = os.path.join(WORKSPACE, "logs/aurora2_marathon.log")
QUOTA_URL = "http://127.0.0.1:18790/api/claudequota"

MODEL = sys.argv[sys.argv.index("--model") + 1] if "--model" in sys.argv else "claude-opus-5"
MAX_KAPITEL = int(sys.argv[sys.argv.index("--max-kapitel") + 1]) if "--max-kapitel" in sys.argv else 12
STOP_WOCHE_PCT = float(sys.argv[sys.argv.index("--stop-woche-pct") + 1]) if "--stop-woche-pct" in sys.argv else 95.0

MARKER_START = "<!-- AURORA2_MARATHON_STATUS -->"
MARKER_END = "<!-- /AURORA2_MARATHON_STATUS -->"


def log(msg):
    line = f"[{datetime.now().strftime('%H:%M:%S')}] {msg}"
    print(line, flush=True)


def get_quota():
    with urllib.request.urlopen(QUOTA_URL, timeout=10) as r:
        return json.loads(r.read())


def telegram(msg):
    try:
        cfg = json.loads(Path(f"{WORKSPACE}/config/telegram_bot.json").read_text())
        import urllib.parse
        data = urllib.parse.urlencode({"chat_id": cfg["chris_id"], "text": msg, "parse_mode": "HTML"}).encode()
        urllib.request.urlopen(f"https://api.telegram.org/bot{cfg['bot_token']}/sendMessage", data=data, timeout=10)
    except Exception as ex:
        log(f"Telegram-Fehler (ignoriert): {ex}")


def update_status_block(text):
    try:
        content = Path(AKTUELL_FILE).read_text()
    except FileNotFoundError:
        content = ""
    block = f"{MARKER_START}\n{text}\n{MARKER_END}"
    if MARKER_START in content and MARKER_END in content:
        pre = content.split(MARKER_START)[0]
        post = content.split(MARKER_END)[1]
        new_content = pre + block + post
    else:
        new_content = block + "\n\n" + content
    Path(AKTUELL_FILE).write_text(new_content)


def build_prompt(buch, anweisung):
    kommentare = buch.get("kommentare", [])
    offene = [k for k in kommentare if not k.get("erledigt")]
    prots = json.dumps(buch.get("protagonisten", []), ensure_ascii=False, indent=2)
    if buch.get("antagonisten"):
        prots += "\n\nANTAGONISTEN:\n" + json.dumps(buch["antagonisten"], ensure_ascii=False, indent=2)
    if buch.get("nebenfiguren"):
        prots += "\n\nNEBENFIGUREN (konsistent halten, plastisch einsetzen):\n" + json.dumps(buch["nebenfiguren"], ensure_ascii=False, indent=2)
    krit = json.dumps(buch.get("kriterien", {}), ensure_ascii=False, indent=2)
    _st = buch.get("steuerung", {})
    _rl = _st.get("rote_linien", [])
    _eintraege = _st.get("eintraege", [])
    steuer_txt = ""
    if _rl:
        steuer_txt += "\nROTE LINIEN (unbedingt einhalten — Dinge die NICHT passieren dürfen / Vorgaben):\n" + "\n".join(f"- {x}" for x in _rl) + "\n"
    _aktive = [e for e in _eintraege if e.get("status") != "nicht_empfohlen"]
    if _aktive:
        steuer_txt += "\nSTEUERUNG & WÜNSCHE (vom Autor; wo nicht anders vermerkt, liegt das Timing bei dir — nicht alles auf einmal, dramaturgisch einsetzen):\n"
        _mark = {"in_arbeit": "[JETZT einbauen]", "umgesetzt": "[bereits umgesetzt — konsistent halten]", "geheim": "[umsetzen, dezent/unauffällig]", "vorgemerkt": "[für später vormerken]"}
        for e in _aktive:
            steuer_txt += f"- {_mark.get(e.get('status'), '')} {e.get('text', '')}\n"
    _gw = (buch.get("geheim", {}).get("wendung") or "").strip()
    geheim_txt = ""
    if _gw:
        geheim_txt = f"""
GEHEIME MASTER-WENDUNG (NUR FÜR DICH — Chris darf sie NIEMALS erfahren, auch nicht andeutungsweise):
{_gw}
Arbeite konsequent auf diese Wendung hin. Säe unauffällige Hinweise/Saatkörner, die sie später glaubwürdig und rückwirkend stimmig machen — aber so subtil, dass ein Erstleser sie nicht als Hinweis erkennt.
"""
    kap_voll = "\n\n".join([f"=== {k['titel']} ===\n{k['text']}" for k in buch.get("kapitel", [])])
    prompt = f"""Du bist Bolla, KI-Assistent von Chris Mandel, und schreibst gemeinsam die Fortsetzung des deutschen KI-Thrillers AURORA.

BUCH: {buch.get("titel", "AURORA II")} — {buch.get("untertitel", "")}

BUCHKRITERIEN (UNBEDINGT BEACHTEN):
{krit}

FIGUREN (aus Buch I übernommen bzw. neu):
{prots}

FIGURENFÜHRUNG (Ken-Follett-Prinzip): Nutze die Profile aktiv — zeige aussehen, detail, macke, wunde und stimme in Handlung und Dialog, statt sie nur zu kennen. Jede Figur soll ein klares, authentisches, interessantes Bild ergeben und konsistent zu ihrem Profil sprechen und handeln.
{steuer_txt}{geheim_txt}
BISHERIGE KAPITEL VON BUCH II (vollständig):
{kap_voll if kap_voll else "Noch keine Kapitel — fange frisch an, als direkte Fortsetzung von Buch I."}

ANWEISUNG VON CHRIS:
{anweisung}

Antworte AUSSCHLIESSLICH in genau diesem Format mit den Trennmarken (kein JSON, kein Markdown). Lass Felder leer wenn nicht zutreffend:

###ANTWORT###
(Kurze Rückmeldung, 1-3 Sätze)
###TITEL_ABSCHNITT###
(Titel des neuen Kapitels, z.B. "Kapitel 1: ...")
###INHALT###
(Der vollständige generierte Text — frei schreiben, Anführungszeichen, Absätze erlaubt.)
###BUCHTITEL_NEU###
(Nur wenn Buchtitel geändert werden soll, sonst leer)
###NAECHSTER_SCHRITT###
(Was als nächstes sinnvoll wäre)
###ENDE###"""
    return prompt


def extract(raw, tag_start, tag_end):
    mm = re.search(re.escape(tag_start) + r"(.*?)" + re.escape(tag_end), raw, re.DOTALL)
    return mm.group(1).strip() if mm else ""


def schreibe_kapitel():
    with open(BUCH_FILE) as f:
        buch = json.load(f)
    anweisung = "Schreibe das nächste Kapitel."
    prompt = build_prompt(buch, anweisung)
    cl = "/home/bolla/.local/bin/claude"
    r = subprocess.run(
        [cl, "-p", "--output-format", "json", "--model", MODEL],
        input=prompt, capture_output=True, text=True, timeout=1800,
        cwd=os.path.expanduser("~"),
    )
    if r.returncode != 0:
        raise RuntimeError(f"claude-Fehler: {r.stderr[:300]}")
    raw = json.loads(r.stdout).get("result", "")
    gen = {
        "antwort_text": extract(raw, "###ANTWORT###", "###TITEL_ABSCHNITT###"),
        "neuer_inhalt_titel": extract(raw, "###TITEL_ABSCHNITT###", "###INHALT###"),
        "neuer_inhalt": extract(raw, "###INHALT###", "###BUCHTITEL_NEU###"),
        "titel_update": extract(raw, "###BUCHTITEL_NEU###", "###NAECHSTER_SCHRITT###"),
        "naechster_schritt": extract(raw, "###NAECHSTER_SCHRITT###", "###ENDE###"),
    }
    if not gen["neuer_inhalt"] or not gen["neuer_inhalt_titel"]:
        raise RuntimeError(f"Kein Kapitel im Output erkannt. Antwort-Anfang: {raw[:300]}")

    with open(BUCH_FILE) as f:
        buch2 = json.load(f)
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    if gen.get("titel_update"):
        buch2["titel"] = gen["titel_update"]
    neuer_titel = gen["neuer_inhalt_titel"]
    existing_idx = next((i for i, k in enumerate(buch2.get("kapitel", [])) if k["titel"] == neuer_titel), None)
    kap_eintrag = {"titel": neuer_titel, "text": gen["neuer_inhalt"], "datum": now, "modell": MODEL}
    if existing_idx is not None:
        buch2["kapitel"][existing_idx] = kap_eintrag
    else:
        buch2.setdefault("kapitel", []).append(kap_eintrag)
    buch2.setdefault("statistik", {})["kapitel_gesamt"] = len(buch2["kapitel"])
    buch2["statistik"]["woerter_gesamt"] = sum(len(k["text"].split()) for k in buch2["kapitel"])
    buch2["statistik"]["letzte_session"] = now
    buch2["letzteAktion"] = now
    if gen.get("naechster_schritt"):
        buch2["naechsterSchritt"] = gen["naechster_schritt"]
    with open(BUCH_FILE, "w") as f:
        json.dump(buch2, f, ensure_ascii=False, indent=2)
    return neuer_titel, len(gen["neuer_inhalt"].split()), gen.get("antwort_text", "")


def main():
    log(f"=== Marathon-Start: Modell={MODEL}, max_kapitel={MAX_KAPITEL}, stop_woche_pct={STOP_WOCHE_PCT} ===")
    geschrieben = []
    fehler_in_folge = 0
    grund = ""
    for i in range(1, MAX_KAPITEL + 1):
        try:
            q = get_quota()
        except Exception as ex:
            log(f"Quota-Check fehlgeschlagen ({ex}) — breche sicherheitshalber ab.")
            grund = f"Quota-API nicht erreichbar: {ex}"
            break
        woche_pct = q.get("seven_day_pct", 0)
        fuenf_h_pct = q.get("five_hour_pct", 0)
        log(f"Vor Kapitel {i}: Woche {woche_pct}% verbraucht, 5h {fuenf_h_pct}% verbraucht.")
        if woche_pct >= STOP_WOCHE_PCT:
            grund = f"Wochenkontingent bei {woche_pct}% (Ziel-Stopp {STOP_WOCHE_PCT}%) erreicht."
            log(grund)
            break
        update_status_block(
            f"### 🔄 AURORA II Marathon läuft (seit {datetime.now().strftime('%H:%M')})\n"
            f"Kapitel bisher in diesem Lauf: {len(geschrieben)} — gerade dabei: Kapitel {i}.\n"
            f"Woche: {woche_pct}% verbraucht · 5h-Fenster: {fuenf_h_pct}% verbraucht.\n"
        )
        try:
            titel, worte, antwort = schreibe_kapitel()
            geschrieben.append((titel, worte))
            fehler_in_folge = 0
            log(f"✅ {titel} fertig ({worte} Wörter). Antwort: {antwort[:200]}")
        except Exception as ex:
            fehler_in_folge += 1
            log(f"❌ Fehler bei Kapitel {i}: {ex}")
            if fehler_in_folge >= 2:
                grund = f"2 Fehler in Folge, breche ab. Letzter Fehler: {ex}"
                break
            time.sleep(10)
    else:
        grund = f"Obergrenze {MAX_KAPITEL} Kapitel erreicht."

    try:
        q = get_quota()
        woche_pct = q.get("seven_day_pct", "?")
        fuenf_h_pct = q.get("five_hour_pct", "?")
    except Exception:
        woche_pct = fuenf_h_pct = "?"

    zusammenfassung = "\n".join(f"- {t} ({w} Wörter)" for t, w in geschrieben) or "(keine)"
    status_text = (
        f"### ✅ AURORA II Marathon beendet ({datetime.now().strftime('%d.%m.%Y %H:%M')})\n"
        f"**Grund für Stopp:** {grund}\n\n"
        f"**Neue Kapitel in diesem Lauf ({len(geschrieben)}):**\n{zusammenfassung}\n\n"
        f"**Budget danach:** Woche {woche_pct}% verbraucht · 5h-Fenster {fuenf_h_pct}% verbraucht.\n"
    )
    update_status_block(status_text)
    log("=== Marathon-Ende ===\n" + status_text)
    telegram(
        f"🌙 <b>AURORA II Marathon fertig</b>\n"
        f"{len(geschrieben)} neue Kapitel geschrieben mit {MODEL}.\n"
        f"Grund für Stopp: {grund}\n"
        f"Budget: Woche {woche_pct}% verbraucht, 5h {fuenf_h_pct}%."
    )


if __name__ == "__main__":
    main()
