#!/usr/bin/env python3
"""
TRANSLATION-EIGENVALUE THEOREM: Translation Operator Eigenvalue Theorem on BZ Corners of Z_L³

Framework object:
  The periodic cubic lattice Z_L³ (L even) with discrete translation
  operators T_μ (μ = 1, 2, 3) acting by T_μ |x⟩ = |x + e_μ⟩.
  The BZ corner states |X_α⟩ are the plane-wave states at momentum
  p_α = π α where α ∈ {0, 1}³:
    |X_α⟩(x) = (1/√L³) exp(i π α · x)

Theorem (TRANSLATION-EIGENVALUE THEOREM):
  (i)   The three translation operators T_1, T_2, T_3 on C^{L³} are
        unitary and pairwise commute.
  (ii)  The BZ corner states {|X_α⟩ : α ∈ {0,1}³} are orthonormal
        (for L even).
  (iii) Each BZ corner state |X_α⟩ is a SIMULTANEOUS eigenstate of all
        three translation operators with eigenvalue
           T_μ |X_α⟩ = (-1)^{α_μ} |X_α⟩

Proof method:
  Direct computation using the discrete plane-wave representation.
  Every step is explicit algebra; no approximations, no bridges.

Reusability:
  Any framework derivation that uses:
  - BZ corner states as translation eigenstates
  - The mapping between cube labels α ∈ {0,1}³ and momentum eigenvalues
  - Selection rules based on translation parity
  - Generation assignments to hw=k BZ corners on Z_L³
  cites this lemma for the translation-eigenvalue fact.

  This is the Z_L³ analog of CUBE-SHIFT JOINT-EIGENSTRUCTURE THEOREM's cube-level statement. Together
  they link the abstract taste cube (C^8) with the physical lattice
  (C^{L³}).

No structural identifications. No imports. Pure math.
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


# ============================================================================
# Setup: construct translation operators and BZ corner states on Z_L³
# ============================================================================

def site_index(x: tuple, L: int) -> int:
    """Map lattice site x = (x_1, x_2, x_3) to a single index in [0, L³)."""
    return ((x[0] % L) * L + (x[1] % L)) * L + (x[2] % L)


def build_translation(mu: int, L: int) -> np.ndarray:
    """
    Construct the discrete translation T_μ on C^{L³} such that
    T_μ |x⟩ = |x + e_μ⟩.

    Matrix form: (T_μ)_{yx} = 1 iff y = x + e_μ (mod L), else 0.
    """
    N = L ** 3
    T = np.zeros((N, N), dtype=complex)
    for x1 in range(L):
        for x2 in range(L):
            for x3 in range(L):
                x = (x1, x2, x3)
                y = list(x)
                y[mu] = (y[mu] + 1) % L
                i_y = site_index(tuple(y), L)
                i_x = site_index(x, L)
                T[i_y, i_x] = 1.0
    return T


def bz_corner_state(alpha: tuple, L: int) -> np.ndarray:
    """
    Construct the BZ corner state |X_α⟩ with α ∈ {0,1}³:
      |X_α⟩(x) = (1/√L³) exp(i π α · x)

    For α_μ ∈ {0,1}, exp(iπ α_μ x_μ) = (-1)^{α_μ x_μ}, so the state
    is real.
    """
    N = L ** 3
    psi = np.zeros(N, dtype=complex)
    for x1 in range(L):
        for x2 in range(L):
            for x3 in range(L):
                x = (x1, x2, x3)
                i = site_index(x, L)
                phase = (-1) ** (alpha[0] * x1) * (-1) ** (alpha[1] * x2) * (-1) ** (alpha[2] * x3)
                psi[i] = phase
    return psi / math.sqrt(N)


# ============================================================================
# Part 1: Translation operators are unitary and commute pairwise
# ============================================================================

def part1_translation_algebra(L: int = 4) -> tuple:
    print("\n" + "=" * 72)
    print(f"PART 1: Translation operators on Z_{L}³ — unitarity and commutativity")
    print("=" * 72)

    T = [build_translation(μ, L) for μ in range(3)]

    for μ in range(3):
        T_μ = T[μ]
        T_μ_dag = T_μ.conj().T
        check(f"T_{μ+1} is unitary (T·T† = I)",
              np.allclose(T_μ @ T_μ_dag, np.eye(L**3)),
              f"max|T·T† − I| = {np.max(np.abs(T_μ @ T_μ_dag - np.eye(L**3))):.2e}")

    for i, j in itertools.combinations(range(3), 2):
        comm = T[i] @ T[j] - T[j] @ T[i]
        check(f"[T_{i+1}, T_{j+1}] = 0",
              np.allclose(comm, 0),
              f"max|comm| = {np.max(np.abs(comm)):.2e}")

    print("\n  Proof:")
    print("  T_μ permutes the L³ lattice sites; each permutation matrix")
    print("  is unitary. Translations in different directions commute")
    print("  because (x + e_i) + e_j = (x + e_j) + e_i on a commutative")
    print("  lattice Z_L³.")

    return T


# ============================================================================
# Part 2: BZ corner orthonormality
# ============================================================================

def part2_orthonormality(L: int = 4) -> list:
    print("\n" + "=" * 72)
    print(f"PART 2: BZ corner orthonormality on Z_{L}³ (L must be even)")
    print("=" * 72)

    if L % 2 != 0:
        print(f"  L = {L} is ODD; orthonormality fails. Using even L.")
        return []

    alphas = list(itertools.product([0, 1], repeat=3))
    corners = [(alpha, bz_corner_state(alpha, L)) for alpha in alphas]

    for (alpha, psi) in corners:
        norm_sq = np.real(np.vdot(psi, psi))
        check(f"|X_{alpha}| = 1",
              abs(norm_sq - 1.0) < 1e-12,
              f"|ψ|² = {norm_sq:.6f}")

    print("\n  Pairwise orthogonality:")
    for (a_i, psi_i), (a_j, psi_j) in itertools.combinations(corners, 2):
        dot = abs(np.vdot(psi_i, psi_j))
        check(f"⟨X_{a_i} | X_{a_j}⟩ = 0",
              dot < 1e-12,
              f"|dot| = {dot:.2e}")

    print("\n  Proof:")
    print("  ⟨X_α | X_β⟩ = (1/L³) Σ_x (-1)^{(α+β)·x}")
    print("             = (1/L³) ∏_μ Σ_{x_μ=0}^{L-1} (-1)^{(α+β)_μ x_μ}")
    print("  Each factor is a geometric series:")
    print("    L   if (α+β)_μ = 0 mod 2   (i.e., α_μ = β_μ)")
    print("    0   if (α+β)_μ = 1 mod 2 and L even")
    print("  So ⟨X_α|X_β⟩ = δ_{α,β} for L even.")

    return corners


# ============================================================================
# Part 3: Translation eigenvalue theorem
# ============================================================================

def part3_eigenvalue_theorem(L: int = 4) -> None:
    print("\n" + "=" * 72)
    print(f"PART 3: Translation eigenvalue theorem T_μ |X_α⟩ = (-1)^{{α_μ}} |X_α⟩")
    print("=" * 72)

    T = [build_translation(μ, L) for μ in range(3)]
    alphas = list(itertools.product([0, 1], repeat=3))

    print("\n  For each BZ corner α ∈ {0,1}³ and each direction μ:")
    for alpha in alphas:
        psi = bz_corner_state(alpha, L)
        for μ in range(3):
            T_μ_psi = T[μ] @ psi
            expected_eigenvalue = (-1) ** alpha[μ]
            expected_vec = expected_eigenvalue * psi
            check(f"  T_{μ+1} |X_{alpha}⟩ = {expected_eigenvalue:+d} |X_{alpha}⟩",
                  np.allclose(T_μ_psi, expected_vec, atol=1e-12),
                  f"|T|X⟩ − λ|X⟩| max = {np.max(np.abs(T_μ_psi - expected_vec)):.2e}")

    print("\n  Proof:")
    print("  (T_μ |X_α⟩)(x) = |X_α⟩(x - e_μ)")
    print("                 = (1/√L³) exp(i π α · (x - e_μ))")
    print("                 = (1/√L³) exp(i π α · x) · exp(-i π α_μ)")
    print("                 = |X_α⟩(x) · (-1)^{α_μ}")
    print("  where we used α_μ ∈ {0,1} so exp(-iπ α_μ) = (-1)^{α_μ}.")


# ============================================================================
# Part 4: Simultaneous eigenbasis (joint-eigenvalue labels)
# ============================================================================

def part4_simultaneous_eigenbasis(L: int = 4) -> None:
    print("\n" + "=" * 72)
    print("PART 4: The 8 BZ corners form a simultaneous eigenbasis of {T_1, T_2, T_3}")
    print("=" * 72)

    alphas = list(itertools.product([0, 1], repeat=3))
    T = [build_translation(μ, L) for μ in range(3)]

    print("\n  Joint eigenvalue tuples (−1)^{α_1}, (−1)^{α_2}, (−1)^{α_3}:")
    eigenvalue_tuples = []
    for alpha in alphas:
        psi = bz_corner_state(alpha, L)
        eigs = tuple(((-1) ** a) for a in alpha)
        eigenvalue_tuples.append(eigs)
        for μ in range(3):
            T_μ_psi = T[μ] @ psi
            assert np.allclose(T_μ_psi, eigs[μ] * psi, atol=1e-12)
        print(f"    X_{alpha} → joint eigenvalues {eigs}")

    # Each sign triple is distinct
    check("8 BZ corners give 8 distinct joint eigenvalue triples",
          len(set(eigenvalue_tuples)) == 8)

    # The 8 BZ corners span the hw ∈ {0,1,2,3} spectrum but are all
    # translation eigenstates
    print("\n  The 8 sign triples exhaust all possible joint eigenvalues in")
    print("  {+1,-1}³, confirming the BZ corners form a complete set of")
    print("  joint eigenstates (for the relevant 8-dimensional subspace of")
    print("  C^{L³} spanned by these corners).")


# ============================================================================
# Part 5: Theorem statement
# ============================================================================

def part5_theorem_statement() -> None:
    print("\n" + "=" * 72)
    print("PART 5: TRANSLATION-EIGENVALUE THEOREM formal statement")
    print("=" * 72)

    print("""
  THEOREM (TRANSLATION-EIGENVALUE THEOREM, Translation Operator Eigenvalue on BZ Corners).
  Let Z_L³ be the periodic cubic lattice with L even. Let T_μ for
  μ = 1, 2, 3 be the discrete translation on C^{L³} defined by
  T_μ |x⟩ = |x + e_μ⟩. Let |X_α⟩ for α ∈ {0,1}³ be the BZ corner state
    |X_α⟩(x) = (1/√L³) exp(i π α · x) = (1/√L³) (−1)^{α · x}.

  Then:

  (1) T_1, T_2, T_3 are unitary and pairwise commute.
  (2) The 8 BZ corner states {|X_α⟩ : α ∈ {0,1}³} are orthonormal.
  (3) Each |X_α⟩ is a simultaneous eigenstate of all three translations:
         T_μ |X_α⟩ = (−1)^{α_μ} |X_α⟩
     so the joint eigenvalue triple is ((−1)^{α_1}, (−1)^{α_2}, (−1)^{α_3}).
  (4) The 8 distinct sign triples in {+1, −1}³ exhaust the joint-eigenvalue
     spectrum, so the 8 BZ corners form a complete simultaneous eigenbasis
     for {T_1, T_2, T_3} on the 8-dim subspace they span.

  PROOF. (1) is standard: translations are site permutations (unitary),
  and they commute on a commutative lattice. (2) follows from discrete
  plane-wave orthogonality on Z_L for L even. (3) by direct computation
  using α_μ ∈ {0,1}: exp(−iπα_μ) = (−1)^{α_μ}. (4) by enumerating
  {+1, −1}³ = 8 distinct triples, matching 8 BZ corners.

  QED.

  REUSABILITY. Cited wherever downstream work refers to:
  - BZ corner states as simultaneous translation eigenstates
  - The α ↔ eigenvalue-triple correspondence
  - Selection rules based on translation parity signatures
""")


def main() -> int:
    print("=" * 72)
    print("  TRANSLATION-EIGENVALUE THEOREM: Translation Eigenvalue Theorem on Z_L³ BZ Corners")
    print("=" * 72)

    L = 4
    T = part1_translation_algebra(L)
    corners = part2_orthonormality(L)
    part3_eigenvalue_theorem(L)
    part4_simultaneous_eigenbasis(L)
    part5_theorem_statement()

    # Additional test: same theorem holds on a larger lattice (L = 6)
    print("\n" + "=" * 72)
    print("PART 6: Lattice-size invariance (same theorem at L = 6)")
    print("=" * 72)
    T6 = [build_translation(μ, 6) for μ in range(3)]
    alpha_test = (1, 0, 1)
    psi6 = bz_corner_state(alpha_test, 6)
    for μ in range(3):
        T_μ_psi = T6[μ] @ psi6
        expected = (-1) ** alpha_test[μ] * psi6
        check(f"  At L=6: T_{μ+1} |X_{alpha_test}⟩ = (-1)^{{{alpha_test[μ]}}} |X⟩",
              np.allclose(T_μ_psi, expected, atol=1e-12))

    print("\n" + "=" * 72)
    print(f"  TOTAL: PASS={PASS_COUNT}, FAIL={FAIL_COUNT}")
    print("=" * 72)

    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
