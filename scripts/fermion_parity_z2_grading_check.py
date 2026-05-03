"""Total fermion parity (-1)^Q̂ on framework Fock space.

By axiom_first_lattice_noether (cited), N2 supplies the conserved
fermion-number current with total Q̂. Define the fermion parity operator

    (-1)^Q̂  :=  exp(i π Q̂)

acting on the framework's N-site Fock space H = ⊗_{x=1}^N C².

Then:
  (P1) (-1)^Q̂ is unitary and Hermitian (its own inverse): ((-1)^Q̂)² = I
  (P2) (-1)^Q̂ commutes with H (since [H, Q̂] = 0)
  (P3) Spec((-1)^Q̂) = {+1, -1}
  (P4) Z_2 grading: H = H_even ⊕ H_odd with dim H_even = dim H_odd = 2^{N-1}
  (P5) Local fermion operator a_x is Z_2-odd: (-1)^Q̂ a_x (-1)^Q̂ = -a_x
  (P6) Local fermion bilinear a_x^† a_y is Z_2-even: invariant under (-1)^Q̂

This is the framework's *fermion parity superselection rule*: only Z_2-even
operators (bilinears, currents, energy density) connect physical states.

Tests:
  (T1) (-1)^Q̂ is Hermitian
  (T2) ((-1)^Q̂)² = I
  (T3) [(-1)^Q̂, n̂_x] = 0 for all x (since n̂ is Z_2-even)
  (T4) Spec((-1)^Q̂) = {+1, -1}
  (T5) Z_2-grading dim balance: dim H_even = dim H_odd = 2^{N-1}
  (T6) Z_2-odd action on a_x: {(-1)^Q̂, a_x} = 0
  (T7) Z_2-even action on bilinears: [(-1)^Q̂, a_x^† a_y] = 0
"""
from __future__ import annotations

import numpy as np


def kron_chain(matrices: list[np.ndarray]) -> np.ndarray:
    result = matrices[0]
    for M in matrices[1:]:
        result = np.kron(result, M)
    return result


def main() -> None:
    print("=" * 72)
    print("FRAMEWORK FERMION PARITY (-1)^Q̂ AND Z_2 GRADING")
    print("=" * 72)
    print()

    N = 4  # 4-site Fock space
    dim = 2 ** N
    print(f"  Toy model: N = {N} sites, dim = {dim}")
    print()

    a_op = np.array([[0, 1], [0, 0]], dtype=complex)  # σ_+
    a_dag = a_op.conj().T  # σ_-
    n_local = a_dag @ a_op  # diag(0, 1)
    sigma_3 = np.array([[1, 0], [0, -1]], dtype=complex)
    I2 = np.eye(2, dtype=complex)

    def at_site(local_op: np.ndarray, x: int) -> np.ndarray:
        factors = [local_op if i == x else I2 for i in range(N)]
        return kron_chain(factors)

    # Build Q̂_total
    Q_total = sum(at_site(n_local, x) for x in range(N))
    Iden = np.eye(dim, dtype=complex)

    # Build (-1)^Q̂ via spectral decomposition (since Q̂ is diagonal in Fock basis)
    # Easier: use σ_3-formula. n = (I - σ_3)/2, so Q = N/2 - (1/2) Σ σ_3,x
    # Then (-1)^Q = (-1)^{N/2 - (1/2) Σ σ_3} = (-1)^{N/2} · (-1)^{-(1/2) Σ σ_3}
    # = (-1)^{N/2} · ∏_x (-1)^{-σ_3,x / 2}
    # Hmm, easier: (-1)^Q is diagonal in Fock basis with value (-1)^{|ν|} on |ν⟩
    # = ∏_x (-1)^{ν_x} = ∏_x σ_3,x (with appropriate convention)
    # Specifically: ν_x = 0 ↔ σ_3 = +1, ν_x = 1 ↔ σ_3 = -1
    # So (-1)^{ν_x} = +1 if ν_x = 0 (σ_3 = +1), and -1 if ν_x = 1 (σ_3 = -1)
    # i.e. (-1)^{ν_x} = σ_3,x as an eigenvalue
    # So (-1)^Q = ∏_x σ_3,x (tensor product of σ_3's)
    F = kron_chain([sigma_3] * N)  # = ⊗ σ_3

    # Verify F = (-1)^Q on the diagonal
    print(f"  Computing (-1)^Q̂ via product of σ_3 over all sites")
    diag_Q = np.diag(Q_total).real.astype(int)
    diag_F = np.diag(F).real.astype(int)
    expected_F_diag = (-1) ** diag_Q
    formula_dev = np.linalg.norm(diag_F - expected_F_diag)
    print(f"  ||diag((-1)^Q̂) - diag(⊗ σ_3)|| = {formula_dev:.3e}")
    if formula_dev > 1e-10:
        # If formula doesn't match, build directly via spectral decomposition
        print("  (Falling back to direct construction via diag.)")
        F = np.diag((-1.0) ** diag_Q).astype(complex)
    print()

    # ----- Test 1: (-1)^Q̂ is Hermitian -----
    print("-" * 72)
    print("TEST 1: (-1)^Q̂ is Hermitian")
    print("-" * 72)
    dev1 = np.linalg.norm(F - F.conj().T)
    print(f"  ||F - F†|| = {dev1:.3e}")
    t1_ok = dev1 < 1e-12
    print(f"  STATUS: {'PASS' if t1_ok else 'FAIL'}")
    print()

    # ----- Test 2: F² = I (involution) -----
    print("-" * 72)
    print("TEST 2: ((-1)^Q̂)² = I  (involution)")
    print("-" * 72)
    F_sq = F @ F
    dev2 = np.linalg.norm(F_sq - Iden)
    print(f"  ||F² - I|| = {dev2:.3e}")
    t2_ok = dev2 < 1e-12
    print(f"  STATUS: {'PASS' if t2_ok else 'FAIL'}")
    print()

    # ----- Test 3: [F, n̂_x] = 0 (since n̂ is Z_2-even) -----
    print("-" * 72)
    print("TEST 3: [(-1)^Q̂, n̂_x] = 0  for all x  (n̂ is Z_2-even)")
    print("-" * 72)
    max_comm = 0.0
    for x in range(N):
        n_x = at_site(n_local, x)
        comm = F @ n_x - n_x @ F
        d = np.linalg.norm(comm)
        max_comm = max(max_comm, d)
    print(f"  max ||[F, n̂_x]|| = {max_comm:.3e}")
    t3_ok = max_comm < 1e-12
    print(f"  STATUS: {'PASS' if t3_ok else 'FAIL'}")
    print()

    # ----- Test 4: Spec(F) = {+1, -1} -----
    print("-" * 72)
    print("TEST 4: Spec((-1)^Q̂) = {+1, -1}")
    print("-" * 72)
    eigs = sorted(set(np.round(np.linalg.eigvalsh(F).real, 8)))
    print(f"  Distinct eigenvalues: {eigs}")
    t4_ok = eigs == [-1.0, 1.0]
    print(f"  STATUS: {'PASS' if t4_ok else 'FAIL'}")
    print()

    # ----- Test 5: Z_2 grading dim balance -----
    print("-" * 72)
    print(f"TEST 5: dim H_even = dim H_odd = 2^{{N-1}} = {2 ** (N - 1)}")
    print("-" * 72)
    eigvals = np.linalg.eigvalsh(F).real
    n_pos = sum(1 for e in eigvals if e > 0)
    n_neg = sum(1 for e in eigvals if e < 0)
    print(f"  dim H_even (eigenvalue +1) = {n_pos}")
    print(f"  dim H_odd  (eigenvalue -1) = {n_neg}")
    t5_ok = n_pos == 2 ** (N - 1) and n_neg == 2 ** (N - 1)
    print(f"  STATUS: {'PASS' if t5_ok else 'FAIL'}")
    print()

    # ----- Test 6: {F, a_x} = 0 (a_x is Z_2-odd) -----
    print("-" * 72)
    print("TEST 6: {(-1)^Q̂, a_x} = 0  for all x  (a_x is Z_2-odd)")
    print("-" * 72)
    max_anti = 0.0
    for x in range(N):
        # On a tensor product, a_x acting at site x might need Jordan-Wigner-like
        # phases for a true CAR. But the σ_+ at site x without JW string is what
        # we use here (matches the per-site fermion convention; Q̂ is built from
        # n̂_x = a_x^† a_x without JW).
        a_x_op = at_site(a_op, x)
        anti = F @ a_x_op + a_x_op @ F
        d = np.linalg.norm(anti)
        max_anti = max(max_anti, d)
    print(f"  max ||{{F, a_x}}|| = {max_anti:.3e}")
    t6_ok = max_anti < 1e-12
    print(f"  STATUS: {'PASS' if t6_ok else 'FAIL'}")
    print()

    # ----- Test 7: [F, a_x^† a_y] = 0 (bilinears are Z_2-even) -----
    print("-" * 72)
    print("TEST 7: [(-1)^Q̂, a_x^† a_y] = 0  (bilinears are Z_2-even)")
    print("-" * 72)
    max_comm_bil = 0.0
    for x in range(N):
        for y in range(N):
            a_x_dag = at_site(a_dag, x)
            a_y = at_site(a_op, y)
            bil = a_x_dag @ a_y
            comm = F @ bil - bil @ F
            d = np.linalg.norm(comm)
            max_comm_bil = max(max_comm_bil, d)
    print(f"  max ||[F, a_x^† a_y]|| = {max_comm_bil:.3e}")
    t7_ok = max_comm_bil < 1e-12
    print(f"  STATUS: {'PASS' if t7_ok else 'FAIL'}")
    print()

    print("=" * 72)
    print(f"  Test 1 ((-1)^Q̂ Hermitian):                       {'PASS' if t1_ok else 'FAIL'}")
    print(f"  Test 2 (((-1)^Q̂)² = I involution):                {'PASS' if t2_ok else 'FAIL'}")
    print(f"  Test 3 ([F, n̂_x] = 0):                            {'PASS' if t3_ok else 'FAIL'}")
    print(f"  Test 4 (Spec = {{+1, -1}}):                         {'PASS' if t4_ok else 'FAIL'}")
    print(f"  Test 5 (Z_2 grading dim balance):                 {'PASS' if t5_ok else 'FAIL'}")
    print(f"  Test 6 (a_x is Z_2-odd: {{F, a_x}} = 0):            {'PASS' if t6_ok else 'FAIL'}")
    print(f"  Test 7 (bilinear a_x^† a_y is Z_2-even):           {'PASS' if t7_ok else 'FAIL'}")
    all_ok = all([t1_ok, t2_ok, t3_ok, t4_ok, t5_ok, t6_ok, t7_ok])
    print(f"  OVERALL: {'PASS' if all_ok else 'FAIL'}")
    if not all_ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
