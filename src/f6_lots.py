"""Fig. 5. Authentic lots seen as new material (leave-one-lot-out, chemically informative regions).
(a) Predicted adulterant fraction (100 % minus predicted tahini) of the scans of each withheld authentic
lot, PLS-R (black squares) and MT-DNN composition head (purple circles; mean of five seeds per scan),
with each fold's regression-route threshold (PLS-R: one line; MT-DNN-R: range over seeds).
(b) Exploratory: departure of each authentic lot's mean SNV spectrum from the mean of the other four,
in units of the pooled within-lot SD (results/lot_departure.csv, src/s03_lots.py)."""
import json

import numpy as np
import pandas as pd

from common import RESULTS
from figstyle import C, DOUBLE, panel, plt, save

pred_p = RESULTS / "pred_lolo_chem.csv"
info_p = RESULTS / "run_info_lolo_chem.json"
dep_p = RESULTS / "lot_departure.csv"
pred = pd.read_csv(pred_p)
info = {f["fold"]: f for f in json.loads(info_p.read_text())["folds"]}
dep = pd.read_csv(dep_p)
lots = sorted(info)

fig, axs = plt.subplots(1, 2, figsize=(DOUBLE, 6.4 / 2.54), gridspec_kw=dict(width_ratios=[1, 1.45]))
ax = axs[0]
a = pred[pred.tag == 0].copy()
a["pad"] = 100 - a["p_tahini"]
rng = np.random.RandomState(1)
for i, L in enumerate(lots):
    pls = a[(a.model == "PLS-R") & (a.fold == L)]["pad"].to_numpy()
    dnn = a[(a.model == "MT-DNN") & (a.fold == L)].groupby("idx")["pad"].mean().to_numpy()
    ax.plot(i - 0.17 + rng.uniform(-0.07, 0.07, len(pls)), pls, "s", color=C["PLS"], ms=1.6, alpha=0.6, mew=0)
    ax.plot(i + 0.17 + rng.uniform(-0.07, 0.07, len(dnn)), dnn, "o", color=C["MT-DNN"], ms=1.6, alpha=0.6, mew=0)
    ax.hlines(info[L]["plsr_threshold"], i - 0.32, i - 0.02, color=C["PLS"], lw=0.9)
    t = info[L]["dnnr_threshold"]
    ax.fill_between([i + 0.02, i + 0.32], min(t), max(t), color=C["MT-DNN"], alpha=0.35, lw=0)
ax.plot([], [], "s", color=C["PLS"], ms=3, label="PLS-R")
ax.plot([], [], "o", color=C["MT-DNN"], ms=3, label="MT-DNN")
ax.plot([], [], "-", color=C["grey"], lw=0.9, label="Fold threshold")
ax.set_xticks(range(len(lots)))
ax.set_xticklabels([f"{L}" for L in lots])
ax.set_xlabel("Withheld authentic lot")
ax.set_ylabel("Predicted adulterant (%)")
ax.set_ylim(bottom=-0.5)
ax.legend(loc="upper left", handlelength=1.2)
panel(ax, "a")

ax = axs[1]
wn = dep["wavenumber"].to_numpy()
m = (wn >= 900) & (wn <= 1800)
STY = {"T1": ("-", 1.1, "#000000"), "T2": ("--", 0.8, "#555555"), "T3": (":", 0.8, "#555555"),
       "T4": ("-.", 0.8, "#555555"), "T5": ("-", 0.8, "#999999")}
for L in lots:
    ls, lw, col = STY[L]
    ax.plot(wn[m], dep[L].to_numpy()[m], ls=ls, lw=lw, color=col, label=L)
for lo, hi in ((1180, 1280), (1700, 1720)):
    ax.axvspan(lo, hi, color="#DDDDDD", lw=0, zorder=0)
ax.axhline(0, color="#000000", lw=0.4)
ax.set_xlim(1800, 900)
ax.set_xlabel("Wavenumber (cm$^{-1}$)")
ax.set_ylabel("Departure from other lots (pooled SD)")
ax.legend(ncol=5, loc="lower left", handlelength=1.8, columnspacing=1.0)
panel(ax, "b", x=-0.11)
fig.tight_layout()
save(fig, "fig5_lots", __file__, [pred_p, info_p, dep_p])
