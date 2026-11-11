"""Write build/reference.docx, the Word style template used by build.py (pandoc --reference-doc).

Pandoc's default reference document, restyled for review copies (submission checklist 1b, rule 5):
A4, 2.54 cm margins, Times New Roman 11 pt, line spacing 1.15, bold title and headings, compact 8 pt tables,
continuous line numbers and centred page numbers, so reviewers can cite "page 7, line 245".

    python build/make_reference_docx.py
"""
import subprocess
from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt

OUT = Path(__file__).resolve().parent / "reference.docx"
FONT, SIZE, LINE, AFTER = "Times New Roman", 11, 1.15, 6
BODY = ("Normal", "Body Text", "First Paragraph", "Block Text", "Bibliography", "Abstract")


def main():
    subprocess.run(["pandoc", "-o", str(OUT), "--print-default-data-file", "reference.docx"], check=True)
    d = Document(str(OUT))
    for s in d.sections:
        s.page_width, s.page_height = Cm(21.0), Cm(29.7)
        s.left_margin = s.right_margin = s.top_margin = s.bottom_margin = Cm(2.54)
    for st in d.styles:
        f = getattr(st, "font", None)
        if f is None:
            continue
        f.name = FONT
        rf = st.element.get_or_add_rPr().find(qn("w:rFonts"))
        if rf is not None:
            for a in ("asciiTheme", "hAnsiTheme", "eastAsiaTheme", "cstheme"):
                rf.attrib.pop(qn("w:" + a), None)
        name = st.name or ""
        pf = getattr(st, "paragraph_format", None)
        if name in BODY:
            f.size = Pt(SIZE)
            if pf is not None:
                pf.line_spacing, pf.space_after, pf.space_before = LINE, Pt(AFTER), Pt(0)
        elif name in ("Compact", "Table"):            # tables: 8 pt, no spacing (keeps Table 1 on one page)
            f.size = Pt(8)
            if pf is not None:
                pf.line_spacing, pf.space_after, pf.space_before = 1.0, Pt(0), Pt(0)
        elif name.startswith("Heading"):
            f.size = Pt({"Heading 1": 14, "Heading 2": 12, "Heading 3": 11}.get(name, 11))
            f.color.rgb = None
            f.bold = True
        elif name == "Title":
            f.size = Pt(16)
            f.bold = True
            f.color.rgb = None
        elif name in ("Table Caption", "Image Caption", "Caption"):
            f.size = Pt(10)
    for s in d.sections:
        sp = s._sectPr
        for old in sp.findall(qn("w:lnNumType")):
            sp.remove(old)
        ln = OxmlElement("w:lnNumType")
        ln.set(qn("w:countBy"), "1")
        ln.set(qn("w:restart"), "continuous")
        ln.set(qn("w:distance"), "283")
        anchor = sp.find(qn("w:pgNumType"))
        if anchor is None:
            anchor = sp.find(qn("w:cols"))
        anchor.addprevious(ln) if anchor is not None else sp.append(ln)
        p = s.footer.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run()
        for tag, attr in (("w:fldChar", "begin"), ("w:instrText", None), ("w:fldChar", "end")):
            el = OxmlElement(tag)
            if attr:
                el.set(qn("w:fldCharType"), attr)
            else:
                el.set(qn("xml:space"), "preserve")
                el.text = " PAGE "
            r._r.append(el)
    d.save(str(OUT))
    print("wrote", OUT)


if __name__ == "__main__":
    main()
