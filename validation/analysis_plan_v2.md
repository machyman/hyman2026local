# hyman2026local: AMReX validation analysis plan, amendment v2

**Amends:** `validation/analysis_plan.md` (v1, SHA-256 `e4c615e3b68fc1d42400f1e13f07d46de23e02e8eb14db3c25fe78424e465c15`). v1 is unchanged on disk and stays in force except where this file says otherwise.
**Written:** 2026-10-08 (America/Denver), S3, **before any S4 timing.** Under v1's amendment rule this costs nothing and is not a deviation.

## What data existed when this was written

Everything is S3 harness data and is non-analysis under v1 §4. All of it is in `validation/smoke/` and `validation/calibration/`.

- **Smoke runs.** Training configurations only, both schedules: `d2_point_L2`, `d2_disk_L3`, `d3_point_L2` and `d3_ball_L2`, with harness builds v1 and v2. Then `d2_point_L2` and `d3_point_L2` again at the calibrated window lengths.
- **Calibration runs.** One run of each of the 17 primary configurations, subcycled schedule only, at v1's default $n_c$. No held-out configuration has been run under global stepping, and no held-out speedup has been computed.

**Disclosure.** In the smoke runs the kernel time per update differed between the two schedules by about 15 percent on the finest level of `d2_disk_L3`. In the subcycled advance, the flux and update loops are fused and the fluxes are copied for the flux registers. In the global advance, the two loops run separately. No model was added, removed or changed in response. The schedule-specific kernel model K2s was already in v1 §6.

## Change 1: window length per configuration (v1 §4)

v1 fixed one $n_c$ per dimension, to be raised for a dimension whose cheapest configuration timed under 0.5 s. Calibration shows the subcycled cost of one coarse interval spanning 0.80 ms to 1.17 s in 2D and 6.5 ms to 3.76 s in 3D. No single $n_c$ per dimension gives the cheap configurations a window long enough to time without making the costly ones run for many minutes per repetition.

**New rule.** $n_c(c)=\max\bigl(n_c^0(d),\ \lceil 2.0\ \mathrm{s}/\tau_L(c)\rceil\bigr)$. Here $n_c^0=4$ in 2D and $3$ in 3D, and $\tau_L(c)$ is the subcycled window time per coarse interval from configuration $c$'s calibration run. Every subcycled window is then about 2 s or longer. The values are in `validation/nc_map.json` (SHA-256 `19a4070f758ff9e728826d67efb0161f58036de204e9ac887874c4f3c24db6b5`). They range from 3 to 2505.

**Why this leaves the test unchanged.** Both schedules of a configuration use the same $n_c$, so they cover the same simulated interval. The models see $n_c$ only through the advance counts $A^s_\ell$, which scale with $n_c$ under both schedules. The speedup and its prediction do not depend on $n_c$. Relative residuals keep configurations with different window lengths on an equal footing in the fit.

## Change 2: precision of the conservation sums (v1 §2, §5)

The harness printed with AMReX's 10 significant digits, too few to test v1 §5's drift bound of $10^{-10}$. Harness v2 prints the two sums with 17 digits; nothing else changed. The patch is now SHA-256 `68f11783cf8fce52abf66894388662e04976e3056fa2d95d4129a4a26ed4eb03`, recorded in `validation/BUILD.md`. Every calibration run and every later run uses harness v2. The smoke runs show drift between 0 and $3.5\times10^{-14}$.

## Unchanged

The configurations, the held-out split, the timers, the repetitions and their order, the models, fitting, selection, the prediction freeze, the R1.2 verdict, the explanation standard, the secondary analyses and the QC rules all stand as in v1.
