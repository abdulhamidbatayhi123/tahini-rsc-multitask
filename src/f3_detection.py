"""Fig. 3. Screening on withheld production lots (leave-one-lot-out, chemically informative regions).
(a) Share of the scans of each withheld authentic lot flagged as adulterated (false positives), for the
four decision routes (results/metrics_lot.csv, fp_rate_authentic; MT-DNN routes: mean of five seeds).
(b) Share of blend scans flagged at each nominal adulterant level (4-100 %), pooled over the five withheld
lots; MT-DNN routes averaged over five seeds. Pooled sensitivity with cluster-bootstrap 95 % intervals is
given in the legend (results/metrics.csv)."""
import sys

import numpy as np
import pandas as pd

from common import RESULTS
from figstyle import C, DOUBLE, panel, plt, save

SCHEME = sys.argv[1] if len(sys.argv) > 1 else "lolo"
REG = "chem"
pred_p = RESULTS / f"pred_{SCHEME}_{REG}.csv"
met_p = RESULTS / "metrics.csv"
lot_p = RESULTS / "metrics_lot.csv"
pred = pd.read_csv(pred_p)
met = pd.read_csv(met_p)
met = met[(met.scheme == SCHEME) & (met.regions == REG) & (met.level == "scan")].set_index("model")
lot = pd.read_csv(lot_p)
lot = lot[(lot.scheme == SCHEME) & (lot.regions == REG)]

ROUTES = [("PLS-DA", C["PLS"], "s", "-"), ("PLS-R", C["PLS"], "D", "--"),
          ("MT-DNN", C["MT-DNN"], "o", "-"), ("MT-DNN-R", C["MT-DNN"], "^", "--")]
fig, axs = plt.subplots(1, 2, figsize=(DOUBLE, 6.2 / 2.54), gridspec_kw=dict(width_ratios=[1, 1.6]))

ax = axs[0]
folds = sorted(lot.fold.unique())
names = [r[0] for r in ROUTES]
M = lot.pivot(index="model", columns="fold", values="fp_rate_authentic").loc[names, folds].to_numpy()
ax.imshow(M, cmap="Greys", vmin=0, vmax=1.25, aspect="auto")
for i in range(M.shape[0]):
    for j in range(M.shape[1]):
        v = M[i, j]
        ax.text(j, i, f"{100 * v:.0f}", ha="center", va="center", fontsize=6.5,
                color="#ffffff" if v > 0.6 else "#000000")
ax.set_xticks(range(len(folds)))
ax.set_xticklabels(folds)
ax.set_yticks(range(len(names)))
ax.set_yticklabels(names)
ax.set_xlabel("Withheld authentic lot")
ax.set_title("Authentic scans flagged (%)", fontsize=7)
for s in ax.spines.values():
    s.set_visible(False)
ax.tick_params(length=0)
panel(ax, "a", x=-0.30)

ax = axs[1]
pred["level"] = (100 - pred["y_tahini"]).round().astype(int)
pred = pred[pred.tag == 1]
for m, col, mk, ls in ROUTES:
    d = pred[pred.model == m].groupby(["seed", "level"]).decide.mean().groupby("level").mean()
    r = met.loc[m]
    lab = f"{m} ({r['sensitivity']:.3f}; {r['sensitivity_lo']:.3f}–{r['sensitivity_hi']:.3f})"
    ax.plot(d.index, d.values, color=col, ls=ls, marker=mk, mfc=col if "-R" not in m else "white",
            label=lab, ms=2.8)
ax.set_xlabel("Nominal adulterant fraction (%)")
ax.set_ylabel("Blend scans flagged")
ax.set_ylim(-0.03, 1.05)
ax.set_xlim(0, 102)
ax.legend(loc="lower right", title="Route (sensitivity; 95 % CI)", title_fontsize=6.5)
panel(ax, "b", x=-0.09)
fig.tight_layout(w_pad=1.5)
save(fig, f"fig3_detection_{SCHEME}", __file__, [pred_p, met_p, lot_p])
