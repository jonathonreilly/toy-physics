#!/usr/bin/env python3
"""
SU(3) Commutant Theorem -- Numerical Verification of Each Proof Step
====================================================================

Companion script to docs/SU3_FORMAL_THEOREM_NOTE.md.
Verifies every algebraic claim in the basis-free proof numerically.

The proof uses:
  - The Kawamoto-Smit (KS) tensor product structure C^8 = C^2 x C^2 x C^2
  - su(2) acting on the first tensor factor (not the bivector su(2))
  - SWAP_{23} exchanging the second and third tensor factors
  - Commutant analysis via Schur's lemma

Self-contained: numpy only.
"""

import sys
import numpy as np

np.set_printoptions(precision=8, linewidth=120)

# ---------------------------------------------------------------------------
# Pauli matrices
# ---------------------------------------------------------------------------
I2 = np.eye(2, dtype=complex)
sx = np.array([[0, 1], [1, 0]], dtype=complex)
sy = np.array([[0, -1j], [1j, 0]], dtype=complex)
sz = np.array([[1, 0], [0, -1]], dtype=complex)
I8 = np.eye(8, dtype=complex)

PASS_COUNT = 0
FAIL_COUNT = 0


def check(name, condition, detail=""):
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if condition else "FAIL"
    if condition:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1
    msg = f"  [{status}] {name}"
    if detail:
        msg += f"  ({detail})"
    print(msg)
    return condition


def commutator(A, B):
    return A @ B - B @ A


def anticommutator(A, B):
    return A @ B + B @ A


def is_close(A, B, tol=1e-10):
    return np.linalg.norm(A - B) < tol


def commutant_basis(operators):
    """Find a basis for the commutant of a set of operators via SVD null space."""
    n = operators[0].shape[0]
    constraints = []
    for Op in operators:
        C = np.kron(Op, np.eye(n)) - np.kron(np.eye(n), Op.T)
        constraints.append(C)
    M = np.vstack(constraints)
    U, S, Vh = np.linalg.svd(M)
    tol = 1e-8
    rank = np.sum(S > tol)
    null_vecs = Vh[rank:].conj().T
    return null_vecs, null_vecs.shape[1]


# ===========================================================================
# STEP 1: KS representation and tensor product structure
# ===========================================================================
def verify_step1():
    print("\n" + "=" * 70)
    print("STEP 1: Kawamoto-Smit representation and tensor product C^2 x C^2 x C^2")
    print("=" * 70)

    # KS Clifford generators
    G1 = np.kron(np.kron(sx, I2), I2)
    G2 = np.kron(np.kron(sz, sx), I2)
    G3 = np.kron(np.kron(sz, sz), sx)
    gammas = [G1, G2, G3]

    # Verify Clifford relations {G_mu, G_nu} = 2 delta_{mu nu} I_8
    for mu in range(3):
        for nu in range(mu, 3):
            ac = anticommutator(gammas[mu], gammas[nu])
            expected = 2.0 * (1 if mu == nu else 0) * I8
            check(
                f"{{Gamma_{mu+1}, Gamma_{nu+1}}} = {2 if mu == nu else 0} I",
                is_close(ac, expected),
            )

    # Verify each Gamma is Hermitian and unitary (squares to I)
    for mu in range(3):
        check(f"Gamma_{mu+1} is Hermitian", is_close(gammas[mu], gammas[mu].conj().T))
        check(f"Gamma_{mu+1}^2 = I", is_close(gammas[mu] @ gammas[mu], I8))

    # Verify the tensor product structure explicitly
    check("G1 = sx x I x I", is_close(G1, np.kron(np.kron(sx, I2), I2)))
    check("G2 = sz x sx x I", is_close(G2, np.kron(np.kron(sz, sx), I2)))
    check("G3 = sz x sz x sx", is_close(G3, np.kron(np.kron(sz, sz), sx)))

    # Verify 2^3 = 8 Clifford products span an 8-dimensional space
    products = [I8]
    for mu in range(3):
        products.append(gammas[mu])
    for mu in range(3):
        for nu in range(mu + 1, 3):
            products.append(gammas[mu] @ gammas[nu])
    products.append(gammas[0] @ gammas[1] @ gammas[2])

    vecs = np.array([p.flatten() for p in products])
    rank = np.linalg.matrix_rank(vecs, tol=1e-10)
    check("8 Clifford products are linearly independent", rank == 8, f"rank = {rank}")

    # Verify the staggered phase structure: G_mu shifts bit mu with sign (-1)^{a_1+...+a_{mu-1}}
    for alpha in range(8):
        a1 = (alpha >> 2) & 1
        a2 = (alpha >> 1) & 1

        beta1 = alpha ^ 4
        check(
            f"G1 shifts site {alpha:03b} -> {beta1:03b} with sign +1",
            abs(G1[beta1, alpha] - 1.0) < 1e-10,
        )

        beta2 = alpha ^ 2
        expected_sign2 = (-1) ** a1
        check(
            f"G2 shifts site {alpha:03b} -> {beta2:03b} with sign {expected_sign2:+.0f}",
            abs(G2[beta2, alpha] - expected_sign2) < 1e-10,
        )

        beta3 = alpha ^ 1
        expected_sign3 = (-1) ** (a1 + a2)
        check(
            f"G3 shifts site {alpha:03b} -> {beta3:03b} with sign {expected_sign3:+.0f}",
            abs(G3[beta3, alpha] - expected_sign3) < 1e-10,
        )

    return gammas


# ===========================================================================
# STEP 2: Distinguished su(2) on the first tensor factor
# ===========================================================================
def verify_step2(gammas):
    print("\n" + "=" * 70)
    print("STEP 2: su(2) on the first tensor factor")
    print("=" * 70)

    T1 = 0.5 * np.kron(np.kron(sx, I2), I2)
    T2 = 0.5 * np.kron(np.kron(sy, I2), I2)
    T3 = 0.5 * np.kron(np.kron(sz, I2), I2)
    T_gens = [T1, T2, T3]

    # Verify su(2) commutation relations
    check("[T1, T2] = i T3", is_close(commutator(T1, T2), 1j * T3))
    check("[T2, T3] = i T1", is_close(commutator(T2, T3), 1j * T1))
    check("[T3, T1] = i T2", is_close(commutator(T3, T1), 1j * T2))

    for k in range(3):
        check(f"T_{k+1} is Hermitian", is_close(T_gens[k], T_gens[k].conj().T))

    # T1 = Gamma_1 / 2
    check("T1 = Gamma_1 / 2", is_close(T1, gammas[0] / 2.0))

    # T2, T3 are NOT in Cl(3)
    cl3_basis = [I8] + list(gammas)
    cl3_basis += [gammas[i] @ gammas[j] for i in range(3) for j in range(i + 1, 3)]
    cl3_basis += [gammas[0] @ gammas[1] @ gammas[2]]
    A = np.array([b.flatten() for b in cl3_basis]).T

    for k, label in [(1, "T2"), (2, "T3")]:
        coeffs = np.linalg.lstsq(A, T_gens[k].flatten(), rcond=None)[0]
        recon = sum(c * b for c, b in zip(coeffs, cl3_basis))
        err = np.linalg.norm(T_gens[k] - recon)
        check(f"{label} is NOT in Cl(3)", err > 0.1, f"reconstruction error = {err:.4f}")

    # Casimir
    S_sq = T1 @ T1 + T2 @ T2 + T3 @ T3
    evals = np.sort(np.linalg.eigvalsh(S_sq.real))
    unique = np.unique(np.round(evals, 6))
    check(
        "Casimir = 3/4 (spin-1/2) x 8",
        len(unique) == 1 and abs(unique[0] - 0.75) < 1e-6,
        f"eigenvalues = {unique}",
    )

    # T_k and bivector B_k are independent
    B1 = -0.5j * gammas[1] @ gammas[2]
    B2 = -0.5j * gammas[2] @ gammas[0]
    B3 = -0.5j * gammas[0] @ gammas[1]

    all_vecs = np.array(
        [T1.flatten(), T2.flatten(), T3.flatten(),
         B1.flatten(), B2.flatten(), B3.flatten()]
    )
    rank = np.linalg.matrix_rank(all_vecs, tol=1e-8)
    check("T_k and bivector B_k are independent (rank 6)", rank == 6, f"rank = {rank}")

    return T_gens


# ===========================================================================
# STEP 3: SWAP_{23} commutes with su(2)
# ===========================================================================
def verify_step3(T_gens):
    print("\n" + "=" * 70)
    print("STEP 3: SWAP_{23} commutes with su(2)")
    print("=" * 70)

    SWAP23 = np.zeros((8, 8), dtype=complex)
    for a in range(2):
        for b in range(2):
            for c in range(2):
                src = 4 * a + 2 * b + c
                dst = 4 * a + 2 * c + b
                SWAP23[dst, src] = 1.0

    check("SWAP23^2 = I", is_close(SWAP23 @ SWAP23, I8))
    check("SWAP23 is Hermitian", is_close(SWAP23, SWAP23.conj().T))

    P_4 = np.zeros((4, 4), dtype=complex)
    for b in range(2):
        for c in range(2):
            P_4[2 * c + b, 2 * b + c] = 1.0
    check("SWAP23 = I_2 x P_4", is_close(SWAP23, np.kron(I2, P_4)))

    for k in range(3):
        comm = commutator(SWAP23, T_gens[k])
        check(f"[SWAP23, T_{k+1}] = 0", is_close(comm, np.zeros((8, 8))))

    # Bivectors do NOT commute with SWAP23
    G1 = np.kron(np.kron(sx, I2), I2)
    G2 = np.kron(np.kron(sz, sx), I2)
    G3 = np.kron(np.kron(sz, sz), sx)
    B1 = -0.5j * G2 @ G3
    B2 = -0.5j * G3 @ G1
    B3 = -0.5j * G1 @ G2

    for k, Bk in enumerate([B1, B2, B3]):
        comm = commutator(SWAP23, Bk)
        check(f"[SWAP23, B_{k+1}] != 0 (bivectors do not commute)", np.linalg.norm(comm) > 0.1)

    return SWAP23


# ===========================================================================
# STEP 4: Sym^2 + Anti^2 decomposition
# ===========================================================================
def verify_step4(SWAP23):
    print("\n" + "=" * 70)
    print("STEP 4: W = Sym^2(C^2) + Anti^2(C^2) = C^3 + C^1")
    print("=" * 70)

    evals = np.sort(np.linalg.eigvalsh(SWAP23.real))
    n_plus = np.sum(evals > 0.5)
    n_minus = np.sum(evals < -0.5)
    check(f"SWAP23 spectrum: +1 x {n_plus}, -1 x {n_minus}", n_plus == 6 and n_minus == 2)

    Pi_plus = (I8 + SWAP23) / 2.0
    Pi_minus = (I8 - SWAP23) / 2.0

    check("Pi_+ is projector", is_close(Pi_plus @ Pi_plus, Pi_plus))
    check("Pi_- is projector", is_close(Pi_minus @ Pi_minus, Pi_minus))
    check("Pi_+ + Pi_- = I", is_close(Pi_plus + Pi_minus, I8))
    check("Pi_+ Pi_- = 0", is_close(Pi_plus @ Pi_minus, np.zeros((8, 8))))
    check("rank(Pi_+) = 6", np.linalg.matrix_rank(Pi_plus, tol=1e-10) == 6)
    check("rank(Pi_-) = 2", np.linalg.matrix_rank(Pi_minus, tol=1e-10) == 2)

    # Verify P_4 on C^4
    P_4 = np.zeros((4, 4), dtype=complex)
    for b in range(2):
        for c in range(2):
            P_4[2 * c + b, 2 * b + c] = 1.0
    evals_4 = np.sort(np.linalg.eigvalsh(P_4.real))
    check("P_4 spectrum: -1 x 1, +1 x 3", np.allclose(evals_4, [-1, 1, 1, 1]))

    # Explicit bases
    e0 = np.array([1, 0], dtype=complex)
    e1 = np.array([0, 1], dtype=complex)
    sym = [np.kron(e0, e0), (np.kron(e0, e1) + np.kron(e1, e0)) / np.sqrt(2), np.kron(e1, e1)]
    anti = [(np.kron(e0, e1) - np.kron(e1, e0)) / np.sqrt(2)]
    for i, v in enumerate(sym):
        check(f"Sym^2 basis {i}: P v = +v", is_close(P_4 @ v, v))
    for i, v in enumerate(anti):
        check(f"Anti^2 basis {i}: P v = -v", is_close(P_4 @ v, -v))

    return Pi_plus, Pi_minus


# ===========================================================================
# STEP 5: Commutant = gl(3) + gl(1)
# ===========================================================================
def verify_step5(T_gens, SWAP23, Pi_plus, Pi_minus):
    print("\n" + "=" * 70)
    print("STEP 5: Commutant of {su(2), SWAP23} = gl(3) + gl(1)")
    print("=" * 70)

    _, dim_su2 = commutant_basis(T_gens)
    check(f"dim Comm(su(2)) = 16", dim_su2 == 16, f"got {dim_su2}")

    null_vecs, dim_both = commutant_basis(T_gens + [SWAP23])
    check(f"dim Comm(su(2), SWAP23) = 10", dim_both == 10, f"got {dim_both}")

    # Block diagonal in Sym/Anti
    n = 8
    comm_matrices = [null_vecs[:, i].reshape(n, n) for i in range(dim_both)]
    for i, M in enumerate(comm_matrices):
        block_diag = Pi_plus @ M @ Pi_plus + Pi_minus @ M @ Pi_minus
        check(f"Comm element {i}: block diagonal", is_close(M, block_diag))

    # Restricted ranks
    evals_s, evecs_s = np.linalg.eigh(SWAP23.real)
    V_plus = evecs_s[:, evals_s > 0.5]
    V_minus = evecs_s[:, evals_s < -0.5]

    rp = [V_plus.conj().T @ M @ V_plus for M in comm_matrices]
    rm = [V_minus.conj().T @ M @ V_minus for M in comm_matrices]

    rank_pp = np.linalg.matrix_rank(np.array([m.flatten() for m in rp]), tol=1e-8)
    rank_mm = np.linalg.matrix_rank(np.array([m.flatten() for m in rm]), tol=1e-8)
    check(f"C^6 block rank = 9", rank_pp == 9, f"got {rank_pp}")
    check(f"C^2 block rank = 1", rank_mm == 1, f"got {rank_mm}")

    # su(3) = Hermitian traceless part
    ht = []
    for M in comm_matrices:
        Mp = V_plus.conj().T @ M @ V_plus
        H = (Mp + Mp.conj().T) / 2.0
        H -= np.trace(H) / 6.0 * np.eye(6)
        if np.linalg.norm(H) > 1e-10:
            ht.append(H)
        A = (Mp - Mp.conj().T) / (2.0j)
        A -= np.trace(A) / 6.0 * np.eye(6)
        if np.linalg.norm(A) > 1e-10:
            ht.append(A)

    rank_ht = np.linalg.matrix_rank(np.array([h.flatten() for h in ht]), tol=1e-8)
    check(f"Hermitian traceless on C^6: rank = 8 = dim su(3)", rank_ht == 8, f"got {rank_ht}")

    print("\n  CONCLUSION: compact semisimple commutant = su(3)")


# ===========================================================================
# STEP 6: Hypercharge
# ===========================================================================
def verify_step6(T_gens, SWAP23, Pi_plus, Pi_minus):
    print("\n" + "=" * 70)
    print("STEP 6: Traceless U(1) = hypercharge")
    print("=" * 70)

    Y = (1.0 / 3.0) * Pi_plus + (-1.0) * Pi_minus

    check("Y is Hermitian", is_close(Y, Y.conj().T))
    check("Tr(Y) = 0", abs(np.trace(Y)) < 1e-10)

    evals = np.sort(np.linalg.eigvalsh(Y.real))
    check("Y = +1/3 x 6", np.sum(np.abs(evals - 1.0 / 3.0) < 1e-6) == 6)
    check("Y = -1 x 2", np.sum(np.abs(evals + 1.0) < 1e-6) == 2)

    for k in range(3):
        check(f"[Y, T_{k+1}] = 0", is_close(commutator(Y, T_gens[k]), np.zeros((8, 8))))
    check("[Y, SWAP23] = 0", is_close(commutator(Y, SWAP23), np.zeros((8, 8))))

    print("\n  C^8 = (2,3)_{+1/3} + (2,1)_{-1}")
    print("       = quark doublet   lepton doublet")


# ===========================================================================
# BONUS: Explicit Gell-Mann generators
# ===========================================================================
def verify_gellmann(T_gens, SWAP23):
    print("\n" + "=" * 70)
    print("BONUS: Explicit Gell-Mann generators")
    print("=" * 70)

    e0 = np.array([1, 0], dtype=complex)
    e1 = np.array([0, 1], dtype=complex)
    U4 = np.column_stack([
        np.kron(e0, e0),
        (np.kron(e0, e1) + np.kron(e1, e0)) / np.sqrt(2),
        np.kron(e1, e1),
        (np.kron(e0, e1) - np.kron(e1, e0)) / np.sqrt(2),
    ])
    check("U4 is unitary", is_close(U4.conj().T @ U4, np.eye(4)))
    U8 = np.kron(I2, U4)

    SWAP_new = U8.conj().T @ SWAP23 @ U8
    expected = np.diag([1, 1, 1, -1, 1, 1, 1, -1]).astype(complex)
    check("SWAP23 diagonal in new basis", is_close(SWAP_new, expected))

    lam = [
        np.array([[0, 1, 0], [1, 0, 0], [0, 0, 0]], dtype=complex),
        np.array([[0, -1j, 0], [1j, 0, 0], [0, 0, 0]], dtype=complex),
        np.array([[1, 0, 0], [0, -1, 0], [0, 0, 0]], dtype=complex),
        np.array([[0, 0, 1], [0, 0, 0], [1, 0, 0]], dtype=complex),
        np.array([[0, 0, -1j], [0, 0, 0], [1j, 0, 0]], dtype=complex),
        np.array([[0, 0, 0], [0, 0, 1], [0, 1, 0]], dtype=complex),
        np.array([[0, 0, 0], [0, 0, -1j], [0, 1j, 0]], dtype=complex),
        np.array([[1, 0, 0], [0, 1, 0], [0, 0, -2]], dtype=complex) / np.sqrt(3),
    ]

    for a_idx, la in enumerate(lam):
        la_4 = np.zeros((4, 4), dtype=complex)
        la_4[:3, :3] = la
        La_8 = U8 @ np.kron(I2, la_4) @ U8.conj().T
        ok = all(
            is_close(commutator(La_8, T_gens[k]), np.zeros((8, 8))) for k in range(3)
        ) and is_close(commutator(La_8, SWAP23), np.zeros((8, 8)))
        check(f"lambda_{a_idx+1}: commutes with su(2) + SWAP", ok)

    # su(3) closure
    T_su3 = []
    for la in lam:
        la_4 = np.zeros((4, 4), dtype=complex)
        la_4[:3, :3] = la
        T_su3.append(U8 @ np.kron(I2, la_4 / 2.0) @ U8.conj().T)

    max_err = 0
    for a in range(8):
        for b in range(a + 1, 8):
            c_ab = commutator(T_su3[a], T_su3[b])
            coeffs = [
                np.trace(c_ab @ T_su3[c].conj().T) /
                np.trace(T_su3[c] @ T_su3[c].conj().T)
                for c in range(8)
            ]
            recon = sum(c * T for c, T in zip(coeffs, T_su3))
            max_err = max(max_err, np.linalg.norm(c_ab - recon))

    check("su(3) closes under commutation", max_err < 1e-8, f"max err = {max_err:.2e}")


# ===========================================================================
# MAIN
# ===========================================================================
def main():
    print("=" * 70)
    print("SU(3) COMMUTANT THEOREM -- NUMERICAL VERIFICATION")
    print("Companion to docs/SU3_FORMAL_THEOREM_NOTE.md")
    print("=" * 70)

    gammas = verify_step1()
    T_gens = verify_step2(gammas)
    SWAP23 = verify_step3(T_gens)
    Pi_plus, Pi_minus = verify_step4(SWAP23)
    verify_step5(T_gens, SWAP23, Pi_plus, Pi_minus)
    verify_step6(T_gens, SWAP23, Pi_plus, Pi_minus)
    verify_gellmann(T_gens, SWAP23)

    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"  Total checks: {PASS_COUNT + FAIL_COUNT}")
    print(f"  Passed: {PASS_COUNT}")
    print(f"  Failed: {FAIL_COUNT}")

    if FAIL_COUNT == 0:
        print("\n  ALL CHECKS PASSED")
        print("  Every algebraic claim in the formal proof is numerically verified.")
    else:
        print(f"\n  WARNING: {FAIL_COUNT} checks FAILED")

    return FAIL_COUNT


if __name__ == "__main__":
    sys.exit(main())
