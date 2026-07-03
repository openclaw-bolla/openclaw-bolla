#!/usr/bin/env python3
"""AURORA EPUB Generator — erstellt AURORA_deutsch.epub in OneDrive"""

import json, os, zipfile, html, re, base64, urllib.request, time, uuid

EPUB_PATH = "/mnt/d/OneDrive/Dokumente/AURORA/AURORA_deutsch.epub"
KI_BUCH   = "/home/bolla/workspace/data/ki_buch.json"
MC_URL    = "http://127.0.0.1:18790"
AUTOR     = "Chris Mandel"
UID       = "urn:uuid:" + str(uuid.uuid4())

# ──────────────────────────────────────────────
# Backmatter-Texte (Deutsch)
# ──────────────────────────────────────────────





# ──────────────────────────────────────────────
# Helper: plain text → HTML-Absätze
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
    """Markdown-Subset → XHTML: *em*, --- → <hr>, Absätze."""
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
        if p.startswith('## '):
            out.append(f'<h2 class="subhead">{html.escape(p[3:].strip())}</h2>')
            continue
        p = html.escape(p)
        p = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', p)
        p = re.sub(r'\*(.*?)\*', r'<em>\1</em>', p)
        p = p.replace('\n', '<br/>\n')
        out.append(f'<p>{p}</p>')
    return '\n'.join(out)

def xhtml_wrap(title_str, body_html, extra_css=""):
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml"
      xmlns:epub="http://www.idpf.org/2007/ops" xml:lang="de">
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
# Cover-Generierung via MAI
# ──────────────────────────────────────────────

def generate_cover():
    prompt = (
        "Book cover background art for a dark German AI thriller novel. "
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
            print(f"  Cover ✓  (Tageslimit-Rest: {d.get('remaining','?')})")
            return base64.b64decode(d["image_b64"])
        else:
            print(f"  Cover-Fehler: {d.get('error')}")
            return None
    except Exception as e:
        print(f"  Cover-Exception: {e}")
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
h2.subhead {
  font-size: 1.05em;
  font-weight: bold;
  text-align: left;
  color: #222;
  margin: 1.8em 0 0.4em 0;
}
h2.subhead + p { text-indent: 0; }
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
/* Cover */
body.cover-body {
  margin: 0; padding: 0;
  background: #060912;
}
.cover-wrap {
  position: relative;
  width: 100%;
}
.cover-wrap img {
  display: block;
  width: 100%;
}
.cover-overlay {
  position: absolute;
  top: 0; left: 0; right: 0; bottom: 0;
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  align-items: center;
  padding: 0 5% 8%;
  background: linear-gradient(to bottom,
    rgba(0,0,0,0) 50%,
    rgba(6,9,18,0.7) 80%,
    rgba(6,9,18,0.92) 100%);
}
.cover-title {
  font-family: 'Palatino Linotype', Palatino, Georgia, serif;
  font-size: 3.2em;
  font-weight: bold;
  color: #ffffff;
  letter-spacing: 0.3em;
  text-align: center;
  white-space: nowrap;
  word-break: keep-all;
  overflow-wrap: normal;
  text-shadow:
    0 0 30px rgba(80,200,255,0.7),
    0 0 60px rgba(80,200,255,0.3),
    0 3px 6px rgba(0,0,0,0.9);
  margin: 0 0 0.3em 0;
}
.cover-author {
  font-size: 1em;
  color: rgba(255,255,255,0.8);
  letter-spacing: 0.25em;
  text-align: center;
  text-shadow: 0 1px 4px rgba(0,0,0,0.9);
  margin: 0;
}
"""

# ──────────────────────────────────────────────
# Seiten-Inhalte
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
      xmlns:epub="http://www.idpf.org/2007/ops" xml:lang="de">
<head>
  <meta charset="UTF-8"/>
  <title>AURORA</title>
  <style>html,body{{margin:0;padding:0;}}</style>
</head>
{body}
</html>'''

def vorspann_xhtml(text):
    text = text.strip()
    parts = text.split('\n', 1)
    headword = parts[0].strip()
    rest = parts[1].strip() if len(parts) > 1 else ''
    body = (f'  <p class="vorspann-headword">{html.escape(headword)}</p>\n'
            f'  <div class="vorspann">{html.escape(rest)}</div>')
    return xhtml_wrap("Vorspann", body)

def impressum_xhtml(text):
    body = f'  <div class="impressum">{html.escape(text.strip())}</div>'
    return xhtml_wrap("Impressum", body)

def vorwort_xhtml(text):
    body = f'  <h1 class="section-title">Vorwort</h1>\n  {md2html(text)}'
    return xhtml_wrap("Vorwort", body)

def chapter_xhtml(kapitel_obj, idx):
    titel = kapitel_obj.get("titel", f"Kapitel {idx}")
    text  = kapitel_obj.get("text", "")
    label = "Prolog" if idx == 0 else titel
    # Titel-Dopplung entfernen: erste Textzeile, wenn sie den Kapiteltitel wiederholt (ggf. **markiert**)
    _lines = text.lstrip().split('\n', 1)
    if _lines and _lines[0].strip().strip('*').strip() == titel.strip():
        text = _lines[1].lstrip('\n') if len(_lines) > 1 else ''
    # md2html rendert *kursiv*, **fett**, ## Zwischenüberschrift, --- Szenentrenner
    body  = f'  <h1 class="chapter-title">{html.escape(label)}</h1>\n  {md2html(text)}'
    return xhtml_wrap(label, body)

def epilog_xhtml(subtitle, body_text):
    body = (f'  <h1 class="section-title">Epilog</h1>\n'
            f'  <h2 class="section-subtitle">{html.escape(subtitle)}</h2>\n'
            f'  {md2html(body_text)}')
    return xhtml_wrap("Epilog", body)

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
    spine += '    <itemref idref="impressum" properties="page-spread-left"/>\n'
    spine += '    <itemref idref="vorwort" properties="page-spread-right"/>\n'
    spine += '    <itemref idref="vorspann" properties="page-spread-right"/>\n'
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
    <dc:language>de</dc:language>
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
        ('cover',     'Cover',       'Text/cover.xhtml'),
        ('impressum', 'Impressum',   'Text/impressum.xhtml'),
        ('vorwort',   'Vorwort',     'Text/vorwort.xhtml'),
        ('vorspann',  'Vorspann',    'Text/vorspann.xhtml'),
    ]
    for i, k in enumerate(kapitel):
        fid  = 'prolog' if i == 0 else f'chapter{i:02d}'
        items.append((fid, k['titel'], f'Text/{fid}.xhtml'))
    items.append(('epilog',     'Epilog',           'Text/epilog.xhtml'))
    items.append(('ueberautor', 'Über den Autor',   'Text/ueberautor.xhtml'))
    items.append(('danksagung', 'Danksagung',       'Text/danksagung.xhtml'))
    items.append(('rezension',  'Rezensions-Bitte', 'Text/rezension.xhtml'))

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
        ('Text/impressum.xhtml', 'Impressum'),
        ('Text/vorwort.xhtml',   'Vorwort'),
        ('Text/vorspann.xhtml',  'Vorspann'),
    ]
    for i, k in enumerate(kapitel):
        href = 'Text/prolog.xhtml' if i == 0 else f'Text/chapter{i:02d}.xhtml'
        items.append((href, k['titel']))
    items.append(('Text/epilog.xhtml',     'Epilog'))
    items.append(('Text/ueberautor.xhtml', 'Über den Autor'))
    items.append(('Text/danksagung.xhtml', 'Danksagung'))
    items.append(('Text/rezension.xhtml',  'Rezensions-Bitte'))

    li = ''.join(f'      <li><a href="{h}">{html.escape(t)}</a></li>\n' for h, t in items)

    return f'''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml"
      xmlns:epub="http://www.idpf.org/2007/ops" xml:lang="de">
<head>
  <meta charset="UTF-8"/>
  <title>Inhaltsverzeichnis</title>
  <link rel="stylesheet" type="text/css" href="css/style.css"/>
</head>
<body>
  <nav epub:type="toc" id="toc">
    <h1 class="section-title">Inhalt</h1>
    <ol>
{li}    </ol>
  </nav>
</body>
</html>'''

# ──────────────────────────────────────────────
# Haupt-Build
# ──────────────────────────────────────────────

def build():
    with open(KI_BUCH, encoding="utf-8") as f:
        buch = json.load(f)

    kapitel   = buch.get("kapitel", [])
    vorspann  = buch.get("vorspann", "")
    vorwort   = buch.get("vorwort", "")
    impressum = buch.get("impressum", "")
    epilog            = buch.get("epilog", "")
    epilog_untertitel = buch.get("epilog_untertitel", "")
    ueber_autor       = buch.get("ueber_autor", "")
    danksagung        = buch.get("danksagung", "")
    rezensions_bitte  = buch.get("rezensions_bitte", "")
    _req = {"vorspann":vorspann,"vorwort":vorwort,"impressum":impressum,"epilog":epilog,
            "epilog_untertitel":epilog_untertitel,"ueber_autor":ueber_autor,
            "danksagung":danksagung,"rezensions_bitte":rezensions_bitte}
    _missing = [k for k,v in _req.items() if not str(v).strip()]
    if _missing:
        raise SystemExit("FEHLER: Pflichtfelder fehlen in der JSON-Quelle: %s. Build abgebrochen (kein Hardcode-Fallback)." % _missing)

    print(f"AURORA EPUB Generator")
    print(f"  {len(kapitel)} Kapitel geladen")
    LOCAL_COVER = "/mnt/d/OneDrive/Dokumente/Bolla/AURORA/4_Cover_Quellen/AURORA_Cover_Master.png"
    if os.path.exists(LOCAL_COVER):
        print(f"  Verwende festes Release-Cover: AURORA_Cover_Master.png")
        with open(LOCAL_COVER, 'rb') as f:
            cover_bytes = f.read()
    else:
        print(f"  Generiere Cover via MAI...")
        cover_bytes = generate_cover()
    has_cover = cover_bytes is not None

    os.makedirs(os.path.dirname(EPUB_PATH), exist_ok=True)

    print(f"  Baue EPUB...")
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

        z.writestr("OEBPS/Text/epilog.xhtml",     epilog_xhtml(epilog_untertitel, epilog))
        z.writestr("OEBPS/Text/ueberautor.xhtml", backmatter_xhtml("Über den Autor", ueber_autor))
        z.writestr("OEBPS/Text/danksagung.xhtml", backmatter_xhtml("Danksagung", danksagung))
        z.writestr("OEBPS/Text/rezension.xhtml",  backmatter_xhtml("Rezensions-Bitte", rezensions_bitte))

    size_kb = os.path.getsize(EPUB_PATH) // 1024
    print(f"\n✅ EPUB fertig!")
    print(f"   Pfad:  {EPUB_PATH}")
    print(f"   Größe: {size_kb} KB")
    print(f"   Cover: {'✓ Portrait-Cover' if has_cover else '✗ (Fallback Text-Cover)'}")
    print(f"   Sektionen: Vorspann + Impressum + Vorwort + {len(kapitel)} Kap. + Epilog + Backmatter")

if __name__ == "__main__":
    build()
