"""Build the manuscript: manuscript/*.md (in order) -> build/out/manuscript.md -> .docx (pandoc).

Citations: [@key] or [@a;@b] -> superscript numbers in order of first citation (RSC: after punctuation,
commas without spaces, en dash for three or more consecutive). "ref. [#key]" -> "ref. N".
Reference list from manuscript/references.json in RSC Vancouver form:
A. Name, B. Name and C. Name, Journal Abbrev., year, volume, pages.
Gates: every cited key exists and is marked verified; no TODO left (warn); no unused reference (warn)."""
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MS = ROOT / "manuscript"
OUT = ROOT / "build" / "out"
OUT.mkdir(parents=True, exist_ok=True)
ORDER = ["00_front.md", "01_introduction.md", "02_experimental.md", "03_results.md", "04_conclusions.md",
         "05_declarations.md"]


def compress(nums):
    nums = sorted(set(nums))
    out, i = [], 0
    while i < len(nums):
        j = i
        while j + 1 < len(nums) and nums[j + 1] == nums[j] + 1:
            j += 1
        out.append(f"{nums[i]}–{nums[j]}" if j - i >= 2 else ",".join(map(str, nums[i:j + 1])))
        i = j + 1
    return ",".join(out)


def fmt_ref(r):
    a = r["authors"]
    names = a[0] if len(a) == 1 else ", ".join(a[:-1]) + " and " + a[-1]
    if r.get("type") == "data":
        return f"{names}, {r['repository']}, {r['title']}, {r['year']}, DOI: {r['doi']}."
    if r.get("type") == "book":
        return f"{names}, {r['title']}, {r['publisher']}, {r['place']}, {r['year']}."
    if r.get("type") == "web":
        return f"{r['title']}, {r['url']}, (accessed {r['accessed']})."
    s = f"{names}, *{r['journal']}*, {r['year']}, **{r['volume']}**, {r['pages']}"
    return s + (f", DOI: {r['doi']}." if r.get("doi") else ".")


def main():
    refs = json.loads((MS / "references.json").read_text(encoding="utf-8"))
    text = "\n\n".join((MS / f).read_text(encoding="utf-8") for f in ORDER if (MS / f).exists())
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)           # source comments stay in the sources
    order = []

    def num(k):
        if k not in refs:
            sys.exit(f"GATE: unknown reference key {k}")
        if not refs[k].get("verified"):
            print(f"WARN: reference {k} not yet verified live")
        if k not in order:
            order.append(k)
        return order.index(k) + 1

    def cite(m):
        keys = [k.strip().lstrip("@") for k in m.group(1).split(";")]
        return "^" + compress([num(k) for k in keys]) + "^"

    text = re.sub(r"\[(@[^\]]+)\]", cite, text)
    text = re.sub(r"\[#([\w-]+)\]", lambda m: str(num(m.group(1))), text)
    # RSC: superscript after punctuation
    text = re.sub(r"(\^[0-9,–]+\^)([.,;:])", r"\2\1", text)
    reflist = "\n".join(f"{i + 1}. {fmt_ref(refs[k])}" for i, k in enumerate(order))
    text += "\n\n## References\n\n" + reflist + "\n"
    for k in refs:
        if k not in order:
            print(f"WARN: reference {k} not cited")
    if "TODO" in text:
        print("WARN: TODO left in text")
    md = OUT / "manuscript.md"
    md.write_text(text, encoding="utf-8")
    subprocess.run(["pandoc", str(md), "-o", str(OUT / "manuscript.docx"), "--resource-path", str(ROOT)],
                   check=True)
    words = len(re.sub(r"## References.*", "", text, flags=re.S).split())
    print(f"built {OUT / 'manuscript.docx'}; {len(order)} references; ~{words} words incl. captions")


if __name__ == "__main__":
    main()
