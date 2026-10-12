# Changelog: hyman2026local

All notable session-level changes to this manuscript are recorded here. The most recent entries appear first.

This file is maintained by the manuscript-tracking skill. One entry per working session.

---

## 2026-10-12: Session 13, part 1 (repository reset to the CGR v1_7_0 archive; post-push check PASS; Stage B pending; branch 11)

v1_7_0 unchanged. Branch 11 opened on the Session 12 startup prompt; STEP 4 reconciled cleanly (M13.1) and STEP 6 held on the repository state.

### Rulings and answers
- M12.5 settled (M13.2): Mac uploaded the COR archive to the repository by mistake instead of the CGR archive. No Zenodo connection.
- Mac approved by name (15:09): force-push the v1_7_0 commit to `machyman/hyman2026local` main, replacing commits `63bde79` and `5ca6418` (M13.3).

### Protocols run
- manuscript-github post-push check on a fresh download (`crv.py`, CRV v1.0): 430/430 files byte-identical to `hyman2026local_2026-10-12.zip`; one commit, `d41e7cf`, tree `ad90d9c4…`; P1 4/4 printed paths, P2 57 links; 2 MEDIUM by design, 1 LOW; gate PASS. The v1_6_1 files return 404 over raw; the v1_7_0 files return 200.

### Distribution
- GitHub: `distribution.github` set to created, public. The repository serves v1_7_0. Not on arXiv yet.

### Files added / changed / removed
- Added: `hyman2026local_PostPush_S13_2026-10-12.md`, `hyman2026local_repo_reset.sh`
- Changed: `MANUSCRIPT_STATUS.yaml`, `README.md` (re-rendered), `hyman2026local_MasterPlan.md` (rev 36), `SHA256SUMS`, this file
- Removed: none

### Next
- Mac posts v1_7_0 to arXiv from `hyman2026local_v1_7_0_arXiv.tar.gz` with `hyman2026local_v1_7_0_arXiv_metadata.txt`; then S13 part 2, CGR Stage B. The recovery archive predates these records; the next `\BRANCH` rebuilds it.

## 2026-10-12: Session 12 (Li and Hyman credit under G21 to G24; v1_6_1 to v1_7_0; COR, arXiv and CGR packages rebuilt; branch 10)

**Versions:** main v1_6_1 → v1_7_0 (y-bump)
**Status:** not_yet_submitted. Nothing was posted or pushed by Claude. Observed 2026-10-12: the public repository serves the COR v1_6_1 contents (M12.5), pending Mac's confirmation

### Protocols run
- Startup STEPs 0 to 6. STEP 4 was clean (M12.1). Recovery archive observed as `44defe17…`. The branch again opened on a message carrying message 1's zip
- K: tracking consistent (M12.2); path forward (M12.3). R decided the minor items within G21 to G24 (M12.4)
- E1: `archive/v1_6_1/` holds the v1_6_1 set (11 files, byte-equal). `hyman2026local_v1_7_0.tex` changes 8 lines of v1_6_1:
  - `\date`
  - §1: the cite, the report's derivation, tests and conclusion, the 2003 remark, point and line refinement
  - §1 (ii): the closed forms extend the two- and three-level formulas of Li and Hyman to deep hierarchies
  - §2: credit, with covered coarse cells advanced and no overhead
  - §3.1: their Eq. (3)
  - §3.4: their Eq. (8) as the identity with δ = 0, a = 1 and a full base grid; equal counts hold only around a point; their tests and the agreement read from their figures (about 7 and 13 percent), replacing the "not recorded" sentence
  - §4.2: the advected-vortex dispersion sentence (G24)
- Bibliography: `li2002local` replaced by `li2006local` (LA-UR-06-8741, 2006, note on the 2002 version; VER verified from the primary document)
- E2: clean build in 3 passes: 25 pp, 0 errors, 0 undefined, 0 warnings, 0/0 boxes, 34/35/34, 0 bibtex warnings, 0 em dashes. Table rows still at .tex lines 364 and 460. Abstract unchanged (1,642 / 1,670)
- ASM: mean 23.0, short 8.2%, run 3, commas 5.42, connectives 0.49, nominalizations 2.62, no dashes, all inside the research-article bands. A first draft measured mean 23.1, and two sentences were shortened
- E3: the reproduce script now names v1_7_0 (`78168efd…`). Its log is identical and Figures 1 and 2 regenerate byte for byte (PNGs pixel-identical). The registry's six references were updated; integrity 38/38
- E4: independent diff check, `hyman2026local_DiffCheck_S12_2026-10-12.md`. Round 1 found 0 HIGH, 5 MEDIUM and 8 LOW; the follow-up found 0 HIGH, 1 MEDIUM and 3 LOW. Every MEDIUM was fixed. There is no unclaimed change, and every Li and Hyman statement traces to the report
- E5, COR v4.1: `hyman2026local_COR_2026-10-12.zip` (`5fa2245a…`), `hyman2026local_v1_7_0_arXiv.tar.gz` (`43550976…`) and the metadata file (25 pages). Each compiles in isolation: 25 pp, 0 errors and warnings
- E6, CGR v4.1.1: `hyman2026local_2026-10-12.zip` (`a2dc9f20…`, 430 files), the S11 tree with the v1_7_0 files, the bumped script, the README, `CITATION.cff` and STATUS. CGR-Audit: 0 CRITICAL, 0 HIGH, 0 MEDIUM, 2 LOW. FreshExtract: PASS (25 pp; every log and rows file identical; figure PDFs byte-identical). manuscript-github: gate PASS (0 CRITICAL, 0 HIGH, 2 MEDIUM by design, 1 LOW)

### Files added / changed / removed
- Added: `hyman2026local_v1_7_0.tex`, `.bbl`, `.pdf`; `hyman2026local_v1_7_0_arXiv.tar.gz`; `hyman2026local_v1_7_0_arXiv_metadata.txt`; `hyman2026local_COR_2026-10-12.zip`; `hyman2026local_2026-10-12.zip`; `hyman2026local_DiffCheck_S12_2026-10-12.md`; `archive/v1_6_1/` (11 files); `hyman2026local_Session12_Report.md`; `hyman2026local_RunReport_2026-10-12.md`
- Changed: `hyman2026local.bib` (`ef960212…`); `hyman2026local_reproduce.py` (comment lines only); Master Plan (rev 33 to 34); YAML (version, distribution, `cgr`, `protected_extra`, `readme_extra_files`, metadata); README (re-rendered); SHA256SUMS; this file
- Removed: none

### After the run's exit (2026-10-12)
- Mac's reply at 10:04: the cleanup proposal approved by name, with `\GO`. `\GO` accepts the recommendations; it does not confirm the repository state (M12.5), which stays open (M12.8)
- S13 added: the post-push check and CGR Stage B, waiting on Mac's push and posting (M12.9)

### Branch (\BRANCH v1_18_0)
- Phase 0: key `hyman2026local` by the substrate stem; about 45% used. Phase 1: 652 files, 70,873,144 bytes, no zero-byte files; highest v1_7_0, also the newest
- Phase 2: clean build of v1_7_0: 3 passes, 25 pp, 0 errors, warnings and boxes, 34/35/34, 0 bibtex warnings, 0 em dashes; `.bbl` and PDF text identical to outputs
- Phase 3: `BRANCH_Snapshot_hyman2026local_2026-10-12_run2.zip`, 648 files, count diff empty, `14ffc65c…`
- Phase 4 and 5a: `CLEANUP_PROPOSAL_hyman2026local_2026-10-12_run2.md` approved by name (10:04); removed `BRANCH_Recovery_hyman2026local_2026-10-09_run3.zip`, `BRANCH_Snapshot_hyman2026local_2026-10-09_run3.zip`, `hyman2026local_v1_6_1.pdf` (copy in `archive/v1_6_1/`); 651 files remain
- Phase 5b: `HANDOFF_hyman2026local_Session12.md`, this section, the Session 12 report's closing section, Plan, YAML, README, SHA256SUMS. Phase 5c: `BRANCH_Recovery_hyman2026local_2026-10-12_run2.zip`
- Phase 6: 11/11. Manifest 653/653; self-inclusion 5/5; hashes and F-1 at 68,292 bytes; `/home/claude` 0 work files; prompt paths 21, one adjudicated: `hyman2026local_v1_6_1.pdf` appears in the prompt's prose as deleted, with its copy in `archive/v1_6_1/` (P6); numbers 12/12/12/12/12; archives 649 and 648 files, byte-diff empty; cross-file; currency; first task S13; registry 38/38 and every `readme_extra_files` path on disk
- Phase 7: startup prompt displayed (branch point message 2; first task S13, which waits on Mac's push)
- Phase 8 pass 1 (cold): 0 discrepancies; recovery byte-diff empty over 649 files; README render matches; no file newer than the archive. Recovery build before the final one: `390b3c6c…` (first seal). Closing record written and re-sealed, then Phase 8 pass 2

### Next
- Branch 11 opens at message 2. S13 waits on Mac: confirm the repository state, replace its contents with `hyman2026local_2026-10-12.zip`, then the post-push check; post v1_7_0 to arXiv, then CGR Stage B

## 2026-10-10: Session 11 (CGR v4.1.1: GitHub repository archive; v1_6_1 unchanged; branch 9)

**Versions:** main v1_6_1 (unchanged)
**Status:** not_yet_submitted; repository not yet created (Mac's); nothing pushed

### Protocols run
- B after S10: about 58% used; S11 run in this branch on Mac's instruction, kept lean (M10.12)
- V on S10 passed from disk (M11.1); R decided S11's items (M11.2)
- CGR v4.1.1 Phase 1: repository assembled (430 files, 2.35 MB unpacked): the manuscript set, the reproduce script and log, `validation/` without `__pycache__`, `README.md`, `LICENSE` (MIT, Mac's choice), `CITATION.cff` (arXiv TBD, Stage A), `requirements.txt`, `MANUSCRIPT_STATUS.yaml`, `STATUS.md` (rendered dashboard), `CHANGELOG.md`, the renderer, and index pages in `validation/`, `validation/data/` and `validation/exploratory/`
- Phase 2, CGR-Audit (block-on-critical): checks 3, 4a (all printed and promised names resolve; URL agrees with CITATION.cff), 4b (every file documented), 4c (every labelled table and figure registered, registry 38/38, printed hashes `e4c615e3`, `cbc2f22c`, `11d2e030` match their files), 5 (MIT; no contradictory notice), 7: 0 CRITICAL, 0 HIGH, 0 MEDIUM, 2 LOW (M11.3)
- Phase 3, CGR-FreshExtract: PASS. Clean directory, `env -i`, one chained shell: 2 pdflatex passes, 24 pp, 0 file-not-found, 0 undefined; reproduce log, Table 5 and A1 rows and logs, Figure 3 log identical; three figure PDFs byte-identical; no `.pyc` written
- manuscript-github (pre-push): source-layer gate PASS after the README entries became links and three index pages were added (M11.4)
- Phase 4: `hyman2026local_2026-10-10.zip`, SHA-256 `3ccc86be…` (first build `da006457…` replaced before any record named it)

### Files added / changed / removed
- Added: `hyman2026local_2026-10-10.zip`, `hyman2026local_Session11_Report.md`, `hyman2026local_RunReport_2026-10-10.md`
- Changed: Master Plan (rev 30 to 31), YAML (`distribution.github`, `cgr` block), README (re-rendered), SHA256SUMS, this file
- Removed: none

### After the run's exit (2026-10-12)
- Mac supplied Li and Hyman, "Local Time Step versus Locked Time Step for Adaptive Mesh Refinement", LA-UR-06-8741 (`references/`, M11.5). It derives the note's two-level formula and an equal-count three-level formula, and tests them in 1D and 2D. v1_6_1's §3.4 sentence that those configurations are not recorded is wrong; v1_6_1 is held from posting
- Rulings G21 to G24 (`\GO`, 09:05): credit and reframe, correct §3.4 and cite the report in §1, cite LA-UR-06-8741 (2006, a 2002 version circulated; R1.6 reversed), one accuracy sentence in §4.2. Added as S12 (v1_7_0, then the packages rebuilt); the exit criterion gains S12

### Branch (\BRANCH v1_18_0)
- Phase 0: key `hyman2026local` by the substrate stem; about 74% used. Phase 1: 630 files, 57,567,558 bytes; highest v1_6_1, also the newest
- Phase 2: clean build of v1_6_1: 3 passes, 24 pp, 0 errors, warnings and boxes, 33/35/33, 0 bibtex warnings, 0 em dashes; `.bbl` and PDF text identical to outputs
- Phase 3: `BRANCH_Snapshot_hyman2026local_2026-10-12.zip`, 626 files, count diff empty, `6879b26b…`
- Phase 4 and 5a: `CLEANUP_PROPOSAL_hyman2026local_2026-10-12.md` approved by name (09:11); removed `BRANCH_Recovery_hyman2026local_2026-10-09_run2.zip`, `BRANCH_Snapshot_hyman2026local_2026-10-09_run2.zip`, `hyman2026local_v1_6_0.pdf` (copy in `archive/v1_6_0/`); 629 files remain
- Phase 5b: `HANDOFF_hyman2026local_Session11.md`, this section, the Session 11 report's closing section, Plan, YAML, README, SHA256SUMS. Phase 5c: `BRANCH_Recovery_hyman2026local_2026-10-12.zip`
- Phase 6: 11/11 (manifest 631/631; self-inclusion 5/5; hashes and F-1 at 62,328 bytes; `/home/claude` 0 work files; prompt paths 20, one adjudicated: `hyman2026local_v1_6_0.pdf` appears in the prompt's prose as deleted, with its copy in `archive/v1_6_0/` (P6); numbers 11/11/11/11/11; archives 627 and 626 files, byte-diff empty; cross-file; currency; first task; registry 38/38 and every `readme_extra_files` path on disk)
- Phase 8 pass 1 (cold): 0 discrepancies. Recovery build before the final one: `877856b5…` (first seal). Closing record written and re-sealed, then Phase 8 pass 2

### Next
- Branch 10 opens at message 2 with S12 kickoff (gate K): the Li and Hyman credit in v1_7_0 under G21 to G24, then the COR, arXiv and CGR packages rebuilt

## 2026-10-10: Session 10 (COR v4.1: Overleaf-ready package and arXiv tarball; v1_6_1; branch 9)

**Versions:** main v1_6_0 → v1_6_1 (z-bump: Table 3's float moved for L8; the AUTHOR note replaced by the statement of responsibility under G12; date October 10, 2026)
**Status:** not_yet_submitted; Mac re-confirmed nothing on arXiv and no repository yet

### Protocols run
- Branch 9 startup STEPs 0 to 6: STEP 4 clean (604/604; F-1 pass at 54,843 bytes, `a001bf41…`; handoff `40acf9dd…` equals its stanza; recovery byte-diff empty over 600 files; three PNGs pixel-identical, caBX only); recovery archive run3 observed `8a507dddfb7776412888346149cf8102138acdeaa8a6c228ea2e92f24fa5fb60`; no warm pass (M10.1); the opening message again carried message 1's zip (M10.2); the scratchpad persisted, with 83 more unmatched files, all accounted for (M10.3)
- Gate K (Plan rev 29): tracking consistent (M10.4); V on S9 passed from disk (M10.5); path forward unchanged under G18(a) (M10.6). Gate R: minor items decided (M10.7)
- COR v4.1 Phase 0: compile clean; all 33 cited references VER Verified, li2002local uncited (R1.6); S1 to S9 complete; G12 confirmed by Mac at 13:00
- Phase 1: Mac accepted the recorded state ("accept \GO", 07:52); public checks agree (M10.8). Phase 2: skipped (`authors_anonymized: false`). Phase 3: README rendered from the YAML
- Phase 4: `hyman2026local_COR_2026-10-10.zip` (10 files) and `hyman2026local_v1_6_1_arXiv.tar.gz` (5 files); each compiles in isolation with 0 errors, 0 undefined, 0 warnings, 0 boxes, 24 pp, the tarball from its shipped `.bbl` without bibtex
- Phase 5: YAML `distribution.arxiv` and `distribution.overleaf`. Phase 6: output
- Rulings: G12 confirmed; G20, G18(a) covers the HIGH both S9 scorers rank first, so the exit criterion's no-HIGH clause is met; MIT license for S11 (M10.11)
- ASM (v1_6_1): mean 23.0, short 8.3%, run 3, commas 5.45, connectives 0.49, nominalizations 2.56; no dashes

### Manuscript edits (v1_6_1)
- L8: Table 3's float moved in the source to just above the paragraph that cites it, no word changed. Table 3 now sits at the foot of page 8 with its citing paragraph under it, and §3.4 starts mid-page 10 (M10.9)
- "Use of AI tools": the AUTHOR note replaced by "The author checked the derivations and computations and takes full responsibility for the content of this paper." (G12(a))
- `\date`: October 10, 2026
- Compile: 0 errors, 0 undefined, 0 warnings, 0/0 boxes, 24 pp, 33/35/33, 0 bibtex warnings, 3 passes; `.bbl` byte-identical to v1_6_0's; SHA-256 `d9f193cb…`

### Reproducibility / assets
- `hyman2026local_reproduce.py` names v1_6_1; its log is byte-identical and Figures 1 and 2 regenerate byte for byte; the registry's six references carry `f6709d5f…`; integrity 38/38
- Table 5 and Table A1 rows unchanged, at .tex lines 364 and 460

### Files added / changed / removed
- Added: `hyman2026local_v1_6_1.tex/.pdf/.bbl`, `archive/v1_6_0/` (11 files), `hyman2026local_COR_2026-10-10.zip`, `hyman2026local_v1_6_1_arXiv.tar.gz`, `hyman2026local_v1_6_1_arXiv_metadata.txt`, `recovered_scratchpad_branch8/` (4 files, M10.3), `hyman2026local_Session10_Report.md`
- Changed: `hyman2026local_reproduce.py` (version label), Master Plan (rev 28 to 30), YAML, README (re-rendered), SHA256SUMS, this file
- Removed: none

### Next
- S11: CGR v4.1.1, the GitHub repository archive (MIT license; repository `machyman/hyman2026local`, which Mac creates); assemble, CGR-Audit, CGR-FreshExtract, manuscript-github verification; no push

## 2026-10-09: Session 9 (second restructuring for readiness under G17(b); v1_6_0; branch 8)

**Versions:** main v1_5_0 → v1_6_0 (y-bump: new subsections in Sections 3 and 4; text only, no new measurement)
**Score:** GSR v3 STS 79 (scorer A) and 78 (scorer B), two cold agents blind to earlier reviews, on v1_6_0 before the diff-check fixes; mean 78.5; E-points 0 (gate closed; would-be 7 for each); MREP 79 and 78; SISC estimates 76 and about 75. The S9 target (mean of the two at least 90) is not met. S8 scored v1_5_0 at 78 and S7 scored v1_4_1 at 80.
**Status:** not_yet_submitted (no change)

### Protocols run
- Branch 8 startup STEPs 0 to 6: STEP 4 clean (585/585; F-1 pass at 47,812 bytes, `a3d71e5f…`; handoff `41dbb255…` equals its stanza; recovery byte-diff empty over 581 files; three PNGs pixel-identical, caBX only); recovery archive run2 observed `ba6923ddec46eb1d0cf8913a5d9c3c7b922eb80616997a69bd25eae833212873`; no warm pass in the manifest checks (M9.1); the opening message again carried message 1's zip (M9.2)
- Gate K (Plan rev 25): tracking consistent; V on S8 passed from disk (M9.5). The registry integrity check matched 37 of 38: the fig2 PNG was registered by its generator hash; set to the on-disk hash (M9.4; a warm pass at branch 7's Phase 6 check 3, file class (d))
- Gate R: no major decision, since G17(b) is ruled (M9.6)
- Independent diff check v1_5_0 → v1_6_0: 1 HIGH (the Conclusions paraphrased the geometry clause), 2 MEDIUM (the x_C row; the geometric-counts condition), 9 LOW; fixed. Follow-up round: every HIGH and MEDIUM resolved; 2 new LOW (L10 fixed, L11 logged); L8 (layout of 3.4 and Table 3) deferred to final layout (`hyman2026local_DiffCheck_S9_2026-10-09.md`)
- Two cold GSR v3 scorers (`hyman2026local_GSR_S9A_2026-10-09.md`, `hyman2026local_GSR_S9B_2026-10-09.md`): both rank as HIGH that the AMReX test does not exercise the decision; both propose compressing Section 5 around one overhead measure, moving the one-run test into Section 2 and gathering the limitations after Section 5; both project 86 to 89 if that is done
- ASM (v1_6_0): mean 23.0, short 8.3%, run 3, commas 5.46, connectives 0.49, nominalizations 2.55; no dashes; research-article bands met, with the mean and the short run at their edges

### Manuscript edits (v1_6_0)
- §3.2 split at its seams: §3.2 "Growth law" (Lemma 1), §3.3 "Budgets for feature-following hierarchies" (Proposition 2, the corollary, the base-grid remark, Tables 2 and 3, Figures 1 and 2) and §3.4 "Agreement with earlier estimates"; "Explicit counts" is now §3.5; only the joins reworded
- The old §3.3, "Published overheads against the budgets", moved verbatim to open §4, now "Published overheads and what the work model leaves out", under a two-sentence lead-in; the omissions are §4.2. References to the tagging rule, the growth factor and padding now point to §3.2
- §5.1: an unnumbered table naming $x_C$, $(O_L-O_G)/K_G$ and $y$, what each counts and where each is used; two sentences shortened to feed it. The $y$ row states $H+\beta O_G$, which follows from $T_G=K_G+O_G$ (L11)
- Conclusions' first paragraph: twelve sentences to three; restatements of the body cut, the qualifiers of every kept claim kept (diff check H1, M2)
- Glosses: AMReX at first use, "a framework for block-structured adaptive mesh refinement (AMR)" citing zhang2019amrex, so "(AMR)" is defined there and shortened later; one sentence on the box-counting law. unsrtnat renumbers the references (L5)
- Abstract unchanged: 1,642 source characters, 1,670 with `\Sid` expanded, 273 words
- Compile: 0 errors, 0 undefined, 0 warnings, 0/0 boxes, 24 pp, bibliography 33/35/33, 0 bibtex warnings, 3 passes; SHA-256 `a0f7da60…`

### Reproducibility / assets
- No generator, input or figure changed. The Table 5 and Table A1 rows still equal their rows files (now at .tex lines 364 and 460)
- Registry: fig2 PNG hash set to the on-disk file (M9.4); integrity 38/38 after the close writes

### Files added / changed / removed
- Added: `hyman2026local_v1_6_0.tex/.pdf/.bbl`, `archive/v1_5_0/` (11 files), `hyman2026local_GSR_S9A_2026-10-09.md`, `hyman2026local_GSR_S9B_2026-10-09.md`, `hyman2026local_DiffCheck_S9_2026-10-09.md`, `hyman2026local_Session9_Report.md`
- Changed: Master Plan (rev 24 to 26), YAML, README (re-rendered), SHA256SUMS, this file
- Removed: none

### Branch (\BRANCH v1_18_0)
- B fired after S9 (about 60% used; COR and the branch protocol would pass 85%)
- Branch gate: V on S9 passed from disk (M9.13); R raised G18 (readiness after S9); G12 open
- Phase 0: key `hyman2026local` by the substrate stem. Phase 1: 603 files, 48,181,343 bytes; highest version v1_6_0, also the newest by mtime; the arXiv tarballs' order is restore order, not a signal (M9.14)
- Phase 2: clean build after the last .tex write: 0 errors, 0 undefined, 0 warnings, 0/0 boxes, 24 pp, 33/35/33, 0 bibtex warnings, 0 em dashes, 3 passes; `.bbl` and PDF text identical to outputs
- Phase 3: `BRANCH_Snapshot_hyman2026local_2026-10-09_run3.zip`, 599 files, count diff empty, `e6ea88ef…`
- Phase 4: `CLEANUP_PROPOSAL_hyman2026local_2026-10-09_run3.md`, 3 files, 16,403,100 bytes; found `readme_extra_files` naming the two run4 archives deleted in branch 6 (M9.14)
- Rulings (20:09): cleanup run 3 approved by name; `\GO`: G18(a), COR v4.1 next as S10 with the S9 scorers' architecture recorded as E-S9 (M9.15); G12 not given
- Phase 5a: removed `BRANCH_Recovery_hyman2026local_2026-10-09.zip`, `BRANCH_Snapshot_hyman2026local_2026-10-09.zip`, `hyman2026local_v1_5_0.pdf` (M9.16)
- Phase 5b: `hyman2026local_reproduce.py` relabelled for v1_6_0, log byte-identical, registry rehashed (M9.17); YAML repairs (M9.18); `HANDOFF_hyman2026local_Session9.md`, this entry, Session 9 report, Plan rev 28, YAML, README, SHA256SUMS. Phase 5c: `BRANCH_Recovery_hyman2026local_2026-10-09_run3.zip`
- Phase 6: 11/11. Manifest 604/604 both ways; self-inclusion 5/5; hashes and F-1 (54,051 bytes before the stanza); `/home/claude` 0 work files; prompt paths 27, one adjudicated (`hyman2026local_v1_5_0.pdf` is named in the prompt's prose as deleted, with its copy in `archive/v1_5_0/`; P6); numbers 9/9/9/9/9; archives 599 and 600 files, key files byte-equal; cross-file agreement; currency; first task; phase walk
- Phase 8 pass 1 (cold): 0 discrepancies; byte-diff empty over 600 extracted files; no file newer than the archive; README render matches; registry 38/38 and every `readme_extra_files` path on disk (the M9.4 and M9.14 lessons, now part of the cold pass). Recovery build before the final one: `083cfc3e…` (first seal). Closing record written and re-sealed, then Phase 8 pass 2

### Next
- Branch 9 opens at message 2 with S10 kickoff (gate K): COR v4.1 under G18(a); its Phase 0 needs the G12 attestation, and its Phase 1 stops for changeable state (M3.3)

## 2026-10-09: Session 8 (restructuring for readiness under G15(a′); v1_5_0; branch 7)

**Versions:** main v1_4_1 → v1_5_0 (y-bump: new Appendix A and Table A1, sections moved; no new measurement)
**Score:** GSR v3 STS 78 (cold agent on v1_5_0 before the diff-check fixes; components archetype 75, introduction 80, narrative 87, dependency 80, redundancy 70, placement 75, referee readiness 80); E-points 0 (gate closed); MREP 78. S7 scored v1_4_1 at 80 with another agent. The S8 target of 90 is not met; the projected 86 to 88 did not appear.
**Status:** not_yet_submitted (no change)

### Protocols run
- Branch 7 startup STEPs 0 to 6: STEP 4 clean (563/563; F-1 pass at 40,531 bytes, `0be5816e…`; handoff `f4560001…` equals its stanza; recovery byte-diff empty over 559 files; three PNGs pixel-identical, caBX only); recovery archive observed `bf202f3d1268b6a317bf6fce0108672525b2f4fc890a23e5ea4bc0330b3fe714`; no warm pass (M8.1); the opening message again carried message 1's zip (M8.2)
- Gate K (Plan rev 21): tracking consistent; V on S7 passed from disk (M8.4); R re-presented G15 with option (a′)
- Ruling gate (`\GO`, 10:49): G15(a′) and G16(a) accepted; G12 not given. Plan rev 22: restructuring inserted as S8, COR S9, CGR S10 (M8.7, M8.8)
- dataviz validator on Figure 1's palette (unchanged): PASS (CVD ΔE 24.7, normal-vision ΔE 33.6)
- Cold GSR v3 rescore (independent agent, blind to earlier reviews): STS 78; every table and figure regenerated byte-identical; no numerical error; 1 HIGH (the AUTHOR placeholder, G12), 2 MEDIUM, 7 LOW (`hyman2026local_GSR_S8_2026-10-09.md`)
- Independent diff check v1_4_1 → v1_5_0: 5 HIGH, 7 MEDIUM, 14 LOW, all claim-strength or accuracy defects introduced by the restructuring; fixed. Follow-up round: all resolved, 2 new MEDIUM (figures floated after the References; the coverage sentence) and 4 LOW, fixed (`hyman2026local_DiffCheck_S8_2026-10-09.md`)
- ASM (v1_5_0): mean 23.0, short 7.7%, run 2, commas 5.48, connectives 0.51, nominalizations 2.52; no dashes; research-article bands met

### Manuscript edits (v1_5_0)
- Abstract: novelty first; published overheads scoped to the DG and octree codes they come from; own overhead result and the fitted-model clause kept (diff check H1, M1); 1,642 source characters, 1,670 with `\Sid` expanded; 273 words, above the 200-word target (M8.11)
- §1: numbered contributions; gloss of PeleLMeX's closed-chamber algorithm (checked against the JOSS paper); boxed decision rule and budget ladder with the conditions Propositions 1 and 2 need
- §3.3 (new): "Published overheads against the budgets", moved from §4 beside Figure 1; §3.2's novelty sentence adds curved surfaces
- §4 keeps the overhead parts, time on parallel machines and accuracy
- §5: "Testing the model" folded into §5.1; held-out coverage stated with both facts (M8.13); protocol detail to Appendix A; §5.3 gains the counterfactual sentence (post hoc, Table A1); §5.6 states the scope, break-even and test caveats once; §5 body 2,745 → 2,292 words, about 17 percent shorter, not the third the row named
- Conclusions: one open-question sentence on a near-break-even test (M8.14); final paragraph on what a developer gains, ending on the dimension message, with the one-run test as a qualified aid (G4(a) wording kept)
- Appendix A (new): plan and amendment hashes, data checks and reruns, fit details, bootstrap, exploratory set, AMReX level counts, Table A1
- Figure 1 redrawn from existing data: legend and AMReX ranges below the panels, larger markers, feature names on tick labels, band annotated; caption notes the 2D disk at δ=2
- Preamble: PDF title and author; `\theHtable` for the appendix table; figures placed `[tbp]`; `\clearpage` before the References
- Compile: 0 errors, 0 undefined, 0 warnings, 0/0 boxes, 24 pp, bibliography 33/35/33, 0 bibtex warnings, 3 passes; SHA-256 `e594d1b1…`

### Reproducibility / assets
- New: `validation/s8_appendix_table.py` → `validation/tableA1_rows.tex`, `validation/s8_appendix_table_output.txt` (registered as tabA1); reproduces "6 of 17" and "3 of 17"; smallest margins 0.087 and 0.156
- Changed: `hyman2026local_reproduce.py` (Figure 1 section; docstring version), `hyman2026local_reproduce_output.txt` (fig2 PNG hash line), `hyman2026local_fig2_dimension.pdf/.png`; Figure 2 and its files unchanged
- Integrity check: 9/9 deposited assets, 38/38 hashes PASS
- Side effect: importing `s6_tables.py` wrote `validation/__pycache__/s6_tables.cpython-313.pyc` (not deleted; for the next cleanup proposal, M8.9)

### Files added / changed / removed
- Added: `hyman2026local_v1_5_0.tex/.pdf/.bbl`, `archive/v1_4_1/` (11 files), `validation/s8_appendix_table.py`, `validation/tableA1_rows.tex`, `validation/s8_appendix_table_output.txt`, `validation/__pycache__/s6_tables.cpython-313.pyc`, `hyman2026local_GSR_S8_2026-10-09.md`, `hyman2026local_DiffCheck_S8_2026-10-09.md`, `hyman2026local_Session8_Report.md`
- Changed: Master Plan (rev 21 to 23), YAML, README (re-rendered), SHA256SUMS, this file, `hyman2026local_reproduce.py`, its output, the Figure 1 files
- Removed: none

### Branch (\BRANCH v1_18_0)
- B fired after S8 (about 76% used; a further text session and the branch protocol would pass 85%)
- Branch gate: V on S8 passed from disk (M8.15); R raised G17 (readiness after S8); G12 open
- Phase 0: key `hyman2026local` by the substrate stem. Phase 1: 584 files, 41,043,685 bytes; highest version v1_5_0, also the newest by mtime
- Phase 2: clean build after the last .tex write: 0 errors, 0 undefined, 0 warnings, 0/0 boxes, 24 pp, 33/35/33, 0 bibtex warnings, 0 em dashes, 3 passes; the PDF in outputs is that build
- Phase 3: `BRANCH_Snapshot_hyman2026local_2026-10-09_run2.zip`, 580 files, count diff empty, `7a135b8e…`
- Phase 4: `CLEANUP_PROPOSAL_hyman2026local_2026-10-09_run2.md`, 5 files, 13,750,140 bytes; approved by name (13:51) with `\GO` (G17(b)); Phase 5a removed 3 files; the two `.pyc` caches are under the protected `validation/` and stay (proposal erratum, M8.17)
- Phase 5b: `HANDOFF_hyman2026local_Session8.md`, this entry, Session 8 report, Plan rev 24, YAML, README, SHA256SUMS. Phase 5c: `BRANCH_Recovery_hyman2026local_2026-10-09_run2.zip`
- Phase 6: 11/11 after one repair of a check, not of the folder (check 5's path pattern stopped at hyphens; the deleted `hyman2026local_v1_4_1.pdf`, named in the prompt's prose, adjudicated, P6). Manifest 585/585; self-inclusion 5/5; hashes and F-1 (47,112 bytes); `/home/claude` 0 work files; prompt paths 25/25; numbers 8/8/8/8/8; archives 580 and 581 files, key files byte-equal; cross-file agreement; currency; first task; phase walk
- Phase 8 pass 1 (cold): 0 discrepancies; byte-diff empty over 581 extracted files; no file newer than the archive; README render matches. Recovery build before the final one: `0679a326…` (first seal). Closing record written and re-sealed, then Phase 8 pass 2

### Next
- Branch 8 opens at message 2 with S9 kickoff (gate K): the second restructuring under G17(b) (v1_6_0, two cold scorers); the G12 attestation is still Mac's

## 2026-10-09: Session 7 (author items, referee 3's LOW items, readiness score; v1_4_1; branch 6)

**Versions:** main v1_4_0 → v1_4_1 (z-bump: wording, disclosures, AI-use addition, repository URL; no new result)
**Score:** GSR v3 STS 80 (Good; cold agent on v1_4_1), below the 85 gate, so E-points 0 and MREP 80 (was 77 at the S2 freeze). The S7 target of 90 is not met.
**Status:** not_yet_submitted (no change)

### Protocols run
- Branch 6 startup STEPs 0 to 6: STEP 4 clean (545/545; F-1 pass at 33,923 bytes; recovery byte-diff empty over 541 files; three PNGs pixel-identical, caBX only); recovery archive run5 observed `10bb03ea…`; no warm pass (M7.1); the opening message again carried message 1's zip (M7.2)
- Gate K (Plan rev 16): tracking consistent; five stale YAML values logged (M7.4); V on S6 passed from disk
- Ruling gate G9 to G14 (`\GO`, 2026-10-09 07:21): G10, G11, G13, G14 (a); G12 accepted as wording only. G9(a), an injected-cost sweep near break-even, was reopened before any work: every quantity it would measure follows from the existing timers. G9′(a) ruled by `\GO` at 07:29: E-S6 kept for a journal version, one explanation added to §5.3
- Diff check of v1_4_0 → v1_4_1 (independent agent): 1 HIGH, 2 MEDIUM, 6 LOW; all fixed; follow-up check: no HIGH or MEDIUM remain, three LOW notes, two applied (`hyman2026local_DiffCheck_S7_2026-10-09.md`)
- Citation role check of §5's one key, `zhang2019amrex`, against the JOSS record (DOI 10.21105/joss.01370; 17 authors, vol. 4, no. 37, art. 1370, 2019): SUPPORTS, cited as the AMReX framework; its metadata was verified at S2
- GSR v3 readiness score (cold agent, blind to earlier reviews): STS 80; components archetype 78, introduction 84, narrative 83, dependency 85, redundancy 72, placement 76, referee readiness 80; SISC estimate about 77 (`hyman2026local_GSR_S7_2026-10-09.md`)
- ASM (v1_4_1): mean 22.6, short 8.2%, run 2, commas 5.47, connectives 0.51, nominalizations 2.49; no dashes; research-article bands met

### Manuscript edits (v1_4_1)
- AI-use statement: the approved G10 sentence on Section 5's provenance added; the responsibility marker left for Mac (G12)
- Reproducibility: the repository URL marker replaced by `https://github.com/machyman/hyman2026local` (G11); the repository does not exist yet
- §5.3: two sentences on why no configuration came near break-even and what cost could bring it there (G9′(a), wording corrected after the diff check)
- Referee 3's LOW items (G14): amendment v2's calibration and smoke runs disclosed (§5.1); the comparison $x_C<\beta$ called an identity with $S>1$ (§5.1); the bootstrap interval's skew stated (§5.2); "therefore" sentence replaced (§5.2); Figure 1 caption says the crosses are finite-depth budgets on the $\beta_\infty$ axis; abstract and conclusions restate Corollary 1(i) at the same depth; abstract adds the equal-cost condition for $S_{\mathrm{ideal}}$. Items 1 and 2 were already met in v1_4_0; item 5 is G11 and G12
- From the cold score: saving error 22 percent for the model (0.219) in the abstract and "21 and 22 percent" in §5.2; abstract trimmed to 1,850 source characters, 1,892 with the macro expanded (arXiv limit 1,920); AMR defined at its first use in the body; date October 9, 2026
- Compile: 0 errors, 0 undefined, 0 warnings, 0/0 boxes, 22 pp, bibliography 33/35/33, 0 bibtex warnings, 4 passes; SHA-256 `1d376b31…`

### Reproducibility / assets
- No figure, table or generator changed; `.bbl` identical to v1_4_0's
- Integrity check: 8/8 deposited assets, 30/30 hashes PASS
- YAML repairs logged at K (M7.4): fig2 provenance note, README extra-files entry, abstract length, required documents (fig3 added), protected list

### Files added / changed / removed
- Added: `hyman2026local_v1_4_1.tex/.pdf/.bbl`, `archive/v1_4_0/` (11 files), `hyman2026local_GSR_S7_2026-10-09.md`, `hyman2026local_DiffCheck_S7_2026-10-09.md`, `hyman2026local_Session7_Report.md`
- Changed: Master Plan (rev 16 to 20), YAML, README (re-rendered), SHA256SUMS, this file
- Removed (cleanup run 6, approved by name): `BRANCH_Recovery_hyman2026local_2026-10-08_run4.zip`, `BRANCH_Snapshot_hyman2026local_2026-10-08_run4.zip`, `hyman2026local_v1_4_0.pdf` (copy in `archive/v1_4_0/`)

### Branch (\BRANCH v1_18_0)
- B fired after S7 (about 69% used; the proposed S8 and the branch protocol would pass 85%)
- Branch gate: V on S7 passed from disk (M7.11); R raised G15 (restructuring for readiness) and G16 (the scorer's natural near-break-even design); G12 open
- Phase 0: key `hyman2026local` by the substrate stem; the YAML has no `citation_key` field (M7.12). Phase 1: 562 files, 34,099,989 bytes; highest versions v1_4_1; arXiv-tarball mtimes reflect restore order, not a P2 halt (M7.12)
- Phase 2: clean room, 0 errors, 0 undefined, 0 warnings, 0/0 boxes, 22 pp, 33/35/33, 0 bibtex warnings, 0 em dashes, 4 passes; PDF text and `.bbl` identical to outputs
- Phase 3: `BRANCH_Snapshot_hyman2026local_2026-10-09.zip`, 558 files, count diff empty, `9fefb5d2…`
- Phase 4: `CLEANUP_PROPOSAL_hyman2026local_2026-10-09.md`, 3 files, 11,183,632 bytes; approved by name (08:08); Phase 5a removed the 3 files (564 to 561); erratum appended (M7.13)
- Phase 5b: `HANDOFF_hyman2026local_Session7.md`, this entry, Session 7 report, Plan rev 20, YAML, README, SHA256SUMS. Phase 5c: `BRANCH_Recovery_hyman2026local_2026-10-09.zip`
- Phase 6: 11/11 after one repair (M7.14: the Plan header and the goal's deliverable line still named v1_4_0; re-sealed; prior recovery build `abbcb07e…`). Manifest 563/563; self-inclusion 5/5; hashes and F-1 (39,624 bytes); `/home/claude` 0 work files; prompt paths 24/24 (two strings adjudicated, P6); numbers 7/7/7/7/7; archives 558 and 559 files, recovery byte-diff empty; cross-file agreement; currency; first task; phase walk
- Phase 8 pass 1 (cold): 0 discrepancies; byte-diff empty over 559 extracted files; no file newer than the archive; README render matches. Recovery builds before the final one: `abbcb07e…` (first seal), `d8c7b44c…` (after the M7.14 repair), `132245b3…` and `2db1e067…` (two closing-record re-seals; the first ran after an edit failed its anchor check and wrote nothing, so a timestamp fix needed a second). Closing record written and re-sealed, then Phase 8 pass 2

### Next
- Branch 7 opens at message 2 with S8 kickoff (gate K); first items: Mac's rulings on G15 and G16 and the G12 attestation

## 2026-10-08: Session 6 (validation section, v1_4_0; branch 5)

**Versions:** main v1_3_2 → v1_4_0 (y-bump: new Section 5, Table 5, Figure 3 in the manuscript)
**Score:** MREP 77 (not re-scored; readiness scoring is S7)
**Status:** not_yet_submitted (no change)

### Protocols run
- Branch 5 startup STEPs 0 to 6: STEP 4 clean (523/523, F-1 pass, recovery byte-diff empty over 519 files, three PNGs pixel-identical); recovery archive run4 observed `4e365e61…`; no warm pass (M2.10 datum); the opening message carried message 1's zip and a pasted Session 4 listing (M6.1)
- Gates K, V, R: tracking consistent; V on S5 passed from disk; ruling gate G4 to G6, all (a) (`\GO`, 20:30)
- Dataviz validator on Figure 3's palette: all checks pass (2 slots, adjacent and all pairs)
- VER role pass on the 16 S2 entries (independent agent): 0 HIGH, 3 MEDIUM and 6 LOW, fixes applied (M6.6)
- Cold referee 1: 4 HIGH → ruling gate G7, G8, both (a) (`\GO`, 21:29); referee 2: 2 HIGH, fixed in the text (M6.9); referee 3: no HIGH, MEDIUM fixes applied (M6.10)
- ASM before (v1_3_2) and after (v1_4_0): mean 22.7 → 22.6, short 6.4% → 7.9%, run 2 → 2, commas 5.50 → 5.43, connectives 0.55 → 0.51; no dashes; all research-article bands met

### Manuscript edits (v1_4_0)
- New §5 "A paired test in AMReX": design, prediction (pre-specified verdict PASS, median 0.071), post hoc counts-alone baseline (0.073) and component errors, overhead ($x_C$ −0.42 to −0.003; $y$ −0.11 to 0.19), one-run test, level counts, exploratory runs and scope
- Table 5 (17 configurations) and Figure 3 enter the manuscript; Figure 1 gains the AMReX finite-depth budgets and a label with both overhead measures
- Abstract, introduction roadmap, §4 (one-run test's equal-cost condition, published-overhead link), conclusions revised under G3(a), G4(a), G7(a), G8(a); Lemma 1 wording (nesting, Δx₀); Corollary 1 band note; carried findings W3-6, W4-3, W5-11, W5-16(c)
- Compile: 0 errors, 0 undefined, 0 warnings, 0/0 boxes, 21 pp, bibliography 33/35/33, 4 passes

### Reproducibility / assets
- New asset tab5: `validation/s6_tables.py` → `validation/table5_rows.tex`, `validation/s6_tables_output.txt`
- fig2 (printed Figure 1) regenerated; `hyman2026local_reproduce.py` gains the AMReX points and range checks; the Breuer–Heinecke pair labels corrected; Figure 2 (budget chart) unchanged byte for byte
- fig3 registry PNG hash set to the on-disk file (caBX), generator hash kept in the note (M6.3)
- Integrity check: 8/8 deposited assets, 30/30 hashes PASS

### Files added / changed / removed
- Added: `hyman2026local_v1_4_0.tex/.pdf/.bbl`, `archive/v1_3_2/` (10 files), `hyman2026local_VER_RolePass_S6_2026-10-08.md`, `hyman2026local_Referee_S6_2026-10-08.md`, `hyman2026local_Referee2_S6_2026-10-08.md`, `hyman2026local_Referee3_S6_2026-10-08.md`, `validation/s6_tables.py`, `validation/s6_tables_output.txt`, `validation/table5_rows.tex`, `hyman2026local_Session6_Report.md`
- Changed: `hyman2026local_reproduce.py` and its output log, `hyman2026local_fig2_dimension.pdf/.png`, `validation/deviations.md` (D2, D3), Master Plan (rev 13, 14), YAML, README (re-rendered), SHA256SUMS, this file
- Removed: none

### Branch (\BRANCH v1_18_0)
- B gate fired after S6 (ledger about 335,000 tokens against the 300,000-token calibrated window; no turn was cut)
- V on S6 passed from disk; R on S7 raised E-S6 (major; not ruled in Mac's Phase 4 reply; carried to S7 kickoff)
- Phase 2 equals the S6 record (21 pp, 0 errors, 0 warnings, bibliography 33/35/33, 4 passes); snapshot `BRANCH_Snapshot_hyman2026local_2026-10-08_run5.zip` (540 files, SHA-256 `8dae645e…`, empty count diff; a first count check misread the `outputs` symlink, M6.12)
- Cleanup run 5 approved by name; 3 files, 10,488,816 bytes removed (two run3 archives, top-level v1_3_2 PDF); outputs 543 files
- Handoff `HANDOFF_hyman2026local_Session6.md`; recovery archive `BRANCH_Recovery_hyman2026local_2026-10-08_run5.zip`
- Next: branch 6 opens at message 2 with S7 kickoff (gate K); first item, Mac's ruling on E-S6

### Closing record (\BRANCH Phases 6 to 8)
- Phase 6: 11/11. Manifest 545/545; self-inclusion 5/5; hashes and F-1 (33,165 bytes); `/home/claude` 0 work files; prompt paths 17/17; numbers 6/6/6/6/6; archives 541 and 540, recovery byte-diff empty; cross-file agreement; currency; first task; phase walk
- Phase 8 pass 1 (cold): 0 discrepancies; no file newer than the archive; README render matches
- Re-seal after this record: recovery archive rebuilt; prior build `740c5bcb41149b5f3664a694db3ad80599b18833b4539aa43d5542444d3b3fda`; pass 2 re-checks and writes nothing
- Branch-5 working scripts (seal, checks, YAML and text editors, the referee and VER agent reports' originals) stay in the session scratchpad only; every output they produced is in outputs

### Items deferred / flagged for next session
- S7: Mac's two `\authornote` markers and the AI-use statement, which does not yet mention the AMReX work (M6.11); title and key (R1.5); readiness ≥ 90; referee 3's LOW items
- Deferred enhancement E-S6 (one configuration near break-even) awaits Mac's ruling
- The arXiv tarball was not rebuilt for v1_4_0 (S8, COR)

---

## 2026-10-08: Session 5 (fit, freeze, evaluation, Figure 3, exploratory set; branch 4)

**Versions:** main v1_3_2 (unchanged)
**Score:** MREP 77 (no change; target: readiness ≥ 90, Plan S7)
**Status:** not_yet_submitted (no change)

### Protocols run
- Branch 4 startup STEPs 0 to 6: STEP 4 clean (408/408, F-1 pass, recovery byte-diff empty, PNG pixels identical); recovery archive run3 observed `659860a0…`; no warm pass (M2.10 datum)
- Gates K, V, R: tracking consistent; S4 verified from disk; minor rulings M5.1 to M5.5; no major ruling
- Freeze: K1+O3 selected by training leave-one-out (median 0.124); hash `11d2e030…` recorded in the entry below before evaluation
- **R1.2 verdict PASS:** median held-out error 0.071 (95% bootstrap CI 0.021 to 0.082); largest 0.080 (`d3_sphere_L2`); no miss above 20%, so nothing to explain
- Transparency (after the verdict): all twelve pre-registered pairs pass too (held-out medians 0.032 to 0.071, largest single error 0.144)
- Independent recomputation by a separate agent from the raw data: freeze hash, errors, coefficients, held-out predictions and LOO medians all agree (largest relative difference 2.2e-14)
- Secondary: $H<0$ in all 17 configurations ($x$ −0.45 to −0.06); subcycling wins in all 17; one-run test holds in 6 of 17 with no false positive
- Exploratory set after the freeze (deviation D1; 6 calibration plus 60 paired runs, 0 failures): frozen-pair errors 0.001 to 0.136, including $r=4$ and $L=6$

### Reproducibility / assets
- Registered fig3 (`validation/fig3_validation.py` → `hyman2026local_fig3_validation.pdf/.png`; inputs hashed); regenerated byte-identically twice
- Integrity check: 7/7 deposited assets PASS (22 hashes)

### Files added / removed
- Added: `validation/predictions_frozen.csv`, `predictions_frozen_selection.json`, `evaluation_s5.json/.md`
- Added: `validation/fig3_validation.py` and its output log, `hyman2026local_fig3_validation.pdf/.png`
- Added: `validation/s5_independent_check.py` and its output, `validation/deviations.md` (D1)
- Added: `validation/exploratory/` (calibration, data, window map, console log, summary), `validation/exploratory_s5.py`
- Added: `recovered_scratchpad_branch3/` (18 branch-3 scratchpad files, unclassified, M5.5); `hyman2026local_Session5_Report.md`
- Changed: Master Plan (rev 10, 11, then 12), YAML, README (re-rendered), this file
- Removed (cleanup run 4, approved by name): `BRANCH_Snapshot_..._run2.zip`, `BRANCH_Recovery_..._run2.zip`, and 12 files in `recovered_scratchpad_branch3/` (copies in the run4 snapshot)

### Branch (\BRANCH v1_18_0)
- B gate fired after S5: used about 67%; S6 (about 45%) plus the branch protocol (about 15%) exceeds 85%
- V on S5 passed from disk; R on S6 raised G1 to G3; Mac accepted all three, option (a) each (`\GO`, 19:47)
- Phase 2 equals the baseline; snapshot `BRANCH_Snapshot_hyman2026local_2026-10-08_run4.zip` (529 files, SHA-256 `93dff605…`, empty count diff)
- Cleanup run 4 approved by name; 14 files, 9,488,226 bytes removed; outputs 521 files. Count erratum: header said 13, table listed 14 (M5.6)
- M3.3 (arXiv and GitHub state) not answered; carried to S8's COR Phase 1
- Handoff `HANDOFF_hyman2026local_Session5.md`; recovery archive `BRANCH_Recovery_hyman2026local_2026-10-08_run4.zip`
- Next: branch 5 opens at message 2 with S6 kickoff (gate K)

### Closing record (\BRANCH Phases 6 to 8)
- Phase 6: 11/11. Manifest 523/523; hashes; F-1; archives 529 and 519; numbers 5/5; currency; first task; SHA256SUMS 516/516
- Re-seals before Phase 6: the Plan state line was written after SHA256SUMS, so the seal order was fixed (SHA256SUMS, handoff, archive); prior recovery builds `2768d30a…`, `7aa83eef…`
- Phase 8 pass 1 (cold): 0 discrepancies; recovery byte-diff empty over 519 files; no file newer than the archive; README render matches
- Re-seal after this record: recovery archive rebuilt; prior build `c7f9a30b358402473396f82cd33b8188b3a91bd990477156878439adc96f3e1e`; pass 2 re-checks and writes nothing
- Branch-4 working tools (seal, verify and handoff writers) stay in the session scratchpad only; they are reconstructible from this record and the branch-3 tools kept in `recovered_scratchpad_branch3/`

### Items deferred / flagged for next session
- S6: validation section, Figure 3 in the manuscript, abstract, §4, Figure 1's band with the AMReX points
- Rulings for the S6 text: G1(a) keep Lemma 1 and report measured growth; G2(a) one-run test stays sufficient, conservatism reported; G3(a) negative $H$ in the validation section and one scoped abstract clause
- Run Figure 3 through the dataviz validator before it enters the manuscript (M5.6)

---

## 2026-10-08: Session 5 in progress, prediction freeze record (branch 4; written before any evaluation)

**Versions:** main v1_3_2 (unchanged)

### Prediction freeze (analysis plan v1 §8, step 1)
- `validation/fit.py validation/data --freeze validation/predictions_frozen.csv` ran at 19:20:45 MDT; training rows and held-out counts only (its assertion passed)
- Selected pair **K1+O3** by training leave-one-configuration-out: median 0.1237, 14 parameters; nearest K2+O3 0.1249 (16), K3+O3 0.1298 (21); the parameter tie rule did not bind
- `validation/predictions_frozen.csv`: 1241 bytes, SHA-256 `11d2e03060d6de2b0d26e76da09690e468fdff53851eda638bf2905fa8cc9721`
- `validation/predictions_frozen_selection.json` (training scores and coefficients): 6813 bytes, SHA-256 `8c2f74277c9e9feb29176e3dc37630b9f1bae24ed36c5c2537763448296ce32d`
- No held-out speedup has been computed or displayed. `validation/evaluate.py` runs only after this entry is saved, with the hash above

---

## 2026-10-08: Session 4 (paired AMReX runs, primary matrix; branch 3)

**Versions:** main v1_3_2 (unchanged)
**Score:** MREP 77 (no change; target: readiness ≥ 90, Plan S7)
**Status:** not_yet_submitted (no change)

### Protocols run
- Primary matrix: 17 configurations × 2 schedules × 5 repetitions, 170 runs, 0 failures
- Plan §10 reruns: 4 cells with CV ≥ 5% rerun once; 1 still flagged (`d2_circle_L3` global, 0.073)
- QC: CV 0.007 to 0.073 (median 0.032); timer sums 95.9 to 99.9% of wall
- QC: level counts identical across schedules and repetitions; drift ≤ 1.3e-13
- Held-out speedups not computed (plan §8); training results in `validation/data/qc_summary.md`
- Training: measured $H<0$ in all 10 (x = −0.06 to −0.44); subcycling wins in all 10
- Training: one-run test holds for the 5 points, fails for the 5 disks and balls (no false positive)
- Level counts: mean growth below $r^\delta$ at these depths (descriptive, for S6)

### Reproducibility / assets
- `validation/data/`: runs.csv, levels.csv, logs, inputs, qc.json, qc_summary.md
- Added `validation/qc_s4.py`; `run_matrix.py` gains a plan §10 rerun mode
- Drafted `validation/fit.py` and `validation/evaluate.py` for S5 (not yet run)
- Integrity check: 6/6 deposited assets PASS (unchanged)

### Files added / removed
- Added: `validation/data/`, `validation/qc_s4.py`, `validation/fit.py`, `validation/evaluate.py`
- Added: `hyman2026local_Session4_Report.md`
- Added: `protocols/COR_v4.1_Protocol.md`, `protocols/CGR_v4.1.1_Protocol_Consolidated.md` (R3.1)
- Added: `archive/branch1_superseded/` (2 early branch-1 files, M4.1); `CLEANUP_PROPOSAL_..._run3.md`
- Changed: `validation/run_matrix.py`, Master Plan (rev 9), YAML, README (re-rendered), this file
- Removed (cleanup run 3, approved by name): `hyman2026local_v1_3_0.tex/.bbl`, `v1_3_1.bbl/.pdf`; copies in `archive/`
- Removed (cleanup run 3): branch-1 `BRANCH_Snapshot_...2026-10-08.zip` and `BRANCH_Recovery_...2026-10-08.zip`

### Branch (\BRANCH v1_18_0)
- B gate fired after S4: used about 61%, projected 89% with S5 and the branch protocol
- Mac's ruling R3.1: COR v4.1 (S8) and CGR v4.1.1 (S9) after document editing is final
- Snapshot `BRANCH_Snapshot_hyman2026local_2026-10-08_run3.zip` (402 files, empty count diff)
- Cleanup run 3 approved by name; A8 files extracted and verified first (M4.1); outputs 406 files
- Handoff `HANDOFF_hyman2026local_Session4.md`; recovery archive `BRANCH_Recovery_hyman2026local_2026-10-08_run3.zip`
- Next: branch 4 opens at message 2 with S5 kickoff (gate K)

### Closing record (\BRANCH Phases 6 to 8)
- Phase 6: 11/11. Manifest 408/408; hashes; F-1; archives 402/404; numbers; currency; first task. Check 5 adjudicated: "its qc.json" names the scratch copy's output, not an outputs path
- Phase 5c naming slip: the recovery archive first took the freed base name; renamed `_run3` before any check
- Phase 8 pass 1: 0 discrepancies; byte-diff empty over 404 files; README render matches; SHA256SUMS 401/401
- Re-seal after this record: recovery archive rebuilt; prior build `21f70ba69c79e7ab…`; pass 2 re-checks, writes nothing
- Partial write while recording: Plan state-line anchor failed after this entry and the report were written; repaired at once

### Items deferred / flagged for next session
- S5: fit, select, freeze predictions (hash before evaluation), evaluate, Figure 3
- Exploratory set after the S5 freeze (M3.10)

---

## 2026-10-08: Session 3 (AMReX validation harness; branch 3, opened at message 2)

**Versions:** main v1_3_2 (unchanged)
**Score:** MREP 77 (no change; target: readiness ≥ 90, Plan S7)
**Status:** not_yet_submitted (no change)

### Protocols run
- Branch 3 startup STEP 0 to 6: STEP 4 clean; no warm pass (M2.10 datum)
- Recovery archive SHA-256 observed: `ba1102dc430cf7e3a52cd091aa3837a9ad2d5e6c8560e33abb4b6faf45e5b5fd`
- Gate K: Plan rev 6; V on S2 passed; minor rulings M3.1 to M3.10
- Mac's `\GO` (18:15 MDT) accepted the K recommendations, M3.7 included
- Analysis plan v1 hashed `e4c615e3…` before any timed run (C1(a), M3.8)
- Amendment v2 hashed `cbc2f22c…` before any S4 timing (M3.9)
- 47 smoke and calibration runs: timer sums 96.0 to 99.9% of wall
- Conservation drift ≤ 3.5e-14 (harness v2); counts identical across schedules

### Reproducibility / assets
- AMReX pinned `6bff8018…`; amrex-tutorials pinned `1a73f32e…`
- Harness v2 patch `68f11783…`; 2D and 3D builds clean, 0 warnings
- Window map `validation/nc_map.json` (`19a4070f…`), from subcycled runs only
- `validation/` and the Session 3 report added to `assets.protected_extra`
- Integrity check: 6/6 deposited assets PASS (unchanged)

### Files added / removed
- Added: `validation/analysis_plan.md`, `analysis_plan_v2.md`, `BUILD.md`, `run_matrix.py`, `nc_map.json`
- Added: `validation/harness/Advection_AmrCore.patch`; `validation/smoke/`, `validation/calibration/` (non-analysis)
- Added: `hyman2026local_Session3_Report.md`
- Changed: Master Plan (rev 7), YAML, README (re-rendered), this file
- Removed: none

### Items deferred / flagged for next session
- S4: primary matrix, 5 repetitions; held-out speedups withheld until the S5 freeze
- Exploratory set after the S5 freeze (M3.10)
- Mac: AUTHOR markers (W5-7); confirm arXiv and GitHub state (M3.3)

---

## 2026-10-08: Session 2 (MREP cycle WU0 to WU8; branch gate; \BRANCH)

**Versions:** main v1_2_1 → v1_3_0 (y, WU8) → v1_3_1 (z, compliance pass) → v1_3_2 (z, AI-use sentence)
**Score:** MREP not run → 77 at freeze, on v1_2_1 (target: readiness ≥ 90, Plan S7)
**Status:** not_yet_submitted (no change)

The three Session 2 entries below are work-unit records, kept unedited as the audit trail: the WU3 to WU6 entry records the freeze hash before the Weak Points list was opened (M2.10).

### Manuscript edits
- v1_3_0: positioned against Kritsuk, Domingues, Seny, Fernando–Sundar, AMReX `Optimal`, SeisSol
- v1_3_0: new Lemma 1, Corollary 1, normalization remark, capped time ratio
- v1_3_0: one-run test, latency both ways, published-overhead bracket 0.001 to 0.046
- v1_3_0: new Figure 1 (dimension chart), Table 3 (codimension); Table 4 tilted circle
- v1_3_0: bibliography 19 → 35 entries; Mac's three passages kept verbatim
- v1_3_1: FLTE ties before 71 citations and references; `microtype` added
- v1_3_1: Figure 2 recolored, slot 4 → slot 7 (W5-16(f), SA-6)
- v1_3_1: rendered word sequence unchanged apart from line breaks; labels unchanged
- v1_3_2: approved AI-use sentence added (W0-6); no other change

### Protocols run
- MREP WU0 to WU8, kit v6.31-preview; GATEs A, B, C ruled by Mac
- Report frozen at WU6: 1 CRITICAL, 8 HIGH, 12 MEDIUM, 22 LOW, 3 INFO
- WU7 RTP measures: 10 structural findings; 8 of 9 weak points confirmed (contaminated)
- ASM on v1_3_0: mean 22.7, short 6.5%, run 2, commas 5.47; v1_3_1 identical
- Branch-gate V: passed; one finding (W5-16(f) unaccounted), repaired in v1_3_1
- FLTE lint: 2 content placeholders (Mac's AUTHOR markers); no other blockers
- Compile v1_3_2: 0 errors, 0 warnings, 0 boxes; 16 pages; bib 32/35/32

### Distribution / submission state changes
- arXiv: package rebuilt as `hyman2026local_v1_3_2_arXiv.tar.gz`; builds cleanly; not posted
- arXiv categories confirmed by Mac: math.NA, cross-list physics.comp-ph

### Reproducibility / assets
- Registered fig2 (dimension chart, printed Figure 1) and tab3 (codimension), hashed
- Generator relabeled by printed numbers; fig1 recolored; numeric log lines unchanged
- Exact check 707 cases PASS; wu8 15 PASS; wu1 53 PASS
- Both PNGs gained platform `caBX` chunks; pixels identical (M2.9)
- Integrity check: 14/14 hashes PASS after the v1_3_1 updates
- Archived v1_2_1, v1_3_0 and v1_3_1 version sets in `archive/`

### Files added / removed
- Added: v1_3_0, v1_3_1, v1_3_2 tex, pdf, bbl, arXiv packages; `archive/v1_2_1/`, `archive/v1_3_0/`, `archive/v1_3_1/`
- Added: dimension chart pdf/png; nine MREP handoffs; seven MREP reports; Session 2 report
- Added: `verification/wu1_*`, `wu5_*`, `wu8_*`; MREP kit copy
- Removed (A8, approved by name): `Session1_Report.md`, `HANDOFF_2.md`; copies in the branch-1 snapshot
- Removed (cleanup run 2, approved by name): `hyman2026local_v1_2_1.tex/.pdf/.bbl`, `hyman2026local_v1_3_0.pdf`; archive copies kept
- Full manifest with hashes: `HANDOFF_hyman2026local_Session2.md`

### Branch (\BRANCH v1_18_0)
- Rulings at the gate: R1.1 confirmed; R1.2 (a); W0-6 applied; categories confirmed
- Snapshot `BRANCH_Snapshot_hyman2026local_2026-10-08_run2.zip` (89 files, empty count diff)
- Phase 5a first skipped (`\GO` named no proposal), then run on Mac's approval by name (M2.14)
- Removed: 4 top-level duplicates, recovered folder, `/home/claude/v_s2/`; outputs 117 → 105
- Recovery archive first build `6a14eda667d92dcd…` superseded by the post-5a re-seal
- Handoff `HANDOFF_hyman2026local_Session2.md`; recovery archive `BRANCH_Recovery_hyman2026local_2026-10-08_run2.zip`
- Next: branch 3 opens at message 2 with S3 kickoff (gate K)

### Closing record (\BRANCH Phases 6 to 8)
- Phase 6: 11/11 checks pass (manifest 105/105, hashes, F-1, archives, numbers, currency, first task)
- Phase 7: startup prompt emitted; a copy is in the handoff
- Phase 8 pass 1: 11/11; archive byte-diff empty over 101 files (positive control live); 0 discrepancies
- Re-seal after this record: recovery archive rebuilt; prior build `f119230c73515f0d…`; pass 2 re-checks, writes nothing

### Items deferred / flagged for next session
- Mac: resolve the two AUTHOR markers (W5-7)
- S3: AMReX validation harness and hashed analysis plan (C1(a)); posting blocked until S5
- S6: VER role pass on the 16 new entries; W3-6, W4-3, W5-11, W5-16(c)

---

## 2026-10-08: Session 2, branch 2 (continued): MREP WU3 to WU6; findings FROZEN; stopped at GATE C

**Substrate:** `hyman2026local_v1_2_1.tex` unchanged (`f3935936fb6b7615…`).

### Rulings
- GATE B, by Mac's `\GO`: B1 to B6 as recommended.
- A8 is still unapproved (P4).
- Minor rulings: M2.1 (NTA confirmation deferred to GATE C); M2.2 (cold independent HR panel).

### WU3 (GSR, NTA, FTQ; blind RTP-draft pass)
- GSR STS 77; E-points gated.
- NTA MINOR: anchors 4/5; the closing sentence counts as a D2 drift.
- FTQ GOOD; recommends a design chart.
- RTP draft (blind): STS 58; R-1 to R-10 (2 HIGH, 5 MEDIUM, 3 LOW), frozen for WU7.

### WU4 (SPRE v4.5 diagnostic)
- Every §12.3 research band met.
- SPRE CV floor conflict reported (W4-1); Phase 1.5 anchors flagged.

### WU5 (HR v2.1.1, cold independent panel)
- Major revision before posting.
- Strongest objection: $H$, the only addition to existing work-count models, is never measured or bounded.
- New: Fernando & Sundar; Faloutsos & Gaede; Nyx production use of AMReX `Optimal`; the limit claimed beyond hypotheses (aligned circle oscillates to $L=11$, executor-verified); the latency argument one-sided.

### WU6 (IMP v1.2)
- Grade: GOOD.
- Weakest element: evidence on $H$ (REVIEWER-BLOCKING if deferred).
- Frozen findings report: 1 CRITICAL, 8 HIGH, 12 MEDIUM, 22 LOW, 3 INFO.
- **Freeze hash:** `hyman2026local_MREP_Report_2026-10-08.md` SHA-256 `831cf444d9ff7ba07541a74939fa85247395c00b20787d87e64590fae44e5d38`.

### Files added / changed / removed
- Added:
  - `hyman2026local_MREP_Report_2026-10-08.md` `831cf444d9ff7ba07541a74939fa85247395c00b20787d87e64590fae44e5d38`
  - `hyman2026local_WU3_Structure_Report_2026-10-08.md` `86a6be82517a7396450e4f9392963b8c5bf1be61cd75e89eba2ed3608190db49`
  - `hyman2026local_WU4_Prose_Report_2026-10-08.md` `e1d6faddab73638112896f39c3e839a58190b88888a1dab1612ce663a79eb404`
  - `hyman2026local_HR_Report_2026-10-08.md` `65accfc47678f335778b79e89513bd73181db12a689734a7829ca81d6587b826`
  - `hyman2026local_PathToExceptional_2026-10-08.md` `cd6bcda761f9e63ee537831436662b459b478e3fbadc9e2b087a3bfb9e473e36`
  - `HANDOFF_hyman2026local_MREP_WU3.md` `d543aa87c388b3bf606fed8d52bbc1d5fc86331891bb51a6cfce4c76502a5093`
  - `HANDOFF_hyman2026local_MREP_WU4.md` `7eea783479581d6c6224c4862e7c4baa10cb6daf3e8591c2728f3b09c5962b04`
  - `HANDOFF_hyman2026local_MREP_WU5.md` `553ab5403eb2f0ddf33d3be97b9ef4d12f6e587283541dd3a3cdb3d6afd0ed99`
  - `HANDOFF_hyman2026local_MREP_WU6.md` `6541b95084bfc895161b8bcb1315d245070f6ed87672012e8f1956fba9366145`
  - `verification/wu5_circle_alignment_check.py` `27ee2706d921656846978579698fcbb394306fd9bbb06be14b1b97289773ac2d`
- Changed: `hyman2026local_MREP_Report_2026-10-08.md` (cumulative, then frozen), `hyman2026local_MasterPlan.md`, `MANUSCRIPT_STATUS.yaml`, `README.md` (re-rendered).
- Removed: none.

### Next
- GATE C rulings C1 to C7 and A8; then WU7 (RTP measures) and WU8+ revisions.

---

## 2026-10-08: Session 2, branch 2 (continued): MREP WU1 and WU2; stopped at GATE B

**Substrate:** `hyman2026local_v1_2_1.tex` unchanged (`f3935936fb6b7615…`).

### Rulings
- GATE A, by Mac's `\GO`: A1 to A7 as recommended (A7: arXiv only for this cycle).
- A8 (cleanup deletion) is still unapproved (P4).

### WU1, verification (VEE, VES, PRP-Lite, Measurement Discipline, RMV, CER)
- No mathematical error.
  - 11 equations and 5 statements verified; 2 proofs checked.
  - 132 of 132 load-bearing numbers re-derived by a fresh script (53 PASS, 0 FAIL).
  - The Table 3 counts reproduced by an independent rebuild.
- CER Tier 1: two clean-venv runs give identical logs; Figure 1 bytes are environment-dependent (W1-9).
- Findings: W1-1, W1-2 (MEDIUM); W1-3 to W1-7, W1-9, W1-10 (LOW).

### WU2, bibliography (VER v3.7, BKS, LRV)
- 19 of 19 entries' metadata confirmed; 0 DOI errors; key-year lint clean.
- 38 role checks: 25 SUPPORTS, 11 PARTIAL, 2 ROLE-UNVERIFIED, 0 DOES-NOT-SUPPORT.
- LA-UR-03-8927 checked directly.
- LRV found three HIGH positioning gaps:
  - Kritsuk et al. (growth law);
  - Domingues et al. and Seny et al. (β);
  - AMReX `Optimal` subcycling search in source commit 6bff801.
- Totals: 3 HIGH, 5 MEDIUM, 17 LOW, 2 INFO.

### Files added / changed / removed
- Added:
  - `HANDOFF_hyman2026local_MREP_WU1.md` `d973bb8fdf980f9908bc95d35216ced3cc3313ed664c2b4678b499dc00764659`
  - `HANDOFF_hyman2026local_MREP_WU2.md` `c10a002f7425706aac8d1e559104f40888d18b8cd03987408e777df55bdfde9a`
  - `hyman2026local_MREP_Report_2026-10-08.md` `8d6995e79e785992d3fa26c55f8e551a8c1d494c0a53f145055146ab919f77af`
  - `hyman2026local_Verification_Register_2026-10-08.md` `918157aec277ab026f82d1beb6c2a6696ad7452053e33c82a9f9ebb8c43b4add`
  - `hyman2026local_VER_Report_2026-10-08.md` `374d0b1e5c80e297848dcedb198a85f20f95a2d5e0976dfe81eb993039214d08`
  - `verification/wu1_independent_checks.py` `051f7319d75dda38f4ec75efdae690513f109dccfa03298d8646924ddd19857a`
  - `verification/wu1_independent_checks_output.txt` `b6154e1d6cf6a1c9caaff44d1faab2c315ee79252d95645aed7e92a2872b5bdf`
- Changed: `hyman2026local_MasterPlan.md` (decision log, S2 row, state line), `MANUSCRIPT_STATUS.yaml` (next_task, handoff_file, readme_extra_files), `README.md` (re-rendered).
- Removed: none.

### Next
- GATE B rulings and A8; then WU3.

---

## 2026-10-08: Session 2, branch 2 (opened at message 2; MREP cycle WU0; stopped at GATE A)

**Substrate:** `hyman2026local_v1_2_1.tex` unchanged (SHA-256 `f3935936fb6b7615…`).

### Branch open (startup STEPs 0 to 6)
- Skills: session-branch v1_18_0, session-autopilot v1_0_1, manuscript-tracking 1.3, manuscript-review 2.3 (all installed). The manuscript-review scripts carry no version string, so no script/skill mismatch can be tested.
- STEP 3: clean-room compile matches the baseline (0 errors, 0 warnings, 0 boxes, 11 pages, bib 19/19/19, 0 em dashes; 3 pdflatex passes). The reproduce log is byte-identical, sha256 lines included.
- STEP 4: 41/41 files match the Session 1 manifest. The CHANGELOG verifies by F-1 (4732 bytes, `e00a5e2a…`), and the handoff hash equals the F-1 stanza. The recovery archive byte-diff is empty. The PNG is pixel-identical to the generator output (caBX only), and `/home/claude` holds no work files. Recovery archive SHA-256 as observed: `88f2e5abad23dd46a01bcd699a989a2c23a8472fb66bcac53e07f1801f5ad87c`. Clean STEP 4: no warm pass (M2.10 datum).
- STEP 6: S2 was not marked done, so the branch proceeded to K.
- Measurement note (P6): a first bibtex warning count of 1 was the `warning$` built-in in the .blg function table. Real bibtex warnings: 0.

### Rulings and plan
- Mac: "Execute the pasted prompt and \GO", with the MREP launch prompt and `hyman2026local_MREP_Kit.zip`.
- Recorded under `\GO`: R1.3, R1.4, R1.5 and R1.6 (Plan decision log). R1.1 and R1.2 are held as GATE A item A7, because the launch prompt says arXiv only and the Plan draft says arXiv then a journal (P2).
- The cleanup proposal stays unapproved: `\GO` does not name it (P4). It is GATE A item A8.
- Plan rev 3: the MREP cycle is S2, and the AMReX sessions are renumbered S3 to S7.

### MREP WU0 (pre-flight)
- Pinned hashes; Weak Points list sealed (hashed from the archive stream only); contamination undetermined for branch 1.
- Maturity: mature for full review. No SI. Code exists, so RMV and CER are on.
- Findings W0-1 to W0-6. The main one: v1_2_1 is Session 1's rewrite, not RTP's draft (GATE A item A1).

### Files added / changed / removed
- Added: `hyman2026local_MREP_Kit.zip` (copy of Mac's upload; protected) and `HANDOFF_hyman2026local_MREP_WU0.md` (SHA-256 `6dd89b2ccc27dedb1176c67be97cdc168bded9a093bbcc17b328e0b7a590dcb1`).
- Changed: `hyman2026local_MasterPlan.md` (rev 3), `MANUSCRIPT_STATUS.yaml` (next_task, handoff_file, protected_extra, metadata), `README.md` (re-rendered).
- Removed: none.

### Next
- Mac's GATE A rulings A1 to A8; then WU1 verification.

---

## 2026-10-08: Session 1, branch 1 (transfer from ChatGPT; standalone rewrite, new analysis, SPRE; sync; \BRANCH)

**Versions:** main `amrstepping_v1_1_0` → `hyman2026local_v1_2_0` (key renamed per §7.6; y-bump) → `v1_2_1` (z-bump, same session)
**Score:** MREP not run
**Status:** not_yet_submitted (no change)

### Manuscript edits
- Rewritten as a standalone arXiv note; claim IDs, GAP boxes and session language removed
- Positioned against Dursi & Zingale (2005); bibliography grown from 4 to 17 verified references
- New: overhead budget β = 1 − 1/S_ideal; box-counting growth law ρ ≈ r^δ
- New: Prop. 2 with coverage fraction a (both counting conventions); Remarks 2 and 3
- New: Table 2 (limits), Table 3 (synthetic counts), Figure 1 (budget against depth)
- Corrected the C-06 codimension scaling; the r = 4 sensitivity table folded into the §2 example
- Pilot section and figure removed (Mac's ruling); files archived with a diagnosis
- v1_2_1: cited Li & Hyman (2002 report; LA-UR-03-8927) on locked vs local time steps (§1, §4.2, §5)
- Sync: five citation keys standardized (build-path only; rendered text identical); v1_2_1 re-hashed `f3935936fb6b7615…`
- Sync: VER annote added to all 19 bib entries (18 Verified, 1 Unable to verify: li2002local)

### Protocols run
- SPRE rewrite (research-article register, §12.3); ASM before and after; all bands met, long words flagged
- VER-lite: 15 scholarly entries verified via Crossref/publisher; 2 docs pages accessed 2026-10-08
- Independent cold referee, two passes: 3 HIGH + 8 MEDIUM, then 2 MEDIUM; all resolved
- Clean-room 4-pass compile: 0 errors, 0 warnings, 11 pp
- MD-1 positive controls certify zero dashes, banned connectives and placeholders
- Tracking: Master Plan draft (rev 1), README renderer, YAML plan pointer and session fields

### Distribution / submission state changes
- arXiv: source package built (`hyman2026local_v1_2_1_arXiv.tar.gz`; v1_2_0 package archived); not posted

### Reproducibility / assets
- Registered fig1, tab1, tab2, tab3 → `hyman2026local_reproduce.py` (hashed)
- Integrity check: 4/4 deposited assets verified; figure regenerates byte-identically; PASS

### Branch (\BRANCH v1_18_0)
- Snapshot `BRANCH_Snapshot_hyman2026local_2026-10-08.zip` (34 files); recovery archive `BRANCH_Recovery_hyman2026local_2026-10-08.zip`
- Phase 5a skipped: no approval naming the cleanup proposal (P4); proposal carried to S2 kickoff
- Registry: Figure 1 PNG re-hashed after a platform-inserted `caBX` chunk (pixels identical; M1.6)
- Next: branch 2 opens at S2 kickoff (gate K): rulings R1.1–R1.6 and cleanup approval

### Closing record (\BRANCH Phases 6 to 8)
- Phase 6: 11/11 checks pass (manifest 41/41, hashes, F-1, archives, session numbers, currency, first task)
- Phase 7: startup prompt emitted; a copy is in the handoff
- Phase 8 pass 1: 41 files; archive byte-diff empty over 39 files (positive control live); 0 newer files; README matches the render; 11/11 pass; 0 file discrepancies
- Phase 8 check defect fixed (P6): `find` on the outputs symlink listed 0 files (P8.1, P8.3); a trailing slash fixed it; no file affected
- Re-seal after this record: recovery archive rebuilt under the same name; prior build SHA-256 `ae91d3878ff7df58a027828cfb98c853bdb87dbe4bd265160408169490fcf923`; Phase 8 pass 2 verifies it
- Phase 8 pass 2: check 3 failed; the handoff writer hashed the CHANGELOG with its F-1 stanza; writer fixed to strip it; re-sealed (pass 2 build `46f7b03ef79ecc7c`); pass 3 verifies

### Files added / removed
- Added: `hyman2026local_MasterPlan.md`, `hyman2026local_render_readme.py`, `hyman2026local_Session1_Report.md`, `HANDOFF_hyman2026local_Session1.md`, `CLEANUP_PROPOSAL_hyman2026local_2026-10-08.md`, `BRANCH_Snapshot_hyman2026local_2026-10-08.zip`, `BRANCH_Recovery_hyman2026local_2026-10-08.zip`, `verification/claude_symcheck.py`, `verification/claude_asm_shortlist.py`, `verification/claude_asm_longlist.py`
- Removed: none (cleanup proposal awaiting approval: `Session1_Report.md`, `HANDOFF_2.md`)

### Items deferred / flagged for next session
- Mac: check derivations; resolve the 2 AUTHOR markers (repo URL, responsibility statement)
- Mac: confirm li2002local details (2002 LANL report not found online); decide on 'locked' terminology
- Mac: decide on the title/key and on AMReX paired-run validation (memo §2)
- Mac: rulings R1.1–R1.6 on the Master Plan draft (goal, exit criterion, validation scope, terminology, title/key, li2002local)

---

F-1: `HANDOFF_hyman2026local_Session1.md` SHA-256 `fae9d69519f9095671d72f4fc91304d87fa93a6a954999fc46c3e305e6d8f956` (its manifest row is self-referential; recorded after the file closed).

F-1: `HANDOFF_hyman2026local_Session2.md` SHA-256 `bf7d3d178a7f26e21d03e66711a1647731d61a1078d4e629ea4aaee522882d3e` (its manifest row is self-referential; recorded after the file closed).

F-1: `HANDOFF_hyman2026local_Session4.md` SHA-256 `1af689a5fc949eb7daa17ff74741aeac49b5745bd634ae55b81235d586009c42` (its manifest row is self-referential; recorded after the file closed).

F-1: `HANDOFF_hyman2026local_Session5.md` SHA-256 `855355edfb177b4452a13c93c4b7e12cb8a221d63ab77076aa523d9063a37d8a` (its manifest row is self-referential; recorded after the file closed).

F-1: `HANDOFF_hyman2026local_Session6.md` SHA-256 `1276e9c2ea64f204f3768247a2e28c3e5346287eb9194e6218ffb3212cf2d1c7` (its manifest row is self-referential; recorded after the file closed).

F-1: `HANDOFF_hyman2026local_Session7.md` SHA-256 `f456000186f6dfaa1e52a3f7ebd7e4c31169d61c8000d8facc65dab27ea5d38a` (its manifest row is self-referential; recorded after the file closed).

F-1: `HANDOFF_hyman2026local_Session8.md` SHA-256 `41dbb2556c75094dde3081ab5b20cf125e2232c35f85c71426f0c8f220fd1efc` (its manifest row is self-referential; recorded after the file closed).

F-1: `HANDOFF_hyman2026local_Session9.md` SHA-256 `40acf9ddd371ede0a50e30ec8935aadcbe27b0f84dbd8219be2e7d466f31d184` (its manifest row is self-referential; recorded after the file closed).

F-1: `HANDOFF_hyman2026local_Session11.md` SHA-256 `15b99f45a438e7b2c99d600632605a31df40cd4df3ea4e6734858a6074fa976a` (its manifest row is self-referential; recorded after the file closed).

F-1: `HANDOFF_hyman2026local_Session12.md` SHA-256 `61cc5ef9bff1c9ed997544c93e9df3bd65199dc51dcb7334f4bd15f6d179b5ea` (its manifest row is self-referential; recorded after the file closed).
