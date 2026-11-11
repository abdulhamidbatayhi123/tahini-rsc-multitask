## 1 Introduction

Tahini is a paste of roasted, hulled sesame seeds and a staple of Middle Eastern and Mediterranean
cuisine. Its price invites substitution with cheaper oilseed pastes such as sunflower or peanut paste,
which look and taste similar once blended. Substitution with peanut is also a safety problem, because
peanut is a major allergen and tahini consumers who avoid peanut have no reason to suspect it; products
sold as tahini have been recalled for undeclared peanut.[@fsa2018] Targeted reference methods exist:
gas chromatography of the fatty acids detects foreign oils in sesame oil;[@peng2015] real-time PCR
and liquid chromatography–mass spectrometry detect allergenic nuts at mg kg<sup>−1</sup>
levels;[@stephan2004;@torricelli2020;@new2020] and nuclear magnetic resonance spectroscopy detects peanut in other
foods.[@schmitt2020] They are slow, need trained staff and answer only the question they
were designed for. A rapid screen that flags a suspect sample and estimates how much of it is not
tahini would decide which samples are worth sending to such a laboratory.

Mid-infrared spectroscopy with attenuated total reflectance (ATR–FTIR) fits that role. It needs no
sample preparation, takes about a minute per spectrum, and records the bands of the lipids, proteins and
carbohydrates that make up an oilseed paste.[@guillen1997;@barth2007] Combined with chemometrics,
infrared spectroscopy has been used to authenticate edible oils,[@rohman2010;@ozulku2017;@ozen2024] to
follow lipid oxidation in a sunflower kernel paste[@muresan2016] and, more recently, to authenticate tahini:
Kucukcelebioglu et al. built one-class ATR–FTIR and UV–Vis models for tahini spiked with peanut or sunflower
oil.[@kucukcelebioglu2026] Earlier, Temiz et al. had quantified sunflower oil in the oil extracted from tahini
by synchronous fluorescence spectroscopy.[@temiz2017] Both studies used an oil as the adulterant. We
released 1554 ATR–FTIR spectra of tahini blended with sunflower or peanut paste and compared six
calibration models on them.[@batayhi2026] The chemistry makes the task hard: the three pastes are
dominated by the same triglyceride bands, so adulteration changes the intensity of shared bands rather
than adding new ones.[@batayhi2026] The standard chemometric answer is a pair of models, partial
least-squares discriminant analysis (PLS-DA) for the yes-or-no decision and PLS regression for the
amount.[@wold2001;@brereton2014]

Neural networks can replace such pairs with one model. In multitask learning, related outputs share a
common hidden representation and are trained together, so that each task can act as a regulariser for
the other.[@caruana1997] Multitask networks that classify and quantify adulteration from one spectrum
have been reported for olive oil by Raman spectroscopy,[@liang2024;@qin2026] for turmeric powder[@zeng2026] and
chicken in lamb[@fan2026] by near-infrared spectroscopy, for protein adulterants in milk powder by laser-induced
breakdown spectroscopy[@shao2026] and for Fritillaria bulb powder by hyperspectral imaging,[@ding2027] and the coupling between identifying a component and estimating
its concentration has been treated as a learning problem in its own right.[@ning2026] For screening,
the two tasks are tied by definition: a sample is adulterated exactly when its tahini fraction is below
100 %. A network with two output layers (heads), one for the class and one for the composition, can
therefore reach the decision in two ways. It can take it directly from the classification head (a
qualitative limit test), or compare the predicted composition with a cut-off (a quantitative test
with a decision limit). Which of
the two should make the decision when the network meets material it was not calibrated on has not, to
our knowledge, been tested. The multitask studies we examined in full report classification accuracy and
regression error side by side, without deriving a screening decision from the predicted amount or comparing
it with the classification output.[@fan2026;@shao2026;@ding2027]

That test is where many spectroscopic studies are weakest. A paste is usually scanned many times, and
replicate scans of one sample are far more alike than scans of different samples. When replicate scans
are split at random between training and test sets, the model is tested on near-copies of its training
data, and the reported accuracy measures memory rather than generalisation; this form of data leakage
is a recognised cause of irreproducible results in spectroscopy and machine learning.[@guo2017;@kapoor2023]
Of the multitask studies above, one divided its samples, each measured repeatedly, between cross-validation
folds at random without stating that the repeated measurements were kept together,[@qin2026] one divided all
spectra at random between training, validation and test sets,[@shao2026] and one held out, for each mixture,
one of four replicate preparations made from the same raw materials.[@ding2027] Only the first applied its
network to material from outside the training set: commercial blends of one nominal composition, for which it
reported the predicted olive-oil content, without testing whether authentic oil from new sources was accepted.[@qin2026]
How such networks decide on new authentic material is therefore largely unknown. On the present data the
difference is large: a scan-level random split, the default of most machine-learning tutorials, puts
54 of the 55 physical samples on both sides of the split (ESI). In our earlier study, with each
authentic lot serving as the blank while it was withheld, the detection limits were 8.9–21.6 % adulterant,
and authentic tahini from the lots least like the others was flagged as adulterated;[@batayhi2026] on
other ATR–FTIR adulteration data, withholding whole brands degraded every model we tested.[@batayhi2026b]
<!-- Full texts read 2026-11-10 (hub pdfs/; extracted text checked): Fan 2026 p3 'classification dataset (240 samples) was randomly partitioned into five equal-sized subsets', regression 80/20, decision from classification head only, no LOD; Shao 2026 p5 'all spectra randomly partitioned into 70 % for training, 20 % for validation ... 10 % for final testing', 86 pellets, single local-market source; Ding 2027 p4 'partitioned based on the independent repacking sessions', p12 'closed-set scenario', no decision rule. Temiz 2017 p2: oil extracted from tahini with cyclohexane, sunflower oil blends, SFS + PLS. Liang 2024 and Kucukcelebioglu 2026: publisher abstract only (paywalled). -->
<!-- 54 of 55: audit/check_split.py. LOD 8.9-21.6 % (pooled out-of-fold, each authentic lot as blank; nested LOLO 10.3-19.5 %) and T1/T5 false positives: Foods 15:3639 Section 3.2 and Table 5 (T-TR2 fix). Qin 2026 (open access, read live 2026-11-10): Sec. 2.7 'all samples were randomly divided into five mutually exclusive subsets'; Sec. 2.2 three positions x 10 repeated measurements per sample; Sec. 3.7 external validation on 'commercially available blended oil (BO) samples' with 'a nominal olive oil content of 5%', regression only. Ding 2027: Sec. 2.1 four independently weighed, mixed and packed batches, the fourth held out; Sec. 2.3 'repacking sessions' (T-TR4 wording fix). Foods 15:2949 abstract: 'leave-one-brand-out validation degraded every model' (read live 2026-11-09). -->

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
