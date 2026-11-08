"""Metrics, cluster-bootstrap intervals, per-lot results and LOD from the saved predictions.

Output: results/metrics.csv (one row per scheme x regions x model x level), results/metrics_lot.csv,
results/metrics.json (with input hashes)."""
import sys

import numpy as np
import pandas as pd

from common import COMP, RESULTS, cluster_bootstrap, dump, lod, sample_level, scores, sha256

MODELS = ["PLS-DA", "PLS-R", "MT-DNN", "MT-DNN-R"]
KEYS = ["sensitivity", "specificity", "balanced_accuracy", "auc", "r2_tahini", "rmsep_tahini", "mae_tahini",
        "rmsep_sunflower", "rmsep_peanut", "identification", "fp", "fn", "tp", "tn"]
NBOOT = int(sys.argv[1]) if len(sys.argv) > 1 else 1000


def arrays(df):
    y = df[["y_" + c for c in COMP]].to_numpy()
    p = df[["p_" + c for c in COMP]].to_numpy()
    return y, df["tag"].to_numpy(), df["group"].to_numpy(), p, df["decide"].to_numpy(), df["score"].to_numpy()


def metric_fn(df, level, thr):
    """Return f(sub_df) -> metrics at scan or sample level. thr: decision threshold on score for sample level."""
    def f(sub):
        y, tag, g, p, dec, sc = arrays(sub)
        if level == "sample":
            # regression routes carry the fold's threshold per scan ("thr"); the decision compares the
            # sample's mean predicted adulterant with it, while the AUC uses the raw mean score
            t_s = sub["thr"].groupby(sub["group"].to_numpy(), sort=False).mean().to_numpy() if "thr" in sub else thr
            _, y, tag, p, sc = sample_level(g, y, tag, p, sc)
            dec = (sc > t_s).astype(int)
            g = None
        return scores(y, tag, g, p, dec, sc)
    return f


def fold_thresholds(scheme, regions):
    """Per-fold decision thresholds of the regression routes, from run_info (PLS-R; MT-DNN-R per seed)."""
    import json
    info = json.loads((RESULTS / f"run_info_{scheme}_{regions}.json").read_text())
    t = {}
    for f in info["folds"]:
        t[("PLS-R", f["fold"], -1)] = f["plsr_threshold"]
        for s, v in enumerate(f.get("dnnr_threshold", [])):
            t[("MT-DNN-R", f["fold"], s)] = v
    return t


def run_one(scheme, regions):
    pred = pd.read_csv(RESULTS / f"pred_{scheme}_{regions}.csv")
    thr = fold_thresholds(scheme, regions)
    rows, lots = [], []
    for model in MODELS:
        dm = pred[pred.model == model]
        seeds = sorted(dm.seed.unique())
        for level in ("scan", "sample"):
            per_seed = []
            for s in seeds:
                d = dm[dm.seed == s].copy()
                if model in ("PLS-R", "MT-DNN-R") and level == "sample":
                    # sample decision: mean predicted adulterant fraction vs the fold's own threshold
                    d["thr"] = d["fold"].map(lambda f: thr[(model, f, s)])
                f = metric_fn(d, level, 0.0)
                per_seed.append((d, f))
            point = pd.DataFrame([f(d) for d, f in per_seed])

            def boot_stat(idx_df_list):
                return pd.DataFrame([f(dd) for dd, (_, f) in zip(idx_df_list, per_seed)]).mean().to_dict()

            # cluster bootstrap over physical samples (same draw for every seed)
            base = per_seed[0][0]
            groups = base["group"].to_numpy()
            rng = np.random.RandomState(0)
            ug = np.unique(groups)
            draws = []
            POS = [{u: np.where(d["group"].to_numpy() == u)[0] for u in ug} for d, _ in per_seed]
            for _ in range(NBOOT):
                pick = rng.choice(ug, len(ug), replace=True)
                subs = []
                for (d, _), pos in zip(per_seed, POS):
                    # each drawn copy of a sample gets its own label, so duplicates stay separate samples
                    sub = d.iloc[np.concatenate([pos[u] for u in pick])].copy()
                    sub["group"] = np.concatenate([[f"{u}#{k}"] * len(pos[u]) for k, u in enumerate(pick)])
                    subs.append(sub)
                try:
                    draws.append(boot_stat(subs))
                except ValueError:
                    pass
            B = pd.DataFrame(draws)
            row = dict(scheme=scheme, regions=regions, model=model, level=level, n_seeds=len(seeds),
                       n_boot=len(B))
            for k in KEYS:
                row[k] = point[k].mean()
                row[k + "_seed_min"], row[k + "_seed_max"] = point[k].min(), point[k].max()
                if k in B:
                    row[k + "_lo"], row[k + "_hi"] = np.nanpercentile(B[k], [2.5, 97.5])
            rows.append(row)
        # LOD (scan level, pooled out-of-sample predictions; mean over seeds)
        L = []
        for s in seeds:
            d = dm[dm.seed == s]
            pa = 100 - d["p_tahini"].to_numpy()
            na = 100 - d["y_tahini"].to_numpy()
            L.append(lod(pa, na, d["tag"].to_numpy()))
        rows[-1]["lod"] = float(np.mean([l[0] for l in L]))
        rows[-1]["lod_sigma"] = float(np.mean([l[1] for l in L]))
        rows[-1]["lod_slope"] = float(np.mean([l[2] for l in L]))
        # per fold (lot) metrics
        for fold, dfold in dm.groupby("fold"):
            res = []
            for s in seeds:
                d = dfold[dfold.seed == s]
                y, tag, g, p, dec, sc = arrays(d)
                r = scores(y, tag, g, p, dec, sc)
                r["fp_rate_authentic"] = float(dec[tag == 0].mean()) if (tag == 0).any() else np.nan
                r["fn_rate_blends"] = float(1 - dec[tag == 1].mean()) if (tag == 1).any() else np.nan
                res.append(r)
            R = pd.DataFrame(res).mean().to_dict()
            lots.append(dict(scheme=scheme, regions=regions, model=model, fold=fold, **R))
    return rows, lots


ONLY = set(sys.argv[2].split(",")) if len(sys.argv) > 2 else None    # e.g. random_chem,holdout_full


def main():
    allrows, alllots, hashes = [], [], {}
    if ONLY:   # update only these configurations; keep the other rows of the existing files
        old = pd.read_csv(RESULTS / "metrics.csv")
        oldl = pd.read_csv(RESULTS / "metrics_lot.csv")
        keep = ~(old.scheme + "_" + old.regions).isin(ONLY)
        keepl = ~(oldl.scheme + "_" + oldl.regions).isin(ONLY)
        allrows, alllots = old[keep].to_dict("records"), oldl[keepl].to_dict("records")
        import json
        hashes = json.loads((RESULTS / "metrics_info.json").read_text()).get("inputs_sha256", {})
    for scheme in ("random", "holdout", "lolo"):
        for regions in ("chem", "full"):
            p = RESULTS / f"pred_{scheme}_{regions}.csv"
            if not p.exists() or (ONLY and f"{scheme}_{regions}" not in ONLY):
                continue
            hashes[p.name] = sha256(p)
            r, l = run_one(scheme, regions)
            allrows += r
            alllots += l
            print("done", scheme, regions, flush=True)
    pd.DataFrame(allrows).to_csv(RESULTS / "metrics.csv", index=False)
    pd.DataFrame(alllots).to_csv(RESULTS / "metrics_lot.csv", index=False)
    hashes["s02_metrics.py"] = sha256(__file__)
    dump(dict(n_boot=NBOOT, inputs_sha256=hashes), "metrics_info.json")


if __name__ == "__main__":
    main()
