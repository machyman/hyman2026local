#!/usr/bin/env python3
"""Exploratory set of the hyman2026local AMReX validation (analysis plan v1 section 3; Plan M3.10; deviation D1).

  python3 exploratory_s5.py EXPLORATORY_DATA_DIR --selection predictions_frozen_selection.json --out-prefix PREFIX

EXPLORATORY. Never part of the R1.2 verdict. Run only after the S5 prediction freeze and evaluation.
For each configuration: QC (repetitions, CV of the window time, timer sums, conservation drift, identity of the
level counts across schedules), the measured speedup S, the count-based ideal S_id and budget beta, the measured
overhead H = O_L - O_G and x = H/K_G, the one-run test of Section 4, and the speedup predicted by the frozen
selected pair (coefficients from the selection file, unchanged) from the configuration's initial level counts.
With regridding on, the counts change during the run; the prediction then uses the initial hierarchy and is
reported as such. Writes PREFIX.json and PREFIX.md.
"""
import argparse, csv, json, os, statistics as st, sys
from collections import defaultdict
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fit as F   # noqa: E402


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("data"); ap.add_argument("--selection", required=True); ap.add_argument("--out-prefix", required=True)
    a = ap.parse_args()
    sel = json.load(open(a.selection))
    kk, ok = sel["selected"].split("+")
    coef = {int(d): (np.array(v["kernel"]) if isinstance(v["kernel"], list) else {int(k): x for k, x in v["kernel"].items()},
                     {s: np.array(v["overhead"][s]) for s in F.SCHEDS}) for d, v in sel["coefficients"].items()}

    runs = list(csv.DictReader(open(os.path.join(a.data, "runs.csv"))))
    levels = defaultdict(list)
    for r in csv.DictReader(open(os.path.join(a.data, "levels.csv"))):
        levels[r["run_id"]].append(r)
    bad = [r["run_id"] for r in runs if r["status"] != "ok"]
    qc = defaultdict(lambda: dict(T=[], ratio=[], drift=[], NB=set()))
    for r in runs:
        if r["status"] != "ok":
            continue
        q = qc[(r["config"], r["schedule"])]
        q["T"].append(float(r["window_wall"])); q["ratio"].append(float(r["timer_ratio"])); q["drift"].append(abs(float(r["phi_drift"])))
        q["NB"].add(tuple((int(x["N"]), int(x["B"])) for x in sorted(levels[r["run_id"]], key=lambda x: int(x["level"]))))

    data = F.load(F.load_raw(a.data, heldout_timing=True), allow_heldout_timing=True)
    out = {}
    for c, e in sorted(data.items()):
        m = e["meta"]; r = m["r"]; L = m["L"]
        g, l = e["timing"]["global"], e["timing"]["subcycle"]
        lvL = F.lv_list(e, "subcycle")
        N = [x["N"] for x in lvL]
        S = g["T"] / l["T"]
        Sid = r ** L * sum(N) / sum(r ** j * N[j] for j in range(L + 1))
        H = l["O"] - g["O"]
        kc, oc = coef[m["dim"]]
        p = F.predict_config(kk, ok, kc, oc, e)
        qG, qL = qc[(c, "global")], qc[(c, "subcycle")]
        cv = {s: (st.stdev(q["T"]) / st.mean(q["T"]) if len(q["T"]) > 1 else None) for s, q in (("global", qG), ("subcycle", qL))}
        out[c] = dict(dim=m["dim"], feature=m["feature"], L=L, r=r, reps=dict(global_=len(qG["T"]), subcycle=len(qL["T"])),
                      cv=cv, timer_ratio=[min(qG["ratio"] + qL["ratio"]), max(qG["ratio"] + qL["ratio"])],
                      drift_max=max(qG["drift"] + qL["drift"]),
                      counts_identical=(len(qG["NB"] | qL["NB"]) == 1), M=N, B=[x["B"] for x in lvL],
                      S=S, S_id=Sid, beta=1 - 1 / Sid, H=H, x=H / g["K"], one_run=bool(l["O"] < (Sid - 1) * l["K"]),
                      wins=bool(S > 1), S_hat_frozen_pair=p["S"], e=abs(p["S"] - S) / S,
                      K=dict(G=g["K"], L=l["K"]), O=dict(G=g["O"], L=l["O"]),
                      K_hat=dict(G=p["global"]["K"], L=p["subcycle"]["K"]), O_hat=dict(G=p["global"]["O"], L=p["subcycle"]["O"]))
    res = dict(label="EXPLORATORY: not part of the R1.2 verdict", pair=f"{kk}+{ok}", failed_runs=bad, configs=out)
    json.dump(res, open(a.out_prefix + ".json", "w"), indent=1)

    md = ["# S5 exploratory set (EXPLORATORY: not part of the R1.2 verdict)", "",
          f"Analysis plan v1 §3; Plan M3.10; deviation D1. Predictions use the frozen pair **{kk}+{ok}** with its training coefficients unchanged. Failed runs: {len(bad)}.", "",
          "| Configuration | CV of $T$ (G / L) | Timers/$T$ | Counts identical | $S$ | $\\hat S$ (frozen pair) | $e$ | $S_{\\mathrm{id}}$ | $x=H/K_G$ | β | One-run test | Subcycling wins |",
          "|---|---|---|---|---:|---:|---:|---:|---:|---:|---|---|"]
    for c, v in out.items():
        md.append(f"| `{c}` | {v['cv']['global']:.3f} / {v['cv']['subcycle']:.3f} | {v['timer_ratio'][0]:.3f} to {v['timer_ratio'][1]:.3f} | "
                  f"{v['counts_identical']} | {v['S']:.3f} | {v['S_hat_frozen_pair']:.3f} | {v['e']:.3f} | {v['S_id']:.3f} | {v['x']:.3f} | "
                  f"{v['beta']:.3f} | {v['one_run']} | {v['wins']} |")
    md += ["", "Level counts $M_\\ell$ (initial hierarchy):", ""]
    for c, v in out.items():
        md.append(f"- `{c}`: M = {v['M']}, B = {v['B']}")
    open(a.out_prefix + ".md", "w").write("\n".join(md) + "\n")
    for c, v in out.items():
        print(f"{c:26s} S {v['S']:.3f}  S_hat {v['S_hat_frozen_pair']:.3f}  e {v['e']:.3f}  x {v['x']:+.3f}  beta {v['beta']:.3f}  "
              f"CV {v['cv']['global']:.3f}/{v['cv']['subcycle']:.3f}  counts_identical {v['counts_identical']}")


if __name__ == "__main__":
    main()
