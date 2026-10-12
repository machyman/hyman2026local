# When Is Local Time Stepping Worthwhile? A Cost Analysis for Nested Adaptive Mesh Refinement

James M. Hyman, Department of Mathematics, Tulane University.

This repository holds the source of the paper (version v1_7_0), the script that reproduces its analytical tables and Figures 1 and 2, and the AMReX validation behind Section 5, Table 5, Table A1 and Figure 3. arXiv identifier: TBD.

## Reproduce

You need Python 3.13 with the packages in `requirements.txt`, and a TeX distribution with `pdflatex`.

```
mkdir -p out

# The paper. The .bbl is included, so bibtex is optional.
pdflatex hyman2026local_v1_7_0.tex
pdflatex hyman2026local_v1_7_0.tex

# Tables 1 to 4, Figures 1 and 2, and the exact checks (seconds; no random numbers).
python3 hyman2026local_reproduce.py --outdir out > out/reproduce_output.txt

# Table 5, Table A1 and Figure 3, from the recorded AMReX timings.
python3 validation/s6_tables.py validation/data --evaluation validation/evaluation_s5.json --selection validation/predictions_frozen_selection.json --out out/table5_rows.tex
python3 validation/s8_appendix_table.py validation/data --evaluation validation/evaluation_s5.json --out out/tableA1_rows.tex
python3 validation/fig3_validation.py validation/data --frozen validation/predictions_frozen.csv --evaluation validation/evaluation_s5.json --outdir out
```

Each script prints a log. The logs saved beside them are the reference: `hyman2026local_reproduce_output.txt` and the `*_output.txt` files in `validation/`. The rows files should equal `validation/table5_rows.tex` and `validation/tableA1_rows.tex`. With the versions above, the figure PDFs regenerate byte for byte. Compare PNGs by pixels, since some hosts add metadata to PNG files.

Re-running the AMReX timings needs AMReX and amrex-tutorials at the pinned commits, the patch in `validation/harness/`, and `validation/run_matrix.py`. [`validation/BUILD.md`](validation/BUILD.md) gives the steps. Timings depend on the machine, so new runs will not match the recorded ones digit for digit.

## Figure file names

The file names keep the order in which the figures were made.

| File | Printed as |
|---|---|
| `hyman2026local_fig2_dimension.pdf`, `.png` | Figure 1 |
| `hyman2026local_fig1_budget.pdf`, `.png` | Figure 2 |
| `hyman2026local_fig3_validation.pdf`, `.png` | Figure 3 |

## Repository structure

| Path | What it is |
|---|---|
| [`hyman2026local_v1_7_0.tex`](hyman2026local_v1_7_0.tex) | Paper source |
| [`hyman2026local_v1_7_0.bbl`](hyman2026local_v1_7_0.bbl), [`hyman2026local.bib`](hyman2026local.bib) | Bibliography, compiled and source |
| [`hyman2026local_v1_7_0.pdf`](hyman2026local_v1_7_0.pdf) | The paper, 25 pages |
| `hyman2026local_fig*.pdf`, `hyman2026local_fig*.png` | The three figures (see the table above) |
| [`hyman2026local_reproduce.py`](hyman2026local_reproduce.py) | Exact checks, Tables 1 to 4, Figures 1 and 2 |
| [`hyman2026local_reproduce_output.txt`](hyman2026local_reproduce_output.txt) | Its reference log |
| [`validation/`](validation/README.md) | The AMReX validation; its own README lists every file |
| [`requirements.txt`](requirements.txt) | Python package versions used |
| [`LICENSE`](LICENSE) | MIT License, for the code |
| [`LICENSE-CC-BY-4.0.md`](LICENSE-CC-BY-4.0.md) | CC BY 4.0, for the paper, figures, data and documentation |
| [`CITATION.cff`](CITATION.cff) | How to cite |
| [`MANUSCRIPT_STATUS.yaml`](MANUSCRIPT_STATUS.yaml) | Manuscript status and the registry of every figure and table: generator, inputs, outputs and SHA-256 hashes. It describes the author's full working folder, so it names some files that are not in this repository |
| [`CHANGELOG.md`](CHANGELOG.md) | Session-by-session history of the manuscript |

## AMReX

The harness patches the Advection_AmrCore example of amrex-tutorials (commit `1a73f32e10514d917333ea7a3fd54e661e232144`), built against AMReX (commit `6bff801899baed998581e74ab20ee2137d6b2dee`). Neither is redistributed here, and both keep their own licenses. The patch is a diff against amrex-tutorials.

## Development Tools

This research used AI-assisted workflows for analysis, manuscript preparation and review. The section "Use of AI tools" in the paper gives the full disclosure. The author checked the derivations and computations and takes full responsibility for the content of this paper.

## License

The code, meaning every `.py` file, the harness patch and `requirements.txt`, is under the MIT License; see [`LICENSE`](LICENSE). Everything else, including the paper, its source and bibliography, the figures, the data, the logs and the documentation, is under CC BY 4.0; see [`LICENSE-CC-BY-4.0.md`](LICENSE-CC-BY-4.0.md). AMReX and amrex-tutorials keep their own licenses (see above).

## Citation

See [`CITATION.cff`](CITATION.cff). The arXiv identifier will replace TBD once the paper is posted.
