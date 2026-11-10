"""Generated ESI tables (markdown) from the result files; nothing typed by hand.
Writes manuscript/esi_tables.md, included by manuscript/esi.md via build/build_esi.py."""
import json
from pathlib import Path

import pandas as pd

from common import RESULTS

OUT = Path(__file__).resolve().parents[1] / "manuscript" / "esi_tables.md"
L = []


def table(title, hdr, rows, note=""):
    L.extend([f"**{title}**", "", "| " + " | ".join(hdr) + " |", "|" + "|".join(["---"] * len(hdr)) + "|"])
    L.extend("| " + " | ".join(map(str, r)) + " |" for r in rows)
    if note:
        L.extend(["", note])
    L.append("")


# S1 per-fold settings
info = json.loads((RESULTS / "run_info_lolo_chem.json").read_text())
rows = []
for f in info["folds"]:
    t = f["dnnr_threshold"]
    rows.append([f["fold"], f["n_train"], f["n_test"], f["pls_k_reg"], f["pls_k_cls"], f"{f['plsr_threshold']:.2f}",
                 f"{min(t):.2f}–{max(t):.2f}", ", ".join(map(str, f["dnn_best_epoch"]))])
table("Table S1 Settings chosen inside each leave-one-lot-out training set (chemically informative regions).",
      ["Withheld lot", "Training scans", "Test scans", "PLS2 latent variables", "PLS-DA latent variables",
       "PLS-R threshold (% adulterant)", "MT-DNN-R threshold, range over seeds (% adulterant)",
       "MT-DNN best epoch (seeds 0–4)"], rows,
      "Source: results/run_info_lolo_chem.json.")

# S2 per-lot metrics
lot = pd.read_csv(RESULTS / "metrics_lot.csv")
lot = lot[(lot.scheme == "lolo") & (lot.regions == "chem")]
rows = []
for (fold, model), r in lot.set_index(["fold", "model"]).sort_index().iterrows():
    quant = model in ("PLS-R", "MT-DNN")
    rows.append([fold, model, f"{100 * r.fp_rate_authentic:.1f}", f"{100 * r.fn_rate_blends:.1f}",
                 f"{r.rmsep_tahini:.2f}" if quant else "", f"{r.r2_tahini:.3f}" if quant else "",
                 f"{100 * r.identification:.1f}" if quant else ""])
table("Table S2 Results for each withheld lot (scan level; MT-DNN routes: mean of five seeds).",
      ["Withheld lot", "Route", "Authentic scans flagged (%)", "Blend scans missed (%)", "RMSEP (% tahini)", "R²",
       "Identification (%)"], rows,
      "Source: results/metrics_lot.csv. R² within one lot is computed over that lot's 11 samples only.")

# S3 lot departure
dep = json.loads((RESULTS / "lot_departure.json").read_text())
_depcsv = pd.read_csv(RESULTS / "lot_departure.csv", index_col="wavenumber")  # unrounded (JSON stores 2 dp)
rows = []
for k in ("T1", "T2", "T3", "T4", "T5"):
    v = dep[k]
    o = v["observed"]
    rows.append([k, f"{v['rms_d']:.2f}", "; ".join(f"{b[0]} ({_depcsv.loc[_depcsv.index[abs(_depcsv.index - b[0]).argmin()], k]:+.2f})"
                                                for b in v["top_bands"]),
                 f"{v['pls_adulterant_shift']:+.1f}", f"{o['PLS-R']['authentic_adult_mean']:.2f}",
                 f"{o['MT-DNN']['authentic_adult_mean']:.2f}"])
table("Table S3 Exploratory: how each authentic lot departs from the other four.",
      ["Lot", "RMS departure (pooled SD)", "Largest departures, cm⁻¹ (SD units)",
       "Projected PLS adulterant shift (points)", "Observed PLS-R mean (% adulterant)",
       "Observed MT-DNN mean (% adulterant)"], rows,
      "Source: results/lot_departure.json (src/s03_lots.py). The projected shift is the unscaled departure "
      "multiplied by the sunflower and peanut PLS2 coefficients of the model that withheld the lot, before "
      "clipping; observed values are the mean predicted adulterant fraction of the lot's authentic scans.")
rows = [[nm.replace("100", " paste, 100 %"), dep[nm]["n_scans"],
         "; ".join(f"{b[0]} ({b[1]:+.3f})" for b in dep[nm]["top_bands"])] for nm in ("sunflower100", "peanut100")]
table("Table S4 Largest differences between the pure adulterant pastes and authentic tahini (mean SNV spectra).",
      ["Paste", "Scans", "Wavenumber, cm⁻¹ (difference, SNV units)"], rows, "Source: results/lot_departure.json.")

# S5 agreement rule
con = json.loads((RESULTS / "consensus.json").read_text())
rows = [["PLS-R", "–", ", ".join(con["PLS-R"]["fp_lots"]) or "none",
         "; ".join(f"{m[0]} % {m[1]} ({m[2]})" for m in con["PLS-R"]["missed"]) or "none"]]
for s in con["per_seed"]:
    for key, lab in (("mtdnn_r", "MT-DNN-R"), ("both", "PLS-R and MT-DNN-R")):
        v = s[key]
        rows.append([lab, s["seed"], ", ".join(v["fp_lots"]) or "none",
                     "; ".join(f"{m[0]} % {m[1]} ({m[2]})" for m in v["missed"]) or "none"])
table("Table S5 Exploratory sample-level agreement rule (leave-one-lot-out; 5 authentic and 50 blend samples).",
      ["Rule", "Seed", "Authentic lots flagged", "Blends missed (level, adulterant, lot)"], rows,
      "Source: results/consensus.json (src/s04_consensus.py).")

# S6 effect of amendment A2 (MT-DNN refit on all training samples); point estimates, before = results/v1_A1
m = pd.read_csv(RESULTS / "metrics.csv")
old = pd.read_csv(RESULTS / "v1_A1" / "metrics.csv")
rows = []
for scheme in ("holdout", "lolo", "random"):
    for level in ("sample", "scan"):
        for model in ("MT-DNN", "MT-DNN-R"):
            sel = lambda d: d[(d.scheme == scheme) & (d.level == level) & (d.model == model) & (d.regions == "chem")]
            o, n = sel(old), sel(m)
            if o.empty or n.empty:
                continue
            o, n = o.iloc[0], n.iloc[0]
            pair = lambda k, f: f"{f(o[k])} / {f(n[k])}"
            pct = lambda v: f"{100 * v:.1f}"
            rows.append([scheme, level, model, pair("sensitivity", pct), pair("specificity", pct),
                         pair("auc", lambda v: f"{v:.3f}"), pair("rmsep_tahini", lambda v: f"{v:.2f}"),
                         pair("lod", lambda v: f"{v:.2f}") if level == "sample" and model == "MT-DNN" else ""])
table("Table S6 MT-DNN results before / after amendment A2 (refit on all training samples; chemically informative "
      "regions; point estimates, means over five seeds). PLS results are not affected by A2.",
      ["Validation", "Level", "Route", "Sensitivity (%)", "Specificity (%)", "AUC", "RMSEP (% tahini)", "LOD (%)"], rows,
      "Source: results/v1_A1/metrics.csv (before) and results/metrics.csv (after).")

# S7 full-range sensitivity, if available
full = m[(m.regions == "full")]
if not full.empty:
    rows = []
    for scheme in ("holdout", "lolo", "random"):
        for model in ("PLS-DA", "PLS-R", "MT-DNN", "MT-DNN-R"):
            c = m[(m.scheme == scheme) & (m.level == "scan") & (m.model == model) & (m.regions == "chem")]
            f = m[(m.scheme == scheme) & (m.level == "scan") & (m.model == model) & (m.regions == "full")]
            if c.empty or f.empty:
                continue
            c, f = c.iloc[0], f.iloc[0]
            rows.append([scheme, model, f"{100 * c.sensitivity:.1f} / {100 * f.sensitivity:.1f}",
                         f"{100 * c.specificity:.1f} / {100 * f.specificity:.1f}",
                         f"{c.rmsep_tahini:.2f} / {f.rmsep_tahini:.2f}"])
    table("Table S7 Sensitivity analysis: chemically informative regions (752 channels) / full 600–4000 cm⁻¹ range "
          "(scan level).", ["Validation", "Route", "Sensitivity (%)", "Specificity (%)", "RMSEP (% tahini)"], rows,
          "Source: results/metrics.csv (regions chem and full).")


# S8 supplementary analyses (src/s05_extra.py)
ex = json.loads((RESULTS / "extra.json").read_text())
rows = []
for fam, res in ex["paired"].items():
    for r in res:
        rows.append(["Paired routes, " + fam, "seed " + str(r["seed"]) if r["seed"] >= 0 else "–",
                     f"class right / regression wrong: {r['class_right_reg_wrong']}; reverse: {r['class_wrong_reg_right']}; "
                     f"exact McNemar p = {r['p_exact']:.2f}"])
for model, lw in ex["lowest_level_95"].items():
    lev = ex["detection_by_level"][model]
    low = "; ".join(f"{float(k):.0f} %: {100 * v:.0f}" for k, v in lev.items() if v < 0.95)
    rows.append(["Detection by level, " + model, "–", f"every level ≥ {lw:.0f} % flagged in ≥ 95 % of scans; "
                 f"levels below 95 %: {low or 'none'}"])
for model, v in ex["pure_excluded"]["sample_sensitivity"].items():
    rows.append(["Without pure adulterants, " + model, "–",
                 f"sample sensitivity {100 * v['all']:.1f} % (50 blends) / {100 * v['no_pure']:.1f} % (48 blends)"])
for model in ("PLS-R", "MT-DNN"):
    a, b = ex["pure_excluded"][model]["all"], ex["pure_excluded"][model]["no_pure"]
    rows.append(["Without pure adulterants, " + model, "–", f"slope {a['slope']:.3f} / {b['slope']:.3f}; "
                 f"LOD {a['lod']:.1f} / {b['lod']:.1f} % adulterant"])
rows.append(["PLS-R blank by lot", "–", "; ".join(f"{k}: {v['mean']:.1f} ± {v['sd']:.1f} %"
                                                  for k, v in ex["pls_blank_by_lot"].items())])
rows.append(["PLS-R LOD, lot left out of the blank", "–", "; ".join(f"{k}: {v['lod']:.1f} %"
                                                                   for k, v in ex["pls_lod_leave_lot_out_of_blank"].items())])
table("Table S8 Supplementary analyses (leave-one-lot-out, chemically informative regions; added at review stage).",
      ["Analysis", "Seed", "Result"], rows,
      "Source: results/extra.json (src/s05_extra.py). Each nominal level occurs in one lot only, so detection by "
      "level is confounded with the lot effect (lot T1 holds the 4 % blends).")

# S9 one-class baseline (src/s06_oneclass.py)
oc = json.loads((RESULTS / "oneclass.json").read_text())
rows = []
for key, v in oc["settings"].items():
    s, c = v["sample"], v["scan"]
    rows.append([key.replace("_", ", "), f"{100 * c['sensitivity']:.1f}", f"{100 * c['specificity']:.1f}",
                 f"{100 * s['sensitivity']:.0f}", f"{100 * s['specificity']:.0f}",
                 ", ".join(f"{m['adulterant_pct']:.0f}" for m in s["missed_blends"]) or "none",
                 " / ".join(f"{100 * v['per_lot'][l]['authentic_scans_flagged']:.0f}" for l in ("T1", "T2", "T3", "T4", "T5"))])
table("Table S9 Exploratory one-class baseline: PCA fitted on authentic training scans only, flag when T² or Q exceeds "
      "its limit (leave-one-lot-out, chemically informative regions; added at review stage).",
      ["Setting (components, limit)", "Scan sensitivity (%)", "Scan specificity (%)", "Sample sensitivity (%, 50 blends)",
       "Sample specificity (%, 5 lots)", "Blends missed (% adulterant)", "Authentic scans flagged T1/T2/T3/T4/T5 (%)"], rows,
      "Source: results/oneclass.json. sd3: mean + 3 SD of out-of-fold statistics (leave-one-training-lot-out), the rule "
      "used for the regression routes; p99: 99th percentile; combined: T²/T²₀ + Q/Q₀. The 99 % explained-variance rule "
      "reached the cap of 15 components in every fold.")

# S10 saturation-robust thresholds (src/s07_robust_threshold.py), if complete
_rp = RESULTS / "robust_threshold.json"
if _rp.exists():
    rt = json.loads(_rp.read_text(encoding="utf-8"))
    if not rt["missing_dnn_cv"]:
        pf = pd.DataFrame(rt["per_fold"])
        pooled = {(r["model"], r["rule"]): r for r in rt["pooled"]}
        NAMES = {"orig": "mean + 3 SD (as reported)", "logit": "mean + 3 SD on logit scale", "q99": "99th percentile",
                 "q999": "99.9th percentile", "sample3sd": "mean + 3 SD of sample means"}
        rows = []
        for model in ("MT-DNN-R", "PLS-R"):
            for rule, nm in NAMES.items():
                if (model, rule) not in pooled:
                    continue
                q = pooled[(model, rule)]
                thr = pf[(pf.model == model) & (pf.rule == rule)].groupby("fold").threshold.agg(["min", "max"])
                thr_s = "; ".join(f"{f} {a:.2f}" if abs(a - b) < 5e-3 else f"{f} {a:.2f}–{b:.2f}"
                                  for f, (a, b) in thr.iterrows())
                rng = lambda k: (f"{100 * q[k]:.0f}" if q[k + "_min"] == q[k + "_max"]
                                 else f"{100 * q[k]:.0f} ({100 * q[k + '_min']:.0f}–{100 * q[k + '_max']:.0f})")
                fpl = q["fp_lots_per_seed"]
                fpl = sorted(set(fpl)) if fpl and isinstance(fpl[0], str) else sorted({x for s_ in fpl for x in s_})
                rows.append([model, nm, thr_s, rng("sensitivity"), rng("specificity"), ", ".join(fpl) or "none"])
        table("Table S10 Exploratory: regression-route decisions with alternative threshold rules (leave-one-lot-out, "
              "sample level; MT-DNN-R: mean over five seeds, range in parentheses).",
              ["Route", "Threshold rule", "Threshold by withheld lot (% adulterant)", "Sensitivity (%, 50 blends)",
               "Specificity (%, 5 lots)", "Authentic lots rejected"], rows,
              "Source: results/robust_threshold.json (src/s07_robust_threshold.py). Thresholds are computed from grouped "
              "five-fold cross-validation predictions on the authentic training scans, recomputed with the code of the "
              "main analysis (stored thresholds reproduced within 2 × 10⁻¹⁵). The logit rule is not meaningful for PLS-R, whose "
              "clipped output places many authentic training scans at exactly 0 % adulterant; the sample-mean rule rests "
              "on four authentic training samples.")


_si = RESULTS / "session_indicators.json"
if _si.exists():
    si = json.loads(_si.read_text(encoding="utf-8"))
    NM = {"co2": "CO₂ band, 2340–2370 cm⁻¹ (10⁻³ absorbance)", "water_vapour": "Water-vapour lines, 3600–3900 cm⁻¹ (10⁻⁵ absorbance)"}
    SC = {"co2": 1e3, "water_vapour": 1e5}
    rows = []
    for k, v in si["indicators"].items():
        for lt in si["lots"]:
            rows.append([NM[k] if lt == si["lots"][0] else "", lt,
                         f"{SC[k] * v['authentic_mean'][lt]:.2f} ± {SC[k] * v['authentic_sd'][lt]:.2f}",
                         f"{SC[k] * v['blend_mean'][lt]:.2f}"])
    co, wv = si["indicators"]["co2"], si["indicators"]["water_vapour"]
    table("Table S11 Optical-path indicators by lot (raw absorbance; bands the sample does not produce).",
          ["Indicator", "Lot", "Authentic scans, mean ± SD", "Blends of the lot, mean of sample means"], rows,
          "Source: results/session_indicators.json (src/s08_session.py). CO₂: mean absorbance at 2340–2370 cm⁻¹ minus the "
          "mean of its flanks (2240–2260 and 2400–2420 cm⁻¹); water vapour: SD of the first difference over 3600–3900 cm⁻¹. "
          f"The water-vapour indicator also contains detector noise. "
          f"T1 lies {abs(co['T1_minus_others_in_within_lot_sd']):.1f} (CO₂) and {abs(wv['T1_minus_others_in_within_lot_sd']):.1f} "
          "(water vapour) pooled within-lot SDs below the mean of the other lots; the replicate scans of one sample per lot "
          "are not independent, so these figures are descriptive. The data carry no acquisition dates. The authentic lots "
          "were therefore not all measured under the same optical-path conditions (T1 and T2 low, T3–T5 high), and the "
          "effect of a lot cannot be separated from that of its measurement session. The blends were not necessarily "
          "measured with their own lot: their water-vapour values all lie near those of T1 and T2.")

# S12 preprocessing sensitivity (T-TR4 referee read): SNV over retained regions; fingerprint cut at 700 cm-1
if {"chemsnv", "chem700"} <= set(m[m.scheme == "lolo"].regions):
    ml = pd.read_csv(RESULTS / "metrics_lot.csv")
    VAR = {"chem": "As reported (SNV over 600–4000 cm⁻¹; 600–1800 and 2800–3050 cm⁻¹)",
           "chemsnv": "SNV computed over the retained regions only",
           "chem700": "Fingerprint region cut at 700 cm⁻¹ (ZnSe edge excluded)"}
    rows = []
    for reg, nm in VAR.items():
        for model in ("PLS-DA", "PLS-R", "MT-DNN", "MT-DNN-R"):
            sm = m[(m.scheme == "lolo") & (m.regions == reg) & (m.model == model) & (m.level == "sample")]
            sc = m[(m.scheme == "lolo") & (m.regions == reg) & (m.model == model) & (m.level == "scan")]
            if sm.empty or sc.empty:
                continue
            sm, sc = sm.iloc[0], sc.iloc[0]
            lots = ml[(ml.scheme == "lolo") & (ml.regions == reg) & (ml.model == model)]
            rej = ", ".join(f"{r.fold} ({100 * r.fp_rate_authentic:.0f} %)" for r in lots.itertuples()
                            if r.fp_rate_authentic > 0.5) or "none"
            quant = model in ("PLS-R", "MT-DNN")
            rows.append([nm if model == "PLS-DA" else "", model, f"{100 * sm.sensitivity:.0f}",
                         f"{100 * sm.specificity:.0f}", f"{sc.rmsep_tahini:.2f}" if quant else "", rej])
    table("Table S12 Sensitivity analysis: preprocessing (leave-one-lot-out; MT-DNN: means over five seeds).",
          ["Input", "Route", "Sample sensitivity (%)", "Sample specificity (%)", "Scan RMSEP (% tahini)",
           "Authentic lots with more than half of their scans flagged"], rows,
          "Source: results/metrics.csv and results/metrics_lot.csv (regions chem, chemsnv, chem700; src/s01_run.py, "
          "src/s02_metrics.py).")

OUT.write_text("\n".join(L) + "\n<!-- generated by src/esi_tables.py; do not edit by hand -->\n", encoding="utf-8")
print(OUT.read_text(encoding="utf-8")[:3000])
