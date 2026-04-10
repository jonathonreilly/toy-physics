# Work Backlog: Post-Staggered Priorities

**Date:** 2026-04-10  
**Branch:** `frontier/spot-checks`

## Frozen State

- Primary live architecture:
  `frontier_staggered_17card.py` (force-based canonical card)
- Retained full-suite baseline:
  `frontier_staggered_full_suite.py`
  - `1D`: `29/38`
  - `3D`: `28/38`
- Scalar graph lane remains the gravity/base-layer control.
- Chiral 3D remains a diagnostic / negative-control lane, not the main program.

## Immediate Queue

The next work package is no longer scorekeeping. It is:

1. **Backreaction prototype**
   - replace external `V = m * Phi` with a source-generated `Phi` on the same graph/lattice
   - keep force `F = -<dV/dz>` as the primary gravity observable
   - prove a minimal source-response / two-body / stability loop
   - use `docs/STAGGERED_BACKREACTION_NOTE.md` as the prototype spec

2. **Graph portability of staggered / Dirac transport**
   - bipartite random geometric graphs
   - bipartite growing graphs
   - layered / DAG-compatible bipartite graphs

3. **Graph-Dirac design memo**
   - classify graph families as admissible, marginal, or incompatible
   - name the graph invariants the staggered lane actually requires

## Priority Order

### P0: Keep the architecture stack clean

- **Primary matter lane**: staggered fermion + potential gravity
- **Gravity control lane**: scalar graph / graph-Laplacian scalar
- **Negative control lane**: chiral coin gravity

Do not spend primary research time on rescuing factorized `CH-3D`.

### P1: Graph portability of staggered / Dirac transport

**Question:** does the retained staggered mechanism survive on axiom-like graphs,
or is it mostly a periodic cubic-lattice artifact?

**Targets**
- Bipartite random geometric graphs
- Bipartite growing graphs
- Layered / DAG-compatible bipartite graphs

**Minimum retained subset**
- Born / linearity
- Norm / unitarity
- Force sign
- `F∝M`
- Achromatic force
- Equivalence
- State-family robustness
- Native gauge response if cycles exist

**Deliverable**
- One retained harness
- One results note with honest pass/fail language

### P2: Backreaction prototype

**Question:** can the potential become endogenous rather than external?

**First acceptable version**
- Source field or density solves for `Φ` on the same graph
- Staggered matter evolves in that `Φ`
- Recompute source-response / two-body / stability rows

**Deliverable**
- Minimal two-field or source-response prototype
- One note stating what is external, what is solved self-consistently, and what
  still fails

### P3: Graph-Dirac / Kähler-Dirac design memo

**Question:** what graph structure is actually required for staggered transport?

**Need to specify**
- Bipartite requirement
- Orientation / staggering conventions
- Layering / causal compatibility
- Allowed cycle structure
- Failure modes on irregular graphs

**Deliverable**
- One design memo that says which graph families are admissible, marginal, or
  structurally incompatible

## Secondary Work Only After P1-P3

- Larger 3D periodic lattices
- Centroid / shell convergence studies
- Extra moonshot rows
- Chiral 3D rescue attempts

## Stopping Rule

If staggered transport does **not** survive graph irregularity, stop promoting it
as the main foundational lane and fall back to:
- scalar graph as the retained base layer
- two-field graph theory as the main successor program
