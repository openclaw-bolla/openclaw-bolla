import os, sys, json, time, shutil
sys.path.insert(0,"/tmp/claude-1000/nb"); from groups_map import MAP
import analyze as A
done=json.load(open("decisions.json")) if os.path.exists("decisions.json") else {}
todo=[g for g in MAP if g not in done]
t0=time.time()
while todo and time.time()-t0<7200:
    g=todo[0]
    if not os.path.exists(f"cand/{g}/meta.json"): time.sleep(5); continue
    try: r=A.analyze(g)
    except Exception as e: r=dict(group=g,contact=MAP[g],status="FEHLER "+repr(e)[:150],cands=[])
    done[g]=r; json.dump(done,open("decisions.json","w"),ensure_ascii=False,default=str)
    b=r.get("best") or {}
    print(g,"->",r["contact"],"|",r["status"],"| cur",r.get("cur_total"),"best",b.get("total"),b.get("date"),b.get("fw"),"sim",None if b.get("sim_cur") is None else round(b["sim_cur"],2),"others",b.get("others"),flush=True)
    for f in os.listdir(f"cand/{g}"):
        if f.endswith(".jpg"): os.remove(f"cand/{g}/{f}")
    todo.pop(0)
print("RUNNER FERTIG")
