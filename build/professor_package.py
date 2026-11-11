"""Build the package for the submitting author (checklist 1b, rule 11).

Run after build.py, build.py esi and package.py. Writes build/professor_package/ and
build/tahini_rsc_professor_package.zip:

  01_Manuscript.docx ... 08_Cover_letter.docx   upload files, numbered in ScholarOne upload order
  Form_sheet.docx                               copy-paste text for the ScholarOne form, generated FROM the manuscript
  Reading_copies/                               manuscript and ESI as PDF, exported with Microsoft Word
  Later_revision_stage/                         TOC graphic and text (RSC asks for them at revision)
  README.txt                                    what to do, in plain words

    python build/professor_package.py
"""
import re
import shutil
import subprocess
import zipfile
from pathlib import Path

from docx import Document
from docx.shared import Pt

ROOT = Path(__file__).resolve().parents[1]
MS = ROOT / "manuscript"
SUB = ROOT / "build" / "submission"
PK = ROOT / "build" / "professor_package"
ZIP = ROOT / "build" / "tahini_rsc_professor_package.zip"


def strip_comments(t):
    return re.sub(r"<!--.*?-->", "", t, flags=re.S)


def plain(t):
    t = strip_comments(t)
    t = re.sub(r"<sup>(.*?)</sup>", lambda m: m.group(1).replace("−1", "⁻¹").replace("2", "²"), t)
    t = re.sub(r"<sub>(.*?)</sub>", r"\1", t)
    t = re.sub(r"\[@[^\]]+\]", "", t)
    t = re.sub(r"\[#([\w-]+)\]", "[see manuscript]", t)
    t = t.replace("*", "")
    return re.sub(r"[ \t]*\n[ \t]*(?!\n)", " ", t).strip()


def section(md, head):
    t = (MS / md).read_text(encoding="utf-8")
    return t.split(f"## {head}", 1)[1].split("\n## ", 1)[0]


def word_pdf(src, dst):
    ps = ("$w=New-Object -ComObject Word.Application; $w.Visible=$false; "
          f"$d=$w.Documents.Open('{src}', $false, $true); $d.SaveAs2('{dst}', 17); $d.Close($false); $w.Quit()")
    subprocess.run(["powershell", "-NoProfile", "-Command", ps], check=True)


def main():
    if PK.exists():
        shutil.rmtree(PK)
    (PK / "Reading_copies").mkdir(parents=True)
    (PK / "Later_revision_stage").mkdir()

    figs = sorted((SUB / "figures").glob("Fig*.tif"), key=lambda p: int(re.sub(r"\D", "", p.stem)))
    order = [(SUB / "manuscript.docx", "Manuscript.docx")]
    order += [(f, f.name) for f in figs]
    order += [(SUB / "esi.docx", "ESI.docx"), (SUB / "cover_letter.docx", "Cover_letter.docx")]
    uploads = []
    for i, (src, name) in enumerate(order, 1):
        dst = PK / f"{i:02d}_{name}"
        shutil.copy(src, dst)
        uploads.append(dst.name)
    shutil.copy(SUB / "figures" / "TOC_graphic.tif", PK / "Later_revision_stage" / "TOC_graphic.tif")
    shutil.copy(SUB / "toc_entry_text.docx", PK / "Later_revision_stage" / "TOC_text.docx")
    word_pdf(SUB / "manuscript.docx", PK / "Reading_copies" / "Manuscript.pdf")
    word_pdf(SUB / "esi.docx", PK / "Reading_copies" / "ESI.pdf")

    front = (MS / "00_front.md").read_text(encoding="utf-8")
    title = re.search(r'title: "(.*?)"', front).group(1)
    abstract = plain(front.split("## Abstract", 1)[1].split("<!-- abstract", 1)[0])
    n_abs = len(abstract.split())
    das = plain(section("05_declarations.md", "Data availability"))
    ack = plain(section("05_declarations.md", "Acknowledgements"))
    coi = plain(section("05_declarations.md", "Conflicts of interest"))
    contrib = plain(section("05_declarations.md", "Author contributions"))
    cl = (MS / "cover_letter.md").read_text(encoding="utf-8")
    ai = plain(cl.split("Generative AI declaration (RSC policy): ", 1)[1].split("\n\n", 1)[0])
    n_tab = len(list(MS.glob("03b_table*.md")))

    d = Document()
    d.styles["Normal"].font.name = "Calibri"
    d.styles["Normal"].font.size = Pt(11)
    d.add_heading("ScholarOne form: text to copy (RSC Advances)", 1)
    d.add_paragraph("Generated from the manuscript files by build/professor_package.py, so it matches the "
                    "manuscript word for word.")

    def field(label, text):
        p = d.add_paragraph()
        p.add_run(label).bold = True
        d.add_paragraph(text)

    field("Journal and article type", "RSC Advances, Paper")
    field("Title", title)
    field(f"Abstract ({n_abs} words; limit about 250)", abstract)
    field("Authors, in this order",
          "1. Arzu Yılmaz, Department of Food Engineering, Faculty of Chemical and Metallurgical Engineering, "
          "Yildiz Technical University, 34220 Istanbul, Türkiye (no ORCID)\n"
          "2. Abdulhamid Batayhi, Department of Mechatronics Engineering, Faculty of Mechanical Engineering, "
          "Yildiz Technical University, 34220 Istanbul, Türkiye; ORCID 0009-0007-0374-6755; "
          "abdulhamid.batayhi@std.yildiz.edu.tr\n"
          "3. Muhammed Özgölet (corresponding author), Department of Food Engineering, Faculty of Chemical and "
          "Metallurgical Engineering, Yildiz Technical University, 34220 Istanbul, Türkiye; "
          "ORCID 0000-0001-5584-097X; mozgolet@yildiz.edu.tr\n"
          "4. Muhammet Arici, Department of Food Engineering, Faculty of Chemical and Metallurgical Engineering, "
          "Yildiz Technical University, 34220 Istanbul, Türkiye; ORCID 0000-0003-4126-200X; "
          "muarici@yildiz.edu.tr (as printed in Foods 2026, 15, 3639)")
    field("Author contributions (CRediT)", contrib)
    field("Funding", "No external funding.")
    field("Conflicts of interest", coi)
    field("Data availability", das)
    field("Generative AI declaration (also in the cover letter, Section 2.9 and the Acknowledgements)", ai)
    field("Acknowledgements (as in the manuscript)", ack)
    field("Files", f"{len(figs)} figures (TIFF, 600 dpi), {n_tab} tables (in the manuscript), "
          "Electronic Supplementary Information (one Word file).")
    field("Preferred reviewers", "None (authors' decision, 2026-11-11). If the system will not continue without "
          "names, a list of candidates is available from Abdulhamid Batayhi.")
    field("Previously published or submitted elsewhere?",
          "No. The spectra were published with Batayhi et al., Foods, 2026, 15, 3639; the cover letter explains "
          "what is new.")
    d.save(PK / "Form_sheet.docx")

    readme = f"""Tahini paper for RSC Advances: submission package

Title: {title}

To submit (ScholarOne, RSC Advances, article type Paper):
1. Upload the numbered files in this order: {", ".join(uploads)}.
   File type: 01 = main manuscript, 02 to {len(figs) + 1:02d} = figures, ESI = electronic supplementary
   information, cover letter = cover letter.
2. Copy the title, abstract, author details and statements from Form_sheet.docx into the form.
3. Leave preferred reviewers empty if the system allows it.

Reading_copies has the manuscript and the ESI as PDF (made with Word), for reading only. Do not upload them.
Later_revision_stage has the table-of-contents graphic and text. RSC asks for them only at revision.

Before submitting, all four authors should read and approve the manuscript.

Code and results: https://github.com/abdulhamidbatayhi123/tahini-rsc-multitask
Archive: https://doi.org/10.5281/zenodo.24126434
"""
    (PK / "README.txt").write_text(readme, encoding="utf-8")

    if ZIP.exists():
        ZIP.unlink()
    with zipfile.ZipFile(ZIP, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(PK.rglob("*")):
            if f.is_file():
                z.write(f, f.relative_to(PK))
    print(f"abstract {n_abs} words; {len(uploads)} upload files -> {ZIP.name}")


if __name__ == "__main__":
    main()
