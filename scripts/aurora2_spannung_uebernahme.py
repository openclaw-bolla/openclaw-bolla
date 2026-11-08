#!/usr/bin/env python3
"""AURORA II - Nachlauf zum Spannungs-Job (Chris-Auftrag 08.11.2026, ohne Rueckfragen):
 0 wartet, bis ausreizen_spannung.py fertig ist (state.json hat alle Tasks inkl. 'konsistenz')
 1 Pruefpunkt: greifen die Neufassungen Kap. 25-38 die 10 Saat-Einschuebe (saat.md) woertlich wieder auf?
   (ein Modelllauf; darf kap/NN.txt um einen Halbsatz ergaenzen, schreibt saat_pruefung.md)
 2 Backup aurora2.json
 3 Neufassungen Kap. 25-38 uebernehmen (OHNE Blau). Kapitel mit verlorenen Chris-Markierungen werden NICHT uebernommen.
 4 Saat-Einschuebe als BLAUE Vorschlaege (einschub_vorschlaege, status 'wartet') in Kap. 1-24
 5 Status an Mission Control (job_status)
Notbremse: touch /tmp/aurora_spannung_stop   Resume: state_uebernahme.json
"""
import datetime as dt
import json
import os
import re
import shutil
import sys
import time
import uuid

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import limit_gate  # noqa: E402

W = "/home/bolla/workspace"
OUT = f"{W}/scratch/spannung_20261107"
KAP = f"{OUT}/kap"
JSON = f"{W}/data/aurora2.json"
LOG = f"{W}/logs/aurora2_spannung_uebernahme.log"
ST = f"{OUT}/state_uebernahme.json"
STOP = "/tmp/aurora_spannung_stop"
CL = shutil.which("claude") or os.path.expanduser("~/.local/bin/claude")
M = "~/.claude/projects/-home-bolla/memory"


def log(msg):
    line = f"[{dt.datetime.now().strftime('%d.%m. %H:%M:%S')}] {msg}"
    print(line, flush=True)
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(line + "\n")


def status(st, detail):
    try:
        from job_status import report
        report("aurora2-spannung-einbau", "AURORA II Neufassung einbauen (Kap. 25-38 + Saat blau)", st, detail)
    except Exception as e:
        log(f"job_status fehlgeschlagen: {e}")


def st_load():
    try:
        return json.load(open(ST, encoding="utf-8"))
    except Exception:
        return {"done": []}


def st_save(s):
    json.dump(s, open(ST, "w", encoding="utf-8"))


def spannung_fertig():
    try:
        done = json.load(open(f"{OUT}/state.json", encoding="utf-8"))["done"]
    except Exception:
        return False
    need = ["konzept", "konsistenz"] + [f"kap_{n}" for n in range(25, 39)]
    return all(x in done for x in need)


def load():
    return json.load(open(JSON, encoding="utf-8"))


def save(d):
    tmp = JSON + ".tmp"
    json.dump(d, open(tmp, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    os.replace(tmp, JSON)


def norm(t):
    t = re.sub(r"[*»«\"“”„]", "", t or "")
    return re.sub(r"\s+", " ", t).strip()


def kap_nr(titel):
    m = re.match(r"Kapitel (\d+)", titel or "")
    return int(m.group(1)) if m else None


def pruefpunkt():
    prompt = f"""AURORA II (Roman von Chris Mandel). Arbeite selbststaendig, keine Rueckfragen, aendere NICHTS in {JSON}.
Lies {OUT}/saat.md (10 Saat-Einschuebe fuer Kap. 1-24; jede Ueberschrift nennt das Ziel-Kapitel/die Wendung, z.B. 'BW1 Kap. 33', 'Gefahr 3, Kap. 31') und {OUT}/konzept.md (Wendungsplan, wo die Saat aufgeht) sowie die neuen Kapitel {KAP}/25.txt bis 38.txt.
AUFGABE (Pruefpunkt): Pruefe fuer JEDE Saat S1-S10, ob das Kapitel, in dem sie aufgeht, sie WOERTLICH bzw. erkennbar wieder aufgreift (gleiches Stichwort/Bild, z.B. 'der Daumen', 'die Lunge'), sodass ein normaler Leser 'ach ja, der' denkt. Wenn nicht: ergaenze in der betreffenden {KAP}/NN.txt einen kurzen Halbsatz (max. 15 Woerter) an passender Stelle, im Ton des Kapitels, ohne etwas anderes zu aendern; vorher Kopie nach {KAP}/NN.txt.vor_saat. Beachte: Einschuebe in Kap. 1-24 sind noch nicht eingebaut, aber werden woertlich wie in saat.md eingebaut.
Schreibe {OUT}/saat_pruefung.md: je Saat eine Zeile 'S# -> Kap. N: greift auf / ergaenzt (Halbsatz: ...) / Problem: ...'. Vermerke auch Saat-Probleme, die du nicht loesen kannst (z.B. Widerspruch zum neuen Kanon). Letzte Zeile deiner Antwort: eine Zeile Zusammenfassung."""
    r = limit_gate.run([CL, "-p", "--model", "sonnet", "--allowedTools", "Read,Write,Edit,Glob,Grep"],
                       input=prompt, capture_output=True, text=True, timeout=3600)
    log(f"Pruefpunkt rc={r.returncode} {(r.stdout or '')[-300:].strip()!r}")
    return r.returncode == 0


def parse_saat():
    txt = open(f"{OUT}/saat.md", encoding="utf-8").read()
    out = []
    for blk in re.split(r"\n(?=## S\d+ ·)", txt):
        m = re.match(r"## (S\d+) · Kap\. (\d+)", blk)
        if not m:
            continue
        a = re.search(r"\*\*Anker:\*\*\s*(.+)", blk)
        n = re.search(r"\*\*Neu:\*\*\s*(.+)", blk)
        if a and n:
            out.append({"id": m.group(1), "kap": int(m.group(2)), "anker": a.group(1).strip(), "neu": n.group(1).strip()})
    return out


def find_anker(text, anker):
    cands = [anker, anker.strip("*").strip(), re.sub(r"\*\*", "", anker)]
    for c in cands:
        if c and text.count(c) == 1:
            return c
    return None


def uebernehmen():
    d = load()
    kapmap = {kap_nr(k["titel"]): k for k in d["kapitel"]}
    erg = []
    for n in range(25, 39):
        p = f"{KAP}/{n}.txt"
        k = kapmap[n]
        neu = open(p, encoding="utf-8").read().strip()
        if len(neu.split()) < 0.6 * len(k["text"].split()):
            erg.append(f"Kap. {n}: NICHT uebernommen (Entwurf zu kurz)")
            continue
        fehlt = []
        for e in d.get("satz_markierungen", []):
            if e.get("kapitel_titel") == k["titel"] and e.get("status") == "uebernommen":
                s = (e.get("neu") or e.get("satz") or "").strip()
                if s and norm(s) in norm(k["text"]) and norm(s) not in norm(neu):
                    fehlt.append(s[:70])
        lm = d.get("lesemarken", {}).get(k["titel"])
        if lm and lm.get("satz") and norm(lm["satz"])[:40] in norm(k["text"]) and norm(lm["satz"])[:40] not in norm(neu):
            fehlt.append("Lesemarke: " + lm["satz"][:50])
        if fehlt:
            erg.append(f"Kap. {n}: NICHT uebernommen (Chris-Markierungen fehlen im Entwurf: {fehlt[:2]})")
            continue
        k["text"] = neu
        erg.append(f"Kap. {n}: uebernommen ({len(neu.split())} W)")
    d["statistik"]["woerter_gesamt"] = sum(len(x["text"].split()) for x in d["kapitel"])
    save(d)
    return erg


def saat_blau():
    d = load()
    kapmap = {kap_nr(k["titel"]): k for k in d["kapitel"]}
    erg = []
    for s in parse_saat():
        k = kapmap.get(s["kap"])
        if not k:
            erg.append(f"{s['id']}: Kapitel fehlt")
            continue
        if any(e.get("saat") == s["id"] for e in d.get("einschub_vorschlaege", [])):
            erg.append(f"{s['id']}: schon eingebaut")
            continue
        text = k["text"]
        ank = find_anker(text, s["anker"])
        if not ank or s["neu"] in text:
            erg.append(f"{s['id']}: Anker nicht eindeutig (Kap. {s['kap']}) - NICHT eingebaut")
            continue
        idx = text.index(ank) + len(ank)
        end = text.find("\n\n", idx)
        if end == -1:
            end = len(text)
        absatzende = text[idx:end].strip() == ""
        neu = s["neu"]
        if absatzende and not neu.startswith(("»", "**")):
            k["text"] = text[:idx] + " " + neu + text[idx:]
        else:
            k["text"] = text[:end] + "\n\n" + neu + text[end:]
        d.setdefault("einschub_vorschlaege", []).append({
            "id": f"ei-saat-{s['kap']}-{uuid.uuid4().hex[:6]}",
            "saat": s["id"],
            "label": "Saat (bereitet spaetere Wendung vor)",
            "kapitel_titel": k["titel"],
            "text": neu,
            "begruendung": "Kleiner Einschub, der eine spaetere Wendung fair vorbereitet; wirkt hier beilaeufig.",
            "status": "wartet",
            "erstellt_am": dt.datetime.now().strftime("%Y-%m-%d %H:%M"),
        })
        erg.append(f"{s['id']}: Kap. {s['kap']} blau eingebaut")
    d["statistik"]["woerter_gesamt"] = sum(len(x["text"].split()) for x in d["kapitel"])
    save(d)
    return erg


def main():
    s = st_load()
    status("laeuft", "wartet auf Spannungs-Job")
    while not spannung_fertig():
        if os.path.exists(STOP):
            log("Notbremse")
            return
        time.sleep(60)
    log("Spannungs-Job fertig -> Nachlauf")
    status("laeuft", "Pruefpunkt Saat")
    if "pruefpunkt" not in s["done"]:
        if not pruefpunkt():
            status("aktion", "Pruefpunkt fehlgeschlagen - Einbau NICHT gestartet")
            return
        s["done"].append("pruefpunkt")
        st_save(s)
    if "einbau" not in s["done"]:
        ts = dt.datetime.now().strftime("%Y%m%d_%H%M")
        shutil.copy(JSON, f"{W}/backups/aurora2_vor_spannung_einbau_{ts}.json")
        log(f"Backup backups/aurora2_vor_spannung_einbau_{ts}.json")
        e1 = uebernehmen()
        e2 = saat_blau()
        for z in e1 + e2:
            log("  " + z)
        open(f"{OUT}/einbau_protokoll.md", "w", encoding="utf-8").write("# Einbau\n\n" + "\n".join("- " + z for z in e1 + e2) + "\n")
        s["done"].append("einbau")
        st_save(s)
        probleme = [z for z in e1 + e2 if "NICHT" in z]
        if probleme:
            status("aktion", f"Eingebaut, aber {len(probleme)} Punkte offen: " + " | ".join(probleme)[:300])
        else:
            status("ok", "Kap. 25-38 neu uebernommen, 10 Saat-Einschuebe blau in Kap. 1-24 - bereit zum Lesen")
    log("ENDE")


if __name__ == "__main__":
    main()
