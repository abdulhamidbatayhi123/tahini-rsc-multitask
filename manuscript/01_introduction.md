## 1 Introduction

Tahini is a paste of roasted, hulled sesame seeds and a staple of Middle Eastern and Mediterranean
cuisine. Its price invites substitution with cheaper oilseed pastes such as sunflower or peanut paste,
which look and taste similar once blended. Substitution with peanut is also a safety problem, because
peanut is a major allergen and tahini consumers who avoid peanut have no reason to suspect it; products
sold as tahini have been recalled for undeclared peanut.[@fsa2018] Targeted reference methods exist:
gas chromatography of the fatty acids detects foreign oils in sesame oil;[@peng2015] real-time PCR
and liquid chromatography–mass spectrometry detect allergenic nuts at mg kg<sup>−1</sup>
levels;[@torricelli2020;@new2020] and nuclear magnetic resonance spectroscopy detects peanut in other
foods.[@schmitt2020] They are slow, need trained staff and answer only the question they
were designed for. A rapid screen that flags a suspect sample and estimates how much of it is not
tahini would decide which samples are worth sending to such a laboratory.

Mid-infrared spectroscopy with attenuated total reflectance (ATR–FTIR) fits that role. It needs no
sample preparation, takes about a minute per spectrum, and records the bands of the lipids, proteins and
carbohydrates that make up an oilseed paste.[@guillen1997;@barth2007] Combined with chemometrics,
infrared spectroscopy has been used to authenticate edible oils,[@rohman2010;@ozulku2017;@ozen2024] to
follow lipid oxidation in a sunflower kernel paste[@muresan2016] and, more recently, to authenticate tahini.
Kucukcelebioglu et al. built one-class models for tahini spiked with oils,[@kucukcelebioglu2026] and we
released 1554 ATR–FTIR spectra of tahini blended with sunflower or peanut paste and compared six
calibration models on them.[@batayhi2026] The chemistry makes the task hard: the three pastes are
dominated by the same triglyceride bands, so adulteration changes the intensity of shared bands rather
than adding new ones.[@batayhi2026] The standard chemometric answer is a pair of models, partial
least-squares discriminant analysis (PLS-DA) for the yes-or-no decision and PLS regression for the
amount.[@wold2001]

Neural networks can replace such pairs with one model. In multitask learning, related outputs share a
common hidden representation and are trained together, so that each task can act as a regulariser for
the other.[@caruana1997] Multitask networks that classify and quantify adulteration from one spectrum
have been reported for olive oil by Raman spectroscopy[@liang2024;@qin2026] and for turmeric powder by
near-infrared spectroscopy,[@zeng2026] and the coupling between identifying a component and estimating
its concentration has been treated as a learning problem in its own right.[@ning2026] For screening,
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
is a recognised cause of irreproducible results in spectroscopy and machine learning.[@guo2017;@kapoor2023]
At least one of the multitask studies above divided its spectra, which included repeated measurements
of each blend, between cross-validation folds at random,[@qin2026] so how such networks behave on new
material is largely unknown. On the present data the
difference is large: a scan-level random split, the default of most machine-learning tutorials, puts
54 of the 55 physical samples on both sides of the split (ESI). In our earlier study, when a whole
production lot was withheld, the detection limits rose to 9–22 % adulterant and authentic tahini from
the lots least like the others was flagged as adulterated.[@batayhi2026]
<!-- 54 of 55: audit/check_split.py. LOD 8.9-21.6 % and T1/T5 false positives: Foods 15:3639 Section 3.2 and Table 5. Qin 2026 random 5-fold: T-TR1 (full text read by cs); re-verify wording before submission. -->

The present study uses the released tahini spectra[@batayhi2026] to ask three questions under
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
