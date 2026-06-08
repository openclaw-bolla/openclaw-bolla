#!/usr/bin/env python3
"""Erzeugt schön lesbare Roman-PDFs auf dem OneDrive-Desktop.
Große, ruhige Schrift (Chris, 70, künstliche Linsen). Dunkle Schrift auf hellem Grund.
Erzeugt: (1) komplettes Buch (Prolog–letztes Kapitel), (2) die zuletzt geschriebenen Kapitel."""

import json, re, datetime, sys
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, PageBreak,
                                HRFlowable, KeepTogether)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY

DESK = "/mnt/d/OneDrive/Desktop"
BOOK = "/home/bolla/workspace/data/ki_buch.json"

INK    = colors.HexColor('#1a1a1a')
SOFT   = colors.HexColor('#555555')
ACCENT = colors.HexColor('#7a2e4a')
RULE   = colors.HexColor('#cccccc')

d = json.load(open(BOOK, encoding="utf-8"))
ALLK = d['kapitel']
today = datetime.date.today().strftime("%d.%m.%Y")

body = ParagraphStyle('body', fontName='Times-Roman', fontSize=13, leading=20,
                      alignment=TA_JUSTIFY, textColor=INK, spaceAfter=10)
scene = ParagraphStyle('scene', fontName='Times-Bold', fontSize=11.5, leading=16,
                       textColor=ACCENT, spaceBefore=14, spaceAfter=8, alignment=TA_LEFT)
chap = ParagraphStyle('chap', fontName='Times-Bold', fontSize=20, leading=26,
                      textColor=INK, spaceBefore=6, spaceAfter=4, alignment=TA_LEFT)
chapnum = ParagraphStyle('chapnum', fontName='Times-Italic', fontSize=12, leading=16,
                         textColor=SOFT, spaceAfter=18, alignment=TA_LEFT)
title = ParagraphStyle('title', fontName='Times-Bold', fontSize=34, leading=40,
                       textColor=INK, alignment=TA_CENTER, spaceAfter=6)
subtitle = ParagraphStyle('subtitle', fontName='Times-Italic', fontSize=15, leading=22,
                          textColor=SOFT, alignment=TA_CENTER, spaceAfter=30)
small = ParagraphStyle('small', fontName='Times-Italic', fontSize=10.5, leading=15,
                       textColor=SOFT, alignment=TA_CENTER)

def esc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

def render_chapter(flow, k):
    titel = k.get('titel', 'Kapitel')
    if ":" in titel:
        nr, _, name = titel.partition(":")
        head = [Paragraph(esc(name.strip()), chap), Paragraph(esc(nr.strip()), chapnum)]
    else:
        head = [Paragraph(esc(titel), chap), Spacer(1, 6)]
    head.append(HRFlowable(width="100%", thickness=0.8, color=RULE, spaceAfter=14))
    flow.append(KeepTogether(head))
    for raw in k.get('text', '').split("\n"):
        line = raw.strip()
        if not line:
            continue
        if line == "---":
            flow.append(Spacer(1, 6))
            flow.append(HRFlowable(width="22%", thickness=0.8, color=RULE,
                                   spaceBefore=6, spaceAfter=10, hAlign='CENTER'))
            continue
        if line.startswith("**") and line.endswith("**"):
            flow.append(Paragraph(esc(line.strip("*").strip()), scene))
            continue
        txt = re.sub(r'\*(.+?)\*', r'<i>\1</i>', esc(line))
        flow.append(Paragraph(txt, body))
    flow.append(PageBreak())

def build(out, kapitel, untertitel_zeile):
    doc = SimpleDocTemplate(out, pagesize=A4,
        leftMargin=2.4*cm, rightMargin=2.4*cm, topMargin=2.2*cm, bottomMargin=2.0*cm,
        title="AURORA", author="Bolla für Chris")
    flow = []
    flow.append(Spacer(1, 3.5*cm))
    flow.append(Paragraph("AURORA", title))
    flow.append(Paragraph("Was bleibt, wenn die Maschinen träumen", subtitle))
    flow.append(HRFlowable(width="40%", thickness=1, color=RULE, spaceBefore=4, spaceAfter=24, hAlign='CENTER'))
    flow.append(Paragraph(untertitel_zeile, ParagraphStyle('k', parent=chap, alignment=TA_CENTER)))
    flow.append(Spacer(1, 0.6*cm))
    flow.append(Paragraph(f"Stand {today}", small))
    flow.append(Spacer(1, 6*cm))
    flow.append(Paragraph("für Chris &middot; von Bolla 🐾", small))
    flow.append(PageBreak())
    for k in kapitel:
        render_chapter(flow, k)
    doc.build(flow)
    print("PDF:", out)

# 1) Komplettes Buch
build(f"{DESK}/AURORA_Buch_komplett.pdf", ALLK, "Prolog &ndash; Kapitel 18")

# 2) Zuletzt geschriebene Kapitel (13-18)
neu_titles = ["Kapitel 13: Was man nicht begraebt",
              "Kapitel 14: Was man nicht teilt",
              "Kapitel 15: Was man nicht laut sagt",
              "Kapitel 16: Was man nicht zuruecknimmt",
              "Kapitel 17: Was man nicht wiederfindet",
              "Kapitel 18: Was man nicht verzeiht"]
neu = [k for k in ALLK if k.get('titel') in neu_titles]
build(f"{DESK}/AURORA_Kapitel_13-18.pdf", neu, "Kapitel 13 &ndash; 18")
