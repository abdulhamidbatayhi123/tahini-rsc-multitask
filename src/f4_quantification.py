"""Fig. 4. Quantification on withheld production lots (leave-one-lot-out, chemically informative regions).
Predicted against nominal tahini fraction for (a) PLS and (b) the MT-DNN (mean of five seeds). Points are
physical-sample means of the scan predictions, bars +/- 1 SD over the scans; marker and colour show the
adulterant. Legends give R2 and RMSEP at scan level (from results/metrics.csv)."""
import sys

import numpy as np
import pandas as pd

from common import RESULTS
from figstyle import C, DOUBLE, MK, panel, plt, save

SCHEME = sys.argv[1] if len(sys.argv) > 1 else "lolo"
REG = "chem"
pred_p = RESULTS / f"pred_{SCHEME}_{REG}.csv"
met_p = RESULTS / "metrics.csv"
pred = pd.read_csv(pred_p)
met = pd.read_csv(met_p)
met = met[(met.scheme == SCHEME) & (met.regions == REG) & (met.level == "scan")].set_index("model")

fig, axs = plt.subplots(1, 2, figsize=(DOUBLE, 7.6 / 2.54), sharey=True)
for ax, (model, title, letter) in zip(axs, (("PLS-R", "PLS", "a"), ("MT-DNN", "MT-DNN", "b"))):
    d = pred[pred.model == model].copy()
    d["adulterant"] = np.where(d.y_sunflower > 0, "sunflower", np.where(d.y_peanut > 0, "peanut", "tahini"))
    # average seeds per scan first, then summarise per physical sample
    s = d.groupby(["idx", "group", "adulterant"], as_index=False)[["y_tahini", "p_tahini"]].mean()
    g = s.groupby(["group", "adulterant"]).agg(y=("y_tahini", "mean"), p=("p_tahini", "mean"),
                                                sd=("p_tahini", "std")).reset_index()
    ax.plot([0, 100], [0, 100], color=C["grey"], lw=0.6, ls="--", zorder=0)
    for a, lab in (("tahini", "Authentic tahini"), ("sunflower", "Sunflower paste blends"),
                   ("peanut", "Peanut paste blends")):
        q = g[g.adulterant == a]
        ax.errorbar(q.y, q.p, yerr=q.sd, fmt=MK[a], color=C[a], ms=3.2, capsize=1.2, lw=0.6, label=lab,
                    mfc=C[a] if a != "peanut" else "white")
    r = met.loc[model]
    ax.text(0.04, 0.96, f"{title}\nR$^2$ = {r.r2_tahini:.3f}\nRMSEP = {r.rmsep_tahini:.2f} %",
            transform=ax.transAxes, va="top", fontsize=6.5)
    ax.set_xlabel("Nominal tahini fraction (%)")
    ax.set_xlim(-4, 104)
    ax.set_ylim(-4, 108)
    panel(ax, letter, x=-0.12)
axs[0].set_ylabel("Predicted tahini fraction (%)")
axs[1].legend(loc="lower right")
fig.tight_layout(w_pad=1.2)
save(fig, f"fig4_quantification_{SCHEME}", __file__, [pred_p, met_p])
