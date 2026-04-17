# Poisson Self-Field: Transverse Profile from a Local Equation

**Date:** 2026-04-06
**Status:** retained positive (partial derivation) — transverse profile derived from 2D Poisson; longitudinal falloff still imposed; F~M=0.9997, Born=7.07e-16 on Poisson branch

## Artifact chain

- [`scripts/poisson_self_field.py`](../scripts/poisson_self_field.py)
- [`logs/2026-04-06-poisson-self-field.txt`](../logs/2026-04-06-poisson-self-field.txt)

## Question

Can the gravitational field be DERIVED from a local equation instead
of imposed as f=s/r?

## Result: PARTIAL

The TRANSVERSE (y, z) profile at each layer is derived from a 2D
Poisson equation:

  laplacian_⊥(f) = -source(iy, iz)

The LONGITUDINAL (x) falloff is still imposed via an explicit
1/(dx+0.1) factor in `_make_poisson_field`. So the full 3D field
law is not yet derived from a single PDE — only the transverse
profile is a Poisson consequence.

| Property | Imposed 1/r | Poisson (transverse) |
| --- | ---: | ---: |
| F~M (Fam1) | 0.990 | **0.9997** |
| F~M (Fam2) | 0.993 | **0.9993** |
| F~M (Fam3) | 0.994 | **0.9994** |
| Born (on Poisson branch) | 0.00e+00 | **7.07e-16** |
| Gravity | TOWARD | **TOWARD** |
| Null (s=0) | exact | **exact** |

The Born test is now run with the Poisson field active (not the
zero-field baseline). 7.07e-16 is at machine precision — the linear
propagator is preserved by the Poisson branch.

The transverse Poisson profile gives BETTER F~M than imposed 1/r
(0.9997 vs 0.990), because it is lattice-adapted instead of continuum.

## What this means

The model's transverse field is no longer an input — it's a
consequence of a local PDE on each layer. The longitudinal axis
remains imposed; deriving it requires solving a 3D Poisson or
wave equation across layers, which is the next step.

## Claim boundary

- Transverse profile: derived from 2D Poisson per layer
- Longitudinal profile: still imposed as 1/(dx+0.1)
- Static (no time evolution); dynamical field is the next milestone
- Connection to causal cone / retardation requires time-dependent generalization
