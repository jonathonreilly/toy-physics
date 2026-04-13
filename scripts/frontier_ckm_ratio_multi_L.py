#!/usr/bin/env python3
"""
CKM c_12/c_23 Ratio: Multi-L High-Statistics Measurement
=========================================================

Measures the inter-valley amplitude ratio R = |T_12|/|T_23| across multiple
lattice sizes (L=6,8,10,12) with high statistics to:

  1. Reduce statistical error on R (currently ~20% spread at L=8, 12 configs)
  2. Check L-dependence (should be weak if ratio is physical)
  3. Extrapolate to L -> infinity if there is a trend

PHYSICS:
  The ratio R = |T_12|/|T_23| eliminates the absolute normalization K entirely.
  It measures the EWSB asymmetry between the weak-axis (1-2) and color (2-3)
  inter-valley transitions. On the staggered lattice with EWSB term
  H_EWSB = y*v*Gamma_1:

    - T_12 crosses the weak axis (direction 1) and is EWSB-enhanced
    - T_23 connects color corners X_2 and X_3, orthogonal to EWSB
    - R > 1 is a parameter-free prediction of the framework

  From R, V_cb follows via the NNI formula without knowing K:
    c_12/c_23 = R * sqrt(kappa_12/kappa_23)   (EW charge correction)

LATTICE PLAN:
  L=6:  N_cfg=50   dim=648    ~0.006 GB  (fast baseline)
  L=8:  N_cfg=50   dim=1536   ~0.04  GB  (primary measurement)
  L=10: N_cfg=30   dim=3000   ~0.14  GB  (volume check)
  L=12: N_cfg=20   dim=5184   ~0.40  GB  (large-volume anchor)

USAGE:
  python3 scripts/frontier_ckm_ratio_multi_L.py               # full run
  python3 scripts/frontier_ckm_ratio_multi_L.py --quick        # test (3 cfgs each)
  python3 scripts/frontier_ckm_ratio_multi_L.py 2>&1 | tee ~/Desktop/ckm_ratio_multi_L.txt

Self-contained: numpy + scipy only.
"""

from __future__ import annotations

import argparse
import sys
import time
import numpy as np

np.set_printoptions(precision=10, linewidth=120, suppress=True)

# =============================================================================
# Physical constants
# =============================================================================

SIN2_TW = 0.231
ALPHA_S_2GEV = 0.30
ALPHA_EM = 1.0 / 137.0

Q_UP, T3_UP = 2.0 / 3.0, 0.5
Q_DOWN, T3_DOWN = -1.0 / 3.0, -0.5

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

# Fitted NNI coefficients (target values)
C12_U_FIT = 1.48
C23_U_FIT = 0.65
C12_D_FIT = 0.91
C23_D_FIT = 0.65


# =============================================================================
# SU(3) gauge utilities
# =============================================================================

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
    """Sum of staples around link U_mu(x) for Wilson gauge action."""
    coords = [x, y, z]
    staple_sum = np.zeros((3, 3), dtype=complex)

    for nu in range(3):
        if nu == mu:
            continue

        xp_mu = list(coords)
        xp_mu[mu] = (xp_mu[mu] + 1) % L
        xp_nu = list(coords)
        xp_nu[nu] = (xp_nu[nu] + 1) % L

        U_nu_xpmu = gauge_links[nu][xp_mu[0], xp_mu[1], xp_mu[2]]
        U_mu_xpnu = gauge_links[mu][xp_nu[0], xp_nu[1], xp_nu[2]]
        U_nu_x = gauge_links[nu][x, y, z]
        staple_sum += U_nu_xpmu @ U_mu_xpnu.conj().T @ U_nu_x.conj().T

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
    """One Metropolis sweep. Returns acceptance rate."""
    n_accept = 0
    n_total = 0

    for mu in range(3):
        for x in range(L):
            for y in range(L):
                for z in range(L):
                    U_old = gauge_links[mu][x, y, z].copy()
                    staple = wilson_action_staple(gauge_links, L, mu, x, y, z)
                    dU = su3_near_identity(rng, epsilon)
                    U_new = dU @ U_old

                    delta_S = -(beta / 3.0) * np.real(
                        np.trace((U_new - U_old) @ staple)
                    )

                    if delta_S < 0 or rng.random() < np.exp(-delta_S):
                        gauge_links[mu][x, y, z] = U_new
                        n_accept += 1
                    n_total += 1

    return n_accept / n_total


def generate_gauge_config(L, beta, rng, n_therm=50, n_skip=10, epsilon=0.2):
    """Generate a thermalized SU(3) gauge configuration via Metropolis."""
    gauge_links = []
    for mu in range(3):
        links = np.zeros((L, L, L, 3, 3), dtype=complex)
        for x in range(L):
            for y in range(L):
                for z in range(L):
                    links[x, y, z] = np.eye(3, dtype=complex)
        gauge_links.append(links)

    for sweep in range(n_therm):
        metropolis_update(gauge_links, L, beta, rng, epsilon)

    for sweep in range(n_skip):
        metropolis_update(gauge_links, L, beta, rng, epsilon)

    return gauge_links


def measure_plaquette(gauge_links, L):
    """Measure average plaquette."""
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
# Dirac operator (dense, position-space)
# =============================================================================

def build_dirac_operator(L, gauge_links, r_wilson, y_v):
    """
    Build H = H_KS + H_W + H_EWSB as a dense matrix.
    dim = 3 * L^3 (color x sites).
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

                            # Staggered kinetic
                            H[ia, jb] += 0.5 * eta_val * U[a, b]
                            H[jb, ia] -= 0.5 * eta_val * U[a, b].conj()

                            # Wilson taste-breaking
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
    Returns T matrix and the BZ corners used.
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
    """EW coupling for 1-2 transition (crosses weak axis)."""
    g_neutral = Q ** 2 + (T3 - Q * SIN2_TW) ** 2
    g_charged = T3 ** 2
    return g_neutral + g_charged


def ew_kappa_23(Q, T3):
    """EW coupling for 2-3 transition (color-color)."""
    g_neutral = Q ** 2 + (T3 - Q * SIN2_TW) ** 2
    return g_neutral


# =============================================================================
# NNI mass matrix and CKM
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
# Jackknife
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


def bootstrap_mean_err(samples, n_boot=1000, rng_seed=42):
    """Bootstrap estimate of mean and standard error."""
    rng = np.random.default_rng(rng_seed)
    n = len(samples)
    boot_means = np.zeros(n_boot)
    for b in range(n_boot):
        idx = rng.integers(0, n, size=n)
        boot_means[b] = np.mean(samples[idx])
    return np.mean(samples), np.std(boot_means)


# =============================================================================
# Single lattice-size measurement
# =============================================================================

def run_lattice_size(L, n_cfg, beta, r_wilson, y_v, rng_base_seed,
                     n_therm, n_skip, epsilon_metro):
    """
    Run the ratio measurement at a given L.
    Returns dict with per-config data and ensemble statistics.
    """
    dim = L ** 3 * 3
    mem_gb = dim ** 2 * 16 / 1e9

    print(f"\n{'=' * 78}")
    print(f"  L = {L}  |  dim = {dim}  |  mem = {mem_gb:.3f} GB  |  N_cfg = {n_cfg}")
    print(f"  beta={beta}  r_W={r_wilson}  yv={y_v}  "
          f"n_therm={n_therm}  n_skip={n_skip}  eps={epsilon_metro}")
    print(f"{'=' * 78}")

    assert mem_gb < 12.0, f"Matrix too large: {mem_gb:.1f} GB"

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

        gauge_links = generate_gauge_config(
            L, beta, rng, n_therm=n_therm, n_skip=n_skip, epsilon=epsilon_metro
        )

        plaq = measure_plaquette(gauge_links, L)
        all_plaq.append(plaq)

        H_total = build_dirac_operator(L, gauge_links, r_wilson, y_v)
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

        print(f"  cfg {cfg+1:3d}/{n_cfg}: plaq={plaq:.4f}  "
              f"|T12|={t12:.3e}  |T23|={t23:.3e}  "
              f"R={R12_23:.3f}  [{t_cfg:.1f}s, ETA {t_remaining:.0f}s]")

    total_time = time.time() - t_start

    # Ensemble statistics
    arr_R = np.array(all_R12_23)
    R_jk_mean, R_jk_err = jackknife_mean_err(arr_R)
    R_bs_mean, R_bs_err = bootstrap_mean_err(arr_R)

    # Ratio of means (alternative estimator)
    t12_mean = np.mean(all_t12)
    t23_mean = np.mean(all_t23)
    rom = t12_mean / t23_mean if t23_mean > 0 else float('inf')

    # Z2 residual: X_2 and X_3 should be degenerate
    z2_residuals = np.array([
        abs(all_t12[i] - all_t13[i]) / max(all_t12[i], all_t13[i])
        if max(all_t12[i], all_t13[i]) > 0 else 0.0
        for i in range(n_cfg)
    ])

    plaq_mean, plaq_err = jackknife_mean_err(np.array(all_plaq))
    R13_mean, R13_err = jackknife_mean_err(np.array(all_R13_23))

    print(f"\n  --- L={L} Results ({n_cfg} cfgs, {total_time:.0f}s) ---")
    print(f"  Plaquette:          {plaq_mean:.6f} +/- {plaq_err:.6f}")
    print(f"  R_12/23 (jackknife): {R_jk_mean:.4f} +/- {R_jk_err:.4f}")
    print(f"  R_12/23 (bootstrap): {R_bs_mean:.4f} +/- {R_bs_err:.4f}")
    print(f"  R_12/23 (ratio/means): {rom:.4f}")
    print(f"  R_13/23 (check Z2):  {R13_mean:.4f} +/- {R13_err:.4f}")
    print(f"  Z2 residual <|T12-T13|/max>: {np.mean(z2_residuals):.4f}")

    return {
        'L': L, 'n_cfg': n_cfg, 'total_time': total_time,
        'plaq_mean': plaq_mean, 'plaq_err': plaq_err,
        'R_jk_mean': R_jk_mean, 'R_jk_err': R_jk_err,
        'R_bs_mean': R_bs_mean, 'R_bs_err': R_bs_err,
        'rom': rom,
        'R13_mean': R13_mean, 'R13_err': R13_err,
        'z2_mean': np.mean(z2_residuals),
        'all_R12_23': arr_R,
        'all_t12': np.array(all_t12),
        'all_t13': np.array(all_t13),
        'all_t23': np.array(all_t23),
    }


# =============================================================================
# L-dependence analysis
# =============================================================================

def analyze_L_dependence(results_by_L):
    """
    Analyze L-dependence of R_12/23 and extrapolate to L -> infinity.
    """
    print(f"\n{'=' * 78}")
    print(f"  L-DEPENDENCE ANALYSIS")
    print(f"{'=' * 78}")

    Ls = sorted(results_by_L.keys())
    Rs = np.array([results_by_L[L]['R_jk_mean'] for L in Ls])
    errs = np.array([results_by_L[L]['R_jk_err'] for L in Ls])
    inv_L = np.array([1.0 / L for L in Ls])

    print(f"\n  {'L':>4}  {'1/L':>8}  {'R_12/23':>10}  {'err':>8}  {'N_cfg':>6}")
    print(f"  {'-' * 45}")
    for i, L in enumerate(Ls):
        print(f"  {L:4d}  {inv_L[i]:8.4f}  {Rs[i]:10.4f}  {errs[i]:8.4f}  "
              f"{results_by_L[L]['n_cfg']:6d}")

    # Weighted mean (if L-dependence is negligible)
    w = 1.0 / errs**2
    R_wmean = np.sum(w * Rs) / np.sum(w)
    R_wmean_err = 1.0 / np.sqrt(np.sum(w))

    print(f"\n  Weighted mean R_12/23 = {R_wmean:.4f} +/- {R_wmean_err:.4f}")

    # Check chi^2/dof for consistency
    chi2 = np.sum(w * (Rs - R_wmean)**2)
    dof = len(Ls) - 1
    chi2_dof = chi2 / dof if dof > 0 else 0.0

    print(f"  chi^2/dof = {chi2:.2f}/{dof} = {chi2_dof:.2f}")
    if chi2_dof < 2.0:
        print(f"  -> Consistent with no L-dependence (chi^2/dof < 2)")
    else:
        print(f"  -> Possible L-dependence detected (chi^2/dof > 2)")

    # Linear extrapolation: R(L) = R_inf + c/L
    R_inf = R_wmean
    R_inf_err = R_wmean_err

    if len(Ls) >= 3:
        try:
            # Weighted linear fit: R = a + b/L
            A = np.column_stack([np.ones(len(Ls)), inv_L])
            W = np.diag(w)
            AtwA = A.T @ W @ A
            Atwb = A.T @ W @ Rs
            params = np.linalg.solve(AtwA, Atwb)
            cov = np.linalg.inv(AtwA)

            R_inf = params[0]
            R_inf_err = np.sqrt(cov[0, 0])
            slope = params[1]
            slope_err = np.sqrt(cov[1, 1])

            print(f"\n  Linear fit R = R_inf + c/L:")
            print(f"    R_inf = {R_inf:.4f} +/- {R_inf_err:.4f}")
            print(f"    c     = {slope:.4f} +/- {slope_err:.4f}")

            if abs(slope) < 2 * slope_err:
                print(f"    -> Slope consistent with zero (|c| < 2*sigma)")
                print(f"    -> Using weighted mean as best estimate")
                R_inf = R_wmean
                R_inf_err = R_wmean_err
            else:
                print(f"    -> Non-zero slope at {abs(slope)/slope_err:.1f} sigma")
                print(f"    -> Using extrapolated R_inf")
        except np.linalg.LinAlgError:
            print(f"\n  Linear fit failed; using weighted mean")

    print(f"\n  BEST ESTIMATE: R_12/23 = {R_inf:.4f} +/- {R_inf_err:.4f}")

    return R_inf, R_inf_err, R_wmean, R_wmean_err


# =============================================================================
# CKM extraction from ratio
# =============================================================================

def extract_ckm_from_ratio(R, R_err):
    """
    Extract V_cb and other CKM elements from the ratio R = c_12/c_23.
    The ratio eliminates K entirely.
    """
    print(f"\n{'=' * 78}")
    print(f"  CKM EXTRACTION FROM RATIO R_12/23")
    print(f"{'=' * 78}")

    # EW charge factors
    k12_u = ew_kappa_12(Q_UP, T3_UP)
    k23_u = ew_kappa_23(Q_UP, T3_UP)
    k12_d = ew_kappa_12(Q_DOWN, T3_DOWN)
    k23_d = ew_kappa_23(Q_DOWN, T3_DOWN)

    print(f"\n  EW charge factors:")
    print(f"    kappa_12(u) = {k12_u:.4f}    kappa_23(u) = {k23_u:.4f}")
    print(f"    kappa_12(d) = {k12_d:.4f}    kappa_23(d) = {k23_d:.4f}")

    # The lattice ratio R = |T_12|/|T_23| gives the NNI coefficient ratio:
    #   c_12/c_23 = R * sqrt(kappa_12/kappa_23)  for each sector
    # But the EW charge correction enters only in the NNI coefficient mapping.
    # The raw lattice ratio R is sector-independent.

    ew_corr_u = np.sqrt(k12_u / k23_u)
    ew_corr_d = np.sqrt(k12_d / k23_d)

    c12_over_c23_u = R * ew_corr_u
    c12_over_c23_d = R * ew_corr_d

    print(f"\n  Lattice ratio R = {R:.4f} +/- {R_err:.4f}")
    print(f"  EW correction sqrt(k12/k23):")
    print(f"    up sector:   {ew_corr_u:.4f}")
    print(f"    down sector: {ew_corr_d:.4f}")
    print(f"  c_12/c_23 (up)   = {c12_over_c23_u:.4f}")
    print(f"  c_12/c_23 (down) = {c12_over_c23_d:.4f}")

    # Fitted ratio for comparison
    fit_ratio_u = C12_U_FIT / C23_U_FIT
    fit_ratio_d = C12_D_FIT / C23_D_FIT

    print(f"\n  Fitted ratio c_12/c_23:")
    print(f"    up sector:   {fit_ratio_u:.4f}")
    print(f"    down sector: {fit_ratio_d:.4f}")

    dev_u = abs(c12_over_c23_u - fit_ratio_u) / fit_ratio_u * 100
    dev_d = abs(c12_over_c23_d - fit_ratio_d) / fit_ratio_d * 100
    print(f"  Deviation: up {dev_u:.1f}%, down {dev_d:.1f}%")

    # 1-loop normalization for absolute coefficients
    N_c = 3
    alpha_s = ALPHA_S_2GEV
    L_enh = np.log(1.22e19 / 246.0) / (4.0 * np.pi)
    C_base = N_c * alpha_s * L_enh / np.pi
    kappa_ref = (k23_u + k23_d) / 2.0

    c23_u = C_base * np.sqrt(k23_u / kappa_ref)
    c23_d = C_base * np.sqrt(k23_d / kappa_ref)
    c12_u = c23_u * c12_over_c23_u
    c12_d = c23_d * c12_over_c23_d

    c12_u_err = c23_u * R_err * ew_corr_u
    c12_d_err = c23_d * R_err * ew_corr_d

    print(f"\n  Absolute NNI coefficients (1-loop + ratio):")
    print(f"  {'coeff':>8}  {'derived':>10}  {'err':>8}  {'fitted':>8}  {'dev%':>6}")
    print(f"  {'-' * 50}")
    for name, val, err, fit in [
        ('c12_u', c12_u, c12_u_err, C12_U_FIT),
        ('c23_u', c23_u, 0.0, C23_U_FIT),
        ('c12_d', c12_d, c12_d_err, C12_D_FIT),
        ('c23_d', c23_d, 0.0, C23_D_FIT),
    ]:
        dev = abs(val - fit) / fit * 100
        err_s = f"+/- {err:.4f}" if err > 0 else "  (norm)"
        print(f"  {name:>8}  {val:10.4f}  {err_s:>8}  {fit:8.4f}  {dev:5.1f}%")

    # Build CKM
    M_u = build_nni_mass_matrix(MASSES_UP, c12_u, c23_u)
    M_d = build_nni_mass_matrix(MASSES_DOWN, c12_d, c23_d)
    V_ckm, m_u_diag, m_d_diag = diagonalize_and_ckm(M_u, M_d)

    V_us = abs(V_ckm[0, 1])
    V_cb = abs(V_ckm[1, 2])
    V_ub = abs(V_ckm[0, 2])

    print(f"\n  |V_CKM| matrix:")
    for i in range(3):
        row = "    "
        for j in range(3):
            row += f"{abs(V_ckm[i, j]):10.6f}"
        print(row)

    print(f"\n  {'element':>10}  {'derived':>10}  {'PDG':>10}  {'dev%':>8}")
    print(f"  {'-' * 45}")
    for name, val, pdg in [
        ('|V_us|', V_us, V_US_PDG),
        ('|V_cb|', V_cb, V_CB_PDG),
        ('|V_ub|', V_ub, V_UB_PDG),
    ]:
        dev = abs(val - pdg) / pdg * 100
        print(f"  {name:>10}  {val:10.6f}  {pdg:10.6f}  {dev:7.1f}%")

    # Jackknife CKM error propagation
    # Vary R within its error band
    n_samples = 200
    rng = np.random.default_rng(12345)
    R_samples = rng.normal(R, R_err, n_samples)

    V_us_samples = []
    V_cb_samples = []
    V_ub_samples = []

    for R_s in R_samples:
        c12u_s = c23_u * R_s * ew_corr_u
        c12d_s = c23_d * R_s * ew_corr_d
        Mu_s = build_nni_mass_matrix(MASSES_UP, c12u_s, c23_u)
        Md_s = build_nni_mass_matrix(MASSES_DOWN, c12d_s, c23_d)
        V_s, _, _ = diagonalize_and_ckm(Mu_s, Md_s)
        V_us_samples.append(abs(V_s[0, 1]))
        V_cb_samples.append(abs(V_s[1, 2]))
        V_ub_samples.append(abs(V_s[0, 2]))

    V_us_err = np.std(V_us_samples)
    V_cb_err = np.std(V_cb_samples)
    V_ub_err = np.std(V_ub_samples)

    print(f"\n  CKM with propagated errors:")
    print(f"    |V_us| = {V_us:.6f} +/- {V_us_err:.6f}  (PDG: {V_US_PDG})")
    print(f"    |V_cb| = {V_cb:.6f} +/- {V_cb_err:.6f}  (PDG: {V_CB_PDG})")
    print(f"    |V_ub| = {V_ub:.6f} +/- {V_ub_err:.6f}  (PDG: {V_UB_PDG})")

    # Unitarity check
    row0_sq = sum(abs(V_ckm[0, j]) ** 2 for j in range(3))
    print(f"\n  Unitarity: sum|V_u*|^2 = {row0_sq:.8f}")

    return {
        'R': R, 'R_err': R_err,
        'c12_over_c23_u': c12_over_c23_u, 'c12_over_c23_d': c12_over_c23_d,
        'c12_u': c12_u, 'c23_u': c23_u, 'c12_d': c12_d, 'c23_d': c23_d,
        'V_us': V_us, 'V_cb': V_cb, 'V_ub': V_ub,
        'V_us_err': V_us_err, 'V_cb_err': V_cb_err, 'V_ub_err': V_ub_err,
    }


# =============================================================================
# Final summary
# =============================================================================

def print_summary(results_by_L, R_inf, R_inf_err, ckm):
    """Print final summary."""
    print(f"\n{'#' * 78}")
    print(f"#  FINAL SUMMARY: c_12/c_23 MULTI-L RATIO MEASUREMENT")
    print(f"{'#' * 78}")

    print(f"\n  Lattice parameters: beta=6, r_W=1.0, yv=0.5")

    print(f"\n  {'L':>4}  {'N_cfg':>6}  {'R_12/23':>10}  {'err':>8}  {'plaq':>8}  {'Z2':>6}  {'time':>6}")
    print(f"  {'-' * 58}")
    for L in sorted(results_by_L.keys()):
        r = results_by_L[L]
        print(f"  {L:4d}  {r['n_cfg']:6d}  {r['R_jk_mean']:10.4f}  "
              f"{r['R_jk_err']:8.4f}  {r['plaq_mean']:8.4f}  "
              f"{r['z2_mean']:6.3f}  {r['total_time']:5.0f}s")

    print(f"\n  BEST R_12/23 = {R_inf:.4f} +/- {R_inf_err:.4f}")

    print(f"\n  CKM Results:")
    print(f"    |V_us| = {ckm['V_us']:.6f} +/- {ckm['V_us_err']:.6f}  "
          f"(PDG {V_US_PDG}, dev {abs(ckm['V_us']-V_US_PDG)/V_US_PDG*100:.1f}%)")
    print(f"    |V_cb| = {ckm['V_cb']:.6f} +/- {ckm['V_cb_err']:.6f}  "
          f"(PDG {V_CB_PDG}, dev {abs(ckm['V_cb']-V_CB_PDG)/V_CB_PDG*100:.1f}%)")
    print(f"    |V_ub| = {ckm['V_ub']:.6f} +/- {ckm['V_ub_err']:.6f}  "
          f"(PDG {V_UB_PDG}, dev {abs(ckm['V_ub']-V_UB_PDG)/V_UB_PDG*100:.1f}%)")

    # Structural checks
    print(f"\n  Structural checks:")
    checks = [
        ("R_12/23 > 1 (EWSB enhancement)", R_inf > 1.0),
        ("c_12/c_23 > 1 for both sectors",
         ckm['c12_over_c23_u'] > 1.0 and ckm['c12_over_c23_d'] > 1.0),
        ("|V_us| > |V_cb| > |V_ub| (hierarchy)",
         ckm['V_us'] > ckm['V_cb'] > ckm['V_ub']),
        ("R_12/23 statistical error < 15%",
         R_inf_err / R_inf < 0.15 if R_inf > 0 else False),
    ]

    n_pass = 0
    for desc, passed in checks:
        status = "PASS" if passed else "FAIL"
        print(f"    [{status}] {desc}")
        if passed:
            n_pass += 1

    print(f"\n  Checks: {n_pass}/{len(checks)} passed")
    print(f"\n{'#' * 78}")


# =============================================================================
# Main
# =============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="CKM c_12/c_23 ratio: multi-L high-statistics measurement"
    )
    parser.add_argument('--quick', action='store_true',
                        help='Quick test: 3 configs per L, L=6,8 only')
    parser.add_argument('--beta', type=float, default=6.0)
    parser.add_argument('--rwilson', type=float, default=1.0)
    parser.add_argument('--yv', type=float, default=0.5)
    parser.add_argument('--seed', type=int, default=20260413)
    args = parser.parse_args()

    print("=" * 78)
    print("  CKM c_12/c_23 RATIO: MULTI-L HIGH-STATISTICS MEASUREMENT")
    print("=" * 78)
    print(f"  Date: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"  Python: {sys.version.split()[0]}")
    print(f"  NumPy: {np.__version__}")

    if args.quick:
        print(f"\n  MODE: QUICK TEST")
        lattice_plan = [(6, 3), (8, 3)]
        n_therm = 20
        n_skip = 5
    else:
        print(f"\n  MODE: FULL PRODUCTION")
        lattice_plan = [(6, 50), (8, 50), (10, 30), (12, 20)]
        n_therm = 100
        n_skip = 20

    epsilon_metro = 0.2

    print(f"  Lattice plan:")
    total_cfgs = 0
    for L, ncfg in lattice_plan:
        dim = L ** 3 * 3
        mem_gb = dim ** 2 * 16 / 1e9
        print(f"    L={L:2d}: {ncfg:3d} cfgs, dim={dim:5d}, mem={mem_gb:.3f} GB")
        total_cfgs += ncfg
    print(f"  Total configs: {total_cfgs}")
    print(f"  beta={args.beta}, r_W={args.rwilson}, yv={args.yv}, seed={args.seed}")

    t_total_start = time.time()

    results_by_L = {}
    for L, n_cfg in lattice_plan:
        results_by_L[L] = run_lattice_size(
            L, n_cfg, args.beta, args.rwilson, args.yv, args.seed,
            n_therm, n_skip, epsilon_metro
        )

    # L-dependence analysis
    R_inf, R_inf_err, R_wmean, R_wmean_err = analyze_L_dependence(results_by_L)

    # CKM extraction
    ckm = extract_ckm_from_ratio(R_inf, R_inf_err)

    # Summary
    print_summary(results_by_L, R_inf, R_inf_err, ckm)

    t_total = time.time() - t_total_start
    print(f"\n  Total wall time: {t_total:.0f}s ({t_total/60:.1f} min)")

    return 0


if __name__ == '__main__':
    sys.exit(main())
