"""Verschiebt alle Datumsangaben im AURORA-II-Buch um -1 Tag (Wochentage bleiben).
Grund: Buchkalender folgte 2025 (10.11.=Montag); Handlungsjahr ist 2026 (9.11.=Montag).
Aufruf: python3 aurora_kalender_2026.py [--apply]"""
import json,re,sys,os
P='/home/bolla/workspace/data/aurora2.json'
MON=['Januar','Februar','März','April','Mai','Juni','Juli','August','September','Oktober','November','Dezember']
ML=[31,28,31,30,31,30,31,31,30,31,30,31]
MONRE='|'.join(MON)
ST={1:'erst',2:'zweit',3:'dritt',4:'viert',5:'fünft',6:'sechst',7:'siebt',8:'acht',9:'neunt',10:'zehnt',11:'elft',12:'zwölft',
    13:'dreizehnt',14:'vierzehnt',15:'fünfzehnt',16:'sechzehnt',17:'siebzehnt',18:'achtzehnt',19:'neunzehnt',20:'zwanzigst',
    21:'einundzwanzigst',22:'zweiundzwanzigst',23:'dreiundzwanzigst',24:'vierundzwanzigst',25:'fünfundzwanzigst',
    26:'sechsundzwanzigst',27:'siebenundzwanzigst',28:'achtundzwanzigst',29:'neunundzwanzigst',30:'dreißigst',31:'einunddreißigst'}
REV={v:k for k,v in ST.items()}
STEMRE='|'.join(sorted(REV,key=len,reverse=True))
def prev(d,mi):
    if d>1: return d-1,mi
    mi2=(mi-1)%12; return ML[mi2],mi2
def cap(w,orig): return w
log=[]
# 1) Ordinalwort + Monat: "elften Oktober", "dritten November"
def r_ord(m):
    stem,end,mon=m.group(1),m.group(2),m.group(3)
    d=REV[stem]; mi=MON.index(mon); d2,mi2=prev(d,mi)
    new=f"{ST[d2]}{end} {MON[mi2]}"
    log.append((m.group(0),new)); return new
RE_ORD=re.compile(r'\b('+STEMRE+r')(e|en|er|es|em)\s('+MONRE+r')\b')
# 2) "11. Oktober" (nicht vor Jahreszahl 20xx)
def r_num(m):
    d=int(m.group(1)); mon=m.group(2); mi=MON.index(mon); d2,mi2=prev(d,mi)
    new=f"{d2}. {MON[mi2]}"; log.append((m.group(0),new)); return new
RE_NUM=re.compile(r'\b(\d{1,2})\.\s('+MONRE+r')\b(?!\s(?:19|20)\d\d)')
# 3) numerisch "10.11." / "04.11." (Monat 7-12, kein Jahr danach)
def r_dm(m):
    d=int(m.group(1)); mo=int(m.group(2)); d2,mi2=prev(d,mo-1)
    new=(f"{d2:02d}." if len(m.group(1))==2 else f"{d2}.")+(f"{mi2+1:02d}." if len(m.group(2))==2 else f"{mi2+1}.")
    log.append((m.group(0),new)); return new
RE_DM=re.compile(r'(?<![\d.])(\d{1,2})\.(0?[7-9]|1[0-2])\.(?![\d])')
PRE=[('vom siebzehnten bis dreiundzwanzigsten November','vom sechzehnten bis zweiundzwanzigsten November'),
     ('Vierundzwanzigster bis dreißigster November','Dreiundzwanzigster bis neunundzwanzigster November'),
     ('vom 1. auf den 2. Dezember','vom 30. November auf den 1. Dezember')]
def shift(s):
    for a,b in PRE:
        if a in s: s=s.replace(a,'\x00'+b.replace(' ','\x01')+'\x00'); log.append((a,b))
    s=RE_ORD.sub(r_ord,s); s=RE_NUM.sub(r_num,s); s=RE_DM.sub(r_dm,s)
    return s.replace('\x01',' ').replace('\x00','')
def walk(o):
    if isinstance(o,str): return shift(o)
    if isinstance(o,list): return [walk(x) for x in o]
    if isinstance(o,dict): return {k:walk(v) for k,v in o.items()}
    return o
if __name__=='__main__':
    d=json.load(open(P,encoding='utf-8'))
    for key in ('kapitel','glossar','geheim','kriterien','steuerung','einschub_vorschlaege'):
        n0=len(log); d[key]=walk(d[key]); print(key,len(log)-n0,'Ersetzungen')
    from collections import Counter
    for (a,b),c in sorted(Counter(log).items()): print(f'{a!r} -> {b!r} x{c}')
    if '--apply' in sys.argv:
        open(P+'.tmp','w',encoding='utf-8').write(json.dumps(d,ensure_ascii=False,indent=2)); os.replace(P+'.tmp',P); print('ANGEWANDT')
