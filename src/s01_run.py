"""Run every model under every validation scheme and save scan-level out-of-sample predictions.

Schemes: random (scan-level 80/20, leakage contrast), holdout (Foods grouped 70/30), lolo (5 folds).
Regions: chem (primary), full (sensitivity). Models: PLS pair, MT-DNN (5 seeds).
Output: results/pred_<scheme>_<regions>.csv and results/run_info_<scheme>_<regions>.json."""
import sys
import time

import numpy as np
import pandas as pd
from sklearn.cross_decomposition import PLSRegression
from sklearn.model_selection import GroupKFold, train_test_split

from common import (COMP, MTDNN, RESULTS, PLSPair, comp_from_pls, dump, features, load, lolo_folds,
                    primary_split, regression_threshold, sha256)

SEEDS = [0, 1, 2, 3, 4]


def splits(d, scheme):
    n = len(d["tag"])
    if scheme == "random":
        tr, te = train_test_split(np.arange(n), test_size=0.2, random_state=42)
        return [("random", tr, te)]
    if scheme == "holdout":
        tr, te = primary_split(d)
        return [("holdout", tr, te)]
    return lolo_folds(d)


def pls_cv_threshold(X, y, tag, groups, k):
    """Grouped 5-fold CV predictions inside training -> mean + 3 SD threshold on authentic scans."""
    P = np.zeros_like(y)
    for tr, va in GroupKFold(5).split(X, y, groups):
        m = PLSRegression(n_components=k, scale=False).fit(X[tr], y[tr])
        P[va] = comp_from_pls(m.predict(X[va]))
    return regression_threshold(P, tag)


def main(scheme, regions, only_fold=None):
    d = load()
    X, wn = features(d, regions)
    y, tag, g = d["y"], d["tag"], d["group"]
    rows, info = [], dict(scheme=scheme, regions=regions, n_features=int(X.shape[1]),
                          wn_min=float(wn.min()), wn_max=float(wn.max()), folds=[])
    for name, tr, te in splits(d, scheme):
        if only_fold and name != only_fold:
            continue
        t0 = time.process_time()
        shared = len(set(g[tr]) & set(g[te]))
        fi = dict(fold=name, n_train=len(tr), n_test=len(te), samples_test=len(set(g[te])),
                  samples_shared=shared)
        base = dict(fold=name, idx=te, group=g[te], lot=d["lot"][te], tag=tag[te],
                    y_tahini=y[te, 0], y_sunflower=y[te, 1], y_peanut=y[te, 2])
        # PLS pair (grouped CV for component selection; with the random scheme the CV is grouped too)
        pp = PLSPair().fit(X[tr], y[tr], tag[tr], g[tr])
        o = pp.predict(X[te])
        thr = pls_cv_threshold(X[tr], y[tr], tag[tr], g[tr], pp.kr)
        fi.update(pls_k_reg=pp.kr, pls_k_cls=pp.kc, plsr_threshold=float(thr))
        adul = 100 - o["comp"][:, 0]
        for model, dec, sc in (("PLS-DA", o["decide"], o["score"]), ("PLS-R", (adul > thr).astype(int), adul)):
            rows.append(pd.DataFrame({**base, "model": model, "seed": -1, "decide": dec, "score": sc,
                                      **{f"p_{c}": o["comp"][:, j] for j, c in enumerate(COMP)}}))
        # MT-DNN
        fi["dnn_best_epoch"], fi["dnnr_threshold"] = [], []
        for s in SEEDS:
            m = MTDNN(seed=s).fit(X[tr], y[tr], tag[tr], g[tr])
            o = m.predict(X[te])
            fi["dnn_best_epoch"].append(int(m.best_epoch))
            m.history.assign(fold=name, seed=s).to_csv(RESULTS / f"hist_{scheme}_{regions}_{name}_s{s}.csv", index=False)
            comp_cols = {f"p_{c}": o["comp"][:, j] for j, c in enumerate(COMP)}
            rows.append(pd.DataFrame({**base, "model": "MT-DNN", "seed": s, "decide": o["decide"], "score": o["score"],
                                      "prob": o["prob"], **comp_cols}))
            # regression route: threshold from grouped 5-fold CV inside training (same rule as PLS-R)
            P = np.zeros_like(y[tr])
            for itr, iva in GroupKFold(5).split(X[tr], y[tr], g[tr]):
                mi = MTDNN(seed=s).fit(X[tr][itr], y[tr][itr], tag[tr][itr], g[tr][itr])
                P[iva] = mi.predict(X[tr][iva])["comp"]
            thr_d = regression_threshold(P, tag[tr])
            fi["dnnr_threshold"].append(float(thr_d))
            adul_d = 100 - o["comp"][:, 0]
            rows.append(pd.DataFrame({**base, "model": "MT-DNN-R", "seed": s, "decide": (adul_d > thr_d).astype(int),
                                      "score": adul_d, **comp_cols}))
        fi["cpu_s"] = time.process_time() - t0
        info["folds"].append(fi)
        print(scheme, regions, fi, flush=True)
    info["inputs_sha256"] = {"data": sha256(__import__("common").DATA_XLSX), "common.py": sha256(__file__.replace("s01_run.py", "common.py")),
                             "s01_run.py": sha256(__file__)}
    part = f"_{only_fold}.part" if only_fold else ""
    pd.concat(rows).to_csv(RESULTS / f"pred_{scheme}_{regions}{part}.csv", index=False)
    dump(info, f"run_info_{scheme}_{regions}{part}.json")


def merge(scheme, regions):
    """Combine per-fold parts (python s01_run.py lolo chem T1 ... T5) into the standard files."""
    import json
    folds = [f for f, _, _ in lolo_folds(load())]
    parts = [RESULTS / f"pred_{scheme}_{regions}_{f}.part.csv" for f in folds]
    infos = [json.loads((RESULTS / f"run_info_{scheme}_{regions}_{f}.part.json").read_text()) for f in folds]
    assert all(p.exists() for p in parts)
    assert len({json.dumps(i["inputs_sha256"], sort_keys=True) for i in infos}) == 1, "parts ran on different code"
    pd.concat([pd.read_csv(p) for p in parts]).to_csv(RESULTS / f"pred_{scheme}_{regions}.csv", index=False)
    info = {k: v for k, v in infos[0].items() if k != "folds"}
    info["folds"] = [i["folds"][0] for i in infos]
    dump(info, f"run_info_{scheme}_{regions}.json")
    print("merged", scheme, regions, len(parts), "folds")


if __name__ == "__main__":
    if sys.argv[1] == "merge":
        merge(sys.argv[2], sys.argv[3])
    else:
        main(sys.argv[1], sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else None)
