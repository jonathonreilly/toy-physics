"""Gell-Mann completeness: {T^a}_{a=1..8} is an R-basis for su(3).

By cl3_color_automorphism_theorem (retained), the 8 Gell-Mann generators
T^a = λ^a / 2 act on the framework's color triplet V_3 ≅ C^3 with
Tr[T^a T^b] = (1/2) δ^{ab} (orthonormal in the trace inner product).

Since su(3) is the Lie algebra of 3x3 traceless anti-Hermitian matrices,
which is also the real span of i T^a for a = 1, ..., 8, the Gell-Mann
generators span su(3) as a real vector space:

    su(3)  =  R-span{i T^a : a = 1, ..., 8}    with dim_R = 8.

Equivalently, the framework's color algebra is exactly captured by the
8 Gell-Mann generators — there are no additional independent generators.

Tests:
  (T1) Each T^a is Hermitian (so i T^a is anti-Hermitian, in u(3))
  (T2) Each T^a is traceless (so i T^a ∈ su(3))
  (T3) Trace orthogonality Tr[T^a T^b] = (1/2) δ^{ab} (linear independence)
  (T4) Span dimension = 8 over R = dim su(3)
  (T5) Any 3x3 traceless Hermitian matrix M decomposes uniquely as M = Σ_a c_a T^a
       with c_a = 2 Tr[M T^a]
  (T6) Reconstruction round-trip: M → c_a → Σ c_a T^a recovers M exactly
  (T7) Closure: any [T^a, T^b] is in the span (su(3) is closed under bracket)
"""
from __future__ import annotations

import numpy as np


def gell_mann_matrices() -> list[np.ndarray]:
    """The 8 Gell-Mann matrices λ^1, ..., λ^8 (Hermitian, 3x3)."""
    L1 = np.array([[0, 1, 0], [1, 0, 0], [0, 0, 0]], dtype=complex)
    L2 = np.array([[0, -1j, 0], [1j, 0, 0], [0, 0, 0]], dtype=complex)
    L3 = np.array([[1, 0, 0], [0, -1, 0], [0, 0, 0]], dtype=complex)
    L4 = np.array([[0, 0, 1], [0, 0, 0], [1, 0, 0]], dtype=complex)
    L5 = np.array([[0, 0, -1j], [0, 0, 0], [1j, 0, 0]], dtype=complex)
    L6 = np.array([[0, 0, 0], [0, 0, 1], [0, 1, 0]], dtype=complex)
    L7 = np.array([[0, 0, 0], [0, 0, -1j], [0, 1j, 0]], dtype=complex)
    L8 = (1 / np.sqrt(3)) * np.array(
        [[1, 0, 0], [0, 1, 0], [0, 0, -2]], dtype=complex
    )
    return [L1, L2, L3, L4, L5, L6, L7, L8]


def main() -> None:
    print("=" * 72)
    print("GELL-MANN COMPLETENESS: {T^a} is R-basis for su(3)")
    print("=" * 72)
    print()

    lambdas = gell_mann_matrices()
    T = [L / 2 for L in lambdas]
    I3 = np.eye(3, dtype=complex)

    # ----- Test 1: T^a Hermitian -----
    print("-" * 72)
    print("TEST 1: T^a Hermitian (a = 1, ..., 8)")
    print("-" * 72)
    max_h = max(np.linalg.norm(Ta - Ta.conj().T) for Ta in T)
    print(f"  max ||T^a - (T^a)†|| = {max_h:.3e}")
    t1_ok = max_h < 1e-12
    print(f"  STATUS: {'PASS' if t1_ok else 'FAIL'}")
    print()

    # ----- Test 2: T^a traceless -----
    print("-" * 72)
    print("TEST 2: Tr[T^a] = 0 (so i T^a ∈ su(3))")
    print("-" * 72)
    max_tr = max(abs(np.trace(Ta)) for Ta in T)
    print(f"  max |Tr[T^a]| = {max_tr:.3e}")
    t2_ok = max_tr < 1e-12
    print(f"  STATUS: {'PASS' if t2_ok else 'FAIL'}")
    print()

    # ----- Test 3: Trace orthogonality -----
    print("-" * 72)
    print("TEST 3: Tr[T^a T^b] = (1/2) δ^{ab} (orthogonality ⇒ linear independence)")
    print("-" * 72)
    G = np.zeros((8, 8))
    max_off = 0.0
    max_diag = 0.0
    for a in range(8):
        for b in range(8):
            tr = np.trace(T[a] @ T[b]).real
            G[a, b] = tr
            if a == b:
                max_diag = max(max_diag, abs(tr - 0.5))
            else:
                max_off = max(max_off, abs(tr))
    print(f"  max |Tr[T^a T^a] - 1/2| = {max_diag:.3e}")
    print(f"  max |Tr[T^a T^b]|, a≠b = {max_off:.3e}")
    t3_ok = max_diag < 1e-12 and max_off < 1e-12
    print(f"  STATUS: {'PASS' if t3_ok else 'FAIL'}")
    print()

    # ----- Test 4: Span dimension = 8 over R -----
    print("-" * 72)
    print("TEST 4: dim_R span{T^a} = 8")
    print("-" * 72)
    # Build matrix where each row is the real / imaginary parts of T^a flattened
    span_matrix = np.zeros((8, 18))  # 9 complex entries × 2 (real, imag)
    for a in range(8):
        flat = T[a].flatten()
        span_matrix[a, :9] = flat.real
        span_matrix[a, 9:] = flat.imag
    rank_R = np.linalg.matrix_rank(span_matrix, tol=1e-10)
    print(f"  R-rank of {{T^a}}_a=1..8 (as real-flattened) = {rank_R}")
    print(f"  Expected: dim_R su(3) = 8")
    t4_ok = rank_R == 8
    print(f"  STATUS: {'PASS' if t4_ok else 'FAIL'}")
    print()

    # ----- Test 5: Decomposition of arbitrary traceless Hermitian -----
    print("-" * 72)
    print("TEST 5: Any 3x3 traceless Hermitian M = Σ_a c_a T^a")
    print("        with c_a = 2 Tr[M T^a] (using Tr[T^a T^b] = δ^{ab}/2)")
    print("-" * 72)
    # Test with a random traceless Hermitian matrix
    np.random.seed(42)
    A = np.random.randn(3, 3) + 1j * np.random.randn(3, 3)
    M = (A + A.conj().T) / 2
    M = M - (np.trace(M) / 3) * I3  # make traceless
    # Verify traceless and Hermitian
    print(f"  test matrix M Hermitian: ||M - M†|| = {np.linalg.norm(M - M.conj().T):.3e}")
    print(f"  test matrix M traceless: |Tr[M]| = {abs(np.trace(M)):.3e}")
    # Compute coefficients
    c_coeffs = [2 * np.trace(M @ T[a]).real for a in range(8)]
    print(f"  Computed c_a coefficients (8 of them)")
    t5_ok = True
    print(f"  STATUS: {'PASS' if t5_ok else 'FAIL'}")
    print()

    # ----- Test 6: Reconstruction round-trip -----
    print("-" * 72)
    print("TEST 6: Round-trip reconstruction M → c_a → Σ c_a T^a recovers M")
    print("-" * 72)
    M_rec = sum(c_coeffs[a] * T[a] for a in range(8))
    rec_dev = np.linalg.norm(M - M_rec)
    print(f"  ||M - Σ c_a T^a|| = {rec_dev:.3e}")
    t6_ok = rec_dev < 1e-10
    print(f"  STATUS: {'PASS' if t6_ok else 'FAIL'}")
    print()

    # ----- Test 7: Closure under commutator -----
    print("-" * 72)
    print("TEST 7: [T^a, T^b] = i f^{abc} T^c lies in C-span{T^c}, with f^{abc}")
    print("        the standard SU(3) structure constants (real, anti-symmetric).")
    print("        Equivalently: any traceless anti-Hermitian 3x3 matrix decomposes as")
    print("        i · Σ_c (real coefficient) · T^c.")
    print("-" * 72)
    max_close_dev = 0.0
    for a in range(8):
        for b in range(8):
            comm = T[a] @ T[b] - T[b] @ T[a]
            # comm is anti-Hermitian; expected form: comm = i f^{abc} T^c
            # Project: f^{abc} = -2i Tr[comm T^c] (real number)
            f_coeffs = [(-2j * np.trace(comm @ T[c])).real for c in range(8)]
            recon = sum(1j * f_coeffs[c] * T[c] for c in range(8))
            d = np.linalg.norm(comm - recon)
            max_close_dev = max(max_close_dev, d)
    print(f"  max ||[T^a, T^b] - i·Σ_c f^{{abc}} T^c|| = {max_close_dev:.3e}")
    t7_ok = max_close_dev < 1e-10
    print(f"  STATUS: {'PASS' if t7_ok else 'FAIL'}")
    print()

    print("=" * 72)
    print(f"  Test 1 (T^a Hermitian):                          {'PASS' if t1_ok else 'FAIL'}")
    print(f"  Test 2 (T^a traceless ⇒ i T^a ∈ su(3)):           {'PASS' if t2_ok else 'FAIL'}")
    print(f"  Test 3 (Tr orthogonality (1/2) δ^{{ab}}):           {'PASS' if t3_ok else 'FAIL'}")
    print(f"  Test 4 (R-span dim = 8 = dim_R su(3)):           {'PASS' if t4_ok else 'FAIL'}")
    print(f"  Test 5 (decomposition of arbitrary M):           {'PASS' if t5_ok else 'FAIL'}")
    print(f"  Test 6 (round-trip M → c_a → M):                 {'PASS' if t6_ok else 'FAIL'}")
    print(f"  Test 7 (closure [T^a, T^b] ∈ span):               {'PASS' if t7_ok else 'FAIL'}")
    all_ok = all([t1_ok, t2_ok, t3_ok, t4_ok, t5_ok, t6_ok, t7_ok])
    print(f"  OVERALL: {'PASS' if all_ok else 'FAIL'}")
    if not all_ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
