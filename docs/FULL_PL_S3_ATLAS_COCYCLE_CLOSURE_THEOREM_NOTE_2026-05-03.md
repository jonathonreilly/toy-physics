# Full PL S^3 Atlas Cocycle Closure on the 4-Simplex Boundary — Theorem Note

**Date:** 2026-05-03
**Type:** closing_derivation (output type a)
**Claim scope:** closes Obstruction 1 from cycle 10's GR atlas closure
stretch attempt by constructing the full 5-chart PL S^3 = ∂(4-simplex)
atlas data and numerically verifying the 10 triangle-overlap cocycle
conditions, the 10 pairwise overlap-invariance relations, and the 5
K_GR(D_i) nondegeneracies on the 10-dimensional symmetric-tensor basis.
**Status:** branch-local closing-derivation candidate; audit-lane
ratification required for any retained-grade interpretation.
**Runner:** [`scripts/frontier_full_pl_s3_atlas_cocycle_closure.py`](./../scripts/frontier_full_pl_s3_atlas_cocycle_closure.py)
**Authority role:** sharpens parent's class-A load-bearing step with
explicit numerical multi-chart cocycle compatibility on PL S^3.

## Executive summary

Cycle 10
([`GR_ATLAS_CLOSURE_STRETCH_ATTEMPT_NOTE_2026-05-02.md`](GR_ATLAS_CLOSURE_STRETCH_ATTEMPT_NOTE_2026-05-02.md))
provided a 2-chart minimal numerical demonstration of the parent's
overlap-invariance + K_GR-nondegeneracy claim. Its three named
obstructions were:

1. Multi-chart cocycle conditions on triple overlaps NOT verified.
2. Global stationary section on patched atlas NOT computed.
3. Atlas-refinement / continuum limit NOT addressed.

This note closes **Obstruction 1** and provides a partial spot-check
on Obstruction 2; Obstruction 3 remains untouched.

## A_min (minimal allowed premise set)

- (P1) Cycle 10's algebraic results, admitted-as-prior-cycle inputs:
  - Local bilinear form `B_D(h, k) = -Tr(D^{-1} h D^{-1} k)` on
    4×4 symmetric h, k with invertible 4×4 symmetric D.
  - Chart transition `D' = T^T D T` for invertible 4×4 T.
  - K_GR(D) on 10-dim symmetric-tensor basis, 10×10 nondegenerate
    Gram matrix of B_D.
  - Symmetric-tensor representation of T: induced rep R(T) on the
    10-dim basis, with R(T)R(S) = R(TS) on composition.
  - K_GR transition rule on a 2-chart overlap:
    G_{D'} = R(T)^{-T} G_D R(T)^{-1}.
- (P2) Standard linear algebra (admitted-context external):
  matrix similarity, induced representations on tensor spaces,
  4-simplex boundary combinatorics.
- (P3) Standard topological combinatorics: PL S^3 = boundary of the
  4-simplex on vertices {0, 1, 2, 3, 4}; 5 vertices, 10 edges, 10
  triangles, 5 tetrahedra (= ∂Δ^4 = 4-simplex boundary).

## Forbidden imports

- No GR field equations / specific solutions (Schwarzschild, Kerr,
  FLRW, etc.) consumed.
- No PDG observed values consumed.
- No literature numerical comparators consumed.
- No fitted selectors consumed.
- No admitted unit conventions load-bearing on retention.
- No same-surface family arguments.

## PL S^3 atlas combinatorics

The boundary of a 4-simplex on vertex set {0, 1, 2, 3, 4} is
combinatorially:

| element | count | role |
|---|---|---|
| 0-simplex (vertex) | 5 | charts (open-star at each vertex) |
| 1-simplex (edge) | 10 | chart pairwise overlaps |
| 2-simplex (triangle) | 10 | triple overlaps with cocycle conditions |
| 3-simplex (tetrahedron) | 5 | facets of the boundary |

The boundary ∂Δ^4 is homeomorphic to S^3, the 3-sphere. Each chart
covers an open star at a vertex; pairwise overlaps live on edges;
triple overlaps live on triangles. The cocycle condition sits on the
2-simplices.

## Atlas data construction

**Local backgrounds.** D_0 = diag(-1, 1, 1, 1) (Lorentzian signature,
Minkowski-like). For each i ∈ {1, 2, 3, 4}, choose a generic random
invertible 4×4 matrix T_{0i} (seed 20260503) and set
D_i = T_{0i}^T D_0 T_{0i}.

**Chart transitions T_{ij} for i < j**, all 10 edges of ∂Δ^4:

- **Spoke edges** `(0, i)` for i ∈ {1, 2, 3, 4}: 4 free transitions
  T_{0i} = T_{0i} (random invertible matrices).
- **Cycle edges** `(i, j)` for i, j ∈ {1, 2, 3, 4}, i < j: 6
  cocycle-forced transitions T_{ij} = T_{0i}^{-1} T_{0j}.

By construction T_{ij}^T D_i T_{ij} = T_{0j}^T (T_{0i}^{-1})^T D_i
T_{0i}^{-1} T_{0j} = T_{0j}^T D_0 T_{0j} = D_j (because
D_i = T_{0i}^T D_0 T_{0i} ⟹ D_0 = (T_{0i}^{-1})^T D_i T_{0i}^{-1}).

**This means the 4 free spoke transitions algebraically determine all
10 transitions and all 10 cocycle conditions.** The substantive
content of the cycle is verifying numerically that the algebra holds
on every triangle to machine precision.

## Cocycle structure on triple overlaps

For a triangle (i, j, k) with i < j < k, the three edges (i, j),
(j, k), (i, k) and their three transitions T_{ij}, T_{jk}, T_{ik}
must satisfy:

```
T_{ij} T_{jk} = T_{ik}
```

Reading: chart i → chart j → chart k composed equals direct
chart i → chart k transition. This is the standard 1-cocycle
condition for atlas data on a simplicial complex.

Convention: the equation should hold up to an element of the
stabilizer of D_i (the (3,1)-Lorentz group O(1,3)) acting on the
right of T_{ik}. In our random construction the spoke transitions
are generic, so the construction picks out a specific representative
in each conjugacy class and the cocycles hold to machine precision
by exact equality, no stabilizer ambiguity.

## Verification (numerical, runner-checked)

The runner [`frontier_full_pl_s3_atlas_cocycle_closure.py`](./../scripts/frontier_full_pl_s3_atlas_cocycle_closure.py)
verifies (PASS = 72, FAIL = 0):

1. **PL S^3 combinatorics correct**: 5 vertices, 10 edges, 10
   triangles, 5 tetrahedra.
2. **Atlas data construction succeeds**: 10 invertible 4×4 chart
   transitions T_{ij}; 5 invertible 4×4 backgrounds D_i with
   Lorentzian signature (1 negative eigenvalue each).
3. **5 K_GR nondegeneracies**: each K_GR(D_i) is a 10×10 symmetric
   matrix, |det K_GR(D_i)| > 1e-10 on every chart.
4. **10 pairwise overlap-invariance relations**: for each edge (i, j),
   B_{D_j}(T_{ij}^T h T_{ij}, T_{ij}^T k T_{ij}) = B_{D_i}(h, k) on
   5 random symmetric (h, k) pairs per edge (50 random tests total),
   max |diff| < 1e-12 on every edge.
5. **10 K_GR transition rules**: for each edge (i, j),
   K_GR(D_j) = R(T_{ij})^{-T} K_GR(D_i) R(T_{ij})^{-1} where R(T) is
   the 10×10 induced representation of T on the symmetric-tensor
   basis. max |diff| < 1e-12 on every edge.
6. **10 triangle cocycle conditions**: for each triangle (i, j, k),
   T_{ij} T_{jk} = T_{ik} to machine precision (max |diff| < 1e-15
   on every triangle). **This closes Obstruction 1 of cycle 10.**
7. **Counterfactual**: perturbing one forced edge T_{12} by 0.05 ×
   (random 4×4) breaks the cocycle on the 3 triangles containing
   edge (1, 2): (0, 1, 2), (1, 2, 3), (1, 2, 4). Restoration
   recovers the cocycle.
8. **Sanity**: each cycle edge T_{ij} for i, j ∈ {1, 2, 3, 4}, i<j
   is computed from the spoke transitions: T_{ij} = T_{0i}^{-1}
   T_{0j} (max |diff| = 0).
9. **Aggregate**: 5 + 10 + 10 + 10 = 35 core verifications all pass
   simultaneously.

Plus 1 partial spot-check on Obstruction 2 (Step 9 in runner):

10. **Patched stationary system on one edge**: solve K_GR(D_0) v_0 =
    J_0 for a non-trivial diagonal source J_0; transport J onto
    chart 1 by the source-pairing rule J_1 = R(T_{01})^{-T} J_0;
    solve K_GR(D_1) v_1 = J_1; verify v_1 equals the transported
    expectation R(T_{01}) v_0 to machine precision.

Total: 72 PASS / 0 FAIL.

## What this closes (cycle 10's Obstruction 1)

Quoted from cycle 10's named obstruction:

> Specific repair target: construct the chart transition data T_{ij}
> for each edge of the 4-simplex S³, then verify the 10 triple-overlap
> cocycle conditions.

The runner does exactly this:
- Constructs T_{ij} for all 10 edges of ∂Δ^4.
- Verifies the 10 triple-overlap cocycle conditions
  T_{ij} T_{jk} = T_{ik}.

**Obstruction 1 of cycle 10 is closed.**

## What this does NOT claim (remaining named obstructions)

### Remaining Obstruction A (was cycle 10's Obstruction 2): full global stationary section

The patched stationary system is only spot-checked on one edge with
one source. A full global stationary section requires:

- choosing a class of physical sources J_i compatibly defined on each
  chart;
- showing the local solutions v_i = K_GR(D_i)^{-1} J_i agree on all
  10 pairwise overlaps and 10 triangle overlaps simultaneously;
- proving uniqueness on the patched atlas.

The spot-check on one edge with one source verifies the source-
pairing rule is consistent at the algebra level, but does not
discharge the global solution-existence + uniqueness obligation.

### Remaining Obstruction B (was cycle 10's Obstruction 3): atlas-refinement / continuum limit

The parent's claim is restricted to FINITE atlases. The continuum
limit (or discretization-independence) is not addressed. Adding a
chart at a new vertex would extend the spoke construction by one
free transition; this preserves cocycles by construction. But the
continuum limit is a different question and remains open.

## What this claims

- `(C1)` PL S^3 = ∂Δ^4 atlas combinatorics: 5 charts, 10 edges, 10
  triangles, 5 tetrahedra.
- `(C2)` Explicit construction of compatible 5-chart atlas data:
  - 5 nondegenerate Lorentzian backgrounds D_i;
  - 10 invertible chart transitions T_{ij} (4 free + 6 cocycle-forced).
- `(C3)` All 5 K_GR(D_i) on 10-dim symmetric-tensor basis are
  10×10 nondegenerate symmetric Gram matrices.
- `(C4)` All 10 pairwise overlap-invariance relations B_{D_j} = B_{D_i}
  on transformed (h, k) verified to machine precision.
- `(C5)` All 10 K_GR transition rules verified to machine precision.
- `(C6)` All 10 triangle cocycle conditions T_{ij} T_{jk} = T_{ik}
  verified to machine precision.
- `(C7)` Counterfactual: a single perturbed edge breaks the cocycle
  on exactly the 3 triangles containing that edge.
- `(C8)` Source-pairing rule on a 1-edge patched stationary spot-check.

`(C1)` through `(C7)` together constitute the closing of cycle 10's
Obstruction 1.

## Cited dependencies

- (P1, cycle 10) [`GR_ATLAS_CLOSURE_STRETCH_ATTEMPT_NOTE_2026-05-02.md`](GR_ATLAS_CLOSURE_STRETCH_ATTEMPT_NOTE_2026-05-02.md) —
  prior-cycle algebraic primitives (B_D, K_GR, transition rule).
- (P2) [`UNIVERSAL_GR_LORENTZIAN_GLOBAL_ATLAS_CLOSURE_NOTE.md`](UNIVERSAL_GR_LORENTZIAN_GLOBAL_ATLAS_CLOSURE_NOTE.md) —
  parent row, audited_conditional, td=42, lbs=A.
- (P3) [`UNIVERSAL_GR_DISCRETE_GLOBAL_CLOSURE_NOTE.md`](UNIVERSAL_GR_DISCRETE_GLOBAL_CLOSURE_NOTE.md) —
  related universal-route note (not directly load-bearing here).
- (P4) Standard simplicial-complex combinatorics (admitted-context
  external).

## Forbidden imports check

- No PDG observed values consumed.
- No literature numerical comparators consumed.
- No fitted selectors consumed.
- No admitted unit conventions load-bearing on retention.
- No same-surface family arguments.
- No GR field equations / specific solutions consumed.

## Validation

Primary runner: [`scripts/frontier_full_pl_s3_atlas_cocycle_closure.py`](./../scripts/frontier_full_pl_s3_atlas_cocycle_closure.py)
verifies items 1-9 above. PASS = 72, FAIL = 0.

```bash
python3 scripts/frontier_full_pl_s3_atlas_cocycle_closure.py
```

## Cross-references

- [`GR_ATLAS_CLOSURE_STRETCH_ATTEMPT_NOTE_2026-05-02.md`](GR_ATLAS_CLOSURE_STRETCH_ATTEMPT_NOTE_2026-05-02.md) —
  cycle 10 sister: 2-chart minimal demo + 3 named obstructions.
  This note closes Obstruction 1 of that note.
- [`UNIVERSAL_GR_LORENTZIAN_GLOBAL_ATLAS_CLOSURE_NOTE.md`](UNIVERSAL_GR_LORENTZIAN_GLOBAL_ATLAS_CLOSURE_NOTE.md) —
  parent row.
- [`UNIVERSAL_GR_DISCRETE_GLOBAL_CLOSURE_NOTE.md`](UNIVERSAL_GR_DISCRETE_GLOBAL_CLOSURE_NOTE.md) —
  related universal-route note.
- [`STAGGERED_PARITY_COUPLING_FORCED_FROM_DIRAC_THEOREM_NOTE_2026-05-02.md`](STAGGERED_PARITY_COUPLING_FORCED_FROM_DIRAC_THEOREM_NOTE_2026-05-02.md) —
  cycle 05 retained-promotion campaign sister: framework's gravity
  sign work.

## Audit-graph effect

If independent audit ratifies this closing derivation:
- Parent row's load-bearing class-A step gains explicit numerical
  verification of multi-chart cocycle compatibility on PL S^3.
- Cycle 10's Obstruction 1 is **closed**.
- Cycle 10's Obstructions 2 (global stationary section) and 3
  (atlas-refinement) remain open as next-cycle stretch targets.
- Future cycle: solve the patched stationary system globally on
  arbitrary sources; address atlas-refinement / continuum limit.
