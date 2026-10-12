# validation/data: the primary runs

The 17 primary configurations, each timed under subcycling and under global stepping. [Back to the validation README](../README.md).

| Path | What it is |
|---|---|
| [`runs.csv`](runs.csv) | One row per run: configuration, schedule, repetition, wall times and timer decomposition |
| [`levels.csv`](levels.csv) | Per-level counts (cells, boxes) and per-level timers for each run |
| [`qc_summary.md`](qc_summary.md), [`qc.json`](qc.json) | Quality control of these runs, written by `../qc_s4.py` |
| `inputs/` | The AMReX inputs file of each run, written by `../run_matrix.py` |
| `logs/` | The console log of each run, with the harness report between `HARNESS_BEGIN` and `HARNESS_END` |
