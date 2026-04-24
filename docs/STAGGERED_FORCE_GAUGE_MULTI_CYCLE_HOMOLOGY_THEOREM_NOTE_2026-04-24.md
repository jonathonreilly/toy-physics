# Multi-Cycle Homology Extension of the Force-vs-Gauge Separation Theorem

**Date:** 2026-04-24
**Status:** theorem-grade extension of the loop-15 force-vs-gauge
separation theorem to graphs with arbitrary first Betti number `b_1`.
**Runner:** `scripts/frontier_staggered_force_gauge_multi_cycle_homology_theorem.py`
**Result:** `15/15 PASS`. Wallclock 0.02 s.
**Predecessor:** [`STAGGERED_FORCE_GAUGE_SEPARATION_THEOREM_NOTE_2026-04-24.md`](STAGGERED_FORCE_GAUGE_SEPARATION_THEOREM_NOTE_2026-04-24.md)
(loop 15, single-cycle theorem).

## 1. Question

Loop 15 proved the structural force-vs-gauge separation on
single-cycle graphs (square, triangle, pentagon). The natural
N+2 extension is to graphs with multiple independent cycles, where
the cycle-homology dimension `b_1(G)` is the number of independent
gauge observables. Does the theorem hold uniformly across the full
homology basis?

## 2. Theorem (extension)

Given any connected graph `G = (V, E)` with scalar source field
`phi: V -> R`:

### M.1 First Betti number via Euler formula

```
b_1(G) = |E| - |V| + c
```

where `c = #` of connected components. This counts the number of
independent cycles in `G`. For example:

- bow-tie (two triangles sharing one edge): `V=4, E=5, c=1 -> b_1=2`.
- triangular prism: `V=6, E=9, c=1 -> b_1=4`.

### M.2 Fundamental cycle basis via BFS spanning tree

A BFS spanning tree of `G` has `|V| - c` tree edges. The remaining
`b_1` edges are "back edges". Each back edge `(u, v)`, together
with the unique tree path from `v` to `u`, forms a fundamental
cycle. The `b_1` fundamental cycles are a basis of the cycle space
`H_1(G, Z)`.

### M.3 Stokes for exact 1-form on every basis cycle

For `j = d phi` (the exterior derivative of a scalar 0-form, i.e.
`j(i, j) = phi(j) - phi(i)`):

```
sum_{e in C} j(e) = 0  for every cycle C in G
```

In particular, the integral vanishes on every basis cycle. By
linearity of the cycle space, the integral also vanishes on every
linear combination of basis cycles (i.e., every cycle in `G`).
Verified symbolically on the bow-tie's two basis cycles and the
triangular prism's four basis cycles, plus a non-basis outer
hexagon on the prism and an outer quadrilateral on the bow-tie.

### M.4 Per-cycle detector spans

Each fundamental cycle has its own source-proximal non-bridge
edge. Different cycles can have vastly different optimal spans,
depending on the cycle's source-proximity:

- A cycle that visits the source vertex has its source-proximal
  edge incident to the source, giving a near-source large span.
- A cycle far from the source has its source-proximal edge at
  distance ≥ 2 from the source, giving a smaller span.

On the triangular prism with source at vertex 5 (top triangle, not
the BFS root) and Yukawa screening `mu=1.0`, the per-cycle optimal
spans differ by **2.7x** between the source-distant bottom-triangle
cycle (span 0.466) and the source-proximal cycles reaching the top
triangle (span 1.264).

### M.5 b_1 independent gauge observables

The `b_1` cycles in the basis correspond to `b_1` independent
"gauge observables" — i.e., independent line-integral observables
over distinct cycle homology generators. All are zero as cycle
integrals (by M.3), but each has its own per-edge optimal-detector
span (by M.4), giving `b_1` independent detector readouts on a
graph with `b_1` independent cycles.

This is the proper "gauge observable basis" on multi-cycle graphs,
generalizing the loop-15 single-cycle theorem.

## 3. Worked examples

### Bow-tie (b_1 = 2)

Vertices `{0, 1, 2, 3}`, edges `{(0,1), (0,2), (1,2), (1,3), (2,3)}`.

Fundamental cycles (BFS root = 0):

- `cycle 0 = (1, 0, 2, 1)` from back edge `(1, 2)`.
- `cycle 1 = (2, 0, 1, 3, 2)` from back edge `(2, 3)`.

Both share the source vertex `0`, so optimal spans are equal
(both 0.7863 with mu=0.5). Cycle integrals: identically zero.

### Triangular prism (b_1 = 4)

Vertices `{0,..,5}`, edges = bottom triangle `(0,1), (1,2), (0,2)`
+ top triangle `(3,4), (4,5), (3,5)` + verticals `(0,3), (1,4),
(2,5)`. `V=6, E=9, b_1 = 4`.

Fundamental cycles (BFS root = 0):

- `cycle 0`: back edge `(1, 2)` -> `(1, 0, 2, 1)`.
- `cycle 1`: back edge `(3, 4)` -> `(3, 0, 1, 4, 3)`.
- `cycle 2`: back edge `(3, 5)` -> `(3, 0, 2, 5, 3)`.
- `cycle 3`: back edge `(4, 5)` -> `(4, 1, 0, 2, 5, 4)`.

With source at vertex 5 (top triangle, far from BFS root) and
mu=1.0:

- cycle 0 (bottom triangle only): max span = 0.466.
- cycle 1 (bottom + one vertical): max span = 0.466.
- cycle 2, cycle 3: contain edges adjacent to vertex 5 (edges
  `(2,5)`, `(5,4)`): max span = 1.264.

Ratio of max-span / min-span across the basis: **2.71x**. The
b_1 independent gauge observables are all zero as cycle integrals
but have distinct detector spans reflecting their cycle-source
proximity.

## 4. Verdicts

| Section | Test | Verdict |
|---|---|---|
| A | Euler formula on bow-tie + prism | PASS |
| B.1, B.2 | Fundamental cycle count = b_1 | PASS |
| C.1, C.2 | Cycle integral = 0 on all basis cycles | PASS |
| D.1, D.2 | Non-basis cycle integral = 0 (chain linearity) | PASS |
| E.1 | Per-cycle source-proximal edge = max-span edge | PASS |
| E.2 | Per-cycle spans well-defined as b_1 observables | PASS |
| F.1 | Prism gauge observables = b_1 (= 4) | PASS |
| F.2 | Prism per-cycle span ratio > 2x with source ≠ root | PASS |
| G | All basis cycle integrals = 0 numerically (40 time samples) | PASS |
| H.1 | Honest open: non-abelian lift is N+4 | PASS |

## 5. What this changes

- The loop-15 single-cycle theorem is now extended to a full
  multi-cycle / homology-basis theorem.
- Future graph-native backreaction cards can specify the gauge-
  observable basis for any graph topology in terms of its
  fundamental-cycle decomposition.
- Per-cycle source-proximal edge rules are well-defined for each
  basis cycle independently.
- The `b_1` independent gauge observables (one per homology
  generator) are now characterized in terms of detector spans, not
  cycle integrals (which are all zero by Stokes).

## 6. What this does NOT close

- The theorem is for scalar `phi` (U(1)-trivial). The non-abelian
  lift (`phi -> A_µ` connection, cycle integral -> Wilson loop) is
  the planned N+4 extension.
- Graphs with multi-vertex sources (rather than a single source
  vertex) require the cycle-source-proximity to be redefined; this
  generalization is straightforward but not covered here.
- Time-dependent kernel choices beyond Yukawa (e.g., Coulomb,
  logarithmic) are not explicitly tested; the theorem is
  kernel-agnostic at the structural level (M.1-M.3) but the
  span-magnitude prediction (M.4) does depend on the kernel.

## 7. Falsifier

- A cycle in the basis producing nonzero integral of `j = d phi`
  (would refute M.3, contradicting `d o d = 0`).
- `b_1(G)` from Euler formula disagreeing with the fundamental
  cycle count (would refute M.2).
- Per-cycle source-proximal edge failing the optimal-span
  prediction (would refute M.4).
- A cycle outside the basis giving an integral inconsistent with
  the chain-linearity prediction (would refute M.5).

The runner exposes all four; 15/15 gates pass.

## 8. Provenance

- Runner: `scripts/frontier_staggered_force_gauge_multi_cycle_homology_theorem.py`
- Dependencies: `sympy`, `numpy`, `math`, `collections.deque`
  (no frontend harness; uses graph helpers built in the runner).
- Result: `15/15 PASS`, wallclock `0.02 s`.
- Reproducibility: fully deterministic; symbolic + numerical
  verification on explicit small graphs (bow-tie b_1=2, triangular
  prism b_1=4).
- Runtime caveat: validation host Python 3.12.8, numpy 2.4.1, scipy
  1.17.0, sympy 1.14.0 vs pinned 3.13.5, 2.4.4, 1.17.1. Purely
  algebraic; version drift is not a confounder.
