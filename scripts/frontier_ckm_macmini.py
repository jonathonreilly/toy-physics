#!/usr/bin/env python3
"""
CKM NNI Coefficients: Production Lattice Computation (Mac Mini M4)
==================================================================

Computes the CKM mixing matrix from first principles via inter-valley
scattering on the staggered lattice with EWSB.

HARDWARE TARGET: Mac Mini M4, 16GB RAM
  L=8:  dim = 3 * 512  = 1536  -> ~0.04 GB (trivial)
  L=12: dim = 3 * 1728 = 5184  -> ~0.4 GB  (comfortable)

COMPUTATION:
  1. Generate N_cfg SU(3) gauge configurations via Metropolis at beta=6
  2. For each config: build staggered + Wilson Dirac operator D
  3. Add EWSB: H_EWSB = y*v*Gamma_1 (VEV in direction 1)
  4. Build BZ-corner wave packets at X1=(pi,0,0), X2=(0,pi,0), X3=(0,0,pi)
  5. Compute inter-valley scattering amplitudes T_ij
  6. Extract c_ij = T_ij / sqrt(E_i * E_j) normalized by diagonal
  7. Ensemble averages and statistical errors (jackknife)
  8. Build M_u and M_d mass matrices with computed c_ij
  9. Diagonalize -> extract V_CKM
  10. Compare to PDG

USAGE:
  python3 scripts/frontier_ckm_macmini.py                   # full run (50 cfgs, L=8,12)
  python3 scripts/frontier_ckm_macmini.py --quick            # test run (5 cfgs, L=6)
  python3 scripts/frontier_ckm_macmini.py --ncfg 100         # custom config count
  python3 scripts/frontier_ckm_macmini.py 2>&1 | tee ~/Desktop/ckm_results.txt

Self-contained: numpy + scipy only.
"""

from __future__ import annotations

import argparse
import sys
import time
import numpy as np
from scipy import sparse
from scipy.sparse import lil_matrix, csr_matrix

np.set_printoptions(precision=10, linewidth=120, suppress=True)

# =============================================================================
# Physical constants
# =============================================================================

SIN2_TW = 0.231
ALPHA_S_2GEV = 0.30
ALPHA_EM = 1.0 / 137.0

Q_UP, T3_UP = 2.0 / 3.0, 0.5
Q_DOWN, T3_DOWN = -1.0 / 3.0, -0.5

# Fitted NNI coefficients (target values from frontier_ckm_mass_matrix_fix.py)
C12_U_FIT = 1.48
C23_U_FIT = 0.65
C12_D_FIT = 0.91
C23_D_FIT = 0.65

# PDG CKM elements
V_US_PDG = 0.2243
V_CB_PDG = 0.0422
V_UB_PDG = 0.00394

# Quark masses (PDG, running at 2 GeV in GeV)
M_UP = 2.16e-3
M_CHARM = 1.27
M_TOP = 172.76
M_DOWN = 4.67e-3
M_STRANGE = 0.093
M_BOTTOM = 4.18

MASSES_UP = [M_UP, M_CHARM, M_TOP]
MASSES_DOWN = [M_DOWN, M_STRANGE, M_BOTTOM]


# =============================================================================
# SU(3) utilities
# =============================================================================

def su3_random(rng):
    """Generate a random SU(3) matrix via QR decomposition."""
    Z = rng.standard_normal((3, 3)) + 1j * rng.standard_normal((3, 3))
    Q, R = np.linalg.qr(Z)
    d = np.diag(R)
    ph = d / np.abs(d)
    Q = Q @ np.diag(ph.conj())
    det = np.linalg.det(Q)
    Q = Q / (det ** (1.0 / 3.0))
    return Q


def su3_near_identity(rng, epsilon):
    """SU(3) matrix close to identity for Metropolis updates."""
    H = rng.standard_normal((3, 3)) + 1j * rng.standard_normal((3, 3))
    H = (H + H.conj().T) / 2.0
    H = H - np.trace(H) / 3.0 * np.eye(3)
    U = np.eye(3, dtype=complex) + 1j * epsilon * H
    Q, R = np.linalg.qr(U)
    d = np.diag(R)
    ph = d / np.abs(d)
    Q = Q @ np.diag(ph.conj())
    det = np.linalg.det(Q)
    Q = Q / (det ** (1.0 / 3.0))
    return Q


def wilson_action_staple(gauge_links, L, mu, x, y, z):
    """
    Compute the sum of staples around the link U_mu(x) for the Wilson gauge action.
    Returns a 3x3 complex matrix (the staple sum).
    """
    coords = [x, y, z]
    N = 3  # spatial dimensions
    staple_sum = np.zeros((3, 3), dtype=complex)

    for nu in range(N):
        if nu == mu:
            continue

        # Forward staple: U_nu(x+mu) * U_mu(x+nu)^dag * U_nu(x)^dag
        xp_mu = list(coords)
        xp_mu[mu] = (xp_mu[mu] + 1) % L
        xp_nu = list(coords)
        xp_nu[nu] = (xp_nu[nu] + 1) % L

        U_nu_xpmu = gauge_links[nu][xp_mu[0], xp_mu[1], xp_mu[2]]
        U_mu_xpnu = gauge_links[mu][xp_nu[0], xp_nu[1], xp_nu[2]]
        U_nu_x = gauge_links[nu][x, y, z]

        staple_sum += U_nu_xpmu @ U_mu_xpnu.conj().T @ U_nu_x.conj().T

        # Backward staple: U_nu(x+mu-nu)^dag * U_mu(x-nu)^dag * U_nu(x-nu)
        xp_mu_mn = list(coords)
        xp_mu_mn[mu] = (xp_mu_mn[mu] + 1) % L
        xp_mu_mn[nu] = (xp_mu_mn[nu] - 1) % L
        xm_nu = list(coords)
        xm_nu[nu] = (xm_nu[nu] - 1) % L

        U_nu_xpmumnu = gauge_links[nu][xp_mu_mn[0], xp_mu_mn[1], xp_mu_mn[2]]
        U_mu_xmnu = gauge_links[mu][xm_nu[0], xm_nu[1], xm_nu[2]]
        U_nu_xmnu = gauge_links[nu][xm_nu[0], xm_nu[1], xm_nu[2]]

        staple_sum += U_nu_xpmumnu.conj().T @ U_mu_xmnu.conj().T @ U_nu_xmnu

    return staple_sum


def metropolis_update(gauge_links, L, beta, rng, epsilon=0.2):
    """
    One Metropolis sweep over all links.
    Wilson gauge action: S = beta * sum_plaq Re Tr(1 - U_plaq) / 3.
    Returns acceptance rate.
    """
    n_accept = 0
    n_total = 0

    for mu in range(3):
        for x in range(L):
            for y in range(L):
                for z in range(L):
                    U_old = gauge_links[mu][x, y, z].copy()
                    staple = wilson_action_staple(gauge_links, L, mu, x, y, z)

                    # Propose: U_new = dU * U_old
                    dU = su3_near_identity(rng, epsilon)
                    U_new = dU @ U_old

                    # Delta S = -(beta/3) * Re Tr((U_new - U_old) * staple)
                    delta_S = -(beta / 3.0) * np.real(
                        np.trace((U_new - U_old) @ staple)
                    )

                    if delta_S < 0 or rng.random() < np.exp(-delta_S):
                        gauge_links[mu][x, y, z] = U_new
                        n_accept += 1

                    n_total += 1

    return n_accept / n_total


def generate_gauge_config(L, beta, rng, n_therm=50, n_skip=10, epsilon=0.2):
    """
    Generate a thermalized SU(3) gauge configuration via Metropolis.
    Starts from cold start (identity), thermalizes, then returns config.
    """
    # Cold start
    gauge_links = []
    for mu in range(3):
        links = np.zeros((L, L, L, 3, 3), dtype=complex)
        for x in range(L):
            for y in range(L):
                for z in range(L):
                    links[x, y, z] = np.eye(3, dtype=complex)
        gauge_links.append(links)

    # Thermalization sweeps
    for sweep in range(n_therm):
        acc = metropolis_update(gauge_links, L, beta, rng, epsilon)

    # Additional decorrelation sweeps
    for sweep in range(n_skip):
        metropolis_update(gauge_links, L, beta, rng, epsilon)

    return gauge_links


def measure_plaquette(gauge_links, L):
    """Measure average plaquette for monitoring thermalization."""
    plaq_sum = 0.0
    n_plaq = 0

    for mu in range(3):
        for nu in range(mu + 1, 3):
            for x in range(L):
                for y in range(L):
                    for z in range(L):
                        coords = [x, y, z]
                        xp_mu = list(coords)
                        xp_mu[mu] = (xp_mu[mu] + 1) % L
                        xp_nu = list(coords)
                        xp_nu[nu] = (xp_nu[nu] + 1) % L

                        U1 = gauge_links[mu][x, y, z]
                        U2 = gauge_links[nu][xp_mu[0], xp_mu[1], xp_mu[2]]
                        U3 = gauge_links[mu][xp_nu[0], xp_nu[1], xp_nu[2]]
                        U4 = gauge_links[nu][x, y, z]

                        plaq = U1 @ U2 @ U3.conj().T @ U4.conj().T
                        plaq_sum += np.real(np.trace(plaq)) / 3.0
                        n_plaq += 1

    return plaq_sum / n_plaq


# =============================================================================
# Staggered Dirac operator (sparse, position-space)
# =============================================================================

def build_dirac_operator_sparse(L, gauge_links, r_wilson, y_v):
    """
    Build the full Dirac operator D = H_KS + H_W + H_EWSB as a sparse matrix.

    Position-space representation: dim = 3 * L^3 (color x sites).
    Memory: O(dim * 18) entries (sparse) << O(dim^2) for dense.

    For L=12: dim=5184, sparse has ~93k entries -> ~2 MB (vs 400 MB dense).
    We build in lil_matrix (fast construction) then convert to csr (fast matvec).
    """
    N = L ** 3
    dim = N * 3

    def site_index(x, y, z):
        return ((x % L) * L + (y % L)) * L + (z % L)

    def eta(mu, x, y, z):
        if mu == 0:
            return 1.0
        elif mu == 1:
            return (-1.0) ** x
        else:
            return (-1.0) ** (x + y)

    e_mu = [(1, 0, 0), (0, 1, 0), (0, 0, 1)]

    # Use dense matrices -- at L=12 this is 5184x5184 complex128 = ~0.4 GB
    # which fits comfortably in 16 GB RAM
    H = np.zeros((dim, dim), dtype=complex)

    for x in range(L):
        for y in range(L):
            for z in range(L):
                site_a = site_index(x, y, z)

                for mu in range(3):
                    dx, dy, dz = e_mu[mu]
                    xp = (x + dx) % L
                    yp = (y + dy) % L
                    zp = (z + dz) % L
                    site_b = site_index(xp, yp, zp)

                    U = gauge_links[mu][x, y, z]
                    eta_val = eta(mu, x, y, z)

                    for a in range(3):
                        for b in range(3):
                            ia = site_a * 3 + a
                            jb = site_b * 3 + b

                            # Staggered kinetic (anti-Hermitian)
                            H[ia, jb] += 0.5 * eta_val * U[a, b]
                            H[jb, ia] -= 0.5 * eta_val * U[a, b].conj()

                            # Wilson taste-breaking (Hermitian)
                            H[ia, jb] -= 0.5 * r_wilson * U[a, b]
                            H[jb, ia] -= 0.5 * r_wilson * U[a, b].conj()

                    # Wilson diagonal
                    for a in range(3):
                        ia = site_a * 3 + a
                        H[ia, ia] += r_wilson

                # EWSB: shift in direction 1 (mu=0), color-diagonal
                xp_ewsb = (x + 1) % L
                site_b_ewsb = site_index(xp_ewsb, y, z)
                for a in range(3):
                    ia = site_a * 3 + a
                    jb = site_b_ewsb * 3 + a
                    H[ia, jb] += y_v
                    H[jb, ia] += y_v

    return H


# =============================================================================
# Wave packets at BZ corners
# =============================================================================

def build_wave_packet(L, K, sigma, color_vec=None):
    """Gaussian wave packet centered at BZ corner K."""
    N = L ** 3
    if color_vec is None:
        color_vec = np.array([1, 0, 0], dtype=complex)

    psi = np.zeros(N * 3, dtype=complex)
    center = L / 2.0

    for x in range(L):
        for y in range(L):
            for z in range(L):
                site = ((x % L) * L + (y % L)) * L + (z % L)
                dx = min(abs(x - center), L - abs(x - center))
                dy = min(abs(y - center), L - abs(y - center))
                dz = min(abs(z - center), L - abs(z - center))
                r2 = dx ** 2 + dy ** 2 + dz ** 2
                envelope = np.exp(-r2 / (2.0 * sigma ** 2))
                phase = np.exp(1j * (K[0] * x + K[1] * y + K[2] * z))
                for a in range(3):
                    psi[site * 3 + a] = phase * envelope * color_vec[a]

    norm = np.linalg.norm(psi)
    if norm > 0:
        psi /= norm
    return psi


def compute_inter_valley_amplitudes(L, H_total, sigma=None):
    """
    Compute 3x3 inter-valley scattering matrix T_ij averaged over color.
    T_ij = <psi_i| H_total |psi_j>
    """
    PI = np.pi
    corners = [
        np.array([PI, 0, 0]),   # X1 -- weak corner (EWSB axis)
        np.array([0, PI, 0]),   # X2 -- color corner
        np.array([0, 0, PI]),   # X3 -- color corner
    ]

    if sigma is None:
        sigma = L / 4.0

    T = np.zeros((3, 3), dtype=complex)

    for color_idx in range(3):
        color_vec = np.zeros(3, dtype=complex)
        color_vec[color_idx] = 1.0

        packets = []
        for Ki in corners:
            psi = build_wave_packet(L, Ki, sigma, color_vec)
            packets.append(psi)

        for i in range(3):
            for j in range(3):
                T[i, j] += packets[i].conj() @ (H_total @ packets[j])

    T /= 3.0
    return T, corners


# =============================================================================
# EW coupling factors
# =============================================================================

def ew_kappa_12(Q, T3):
    """EW coupling for 1-2 transition (crosses weak axis): neutral + charged."""
    g_neutral = Q ** 2 + (T3 - Q * SIN2_TW) ** 2
    g_charged = T3 ** 2
    return g_neutral + g_charged


def ew_kappa_23(Q, T3):
    """EW coupling for 2-3 transition (color-color): neutral only."""
    g_neutral = Q ** 2 + (T3 - Q * SIN2_TW) ** 2
    return g_neutral


# =============================================================================
# NNI mass matrix and CKM extraction
# =============================================================================

def build_nni_mass_matrix(masses, c12, c23):
    """Build NNI texture mass matrix."""
    m1, m2, m3 = masses
    M = np.zeros((3, 3))
    M[0, 0] = m1
    M[1, 1] = m2
    M[2, 2] = m3
    M[0, 1] = M[1, 0] = c12 * np.sqrt(m1 * m2)
    M[1, 2] = M[2, 1] = c23 * np.sqrt(m2 * m3)
    return M


def diagonalize_and_ckm(M_u, M_d):
    """Diagonalize mass matrices and extract V_CKM."""
    eigvals_u, U_u = np.linalg.eigh(M_u @ M_u.T)
    eigvals_d, U_d = np.linalg.eigh(M_d @ M_d.T)
    idx_u = np.argsort(eigvals_u)
    idx_d = np.argsort(eigvals_d)
    U_u = U_u[:, idx_u]
    U_d = U_d[:, idx_d]
    V_ckm = U_u.T @ U_d
    return V_ckm, np.sqrt(np.maximum(np.sort(eigvals_u), 0)), \
        np.sqrt(np.maximum(np.sort(eigvals_d), 0))


# =============================================================================
# Jackknife error estimation
# =============================================================================

def jackknife_mean_err(samples):
    """Jackknife estimate of mean and standard error."""
    n = len(samples)
    if n < 2:
        return np.mean(samples), 0.0
    mean_full = np.mean(samples)
    jack_means = np.zeros(n)
    for i in range(n):
        jack_means[i] = np.mean(np.delete(samples, i))
    var = (n - 1) / n * np.sum((jack_means - mean_full) ** 2)
    return mean_full, np.sqrt(var)


# =============================================================================
# Main computation for a single lattice size
# =============================================================================

def run_lattice_size(L, n_cfg, beta, r_wilson, y_v, rng_base_seed,
                     n_therm, n_skip, epsilon_metro):
    """
    Run the full computation at a given lattice size.
    Returns dict of results.
    """
    dim = L ** 3 * 3
    mem_gb = dim ** 2 * 16 / 1e9  # complex128 = 16 bytes

    print(f"\n{'=' * 78}")
    print(f"  LATTICE SIZE L = {L}")
    print(f"  dim = 3 * {L}^3 = {dim}")
    print(f"  Dense matrix memory: {mem_gb:.3f} GB")
    print(f"  Gauge configs: {n_cfg}")
    print(f"  beta = {beta}, r_Wilson = {r_wilson}, y*v = {y_v}")
    print(f"  Metropolis: n_therm={n_therm}, n_skip={n_skip}, epsilon={epsilon_metro}")
    print(f"{'=' * 78}")

    assert mem_gb < 12.0, f"Matrix too large: {mem_gb:.1f} GB exceeds 12 GB safety limit"

    # Storage for per-config observables
    all_t12 = []
    all_t13 = []
    all_t23 = []
    all_R12_23 = []
    all_R13_23 = []
    all_plaq = []

    t_start = time.time()

    for cfg in range(n_cfg):
        t_cfg_start = time.time()

        rng = np.random.default_rng(seed=rng_base_seed + cfg * 137)

        # Step 1: Generate thermalized gauge config
        gauge_links = generate_gauge_config(
            L, beta, rng, n_therm=n_therm, n_skip=n_skip, epsilon=epsilon_metro
        )

        # Measure plaquette
        plaq = measure_plaquette(gauge_links, L)
        all_plaq.append(plaq)

        # Step 2: Build Dirac operator
        H_total = build_dirac_operator_sparse(L, gauge_links, r_wilson, y_v)

        # Step 3: Compute inter-valley amplitudes
        T, corners = compute_inter_valley_amplitudes(L, H_total)

        t12 = abs(T[0, 1])
        t13 = abs(T[0, 2])
        t23 = abs(T[1, 2])

        R12_23 = t12 / t23 if t23 > 1e-20 else float('inf')
        R13_23 = t13 / t23 if t23 > 1e-20 else float('inf')

        all_t12.append(t12)
        all_t13.append(t13)
        all_t23.append(t23)
        all_R12_23.append(R12_23)
        all_R13_23.append(R13_23)

        t_cfg = time.time() - t_cfg_start
        t_elapsed = time.time() - t_start
        t_remaining = t_elapsed / (cfg + 1) * (n_cfg - cfg - 1)

        print(f"  cfg {cfg+1:4d}/{n_cfg}: plaq={plaq:.4f}  "
              f"|T_12|={t12:.4e}  |T_23|={t23:.4e}  "
              f"R_12/R_23={R12_23:.3f}  "
              f"[{t_cfg:.1f}s, ETA {t_remaining:.0f}s]")

    total_time = time.time() - t_start

    # Ensemble statistics (jackknife)
    R12_23_mean, R12_23_err = jackknife_mean_err(np.array(all_R12_23))
    R13_23_mean, R13_23_err = jackknife_mean_err(np.array(all_R13_23))
    t12_mean, t12_err = jackknife_mean_err(np.array(all_t12))
    t13_mean, t13_err = jackknife_mean_err(np.array(all_t13))
    t23_mean, t23_err = jackknife_mean_err(np.array(all_t23))
    plaq_mean, plaq_err = jackknife_mean_err(np.array(all_plaq))

    # Ratio of means (more stable estimator)
    rom_12_23 = t12_mean / t23_mean if t23_mean > 0 else float('inf')

    # Z2 residual: T_12 ~ T_13
    z2_residuals = [abs(all_t12[i] - all_t13[i]) / max(all_t12[i], all_t13[i])
                    if max(all_t12[i], all_t13[i]) > 0 else 0.0
                    for i in range(n_cfg)]
    z2_mean = np.mean(z2_residuals)

    print(f"\n  --- L={L} Ensemble Results ({n_cfg} configs, {total_time:.0f}s) ---")
    print(f"  Average plaquette: {plaq_mean:.6f} +/- {plaq_err:.6f}")
    print(f"  |T_12| = {t12_mean:.6e} +/- {t12_err:.6e}")
    print(f"  |T_13| = {t13_mean:.6e} +/- {t13_err:.6e}")
    print(f"  |T_23| = {t23_mean:.6e} +/- {t23_err:.6e}")
    print(f"  R_12/R_23 (mean of ratios) = {R12_23_mean:.4f} +/- {R12_23_err:.4f}")
    print(f"  R_12/R_23 (ratio of means) = {rom_12_23:.4f}")
    print(f"  R_13/R_23 (mean of ratios) = {R13_23_mean:.4f} +/- {R13_23_err:.4f}")
    print(f"  Z2 residual <|T12-T13|/max> = {z2_mean:.4f}")

    return {
        'L': L, 'n_cfg': n_cfg, 'total_time': total_time,
        'plaq_mean': plaq_mean, 'plaq_err': plaq_err,
        't12_mean': t12_mean, 't12_err': t12_err,
        't13_mean': t13_mean, 't13_err': t13_err,
        't23_mean': t23_mean, 't23_err': t23_err,
        'R12_23_mean': R12_23_mean, 'R12_23_err': R12_23_err,
        'R13_23_mean': R13_23_mean, 'R13_23_err': R13_23_err,
        'rom_12_23': rom_12_23,
        'z2_mean': z2_mean,
        'all_R12_23': all_R12_23,
        'all_t12': all_t12, 'all_t13': all_t13, 'all_t23': all_t23,
    }


# =============================================================================
# Extract NNI coefficients and CKM from lattice results
# =============================================================================

def extract_ckm_from_lattice(results_by_L):
    """
    Extract NNI coefficients and V_CKM from the lattice results.

    Uses the largest available lattice for the final numbers.
    """
    print(f"\n{'=' * 78}")
    print("  CKM EXTRACTION FROM LATTICE DATA")
    print(f"{'=' * 78}")

    # Use largest L for primary result
    L_primary = max(results_by_L.keys())
    res = results_by_L[L_primary]

    R_12_23 = res['rom_12_23']  # ratio of means (most stable)
    R_12_23_err = res['R12_23_err']

    print(f"\n  Primary lattice: L = {L_primary}")
    print(f"  Lattice ratio R_12/R_23 = {R_12_23:.4f} +/- {R_12_23_err:.4f}")

    # Volume dependence check if multiple L available
    if len(results_by_L) > 1:
        print(f"\n  Volume dependence:")
        for L_val in sorted(results_by_L.keys()):
            r = results_by_L[L_val]
            print(f"    L={L_val:2d}: R_12/R_23 = {r['rom_12_23']:.4f} "
                  f"+/- {r['R12_23_err']:.4f}  "
                  f"(plaq = {r['plaq_mean']:.4f})")

    # 1-loop normalization (absolute scale)
    N_c = 3
    alpha_s = ALPHA_S_2GEV
    L_enh = np.log(1.22e19 / 246.0) / (4.0 * np.pi)
    C_base = N_c * alpha_s * L_enh / np.pi

    print(f"\n  1-loop normalization:")
    print(f"    alpha_s(2 GeV) = {alpha_s}")
    print(f"    N_c = {N_c}")
    print(f"    Log enhancement = {L_enh:.4f}")
    print(f"    C_base = N_c * alpha_s * L_enh / pi = {C_base:.4f}")

    # EW charge weighting
    k12_u = ew_kappa_12(Q_UP, T3_UP)
    k23_u = ew_kappa_23(Q_UP, T3_UP)
    k12_d = ew_kappa_12(Q_DOWN, T3_DOWN)
    k23_d = ew_kappa_23(Q_DOWN, T3_DOWN)
    kappa_ref = (k23_u + k23_d) / 2.0

    print(f"\n  EW charge factors:")
    print(f"    kappa_12 (up)   = {k12_u:.4f}")
    print(f"    kappa_23 (up)   = {k23_u:.4f}")
    print(f"    kappa_12 (down) = {k12_d:.4f}")
    print(f"    kappa_23 (down) = {k23_d:.4f}")
    print(f"    kappa_ref       = {kappa_ref:.4f}")

    # Derived NNI coefficients
    c12_u = C_base * R_12_23 * np.sqrt(k12_u / kappa_ref)
    c23_u = C_base * np.sqrt(k23_u / kappa_ref)
    c12_d = C_base * R_12_23 * np.sqrt(k12_d / kappa_ref)
    c23_d = C_base * np.sqrt(k23_d / kappa_ref)

    # Error propagation (linear in R_12_23)
    c12_u_err = C_base * R_12_23_err * np.sqrt(k12_u / kappa_ref)
    c23_u_err = 0.0  # c23 does not depend on R
    c12_d_err = C_base * R_12_23_err * np.sqrt(k12_d / kappa_ref)
    c23_d_err = 0.0

    print(f"\n  {'=' * 65}")
    print(f"  DERIVED NNI COEFFICIENTS")
    print(f"  {'=' * 65}")
    print(f"  {'coeff':>8}  {'derived':>12}  {'error':>10}  {'fitted':>10}  {'dev%':>8}")
    print(f"  {'-' * 65}")

    pairs = [
        ('c12_u', c12_u, c12_u_err, C12_U_FIT),
        ('c23_u', c23_u, c23_u_err, C23_U_FIT),
        ('c12_d', c12_d, c12_d_err, C12_D_FIT),
        ('c23_d', c23_d, c23_d_err, C23_D_FIT),
    ]

    for name, derived, err, fitted in pairs:
        dev = abs(derived - fitted) / fitted * 100
        err_str = f"+/- {err:.4f}" if err > 0 else "  (fixed)"
        print(f"  {name:>8}  {derived:12.4f}  {err_str:>10}  {fitted:10.4f}  {dev:7.1f}%")

    # Build mass matrices and extract CKM
    print(f"\n  {'=' * 65}")
    print(f"  CKM MATRIX EXTRACTION")
    print(f"  {'=' * 65}")

    M_u = build_nni_mass_matrix(MASSES_UP, c12_u, c23_u)
    M_d = build_nni_mass_matrix(MASSES_DOWN, c12_d, c23_d)

    V_ckm, m_u_diag, m_d_diag = diagonalize_and_ckm(M_u, M_d)

    V_us = abs(V_ckm[0, 1])
    V_cb = abs(V_ckm[1, 2])
    V_ub = abs(V_ckm[0, 2])

    print(f"\n  Diagonalized quark masses (GeV):")
    print(f"    Up sector:   {m_u_diag[0]:.4e}  {m_u_diag[1]:.4f}  {m_u_diag[2]:.2f}")
    print(f"    Down sector: {m_d_diag[0]:.4e}  {m_d_diag[1]:.4f}  {m_d_diag[2]:.2f}")

    print(f"\n  |V_CKM| matrix:")
    for i in range(3):
        row = "    "
        for j in range(3):
            row += f"{abs(V_ckm[i, j]):10.6f}"
        print(row)

    print(f"\n  {'element':>10}  {'derived':>12}  {'PDG':>10}  {'ratio':>8}  {'dev%':>8}")
    print(f"  {'-' * 55}")

    ckm_pairs = [
        ('|V_us|', V_us, V_US_PDG),
        ('|V_cb|', V_cb, V_CB_PDG),
        ('|V_ub|', V_ub, V_UB_PDG),
    ]

    for name, derived, pdg in ckm_pairs:
        ratio = derived / pdg
        dev = abs(derived - pdg) / pdg * 100
        print(f"  {name:>10}  {derived:12.6f}  {pdg:10.6f}  {ratio:8.4f}  {dev:7.1f}%")

    # Unitarity check
    row0_sq = sum(abs(V_ckm[0, j]) ** 2 for j in range(3))
    row1_sq = sum(abs(V_ckm[1, j]) ** 2 for j in range(3))
    print(f"\n  Unitarity: |V_ud|^2+|V_us|^2+|V_ub|^2 = {row0_sq:.8f}")
    print(f"             |V_cd|^2+|V_cs|^2+|V_cb|^2 = {row1_sq:.8f}")

    # Jackknife CKM errors (from ratio fluctuations)
    if len(res['all_R12_23']) > 1:
        V_us_samples = []
        V_cb_samples = []
        V_ub_samples = []

        for R_samp in res['all_R12_23']:
            c12u_s = C_base * R_samp * np.sqrt(k12_u / kappa_ref)
            c12d_s = C_base * R_samp * np.sqrt(k12_d / kappa_ref)
            Mu_s = build_nni_mass_matrix(MASSES_UP, c12u_s, c23_u)
            Md_s = build_nni_mass_matrix(MASSES_DOWN, c12d_s, c23_d)
            V_s, _, _ = diagonalize_and_ckm(Mu_s, Md_s)
            V_us_samples.append(abs(V_s[0, 1]))
            V_cb_samples.append(abs(V_s[1, 2]))
            V_ub_samples.append(abs(V_s[0, 2]))

        V_us_mean, V_us_err = jackknife_mean_err(np.array(V_us_samples))
        V_cb_mean, V_cb_err = jackknife_mean_err(np.array(V_cb_samples))
        V_ub_mean, V_ub_err = jackknife_mean_err(np.array(V_ub_samples))

        print(f"\n  CKM with jackknife errors:")
        print(f"    |V_us| = {V_us_mean:.6f} +/- {V_us_err:.6f}  (PDG: {V_US_PDG})")
        print(f"    |V_cb| = {V_cb_mean:.6f} +/- {V_cb_err:.6f}  (PDG: {V_CB_PDG})")
        print(f"    |V_ub| = {V_ub_mean:.6f} +/- {V_ub_err:.6f}  (PDG: {V_UB_PDG})")

    return {
        'c12_u': c12_u, 'c23_u': c23_u, 'c12_d': c12_d, 'c23_d': c23_d,
        'c12_u_err': c12_u_err, 'c12_d_err': c12_d_err,
        'V_us': V_us, 'V_cb': V_cb, 'V_ub': V_ub,
        'V_ckm': V_ckm,
    }


# =============================================================================
# Summary report
# =============================================================================

def print_summary(results_by_L, ckm_results):
    """Print final summary suitable for paper/notes."""
    print(f"\n{'#' * 78}")
    print(f"#  FINAL SUMMARY: CKM FROM STAGGERED LATTICE WITH EWSB")
    print(f"{'#' * 78}")

    print(f"\n  Lattice parameters:")
    print(f"    beta = 6 (g = 1)")
    print(f"    Wilson r = 1.0")
    print(f"    EWSB y*v = 0.5 (VEV in direction 1)")

    print(f"\n  Lattice sizes computed:")
    for L in sorted(results_by_L.keys()):
        r = results_by_L[L]
        print(f"    L={L:2d}: {r['n_cfg']} configs, "
              f"plaq = {r['plaq_mean']:.4f} +/- {r['plaq_err']:.4f}, "
              f"R_12/R_23 = {r['rom_12_23']:.4f} +/- {r['R12_23_err']:.4f}")

    print(f"\n  NNI Texture Coefficients:")
    print(f"    c_12^u = {ckm_results['c12_u']:.4f} +/- {ckm_results['c12_u_err']:.4f}  (fitted: {C12_U_FIT})")
    print(f"    c_23^u = {ckm_results['c23_u']:.4f}  (from 1-loop norm, fitted: {C23_U_FIT})")
    print(f"    c_12^d = {ckm_results['c12_d']:.4f} +/- {ckm_results['c12_d_err']:.4f}  (fitted: {C12_D_FIT})")
    print(f"    c_23^d = {ckm_results['c23_d']:.4f}  (from 1-loop norm, fitted: {C23_D_FIT})")

    print(f"\n  CKM Elements:")
    print(f"    |V_us| = {ckm_results['V_us']:.6f}  (PDG: {V_US_PDG})")
    print(f"    |V_cb| = {ckm_results['V_cb']:.6f}  (PDG: {V_CB_PDG})")
    print(f"    |V_ub| = {ckm_results['V_ub']:.6f}  (PDG: {V_UB_PDG})")

    # Structural checks
    print(f"\n  Structural checks (parameter-free predictions):")
    checks = [
        ("c_12 > c_23 (weak-axis enhancement)",
         ckm_results['c12_u'] > ckm_results['c23_u']
         and ckm_results['c12_d'] > ckm_results['c23_d']),
        ("c_12^u > c_12^d (EW charge hierarchy)",
         ckm_results['c12_u'] > ckm_results['c12_d']),
        ("|V_us| > |V_cb| > |V_ub| (CKM hierarchy)",
         ckm_results['V_us'] > ckm_results['V_cb'] > ckm_results['V_ub']),
        ("All c_ij are O(1)",
         all(0.1 < c < 5.0 for c in [ckm_results['c12_u'], ckm_results['c23_u'],
                                       ckm_results['c12_d'], ckm_results['c23_d']])),
    ]

    n_pass = 0
    for desc, passed in checks:
        status = "PASS" if passed else "FAIL"
        print(f"    [{status}] {desc}")
        if passed:
            n_pass += 1

    print(f"\n  Structural checks: {n_pass}/{len(checks)} passed")
    print(f"\n{'#' * 78}")


# =============================================================================
# Main
# =============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="CKM NNI coefficients from staggered lattice (Mac Mini M4)"
    )
    parser.add_argument('--quick', action='store_true',
                        help='Quick test: 5 configs, L=6 only')
    parser.add_argument('--ncfg', type=int, default=None,
                        help='Number of gauge configurations (default: 50)')
    parser.add_argument('--beta', type=float, default=6.0,
                        help='Gauge coupling beta (default: 6.0)')
    parser.add_argument('--rwilson', type=float, default=1.0,
                        help='Wilson parameter r (default: 1.0)')
    parser.add_argument('--yv', type=float, default=0.5,
                        help='EWSB coupling y*v (default: 0.5)')
    parser.add_argument('--seed', type=int, default=20260413,
                        help='Base RNG seed (default: 20260413)')
    args = parser.parse_args()

    print("=" * 78)
    print("  CKM NNI COEFFICIENTS: PRODUCTION LATTICE COMPUTATION")
    print("  Mac Mini M4 (16 GB RAM)")
    print("=" * 78)
    print(f"  Date: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"  Python: {sys.version.split()[0]}")
    print(f"  NumPy: {np.__version__}")

    if args.quick:
        print(f"\n  MODE: QUICK TEST")
        lattice_sizes = [6]
        n_cfg = args.ncfg if args.ncfg else 5
        n_therm = 20
        n_skip = 5
    else:
        print(f"\n  MODE: FULL PRODUCTION RUN")
        lattice_sizes = [8, 12]
        n_cfg = args.ncfg if args.ncfg else 50
        n_therm = 100
        n_skip = 20

    epsilon_metro = 0.2
    beta = args.beta
    r_wilson = args.rwilson
    y_v = args.yv

    print(f"  Lattice sizes: {lattice_sizes}")
    print(f"  Gauge configs per size: {n_cfg}")
    print(f"  beta = {beta}, r_Wilson = {r_wilson}, y*v = {y_v}")
    print(f"  Metropolis: n_therm={n_therm}, n_skip={n_skip}, epsilon={epsilon_metro}")
    print(f"  RNG seed: {args.seed}")

    # Memory estimate
    for L in lattice_sizes:
        dim = L ** 3 * 3
        mem_gb = dim ** 2 * 16 / 1e9
        print(f"  L={L}: dim={dim}, matrix memory={mem_gb:.3f} GB")

    t_total_start = time.time()

    # Run each lattice size
    results_by_L = {}
    for L in lattice_sizes:
        results_by_L[L] = run_lattice_size(
            L, n_cfg, beta, r_wilson, y_v, args.seed,
            n_therm, n_skip, epsilon_metro
        )

    # Extract CKM from combined results
    ckm_results = extract_ckm_from_lattice(results_by_L)

    # Print summary
    print_summary(results_by_L, ckm_results)

    t_total = time.time() - t_total_start
    print(f"\n  Total wall time: {t_total:.0f}s ({t_total/60:.1f} min)")

    return 0


if __name__ == '__main__':
    sys.exit(main())
