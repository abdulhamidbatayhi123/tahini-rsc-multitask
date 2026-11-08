# Analysis plan (fixed 2026-11-08, BEFORE any grouped result was computed)

Target journal: RSC Advances (Royal Society of Chemistry). Authors: to be supplied by the user.

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
regions. The preliminary run is reproduced (script `src/s00_reproduce_random_split.py`) and reported
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
