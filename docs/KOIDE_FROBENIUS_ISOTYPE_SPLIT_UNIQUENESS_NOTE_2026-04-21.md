# Q-Route Block-by-Block Forcing: Frobenius Isotype Split Uniqueness

**Date:** 2026-04-21
**Status:** Strong executable support verification of the April 21 AM-GM route.
**Runner:** `scripts/frontier_koide_frobenius_isotype_split_uniqueness.py` — 28/28 PASS.
All checks are executable symbolic or numeric computations; no literal
`True` placeholders remain.

---

## Statement

Every building block of the Koide `F = log(E_+ · E_⊥)` + AM-GM route to
`Q = 2/3` is verified executable and structurally fixed by the admitted
Cl(3)/Herm_circ(3) setup. This note is about the internal mathematical chain on
that admitted route. It does not by itself prove the remaining physical/source-
law bridge showing that the charged-lepton packet must be selected by this
extremal principle.

## Forced building blocks (each with an executable check)

1. **Frobenius (trace) inner product** `⟨A, B⟩ = Tr(AB)` is the
   canonical inner product on Herm(3). The runner verifies
   Ad-invariance executively: for a generic U(3) element `U =
   diag(e^{it_1}, e^{it_2}, e^{it_3})` and Hermitian test matrices
   A, B, sympy confirms `Tr(U^†AU · U^†BU) = Tr(AB)` identically in
   the (t_i). Positive-definiteness rules out alternative bilinear
   forms (e.g. `(tr A)(tr B)` vanishes on traceless matrices).

2. **C_3-singlet vector projector** `P_0 = J/3` on C³. The runner
   computes C's eigenvalues, identifies the unique real eigenvalue
   (= 1), extracts its eigenvector (1,1,1)/√3, forms the rank-1
   Hermitian projector, and confirms it equals J/3 symbolically.

3. **Matrix-space scalar projector** `P_I : M ↦ (tr M / 3) · I`
   is the unique orthogonal projection from Herm(3) onto scalar
   multiples of I in the Frobenius inner product. The runner
   computes `P_I(M) = a·I` symbolically and confirms Frobenius
   orthogonality.

   *Important clarification*: `P_0 = J/3` (vector-space) and `P_I`
   (matrix-space) are distinct projectors serving distinct roles.
   The isotype energies E_+, E_⊥ use the matrix-space projector `P_I`.

4. **Singlet (scalar-subspace) energy** `E_+ = ||P_I(M)||_F² =
   (tr M)²/3 = 3a²` — computed symbolically.

5. **Doublet (traceless-subspace) energy** `E_⊥ = ||(I − P_I)(M)||_F²
   = Tr(M²) − E_+ = 6|b|²` — computed symbolically.

6. **Positivity**: the runner checks `sp.solve(3a² < 0, a)` and
   `sp.solve(6(x² + y²) < 0, [x, y])` return empty / False over the
   reals. For the interior case, PDG charged-lepton masses are
   substituted and the runner confirms `E_+ > 0` AND `E_⊥ > 0`
   numerically (strict, not just non-negative).

7. **Pythagoras**: `E_+ + E_⊥ = Tr(M²)` verified symbolically.

8. **AM-GM maximum**: the runner computes the univariate product
   `P(E_+) = E_+ · (N − E_+)`, solves dP/dE_+ = 0, finds the unique
   critical point at E_+ = N/2 with P = (N/2)², and checks d²P/dE_+²
   = −2 < 0 (strict concavity). Solving `3a² = 6|b|²` at equality
   gives κ = a²/|b|² = 2, hence Q = 2/3 at d = 3.

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

**No hidden internal choice is made on this route.** The Frobenius inner product is the canonical
trace form (unique up to scale). The projections `P_I` and `I − P_I`
are the unique Frobenius-orthogonal projections onto scalar and
traceless subspaces. AM-GM is a mathematical inequality, not a
prescription. Consequently, this admitted block-total route isolates the Koide
point `Q = 2/3`. What remains open is not the internal AM-GM step, but the
physical/source-law bridge from the accepted charged-lepton framework surface to
this extremal principle.

The "(2, 1) weights" appearing in the equivalent form `F = 2 log(tr G) + log(C_2)`
are the algebraic consequence of the definitional relation
`E_+ = (tr G)²/d` (which squares `tr G`), not a rep-theoretic
prescription.
