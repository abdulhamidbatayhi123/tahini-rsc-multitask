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
rows = []
for k in ("T1", "T2", "T3", "T4", "T5"):
    v = dep[k]
    o = v["observed"]
    rows.append([k, f"{v['rms_d']:.2f}", "; ".join(f"{b[0]} ({b[1]:+.1f})" for b in v["top_bands"]),
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

# S6 full-range sensitivity, if available
m = pd.read_csv(RESULTS / "metrics.csv")
full = m[(m.regions == "full")]
if not full.empty:
    rows = []
    for (s, model), r in m[(m.level == "scan")].set_index(["scheme", "model"]).sort_index().iterrows():
        pass
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
    table("Table S6 Sensitivity analysis: chemically informative regions (752 channels) / full 600–4000 cm⁻¹ range "
          "(scan level).", ["Validation", "Route", "Sensitivity (%)", "Specificity (%)", "RMSEP (% tahini)"], rows,
          "Source: results/metrics.csv (regions chem and full).")

OUT.write_text("\n".join(L) + "\n<!-- generated by src/esi_tables.py; do not edit by hand -->\n", encoding="utf-8")
print(OUT.read_text(encoding="utf-8")[:3000])
