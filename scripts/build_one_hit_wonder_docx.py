"""Erzeugt 'Top 50 One-Hit-Wonder (Deutschland)' als 1-Seiten-Word-Datei.
Quellen: de.wikipedia.org/wiki/One-Hit-Wonder (Listen nach Jahr), taschenhirn.de (Ergänzung).
Nur Titel/Interpret/Jahr, die dort so stehen — keine eigenen Zusatzbehauptungen."""
import sys
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

OUT = sys.argv[1] if len(sys.argv) > 1 else "Top_50_One-Hit-Wonder_Deutschland.docx"

# (Jahr, Titel, Interpret)
SONGS = [
    (1962, "Telstar", "The Tornados"),
    (1967, "San Francisco", "Scott McKenzie"),
    (1969, "In the Year 2525", "Zager and Evans"),
    (1970, "Spirit in the Sky", "Norman Greenbaum"),
    (1974, "Hooked on a Feeling", "Blue Swede"),
    (1976, "Disco Duck", "Rick Dees"),
    (1977, "Ça plane pour moi", "Plastic Bertrand"),
    (1977, "Magic Fly", "Space"),
    (1977, "Black Betty", "Ram Jam"),
    (1977, "Porque te vas", "Jeanette"),
    (1979, "Ring My Bell", "Anita Ward"),
    (1979, "Video Killed the Radio Star", "The Buggles"),
    (1979, "Funkytown", "Lipps, Inc."),
    (1979, "Das Lied von Manuel", "Pony"),
    (1979, "My Sharona", "The Knack"),
    (1981, "Eisbär", "Grauzone"),
    (1983, "Der Knutschfleck", "Ixi"),
    (1983, "Die Sennerin vom Königsee", "Kiz"),
    (1984, "One Night in Bangkok", "Murray Head"),
    (1985, "Comanchero", "Raggio di Luna"),
    (1985, "St. Elmo's Fire", "John Parr"),
    (1986, "Resi, i hol di mit mei'm Traktor ab", "Wolfgang Fierek"),
    (1986, "My Favourite Waste of Time", "Owen Paul"),
    (1986, "J'aime la vie", "Sandra Kim"),
    (1987, "Ich liebe dich", "Clowns & Helden"),
    (1987, "Voyage, voyage", "Desireless"),
    (1987, "Lean on Me", "Club Nouveau"),
    (1987, "Pump Up the Volume", "M/A/R/R/S"),
    (1988, "Go for Gold", "The Winners"),
    (1990, "Pump ab das Bier", "Werner Wichtig"),
    (1990, "Beinhart", "Torfrock"),
    (1992, "Baby Got Back", "Sir Mix-a-Lot"),
    (1994, "Doop", "Doop"),
    (1995, "Alice, Who the X Is Alice?", "Gompie"),
    (1996, "Macarena", "Los del Río"),
    (1997, "Freed from Desire", "Gala"),
    (1997, "Tic, Tic Tac", "Chili & Carrapicho"),
    (1998, "Big Big World", "Emilia"),
    (1999, "Mambo No. 5", "Lou Bega"),
    (1999, "Flat Beat", "Mr Oizo"),
    (2002, "The Ketchup Song", "Las Ketchup"),
    (2004, "Dragostea din tei", "Haiducii"),
    (2008, "Kleiner Hai", "Alemuel"),
    (2010, "Stereo Love", "Edward Maya & Vika Jigulina"),
    (2011, "Somebody That I Used to Know", "Gotye feat. Kimbra"),
    (2012, "Gangnam Style", "Psy"),
    (2013, "Harlem Shake", "Baauer"),
    (2013, "The Fox", "Ylvis"),
    (2014, "I'm an Albatraoz", "AronChupa"),
    (2021, "Wellerman", "Nathan Evans"),
]
assert len(SONGS) == 50, len(SONGS)

FONT = "Aptos"
ACCENT = RGBColor(0x1F, 0x3A, 0x5F)

doc = Document()
sec = doc.sections[0]
sec.page_width, sec.page_height = Cm(21.0), Cm(29.7)
sec.left_margin = sec.right_margin = Cm(1.6)
sec.top_margin, sec.bottom_margin = Cm(1.4), Cm(1.2)

normal = doc.styles["Normal"]
normal.font.name = FONT
normal.font.size = Pt(9)
normal.element.rPr.rFonts.set(qn("w:eastAsia"), FONT)
pf = normal.paragraph_format
pf.space_after = Pt(0)
pf.space_before = Pt(0)
pf.line_spacing = 1.15


def run(p, text, size=None, bold=False, italic=False, color=None):
    r = p.add_run(text)
    r.font.name = FONT
    r._element.rPr.rFonts.set(qn("w:eastAsia"), FONT)
    if size:
        r.font.size = Pt(size)
    r.bold = bold
    r.italic = italic
    if color:
        r.font.color.rgb = color
    return r


p = doc.add_paragraph()
run(p, "Die 50 bekanntesten One-Hit-Wonder", 17, bold=True, color=ACCENT)
p = doc.add_paragraph()
run(p, "Einmal-Hits, die auch in Deutschland ein Begriff sind — zusammengestellt am 25.09.2026", 9.5, italic=True)
p.paragraph_format.space_after = Pt(6)

tbl = doc.add_table(rows=25, cols=6)
tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
tbl.autofit = False
widths = [Cm(0.8), Cm(1.1), Cm(6.6), Cm(0.8), Cm(1.1), Cm(6.6)]


def shade(cell, hexcolor):
    tcPr = cell._element.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), hexcolor)
    tcPr.append(shd)


def fill(cells, n, song):
    year, title, artist = song
    c_nr, c_year, c_txt = cells
    p1 = c_nr.paragraphs[0]
    p1.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    run(p1, f"{n}.", 9, bold=True, color=ACCENT)
    p2 = c_year.paragraphs[0]
    run(p2, str(year), 9)
    p3 = c_txt.paragraphs[0]
    run(p3, title, 9.5, bold=True)
    p3.add_run().add_break()
    run(p3, artist, 8.5, color=RGBColor(0x55, 0x55, 0x55))


for i in range(25):
    row = tbl.rows[i]
    for j, w in enumerate(widths):
        row.cells[j].width = w
    fill(row.cells[0:3], i + 1, SONGS[i])
    fill(row.cells[3:6], i + 26, SONGS[i + 25])
    if i % 2 == 0:
        for c in row.cells:
            shade(c, "F2F5F9")
    # Zeilen nicht umbrechen lassen
    trPr = row._tr.get_or_add_trPr()
    cant = OxmlElement("w:cantSplit")
    trPr.append(cant)

p = doc.add_paragraph()
p.paragraph_format.space_before = Pt(6)
run(p, "Hinweis: ", 8, bold=True)
run(p, "Es gibt keine offizielle Rangliste der One-Hit-Wonder — die Liste ist daher chronologisch "
       "sortiert, nicht nach Rang. Auswahl nach Bekanntheit in Deutschland (Bolla). "
       "Titel, Interpret und Jahr nach den One-Hit-Wonder-Listen von Wikipedia bzw. taschenhirn.de.", 8)

doc.save(OUT)
print("OK", OUT)
