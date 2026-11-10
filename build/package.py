"""Assemble the RSC Advances submission package in build/submission/ (see SUBMISSION_CHECKLIST.md).

Run after build.py and build.py esi. Copies the manuscript and ESI .docx, converts the cover letter and the
table-of-contents text to .docx, copies the 600 dpi TIFF figures and the TOC graphic, checks the RSC limits that can
be checked automatically, and writes a ZIP (ScholarOne accepts a ZIP of up to 20 files).
"""
import re
import shutil
import subprocess
import zipfile
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "build" / "out"
SUB = ROOT / "build" / "submission"
if SUB.exists():
    shutil.rmtree(SUB)
SUB.mkdir(parents=True)


def strip_comments(t):
    return re.sub(r"<!--.*?-->", "", t, flags=re.S).strip() + "\n"


def to_docx(src_md, dst):
    tmp = SUB / (dst.stem + ".md")
    tmp.write_text(strip_comments(src_md.read_text(encoding="utf-8")), encoding="utf-8")
    subprocess.run(["pandoc", str(tmp), "-o", str(dst)], check=True)
    tmp.unlink()


problems = []
shutil.copy(OUT / "manuscript.docx", SUB / "manuscript.docx")
shutil.copy(OUT / "esi.docx", SUB / "esi.docx")
to_docx(ROOT / "manuscript" / "cover_letter.md", SUB / "cover_letter.docx")
to_docx(ROOT / "manuscript" / "toc.md", SUB / "toc_entry_text.docx")

# abstract length (RSC: about 50-250 words)
front = (ROOT / "manuscript" / "00_front.md").read_text(encoding="utf-8")
abstract = strip_comments(front.split("## Abstract", 1)[1]).split("\n## ")[0]
n_abs = len(abstract.split())
if not 50 <= n_abs <= 250:
    problems.append(f"abstract {n_abs} words")

# TOC text (max 250 characters, 1-2 sentences)
toc = strip_comments((ROOT / "manuscript" / "toc.md").read_text(encoding="utf-8")).strip()
if len(toc) > 250:
    problems.append(f"TOC text {len(toc)} characters")

# figures: TIFF, >= 600 dpi, width 8.3 or 17.1 cm, height <= 23.3 cm; TOC graphic max 8 x 4 cm
figdir = SUB / "figures"
figdir.mkdir()
# main-text figures as separate TIFFs named by their caption number (ESI figures are embedded in esi.docx)
figs = re.findall(r"!\[Fig\. (\d+) .*?\]\((?:\.\./)?figures/([\w.-]+)\.(?:png|tif)\)",
                  (ROOT / "manuscript" / "03c_figures.md").read_text(encoding="utf-8"), flags=re.S)
targets = [(f"Fig{n}.tif", stem) for n, stem in figs] + [("TOC_graphic.tif", "toc_graphic")]
assert [int(n) for n, _ in figs] == list(range(1, len(figs) + 1)), figs
for name, stem in targets:
    f = ROOT / "figures" / f"{stem}.tif"
    if not f.exists():
        problems.append(f"missing {f.name}")
        continue
    im = Image.open(f)
    dpi = float(im.info.get("dpi", (0, 0))[0])
    w, h = (round(x / dpi * 2.54, 2) for x in im.size)
    if dpi < 600:
        problems.append(f"{f.name} {dpi} dpi")
    if stem == "toc_graphic":
        if w > 8.0 + 1e-6 or h > 4.0 + 1e-6:
            problems.append(f"TOC graphic {w} x {h} cm")
    else:
        if min(abs(w - 8.3), abs(w - 17.1)) > 0.05 or h > 23.3:
            problems.append(f"{f.name} {w} x {h} cm")
    shutil.copy(f, figdir / name)
    print(f"{name} <- {f.name}: {w} x {h} cm, {dpi:.0f} dpi")

files = sorted(p for p in SUB.rglob("*") if p.is_file())
if len(files) > 20:
    problems.append(f"{len(files)} files (ZIP limit 20)")
z = SUB.parent / "submission_rsc_advances.zip"
with zipfile.ZipFile(z, "w", zipfile.ZIP_DEFLATED) as zf:
    for p in files:
        zf.write(p, p.relative_to(SUB))
print(f"abstract {n_abs} words; TOC text {len(toc)} characters; {len(files)} files -> {z.name}")
print("PROBLEMS: " + "; ".join(problems) if problems else "all automatic checks passed")
