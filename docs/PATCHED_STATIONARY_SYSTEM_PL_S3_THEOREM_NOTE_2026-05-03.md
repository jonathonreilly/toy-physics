# Patched Stationary System on PL S^3 — Theorem Note

**Date:** 2026-05-03
**Type:** closing_derivation (output type a)
**Claim scope:** closes Obstruction 2 from cycle 10's GR atlas closure
stretch attempt by implementing the patched stationary system solver
on cycle 13's 5-chart PL S^3 = ∂(4-simplex) atlas. Verifies global
solution existence + uniqueness on 6 distinct source profiles, with
all 10 edge-compatibilities + 10 triangle-compatibilities + 5
tetrahedron-compatibilities checked per profile.
**Status:** branch-local closing-derivation candidate; audit-lane
ratification required for any retained-grade interpretation.
**Runner:** [`scripts/frontier_patched_stationary_system_pl_s3.py`](./../scripts/frontier_patched_stationary_system_pl_s3.py)
**Authority role:** sharpens parent's class-A load-bearing step with
explicit numerical patched-system solver on PL S^3.

## Executive summary

Cycle 10
([`GR_ATLAS_CLOSURE_STRETCH_ATTEMPT_NOTE_2026-05-02.md`](GR_ATLAS_CLOSURE_STRETCH_ATTEMPT_NOTE_2026-05-02.md))
provided a 2-chart minimal numerical demonstration of the parent's
overlap-invariance + K_GR-nondegeneracy claim with three named
obstructions:

1. Multi-chart cocycle conditions on triple overlaps NOT verified.
2. Global stationary section on patched atlas NOT computed.
3. Atlas-refinement / continuum limit NOT addressed.

Cycle 13 ([`FULL_PL_S3_ATLAS_COCYCLE_CLOSURE_THEOREM_NOTE_2026-05-03.md`](FULL_PL_S3_ATLAS_COCYCLE_CLOSURE_THEOREM_NOTE_2026-05-03.md))
closed **Obstruction 1** by constructing the full 5-chart atlas and
verifying all 10 cocycle conditions T_{ij} T_{jk} = T_{ik}.

This cycle (14) closes **Obstruction 2** by implementing the patched
stationary system solver on cycle 13's atlas. **Obstruction 3** remains
the only open named obstruction.

## A_min (minimal allowed premise set)

- (P1) Cycle 10's algebraic results, admitted-as-prior-cycle inputs:
  - Local bilinear form `B_D(h, k) = -Tr(D^{-1} h D^{-1} k)` on
    4×4 symmetric h, k with invertible 4×4 symmetric D.
  - Chart transition `D' = T^T D T` for invertible 4×4 T.
  - K_GR(D) on 10-dim symmetric-tensor basis, 10×10 nondegenerate
    Gram matrix of B_D.
  - Symmetric-tensor representation of T: induced rep R(T) on the
    10-dim basis.
  - K_GR transition rule on a 2-chart overlap:
    G_{D'} = R(T)^{-T} G_D R(T)^{-1}.
- (P2) Cycle 13's atlas results, admitted-as-prior-cycle inputs:
  - 5-chart atlas on ∂Δ^4: 5 backgrounds D_i (with D_0 = diag(-1,1,1,1)),
    10 transitions T_{ij} (4 free spokes T_{0i} from seed 20260503,
    6 cycle-derived T_{ij} = T_{0i}^{-1} T_{0j}).
  - 10 triangle cocycle conditions T_{ij} T_{jk} = T_{ik}.
  - 5 K_GR(D_i) nondegenerate.
  - 10 K_GR transition rules across edges.
- (P3) Standard linear algebra (admitted-context external):
  - Linear systems Ax = b, nondegenerate solver,
  - Induced representations on tensor spaces.

## Forbidden imports

- No GR field equations / specific solutions (Schwarzschild, Kerr,
  FLRW, etc.) consumed.
- No PDG observed values consumed.
- No literature numerical comparators consumed.
- No fitted selectors consumed.
- No admitted unit conventions load-bearing on retention.
- No same-surface family arguments.

## The patched stationary system

On the 5-chart atlas of cycle 13, the patched stationary system is

    K_GR(D_i) h_i = J_i,    i = 0, 1, 2, 3, 4

with edge-compatibility on every overlap (i, j) ∈ EDGES (10 edges):

    h_j = R(T_{ij}) h_i                          (h-transport)
    J_j = R(T_{ij})^{-T} J_i                     (source-pairing)

and triangle-compatibility on every triple overlap (i, j, k) ∈
TRIANGLES (10 triangles):

    R(T_{jk}) R(T_{ij}) = R(T_{ik})              (anti-rep cocycle on h)
    R(T_{jk})^{-T} R(T_{ij})^{-T} = R(T_{ik})^{-T}    (dual on sources)

**The order in the rep cocycle reverses from the matrix cocycle**
because R is an *anti-homomorphism* (R(AB) = R(B) R(A)) — see
"Anti-rep convention" below.

## Anti-rep convention

The action h ↦ T^T h T on 4×4 symmetric h is a *right action*: when
we apply T then S in succession, we get

    h ↦ T^T h T ↦ S^T T^T h T S = (TS)^T h (TS)

So the coefficient-vector rep R defined by `v' = R(T) v` for
`h' = T^T h T` satisfies

    R(TS) = R(S) R(T)        (anti-homomorphism)

Combined with cycle 13's matrix cocycle `T_{ij} T_{jk} = T_{ik}`, this
gives

    R(T_{ik}) = R(T_{ij} T_{jk}) = R(T_{jk}) R(T_{ij})

which is the rep-level cocycle that the patched-system solver uses for
triangle compatibility. The dual statement on sources (with R(T)^{-T})
is

    R(T_{ik})^{-T} = R(T_{jk})^{-T} R(T_{ij})^{-T}

(note the order of the inverse-transposes preserves the order of the
underlying anti-rep, because (R(T_{jk}) R(T_{ij}))^{-T} = R(T_{jk})^{-T}
R(T_{ij})^{-T}).

## Theorem (closing derivation)

**Theorem (patched stationary system on PL S^3).** Let
{D_0, ..., D_4} and {T_{ij}}_{(i,j) ∈ EDGES} be the cycle 13 atlas.
For an arbitrary 4×4 symmetric source J_0 on chart 0, define
J_i = R(T_{0i})^{-T} J_0 ∈ ℝ^{10} on each chart i = 1, 2, 3, 4
(source-pairing from chart 0). Then:

(A) **Existence**: for each i, the chart-local equation
K_GR(D_i) h_i = J_i has a unique solution h_i ∈ ℝ^{10} (because
K_GR(D_i) is 10×10 nondegenerate, by cycle 13 Step 4).

(B) **Edge-compatibility**: for every edge (i, j) ∈ EDGES,
h_j = R(T_{ij}) h_i (10 conditions). This follows from cycle 13's
K_GR transition rule G_j = R(T_{ij})^{-T} G_i R(T_{ij})^{-1} combined
with the source-pairing rule J_j = R(T_{ij})^{-T} J_i and the
anti-rep cocycle R(T_{0j}) = R(T_{ij}) R(T_{0i}) (which holds because
R is an anti-rep and T_{0i} T_{ij} = T_{0j}).

(C) **Triangle-compatibility**: for every triangle (i, j, k) ∈
TRIANGLES, h_k = R(T_{jk}) R(T_{ij}) h_i = R(T_{ik}) h_i (10
conditions). This follows from edge-compatibility iterated through
two edges, plus the anti-rep cocycle.

(D) **Tetrahedron-compatibility**: for every tetrahedron
(i, j, k, l) ∈ TETRAHEDRA, all 6 pairwise transports within the
tetrahedron agree (5 tetrahedra × 6 pairs = 30 conditions).

(E) **Linearity in source**: for any α, β ∈ ℝ and source profiles
J_a, J_b, the patched solution for α J_a + β J_b is α h(J_a) +
β h(J_b) on every chart (5 charts).

(F) **Counterfactual robustness**: deviation from source-pairing
breaks edge-compatibility; deviation from cocycle breaks triangle-
compatibility. Both verified.

The 5-tuple (h_0, h_1, h_2, h_3, h_4) constitutes the **global
stationary section** of the patched system, defined modulo the
trivial kernel of the local K_GR operators.

**Proof.** By construction (Steps 3-5 of the runner) and direct
numerical verification at machine precision (max diff < 1e-7 on
every overlap, residuals < 1e-13 on every chart-local solve).

## Verification (numerical, runner-checked)

The runner [`frontier_patched_stationary_system_pl_s3.py`](./../scripts/frontier_patched_stationary_system_pl_s3.py)
verifies (PASS = 51, FAIL = 0):

1. **Cycle 13 atlas reconstruction** (3 pre-flight checks):
   5 backgrounds + 10 transitions + 10 cocycle conditions still hold.
2. **6 source profiles** (7 checks): trace, pure_time, pure_space,
   shear, random_gaussian, structural — all verified symmetric.
3. **30 chart-local solves** (6 source profiles × 5 charts): residuals
   2e-15 to 3e-13 on every chart-local solve.
4. **60 edge-vector compatibility checks** (6 source profiles × 10
   edges): max diff 5e-13 on h_j = R(T_{ij}) h_i across every edge.
5. **60 source-pairing checks** (6 source profiles × 10 edges):
   max diff 8e-14 on J_j = R(T_{ij})^{-T} J_i across every edge.
6. **60 triangle-compatibility checks** (6 source profiles × 10
   triangles): max diff 4e-13.
7. **3 tetrahedron-compatibility aggregates** (3 source profiles ×
   5 tetrahedra × 6 pairs each = 90 pairwise transports total).
8. **10 4×4 matrix-reconstruction checks** (structural source × 10
   edges): h_j_mat = T_{ij}^T h_i_mat T_{ij}, closing the loop on
   the coefficient-vector representation.
9. **Existence + uniqueness aggregate** for the structural source
   on the patched atlas.
10. **Counterfactual: source-pairing failure** breaks edge-(0,1)
    compatibility while not affecting other edges.
11. **Counterfactual: cocycle failure** (perturbed T_{12}) breaks
    edge-(1,2) compatibility.
12. **Anti-rep cocycle verification** (10 triangles): R(T_{jk})
    R(T_{ij}) = R(T_{ik}) at machine precision.
13. **Dual cocycle verification** (10 triangles): R(T_{jk})^{-T}
    R(T_{ij})^{-T} = R(T_{ik})^{-T}.
14. **Linearity in source**: 5-chart linearity check on a 2-source
    combination at machine precision.
15. **Aggregate verification** across all 6 source profiles.
16. **Cycle 13 spot-check recovery**: cycle 14's chart-1 solve for
    the trace source matches cycle 13's edge-(0,1) spot check.

Total: 51 PASS / 0 FAIL.

## What this closes (cycle 10's Obstruction 2)

Quoted from cycle 10's named obstruction:

> Specific repair target: implement the patched stationary system
> solver and verify a global solution exists for a non-trivial source.

The runner does exactly this:
- Implements the patched-system solver on cycle 13's atlas.
- Verifies global solutions exist for **6 distinct non-trivial source
  profiles** (not just one).
- Verifies edge-compatibility on every one of 10 edges.
- Verifies triangle-compatibility on every one of 10 triangles.
- Verifies tetrahedron-compatibility on every one of 5 tetrahedra.
- Demonstrates linearity in source.
- Provides counterfactuals for both source and cocycle failure modes.

**Obstruction 2 of cycle 10 is closed.**

## What this does NOT claim (remaining named obstruction)

### Remaining Obstruction (was cycle 10's Obstruction 3): atlas-refinement / continuum limit

The parent's claim is restricted to FINITE atlases. The continuum
limit (or discretization-independence) is not addressed. Adding a
chart at a new vertex would extend the spoke construction by one
free transition; this preserves cocycles and the patched-system
solver by construction. But the continuum limit is a different
question and remains open.

This is the only remaining named obstruction from cycle 10's
stretch-attempt note.

## What this claims

- `(C1)` Patched stationary system K_GR(D_i) h_i = J_i has a unique
  global solution on cycle 13's 5-chart PL S^3 atlas for any
  symmetric-tensor source J_0 on chart 0, with J_i defined by
  source-pairing.
- `(C2)` Global section satisfies edge-compatibility on all 10 edges.
- `(C3)` Global section satisfies triangle-compatibility on all 10
  triangles via the anti-rep cocycle.
- `(C4)` Global section satisfies tetrahedron-compatibility on all
  5 tetrahedra (4-vertex consistency).
- `(C5)` Solver is linear in source (verified).
- `(C6)` Counterfactuals: deviations from source-pairing or cocycle
  break compatibility as expected.
- `(C7)` 4×4 matrix reconstruction h_j_mat = T_{ij}^T h_i_mat T_{ij}
  holds on every edge, closing the loop with the underlying tensor
  representation.
- `(C8)` Algebraic theorem: R is an anti-homomorphism on the
  symmetric-tensor representation; R(T_{jk}) R(T_{ij}) = R(T_{ik})
  is the operative triangle-compatibility relation.

`(C1)` through `(C8)` together constitute the closing of cycle 10's
Obstruction 2.

## Cited dependencies

- (P1, cycle 10) [`GR_ATLAS_CLOSURE_STRETCH_ATTEMPT_NOTE_2026-05-02.md`](GR_ATLAS_CLOSURE_STRETCH_ATTEMPT_NOTE_2026-05-02.md) —
  prior-cycle algebraic primitives (B_D, K_GR, transition rule).
- (P2, cycle 13) [`FULL_PL_S3_ATLAS_COCYCLE_CLOSURE_THEOREM_NOTE_2026-05-03.md`](FULL_PL_S3_ATLAS_COCYCLE_CLOSURE_THEOREM_NOTE_2026-05-03.md) —
  prior-cycle atlas (5 charts, 10 edges, 10 triangles, cocycle data).
- (P3) [`UNIVERSAL_GR_LORENTZIAN_GLOBAL_ATLAS_CLOSURE_NOTE.md`](UNIVERSAL_GR_LORENTZIAN_GLOBAL_ATLAS_CLOSURE_NOTE.md) —
  parent row, audited_conditional, td=42, lbs=A.
- (P4) Standard linear algebra (admitted-context external).

## Forbidden imports check

- No PDG observed values consumed.
- No literature numerical comparators consumed.
- No fitted selectors consumed.
- No admitted unit conventions load-bearing on retention.
- No same-surface family arguments.
- No GR field equations / specific solutions consumed.

## Validation

Primary runner: [`scripts/frontier_patched_stationary_system_pl_s3.py`](./../scripts/frontier_patched_stationary_system_pl_s3.py)
verifies items 1-16 above. PASS = 51, FAIL = 0.

```bash
python3 scripts/frontier_patched_stationary_system_pl_s3.py
```

## Cross-references

- [`FULL_PL_S3_ATLAS_COCYCLE_CLOSURE_THEOREM_NOTE_2026-05-03.md`](FULL_PL_S3_ATLAS_COCYCLE_CLOSURE_THEOREM_NOTE_2026-05-03.md) —
  cycle 13 sister: 5-chart atlas + 10 cocycle conditions verified.
  This note builds on cycle 13's atlas to close Obstruction 2.
- [`GR_ATLAS_CLOSURE_STRETCH_ATTEMPT_NOTE_2026-05-02.md`](GR_ATLAS_CLOSURE_STRETCH_ATTEMPT_NOTE_2026-05-02.md) —
  cycle 10: 2-chart minimal demo + 3 named obstructions (Obstruction
  1 closed by cycle 13; Obstruction 2 closed by this note;
  Obstruction 3 remains open).
- [`UNIVERSAL_GR_LORENTZIAN_GLOBAL_ATLAS_CLOSURE_NOTE.md`](UNIVERSAL_GR_LORENTZIAN_GLOBAL_ATLAS_CLOSURE_NOTE.md) —
  parent row.
- [`UNIVERSAL_GR_DISCRETE_GLOBAL_CLOSURE_NOTE.md`](UNIVERSAL_GR_DISCRETE_GLOBAL_CLOSURE_NOTE.md) —
  related universal-route note (not directly load-bearing here).
- [`STAGGERED_PARITY_COUPLING_FORCED_FROM_DIRAC_THEOREM_NOTE_2026-05-02.md`](STAGGERED_PARITY_COUPLING_FORCED_FROM_DIRAC_THEOREM_NOTE_2026-05-02.md) —
  cycle 05 retained-promotion campaign sister: framework's gravity
  sign work.

## Audit-graph effect

If independent audit ratifies this closing derivation:
- Parent row's load-bearing class-A step gains explicit numerical
  verification of the global stationary section on the patched PL
  S^3 atlas for arbitrary symmetric-tensor sources.
- Cycle 10's Obstruction 2 is **closed**.
- Combined with cycle 13's closure of Obstruction 1, only
  Obstruction 3 (atlas-refinement / continuum limit) remains as a
  next-cycle stretch target.
- Future cycle: extend the patched-system solver to sources defined
  on a refined PL S^3 (more vertices) or address the continuum
  limit. Adding charts preserves cocycles + solver by spoke
  construction, but a continuum limit is a substantively different
  problem.

## Author-side disclosures

- This note documents a closing-derivation candidate.
- No retained-grade promotion claimed; audit-lane ratification
  required.
- The numerical verification is to machine precision on every test
  point (residuals 2e-15 to 3e-13 on chart-local solves; max diff
  ~5e-13 on edge compatibility; ~4e-13 on triangle compatibility).
- The substantive content beyond cycle 13 is the **solver itself**:
  given an arbitrary chart-0 source J_0, the runner produces the
  global stationary section h = (h_0, ..., h_4) and verifies all
  10 edges, 10 triangles, and 5 tetrahedra of the simplicial
  complex are mutually compatible.
- The discovery during cycle 14 that R is an anti-homomorphism
  (not a homomorphism) — and the corresponding correct ordering
  R(T_{jk}) R(T_{ij}) = R(T_{ik}) — is the algebraic mechanism
  that makes triangle-compatibility automatic given the matrix
  cocycle. Both versions (correct anti-rep ordering and incorrect
  homomorphism ordering) are diagnostically tested in the runner.
