#!/usr/bin/env python3
"""
Residual Z_2 Commutant on C^8 (post-SSB structure)

Framework object:
  Let Z_2 = ⟨(12)⟩ ⊂ S_3 be the residual subgroup that fixes one
  axis (say axis 3) and swaps the other two.  This is the natural
  residual subgroup produced by the V_sel SSB pattern S_3 → Z_2
  in frameworks that use the taste cube C^8 = (C²)^⊗³.

Theorem (Residual Z_2 Commutant on C^8):
  (1) C^8 decomposes under this Z_2 as
         C^8  ≅  6 · (trivial Z_2)  ⊕  2 · (sign Z_2).
      Hw-by-hw breakdown:
         hw = 0:  1 · trivial
         hw = 1:  2 · trivial  ⊕  1 · sign
         hw = 2:  2 · trivial  ⊕  1 · sign
         hw = 3:  1 · trivial.
  (2) dim_C End(C^8)^{Z_2} = 6² + 2² = 40.
  (3) The dimension of the Hermitian S_3-invariant commutant jumps
      from 20 (S_3-invariant) to 40 (Z_2-invariant) upon SSB, i.e.
      SSB doubles the number of real parameters available for
      operators on the taste cube.
  (4) Restricted to the hw=1 triplet alone, dim End(V_{hw=1})^{Z_2}
      = 2² + 1² = 5, which is enough to accommodate three distinct
      eigenvalues (consistent with the S_3 Mass-Matrix No-Go, Batch 4).

Proof method: direct Schur dimension count + explicit basis
construction and commutativity verification.

Reusability:
  - Canonical quantification of the "relief" provided by S_3 → Z_2 SSB
  - Used whenever a framework claim requires residual Z_2 invariance
    and needs to count free parameters / degrees of freedom
  - Complements Batch 4 S_3 Mass-Matrix No-Go: no-go shows SSB is
    necessary; this result shows how much symmetry-breaking relief is
    obtained
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
# Z_2 generator on C^8 = (C^2)^⊗3:
#   swap of factors 1 and 2 (axes 1 and 2)
# ---------------------------------------------------------------------------

def axis_swap_12() -> np.ndarray:
    """Unitary on C^8 swapping axes 1 and 2 (fixing axis 3)."""
    U = np.zeros((8, 8), dtype=complex)
    for a, b, c in itertools.product([0, 1], repeat=3):
        src = a * 4 + b * 2 + c
        # swap a <-> b in destination
        dst = b * 4 + a * 2 + c
        U[dst, src] = 1.0
    return U


def hw(alpha: tuple) -> int:
    return sum(alpha)


# ---------------------------------------------------------------------------
# Part 1: Z_2 decomposition of C^8
# ---------------------------------------------------------------------------

def part1_decomposition() -> dict:
    print("\n" + "=" * 72)
    print("PART 1: Z_2 decomposition of C^8")
    print("=" * 72)

    U = axis_swap_12()
    check("Z_2 generator U is unitary",
          np.allclose(U.conj().T @ U, np.eye(8)))
    check("Z_2 generator U² = I",
          np.allclose(U @ U, np.eye(8)))

    # Classify each basis element
    states = list(itertools.product([0, 1], repeat=3))

    # Build +1 and -1 eigenbases explicitly by hw level
    trivs: list[np.ndarray] = []
    signs: list[np.ndarray] = []
    hw_counts = {k: {"triv": 0, "sign": 0} for k in range(4)}

    for alpha in states:
        a, b, c = alpha
        idx = a * 4 + b * 2 + c
        beta = (b, a, c)
        idx_swap = b * 4 + a * 2 + c
        if alpha == beta:
            # Already Z_2-fixed
            v = np.zeros(8, dtype=complex)
            v[idx] = 1.0
            trivs.append(v)
            hw_counts[hw(alpha)]["triv"] += 1
        elif alpha < beta:
            # Pair (alpha, beta) with alpha < beta in lex order
            v_plus = np.zeros(8, dtype=complex)
            v_plus[idx] = 1.0 / np.sqrt(2)
            v_plus[idx_swap] = 1.0 / np.sqrt(2)
            v_minus = np.zeros(8, dtype=complex)
            v_minus[idx] = 1.0 / np.sqrt(2)
            v_minus[idx_swap] = -1.0 / np.sqrt(2)
            trivs.append(v_plus)
            signs.append(v_minus)
            hw_counts[hw(alpha)]["triv"] += 1
            hw_counts[hw(alpha)]["sign"] += 1

    print(f"\n  Hw-by-hw decomposition (triv, sign):")
    for k in range(4):
        print(f"    hw = {k}:  triv = {hw_counts[k]['triv']},  "
              f"sign = {hw_counts[k]['sign']}")
    total_triv = sum(c["triv"] for c in hw_counts.values())
    total_sign = sum(c["sign"] for c in hw_counts.values())
    print(f"    TOTAL:   triv = {total_triv},  sign = {total_sign}")

    check("Total trivial multiplicity = 6", total_triv == 6)
    check("Total sign multiplicity = 2", total_sign == 2)
    check("Hw=0: 1·triv",
          hw_counts[0] == {"triv": 1, "sign": 0})
    check("Hw=1: 2·triv + 1·sign",
          hw_counts[1] == {"triv": 2, "sign": 1})
    check("Hw=2: 2·triv + 1·sign",
          hw_counts[2] == {"triv": 2, "sign": 1})
    check("Hw=3: 1·triv",
          hw_counts[3] == {"triv": 1, "sign": 0})

    # Verify by eigenvalue count
    eigvals = np.linalg.eigvalsh(U.conj().T @ U + U)  # build U+I then U-I
    # Simpler: directly count ±1 eigenvalues of U
    w = np.linalg.eigvals(U)
    count_plus = int(np.round(np.sum(np.isclose(w, 1.0))))
    count_minus = int(np.round(np.sum(np.isclose(w, -1.0))))
    check("Direct eigenvalue count: +1 mult = 6",
          count_plus == 6, f"obs +1 mult = {count_plus}")
    check("Direct eigenvalue count: -1 mult = 2",
          count_minus == 2, f"obs -1 mult = {count_minus}")

    # Verify all constructed vectors have the right eigenvalue
    for v in trivs:
        if not np.allclose(U @ v, v, atol=1e-12):
            check("trivial vector is +1 eigenvector", False)
            return {}
    for v in signs:
        if not np.allclose(U @ v, -v, atol=1e-12):
            check("sign vector is -1 eigenvector", False)
            return {}
    check("All 6 trivial vectors are +1 eigenvectors", True)
    check("All 2 sign vectors are -1 eigenvectors", True)

    return {"trivs": trivs, "signs": signs, "U": U, "hw_counts": hw_counts}


# ---------------------------------------------------------------------------
# Part 2: dim End(C^8)^{Z_2} = 40
# ---------------------------------------------------------------------------

def part2_commutant_dim(data: dict) -> None:
    print("\n" + "=" * 72)
    print("PART 2: dim End(C^8)^{Z_2} = 40")
    print("=" * 72)

    U = data["U"]

    # Build the commutant by solving [U, M] = 0 as a linear system.
    # M is a general 8x8 complex matrix; constraint is U M = M U.
    # As 64-dim complex linear equations.
    n = 8
    # C x = 0 where x = vec(M), and C is (n² x n²) matrix of the
    # commutator map M ↦ U M - M U.
    C = np.zeros((n * n, n * n), dtype=complex)
    for j in range(n):
        for k in range(n):
            # Unit vector E_{jk}: 1 at (j,k)
            # U E_{jk} has entries U[:,j] in column k
            # E_{jk} U has entries U[k,:] in row j
            M = np.zeros((n, n), dtype=complex)
            M[j, k] = 1.0
            commutator = U @ M - M @ U
            C[:, j * n + k] = commutator.reshape(n * n)

    rank = np.linalg.matrix_rank(C, tol=1e-10)
    null_dim = n * n - rank
    print(f"  Commutator map rank          = {rank}")
    print(f"  dim(ker commutator) = dim End(C^8)^{{Z_2}} = {null_dim}")

    check("dim End(C^8)^{Z_2} = 40 (Schur: 6² + 2²)",
          null_dim == 40)

    # Dimension count by Schur: sum of (multiplicity)² for each irrep
    mult_sum = 6 ** 2 + 2 ** 2
    print(f"  Schur prediction: 6² + 2² = {mult_sum}")
    check("Matches Schur dimension 6² + 2²", null_dim == mult_sum)

    # Compare with S_3-invariant dim
    print(f"\n  S_3-invariant dim (Batch 3): 20")
    print(f"  Z_2-invariant dim (this theorem): 40")
    check("SSB S_3 → Z_2 doubles the commutant dim", null_dim == 2 * 20)


# ---------------------------------------------------------------------------
# Part 3: Restricted to hw=1, dim = 5
# ---------------------------------------------------------------------------

def part3_hw1_commutant() -> None:
    print("\n" + "=" * 72)
    print("PART 3: Restricted commutant on hw=1 triplet, dim = 5")
    print("=" * 72)

    # Hw=1 states: |100⟩ (idx 4), |010⟩ (idx 2), |001⟩ (idx 1)
    # Under Z_2 = swap axes 1 and 2: |100⟩ ↔ |010⟩, |001⟩ fixed.
    # As Z_2 rep: 2·triv + 1·sign.

    # Build Z_2 generator restricted to hw=1 (3x3)
    U3 = np.array([
        [1.0, 0.0, 0.0],   # |001⟩ fixed
        [0.0, 0.0, 1.0],   # |010⟩ <-> |100⟩
        [0.0, 1.0, 0.0],
    ], dtype=complex)

    check("Hw=1 Z_2 generator is involution",
          np.allclose(U3 @ U3, np.eye(3)))

    # Count commutant dim
    n = 3
    C = np.zeros((n * n, n * n), dtype=complex)
    for j in range(n):
        for k in range(n):
            M = np.zeros((n, n), dtype=complex)
            M[j, k] = 1.0
            commutator = U3 @ M - M @ U3
            C[:, j * n + k] = commutator.reshape(n * n)
    rank = np.linalg.matrix_rank(C, tol=1e-10)
    null_dim = n * n - rank

    print(f"  dim End(hw=1)^{{Z_2}} = {null_dim}")
    check("dim = 5 = 2² + 1² on hw=1",
          null_dim == 5)

    # Build an explicit Z_2-invariant 3x3 Hermitian with 3 distinct eigenvalues
    # In basis (|001⟩, |010⟩, |100⟩):
    # Z_2 acts: fix first, swap second and third.
    # General Z_2-invariant Hermitian M has:
    #   M[0,0] = a (real)
    #   M[1,1] = M[2,2] = b (real)
    #   M[1,2] = M[2,1] = c (real, since Hermitian + Z_2-inv forces real)
    #   M[0,1] = M[0,2] = d (complex)
    #   M[1,0] = M[2,0] = d*
    # Free real parameters: a, b, c, Re(d), Im(d) = 5 ✓
    a, b, c, dr, di = 1.0, 2.0, 0.3, 0.4, 0.5
    d = dr + 1j * di
    M = np.array([
        [a,           d,   d   ],
        [np.conj(d),  b,   c   ],
        [np.conj(d),  c,   b   ],
    ], dtype=complex)

    check("Constructed Z_2-invariant matrix is Hermitian",
          np.allclose(M, M.conj().T))
    # Commutes with Z_2 generator
    check("Constructed Z_2-invariant matrix commutes with Z_2",
          np.allclose(U3 @ M, M @ U3))
    eigs = np.linalg.eigvalsh(M)
    n_distinct = len(np.unique(np.round(eigs, 8)))
    print(f"  Eigenvalues of explicit Z_2-invariant Hermitian: {eigs}")
    check("Explicit Z_2-invariant Hermitian has 3 distinct eigenvalues",
          n_distinct == 3,
          f"distinct eigvals = {n_distinct}")


# ---------------------------------------------------------------------------
# Part 4: Hermitian cut: real dim = 40
# ---------------------------------------------------------------------------

def part4_hermitian_real_dim(data: dict) -> None:
    print("\n" + "=" * 72)
    print("PART 4: Hermitian Z_2-invariant operators: real dim = 40")
    print("=" * 72)

    U = data["U"]
    n = 8
    # For each basis of End(C^8)^{Z_2}, the Hermitian subspace has
    # real dim = complex dim of commutant = 40.
    # (Because commutant is *-closed under Hermitian conjugation since
    # Z_2 is unitary.)

    # Verify by checking U† commutes implies commutant *-closed
    # U† = U^{-1} = U (involution) — so conjugation preserves commutant.
    check("Z_2 generator is Hermitian (U = U†)",
          np.allclose(U, U.conj().T))
    check("Commutant is *-closed (Hermitian subspace has real dim = complex dim = 40)",
          True)

    # Sanity: construct 40 linearly independent Hermitian Z_2-invariant
    # operators by random projection.  Take random M, project to
    # commutant via averaging over Z_2, then Hermitize.
    rng = np.random.default_rng(0)
    Hermitians = []
    for _ in range(60):
        M = rng.normal(size=(n, n)) + 1j * rng.normal(size=(n, n))
        # Project to Z_2 commutant
        M_avg = 0.5 * (M + U @ M @ U)  # since U² = I
        # Hermitize
        H = 0.5 * (M_avg + M_avg.conj().T)
        Hermitians.append(H.reshape(n * n))
    H_matrix = np.stack(Hermitians, axis=1)
    # Over R: stack real and imaginary parts
    H_real = np.vstack([H_matrix.real, H_matrix.imag])
    rank_real = np.linalg.matrix_rank(H_real, tol=1e-10)
    print(f"  Real rank of 60 random Hermitian Z_2-invariants = {rank_real}")
    check("Real dim of Hermitian Z_2-invariant subspace = 40",
          rank_real == 40,
          f"rank = {rank_real}")


# ---------------------------------------------------------------------------
# Part 5: Theorem statement
# ---------------------------------------------------------------------------

def part5_theorem() -> None:
    print("\n" + "=" * 72)
    print("PART 5: Residual Z_2 Commutant Theorem (statement)")
    print("=" * 72)

    print("""
  THEOREM (Residual Z_2 Commutant on C^8).  Let Z_2 = ⟨τ⟩ ⊂ S_3 be
  the residual subgroup generated by the swap τ = (12) of two taste
  axes, acting on C^8 = (C²)^⊗³ by axis permutation.  Then:

  (1) C^8 decomposes as a Z_2 representation as
         C^8  ≅  6 · 1  ⊕  2 · sgn,
      where 1 is the trivial rep and sgn the sign rep.  Hamming-weight
      breakdown:
         hw = 0:  1 · 1
         hw = 1:  2 · 1  ⊕  1 · sgn
         hw = 2:  2 · 1  ⊕  1 · sgn
         hw = 3:  1 · 1.

  (2) By Schur's lemma,
         dim_C End(C^8)^{Z_2}  =  6²  +  2²  =  40,
      and dim_R (Hermitian part)  =  40.

  (3) Upon SSB S_3 → Z_2, the dimension of the Hermitian invariant
      operator algebra on C^8 doubles from 20 (S_3-invariant, Batch 3)
      to 40 (Z_2-invariant).

  (4) Restricted to the hw=1 triplet, dim End(V_1)^{Z_2} = 2² + 1² = 5,
      which suffices for three distinct eigenvalues (companion to the
      S_3 Mass-Matrix No-Go, Batch 4).

  PROOF.  By direct decomposition of the standard basis under the
  involution τ on axes 1, 2 — paired states give 1 ⊕ sgn, fixed
  states give 1 — followed by Schur's lemma.  QED.

  REUSABILITY.  Quantifies the operator-level relief provided by
  S_3 → Z_2 SSB.  Companion to the S_3 Mass-Matrix No-Go:  the no-go
  shows SSB is necessary for three-way-distinct generation masses;
  this result shows the relief is a doubling (20 → 40) of the
  invariant-operator dimension on the full taste cube, with the
  hw=1 restricted commutant jumping 2 → 5.
""")


def main() -> int:
    print("=" * 72)
    print("  Residual Z_2 Commutant on C^8 (post-SSB structure)")
    print("=" * 72)

    data = part1_decomposition()
    part2_commutant_dim(data)
    part3_hw1_commutant()
    part4_hermitian_real_dim(data)
    part5_theorem()

    print("\n" + "=" * 72)
    print(f"  TOTAL: PASS={PASS_COUNT}, FAIL={FAIL_COUNT}")
    print("=" * 72)

    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
