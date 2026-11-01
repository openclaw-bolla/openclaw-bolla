import json, time, urllib.request
API = "http://127.0.0.1:18790"
def get(p): return json.load(urllib.request.urlopen(API + p, timeout=30))
def post(p, b):
    r = urllib.request.Request(API + p, data=json.dumps(b).encode(), headers={"Content-Type": "application/json"})
    return json.load(urllib.request.urlopen(r, timeout=30))
for kind in ("marie", "anton", "mia"):
    print(kind, post("/api/tonies/generate", {"kind": kind, "teil": "song", "wunsch": ""}), flush=True)
    for _ in range(60):
        time.sleep(10)
        if not get("/api/tonies")["kinder"][kind]["song"].get("busy"): break
    print(kind, "fertig", get("/api/tonies")["kinder"][kind]["song"].get("fehler"), flush=True)
