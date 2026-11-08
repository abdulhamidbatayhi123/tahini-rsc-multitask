"""Fig. 2. Workflow: data and validation units -> preprocessing -> two model families -> two decision
routes -> outputs. Drawn in code; check() asserts that no text leaves its box or overlaps another box."""
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

from figstyle import DOUBLE, plt, save

W, H = DOUBLE, 6.4 / 2.54
fig = plt.figure(figsize=(W, H))
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, 171)
ax.set_ylim(0, 64)
ax.axis("off")
BOXES = []


def box(x, y, w, h, title, lines=(), fill="#FFFFFF", bold=True):
    p = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.4,rounding_size=1.5", lw=0.7, ec="#000000", fc=fill)
    ax.add_patch(p)
    t = ax.text(x + w / 2, y + h - 2.2, title, ha="center", va="top", fontsize=7,
                fontweight="bold" if bold else "normal")
    texts = [t]
    for i, ln in enumerate(lines):
        texts.append(ax.text(x + 2, y + h - 7.0 - 4.0 * i, ln, ha="left", va="top", fontsize=6.2))
    BOXES.append(((x, y, w, h), texts))


def arrow(x0, y0, x1, y1):
    ax.add_patch(FancyArrowPatch((x0, y0), (x1, y1), arrowstyle="-|>", mutation_scale=7, lw=0.7, color="#000000"))


box(1, 34, 36, 29, "ATR–FTIR data", ["1554 spectra, 55 samples", "5 authentic lots (T1–T5)", "50 blends: sunflower or",
                                       "peanut paste, 4–100 %", "14–151 scans per sample"])
box(1, 1, 36, 29, "Validation", ["Unit: physical sample", "Grouped 70/30 hold-out", "Leave-one-lot-out (5 folds)",
                                   "Selection nested in", "every training set"], fill="#F2F2F2")
box(43, 34, 30, 29, "Preprocessing", ["SNV per spectrum", "Keep 600–1800 and", "2800–3050 cm$^{-1}$", "(752 channels)",
                                        "CO$_2$, H$_2$O bands out"])
box(79, 34, 44, 29, "Multitask DNN", ["Dense 128 (ReLU)", "Dropout 0.2", "Dense 64 (ReLU)",
                                        "Head A: sigmoid, P(adulterated)", "Head B: softmax, 3 fractions"],
    fill="#F7E4EF")
box(79, 1, 44, 29, "Chemometric reference", ["PLS-DA (class)", "PLS2 regression", "(tahini, sunflower, peanut)",
                                               "Components by grouped", "5-fold CV"], fill="#F2F2F2")
box(129, 34, 41, 29, "Decision routes", ["Class head (MT-DNN, PLS-DA)", "Regression route (-R):",
                                           "predicted adulterant >", "mean + 3 SD of authentic", "scans in training CV"])
box(129, 1, 41, 29, "Outputs", ["Pure / adulterated", "Adulterant identity", "Tahini, sunflower and",
                                  "peanut fraction (%)", "Detection limit (LOD)"])
arrow(37, 48.5, 43, 48.5)
arrow(73, 48.5, 79, 48.5)
arrow(73, 40, 79, 18)
arrow(123, 48.5, 129, 48.5)
arrow(123, 18, 129, 40)
arrow(149.5, 34, 149.5, 30)
arrow(19, 34, 19, 30)


def check():
    fig.canvas.draw()
    r = fig.canvas.get_renderer()
    inv = ax.transData.inverted()
    rects = [b for b, _ in BOXES]
    for (x, y, w, h), texts in BOXES:
        for t in texts:
            bb = t.get_window_extent(r).transformed(inv)
            assert bb.x0 >= x - 0.3 and bb.x1 <= x + w + 0.3 and bb.y0 >= y - 0.3 and bb.y1 <= y + h + 0.3, \
                f"text leaves box: {t.get_text()!r}"
    for i, a in enumerate(rects):
        for b in rects[i + 1:]:
            ov = not (a[0] + a[2] <= b[0] or b[0] + b[2] <= a[0] or a[1] + a[3] <= b[1] or b[1] + b[3] <= a[1])
            assert not ov, f"boxes overlap {a} {b}"


check()
save(fig, "fig2_workflow", __file__)
