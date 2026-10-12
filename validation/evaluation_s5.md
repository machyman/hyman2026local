# S5 evaluation (analysis plan v1 section 8; amendment v2)

Frozen predictions SHA-256 `11d2e03060d6de2b0d26e76da09690e468fdff53851eda638bf2905fa8cc9721`; selected pair **K1+O3**.

## Held-out errors

| Configuration | $S$ measured | $\hat S$ | $e$ | 95% CI of $e$ |
|---|---:|---:|---:|---|
| `d2_circle_L2_r2` | 1.3668 | 1.4634 | 0.0706 | 0.0066 to 0.1326 |
| `d2_circle_L3_r2` | 1.5940 | 1.5721 | 0.0137 | 0.0046 to 0.1591 |
| `d2_circle_L4_r2` | 1.5044 | 1.6119 | 0.0715 | 0.0040 to 0.1199 |
| `d3_circle_L2_r2` | 1.2804 | 1.2790 | 0.0011 | 0.0007 to 0.0626 |
| `d3_circle_L3_r2` | 1.5205 | 1.4064 | 0.0750 | 0.0039 to 0.1329 |
| `d3_sphere_L2_r2` | 1.1906 | 1.0949 | 0.0804 | 0.0161 to 0.1156 |
| `d3_sphere_L3_r2` | 1.2217 | 1.1513 | 0.0577 | 0.0027 to 0.1095 |

**Median error:** 0.0706 (95% CI 0.0211 to 0.0823); tolerance 0.10.
**Held-out misses above 20 percent:** none.

## All twelve pairs on the held-out set (transparency, after the verdict)

| Pair | Median held-out error |
|---|---:|
| K1+O1 | 0.0322 |
| K2s+O1 | 0.0329 |
| K2+O1 | 0.0390 |
| K1+O2 | 0.0399 |
| K3+O1 | 0.0451 |
| K3+O2 | 0.0457 |
| K2+O2 | 0.0462 |
| K2s+O3 | 0.0538 |
| K3+O3 | 0.0555 |
| K2s+O2 | 0.0576 |
| K2+O3 | 0.0598 |
| K1+O3 | 0.0706 |

## Secondary analyses (descriptive)

| Configuration | Role | $S$ | $S_{\mathrm{id}}$ | $x=H/K_G$ | β | β − x | One-run test | Cost-weighted test | Subcycling wins | Growth | $r^\delta$ |
|---|---|---:|---:|---:|---:|---:|---|---|---|---:|---:|
| `d2_circle_L2_r2` | heldout | 1.367 | 1.541 | -0.286 | 0.351 | 0.637 | False | False | True | 1.61 | 2 |
| `d2_circle_L3_r2` | heldout | 1.594 | 1.631 | -0.425 | 0.387 | 0.812 | False | False | True | 1.58 | 2 |
| `d2_circle_L4_r2` | heldout | 1.504 | 1.659 | -0.450 | 0.397 | 0.848 | False | False | True | 1.68 | 2 |
| `d2_disk_L2_r2` | training | 1.291 | 1.219 | -0.214 | 0.179 | 0.394 | False | False | True | 3.55 | 4 |
| `d2_disk_L3_r2` | training | 1.387 | 1.197 | -0.394 | 0.165 | 0.559 | False | False | True | 3.59 | 4 |
| `d2_disk_L4_r2` | training | 1.316 | 1.180 | -0.333 | 0.153 | 0.486 | False | False | True | 3.69 | 4 |
| `d2_point_L2_r2` | training | 2.172 | 3.710 | -0.128 | 0.730 | 0.858 | True | True | True | 0.44 | 1 |
| `d2_point_L3_r2` | training | 3.678 | 6.405 | -0.305 | 0.844 | 1.149 | True | True | True | 0.82 | 1 |
| `d2_point_L4_r2` | training | 5.232 | 10.296 | -0.439 | 0.903 | 1.342 | True | True | True | 0.76 | 1 |
| `d3_ball_L2_r2` | training | 1.213 | 1.179 | -0.087 | 0.151 | 0.238 | False | False | True | 2.81 | 8 |
| `d3_ball_L3_r2` | training | 1.182 | 1.151 | -0.098 | 0.131 | 0.229 | False | False | True | 3.86 | 8 |
| `d3_circle_L2_r2` | heldout | 1.280 | 1.437 | -0.092 | 0.304 | 0.396 | False | False | True | 1.12 | 2 |
| `d3_circle_L3_r2` | heldout | 1.521 | 1.632 | -0.161 | 0.387 | 0.548 | True | True | True | 1.32 | 2 |
| `d3_point_L2_r2` | training | 2.092 | 2.857 | -0.060 | 0.650 | 0.710 | True | True | True | 1.00 | 1 |
| `d3_point_L3_r2` | training | 2.669 | 3.211 | -0.193 | 0.689 | 0.881 | True | True | True | 0.88 | 1 |
| `d3_sphere_L2_r2` | heldout | 1.191 | 1.192 | -0.088 | 0.161 | 0.250 | False | False | True | 2.69 | 4 |
| `d3_sphere_L3_r2` | heldout | 1.222 | 1.244 | -0.098 | 0.196 | 0.294 | False | False | True | 2.86 | 4 |
