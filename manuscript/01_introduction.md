## 1 Introduction

Tahini is a paste of roasted, hulled sesame seeds and a staple of Middle Eastern and Mediterranean
cuisine. Its price invites substitution with cheaper oilseed pastes such as sunflower or peanut paste,
which look and taste similar once blended. Substitution with peanut is also a safety problem, because
peanut is a major allergen and tahini consumers who avoid peanut have no reason to suspect it; products
sold as tahini have been recalled for undeclared peanut.[@fsa2018] Targeted reference methods exist:
gas chromatography of the fatty acids detects foreign oils in sesame oil,[@peng2015] and real-time PCR,
immunoassays and liquid chromatography–mass spectrometry detect allergenic nuts at mg kg<sup>−1</sup>
levels.[@torricelli2020;@new2020] They are slow, need trained staff and answer only the question they
were designed for. A rapid screen that flags a suspect sample and estimates how much of it is not
tahini would decide which samples are worth sending to such a laboratory.

Mid-infrared spectroscopy with attenuated total reflectance (ATR–FTIR) fits that role. It needs no
sample preparation, takes about a minute per spectrum, and records the bands of the lipids, proteins and
carbohydrates that make up an oilseed paste.[@guillen1997;@barth2007] Combined with chemometrics it has
been used to authenticate edible oils[@rohman2010;@ozulku2017;@ozen2024] and, more recently, tahini.
Kucukcelebioglu et al. built one-class models for tahini spiked with oils,[@kucukcelebioglu2026] and we
released 1554 ATR–FTIR spectra of tahini blended with sunflower or peanut paste and compared six
calibration models on them.[@batayhi2026] The chemistry makes the task hard: the three pastes are
dominated by the same triglyceride bands, so adulteration changes the intensity of shared bands rather
than adding new ones.[@batayhi2026] The standard chemometric answer is a pair of models, partial
least-squares discriminant analysis (PLS-DA) for the yes-or-no decision and PLS regression for the
amount.[@wold2001]

Neural networks can replace such pairs with one model. In multitask learning, related outputs share a
common hidden representation and are trained together, so that each task can act as a regulariser for
the other.[@caruana1997] For food screening the two tasks are naturally related: a sample is adulterated
exactly when its tahini fraction is below 100 %. One network with a classification head and a
composition head would give the decision, the identity of the adulterant and its amount in a single
pass, and a softmax composition head guarantees a physically valid answer, non-negative fractions that
sum to 100 %. Whether the two heads agree, and which of them should make the decision, has not been
tested on material from a new production lot.

That test is where many spectroscopic studies are weakest. A paste is usually scanned many times, and
replicate scans of one sample are far more alike than scans of different samples. When replicate scans
are split at random between training and test sets, the model is tested on near-copies of its training
data, and the reported accuracy measures memory rather than generalisation; this form of data leakage
is a recognised cause of irreproducible machine-learning results.[@kapoor2023] On the present data the
difference is large. A scan-level random split, the default of most machine-learning tutorials, put
54 of the 55 physical samples on both sides and returned two misclassified scans out of 311 and an AUC
of 0.9998 (ESI). In our earlier study, when a whole production lot was withheld, the detection limits
were 9–22 % adulterant for the leading models.[@batayhi2026]
<!-- 54 of 55, 311, 150/161: audit/check_split.py; AUC 0.9998 and 2 errors: originals_preliminary/2.png, 3.png (preliminary run); replace by our own random-scheme numbers from results/metrics.csv when available. LOD 8.93-21.59 %: Foods 15:3639 Section 3.2 -->

The present study therefore asks whether a single multitask network can screen tahini for sunflower
or peanut paste and quantify the substitution when it meets a production lot it has never seen, and how
it compares with PLS-DA and PLS regression under identical validation. TODO contributions after results.
