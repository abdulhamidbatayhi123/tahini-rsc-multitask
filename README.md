# Screening tahini for sunflower and peanut paste on unseen production lots

Code, analysis plan, predictions and manuscript sources for the paper *"Screening tahini for sunflower
and peanut paste on unseen production lots: a multitask neural network and partial least squares on
ATR–FTIR spectra"* (in preparation for *RSC Advances*).

The study reuses the tahini ATR–FTIR spectra released with Batayhi et al., *Foods* 2026, **15**, 3639
(<https://doi.org/10.3390/foods15203639>; data: <https://doi.org/10.5281/zenodo.21446757>). It
compares a multitask neural network (classification head + softmax composition head) with PLS-DA and
PLS regression under sample-grouped hold-out and leave-one-lot-out validation, and compares two ways of
reaching the authentic/adulterated decision: the classification output, or a cut-off on the predicted
composition.

## Main results (leave-one-lot-out; `results/metrics.csv`)

| Route | Sensitivity, samples | Specificity, samples | Withheld authentic lot rejected |
|---|---|---|---|
| PLS-DA | 88 % | 60 % | T1, half of T2 |
| PLS-R (cut-off on predicted composition) | 98 % | 80 % | T5 |
| MT-DNN class head | 100 % | 84 % | T1 |
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
| `src/f*.py`, `src/t*.py` | Figures (RSC artwork rules asserted in `figstyle.py`) and generated tables |
| `results/` | Predictions, run information (selected components, thresholds, input hashes), metrics |
| `figures/` | PDF, 600 dpi TIFF and PNG of every figure, each with a provenance file (script and input hashes) |
| `manuscript/`, `build/` | Markdown sources and the builder (citations checked live on Crossref; `build/build.py` -> `.docx`) |
| `audit/check_split.py` | Shows that the preliminary scan-level split put 54 of 55 samples on both sides |
| `originals_preliminary/` | Figures of the preliminary (leaked) analysis that motivated the rebuild |

## Reproduce

```bash
pip install -r requirements.txt
bash get_data.sh            # clones the data repository at the pinned commit into source_repo/
bash run_all.sh             # all schemes, one at a time (CPU; about 30 min per scheme and region set)
cd src && python s02_metrics.py 1000 && python s03_lots.py && python s04_consensus.py
python f1_spectra.py && python f2_workflow.py && python f3_detection.py lolo && python f4_quantification.py lolo && python f6_lots.py
python t1_table.py && python t2_leakage.py
cd .. && python build/build.py   # needs pandoc
```

Tested with Python 3.13.5, PyTorch 2.7.1 (CPU), scikit-learn 1.7.0, NumPy 2.2.6, pandas 2.3.0,
matplotlib 3.10.3 on Windows 11. Network results are means over five seeds; exact values can differ in
the last digits on other hardware or library versions.

## Licence

Code: MIT (`LICENSE`). The spectra are not redistributed here; they are CC BY 4.0 from the data
repository above. Please cite the paper and the data record when using this code.
