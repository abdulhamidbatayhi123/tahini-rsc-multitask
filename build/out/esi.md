---
title: "Electronic supplementary information for: Screening tahini for sunflower and peanut paste on unseen production lots: a multitask neural network and partial least squares on ATR–FTIR spectra"
---

## S1 Why the preliminary analysis was rebuilt

The analysis began from a preliminary run in which the 1554 scans were divided at random into training
and test sets (80/20). Reproducing that division (scikit-learn `train_test_split`, seed 42) showed that
replicate scans of 54 of the 55 physical samples fell on both sides, so the test set consisted largely
of near-copies of training scans (`audit/check_split.py` in the repository). The preliminary run reported
an AUC of 0.9998 and two misclassified test scans; its figures are kept in `originals_preliminary/` of
the repository. All results in the article come from the rebuilt analysis, whose plan was fixed before
any grouped result was seen (`DESIGN.md`).

## S2 Amendments to the analysis plan

Two amendments were made and are dated in `DESIGN.md`. Amendment A1 was made after seeing only the
training histories of the random scheme: the class-head loss dominated and rose on unseen samples from
the first epochs, so the composition loss was weighted by 10, label smoothing (0.05), weight decay
(10<sup>−4</sup>) and a minimum of 20 epochs were added, and the MT-DNN regression route was added to the
comparison. Amendment A2 was made after the first lot-out results, when an independent review of the
code showed that the network never trained on its early-stopping samples, which in lot-out validation
removed one or two of the four training authentic lots from training in most fits. The network is now
retrained on all training samples for the number of epochs chosen by early stopping. Table S6 compares
the results before and after A2. The same review found that duplicate draws were merged in the
sample-level bootstrap; this was corrected for all reported intervals.

## S3 Training histories

![Fig. S1 MT-DNN training histories in leave-one-lot-out validation: (a) inner-validation binary cross-entropy of the class head and (b) mean squared error of the composition head (fractions scaled to 0–1), median over five seeds for each withheld lot; dots mark the epoch chosen by early stopping for each seed.](figures/figS1_histories.png)

## S4 Hold-out quantification

![Fig. S2 Quantification on the grouped hold-out test set (17 samples, one authentic lot): predicted against nominal tahini fraction for (a) PLS regression and (b) the MT-DNN composition head. Points are sample means and bars ±1 SD over scans.](figures/fig4_quantification_holdout.png)

## S5 Supplementary tables


**Table S1 Settings chosen inside each leave-one-lot-out training set (chemically informative regions).**

| Withheld lot | Training scans | Test scans | PLS2 latent variables | PLS-DA latent variables | PLS-R threshold (% adulterant) | MT-DNN-R threshold, range over seeds (% adulterant) | MT-DNN best epoch (seeds 0–4) |
|---|---|---|---|---|---|---|---|
| T1 | 1243 | 311 | 14 | 22 | 7.06 | 0.46–1.24 | 87, 68, 62, 56, 37 |
| T2 | 1243 | 311 | 14 | 4 | 8.55 | 1.75–5.05 | 93, 55, 34, 50, 65 |
| T3 | 1244 | 310 | 14 | 2 | 8.02 | 3.20–5.94 | 92, 23, 50, 79, 43 |
| T4 | 1243 | 311 | 11 | 3 | 6.36 | 2.04–3.19 | 82, 79, 34, 69, 28 |
| T5 | 1243 | 311 | 15 | 3 | 6.08 | 3.63–6.52 | 66, 51, 37, 57, 21 |

Source: results/run_info_lolo_chem.json.

**Table S2 Results for each withheld lot (scan level; MT-DNN routes: mean of five seeds).**

| Withheld lot | Route | Authentic scans flagged (%) | Blend scans missed (%) | RMSEP (% tahini) | R² | Identification (%) |
|---|---|---|---|---|---|---|
| T1 | MT-DNN | 77.7 | 1.4 | 6.14 | 0.957 | 95.5 |
| T1 | MT-DNN-R | 93.9 | 0.0 |  |  |  |
| T1 | PLS-DA | 100.0 | 0.0 |  |  |  |
| T1 | PLS-R | 1.3 | 9.9 | 3.16 | 0.989 | 99.4 |
| T2 | MT-DNN | 5.3 | 0.0 | 3.32 | 0.988 | 96.5 |
| T2 | MT-DNN-R | 3.8 | 1.4 |  |  |  |
| T2 | PLS-DA | 52.3 | 0.0 |  |  |  |
| T2 | PLS-R | 0.0 | 0.0 | 3.82 | 0.985 | 93.8 |
| T3 | MT-DNN | 0.0 | 0.0 | 2.91 | 0.992 | 99.4 |
| T3 | MT-DNN-R | 0.0 | 2.3 |  |  |  |
| T3 | PLS-DA | 0.0 | 30.2 |  |  |  |
| T3 | PLS-R | 0.0 | 0.0 | 3.40 | 0.989 | 100.0 |
| T4 | MT-DNN | 0.0 | 0.2 | 3.65 | 0.989 | 93.4 |
| T4 | MT-DNN-R | 0.0 | 0.0 |  |  |  |
| T4 | PLS-DA | 0.0 | 26.9 |  |  |  |
| T4 | PLS-R | 0.0 | 3.1 | 4.35 | 0.984 | 93.1 |
| T5 | MT-DNN | 0.0 | 0.0 | 3.61 | 0.990 | 100.0 |
| T5 | MT-DNN-R | 0.0 | 0.0 |  |  |  |
| T5 | PLS-DA | 0.0 | 0.6 |  |  |  |
| T5 | PLS-R | 100.0 | 0.0 | 7.97 | 0.952 | 100.0 |

Source: results/metrics_lot.csv. R² within one lot is computed over that lot's 11 samples only.

**Table S3 Exploratory: how each authentic lot departs from the other four.**

| Lot | RMS departure (pooled SD) | Largest departures, cm⁻¹ (SD units) | Projected PLS adulterant shift (points) | Observed PLS-R mean (% adulterant) | Observed MT-DNN mean (% adulterant) |
|---|---|---|---|---|---|
| T1 | 1.61 | 1215 (-8.3); 1273 (-5.5); 1248 (-4.9); 733 (-3.5); 1190 (-2.3); 1362 (-2.1) | +3.0 | 3.58 | 2.65 |
| T2 | 1.11 | 717 (+4.2); 1709 (+4.0); 743 (+2.3); 1117 (-2.2); 781 (+2.1); 3015 (+2.0) | +0.8 | 3.82 | 0.66 |
| T3 | 1.36 | 1620 (+2.3); 1711 (-2.3); 1574 (+2.2); 1670 (+2.2); 1645 (+2.1); 1317 (+2.0) | +1.5 | 3.98 | 0.12 |
| T4 | 1.31 | 1246 (+5.4); 1217 (+3.7); 717 (-3.7); 1273 (+3.0); 1134 (-2.4); 1352 (+2.4) | -12.6 | 2.33 | 0.03 |
| T5 | 1.26 | 1213 (+4.1); 908 (+3.0); 1134 (+2.7); 1452 (-2.7); 883 (+2.5); 1703 (-2.5) | +8.9 | 10.34 | 0.18 |

Source: results/lot_departure.json (src/s03_lots.py). The projected shift is the unscaled departure multiplied by the sunflower and peanut PLS2 coefficients of the model that withheld the lot, before clipping; observed values are the mean predicted adulterant fraction of the lot's authentic scans.

**Table S4 Largest differences between the pure adulterant pastes and authentic tahini (mean SNV spectra).**

| Paste | Scans | Wavenumber, cm⁻¹ (difference, SNV units) |
|---|---|---|
| sunflower paste, 100 % | 17 | 2920 (-0.287); 989 (+0.250); 602 (+0.249); 669 (+0.224); 2851 (-0.220); 1051 (+0.203); 623 (+0.202); 644 (+0.178) |
| peanut paste, 100 % | 16 | 2920 (+0.637); 2853 (+0.498); 1655 (-0.294); 1041 (-0.283); 1101 (-0.261); 1063 (-0.232); 1749 (+0.214); 1132 (-0.208) |

Source: results/lot_departure.json.

**Table S5 Exploratory sample-level agreement rule (leave-one-lot-out; 5 authentic and 50 blend samples).**

| Rule | Seed | Authentic lots flagged | Blends missed (level, adulterant, lot) |
|---|---|---|---|
| PLS-R | – | T5 | 4 % peanut (T1) |
| MT-DNN-R | 0 | T1 | none |
| PLS-R and MT-DNN-R | 0 | none | 4 % peanut (T1) |
| MT-DNN-R | 1 | T1 | none |
| PLS-R and MT-DNN-R | 1 | none | 4 % peanut (T1) |
| MT-DNN-R | 2 | T1 | none |
| PLS-R and MT-DNN-R | 2 | none | 4 % peanut (T1) |
| MT-DNN-R | 3 | T1 | none |
| PLS-R and MT-DNN-R | 3 | none | 4 % peanut (T1) |
| MT-DNN-R | 4 | T1 | none |
| PLS-R and MT-DNN-R | 4 | none | 4 % peanut (T1) |

Source: results/consensus.json (src/s04_consensus.py).


