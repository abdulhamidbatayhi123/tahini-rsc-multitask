"""Exploratory (added after the lot-out results): how each authentic lot departs from the other four.

For every authentic lot L: d(L) = mean SNV spectrum of L minus the mean of the other four lot means,
divided by the pooled within-lot SD (mean of the five per-lot SDs). Reports the RMS of d over the
752 channels and the six largest |d| bands at least 25 cm-1 apart. Also projects d(L) on the PLS-R
tahini coefficient of the lot-out model that withheld L, to show which departures move the PLS
prediction (refit here with the fold's own k from run_info).
Output: results/lot_departure.json, results/lot_departure.csv (per-channel d for the ESI figure)."""
import json

import numpy as np
import pandas as pd
from sklearn.cross_decomposition import PLSRegression

from common import RESULTS, dump, features, load


def main():
    d = load()
    Z, wn = features(d, "chem")
    info = json.loads((RESULTS / "run_info_lolo_chem.json").read_text())
    kreg = {f["fold"]: f["pls_k_reg"] for f in info["folds"]}
    a = d["tag"] == 0
    lots = sorted(set(d["lot"]))
    M = {L: Z[a & (d["lot"] == L)].mean(0) for L in lots}
    sd = np.mean([Z[a & (d["lot"] == L)].std(0, ddof=1) for L in lots], 0)
    out, cols = {}, {"wavenumber": wn}
    for L in lots:
        dl = (M[L] - np.mean([M[k] for k in lots if k != L], 0)) / sd
        cols[L] = dl
        picked = []
        for i in np.argsort(-np.abs(dl)):
            if all(abs(wn[i] - wn[j]) > 25 for j in picked):
                picked.append(i)
            if len(picked) == 6:
                break
        tr = d["lot"] != L
        pls = PLSRegression(n_components=kreg[L], scale=False).fit(Z[tr], d["y"][tr])
        coef = pls.coef_.reshape(3, -1)[0] if pls.coef_.shape[0] == 3 else pls.coef_[:, 0]
        raw = M[L] - np.mean([M[k] for k in lots if k != L], 0)
        out[L] = dict(rms_d=float(np.sqrt((dl ** 2).mean())),
                      top_bands=[[round(float(wn[i])), round(float(dl[i]), 2)] for i in picked],
                      pls_tahini_shift=float(raw @ coef))
    # pure adulterant pastes (lot T5, 100 %) minus the authentic mean, SNV units, top bands 20 cm-1 apart
    T = Z[a].mean(0)
    for j, nm in ((1, "sunflower100"), (2, "peanut100")):
        m = d["y"][:, j] == 100
        D = Z[m].mean(0) - T
        picked = []
        for i in np.argsort(-np.abs(D)):
            if all(abs(wn[i] - wn[k]) > 20 for k in picked):
                picked.append(i)
            if len(picked) == 8:
                break
        out[nm] = dict(n_scans=int(m.sum()), top_bands=[[round(float(wn[i])), round(float(D[i]), 3)] for i in picked])
        cols[nm] = D
    pd.DataFrame(cols).to_csv(RESULTS / "lot_departure.csv", index=False)
    dump(out, "lot_departure.json")
    for L, v in out.items():
        print(L, v)


if __name__ == "__main__":
    main()
