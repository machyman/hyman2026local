#!/usr/bin/env python3
"""Figure 3 of hyman2026local: measured against predicted speedup in the AMReX validation (Plan S5).

  python3 fig3_validation.py DATA_DIR --frozen predictions_frozen.csv --evaluation evaluation_s5.json --outdir DIR

Panel (a): predicted speedup against measured speedup. Held-out configurations (filled markers) use the
frozen predictions (analysis plan v1 section 8). Training configurations (open markers) use the
leave-one-configuration-out predictions of the selected pair (section 7), recomputed here with fit.py.
The shaded band is the 10 percent tolerance; the dashed lines mark 20 percent.
Panel (b): held-out relative errors with 95 percent bootstrap intervals from evaluate.py, and their median.

Writes hyman2026local_fig3_validation.pdf and .png to DIR and prints the plotted values and the PNG hash.
Deterministic. Requires NumPy, SciPy (through fit.py) and Matplotlib; scikit-image only for the palette check.
"""
import argparse, csv, hashlib, json, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fit as F   # noqa: E402  (fit.py in the same folder)

INK, INK2, MUTED, GRID, AXIS = "#0b0b0b", "#52514e", "#898781", "#e1e0d9", "#c3c2b7"
C2D, C3D, BAND = "#2a78d6", "#eb6834", "#d9d7cf"     # categorical slots 1 and 2 (validated pair); neutral band
MARK = {"point": "o", "circle": "s", "sphere": "^", "disk": "D", "ball": "D"}
CLASS = {"point": "point", "circle": "curve", "sphere": "surface", "disk": "filled region", "ball": "filled region"}


def loco_predictions(data, kk, ok):
    """Leave-one-configuration-out predicted speedups of the training set for one pair (plan section 7)."""
    train = {c: e for c, e in data.items() if e["meta"]["role"] == "training"}
    out = {}
    for c, e in train.items():
        d = e["meta"]["dim"]
        sub = {k: v for k, v in train.items() if k != c}
        kc, oc = F.fit_pair(kk, ok, sub, d)
        out[c] = (F.measured_S(e), F.predict_config(kk, ok, kc, oc, e)["S"])
    return out


def palette_check():
    """CIEDE2000 between every pair of plotted colours (normal vision); floor 15 for the two data slots."""
    try:
        import numpy as np
        from skimage.color import rgb2lab, deltaE_ciede2000
    except ImportError:
        return "palette check skipped (scikit-image absent)"
    def lab(h):
        return rgb2lab(np.array([[[int(h[i:i + 2], 16) / 255 for i in (1, 3, 5)]]]))[0, 0]
    cols = {"2D": C2D, "3D": C3D, "band": BAND, "white": "#ffffff", "ink2": INK2}
    names = list(cols)
    rows = []
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            rows.append(f"{names[i]}-{names[j]} {float(deltaE_ciede2000(lab(cols[names[i]]), lab(cols[names[j]]))):.1f}")
    return "palette dE2000: " + ", ".join(rows)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("data"); ap.add_argument("--frozen", required=True)
    ap.add_argument("--evaluation", required=True); ap.add_argument("--outdir", default=".")
    a = ap.parse_args()
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.lines import Line2D
    from matplotlib.ticker import FixedLocator, FixedFormatter, NullLocator

    ev = json.load(open(a.evaluation))
    frozen = {r["config"]: r for r in csv.DictReader(open(a.frozen))}
    if hashlib.sha256(open(a.frozen, "rb").read()).hexdigest() != ev["frozen_sha256"]:
        sys.exit("frozen predictions do not match the evaluation's recorded hash")
    kk, ok = ev["model"].split("+")
    data = F.load(F.load_raw(a.data, heldout_timing=True), allow_heldout_timing=True)
    loco = loco_predictions(data, kk, ok)

    plt.rcParams.update({"pdf.fonttype": 42, "font.size": 10, "axes.edgecolor": AXIS, "axes.labelcolor": INK2,
                         "xtick.color": MUTED, "ytick.color": MUTED, "font.family": "DejaVu Sans"})
    fig = plt.figure(figsize=(7.0, 4.0))
    ax = fig.add_axes([0.085, 0.265, 0.354, 0.62])      # square in inches: 0.354 * 7.0 = 0.62 * 4.0
    bx = fig.add_axes([0.632, 0.265, 0.33, 0.62])

    # ---- (a) predicted against measured speedup
    lo, hi = 1.0, 6.5
    xs = [lo, hi]
    ax.fill_between(xs, [0.9 * x for x in xs], [1.1 * x for x in xs], color=BAND, alpha=0.55, lw=0, zorder=1)
    ax.plot(xs, xs, color=INK2, lw=0.9, zorder=2)
    for f in (0.8, 1.2):
        ax.plot(xs, [f * x for x in xs], color=MUTED, lw=0.8, ls=(0, (3, 2)), zorder=2)
    print(f"Figure 3 (a): pair {kk}+{ok}")
    for c, (S, Sh) in sorted(loco.items()):
        m = data[c]["meta"]; col = C2D if m["dim"] == 2 else C3D
        ax.plot([S], [Sh], MARK[m["feature"]], ms=5.5, mfc="white", mec=col, mew=1.2, zorder=3)
        print(f"   training {c:16s} S {S:.4f}  S_hat(LOO) {Sh:.4f}  e {abs(Sh - S) / S:.4f}")
    for c, v in sorted(ev["heldout"].items()):
        m = data[c]["meta"]; col = C2D if m["dim"] == 2 else C3D
        assert abs(float(frozen[c]["S_hat"]) - v["S_hat"]) < 1e-12
        ax.plot([v["S"]], [v["S_hat"]], MARK[m["feature"]], ms=6.0, color=col, mec="white", mew=0.7, zorder=4)
        print(f"   held out {c:16s} S {v['S']:.4f}  S_hat(frozen) {v['S_hat']:.4f}  e {v['e']:.4f}")
    ax.set_xscale("log"); ax.set_yscale("log")
    ax.set_xlim(lo, hi); ax.set_ylim(lo, hi)
    ticks = [1, 1.5, 2, 3, 4, 6]
    for axis in (ax.xaxis, ax.yaxis):
        axis.set_major_locator(FixedLocator(ticks)); axis.set_major_formatter(FixedFormatter([f"{t:g}" for t in ticks]))
        axis.set_minor_locator(NullLocator())
    ax.grid(True, which="major", color=GRID, lw=0.6, zorder=0); ax.set_axisbelow(True)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.set_xlabel(r"measured speedup $S=T_G/T_L$")
    ax.set_ylabel(r"predicted speedup $\hat S$")
    ax.set_title("(a) prediction against measurement", color=INK, fontsize=10.5, loc="left")

    # ---- (b) held-out errors with 95% bootstrap intervals
    order = sorted(ev["heldout"], key=lambda c: (data[c]["meta"]["dim"], data[c]["meta"]["feature"], data[c]["meta"]["L"]))
    ys = list(range(len(order), 0, -1))
    for y, c in zip(ys, order):
        v = ev["heldout"][c]; m = data[c]["meta"]; col = C2D if m["dim"] == 2 else C3D
        bx.hlines(y, v["e_ci95"][0], v["e_ci95"][1], color=col, lw=1.6, zorder=3)
        bx.plot([v["e"]], [y], MARK[m["feature"]], ms=6.0, color=col, mec="white", mew=0.7, zorder=4)
    ym = 0
    mci = ev["median_error_ci95"]
    bx.hlines(ym, mci[0], mci[1], color=INK, lw=1.6, zorder=3)
    bx.plot([ev["median_error"]], [ym], "o", ms=6.0, color=INK, mec="white", mew=0.7, zorder=4)
    bx.axhline(0.5, color=AXIS, lw=0.6, zorder=1)
    bx.axvline(0.10, color=INK2, lw=1.0, ls=(0, (4, 2)), zorder=2)
    bx.axvline(0.20, color=MUTED, lw=0.9, ls=(0, (1, 2)), zorder=2)
    top = len(order) + 1.75
    bx.text(0.104, top, "tolerance\non the median", fontsize=8, color=INK2, va="top", ha="left")
    bx.text(0.204, top, "miss to\nexplain", fontsize=8, color=MUTED, va="top", ha="left")
    labels = [f"{data[c]['meta']['dim']}D {c.split('_')[1]}, $L={data[c]['meta']['L']}$" for c in order] + ["median of 7"]
    bx.set_yticks(ys + [ym]); bx.set_yticklabels(labels, fontsize=8.5, color=INK2)
    bx.tick_params(axis="y", length=0)
    bx.set_ylim(-0.7, top + 0.15)
    bx.set_xlim(0, 0.25)
    bx.set_xticks([0, 0.05, 0.10, 0.15, 0.20, 0.25])
    bx.set_xticklabels(["0", "0.05", "0.10", "0.15", "0.20", "0.25"])
    bx.grid(True, axis="x", which="major", color=GRID, lw=0.6, zorder=0); bx.set_axisbelow(True)
    for s in ("top", "right", "left"):
        bx.spines[s].set_visible(False)
    bx.set_xlabel(r"held-out error $|\hat S-S|/S$")
    bx.set_title("(b) held-out error, 95% interval", color=INK, fontsize=10.5, loc="left")

    from matplotlib.patches import Patch
    handles = [Line2D([], [], ls="", marker="s", ms=6.0, color=INK2, mec="white", label="curve, held out (frozen)"),
               Line2D([], [], ls="", marker="^", ms=6.0, color=INK2, mec="white", label="surface, held out (frozen)"),
               Line2D([], [], ls="", marker="o", ms=5.5, mfc="white", mec=INK2, mew=1.2, label="point, training (leave-one-out)"),
               Line2D([], [], ls="", marker="D", ms=5.0, mfc="white", mec=INK2, mew=1.2, label="filled region, training (leave-one-out)"),
               Line2D([], [], color=C2D, lw=3, label="2D"), Line2D([], [], color=C3D, lw=3, label="3D"),
               Patch(color=BAND, alpha=0.55, lw=0, label="within 10% of measured"),
               Line2D([], [], color=MUTED, lw=0.8, ls=(0, (3, 2)), label="20% from measured")]
    fig.legend(handles=handles, loc="lower center", bbox_to_anchor=(0.5, 0.0), ncol=4, frameon=False, fontsize=8,
               labelcolor=INK2, handlelength=1.4, columnspacing=1.1, labelspacing=0.45)

    os.makedirs(a.outdir, exist_ok=True)
    print(f"   median held-out error {ev['median_error']:.4f} (95% CI {mci[0]:.4f} to {mci[1]:.4f})")
    print("   " + palette_check())
    for ext in ("pdf", "png"):
        p = os.path.join(a.outdir, f"hyman2026local_fig3_validation.{ext}")
        fig.savefig(p, dpi=300, metadata={"CreationDate": None} if ext == "pdf" else None)
        if ext == "png":
            print(f"   sha256 {os.path.basename(p)} {hashlib.sha256(open(p, 'rb').read()).hexdigest()}")
    plt.close(fig)


if __name__ == "__main__":
    main()
