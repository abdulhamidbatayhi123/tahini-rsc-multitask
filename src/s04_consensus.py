"""Exploratory (added after the lot-out results, not in DESIGN.md): sample-level agreement rule.

A physical sample is flagged when BOTH regression routes flag it: PLS-R (mean predicted adulterant of its
scans > the fold's PLS-R threshold) AND MT-DNN-R (same, per seed, fold threshold of that seed).
Reported per seed with the lots of any false positive and the nominal levels of missed blends; compared
with each route alone. Leave-one-lot-out, chemically informative regions.
Output: results/consensus.json (sensitivity variants: python s04_consensus.py chemsnv|chem700 -> consensus_<regions>.json)."""
import json
import sys

import pandas as pd

from common import RESULTS, dump


def main(regions="chem"):
    p = pd.read_csv(RESULTS / f"pred_lolo_{regions}.csv")
    info = {f["fold"]: f for f in json.loads((RESULTS / f"run_info_lolo_{regions}.json").read_text())["folds"]}
    p["adult_pred"] = 100 - p["p_tahini"]
    s = (p[p.model.isin(["PLS-R", "MT-DNN-R"])]
         .groupby(["model", "seed", "fold", "group", "tag"])
         .agg(adult_pred=("adult_pred", "mean"), y_tahini=("y_tahini", "first"),
              y_sunflower=("y_sunflower", "first")).reset_index())
    s["thr"] = [info[f]["plsr_threshold"] if m == "PLS-R" else info[f]["dnnr_threshold"][sd]
                for m, f, sd in zip(s["model"], s["fold"], s["seed"])]
    s["flag"] = s["adult_pred"] > s["thr"]
    pl = s[s.model == "PLS-R"].set_index("group")

    def summary(flag, ref):
        miss = ref[(~flag) & (ref.tag == 1)]
        return dict(fp_lots=ref.fold[flag & (ref.tag == 0)].tolist(), n_authentic=int((ref.tag == 0).sum()),
                    n_blends=int((ref.tag == 1).sum()), missed=[
                        [round(100 - r.y_tahini), "sunflower" if r.y_sunflower > 0 else "peanut", r.fold]
                        for r in miss.itertuples()])
    out = {"PLS-R": summary(pl["flag"], pl), "per_seed": []}
    for seed in sorted(s.seed[s.model == "MT-DNN-R"].unique()):
        dn = s[(s.model == "MT-DNN-R") & (s.seed == seed)].set_index("group").reindex(pl.index)
        out["per_seed"].append(dict(seed=int(seed), mtdnn_r=summary(dn["flag"], dn),
                                    both=summary(pl["flag"] & dn["flag"], pl)))
    dump(out, "consensus.json" if regions == "chem" else f"consensus_{regions}.json")
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "chem")
