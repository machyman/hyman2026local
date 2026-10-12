# hyman2026local: deviation log for the AMReX validation

Every departure from `validation/analysis_plan.md` (v1, SHA-256 `e4c615e3…`) and its amendment `validation/analysis_plan_v2.md` (`cbc2f22c…`) is recorded here with its date, what changed, why, and what data existed at the time (plan v1 §10).

## D1. Window length for the exploratory set (2026-10-08, S5, branch 4)

- **What changed.** Amendment v2 set the timing window per configuration, $n_c(c)=\max(n_c^0(d), \lceil 2.0\,\mathrm{s}/\tau_L(c)\rceil)$, from one subcycled calibration run of each **primary** configuration. It did not name the six exploratory configurations of plan v1 §3. The same rule is applied to them: one subcycled calibration run each at the default $n_c^0$ ($4$ in 2D, $3$ in 3D), then five paired repetitions at the resulting $n_c$. Master Plan minor ruling M5.4.
- **How.** `run_matrix.py`'s `calibrate` mode covers the primary configurations only, so the six calibration runs used its `smoke` mode with `--schedules subcycle` (run ids `smoke_*`, in `validation/exploratory/calibration/`). The resulting map is `validation/exploratory/nc_map_exploratory.json` (SHA-256 `bcd63180e50b5362…`), with values from 5 to 855. The paired runs are in `validation/exploratory/data/`.
- **Why.** Without it the cheap exploratory configurations would time windows of a few milliseconds, which v2 showed are too short to time. Applying v2's rule keeps the exploratory data comparable with the primary data.
- **Data at the time.** All S4 data existed. The S5 prediction freeze (`validation/predictions_frozen.csv`, SHA-256 `11d2e030…`) and the evaluation (`validation/evaluation_s5.json`) were complete, so no exploratory run could inform the fit, the selection or the verdict (plan v1 §3; Plan M3.10). No exploratory configuration had been run.
- **Effect on the verdict.** None. Exploratory results are descriptive and are labelled exploratory wherever they are reported.

## D2. Presentation of secondary analysis (b) in Figure 1 (2026-10-08, S6, branch 5)

- **What changed.** Plan v1 §9(b) said the measured overhead fractions $x=H/K_G$ would be the AMReX points for Figure 1's band of published overheads. All 17 are negative ($-0.45$ to $-0.06$), so they cannot be drawn on the figure's logarithmic axis. Figure 1 instead marks the 17 finite-depth budgets $\beta$ at their $\delta$ on the $r=2$ panel, and a label in the band and the caption state the measured range of $x$. The values of $x$ and $\beta$ for every configuration are in Table 5. Master Plan ruling G6(a) (Mac, `\GO`, 2026-10-08 20:30 MDT).
- **Data at the time.** All S4 and S5 data, the freeze and the evaluation existed. The change is to presentation only.
- **Effect on the verdict.** None. Secondary analyses are descriptive.

## D3. The overhead reported in the manuscript (2026-10-08, S6, branch 5)

- **What changed.** Plan v1 §5 defined the measured overhead as $H=O_L-O_G$, the difference in time outside the update kernels, with $x=H/K_G$. After two cold referee passes, v1_4_0 reports as its headline the overhead as Section 2 of the note defines it: the difference between the schedules in the time spent beyond one cost per update $C=K_G/U_G$, $H_C=T_L-T_G+C(U_G-U_L)$, with $x_C=H_C/K_G$ from $-0.422$ to $-0.003$. It also reports the time-ratio measure $y=1/S-1/S_{\mathrm{id}}$ ($-0.114$ to $0.191$), which matches how the published overheads are computed. The plan's $x$ ($-0.45$ to $-0.06$) is reported as the non-kernel part of $H_C$. Figure 1's label now quotes the $x_C$ range, which supersedes the range quoted in D2. Master Plan ruling G8(a) (Mac, `\GO`, 2026-10-08 21:29 MDT). All three quantities are computed by `validation/s6_tables.py`.
- **Data at the time.** All S4 and S5 data, the freeze and the evaluation existed.
- **Effect on the verdict.** None. The R1.2 verdict concerns the speedup, and secondary analyses are descriptive.
