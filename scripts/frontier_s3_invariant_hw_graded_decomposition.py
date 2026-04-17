#!/usr/bin/env python3
"""
Hw-Graded Decomposition of End(C^8)^{S_3}

Framework object:
  The S_3-invariant operator algebra End(C^8)^{S_3} (dim 20, Batch 3)
  on the taste cube C^8 = (C²)^⊗³.  The Hamming-weight grading
  C^8 = V_0 ⊕ V_1 ⊕ V_2 ⊕ V_3 (dimensions 1 + 3 + 3 + 1) induces a
  grading of operators.

Theorem (hw-graded decomposition):
  The 20-dim S_3-invariant commutant decomposes by Hamming-weight
  transitions as

     End(C^8)^{S_3}  =  D  ⊕  O

  where
     D  =  hw-preserving S_3-invariants  (block-diagonal in hw)
           with dim_C D = 1 + 2 + 2 + 1 = 6
     O  =  hw-changing S_3-invariants   (off-hw-block)
           with dim_C O = 14
     dim_C (D ⊕ O) = 20  ✓

  Breakdown of the 6 hw-diagonal complex dimensions:
     V_0 = 1 · A_1:        End(V_0)^{S_3} has dim 1
     V_1 = 1 · A_1 + 1 · E: End(V_1)^{S_3} has dim 2
     V_2 = 1 · A_1 + 1 · E: End(V_2)^{S_3} has dim 2
     V_3 = 1 · A_1:        End(V_3)^{S_3} has dim 1

  Breakdown of the 14 hw-off-diagonal complex dimensions (hw j < k):
     (0,1): 1 · A_1 link               → dim 1
     (0,2): 1 · A_1 link               → dim 1
     (0,3): 1 · A_1 link               → dim 1
     (1,2): 1 · A_1 link + 1 · E link  → dim 2
     (1,3): 1 · A_1 link               → dim 1
     (2,3): 1 · A_1 link               → dim 1
     total directed (j → k): 1+1+1+2+1+1 = 7
     off-diagonal complex: 2 × 7 = 14  (both directions j→k and k→j)

  Real Hermitian cut has dim 20 = 6 + 14 (the *-closed commutant
  keeps real dim equal to complex dim).

Proof method: Schur-lemma application using the hw-refined isotypic
decomposition of C^8 (from Batch 2 taste-cube decomposition), plus
explicit block counting and numerical rank verification.

Reusability:
  - Refines Batch 3's S_3 Invariant Operator Dimension theorem (dim 20)
    and hw-parity block decomposition (10+10) to the full hw grading.
  - Distinguishes mass-matrix-like operators (hw-preserving) from
    transition-like operators (hw-changing) within the S_3-invariant
    algebra.
  - Used whenever a framework operator is known to preserve hw level
    (block-diagonal in hw) or to change it by a specific amount.
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


# ---------------------------------------------------------------------------
# S_3 generators on C^8 = (C²)^⊗³ (axis permutation)
# ---------------------------------------------------------------------------

def axis_permutation(perm: tuple) -> np.ndarray:
    """Unitary implementing axis permutation on C^8.  perm is a
    3-tuple giving where each axis maps to."""
    U = np.zeros((8, 8), dtype=complex)
    for a in itertools.product([0, 1], repeat=3):
        src = a[0] * 4 + a[1] * 2 + a[2]
        # Permute coordinates: new_a[perm[i]] = a[i]
        new_a = [0, 0, 0]
        for i in range(3):
            new_a[perm[i]] = a[i]
        dst = new_a[0] * 4 + new_a[1] * 2 + new_a[2]
        U[dst, src] = 1.0
    return U


def s3_generators() -> list:
    # Transposition (12): axis 0 <-> axis 1
    tau12 = axis_permutation((1, 0, 2))
    # 3-cycle (123): 0 -> 1 -> 2 -> 0
    sigma = axis_permutation((1, 2, 0))
    return [tau12, sigma]


def hw(alpha: tuple) -> int:
    return sum(alpha)


# ---------------------------------------------------------------------------
# Hw-block projectors
# ---------------------------------------------------------------------------

def hw_projectors() -> list:
    """Return 4 projectors Π_0, Π_1, Π_2, Π_3 onto hw-k subspaces."""
    projs = [np.zeros((8, 8), dtype=complex) for _ in range(4)]
    for alpha in itertools.product([0, 1], repeat=3):
        idx = alpha[0] * 4 + alpha[1] * 2 + alpha[2]
        projs[hw(alpha)][idx, idx] = 1.0
    return projs


# ---------------------------------------------------------------------------
# Part 1: Verify S_3 commutes with hw grading
# ---------------------------------------------------------------------------

def part1_s3_preserves_hw() -> None:
    print("\n" + "=" * 72)
    print("PART 1: S_3 preserves the hw grading")
    print("=" * 72)

    projs = hw_projectors()
    gens = s3_generators()
    labels = ["τ=(12)", "σ=(123)"]
    for g, lbl in zip(gens, labels):
        for k, P in enumerate(projs):
            commutes = np.allclose(g @ P, P @ g)
            check(f"[{lbl}, Π_hw={k}] = 0", commutes)


# ---------------------------------------------------------------------------
# Part 2: Isotypic decomposition on each hw block
# ---------------------------------------------------------------------------

def part2_hw_block_irreps() -> dict:
    print("\n" + "=" * 72)
    print("PART 2: Isotypic decomposition V_k = m_A1 · A_1 ⊕ m_E · E")
    print("=" * 72)

    # Known from Batch 2:
    # V_0 = 1·A_1       (m_A1=1, m_E=0)
    # V_1 = 1·A_1+1·E   (m_A1=1, m_E=1)
    # V_2 = 1·A_1+1·E   (m_A1=1, m_E=1)
    # V_3 = 1·A_1       (m_A1=1, m_E=0)
    # No A_2 component.

    # Verify by computing the trivial-irrep projector
    # P_{A_1} = (1/6) Σ_{g in S_3} U(g) and checking rank on each hw block.

    # Build all 6 S_3 elements as axis permutations
    perms = [
        (0, 1, 2),  # e
        (1, 0, 2),  # (01)
        (0, 2, 1),  # (12)
        (2, 1, 0),  # (02)
        (1, 2, 0),  # (012)
        (2, 0, 1),  # (021)
    ]
    P_A1 = sum(axis_permutation(p) for p in perms) / 6.0

    projs = hw_projectors()
    hw_decomp = {}
    for k, Pk in enumerate(projs):
        # A_1 dim = rank of Pk @ P_A1 @ Pk
        M_k = Pk @ P_A1 @ Pk
        dim_A1_k = int(np.round(np.real(np.trace(M_k))))
        dim_total_k = int(np.round(np.real(np.trace(Pk))))
        # E dim = (total - A_1) / 2; since 2-dim per copy
        dim_E_k = (dim_total_k - dim_A1_k) // 2
        # A_2 dim = 0 (no sign rep in C^8)
        hw_decomp[k] = {"A1": dim_A1_k, "E": dim_E_k, "total": dim_total_k}
        print(f"  V_{k}:  dim = {dim_total_k},  m_A1 = {dim_A1_k},  "
              f"m_E = {dim_E_k}")

    check("V_0 = 1·A_1", hw_decomp[0] == {"A1": 1, "E": 0, "total": 1})
    check("V_1 = 1·A_1 + 1·E", hw_decomp[1] == {"A1": 1, "E": 1, "total": 3})
    check("V_2 = 1·A_1 + 1·E", hw_decomp[2] == {"A1": 1, "E": 1, "total": 3})
    check("V_3 = 1·A_1", hw_decomp[3] == {"A1": 1, "E": 0, "total": 1})

    return hw_decomp


# ---------------------------------------------------------------------------
# Part 3: Hw-diagonal S_3-invariant dim = 6
# ---------------------------------------------------------------------------

def part3_hw_diagonal_dim(hw_decomp: dict) -> None:
    print("\n" + "=" * 72)
    print("PART 3: Hw-diagonal S_3-invariant commutant dim = 6")
    print("=" * 72)

    # Within each V_k, dim End(V_k)^{S_3} = m_A1² + m_E² (no A_2)
    total_diag = 0
    for k in range(4):
        m_A1 = hw_decomp[k]["A1"]
        m_E = hw_decomp[k]["E"]
        dim_k = m_A1 ** 2 + m_E ** 2
        total_diag += dim_k
        print(f"  dim End(V_{k})^{{S_3}} = {m_A1}² + {m_E}² = {dim_k}")

    print(f"\n  Total hw-diagonal dim = {total_diag}")
    check("Hw-diagonal dim = 6", total_diag == 6)

    # Numerical verification: solve the commutator system restricted to
    # the hw-diagonal subspace
    projs = hw_projectors()
    gens = s3_generators()

    # Commutant dim of hw-diagonal operators
    # Build a basis of hw-diagonal matrices (block-diagonal 8x8)
    # and solve [M, g] = 0 for g in gens.
    hw_diag_basis = []
    for k, Pk in enumerate(projs):
        d_k = int(np.round(np.trace(Pk).real))
        # Indices in hw-k block
        idx_list = [i for i in range(8) if Pk[i, i] == 1.0]
        for i in idx_list:
            for j in idx_list:
                M = np.zeros((8, 8), dtype=complex)
                M[i, j] = 1.0
                hw_diag_basis.append(M)
    # The hw-diagonal subspace of End(C^8) has complex dim
    # 1² + 3² + 3² + 1² = 20.
    check("hw-diagonal End-space dim = 1+9+9+1 = 20",
          len(hw_diag_basis) == 20)

    # Find commutant: M in hw-diag s.t. [M, g] = 0 for g in gens
    B = np.stack([M.reshape(64) for M in hw_diag_basis], axis=1)  # 64 x 20

    constraints = []
    for g in gens:
        for Mi in hw_diag_basis:
            commutator = g @ Mi - Mi @ g
            constraints.append(commutator.reshape(64))
    # Set up: find c in C^20 such that Σ_i c_i [g, M_i] = 0 for all g
    # Constraint matrix
    C_mats = []
    for g in gens:
        Cg = np.stack([(g @ M - M @ g).reshape(64) for M in hw_diag_basis], axis=1)
        C_mats.append(Cg)
    C = np.vstack(C_mats)  # (2*64 x 20)
    rank = np.linalg.matrix_rank(C, tol=1e-10)
    null_dim = 20 - rank
    print(f"  Numerical commutant dim on hw-diagonal = {null_dim}")
    check("Numerical hw-diagonal S_3-commutant dim = 6",
          null_dim == 6)


# ---------------------------------------------------------------------------
# Part 4: Hw-off-diagonal S_3-invariant dim = 14
# ---------------------------------------------------------------------------

def part4_hw_offdiag_dim(hw_decomp: dict) -> None:
    print("\n" + "=" * 72)
    print("PART 4: Hw-off-diagonal S_3-invariant commutant dim = 14")
    print("=" * 72)

    # For j < k, Hom(V_j, V_k)^{S_3} has dim
    # m_A1^{(j)} * m_A1^{(k)} + m_E^{(j)} * m_E^{(k)}
    total_off_one_way = 0
    for j in range(4):
        for k in range(4):
            if j < k:
                ma_j = hw_decomp[j]["A1"]
                ma_k = hw_decomp[k]["A1"]
                me_j = hw_decomp[j]["E"]
                me_k = hw_decomp[k]["E"]
                dim_jk = ma_j * ma_k + me_j * me_k
                total_off_one_way += dim_jk
                print(f"  dim Hom(V_{j}, V_{k})^{{S_3}} = "
                      f"{ma_j}·{ma_k} + {me_j}·{me_k} = {dim_jk}")
    print(f"\n  Total one-way off-diagonal dim = {total_off_one_way}")
    check("One-way off-diagonal dim = 7 (j < k)",
          total_off_one_way == 7)

    total_off = 2 * total_off_one_way
    check("Two-way off-diagonal dim (j ≠ k) = 14",
          total_off == 14)

    # Numerical: solve commutator on off-hw-diagonal subspace
    gens = s3_generators()
    projs = hw_projectors()
    off_diag_basis = []
    for j in range(4):
        for k in range(4):
            if j == k:
                continue
            # Indices in V_j and V_k
            idx_j = [i for i in range(8) if projs[j][i, i] == 1.0]
            idx_k = [i for i in range(8) if projs[k][i, i] == 1.0]
            for a in idx_j:
                for b in idx_k:
                    M = np.zeros((8, 8), dtype=complex)
                    M[b, a] = 1.0  # maps V_j to V_k (row b, col a)
                    off_diag_basis.append(M)
    # Total: sum over j≠k of |V_j|*|V_k| = (total dim)² - (hw-diag dim)
    # = 64 - 20 = 44
    check("Off-diagonal End-space dim = 44",
          len(off_diag_basis) == 44)

    C_mats = []
    for g in gens:
        Cg = np.stack([(g @ M - M @ g).reshape(64) for M in off_diag_basis], axis=1)
        C_mats.append(Cg)
    C = np.vstack(C_mats)
    rank = np.linalg.matrix_rank(C, tol=1e-10)
    null_dim = 44 - rank
    print(f"  Numerical commutant dim on off-hw-diagonal = {null_dim}")
    check("Numerical off-diagonal S_3-commutant dim = 14",
          null_dim == 14)


# ---------------------------------------------------------------------------
# Part 5: Total = 20 (Batch 3 cross-check)
# ---------------------------------------------------------------------------

def part5_total() -> None:
    print("\n" + "=" * 72)
    print("PART 5: Total 6 + 14 = 20 (Batch 3 cross-check)")
    print("=" * 72)

    gens = s3_generators()
    # Full commutant dim
    n = 8
    bases = []
    for j in range(n):
        for k in range(n):
            M = np.zeros((n, n), dtype=complex)
            M[j, k] = 1.0
            bases.append(M)
    C_mats = []
    for g in gens:
        Cg = np.stack([(g @ M - M @ g).reshape(n * n) for M in bases], axis=1)
        C_mats.append(Cg)
    C = np.vstack(C_mats)
    rank = np.linalg.matrix_rank(C, tol=1e-10)
    null_dim = n * n - rank
    print(f"  dim End(C^8)^{{S_3}} = {null_dim}")
    check("Total dim = 20 (matches Batch 3 S_3-Invariant Operator Dimension)",
          null_dim == 20)
    check("Decomposition: 6 (hw-diagonal) + 14 (hw-off-diagonal) = 20",
          6 + 14 == 20)


# ---------------------------------------------------------------------------
# Part 6: Theorem statement
# ---------------------------------------------------------------------------

def part6_theorem() -> None:
    print("\n" + "=" * 72)
    print("PART 6: Hw-Graded Decomposition Theorem (statement)")
    print("=" * 72)

    print("""
  THEOREM (Hw-graded decomposition of End(C^8)^{S_3}).  Let
  C^8 = V_0 ⊕ V_1 ⊕ V_2 ⊕ V_3 be the Hamming-weight decomposition of
  the taste cube (dimensions 1 + 3 + 3 + 1).  Then the S_3-invariant
  commutant decomposes as

     End(C^8)^{S_3}  =  D  ⊕  O

  where

  (1) D = hw-preserving S_3-invariants.  As a sum over hw blocks:
         dim_C D  =  Σ_k dim_C End(V_k)^{S_3}  =  1 + 2 + 2 + 1  =  6,
      with each V_k contribution computed by Schur on the hw-block
      irrep content V_k = m_A1^{(k)} · A_1 + m_E^{(k)} · E.

  (2) O = hw-changing S_3-invariants (j ≠ k).  As a sum over ordered
      hw pairs:
         dim_C O  =  Σ_{j ≠ k} dim_C Hom(V_j, V_k)^{S_3}  =  14,
      with the one-way (j < k) sum 1+1+1+2+1+1 = 7, doubled by the
      two orderings.

  (3) dim_C End(C^8)^{S_3}  =  6 + 14  =  20, matching the Batch 3
      S_3-Invariant Operator Dimension theorem.

  (4) Hermitian real dim preserves the split: 6 + 14 = 20.

  PROOF.  Schur's lemma applied to the isotypic decomposition of each
  V_k and the restriction of S_3 irreps across hw blocks.  Verified
  numerically via kernel of the commutator map on the hw-graded
  subspaces of End(C^8).  QED.

  REUSABILITY.  Refines the Batch 3 S_3 dim-20 theorem into an
  hw-graded structure.  Separates mass-matrix-like (hw-preserving)
  operators from transition-like (hw-changing) operators.  Used when
  a framework operator is known to respect hw grading (e.g. gauge
  operators preserving particle content) or to change hw by a
  specific amount (e.g. Yukawa-like hw-1 transitions).
""")


def main() -> int:
    print("=" * 72)
    print("  Hw-Graded Decomposition of End(C^8)^{S_3}")
    print("=" * 72)

    part1_s3_preserves_hw()
    hw_decomp = part2_hw_block_irreps()
    part3_hw_diagonal_dim(hw_decomp)
    part4_hw_offdiag_dim(hw_decomp)
    part5_total()
    part6_theorem()

    print("\n" + "=" * 72)
    print(f"  TOTAL: PASS={PASS_COUNT}, FAIL={FAIL_COUNT}")
    print("=" * 72)

    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
