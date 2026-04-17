# Graph-Dirac / Kähler-Dirac Requirements

**Date:** 2026-04-10  
**Branch:** `frontier/spot-checks`

## Purpose

This memo freezes the graph assumptions required by the retained staggered / Dirac
lane. It is not a claim that all graph families work. It is a requirements
document for the next implementation step: move the staggered mechanism off the
periodic cubic lattice and onto graph families that preserve the same transport
logic.

The current retained staggered result is the force-based canonical card in
[`frontier_staggered_17card.py`](../scripts/frontier_staggered_17card.py).
That lane is the reference point for the graph invariants below.

## What The Staggered Lane Actually Uses

The staggered architecture depends on all of the following:

- a bipartite site parity, so the field can carry an alternating sign structure
- a nearest-neighbor hopping operator, so the Dirac/staggered dispersion stays local
- an orientation or layering convention, so "forward" and "backward" hops are
  unambiguous
- a consistent notion of cycles or boundaries, so gauge/current observables are
  well-defined
- a graph family where the force observable is not overwhelmed by recurrence or
  parity artifacts

On the periodic cubic lattice, these conditions are naturally satisfied by the
standard staggering convention

```text
epsilon(x) = (-1)^(x1 + x2 + x3)
```

and by the nearest-neighbor Dirac/staggered hopping used in the current scripts.

## Required Graph Invariants

### 1. Bipartite structure

The graph must admit a global 2-coloring.

Why it matters:

- staggered fermions need an even/odd split
- the mass term and the kinetic term rely on alternating sign structure
- the family robustness tests depend on being able to define parity classes

Failure mode:

- odd cycles or local defects that destroy the 2-coloring
- no consistent even/odd sublattice
- chirality/parity becomes ambiguous and the force-based rows stop matching the
  intended physics

### 2. Orientation and staggering convention

The graph must support a stable notion of oriented nearest-neighbor transport.

Why it matters:

- the Dirac/staggered operator is not just adjacency; it is oriented hopping
- the sign factors that implement staggered gamma structure need a consistent
  convention across the graph
- current and gauge observables depend on the same orientation

Minimum requirement:

- each edge should have a reproducible "forward" / "backward" interpretation
- if the graph is undirected, the implementation must still induce a stable
  local orientation for the staggering phases

Failure mode:

- random edge orientation that changes from run to run
- local parity flips that cannot be extended globally
- gauge current becomes a proxy rather than a retained observable

### 3. Layering or causal compatibility

The graph should either:

- be explicitly layered, or
- admit a causal/topological ordering compatible with the staggered update

Why it matters:

- the retained staggered implementation is local and stepwise
- the graph-Dirac transport is easiest to preserve when updates move through
  layers or parity levels consistently
- DAG-like growth is only meaningful if the update order respects the graph
  orientation

Failure mode:

- cycles that force contradictory update order
- no monotone layer structure
- growth adds edges that destroy the previous staggering convention

### 4. Cycle constraints

Cycles are not automatically forbidden, but they must be controlled.

Allowed:

- even cycles that preserve bipartiteness
- toroidal cycles with consistent parity wrap
- bounded cycles that support a current/flux observable

Marginal:

- long irregular cycles that preserve bipartiteness but introduce strong
  recurrence
- torus quotients where parity wrap is technically valid but finite-size effects
  dominate the force observable

Incompatible:

- odd cycles
- non-bipartite wrap identifications
- cycles that break the staggering sign convention or invalidate a current loop

### 5. Locality / degree control

The transport law must remain nearest-neighbor or uniformly local.

Why it matters:

- the retained staggered result assumes local hopping
- the force-based gravity rows are meaningful only if propagation is not
  overwhelmed by long-range shortcuts
- high-degree or dense graphs can destroy the clean staggered interpretation

Failure mode:

- long-range edges act like hidden couplings
- dense graphs wash out the parity structure
- the force observable becomes graph-shape dependent rather than transport-based

## Family Classification

### Admissible

These families are structurally compatible with the retained staggered logic:

- even-sized rectangular lattices with periodic or open boundaries
- bipartite cubic lattices with consistent wrap parity
- layered bipartite graphs with bounded degree
- DAG-compatible bipartite growth graphs where each new layer preserves parity
- bipartite random geometric graphs, if the bipartition and orientation can be
  made globally consistent

### Marginal

These families may work, but only with careful implementation and explicit
validation:

- random geometric graphs after bipartitioning and pruning odd-cycle defects
- grown graphs that remain layered but develop local parity irregularities
- toroidal quotients with large finite-size recurrence
- irregular bipartite graphs with small local defects

These are worth testing, but they should not be assumed to preserve the staggered
physics without a dedicated harness.

### Incompatible

These families do not preserve the current staggered requirements:

- graphs with odd cycles
- non-bipartite random graphs
- dense graphs with no stable local orientation
- graphs with ambiguous parity under periodic identification
- complete or nearly complete graphs
- graphs whose edge structure destroys nearest-neighbor locality

If a family lands here, the right response is not to tune harder. The graph
family is wrong for the retained staggered operator.

## Failure Modes On Irregular Graphs

The current scripts show three recurring failure modes when the graph or
observable is not well matched to the staggered structure:

1. **Parity ambiguity**
   The even/odd decomposition no longer maps cleanly onto the graph.

2. **Recurrence artifacts**
   Periodic identifications or finite-size effects make centroid-based gravity
   oscillate with graph size even when the force remains well behaved.

3. **Gauge/current ambiguity**
   If there is no clean loop structure, a gauge test becomes a proxy rather than
   a retained observable.

Those failures are not the same thing as "the physics is wrong." They mean the
graph family does not satisfy the operator's assumptions.

## What The Current Results Say

The current branch supports the following claims:

- the staggered mechanism is robust on the periodic cubic lattice
- force is the correct gravity observable for the retained staggered card
- centroid-based gravity is too sensitive to recurrence on periodic lattices
- gauge response can be made native when the graph admits a real loop

The branch does **not** yet show that every graph family works.
The right next step is to test the retained staggered transport on graph families
that preserve bipartiteness, orientation, and locality.

## Practical Rule For Future Harnesses

When a new graph family is proposed, check these questions first:

- Can the graph be globally 2-colored?
- Can the staggering convention be defined without local exceptions?
- Can the update remain nearest-neighbor?
- Can a loop/current observable be defined natively?
- Does the force observable converge without recurrence artifacts?

If the answer to any of those is no, mark the family as marginal or incompatible
before spending time on a large harness.

