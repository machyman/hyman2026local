#!/usr/bin/env python3
"""Reproduce every number, table and figure in
"When Is Local Time Stepping Worthwhile? A Cost Analysis for Nested Adaptive Mesh Refinement"
(J. M. Hyman, manuscript hyman2026local v1_7_0; equation numbers unchanged since v1_3_0).

Sections
  A  Exact checks of the two-level and multilevel identities, the bounded-ratio corollary,
     the normalization invariance, the one-run test and the capped time ratio (rational arithmetic).
  B  Table 1: fine-cell fraction and ideal speedup at a fixed refined volume (p = 1/20, r = 4).
  C  Two-level overhead example quoted in Section 2 (r = 4, f = 1/10 and 9/10, h = 1/2).
  D  Tables 2 and 3: ideal speedup and overhead budget by feature dimension, ratio and counting
     convention (a = 1: every cell of a level advanced; a = 1 - r^(delta-d): uncovered cells only).
  E  Table 4: explicit cell counts for synthetic feature-following hierarchies in 3D, with the
     uncovered-cell budget, the grid-aligned circle to L = 11, and band and ratio sensitivity.
  F  Printed Figure 2 (file hyman2026local_fig1_budget): overhead budget beta_L versus the number of refined levels.
  G  Printed Figure 1 (file hyman2026local_fig2_dimension): deep-hierarchy budget against the feature dimension delta, with the overhead
     fractions implied by published local-time-stepping measurements.
  H  Overhead fractions H/W_glob = 1/S_achieved - 1/S_theory from published speedup pairs.
  I  Synchronization phases per coarse step for fused and per-level global stepping.

Usage:  python3 hyman2026local_reproduce.py [--outdir DIR] [--no-figure]
Requires Python >= 3.9 and NumPy; Matplotlib for Figures 1 and 2. Deterministic: no random numbers.
"""
import argparse, hashlib, itertools, os, platform, sys
from fractions import Fraction as F
import numpy as np

# ---------------------------------------------------------------- formulas
# Equation numbers refer to manuscript v1_7_0 (labels in brackets; unchanged since v1_3_0).
def speedup_two_level(r, f, h):
    """S = W_G / W_L = r / (1 + (r-1) f + h), Eq. (3) [eq:speed]."""
    return F(r) / (1 + (r - 1) * f + h)

def budget_two_level(r, f):
    """beta = 1 - 1/S_ideal = (1 - 1/r)(1 - f), Eq. (4) [eq:budget]."""
    return (1 - F(1, r)) * (1 - f)

def speedup_multilevel(N, C, q, Q):
    """Ideal multilevel speedup W_G / (W_L - H), from Eq. (5) [eq:multiwork]."""
    return F(Q * sum(c * n for c, n in zip(C, N)), sum(qq * c * n for qq, c, n in zip(q, C, N)))

def speedup_geometric(r, rho, L, a=F(1)):
    """S_L for N_l = N_L rho^(l-L), l = 0..L, with all finest-level cells and a fraction a of each
    coarser level advanced, uniform cost, q_l = r^l, Eq. (9) [eq:SL]."""
    num = 1 + a * sum(F(1) / F(rho) ** j for j in range(1, L + 1))
    den = 1 + a * sum(F(1) / F(r * rho) ** j for j in range(1, L + 1))
    return num / den

def leaf_fraction(r, delta, d):
    """a = 1 - r^(delta-d): fraction of a level's cells left uncovered by the next level."""
    return 1 - F(r ** delta, r ** d)

def speedup_limit(r, delta, a=F(1)):
    """S_inf = [1 + a/(rho-1)] / [1 + a/(r rho - 1)] for delta > 0, Eq. (10) [eq:Sinf]."""
    rho = r ** delta
    return (1 + a / F(rho - 1)) / (1 + a / F(r * rho - 1))

def budget_limit(r, delta, a=F(1)):
    """beta_inf = a (r-1) rho / [(rho - 1 + a)(r rho - 1)], Eq. (10) [eq:Sinf]."""
    rho = r ** delta
    return a * (r - 1) * rho / ((rho - 1 + a) * (r * rho - 1))

# ---------------------------------------------------------------- A: exact checks
def section_A(out):
    n = 0
    for r in (2, 3, 4, 8):
        for nc in (1, 9, 100):
            for nf in (1, 2, 400):
                for H in (0, 1, 10, 1000):
                    WG = r * (nc + nf); WL = nc + r * nf + H          # C = 1
                    assert (WL < WG) == (H < (r - 1) * nc)            # Proposition 1
                    f = F(nf, nc + nf); h = F(H, nc + nf)
                    assert F(WG, WL) == speedup_two_level(r, f, h)    # Eq. (3)
                    beta = budget_two_level(r, f)
                    assert (WL < WG) == (F(H, WG) < beta)             # Eq. (4)
                    n += 1
    # multilevel identity, Eqs. (5)-(6), with unequal costs and an irregular schedule
    for N, Cc, q in (([5, 7, 11], [1, 2, 3], [1, 2, 6]), ([100, 40, 40, 40], [1, 1, 1, 1], [1, 2, 4, 8])):
        Q = q[-1]
        for H in (0, 3, 50, 10**4):
            WG = Q * sum(c * x for c, x in zip(Cc, N)); WL = sum(a * c * x for a, c, x in zip(q, Cc, N)) + H
            assert (WL < WG) == (H < sum((Q - a) * c * x for a, c, x in zip(q, Cc, N)))
            n += 1
    # geometric hierarchy: closed forms, monotonicity, weighted-average bound
    for r in (2, 3, 4):
        for delta in (0, 1, 2, 3):
            rho = r ** delta
            vals = [speedup_geometric(r, rho, L) for L in range(0, 16)]
            assert all(vals[i + 1] > vals[i] for i in range(15))
            assert all(1 <= v <= r ** L for L, v in enumerate(vals))
            if delta == 0:
                for L, v in enumerate(vals):
                    assert v == F(L + 1) * (1 - F(1, r)) / (1 - F(1, r) ** (L + 1))   # Eq. (11), a = 1
            else:
                lim = speedup_limit(r, delta)
                assert lim == F(r * rho - 1, r * (rho - 1)) == 1 + F(r - 1, r * (r ** delta - 1))
                assert 1 - 1 / lim == budget_limit(r, delta) == F(r - 1, r ** (delta + 1) - 1)
                assert all(v < lim for v in vals) and abs(float(lim - vals[-1])) < 1e-3
            n += 1
    # generalized Proposition 2 (fraction a of coarser levels advanced) against explicit counting
    for r in (2, 4):
        for d in (1, 2, 3):
            for delta in range(0, d + 1):
                rho, a, L = r ** delta, leaf_fraction(r, delta, d), 30
                N = [F(rho) ** l for l in range(L + 1)]
                M = [N[l] - N[l + 1] / r ** d for l in range(L)] + [N[L]]       # uncovered cells only
                assert speedup_multilevel(M, [1] * (L + 1), [r ** l for l in range(L + 1)], r ** L) \
                    == speedup_geometric(r, rho, L, a)
                if delta == 0 and a > 0:                                         # Eq. (11), general a
                    for LL in range(0, 12):
                        assert speedup_geometric(r, 1, LL, a) == (1 + a * LL) / (1 + a * (1 - F(1, r) ** LL) / (r - 1))
                if delta > 0 and a > 0:
                    lim = speedup_limit(r, delta, a)
                    assert 1 - 1 / lim == budget_limit(r, delta, a)
                n += 1
    # extra cells on level 0 raise S_L (each adds r^L to W_G and 1 to W_L)
    for r, delta in ((2, 1), (2, 2), (4, 2)):
        rho, L = r ** delta, 5
        N = [F(rho) ** l for l in range(L + 1)]
        base = speedup_multilevel(N, [1] * (L + 1), [r ** l for l in range(L + 1)], r ** L)
        for extra in (1, 10, 1000):
            N2 = [N[0] + extra] + N[1:]
            assert speedup_multilevel(N2, [1] * (L + 1), [r ** l for l in range(L + 1)], r ** L) > base
        n += 1
    # normalization invariance: H/W_glob < beta  <=>  H/W_sub < beta (W_sub includes H)
    for beta in (F(1, 85), F(1, 21), F(1, 7), F(1, 2)):
        for x in (F(0), F(1, 1000), beta / 2, beta, 2 * beta, F(1, 3)):
            y = x / (1 - beta + x)
            assert (x < beta) == (y < beta)
            n += 1
    # one-run sufficient test: kernel time K = W_sub - H, non-kernel time O >= H  =>  O < (S_ideal - 1) K implies W_sub < W_glob
    for Wg, K in ((100, 60), (100, 90), (100, 99)):
        S_id = F(Wg, K)
        for H in range(0, 50):
            for O in (H, H + 1, H + 5):
                if O < (S_id - 1) * K:
                    assert K + H < Wg
                n += 1
    # capped time ratio r_t <= r: S_inf = [1 + a/(rho-1)] / [1 + a/(r_t rho - 1)], rho = r^delta in space
    for r, rt in ((4, 2), (4, 3), (2, 1), (8, 2)):
        for delta in (1, 2, 3):
            rho = F(r) ** delta
            for a in (F(1), F(1, 2)):
                L = 60
                Mx = [rho ** l for l in range(L + 1)]
                adv = [a * x for x in Mx[:-1]] + [Mx[-1]]
                S = F(rt) ** L * sum(adv) / sum(F(rt) ** l * adv[l] for l in range(L + 1))
                lim = (1 + a / (rho - 1)) / (1 + a / (rt * rho - 1))
                assert abs(float(S - lim)) < 1e-12
                if a == 1:
                    assert 1 - 1 / lim == F(rt - 1, rt * rho - 1)
                n += 1
    # bounded-ratio corollary: k1 rho^l <= M_l <= k2 rho^l  =>  (S_L - 1)/(S_L^geo - 1) in [1/kappa, kappa]
    for r, delta in ((2, 1), (2, 2), (4, 1)):
        rho = F(r) ** delta
        for pattern in ((1, 2), (2, 1, 1), (1, 1, 3, 2), (3, 1)):
            L = 8
            w = [F(pattern[l % len(pattern)]) for l in range(L + 1)]
            kappa = max(w) / min(w)
            for a in (F(1), F(1, 2)):
                M = [w[l] * rho ** l for l in range(L + 1)]
                geo = [rho ** l for l in range(L + 1)]
                def S_of(Mv):
                    adv = [a * x for x in Mv[:-1]] + [Mv[-1]]
                    return F(r) ** L * sum(adv) / sum(F(r) ** l * adv[l] for l in range(L + 1))
                ratio = (S_of(M) - 1) / (S_of(geo) - 1)
                assert 1 / kappa <= ratio <= kappa
                n += 1
    print(f"A  EXACT-CHECK PASS ({n} cases)", file=out)

# ---------------------------------------------------------------- B: Table 1
def section_B(out):
    r, p = 4, F(1, 20)
    print("B  Table 1: fixed refined volume p = 1/20, r = 4 (H = 0)", file=out)
    rows = []
    for d in (1, 2, 3):
        f = p * r ** d / (1 - p + p * r ** d)
        S = speedup_two_level(r, f, 0)
        rows.append((d, f, S))
        print(f"   d={d}  f_d={float(f):.4f}  S_ideal={float(S):.4f}  beta={float(1 - 1/S):.4f}", file=out)
    return rows

# ---------------------------------------------------------------- C: two-level example
def section_C(out):
    r = 4
    print("C  Two-level example, r = 4", file=out)
    for f in (F(1, 10), F(1, 2), F(9, 10)):
        S0 = speedup_two_level(r, f, 0); Sh = speedup_two_level(r, f, F(1, 2))
        print(f"   f={float(f):.2f}  S_ideal={float(S0):.4f}  beta={float(budget_two_level(r, f)):.4f}"
              f"  S(h=0.1)={float(speedup_two_level(r, f, F(1, 10))):.4f}  S(h=0.5)={float(Sh):.4f}"
              f"  H/W_G at h=0.5: {float(F(1, 2) / r):.4f}", file=out)

# ---------------------------------------------------------------- D: Tables 2 and 3
def section_D(out):
    print("D  Table 2: S and beta with all cells advanced (a = 1); beta with uncovered cells only, d = 3", file=out)
    for r in (2, 4):
        for delta in (1, 2, 3):
            S = speedup_limit(r, delta); b = budget_limit(r, delta)
            a3 = leaf_fraction(r, delta, 3)
            bl = budget_limit(r, delta, a3) if a3 > 0 else F(0)
            print(f"   r={r} delta={delta}  S_inf={S} = {float(S):.4f}   beta_inf={b} = {float(b):.4f}"
                  f"   leaf d=3: a={a3}, beta_inf={bl} = {float(bl):.4f}", file=out)
        for L in (3, 7):
            S = speedup_geometric(r, 1, L); a3 = leaf_fraction(r, 0, 3); Sl = speedup_geometric(r, 1, L, a3)
            print(f"   r={r} delta=0  L={L}  S_L={float(S):.4f}  beta_L={float(1 - 1/S):.4f}"
                  f"   leaf d=3: S_L={float(Sl):.4f} beta_L={float(1 - 1/Sl):.4f}", file=out)
    print("   Table 3: per-level gain for a point, uncovered cells only: a(r-1)/(r-1+a)", file=out)
    for r in (2, 4):
        print(f"   r={r}: " + "  ".join(f"d={d}: {leaf_fraction(r,0,d)*(r-1)/(r-1+leaf_fraction(r,0,d))}" for d in (1, 2, 3)), file=out)
    print("   Table 3: leaf budgets for a curve in d = 2 and d = 3: " + "  ".join(
        f"r={r},d={d}: {budget_limit(r, 1, leaf_fraction(r, 1, d))}" for r in (2, 4) for d in (2, 3)), file=out)
    print("   capped time ratio r_t < r (rho = r^delta in space), a = 1: beta_inf = (r_t - 1)/(r_t rho - 1)", file=out)
    for r, rt in ((4, 2), (2, 1)):
        print(f"   r={r} r_t={rt}: " + "  ".join(f"delta={dl}: {F(rt - 1, rt * r ** dl - 1)}" for dl in (1, 2, 3)), file=out)
    # how quickly the limit is reached (relative gap of beta_L to beta_inf, a = 1)
    for r in (2, 4):
        for delta in (1, 2, 3):
            lim = budget_limit(r, delta)
            gaps = [float((lim - (1 - 1 / speedup_geometric(r, r ** delta, L))) / lim) for L in range(1, 9)]
            print(f"   r={r} delta={delta}  relative gap (beta_inf - beta_L)/beta_inf, L=1..8: " + " ".join(f"{g:.1e}" for g in gaps), file=out)

# ---------------------------------------------------------------- E: synthetic hierarchies
CENTER = np.array([0.5123, 0.4871, 0.5037])   # off-center so no feature passes through grid nodes
RADIUS = 0.3
TILT = 0.37                                     # radians; tilts the circle out of the grid planes

def distance(kind, x):
    v = x - CENTER
    if kind == "point":
        return np.sqrt((v ** 2).sum(1))
    if kind == "circle":                        # circle of radius RADIUS in the grid-parallel plane z = CENTER[2]
        rr = np.sqrt(v[:, 0] ** 2 + v[:, 1] ** 2)
        return np.sqrt((rr - RADIUS) ** 2 + v[:, 2] ** 2)
    if kind == "circle_tilted":                 # same circle, its plane rotated by TILT about the x-axis
        c, s = np.cos(TILT), np.sin(TILT)
        y = c * v[:, 1] + s * v[:, 2]; z = -s * v[:, 1] + c * v[:, 2]
        rr = np.sqrt(v[:, 0] ** 2 + y ** 2)
        return np.sqrt((rr - RADIUS) ** 2 + z ** 2)
    if kind == "sphere":
        return np.abs(np.sqrt((v ** 2).sum(1)) - RADIUS)
    if kind == "ball":
        return np.maximum(np.sqrt((v ** 2).sum(1)) - RADIUS, 0.0)
    raise ValueError(kind)

def hierarchy_counts(kind, n0=16, L=5, band=2.0, r=2):
    """Cells held per level, M_l, when level l+1 consists of the r^3 children of every level-l cell
    whose center lies within band * dx_l of the feature (distance <= band * dx_l), in the unit cube."""
    child = np.array(list(itertools.product(range(r), repeat=3)), dtype=np.int64)
    idx = np.array(list(itertools.product(range(n0), repeat=3)), dtype=np.int64)
    counts, n = [len(idx)], n0
    for lev in range(L):
        tagged = idx[distance(kind, (idx + 0.5) / n) <= band / n]
        counts.append(r ** 3 * len(tagged))
        if lev < L - 1:
            idx = (r * tagged[:, None, :] + child[None, :, :]).reshape(-1, 3)
        n *= r
    return counts

def speedup_counts(M, r=2, uncovered=False):
    """Ideal speedup from held counts M_0..M_L (uniform cost, q_l = r^l). With uncovered=True only
    cells not covered by the next level are advanced on levels l < L (M_l - M_{l+1}/r^3)."""
    L = len(M) - 1
    N = [M[l] - F(M[l + 1], r ** 3) for l in range(L)] + [M[L]] if uncovered else M
    return speedup_multilevel(N, [1] * (L + 1), [r ** l for l in range(L + 1)], r ** L)

def section_E(out):
    print("E  Table 4: synthetic 3D hierarchies, base 16^3, r = 2, band = 2 cells, L = 5 (circle tilted by TILT)", file=out)
    rows = []
    for kind, delta in (("point", 0), ("circle_tilted", 1), ("sphere", 2), ("ball", 3)):
        M = hierarchy_counts(kind)
        L = len(M) - 1
        S_counts = speedup_counts(M)
        S_model = speedup_geometric(2, 2 ** delta, L)
        bu = 1 - 1 / speedup_counts(M, uncovered=True)
        mean_growth = (M[L] / M[1]) ** (1 / (L - 1))
        last = M[L] / M[L - 1]
        seq = [speedup_counts(M[:k + 1]) for k in range(1, L + 1)]
        rows.append((kind, delta, M, mean_growth, last, S_counts, S_model, bu))
        print(f"   {kind:13s} S_L from counts, L=1..5: " + " ".join(f"{float(x):.4f}" for x in seq)
              + "   beta_L: " + " ".join(f"{float(1 - 1/x):.4f}" for x in seq), file=out)
        print(f"   {kind:13s} delta={delta}  M={M}  mean growth (M5/M1)^(1/4)={mean_growth:.3f}"
              f"  last M5/M4={last:.3f}  r^delta={2**delta}  S5(counts)={float(S_counts):.4f}"
              f"  S5(geometric model)={float(S_model):.4f}  beta_u(counts, L=5)={float(bu):.4f}"
              + ("" if delta == 0 else f"  S_inf={float(speedup_limit(2, delta)):.4f}"
                 f"  beta_u,inf={float(budget_limit(2, delta, leaf_fraction(2, delta, 3))):.4f}"), file=out)
    for kind in ("circle", "circle_tilted"):
        M = hierarchy_counts(kind, L=11)
        seq = [speedup_counts(M[:k + 1]) for k in range(1, 12)]
        geo = [M[l] / (M[1] * 2 ** (l - 1)) for l in range(1, 12)]
        print(f"   {kind:13s} L=1..11 ratios: " + " ".join(f"{M[l]/M[l-1]:.3f}" for l in range(2, 12))
              + "   S_L: " + " ".join(f"{float(x):.4f}" for x in seq)
              + f"   min/max S_L for L>=5: {min(float(x) for x in seq[4:]):.4f}/{max(float(x) for x in seq[4:]):.4f}"
              + f"   kappa(levels 1..11)={max(geo)/min(geo):.4f}", file=out)
    for kind in ("point", "circle_tilted", "sphere", "ball"):
        M = hierarchy_counts(kind, band=3.0)
        print(f"   band=3 {kind:13s} M={M}  mean growth={(M[5]/M[1])**0.25:.3f}", file=out)
    M = hierarchy_counts("circle_tilted", L=3, r=4)
    print(f"   r=4 circle_tilted L=3  M={M}  growth M2/M1={M[2]/M[1]:.3f} M3/M2={M[3]/M[2]:.3f}  r^delta=4"
          f"  S3(counts)={float(speedup_counts(M, r=4)):.4f}  S_inf={float(speedup_limit(4, 1)):.4f}", file=out)
    return rows

# ---------------------------------------------------------------- F: printed Figure 2
def section_F(outdir, out):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.ticker import FixedLocator, FixedFormatter, NullLocator
    ink, ink2, muted, grid, axis = "#0b0b0b", "#52514e", "#898781", "#e1e0d9", "#c3c2b7"
    colors = ["#2a78d6", "#eb6834", "#1baf7a", "#4a3aa7"]          # categorical slots 1, 2, 3, 7; all pairs validated
    # (v1_3_1: slot 4 #eda100 failed the all-pairs normal-vision floor against slot 2, dE 13.7 < 15; SA-6)
    markers = ["o", "s", "^", "D"]
    names = ["point", "curve", "surface", "filled region"]
    plt.rcParams.update({"pdf.fonttype": 42, "font.size": 10, "axes.edgecolor": axis, "axes.labelcolor": ink2,
                         "xtick.color": muted, "ytick.color": muted, "font.family": "DejaVu Sans"})
    Ls = np.arange(1, 9)
    fig, axes = plt.subplots(1, 2, figsize=(7.0, 3.3), sharey=True)
    yt = [0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1.0]
    for ax, r in zip(axes, (2, 4)):
        for k, delta in enumerate((0, 1, 2, 3)):
            beta = [float(1 - 1 / speedup_geometric(r, r ** delta, int(L))) for L in Ls]
            ax.plot(Ls, beta, color=colors[k], lw=1.6, marker=markers[k], ms=5.5,
                    mec="white", mew=0.8, label=rf"$\delta={delta}$ ({names[k]})", zorder=3)
            if delta > 0:
                lim = budget_limit(r, delta)
                ax.hlines(float(lim), 0.6, 8.15, color=colors[k], lw=0.8, ls=(0, (2, 2)), alpha=0.8, zorder=2)
                ax.text(8.35, float(lim), f"{lim.numerator}/{lim.denominator}", color=ink2,
                        va="center", ha="left", fontsize=9)
        ax.set_yscale("log")
        ax.set_ylim(0.008, 1.05)
        ax.yaxis.set_major_locator(FixedLocator(yt))
        ax.yaxis.set_major_formatter(FixedFormatter([f"{v:g}" for v in yt]))
        ax.yaxis.set_minor_locator(NullLocator())
        ax.set_xlim(0.6, 9.4)
        ax.set_xticks(range(1, 9))
        ax.grid(True, which="major", color=grid, lw=0.6, zorder=0)
        ax.set_axisbelow(True)
        for s in ("top", "right"):
            ax.spines[s].set_visible(False)
        ax.set_title(rf"refinement ratio $r={r}$", color=ink, fontsize=10.5, loc="left")
        ax.set_xlabel(r"number of refined levels $L$")
    axes[0].set_ylabel(r"overhead budget $\beta_L = 1 - 1/S_L$")
    axes[0].legend(loc="lower left", bbox_to_anchor=(0.0, 0.0), frameon=False, fontsize=9,
                   handlelength=1.6, labelcolor=ink2, ncol=2, columnspacing=0.8)
    fig.tight_layout(w_pad=2.2)
    paths = []
    for ext in ("pdf", "png"):
        p = os.path.join(outdir, f"hyman2026local_fig1_budget.{ext}")
        fig.savefig(p, dpi=300, metadata={"CreationDate": None} if ext == "pdf" else None)
        paths.append(p)
    plt.close(fig)
    print("F  Figure 2 (budget against depth) written: " + ", ".join(os.path.basename(p) for p in paths), file=out)
    return paths

# ---------------------------------------------------------------- H: overhead fractions
# Published (theoretical, achieved) speedup pairs, typed from the sources (VER 2026-10-08):
#   Breuer & Heinecke (IPDPS 2022, Sec. VII-B): 2.14 achieved = 94% of theoretical 2.28 (Table I); 6.0 achieved of
#   theoretical 6.3 (LOH.3 accuracy run, Sec. VII-B a; relabelled in v1_4_0 after the S6 VER role pass, finding L2).
#   Seny et al. (JCP 2014, Sec. 5.3): theoretical 10.932, achieved 10.457.
#   Fernando & Sundar (SISC 2022, Table 2): estimated/reported 3.31/3.30, 3.31/2.87, 3.49/3.12, 3.56/3.21.
PUBLISHED_PAIRS = [("Breuer-Heinecke Table I", 2.28, 2.14), ("Breuer-Heinecke accuracy", 6.3, 6.0),
                   ("Seny et al. turbofan", 10.932, 10.457),
                   ("Fernando-Sundar d=9", 3.31, 3.30), ("Fernando-Sundar d=10", 3.31, 2.87),
                   ("Fernando-Sundar d=11", 3.49, 3.12), ("Fernando-Sundar d=12", 3.56, 3.21)]

def section_H(out):
    """H/W_glob = 1/S_achieved - 1/S_theory, since S_achieved = W_glob/W_sub and S_theory = W_glob/(W_sub - H)."""
    print("H  Overhead fractions implied by published speedup pairs: H/W_glob = 1/S_ach - 1/S_th", file=out)
    vals = []
    for name, sth, sach in PUBLISHED_PAIRS:
        x = 1 / sach - 1 / sth
        vals.append(x)
        print(f"   {name:26s} S_th={sth:<7}  S_ach={sach:<7}  H/W_glob={x:.4f}", file=out)
    print(f"   range {min(vals):.4f} to {max(vals):.4f}; median {sorted(vals)[len(vals)//2]:.4f}", file=out)
    return min(vals), max(vals)

# ---------------------------------------------------------------- I: synchronization phases
def section_I(out):
    print("I  Phases per coarse step: global stepping fused = Q, global per-level = (L+1) Q, subcycling = sum r^l", file=out)
    for r, L in ((2, 3), (2, 5), (4, 3)):
        Q = r ** L; sub = sum(r ** l for l in range(L + 1))
        print(f"   r={r} L={L}: fused {Q}  per-level {(L + 1) * Q}  subcycling {sub}  sub/fused={sub/Q:.3f}"
              f"  limit r/(r-1)={r/(r-1):.3f}", file=out)

# ---------------------------------------------------------------- G: printed Figure 1
# AMReX primary configurations (Section 5; r = 2, every cell advanced): (config, d, delta, L, beta, x = H/K_G),
# copied to four decimals from validation/evaluation_s5.json (SHA-256 d255b29e...), key "secondary".
# Figure 1 marks beta at each delta (Plan G6(a), deviation D2). The label quotes the Section 2 overhead x_C = H_C/K_G with
# one cost per update from global stepping (ruling G8(a)); its range comes from validation/s6_tables.py, section D.
AMREX_XC_RANGE = (-0.422, -0.003)
AMREX_Y_RANGE = (-0.114, 0.191)     # y = 1/S - 1/S_id, the measure used for the published band (s6_tables.py, D)
AMREX_POINTS = [
    ("d2_point_L2_r2", 2, 0, 2, 0.7305, -0.1277), ("d2_point_L3_r2", 2, 0, 3, 0.8439, -0.3054),
    ("d2_point_L4_r2", 2, 0, 4, 0.9029, -0.4395), ("d2_circle_L2_r2", 2, 1, 2, 0.3512, -0.2855),
    ("d2_circle_L3_r2", 2, 1, 3, 0.3871, -0.4247), ("d2_circle_L4_r2", 2, 1, 4, 0.3971, -0.4505),
    ("d2_disk_L2_r2", 2, 2, 2, 0.1794, -0.2142), ("d2_disk_L3_r2", 2, 2, 3, 0.1648, -0.3942),
    ("d2_disk_L4_r2", 2, 2, 4, 0.1529, -0.3331), ("d3_point_L2_r2", 3, 0, 2, 0.6500, -0.0599),
    ("d3_point_L3_r2", 3, 0, 3, 0.6886, -0.1927), ("d3_circle_L2_r2", 3, 1, 2, 0.3042, -0.0918),
    ("d3_circle_L3_r2", 3, 1, 3, 0.3872, -0.1611), ("d3_sphere_L2_r2", 3, 2, 2, 0.1612, -0.0883),
    ("d3_sphere_L3_r2", 3, 2, 3, 0.1961, -0.0980), ("d3_ball_L2_r2", 3, 3, 2, 0.1515, -0.0867),
    ("d3_ball_L3_r2", 3, 3, 3, 0.1313, -0.0977)]


def check_amrex_points(path, out):
    """Confirm AMREX_POINTS against the evaluation file, and AMREX_XC_RANGE against the output of
    validation/s6_tables.py, when they are present (both ship in validation/)."""
    s6 = os.path.join(os.path.dirname(path or "."), "s6_tables_output.txt")
    if os.path.exists(s6):
        import re
        m = re.search(r"x_C ([+-][0-9.]+) to ([+-][0-9.]+)", open(s6).read())
        assert m and (float(m.group(1)), float(m.group(2))) == AMREX_XC_RANGE, f"x_C range disagrees with {s6}"
        m = re.search(r"1/S - 1/S_id: ([+-][0-9.]+) to ([+-][0-9.]+)", open(s6).read())
        assert m and (float(m.group(1)), float(m.group(2))) == AMREX_Y_RANGE, f"y range disagrees with {s6}"
        print(f"G  AMReX x_C range {AMREX_XC_RANGE} agrees with s6_tables_output.txt", file=out)
    if not path or not os.path.exists(path):
        print("G  AMReX points: evaluation file not found; embedded values used", file=out)
        return
    import json
    sec = json.load(open(path))["secondary"]
    bad = [c for c, d, dl, L, b, x in AMREX_POINTS
           if abs(sec[c]["beta"] - b) > 5e-5 or abs(sec[c]["x"] - x) > 5e-5 or sec[c]["delta"] != dl]
    assert not bad and len(sec) == len(AMREX_POINTS), f"AMReX points disagree with {path}: {bad}"
    print(f"G  AMReX points: {len(AMREX_POINTS)} agree with {os.path.basename(path)} to 5e-5; "
          f"beta {min(p[4] for p in AMREX_POINTS):.3f} to {max(p[4] for p in AMREX_POINTS):.3f}, "
          f"x {min(p[5] for p in AMREX_POINTS):.3f} to {max(p[5] for p in AMREX_POINTS):.3f}", file=out)


def section_G(outdir, out, band):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.ticker import FixedLocator, FixedFormatter, NullLocator
    ink, ink2, muted, grid, axis = "#0b0b0b", "#52514e", "#898781", "#e1e0d9", "#c3c2b7"
    c_all, c_unc, c_band = "#2a78d6", "#eb6834", "#d9d7cf"      # categorical slots 1-2 (validated); neutral band
    plt.rcParams.update({"pdf.fonttype": 42, "font.size": 10, "axes.edgecolor": axis, "axes.labelcolor": ink2,
                         "xtick.color": muted, "ytick.color": muted, "font.family": "DejaVu Sans"})
    fig, axes = plt.subplots(1, 2, figsize=(7.0, 4.0), sharey=True)   # S8: legend moved below the panels
    yt = [0.001, 0.003, 0.01, 0.03, 0.1, 0.3, 1.0]
    ds = np.linspace(0.0, 3.0, 301)
    for ax, r in zip(axes, (2, 4)):
        ax.axhspan(band[0], band[1], color=c_band, alpha=0.55, lw=0, zorder=1)
        ax.text(-0.12, band[1] * 0.80, "published LTS overheads\n" + rf"$1/S_{{\rm ach}}-1/S_{{\rm th}}$: {100 * band[0]:.1f} to {100 * band[1]:.1f}%",
                fontsize=8, color=ink2, va="top", ha="left", zorder=2, linespacing=1.2)   # S8: band annotated in both panels
        b_all = [1.0 if d == 0 else (r - 1) / (r ** (d + 1) - 1) for d in ds]
        b_unc = []
        for d in ds:
            rho, a = r ** d, 1 - r ** (d - 3)
            b_unc.append(1.0 if d == 0 else (a * (r - 1) * rho / ((rho - 1 + a) * (r * rho - 1)) if a > 0 else np.nan))
        ax.plot(ds, b_all, color=c_all, lw=2, label="every cell advanced ($a=1$)", zorder=3)
        ax.plot(ds, b_unc, color=c_unc, lw=2, ls=(0, (5, 2)), label="uncovered cells only ($d=3$)", zorder=3)
        for d, name in ((0, "point"), (1, "curve"), (2, "surface"), (3, "filled")):
            y = 1.0 if d == 0 else (r - 1) / (r ** (d + 1) - 1)
            ax.plot([d], [y], "o", ms=6.5, color=c_all, mec="white", mew=1.0, zorder=4)
            # S8: the feature names moved from the plot to the tick labels, clear of the AMReX crosses
        ax.axvline(2.31, color=muted, lw=0.8, ls=(0, (1, 2)), zorder=2)
        ax.text(2.35, 0.75, "turbulent\ninterface", fontsize=8.5, color=ink2, va="top", ha="left")
        if r == 2:   # AMReX finite-depth budgets (Section 5); 2D left of delta, 3D right, deeper further out
            for c, d, dl, L, b, x in AMREX_POINTS:
                xo = dl + (-1 if d == 2 else 1) * (0.05 + 0.04 * (L - 2))
                ax.plot([xo], [b], "+" if d == 2 else "x", ms=8.0, color=ink, mew=1.6, zorder=5)   # S8: larger markers
            ax.plot([], [], "+", ms=8.0, color=ink, mew=1.6, label=r"AMReX budgets $\beta$, 2D ($L=2$ to $4$)")
            ax.plot([], [], "x", ms=8.0, color=ink, mew=1.6, label=r"AMReX budgets $\beta$, 3D ($L=2$, $3$)")
        ax.set_yscale("log"); ax.set_ylim(0.001, 1.9)
        ax.yaxis.set_major_locator(FixedLocator(yt)); ax.yaxis.set_major_formatter(FixedFormatter([f"{v:g}" for v in yt]))
        ax.yaxis.set_minor_locator(NullLocator())
        ax.set_xlim(-0.2, 3.2); ax.set_xticks([0, 1, 2, 3])
        ax.set_xticklabels(["0\npoint", "1\ncurve", "2\nsurface", "3\nfilled"])
        ax.set_xticks([0.5, 1.5, 2.5], minor=True)
        ax.grid(True, which="both", axis="x", color=grid, lw=0.6, zorder=0)
        ax.grid(True, which="major", axis="y", color=grid, lw=0.6, zorder=0); ax.set_axisbelow(True)
        for sp in ("top", "right"):
            ax.spines[sp].set_visible(False)
        ax.set_title(rf"refinement ratio $r={r}$", color=ink, fontsize=10.5, loc="left")
        ax.set_xlabel(r"dimension of the refined feature $\delta$")
    axes[0].set_ylabel(r"deep-hierarchy budget $\beta_\infty$")
    h, lab = axes[0].get_legend_handles_labels()   # S8: legend and AMReX overhead ranges below the panels, outside the band
    fig.legend(h, lab, loc="lower left", bbox_to_anchor=(0.075, 0.0), ncol=2, frameon=False, fontsize=8.5,
               labelcolor=ink2, handlelength=2.2, columnspacing=1.6)
    fig.text(0.075, 0.115, "AMReX overheads (Sec. 5): " + rf"$H/K_G$ from ${AMREX_XC_RANGE[0]:.2f}$ to ${AMREX_XC_RANGE[1]:.3f}$; "
             + rf"$1/S-1/S_{{\rm id}}$ from ${AMREX_Y_RANGE[0]:.2f}$ to ${AMREX_Y_RANGE[1]:.2f}$", fontsize=8.5, color=ink2, ha="left", va="bottom")
    fig.tight_layout(w_pad=2.0, rect=(0, 0.16, 1, 1))
    paths = []
    for ext in ("pdf", "png"):
        pth = os.path.join(outdir, f"hyman2026local_fig2_dimension.{ext}")
        fig.savefig(pth, dpi=300, metadata={"CreationDate": None} if ext == "pdf" else None)
        paths.append(pth)
    plt.close(fig)
    print("G  Figure 1 (budget against dimension) written: " + ", ".join(os.path.basename(p) for p in paths), file=out)
    return paths

# ---------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--outdir", default=".")
    ap.add_argument("--no-figure", action="store_true")
    ap.add_argument("--evaluation", default=os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                         "validation", "evaluation_s5.json"),
                    help="AMReX evaluation file used to confirm the Figure 1 points (optional)")
    a = ap.parse_args()
    os.makedirs(a.outdir, exist_ok=True)
    out = sys.stdout
    print(f"python {platform.python_version()}  numpy {np.__version__}", file=out)
    section_A(out); section_B(out); section_C(out); section_D(out); section_E(out)
    band = section_H(out); section_I(out)
    check_amrex_points(a.evaluation, out)
    if not a.no_figure:
        import matplotlib
        print(f"matplotlib {matplotlib.__version__}", file=out)
        for p in section_F(a.outdir, out) + section_G(a.outdir, out, band):
            if p.endswith(".png"):
                print(f"   sha256 {os.path.basename(p)} {hashlib.sha256(open(p, 'rb').read()).hexdigest()}", file=out)

if __name__ == "__main__":
    main()
