## 2 Experimental

### 2.1 Samples and spectra

The spectra are the tahini set released with our earlier calibration study (ref. [#batayhi2026]), where the
sample preparation is described in full; it is summarised here. Five authentic tahini (sesame paste)
samples, each from a different production lot (T1–T5), were obtained from suppliers in Istanbul, and
sunflower paste and peanut paste from a local supermarket. Each lot was blended with each adulterant at
five levels between 4 and 100 % (w/w) in 4 % steps, interleaved across lots so that every level occurs
once per adulterant: T1 4, 24, 44, 64 and 84 %; T2 8, 28, 48, 68 and 88 %; T3 12, 32, 52, 72 and 92 %;
T4 16, 36, 56, 76 and 96 %; T5 20, 40, 60, 80 and 100 %. With the five unblended lots this gives 55
physical samples. Blends were homogenised with a spatula for 2 min. Spectra were recorded on a Bruker
Tensor 27 FTIR spectrometer (Bruker Optik GmbH, Ettlingen, Germany) with a ZnSe ATR accessory, at
4 cm<sup>−1</sup> resolution over 4000–600 cm<sup>−1</sup> with 16 co-added scans, and the sample was repositioned on
the crystal between acquisitions. Each blend was scanned 14 to 17 times and each authentic lot 150 or
151 times, giving 1554 spectra (754 authentic, 800 blends) of 1762 channels.
<!-- counts: results/f1_numbers.json n_auth=754; audit/check_split.py output (1554, 55 samples); source_repo/data/tahini/README.md -->

Every spectrum carries the three mass fractions (tahini, sunflower paste, peanut paste), which sum to
100 %, and a binary label (authentic or adulterated). The 100 % sunflower and 100 % peanut samples of lot
T5 are pure adulterant and are labelled adulterated.

### 2.2 Preprocessing and spectral regions

Each spectrum was corrected by the standard normal variate (SNV),[@barnes1989] computed over the full
600–4000 cm<sup>−1</sup> range; SNV acts on one spectrum at a time and therefore cannot leak information between
training and test sets. The models were then given the
two regions that carry the chemistry of the pastes, 2800–3050 cm<sup>−1</sup> (C–H stretching) and
600–1800 cm<sup>−1</sup> (carbonyl, amide and fingerprint bands), 752 channels in total. The atmospheric CO<sub>2</sub>
band (about 2250–2400 cm<sup>−1</sup>) and the water-vapour rotation lines above 3550 cm<sup>−1</sup> were excluded because
they record the state of the optical path, not the sample. The full 600–4000 cm<sup>−1</sup> range was run as a
sensitivity analysis (ESI, Table S7).
<!-- n_channels_chem=752: results/f1_numbers.json -->

### 2.3 Multitask network

The multitask deep neural network (MT-DNN) has a shared trunk of two fully connected layers (128 and 64
units, ReLU activation, dropout 0.2 after the first) and two heads (Fig. 2). Head A is a single sigmoid
unit that gives the probability that the scan is adulterated. Head B is a three-unit softmax whose
outputs, multiplied by 100, are the tahini, sunflower and peanut fractions; the softmax makes the
predicted composition non-negative and sum to 100 % by construction. The loss is the binary
cross-entropy of head A (targets smoothed by 0.05) plus ten times the mean squared error of head B on
fractions scaled to 0–1. Training used Adam (learning rate 10<sup>−3</sup>, weight decay 10<sup>−4</sup>, batch size 32) for at
most 300 epochs. The number of epochs was chosen by early stopping on the loss of an inner validation
set of 20 % of the training samples, drawn by physical sample, with a patience of 30 epochs after a
minimum of 20. The network was then retrained from the same initialisation on all training samples for
the chosen number of epochs, so that every training sample, and every training lot, contributed to the
final model; inputs were standardised channel by channel with the mean and SD of all training samples.
Every MT-DNN result is the mean over five random seeds. The network was implemented in
PyTorch 2.7.1.
<!-- architecture and settings: src/common.py MTDNN, MTNet; DESIGN.md + amendment A1 -->

### 2.4 Chemometric reference models

The reference is the standard chemometric pair: partial least-squares discriminant analysis (PLS-DA)
on the one-hot class and PLS2 regression on the three fractions, without scaling of the SNV inputs
(scikit-learn 1.7.0). The number of latent variables (1–25) of each model was chosen inside every
training set by grouped five-fold cross-validation (minimum root-mean-square error of
cross-validation). PLS2 predictions were clipped at zero and rescaled to sum to 100 %.
<!-- src/common.py PLSPair, select_pls_k; versions: python -c import sklearn (1.7.0) -->

### 2.5 Two routes to a screening decision

Each model family gives two decisions. The class route uses the classification output directly: the
sigmoid probability above 0.5 for the MT-DNN, and the larger of the two PLS-DA responses. The
regression route (written PLS-R and MT-DNN-R) flags a scan as adulterated when its predicted adulterant
fraction (100 % minus the predicted tahini fraction) exceeds a threshold set on the training data alone:
the mean plus three SDs of the predicted adulterant fraction of the authentic training scans. These
predictions were taken from a grouped five-fold cross-validation inside the training set, because
predictions on the training scans themselves would understate their spread; the cross-validation
groups are physical samples, so an authentic training lot is withheld in it while its blends are not,
and the threshold is then applied to the model refitted on the whole training set. For sample-level
decisions, the scans of one physical sample were averaged (the predicted adulterant fraction for the
regression routes, the logit of the MT-DNN class head and the difference of the two PLS-DA responses
for the class routes) and the mean was compared with the same threshold, or with zero.

### 2.6 Validation

The unit of splitting is the physical sample. Replicate scans of one sample are far more alike than
scans of different samples, so a split that separates them would test the model on near-copies of its
training data. Two designs were used. The first is the grouped 70/30 hold-out of ref. [#batayhi2026], which puts
38 samples (1146 spectra) in training and 17 samples (408 spectra) in the test set, so that the results
can be compared with the published benchmark. It contains a single authentic lot and no blend below
16 % adulterant. The second, and the main test of this paper, is leave-one-lot-out validation: each
production lot is withheld in turn with its ten blends (five folds), and all selection, scaling, early
stopping and threshold setting is repeated inside the remaining four lots. Because each lot carries its
own adulteration levels, every level from 4 to 100 % and every authentic lot is predicted exactly once by
a model that never saw that lot. To show how much a scan-level split inflates the apparent accuracy,
the same models were also run on a random 80/20 split of the scans (ESI).
<!-- holdout sizes: results/run_info_holdout_chem.json n_train=1146 n_test=408 samples_test=17 -->

### 2.7 Metrics and statistics

Screening was scored by sensitivity, specificity, balanced accuracy and the area under the receiver
operating characteristic curve (AUC), at scan level and, after averaging the scans of each sample, at
sample level. The adulterant was taken as identified when the larger predicted adulterant fraction
belonged to the true adulterant. Quantification was scored on the tahini fraction by the coefficient of
determination (R<sup>2</sup>), the root-mean-square error of prediction (RMSEP) and the mean absolute error. The
limit of detection followed the calibration-slope convention of ICH Q2(R2)[@ich2023] used in ref. [#batayhi2026],
LOD = 3.3σ/S, where σ is the SD of the predicted adulterant fraction of withheld authentic scans and S the
slope of predicted on nominal adulterant fraction; the more rigorous multivariate LOD interval of
Allegrini and Olivieri[@allegrini2014] was not used, for comparability with the earlier study. Because a
bounded output and a lot-wise bias both distort σ, the share of blend scans flagged at each nominal
level is also reported, the empirical alternative that the guideline allows. In leave-one-lot-out validation the predictions of the five
withheld lots are pooled, so σ includes the differences between authentic lots; within the hold-out test
set, which holds a single authentic lot, σ reflects replicate scatter only and the LOD is given for
comparison. All 95 % intervals are cluster-bootstrap percentiles (1000 draws) that
resample whole physical samples, never single scans;[@field2007] for the MT-DNN each draw averages the five seeds.
With five lots the lot level is too coarse to resample, so lot-out results are also reported fold by
fold.

### 2.8 Exploratory analyses

Two analyses were added after the leave-one-lot-out results had been seen and are reported as
exploratory. For each authentic lot, the mean SNV spectrum of the lot minus the mean of the other four
lot means was divided by the within-lot SD (the mean of the five per-lot SDs), to locate the bands in which the lot departs from
the others, and the unscaled difference was projected on the tahini coefficient vector of the PLS-R
model that had withheld that lot, to estimate how far the departure alone moves the PLS prediction. A
sample-level agreement rule, which flags a sample only when both regression routes (PLS-R and MT-DNN-R)
flag it, was also evaluated. At a later internal review stage we added an exact McNemar test of the
two decision routes within each model family on the 55 withheld samples, results by nominal level and
without the two pure-adulterant samples (ESI, Table S8), and a one-class baseline: principal-component
analysis of the mean-centred authentic training scans (components chosen to explain 99 % of the
variance, at most 15), flagging a scan when Hotelling's T² or the residual Q exceeded its limit, set at
mean + 3 SD of the out-of-fold values obtained by leaving out one training lot at a time (ESI, Table S9).
Code, predictions and the analysis plan with its amendments are in the
repository (Data availability).
