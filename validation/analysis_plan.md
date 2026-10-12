# hyman2026local: AMReX validation analysis plan (v1)

**Written:** 2026-10-08 (America/Denver), S3, branch 3, before any timed execution of the harness.
**Status:** fixed. Its SHA-256 is recorded in `CHANGELOG.md`, the Master Plan decision log and `hyman2026local_Session3_Report.md`. Rulings in force: C1(a) (validate before posting), R1.2 option (a) (the tolerance), M3.6 and M3.7 (this plan's timing and design).
**Amendments:** none are made to this file. An amendment is a new file, `analysis_plan_v2.md`, that names this file's hash, states what changed and why, and says whether any S4 timing existed when it was written. Amendments written before the first S4 timing cost nothing. Later ones are deviations and are reported as such.

## 1. Question

Section 4 of the note ("Testing the model") proposes a direct test. Run the same hierarchy with subcycling on and off in one code. Fit the per-update costs $C_\ell$ and the overhead $H$ on some runs. Ask whether they predict the measured speedup on others, across a point, a filament, a front and a filled region in two and three dimensions. This plan fixes that test before any data exist.

**Primary hypothesis (H1, the R1.2 criterion).** Costs and an overhead model fitted on the training configurations predict the measured speedup $S=T_G/T_L$ of the held-out configurations from their level counts alone. The median absolute relative error is at most 10 percent. Every held-out error above 20 percent is explained by the standard in §8.

**Secondary questions (descriptive, not part of the verdict).** Does the one-run test of §4 agree with the paired measurement? How does the measured overhead fraction compare with the budget $\beta$? Do the real AMReX level counts grow by about $r^\delta$, as Lemma 1 predicts?

## 2. Harness

- **Code.** `amrex-tutorials/ExampleCodes/Amr/Advection_AmrCore` at commit `1a73f32e10514d917333ea7a3fd54e661e232144`, built against `amrex` at `6bff801899baed998581e74ab20ee2137d6b2dee` (M3.5). The tutorial already has both schedules: `timeStepWithSubcycling` (subcycled, `adv.do_subcycle = 1`) and `timeStepNoSubcycling` with `AdvancePhiAllLevels` (global stepping, `adv.do_subcycle = 0`). It advances every cell of every level, so $a=1$.
- **Patch** (`validation/harness/Advection_AmrCore.patch`; its hash goes in `validation/BUILD.md` before the first timed execution). It changes only what this test needs:
  1. **Geometric tagging.** At level $\ell$ a cell is tagged when its center lies within $b=2$ cell widths, $2\Delta x_\ell$, of a feature $F$. This is the rule of Section 3.3 and Table 4. The phi-threshold tagging is not used. Features: point; circle; sphere (3D); filled disk (2D) or ball (3D). Center $c=(0.5123, 0.4871[, 0.5037])$, radius $0.3$. In 3D the circle lies in a plane through $c$ tilted $0.37$ rad about the $x$-axis. Distance to a filled region is zero inside it.
  2. **Constant velocity** $u=(1,1[,1])$ in place of the time-dependent swirl. Every level then sees the same maximum speed, the CFL step on level $\ell$ is exactly $\Delta t_0 r^{-\ell}$, and $Q=r^L$ holds exactly under both schedules. With the swirl, a slow region under a fine level could change the effective time ratio, which is the $r_t<r$ case of Section 2.2 and is not tested here.
  3. **Per-level wall-clock timers** (`amrex::second()`), defined in §4, written with the counts to a one-line-per-level report at the end of the run.
  4. **A timing window** that opens after one warm-up coarse interval.
  5. **Hierarchy diagnostics** at initialization: $N_\ell$, $B_\ell$, $G_\ell$ and $G^{\mathrm{cf}}_\ell$ (defined in §5).
  The kernels, interpolation, flux registers and averaging are untouched.
- **Build.** GNU make, `DIM=2` and `DIM=3`, `COMP=gnu` (g++ 13.3), `USE_MPI=FALSE`, `USE_OMP=FALSE`, double precision, CPU, AMReX's default optimized flags. The build lines go in `validation/BUILD.md`.
- **Fixed inputs** for every primary run: periodic unit square or cube; $r=2$ (`amr.ref_ratio = 2`); `amr.blocking_factor = 8`; `amr.n_error_buf = 1`; `amr.grid_eff = 0.7`; `amr.n_proper = 1`; base grid $128^2$ with `max_grid_size = 64` in 2D, and $32^3$ with `max_grid_size = 32` in 3D; `adv.cfl = 0.5`; `adv.do_reflux = 1`; `amr.regrid_int = 0`, so the hierarchy is built once at initialization and stays fixed; plot and checkpoint files off; `amr.v = 0`. The initial data are the tutorial's unchanged Gaussian.

## 3. Configurations and the held-out split

**Primary matrix**, 17 configurations, each run under both schedules:

| $d$ | Feature | $\delta$ | Depths $L$ | Role |
|---|---|---|---|---|
| 2 | point | 0 | 2, 3, 4 | training |
| 2 | circle | 1 | 2, 3, 4 | **held out** |
| 2 | disk | 2 | 2, 3, 4 | training |
| 3 | point | 0 | 2, 3 | training |
| 3 | circle | 1 | 2, 3 | **held out** |
| 3 | sphere | 2 | 2, 3 | **held out** |
| 3 | ball | 3 | 2, 3 | training |

Ten training configurations and seven held-out configurations. The split is by geometry. The model is fitted on the extremes, the point and the filled region, and predicts the curve and the surface. These intermediate cases are the ones the note's budgets are about. Holding out whole geometries tests whether fitted costs transfer to hierarchies of a shape the fit never saw. A random split of configurations would be a weaker test.

**Exploratory set**, never part of the verdict and labelled so wherever reported:
- (i) regridding on (`amr.regrid_int = 2`): circle, $L=3$, in 2D and 3D;
- (ii) $r=4$: 2D point and circle at $L=2$;
- (iii) deeper points: 2D at $L=6$, 3D at $L=4$.

## 4. Measurement protocol

- **Window.** Each run takes $n_c+1$ coarse intervals. Timers and the window clock reset when the first coarse interval ends. That is after coarse step 1 when subcycling, and after fine step $Q$ under global stepping. $n_c=4$ in 2D and $3$ in 3D. If the S3 smoke runs show a subcycled window shorter than 0.5 s for the cheapest primary configuration of a dimension, $n_c$ for that dimension is raised before S4 and recorded in `validation/BUILD.md`. Smoke runs are harness checks; their timings enter no fit, test or figure.
- **Step counts.** Subcycling uses `max_step = n_c + 1`. Global stepping uses `max_step = (n_c + 1) Q`. `stop_time` is set out of reach. Both schedules cover the same simulated interval exactly.
- **Timers,** per level $\ell$ unless noted:
  - `kern`: the velocity definition plus the flux and conservative-update loops, including the flux scaling and copies inside those loops;
  - `fill`: allocation of the ghosted state plus `FillPatch`;
  - `sync`: allocation of the flux MultiFabs, the flux-register `CrseInit`, `FineAdd` and `Reflux` (subcycled), or `average_down_faces` (global);
  - `avg`: averaging down onto level $\ell$;
  - `cfl`: the CFL check inside the level advance;
  - global, not per level: `dt` (`ComputeDt`), `diag` (the conservation sum), `regrid`.
  $K=\sum_\ell \mathtt{kern}_\ell$. $O=T-K$ is all non-kernel time, the untimed remainder included.
- **Timer-sum check.** The timers sum to between 95 and 105 percent of the window wall time $T$. This is the S3 success criterion and an S4 QC gate.
- **Repetitions and order.** Five repetitions per configuration and schedule. Order is rep-major. Within each repetition the configurations run in a fixed pseudorandom order (seed 20261008). Within each configuration the schedule order alternates by repetition: global first on odd repetitions, subcycled first on even ones. Runs are sequential, single process and single thread, with nothing else running.
- **Statistic.** The median over the five repetitions of each timed quantity.

## 5. Quantities

For a configuration with levels $\ell=0,\dots,L$, $q_\ell=2^\ell$ and $Q=2^L$:

- $N_\ell$: valid cells on level $\ell$, which equals $M_\ell$ since every cell is advanced. $B_\ell$: boxes on level $\ell$.
- $G_\ell$: cells in the 3-cell halo of each box, summed over boxes. $G^{\mathrm{cf}}_\ell$: the part of that halo not covered by level $\ell$'s own boxes. It is logged for diagnosis, not used as a regressor.
- $A^s_\ell$: advances of level $\ell$ in the window under schedule $s$. $A^L_\ell=n_c q_\ell$ and $A^G_\ell=n_c Q$. $U^s_\ell=A^s_\ell N_\ell$ is the number of cell updates.
- $T_s$, $K_s$, $O_s$: window wall time, kernel time and non-kernel time under schedule $s$, with $s=G$ for global and $s=L$ for subcycled.
- Measured speedup $S=T_G/T_L$, from the medians.
- Ideal speedup from counts, uniform cost: $S_{\mathrm{id}}=Q\sum_\ell N_\ell/\sum_\ell q_\ell N_\ell$, and the budget $\beta=1-1/S_{\mathrm{id}}$.
- Measured overhead $H=O_L-O_G$, and its fraction of global kernel work $x=H/K_G$.

**Identity checks.** The two schedules must give identical $N_\ell$ and $B_\ell$ for a configuration. The conservation sum must drift by less than $10^{-10}$ relative over the run under both schedules.

## 6. Models

A prediction for configuration $c$ under schedule $s$ is $\hat T_s=\hat K_s+\hat O_s$, and the predicted speedup is $\hat S=\hat T_G/\hat T_L$. It uses only the configuration's counts $N_\ell$, $B_\ell$, $G_\ell$ and $A^s_\ell$.

**Kernel models.** Fitted per dimension $d$ to the measured per-level kernel times.
- K1: one cost per update, pooled over schedules: $\hat K_s=c_d\sum_\ell U^s_\ell$.
- K2: per update plus per box advance, pooled: $\hat K_s=\sum_\ell A^s_\ell\,(c_d N_\ell+\kappa_d B_\ell)$.
- K2s: as K2, with separate coefficients for each schedule (Remark 3, schedule-dependent costs).
- K3: a cost per update for each level, pooled. This is the paper's $C_\ell$ taken literally: $\hat K_s=\sum_\ell C_{d,\ell}U^s_\ell$, with $C_{d,\ell}$ the median over training runs of $\mathtt{kern}_\ell/U_\ell$.

**Overhead models.** Fitted per dimension and per schedule to the measured $O_s$.
- O1, proportional: $\hat O_s=h_{d,s}\hat K_s$.
- O2, per advance plus ghost cells: $\hat O_s=\sum_\ell A^s_\ell\,(\alpha_{d,s}+\gamma_{d,s}G_\ell)$.
- O3, O2 plus a per-cell term: $\hat O_s=\sum_\ell A^s_\ell\,(\alpha_{d,s}+\gamma_{d,s}G_\ell+\eta_{d,s}N_\ell)$.

The predicted overhead of subcycling is $\hat H=\hat O_L-\hat O_G$.

## 7. Fitting and model selection (training data only)

- Coefficients are fitted by non-negative least squares on relative residuals: each row is divided by the observed value. The data are the per-configuration medians of the training configurations.
- **Selection.** For each of the twelve pairs (K1, K2, K2s, K3) × (O1, O2, O3), run leave-one-configuration-out over the ten training configurations. Refit without configuration $c$, predict $\hat S_c$, and record $e_c=|\hat S_c-S_c|/S_c$. The score is the median of $e_c$. The pair with the lowest score is selected. A pair within 0.01 of the lowest score that has fewer parameters is preferred. Any remaining tie goes in the listed order, K before O. One pair is chosen for both dimensions, scored on the pooled training errors.
- The selected pair is refitted on all ten training configurations. No held-out quantity enters fitting or selection.

## 8. Prediction freeze, evaluation and the verdict

1. **Freeze.** The S5 fit script writes $\hat S$, $\hat T_G$, $\hat T_L$, $\hat K_s$ and $\hat O_s$ for the seven held-out configurations to `validation/predictions_frozen.csv`. It reads only the training rows and the held-out counts. The file's SHA-256 is recorded in `CHANGELOG.md` before the evaluation script runs.
2. **Data discipline before the freeze.** S4's summary computes QC metrics for every run, but speedups only for training configurations. No held-out speedup is computed or displayed before the freeze.
3. **Errors.** $e_c=|\hat S_c-S_c|/S_c$ for each held-out $c$, and their median $\tilde e$.
4. **Verdict (R1.2).** Pass when $\tilde e\le 0.10$ and every held-out $e_c>0.20$ is explained.
   **Explanation standard.** Decompose the miss into kernel and overhead parts under each schedule, comparing predicted with measured $K_s$ and $O_s$. Name the component and level that carry more than half of the error. Name a mechanism the timers or counts support. An unexplained miss above 20 percent fails the criterion.
5. **Uncertainty.** Bootstrap with 2,000 resamples, seed 20261008, over repetitions within each configuration and schedule. Training resamples are refitted with the selected pair. Report 95 percent percentile intervals for each $e_c$ and for $\tilde e$.
6. **If the verdict fails,** the result is reported as found. No refit that uses held-out data counts toward the verdict. A revised model may be shown only as exploratory and must be labelled so. All twelve pairs' held-out errors are reported after the verdict, for transparency.

## 9. Secondary analyses (descriptive)

- **(a) One-run test.** From each subcycled run alone, the sufficient condition of §4 holds when $O_L<(S_{\mathrm{id}}-1)K_L$. Compare with the sign of $S-1$. A false positive, where the test holds but global stepping is faster, is reported as a failure of the test's assumption of uniform cost, together with the spread of the per-level costs. A variant replaces $S_{\mathrm{id}}$ with the cost-weighted value from the same run's $\mathtt{kern}_\ell/U_\ell$.
- **(b) Measured overhead against the budget.** $x$ against $\beta$ for each configuration, and the margin $\beta-x$. These are the AMReX points for Figure 1's band in S6.
- **(c) Real-hierarchy counts** (C5, W5-12). $M_\ell$ and the mean growth factor $(M_L/M_1)^{1/(L-1)}$ against $r^\delta$, and against the synthetic counts of Table 4 for the same features.
- **(d) Per-update cost** across levels, box sizes and schedules (Remarks 2 and 3).

## 10. QC, exclusions and deviations

- A run that aborts, violates the CFL check or returns a non-finite conservation sum is rerun once. Both attempts are logged.
- A coefficient of variation of $T$ at or above 5 percent over the five repetitions: that cell's five repetitions are rerun once. If it is still at or above 5 percent, the cell is kept and flagged.
- A timer sum outside 95 to 105 percent is flagged. If it is systematic, it is an instrumentation defect and is fixed in S3, before S4.
- An identity check failure in §5 excludes the configuration until it is explained.
- Every departure from this plan goes in `validation/deviations.md` with its date, what changed, why, and whether S4 or S5 data existed at the time.

## 11. What this test can and cannot show

It tests whether the note's accounting, with fitted costs and a fitted overhead, transfers across geometries in one code, on one core, for one explicit kernel, on a fixed hierarchy. It does not test parallel time, regridding in the primary set, elliptic synchronization, GPU launch costs, or accuracy at matched error. Section 4 of the note names each of these as outside the work model. The container is shared and has two cores, so absolute times say nothing about production machines. The test is about ratios and predictions.

## 12. Files

- `validation/analysis_plan.md`: this file.
- `validation/BUILD.md`: pins, build lines and patch hash.
- `validation/harness/Advection_AmrCore.patch`: the patch.
- `validation/run_matrix.py`: writes the inputs, runs the binaries and parses the reports.
- `validation/smoke/`: S3 smoke logs (non-analysis).
- `validation/data/runs.csv`: S4 raw data.
- `validation/fit.py`: S5 fitting.
- `validation/predictions_frozen.csv`: the S5 prediction freeze.
- `validation/deviations.md`: the deviation log.
