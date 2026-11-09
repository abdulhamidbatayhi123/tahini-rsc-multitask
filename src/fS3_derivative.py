"""ESI Fig. S3 (referee point B4): second-derivative spectra of the five authentic lots.

Savitzky-Golay second derivative (polynomial order 2, window 13 points = 12 intervals x 1.929 cm-1
= 23.1 cm-1 wide) of the SNV spectra (SNV over the full spectrum, as in common.features), computed on
the full contiguous axis and then cut to three windows:
  (a) 1150-1300 cm-1, lot T1 against the other four (ester C-O / amide III region of Section 3.5);
  (b) 1680-1780 cm-1, lot T2 against the other four (ester C=O and the free-fatty-acid shoulder near 1709);
  (c) 690-740 cm-1, lot T2 against the other four (CH2 rocking near 717-720).
Per-lot mean +/- SD over the authentic scans (tag == 0). Windows 9 (15.4 cm-1) and 17 (30.9 cm-1)
points are run as a robustness check (results only, not plotted).

Band centres = local minima of each lot's mean second derivative inside the window (value < 0 and
prominence >= PROM_FRAC of the largest |mean| in that window over all lots), located to sub-channel
precision by a three-point parabola. Standardised difference (same definition as Section 2.8 /
s03_lots.py, applied to the second derivative): mean of the target lot minus the mean of the other four
lot means, divided by the mean of the five per-lot SDs. Shift test: each target-lot minimum is matched
to the nearest minimum of the mean of the other four lot means; a shift is called when the interpolated
positions differ by more than one channel (1.93 cm-1). Per-scan minimum positions (parabolic, searched
within +/- 4 channels of the lot-mean minimum) give a scan-level check of the same shift.

Outputs: figures/figS3_derivative.{pdf,tif,png} + provenance, results/derivative_bands.json.
Exploratory, added after the lot-out results in answer to the referee; no model is refitted."""
import json
from pathlib import Path

import numpy as np
from scipy.signal import find_peaks, savgol_filter

from common import DATA_XLSX, RESULTS, load, sha256, snv
from figstyle import DOUBLE, FIG, panel, plt, save

WINDOWS = {"a": ("T1", 1150.0, 1300.0), "b": ("T2", 1680.0, 1780.0), "c": ("T2", 690.0, 740.0)}
SG_MAIN, SG_ROBUST, POLY = 13, (9, 17), 2
PROM_FRAC = 0.05
TARGET_COL, OTHER_COL = "#D55E00", "#7F7F7F"     # Okabe-Ito vermillion (not used elsewhere) vs grey
SCALE = 1e3                                       # plot units: 10^-3 cm^2


def parabolic(y, i):
    """Sub-channel position (fractional index) of an extremum at interior index i."""
    a, b, c = y[i - 1], y[i], y[i + 1]
    den = a - 2 * b + c
    return i + (0.5 * (a - c) / den if den != 0 else 0.0)


def interp_wn(wn, x):
    return float(np.interp(x, np.arange(len(wn)), wn))


def minima(y, wn, prom):
    idx, _ = find_peaks(-y, prominence=prom)
    idx = [i for i in idx if 0 < i < len(y) - 1 and y[i] < 0]
    return [dict(channel_wn=round(float(wn[i]), 2), centre_wn=round(interp_wn(wn, parabolic(y, i)), 2),
                 value=float(y[i]), _i=int(i)) for i in idx]


def per_scan_positions(D, wn, i0, half=4):
    """Parabolic minimum position of every scan within +/- half channels of index i0 (cm-1)."""
    lo, hi = i0 - half, i0 + half + 1
    out = []
    for row in D:
        seg = row[lo:hi]
        j = int(np.argmin(seg))
        if 0 < j < len(seg) - 1:
            out.append(interp_wn(wn, lo + parabolic(seg, j)))
        else:
            out.append(np.nan)
    return np.array(out)


def analyse(Z, wn, lot, sg):
    dx = float(np.mean(np.diff(wn)))
    D = savgol_filter(Z, sg, POLY, deriv=2, delta=dx, axis=1)
    lots = sorted(set(lot))
    M = {L: D[lot == L].mean(0) for L in lots}
    S = {L: D[lot == L].std(0, ddof=1) for L in lots}
    pooled = np.mean([S[L] for L in lots], 0)
    res = {}
    for key, (T, lo, hi) in WINDOWS.items():
        w = (wn >= lo) & (wn <= hi)
        ww = wn[w]
        others = [L for L in lots if L != T]
        ref = np.mean([M[L] for L in others], 0)
        dstd = (M[T] - ref) / pooled
        prom = PROM_FRAC * max(np.abs(M[L][w]).max() for L in lots)
        mins = {L: minima(M[L][w], ww, prom) for L in lots}
        ref_mins = minima(ref[w], ww, prom)
        off = int(np.where(w)[0][0])
        tgt = []
        for m in mins[T]:
            i = m["_i"] + off
            entry = {k: v for k, v in m.items() if k != "_i"}
            entry["std_diff_at_target_min"] = round(float(dstd[i]), 2)
            if ref_mins:
                r = min(ref_mins, key=lambda q: abs(q["centre_wn"] - m["centre_wn"]))
                ri = r["_i"] + off
                sh = m["centre_wn"] - r["centre_wn"]
                entry.update(matched_ref_centre_wn=r["centre_wn"], shift_cm1=round(sh, 2),
                             shift_channels=round(sh / dx, 2), shift_gt_1_channel=bool(abs(sh) > dx),
                             std_diff_at_ref_min=round(float(dstd[ri]), 2),
                             depth_ratio_target_over_ref=round(float(M[T][i] / ref[ri]), 3))
                # scan-level check around the target-lot minimum
                pt = per_scan_positions(D[lot == T], wn, i)
                po = {L: per_scan_positions(D[lot == L], wn, ri) for L in others}
                entry["per_scan_centre_wn"] = {
                    T: [round(float(np.nanmean(pt)), 2), round(float(np.nanstd(pt, ddof=1)), 2)],
                    **{L: [round(float(np.nanmean(v)), 2), round(float(np.nanstd(v, ddof=1)), 2)]
                       for L, v in po.items()}}
            tgt.append(entry)
        j = int(np.argmax(np.abs(dstd[w])))
        res[key] = dict(
            target_lot=T, range_cm1=[lo, hi], prominence_threshold=prom,
            minima_per_lot={L: [{k: v for k, v in m.items() if k != "_i"} for m in mins[L]] for L in lots},
            minima_mean_of_other_four=[{k: v for k, v in m.items() if k != "_i"} for m in ref_mins],
            target_minima=tgt,
            max_abs_std_diff_in_window=dict(wn=round(float(ww[j]), 2), value=round(float(dstd[w][j]), 2)))
    # 1709 component: any local minimum (no prominence filter, value < 0) within 1700-1718 cm-1
    w = (wn >= 1700) & (wn <= 1718)
    ww = wn[w]
    f1709 = {}
    for L in lots:
        y = M[L][w]
        idx, _ = find_peaks(-y)
        idx = [i for i in idx if y[i] < 0]
        scans = D[lot == L][:, w]
        frac = float(np.mean([any(r[i] < 0 for i in find_peaks(-r)[0]) for r in scans]))
        f1709[L] = dict(mean_has_minimum=bool(idx),
                        mean_minima_wn=[round(interp_wn(ww, parabolic(y, i)), 2) for i in idx if 0 < i < len(y) - 1],
                        value_at_1709=float(np.interp(1709.0, wn, M[L])),
                        fraction_of_scans_with_minimum=round(frac, 3))
    others = [L for L in lots if L != "T2"]
    i09 = int(np.argmin(np.abs(wn - 1709.0)))
    f1709["T2_std_diff_at_1709"] = round(float((M["T2"][i09] - np.mean([M[L][i09] for L in others])) / pooled[i09]), 2)
    res["component_1709"] = f1709
    # standardised difference of the 2nd derivative at the Section 3.5 SNV-departure bands, and per-lot
    # RMS / largest |d| over 600-1800 cm-1 (same definition as s03_lots.py, here on the 2nd derivative)
    dd = {L: (M[L] - np.mean([M[k] for k in lots if k != L], 0)) / pooled for L in lots}
    res["std_diff_at_section35_bands"] = {
        f"{L}@{v}": round(float(dd[L][int(np.argmin(np.abs(wn - v)))]), 2)
        for L, v in (("T1", 1215), ("T1", 1248), ("T1", 1273), ("T2", 1709), ("T2", 717))}
    m = (wn >= 600) & (wn <= 1800)
    res["lot_departure_600_1800"] = {
        L: dict(rms=round(float(np.sqrt((dd[L][m] ** 2).mean())), 2),
                max_abs_wn=round(float(wn[m][np.argmax(np.abs(dd[L][m]))]), 1),
                max_abs_value=round(float(dd[L][m][np.argmax(np.abs(dd[L][m]))]), 2)) for L in lots}
    return res, D, M, S


def main():
    d = load()
    wn = d["wn"]
    a = d["tag"] == 0
    Z = snv(d["X"])[a]
    lot = d["lot"][a]
    dx = float(np.mean(np.diff(wn)))
    out = dict(
        description=__doc__.split("\n")[0],
        method=dict(preprocessing="SNV over full spectrum (common.snv), then Savitzky-Golay 2nd derivative "
                                  "on the full contiguous axis (scipy.signal.savgol_filter, delta = spacing)",
                    polyorder=POLY, spacing_cm1=round(dx, 4),
                    windows_points={str(s): round((s - 1) * dx, 1) for s in (SG_MAIN, *SG_ROBUST)},
                    window_width_note="width = (points - 1) x spacing, cm-1",
                    minimum_rule=f"local minimum of lot-mean 2nd derivative, value < 0, prominence >= "
                                 f"{PROM_FRAC} x largest |mean| in window over the five lots; parabolic interpolation",
                    std_diff="(target lot mean - mean of other four lot means) / mean of five per-lot SDs",
                    shift_rule="|target centre - centre of nearest minimum of mean of other four| > 1 channel",
                    units="2nd derivative of SNV absorbance, cm^2"),
        n_scans={L: int((lot == L).sum()) for L in sorted(set(lot))},
        results={})
    for sg in (SG_MAIN, *SG_ROBUST):
        r, D, M, S = analyse(Z, wn, lot, sg)
        out["results"][f"sg{sg}"] = r
        if sg == SG_MAIN:
            Dm, Mm, Sm = D, M, S
    out["dataset_metadata"] = dict(
        per_lot_acquisition_dates="none in data file or README",
        per_lot_temperatures="none in data file or README",
        what_exists="README: Bruker Tensor 27 ATR, 4 cm-1, 16 scans, Istanbul suppliers; xlsx docProps only "
                    "file created 2025-12-08 / modified 2026-03-18 (file-level, not per lot); columns are "
                    "isim, label and the three fractions only")
    p = RESULTS / "derivative_bands.json"
    p.write_text(json.dumps(out, indent=2))

    # ------------------------------------------------------------------------------- figure
    lots = sorted(set(lot))
    fig, axs = plt.subplots(1, 3, figsize=(DOUBLE, 6.2 / 2.54), gridspec_kw=dict(width_ratios=[1.5, 1.0, 0.75]))
    LSO = {"T1": "-", "T2": "-", "T3": "--", "T4": ":", "T5": "-."}
    titles = {"a": "Ester C–O / amide III", "b": "C=O (ester; FFA near 1709)", "c": "CH$_2$ rocking"}
    for ax, (key, (T, lo, hi)) in zip(axs, WINDOWS.items()):
        w = (wn >= lo - 0.01) & (wn <= hi + 0.01)
        for L in lots:
            tgt = L == T
            col = TARGET_COL if tgt else OTHER_COL
            m, s = Mm[L][w] * SCALE, Sm[L][w] * SCALE
            ax.fill_between(wn[w], m - s, m + s, color=col, alpha=0.22 if tgt else 0.10, lw=0, zorder=2 if tgt else 1)
            ax.plot(wn[w], m, color=col, lw=1.1 if tgt else 0.7, ls="-" if tgt else LSO[L],
                    zorder=4 if tgt else 3, label=L)
        for m in out["results"][f"sg{SG_MAIN}"][key]["target_minima"]:
            ax.axvline(m["centre_wn"], color="#000000", lw=0.35, ls=(0, (1, 2)), zorder=0)
        if key == "b":
            ax.axvspan(1700, 1718, color="#E5E5E5", lw=0, zorder=0)
        ax.axhline(0, color="#000000", lw=0.4, zorder=0)
        ax.set_xlim(hi, lo)
        ax.set_xlabel("Wavenumber (cm$^{-1}$)")
        ax.set_title(f"{titles[key]}: {T} vs other lots", fontsize=6.5)
        ax.legend(loc="lower left" if key != "c" else "lower right", handlelength=1.8, fontsize=6,
                  ncol=1, borderaxespad=0.2)
        panel(ax, key, x=-0.2 if key == "a" else -0.24)
    axs[0].set_ylabel("2nd derivative of SNV spectrum (10$^{-3}$ cm$^{2}$)")
    fig.tight_layout(w_pad=0.8)
    save(fig, "figS3_derivative", __file__, [DATA_XLSX, Path(__file__).resolve().parents[0] / "common.py"])
    fig.savefig(FIG / "figS3_derivative.png", dpi=300)          # ESI PNG at 300 dpi (save() writes 200)
    pp = FIG / "figS3_derivative.provenance.json"
    prov = json.loads(pp.read_text())
    prov.update(png_dpi=300, tif_dpi=600, tif_compression="LZW", results_json=p.name,
                results_json_sha256=sha256(p), sg_window_points=SG_MAIN, sg_polyorder=POLY)
    pp.write_text(json.dumps(prov, indent=2))
    print(json.dumps(out["results"], indent=1)[:6000])


if __name__ == "__main__":
    main()
