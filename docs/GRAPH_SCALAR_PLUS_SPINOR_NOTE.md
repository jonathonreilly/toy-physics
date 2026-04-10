# Graph Scalar + Spinor Note

**Date:** 2026-04-10  
**Harness:** [`scripts/frontier_graph_scalar_plus_spinor.py`](../scripts/frontier_graph_scalar_plus_spinor.py)

This note records the first lightweight two-field successor prototype:

- a simple scalar gravity background on a cubic graph
- a separate 4-component Dirac matter sector on the same graph

The goal is narrow: test whether a two-field split is more plausible than
forcing gravity, spin, and transport into one scalar or coin-based field.

## What The Prototype Tests

The script reports only four diagnostics:

1. norm behavior
2. whether the matter sector feels the scalar gravity signal
3. whether an obvious spinor-specific quantity survives
4. the biggest immediate blocker

## Prototype Result

The script is intentionally minimal and one-way coupled:

- the scalar background is a fixed normalized source bump
- the Dirac matter field evolves on the same cubic lattice
- the scalar background enters as a local potential for the matter field

That makes the model useful as a feasibility probe, not as a final theory.

First run on the default operating point (`n=17`, `steps=14`,
`matter_mass=0.22`, `source_offset=3`) gave:

- matter norm drift `~8e-15`
- matter centroid shift `delta_cz > 0` for all tested source strengths
- `gamma5` stayed near zero for the chosen initial state, but the
  upper/lower block imbalance remained clearly nonzero
- the signal scaled linearly across the small strength scan

## Interpretation

The two-field lane is worth pursuing if the matter sector:

- keeps unitary norm
- shifts toward the scalar source
- preserves a nontrivial spinor observable such as `gamma5` expectation or
  upper/lower block imbalance

If those three survive together, the next bottleneck is not local transport
anymore. It becomes self-consistent backreaction:

- the scalar field is still external
- the matter sector does not yet source the scalar field

That is the biggest immediate blocker for the two-field direction.

## Carry-Forward

If the prototype is positive, the next step is a self-consistent coupled model:

- scalar field sourced by matter density
- matter field propagated on the same graph
- both fields updated on one shared cubic topology

Right now the biggest blocker is still the same:

- the scalar sector is external and static
- there is no backreaction from spinor matter into the scalar source
- the lane is therefore a one-way proof of concept, not a closed two-field theory

That would test whether the scalar+spinor split is a real foundation or only a
useful one-way approximation.
