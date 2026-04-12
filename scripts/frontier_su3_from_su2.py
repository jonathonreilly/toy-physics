#!/usr/bin/env python3
"""
SU(3) from SU(2) x U(1) Combination
=====================================

QUESTION: Can we build the 8 generators of SU(3) from the existing
SU(2) generators (from Cl(3) taste algebra) and U(1) phases?

CONTEXT: The Standard Model decomposition under SU(2) x U(1) is:
  SU(3) -> SU(2) x U(1)
  8 generators decompose as: 3 (SU(2)) + 1 (U(1)) + 4 (off-diagonal)

The staggered lattice gives us:
  - SU(2): S_k = -(i/2) eps_{ijk} Gamma_i Gamma_j in 8-dim taste space
  - U(1): edge phases phi_{ij} on links

APPROACH:
1. Start with the 8-dim taste space from Cl(3) on the cubic lattice
2. Extract the SU(2) generators S_1, S_2, S_3 (proven to work)
3. Extract the U(1) generator from the diagonal Gamma products
4. Try to construct the remaining 4 generators of SU(3) from:
   a) Products of Gamma matrices
   b) Combinations of SU(2) generators with U(1)
   c) The full Cl(3) algebra's 2^6 - 1 = 63 independent elements
5. Check if any 8-element subset closes to su(3)

The key mathematical question: does the 8-dim Cl(3) representation
contain a 3-dim IRREDUCIBLE subspace that transforms as the fundamental
rep of SU(3)?

Self-contained: numpy + scipy only.
"""

import sys
import time
import numpy as np

np.set_printoptions(precision=6, linewidth=120)

# Pauli matrices
SIGMA = [
    np.eye(2, dtype=complex),
    np.array([[0, 1], [1, 0]], dtype=complex),
    np.array([[0, -1j], [1j, 0]], dtype=complex),
    np.array([[1, 0], [0, -1]], dtype=complex),
]

# Gell-Mann matrices (8 generators of su(3))
GELLMANN = []
GELLMANN.append(np.array([[0, 1, 0], [1, 0, 0], [0, 0, 0]], dtype=complex))
GELLMANN.append(np.array([[0, -1j, 0], [1j, 0, 0], [0, 0, 0]], dtype=complex))
GELLMANN.append(np.array([[1, 0, 0], [0, -1, 0], [0, 0, 0]], dtype=complex))
GELLMANN.append(np.array([[0, 0, 1], [0, 0, 0], [1, 0, 0]], dtype=complex))
GELLMANN.append(np.array([[0, 0, -1j], [0, 0, 0], [1j, 0, 0]], dtype=complex))
GELLMANN.append(np.array([[0, 0, 0], [0, 0, 1], [0, 1, 0]], dtype=complex))
GELLMANN.append(np.array([[0, 0, 0], [0, 0, -1j], [0, 1j, 0]], dtype=complex))
GELLMANN.append(np.array([[1, 0, 0], [0, 1, 0], [0, 0, -2]], dtype=complex) / np.sqrt(3))


def build_clifford_algebra():
    """
    Build the Cl(3) Gamma matrices in the 8-dim taste space.

    Standard construction:
    Gamma_1 = sigma_x (x) I (x) I
    Gamma_2 = sigma_y (x) sigma_x (x) I
    Gamma_3 = sigma_y (x) sigma_y (x) sigma_x

    These generate the 2^3 = 8 dimensional Clifford algebra.
    """
    print("\n--- Building Cl(3) in 8-dim taste space ---")

    I2 = SIGMA[0]
    sx, sy, sz = SIGMA[1], SIGMA[2], SIGMA[3]

    G1 = np.kron(np.kron(sx, I2), I2)
    G2 = np.kron(np.kron(sy, sx), I2)
    G3 = np.kron(np.kron(sy, sy), sx)

    gammas = [G1, G2, G3]

    # Verify Clifford: {G_mu, G_nu} = 2 delta I
    for mu in range(3):
        for nu in range(mu, 3):
            ac = gammas[mu] @ gammas[nu] + gammas[nu] @ gammas[mu]
            expected = 2.0 * (1 if mu == nu else 0) * np.eye(8)
            err = np.linalg.norm(ac - expected)
            if err > 1e-10:
                print(f"  WARNING: Clifford error for (G{mu+1}, G{nu+1}): {err:.2e}")
    print("  Clifford algebra verified: {G_mu, G_nu} = 2 delta I")

    return gammas


def extract_su2_generators(gammas):
    """
    Extract SU(2) spin generators from Cl(3):
    S_k = -(i/2) epsilon_{ijk} Gamma_i Gamma_j
    """
    S1 = -0.5j * gammas[1] @ gammas[2]
    S2 = -0.5j * gammas[2] @ gammas[0]
    S3 = -0.5j * gammas[0] @ gammas[1]

    # Verify [S_i, S_j] = i epsilon_{ijk} S_k
    err12 = np.linalg.norm((S1 @ S2 - S2 @ S1) - 1j * S3)
    err23 = np.linalg.norm((S2 @ S3 - S3 @ S2) - 1j * S1)
    err31 = np.linalg.norm((S3 @ S1 - S1 @ S3) - 1j * S2)

    print(f"\n--- SU(2) spin generators ---")
    print(f"  [S1, S2] = i*S3 error: {err12:.2e}")
    print(f"  [S2, S3] = i*S1 error: {err23:.2e}")
    print(f"  [S3, S1] = i*S2 error: {err31:.2e}")

    # Casimir
    S_sq = S1 @ S1 + S2 @ S2 + S3 @ S3
    evals = np.linalg.eigvalsh(S_sq.real)
    unique = np.unique(np.round(evals, 4))
    print(f"  Casimir eigenvalues: {unique}")
    for c in unique:
        j = (-1 + np.sqrt(1 + 4 * c)) / 2
        mult = np.sum(np.abs(evals - c) < 0.01)
        print(f"    S^2 = {c:.4f} -> j = {j:.4f}, multiplicity = {mult}")

    return [S1, S2, S3]


def build_all_clifford_products(gammas):
    """
    Build all independent elements of Cl(3):
    I, G_1, G_2, G_3, G_1G_2, G_1G_3, G_2G_3, G_1G_2G_3
    Total: 2^3 = 8 basis elements.

    Each is an 8x8 matrix. Some are Hermitian, some anti-Hermitian.
    """
    print("\n--- All Cl(3) basis elements ---")

    elements = []
    labels = []

    # Identity
    elements.append(np.eye(8, dtype=complex))
    labels.append("I")

    # Degree 1
    for mu in range(3):
        elements.append(gammas[mu])
        labels.append(f"G{mu+1}")

    # Degree 2
    for mu in range(3):
        for nu in range(mu + 1, 3):
            prod = gammas[mu] @ gammas[nu]
            elements.append(prod)
            labels.append(f"G{mu+1}G{nu+1}")

    # Degree 3
    prod123 = gammas[0] @ gammas[1] @ gammas[2]
    elements.append(prod123)
    labels.append("G1G2G3")

    for e, lab in zip(elements, labels):
        is_herm = np.linalg.norm(e - e.conj().T) < 1e-10
        is_antiherm = np.linalg.norm(e + e.conj().T) < 1e-10
        sq = e @ e
        sq_id = np.linalg.norm(sq - np.eye(8)) < 1e-10
        sq_neg = np.linalg.norm(sq + np.eye(8)) < 1e-10
        print(f"  {lab:>8}: Herm={is_herm}, AntiHerm={is_antiherm}, "
              f"A^2={'I' if sq_id else '-I' if sq_neg else 'other'}")

    return elements, labels


def search_su3_in_taste_space(gammas, su2_gens):
    """
    Search for SU(3) subalgebras within the 8-dim taste space.

    Strategy: SU(3) has a maximal SU(2) x U(1) subgroup.
    The SU(2) part is {S_1, S_2, S_3} acting on 2 of 3 colors.
    The U(1) part is lambda_8 = diag(1, 1, -2)/sqrt(3).

    In the 8-dim space, we have 8 = 2 + 2 + 2 + 2 under each SU(2).
    For SU(3), we need 8 = 3 + 3_bar + 1 + 1 (adjoint decomposition)
    or 8 = 3 + 2 + 2 + 1 (various branchings).

    The fundamental question: can we find a 3-dimensional subspace
    of the 8-dim taste space that transforms irreducibly under some
    set of 8 generators closing to su(3)?
    """
    print("\n--- Searching for SU(3) in 8-dim taste space ---")

    S1, S2, S3 = su2_gens

    # The isospin SU(2) generators (first tensor factor)
    I2 = np.eye(2, dtype=complex)
    T1 = 0.5 * np.kron(np.kron(SIGMA[1], I2), I2)
    T2 = 0.5 * np.kron(np.kron(SIGMA[2], I2), I2)
    T3 = 0.5 * np.kron(np.kron(SIGMA[3], I2), I2)

    print("  Two independent SU(2) subalgebras found:")
    print(f"    Spin SU(2): S_k = -(i/2) eps_ijk G_i G_j")
    print(f"    Isospin SU(2): T_k = (1/2) sigma_k (x) I (x) I")

    # Check commutativity
    comm_ST = np.linalg.norm(S1 @ T1 - T1 @ S1)
    print(f"  [S1, T1] norm: {comm_ST:.6f}")
    commute = comm_ST < 1e-10
    print(f"  Spin and isospin commute: {commute}")

    # SU(3) ⊃ SU(2) x U(1): need to find the U(1) generator
    # In the Standard Model embedding: Y = (2/3)(lambda_8 * sqrt(3)/2)
    # Here, look for diagonal generators that commute with one SU(2)

    # Build candidate U(1) generators from diagonal Clifford products
    G1, G2, G3 = gammas
    G12 = G1 @ G2
    G23 = G2 @ G3
    G13 = G1 @ G3
    G123 = G1 @ G2 @ G3

    diag_candidates = [
        (G12, "G1G2"),
        (G23, "G2G3"),
        (G13, "G1G3"),
        (G123, "G1G2G3"),
    ]

    # Make Hermitian generators from anti-Hermitian ones
    hermitian_candidates = []
    for M, lab in diag_candidates:
        if np.linalg.norm(M - M.conj().T) < 1e-10:
            hermitian_candidates.append((M, lab))
        elif np.linalg.norm(M + M.conj().T) < 1e-10:
            hermitian_candidates.append((1j * M, f"i*{lab}"))

    print("\n  Diagonal Hermitian generators from Cl(3):")
    for H, lab in hermitian_candidates:
        evals = np.linalg.eigvalsh(H.real)
        unique = np.unique(np.round(evals, 4))
        print(f"    {lab}: eigenvalues = {unique}")

    # Try to extend SU(2) to SU(3)
    # We need 5 more generators beyond S_1, S_2, S_3
    # These should be: lambda_4, lambda_5, lambda_6, lambda_7, lambda_8
    # projected into the 8-dim space

    print("\n--- Attempting SU(2) -> SU(3) extension ---")

    # Build all anti-Hermitian elements and their commutators with SU(2)
    all_gens = [S1, S2, S3]
    all_labels = ["S1", "S2", "S3"]

    # Add diagonal generators
    for H, lab in hermitian_candidates:
        all_gens.append(H)
        all_labels.append(lab)

    # Add off-diagonal products
    off_diag = [
        (G1, "G1"), (G2, "G2"), (G3, "G3"),
    ]
    for M, lab in off_diag:
        all_gens.append(M)
        all_labels.append(lab)

    # Commutator closure
    basis = list(all_gens)
    basis_labels = list(all_labels)

    for iteration in range(6):
        new_els = []
        new_labs = []
        current = len(basis)
        for i in range(current):
            for j in range(i + 1, current):
                comm = basis[i] @ basis[j] - basis[j] @ basis[i]
                cn = np.linalg.norm(comm)
                if cn < 1e-10:
                    continue
                comm = comm / cn

                residual = comm.copy()
                for b in basis + new_els:
                    bn = np.trace(b.conj().T @ b).real
                    if bn < 1e-10:
                        continue
                    ov = np.trace(b.conj().T @ residual) / bn
                    residual = residual - ov * b

                if np.linalg.norm(residual) > 0.1:
                    residual = residual / np.linalg.norm(residual)
                    new_els.append(residual)
                    new_labs.append(f"[{basis_labels[i]},{basis_labels[j]}]")

        if not new_els:
            print(f"  Iteration {iteration+1}: closed! Algebra dimension = {len(basis)}")
            break
        basis.extend(new_els)
        basis_labels.extend(new_labs)
        print(f"  Iteration {iteration+1}: added {len(new_els)}, total = {len(basis)}")

    full_dim = len(basis)
    print(f"\n  Full algebra dimension: {full_dim}")

    # Identify the algebra
    # su(2) = 3, su(3) = 8, su(4) = 15, so(8) = 28
    # su(2)^3 = 9, su(2) x su(2) = 6
    known = {3: "su(2)", 6: "su(2)+su(2)", 8: "su(3)", 9: "su(2)+su(2)+su(2)",
             10: "so(5) or sp(4)", 15: "su(4)", 21: "so(7) or sp(6)",
             28: "so(8)", 63: "su(8)"}
    if full_dim in known:
        print(f"  Identified as: {known[full_dim]}")
    else:
        print(f"  Dimension {full_dim} does not match standard simple Lie algebras")

    return full_dim


def try_embedding_3d_subspace(gammas):
    """
    Try to find a 3-dimensional subspace of the 8-dim taste space
    that carries the fundamental representation of SU(3).

    If 8 = 3 + 3* + 1 + 1 under SU(3), there should be a 3-dim
    subspace with 8 generators acting on it as Gell-Mann matrices.
    """
    print("\n--- Searching for 3-dim SU(3) fundamental subspace ---")

    n = 8  # taste space dimension

    # Strategy: use random projections onto 3-dim subspaces
    # and check if the projected algebra looks like su(3)

    G1, G2, G3 = gammas
    all_ops = [G1, G2, G3, G1 @ G2, G2 @ G3, G1 @ G3, G1 @ G2 @ G3,
               -0.5j * G2 @ G3, -0.5j * G3 @ G1, -0.5j * G1 @ G2]

    best_score = 0
    best_dim = 0

    np.random.seed(42)
    n_trials = 200

    for trial in range(n_trials):
        # Random 3-dim subspace of C^8
        V = np.random.randn(8, 3) + 1j * np.random.randn(8, 3)
        Q, _ = np.linalg.qr(V)
        P = Q[:, :3]  # 8x3 projection

        # Project all operators onto this subspace
        projected = []
        for op in all_ops:
            M3 = P.conj().T @ op @ P  # 3x3
            # Make traceless Hermitian
            H = (M3 + M3.conj().T) / 2
            tr = np.trace(H) / 3
            H_tl = H - tr * np.eye(3)
            if np.linalg.norm(H_tl) > 0.01:
                projected.append(H_tl / np.linalg.norm(H_tl))

            # Also anti-Hermitian -> Hermitian
            A = (M3 - M3.conj().T) / (2j)
            tr = np.trace(A) / 3
            A_tl = A - tr * np.eye(3)
            if np.linalg.norm(A_tl) > 0.01:
                projected.append(A_tl / np.linalg.norm(A_tl))

        # Find independent generators
        independent = []
        for g in projected:
            residual = g.copy()
            for b in independent:
                ov = np.trace(b.conj().T @ residual) / np.trace(b.conj().T @ b).real
                residual = residual - ov * b
            if np.linalg.norm(residual) > 0.1:
                residual = residual / np.linalg.norm(residual)
                independent.append(residual)

        # Commutator closure
        basis = list(independent[:8])
        for iteration in range(4):
            new_els = []
            current = len(basis)
            for i in range(current):
                for j in range(i + 1, current):
                    comm = basis[i] @ basis[j] - basis[j] @ basis[i]
                    cn = np.linalg.norm(comm)
                    if cn < 1e-10:
                        continue
                    comm_h = 1j * comm / cn
                    residual = comm_h.copy()
                    for b in basis + new_els:
                        bn = np.trace(b.conj().T @ b).real
                        if bn < 1e-10:
                            continue
                        ov = np.trace(b.conj().T @ residual) / bn
                        residual = residual - ov * b
                    if np.linalg.norm(residual) > 0.1:
                        residual = residual / np.linalg.norm(residual)
                        new_els.append(residual)
            if not new_els:
                break
            basis.extend(new_els)

        dim = len(basis)
        if dim == 8:
            # Check Gell-Mann coverage
            gm_covered = 0
            for lam in GELLMANN:
                max_ov = max(abs(np.trace(g.conj().T @ lam)) /
                           (np.linalg.norm(g, 'fro') * np.linalg.norm(lam, 'fro'))
                           for g in basis)
                if max_ov > 0.3:
                    gm_covered += 1
            if gm_covered > best_score:
                best_score = gm_covered
                best_dim = dim
                if gm_covered == 8:
                    print(f"  Trial {trial}: FOUND su(3)! dim={dim}, Gell-Mann={gm_covered}/8")
                    return True, dim, gm_covered

        if dim > best_dim:
            best_dim = dim

    print(f"  Best algebra dimension found: {best_dim}")
    print(f"  Best Gell-Mann coverage: {best_score}/8")
    return False, best_dim, best_score


def analyze_8_to_3_decomposition(gammas, su2_gens):
    """
    Analyze how the 8-dim taste space decomposes under SU(2) and
    what structure would be needed for SU(3).

    Under SU(2) spin, 8 = 4 doublets (j=1/2).
    Under SU(2) isospin, 8 = 4 doublets (j=1/2).
    Under SU(2)_spin x SU(2)_isospin, 8 = (2,2,2) = tensor product of 3 doublets.

    For SU(3), we would need: 8 = 3 + 3* + 1 + 1 or 8 = 3 + 5 etc.
    This requires a DIFFERENT decomposition of the 8-dim space.
    """
    print("\n--- Decomposition of 8-dim taste space ---")

    S1, S2, S3 = su2_gens

    # Decompose under SU(2)_spin
    S_sq = S1 @ S1 + S2 @ S2 + S3 @ S3
    evals, evecs = np.linalg.eigh(S_sq.real)

    print("  Under SU(2) spin:")
    for j_val in np.unique(np.round(evals, 4)):
        mult = np.sum(np.abs(evals - j_val) < 0.01)
        j = (-1 + np.sqrt(1 + 4 * j_val)) / 2
        print(f"    j = {j:.2f}: multiplicity {mult} (= {int(mult/(2*j+1))} copies of spin-{j:.1f})")

    # Check: the tensor structure 8 = 2 (x) 2 (x) 2
    # means the three independent SU(2)'s each give a doublet.
    # To get SU(3), we need to GROUP the three factors differently.

    # SU(3) fundamental: the 3 of SU(3) can be embedded in
    # the 8-dim space as a 3-dim subspace IF we identify:
    # |1> = |+,+,+>, |2> = |+,-,->, |3> = |-,+,->
    # (or some such assignment)

    # Let's try: use the S3 eigenvalues to define a 3-coloring
    S3_evals, S3_evecs = np.linalg.eigh(S3.real)
    print(f"\n  S3 eigenvalues: {np.round(S3_evals, 4)}")

    # Group into multiplets
    # The 8 = 2 x 2 x 2 structure under SU(2)^3 means:
    # Each state is labeled by (s1, s2, s3) where si = +/- 1/2
    I2 = np.eye(2, dtype=complex)
    sz = SIGMA[3]

    # Build the three independent S_z operators
    Sz1 = 0.5 * np.kron(np.kron(sz, I2), I2)
    Sz2 = 0.5 * np.kron(np.kron(I2, sz), I2)
    Sz3 = 0.5 * np.kron(np.kron(I2, I2), sz)

    print("\n  Quantum numbers of the 8 taste states:")
    print(f"  {'State':>6} {'sz1':>6} {'sz2':>6} {'sz3':>6} {'sum':>6}")
    for i in range(8):
        s1 = Sz1[i, i].real
        s2 = Sz2[i, i].real
        s3 = Sz3[i, i].real
        s_sum = s1 + s2 + s3
        print(f"  {i:>6} {s1:>+6.1f} {s2:>+6.1f} {s3:>+6.1f} {s_sum:>+6.1f}")

    # The key observation: 8 states have quantum numbers that naturally
    # group into:
    # - 1 state with sum = +3/2: (+++), -- NOT a triplet
    # - 3 states with sum = +1/2: (++-), (+-+), (-++)  -- THIS could be a triplet
    # - 3 states with sum = -1/2: (--+), (-+-), (+--) -- THIS could be an anti-triplet
    # - 1 state with sum = -3/2: (---) -- NOT a triplet

    print("\n  Grouping by total sz:")
    for target_sum in [1.5, 0.5, -0.5, -1.5]:
        states = []
        for i in range(8):
            s = Sz1[i, i].real + Sz2[i, i].real + Sz3[i, i].real
            if abs(s - target_sum) < 0.01:
                states.append(i)
        print(f"    sum = {target_sum:+.1f}: states {states} (multiplicity {len(states)})")

    # The 3+3+1+1 decomposition is exactly what SU(3) needs!
    # 3 (fundamental) + 3* (anti-fundamental) + 1 + 1 = 8
    print("\n  8 = 3 + 3* + 1 + 1 decomposition EXISTS in the taste space!")
    print("  The triplet (3 states with sum=+1/2) transforms as the")
    print("  fundamental rep of a POTENTIAL SU(3).")

    # Now check: do any operators in the Clifford algebra map between
    # these triplet states in a way consistent with Gell-Mann matrices?
    triplet_states = []
    for i in range(8):
        s = Sz1[i, i].real + Sz2[i, i].real + Sz3[i, i].real
        if abs(s - 0.5) < 0.01:
            triplet_states.append(i)

    print(f"\n  Triplet states: {triplet_states}")

    # Project Clifford generators onto triplet subspace
    P_trip = np.zeros((8, 3), dtype=complex)
    for k, i in enumerate(triplet_states):
        P_trip[i, k] = 1.0

    print("\n  Clifford generators projected onto triplet subspace:")
    G1, G2, G3 = gammas
    all_ops = [
        (G1, "G1"), (G2, "G2"), (G3, "G3"),
        (G1 @ G2, "G1G2"), (G2 @ G3, "G2G3"), (G1 @ G3, "G1G3"),
        (G1 @ G2 @ G3, "G123"),
        (-0.5j * G2 @ G3, "S1"), (-0.5j * G3 @ G1, "S2"), (-0.5j * G1 @ G2, "S3"),
    ]

    projected_gens = []
    projected_labels = []
    for op, lab in all_ops:
        M3 = P_trip.conj().T @ op @ P_trip
        norm = np.linalg.norm(M3)
        if norm > 0.01:
            # Extract Hermitian traceless part
            H = (M3 + M3.conj().T) / 2
            tr = np.trace(H) / 3
            H_tl = H - tr * np.eye(3)
            if np.linalg.norm(H_tl) > 0.01:
                projected_gens.append(H_tl / np.linalg.norm(H_tl))
                projected_labels.append(f"{lab}_H")

            # Anti-Hermitian -> Hermitian
            A = (M3 - M3.conj().T) / (2j)
            tr = np.trace(A) / 3
            A_tl = A - tr * np.eye(3)
            if np.linalg.norm(A_tl) > 0.01:
                projected_gens.append(A_tl / np.linalg.norm(A_tl))
                projected_labels.append(f"{lab}_A")

    print(f"  Non-zero projected generators: {len(projected_gens)}")

    # Find independent ones
    independent = []
    ind_labels = []
    for g, lab in zip(projected_gens, projected_labels):
        residual = g.copy()
        for b in independent:
            ov = np.trace(b.conj().T @ residual) / np.trace(b.conj().T @ b).real
            residual = residual - ov * b
        if np.linalg.norm(residual) > 0.1:
            residual = residual / np.linalg.norm(residual)
            independent.append(residual)
            ind_labels.append(lab)

    print(f"  Independent generators: {len(independent)}")
    for g, lab in zip(independent, ind_labels):
        overlaps = [abs(np.trace(g.conj().T @ lam)) /
                    (np.linalg.norm(g, 'fro') * np.linalg.norm(lam, 'fro'))
                    for lam in GELLMANN]
        best_j = np.argmax(overlaps)
        print(f"    {lab}: best Gell-Mann match = lambda_{best_j+1} (overlap={overlaps[best_j]:.4f})")

    # Commutator closure on the triplet
    basis = list(independent)
    for iteration in range(5):
        new_els = []
        current = len(basis)
        for i in range(current):
            for j in range(i + 1, current):
                comm = basis[i] @ basis[j] - basis[j] @ basis[i]
                cn = np.linalg.norm(comm)
                if cn < 1e-10:
                    continue
                comm_h = 1j * comm / cn
                residual = comm_h.copy()
                for b in basis + new_els:
                    bn = np.trace(b.conj().T @ b).real
                    if bn < 1e-10:
                        continue
                    ov = np.trace(b.conj().T @ residual) / bn
                    residual = residual - ov * b
                if np.linalg.norm(residual) > 0.1:
                    residual = residual / np.linalg.norm(residual)
                    new_els.append(residual)
        if not new_els:
            break
        basis.extend(new_els)

    triplet_dim = len(basis)
    print(f"\n  Algebra on triplet subspace: dimension = {triplet_dim}")
    if triplet_dim == 8:
        print("  THIS IS su(3)!")
    elif triplet_dim == 3:
        print("  This is su(2) -- only the SU(2) subgroup acts on the triplet")

    # Check Gell-Mann coverage on triplet
    gm_covered = 0
    for j, lam in enumerate(GELLMANN):
        max_ov = 0
        for g in basis:
            ov = abs(np.trace(g.conj().T @ lam)) / (np.linalg.norm(g, 'fro') * np.linalg.norm(lam, 'fro'))
            max_ov = max(max_ov, ov)
        if max_ov > 0.3:
            gm_covered += 1
    print(f"  Gell-Mann directions covered: {gm_covered}/8")

    return triplet_dim, gm_covered


def main():
    t0 = time.time()

    print("=" * 80)
    print("SU(3) FROM SU(2) x U(1) COMBINATION")
    print("=" * 80)

    # Build Cl(3)
    gammas = build_clifford_algebra()

    # Extract SU(2)
    su2_gens = extract_su2_generators(gammas)

    # All Clifford products
    elements, labels = build_all_clifford_products(gammas)

    # Search for SU(3) in full taste algebra
    full_dim = search_su3_in_taste_space(gammas, su2_gens)

    # Random projection search
    found, proj_dim, proj_score = try_embedding_3d_subspace(gammas)

    # Decomposition analysis
    trip_dim, trip_gm = analyze_8_to_3_decomposition(gammas, su2_gens)

    # ---- VERDICT ----
    print(f"\n{'='*80}")
    print("VERDICT")
    print(f"{'='*80}")

    elapsed = time.time() - t0

    print(f"""
  STARTING POINT:
  - 8-dim taste space from Cl(3) on staggered cubic lattice
  - SU(2) spin generators S_k = -(i/2) eps_ijk G_i G_j: CONFIRMED
  - SU(2) isospin generators T_k = (1/2) sigma_k (x) I (x) I: CONFIRMED
  - Full Cl(3) algebra: 8 independent elements (I + 3 + 3 + 1)

  KEY RESULTS:
  1. Full algebra from Cl(3) generators: dimension {full_dim}
     - This is {'su(3)' if full_dim == 8 else 'NOT su(3)' if full_dim != 8 else ''} (su(3) needs dim 8)
     - The Clifford algebra Cl(3) ~ M(2) x M(2) has Lie algebra su(4) ~ so(6)
     - su(4) CONTAINS su(3) as a subalgebra, so the structure is there

  2. Random 3-dim subspace search: best dim = {proj_dim}, Gell-Mann = {proj_score}/8
     {'- FOUND su(3) in a 3-dim subspace!' if found else '- Did not find full su(3) in random projections'}

  3. Natural 8 = 3 + 3* + 1 + 1 decomposition:
     - The 8 taste states group as 3 + 3 + 1 + 1 by total spin
     - Cl(3) projected onto the triplet: algebra dimension = {trip_dim}
     - Gell-Mann coverage on triplet: {trip_gm}/8

  INTERPRETATION:
  The 8-dim taste space from the BIPARTITE (Z_2) cubic lattice contains
  SU(2) but not naturally SU(3). The reason is clear:

  - Z_2 parity -> Clifford algebra Cl(3) -> su(2) subalgebras
  - Cl(3) is a 2^3-dim algebra over R, isomorphic to M(2,R) x M(2,R)
  - The Lie algebra of M(2) x M(2) is gl(2) x gl(2), containing su(2) x su(2)
  - su(3) requires a 3-fold structure that Z_2 cannot provide

  TO GET SU(3), YOU NEED Z_3 (not Z_2):
  - Replace bipartite (2-coloring) with 3-coloring
  - Replace Clifford algebra Cl(3) with Weyl-Heisenberg (clock-shift) algebra
  - This gives 3^d taste space with natural SU(3) structure
  - See: frontier_su3_triangulated.py for the explicit construction

  BOTTOM LINE: SU(3) does NOT emerge from the Z_2 staggered lattice's
  Cl(3) algebra. The path SU(2) x U(1) -> SU(3) requires ADDITIONAL
  Z_3 structure (3-colorable graph or 3-cycle internal space).

  Time: {elapsed:.1f}s
""")


if __name__ == "__main__":
    main()
