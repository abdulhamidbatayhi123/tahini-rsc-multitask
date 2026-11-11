# Screening tahini for sunflower and peanut paste on unseen production lots

Code, analysis plan, predictions and manuscript sources for the paper *"Screening tahini for sunflower
and peanut paste on unseen production lots: a multitask neural network and partial least squares on
ATR–FTIR spectra"* (in preparation for *RSC Advances*).

Archived release: v1.1.0, <https://doi.org/10.5281/zenodo.24120431> (all versions: <https://doi.org/10.5281/zenodo.24087710>). Please cite the paper and this archive
(see `CITATION.cff`).

The study reuses the tahini ATR–FTIR spectra released with Batayhi et al., *Foods* 2026, **15**, 3639
(<https://doi.org/10.3390/foods15203639>; data: <https://doi.org/10.5281/zenodo.23168994>, v2.2.0). It
compares a multitask neural network (classification head + softmax composition head) with PLS-DA and
PLS regression under sample-grouped hold-out and leave-one-lot-out validation, and compares two ways of
reaching the authentic/adulterated decision: the classification output, or a cut-off on the predicted
composition.

## Main results (leave-one-lot-out; `results/metrics.csv`)

| Route | Sensitivity, samples | Specificity, samples | Withheld authentic lot rejected |
|---|---|---|---|
| PLS-DA | 88 % | 60 % | T1, half of T2 |
| PLS-R (cut-off on predicted composition) | 98 % | 80 % | T5 |
| MT-DNN class head | 100 % | 80 % | T1 |
| MT-DNN-R (cut-off on predicted composition) | 100 % | 80 % | T1 |

A scan-level random split (54 of 55 samples on both sides) hides these false positives completely
(Table 2 of the paper). Analyses added after the results were seen are labelled exploratory in
`DESIGN.md`.

## Layout

| Path | Content |
|---|---|
| `DESIGN.md` | Analysis plan fixed before the grouped results, with dated amendments and the exploratory analyses |
| `src/common.py` | Data loading, SNV, regions, splits, PLS pair, multitask network, metrics, cluster bootstrap |
| `src/s01_run.py` | Runs all models for one validation scheme (`random`, `holdout`, `lolo`) and region set (`chem`, `full`) |
| `src/s02_metrics.py` | Metrics, cluster-bootstrap intervals, per-lot results, LOD |
| `src/s03_lots.py`, `src/s04_consensus.py` | Exploratory: lot departure spectra; two-route agreement rule |
| `src/s05_extra.py`, `src/s06_oneclass.py`, `src/s07_robust_threshold.py` | Review-stage analyses: paired McNemar test, detection by level, one-class PCA baseline, saturation-robust thresholds (ESI Tables S8–S10) |
| `audit/a2_val_split.py` | Reproduces the inner early-stopping sets removed before amendment A2 (`results/a2_val_split.json`) |
| `src/f*.py`, `src/t*.py` | Figures (RSC artwork rules asserted in `figstyle.py`) and generated tables |
| `results/` | Predictions, run information (selected components, thresholds, input hashes), metrics |
| `figures/` | PDF, 600 dpi TIFF and PNG of every figure, each with a provenance file (script and input hashes) |
| `manuscript/`, `build/` | Markdown sources and the builder (citations checked live on Crossref; `build/build.py` -> `.docx`) |
| `src/s08_session.py` | Optical-path indicators (CO₂ band, water-vapour lines) by lot (`results/session_indicators.json`, ESI Table S11) |
| `audit/check_split.py` | Shows that the preliminary scan-level split put 54 of 55 samples on both sides |
| `originals_preliminary/` | Figures of the preliminary (leaked) analysis that motivated the rebuild |

## Reproduce

```bash
pip install -r requirements.txt
bash get_data.sh            # clones the data repository at the pinned commit into source_repo/
bash run_all.sh             # all schemes and input variants, one at a time (CPU; 0.5-4 h per run on a shared machine)
cd src && python s02_metrics.py 1000 && python s03_lots.py && python s04_consensus.py
python s04_consensus.py chemsnv && python s04_consensus.py chem700
python s05_extra.py && python s06_oneclass.py && TORCH_THREADS=6 python s07_robust_threshold.py && python s08_session.py
python ../audit/a2_val_split.py
python f1_spectra.py && python f2_workflow.py && python f3_detection.py lolo && python f4_quantification.py lolo && python f6_lots.py
python fS1_histories.py && python f4_quantification.py holdout && python fS3_derivative.py && python fTOC.py
python t1_table.py && python t2_leakage.py && python esi_tables.py
cd .. && python build/build.py && python build/build.py esi   # needs pandoc
python build/make_reference_docx.py   # Word style template (line and page numbers)
python build/package.py            # RSC Advances submission package (build/submission_rsc_advances.zip)
python build/professor_package.py   # package for the submitting author (numbered files, form sheet, Word PDFs)
```

`s07_robust_threshold.py` reads the cross-validated training predictions cached in `audit/robust_cv/` and needs no
network training; delete that folder to recompute them (25 network fits plus PLS, a few hours on CPU; 20 of the 25 fits
took 1.8 h in the original run, `results/robust_threshold_run.log`). Bit-exact agreement with the stored thresholds
needs `TORCH_THREADS=6`, the thread count of the original run. Other thread counts change the network predictions
slightly, because rounding differences can shift the early-stopping epoch: with 2 threads (fold T1, seed 0, cached in
`audit/robust_cv/threads2_dnn_T1_s0.csv`) the mean + 3 SD threshold was 0.80 % instead of 0.76 %.

Tested with Python 3.13.5, PyTorch 2.7.1 (CPU), scikit-learn 1.7.0, NumPy 2.2.6, pandas 2.3.0,
matplotlib 3.10.3 on Windows 11. Network results are means over five seeds; exact values can differ in
the last digits on other hardware or library versions.

## Licence

Code: MIT (`LICENSE`). The spectra are not redistributed here; they are CC BY 4.0 from the data
repository above. Please cite the paper and the data record when using this code.
