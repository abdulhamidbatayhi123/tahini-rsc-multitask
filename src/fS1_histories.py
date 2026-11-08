"""Fig. S1. MT-DNN training histories in leave-one-lot-out validation (chemically informative regions).
For each withheld lot, the inner-validation binary cross-entropy of the class head (a) and the mean
squared error of the composition head on fractions scaled to 0-1 (b), median over five seeds; dots mark
the epoch restored by early stopping for each seed (results/hist_lolo_chem_*.csv, run_info)."""
import json

import numpy as np
import pandas as pd

from common import RESULTS
from figstyle import DOUBLE, panel, plt, save

files = sorted(RESULTS.glob("hist_lolo_chem_*.csv"))
h = pd.concat([pd.read_csv(f) for f in files])
info_p = RESULTS / "run_info_lolo_chem.json"
best = {f["fold"]: f["dnn_best_epoch"] for f in json.loads(info_p.read_text())["folds"]}
STY = {"T1": ("-", "#000000"), "T2": ("--", "#555555"), "T3": (":", "#555555"), "T4": ("-.", "#555555"),
       "T5": ("-", "#999999")}
fig, axs = plt.subplots(1, 2, figsize=(DOUBLE, 6.0 / 2.54))
for ax, col, lab, letter in ((axs[0], "val_bce", "Validation BCE, class head", "a"),
                             (axs[1], "val_mse", "Validation MSE, composition head", "b")):
    for fold, d in h.groupby("fold"):
        med = d.groupby("epoch")[col].median()
        ls, c = STY[fold]
        ax.plot(med.index, med.values, ls=ls, color=c, lw=0.9, label=fold)
        for s, e in enumerate(best[fold]):
            v = d[(d.seed == s) & (d.epoch == e)][col]
            if len(v):
                ax.plot(e, v.iloc[0], "o", color=c, ms=2.2)
    ax.set_yscale("log")
    ax.set_xlabel("Epoch")
    ax.set_ylabel(lab)
    panel(ax, letter)
axs[0].legend(ncol=2, loc="upper right", handlelength=1.8, columnspacing=0.8)
fig.tight_layout()
save(fig, "figS1_histories", __file__, files + [info_p])
