# hyman2026local: AMReX validation harness, build notes

**Written:** 2026-10-08 (America/Denver), S3, before the first timed execution of the harness (analysis plan v1, `validation/analysis_plan.md`, SHA-256 `e4c615e3b68fc1d42400f1e13f07d46de23e02e8eb14db3c25fe78424e465c15`).

## Pins (Plan M3.5)

| Repository | Commit | Date |
|---|---|---|
| `https://github.com/AMReX-Codes/amrex` | `6bff801899baed998581e74ab20ee2137d6b2dee` | 2026-10-08 ("Parser: Speed up evaluation (#6050)") |
| `https://github.com/AMReX-Codes/amrex-tutorials` | `1a73f32e10514d917333ea7a3fd54e661e232144` | 2026-07-08 (merge of PR #170) |

The pair builds together, so the fallback pin was not needed.

## Patch

`validation/harness/Advection_AmrCore.patch`: 617 lines, SHA-256 `68f11783cf8fce52abf66894388662e04976e3056fa2d95d4129a4a26ed4eb03` (harness v2). The first build (harness v1, patch `bf75dc6d5ae2447abb6554c9ddc51190cb0536dfa08eff9c238ab8d805fb9e64`) printed the conservation sums with only 10 digits. v2 prints them with 17 (analysis plan v2, change 2) and is otherwise identical. Only the first smoke runs used v1; they are labelled by the `harness` column. It applies cleanly to `amrex-tutorials` at the pin (`git apply --check`, verified on a fresh clone). It touches six files under `ExampleCodes/Amr/Advection_AmrCore/Source/`:

- `AmrCoreAdv.H`, `AmrCoreAdv.cpp`:
  - geometric tagging in `ErrorEst`, the same distance functions as `hyman2026local_reproduce.py` Section E;
  - harness parameters (`adv.feature`, `adv.feature_center`, `adv.feature_radius`, `adv.feature_tilt`, `adv.tag_band`, `adv.vel`);
  - the timing window in `Evolve`;
  - timers around `ComputeDt`, `regrid`, the velocity definition, `Reflux` and the averaging down;
  - `ReportHarness()`, which prints the counts and timers between `HARNESS_BEGIN` and `HARNESS_END`.
- `AdvancePhiAtLevel.cpp` (subcycled advance): timers for the flux MultiFab allocation and the flux-register calls (`sync`), the ghosted state and `FillPatch` (`fill`), the flux and update loops (`kern`) and the CFL check (`cfl`), plus the advance count.
- `AdvancePhiAllLevels.cpp` (global advance): timers for the flux MultiFab allocation and `average_down_faces` (`sync`, charged to the coarser level), `FillPatch` (`fill`), and the flux and update loops (`kern`), plus the advance count.
- `DefineVelocity.cpp`: a constant velocity `adv.vel` replaces the time-dependent swirl.
- `main.cpp`: calls `ReportHarness()` after `Evolve()`.

The tutorial's own conservation print each step was replaced by a sum at the start and the end of the timing window. Both sums are taken outside the window, so the `diag` timer reads zero by construction. The per-step `Coarse STEP` prints are now behind `amr.v`, which is 0 in every run, so no console output falls inside the window.

## Build

Toolchain: g++ 13.3.0 (Ubuntu 13.3.0-6ubuntu2~24.04.1), GNU make, 2 cores, 7 GB, Linux 6.18. No MPI, no OpenMP, no Fortran (`BL_NO_FORT`).

```
git clone https://github.com/AMReX-Codes/amrex.git && (cd amrex && git checkout 6bff801899baed998581e74ab20ee2137d6b2dee)
git clone https://github.com/AMReX-Codes/amrex-tutorials.git && (cd amrex-tutorials && git checkout 1a73f32e10514d917333ea7a3fd54e661e232144)
cd amrex-tutorials && git apply /path/to/validation/harness/Advection_AmrCore.patch
cd ExampleCodes/Amr/Advection_AmrCore/Exec
make -j2 AMREX_HOME=/abs/path/to/amrex DIM=2 USE_MPI=FALSE USE_OMP=FALSE COMP=gnu DEBUG=FALSE
make -j2 AMREX_HOME=/abs/path/to/amrex DIM=3 USE_MPI=FALSE USE_OMP=FALSE COMP=gnu DEBUG=FALSE
```

AMReX's flags for this configuration: `-g1 -O3 -fno-math-errno -finline-limit=43210 -std=c++20 -pthread -DNDEBUG`. Both builds finished with no warning and no error.

| Binary | Size | SHA-256 (this container) |
|---|---:|---|
| `main2d.gnu.ex` (harness v2) | 14868464 | `e12ae4a1b3d8d94639e051692d86231a828fc48419cbc2fcb7cdfcc879dd0691` |
| `main3d.gnu.ex` (harness v2) | 15942960 | `2e7b2874be38a6b2642e167b2cc8b55336b2a2c0b71b2fa2cf6f10006f4ae809` |
| `main2d.gnu.ex` (harness v1, superseded) | 14868528 | `b5812bc18ccb29bf47259496f582800feff49dec8627afc05309fc6613b75090` |
| `main3d.gnu.ex` (harness v1, superseded) | 15943144 | `14cd333243e58aa56acd629130bf65fec9dceedc96d8dff9a54e940f580b8363` |

Binary hashes depend on the toolchain and paths. They identify the binaries used here and are not expected to reproduce elsewhere.

## Running

`validation/run_matrix.py` writes the inputs, runs a binary per configuration and schedule, and parses the `HARNESS` block into `runs.csv` and `levels.csv`. Inputs follow analysis plan §2. The clones and build trees live in the session scratchpad (Plan M3.4) and are rebuilt from the pins and the patch.

## Window length (analysis plan §4)

Fixed before S4 by analysis plan v2, change 1. $n_c(c)=\max(n_c^0(d),\lceil 2.0\,\mathrm{s}/\tau_L(c)\rceil)$, with $n_c^0=4$ (2D) and $3$ (3D), and $\tau_L$ from one subcycled calibration run per configuration (`validation/calibration/`). The map is `validation/nc_map.json`. Pass it to `run_matrix.py --nc-file`.

| Configuration | Role | $\tau_L$ (ms per coarse interval) | $n_c$ | Subcycled window (s) |
|---|---|---:|---:|---:|
| `d2_point_L2_r2` | training | 0.80 | 2505 | 2.00 |
| `d2_point_L3_r2` | training | 1.15 | 1745 | 2.00 |
| `d2_point_L4_r2` | training | 2.82 | 709 | 2.00 |
| `d2_circle_L2_r2` | held out | 10.22 | 196 | 2.00 |
| `d2_circle_L3_r2` | held out | 33.41 | 60 | 2.00 |
| `d2_circle_L4_r2` | held out | 162.24 | 13 | 2.11 |
| `d2_disk_L2_r2` | training | 16.39 | 123 | 2.02 |
| `d2_disk_L3_r2` | training | 135.45 | 15 | 2.03 |
| `d2_disk_L4_r2` | training | 1167.43 | 4 | 4.67 |
| `d3_point_L2_r2` | training | 6.50 | 308 | 2.00 |
| `d3_point_L3_r2` | training | 17.12 | 117 | 2.00 |
| `d3_circle_L2_r2` | held out | 86.86 | 24 | 2.08 |
| `d3_circle_L3_r2` | held out | 390.31 | 6 | 2.34 |
| `d3_sphere_L2_r2` | held out | 352.90 | 6 | 2.12 |
| `d3_sphere_L3_r2` | held out | 2673.86 | 3 | 8.02 |
| `d3_ball_L2_r2` | training | 387.43 | 6 | 2.32 |
| `d3_ball_L3_r2` | training | 3755.33 | 3 | 11.27 |

The calibration ran the subcycled schedule only, so no held-out speedup exists before S4.
