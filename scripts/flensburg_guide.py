#!/usr/bin/env python3
"""Flensburg Rundgang — Word-Dokument Generator v2"""

from staticmap import StaticMap, CircleMarker, Line
from docx import Document
from docx.shared import Inches, Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import math, requests
from PIL import Image, ImageDraw, ImageFont

OUTPUT   = "/mnt/d/OneDrive/Desktop/Flensburg_Rundgang.docx"
MAP_FILE = "/tmp/flensburg_map.png"

ZOOM   = 15
IMG_W  = 900
IMG_H  = 720
# Karten-Mittelpunkt: leicht nördlich des Parkhauses damit alles passt
CTR_LAT = 54.7895
CTR_LON = 9.4308

STOPS = [
    {"nr": 1, "name": "Parkhaus Süderhofenden",      "lat": 54.7838, "lon": 9.4378,
     "color": "#6366f1", "dist": "—",     "zeit": "—",      "notiz": "Ausgangspunkt im Zentrum"},
    {"nr": 2, "name": "Südermarkt & Nikolaikirche",  "lat": 54.7832, "lon": 9.4355,
     "color": "#f59e0b", "dist": "350 m", "zeit": "4 Min",  "notiz": "Gotische Hallenkirche (14. Jh.), historischer Marktplatz"},
    {"nr": 3, "name": "Schifffahrts- & Rummuseum",   "lat": 54.7872, "lon": 9.4325,
     "color": "#f59e0b", "dist": "500 m", "zeit": "7 Min",  "notiz": "800 J. Seefahrt + Rum-Keller (Di–So 10–17, 8 €)"},
    {"nr": 4, "name": "Museumshafen",                "lat": 54.7890, "lon": 9.4308,
     "color": "#f59e0b", "dist": "250 m", "zeit": "3 Min",  "notiz": "Histor. Rahsegler & Schoner — Eintritt frei"},
    {"nr": 5, "name": "Hafenspitze (Kaffeepause)",   "lat": 54.7918, "lon": 9.4282,
     "color": "#0ea5e9", "dist": "400 m", "zeit": "5 Min",  "notiz": "Biergarten mit Förde-Panoramablick bis nach Dänemark"},
    {"nr": 6, "name": "Kaufmannshöfe Norderstr.",    "lat": 54.7905, "lon": 9.4325,
     "color": "#f59e0b", "dist": "550 m", "zeit": "7 Min",  "notiz": "18 histor. Innenhöfe (18. Jh.) — Norderstr. 86 empfohlen"},
    {"nr": 7, "name": "Nordermarkt & Neptunbrunnen", "lat": 54.7928, "lon": 9.4318,
     "color": "#f59e0b", "dist": "250 m", "zeit": "3 Min",  "notiz": "Ältester Markt (um 1200), Brunnen von 1758"},
    {"nr": 8, "name": "Nordertor",                   "lat": 54.7952, "lon": 9.4305,
     "color": "#ef4444", "dist": "300 m", "zeit": "4 Min",  "notiz": "Wahrzeichen Flensburgs — gotisches Stadttor von 1595"},
    {"nr": 9, "name": "Duburg-Ruine (Aussicht)",     "lat": 54.7940, "lon": 9.4238,
     "color": "#16a34a", "dist": "700 m", "zeit": "9 Min",  "notiz": "Mittelalterl. Burg (1411), Panorama über Flensburg & Förde"},
]

RETURN_ROW = ("→1", "Zurück zum Parkhaus", "1,1 km / 14 Min", "Durch die Innenstadt zurück")
TOTAL_ROW  = ("∑",  "Gesamt",              "~4,5 km",         "~56 Min reine Gehzeit (ohne Pausen)")


# ── Routing ───────────────────────────────────────────────────────────────────
def get_osrm_route():
    pts = STOPS + [STOPS[0]]
    coords = ";".join(f"{s['lon']},{s['lat']}" for s in pts)
    url = f"http://router.project-osrm.org/route/v1/foot/{coords}?geometries=geojson&overview=full"
    try:
        r = requests.get(url, timeout=25)
        d = r.json()
        if d.get("code") == "Ok":
            print("  OSRM: Straßenroute geladen")
            return [(c[0], c[1]) for c in d["routes"][0]["geometry"]["coordinates"]]
    except Exception as e:
        print(f"  OSRM fehlgeschlagen ({e}), nehme Luftlinien")
    return [(s["lon"], s["lat"]) for s in pts]


# ── Pixel-Koordinaten ──────────────────────────────────────────────────────────
def ll2px(lat, lon):
    def deg2t(la, lo):
        n = 2 ** ZOOM
        x = (lo + 180) / 360 * n
        y = (1 - math.log(math.tan(math.radians(la)) + 1 / math.cos(math.radians(la))) / math.pi) / 2 * n
        return x, y
    cx, cy = deg2t(CTR_LAT, CTR_LON)
    px, py = deg2t(lat, lon)
    return int((px - cx) * 256 + IMG_W / 2), int((py - cy) * 256 + IMG_H / 2)


# ── Karte ──────────────────────────────────────────────────────────────────────
def generate_map():
    m = StaticMap(IMG_W, IMG_H, url_template="https://tile.openstreetmap.org/{z}/{x}/{y}.png")

    route = get_osrm_route()
    m.add_line(Line(route, "#3b82f6", 4))

    # Kleine unsichtbare Marker damit StaticMap die Bounds kennt
    for s in STOPS:
        m.add_marker(CircleMarker((s["lon"], s["lat"]), "white", 1))

    img = m.render(zoom=ZOOM, center=(CTR_LON, CTR_LAT))
    draw = ImageDraw.Draw(img)

    try:
        font_nr  = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 15)
        font_hdr = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 12)
        font_sm  = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 11)
    except Exception:
        font_nr = font_hdr = font_sm = ImageFont.load_default()

    def draw_marker(x, y, text, hex_col):
        r = 15
        rgb = tuple(int(hex_col.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
        # Schwarzer Schatten-Ring für Kontrast
        draw.ellipse([x-r-2, y-r-2, x+r+2, y+r+2], fill=(20, 20, 20))
        draw.ellipse([x-r, y-r, x+r, y+r], fill=rgb)
        # Zentrierte Zahl
        bb = draw.textbbox((0, 0), text, font=font_nr)
        tw, th = bb[2]-bb[0], bb[3]-bb[1]
        draw.text((x - tw//2 - bb[0], y - th//2 - bb[1]), text, font=font_nr, fill="white")

    for s in STOPS:
        px, py = ll2px(s["lat"], s["lon"])
        draw_marker(px, py, str(s["nr"]), s["color"])

    # Legende
    lx, ly = 8, 8
    lh = 26 + len(STOPS) * 19 + 6
    draw.rectangle([lx, ly, lx+240, ly+lh], fill=(255, 255, 255), outline=(160, 160, 160))
    draw.text((lx+7, ly+6), "RUNDGANG FLENSBURG", font=font_hdr, fill=(20, 20, 20))
    for i, s in enumerate(STOPS):
        ry = ly + 26 + i * 19
        rgb = tuple(int(s["color"].lstrip('#')[j:j+2], 16) for j in (0, 2, 4))
        draw.ellipse([lx+7, ry+3, lx+22, ry+18], fill=rgb)
        nb = draw.textbbox((0, 0), str(s["nr"]), font=font_sm)
        nw, nh = nb[2]-nb[0], nb[3]-nb[1]
        draw.text((lx+14 - nw//2 - nb[0], ry+10 - nh//2 - nb[1]), str(s["nr"]), font=font_sm, fill="white")
        draw.text((lx+28, ry+3), s["name"][:30], font=font_sm, fill=(20, 20, 20))

    img.save(MAP_FILE, quality=92)
    print(f"  Karte: {MAP_FILE}")


# ── Word-Dokument ──────────────────────────────────────────────────────────────
def set_bg(cell, hex_color):
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), hex_color)
    tcPr.append(shd)


def cell_para(cell, text, size=9, bold=False, color=None):
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(1)
    p.paragraph_format.space_after  = Pt(1)
    if p.runs:
        run = p.runs[0]
    else:
        run = p.add_run()
    run.text = text
    run.font.size = Pt(size)
    run.font.bold = bold
    if color:
        run.font.color.rgb = color


def generate_doc():
    doc = Document()

    for sec in doc.sections:
        sec.top_margin    = Cm(1.5)
        sec.bottom_margin = Cm(1.5)
        sec.left_margin   = Cm(1.8)
        sec.right_margin  = Cm(1.8)

    # Titel
    t = doc.add_heading("Flensburg — Rundgang", 0)
    t.alignment = WD_ALIGN_PARAGRAPH.CENTER
    t.runs[0].font.size = Pt(17)
    t.runs[0].font.color.rgb = RGBColor(0x1e, 0x40, 0xaf)
    t.paragraph_format.space_before = Pt(0)
    t.paragraph_format.space_after  = Pt(2)

    # Untertitel
    sub = doc.add_paragraph("Donnerstag  ·  VW ID.3  ·  ~4,5 km  ·  ca. 3–4 Stunden mit Pausen")
    sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    sub.runs[0].font.size = Pt(9)
    sub.runs[0].font.color.rgb = RGBColor(0x64, 0x74, 0x8b)
    sub.paragraph_format.space_after = Pt(4)

    # Laden-Info
    p1 = doc.add_paragraph()
    r1 = p1.add_run("⚡ EnBW HPC 300 kW: BAUHAUS Schleswiger Str. 107–109 (2,5 km vor Zentrum) — weitere Stationen in der EnBW-App")
    r1.font.size = Pt(9); r1.font.bold = True
    r1.font.color.rgb = RGBColor(0x15, 0x80, 0x3d)
    p1.paragraph_format.space_after = Pt(2)

    p2 = doc.add_paragraph()
    r2 = p2.add_run("🅿  Parkhaus Süderhofenden — zentral, normale Parkgebühren, direkt am Startpunkt")
    r2.font.size = Pt(9)
    r2.font.color.rgb = RGBColor(0x44, 0x55, 0x6b)
    p2.paragraph_format.space_after = Pt(5)

    # Karte
    doc.add_picture(MAP_FILE, width=Inches(5.0))
    doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
    doc.paragraphs[-1].paragraph_format.space_after = Pt(6)

    # Tabelle (Route + Highlights kombiniert)
    tbl = doc.add_table(rows=1, cols=4)
    tbl.style = 'Table Grid'
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER

    # Tabellen-Layout auf fixed setzen
    tblPr = tbl._tbl.find(qn('w:tblPr'))
    if tblPr is None:
        tblPr = OxmlElement('w:tblPr')
        tbl._tbl.insert(0, tblPr)
    tblLayout = OxmlElement('w:tblLayout')
    tblLayout.set(qn('w:type'), 'fixed')
    tblPr.append(tblLayout)

    # Spaltenbreiten: 0.7 | 4.5 | 2.2 | 9.7 = 17.1 cm
    COL_W = [Cm(0.7), Cm(4.5), Cm(2.2), Cm(9.7)]

    hdr = tbl.rows[0].cells
    for i, (txt, w) in enumerate(zip(["#", "Station", "↔ / ⏱", "Highlight"], COL_W)):
        hdr[i].width = w
        cell_para(hdr[i], txt, size=9, bold=True, color=RGBColor(0xff, 0xff, 0xff))
        set_bg(hdr[i], "1e40af")

    rows_data = []
    for s in STOPS:
        if s["nr"] == 1:
            dt = "Start"
        else:
            dt = f"{s['dist']} / {s['zeit']}"
        rows_data.append((str(s["nr"]), s["name"], dt, s["notiz"]))
    rows_data.append(RETURN_ROW)
    rows_data.append(TOTAL_ROW)

    for i, (nr, name, dist, notiz) in enumerate(rows_data):
        row = tbl.add_row().cells
        is_total = (i == len(rows_data) - 1)
        for j, (cell, w) in enumerate(zip(row, COL_W)):
            cell.width = w
        cell_para(row[0], nr,     bold=is_total)
        cell_para(row[1], name,   bold=is_total)
        cell_para(row[2], dist,   bold=is_total)
        cell_para(row[3], notiz,  bold=is_total)
        if is_total:
            for cell in row:
                set_bg(cell, "dbeafe")
        elif i % 2 == 1:
            for cell in row:
                set_bg(cell, "f0f5ff")

    # Footer
    foot = doc.add_paragraph("Bolla · Flensburg Ausflug · Viel Spaß! 🐾")
    foot.alignment = WD_ALIGN_PARAGRAPH.CENTER
    foot.runs[0].font.size = Pt(8)
    foot.runs[0].font.color.rgb = RGBColor(0x94, 0xa3, 0xb8)
    foot.paragraph_format.space_before = Pt(4)

    doc.save(OUTPUT)
    print(f"  Word: {OUTPUT}")


if __name__ == "__main__":
    print("Generiere Karte...")
    generate_map()
    print("Erstelle Word-Dokument...")
    generate_doc()
    print("Fertig!")
