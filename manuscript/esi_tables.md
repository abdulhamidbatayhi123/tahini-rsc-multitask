**Table S1 Settings chosen inside each leave-one-lot-out training set (chemically informative regions).**

| Withheld lot | Training scans | Test scans | PLS2 latent variables | PLS-DA latent variables | PLS-R threshold (% adulterant) | MT-DNN-R threshold, range over seeds (% adulterant) | MT-DNN best epoch (seeds 0–4) |
|---|---|---|---|---|---|---|---|
| T1 | 1243 | 311 | 14 | 22 | 7.06 | 0.40–0.78 | 87, 68, 62, 56, 37 |
| T2 | 1243 | 311 | 14 | 4 | 8.55 | 1.82–3.70 | 93, 55, 34, 50, 65 |
| T3 | 1244 | 310 | 14 | 2 | 8.02 | 3.65–5.16 | 92, 23, 50, 79, 43 |
| T4 | 1243 | 311 | 11 | 3 | 6.36 | 2.56–4.46 | 82, 79, 34, 69, 28 |
| T5 | 1243 | 311 | 15 | 3 | 6.08 | 3.70–4.88 | 66, 51, 37, 57, 21 |

Source: results/run_info_lolo_chem.json.

**Table S2 Results for each withheld lot (scan level; MT-DNN routes: mean of five seeds).**

| Withheld lot | Route | Authentic scans flagged (%) | Blend scans missed (%) | RMSEP (% tahini) | R² | Identification (%) |
|---|---|---|---|---|---|---|
| T1 | MT-DNN | 98.0 | 0.0 | 5.46 | 0.966 | 95.3 |
| T1 | MT-DNN-R | 100.0 | 0.0 |  |  |  |
| T1 | PLS-DA | 100.0 | 0.0 |  |  |  |
| T1 | PLS-R | 1.3 | 9.9 | 3.16 | 0.989 | 99.4 |
| T2 | MT-DNN | 3.0 | 0.0 | 2.36 | 0.994 | 95.1 |
| T2 | MT-DNN-R | 0.3 | 0.0 |  |  |  |
| T2 | PLS-DA | 52.3 | 0.0 |  |  |  |
| T2 | PLS-R | 0.0 | 0.0 | 3.82 | 0.985 | 93.8 |
| T3 | MT-DNN | 0.0 | 0.0 | 3.05 | 0.991 | 99.7 |
| T3 | MT-DNN-R | 0.0 | 0.3 |  |  |  |
| T3 | PLS-DA | 0.0 | 30.2 |  |  |  |
| T3 | PLS-R | 0.0 | 0.0 | 3.40 | 0.989 | 100.0 |
| T4 | MT-DNN | 0.0 | 0.2 | 4.06 | 0.986 | 95.9 |
| T4 | MT-DNN-R | 0.0 | 0.0 |  |  |  |
| T4 | PLS-DA | 0.0 | 26.9 |  |  |  |
| T4 | PLS-R | 0.0 | 3.1 | 4.35 | 0.984 | 93.1 |
| T5 | MT-DNN | 0.0 | 0.0 | 4.03 | 0.988 | 100.0 |
| T5 | MT-DNN-R | 0.0 | 0.0 |  |  |  |
| T5 | PLS-DA | 0.0 | 0.6 |  |  |  |
| T5 | PLS-R | 100.0 | 0.0 | 7.97 | 0.952 | 100.0 |

Source: results/metrics_lot.csv. R² within one lot is computed over that lot's 11 samples only.

**Table S3 Exploratory: how each authentic lot departs from the other four.**

| Lot | RMS departure (pooled SD) | Largest departures, cm⁻¹ (SD units) | Projected PLS adulterant shift (points) | Observed PLS-R mean (% adulterant) | Observed MT-DNN mean (% adulterant) |
|---|---|---|---|---|---|
| T1 | 1.61 | 1215 (-8.3); 1273 (-5.5); 1248 (-4.9); 733 (-3.5); 1190 (-2.3); 1362 (-2.1) | +3.0 | 3.58 | 2.92 |
| T2 | 1.11 | 717 (+4.2); 1709 (+4.0); 743 (+2.3); 1117 (-2.2); 781 (+2.1); 3015 (+2.0) | +0.8 | 3.82 | 0.41 |
| T3 | 1.36 | 1620 (+2.3); 1711 (-2.3); 1574 (+2.2); 1670 (+2.2); 1645 (+2.1); 1317 (+2.0) | +1.5 | 3.98 | 0.08 |
| T4 | 1.31 | 1246 (+5.4); 1217 (+3.7); 717 (-3.7); 1273 (+3.0); 1134 (-2.4); 1352 (+2.4) | -12.6 | 2.33 | 0.02 |
| T5 | 1.26 | 1213 (+4.1); 908 (+3.0); 1134 (+2.7); 1452 (-2.7); 883 (+2.5); 1703 (-2.5) | +8.9 | 10.34 | 0.12 |

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

**Table S6 MT-DNN results before / after amendment A2 (refit on all training samples; chemically informative regions; point estimates, means over five seeds). PLS results are not affected by A2.**

| Validation | Level | Route | Sensitivity (%) | Specificity (%) | AUC | RMSEP (% tahini) | LOD (%) |
|---|---|---|---|---|---|---|---|
| holdout | sample | MT-DNN | 100.0 / 100.0 | 100.0 / 100.0 | 1.000 / 1.000 | 3.98 / 3.79 | 0.07 / 0.03 |
| holdout | sample | MT-DNN-R | 100.0 / 100.0 | 100.0 / 100.0 | 1.000 / 1.000 | 3.98 / 3.79 |  |
| holdout | scan | MT-DNN | 99.6 / 100.0 | 100.0 / 100.0 | 1.000 / 1.000 | 4.02 / 3.95 |  |
| holdout | scan | MT-DNN-R | 100.0 / 100.0 | 100.0 / 100.0 | 1.000 / 1.000 | 4.02 / 3.95 |  |
| lolo | sample | MT-DNN | 100.0 / 100.0 | 84.0 / 80.0 | 0.998 / 0.998 | 4.64 / 4.55 | 3.81 / 4.10 |
| lolo | sample | MT-DNN-R | 100.0 / 100.0 | 80.0 / 80.0 | 0.998 / 1.000 | 4.64 / 4.55 |  |
| lolo | scan | MT-DNN | 99.7 / 100.0 | 83.5 / 79.9 | 0.995 / 0.996 | 4.11 / 3.95 |  |
| lolo | scan | MT-DNN-R | 99.3 / 100.0 | 80.6 / 80.1 | 0.999 / 1.000 | 4.11 / 3.95 |  |
| random | sample | MT-DNN | 99.6 / 100.0 | 96.0 / 100.0 | 0.998 / 1.000 | 2.80 / 3.15 | 0.75 / 0.37 |
| random | sample | MT-DNN-R | 97.1 / 97.6 | 100.0 / 100.0 | 1.000 / 1.000 | 2.80 / 3.15 |  |
| random | scan | MT-DNN | 99.3 / 99.9 | 95.7 / 100.0 | 0.991 / 1.000 | 2.52 / 2.75 |  |
| random | scan | MT-DNN-R | 97.8 / 97.8 | 100.0 / 100.0 | 1.000 / 1.000 | 2.52 / 2.75 |  |

Source: results/v1_A1/metrics.csv (before) and results/metrics.csv (after).

<!-- generated by src/esi_tables.py; do not edit by hand -->
