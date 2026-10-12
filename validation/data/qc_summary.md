# S4 QC summary (analysis plan v1 section 10, amendment v2)

Runs: 190 recorded, 0 failed; 170 used. Cells rerun for CV (plan section 10): d2_circle_L2_r2|subcycle, d2_circle_L3_r2|global, d2_circle_L3_r2|subcycle, d2_disk_L2_r2|global; their 20 primary repetitions are superseded. Held-out speedups are not computed here (plan section 8).

## QC by cell

| Configuration | Schedule | n | CV | Timer sum / wall | Max drift | Finest level |
|---|---|---:|---:|---|---:|---|
| `d2_circle_L2_r2` | global | 5 | 0.042 | 0.984 to 0.984 | 2.2e-16 | [2] |
| `d2_circle_L2_r2` | subcycle (rerun) | 5 | 0.015 | 0.987 to 0.987 | 6.5e-16 | [2] |
| `d2_circle_L3_r2` | global (rerun) | 5 | 0.073 | 0.986 to 0.987 | 0.0e+00 | [3] |
| `d2_circle_L3_r2` | subcycle (rerun) | 5 | 0.026 | 0.990 to 0.990 | 2.2e-16 | [3] |
| `d2_circle_L4_r2` | global | 5 | 0.037 | 0.984 to 0.986 | 2.2e-16 | [4] |
| `d2_circle_L4_r2` | subcycle | 5 | 0.034 | 0.987 to 0.989 | 1.5e-15 | [4] |
| `d2_disk_L2_r2` | global (rerun) | 5 | 0.033 | 0.990 to 0.991 | 4.3e-16 | [2] |
| `d2_disk_L2_r2` | subcycle | 5 | 0.047 | 0.993 to 0.993 | 2.2e-15 | [2] |
| `d2_disk_L3_r2` | global | 5 | 0.023 | 0.980 to 0.982 | 1.1e-15 | [3] |
| `d2_disk_L3_r2` | subcycle | 5 | 0.045 | 0.991 to 0.993 | 1.1e-15 | [3] |
| `d2_disk_L4_r2` | global | 5 | 0.039 | 0.985 to 0.986 | 1.1e-15 | [4] |
| `d2_disk_L4_r2` | subcycle | 5 | 0.026 | 0.988 to 0.988 | 0.0e+00 | [4] |
| `d2_point_L2_r2` | global | 5 | 0.016 | 0.977 to 0.978 | 3.5e-14 | [2] |
| `d2_point_L2_r2` | subcycle | 5 | 0.030 | 0.975 to 0.976 | 2.4e-15 | [2] |
| `d2_point_L3_r2` | global | 5 | 0.020 | 0.973 to 0.974 | 9.2e-14 | [3] |
| `d2_point_L3_r2` | subcycle | 5 | 0.040 | 0.969 to 0.971 | 1.9e-15 | [3] |
| `d2_point_L4_r2` | global | 5 | 0.038 | 0.969 to 0.970 | 1.3e-13 | [4] |
| `d2_point_L4_r2` | subcycle | 5 | 0.029 | 0.959 to 0.960 | 1.1e-15 | [4] |
| `d3_ball_L2_r2` | global | 5 | 0.033 | 0.983 to 0.984 | 2.2e-16 | [2] |
| `d3_ball_L2_r2` | subcycle | 5 | 0.027 | 0.984 to 0.986 | 4.3e-16 | [2] |
| `d3_ball_L3_r2` | global | 5 | 0.035 | 0.999 to 0.999 | 2.2e-16 | [3] |
| `d3_ball_L3_r2` | subcycle | 5 | 0.030 | 0.999 to 0.999 | 0.0e+00 | [3] |
| `d3_circle_L2_r2` | global | 5 | 0.007 | 0.997 to 0.998 | 6.5e-16 | [2] |
| `d3_circle_L2_r2` | subcycle | 5 | 0.022 | 0.997 to 0.998 | 6.5e-16 | [2] |
| `d3_circle_L3_r2` | global | 5 | 0.030 | 0.997 to 0.997 | 6.5e-16 | [3] |
| `d3_circle_L3_r2` | subcycle | 5 | 0.035 | 0.997 to 0.998 | 2.2e-16 | [3] |
| `d3_point_L2_r2` | global | 5 | 0.045 | 0.995 to 0.995 | 2.2e-16 | [2] |
| `d3_point_L2_r2` | subcycle | 5 | 0.047 | 0.995 to 0.996 | 2.2e-16 | [2] |
| `d3_point_L3_r2` | global | 5 | 0.032 | 0.992 to 0.993 | 1.9e-15 | [3] |
| `d3_point_L3_r2` | subcycle | 5 | 0.048 | 0.992 to 0.993 | 2.2e-16 | [3] |
| `d3_sphere_L2_r2` | global | 5 | 0.016 | 0.998 to 0.998 | 6.5e-16 | [2] |
| `d3_sphere_L2_r2` | subcycle | 5 | 0.028 | 0.998 to 0.998 | 2.2e-16 | [2] |
| `d3_sphere_L3_r2` | global | 5 | 0.025 | 0.998 to 0.998 | 2.2e-16 | [3] |
| `d3_sphere_L3_r2` | subcycle | 5 | 0.029 | 0.998 to 0.998 | 6.5e-16 | [3] |

## Level counts (predictors; all configurations)

| Configuration | Role | δ | $M_\ell$ | Boxes | Mean growth | $r^\delta$ | $S_{\mathrm{id}}$ (counts) | β |
|---|---|---:|---|---|---:|---:|---:|---:|
| `d2_circle_L2_r2` | heldout | 1 | 16384, 15744, 25280 | 4, 20, 43 | 1.61 | 2 | 1.541 | 0.351 |
| `d2_circle_L3_r2` | heldout | 1 | 16384, 19648, 34752, 49216 | 4, 19, 39, 84 | 1.58 | 2 | 1.631 | 0.387 |
| `d2_circle_L4_r2` | heldout | 1 | 16384, 20992, 38336, 66624, 98880 | 4, 16, 42, 87, 190 | 1.68 | 2 | 1.659 | 0.397 |
| `d2_disk_L2_r2` | training | 2 | 16384, 29568, 104960 | 4, 9, 30 | 3.55 | 4 | 1.219 | 0.179 |
| `d2_disk_L3_r2` | training | 2 | 16384, 30976, 107584, 399424 | 4, 9, 36, 100 | 3.59 | 4 | 1.197 | 0.165 |
| `d2_disk_L4_r2` | training | 2 | 16384, 30976, 107584, 399424, 1557504 | 4, 9, 36, 100, 400 | 3.69 | 4 | 1.180 | 0.153 |
| `d2_point_L2_r2` | training | 0 | 16384, 576, 256 | 4, 1, 1 | 0.44 | 1 | 3.710 | 0.730 |
| `d2_point_L3_r2` | training | 0 | 16384, 576, 384, 384 | 4, 1, 1, 1 | 0.82 | 1 | 6.405 | 0.844 |
| `d2_point_L4_r2` | training | 0 | 16384, 576, 576, 576, 256 | 4, 1, 1, 1, 1 | 0.76 | 1 | 10.296 | 0.903 |
| `d3_ball_L2_r2` | training | 3 | 32768, 253952, 713728 | 1, 12, 46 | 2.81 | 8 | 1.179 | 0.151 |
| `d3_ball_L3_r2` | training | 3 | 32768, 262144, 884736, 3904512 | 1, 8, 27, 228 | 3.86 | 8 | 1.151 | 0.131 |
| `d3_circle_L2_r2` | heldout | 1 | 32768, 100352, 112640 | 1, 6, 22 | 1.12 | 2 | 1.437 | 0.304 |
| `d3_circle_L3_r2` | heldout | 1 | 32768, 119808, 192000, 209408 | 1, 8, 21, 50 | 1.32 | 2 | 1.632 | 0.387 |
| `d3_point_L2_r2` | training | 0 | 32768, 4096, 4096 | 1, 1, 1 | 1.00 | 1 | 2.857 | 0.650 |
| `d3_point_L3_r2` | training | 0 | 32768, 9216, 9216, 7168 | 1, 1, 1, 2 | 0.88 | 1 | 3.211 | 0.689 |
| `d3_sphere_L2_r2` | heldout | 2 | 32768, 204800, 549888 | 1, 12, 79 | 2.69 | 4 | 1.192 | 0.161 |
| `d3_sphere_L3_r2` | heldout | 2 | 32768, 262144, 837120, 2150400 | 1, 8, 39, 316 | 2.86 | 4 | 1.244 | 0.196 |

## Training configurations: measured speedup and overhead

| Configuration | $S=T_G/T_L$ | $S_{\mathrm{id}}$ | $H$ (s) | $x=H/K_G$ | β | One-run test holds | Subcycling wins |
|---|---:|---:|---:|---:|---:|---|---|
| `d2_disk_L2_r2` | 1.291 | 1.219 | -0.3354 | -0.214 | 0.179 | False | True |
| `d2_disk_L3_r2` | 1.387 | 1.197 | -0.6497 | -0.394 | 0.165 | False | True |
| `d2_disk_L4_r2` | 1.316 | 1.180 | -1.0947 | -0.333 | 0.153 | False | True |
| `d2_point_L2_r2` | 2.172 | 3.710 | -0.4332 | -0.128 | 0.730 | True | True |
| `d2_point_L3_r2` | 3.678 | 6.405 | -1.5216 | -0.305 | 0.844 | True | True |
| `d2_point_L4_r2` | 5.232 | 10.296 | -1.8282 | -0.439 | 0.903 | True | True |
| `d3_ball_L2_r2` | 1.213 | 1.179 | -0.1720 | -0.087 | 0.151 | False | True |
| `d3_ball_L3_r2` | 1.182 | 1.151 | -0.9013 | -0.098 | 0.131 | False | True |
| `d3_point_L2_r2` | 2.092 | 2.857 | -0.2332 | -0.060 | 0.650 | True | True |
| `d3_point_L3_r2` | 2.669 | 3.211 | -0.8143 | -0.193 | 0.689 | True | True |

## Flags

- d2_circle_L3_r2 global: CV 0.073 >= 0.05 after rerun (kept, flagged)
