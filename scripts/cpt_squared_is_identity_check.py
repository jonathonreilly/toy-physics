"""(CPT)² = I check on the framework CPT structure."""
from __future__ import annotations

import numpy as np


def main() -> None:
    print("=" * 72)
    print("(CPT)² = I CHECK")
    print("=" * 72)
    print()

    # Build a small toy: 2-site system, C = sublattice parity, P = swap, T = K
    n_sites = 4
    rng = np.random.default_rng(20260502)

    # C: sublattice parity (-1)^x — real diagonal
    C = np.diag([(-1) ** x for x in range(n_sites)]).astype(complex)
    # P: spatial inversion x → -x mod n_sites — real permutation
    P = np.zeros((n_sites, n_sites), dtype=complex)
    for x in range(n_sites):
        P[(-x) % n_sites, x] = 1.0
    # T: complex conjugation operator (applied to states); on operators, T M T = M*
    # For matrix purposes, T is represented by K (the complex conjugation operation),
    # which we apply explicitly.

    CP = C @ P
    print(f"  C is real diagonal: {np.allclose(C.imag, 0)}")
    print(f"  P is real permutation: {np.allclose(P.imag, 0)} and CP is real: {np.allclose(CP.imag, 0)}")
    print()

    # ----- Test 1: (CP)² = I -----
    print("-" * 72)
    print("TEST 1: (CP)² = I (cited from CPT_EXACT_NOTE)")
    print("-" * 72)
    CP_sq = CP @ CP
    cp_resid = np.linalg.norm(CP_sq - np.eye(n_sites))
    print(f"  ||(CP)² - I|| = {cp_resid:.3e}")
    t1_ok = cp_resid < 1e-12
    print(f"  STATUS: {'PASS' if t1_ok else 'FAIL'}")
    print()

    # ----- Test 2: T² = I (complex conjugation squared) -----
    print("-" * 72)
    print("TEST 2: T² = K² = I (complex conjugation squared)")
    print("-" * 72)
    # Apply K twice to a generic complex vector
    psi = rng.standard_normal(n_sites) + 1j * rng.standard_normal(n_sites)
    psi_after = psi.conj().conj()
    diff = np.linalg.norm(psi_after - psi)
    print(f"  ||K² ψ - ψ|| = {diff:.3e}")
    t2_ok = diff < 1e-12
    print(f"  STATUS: {'PASS' if t2_ok else 'FAIL'}")
    print()

    # ----- Test 3: (CPT)² = I on a generic state -----
    print("-" * 72)
    print("TEST 3: (CPT)² ψ = ψ on a generic complex state")
    print("-" * 72)
    # CPT ψ = CP · K ψ = CP · ψ.conj()
    # (CPT)² ψ = CPT · (CP · ψ.conj()) = CP · K · (CP · ψ.conj()) = CP · (CP · ψ.conj()).conj()
    #          = CP · CP* · ψ = (CP)² · ψ = ψ (since (CP)² = I and CP real, CP* = CP)
    psi = rng.standard_normal(n_sites) + 1j * rng.standard_normal(n_sites)
    cpt_psi = CP @ psi.conj()
    cptsq_psi = CP @ cpt_psi.conj()
    diff = np.linalg.norm(cptsq_psi - psi)
    print(f"  ||(CPT)² ψ - ψ|| = {diff:.3e}")
    t3_ok = diff < 1e-12
    print(f"  STATUS: {'PASS' if t3_ok else 'FAIL'}")
    print()

    # ----- Test 4: 5 random states all satisfy (CPT)² = I -----
    print("-" * 72)
    print("TEST 4: 5 random states all satisfy (CPT)² ψ = ψ")
    print("-" * 72)
    max_resid = 0.0
    for trial in range(5):
        psi = rng.standard_normal(n_sites) + 1j * rng.standard_normal(n_sites)
        cptsq = CP @ (CP @ psi.conj()).conj()
        d = np.linalg.norm(cptsq - psi)
        max_resid = max(max_resid, d)
    print(f"  max ||(CPT)² ψ - ψ|| over 5 random ψ = {max_resid:.3e}")
    t4_ok = max_resid < 1e-12
    print(f"  STATUS: {'PASS' if t4_ok else 'FAIL'}")
    print()

    # ----- Summary -----
    print("=" * 72)
    print(f"  Test 1 ((CP)² = I):                     {'PASS' if t1_ok else 'FAIL'}")
    print(f"  Test 2 (T² = I):                        {'PASS' if t2_ok else 'FAIL'}")
    print(f"  Test 3 ((CPT)² ψ = ψ generic):          {'PASS' if t3_ok else 'FAIL'}")
    print(f"  Test 4 (5-trial universality):          {'PASS' if t4_ok else 'FAIL'}")
    all_ok = t1_ok and t2_ok and t3_ok and t4_ok
    print(f"  OVERALL: {'PASS' if all_ok else 'FAIL'}")
    if not all_ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
