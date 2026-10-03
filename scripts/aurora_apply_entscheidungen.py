import re,json,os
from docx import Document
W='/home/bolla/workspace'
md=open(f'{W}/scratch/aurora_samstag_20261003/vorschlaege_fuer_chris.md',encoding='utf-8').read()
blocks=re.split(r'^### ',md,flags=re.M)[1:]
dec={}
d=Document('/mnt/d/OneDrive/Desktop/AURORA_II_Vorschlaege_Kap1-8.docx')
cur=None
for p in d.paragraphs:
    m=re.match(r'^(\d+)\. ',p.text)
    if m: cur=int(m.group(1))
    if p.text.startswith('Entscheidung:'): dec[cur]=p.text[13:].strip(' _')
SKIP={16,22,28,33,38,50,55,57,69}   # manuell
data=json.load(open(f'{W}/data/aurora2.json',encoding='utf-8'))
log=[]
for i,b in enumerate(blocks,1):
    kn=int(re.match(r'Kap\. (\d+)',b).group(1))
    z=re.search(r'^STELLE:\s*(.*?)\n\nVORSCHLAG:',b,re.M|re.S); e=re.search(r'^VORSCHLAG:\s*(.*?)\s*\Z',b,re.M|re.S)
    z=z.group(1).strip(); e=e.group(1).strip()
    if i in SKIP or not dec[i].lower().startswith('ja'): continue
    k=[x for x in data['kapitel'] if re.match(rf'^\s*(Kapitel\s*)?{kn}\b',x['titel'])] or [data['kapitel'][kn-1]]
    t=k[0]['text']; c=t.count(z)
    if c==1: k[0]['text']=t.replace(z,e,1); log.append(f'{i} OK Kap{kn}')
    else: log.append(f'{i} TREFFER={c} Kap{kn}: {z[:70]}')
open(f'{W}/data/aurora2.json.tmp_chris','w',encoding='utf-8').write(json.dumps(data,ensure_ascii=False,indent=2))
os.replace(f'{W}/data/aurora2.json.tmp_chris',f'{W}/data/aurora2.json')
print('\n'.join(l for l in log if 'OK' not in l)); print(sum('OK' in l for l in log),'angewandt')
