"""Audit: does the user's confusion matrix (test n=311: 150 pure, 161 adulterated)
match a random spectrum-level 80/20 split (replicate leakage) rather than a grouped split?"""
import sys
import pandas as pd
from sklearn.model_selection import train_test_split

path = sys.argv[1]
df = pd.read_pickle(path) if path.endswith(".pkl") else pd.read_excel(path)
y = df["Tağşiş Var mı"].astype(int).values
g = df["isim"].astype(str).values
print("n spectra", len(df), "pure", (y == 0).sum(), "adult", (y == 1).sum(), "samples", len(set(g)))
hits = []
for strat in (False, True):
    for rs in list(range(0, 101)) + [123, 1234, 2024, 2025, 2026]:
        idx = list(range(len(y)))
        tr, te = train_test_split(idx, test_size=0.2, random_state=rs, stratify=y if strat else None)
        n0 = int((y[te] == 0).sum()); n1 = int((y[te] == 1).sum())
        shared = len(set(g[tr]) & set(g[te]))
        if (n0, n1) == (150, 161):
            hits.append((strat, rs, shared))
print("test size", len(te))
print("splits reproducing 150/161 (stratify, seed, samples on both sides):", hits[:20], "count", len(hits))
tr, te = train_test_split(list(range(len(y))), test_size=0.2, random_state=42)
print("seed 42 unstratified: test pure", (y[te] == 0).sum(), "adult", (y[te] == 1).sum(),
      "physical samples shared train/test", len(set(g[tr]) & set(g[te])), "of", len(set(g)))
