"""Optical-path indicators by lot (referee read T-TR4, 2026-11-10).

The released data carry no acquisition dates. Bands that the sample does not produce record the state of the
optical path at the time of measurement: the atmospheric CO2 band (2340-2370 cm-1, against its flanks) and the
water-vapour rotation lines (3600-3900 cm-1, SD of the first difference). If these differ between lots, and the
blends of a lot share the value of their own authentic lot, lots were probably measured in separate sessions and
lot cannot be separated from measurement session.

Output: results/session_indicators.json
"""
import numpy as np
from scipy import stats

from common import dump, load

d = load()
X, wn, g, lot, tag = d["X"], d["wn"], d["group"], d["lot"], d["tag"]


def band(lo, hi):
    return (wn >= lo) & (wn <= hi)


ind = {
    "co2": X[:, band(2340, 2370)].mean(1)
    - 0.5 * (X[:, band(2240, 2260)].mean(1) + X[:, band(2400, 2420)].mean(1)),
    "water_vapour": np.std(np.diff(X[:, band(3600, 3900)], axis=1), axis=1),
}
lots = sorted(set(lot))
out = dict(description=__doc__.strip().splitlines()[0], lots=lots, indicators={})
for name, v in ind.items():
    au = tag == 0
    F, p = stats.f_oneway(*[v[au & (lot == L)] for L in lots])
    samples = sorted(set(g[tag == 1]))
    smean = {s: float(v[g == s].mean()) for s in samples}
    blend_by_lot = {L: [smean[s] for s in samples if s.split("_")[0] == L] for L in lots}
    Fb, pb = stats.f_oneway(*blend_by_lot.values())
    auth_mean = {L: float(v[au & (lot == L)].mean()) for L in lots}
    auth_sd = {L: float(v[au & (lot == L)].std(ddof=1)) for L in lots}
    blend_mean = {L: float(np.mean(blend_by_lot[L])) for L in lots}
    # rank of each lot's blends among all lots (is the lowest authentic lot also the lowest blend group?)
    out["indicators"][name] = dict(
        authentic_scan_anova_F=float(F), authentic_scan_anova_p=float(p),
        blend_sample_means_by_lot_anova_F=float(Fb), blend_sample_means_by_lot_anova_p=float(pb),
        authentic_mean=auth_mean, authentic_sd=auth_sd, blend_mean=blend_mean,
        lowest_authentic_lot=str(min(auth_mean, key=auth_mean.get)), lowest_blend_lot=str(min(blend_mean, key=blend_mean.get)),
        spearman_authentic_vs_blend_lot_means=float(stats.spearmanr([auth_mean[L] for L in lots],
                                                                      [blend_mean[L] for L in lots])[0]),
    )
    # T1 authentic relative to the other four lots, in pooled within-lot SDs
    others = [L for L in lots if L != "T1"]
    sd_pool = float(np.sqrt(np.mean([auth_sd[L] ** 2 for L in lots])))
    out["indicators"][name]["T1_minus_others_in_within_lot_sd"] = float(
        (auth_mean["T1"] - np.mean([auth_mean[L] for L in others])) / sd_pool)
dump(out, "session_indicators.json")
for k, v in out["indicators"].items():
    print(k, {kk: (round(vv, 4) if isinstance(vv, float) else vv) for kk, vv in v.items()
              if not isinstance(vv, dict)})
