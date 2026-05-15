# Koide Lightcone Primitive — Operator-Level Equivalent of NSC

**Date:** 2026-05-10

**Type:** positive_theorem
**Claim scope:** for any positive real 3-vector `v = (v_1, v_2, v_3) ∈ R^3_{>0}`,
if `v` is the eigenvalue vector of a Z_3-equivariant Hermitian operator
`A` on a 3-dimensional space (i.e., `A = a I + b R + c R²` where R is the
cyclic shift permutation matrix and `c = b*` for real eigenvalues),
then the scalar condition `Q(v) = (Σ v_g²)/(Σ v_g)² = 2/3` holds if
and only if the **Lightcone Condition** holds on the coefficients
`(a, b, c)`:

```text
   a²  =  |b|²  +  |c|²       (LCC)
```

Equivalently (using `c = b*`): `a² = 2|b|²`, i.e., `|b|/a = 1/√2`.
**Status authority:** independent audit lane only. This source note
does not set or predict an audit outcome; later status is generated
by the audit pipeline after independent review.

This is a **pure algebraic equivalence** identifying the
(NSC, Foot 45°, Koide Q = 2/3) family of equivalent conditions with
an **operator-level coefficient identity** in the canonical
Z_3-equivariant basis `{I, R, R²}`. It is **not** a derivation of
Q = 2/3 from any framework. It REDUCES the Koide closure problem
from "derive Q = 2/3 for the scalar mass spectrum" to "derive
a² = |b|² + |c|² for the lepton mass-square-root operator's
coefficients in the Z_3-equivariant basis."

The form `a² = |b|² + |c|²` is the **null cone** in a (1, 2)-signature
quadratic form on the operator coefficients. The candidate
structural mechanism (per cross-domain literature survey, §7) is
Connes-style spectral-triple grading on a Cl(3)/Z³ Frobenius finite
algebra: the Z_3 character grading IS the spectral-triple γ-grading,
and `Tr(γ √(D†D))` is the canonical spectral object whose vanishing
realizes LCC.

**Primary runner:** [`scripts/frontier_koide_lightcone_primitive.py`](./../scripts/frontier_koide_lightcone_primitive.py)

**Lane:** 6 — charged-lepton mass workstream context only; closure
not claimed.

---

## 1. Theorem statement

**Theorem (Koide Lightcone Primitive — LCC equivalence).**

Let `A` be a 3×3 Hermitian operator that commutes with the cyclic
permutation `R` defined by

```text
   R  :=  [[0, 0, 1],
           [1, 0, 0],
           [0, 1, 0]]                                                  (1.1)
```

(R is the order-3 cyclic shift, R³ = I). By Z_3-equivariance, A has
the form

```text
   A  =  a I  +  b R  +  c R²                                          (1.2)
```

for unique complex coefficients `(a, b, c)`. By Hermiticity of A
(and using `R^† = R^{-1} = R²`), we have **c = b*** (complex
conjugate).

Let `v = (v_0, v_1, v_2) ∈ R^3_{>0}` be the eigenvalue vector of A.
Then

```text
   Q(v) = (Σ_g v_g²)/(Σ_g v_g)² = 2/3       (Koide)
   ⟺
   a²  =  |b|²  +  |c|²                      (LCC)                    (1.3)
```

Since `c = b*` implies `|b| = |c|`, LCC reduces to `a² = 2|b|²`,
equivalently `|b|/a = 1/√2`.

## 2. Proof

### 2.1 Eigenvalues of a Z_3-equivariant operator

A 3×3 matrix that commutes with R is diagonal in the basis of R's
eigenvectors, the **Z_3 characters** {ψ_0, ψ_ω, ψ_{ω²}} where
ψ_k has components `(1, ω^k, ω^{2k})/√3` with ω = e^{2πi/3}.

R acts as multiplication by ω^k on ψ_k. Therefore A acts as

```text
   A ψ_k  =  (a + b ω^k + c ω^{2k}) ψ_k                                (2.1.1)
```

The eigenvalues of A are

```text
   λ_k  =  a + b ω^k + c ω^{2k}        k = 0, 1, 2                    (2.1.2)
```

These are real iff `c = b*` (a standard fact from Z_n-Fourier analysis
of Hermitian operators).

For Hermitian A, label the eigenvalues `v_k := λ_k`. The eigenvalue
vector `v = (v_0, v_1, v_2)` is real, and is the discrete inverse
Fourier transform of `(a, b, c)`:

```text
   v_g  =  √3 × (Fourier inverse of (a, b, c) at g)                    (2.1.3)
```

Direct computation:

```text
   v_g  =  a + b ω^g + c ω^{-g}  =  a + 2 Re(b ω^g)                    (2.1.4)
```

writing `b = β e^{iφ}` with `β ≥ 0` real,

```text
   v_g  =  a + 2β cos(φ + 2πg/3)                                       (2.1.5)
```

### 2.2 Sum and sum-of-squares from the parametrization

By orthogonality of cosines on the cyclic group Z_3 (sum of cosines
at 120° intervals = 0):

```text
   Σ_g cos(φ + 2πg/3)  =  0                                            (2.2.1)
```

Hence

```text
   Σ_g v_g  =  3a + 2β · 0  =  3a                                      (2.2.2)
```

For sum of squares, expand `v_g² = a² + 4aβ cos(...) + 4β² cos²(...)`:

```text
   Σ_g v_g²  =  3a² + 4aβ · 0 + 4β² · (3/2)
              =  3a² + 6β²                                              (2.2.3)
```

using `Σ_g cos²(φ + 2πg/3) = 3/2` (standard sum of squared cosines
at equispaced angles).

### 2.3 Koide ratio in the (a, β) parametrization

```text
   Q(v)  =  (Σ v_g²) / (Σ v_g)²  =  (3a² + 6β²) / 9a²
        =  1/3 + (2/3)(β/a)²                                            (2.3.1)
```

Setting `Q(v) = 2/3`:

```text
   1/3 + (2/3)(β/a)²  =  2/3
   (2/3)(β/a)²        =  1/3
   (β/a)²             =  1/2                                            (2.3.2)
```

i.e., **`β = a/√2`**, equivalently **`a² = 2β² = |b|² + |c|²`**
(since `|b| = |c| = β`).

This is LCC (1.3). ∎

### 2.4 Reverse direction

By symmetry of the steps in §2.3, LCC ⟹ Q = 2/3 is immediate:
starting from `(β/a)² = 1/2` and substituting into (2.3.1) gives
`Q(v) = 2/3`.

The equivalence Q = 2/3 ⟺ LCC therefore holds for any
Z_3-equivariant Hermitian A with the eigenvalue parametrization
(2.1.5).

## 3. Geometric / signature interpretation

The coefficient triple `(a, b, c)` with `c = b*` is equivalent to
the real triple `(a, Re(b), Im(b)) ∈ R³` (since `c = b*` is a real
constraint).

The Lightcone Condition `a² = |b|² + |c|² = 2|b|² = 2(Re(b)² + Im(b)²)`
is the **null cone** in the quadratic form

```text
   Q_L(a, x, y)  :=  a² - x² - y²                                       (3.1)
```

on R³ with signature (+, −, −) (one timelike, two spacelike), where
`x = √2 Re(b)` and `y = √2 Im(b)`.

This is the (1, 2)-signature Minkowski-like quadratic form. Koide
Q = 2/3 ⟺ the coefficient vector `(a, x, y)` is **lightlike**
under Q_L.

### 3.1 Connection to Foot's 45° angle

Foot 1994 wrote Q = 2/3 as the geometric condition that
`angle(v, (1,1,1)) = 45°` in R³ (component basis). The Lightcone
Primitive is the same condition stated in the OPERATOR coefficient
basis, where it takes the form of a null cone in a (1, 2)-signature
quadratic form.

In terms of the (a, β) parametrization: `cos(angle) = √(a²/(a² + 2β²))`.
At LCC (`β = a/√2`), `cos² = a²/(a² + a²) = 1/2`, so angle = 45°. ✓

## 4. Claim boundary

This note imports no measured lepton masses, no PDG values, no
fitted selector, and no literature numerical comparator. If a later
physics note applies the identity to charged-lepton square-root
masses, those masses are separate inputs for that later note. They
are not inputs to this algebraic equivalence theorem.

The Koide-NSC equivalence theorem in
`KOIDE_Q_TWO_THIRDS_Z3_CHARACTER_NORM_SPLIT_RECASTING_THEOREM_NOTE_2026-05-10.md`
shows that for any 3-vector v ∈ R^3_{>0}, Q = 2/3 ⟺ `|c_0|² = |c_1|² + |c_2|²`
where c_k are the discrete Fourier coefficients of v. This note
shows that **for the same v expressed as eigenvalues of a
Z_3-equivariant operator A**, the same condition translates to
LCC on A's coefficients `(a, b, c)`.

The two formulations are equivalent under the Z_3 Fourier transform
(direct vs inverse). NSC and LCC are the same condition on different
sides of the discrete Fourier duality.

## 5. Significance — what this REDUCES the closure problem to

Prior recasting (`KOIDE_Q_TWO_THIRDS_Z3_CHARACTER_NORM_SPLIT_RECASTING`)
identified that Koide closure on Cl(3)/Z³ would require deriving
the norm split `|c_0|² = |c_1|² + |c_2|²` for the mass-square-root
vector. This Lightcone Primitive sharpens that target by stating
it OPERATOR-LEVEL: derive `a² = |b|² + |c|²` for the lepton
mass-square-root operator's coefficients in the canonical
Z_3-equivariant basis.

The operator-level form is more amenable to derivation by
structural arguments:

- **Trace-zero condition on a graded operator:** if there exists a
  `Z_2` grading `Γ` on the 3-generation operator space such that
  `Tr(A Γ) = 0` is structurally forced, then a specific form of
  this constraint reduces to LCC.

- **Light-cone condition from emergent (1, 2)-signature:** if the
  framework's emergent time structure (per
  `ANOMALY_FORCES_TIME_THEOREM`) extends to a Lorentzian-type
  quadratic form on the Z_3-equivariant coefficient space, the
  lepton mass operator being "lightlike" in this space gives LCC.

- **Connes-style spectral-triple grading:** per
  `Chamseddine–Connes` 1996, the spectral action `Tr f(D/Λ)` on a
  finite spectral triple with γ-grading produces specific trace
  identities. If the framework's lepton sector is a finite spectral
  triple with the Z_3 character grading playing the role of γ,
  the LCC emerges as a `Tr(γ √(D†D)) = 0` identity.

These are research-level open derivation routes, not closures. The
Lightcone Primitive itself is a pure algebraic equivalence —
mathematically rigorous, framework-independent, and a precise
single target for any future derivation attempt.

## 6. What this theorem does NOT establish

- A derivation of Koide Q = 2/3 from any framework
- A Lane 6 closure
- A physical Cl(3)/Z³ mechanism for LCC
- A prediction of m_e, m_μ, m_τ individually
- A falsification of #912, #1018, #1026, #1048
- Anything not entailed by the algebraic equivalence in §1-2

## 7. Cross-domain mathematical context (non-load-bearing)

Cross-domain literature survey identified candidate mechanisms that
could structurally force LCC. The strongest candidates:

**Connes–Chamseddine spectral action (1996).** A finite spectral
triple `(A, H, D)` with grading `γ` produces the spectral action
`Tr f(D/Λ)`. The Z_3 character difference operator
`Γ_χ = 2J/3 − I` (with eigenvalue +1 on Z_3-singlet, −1 on
Z_3-doublet) plays the role of γ on a Z_3-graded finite spectral
triple. The trace identity `Tr(γ √(D†D)) = 0` is exactly LCC
expressed on the eigenvalue spectrum of `√(D†D) = √M`.

**Brannen circulant analysis (`MASSES2.pdf`).** Brannen's circulant
parametrization of the lepton mass-square-root vector uses a phase
δ = 2/9 (radian fraction) that matches the framework's retained
`KOIDE_Q23_DELTA_LINKING_RELATION_THEOREM_NOTE_2026-04-20`. The
circulant form `M = a I + b R + c R²` is exactly the
Z_3-equivariant form of (1.2).

**Frobenius algebra / 2D TFT (Teleman lectures).** A commutative
Frobenius algebra on `C[Z_3]` with trace form `ε(g) = δ_{g,e}` has
handle operator `H = 3 · P_singlet`. For square-root states (PSD
lifts of a state), `Tr(√ρ · (H − I)) = 0` reproduces Γ_χ. This
provides a 2D-TFT realization of LCC.

**Sumino isosceles right triangle (2009).** The 45° angle in Foot's
geometric form corresponds to an isosceles right triangle in
mass-square-root space. Sumino's gauge-radiative mechanism realizes
this triangle via cancellation between gauge corrections; LCC is
the abstract operator-level encoding of the same triangle.

These connections are non-load-bearing on the proof in §2; they
constitute the candidate derivation routes for future research.

## 8. Falsifiers

The algebraic equivalence (Q = 2/3 ⟺ LCC) is mathematically rigorous
and falsified only by:

1. A computational error in the Z_3-Fourier transform or the
   parametrization `v_g = a + 2β cos(φ + 2πg/3)` (verified by the
   runner symbolically).
2. A redefinition of Koide Q that differs from `(Σ m)/(Σ √m)²`.
3. A redefinition of Z_3-equivariant operator that excludes the
   `aI + bR + cR²` parametrization.

The CONNECTION to Lane 6 is falsified if LCC is shown to be
underivable from Cl(3)/Z³ alone — but that's a closure question,
not a falsifier of this algebraic equivalence.

## 9. Non-load-bearing Lane 6 context

This theorem is graph-disconnected from the Lane 6 physics chain.
The following files are useful context but none are load-bearing
dependencies of the proof above:

- `CKM_KOIDE_CROSS_SECTOR_Z3_CLOSURE_THEOREM_NOTE_2026-04-25.md`
- `Z3_CHARACTER_ISOMORPHISM_COLOR_GENERATION_OPEN_GATE_NOTE_2026-05-10.md`
- `KOIDE_Q_TWO_THIRDS_Z3_CHARACTER_NORM_SPLIT_RECASTING_THEOREM_NOTE_2026-05-10.md`
- `CHARGED_LEPTON_Y_TAU_WARD_COMBINED_NO_GO_NOTE_2026-05-10.md`
- `LEPTON_BLOCK_D12_PRIME_MATCHING_NO_GO_NOTE_2026-05-10.md`
- `LEPTON_BLOCK_SCALAR_SINGLET_COMPOSITE_UNIQUENESS_D17_PRIME_THEOREM_NOTE_2026-05-10.md`
- `LEPTON_BLOCK_TREE_LEVEL_EXCHANGE_D16_PRIME_THEOREM_NOTE_2026-05-10.md`
- `KOIDE_Q_DELTA_LINKING_RELATION_THEOREM_NOTE_2026-04-20.md` (retained δ = 2/9)
- `ANOMALY_FORCES_TIME_THEOREM_NOTE.md` (emergent (1, 3) signature)

The possible physics chain remains open: Lane 6 would need a
framework-derived lepton mass operator and a derivation of LCC for
that operator before this algebraic recasting could contribute to
a Koide closure.

## 10. Literature context

Non-load-bearing references for the cross-domain math:

- **Foot 1994**: G. Foot, "A note on Koide's lepton mass relation,"
  Mod. Phys. Lett. A 9 (1994) 437 — 45° geometric form
- **Chamseddine–Connes 1996**: A. Chamseddine, A. Connes, "The
  spectral action principle," hep-th/9606001 — finite spectral
  triples with γ-grading
- **Brannen `MASSES2.pdf`**: circulant + phase 2/9
- **Sumino 2009**: arXiv:0903.3640 — isosceles right triangle form
- **Teleman**: Berkeley lectures on 2D TFT — Frobenius algebra handle
  operator
- **Schur orthogonality**: Wigner-Eckart on finite groups —
  algebraic engine for character-graded trace identities

## 11. Boundary

This is a NARROW POSITIVE ALGEBRAIC EQUIVALENCE THEOREM on the
operator-coefficient form of Koide's relation. It establishes
mathematically that:

> Q = 2/3 (scalar Koide on eigenvalues) ⟺ a² = |b|² + |c|² (LCC on
> Z_3-equivariant operator coefficients).

It does NOT close Koide. It provides a precise OPERATOR-LEVEL target
(LCC = null cone in (1, 2)-signature) for any future structural
derivation, complementing the eigenvalue-level NSC target from the
earlier recasting theorem. Together NSC and LCC give Koide a
DUAL-FORMULATION:

- **NSC** (eigenvalue side): `|c_0|² = |c_1|² + |c_2|²` for
  Fourier coefficients of the eigenvalue vector
- **LCC** (operator side): `a² = |b|² + |c|²` for coefficients in
  the Z_3-equivariant operator basis

The two are exchanged by the discrete Fourier transform.

A class-A runner verifies the algebraic equivalence symbolically
(`scripts/frontier_koide_lightcone_primitive.py`).
