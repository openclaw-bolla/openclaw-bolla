#!/usr/bin/env python3
"""Holt alle Suno-Songs, filtert für DistroKid-Tauglichkeit.
Buckets: glucksrad / schule / geburtstag_name / kandidat.
Speichert Rohliste + Filterergebnis als JSON. KEIN Download hier (separat)."""
import json, re, time, sys, urllib.request, urllib.error

WS = "/home/bolla/workspace"
TOKEN = json.load(open(f"{WS}/config/suno_token.json"))["token"]
BASE = "https://studio-api-prod.suno.com"

# --- Glücksrad-Songtitel (aus Ordner "Songs zum Glücksrad Musikstile") = generische Genre-Klone ---
GLUCKSRAD = {
    "back to the chalkboard","lonely echoes","shake it loose","echoes of eternity",
    "schoolhouse days","fever in the classroom","school's got soul","faith in the classroom",
    "classroom chaos","school rules","classroom daydreams","night whispers","classroom dreams",
    "the forgotten star","escuela de vida","hellish hallways","school bells ringing",
    "class in session","school vibes","school of no rules","school days groove","school of life",
    "schoolyard swing",
}
SCHUL_RE = re.compile(r"\b(classroom|school|schul|escuela|chalkboard|hallway|teenage dream|schoolhouse|schoolyard)", re.I)
GEB_RE   = re.compile(r"(happy birthday|geburtstag|glückwunsch|herzlichen|\bbday\b|\d{1,2}\.\d{1,2}\.\d{2,4})", re.I)
# Enkel/Familie-Namen (immer raus)
FAMILIE  = {"emma","maja","mia","feli","marie","sara","anton","reni","renate","robin","steffi","mandel","lessing"}

def fetch_all():
    songs, page = [], 0
    while True:
        url = f"{BASE}/api/feed/?page={page}&page_size=20"
        req = urllib.request.Request(url, headers={
            "Authorization":f"Bearer {TOKEN}","Accept":"application/json",
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36",
            "Origin":"https://suno.com","Referer":"https://suno.com/",
        })
        for attempt in range(4):
            try:
                with urllib.request.urlopen(req, timeout=30) as r:
                    data = json.load(r); break
            except urllib.error.HTTPError as e:
                if e.code == 429:
                    print(f"  429 auf Seite {page}, warte 12s…", flush=True); time.sleep(12); continue
                if e.code == 401:
                    print("  401 — Token abgelaufen/ungültig. Abbruch.", flush=True); return songs, "401"
                raise
        else:
            print(f"  Seite {page}: zu viele 429, Stop.", flush=True); break
        if not data:
            break
        for s in data:
            songs.append({
                "id": s.get("id"),
                "title": (s.get("title") or "").strip(),
                "status": s.get("status"),
                "audio_url": s.get("audio_url") or f"https://cdn1.suno.ai/{s.get('id')}.mp3",
                "image_url": s.get("image_url") or f"https://cdn2.suno.ai/image_{s.get('id')}.jpeg",
                "created": s.get("created_at"),
            })
        print(f"  Seite {page}: +{len(data)} (gesamt {len(songs)})", flush=True)
        page += 1
        time.sleep(0.4)
    return songs, "ok"

def classify(title):
    t = title.lower().strip()
    words = set(re.findall(r"[a-zäöüß]+", t))
    if t in GLUCKSRAD:           return "glucksrad"
    if GEB_RE.search(t):         return "geburtstag_name"
    if words & FAMILIE:          return "geburtstag_name"
    if SCHUL_RE.search(t):       return "schule"
    return "kandidat"

def main():
    print("Hole alle Songs von Suno…", flush=True)
    songs, st = fetch_all()
    print(f"Insgesamt {len(songs)} Songs geholt (Status {st}).", flush=True)
    # dedupe nach (title,id)
    buckets = {"glucksrad":[], "schule":[], "geburtstag_name":[], "kandidat":[]}
    for s in songs:
        if not s["title"]:
            s["title"] = "(ohne Titel)"
        buckets[classify(s["title"])].append(s)
    json.dump(songs, open(f"{WS}/data/suno_all_songs.json","w"), ensure_ascii=False, indent=1)
    json.dump(buckets, open(f"{WS}/data/suno_filter_result.json","w"), ensure_ascii=False, indent=1)
    print("\n=== FILTER-ERGEBNIS ===")
    for k,v in buckets.items():
        print(f"  {k:18s}: {len(v)}")
    print(f"\nRoh: data/suno_all_songs.json  |  Buckets: data/suno_filter_result.json")

if __name__ == "__main__":
    main()
