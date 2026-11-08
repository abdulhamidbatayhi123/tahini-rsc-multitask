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
  3. Decision from regression (both models): "adulterated" when the predicted adulterant fraction
     exceeds a threshold set on training data as mean + 3 SD of the predicted adulterant fraction of
     the training authentic scans (the Foods LOD convention).
- Metrics: classification - sensitivity, specificity, balanced accuracy, ROC AUC, confusion matrix;
  identification - share of adulterated samples whose dominant predicted adulterant is the true one;
  quantification - R2, RMSEP and MAE of the tahini fraction (and per component); LOD as in Foods.
- Intervals: cluster bootstrap over physical samples (1000 draws); lot-level results also shown per
  lot, since five lots are a coarse resampling level.
- Any analysis added after the first grouped results are seen is labelled exploratory.
