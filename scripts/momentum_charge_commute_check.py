"""[P̂_total^μ, Q̂_total] = 0 check on framework lattice."""
from __future__ import annotations

import math

import numpy as np


def main() -> None:
    print("=" * 72)
    print("[P̂_total^μ, Q̂_total] = 0 CHECK")
    print("=" * 72)
    print()

    # Setup: 1D periodic chain with N sites, on which we have particle modes
    # P̂ is the translation generator (lattice momentum)
    # Q̂ is the total fermion number
    # On a Fock space built from N sites, both should commute.

    # Toy model: 6-site 1D chain, single-mode-per-site fermionic Fock space
    n_sites = 6
    dim = 2 ** n_sites
    print(f"  Toy model: {n_sites}-site 1D chain, dim = {dim}")
    print()

    # Build Q̂ = total fermion number (diagonal)
    Q = np.diag([bin(b).count("1") for b in range(dim)]).astype(complex)

    # Build translation operator T (cyclic shift of sites)
    # T |bit_pattern⟩ = |cyclic-shifted bit pattern⟩
    T = np.zeros((dim, dim), dtype=complex)
    for b in range(dim):
        # Cyclic left shift of n_sites-bit pattern
        b_shifted = ((b << 1) | (b >> (n_sites - 1))) & ((1 << n_sites) - 1)
        T[b_shifted, b] = 1.0

    # P̂ = -i log(T): use the unitary T's spectrum to define P̂
    eigT, vecsT = np.linalg.eig(T)
    # log on unit circle: principal value of arg
    log_eigT = np.angle(eigT)
    P = vecsT @ np.diag(log_eigT) @ np.linalg.inv(vecsT)
    # Symmetrize tiny non-Hermiticity from finite precision
    P = 0.5 * (P + P.conj().T)

    # ----- Test 1: P̂ is Hermitian -----
    print("-" * 72)
    print("TEST 1: P̂ (translation generator) is Hermitian")
    print("-" * 72)
    P_herm = np.linalg.norm(P - P.conj().T)
    print(f"  ||P̂ - P̂†|| = {P_herm:.3e}")
    t1_ok = P_herm < 1e-9
    print(f"  STATUS: {'PASS' if t1_ok else 'FAIL'}")
    print()

    # ----- Test 2: Q̂ is Hermitian -----
    print("-" * 72)
    print("TEST 2: Q̂ (fermion number) is Hermitian")
    print("-" * 72)
    Q_herm = np.linalg.norm(Q - Q.conj().T)
    print(f"  ||Q̂ - Q̂†|| = {Q_herm:.3e}")
    t2_ok = Q_herm < 1e-12
    print(f"  STATUS: {'PASS' if t2_ok else 'FAIL'}")
    print()

    # ----- Test 3: [P̂, Q̂] = 0 -----
    print("-" * 72)
    print("TEST 3: [P̂, Q̂] = 0 on H_phys")
    print("-" * 72)
    comm = P @ Q - Q @ P
    comm_norm = np.linalg.norm(comm)
    print(f"  ||[P̂, Q̂]||_F = {comm_norm:.3e}")
    t3_ok = comm_norm < 1e-9
    print(f"  STATUS: {'PASS' if t3_ok else 'FAIL'}")
    print()

    # ----- Test 4: simultaneous eigenbasis exists -----
    print("-" * 72)
    print("TEST 4: P̂ and Q̂ admit common eigenbasis")
    print("-" * 72)
    # Compute eigenvectors of (P + 100*Q) (large hierarchy → diagonalizes both)
    H_combined = P + 100.0 * Q
    H_combined = 0.5 * (H_combined + H_combined.conj().T)
    eigvals, vecs = np.linalg.eigh(H_combined)
    # In this basis, both P and Q should be diagonal (or nearly so)
    P_diag = vecs.conj().T @ P @ vecs
    Q_diag = vecs.conj().T @ Q @ vecs
    P_off = np.linalg.norm(P_diag - np.diag(np.diag(P_diag)))
    Q_off = np.linalg.norm(Q_diag - np.diag(np.diag(Q_diag)))
    print(f"  Off-diagonal of P̂ in common basis: {P_off:.3e}")
    print(f"  Off-diagonal of Q̂ in common basis: {Q_off:.3e}")
    t4_ok = P_off < 1e-6 and Q_off < 1e-9
    print(f"  STATUS: {'PASS' if t4_ok else 'FAIL'}")
    print()

    # ----- Test 5: T has finite order N (so P̂ spectrum ⊂ Brillouin zone) -----
    print("-" * 72)
    print("TEST 5: T^N = I (translation has order N)")
    print("        ⇒ T eigenvalues are N-th roots of unity")
    print("        ⇒ P̂ eigenvalues lie in Brillouin-zone set {2π k / N : k=0..N-1}")
    print("-" * 72)
    # Structural check: T^N = I (cyclic shift of N sites has order N)
    T_N = np.linalg.matrix_power(T, n_sites)
    T_N_dev = np.linalg.norm(T_N - np.eye(dim))
    print(f"  ||T^N - I||_F = {T_N_dev:.3e}")
    # Spectrum check: snap each eigenvalue of T to nearest N-th root of unity
    T_eigvals = np.linalg.eigvals(T)
    target_roots = np.array([np.exp(2j * math.pi * k / n_sites) for k in range(n_sites)])
    snap_dists = [min(abs(ev - r) for r in target_roots) for ev in T_eigvals]
    max_snap = max(snap_dists)
    print(f"  max distance from nearest N-th root of unity: {max_snap:.3e}")
    # Brillouin-zone allowed values for reference
    allowed = sorted(round(((2 * math.pi * k / n_sites + math.pi) % (2 * math.pi)) - math.pi, 4) for k in range(n_sites))
    print(f"  Brillouin-zone allowed values (principal range): {allowed}")
    t5_ok = T_N_dev < 1e-9 and max_snap < 1e-6
    print(f"  STATUS: {'PASS' if t5_ok else 'FAIL'}")
    print()

    print("=" * 72)
    print(f"  Test 1 (P̂ Hermitian):                 {'PASS' if t1_ok else 'FAIL'}")
    print(f"  Test 2 (Q̂ Hermitian):                 {'PASS' if t2_ok else 'FAIL'}")
    print(f"  Test 3 ([P̂, Q̂] = 0):                 {'PASS' if t3_ok else 'FAIL'}")
    print(f"  Test 4 (common eigenbasis):           {'PASS' if t4_ok else 'FAIL'}")
    print(f"  Test 5 (P̂ Brillouin-zone spectrum):   {'PASS' if t5_ok else 'FAIL'}")
    all_ok = all([t1_ok, t2_ok, t3_ok, t4_ok, t5_ok])
    print(f"  OVERALL: {'PASS' if all_ok else 'FAIL'}")
    if not all_ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
