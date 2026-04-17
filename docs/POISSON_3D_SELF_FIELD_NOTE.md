# Poisson 3D Self-Field: Full Field from One Local Equation

**Date:** 2026-04-07
**Status:** retained positive — full 3D field derived from single PDE; F~M=0.9999, Born=1.1e-15, gravity TOWARD all families

## Artifact chain

- [`scripts/poisson_3d_self_field.py`](../scripts/poisson_3d_self_field.py)
- [`logs/2026-04-07-poisson-3d-self-field.txt`](../logs/2026-04-07-poisson-3d-self-field.txt)

## Question

The 2D Poisson note left the longitudinal axis imposed via 1/(dx+0.1).
Can we drop that fudge and derive BOTH transverse and longitudinal
falloff from a single local equation?

## Result: YES

Solve laplacian_3D(f) = -source on the full (x, y, z) lattice with
a delta source at the mass position. 6-point Gauss-Seidel stencil,
200 iterations.

Both axes are now Poisson consequences. Profile is symmetric in
the transverse and longitudinal directions (peak at source layer,
falloff in both directions of x). No explicit longitudinal factor.

| Property | 2D Poisson (transverse only) | 3D Poisson (full) |
| --- | ---: | ---: |
| F~M (Fam1) | 0.9997 | **0.9999** |
| F~M (Fam2) | 0.9993 | **0.9998** |
| F~M (Fam3) | 0.9994 | **0.9998** |
| Born | 7.07e-16 | **1.10e-15** |
| Gravity | TOWARD | **TOWARD (3/3)** |
| Null (s=0) | exact | **exact** |
| Longitudinal axis | imposed 1/(dx+0.1) | **derived** |

F~M improves slightly (0.9998 vs 0.9994). Born stays at machine
precision. Gravity sign and null behaviour preserved.

## What this means

The model's axiom set drops one input. The OLD frontier was:
- causal DAG + path-sum + scalar field (2D Poisson + imposed 1/dx) + S=L(1-f)

The NEW frontier is:
- causal DAG + path-sum + 3D Poisson + S=L(1-f)

The scalar field is now fully a CONSEQUENCE of one local PDE on the
lattice, not a starting assumption in any axis. The 1/r profile,
the gravity TOWARD result, F∝M, and Born preservation all emerge
from the same single equation.

## Claim boundary

- Static field (solved once on the lattice; no time evolution)
- 6-point stencil; finer stencils not yet tested
- 200 iterations; convergence on larger NL not benchmarked
- Connection to causal cone / retardation requires the wave equation
  (time-dependent generalization of this PDE)
