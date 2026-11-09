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
lie along its regression vector. Hold-out estimates with a single authentic lot, and scan-level random
splits even more so, hide this behaviour completely.

Third, because the two families fail on different lots, combining them is a promising and cheap way
to protect specificity. In this set, requiring both composition routes to agree removed every false
positive at the cost of one 4 % blend; the first part follows by construction once the two families
reject different lots, so only the cost is informative. This rule was found after the results were known and rests on
five authentic lots; it needs testing on new lots, other suppliers and a second instrument before it
can support routine screening. For any such use, the authentic reference set must cover the variation
between lots that the screen will meet,[@esslinger2014] and a positive result should be confirmed by a targeted method.
