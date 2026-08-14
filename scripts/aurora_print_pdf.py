#!/usr/bin/env python3
"""
AURORA — Taschenbuch-Innenteil als druckfertiges PDF (KDP Paperback).
Aus derselben JSON wie das EPUB (keine Hartkodierung).

Format: 5x8" (127x203.2mm), EB Garamond 11.5pt, Blocksatz mit pyphen-Silbentrennung,
gespiegelte Ränder (Bundsteg), Kolumnentitel + Seitenzahlen ab Vorwort.

Aufruf:
  python3 aurora_print_pdf.py de   -> AURORA_innenteil_de.pdf
  python3 aurora_print_pdf.py en   -> AURORA_innenteil_en.pdf
"""
import sys, re, html
from pathlib import Path
import pyphen
from reportlab.lib.units import mm
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_LEFT
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame,
                                Paragraph, Spacer, PageBreak, FrameBreak)
from reportlab.platypus.doctemplate import NextPageTemplate

# ---------------------------------------------------------------- Konfiguration
LANG = (sys.argv[1] if len(sys.argv) > 1 else "de").lower()
CFG = {
    "de": dict(json="/home/bolla/workspace/data/ki_buch.json",
               out="/mnt/d/OneDrive/Dokumente/Bolla/AURORA/3_Taschenbuch/1_DE_Innenteil.pdf",
               hyph="de_DE", autor="Chris Mandel",
               t_epilog="Epilog", t_autor="Über den Autor",
               t_dank="Danksagung", t_rezension=None,
               t_prolog="Prolog", t_vorwort="Vorwort"),
    "en": dict(json="/home/bolla/workspace/data/ki_buch_en_adapted.json",
               out="/mnt/d/OneDrive/Dokumente/Bolla/AURORA/3_Taschenbuch/3_EN_Innenteil.pdf",
               hyph="en_US", autor="Chris Mandel",
               t_epilog="Epilogue", t_autor="About the Author",
               t_dank="Acknowledgements", t_rezension=None,
               t_prolog="Prologue", t_vorwort="Preface"),
}[LANG]

import json
D = json.loads(Path(CFG["json"]).read_text())
TITEL = D.get("titel", "AURORA")

# ---------------------------------------------------------------- Schrift
FB = "/home/bolla/workspace/fonts/ebgaramond"
pdfmetrics.registerFont(TTFont("EBG",   f"{FB}/EBGaramond-Regular.ttf"))
pdfmetrics.registerFont(TTFont("EBG-I", f"{FB}/EBGaramond-Italic.ttf"))
pdfmetrics.registerFont(TTFont("EBG-B", f"{FB}/EBGaramond-Bold.ttf"))
pdfmetrics.registerFont(TTFont("EBG-BI",f"{FB}/EBGaramond-BoldItalic.ttf"))
pdfmetrics.registerFontFamily("EBG", normal="EBG", bold="EBG-B",
                              italic="EBG-I", boldItalic="EBG-BI")

# ---------------------------------------------------------------- Silbentrennung
_dic = pyphen.Pyphen(lang=CFG["hyph"])
SHY = "­"
def hyphenate(text):
    """Soft-Hyphens in Wörter >= 5 Buchstaben einfügen (reportlab trennt daran)."""
    def repl(m):
        w = m.group(0)
        return _dic.inserted(w, hyphen=SHY) if len(w) >= 6 else w
    return re.sub(r"[A-Za-zÀ-ÿ]+", repl, text)

def md_inline(text):
    """*em* -> <i>, escape, dann Silbentrennung. Erhält reportlab-Markup-Sicherheit."""
    text = html.escape(text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"\*(.+?)\*", r"<i>\1</i>", text)
    # Silbentrennung nur auf Textteile, nicht auf Tags: split an < >
    out, i = [], 0
    for part in re.split(r"(<[^>]+>)", text):
        out.append(part if part.startswith("<") else hyphenate(part))
    return "".join(out)

# ---------------------------------------------------------------- Seitenmaße
PW, PH = 127*mm, 203.2*mm           # 5 x 8 Zoll
M_TOP, M_BOT = 16*mm, 17*mm
M_GUT, M_OUT = 19*mm, 13*mm         # Bundsteg innen / außen
FW = PW - M_GUT - M_OUT
FH = PH - M_TOP - M_BOT

# ---------------------------------------------------------------- Stile
body = ParagraphStyle("body", fontName="EBG", fontSize=11.5, leading=15.5,
                      alignment=TA_JUSTIFY, firstLineIndent=5*mm,
                      spaceBefore=0, spaceAfter=0, hyphenationLang=CFG["hyph"])
body0 = ParagraphStyle("body0", parent=body, firstLineIndent=0)   # 1. Absatz
scene = ParagraphStyle("scene", parent=body, alignment=TA_CENTER,
                       firstLineIndent=0, spaceBefore=6, spaceAfter=6)
chno  = ParagraphStyle("chno", fontName="EBG", fontSize=11, leading=14,
                       alignment=TA_CENTER, textColor="#777777", spaceAfter=2)
chtit = ParagraphStyle("chtit", fontName="EBG-B", fontSize=18, leading=22,
                       alignment=TA_CENTER, spaceAfter=14)
# Titelei
t_main = ParagraphStyle("t_main", fontName="EBG-B", fontSize=40, leading=46,
                        alignment=TA_CENTER)
t_sub  = ParagraphStyle("t_sub", fontName="EBG-I", fontSize=15, leading=20,
                        alignment=TA_CENTER, textColor="#333333")
t_auth = ParagraphStyle("t_auth", fontName="EBG", fontSize=14, leading=18,
                        alignment=TA_CENTER)
t_half = ParagraphStyle("t_half", fontName="EBG", fontSize=22, leading=28,
                        alignment=TA_CENTER, textColor="#555555")
impr   = ParagraphStyle("impr", fontName="EBG", fontSize=9.5, leading=13,
                        alignment=TA_CENTER, textColor="#333333")
headword = ParagraphStyle("headword", fontName="EBG-I", fontSize=20, leading=26,
                          alignment=TA_LEFT, spaceAfter=10)
vorspann = ParagraphStyle("vorspann", fontName="EBG-I", fontSize=12.5, leading=18,
                          alignment=TA_LEFT, textColor="#222222")
secttit = ParagraphStyle("secttit", fontName="EBG-B", fontSize=20, leading=26,
                         alignment=TA_CENTER, spaceAfter=16)
# Zwischenüberschrift im Vorwort (## ...)
subhead = ParagraphStyle("subhead", fontName="EBG-B", fontSize=12.5, leading=16,
                         alignment=TA_LEFT, firstLineIndent=0,
                         spaceBefore=12, spaceAfter=3)

# ---------------------------------------------------------------- Flowable-Bau
def paras(text, style_first=body0, style_rest=body):
    """JSON-Text -> Liste von Paragraphs. '---' = Szenentrenner. *em* = kursiv."""
    flow, first = [], True
    for blk in re.split(r"\n{2,}", text.strip()):
        blk = blk.strip()
        if not blk:
            continue
        if blk == "---":
            flow.append(Paragraph("✳", scene)); first = True; continue
        if blk.startswith("## "):
            flow.append(Paragraph(md_inline(blk[3:].strip()), subhead))
            first = True; continue   # 1. Absatz nach Zwischenüberschrift bündig
        blk = blk.replace("\n", "<br/>")
        flow.append(Paragraph(md_inline(blk), style_first if first else style_rest))
        first = False
    return flow

story = []

def new_page(): story.append(PageBreak())

# --- Schmutztitel (S.1)
story += [Spacer(1, FH*0.32), Paragraph(html.escape(TITEL), t_half)]
new_page()
# --- Haupttitel (S.2)
story += [Spacer(1, FH*0.22), Paragraph(html.escape(TITEL), t_main),
          Spacer(1, 8*mm), Paragraph(html.escape(D.get("untertitel","")), t_sub),
          Spacer(1, FH*0.30), Paragraph(html.escape(CFG["autor"]), t_auth)]
new_page()
# --- Impressum (S.3)
story += [Spacer(1, FH*0.30)]
for ln in re.split(r"\n{2,}", D.get("impressum","").strip()):
    story.append(Paragraph(html.escape(ln.strip()).replace("\n","<br/>"), impr))
    story.append(Spacer(1, 5))
new_page()
# --- Vorwort (mit Überschrift)
story.append(Spacer(1, FH*0.10))
story.append(Paragraph(html.escape(CFG["t_vorwort"]), secttit))
story += paras(D.get("vorwort",""))
new_page()
# --- Vorspann / Definition (eigene Seite direkt vor dem Prolog)
vs = D.get("vorspann","").strip()
vs_parts = re.split(r"\n{2,}", vs)
story += [Spacer(1, FH*0.22)]
if vs_parts:
    story.append(Paragraph(html.escape(vs_parts[0].strip()), headword))
    for p in vs_parts[1:]:
        story.append(Paragraph(html.escape(p.strip()).replace("\n","<br/>"), vorspann))
        story.append(Spacer(1, 6))
new_page()

# --- Kapitel
kap = D.get("kapitel", [])
for idx, k in enumerate(kap):
    titel = k.get("titel", f"Kapitel {idx}")
    label = CFG["t_prolog"] if (idx == 0 and titel.lower() in ("prolog","prologue")) else f"{idx}"
    story.append(Spacer(1, FH*0.10))
    if idx == 0 and titel.lower() in ("prolog","prologue"):
        story.append(Paragraph(html.escape(titel), chtit))
    else:
        story.append(Paragraph(label, chno))
        story.append(Paragraph(html.escape(titel), chtit))
    _txt = k.get("text","")
    _lines = _txt.lstrip().split('\n', 1)
    if _lines and _lines[0].strip().strip('*').strip() == titel.strip():
        _txt = _lines[1].lstrip('\n') if len(_lines) > 1 else ''
    story += paras(_txt)
    new_page()

# --- Epilog
story.append(Spacer(1, FH*0.10))
story.append(Paragraph(html.escape(CFG["t_epilog"]), chtit))
if D.get("epilog_untertitel"):
    story.append(Paragraph("<i>"+html.escape(D["epilog_untertitel"])+"</i>", t_sub))
    story.append(Spacer(1, 10))
story += paras(D.get("epilog",""))
new_page()

# --- Backmatter
def section(title, key):
    if not D.get(key): return
    story.append(Spacer(1, FH*0.10))
    story.append(Paragraph(html.escape(title), secttit))
    story.extend(paras(D[key]))
    new_page()

section(CFG["t_autor"], "ueber_autor")
section(CFG["t_dank"], "danksagung")
# Rezensions-Bitte (eigener Titel je Sprache)
if D.get("rezensions_bitte"):
    story.append(Spacer(1, FH*0.18))
    story += paras(D["rezensions_bitte"])

# ---------------------------------------------------------------- Seitenrahmen
FOLIO_FROM = 4   # Titelei (Schmutztitel/Haupttitel/Impressum, S.1-3) ohne Kopf-/Fußzeile
def draw_footer(canvas, doc, with_header):
    pg = doc.page
    if pg < FOLIO_FROM:
        return
    canvas.saveState()
    canvas.setFont("EBG", 10)
    canvas.drawCentredString(PW/2, 9*mm, str(pg))
    if with_header:
        canvas.setFont("EBG", 9)
        canvas.setFillColor("#666666")
        if pg % 2 == 0:   # linke Seite
            canvas.drawString(M_OUT, PH-11*mm, CFG["autor"])
        else:             # rechte Seite
            canvas.drawRightString(PW-M_OUT, PH-11*mm, TITEL)
    canvas.restoreState()

def f_flow(c, d):  draw_footer(c, d, True)

# Frames: gespiegelt (rechte/ungerade Seite Bund links; linke/gerade Bund rechts)
frame_right = Frame(M_GUT, M_BOT, FW, FH, id="r",
                    leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
frame_left  = Frame(M_OUT, M_BOT, FW, FH, id="l",
                    leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)

class BookDoc(BaseDocTemplate):
    def handle_pageBegin(self):
        self._handle_pageBegin()
        # nächste Seite: Parität bestimmt Bundseite
        self._handle_nextPageTemplate("L" if self.page % 2 == 1 else "R")

doc = BookDoc(CFG["out"], pagesize=(PW, PH),
              title=TITEL, author=CFG["autor"])
doc.addPageTemplates([
    PageTemplate(id="R", frames=[frame_right], onPage=f_flow),  # ungerade/rechts (Default S.1)
    PageTemplate(id="L", frames=[frame_left],  onPage=f_flow),  # gerade/links
])

doc.build(story)
print(f"✅ {CFG['out']}  ({LANG.upper()})")
