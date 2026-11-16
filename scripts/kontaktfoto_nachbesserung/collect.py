import os, sys, json, math, time, requests, datetime
os.environ["LD_LIBRARY_PATH"]="/home/bolla/workspace/scripts/browser_libs/extracted/usr/lib/x86_64-linux-gnu:"+os.environ.get("LD_LIBRARY_PATH","")
sys.path.insert(0,"/tmp/claude-1000/nb"); from groups_map import MAP
from playwright.sync_api import sync_playwright
B="https://onedrive.live.com/personal/52539b07421473cf/_api/v2.1/drives/52539b07421473cf"
ents=json.load(open("ents.json"))["value"]
gid={e["identity"]["user"].get("displayName"):e["id"] for e in ents if e["identity"]["user"].get("displayName")}
only=sys.argv[1:]  # optional Gruppenliste
OUT="cand"; os.makedirs(OUT,exist_ok=True)
now=datetime.datetime(2026,11,16)
def dt(it):
    p=it.get("photo") or {}
    s=p.get("takenDateTime") or p.get("alternateTakenDateTime") or (it.get("fileSystemInfo") or {}).get("lastModifiedDateTime") or it.get("createdDateTime")
    return datetime.datetime.strptime(s[:19],"%Y-%m-%dT%H:%M:%S")
with sync_playwright() as p:
    ctx=p.chromium.launch_persistent_context("/home/bolla/workspace/config/browser_profile_onedrive_personen_edge",headless=True,viewport={"width":1400,"height":1000})
    pg=ctx.pages[0] if ctx.pages else ctx.new_page()
    pg.goto("https://onedrive.live.com/photos?photosData=%2Fphotos%2Fpeople"); pg.wait_for_timeout(6000)
    if "login" in pg.url: print("LOGIN ABGELAUFEN"); sys.exit(2)
    JS="async(u)=>{const a=await fetch(u,{credentials:'include'});return [a.status, await a.text()]}"
    for g,contact in MAP.items():
        if only and g not in only: continue
        d=f"{OUT}/{g}"; 
        if os.path.exists(d+"/meta.json"): continue
        os.makedirs(d,exist_ok=True)
        eid=gid[g]; items=[]
        url=(B+"/items/root/items?%24filter=photo+ne+null+and+%28detectedEntity%2FrecognizedEntity%2Fid+eq+%27"+eid+"%27%29&orderby=photo%2FtakenDateTime+desc"
             "&select=id%2Cname%2Cimage%2Cphoto%2CfileSystemInfo%2CcreatedDateTime%2Csize&top=200&%24expand=detectedEntities%28expand%3DrecognizedEntity%29")
        for page in range(3):
            st,tx=pg.evaluate(JS,url)
            if st!=200: print(g,"Listenfehler",st,tx[:150]); break
            j=json.loads(tx); items+=j["value"]; url=j.get("@odata.nextLink")
            if not url or len(items)>=300: break
        cands=[]
        for it in items:
            im=it.get("image") or {}; W,H=im.get("width"),im.get("height")
            if not W: continue
            faces=it.get("detectedEntities") or []
            me=[f for f in faces if (f.get("recognizedEntity") or {}).get("id")==eid]
            if len(me)!=1: continue
            f=me[0]; fw,fh=f["boundingBoxWidth"],f["boundingBoxHeight"]
            if fw<110: continue
            age=(now-dt(it)).days/365.25
            if age<0: age=0
            pre=0.55*math.exp(-age/3)+0.45*min(1,fw/300)
            cands.append(dict(id=it["id"],name=it["name"],date=dt(it).strftime("%Y-%m-%d"),W=W,H=H,box=[f["boundingBoxLeft"],f["boundingBoxTop"],fw,fh],nfaces=len(faces),pre=pre,size=it.get("size")))
        cands.sort(key=lambda c:-c["pre"]); cands=cands[:8]
        for k,c in enumerate(cands):
            st,tx=pg.evaluate(JS,B+"/items/"+c["id"]); 
            try: dl=json.loads(tx).get("@content.downloadUrl")
            except Exception: dl=None
            if not dl: c["file"]=None; continue
            r=requests.get(dl,timeout=120)
            if r.status_code==200 and len(r.content)>5000:
                fn=f"{d}/{k}.jpg"; open(fn,"wb").write(r.content); c["file"]=fn
            else: c["file"]=None
        json.dump(dict(group=g,contact=contact,total=len(items),cands=cands),open(d+"/meta.json","w"),ensure_ascii=False)
        print(g,"->",contact,"Items",len(items),"Kandidaten",len([c for c in cands if c.get("file")]),flush=True)
    ctx.close()
