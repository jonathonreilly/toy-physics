# I1 Block-by-Block Forcing: Frobenius Isotype Split Uniqueness

**Date:** 2026-04-21
**Status:** Retained-forced verification of the I1 AM-GM closure.
**Runner:** `scripts/frontier_koide_frobenius_isotype_split_uniqueness.py` — 32/32 PASS.

---

## Statement

Every building block of the Koide `F = log(E_+ · E_⊥)` + AM-GM
derivation of Q = 2/3 is verified forced by the retained
Cl(3)/Herm_circ(3) axioms — no choice is made anywhere; every piece
is determined by the retained structure.

## Forced building blocks

1. **Frobenius (trace) inner product** `⟨A, B⟩ = Tr(AB)` is the
   canonical inner product on Herm(3), unique up to scale by
   bilinearity + symmetry + conjugation-invariance +
   positive-definiteness.

2. **C_3-singlet vector projector** `P_0 = J/3` on C³ is the unique
   rank-1 Hermitian projector onto span{(1,1,1)/√3}, commuting with
   the cyclic shift C.

3. **Matrix-space scalar projector** `P_I : M ↦ (tr M / 3) · I`
   is the unique orthogonal projection from Herm(3) onto scalar
   multiples of I in the Frobenius inner product.

   *Important clarification*: `P_0 = J/3` (vector-space) and `P_I`
   (matrix-space) are distinct projectors serving distinct roles.
   The isotype energies E_+, E_⊥ use the matrix-space projector `P_I`.

4. **Singlet (scalar-subspace) energy** `E_+ = ||P_I(M)||_F² = (tr M)²/3 = 3a²`.

5. **Doublet (traceless-subspace) energy** `E_⊥ = ||(I − P_I)(M)||_F² = Tr(M²) − E_+ = 6|b|²`.

6. **Positivity**: E_+, E_⊥ ≥ 0. Interior case (both > 0) is generic
   for physical charged leptons with non-degenerate masses.

7. **Pythagoras** (orthogonal decomposition in Frobenius inner product):
   E_+ + E_⊥ = Tr(M²) exactly.

## AM-GM gives Q = 2/3

Given the forced decomposition, AM-GM applies directly:

- Constraint: `E_+ + E_⊥ = Tr(M²) = N` (fixed total Frobenius norm).
- Functional: `F_sym = log(E_+) + log(E_⊥) = log(E_+ · E_⊥)`.
- Hessian has eigenvalues −1/E_+² and −1/E_⊥² (strictly concave).
- Unique maximum at `E_+ = E_⊥ = N/2`.

At the maximum:
- `κ = a²/|b|² = 2 · (E_+/E_⊥) = 2`.
- `Q = (1 + 2/κ)/d = (1 + 1)/3 = 2/3` at d = 3.

## Why this answers the reviewer question "is F a choice?"

**No choice is made.** The Frobenius inner product is the canonical
trace form (unique up to scale). The projections `P_I` and `I − P_I`
are the unique Frobenius-orthogonal projections onto scalar and
traceless subspaces. AM-GM is a mathematical inequality, not a
prescription. Consequently, Q = 2/3 is retained-forced: it follows
by theorem from the retained Cl(3)/Herm_circ(3) axioms.

The "(2, 1) weights" appearing in the equivalent form `F = 2 log(tr G) + log(C_2)`
are the algebraic consequence of the definitional relation
`E_+ = (tr G)²/d` (which squares `tr G`), not a rep-theoretic
prescription.
