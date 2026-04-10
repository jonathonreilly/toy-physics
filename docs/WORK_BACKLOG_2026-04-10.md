# Work Backlog

**Scope:** next steps for the retained staggered / graph-Dirac program.

This backlog is ordered by value to the main project, not by ease.

## P0 - Endogenous Field Closure

- Portability is now established enough for the retained force battery:
  baseline portability, stress portability, and the failure map are all frozen.
- Native gauge/current closure is now retained on the cycle-bearing stress
  families; the remaining gauge holdout is the layered cycle-bearing family.
- The main blocker is no longer transport portability. It is endogenous-field
  scale closure on the cycle-bearing graph families.
- Push beyond
  [`frontier_staggered_backreaction_prototype.py`](../scripts/frontier_staggered_backreaction_prototype.py)
  and
  [`frontier_staggered_backreaction_iterative.py`](../scripts/frontier_staggered_backreaction_iterative.py):
  the solved/source-generated `Phi` has the right sign and structure, but it is
  still too weak relative to the external-kernel control on cycle-bearing
  families.
- Prioritize genuinely different source-to-field rules or iterative endogenous
  closure over more small linear preconditioning sweeps.
- Acceptance gate:
  materially reduce the force-scale gap on cycle-bearing families without
  losing TOWARD sign, exact source linearity, exact additivity, or norm
  stability.

## P1 - Native Gauge Holdout on Layered Graphs

- [`frontier_staggered_graph_gauge_closure.py`](../scripts/frontier_staggered_graph_gauge_closure.py)
  closes native gauge/current on the cycle-bearing stress families.
- The narrow remaining miss is the layered cycle-bearing family, which still
  has a weak current span and fails the retained threshold.
- Next step: engineer or identify a layered cycle geometry that supports a
  robust graph-native loop current without collapsing the layered/DAG-like
  structure.
- Stay on the same graph-native staggered transport law. No 1D helpers or proxy
  substitutions.

## P2 - Shell / Spectral Diagnostics for the Source Sector

- Compare `phi_solved(depth)` against `phi_ext(depth)` directly on one
  cycle-bearing family and one layered family.
- Add a low-mode or shell-profile readout so the force-scale miss is explained
  structurally, not just numerically.
- Use this to decide whether the next closure attempt should be:
  - a different Green's-function map
  - a genuinely nonlinear iterative source sector
  - or a graph-family-specific normalization rule

## P3 - Graph-Dirac Design

- Write down the graph invariants the staggered lane actually needs.
- Separate "bipartite", "layered", "cycle-bearing", and "DAG-compatible" as
  explicit architectural constraints.
- Identify which graph families are structurally incompatible before coding.

## P4 - Documentation Hygiene

- Keep the force-based staggered card separate from the repo-wide centroid card.
- Keep the portability probe separate from the canonical card.
- Preserve the full-suite baseline as `29/38` in 1D and `28/38` in 3D.
- Tighten the staggered card doc so the semantic differences table fully matches
  the force-based script and the tested family sets.

## Acceptance Criteria

- A portability result is promotable only if it stays honest across graph
  family changes, not just on one retained graph.
- Backreaction is promotable only if the force rows survive with an endogenous
  `Phi`.
- A design memo is promotable only if it lists the required graph invariants
  and failure modes concretely enough to guide implementation.
