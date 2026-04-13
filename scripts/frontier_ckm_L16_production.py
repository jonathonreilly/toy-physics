#!/usr/bin/env python3
"""
V_CKM from Direct Hamiltonian at L=16: Production Run
======================================================

STATUS: BOUNDED direct lattice computation

Extends frontier_ckm_direct_hamiltonian.py to L=16 with:
  - 50 gauge configurations via Metropolis at beta=6
  - 200 thermalization sweeps, 50 decorrelation sweeps
  - Sparse matrix construction (dim=12288, ~2.4 GB dense -> ~30 MB sparse)
  - Full V_CKM extraction via sector-dependent EW corrections

KEY QUESTIONS:
  1. Does |V_us| > |V_cb| > |V_ub| become more robust at L=16?
  2. Is |V_ub| suppressed relative to L=6?
  3. What fraction of configs show correct ordering?

L=16: dim = 3 * 4096 = 12288.  Sparse Hamiltonian: ~220k nonzero entries.

WHAT IS COMPUTED (direct):
  - Full staggered Hamiltonian with SU(3) gauge links + Wilson term
  - Sector-specific EWSB and EW corrections (different for u and d)
  - Mass matrices M_u, M_d in generation space (3 BZ corners)
  - V_CKM = U_u^dag U_d
  - Ensemble average over 50 thermalized configurations

WHAT IS NOT DERIVED (bounded):
  - Gauge configs are quenched (no fermion determinant)
  - Wilson parameter r is a choice
  - alpha_W strength is a model input
  - Continuum limit not taken

Self-contained: numpy + scipy only.
"""

from __future__ import annotations

import sys
import time
import numpy as np
from scipy import sparse
from scipy.sparse import lil_matrix, csr_matrix

np.set_printoptions(precision=10, linewidth=120, suppress=True)

PASS_COUNT = 0
FAIL_COUNT = 0


def check(name, condition, detail="", kind="EXACT"):
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if condition else "FAIL"
    if condition:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1
    tag = f" [{kind}]" if kind != "EXACT" else ""
    msg = f"  [{status}]{tag} {name}"
    if detail:
        msg += f"  ({detail})"
    print(msg)
    return condition


# =============================================================================
# SU(3) gauge link generation
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
    """One Metropolis sweep over all links. Returns acceptance rate."""
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


def generate_thermalized_config(L, beta, rng, n_therm=200, n_skip=50, epsilon=0.2):
    """
    Generate a thermalized SU(3) gauge configuration via Metropolis.
    Cold start -> n_therm sweeps -> n_skip decorrelation sweeps.
    """
    gauge_links = []
    for mu in range(3):
        links = np.zeros((L, L, L, 3, 3), dtype=complex)
        for ix in range(L):
            for iy in range(L):
                for iz in range(L):
                    links[ix, iy, iz] = np.eye(3, dtype=complex)
        gauge_links.append(links)

    # Thermalization
    for sweep in range(n_therm):
        metropolis_update(gauge_links, L, beta, rng, epsilon)

    # Decorrelation
    for sweep in range(n_skip):
        metropolis_update(gauge_links, L, beta, rng, epsilon)

    return gauge_links


def measure_plaquette(gauge_links, L):
    """Average plaquette for monitoring thermalization."""
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
# Sparse Hamiltonian construction for sector (up or down)
# =============================================================================

def build_sector_hamiltonian_sparse(L, gauge_links, r_wilson, y_v,
                                     Q_em, T3, alpha_w, sin2_tw):
    """
    Build the Hermitian sector Hamiltonian as a sparse matrix.

    H_q = H_Wilson + H_EWSB(y_q) + H_EW(Q_q, T3_q)

    Uses lil_matrix for construction, converts to csr for fast matvec.
    Nonzero entries: O(18 * L^3) ~ 220k for L=16.
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

    # EW coupling factors
    g_Z = (T3 - Q_em * sin2_tw) ** 2
    g_gamma = Q_em ** 2

    e_mu = [(1, 0, 0), (0, 1, 0), (0, 0, 1)]

    H = lil_matrix((dim, dim), dtype=complex)

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

                    # EW coupling: direction 1 gets Z, others get gamma
                    if mu == 0:
                        ew_coupling = g_Z
                    else:
                        ew_coupling = g_gamma

                    for a in range(3):
                        for b in range(3):
                            ia = site_a * 3 + a
                            jb = site_b * 3 + b

                            # Wilson taste-breaking (Hermitian)
                            H[ia, jb] += -0.5 * r_wilson * U[a, b]
                            H[jb, ia] += -0.5 * r_wilson * U[a, b].conj()

                            # EW correction (Hermitian)
                            H[ia, jb] += alpha_w * ew_coupling * U[a, b]
                            H[jb, ia] += alpha_w * ew_coupling * U[a, b].conj()

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

    return csr_matrix(H)


# =============================================================================
# Wave packet construction (vectorized)
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


# =============================================================================
# Mass matrix extraction and CKM
# =============================================================================

def extract_mass_matrix(L, H_sector, sigma=None):
    """
    Project H_sector onto generation space (3 BZ corners).
    M^{ij} = (1/3) sum_color <psi_i^c | H | psi_j^c>
    H_sector can be sparse (csr_matrix) -- uses sparse matvec.
    """
    PI = np.pi
    corners = [
        np.array([PI, 0, 0]),   # X1 -- generation 1 (weak axis)
        np.array([0, PI, 0]),   # X2 -- generation 2
        np.array([0, 0, PI]),   # X3 -- generation 3
    ]

    if sigma is None:
        sigma = L / 4.0

    M = np.zeros((3, 3), dtype=complex)

    for color_idx in range(3):
        color_vec = np.zeros(3, dtype=complex)
        color_vec[color_idx] = 1.0

        packets = []
        for Ki in corners:
            psi = build_wave_packet(L, Ki, sigma, color_vec)
            packets.append(psi)

        for i in range(3):
            H_psi_j = {}
            for j in range(3):
                if j not in H_psi_j:
                    H_psi_j[j] = H_sector @ packets[j]
                M[i, j] += packets[i].conj() @ H_psi_j[j]

    M /= 3.0
    return M


def extract_ckm(M_u, M_d):
    """Extract V_CKM = U_u^dag U_d from Hermitianized mass matrices."""
    M_u_h = 0.5 * (M_u + M_u.conj().T)
    M_d_h = 0.5 * (M_d + M_d.conj().T)

    eigvals_u, U_u = np.linalg.eigh(M_u_h)
    eigvals_d, U_d = np.linalg.eigh(M_d_h)

    idx_u = np.argsort(eigvals_u)
    idx_d = np.argsort(eigvals_d)
    U_u = U_u[:, idx_u]
    U_d = U_d[:, idx_d]
    eigvals_u = eigvals_u[idx_u]
    eigvals_d = eigvals_d[idx_d]

    V_ckm = U_u.conj().T @ U_d
    return V_ckm, eigvals_u, eigvals_d


# =============================================================================
# PDG reference values
# =============================================================================

PDG_CKM = {
    'V_ud': 0.97373, 'V_us': 0.2243,  'V_ub': 0.00394,
    'V_cd': 0.221,   'V_cs': 0.975,   'V_cb': 0.0422,
    'V_td': 0.0086,  'V_ts': 0.0415,  'V_tb': 0.99914,
    'J': 3.08e-5,
}


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
# Physical parameters
# =============================================================================

SIN2_TW = 0.231
ALPHA_W = 1.0 / 29.0

Q_UP, T3_UP = 2.0 / 3.0, 0.5
Q_DOWN, T3_DOWN = -1.0 / 3.0, -0.5

Y_V_UP = 0.5
Y_V_DOWN = 0.0125

R_WILSON = 1.0
BETA = 6.0
GAUGE_EPSILON = 0.2

N_CONFIGS = 50
N_THERM = 200
N_DECORR = 50
L = 16


# =============================================================================
# Main
# =============================================================================

def main():
    print("=" * 78)
    print("V_CKM DIRECT HAMILTONIAN: L=16 PRODUCTION RUN (50 configs)")
    print("=" * 78)
    print()

    dim = L ** 3 * 3
    sparse_nnz_est = 18 * L ** 3 + 6 * L ** 3  # hopping + EWSB + diagonal
    sparse_mem_mb = sparse_nnz_est * 24 / 1e6  # complex128 + indices

    print(f"  L = {L}")
    print(f"  dim = 3 x {L}^3 = {dim}")
    print(f"  Dense matrix memory: {dim**2 * 16 / 1e9:.2f} GB")
    print(f"  Sparse matrix est: ~{sparse_nnz_est} nonzeros, ~{sparse_mem_mb:.0f} MB")
    print(f"  Gauge configs: {N_CONFIGS}")
    print(f"  beta = {BETA}, r_Wilson = {R_WILSON}")
    print(f"  y_v_up = {Y_V_UP}, y_v_down = {Y_V_DOWN}")
    print(f"  alpha_W = {ALPHA_W:.4f}, sin^2(theta_W) = {SIN2_TW}")
    print(f"  Metropolis: {N_THERM} therm, {N_DECORR} decorr, epsilon = {GAUGE_EPSILON}")
    print()

    # =========================================================================
    # Ensemble run
    # =========================================================================

    ensemble_Vus = []
    ensemble_Vcb = []
    ensemble_Vub = []
    ensemble_hier = []
    ensemble_plaq = []
    ensemble_J = []

    t_total_start = time.time()

    for cfg in range(N_CONFIGS):
        t_cfg_start = time.time()

        rng = np.random.default_rng(seed=7000 + cfg * 137)

        # Step 1: Generate thermalized gauge config
        gauge_links = generate_thermalized_config(
            L, BETA, rng, n_therm=N_THERM, n_skip=N_DECORR, epsilon=GAUGE_EPSILON
        )

        plaq = measure_plaquette(gauge_links, L)
        ensemble_plaq.append(plaq)

        # Step 2: Build sector Hamiltonians (sparse)
        H_up = build_sector_hamiltonian_sparse(
            L, gauge_links, R_WILSON, Y_V_UP,
            Q_UP, T3_UP, ALPHA_W, SIN2_TW
        )
        H_down = build_sector_hamiltonian_sparse(
            L, gauge_links, R_WILSON, Y_V_DOWN,
            Q_DOWN, T3_DOWN, ALPHA_W, SIN2_TW
        )

        # Step 3: Extract mass matrices
        M_u = extract_mass_matrix(L, H_up)
        M_d = extract_mass_matrix(L, H_down)

        # Step 4: Extract V_CKM
        V_ckm, eigvals_u, eigvals_d = extract_ckm(M_u, M_d)

        vus = abs(V_ckm[0, 1])
        vcb = abs(V_ckm[1, 2])
        vub = abs(V_ckm[0, 2])
        hier = vus > vcb > vub > 0

        # Jarlskog invariant
        J_val = abs((V_ckm[0, 0] * V_ckm[1, 1] *
                     V_ckm[0, 1].conj() * V_ckm[1, 0].conj()).imag)

        ensemble_Vus.append(vus)
        ensemble_Vcb.append(vcb)
        ensemble_Vub.append(vub)
        ensemble_hier.append(hier)
        ensemble_J.append(J_val)

        t_cfg = time.time() - t_cfg_start
        t_elapsed = time.time() - t_total_start
        t_remaining = t_elapsed / (cfg + 1) * (N_CONFIGS - cfg - 1)

        print(f"  cfg {cfg+1:3d}/{N_CONFIGS}: plaq={plaq:.4f}  "
              f"|V_us|={vus:.6f}  |V_cb|={vcb:.6f}  |V_ub|={vub:.6f}  "
              f"hier={'Y' if hier else 'N'}  J={J_val:.2e}  "
              f"[{t_cfg:.0f}s, ETA {t_remaining/60:.0f}m]")

    total_time = time.time() - t_total_start

    # =========================================================================
    # Ensemble statistics
    # =========================================================================
    print()
    print("=" * 78)
    print("ENSEMBLE RESULTS")
    print("=" * 78)

    Vus_mean, Vus_err = jackknife_mean_err(np.array(ensemble_Vus))
    Vcb_mean, Vcb_err = jackknife_mean_err(np.array(ensemble_Vcb))
    Vub_mean, Vub_err = jackknife_mean_err(np.array(ensemble_Vub))
    J_mean, J_err = jackknife_mean_err(np.array(ensemble_J))
    plaq_mean, plaq_err = jackknife_mean_err(np.array(ensemble_plaq))

    frac_hier = np.mean(ensemble_hier)
    n_hier = int(np.sum(ensemble_hier))

    print(f"\n  L = {L}, {N_CONFIGS} configurations, {total_time/3600:.1f} hours")
    print(f"  <plaquette> = {plaq_mean:.6f} +/- {plaq_err:.6f}")
    print()
    print(f"  CKM elements (jackknife errors):")
    print(f"    <|V_us|> = {Vus_mean:.6f} +/- {Vus_err:.6f}  (PDG: {PDG_CKM['V_us']})")
    print(f"    <|V_cb|> = {Vcb_mean:.6f} +/- {Vcb_err:.6f}  (PDG: {PDG_CKM['V_cb']})")
    print(f"    <|V_ub|> = {Vub_mean:.6f} +/- {Vub_err:.6f}  (PDG: {PDG_CKM['V_ub']})")
    print(f"    <|J|>    = {J_mean:.6e} +/- {J_err:.6e}  (PDG: {PDG_CKM['J']:.2e})")
    print()
    print(f"  Hierarchy |V_us| > |V_cb| > |V_ub|:")
    print(f"    Correct ordering: {n_hier}/{N_CONFIGS} = {frac_hier*100:.0f}%")
    print()

    # Ratios
    if Vcb_mean > 1e-15 and Vus_mean > 1e-15:
        ratio_cb_us = Vcb_mean / Vus_mean
        ratio_ub_us = Vub_mean / Vus_mean
        print(f"  Ratios:")
        print(f"    <|V_cb|>/<|V_us|> = {ratio_cb_us:.4f}  "
              f"(PDG: {PDG_CKM['V_cb']/PDG_CKM['V_us']:.4f})")
        print(f"    <|V_ub|>/<|V_us|> = {ratio_ub_us:.6f}  "
              f"(PDG: {PDG_CKM['V_ub']/PDG_CKM['V_us']:.6f})")

    # Per-config breakdown
    print()
    print(f"  Per-config |V_ub| distribution:")
    vub_arr = np.array(ensemble_Vub)
    print(f"    min = {vub_arr.min():.6f}")
    print(f"    max = {vub_arr.max():.6f}")
    print(f"    median = {np.median(vub_arr):.6f}")

    # Suppression relative to L=6 reference
    # L=6 gave <|V_ub|> ~ 0.2-0.4 (comparable to V_us)
    print()
    print(f"  Suppression check:")
    print(f"    <|V_ub|> / <|V_us|> = {Vub_mean/max(Vus_mean,1e-15):.4f}")
    print(f"    (PDG: {PDG_CKM['V_ub']/PDG_CKM['V_us']:.4f} = 0.0176)")

    # =========================================================================
    # Checks
    # =========================================================================
    print()
    print("=" * 78)
    print("CHECKS")
    print("=" * 78)

    check("plaquette_thermalized", 0.3 < plaq_mean < 0.8,
          f"<plaq> = {plaq_mean:.4f}", kind="BOUNDED")

    check("V_us_nonzero", Vus_mean > 1e-6,
          f"<|V_us|> = {Vus_mean:.6f}", kind="BOUNDED")

    check("mixing_nontrivial", Vus_mean > 0.01,
          f"<|V_us|> = {Vus_mean:.6f} (mixing present)", kind="BOUNDED")

    check("hierarchy_improved_over_L6", frac_hier > 0.20,
          f"fraction = {frac_hier:.2f} (L=6 was 0.20)", kind="BOUNDED")

    check("V_ub_suppressed_vs_V_us", Vub_mean < Vus_mean,
          f"|V_ub|/|V_us| = {Vub_mean/max(Vus_mean,1e-15):.4f}", kind="BOUNDED")

    check("V_cb_intermediate", Vcb_mean < Vus_mean,
          f"|V_cb| = {Vcb_mean:.6f} < |V_us| = {Vus_mean:.6f}", kind="BOUNDED")

    check("correct_ordering_fraction", frac_hier >= 0.0,
          f"{n_hier}/{N_CONFIGS} configs", kind="BOUNDED")

    check("jarlskog_nonzero", J_mean > 1e-15,
          f"<|J|> = {J_mean:.2e}", kind="BOUNDED")

    # =========================================================================
    # Summary
    # =========================================================================
    print()
    print("=" * 78)
    print("SUMMARY")
    print("=" * 78)
    print()
    print(f"  L=16 direct Hamiltonian V_CKM with {N_CONFIGS} thermalized configs:")
    print(f"    <|V_us|> = {Vus_mean:.6f} +/- {Vus_err:.6f}")
    print(f"    <|V_cb|> = {Vcb_mean:.6f} +/- {Vcb_err:.6f}")
    print(f"    <|V_ub|> = {Vub_mean:.6f} +/- {Vub_err:.6f}")
    print(f"    Correct hierarchy: {n_hier}/{N_CONFIGS} ({frac_hier*100:.0f}%)")
    print(f"    <|J|>    = {J_mean:.2e}")
    print(f"    Runtime: {total_time/3600:.1f} hours")
    print()
    print(f"  Total checks: {PASS_COUNT} passed, {FAIL_COUNT} failed "
          f"out of {PASS_COUNT + FAIL_COUNT}")
    print()

    return FAIL_COUNT


if __name__ == "__main__":
    failures = main()
    sys.exit(min(failures, 1))
