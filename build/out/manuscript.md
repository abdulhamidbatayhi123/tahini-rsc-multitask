---
title: "Screening tahini for sunflower and peanut paste on unseen production lots: a multitask neural network and partial least squares on ATR–FTIR spectra"
---


Abdulhamid Batayhi,^a^ Muhammed Özgölet,^b^ Hasan Cankurt^b,c^ and Muhammet Arici^b^

^a^ Department of Mechatronics Engineering, Faculty of Mechanical Engineering, Yildiz Technical University, 34220 Istanbul, Türkiye.
^b^ Department of Food Engineering, Faculty of Chemical and Metallurgical Engineering, Yildiz Technical University, 34220 Istanbul, Türkiye.
^c^ Department of Nutrition and Dietetics, Faculty of Health Sciences, Biruni University, 34214 Istanbul, Türkiye.

Electronic supplementary information (ESI) available. See DOI: to be assigned.

## Abstract

Tahini is substituted with cheaper oilseed pastes, and peanut paste adds an undeclared allergen. We
tested whether a multitask neural network can screen tahini for sunflower or peanut paste and
estimate the substitution from one attenuated total reflectance Fourier-transform infrared (ATR–FTIR)
spectrum when it meets a production lot it was not calibrated on, and whether the screening
decision should come from a classification head or from the predicted composition. On 1554 spectra
of 55 physical samples from five tahini lots, the network and the chemometric pair of PLS-DA and PLS
regression were validated with whole samples and whole lots withheld. On a conventional grouped
hold-out, every decision route accepted the authentic test lot. With each lot withheld in turn, blends
were still detected (sample-level sensitivity 98–100% for the composition-based routes) and the
composition was predicted with a root-mean-square error of 4.1–4.9% tahini, but every route rejected at
least one authentic lot (specificity 60–84%). The classification head brought no gain over a cut-off on
the predicted composition. The rejected lot differed between model families: lot T1, whose ester C–O
and amide III region at 1180–1280 cm<sup>−1</sup> departs most from the other lots, for the network, and lot T5,
whose spectral departure lies along the PLS regression vector, for PLS. In an exploratory analysis,
flagging a sample only when both composition routes agreed accepted all five authentic lots and
detected 49 of 50 blends. Lot-to-lot variation of authentic tahini, not model architecture, limits
infrared screening.



## 1 Introduction

Tahini is a paste of roasted, hulled sesame seeds and a staple of Middle Eastern and Mediterranean
cuisine. Its price invites substitution with cheaper oilseed pastes such as sunflower or peanut paste,
which look and taste similar once blended. Substitution with peanut is also a safety problem, because
peanut is a major allergen and tahini consumers who avoid peanut have no reason to suspect it; products
sold as tahini have been recalled for undeclared peanut.^1^ Targeted reference methods exist:
gas chromatography of the fatty acids detects foreign oils in sesame oil;^2^ real-time PCR
and liquid chromatography–mass spectrometry detect allergenic nuts at mg kg<sup>−1</sup>
levels;^3,4^ and nuclear magnetic resonance spectroscopy detects peanut in other
foods.^5^ They are slow, need trained staff and answer only the question they
were designed for. A rapid screen that flags a suspect sample and estimates how much of it is not
tahini would decide which samples are worth sending to such a laboratory.

Mid-infrared spectroscopy with attenuated total reflectance (ATR–FTIR) fits that role. It needs no
sample preparation, takes about a minute per spectrum, and records the bands of the lipids, proteins and
carbohydrates that make up an oilseed paste.^6,7^ Combined with chemometrics,
infrared spectroscopy has been used to authenticate edible oils,^8–10^ to
follow lipid oxidation in a sunflower kernel paste^11^ and, more recently, to authenticate tahini.
Kucukcelebioglu et al. built one-class models for tahini spiked with oils,^12^ and we
released 1554 ATR–FTIR spectra of tahini blended with sunflower or peanut paste and compared six
calibration models on them.^13^ The chemistry makes the task hard: the three pastes are
dominated by the same triglyceride bands, so adulteration changes the intensity of shared bands rather
than adding new ones.^13^ The standard chemometric answer is a pair of models, partial
least-squares discriminant analysis (PLS-DA) for the yes-or-no decision and PLS regression for the
amount.^14^

Neural networks can replace such pairs with one model. In multitask learning, related outputs share a
common hidden representation and are trained together, so that each task can act as a regulariser for
the other.^15^ Multitask networks that classify and quantify adulteration from one spectrum
have been reported for olive oil by Raman spectroscopy^16,17^ and for turmeric powder by
near-infrared spectroscopy,^18^ and the coupling between identifying a component and estimating
its concentration has been treated as a learning problem in its own right.^19^ For screening,
the two tasks are tied by definition: a sample is adulterated exactly when its tahini fraction is below
100 %. A network with a classification head and a composition head therefore offers two ways to reach
the same decision, either directly from the classification head (a qualitative limit test) or by
comparing the predicted composition with a cut-off (a quantitative test with a decision limit). Which of
the two should make the decision when the network meets material it was not calibrated on has not, to
our knowledge, been tested.

That test is where many spectroscopic studies are weakest. A paste is usually scanned many times, and
replicate scans of one sample are far more alike than scans of different samples. When replicate scans
are split at random between training and test sets, the model is tested on near-copies of its training
data, and the reported accuracy measures memory rather than generalisation; this form of data leakage
is a recognised cause of irreproducible results in spectroscopy and machine learning.^20,21^
At least one of the multitask studies above divided its spectra, which included repeated measurements
of each blend, between cross-validation folds at random,^17^ so how such networks behave on new
material is largely unknown. On the present data the
difference is large: a scan-level random split, the default of most machine-learning tutorials, puts
54 of the 55 physical samples on both sides of the split (ESI). In our earlier study, when a whole
production lot was withheld, the detection limits rose to 9–22 % adulterant and authentic tahini from
the lots least like the others was flagged as adulterated.^13^


The present study uses the released tahini spectra^13^ to ask three questions under
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

The spectra are the tahini set released with our earlier calibration study (ref. 13), where the
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

Each spectrum was corrected by the standard normal variate (SNV),^22^ which acts on one spectrum at a time
and therefore cannot leak information between training and test sets. The models were then given the
two regions that carry the chemistry of the pastes, 2800–3050 cm<sup>−1</sup> (C–H stretching) and
600–1800 cm<sup>−1</sup> (carbonyl, amide and fingerprint bands), 752 channels in total. The atmospheric CO<sub>2</sub>
band (about 2250–2400 cm<sup>−1</sup>) and the water-vapour rotation lines above 3550 cm<sup>−1</sup> were excluded because
they record the state of the optical path, not the sample. The full 600–4000 cm<sup>−1</sup> range was run as a
sensitivity analysis (ESI).


### 2.3 Multitask network

The multitask deep neural network (MT-DNN) has a shared trunk of two fully connected layers (128 and 64
units, ReLU activation, dropout 0.2 after the first) and two heads (Fig. 2). Head A is a single sigmoid
unit that gives the probability that the scan is adulterated. Head B is a three-unit softmax whose
outputs, multiplied by 100, are the tahini, sunflower and peanut fractions; the softmax makes the
predicted composition non-negative and sum to 100 % by construction. The loss is the binary
cross-entropy of head A (targets smoothed by 0.05) plus ten times the mean squared error of head B on
fractions scaled to 0–1. Inputs were standardised channel by channel with the training-set mean and SD.
Training used Adam (learning rate 10<sup>−3</sup>, weight decay 10<sup>−4</sup>, batch size 32) for at most 300 epochs. Early
stopping monitored the loss on an inner validation set of 20 % of the training samples, drawn by
physical sample, with a patience of 30 epochs after a minimum of 20, and the weights of the best epoch
were restored. Every MT-DNN result is the mean over five random seeds. The network was implemented in
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
predictions on the training scans themselves would understate their spread. For sample-level decisions,
the scans of one physical sample were averaged and the mean compared with the same threshold.

### 2.6 Validation

The unit of splitting is the physical sample. Replicate scans of one sample are far more alike than
scans of different samples, so a split that separates them would test the model on near-copies of its
training data. Two designs were used. The first is the grouped 70/30 hold-out of ref. 13, which puts
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
limit of detection followed the calibration-slope convention of ref. 13, LOD = 3.3σ/S, where σ is the
SD of the predicted adulterant fraction of withheld authentic scans and S the slope of predicted on
nominal adulterant fraction.^23^ In leave-one-lot-out validation the predictions of the five
withheld lots are pooled, so σ includes the differences between authentic lots; within the hold-out test
set, which holds a single authentic lot, σ reflects replicate scatter only and the LOD is given for
comparison. All 95 % intervals are cluster-bootstrap percentiles (1000 draws) that
resample whole physical samples, never single scans;^24^ for the MT-DNN each draw averages the five seeds.
With five lots the lot level is too coarse to resample, so lot-out results are also reported fold by
fold.

### 2.8 Exploratory analyses

Two analyses were added after the leave-one-lot-out results had been seen and are reported as
exploratory. For each authentic lot, the mean SNV spectrum of the lot minus the mean of the other four
lot means was divided by the pooled within-lot SD, to locate the bands in which the lot departs from
the others, and the unscaled difference was projected on the tahini coefficient vector of the PLS-R
model that had withheld that lot, to estimate how far the departure alone moves the PLS prediction. A
sample-level agreement rule, which flags a sample only when both regression routes (PLS-R and MT-DNN-R)
flag it, was also evaluated. Code, predictions and the analysis plan with its amendments are in the
repository (Data availability).


## 3 Results and discussion

### 3.1 What separates the three pastes in the mid-infrared

The mean spectra of the three pastes are dominated by the same lipid bands (Fig. 1a): the olefinic
=C–H stretch near 3008 cm<sup>−1</sup>, the CH<sub>2</sub> stretches at 2922 and 2853 cm<sup>−1</sup>, the ester carbonyl near
1745 cm<sup>−1</sup>, the CH<sub>2</sub> scissoring near 1463 cm<sup>−1</sup>, the ester C–O stretches around 1160 cm<sup>−1</sup> and the CH<sub>2</sub>
rocking band near 721 cm<sup>−1</sup>.^6^ The protein of the seeds adds the amide I and amide II bands
near 1650 and 1540 cm<sup>−1</sup>.^7^ Adulteration therefore changes the relative intensity of bands
that all three pastes share. After SNV, pure sunflower paste differs from authentic tahini mainly by
weaker CH<sub>2</sub> stretching (−0.29 and −0.22 SNV units at 2920 and 2851 cm<sup>−1</sup>) and stronger absorption at
989 and 1051 cm<sup>−1</sup> (+0.25 and +0.20), the region of C–O stretching in carbohydrates,^25^
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

TODO random vs grouped (after random run): ESI table.

### 3.3 Benchmark: the grouped hold-out

On the grouped hold-out of the earlier study, every route accepted all scans of the authentic test
sample and the regression routes flagged every blend scan (Table 1). The class routes were slightly
weaker: the MT-DNN class head missed one blend scan, and PLS-DA missed 25 scans, with two blend samples
(76 % tahini with sunflower and 84 % tahini with peanut paste) falling on the authentic side.
Quantification reproduced the published benchmark: PLS gave R<sup>2</sup> 0.997 and RMSEP 1.93 % tahini and the
MT-DNN composition head 0.985 and 4.02 %, against 0.994 for PLS and 0.988 for a single-task network in
ref. 13. This partition is the easy case. Its test set holds one authentic lot and no
blend below 16 % adulterant, so the perfect specificity rests on a single authentic sample. It also
gives a misleading detection limit: the softmax output of the MT-DNN saturates at 0 % adulterant for
the authentic test scans (σ = 0.02 percentage points), which gives an LOD of 0.07 %, whereas PLS, whose
output is not bounded, gave 2.7 %. Neither figure measures what happens with a new lot.


### 3.4 Screening production lots never seen in training

Withholding each production lot in turn changed the picture in one respect only (Fig. 3, Table 1).
Blends were still detected: at sample level the MT-DNN routes flagged all 50 withheld blends, PLS-R
missed one (4 % peanut paste in lot T1) and PLS-DA missed six. PLS-DA was the weakest route throughout.
It missed all scans of the 12 % blends and most of those at 16, 32 and 36 % (Fig. 3b), and the number
of latent variables chosen for it ranged from 2 to 22 across folds, a sign that the discriminant
direction was poorly determined by four lots.

Authentic tahini from a new lot was the problem. Every route rejected at least one of the five withheld
authentic lots (Fig. 3a), so the sample-level specificity ranged from 60 % for PLS-DA to 84 % for the
MT-DNN class head, with 95 % intervals reaching down to 0–60 %. The failures were concentrated in one
lot per model family. The two MT-DNN routes flagged lot T1 (78 % of its scans by the class head and 94 %
by the composition cut-off), PLS-R flagged lot T5 (100 %), and PLS-DA flagged T1 entirely and half of
T2. The remaining lots were accepted almost completely by every route. This pattern, in which the
false positives come from whole lots rather than from scattered scans, was also seen for the six
single-task models of the earlier study, where PLS and the multilayer perceptron flagged T1 and T5 and
other models flagged other lots.^13^ It means that the specificity of any of these screens is
set by how far a new authentic lot lies from the calibration lots, not by the scan-to-scan noise that a
hold-out estimate measures.


The pooled lot-out detection limit was 11.1 % adulterant for PLS (σ = 3.2 percentage points), close to
the 10.3–19.5 % reported for the leading models under nested lot-out validation in ref. 13.
The MT-DNN gave 3.8 % (σ = 1.1), but this figure should not be read as a fourfold gain in sensitivity.
Its σ is small because the softmax output cannot fall below 0 % adulterant, so authentic lots that the
network recognises contribute almost no spread, and the one lot it does not recognise (T1) sits above
its threshold. The calibration-slope LOD assumes an unbounded, roughly normal blank response, and a
saturating output violates that assumption.


### 3.5 Why a withheld authentic lot is rejected

The rejected lots are those whose spectra depart from the other four in the directions that each model
reads as adulteration (Fig. 5). Lot T1 departs most: the root-mean-square departure of its mean SNV
spectrum from the other lots is 1.61 pooled within-lot SDs, against 1.11–1.36 for the others, and the
departure is concentrated between 1180 and 1280 cm<sup>−1</sup>, where T1 absorbs 4.9–8.4 SDs less than the other lots
at 1215, 1248 and 1273 cm<sup>−1</sup> (Fig. 5b). This region holds the C–O stretching of the ester groups of the
triglycerides^6^ and the amide III band of the proteins.^7^ The MT-DNN, which flagged
T1, predicted 2.6 % adulterant for its authentic scans on average, against a threshold of 0.5–1.2 %
set on the four training lots, for which the softmax output was close to zero (Fig. 5a). The same
lot also carried the largest quantification error of the network: the tahini fraction of the T1 blends
was underestimated by 6.0 percentage points on average, against at most 1.7 for the other lots.

Lot T5 is not the most atypical lot overall, but its departure lies along the PLS regression vector.
Projected on the PLS tahini and adulterant coefficients of the model that withheld it, the T5 departure
alone moves the prediction by 8.9 percentage points towards adulteration, against 3.0 for T1 and less
than 2 for T2 and T3, and the observed mean prediction for authentic T5 was 10.3 % adulterant, above the
6.1 % threshold of that fold. For lot T4 the projection points the other way, towards a tahini fraction
above 100 %, which the clipping of the PLS output turns into a small positive bias. Lot T2 has the
largest departure at 1709 cm<sup>−1</sup> (+4.1 SDs), the carbonyl band of free fatty acids,^6^ which
suggests more hydrolysis of its triglycerides; this did not cause false positives for the regression
routes but may explain why PLS-DA rejected half of its scans. These band assignments are offered as
interpretation of an exploratory analysis, not as proof of cause.

The two model families therefore fail for different reasons. PLS is a linear projection, and a lot is
rejected when its spectral difference happens to align with the regression vector, whatever the size of
that difference. The MT-DNN is non-linear and its softmax output is confident wherever the training data
are dense, so a lot is rejected when it is far from all four training lots in any direction, as T1 is.


### 3.6 Quantification and identification of the adulterant

Both composition outputs transferred to new lots far better than the decisions built on them (Fig. 4).
Over the five withheld lots, PLS gave a scan-level R<sup>2</sup> of 0.979 and RMSEP of 4.87 % tahini and the
MT-DNN 0.985 and 4.11 %, with overlapping intervals (Table 1); at sample level, where averaging removes
replicate scatter but not lot bias, the order reversed (PLS 3.80 %, MT-DNN 4.64 %). The errors of each
model were concentrated in the lot it also misjudged at the screening step: the lot-wise RMSEP was
largest for T5 with PLS (7.97 %) and for T1 with the MT-DNN (6.14 %), and 2.9–4.4 % for every other lot
and model. The adulterant was identified correctly in 97 % of blend scans by both families, with the
lowest lot-wise value, 93 %, for lot T4 with both. Lot-out quantification is thus about twice as
uncertain as the hold-out suggested for PLS (RMSEP 4.87 against 1.93 %) and about as uncertain for the
MT-DNN (4.11 against 4.02 %); the network loses less when moving to a new lot but starts from a worse
hold-out calibration.


### 3.7 One network or two models?

The classification head did not make the network a better screen than its own composition output. On
withheld lots the class head and the composition cut-off of the MT-DNN agreed on which lot to reject,
detected blends equally well (scan-level sensitivity 99.7 and 99.3 %) and had intervals that overlap
completely (Table 1). The same holds for PLS, where the regression route was better than PLS-DA on
every count. A dedicated classifier adds a second decision to calibrate and, in the PLS family, a less
stable one; thresholding the predicted composition gives the decision, the identity of the adulterant
and its amount from one output, and has a threshold that can be read in composition units. The value
of the multitask network lies elsewhere: it is a second, non-linear view of the same spectra whose
errors fall on different lots from those of PLS.

That complementarity suggests a simple rule, which we tested only after seeing the results: flag a
sample only when both regression routes flag it. Applied to the lot-out predictions, the rule accepted
all five withheld authentic lots and still flagged 49 of the 50 blends, for each of the five network
seeds; the one blend missed was the 4 % peanut paste blend of lot T1, which PLS-R alone also missed.
With five authentic lots this is a hypothesis, not a validated screening rule, and it will fail for a
lot that departs along the PLS vector and from the network's training data at the same time. It does
show that combining a linear and a non-linear calibration is a cheaper way to protect specificity than
an additional classification head, and it should be tested on lots not used here.



Table 1 Screening, quantification and identification on withheld samples (chemically informative regions). Values are point estimates with cluster-bootstrap 95 % intervals (1000 draws over physical samples); MT-DNN values are means over five seeds. Quantification and identification are properties of the composition output and are shown once per model family. The hold-out test set contains a single authentic lot, so its specificity rests on one authentic sample; in leave-one-lot-out validation five authentic samples, one per lot, are withheld.

| Validation | Level | Route | Sensitivity (%) | Specificity (%) | AUC | RMSEP (%) | R² | Identification (%) |
|---|---|---|---|---|---|---|---|---|
| Grouped hold-out | sample | PLS-DA | 87.5 (77.8–100.0) | 100.0 (100.0–100.0) | 1.000 (1.000–1.000) |  |  |  |
| Grouped hold-out | sample | PLS-R | 100.0 (100.0–100.0) | 100.0 (100.0–100.0) | 1.000 (1.000–1.000) | 1.42 (1.15–1.62) | 0.997 (0.995–0.998) | 100.0 (100.0–100.0) |
| Grouped hold-out | sample | MT-DNN | 100.0 (100.0–100.0) | 100.0 (100.0–100.0) | 1.000 (1.000–1.000) | 3.98 (3.19–4.56) | 0.979 (0.961–0.986) | 100.0 (100.0–100.0) |
| Grouped hold-out | sample | MT-DNN-R | 100.0 (100.0–100.0) | 100.0 (100.0–100.0) | 1.000 (1.000–1.000) |  |  |  |
| Grouped hold-out | scan | PLS-DA | 90.3 (74.2–100.0) | 100.0 (100.0–100.0) | 0.999 (0.997–1.000) |  |  |  |
| Grouped hold-out | scan | PLS-R | 100.0 (100.0–100.0) | 100.0 (100.0–100.0) | 1.000 (1.000–1.000) | 1.93 (1.69–2.30) | 0.997 (0.987–0.997) | 100.0 (100.0–100.0) |
| Grouped hold-out | scan | MT-DNN | 99.6 (98.8–100.0) | 100.0 (100.0–100.0) | 1.000 (1.000–1.000) | 4.02 (2.67–5.58) | 0.985 (0.933–0.992) | 99.8 (99.5–100.0) |
| Grouped hold-out | scan | MT-DNN-R | 100.0 (100.0–100.0) | 100.0 (100.0–100.0) | 1.000 (1.000–1.000) |  |  |  |
| Leave-one-lot-out | sample | PLS-DA | 88.0 (81.2–94.4) | 60.0 (0.0–100.0) | 0.888 (0.750–1.000) |  |  |  |
| Leave-one-lot-out | sample | PLS-R | 98.0 (96.4–100.0) | 80.0 (50.0–100.0) | 0.984 (0.943–1.000) | 3.80 (3.08–4.34) | 0.985 (0.979–0.991) | 96.0 (92.9–100.0) |
| Leave-one-lot-out | sample | MT-DNN | 100.0 (100.0–100.0) | 84.0 (60.0–100.0) | 0.998 (0.994–1.000) | 4.64 (3.89–5.21) | 0.978 (0.968–0.985) | 97.2 (95.3–100.0) |
| Leave-one-lot-out | sample | MT-DNN-R | 100.0 (100.0–100.0) | 80.0 (50.0–100.0) | 0.998 (0.994–1.000) |  |  |  |
| Leave-one-lot-out | scan | PLS-DA | 88.5 (79.5–95.9) | 69.6 (27.1–100.0) | 0.871 (0.655–0.997) |  |  |  |
| Leave-one-lot-out | scan | PLS-R | 97.4 (94.4–100.0) | 79.7 (33.0–100.0) | 0.986 (0.950–1.000) | 4.87 (3.37–6.58) | 0.979 (0.953–0.990) | 97.2 (93.5–100.0) |
| Leave-one-lot-out | scan | MT-DNN | 99.7 (99.2–100.0) | 83.5 (48.3–100.0) | 0.995 (0.983–1.000) | 4.11 (3.26–5.24) | 0.985 (0.973–0.990) | 97.0 (93.8–99.9) |
| Leave-one-lot-out | scan | MT-DNN-R | 99.3 (98.3–100.0) | 80.6 (37.6–100.0) | 0.999 (0.997–1.000) |  |  |  |




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

First, the decision is best taken from the predicted composition. The classification head added a
second output to calibrate without improving sensitivity or specificity, and PLS-DA was the least
stable route of all. A cut-off on the predicted tahini fraction, set from authentic training samples
alone, gives the decision in composition units together with the amount and identity of the
adulterant.

Second, specificity on new lots, not sensitivity, limits the method. Blends were detected almost
completely on unseen lots, but every route rejected at least one of five authentic lots. The rejected
lot depended on the model: the network rejected the lot that departed most from the others, in the
ester C–O and amide III region near 1180–1280 cm<sup>−1</sup>, and PLS rejected the lot whose departure happened to
lie along its regression vector. Hold-out estimates with a single authentic lot, and scan-level random
splits even more so, hide this behaviour completely.

Third, because the two families fail on different lots, combining them is a promising and cheap way
to protect specificity. In this set, requiring both composition routes to agree removed every false
positive at the cost of one 4 % blend. This rule was found after the results were known and rests on
five authentic lots; it needs testing on new lots, other suppliers and a second instrument before it
can support routine screening. For any such use, the authentic reference set must cover the variation
between lots that the screen will meet,^26^ and a positive result should be confirmed by a targeted method.


## Author contributions


A. Batayhi: conceptualization, methodology, software, formal analysis, data curation, visualization,
writing – original draft. M. Özgölet: investigation, resources, writing – review and editing.
H. Cankurt: conceptualization, investigation, supervision, writing – review and editing. M. Arici:
supervision, writing – review and editing.

## Conflicts of interest

There are no conflicts to declare.

## Data availability

The ATR–FTIR spectra analysed in this study were released with ref. 13 and are available
on Zenodo at https://doi.org/10.5281/zenodo.21446757.^27^ The code for this study (data
loading, models, validation, statistics and figures), the analysis plan with its dated amendments,
and all predictions and result files from which the reported numbers are computed are available at
REPOSITORY-DOI-TO-BE-ASSIGNED. Analyses used Python with scikit-learn 1.7.0^28^ and
PyTorch 2.7.1.

## Acknowledgements


During the preparation of this work the authors used Claude (Anthropic) as a tool to assist with
code, literature searching and language editing. The authors designed the study, made every
scientific decision, checked all output, and take full responsibility for the content of the article.


## References

1. Food Standards Agency, John & Pascalis recalls Four Seasons Sesame Tahini because of undeclared peanuts, Allergy Alert FSA-AA-76-2018, https://www.food.gov.uk/news-alerts/alert/fsa-aa-76-2018 (archived copy: http://web.archive.org/web/20220708013426/https://www.food.gov.uk/news-alerts/alert/fsa-aa-76-2018), (accessed November 2026).
2. D. Peng, Y. Bi, X. Ren, G. Yang, S. Sun and X. Wang, *Food Chem.*, 2015, **188**, 415–421, DOI: 10.1016/j.foodchem.2015.05.001.
3. M. Torricelli, E. Pierboni, C. Rondini, S. Altissimi and N. Haouet, *Foods*, 2020, **9**, 1085, DOI: 10.3390/foods9081085.
4. L. S. New, J. Stahl-Zeng, A. Schreiber, M. Cafazzo, A. Liu, S. Brunelle and H.-F. Liu, *J. AOAC Int.*, 2020, **103**, 570–583, DOI: 10.5740/jaoacint.19-0112.
5. C. Schmitt, T. Bastek, A. Stelzer, T. Schneider, M. Fischer and T. Hackl, *J. Agric. Food Chem.*, 2020, **68**, 14364–14373, DOI: 10.1021/acs.jafc.0c01999.
6. M. D. Guillén and N. Cabo, *J. Sci. Food Agric.*, 1997, **75**, 1–11, DOI: 10.1002/(sici)1097-0010(199709)75:1<1::aid-jsfa842>3.0.co;2-r.
7. A. Barth, *Biochim. Biophys. Acta, Bioenerg.*, 2007, **1767**, 1073–1101, DOI: 10.1016/j.bbabio.2007.06.004.
8. A. Rohman and Y. C. Man, *Food Res. Int.*, 2010, **43**, 886–892, DOI: 10.1016/j.foodres.2009.12.006.
9. G. Ozulku, R. M. Yildirim, O. S. Toker, S. Karasu and M. Z. Durak, *Food Control*, 2017, **82**, 212–216, DOI: 10.1016/j.foodcont.2017.06.034.
10. B. Ozen, C. Cavdaroglu and F. Tokatli, *Anal. Methods*, 2024, **16**, 4216–4233, DOI: 10.1039/d4ay00562g.
11. V. Mureșan, S. Danthine, A. E. Mureșan, E. Racolța, C. Blecker, S. Muste, C. Socaciu and V. Baeten, *Talanta*, 2016, **155**, 336–346, DOI: 10.1016/j.talanta.2016.04.019.
12. N. Kucukcelebioglu, Y. B. Karakas, C. Cavdaroglu and B. Ozen, *Food Anal. Methods*, 2026, **19**, 358, DOI: 10.1007/s12161-026-03268-5.
13. A. Batayhi, M. Özgölet, H. Cankurt and M. Arici, *Foods*, 2026, **15**, 3639, DOI: 10.3390/foods15203639.
14. S. Wold, M. Sjöström and L. Eriksson, *Chemom. Intell. Lab. Syst.*, 2001, **58**, 109–130, DOI: 10.1016/s0169-7439(01)00155-1.
15. R. Caruana, *Mach. Learn.*, 1997, **28**, 41–75, DOI: 10.1023/a:1007379606734.
16. S. Liang, G. Chen, C. Ma, J. Gu, C. Zhu, L. Li, H. Gao, Z. Yang, J. Cao and Z. Chen, *Food Anal. Methods*, 2025, **18**, 385–397, DOI: 10.1007/s12161-024-02728-0.
17. X. Qin, Y. Chen, B. Li, S. Zeng, G. Mei and C. Yu, *Foods*, 2026, **15**, 2030, DOI: 10.3390/foods15112030.
18. J. Zeng, Z. Wu, E. Zhang, Z. Liu, T. Zhang and L. Li, *J. AOAC Int.*, 2026, **109**, 924–936, DOI: 10.1093/jaoacint/qsag068.
19. H. Ning, M. Ma, Z. Shi and L. Ding, *Anal. Chim. Acta*, 2026, **1391**, 345050, DOI: 10.1016/j.aca.2025.345050.
20. S. Guo, T. Bocklitz, U. Neugebauer and J. Popp, *Anal. Methods*, 2017, **9**, 4410–4417, DOI: 10.1039/c7ay01363a.
21. S. Kapoor and A. Narayanan, *Patterns*, 2023, **4**, 100804, DOI: 10.1016/j.patter.2023.100804.
22. R. J. Barnes, M. S. Dhanoa and S. J. Lister, *Appl. Spectrosc.*, 1989, **43**, 772–777, DOI: 10.1366/0003702894202201.
23. F. Allegrini and A. C. Olivieri, *Anal. Chem.*, 2014, **86**, 7858–7866, DOI: 10.1021/ac501786u.
24. C. A. Field and A. H. Welsh, *J. R. Stat. Soc. B*, 2007, **69**, 369–390, DOI: 10.1111/j.1467-9868.2007.00593.x.
25. M. Kačuráková, *Carbohydr. Polym.*, 2001, **44**, 291–303, DOI: 10.1016/s0144-8617(00)00245-9.
26. S. Esslinger, J. Riedl and C. Fauhl-Hassek, *Food Res. Int.*, 2014, **60**, 189–204, DOI: 10.1016/j.foodres.2013.10.015.
27. A. Batayhi, M. Özgölet, H. Cankurt and M. Arici, Zenodo, kanfood: Kolmogorov–Arnold networks as closed-form calibrations for food spectroscopy, 2026, DOI: 10.5281/zenodo.21446757.
28. F. Pedregosa, G. Varoquaux, A. Gramfort, V. Michel, B. Thirion, O. Grisel, M. Blondel, P. Prettenhofer, R. Weiss, V. Dubourg, J. Vanderplas, A. Passos, D. Cournapeau, M. Brucher, M. Perrot and E. Duchesnay, *J. Mach. Learn. Res.*, 2011, **12**, 2825–2830.
