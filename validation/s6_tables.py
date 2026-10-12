#!/usr/bin/env python3
"""S6 tables for hyman2026local (analysis plan v1 section 9; Master Plan S6, M5.3).

Reads the primary data and the S5 outputs; computes nothing that enters the R1.2 verdict.

  A  Table 5 rows (LaTeX): per configuration, the role, measured speedup S, the error of the
     selected pair K1+O3 (frozen prediction for held-out rows, training leave-one-configuration-out
     for training rows), S_id from counts, budget beta, overhead fraction x = H/K_G, the one-run
     test, and the mean growth factor against r^delta.
  B  Where the negative overhead comes from: the median non-kernel time of each schedule split by
     timer (fill, sync, avg, cfl summed over levels; dt, diag; untimed remainder), and each timer's
     share of O_G - O_L = -H.
  C  Plan section 9(c): level ratios of the real AMReX hierarchies against the synthetic counts of
     Table 4 (3D, 16^3 base, b = 2, no blocking), and the share of the domain that level 1 covers.

Usage:  python3 validation/s6_tables.py validation/data --evaluation validation/evaluation_s5.json \
            --selection validation/predictions_frozen_selection.json --out validation/table5_rows.tex
Python 3, standard library only. Deterministic.
"""
import argparse, csv, json, os, statistics as st
from collections import defaultdict

LABEL = {"point": "point", "circle": "circle", "disk": "disk", "sphere": "sphere", "ball": "ball"}
ORDER = [("2", "point"), ("2", "circle"), ("2", "disk"), ("3", "point"), ("3", "circle"),
         ("3", "sphere"), ("3", "ball")]
# Table 4 of the note (synthetic, 3D, 16^3 base, r = 2, band of two cell widths, no blocking)
SYNTH = {"point": [4096, 288, 272, 304, 240, 304], "circle": [4096, 2984, 6072, 12144, 24416, 48344],
         "sphere": [4096, 9808, 37616, 148728, 592808, 2372680],
         "ball": [4096, 10552, 52376, 319272, 2209632, 16396936]}


def load(D):
    runs = [r for r in csv.DictReader(open(os.path.join(D, "runs.csv"))) if r["status"] == "ok"]
    rerun_cells = {(r["config"], r["schedule"]) for r in runs if r["mode"] == "rerun"}
    runs = [r for r in runs if r["mode"] == "rerun" or (r["config"], r["schedule"]) not in rerun_cells]
    lv = defaultdict(list)
    for r in csv.DictReader(open(os.path.join(D, "levels.csv"))):
        lv[r["run_id"]].append(r)
    cells = defaultdict(list)
    for r in runs:
        levels = lv[r["run_id"]]
        T = float(r["window_wall"])
        rec = dict(T=T, K=float(r["kern"]), O=float(r["nonkern"]), dt=float(r["tm_dt"]),
                   diag=float(r["tm_diag"]), regrid=float(r["tm_regrid"]),
                   untimed=T - float(r["timer_sum"]))
        for k in ("fill", "sync", "avg", "cfl"):
            rec[k] = sum(float(x[k]) for x in levels)
        cells[(r["config"], r["schedule"])].append(rec)
    return {k: {q: st.median(x[q] for x in v) for q in v[0]} for k, v in cells.items()}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("data")
    ap.add_argument("--evaluation", required=True)
    ap.add_argument("--selection", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    ev = json.load(open(a.evaluation))
    sel = json.load(open(a.selection))
    loo = [p for p in sel["loco"] if p["pair"] == ev["model"]][0]["errors"]
    sec = ev["secondary"]
    med = load(a.data)

    # Section 2 overhead with one cost per update taken from global stepping (S6 referee R-3, ruling G8(a)):
    # H_C = T_L - T_G + C (U_G - U_L), C = K_G / U_G, reported as x_C = H_C / K_G. T, K are medians over repetitions
# (second referee Q-8: T from its own median, not K + O).
    import sys as _sys
    _sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import fit as F
    full = F.load(a.data, allow_heldout_timing=True)
    def U(c, s):
        return sum(x["A"] * x["N"] for x in F.lv_list(full[c], s))
    xc = {}
    for c in sec:
        t = full[c]["timing"]
        C = t["global"]["K"] / U(c, "global")
        H2 = t["subcycle"]["T"] - t["global"]["T"] + C * (U(c, "global") - U(c, "subcycle"))
        xc[c] = H2 / t["global"]["K"]
    yv = {c: 1 / sec[c]["S"] - 1 / sec[c]["S_id"] for c in sec}
    e_id = {c: abs(sec[c]["S_id"] - sec[c]["S"]) / sec[c]["S"] for c in sec}

    # ---- A: Table 5 rows (d, feature, delta, L, S, e model, e counts, S_id, beta, x_C, y, one-run, growth)
    rows = []
    for d, feat in ORDER:
        for c in sorted((c for c, v in sec.items() if str(v["dim"]) == d and v["feature"] == feat),
                        key=lambda c: sec[c]["L"]):
            v = sec[c]
            held = v["role"] == "heldout"
            e = ev["heldout"][c]["e"] if held else loo[c]
            rows.append((c, f"{d} & {LABEL[feat]} & {v['delta']} & {v['L']} & {v['S']:.3f} & "
                            f"{e:.3f}{'' if held else '$^{*}$'} & {e_id[c]:.3f} & {v['S_id']:.3f} & "
                            f"{v['beta']:.3f} & ${xc[c]:.3f}$ & ${yv[c]:.3f}$ & {'yes' if v['one_run'] else 'no'} & "
                            f"{v['growth']:.2f}\\\\"))
    with open(a.out, "w") as f:
        f.write("% generated by validation/s6_tables.py; do not edit by hand\n")
        prev_d = None
        for c, line in rows:
            if prev_d is not None and line[0] != prev_d:
                f.write("\\addlinespace\n")
            prev_d = line[0]
            f.write(line + "\n")
    print(f"A  Table 5: {len(rows)} rows written to {a.out}")
    print(f"   held-out frozen errors: median {ev['median_error']:.4f}; "
          f"training LOO errors: median {st.median(loo.values()):.4f}, max {max(loo.values()):.3f} "
          f"({max(loo, key=loo.get)})")
    print(f"   x range {min(v['x'] for v in sec.values()):.3f} to {max(v['x'] for v in sec.values()):.3f}; "
          f"margin beta - x {min(v['margin'] for v in sec.values()):.3f} to "
          f"{max(v['margin'] for v in sec.values()):.3f}; one-run test holds in "
          f"{sum(v['one_run'] for v in sec.values())} of {len(sec)}; subcycling wins in "
          f"{sum(v['wins'] for v in sec.values())}; false positives "
          f"{sum(v['one_run'] and not v['wins'] for v in sec.values())}; cost-weighted variant agrees in "
          f"{sum(v['one_run'] == v['one_run_costweighted'] for v in sec.values())}")
    ratio = [v["S"] / v["S_id"] for v in sec.values()]
    print(f"   S/S_id: {min(ratio):.3f} to {max(ratio):.3f}; S > S_id in "
          f"{sum(r > 1 for r in ratio)} of {len(ratio)}")

    # ---- B: where -H = O_G - O_L comes from
    cats = ["fill", "sync", "avg", "cfl", "dt", "diag", "untimed"]
    tot = defaultdict(float)
    print("B  non-kernel time by timer, medians over repetitions (seconds); share of O_G - O_L")
    print("   config               O_G     O_L   " + "  ".join(f"{k:>7}" for k in cats))
    for c in sorted(sec):
        g, l = med[(c, "global")], med[(c, "subcycle")]
        diff = g["O"] - l["O"]
        shares = {k: (g[k] - l[k]) / diff for k in cats}
        for k in cats:
            tot[k] += (g[k] - l[k])
        tot["all"] += diff
        print(f"   {c:18s} {g['O']:7.3f} {l['O']:7.3f}   " + "  ".join(f"{shares[k]:7.2f}" for k in cats))
    print("   pooled shares: " + ", ".join(f"{k} {tot[k] / tot['all']:.2f}" for k in cats))
    fillavg = [(med[(c, 'global')]['fill'] + med[(c, 'global')]['avg'] - med[(c, 'subcycle')]['fill']
                - med[(c, 'subcycle')]['avg']) / (med[(c, 'global')]['O'] - med[(c, 'subcycle')]['O'])
               for c in sec]
    print(f"   fill + avg share of O_G - O_L per configuration: {min(fillavg):.2f} to {max(fillavg):.2f}")
    syncd = [(med[(c, 'subcycle')]['sync'] - med[(c, 'global')]['sync']) for c in sec]
    print(f"   sync_L - sync_G (s): {min(syncd):.3f} to {max(syncd):.3f}; positive in "
          f"{sum(s > 0 for s in syncd)} of {len(syncd)}")
    olk = [med[(c, 'subcycle')]['O'] / med[(c, 'subcycle')]['K'] for c in sec]
    ogk = [med[(c, 'global')]['O'] / med[(c, 'global')]['K'] for c in sec]
    print(f"   O_L/K_L {min(olk):.2f} to {max(olk):.2f}; O_G/K_G {min(ogk):.2f} to {max(ogk):.2f}")

    # ---- D: post hoc checks raised by the S6 cold referee (descriptive; not part of the verdict)
    import sys as _sys
    _sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import fit as F
    full = F.load(a.data, allow_heldout_timing=True)
    held = sorted(c for c, v in sec.items() if v["role"] == "heldout")
    allc = sorted(sec)
    def U(c, s):
        return sum(x["A"] * x["N"] for x in F.lv_list(full[c], s))
    e_id = {c: abs(sec[c]["S_id"] - sec[c]["S"]) / sec[c]["S"] for c in allc}
    e_m = {c: ev["heldout"][c]["e"] for c in held}
    sm1_id = {c: abs(sec[c]["S_id"] - sec[c]["S"]) / (sec[c]["S"] - 1) for c in held}
    sm1_m = {c: abs(ev["heldout"][c]["S_hat"] - sec[c]["S"]) / (sec[c]["S"] - 1) for c in held}
    print("D  baseline: S_id from the counts alone, no fitted coefficient")
    print(f"   held-out median e: counts {st.median(e_id[c] for c in held):.4f}, selected model "
          f"{st.median(e_m.values()):.4f}; on S-1: counts {st.median(sm1_id.values()):.3f}, "
          f"model {st.median(sm1_m.values()):.3f}")
    for grp, feats in (("points", {"point"}), ("filled regions", {"disk", "ball"})):
        cs = [c for c in allc if sec[c]["feature"] in feats]
        print(f"   counts-alone e on {grp}: {min(e_id[c] for c in cs):.3f} to {max(e_id[c] for c in cs):.3f}")
    print("   held-out components of the frozen prediction (model minus measured):")
    dec = ev["decomposition"]
    for c in held:
        g, l = dec[c]["global"], dec[c]["subcycle"]
        Hm, Hp = l["O"] - g["O"], l["O_hat"] - g["O_hat"]
        print(f"   {c:18s} H measured {Hm:+.3f} s, predicted {Hp:+.3f} s; x {Hm / g['K']:+.3f} vs "
              f"{Hp / g['K_hat']:+.3f}; T_G {g['T_hat'] / g['T'] - 1:+.3f}, T_L {l['T_hat'] / l['T'] - 1:+.3f}")
    pub = {c: 1 / sec[c]["S"] - 1 / sec[c]["S_id"] for c in allc}
    print(f"   published-style 1/S - 1/S_id: {min(pub.values()):+.3f} to {max(pub.values()):+.3f}; "
          f"positive in {sum(v > 0 for v in pub.values())} of {len(pub)}; above 0.046 in "
          f"{sum(v > 0.046 for v in pub.values())}")
    print(f"   Section 2 overhead with one cost per update C = K_G/U_G (median T): x_C {min(xc.values()):+.3f} to "
          f"{max(xc.values()):+.3f}; negative in {sum(v < 0 for v in xc.values())} of {len(xc)}; margin beta - x_C "
          f"{min(sec[c]['beta'] - xc[c] for c in allc):.3f} to {max(sec[c]['beta'] - xc[c] for c in allc):.3f}")
    nodt = {c: xc[c] + (med[(c, 'global')]['dt'] - med[(c, 'subcycle')]['dt']) / full[c]['timing']['global']['K'] for c in allc}
    nocfl = {c: nodt[c] + (med[(c, 'global')]['cfl'] - med[(c, 'subcycle')]['cfl']) / full[c]['timing']['global']['K'] for c in allc}
    dtshare = [med[(c, 'global')]['dt'] / med[(c, 'global')]['T'] for c in allc]
    print(f"   sensitivity (second referee Q-5): time-step computation is {min(dtshare):.3f} to {max(dtshare):.3f} of T_G; "
          f"without the dt difference x_C > 0 in {sum(v > 0 for v in nodt.values())} of 17; without dt and cfl "
          f"differences in {sum(v > 0 for v in nocfl.values())} of 17")
    sl = sorted(sec[c]['S'] for c in allc if sec[c]['feature'] != 'point')
    print(f"   measured S for curves, surfaces and filled regions: {sl[0]:.3f} to {sl[-1]:.3f}; points: " +
          ", ".join(f"{c} {sec[c]['S']:.3f}" for c in allc if sec[c]['feature'] == 'point'))
    kr = {c: (full[c]["timing"]["subcycle"]["K"] / U(c, "subcycle")) /
             (full[c]["timing"]["global"]["K"] / U(c, "global")) for c in allc}
    print(f"   kernel cost per update, subcycled over global: {min(kr.values()):.3f} to {max(kr.values()):.3f}")
    sav = [1 - 1 / sec[c]["S"] for c in allc]
    print(f"   realized saving 1 - 1/S: {min(sav):.3f} to {max(sav):.3f}")
    for d_ in ("2", "3"):
        co = sel["coefficients"][d_]
        z = sum(v == 0.0 for s_ in ("global", "subcycle") for v in co["overhead"][s_])
        print(f"   {d_}D coefficients: kernel {co['kernel']}, overhead zero entries {z} of 6")
    # third referee M-4: the reruns ran in a later session; the verdict with the original repetitions instead
    allr = [r for r in csv.DictReader(open(os.path.join(a.data, "runs.csv"))) if r["status"] == "ok"]
    rer = sorted({(r["config"], r["schedule"]) for r in allr if r["mode"] == "rerun"})
    def S_from(mode_ok):
        T = defaultdict(list)
        for r in allr:
            if mode_ok(r):
                T[(r["config"], r["schedule"])].append(float(r["window_wall"]))
        return {c: st.median(T[(c, "global")]) / st.median(T[(c, "subcycle")]) for c in allc}
    S_orig = S_from(lambda r: r["mode"] == "primary")
    for c, sch in rer:
        print(f"   rerun cell {c} {sch}: S with original repetitions {S_orig[c]:.3f}, with the rerun {sec[c]['S']:.3f}")
    e_orig = [abs(ev["heldout"][c]["S_hat"] - S_orig[c]) / S_orig[c] for c in held]
    print(f"   held-out median e with the original repetitions: {st.median(e_orig):.4f}; max {max(e_orig):.3f}")
    n_ok = sum(1 for r in csv.DictReader(open(os.path.join(a.data, "runs.csv"))) if r["status"] == "ok")
    print(f"   runs.csv rows with status ok: {n_ok}")

    # ---- C: plan 9(c), real against synthetic counts
    print("C  level ratios M_{l+1}/M_l: AMReX (initial hierarchy) against Table 4 (synthetic, 3D)")
    for c in sorted(sec):
        v = sec[c]
        M = v["M"]
        rat = [M[i + 1] / M[i] for i in range(1, len(M) - 1)]
        cover = M[1] / (2 ** v["dim"] * M[0])
        line = (f"   {c:18s} M={M} ratios(l>=1)={[round(x, 2) for x in rat]} mean={v['growth']:.2f} "
                f"r^delta={v['r_delta']} level-1 covers {cover:.3f} of the domain")
        if v["dim"] == 3 and v["feature"] in SYNTH:
            S = SYNTH[v["feature"]]
            srat = [S[i + 1] / S[i] for i in range(1, v["L"])]
            line += f" | synthetic ratios to the same depth {[round(x, 2) for x in srat]}"
        print(line)


if __name__ == "__main__":
    main()
