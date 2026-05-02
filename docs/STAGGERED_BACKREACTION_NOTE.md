# Staggered Backreaction Prototype

**Date:** 2026-04-10  
**Status:** bounded - bounded or caveated result note

## Objective

Replace the externally imposed gravity potential `V = m * Phi` with a
source-generated `Phi` on the same lattice or graph, while keeping the
staggered matter transport law intact.

The primary observable remains the force:

`F = -<dV/dz>`

## Minimum Acceptable Prototype

1. A source sector that generates `Phi` from density or point-source data on
   the same graph.
2. Staggered matter that evolves in that generated `Phi`.
3. A minimal two-body / source-response / stability check.
4. A zero-source control that reduces exactly to free staggered transport.

## Required Controls

- `Phi = 0` baseline
- fixed external `Phi` baseline
- source doubled vs source removed
- stability under modest lattice-size or graph-family changes

## Minimum Success Criteria

- source-generated `Phi` changes the force response relative to the zero-source
  control
- force remains TOWARD in the intended weak-field regime
- norm stays stable
- the prototype distinguishes external background coupling from endogenous
  source-generated coupling

## First Retained Run

The current prototype already gives a clean bounded source-response read on the
retained graph families:

| Family | n | `F_ext` | `F_solve` | force gap | source `R²` | two-body resid | self-force | self-gap | norm |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| bipartite random geometric | 36 | `+1.488e+00` | `+5.593e-02` | `9.624e-01` | `0.9830` | `1.264e-16` | `+3.382e-02` | `3.953e-01` | `4.44e-16` |
| bipartite growing | 48 | `+1.750e+00` | `+6.788e-02` | `9.612e-01` | `0.9864` | `2.046e-16` | `+4.282e-02` | `3.692e-01` | `7.77e-16` |
| layered bipartite DAG-compatible | 36 | `+1.852e+00` | `+2.183e-01` | `8.822e-01` | `0.9998` | `6.561e-16` | `+2.405e-01` | `1.016e-01` | `0.00e+00` |

## Readout

- Zero-source reduction is exact on all three families.
- Source-response linearity holds with `R^2 >= 0.98` (1/3 families
  cross the `R^2 > 0.99` near-exactness threshold; the layered DAG-
  compatible family at `R^2 = 0.9998`).
- Two-body additivity is exact to machine precision.
- Force stays TOWARD on every tested family.
- The remaining gap is not the sign or stability, but the mismatch between the
  external-kernel control and the solved endogenous field. That is the next
  backreaction seam.

## What This Prototype Is Not

- not a full self-gravitating theory
- not a cosmology or Hawking test
- not a replacement for the retained staggered card
- not a claim that backreaction is solved if only the source is external

## Next Implementation Targets

- [`scripts/frontier_staggered_backreaction_prototype.py`](../scripts/frontier_staggered_backreaction_prototype.py)
- next step: iterate the same graph-solved Poisson update until the source-
  generated force scale moves closer to the external-kernel control on the
  cycle-bearing families
- follow-on target: a graph-portability backreaction probe that reuses the same
  retained bipartite families, then extends to the adversarial failure-map
  variants only if the retained rows remain stable

## Why This Matters

This is the first meaningful step beyond the current retained staggered
architecture. If gravity can be sourced internally on the same graph without
breaking the force-based result, the model moves from "field in a background"
to a genuinely interacting graph theory.
