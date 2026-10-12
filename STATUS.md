# When Is Local Time Stepping Worthwhile? A Cost Analysis for Nested Adaptive Mesh Refinement

**Manuscript ID:** `hyman2026local` · **Current version:** v1_7_0 (25 pp)
**Last updated:** 2026-10-12 · **MREP score:** 78.5/100

---

## Authors

- **James M. Hyman**, Department of Mathematics, Tulane University · `mhyman@tulane.edu` · ORCID: 0000-0001-5247-5794 · *corresponding author*

---

## Target Journal

**arXiv only for this cycle (GATE A ruling A7, 2026-10-08); a journal is a deferred option** (—)

| Field | Value |
|---|---|
| Submission system | — |
| URL | — |
| Blinding | open |
| Page limit | none |
| Format class | `article` |

**Format requirements:**
- 12pt article, 0.75in margins (house default)
- natbib numeric, unsrtnat style; .bbl shipped with the arXiv source
- arXiv abstract metadata limit 1920 characters (v1_7_0 abstract, unchanged since v1_5_0, 1,642 characters of source, 1,670 with the S_ideal macro expanded)

**Required documents at submission:**
- manuscript_source
- bbl
- figure_pdfs (fig1, fig2, fig3)

---

## Submission Status

**Current status: `not_yet_submitted`**

| Field | Value |
|---|---|
| Prepared date | — |
| Submitted date | — |
| Manuscript ID (journal) | — |
| Current round | 0 |
| Editor assigned | — |
| Decision expected by | — |

> S12 (2026-10-12, branch 10): v1_7_0 credits Li and Hyman, LA-UR-06-8741 (G21 to G24); COR package, arXiv tarball and CGR archive rebuilt for v1_7_0; nothing posted or pushed by Claude. Observed 2026-10-12 (M12.5): github.com/machyman/hyman2026local is public and serves the COR v1_6_1 package contents, without the reproduce script or validation/; no arXiv listing found; to be confirmed by Mac. Branch 9 close (2026-10-12): Mac recovered Li and Hyman, LA-UR-06-8741, which derives the note's two-level formula and tests it; v1_6_1 is held from posting; rulings G21 to G24 add S12 (credit, the §3.4 correction, the citation, the accuracy sentence) in v1_7_0, with the packages rebuilt. S11 CGR v4.1.1 (2026-10-10, branch 9): repository archive hyman2026local_2026-10-10.zip (430 files, MIT license, CITATION.cff with arXiv TBD); CGR-Audit 0 CRITICAL, 0 HIGH, 0 MEDIUM, 2 LOW; CGR-FreshExtract PASS; manuscript-github source-layer gate PASS; nothing pushed. S10 COR v4.1 (2026-10-10, branch 9): Mac confirmed G12 at 13:00, so v1_6_1 replaces the AUTHOR note with the statement of responsibility and is dated October 10, 2026 (24 pp, compile clean); G18(a) covers the HIGH both S9 scorers rank first (G20); MIT license for the repository (S11). COR Phase 1 (2026-10-10, branch 9): Mac accepted the recorded state ('accept \GO', 07:52): not submitted, not on arXiv, no GitHub repository yet, no referee reports, no companion papers; public checks agree (M10.8). S10 in progress: v1_6_1 (z-bump) moves Table 3's float above the paragraph that cites it (L8, M10.9), no word changed; the G12 attestation not given, so the COR bundle waits. Branch gate after S9 (2026-10-09, branch 8): Mac approved cleanup proposal 2026-10-09 run 3 by name (3 files: the two 2026-10-09 run 1 archives and the top-level v1_5_0 PDF, whose copy is in archive/v1_5_0/) and sent \GO at 20:09, accepting G18(a): COR v4.1 next (S10) at the current readiness, with the S9 scorers' converged architecture and G16(b) recorded for a journal version (E-S9, E-S6); the G12 attestation not given. S9 (2026-10-09, branch 8): v1_6_0 (y-bump, 24 pp) restructures v1_5_0 under G17(b): Section 3.2 split into Growth law, Budgets for feature-following hierarchies and Agreement with earlier estimates; published overheads moved to open Section 4 (Published overheads and what the work model leaves out); an unnumbered measures table in 5.1; the Conclusions' first paragraph in three sentences; glosses of AMReX and the box-counting law. Two cold GSR scorers: STS 79 and 78, mean 78.5 (target 90 not met); diff check 1 HIGH and 2 MEDIUM fixed, follow-up clean of HIGH and MEDIUM. Registry: fig2 PNG hash set to the on-disk file (M9.4). Branch gate after S8 (2026-10-09, branch 7): Mac approved cleanup proposal 2026-10-09 run 2 by name (executed for 3 files: the two run5 archives and the top-level v1_4_1 PDF, whose copy is in archive/v1_4_1/; the two .pyc caches are under the protected validation/ and stay) and sent \GO at 13:51, accepting G17(b), a second text-only restructuring as S9 (COR S10, CGR S11); the G12 attestation not given. S8 (2026-10-09, branch 7): v1_5_0 (y-bump, 24 pp) restructures v1_4_1 under G15(a′): abstract novelty first, decision box in Section 1, published overheads as Section 3.3, Testing the model folded into 5.1, Section 5 cut with protocol detail in Appendix A, Table A1 counterfactuals, Figure 1 redrawn; cold GSR STS 78 (target 90 not met); diff check 5 HIGH and 7 MEDIUM fixed, follow-up 2 MEDIUM fixed. Branch gate after S7 (2026-10-09, branch 6): Mac approved cleanup run 6 by name (3 files: the two run4 archives and the top-level v1_4_0 PDF, whose copy is in archive/v1_4_0/); G15 (restructuring for readiness), G16 (natural near-break-even design) and the G12 attestation not yet ruled, carried to S8 kickoff. S7 (2026-10-09, branch 6): v1_4_1 (z-bump, 22 pp) adds the AI-use sentence on Section 5 (G10), the repository URL (G11), referee 3's ten LOW items (G14) and a Section 5.3 explanation of why no one-core run came near break-even (G9 prime (a); E-S6 kept for a journal version after the injected-cost design was withdrawn as uninformative). The responsibility marker stays until Mac attests (G12). Cold GSR v3 score STS 80, below the 90 target; restructuring proposed as G15. Diff check: no HIGH or MEDIUM remain. Branch gate after S6 (2026-10-08, branch 5): Mac approved cleanup run 5 by name (3 files: the two run3 archives and the top-level v1_3_2 PDF, whose copy is in archive/v1_3_2/); E-S6 not yet ruled, carried to S7 kickoff. S6 (2026-10-08, branch 5): v1_4_0 adds Section 5, a paired test in AMReX, with Table 5 and Figure 3, and AMReX budgets on Figure 1 (rulings G4 to G8, all option (a)). Pre-specified result: the frozen model predicts held-out speedups with median error 0.071 (PASS); post hoc, the update counts alone do as well (0.073) except for points, the model misses the components, and no configuration nears break-even. Overhead: x_C (Section 2 definition) -0.42 to -0.003, negative in all 17; time-ratio y -0.11 to 0.19, positive in 12. VER role pass on the 16 S2 entries: 0 HIGH, fixes applied. Cold referees: 4 HIGH, then 2 HIGH, then none after revision. ASM bands met. Two AUTHOR markers (repository URL; responsibility statement) block arXiv posting. arXiv categories math.NA with cross-list physics.comp-ph confirmed by Mac (2026-10-08). GATE C ruling C1: run the AMReX paired validation (Plan S3-S5) before posting. S5 (2026-10-08): the pre-registered held-out test passes R1.2 (median error 0.071, 95% CI 0.021 to 0.082; no miss above 20%); the manuscript does not report it until S6. Posting remains Mac's decision.

---

## Distribution Channels

### arXiv

| Field | Value |
|---|---|
| Posted? | ❌ Not yet |
| Identifier | — |
| URL | — |
| Posted date | — |
| Primary category | math.NA |
| Cross-list | physics.comp-ph |
| Package built? | ✅ |
| Package path | `hyman2026local_v1_6_1_arXiv.tar.gz` |

### GitHub

| Field | Value |
|---|---|
| Repository created? | ❌ Not yet |
| URL | https://github.com/machyman/hyman2026local |
| Visibility | planned |
| Canonical YAML URL | — |
| Package built? | ✅ |
| Package path | `hyman2026local_2026-10-10.zip` |

### Zenodo

| Field | Value |
|---|---|
| DOI minted? | ❌ |
| DOI | — |
| URL | — |

---

## Compile State (latest)

| Metric | Value |
|---|---:|
| Main paper pages | 25 |
| SI pages | n/a |
| Errors | 0 |
| Undefined references | 0 |
| Overfull hboxes | 0 |
| Last compiled | 2026-10-12 |

**Bibliography:** `hyman2026local.bib` (35 entries, `unsrtnat` style)

---

## Reproducibility

**Integrity check:** ✅ PASS (last run 2026-10-10)

| Registered | Count |
|---|---:|
| Figures | 3 |
| Tables | 6 |
| Deposited (code + data present, hashed) | 9 |
| Awaited (not yet provided) | 0 |
| External (hosted elsewhere) | 0 |
| Unhashed (registered, hash pending) | 0 |

*All figures and tables have deposited or externally-archived generators with verified hashes. Repository is reproducible.*

**Asset map:**

| ID | Kind | Status | Generator | Output | Verified |
|---|---|---|---|---|---|
| `fig1` | figure | deposited | `hyman2026local_reproduce.py` | `hyman2026local_fig1_budget.pdf` | 2026-10-12 |
| `fig2` | figure | deposited | `hyman2026local_reproduce.py` | `hyman2026local_fig2_dimension.pdf` | 2026-10-12 |
| `fig3` | figure | deposited | `validation/fig3_validation.py` | `hyman2026local_fig3_validation.pdf` | 2026-10-08 |
| `tab1` | table | deposited | `hyman2026local_reproduce.py` | `hyman2026local_reproduce_output.txt` | 2026-10-12 |
| `tab2` | table | deposited | `hyman2026local_reproduce.py` | `hyman2026local_reproduce_output.txt` | 2026-10-12 |
| `tab3` | table | deposited | `hyman2026local_reproduce.py` | `hyman2026local_reproduce_output.txt` | 2026-10-12 |
| `tab4` | table | deposited | `hyman2026local_reproduce.py` | `hyman2026local_reproduce_output.txt` | 2026-10-12 |
| `tab5` | table | deposited | `validation/s6_tables.py` | `validation/table5_rows.tex` | 2026-10-08 |
| `tabA1` | table | deposited | `validation/s8_appendix_table.py` | `validation/tableA1_rows.tex` | 2026-10-09 |

---

## File Manifest (Current Working Set)

This package contains:
- `hyman2026local_v1_7_0.tex` — main manuscript source
- `hyman2026local.bib` — bibliography
- `hyman2026local_v1_6_1.pdf` — v1_6_1 PDF (24 pp); .bbl alongside
- `hyman2026local_COR_2026-10-10.zip` — COR v4.1 Overleaf-ready package (tex, bib, bbl, three figure PDFs, README, YAML, CHANGELOG, arXiv metadata); compiles in isolation
- `hyman2026local_v1_6_1_arXiv.tar.gz` — arXiv source (tex, bbl, three figure PDFs); compiles in isolation without bibtex
- `hyman2026local_v1_6_1_arXiv_metadata.txt` — title, author, categories, comments and the abstract with S_ideal expanded (1,670 characters) for the arXiv form
- `hyman2026local_Session10_Report.md` — Session 10 report (COR v4.1) with gate log
- `hyman2026local_2026-10-10.zip` — CGR v4.1.1 repository archive for machyman/hyman2026local (MIT); audit and fresh extract pass; not pushed
- `hyman2026local_Session11_Report.md` — Session 11 report (CGR v4.1.1) with gate log
- `hyman2026local_RunReport_2026-10-10.md` — run report with the excellence assessment
- `archive/v1_6_0/` — the v1_6_0 version set (tex, pdf, bbl, generator, log, three figures)
- `archive/v1_5_0/` — the v1_5_0 version set (tex, pdf, bbl, generator, log, three figures)
- `hyman2026local_GSR_S9A_2026-10-09.md` — S9 cold GSR v3 score by scorer A on v1_6_0 (STS 79) with actions
- `hyman2026local_GSR_S9B_2026-10-09.md` — S9 cold GSR v3 score by scorer B on v1_6_0 (STS 78) with actions
- `hyman2026local_DiffCheck_S9_2026-10-09.md` — S9 independent check of v1_5_0 to v1_6_0 (1 HIGH and 2 MEDIUM fixed; follow-up round found none)
- `hyman2026local_Session9_Report.md` — Session 9 report (second restructuring under G17(b), v1_6_0) with gate log
- `archive/v1_4_1/` — the v1_4_1 version set (tex, pdf, bbl, generator, log, three figures)
- `hyman2026local_GSR_S8_2026-10-09.md` — S8 cold GSR v3 readiness score on v1_5_0 (STS 78) with actions
- `hyman2026local_DiffCheck_S8_2026-10-09.md` — S8 independent check of v1_4_1 to v1_5_0 (5 HIGH, 7 MEDIUM fixed; follow-up round with 2 MEDIUM fixed)
- `hyman2026local_Session8_Report.md` — Session 8 report (restructuring under G15(a′), v1_5_0) with gate log
- `validation/s8_appendix_table.py` — Table A1 rows, the post hoc counterfactual overheads (output in s8_appendix_table_output.txt, rows in tableA1_rows.tex)
- `archive/v1_4_0/` — the v1_4_0 version set (tex, pdf, bbl, generator, log, three figures)
- `hyman2026local_GSR_S7_2026-10-09.md` — S7 cold GSR v3 readiness score (STS 80) with actions toward 90
- `hyman2026local_DiffCheck_S7_2026-10-09.md` — S7 independent check of the v1_4_0 to v1_4_1 edits (fixes applied; follow-up clean)
- `hyman2026local_Session7_Report.md` — Session 7 report (author items, LOW items, readiness score) with gate log
- `archive/v1_3_2/` — the v1_3_2 version set (tex, pdf, bbl, arXiv package, generator, log, both figures)
- `hyman2026local_VER_RolePass_S6_2026-10-08.md` — S6 VER role pass on the 16 S2 bibliography entries (0 HIGH; three wording fixes; Athena++ addendum)
- `hyman2026local_Referee_S6_2026-10-08.md` — S6 cold referee pass 1 (4 HIGH; led to rulings G7, G8)
- `hyman2026local_Referee2_S6_2026-10-08.md` — S6 cold referee pass 2 (2 HIGH, fixed in the text)
- `hyman2026local_Referee3_S6_2026-10-08.md` — S6 cold referee pass 3 (no HIGH; MEDIUM fixes applied)
- `validation/s6_tables.py` — Table 5 rows, overhead decomposition, level ratios and the post hoc referee checks (output in s6_tables_output.txt, rows in table5_rows.tex)
- `hyman2026local_Session6_Report.md` — Session 6 report (validation section, v1_4_0, referee passes) with gate log
- `hyman2026local_v1_3_2.bbl` — compiled bibliography (shipped with the arXiv source)
- `hyman2026local_fig2_dimension.pdf` — printed Figure 1, budget against feature dimension (PNG copy alongside)
- `archive/v1_2_1/` — the v1_2_1 version set (tex, pdf, bbl, arXiv package, generator, log, Figure 1)
- `archive/v1_3_0/` — the v1_3_0 version set (tex, pdf, bbl, arXiv package, generator, log, both figures)
- `hyman2026local_v1_3_0_arXiv.tar.gz` — superseded v1_3_0 arXiv package (copy in archive/v1_3_0/)
- `RTP_StressTest_Review_hyman2026local_2026-10-08.md` — WU7 RTP measures for the RTP development conversation
- `HANDOFF_hyman2026local_MREP_WU7.md` — MREP WU7 handoff
- `HANDOFF_hyman2026local_MREP_WU8.md` — MREP WU8 handoff (v1_3_0)
- `HANDOFF_hyman2026local_Session2.md` — branch handoff and manifest (Session 2 closing; startup prompt for branch 3)
- `CLEANUP_PROPOSAL_hyman2026local_2026-10-08_run2.md` — cleanup proposal run 2; approved by Mac by name and executed 2026-10-08 (4 outputs files, the recovered folder and /home/claude/v_s2 removed)
- `hyman2026local_reproduce.py` — generator for Tables 1-4, both figures and the overhead bracket (exact arithmetic; deterministic)
- `hyman2026local_reproduce_output.txt` — log of the generator run that the tables quote
- `hyman2026local_fig1_budget.pdf` — printed Figure 2, budget against depth (PNG copy alongside)
- `hyman2026local_v1_3_2_arXiv.tar.gz` — arXiv source package (tex + bbl + two figures); builds cleanly; not posted
- `hyman2026local_v1_3_1_arXiv.tar.gz` — superseded v1_3_1 arXiv package (copy in archive/v1_3_1/)
- `archive/v1_3_1/` — the v1_3_1 version set (tex, pdf, bbl, arXiv package, generator, log, both figures)
- `hyman2026local_v1_2_1_arXiv.tar.gz` — superseded v1_2_1 arXiv package (copy in archive/v1_2_1/)
- `hyman2026local_MasterPlan.md` — Master Plan for session-autopilot (rev 20; S7 closed, v1_4_1; G9 to G14 ruled; G15, G16 and the G12 attestation pending; next S8 in branch 7)
- `hyman2026local_Session2_Report.md` — Session 2 report (MREP cycle WU0-WU8, v1_3_0) with gate log
- `hyman2026local_Session3_Report.md` — Session 3 report (AMReX validation harness) with gate log
- `hyman2026local_Session4_Report.md` — Session 4 report (paired AMReX runs, QC, training-set observations) with gate log
- `validation/data/` — S4 primary matrix and plan-section-10 reruns (runs.csv, levels.csv, logs, inputs, qc.json, qc_summary.md)
- `validation/qc_s4.py` — S4 quality control; training-only speedups before the freeze
- `validation/fit.py` — S5 fitting, selection and prediction freeze (reads no held-out timing)
- `validation/evaluate.py` — S5 evaluation after the freeze hash is recorded
- `validation/analysis_plan.md` — AMReX validation analysis plan v1, hashed before any timed run (SHA-256 e4c615e3b68fc1d4)
- `validation/analysis_plan_v2.md` — pre-data amendment v2 (window length per configuration; 17-digit conservation sums; SHA-256 cbc2f22c647c52f0)
- `validation/BUILD.md` — AMReX pins, build lines, patch and binary hashes, window map
- `validation/harness/Advection_AmrCore.patch` — harness v2 patch to amrex-tutorials Advection_AmrCore (tagging, constant velocity, timers, window)
- `validation/run_matrix.py` — writes inputs, runs the harness, parses its reports into runs.csv and levels.csv
- `validation/nc_map.json` — timing-window length per configuration (amendment v2)
- `validation/smoke/` — S3 smoke runs (non-analysis)
- `validation/calibration/` — S3 calibration runs, subcycled only (non-analysis)
- `hyman2026local_MREP_Kit.zip` — MREP kit (bundle v6.31-preview) and launch prompt for the S2 review cycle
- `HANDOFF_hyman2026local_MREP_WU0.md` — MREP WU0 pre-flight report and MSHP handoff (GATE A rulings)
- `HANDOFF_hyman2026local_MREP_WU1.md` — MREP WU1 verification handoff
- `HANDOFF_hyman2026local_MREP_WU2.md` — MREP WU2 bibliography handoff (GATE B)
- `hyman2026local_MREP_Report_2026-10-08.md` — MREP findings report, FROZEN at WU6 (SHA-256 831cf444d9ff7ba0)
- `hyman2026local_Verification_Register_2026-10-08.md` — WU1 verification register (equations, statements, proofs, numbers)
- `hyman2026local_VER_Report_2026-10-08.md` — WU2 bibliography, BKS and LRV report
- `hyman2026local_WU3_Structure_Report_2026-10-08.md` — WU3 GSR, NTA, FTQ report and blind RTP-draft pass
- `hyman2026local_WU4_Prose_Report_2026-10-08.md` — WU4 SPRE diagnostic report
- `hyman2026local_HR_Report_2026-10-08.md` — WU5 cold HR v2.1.1 panel report
- `hyman2026local_PathToExceptional_2026-10-08.md` — WU6 IMP synthesis, grade and path to exceptional
- `HANDOFF_hyman2026local_MREP_WU3.md` — MREP WU3 handoff
- `HANDOFF_hyman2026local_MREP_WU4.md` — MREP WU4 handoff
- `HANDOFF_hyman2026local_MREP_WU5.md` — MREP WU5 handoff
- `HANDOFF_hyman2026local_MREP_WU6.md` — MREP WU6 handoff (GATE C; frozen report hash)
- `hyman2026local_render_readme.py` — renders this README from the YAML (--check diffs)
- `hyman2026local_ImprovementMemo_v1_2_0.md` — excellence-first improvement memo
- `hyman2026local_Session1_Report.md` — Session 1 report with gate log
- `HANDOFF_hyman2026local_Session1.md` — branch handoff and manifest
- `verification/` — independent referee check scripts, plus Claude's symbolic check and ASM helpers
- `archive/` — ChatGPT v1.1.0 package (rollback anchor), v1_2_0 snapshot, pilot diagnosis
- `CLEANUP_PROPOSAL_hyman2026local_2026-10-08.md` — cleanup proposal; approved by Mac and executed 2026-10-08 (2 files deleted; copies in the BRANCH snapshot)
- `HANDOFF_hyman2026local_Session4.md` — branch handoff and manifest (Session 4 closing; startup prompt for branch 4)
- `CLEANUP_PROPOSAL_hyman2026local_2026-10-08_run3.md` — cleanup proposal run 3; approved by Mac by name and executed 2026-10-08 (6 files)
- `BRANCH_Snapshot_hyman2026local_2026-10-09_run3.zip` — pre-cleanup snapshot for 2026-10-09 run 3 (599 files)
- `BRANCH_Recovery_hyman2026local_2026-10-09_run3.zip` — recovery archive for branch 9
- `CLEANUP_PROPOSAL_hyman2026local_2026-10-09_run3.md` — cleanup proposal 2026-10-09 run 3; approved by Mac by name and executed 2026-10-09 (3 files)
- `BRANCH_Snapshot_hyman2026local_2026-10-12.zip` — pre-cleanup snapshot for 2026-10-12 (626 files)
- `BRANCH_Recovery_hyman2026local_2026-10-12.zip` — recovery archive for branch 10
- `CLEANUP_PROPOSAL_hyman2026local_2026-10-12.md` — cleanup proposal 2026-10-12; approved by Mac by name and executed 2026-10-12 (3 files)
- `HANDOFF_hyman2026local_Session11.md` — handoff for branch 10 (S12 first)
- `references/Li_Hyman_LA-UR-06-8741_local_vs_locked.pdf` — Li and Hyman, Local Time Step versus Locked Time Step for Adaptive Mesh Refinement, LA-UR-06-8741 (the source behind rulings G21 to G24)
- `HANDOFF_hyman2026local_Session7.md` — branch handoff and manifest (Session 7 closing; startup prompt for branch 7)
- `HANDOFF_hyman2026local_Session8.md` — branch handoff and manifest (Session 8 closing; startup prompt for branch 8)
- `HANDOFF_hyman2026local_Session9.md` — branch handoff and manifest (Session 9 closing; startup prompt for branch 9)
- `CLEANUP_PROPOSAL_hyman2026local_2026-10-09_run2.md` — cleanup proposal 2026-10-09 run 2; approved by Mac by name and executed 2026-10-09 (3 of 5 files executed; the two protected .pyc caches stay; the v1_4_1 PDF has copies in archive/v1_4_1/ and the run2 snapshot)
- `CLEANUP_PROPOSAL_hyman2026local_2026-10-08_run5.md` — cleanup proposal run 5; approved by Mac by name and executed 2026-10-08 (3 files; copies in the run5 snapshot)
- `HANDOFF_hyman2026local_Session6.md` — branch handoff and manifest (Session 6 closing; startup prompt for branch 6)
- `CLEANUP_PROPOSAL_hyman2026local_2026-10-08_run4.md` — cleanup proposal run 4; approved by Mac by name and executed 2026-10-08 (14 files; count erratum appended)
- `HANDOFF_hyman2026local_Session5.md` — branch handoff and manifest (Session 5 closing; startup prompt for branch 5)
- `protocols/` — COR v4.1 and CGR v4.1.1 protocol texts (ruling R3.1; Plan S8 and S9)
- `archive/branch1_superseded/` — early Session1_Report.md and HANDOFF_2.md, kept from the released branch-1 snapshot (M4.1)
- `SHA256SUMS` — checksums of every file except itself, the handoff, the changelog and the BRANCH archives
- `hyman2026local_fig3_validation.pdf` — Figure 3 (S5), measured against predicted speedup and held-out errors; PNG copy alongside; enters the manuscript at S6
- `validation/predictions_frozen.csv` — S5 prediction freeze, seven held-out configurations (SHA-256 11d2e03060d6de2b, recorded before evaluation)
- `validation/predictions_frozen_selection.json` — S5 training leave-one-out scores for the twelve pairs and the selected pair's coefficients
- `validation/evaluation_s5.json` — S5 evaluation (R1.2 verdict inputs, bootstrap, all twelve pairs, secondary analyses); .md summary alongside
- `validation/fig3_validation.py` — Figure 3 generator (log in fig3_validation_output.txt)
- `validation/s5_independent_check.py` — independent recomputation of the S5 freeze, fit, selection and errors (output alongside)
- `validation/deviations.md` — deviation log (D1 exploratory windows; D2 Figure 1 presentation; D3 overhead measure)
- `validation/exploratory/` — exploratory set after the freeze (calibration, paired data, window map, summary); never part of the verdict
- `validation/exploratory_s5.py` — exploratory summary with the frozen pair's predictions
- `hyman2026local_Session5_Report.md` — Session 5 report (fit, freeze, evaluation, Figure 3, exploratory set) with gate log
- `recovered_scratchpad_branch3/` — 6 branch-3 scratchpad files kept by cleanup run 4 (patch edit scripts, branch tools, S4 console log) plus a README
- `recovered_scratchpad_branch8/` — the S9 text both GSR scorers read, the S9 diff check's input and the G17(b) ruling text, copied from the scratchpad at S10 (M10.3), with a README
- `MANUSCRIPT_STATUS.yaml` — structured status + asset registry (this README's source of truth)
- `CHANGELOG.md` — chronological change record
- `README.md` — this file (rendered from YAML; do not edit directly)

Every file that backs a manuscript figure or table is registered in `assets:` and is protected from deletion during branch cleanup.

---

## Compilation

### Main paper

```
pdflatex hyman2026local_v1_7_0.tex
bibtex hyman2026local_v1_7_0
pdflatex hyman2026local_v1_7_0.tex
pdflatex hyman2026local_v1_7_0.tex
```

---

*This README is rendered from `MANUSCRIPT_STATUS.yaml`. To update, edit the YAML and re-render via the manuscript-tracking skill. Do not edit this README directly.*
