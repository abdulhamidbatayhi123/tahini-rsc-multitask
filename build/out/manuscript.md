---
title: "Screening tahini for sunflower and peanut paste on unseen production lots: a multitask neural network and partial least squares on ATR–FTIR spectra"
---


Arzu Yılmaz,^a^ Abdulhamid Batayhi,^b^ Muhammed Özgölet\*^a^ and Muhammet Arici^a^

^a^ Department of Food Engineering, Faculty of Chemical and Metallurgical Engineering, Yildiz Technical University, 34220 Istanbul, Türkiye. E-mail: mozgolet@yildiz.edu.tr
^b^ Department of Mechatronics Engineering, Faculty of Mechanical Engineering, Yildiz Technical University, 34220 Istanbul, Türkiye.

Electronic supplementary information (ESI) available. See DOI: to be assigned.

## Abstract

Tahini is substituted with cheaper oilseed pastes, and peanut paste adds an undeclared allergen. We
tested whether a multitask neural network screens tahini for sunflower or peanut paste and
estimates the substitution from one attenuated total reflectance Fourier-transform infrared (ATR–FTIR)
spectrum of a production lot it was not calibrated on, and whether the screening
decision should come from a classification head or from the predicted composition. On 1554 spectra
of 55 physical samples from five tahini lots, the network and partial least squares discriminant analysis and
regression (PLS-DA, PLS) were validated with whole samples or lots withheld. On a grouped
hold-out, every route accepted the authentic test lot. With each lot withheld in turn, blends
were still detected (sample-level sensitivity 98–100% for the composition routes) and the
composition was predicted with a scan-level root-mean-square error of 4.0–4.9% tahini, but every route rejected at
least one authentic lot (specificity 60–80%). The classification head showed no advantage over a
cut-off on the predicted composition. The rejected lot differed between model families: lot T1, the most
atypical lot (a broad absorbance difference near 1180–1280 cm<sup>−1</sup>), for the network, and lot T5,
whose spectral departure lies along the PLS regression vector, for PLS. A post hoc rule flagging a
sample only when both composition routes agreed accepted all five authentic lots, as it must once the
families reject different lots, and detected 49 of 50 blends. Differences between authentic lots, not model architecture, limited screening; here they cannot be separated
from the measurement session.



## 1 Introduction

Tahini is a paste of roasted, hulled sesame seeds and a staple of Middle Eastern and Mediterranean
cuisine. Its price invites substitution with cheaper oilseed pastes such as sunflower or peanut paste,
which look and taste similar once blended. Substitution with peanut is also a safety problem, because
peanut is a major allergen and tahini consumers who avoid peanut have no reason to suspect it; products
sold as tahini have been recalled for undeclared peanut.^1^ Targeted reference methods exist:
gas chromatography of the fatty acids detects foreign oils in sesame oil;^2^ real-time PCR
and liquid chromatography–mass spectrometry detect allergenic nuts at mg kg<sup>−1</sup>
levels;^3–5^ and nuclear magnetic resonance spectroscopy detects peanut in other
foods.^6^ They are slow, need trained staff and answer only the question they
were designed for. A rapid screen that flags a suspect sample and estimates how much of it is not
tahini would decide which samples are worth sending to such a laboratory.

Mid-infrared spectroscopy with attenuated total reflectance (ATR–FTIR) fits that role. It needs no
sample preparation, takes about a minute per spectrum, and records the bands of the lipids, proteins and
carbohydrates that make up an oilseed paste.^7,8^ Combined with chemometrics,
infrared spectroscopy has been used to authenticate edible oils,^9–11^ to
follow lipid oxidation in a sunflower kernel paste^12^ and, more recently, to authenticate tahini:
Kucukcelebioglu et al. built one-class ATR–FTIR and UV–Vis models for tahini spiked with peanut or sunflower
oil.^13^ Earlier, Temiz et al. had quantified sunflower oil in the oil extracted from tahini
by synchronous fluorescence spectroscopy.^14^ Both studies used an oil as the adulterant. We
released 1554 ATR–FTIR spectra of tahini blended with sunflower or peanut paste and compared six
calibration models on them.^15^ The chemistry makes the task hard: the three pastes are
dominated by the same triglyceride bands, so adulteration changes the intensity of shared bands rather
than adding new ones.^15^ The standard chemometric answer is a pair of models, partial
least-squares discriminant analysis (PLS-DA) for the yes-or-no decision and PLS regression for the
amount.^16,17^

Neural networks can replace such pairs with one model. In multitask learning, related outputs share a
common hidden representation and are trained together, so that each task can act as a regulariser for
the other.^18^ Multitask networks that classify and quantify adulteration from one spectrum
have been reported for olive oil by Raman spectroscopy,^19,20^ for turmeric powder^21^ and
chicken in lamb^22^ by near-infrared spectroscopy, for protein adulterants in milk powder by laser-induced
breakdown spectroscopy^23^ and for Fritillaria bulb powder by hyperspectral imaging,^24^ and the coupling between identifying a component and estimating
its concentration has been treated as a learning problem in its own right.^25^ For screening,
the two tasks are tied by definition: a sample is adulterated exactly when its tahini fraction is below
100 %. A network with a classification head and a composition head therefore offers two ways to reach
the same decision, either directly from the classification head (a qualitative limit test) or by
comparing the predicted composition with a cut-off (a quantitative test with a decision limit). Which of
the two should make the decision when the network meets material it was not calibrated on has not, to
our knowledge, been tested. The multitask studies we examined in full report classification accuracy and
regression error side by side, without deriving a screening decision from the predicted amount or comparing
it with the classification output.^22–24^

That test is where many spectroscopic studies are weakest. A paste is usually scanned many times, and
replicate scans of one sample are far more alike than scans of different samples. When replicate scans
are split at random between training and test sets, the model is tested on near-copies of its training
data, and the reported accuracy measures memory rather than generalisation; this form of data leakage
is a recognised cause of irreproducible results in spectroscopy and machine learning.^26,27^
Of the multitask studies above, one divided its samples, each measured repeatedly, between cross-validation
folds at random without stating that the repeated measurements were kept together,^20^ one divided all
spectra at random between training, validation and test sets,^23^ and one held out, for each mixture,
one of four replicate preparations made from the same raw materials.^24^ Only the first applied its
network to material from outside the training set: commercial blends of one nominal composition, for which it
reported the predicted olive-oil content, without testing whether authentic oil from new sources was accepted.^20^
How such networks decide on new authentic material is therefore largely unknown. On the present data the
difference is large: a scan-level random split, the default of most machine-learning tutorials, puts
54 of the 55 physical samples on both sides of the split (ESI). In our earlier study, with each
authentic lot serving as the blank while it was withheld, the detection limits were 8.9–21.6 % adulterant,
and authentic tahini from the lots least like the others was flagged as adulterated;^15^ on
other ATR–FTIR adulteration data, withholding whole brands degraded every model we tested.^28^



The present study uses the released tahini spectra^15^ to ask three questions under
validation that withholds whole physical samples and whole production lots. First, does a multitask
network with a classification head and a composition head screen tahini for sunflower or peanut paste,
identify the adulterant and estimate its amount as well as the chemometric pair of PLS-DA and PLS
regression? Second, should the screening decision come from the classification head or from the
predicted composition? Third, what in the spectra of an authentic lot makes a model reject it? Relative
to the earlier study, the data, the grouped hold-out partition, the three-fraction output, the
detection-limit convention and the use of a cut-off on the predicted tahini fraction are reused. New are
the classification head and its joint training with a softmax composition head, a cut-off set from
authentic training samples alone, the comparison of the two decision routes for both model families,
and the band-level account of why a withheld authentic lot is rejected.


## 2 Experimental

### 2.1 Samples and spectra

The spectra are the tahini set released with our earlier calibration study (ref. 15), where the
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


Every spectrum carries the three mass fractions (tahini, sunflower paste, peanut paste), which sum to
100 %, and a binary label (authentic or adulterated). The 100 % sunflower and 100 % peanut samples of lot
T5 are pure adulterant and are labelled adulterated.

### 2.2 Preprocessing and spectral regions

Each spectrum was corrected by the standard normal variate (SNV),^29^ computed over the full
600–4000 cm<sup>−1</sup> range; SNV acts on one spectrum at a time and therefore cannot leak information between
training and test sets. The models were then given the
two regions that carry the chemistry of the pastes, 2800–3050 cm<sup>−1</sup> (C–H stretching) and
600–1800 cm<sup>−1</sup> (carbonyl, amide and fingerprint bands), 752 channels in total. The atmospheric CO<sub>2</sub>
band (about 2250–2400 cm<sup>−1</sup>) and the water-vapour rotation lines above 3550 cm<sup>−1</sup> were excluded because
they record the state of the optical path, not the sample. The full 600–4000 cm<sup>−1</sup> range was run as a
sensitivity analysis (ESI, Table S7); SNV computed over the retained regions only, and a fingerprint
region starting at 700 cm<sup>−1</sup>, where the ZnSe element approaches its transmission limit, were run as further
sensitivity analyses (Section 3.4).


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


### 2.4 Chemometric reference models

The reference is the standard chemometric pair: partial least-squares discriminant analysis (PLS-DA)
on the one-hot class and PLS2 regression on the three fractions, without scaling of the SNV inputs
(scikit-learn 1.7.0). The number of latent variables (1–25) of each model was chosen inside every
training set by grouped five-fold cross-validation (minimum root-mean-square error of
cross-validation). PLS2 predictions were clipped at zero and rescaled to sum to 100 %.


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
for the class routes) and the mean was compared with the same threshold, or with zero. At scan level the
two classes were nearly balanced (754 authentic and 800 blend spectra), because each authentic lot was
scanned about ten times as often as each blend, so the 0.5 cut-off of the sigmoid head was kept; at
sample level a lot-out training set held 4 authentic and 40 blend samples.

### 2.6 Validation

The unit of splitting is the physical sample. Replicate scans of one sample are far more alike than
scans of different samples, so a split that separates them would test the model on near-copies of its
training data. Two designs were used. The first is the grouped 70/30 hold-out of ref. 15, which puts
38 samples (1146 spectra) in training and 17 samples (408 spectra) in the test set, so that the results
can be compared with the published benchmark. It contains a single authentic lot and no blend below
16 % adulterant. The second, and the main test of this paper, is leave-one-lot-out validation: each
production lot is withheld in turn with its ten blends (five folds), and all selection, scaling, early
stopping and threshold setting is repeated inside the remaining four lots. Because each lot carries its
own adulteration levels, every level from 4 to 100 % and every authentic lot is predicted exactly once by
a model that never saw that lot. To show how much a scan-level split inflates the apparent accuracy,
the same models were also run on a random 80/20 split of the scans (ESI).


### 2.7 Metrics and statistics

Screening was scored by sensitivity, specificity, balanced accuracy and the area under the receiver
operating characteristic curve (AUC), at scan level and, after averaging the scans of each sample, at
sample level. The adulterant was taken as identified when the larger predicted adulterant fraction
belonged to the true adulterant. Quantification was scored on the tahini fraction by the coefficient of
determination (R<sup>2</sup>), the root-mean-square error of prediction (RMSEP) and the mean absolute error. The
limit of detection followed the calibration-slope convention of ICH Q2(R2)^30^ used in ref. 15,
LOD = 3.3σ/S, where σ is the SD of the predicted adulterant fraction of withheld authentic scans and S the
slope of predicted on nominal adulterant fraction; the more rigorous multivariate LOD interval of
Allegrini and Olivieri^31^ was not used, for comparability with the earlier study. Because a
bounded output and a lot-wise bias both distort σ, the share of blend scans flagged at each nominal
level is also reported, the empirical alternative that the guideline allows. In leave-one-lot-out validation the predictions of the five
withheld lots are pooled, so σ includes the differences between authentic lots; within the hold-out test
set, which holds a single authentic lot, σ reflects replicate scatter only and the LOD is given for
comparison. All 95 % intervals are cluster-bootstrap percentiles (1000 draws) that
resample whole physical samples, never single scans;^32^ for the MT-DNN each draw averages the five seeds.
For lot-out specificity at sample level, which rests on five authentic samples, the exact Clopper–Pearson
interval is given instead.^33^ Blends of one lot share that lot's bias, so the sensitivity intervals,
which resample blends as independent samples, are too narrow for new lots.
With five lots the lot level is too coarse to resample, so lot-out results are also reported fold by
fold.

### 2.8 Exploratory analyses

Two analyses were added after the leave-one-lot-out results had been seen and are reported as
exploratory. For each authentic lot, the mean SNV spectrum of the lot minus the mean of the other four
lot means was divided by the within-lot SD (the mean of the five per-lot SDs), to locate the bands in which the lot departs from
the others; the same difference was computed on Savitzky–Golay second-derivative spectra (second-order
polynomial, windows of 9, 13 and 17 points) to separate shifted or additional bands from broad changes
in absorbance, and the unscaled difference was projected on the tahini coefficient vector of the PLS-R
model that had withheld that lot, to estimate how far the departure alone moves the PLS prediction. A
sample-level agreement rule, which flags a sample only when both regression routes (PLS-R and MT-DNN-R)
flag it, was also evaluated. At a later internal review stage we added an exact McNemar test of the
two decision routes within each model family on the 55 withheld samples, results by nominal level and
without the two pure-adulterant samples (ESI, Table S8), and a one-class baseline: principal-component
analysis of the mean-centred authentic training scans (components chosen to explain 99 % of the
variance, at most 15), flagging a scan when Hotelling's T² or the residual Q exceeded its limit, set at
mean + 3 SD of the out-of-fold values obtained by leaving out one training lot at a time (ESI, Table S9).
At the same stage the regression threshold was recomputed from the same cross-validated authentic training
predictions with four alternative rules (99th and 99.9th percentiles, mean + 3 SD of the sample means, and mean +
3 SD on the logit scale) and the lot-out decisions were scored again (ESI, Table S10).
Code, predictions and the analysis plan with its amendments are in the
repository (Data availability).


## 3 Results and discussion

### 3.1 What separates the three pastes in the mid-infrared

The mean spectra of the three pastes are dominated by the same lipid bands (Fig. 1a): the olefinic
=C–H stretch near 3008 cm<sup>−1</sup>, the CH<sub>2</sub> stretches at 2922 and 2853 cm<sup>−1</sup>, the ester carbonyl near
1745 cm<sup>−1</sup>, the CH<sub>2</sub> scissoring near 1463 cm<sup>−1</sup>, the ester C–O stretches around 1160 cm<sup>−1</sup> and the CH<sub>2</sub>
rocking band near 721 cm<sup>−1</sup>.^7^ The protein of the seeds adds the amide I and amide II bands
near 1650 and 1540 cm<sup>−1</sup>.^8^ Adulteration therefore changes the relative intensity of bands
that all three pastes share. After SNV, pure sunflower paste differs from authentic tahini mainly by
weaker CH<sub>2</sub> stretching (−0.29 and −0.22 SNV units at 2920 and 2851 cm<sup>−1</sup>) and stronger absorption at
989 and 1051 cm<sup>−1</sup> (+0.25 and +0.20), the region of C–O stretching in carbohydrates,^34^
and below 700 cm<sup>−1</sup>. Pure peanut paste differs in the opposite direction: stronger CH<sub>2</sub> stretching
(+0.64 and +0.50 at 2920 and 2853 cm<sup>−1</sup>) and ester carbonyl (+0.21 at 1749 cm<sup>−1</sup>), and weaker amide I
(−0.29 at 1655 cm<sup>−1</sup>) and carbohydrate C–O bands (−0.21 to −0.28 between 1041 and 1132 cm<sup>−1</sup>). Relative
to tahini, then, the sunflower paste carries less lipid signal and the peanut paste more, which is
why the two adulterants pull the spectrum in different directions and can be told apart.


Most of the information that distinguishes one physical sample from another lies in the two regions
given to the models. The median ratio of between-sample to within-sample variance was 5.0 over
600–1800 cm<sup>−1</sup> and 7.4 over 2800–3050 cm<sup>−1</sup>, against 2.6 in the CO<sub>2</sub> band and 2.6 in the water-vapour
region (Fig. 1b). Within-sample variance is not small anywhere: replicate scans of one sample,
repositioned on the crystal, differ appreciably, and this is the variation that a scan-level split
lets the model see on both sides.


### 3.2 A scan-level split hides the problem

Table 2 shows the same models under the three validation designs. A random 80/20 split of the scans
put replicate scans of 54 of the 55 physical samples on both sides, although component selection, early
stopping and the decision thresholds were still chosen by grouped cross-validation inside the training
scans, so only the outer split leaked. On that split the composition was predicted with an RMSEP of
1.79 % tahini by PLS and 2.75 % by the MT-DNN, and every route except PLS-DA accepted every
authentic scan. Withholding whole lots raised the RMSEP to 4.87 and 3.95 % and lowered the specificity of
the same routes to about 80 %, with scan-level bootstrap intervals reaching down to 33–35 %. The random split therefore
makes the quantification error look 1.4–2.7 times smaller and hides the false positives completely, because
every authentic lot is represented in training and the test scans of a lot are near-copies of its
training scans. The grouped hold-out of the earlier study removes the replicate leakage but, with a
single authentic lot in its test set, still cannot reveal the lot effect. The preliminary analysis that
motivated this work used a random split of the scans and reported an AUC of 0.9998; none of the figures from such a split describes how the screen would perform on a new
production lot.


### 3.3 Benchmark: the grouped hold-out

On the grouped hold-out of the earlier study, every route accepted all scans of the authentic test
sample, and every route except PLS-DA flagged every blend scan (Table 1). PLS-DA missed 25 blend scans, with two blend samples
(76 % tahini with sunflower and 84 % tahini with peanut paste) falling on the authentic side.
Quantification was consistent with the published benchmark: PLS gave R<sup>2</sup> 0.997 and RMSEP 1.93 % tahini and the
MT-DNN composition head 0.986 and 3.95 %, against 0.994 for PLS and 0.988 for a regression-only multilayer perceptron in
ref. 15. This partition is the easy case. Its test set holds one authentic lot and no
blend below 16 % adulterant, so the perfect specificity rests on a single authentic sample. It also
gives a misleading detection limit: the softmax output of the MT-DNN saturates at 0 % adulterant for
the authentic test scans (σ = 0.01 percentage points), which gives an LOD of 0.03 %, whereas PLS, whose
output is not bounded, gave 2.7 %. Neither figure measures what happens with a new lot.


### 3.4 Screening production lots never seen in training

Withholding each production lot in turn changed the picture in one respect only (Fig. 3, Table 1).
Blends were still detected: at sample level the MT-DNN routes flagged all 50 withheld blends, PLS-R
missed one (4 % peanut paste in lot T1) and PLS-DA missed six. PLS-DA was the weakest route throughout.
It missed all scans of the 12 % blends, almost all of those at 16 % and about a third of those at
32 and 36 % (Fig. 3b), and the number
of latent variables chosen for it ranged from 2 to 22 across folds, a sign that the discriminant
direction was poorly determined by four lots.

Authentic tahini from a new lot was the problem. Every route rejected at least one of the five withheld
authentic lots (Fig. 3a), so the sample-level specificity was 60 % for PLS-DA and 80 % for the other
three routes, with exact 95 % intervals reaching down to 15 and 28 % (Table 1). The failures were concentrated in one
lot per model family. The two MT-DNN routes flagged lot T1 (98 % of its scans by the class head and 100 %
by the composition cut-off), PLS-R flagged lot T5 (100 %), and PLS-DA flagged T1 entirely and half of
T2. The remaining lots were accepted almost completely by every route. This pattern, in which the
false positives come from whole lots rather than from scattered scans, was also seen for the six
single-task models of the earlier study, where PLS and the multilayer perceptron flagged T1 and T5 and
other models flagged other lots.^15^ It means that the specificity of any of these screens is
set by how far a new authentic lot lies from the calibration lots, not by the scan-to-scan noise that a
hold-out estimate measures.
With the full 600–4000 cm<sup>−1</sup> range as input the same lots were rejected at sample level (T1 by both
MT-DNN routes and PLS-DA, T5 by PLS-R) and every route reached 80 % sample-level specificity, so the lot
effect does not depend on the choice of spectral regions. The scan-level picture did change: PLS-R also
flagged 29 % of the T1 scans, PLS-DA no longer flagged T2 (3 % of its scans), and the lot-out RMSEP rose
to 5.32 % for PLS and 5.73 % for the MT-DNN, with the MT-DNN error on T1 reaching 9.76 % (ESI, Table S7). The region choice therefore matters more for
the network's quantification of a departing lot than the pooled error suggests. Two further changes to the
input left the rejected lots unchanged (ESI, Table S12): computing SNV over the retained regions only, which
removes any influence of the CO<sub>2</sub> and water-vapour regions on the normalisation, and starting the
fingerprint region at 700 cm<sup>−1</sup>, near the low-wavenumber limit of the ZnSe element. In both, the MT-DNN
routes rejected T1 and PLS-R rejected T5, sample-level specificity stayed at 80 % for these three routes,
the sample-level sensitivity of PLS-R fell from 98 to 94 and 96 %, and the lot-out RMSEP was 3.62–4.06 % for
the MT-DNN and 4.92–5.18 % for PLS. PLS-DA changed most: its rejection of half of the T2 scans disappeared
(7 % of scans) when the region below 700 cm<sup>−1</sup> was removed, as it did with the full range, which raised its
sample-level specificity from 60 to 80 %.




The pooled lot-out detection limit was 11.1 % adulterant for PLS (σ = 3.2 percentage points), within
the 10.3–19.5 % reported for the leading models under nested lot-out validation in ref. 15 but
below the 19.5 % of its PLS model, which used all 1762 channels and a different model selection, so the
two values are not directly comparable. Most of this σ is the offset of one lot: authentic T5 averaged
10.3 % predicted adulterant against 2.3–4.0 % for the other lots, and with T5 left out of the blank the
PLS detection limit fell to 5.2 % (ESI, Table S8).
The MT-DNN gave 4.1 % (σ = 1.2), but this figure should not be read as an almost threefold gain in sensitivity.
Its σ is small because the softmax output cannot fall below 0 % adulterant, so authentic lots that the
network recognises contribute almost no spread, and the one lot it does not recognise (T1) sits above
its threshold. The calibration-slope LOD assumes an unbounded, roughly normal blank response, and a
saturating output violates that assumption.

The share of blend scans flagged at each nominal level (Fig. 3b) avoids that assumption but cannot
replace it here, because each level occurs in one lot only. The MT-DNN routes flagged at least 98.7 % of
the scans at every level from 4 % upwards, but the 4 % blends belong to lot T1, which the network flags
whatever its composition, so detection at the lowest levels cannot be separated from the lot effect.
PLS-R flagged every level from 20 % upwards in at least 95 % of the scans and missed half of the 4 % scans
and 16 % of the 16 % scans. Excluding the two pure-adulterant samples, which anchor the calibration,
changed neither the sample-level sensitivity (97.9 % for PLS-R, 100 % for both MT-DNN routes, over 48
blends) nor the calibration slopes by more than 0.01 (ESI, Table S8).


### 3.5 Why a withheld authentic lot is rejected

The rejected lots are those whose spectra depart from the other four in the directions that each model
reads as adulteration (Fig. 5). Lot T1 departs most: the root-mean-square departure of its mean SNV
spectrum from the other lots is 1.61 pooled within-lot SDs, against 1.11–1.36 for the others, and the
departure is concentrated between 1180 and 1280 cm<sup>−1</sup>, where T1 absorbs 4.90 to 8.35 SDs less than the other lots
at 1215, 1248 and 1273 cm<sup>−1</sup> (Fig. 5b). Lots T4 and T5 depart the other way in the same window (+5.40 SDs at
1246 cm<sup>−1</sup> and +4.10 SDs at 1213 cm<sup>−1</sup>), so this region varies between lots in general, and T1 lies at
one end of that variation. This region holds the C–O stretching of the triglyceride ester
groups, tabulated near 1238 cm<sup>−1</sup>,^7^ and the weak amide III band of the proteins.^8^
Second-derivative spectra (Savitzky–Golay, 13 points or 23 cm<sup>−1</sup>; ESI, Fig. S3) resolve the same three
bands in this region, near 1162, 1239 and 1278 cm<sup>−1</sup>, at the same positions in all five lots (within 0.3
cm<sup>−1</sup>, a sixth of a data channel), and no separate component near 1215 or 1248 cm<sup>−1</sup> in any lot. At
1215, 1248 and 1273 cm<sup>−1</sup> the standardised departure of T1 falls to 1.3, 0.6 and 1.8 SDs in the second
derivative, and to no more than 2.1 SDs anywhere in the region with windows of 9 to 17 points. The T1
departure is therefore a broad difference in absorbance, not a shifted or additional band, and it
cannot be assigned to one functional group; T1 remains the most atypical lot in the second derivative
as well (root-mean-square departure over 600–1800 cm<sup>−1</sup> 1.10 SDs, against 0.65–0.86). The MT-DNN, which flagged
T1, predicted 2.9 % adulterant for its authentic scans on average, against a threshold of 0.4–0.8 %
set on the four training lots, for which the softmax output was close to zero (Fig. 5a). The threshold is
low because the composition head saturates: authentic training scans give a predicted adulterant
fraction near 0 % with little spread, so the mean + 3 SD rule places the cut-off within a percentage point of
zero, and a modest shift of a new lot is enough to cross it. In the other four folds, where the
training set included T1, the thresholds were 1.8–5.2 %. The rejection of T1 does not depend on this rule:
with the cut-off set at the 99th or 99.9th percentile of the cross-validated authentic training predictions, at
mean + 3 SD of their sample means or at mean + 3 SD on the logit scale, the threshold of the T1 fold stayed between
0.3 and 2.0 %, and T1 was rejected, and no other lot, with all five seeds under every rule (ESI, Table S10). The
PLS-R rejection of T5 was equally stable, except under the logit rule, which is not meaningful for the clipped PLS
output and lowered its sensitivity to 30 %.
The same
lot also carried the largest quantification error of the network: the tahini fraction of the T1 blends
was underestimated by 5.3 percentage points on average, against biases of −0.7 to +3.2 for the other lots.

Lot T5 is not the most atypical lot overall, but its departure lies along the PLS regression vector.
Projected on the PLS tahini and adulterant coefficients of the model that withheld it, the T5 departure
alone moves the prediction by 8.9 percentage points towards adulteration, against 3.0 for T1 and less
than 2 for T2 and T3, and the observed mean prediction for authentic T5 was 10.3 % adulterant, above the
6.1 % threshold of that fold. For lot T4 the projection points the other way and is larger (12.6 points towards a tahini fraction
above 100 %), which the clipping of the PLS output turns into a small positive bias. The PLS vector is
thus sensitive to lot differences in both directions; clipping hides one of them, and only a departure
towards adulteration produces a false positive. Lot T2
departs by +4.05 SDs at 1709 cm<sup>−1</sup>, more than any other lot there, where free fatty acids absorb,^35^
and its largest departure is at 717 cm<sup>−1</sup> (+4.25 SDs), in the CH<sub>2</sub> rocking region whose shape follows the
physical state of the fat. Neither departure corresponds to a resolved band: in the second derivative no
lot, and none of the 754 authentic scans, shows a minimum between 1700 and 1718 cm<sup>−1</sup>, where the
signal is the flank of the ester carbonyl band at 1744 cm<sup>−1</sup>; the CH<sub>2</sub> rocking minimum lies at 722.5 cm<sup>−1</sup>
in every lot; and the departures of T2 at 1709 and 717 cm<sup>−1</sup> fall to −0.9 and +0.4 SDs (ESI, Fig. S3). The
T2 departure is thus also a broad change in band shape or baseline, which could have a physical cause
(temperature, crystallinity, contact with the crystal) as well as a chemical one; acquisition
temperature was not recorded. It did not cause false positives for the regression routes but may explain
why PLS-DA rejected half of its scans. These observations describe how the lots differ, not why: no
further chemical analysis of the lots (free fatty acids, oil, protein or moisture content) was
possible, and finding the cause requires reference measurements on new lots. Part of the differences may also
arise in the measurement rather than in the tahini. The data carry no acquisition dates, but two bands
that the sample does not produce, the atmospheric CO<sub>2</sub> band and the water-vapour lines, record the
state of the optical path, and both differed between the authentic lots (ESI, Table S11): they were low
for T1 and T2 and high for T3–T5, with no overlap of the lot means, and T1 lay 2.0 and 2.8 within-lot SDs
below the other lots. The authentic lots were therefore not all measured under the same conditions, and in
this set the effect of a lot cannot be separated from that of its measurement session. This applies most
to T1; T5, the lot rejected by PLS, shares its optical-path state with the accepted lots T3 and T4.


The two model families therefore fail for different reasons. PLS is a linear projection, and a lot is
rejected when its spectral difference happens to align with the regression vector, whatever the size of
that difference. The MT-DNN is non-linear and its softmax output is confident wherever the training data
are dense, so a lot is rejected when it is far from all four training lots in any direction, as T1 is.



### 3.6 Quantification and identification of the adulterant

Both composition outputs transferred to new lots far better than the decisions built on them (Fig. 4).
Over the five withheld lots, PLS gave a scan-level R<sup>2</sup> of 0.979 and RMSEP of 4.87 % tahini and the
MT-DNN 0.986 and 3.95 %, with overlapping intervals (Table 1); at sample level, where averaging removes
replicate scatter but not lot bias, the order reversed (PLS 3.80 %, MT-DNN 4.55 %). The errors of each
model were concentrated in the lot it also misjudged at the screening step: the lot-wise RMSEP was
largest for T5 with PLS (7.97 %) and for T1 with the MT-DNN (5.46 %), and 2.4–4.4 % for every other lot
and model. The adulterant was identified correctly in 97 % of blend scans by both families, with the
lowest lot-wise value 93 % (lot T4) for PLS and 95 % (lot T2) for the MT-DNN. Lot-out quantification is thus about two and a half times as
uncertain as the hold-out suggested for PLS (RMSEP 4.87 against 1.93 %) and about as uncertain for the
MT-DNN (3.95 % in both designs); the network loses less when moving to a new lot but starts from a worse
hold-out calibration.


### 3.7 One network or two models?

The classification head showed no detectable advantage over the network's own composition output. On
withheld lots the class head and the composition cut-off of the MT-DNN reached the same decision for
all 55 samples in every seed, rejected the same lot and detected blends equally well (scan-level
sensitivity 100 % for both; Table 1). In the PLS family the regression route was right where PLS-DA was
wrong for eight samples and the reverse held for two (exact McNemar test, p = 0.11). With five
authentic samples no difference in specificity could reach significance: even if one route were right
on all five and the other wrong on all five, the exact two-sided McNemar p would be 2 × 0.5<sup>5</sup> = 0.0625.
The result is therefore absence of evidence for a gain, not evidence of equivalence. What the data do
show is that, for the MT-DNN, the class head was redundant with the composition output, and the
recommendation that follows rests on parsimony. A dedicated classifier adds a second decision to calibrate and, in the PLS family, a less
stable one; thresholding the predicted composition gives the decision, the identity of the adulterant
and its amount from one output, and has a threshold that can be read in composition units. The value
of the multitask network lies elsewhere: it is a second, non-linear view of the same spectra whose
errors fall on different lots from those of PLS.

That complementarity suggests a simple rule, which we tested only after seeing the results: flag a
sample only when both regression routes flag it. Once the two families reject different lots, an AND
rule accepts every authentic lot by construction, so its specificity here is a consequence of how the
rule was chosen, not evidence for it; its cost in sensitivity is the informative part. Applied to the lot-out predictions, the rule accepted
all five withheld authentic lots and still flagged 49 of the 50 blends, for each of the five network
seeds; the one blend missed was the 4 % peanut paste blend of lot T1, which PLS-R alone also missed.
With the two input variants of Table S12 the rule again accepted all five authentic lots and flagged 47
and 48 of the 50 blends, missing the 4 % blends of T1 and, with SNV over the retained regions, the 16 %
sunflower blend of T4.

With five authentic lots this is a hypothesis, not a validated screening rule, and it will fail for a
lot that departs along the PLS vector and from the network's training data at the same time. It
suggests that combining a linear and a non-linear calibration may protect specificity where an additional
classification head did not, at the cost of maintaining two models, and it should be tested on lots not used here.

A one-class model answers the screening question without seeing either adulterant and might avoid the
lot problem. As a simple baseline, a principal-component model fitted on the
authentic training scans alone (15 components, the cap, which the 99 % variance rule reached in every
fold; T² and Q limits set, like the regression thresholds, at
mean + 3 SD of out-of-fold values) accepted all five withheld authentic lots at sample level, but only
narrowly for T1, whose mean T² reached 0.97 of its limit and of whose scans 43 % exceeded a limit, and it missed 9 of the 50 blends, all at or below
32 % adulterant (ESI, Table S9). The limits rest on four training lots and moved considerably with the
number of components and the limit rule. Without adulterant examples the screen trades the false
positives of the supervised routes for missed low-level blends, which is the same lot effect seen from
the other side.




Table 1 Screening, quantification and identification on withheld samples (chemically informative regions). Values are point estimates with cluster-bootstrap 95 % intervals (1000 draws over physical samples); MT-DNN values are means of the five per-seed values (the figures instead average the predictions of the five seeds per scan). Quantification and identification are properties of the composition output and are shown once per model family. Hold-out: grouped hold-out; lot-out: leave-one-lot-out; ID: identification of the adulterant. ‡ No interval: the hold-out test set contains a single authentic lot. † In leave-one-lot-out validation five authentic samples, one per lot, are withheld; exact (Clopper–Pearson) 95 % interval for the proportion of the five authentic lots accepted; scan-level specificity intervals resample the same five authentic samples and are indicative only. Sensitivity intervals resample blends as independent samples and do not account for the shared bias of the blends of one lot, so they are too narrow for new lots.

| Validation | Level | Route | Sensitivity (%) | Specificity (%) | AUC | RMSEP (%) | R² | ID (%) |
|---|---|---|---|---|---|---|---|---|
| Hold-out | sample | PLS-DA | 87.5 (68.8–100.0) | 100.0‡ | 1.000 (1.000–1.000) |  |  |  |
| Hold-out | sample | PLS-R | 100.0 (100.0–100.0) | 100.0‡ | 1.000 (1.000–1.000) | 1.42 (1.09–1.70) | 0.997 (0.994–0.999) | 100.0 (100.0–100.0) |
| Hold-out | sample | MT-DNN | 100.0 (100.0–100.0) | 100.0‡ | 1.000 (1.000–1.000) | 3.79 (2.89–4.55) | 0.980 (0.958–0.990) | 100.0 (100.0–100.0) |
| Hold-out | sample | MT-DNN-R | 100.0 (100.0–100.0) | 100.0‡ | 1.000 (1.000–1.000) |  |  |  |
| Hold-out | scan | PLS-DA | 90.3 (74.2–100.0) | 100.0‡ | 0.999 (0.997–1.000) |  |  |  |
| Hold-out | scan | PLS-R | 100.0 (100.0–100.0) | 100.0‡ | 1.000 (1.000–1.000) | 1.93 (1.69–2.30) | 0.997 (0.987–0.997) | 100.0 (100.0–100.0) |
| Hold-out | scan | MT-DNN | 100.0 (100.0–100.0) | 100.0‡ | 1.000 (1.000–1.000) | 3.95 (2.58–5.53) | 0.986 (0.934–0.993) | 100.0 (100.0–100.0) |
| Hold-out | scan | MT-DNN-R | 100.0 (100.0–100.0) | 100.0‡ | 1.000 (1.000–1.000) |  |  |  |
| Lot-out | sample | PLS-DA | 88.0 (77.8–96.1) | 60.0 (14.7–94.7)† | 0.888 (0.690–1.000) |  |  |  |
| Lot-out | sample | PLS-R | 98.0 (93.8–100.0) | 80.0 (28.4–99.5)† | 0.988 (0.951–1.000) | 3.80 (2.98–4.62) | 0.985 (0.976–0.991) | 96.0 (90.4–100.0) |
| Lot-out | sample | MT-DNN | 100.0 (100.0–100.0) | 80.0 (28.4–99.5)† | 0.998 (0.992–1.000) | 4.55 (3.80–5.28) | 0.979 (0.968–0.986) | 97.2 (94.3–100.0) |
| Lot-out | sample | MT-DNN-R | 100.0 (100.0–100.0) | 80.0 (28.4–99.5)† | 1.000 (1.000–1.000) |  |  |  |
| Lot-out | scan | PLS-DA | 88.5 (79.5–95.9) | 69.6 (27.1–100.0) | 0.871 (0.655–0.997) |  |  |  |
| Lot-out | scan | PLS-R | 97.4 (94.4–100.0) | 79.7 (33.0–100.0) | 0.986 (0.950–1.000) | 4.87 (3.37–6.58) | 0.979 (0.953–0.990) | 97.2 (93.5–100.0) |
| Lot-out | scan | MT-DNN | 100.0 (99.8–100.0) | 79.9 (34.8–100.0) | 0.996 (0.986–1.000) | 3.95 (3.17–4.99) | 0.986 (0.976–0.990) | 97.2 (94.4–99.9) |
| Lot-out | scan | MT-DNN-R | 100.0 (99.9–100.0) | 80.1 (33.5–100.0) | 1.000 (0.999–1.000) |  |  |  |




Table 2 The same models under three validation designs (scan level, chemically informative regions; cluster-bootstrap 95 % intervals over physical samples; MT-DNN means over five seeds). RMSEP is for the tahini fraction. Lot-out specificity intervals resample the five authentic samples and are indicative only (exact sample-level intervals: Table 1).

| Validation | RMSEP PLS (%) | RMSEP MT-DNN (%) | Specificity PLS-R (%) | Specificity MT-DNN-R (%) | Specificity MT-DNN class head (%) |
|---|---|---|---|---|---|
| Random 80/20 split of scans (54 of 55 samples on both sides) | 1.79 (1.59–2.00) | 2.75 (2.16–3.54) | 100.0 (100.0–100.0) | 100.0 (100.0–100.0) | 100.0 (100.0–100.0) |
| Grouped hold-out (17 test samples, 1 authentic lot) | 1.93 (1.69–2.30) | 3.95 (2.58–5.53) | 100.0 (one authentic sample) | 100.0 (one authentic sample) | 100.0 (one authentic sample) |
| Leave-one-lot-out (5 folds, all 55 samples) | 4.87 (3.37–6.58) | 3.95 (3.17–4.99) | 79.7 (33.0–100.0) | 80.1 (33.5–100.0) | 79.9 (34.8–100.0) |




## Figures

![Fig. 1 (a) Mean ATR–FTIR spectra of authentic tahini (754 scans of five lots), pure sunflower paste (17 scans) and pure peanut paste (16 scans), with the main band assignments; the shaded ranges (600–1800 and 2800–3050 cm<sup>−1</sup>) are the regions given to the models. (b) Ratio of between-sample to within-sample variance of the SNV spectra at each wavenumber (log scale), computed over the 55 physical samples; higher values mean that the channel separates samples more than it varies between replicate scans of one sample.](figures/fig1_spectra.png)

![Fig. 2 Workflow. Spectra are split by physical sample (grouped hold-out) or by production lot (leave-one-lot-out); SNV and region selection act on each spectrum. Two model families (PLS-DA with PLS2 regression; the multitask network with a classification head and a softmax composition head) give two decision routes each: the classification output, or a cut-off on the predicted adulterant fraction set from authentic training samples.](figures/fig2_workflow.png)

![Fig. 3 Screening on withheld production lots (leave-one-lot-out). (a) Percentage of the scans of each withheld authentic lot flagged as adulterated (false positives) by each decision route; MT-DNN routes are means over five seeds. (b) Percentage of blend scans flagged at each nominal adulterant level, pooled over the five withheld lots; the legend gives the pooled scan-level sensitivity with its cluster-bootstrap 95 % interval.](figures/fig3_detection_lolo.png)

![Fig. 4 Quantification on withheld production lots (leave-one-lot-out). Predicted against nominal tahini fraction for (a) PLS regression and (b) the composition head of the MT-DNN (mean of five seeds). Points are physical-sample means of the scan predictions and bars ±1 SD over the scans; R<sup>2</sup> and RMSEP are at scan level (Table 1).](figures/fig4_quantification_lolo.png)

![Fig. 5 Why a withheld authentic lot is rejected. (a) Predicted adulterant fraction (100 % minus predicted tahini) of the scans of each withheld authentic lot for PLS regression (squares) and the MT-DNN composition head (circles, mean of five seeds per scan), with the decision threshold of that fold (line, PLS-R; band, range over the five MT-DNN-R seeds). (b) Exploratory: departure of each authentic lot's mean SNV spectrum from the mean of the other four lots, in units of the pooled within-lot SD; grey bands mark 1180–1280 cm<sup>−1</sup> (ester C–O and amide III) and 1700–1720 cm<sup>−1</sup> (free fatty acid C=O).](figures/fig5_lots.png)


## 4 Conclusions

A multitask network with a classification head and a softmax composition head screened tahini for
sunflower and peanut paste, identified the adulterant and estimated its amount from one ATR–FTIR
spectrum about as well as the chemometric pair of PLS-DA and PLS regression, when whole production
lots were withheld. Three conclusions follow for infrared screening of pastes.

First, on grounds of parsimony the decision is best taken from the predicted composition. The
classification head added a second output to calibrate with no detectable gain in sensitivity or
specificity (with five lots, small differences could not be detected), and PLS-DA was the least
stable route of all. A cut-off on the predicted tahini fraction, set from authentic training samples
alone, gives the decision in composition units together with the amount and identity of the
adulterant.

Second, specificity on new lots, not sensitivity, limits the method. Blends were detected almost
completely on unseen lots, but every route rejected at least one of five authentic lots. The rejected
lot depended on the model: the network rejected the lot that departed most from the others, a broad
absorbance difference near 1180–1280 cm<sup>−1</sup> rather than a shifted band, and PLS rejected the lot whose departure happened to
lie along its regression vector. Whether these departures arise in the tahini or in the measurement
session cannot be decided from these data, because the authentic lots were not all measured under the
same optical-path conditions. Hold-out estimates with a single authentic lot, and scan-level random
splits even more so, hide this behaviour completely.

Third, because the two families fail on different lots, combining them may protect specificity, at
the cost of maintaining two models. In this set, requiring both composition routes to agree removed every false
positive at the cost of one 4 % blend; the first part follows by construction once the two families
reject different lots, so only the cost is informative. This rule was found after the results were known and rests on
five authentic lots; it needs testing on new lots, each measured in several sessions in interleaved order, other suppliers and a
second instrument before it
can support routine screening. For any such use, the authentic reference set must cover the variation
between lots that the screen will meet,^36^ and a positive result should be confirmed by a targeted method.


## Author contributions


A. Yılmaz: conceptualization, methodology, investigation, data curation, writing – review and editing.
A. Batayhi: conceptualization, methodology, software, validation, formal analysis, visualization,
writing – original draft. M. Özgölet: conceptualization, methodology, supervision, writing – review and
editing. M. Arici: conceptualization, methodology, supervision, writing – review and editing.

## Conflicts of interest

There are no conflicts to declare.

## Data availability

The ATR–FTIR spectra analysed in this study were released with ref. 15 and are available
on Zenodo (version 2.2.0, https://doi.org/10.5281/zenodo.23168994; all versions: https://doi.org/10.5281/zenodo.21446757).^37^ The code for this study (data
loading, models, validation, statistics and figures), the analysis plan with its dated amendments,
and all predictions and result files from which the reported numbers are computed are available at
https://github.com/abdulhamidbatayhi123/tahini-rsc-multitask (release v1.1.0 archived on Zenodo, https://doi.org/10.5281/zenodo.24120431). Analyses used Python with scikit-learn 1.7.0^38^ and
PyTorch 2.7.1.

## Acknowledgements


This research received no external funding. During the preparation of this work the authors used Claude (Anthropic) as a tool to assist with
code, literature searching and language editing. The authors designed the study, made every
scientific decision, checked all output, and take full responsibility for the content of the article.


## References

1. Food Standards Agency, John & Pascalis recalls Four Seasons Sesame Tahini because of undeclared peanuts, Allergy Alert FSA-AA-76-2018, https://www.food.gov.uk/news-alerts/alert/fsa-aa-76-2018 (archived copy: http://web.archive.org/web/20220708013426/https://www.food.gov.uk/news-alerts/alert/fsa-aa-76-2018), (accessed November 2026).
2. D. Peng, Y. Bi, X. Ren, G. Yang, S. Sun and X. Wang, *Food Chem.*, 2015, **188**, 415–421, DOI: 10.1016/j.foodchem.2015.05.001.
3. O. Stephan and S. Vieths, *J. Agric. Food Chem.*, 2004, **52**, 3754–3760, DOI: 10.1021/jf035178u.
4. M. Torricelli, E. Pierboni, C. Rondini, S. Altissimi and N. Haouet, *Foods*, 2020, **9**, 1085, DOI: 10.3390/foods9081085.
5. L. S. New, J. Stahl-Zeng, A. Schreiber, M. Cafazzo, A. Liu, S. Brunelle and H.-F. Liu, *J. AOAC Int.*, 2020, **103**, 570–583, DOI: 10.5740/jaoacint.19-0112.
6. C. Schmitt, T. Bastek, A. Stelzer, T. Schneider, M. Fischer and T. Hackl, *J. Agric. Food Chem.*, 2020, **68**, 14364–14373, DOI: 10.1021/acs.jafc.0c01999.
7. M. D. Guillén and N. Cabo, *J. Sci. Food Agric.*, 1997, **75**, 1–11, DOI: 10.1002/(sici)1097-0010(199709)75:1<1::aid-jsfa842>3.0.co;2-r.
8. A. Barth, *Biochim. Biophys. Acta, Bioenerg.*, 2007, **1767**, 1073–1101, DOI: 10.1016/j.bbabio.2007.06.004.
9. A. Rohman and Y. C. Man, *Food Res. Int.*, 2010, **43**, 886–892, DOI: 10.1016/j.foodres.2009.12.006.
10. G. Ozulku, R. M. Yildirim, O. S. Toker, S. Karasu and M. Z. Durak, *Food Control*, 2017, **82**, 212–216, DOI: 10.1016/j.foodcont.2017.06.034.
11. B. Ozen, C. Cavdaroglu and F. Tokatli, *Anal. Methods*, 2024, **16**, 4216–4233, DOI: 10.1039/d4ay00562g.
12. V. Mureșan, S. Danthine, A. E. Mureșan, E. Racolța, C. Blecker, S. Muste, C. Socaciu and V. Baeten, *Talanta*, 2016, **155**, 336–346, DOI: 10.1016/j.talanta.2016.04.019.
13. N. Kucukcelebioglu, Y. B. Karakas, C. Cavdaroglu and B. Ozen, *Food Anal. Methods*, 2026, **19**, 358, DOI: 10.1007/s12161-026-03268-5.
14. H. T. Temiz, U. Tamer, A. Berkkan and I. H. Boyaci, *Talanta*, 2017, **167**, 557–562, DOI: 10.1016/j.talanta.2017.02.044.
15. A. Batayhi, M. Özgölet, H. Cankurt and M. Arici, *Foods*, 2026, **15**, 3639, DOI: 10.3390/foods15203639.
16. S. Wold, M. Sjöström and L. Eriksson, *Chemom. Intell. Lab. Syst.*, 2001, **58**, 109–130, DOI: 10.1016/s0169-7439(01)00155-1.
17. R. G. Brereton and G. R. Lloyd, *J. Chemom.*, 2014, **28**, 213–225, DOI: 10.1002/cem.2609.
18. R. Caruana, *Mach. Learn.*, 1997, **28**, 41–75, DOI: 10.1023/a:1007379606734.
19. S. Liang, G. Chen, C. Ma, J. Gu, C. Zhu, L. Li, H. Gao, Z. Yang, J. Cao and Z. Chen, *Food Anal. Methods*, 2025, **18**, 385–397, DOI: 10.1007/s12161-024-02728-0.
20. X. Qin, Y. Chen, B. Li, S. Zeng, G. Mei and C. Yu, *Foods*, 2026, **15**, 2030, DOI: 10.3390/foods15112030.
21. J. Zeng, Z. Wu, E. Zhang, Z. Liu, T. Zhang and L. Li, *J. AOAC Int.*, 2026, **109**, 924–936, DOI: 10.1093/jaoacint/qsag068.
22. Y. Fan, Y. Gao, J. Cao, K. Wei, L. Qin, R. Li, Y. Zhang, J. Li, C. Wang, Q. Zhao, Q. Shen and Y. Xue, *Food Chem.*, 2026, **529**, 151087, DOI: 10.1016/j.foodchem.2026.151087.
23. Q. Shao, Y. Li, H. Chai, D. Zhang, Y. Ye, H. Ma and L. Guo, *Food Res. Int.*, 2026, **225**, 118066, DOI: 10.1016/j.foodres.2025.118066.
24. H. Ding, K. Chen, T. Wang, Y. Zhang, Y. Dai and Z. Liu, *Talanta*, 2027, **311**, 130285, DOI: 10.1016/j.talanta.2026.130285.
25. H. Ning, M. Ma, Z. Shi and L. Ding, *Anal. Chim. Acta*, 2026, **1391**, 345050, DOI: 10.1016/j.aca.2025.345050.
26. S. Guo, T. Bocklitz, U. Neugebauer and J. Popp, *Anal. Methods*, 2017, **9**, 4410–4417, DOI: 10.1039/c7ay01363a.
27. S. Kapoor and A. Narayanan, *Patterns*, 2023, **4**, 100804, DOI: 10.1016/j.patter.2023.100804.
28. A. Batayhi, M. Özgölet and O. Sagdic, *Foods*, 2026, **15**, 2949, DOI: 10.3390/foods15172949.
29. R. J. Barnes, M. S. Dhanoa and S. J. Lister, *Appl. Spectrosc.*, 1989, **43**, 772–777, DOI: 10.1366/0003702894202201.
30. International Council for Harmonisation, ICH Harmonised Guideline Q2(R2): Validation of Analytical Procedures, adopted 1 November 2023, https://database.ich.org/sites/default/files/ICH_Q2%28R2%29_Guideline_2023_1130.pdf, (accessed November 2026).
31. F. Allegrini and A. C. Olivieri, *Anal. Chem.*, 2014, **86**, 7858–7866, DOI: 10.1021/ac501786u.
32. C. A. Field and A. H. Welsh, *J. R. Stat. Soc. Ser. B Stat. Methodol.*, 2007, **69**, 369–390, DOI: 10.1111/j.1467-9868.2007.00593.x.
33. C. J. Clopper and E. S. Pearson, *Biometrika*, 1934, **26**, 404–413, DOI: 10.1093/biomet/26.4.404.
34. M. Kačuráková and R. H. Wilson, *Carbohydr. Polym.*, 2001, **44**, 291–303, DOI: 10.1016/s0144-8617(00)00245-9.
35. A. A. Ismail, F. R. van de Voort, G. Emo and J. Sedman, *J. Am. Oil Chem. Soc.*, 1993, **70**, 335–341, DOI: 10.1007/bf02552703.
36. S. Esslinger, J. Riedl and C. Fauhl-Hassek, *Food Res. Int.*, 2014, **60**, 189–204, DOI: 10.1016/j.foodres.2013.10.015.
37. A. Batayhi, M. Özgölet, H. Cankurt and M. Arici, Zenodo, kanfood: Kolmogorov–Arnold networks as closed-form calibrations for food spectroscopy, version 2.2.0, 2026, DOI: 10.5281/zenodo.23168994.
38. F. Pedregosa, G. Varoquaux, A. Gramfort, V. Michel, B. Thirion, O. Grisel, M. Blondel, P. Prettenhofer, R. Weiss, V. Dubourg, J. Vanderplas, A. Passos, D. Cournapeau, M. Brucher, M. Perrot and E. Duchesnay, *J. Mach. Learn. Res.*, 2011, **12**, 2825–2830.
