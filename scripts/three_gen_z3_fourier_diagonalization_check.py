"""Z_3 Fourier diagonalization on the framework's hw=1 generation triplet.

By three_generation_observable_theorem_note (retained, td=123), the framework's
retained hw=1 sectors {X_1, X_2, X_3} on H_{hw=1} ≅ C^3 carry the cyclic
action of C3[111]: C3[111] · X_a = X_{a+1 mod 3}. Together with the
translation projectors, C3[111] generates the full operator algebra M_3(C).

Define the Z_3 Fourier basis on H_{hw=1}:

    Y_k = (1/√3) Σ_{a=1}^{3} ω^{-(k)(a-1)} X_a    for k = 0, 1, 2

where ω = exp(2πi/3) is the primitive 3rd root of unity.

This block establishes:

(F1) C3[111] is order 3: (C3[111])^3 = I on H_{hw=1}.
(F2) Eigenvalues of C3[111] are exactly {1, ω, ω²}; each multiplicity 1.
(F3) The Fourier basis Y_k diagonalizes C3[111]: C3[111] Y_k = ω^k Y_k.
(F4) Y_k are orthonormal: ⟨Y_k, Y_j⟩ = δ_{kj}.
(F5) The Fourier basis is complete: span_C{Y_0, Y_1, Y_2} = H_{hw=1}.
(F6) Inverse Fourier transform: X_a = (1/√3) Σ_k ω^{(k)(a-1)} Y_k.
(F7) Isotypic decomposition: H_{hw=1} = V_0 ⊕ V_1 ⊕ V_2, with V_k = span{Y_k}
     the k-th Z_3-isotypic component (dim V_k = 1 each).
(F8) C3[111] is unitarily equivalent to the diagonal matrix
     diag(1, ω, ω²) in the Y_k basis.

This is the explicit Z_3 finite-Fourier transform applied to the framework's
specific hw=1 triplet — a concrete diagonalization that the cited theorem
asserts exists (via "C3[111] generates Z_3 action") but does not write down.
"""
from __future__ import annotations

import numpy as np


def main() -> None:
    print("=" * 72)
    print("Z_3 FOURIER DIAGONALIZATION OF C3[111] ON FRAMEWORK hw=1 TRIPLET")
    print("=" * 72)
    print()

    # Build the abstract H_{hw=1} ≅ C^3 with basis {X_1, X_2, X_3}.
    # C3[111] acts as cyclic shift: X_1 → X_2, X_2 → X_3, X_3 → X_1.
    # In matrix form on the X basis (with X_a as standard basis vector e_{a-1}):
    #   C3[111] = [[0, 0, 1], [1, 0, 0], [0, 1, 0]]
    # i.e. C3 e_0 = e_1, C3 e_1 = e_2, C3 e_2 = e_0.
    C3 = np.array([
        [0, 0, 1],
        [1, 0, 0],
        [0, 1, 0],
    ], dtype=complex)
    I3 = np.eye(3, dtype=complex)
    omega = np.exp(2j * np.pi / 3)

    # ----- Test (F1): C3^3 = I -----
    print("-" * 72)
    print("TEST (F1): (C3[111])^3 = I_3  (order-3 unitary)")
    print("-" * 72)
    C3_cubed = C3 @ C3 @ C3
    dev_F1 = np.linalg.norm(C3_cubed - I3)
    print(f"  ||C3^3 - I|| = {dev_F1:.3e}")
    t1 = dev_F1 < 1e-12
    print(f"  STATUS: {'PASS' if t1 else 'FAIL'}")
    print()

    # ----- Test (F2): eigenvalues are exactly {1, ω, ω²} -----
    print("-" * 72)
    print("TEST (F2): Eigenvalues of C3[111] = {1, ω, ω²}")
    print("-" * 72)
    eig = np.linalg.eigvals(C3)
    eig_sorted = sorted(eig.tolist(), key=lambda z: np.angle(z))
    expected = sorted([1.0+0j, omega, omega.conjugate()], key=lambda z: np.angle(z))
    print(f"  Computed eigenvalues: {[f'{e.real:+.4f}{e.imag:+.4f}i' for e in eig_sorted]}")
    print(f"  Expected eigenvalues: {[f'{e.real:+.4f}{e.imag:+.4f}i' for e in expected]}")
    max_eig_dev = max(abs(c - e) for c, e in zip(eig_sorted, expected))
    print(f"  max |computed - expected| = {max_eig_dev:.3e}")
    t2 = max_eig_dev < 1e-10
    print(f"  STATUS: {'PASS' if t2 else 'FAIL'}")
    print()

    # ----- Test (F3): Fourier basis Y_k diagonalizes C3 with eigenvalue ω^k -----
    print("-" * 72)
    print("TEST (F3): C3[111] Y_k = ω^k Y_k  for k = 0, 1, 2")
    print("           where Y_k = (1/√3) Σ_a ω^{-k(a-1)} X_a")
    print("-" * 72)
    Y = np.zeros((3, 3), dtype=complex)  # columns are Y_0, Y_1, Y_2
    for k in range(3):
        for a in range(3):  # a = 0, 1, 2 corresponds to X_1, X_2, X_3
            Y[a, k] = (1 / np.sqrt(3)) * omega ** (-k * a)

    max_diag_dev = 0.0
    for k in range(3):
        Y_k = Y[:, k]
        lhs = C3 @ Y_k
        rhs = (omega ** k) * Y_k
        d = np.linalg.norm(lhs - rhs)
        max_diag_dev = max(max_diag_dev, d)
        print(f"  k={k}: ||C3·Y_k - ω^{k}·Y_k|| = {d:.3e}")
    t3 = max_diag_dev < 1e-10
    print(f"  STATUS: {'PASS' if t3 else 'FAIL'}")
    print()

    # ----- Test (F4): Y_k are orthonormal -----
    print("-" * 72)
    print("TEST (F4): ⟨Y_k, Y_j⟩ = δ_{kj}  (orthonormality)")
    print("-" * 72)
    inner = Y.conj().T @ Y
    inner_dev = np.linalg.norm(inner - I3)
    print(f"  ||Y† Y - I|| = {inner_dev:.3e}")
    t4 = inner_dev < 1e-10
    print(f"  STATUS: {'PASS' if t4 else 'FAIL'}")
    print()

    # ----- Test (F5): Y is complete (basis of H_{hw=1}) -----
    print("-" * 72)
    print("TEST (F5): span{Y_0, Y_1, Y_2} = H_{hw=1}  (basis completeness)")
    print("-" * 72)
    rank_Y = np.linalg.matrix_rank(Y, tol=1e-10)
    completeness_dev = np.linalg.norm(Y @ Y.conj().T - I3)
    print(f"  rank(Y) = {rank_Y}  (full rank = 3)")
    print(f"  ||Y Y† - I|| = {completeness_dev:.3e}  (resolution of identity)")
    t5 = rank_Y == 3 and completeness_dev < 1e-10
    print(f"  STATUS: {'PASS' if t5 else 'FAIL'}")
    print()

    # ----- Test (F6): Inverse Fourier transform: X_a = (1/√3) Σ_k ω^{k(a-1)} Y_k -----
    print("-" * 72)
    print("TEST (F6): X_a = (1/√3) Σ_k ω^{k(a-1)} Y_k  (inverse Fourier)")
    print("-" * 72)
    X = np.eye(3, dtype=complex)  # X_a = e_{a-1}
    max_inv_dev = 0.0
    for a in range(3):
        X_a_reconstruct = np.zeros(3, dtype=complex)
        for k in range(3):
            X_a_reconstruct += (1 / np.sqrt(3)) * (omega ** (k * a)) * Y[:, k]
        d = np.linalg.norm(X[:, a] - X_a_reconstruct)
        max_inv_dev = max(max_inv_dev, d)
    print(f"  max ||X_a - (1/√3) Σ_k ω^{{k(a-1)}} Y_k|| = {max_inv_dev:.3e}")
    t6 = max_inv_dev < 1e-10
    print(f"  STATUS: {'PASS' if t6 else 'FAIL'}")
    print()

    # ----- Test (F7): Isotypic decomposition with each V_k of dimension 1 -----
    print("-" * 72)
    print("TEST (F7): H_{hw=1} = V_0 ⊕ V_1 ⊕ V_2  with dim V_k = 1 each")
    print("           V_k = {v ∈ H_{hw=1} : C3 v = ω^k v}")
    print("-" * 72)
    dims = []
    for k in range(3):
        # Compute the eigenspace of C3 with eigenvalue ω^k by SVD of (C3 - ω^k I)
        proj = C3 - (omega ** k) * I3
        # null space dimension = 3 - rank
        nullity = 3 - np.linalg.matrix_rank(proj, tol=1e-10)
        dims.append(nullity)
        print(f"  V_{k}: eigenspace of C3 for eigenvalue ω^{k}, dim = {nullity}")
    t7 = dims == [1, 1, 1]
    print(f"  STATUS: {'PASS' if t7 else 'FAIL'}")
    print()

    # ----- Test (F8): Diagonalization in Y basis -----
    print("-" * 72)
    print("TEST (F8): C3 in Y basis = diag(1, ω, ω²)")
    print("-" * 72)
    C3_in_Y = Y.conj().T @ C3 @ Y
    expected_diag = np.diag([1, omega, omega ** 2])
    diag_dev = np.linalg.norm(C3_in_Y - expected_diag)
    print(f"  ||Y† C3 Y - diag(1, ω, ω²)|| = {diag_dev:.3e}")
    t8 = diag_dev < 1e-10
    print(f"  STATUS: {'PASS' if t8 else 'FAIL'}")
    print()

    # ----- Test (F9): Cyclic average projector P_cyc = (I + C3 + C3²)/3 -----
    print("-" * 72)
    print("TEST (F9): P_cyc = (1/3)(I + C3 + C3²) is rank-1 projector onto V_0")
    print("           = symmetric 3-singlet subspace")
    print("-" * 72)
    P_cyc = (I3 + C3 + C3 @ C3) / 3.0
    # Verify P² = P
    P_sq = P_cyc @ P_cyc
    idemp_dev = np.linalg.norm(P_sq - P_cyc)
    rank_P = np.linalg.matrix_rank(P_cyc, tol=1e-10)
    # Verify P projects onto V_0 (Y_0 column)
    P_action_on_Y0 = P_cyc @ Y[:, 0]
    proj_on_V0 = np.linalg.norm(P_action_on_Y0 - Y[:, 0])
    print(f"  ||P²cyc - P_cyc|| (idempotency) = {idemp_dev:.3e}")
    print(f"  rank(P_cyc) = {rank_P} (expected 1)")
    print(f"  ||P_cyc Y_0 - Y_0|| (acts as identity on V_0) = {proj_on_V0:.3e}")
    t9 = idemp_dev < 1e-10 and rank_P == 1 and proj_on_V0 < 1e-10
    print(f"  STATUS: {'PASS' if t9 else 'FAIL'}")
    print()

    print("=" * 72)
    print(f"  Test (F1) [C3^3 = I]:                         {'PASS' if t1 else 'FAIL'}")
    print(f"  Test (F2) [eigenvalues = {{1, ω, ω²}}]:        {'PASS' if t2 else 'FAIL'}")
    print(f"  Test (F3) [Fourier diagonalization]:          {'PASS' if t3 else 'FAIL'}")
    print(f"  Test (F4) [orthonormality of Y_k]:            {'PASS' if t4 else 'FAIL'}")
    print(f"  Test (F5) [completeness span{{Y_k}} = H]:      {'PASS' if t5 else 'FAIL'}")
    print(f"  Test (F6) [inverse Fourier]:                  {'PASS' if t6 else 'FAIL'}")
    print(f"  Test (F7) [isotypic decomposition 1+1+1]:     {'PASS' if t7 else 'FAIL'}")
    print(f"  Test (F8) [C3 = diag(1, ω, ω²) in Y basis]:   {'PASS' if t8 else 'FAIL'}")
    print(f"  Test (F9) [P_cyc projector onto V_0]:         {'PASS' if t9 else 'FAIL'}")
    all_ok = all([t1, t2, t3, t4, t5, t6, t7, t8, t9])
    print(f"  OVERALL: {'PASS' if all_ok else 'FAIL'}")
    if not all_ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
