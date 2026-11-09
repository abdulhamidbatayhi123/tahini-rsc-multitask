"""Referee point B2 (exploratory, added in revision): robustness of the regression-route decision threshold.

In leave-one-lot-out validation (chemically informative regions) the regression routes flag a sample when its
mean predicted adulterant fraction (100 - predicted tahini %) exceeds a cut-off computed from grouped 5-fold CV
predictions on the authentic TRAINING scans (common.regression_threshold: mean + 3 SD). For the MT-DNN the
softmax head saturates near 0 % adulterant, so this cut-off collapses in some folds. Here the cut-off is
recomputed per lot fold (and per seed for the MT-DNN) with alternative rules and the sample-level decisions are
re-scored:
  orig       mean + 3 SD of scan predictions (must reproduce run_info_lolo_chem.json)
  logit      mean + 3 SD on logit(adulterant fraction), fractions clipped to [1e-4, 1 - 1e-4], back-transformed
  q99, q999  empirical 99th / 99.9th percentile of the scan predictions (numpy linear interpolation)
  sample3sd  mean + 3 SD of the sample-averaged predictions (one authentic sample per training lot, so n = 4)
The grouped-CV predictions inside each training set were not stored by s01_run.py, so they are recomputed here
with exactly the s01 code path (same GroupKFold(5) on sample names, same PLS k from select_pls_k, same MTDNN
seeds). Withheld-lot predictions are taken from results/pred_lolo_chem.csv (not refitted).
Sample = mean of its scans' predicted adulterant fraction (s02_metrics.py / s05_extra.py); MT-DNN pooled
sensitivity/specificity per seed, then mean over the 5 seeds (as s02_metrics.py).

Usage:  python s07_robust_threshold.py [pls|dnn FOLD SEED|all|report]
  pls            recompute PLS CV predictions (cached)
  dnn T1 0       recompute MT-DNN inner-CV predictions for one fold/seed (cached)
  all            everything missing, then report
  report         rules + scoring from the cached CV predictions
Cache: audit/robust_cv/*.csv; outputs results/robust_threshold.json, results/robust_threshold.csv and
results/robust_threshold_cvpred.csv (all grouped-CV predictions used).
Threads: TORCH_THREADS env (default 2), set after importing common (which overrides it). The stored s01 run
effectively used cpu_count // 2 = 6 torch threads (common.py resets the TORCH_THREADS=2 of run_v2.sh at import);
bit-exact reproduction of the MT-DNN thresholds needs TORCH_THREADS=6 (2 threads gives float-level drift that the
early-stopping epoch choice amplifies)."""
import json
import os
import sys
import time

import numpy as np
import pandas as pd
import torch
from sklearn.cross_decomposition import PLSRegression
from sklearn.model_selection import GroupKFold

from common import (MTDNN, RESULTS, ROOT, comp_from_pls, dump, features, load, lolo_folds, regression_threshold,
                    select_pls_k, sha256)

torch.set_num_threads(int(os.environ.get("TORCH_THREADS", 2)))
SEEDS = [0, 1, 2, 3, 4]
CACHE = ROOT / "audit" / "robust_cv"
CACHE.mkdir(parents=True, exist_ok=True)
EPS = 1e-4
RULES = ["orig", "logit", "q99", "q999", "sample3sd"]


def setup():
    d = load()
    X, _ = features(d, "chem")
    return d, X


def cv_frame(fold, model, seed, idx, d, P, extra=None):
    return pd.DataFrame(dict(fold=fold, model=model, seed=seed, idx=idx, group=d["group"][idx], lot=d["lot"][idx],
                             tag=d["tag"][idx], y_tahini=d["y"][idx, 0], p_tahini=P[:, 0], **(extra or {})))


def run_pls():
    d, X = setup()
    y, tag, g = d["y"], d["tag"], d["group"]
    out = []
    for L, tr, te in lolo_folds(d):
        t0 = time.time()
        k, _ = select_pls_k(X[tr], y[tr], g[tr])                  # = PLSPair.kr in s01
        P = np.zeros_like(y[tr])
        for itr, iva in GroupKFold(5).split(X[tr], y[tr], g[tr]):  # = s01.pls_cv_threshold
            m = PLSRegression(n_components=k, scale=False).fit(X[tr][itr], y[tr][itr])
            P[iva] = comp_from_pls(m.predict(X[tr][iva]))
        out.append(cv_frame(L, "PLS-R", -1, tr, d, P, dict(k=k)))
        print("PLS", L, "k", k, "thr", regression_threshold(P, tag[tr]), f"{time.time() - t0:.0f}s", flush=True)
    pd.concat(out).to_csv(CACHE / "pls.csv", index=False)


def run_dnn(fold, seed):
    d, X = setup()
    y, tag, g = d["y"], d["tag"], d["group"]
    (L, tr, te), = [f for f in lolo_folds(d) if f[0] == fold]
    t0 = time.time()
    P = np.zeros_like(y[tr])
    for itr, iva in GroupKFold(5).split(X[tr], y[tr], g[tr]):      # = s01 MT-DNN-R threshold loop
        mi = MTDNN(seed=seed).fit(X[tr][itr], y[tr][itr], tag[tr][itr], g[tr][itr])
        P[iva] = mi.predict(X[tr][iva])["comp"]
    cv_frame(L, "MT-DNN-R", seed, tr, d, P).to_csv(CACHE / f"dnn_{L}_s{seed}.csv", index=False)
    print("DNN", L, seed, "thr", regression_threshold(P, tag[tr]), f"{time.time() - t0:.0f}s wall",
          "threads", torch.get_num_threads(), flush=True)


# ------------------------------------------------------------------------------------------ rules
def thresholds(cv):
    """cv: CV predictions of one training set (all scans). Returns dict rule -> threshold (% adulterant)."""
    au = cv[cv.tag == 0]
    a = (100 - au["p_tahini"]).to_numpy()
    z = np.clip(a / 100, EPS, 1 - EPS)
    z = np.log(z / (1 - z))
    zt = z.mean() + 3 * z.std(ddof=1)
    s = au.assign(a=a).groupby("group")["a"].mean().to_numpy()
    return dict(orig=float(regression_threshold(cv[["p_tahini"]].to_numpy(), cv["tag"].to_numpy())),
                logit=float(100 / (1 + np.exp(-zt))), q99=float(np.percentile(a, 99)),
                q999=float(np.percentile(a, 99.9)), sample3sd=float(s.mean() + 3 * s.std(ddof=1)),
                n_auth_scans=int(len(a)), n_auth_samples=int(len(s)), n_auth_scans_clipped_low=int((a / 100 < EPS).sum()))


def score_fold(test, thr):
    """test: withheld-lot predictions of one model/seed (score = predicted adulterant %)."""
    au = test[test.tag == 0]
    smp = test.groupby("group").agg(tag=("tag", "first"), a=("score", "mean"))
    bl = smp[smp.tag == 1]
    ausmp = smp[smp.tag == 0]
    assert len(ausmp) == 1 and len(bl) == 10
    return dict(threshold=thr, auth_scans_flagged_share=float((au.score > thr).mean()),
                auth_sample_mean_pred=float(ausmp.a.iloc[0]), auth_sample_flagged=int(ausmp.a.iloc[0] > thr),
                blends_flagged=int((bl.a > thr).sum()), n_blends=int(len(bl)))


def report():
    pred = pd.read_csv(RESULTS / "pred_lolo_chem.csv")
    info = json.loads((RESULTS / "run_info_lolo_chem.json").read_text())
    stored = {f["fold"]: f for f in info["folds"]}
    folds = sorted(stored)
    cv = [pd.read_csv(CACHE / "pls.csv")]
    missing = []
    for L in folds:
        for s in SEEDS:
            p = CACHE / f"dnn_{L}_s{s}.csv"
            (cv.append(pd.read_csv(p)) if p.exists() else missing.append(f"{L}_s{s}"))
    cv = pd.concat(cv)
    out = dict(description=__doc__.split("Usage:")[0].strip(), missing_dnn_cv=missing, checks={}, per_fold=[],
               pooled={})

    # ---- check 0: stored decisions / sample metrics reproduce from stored thresholds
    chk = out["checks"]
    met = pd.read_csv(RESULTS / "metrics.csv")
    extra = json.loads((RESULTS / "extra.json").read_text())
    for model in ("PLS-R", "MT-DNN-R"):
        dm = pred[pred.model == model]
        st = dm.apply(lambda r: stored[r.fold]["plsr_threshold"] if model == "PLS-R"
                      else stored[r.fold]["dnnr_threshold"][r.seed], axis=1)
        chk[f"{model}_scan_decide_equals_score_gt_stored_thr"] = bool(((dm.score > st).astype(int) == dm.decide).all())
        chk[f"{model}_score_equals_100_minus_p_tahini_maxabs"] = float((dm.score - (100 - dm.p_tahini)).abs().max())

    # ---- per fold x model x seed
    rows = []
    for L in folds:
        for model, seeds in (("PLS-R", [-1]), ("MT-DNN-R", SEEDS)):
            for s in seeds:
                c = cv[(cv.fold == L) & (cv.model == model) & (cv.seed == s)]
                test = pred[(pred.fold == L) & (pred.model == model) & (pred.seed == s)]
                st = stored[L]["plsr_threshold"] if model == "PLS-R" else stored[L]["dnnr_threshold"][s]
                base = dict(fold=L, model=model, seed=s)
                rows.append(dict(base, rule="stored", **score_fold(test, st)))
                if len(c) == 0:
                    continue
                if model == "PLS-R":
                    chk.setdefault("PLS_k_reg_equal_stored", {})[L] = bool(int(c.k.iloc[0]) == stored[L]["pls_k_reg"])
                T = thresholds(c)
                chk.setdefault(f"{model}_orig_threshold_recomputed_minus_stored", {})[f"{L}_s{s}"] = T["orig"] - st
                for r in RULES:
                    rows.append(dict(base, rule=r, n_auth_scans=T["n_auth_scans"], n_auth_samples=T["n_auth_samples"],
                                     n_auth_scans_clipped_low=T["n_auth_scans_clipped_low"], **score_fold(test, T[r])))
    df = pd.DataFrame(rows)
    out["per_fold"] = df.to_dict(orient="records")

    # ---- pooled sample-level sensitivity (50 blends) / specificity (5 lots); MT-DNN per seed then mean
    pooled = []
    for (model, rule), g in df.groupby(["model", "rule"], sort=False):
        per_seed = []
        for s, gs in g.groupby("seed"):
            if gs.fold.nunique() != len(folds):
                continue
            per_seed.append(dict(seed=int(s), sensitivity=gs.blends_flagged.sum() / gs.n_blends.sum(),
                                 specificity=1 - gs.auth_sample_flagged.sum() / len(gs),
                                 fp_lots=",".join(gs.fold[gs.auth_sample_flagged == 1]),
                                 auth_scan_fp_share=float(gs.auth_scans_flagged_share.mean())))
        if not per_seed:
            continue
        P = pd.DataFrame(per_seed)
        pooled.append(dict(model=model, rule=rule, n_seeds=len(P), sensitivity=float(P.sensitivity.mean()),
                           sensitivity_min=float(P.sensitivity.min()), sensitivity_max=float(P.sensitivity.max()),
                           specificity=float(P.specificity.mean()), specificity_min=float(P.specificity.min()),
                           specificity_max=float(P.specificity.max()),
                           auth_scan_fp_share_mean=float(P.auth_scan_fp_share.mean()),
                           fp_lots_per_seed=P.fp_lots.tolist()))
    pooled = pd.DataFrame(pooled)
    out["pooled"] = pooled.to_dict(orient="records")

    # ---- check: stored-threshold pooled sample metrics equal metrics.csv and extra.json
    for model in ("PLS-R", "MT-DNN-R"):
        m = met[(met.scheme == "lolo") & (met.regions == "chem") & (met.model == model) & (met.level == "sample")].iloc[0]
        p = pooled[(pooled.model == model) & (pooled.rule == "stored")].iloc[0]
        chk[f"{model}_stored_sample_sens_spec_vs_metrics_csv"] = dict(
            here=[p.sensitivity, p.specificity], metrics_csv=[float(m.sensitivity), float(m.specificity)],
            extra_json_sens=extra["pure_excluded"]["sample_sensitivity"][model]["all"],
            equal=bool(np.isclose(p.sensitivity, m.sensitivity) and np.isclose(p.specificity, m.specificity)
                       and np.isclose(p.sensitivity, extra["pure_excluded"]["sample_sensitivity"][model]["all"])))
    # per-lot scan false-positive rate with stored thresholds vs metrics_lot.csv (mean over seeds)
    ml = pd.read_csv(RESULTS / "metrics_lot.csv")
    ml = ml[(ml.scheme == "lolo") & (ml.regions == "chem")]
    for model in ("PLS-R", "MT-DNN-R"):
        here = df[(df.model == model) & (df.rule == "stored")].groupby("fold").auth_scans_flagged_share.mean()
        ref = ml[ml.model == model].set_index("fold").fp_rate_authentic
        chk[f"{model}_stored_auth_scan_fp_rate_maxabs_vs_metrics_lot"] = float((here - ref.loc[here.index]).abs().max())
    for k in [k for k in chk if k.endswith("recomputed_minus_stored")]:
        v = np.abs(list(chk[k].values()))
        chk[k + "_maxabs"] = float(v.max())

    out["inputs_sha256"] = {n: sha256(RESULTS / n) for n in ("pred_lolo_chem.csv", "run_info_lolo_chem.json")}
    out["inputs_sha256"]["common.py"] = sha256(ROOT / "src" / "common.py")
    out["inputs_sha256"]["s07_robust_threshold.py"] = sha256(__file__)
    out["torch_threads"] = torch.get_num_threads()
    dump(out, "robust_threshold.json")
    df.to_csv(RESULTS / "robust_threshold.csv", index=False)
    cv.to_csv(RESULTS / "robust_threshold_cvpred.csv", index=False)
    with pd.option_context("display.width", 200, "display.max_columns", 20):
        print(json.dumps(chk, indent=1, default=float))
        print(pooled.drop(columns=["fp_lots_per_seed"]))


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "all"
    if cmd == "pls":
        run_pls()
    elif cmd == "dnn":
        run_dnn(sys.argv[2], int(sys.argv[3]))
    elif cmd == "report":
        report()
    elif cmd == "all":
        if not (CACHE / "pls.csv").exists():
            run_pls()
        for L in ["T1", "T2", "T3", "T4", "T5"]:
            for s in SEEDS:
                if not (CACHE / f"dnn_{L}_s{s}.csv").exists():
                    run_dnn(L, s)
        report()
