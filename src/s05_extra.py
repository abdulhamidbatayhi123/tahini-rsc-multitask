"""Supplementary analyses requested in review (leave-one-lot-out, chemically informative regions).

1. Paired comparison of the two decision routes within each model family on the 55 withheld samples
   (exact McNemar test; MT-DNN per seed).
2. Empirical detection by level (ICH Q2(R2) visual-evaluation approach): share of blend scans flagged at
   each nominal adulterant level and the lowest level from which every level is flagged in >= 95 % of scans.
3. Sensitivity, calibration slope and LOD with and without the two pure-adulterant samples (0 % tahini).
4. LOD of PLS with each authentic lot left out of the blank, and the per-lot mean and SD of the blank.
Output: results/extra.json. Decisions follow s02_metrics.py exactly (scan: column 'decide'; sample: mean
score vs 0 for the class routes and vs the fold threshold for the regression routes)."""
import numpy as np
import pandas as pd
from scipy.stats import binomtest

from common import RESULTS, dump, lod
from s02_metrics import fold_thresholds

pred = pd.read_csv(RESULTS / "pred_lolo_chem.csv")
thr = fold_thresholds("lolo", "chem")
pred["adul_nom"] = 100 - pred["y_tahini"]
pred["adul_pred"] = 100 - pred["p_tahini"]
out = {}


def sample_decisions(model, seed):
    d = pred[(pred.model == model) & (pred.seed == seed)]
    a = d.groupby("group").agg(fold=("fold", "first"), tag=("tag", "first"), score=("score", "mean"),
                               adul_nom=("adul_nom", "first"))
    t = a["fold"].map(lambda f: thr[(model, f, seed)]) if model in ("PLS-R", "MT-DNN-R") else 0.0
    a["flag"] = (a["score"] > t).astype(int)
    a["correct"] = (a["flag"] == a["tag"]).astype(int)
    return a


# 1 paired route comparison
pairs = {"PLS": ("PLS-DA", "PLS-R", [-1]), "MT-DNN": ("MT-DNN", "MT-DNN-R", sorted(pred[pred.model == "MT-DNN"].seed.unique()))}
out["paired"] = {}
for fam, (cls, reg, seeds) in pairs.items():
    res = []
    for s in seeds:
        a, b = sample_decisions(cls, s), sample_decisions(reg, s).loc[sample_decisions(cls, s).index]
        n01 = int(((a.correct == 1) & (b.correct == 0)).sum())   # class route right, regression route wrong
        n10 = int(((a.correct == 0) & (b.correct == 1)).sum())
        p = binomtest(n01, n01 + n10, 0.5).pvalue if n01 + n10 else 1.0
        res.append(dict(seed=int(s), class_right_reg_wrong=n01, class_wrong_reg_right=n10, p_exact=float(p),
                        n_samples=int(len(a))))
    out["paired"][fam] = res

# 2 detection by level (scan level)
lev = {}
for model in ("PLS-DA", "PLS-R", "MT-DNN", "MT-DNN-R"):
    d = pred[(pred.model == model) & (pred.tag == 1)]
    r = d.groupby("adul_nom")["decide"].mean()          # pooled over seeds = mean over seeds (equal scans)
    lev[model] = {float(k): float(v) for k, v in r.items()}
    ok = r >= 0.95
    lowest = None
    for L in sorted(r.index):
        if ok[r.index >= L].all():
            lowest = float(L)
            break
    out.setdefault("lowest_level_95", {})[model] = lowest
out["detection_by_level"] = lev

# 3 with / without pure adulterants
out["pure_excluded"] = {}
for model in ("PLS-R", "MT-DNN"):
    seeds = sorted(pred[pred.model == model].seed.unique())
    rows = []
    for s in seeds:
        d = pred[(pred.model == model) & (pred.seed == s)]
        for lab, dd in (("all", d), ("no_pure", d[d.y_tahini > 0])):
            L, sig, S = lod(dd.adul_pred.to_numpy(), dd.adul_nom.to_numpy(), dd.tag.to_numpy())
            rows.append(dict(seed=int(s), set=lab, lod=L, sigma=sig, slope=S))
    df = pd.DataFrame(rows).groupby("set")[["lod", "sigma", "slope"]].mean()
    out["pure_excluded"][model] = df.to_dict(orient="index")
for model in ("PLS-DA", "PLS-R", "MT-DNN", "MT-DNN-R"):
    seeds = sorted(pred[pred.model == model].seed.unique())
    sens_all, sens_np = [], []
    for s in seeds:
        a = sample_decisions(model, s)
        bl = a[a.tag == 1]
        sens_all.append(bl.flag.mean())
        sens_np.append(bl[bl.adul_nom < 100].flag.mean())
    out["pure_excluded"].setdefault("sample_sensitivity", {})[model] = dict(all=float(np.mean(sens_all)),
                                                                           no_pure=float(np.mean(sens_np)),
                                                                           n_blends_no_pure=int((bl.adul_nom < 100).sum()))

# 4 PLS blank by lot
d = pred[pred.model == "PLS-R"]
au = d[d.tag == 0]
out["pls_blank_by_lot"] = {lot: dict(mean=float(g.adul_pred.mean()), sd=float(g.adul_pred.std(ddof=1)))
                           for lot, g in au.groupby("lot")}
out["pls_lod_leave_lot_out_of_blank"] = {}
for lot in sorted(au.lot.unique()):
    dd = d[~((d.tag == 0) & (d.lot == lot))]
    L, sig, S = lod(dd.adul_pred.to_numpy(), dd.adul_nom.to_numpy(), dd.tag.to_numpy())
    out["pls_lod_leave_lot_out_of_blank"][lot] = dict(lod=L, sigma=sig, slope=S)

dump(out, "extra.json")
import json
print(json.dumps(out, indent=1, default=float)[:6000])
