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

## What This Prototype Is Not

- not a full self-gravitating theory
- not a cosmology or Hawking test
- not a replacement for the retained staggered card
- not a claim that backreaction is solved if only the source is external

## Next Implementation Targets

- [`scripts/frontier_staggered_backreaction_prototype.py`](../scripts/frontier_staggered_backreaction_prototype.py)
- [`STAGGERED_BACKREACTION_RESULTS_2026-04-10.md`](./STAGGERED_BACKREACTION_RESULTS_2026-04-10.md)
- next step: iterate the same graph-solved Poisson update until the source-
  generated force scale moves closer to the external-kernel control on the
  cycle-bearing families

## Why This Matters

This is the first meaningful step beyond the current retained staggered
architecture. If gravity can be sourced internally on the same graph without
breaking the force-based result, the model moves from "field in a background"
to a genuinely interacting graph theory.
