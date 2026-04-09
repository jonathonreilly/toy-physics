# Wave Static Matrix-Free Shared Geometry Compare

**Date:** 2026-04-08

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

The current retained run uses the shared frozen source at `z_phys = 3.0`
and the shared lattice spacing `H = 0.25`.

The direct and matrix-free solvers agree extremely closely on the static
field:

- `max |direct - mf| = 2.327e-08`
- `rel field mismatch = 7.940e-06`
- direct residual `= 1.992e-10`
- matrix-free residual `= 1.830e-10`
- matrix-free iterations `= 115`

On the beam side, the propagated static responses also match very closely:

- `dS direct = +0.015456`
- `dS mf = +0.015456`
- `rel(dS) = 1.863e-06`

The underlying exact-static comparator is still far from `dM` on this
shared geometry (`rel_MS ≈ 62%`), but that is a comparator-science issue,
not an engine-equivalence issue.

So the retained conclusion here stays narrow:

> matrix-free is a strong drop-in replacement for the direct exact-static
> engine on the shared geometry tested, even at the finer retained `H=0.25`
> point.

## Artifact chain

- [`scripts/wave_static_matrixfree_shared_geometry_compare.py`](../scripts/wave_static_matrixfree_shared_geometry_compare.py)
- [`logs/2026-04-08-wave-static-matrixfree-shared-geometry-compare.txt`](../logs/2026-04-08-wave-static-matrixfree-shared-geometry-compare.txt)
