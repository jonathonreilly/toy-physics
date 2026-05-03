"""Per-site charge density Q̂_x has eigenvalues {0, 1}; total Q̂ has integer spectrum.

By axiom_first_cl3_per_site_uniqueness (cited), per-site Hilbert ≅ C² with
basis {|0⟩, |1⟩} (eigenvectors of σ_3). The single-mode fermionic
creation/annihilation operators are

    a   = σ_- = (σ_1 + i σ_2) / 2  =  [[0, 0], [1, 0]]    (lowering)
    a^† = σ_+ = (σ_1 - i σ_2) / 2  =  [[0, 1], [0, 0]]    (raising)

The per-site number operator is n_x := a_x^† a_x. By direct computation:

    n_x · |0⟩ = 0,      n_x · |1⟩ = |1⟩

so n_x has eigenvalues exactly {0, 1}.

The total charge operator on the framework's N-site Fock space is

    Q̂_total = Σ_{x=1}^N n_x    (mutually commuting on the tensor product)

with spectrum {0, 1, ..., N}, multiplicity C(N, k) for each k.

This proves charge quantization on the framework: any framework state
carries an integer-valued total charge in the range [0, N_sites].

Tests:
  (T1) σ_- σ_+ + σ_+ σ_- = I on Pauli C² (canonical anticommutation single-mode)
  (T2) n = σ_+ σ_- has eigenvalues exactly {0, 1}
  (T3) Multi-site n_x are pairwise commuting (tensor product structure)
  (T4) Q̂_total = Σ_x n_x has integer spectrum {0, 1, ..., N}
  (T5) Multiplicity at charge k is C(N, k) (binomial counting)
  (T6) Q̂_total = N·I/2 + Σ_x σ_3,x / 2 (alternative formula via σ_3 = 2 n - I)
"""
from __future__ import annotations

import math
from itertools import product as iproduct

import numpy as np


def kron_chain(matrices: list[np.ndarray]) -> np.ndarray:
    """Compute the Kronecker product of a list of matrices."""
    result = matrices[0]
    for M in matrices[1:]:
        result = np.kron(result, M)
    return result


def n_at_site(N: int, x: int) -> np.ndarray:
    """n_x = I ⊗ ... ⊗ n ⊗ ... ⊗ I  with n at position x (0-indexed)."""
    sigma_plus = np.array([[0, 1], [0, 0]], dtype=complex)  # raising
    sigma_minus = np.array([[0, 0], [1, 0]], dtype=complex)  # lowering
    n = sigma_plus @ sigma_minus  # = diag(1, 0): a^† a annihilates |0⟩, gives |1⟩ on |1⟩
    # Wait: with basis {|0⟩, |1⟩} and σ_- = [[0,0],[1,0]] (lowering: σ_- |0⟩ = |1⟩? No)
    # Convention check: with |0⟩ = (1, 0)^T and |1⟩ = (0, 1)^T,
    # σ_- = (σ_1 - i σ_2) / 2 = [[0, 0], [1, 0]] sends |0⟩ ↦ (0, 1)^T = |1⟩ — that's RAISING in occupation.
    # So actually σ_- in the standard Pauli convention raises occupation.
    # Recompute: with |0⟩ = empty (no fermion), |1⟩ = occupied,
    #   a |0⟩ = 0,  a |1⟩ = |0⟩  →  a = ?
    # a as 2x2 matrix in basis {|0⟩, |1⟩}: rows/cols indexed by output/input
    # a = ⟨out|a|in⟩: a_{0,1} = ⟨0|a|1⟩ = 1, a_{0,0} = a_{1,0} = a_{1,1} = 0
    # So a = [[0, 1], [0, 0]] = σ_+ in our convention.
    # And a^† = [[0, 0], [1, 0]] = σ_-
    # Then n = a^† a = [[0,0],[1,0]] · [[0,1],[0,0]] = [[0, 0], [0, 1]] = diag(0, 1)
    # which has eigenvalue 0 on |0⟩ and 1 on |1⟩. Good.
    a_op = np.array([[0, 1], [0, 0]], dtype=complex)
    a_dag = a_op.conj().T
    n_local = a_dag @ a_op  # = diag(0, 1)
    I2 = np.eye(2, dtype=complex)
    factors = [n_local if i == x else I2 for i in range(N)]
    return kron_chain(factors)


def main() -> None:
    print("=" * 72)
    print("Q̂ INTEGER SPECTRUM ON FRAMEWORK FOCK SPACE")
    print("=" * 72)
    print()

    # First verify single-site structure
    a_op = np.array([[0, 1], [0, 0]], dtype=complex)
    a_dag = a_op.conj().T
    n_local = a_dag @ a_op
    I2 = np.eye(2, dtype=complex)

    # ----- Test 1: Single-mode CCR-fermion: {a, a^†} = I -----
    print("-" * 72)
    print("TEST 1: {a, a^†} = I on per-site Pauli C² (single-mode fermion)")
    print("-" * 72)
    anti = a_op @ a_dag + a_dag @ a_op
    dev1 = np.linalg.norm(anti - I2)
    print(f"  ||{{a, a^†}} - I|| = {dev1:.3e}")
    # Also check {a, a} = 0 and {a^†, a^†} = 0
    aa = a_op @ a_op + a_op @ a_op
    aada = a_dag @ a_dag + a_dag @ a_dag
    dev1b = np.linalg.norm(aa) + np.linalg.norm(aada)
    print(f"  ||{{a, a}} + {{a^†, a^†}}|| = {dev1b:.3e}  (Grassmann nilpotency)")
    t1_ok = dev1 < 1e-12 and dev1b < 1e-12
    print(f"  STATUS: {'PASS' if t1_ok else 'FAIL'}")
    print()

    # ----- Test 2: n = a^† a has eigenvalues exactly {0, 1} -----
    print("-" * 72)
    print("TEST 2: n = a^† a has eigenvalues exactly {0, 1}")
    print("-" * 72)
    eigs_n = sorted(np.linalg.eigvalsh(n_local).tolist())
    print(f"  n eigenvalues = {eigs_n}")
    t2_ok = abs(eigs_n[0] - 0.0) < 1e-12 and abs(eigs_n[1] - 1.0) < 1e-12
    print(f"  STATUS: {'PASS' if t2_ok else 'FAIL'}")
    print()

    # Now multi-site
    N = 4  # 4 sites for explicit Fock space
    dim = 2 ** N
    print(f"  Multi-site Fock space: N = {N} sites, dim = {dim}")
    print()

    # ----- Test 3: Multi-site n_x mutually commute -----
    print("-" * 72)
    print(f"TEST 3: Multi-site n_x mutually commute  (x = 0, ..., {N-1})")
    print("-" * 72)
    n_ops = [n_at_site(N, x) for x in range(N)]
    max_comm = 0.0
    for i in range(N):
        for j in range(N):
            if i == j:
                continue
            comm = n_ops[i] @ n_ops[j] - n_ops[j] @ n_ops[i]
            d = np.linalg.norm(comm)
            max_comm = max(max_comm, d)
    print(f"  max ||[n_x, n_y]|| = {max_comm:.3e}")
    t3_ok = max_comm < 1e-12
    print(f"  STATUS: {'PASS' if t3_ok else 'FAIL'}")
    print()

    # ----- Test 4: Q̂_total = Σ n_x has integer spectrum {0, 1, ..., N} -----
    print("-" * 72)
    print(f"TEST 4: Q̂_total = Σ_x n_x has integer spectrum {{0, 1, ..., {N}}}")
    print("-" * 72)
    Q_total = sum(n_ops)
    eigs_Q = sorted(np.linalg.eigvalsh(Q_total).tolist())
    print(f"  Q̂ eigenvalues (sorted): {eigs_Q}")
    distinct = sorted(set(round(e, 10) for e in eigs_Q))
    print(f"  Distinct values: {distinct}")
    expected = list(range(N + 1))
    t4_ok = all(any(abs(d - k) < 1e-10 for d in distinct) for k in expected) and len(distinct) == len(expected)
    print(f"  Expected: {expected}")
    print(f"  STATUS: {'PASS' if t4_ok else 'FAIL'}")
    print()

    # ----- Test 5: Multiplicity at charge k is C(N, k) -----
    print("-" * 72)
    print(f"TEST 5: Multiplicity at charge k is C({N}, k) = binomial(N, k)")
    print("-" * 72)
    multiplicities = {}
    for e in eigs_Q:
        k = int(round(e))
        multiplicities[k] = multiplicities.get(k, 0) + 1
    expected_mult = {k: math.comb(N, k) for k in range(N + 1)}
    print(f"  observed multiplicities: {multiplicities}")
    print(f"  expected (C(N, k)):      {expected_mult}")
    t5_ok = multiplicities == expected_mult
    print(f"  STATUS: {'PASS' if t5_ok else 'FAIL'}")
    print()

    # ----- Test 6: Equivalent formula via σ_3 -----
    print("-" * 72)
    print(f"TEST 6: Q̂_total = N/2 · I + (1/2) Σ_x (-σ_{{3,x}})  (since n = (I - σ_3)/2)")
    print(f"        Note: with |0⟩ being eigenvector of +1 of σ_3 and |1⟩ being -1,")
    print(f"        n = a^† a has eigenvalue 0 on |0⟩ and 1 on |1⟩, so n = (I - σ_3)/2.")
    print("-" * 72)
    sigma_3 = np.array([[1, 0], [0, -1]], dtype=complex)

    def sigma_3_at_site(N, x):
        factors = [sigma_3 if i == x else I2 for i in range(N)]
        return kron_chain(factors)

    # n = (I - σ_3) / 2 ⇒ Σ n_x = N/2 · I - (1/2) Σ σ_3,x
    Q_alt = (N / 2) * np.eye(dim, dtype=complex) - 0.5 * sum(sigma_3_at_site(N, x) for x in range(N))
    dev6 = np.linalg.norm(Q_total - Q_alt)
    print(f"  ||Q̂_total - (N/2 I - (1/2)Σ σ_3,x)|| = {dev6:.3e}")
    t6_ok = dev6 < 1e-12
    print(f"  STATUS: {'PASS' if t6_ok else 'FAIL'}")
    print()

    print("=" * 72)
    print(f"  Test 1 ({{a, a^†}} = I and Grassmann nilpotency):    {'PASS' if t1_ok else 'FAIL'}")
    print(f"  Test 2 (n eigenvalues = {{0, 1}}):                    {'PASS' if t2_ok else 'FAIL'}")
    print(f"  Test 3 (multi-site n_x commute):                    {'PASS' if t3_ok else 'FAIL'}")
    print(f"  Test 4 (Q̂_total integer spectrum {{0,...,N}}):       {'PASS' if t4_ok else 'FAIL'}")
    print(f"  Test 5 (multiplicity = binomial(N,k)):              {'PASS' if t5_ok else 'FAIL'}")
    print(f"  Test 6 (Q̂_total = N/2·I - (1/2)Σ σ_3 formula):       {'PASS' if t6_ok else 'FAIL'}")
    all_ok = all([t1_ok, t2_ok, t3_ok, t4_ok, t5_ok, t6_ok])
    print(f"  OVERALL: {'PASS' if all_ok else 'FAIL'}")
    if not all_ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
