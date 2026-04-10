# Work Backlog

**Scope:** next steps for the retained staggered / graph-Dirac program.

This backlog is ordered by value to the main project, not by ease.

## P0 - Portability

- Extend [`frontier_staggered_graph_portability.py`](../scripts/frontier_staggered_graph_portability.py) to larger and more irregular bipartite graphs.
- Run [`frontier_staggered_graph_portability_stress.py`](../scripts/frontier_staggered_graph_portability_stress.py) as the next portability gate on larger, more irregular, less forgiving bipartite families.
- Add one more graph family if it clarifies the boundary between "portable" and "periodic-lattice only".
- Keep the retained battery narrow: Born/linearity, norm, force sign, `F∝M`,
  achromatic force, equivalence, robustness, and gauge if cycles exist.

## P1 - Backreaction

- Replace the external source potential with a graph-solved source sector.
- Test whether the force rows survive once `Phi` is endogenous instead of imposed.
- Keep the transport law fixed while only the source field changes.

## P2 - Graph-Dirac Design

- Write down the graph invariants the staggered lane actually needs.
- Separate "bipartite", "layered", "cycle-bearing", and "DAG-compatible" as
  explicit architectural constraints.
- Identify which graph families are structurally incompatible before coding.

## P3 - Documentation Hygiene

- Keep the force-based staggered card separate from the repo-wide centroid card.
- Keep the portability probe separate from the canonical card.
- Preserve the full-suite baseline as `29/38` in 1D and `28/38` in 3D.

## Acceptance Criteria

- A portability result is promotable only if it stays honest across graph
  family changes, not just on one retained graph.
- Backreaction is promotable only if the force rows survive with an endogenous
  `Phi`.
- A design memo is promotable only if it lists the required graph invariants
  and failure modes concretely enough to guide implementation.
