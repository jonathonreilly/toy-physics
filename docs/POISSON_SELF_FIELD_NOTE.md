# Poisson Self-Field: Gravity from a Local Equation

**Date:** 2026-04-06
**Status:** retained positive — Poisson-generated field gives F~M=1.000, Born=1.6e-15, portable

## Question

Can the gravitational field be DERIVED from a local equation instead
of imposed as f=s/r?

## Result: YES

Solve the 2D Poisson equation at each layer:
  laplacian(f) = -source(iy, iz)

The source is a delta function at the mass position. The solution is
a 1/r-like profile that emerges from the Poisson equation, not from
assumption.

| Property | Imposed 1/r | Poisson-generated |
| --- | ---: | ---: |
| F~M (Fam1) | 0.990 | **0.9997** |
| F~M (Fam2) | 0.993 | **0.9993** |
| F~M (Fam3) | 0.994 | **0.9994** |
| Born | 0.00e+00 | **1.6e-15** |
| Gravity | TOWARD | **TOWARD** |
| Null (s=0) | exact | **exact** |

The Poisson field gives BETTER F~M than the imposed 1/r field (0.9997
vs 0.990). This is because the Poisson solution has the correct
lattice-adapted profile, not the continuum 1/r.

## What this means

The model's axioms can be reduced:
- OLD: causal DAG + path-sum + scalar field (imposed 1/r) + action S=L(1-f)
- NEW: causal DAG + path-sum + Poisson equation + action S=L(1-f)

The field is no longer an input — it's derived from a local PDE.
The 1/r profile is a CONSEQUENCE of the Poisson equation on the lattice,
not a starting assumption.

## Claim boundary

The Poisson solver is static (solved at each layer independently).
This is NOT yet a dynamical field equation (no time evolution).
The connection to the causal cone / retardation results requires
a time-dependent generalization (wave equation with proper evolution).
