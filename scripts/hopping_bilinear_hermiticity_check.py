"""Hopping bilinear H_{xy} = a_x^† a_y + a_y^† a_x is Hermitian and translation-covariant.

By axiom_first_lattice_noether (cited, supplies translations T_a) and
axiom_first_cl3_per_site_uniqueness (cited, supplies per-site Pauli C²
with fermion ops a_x, a_x^†), the Hermitian symmetric hopping bilinear

    H_{xy}  :=  a_x^† a_y  +  a_y^† a_x

between sites x and y is the building block of any tight-binding lattice
Hamiltonian. The key structural facts:

  (H1) Hermiticity: (H_{xy})^† = H_{xy}
  (H2) Translation covariance: T_a H_{xy} T_a^† = H_{x+a, y+a}
  (H3) Sum H = Σ_{⟨xy⟩} H_{xy} over translation-invariant link family
       commutes with every T_a
  (H4) Reality: ⟨ν|H_{xy}|μ⟩ ∈ R for binary occupation states ν, μ
  (H5) Particle-number conservation: [H_{xy}, Q̂] = 0
  (H6) Spectrum is real (since Hermitian)
  (H7) H_{xy} swaps occupations between x and y, preserving global Q̂
"""
from __future__ import annotations

import itertools

import numpy as np


def kron_chain(matrices: list[np.ndarray]) -> np.ndarray:
    result = matrices[0]
    for M in matrices[1:]:
        result = np.kron(result, M)
    return result


def main() -> None:
    print("=" * 72)
    print("HOPPING BILINEAR H_{xy} = a_x^† a_y + h.c. — Hermitian + translation-covariant")
    print("=" * 72)
    print()

    L = 4  # 4×4×4 periodic lattice
    n_sites = L ** 3
    dim = 2 ** n_sites

    print(f"  Toy model: 4×4×4 = {n_sites} sites; dim Fock = 2^{n_sites} = ... (too big)")
    print(f"  Use 1D toy: N = 4 sites, dim = 16")
    print()
    N = 4
    dim = 2 ** N

    a_op = np.array([[0, 1], [0, 0]], dtype=complex)
    a_dag = a_op.conj().T
    n_local = a_dag @ a_op
    I2 = np.eye(2, dtype=complex)

    def at_site(local_op: np.ndarray, x: int) -> np.ndarray:
        factors = [local_op if i == x else I2 for i in range(N)]
        return kron_chain(factors)

    # Build T_a: cyclic shift on N sites (1D), site x ↦ site x+1 (mod N)
    # In kron convention site 0 = leftmost factor, so basis index has site 0 at
    # bit position N-1. Translation x ↦ x+1 means site contents move: site 0
    # contents go to site 1, etc., which in bit positions means bit (N-1) → bit (N-2),
    # i.e. RIGHT shift of the bit pattern.
    T = np.zeros((dim, dim), dtype=complex)
    for b in range(dim):
        # Right cyclic shift of bits: bit k → bit k-1, bit 0 wraps to bit N-1
        b_shifted = ((b >> 1) | ((b & 1) << (N - 1))) & ((1 << N) - 1)
        T[b_shifted, b] = 1.0

    # Hopping bilinear at link (x, y)
    def hopping(x: int, y: int) -> np.ndarray:
        return at_site(a_dag, x) @ at_site(a_op, y) + at_site(a_dag, y) @ at_site(a_op, x)

    # ----- Test 1: H_{xy} Hermitian -----
    print("-" * 72)
    print("TEST 1: H_{xy} = a_x^† a_y + a_y^† a_x is Hermitian")
    print("-" * 72)
    max_h = 0.0
    test_links = [(0, 1), (1, 2), (0, 3), (1, 3)]
    for x, y in test_links:
        H_xy = hopping(x, y)
        d = np.linalg.norm(H_xy - H_xy.conj().T)
        max_h = max(max_h, d)
    print(f"  max ||H_{{xy}} - H_{{xy}}†|| = {max_h:.3e}")
    t1_ok = max_h < 1e-12
    print(f"  STATUS: {'PASS' if t1_ok else 'FAIL'}")
    print()

    # ----- Test 2: Translation covariance T H_{xy} T† = H_{x+1, y+1} -----
    print("-" * 72)
    print("TEST 2: T H_{xy} T^† = H_{x+1, y+1}  (mod N for periodic)")
    print("-" * 72)
    max_cov = 0.0
    for x, y in test_links:
        H_xy = hopping(x, y)
        H_xy_shifted = T @ H_xy @ T.conj().T
        H_expected = hopping((x + 1) % N, (y + 1) % N)
        d = np.linalg.norm(H_xy_shifted - H_expected)
        max_cov = max(max_cov, d)
        print(f"  link ({x},{y}) → ({(x+1)%N},{(y+1)%N}): ||·|| = {d:.3e}")
    t2_ok = max_cov < 1e-12
    print(f"  STATUS: {'PASS' if t2_ok else 'FAIL'}")
    print()

    # ----- Test 3: Sum over translation-invariant family commutes with T -----
    print("-" * 72)
    print("TEST 3: H_total = Σ_x H_{x, x+1} commutes with T (translation-invariant)")
    print("-" * 72)
    H_total = sum(hopping(x, (x + 1) % N) for x in range(N))
    comm = T @ H_total - H_total @ T
    d = np.linalg.norm(comm)
    print(f"  ||[T, H_total]|| = {d:.3e}")
    t3_ok = d < 1e-12
    print(f"  STATUS: {'PASS' if t3_ok else 'FAIL'}")
    print()

    # ----- Test 4: Spectrum is real -----
    print("-" * 72)
    print("TEST 4: H_total spectrum is real (Hermitian guaranteed)")
    print("-" * 72)
    eigs = np.linalg.eigvalsh(H_total)
    max_imag = np.max(np.abs(np.linalg.eigvals(H_total).imag))
    print(f"  spectrum range = [{eigs[0]:.4f}, {eigs[-1]:.4f}]")
    print(f"  max |Im(eig)| (using non-Hermitian-aware solver) = {max_imag:.3e}")
    t4_ok = max_imag < 1e-10
    print(f"  STATUS: {'PASS' if t4_ok else 'FAIL'}")
    print()

    # ----- Test 5: Particle-number conservation [H, Q̂] = 0 -----
    print("-" * 72)
    print("TEST 5: [H_{xy}, Q̂_total] = 0  (hopping conserves total fermion number)")
    print("-" * 72)
    Q_total = sum(at_site(n_local, x) for x in range(N))
    max_qcomm = 0.0
    for x, y in test_links:
        H_xy = hopping(x, y)
        comm = H_xy @ Q_total - Q_total @ H_xy
        d = np.linalg.norm(comm)
        max_qcomm = max(max_qcomm, d)
    print(f"  max ||[H_{{xy}}, Q̂]|| = {max_qcomm:.3e}")
    t5_ok = max_qcomm < 1e-12
    print(f"  STATUS: {'PASS' if t5_ok else 'FAIL'}")
    print()

    # ----- Test 6: Hopping action is occupation swap (preserves Q̂) -----
    print("-" * 72)
    print("TEST 6: H_{xy} maps |...n_x = 1, n_y = 0...⟩ ↔ |...n_x = 0, n_y = 1...⟩")
    print("        (occupation swap; preserves total Q̂ = sum)")
    print("-" * 72)
    # State with occupation 1 at site 1 only.
    # In kron convention with N=4: |b_0 b_1 b_2 b_3⟩ where b_i = occupation at site i.
    # Index of state with site 1 occupied: bit pattern (0, 1, 0, 0) at positions
    # (site 0, site 1, site 2, site 3) = bit (N-1-i). For site 1: bit (N-1-1) = bit 2.
    # Index = 1 << 2 = 4.
    state_initial = np.zeros(dim, dtype=complex)
    state_initial[1 << (N - 1 - 1)] = 1.0  # site 1 occupied
    H_01 = hopping(0, 1)
    state_final = H_01 @ state_initial
    # H_{01} maps occupation at site 1 → occupation at site 0 (and vice versa)
    state_target = np.zeros(dim, dtype=complex)
    state_target[1 << (N - 1 - 0)] = 1.0  # site 0 occupied
    overlap = np.abs(np.vdot(state_target, state_final))
    print(f"  ⟨n_0=1, others=0 | H_{{01}} | n_1=1, others=0⟩ = {overlap:.4f}")
    # Also check the reverse via Q̂ preservation
    q_initial = np.real(np.vdot(state_initial, Q_total @ state_initial))
    q_final_norm = np.linalg.norm(state_final)
    q_final = np.real(np.vdot(state_final, Q_total @ state_final)) / (q_final_norm ** 2 + 1e-30)
    print(f"  Q on initial = {q_initial}, Q on final = {q_final}")
    t6_ok = overlap > 0.99 and abs(q_initial - q_final) < 1e-10
    print(f"  STATUS: {'PASS' if t6_ok else 'FAIL'}")
    print()

    # ----- Test 7: Translation invariance of full lattice Hamiltonian -----
    print("-" * 72)
    print("TEST 7: Full Hamiltonian H = Σ_⟨xy⟩ H_{xy} (over nearest-neighbor links)")
    print("        is translation-invariant: T H T^† = H")
    print("-" * 72)
    # Already tested in Test 3 for the 1D chain. Make explicit.
    H_chain = sum(hopping(x, (x + 1) % N) for x in range(N))
    H_chain_shifted = T @ H_chain @ T.conj().T
    d = np.linalg.norm(H_chain_shifted - H_chain)
    print(f"  ||T H T^† - H|| = {d:.3e}")
    t7_ok = d < 1e-12
    print(f"  STATUS: {'PASS' if t7_ok else 'FAIL'}")
    print()

    print("=" * 72)
    print(f"  Test 1 (H_{{xy}} Hermitian):                       {'PASS' if t1_ok else 'FAIL'}")
    print(f"  Test 2 (T H_{{xy}} T^† = H_{{x+1, y+1}} cov):        {'PASS' if t2_ok else 'FAIL'}")
    print(f"  Test 3 ([T, H_total] = 0 (sum is invariant)):     {'PASS' if t3_ok else 'FAIL'}")
    print(f"  Test 4 (spectrum is real):                        {'PASS' if t4_ok else 'FAIL'}")
    print(f"  Test 5 ([H_{{xy}}, Q̂] = 0):                         {'PASS' if t5_ok else 'FAIL'}")
    print(f"  Test 6 (occupation swap):                         {'PASS' if t6_ok else 'FAIL'}")
    print(f"  Test 7 (full Hamiltonian translation-invariant):  {'PASS' if t7_ok else 'FAIL'}")
    all_ok = all([t1_ok, t2_ok, t3_ok, t4_ok, t5_ok, t6_ok, t7_ok])
    print(f"  OVERALL: {'PASS' if all_ok else 'FAIL'}")
    if not all_ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
