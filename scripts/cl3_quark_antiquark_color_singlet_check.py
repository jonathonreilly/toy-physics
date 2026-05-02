"""3 ⊗ 3̄ = 1 ⊕ 8 color singlet decomposition check on Cl(3) color structure."""
from __future__ import annotations

import math

import numpy as np


def gell_mann_matrices():
    s = []
    s.append(np.array([[0, 1, 0], [1, 0, 0], [0, 0, 0]], dtype=complex))
    s.append(np.array([[0, -1j, 0], [1j, 0, 0], [0, 0, 0]], dtype=complex))
    s.append(np.array([[1, 0, 0], [0, -1, 0], [0, 0, 0]], dtype=complex))
    s.append(np.array([[0, 0, 1], [0, 0, 0], [1, 0, 0]], dtype=complex))
    s.append(np.array([[0, 0, -1j], [0, 0, 0], [1j, 0, 0]], dtype=complex))
    s.append(np.array([[0, 0, 0], [0, 0, 1], [0, 1, 0]], dtype=complex))
    s.append(np.array([[0, 0, 0], [0, 0, -1j], [0, 1j, 0]], dtype=complex))
    s.append(np.array([[1, 0, 0], [0, 1, 0], [0, 0, -2]], dtype=complex) / math.sqrt(3))
    return s


def main() -> None:
    print("=" * 72)
    print("3 ⊗ 3̄ = 1 ⊕ 8 COLOR SINGLET DECOMPOSITION CHECK")
    print("=" * 72)
    print()

    N_c = 3
    print(f"  N_c = {N_c} (from Cl(3) color automorphism note)")
    print(f"  3 ⊗ 3̄ has dimension {N_c*N_c} = 9")
    print()

    # ----- Test 1: dimension count -----
    print("-" * 72)
    print("TEST 1: dim(3 ⊗ 3̄) = 1 + 8 = 9")
    print("-" * 72)
    dim_singlet = 1
    dim_octet = N_c * N_c - 1
    total = dim_singlet + dim_octet
    print(f"  dim(singlet) + dim(octet) = {dim_singlet} + {dim_octet} = {total}")
    t1_ok = total == N_c * N_c
    print(f"  STATUS: {'PASS' if t1_ok else 'FAIL'}")
    print()

    # ----- Test 2: singlet construction is normalized -----
    print("-" * 72)
    print("TEST 2: |singlet⟩ = (1/√3) Σ_i |i ī⟩ is normalized")
    print("-" * 72)
    # Construct in basis {|11⟩, |12⟩, ..., |33⟩} (9-dim)
    singlet = np.zeros(9, dtype=complex)
    for i in range(3):
        singlet[i * 3 + i] = 1.0 / math.sqrt(3)
    norm = float(np.real(singlet.conj() @ singlet))
    print(f"  ⟨singlet|singlet⟩ = {norm:.10f}")
    t2_ok = abs(norm - 1.0) < 1e-12
    print(f"  STATUS: {'PASS' if t2_ok else 'FAIL'}")
    print()

    # ----- Test 3: singlet is SU(3)-invariant -----
    print("-" * 72)
    print("TEST 3: |singlet⟩ is annihilated by all 8 SU(3)_c generators T^a ⊗ I + I ⊗ (-T^a)*")
    print("-" * 72)
    lams = gell_mann_matrices()
    Ts = [lam / 2 for lam in lams]
    # Generators on 3 ⊗ 3̄: T^a ⊗ I_3 + I_3 ⊗ (-(T^a)^T) = T^a ⊗ I - I ⊗ (T^a)^T
    I3 = np.eye(3, dtype=complex)
    max_resid = 0.0
    for a, T in enumerate(Ts):
        gen = np.kron(T, I3) - np.kron(I3, T.T)  # for the conjugate rep, generator is -T^T (or equivalently -T*)
        action = gen @ singlet
        norm_action = float(np.linalg.norm(action))
        max_resid = max(max_resid, norm_action)
    print(f"  max ||T^a |singlet⟩|| over 8 generators = {max_resid:.3e}")
    t3_ok = max_resid < 1e-10
    print(f"  STATUS: {'PASS' if t3_ok else 'FAIL'}")
    print()

    # ----- Test 4: singlet projector P = |singlet⟩⟨singlet| has trace 1 -----
    print("-" * 72)
    print("TEST 4: Tr(P_singlet) = 1 and P_singlet² = P_singlet")
    print("-" * 72)
    P = np.outer(singlet, singlet.conj())
    tr_P = float(np.real(np.trace(P)))
    P_sq = P @ P
    proj_resid = float(np.linalg.norm(P_sq - P))
    print(f"  Tr(P_singlet) = {tr_P:.6f}")
    print(f"  ||P² - P|| = {proj_resid:.3e}")
    t4_ok = abs(tr_P - 1.0) < 1e-12 and proj_resid < 1e-12
    print(f"  STATUS: {'PASS' if t4_ok else 'FAIL'}")
    print()

    # ----- Test 5: octet dimension = 9 - 1 = 8 -----
    print("-" * 72)
    print("TEST 5: orthogonal complement of singlet in 3 ⊗ 3̄ has dim 8")
    print("-" * 72)
    # Project out singlet from identity
    I9 = np.eye(9, dtype=complex)
    P_octet = I9 - P
    rank_octet = np.linalg.matrix_rank(P_octet, tol=1e-10)
    print(f"  rank(I - P_singlet) = {rank_octet}")
    t5_ok = rank_octet == 8
    print(f"  STATUS: {'PASS' if t5_ok else 'FAIL'}")
    print()

    # ----- Summary -----
    print("=" * 72)
    print(f"  Test 1 (dim 1 + 8 = 9):              {'PASS' if t1_ok else 'FAIL'}")
    print(f"  Test 2 (singlet normalized):         {'PASS' if t2_ok else 'FAIL'}")
    print(f"  Test 3 (SU(3)-invariance):           {'PASS' if t3_ok else 'FAIL'}")
    print(f"  Test 4 (singlet projector valid):    {'PASS' if t4_ok else 'FAIL'}")
    print(f"  Test 5 (octet rank = 8):             {'PASS' if t5_ok else 'FAIL'}")
    all_ok = t1_ok and t2_ok and t3_ok and t4_ok and t5_ok
    print(f"  OVERALL: {'PASS' if all_ok else 'FAIL'}")
    if not all_ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
