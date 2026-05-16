# A1 Physical Bridge — theoretical attempt

**Date:** 2026-04-22
**References:**
- `origin/review/scalar-selector-cycle1-theorems`: KOIDE_FROBENIUS_ISOTYPE_SPLIT_UNIQUENESS,
  KOIDE_KAPPA_BLOCK_TOTAL_FROBENIUS_MEASURE, KOIDE_Q_DELTA_CLOSURE_PACKAGE_README
- current charged-lepton support packet plus the April 22 support runners

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

**Status**: the proposed_retained framework has 3 DISCRETE eigenvalues, not a
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

Recommended next options:

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

## 5. Executable no-go runner

Companion runner:
`scripts/frontier_koide_a1_physical_bridge_attempt_nogo_2026_04_22.py`.

The runner makes Attempts 1-4 executable as symbolic identities on the
circulant Hermitian carrier `H = a I + b C + bbar C^2`:

- Section A: log|det H| at fixed Tr(H^2) has its critical point at
  `|b|/a` strictly off `1/sqrt(2)` (A.2 verifies `dW/dt|_(t=pi/4) != 0`;
  A.3 locates the actual critical point and quantifies the gap).
- Section B: per-eigenvalue Coleman-Weinberg stationarity gives
  `u = sqrt(e) * mu` for every eigenvalue, forcing `e_1 = e_2 = e_3`
  and hence `|b|/a = 0` (Koide `Q = 1/3`, not `2/3`).
- Section C: Gaussian max-entropy on `(a, b_R, b_I)` at fixed Frobenius
  gives `<a^2>/<|b|^2> = 1`, not `2`. The factor-2 mismatch is exact
  and persists at any temperature.
- Section D: uniform max-entropy on the 3-eigenvalue simplex with
  fixed mean gives `lambda_0 = lambda_1 = lambda_2`, i.e. `Q = 1/3`.
  The continuous-distribution `CV = 1` (exponential max-entropy) is
  not realizable on 3-point support from a mean constraint alone.

Each fail-case is now a symbolic identity with sympy, so the no-go
boundary on which this note rests is auditable and the safe boundary
stated by the original audit ("these four attempted physical
mechanisms do not currently close the A1 bridge") is now backed by an
executable runner.

The runner does **not** supply the missing physical bridge; it only
makes the four failure calculations executable.

## 6. Audit dependency-graph anchors (internal-chain side)

The auditor's `notes_for_re_audit_if_any` named this row's missing
dependency edges as:

- `review_branch_KOIDE_FROBENIUS_ISOTYPE_SPLIT_UNIQUENESS_not_registered_one_hop_dependency`
- `review_branch_KOIDE_KAPPA_BLOCK_TOTAL_FROBENIUS_MEASURE_not_registered_one_hop_dependency`
- `review_branch_KOIDE_Q_DELTA_CLOSURE_PACKAGE_README_not_registered_one_hop_dependency`
- `runner_for_WJ_Coleman_Weinberg_max_entropy_CV_attempts_not_registered`

Three of these supplier notes already exist on disk in this branch
and target the **internal-chain** side of the A1 closure problem
(i.e. the retained block-total Frobenius extremization theorem on
`Herm_circ(3)`, not the open physical source-law). Section 5 above
adds the runner anchor; this section adds the supplier-note anchors:

1. `docs/KOIDE_KAPPA_BLOCK_TOTAL_FROBENIUS_MEASURE_THEOREM_NOTE_2026-04-19.md`
   — exhibits the block-total Frobenius functional
   `E_I(H) = ||pi_I(H)||_F^2` on `Herm_circ(3)` and proves its
   equal-weight extremum at fixed `E_+ + E_perp` is exactly
   `E_+ = E_perp <=> kappa = 2 <=> A1`. Names `d = 3` uniqueness via
   the multiplicity pattern (1 trivial + 1 doublet).
2. `docs/KOIDE_KAPPA_BLOCK_TOTAL_FROBENIUS_ALGEBRAIC_NARROW_THEOREM_NOTE_2026-05-10.md`
   — narrow algebraic companion to (1) with the AM-GM step on the
   log-functional written as a stand-alone identity at `d = 3`.
3. `docs/KOIDE_FROBENIUS_ISOTYPE_SPLIT_UNIQUENESS_NOTE_2026-04-21.md`
   — uniqueness of the isotypic split `pi_+` vs `pi_perp` on
   `Herm_circ(3)`; no other Frobenius-orthogonal splitting, so the
   choice of `E_+(H) + E_perp(H)` is canonical given the isotype
   structure of the carrier.
4. `docs/KOIDE_Q_DELTA_CLOSURE_PACKAGE_README_2026-04-21.md`
   — package README for the operator-side `Q`-delta closure; lists
   the review-branch theorems this note referenced in its
   internal-chain framing.

The runner's Section E records these supplier notes as on-disk facts
and explicitly disavows status promotion in E.6.

These four anchors close the **internal-chain** half of the audit gap
(the block-total Frobenius extremization theorem, the canonical
isotype split, and the operator-side Q-delta closure package are all
now reachable from this row in the citation graph). They do **not**
close the **physical-source** half (the open gate is still: why does
the charged-lepton physical packet extremize `S_block` rather than
another natural functional). The runner's Sections A-D verify that
the four standard QFT/statistical-mechanics functionals named in this
note do not select the same extremum as `S_block`, which is what the
original audit's safe-boundary statement asserted.

This section is graph-bookkeeping only and does not promote any
audit_status; the independent audit lane retains sole responsibility
for setting `effective_status`.
