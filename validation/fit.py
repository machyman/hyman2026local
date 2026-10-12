#!/usr/bin/env python3
"""S5 fitting, model selection and prediction freeze for the hyman2026local AMReX validation
(analysis plan v1, validation/analysis_plan.md, sections 6 to 8; amendment v2).

  python3 fit.py DATA_DIR --freeze OUT.csv
      Reads the training configurations' timings and the held-out configurations' COUNTS only.
      Scores the twelve (kernel, overhead) model pairs by leave-one-configuration-out over the
      training set, selects one pair by the plan's rule, refits it on all training data and writes
      the held-out predictions to OUT.csv. No held-out timing is read on this path.

The evaluation (errors, verdict, bootstrap, secondary analyses) is evaluate.py, run only after
the SHA-256 of OUT.csv has been recorded in CHANGELOG.md.

Requires Python 3.9+, NumPy and SciPy (scipy.optimize.nnls).
"""
import argparse, csv, json, math, os, statistics as st, sys
from collections import defaultdict
import numpy as np
from scipy.optimize import nnls

KERNELS = ["K1", "K2", "K2s", "K3"]
OVERHEADS = ["O1", "O2", "O3"]
SCHEDS = ["global", "subcycle"]


# ---------------------------------------------------------------- data
def load_raw(D, heldout_timing=False):
    """Parse runs.csv and levels.csv once: {(config, schedule): [rep dicts]} plus metadata and counts.
    Held-out timing columns are not parsed unless heldout_timing (plan section 8: the freeze path
    reads only the training rows and the held-out counts)."""
    runs = [r for r in csv.DictReader(open(os.path.join(D, "runs.csv"))) if r["status"] == "ok"]
    # plan section 10: a cell rerun for high CV uses its rerun repetitions in place of the primary ones
    rerun_cells = {(r["config"], r["schedule"]) for r in runs if r["mode"] == "rerun"}
    runs = [r for r in runs if r["mode"] == "rerun" or (r["config"], r["schedule"]) not in rerun_cells]
    lv = defaultdict(list)
    for r in csv.DictReader(open(os.path.join(D, "levels.csv"))):
        lv[r["run_id"]].append(r)
    cells, meta, counts = defaultdict(list), {}, {}
    for r in runs:
        c, s = r["config"], r["schedule"]
        meta[c] = dict(role=r["role"], dim=int(r["dim"]), feature=r["feature"],
                       delta=int(r["delta"]), L=int(r["L"]), r=int(r["r"]))
        levels = sorted(lv[r["run_id"]], key=lambda x: int(x["level"]))
        counts.setdefault(c, {})[s] = {int(x["level"]): dict(N=int(x["N"]), B=int(x["B"]), G=int(x["G"]),
                                                             A=int(x["n_adv"])) for x in levels}
        if r["role"] == "heldout" and not heldout_timing:
            continue
        cells[(c, s)].append(dict(T=float(r["window_wall"]), K=float(r["kern"]), O=float(r["nonkern"]),
                                  kern=[float(x["kern"]) for x in levels]))
    return dict(cells=cells, meta=meta, counts=counts)


def load(D_or_raw, allow_heldout_timing=False, rng=None):
    """Return {config: {meta, levels, timing}}. Held-out timings are dropped unless
    allow_heldout_timing. With rng (numpy Generator), repetitions are resampled with
    replacement within each (configuration, schedule) before the medians are taken."""
    raw = load_raw(D_or_raw, heldout_timing=allow_heldout_timing) if isinstance(D_or_raw, str) else D_or_raw
    out = {}
    for c, m in raw["meta"].items():
        out[c] = dict(meta=m, levels=raw["counts"][c], timing={})
    for (c, s), reps in raw["cells"].items():
        if raw["meta"][c]["role"] == "heldout" and not allow_heldout_timing:
            continue
        sample = reps if rng is None else [reps[i] for i in rng.integers(0, len(reps), len(reps))]
        L = raw["meta"][c]["L"]
        out[c]["timing"][s] = dict(T=st.median(x["T"] for x in sample), K=st.median(x["K"] for x in sample),
                                   O=st.median(x["O"] for x in sample),
                                   kern=[st.median(x["kern"][l] for x in sample) for l in range(L + 1)])
    return out


def lv_list(e, s):
    L = e["meta"]["L"]
    return [e["levels"][s][l] for l in range(L + 1)]


# ---------------------------------------------------------------- models (plan section 6)
def kernel_features(kind, lvls, s):
    """Rows of the per-level kernel design for one (configuration, schedule)."""
    rows = []
    for l, x in enumerate(lvls):
        U = x["A"] * x["N"]
        if kind == "K1":
            rows.append([U])
        elif kind == "K2":
            rows.append([U, x["A"] * x["B"]])
        elif kind == "K2s":
            z = [0.0, 0.0, 0.0, 0.0]
            j = 0 if s == "global" else 2
            z[j], z[j + 1] = U, x["A"] * x["B"]
            rows.append(z)
        else:
            raise ValueError(kind)
    return rows


def fit_kernel(kind, data, d):
    cfgs = [c for c, e in data.items() if e["meta"]["dim"] == d and e["timing"]]
    if kind == "K3":
        per = defaultdict(list)
        for c in cfgs:
            e = data[c]
            for s in SCHEDS:
                for l, x in enumerate(lv_list(e, s)):
                    per[l].append(e["timing"][s]["kern"][l] / (x["A"] * x["N"]))
        return {l: st.median(v) for l, v in per.items()}
    X, y = [], []
    for c in cfgs:
        e = data[c]
        for s in SCHEDS:
            for row, kt in zip(kernel_features(kind, lv_list(e, s), s), e["timing"][s]["kern"]):
                X.append([v / kt for v in row]); y.append(1.0)
    coef, _ = nnls(np.array(X), np.array(y))
    return coef


def predict_kernel(kind, coef, lvls, s):
    if kind == "K3":
        return sum(coef[l] * x["A"] * x["N"] for l, x in enumerate(lvls))
    return float(sum(np.dot(coef, row) for row in kernel_features(kind, lvls, s)))


def overhead_features(kind, lvls, Khat):
    if kind == "O1":
        return [Khat]
    A = sum(x["A"] for x in lvls)
    AG = sum(x["A"] * x["G"] for x in lvls)
    if kind == "O2":
        return [A, AG]
    if kind == "O3":
        return [A, AG, sum(x["A"] * x["N"] for x in lvls)]
    raise ValueError(kind)


def fit_pair(kk, ok, data, d):
    kc = fit_kernel(kk, data, d)
    oc = {}
    cfgs = [c for c, e in data.items() if e["meta"]["dim"] == d and e["timing"]]
    for s in SCHEDS:
        X, y = [], []
        for c in cfgs:
            e = data[c]
            lv = lv_list(e, s)
            Kh = predict_kernel(kk, kc, lv, s)
            Ob = e["timing"][s]["O"]
            X.append([v / Ob for v in overhead_features(ok, lv, Kh)]); y.append(1.0)
        oc[s], _ = nnls(np.array(X), np.array(y))
    return kc, oc


def predict_config(kk, ok, kc, oc, e):
    res = {}
    for s in SCHEDS:
        lv = lv_list(e, s)
        Kh = predict_kernel(kk, kc, lv, s)
        Oh = float(np.dot(oc[s], overhead_features(ok, lv, Kh)))
        res[s] = dict(K=Kh, O=Oh, T=Kh + Oh)
    res["S"] = res["global"]["T"] / res["subcycle"]["T"]
    return res


def nparams(kk, ok, data, d):
    if kk == "K3":
        nk = 1 + max(e["meta"]["L"] for e in data.values() if e["meta"]["dim"] == d)
    else:
        nk = {"K1": 1, "K2": 2, "K2s": 4}[kk]
    return nk + 2 * {"O1": 1, "O2": 2, "O3": 3}[ok]


def measured_S(e):
    return e["timing"]["global"]["T"] / e["timing"]["subcycle"]["T"]


# ---------------------------------------------------------------- selection (plan section 7)
def loco_scores(train):
    scores = {}
    for kk in KERNELS:
        for ok in OVERHEADS:
            errs = []
            for c, e in train.items():
                d = e["meta"]["dim"]
                sub = {k: v for k, v in train.items() if k != c}
                kc, oc = fit_pair(kk, ok, sub, d)
                p = predict_config(kk, ok, kc, oc, e)
                errs.append(abs(p["S"] - measured_S(e)) / measured_S(e))
            scores[(kk, ok)] = dict(median=st.median(errs), errors=dict(zip(train.keys(), errs)))
    return scores


def select(scores, data):
    best = min(v["median"] for v in scores.values())
    order = [(kk, ok) for kk in KERNELS for ok in OVERHEADS]   # listed order, K before O
    near = [p for p in order if scores[p]["median"] <= best + 0.01]
    npar = {p: sum(nparams(p[0], p[1], data, d) for d in (2, 3)) for p in near}
    fewest = min(npar.values())
    exact_best = [p for p in order if scores[p]["median"] == best]
    # a pair within 0.01 of the best with fewer parameters than the best is preferred
    best_np = min(sum(nparams(p[0], p[1], data, d) for d in (2, 3)) for p in exact_best)
    cands = [p for p in near if npar[p] == fewest] if fewest < best_np else exact_best
    return cands[0]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("data")
    ap.add_argument("--freeze", required=True)
    a = ap.parse_args()
    data = load(a.data, allow_heldout_timing=False)
    train = {c: e for c, e in data.items() if e["meta"]["role"] == "training"}
    held = {c: e for c, e in data.items() if e["meta"]["role"] == "heldout"}
    assert all(not e["timing"] for e in held.values()), "held-out timing leaked into the freeze path"
    assert len(train) == 10 and len(held) == 7, (len(train), len(held))
    scores = loco_scores(train)
    pick = select(scores, data)
    kk, ok = pick
    fits = {d: fit_pair(kk, ok, train, d) for d in (2, 3)}
    rows = []
    for c, e in sorted(held.items()):
        kc, oc = fits[e["meta"]["dim"]]
        p = predict_config(kk, ok, kc, oc, e)
        rows.append(dict(config=c, dim=e["meta"]["dim"], feature=e["meta"]["feature"], L=e["meta"]["L"],
                         model=f"{kk}+{ok}", S_hat=p["S"],
                         T_G_hat=p["global"]["T"], T_L_hat=p["subcycle"]["T"],
                         K_G_hat=p["global"]["K"], K_L_hat=p["subcycle"]["K"],
                         O_G_hat=p["global"]["O"], O_L_hat=p["subcycle"]["O"]))
    with open(a.freeze, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
    sel = dict(selected=f"{kk}+{ok}",
               loco=[dict(pair=f"{p[0]}+{p[1]}", median=v["median"],
                          params=sum(nparams(p[0], p[1], data, d) for d in (2, 3)),
                          errors=v["errors"]) for p, v in scores.items()],
               coefficients={str(d): dict(kernel=(fits[d][0].tolist() if hasattr(fits[d][0], "tolist") else {str(k): v for k, v in fits[d][0].items()}),
                                         overhead={s: fits[d][1][s].tolist() for s in SCHEDS}) for d in (2, 3)})
    json.dump(sel, open(os.path.splitext(a.freeze)[0] + "_selection.json", "w"), indent=1)
    print(f"selected {kk}+{ok}; LOCO median {scores[pick]['median']:.4f}")
    for p, v in sorted(scores.items(), key=lambda t: t[1]["median"]):
        print(f"  {p[0]:3s}+{p[1]}  LOCO median {v['median']:.4f}  params {sum(nparams(p[0], p[1], data, d) for d in (2, 3))}")
    print(f"wrote {a.freeze} ({len(rows)} held-out predictions)")


if __name__ == "__main__":
    main()
