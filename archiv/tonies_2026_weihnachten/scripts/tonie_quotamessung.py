import json, time, urllib.request
API = "http://127.0.0.1:18790"
def get(p): return json.load(urllib.request.urlopen(API + p, timeout=30))
def post(p, b):
    r = urllib.request.Request(API + p, data=json.dumps(b).encode(), headers={"Content-Type": "application/json"})
    return json.load(urllib.request.urlopen(r, timeout=30))
def q():
    d = get("/api/claudequota"); return d["five_hour_pct"], d["seven_day_pct"]
print("vorher", q(), flush=True)
for kind, teil in [("anton", "lied"), ("mia", "song"), ("mia", "lied"), ("mia", "geschichte")]:
    post("/api/tonies/generate", {"kind": kind, "teil": teil, "wunsch": ""})
    for _ in range(60):
        time.sleep(10)
        if not get("/api/tonies")["kinder"][kind][teil].get("busy"): break
    print(kind, teil, "fertig", q(), flush=True)
time.sleep(60)
print("nachher", q(), flush=True)
