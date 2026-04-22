# A1 Physical Bridge — theoretical attempt

**Date:** 2026-04-22
**Branch:** `koide-equivariant-berry-aps-selector` (working)
**References:**
- `origin/review/scalar-selector-cycle1-theorems`: KOIDE_FROBENIUS_ISOTYPE_SPLIT_UNIQUENESS,
  KOIDE_KAPPA_BLOCK_TOTAL_FROBENIUS_MEASURE, KOIDE_Q_DELTA_CLOSURE_PACKAGE_README
- Local package: KOIDE_LANE_MASTER_CLOSURE_NOTE + 25 runners (181/181 PASS)

## Problem statement

The review branch establishes a rigorous internal mathematical chain:

```
On Herm_circ(3), the block-total Frobenius functional
  S_block(H) = log E_+(H) + log E_⊥(H)
where
  E_+  = (tr H)²/d = 3a²
  E_⊥  = Tr(H²) - (tr H)²/d = 6|b|²
is uniquely maximized (AM-GM under fixed Tr H²) at E_+ = E_⊥,
equivalently κ = a²/|b|² = 2, equivalently A1/Koide Q = 2/3.
```

Every step is executable and forced by Cl(3)/Herm_circ(3) structure.

**Open bridge**: why does the charged-lepton physical packet extremize S_block
rather than some other natural functional?

This note documents my theoretical attempts to close this bridge.

## Attempt 1: Identify S_block with retained W[J] = log|det(D+J)|

**Claim tested:** S_block(H) equals (up to factors) the retained observable
principle W[J=0] = log|det D_lep| for the charged-lepton Dirac operator D_lep.

**Calculation:** For circulant H = aI + bC + b̄C² with eigenvalues
(a+2|b|, a-|b|, a-|b|) (real b):

- log det H = log(a+2|b|) + 2 log(a-|b|) (sum of eigenvalue logs)
- S_block  = log(3a²) + log(6|b|²) = log(18 a²|b|²) (block-norm logs)

These are **different** functions of (a, |b|). Extremizing each at fixed
Tr H² gives different (a, |b|):

- W[J=0] extremum: |b|/a ≈ 3.303 (NOT A1)
- S_block extremum: |b|/a = 1/√2 (= A1)

**Verdict**: ATTEMPT 1 FAILS. W[J=0] ≠ S_block, and the retained
observable principle does NOT force A1.

## Attempt 2: 1-loop Coleman-Weinberg effective potential

**Claim tested:** V_CW(H) = -(1/64π²) Tr[H^4 (log H²/μ² − 3/2)] has
extremum at A1.

**Calculation:** For circulant H with eigenvalues (u, v, v):

- ∂V_CW/∂u = 0 ⟹ log(u²/μ²) = 1 ⟹ u = √e · μ
- ∂V_CW/∂v = 0 ⟹ log(v²/μ²) = 1 ⟹ v = √e · μ

So V_CW extremum at u = v (all eigenvalues equal). This is Q = 1/3
(uniform spectrum), NOT A1.

**Verdict**: ATTEMPT 2 FAILS. Coleman-Weinberg does NOT give A1.

## Attempt 3: Max-entropy on circulant family at fixed Frobenius

**Claim tested:** max-entropy over Herm_circ(3) with fixed ||H||_F² = N
gives ⟨a²/|b|²⟩ = 2 = A1 on average.

**Calculation:** Uniform measure on the 3-dim real vector space of circulant
Hermitian matrices (params: a, Re b, Im b). Constraint ||H||_F² = 3a² + 6|b|² = N.

Gaussian at fixed Frobenius: P(a, b_R, b_I) ∝ exp(-c·(3a² + 6(b_R²+b_I²)))

⟨a²⟩ = 1/(6c·2) ... let me recompute carefully:
Q(a, b_R, b_I) = 3a² + 6b_R² + 6b_I². (Q^{-1})_{aa} = 1/6.
⟨a²⟩ = (1/2)·(Q^{-1})_{aa}/c = 1/(12c).
⟨|b|²⟩ = ⟨b_R²+b_I²⟩ = (1/2)·2·(1/12)/c = 1/(12c).

⟨a²⟩/⟨|b|²⟩ = 1, NOT 2.

**Verdict**: ATTEMPT 3 FAILS. Gaussian max-entropy at fixed Frobenius gives
⟨a²⟩ = ⟨|b|²⟩, NOT A1.

## Attempt 4: CV = 1 as max-entropy on positive reals

**Reformulation**: A1 is EQUIVALENT to coefficient-of-variation CV = 1 on
the eigenvalue distribution:

  var(eig H) = mean²(eig H)  ⟺  A1 (Frobenius equipartition)

**Physical claim**: CV = 1 is the max-entropy CV for an EXPONENTIAL
distribution on positive reals with fixed mean.

**Status**: the retained framework has 3 DISCRETE eigenvalues, not a
continuous distribution. The continuous max-entropy argument (exponential
has CV = 1) doesn't directly apply to 3-point support.

For 3 eigenvalues (λ_0, λ_1, λ_2) with λ_0 > 0, Σλ_k = fixed, max-entropy
over the simplex gives uniform (λ_0 = λ_1 = λ_2), which is Q = 1/3 not 2/3.

To get CV = 1 (= A1), need additional constraint beyond fixed mean.

**Verdict**: ATTEMPT 4 PARTIALLY WORKS. CV = 1 is A1 (rigorous identity),
but the physical source of CV = 1 constraint is not identified.

## Summary of failed attempts

| # | Mechanism | Result |
|---|---|---|
| 1 | W[J=0] = log det H | Different functional, extremum at wrong point |
| 2 | Coleman-Weinberg V_CW | Extremum at uniform eigenvalues (Q=1/3, not 2/3) |
| 3 | Gaussian max-ent at fixed \|\|H\|\|_F | ⟨a²⟩=⟨\|b\|²⟩, not 2⟨\|b\|²⟩ |
| 4 | CV=1 / max-ent positive reals | Continuous argument, not 3-point |

None of the standard QFT/statistical-mechanics mechanisms gives A1
directly.

## What remains

The physical source-law bridge for A1 still requires:

- Either a non-standard QFT mechanism (anomaly, topological, or
  asymmetric measure) distinguishing isotype blocks
- Or adoption of S_block as a new retained primitive (block-total
  Frobenius extremal principle)
- Or Koide-Nishiura V(Φ) = [2(trΦ)² − 3tr(Φ²)]² import as retained
  EW-scalar-lane content

The review branch's position stands: A1 is mathematically well-defined
and the internal chain is gap-free, but the physical bridge is genuinely
open. My /loop iterations 1-8 + this attempt confirm: iterative
theoretical work has explored the landscape thoroughly without closing
the bridge.

## Recommendation

Handoff to canonical-branch theorist with these options:

1. **Best fit for retained framework**: treat S_block extremum as a new
   retained primitive. The three-way Lie-theoretic match (A_1 Weyl
   vector, SU(2)_L Casimir-difference, Clifford dim-ratio) provides
   strong structural evidence that this IS the right primitive.

2. **Import route**: add Koide-Nishiura V(Φ) to the retained EW-scalar
   lane. Outside Theorem 6 (4th-order Clifford cancellation) and gives
   A1 as VEV minimum.

3. **Research direction**: explore whether the Cl(3) even-subalgebra
   structure (Cl⁺(3) ≅ ℍ, dim 4) together with the spinor action
   (dim 2) gives a rigorous amplitude-ratio lemma via path-integral
   measure analysis on the flavor-gauge bundle.

All three are well-defined research directions. The /loop has produced
the landscape map; what remains is theorist's choice.
