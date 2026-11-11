# RSC Advances submission checklist

Read from the live author guidelines on 2026-11-10:
https://www.rsc.org/publishing/publish-with-us/publish-a-journal-article/rsc-advances

| Requirement (RSC) | Status |
|---|---|
| Article text as Word, PDF or LaTeX; template optional | build/build.py -> manuscript.docx |
| Abstract: single paragraph, about 50–250 words | 239 words, no acronyms (package.py gate: at most 240, margin under the cap) |
| Vancouver numbered superscript references, CASSI abbreviations, all author names | references.json via Crossref; CASSI map |
| Figures TIFF, 600 dpi or more, 8.3 or 17.1 cm wide, at most 23.3 cm high | all 17.1 cm, 600 dpi (figures/*.tif) |
| Author contributions (CRediT recommended) | 05_declarations.md |
| Conflicts of interest ("There are no conflicts to declare") | 05_declarations.md |
| Data availability after conflicts, before acknowledgements; full URLs; code version | 05_declarations.md (data v2.2.0, code v1.1.0) |
| Funding in Acknowledgements; generative-AI use declared in three places as RSC's author-responsibilities page requires (read live 2026-11-11): cover letter, Experimental (Section 2.9, how the tool was used incl. prompts), Acknowledgements (tool and version) | 05_declarations.md, 02_experimental.md §2.9, cover_letter.md |
| Cover letter with a statement of importance, addressed to the Executive Editor, same title as the manuscript; no reviewer names in it | cover_letter.md |
| Preferred reviewers: entered in ScholarOne only | none (authors 2026-11-11); fallback list in the private hub if the field is mandatory |
| ESI submitted with the original submission | esi.docx |
| TOC entry (required at revision): graphic max 8 x 4 cm, TIFF 600 dpi; text 1–2 sentences, max 250 characters, not a repeat of title/abstract, editable (.docx) | figures/toc_graphic.tif 8.0 x 4.0 cm; manuscript/toc.md 201 characters |
| Upload: up to 5 files at once, or a ZIP of up to 20 files | |
| APC if accepted: GBP 2,200 + local taxes (Research4Life Group A/B: waiver) | for the corresponding author |
| Scope: must advance chemistry; papers with little chemistry are out of scope | spectral interpretation (Sec. 3.5, ESI Fig. S3) carries the chemistry |
| Optional: transparent peer review | author choice in ScholarOne |

## Checklist 1b pass (2026-11-11, PAPER_WORKFLOW_LESSONS.md section 1b)

- Abstract and title without acronyms; abstract 239 words (margin under 250).
- Word layout: build/make_reference_docx.py (A4, bold headings, continuous line numbers, page numbers).
- Build gate: raw HTML super/subscripts are converted for Word (cm⁻¹, R², T² were flat before); the build refuses any left.
- Two fresh-eyes reviews in read-only subagents: readability (hardest sentences, undefined terms, logic jumps) and
  compliance against the live RSC Advances guidelines and author-responsibilities page; fixes applied.
- Pages looked at in PDFs exported with Microsoft Word (page 1, a figure page, references).
- Peer review is single-anonymised (RSC Advances guidelines): names in the manuscript are correct; no anonymised copy needed.
- Professor package: python build/professor_package.py -> build/tahini_rsc_professor_package.zip (numbered upload
  files, copy-paste form sheet generated from the manuscript, Word reading PDFs, README).
