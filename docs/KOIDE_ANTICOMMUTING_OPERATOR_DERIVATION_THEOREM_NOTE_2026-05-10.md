# Koide Anti-Commuting Operator → LCC Derivation Theorem

**Date:** 2026-05-10

**Type:** positive_theorem
**Claim scope:** for any 3-dimensional Hermitian operator H on R^3 that
anti-commutes with the Z_3 character grading operator
`Γ_χ = 2J/3 - I` (where J is the rank-1 all-ones matrix), and any
eigenvector `v ∈ R^3` of H with non-zero eigenvalue, the expectation
value `<v|Γ_χ|v>` vanishes identically. Equivalently, v satisfies the
Lightcone Condition (LCC) `a² = |b|² + |c|²` on the Z_3-equivariant
coefficient decomposition, equivalently the Koide ratio
`Q(v) = (Σv²)/(Σv)² = 2/3`.
**Status authority:** independent audit lane only. This source note
does not set or predict an audit outcome; later status is generated
by the audit pipeline after independent review.

This is a **pure algebraic derivation theorem** identifying a
structural mechanism by which any framework supplying a specific
operator content (Hermitian H anti-commuting with Γ_χ, with the
lepton mass-square-root vector as an eigenvector of nonzero
eigenvalue) automatically produces the Koide relation `Q = 2/3`.

It sharpens the Koide closure question one further level: from
"derive LCC on the mass-square-root operator coefficients" to
"derive the existence of an Hermitian anti-commuting operator H
with v as eigenvector."

**Primary runner:** [`scripts/frontier_koide_anticommuting_operator_derivation.py`](./../scripts/frontier_koide_anticommuting_operator_derivation.py)

**Lane:** 6 — charged-lepton mass workstream context only; closure
not claimed.

---

## 1. Theorem statement

**Theorem (Anti-Commuting Operator → LCC).**

Let:
- `Γ_χ := (2/3) J − I` where `J ∈ R^{3×3}` is the rank-1 all-ones
  matrix (Γ_χ has eigenvalues +1 on the (1,1,1) singlet direction
  and −1 on the orthogonal 2-plane doublet).
- `H ∈ R^{3×3}` be Hermitian (real symmetric) with `{H, Γ_χ} = 0`
  (anti-commutation).
- `v ∈ R^3` be an eigenvector of H with eigenvalue `λ ≠ 0`.

Then:

```text
   <v | Γ_χ | v>  =  0                                                  (1.1)
```

Equivalently, the Z_3-character Fourier coefficients
`c_k = (1/√3) Σ_g ω^{kg} v_g` of v satisfy

```text
   |c_0|²  =  |c_1|²  +  |c_2|²       (NSC)                            (1.2)
```

and equivalently the Koide ratio of v satisfies

```text
   Q(v)  :=  (Σ_g v_g²) / (Σ_g v_g)²  =  2/3                          (1.3)
```

## 2. Proof

The proof is a standard application of the anti-commutation
relation to a Hermitian eigenvalue problem.

### 2.1 Anti-commutation gives a sign flip

Since `{H, Γ_χ} = 0`, we have

```text
   H Γ_χ  =  -Γ_χ H                                                    (2.1.1)
```

### 2.2 Conjugating the expectation value

For `v` an eigenvector of `H` with `H v = λ v` (and `λ ∈ R` since
H Hermitian):

```text
   λ² <v | Γ_χ | v>  =  <v | H² Γ_χ | v>                              (2.2.1)
```

(using `H v = λ v` to factor `λ²` out, treating H as Hermitian
acting on both sides).

Now using (2.1.1) twice:

```text
   H² Γ_χ  =  H (H Γ_χ)  =  H (-Γ_χ H)  =  -(HΓ_χ)H  =  -(-Γ_χH)H  =  Γ_χ H²
```

Wait — let me redo this more carefully. H² Γ_χ vs Γ_χ H²:

```text
   H² Γ_χ  =  H · (H Γ_χ)  =  H · (-Γ_χ H)  =  -H Γ_χ H
   H² Γ_χ  =  -H Γ_χ H  =  -(H Γ_χ) H  =  -(-Γ_χ H) H  =  Γ_χ H²
```

So `[H², Γ_χ] = 0`, i.e., `H²` and `Γ_χ` commute. Therefore
`H² Γ_χ = Γ_χ H²`.

Now back to (2.2.1):

```text
   λ² <v | Γ_χ | v>  =  <v | H² Γ_χ | v>  =  <v | Γ_χ H² | v>          (2.2.2)
                    =  <H v | Γ_χ | H v>  =  <λv | Γ_χ | λv>
                    =  λ² <v | Γ_χ | v>                                (2.2.3)
```

This is a tautology so far. We need a different approach.

### 2.3 The correct argument

Consider <v | H Γ_χ | v> two ways:

**Way 1:** evaluate H on v on the left:
```text
   <v | H Γ_χ | v>  =  <H v | Γ_χ | v>  =  λ <v | Γ_χ | v>            (2.3.1)
```

**Way 2:** use anti-commutation `H Γ_χ = -Γ_χ H`:
```text
   <v | H Γ_χ | v>  =  -<v | Γ_χ H | v>  =  -<v | Γ_χ | H v>
                    =  -λ <v | Γ_χ | v>                                (2.3.2)
```

Equating (2.3.1) and (2.3.2):

```text
   λ <v | Γ_χ | v>  =  -λ <v | Γ_χ | v>                               (2.3.3)
   2λ <v | Γ_χ | v>  =  0                                              (2.3.4)
```

Since `λ ≠ 0` (by hypothesis):

```text
   <v | Γ_χ | v>  =  0                                                 (2.3.5)
```

### 2.4 Equivalence to NSC and Koide Q = 2/3

The expectation value:

```text
   <v | Γ_χ | v>  =  v^T Γ_χ v  =  (2/3) v^T J v - v^T v
                  =  (2/3)(Σ v_g)² - Σ v_g²                            (2.4.1)
```

Setting this to zero:

```text
   (2/3)(Σ v_g)²  =  Σ v_g²                                            (2.4.2)
   3 Σ v_g²       =  2 (Σ v_g)²                                        (2.4.3)
```

which is exactly `Q(v) = 2/3`. By the earlier recasting theorem
(`KOIDE_Q_TWO_THIRDS_Z3_CHARACTER_NORM_SPLIT_RECASTING_THEOREM_NOTE_2026-05-10`),
this is equivalent to NSC: `|c_0|² = |c_1|² + |c_2|²`. ∎

## 3. Characterization of anti-commuting H

### 3.1 Explicit parametrization

For a real symmetric matrix H on R^3 to anti-commute with
`Γ_χ = (2/3) J - I`, expand the constraint `H Γ_χ + Γ_χ H = 0`:

```text
   (2/3)(H J + J H) - 2 H  =  0
   H J + J H  =  3 H                                                   (3.1.1)
```

Let `h := (1,1,1) H` (a 3-row vector) and `h' := H (1,1,1)^T` (a
3-column vector). Then `J H = (1,1,1)^T h` and
`H J = h' (1,1,1)`, both rank-1 matrices.

`(J H + H J)_{ij} = h_j + h'_i`, while
`(3 H)_{ij} = 3 H_{ij}`.

Setting these equal:

```text
   H_{ij}  =  (h_j + h'_i) / 3                                         (3.1.2)
```

Consistency: row sum of H must equal h'_i. From (3.1.2):
`Σ_j H_{ij} = (Σ_j h_j + 3 h'_i) / 3 = (h̄ + 3 h'_i) / 3`. For this
to equal h'_i, need `h̄ := Σ h_j = 0`. Similarly column sum gives
`Σ h'_i = 0`.

For Hermitian H (real symmetric), the additional constraint
`H = H^T` gives `(h_j + h'_i) = (h_i + h'_j)`, i.e.,
`h_j - h'_j = h_i - h'_i` for all i, j. This forces
`h - h' = constant × (1,1,1)`. Combined with `h̄ = h̄' = 0`, the
constant is 0, so `h = h'`.

**Result:** Hermitian anti-commuting H is parametrized by a single
3-vector h with `Σ h = 0`:

```text
   H  =  (1/3) (1⊗h + h⊗1)                                            (3.1.3)
```

The space of such h has 2 real dimensions (R^3 with Σh = 0).

### 3.2 Eigenstructure of H

For any such H, the singlet direction (1,1,1)/√3 is in the kernel:

```text
   H (1,1,1)^T  =  (1/3) (1⊗h + h⊗1) (1,1,1)^T
                 =  (1/3) [h_1 + h_2 + h_3 + 3 h⊗1 (1,1,1)^T / 3]
                 =  (1/3) [0 + h] = h/3
```

Hmm, that's not zero. Let me recompute.

`H (1,1,1)^T`: applying H to the all-ones vector.
`H_{ij} = (h_j + h'_i)/3`. With h' = h:
`(H · 1)_i = Σ_j (h_j + h_i)/3 = (Σ_j h_j + 3 h_i)/3 = (h̄ + 3 h_i)/3 = h_i`
(using h̄ = 0).

So `H (1,1,1)^T = h`. So the all-ones vector is NOT an eigenvector
of H (unless h is proportional to (1,1,1), but `Σh = 0` rules that
out).

The eigenvectors of H are different from the singlet/doublet
decomposition under Γ_χ. This is exactly the property needed —
H "mixes" the singlet and doublet subspaces, which is what
anti-commutation with Γ_χ requires.

For a specific example: h = (1, -1, 0) (Σh = 0).

```text
   H  =  (1/3) [[2, 0, 1], [0, -2, -1], [1, -1, 0]]
```

Eigenvalues (computed sympy): {-√6/3, 0, +√6/3}.

The eigenvector with λ = 0 has `<v | Γ_χ | v> ≠ 0` (so doesn't give
LCC by this mechanism).

The eigenvectors with λ = ±√6/3 have `<v | Γ_χ | v> = 0` (verified
symbolically — see runner Part 5).

So this specific h gives a 2-dim family of v vectors (the two
nonzero-eigenvalue eigenvectors of H) that satisfy LCC / Koide.

### 3.3 General h gives a 2-dim family of Koide-satisfying v

For any choice of h with `Σ h = 0` and `h ≠ 0`, the operator H of
(3.1.3) has eigenvalues `{−λ, 0, +λ}` for some real `λ > 0`. The
two nonzero-eigenvalue eigenvectors are real and orthogonal to the
zero eigenvector. By Theorem 1.1, both eigenvectors satisfy
LCC / NSC / Koide Q = 2/3.

As h varies over R^3 with `Σh = 0` (a 2-parameter family), the
λ ≠ 0 eigenvectors of H trace out the Koide cone in R^3.

## 4. What this sharpens

Prior structural targets:

| Level | Target | Notes |
|---|---|---|
| Eigenvalue | Q = 2/3 on (v_e, v_μ, v_τ) | Scalar Koide |
| Eigenvalue (Fourier) | NSC: \|c_0\|² = \|c_1\|² + \|c_2\|² | Recasting theorem #1069 |
| Operator (Z_3-equiv) | LCC: a² = \|b\|² + \|c\|² | Lightcone primitive #1137 |
| **Operator (anti-comm)** | **Find Hermitian H ⊥ Γ_χ with v as eigenvector** | **This note** |

This further reduces the Koide closure problem to **finding a
specific Hermitian operator H on the 3-generation triplet**
that anti-commutes with the Z_3 character grading. The search
space is 2-dim (parametrized by `h` with `Σh = 0`), so the task
is finite and explicit.

## 5. What this theorem does NOT establish

- A derivation of Q = 2/3 from any framework
- A Lane 6 closure
- The existence of a specific framework-derived H of the required form
- A prediction of m_e, m_μ, m_τ individually
- A falsification of #912, #1018, #1026, #1048

It only establishes the algebraic implication:

> {H Hermitian on R^3, {H, Γ_χ} = 0, H v = λ v with λ ≠ 0}
>   ⟹  v satisfies Koide Q = 2/3

## 6. Candidate framework operators H

The 2-dim family of Hermitian anti-commuting H is parametrized by
`H = (1/3)(1⊗h + h⊗1)` with `Σh = 0`. Candidate framework operators
that could realize this form:

### 6.1 Cl(3) bivector action

Cl(3) has three bivectors `{γ_2γ_3, γ_3γ_1, γ_1γ_2}` forming an
su(2) algebra. Their action on the 3-generation triplet (per
CL3_TASTE_GENERATION_THEOREM) could produce an H of the required
form. Specifically: the antisymmetric "circulator" combination
`H = (R - R^T)/i` is the anti-Hermitian commutator part of the
3-cycle.

However, `(R - R^T)/i` has eigenvalues 0 on the singlet and ±√3
on the doublet (per the lightcone primitive note §2). Both
non-zero eigenvectors of this operator are in the doublet
subspace. They do NOT mix singlet and doublet, so this operator
COMMUTES with Γ_χ (not anti-commutes).

So Cl(3) bivectors alone do not provide the needed H. A more
elaborate construction is required.

### 6.2 Staggered Dirac taste operators

The staggered Dirac on Z³ acts on the 2³ = 8 taste cube. Specific
generators of taste shifts (which mix the 8 taste states across
generation candidates) might produce H of the required form when
restricted to the 3-generation subspace. This is research-level
open.

### 6.3 Spectral triple Dirac operator

In a Connes-style spectral triple with finite Hilbert space H,
the Dirac operator D acts on H ⊗ H_{KO} (with H_{KO} the
KO-dimension-encoded internal space). For a Cl(3)/Z³ spectral
triple with the Z_3 character grading playing the role of γ, the
Dirac D could anti-commute with γ automatically (a standard
property of Dirac operators in NCG). The off-diagonal blocks of
D mix singlet ↔ doublet, providing the anti-commuting H structure.

This is the most natural framework realization, per the cross-
domain literature review.

## 7. Falsifiers

The algebraic theorem is mathematically rigorous, falsified only
by a computational error in the anti-commutation derivation §2
(verified symbolically by the runner).

The CONNECTION to a framework derivation is falsified if no
Hermitian H of the required form exists in the Cl(3)/Z³ operator
content — but that's a closure question, not a falsifier of this
algebraic theorem.

## 8. Non-load-bearing Lane 6 context

This theorem is graph-disconnected from the Lane 6 physics chain.
The following files are useful context but none are load-bearing
dependencies of the proof above:

- `KOIDE_LIGHTCONE_PRIMITIVE_THEOREM_NOTE_2026-05-10.md` (the LCC
  formulation this sharpens)
- `KOIDE_Q_TWO_THIRDS_Z3_CHARACTER_NORM_SPLIT_RECASTING_THEOREM_NOTE_2026-05-10.md`
  (the NSC formulation)
- `CKM_KOIDE_CROSS_SECTOR_Z3_CLOSURE_THEOREM_NOTE_2026-04-25.md`
- `Z3_CHARACTER_ISOMORPHISM_COLOR_GENERATION_OPEN_GATE_NOTE_2026-05-10.md`
- `CHARGED_LEPTON_Y_TAU_WARD_COMBINED_NO_GO_NOTE_2026-05-10.md`
- `KOIDE_Q_DELTA_LINKING_RELATION_THEOREM_NOTE_2026-04-20.md`
- `ANOMALY_FORCES_TIME_THEOREM_NOTE.md`

The possible physics chain remains open: Lane 6 would need a
framework-derived anti-commuting operator H of the required form,
with the lepton mass-square-root vector as one of its non-zero-
eigenvalue eigenvectors, before this algebraic theorem could
contribute to a Koide closure.

## 9. Literature context

Anti-commuting operator arguments are standard in quantum
mechanics and representation theory:

- **Chirality / γ_5 in 4D QFT**: any Dirac operator D anti-commutes
  with γ_5. Eigenvectors of D with non-zero mass eigenvalue have
  zero chirality expectation. The Koide derivation here is the
  finite-dim analog of this 4D fact.
- **Connes' spectral triple**: a Z_2-graded spectral triple has
  Dirac D anti-commuting with γ. Spectral action principles
  exploit this routinely.
- **Witten index / supersymmetry**: in SUSY QM, the Hamiltonian
  anti-commutes with the Q-charge. Witten index = `Tr (-1)^F` is
  a topological invariant constrained by this.
- **Wigner-Eckart on finite groups**: trace identities on
  representations of finite groups follow from character
  orthogonality (Schur), which is the algebraic engine here.

The connection between the Z_3 character grading and a
Dirac-style anti-commuting operator is the new content of this
note — it identifies the SPECIFIC operator structure that would
realize Koide Q = 2/3 on the 3-generation triplet.

## 10. Boundary

This is a NARROW POSITIVE DERIVATION THEOREM. It establishes
that, given the existence of an Hermitian H on R^3 that
anti-commutes with the Z_3 character grading Γ_χ, ANY non-zero-
eigenvalue eigenvector v of H automatically satisfies Koide
Q = 2/3.

It SHARPENS the Koide closure question from "derive Q = 2/3" to
"find a Hermitian anti-commuting H with v as eigenvector." The
existence/uniqueness of such an H within the Cl(3)/Z³ framework
is an open research-level question with named candidate routes
(§6).

A class-A runner verifies the derivation symbolically and
exhibits explicit examples of anti-commuting H matrices and
their LCC-satisfying eigenvectors
(`scripts/frontier_koide_anticommuting_operator_derivation.py`).
