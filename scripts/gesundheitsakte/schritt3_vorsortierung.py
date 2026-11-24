#!/usr/bin/env python3
"""Schritt 3: Vorsortierung (Haiku, Pakete à 25, ~12 Aufrufe). Nur lesend. Ergebnis: data/gesundheitsakte/vorsortierung.jsonl"""
import json, subprocess, os, sys, time
D="/home/bolla/workspace/data/gesundheitsakte/"
CLAUDE=os.path.expanduser("~/.local/bin/claude")
if not os.path.exists(CLAUDE): CLAUDE="claude"
items=[]
for l in open(D+"files_hits.jsonl"):
    x=json.loads(l); items.append({"k":"datei","ref":x["path"],"text":x.get("text"),"self":x.get("self"),"reni":x.get("reni"),"hits":x.get("content_hits") or x.get("name_hits"),"snip":(x.get("snippet") or "")[:350]})
for l in open(D+"mail_hits.jsonl"):
    x=json.loads(l); items.append({"k":"mail","ref":x["id"],"datum":x.get("date"),"von":x.get("from"),"betreff":x.get("subject"),"snip":(x.get("preview") or "")[:300],"anh":x.get("att")})
for i,x in enumerate(items): x["n"]=i
PROMPT="""Du sortierst Fundstellen für eine Gesundheitsakte von CHRIS Mandel (Ernst Christoph, geb. 21.12.1955; Ehefrau Reni, Sohn Robin sind NICHT gemeint, außer es betrifft Chris). Für jeden Eintrag entscheide:
rel = "ja" (medizinisch relevant für Chris: Befund, Arztbrief, OP, Diagnose, Medikament, Reha, Zahn, Augen, Termin/Nachsorge), "nein" (nicht Chris, Werbung, Versicherung ohne med. Inhalt, Spam, Reni/Robin), "unklar".
kat = Herz | Haut | Auge | Zahn | Schilddrüse | Orthopädie | Reha | Medikation | Sonstiges | -
datum = Ereignisdatum JJJJ-MM-TT oder JJJJ-MM oder "" wenn nicht erkennbar (nichts raten).
notiz = max 12 Wörter.
Bei text=kein_text_scan nur nach Dateiname urteilen, rel dann "unklar" wenn Name plausibel medizinisch, sonst "nein".
Antworte NUR mit einem JSON-Array [{"n":..,"rel":..,"kat":..,"datum":..,"notiz":..}] für alle Einträge, ohne Text drumherum.

EINTRÄGE:
"""
out=D+"vorsortierung.jsonl"
done=set()
if os.path.exists(out):
    for l in open(out): done.add(json.loads(l)["n"])
B=25
for s in range(0,len(items),B):
    pk=[x for x in items[s:s+B] if x["n"] not in done]
    if not pk: continue
    for versuch in range(3):
        r=subprocess.run([CLAUDE,"-p",PROMPT+json.dumps(pk,ensure_ascii=False),"--model","haiku"],capture_output=True,text=True,timeout=300)
        t=r.stdout.strip()
        a,b=t.find("["),t.rfind("]")
        try:
            res=json.loads(t[a:b+1]); break
        except Exception:
            res=None; time.sleep(20)
    print(f"Paket {s//B+1}: {'ok' if res else 'FEHLER'}",flush=True)
    if not res: continue
    by={x["n"]:x for x in items}
    with open(out,"a") as f:
        for e in res:
            if e.get("n") in by:
                e["k"]=by[e["n"]]["k"]; e["ref"]=by[e["n"]]["ref"]; f.write(json.dumps(e,ensure_ascii=False)+"\n")
print("FERTIG",flush=True)
