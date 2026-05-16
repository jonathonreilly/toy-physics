# Koide Z_3-Equivariant Anti-Commuting Operator No-Go

**Date:** 2026-05-16

**Type:** no_go
**Claim scope:** for any 3×3 Hermitian operator H on R^3 that
(i) is Z_3-equivariant (commutes with the cyclic shift R = the 3-cycle
permutation matrix), AND
(ii) anti-commutes with the Z_3 character grading
`Γ_χ = (2/3) J − I` (where J is the rank-1 all-ones matrix),
necessarily H = 0.

**Status authority:** independent audit lane only. This source note
does not set or predict an audit outcome; later status is generated
by the audit pipeline after independent review.

This is a **pure algebraic no-go** that closes a specific candidate
realization of the retained anti-commuting operator family of
`KOIDE_ANTICOMMUTING_OPERATOR_DERIVATION_THEOREM_NOTE_2026-05-10.md`:
namely, **no element of the 2-dim anti-commuting family is
Z_3-equivariant (other than H = 0)**.

As a corollary, **no Connes-Lott style finite spectral triple on
`Cl(3) ⋊ Z_3` with Z_3-equivariant Yukawa Dirac D can realize the
required anti-commuting Hermitian H of the Level 4 theorem.** The
Connes first-order condition forces D on the 3-generation triplet
to be Z_3-equivariant on both sides, and the present no-go then
forces D = 0 on that subspace.

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

## 3. Equivalent statements

The theorem admits four equivalent reformulations:

(a) Algebraic: `comm(R) ∩ anticomm(Γ_χ) = {0}` inside `Sym(R³)`.

(b) Fourier: in the Z_3 character basis, H is diagonal (by Z_3-equivariance)
    and Γ_χ is diagonal with non-zero entries; their anti-commutator
    diagonal vanishes only when H itself is zero.

(c) Geometric: the 2-dim anti-commuting family
    `{H = (1/3)(1⊗h + h⊗1) : h ∈ R³, Σh = 0}` of
    `KOIDE_ANTICOMMUTING_OPERATOR_DERIVATION_THEOREM_NOTE_2026-05-10`
    is **disjoint from** the 3-dim circulant algebra
    `⟨I, R, R²⟩` (intersection only at H = 0).

(d) Categorical: the Z_3-equivariant subcategory of `Sym(R³)` (as a
    `R[Z_3]`-module) and the Γ_χ-anti-commuting subcategory have
    trivial intersection.

## 4. Connes-Lott corollary

**Corollary (Connes-Lott Z_3-Equivariant Yukawa No-Go).**

Let `(A, H, D, γ, J)` be a finite spectral triple with:
- `A = Cl(3) ⋊ Z_3` (or any algebra containing the Z_3 group action),
- `H = R³ ⊕ R³` (Connes-Lott left-right structure),
- `D = [[0, M], [M†, 0]]` (off-diagonal Yukawa, `M ∈ Mat_3(C)`),
- `γ = diag(I, −I)` (Z_2 chiral grading).

Suppose:
1. The first-order condition `[[D, a], b°] = 0` for all `a, b ∈ A`
   forces M to be Z_3-equivariant: `[M, R] = 0`.
2. We attempt to identify `γ` on a single `R³` factor with `Γ_χ` (i.e.,
   we ask that the restriction of D to `R³ ⊕ R³` anti-commute with
   `Γ_χ ⊕ Γ_χ` instead of `diag(I, −I)`).

Then **D = 0**, i.e., the Connes-Lott Yukawa structure is trivial.

**Proof:** By assumption (1), M is a 3×3 circulant. By the main
theorem with the identification (2), `{M, Γ_χ} = 0` forces M = 0,
hence D = 0. □

The corollary shows the natural Connes-Lott candidate construction
for realizing the Level 4 anti-commuting H is **structurally
incompatible** with Z_3-equivariance. To recover a non-trivial D
matching the Level 4 H, one must either:
(I) drop Z_3-equivariance on D (losing "framework primitivity" via
the Z_3 group action — h becomes an external input), OR
(II) reinterpret the spectral-triple γ-grading as NOT being identified
with Γ_χ (in which case Level 4's anti-commutation hypothesis does
not directly apply, and one needs a separate bridge theorem).

Both alternatives are open research directions; this no-go closes
only the direct identification.

## 5. What this no-go does NOT establish

- A no-go on Level 5 globally. Other spectral-triple constructions
  (e.g., dropping Z_3-equivariance on D, twisted/modular spectral
  triples per Connes-Moscovici 2008, or alternative gradings) are
  not ruled out by this theorem.
- A retirement of any retained Koide chain theorem (Levels 1-4
  remain audit-ratified).
- A claim about Lane 6 closure.
- A statement about the staggered-Dirac taste cube route (which is
  not Z_3-equivariant in the sense of this theorem).

The theorem rules out ONLY the direct identification of the
spectral-triple γ-grading with `Γ_χ` while preserving Z_3-equivariance
of D.

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

This no-go is graph-disconnected from the Lane 6 physics chain. It
constrains the SPACE of candidate framework realizations of the
Level 4 anti-commuting H — it does not assert any Koide closure or
charged-lepton mass derivation.

## 9. Boundary

This is a NARROW POSITIVE NO-GO THEOREM. It establishes that the
intersection of two subspaces of `Sym(R^3)` is trivial:

> `comm(R) ∩ anticomm(Γ_χ) = {0}`   inside   `Sym(R³)`

equivalently that the discrete Fourier transform on Z_3 is invertible
applied to circulant coefficients required to vanish by anti-commutation
with a non-degenerate circulant Γ_χ.

The CONNECTION to spectral-triple constructions is a corollary
(§4): the natural Connes-Lott structure on `Cl(3) ⋊ Z_3` with
Z_3-equivariant Yukawa is structurally incompatible with
identifying the Z_2 chirality grading with `Γ_χ`.

A class-A runner verifies the algebraic core symbolically and
exhibits explicit Z_3 Fourier transforms of (a, b, c) showing the
forcing to zero
(`scripts/frontier_koide_z3_equivariant_anticommuting_no_go.py`).
