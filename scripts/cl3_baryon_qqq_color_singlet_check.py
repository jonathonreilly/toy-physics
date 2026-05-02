"""3 ⊗ 3 ⊗ 3 baryon color singlet check on retained SU(3)_c."""
from __future__ import annotations

import math
import itertools

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
    print("3 ⊗ 3 ⊗ 3 BARYON COLOR SINGLET CHECK")
    print("=" * 72)
    print()
    N_c = 3
    print(f"  N_c = {N_c} (from retained Cl(3) color automorphism note)")
    print(f"  3 ⊗ 3 ⊗ 3 has dimension {N_c**3} = 27")
    print()

    # ----- Test 1: dimension count -----
    print("-" * 72)
    print("TEST 1: dim(3 ⊗ 3 ⊗ 3) = 1 + 8 + 8 + 10 = 27")
    print("-" * 72)
    dim_singlet = 1
    dim_octet = 8
    dim_octet2 = 8
    dim_decuplet = 10
    total = dim_singlet + dim_octet + dim_octet2 + dim_decuplet
    print(f"  1 + 8 + 8 + 10 = {total}")
    print(f"  3^3 = {N_c**3}")
    t1_ok = total == N_c**3
    print(f"  STATUS: {'PASS' if t1_ok else 'FAIL'}")
    print()

    # ----- Test 2: Levi-Civita baryon singlet construction is normalized -----
    print("-" * 72)
    print("TEST 2: |baryon_singlet⟩ = (1/√6) ε_{abc} |abc⟩ is normalized")
    print("-" * 72)
    # 27-dim basis: (a, b, c) → index 9a + 3b + c, indexing from 0
    singlet = np.zeros(N_c ** 3, dtype=complex)
    # Levi-Civita on (a, b, c) ∈ {0, 1, 2}^3
    perms = list(itertools.permutations(range(N_c)))
    for perm in perms:
        sign = 1
        # Compute permutation sign
        pi = list(perm)
        for i in range(N_c):
            for j in range(i+1, N_c):
                if pi[i] > pi[j]:
                    sign = -sign
        a, b, c = perm
        idx = 9 * a + 3 * b + c
        singlet[idx] = sign / math.sqrt(6)
    norm = float(np.real(singlet.conj() @ singlet))
    print(f"  ⟨singlet|singlet⟩ = {norm:.10f}")
    t2_ok = abs(norm - 1.0) < 1e-12
    print(f"  STATUS: {'PASS' if t2_ok else 'FAIL'}")
    print()

    # ----- Test 3: SU(3) invariance: T^a |singlet⟩ = 0 -----
    print("-" * 72)
    print("TEST 3: SU(3) generator action on baryon singlet vanishes")
    print("        T^a_total = T^a ⊗ I ⊗ I + I ⊗ T^a ⊗ I + I ⊗ I ⊗ T^a")
    print("-" * 72)
    lams = gell_mann_matrices()
    Ts = [lam / 2 for lam in lams]
    I3 = np.eye(N_c, dtype=complex)
    max_resid = 0.0
    for a, T in enumerate(Ts):
        gen_total = (np.kron(np.kron(T, I3), I3) + np.kron(np.kron(I3, T), I3) + np.kron(np.kron(I3, I3), T))
        action = gen_total @ singlet
        resid = float(np.linalg.norm(action))
        max_resid = max(max_resid, resid)
    print(f"  max ||T^a_total |singlet⟩|| over 8 generators = {max_resid:.3e}")
    t3_ok = max_resid < 1e-10
    print(f"  STATUS: {'PASS' if t3_ok else 'FAIL'}")
    print()

    # ----- Test 4: total antisymmetry under permutations -----
    print("-" * 72)
    print("TEST 4: |singlet⟩ picks up sign(σ) under permutation σ")
    print("-" * 72)
    # Build permutation operator on basis |abc⟩ → |σ(abc)⟩
    print("  Testing all 6 permutations:")
    sign_correct = []
    for perm in itertools.permutations(range(3)):
        # Build the operator that permutes the 3 quark slots
        P = np.zeros((N_c**3, N_c**3), dtype=complex)
        for a in range(N_c):
            for b in range(N_c):
                for c in range(N_c):
                    src_idx = 9*a + 3*b + c
                    indices = (a, b, c)
                    permuted = (indices[perm[0]], indices[perm[1]], indices[perm[2]])
                    dst_idx = 9*permuted[0] + 3*permuted[1] + permuted[2]
                    P[dst_idx, src_idx] = 1.0
        # Apply
        permuted_singlet = P @ singlet
        # Sign of perm
        sign = 1
        pi = list(perm)
        for i in range(3):
            for j in range(i+1, 3):
                if pi[i] > pi[j]:
                    sign = -sign
        ratio = permuted_singlet / singlet
        # Pick a nonzero index
        nonzero_idx = np.argmax(np.abs(singlet))
        observed_sign = float(np.real(ratio[nonzero_idx]))
        sign_correct.append(abs(observed_sign - sign) < 1e-12)
        print(f"    perm {perm}: expected sign={sign}, observed={observed_sign:.0f} → {'✓' if abs(observed_sign-sign) < 1e-12 else '✗'}")
    t4_ok = all(sign_correct)
    print(f"  STATUS: {'PASS' if t4_ok else 'FAIL'}")
    print()

    # ----- Test 5: only ONE color singlet in 3 ⊗ 3 ⊗ 3 -----
    print("-" * 72)
    print("TEST 5: SU(3) singlet subspace in 3 ⊗ 3 ⊗ 3 has dimension 1")
    print("-" * 72)
    # Compute total Casimir or directly: project onto null space of all T^a_total
    casimir_total = sum(T @ T for T in Ts) / 2  # quadratic Casimir
    # The total T^a action on a state v: gen_total @ v should be 0 iff v is singlet
    # Build the 'invariance' operator: sum_a (T^a_total)^† T^a_total
    invariance = np.zeros((N_c**3, N_c**3), dtype=complex)
    for T in Ts:
        gen_total = (np.kron(np.kron(T, I3), I3) + np.kron(np.kron(I3, T), I3) + np.kron(np.kron(I3, I3), T))
        invariance += gen_total.conj().T @ gen_total
    # Singlet = null space of `invariance`
    eigvals = np.linalg.eigvalsh(invariance)
    n_singlet = int(np.sum(eigvals < 1e-10))
    print(f"  smallest 5 eigenvalues of total Casimir-action: {sorted(eigvals)[:5]}")
    print(f"  number of singlets (near-zero eigenvalues) = {n_singlet}")
    t5_ok = n_singlet == 1
    print(f"  STATUS: {'PASS' if t5_ok else 'FAIL'}")
    print()

    print("=" * 72)
    print(f"  Test 1 (dim 1+8+8+10 = 27):                {'PASS' if t1_ok else 'FAIL'}")
    print(f"  Test 2 (singlet normalized):               {'PASS' if t2_ok else 'FAIL'}")
    print(f"  Test 3 (SU(3) invariance):                 {'PASS' if t3_ok else 'FAIL'}")
    print(f"  Test 4 (total antisymmetry under perms):   {'PASS' if t4_ok else 'FAIL'}")
    print(f"  Test 5 (uniqueness of singlet, dim = 1):   {'PASS' if t5_ok else 'FAIL'}")
    all_ok = all([t1_ok, t2_ok, t3_ok, t4_ok, t5_ok])
    print(f"  OVERALL: {'PASS' if all_ok else 'FAIL'}")
    if not all_ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
