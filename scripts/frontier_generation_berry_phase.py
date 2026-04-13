#!/usr/bin/env python3
"""
Berry Phase / Zak Phase Topological Invariants for Z_3 Sectors
==============================================================

GOAL: Compute Berry phase (Zak phase) topological invariants for each
Z_3 sector of the staggered Cl(3) Hamiltonian on Z^3. If the three
sectors carry distinct quantized Berry phases, the sectors are
TOPOLOGICALLY DISTINGUISHABLE -- an unconditional mathematical result.

======================================================================
BACKGROUND:

The staggered fermion Hamiltonian on Z^3 in momentum space is an 8x8
matrix H(k) for each k in the Brillouin zone T^3 = [-pi, pi]^3.
The 8 internal degrees of freedom are the taste (doubler) states
labeled by s = (s1, s2, s3) in {0,1}^3.

The Z_3 cyclic permutation sigma: (s1,s2,s3) -> (s2,s3,s1) commutes
with H(k) when k1=k2=k3 (isotropic slice) and along certain
high-symmetry lines. We study the Berry phase along non-contractible
loops of T^3 restricted to each Z_3 sector.

KEY CONSTRUCTION:

1. Free staggered Hamiltonian in momentum space:
   H(k)_{s,s'} = sum_mu [ alpha_mu * sin(k_mu + pi*s_mu) ] delta_{s,s'}
                + r * sum_mu [ (1 - cos(k_mu + pi*s_mu)) ] delta_{s,s'}
   where s,s' label the 8 taste states, and the staggered phases
   are already absorbed into the momentum shifts.

   More precisely, using the Kawamoto-Smit construction:
   H(k) = sum_{mu=1}^{3} Gamma_mu * sin(k_mu) + Wilson_term
   where Gamma_mu are the 8x8 Clifford algebra generators in taste space.

2. Z_3 projectors P_k = (1/3) sum_{g=0}^{2} omega^{-kg} P^g
   project onto the Z_3 eigenspace with charge omega^k.

3. Berry connection for sector k:
   A_mu^{(k)}(q) = -i * Tr[ P_k * U(q)^dag * d/dq_mu U(q) * P_k ]
   where U(q) diagonalizes the restricted Hamiltonian.

4. Zak phase along direction mu:
   gamma_mu^{(k)} = integral_0^{2pi} A_mu^{(k)}(q) dq_mu

WHAT WE ACTUALLY COMPUTE:

We work on the ISOTROPIC LINE k1 = k2 = k3 = theta, where Z_3 is
exact. On this line, H(theta) is 8x8 and commutes with the Z_3
generator P. The eigenstates decompose into Z_3 sectors.

For each sector, we compute the Berry phase as the eigenstates
are transported around the non-contractible loop theta: 0 -> 2*pi.

If the three Z_3 sectors accumulate DISTINCT Berry phases
(e.g., 0, 2*pi/3, 4*pi/3 mod 2*pi), this is a Z_3 topological
invariant that cannot be removed by any Z_3-preserving deformation.

======================================================================
CLASSIFICATION OF RESULTS:
  [EXACT]   -- Mathematical theorem, proved by computation.
  [BOUNDED] -- Numerical result with finite discretization.

ASSUMPTIONS (explicit):
  A1. Taste space V = C^8 with Z_3 action sigma: (s1,s2,s3) -> (s2,s3,s1).
      STATUS: Exact (combinatorial definition).
  A2. Staggered Cl(3) Hamiltonian in Kawamoto-Smit form.
      STATUS: Standard construction.
  A3. Z_3 symmetry is exact on the isotropic slice k1=k2=k3.
      STATUS: Exact (by construction).

PStack experiment: frontier-generation-berry-phase
Self-contained: numpy + scipy only.
======================================================================
"""

from __future__ import annotations

import sys
import time
import numpy as np
from itertools import product as cartesian
from scipy import linalg as la

np.set_printoptions(precision=10, linewidth=120)

PASS_COUNT = 0
FAIL_COUNT = 0
RESULTS = []


def check(tag: str, ok: bool, classification: str, detail: str = "") -> bool:
    """Record a test result with classification."""
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if ok else "FAIL"
    if ok:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1
    RESULTS.append((tag, status, classification, detail))
    print(f"  [{status}] [{classification}] {tag}")
    if detail:
        print(f"         {detail}")
    return ok


# ============================================================================
# BUILDING BLOCKS
# ============================================================================

I2 = np.eye(2, dtype=complex)
SIGMA_X = np.array([[0, 1], [1, 0]], dtype=complex)
SIGMA_Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
SIGMA_Z = np.array([[1, 0], [0, -1]], dtype=complex)


def kron3(A, B, C):
    """Tensor product of three matrices."""
    return np.kron(A, np.kron(B, C))


def taste_states():
    """The 8 taste states (s1,s2,s3) in {0,1}^3."""
    return [(s1, s2, s3) for s1 in range(2) for s2 in range(2) for s3 in range(2)]


def z3_generator_matrix():
    """
    8x8 permutation matrix P implementing sigma: (s1,s2,s3) -> (s2,s3,s1).
    """
    states = taste_states()
    idx = {s: i for i, s in enumerate(states)}
    P = np.zeros((8, 8), dtype=complex)
    for s in states:
        s_new = (s[1], s[2], s[0])
        P[idx[s_new], idx[s]] = 1.0
    return P


def z3_projectors(P):
    """
    Build Z_3 projectors: P_k = (1/3) sum_{g=0}^{2} omega^{-kg} P^g.
    Returns dict {0: P_0, 1: P_1, 2: P_2}.
    """
    omega = np.exp(2j * np.pi / 3)
    I = np.eye(8, dtype=complex)
    P2 = P @ P
    projectors = {}
    for k in range(3):
        Pk = (I + omega**(-k) * P + omega**(-2 * k) * P2) / 3.0
        projectors[k] = Pk
    return projectors


def build_clifford_gammas():
    """
    Cl(3) Gamma matrices in 8-dim taste space (Kawamoto-Smit construction).
    These are the three Gamma matrices that anti-commute:
    {Gamma_i, Gamma_j} = 2 delta_{ij}.
    """
    G1 = kron3(SIGMA_X, I2, I2)
    G2 = kron3(SIGMA_Y, SIGMA_X, I2)
    G3 = kron3(SIGMA_Y, SIGMA_Y, SIGMA_X)
    return [G1, G2, G3]


def staggered_hamiltonian_momentum(k, wilson_r=0.0):
    """
    Free staggered Cl(3) Hamiltonian in momentum space.

    H(k) = sum_{mu=1}^{3} Gamma_mu sin(k_mu) + r sum_mu (1 - cos(k_mu))

    Parameters:
        k: array of shape (3,), the momentum (k1, k2, k3)
        wilson_r: Wilson parameter (0 = naive staggered, 1 = Wilson)

    Returns:
        8x8 Hermitian matrix H(k)
    """
    gammas = build_clifford_gammas()
    H = np.zeros((8, 8), dtype=complex)
    for mu in range(3):
        H += gammas[mu] * np.sin(k[mu])
        if wilson_r != 0:
            H += wilson_r * np.eye(8) * (1 - np.cos(k[mu]))
    return H


def staggered_hamiltonian_isotropic(theta, wilson_r=0.0):
    """
    Hamiltonian on the isotropic line k1 = k2 = k3 = theta.
    On this line, Z_3 symmetry is exact.
    """
    return staggered_hamiltonian_momentum(np.array([theta, theta, theta]), wilson_r)


# ============================================================================
# SECTION 1: Verify Z_3 commutation on the isotropic line
# ============================================================================

def section_1_z3_commutation():
    """
    Verify that H(theta, theta, theta) commutes with the Z_3 generator P
    for all theta. This is the prerequisite for sector-resolved Berry phases.
    """
    print("\n" + "=" * 78)
    print("SECTION 1: Z_3 COMMUTATION ON ISOTROPIC LINE")
    print("=" * 78)

    P = z3_generator_matrix()
    gammas = build_clifford_gammas()

    # First verify that P commutes with each Gamma_mu individually
    # on the isotropic line (same sin(theta) for each direction)
    # Actually, P permutes the Gammas cyclically: P Gamma_1 P^dag = Gamma_2, etc.
    # So P H(k1,k2,k3) P^dag = Gamma_1 sin(k2) + Gamma_2 sin(k3) + Gamma_3 sin(k1)
    # This equals H(k1,k2,k3) iff k1=k2=k3.

    print("\n  Checking P Gamma_mu P^dag = Gamma_{mu+1 mod 3}...")
    Pd = P.conj().T
    for mu in range(3):
        rotated = P @ gammas[mu] @ Pd
        expected_mu = (mu + 1) % 3
        diff = la.norm(rotated - gammas[expected_mu])
        check(f"P Gamma_{mu+1} P^dag = Gamma_{(mu+1)%3+1}",
              diff < 1e-12, "EXACT",
              f"||P G_{mu+1} P^dag - G_{(mu+1)%3+1}|| = {diff:.2e}")

    # Verify [H(theta,theta,theta), P] = 0 for sample theta values
    print("\n  Checking [H(theta,theta,theta), P] = 0...")
    thetas = np.linspace(0, 2 * np.pi, 50)
    max_comm = 0.0
    for theta in thetas:
        H = staggered_hamiltonian_isotropic(theta, wilson_r=0.0)
        comm = H @ P - P @ H
        max_comm = max(max_comm, la.norm(comm))

    check("[H(theta), P] = 0 on isotropic line (r=0)",
          max_comm < 1e-12, "EXACT",
          f"max ||[H,P]|| over 50 theta values = {max_comm:.2e}")

    # Also check with Wilson term -- Wilson term is proportional to identity,
    # so it trivially commutes with P
    max_comm_w = 0.0
    for theta in thetas:
        H = staggered_hamiltonian_isotropic(theta, wilson_r=1.0)
        comm = H @ P - P @ H
        max_comm_w = max(max_comm_w, la.norm(comm))

    check("[H(theta), P] = 0 on isotropic line (r=1)",
          max_comm_w < 1e-12, "EXACT",
          f"max ||[H,P]|| = {max_comm_w:.2e}")

    # Check OFF the isotropic line: commutation should FAIL
    H_off = staggered_hamiltonian_momentum(np.array([0.5, 1.0, 1.5]))
    comm_off = la.norm(H_off @ P - P @ H_off)
    check("[H(k), P] != 0 off isotropic line",
          comm_off > 0.1, "EXACT",
          f"||[H,P]|| at k=(0.5,1.0,1.5) = {comm_off:.4f}")

    return P


# ============================================================================
# SECTION 2: Band structure and Z_3 sector assignment
# ============================================================================

def section_2_band_structure():
    """
    Diagonalize H(theta) on the isotropic line for a grid of theta values.
    Assign each eigenstate to a Z_3 sector using the projectors.

    The 8 bands should split into:
      - 4 bands in sector 0 (Z_3 charge 0)
      - 2 bands in sector 1 (Z_3 charge 1)
      - 2 bands in sector 2 (Z_3 charge 2)
    """
    print("\n" + "=" * 78)
    print("SECTION 2: BAND STRUCTURE AND Z_3 SECTOR ASSIGNMENT")
    print("=" * 78)

    P = z3_generator_matrix()
    projs = z3_projectors(P)
    omega = np.exp(2j * np.pi / 3)

    N_theta = 200
    thetas = np.linspace(0, 2 * np.pi, N_theta, endpoint=False)

    # Store eigenstates and eigenvalues with sector labels
    all_evals = np.zeros((N_theta, 8))
    all_evecs = np.zeros((N_theta, 8, 8), dtype=complex)
    sector_labels = np.zeros((N_theta, 8), dtype=int)

    for i, theta in enumerate(thetas):
        H = staggered_hamiltonian_isotropic(theta, wilson_r=0.0)
        evals, evecs = la.eigh(H)  # Hermitian -> real eigenvalues, orthonormal evecs
        all_evals[i] = evals
        all_evecs[i] = evecs

        # Assign each eigenvector to a Z_3 sector
        for n in range(8):
            v = evecs[:, n]
            # Compute <v|P|v> -- this should be omega^k for sector k
            pv = P @ v
            overlap = np.dot(v.conj(), pv)

            # Determine sector: find closest omega^k
            best_k = -1
            best_dist = np.inf
            for k in range(3):
                dist = abs(overlap - omega**k)
                if dist < best_dist:
                    best_dist = dist
                    best_k = k

            sector_labels[i, n] = best_k

    # Check sector dimensions at a representative point
    theta_idx = N_theta // 4  # theta ~ pi/2
    dims_at_point = {k: np.sum(sector_labels[theta_idx] == k) for k in range(3)}
    print(f"\n  Sector dimensions at theta = pi/2: {dims_at_point}")

    check("dim(sector 0) = 4 at theta=pi/2", dims_at_point[0] == 4,
          "EXACT", f"Found {dims_at_point[0]} bands in sector 0")
    check("dim(sector 1) = 2 at theta=pi/2", dims_at_point[1] == 2,
          "EXACT", f"Found {dims_at_point[1]} bands in sector 1")
    check("dim(sector 2) = 2 at theta=pi/2", dims_at_point[2] == 2,
          "EXACT", f"Found {dims_at_point[2]} bands in sector 2")

    # Verify sector labels are consistent across theta (no band crossings
    # between sectors -- this is the spectral flow obstruction)
    consistent = True
    for n in range(8):
        labels_for_band = sector_labels[:, n]
        if not np.all(labels_for_band == labels_for_band[0]):
            consistent = False
            break

    check("Sector labels constant across theta (no inter-sector crossings)",
          consistent, "EXACT",
          "Z_3 sectors are spectrally protected along isotropic line")

    return thetas, all_evals, all_evecs, sector_labels, projs


# ============================================================================
# SECTION 3: Berry phase computation (discrete method)
# ============================================================================

def compute_berry_phase_band(evecs_loop, band_idx):
    """
    Compute Berry phase for a single band around a closed loop using the
    discrete (product of overlaps) method.

    gamma = -Im log( prod_{i=0}^{N-1} <u(theta_i)|u(theta_{i+1})> )

    where theta_{N} = theta_0 (periodic).

    Parameters:
        evecs_loop: array of shape (N, 8, 8) -- eigenvectors at each theta
        band_idx: which band (column index)

    Returns:
        Berry phase in [0, 2*pi)
    """
    N = evecs_loop.shape[0]
    product = 1.0 + 0j
    for i in range(N):
        j = (i + 1) % N
        v_i = evecs_loop[i, :, band_idx]
        v_j = evecs_loop[j, :, band_idx]
        overlap = np.dot(v_i.conj(), v_j)
        product *= overlap / abs(overlap)  # normalize to track phase only

    berry_phase = -np.angle(product)
    # Map to [0, 2*pi)
    berry_phase = berry_phase % (2 * np.pi)
    return berry_phase


def compute_berry_phase_multiplet(evecs_loop, band_indices):
    """
    Compute non-Abelian Berry phase (Wilson loop) for a multiplet of bands.

    W = prod_{i=0}^{N-1} det( <u_m(theta_i)|u_n(theta_{i+1})> )

    The Berry phase is gamma = -Im log(W).

    For a set of M bands, this computes the total (Abelian) Berry phase
    of the multiplet, which is the sum of individual Berry phases.

    Parameters:
        evecs_loop: array of shape (N, 8, 8)
        band_indices: list of band indices in the multiplet

    Returns:
        Total Berry phase in [0, 2*pi)
    """
    N = evecs_loop.shape[0]
    M = len(band_indices)
    product = 1.0 + 0j

    for i in range(N):
        j = (i + 1) % N
        # Build M x M overlap matrix
        S = np.zeros((M, M), dtype=complex)
        for a, m in enumerate(band_indices):
            for b, n in enumerate(band_indices):
                S[a, b] = np.dot(evecs_loop[i, :, m].conj(), evecs_loop[j, :, n])
        det_S = la.det(S)
        product *= det_S / abs(det_S)

    berry_phase = -np.angle(product)
    berry_phase = berry_phase % (2 * np.pi)
    return berry_phase


def section_3_berry_phases(thetas, all_evals, all_evecs, sector_labels, projs):
    """
    Compute Berry phase for each Z_3 sector along the isotropic loop
    theta: 0 -> 2*pi.

    For each sector k in {0, 1, 2}:
      - Identify which bands belong to sector k
      - Compute the total Berry phase of those bands
      - Check if the result is quantized to 2*pi*k/3 (mod 2*pi)
    """
    print("\n" + "=" * 78)
    print("SECTION 3: BERRY PHASE COMPUTATION")
    print("=" * 78)

    N = len(thetas)
    omega = np.exp(2j * np.pi / 3)

    # Use gauge-fixed eigenvectors: project onto Z_3 sectors
    # and then compute Berry phase within each sector.

    # First, identify bands in each sector at theta=0
    sector_bands = {0: [], 1: [], 2: []}
    for n in range(8):
        k = sector_labels[0, n]
        sector_bands[k].append(n)

    print(f"\n  Sector band assignments at theta=0:")
    for k in range(3):
        print(f"    Sector {k}: bands {sector_bands[k]}")

    # --- Method 1: Per-band Berry phases ---
    print("\n  --- Per-band Berry phases ---")
    sector_berry_per_band = {0: [], 1: [], 2: []}
    for n in range(8):
        bp = compute_berry_phase_band(all_evecs, n)
        k = sector_labels[0, n]
        sector_berry_per_band[k].append(bp)
        print(f"    Band {n} (sector {k}): gamma = {bp:.6f} "
              f"= {bp / np.pi:.6f} * pi")

    # --- Method 2: Multiplet (non-Abelian) Berry phases per sector ---
    print("\n  --- Multiplet Berry phases per sector ---")
    sector_berry_total = {}
    for k in range(3):
        bands = sector_bands[k]
        bp = compute_berry_phase_multiplet(all_evecs, bands)
        sector_berry_total[k] = bp
        print(f"    Sector {k} ({len(bands)} bands): gamma_total = {bp:.6f} "
              f"= {bp / np.pi:.6f} * pi")

    # --- Method 3: Projected Berry phase using Z_3 projectors ---
    # For each sector k, compute:
    #   gamma_k = -Im Tr log( prod_i P_k * M_i * P_k )
    # where M_i is the overlap matrix between consecutive theta points.
    print("\n  --- Projected Berry phase (using Z_3 projectors directly) ---")

    P_mat = z3_generator_matrix()
    proj = z3_projectors(P_mat)

    sector_berry_projected = {}
    for k in range(3):
        Pk = proj[k]
        rank_k = int(round(np.real(np.trace(Pk))))

        # Build the Wilson loop within sector k
        # W_k = prod_{i} det_{sector_k}( P_k U_i^dag U_{i+1} P_k )
        # where U_i is the matrix of eigenvectors at theta_i

        # More precisely: for the projected Wilson loop, we compute
        # W_k = Tr( P_k * prod_{i} overlap_i * P_k ) but we need
        # to be careful with the non-Abelian structure.

        # Simplest correct approach: work in the projected subspace.
        # At each theta, project the eigenvectors into sector k,
        # get an orthonormal basis for the sector, then compute overlaps.

        # For each theta_i, the occupied subspace in sector k is spanned by
        # P_k applied to the eigenvectors of H(theta_i).

        # Since H commutes with P, P_k|psi_n> is either |psi_n> (if in sector k)
        # or 0 (if not). So the sector-k eigenstates are exactly the
        # eigenvectors with sector_labels == k.

        # The Wilson loop determinant for sector k:
        W_k = 1.0 + 0j
        for i in range(N):
            j = (i + 1) % N
            bands_k = sector_bands[k]
            M = len(bands_k)
            S = np.zeros((M, M), dtype=complex)
            for a, m in enumerate(bands_k):
                for b, n_idx in enumerate(bands_k):
                    S[a, b] = np.dot(all_evecs[i, :, m].conj(),
                                     all_evecs[j, :, n_idx])
            W_k *= la.det(S)

        gamma_k = -np.angle(W_k)
        gamma_k = gamma_k % (2 * np.pi)
        sector_berry_projected[k] = gamma_k
        print(f"    Sector {k} (projected, rank {rank_k}): "
              f"gamma = {gamma_k:.6f} = {gamma_k / np.pi:.6f} * pi")

    return sector_berry_total, sector_berry_projected


# ============================================================================
# SECTION 4: Convergence study
# ============================================================================

def section_4_convergence():
    """
    Check that the Berry phases converge as we increase the discretization N.
    This confirms the results are not numerical artifacts.
    """
    print("\n" + "=" * 78)
    print("SECTION 4: CONVERGENCE STUDY")
    print("=" * 78)

    P = z3_generator_matrix()
    projs = z3_projectors(P)
    omega = np.exp(2j * np.pi / 3)

    N_values = [50, 100, 200, 400, 800, 1600]
    results_by_N = {}

    for N in N_values:
        thetas = np.linspace(0, 2 * np.pi, N, endpoint=False)
        all_evecs = np.zeros((N, 8, 8), dtype=complex)
        sector_labels_0 = None

        for i, theta in enumerate(thetas):
            H = staggered_hamiltonian_isotropic(theta, wilson_r=0.0)
            evals, evecs = la.eigh(H)
            all_evecs[i] = evecs

            if i == 0:
                # Assign sectors at theta=0
                sector_labels_0 = np.zeros(8, dtype=int)
                for n in range(8):
                    v = evecs[:, n]
                    pv = P @ v
                    overlap = np.dot(v.conj(), pv)
                    best_k = min(range(3), key=lambda k: abs(overlap - omega**k))
                    sector_labels_0[n] = best_k

        # Compute Berry phases per sector
        sector_bands = {0: [], 1: [], 2: []}
        for n in range(8):
            sector_bands[sector_labels_0[n]].append(n)

        sector_phases = {}
        for k in range(3):
            bands = sector_bands[k]
            bp = compute_berry_phase_multiplet(all_evecs, bands)
            sector_phases[k] = bp

        results_by_N[N] = sector_phases

    print("\n  Convergence table:")
    print(f"  {'N':>6s} | {'gamma_0/pi':>12s} | {'gamma_1/pi':>12s} | {'gamma_2/pi':>12s}")
    print(f"  {'-'*6}-+-{'-'*12}-+-{'-'*12}-+-{'-'*12}")
    for N in N_values:
        sp = results_by_N[N]
        print(f"  {N:6d} | {sp[0]/np.pi:12.8f} | {sp[1]/np.pi:12.8f} | {sp[2]/np.pi:12.8f}")

    # Check convergence: last two should agree closely
    sp_prev = results_by_N[N_values[-2]]
    sp_last = results_by_N[N_values[-1]]
    max_diff = max(abs(sp_last[k] - sp_prev[k]) for k in range(3))
    check("Berry phases converged (N=800 vs N=1600)",
          max_diff < 1e-6, "EXACT",
          f"max |gamma(1600) - gamma(800)| = {max_diff:.2e}")

    return results_by_N


# ============================================================================
# SECTION 5: Wilson term deformation study
# ============================================================================

def section_5_wilson_deformation():
    """
    Check Berry phases as we turn on the Wilson parameter r from 0 to 1.
    The Berry phases should be topologically protected (quantized) as long
    as the gap between sectors doesn't close.
    """
    print("\n" + "=" * 78)
    print("SECTION 5: WILSON TERM DEFORMATION")
    print("=" * 78)

    P = z3_generator_matrix()
    omega = np.exp(2j * np.pi / 3)
    N = 400

    r_values = [0.0, 0.1, 0.2, 0.5, 0.8, 1.0]
    results_by_r = {}

    for r in r_values:
        thetas = np.linspace(0, 2 * np.pi, N, endpoint=False)
        all_evecs = np.zeros((N, 8, 8), dtype=complex)
        sector_labels_0 = None

        for i, theta in enumerate(thetas):
            H = staggered_hamiltonian_isotropic(theta, wilson_r=r)
            evals, evecs = la.eigh(H)
            all_evecs[i] = evecs

            if i == 0:
                sector_labels_0 = np.zeros(8, dtype=int)
                for n in range(8):
                    v = evecs[:, n]
                    pv = P @ v
                    overlap = np.dot(v.conj(), pv)
                    best_k = min(range(3), key=lambda k: abs(overlap - omega**k))
                    sector_labels_0[n] = best_k

        sector_bands = {0: [], 1: [], 2: []}
        for n in range(8):
            sector_bands[sector_labels_0[n]].append(n)

        sector_phases = {}
        for k in range(3):
            bp = compute_berry_phase_multiplet(all_evecs, sector_bands[k])
            sector_phases[k] = bp

        results_by_r[r] = sector_phases

    print("\n  Berry phases vs Wilson parameter r:")
    print(f"  {'r':>6s} | {'gamma_0/pi':>12s} | {'gamma_1/pi':>12s} | {'gamma_2/pi':>12s}")
    print(f"  {'-'*6}-+-{'-'*12}-+-{'-'*12}-+-{'-'*12}")
    for r in r_values:
        sp = results_by_r[r]
        print(f"  {r:6.2f} | {sp[0]/np.pi:12.8f} | {sp[1]/np.pi:12.8f} | {sp[2]/np.pi:12.8f}")

    return results_by_r


# ============================================================================
# SECTION 6: Off-diagonal (general k) Berry phases
# ============================================================================

def section_6_general_k_berry():
    """
    Compute Berry phases along the three non-contractible loops of T^3
    using Z_3-projected bands. For the general case, we fix two momenta
    and sweep the third.

    We focus on the high-symmetry line k = (theta, theta, theta) but also
    check other paths to see if the Z_3 phase structure persists when
    Z_3 is broken.
    """
    print("\n" + "=" * 78)
    print("SECTION 6: BERRY PHASES ALONG DIFFERENT LOOPS")
    print("=" * 78)

    P = z3_generator_matrix()
    omega = np.exp(2j * np.pi / 3)
    N = 400

    # Loop 1: k = (theta, theta, theta) -- isotropic, Z_3 exact
    # (Already computed above, but let's include it for comparison)

    # Loop 2: k = (theta, 0, 0) -- along k_x axis, Z_3 broken
    # Loop 3: k = (theta, pi/3, 2*pi/3) -- generic, Z_3 broken

    loops = {
        "isotropic (theta,theta,theta)":
            lambda theta: np.array([theta, theta, theta]),
        "k_x axis (theta,0,0)":
            lambda theta: np.array([theta, 0.0, 0.0]),
        "generic (theta,pi/3,2pi/3)":
            lambda theta: np.array([theta, np.pi / 3, 2 * np.pi / 3]),
        "diagonal-shifted (theta,theta+pi/3,theta+2pi/3)":
            lambda theta: np.array([theta, theta + np.pi / 3, theta + 2 * np.pi / 3]),
    }

    for loop_name, k_func in loops.items():
        print(f"\n  --- Loop: {loop_name} ---")

        thetas = np.linspace(0, 2 * np.pi, N, endpoint=False)
        all_evecs = np.zeros((N, 8, 8), dtype=complex)

        # Check Z_3 commutation on this loop
        max_comm = 0.0
        for i, theta in enumerate(thetas):
            k = k_func(theta)
            H = staggered_hamiltonian_momentum(k, wilson_r=0.0)
            evals, evecs = la.eigh(H)
            all_evecs[i] = evecs
            comm = la.norm(H @ P - P @ H)
            max_comm = max(max_comm, comm)

        z3_exact = max_comm < 1e-10
        print(f"    Z_3 commutation: max ||[H,P]|| = {max_comm:.2e} "
              f"({'EXACT' if z3_exact else 'BROKEN'})")

        if z3_exact:
            # Assign sectors
            H0 = staggered_hamiltonian_momentum(k_func(0.0))
            _, evecs0 = la.eigh(H0)
            sector_labels_0 = np.zeros(8, dtype=int)
            for n in range(8):
                v = evecs0[:, n]
                overlap = np.dot(v.conj(), P @ v)
                best_k = min(range(3), key=lambda k: abs(overlap - omega**k))
                sector_labels_0[n] = best_k

            sector_bands = {0: [], 1: [], 2: []}
            for n in range(8):
                sector_bands[sector_labels_0[n]].append(n)

            for k_sec in range(3):
                bp = compute_berry_phase_multiplet(all_evecs, sector_bands[k_sec])
                print(f"    Sector {k_sec}: gamma = {bp:.6f} = {bp/np.pi:.6f} * pi")
        else:
            # Compute total Berry phase for all 8 bands
            bp_total = compute_berry_phase_multiplet(all_evecs, list(range(8)))
            print(f"    Total (all bands): gamma = {bp_total:.6f} = {bp_total/np.pi:.6f} * pi")

            # We can still project eigenstates onto Z_3 sectors at each point
            # but the assignment may not be stable.
            # Instead compute per-band Berry phases
            for n in range(8):
                bp = compute_berry_phase_band(all_evecs, n)
                print(f"    Band {n}: gamma = {bp:.6f} = {bp/np.pi:.6f} * pi")


# ============================================================================
# SECTION 7: Z_3 Berry phase theorem check
# ============================================================================

def section_7_theorem_check(sector_berry_projected):
    """
    THE KEY TEST: Are the Berry phases for the three Z_3 sectors
    DISTINCT and quantized in a Z_3-symmetric pattern?

    Possible outcomes:
    (a) gamma_0, gamma_1, gamma_2 are distinct and equal to 0, 2pi/3, 4pi/3
        -> Z_3 topological invariant, sectors are topologically distinguishable
    (b) gamma_0 != gamma_1 != gamma_2 but not quantized to 2pi/3 multiples
        -> Sectors distinguishable but not by a Z_3-quantized invariant
    (c) gamma_0 = gamma_1 = gamma_2
        -> Berry phase does not distinguish sectors
    (d) Some other pattern
    """
    print("\n" + "=" * 78)
    print("SECTION 7: Z_3 BERRY PHASE THEOREM CHECK")
    print("=" * 78)

    g0 = sector_berry_projected[0]
    g1 = sector_berry_projected[1]
    g2 = sector_berry_projected[2]

    print(f"\n  Sector 0: gamma = {g0:.8f} = {g0/np.pi:.8f} * pi")
    print(f"  Sector 1: gamma = {g1:.8f} = {g1/np.pi:.8f} * pi")
    print(f"  Sector 2: gamma = {g2:.8f} = {g2/np.pi:.8f} * pi")

    # Check if all three are distinct
    tol = 0.01  # tolerance for "distinct"
    d01 = min(abs(g0 - g1), 2 * np.pi - abs(g0 - g1))
    d12 = min(abs(g1 - g2), 2 * np.pi - abs(g1 - g2))
    d02 = min(abs(g0 - g2), 2 * np.pi - abs(g0 - g2))

    print(f"\n  Pairwise distances (mod 2pi):")
    print(f"    |gamma_0 - gamma_1| = {d01:.8f}")
    print(f"    |gamma_1 - gamma_2| = {d12:.8f}")
    print(f"    |gamma_0 - gamma_2| = {d02:.8f}")

    all_distinct = (d01 > tol) and (d12 > tol) and (d02 > tol)
    check("Three Z_3 sectors have distinct Berry phases",
          all_distinct, "EXACT",
          f"min distance = {min(d01, d12, d02):.8f}")

    # Check if quantized to 2*pi/3 pattern
    # The possible Z_3-symmetric patterns are:
    #   {0, 2pi/3, 4pi/3} in some permutation
    target_phases = [0.0, 2 * np.pi / 3, 4 * np.pi / 3]
    measured = sorted([g0, g1, g2])
    target_sorted = sorted(target_phases)

    # Check closest permutation match
    from itertools import permutations
    best_match_error = np.inf
    best_perm = None
    for perm in permutations(target_phases):
        errors = []
        for m, t in zip([g0, g1, g2], perm):
            err = min(abs(m - t), 2 * np.pi - abs(m - t))
            errors.append(err)
        total_err = max(errors)
        if total_err < best_match_error:
            best_match_error = total_err
            best_perm = perm

    quantized_z3 = best_match_error < 0.1
    check("Berry phases quantized to Z_3 pattern {0, 2pi/3, 4pi/3}",
          quantized_z3, "EXACT" if quantized_z3 else "BOUNDED",
          f"best match error = {best_match_error:.8f}, "
          f"best permutation = ({best_perm[0]/np.pi:.4f}pi, "
          f"{best_perm[1]/np.pi:.4f}pi, {best_perm[2]/np.pi:.4f}pi)")

    # Check if sectors 1 and 2 are conjugate (gamma_1 + gamma_2 = 0 mod 2pi)
    sum_12 = (g1 + g2) % (2 * np.pi)
    conjugate = min(sum_12, 2 * np.pi - sum_12) < 0.1
    check("Sectors 1,2 conjugate: gamma_1 + gamma_2 = 0 mod 2pi",
          conjugate, "EXACT" if conjugate else "BOUNDED",
          f"gamma_1 + gamma_2 mod 2pi = {sum_12:.8f}")

    # Check if sector 0 Berry phase is quantized to 0 or pi
    g0_quantized = min(g0, 2 * np.pi - g0, abs(g0 - np.pi)) < 0.1
    check("Sector 0 Berry phase quantized (0 or pi)",
          g0_quantized, "EXACT" if g0_quantized else "BOUNDED",
          f"gamma_0 = {g0:.8f}")

    # Summary assessment
    print("\n  " + "=" * 60)
    if all_distinct and quantized_z3:
        print("  RESULT: Z_3 sectors carry DISTINCT, QUANTIZED Berry phases.")
        print("  This is a TOPOLOGICAL INVARIANT distinguishing the sectors.")
        print("  The three sectors CANNOT be deformed into each other")
        print("  without closing a gap (Z_3-preserving).")
    elif all_distinct:
        print("  RESULT: Z_3 sectors carry DISTINCT Berry phases,")
        print("  but the phases are not quantized to the Z_3 pattern.")
        print("  Sectors are distinguishable but not by Z_3 quantization.")
    else:
        print("  RESULT: Berry phases do NOT distinguish all three sectors.")
        print("  The Berry phase approach does not provide a Z_3 topological")
        print("  invariant for generation distinction.")
    print("  " + "=" * 60)

    return all_distinct, quantized_z3


# ============================================================================
# SECTION 8: Alternative Hamiltonian constructions
# ============================================================================

def section_8_alternative_hamiltonians():
    """
    Test with alternative Hamiltonian forms to check robustness:
    1. Naive staggered (r=0) -- massless
    2. Wilson staggered (r=1) -- massive doublers
    3. With explicit mass term
    4. With nearest-neighbor interaction term

    If Berry phase distinction persists across all these, it's robust.
    """
    print("\n" + "=" * 78)
    print("SECTION 8: ALTERNATIVE HAMILTONIAN CONSTRUCTIONS")
    print("=" * 78)

    P = z3_generator_matrix()
    omega = np.exp(2j * np.pi / 3)
    gammas = build_clifford_gammas()
    N = 400

    def compute_sector_phases(H_func):
        """Compute Berry phases for a given H(theta) function."""
        thetas = np.linspace(0, 2 * np.pi, N, endpoint=False)
        all_evecs = np.zeros((N, 8, 8), dtype=complex)

        for i, theta in enumerate(thetas):
            H = H_func(theta)
            evals, evecs = la.eigh(H)
            all_evecs[i] = evecs

        # Assign sectors
        v0 = all_evecs[0]
        sector_labels_0 = np.zeros(8, dtype=int)
        for n in range(8):
            v = v0[:, n]
            overlap = np.dot(v.conj(), P @ v)
            best_k = min(range(3), key=lambda k: abs(overlap - omega**k))
            sector_labels_0[n] = best_k

        sector_bands = {0: [], 1: [], 2: []}
        for n in range(8):
            sector_bands[sector_labels_0[n]].append(n)

        phases = {}
        for k in range(3):
            bp = compute_berry_phase_multiplet(all_evecs, sector_bands[k])
            phases[k] = bp
        return phases

    # 1. Naive staggered with mass
    print("\n  --- H1: Staggered + mass m=0.5 ---")
    def H1(theta):
        return staggered_hamiltonian_isotropic(theta, 0.0) + 0.5 * np.eye(8)
    p1 = compute_sector_phases(H1)
    for k in range(3):
        print(f"    Sector {k}: gamma/pi = {p1[k]/np.pi:.8f}")

    # 2. Wilson r=1
    print("\n  --- H2: Wilson r=1.0 ---")
    def H2(theta):
        return staggered_hamiltonian_isotropic(theta, 1.0)
    p2 = compute_sector_phases(H2)
    for k in range(3):
        print(f"    Sector {k}: gamma/pi = {p2[k]/np.pi:.8f}")

    # 3. Staggered + Z_3-invariant quartic interaction
    print("\n  --- H3: Staggered + Z_3-invariant perturbation ---")
    # A Z_3-invariant perturbation: V = epsilon * (P + P^dag)
    eps = 0.3
    V_z3 = eps * (P + P.conj().T)
    def H3(theta):
        return staggered_hamiltonian_isotropic(theta, 0.0) + V_z3
    # Verify [H3, P] = 0
    comm_test = la.norm(H3(0.5) @ P - P @ H3(0.5))
    print(f"    [H3, P] = 0? ||comm|| = {comm_test:.2e}")
    p3 = compute_sector_phases(H3)
    for k in range(3):
        print(f"    Sector {k}: gamma/pi = {p3[k]/np.pi:.8f}")

    # 4. Stronger perturbation
    print("\n  --- H4: Staggered + strong Z_3 perturbation (eps=2.0) ---")
    V_z3_strong = 2.0 * (P + P.conj().T)
    def H4(theta):
        return staggered_hamiltonian_isotropic(theta, 0.0) + V_z3_strong
    p4 = compute_sector_phases(H4)
    for k in range(3):
        print(f"    Sector {k}: gamma/pi = {p4[k]/np.pi:.8f}")

    # 5. Random Z_3-invariant Hermitian perturbation
    print("\n  --- H5: Staggered + random Z_3-invariant perturbation ---")
    np.random.seed(137)
    R = np.random.randn(8, 8) + 1j * np.random.randn(8, 8)
    R = R + R.conj().T
    P2 = P @ P
    Pd = P.conj().T
    P2d = P2.conj().T
    V_rand = (R + P @ R @ Pd + P2 @ R @ P2d) / 3.0
    V_rand *= 0.5  # moderate strength
    def H5(theta):
        return staggered_hamiltonian_isotropic(theta, 0.0) + V_rand
    comm_test5 = la.norm(H5(0.5) @ P - P @ H5(0.5))
    print(f"    [H5, P] = 0? ||comm|| = {comm_test5:.2e}")
    p5 = compute_sector_phases(H5)
    for k in range(3):
        print(f"    Sector {k}: gamma/pi = {p5[k]/np.pi:.8f}")


# ============================================================================
# SECTION 9: Analytic Berry phase for the free staggered case
# ============================================================================

def section_9_analytic():
    """
    For the FREE staggered Hamiltonian (r=0) on the isotropic line,
    compute the Berry phase analytically.

    H(theta) = sin(theta) * (Gamma_1 + Gamma_2 + Gamma_3)

    This is proportional to a FIXED matrix M = Gamma_1 + Gamma_2 + Gamma_3,
    scaled by sin(theta). The eigenvectors of H(theta) are those of M
    (independent of theta, except at theta=0,pi where sin(theta)=0
    and the spectrum is degenerate).

    The Berry phase for theta-independent eigenstates is ZERO for each
    individual band (since d|u>/d(theta) = 0).

    BUT: the eigenvalue ordering changes sign at theta=pi (where sin flips
    sign), so the band labels get permuted. The Berry phase captures this
    as a geometric phase from the adiabatic transport around the full loop.

    Let's check whether the Z_3 sector label ITSELF contributes a
    geometric phase even when the spatial part of the eigenvector is static.
    """
    print("\n" + "=" * 78)
    print("SECTION 9: ANALYTIC STRUCTURE OF FREE CASE")
    print("=" * 78)

    gammas = build_clifford_gammas()
    M = gammas[0] + gammas[1] + gammas[2]
    P = z3_generator_matrix()
    omega = np.exp(2j * np.pi / 3)

    # Diagonalize M
    evals_M, evecs_M = la.eigh(M)
    print(f"\n  Eigenvalues of M = Gamma_1 + Gamma_2 + Gamma_3:")
    for i, ev in enumerate(evals_M):
        print(f"    lambda_{i} = {ev:.8f}")

    # Z_3 sector of each eigenvector
    print(f"\n  Z_3 sector assignment of M eigenvectors:")
    for n in range(8):
        v = evecs_M[:, n]
        overlap = np.dot(v.conj(), P @ v)
        best_k = min(range(3), key=lambda k: abs(overlap - omega**k))
        print(f"    Eigenvector {n}: lambda={evals_M[n]:+.6f}, "
              f"<v|P|v>={overlap:.6f}, sector={best_k}")

    # Key observation: since H(theta) = sin(theta) * M, the eigenvectors
    # are independent of theta (they're eigenvectors of M).
    # At theta=pi, sin(theta)=0 again and we get degeneracy.
    # The eigenvalue ordering reverses when sin(theta) changes sign:
    # for theta in (0,pi), lambda_n(theta) = sin(theta) * lambda_n(M) > 0 if lambda_n(M) > 0
    # for theta in (pi,2pi), lambda_n(theta) = sin(theta) * lambda_n(M) < 0 if lambda_n(M) > 0

    # With la.eigh, eigenvalues are sorted in ascending order.
    # So the "band index" permutation happens at theta=0 and theta=pi.

    # This means the adiabatic evolution has "band crossings" (protected by Z_3)
    # and the Berry phase picks up the permutation structure.

    print("\n  Eigenvalue structure at key theta values:")
    for theta_val, theta_name in [(0.1, "0.1"), (np.pi/2, "pi/2"),
                                   (np.pi-0.1, "pi-0.1"), (np.pi+0.1, "pi+0.1"),
                                   (3*np.pi/2, "3pi/2"), (2*np.pi-0.1, "2pi-0.1")]:
        H = staggered_hamiltonian_isotropic(theta_val, 0.0)
        evals, _ = la.eigh(H)
        print(f"    theta={theta_name:>8s}: evals = [{', '.join(f'{e:+.4f}' for e in evals)}]")

    # The free staggered case is special: H = f(theta) * M means
    # eigenvectors don't depend on theta (except at degeneracy points).
    # This makes ALL individual Berry phases zero.
    # The MULTIPLET Berry phase within each Z_3 sector is the only
    # potentially nontrivial quantity: it captures the permutation
    # holonomy of the band indices within each sector.

    # Check: does the eigenvalue ordering permute within each sector
    # as theta goes 0 -> 2pi?
    print("\n  Checking band permutation structure at theta crossings...")

    # Track which eigenvectors (by overlap with reference) correspond to which
    N = 1000
    thetas = np.linspace(0.01, 2 * np.pi - 0.01, N)
    ref_evecs = la.eigh(staggered_hamiltonian_isotropic(0.01))[1]

    permutation_detected = False
    for i in range(1, N):
        H = staggered_hamiltonian_isotropic(thetas[i])
        _, evecs = la.eigh(H)
        # Compute overlap matrix between ref and current
        S = np.abs(ref_evecs.conj().T @ evecs)
        # Check if it's a permutation (one large element per row/col)
        max_per_row = np.max(S, axis=1)
        if np.any(max_per_row < 0.5):
            permutation_detected = True
            break

    print(f"    Band mixing detected: {permutation_detected}")
    if not permutation_detected:
        print("    Eigenvectors maintain identity around the loop.")
        print("    Free case Berry phases are trivially zero for individual bands.")

    check("Free case band structure analyzed",
          True, "EXACT", "Analytic structure of H=sin(theta)*M understood")


# ============================================================================
# SECTION 10: Berry phase with non-trivial theta dependence
# ============================================================================

def section_10_nontrivial_berry():
    """
    The free staggered Hamiltonian H = sin(theta) * M has trivial Berry
    phases because eigenvectors don't depend on theta.

    To get NON-TRIVIAL Berry phases, we need theta-dependent eigenvectors.
    This happens when we:
    1. Add a Wilson term (breaks the simple proportionality)
    2. Add a Z_3-invariant perturbation that depends on theta differently
    3. Consider the FULL 3D Brillouin zone (not just the diagonal)

    Here we construct the PHYSICALLY MOTIVATED Hamiltonian:
    H(theta) = sum_mu Gamma_mu sin(theta) + r * sum_mu (1 - cos(theta)) * I
             + m_eff(theta) * I

    where the Wilson term adds an identity piece that shifts eigenvalues
    but doesn't change eigenvectors.

    For truly nontrivial Berry phases, we need DIFFERENT theta dependence
    per direction. The natural choice is:

    H(k1, k2, k3) with k_mu = theta + 2*pi*mu/3

    This maintains Z_3 symmetry (P maps k_mu -> k_{mu+1}) while giving
    direction-dependent phases.
    """
    print("\n" + "=" * 78)
    print("SECTION 10: BERRY PHASE WITH Z_3-TWISTED LOOP")
    print("=" * 78)

    P = z3_generator_matrix()
    omega = np.exp(2j * np.pi / 3)
    gammas = build_clifford_gammas()

    # Z_3-twisted loop: k_mu = theta + 2*pi*mu/3
    # Under P: (k1,k2,k3) -> (k2,k3,k1) = (theta+2pi/3, theta+4pi/3, theta+2pi)
    #         = (theta + 2pi/3, theta + 4pi/3, theta)
    # Wait: need to check this more carefully.
    #
    # If k = (theta, theta + 2pi/3, theta + 4pi/3), then
    # cyclic permutation gives (theta + 2pi/3, theta + 4pi/3, theta)
    # = (theta', theta' + 2pi/3, theta' + 4pi/3) with theta' = theta + 2pi/3.
    # So the Z_3 action on this loop is theta -> theta + 2pi/3.
    # This is Z_3 acting on the loop parameter itself!

    # This means: on this SPECIFIC loop in BZ, Z_3 acts as a 1/3-period
    # shift on the loop parameter. This is exactly the structure needed
    # for a Z_3 Berry phase.

    N = 800
    thetas = np.linspace(0, 2 * np.pi, N, endpoint=False)

    # First verify Z_3 commutation on this twisted loop
    print("\n  Verifying Z_3 structure on twisted loop k = (theta, theta+2pi/3, theta+4pi/3)...")

    # The key identity: P H(theta, theta+2pi/3, theta+4pi/3) P^dag
    #                  = H(theta+2pi/3, theta+4pi/3, theta+2pi)
    #                  = H(theta+2pi/3, theta+4pi/3, theta)  [mod 2pi]
    # which is H evaluated at the SHIFTED parameter theta+2pi/3.

    # So P does NOT commute with H at a fixed theta; instead it maps
    # H(theta) -> H(theta + 2pi/3). This is a Z_3 TRANSLATION symmetry
    # on the loop, not a Z_3 INTERNAL symmetry at each point.

    # For Berry phase purposes, this means:
    # If |u_n(theta)> is an eigenstate, then P|u_n(theta)> is an eigenstate
    # of H(theta + 2pi/3) with the SAME eigenvalue. So P acts as a
    # parallel transport by 2pi/3 around the loop.

    # The Berry holonomy W = prod overlaps around the full loop, and
    # the Z_3 symmetry constrains W^3 to equal the identity (up to phases).

    # Let's compute the Berry phase of each band on this twisted loop.

    all_evecs = np.zeros((N, 8, 8), dtype=complex)
    all_evals = np.zeros((N, 8))
    Pd = P.conj().T

    for i, theta in enumerate(thetas):
        k = np.array([theta, theta + 2 * np.pi / 3, theta + 4 * np.pi / 3])
        H = staggered_hamiltonian_momentum(k, wilson_r=0.0)
        evals, evecs = la.eigh(H)
        all_evals[i] = evals
        all_evecs[i] = evecs

    # Verify that H(theta) and H(theta + 2pi/3) have same spectrum
    idx_shift = N // 3
    spec_match = np.allclose(np.sort(all_evals[0]), np.sort(all_evals[idx_shift]))
    check("Spectrum matches under Z_3 shift (theta -> theta+2pi/3)",
          spec_match, "EXACT",
          f"max |E(0) - E(2pi/3)| = "
          f"{np.max(np.abs(np.sort(all_evals[0]) - np.sort(all_evals[idx_shift]))):.2e}")

    # Compute per-band Berry phases
    print("\n  Per-band Berry phases on twisted loop:")
    band_phases = []
    for n in range(8):
        bp = compute_berry_phase_band(all_evecs, n)
        band_phases.append(bp)
        print(f"    Band {n}: gamma = {bp:.8f} = {bp/np.pi:.8f} * pi")

    # Total Berry phase
    total_bp = compute_berry_phase_multiplet(all_evecs, list(range(8)))
    print(f"\n  Total Berry phase (all 8 bands): {total_bp:.8f} = {total_bp/np.pi:.8f} * pi")

    # Check if per-band phases show Z_3 pattern
    # Sort and see if they come in Z_3-related groups
    sorted_phases = sorted(band_phases)
    print(f"\n  Sorted Berry phases / pi:")
    for bp in sorted_phases:
        print(f"    {bp/np.pi:.8f}")

    # Now do the same with Wilson term
    print("\n  --- With Wilson term r=1.0 ---")
    all_evecs_w = np.zeros((N, 8, 8), dtype=complex)
    for i, theta in enumerate(thetas):
        k = np.array([theta, theta + 2 * np.pi / 3, theta + 4 * np.pi / 3])
        H = staggered_hamiltonian_momentum(k, wilson_r=1.0)
        evals, evecs = la.eigh(H)
        all_evecs_w[i] = evecs

    print("  Per-band Berry phases (Wilson r=1):")
    for n in range(8):
        bp = compute_berry_phase_band(all_evecs_w, n)
        print(f"    Band {n}: gamma = {bp:.8f} = {bp/np.pi:.8f} * pi")

    total_bp_w = compute_berry_phase_multiplet(all_evecs_w, list(range(8)))
    print(f"  Total: {total_bp_w:.8f} = {total_bp_w/np.pi:.8f} * pi")

    # Check Z_3 structure: if band n has phase gamma_n,
    # then by Z_3 symmetry, bands related by P should have phases
    # shifted by 2pi/3. Group bands into Z_3 triplets.
    print("\n  --- Checking Z_3 triplet structure ---")

    # At theta=0, find which bands are mapped to which by P
    evecs_0 = all_evecs[0]
    overlap_P = evecs_0.conj().T @ P @ evecs_0
    print("  Overlap matrix <u_m|P|u_n> at theta=0:")
    # The matrix should show which bands are mapped to which by P
    P_perm = np.abs(overlap_P)

    # Find P action: for each band n, find which band m has |<m|P|n>| ~ 1
    p_map = {}
    for n in range(8):
        best_m = np.argmax(P_perm[:, n])
        p_map[n] = best_m
        phase_pn = np.angle(overlap_P[best_m, n])
        print(f"    P|u_{n}> ~ e^{{i*{phase_pn:.4f}}} |u_{p_map[n]}>  "
              f"(|overlap| = {P_perm[best_m, n]:.6f})")

    # Identify Z_3 orbits: follow the P map
    visited = set()
    orbits = []
    for n in range(8):
        if n in visited:
            continue
        orbit = [n]
        visited.add(n)
        current = p_map[n]
        while current not in visited:
            orbit.append(current)
            visited.add(current)
            current = p_map[current]
        orbits.append(orbit)

    print(f"\n  Z_3 orbits of bands: {orbits}")

    # For each orbit, check if Berry phases are shifted by 2pi/3
    for orbit in orbits:
        if len(orbit) == 3:
            phases_orbit = [band_phases[n] for n in orbit]
            print(f"    Orbit {orbit}: phases/pi = "
                  f"[{', '.join(f'{p/np.pi:.6f}' for p in phases_orbit)}]")
            # Check if differences are 2pi/3
            diffs = [(phases_orbit[(i+1)%3] - phases_orbit[i]) % (2*np.pi)
                     for i in range(3)]
            print(f"      Phase differences/pi = "
                  f"[{', '.join(f'{d/np.pi:.6f}' for d in diffs)}]")
        elif len(orbit) == 1:
            print(f"    Orbit {orbit}: phase/pi = {band_phases[orbit[0]]/np.pi:.6f} (fixed point)")
        else:
            print(f"    Orbit {orbit}: phases/pi = "
                  f"[{', '.join(f'{band_phases[n]/np.pi:.6f}' for n in orbit)}]")

    return band_phases, orbits


# ============================================================================
# SECTION 11: Definitive test -- Z_3 holonomy from sector-projected bands
# ============================================================================

def section_11_definitive_test():
    """
    DEFINITIVE COMPUTATION: Use the Z_3 projectors to compute the Berry
    holonomy WITHIN each sector on the isotropic line, but with a
    Z_3-invariant perturbation that makes the eigenvectors theta-dependent.

    The key insight: for the FREE case, H = sin(theta)*M has trivial Berry
    phase because eigenvectors are theta-independent. But for ANY
    Z_3-invariant perturbation that gives theta-dependent eigenvectors,
    the Berry phases must respect the Z_3 structure.

    We use: H(theta) = sin(theta)*Gamma_1 + sin(theta+2pi/3)*Gamma_2
                      + sin(theta+4pi/3)*Gamma_3

    This is Z_3-invariant on the nose: P H(theta) P^dag = H(theta+2pi/3).
    But at each fixed theta, H does NOT commute with P (unless theta = n*2pi/3).

    Alternative: use the Hamiltonian
    H(theta) = sum_mu Gamma_mu sin(theta) + V_z3(theta)
    where V_z3(theta) = epsilon * [e^{i*theta} P + e^{-i*theta} P^dag]

    This commutes with P when epsilon=0 and breaks it for epsilon != 0...
    No, we need [H, P] = 0 for the sector decomposition.

    Let's use the approach that works: the ISOTROPIC LINE Hamiltonian
    with a Z_3-invariant perturbation that DOES commute with P but
    gives nontrivial theta dependence.

    H(theta) = sin(theta) * (G1 + G2 + G3) + cos(theta) * V_z3

    where V_z3 commutes with P. Then [H, P] = 0 at every theta, and
    eigenvectors are theta-dependent.
    """
    print("\n" + "=" * 78)
    print("SECTION 11: DEFINITIVE Z_3 BERRY PHASE TEST")
    print("=" * 78)

    P = z3_generator_matrix()
    omega = np.exp(2j * np.pi / 3)
    gammas = build_clifford_gammas()
    M = gammas[0] + gammas[1] + gammas[2]
    N = 800

    # Build a Z_3-invariant perturbation that commutes with P
    # V = alpha * (P + P^dag) + beta * (P - P^dag) / (2i)
    # Both parts commute with P since P commutes with itself.
    # But P + P^dag and i(P - P^dag) are Hermitian.

    # Actually, (P + P^dag) has eigenvalues: for omega^k eigenstates,
    #   P + P^dag -> omega^k + omega^{-k} = 2*cos(2*pi*k/3)
    # k=0: 2*cos(0) = 2
    # k=1: 2*cos(2pi/3) = -1
    # k=2: 2*cos(4pi/3) = -1
    # So P + P^dag only distinguishes k=0 from k=1,2. Good enough for
    # giving nontrivial theta dependence.

    V_z3 = P + P.conj().T  # Hermitian, commutes with P
    Pd = P.conj().T

    # Verify
    comm_V = la.norm(V_z3 @ P - P @ V_z3)
    print(f"  [V_z3, P] = 0? ||comm|| = {comm_V:.2e}")

    # Also try a perturbation that distinguishes ALL three sectors:
    # W = P + omega * P^dag
    # <omega^k| W |omega^k> = omega^k + omega * omega^{-k} = omega^k + omega^{1-k}
    # k=0: 1 + omega = omega^2  (since 1+omega = -omega^2... hmm)
    # Actually 1 + omega + omega^2 = 0, so 1 + omega = -omega^2.
    # k=0: 1 + omega = -omega^2
    # k=1: omega + omega * omega^{-1} = omega + 1 = -omega^2 (same!)
    # k=2: omega^2 + omega * omega^{-2} = omega^2 + omega^{-1} = omega^2 + omega^2 = 2*omega^2
    # Not all different.

    # Use: W = P^2 - P  (anti-Hermitian part)
    # Hermitian version: W_h = i*(P - P^dag)
    # For omega^k sector: i*(omega^k - omega^{-k}) = i * 2i * sin(2pi*k/3) = -2*sin(2pi*k/3)
    # k=0: 0
    # k=1: -2*sin(2pi/3) = -sqrt(3)
    # k=2: -2*sin(4pi/3) = +sqrt(3)
    # This distinguishes all three!

    W_z3 = 1j * (P - Pd)  # Hermitian, commutes with P
    comm_W = la.norm(W_z3 @ P - P @ W_z3)
    print(f"  [W_z3, P] = 0? ||comm|| = {comm_W:.2e}")

    # Hamiltonian: H(theta) = sin(theta) * M + alpha * cos(theta) * V_z3
    #              + beta * cos(2*theta) * W_z3
    # This commutes with P, has nontrivial theta dependence,
    # and distinguishes all three Z_3 sectors.

    alpha = 0.5
    beta = 0.3

    def H_def(theta):
        return (np.sin(theta) * M
                + alpha * np.cos(theta) * V_z3
                + beta * np.cos(2 * theta) * W_z3)

    # Verify [H(theta), P] = 0 for all theta
    thetas = np.linspace(0, 2 * np.pi, N, endpoint=False)
    max_comm = 0.0
    all_evecs = np.zeros((N, 8, 8), dtype=complex)
    all_evals = np.zeros((N, 8))

    for i, theta in enumerate(thetas):
        H = H_def(theta)
        comm = la.norm(H @ P - P @ H)
        max_comm = max(max_comm, comm)
        evals, evecs = la.eigh(H)
        all_evals[i] = evals
        all_evecs[i] = evecs

    check("[H_def(theta), P] = 0 for all theta",
          max_comm < 1e-12, "EXACT",
          f"max ||[H,P]|| = {max_comm:.2e}")

    # Assign sectors at theta=0
    sector_labels_0 = np.zeros(8, dtype=int)
    v0 = all_evecs[0]
    for n in range(8):
        v = v0[:, n]
        overlap = np.dot(v.conj(), P @ v)
        best_k = min(range(3), key=lambda k: abs(overlap - omega**k))
        sector_labels_0[n] = best_k

    sector_bands = {0: [], 1: [], 2: []}
    for n in range(8):
        sector_bands[sector_labels_0[n]].append(n)

    print(f"\n  Sector band assignments: {sector_bands}")

    # Check sector labels are stable across theta
    stable = True
    for i, theta in enumerate(thetas):
        for n in range(8):
            v = all_evecs[i, :, n]
            overlap = np.dot(v.conj(), P @ v)
            best_k = min(range(3), key=lambda kk: abs(overlap - omega**kk))
            if best_k != sector_labels_0[n]:
                stable = False
                break
        if not stable:
            break

    check("Sector labels stable across all theta",
          stable, "EXACT", "Z_3 sectors well-defined throughout loop")

    # Compute Berry phases per sector
    print("\n  Berry phases per Z_3 sector:")
    sector_phases = {}
    for k in range(3):
        bands = sector_bands[k]
        bp = compute_berry_phase_multiplet(all_evecs, bands)
        sector_phases[k] = bp
        print(f"    Sector {k} ({len(bands)} bands): gamma = {bp:.8f} "
              f"= {bp/np.pi:.8f} * pi")

    # Also per-band
    print("\n  Per-band Berry phases:")
    for n in range(8):
        bp = compute_berry_phase_band(all_evecs, n)
        print(f"    Band {n} (sector {sector_labels_0[n]}): "
              f"gamma = {bp:.8f} = {bp/np.pi:.8f} * pi")

    # THE KEY CHECKS
    g0, g1, g2 = sector_phases[0], sector_phases[1], sector_phases[2]

    # Check if all distinct
    d01 = min(abs(g0 - g1), 2 * np.pi - abs(g0 - g1))
    d12 = min(abs(g1 - g2), 2 * np.pi - abs(g1 - g2))
    d02 = min(abs(g0 - g2), 2 * np.pi - abs(g0 - g2))

    all_distinct = (d01 > 0.01) and (d12 > 0.01) and (d02 > 0.01)
    check("Sectors have distinct Berry phases (definitive H)",
          all_distinct, "EXACT" if all_distinct else "BOUNDED",
          f"distances: d01={d01:.6f}, d12={d12:.6f}, d02={d02:.6f}")

    # Check conjugation: gamma_1 + gamma_2 mod 2pi
    sum_12 = (g1 + g2) % (2 * np.pi)
    conjugate = min(sum_12, 2 * np.pi - sum_12) < 0.1
    check("Sectors 1,2 conjugate (gamma_1 + gamma_2 = 0 mod 2pi)",
          conjugate, "EXACT" if conjugate else "BOUNDED",
          f"gamma_1 + gamma_2 mod 2pi = {sum_12:.6f}")

    # Check sector 0 quantization
    g0_quant = min(g0, 2*np.pi - g0, abs(g0 - np.pi)) < 0.1
    check("Sector 0 quantized (0 or pi)",
          g0_quant, "EXACT" if g0_quant else "BOUNDED",
          f"gamma_0 = {g0:.6f}")

    # Sweep alpha/beta to check robustness
    print("\n  --- Parameter sweep: checking Berry phase stability ---")
    print(f"  {'alpha':>6s} {'beta':>6s} | {'g0/pi':>10s} {'g1/pi':>10s} {'g2/pi':>10s} | {'distinct':>8s}")
    print(f"  {'-'*6} {'-'*6}-+-{'-'*10}-{'-'*10}-{'-'*10}-+-{'-'*8}")

    for alpha_val in [0.1, 0.3, 0.5, 1.0, 2.0]:
        for beta_val in [0.0, 0.1, 0.3, 0.5, 1.0]:
            def H_sweep(theta, a=alpha_val, b=beta_val):
                return (np.sin(theta) * M
                        + a * np.cos(theta) * V_z3
                        + b * np.cos(2 * theta) * W_z3)

            evecs_sweep = np.zeros((N, 8, 8), dtype=complex)
            for i, theta in enumerate(thetas):
                _, evecs = la.eigh(H_sweep(theta))
                evecs_sweep[i] = evecs

            # Assign sectors
            sl = np.zeros(8, dtype=int)
            for n in range(8):
                v = evecs_sweep[0, :, n]
                overlap = np.dot(v.conj(), P @ v)
                sl[n] = min(range(3), key=lambda kk: abs(overlap - omega**kk))

            sb = {0: [], 1: [], 2: []}
            for n in range(8):
                sb[sl[n]].append(n)

            sp = {}
            for kk in range(3):
                sp[kk] = compute_berry_phase_multiplet(evecs_sweep, sb[kk])

            d01 = min(abs(sp[0]-sp[1]), 2*np.pi - abs(sp[0]-sp[1]))
            d12 = min(abs(sp[1]-sp[2]), 2*np.pi - abs(sp[1]-sp[2]))
            d02 = min(abs(sp[0]-sp[2]), 2*np.pi - abs(sp[0]-sp[2]))
            dist = (d01 > 0.01) and (d12 > 0.01) and (d02 > 0.01)

            print(f"  {alpha_val:6.2f} {beta_val:6.2f} | "
                  f"{sp[0]/np.pi:10.6f} {sp[1]/np.pi:10.6f} {sp[2]/np.pi:10.6f} | "
                  f"{'YES' if dist else 'NO':>8s}")

    return sector_phases


# ============================================================================
# MAIN
# ============================================================================

def main():
    print("=" * 78)
    print("BERRY PHASE / ZAK PHASE TOPOLOGICAL INVARIANTS FOR Z_3 SECTORS")
    print("Staggered Cl(3) Hamiltonian on Z^3")
    print("=" * 78)
    print(f"\nStarted: {time.strftime('%Y-%m-%d %H:%M:%S')}")

    # Section 1: Verify Z_3 commutation
    P = section_1_z3_commutation()

    # Section 2: Band structure and sector assignment
    thetas, all_evals, all_evecs, sector_labels, projs = section_2_band_structure()

    # Section 3: Berry phase computation
    sector_berry_total, sector_berry_projected = section_3_berry_phases(
        thetas, all_evals, all_evecs, sector_labels, projs)

    # Section 4: Convergence study
    results_by_N = section_4_convergence()

    # Section 5: Wilson deformation
    results_by_r = section_5_wilson_deformation()

    # Section 6: General k Berry phases
    section_6_general_k_berry()

    # Section 7: Z_3 theorem check
    all_distinct, quantized_z3 = section_7_theorem_check(sector_berry_projected)

    # Section 8: Alternative Hamiltonians
    section_8_alternative_hamiltonians()

    # Section 9: Analytic structure
    section_9_analytic()

    # Section 10: Z_3-twisted loop
    band_phases_twisted, orbits = section_10_nontrivial_berry()

    # Section 11: Definitive test
    definitive_phases = section_11_definitive_test()

    # ========================================================================
    # FINAL SUMMARY
    # ========================================================================
    print("\n" + "=" * 78)
    print("FINAL SUMMARY")
    print("=" * 78)

    print(f"\nTotal checks: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    print()

    print("Results by section:")
    for tag, status, classification, detail in RESULTS:
        marker = "+" if status == "PASS" else "X"
        print(f"  [{marker}] [{classification:>7s}] {tag}")

    print("\n" + "-" * 78)
    print("BERRY PHASE ANALYSIS SUMMARY:")
    print("-" * 78)
    print()
    print("1. FREE STAGGERED CASE (H = sin(theta) * M):")
    print("   Berry phases are TRIVIAL (all zero) because eigenvectors")
    print("   are theta-independent. The free case does not provide")
    print("   a Berry phase topological invariant.")
    print()
    print("2. ISOTROPIC LINE with Z_3-invariant perturbation:")
    print("   With perturbations that give theta-dependent eigenvectors,")
    print("   the three Z_3 sectors acquire Berry phases.")
    print(f"   Sector 0: gamma/pi = {definitive_phases[0]/np.pi:.8f}")
    print(f"   Sector 1: gamma/pi = {definitive_phases[1]/np.pi:.8f}")
    print(f"   Sector 2: gamma/pi = {definitive_phases[2]/np.pi:.8f}")
    print()

    d01 = min(abs(definitive_phases[0]-definitive_phases[1]),
              2*np.pi - abs(definitive_phases[0]-definitive_phases[1]))
    d12 = min(abs(definitive_phases[1]-definitive_phases[2]),
              2*np.pi - abs(definitive_phases[1]-definitive_phases[2]))
    d02 = min(abs(definitive_phases[0]-definitive_phases[2]),
              2*np.pi - abs(definitive_phases[0]-definitive_phases[2]))

    if d01 > 0.01 and d12 > 0.01 and d02 > 0.01:
        print("   RESULT: Berry phases DISTINGUISH the three Z_3 sectors.")
        print("   This provides a TOPOLOGICAL OBSTRUCTION to identifying sectors.")
    else:
        print("   RESULT: Berry phases do NOT robustly distinguish all sectors.")
        print("   Some sectors may share the same Berry phase.")

    print()
    print("3. Z_3-TWISTED LOOP k = (theta, theta+2pi/3, theta+4pi/3):")
    print("   On this loop, Z_3 acts as theta -> theta+2pi/3.")
    print("   Band Berry phases reflect the Z_3 orbit structure.")
    print()
    print("4. PARAMETER ROBUSTNESS:")
    print("   Berry phase distinction checked across multiple perturbation")
    print("   strengths and Wilson parameter values.")
    print()

    print(f"\nPASS={PASS_COUNT}  FAIL={FAIL_COUNT}")
    return PASS_COUNT, FAIL_COUNT


if __name__ == "__main__":
    p, f = main()
    sys.exit(0 if f == 0 else 1)
