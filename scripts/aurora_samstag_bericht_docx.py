import re
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

SRC='/home/bolla/workspace/scratch/aurora_samstag_20261003/uebersicht.md'
OUT='/mnt/d/OneDrive/Desktop/AURORA_II_Samstagslauf_Bericht.docx'

fazit={
1:"Starkes Fundament, Zeitlogik korrigiert.",
2:"Zahlen-Kanon (AURORA 4 J. 7 M.) geprüft; Selbstmord-Vergleich offen.",
3:"Zahlenfehler benannt; Atmosphäre und Saat passen.",
4:"Siez-Bogen trägt; Kaffeebecher-Slapstick und Emils Alter prüfen.",
5:"Schrank-Szene warm; kleine Zahlen-/Zeitfehler, Jacke geklärt.",
6:"Kollmann/Basti lebendig; Jackenlogik jetzt entschieden.",
7:"Sehr dicht, Cliffhanger sitzt; Glasübergangs-Vorausschau offen.",
8:"Bester Cliffhanger („aufgeräumt“/„gelöscht“); Titel-Zahl offen.",
9:"Emotional dicht; Emil-Finger, Riemann-Episode prüfen.",
10:"Humor-Maßstab; Falkners Alter und Poststempel korrigiert.",
11:"Mond-Lied ist der Herzschlag des Buchs; Daten bereinigt.",
12:"Szymanski, Ashworth stark; Zeitrechnung korrigiert.",
13:"Hanne-Szene ein Höhepunkt; Zählverschiebungen behoben.",
14:"Frauke/Begleitperson Herzstück; Daten in Theos Notizen.",
15:"Abschied von AURORA stark; Stapelnummer, Zeitsprung korrigiert.",
16:"Eines der emotionalsten Kapitel; drei Konsistenzfehler behoben.",
17:"Sog durch Uhrzeit-Takte; fast nur Zeitangaben korrigiert.",
18:"Gerichtsszene hält die Spannung; Zahlen und Zeiten korrigiert.",
19:"Neu: Kaffeeautomat-Lösung; Tor-Widerspruch zu Kap. 16 behoben.",
20:"Neu: die vierzehn Sekunden; Zeitlogik, Vorgriff geglättet.",
21:"Neu: Theo-Indizien aufgelöst; Hanne an der Waage.",
22:"Neu: viele Fäden geschlossen, zwei neue geöffnet.",
23:"Neu: Falkner/AURORA „Jetzt schon.“ – einer der besten Momente.",
}
rows=[]
for line in open(SRC,encoding='utf-8'):
    m=re.match(r'- Kap (\d+) \[(\w+)\]: Humor ([\d.]+)/1000 · Spannung (\d+)/10 · Cliffhanger (\d+)/10 · Patches ok (\d+) / abgelehnt (\d+)',line)
    if m: rows.append(m.groups())

d=Document()
s=d.sections[0]
s.page_width,s.page_height=Cm(21),Cm(29.7)
for a in ('left_margin','right_margin'): setattr(s,a,Cm(1.7))
s.top_margin=Cm(1.5); s.bottom_margin=Cm(1.5)
st=d.styles['Normal']; st.font.name='Aptos'; st.font.size=Pt(10)
st.element.rPr.rFonts.set(qn('w:asciiTheme'),'minorHAnsi')
pf=st.paragraph_format; pf.space_after=Pt(0); pf.space_before=Pt(0); pf.line_spacing=1.15

def para(text='',bold=False,size=None,color=None,after=0):
    p=d.add_paragraph(); r=p.add_run(text); r.bold=bold; r.font.name='Aptos'
    if size: r.font.size=Pt(size)
    if color: r.font.color.rgb=RGBColor(*color)
    p.paragraph_format.space_after=Pt(after); return p
def shade(cell,hexcol):
    tcPr=cell._tc.get_or_add_tcPr(); sh=OxmlElement('w:shd')
    sh.set(qn('w:val'),'clear'); sh.set(qn('w:color'),'auto'); sh.set(qn('w:fill'),hexcol); tcPr.append(sh)

para('AURORA II – Bericht Samstags-Lauf',True,16,(0x1F,0x3A,0x5F))
para('3. Oktober 2026, 12:30 bis 22:02 Uhr · Stand Buch: 24 Kapitel, rund 114.000 Wörter',False,10,(0x55,0x55,0x55),after=6)

para('Das Wichtigste',True,12,(0x1F,0x3A,0x5F))
for t in ['Kapitel 1–18 wurden geprüft, 157 Korrekturen sind eingebaut (66 abgelehnt, weil sie nicht sicher oder nicht erlaubt waren).',
          'Kapitel 1–8 (von dir gegengelesen) wurden nur bei Grammatik/Tippfehlern automatisch angefasst. Inhaltliche Funde dort sind in deiner Entscheidungsliste gelandet und seitdem eingearbeitet.',
          'Sechs neue Kapitel (19–24) wurden geschrieben und gegengelesen. Dann war das 5-Stunden-Limit erreicht, der Lauf hat sich selbst beendet.',
          'Kap. 25–27 sind noch nicht geschrieben. Der Lauf kann auf Zuruf fortgesetzt werden.',
          'Ab Kap. 19 sind Plot-Weichen möglich – beim Lesen bitte sagen, was dir gefällt.']:
    p=d.add_paragraph(style='List Bullet'); p.add_run(t).font.name='Aptos'
para('',after=2)

para('Kapitel im Überblick',True,12,(0x1F,0x3A,0x5F),after=2)
t=d.add_table(rows=1,cols=6); t.style='Table Grid'; t.autofit=False
hdr=['Kap.','Humor','Spann.','Cliff.','Korr. ok/abgel.','Fazit']
widths=[Cm(1.1),Cm(1.5),Cm(1.4),Cm(1.3),Cm(2.4),Cm(9.9)]
for i,h in enumerate(hdr):
    c=t.rows[0].cells[i]; c.text=''; r=c.paragraphs[0].add_run(h); r.bold=True; r.font.size=Pt(9); r.font.color.rgb=RGBColor(255,255,255); shade(c,'1F3A5F')
for kap,typ,hu,sp,cl,ok,ab in rows:
    n=int(kap); cells=t.add_row().cells
    vals=[kap+(' neu' if typ=='neu' else ''),hu,sp,cl,f'{ok} / {ab}',fazit.get(n,'')]
    for i,v in enumerate(vals):
        cells[i].text=''; r=cells[i].paragraphs[0].add_run(v); r.font.size=Pt(9)
        if i<5: cells[i].paragraphs[0].alignment=WD_ALIGN_PARAGRAPH.CENTER
    if typ=='neu':
        for c in cells: shade(c,'EAF2E3')
for row in t.rows:
    for i,w in enumerate(widths): row.cells[i].width=w
para('Humor = Momente pro 1000 Wörter (Maßstab Kap. 10 ≈ 8). Spannung/Cliffhanger je 1–10. Grün = neu geschrieben.',False,8,(0x55,0x55,0x55),after=6)

para('Offene Punkte für dich',True,12,(0x1F,0x3A,0x5F),after=2)
offen=[
('Kap. 2','Der Vergleich „wie ein Selbstmordversuch“ (Jonas, Kopfhörer um den Hals) sollte wegen der Jugendfreigabe raus. Dein Kapitel, daher nicht angefasst. Ersatz vorschlagen?'),
('Kap. 7','Die Glasübergangs-Vorausschau verlässt Marlies Perspektive und gibt ein großes Versprechen ohne Gegenstück später. Bleibt sie?'),
('Kap. 8','Titel „Vierzig Häkchen“, aber im Kapitel stehen 39 Vorgänge. Sammelhaken als vierzigster zählen oder Titel ändern?'),
('Kap. 9','Die Riemann-Episode steht plotlogisch sehr groß. So lassen?'),
('Kap. 19','Prüfen, ob Kreft Theos Satz in Kap. 15 tatsächlich sagt (Bezug stimmt sonst nicht).'),
('Kalender','Die Wochentage zu den Daten passen zur Kalenderlage 2025 (z. B. 10.11. = Montag, 11.10. = Samstag), nicht zu 2026. Jahr im Text steht nirgends. Entscheidung: Buchkalender so lassen (nur intern 2026) oder Handlungsjahr 2025 festlegen?'),
]
for k,tx in offen:
    p=d.add_paragraph(style='List Bullet'); r=p.add_run(k+': '); r.bold=True; r.font.name='Aptos'; p.add_run(tx).font.name='Aptos'
para('',after=2)
para('Dateien: workspace/scratch/aurora_samstag_20261003 (changes.md = alle Textänderungen Vorher/Nachher, uebersicht.md) · Backup vor Start: workspace/backups/aurora2_backup_vor_samstag_20261003_1222.json · Lesebegleiter: workspace/docs/AURORA_II_Lesebegleiter_20261003.md',False,8,(0x55,0x55,0x55))
d.save(OUT); print('gespeichert',OUT,len(rows),'Kapitel')
