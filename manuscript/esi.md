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
removed one (15 of the 25 fold–seed fits) or two (5 fits) of the four authentic training lots from training
(results/a2_val_split.json, audit/a2_val_split.py). The network is now
retrained on all training samples for the number of epochs chosen by early stopping. Table S6 compares
the results before and after A2. The same review found that duplicate draws were merged in the
sample-level bootstrap; this was corrected for all reported intervals. Table S8 collects analyses added at the review stage: a paired test of the two decision routes,
detection by nominal level, results without the pure-adulterant samples and the lot-wise blank of PLS. Table S9 gives an exploratory one-class baseline
(principal-component T² and Q fitted on authentic training scans only), and Table S10 the regression-route decisions
under alternative threshold rules (src/s07_robust_threshold.py, which recomputes the cross-validated training
predictions that set the thresholds and reproduces the stored thresholds within 2 × 10⁻¹⁵). Table S11 gives
indicators of the optical path (atmospheric CO₂ band and water-vapour lines) for each lot (src/s08_session.py). Table S12 repeats the lot-out analysis with SNV computed over the retained
regions only and with the fingerprint region cut at 700 cm⁻¹.

## S3 Training histories

![Fig. S1 MT-DNN training histories in leave-one-lot-out validation: (a) inner-validation binary cross-entropy of the class head and (b) mean squared error of the composition head (fractions scaled to 0–1), median over five seeds for each withheld lot; dots mark the epoch chosen by early stopping for each seed.](figures/figS1_histories.png)

## S4 Hold-out quantification

![Fig. S2 Quantification on the grouped hold-out test set (17 samples, one authentic lot): predicted against nominal tahini fraction for (a) PLS regression and (b) the MT-DNN composition head. Points are sample means and bars ±1 SD over scans.](figures/fig4_quantification_holdout.png)

## S4b Second-derivative spectra of the authentic lots

![Fig. S3 Second-derivative spectra (Savitzky–Golay, 13 points = 23 cm<sup>−1</sup>, second-order polynomial, of the SNV spectra) of the five authentic lots, lot means with ±1 SD bands: (a) 1150–1300 cm<sup>−1</sup>, lot T1 against the other lots; (b) 1680–1780 cm<sup>−1</sup> and (c) 690–740 cm<sup>−1</sup>, lot T2 against the other lots. Dotted lines mark the band minima of the other four lots; the shaded band in (b) is 1700–1718 cm<sup>−1</sup>, where free fatty acids absorb. Band positions agree within 0.3 cm<sup>−1</sup> in all lots, and no separate component is resolved near 1215, 1248, 1709 or 717 cm<sup>−1</sup>; windows of 9 and 17 points give the same result (results/derivative_bands.json).](figures/figS3_derivative.png)

## S5 Supplementary tables
