# Staggered Backreaction Prototype

**Date:** 2026-04-10  
**Status:** prototype implemented

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
| bipartite random geometric | 36 | `+3.247e-01` | `+4.002e-02` | `8.767e-01` | `1.0000` | `1.862e-16` | `+1.184e-02` | `7.041e-01` | `4.44e-16` |
| bipartite growing | 48 | `+5.232e-01` | `+5.066e-02` | `9.032e-01` | `1.0000` | `2.874e-16` | `+1.782e-02` | `6.482e-01` | `7.77e-16` |
| layered bipartite DAG-compatible | 36 | `+1.714e+00` | `+2.127e-01` | `8.759e-01` | `1.0000` | `2.703e-16` | `+2.097e-01` | `1.453e-02` | `0.00e+00` |

## Readout

- Zero-source reduction is exact on all three families.
- Source-response linearity is exact at the tested strength scan.
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
