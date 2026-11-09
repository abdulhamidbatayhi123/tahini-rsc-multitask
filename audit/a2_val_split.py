"""Audit for amendment A2 (ESI S2): before A2 the MT-DNN never trained on its inner early-stopping set.
Reproduce that set exactly (GroupShuffleSplit, test_size 0.2, random_state = seed, as in common.MTDNN.fit) for every
leave-one-lot-out fold and seed, and count the authentic training lots it removed. Writes results/a2_val_split.json."""
import json
import sys
from collections import Counter

import numpy as np
from sklearn.model_selection import GroupShuffleSplit

sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[1] / "src"))
from common import RESULTS, load, lolo_folds  # noqa: E402

d = load()
rows = []
for L, tr, _ in lolo_folds(d):
    g, tag = d["group"][tr], d["tag"][tr]
    for s in range(5):
        _, va = next(GroupShuffleSplit(n_splits=1, test_size=0.2, random_state=s).split(np.zeros(len(tr)), groups=g))
        auth_out = sorted(set(g[va][tag[va] == 0]))
        rows.append(dict(fold=L, seed=s, val_samples=len(set(g[va])), authentic_lots_removed=len(auth_out),
                         removed=auth_out))
cnt = Counter(r["authentic_lots_removed"] for r in rows)
out = dict(note="inner early-stopping set of the pre-A2 MT-DNN, lot-out chem, 5 folds x 5 seeds",
           count_by_n_authentic_removed={str(k): v for k, v in sorted(cnt.items())}, fits=rows)
(RESULTS / "a2_val_split.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
print(out["count_by_n_authentic_removed"])
