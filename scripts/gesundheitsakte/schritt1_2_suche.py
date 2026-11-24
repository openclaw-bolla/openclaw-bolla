#!/usr/bin/env python3
"""Gesundheitsakte Chris — Schritt 1+2: lokale Suche, KEINE Claude-Tokens.
1) OneDrive-Dateien (Name + Textinhalt pdf/docx/txt) -> files_hits.jsonl
2) Outlook-Mails (Graph $search, nur Betreff/Absender/Datum/Vorschau) -> mail_hits.jsonl
Nur lesend. Ergebnisse privat (chmod 700) unter workspace/data/gesundheitsakte/."""
import sys, os, re, json, time, zipfile, urllib.request, urllib.parse
sys.path.insert(0, "/home/bolla/workspace/scripts")
from job_status import report
OUT = "/home/bolla/workspace/data/gesundheitsakte/"
JOB = "gesundheitsakte"
KW = ["arztbrief","befund","diagnose","krankenhaus","klinik","operation","entlassung","gallenblase","gallenstein","darmspiegelung","koloskopie","magenspiegelung","gastroskopie","pneumothorax","herzkatheter","stent","kardiolog","schilddrüse","schilddruese","hypothyreose","rechtsschenkelblock","rezept","überweisung","ueberweisung","röntgen","mrt","ct-","ultraschall","sonograph","labor","impfung","impfpass","zahnarzt","zahnersatz","augenarzt","augen lasern","lasik","hautarzt","orthopäd","physiotherapie","reha","krankschreibung","arbeitsunfähig","bänderriss","baenderriss","patient","anamnese","medikament","hausarzt","facharzt","blutdruck","cholesterin","ekg"]
SELF = re.compile(r"(christoph|ernst)\s+mandel|mandel,?\s+(ernst\s+)?christoph|21\.12\.1955", re.I)
RENI = re.compile(r"renate\s+mandel|mandel,?\s+renate|24\.10\.1965", re.I)
ROOTS = ["/mnt/d/OneDrive/Dokumente","/mnt/d/OneDrive/Eigene Dateien","/mnt/d/OneDrive/Desktop"]
SKIP_DIR = re.compile(r"(^|/)(Bolla|Adobe|Audacity\d?|Freemake|Journals|Office|Copilot|Dokumente Robin|Reni|Fun|Robin|Gesundheit - TK|node_modules|\.git|OneNote.*|Outlook-Dateien|ID\.3|My Games|Downloads|AURORA)(/|$)", re.I)
EXT = {".pdf",".docx",".txt",".doc",".rtf",".jpg",".jpeg",".png",".odt",".xlsx"}
TEXT_EXT = {".pdf",".docx",".txt"}
def hits_in(s):
    s=s.lower(); return sorted({k for k in KW if k in s})
def text_of(p, ext):
    try:
        if ext==".txt": return open(p,errors="ignore").read(60000)
        if ext==".docx":
            x=zipfile.ZipFile(p).read("word/document.xml").decode("utf8","ignore")
            return re.sub(r"\s+"," ",re.sub(r"<[^>]+>"," ",x))[:60000]
        if ext==".pdf":
            from pypdf import PdfReader
            r=PdfReader(p); return " ".join((pg.extract_text() or "") for pg in r.pages[:8])[:60000]
    except Exception as e: return None
    return ""
def step1():
    n=0; out=open(OUT+"files_hits.jsonl","w",buffering=1)
    for root in ROOTS:
        for d,dirs,files in os.walk(root):
            dirs[:] = [x for x in dirs if not SKIP_DIR.search(d+"/"+x)]
            for f in files:
                ext=os.path.splitext(f)[1].lower()
                if ext not in EXT: continue
                p=os.path.join(d,f); n+=1
                if n%500==0: report(JOB,"Gesundheitsakte","laeuft",f"Schritt 1: {n} Dateien geprüft")
                try:
                    if os.path.getsize(p)>25_000_000: continue
                except Exception: continue
                nh=hits_in(f+" "+d)
                rec={"path":p,"name_hits":nh,"in_gesundheit":"gesundheit" in p.lower() or "versicherung" in p.lower(),"text":"nicht_gelesen"}
                if ext in TEXT_EXT:
                    t=text_of(p,ext)
                    if t is None: rec["text"]="fehler"
                    elif len(t.strip())<30 and ext==".pdf": rec["text"]="kein_text_scan"
                    else:
                        ch=hits_in(t); rec["text"]="ok"; rec["content_hits"]=ch
                        rec["self"]=bool(SELF.search(t)); rec["reni"]=bool(RENI.search(t))
                        if ch and (rec["self"] or nh or rec["in_gesundheit"]): rec["snippet"]=t[:300]
                elif ext in {".jpg",".jpeg",".png"}: rec["text"]="bild"
                if nh or rec.get("content_hits") and (rec.get("self") or rec["in_gesundheit"]) or rec["text"]=="kein_text_scan" and (nh or rec["in_gesundheit"]):
                    out.write(json.dumps(rec,ensure_ascii=False)+"\n")
    out.close(); return n
def step2():
    from outlook_oauth2 import refresh_access_token
    tok=refresh_access_token(); seen={}
    terms=["Arztbrief","Befund","Diagnose","Krankenhaus","Klinik","Operation","Gallenblase","Darmspiegelung","Koloskopie","Pneumothorax","Herzkatheter","Rezept","Überweisung","Röntgen","MRT","Ultraschall","Impfung","Zahnarzt","Augenarzt","Hautarzt","Orthopäde","Physiotherapie","Reha","Krankschreibung","Bänderriss","Hausarzt","Facharzt","Patient","Arzttermin","Laborwerte"]
    for t in terms:
        url="https://graph.microsoft.com/v1.0/me/messages?$search="+urllib.parse.quote(f'"{t}"')+"&$top=100&$select=subject,from,receivedDateTime,bodyPreview,hasAttachments"
        try:
            r=urllib.request.Request(url,headers={"Authorization":"Bearer "+tok})
            for m in json.load(urllib.request.urlopen(r,timeout=60)).get("value",[]):
                e=seen.setdefault(m["id"],{"subject":m["subject"],"from":(m.get("from") or {}).get("emailAddress",{}).get("address"),"date":m["receivedDateTime"][:10],"preview":m["bodyPreview"][:300],"att":m["hasAttachments"],"terms":[]})
                e["terms"].append(t)
        except Exception as ex: print("mail-fehler",t,repr(ex),flush=True)
        time.sleep(1)
    with open(OUT+"mail_hits.jsonl","w") as f:
        for i,e in seen.items(): f.write(json.dumps({"id":i,**e},ensure_ascii=False)+"\n")
    return len(seen)
if __name__=="__main__":
    report(JOB,"Gesundheitsakte","laeuft","Schritt 1+2 gestartet (lokal, ohne Tokens)")
    try:
        n=step1(); m=step2()
        report(JOB,"Gesundheitsakte","ok",f"Schritt 1+2 fertig: {n} Dateien geprüft, {m} Mails als Treffer. Weiter mit Vorsortierung.")
    except Exception as e:
        report(JOB,"Gesundheitsakte","fehler",repr(e)[:200])
