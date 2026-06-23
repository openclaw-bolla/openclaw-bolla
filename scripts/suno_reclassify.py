#!/usr/bin/env python3
"""Reklassifiziert die schon geholten Songs (data/suno_all_songs.json) mit
deutlich schärferen Geburtstag/Name/Schule-Filtern. Kein erneuter Fetch."""
import json, re
WS = "/home/bolla/workspace"
songs = json.load(open(f"{WS}/data/suno_all_songs.json"))

GLUCKSRAD = {
    "back to the chalkboard","lonely echoes","shake it loose","echoes of eternity",
    "schoolhouse days","fever in the classroom","school's got soul","faith in the classroom",
    "classroom chaos","school rules","classroom daydreams","night whispers","classroom dreams",
    "the forgotten star","escuela de vida","hellish hallways","school bells ringing",
    "class in session","school vibes","school of no rules","school days groove","school of life",
    "schoolyard swing",
}
# Geburtstags-Marker (Schüler-Geburtstagslieder)
GEB = re.compile(r"(🎂|🎉|🎈|happy birthday|geburtstag|glückwunsch|herzlichen|\bbday\b|birthday|"
                 r"\bthirteen\b|\btwelve\b|\beleven\b|\bfourteen\b|\bfifteen\b|candles?|countdown|"
                 r"turned thirteen|level 13|happy place|big day|happy day|großer tag|wird bald|"
                 r"\bwird\s+\d|\bat 1[3-5]\b|\b1[3-5]th\b|shining thirteen|seventh star|"
                 r"der neue stern|unser held|my password|, almost|macht.s digital|"
                 r"\b[A-ZÄÖÜ][a-zäöü]{2,}\s+\d{1,2}\b|"          # Name + Zahl (Mara 13)
                 r"\d{1,2}\.\d{1,2}\.\d{2,4})", re.I)
SCHULE = re.compile(r"(classroom|school|schul|escuela|chalkboard|hallway|teenage dream|"
                    r"klasse|\b7[a-c]\b|7er|7ern|graders|pausenklingel|nikolaus)", re.I)
ARTEFAKT = re.compile(r"(^replace\b|^\(ohne titel\)$|^rbn|^[A-Z0-9]{5,8}$)", re.I)
# Possessiv-Name:  Wort + 's/´s/'s  (Lena's, Jonte's …) — aber nicht "don't" etc.
POSSESS = re.compile(r"[A-ZÄÖÜ][a-zäöüа-я]+[’'´]s\b")
# "for X" / "für X" mit großgeschriebenem Namen
FORNAME = re.compile(r"\b(for|für)\s+[A-ZÄÖÜ][a-zä-ü]+", re.I)
# bekannte Vornamen aus Sichtung (Schülernamen)
NAMEN = set("""lena georg laiba jonte ben levin emilia jannes sunje hilrich tina vadim justus mats
hannes ozan zhiwen audrey taavi emily josse jara victor paula kian suri eneko mika anna carl
mohammed paul lotta jesper abdul linnea samuel alea bella samira ida henrike carsten blagovest
suleiman aashir pauli nino jamie cleo tiu carla janna yannick lilly lana charlotte jakob lio
melinda alina ahmet gizem leo emma maja mia feli marie sara anton reni renate robin steffi mandel
lessing ophelia abdul nikolaus jesper kian audreys taavis tina paula alea cleo
amir amara artim artims kjell helvi nikias nikias' henri henris lara laras péter peter peters
moritz merle tim alice johanna mathis kim felix mino minos frieda greta lone elaina mara nele
robinreich woyke amirs""".split())
FAMILIE = {"emma","maja","mia","feli","marie","sara","anton","reni","renate","robin","steffi","mandel","lessing"}

def classify(title):
    t = title.lower().strip()
    if t in GLUCKSRAD: return "glucksrad"
    if ARTEFAKT.search(t): return "artefakt"
    if SCHULE.search(t): return "schule"
    if GEB.search(title): return "geburtstag_name"
    if POSSESS.search(title) or FORNAME.search(title): return "geburtstag_name"
    words = set(re.findall(r"[a-zäöüßа-я]+", t))
    if words & FAMILIE: return "geburtstag_name"
    if words & NAMEN: return "geburtstag_name"
    return "kandidat"

buckets = {"glucksrad":[], "schule":[], "artefakt":[], "geburtstag_name":[], "kandidat":[]}
for s in songs:
    if not s.get("title"): s["title"]="(ohne Titel)"
    buckets[classify(s["title"])].append(s)

json.dump(buckets, open(f"{WS}/data/suno_filter_result.json","w"), ensure_ascii=False, indent=1)
print("=== SCHÄRFERES FILTER-ERGEBNIS ===")
for k,v in buckets.items(): print(f"  {k:18s}: {len(v)}")
print(f"\n=== KANDIDATEN ({len(buckets['kandidat'])}) — komplett ===")
seen=set()
for s in buckets["kandidat"]:
    key=s["title"].strip().lower()
    dup=" [DUP]" if key in seen else ""; seen.add(key)
    print(f'  • {s["title"]}{dup}')
