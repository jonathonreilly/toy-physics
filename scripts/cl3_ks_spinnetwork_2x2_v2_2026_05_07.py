"""
Cl(3) -> KS, 2x2 spatial torus, spin-network ED v2.

KEY UPGRADE OVER v1: explicit linked / 'shared-vertex' invariants.

The character-product basis chi_lambda(W_1) chi_mu(W_2) only spans the
TRIVIAL intertwiner sector at shared vertices/edges. The key missing
states are 'linked' invariants where 4 indices are contracted via
non-trivial intertwiners (adjoint, etc.) at vertices.

For SU(3), at a vertex with 4 incident fund-rep edges, the invariant
space includes:
  I_a = Tr(U_1 U_2) Tr(U_3 U_4)    [from 3⊗3->6+3* trivial assignment]
  I_b = Tr(U_1 U_3) Tr(U_2 U_4)    [different pairing]
  I_c = Tr(U_1 U_4) Tr(U_2 U_3)    [yet another pairing]
plus determinant-like invariants from epsilon contractions.

For our 2x2 torus problem, we add 'matrix-element' invariants like:
  T_e^{ab}(W_1, W_2) = (W_1)^a_b (W_2^*)^c_d delta_ad delta_bc
                     = Tr(W_1^T (W_2^*)^T) [different from Tr(W_1) Tr(W_2)]

These pick up the (1,1)-adjoint component of overlapping (1,0)-fund
loops at shared edges.

We use NUMERICAL Casimir (finite-difference Lie derivatives, validated
in v1) and add a richer basis of gauge-invariant Wilson-loop products
including these linked invariants.
"""

from __future__ import annotations

import time
import numpy as np
from numpy.linalg import eigh
from scipy.linalg import expm

from cl3_ks_single_plaquette_2026_05_07 import casimir
from cl3_ks_two_plaquette_2026_05_07 import sample_su3, chi_pq
from cl3_ks_spinnetwork_2x2_2026_05_07 import (
    LINK_KEYS, gell_mann_generators, perturbed_links,
    diagonalize_with_gram,
)


# -------------------------------------------------------------------
# Loop holonomies (full matrix, not just trace)
# -------------------------------------------------------------------

def matprod(*Us):
    out = Us[0]
    for U in Us[1:]:
        out = np.einsum('nij,njk->nik', out, U)
    return out


def matinv(U):
    return np.conj(U.transpose(0, 2, 1))


def re_trace_over_Nc(M, N_c=3):
    return np.trace(M, axis1=1, axis2=2).real / N_c


def loop_matrices(samples):
    """Compute Wilson-loop holonomy matrices (not just characters)."""
    holos = {}

    # 4 plaquettes
    for i in [0, 1]:
        for j in [0, 1]:
            ip = (i + 1) % 2
            jp = (j + 1) % 2
            U1 = samples[f'x_{i}{j}']
            U2 = samples[f'y_{ip}{j}']
            U3_inv = matinv(samples[f'x_{i}{jp}'])
            U4_inv = matinv(samples[f'y_{i}{j}'])
            holos[f'P{i}{j}'] = matprod(U1, U2, U3_inv, U4_inv)

    # 4 non-contractible loops
    for j in [0, 1]:
        holos[f'X{j}'] = matprod(samples[f'x_0{j}'], samples[f'x_1{j}'])
    for i in [0, 1]:
        holos[f'Y{i}'] = matprod(samples[f'y_{i}0'], samples[f'y_{i}1'])

    return holos


# -------------------------------------------------------------------
# Construct rich gauge-invariant basis
# -------------------------------------------------------------------

# SU(3) Cayley-Hamilton: U^3 = (Tr U) U^2 - (1/2)((Tr U)^2 - Tr U^2) U + det(U) I
# For SU(3), det(U) = 1, so any matrix product can be reduced.

# Single-rep characters:
#   (0,0): 1
#   (1,0): Tr W
#   (0,1): Tr W^*
#   (1,1): |Tr W|^2 - 1
#   (2,0): (Tr W)^2/2 + Tr W^2 / 2
#   (0,2): conjugate of (2,0)

# Full Wilson loop matrix W gives also matrix elements W^a_b.
# Linked invariants: contractions of two W matrices at a shared edge:
#   For loops W_1, W_2 sharing exactly edge e, with U_e in W_1 and
#   U_e^{-1} in W_2 (or vice versa), define:
#     L(W_1, W_2) = Tr(W_1) Tr(W_2)         [character product, included]
#     L_adj(W_1, W_2) = Tr(W_1 W_2)         [linked via shared edge:
#                                            this 'cancels' U_e U_e^{-1}=I
#                                            and gives a longer loop!]
# Hmm — actually if W_1 contains U_e and W_2 contains U_e^{-1},
# then concatenating gives U_e U_e^{-1} = I, leaving a single longer loop.
# This is just another Wilson loop, ALREADY in our basis if we add
# longer loops!

# Truly linked (non-reducible) invariants need shared edges with the
# SAME orientation (both U_e), giving Tr(U_e A U_e B) with arbitrary
# A, B. Such 'theta-graph' contractions are NOT just longer Wilson loops.

# Theta graphs:
#   Two paths from vertex v_1 to vertex v_2 (forward direction),
#   contracted at both endpoints via delta:
#     T(P_1, P_2) = (P_1)^a_b (P_2^*)^a_b = Tr(P_1 P_2^dag)
#   This is the 'connected' part of <Tr P_1 Tr P_2*>.

def build_basis_v2(samples, irrep_set,
                    include_pairs=True,
                    include_theta_graphs=True,
                    include_higher_loops=True):
    """
    Build basis with character products PLUS theta-graph (linked) invariants.

    Theta graph invariant: Tr(U_1 U_2^dag) where U_1, U_2 are matrix
    products along two paths from same start to same end vertex.

    Returns: F (n_basis, N), labels.
    """
    holos = loop_matrices(samples)
    N = next(iter(holos.values())).shape[0]
    F_list = [np.ones(N, dtype=complex)]
    labels = [{'kind': 'trivial'}]

    plaq_ids = ['P00', 'P10', 'P01', 'P11']
    nc_ids = ['X0', 'X1', 'Y0', 'Y1']
    all_ids = plaq_ids + nc_ids

    # Singles: chi_lambda(W) for each loop and irrep
    nontriv_irreps = [lam for lam in irrep_set if lam != (0, 0)]
    for W in all_ids:
        for lam in nontriv_irreps:
            F_list.append(chi_pq(holos[W], *lam))
            labels.append({'kind': 'single', 'loop': W, 'irrep': lam})

    # Higher-length loops: products of overlapping plaquettes that simplify
    # to longer Wilson loops via U_e U_e^{-1} cancellation.
    # E.g., P_00 P_10 share edge y_10: P_00 has U_y10 going up, P_10 has
    # U_y10 going DOWN (i.e., U_y10^{-1}). Product = traversal of the 1x2
    # rectangle. This is a length-6 loop.
    if include_higher_loops:
        # P_00 traversed concatenated with P_10 (sharing edge y_10):
        # Original P_00 = U_x00 U_y10 U_x01^{-1} U_y00^{-1}
        # Original P_10 = U_x10 U_y00 U_x11^{-1} U_y10^{-1}  (uses y_00 going up)
        # Wait, P_10 from vertex (1,0): U_x(1,0) U_y(0,0=site 2,0 % 2=0,0) ...
        # Let me reuse the existing geometry:
        # P_ij = U_x(i,j) U_y(i+1,j) U_x(i,j+1)^-1 U_y(i,j)^-1
        # P_00 = U_x_00 U_y_10 U_x_01^-1 U_y_00^-1
        # P_10 = U_x_10 U_y_00 U_x_11^-1 U_y_10^-1
        # Shared edge: y_10 (in P_00 forward, in P_10 inverse).
        # Concatenation: P_00 then P_10:
        # U_x_00 U_y_10 U_x_01^-1 U_y_00^-1 U_x_10 U_y_00 U_x_11^-1 U_y_10^-1
        # Length-8 closed loop.
        # However, U_y_00^-1 followed by U_y_00 has y_00 cancellation only
        # if matrix-multiplied; but they're at different positions in the
        # product so they don't cancel. So this is genuinely a length-8 loop.
        L_2x1 = matprod(
            samples['x_00'], samples['y_10'], matinv(samples['x_01']),
            matinv(samples['y_00']), samples['x_10'], samples['y_00'],
            matinv(samples['x_11']), matinv(samples['y_10']),
        )
        # Hmm this doesn't simplify to a 1x2 rectangle directly.
        # Let me just add it as a generic length-8 loop.
        holos['L8a'] = L_2x1
        for lam in [(0, 0)] + nontriv_irreps:
            if lam == (0, 0):
                continue
            F_list.append(chi_pq(L_2x1, *lam))
            labels.append({'kind': 'long', 'loop': 'L8a', 'irrep': lam})

        # 1x2 rectangle: traverse along x for 2 units, up by 1, back, down
        # = U_x(0,0) U_x(1,0) U_y(0,0) U_x(0,1)^-1 U_x(1,1)^-1 U_y(0,0)^-1
        # No this is wrong. Let me just construct by tracing edges.
        # 1x2 rectangle starting at (0,0), going +x, +x, +y, -x, -x, -y:
        # That's: x_00, x_10, y_00 (going from (0,0) to (0,1)),
        # then -x_01 (going from (1,1) back to (0,1)),
        # then -x_11 actually we need to be careful about indexing.
        # Let's rename: x_ij = link from (i,j) to (i+1,j). So x_00 from (0,0) to (1,0).
        # Then going (0,0) -x-> (1,0) -x-> (2,0)=(0,0) PBC! So 2 x-steps wraps around.
        # Hmm in our 2x2 PBC, 2 steps of x is X_j (non-contractible).
        # So 1x2 rectangle = X_0 + going up + X_0^-1 + going down.
        # With PBC, this might just be the trivial loop or a torus boundary.
        # Skip and just keep the L8a above.

    # Theta-graph linked invariants: Tr(W_1 W_2^dag) where W_1, W_2 share
    # both endpoints. For 2x2 torus, the most natural ones are formed from
    # adjacent plaquettes.
    # E.g., from vertex (0,0) to vertex (1,1), there are 2 paths:
    #   path1 = U_x_00 U_y_10 (right then up)
    #   path2 = U_y_00 U_x_01 (up then right)
    # Theta graph: Tr(path1 path2^dag) = Tr(U_x_00 U_y_10 U_x_01^-1 U_y_00^-1)
    # Wait — that's just P_00! Trace of plaquette.
    # So this 'theta graph' from (0,0) to (1,1) is simply chi_(1,0)(P_00).
    # Already in basis.

    # Hmm, for theta graphs to be NEW invariants, the two paths need to be
    # genuinely different and not just a closed loop. The simplest 'theta'
    # invariant is in higher reps:
    # Theta_{1,1}(P_00, P_10) = Tr(P_00) Tr(P_10) - (1/N_c) Tr(P_00 P_10)
    # = (1,1)-adjoint component of P_00 \otimes P_10.
    # The MISSING invariant in the character-product basis is:
    #   Tr(P_00 P_10) [matrix-product trace, NOT product of traces]
    # This is a different gauge invariant!
    if include_theta_graphs:
        # Pairwise matrix-product traces: Tr(W_1 W_2) and Tr(W_1 W_2^dag)
        # for distinct loops. These are DIFFERENT from Tr(W_1) Tr(W_2)
        # unless W_1 W_2 reduces to a known loop.

        # Note: Tr(P_00 P_10) is a length-8 'figure-eight' loop traversal
        # if P_00, P_10 share edges. Even when they don't, it's an
        # 8-link connected closed walk (or two disjoint loops mapped
        # together), giving a NEW invariant beyond character products.

        for ia, W1 in enumerate(all_ids):
            for ib, W2 in enumerate(all_ids):
                if ib <= ia:
                    continue
                # Tr(W_1 W_2)
                T12 = np.trace(np.einsum('nij,njk->nik', holos[W1], holos[W2]),
                                 axis1=1, axis2=2)
                F_list.append(T12)
                labels.append({'kind': 'theta', 'loops': [W1, W2],
                                 'op': 'Tr(W1 W2)'})
                # Tr(W_1 W_2^dag)
                T12dag = np.trace(np.einsum('nij,njk->nik', holos[W1],
                                              matinv(holos[W2])),
                                    axis1=1, axis2=2)
                F_list.append(T12dag)
                labels.append({'kind': 'theta', 'loops': [W1, W2],
                                 'op': 'Tr(W1 W2dag)'})

    # Pair products of singles (kept from v1)
    if include_pairs:
        low_irreps = [lam for lam in irrep_set
                       if lam in [(1, 0), (0, 1), (1, 1)]]
        for ia, W1 in enumerate(all_ids):
            for ib, W2 in enumerate(all_ids):
                if ib <= ia:
                    continue
                for lam1 in low_irreps:
                    for lam2 in low_irreps:
                        F_list.append(
                            chi_pq(holos[W1], *lam1) * chi_pq(holos[W2], *lam2)
                        )
                        labels.append({'kind': 'pair',
                                         'loops': [(W1, lam1), (W2, lam2)]})

    F = np.array(F_list)
    return F, labels, holos


# -------------------------------------------------------------------
# Build Hamiltonian (using v1 numerical Casimir machinery)
# -------------------------------------------------------------------

def build_H_and_Gram(g_squared, samples, irrep_set,
                      include_pairs, include_theta_graphs,
                      include_higher_loops, eps=1e-2,
                      verbose=True, N_c=3):
    F, labels, holos = build_basis_v2(
        samples, irrep_set,
        include_pairs=include_pairs,
        include_theta_graphs=include_theta_graphs,
        include_higher_loops=include_higher_loops,
    )
    n_basis, N = F.shape
    if verbose:
        print(f"  Basis size: {n_basis}, samples: {N}")

    # Gram
    Gram = (np.conj(F) @ F.T) / N

    # Magnetic
    plaqs = [holos[f'P{i}{j}'] for i in [0, 1] for j in [0, 1]]
    M_values = -(1.0 / g_squared) * sum(re_trace_over_Nc(p, N_c) for p in plaqs)
    H_mag = (np.conj(F) * M_values[np.newaxis, :]) @ F.T / N

    # Casimir on each link (numerical via finite-difference Lie derivative)
    T_list = gell_mann_generators()
    H_C = np.zeros((n_basis, n_basis), dtype=complex)
    for k, link_key in enumerate(LINK_KEYS):
        if verbose:
            t0 = time.time()
        Chat_F = np.zeros((n_basis, N), dtype=complex)
        for T_a in T_list:
            samples_plus = perturbed_links(samples, link_key, T_a, eps, +1)
            samples_minus = perturbed_links(samples, link_key, T_a, eps, -1)
            F_plus, _, _ = build_basis_v2(
                samples_plus, irrep_set,
                include_pairs=include_pairs,
                include_theta_graphs=include_theta_graphs,
                include_higher_loops=include_higher_loops,
            )
            F_minus, _, _ = build_basis_v2(
                samples_minus, irrep_set,
                include_pairs=include_pairs,
                include_theta_graphs=include_theta_graphs,
                include_higher_loops=include_higher_loops,
            )
            Chat_F -= (F_plus + F_minus - 2.0 * F) / (eps ** 2)
        contrib = (np.conj(F) @ Chat_F.T) / N
        H_C += contrib
        if verbose:
            dt = time.time() - t0
            print(f"    link {link_key}: Casimir computed ({dt:.1f}s)")
    H_C *= (g_squared / 2.0)

    H = H_C + H_mag
    H = 0.5 * (H + np.conj(H.T))
    Gram = 0.5 * (Gram + np.conj(Gram.T))

    return H, Gram, F, labels, holos


def expectation_P(psi, F, holos, N_c=3):
    plaqs = [holos[f'P{i}{j}'] for i in [0, 1] for j in [0, 1]]
    P_vals = sum(re_trace_over_Nc(p) for p in plaqs) / 4.0
    psi_at = np.conj(psi) @ F
    norm = np.mean(np.abs(psi_at) ** 2)
    return float(np.mean(np.abs(psi_at) ** 2 * P_vals) / norm)


def run_one(g_squared, irrep_set, N_samples=4000, seed=11,
             include_pairs=True, include_theta_graphs=True,
             include_higher_loops=True, eps=1e-2,
             verbose=True):
    if verbose:
        print(f"\n--- 2x2 torus v2 spin-network, g^2 = {g_squared} ---")
        print(f"  irreps: {irrep_set}")
        print(f"  pairs: {include_pairs}, theta: {include_theta_graphs}, "
              f"long_loops: {include_higher_loops}")
    t0 = time.time()
    from cl3_ks_spinnetwork_2x2_2026_05_07 import haar_sample_8links
    samples = haar_sample_8links(N_samples, seed=seed)
    H, Gram, F, labels, holos = build_H_and_Gram(
        g_squared, samples, irrep_set,
        include_pairs=include_pairs,
        include_theta_graphs=include_theta_graphs,
        include_higher_loops=include_higher_loops,
        eps=eps, verbose=verbose,
    )
    evals, evecs, n_keep = diagonalize_with_gram(H, Gram)

    psi0 = evecs[:, 0]
    P_avg = expectation_P(psi0, F, holos)

    if verbose:
        print(f"  E_0 = {evals[0].real:.6f}  (kept {n_keep}/{F.shape[0]})")
        print(f"  <P>_avg = {P_avg:.6f}")
        print(f"  Total time: {time.time()-t0:.1f}s")

    return {
        'g_squared': g_squared,
        'P_avg': P_avg,
        'E_0': evals[0].real,
        'n_basis': F.shape[0],
        'n_kept': n_keep,
    }


if __name__ == "__main__":
    print("=" * 70)
    print("Cl(3) -> KS, 2x2 spatial torus, spin-network ED v2")
    print("(WITH theta-graph linked invariants and longer loops)")
    print("=" * 70)

    print("\n[1] 3 irreps, characters only (baseline)")
    irrep_3 = [(0, 0), (1, 0), (0, 1)]
    r1 = run_one(1.0, irrep_3, N_samples=4000, seed=11,
                  include_pairs=True, include_theta_graphs=False,
                  include_higher_loops=False, eps=1e-2)

    print("\n[2] 3 irreps + theta graphs")
    r2 = run_one(1.0, irrep_3, N_samples=4000, seed=11,
                  include_pairs=True, include_theta_graphs=True,
                  include_higher_loops=False, eps=1e-2)

    print("\n[3] 3 irreps + theta + length-8 loops")
    r3 = run_one(1.0, irrep_3, N_samples=4000, seed=11,
                  include_pairs=True, include_theta_graphs=True,
                  include_higher_loops=True, eps=1e-2)

    print("\n[4] 4 irreps + theta + long loops")
    irrep_4 = [(0, 0), (1, 0), (0, 1), (1, 1)]
    r4 = run_one(1.0, irrep_4, N_samples=4000, seed=11,
                  include_pairs=True, include_theta_graphs=True,
                  include_higher_loops=True, eps=1e-2)

    print("\n=== Summary at g^2 = 1.0 ===")
    print(f"3 irreps, pairs only:                 <P> = {r1['P_avg']:.4f}, n_basis = {r1['n_basis']}")
    print(f"3 irreps, pairs + theta:              <P> = {r2['P_avg']:.4f}, n_basis = {r2['n_basis']}")
    print(f"3 irreps, pairs + theta + long:       <P> = {r3['P_avg']:.4f}, n_basis = {r3['n_basis']}")
    print(f"4 irreps, pairs + theta + long:       <P> = {r4['P_avg']:.4f}, n_basis = {r4['n_basis']}")
    print(f"\nReference targets:")
    print(f"  Wilson 4D MC at beta=6, 2x2x2x16:    0.6243 (spatial)")
    print(f"  Wilson 4D MC at beta=6, 4x4x4x4:     0.5974 (spatial)")
    print(f"  KS literature (3D thermo limit):     ~0.55-0.60")
