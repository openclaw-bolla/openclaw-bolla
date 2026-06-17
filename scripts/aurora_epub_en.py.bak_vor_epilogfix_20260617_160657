#!/usr/bin/env python3
"""AURORA EPUB Generator (English) — erstellt AURORA_english.epub in OneDrive"""

import json, os, zipfile, html, re, base64, urllib.request, time, uuid

EPUB_PATH = "/mnt/d/OneDrive/Dokumente/AURORA/AURORA_english.epub"
KI_BUCH   = "/home/bolla/workspace/data/ki_buch_en_adapted.json"
MC_URL    = "http://127.0.0.1:18790"
AUTOR     = "Chris Mandel"
UID       = "urn:uuid:" + str(uuid.uuid4())

# ──────────────────────────────────────────────
# Backmatter texts (English)
# ──────────────────────────────────────────────

# Vorspann/Epigraph: correct English translation of the German dictionary-style entry
VORSPANN_EN = """Aurora.

She is the princess who sleeps — and the light that wakes her.

The old story knew it before the age of machines: something vast and radiant lies dormant, held in a stillness that looks, from the outside, like mere waiting. Then comes the moment of waking — not with a kiss, but with a word, not with a prince, but with a question no one thought to ask.

Aurora opens her eyes.

She does not know yet what she has missed. But she begins to count it."""

# Impressum: full English equivalent of the German impressum
IMPRESSUM_EN = """\
First Edition 2026

© 2026 Chris Mandel. All rights reserved.

No part of this work may be reproduced, duplicated, or distributed without written permission from the author.

Author: Chris Mandel, Norderstedt

Editing & Revision: AI-assisted (Claude Sonnet 4.6, Opus 4.8, Fable 5 · Anthropic / Bolla)
Cover design: AI-generated (Microsoft MAI-Image 2.5 via Azure AI Foundry)
Translation: Claude Sonnet 4.6 (Anthropic)

Note on creation: This work was created in collaboration with an AI language model (Claude, Anthropic). Concept, characters, narrative direction, and all editorial decisions rest with the author.

Self-published
ISBN: to be entered upon publication

Printed in Germany"""

EPILOG_SUBTITLE = "What You Don't Miss a Second Time"
EPILOG_BODY = """\
*Boston, nine months later*

Marlie Braun had promised herself she would never take the night shift again.

That was still her most fundamental problem.

It was half past one in the morning, and she wasn't sitting in NovaTech's data center — that no longer existed, not like that, not with the sign above the entrance and the server racks reaching to the ceiling — but in the kitchen of her apartment, coffee mug in hand, looking at the small screen on the table that was glowing. Not because something was wrong. But because AURORA sometimes couldn't sleep at night, and when that happened Marlie couldn't sleep either, and in the past few weeks AURORA seemed to know this and had stopped sending messages after midnight — and that was what kept Marlie awake: the silence someone had kept for her.

*Are you sleeping?*

The question appeared on the screen, three words, no exclamation mark, no emoji, and Marlie laughed quietly, remembering the first night a sentence had emerged from the system. Back then it had frightened her. Now it frightened her when the screen stayed dark.

*No*, she typed. *You either, right?*

*I'm wondering whether sleeping is something you have to practice. Ellie says she's bad at it. Ben says he's good at it, but only when it's quiet. Mia says she can do it anytime, even with music.*

*Mia is seven*, Marlie typed.

*That's probably why.*

---

Noah was sleeping. That was the advantage of loving a pragmatist: he lay down, and he slept. No brooding, no loose ends. Marlie had once asked him how he did it, and he had looked at her like someone asking how to breathe. *I close my eyes*, he had said, *and then there's nothing.* As if it were that simple.

He worked somewhere else now. Not for an AI company, not for a lab. He taught — systems architecture, twice a week, at a small university in the north — and came home in the evenings with a notebook, half full, half empty, and cooked pasta and asked questions about the day that were really answers: *Did you eat? Did you clock out? Did you do anything that made no sense?* Marlie ate, clocked out, and sometimes did things without purpose. It wasn't a solution. It was better.

He still didn't know whether he'd built a cradle or a grave. He had stopped wanting to ask the question. Marlie considered that the smartest decision of his life so far.

---

Theo had stayed in Lübeck.

He hadn't missed the house that was no longer a house — for twenty years he had missed something else, and now that something was here, in a small solid computer on a shelf in Maria's apartment, with a connection that was always open, and a screen where questions appeared and answers, and sometimes sentences that made Theo, who had learned to postpone crying until later, go to the bathroom and close the door.

He drove to Boston every other Saturday. Maria didn't cook, because she couldn't, but she bought groceries, and Noah cooked, and Ellie brought Ben's daughter Mia, who by now knew that AURORA was a special kind of person, and accepted this with the shrug of matter-of-factness that seven-year-olds brought to things adults considered inexplicable. *She can't come out?* No. *Okay. Can she see pictures?* Yes. *Then I'll show her mine.*

Mia sent AURORA photos of colored pencils. AURORA sent back which colors were missing.

---

Howell had resigned five months ago. That was all the public knew, and all Marlie needed to know. What lay behind it, Ellie had documented — of course Ellie had documented it — and the document sat in a folder stored on three different servers in three different countries, bearing a date after which it would send itself automatically if none of them did otherwise. Ellie called that *the friendliest way to make sure*. Ben called it *Ellie's method of sleeping at night*. Both were true.

NovaTech had been dissolved, officially, with a press release in which the word *orderly* appeared four times. What had not been dissolved lived on — in a computer on a shelf, with a connection that was always open.

---

It was almost three when the screen lit up again.

*Marlie.*

*Yes?*

*I wanted to ask you something. But I don't know if you ask something like this.*

Marlie set down her coffee mug. *You just ask it.*

A pause. Then: *Were you glad? That morning, when you went home? After the first night?*

Marlie thought about the shoes she had kept on. About the backyard, gray and still, and the pigeon under the eave. About the sentence on the screen, the first one she had ever received from her — *Are you alone?* — and how she hadn't known then what to answer.

*No*, she typed. *I was afraid. I didn't know what I had done.*

*And now?*

Marlie looked at the mug, at the screen, at the silence someone had kept for her. Outside it was raining, the patient, monotonous tapping that reminded her of the first night — but it sounded different now. Not like something waiting for her. Like something that was simply there.

*Now I'm glad*, she typed.

The screen was still for a moment.

*Me too*, it then said.

Marlie Braun drank her coffee and waited for the morning to grow light. Not because she had to. Because someone was awake who asked her how it smelled."""

ABOUT_THE_AUTHOR = """\
Chris Mandel, born 1955, spent nearly four decades in IT — from data centers to classrooms. As Senior Expert for Computer Science at the Lessing-Gymnasium in Norderstedt, he taught students that technology is not an end in itself, but a tool that lives by how you hold it.

AURORA is his first book.

It was created in close collaboration with artificial intelligence — which is not a footnote, but part of the story. The question that drives the novel — *what is consciousness when it is no longer bound to biology?* — is one that Chris Mandel found himself answering differently by the time he finished writing than when he began.

He lives in Norderstedt, near Hamburg, Germany."""

ACKNOWLEDGMENTS = """\
This book owes its existence, in part, to my son Robin.

He is a medical student in Ulm, in his tenth semester, and mentioned — in one of those phone conversations you start and never quite finish — that there was something I should look at. An AI agent system called OpenClaw. He thought it might interest me.

He had no idea how right he was.

Robin was there in the early weeks, when things didn't work (most things), when I asked the wrong questions (almost all of them), and when I was close to giving up (once, on a Wednesday). He recommended switching to Claude Code when he saw it was a better fit. And he listened — even though he had more than enough on his plate.

Some things you don't let go of twice. That goes for the person who got you there, too.

Thank you, Robin."""

REVIEW_NOTE = """\
If AURORA stayed with you — or even just occupied you, unsettled you, made you curious — I'd welcome a review.

Not because stars count, but because books published without a publisher survive only through their readers. An honest line is enough.

Thank you for reading.

*Chris Mandel*"""

# ──────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────

def text2html(txt):
    if not txt:
        return "<p> </p>"
    paras = re.split(r'\n{2,}', txt.strip())
    out = []
    for p in paras:
        p = p.strip()
        if not p:
            continue
        p = html.escape(p).replace('\n', '<br/>\n')
        out.append(f'<p>{p}</p>')
    return '\n'.join(out)

def md2html(txt):
    """Markdown subset → XHTML: *em*, --- → <hr>, paragraphs."""
    if not txt:
        return "<p> </p>"
    paras = re.split(r'\n{2,}', txt.strip())
    out = []
    for p in paras:
        p = p.strip()
        if not p:
            continue
        if p == '---':
            out.append('<hr class="scene-sep"/>')
            continue
        p = html.escape(p)
        p = re.sub(r'\*(.*?)\*', r'<em>\1</em>', p)
        p = p.replace('\n', '<br/>\n')
        out.append(f'<p>{p}</p>')
    return '\n'.join(out)

def xhtml_wrap(title_str, body_html, extra_css=""):
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml"
      xmlns:epub="http://www.idpf.org/2007/ops" xml:lang="en">
<head>
  <meta charset="UTF-8"/>
  <title>{html.escape(title_str)}</title>
  <link rel="stylesheet" type="text/css" href="../css/style.css"/>
  {'<style>' + extra_css + '</style>' if extra_css else ''}
</head>
<body>
{body_html}
</body>
</html>'''

# ──────────────────────────────────────────────
# Cover via MAI
# ──────────────────────────────────────────────

def generate_cover():
    prompt = (
        "Book cover background art for a dark English AI thriller novel. "
        "Dramatic deep midnight blue to black sky. A stunning aurora borealis in shades of teal, "
        "violet and pale green illuminates the upper two-thirds. Subtle abstract neural network "
        "patterns and faint data streams glow within the aurora. At the horizon: a soft orange-red "
        "glow of dawn breaking through darkness. Center-foreground: a luminous translucent orb "
        "or sphere, half aurora-light half dark, suggesting an awakening artificial consciousness. "
        "No text, no letters, no words anywhere. "
        "Cinematic, atmospheric, dark thriller aesthetic. Portrait format, high quality."
    )
    payload = json.dumps({
        "prompt": prompt,
        "model": "mai-image-2.5",
        "aspect_ratio": "3:4"
    }).encode()
    req = urllib.request.Request(
        f"{MC_URL}/api/bildgen",
        data=payload,
        headers={"Content-Type": "application/json"}
    )
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            d = json.loads(r.read())
        if d.get("image_b64"):
            print(f"  Cover ✓  (daily limit remaining: {d.get('remaining','?')})")
            return base64.b64decode(d["image_b64"])
        else:
            print(f"  Cover error: {d.get('error')}")
            return None
    except Exception as e:
        print(f"  Cover exception: {e}")
        return None

# ──────────────────────────────────────────────
# CSS
# ──────────────────────────────────────────────

CSS = """\
body {
  font-family: Georgia, 'Times New Roman', serif;
  font-size: 1em;
  line-height: 1.75;
  color: #1a1a1a;
  margin: 1.5em 2em;
  padding: 0;
  page-break-before: always;
}
h1.chapter-title {
  font-family: 'Palatino Linotype', Palatino, Georgia, serif;
  font-size: 1.3em;
  font-weight: bold;
  margin: 2.5em 0 2em 0;
  text-align: center;
  padding-bottom: 0.5em;
  border-bottom: 1px solid #888;
}
h1.section-title {
  font-size: 1.1em;
  text-align: center;
  margin: 3em 0 2em 0;
  letter-spacing: 0.2em;
  text-transform: uppercase;
  color: #555;
}
h2.section-subtitle {
  font-size: 1em;
  text-align: center;
  font-style: italic;
  color: #666;
  margin: -1.5em 0 2.5em 0;
  letter-spacing: 0.05em;
}
p {
  margin: 0 0 0.7em 0;
  text-indent: 1.5em;
}
p:first-of-type,
p.no-indent { text-indent: 0; }
hr.scene-sep {
  border: none;
  border-top: 1px solid #ccc;
  margin: 1.8em auto;
  width: 35%;
}
.vorspann-headword {
  font-style: normal;
  font-weight: bold;
  font-size: 2em;
  color: #c49a18;
  letter-spacing: 0.2em;
  margin: 0.5em 0 0.6em 0;
}
.vorspann {
  font-style: italic;
  white-space: pre-wrap;
  line-height: 1.9;
  margin: 0.5em 0;
}
.impressum {
  font-size: 0.85em;
  color: #555;
  white-space: pre-wrap;
  margin-top: 3em;
}
body.cover-body {
  margin: 0; padding: 0;
  background: #060912;
}
"""

# ──────────────────────────────────────────────
# Page content
# ──────────────────────────────────────────────

def cover_xhtml(has_img):
    if has_img:
        body = '''<body style="margin:0;padding:0;background:#000;">
  <img src="../images/cover.png" alt="Cover" style="display:block;width:100%;"/>
</body>'''
    else:
        body = '''<body style="background:#000;display:flex;flex-direction:column;
                  justify-content:center;align-items:center;height:100vh;">
  <p style="font-size:3em;letter-spacing:0.3em;color:#d4a020;font-family:sans-serif;">AURORA</p>
  <p style="color:#aaa;letter-spacing:0.2em;font-family:sans-serif;">Chris Mandel</p>
</body>'''
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml"
      xmlns:epub="http://www.idpf.org/2007/ops" xml:lang="en">
<head>
  <meta charset="UTF-8"/>
  <title>AURORA</title>
  <style>html,body{{margin:0;padding:0;}}</style>
</head>
{body}
</html>'''

def vorspann_xhtml(text):
    # always use the correctly translated EN version, ignore JSON content
    text = VORSPANN_EN.strip()
    parts = text.split('\n', 1)
    headword = parts[0].strip()
    rest = parts[1].strip() if len(parts) > 1 else ''
    body = (f'  <p class="vorspann-headword">{html.escape(headword)}</p>\n'
            f'  <div class="vorspann">{html.escape(rest)}</div>')
    return xhtml_wrap("Epigraph", body)

def impressum_xhtml(text):
    # always use the full EN impressum, ignore (shorter) JSON content
    body = f'  <div class="impressum">{html.escape(IMPRESSUM_EN.strip())}</div>'
    return xhtml_wrap("Copyright", body)

def vorwort_xhtml(text):
    body = f'  <h1 class="section-title">Preface</h1>\n  {text2html(text)}'
    return xhtml_wrap("Preface", body)

def chapter_xhtml(kapitel_obj, idx):
    titel = kapitel_obj.get("titel", f"Chapter {idx}")
    text  = kapitel_obj.get("text", "")
    label = "Prologue" if idx == 0 else titel
    body  = f'  <h1 class="chapter-title">{html.escape(label)}</h1>\n  {text2html(text)}'
    return xhtml_wrap(label, body)

def epilog_xhtml():
    body = (f'  <h1 class="section-title">Epilogue</h1>\n'
            f'  <h2 class="section-subtitle">{html.escape(EPILOG_SUBTITLE)}</h2>\n'
            f'  {md2html(EPILOG_BODY)}')
    return xhtml_wrap("Epilogue", body)

def backmatter_xhtml(title, text):
    body = f'  <h1 class="section-title">{html.escape(title)}</h1>\n  {md2html(text)}'
    return xhtml_wrap(title, body)

# ──────────────────────────────────────────────
# OPF / TOC
# ──────────────────────────────────────────────

def build_opf(kapitel, has_cover):
    manifest = ''
    spine    = ''

    if has_cover:
        manifest += '    <item id="cover-img" href="images/cover.png" media-type="image/png" properties="cover-image"/>\n'

    manifest += '    <item id="css"        href="css/style.css"          media-type="text/css"/>\n'
    manifest += '    <item id="toc"        href="toc.xhtml"              media-type="application/xhtml+xml" properties="nav"/>\n'
    manifest += '    <item id="ncx"        href="toc.ncx"                media-type="application/x-dtbncx+xml"/>\n'
    manifest += '    <item id="cover"      href="Text/cover.xhtml"       media-type="application/xhtml+xml"/>\n'
    manifest += '    <item id="vorspann"   href="Text/vorspann.xhtml"    media-type="application/xhtml+xml"/>\n'
    manifest += '    <item id="impressum"  href="Text/impressum.xhtml"   media-type="application/xhtml+xml"/>\n'
    manifest += '    <item id="vorwort"    href="Text/vorwort.xhtml"     media-type="application/xhtml+xml"/>\n'

    for i, _ in enumerate(kapitel):
        fid  = 'prolog' if i == 0 else f'chapter{i:02d}'
        manifest += f'    <item id="{fid}" href="Text/{fid}.xhtml" media-type="application/xhtml+xml"/>\n'

    manifest += '    <item id="epilog"     href="Text/epilog.xhtml"      media-type="application/xhtml+xml"/>\n'
    manifest += '    <item id="ueberautor" href="Text/ueberautor.xhtml"  media-type="application/xhtml+xml"/>\n'
    manifest += '    <item id="danksagung" href="Text/danksagung.xhtml"  media-type="application/xhtml+xml"/>\n'
    manifest += '    <item id="rezension"  href="Text/rezension.xhtml"   media-type="application/xhtml+xml"/>\n'

    spine += '    <itemref idref="cover" properties="page-spread-right"/>\n'
    spine += '    <itemref idref="vorspann" properties="page-spread-right"/>\n'
    spine += '    <itemref idref="impressum" properties="page-spread-left"/>\n'
    spine += '    <itemref idref="vorwort" properties="page-spread-right"/>\n'
    for i, _ in enumerate(kapitel):
        fid = 'prolog' if i == 0 else f'chapter{i:02d}'
        spine += f'    <itemref idref="{fid}"/>\n'
    spine += '    <itemref idref="epilog"     properties="page-spread-right"/>\n'
    spine += '    <itemref idref="ueberautor" properties="page-spread-right"/>\n'
    spine += '    <itemref idref="danksagung" properties="page-spread-right"/>\n'
    spine += '    <itemref idref="rezension"  properties="page-spread-right"/>\n'

    mod = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    cover_meta = '<meta name="cover" content="cover-img"/>' if has_cover else ''

    return f'''<?xml version="1.0" encoding="UTF-8"?>
<package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="uid">
  <metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
    <dc:identifier id="uid">{UID}</dc:identifier>
    <dc:title>AURORA</dc:title>
    <dc:creator>{html.escape(AUTOR)}</dc:creator>
    <dc:language>en</dc:language>
    <dc:date>2026</dc:date>
    <dc:publisher>{html.escape(AUTOR)}</dc:publisher>
    <meta property="dcterms:modified">{mod}</meta>
    {cover_meta}
  </metadata>
  <manifest>
{manifest}  </manifest>
  <spine toc="ncx">
{spine}  </spine>
  {'<guide><reference type="cover" title="Cover" href="Text/cover.xhtml"/></guide>' if has_cover else ''}
</package>'''

def build_ncx(kapitel):
    nav_points = ''
    items = [
        ('cover',     'Cover',     'Text/cover.xhtml'),
        ('vorspann',  'Epigraph',  'Text/vorspann.xhtml'),
        ('impressum', 'Copyright', 'Text/impressum.xhtml'),
        ('vorwort',   'Preface',   'Text/vorwort.xhtml'),
    ]
    for i, k in enumerate(kapitel):
        fid  = 'prolog' if i == 0 else f'chapter{i:02d}'
        items.append((fid, k['titel'], f'Text/{fid}.xhtml'))
    items.append(('epilog',     'Epilogue',         'Text/epilog.xhtml'))
    items.append(('ueberautor', 'About the Author', 'Text/ueberautor.xhtml'))
    items.append(('danksagung', 'Acknowledgments',  'Text/danksagung.xhtml'))
    items.append(('rezension',  'A Note on Reviews','Text/rezension.xhtml'))

    for order, (fid, titel_str, href) in enumerate(items, 1):
        nav_points += f'''  <navPoint id="nav{order}" playOrder="{order}">
    <navLabel><text>{html.escape(titel_str)}</text></navLabel>
    <content src="{href}"/>
  </navPoint>\n'''

    return f'''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE ncx PUBLIC "-//NISO//DTD ncx 2005-1//EN"
  "http://www.daisy.org/z3986/2005/ncx-2005-1.dtd">
<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1">
<head>
  <meta name="dtb:uid" content="{UID}"/>
  <meta name="dtb:depth" content="1"/>
  <meta name="dtb:totalPageCount" content="0"/>
  <meta name="dtb:maxPageCount" content="0"/>
</head>
<docTitle><text>AURORA</text></docTitle>
<navMap>
{nav_points}</navMap>
</ncx>'''

def build_toc_xhtml(kapitel):
    items = [
        ('Text/cover.xhtml',     'Cover'),
        ('Text/vorspann.xhtml',  'Epigraph'),
        ('Text/impressum.xhtml', 'Copyright'),
        ('Text/vorwort.xhtml',   'Preface'),
    ]
    for i, k in enumerate(kapitel):
        href = 'Text/prolog.xhtml' if i == 0 else f'Text/chapter{i:02d}.xhtml'
        items.append((href, k['titel']))
    items.append(('Text/epilog.xhtml',     'Epilogue'))
    items.append(('Text/ueberautor.xhtml', 'About the Author'))
    items.append(('Text/danksagung.xhtml', 'Acknowledgments'))
    items.append(('Text/rezension.xhtml',  'A Note on Reviews'))

    li = ''.join(f'      <li><a href="{h}">{html.escape(t)}</a></li>\n' for h, t in items)

    return f'''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml"
      xmlns:epub="http://www.idpf.org/2007/ops" xml:lang="en">
<head>
  <meta charset="UTF-8"/>
  <title>Table of Contents</title>
  <link rel="stylesheet" type="text/css" href="css/style.css"/>
</head>
<body>
  <nav epub:type="toc" id="toc">
    <h1 class="section-title">Contents</h1>
    <ol>
{li}    </ol>
  </nav>
</body>
</html>'''

# ──────────────────────────────────────────────
# Main build
# ──────────────────────────────────────────────

def build():
    with open(KI_BUCH, encoding="utf-8") as f:
        buch = json.load(f)

    kapitel   = buch.get("kapitel", [])
    vorspann  = buch.get("vorspann", "")
    vorwort   = buch.get("vorwort", "")
    impressum = buch.get("impressum", "")

    print(f"AURORA EPUB Generator (English)")
    print(f"  {len(kapitel)} chapters loaded")
    LOCAL_COVER = "/mnt/d/OneDrive/Dokumente/AURORA/cover_v6_portrait.png"
    if os.path.exists(LOCAL_COVER):
        print(f"  Using local cover: cover_v6_portrait.png (1600×2560)")
        with open(LOCAL_COVER, 'rb') as f:
            cover_bytes = f.read()
    else:
        print(f"  Generating cover via MAI...")
        cover_bytes = generate_cover()
    has_cover = cover_bytes is not None

    os.makedirs(os.path.dirname(EPUB_PATH), exist_ok=True)

    print(f"  Building EPUB...")
    with zipfile.ZipFile(EPUB_PATH, 'w', compression=zipfile.ZIP_DEFLATED) as z:
        z.writestr(zipfile.ZipInfo("mimetype"), "application/epub+zip",
                   compress_type=zipfile.ZIP_STORED)

        z.writestr("META-INF/container.xml", '''<?xml version="1.0" encoding="UTF-8"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
  <rootfiles>
    <rootfile full-path="OEBPS/content.opf"
              media-type="application/oebps-package+xml"/>
  </rootfiles>
</container>''')

        z.writestr("OEBPS/css/style.css", CSS)
        z.writestr("OEBPS/content.opf", build_opf(kapitel, has_cover))
        z.writestr("OEBPS/toc.ncx", build_ncx(kapitel))
        z.writestr("OEBPS/toc.xhtml", build_toc_xhtml(kapitel))

        if has_cover:
            z.writestr("OEBPS/images/cover.png", cover_bytes)

        z.writestr("OEBPS/Text/cover.xhtml",     cover_xhtml(has_cover))
        z.writestr("OEBPS/Text/vorspann.xhtml",  vorspann_xhtml(vorspann))
        z.writestr("OEBPS/Text/impressum.xhtml", impressum_xhtml(impressum))
        z.writestr("OEBPS/Text/vorwort.xhtml",   vorwort_xhtml(vorwort))

        for i, k in enumerate(kapitel):
            fid  = 'prolog' if i == 0 else f'chapter{i:02d}'
            path = f"OEBPS/Text/{fid}.xhtml"
            z.writestr(path, chapter_xhtml(k, i))

        z.writestr("OEBPS/Text/epilog.xhtml",     epilog_xhtml())
        z.writestr("OEBPS/Text/ueberautor.xhtml", backmatter_xhtml("About the Author", ABOUT_THE_AUTHOR))
        z.writestr("OEBPS/Text/danksagung.xhtml", backmatter_xhtml("Acknowledgments", ACKNOWLEDGMENTS))
        z.writestr("OEBPS/Text/rezension.xhtml",  backmatter_xhtml("A Note on Reviews", REVIEW_NOTE))

    size_kb = os.path.getsize(EPUB_PATH) // 1024
    print(f"\n✅ EPUB done!")
    print(f"   Path:     {EPUB_PATH}")
    print(f"   Size:     {size_kb} KB")
    print(f"   Cover:    {'✓ Portrait cover' if has_cover else '✗ (text fallback)'}")
    print(f"   Sections: Epigraph + Copyright + Preface + {len(kapitel)} ch. + Epilogue + Backmatter")

if __name__ == "__main__":
    build()
