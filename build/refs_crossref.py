"""Verify references live on Crossref and write manuscript/references.json in RSC form.

Input: manuscript/refs_wanted.tsv  (key <TAB> doi-or-'?' <TAB> title words for search)
For each entry the DOI is resolved (or searched by title), the record's title is compared with the
wanted title (token overlap), and authors/journal/year/volume/pages are taken from the Crossref record.
No e-mail address is sent. Output keeps 'verified': true only when the title overlap >= 0.8.
Entries of type book/web/data are kept from manual_refs.json (checked by hand, see that file)."""
import json
import re
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

MS = Path(__file__).resolve().parents[1] / "manuscript"
UA = {"User-Agent": "tahini-rsc-refcheck/1.0 (python urllib)"}


def get(url):
    for attempt in range(4):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30) as r:
                return json.loads(r.read().decode())
        except Exception as e:  # noqa: BLE001
            if attempt == 3:
                raise
            time.sleep(2 + 3 * attempt)


def toks(s):
    return set(re.findall(r"[a-z0-9]+", re.sub(r"<[^>]+>", " ", s.lower())))


def overlap(a, b):
    A, B = toks(a), toks(b)
    i = len(A & B)
    return min(i / max(1, len(A)), i / max(1, len(B)))      # symmetric: both titles must match


def initials(given):
    parts = re.split(r"[\s]+", given.strip())
    out = []
    for p in parts:
        sub = p.split("-")
        out.append("-".join(s[0] + "." for s in sub if s))
    return " ".join(out)


def to_rsc(msg):
    authors = []
    for a in msg.get("author", []):
        if "family" in a:
            authors.append((initials(a.get("given", "")) + " " + a["family"]).strip())
        elif "name" in a:
            authors.append(a["name"])
    journal = (msg.get("short-container-title") or msg.get("container-title") or [""])[0]
    year = (msg.get("published-print") or msg.get("published-online") or msg.get("issued"))["date-parts"][0][0]
    pages = msg.get("page") or msg.get("article-number") or ""
    pages = pages.replace("-", "–")
    return dict(authors=authors, journal=journal, year=year, volume=msg.get("volume", ""), pages=pages,
                doi=msg["DOI"], title=(msg.get("title") or [""])[0], type_crossref=msg.get("type"))


def main():
    out = {}
    manual = MS / "manual_refs.json"
    if manual.exists():
        out.update(json.loads(manual.read_text(encoding="utf-8")))
    rows = [l.rstrip("\n").split("\t") for l in (MS / "refs_wanted.tsv").read_text(encoding="utf-8").splitlines()
            if l.strip() and not l.startswith("#")]
    for key, doi, title in rows:
        try:
            if doi != "?":
                msg = get("https://api.crossref.org/works/" + urllib.parse.quote(doi))["message"]
            else:
                q = urllib.parse.quote(title)
                items = get(f"https://api.crossref.org/works?query.bibliographic={q}&rows=8")["message"]["items"]
                items = [m for m in items if m.get("type") != "component" and ".s0" not in m["DOI"]]
                msg = max(items, key=lambda m: overlap(title, (m.get("title") or [""])[0]))
            r = to_rsc(msg)
            r["title_overlap"] = round(overlap(title, r["title"]), 2)
            r["verified"] = r["title_overlap"] >= 0.8
            r["checked"] = time.strftime("%Y-%m-%d") + " Crossref"
            out[key] = r
            print(f"{key:24s} {r['verified']!s:5s} {r['title_overlap']:.2f} {r['doi']}  {r['title'][:70]}")
        except Exception as e:  # noqa: BLE001
            print(f"{key:24s} ERROR {e}", file=sys.stderr)
        time.sleep(0.4)
    (MS / "references.json").write_text(json.dumps(out, indent=1, ensure_ascii=False), encoding="utf-8")


if __name__ == "__main__":
    main()
