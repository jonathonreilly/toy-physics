# Koide Block-Diagonality Obstruction — Strengthening of the Z_3-Equivariant No-Go

**Date:** 2026-05-16

**Type:** exact_support
**Claim scope:** for any Hermitian H ∈ Sym(R^3) that
(i) preserves the singlet/doublet eigenspace decomposition of `Γ_χ = (2/3) J − I`
    (equivalently, H is block-diagonal in the (singlet, doublet) basis), AND
(ii) anti-commutes with Γ_χ,
necessarily H = 0.

**Status authority:** independent audit lane only. This source note
does not set or predict an audit outcome; later status is generated
by the audit pipeline after independent review.

**Hostile review record:** Internal hostile reviewer for this loop's
Cycle 2 returned verdict DEMOTE with the following findings:
- The §2 proof is genuinely simpler than Cycle 1's Z_3 Fourier
  argument, but uses the same underlying obstruction mechanism
  (Γ_χ has full-spectrum non-zero eigenvalues on every block).
- The class of H covered is strictly larger than Cycle 1's
  (3 extra real dimensions), but those dimensions are not
  physically distinguished — no candidate framework realization
  in the Koide chain produces block-diagonal-but-not-Z_3-equivariant H.
- V3 reconstruction concern is sharper than Cycle 1: an audit lane
  can derive this from L4 + projector calculus in one paragraph.
- The §4 three-case table is breadth without depth: each tested
  algebra (Z_3, R ⊕ Mat_2(R), R · I_s ⊕ R · I_D) satisfies the
  corollary hypothesis trivially by construction.
- §5/Part 5 (L4-family escape) restates L4 §3.2's existing
  observation that H "mixes singlet and doublet".

The note is landed at the demoted **exact_support** tier with the
honest scoping below. This is a strengthening identity for the
campaign's documentation of structural obstructions, not a
positive_theorem promotion of the audit-lane verdict.

This is a **pure algebraic block-diagonality identity** that
**strictly generalizes** the `KOIDE_Z3_EQUIVARIANT_ANTICOMMUTING_NO_GO_NOTE_2026-05-16`
from "Z_3-equivariant H" to "H block-diagonal in Γ_χ's eigenspace
decomposition." Z_3-equivariance is one sufficient (but not necessary)
condition for the block-diagonality assumption (i).

**Scope clarification:** This note documents a STRUCTURAL OBSERVATION
about an obstruction common to multiple candidate spectral-triple
realizations of the retained Level 4 anti-commuting H. It does NOT:
- Address constructions where H is NOT block-diagonal in Γ_χ's
  eigenbasis (e.g., multi-factor Connes-Lott with γ_CL on a
  separate tensor factor from Γ_χ).
- Address constructions where Γ_χ is NOT preserved by the framework
  primitive (e.g., SO(3)-irreducible actions where R³ is one block).
- Address routes with different gradings (twisted/modular spectral
  triples, parity gradings, chirality gradings on doubled spaces).

**Primary runner:** [`scripts/frontier_koide_block_diagonal_obstruction.py`](./../scripts/frontier_koide_block_diagonal_obstruction.py)

**Lane:** 6 — charged-lepton mass workstream context only; closure
not claimed.

---

## 1. Theorem statement

**Theorem (Block-Diagonality Obstruction).**

Let `Γ_χ = (2/3) J − I` on R^3 with eigenspace decomposition
`R^3 = s ⊕ D` where:
- `s = R · (1,1,1)^T` is the +1 eigenspace (singlet, dim 1)
- `D = s^⊥` is the −1 eigenspace (doublet, dim 2)

Let `P_s`, `P_D` be the orthogonal projectors onto `s` and `D`.

Let `H ∈ Sym(R^3)` (Hermitian, real symmetric) such that:
```text
   [H, P_s]  =  [H, P_D]  =  0                                       (1.1)
                  (equivalently: H is block-diagonal in s ⊕ D)
   {H, Γ_χ}  =  0                                                    (1.2)
                  (anti-commutation with Γ_χ)
```

Then H = 0.

## 2. Proof

In the eigenbasis of Γ_χ, write H block-diagonally:
```text
   H  =  H_s  ⊕  H_D                                                  (2.1)
```
where `H_s` is a real scalar (1×1 block on the singlet) and `H_D`
is a real symmetric 2×2 matrix (on the doublet).

Γ_χ acts as +1 on `s` and −1 on `D`:
```text
   Γ_χ  =  (+1)  ⊕  (−I_2)                                           (2.2)
```

The anti-commutator block-decomposes:
```text
   {H, Γ_χ}  =  {H_s, (+1)}  ⊕  {H_D, (−I_2)}
              =  2 H_s        ⊕  (−2 H_D)                            (2.3)
```

For (1.2) to hold component-by-component:
```text
   H_s   =  0                                                         (2.4)
   H_D   =  0                                                         (2.5)
```

Hence H = 0. ∎

## 3. Comparison with Cycle 1's Z_3-Equivariant Result

The Cycle 1 result (`KOIDE_Z3_EQUIVARIANT_ANTICOMMUTING_NO_GO_NOTE_2026-05-16`)
proved: H Z_3-equivariant (`[H, R] = 0`) + `{H, Γ_χ} = 0` ⟹ H = 0.

The present theorem proves: H block-diagonal in Γ_χ's eigenspaces +
`{H, Γ_χ} = 0` ⟹ H = 0.

**The block-diagonality condition is STRICTLY WEAKER than
Z_3-equivariance.** Specifically:

- Every Z_3-equivariant H is block-diagonal in (s, D) (since the Z_3
  regular rep on R³ preserves the singlet/doublet decomposition).
- BUT the converse is false. Many block-diagonal H are not
  Z_3-equivariant. For example, `H = 0 ⊕ M_D` with `M_D` a generic
  real symmetric 2×2 matrix is block-diagonal in (s, D), but NOT
  generally Z_3-equivariant (the Z_3 doublet representation is
  2-dim, with specific cyclic structure).

So the present theorem **closes more cases** than Cycle 1 with the
same final conclusion `H = 0`. The proof is also shorter and
basis-independent (no Z_3 Fourier transform needed).

## 4. Algebra-Equivariance Reformulation

**Corollary 4.1 (General Algebra-Equivariance).**

Let A be a unital associative algebra acting on R^3 such that
`Γ_χ ∈ commutant(A)`. Then every Hermitian H ∈ commutant(A)
satisfying `{H, Γ_χ} = 0` is H = 0.

**Proof:** `Γ_χ ∈ commutant(A)` means A preserves the eigenspace
decomposition of Γ_χ (`A` commutes with the projectors `P_s`, `P_D`).
Hence `commutant(A) ⊆ End(s) ⊕ End(D)` (block-diagonal in (s, D)).
Any Hermitian H ∈ commutant(A) is block-diagonal; apply the main
theorem. □

**Tested algebra cases:**

| A | A non-trivial? | Γ_χ ∈ commutant(A)? | A-equivariant H anti-comm Γ_χ ≠ 0? |
|---|---|---|---|
| `Z_3` regular rep on R³ | Yes | Yes | No (Cycle 1) |
| `SO(3)` vector rep | Yes | No (R³ is irreducible) | N/A (premise fails) |
| `Cl(3)` spinor on R³ | Yes | No (R³ is irreducible) | N/A |
| Trivial algebra (R · I) | No | Yes trivially | Many, but A doesn't distinguish Γ_χ |
| Diagonal alg in *original* basis | Yes | No (Γ_χ has off-diagonal entries 2/3) | N/A |
| R ⊕ Mat_2(R) (block diag in (s, D)) | Yes | Yes | No (Cor 4.1, m_s = 0, M_D = 0) |
| Staggered taste shifts ⟨T_1, T_2, T_3⟩ on V_3 | Yes | No (Γ_χ non-diagonal in V_3 basis) | N/A on this basis |

## 5. Implications across the 5-route fan-out

The corollary explains why several of the spectral-triple routes
from the loop's `ROUTE_PORTFOLIO.md` hit obstructions:

**R2 (Connes-Lott Z_3-equivariant Yukawa):** A ⊇ Z_3 forces M
Z_3-equivariant ⟹ block-diagonal in (s, D) ⟹ Cor 4.1 ⟹ M = 0
(special case = Cycle 1).

**Staggered Dirac on V_3 (NG-3 route):** The natural Z_3
coordinate-permutation on V_3 is an A = Z_3 instance; Γ_χ on V_3 in
the appropriate (s, D) basis is in commutant(A); Cor 4.1 applies.
Confirmed by parallel agent computation:
`D²|_{V_3} = −(3/2) I_3` (a Z_3-equivariant scalar, trivially
consistent with both conditions but Koide-trivial).

**What R3, R4, R5 do NOT fall under this obstruction:**
- R3 (Chamseddine-Connes): SO(2) symmetry on `Σh = 0` plane.
  Different mechanism: the spectral action functional is invariant
  under rotations of h within the doublet sector, so no specific
  h is selected.
- R4 (complex 4-dim): reality obstruction. The complex h_C = (1, ω, ω²)
  Z_3-character vector gives a valid anti-commuting Hermitian H but
  the eigenvectors are not real-positive.
- R5 (twisted modular): non-Hermitian Dirac forced by Z_3 twist;
  outside the Z_2 anti-commutation hypothesis of the present theorem.

## 6. What this support note does NOT establish

- A no-go on Level 5 globally. Constructions where H is NOT
  block-diagonal in Γ_χ's eigenbasis remain open:
  - Multi-factor Connes-Lott `H = R^3 ⊗ K` where the L4
    anti-commutation lives on the R^3 factor and the framework
    primitivity comes from the K factor (γ_CL = γ_K).
  - Constructions where Γ_χ acts on a DIFFERENT R^3 than the one
    where H sits (e.g., as a label on multi-generation Hilbert
    space rather than on the generation Hilbert space).
  - Symmetry-breaking constructions where the framework primitive
    A acts with a non-trivial vacuum expectation that picks out a
    specific h.
- A retirement of any retained Koide chain theorem.
- A claim about Lane 6 closure.
- The R3, R4, R5 obstructions (which have their own structural
  reasons documented in the loop's `ROUTE_PORTFOLIO.md`).

## 7. Falsifiers

- A computational error in §2 (verified by the runner — 8 PASS / 0
  FAIL, all class-A).
- A counterexample of the form: block-diagonal Hermitian H on R^3
  with `{H, Γ_χ} = 0` and H ≠ 0. Refuted by the explicit two-block
  argument of §2.
- A counterexample of the form: non-trivial algebra A with
  `Γ_χ ∈ commutant(A)` and a non-zero A-equivariant Hermitian H
  with `{H, Γ_χ} = 0`. Refuted by Cor 4.1.

## 8. Cross-references (non-load-bearing)

- Anti-commuting H 2-dim family characterization:
  `KOIDE_ANTICOMMUTING_OPERATOR_DERIVATION_THEOREM_NOTE_2026-05-10.md`
- Z_3-equivariant special case:
  `KOIDE_Z3_EQUIVARIANT_ANTICOMMUTING_NO_GO_NOTE_2026-05-16.md` (this
  campaign's Cycle 1)
- Lightcone Primitive:
  `KOIDE_LIGHTCONE_PRIMITIVE_THEOREM_NOTE_2026-05-10.md`
- NSC recasting:
  `KOIDE_Q_TWO_THIRDS_Z3_CHARACTER_NORM_SPLIT_RECASTING_THEOREM_NOTE_2026-05-10.md`
- Chamseddine-Connes spectral triple machinery:
  hep-th/9606001 (admitted import)

## 9. Boundary

This is a NARROW EXACT SUPPORT IDENTITY. It establishes the
block-diagonality obstruction:

> Block-diagonal H in Γ_χ's eigenbasis + `{H, Γ_χ} = 0`  ⟹  H = 0

This subsumes Cycle 1's Z_3-equivariant special case under a
strictly more general structural statement. The proof is a 3-line
block decomposition (Section 2), shorter than Cycle 1's Fourier
diagonalization argument.

A class-A runner verifies the algebraic core symbolically including:
- Block-diagonal H structure in (s, D)
- Γ_χ block-diagonal action (+I_s ⊕ −I_D)
- Anti-commutator block-by-block decomposition
- Forcing H_s = 0 and H_D = 0
- Algebra-equivariance corollary 4.1 for several test algebras
- Subsumption of Cycle 1 as the A = Z_3 special case
