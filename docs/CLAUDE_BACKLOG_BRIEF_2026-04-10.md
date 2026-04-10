# Claude Handoff: Next Significant Work

## Objective

Push the project forward in the most significant way:

1. test whether the retained staggered Dirac + potential gravity mechanism
   survives on axiom-like graph families
2. then prototype endogenous / backreacting gravity

Do **not** spend main effort on periodic-lattice polish or chiral-3D rescue.

## Frozen Current State

- Canonical staggered card:
  `frontier_staggered_17card.py`
- Full suite baseline:
  `frontier_staggered_full_suite.py`
  - `1D = 29/38`
  - `3D = 28/38`
- Force is the primary gravity observable for staggered lanes.
- Centroid/shell are diagnostics only.
- Scalar graph lane is the gravity/base-layer control.
- Chiral coin gravity is a diagnostic / negative control.

## Workstreams

### 1. Graph portability (highest priority)

Build staggered / Kähler-Dirac transport on:
- bipartite random geometric graphs
- bipartite growing graphs
- layered / DAG-compatible bipartite graphs

Start with a tight retained battery:
- Born / linearity
- norm / unitarity
- force sign
- `F∝M`
- achromatic force
- equivalence
- state-family robustness
- native gauge response if cycles exist

Required output:
- one retained harness
- one short note with honest pass/fail language

### 2. Backreaction prototype

Replace external `V = m * Phi` with a source-generated `Phi` on the same
graph/lattice.

Minimum acceptable prototype:
- source sector or density-generated `Phi`
- staggered matter evolves in that `Phi`
- minimal two-body / source-response / stability check
- force remains the primary gravity observable

Required output:
- one prototype script under `scripts/`
- one note under `docs/` that states exact results and failure modes
- use `docs/STAGGERED_BACKREACTION_NOTE.md` as the prototype spec

### 3. Graph-Dirac design memo

Write down the graph invariants required by the staggered lane:
- bipartite structure
- orientation / staggering convention
- layering or causal compatibility
- cycle constraints
- expected failure modes

Required output:
- one memo classifying graph families as admissible / marginal / incompatible

## Rules

- Keep force as the primary gravity observable on staggered lanes.
- Do not silently swap card semantics; document any semantic changes.
- Prefer one retained harness per task over many exploratory fragments.
- If a graph family fails structurally, say so quickly and move on.

## Success Condition

The project materially advances if staggered transport plus potential gravity
survives off the periodic cubic lattice. If it does not, pivot to a two-field
graph theory with scalar gravity sector + staggered matter sector.
