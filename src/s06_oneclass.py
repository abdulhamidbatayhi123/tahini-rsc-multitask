"""One-class (PCA T2/Q) baseline under leave-one-lot-out, chem regions.

ADDED AFTER THE MAIN RESULTS, AT REVIEWER REQUEST; EXPLORATORY (not part of DESIGN.md).

Per withheld lot: PCA is fitted on the AUTHENTIC training scans only (4 lots), mean-centred without
autoscaling (as PLS, scale=False), on the same SNV + chem features as s01_run.py. Per scan: Hotelling T2
(sum t_a^2 / var_a) and Q (squared residual). k = smallest number of components explaining >= 99 % of the
authentic training variance (cap 15). Limits come from leave-one-training-lot-out inner CV over the
authentic training scans (GroupKFold over the 4 authentic samples = 4 lots): out-of-fold T2 and Q are
pooled and limit = mean + 3 SD (the paper's rule for the regression routes). A scan is flagged when
T2 > t_lim OR Q > q_lim; a sample is flagged when its mean T2 or mean Q exceeds the limit (mirrors s02).
Variants: 99th-percentile limits; k in {2, 5, 10}; a combined distance T2/mean(T2_oof) + Q/mean(Q_oof)
with a mean + 3 SD limit (DD-SIMCA-like). Deterministic (SVD, no randomness).

Output: results/oneclass.json, results/pred_lolo_chem_oneclass.csv. Run from src/: python s06_oneclass.py"""
import os

for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS", "TORCH_THREADS"):
    os.environ[v] = "2"
import time

import numpy as np
import pandas as pd
from sklearn.model_selection import GroupKFold

import common
from common import RESULTS, dump, features, load, lolo_folds, sha256

common.torch.set_num_threads(2)      # common.py resets torch threads at import; torch is not used here
KMAX, VAR = 15, 0.99


def pca_fit(X, k=None):
    """Mean-centred PCA by SVD. k=None picks the smallest k with cumulative variance >= VAR (cap KMAX)."""
    mu = X.mean(0)
    _, s, Vt = np.linalg.svd(X - mu, full_matrices=False)
    ev = s ** 2 / (len(X) - 1)
    if k is None:
        k = min(int(np.searchsorted(np.cumsum(ev) / ev.sum(), VAR) + 1), KMAX)
    return dict(mu=mu, P=Vt[:k].T, lam=ev[:k], k=k)


def stats(m, X):
    """Hotelling T2 and Q (squared reconstruction residual) per scan."""
    Xc = X - m["mu"]
    T = Xc @ m["P"]
    return (T ** 2 / m["lam"]).sum(1), ((Xc - T @ m["P"].T) ** 2).sum(1)


def limits(X, groups, k):
    """Out-of-fold T2/Q of authentic training scans, leave-one-training-lot-out (GroupKFold over samples)."""
    t2, q = np.zeros(len(X)), np.zeros(len(X))
    for itr, iva in GroupKFold(len(set(groups))).split(X, groups=groups):
        t2[iva], q[iva] = stats(pca_fit(X[itr], k), X[iva])
    c = t2 / t2.mean() + q / q.mean()
    m3 = lambda a: float(a.mean() + 3 * a.std(ddof=1))
    return dict(sd3=dict(t2=m3(t2), q=m3(q)), p99=dict(t2=float(np.percentile(t2, 99)), q=float(np.percentile(q, 99))),
                comb=dict(t0=float(t2.mean()), q0=float(q.mean()), c=m3(c)))


def evaluate(df):
    """df: fold, group, lot, tag, y_tahini, T2, Q, t_lim, q_lim (or C, c_lim) per scan -> metrics dict."""
    comb = "C" in df
    df = df.assign(flag=(df.C > df.c_lim) if comb else (df.T2 > df.t_lim) | (df.Q > df.q_lim)).astype({"flag": int})
    s = df.groupby("group", sort=False).mean(numeric_only=True)
    s["flag"] = (s.C > s.c_lim) if comb else (s.T2 > s.t_lim) | (s.Q > s.q_lim)
    s["lot"] = df.groupby("group", sort=False)["lot"].first()
    per_lot = {L: dict(authentic_scans_flagged=float(d.flag[d.tag == 0].mean()),
                       blend_scans_flagged=float(d.flag[d.tag == 1].mean())) for L, d in df.groupby("lot")}
    a, b = s[s.tag == 0], s[s.tag == 1]
    missed = b[~b.flag]
    return df, dict(per_lot=per_lot,
                    scan=dict(sensitivity=float(df.flag[df.tag == 1].mean()), specificity=float(1 - df.flag[df.tag == 0].mean()),
                              n_blend=int((df.tag == 1).sum()), n_authentic=int((df.tag == 0).sum())),
                    sample=dict(sensitivity=float(b.flag.mean()), specificity=float(1 - a.flag.mean()),
                                n_blend=len(b), n_authentic=len(a),
                                authentic_flagged=sorted(a.index[a.flag].tolist()),
                                missed_blends=[dict(group=g, lot=r.lot, adulterant_pct=float(100 - r.y_tahini))
                                               for g, r in missed.sort_values("y_tahini", ascending=False).iterrows()],
                                missed_levels=sorted(float(100 - v) for v in missed.y_tahini)))


def main():
    t0 = time.time()
    d = load()
    X, _ = features(d, "chem")
    tag, g, lot, yt = d["tag"], d["group"], d["lot"], d["y"][:, 0]
    rows, folds = {}, []
    for L, tr, te in lolo_folds(d):
        au = tr[tag[tr] == 0]
        base = pd.DataFrame(dict(fold=L, group=g[te], lot=lot[te], tag=tag[te], y_tahini=yt[te]))
        main_k = pca_fit(X[au])["k"]
        fi = dict(fold=L, n_authentic_train=len(au), k_main=main_k, limits={})
        for k in sorted({main_k, 2, 5, 10}):
            m = pca_fit(X[au], k)
            t2, q = stats(m, X[te])
            lim = limits(X[au], g[au], k)
            fi["limits"][f"k{k}"] = lim
            t2_tr, q_tr = stats(m, X[au])
            fi["limits"][f"k{k}"]["train_refit_p99"] = dict(t2=float(np.percentile(t2_tr, 99)), q=float(np.percentile(q_tr, 99)))
            tags = (["main"] if k == main_k else []) + ([f"k{k}"] if k in (2, 5, 10) else [])
            for name in tags:
                for rule in ("sd3", "p99"):
                    rows.setdefault(f"{name}_{rule}", []).append(base.assign(k=k, T2=t2, Q=q, t_lim=lim[rule]["t2"], q_lim=lim[rule]["q"]))
                c = lim["comb"]
                rows.setdefault(f"{name}_combined_sd3", []).append(
                    base.assign(k=k, T2=t2, Q=q, C=t2 / c["t0"] + q / c["q0"], c_lim=c["c"]))
        folds.append(fi)
        print(L, "k_main", main_k, flush=True)
    out = dict(note="Added after the main results at reviewer request; exploratory one-class PCA T2/Q baseline.",
               rule="flag if T2 > t_lim OR Q > q_lim (combined: C > c_lim); sample = mean statistic per sample vs limit",
               k_rule=f"smallest k with >= {VAR:.0%} authentic training variance, cap {KMAX}", folds=folds, settings={})
    for name, parts in rows.items():
        df, res = evaluate(pd.concat(parts, ignore_index=True))
        res["k_per_fold"] = df.groupby("fold")["k"].first().astype(int).to_dict()
        out["settings"][name] = res
        if name == "main_sd3":
            df[["fold", "group", "lot", "tag", "y_tahini", "T2", "Q", "flag"]].to_csv(
                RESULTS / "pred_lolo_chem_oneclass.csv", index=False)
    out["runtime_s"] = time.time() - t0
    out["inputs_sha256"] = {"data": sha256(common.DATA_XLSX), "common.py": sha256(common.__file__),
                            "s06_oneclass.py": sha256(__file__)}
    dump(out, "oneclass.json")
    for name, r in out["settings"].items():
        print(f"{name:20s} k={r['k_per_fold']} scan Se={r['scan']['sensitivity']:.3f} Sp={r['scan']['specificity']:.3f} "
              f"| sample Se={r['sample']['sensitivity']:.3f} Sp={r['sample']['specificity']:.3f} missed={r['sample']['missed_levels']}")
    print(f"runtime {out['runtime_s']:.1f} s")


if __name__ == "__main__":
    main()
