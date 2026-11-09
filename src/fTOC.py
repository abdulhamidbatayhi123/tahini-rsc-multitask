"""Graphical abstract (RSC table-of-contents entry, 8 cm x 4 cm).
Left: mean SNV spectra of authentic tahini and the two adulterant pastes (input). Right: which withheld authentic
lot each composition route rejected at sample level (leave-one-lot-out): MT-DNN-R and PLS-R from
results/metrics_lot.csv (share of authentic scans flagged), agreement rule from results/consensus.json."""
import json

import matplotlib
import numpy as np

from common import RESULTS
from figstyle import C, FIG, plt

from common import load

_d = load()
_auth, _g = _d["tag"] == 0, _d["group"]
WN = _d["wn"]
MEANS = {"tahini": _d["X"][_auth].mean(0), "sunflower": _d["X"][_g == "T5_S100"].mean(0),
         "peanut": _d["X"][_g == "T5_P100"].mean(0)}

lot = __import__("pandas").read_csv(RESULTS / "metrics_lot.csv")
lot = lot[(lot.scheme == "lolo") & (lot.regions == "chem")]
con = json.loads((RESULTS / "consensus.json").read_text())
LOTS = ["T1", "T2", "T3", "T4", "T5"]
fp = {m: lot[lot.model == m].set_index("fold").loc[LOTS, "fp_rate_authentic"].to_numpy() for m in ("MT-DNN-R", "PLS-R")}
both_fp = set().union(*[set(s["both"]["fp_lots"]) for s in con["per_seed"]])
rows = [("Network", fp["MT-DNN-R"]), ("PLS", fp["PLS-R"]), ("Flag only if both", np.array([1.0 if l in both_fp else 0.0 for l in LOTS]))]

fig = plt.figure(figsize=(8 / 2.54, 4 / 2.54))
ax = fig.add_axes([0.03, 0.22, 0.38, 0.62])
wn, means = WN, MEANS
for name, col, ls in (("tahini", "#000000", "-"), ("sunflower", C["sunflower"], "--"), ("peanut", C["peanut"], ":")):
    m = (wn >= 900) & (wn <= 1800)
    ax.plot(wn[m], means[name][m], color=col, ls=ls, lw=0.8, label=name)
ax.invert_xaxis()
ax.set_yticks([])
ax.set_xticks([1700, 1300, 900])
ax.tick_params(labelsize=6)
ax.set_xlabel("cm$^{-1}$", fontsize=6, labelpad=1)
ax.legend(fontsize=5.5, frameon=False, loc="upper center", bbox_to_anchor=(0.55, 1.02), handlelength=1.6, borderaxespad=0.1)
for s in ("top", "right", "left"):
    ax.spines[s].set_visible(False)
fig.text(0.22, 0.92, "ATR–FTIR, unseen lot", ha="center", fontsize=6.5)

ax2 = fig.add_axes([0.66, 0.22, 0.33, 0.62])
M = np.vstack([r[1] for r in rows])
ax2.imshow(M, cmap="Greys", vmin=0, vmax=1.25, aspect="auto")
for i in range(M.shape[0]):
    for j in range(M.shape[1]):
        ax2.text(j, i, "no" if M[i, j] > 0.5 else "yes", ha="center", va="center", fontsize=6,
                 color="#ffffff" if M[i, j] > 0.6 else "#000000")
ax2.set_xticks(range(5), LOTS, fontsize=6)
ax2.set_yticks(range(3), [r[0] for r in rows], fontsize=6)
ax2.tick_params(length=0)
for s in ax2.spines.values():
    s.set_visible(False)
fig.text(0.78, 0.92, "Authentic lot accepted?", ha="center", fontsize=6.5)
fig.text(0.45, 0.53, "→", ha="center", va="center", fontsize=12)
for t in fig.findobj(matplotlib.text.Text):
    assert not t.get_text().strip() or t.get_fontsize() >= 5.5
for ext, kw in (("pdf", {}), ("tif", dict(dpi=600, pil_kwargs={"compression": "tiff_lzw"})), ("png", dict(dpi=300))):
    fig.savefig(FIG / f"toc_graphic.{ext}", **kw)
print("saved", FIG / "toc_graphic.png", M.round(2).tolist())
