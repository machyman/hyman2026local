# S5 exploratory set (EXPLORATORY: not part of the R1.2 verdict)

Analysis plan v1 §3; Plan M3.10; deviation D1. Predictions use the frozen pair **K1+O3** with its training coefficients unchanged. Failed runs: 0.

| Configuration | CV of $T$ (G / L) | Timers/$T$ | Counts identical | $S$ | $\hat S$ (frozen pair) | $e$ | $S_{\mathrm{id}}$ | $x=H/K_G$ | β | One-run test | Subcycling wins |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---|---|
| `d2_circle_L2_r4` | 0.049 / 0.026 | 0.985 to 0.987 | True | 1.359 | 1.240 | 0.088 | 1.271 | -0.343 | 0.213 | False | True |
| `d2_circle_L3_r2_regrid` | 0.090 / 0.065 | 0.987 to 0.991 | True | 1.601 | 1.572 | 0.018 | 1.631 | -0.520 | 0.387 | False | True |
| `d2_point_L2_r4` | 0.019 / 0.056 | 0.974 to 0.981 | True | 5.279 | 5.998 | 0.136 | 8.875 | -0.280 | 0.887 | True | True |
| `d2_point_L6_r2` | 0.010 / 0.059 | 0.948 to 0.963 | True | 7.415 | 7.426 | 0.001 | 16.401 | -0.644 | 0.939 | True | True |
| `d3_circle_L3_r2_regrid` | 0.021 / 0.026 | 0.997 to 0.998 | True | 1.512 | 1.406 | 0.070 | 1.632 | -0.185 | 0.387 | True | True |
| `d3_point_L4_r2` | 0.035 / 0.029 | 0.991 to 0.992 | True | 3.748 | 3.788 | 0.011 | 4.541 | -0.245 | 0.780 | True | True |

Level counts $M_\ell$ (initial hierarchy):

- `d2_circle_L2_r4`: M = [16384, 38976, 153792], B = [4, 43, 159]
- `d2_circle_L3_r2_regrid`: M = [16384, 19648, 34752, 49216], B = [4, 19, 39, 84]
- `d2_point_L2_r4`: M = [16384, 1024, 768], B = [4, 1, 1]
- `d2_point_L6_r2`: M = [16384, 576, 576, 576, 576, 576, 384], B = [4, 1, 1, 1, 1, 1, 1]
- `d3_circle_L3_r2_regrid`: M = [32768, 119808, 192000, 209408], B = [1, 8, 21, 50]
- `d3_point_L4_r2`: M = [32768, 9216, 9216, 9216, 4096], B = [1, 1, 1, 1, 1]
