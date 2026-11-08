## 3 Results and discussion

### 3.1 What separates the three pastes in the mid-infrared

The mean spectra of the three pastes are dominated by the same lipid bands (Fig. 1a): the olefinic
=C–H stretch near 3008 cm<sup>−1</sup>, the CH<sub>2</sub> stretches at 2922 and 2853 cm<sup>−1</sup>, the ester carbonyl near
1745 cm<sup>−1</sup>, the CH<sub>2</sub> scissoring near 1463 cm<sup>−1</sup>, the ester C–O stretches around 1160 cm<sup>−1</sup> and the CH<sub>2</sub>
rocking band near 721 cm<sup>−1</sup>.[@guillen1997] The protein of the seeds adds the amide I and amide II bands
near 1650 and 1540 cm<sup>−1</sup>.[@barth2007] Adulteration therefore changes the relative intensity of bands
that all three pastes share. After SNV, pure sunflower paste differs from authentic tahini mainly by
weaker CH<sub>2</sub> stretching (−0.29 and −0.22 SNV units at 2920 and 2851 cm<sup>−1</sup>) and stronger absorption at
989 and 1051 cm<sup>−1</sup> (+0.25 and +0.20), the region of C–O stretching in carbohydrates,[@kacurakova2001]
and below 700 cm<sup>−1</sup>. Pure peanut paste differs in the opposite direction: stronger CH<sub>2</sub> stretching
(+0.64 and +0.50 at 2920 and 2853 cm<sup>−1</sup>) and ester carbonyl (+0.21 at 1749 cm<sup>−1</sup>), and weaker amide I
(−0.29 at 1655 cm<sup>−1</sup>) and carbohydrate C–O bands (−0.21 to −0.28 between 1041 and 1132 cm<sup>−1</sup>). Relative
to tahini, then, the sunflower paste carries less lipid signal and the peanut paste more, which is
why the two adulterants pull the spectrum in different directions and can be told apart.
<!-- SNV differences: results/lot_departure.json sunflower100/peanut100 (src/s03_lots.py) -->

Most of the information that distinguishes one physical sample from another lies in the two regions
given to the models. The median ratio of between-sample to within-sample variance was 5.0 over
600–1800 cm<sup>−1</sup> and 7.4 over 2800–3050 cm<sup>−1</sup>, against 2.6 in the CO<sub>2</sub> band and 2.6 in the water-vapour
region (Fig. 1b). Within-sample variance is not small anywhere: replicate scans of one sample,
repositioned on the crystal, differ appreciably, and this is the variation that a scan-level split
lets the model see on both sides.
<!-- F medians: results/f1_numbers.json -->

### 3.2 A scan-level split hides the problem

TODO random vs grouped (after random run): ESI table.

### 3.3 Benchmark: the grouped hold-out

On the grouped hold-out of the earlier study, every route accepted all scans of the authentic test
sample and the regression routes flagged every blend scan (Table 1). The class routes were slightly
weaker: the MT-DNN class head missed one blend scan, and PLS-DA missed 25 scans, with two blend samples
(76 % tahini with sunflower and 84 % tahini with peanut paste) falling on the authentic side.
Quantification reproduced the published benchmark: PLS gave R<sup>2</sup> 0.997 and RMSEP 1.93 % tahini and the
MT-DNN composition head 0.985 and 4.02 %, against 0.994 for PLS and 0.988 for a single-task network in
ref. [#batayhi2026]. This partition is the easy case. Its test set holds one authentic lot and no
blend below 16 % adulterant, so the perfect specificity rests on a single authentic sample. It also
gives a misleading detection limit: the softmax output of the MT-DNN saturates at 0 % adulterant for
the authentic test scans (σ = 0.02 percentage points), which gives an LOD of 0.07 %, whereas PLS, whose
output is not bounded, gave 2.7 %. Neither figure measures what happens with a new lot.
<!-- Table 1: src/t1_table.py <- results/metrics.csv (holdout, chem). PLS-DA misses: groups T1_S24 (76 % tahini) and T4_P16 (84 %) from results/pred_holdout_chem.csv (sample mean score <= 0). LOD holdout: metrics.csv lod/lod_sigma (MT-DNN 0.0738, sigma 0.0223; PLS 2.718). Foods: Table 2 PLS 0.994, MLP 0.988. -->

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
other models flagged other lots.[@batayhi2026] It means that the specificity of any of these screens is
set by how far a new authentic lot lies from the calibration lots, not by the scan-to-scan noise that a
hold-out estimate measures.
<!-- sample-level counts: results/consensus.json (PLS-R missed [4, peanut, T1]); results/metrics.csv lolo sample fn: PLS-DA 6, PLS-R 1, MT-DNN 0, MT-DNN-R 0; specificity 0.60/0.80/0.84/0.80. Per-lot FP: results/metrics_lot.csv fp_rate_authentic. PLS-DA k range: results/run_info_lolo_chem.json pls_k_cls 22,4,2,3,3. Level shares: Fig. 3b from pred_lolo_chem.csv. Foods Table 5. -->

The pooled lot-out detection limit was 11.1 % adulterant for PLS (σ = 3.2 percentage points), close to
the 10.3–19.5 % reported for the leading models under nested lot-out validation in ref. [#batayhi2026].
The MT-DNN gave 3.8 % (σ = 1.1), but this figure should not be read as a fourfold gain in sensitivity.
Its σ is small because the softmax output cannot fall below 0 % adulterant, so authentic lots that the
network recognises contribute almost no spread, and the one lot it does not recognise (T1) sits above
its threshold. The calibration-slope LOD assumes an unbounded, roughly normal blank response, and a
saturating output violates that assumption.
<!-- LOD lolo: results/metrics.csv lod 11.076 (sigma 3.155, slope 0.940) PLS; 3.806 (sigma 1.138, slope 0.988) MT-DNN. Foods nested LOLO: KAN 10.3, MLP 17.5, PLS 19.5 % (Section 3.2). -->

### 3.5 Why a withheld authentic lot is rejected

The rejected lots are those whose spectra depart from the other four in the directions that each model
reads as adulteration (Fig. 5). Lot T1 departs most: the root-mean-square departure of its mean SNV
spectrum from the other lots is 1.61 pooled within-lot SDs, against 1.11–1.36 for the others, and the
departure is concentrated between 1180 and 1280 cm<sup>−1</sup>, where T1 absorbs 4.9–8.4 SDs less than the other lots
at 1215, 1248 and 1273 cm<sup>−1</sup> (Fig. 5b). This region holds the C–O stretching of the ester groups of the
triglycerides[@guillen1997] and the amide III band of the proteins.[@barth2007] The MT-DNN, which flagged
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
largest departure at 1709 cm<sup>−1</sup> (+4.1 SDs), the carbonyl band of free fatty acids,[@guillen1997] which
suggests more hydrolysis of its triglycerides; this did not cause false positives for the regression
routes but may explain why PLS-DA rejected half of its scans. These band assignments are offered as
interpretation of an exploratory analysis, not as proof of cause.

The two model families therefore fail for different reasons. PLS is a linear projection, and a lot is
rejected when its spectral difference happens to align with the regression vector, whatever the size of
that difference. The MT-DNN is non-linear and its softmax output is confident wherever the training data
are dense, so a lot is rejected when it is far from all four training lots in any direction, as T1 is.
<!-- results/lot_departure.json: rms_d T1 1.61, others 1.11-1.36; top_bands T1 1215 -8.35, 1273 -5.48, 1248 -4.90; T2 1709 +4.05; pls_adulterant_shift T5 8.92, T1 3.04, T2 0.82, T3 1.51, T4 -12.59; observed MT-DNN T1 authentic_adult_mean 2.65, blend_tahini_bias -6.04 (others -0.53..1.72); PLS-R T5 authentic_adult_mean 10.34. Thresholds: run_info_lolo_chem.json T1 dnnr 0.458-1.241; T5 plsr 6.08. -->

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
<!-- results/metrics.csv lolo scan/sample r2_tahini, rmsep_tahini, identification; results/metrics_lot.csv rmsep_tahini per fold (PLS T5 7.97, MT-DNN T1 6.14; others 2.91-4.35); identification per fold (T4 0.931 PLS, 0.934 MT-DNN). -->

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
<!-- results/consensus.json: per_seed both fp_lots [] for seeds 0-4, missed [[4, peanut, T1]]; PLS-R missed the same. metrics.csv lolo scan sensitivity MT-DNN 0.997, MT-DNN-R 0.993. -->
