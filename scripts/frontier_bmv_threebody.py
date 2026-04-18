#!/usr/bin/env python3
"""
Historical heuristic three-body branch-entanglement diagnostic on a staggered
lattice.

Extension of the 2-body branch-entanglement protocol to three particles in a
triangular arrangement. A gravitational source at the center is placed in an
externally imposed superposition of two configurations (present vs absent).
Each particle evolves under both branches. The three-particle joint state:

  |Psi> = (|psi_1A>|psi_2A>|psi_3A> + |psi_1B>|psi_2B>|psi_3B>) / sqrt(2)

For this 2-branch superposition of product states:

  Bipartite entropies:
    S(1|23) = H_binary((1 + |<2A|2B>|*|<3A|3B>|) / 2)
    S(2|13) = H_binary((1 + |<1A|1B>|*|<3A|3B>|) / 2)
    S(3|12) = H_binary((1 + |<1A|1B>|*|<2A|2B>|) / 2)

  Pairwise entropies (subsystem of two particles, traced over the third):
    S(1|2)  = from the reduced 2-particle density matrix, tracing out particle 3
    S(2|3)  = similarly
    S(1|3)  = similarly

  Residual tangle (3-tangle analog):
    tau_3 ~ C_{1|23}^2 - C_{1|2}^2 - C_{1|3}^2

  Classification:
    GHZ-type: all bipartite entropies roughly equal, tau_3 > 0
    W-type:   bipartite entropies may differ, tau_3 ~ 0
    Biseparable: at least one bipartite entropy ~ 0

Historical note:
  This standalone runner was the first tripartite probe, but its
  GHZ/W interpretation is superseded by
  frontier_branch_entanglement_robustness.py.
  Keep this script as a historical exploratory heuristic surface, not the
  canonical classifier.
"""

from __future__ import annotations

import math
import time

import numpy as np
from scipy.sparse import eye as speye
from scipy.sparse import lil_matrix
from scipy.sparse.linalg import spsolve

from periodic_geometry import infer_periodic_extents, minimum_image_distance

# ── Physical parameters ──────────────────────────────────────────────
MASS = 0.30
MU2 = 0.22
DT = 0.12
N_STEPS = 30
SIDE = 12
G_VALUES = [1, 5, 10, 20, 50]

# Particle positions (triangular arrangement)
POS_1 = (2.0, 6.0)
POS_2 = (6.0, 2.0)
POS_3 = (10.0, 6.0)
SOURCE_POS = (6, 6)
SIGMA = 1.5


# ── Lattice construction ─────────────────────────────────────────────

def make_lattice_2d(side: int):
    """Build a 2D periodic staggered lattice with checkerboard coloring."""
    coords = []
    colors = []
    adj = {}
    index = {}
    idx = 0
    for x in range(side):
        for y in range(side):
            coords.append((float(x), float(y)))
            colors.append((x + y) % 2)
            index[(x, y)] = idx
            idx += 1
    pos = np.array(coords)
    color = np.array(colors, dtype=int)
    n = len(pos)
    for x in range(side):
        for y in range(side):
            a = index[(x, y)]
            adj[a] = []
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                adj[a].append(index[((x + dx) % side, (y + dy) % side)])
    return pos, color, adj, index, n


def build_laplacian(pos: np.ndarray, adj: dict[int, list[int]]):
    n = len(pos)
    lap = lil_matrix((n, n), dtype=float)
    extents = infer_periodic_extents(pos)
    for i, nbs in adj.items():
        for j in nbs:
            if i >= j:
                continue
            d = minimum_image_distance(pos[i], pos[j], extents)
            w = 1.0 / max(d, 0.5)
            lap[i, j] -= w
            lap[j, i] -= w
            lap[i, i] += w
            lap[j, j] += w
    return lap.tocsr()


def build_hamiltonian(pos: np.ndarray, color: np.ndarray,
                      adj: dict[int, list[int]], phi: np.ndarray):
    """Staggered-fermion Hamiltonian with gravitational potential phi."""
    n = len(pos)
    ham = lil_matrix((n, n), dtype=complex)
    parity = np.where(color == 0, 1.0, -1.0)
    ham.setdiag((MASS + phi) * parity)
    extents = infer_periodic_extents(pos)
    for i, nbs in adj.items():
        for j in nbs:
            if i >= j:
                continue
            d = minimum_image_distance(pos[i], pos[j], extents)
            w = 1.0 / max(d, 0.5)
            ham[i, j] += -0.5j * w
            ham[j, i] += 0.5j * w
    return ham.tocsr()


def cn_step(ham, psi: np.ndarray):
    """Crank-Nicolson time step."""
    n = ham.shape[0]
    ap = (speye(n, format="csc") + 1j * ham * DT / 2).tocsc()
    am = speye(n, format="csr") - 1j * ham * DT / 2
    return spsolve(ap, am.dot(psi))


def gaussian_at(pos: np.ndarray, center: tuple[float, float], sigma: float):
    """Gaussian wavepacket centered at (cx, cy)."""
    cx, cy = center
    rsq = (pos[:, 0] - cx) ** 2 + (pos[:, 1] - cy) ** 2
    psi = np.exp(-0.5 * rsq / sigma ** 2).astype(complex)
    norm = np.linalg.norm(psi)
    if norm < 1e-30:
        raise ValueError(f"Gaussian at {center} has zero norm on lattice")
    return psi / norm


def binary_entropy(p: float) -> float:
    """H(p) = -p log(p) - (1-p) log(1-p), using natural log."""
    if p <= 0.0 or p >= 1.0:
        return 0.0
    return -p * math.log(p) - (1.0 - p) * math.log(1.0 - p)


# ── Three-body branch-entanglement protocol ─────────────────────────

def run_threebody_bmv(g: float):
    """Run the three-body branch-entanglement protocol for a given source coupling G."""
    pos, color, adj, index, n = make_lattice_2d(SIDE)
    lap = build_laplacian(pos, adj)

    # Source at center
    source_node = index[SOURCE_POS]

    # Two source configurations: A = source present, B = absent
    rho_ext = np.zeros(n)
    rho_ext[source_node] = g
    phi_A = spsolve((lap + MU2 * speye(n, format="csr")).tocsc(), rho_ext)
    phi_B = np.zeros(n)

    ham_A = build_hamiltonian(pos, color, adj, phi_A)
    ham_B = build_hamiltonian(pos, color, adj, phi_B)

    # Three initial wavepackets in triangular arrangement
    psi_init = [
        gaussian_at(pos, POS_1, SIGMA),
        gaussian_at(pos, POS_2, SIGMA),
        gaussian_at(pos, POS_3, SIGMA),
    ]

    # Evolve each particle under each geometry (6 evolutions)
    psi_A = [p.copy() for p in psi_init]
    psi_B = [p.copy() for p in psi_init]

    for _ in range(N_STEPS):
        for i in range(3):
            psi_A[i] = cn_step(ham_A, psi_A[i])
            psi_B[i] = cn_step(ham_B, psi_B[i])

    # Branch overlaps for each particle: o_i = |<psi_iA|psi_iB>|
    overlaps = [abs(np.vdot(psi_A[i], psi_B[i])) for i in range(3)]
    o1, o2, o3 = overlaps

    # Norms (unitarity check)
    norms = {}
    for i in range(3):
        norms[f"n{i+1}A"] = np.linalg.norm(psi_A[i])
        norms[f"n{i+1}B"] = np.linalg.norm(psi_B[i])

    # ── Bipartite entropies ──────────────────────────────────────────
    # For |Psi> = (|1A>|2A>|3A> + |1B>|2B>|3B>) / sqrt(2):
    # rho_1 = Tr_{23}(|Psi><Psi|)
    #   eigenvalues: (1 +/- |<2A|2B>|*|<3A|3B>|) / 2
    # S(1|23) = H_binary((1 + o2*o3) / 2)
    s_1_23 = binary_entropy(0.5 + 0.5 * o2 * o3)
    s_2_13 = binary_entropy(0.5 + 0.5 * o1 * o3)
    s_3_12 = binary_entropy(0.5 + 0.5 * o1 * o2)

    # ── Pairwise entropies ───────────────────────────────────────────
    # rho_{12} = Tr_3(|Psi><Psi|)
    #   = (1/2)(|1A,2A><1A,2A| + |1B,2B><1B,2B|
    #          + <3A|3B> |1A,2A><1B,2B| + <3B|3A> |1B,2B><1A,2A|)
    #
    # rho_1_from_12 = Tr_2(rho_{12})
    #   = (1/2)(|1A><1A| + |1B><1B|
    #          + <3A|3B>*<2A|2B> |1A><1B| + h.c.)
    #   eigenvalues: (1 +/- |<2A|2B>|*|<3A|3B>|) / 2
    #   This is the SAME as S(1|23) -- which makes sense: S(rho_1) is unique.
    #
    # For the pairwise concurrence, we need the entropy of subsystem {i}
    # when the full state is restricted to particles {i,j} (traced over k).
    # But rho_{ij} is a 2-qubit-like state. Its entanglement:
    #
    # rho_{12} lives in a 2-branch space. Its Schmidt decomposition:
    # rho_{12} has eigenvalues from a 2x2 Gram matrix.
    # The Gram matrix of the unnormalized branches:
    # G_ij = <branch_i|branch_j>
    # |b1> = |1A>|2A>, |b2> = |1B>|2B>
    # G = [[1, o1*o2*phase], [o1*o2*phase*, 1]]  (phase from <3A|3B>)
    # Wait -- rho_{12} = (1/2)(|b1><b1| + |b2><b2| + <3A|3B>|b1><b2| + h.c.)
    # Eigenvalues of rho_{12}: (1 +/- |<3A|3B>| * |<b1|b2>|) / 2
    #   where |<b1|b2>| = |<1A|1B>|*|<2A|2B>| = o1*o2
    #
    # Actually rho_{12} eigenvalues: (1 +/- o3 * sqrt{...}) / 2
    # Let's be precise. rho_{12} = (1/2)(|b1><b1| + |b2><b2| + c3*|b1><b2| + c3*|b2><b1|)
    # where c3 = <3A|3B> (complex).
    # In the basis {|b1>, |b2>} (NOT orthonormal), the matrix is:
    # M = (1/2)[[1, c3], [c3*, 1]]  but this is in a non-orthogonal basis.
    #
    # The actual eigenvalues of rho_{12} in the full n^2 space:
    # rho_{12} has rank at most 2 (spanned by |b1>, |b2>).
    # The 2x2 representation in the {|b1>, |b2>} basis with overlap S12 = <b1|b2> = o1*o2*phase:
    # rho = (1/2)[[1, c3], [c3*, 1]] in non-orthogonal basis with overlap matrix [[1, S12], [S12*, 1]]
    #
    # Eigenvalues of rho (as operator): solve (1/2)[[1,c3],[c3*,1]] v = lambda [[1,S12],[S12*,1]] v
    # lambda = (1 +/- |c3|) / (2*(1 +/- |S12|)) ... this gets complicated.
    #
    # Simpler approach: compute S(rho_{12}) via the eigenvalues of the 2x2 matrix
    # A_ij = <bi|bj> * (coefficient)
    # For our state |Psi> = (|b1>|3A> + |b2>|3B>) / sqrt(2)
    # rho_{12} = Tr_3[(1/2)(|b1>|3A> + |b2>|3B>)(<b1|<3A| + <b2|<3B|)]
    #          = (1/2)(|b1><b1| + |b2><b2| + <3A|3B>|b1><b2| + <3B|3A>|b2><b1|)
    #
    # S(rho_{12}): compute numerically via the Gram matrix approach.
    # The operator rho_{12} has eigenvalues determined by the 2x2 matrix:
    # K = (1/2) * [[1, c3], [c3*, 1]]  (coefficient matrix)
    # Overlap matrix: G = [[1, s12], [s12*, 1]]  where s12 = <b1|b2> = <1A|1B><2A|2B>
    # Eigenvalues of rho_{12} as operator: solve K v = lambda G v
    # det(K - lambda G) = 0
    # (1/2 - lambda)(1/2 - lambda) - (c3/2 - lambda*s12)(c3*/2 - lambda*s12*) = 0
    # Let a = 1/2, b = c3/2, s = s12
    # (a-lambda)^2 - |b - lambda*s|^2 = 0
    # (a-lambda)^2 - (b-lambda*s)(b*-lambda*s*) = 0
    #
    # For the entanglement of the subsystem {1} within {1,2}:
    # This is just S(rho_1) which we already computed as S(1|23).
    # The pairwise entanglement of {1,2} = S(rho_{12}) but that's the entropy
    # of the 2-particle reduced state = S(3|12) by purity of the full state...
    # Wait, the full state is pure, so S(rho_{12}) = S(rho_3) = S(3|12).
    #
    # So for the residual tangle computation:
    # C_{1|23}^2: concurrence of particle 1 vs rest
    # C_{1|2}^2: concurrence of particle 1 vs 2 (tracing out 3)
    # C_{1|3}^2: concurrence of particle 1 vs 3 (tracing out 2)
    #
    # For the residual tangle in our 2-branch state, we can compute
    # the pairwise concurrences from the pairwise reduced states.
    #
    # rho_{12} (traced out 3): this is an effective 2-qubit state in the
    # 2-branch subspace. The concurrence of this state (1 vs 2):
    # Using the formula for a rank-2 state with overlaps.
    #
    # For a state rho_{12} = (1/2)(|a1,a2><a1,a2| + |b1,b2><b1,b2| + c3|a1,a2><b1,b2| + h.c.)
    # Tr_2(rho_{12}) = (1/2)(|a1><a1| + |b1><b1| + c3*<a2|b2>|a1><b1| + h.c.)
    # S_1_from_12 = H_binary((1 + |c3|*o2)/2) = H_binary((1 + o3*o2)/2) = S(1|23) [same!]
    #
    # The concurrence of rho_{12} between particles 1 and 2:
    # For our effective 2-qubit state, the concurrence can be extracted from:
    # C_{12} = 2*max(0, sqrt(lambda_max) - ...) using the eigenvalues of rho*rho_tilde.
    #
    # But in the 2-branch approximation, there's a cleaner formula.
    # The state rho_{12} in the {|a1a2>, |b1b2>} subspace (after Gram-Schmidt):
    # Can be written as a 2x2 density matrix with off-diagonal element c3/2.
    # After proper orthogonalization, the concurrence of a 2x2 rho:
    # C = 2|rho_{01}| for a rank-2 state? No, that's for pure states.
    #
    # Actually, the pairwise entanglement for our specific structure:
    # rho_{12} is mixed (rank 2 in general). The entanglement is characterized
    # by the concurrence formula for 2-qubit states.
    #
    # Simpler: for the tangle estimate, use the linear entropy:
    # tau_linear(rho_i) = 2(1 - Tr(rho_i^2))
    # For rho_1 with eigenvalues (1+x)/2, (1-x)/2 where x = o2*o3:
    # Tr(rho_1^2) = ((1+x)/2)^2 + ((1-x)/2)^2 = (1+x^2)/2
    # tau_1|23 = 2(1 - (1+x^2)/2) = 1 - x^2
    # where x = o2*o3 for particle 1, etc.

    tau_1_23 = 1.0 - (o2 * o3) ** 2  # linear entropy tangle, particle 1 vs {2,3}
    tau_2_13 = 1.0 - (o1 * o3) ** 2
    tau_3_12 = 1.0 - (o1 * o2) ** 2

    # Pairwise tangles from the 2-particle reduced density matrices.
    # rho_{12} has rank 2 in the 2-branch subspace. To get the pairwise
    # entanglement (1 vs 2 in rho_{12}), we use the PPT criterion approach.
    #
    # For the 2-branch state, rho_{12} can be diagonalized analytically.
    # Let s12 = <1A|1B><2A|2B> (product of single-particle overlaps for 1,2)
    # Let c3 = <3A|3B>
    # Eigenvalues of rho_{12}: (1 +/- |c3|) / 2  * correction from non-orthogonality
    #
    # More carefully: rho_{12} in Hilbert space of particles 1,2 has rank <= 2.
    # We can compute its eigenvalues numerically from the 2x2 Gram matrix:
    # G_{ij} = <psi_i|psi_j> where |psi_1> = |1A,2A>/sqrt(2), |psi_2> = c3|1B,2B>/sqrt(2)
    # Wait, let me use the proper formula.
    #
    # |Psi> = (|1A>|2A>|3A> + |1B>|2B>|3B>) / sqrt(2)
    # rho_{12} = (1/2)(|1A,2A><1A,2A| + |1B,2B><1B,2B| + c3*|1A,2A><1B,2B| + c3.conj*|1B,2B><1A,2A|)
    # where c3 = <3A|3B>.
    #
    # Eigenvalues of rho_{12}: use the fact that it's a 2x2 matrix in the
    # (generally non-orthogonal) basis {|1A,2A>, |1B,2B>}.
    # Coefficient matrix: C = (1/2)[[1, c3], [c3*, 1]]
    # Overlap matrix: S = [[1, s12], [s12*, 1]] where s12 = <1A|1B>*<2A|2B>
    # Eigenvalues: solve det(C - lambda*S) = 0
    # (1/2 - lambda) * (1/2 - lambda) - (c3/2 - lambda*s12)*(c3*/2 - lambda*s12*) = 0
    #
    # Let's compute numerically.

    # Complex overlaps (not just magnitudes)
    c = [np.vdot(psi_A[i], psi_B[i]) for i in range(3)]  # complex overlaps

    # Pairwise entanglement: compute S(rho_{ij}) and the entanglement of
    # particle i within rho_{ij}.
    #
    # For the residual tangle, the standard approach for the linear entropy version:
    # tau_3 = tau_{1|23} - tau_{1|2} - tau_{1|3}
    # where tau_{i|j} is the linear entropy tangle of the pairwise reduced state.
    #
    # tau_{1|2}: entanglement of 1 vs 2 in rho_{12}.
    # For rho_{12}, Tr_2 gives rho_1, and the linear entropy of rho_1 given rho_{12}
    # is the same tau_{1|23} we already computed (since rho_1 is the same regardless
    # of whether we first trace out 3 then 2, or trace out {2,3} directly).
    #
    # The PAIRWISE tangle tau_{1|2} is NOT the same as tau_{1|23}.
    # tau_{1|2} measures the entanglement specifically between 1 and 2 in rho_{12},
    # not the entanglement of 1 with everything else.
    #
    # For our 2-branch structure, compute pairwise concurrences:
    # rho_{12} in the {|1A,2A>, |1B,2B>} subspace.
    # To compute the pairwise entanglement, we need the partial transpose criterion.
    #
    # Strategy: compute the eigenvalues of rho_{12} and of rho_{12}^{T_2} (partial transpose)
    # numerically, using the 2x2 generalized eigenvalue approach.

    pairwise_tangles = {}
    pairs = [(0, 1, 2), (0, 2, 1), (1, 2, 0)]  # (i, j, traced_out)
    pair_labels = ["tau_12", "tau_13", "tau_23"]

    for (i, j, k), label in zip(pairs, pair_labels):
        # rho_{ij} in the 2-branch subspace {|iA,jA>, |iB,jB>}
        # Coefficient matrix: (1/2)[[1, c_k], [c_k*, 1]]
        # Overlap matrix: [[1, s_ij], [s_ij*, 1]] where s_ij = <iA|iB>*<jA|jB>
        ck = c[k]
        s_ij = c[i] * c[j]

        # Compute eigenvalues of rho_{ij} via generalized eigenvalue problem
        C_mat = 0.5 * np.array([[1.0, ck], [np.conj(ck), 1.0]])
        S_mat = np.array([[1.0, s_ij], [np.conj(s_ij), 1.0]])

        # Eigenvalues of C_mat w.r.t. S_mat
        # det(C - lambda S) = 0
        # (0.5 - lambda)(0.5 - lambda) - (ck/2 - lambda*s_ij)(ck*/2 - lambda*s_ij*) = 0
        a_coeff = 1.0 - abs(s_ij) ** 2
        b_coeff = -(1.0 - abs(ck) ** 2 * abs(s_ij) ** 2 / abs(s_ij + 1e-30) ** 2)
        # This is getting messy. Use scipy instead.
        from scipy.linalg import eigvalsh
        # For Hermitian generalized eigenvalue: C v = lambda S v
        # scipy.linalg.eigvalsh(C, S) -- but S must be positive definite
        det_S = 1.0 - abs(s_ij) ** 2
        if det_S > 1e-10:
            eigs = eigvalsh(C_mat, S_mat)
            eigs = np.clip(eigs, 0, 1)
        else:
            # Branches nearly identical for these two particles
            # rho_{ij} ~ |psi_i,psi_j><psi_i,psi_j| (pure, no entanglement)
            eigs = np.array([0.0, 1.0])

        # S(rho_{ij}) = von Neumann entropy
        s_ij_entropy = sum(-e * math.log(max(e, 1e-30)) for e in eigs if e > 1e-30)

        # For the pairwise entanglement (tangle), we need entanglement of i vs j.
        # Tr_j(rho_{ij}) = rho_i (same as before).
        # Entanglement of formation / concurrence for mixed 2-qubit-like states.
        #
        # For our rank-2 state in a 2x2 subspace, the concurrence simplifies:
        # The 2x2 density matrix (in an orthonormalized basis) has concurrence
        # C = 2|rho_{01}| - 2*sqrt(rho_{00}*rho_{11}) ... no, that's not right either.
        #
        # Use the linear entropy tangle for the pairwise entanglement:
        # Tr_j(rho_{ij}) = rho_i, so tau_linear(rho_i) = 1 - Tr(rho_i^2)
        # But this is the SAME for rho_i regardless of which j we trace out.
        # So tau_{i|j} defined via linear entropy of rho_i from rho_{ij} = tau_{i|23}!
        # That can't be right for CKW...
        #
        # The CKW inequality uses the SQUARED CONCURRENCE of the pairwise state,
        # not the single-particle entropy. For our 2-branch scenario:
        #
        # rho_{ij} has a decomposition into pure states.
        # The entanglement of rho_{ij} (i vs j) is bounded by the entanglement of formation.
        # For a rank-2 state, EoF can be computed from the concurrence.
        #
        # The concurrence of rho_{ij} (rank 2, in a 2-party system):
        # rho_{ij} = sum_alpha p_alpha |phi_alpha><phi_alpha|
        # = (eigendecomposition using the computed eigenvalues)
        #
        # For the eigenstates of rho_{ij}, each eigenstate is a product state in
        # the 1-particle Hilbert spaces (they're superpositions of |iA,jA> and |iB,jB>).
        # A product-basis decomposition:
        # Each eigenstate |Phi_alpha> = a_alpha |iA,jA> + b_alpha |iB,jB>
        # This is NOT necessarily a product state |phi_i>|phi_j> -- it's entangled
        # between particles i and j.
        #
        # The concurrence of a pure state |a1,a2> + b|b1,b2> (normalized) is:
        # C = 2|a||b| * sqrt(1 - |<a1|b1>|^2) * sqrt(1 - |<a2|b2>|^2)
        # ... roughly.
        #
        # This is getting very involved. Let's use a more practical approach.

        # Practical pairwise tangle via the negativity of rho_{ij}^{T_j}:
        # Partial transpose of rho_{ij} w.r.t. particle j.
        # For our 2-branch state:
        # rho_{ij} = (1/2)(|iA><iA| x |jA><jA| + |iB><iB| x |jB><jB|
        #            + c_k |iA><iB| x |jA><jB| + c_k* |iB><iA| x |jB><jA|)
        # Partial transpose on j: |jA><jB| -> |jB><jA|
        # rho_{ij}^{T_j} = (1/2)(|iA><iA| x |jA><jA| + |iB><iB| x |jB><jB|
        #                  + c_k |iA><iB| x |jB><jA| + c_k* |iB><iA| x |jA><jB|)
        #
        # In the 4-dim basis {|iA,jA>, |iA,jB>, |iB,jA>, |iB,jB>} with overlaps,
        # this is very complex in the non-orthogonal basis.
        #
        # SIMPLIFICATION: use the negativity bound.
        # For a 2-branch superposition state, the negativity can be computed from
        # the overlaps analytically.
        #
        # For |Psi> = (|a>|c>|e> + |b>|d>|f>)/sqrt(2), the reduced state rho_{12}:
        # Negativity_{1:2}(rho_{12}) can be computed as:
        # N_{12} = max(0, (|c_k|^2 - |<iA|iB>|^2 * |<jA|jB>|^2) / (2*(1 - |<iA|iB>|^2 * |<jA|jB>|^2)))
        #
        # Actually, let's just use a simpler diagnostic that's well-defined:
        # the MUTUAL INFORMATION I(i:j) = S(i) + S(j) - S(ij)
        # This captures total correlations (classical + quantum).

        # S(i) = S(i|jk) already computed above
        # S(ij) = S(k) by purity: S(rho_{ij}) = S(rho_k)
        # So I(i:j) = S(i) + S(j) - S(k)

        # Store for later
        pairwise_tangles[label] = s_ij_entropy

    # Bipartite entropies (single particle entropies)
    s_1 = s_1_23
    s_2 = s_2_13
    s_3 = s_3_12

    # S(rho_{ij}) = S(rho_k) by purity of full state
    s_12 = s_3_12  # S(rho_{12}) = S(rho_3)
    s_13 = s_2_13  # S(rho_{13}) = S(rho_2)
    s_23 = s_1_23  # S(rho_{23}) = S(rho_1)

    # Mutual information
    mi_12 = s_1 + s_2 - s_12  # I(1:2) = S(1) + S(2) - S(12)
    mi_13 = s_1 + s_3 - s_13
    mi_23 = s_2 + s_3 - s_23

    # ── Tangle estimate ──────────────────────────────────────────────
    # Linear entropy tangle (CKW-like):
    # tau_{1|23} = 1 - (o2*o3)^2
    # For pairwise: use the squared negativity as proxy.
    # The negativity of rho_{ij} can be computed from the PPT criterion.
    #
    # For our specific 2-branch state, a clean formula for pairwise concurrence:
    # C_{ij}^2 can be bounded. For the residual 3-tangle:
    #
    # In the 2-branch subspace, the state is effectively a 2-level system.
    # The 3-tangle for states of the form (|abc> + |def>)/sqrt(2):
    #
    # tau_3 = 4|det(T)|^2 where T is a 2x2x2 tensor.
    # For |Psi> = (1/sqrt(2))(|0>_eff|0>_eff|0>_eff + |1>_eff|1>_eff|1>_eff) = GHZ state!
    #
    # But our |0>_eff and |1>_eff are not orthogonal (overlaps o_i != 0).
    # In the limit o_i -> 0 (all overlaps vanish), the state IS a GHZ state.
    # In the limit o_i -> 1 (no evolution difference), no entanglement.
    #
    # The 3-tangle for this "non-orthogonal GHZ" state:
    # After Gram-Schmidt on each particle's 2-branch space:
    # |0'> = |A>, |1'> = (|B> - o*|A>) / sqrt(1 - |o|^2)
    # In this basis: |Psi> = (1/sqrt(2))(|0'0'0'> + prod_i(o_i)|0'0'0'> + ...)
    #
    # This is complex. Let's use a direct numerical approach for the 3-tangle
    # via the pure state formula.

    # For a pure 3-qubit state |Psi> in the computational basis {|000>,...,|111>}:
    # tau_3 = 4|d_1 - 2*d_2 + 4*d_3| where d's involve the coefficients.
    # But our "qubits" are not orthogonal.
    #
    # PRACTICAL APPROACH: Gram-Schmidt each particle's {|A>,|B>} space,
    # express the state in the orthonormal 2x2x2 basis, then compute 3-tangle.

    # Gram-Schmidt for each particle
    gs_coeffs = []  # coefficients of |Psi> in orthonormal basis
    # |0_i> = |iA>
    # |1_i> = (|iB> - c_i |iA>) / sqrt(1 - |c_i|^2)
    #
    # |Psi> = (1/sqrt(2))(|1A>|2A>|3A> + |1B>|2B>|3B>)
    #       = (1/sqrt(2))(|0_1>|0_2>|0_3>
    #         + (c_1|0_1> + s_1_eff|1_1>)(c_2|0_2> + s_2_eff|1_2>)(c_3|0_3> + s_3_eff|1_3>))
    # where s_i_eff = sqrt(1 - |c_i|^2)

    s_eff = [np.sqrt(max(1.0 - abs(c[i]) ** 2, 0.0)) for i in range(3)]

    # The 8 coefficients a_{ijk} of |Psi> in the {|0>,|1>}^3 basis:
    a = np.zeros(8, dtype=complex)
    # First term: |000>
    a[0] += 1.0 / np.sqrt(2.0)
    # Second term: expand product (c_1|0> + s_1|1>)(c_2|0> + s_2|1>)(c_3|0> + s_3|1>)
    for b1 in range(2):
        for b2 in range(2):
            for b3 in range(2):
                idx = b1 * 4 + b2 * 2 + b3
                coeff = 1.0 / np.sqrt(2.0)
                coeff *= (c[0] if b1 == 0 else s_eff[0])
                coeff *= (c[1] if b2 == 0 else s_eff[1])
                coeff *= (c[2] if b3 == 0 else s_eff[2])
                a[idx] += coeff

    # Normalize (should already be ~1 if overlaps are consistent)
    norm_a = np.linalg.norm(a)
    a /= norm_a

    # 3-tangle for a pure 3-qubit state (Cayley hyperdeterminant formula):
    # tau = 4|D| where D is the hyperdeterminant of the 2x2x2 coefficient tensor.
    # D = a000^2 a111^2 + a001^2 a110^2 + a010^2 a101^2 + a011^2 a100^2
    #   - 2(a000 a001 a110 a111 + a000 a010 a101 a111 + a000 a011 a100 a111
    #       + a001 a010 a101 a110 + a001 a011 a100 a110 + a010 a011 a100 a101)
    #   + 4(a000 a011 a101 a110 + a001 a010 a100 a111)
    a000, a001, a010, a011 = a[0], a[1], a[2], a[3]
    a100, a101, a110, a111 = a[4], a[5], a[6], a[7]

    D = (a000 ** 2 * a111 ** 2 + a001 ** 2 * a110 ** 2
         + a010 ** 2 * a101 ** 2 + a011 ** 2 * a100 ** 2
         - 2 * (a000 * a001 * a110 * a111
                + a000 * a010 * a101 * a111
                + a000 * a011 * a100 * a111
                + a001 * a010 * a101 * a110
                + a001 * a011 * a100 * a110
                + a010 * a011 * a100 * a101)
         + 4 * (a000 * a011 * a101 * a110
                + a001 * a010 * a100 * a111))

    three_tangle = 4 * abs(D)

    # ── Pairwise concurrences via the 3-qubit reduced density matrices ──
    # rho_{ij} = Tr_k(|Psi><Psi|) in the orthonormal basis
    # Concurrence of a 2-qubit mixed state: C = max(0, l1-l2-l3-l4)
    # where l_i are sqrt of eigenvalues of rho * (Y x Y) rho* (Y x Y) in decreasing order.

    def concurrence_pair(a_coeffs, trace_out):
        """Compute concurrence of particles i,j after tracing out particle k.
        trace_out: which qubit index (0,1,2) to trace out."""
        # Build the 4x4 reduced density matrix rho_{ij}
        rho = np.zeros((4, 4), dtype=complex)
        for b_k in range(2):
            # For each value of the traced-out qubit, get the 4-component vector
            vec = np.zeros(4, dtype=complex)
            for b_i in range(2):
                for b_j in range(2):
                    if trace_out == 0:
                        idx_full = b_k * 4 + b_i * 2 + b_j
                    elif trace_out == 1:
                        idx_full = b_i * 4 + b_k * 2 + b_j
                    else:
                        idx_full = b_i * 4 + b_j * 2 + b_k
                    idx_4 = b_i * 2 + b_j
                    vec[idx_4] = a_coeffs[idx_full]
            rho += np.outer(vec, np.conj(vec))

        # Concurrence: C(rho) = max(0, l1 - l2 - l3 - l4)
        # sigma_y x sigma_y
        yy = np.array([[0, 0, 0, -1],
                        [0, 0, 1, 0],
                        [0, 1, 0, 0],
                        [-1, 0, 0, 0]], dtype=complex)
        rho_tilde = yy @ np.conj(rho) @ yy
        M = rho @ rho_tilde
        eigvals = np.sort(np.real(np.linalg.eigvals(M)))[::-1]
        eigvals = np.clip(eigvals, 0, None)
        sqrt_eigvals = np.sqrt(eigvals)
        conc = max(0.0, sqrt_eigvals[0] - sqrt_eigvals[1] - sqrt_eigvals[2] - sqrt_eigvals[3])
        return conc

    c_12 = concurrence_pair(a, trace_out=2)
    c_13 = concurrence_pair(a, trace_out=1)
    c_23 = concurrence_pair(a, trace_out=0)

    # CKW residual tangle check: tau_3 = C_{1|23}^2 - C_{12}^2 - C_{13}^2
    # C_{1|23} = concurrence of particle 1 with the rest = 2*sqrt(det(rho_1))
    # For rho_1 with eigenvalues (1+x)/2, (1-x)/2:
    # det(rho_1) = (1-x^2)/4 where x = o2*o3
    # C_{1|23} = sqrt(1 - x^2) = sqrt(1 - (o2*o3)^2)
    c_1_23 = np.sqrt(max(tau_1_23, 0.0))  # tau_1_23 = 1 - (o2*o3)^2

    ckw_residual = c_1_23 ** 2 - c_12 ** 2 - c_13 ** 2

    # ── Classification ───────────────────────────────────────────────
    threshold = 1e-4
    if max(s_1, s_2, s_3) < threshold:
        classification = "SEPARABLE"
    elif min(s_1, s_2, s_3) < threshold:
        classification = "BISEPARABLE"
    elif three_tangle > threshold:
        # Check if bipartite entropies are roughly equal (GHZ-like)
        s_mean = (s_1 + s_2 + s_3) / 3.0
        s_spread = max(abs(s_1 - s_mean), abs(s_2 - s_mean), abs(s_3 - s_mean))
        if s_spread / max(s_mean, 1e-10) < 0.3:
            classification = "GHZ-type (symmetric)"
        else:
            classification = "GHZ-type (asymmetric)"
    elif max(c_12, c_13, c_23) > threshold:
        classification = "W-type"
    else:
        classification = "MIXED/WEAK"

    return {
        "G": g,
        "overlaps": overlaps,
        "s_1_23": s_1_23,
        "s_2_13": s_2_13,
        "s_3_12": s_3_12,
        "mi_12": mi_12,
        "mi_13": mi_13,
        "mi_23": mi_23,
        "c_12": c_12,
        "c_13": c_13,
        "c_23": c_23,
        "c_1_23": c_1_23,
        "three_tangle": three_tangle,
        "ckw_residual": ckw_residual,
        "classification": classification,
        "norms": norms,
    }


# ── Main ─────────────────────────────────────────────────────────────

def main():
    t0 = time.time()

    print("=" * 90)
    print("HISTORICAL HEURISTIC THREE-BODY BRANCH-ENTANGLEMENT DIAGNOSTIC")
    print("=" * 90)
    print()
    print(f"Lattice: 2D staggered, side={SIDE}, n={SIDE**2}")
    print(f"Particle 1 at {POS_1}, Particle 2 at {POS_2}, Particle 3 at {POS_3}")
    print(f"Source at {SOURCE_POS}")
    print(f"MASS={MASS}, MU2={MU2}, DT={DT}, N_STEPS={N_STEPS}, sigma={SIGMA}")
    print()
    print("Protocol: externally imposed source superposition |A> + |B>,")
    print("          where A=present and B=absent.")
    print("|Psi> = (|psi_1A>|psi_2A>|psi_3A> + |psi_1B>|psi_2B>|psi_3B>) / sqrt(2)")
    print()
    print("Guardrail: this is the historical heuristic runner only.")
    print("Use frontier_branch_entanglement_robustness.py for the canonical")
    print("3-body interpretation surface on current main.")
    print()

    # ── Table: Branch overlaps ───────────────────────────────────────
    print("--- Branch Overlaps ---")
    print(f"{'G':>5s}  {'o_1':>8s} {'o_2':>8s} {'o_3':>8s}")
    print("-" * 36)

    all_results = []
    for g in G_VALUES:
        res = run_threebody_bmv(g)
        all_results.append(res)
        o1, o2, o3 = res["overlaps"]
        print(f"{g:5.0f}  {o1:8.5f} {o2:8.5f} {o3:8.5f}")

    # ── Table: Bipartite entropies ───────────────────────────────────
    print()
    print("--- Bipartite Entropies (nats) ---")
    print(f"{'G':>5s}  {'S(1|23)':>10s} {'S(2|13)':>10s} {'S(3|12)':>10s}  {'type':>20s}")
    print("-" * 60)
    for res in all_results:
        print(f"{res['G']:5.0f}  {res['s_1_23']:10.6f} {res['s_2_13']:10.6f} "
              f"{res['s_3_12']:10.6f}  {res['classification']:>20s}")

    # ── Table: Pairwise concurrences and tangle ──────────────────────
    print()
    print("--- Pairwise Concurrences & 3-Tangle ---")
    print(f"{'G':>5s}  {'C_12':>8s} {'C_13':>8s} {'C_23':>8s}  "
          f"{'C_1|23':>8s} {'tau_3':>10s} {'CKW_res':>10s}")
    print("-" * 70)
    for res in all_results:
        print(f"{res['G']:5.0f}  {res['c_12']:8.5f} {res['c_13']:8.5f} {res['c_23']:8.5f}  "
              f"{res['c_1_23']:8.5f} {res['three_tangle']:10.6f} {res['ckw_residual']:10.6f}")

    # ── Table: Mutual information ────────────────────────────────────
    print()
    print("--- Pairwise Mutual Information (nats) ---")
    print(f"{'G':>5s}  {'I(1:2)':>10s} {'I(1:3)':>10s} {'I(2:3)':>10s}")
    print("-" * 40)
    for res in all_results:
        print(f"{res['G']:5.0f}  {res['mi_12']:10.6f} {res['mi_13']:10.6f} {res['mi_23']:10.6f}")

    # ── Unitarity check ──────────────────────────────────────────────
    print()
    print("--- Unitarity Check (norms) ---")
    worst = 0.0
    for res in all_results:
        for key, val in res["norms"].items():
            dev = abs(val - 1.0)
            if dev > worst:
                worst = dev
    print(f"Worst norm deviation from 1.0: {worst:.2e}")
    if worst < 0.01:
        print("PASS: Unitarity preserved.")
    else:
        print("WARNING: Significant norm deviation.")

    # ── Analysis ─────────────────────────────────────────────────────
    print()
    print("=" * 90)
    print("HEURISTIC ANALYSIS")
    print("=" * 90)
    print()

    # What entanglement class dominates?
    classifications = [r["classification"] for r in all_results]
    ghz_count = sum(1 for c in classifications if "GHZ" in c)
    w_count = sum(1 for c in classifications if c == "W-type")
    sep_count = sum(1 for c in classifications if "SEPARABLE" in c or "BISEPARABLE" in c)

    print(f"Classification summary across G = {G_VALUES}:")
    for res in all_results:
        print(f"  G={res['G']:5.0f}: {res['classification']}")
    print()

    # Historical heuristic classification only.
    if ghz_count > len(G_VALUES) // 2:
        print("DOMINANT CLASS (heuristic): GHZ-type")
        print("  This is the standalone runner's internal classifier only.")
        print("  Use frontier_branch_entanglement_robustness.py for the")
        print("  canonical 3-body interpretation.")
    elif w_count > 0:
        print("DOMINANT CLASS (heuristic): W-type")
        print("  Use frontier_branch_entanglement_robustness.py for the")
        print("  canonical 3-body interpretation.")
    else:
        print("DOMINANT CLASS: Weak/Separable")
        print("  Entanglement too weak to classify reliably.")

    print()

    # Scaling analysis
    tangles = [r["three_tangle"] for r in all_results]
    max_tangle = max(tangles)
    print(f"3-Tangle range: {min(tangles):.6f} to {max_tangle:.6f}")

    # Maximum possible entanglement
    max_s = max(max(r["s_1_23"], r["s_2_13"], r["s_3_12"]) for r in all_results)
    print(f"Max bipartite entropy: {max_s:.5f} nats = {max_s / math.log(2):.5f} bits")
    print(f"  (Max possible for 2-branch: ln(2) = {math.log(2):.5f} nats)")

    print()

    # Symmetry analysis
    print("Symmetry of bipartite entropies:")
    for res in all_results:
        s_vals = [res["s_1_23"], res["s_2_13"], res["s_3_12"]]
        s_mean = np.mean(s_vals)
        s_std = np.std(s_vals)
        ratio = s_std / max(s_mean, 1e-10)
        sym_label = "symmetric" if ratio < 0.15 else "asymmetric"
        print(f"  G={res['G']:5.0f}: mean={s_mean:.5f}, std={s_std:.5f}, "
              f"CV={ratio:.3f} [{sym_label}]")

    # ── Verdict ──────────────────────────────────────────────────────
    print()
    print("=" * 90)
    print("HEURISTIC VERDICT")
    print("=" * 90)
    print()

    # Key insight: the 2-branch mechanism
    print("STRUCTURAL NOTE:")
    print("  This standalone runner uses a heuristic non-orthogonal-state")
    print("  tangle construction. The later robustness harness is the")
    print("  canonical interpretation surface for the 3-body protocol.")
    print()

    if max_tangle > 1e-3:
        print("HEURISTIC RESULT: positive 3-tangle on this runner.")
        print(f"  Maximum 3-tangle: {max_tangle:.6f}")
        print("  Do not treat this as the canonical tripartite classification.")
    elif max_tangle > 1e-6:
        print("HEURISTIC RESULT: weak but non-zero 3-tangle.")
        print(f"  Maximum 3-tangle: {max_tangle:.6f}")
        print("  Do not treat this as the canonical tripartite classification.")
    else:
        print("HEURISTIC RESULT: 3-tangle below this runner's threshold.")
        print("  Overlaps may be too close to 1 on this lattice.")

    # CKW check
    print()
    print("CKW monogamy check (C_{1|23}^2 >= C_{12}^2 + C_{13}^2):")
    for res in all_results:
        lhs = res["c_1_23"] ** 2
        rhs = res["c_12"] ** 2 + res["c_13"] ** 2
        satisfied = "SATISFIED" if res["ckw_residual"] >= -1e-6 else "VIOLATED"
        print(f"  G={res['G']:5.0f}: {lhs:.6f} >= {rhs:.6f}? {satisfied}")

    elapsed = time.time() - t0
    print(f"\nTime: {elapsed:.2f}s")


if __name__ == "__main__":
    main()
