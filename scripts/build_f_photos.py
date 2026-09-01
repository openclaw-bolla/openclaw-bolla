import os, re, json, random, sys, time, subprocess, urllib.request, urllib.error
from PIL import Image, ImageOps

ROOT = "/mnt/d/OneDrive"
OUT  = "/home/bolla/workspace/mission-control/f-photos"
LOG  = "/home/bolla/workspace/scripts/build_f.log"
POOL_SIZE = 120
VISION_MODEL = "claude-sonnet-5"   # Landmark-Erkennung ist kein Opus-Job; ~5x leichter fürs Kontingent
MAXPX, Q, MIN_BYTES = 1600, 85, 90_000

def log(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    open(LOG,"a").write(s+"\n")

open(LOG,"w").write("")
random.seed()

INCLUDE_ROOTS = [
 "Andalusien 2008","Berlin","Bormio 2001","Côte d'Azur","Damüls 2026","Dänemark 2021",
 "EXPO 2000","Europapark 99","Ewalds","Filzmoos 2011","Filzmoos 2012","Fiss Ostern 2016",
 "Fiss Ostern 2017","Florida 2005","Grindelwald 2000","Harz 2024","Holland Ostern 2014",
 "Hong Kong 1999","Ischgl 2022","Italien 2014","Kaprun 1999","Kitzbühel 2014","Kreta 2012",
 "Kreuzfahrt 2025","Kroatien 2018","Malediven 2000","Mallorca 2015","Mandel-Clan","Mandels",
 "Natur","New York 2000","Norden","Norwegen 2005","Norwegen 2007","Ostsee REHA 2022",
 "Paris - Kenia 2017","Paris 2002","Prag 2015","Rhodos 2020","Schladming 2009","Schladming 2010",
 "Schladming 2024","Sizilien 2013","Sölden 2023","Städte","Süddeutschland 2026","Sylt 2012",
 "Teneriffa 2011","Thailand 2022","Türkei 2009","USA 2001","USA 2016","USA 2019",
 "Usedom-Heringsdorf 2022","Venedig 2002","Vogelpark Walsrode","Warth 2018","Warth 2019",
 "West Deutschland Städte 2024","Wien 2003","Zell am See 2014-2015","Zillertal 2013",
 "Zillertal 2024","Ägypten 99",
 "Bilder/Eigene Aufnahmen_Backup/Renate",
 "Bilder/Eigene Aufnahmen_Backup/Robin",
 "Bilder/Eigene Aufnahmen_Backup/Stephanie und Familie",
 "Bilder/Eigene Aufnahmen_Backup/Reisen und Ausflüge",
 "Bilder/Eigene Aufnahmen_Backup/Natur und Landschaft",
 "Bilder/Eigene Aufnahmen_Backup/Events und Feiern",
]
EXCLUDE_SUB = ["_mcf-dateien","robin bereal","reisepräsentation","/panorama",
               "robin/boy2girl","/content","/images1","/images",
               "/sonstiges","aufnahmen_backup/familie","essen und trinken",
               "/büro","/buero","/unfall","/op ","addon bahrenfeld",
               "hüft-tep","reparatur","renovierung","küche mami","/mami/"]
# Ordnernamen, die als Bildunterschrift zu nichtssagend sind -> Ordner wird übersprungen
WEAK_NAMES = {"sonstiges","familie","diverses","verschiedenes","bilder","eigene aufnahmen",
              "eigene aufnahmen_backup","fun fotos","gesammelte werke","today","at home",
              "essen und trinken","bearbeitete bilder"}
def excluded(rel):
    low = rel.lower()
    return any(e in low for e in EXCLUDE_SUB)

MONTHS = ["","Januar","Februar","März","April","Mai","Juni","Juli","August",
          "September","Oktober","November","Dezember"]
def year_from_name(s):
    m = re.findall(r"(19\d{2}|20\d{2})", s)
    return m[-1] if m else None
def nice_place(reldir):
    """reldir = Ordnerpfad OHNE Dateiname."""
    parts = [x for x in reldir.split("/") if x]
    if len(parts) >= 2 and parts[0]=="Bilder" and parts[1]=="Eigene Aufnahmen_Backup":
        parts = parts[2:] or ["Eigene Aufnahmen"]
    def clean(x):
        for _ in range(3):
            x = x.strip(" -–_.")
            x = re.sub(r"[-–\s]*(19\d{2}|20\d{2})(\s*-\s*\d{2,4})?\s*$", "", x)
            x = re.sub(r"[-–\s]*\d{1,2}\s*-\s*\d{1,2}\s*$", "", x)   # "16-9", "21-12"-Reste
            x = re.sub(r"\s+\d{1,2}\s*$", "", x)                      # einzelne Zahl ("Legoland 5")
        return x.strip(" -–_.")
    # reine Jahres-/Datums-/nichtssagende Komponenten raus
    keep = []
    for x in parts:
        if re.fullmatch(r"(19|20)\d{2}", x): continue
        if re.fullmatch(r"\d{1,2}[.\-]\d{1,2}[.\-]\d{2,4}", x): continue
        if re.match(r"^\d{6}[-_ ]", x): x = re.sub(r"^\d{6}[-_ ]+", "", x)
        # Robin-Altersordner ("6-7 Jahre", "23-24", "Erste 3 Monate", "9-12 Monate") -> "Robin"
        if re.fullmatch(r"\d{1,2}\s*-\s*\d{1,2}(\s*jahre?)?", x, re.I) or \
           re.fullmatch(r"(erste|bis)\s+.*(monate?|jahre?)", x, re.I):
            x = "Robin"
        c = clean(x)
        if not c: continue
        if c.lower() in WEAK_NAMES: continue
        if keep and keep[-1] == c: continue
        keep.append(c)
    if not keep:
        return ""   # nichts Brauchbares -> Aufrufer überspringt den Ordner
    # deduplizieren / enthaltene weglassen, max 2 Ebenen (fein · grob)
    fine = keep[-1]
    coarse = keep[0] if keep[0] != fine and keep[0] not in fine and fine not in keep[0] else None
    return f"{fine} · {coarse}" if coarse else fine

_JUNK = re.compile(r"^(img|dsc|dscn|p|pict|photo|foto|image|20\d{6}|1\d{9,})", re.I)
def humanize(fname):
    b = os.path.splitext(os.path.basename(fname))[0]
    b = re.sub(r"\s*\(\d+\)\s*$", "", b)
    b = re.sub(r"[_\-]+", " ", b).strip()
    b = re.sub(r"\b(19\d{2}|20\d{2})\b", "", b)
    b = re.sub(r"\b\d{1,2}[.\-]\d{1,2}([.\-]\d{2,4})?\b", "", b)
    b = re.sub(r"\b\d{2,}\s*(km|k|m)\b", "", b, flags=re.I)
    b = re.sub(r"\biOS\b", "", b)
    b = re.sub(r"\s{2,}", " ", b).strip(" -–")
    if not b or _JUNK.match(b) or len(b) < 3 or not re.search(r"[A-Za-zÄÖÜäöüß]{3}", b):
        return ""
    if b.islower():
        b = b[:1].upper() + b[1:]
    return b


# ---------------- Ortsermittlung Quelle 1: GPS-EXIF + Nominatim Reverse-Geocoding ----------------
NOMINATIM_URL = "https://nominatim.openstreetmap.org/reverse"
NOMINATIM_UA  = "bolla-f-photos/1.0 (privates Familienprojekt)"
NOMINATIM_MIN_INTERVAL = 1.0  # Sekunden zwischen Requests -- Nutzungsbedingungen Nominatim
_last_geocode_call = [0.0]
_GEOCODE_CACHE = {}  # (lat_round, lon_round) -> Ortsname oder None

def _gps_ref(v):
    if isinstance(v, bytes):
        v = v.decode(errors="ignore")
    return str(v).strip().upper()[:1]

def _dms_to_deg(v):
    """v = Tupel (Grad, Minuten, Sekunden), jeweils IFDRational/Zahl -> Dezimalgrad."""
    try:
        d, m, s = v
        return float(d) + float(m) / 60.0 + float(s) / 3600.0
    except Exception:
        return None

def gps_from_exif(ex):
    """ex = im._getexif()-Dict. Gibt (lat, lon) in Dezimalgrad zurück oder None, wenn kein/kaputtes GPS."""
    try:
        gps = ex.get(34853)  # GPSInfo-IFD
        if not gps:
            return None
        lat_dms, lat_ref = gps.get(2), gps.get(1)
        lon_dms, lon_ref = gps.get(4), gps.get(3)
        if not (lat_dms and lon_dms and lat_ref and lon_ref):
            return None
        lat = _dms_to_deg(lat_dms)
        lon = _dms_to_deg(lon_dms)
        if lat is None or lon is None:
            return None
        if _gps_ref(lat_ref) == "S":
            lat = -lat
        if _gps_ref(lon_ref) == "W":
            lon = -lon
        if abs(lat) < 0.001 and abs(lon) < 0.001:
            return None  # "Null Island" -- kaputtes/leeres GPS-Tag
        if not (-90 <= lat <= 90 and -180 <= lon <= 180):
            return None
        return (lat, lon)
    except Exception:
        return None

def reverse_geocode(lat, lon):
    """Nominatim Reverse-Geocoding, cache-freundlich (Koordinaten auf ~2 Nachkommastellen gerundet
    -> nahe beieinanderliegende Fotos teilen sich einen Request). Gibt Ortsnamen zurück oder None."""
    key = (round(lat, 2), round(lon, 2))
    if key in _GEOCODE_CACHE:
        return _GEOCODE_CACHE[key]
    elapsed = time.time() - _last_geocode_call[0]
    if elapsed < NOMINATIM_MIN_INTERVAL:
        time.sleep(NOMINATIM_MIN_INTERVAL - elapsed)
    result = None
    try:
        qs = f"format=json&lat={lat:.5f}&lon={lon:.5f}&zoom=10&accept-language=de"
        req = urllib.request.Request(f"{NOMINATIM_URL}?{qs}", headers={"User-Agent": NOMINATIM_UA})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        addr = data.get("address", {}) or {}
        place = (addr.get("city") or addr.get("town") or addr.get("village")
                 or addr.get("municipality") or addr.get("county"))
        country = addr.get("country")
        if place and country and country.strip().lower() not in ("deutschland", "germany"):
            result = f"{place}, {country}"
        elif place:
            result = place
        elif country:
            result = country
    except Exception as e:
        log("  geocode FAIL", lat, lon, repr(e))
    finally:
        _last_geocode_call[0] = time.time()
    _GEOCODE_CACHE[key] = result
    return result

# ---------------- Ortsermittlung Quelle 2: Vision-Fallback (Opus) ohne GPS ----------------
def vision_place(fp):
    """Sonnet schaut sich das Foto an (gleiches Subprocess-Pattern wie ai_direct() in aufpeppen.py) und
    liefert NUR bei eindeutig erkennbarem Wahrzeichen/markanter Landschaft einen Ortsnamen, sonst None.
    Rät bewusst NICHT -- 'unknown' ist ausdrücklich der bevorzugte Ausgang bei Unsicherheit.
    Wenn ein BEKANNTES Wahrzeichen klar erkennbar ist, wird es der Stadt vorangestellt
    ('Odeonskirche, München')."""
    prompt = (
        "Du bist Bolla, Chris' KI-Assistent. Schau dir mit dem Read-Tool genau dieses eine Foto an:\n"
        f"- {fp}\n\n"
        "Frage: Ist auf dem Bild ein EINDEUTIG erkennbares Wahrzeichen, eine unverwechselbare "
        "Landschaft oder markante Architektur zu sehen (Beispiele: Eiffelturm, Kolosseum, ein "
        "bekannter Berggipfel/Skyline, ein berühmtes Bauwerk)?\n\n"
        "HARTE REGEL, unbedingt einhalten: Sei extrem zurückhaltend. Bei generischen Innenraum-, "
        "Essens-, Personen- oder Alltagsfotos, bei unklarer/uneindeutiger Umgebung, oder wenn du dir "
        "auch nur ETWAS unsicher bist, antworte NUR mit dem Wort 'unknown' -- NICHTS sonst. "
        "Rate NIEMALS ins Blaue. Eine falsche oder erfundene Ortsangabe ist schlimmer als gar keine. "
        "Lieber zehnmal 'unknown' zurückgeben als einmal eine unsichere Vermutung als Fakt ausgeben. "
        "Im Zweifel IMMER 'unknown'.\n\n"
        "Format der Antwort, wenn (und nur wenn) du sicher bist:\n"
        "- Ist ein KONKRETES, allgemein bekanntes Wahrzeichen klar erkennbar, nenne es zuerst, "
        "dann die Stadt: 'Wahrzeichen, Stadt' (z.B. 'Brandenburger Tor, Berlin'). Nur bei wirklich "
        "namhaften, eindeutig identifizierbaren Bauwerken/Orten -- NICHT bei irgendeiner Kirche/Brücke.\n"
        "- Sonst nur der Ort: 'Stadt' oder 'Stadt, Land' (z.B. 'Rom, Italien').\n"
        "- Land nur anhängen, wenn es NICHT Deutschland ist.\n\n"
        "Antworte NUR mit dieser einen Zeile auf Deutsch, knapp, keine Erklärung, keine "
        "Anführungszeichen, kein weiterer Text -- oder NUR mit dem einzelnen Wort 'unknown'."
    )
    try:
        r = subprocess.run(["claude", "-p", prompt, "--model", VISION_MODEL],
                            capture_output=True, text=True, timeout=120)
        out = (r.stdout or "").strip()
        lines = [l.strip() for l in out.splitlines() if l.strip()]
        ans = lines[-1] if lines else ""
        ans = ans.strip(" \"'.")
        if not ans or ans.lower() == "unknown" or len(ans) > 60:
            return None
        return ans
    except Exception as e:
        log("  vision FAIL", fp, repr(e))
        return None


# --- gather (kein per-file stat!) ---
t0 = time.time()
buckets = {}
for inc in INCLUDE_ROOTS:
    base = os.path.join(ROOT, inc)
    if not os.path.isdir(base):
        log("MISS", inc); continue
    for dp, dn, fn in os.walk(base):
        rel = os.path.relpath(dp, ROOT)
        if excluded(rel):
            dn[:] = []; continue
        imgs = []
        for f in fn:
            e = os.path.splitext(f)[1].lower()
            if e not in (".jpg",".jpeg",".png"): continue
            fl = f.lower()
            if any(b in fl for b in ("klein","thumb","route","fahrt","bericht","scan","comic",
                    "bandage","buero","büro","nachtrag","screenshot","werbung","amazon",
                    "bestellung","angebot","_am_pc","_am_schreibtisch",
                    " map","-map","karte","plan ","urkunde","zeugnis","einladung",
                    "op ","hüft","tep","rezept","quittung","rechnung")): continue
            if re.search(r"[_\-]wa\d{3,4}|wa\d{4}", fl): continue   # WhatsApp-Weiterleitungen
            imgs.append(os.path.join(rel, f))
        if imgs:
            buckets[rel] = imgs
    log(f"scan {inc}: {sum(len(v) for v in buckets.values())} kumuliert  ({time.time()-t0:.0f}s)")

# Ordner ohne brauchbare Bildunterschrift komplett verwerfen
leafs = [lf for lf in buckets if nice_place(lf)]
log(f"{len(leafs)}/{len(buckets)} Ordner mit Caption, {sum(len(buckets[l]) for l in leafs)} Fotos, scan {time.time()-t0:.0f}s")

# --- Auswahl: max 1 pro Ordner, max 2 pro Zweig, Streuung ---
def branch(lf):
    ps = lf.split("/")
    return "/".join(ps[:3]) if ps[0] in ("Mandels","Bilder") else ps[0]

def pick_from(lf):
    cands = buckets[lf][:]
    random.shuffle(cands)
    for rel in cands:
        fp = os.path.join(ROOT, rel)
        try:
            if os.path.getsize(fp) < MIN_BYTES: continue
        except OSError:
            continue
        return rel
    return None

picked = []
bcount = {}
# 1) Renate-Ordner zuerst (bis zu 3)
ren = [lf for lf in leafs if lf.lower().endswith("eigene aufnahmen_backup/renate")]
for lf in ren:
    for _ in range(3):
        r = pick_from(lf)
        if r and r not in picked:
            picked.append(r); bcount[branch(lf)] = bcount.get(branch(lf),0)+1
random.shuffle(leafs)
for lf in leafs:
    if len(picked) >= POOL_SIZE: break
    b = branch(lf)
    if bcount.get(b,0) >= 2: continue
    r = pick_from(lf)
    if not r or r in picked: continue
    picked.append(r); bcount[b] = bcount.get(b,0)+1

log(f"{len(picked)} ausgewählt, {time.time()-t0:.0f}s")

# --- Resize + EXIF + Ort (GPS-Geocoding > Vision-Fallback > Ordnername) ---
_UML = {"ä":"ae","ö":"oe","ü":"ue","ß":"ss","Ä":"ae","Ö":"oe","Ü":"ue",
        "á":"a","à":"a","â":"a","é":"e","è":"e","ê":"e","í":"i","ó":"o","ô":"o","ú":"u","ñ":"n","ç":"c"}
def slugify(s):
    """'Odeonskirche, München' -> 'odeonskirche-muenchen'. Nur der Ort-Teil, ohne Datum."""
    s = s.split(" · ")[0]
    s = "".join(_UML.get(c, c) for c in s).lower()
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    s = re.sub(r"-{2,}", "-", s)
    return s or "foto"

# alte Bilder wegräumen -- Dateinamen sind jetzt sprechend, sonst bleiben f00.jpg & Co. als Leichen liegen
for _old in os.listdir(OUT):
    if _old.lower().endswith((".jpg", ".jpeg", ".png")):
        try: os.remove(os.path.join(OUT, _old))
        except OSError: pass

STATS = {"gps_present": 0, "gps_geocoded": 0, "vision_tried": 0, "vision_hit": 0,
         "vision_unknown": 0, "fallback_ordner": 0}
manifest = []
_used_names = set()
for i, rel in enumerate(sorted(picked)):
    fp = os.path.join(ROOT, rel)
    try:
        im = Image.open(fp)
        dt = None
        ex = {}
        try:
            ex = im._getexif() or {}
            raw = ex.get(36867) or ex.get(306)
            mm = re.match(r"(\d{4}):(\d{2}):", str(raw)) if raw else None
            if mm:
                y, mo = int(mm.group(1)), int(mm.group(2))
                if 1990 <= y <= 2027:
                    dt = f"{MONTHS[mo]} {y}" if 1<=mo<=12 else str(y)
        except Exception: pass
        if not dt:
            dt = year_from_name(rel) or ""

        # 1) GPS-EXIF + Reverse-Geocoding (beste Quelle)
        place, place_src = None, "ordner"
        try:
            coords = gps_from_exif(ex)
        except Exception:
            coords = None
        if coords:
            STATS["gps_present"] += 1
            try:
                geo = reverse_geocode(*coords)
            except Exception as e:
                geo = None
                log("  geocode EXC", rel, repr(e))
            if geo:
                STATS["gps_geocoded"] += 1
                place, place_src = geo, "gps"

        # 2) Vision-Fallback, nur wenn GPS-Weg nichts gebracht hat
        if not place:
            STATS["vision_tried"] += 1
            try:
                vp = vision_place(fp)
            except Exception as e:
                vp = None
                log("  vision EXC", rel, repr(e))
            if vp:
                STATS["vision_hit"] += 1
                place, place_src = vp, "vision"
            else:
                STATS["vision_unknown"] += 1

        # 3) Ordnername (bisheriges Verhalten, unveränderter Fallback)
        if not place:
            STATS["fallback_ordner"] += 1
            place = nice_place(os.path.dirname(rel)) or nice_place(rel) or "Familie Mandel"
            place_src = "ordner"

        im = ImageOps.exif_transpose(im).convert("RGB")
        im.thumbnail((MAXPX, MAXPX), Image.LANCZOS)
        stem = slugify(place)
        name = f"{stem}.jpg"
        n = 2
        while name in _used_names:            # gleicher Ort mehrfach -> -2, -3, ...
            name = f"{stem}-{n}.jpg"; n += 1
        _used_names.add(name)
        im.save(os.path.join(OUT, name), "JPEG", quality=Q, optimize=True)
        cap = f"{place} · {dt}" if dt else place
        manifest.append({"src": f"/f-photos/{name}", "cap": cap, "folder": os.path.dirname(rel)})
        log(f"  {name}  {manifest[-1]['cap']}  [{place_src}]   <- {rel}")
    except Exception as e:
        log("  FAIL", rel, repr(e))

json.dump(manifest, open(os.path.join(OUT,"manifest.json"),"w"), ensure_ascii=False, indent=1)
log(f"DONE {len(manifest)} Fotos -> {OUT}  ({time.time()-t0:.0f}s)")
log(f"Orts-Quellen: GPS vorhanden={STATS['gps_present']} (davon geocoded={STATS['gps_geocoded']})  |  "
    f"Vision versucht={STATS['vision_tried']} (davon Ort erkannt={STATS['vision_hit']}, "
    f"unknown={STATS['vision_unknown']})  |  Ordner-Fallback={STATS['fallback_ordner']}")
