#!/usr/bin/env python3
"""Kurstag 06 (Handy-Video, Urheberrecht, YouTube) - Folien-Entwurf aus der 05-Vorlage bauen.

Nimmt Titel- (1) und Fragenfolie (7) aus 05, ersetzt die Inhaltsfolien. Ausgabe nur nach Handouts/Entwurf.
Aufruf: python3 kurstag06_folien_bauen.py
"""
import copy
import math
import os

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Emu, Pt

H = "/mnt/d/OneDrive/Dokumente/Office/7. Klassen/Handouts"
SRC = f"{H}/05-Basics Office -WebApps-Designer-Copilot.pptx"
OUT = f"{H}/Entwurf/06-Basics Office - Handyvideo-YouTube-Urheberrecht.pptx"
FONT = "Aptos"
W = 12192000

PURPLE = RGBColor(0x79, 0x58, 0xAA)
BLUE = RGBColor(0x1F, 0x71, 0xC7)
GREEN = RGBColor(0x2E, 0x8B, 0x57)
RED = RGBColor(0xC0, 0x39, 0x2B)
ORANGE = RGBColor(0xE6, 0x7E, 0x22)
GREY = RGBColor(0x5B, 0x5F, 0x66)
BLACK = RGBColor(0, 0, 0)
WHITE = RGBColor(255, 255, 255)

prs = Presentation(SRC)
layout = [l for m in prs.slide_masters for l in m.slide_layouts if l.name == "2_Titelfolie"][0]
warnings = []


def est_lines(text, size_pt, width_emu):
    cpl = max(1, int((width_emu / 12700) / (size_pt * 0.52)))
    return max(1, math.ceil(len(text) / cpl))


def add_text(slide, x, y, w, h, paras, size=26, color=BLACK, bold=False, line=None, align=None,
             anchor=None, check=True, name="Text"):
    """paras: Liste von Absaetzen; Absatz = str oder Liste von (text, bold)-Runs. '**x**' wird fett."""
    tb = slide.shapes.add_textbox(Emu(x), Emu(y), Emu(w), Emu(h))
    tb.name = name
    tf = tb.text_frame
    tf.word_wrap = True
    if anchor:
        tf.vertical_anchor = anchor
    line = int(size * 1.22) if (not line or line > size * 1.3) else line
    gap = int(size * 0.5)
    total = 0
    for i, p in enumerate(paras):
        para = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        para.line_spacing = Pt(line)
        para.space_after = Pt(gap)
        if align:
            para.alignment = align
        runs = p if isinstance(p, list) else _split_bold(p)
        plain = ""
        for t, b in runs:
            r = para.add_run()
            r.text = t
            plain += t
            f = r.font
            f.size = Pt(size)
            f.bold = bool(b or bold)
            f.name = FONT
            f.color.rgb = color
        total += est_lines(plain, size, w - 182880)
    need = (total * line + len(paras) * gap) * 12700 + 91440
    if check and need > h:
        warnings.append(f"{name}: geschaetzt {need/914400:.2f} in > Box {h/914400:.2f} in")
    return tb


def _split_bold(s):
    parts = s.split("**")
    return [(t, i % 2 == 1) for i, t in enumerate(parts) if t]


def new_slide(title):
    s = prs.slides.add_slide(layout)
    for ph in list(s.placeholders):
        ph._element.getparent().remove(ph._element)
    add_text(s, 1008126, 341576, 9300000, 784830, [title], size=44, bold=True, line=54, check=False,
             name="Titel")
    return s


def box(slide, x, y, w, h, fill, text="", size=22, color=WHITE, bold=True, shape=MSO_SHAPE.ROUNDED_RECTANGLE,
        align=PP_ALIGN.CENTER):
    sh = slide.shapes.add_shape(shape, Emu(x), Emu(y), Emu(w), Emu(h))
    sh.fill.solid()
    sh.fill.fore_color.rgb = fill
    sh.line.fill.background()
    sh.shadow.inherit = False
    tf = sh.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    tf.margin_left = tf.margin_right = Emu(60000)
    tf.margin_top = tf.margin_bottom = Emu(20000)
    lines = text.split("\n") if text else []
    for i, t in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        r = p.add_run()
        r.text = t
        r.font.size = Pt(size)
        r.font.bold = bold
        r.font.name = FONT
        r.font.color.rgb = color
    return sh


BODY_X, BODY_Y, BODY_W, BODY_H = 1008126, 1250000, 10300000, 5400000


def body(slide, paras, size=26, **kw):
    return add_text(slide, BODY_X, BODY_Y, BODY_W, BODY_H, paras, size=size, **kw)


title_slide = prs.slides[0]
# Animation (p:timing) verweist auf das Icon -> mit entfernen, sonst meldet PowerPoint "beschaedigt"
for tm in title_slide._element.findall("{http://schemas.openxmlformats.org/presentationml/2006/main}timing"):
    title_slide._element.remove(tm)
for sh in list(title_slide.shapes):
    if sh.name == "Picture 2":  # Copilot-Icon der 05
        sh._element.getparent().remove(sh._element)
    elif sh.has_text_frame and sh.text_frame.text.strip() == "Web - Apps":
        r = sh.text_frame.paragraphs[0].runs
        r[0].text = "Videos"
        for extra in r[1:]:
            extra.text = ""
# eigene Titelzeile ist ein Textfeld mit mehreren Runs -> Text pruefen
t = [sh.text_frame.text for sh in title_slide.shapes if sh.has_text_frame]
assert any("Videos" in x for x in t), t


# ---------- Inhaltsfolien ----------
# 2 Zeitplan
s = new_slide("Heute: 40 Minuten Handy-Video")
plan = [(3, "Start & Regeln", BLUE), (8, "A  Aufnehmen", GREEN), (12, "B  Schneiden", PURPLE),
        (7, "C  Recht", RED), (8, "D  YouTube", ORANGE), (2, "Puffer", GREY)]
x0, bw, total = 1008126, 10300000, 40
x = x0
for mins, label, col in plan:
    w = int(bw * mins / total)
    box(s, x, 1350000, w - 30000, 700000, col, f"{mins}'", size=22)
    x += w
rows = [("3 Min", "Start: Handy-Regeln, Thema fürs Mini-Video wählen"),
        ("8 Min", "A: Bildschirmaufnahme – Android & iPhone"),
        ("12 Min", "B: Video schneiden – Fotos-App & kostenlose Apps"),
        ("7 Min", "C: Urheberrecht, Recht am eigenen Bild, CC-Lizenzen"),
        ("8 Min", "D: YouTube am PC – teilen, einbinden, hochladen"),
        ("2 Min", "Puffer   →   Summe: 40 Minuten")]
add_text(s, 1008126, 2250000, 10300000, 4300000, [[(a + "   ", True), (b, False)] for a, b in rows], size=28,
         line=0)

# 3 Regeln
s = new_slide("Los geht's: Regeln fürs Handy")
body(s, ["**Handy nur mit Erlaubnis** – und nur für diese Aufgabe",
         "**Vorher:** „Nicht stören“ an, damit nichts ins Video platzt",
         "**Nichts Privates** aufnehmen: keine Chats, Passwörter, Fotos anderer",
         "**Akku** über 30 %, etwas Speicherplatz frei",
         "**Funktion fehlt oder Handy zu alt?** → Partner-Handy nutzen",
         "**Aufgabe:** Mini-Tutorial, 20–30 Sekunden (z. B. „Wecker stellen“)"], size=30, line=0)

# 4 Screen Recording
s = new_slide("Screen Recording: Was ist das?")
body(s, ["Das Handy filmt **den eigenen Bildschirm** – mit allen Fingertipps",
         "Wofür? **Anleitungen**, Fehler zeigen, App-Tipps, Schulprojekte",
         "Achtung: **alles** auf dem Bildschirm landet im Video – auch Nachrichten, Namen, Profilbilder",
         "Manche Apps **blockieren** die Aufnahme (Bild bleibt schwarz)",
         "Die Aufnahme liegt danach **in Fotos/Galerie** – meist im Ordner „Bildschirmaufnahmen“"],
     size=30, line=0)


def two_cols(title, left_head, left, right_head, right, size=26, lcol=GREEN, rcol=BLUE):
    s = new_slide(title)
    cw = 5050000
    box(s, 1008126, 1250000, cw, 520000, lcol, left_head, size=24)
    box(s, 1008126 + cw + 200000, 1250000, cw, 520000, rcol, right_head, size=24)
    add_text(s, 1008126, 1850000, cw, 4750000, left, size=size, line=int(size * 1.4), name="Links")
    add_text(s, 1008126 + cw + 200000, 1850000, cw, 4750000, right, size=size, line=int(size * 1.4),
             name="Rechts")
    return s


two_cols("Aufnahme starten",
         "Android (Samsung, Pixel, Xiaomi …)",
         ["**1** Mit 2 Fingern von oben ziehen: Schnelleinstellungen",
          "**2** Kachel „Bildschirmaufnahme“ oder „Bildschirmrekorder“ (Name je nach Hersteller)",
          "**3** Fehlt sie? Stift-Symbol → Kachel hinzufügen",
          "**4** Antippen, Ton wählen, Start",
          "**5** Stoppen: rotes Symbol/Benachrichtigung"],
         "iPhone (Kontrollzentrum)",
         ["**1** Von oben rechts nach unten wischen (mit Home-Taste: von unten hoch)",
          "**2** Symbol Punkt-im-Kreis antippen: 3-2-1",
          "**3** Mit Ton: Symbol lang drücken → Mikrofon an",
          "**4** Stoppen: roten Balken oben antippen",
          "**5** Fehlt es? Einstellungen → Kontrollzentrum"], size=24)

# 7 Ton / Berechtigungen / Plan B
s = new_slide("Ton, Mikro, Berechtigungen & Plan B")
body(s, ["**Ton wählen:** Systemton (Spiel/Video) oder **Mikro** (deine Stimme) – oder gar keiner",
         "**Mikro an** = Nebengeräusche hört man mit",
         "Das Handy fragt manchmal nach einer **Berechtigung** – nur erlauben, was du willst",
         "Jugendschutz/Bildschirmzeit kann die Funktion **sperren**",
         "**Plan B:** Partner-Handy nutzen – oder als Notlösung den Bildschirm mit einem anderen Handy abfilmen"],
     size=29, line=0)

# 8 Schnitt Grundbegriffe mit Illustration
s = new_slide("Video schneiden – die Grundlagen")
box(s, 1008126, 1350000, 10300000, 620000, PURPLE, "", size=20)
box(s, 1008126, 1350000, 700000, 620000, RED, "weg", size=20)
box(s, 10608126, 1350000, 700000, 620000, RED, "weg", size=20)
add_text(s, 3000000, 1420000, 6000000, 500000, ["dein Clip   (Regler ziehen)"], size=22, color=WHITE, bold=True,
         align=PP_ALIGN.CENTER, check=False)
body_y = 2150000
add_text(s, BODY_X, body_y, BODY_W, 4400000,
         ["**Trimmen:** Anfang und Ende abschneiden",
          "**Teilen (Split):** Clip an einer Stelle zerschneiden, Mittelteil löschen",
          "**Text & Titel** einblenden, **Tempo** ändern",
          "**Musik** nur mit Erlaubnis (→ Urheberrecht!)",
          "**Exportieren:** fertiges Video speichern – kurze Clips reichen (Dateigröße!)"],
         size=30, line=0)

two_cols("Schnitt ohne Extra-App",
         "iPhone: Fotos-App",
         ["**1** Fotos → Video öffnen → **Bearbeiten**",
          "**2** Unten Zeitleiste: gelben Rahmen links/rechts ziehen",
          "**3** **Fertig** – das Original lässt sich zurücksetzen",
          "Auch möglich: Filter, Zuschneiden, Drehen"],
         "Android: Google Fotos / Galerie",
         ["**1** Video öffnen → **Bearbeiten** (Stift)",
          "**2** Regler an der Zeitleiste ziehen",
          "**3** **Speichern** – wenn möglich „als Kopie“",
          "Samsung & Co.: eigene Galerie-App, gleiche Idee"],
         lcol=BLUE, rcol=GREEN, size=28)

# 10 Apps
s = new_slide("Kostenlose Schnitt-Apps (Beispiele)")
body(s, ["Beispiele: **CapCut**, **InShot**, **YouTube Create** – meist für Android **und** iPhone",
         "Funktionen, Preise und Verfügbarkeit **ändern sich** – nichts ist Pflicht",
         "„Gratis“ heißt oft: Werbung oder **Zusatzfunktionen gegen Geld**",
         "**Datenschutz:** nur nötige Berechtigungen erlauben (Fotos, Mikro); Altersfreigabe im Store beachten – im Zweifel **Eltern fragen**",
         "**Musik & Effekte** aus Apps: Nutzungsbedingungen lesen – oft gilt die Erlaubnis nur **in der App**"],
     size=27, line=0)

# 11 Urheberrecht 1
s = new_slide("Urheberrecht: Wem gehört's?")
body(s, ["**Wer etwas schafft** (Foto, Song, Video, Text), ist **Urheber** – automatisch",
         "Kein ©-Zeichen, keine Anmeldung nötig",
         "**Eigenes:** du entscheidest. **Fremdes:** du brauchst **Erlaubnis** (Lizenz)",
         "Der Schutz gilt sehr lang – bis **70 Jahre nach dem Tod**",
         "„Im Internet gefunden“ heißt **nicht** „frei benutzbar“",
         "Gilt für **Bild, Ton und Video**"], size=30, line=0)

# 12 Musik & YouTube
s = new_slide("Musik, Videos & YouTube")
body(s, ["**Hit-Song** unter dein öffentliches Video legen → ohne Erlaubnis **Problem**",
         "YouTube **erkennt Musik automatisch** – Video kann stumm, gesperrt oder mit Werbung versehen werden",
         "Klassenraum zeigen ≠ **öffentlich hochladen**",
         "**Sicher:** eigene Musik, YouTube-Audiomediathek, **CC-Musik** – Bedingungen beachten",
         "Fremde YouTube-Videos **herunterladen** ist laut YouTube-Regeln nicht erlaubt → lieber **verlinken**",
         "Bei Verstößen: Sperre, Verwarnung, im Extremfall **Abmahnung mit Kosten**"],
     size=26, line=0)

# 13 Recht am eigenen Bild
s = new_slide("Recht am eigenen Bild")
body(s, ["**Menschen** in Fotos/Videos nur mit **Einwilligung** veröffentlichen",
         "Unter 18: meist zusätzlich **Eltern fragen**",
         "**Heimlich** filmen oder Gespräche aufnehmen: verboten, kann sogar **strafbar** sein",
         "In der Schule: nur mit Erlaubnis **aller** Beteiligten und der Lehrkraft",
         "**Bildschirmaufnahme:** fremde Chats, Namen, Profilbilder und Nummern **weglassen**",
         "Auch du darfst sagen: **„Bitte nicht filmen!“**",
         "Das ist eine Einführung – **keine Rechtsberatung**"], size=28, line=0)

# 14 CC-Lizenzen
s = new_slide("Creative-Commons-Lizenzen")
badges = [("BY", "Namensnennung nötig", BLUE), ("NC", "nicht kommerziell", ORANGE),
          ("ND", "nicht verändern", RED), ("SA", "Weitergabe unter gleichen Bedingungen", GREEN),
          ("CC0", "frei, ohne Auflagen", GREY)]
bx, bwid = 1008126, 1900000
for i, (k, v, c) in enumerate(badges):
    xx = bx + i * 2100000
    box(s, xx, 1300000, bwid, 620000, c, k, size=26)
    add_text(s, xx, 1950000, bwid, 900000, [v], size=16, line=20, align=PP_ALIGN.CENTER, check=False)
add_text(s, BODY_X, 3000000, BODY_W, 3600000,
         ["**Quellenangabe (TULLU):** Titel – Urheber – Lizenz – Link zur Lizenz – Ursprung (Fundort)",
          "Fundorte: Wikimedia Commons, Pixabay, Unsplash, Pexels – **Lizenz immer auf der Seite prüfen**",
          "YouTube-Suche: Filter **Creative Commons**; bei Google Bilder: Filter für Nutzungsrechte",
          "Auch bei KI-Bildern/-Musik: **Nutzungsbedingungen** des Dienstes lesen"],
         size=26, line=0)

# 15 YouTube teilen & einbinden
s = new_slide("YouTube am PC: teilen & einbinden")
body(s, ["**Teilen:** Video → **Teilen** → Link kopieren",
         "**Startzeit:** Haken „Beginnen bei“ – das Video startet an deiner Stelle",
         "**Einbetten:** Teilen → Einbetten → Code für Webseiten/Blogs",
         "In PowerPoint folgen eigene Wege (später, Thema Audio/Video/Links)",
         "**Link statt Kopie:** Der Urheber behält die Kontrolle, nichts muss heruntergeladen werden",
         "Fremdes Video **nicht** als eigene Datei hochladen"], size=29, line=0)

# 16 YouTube hochladen
s = new_slide("Hochladen: Wer darf's sehen?")
add_text(s, BODY_X, 1250000, BODY_W, 900000,
         ["Demo am Lehrer-PC: YouTube Studio → **Erstellen** → **Video hochladen** → Titel, Beschreibung, "
          "Zielgruppe („für Kinder?“), **Sichtbarkeit**"], size=26, line=0)
vis = [("Privat", "nur ich und Eingeladene", GREEN), ("Nicht gelistet", "jeder mit dem Link", ORANGE),
       ("Öffentlich", "jeder kann es finden", RED)]
for i, (k, v, c) in enumerate(vis):
    xx = 1008126 + i * 3480000
    box(s, xx, 2350000, 3300000, 700000, c, k, size=28)
    add_text(s, xx, 3100000, 3300000, 500000, [v], size=20, line=28, align=PP_ALIGN.CENTER, check=False)
add_text(s, BODY_X, 3800000, BODY_W, 2800000,
         ["Für uns: **Privat** oder **Nicht gelistet** reicht völlig",
          "Konto/Kanal: es gibt **Altersgrenzen** – ohne Erlaubnis der Eltern **kein eigener Kanal**",
          "Lizenz wählen: Standard-YouTube-Lizenz oder Creative Commons"], size=28, line=0)

# 17 Sinnvoll gestalten + Checkliste
s = new_slide("Darf ich das hochladen? Checkliste")
body(s, ["**1** Habe ich es **selbst** gemacht (Bild, Ton, Video)?",
         "**2** Sind **Personen** drauf – und einverstanden (Eltern bei unter 18)?",
         "**3** Fremde Bilder/Musik: **Lizenz erlaubt es** und Quelle ist genannt?",
         "**4** Keine **privaten Daten** sichtbar (Chats, Namen, Adresse, Kennzeichen)?",
         "**5** **Sichtbarkeit** passend gewählt (privat oder nicht gelistet)?",
         "Gut gestaltet: **klarer Titel**, Beschreibung mit **Quellen**, eigenes Vorschaubild"],
     size=29, line=0)

# Folien 2-6 der 05 entfernen, alte Folie 7 ans Ende (erst nach dem Anlegen, sonst kollidieren Part-Namen)
ids = prs.slides._sldIdLst
all_ids = list(ids)
old_last = all_ids[6]
for sld in all_ids[1:6]:
    prs.part.drop_rel(sld.rId)
    ids.remove(sld)
ids.remove(old_last)
ids.append(old_last)

os.makedirs(os.path.dirname(OUT), exist_ok=True)
prs.save(OUT)
print("gespeichert:", OUT, "Folien:", len(prs.slides))
for w in warnings:
    print("WARNUNG:", w)
