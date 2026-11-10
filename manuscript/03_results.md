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
authentic scan. Withholding whole lots raised the RMSEP to 4.87 and 3.95 % and lowered the specificity of
the same routes to about 80 %, with scan-level bootstrap intervals reaching down to 33–35 %. The random split therefore
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
three routes, with exact 95 % intervals reaching down to 15 and 28 % (Table 1). The failures were concentrated in one
lot per model family. The two MT-DNN routes flagged lot T1 (98 % of its scans by the class head and 100 %
by the composition cut-off), PLS-R flagged lot T5 (100 %), and PLS-DA flagged T1 entirely and half of
T2. The remaining lots were accepted almost completely by every route. This pattern, in which the
false positives come from whole lots rather than from scattered scans, was also seen for the six
single-task models of the earlier study, where PLS and the multilayer perceptron flagged T1 and T5 and
other models flagged other lots.[@batayhi2026] It means that the specificity of any of these screens is
set by how far a new authentic lot lies from the calibration lots, not by the scan-to-scan noise that a
hold-out estimate measures.
With the full 600–4000 cm<sup>−1</sup> range as input the same lots were rejected at sample level (T1 by both
MT-DNN routes and PLS-DA, T5 by PLS-R) and every route reached 80 % sample-level specificity, so the lot
effect does not depend on the choice of spectral regions. The scan-level picture did change: PLS-R also
flagged 29 % of the T1 scans, PLS-DA no longer flagged T2 (3 % of its scans), and the lot-out RMSEP rose
to 5.32 % for PLS and 5.73 % for the MT-DNN, with the MT-DNN error on T1 reaching 9.76 % (ESI, Table S7). Two further changes to the input left the
lot-out decisions unchanged (ESI, Table S12): computing SNV over the retained regions only, and cutting the
fingerprint region at 700 cm<sup>−1</sup>, near the low-wavenumber limit of the ZnSe element. In both, the MT-DNN
routes rejected T1, PLS-R rejected T5, sample-level specificity stayed at 80 % for these three routes and the
lot-out RMSEP was 3.62–4.06 % for the MT-DNN and 4.92–5.18 % for PLS. The PLS-DA rejection of half of
the T2 scans was the only fragile result: it disappeared (7 % of scans) when the region below 700 cm<sup>−1</sup>
was removed, as it did with the full range.
<!-- results/metrics.csv lolo chemsnv/chem700 (T-TR4 referee M5/M6): sample spec 0.8 MT-DNN, MT-DNN-R, PLS-R both; PLS-DA 0.6 (chemsnv) / 0.8 (chem700); scan RMSEP MT-DNN 3.621/4.063, PLS 4.923/5.178; metrics_lot fp_rate_authentic PLS-DA T2 0.52 chem/chemsnv, 0.07 chem700. -->
The region choice therefore matters more for the network's quantification of a departing lot than the
pooled error suggests.
<!-- results/metrics.csv regions full lolo: sample specificity 0.8 all routes; scan RMSEP PLS 5.32, MT-DNN 5.73; metrics_lot.csv full fp_rate T1 MT-DNN 1.0, MT-DNN-R 1.0, PLS-DA 1.0, PLS-R T5 1.0 (T1 0.287); PLS-DA T2 0.033; rmsep_tahini T1 MT-DNN 9.76. -->
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
replace it here, because each level occurs in one lot only. The MT-DNN routes flagged at least 98.7 % of
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
departure is concentrated between 1180 and 1280 cm<sup>−1</sup>, where T1 absorbs 4.90 to 8.35 SDs less than the other lots
at 1215, 1248 and 1273 cm<sup>−1</sup> (Fig. 5b). Lots T4 and T5 depart the other way in the same window (+5.40 SDs at
1246 cm<sup>−1</sup> and +4.10 SDs at 1213 cm<sup>−1</sup>), so this region varies between lots in general, and T1 lies at
one end of that variation. This region holds the C–O stretching of the triglyceride ester
groups, tabulated near 1238 cm<sup>−1</sup>,[@guillen1997] and the weak amide III band of the proteins.[@barth2007]
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
output and lowered its sensitivity to 30 %.<!-- results/robust_threshold.json: MT-DNN-R T1 thresholds 0.30–2.01 over
alternative rules and seeds; fp_lots_per_seed T1 x5 for every rule; PLS-R logit sensitivity 0.30 -->
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
departs by +4.05 SDs at 1709 cm<sup>−1</sup>, more than any other lot there, where free fatty acids absorb,[@ismail1993]
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
state of the optical path, and both differed between the authentic lots (one-way ANOVA, p < 10<sup>−100</sup>;
ESI, Table S11): they were low for T1 and T2 and high for T3–T5, with T1 lowest on both. The authentic
lots were therefore not all measured under the same conditions, and in this set the effect of a lot
cannot be separated from that of its measurement session.
<!-- results/session_indicators.json (src/s08_session.py): authentic ANOVA F co2 192.2 p 2.5e-113, water_vapour 400.7 p 2.0e-184; lowest_authentic_lot T1 for both; T1 minus others -2.05 / -2.83 within-lot SD. Referee read T-TR4 M4. -->

The two model families therefore fail for different reasons. PLS is a linear projection, and a lot is
rejected when its spectral difference happens to align with the regression vector, whatever the size of
that difference. The MT-DNN is non-linear and its softmax output is confident wherever the training data
are dense, so a lot is rejected when it is far from all four training lots in any direction, as T1 is.
<!-- results/lot_departure.json: rms_d T1 1.61, others 1.11-1.36; top_bands T1 1215 -8.35, 1273 -5.48, 1248 -4.90; T4 1246 +5.40, T5 1213 +4.10; T2 1709 +4.05; pls_adulterant_shift T5 8.92, T1 3.04, T2 0.82, T3 1.51, T4 -12.59; observed MT-DNN T1 authentic_adult_mean 2.92, blend_tahini_bias -5.27 (others -0.74..3.23); PLS-R T5 authentic_adult_mean 10.34. Thresholds: run_info_lolo_chem.json T1 dnnr 0.400-0.781 (other folds 1.82-5.16); T5 plsr 6.08. -->
<!-- results/derivative_bands.json (src/fS2_derivative.py): sg13 window a minima T1 1161.57/1238.65/1277.93 vs others 1161.59/1238.59/1277.67 (max shift 0.26 cm-1 = 0.13 channel); std_diff_at_section35_bands T1@1215 1.30, @1248 0.62, @1273 1.77, T2@1709 -0.89, T2@717 0.44; max |d| in window a over sg9/13/17: 2.10/1.86/1.82; component_1709 no minimum in any lot, 0 % of scans; window c minimum T2 722.53, others 722.48; lot_departure_600_1800 rms T1 1.10, others 0.65-0.86. Dataset metadata: no acquisition date or temperature. -->

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
<!-- results/metrics.csv lolo scan/sample r2_tahini, rmsep_tahini, identification; results/metrics_lot.csv rmsep_tahini per fold (PLS T5 7.97, MT-DNN T1 5.46; others 2.36-4.35); identification per fold (PLS T4 0.931; MT-DNN lowest T2 0.951). -->

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
With five authentic lots this is a hypothesis, not a validated screening rule, and it will fail for a
lot that departs along the PLS vector and from the network's training data at the same time. It
suggests that combining a linear and a non-linear calibration, which costs no extra model, may protect
specificity where an additional classification head did not, and it should be tested on lots not used here.

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
<!-- results/oneclass.json settings k15_sd3: sample sens 0.82, spec 1.0, missed 4,8,8,12,12,16,20,28,32; T1 authentic scans flagged 0.433; scan spec 0.914; T1 mean T2 100.39 vs limit 103.47 (pred_lolo_chem_oneclass.csv, folds[T1].limits.k15.sd3) = 0.970; k_main 15 in all folds. src/s06_oneclass.py (exploratory, review stage). -->
<!-- results/extra.json paired: PLS class_right_reg_wrong 2, class_wrong_reg_right 8, p 0.109; MT-DNN 0/0 all seeds. results/consensus.json: per_seed both fp_lots [] for seeds 0-4, missed [[4, peanut, T1]]; PLS-R missed the same. metrics.csv lolo scan sensitivity MT-DNN 1.000, MT-DNN-R 1.000. -->
