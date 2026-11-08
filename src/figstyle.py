"""One figure style for the paper, built to the RSC Advances artwork rules read live on 2026-11-08
(docs/journal_rules_rsc_advances.md): width 8.3 cm (single) or 17.1 cm (double), height <= 23.3 cm,
TIFF >= 600 dpi (+ vector PDF), Arial 7 pt. Okabe-Ito colours with one fixed meaning each; every series
also differs by marker or line style. save() asserts the rules and writes a provenance file."""
import hashlib
import json
from pathlib import Path

import warnings

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

warnings.filterwarnings("error", message="Glyph")   # a missing glyph fails the build
CM = 1 / 2.54
SINGLE, DOUBLE, MAX_H = 8.3 * CM, 17.1 * CM, 23.3 * CM
FONT_MIN = 6.0
FIG = Path(__file__).resolve().parents[1] / "figures"
FIG.mkdir(exist_ok=True)

# fixed meanings
C = {
    "tahini": "#009E73",      # bluish green
    "sunflower": "#E69F00",   # orange
    "peanut": "#0072B2",      # blue
    "PLS": "#000000",         # black (PLS-DA / PLS-R)
    "MT-DNN": "#CC79A7",      # reddish purple
    "grey": "#7F7F7F",
}
LS = {"tahini": "-", "sunflower": "--", "peanut": ":"}
MK = {"tahini": "o", "sunflower": "s", "peanut": "^", "PLS": "s", "MT-DNN": "o"}

plt.rcParams.update({
    "font.family": "sans-serif", "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans"],
    "font.size": 7, "axes.titlesize": 7, "axes.labelsize": 7, "xtick.labelsize": 6.5, "ytick.labelsize": 6.5,
    "legend.fontsize": 6.5, "axes.linewidth": 0.6, "xtick.major.width": 0.6, "ytick.major.width": 0.6,
    "lines.linewidth": 1.0, "lines.markersize": 3.5, "pdf.fonttype": 42, "ps.fonttype": 42,
    "axes.spines.top": False, "axes.spines.right": False, "legend.frameon": False,
    "savefig.dpi": 600, "figure.dpi": 150,
})


def panel(ax, letter, x=-0.16, y=1.04):
    ax.text(x, y, letter, transform=ax.transAxes, fontsize=8, fontweight="bold", va="bottom", ha="left")


def _sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def save(fig, name, script, inputs=()):
    w, h = fig.get_size_inches()
    assert abs(w - SINGLE) < 0.01 or abs(w - DOUBLE) < 0.01, f"width {w * 2.54:.2f} cm not 8.3/17.1"
    assert h <= MAX_H + 1e-6, f"height {h * 2.54:.2f} cm > 23.3"
    for t in fig.findobj(matplotlib.text.Text):
        if t.get_text().strip() and t.get_visible():
            assert t.get_fontsize() >= FONT_MIN - 1e-6, f"font {t.get_fontsize()} < {FONT_MIN}: {t.get_text()!r}"
            assert matplotlib.colors.to_hex(t.get_color()) in ("#000000", "#ffffff", "#333333"), \
                f"coloured text {t.get_text()!r}"
    fig.savefig(FIG / f"{name}.pdf")
    fig.savefig(FIG / f"{name}.tif", dpi=600, pil_kwargs={"compression": "tiff_lzw"})
    fig.savefig(FIG / f"{name}.png", dpi=200)
    prov = {"figure": name, "width_cm": round(w * 2.54, 2), "height_cm": round(h * 2.54, 2),
            "script": Path(script).name, "script_sha256": _sha(script), "figstyle_sha256": _sha(__file__),
            "inputs_sha256": {Path(p).name: _sha(p) for p in inputs}}
    (FIG / f"{name}.provenance.json").write_text(json.dumps(prov, indent=2))
    plt.close(fig)
