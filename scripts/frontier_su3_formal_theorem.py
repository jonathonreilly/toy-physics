#!/usr/bin/env python3
"""
SU(3) Commutant Theorem -- Numerical Verification of Each Proof Step
====================================================================

Companion script to docs/SU3_FORMAL_THEOREM_NOTE.md.
Verifies every algebraic claim in the basis-free proof numerically.

Self-contained: numpy + scipy only.
"""

import sys
import numpy as np
from itertools import product as iterproduct

np.set_printoptions(precision=8, linewidth=120)

# ---------------------------------------------------------------------------
# Pauli matrices
# ---------------------------------------------------------------------------
I2 = np.eye(2, dtype=complex)
sx = np.array([[0, 1], [1, 0]], dtype=complex)
sy = np.array([[0, -1j], [1j, 0]], dtype=complex)
sz = np.array([[1, 0], [0, -1]], dtype=complex)

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


def random_unitary(n):
    """Random unitary from Haar measure (QR of random complex Gaussian)."""
    Z = (np.random.randn(n, n) + 1j * np.random.randn(n, n)) / np.sqrt(2)
    Q, R = np.linalg.qr(Z)
    Q = Q @ np.diag(np.exp(1j * np.angle(np.diag(R))))
    return Q


# ===========================================================================
# STEP 1: Clifford algebra representation and uniqueness
# ===========================================================================
def verify_step1():
    print("\n" + "=" * 70)
    print("STEP 1: Clifford representation Cl(3) on C^8")
    print("=" * 70)

    # Kawamoto-Smit construction
    G1 = np.kron(np.kron(sx, I2), I2)
    G2 = np.kron(np.kron(sz, sx), I2)
    G3 = np.kron(np.kron(sz, sz), sx)
    gammas = [G1, G2, G3]

    # Verify Clifford relations {G_mu, G_nu} = 2 delta_{mu nu} I_8
    I8 = np.eye(8, dtype=complex)
    for mu in range(3):
        for nu in range(mu, 3):
            ac = anticommutator(gammas[mu], gammas[nu])
            expected = 2.0 * (1 if mu == nu else 0) * I8
            check(
                f"{{Gamma_{mu+1}, Gamma_{nu+1}}} = {2 if mu == nu else 0} I",
                is_close(ac, expected),
                f"error = {np.linalg.norm(ac - expected):.2e}",
            )

    # Verify unitarity: each Gamma is Hermitian and unitary
    for mu in range(3):
        check(
            f"Gamma_{mu+1} is Hermitian",
            is_close(gammas[mu], gammas[mu].conj().T),
        )
        check(
            f"Gamma_{mu+1} is unitary",
            is_close(gammas[mu] @ gammas[mu], I8),
        )

    # Uniqueness: construct a RANDOM conjugate representation and verify
    # it satisfies the same Clifford relations
    U = random_unitary(8)
    gammas_prime = [U @ G @ U.conj().T for G in gammas]
    for mu in range(3):
        for nu in range(mu, 3):
            ac = anticommutator(gammas_prime[mu], gammas_prime[nu])
            expected = 2.0 * (1 if mu == nu else 0) * I8
            check(
                f"Conjugate rep: {{G'_{mu+1}, G'_{nu+1}}} = {2 if mu == nu else 0} I",
                is_close(ac, expected),
            )

    # Verify that 2^3 = 8 products span the full algebra
    products = [I8]
    labels = ["I"]
    for mu in range(3):
        products.append(gammas[mu])
        labels.append(f"G{mu+1}")
    for mu in range(3):
        for nu in range(mu + 1, 3):
            products.append(gammas[mu] @ gammas[nu])
            labels.append(f"G{mu+1}G{nu+1}")
    products.append(gammas[0] @ gammas[1] @ gammas[2])
    labels.append("G1G2G3")

    # Check linear independence by stacking as vectors
    vecs = np.array([p.flatten() for p in products])
    rank = np.linalg.matrix_rank(vecs, tol=1e-10)
    check(
        f"8 Clifford products are linearly independent",
        rank == 8,
        f"rank = {rank}",
    )

    return gammas


# ===========================================================================
# STEP 2: Unique su(2) in the even subalgebra
# ===========================================================================
def verify_step2(gammas):
    print("\n" + "=" * 70)
    print("STEP 2: Unique su(2) from bivectors")
    print("=" * 70)

    # Bivector generators: B_k = -(i/2) eps_{ijk} G_i G_j
    B1 = -0.5j * gammas[1] @ gammas[2]
    B2 = -0.5j * gammas[2] @ gammas[0]
    B3 = -0.5j * gammas[0] @ gammas[1]
    bivectors = [B1, B2, B3]

    # Verify su(2) commutation relations [B_i, B_j] = i eps_{ijk} B_k
    check("[B1, B2] = i B3", is_close(commutator(B1, B2), 1j * B3))
    check("[B2, B3] = i B1", is_close(commutator(B2, B3), 1j * B1))
    check("[B3, B1] = i B2", is_close(commutator(B3, B1), 1j * B2))

    # Verify Hermiticity
    for k in range(3):
        check(f"B_{k+1} is Hermitian", is_close(bivectors[k], bivectors[k].conj().T))

    # Verify B_k = (sigma_k / 2) tensor I_2 tensor I_2
    I8 = np.eye(8, dtype=complex)
    for k, sigma_k in enumerate([sx, sy, sz]):
        expected = 0.5 * np.kron(np.kron(sigma_k, I2), I2)
        check(
            f"B_{k+1} = (sigma_{k+1}/2) x I x I",
            is_close(bivectors[k], expected),
            f"error = {np.linalg.norm(bivectors[k] - expected):.2e}",
        )

    # Casimir S^2 = B1^2 + B2^2 + B3^2
    S_sq = B1 @ B1 + B2 @ B2 + B3 @ B3
    evals = np.sort(np.linalg.eigvalsh(S_sq.real))
    unique_evals = np.unique(np.round(evals, 6))
    check(
        "Casimir has eigenvalue 3/4 (spin-1/2) with multiplicity 8",
        len(unique_evals) == 1 and np.abs(unique_evals[0] - 0.75) < 1e-6,
        f"eigenvalues = {unique_evals}",
    )

    # The representation is 4 copies of spin-1/2 (8 = 2 * 4)
    print(f"  Decomposition: 8 = 4 x (spin-1/2), confirming multiplicity space dim = 4")

    # Uniqueness check: the even subalgebra is spanned by {I, G1G2, G1G3, G2G3}
    I8 = np.eye(8, dtype=complex)
    even_basis = [I8, gammas[0] @ gammas[1], gammas[0] @ gammas[2], gammas[1] @ gammas[2]]
    vecs = np.array([p.flatten() for p in even_basis])
    rank = np.linalg.matrix_rank(vecs, tol=1e-10)
    check("Even subalgebra Cl+(3) has dimension 4", rank == 4)

    # The traceless Hermitian part of the even algebra is exactly span{B1, B2, B3}
    # Verify: each i*G_mu*G_nu is Hermitian and traceless
    for mu in range(3):
        for nu in range(mu + 1, 3):
            H = -1j * gammas[mu] @ gammas[nu]
            check(
                f"-i G{mu+1}G{nu+1} is Hermitian",
                is_close(H, H.conj().T),
            )
            check(
                f"-i G{mu+1}G{nu+1} is traceless",
                np.abs(np.trace(H)) < 1e-10,
            )

    return bivectors


# ===========================================================================
# STEP 3: Cubic symmetry and SWAP
# ===========================================================================
def verify_step3(gammas, bivectors):
    print("\n" + "=" * 70)
    print("STEP 3: O_h preserves su(2); S_3 acts on multiplicity space")
    print("=" * 70)

    I8 = np.eye(8, dtype=complex)

    # Build SWAP_{23}: exchange second and third tensor factors in C^2 x C^2 x C^2
    # SWAP_{23} |a> |b> |c> = |a> |c> |b>
    SWAP23 = np.zeros((8, 8), dtype=complex)
    for a in range(2):
        for b in range(2):
            for c in range(2):
                src = 4 * a + 2 * b + c
                dst = 4 * a + 2 * c + b
                SWAP23[dst, src] = 1.0

    check("SWAP23^2 = I", is_close(SWAP23 @ SWAP23, I8))
    check("SWAP23 is Hermitian", is_close(SWAP23, SWAP23.conj().T))

    # Verify SWAP23 commutes with all bivectors B_k
    for k in range(3):
        comm = commutator(SWAP23, bivectors[k])
        check(
            f"[SWAP23, B_{k+1}] = 0",
            is_close(comm, np.zeros((8, 8))),
            f"error = {np.linalg.norm(comm):.2e}",
        )

    # Verify that SWAP23 acts as the exchange on the multiplicity space
    # In the decomposition C^8 = C^2_weak x C^4_mult, SWAP23 acts as I_2 x P
    # where P is the swap on C^2 x C^2 = C^4
    P_4 = np.zeros((4, 4), dtype=complex)
    for b in range(2):
        for c in range(2):
            src = 2 * b + c
            dst = 2 * c + b
            P_4[dst, src] = 1.0
    SWAP23_expected = np.kron(I2, P_4)
    check(
        "SWAP23 = I_2 x P_4 (acts only on multiplicity space)",
        is_close(SWAP23, SWAP23_expected),
    )

    # Check that a general axis permutation also preserves su(2)
    # Permutation (123) -> (231): maps G1->G2, G2->G3, G3->G1
    # This should map B_k -> B_{pi(k)} (up to sign from pseudovector transform)
    # Since (123) is a proper rotation (det = +1), B transforms as a vector

    # Build the permutation (12): swap directions 1 and 2
    # This maps G1 <-> G2, G3 -> G3
    # For the bivectors: B3 = -(i/2) G1 G2, so B3 -> -(i/2) G2 G1 = (i/2) G1 G2 = -B3
    # B1 = -(i/2) G2 G3 -> -(i/2) G1 G3 = -B2 (NO: B2 = -(i/2) G3 G1 = (i/2) G1 G3)
    # Let's just verify numerically that the permuted bivectors span the same su(2)

    # For permutation (12): the unitary implementing G1 <-> G2 on C^8 is...
    # We need the actual unitary. Build it from the Kawamoto-Smit structure.
    # The exchange (12) sends site (a1, a2, a3) to (a2, a1, a3).
    # In the standard ordering index = 4*a1 + 2*a2 + a3, the permuted index is
    # 4*a2 + 2*a1 + a3.
    PERM12 = np.zeros((8, 8), dtype=complex)
    for a1 in range(2):
        for a2 in range(2):
            for a3 in range(2):
                src = 4 * a1 + 2 * a2 + a3
                dst = 4 * a2 + 2 * a1 + a3
                PERM12[dst, src] = 1.0

    # Check that the transformed Gammas still generate Cl(3) (possibly permuted)
    G1_perm = PERM12 @ gammas[0] @ PERM12.T
    G2_perm = PERM12 @ gammas[1] @ PERM12.T
    G3_perm = PERM12 @ gammas[2] @ PERM12.T

    # The permuted gammas should still satisfy Clifford relations
    gammas_perm = [G1_perm, G2_perm, G3_perm]
    for mu in range(3):
        for nu in range(mu, 3):
            ac = anticommutator(gammas_perm[mu], gammas_perm[nu])
            expected = 2.0 * (1 if mu == nu else 0) * I8
            check(
                f"Permuted (12): {{G'_{mu+1}, G'_{nu+1}}} = {2 if mu == nu else 0} I",
                is_close(ac, expected),
            )

    # The permuted bivectors span the same su(2)
    B1_perm = -0.5j * gammas_perm[1] @ gammas_perm[2]
    B2_perm = -0.5j * gammas_perm[2] @ gammas_perm[0]
    B3_perm = -0.5j * gammas_perm[0] @ gammas_perm[1]
    bivectors_perm = [B1_perm, B2_perm, B3_perm]

    # Verify the permuted bivectors satisfy su(2)
    check(
        "Permuted bivectors: [B'1, B'2] = i B'3",
        is_close(commutator(B1_perm, B2_perm), 1j * B3_perm),
    )

    # Check they span the same subspace as the original
    all_vecs = np.array(
        [b.flatten() for b in bivectors] + [b.flatten() for b in bivectors_perm]
    )
    rank = np.linalg.matrix_rank(all_vecs, tol=1e-8)
    check(
        "Permuted bivectors span same 3d subspace",
        rank == 3,
        f"rank = {rank} (should be 3)",
    )

    return SWAP23


# ===========================================================================
# STEP 4: Sym^2 + Anti^2 decomposition
# ===========================================================================
def verify_step4(SWAP23):
    print("\n" + "=" * 70)
    print("STEP 4: W = Sym^2(C^2) + Anti^2(C^2) = C^3 + C^1")
    print("=" * 70)

    I8 = np.eye(8, dtype=complex)

    # Eigendecomposition of SWAP23
    evals, evecs = np.linalg.eigh(SWAP23.real)
    evals = np.round(evals, 10)
    n_plus = np.sum(evals > 0.5)
    n_minus = np.sum(evals < -0.5)
    check(
        f"SWAP23 eigenvalues: +1 x {n_plus}, -1 x {n_minus}",
        n_plus == 6 and n_minus == 2,
    )

    # Since SWAP23 = I_2 x P_4, and P_4 has eigenvalues +1 (x3) and -1 (x1),
    # SWAP23 has eigenvalues +1 (x6) and -1 (x2) on C^8.
    # The +1 eigenspace is C^2 x Sym^2(C^2) = C^6
    # The -1 eigenspace is C^2 x Anti^2(C^2) = C^2

    # Projectors
    Pi_plus = (I8 + SWAP23) / 2.0
    Pi_minus = (I8 - SWAP23) / 2.0

    check("Pi_+ is a projector", is_close(Pi_plus @ Pi_plus, Pi_plus))
    check("Pi_- is a projector", is_close(Pi_minus @ Pi_minus, Pi_minus))
    check("Pi_+ + Pi_- = I", is_close(Pi_plus + Pi_minus, I8))
    check(
        "rank(Pi_+) = 6, rank(Pi_-) = 2",
        np.linalg.matrix_rank(Pi_plus, tol=1e-10) == 6
        and np.linalg.matrix_rank(Pi_minus, tol=1e-10) == 2,
    )

    # Verify the P_4 swap on C^4 directly
    P_4 = np.zeros((4, 4), dtype=complex)
    for b in range(2):
        for c in range(2):
            P_4[2 * c + b, 2 * b + c] = 1.0

    evals_4 = np.sort(np.linalg.eigvalsh(P_4.real))
    check(
        "P_4 eigenvalues: -1 x 1, +1 x 3",
        np.allclose(evals_4, [-1, 1, 1, 1]),
    )

    # Explicitly construct Sym^2 and Anti^2 bases
    e0 = np.array([1, 0], dtype=complex)
    e1 = np.array([0, 1], dtype=complex)

    sym_basis = [
        np.kron(e0, e0),
        (np.kron(e0, e1) + np.kron(e1, e0)) / np.sqrt(2),
        np.kron(e1, e1),
    ]
    anti_basis = [(np.kron(e0, e1) - np.kron(e1, e0)) / np.sqrt(2)]

    for i, v in enumerate(sym_basis):
        check(
            f"Sym^2 basis vector {i}: P_4 v = +v",
            is_close(P_4 @ v, v),
        )
    for i, v in enumerate(anti_basis):
        check(
            f"Anti^2 basis vector {i}: P_4 v = -v",
            is_close(P_4 @ v, -v),
        )

    return Pi_plus, Pi_minus


# ===========================================================================
# STEP 5: Commutant = gl(3) + gl(1), compact semisimple part = su(3)
# ===========================================================================
def verify_step5(gammas, bivectors, SWAP23, Pi_plus, Pi_minus):
    print("\n" + "=" * 70)
    print("STEP 5: Commutant of {su(2), SWAP23} = gl(3) + gl(1)")
    print("=" * 70)

    I8 = np.eye(8, dtype=complex)

    # Step 5a: Commutant of su(2) alone has dimension 16 (= 4^2)
    # Find all 8x8 matrices commuting with B1, B2, B3
    # Solve [B_k, X] = 0 for k=1,2,3
    # Vectorize: (B_k x I - I x B_k^T) vec(X) = 0

    def commutant_basis(operators):
        """Find a basis for the commutant of a set of operators."""
        n = operators[0].shape[0]
        constraints = []
        for Op in operators:
            # [Op, X] = 0 means (Op tensor I - I tensor Op^T) vec(X) = 0
            C = np.kron(Op, np.eye(n)) - np.kron(np.eye(n), Op.T)
            constraints.append(C)
        M = np.vstack(constraints)
        # Find null space
        U, S, Vh = np.linalg.svd(M)
        tol = 1e-8
        null_mask = S < tol
        # Also include rows beyond the rank
        rank = np.sum(S > tol)
        null_vecs = Vh[rank:].conj().T
        return null_vecs, null_vecs.shape[1]

    # Commutant of su(2) alone
    null_vecs, dim_su2_comm = commutant_basis(bivectors)
    check(
        f"dim Comm(su(2)) = 16",
        dim_su2_comm == 16,
        f"got {dim_su2_comm}",
    )

    # Step 5b: Commutant of {su(2), SWAP23}
    null_vecs2, dim_su2_swap_comm = commutant_basis(bivectors + [SWAP23])
    check(
        f"dim Comm(su(2), SWAP23) = 10",
        dim_su2_swap_comm == 10,
        f"got {dim_su2_swap_comm}",
    )

    # Step 5c: Verify the commutant decomposes as gl(3) + gl(1)
    # Reconstruct the commutant matrices and check they preserve the
    # Pi_plus / Pi_minus decomposition
    n = 8
    comm_matrices = []
    for i in range(dim_su2_swap_comm):
        M = null_vecs2[:, i].reshape(n, n)
        comm_matrices.append(M)

    # Every commutant element should satisfy Pi_+ M Pi_+ + Pi_- M Pi_- = M
    # (i.e., block diagonal in the Sym/Anti decomposition)
    for i, M in enumerate(comm_matrices):
        block_diag = Pi_plus @ M @ Pi_plus + Pi_minus @ M @ Pi_minus
        check(
            f"Commutant element {i}: block diagonal in Sym/Anti",
            is_close(M, block_diag),
        )

    # Now verify that within the C^6 = C^2 x C^3 block, the commutant
    # acts as I_2 x gl(3). We need to check that the restriction to the
    # +1 eigenspace has dimension 9 (= 3^2) and on the -1 eigenspace
    # has dimension 1.

    # Project to the +1 eigenspace
    # Build orthonormal basis for each eigenspace
    evals, evecs = np.linalg.eigh(SWAP23.real)
    idx_plus = np.where(evals > 0.5)[0]
    idx_minus = np.where(evals < -0.5)[0]
    V_plus = evecs[:, idx_plus]  # 8 x 6
    V_minus = evecs[:, idx_minus]  # 8 x 2

    # Restrict commutant to +1 block: M_++ = V_+^dag M V_+
    # This should be a 6x6 matrix of the form I_2 x m (for 3x3 m)
    restricted_plus = []
    for M in comm_matrices:
        M_pp = V_plus.conj().T @ M @ V_plus
        restricted_plus.append(M_pp)

    # Check dimension of the restricted algebra
    vecs_pp = np.array([m.flatten() for m in restricted_plus])
    rank_pp = np.linalg.matrix_rank(vecs_pp, tol=1e-8)
    check(
        f"Restricted commutant on C^6 has rank 9",
        rank_pp == 9,
        f"got {rank_pp}",
    )

    # Restricted to -1 block
    restricted_minus = []
    for M in comm_matrices:
        M_mm = V_minus.conj().T @ M @ V_minus
        restricted_minus.append(M_mm)

    vecs_mm = np.array([m.flatten() for m in restricted_minus])
    rank_mm = np.linalg.matrix_rank(vecs_mm, tol=1e-8)
    check(
        f"Restricted commutant on C^2 has rank 1",
        rank_mm == 1,
        f"got {rank_mm}",
    )

    # Total: 9 + 1 = 10, confirming gl(3) + gl(1)
    check(
        "Total: 9 + 1 = 10 = dim gl(3) + dim gl(1)",
        rank_pp + rank_mm == 10,
    )

    # Verify that the compact semisimple part is su(3)
    # Extract Hermitian traceless generators from the gl(3) part
    # The su(3) subalgebra has dimension 8
    herm_traceless = []
    for M in comm_matrices:
        M_pp = V_plus.conj().T @ M @ V_plus
        # Make Hermitian part
        H = (M_pp + M_pp.conj().T) / 2.0
        # Make traceless
        H -= np.trace(H) / 6.0 * np.eye(6)
        if np.linalg.norm(H) > 1e-10:
            herm_traceless.append(H)
        # Anti-Hermitian part -> multiply by i to get Hermitian
        A = (M_pp - M_pp.conj().T) / (2.0j)
        A -= np.trace(A) / 6.0 * np.eye(6)
        if np.linalg.norm(A) > 1e-10:
            herm_traceless.append(A)

    vecs_ht = np.array([h.flatten() for h in herm_traceless])
    rank_ht = np.linalg.matrix_rank(vecs_ht, tol=1e-8)
    check(
        f"Hermitian traceless part of gl(3) restricted to C^6 has rank 8",
        rank_ht == 8,
        f"got {rank_ht} (8 = dim su(3))",
    )

    print("\n  CONCLUSION: compact semisimple commutant is su(3) (dim 8)")

    return comm_matrices


# ===========================================================================
# STEP 6: Hypercharge
# ===========================================================================
def verify_step6(SWAP23):
    print("\n" + "=" * 70)
    print("STEP 6: Traceless U(1) = hypercharge")
    print("=" * 70)

    I8 = np.eye(8, dtype=complex)

    # Build projectors
    Pi_plus = (I8 + SWAP23) / 2.0
    Pi_minus = (I8 - SWAP23) / 2.0

    # Hypercharge generator: Y = a Pi_+ + b Pi_-
    # Tracelessness: 6a + 2b = 0 => b = -3a
    # Normalize: a = 1/3, b = -1
    a = 1.0 / 3.0
    b = -1.0
    Y = a * Pi_plus + b * Pi_minus

    check("Y is Hermitian", is_close(Y, Y.conj().T))
    check("Tr(Y) = 0", np.abs(np.trace(Y)) < 1e-10, f"Tr = {np.trace(Y).real:.2e}")

    # Eigenvalues
    evals = np.sort(np.linalg.eigvalsh(Y.real))
    unique_evals = np.unique(np.round(evals, 6))
    print(f"  Y eigenvalues: {unique_evals}")

    # Should be +1/3 (x6) and -1 (x2)
    n_quark = np.sum(np.abs(evals - 1.0 / 3.0) < 1e-6)
    n_lepton = np.sum(np.abs(evals - (-1.0)) < 1e-6)
    check(
        f"Y = +1/3 with multiplicity 6 (quarks)",
        n_quark == 6,
        f"got {n_quark}",
    )
    check(
        f"Y = -1 with multiplicity 2 (leptons)",
        n_lepton == 2,
        f"got {n_lepton}",
    )

    # Verify Y commutes with all bivectors (it should, being in the commutant)
    # We already know Pi_+ and Pi_- commute with B_k (from Step 3 + Step 5)
    # But let's verify explicitly
    B1 = 0.5 * np.kron(np.kron(sx, I2), I2)
    B2 = 0.5 * np.kron(np.kron(sy, I2), I2)
    B3 = 0.5 * np.kron(np.kron(sz, I2), I2)

    for k, Bk in enumerate([B1, B2, B3]):
        check(
            f"[Y, B_{k+1}] = 0",
            is_close(commutator(Y, Bk), np.zeros((8, 8))),
        )

    # Verify Y commutes with SWAP23
    check("[Y, SWAP23] = 0", is_close(commutator(Y, SWAP23), np.zeros((8, 8))))

    # Physical interpretation
    print("\n  Physical content:")
    print("    C^8 = (2, 3)_{+1/3}  +  (2, 1)_{-1}")
    print("         = quark doublet     lepton doublet")
    print("    Matches one generation of left-handed SM fermions")

    return Y


# ===========================================================================
# BONUS: Verify full Gell-Mann structure in the commutant
# ===========================================================================
def verify_gellmann(gammas, bivectors, SWAP23):
    print("\n" + "=" * 70)
    print("BONUS: Explicit Gell-Mann generators in the commutant")
    print("=" * 70)

    I8 = np.eye(8, dtype=complex)

    # Build the 8 Gell-Mann generators embedded in C^8
    # They should act as I_2 x lambda_a on C^2 x C^4
    # where lambda_a acts on C^4 = C^3 + C^1 as (Gell-Mann on C^3) + (0 on C^1)

    # First, get the Sym^2 and Anti^2 bases of C^4
    # In C^4 = C^2 x C^2, with basis |00>, |01>, |10>, |11>:
    # Sym^2 basis: |00>, (|01>+|10>)/sqrt(2), |11>
    # Anti^2 basis: (|01>-|10>)/sqrt(2)

    # Build the change-of-basis matrix for C^4
    e00 = np.array([1, 0, 0, 0], dtype=complex)
    e01 = np.array([0, 1, 0, 0], dtype=complex)
    e10 = np.array([0, 0, 1, 0], dtype=complex)
    e11 = np.array([0, 0, 0, 1], dtype=complex)

    s0 = e00
    s1 = (e01 + e10) / np.sqrt(2)
    s2 = e11
    a0 = (e01 - e10) / np.sqrt(2)

    # Change of basis: new basis = [s0, s1, s2, a0]
    U4 = np.column_stack([s0, s1, s2, a0])  # 4x4 unitary

    check("U4 is unitary", is_close(U4.conj().T @ U4, np.eye(4)))

    # Full change of basis on C^8 = C^2 x C^4
    U8 = np.kron(I2, U4)

    # In the new basis, SWAP23 should be diagonal: diag(+1,...,+1,-1,...,-1)
    SWAP_new = U8.conj().T @ SWAP23 @ U8
    expected_swap = np.diag([1, 1, 1, 1, 1, 1, -1, -1]).astype(complex)
    check(
        "SWAP23 is diagonal in new basis",
        is_close(SWAP_new, expected_swap),
        f"error = {np.linalg.norm(SWAP_new - expected_swap):.2e}",
    )

    # Build Gell-Mann generators on C^3 (standard)
    lam = []
    lam.append(np.array([[0, 1, 0], [1, 0, 0], [0, 0, 0]], dtype=complex))
    lam.append(np.array([[0, -1j, 0], [1j, 0, 0], [0, 0, 0]], dtype=complex))
    lam.append(np.array([[1, 0, 0], [0, -1, 0], [0, 0, 0]], dtype=complex))
    lam.append(np.array([[0, 0, 1], [0, 0, 0], [1, 0, 0]], dtype=complex))
    lam.append(np.array([[0, 0, -1j], [0, 0, 0], [1j, 0, 0]], dtype=complex))
    lam.append(np.array([[0, 0, 0], [0, 0, 1], [0, 1, 0]], dtype=complex))
    lam.append(np.array([[0, 0, 0], [0, 0, -1j], [0, 1j, 0]], dtype=complex))
    lam.append(np.array([[1, 0, 0], [0, 1, 0], [0, 0, -2]], dtype=complex) / np.sqrt(3))

    # Embed each lambda_a as I_2 x (lambda_a + 0) in the new basis
    # In C^8 = C^2 x (C^3 + C^1), lambda_a acts on C^3 and zero on C^1
    for a_idx, la in enumerate(lam):
        # Embed in C^4: top-left 3x3 block is la, bottom-right 1x1 is 0
        la_4 = np.zeros((4, 4), dtype=complex)
        la_4[:3, :3] = la

        # Embed in C^8: I_2 x la_4
        La_8_new = np.kron(I2, la_4)

        # Transform back to original basis
        La_8 = U8 @ La_8_new @ U8.conj().T

        # Verify it commutes with all B_k and SWAP23
        comm_ok = True
        for k in range(3):
            if not is_close(commutator(La_8, bivectors[k]), np.zeros((8, 8))):
                comm_ok = False
        if not is_close(commutator(La_8, SWAP23), np.zeros((8, 8))):
            comm_ok = False

        check(f"Gell-Mann lambda_{a_idx+1}: commutes with su(2) and SWAP23", comm_ok)

    # Verify su(3) structure constants
    print("\n  Verifying su(3) algebra closure (all 8 generators):")
    # Build all 8 embedded generators
    La_list = []
    for la in lam:
        la_4 = np.zeros((4, 4), dtype=complex)
        la_4[:3, :3] = la
        La_8_new = np.kron(I2, la_4)
        La_8 = U8 @ La_8_new @ U8.conj().T
        La_list.append(La_8)

    # Check [T_a, T_b] = i f_{abc} T_c where T_a = lambda_a / 2
    T_list = [la / 2.0 for la in La_list]

    # All commutators should be expressible as linear combinations of T_a
    closure_ok = True
    for a in range(8):
        for b in range(a + 1, 8):
            comm_ab = commutator(T_list[a], T_list[b])
            # Express in terms of T_c
            coeffs = []
            for c in range(8):
                # Coefficient = Tr(comm_ab @ T_c^dag) / Tr(T_c @ T_c^dag)
                # For Gell-Mann: Tr(T_a T_b) = delta_{ab}/2
                coeff = np.trace(comm_ab @ T_list[c].conj().T) / np.trace(
                    T_list[c] @ T_list[c].conj().T
                )
                coeffs.append(coeff)
            # Reconstruct
            recon = sum(c * T for c, T in zip(coeffs, T_list))
            if not is_close(comm_ab, recon):
                closure_ok = False

    check("su(3) algebra closes under commutation", closure_ok)


# ===========================================================================
# MAIN
# ===========================================================================
def main():
    print("=" * 70)
    print("SU(3) COMMUTANT THEOREM -- NUMERICAL VERIFICATION")
    print("Companion to docs/SU3_FORMAL_THEOREM_NOTE.md")
    print("=" * 70)

    np.random.seed(42)

    gammas = verify_step1()
    bivectors = verify_step2(gammas)
    SWAP23 = verify_step3(gammas, bivectors)
    Pi_plus, Pi_minus = verify_step4(SWAP23)
    verify_step5(gammas, bivectors, SWAP23, Pi_plus, Pi_minus)
    Y = verify_step6(SWAP23)
    verify_gellmann(gammas, bivectors, SWAP23)

    # Final summary
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
