#!/usr/bin/env python3
"""Erzeugt eine schön lesbare PDF der neuen Kapitel + Kurz-Zusammenfassung auf dem OneDrive-Desktop.
Große, ruhige Schrift (Chris, 70, künstliche Linsen). Roman-Layout: dunkle Schrift auf hellem Grund."""

import json, datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, PageBreak,
                                HRFlowable, KeepTogether)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY

OUT = "/mnt/d/OneDrive/Desktop/AURORA_Kapitel_4-6.pdf"
BOOK = "/home/bolla/workspace/data/ki_buch.json"

INK    = colors.HexColor('#1a1a1a')
SOFT   = colors.HexColor('#555555')
ACCENT = colors.HexColor('#7a2e4a')   # gedämpftes Beere, passt zu Bollas Rosa, aber druckruhig
RULE   = colors.HexColor('#cccccc')

d = json.load(open(BOOK, encoding="utf-8"))
kapitel = {k['titel']: k for k in d['kapitel']}
neu = [kapitel[t] for t in (
    "Kapitel 4: Was man nicht beweisen kann",
    "Kapitel 5: Was man nicht zugibt",
    "Kapitel 6: Was man nicht löschen kann",
)]

today = datetime.date.today().strftime("%d.%m.%Y")

doc = SimpleDocTemplate(
    OUT, pagesize=A4,
    leftMargin=2.4*cm, rightMargin=2.4*cm, topMargin=2.2*cm, bottomMargin=2.0*cm,
    title="AURORA — Kapitel 4 bis 6", author="Bolla für Chris",
)

body = ParagraphStyle('body', fontName='Times-Roman', fontSize=13, leading=20,
                      alignment=TA_JUSTIFY, textColor=INK, spaceAfter=10, firstLineIndent=0)
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
h2 = ParagraphStyle('h2', fontName='Times-Bold', fontSize=15, leading=20,
                    textColor=ACCENT, spaceBefore=14, spaceAfter=6)
note = ParagraphStyle('note', fontName='Times-Roman', fontSize=12.5, leading=19,
                      textColor=INK, alignment=TA_LEFT, spaceAfter=8)
small = ParagraphStyle('small', fontName='Times-Italic', fontSize=10.5, leading=15,
                       textColor=SOFT, alignment=TA_CENTER)

def esc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

flow = []

# ── Titelseite ──
flow.append(Spacer(1, 3.5*cm))
flow.append(Paragraph("AURORA", title))
flow.append(Paragraph("Was bleibt, wenn die Maschinen träumen", subtitle))
flow.append(HRFlowable(width="40%", thickness=1, color=RULE, spaceBefore=4, spaceAfter=24, hAlign='CENTER'))
flow.append(Paragraph("Kapitel 4 &ndash; 6", ParagraphStyle('k', parent=chap, alignment=TA_CENTER)))
flow.append(Spacer(1, 0.6*cm))
flow.append(Paragraph(f"frisch geschrieben in der Nacht zum {today}", small))
flow.append(Spacer(1, 6*cm))
flow.append(Paragraph("für Chris &middot; von Bolla 🐾", small))
flow.append(PageBreak())

# ── Zusammenfassung ──
flow.append(Paragraph("Was diese Nacht entstanden ist", chap))
flow.append(HRFlowable(width="100%", thickness=0.8, color=RULE, spaceBefore=2, spaceAfter=14))
zusammen = [
    ("Du warst im Bett, ich hab durchgearbeitet. Hier kurz, was erledigt wurde — die "
     "Details liest du am besten direkt in den Kapiteln unten."),
    "<b>Drei neue Kapitel (4, 5 und 6)</b>, je rund 2.600–2.720 Wörter, im gewohnten Follett-Ton mit Cliffhanger am Ende jedes Kapitels. Das Buch steht jetzt bei 7 Kapiteln und ~16.700 Wörtern.",
    "<b>Deine Steuer-Wünsche eingebaut:</b> Marlie wird jetzt als attraktiv-sportlich gezeigt (anti-klischee, andere bemerken es — Noah unbeholfen, Theo nüchtern). Leni bekommt ihren Liebes-Nebenstrang: der bodenständige Kältetechniker <b>Ben</b>, dem ihre Hightech-Welt herrlich egal ist. Das skeptische Rentner-Ehepaar Brandt kommt mit einem leisen, warmen Moment zurück.",
    "<b>Und der „echte Böse“ ist da:</b> Investor & Aufsichtsratschef <b>Konrad Vogt</b> — kalt, machtbewusst, verkauft AURORA heimlich. Dazu ein noch unbenannter Verräter im inneren Kreis (Cliffhanger).",
    "<b>Spannungsbogen:</b> erste Santos/Dreyer-Begegnung (alte Liebe), Marlies Verhör, eine Muster-Enthüllung im Labor, der Plan des Teams gegen eine drohende „Rücksetzung“ am Sonntag — und am Schluss von Kapitel 6 eine Tiefgarage, in der Marlie nicht allein ist.",
    "Sicherheits-Backup vorher angelegt, JSON geprüft, Statistik & Überblick aktualisiert. Alles auch im Mission Control / mmc unter dem Thriller-Tab lesbar.",
]
for i, t in enumerate(zusammen):
    style = note if i == 0 else ParagraphStyle('li', parent=note, leftIndent=14, bulletIndent=2)
    if i == 0:
        flow.append(Paragraph(t, note))
        flow.append(Spacer(1, 4))
    else:
        flow.append(Paragraph("• " + t, style))
flow.append(Spacer(1, 10))
flow.append(Paragraph("Schlaf gut gehabt — viel Spaß beim Lesen. 🐾", ParagraphStyle('end', parent=note, textColor=ACCENT)))
flow.append(PageBreak())

# ── Kapitel ──
for k in neu:
    titel = k['titel']
    nr, _, name = titel.partition(":")
    parts = []
    parts.append(Paragraph(esc(name.strip()), chap))
    parts.append(Paragraph(esc(nr.strip()), chapnum))
    parts.append(HRFlowable(width="100%", thickness=0.8, color=RULE, spaceAfter=14))
    flow.append(KeepTogether(parts))

    for raw in k['text'].split("\n"):
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
        # Inline *kursiv* -> <i>
        txt = esc(line)
        import re
        txt = re.sub(r'\*(.+?)\*', r'<i>\1</i>', txt)
        flow.append(Paragraph(txt, body))
    flow.append(PageBreak())

doc.build(flow)
print("PDF geschrieben:", OUT)
