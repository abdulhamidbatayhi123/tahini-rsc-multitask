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

Table 2 shows the same models under the three validation designs. A random 80/20 split of the scans
put replicate scans of 54 of the 55 physical samples on both sides, although component selection, early
stopping and the decision thresholds were still chosen by grouped cross-validation inside the training
scans, so only the outer split leaked. On that split the composition was predicted with an RMSEP of
1.79 % tahini by PLS and 2.75 % by the MT-DNN, and every route except PLS-DA accepted every
authentic scan. Withholding whole lots raised the RMSEP to 4.87 and 3.96 % and lowered the specificity of
the same routes to about 80 %, with intervals reaching down to 33–35 %. The random split therefore
makes the quantification error look 1.4–2.7 times smaller and hides the false positives completely, because
every authentic lot is represented in training and the test scans of a lot are near-copies of its
training scans. The grouped hold-out of the earlier study removes the replicate leakage but, with a
single authentic lot in its test set, still cannot reveal the lot effect. The preliminary analysis that
motivated this work used a random split of the scans and reported an AUC of 0.9998; none of the figures from such a split describes how the screen would perform on a new
production lot.
<!-- Table 2: src/t2_leakage.py <- results/metrics.csv (random/holdout/lolo, chem, scan). Random split: s01_run.py train_test_split(test_size=0.2, random_state=42), n_test 311, samples_shared 54 (run_info_random_chem.json); inner selection grouped (s01_run.py comment line 53, common.py MTDNN grouped val, regression thresholds grouped CV). Preliminary AUC 0.9998: originals_preliminary (user's figure). -->

### 3.3 Benchmark: the grouped hold-out

On the grouped hold-out of the earlier study, every route accepted all scans of the authentic test
sample, and every route except PLS-DA flagged every blend scan (Table 1). PLS-DA missed 25 blend scans, with two blend samples
(76 % tahini with sunflower and 84 % tahini with peanut paste) falling on the authentic side.
Quantification was consistent with the published benchmark: PLS gave R<sup>2</sup> 0.997 and RMSEP 1.93 % tahini and the
MT-DNN composition head 0.986 and 3.95 %, against 0.994 for PLS and 0.988 for a regression-only multilayer perceptron in
ref. [#batayhi2026]. This partition is the easy case. Its test set holds one authentic lot and no
blend below 16 % adulterant, so the perfect specificity rests on a single authentic sample. It also
gives a misleading detection limit: the softmax output of the MT-DNN saturates at 0 % adulterant for
the authentic test scans (σ = 0.01 percentage points), which gives an LOD of 0.03 %, whereas PLS, whose
output is not bounded, gave 2.7 %. Neither figure measures what happens with a new lot.
<!-- Table 1: src/t1_table.py <- results/metrics.csv (holdout, chem). PLS-DA misses: groups T1_S24 (76 % tahini) and T4_P16 (84 %) from results/pred_holdout_chem.csv (sample mean score <= 0). LOD holdout: metrics.csv lod/lod_sigma (MT-DNN 0.0330, sigma 0.0098; PLS 2.718). Foods: Table 2 PLS 0.994, MLP 0.988. -->

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
three routes, with 95 % intervals reaching down to 0–33 %. The failures were concentrated in one
lot per model family. The two MT-DNN routes flagged lot T1 (98 % of its scans by the class head and 100 %
by the composition cut-off), PLS-R flagged lot T5 (100 %), and PLS-DA flagged T1 entirely and half of
T2. The remaining lots were accepted almost completely by every route. This pattern, in which the
false positives come from whole lots rather than from scattered scans, was also seen for the six
single-task models of the earlier study, where PLS and the multilayer perceptron flagged T1 and T5 and
other models flagged other lots.[@batayhi2026] It means that the specificity of any of these screens is
set by how far a new authentic lot lies from the calibration lots, not by the scan-to-scan noise that a
hold-out estimate measures.
<!-- sample-level counts: results/consensus.json (PLS-R missed [4, peanut, T1]); results/metrics.csv lolo sample fn: PLS-DA 6, PLS-R 1, MT-DNN 0, MT-DNN-R 0; specificity 0.60/0.80/0.80/0.80. Per-lot FP: results/metrics_lot.csv fp_rate_authentic. PLS-DA k range: results/run_info_lolo_chem.json pls_k_cls 22,4,2,3,3. Level shares: Fig. 3b from pred_lolo_chem.csv. Foods Table 5. -->

The pooled lot-out detection limit was 11.1 % adulterant for PLS (σ = 3.2 percentage points), within
the 10.3–19.5 % reported for the leading models under nested lot-out validation in ref. [#batayhi2026] but
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
replace it here, because each level occurs in one lot only. The MT-DNN routes flagged at least 99 % of
the scans at every level from 4 % upwards, but the 4 % blends belong to lot T1, which the network flags
whatever its composition, so detection at the lowest levels cannot be separated from the lot effect.
PLS-R flagged every level from 20 % upwards in at least 95 % of the scans and missed half of the 4 % scans
and 16 % of the 16 % scans. Excluding the two pure-adulterant samples, which anchor the calibration,
changed neither the sample-level sensitivity (97.9 % for PLS-R, 100 % for both MT-DNN routes, over 48
blends) nor the calibration slopes by more than 0.01 (ESI, Table S8).
<!-- LOD lolo: results/metrics.csv lod 11.076 (sigma 3.155, slope 0.940) PLS; 4.104 (sigma 1.214, slope 0.976) MT-DNN. Foods nested LOLO: KAN 10.3, MLP 17.5, PLS 19.5 % (Section 3.2). results/extra.json (src/s05_extra.py): pls_blank_by_lot T5 mean 10.34, others 2.33-3.98; LOD without T5 in blank 5.16; detection_by_level PLS-R 4 %: 0.50, 16 %: 0.84, >=20 % all 1.0 -> lowest_level_95 20; MT-DNN all >= 0.99; pure_excluded sample sensitivity PLS-R 0.979, MT-DNN 1.0; slopes PLS 0.940->0.937, MT-DNN 0.976->0.986. -->

### 3.5 Why a withheld authentic lot is rejected

The rejected lots are those whose spectra depart from the other four in the directions that each model
reads as adulteration (Fig. 5). Lot T1 departs most: the root-mean-square departure of its mean SNV
spectrum from the other lots is 1.61 pooled within-lot SDs, against 1.11–1.36 for the others, and the
departure is concentrated between 1180 and 1280 cm<sup>−1</sup>, where T1 absorbs 4.9 to 8.35 SDs less than the other lots
at 1215, 1248 and 1273 cm<sup>−1</sup> (Fig. 5b). This region holds the C–O stretching of the triglyceride ester
groups, tabulated near 1238 cm<sup>−1</sup>,[@guillen1997] and the weak amide III band of the proteins,[@barth2007]
so the assignment of the 1215 and 1273 cm<sup>−1</sup> departures is tentative. The MT-DNN, which flagged
T1, predicted 2.9 % adulterant for its authentic scans on average, against a threshold of 0.4–0.8 %
set on the four training lots, for which the softmax output was close to zero (Fig. 5a). The threshold is
low because the composition head saturates: authentic training scans give a predicted adulterant
fraction near 0 % with little spread, so the mean + 3 SD rule places the cut-off within a percentage point of
zero, and a modest shift of a new lot is enough to cross it. In the other four folds, where the
training set included T1, the thresholds were 1.8–5.2 %. The same
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
departs by +4.1 SDs at 1709 cm<sup>−1</sup>, more than any other lot there, the carbonyl band of free fatty
acids,[@ismail1993] which suggests more hydrolysis of its triglycerides; its largest departure, however, is
at 717 cm<sup>−1</sup> (+4.25 SDs), in the CH<sub>2</sub> rocking region whose shape follows the physical state of the fat,
so part of the difference between lots may be physical (temperature, crystallinity) rather than chemical; this did not cause false positives for the regression
routes but may explain why PLS-DA rejected half of its scans. These band assignments are offered as
interpretation of an exploratory analysis, not as proof of cause.

The two model families therefore fail for different reasons. PLS is a linear projection, and a lot is
rejected when its spectral difference happens to align with the regression vector, whatever the size of
that difference. The MT-DNN is non-linear and its softmax output is confident wherever the training data
are dense, so a lot is rejected when it is far from all four training lots in any direction, as T1 is.
<!-- results/lot_departure.json: rms_d T1 1.61, others 1.11-1.36; top_bands T1 1215 -8.35, 1273 -5.48, 1248 -4.90; T2 1709 +4.05; pls_adulterant_shift T5 8.92, T1 3.04, T2 0.82, T3 1.51, T4 -12.59; observed MT-DNN T1 authentic_adult_mean 2.92, blend_tahini_bias -5.27 (others -0.74..3.23); PLS-R T5 authentic_adult_mean 10.34. Thresholds: run_info_lolo_chem.json T1 dnnr 0.400-0.781 (other folds 1.82-5.16); T5 plsr 6.08. -->

### 3.6 Quantification and identification of the adulterant

Both composition outputs transferred to new lots far better than the decisions built on them (Fig. 4).
Over the five withheld lots, PLS gave a scan-level R<sup>2</sup> of 0.979 and RMSEP of 4.87 % tahini and the
MT-DNN 0.986 and 3.96 %, with overlapping intervals (Table 1); at sample level, where averaging removes
replicate scatter but not lot bias, the order reversed (PLS 3.80 %, MT-DNN 4.55 %). The errors of each
model were concentrated in the lot it also misjudged at the screening step: the lot-wise RMSEP was
largest for T5 with PLS (7.97 %) and for T1 with the MT-DNN (5.46 %), and 2.4–4.4 % for every other lot
and model. The adulterant was identified correctly in 97 % of blend scans by both families, with the
lowest lot-wise value 93 % (lot T4) for PLS and 95 % (lot T2) for the MT-DNN. Lot-out quantification is thus about two and a half times as
uncertain as the hold-out suggested for PLS (RMSEP 4.87 against 1.93 %) and about as uncertain for the
MT-DNN (3.96 against 3.95 %); the network loses less when moving to a new lot but starts from a worse
hold-out calibration.
<!-- results/metrics.csv lolo scan/sample r2_tahini, rmsep_tahini, identification; results/metrics_lot.csv rmsep_tahini per fold (PLS T5 7.97, MT-DNN T1 5.46; others 2.36-4.35); identification per fold (PLS T4 0.931; MT-DNN lowest T2 0.951). -->

### 3.7 One network or two models?

The classification head showed no detectable advantage over the network's own composition output. On
withheld lots the class head and the composition cut-off of the MT-DNN reached the same decision for
all 55 samples in every seed, rejected the same lot and detected blends equally well (scan-level
sensitivity 100 % for both; Table 1). In the PLS family the regression route was right where PLS-DA was
wrong for eight samples and the reverse held for two (exact McNemar test, p = 0.11). With five authentic
lots these tests have little power, so the result is absence of evidence for a gain, not evidence of
equivalence; the recommendation that follows rests on parsimony. A dedicated classifier adds a second decision to calibrate and, in the PLS family, a less
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
With five authentic lots this is a hypothesis, not a validated screening rule, and it will fail for a
lot that departs along the PLS vector and from the network's training data at the same time. It does
show that combining a linear and a non-linear calibration is a cheaper way to protect specificity than
an additional classification head, and it should be tested on lots not used here.
<!-- results/extra.json paired: PLS class_right_reg_wrong 2, class_wrong_reg_right 8, p 0.109; MT-DNN 0/0 all seeds. results/consensus.json: per_seed both fp_lots [] for seeds 0-4, missed [[4, peanut, T1]]; PLS-R missed the same. metrics.csv lolo scan sensitivity MT-DNN 1.000, MT-DNN-R 1.000. -->
