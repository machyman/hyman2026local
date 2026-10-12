#!/usr/bin/env python3
"""S4 quality control for the hyman2026local AMReX validation (analysis plan v1 section 10, amendment v2).

Reads validation/data/runs.csv and levels.csv and writes qc_summary.md and qc.json beside them.
For every (configuration, schedule) cell: repetitions, median window time, coefficient of variation,
timer-sum range, conservation drift, finest level, and the identity check on N and B across schedules
and repetitions. Speedups, overheads and budgets are computed for TRAINING configurations only; for
held-out configurations only the QC metrics and the level counts (predictors, not outcomes) are reported
(plan section 8, data discipline before the prediction freeze).

Usage:  python3 qc_s4.py DATA_DIR
Standard library only.
"""
import csv, json, math, os, statistics as st, sys
from collections import defaultdict


def main(D):
    runs = [r for r in csv.DictReader(open(os.path.join(D, "runs.csv")))]
    levels = [r for r in csv.DictReader(open(os.path.join(D, "levels.csv")))]
    bad = [r for r in runs if r["status"] != "ok"]
    ok = [r for r in runs if r["status"] == "ok"]
    # plan section 10: a cell rerun for high CV uses its rerun repetitions in place of the primary ones
    rerun_cells = {(r["config"], r["schedule"]) for r in ok if r["mode"] == "rerun"}
    superseded = [r["run_id"] for r in ok if r["mode"] != "rerun" and (r["config"], r["schedule"]) in rerun_cells]
    ok = [r for r in ok if not (r["mode"] != "rerun" and (r["config"], r["schedule"]) in rerun_cells)]
    lv = defaultdict(list)
    for r in levels:
        lv[r["run_id"]].append(r)

    cells = defaultdict(list)
    for r in ok:
        cells[(r["config"], r["schedule"])].append(r)
    configs = sorted({r["config"] for r in ok}, key=lambda c: (int(c[1]), c))
    meta = {r["config"]: r for r in ok}

    out = dict(failed_runs=[r["run_id"] for r in bad], rerun_cells=sorted(f"{c}|{s}" for c, s in rerun_cells),
               superseded_runs=superseded, cells={}, configs={})
    flags = []
    for (c, s), rs in sorted(cells.items()):
        T = [float(r["window_wall"]) for r in rs]
        med = st.median(T)
        cv = st.pstdev(T) / st.mean(T) if len(T) > 1 else float("nan")
        tr = [float(r["timer_ratio"]) for r in rs]
        dr = max(float(r["phi_drift"]) for r in rs)
        fl = {int(r["finest_level"]) for r in rs}
        cell = dict(n=len(rs), rerun=(c, s) in rerun_cells, cv=cv, timer_ratio_min=min(tr), timer_ratio_max=max(tr), drift_max=dr,
                    finest_levels=sorted(fl))
        if meta[c]["role"] == "training":
            cell["T_median"] = med
            cell["K_median"] = st.median(float(r["kern"]) for r in rs)
            cell["O_median"] = st.median(float(r["nonkern"]) for r in rs)
        out["cells"][f"{c}|{s}"] = cell
        if len(rs) < 5: flags.append(f"{c} {s}: only {len(rs)} repetitions")
        if cv >= 0.05: flags.append(f"{c} {s}: CV {cv:.3f} >= 0.05" + (" after rerun (kept, flagged)" if (c, s) in rerun_cells else ""))
        if min(tr) < 0.95 or max(tr) > 1.05: flags.append(f"{c} {s}: timer ratio {min(tr):.3f} to {max(tr):.3f}")
        if dr >= 1e-10: flags.append(f"{c} {s}: conservation drift {dr:.1e}")
        if fl != {int(meta[c]['L'])}: flags.append(f"{c} {s}: finest level {sorted(fl)} != L")

    for c in configs:
        m = meta[c]
        ids = [r["run_id"] for r in ok if r["config"] == c]
        sigs = {tuple((int(x["level"]), int(x["N"]), int(x["B"])) for x in sorted(lv[i], key=lambda x: int(x["level"]))) for i in ids}
        ident = len(sigs) == 1
        if not ident: flags.append(f"{c}: level counts differ across runs")
        sig = sorted(sigs)[0]
        L, r = int(m["L"]), int(m["r"])
        N = [n for (_, n, _) in sig]
        B = [b for (_, _, b) in sig]
        Q = r ** L
        S_id = Q * sum(N) / sum(r ** l * N[l] for l in range(L + 1))
        growth = (N[L] / N[1]) ** (1.0 / (L - 1)) if L >= 2 else float("nan")
        info = dict(role=m["role"], dim=int(m["dim"]), feature=m["feature"], delta=int(m["delta"]), L=L,
                    N=N, B=B, identity=ident, S_id_counts=S_id, beta_counts=1 - 1 / S_id,
                    growth_mean=growth, r_pow_delta=r ** int(m["delta"]))
        if m["role"] == "training":
            g, l = out["cells"][f"{c}|global"], out["cells"][f"{c}|subcycle"]
            S = g["T_median"] / l["T_median"]
            H = l["O_median"] - g["O_median"]
            info.update(S_measured=S, H=H, x=H / g["K_median"],
                        one_run_test=l["O_median"] < (S_id - 1) * l["K_median"],
                        subcycling_wins=S > 1)
        out["configs"][c] = info
    out["flags"] = flags

    json.dump(out, open(os.path.join(D, "qc.json"), "w"), indent=1)
    md = ["# S4 QC summary (analysis plan v1 section 10, amendment v2)", "",
          f"Runs: {len(runs)} recorded, {len(bad)} failed; {len(ok)} used. Cells rerun for CV (plan section 10): {', '.join(out['rerun_cells']) or 'none'}; their {len(superseded)} primary repetitions are superseded. Held-out speedups are not computed here (plan section 8).", "",
          "## QC by cell", "", "| Configuration | Schedule | n | CV | Timer sum / wall | Max drift | Finest level |", "|---|---|---:|---:|---|---:|---|"]
    for k, v in out["cells"].items():
        c, s = k.split("|")
        md.append(f"| `{c}` | {s}{' (rerun)' if v['rerun'] else ''} | {v['n']} | {v['cv']:.3f} | {v['timer_ratio_min']:.3f} to {v['timer_ratio_max']:.3f} | {v['drift_max']:.1e} | {v['finest_levels']} |")
    md += ["", "## Level counts (predictors; all configurations)", "",
           "| Configuration | Role | δ | $M_\\ell$ | Boxes | Mean growth | $r^\\delta$ | $S_{\\mathrm{id}}$ (counts) | β |", "|---|---|---:|---|---|---:|---:|---:|---:|"]
    for c, v in out["configs"].items():
        md.append(f"| `{c}` | {v['role']} | {v['delta']} | {', '.join(map(str, v['N']))} | {', '.join(map(str, v['B']))} | {v['growth_mean']:.2f} | {v['r_pow_delta']} | {v['S_id_counts']:.3f} | {v['beta_counts']:.3f} |")
    md += ["", "## Training configurations: measured speedup and overhead", "",
           "| Configuration | $S=T_G/T_L$ | $S_{\\mathrm{id}}$ | $H$ (s) | $x=H/K_G$ | β | One-run test holds | Subcycling wins |", "|---|---:|---:|---:|---:|---:|---|---|"]
    for c, v in out["configs"].items():
        if v["role"] == "training":
            md.append(f"| `{c}` | {v['S_measured']:.3f} | {v['S_id_counts']:.3f} | {v['H']:.4f} | {v['x']:.3f} | {v['beta_counts']:.3f} | {v['one_run_test']} | {v['subcycling_wins']} |")
    md += ["", "## Flags", ""] + ([f"- {f}" for f in flags] or ["- none"])
    open(os.path.join(D, "qc_summary.md"), "w").write("\n".join(md) + "\n")
    print(f"runs {len(runs)} ok {len(ok)} failed {len(bad)}; flags {len(flags)}")
    for f in flags:
        print("FLAG", f)


if __name__ == "__main__":
    main(sys.argv[1])
