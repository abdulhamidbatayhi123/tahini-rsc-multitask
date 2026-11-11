<!-- Corresponding author M. Özgölet (user, 2026-11-09). Numbers checked against the A2 result files 2026-11-09. -->

Dear Executive Editor,

We submit the manuscript "Screening tahini for sunflower and peanut paste on unseen production lots:
a multitask neural network and partial least squares on infrared spectra" for consideration as an
article in *RSC Advances*.

Tahini is substituted with cheaper oilseed pastes, and substitution with peanut paste introduces an
undeclared allergen. Infrared screening combined with machine learning is often reported with
near-perfect accuracy, but usually on random splits of replicate spectra. We ask what such a screen
does when it meets tahini from a production lot it was not calibrated on, and whether its decision
should come from a dedicated classification output or from the predicted composition.

The main findings are:

1. With whole production lots withheld, blends of sunflower or peanut paste were still detected and
   quantified, but every decision route, neural or chemometric, rejected at least one authentic lot.
   A random split of the same spectra hides this entirely.
2. A classification head trained jointly with the composition head brought no gain over a cut-off on
   the predicted composition, which also gives the identity and amount of the adulterant.
3. The rejected lot differs between model families, and we trace it to where the spectra differ: the
   network rejects the lot that departs most from the others (a broad absorbance difference near
   1180–1280 cm⁻¹, confirmed by second-derivative spectra to involve no shifted band), and PLS
   rejects the lot whose spectral departure lies along its regression vector. Bands that the sample
   does not produce show that the authentic lots were measured under different conditions, so lot and
   measurement session cannot be separated, and the manuscript states this limitation. In an exploratory analysis,
   requiring both models to agree removed the false positives, as it must once they reject different
   lots, at the cost of one blend with 4 % peanut paste.

The chemistry of the spectra carries the argument. The lot that the network rejects differs from the
others over the ester C–O and amide III region, and second-derivative spectra show no band shift there,
so the difference is a broad change in absorbance, not a new or shifted band (Section 3.5). The lot that
PLS rejects departs along the bands that PLS reads as adulteration.

The spectra were released with our earlier article (Batayhi et al.,
*Foods*, 2026, 15, 3639, doi:10.3390/foods15203639), which compared six single-output calibration models
on them. The present manuscript reuses those data, that study's grouped hold-out partition, its
three-fraction output and its detection-limit convention, and states this in the Introduction and
Experimental section. New relative to that article are the multitask network with a classification head (such
networks have been reported for other foods and are cited), the comparison of
the two decision routes for both model families under leave-one-lot-out validation, the threshold rule
set on authentic training samples, and the spectral analysis of why authentic lots are rejected. No
part of the present results has been published or submitted elsewhere.

All code, the analysis plan with its dated amendments, and every prediction from which the reported
numbers are computed are openly available (https://github.com/abdulhamidbatayhi123/tahini-rsc-multitask;
archived release v1.1.1, https://doi.org/10.5281/zenodo.24126434).
Analyses added after the results were seen are labelled exploratory in the manuscript.

We believe the work fits the analytical and food chemistry scope of *RSC Advances*, and that its
practical message is useful beyond tahini: the authentic reference set and the conditions under which
it is measured, not the model architecture, limit infrared screening of food pastes.

Generative AI declaration (RSC policy): the authors did this work with the help of an AI tool, Claude
Opus 5.5 (Anthropic), which helped write the analysis and figure code, search the literature, compile
the references, and draft and edit the text. Its use is described in Section 2.9 and in the
Acknowledgements; every reported number is produced by the archived code.

There are no conflicts of interest to declare.

Yours sincerely,

Muhammed Özgölet, on behalf of all authors (Arzu Yılmaz, Abdulhamid Batayhi, Muhammed Özgölet and Muhammet Arici)
