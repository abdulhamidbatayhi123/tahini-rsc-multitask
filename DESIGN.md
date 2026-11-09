# Analysis plan (fixed 2026-11-08, BEFORE any grouped result was computed)

Target journal: RSC Advances (Royal Society of Chemistry). Authors (from the user, 2026-11-08): Arzu Yılmaz, Abdulhamid Batayhi, Muhammed Özgölet, Muhammet Arici.

## Question
Can one multitask neural network screen tahini (sesame paste) for substitution with sunflower or peanut
paste AND estimate the composition from a single ATR-FTIR spectrum, when tested on physical samples and
production lots it has never seen? How does it compare with the standard chemometric pair PLS-DA + PLS?

## Data
Released tahini ATR-FTIR set of Batayhi et al., Foods 2026, 15, 3639 (doi:10.3390/foods15203639;
data CC-BY-4.0, github.com/abdulhamidbatayhi123/kanfood-tahini-mango-, Zenodo 10.5281/zenodo.21446757).
1554 spectra, 1762 channels (600-4000 cm-1), 55 physical samples (`isim`): 5 authentic lots T1-T5
(150-151 scans each) and 50 blends (14-17 scans each). Lot = prefix of `isim`.
The paper must cite the Foods article as the data source and state what is new here.

## Why the preliminary results are not used
The preliminary figures (`originals_preliminary/`) come from a scan-level random 80/20 split.
`audit/check_split.py` reproduces their test counts (150 pure / 161 adulterated) with
`train_test_split(test_size=0.2, random_state=42)`; that split puts 54 of 55 physical samples on both
sides. The feature importance peaks at the atmospheric CO2 (~2350 cm-1) and water-vapour (>3600 cm-1)
regions. The preliminary run is reproduced (script `src/s01_run.py random` (random scheme)) and reported
in the ESI only as the leakage contrast.

## Fixed choices
- Unit of splitting: physical sample (`isim`); replicate scans never cross a split.
- Primary partition: the Foods grouped 70/30 hold-out (GroupShuffleSplit seed 42), so numbers are
  comparable with the published benchmark.
- Off-distribution test: leave-one-lot-out (5 folds), all selection nested inside each fold.
- Scan-level predictions are reported, AND sample-level predictions (mean over a sample's scans), since
  in practice a sample is scanned several times.
- Spectral input, primary: SNV-normalised absorbance over the chemically informative regions
  2800-3050 cm-1 and 600-1800 cm-1 (CO2 2250-2400 and water-vapour bands excluded).
  Sensitivity: full 600-4000 cm-1.
- Models:
  1. MT-DNN (multitask): shared Dense(128, ReLU) -> Dropout(0.2) -> Dense(64, ReLU); head A sigmoid
     (adulterated yes/no, BCE); head B softmax x 100 over (tahini, sunflower, peanut) so the composition
     sums to 100 % (MSE in fraction units). Loss = BCE + w * MSE, w fixed at 1 after scaling fractions to
     0-1. Adam, lr 1e-3, batch 32, max 300 epochs, early stopping (patience 30) on a grouped inner
     validation split (20 % of training samples); the best-validation-loss weights are restored.
     5 seeds; reported as mean (and seed spread).
  2. PLS-DA (PLS2 on the one-hot class, threshold 0.5) and PLS regression on the three fractions
     (outputs clipped at 0 and rescaled to 100). Number of components 1-25 chosen by grouped 5-fold CV
     inside the training set (minimum RMSECV).
  3. Decision from regression (PLS route "PLS-R"): "adulterated" when the predicted adulterant fraction
     exceeds mean + 3 SD of the predicted adulterant fraction of the training authentic scans, taken
     from grouped 5-fold CV predictions inside the training set (amended 2026-11-08 before results:
     in-sample predictions would understate the SD; the MT-DNN uses its own classification head).
- Leakage contrast (ESI): the same models also run on the scan-level random 80/20 split
  (train_test_split seed 42) that reproduces the preliminary figures.
- Metrics: classification - sensitivity, specificity, balanced accuracy, ROC AUC, confusion matrix;
  identification - share of adulterated samples whose dominant predicted adulterant is the true one;
  quantification - R2, RMSEP and MAE of the tahini fraction (and per component); LOD as in Foods:
  LOD = 3.3 sigma / S, sigma = SD of the predicted adulterant fraction on withheld authentic scans,
  S = slope of predicted on nominal adulterant fraction (computed on leave-one-lot-out predictions).
- Intervals: cluster bootstrap over physical samples (1000 draws); lot-level results also shown per
  lot, since five lots are a coarse resampling level.
- Any analysis added after the first grouped results are seen is labelled exploratory.

## Amendments (each logged with what had been seen)
- A1 (2026-11-08). Seen: ONLY the MT-DNN training histories of the scan-level random scheme (no grouped
  result). With w = 1 the regression term (~0.001-0.005) was negligible against the BCE, and on a grouped
  inner validation set the BCE rose from epoch 1-2 (to 3.6 by epoch 31) while the composition MSE kept
  falling, so early stopping picked epoch 1 for two of five seeds. Changes: w = 10; label smoothing 0.05
  on the class target; Adam weight decay 1e-4; early stopping only after 20 epochs. Added: the MT-DNN
  regression route "MT-DNN-R" (same mean + 3 SD rule as PLS-R, threshold from grouped 5-fold CV inside
  the training set), because the observation suggests the class head may not transfer to new samples
  while the composition head does; the class head vs regression route comparison is therefore
  pre-specified from here on, and was first seen in the random-scheme histories.

## Exploratory analyses added after the leave-one-lot-out results (2026-11-08)
Labelled exploratory in the paper; none changes a primary metric.
- E1 `src/s03_lots.py`: departure of each authentic lot's mean SNV spectrum from the other four (pooled
  within-lot SD units) and its projection on the fold's PLS-R tahini coefficient; pure-paste band
  differences. Motivated by every route flagging one withheld authentic lot (PLS-R: T5; MT-DNN: T1).
- E2 `src/s04_consensus.py`: sample-level rule flagging a sample only when PLS-R and MT-DNN-R both flag
  it. Chosen after seeing that the two families fail on different lots, so it is a hypothesis for new
  lots, not a validated result (five authentic lots).
- `src/f6_lots.py` (Fig. 5) draws E1 and the withheld-lot predictions.

## Amendment A2 (2026-11-08, after the v1 lot-out results; found by an independent code review)
- Problem: the MT-DNN never trained on its grouped inner-validation samples (20 % of training samples). In
  lot-out validation this removed one or two of the four training authentic lots from training in 20 of
  25 (fold, seed) fits, so the network learned "authentic" from fewer lots than PLS. This contradicts the
  intent "all selection repeated inside the training lots" and tilts the PLS vs MT-DNN comparison.
- Fix: early stopping on the inner split chooses only the number of epochs; the network is then retrained
  from scratch on all training samples for that number of epochs (same seed and settings), and inputs are
  standardised with the mean and SD of all training samples. The same applies to the inner-CV fits that
  produce the MT-DNN-R threshold. PLS is unchanged.
- Also fixed: the sample-level cluster bootstrap merged duplicate draws of a sample into one (intervals too
  narrow); each drawn copy now keeps its own label. Sample-level AUC of the regression routes now uses the
  raw mean score (decisions still use each fold's threshold).
- Reporting: A2 results are primary. The v1 (pre-A2) predictions and metrics are kept in results/v1_A1/ and
  compared in the ESI, so the effect of the fix is visible.
- Wording: the plan called the hold-out the primary partition; the manuscript treats leave-one-lot-out as
  the main test because the hold-out holds a single authentic lot (decided after seeing that the hold-out
  specificity rests on one sample). Both are reported in full.

## Review-stage analyses (2026-11-09, after the A2 results; requested by an internal adversarial review)
All exploratory; none changes a reported primary result.
- S8 (`src/s05_extra.py` -> `results/extra.json`): exact McNemar test of class route vs regression route per model family
  on the 55 withheld samples; share of blend scans flagged per nominal level (each level lies in one lot, so this is
  confounded with the lot effect); sensitivity, slope and LOD without the two pure-adulterant samples; PLS blank by lot and
  LOD with each lot left out of the blank.
- One-class baseline (`src/s06_oneclass.py`): PCA T²/Q fitted on authentic training scans only, limits = mean + 3 SD of
  out-of-fold statistics (leave-one-training-lot-out), the same rule as the regression routes.
- Second review round (cs T-TR3, 2026-11-09): second-derivative spectra of the authentic lots (`src/fS3_derivative.py` ->
  `results/derivative_bands.json`, ESI Fig. S3); thresholds robust to output saturation, recomputed per fold
  (`src/s07_robust_threshold.py` -> `results/robust_threshold.json`, ESI Table S10); reproduction of the pre-A2
  early-stopping sets (`audit/a2_val_split.py` -> `results/a2_val_split.json`).

## Corrections ledger
- 2026-11-08 A2: MT-DNN retrained on all training samples (early-stopping samples had been excluded from training).
- 2026-11-08: sample-level bootstrap merged duplicate draws; fixed (each draw relabelled), all intervals recomputed.
- 2026-11-09 text: PLS-DA misses at 32/36 % ("most" -> "about a third"); Foods LOD range attribution (pooled
  out-of-fold, not nested lot-out); T2 largest departure is 717 cm-1, not 1709; "about twice" -> "two and a half times";
  LOD convention cited to ICH Q2(R2), not Allegrini & Olivieri; Kačuráková & Wilson author list.
- 2026-11-09 T-TR3: lot-out MT-DNN scan RMSEP 3.96 -> 3.95 (file 3.9547; three places); "at least 99 %" -> "at least
  98.7 %"; ESI Table S3 regenerated from the unrounded lot_departure.csv (T2 1709 +4.05, not +4.1); abstract RMSE marked
  scan level; full-range sentence completed (PLS-R flags 29 % of T1 scans, MT-DNN T1 RMSEP 9.76 %); ESI tables in
  numerical order; Fig. 3 in percent; J. Am. Oil Chem. Soc. abbreviation; McNemar power statement (maximum
  p = 0.0625 with five authentic samples); one-class component cap and T1 margin stated; class balance stated.
- 2026-11-09 T-TR3 B4: second-derivative spectra show no band shift or extra component for T1 (1180–1280 cm-1) or T2
  (1709, 717 cm-1); the band assignments in Section 3.5, the abstract, the conclusions and the cover letter were
  withdrawn in favour of "broad absorbance difference".
- 2026-11-09 data citation: version DOI 10.5281/zenodo.23168994 (v2.2.0 = pinned commit 3004a07) instead of the concept DOI.
- 2026-11-09 T-TR3 B2 completed (all 5 folds x 5 seeds): stored thresholds reproduced to 1e-15; MT-DNN-R rejects T1 and
  no other lot with every seed under every alternative rule (T1-fold thresholds 0.30–2.01 %); PLS-R rejects T5 under all
  but the logit rule (not meaningful for clipped PLS; sensitivity 30 %). ESI Table S10, one sentence each in 2.8 and 3.5.
