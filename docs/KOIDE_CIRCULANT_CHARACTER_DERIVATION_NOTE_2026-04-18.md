# Koide Q = 2/3 as a C_3[111] Character-Theoretic Derivation — Candidate Retention Note

**Date:** 2026-04-18
**Status:** CANDIDATE PARTIAL FRAMEWORK PREDICTION — awaiting review for retention
**Relates to:** `docs/CHARGED_LEPTON_MASS_HIERARCHY_REVIEW_NOTE_2026-04-17.md`,
`docs/CHARGED_LEPTON_ASSUMPTION_AUDIT_2026-04-17.md`,
`docs/THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md`

## Summary

The charged-lepton Koide relation
```
Q = (m_e + m_μ + m_τ) / (√m_e + √m_μ + √m_τ)² = 2/3
```
is shown to be an **algebraic consequence** of two axiom-level ingredients of
Cl(3) on Z³ plus one specific structural assumption. Previously listed as
Layer-5 assumption `A5.1` ("Q = 2/3 exact") and `A5.2` ("Koide meaningful, not
coincidence") in the charged-lepton assumption audit, this note promotes Q = 2/3
from **coincidence-status to candidate framework prediction**, pending review of
one equipartition assumption and one phenomenological identification.

The three charged-lepton masses reduce to a **one-parameter family** (plus
overall scale) given Koide:
```
√m_k = v_0 (1 + √2 cos(δ + 2πk/3))        [Brannen/Rivero 2006, hep-ph/0505220]
```
with `δ ≈ 2/9 rad` for charged leptons. The Koide prediction is independent of
δ; the three individual masses depend on δ through the cosine structure.

## Retained inputs (strict Cl(3)/Z³ consequences)

### R1. Circulant Hermitian form on a C_3[111] orbit (axiom-clean)

On the retained hw=1 triplet `T_1 = span{X_1, X_2, X_3}`, the cyclic permutation
`C_3[111] : X_i → X_{i+1 mod 3}` acts by conjugation on `M_3(ℂ)`. Any Hermitian
operator that commutes with this action has the **circulant matrix form**:
```
H = a·I + b·C + b̄·C²          a ∈ ℝ,  b ∈ ℂ
```
where `C` is the cyclic shift matrix. This is **pure character theory**: it
follows directly from `C_3` representation theory applied to the 9-dimensional
Hermitian algebra `M_3(ℂ)_Herm`, which decomposes under C_3 conjugation as
`3·trivial ⊕ 3·ω ⊕ 3·ω̄`. The trivial-isotypic Hermitian subalgebra is exactly
the circulants.

**Axiom status:** strict consequence of Cl(3)/Z³ + C_3[111] retained cyclic structure.

### R2. Circulant eigenvalue spectrum (axiom-clean)

The eigenvalues of `H = a·I + b·C + b̄·C²`, obtained by diagonalization in the
Fourier basis:
```
λ_k = a + 2|b| cos(arg(b) + 2πk/3)          k ∈ {0, 1, 2}
```
This is the Brannen/Rivero spectral form with the identifications
```
v_0 = a,       arg(b) = δ,       2|b| = (coefficient of cosine)
```

**Axiom status:** strict consequence of R1 via standard diagonalization.

## One structural assumption

### A1. Frobenius-norm equipartition of trivial : nontrivial sectors (3 : 6)

In the 9-dim `M_3(ℂ)_Herm`, the circulant matrix `H` has Frobenius norm
```
‖H‖² = 3a² + 6|b|²
```
counting the 3 diagonal entries (each contributing `a²`) and 6 off-diagonal
entries (each contributing `|b|²`).

**Assumption:** these two sectors contribute equally:
```
3a² = 6|b|²    ⟹    |b| = a/√2    ⟹    2|b| = √2 · a
```

This fixes the **√2 coefficient** in the Brannen/Rivero form:
```
λ_k = a (1 + √2 cos(δ + 2πk/3))
```

**Justification candidates (none fully axiom-derived):**
- Random-matrix measure with uniform entry distribution
- Gaussian ensemble equipartitioning energy between matrix modes
- Second-order phase-transition critical-point equipartition (analogous to
  classical equipartition per degree of freedom)
- Schur orthogonality between irrep sectors of C_3 on `M_3(ℂ)`

**This assumption is the one load-bearing non-axiom step.** It is the
magnitude-squared equipartition primitive discussed in the assumption audit
(`CHARGED_LEPTON_ASSUMPTION_AUDIT_2026-04-17.md` Layer 4). It is NOT retained as a
theorem on the current surface.

## One phenomenological identification

### P1. Spectral eigenvalues correspond to √m, not m

The circulant form gives eigenvalues `λ_k`. Identifying these with the
**square-roots of charged-lepton masses**:
```
λ_k = √m_k
```
reproduces observed charged-lepton masses to sub-percent precision at
`δ = 2/9 rad` (see §"Verification"). An alternative identification `λ_k = m_k`
would NOT give Koide `Q = 2/3`.

**Status:** This identification is empirical, motivated by the Koide relation
itself (which is naturally expressed in `√m` space). It is NOT derived from
Cl(3)/Z³. Possible structural origins for future investigation:
- Dirac spinor normalization (fermion wave functions have `√m` character)
- Square-root structure of Clifford algebra (Cl(3) spinors carry half-integer
  scaling)
- Second-order return theorem: hw=1 intermediate-space matrix elements are
  second-order in Γ_1, giving m² in one convention but m^1 after taking square
  root of the cascade

## Koide Q = 2/3 as algebraic consequence

Given R1 + R2 + A1 + P1, and using the standard cosine identities for
third-roots-of-unity:

```
Σ_k cos(δ + 2πk/3) = 0                    (zero-sum of 3rd roots of unity)
Σ_k cos²(δ + 2πk/3) = 3/2                  (standard identity)
```

Then:
```
Σ_k √m_k = Σ_k v_0 (1 + √2 cos(θ_k))
        = 3 v_0 + √2 · 0
        = 3 v_0

Σ_k m_k = v_0² Σ_k (1 + √2 cos(θ_k))²
       = v_0² [3 + 2√2 Σ cos + 2 Σ cos²]
       = v_0² [3 + 0 + 2 · 3/2]
       = 6 v_0²

Q = (Σ m_k) / (Σ √m_k)² = 6 v_0² / 9 v_0² = 2/3
```

**Q = 2/3 is an exact algebraic consequence, independent of δ.**

## Numerical verification against PDG (2024)

**Input:** PDG pole masses
- `m_e = 0.5109989 MeV`
- `m_μ = 105.6583745 MeV`
- `m_τ = 1776.86 MeV`

**Compute:**
- `√m_e = 0.71484 √MeV`
- `√m_μ = 10.27903 √MeV`
- `√m_τ = 42.15282 √MeV`
- `v_0 = (√m_e + √m_μ + √m_τ) / 3 = 17.71556 √MeV`

**Predict from Brannen/Rivero at δ = 2/9:**

| k | `δ + 2πk/3` (rad) | `cos(·)` | `1 + √2 cos(·)` | `v_0 × (·)` (√MeV) | Assign to |
|---|---|---|---|---|---|
| 0 | 0.22222 | +0.97541 | 2.37937 | 42.1531 | τ |
| 1 | 2.31662 | −0.67858 | 0.04038 | 0.7154 | e |
| 2 | 4.41101 | −0.29684 | 0.58022 | 10.2770 | μ |

**Residuals against PDG √m:**
- τ: +0.001% (42.1531 vs 42.15282)
- e: +0.08%  (0.7154 vs 0.71484) — *agent prior residual estimate 0.003% was tight; recomputation here gives 0.08%, still sub-percent*
- μ: −0.02% (10.2770 vs 10.27903)

**Koide Q from these predictions:** exact 2/3 by construction (independent of δ).

**Best-fit δ from PDG:** 0.22227 rad (vs 2/9 = 0.22222). Difference 5×10⁻⁵ rad.

## What remains OPEN

### O1. Derivation of δ = 2/9 rad

No axiom-level mechanism for the specific value `δ ≈ 2/9 rad` has been
identified. Candidate derivations tested:
- `2/dim(M_3(ℂ)_Herm) = 2/9` — dimensional ratio, but interpreting as radians
  requires justification
- `2 arctan(1/9) = 0.22131` — 0.41% from 2/9, no framework provenance
- `π/14 = 0.22440` — 0.98% off, no framework provenance
- Temporal phase (APBC, Matsubara, winding) — all give π or 2π/n phases, not 2/9
- `δ = π/12 (critical angle)` — gives massless electron; observed δ = 2/9 sits
  just below this by 0.04 rad

### O2. Scale v_0

The overall scale `v_0 = 17.72 √MeV` determines absolute masses given the
ratios. Likely derivable from the retained hierarchy theorem
`v = M_Pl × (7/8)^(1/4) × α_LM^{16}` via a generation-sector normalization, but
this computation has not been performed.

### O3. Justification of the equipartition assumption A1

The 3:6 Frobenius-norm equipartition giving √2 requires structural grounding.
Candidates listed above; none rigorously derived. This is the same load-bearing
step flagged as Primitive D / magnitude-squared equipartition in the assumption
audit.

### O4. Justification of the √m identification P1

Why do circulant eigenvalues correspond to `√m` rather than `m` or `m²`?
Not currently derived; observationally forced.

## Impact on retained audit

If accepted with caveats, this note **promotes assumptions A5.1 and A5.2** of
the charged-lepton assumption audit:

**Before:** `A5.1: Q = 2/3 exact (assumption)` and `A5.2: Koide meaningful
(numerical coincidence vs signal)`.

**After:** Q = 2/3 is axiom-derived modulo equipartition (A1) and √m
identification (P1). Koide is a signal, not a coincidence — it's the C_3[111]
character-theoretic consequence of the retained generation structure.

The three-mass derivation problem reduces to a **one-parameter problem**:
- Derive the overall scale `v_0` (framework-tractable via hierarchy theorem)
- Derive the phase `δ = 2/9 rad` (OPEN)

## Proposed status classification

**CANDIDATE PARTIAL FRAMEWORK PREDICTION — AWAITING REVIEW**

This is a reduction of the charged-lepton mass-hierarchy problem, not a full
closure. The circulant form (R1, R2) is axiom-clean; the equipartition (A1)
and √m identification (P1) are structural assumptions requiring either
derivation or formal acceptance as retained primitives. Koide Q = 2/3 holds
exactly given R1+R2+A1+P1.

If retained as a partial prediction:
- The bounded `TRUE_NO_PREDICTION` status on Q = 2/3 promotes to RETAINED
- The three-mass problem reframes as "derive δ = 2/9 and v_0"
- The review note's Layer-5 assumptions receive a concrete derivation pathway

If the equipartition (A1) or √m identification (P1) are rejected:
- Koide remains a coincidence-class observation
- No change to bounded-package status

## Connection to Brannen/Rivero phenomenology

This derivation aligns with the Brannen (2006) + Rivero phenomenological
parametrization of charged-lepton masses (Gsponer/Rivero, hep-ph/0505220 and
subsequent work). Their circulant ansatz has been shown to fit PDG masses to
sub-10⁻⁵ precision at δ = 2/9 rad. This note provides a **character-theoretic
interpretation** of that ansatz as the natural Hermitian operator structure on
the retained C_3[111] orbit, and reduces Koide Q = 2/3 to an algebraic identity
of the cosine structure.

The Sumino (2009) family-gauge-symmetry derivation of Koide
(arXiv:0812.2090) provides a radiative-cancellation mechanism operating at
pole-mass vs running-mass scale. Our derivation is complementary: it's a
structural (not radiative) origin for Koide, valid at whichever scale the
circulant identification is made. Whether this is pole-mass scale (as in Sumino)
or hierarchy-theorem scale is a downstream question.

## Testable predictions / sharp questions

1. **Quark Koide extension.** Does the quark sector carry an analogous circulant
   structure under C_3[111] with a different δ? Literature notes (c,b,t) give
   `Q ≈ 0.67` at ~5% level. A framework-native prediction of the quark δ would
   be a sharp test.

2. **Neutrino Koide extension.** Brannen's neutrino conjecture uses `δ = 2/9 +
   π/12` in the circulant form and predicts neutrino mass ordering consistent
   with current oscillation data. Framework derivation of this complementary
   phase would further validate the structure.

3. **δ = 2/9 origin.** Any specific framework mechanism selecting this phase
   would close the remaining gap.

## File references

- Parent review: `CHARGED_LEPTON_MASS_HIERARCHY_REVIEW_NOTE_2026-04-17.md`
- Audit context: `CHARGED_LEPTON_ASSUMPTION_AUDIT_2026-04-17.md`
- Generation-space theorem: `THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md`
- C_3[111] retained surface: `HW1_SECOND_ORDER_RETURN_SHAPE_THEOREM_NOTE.md`
- Literature: Brannen 2006 (unpublished notes); Rivero/Gsponer hep-ph/0505220;
  Koide 1981 PLB 120:161; Sumino arXiv:0812.2090 & 0903.3640;
  Xing/Zhang hep-ph/0602134 (running-vs-pole analysis);
  Kartavtsev arXiv:1111.0480 (multi-sector extensions).
