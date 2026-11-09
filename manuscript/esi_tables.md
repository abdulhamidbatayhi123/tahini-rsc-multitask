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
| T1 | 1.61 | 1215 (-8.35); 1273 (-5.48); 1248 (-4.90); 733 (-3.50); 1190 (-2.34); 1362 (-2.07) | +3.0 | 3.58 | 2.92 |
| T2 | 1.11 | 717 (+4.25); 1709 (+4.05); 743 (+2.31); 1117 (-2.17); 781 (+2.06); 3015 (+2.02) | +0.8 | 3.82 | 0.41 |
| T3 | 1.36 | 1620 (+2.28); 1711 (-2.26); 1574 (+2.22); 1670 (+2.17); 1645 (+2.14); 1317 (+2.05) | +1.5 | 3.98 | 0.08 |
| T4 | 1.31 | 1246 (+5.40); 1217 (+3.71); 717 (-3.70); 1273 (+2.98); 1134 (-2.39); 1352 (+2.36) | -12.6 | 2.33 | 0.02 |
| T5 | 1.26 | 1213 (+4.10); 908 (+3.01); 1134 (+2.69); 1452 (-2.66); 883 (+2.52); 1703 (-2.51) | +8.9 | 10.34 | 0.12 |

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

**Table S7 Sensitivity analysis: chemically informative regions (752 channels) / full 600–4000 cm⁻¹ range (scan level).**

| Validation | Route | Sensitivity (%) | Specificity (%) | RMSEP (% tahini) |
|---|---|---|---|---|
| holdout | PLS-DA | 90.3 / 91.8 | 100.0 / 100.0 | 1.93 / 2.02 |
| holdout | PLS-R | 100.0 / 100.0 | 100.0 / 100.0 | 1.93 / 2.02 |
| holdout | MT-DNN | 100.0 / 100.0 | 100.0 / 100.0 | 3.95 / 4.04 |
| holdout | MT-DNN-R | 100.0 / 99.8 | 100.0 / 100.0 | 3.95 / 4.04 |
| lolo | PLS-DA | 88.5 / 92.1 | 69.6 / 79.4 | 4.87 / 5.32 |
| lolo | PLS-R | 97.4 / 99.5 | 79.7 / 74.3 | 4.87 / 5.32 |
| lolo | MT-DNN | 100.0 / 100.0 | 79.9 / 80.1 | 3.95 / 5.73 |
| lolo | MT-DNN-R | 100.0 / 97.2 | 80.1 / 79.9 | 3.95 / 5.73 |
| random | PLS-DA | 95.0 / 91.9 | 99.3 / 100.0 | 1.79 / 1.97 |
| random | PLS-R | 95.0 / 95.0 | 100.0 / 100.0 | 1.79 / 1.97 |
| random | MT-DNN | 99.9 / 99.4 | 100.0 / 100.0 | 2.75 / 2.73 |
| random | MT-DNN-R | 97.8 / 97.5 | 100.0 / 100.0 | 2.75 / 2.73 |

Source: results/metrics.csv (regions chem and full).

**Table S8 Supplementary analyses (leave-one-lot-out, chemically informative regions; added at review stage).**

| Analysis | Seed | Result |
|---|---|---|
| Paired routes, PLS | – | class right / regression wrong: 2; reverse: 8; exact McNemar p = 0.11 |
| Paired routes, MT-DNN | seed 0 | class right / regression wrong: 0; reverse: 0; exact McNemar p = 1.00 |
| Paired routes, MT-DNN | seed 1 | class right / regression wrong: 0; reverse: 0; exact McNemar p = 1.00 |
| Paired routes, MT-DNN | seed 2 | class right / regression wrong: 0; reverse: 0; exact McNemar p = 1.00 |
| Paired routes, MT-DNN | seed 3 | class right / regression wrong: 0; reverse: 0; exact McNemar p = 1.00 |
| Paired routes, MT-DNN | seed 4 | class right / regression wrong: 0; reverse: 0; exact McNemar p = 1.00 |
| Detection by level, PLS-DA | – | every level ≥ 56 % flagged in ≥ 95 % of scans; levels below 95 %: 12 %: 0; 16 %: 3; 32 %: 66; 36 %: 62; 52 %: 81 |
| Detection by level, PLS-R | – | every level ≥ 20 % flagged in ≥ 95 % of scans; levels below 95 %: 4 %: 50; 16 %: 84 |
| Detection by level, MT-DNN | – | every level ≥ 4 % flagged in ≥ 95 % of scans; levels below 95 %: none |
| Detection by level, MT-DNN-R | – | every level ≥ 4 % flagged in ≥ 95 % of scans; levels below 95 %: none |
| Without pure adulterants, PLS-DA | – | sample sensitivity 88.0 % (50 blends) / 87.5 % (48 blends) |
| Without pure adulterants, PLS-R | – | sample sensitivity 98.0 % (50 blends) / 97.9 % (48 blends) |
| Without pure adulterants, MT-DNN | – | sample sensitivity 100.0 % (50 blends) / 100.0 % (48 blends) |
| Without pure adulterants, MT-DNN-R | – | sample sensitivity 100.0 % (50 blends) / 100.0 % (48 blends) |
| Without pure adulterants, PLS-R | – | slope 0.940 / 0.937; LOD 11.1 / 11.1 % adulterant |
| Without pure adulterants, MT-DNN | – | slope 0.976 / 0.986; LOD 4.1 / 4.1 % adulterant |
| PLS-R blank by lot | – | T1: 3.6 ± 1.4 %; T2: 3.8 ± 1.8 %; T3: 4.0 ± 1.4 %; T4: 2.3 ± 0.7 %; T5: 10.3 ± 1.6 % |
| PLS-R LOD, lot left out of the blank | – | T1: 11.9 %; T2: 11.9 %; T3: 12.1 %; T4: 11.4 %; T5: 5.2 % |

Source: results/extra.json (src/s05_extra.py). Each nominal level occurs in one lot only, so detection by level is confounded with the lot effect (lot T1 holds the 4 % blends).

**Table S9 Exploratory one-class baseline: PCA fitted on authentic training scans only, flag when T² or Q exceeds its limit (leave-one-lot-out, chemically informative regions; added at review stage).**

| Setting (components, limit) | Scan sensitivity (%) | Scan specificity (%) | Sample sensitivity (%, 50 blends) | Sample specificity (%, 5 lots) | Blends missed (% adulterant) | Authentic scans flagged T1/T2/T3/T4/T5 (%) |
|---|---|---|---|---|---|---|
| k2, sd3 | 81.4 | 86.3 | 78 | 100 | 4, 4, 8, 12, 12, 16, 16, 20, 20, 24, 36 | 0 / 34 / 34 / 0 / 1 |
| k2, p99 | 80.9 | 88.5 | 80 | 100 | 4, 4, 12, 12, 16, 16, 20, 20, 24, 36 | 0 / 40 / 17 / 0 / 0 |
| k2, combined, sd3 | 74.0 | 95.0 | 72 | 100 | 4, 4, 8, 8, 12, 12, 16, 16, 20, 20, 24, 24, 32, 36 | 0 / 1 / 23 / 0 / 2 |
| k5, sd3 | 81.4 | 97.5 | 82 | 100 | 4, 4, 8, 12, 12, 16, 20, 32, 36 | 2 / 11 / 0 / 0 / 0 |
| k5, p99 | 82.8 | 97.6 | 84 | 100 | 4, 4, 8, 12, 12, 16, 32, 36 | 2 / 10 / 0 / 0 / 0 |
| k5, combined, sd3 | 76.4 | 98.7 | 78 | 100 | 4, 4, 8, 12, 12, 16, 20, 32, 36, 40, 52 | 0 / 7 / 0 / 0 / 0 |
| k10, sd3 | 81.4 | 94.7 | 82 | 100 | 4, 8, 8, 12, 12, 16, 20, 28, 32 | 27 / 0 / 0 / 0 / 0 |
| k10, p99 | 84.6 | 95.0 | 84 | 100 | 4, 4, 8, 8, 12, 12, 16, 28 | 25 / 0 / 0 / 0 / 0 |
| k10, combined, sd3 | 75.6 | 93.1 | 76 | 100 | 4, 8, 8, 12, 12, 16, 20, 28, 32, 36, 48, 52 | 35 / 0 / 0 / 0 / 0 |
| main, sd3 | 82.4 | 91.4 | 82 | 100 | 4, 8, 8, 12, 12, 16, 20, 28, 32 | 43 / 0 / 0 / 0 / 0 |
| main, p99 | 86.0 | 92.7 | 86 | 100 | 4, 8, 8, 12, 12, 16, 28 | 37 / 0 / 0 / 0 / 0 |
| main, combined, sd3 | 78.2 | 91.5 | 78 | 100 | 8, 8, 12, 12, 16, 20, 28, 32, 36, 48, 52 | 43 / 0 / 0 / 0 / 0 |

Source: results/oneclass.json. sd3: mean + 3 SD of out-of-fold statistics (leave-one-training-lot-out), the rule used for the regression routes; p99: 99th percentile; combined: T²/T²₀ + Q/Q₀. The 99 % explained-variance rule reached the cap of 15 components in every fold.

**Table S10 Exploratory: regression-route decisions with alternative threshold rules (leave-one-lot-out, sample level; MT-DNN-R: mean over five seeds, range in parentheses).**

| Route | Threshold rule | Threshold by withheld lot (% adulterant) | Sensitivity (%, 50 blends) | Specificity (%, 5 lots) | Authentic lots rejected |
|---|---|---|---|---|---|
| MT-DNN-R | mean + 3 SD (as reported) | T1 0.40–0.78; T2 1.82–3.70; T3 3.65–5.16; T4 2.56–4.46; T5 3.70–4.88 | 100 | 80 | T1 |
| MT-DNN-R | mean + 3 SD on logit scale | T1 0.63–2.01; T2 8.16–42.79; T3 27.87–77.39; T4 13.00–50.97; T5 37.55–57.81 | 70 (62–84) | 80 | T1 |
| MT-DNN-R | 99th percentile | T1 0.52–0.86; T2 1.80–3.47; T3 3.62–5.11; T4 2.40–4.60; T5 3.01–4.52 | 100 | 80 | T1 |
| MT-DNN-R | 99.9th percentile | T1 0.77–1.42; T2 2.31–5.98; T3 5.13–6.93; T4 2.84–8.00; T5 3.55–5.43 | 100 (98–100) | 80 | T1 |
| MT-DNN-R | mean + 3 SD of sample means | T1 0.30–0.73; T2 1.72–3.98; T3 3.53–5.18; T4 2.53–4.36; T5 3.62–5.02 | 100 | 80 | T1 |
| PLS-R | mean + 3 SD (as reported) | T1 7.06; T2 8.55; T3 8.02; T4 6.36; T5 6.08 | 98 | 80 | T5 |
| PLS-R | mean + 3 SD on logit scale | T1 83.79; T2 53.04; T3 82.90; T4 84.14; T5 61.37 | 30 | 100 | none |
| PLS-R | 99th percentile | T1 7.06; T2 8.12; T3 7.70; T4 6.41; T5 5.29 | 98 | 80 | T5 |
| PLS-R | 99.9th percentile | T1 7.98; T2 9.75; T3 8.91; T4 7.50; T5 6.37 | 94 | 80 | T5 |
| PLS-R | mean + 3 SD of sample means | T1 6.29; T2 7.14; T3 7.43; T4 5.98; T5 3.31 | 100 | 80 | T5 |

Source: results/robust_threshold.json (src/s07_robust_threshold.py). Thresholds are computed from grouped five-fold cross-validation predictions on the authentic training scans, recomputed with the code of the main analysis (stored thresholds reproduced to 10⁻¹⁵). The logit rule is not meaningful for PLS-R, whose clipped output places many authentic training scans at exactly 0 % adulterant; the sample-mean rule rests on four authentic training samples.

<!-- generated by src/esi_tables.py; do not edit by hand -->
