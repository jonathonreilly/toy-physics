#!/usr/bin/env python3
"""
Hadamard Basis: Simultaneous Eigenbasis of T_μ + S_3 Label-Permutation Action

Framework objects:
  - Taste cube C^8 = (C²)⊗³ with Hadamard basis |ψ_s⟩ for s ∈ {±1}³
    (Cube-Shift Joint-Eigenstructure Theorem).
  - On Z_L³ BZ-corner subspace via Φ: |ψ_s⟩ ↦ |ψ_s^lattice⟩
    (Site-Phase / Cube-Shift Intertwiner Theorem).
  - S_3 axis-permutation action on C^8 (S_3 Taste-Cube Decomposition).
  - Hw-parity projectors Π_± = (1 ± T_1 T_2 T_3)/2 (Hamming-Weight
    Parity Conservation Theorem).

Theorem:
  (i)   The Hadamard basis simultaneously diagonalizes T_1, T_2, T_3
        on the BZ-corner subspace. Specifically,
           T_μ |ψ_s^lattice⟩ = s_μ |ψ_s^lattice⟩.
  (ii)  Hence T_1 T_2 T_3 has eigenvalue s_1 s_2 s_3 on |ψ_s^lattice⟩.
  (iii) The hw-parity projectors Π_± diagonalize in the Hadamard basis:
           Π_+ = Σ_{s: s_1 s_2 s_3 = +1} |ψ_s^lattice⟩ ⟨ψ_s^lattice|
           Π_- = Σ_{s: s_1 s_2 s_3 = -1} |ψ_s^lattice⟩ ⟨ψ_s^lattice|
        Each sum has exactly 4 terms (so each Π_± has rank 4).
  (iv)  S_3 acts on the Hadamard basis as a label permutation:
           U(π) |ψ_s⟩ = |ψ_{π·s}⟩
        where (π · s)_μ = s_{π^{-1}(μ)}.
  (v)   Consequently, S_3 preserves the hw-parity decomposition:
        the sign-product s_1 s_2 s_3 is S_3-invariant (invariant under
        permutations of the factors), so S_3 maps each hw-parity subspace
        to itself.

Proof method: direct algebra using the Hadamard formula + the individual
Batch 1 and Batch 2 theorems.

Reusability:
  - Block-diagonalizes hw-parity-preserving operators in a canonical
    orthonormal basis
  - Makes S_3 symmetry manifest as label permutation (useful for
    symmetry-based calculations)
  - Connects the abstract-cube picture (C^8) and the lattice picture
    (C^{L³}) in a way that respects both S_3 and hw-parity
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
# Setup
# ============================================================================

def hadamard_basis_c8(s: tuple) -> np.ndarray:
    """|ψ_s⟩ on C^8 with signs s = (s_1, s_2, s_3) ∈ {±1}³."""
    psi = np.zeros(8, dtype=complex)
    for alpha in itertools.product([0, 1], repeat=3):
        idx = alpha[0] * 4 + alpha[1] * 2 + alpha[2]
        chi = (s[0] ** alpha[0]) * (s[1] ** alpha[1]) * (s[2] ** alpha[2])
        psi[idx] = chi
    return psi / math.sqrt(8)


def cube_shift(mu: int) -> np.ndarray:
    sigma_x = np.array([[0, 1], [1, 0]], dtype=complex)
    I2 = np.eye(2, dtype=complex)
    factors = [I2, I2, I2]
    factors[mu] = sigma_x
    return np.kron(np.kron(factors[0], factors[1]), factors[2])


def S3_unitary(perm: tuple) -> np.ndarray:
    perm_inv = [0, 0, 0]
    for i, pi_i in enumerate(perm):
        perm_inv[pi_i] = i
    U = np.zeros((8, 8), dtype=complex)
    for alpha in itertools.product([0, 1], repeat=3):
        new_alpha = tuple(alpha[perm_inv[i]] for i in range(3))
        idx_alpha = alpha[0] * 4 + alpha[1] * 2 + alpha[2]
        idx_new = new_alpha[0] * 4 + new_alpha[1] * 2 + new_alpha[2]
        U[idx_new, idx_alpha] = 1
    return U


# ============================================================================
# Part 1: Hadamard basis diagonalizes cube-shifts S_μ
# ============================================================================

def part1_hadamard_diagonalizes() -> None:
    print("\n" + "=" * 72)
    print("PART 1: Hadamard basis diagonalizes S_μ (and hence T_μ on BZ)")
    print("=" * 72)

    all_signs = list(itertools.product([+1, -1], repeat=3))
    S = [cube_shift(mu) for mu in range(3)]

    for s in all_signs:
        psi = hadamard_basis_c8(s)
        for mu in range(3):
            Sp = S[mu] @ psi
            expected = s[mu] * psi
            check(f"  S_{mu+1} |ψ_{s}⟩ = {s[mu]:+d} |ψ_{s}⟩",
                  np.allclose(Sp, expected, atol=1e-12))

    print("\n  By Site-Phase / Cube-Shift Intertwiner Theorem, this transfers")
    print("  to the BZ-corner subspace: T_μ |ψ_s^lattice⟩ = s_μ |ψ_s^lattice⟩.")


# ============================================================================
# Part 2: Hw-parity projectors in Hadamard basis
# ============================================================================

def part2_hw_parity_in_hadamard() -> None:
    print("\n" + "=" * 72)
    print("PART 2: Hw-parity projectors in Hadamard basis")
    print("=" * 72)

    all_signs = list(itertools.product([+1, -1], repeat=3))

    # The hw-parity operator on C^8 (abstract cube): S_1 S_2 S_3
    S = [cube_shift(mu) for mu in range(3)]
    Q = S[0] @ S[1] @ S[2]

    # Verify eigenvalue on each Hadamard vector
    plus_eigenvectors = []
    minus_eigenvectors = []
    for s in all_signs:
        psi = hadamard_basis_c8(s)
        eigenvalue = s[0] * s[1] * s[2]
        Qp = Q @ psi
        check(f"  (S_1 S_2 S_3) |ψ_{s}⟩ = {eigenvalue:+d} |ψ_{s}⟩",
              np.allclose(Qp, eigenvalue * psi, atol=1e-12))
        if eigenvalue == +1:
            plus_eigenvectors.append(s)
        else:
            minus_eigenvectors.append(s)

    check("Exactly 4 Hadamard vectors with s_1 s_2 s_3 = +1",
          len(plus_eigenvectors) == 4,
          f"found {len(plus_eigenvectors)}")
    check("Exactly 4 Hadamard vectors with s_1 s_2 s_3 = -1",
          len(minus_eigenvectors) == 4,
          f"found {len(minus_eigenvectors)}")

    print(f"\n  + eigenspace (rank 4): s ∈ {plus_eigenvectors}")
    print(f"  − eigenspace (rank 4): s ∈ {minus_eigenvectors}")

    # Build projectors explicitly
    Pi_plus = sum(np.outer(hadamard_basis_c8(s), hadamard_basis_c8(s).conj())
                  for s in plus_eigenvectors)
    Pi_minus = sum(np.outer(hadamard_basis_c8(s), hadamard_basis_c8(s).conj())
                   for s in minus_eigenvectors)

    check("Π_+ + Π_- = I (completeness)",
          np.allclose(Pi_plus + Pi_minus, np.eye(8)))
    check("Π_+ has rank 4",
          np.linalg.matrix_rank(Pi_plus) == 4)
    check("Π_- has rank 4",
          np.linalg.matrix_rank(Pi_minus) == 4)

    # Verify Π_+ = (1 + Q)/2 and Π_- = (1 − Q)/2
    check("Π_+ = (1 + S_1 S_2 S_3) / 2",
          np.allclose(Pi_plus, (np.eye(8) + Q) / 2))
    check("Π_- = (1 − S_1 S_2 S_3) / 2",
          np.allclose(Pi_minus, (np.eye(8) - Q) / 2))


# ============================================================================
# Part 3: S_3 acts on Hadamard basis as label permutation
# ============================================================================

def part3_s3_on_hadamard() -> None:
    print("\n" + "=" * 72)
    print("PART 3: S_3 action on Hadamard basis: U(π) |ψ_s⟩ = |ψ_{π·s}⟩")
    print("=" * 72)

    all_signs = list(itertools.product([+1, -1], repeat=3))
    S3_elements = {
        "e":       (0, 1, 2),
        "(12)":    (1, 0, 2),
        "(23)":    (0, 2, 1),
        "(13)":    (2, 1, 0),
        "(123)":   (1, 2, 0),
        "(132)":   (2, 0, 1),
    }

    for name, perm in S3_elements.items():
        U = S3_unitary(perm)
        for s in all_signs:
            psi_s = hadamard_basis_c8(s)
            Upsi = U @ psi_s

            # Compute π · s
            perm_inv = [0, 0, 0]
            for i, pi_i in enumerate(perm):
                perm_inv[pi_i] = i
            pi_s = tuple(s[perm_inv[mu]] for mu in range(3))

            psi_pi_s = hadamard_basis_c8(pi_s)

            check(f"  U({name}) |ψ_{s}⟩ = |ψ_{pi_s}⟩",
                  np.allclose(Upsi, psi_pi_s, atol=1e-12),
                  f"match {'✓' if np.allclose(Upsi, psi_pi_s, atol=1e-12) else '✗'}")


# ============================================================================
# Part 4: S_3 preserves hw-parity (since s_1 s_2 s_3 is S_3-invariant)
# ============================================================================

def part4_s3_preserves_hw_parity() -> None:
    print("\n" + "=" * 72)
    print("PART 4: S_3 preserves hw-parity decomposition")
    print("=" * 72)

    all_signs = list(itertools.product([+1, -1], repeat=3))
    S3_elements = {
        "e":     (0, 1, 2),
        "(12)":  (1, 0, 2),
        "(123)": (1, 2, 0),
    }  # spot-check three elements representing each conjugacy class

    # S_3 permutes the labels s, but the product s_1 s_2 s_3 is invariant
    # under permutations of factors.
    for name, perm in S3_elements.items():
        perm_inv = [0, 0, 0]
        for i, pi_i in enumerate(perm):
            perm_inv[pi_i] = i
        for s in all_signs:
            pi_s = tuple(s[perm_inv[mu]] for mu in range(3))
            product_original = s[0] * s[1] * s[2]
            product_permuted = pi_s[0] * pi_s[1] * pi_s[2]
            check(f"  s_1 s_2 s_3 invariant under U({name}) for s={s}",
                  product_original == product_permuted)

    # Verify: Π_+ commutes with each U(π)
    S = [cube_shift(mu) for mu in range(3)]
    Q = S[0] @ S[1] @ S[2]
    Pi_plus = (np.eye(8) + Q) / 2
    Pi_minus = (np.eye(8) - Q) / 2

    for name, perm in S3_elements.items():
        U = S3_unitary(perm)
        check(f"  [U({name}), Π_+] = 0 (S_3 preserves + subspace)",
              np.allclose(U @ Pi_plus - Pi_plus @ U, 0, atol=1e-12))
        check(f"  [U({name}), Π_-] = 0 (S_3 preserves − subspace)",
              np.allclose(U @ Pi_minus - Pi_minus @ U, 0, atol=1e-12))


# ============================================================================
# Part 5: Theorem statement
# ============================================================================

def part5_theorem_statement() -> None:
    print("\n" + "=" * 72)
    print("PART 5: Theorem statement")
    print("=" * 72)

    print("""
  THEOREM (Hadamard Basis: Simultaneous T_μ Eigenbasis + S_3 Label-
  Permutation Action).

  Let |ψ_s⟩ = (1/√8) Σ_{α∈{0,1}³} (∏_μ s_μ^{α_μ}) |α⟩ for s ∈ {±1}³
  be the Hadamard basis of C^8 = (C²)⊗³. Let |ψ_s^lattice⟩ be its
  image under the BZ-corner intertwiner Φ on Z_L³. Then:

  (1) Each cube-shift S_μ acts diagonally in the Hadamard basis:
         S_μ |ψ_s⟩ = s_μ |ψ_s⟩.
      By the Site-Phase / Cube-Shift Intertwiner Theorem, this
      transfers to the translation T_μ on BZ corners:
         T_μ |ψ_s^lattice⟩ = s_μ |ψ_s^lattice⟩.

  (2) The hw-parity operator Q = S_1 S_2 S_3 (on C^8) or T_1 T_2 T_3
      (on BZ corners) has eigenvalue s_1 s_2 s_3 ∈ {±1} on |ψ_s⟩ or
      |ψ_s^lattice⟩ respectively. The hw-parity projectors
         Π_± = (1 ± Q) / 2
      have rank 4 and project onto the span of the 4 Hadamard vectors
      with s_1 s_2 s_3 = ±1 respectively.

  (3) S_3 acts on the Hadamard basis by permutation of the sign labels:
         U(π) |ψ_s⟩ = |ψ_{π · s}⟩,     (π · s)_μ = s_{π^{-1}(μ)}.

  (4) Because the product s_1 s_2 s_3 is invariant under permutations
      of the factors, S_3 preserves the hw-parity decomposition:
         U(π) Π_± U(π)^† = Π_±   for all π ∈ S_3.

  PROOF. (1) and (2) by direct substitution from the Hadamard formula
  and Cube-Shift Joint-Eigenstructure Theorem. (3) by direct
  computation: U(π) acting on the Hadamard formula relabels the α
  indices by π, which by substitution of variables relabels the signs
  s by π. (4) because the product s_1 s_2 s_3 is a symmetric polynomial
  in the s_μ, hence invariant under any permutation.

  QED.

  REUSABILITY. Composes directly with:
  - S_3-Invariant Operator Dimension Theorem: S_3-invariants block-
    diagonalize on the ± hw-parity subspaces, each of which further
    decomposes under S_3 into smaller irreps.
  - Hw-parity Conservation Theorem: the ± eigenspace is the direct
    target of any even-order site-phase polynomial.
  - Cube-Shift Joint-Eigenstructure Theorem: this is its T_μ / BZ-
    corner counterpart.

  Bridges Batch 1 (Hadamard / intertwiner) and Batch 2 (S_3 /
  hw-parity) into a unified block-diagonalization picture.
""")


def main() -> int:
    print("=" * 72)
    print("  Hadamard basis: simultaneous T_μ eigenbasis + S_3 label action")
    print("=" * 72)

    part1_hadamard_diagonalizes()
    part2_hw_parity_in_hadamard()
    part3_s3_on_hadamard()
    part4_s3_preserves_hw_parity()
    part5_theorem_statement()

    print("\n" + "=" * 72)
    print(f"  TOTAL: PASS={PASS_COUNT}, FAIL={FAIL_COUNT}")
    print("=" * 72)

    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
