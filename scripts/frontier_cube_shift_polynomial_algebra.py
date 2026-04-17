#!/usr/bin/env python3
"""
The 8-Dimensional Polynomial Algebra in Cube-Shift Operators

Framework object:
  The three cube-shifts S_1, S_2, S_3 on C^8 (from Cube-Shift
  Joint-Eigenstructure) generate an associative polynomial algebra
  A_S ⊂ End(C^8).

Theorem:
  (i)   A_S is abelian (S_i commute pairwise) and has a basis of 8
        squarefree monomials:
           {I, S_1, S_2, S_3, S_1 S_2, S_1 S_3, S_2 S_3, S_1 S_2 S_3}.
        Higher-degree monomials reduce via S_i² = I to one of these 8.
  (ii)  dim_C A_S = 8.
  (iii) A_S is diagonal in the Hadamard basis {|ψ_s⟩}: each monomial
        M_T = ∏_{i ∈ T} S_i has eigenvalue ∏_{i ∈ T} s_i on |ψ_s⟩.
        The map s ↦ (M_T eigenvalues at s) is a bijection from
        {±1}³ onto the character group of A_S.
  (iv)  A_S is a maximal abelian subalgebra of End(C^8): it contains
        all diagonal 8×8 operators in the Hadamard basis.

Proof method: direct computation + algebra.

Reusability:
  - Identifies the natural "diagonal algebra" in the Hadamard basis
  - Used as a stepping stone: any S_3-invariant diagonal-in-Hadamard
    operator lives in a 4-dim subalgebra of A_S (next theorem)
  - Foundation for analyzing operators that are functions of the
    cube-shifts only
"""

from __future__ import annotations

import itertools
import math
import numpy as np

PASS_COUNT = 0
FAIL_COUNT = 0


def check(name: str, condition: bool, detail: str = "") -> None:
    global PASS_COUNT, FAIL_COUNT
    if condition:
        PASS_COUNT += 1
        status = "PASS"
    else:
        FAIL_COUNT += 1
        status = "FAIL"
    line = f"  [{status}] {name}"
    if detail:
        line += f"  ({detail})"
    print(line)


def cube_shift(mu: int) -> np.ndarray:
    sigma_x = np.array([[0, 1], [1, 0]], dtype=complex)
    I2 = np.eye(2, dtype=complex)
    factors = [I2, I2, I2]
    factors[mu] = sigma_x
    return np.kron(np.kron(factors[0], factors[1]), factors[2])


def hadamard_basis(s: tuple) -> np.ndarray:
    psi = np.zeros(8, dtype=complex)
    for alpha in itertools.product([0, 1], repeat=3):
        idx = alpha[0] * 4 + alpha[1] * 2 + alpha[2]
        chi = (s[0] ** alpha[0]) * (s[1] ** alpha[1]) * (s[2] ** alpha[2])
        psi[idx] = chi
    return psi / math.sqrt(8)


# ============================================================================
# Part 1: 8 squarefree monomials + abelian closure
# ============================================================================

def part1_basis() -> list:
    print("\n" + "=" * 72)
    print("PART 1: 8 squarefree monomials form a basis of A_S")
    print("=" * 72)

    S = [cube_shift(mu) for mu in range(3)]

    # Enumerate the 8 squarefree monomials M_T for T ⊆ {1, 2, 3}
    # T = () gives I; T = (1,) gives S_1; etc.
    monomials = {}
    for r in range(4):
        for T in itertools.combinations(range(3), r):
            M = np.eye(8, dtype=complex)
            for i in T:
                M = M @ S[i]
            name = "I" if not T else " ".join(f"S_{i+1}" for i in T)
            monomials[T] = (name, M)

    print(f"\n  Enumerated {len(monomials)} monomials:")
    for T, (name, M) in monomials.items():
        print(f"    T={T!r:14s} → {name}")

    check("Exactly 8 squarefree monomials",
          len(monomials) == 8)

    # Check that they are linearly independent
    # Flatten each to a 64-vector and check the rank of the matrix
    matrix = np.stack([M.reshape(64) for (name, M) in monomials.values()], axis=1)
    rank = np.linalg.matrix_rank(matrix, tol=1e-10)

    check("The 8 monomials are linearly independent in End(C^8)",
          rank == 8,
          f"rank = {rank}")

    # Abelian: each pair commutes
    for T1, T2 in itertools.combinations(monomials.keys(), 2):
        M1 = monomials[T1][1]
        M2 = monomials[T2][1]
        comm = M1 @ M2 - M2 @ M1
        if not np.allclose(comm, 0):
            print(f"    [M_{T1}, M_{T2}] ≠ 0 — UNEXPECTED")
            check(f"[M_{T1}, M_{T2}] = 0", False)

    # Report general abelian property
    check("All 28 pairs of monomials commute (A_S is abelian)",
          all(np.allclose(
              monomials[T1][1] @ monomials[T2][1],
              monomials[T2][1] @ monomials[T1][1]
          ) for T1, T2 in itertools.combinations(monomials.keys(), 2)))

    # Closure: any monomial product is one of the 8 (via S_i² = I)
    # Spot-check: S_1 · S_1 = I, S_1 · S_2 = S_1 S_2, (S_1 S_2) · (S_2 S_3) = S_1 S_3
    check("S_1 · S_1 = I",
          np.allclose(S[0] @ S[0], np.eye(8)))
    check("S_1 · S_2 · S_1 = S_2 (using S_1² = I and commutativity)",
          np.allclose(S[0] @ S[1] @ S[0], S[1]))
    check("(S_1 S_2) · (S_2 S_3) = S_1 S_3",
          np.allclose((S[0] @ S[1]) @ (S[1] @ S[2]), S[0] @ S[2]))

    return list(monomials.values())


# ============================================================================
# Part 2: Diagonal in the Hadamard basis
# ============================================================================

def part2_hadamard_diagonal(monomials: list) -> None:
    print("\n" + "=" * 72)
    print("PART 2: Every M_T is diagonal in the Hadamard basis")
    print("=" * 72)

    all_signs = list(itertools.product([+1, -1], repeat=3))

    # For each monomial M_T, verify M_T |ψ_s⟩ = (∏_{i∈T} s_i) |ψ_s⟩
    for (name, M) in monomials:
        # Figure out which T this is (from name)
        if name == "I":
            T = ()
        else:
            T = tuple(int(token.split("_")[1]) - 1 for token in name.split())

        for s in all_signs:
            psi_s = hadamard_basis(s)
            M_psi = M @ psi_s
            expected_eigenvalue = 1
            for i in T:
                expected_eigenvalue *= s[i]
            expected = expected_eigenvalue * psi_s

            match = np.allclose(M_psi, expected, atol=1e-12)
            if not match:
                check(f"  M_{T} on ψ_{s}: eigenvalue ∏ s_i", False,
                      f"expected {expected_eigenvalue}")
                return

    check("All 8 monomials are diagonal in Hadamard basis with eigenvalues ∏_{i∈T} s_i",
          True,
          "verified for all 8 monomials × 8 Hadamard vectors")


# ============================================================================
# Part 3: A_S is maximal abelian (= all Hadamard-diagonal operators)
# ============================================================================

def part3_maximal_abelian(monomials: list) -> None:
    print("\n" + "=" * 72)
    print("PART 3: A_S coincides with all Hadamard-diagonal operators")
    print("=" * 72)

    # Any operator D that is diagonal in the Hadamard basis acts as
    # D |ψ_s⟩ = d(s) |ψ_s⟩ with d(s) ∈ C. Parameterized by 8 complex
    # numbers (functions on {±1}³ → C). This gives an 8-dim commutative
    # subspace of End(C^8), and it is A_S.

    # Proof: any function d(s) on {±1}³ can be written as a sum of
    # 8 characters χ_T(s) = ∏_{i∈T} s_i for T ⊆ {1,2,3}
    # (discrete Fourier / Hadamard expansion on Z_2³).

    # Verify by constructing a random Hadamard-diagonal operator and
    # expressing it as a linear combination of the 8 monomials.

    rng = np.random.default_rng(42)
    random_d = rng.normal(size=8) + 1j * rng.normal(size=8)

    all_signs = list(itertools.product([+1, -1], repeat=3))

    # Build the random diagonal operator in Hadamard basis
    D = np.zeros((8, 8), dtype=complex)
    Hadamard_basis_vecs = [hadamard_basis(s) for s in all_signs]
    for i, (s, v) in enumerate(zip(all_signs, Hadamard_basis_vecs)):
        D += random_d[i] * np.outer(v, v.conj())

    # Express D as linear combination of the 8 monomials
    # D = Σ_T c_T M_T with c_T = ⟨D, M_T⟩ / ⟨M_T, M_T⟩ in Frobenius inner product
    monomial_matrices = [M for (name, M) in monomials]
    coefficients = []
    for M in monomial_matrices:
        # Frobenius inner product
        c = np.trace(M.conj().T @ D) / np.trace(M.conj().T @ M)
        coefficients.append(c)

    # Reconstruct D from the coefficients
    D_reconstructed = sum(c * M for c, (name, M) in zip(coefficients, monomials))

    check("Random Hadamard-diagonal operator reconstructible from 8 monomials",
          np.allclose(D, D_reconstructed, atol=1e-10),
          f"max |D - D_reco| = {np.max(np.abs(D - D_reconstructed)):.2e}")

    print("\n  Therefore A_S = span{M_T : T ⊆ {1,2,3}} coincides with the")
    print("  algebra of Hadamard-diagonal operators on C^8.")
    print("  This is a maximal abelian subalgebra of End(C^8) (dim 8 =")
    print("  dim of maximal torus in U(8)).")


# ============================================================================
# Part 4: Theorem statement
# ============================================================================

def part4_theorem_statement() -> None:
    print("\n" + "=" * 72)
    print("PART 4: Cube-Shift Polynomial Algebra Theorem (statement)")
    print("=" * 72)

    print("""
  THEOREM. Let S_1, S_2, S_3 be the cube-shift operators on C^8 and
  A_S ⊂ End(C^8) be the associative algebra they generate. Then:

  (1) A_S is abelian (since [S_i, S_j] = 0) and admits a basis of 8
      squarefree monomials:
         { M_T := ∏_{i ∈ T} S_i : T ⊆ {1, 2, 3} }
      (with M_∅ = I). Hence dim_C A_S = 8.

  (2) Higher-degree monomials reduce to squarefree form via S_i² = I.

  (3) In the Hadamard basis {|ψ_s⟩ : s ∈ {±1}³}, each M_T is diagonal
      with eigenvalue
         M_T |ψ_s⟩ = (∏_{i ∈ T} s_i) |ψ_s⟩.
      The map T ↦ (character χ_T: s ↦ ∏_{i∈T} s_i) is a bijection
      between subsets of {1,2,3} and the Z_2³ characters.

  (4) A_S coincides with the full algebra of Hadamard-diagonal
      operators on C^8 (a maximal abelian subalgebra of End(C^8) of
      dimension 8).

  PROOF. All parts by direct computation + Z_2³ character theory.

  QED.

  REUSABILITY.
  - Identifies the "diagonal" (in Hadamard basis) part of End(C^8)
  - Used as a stepping stone: S_3-invariant diagonal operators live
    in a 4-dim subalgebra (next theorem)
  - Foundation for classifying operators that are polynomial in
    the cube-shifts
""")


def main() -> int:
    print("=" * 72)
    print("  Cube-Shift Polynomial Algebra on C^8 (dim 8)")
    print("=" * 72)

    monomials = part1_basis()
    part2_hadamard_diagonal(monomials)
    part3_maximal_abelian(monomials)
    part4_theorem_statement()

    print("\n" + "=" * 72)
    print(f"  TOTAL: PASS={PASS_COUNT}, FAIL={FAIL_COUNT}")
    print("=" * 72)

    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
