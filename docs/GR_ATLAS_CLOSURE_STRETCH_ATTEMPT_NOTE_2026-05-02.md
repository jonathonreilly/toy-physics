# GR Atlas Closure on PL S³ × R — Stretch Attempt with Named Obstructions

**Date:** 2026-05-02
**Type:** stretch_attempt (output type c)
**Claim scope:** documents a worked stretch attempt at the multi-chart
verification of `UNIVERSAL_GR_LORENTZIAN_GLOBAL_ATLAS_CLOSURE_NOTE.md`'s
claim of finite-atlas closure on discrete PL S³ × R. The attempt
provides a 2-chart minimal numerical demonstration of the exact
overlap-invariance and K_GR nondegeneracy properties; full-atlas
closure (5-chart PL S³ structure with 10 triple-overlap cocycle
conditions and global stationary section) remains open and is
documented as the named obstruction.
**Status:** stretch attempt, audit-lane ratification required for any
retained-grade interpretation. Not a closing derivation.
**Runner:** [`scripts/frontier_gr_atlas_closure_stretch_attempt.py`](./../scripts/frontier_gr_atlas_closure_stretch_attempt.py)
**Authority role:** sharpens parent's class-A load-bearing step with
explicit numerical 2-chart demonstration + named obstructions for
multi-chart closure.

## A_min (minimal allowed premise set)

- (P1) `UNIVERSAL_GR_LORENTZIAN_GLOBAL_ATLAS_CLOSURE_NOTE.md`
  algebraic claims:
  - Local bilinear form `B_D(h, k) = -Tr(D^{-1} h D^{-1} k)`.
  - Chart transition `D' = T_S^T D T_S` for invertible T_S.
  - Local operator `K_GR(D) = H_D ⊗ Λ_R` with H_D the Hessian of
    B_D and Λ_R the local Lorentzian-signature lattice operator.
- (P2) Standard linear algebra (admitted-context external):
  symmetric-tensor representation, matrix transformation under
  similarity.

## Forbidden imports

- No GR field equations as input (we're verifying the lattice/PL
  closure, not deriving GR).
- No specific solution (Schwarzschild, Kerr) as input.
- No phenomenological inputs (Shapiro delay, lensing, etc.).

## Worked attempt

### Step 1: Local bilinear form B_D(h, k)

Implement `B_D(h, k) = -Tr(D^{-1} h D^{-1} k)` for 4×4 symmetric h, k
on a generic 4×4 invertible D.

Verify:
- Symmetric: B_D(h, k) = B_D(k, h) ✓
- Bilinear: B_D(αh, k) = α B_D(h, k) ✓
- B_D(h, h) ≠ 0 generically (nondegeneracy)

### Step 2: Chart transition D → D' = T_S^T D T_S

Pick T_S as a random invertible 4×4 matrix. Construct D' = T_S^T D T_S.

Verify D' is invertible (since T_S is invertible).

### Step 3: Verify B_{D'}(h', k') = B_D(h, k)

For h' = T_S^T h T_S and k' = T_S^T k T_S, verify B_{D'}(h', k') =
B_D(h, k).

This is the **exact overlap-invariance identity** that the parent
note claims. We verify it numerically on random h, k.

### Step 4: Construct K_GR(D) and verify nondegeneracy

K_GR(D) is the operator on symmetric tensors h such that
`<h, K_GR(D) k> = B_D(h, k)`. In matrix form (in a basis of symmetric
tensors), K_GR(D) is the Gram matrix of B_D.

For 4×4 symmetric h, the dimension of the symmetric-tensor space is
10. So K_GR(D) is a 10×10 matrix.

Verify: K_GR(D) is nondegenerate (det ≠ 0) for generic D.

### Step 5: Verify K_GR transformation rule on 2-chart overlap

The parent note states:

```text
G_{D'} = T_S^{-T} G_D T_S^{-1}
```

where G_D is K_GR(D) in matrix form (with appropriate symmetric-tensor
representation). Verify this numerically.

### Step 6: Counterfactual — non-invertible T_S breaks the relation

If T_S is singular, D' is singular, K_GR(D') is undefined. The
overlap-invariance fails. Verify this counterfactual.

### Step 7: Counterfactual — degenerate D breaks K_GR(D) nondegeneracy

If D is singular, B_D involves D^{-1} which doesn't exist. K_GR(D)
is undefined. Verify this counterfactual.

## Named Obstructions

### Obstruction 1: Multi-chart cocycle conditions not verified

The 2-chart demonstration verifies pairwise compatibility:

```text
T_{12}^{-T} G_1 T_{12}^{-1} = G_2
```

For a full atlas of N charts with N(N-1)/2 pairwise overlaps and
N(N-1)(N-2)/6 triple overlaps, the cocycle condition is:

```text
T_{13} = T_{12} T_{23}
```

on every triple overlap. This is a CONSTRAINT on the atlas data, not
automatic from pairwise overlaps.

For PL S³, the boundary of a 4-simplex has **5 vertices, 10 edges, 10
triangles, 5 tetrahedra**. With charts on the 5 vertex-stars:
- 10 pairwise overlaps (one per edge)
- 10 triple overlaps (one per triangle)
- 5 quadruple overlaps (one per tetrahedron)

**Specific repair target**: construct the chart transition data
T_{ij} for each edge of the 4-simplex S³, then verify the 10 triple-
overlap cocycle conditions.

### Obstruction 2: Global stationary section not computed

Even if the atlas is consistently glued, computing the global
stationary section (the metric solution to the patched Einstein
equations on the full PL S³ × R) requires solving a coupled system
across all charts.

**Specific repair target**: implement the patched stationary system
solver and verify a global solution exists for a non-trivial source.

### Obstruction 3: PL S³ × R extension to non-finite atlases not addressed

The parent's claim is restricted to FINITE atlases. The continuum
limit (or discretization-independence) is not addressed.

**Specific repair target**: verify atlas-refinement compatibility:
adding a chart preserves the global stationary section.

## What this claims

- `(P1)` 2-chart overlap-invariance B_D(h, k) = B_{D'}(h', k') is
  numerically verified.
- `(P2)` K_GR(D) nondegeneracy verified for generic 3+1 backgrounds.
- `(P3)` 2-chart K_GR transition rule G_{D'} = T_S^{-T} G_D T_S^{-1}
  numerically verified.
- `(P4)` Counterfactuals: singular T_S or singular D break the
  relations as expected.
- `(P5)` Three named obstructions documented for full multi-chart
  closure.

## What this does NOT claim

- Does NOT verify multi-chart cocycle conditions (Obstruction 1).
- Does NOT compute the global stationary section (Obstruction 2).
- Does NOT address atlas-refinement / continuum limit
  (Obstruction 3).
- Does NOT close the parent row's verdict — sharpens it with
  explicit 2-chart demonstration + multi-chart gap documentation.
- Does NOT promote any author-side tier; audit-lane ratification is
  required.

## Cited dependencies

- (P1) [`UNIVERSAL_GR_LORENTZIAN_GLOBAL_ATLAS_CLOSURE_NOTE.md`](UNIVERSAL_GR_LORENTZIAN_GLOBAL_ATLAS_CLOSURE_NOTE.md) —
  audited_conditional, td=42, lbs=A.
- (P2) Standard symmetric-tensor representation (admitted-context
  external).

## Forbidden imports check

- No PDG observed values consumed.
- No literature numerical comparators consumed.
- No fitted selectors consumed.
- No admitted unit conventions load-bearing on retention.
- No same-surface family arguments.
- No GR field equations / specific solutions consumed.

## Validation

Primary runner: [`scripts/frontier_gr_atlas_closure_stretch_attempt.py`](./../scripts/frontier_gr_atlas_closure_stretch_attempt.py)
verifies:

1. B_D(h, k) symmetric, bilinear, generically nondegenerate.
2. Chart transition D' = T_S^T D T_S preserves invertibility.
3. **Overlap-invariance**: B_{D'}(T_S^T h T_S, T_S^T k T_S) = B_D(h, k).
4. K_GR(D) on symmetric-tensor basis: 10×10 matrix, nondegenerate.
5. **K_GR transition rule**: G_{D'} = T_S^{-T} G_D T_S^{-1}
   (in basis-aware form).
6. Counterfactual: singular T_S breaks invertibility.
7. Counterfactual: singular D breaks K_GR nondegeneracy.
8. Three named obstructions documented for full multi-chart closure.

## Cross-references

- [`UNIVERSAL_GR_LORENTZIAN_GLOBAL_ATLAS_CLOSURE_NOTE.md`](UNIVERSAL_GR_LORENTZIAN_GLOBAL_ATLAS_CLOSURE_NOTE.md) —
  parent row.
- [`UNIVERSAL_GR_DISCRETE_GLOBAL_CLOSURE_NOTE.md`](UNIVERSAL_GR_DISCRETE_GLOBAL_CLOSURE_NOTE.md) —
  related universal-route note.
- [`STAGGERED_PARITY_COUPLING_FORCED_FROM_DIRAC_THEOREM_NOTE_2026-05-02.md`](STAGGERED_PARITY_COUPLING_FORCED_FROM_DIRAC_THEOREM_NOTE_2026-05-02.md) —
  cycle 05 sister: framework's gravity sign work; this PR is the
  GR-side stretch attempt.
