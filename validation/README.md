# validation: the AMReX test of Section 5

This folder holds the paired AMReX test behind Section 5, Table 5, Table A1 and Figure 3 of the paper. The analysis plan and its amendment were fixed before the timings they govern, and the held-out predictions were frozen before evaluation. [Back to the repository README](../README.md).

| Path | What it is |
|---|---|
| [`analysis_plan.md`](analysis_plan.md) | Analysis plan, fixed before any timing (SHA-256 `e4c615e3…`, cited in Section 5) |
| [`analysis_plan_v2.md`](analysis_plan_v2.md) | Its amendment, fixed before the primary runs (`cbc2f22c…`) |
| [`deviations.md`](deviations.md) | Deviation log |
| [`BUILD.md`](BUILD.md) | Build notes: pinned commits, the patch, build steps and run lengths |
| [`harness/Advection_AmrCore.patch`](harness/Advection_AmrCore.patch) | The timing harness, a patch to the Advection_AmrCore example |
| [`run_matrix.py`](run_matrix.py) | Runs the patched binary over the configurations and writes inputs, logs and CSV files |
| [`nc_map.json`](nc_map.json) | Number of coarse intervals timed in each primary configuration |
| `smoke/` ([`runs.csv`](smoke/runs.csv)) | Smoke-test runs (inputs, logs, `runs.csv`, `levels.csv`) |
| `calibration/` ([`runs.csv`](calibration/runs.csv)) | Calibration runs that set the run lengths (inputs, logs, CSV files) |
| `data/` ([`qc_summary.md`](data/qc_summary.md)) | Primary runs: inputs, logs, `runs.csv` (timings), `levels.csv` (cell counts per level), `qc.json` and `qc_summary.md` |
| [`qc_s4.py`](qc_s4.py) | Quality control of the primary runs; writes `data/qc.json` and `data/qc_summary.md` |
| [`fit.py`](fit.py) | Fitting, model selection and the prediction freeze |
| [`predictions_frozen.csv`](predictions_frozen.csv) | Frozen held-out predictions (`11d2e030…`, cited in Section 5) |
| [`predictions_frozen_selection.json`](predictions_frozen_selection.json) | Training leave-one-out scores and the selected model's coefficients |
| [`evaluate.py`](evaluate.py) | Evaluation of the frozen predictions |
| [`evaluation_s5.json`](evaluation_s5.json), [`evaluation_s5.md`](evaluation_s5.md) | Evaluation results and summary |
| [`s5_independent_check.py`](s5_independent_check.py), [`s5_independent_check_output.txt`](s5_independent_check_output.txt) | Independent recomputation of the fit, selection and errors |
| [`exploratory_s5.py`](exploratory_s5.py), `exploratory/` ([`exploratory_s5.md`](exploratory/exploratory_s5.md)) | Exploratory runs and summary after the freeze; never part of the test |
| [`fig3_validation.py`](fig3_validation.py), [`fig3_validation_output.txt`](fig3_validation_output.txt) | Figure 3 generator and its log |
| [`s6_tables.py`](s6_tables.py), [`s6_tables_output.txt`](s6_tables_output.txt), [`table5_rows.tex`](table5_rows.tex) | Table 5 generator, its log and rows |
| [`s8_appendix_table.py`](s8_appendix_table.py), [`s8_appendix_table_output.txt`](s8_appendix_table_output.txt), [`tableA1_rows.tex`](tableA1_rows.tex) | Table A1 generator, its log and rows |

Folders hold many small files. For each folder, the link opens its summary or main table; GitHub lists the rest of a folder when you open it.
