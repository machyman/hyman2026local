#!/usr/bin/env python3
"""S5 evaluation for the hyman2026local AMReX validation (analysis plan v1 sections 8 and 9; amendment v2).

  python3 evaluate.py DATA_DIR --frozen predictions_frozen.csv --frozen-sha256 HEX --out-prefix PREFIX

Run only after the SHA-256 of the frozen predictions has been recorded in CHANGELOG.md. Refuses to run
if the file's hash differs from --frozen-sha256. Writes PREFIX.json and PREFIX.md with:
  - the held-out errors e_c = |S_hat - S| / S, their median, and the R1.2 verdict inputs;
  - a bootstrap (2,000 resamples, seed 20261008) over repetitions, refitting the selected pair;
  - the kernel/overhead decomposition of every held-out miss above 20 percent;
  - all twelve pairs' held-out errors (reported after the verdict, for transparency);
  - secondary analyses: the one-run test, measured overhead x = H/K_G against beta, level-count growth
    against r^delta, and per-update kernel cost by level and schedule.
"""
import argparse, csv, hashlib, json, os, statistics as st, sys
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fit as F   # noqa: E402  (fit.py in the same folder)

SEED = 20261008
NBOOT = 2000


def S_id_counts(e, r):
    lv = F.lv_list(e, "subcycle")
    L = e["meta"]["L"]
    N = [x["N"] for x in lv]
    return r ** L * sum(N) / sum(r ** l * N[l] for l in range(L + 1))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("data"); ap.add_argument("--frozen", required=True)
    ap.add_argument("--frozen-sha256", required=True); ap.add_argument("--out-prefix", required=True)
    a = ap.parse_args()
    h = hashlib.sha256(open(a.frozen, "rb").read()).hexdigest()
    if h != a.frozen_sha256:
        sys.exit(f"frozen predictions hash {h} does not match the recorded {a.frozen_sha256}")
    frozen = {r["config"]: r for r in csv.DictReader(open(a.frozen))}
    model = {r["model"] for r in frozen.values()}
    assert len(model) == 1
    kk, ok = next(iter(model)).split("+")

    raw = F.load_raw(a.data, heldout_timing=True)
    data = F.load(raw, allow_heldout_timing=True)
    train = {c: e for c, e in data.items() if e["meta"]["role"] == "training"}
    held = {c: e for c, e in data.items() if e["meta"]["role"] == "heldout"}

    # ---- primary: errors against the frozen predictions
    res = {}
    for c, e in sorted(held.items()):
        S = F.measured_S(e); Sh = float(frozen[c]["S_hat"])
        res[c] = dict(S=S, S_hat=Sh, e=abs(Sh - S) / S)
    med = st.median(v["e"] for v in res.values())

    # ---- bootstrap over repetitions, refitting the selected pair
    rng = np.random.default_rng(SEED)
    boots = {c: [] for c in held}; bmed = []
    for _ in range(NBOOT):
        d = F.load(raw, allow_heldout_timing=True, rng=rng)
        tr = {c: e for c, e in d.items() if e["meta"]["role"] == "training"}
        fits = {dim: F.fit_pair(kk, ok, tr, dim) for dim in (2, 3)}
        errs = []
        for c in held:
            e = d[c]; kc, oc = fits[e["meta"]["dim"]]
            p = F.predict_config(kk, ok, kc, oc, e)
            S = F.measured_S(e); err = abs(p["S"] - S) / S
            boots[c].append(err); errs.append(err)
        bmed.append(st.median(errs))
    pct = lambda v: [float(np.percentile(v, 2.5)), float(np.percentile(v, 97.5))]
    for c in res:
        res[c]["e_ci95"] = pct(boots[c])
    med_ci = pct(bmed)

    # ---- decomposition of misses above 20 percent (plan section 8, explanation standard)
    decomp = {}
    for c, v in res.items():
        e = held[c]; fr = frozen[c]
        parts = {}
        for s, tag in (("global", "G"), ("subcycle", "L")):
            m = e["timing"][s]
            parts[s] = dict(K=m["K"], K_hat=float(fr[f"K_{tag}_hat"]), O=m["O"], O_hat=float(fr[f"O_{tag}_hat"]),
                            T=m["T"], T_hat=float(fr[f"T_{tag}_hat"]),
                            kern=m["kern"], U=[x["A"] * x["N"] for x in F.lv_list(e, s)])
        decomp[c] = parts
    misses = {c: v for c, v in res.items() if v["e"] > 0.20}

    # ---- transparency: all twelve pairs on the held-out set (reported after the verdict)
    allpairs = {}
    for k2 in F.KERNELS:
        for o2 in F.OVERHEADS:
            fits = {dim: F.fit_pair(k2, o2, train, dim) for dim in (2, 3)}
            errs = {}
            for c, e in held.items():
                kc, oc = fits[e["meta"]["dim"]]
                p = F.predict_config(k2, o2, kc, oc, e)
                errs[c] = abs(p["S"] - F.measured_S(e)) / F.measured_S(e)
            allpairs[f"{k2}+{o2}"] = dict(median=st.median(errs.values()), errors=errs)

    # ---- secondary analyses (plan section 9)
    sec = {}
    for c, e in sorted(data.items()):
        r = e["meta"]["r"]; L = e["meta"]["L"]
        Sid = S_id_counts(e, r)
        g, l = e["timing"]["global"], e["timing"]["subcycle"]
        lvL = F.lv_list(e, "subcycle")
        cost = [l["kern"][j] / (lvL[j]["A"] * lvL[j]["N"]) for j in range(L + 1)]
        N = [x["N"] for x in lvL]
        Sid_c = r ** L * sum(cost[j] * N[j] for j in range(L + 1)) / sum(r ** j * cost[j] * N[j] for j in range(L + 1))
        S = F.measured_S(e); H = l["O"] - g["O"]
        lvG = F.lv_list(e, "global")
        costG = [g["kern"][j] / (lvG[j]["A"] * lvG[j]["N"]) for j in range(L + 1)]
        sec[c] = dict(role=e["meta"]["role"], dim=e["meta"]["dim"], feature=e["meta"]["feature"], delta=e["meta"]["delta"], L=L,
                      S=S, S_id=Sid, S_id_costweighted=Sid_c, beta=1 - 1 / Sid, H=H, x=H / g["K"],
                      margin=(1 - 1 / Sid) - H / g["K"],
                      one_run=bool(l["O"] < (Sid - 1) * l["K"]), one_run_costweighted=bool(l["O"] < (Sid_c - 1) * l["K"]),
                      wins=bool(S > 1), growth=(N[L] / N[1]) ** (1 / (L - 1)) if L >= 2 else None, r_delta=r ** e["meta"]["delta"],
                      M=N, cost_ns_subcycle=[1e9 * x for x in cost], cost_ns_global=[1e9 * x for x in costG])

    out = dict(frozen_sha256=h, model=f"{kk}+{ok}", heldout=res, median_error=med, median_error_ci95=med_ci,
               misses_above_20pct=sorted(misses), decomposition=decomp, all_pairs=allpairs, secondary=sec,
               bootstrap=dict(n=NBOOT, seed=SEED))
    json.dump(out, open(a.out_prefix + ".json", "w"), indent=1)

    md = [f"# S5 evaluation (analysis plan v1 section 8; amendment v2)", "",
          f"Frozen predictions SHA-256 `{h}`; selected pair **{kk}+{ok}**.", "",
          "## Held-out errors", "", "| Configuration | $S$ measured | $\\hat S$ | $e$ | 95% CI of $e$ |", "|---|---:|---:|---:|---|"]
    for c, v in res.items():
        md.append(f"| `{c}` | {v['S']:.4f} | {v['S_hat']:.4f} | {v['e']:.4f} | {v['e_ci95'][0]:.4f} to {v['e_ci95'][1]:.4f} |")
    md += ["", f"**Median error:** {med:.4f} (95% CI {med_ci[0]:.4f} to {med_ci[1]:.4f}); tolerance 0.10.",
           f"**Held-out misses above 20 percent:** {', '.join(sorted(misses)) or 'none'}.", "",
           "## All twelve pairs on the held-out set (transparency, after the verdict)", "",
           "| Pair | Median held-out error |", "|---|---:|"]
    for p, v in sorted(allpairs.items(), key=lambda t: t[1]["median"]):
        md.append(f"| {p} | {v['median']:.4f} |")
    md += ["", "## Secondary analyses (descriptive)", "",
           "| Configuration | Role | $S$ | $S_{\\mathrm{id}}$ | $x=H/K_G$ | β | β − x | One-run test | Cost-weighted test | Subcycling wins | Growth | $r^\\delta$ |",
           "|---|---|---:|---:|---:|---:|---:|---|---|---|---:|---:|"]
    for c, v in sec.items():
        gr = f"{v['growth']:.2f}" if v["growth"] else "n/a"
        md.append(f"| `{c}` | {v['role']} | {v['S']:.3f} | {v['S_id']:.3f} | {v['x']:.3f} | {v['beta']:.3f} | {v['margin']:.3f} | {v['one_run']} | {v['one_run_costweighted']} | {v['wins']} | {gr} | {v['r_delta']} |")
    open(a.out_prefix + ".md", "w").write("\n".join(md) + "\n")
    print(f"median held-out error {med:.4f} (95% CI {med_ci[0]:.4f} to {med_ci[1]:.4f}); misses > 20%: {sorted(misses)}")


if __name__ == "__main__":
    main()
