#!/usr/bin/env python3
"""AURORA II Personen-/Firmen-Check Kap. 1-33 (Chris 27.11.2026). Nur pruefen -> JSON; Einbau separat.
Schlanke claude -p-Aufrufe (ohne CLAUDE.md/Tools), Opus, Figurenregister wird von Block zu Block weitergegeben."""
import json, os, re, subprocess, sys, time, urllib.request
W = "/home/bolla/workspace"
OUT = f"{W}/scratch/personencheck_20261127"
d = json.load(open(f"{W}/data/aurora2.json", encoding="utf-8"))

def quota():
    with urllib.request.urlopen("http://127.0.0.1:18790/api/claudequota", timeout=20) as r:
        return json.load(r)

blocks, cur, n = [], [], 0
for k in d["kapitel"][:33]:
    cur.append(k); n += len(k["text"])
    if n > 115000:
        blocks.append(cur); cur, n = [], 0
if cur:
    blocks.append(cur)

SYS = "Du bist ein sehr zurueckhaltender Lektor fuer deutsche Romane. Du antwortest ausschliesslich mit einem JSON-Objekt."
register = "(noch leer - Buchanfang. Band I wird NICHT als bekannt vorausgesetzt.)"
for i, bl in enumerate(blocks, 1):
    f = f"{OUT}/block{i}.json"
    if os.path.exists(f):
        register = json.load(open(f))["register"]; continue
    q = quota()
    if q["five_hour_pct"] >= 67 or q["seven_day_pct"] >= 67:
        sys.exit(f"STOP Limit: 5h {q['five_hour_pct']} Woche {q['seven_day_pct']}")
    text = "\n\n".join(f"=== {k['titel']} ===\n{k['text']}" for k in bl)
    prompt = f"""Pruefe in diesen Kapiteln von AURORA II (KI-Thriller) NUR Personen und Firmen/Organisationen: Kann ein aufmerksamer Leser folgen?
Echte Stolperstellen sind ausschliesslich: (a) Name taucht auf, ohne dass man irgendwo erfaehrt, wer/was das ist; (b) zwei Personen/Firmen oder ein unklares "er/sie" sind verwechselbar; (c) jemand kehrt nach langer Pause zurueck, ohne jeden Anker.
KEINE Stolperstelle: absichtliche Raetsel (spaetere Aufloesung moeglich), Stellen, die sich im selben Abschnitt klaeren, Nebenfiguren ohne Bedeutung, Stilfragen. Der Autor hat diese Kapitel schon gelesen: im Zweifel NICHTS melden. Hoechstens 2 Funde je Kapitel, viele Kapitel haben 0.
Eine Korrektur ist eine kurze Ergaenzung (wenige Woerter bis ein Satz) im Ton und Niveau des Buches, ohne neue Fakten zu erfinden und ohne Spaeteres vorwegzunehmen.

REGISTER der bisher eingefuehrten Personen/Firmen (aus frueheren Kapiteln):
{register}

{text}

Antworte NUR als JSON:
{{"funde":[{{"kapitel":"exakter Kapiteltitel","zitat":"woertlich und im Kapitel genau einmal vorkommende Stelle (kurz, ganzer Satz)","ersatz":"dieselbe Stelle mit der kleinen Ergaenzung, Originalwortlaut sonst unveraendert","begruendung":"1 kurzer Satz","sicherheit":"hoch|mittel"}}],
"register":"vollstaendiges, fortgeschriebenes Register: je Person/Firma eine kurze Zeile (Name - wer/was - zuletzt Kap. N)"}}"""
    t0 = time.time()
    r = subprocess.run(["/home/bolla/.local/bin/claude", "-p", "--model", "opus", "--output-format", "json", "--tools", "",
                        "--strict-mcp-config", "--setting-sources", "", "--system-prompt", SYS],
                       input=prompt, capture_output=True, text=True, timeout=1500, cwd=f"{OUT}/leer")
    res = json.loads(r.stdout)
    if res.get("is_error"):
        sys.exit("Fehler: " + str(res.get("result"))[:300])
    t = res["result"]
    j = json.loads(t[t.index("{"):t.rindex("}") + 1])
    json.dump(j, open(f, "w"), ensure_ascii=False, indent=1)
    register = j["register"]
    q = quota()
    print(f"Block {i}/{len(blocks)} ({bl[0]['titel'][:11]}..{bl[-1]['titel'][:11]}): {len(j['funde'])} Funde, {int(time.time()-t0)} s, 5h {q['five_hour_pct']} Woche {q['seven_day_pct']}", flush=True)
print("FERTIG")
