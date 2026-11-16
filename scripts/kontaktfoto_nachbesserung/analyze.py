import os, sys, json, io, math, datetime, shutil, importlib.util
import cv2, numpy as np
from PIL import Image, ImageOps
Image.MAX_IMAGE_PIXELS=None
M="/home/bolla/workspace/scripts/models/"
det=cv2.FaceDetectorYN.create(M+"yunet.onnx","",(320,320),0.7,0.3,5000); rec=cv2.FaceRecognizerSF.create(M+"sface.onnx","")
NOW=datetime.datetime(2026,11,16)
spec=importlib.util.spec_from_file_location("s","/home/bolla/workspace/scripts/outlook_gmail_sync.py"); s=importlib.util.module_from_spec(spec); spec.loader.exec_module(s)
tok=s.get_ms_token(); contacts={c["displayName"]:c["id"] for c in s.get_outlook_contacts(tok)}
def detect(bgr):
    h,w=bgr.shape[:2]; det.setInputSize((w,h)); _,f=det.detect(bgr); return [] if f is None else list(f)
def iou(a,b):
    ax,ay,aw,ah=a; bx,by,bw,bh=b; x1,y1=max(ax,bx),max(ay,by); x2,y2=min(ax+aw,bx+bw),min(ay+ah,by+bh)
    i=max(0,x2-x1)*max(0,y2-y1); return i/(aw*ah+bw*bh-i+1e-9)
def metrics(bgr,row):
    x,y,w,h=[int(v) for v in row[:4]]; x=max(x,0); y=max(y,0)
    g=cv2.cvtColor(bgr[y:y+h,x:x+w],cv2.COLOR_BGR2GRAY); g=cv2.resize(g,(160,160),interpolation=cv2.INTER_AREA)
    lv=float(cv2.Laplacian(g,cv2.CV_64F).var())
    re,le,nose=row[4:6],row[6:8],row[8:10]; ed=max(1e-6,abs(le[0]-re[0])); mid=(re[0]+le[0])/2
    frontal=1-min(1,abs(nose[0]-mid)/(ed*0.6)); roll=abs(math.degrees(math.atan2(le[1]-re[1],le[0]-re[0])))
    if roll>180-roll: roll=180-roll
    frontal*=(1-min(0.5,roll/60))
    al=rec.alignCrop(bgr,row); emb=rec.feature(al)
    return dict(lv=lv,frontal=float(frontal),score=float(row[14]),w=int(row[2]),emb=emb)
def cos(a,b): return float(rec.match(a,b,cv2.FaceRecognizerSF_FR_COSINE))
def load_cand(c):
    im=Image.open(c["file"]); raw=im.size
    im2=ImageOps.exif_transpose(im).convert("RGB")
    if im2.size!=(c["W"],c["H"]):
        im2=im.convert("RGB")
        if im2.size!=(c["W"],c["H"]): return None
    return im2
def crop_square(im,box):
    x,y,w,h=box; side=max(w,h)*2.5; cx=x+w/2; cy=y+h*0.58
    side=min(side,min(im.size)); x0=min(max(cx-side/2,0),im.size[0]-side); y0=min(max(cy-side/2,0),im.size[1]-side)
    return im.crop((int(x0),int(y0),int(x0+side),int(y0+side)))
def analyze(g):
    d=f"cand/{g}"; m=json.load(open(d+"/meta.json")); contact=m["contact"]
    out=dict(group=g,contact=contact,items=m["total"],status="",cands=[])
    if contact not in contacts: out["status"]="Kontakt nicht gefunden"; return out
    cur=s.get_outlook_photo(tok,contacts[contact]); cur_info=None
    if cur:
        cim=Image.open(io.BytesIO(cur)).convert("RGB"); cb=cv2.cvtColor(np.array(cim),cv2.COLOR_RGB2BGR)
        fs=detect(cb)
        if fs:
            f=max(fs,key=lambda r:r[2]*r[3]); cm=metrics(cb,f); cur_info=dict(size=cim.size,fw=cm["w"],lv=cm["lv"],frontal=cm["frontal"],emb=cm["emb"],score=cm["score"],bytes=len(cur))
        else: cur_info=dict(size=cim.size,fw=0,lv=0,frontal=0,emb=None,score=0,bytes=len(cur))
    out["cur"]={k:(v if k!="emb" else None) for k,v in (cur_info or {}).items()}
    cs=[]
    for c in m["cands"]:
        if not c.get("file"): continue
        im=load_cand(c)
        if im is None: c["why"]="Größe/Orientierung passt nicht"; cs.append(c); continue
        x,y,w,h=c["box"]; pad=int(max(w,h)*1.2); X0,Y0=max(0,x-pad),max(0,y-pad); X1,Y1=min(im.size[0],x+w+pad),min(im.size[1],y+h+pad)
        reg=im.crop((X0,Y0,X1,Y1)); bgr=cv2.cvtColor(np.array(reg),cv2.COLOR_RGB2BGR)
        fs=detect(bgr); best=None;bi=0
        for f in fs:
            i=iou((f[0]+X0,f[1]+Y0,f[2],f[3]),(x,y,w,h))
            if i>bi: bi,best=i,f
        if best is None or bi<0.3: c["why"]=f"keine Gesichtserkennung auf Box (IoU {bi:.2f})"; cs.append(c); continue
        mt=metrics(bgr,best); c.update(mt={k:v for k,v in mt.items() if k!="emb"},emb=mt["emb"],fw_real=mt["w"],bgr_ok=True)
        # Fremdgesichter im Zuschnitt
        cr=crop_square(im,[best[0]+X0,best[1]+Y0,best[2],best[3]]); cb2=cv2.cvtColor(np.array(cr),cv2.COLOR_RGB2BGR)
        if cb2.shape[0]>800: sc=800/cb2.shape[0]; cb3=cv2.resize(cb2,None,fx=sc,fy=sc)
        else: sc=1; cb3=cb2
        others=[f for f in detect(cb3) if f[2]/sc>0.35*best[2] and iou((f[0]/sc,f[1]/sc,f[2]/sc,f[3]/sc),(best[0]+X0-cr.size[0]*0+0,0,0,1))>=-1]
        # Hauptgesicht = größte Überlappung mit Zentrum; zähle Gesichter deren Zentrum nicht das Hauptgesicht ist
        cxm=(best[0]+X0+best[2]/2); 
        c["others"]=max(0,len([f for f in detect(cb3) if f[2]/sc>0.35*best[2]])-1)
        c["box_det"]=[best[0]+X0,best[1]+Y0,best[2],best[3]]
        cs.append(c)
    ok=[c for c in cs if c.get("mt")]
    if not ok: out["status"]="keine verwertbaren Kandidaten"; out["cands"]=[{k:v for k,v in c.items() if k not in("emb",)} for c in cs]; return out
    # Ausreißer (Fehlerkennung): Ähnlichkeit zum Median der anderen
    for c in ok:
        sims=[cos(c["emb"],o["emb"]) for o in ok if o is not c]
        c["sim_group"]=float(np.median(sims)) if sims else 1.0
        c["sim_cur"]=cos(c["emb"],cur_info["emb"]) if cur_info and cur_info.get("emb") is not None else None
    lvmax=max(c["mt"]["lv"] for c in ok)
    for c in ok:
        age=max(0,(NOW-datetime.datetime.strptime(c["date"],"%Y-%m-%d")).days/365.25)
        rec_=math.exp(-age/3); size_=min(1,c["fw_real"]/300); sh=min(1,c["mt"]["lv"]/max(1,lvmax)); fr=c["mt"]["frontal"]
        c["age"]=round(age,1); c["sharp_rel"]=round(sh,2)
        c["total"]=round(0.40*rec_+0.20*size_+0.25*sh+0.15*fr-0.12*min(2,c["others"]),3)
        c["eligible"]=bool(c["mt"]["score"]>=0.8 and fr>=0.5 and sh>=0.5 and c["fw_real"]>=130 and (len(ok)<3 or c["sim_group"]>=0.2) and (c["sim_cur"] is None or c["sim_cur"]>=0.2))
    el=[c for c in ok if c["eligible"]]
    out["cands"]=[{k:v for k,v in c.items() if k not in("emb",)} for c in cs]
    if not el: out["status"]="keiner geeignet"; return out
    best=max(el,key=lambda c:c["total"])
    # Vergleich mit aktuellem Kontaktfoto
    if cur_info and cur_info.get("emb") is not None:
        sh_c=min(1,cur_info["lv"]/max(1,lvmax)); cur_total=0.40*0.45+0.20*min(1,cur_info["fw"]/300)+0.25*sh_c+0.15*cur_info["frontal"]
        small=max(cur_info["size"])<=320
    else: cur_total=0.2; small=True
    margin=0.08 if small else 0.15
    best_c=best; out["best"]=dict(file=best_c["file"],date=best_c["date"],name=best_c["name"],total=best_c["total"],fw=best_c["fw_real"],sim_cur=best_c["sim_cur"],others=best_c["others"])
    out["cur_total"]=round(cur_total,3); out["margin"]=margin
    if best_c["total"]>=cur_total+margin: 
        out["status"]="ERSETZEN"
        im=load_cand(best_c); cr=crop_square(im,best_c["box_det"]); 
        os.makedirs("out",exist_ok=True); cr.thumbnail((256,256)); cr.save(f"out/{contact}.jpg","JPEG",quality=92); out["crop"]=cr.size
        if cur: open(f"out/{contact}__vorher.jpg","wb").write(cur)
    else: out["status"]="behalten"
    return out
if __name__=="__main__":
    res=[]
    for g in sys.argv[1:]:
        r=analyze(g); res.append(r)
        b=r.get("best") or {}
        print(g,"->",r["contact"],"|",r["status"],"| cur",r.get("cur_total"),"best",b.get("total"),b.get("date"),b.get("fw"),"sim",b.get("sim_cur"),"others",b.get("others"),flush=True)
        if os.path.exists("decisions.json"): d=json.load(open("decisions.json"))
        else: d={}
        d[g]=r; json.dump(d,open("decisions.json","w"),ensure_ascii=False,default=str)
