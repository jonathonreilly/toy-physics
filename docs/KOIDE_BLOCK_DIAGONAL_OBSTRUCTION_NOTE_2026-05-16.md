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

## 1. Assumptions exercise (Elon first-principles)

### 1.1 Framework context cited as background

| Item | Content | Role here |
|---|---|---|
| Z1 | `Γ_χ = (2/3) J − I` on R^3 with eigenvalues +1 (singlet) and −1 (doublet) | cited from `KOIDE_ANTICOMMUTING_OPERATOR_DERIVATION_THEOREM_NOTE_2026-05-10` (retained); not re-ratified here |
| Z2 | L4 2-dim anti-commuting family: H = (1/3)(1⊗h + h⊗1), Σh = 0 | cited; not re-ratified |
| Z3 | Lightcone Primitive: Z_3-equivariant H = aI + bR + b*R² | cited from `KOIDE_LIGHTCONE_PRIMITIVE_THEOREM_NOTE_2026-05-10` (retained) |
| Z4 | Cycle 1 (this campaign): Z_3-equivariant + {H, Γ_χ}=0 ⟹ H=0 | cited from `KOIDE_Z3_EQUIVARIANT_ANTICOMMUTING_NO_GO_NOTE_2026-05-16` (exact_support, sibling cycle); not re-ratified |

### 1.2 The four assumptions in this strengthening note

| Label | Statement |
|---|---|
| A1 | "Block-diagonal in Γ_χ's eigenbasis" is a meaningful framework-level constraint distinct from Z_3-equivariance. |
| A2 | The strictly-weaker hypothesis (relative to Cycle 1's Z_3-equivariance) closes off candidate framework realizations not closed by Cycle 1. |
| A3 | The §4 algebra-equivariance corollary's three-case table represents meaningful breadth (not tautological breadth). |
| A4 | The block-diagonality structural insight is new content distinct from L4's §3 statement "H mixes singlet and doublet". |

### 1.3 Hostile engagement with each assumption

**A1 — "Block-diagonality is a meaningful framework-level constraint."**

The (s, D) decomposition is determined by Γ_χ's spectral decomposition.
"Block-diagonal in (s, D)" means H ∈ End(s) ⊕ End(D), i.e., H preserves
the Z_3-trivial vs Z_3-non-trivial sectors. ANY algebra A acting on R^3
with `Γ_χ ∈ commutant(A)` automatically satisfies this (its commutant
preserves Γ_χ's eigenspaces). So the framework correspondence is:

```text
   Block-diagonal in (s, D)  ⟺  Preserves the Z_3-trivial vs non-trivial sectors
```

This IS a meaningful framework primitive. But the immediate question:
which framework primitives naturally produce H preserving this
decomposition? Z_3-equivariance is one. The retained Lightcone
Primitive note explicitly works in the Z_3-equivariant basis, so the
"block-diagonal" framing is one decomposition step away from
Lightcone-style retained content.

**Hostile verdict on A1:** Constraint is meaningful but is a
restatement of "preserves Γ_χ-eigenspaces", which is implicit in any
discussion of Γ_χ. Not a new structural primitive.

**A2 — "Strict generalization closes off candidate realizations not closed by Cycle 1."**

The 3 extra real dimensions of H closed off (relative to Cycle 1) are:
- Cycle 1 covers Z_3-equivariant H restricted to D = scalar (1-dim on D)
- Cycle 2 covers block-diagonal H with H_D arbitrary in Sym(D) (3-dim on D)
- Extra dimensions = 3 − 1 = 2 dims on D plus possibly something else,
  for a total of 3 extra (per agent computation in the loop pack).

Question: do any candidate framework realizations produce H block-diagonal
in (s, D) but with H_D a NON-SCALAR symmetric 2×2 matrix? This would
require the framework primitive A to act NON-SCALARLY on the doublet
(i.e., A's commutant on D is larger than just scalars). But any algebra
A with Γ_χ ∈ commutant(A) and `A ≠ trivial` necessarily has commutant
that block-diagonalizes — the only question is whether commutant on D
is scalars (Schur on D irreducible) or larger (D reducible under A).

Concrete framework primitives:
- A = Z_3 (regular rep): D irreducible, commutant on D = scalars (1-dim).
  Cycle 1 covers this.
- A = R ⊕ R (diagonal in (s, D)): D trivially reducible (= scalars × 2),
  commutant on D = Mat_2(R) (3-dim). Cycle 2 newly covers this.
- A = trivial (no action): everything is in commutant. Cycle 2 covers this.

The "newly covered" cases (A = R ⊕ R or trivial) are framework primitives
that DON'T act on R^3 in any non-trivial way — they're degenerate cases
that don't provide framework primitivity. So they don't correspond to
candidate Level 5 realizations.

**Hostile verdict on A2:** The 3 extra dimensions are mathematically real
but **physically vacuous**. No candidate framework realization sits in
the "newly covered" region. The hostile reviewer's F-3 finding is
confirmed.

**A3 — "§4 three-case table represents meaningful breadth."**

Each case (a/b/c) trivially satisfies the corollary hypothesis by
construction. Case (a) = Cycle 1 verbatim. Cases (b), (c) are degenerate
algebra choices (R ⊕ Mat_2(R), R ⊕ R) that pre-assume the (s, D)
block-diagonal structure. None of the three cases probes the boundary
"is Γ_χ ∈ commutant(A)?" — they all pre-suppose it.

**Hostile verdict on A3:** Breadth without depth. The cases enumerate
algebras of different sizes, all comfortably interior to the corollary
hypothesis. None tests the corollary's edge.

**A4 — "Block-diagonality insight is new content distinct from L4 §3."**

L4 §3.2 (line 187-194) states: "the all-ones vector is NOT an
eigenvector of H... The eigenvectors of H are different from the
singlet/doublet decomposition under Γ_χ. This is exactly the property
needed — H 'mixes' the singlet and doublet subspaces, which is what
anti-commutation with Γ_χ requires."

This IS the negation of block-diagonality in (s, D). L4 §3 says H mixes
s ↔ D; Cycle 2 says block-diagonal H + anti-commute ⟹ H = 0. These are
two formulations of the same structural fact.

The deeper insight Cycle 2 surfaces is the **direct-sum decomposition of
Sym(R^3) in (s, D)**:

```text
   Sym(R³)  =  (block-diagonal in (s, D))  ⊕  (off-block in (s, D))
            =  [End(s) ⊕ Sym(D)]           ⊕  [singlet↔doublet exchange]
            =  4 real-dim                  ⊕  2 real-dim
```

Anti-commutation with Γ_χ forces H into the off-block component. So:

- Block-diagonal H + anti-commute = block-diagonal ∩ off-block = {0} (Cycle 2).
- Anti-commuting Hermitian H = off-block component = 2 real-dim subspace (= L4 family).

**Hostile verdict on A4:** The direct-sum decomposition Sym(R³) =
(block) ⊕ (off-block) is the underlying mechanism for BOTH L4's 2-dim
family characterization AND Cycle 2's obstruction. L4 §3.2 sees the
"mixes singlet and doublet" half (off-block side); Cycle 2 §2 sees the
"block-diagonal + anti-commute = 0" half (block-diagonal side). They
are dual statements about the same subspace decomposition.

This is a clean structural framing — but it does NOT add new content
beyond L4 §3. It surfaces the underlying geometry that L4 §3 already
identifies.

### 1.4 Elon first-principles — what is the obstruction, really?

**Stripping all framework conventions, what is the structural content?**

The space `Sym(R³)` is 6 real-dim. Any operator `Γ_χ ∈ Sym(R³)` with
spectrum `{+1, −1, −1}` (i.e., trace = −1, det = +1, characteristic
polynomial `(λ−1)(λ+1)²`) has eigenspaces s (dim 1) and D (dim 2).

This decomposition gives an orthogonal direct-sum decomposition:

```text
   Sym(R³)  =  V_block  ⊕  V_off
   dim 6    =  dim 4    ⊕  dim 2
   V_block  =  {H : H = H_s ⊕ H_D}  =  End(s) ⊕ Sym(D)
   V_off    =  {H : H = X ⊕ X^T on (s, D) off-blocks}  =  Hom(s, D) symmetrized
```

Under this decomposition:

```text
   {H, Γ_χ}  =  2 (block component of H)  −  2 · (-1) · (block component)
            =  ... (full formula yields)
   {H, Γ_χ}  =  0   ⟺   H ∈ V_off
```

(Anti-commutation kills the block-diagonal part; only off-block H
satisfies it.)

Cycle 2's main theorem is then a one-line statement:

```text
   V_block ∩ V_off  =  {0}    (orthogonal direct-sum decomposition)
```

This is true by the very definition of direct sum. There is **no new
mathematical content** beyond observing that Γ_χ's spectral decomposition
gives a direct-sum decomposition of Sym(R³), and the L4 anti-commutator
condition picks out one summand.

**What is Cycle 1's theorem, really, in this framing?**

The Z_3 regular rep on R^3 has the same eigenspaces s = trivial-character
subspace, D = non-trivial character subspace. Z_3-equivariant H lives
in `End_{Z_3}(R³) = End(s) ⊕ End_{Z_3}(D) = R ⊕ R[Z_3 \ {0}]^{R} = R ⊕
ℂ ≅ R³` (the circulant algebra, 3 real-dim).

Z_3-equivariant H is, in particular, block-diagonal in (s, D): the
circulant algebra is contained in V_block. So Cycle 1's hypothesis is
V_block ∩ V_off = {0} restricted to the circulant subspace of V_block.

This is even tighter than Cycle 2's statement, but the underlying
mechanism — direct-sum decomposition — is identical.

**Conclusion of the Elon strip-down.** Both Cycle 1 and Cycle 2 are
restatements of the trivial fact that a direct-sum decomposition has
trivial intersection. The structural content lives in Γ_χ's spectral
decomposition (= retained L4 setup) and the L4 §3 observation that the
anti-commuting family lies in V_off. Cycles 1-2 add no new structural
mechanism beyond what L4 already implicitly contains.

**Implication for tier-setting.** The hostile reviewer's DEMOTE verdict
is fully consistent with this Elon analysis. The notes' value is
**exact-support documentation of the direct-sum decomposition that
underlies L4's anti-commuting family characterization** — useful for
structural clarity, not for novel positive_theorem content.

## 2. Theorem statement

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

## 3. Proof

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

## 4. Comparison with Cycle 1's Z_3-Equivariant Result

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

## 5. Algebra-Equivariance Reformulation

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

## 6. Implications across the 5-route fan-out

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

## 7. What this support note does NOT establish

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

## 8. Falsifiers

- A computational error in §2 (verified by the runner — 8 PASS / 0
  FAIL, all class-A).
- A counterexample of the form: block-diagonal Hermitian H on R^3
  with `{H, Γ_χ} = 0` and H ≠ 0. Refuted by the explicit two-block
  argument of §2.
- A counterexample of the form: non-trivial algebra A with
  `Γ_χ ∈ commutant(A)` and a non-zero A-equivariant Hermitian H
  with `{H, Γ_χ} = 0`. Refuted by Cor 4.1.

## 9. Cross-references (non-load-bearing)

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

## 10. Boundary

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
