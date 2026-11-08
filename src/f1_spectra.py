"""Fig. 1. (a) Mean ATR-FTIR spectra of authentic tahini (5 lots), sunflower paste and peanut paste (100 %
samples), with the modelled regions shaded. (b) Ratio of between-sample to within-sample variance of the
SNV spectra per channel (exploratory diagnostic, 2026-11-08): composition information sits in the C-H
stretching and fingerprint regions; the CO2 and water-vapour bands carry little sample-to-sample signal."""
import numpy as np

from common import CHEM_REGIONS, DATA_XLSX, dump, load, snv
from figstyle import C, DOUBLE, LS, panel, plt, save

d = load()
X, wn, g, y = d["X"], d["wn"], d["group"], d["y"]
auth = d["tag"] == 0
sun = g == "T5_S100"
pea = g == "T5_P100"

fig, axs = plt.subplots(2, 1, figsize=(DOUBLE, 9.5 / 2.54), sharex=True)
ax = axs[0]
for lo, hi in CHEM_REGIONS:
    ax.axvspan(lo, hi, color="#E8E8E8", lw=0, zorder=0)
for name, m in (("Tahini, authentic", auth), ("Sunflower paste", sun), ("Peanut paste", pea)):
    key = name.split()[0].strip(",").lower()
    ax.plot(wn, X[m].mean(0), color=C[key], ls=LS[key], label=f"{name} ({m.sum()} scans)")
bands = [(3008, "=C–H"), (2922, "ν$_{as}$ CH$_2$"), (2853, "ν$_s$ CH$_2$"), (1745, "ν C=O"), (1650, "amide I"),
         (1540, "amide II"), (1463, "δ CH$_2$"), (1160, "ν C–O"), (721, "ρ CH$_2$")]
top = X[auth].mean(0)
for b, lab in bands:
    i = np.argmin(abs(wn - b))
    ax.annotate(lab, (wn[i], top[i]), xytext=(0, 6), textcoords="offset points", ha="center", fontsize=6,
                rotation=90, va="bottom")
ax.set_ylabel("Absorbance (a.u.)")
ax.set_ylim(top=0.40)
ax.legend(loc="upper left", bbox_to_anchor=(0.36, 0.97))
panel(ax, "a", x=-0.07)

ax = axs[1]
Z = snv(X)
us = np.unique(g)
W = np.array([Z[g == u].var(0, ddof=1) for u in us]).mean(0)
B = np.array([Z[g == u].mean(0) for u in us]).var(0, ddof=1)
F = B / W
for lo, hi in CHEM_REGIONS:
    ax.axvspan(lo, hi, color="#E8E8E8", lw=0, zorder=0)
ax.axvspan(2250, 2400, color="#F3D9C4", lw=0, zorder=0)
ax.axvspan(3550, 4000, color="#D6E6F2", lw=0, zorder=0)
ax.plot(wn, F, color="#000000", lw=0.8)
ax.set_yscale("log")
ax.axhline(1, color=C["grey"], lw=0.6, ls="--")
yl = ax.get_ylim()
ax.text(2325, yl[1] * 0.6, "CO$_2$", ha="center", fontsize=6.5)
ax.text(3775, yl[1] * 0.6, "H$_2$O vapour", ha="center", fontsize=6.5)
ax.set_ylabel("Between- / within-sample\nvariance (SNV)")
ax.set_xlabel("Wavenumber (cm$^{-1}$)")
ax.set_xlim(4000, 600)
panel(ax, "b", x=-0.07)
fig.tight_layout(h_pad=0.6)

# numbers quoted in the text
def med_in(lo, hi):
    m = (wn >= lo) & (wn <= hi)
    return float(np.median(F[m]))

chem = np.zeros_like(wn, bool)
for lo, hi in CHEM_REGIONS:
    chem |= (wn >= lo) & (wn <= hi)
dump({"n_auth": int(auth.sum()), "n_sun100": int(sun.sum()), "n_pea100": int(pea.sum()),
      "F_median_600_1800": med_in(600, 1800), "F_median_2800_3050": med_in(2800, 3050),
      "F_median_co2_2250_2400": med_in(2250, 2400), "F_median_h2o_3550_4000": med_in(3550, 4000),
      "n_channels_chem": int(chem.sum())}, "f1_numbers.json")
save(fig, "fig1_spectra", __file__, [DATA_XLSX])
