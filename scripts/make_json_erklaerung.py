#!/usr/bin/env python3
"""Erzeugt 'Bolla-JSON-Erklaerung.pdf' für den Claude-Code-Doku-Ordner.
Analog zur Bolla-MD-Erklaerung — erklärt JSON auf Augenhöhe (Chris, IT-versiert,
kein Entwickler). Große, gut lesbare Schrift."""
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer,
                                Preformatted, Table, TableStyle)

OUT = "/mnt/d/OneDrive/Dokumente/Bolla/claud code - openclaw Doku/Bolla-JSON-Erklaerung.pdf"

NAVY = colors.HexColor("#1e3a5f")
ORANGE = colors.HexColor("#d97706")
CODEBG = colors.HexColor("#f1f5f9")

styles = getSampleStyleSheet()
h1 = ParagraphStyle('h1', parent=styles['Title'], fontName='Helvetica-Bold',
                    fontSize=24, textColor=NAVY, spaceAfter=4, alignment=0)
sub = ParagraphStyle('sub', parent=styles['Normal'], fontSize=12,
                     textColor=colors.HexColor("#64748b"), spaceAfter=16)
h2 = ParagraphStyle('h2', parent=styles['Heading2'], fontName='Helvetica-Bold',
                    fontSize=15, textColor=ORANGE, spaceBefore=14, spaceAfter=6)
body = ParagraphStyle('body', parent=styles['Normal'], fontSize=12, leading=18,
                      spaceAfter=8)
code = ParagraphStyle('code', parent=styles['Code'], fontName='Courier',
                      fontSize=10.5, leading=15, textColor=NAVY,
                      backColor=CODEBG, borderPadding=8, leftIndent=4)

doc = SimpleDocTemplate(OUT, pagesize=A4, topMargin=20*mm, bottomMargin=18*mm,
                        leftMargin=20*mm, rightMargin=20*mm,
                        title="Was ist eine JSON-Datei?", author="Bolla")
S = []
S.append(Paragraph("Was ist eine JSON-Datei?", h1))
S.append(Paragraph("Bolla erklärt's — kurz, klar, ohne Fachchinesisch \U0001F43E", sub))

S.append(Paragraph("Die Grundidee", h2))
S.append(Paragraph(
    "Eine <b>JSON-Datei</b> ist einfach eine <b>Text-Datei, die Daten geordnet "
    "speichert</b> — wie ein digitaler Karteikasten, den auch ein Mensch lesen "
    "kann. JSON steht für „JavaScript Object Notation\", aber mit JavaScript "
    "musst du nichts zu tun haben: Es ist heute das Standard-Format, mit dem "
    "Programme Daten austauschen und ablegen.", body))
S.append(Paragraph(
    "Für dich als alten Unix/C-Mann: Denk an eine <b>struct</b>, nur als lesbarer "
    "Text statt im Speicher — oder an ein sehr ordentliches <b>.ini</b>-Config-File, "
    "das sich beliebig verschachteln lässt.", body))

S.append(Paragraph("So sieht das aus (Beispiel AURORA)", h2))
S.append(Preformatted(
    '{\n'
    '  "titel": "AURORA",\n'
    '  "autor": "Chris Mandel",\n'
    '  "kapitel": [\n'
    '    { "nummer": 1, "ueberschrift": "Der Anruf", "text": "Hamburg. Irgendwann bald. ..." },\n'
    '    { "nummer": 2, "ueberschrift": "Drei Woerter", "text": "..." }\n'
    '  ]\n'
    '}', code))

S.append(Paragraph("Die drei Bausteine", h2))
t = Table([
    [Paragraph('<font face="Courier"><b>{ }</b></font>', body),
     Paragraph("Ein <b>Objekt</b> — eine Sammlung von Eigenschaften.", body)],
    [Paragraph('<font face="Courier"><b>[ ]</b></font>', body),
     Paragraph("Eine <b>Liste</b> — hier z.B. alle Kapitel hintereinander.", body)],
    [Paragraph('<font face="Courier"><b>"name": wert</b></font>', body),
     Paragraph("<b>Schlüssel : Wert</b> — links der Name, rechts der Inhalt.", body)],
], colWidths=[38*mm, 122*mm])
t.setStyle(TableStyle([
    ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ('LINEBELOW', (0,0), (-1,-2), 0.4, colors.HexColor("#e2e8f0")),
    ('TOPPADDING', (0,0), (-1,-1), 6), ('BOTTOMPADDING', (0,0), (-1,-1), 6),
]))
S.append(t)

S.append(Paragraph("Warum das für AURORA der Clou ist", h2))
S.append(Paragraph(
    "Der ganze Buchinhalt — Titel, Klappentext, alle 47 Kapitel — steht <b>einmal</b> "
    "in der JSON. Die Build-Skripte lesen sie und erzeugen daraus automatisch das "
    "<b>EPUB</b> (E-Book) <i>und</i> das <b>Druck-PDF</b> — in beiden Sprachen. Du "
    "änderst also <b>eine einzige Datei</b>, und alle Ausgaben bleiben konsistent.", body))
S.append(Paragraph(
    "Deshalb ist die JSON die „Quelle der Wahrheit\". Bei einer großen Überarbeitung "
    "(z.B. Optimierung aller Kapitel mit einem stärkeren KI-Modell) wird der Text "
    "<b>in der JSON</b> verbessert, alles neu gebaut — und anschließend über alle "
    "Verkaufskanäle (D2D + KDP, E-Book + Taschenbuch, DE + EN) verteilt. Den genauen "
    "Ablauf hält Bolla in der Master-Update-Checkliste fest.", body))

doc.build(S)
print("OK:", OUT)
