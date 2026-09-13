#!/usr/bin/env python3
"""
Opern-Infoblatt-Generator  🐾
Erzeugt eine einseitige Übersichtsseite zu einer Oper im "Freischütz/Barbier"-Stil.

Bedienung: Den OPER-Datenblock unten ausfüllen, dann:
    python3 opern_infoblatt.py

Speichert nach:
  - /mnt/d/OneDrive/Dokumente/Allgemeines/Freizeit/<Datei>.docx
  - /mnt/d/OneDrive/Desktop/<Datei>.docx

Design-DNA (aus Freischuetz_Infoseite.docx abgeleitet):
  Cambria · US-Letter · Rand 2/2/0.75/0.75 cm · Titel 26pt bold Akzentfarbe
  Untertitel 10pt grau · 2-Spalten-Boxen mit weißer Headerleiste auf Akzentfarbe
  Labels bold/Akzent, Fließtext 333333 · Handlung-Leiste · Akt-Überschriften + Bullets
  Pro Oper eine eigene Akzentfarbe (Hex ohne #).
"""
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

# ============================== OPER-DATENBLOCK ==============================
OPER = {
    "datei":    "Don_Giovanni_Infoseite",
    "titel":    "Don Giovanni",
    "untertitel": "Dramma giocoso in zwei Akten  ·  Wolfgang Amadeus Mozart (1787)",
    "akzent":   "7A0C2E",   # dunkles Weinrot — Verführung, Blut, Höllenfahrt (Hex ohne #). Pro Oper eigene Farbe.
    "info": [
        ("Komponist:", "Wolfgang Amadeus Mozart (1756–1791)"),
        ("Originaltitel:", "Il dissoluto punito, ossia il Don Giovanni"),
        ("Libretto:", "Lorenzo Da Ponte"),
        ("Uraufführung:", "29. Oktober 1787, Ständetheater Prag"),
        ("Spieldauer:", "ca. 3 Stunden (mit Pause)"),
        ("Gattung:", "Dramma giocoso — Mischung aus Komödie und Tragödie"),
    ],
    "personen": [
        ("Don Giovanni (Bariton):", "Skrupelloser Verführer und Titelheld — kennt keine Reue"),
        ("Leporello (Bass):", "Sein Diener — führt widerwillig Buch über seine Eroberungen"),
        ("Il Commendatore (Bass):", "Donna Annas Vater — von Don Giovanni im Duell getötet"),
        ("Donna Anna (Sopran):", "Tochter des Komturs — schwört Rache für seinen Tod"),
        ("Don Ottavio (Tenor):", "Donna Annas Verlobter — steht treu an ihrer Seite"),
        ("Donna Elvira (Sopran):", "Von Don Giovanni verlassene Frau — verfolgt ihn aus verletztem Stolz"),
        ("Zerlina (Sopran):", "Junge Bäuerin — wird am eigenen Hochzeitstag umworben"),
        ("Masetto (Bass):", "Zerlinas Bräutigam"),
    ],
    "akte": [
        ("1. Akt", [
            "Leporello hält Wache, während Don Giovanni versucht, Donna Anna zu verführen. Sie wehrt sich, ihr Vater, der Komtur, eilt herbei und fordert ihn zum Duell — und stirbt.",
            "Donna Anna und ihr Verlobter Don Ottavio schwören Rache am unbekannten Mörder.",
            "Don Giovanni trifft die von ihm verlassene Donna Elvira wieder. Leporello klärt sie mit der berühmten „Registerarie“ über die schier endlose Liste der Eroberungen seines Herrn auf.",
            "Auf dem Land feiert die Bäuerin Zerlina ihre Hochzeit mit Masetto. Don Giovanni umgarnt sie („Là ci darem la mano“), wird aber von der eifersüchtigen Donna Elvira gestört.",
            "Bei einem Fest auf seinem Schloss versucht Don Giovanni erneut, sich an Zerlina heranzumachen. Als Donna Anna, Ottavio und Elvira maskiert erscheinen, um ihn zu stellen, entkommt er im Tumult.",
        ]),
        ("2. Akt", [
            "Don Giovanni tauscht mit Leporello die Kleider, um Donna Elviras Zofe zu verführen — Leporello muss in seiner Rolle die verzweifelte Elvira ablenken.",
            "Als „Leporello“ verkleidet, singt Don Giovanni sein Ständchen „Deh, vieni alla finestra“ — wird aber von Masetto und aufgebrachten Bauern gestellt und verprügelt Masetto in der Verwirrung.",
            "Der echte Leporello wird enttarnt und kann fliehen.",
            "Auf dem Friedhof begegnet Don Giovanni der steinernen Statue des ermordeten Komturs und lädt sie frech zum Essen ein — die Statue nickt zustimmend.",
            "Beim Abendmahl erscheint die Statue tatsächlich und fordert Don Giovanni zur Reue auf. Er weigert sich trotz aller Warnungen — und wird von den Flammen der Hölle verschlungen.",
            "Im Epilog berichten die Überlebenden, wie es mit ihnen weitergeht: Moral der Geschichte — so endet, wer Böses tut.",
        ]),
    ],
    "musik": [
        ("Ouvertüre:", "Dramatisch-düster — nimmt die Höllenfahrt-Szene des Finales musikalisch vorweg"),
        ("„Madamina, il catalogo è questo“:", "Leporellos berühmte Register-/Katalogarie (1. Akt)"),
        ("„Là ci darem la mano“:", "Verführerisches Duett Don Giovanni–Zerlina"),
        ("„Deh, vieni alla finestra“:", "Don Giovannis Ständchen mit Mandolinenbegleitung (2. Akt)"),
        ("Finale 2. Akt:", "Die Commendatore-Szene — Don Giovannis Höllenfahrt"),
    ],
    "bedeutung": [
        "Don Giovanni gilt neben „Figaros Hochzeit“ und „Così fan tutte“ als eine der drei großen Da-Ponte-Opern Mozarts und als Gipfelwerk der Gattung „dramma giocoso“ — der Verschmelzung von Komödie und Tragödie.",
        "E.T.A. Hoffmann nannte sie später die „Oper aller Opern“. Die unersättliche, bis zuletzt unbeugsame Titelfigur wurde weit über die Musikwelt hinaus zum kulturellen Mythos des Verführers Don Juan.",
    ],
}
# ===========================================================================

FONT = "Cambria"
GRAY = RGBColor(0x77, 0x77, 0x77)
BODY = RGBColor(0x33, 0x33, 0x33)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)


def build(oper):
    accent = oper["akzent"].upper()
    acc_rgb = RGBColor(int(accent[0:2], 16), int(accent[2:4], 16), int(accent[4:6], 16))

    d = Document()
    sec = d.sections[0]
    sec.page_width, sec.page_height = Cm(21.59), Cm(27.94)
    sec.left_margin = sec.right_margin = Cm(2)
    sec.top_margin = sec.bottom_margin = Cm(0.75)
    st = d.styles['Normal']
    st.font.name = FONT
    st.font.size = Pt(10)
    st._element.rPr.rFonts.set(qn('w:eastAsia'), FONT)

    def run_fmt(r, size=10, bold=False, color=BODY, fill=None):
        r.font.name = FONT
        r.font.size = Pt(size)
        r.font.bold = bold
        r.font.color.rgb = color
        if fill:
            rpr = r._r.get_or_add_rPr()
            shd = OxmlElement('w:shd')
            shd.set(qn('w:val'), 'clear')
            shd.set(qn('w:color'), 'auto')
            shd.set(qn('w:fill'), fill)
            rpr.append(shd)

    # Titel + Untertitel
    p = d.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(0)
    run_fmt(p.add_run(oper["titel"]), 26, True, acc_rgb)
    p = d.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(8)
    run_fmt(p.add_run(oper["untertitel"]), 10, False, GRAY)

    def style_table(t):
        t.style = 'Table Grid'
        borders = OxmlElement('w:tblBorders')
        for edge in ('top', 'left', 'bottom', 'right', 'insideH', 'insideV'):
            e = OxmlElement('w:' + edge); e.set(qn('w:val'), 'none')
            borders.append(e)
        t._tbl.tblPr.append(borders)
        t.columns[0].width = t.columns[1].width = Cm(8.79)
        for c in t.rows[0].cells:
            c.width = Cm(8.79)

    def header_bar(para, text):
        para.paragraph_format.space_after = Pt(3)
        run_fmt(para.add_run("  " + text + "  "), 10, True, WHITE, fill=accent)

    def fill_cell_rows(cell, header, rows):
        cell.paragraphs[0].text = ''
        header_bar(cell.paragraphs[0], header)
        for label, value in rows:
            bp = cell.add_paragraph()
            bp.paragraph_format.space_after = Pt(1)
            bp.paragraph_format.line_spacing = 1.0
            if label:
                run_fmt(bp.add_run(label + " "), 10, True, acc_rgb)
            run_fmt(bp.add_run(value), 10, False, BODY)

    def fill_cell_text(cell, header, paras):
        cell.paragraphs[0].text = ''
        header_bar(cell.paragraphs[0], header)
        for para in paras:
            bp = cell.add_paragraph()
            bp.paragraph_format.space_after = Pt(4)
            bp.paragraph_format.line_spacing = 1.0
            run_fmt(bp.add_run(para), 10, False, BODY)

    # Box 1: Infos | Personen
    tA = d.add_table(rows=1, cols=2); style_table(tA)
    fill_cell_rows(tA.rows[0].cells[0], "Allgemeine Informationen", oper["info"])
    fill_cell_rows(tA.rows[0].cells[1], "Personen", oper["personen"])

    d.add_paragraph().paragraph_format.space_after = Pt(2)

    # Handlung-Leiste
    hb = d.add_paragraph()
    hb.paragraph_format.space_before = Pt(4); hb.paragraph_format.space_after = Pt(4)
    run_fmt(hb.add_run("  Handlung  "), 14, True, WHITE, fill=accent)

    for titel, bullets in oper["akte"]:
        ap = d.add_paragraph()
        ap.paragraph_format.space_before = Pt(4); ap.paragraph_format.space_after = Pt(2)
        run_fmt(ap.add_run(titel), 11, True, acc_rgb)
        for b in bullets:
            bp = d.add_paragraph(style='List Bullet')
            bp.paragraph_format.space_after = Pt(2); bp.paragraph_format.line_spacing = 1.0
            run_fmt(bp.add_run(b), 10, False, BODY)

    d.add_paragraph().paragraph_format.space_after = Pt(2)

    # Box 2: Musik | Bedeutung
    tB = d.add_table(rows=1, cols=2); style_table(tB)
    fill_cell_rows(tB.rows[0].cells[0], "Berühmte Musiknummern", oper["musik"])
    fill_cell_text(tB.rows[0].cells[1], "Bedeutung", oper["bedeutung"])

    return d


if __name__ == "__main__":
    import shutil
    d = build(OPER)
    freizeit = f"/mnt/d/OneDrive/Dokumente/Allgemeines/Freizeit/{OPER['datei']}.docx"
    desktop = f"/mnt/d/OneDrive/Desktop/{OPER['datei']}.docx"
    d.save(freizeit)
    shutil.copy(freizeit, desktop)
    print("Gespeichert:", freizeit)
    print("Auf Desktop:", desktop)
