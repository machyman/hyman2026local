#!/usr/bin/env python3
"""Run the hyman2026local AMReX validation harness (analysis plan v1, validation/analysis_plan.md).

Writes one AMReX inputs file per run, runs the patched Advection_AmrCore binary, parses the
HARNESS block it prints, and appends one row per run to runs.csv and one row per run and level
to levels.csv.

Modes
  smoke       S3 harness checks on a named list of configurations (non-analysis data).
  calibrate   one subcycled run of every primary configuration, to size the timing window.
              Prints no speedup.
  primary     the S4 matrix of the analysis plan: 5 repetitions, fixed pseudorandom order
              (seed 20261008), schedule order alternating by repetition. Speedups are printed
              for training configurations only (plan section 8, data discipline).
  exploratory the plan's exploratory set (section 3), labelled as such.
  rerun       plan section 10: rerun the five repetitions of named (configuration, schedule) cells
              whose coefficient of variation was 5 percent or more (--cells CONFIG:SCHEDULE ...).
              Downstream scripts use a cell's rerun repetitions in place of its primary ones.

Usage
  python3 run_matrix.py --exe2d EXE --exe3d EXE --outdir DIR --mode MODE [--configs ...]
                        [--reps N] [--nc-file FILE]
Requires Python 3.9 or later; standard library only.
"""
import argparse, csv, json, math, os, random, subprocess, sys, time

SEED = 20261008

# ---------------------------------------------------------------- configurations (plan section 3)
FEATURES = {2: [("point", 0), ("circle", 1), ("disk", 2)],
            3: [("point", 0), ("circle", 1), ("sphere", 2), ("ball", 3)]}
DEPTHS = {2: [2, 3, 4], 3: [2, 3]}
HELD_OUT = {(2, "circle"), (3, "circle"), (3, "sphere")}
NC_DEFAULT = {2: 4, 3: 3}


def cid(d, feature, L, r=2, tag=""):
    return f"d{d}_{feature}_L{L}_r{r}" + (f"_{tag}" if tag else "")


def primary_configs():
    out = []
    for d in (2, 3):
        for feature, delta in FEATURES[d]:
            for L in DEPTHS[d]:
                role = "heldout" if (d, feature) in HELD_OUT else "training"
                out.append(dict(id=cid(d, feature, L), d=d, feature=feature, delta=delta, L=L, r=2,
                                regrid_int=0, role=role))
    return out


def exploratory_configs():
    return [
        dict(id=cid(2, "circle", 3, tag="regrid"), d=2, feature="circle", delta=1, L=3, r=2, regrid_int=2, role="exploratory"),
        dict(id=cid(3, "circle", 3, tag="regrid"), d=3, feature="circle", delta=1, L=3, r=2, regrid_int=2, role="exploratory"),
        dict(id=cid(2, "point", 2, r=4), d=2, feature="point", delta=0, L=2, r=4, regrid_int=0, role="exploratory"),
        dict(id=cid(2, "circle", 2, r=4), d=2, feature="circle", delta=1, L=2, r=4, regrid_int=0, role="exploratory"),
        dict(id=cid(2, "point", 6), d=2, feature="point", delta=0, L=6, r=2, regrid_int=0, role="exploratory"),
        dict(id=cid(3, "point", 4), d=3, feature="point", delta=0, L=4, r=2, regrid_int=0, role="exploratory"),
    ]


def config_by_id(name):
    for c in primary_configs() + exploratory_configs():
        if c["id"] == name:
            return c
    raise SystemExit(f"unknown configuration {name}")


# ---------------------------------------------------------------- inputs (plan section 2)
def inputs_text(c, schedule, nc):
    d, L, r = c["d"], c["L"], c["r"]
    Q = r ** L
    steps = (nc + 1) * (1 if schedule == "subcycle" else Q)
    base = "128 128" if d == 2 else "32 32 32"
    mgs = 64 if d == 2 else 32
    ones = " ".join(["1"] * d)
    lines = [
        f"max_step = {steps}",
        "stop_time = 1.0e30",
        "geometry.prob_lo = " + " ".join(["0.0"] * d),
        "geometry.prob_hi = " + " ".join(["1.0"] * d),
        f"geometry.is_periodic = {ones}",
        "amr.v = 0",
        f"amr.n_cell = {base}",
        f"amr.max_level = {L}",
        "amr.ref_ratio = " + " ".join([str(r)] * max(L, 1)),
        "amr.blocking_factor = 8",
        f"amr.max_grid_size = {mgs}",
        "amr.n_error_buf = 1",
        "amr.grid_eff = 0.7",
        "amr.n_proper = 1",
        f"amr.regrid_int = {c['regrid_int']}",
        "amr.plot_int = -1",
        "amr.chk_int = -1",
        "adv.cfl = 0.5",
        f"adv.do_subcycle = {1 if schedule == 'subcycle' else 0}",
        "adv.do_reflux = 1",
        f"adv.feature = {c['feature']}",
        "adv.feature_center = " + " ".join(["0.5123", "0.4871", "0.5037"][:d]),
        "adv.feature_radius = 0.3",
        "adv.feature_tilt = 0.37",
        "adv.tag_band = 2.0",
        "adv.vel = " + " ".join(["1.0"] * d),
    ]
    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------- parsing
SCALARS = ["dim", "finest_level", "ref_ratio", "steps_per_coarse", "window_steps", "window_wall",
           "tm_dt", "tm_diag", "tm_regrid", "sum_phi_start", "sum_phi_end"]
LEVEL_FIELDS = ["level", "N", "B", "G", "Gcf", "dt", "n_adv", "kern", "fill", "sync", "avg", "cfl"]


def parse(text):
    if "HARNESS_BEGIN" not in text or "HARNESS_END" not in text:
        raise ValueError("no HARNESS block")
    block = text.split("HARNESS_BEGIN", 1)[1].split("HARNESS_END", 1)[0]
    out, levels = {}, []
    for line in block.strip().splitlines():
        if line.startswith("#") or not line.strip():
            continue
        parts = line.split()
        if parts[0] == "level":
            levels.append(dict(zip(LEVEL_FIELDS, [float(x) for x in parts[1:]])))
        elif parts[0] in ("harness_version", "amrex_version", "schedule", "feature"):
            out[parts[0]] = " ".join(parts[1:])
        else:
            out[parts[0]] = float(parts[1])
    return out, levels


def timer_sum(s, levels):
    return s["tm_dt"] + s["tm_diag"] + s["tm_regrid"] + sum(
        lv["kern"] + lv["fill"] + lv["sync"] + lv["avg"] + lv["cfl"] for lv in levels)


# ---------------------------------------------------------------- running
def run_one(c, schedule, nc, rep, exe, outdir, mode):
    run_id = f"{mode}_{c['id']}_{schedule}_rep{rep}"
    ind = os.path.join(outdir, "inputs"); os.makedirs(ind, exist_ok=True)
    logd = os.path.join(outdir, "logs"); os.makedirs(logd, exist_ok=True)
    inp = os.path.join(ind, f"{c['id']}_{schedule}_nc{nc}.inputs")
    with open(inp, "w") as f:
        f.write(inputs_text(c, schedule, nc))
    t0 = time.time()
    p = subprocess.run([exe, inp], capture_output=True, text=True, cwd=outdir)
    elapsed = time.time() - t0
    with open(os.path.join(logd, run_id + ".log"), "w") as f:
        f.write(p.stdout); f.write(p.stderr)
    if p.returncode != 0:
        return dict(run_id=run_id, status=f"exit{p.returncode}"), []
    s, levels = parse(p.stdout)
    T = s["window_wall"]
    ts = timer_sum(s, levels)
    K = sum(lv["kern"] for lv in levels)
    drift = abs(s["sum_phi_end"] - s["sum_phi_start"]) / abs(s["sum_phi_start"])
    row = dict(run_id=run_id, status="ok", mode=mode, rep=rep, config=c["id"], role=c["role"],
               dim=c["d"], feature=c["feature"], delta=c["delta"], L=c["L"], r=c["r"],
               regrid_int=c["regrid_int"], schedule=schedule, nc=nc,
               finest_level=int(s["finest_level"]), steps_per_coarse=int(s["steps_per_coarse"]),
               window_steps=int(s["window_steps"]), window_wall=T, kern=K, nonkern=T - K,
               tm_dt=s["tm_dt"], tm_diag=s["tm_diag"], tm_regrid=s["tm_regrid"],
               timer_sum=ts, timer_ratio=ts / T if T > 0 else float("nan"),
               phi_drift=drift, process_wall=elapsed, harness=s.get("harness_version", ""))
    lrows = [dict(run_id=run_id, config=c["id"], schedule=schedule, rep=rep,
                  **{k: (int(v) if k in ("level", "N", "B", "G", "Gcf", "n_adv") else v) for k, v in lv.items()})
             for lv in levels]
    return row, lrows


def append_csv(path, rows):
    if not rows:
        return
    new = not os.path.exists(path)
    with open(path, "a", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        if new:
            w.writeheader()
        w.writerows(rows)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--exe2d", required=True)
    ap.add_argument("--exe3d", required=True)
    ap.add_argument("--outdir", required=True)
    ap.add_argument("--mode", required=True, choices=["smoke", "calibrate", "primary", "exploratory", "rerun"])
    ap.add_argument("--configs", nargs="*", default=None, help="configuration ids (smoke mode)")
    ap.add_argument("--cells", nargs="*", default=None, help="CONFIG:SCHEDULE cells (rerun mode)")
    ap.add_argument("--schedules", nargs="*", default=["global", "subcycle"])
    ap.add_argument("--reps", type=int, default=5)
    ap.add_argument("--nc", type=int, default=None, help="override n_c for every run (smoke mode)")
    ap.add_argument("--nc-file", default=None, help="JSON map from configuration id to n_c")
    a = ap.parse_args()
    outdir = os.path.abspath(a.outdir); os.makedirs(outdir, exist_ok=True)
    exe = {2: os.path.abspath(a.exe2d), 3: os.path.abspath(a.exe3d)}
    ncmap = json.load(open(a.nc_file)) if a.nc_file else {}

    def nc_of(c):
        if a.nc is not None:
            return a.nc
        return int(ncmap.get(c["id"], NC_DEFAULT[c["d"]]))

    runs_csv, levels_csv = os.path.join(outdir, "runs.csv"), os.path.join(outdir, "levels.csv")
    if a.mode == "smoke":
        configs = [config_by_id(x) for x in (a.configs or [])]
        plan = [(c, s, 1) for c in configs for s in a.schedules]
    elif a.mode == "rerun":
        plan = []
        for cell in a.cells or []:
            cname, sched = cell.split(":")
            plan += [(config_by_id(cname), sched, rep) for rep in range(1, a.reps + 1)]
    elif a.mode == "calibrate":
        plan = [(c, "subcycle", 1) for c in primary_configs()]
    else:
        configs = primary_configs() if a.mode == "primary" else exploratory_configs()
        plan = []
        rng = random.Random(SEED)
        for rep in range(1, a.reps + 1):
            order = configs[:]
            rng.shuffle(order)
            for c in order:
                scheds = ["global", "subcycle"] if rep % 2 == 1 else ["subcycle", "global"]
                plan += [(c, s, rep) for s in scheds]

    for c, s, rep in plan:
        row, lrows = run_one(c, s, nc_of(c), rep, exe[c["d"]], outdir, a.mode)
        append_csv(runs_csv, [row]); append_csv(levels_csv, lrows)
        if row["status"] != "ok":
            print(f"{row['run_id']}: {row['status']}", flush=True)
            continue
        # plan section 8: no held-out timing is displayed before the prediction freeze
        hide = a.mode in ("primary", "rerun") and c["role"] == "heldout"
        tshow = "T=(withheld)" if hide else f"T={row['window_wall']:.4f}s"
        msg = (f"{row['run_id']}: L={row['finest_level']} {tshow} "
               f"timers/T={row['timer_ratio']:.3f} drift={row['phi_drift']:.1e}")
        print(msg, flush=True)


if __name__ == "__main__":
    main()
