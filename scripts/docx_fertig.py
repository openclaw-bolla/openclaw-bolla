"""Hilfsfunktion: 'Fertig'-Button (Hyperlink auf MP /api/fertig) ans Ende eines python-docx-Dokuments (Chris 16.10.2026)."""
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
import urllib.parse


def add_fertig_button(doc, job_id, titel="", base="http://127.0.0.1:18790"):
    url = f"{base}/api/fertig?id={urllib.parse.quote(job_id)}&titel={urllib.parse.quote(titel)}"
    doc.add_paragraph()
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    part = doc.part
    rid = part.relate_to(url, "http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink", is_external=True)
    h = OxmlElement("w:hyperlink"); h.set(qn("r:id"), rid)
    r = OxmlElement("w:r"); rpr = OxmlElement("w:rPr")
    for tag, val in (("w:color", "FFFFFF"),):
        e = OxmlElement(tag); e.set(qn("w:val"), val); rpr.append(e)
    sz = OxmlElement("w:sz"); sz.set(qn("w:val"), "40"); rpr.append(sz)
    b = OxmlElement("w:b"); rpr.append(b)
    shd = OxmlElement("w:shd"); shd.set(qn("w:val"), "clear"); shd.set(qn("w:color"), "auto"); shd.set(qn("w:fill"), "16A34A"); rpr.append(shd)
    r.append(rpr)
    t = OxmlElement("w:t"); t.text = "   ✅  FERTIG – Bolla Bescheid sagen   "; t.set(qn("xml:space"), "preserve"); r.append(t)
    h.append(r); p._p.append(h)
    n = doc.add_paragraph("Klick auf den grünen Knopf (Strg + Klick) – Bolla bekommt die Meldung und hakt es ab.")
    n.alignment = WD_ALIGN_PARAGRAPH.CENTER
    for run in n.runs: run.font.size = Pt(10); run.font.color.rgb = RGBColor(0x66, 0x66, 0x66)
