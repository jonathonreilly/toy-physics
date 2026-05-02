"""Particle/antiparticle mass equality from retained CPT.

Verifies (M1)-(M3) of CPT_PARTICLE_ANTIPARTICLE_MASS_EQUALITY_THEOREM_-
NOTE_2026-05-02.md on a small explicit CPT-symmetric fermionic
Hamiltonian.

Setup:
  4-mode fermionic Fock space (2 particle modes labeled 'p_0', 'p_1' and
  2 antiparticle modes labeled 'a_0', 'a_1'). CPT acts as the
  antiunitary swap p_i <-> a_i with complex conjugation. We construct
  random Hamiltonians H that satisfy [CPT, H] = 0 by construction
  (symmetrize particle and antiparticle blocks), then verify particle
  and antiparticle eigenvalues are identical.

Tests:
  T1: Hamiltonian Hermiticity sanity.
  T2: [CPT, H] = 0 numerically (CPT-conjugated H equals H).
  T3: spectrum of particle block equals spectrum of antiparticle block
      (M1, M2).
  T4: 5 random CPT-symmetric Hamiltonians all show identical spectra
      (M3 universality).
"""
from __future__ import annotations

import numpy as np


def cpt_symmetric_hamiltonian(seed: int, n_modes: int = 2) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Build a Hermitian Hamiltonian that satisfies [CPT, H] = 0.

    H acts on (particle modes) ⊕ (antiparticle modes), each block of
    dimension n_modes. CPT is the antiunitary swap swap(particle, antiparticle)
    composed with complex conjugation.

    Strategy:
      H = H_p ⊕ H_a in block-diagonal form, with H_a = K H_p K^{-1}
      where K is complex conjugation. Equivalently H_a = H_p^* in matrix form.

    Returns: (H, H_particle_block, H_antiparticle_block).
    """
    rng = np.random.default_rng(seed)
    # Random Hermitian particle block (Hermitian = M + M^†)
    M = rng.standard_normal((n_modes, n_modes)) + 1j * rng.standard_normal((n_modes, n_modes))
    H_p = 0.5 * (M + M.conj().T)
    # Antiparticle block: complex conjugate of particle block (so K H_p K = H_p^* = H_a)
    H_a = H_p.conj()
    # Block-diagonal full H
    full = np.zeros((2 * n_modes, 2 * n_modes), dtype=complex)
    full[:n_modes, :n_modes] = H_p
    full[n_modes:, n_modes:] = H_a
    return full, H_p, H_a


def cpt_operator(n_modes: int = 2) -> tuple[np.ndarray, callable]:
    """CPT acting on the (particle ⊕ antiparticle) block space.

    Antiunitary: swap blocks (matrix S) then complex-conjugate (K).
    We return (S, K_callable) where K_callable applies complex conjugation
    to a given operator/state.
    """
    dim = 2 * n_modes
    S = np.zeros((dim, dim), dtype=complex)
    # Swap: rows i in [0, n_modes) → i + n_modes; rows i in [n_modes, 2n_modes) → i - n_modes
    for i in range(n_modes):
        S[i + n_modes, i] = 1.0
        S[i, i + n_modes] = 1.0
    # K is complex conjugation, applied externally
    K = lambda M: M.conj()
    return S, K


def main() -> None:
    print("=" * 72)
    print("CPT PARTICLE/ANTIPARTICLE MASS EQUALITY CHECK")
    print("=" * 72)
    print()
    print("Setup:")
    print("  4-mode block-Hermitian Hamiltonian on (particle) ⊕ (antiparticle)")
    print("  CPT = swap(p ↔ a) ∘ complex conjugation (antiunitary)")
    print("  Random CPT-symmetric H constructed from random particle block")
    print()

    n_modes = 2
    H, H_p, H_a = cpt_symmetric_hamiltonian(20260502, n_modes)
    S, K = cpt_operator(n_modes)

    # ----- Test 1: Hermiticity -----
    print("-" * 72)
    print("TEST 1: H is Hermitian")
    print("-" * 72)
    herm_resid = np.linalg.norm(H - H.conj().T)
    print(f"  ||H - H^†|| = {herm_resid:.3e}")
    t1_ok = herm_resid < 1e-12
    print(f"  STATUS: {'PASS' if t1_ok else 'FAIL'}")
    print()

    # ----- Test 2: [CPT, H] = 0 -----
    print("-" * 72)
    print("TEST 2: [CPT, H] = 0  (i.e. (CPT) H (CPT)^{-1} = H)")
    print("-" * 72)
    # CPT acting on H (as an operator): (CPT) H (CPT)^{-1} = S K(H) S^{-1} = S H^* S^{-1}
    # Since S is its own inverse (S² = I as a swap), this is S H^* S
    H_cpt = S @ K(H) @ S
    cpt_resid = np.linalg.norm(H_cpt - H)
    print(f"  ||CPT H CPT^{{-1}} - H|| = {cpt_resid:.3e}")
    t2_ok = cpt_resid < 1e-12
    print(f"  STATUS: {'PASS' if t2_ok else 'FAIL'}")
    print()

    # ----- Test 3: particle / antiparticle eigenvalue equality -----
    print("-" * 72)
    print("TEST 3 (M1, M2): particle and antiparticle blocks have")
    print("                 identical spectrum (mass equality)")
    print("-" * 72)
    eigs_p = np.sort(np.linalg.eigvalsh(H_p))
    eigs_a = np.sort(np.linalg.eigvalsh(H_a))
    print(f"  particle block eigenvalues:     {eigs_p.round(8)}")
    print(f"  antiparticle block eigenvalues: {eigs_a.round(8)}")
    diff = np.linalg.norm(eigs_p - eigs_a)
    print(f"  ||eigs_p - eigs_a|| (sorted)    = {diff:.3e}")
    t3_ok = diff < 1e-12
    print(f"  STATUS: {'PASS' if t3_ok else 'FAIL'}")
    print()

    # ----- Test 4: 5 random CPT-symmetric H all show identical spectra -----
    print("-" * 72)
    print("TEST 4 (M3): universality — 5 random CPT-symmetric H all show")
    print("            identical particle/antiparticle spectra")
    print("-" * 72)
    n_trials = 5
    max_diff = 0.0
    for trial in range(n_trials):
        H_t, H_p_t, H_a_t = cpt_symmetric_hamiltonian(20260502 + trial * 100 + 1, n_modes)
        eigs_p_t = np.sort(np.linalg.eigvalsh(H_p_t))
        eigs_a_t = np.sort(np.linalg.eigvalsh(H_a_t))
        d = np.linalg.norm(eigs_p_t - eigs_a_t)
        max_diff = max(max_diff, d)
        print(f"  trial {trial}: particle eigs = {eigs_p_t.round(4)}, antiparticle eigs = {eigs_a_t.round(4)}, |diff| = {d:.2e}")
    print()
    print(f"  max |eigs_p - eigs_a| across {n_trials} trials = {max_diff:.3e}")
    t4_ok = max_diff < 1e-12
    print(f"  STATUS: {'PASS' if t4_ok else 'FAIL'}")
    print()

    # ----- Test 5: counter-example (negative control) -----
    print("-" * 72)
    print("TEST 5 (negative control): a non-CPT-symmetric H DOES break")
    print("                            particle/antiparticle mass equality")
    print("-" * 72)
    # Build H with intentionally different particle and antiparticle blocks
    rng = np.random.default_rng(2026)
    M_p = rng.standard_normal((n_modes, n_modes)) + 1j * rng.standard_normal((n_modes, n_modes))
    H_p_bad = 0.5 * (M_p + M_p.conj().T)
    M_a = rng.standard_normal((n_modes, n_modes)) + 1j * rng.standard_normal((n_modes, n_modes))
    H_a_bad = 0.5 * (M_a + M_a.conj().T)  # different from H_p_bad.conj()
    H_bad = np.zeros((2 * n_modes, 2 * n_modes), dtype=complex)
    H_bad[:n_modes, :n_modes] = H_p_bad
    H_bad[n_modes:, n_modes:] = H_a_bad
    H_bad_cpt = S @ K(H_bad) @ S
    cpt_break = np.linalg.norm(H_bad_cpt - H_bad)
    eigs_p_bad = np.sort(np.linalg.eigvalsh(H_p_bad))
    eigs_a_bad = np.sort(np.linalg.eigvalsh(H_a_bad))
    eigs_diff = np.linalg.norm(eigs_p_bad - eigs_a_bad)
    print(f"  ||CPT H_bad CPT^{{-1}} - H_bad|| = {cpt_break:.3e}  (CPT broken)")
    print(f"  ||eigs_p - eigs_a||              = {eigs_diff:.3e}  (mass equality broken)")
    print(f"  → without CPT, particle/antiparticle spectra differ.")
    t5_ok = cpt_break > 0.1 and eigs_diff > 0.1
    print(f"  STATUS: {'PASS' if t5_ok else 'FAIL'}")
    print()

    # ----- Summary -----
    print("=" * 72)
    print("SUMMARY")
    print("=" * 72)
    print(f"  Test 1 (Hermiticity sanity):                {'PASS' if t1_ok else 'FAIL'}")
    print(f"  Test 2 ([CPT, H] = 0):                      {'PASS' if t2_ok else 'FAIL'}")
    print(f"  Test 3 (M1, M2: identical spectra):         {'PASS' if t3_ok else 'FAIL'}")
    print(f"  Test 4 (M3: universality, 5 trials):        {'PASS' if t4_ok else 'FAIL'}")
    print(f"  Test 5 (negative control: no-CPT breaks):   {'PASS' if t5_ok else 'FAIL'}")
    print()
    all_ok = t1_ok and t2_ok and t3_ok and t4_ok and t5_ok
    print(f"  OVERALL: {'PASS' if all_ok else 'FAIL'}")
    print()
    print("Note: this runner verifies the energy-equality consequence of CPT")
    print("invariance on a 4-mode toy fermionic block-Hamiltonian. The proof")
    print("in the companion theorem note is dimension-independent: it uses")
    print("only [CPT, H] = 0 (retained from cpt_exact_note) plus the standard")
    print("CPT action on particle/antiparticle states. The toy here is a")
    print("structural witness; the full framework matter content has the same")
    print("argument apply to every species in the retained one-generation")
    print("(and three-generation) closure.")
    if not all_ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
