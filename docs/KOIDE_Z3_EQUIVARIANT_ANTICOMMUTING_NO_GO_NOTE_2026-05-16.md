# Koide Z_3-Equivariant Anti-Commuting Operator — Subalgebra Disjointness

**Date:** 2026-05-16

**Claim type:** bounded_theorem
**Status:** bounded algebraic support identity; not a global no-go theorem
**Claim scope:** the subspace of Hermitian operators on R^3 commuting
with the cyclic shift R intersects the subspace of Hermitian operators
anti-commuting with `Γ_χ = (2/3) J − I` only at H = 0.

**Status authority:** independent audit lane only. This source note
does not set or predict an audit outcome; later status is generated
by the audit pipeline after independent review.

This is a **pure algebraic subalgebra-disjointness identity** that
extends the §6.1 negative observation in
`KOIDE_ANTICOMMUTING_OPERATOR_DERIVATION_THEOREM_NOTE_2026-05-10.md`
from one specific operator `(R - R^T)/i` to the full 3-dim circulant
algebra `⟨I, R, R²⟩`.

**Scope clarification:** this note does NOT claim to close standard
Connes-Lott style spectral triple constructions in general. It
addresses ONLY the literal identification of the Connes-Lott Z_2
chirality grading `γ_CL = diag(I, −I)` (on `H_L ⊕ H_R`) with the Z_3
character grading `Γ_χ` (on a single `R³` generation factor) — a
hybrid identification that no standard NCG construction uses. The
generic Connes-Lott structure with `H = R³ ⊗ (H_L ⊕ H_R)`,
`γ_CL = I ⊗ σ_3`, and `Γ_χ` as a SEPARATE grading on the `R³`
factor is NOT addressed by this note. See §4 for the precise scoping.

**Primary runner:** [`scripts/frontier_koide_z3_equivariant_anticommuting_no_go.py`](./../scripts/frontier_koide_z3_equivariant_anticommuting_no_go.py)

**Lane:** 6 — charged-lepton mass workstream context only; closure
not claimed.

---

## 1. Theorem statement

**Theorem (Z_3-Equivariance and Γ_χ-Anti-Commutation Are Incompatible).**

Let `R ∈ R^{3×3}` be the cyclic shift permutation matrix,

```text
   R  :=  [[0, 0, 1],
           [1, 0, 0],
           [0, 1, 0]]                                                  (1.1)
```

with `R^3 = I`. Let `Γ_χ := (2/3) J − I` where `J ∈ R^{3×3}` is the
rank-1 all-ones matrix. Let `H ∈ R^{3×3}` be Hermitian (real
symmetric).

If both
```text
   [H, R]    =  0                                                      (1.2)
   {H, Γ_χ}  =  0                                                      (1.3)
```
then H = 0.

## 2. Proof

The proof is a direct consequence of the fact that Γ_χ lies in the
commutative circulant algebra ⟨I, R, R²⟩.

### 2.1 Z_3-equivariance places H in the circulant algebra

By (1.2), H commutes with R. The commutant of R in `Mat_3(R)` is the
3-real-dim circulant algebra:

```text
   H  =  a I + b R + c R²       for some (a, b, c) ∈ R³               (2.1.1)
```

The circulant algebra ⟨I, R, R²⟩ is commutative: `[R, R²] = 0`.

### 2.2 Γ_χ is itself a circulant

The all-ones matrix `J = I + R + R²` is itself a circulant (the sum
of the cyclic group elements). Therefore

```text
   Γ_χ  =  (2/3) J − I  =  (2/3)(I + R + R²) − I
         =  (-1/3) I  +  (2/3) R  +  (2/3) R²                          (2.2.1)
```

is a circulant. In particular, `[Γ_χ, R] = 0` and `[Γ_χ, R²] = 0`.

### 2.3 Commutativity reduces anti-commutation to a product condition

Since H and Γ_χ both lie in the commutative circulant algebra,
`[H, Γ_χ] = 0` identically. Therefore

```text
   {H, Γ_χ}  =  H Γ_χ + Γ_χ H  =  2 H Γ_χ                              (2.3.1)
```

Condition (1.3) is then equivalent to

```text
   H Γ_χ  =  0                                                          (2.3.2)
```

### 2.4 Diagonalization in the Z_3 Fourier basis

The Fourier basis of R³ (eigenbasis of R) has eigenvalues `1, ω, ω²`
where `ω = e^{2πi/3}` is the primitive cube root of unity. In this
basis:

- `R` is diagonal: `diag(1, ω, ω²)`.
- `J = I + R + R²` is diagonal: `diag(3, 0, 0)` (only the trivial
  character survives).
- `Γ_χ = (2/3) J − I` is diagonal: `diag(+1, −1, −1)`.
- `H = a I + b R + c R²` is diagonal:
  `diag(a + b + c, a + bω + cω², a + bω² + cω)`.

### 2.5 Product condition forces all coefficients to zero

H Γ_χ = 0 in the diagonal basis requires the diagonal product to
vanish component-wise:

```text
   (a + b + c)        · (+1)  =  0    ⟹  a + b + c     =  0          (2.5.1)
   (a + bω + cω²)     · (−1)  =  0    ⟹  a + bω + cω²  =  0          (2.5.2)
   (a + bω² + cω)     · (−1)  =  0    ⟹  a + bω² + cω  =  0          (2.5.3)
```

This is the discrete Fourier transform on Z_3:

```text
   F (a, b, c)^T  =  (0, 0, 0)^T                                        (2.5.4)
```

where F is the Z_3 character matrix (rows indexed by characters, columns
by group elements). F is invertible (Schur orthogonality of characters
on a finite group), so the only solution is `a = b = c = 0`.

Therefore H = 0. ∎

## 3. Equivalent algebraic reformulation

The theorem statement
`comm(R) ∩ anticomm(Γ_χ) = {0}  inside  Sym(R³)`
is equivalent (via the Z_3 discrete Fourier transform of §2.4) to
the linear algebra statement that the 3×3 Z_3 character matrix `F`
applied to the circulant coefficient triple `(a, b, c)` together
with the non-zero Γ_χ eigenvalue triple `(+1, −1, −1)` admits no
non-trivial common solution. The geometric content is that the
2-dim anti-commuting family of
`KOIDE_ANTICOMMUTING_OPERATOR_DERIVATION_THEOREM_NOTE_2026-05-10` is
**disjoint from** the 3-dim circulant algebra `⟨I, R, R²⟩` (their
intersection is only at H = 0).

## 4. Scope-narrow Connes-Lott observation

This section records a SCOPE-NARROW observation about a specific
(forced) Connes-Lott identification. It does NOT close generic
Connes-Lott constructions.

**Observation.** Consider a finite spectral triple `(A, H_st, D, γ, J)`
where one IMPOSES BOTH of these constraints:
1. The Yukawa Dirac D on a single 3-generation factor `R³` is
   Z_3-equivariant: `[D, R] = 0` (e.g., because `A = Cl(3) ⋊ Z_3`
   acts via its regular representation on `R³` and the first-order
   condition forces D into the commutant of R).
2. The spectral-triple grading γ acts on the same `R³` factor as
   the Z_3 character grading `Γ_χ = (2/3) J − I`, with the
   constraint `{D, Γ_χ} = 0`.

Then by the main theorem, **D = 0** on that `R³` factor.

**What this observation does NOT exclude.** The standard
Connes-Lott structure for fermion generations is `H_st = R³ ⊗ (H_L ⊕ H_R)`
(generation factor `R³` tensored with left-right doubling
`H_L ⊕ H_R`), with `γ_CL = I_3 ⊗ σ_3` acting on the chirality
factor — NOT on the generation factor. In such constructions,
`γ_CL ≠ Γ_χ`; the Z_2 chirality grading and the Z_3 character
grading live in different tensor factors. The off-diagonal Yukawa
acts on the generation factor `R³` and is unconstrained by
chirality anti-commutation — the L4 anti-commutation `{·, Γ_χ}=0`
on the generation factor would be a SEPARATE condition, not the
spectral-triple anti-commutation hypothesis.

**Escape hatches.** To recover a non-zero D realizing the L4
anti-commuting form, one must either:
- (I) drop the Z_3-equivariance of D on a single `R³` factor — but
  then "framework primitivity via Z_3 group action" is lost and the
  specific h becomes an external input, or
- (II) use a multi-factor Hilbert space where the spectral-triple
  γ-grading lives on a factor distinct from where Γ_χ acts. The
  main theorem then does not apply, and a separate bridge theorem
  is needed to connect Connes-Lott anti-commutation to the L4
  hypothesis.

Both directions are open. The present note closes ONLY the literal
single-factor identification γ = Γ_χ + Z_3-equivariance.

## 5. What this support note does NOT establish

- A no-go on Level 5 globally. Standard Connes-Lott constructions
  with tensored Hilbert space `R³ ⊗ (H_L ⊕ H_R)` (chirality grading
  on a SEPARATE factor from Γ_χ) are NOT addressed.
- A no-go on twisted/modular spectral triples (Connes-Moscovici
  2008), Chamseddine-Connes spectral action variants, staggered-Dirac
  taste cube routes, or Hilbert-space-extension constructions.
- A retirement of any retained Koide chain theorem. Levels 1-4
  (Z_3 character norm split, Lightcone Primitive, Anti-Commuting
  Operator) remain audit-ratified on main.
- A claim about Lane 6 closure.

The note establishes ONLY the narrow algebraic identity
`comm(R) ∩ anticomm(Γ_χ) = {0}` inside `Sym(R³)`, plus its
scope-narrow corollary about the literal single-factor identification
γ = Γ_χ + Z_3-equivariance of the Dirac.

## 5.1 No-go discipline boundary

This file name retains `NO_GO` because the branch originated as a
negative-route packet, but the landed claim is not a global no-go.  The
negative content is only the exact intersection statement
`comm(R) ∩ anticomm(Γ_χ) = {0}` under the simultaneous assumptions
`[H,R]=0` and `{H,Γ_χ}=0`.

- **N1 alternative routes:** not claimed closed.  At least five routes are
  explicitly outside this bounded identity: multi-factor Connes-Lott with
  chirality on a separate factor, dropped Z_3-equivariance, twisted/modular
  spectral triples, staggered-Dirac taste-cube constructions, and larger
  Hilbert-space extensions.
- **N2 wall independence:** the wall is the simultaneous imposition of
  Z_3-equivariance and Γ_χ anti-commutation on the same R^3 factor.  The
  result does not assert independence from that wall.
- **N3 hidden-wall scan:** no physical species, PMNS, mass, or Level-5
  closure reading is consumed.
- **N4 residual matching:** residual routes are the five alternatives named
  in N1; each remains open.
- **N5 rhetoric audit:** global phrases such as "Level 5 no-go" are excluded;
  the claim is a bounded algebraic support identity.
- **N6 partial-closure path:** a nonzero operator can still enter through any
  route that avoids the same-factor Γ_χ anti-commutation plus R-commutation
  wall.
- **N7 steelman:** the standard Connes-Lott steelman places γ_CL and Γ_χ in
  different tensor factors, so this note does not touch it.
- **N8 cross-cycle echo:** downstream Koide-chain and spectral-triple claims
  must cite this only as a local obstruction, not as retained route closure.

## 6. Falsifiers

- A computational error in §2 (verified symbolically by the runner
  with `dominant_class: A`).
- A claim that Γ_χ does NOT lie in the circulant algebra (refuted by
  the algebraic identity `Γ_χ = (-1/3)I + (2/3)R + (2/3)R²` in §2.2).
- A claim that some non-trivial circulant H satisfies `H Γ_χ = 0`
  (refuted by §2.5 via the invertibility of the Z_3 Fourier
  transform).

## 7. Cross-references (non-load-bearing)

- Anti-commuting H 2-dim family characterization:
  `KOIDE_ANTICOMMUTING_OPERATOR_DERIVATION_THEOREM_NOTE_2026-05-10.md`
- Lightcone Primitive (Z_3-equivariant H working in the circulant
  basis): `KOIDE_LIGHTCONE_PRIMITIVE_THEOREM_NOTE_2026-05-10.md`
- NSC recasting:
  `KOIDE_Q_TWO_THIRDS_Z3_CHARACTER_NORM_SPLIT_RECASTING_THEOREM_NOTE_2026-05-10.md`
- Prior Cl(3) bivector no-go (§6.1 of L4 note): `(R-R^T)/i` commutes
  with Γ_χ, similar structural reason (anti-Hermitian part of R is
  also in the circulant algebra).
- Chamseddine-Connes spectral triple machinery (admitted import):
  hep-th/9606001
- Connes-Moscovici twisted spectral triples (admitted import for
  alternative route R5): Connes-Moscovici 2008

## 8. Lane 6 context

This bounded identity is graph-disconnected from the Lane 6 physics chain. It
constrains the SPACE of candidate framework realizations of the
Level 4 anti-commuting H — it does not assert any Koide closure or
charged-lepton mass derivation.

## 9. Boundary

This is a NARROW EXACT SUPPORT IDENTITY. It establishes the
algebraic subalgebra-intersection fact:

> `comm(R) ∩ anticomm(Γ_χ) = {0}`   inside   `Sym(R³)`

equivalently that the Z_3 discrete Fourier transform is invertible
applied to circulant coefficients required to vanish via product
with the non-degenerate circulant Γ_χ.

The CONNECTION to spectral-triple constructions is a SCOPE-NARROW
observation (§4): the LITERAL single-factor identification of the
Connes-Lott Z_2 chirality grading with Γ_χ, combined with
Z_3-equivariance of the Yukawa Dirac, forces the Dirac to zero.
This does NOT close standard multi-factor Connes-Lott constructions
where γ_CL and Γ_χ live in distinct tensor factors. Such
constructions remain open research targets.

A class-A runner verifies the algebraic core symbolically and
exhibits explicit Z_3 Fourier transforms of (a, b, c) showing the
forcing to zero
(`scripts/frontier_koide_z3_equivariant_anticommuting_no_go.py`).
