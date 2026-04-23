# A1 Route Recommendation — final consolidation

**Date:** 2026-04-22
**Status:** final recommendation after the A1 landscape investigation

## Summary of /loop investigation

A targeted investigation attempted to close the open physical bridge for
A1 (Frobenius equipartition `|b|²/a² = 1/2`, equivalently Brannen
`c = √2`, equivalently Koide `Q = 2/3`). The bridge is:

> Why does the physical charged-lepton packet extremize the block-total
> Frobenius functional `S_block = log(E_+) + log(E_⊥)` on Herm_circ(3)?

**11 iterations produced:**
- 181/181 PASS across 25 runners (A1 characterization and equivalence)
- Comprehensive landscape map of A1 (9 equivalent expressions all = 1/2)
- Import of review-branch theorems (KOIDE_FROBENIUS_ISOTYPE_SPLIT_UNIQUENESS,
  KOIDE_KAPPA_SPECTRUM_OPERATOR_BRIDGE, etc.)
- 5 independent physical-bridge closure attempts

## 5 failed bridge attempts

| # | Mechanism | Why it fails |
|---|---|---|
| 1 | `W[J=0] = log\|det D\|` | Different functional; extremum gives `\|b\|/a ~ 3.3`, not `1/√2` |
| 2 | Coleman-Weinberg 1-loop V_CW | Extremum at uniform eigenvalues (Q=1/3, not 2/3) |
| 3 | Gaussian max-entropy at fixed `\|\|H\|\|_F` | `⟨a²⟩=⟨\|b\|²⟩`, not `2⟨\|b\|²⟩` |
| 4 | CV=1 / exponential max-entropy | Continuous max-ent ≠ 3-point discrete |
| 5 | SU(2)_L Clebsch-Gordan normalization | Z_3 and SU(2)_L commute; same CG for all Yukawa elements |

Additional non-mechanism findings:
- 1-loop QFT gauge contributions enter β-functions with uniform sign
  (cannot give T(T+1) − Y² asymmetry)
- 't Hooft instanton corrections exp(-8π²/g²) at bare g₂² = 1/4 are
  ~ 10^{-138}-suppressed (negligible)
- MRU SO(2)-quotient route was demoted (review branch finding): the
  SO(2) rotation of (B_1, B_2) changes eigenvalue multiset, so not a
  physical gauge symmetry

## What the investigation definitively established

**A1 internal mathematical chain (RIGOROUS, from review branch):**

On Herm_circ(3), the block-total functional:

```
S_block(H) = log E_+(H) + log E_⊥(H)
E_+ = ||P_I(H)||_F² = (tr H)²/3
E_⊥ = ||(I - P_I)(H)||_F² = Tr(H²) - (tr H)²/3
```

is uniquely maximized (AM-GM under fixed Tr H²) at `E_+ = E_⊥`,
equivalently `κ = a²/|b|² = 2`, equivalently `A1` / `Q = 2/3`.

Every step is:
- Frobenius inner product: canonical trace form (unique up to scale)
- Isotype projector P_I: unique Frobenius-orthogonal projection
- AM-GM: textbook mathematical theorem
- Bridge identity `a₀²-2|z|² = 3(a²-2|b|²)`: exact symbolic

**Internal chain is gap-free. No hidden choices.**

## Recommendation

The physical bridge requires one of three routes:

### Route A: Adopt block-total extremum as retained primitive

**Hypothesis**: "The charged-lepton amplitude operator H on Herm_circ(3)
extremizes the block-total Frobenius functional S_block subject to
fixed Tr H²."

**Structural evidence** (documented in /loop iterations):
- 9 distinct natural quantities all equal 1/2 in retained framework
- Casimir-difference `T(T+1) − Y² = 1/2` UNIQUE to (L_doublet, Higgs) pair
- Lie-theoretic match: `|b|²/a² = |ω_{SU(2)_L, fund}|²` (Kostant)
- Clifford dim-ratio: `|b|²/a² = dim(spinor)/dim(Cl⁺(3))`

The multi-directional convergence on 1/2 strongly suggests block-total
extremum is the RIGHT primitive to adopt. It's the cleanest axiom-native
expression of A1 using retained CL3_SM_EMBEDDING quantum numbers.

**Cost**: 1 new retained primitive.
**Benefit**: would close A1 if the primitive is accepted on the package surface.

### Route B: Import Koide-Nishiura quartic V(Φ)

**Add** `V(Φ) = [2(trΦ)² − 3tr(Φ²)]²` to retained EW-scalar lane.

**Properties**:
- `V(Φ) ≥ 0` everywhere (sum of squares)
- `V(Φ) = 0` uniquely when `2(trΦ)² = 3tr(Φ²)` = A1 condition
- `V(Φ)` is U(3)-invariant (trace structure only)
- OUTSIDE Theorem 6 (4th-order Clifford cancellation)

Requires extending retained EW-scalar lane to include this quartic
Higgs-like term. Standard treatment: spontaneous symmetry breaking
gives A1 as VEV minimum.

**Cost**: extends EW-scalar lane content.
**Benefit**: would give a standard-QFT route to A1 as a VEV minimum.

### Route C: Novel QFT mechanism

The physical bridge might close via:
- Anomaly-related Wess-Zumino consistency condition distinguishing
  SU(2)_L from U(1)_Y with opposite signs
- Topological-sector contribution (Stiefel-Whitney w_2 on Cl(3) bundle)
- SU(2)_L vs U(1)_Y asymmetric integration measure

None is currently in retained framework; would require original
theoretical work beyond /loop's scope.

**Cost**: high (requires novel QFT research).
**Benefit**: could close the remaining bridge without adopting a new primitive.

## Concrete next step

Given the 5 failed bridge attempts and the strong Lie-theoretic/dim-
counting evidence, **Route A (adopt block-total extremum as primitive)
is the recommended next route to assess**.

The primitive is:
```
Retained primitive (proposed): the charged-lepton amplitude operator
H on Herm_circ(3) satisfies |b|²/a² = dim(spinor)/dim(Cl⁺(3)) = 1/2.

Equivalently: H sits at the AM-GM extremum of the block-total
Frobenius functional S_block = log E_+ + log E_⊥.

Equivalently: |b|²/a² = T(T+1)_SU(2)_L − Y²_Higgs = 1/2.

Equivalently: Brannen c = √2; Koide Q = 2/3.
```

All four expressions are mathematically equivalent and derivable from
retained CL3_SM_EMBEDDING quantum numbers.

**If this primitive is accepted, it closes the A1 bridge directly.**
Downstream Koide consequences would then need to be re-evaluated on the
canonical package surface together with the still-open Brannen physical
bridge and the separate lepton-scale support lane.

## Conclusion

The investigation appears to have exhausted the obvious standard bridge
mechanisms. Route A is the parsimonious primitive route; Route B is the
conservative import option; Route C is the ambitious new-physics option.
All three remain candidate ways to close A1. The main scientific value of
this note is that the choice is now explicit and the failed standard routes
are documented.
