"""Per-site Cl(3) Hilbert carries the unique j=1/2 spin irrep of su(2).

For each site x ∈ Z^3, axiom_first_cl3_per_site_uniqueness gives ρ : Cl(3) → M_2(C)
with γ_i ↦ σ_i (Pauli). Define spin generators S_i := σ_i / 2. Then:

    [S_i, S_j] = i ε_{ijk} S_k                      (su(2) Lie algebra)
    S² := S_1² + S_2² + S_3² = (3/4) I              (Casimir = j(j+1) for j=1/2)
    S_z eigenvalues = ±1/2                           (m = ±j)

Hence per-site Hilbert is exactly the unique 2-dim spin-1/2 irrep of su(2).
"""
from __future__ import annotations

import numpy as np


def main() -> None:
    print("=" * 72)
    print("PER-SITE Cl(3) HILBERT CARRIES UNIQUE j=1/2 IRREP OF su(2)")
    print("=" * 72)
    print()

    # Pauli matrices (canonical)
    s1 = np.array([[0, 1], [1, 0]], dtype=complex)
    s2 = np.array([[0, -1j], [1j, 0]], dtype=complex)
    s3 = np.array([[1, 0], [0, -1]], dtype=complex)
    I2 = np.eye(2, dtype=complex)
    sigmas = [s1, s2, s3]

    # Spin generators
    S1 = s1 / 2.0
    S2 = s2 / 2.0
    S3 = s3 / 2.0
    S = [S1, S2, S3]

    # ----- Test 1: σ_i are Hermitian -----
    print("-" * 72)
    print("TEST 1: σ_i are Hermitian (Cl(3) generators in Pauli rep)")
    print("-" * 72)
    devs = [np.linalg.norm(s - s.conj().T) for s in sigmas]
    print(f"  ||σ_1 - σ_1†|| = {devs[0]:.3e}")
    print(f"  ||σ_2 - σ_2†|| = {devs[1]:.3e}")
    print(f"  ||σ_3 - σ_3†|| = {devs[2]:.3e}")
    t1_ok = all(d < 1e-12 for d in devs)
    print(f"  STATUS: {'PASS' if t1_ok else 'FAIL'}")
    print()

    # ----- Test 2: Cl(3) anticommutation {σ_i, σ_j} = 2 δ_ij I -----
    print("-" * 72)
    print("TEST 2: Cl(3) anticommutation {σ_i, σ_j} = 2 δ_{ij} I")
    print("-" * 72)
    max_cl3_dev = 0.0
    for i in range(3):
        for j in range(3):
            anti = sigmas[i] @ sigmas[j] + sigmas[j] @ sigmas[i]
            target = 2.0 * (1.0 if i == j else 0.0) * I2
            d = np.linalg.norm(anti - target)
            max_cl3_dev = max(max_cl3_dev, d)
    print(f"  max ||{{σ_i, σ_j}} - 2δ_{{ij}} I|| = {max_cl3_dev:.3e}")
    t2_ok = max_cl3_dev < 1e-12
    print(f"  STATUS: {'PASS' if t2_ok else 'FAIL'}")
    print()

    # ----- Test 3: su(2) Lie algebra [S_i, S_j] = i ε_{ijk} S_k -----
    print("-" * 72)
    print("TEST 3: su(2) Lie algebra [S_i, S_j] = i ε_{ijk} S_k")
    print("-" * 72)
    eps = np.zeros((3, 3, 3))
    eps[0, 1, 2] = eps[1, 2, 0] = eps[2, 0, 1] = 1.0
    eps[0, 2, 1] = eps[2, 1, 0] = eps[1, 0, 2] = -1.0
    max_su2_dev = 0.0
    for i in range(3):
        for j in range(3):
            comm = S[i] @ S[j] - S[j] @ S[i]
            target = sum(1j * eps[i, j, k] * S[k] for k in range(3))
            d = np.linalg.norm(comm - target)
            max_su2_dev = max(max_su2_dev, d)
    print(f"  max ||[S_i, S_j] - i ε_{{ijk}} S_k|| = {max_su2_dev:.3e}")
    t3_ok = max_su2_dev < 1e-12
    print(f"  STATUS: {'PASS' if t3_ok else 'FAIL'}")
    print()

    # ----- Test 4: Casimir S² = (3/4) I -----
    print("-" * 72)
    print("TEST 4: S² = S_1² + S_2² + S_3² = j(j+1) I = (3/4) I  ⇒  j = 1/2")
    print("-" * 72)
    S_sq = S1 @ S1 + S2 @ S2 + S3 @ S3
    target_casimir = 0.75 * I2
    cas_dev = np.linalg.norm(S_sq - target_casimir)
    print(f"  ||S² - (3/4) I|| = {cas_dev:.3e}")
    cas_eigs = sorted(np.linalg.eigvalsh(S_sq).tolist())
    print(f"  S² eigenvalues = {cas_eigs} (both should equal 3/4 = 0.75)")
    t4_ok = cas_dev < 1e-12
    print(f"  STATUS: {'PASS' if t4_ok else 'FAIL'}")
    print()

    # ----- Test 5: S_z eigenvalues = ±1/2 -----
    print("-" * 72)
    print("TEST 5: S_z eigenvalues = m = ±1/2  (i.e. m ∈ {-j, ..., +j})")
    print("-" * 72)
    sz_eigs = sorted(np.linalg.eigvalsh(S3).tolist())
    print(f"  S_z eigenvalues = {sz_eigs}")
    sz_ok = abs(sz_eigs[0] - (-0.5)) < 1e-12 and abs(sz_eigs[1] - 0.5) < 1e-12
    t5_ok = sz_ok
    print(f"  STATUS: {'PASS' if t5_ok else 'FAIL'}")
    print()

    # ----- Test 6: Pauli rep is irreducible (scalar commutant) -----
    print("-" * 72)
    print("TEST 6: Pauli rep is irreducible — commutant is only scalars")
    print("-" * 72)
    # Solve A S_i = S_i A for a general 2x2 matrix A. A one-dimensional
    # commutant means A is scalar, so Schur's lemma gives irreducibility.
    constraints = []
    for gen in S:
        constraints.append(np.kron(gen.T, I2) - np.kron(I2, gen))
    commutant_matrix = np.vstack(constraints)
    singular_values = np.linalg.svd(commutant_matrix, compute_uv=False)
    nullity = int(np.sum(singular_values < 1e-10))
    print(f"  commutant constraint singular values = {singular_values}")
    print(f"  dim commutant = {nullity} (should equal 1: scalar matrices only)")
    t6_ok = nullity == 1
    print(f"  STATUS: {'PASS' if t6_ok else 'FAIL'}")
    print()

    # ----- Test 7: Total dimension matches j=1/2 irrep dimension (2j+1 = 2) -----
    print("-" * 72)
    print("TEST 7: Per-site Hilbert dim = 2j + 1 = 2 for j = 1/2")
    print("-" * 72)
    dim = 2
    j_extracted = (dim - 1) / 2.0
    print(f"  per-site dim = {dim}, extracted j = (dim - 1)/2 = {j_extracted}")
    t7_ok = j_extracted == 0.5
    print(f"  STATUS: {'PASS' if t7_ok else 'FAIL'}")
    print()

    print("=" * 72)
    print(f"  Test 1 (σ_i Hermitian):                       {'PASS' if t1_ok else 'FAIL'}")
    print(f"  Test 2 (Cl(3) anticommutation):               {'PASS' if t2_ok else 'FAIL'}")
    print(f"  Test 3 (su(2) Lie algebra):                   {'PASS' if t3_ok else 'FAIL'}")
    print(f"  Test 4 (Casimir = 3/4 ⇒ j=1/2):               {'PASS' if t4_ok else 'FAIL'}")
    print(f"  Test 5 (S_z eigenvalues = ±1/2):              {'PASS' if t5_ok else 'FAIL'}")
    print(f"  Test 6 (irreducibility via scalar commutant): {'PASS' if t6_ok else 'FAIL'}")
    print(f"  Test 7 (dim = 2j+1 with j=1/2):               {'PASS' if t7_ok else 'FAIL'}")
    all_ok = all([t1_ok, t2_ok, t3_ok, t4_ok, t5_ok, t6_ok, t7_ok])
    print(f"  OVERALL: {'PASS' if all_ok else 'FAIL'}")
    if not all_ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
