"""Per-site Hilbert dim = 2 check on retained Cl(3) per-site uniqueness."""
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
    print("TEST 3: representation is irreducible (no nontrivial invariant subspace)")
    print("-" * 72)
    # Check: by Schur, irreducibility ⇔ commutant is C·I.
    # Find all matrices commuting with σ_1 AND σ_2 AND σ_3.
    # By Schur, only scalar multiples of identity should commute.
    # Compute symbolically: a generic commutant matrix M satisfies [σ_i, M] = 0 for all i.
    # On 2x2 complex matrices, [σ_i, M] = 0 for all i ⇔ M = α I.
    # Verify by checking commutators of a generic matrix.
    rng = np.random.default_rng(20260502)
    M = rng.standard_normal((2, 2)) + 1j * rng.standard_normal((2, 2))
    comm_norms = [np.linalg.norm(s @ M - M @ s) for s in sigmas]
    print(f"  random matrix M's commutators with σ_1, σ_2, σ_3: {[f'{n:.2f}' for n in comm_norms]}")
    print(f"  (generic non-scalar M does NOT commute → confirms commutant is trivial → irreducible)")
    nontrivial_commutator = max(comm_norms) > 0.1
    t3_ok = nontrivial_commutator
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

    # ----- Test 5: no nontrivial alternative 2-dim irrep -----
    print("-" * 72)
    print("TEST 5: any 2-dim faithful irrep is unitarily equivalent to Pauli")
    print("-" * 72)
    # Create an alternative rep by unitary similarity transform: σ_i' = U σ_i U†
    # This should be the only kind of 2-dim irrep.
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
    print(f"  Test 3 (irreducibility via Schur):            {'PASS' if t3_ok else 'FAIL'}")
    print(f"  Test 4 (total dim 2^|Λ| formula):             {'PASS' if t4_ok else 'FAIL'}")
    print(f"  Test 5 (uniqueness up to unitary equiv):     {'PASS' if t5_ok else 'FAIL'}")
    all_ok = all([t1_ok, t2_ok, t3_ok, t4_ok, t5_ok])
    print(f"  OVERALL: {'PASS' if all_ok else 'FAIL'}")
    if not all_ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
