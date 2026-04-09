# Wave Static Matrix-Free Shared Geometry Compare

**Date:** 2026-04-08
**Status:** retained engine-equivalence probe

This probe compares the existing direct static solver against the
matrix-free static solver on one shared geometry and the same beam setup.

The test is intentionally narrow:

> Is the matrix-free static engine a drop-in replacement for the current
> direct discrete static comparator?

## What it compares

- exact discrete static field from the direct probe
- exact discrete static field from the matrix-free probe
- beam-side centroid shift through the same beam DAG

## Retained result

The retained runs use the shared frozen source at `z_phys = 3.0`
at two shared lattice spacings:

| H | realized `z_src` | `max |direct-mf|` | `rel field mismatch` | `rel(dS)` | `rel_MS` |
| ---: | ---: | ---: | ---: | ---: | ---: |
| `0.35` | `3.15` | `1.203e-08` | `4.481e-06` | `2.825e-06` | `22.86%` |
| `0.25` | `3.00` | `2.327e-08` | `7.940e-06` | `1.863e-06` | `62.09%` |

At both tested `H` values, the direct and matrix-free solvers agree
extremely closely on the static field and on the propagated static
beam response:

- `H=0.35`
  - direct residual `= 1.997e-10`
  - matrix-free residual `= 2.292e-10`
  - matrix-free iterations `= 86`
  - `dS direct = +0.010863`
  - `dS mf = +0.010863`
- `H=0.25`
  - direct residual `= 1.992e-10`
  - matrix-free residual `= 1.830e-10`
  - matrix-free iterations `= 115`
  - `dS direct = +0.015456`
  - `dS mf = +0.015456`

The underlying exact-static comparator is still far from `dM` on these
shared geometries, but that is a comparator-science issue, not an
engine-equivalence issue.

So the retained conclusion here stays narrow:

> matrix-free is a strong drop-in replacement for the direct exact-static
> engine on the shared geometries tested.

## Honest read

This note does **not** rescue the exact-comparator lane by itself.
At both tested `H` values, `rel_MS` is still large (`22.86%` and
`62.09%`), so the static comparator can still disagree materially
with the retarded response even when the two static engines agree
with each other almost exactly.

The retained read is:

- matrix-free is a sound engineering path for the exact-static branch
- the remaining problem is the comparator science, not the solver engine

## Artifact chain

- [`scripts/wave_static_matrixfree_shared_geometry_compare.py`](../scripts/wave_static_matrixfree_shared_geometry_compare.py)
- [`scripts/wave_static_matrixfree_shared_geometry_compare_freeze.py`](../scripts/wave_static_matrixfree_shared_geometry_compare_freeze.py)
- [`logs/2026-04-08-wave-static-matrixfree-shared-geometry-compare-h035.txt`](../logs/2026-04-08-wave-static-matrixfree-shared-geometry-compare-h035.txt)
- [`logs/2026-04-08-wave-static-matrixfree-shared-geometry-compare-h025.txt`](../logs/2026-04-08-wave-static-matrixfree-shared-geometry-compare-h025.txt)
