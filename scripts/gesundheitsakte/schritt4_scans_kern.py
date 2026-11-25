#!/usr/bin/env python3
"""Schritt 4a: Kern-Scans (5) per Sonnet-Vision, startet erst nach 22:00. Nur lesend. Ergebnis: data/gesundheitsakte/scan_extraktion.jsonl"""
import json, subprocess, os, time, datetime, glob, shutil, urllib.request
D="/home/bolla/workspace/data/gesundheitsakte/"
B="/mnt/d/OneDrive/Dokumente/Allgemeines/"
SC=[("Herz","Gesundheit/Herz-Kreislauf/2026-11 Herzinfarkt (Paracelsus Henstedt-Ulzburg)/2026-11-23 Vorlaeufiger Arztbrief + Laborbefund (6 Seiten).pdf"),
("Schilddrüse","Gesundheit/Schilddruese-Endokrinologie/2022-04 Anamnese Helios ENDO.pdf"),
("Auge","Versicherungen-Verträge/Augen LAsern/Befundbericht Herr Mandel MN0015512210.pdf"),
("Sonstiges","Versicherungen-Verträge/Versicherungen/KV/Vorläufiger Entlassungsbrief Albertinen Mandel, Christoph.pdf"),
("Sonstiges","Versicherungen-Verträge/Versicherungen/Rente/Schwerbehinderten Ausweis Mandel Christoph.pdf")]
CLAUDE=os.path.expanduser("~/.local/bin/claude")
if not os.path.exists(CLAUDE): CLAUDE="claude"
def quota():
    try: return json.load(urllib.request.urlopen("http://127.0.0.1:18790/api/claudequota",timeout=10))
    except Exception: return {}
def log(m): print(datetime.datetime.now().strftime("%H:%M:%S"),m,flush=True)
now=datetime.datetime.now(); start=now.replace(hour=22,minute=0,second=0,microsecond=0)
if now<start: log(f"warte bis 22:00 ({(start-now).seconds//60} Min)"); time.sleep((start-now).total_seconds())
q=quota(); log(f"Start Quota 5h={q.get('five_hour_pct')} Woche={q.get('seven_day_pct')}")
while (quota().get("five_hour_pct") or 0)>=75: log("Gate 75 % erreicht, warte 10 Min"); time.sleep(600)
tmp="/tmp/gesund_scans"; shutil.rmtree(tmp,ignore_errors=True); os.makedirs(tmp)
out=D+"scan_extraktion.jsonl"
for i,(kat,rel) in enumerate(SC):
    p=B+rel
    pre=f"{tmp}/s{i}"
    import fitz
    try:
        doc=fitz.open(p)
        for n,pg in enumerate(doc): pg.get_pixmap(dpi=110).save(f"{pre}-{n+1:02d}.png")
    except Exception as e: log(f"Render-Fehler {e}")
    imgs=sorted(glob.glob(pre+"*.png"))
    if not imgs: log(f"FEHLER Bilder: {rel}"); continue
    prompt=("Lies diese Seitenbilder (Read-Tool) eines medizinischen Dokuments von Chris (Ernst Christoph Mandel, geb. 21.12.1955). Dateien:\n"+"\n".join(imgs)+
    "\nGib NUR ein JSON-Objekt aus: {\"person_ist_chris\":true/false/\"unklar\",\"dokumentdatum\":\"JJJJ-MM-TT\",\"einrichtung\":\"\",\"arzt\":\"\",\"diagnosen\":[],\"eingriffe\":[],\"medikamente\":[],\"kernwerte\":[],\"nachsorge_termine\":[{\"was\":\"\",\"wann\":\"\"}],\"zusammenfassung\":\"max 60 Wörter\"}. Nichts erfinden, Unlesbares leer lassen.")
    r=subprocess.run([CLAUDE,"-p",prompt,"--model","sonnet","--allowedTools","Read","--add-dir",tmp],capture_output=True,text=True,timeout=600)
    t=r.stdout.strip(); a,b=t.find("{"),t.rfind("}")
    try: res=json.loads(t[a:b+1])
    except Exception: res={"fehler":t[:300]}
    res.update({"datei":rel,"kat":kat,"seiten":len(imgs)})
    open(out,"a").write(json.dumps(res,ensure_ascii=False)+"\n"); log(f"{i+1}/5 {os.path.basename(rel)} {'ok' if 'fehler' not in res else 'FEHLER'}")
shutil.rmtree(tmp,ignore_errors=True)
q=quota(); log(f"FERTIG Quota 5h={q.get('five_hour_pct')} Woche={q.get('seven_day_pct')}")
