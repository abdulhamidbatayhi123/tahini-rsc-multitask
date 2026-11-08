"""Fig. 3. Screening on withheld production lots (leave-one-lot-out, chemically informative regions).
(a) Scan-level sensitivity and specificity of the four decision routes, with cluster-bootstrap 95 %
intervals (resampling physical samples). (b) Share of scans flagged as adulterated at each nominal
adulterant level (0 = authentic tahini), pooled over the five withheld lots; MT-DNN routes averaged over
five seeds."""
import sys

import numpy as np
import pandas as pd

from common import RESULTS
from figstyle import C, DOUBLE, panel, plt, save

SCHEME = sys.argv[1] if len(sys.argv) > 1 else "lolo"
REG = "chem"
pred_p = RESULTS / f"pred_{SCHEME}_{REG}.csv"
met_p = RESULTS / "metrics.csv"
pred = pd.read_csv(pred_p)
met = pd.read_csv(met_p)
met = met[(met.scheme == SCHEME) & (met.regions == REG) & (met.level == "scan")].set_index("model")

ROUTES = [("PLS-DA", C["PLS"], "s", "-"), ("PLS-R", C["PLS"], "D", "--"),
          ("MT-DNN", C["MT-DNN"], "o", "-"), ("MT-DNN-R", C["MT-DNN"], "^", "--")]
fig, axs = plt.subplots(1, 2, figsize=(DOUBLE, 6.2 / 2.54), gridspec_kw=dict(width_ratios=[1, 1.9]))
ax = axs[0]
for j, (metric, lab) in enumerate((("sensitivity", "Sensitivity"), ("specificity", "Specificity"))):
    for i, (m, col, mk, _) in enumerate(ROUTES):
        x = j * 5 + i
        r = met.loc[m]
        ax.errorbar(x, r[metric], yerr=[[r[metric] - r[metric + "_lo"]], [r[metric + "_hi"] - r[metric]]],
                    fmt=mk, color=col, mfc=col if "-R" not in m else "white", capsize=1.5, lw=0.7)
ax.set_xticks([1.5, 6.5])
ax.set_xticklabels(["Sensitivity", "Specificity"])
ax.set_xlim(-1, 9)
ax.set_ylim(0, 1.05)
ax.set_ylabel("Proportion of scans")
panel(ax, "a")

ax = axs[1]
pred["level"] = (100 - pred["y_tahini"]).round().astype(int)
for m, col, mk, ls in ROUTES:
    d = pred[pred.model == m].groupby(["seed", "level"]).decide.mean().groupby("level").mean()
    ax.plot(d.index, d.values, color=col, ls=ls, marker=mk, mfc=col if "-R" not in m else "white",
            label=m, ms=2.8)
ax.set_xlabel("Nominal adulterant fraction (%)")
ax.set_ylabel("Share flagged as adulterated")
ax.set_ylim(-0.03, 1.05)
ax.set_xlim(-2, 102)
ax.legend(loc="lower right", ncol=2)
panel(ax, "b", x=-0.09)
fig.tight_layout(w_pad=1.5)
save(fig, f"fig3_detection_{SCHEME}", __file__, [pred_p, met_p])
