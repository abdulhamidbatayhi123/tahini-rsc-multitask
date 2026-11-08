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
sample-level bootstrap; this was corrected for all reported intervals. Table S8 collects analyses added at the review stage: a paired test of the two decision routes,
detection by nominal level, results without the pure-adulterant samples and the lot-wise blank of PLS. Table S9 gives an exploratory one-class baseline
(principal-component T² and Q fitted on authentic training scans only).

## S3 Training histories

![Fig. S1 MT-DNN training histories in leave-one-lot-out validation: (a) inner-validation binary cross-entropy of the class head and (b) mean squared error of the composition head (fractions scaled to 0–1), median over five seeds for each withheld lot; dots mark the epoch chosen by early stopping for each seed.](figures/figS1_histories.png)

## S4 Hold-out quantification

![Fig. S2 Quantification on the grouped hold-out test set (17 samples, one authentic lot): predicted against nominal tahini fraction for (a) PLS regression and (b) the MT-DNN composition head. Points are sample means and bars ±1 SD over scans.](figures/fig4_quantification_holdout.png)

## S5 Supplementary tables
