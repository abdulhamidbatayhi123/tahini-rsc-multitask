"""Fig. 5 (exploratory, added 2026-11-08 after the hold-out results). Which spectral bands the models use.
Models refitted on all 55 samples (PLS with the component number chosen by grouped CV; MT-DNN with five
seeds). (a) Mean SNV spectrum of authentic tahini for orientation. (b) PLS regression coefficients for the
tahini fraction. (c) MT-DNN attribution for the tahini-fraction output and (d) for the class logit:
mean |gradient x input| over all scans (inputs standardised as in training), averaged over seeds.
Each attribution trace is scaled to its maximum. Output: figures/fig5_attribution.*,
results/attribution.csv, results/attribution_top_bands.json."""
import numpy as np
import pandas as pd
import torch

from common import DATA_XLSX, MTDNN, PLSPair, RESULTS, dump, features, load
from figstyle import C, DOUBLE, panel, plt, save

d = load()
X, wn = features(d, "chem")
y, tag, g = d["y"], d["tag"], d["group"]

pls = PLSPair().fit(X, y, tag, g)
coef_t = pls.reg.coef_[0] if pls.reg.coef_.shape[0] == 3 else pls.reg.coef_[:, 0]

att_reg, att_cls = [], []
for s in range(5):
    m = MTDNN(seed=s).fit(X, y, tag, g)
    xt = torch.tensor((X - m.mu) / m.sd, dtype=torch.float32, requires_grad=True)
    logit, comp = m.net(xt)
    gr, = torch.autograd.grad(comp[:, 0].sum(), xt, retain_graph=True)
    att_reg.append((gr * xt).abs().mean(0).detach().numpy())
    gc, = torch.autograd.grad(logit.sum(), xt)
    att_cls.append((gc * xt).abs().mean(0).detach().numpy())
A_reg, A_cls = np.mean(att_reg, 0), np.mean(att_cls, 0)
pd.DataFrame(dict(wavenumber=wn, pls_coef_tahini=coef_t, att_tahini=A_reg, att_class=A_cls)).to_csv(
    RESULTS / "attribution.csv", index=False)


def top_bands(a, k=8, sep=15.0):
    order, out = np.argsort(a)[::-1], []
    for i in order:
        if all(abs(wn[i] - w) >= sep for w in out):
            out.append(float(wn[i]))
        if len(out) == k:
            break
    return out


dump(dict(pls_k=pls.kr, top_pls=top_bands(np.abs(coef_t)), top_att_tahini=top_bands(A_reg),
          top_att_class=top_bands(A_cls),
          corr_att_tahini_vs_class=float(np.corrcoef(A_reg, A_cls)[0, 1]),
          corr_abs_pls_vs_att_tahini=float(np.corrcoef(np.abs(coef_t), A_reg)[0, 1])), "attribution_top_bands.json")

# plot on a broken x axis: 3050-2800 | 1800-600
fig, axs = plt.subplots(4, 2, figsize=(DOUBLE, 11 / 2.54), sharex="col", sharey="row",
                        gridspec_kw=dict(width_ratios=[250, 1200], wspace=0.05))
mean_auth = X[tag == 0].mean(0)
traces = [(mean_auth, "SNV absorbance", C["tahini"]), (coef_t, "PLS coefficient\n(tahini)", C["PLS"]),
          (A_reg / A_reg.max(), "MT-DNN |grad×input|\n(tahini fraction)", C["MT-DNN"]),
          (A_cls / A_cls.max(), "MT-DNN |grad×input|\n(class logit)", C["MT-DNN"])]
for r, (tr, lab, col) in enumerate(traces):
    for c, (lo, hi) in enumerate(((2800, 3050), (600, 1800))):
        ax = axs[r, c]
        m = (wn >= lo) & (wn <= hi)
        ax.plot(wn[m], tr[m], color=col, lw=0.8)
        if r == 1:
            ax.axhline(0, color=C["grey"], lw=0.5)
        ax.set_xlim(hi, lo)
        if c == 1:
            ax.spines["left"].set_visible(False)
            ax.tick_params(left=False)
    axs[r, 0].set_ylabel(lab)
    panel(axs[r, 0], "abcd"[r], x=-0.9)
for c in range(2):
    axs[3, c].set_xlabel("Wavenumber (cm$^{-1}$)" if c == 1 else " ")
for w, lab in ((2922, "CH$_2$"), (2853, "CH$_2$"), (1745, "C=O"), (1650, "amide I"), (1540, "amide II"),
               (1160, "C–O"), (721, "ρ CH$_2$")):
    col = 0 if w > 2000 else 1
    axs[0, col].annotate(lab, (w, axs[0, col].get_ylim()[1]), ha="center", va="bottom", fontsize=6,
                         annotation_clip=False)
fig.subplots_adjust(left=0.13, right=0.99, top=0.95, bottom=0.09, hspace=0.25)
save(fig, "fig5_attribution", __file__, [DATA_XLSX])
