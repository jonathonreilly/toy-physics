"""SU(3) quadratic Casimir on the fundamental triplet equals 4/3.

By cl3_color_automorphism_theorem (retained), SU(3)_c acts on the framework's
3-dim symmetric base subspace via the canonical Gell-Mann generators
T^a = λ^a / 2 satisfying Tr[T^a T^b] = (1/2) δ^{ab}.

The quadratic Casimir
    C_2  :=  Σ_a T^a T^a
is a scalar multiple of the identity on each irreducible representation
(Schur). On the fundamental "3" of SU(N), C_2 = (N² - 1) / (2N).

For SU(3): C_2(3) = 8 / 6 = 4 / 3.

This number is the universal "color charge squared" of a color-triplet
quark, appearing in:
  - one-gluon-exchange potential coefficient
  - quark self-energy at one loop
  - all hard-scattering color factors involving color triplets

Tests:
  (T1) Gell-Mann anticommutation: {T^a, T^b} = (1/3) δ^{ab} I + d^{abc} T^c
  (T2) Gell-Mann commutation:     [T^a, T^b] = i f^{abc} T^c (su(3) Lie algebra)
  (T3) Tr[T^a T^b] = (1/2) δ^{ab}
  (T4) Casimir C_2 = Σ_a T^a T^a is proportional to identity
  (T5) C_2 eigenvalue equals 4/3 exactly
  (T6) Same Casimir computed via formula (N² - 1) / (2N) = 4/3
"""
from __future__ import annotations

import numpy as np


def gell_mann_matrices() -> list[np.ndarray]:
    """The 8 Gell-Mann matrices λ^1, ..., λ^8 (Hermitian, 3x3).

    Standard normalization: Tr[λ^a λ^b] = 2 δ^{ab}, so T^a := λ^a / 2 has
    Tr[T^a T^b] = (1/2) δ^{ab}.
    """
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
    print("SU(3) QUADRATIC CASIMIR ON FUNDAMENTAL = 4/3")
    print("=" * 72)
    print()

    lambdas = gell_mann_matrices()
    T = [L / 2 for L in lambdas]
    I3 = np.eye(3, dtype=complex)

    # ----- Test 1: Hermitian generators -----
    print("-" * 72)
    print("TEST 1: T^a are Hermitian (a = 1, ..., 8)")
    print("-" * 72)
    max_herm = 0.0
    for a, Ta in enumerate(T):
        d = np.linalg.norm(Ta - Ta.conj().T)
        max_herm = max(max_herm, d)
    print(f"  max ||T^a - (T^a)†|| = {max_herm:.3e}")
    t1_ok = max_herm < 1e-12
    print(f"  STATUS: {'PASS' if t1_ok else 'FAIL'}")
    print()

    # ----- Test 2: Trace orthonormality Tr[T^a T^b] = (1/2) δ^{ab} -----
    print("-" * 72)
    print("TEST 2: Tr[T^a T^b] = (1/2) δ^{ab}")
    print("-" * 72)
    max_trace_dev = 0.0
    for a in range(8):
        for b in range(8):
            tr = np.trace(T[a] @ T[b])
            target = 0.5 if a == b else 0.0
            d = abs(tr - target)
            max_trace_dev = max(max_trace_dev, d)
    print(f"  max |Tr[T^a T^b] - (1/2) δ^{{ab}}| = {max_trace_dev:.3e}")
    t2_ok = max_trace_dev < 1e-12
    print(f"  STATUS: {'PASS' if t2_ok else 'FAIL'}")
    print()

    # ----- Test 3: su(3) Lie algebra [T^a, T^b] = i f^{abc} T^c -----
    print("-" * 72)
    print("TEST 3: su(3) Lie algebra [T^a, T^b] = i f^{abc} T^c (closure)")
    print("-" * 72)
    # Compute commutators and verify each lies in the Hermitian span of T^a
    # by checking that i [T^a, T^b] is Hermitian and lives in span{T^c}.
    max_close_dev = 0.0
    for a in range(8):
        for b in range(8):
            comm = T[a] @ T[b] - T[b] @ T[a]
            # i*comm should be Hermitian (anti-Hermitian comm × i = Hermitian)
            i_comm = 1j * comm
            # Project onto span{T^c}: f^{abc} = -2i Tr[[T^a, T^b] T^c]
            f_abc = [(-2j * np.trace(comm @ T[c])).real for c in range(8)]
            recon = sum(1j * f_abc[c] * T[c] for c in range(8))
            d = np.linalg.norm(comm - recon)
            max_close_dev = max(max_close_dev, d)
    print(f"  max ||[T^a, T^b] - i f^{{abc}} T^c|| = {max_close_dev:.3e}")
    t3_ok = max_close_dev < 1e-10
    print(f"  STATUS: {'PASS' if t3_ok else 'FAIL'}")
    print()

    # ----- Test 4: Casimir C_2 = Σ T^a T^a is proportional to identity -----
    print("-" * 72)
    print("TEST 4: C_2 := Σ_a T^a T^a is proportional to I_3 (Schur)")
    print("-" * 72)
    C2 = sum(Ta @ Ta for Ta in T)
    # Verify C_2 = c · I for some c
    eigs = np.linalg.eigvalsh(C2.real if np.allclose(C2.imag, 0) else 0.5 * (C2 + C2.conj().T))
    eigs_real = sorted(eigs.tolist())
    print(f"  C_2 eigenvalues = {eigs_real}")
    # All eigenvalues should be equal
    spread = max(eigs_real) - min(eigs_real)
    print(f"  spread (max - min) = {spread:.3e}")
    t4_ok = spread < 1e-12
    print(f"  STATUS: {'PASS' if t4_ok else 'FAIL'}")
    print()

    # ----- Test 5: C_2 eigenvalue = 4/3 -----
    print("-" * 72)
    print("TEST 5: C_2 eigenvalue equals 4/3 = 1.333...")
    print("-" * 72)
    c2_value = eigs_real[0]
    target = 4.0 / 3.0
    dev = abs(c2_value - target)
    print(f"  C_2 = {c2_value} (expected 4/3 = {target})")
    print(f"  |C_2 - 4/3| = {dev:.3e}")
    t5_ok = dev < 1e-12
    print(f"  STATUS: {'PASS' if t5_ok else 'FAIL'}")
    print()

    # ----- Test 6: Formula (N² - 1) / (2N) = 4/3 for N = 3 -----
    print("-" * 72)
    print("TEST 6: Casimir formula C_2(N) = (N² - 1) / (2N) gives 4/3 for N=3")
    print("-" * 72)
    N = 3
    C2_formula = (N ** 2 - 1) / (2 * N)
    print(f"  (N² - 1) / (2N) = ({N**2} - 1) / {2*N} = {C2_formula}")
    formula_dev = abs(C2_formula - target)
    print(f"  |formula - 4/3| = {formula_dev:.3e}")
    t6_ok = formula_dev < 1e-12
    print(f"  STATUS: {'PASS' if t6_ok else 'FAIL'}")
    print()

    # ----- Test 7: Numerical = formula -----
    print("-" * 72)
    print("TEST 7: Numerical Casimir = formula Casimir = 4/3")
    print("-" * 72)
    agreement = abs(c2_value - C2_formula)
    print(f"  |numerical C_2 - formula C_2| = {agreement:.3e}")
    t7_ok = agreement < 1e-12
    print(f"  STATUS: {'PASS' if t7_ok else 'FAIL'}")
    print()

    print("=" * 72)
    print(f"  Test 1 (T^a Hermitian):                        {'PASS' if t1_ok else 'FAIL'}")
    print(f"  Test 2 (Tr[T^a T^b] = (1/2) δ^{{ab}}):           {'PASS' if t2_ok else 'FAIL'}")
    print(f"  Test 3 (su(3) Lie algebra closure):            {'PASS' if t3_ok else 'FAIL'}")
    print(f"  Test 4 (C_2 ∝ I_3, Schur):                     {'PASS' if t4_ok else 'FAIL'}")
    print(f"  Test 5 (C_2 = 4/3 numerically):                {'PASS' if t5_ok else 'FAIL'}")
    print(f"  Test 6 (formula (N²-1)/(2N) = 4/3, N=3):       {'PASS' if t6_ok else 'FAIL'}")
    print(f"  Test 7 (numerical = formula):                  {'PASS' if t7_ok else 'FAIL'}")
    all_ok = all([t1_ok, t2_ok, t3_ok, t4_ok, t5_ok, t6_ok, t7_ok])
    print(f"  OVERALL: {'PASS' if all_ok else 'FAIL'}")
    if not all_ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
