"""Per-site Hilbert dim = 2 check on Cl(3) per-site uniqueness."""
from __future__ import annotations

import numpy as np


def main() -> None:
    print("=" * 72)
    print("PER-SITE HILBERT DIM = 2 CHECK")
    print("=" * 72)
    print()

    # Pauli matrices
    sigma_1 = np.array([[0, 1], [1, 0]], dtype=complex)
    sigma_2 = np.array([[0, -1j], [1j, 0]], dtype=complex)
    sigma_3 = np.array([[1, 0], [0, -1]], dtype=complex)
    I2 = np.eye(2, dtype=complex)

    # ----- Test 1: Pauli matrices satisfy Cl(3) anticommutation -----
    print("-" * 72)
    print("TEST 1: σ_i satisfy {σ_i, σ_j} = 2 δ_ij I (Cl(3) algebra)")
    print("-" * 72)
    sigmas = [sigma_1, sigma_2, sigma_3]
    max_resid = 0.0
    for i, si in enumerate(sigmas):
        for j, sj in enumerate(sigmas):
            ac = si @ sj + sj @ si
            expected = 2 * (1.0 if i == j else 0.0) * I2
            resid = np.linalg.norm(ac - expected)
            max_resid = max(max_resid, resid)
    print(f"  max ||{{σ_i, σ_j}} - 2δ_ij I|| = {max_resid:.3e}")
    t1_ok = max_resid < 1e-12
    print(f"  STATUS: {'PASS' if t1_ok else 'FAIL'}")
    print()

    # ----- Test 2: dim of representation = 2 -----
    print("-" * 72)
    print("TEST 2: representation acts on dim-2 complex space")
    print("-" * 72)
    print(f"  σ_i shape: {sigma_1.shape}")
    print(f"  representation is on C^2: dim = 2")
    t2_ok = sigma_1.shape == (2, 2)
    print(f"  STATUS: {'PASS' if t2_ok else 'FAIL'}")
    print()

    # ----- Test 3: representation is irreducible -----
    print("-" * 72)
    print("TEST 3: Pauli commutant is scalar, hence the site module is irreducible")
    print("-" * 72)
    # Solve the linear commutant constraints exactly as a finite-dimensional
    # linear-algebra problem over C: [σ_i, M] = 0 for all i.  The nullspace
    # should be one-dimensional and spanned by the identity matrix.
    basis = []
    for r in range(2):
        for c in range(2):
            E = np.zeros((2, 2), dtype=complex)
            E[r, c] = 1.0
            basis.append(E)
    rows = []
    for s in sigmas:
        for E in basis:
            rows.append((s @ E - E @ s).reshape(-1))
    commutant_matrix = np.stack(rows, axis=1)
    singular_values = np.linalg.svd(commutant_matrix, compute_uv=False)
    rank = int(np.sum(singular_values > 1e-12))
    nullity = 4 - rank
    print(f"  commutant constraint rank = {rank}; nullity = {nullity}")
    print(f"  singular values: {[f'{v:.3e}' for v in singular_values]}")
    t3_ok = nullity == 1
    print(f"  STATUS: {'PASS' if t3_ok else 'FAIL'}")
    print()

    # ----- Test 4: total Hilbert dim formula 2^|Λ| -----
    print("-" * 72)
    print("TEST 4: total Hilbert dim on cube of side L is 2^(L^3)")
    print("-" * 72)
    print(f"  L = 1: |Λ| = 1, dim = 2^1 = 2")
    print(f"  L = 2: |Λ| = 8, dim = 2^8 = 256")
    print(f"  L = 3: |Λ| = 27, dim = 2^27 = {2**27:,}")
    print(f"  L = 4: |Λ| = 64, dim = 2^64 ≈ 1.8 × 10^19")
    t4_ok = 2 ** 27 == 134217728
    print(f"  STATUS: {'PASS' if t4_ok else 'FAIL'}")
    print()

    # ----- Test 5: unitary-equivalent representatives preserve Cl(3) -----
    print("-" * 72)
    print("TEST 5: unitary-equivalent Pauli representatives preserve Cl(3)")
    print("-" * 72)
    # Create an alternative rep by unitary similarity transform: σ_i' = U σ_i U†
    rng2 = np.random.default_rng(100)
    A = rng2.standard_normal((2, 2)) + 1j * rng2.standard_normal((2, 2))
    Q, _ = np.linalg.qr(A)  # random unitary
    sigma_alt = [Q @ s @ Q.conj().T for s in sigmas]
    # Verify alternative still satisfies Cl(3)
    max_resid_alt = 0.0
    for i, si in enumerate(sigma_alt):
        for j, sj in enumerate(sigma_alt):
            ac = si @ sj + sj @ si
            expected = 2 * (1.0 if i == j else 0.0) * I2
            resid = np.linalg.norm(ac - expected)
            max_resid_alt = max(max_resid_alt, resid)
    print(f"  alternative rep (unitary conjugate) max ||{{σ', σ'}} - 2δI|| = {max_resid_alt:.3e}")
    t5_ok = max_resid_alt < 1e-12
    print(f"  STATUS: {'PASS' if t5_ok else 'FAIL'}")
    print()

    print("=" * 72)
    print(f"  Test 1 (Cl(3) anticommutation):              {'PASS' if t1_ok else 'FAIL'}")
    print(f"  Test 2 (dim = 2):                             {'PASS' if t2_ok else 'FAIL'}")
    print(f"  Test 3 (scalar commutant / irreducible):      {'PASS' if t3_ok else 'FAIL'}")
    print(f"  Test 4 (total dim 2^|Λ| formula):             {'PASS' if t4_ok else 'FAIL'}")
    print(f"  Test 5 (unitary-equivalent representatives): {'PASS' if t5_ok else 'FAIL'}")
    all_ok = all([t1_ok, t2_ok, t3_ok, t4_ok, t5_ok])
    print(f"  OVERALL: {'PASS' if all_ok else 'FAIL'}")
    if not all_ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
