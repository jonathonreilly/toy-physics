#!/usr/bin/env python3
"""
Dimension of the S_3-Invariant Operator Algebra on C^8

Framework object:
  The taste cube C^8 = (C²)⊗³ with S_3 axis-permutation action (as
  defined in S3_TASTE_CUBE_DECOMPOSITION_NOTE). The space of
  S_3-invariant linear operators is End(C^8)^{S_3}.

Theorem:
  (i)   dim_C End(C^8)^{S_3} = 20.
  (ii)  This follows from Schur's lemma applied to the decomposition
        C^8 ≅ 4·A_1 ⊕ 2·E and the irrep block structure of End:
            dim End(V)^G = Σ_irrep m_irrep²
        where m_irrep is the multiplicity of the irrep in V.
        For V = 4·A_1 ⊕ 0·A_2 ⊕ 2·E: dim = 4² + 0² + 2² = 20.
  (iii) Explicit basis: the 20 S_3-invariant operators decompose as
            - 16 operators within the 4-copy A_1 block (arbitrary 4×4
              matrix on the A_1 multiplicity space)
            - 4 operators within the 2-copy E block (arbitrary 2×2
              matrix on the E multiplicity space, tensored with
              identity on the 2-dim E irrep).

Proof method:
  Schur's lemma + explicit construction of an S_3-invariant basis +
  numerical verification by averaging over the group.

Reusability:
  - Classifies which operators on C^8 can be S_3-symmetric
  - Used in constructing S_3-invariant Hamiltonians, Yukawa matrices,
    CP-even operators in the framework
  - Constrains framework claims that invoke S_3 symmetry: any such
    claim lives in the 20-dim algebra
"""

from __future__ import annotations

import itertools
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
# S_3 unitaries (from Batch 2's S_3 decomposition theorem)
# ============================================================================

def basis_index(alpha: tuple) -> int:
    return alpha[0] * 4 + alpha[1] * 2 + alpha[2]


S3_elements = {
    "e":       (0, 1, 2),
    "(12)":    (1, 0, 2),
    "(23)":    (0, 2, 1),
    "(13)":    (2, 1, 0),
    "(123)":   (1, 2, 0),
    "(132)":   (2, 0, 1),
}


def build_S3_unitary(perm: tuple) -> np.ndarray:
    perm_inv = [0, 0, 0]
    for i, pi_i in enumerate(perm):
        perm_inv[pi_i] = i
    U = np.zeros((8, 8), dtype=complex)
    for alpha in itertools.product([0, 1], repeat=3):
        new_alpha = tuple(alpha[perm_inv[i]] for i in range(3))
        U[basis_index(new_alpha), basis_index(alpha)] = 1
    return U


# ============================================================================
# Part 1: S_3-invariance via group-averaging projector
# ============================================================================

def s3_invariant_projector() -> np.ndarray:
    """
    The projector onto the S_3-invariant subspace of End(C^8) ≅ C^{64}.
    An operator X is S_3-invariant iff U(π) X U(π)^† = X for all π.
    The projector is the group average:
        P_inv(X) = (1/|S_3|) Σ_π U(π) X U(π)^†.

    Represented as a linear map on vec(X) ∈ C^{64} via
        vec(U X U^†) = (U ⊗ U^*) vec(X).
    """
    Us = {name: build_S3_unitary(perm) for name, perm in S3_elements.items()}

    P = np.zeros((64, 64), dtype=complex)
    for name, U in Us.items():
        # Conjugation X ↦ U X U^† corresponds on vec to (U ⊗ U^conj) vec(X)... carefully
        # If we use column-major vec: vec(U X V^T) = (V ⊗ U) vec(X).
        # For X ↦ U X U^†: vec(U X U^†) = (U^conj ⊗ U) vec(X)  [column-major]
        # We'll use numpy reshape which is row-major.
        # Simpler: build P as the matrix representation of the action.
        for i, j in itertools.product(range(8), repeat=2):
            # Basis vector: E_{ij} with 1 at (i, j).
            E_ij = np.zeros((8, 8), dtype=complex)
            E_ij[i, j] = 1.0
            UEU = U @ E_ij @ U.conj().T
            # Flatten to 64-vector (row-major)
            P[:, i * 8 + j] += UEU.reshape(64) / len(Us)

    return P


def part1_invariant_dimension() -> None:
    print("\n" + "=" * 72)
    print("PART 1: dim End(C^8)^{S_3} via group-averaging projector")
    print("=" * 72)

    P = s3_invariant_projector()

    # P should be a projector: P² = P
    check("Group-average P is idempotent (P² = P)",
          np.allclose(P @ P, P, atol=1e-10))

    check("P is Hermitian",
          np.allclose(P, P.conj().T, atol=1e-10))

    # Dimension of invariant subspace = rank(P) = trace(P)
    trace_P = np.real(np.trace(P))
    rank_P = np.linalg.matrix_rank(P)

    print(f"\n  Trace of P = {trace_P:.4f}")
    print(f"  Rank of P = {rank_P}")

    check("dim End(C^8)^{S_3} = 20",
          abs(trace_P - 20) < 1e-10,
          f"trace = {trace_P}")
    check("rank equals trace (projector property)",
          rank_P == 20)


# ============================================================================
# Part 2: Schur's lemma verification via multiplicity formula
# ============================================================================

def part2_schur_formula() -> None:
    print("\n" + "=" * 72)
    print("PART 2: Schur's lemma — dim End(V)^G = Σ m_irrep²")
    print("=" * 72)

    # From S3_TASTE_CUBE_DECOMPOSITION: V = 4·A_1 ⊕ 0·A_2 ⊕ 2·E
    m = {"A_1": 4, "A_2": 0, "E": 2}

    dim_sq_sum = m["A_1"] ** 2 + m["A_2"] ** 2 + m["E"] ** 2
    print(f"\n  Multiplicities:  m(A_1) = {m['A_1']}, m(A_2) = {m['A_2']}, m(E) = {m['E']}")
    print(f"  Sum of squares:  {m['A_1']}² + {m['A_2']}² + {m['E']}² = {dim_sq_sum}")

    check("Σ m_irrep² = 16 + 0 + 4 = 20",
          dim_sq_sum == 20,
          f"sum = {dim_sq_sum}")

    print("\n  Proof (Schur's lemma):")
    print("  End(⊕_r m_r · V_r)^G = ⊕_r End(C^{m_r}) ⊗ id_{V_r},")
    print("  so dim = Σ_r m_r². For V = 4·A_1 + 2·E: dim = 4² + 2² = 20.")


# ============================================================================
# Part 3: Explicit invariant basis — enumerate 20 independent operators
# ============================================================================

def part3_invariant_basis() -> None:
    print("\n" + "=" * 72)
    print("PART 3: 20 independent S_3-invariant operators")
    print("=" * 72)

    P = s3_invariant_projector()

    # Extract an orthonormal basis of the invariant subspace (rank 20)
    eigenvalues, eigenvectors = np.linalg.eigh(P)
    # Sort by eigenvalue descending
    idx = np.argsort(-eigenvalues.real)
    eigenvalues = eigenvalues[idx]
    eigenvectors = eigenvectors[:, idx]

    # Count eigenvectors with eigenvalue ≈ 1
    invariant_count = int(np.sum(np.abs(eigenvalues - 1.0) < 1e-10))

    check("20 eigenvectors of P with eigenvalue 1 (S_3-invariant)",
          invariant_count == 20,
          f"count = {invariant_count}")

    # Check that the first 20 eigenvectors give genuine S_3-invariant operators
    Us = {name: build_S3_unitary(perm) for name, perm in S3_elements.items()}

    # Take the first (random) eigenvector and reshape to an 8x8 matrix
    # Verify S_3-invariance
    for k in range(min(invariant_count, 5)):  # spot-check first 5
        v = eigenvectors[:, k]
        X = v.reshape(8, 8)

        for name, U in Us.items():
            UXU = U @ X @ U.conj().T
            invariant = np.allclose(UXU, X, atol=1e-10)
            if not invariant:
                print(f"    eigenvector {k} under U({name}): NOT invariant")
                check(f"eigenvector {k} invariant under U({name})", False)
                break
        else:
            continue
        break
    else:
        # All spot-check eigenvectors pass
        check("Spot-check: first 5 eigenvectors of P are S_3-invariant operators",
              True)


# ============================================================================
# Part 4: Identify examples of S_3-invariant operators
# ============================================================================

def part4_canonical_examples() -> None:
    print("\n" + "=" * 72)
    print("PART 4: Canonical S_3-invariant operators (sanity examples)")
    print("=" * 72)

    I_8 = np.eye(8, dtype=complex)
    Us = {name: build_S3_unitary(perm) for name, perm in S3_elements.items()}

    # Identity is S_3-invariant
    check("Identity I_8 is S_3-invariant",
          all(np.allclose(U @ I_8 @ U.conj().T, I_8) for U in Us.values()))

    # Sum of cube-shifts: S_1 + S_2 + S_3 is S_3-invariant
    sigma_x = np.array([[0, 1], [1, 0]], dtype=complex)
    I2 = np.eye(2, dtype=complex)
    S_1 = np.kron(np.kron(sigma_x, I2), I2)
    S_2 = np.kron(np.kron(I2, sigma_x), I2)
    S_3 = np.kron(np.kron(I2, I2), sigma_x)

    S_sum = S_1 + S_2 + S_3
    check("S_1 + S_2 + S_3 is S_3-invariant",
          all(np.allclose(U @ S_sum @ U.conj().T, S_sum, atol=1e-10) for U in Us.values()))

    # Product S_1 S_2 S_3 is S_3-invariant (since S_3 permutes them and the product
    # is a commuting product, it's invariant under conjugation which permutes factors)
    S_prod = S_1 @ S_2 @ S_3
    check("S_1 S_2 S_3 is S_3-invariant",
          all(np.allclose(U @ S_prod @ U.conj().T, S_prod, atol=1e-10) for U in Us.values()))

    # Hamming-weight projectors: S_3 preserves hw (from Batch 2 theorem)
    P_hw = [np.zeros((8, 8), dtype=complex) for _ in range(4)]
    for alpha in itertools.product([0, 1], repeat=3):
        hw = sum(alpha)
        idx = basis_index(alpha)
        P_hw[hw][idx, idx] = 1
    for hw in range(4):
        check(f"hw={hw} projector is S_3-invariant",
              all(np.allclose(U @ P_hw[hw] @ U.conj().T, P_hw[hw], atol=1e-10) for U in Us.values()))


# ============================================================================
# Part 5: Theorem statement
# ============================================================================

def part5_theorem_statement() -> None:
    print("\n" + "=" * 72)
    print("PART 5: S_3-Invariant Operator Dimension Theorem (statement)")
    print("=" * 72)

    print("""
  THEOREM. Let C^8 = (C²)⊗³ carry the S_3 representation by
  tensor-position permutations. Then:

  (1) dim_C End(C^8)^{S_3} = 20.

  (2) This follows from Schur's lemma: for V = ⊕_r m_r · V_r,
         dim End(V)^G = Σ_r m_r².
      Here V = 4·A_1 ⊕ 2·E (from S_3 Taste-Cube Decomposition),
      so dim = 4² + 2² = 20.

  (3) Explicit canonical examples in this 20-dim algebra:
      - Identity I_8
      - S_1 + S_2 + S_3 (sum of cube-shifts)
      - S_1 S_2 S_3 (product of cube-shifts)
      - Each Hamming-weight projector P_hw (for hw = 0, 1, 2, 3)
      - Arbitrary polynomials in the above
      - An orthonormal basis of 20 operators can be extracted from the
        group-averaging projector P = (1/|S_3|) Σ_π U(π) ⊗ U(π)^*.

  (4) As a consequence, the space of S_3-invariant Hermitian operators
      on C^8 is real 20-dim (since Hermiticity + S_3-invariance are
      compatible conditions on a complex 20-dim space).

  PROOF. Schur's lemma + the S_3 Taste-Cube Decomposition theorem.
  Group-averaging projector P has rank 20 (verified numerically),
  equivalently trace 20.

  QED.

  REUSABILITY. Used in:
  - classifying S_3-invariant Hamiltonians, mass matrices, Yukawa
    structures
  - deriving operator basis expansions for specific framework
    observables that preserve axis symmetry
  - constraining framework claims that invoke S_3 invariance:
    any such observable lives in this 20-dim algebra
""")


def main() -> int:
    print("=" * 72)
    print("  S_3-Invariant Operator Algebra on C^8: dim = 20")
    print("=" * 72)

    part1_invariant_dimension()
    part2_schur_formula()
    part3_invariant_basis()
    part4_canonical_examples()
    part5_theorem_statement()

    print("\n" + "=" * 72)
    print(f"  TOTAL: PASS={PASS_COUNT}, FAIL={FAIL_COUNT}")
    print("=" * 72)

    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
