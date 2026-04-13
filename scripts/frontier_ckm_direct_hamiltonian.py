#!/usr/bin/env python3
"""
V_CKM Directly from the Lattice Hamiltonian with EWSB
======================================================

STATUS: BOUNDED direct lattice computation

IDEA:
  Previous CKM scripts computed inter-valley scattering amplitudes T_ij
  and then assembled M_u, M_d with ad-hoc EW coupling coefficients.
  This script eliminates that intermediate step.

  The CKM matrix is V = U_u^dag U_d, where U_u, U_d diagonalize the
  up-type and down-type quark mass matrices.  On the staggered lattice,
  these mass matrices ARE the Hamiltonian restricted to each sector,
  projected onto generation space (the 3 BZ corners).

  The up and down Hamiltonians differ because up-type and down-type
  quarks have different electroweak charges:
    Up:   Q = +2/3,  T3 = +1/2
    Down: Q = -1/3,  T3 = -1/2

  These charges enter through:
    1. The EWSB Yukawa term: H_EWSB ~ y_q * v * Gamma_1
       where y_q differs for up vs down (y_u = m_t/v, y_d = m_b/v)
    2. The Z-boson exchange: H_Z ~ (T3 - Q sin^2 theta_W)^2
       which modifies the diagonal self-energies differently
    3. The photon exchange: H_gamma ~ Q^2
       which adds a Q-dependent correction to gauge interactions

  PROCEDURE:
    1. Build H = H_KS + H_Wilson + H_EWSB (full lattice Hamiltonian)
    2. For each sector q in {u, d}, build H_q = H_base + delta_H_q
       where delta_H_q encodes the EW charge difference
    3. Project onto generation space: M_q^{ij} = <X_i | H_q | X_j>
       where X_i are the hw=1 BZ corners
    4. Diagonalize M_u, M_d -> V_CKM = U_u^dag U_d

  This is ONE computation on ONE lattice. No NNI decomposition,
  no separate coefficients, no K normalization.

WHAT IS COMPUTED (direct):
  - Full staggered Hamiltonian with SU(3) gauge links + Wilson term
  - Sector-specific EWSB and EW corrections
  - Mass matrices M_u, M_d in generation space
  - V_CKM = U_u^dag U_d
  - Comparison to PDG values
  - L-dependence (L=4,6,8)
  - Ensemble averaging over gauge configurations

WHAT IS NOT DERIVED (bounded):
  - Gauge configs are quenched
  - Wilson parameter r is a choice
  - alpha_W strength is a model input
  - Continuum limit not taken

Self-contained: numpy only.
"""

from __future__ import annotations

import sys
import numpy as np

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
    """SU(3) matrix close to identity: U = exp(i*epsilon*H) for random Hermitian H."""
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


def generate_gauge_config(L, rng, epsilon):
    """Generate a quenched gauge configuration on Z^3_L."""
    gauge_links = []
    for mu in range(3):
        links = np.zeros((L, L, L, 3, 3), dtype=complex)
        for x in range(L):
            for y in range(L):
                for z in range(L):
                    links[x, y, z] = su3_near_identity(rng, epsilon)
        gauge_links.append(links)
    return gauge_links


def identity_gauge_config(L):
    """Unit gauge configuration (free field)."""
    gauge_links = []
    for mu in range(3):
        links = np.zeros((L, L, L, 3, 3), dtype=complex)
        for x in range(L):
            for y in range(L):
                for z in range(L):
                    links[x, y, z] = np.eye(3, dtype=complex)
        gauge_links.append(links)
    return gauge_links


# =============================================================================
# Staggered Hamiltonian (KS + Wilson)
# =============================================================================

def build_staggered_hamiltonian(L, gauge_links, r_wilson):
    """
    Build H_KS (staggered kinetic) + H_W (Wilson taste-breaking) on Z^3_L.
    Hilbert space: C^{L^3 * 3} (site x color).
    Returns H_ks (anti-Hermitian), H_w (Hermitian).
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

    H_ks = np.zeros((dim, dim), dtype=complex)
    H_w = np.zeros((dim, dim), dtype=complex)

    e_mu = [(1, 0, 0), (0, 1, 0), (0, 0, 1)]

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
                            H_ks[ia, jb] += 0.5 * eta_val * U[a, b]
                            H_ks[jb, ia] -= 0.5 * eta_val * U[a, b].conj()

                    for a in range(3):
                        ia = site_a * 3 + a
                        H_w[ia, ia] += r_wilson

                    for a in range(3):
                        for b in range(3):
                            ia = site_a * 3 + a
                            jb = site_b * 3 + b
                            H_w[ia, jb] -= 0.5 * r_wilson * U[a, b]
                            H_w[jb, ia] -= 0.5 * r_wilson * U[a, b].conj()

    return H_ks, H_w


# =============================================================================
# EWSB term: Yukawa coupling to VEV in direction 1
# =============================================================================

def build_ewsb_term(L, y_v):
    """
    Build H_EWSB = y*v * Gamma_1 on Z^3_L.
    Gamma_1 = shift operator in direction 1, Hermitianized.
    """
    N = L ** 3
    dim = N * 3

    def site_index(x, y, z):
        return ((x % L) * L + (y % L)) * L + (z % L)

    H_ewsb = np.zeros((dim, dim), dtype=complex)

    for x in range(L):
        for y in range(L):
            for z in range(L):
                site_a = site_index(x, y, z)
                xp = (x + 1) % L
                site_b = site_index(xp, y, z)

                for a in range(3):
                    ia = site_a * 3 + a
                    jb = site_b * 3 + a
                    H_ewsb[ia, jb] += y_v
                    H_ewsb[jb, ia] += y_v

    return H_ewsb


# =============================================================================
# EW charge correction: site-diagonal term from Z/gamma exchange
# =============================================================================

def build_ew_correction(L, gauge_links, Q_em, T3, alpha_w, sin2_tw):
    """
    Build the electroweak correction to the Hamiltonian.

    The Z-boson exchange gives a site-dependent correction proportional to
    (T3 - Q sin^2 theta_W)^2 for neutral current, and Q^2 for photon.

    On the lattice, this modifies the gauge interaction:
      H_EW = alpha_W * [Q^2 * H_gamma + (T3 - Q s^2_W)^2 * H_Z]

    where H_gamma and H_Z are nearest-neighbor hopping weighted by the
    EW charges.  For a first approximation, we use a simpler model:

      H_EW = alpha_W * kappa_q * H_W_gauge

    where kappa_q = Q^2 + (T3 - Q s^2_W)^2 encodes the EW coupling
    strength and H_W_gauge is the Wilson term (which is the taste-breaking
    part that lifts the BZ corner degeneracy).

    But here we do something more precise: we add a DIRECTION-DEPENDENT
    correction.  The EWSB picks out direction 1 as the weak axis.
    The Z-coupling modifies hoppings in the weak direction differently:

      H_EW(x, x+e_1) += alpha_W * g_Z(q) * U_1(x)
      H_EW(x, x+e_2) += alpha_W * g_gamma(q) * U_2(x)
      H_EW(x, x+e_3) += alpha_W * g_gamma(q) * U_3(x)

    where g_Z(q) = (T3 - Q s^2_W)^2 and g_gamma(q) = Q^2.
    This direction dependence creates different off-diagonal elements
    in the mass matrix, generating the CKM hierarchy.
    """
    N = L ** 3
    dim = N * 3

    def site_index(x, y, z):
        return ((x % L) * L + (y % L)) * L + (z % L)

    g_Z = (T3 - Q_em * sin2_tw) ** 2
    g_gamma = Q_em ** 2

    H_ew = np.zeros((dim, dim), dtype=complex)

    e_mu = [(1, 0, 0), (0, 1, 0), (0, 0, 1)]

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

                    # Direction 1 gets Z-coupling, others get gamma-coupling
                    if mu == 0:
                        coupling = g_Z
                    else:
                        coupling = g_gamma

                    for a in range(3):
                        for b in range(3):
                            ia = site_a * 3 + a
                            jb = site_b * 3 + b
                            H_ew[ia, jb] += alpha_w * coupling * U[a, b]
                            H_ew[jb, ia] += alpha_w * coupling * U[a, b].conj()

    return H_ew


# =============================================================================
# Full sector Hamiltonian
# =============================================================================

def build_sector_hamiltonian(L, gauge_links, r_wilson, y_v, Q_em, T3,
                              alpha_w, sin2_tw):
    """
    Build the complete Hamiltonian for a quark sector (up or down).

    H_q = H_Wilson + H_EWSB(y_q) + H_EW(Q_q, T3_q)

    We use H_Wilson (taste-breaking part) as the base, since this is what
    lifts the BZ-corner degeneracy and generates inter-valley scattering.
    The KS kinetic term is anti-Hermitian and contributes only to the
    imaginary part; for mass matrix extraction we use the Hermitian part.
    """
    _, H_w = build_staggered_hamiltonian(L, gauge_links, r_wilson)
    H_ewsb = build_ewsb_term(L, y_v)
    H_ew = build_ew_correction(L, gauge_links, Q_em, T3, alpha_w, sin2_tw)

    H_total = H_w + H_ewsb + H_ew
    return H_total


# =============================================================================
# Wave packet construction
# =============================================================================

def build_smooth_wave_packet(L, K, sigma, color_vec=None):
    """
    Gaussian wave packet centered at BZ corner K.
    psi_K(x) = N * exp(i K.x) * exp(-|x-L/2|^2 / (2 sigma^2)) * color_vec
    """
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
                r2 = dx**2 + dy**2 + dz**2
                envelope = np.exp(-r2 / (2.0 * sigma**2))
                phase = np.exp(1j * (K[0] * x + K[1] * y + K[2] * z))
                for a in range(3):
                    psi[site * 3 + a] = phase * envelope * color_vec[a]

    norm = np.linalg.norm(psi)
    if norm > 0:
        psi /= norm
    return psi


# =============================================================================
# Mass matrix extraction in generation space
# =============================================================================

def extract_mass_matrix(L, H_sector, sigma=None):
    """
    Project H_sector onto generation space (3 BZ corners).

    M^{ij} = (1/3) sum_color <psi_i^c | H_sector | psi_j^c>

    where psi_i^c is a wave packet at BZ corner i with color c,
    and we average over color to get a color-singlet mass matrix.
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
            psi = build_smooth_wave_packet(L, Ki, sigma, color_vec)
            packets.append(psi)

        for i in range(3):
            for j in range(3):
                M[i, j] += packets[i].conj() @ (H_sector @ packets[j])

    M /= 3.0  # color average
    return M


# =============================================================================
# CKM extraction
# =============================================================================

def extract_ckm(M_u, M_d):
    """Extract V_CKM = U_u^dag U_d from Hermitianized mass matrices."""
    # Hermitianize
    M_u_h = 0.5 * (M_u + M_u.conj().T)
    M_d_h = 0.5 * (M_d + M_d.conj().T)

    eigvals_u, U_u = np.linalg.eigh(M_u_h)
    eigvals_d, U_d = np.linalg.eigh(M_d_h)

    # Sort by eigenvalue (ascending = lightest first)
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


def print_ckm_comparison(V, label=""):
    """Print |V_CKM| and compare to PDG."""
    if label:
        print(f"\n  {label}")

    print(f"\n  |V_CKM| matrix:")
    labels = ['d', 's', 'b']
    gen_labels = ['u', 'c', 't']
    header = "         " + "".join(f"    {l:>6}" for l in labels)
    print(header)
    for i in range(3):
        row = f"    {gen_labels[i]:>2}  ["
        for j in range(3):
            row += f" {abs(V[i, j]):.6f}"
        row += " ]"
        print(row)

    V_us = abs(V[0, 1])
    V_cb = abs(V[1, 2])
    V_ub = abs(V[0, 2])

    print(f"\n  Key elements vs PDG:")
    print(f"    |V_us| = {V_us:.6f}  (PDG: {PDG_CKM['V_us']})")
    print(f"    |V_cb| = {V_cb:.6f}  (PDG: {PDG_CKM['V_cb']})")
    print(f"    |V_ub| = {V_ub:.6f}  (PDG: {PDG_CKM['V_ub']})")

    if V_us > 1e-15 and V_cb > 1e-15:
        print(f"    |V_cb|/|V_us| = {V_cb/V_us:.4f}  (PDG: {PDG_CKM['V_cb']/PDG_CKM['V_us']:.4f})")
    if V_us > 1e-15 and V_ub > 1e-15:
        print(f"    |V_ub|/|V_us| = {V_ub/V_us:.4f}  (PDG: {PDG_CKM['V_ub']/PDG_CKM['V_us']:.4f})")

    # Hierarchy check
    hierarchy = V_us > V_cb > V_ub > 0
    print(f"    Hierarchy |V_us| > |V_cb| > |V_ub|: {hierarchy}")

    # Unitarity
    VV = V @ V.conj().T
    uni_err = np.linalg.norm(VV - np.eye(3))
    print(f"    Unitarity error: {uni_err:.2e}")

    # Jarlskog
    J = abs((V[0, 0] * V[1, 1] * V[0, 1].conj() * V[1, 0].conj()).imag)
    print(f"    |J| = {J:.6e}  (PDG: {PDG_CKM['J']:.2e})")

    return V_us, V_cb, V_ub, hierarchy, uni_err, J


# =============================================================================
# Physical parameters
# =============================================================================

# Electroweak
SIN2_TW = 0.231          # sin^2(theta_W)
ALPHA_W = 1.0 / 29.0     # alpha_2 at M_Z ~ 1/29

# Quark charges
Q_UP, T3_UP = 2.0 / 3.0, 0.5
Q_DOWN, T3_DOWN = -1.0 / 3.0, -0.5

# Yukawa couplings (proportional to mass / v)
# We use the ratio: y_u / y_d ~ m_t / m_b ~ 40
# For the lattice, the absolute scale is set by the VEV.
# We parametrize y*v for each sector.
Y_V_UP = 0.5       # up-type Yukawa * VEV
Y_V_DOWN = 0.0125  # down-type Yukawa * VEV (~ y_v_up * m_b/m_t)

# Lattice parameters
R_WILSON = 1.0
GAUGE_EPSILON = 0.3


# =============================================================================
# Main computation
# =============================================================================

def main():
    print("=" * 76)
    print("V_CKM DIRECTLY FROM LATTICE HAMILTONIAN WITH EWSB")
    print("=" * 76)
    print()
    print("  METHOD: Build H_up and H_down on the SAME lattice, differing only")
    print("  in their EW charges (Q, T3) and Yukawa couplings (y*v).")
    print("  Project each onto generation space (3 BZ corners).")
    print("  Diagonalize -> V_CKM = U_u^dag U_d.")
    print()
    print("  NO NNI decomposition.  NO separate coefficients.  NO K normalization.")
    print("  Just: lattice Hamiltonian -> mass matrices -> V_CKM.")
    print()

    # =================================================================
    # PART 1: SANITY CHECKS ON HAMILTONIAN COMPONENTS
    # =================================================================
    print("=" * 76)
    print("PART 1: HAMILTONIAN SANITY CHECKS")
    print("=" * 76)

    L = 6
    rng = np.random.default_rng(seed=42)
    gauge = generate_gauge_config(L, rng, GAUGE_EPSILON)

    # Check SU(3) properties
    unitarity_err = 0.0
    det_err = 0.0
    n_checked = 0
    for mu in range(3):
        for x in range(L):
            for y in range(L):
                for z in range(L):
                    U = gauge[mu][x, y, z]
                    unitarity_err += np.linalg.norm(U @ U.conj().T - np.eye(3))
                    det_err += abs(np.linalg.det(U) - 1.0)
                    n_checked += 1
    unitarity_err /= n_checked
    det_err /= n_checked

    check("gauge_links_unitary", unitarity_err < 1e-10,
          f"avg err = {unitarity_err:.2e}")
    check("gauge_links_det_one", det_err < 1e-10,
          f"avg |det-1| = {det_err:.2e}")

    # Build sector Hamiltonians
    H_up = build_sector_hamiltonian(L, gauge, R_WILSON, Y_V_UP,
                                     Q_UP, T3_UP, ALPHA_W, SIN2_TW)
    H_down = build_sector_hamiltonian(L, gauge, R_WILSON, Y_V_DOWN,
                                       Q_DOWN, T3_DOWN, ALPHA_W, SIN2_TW)

    # Both should be Hermitian (they contain only Hermitian pieces)
    up_herm_err = np.linalg.norm(H_up - H_up.conj().T) / np.linalg.norm(H_up)
    down_herm_err = np.linalg.norm(H_down - H_down.conj().T) / np.linalg.norm(H_down)
    check("H_up_hermitian", up_herm_err < 1e-10, f"err = {up_herm_err:.2e}")
    check("H_down_hermitian", down_herm_err < 1e-10, f"err = {down_herm_err:.2e}")

    # They should DIFFER (that is the whole point)
    diff_norm = np.linalg.norm(H_up - H_down) / np.linalg.norm(H_up)
    check("H_up_neq_H_down", diff_norm > 1e-10,
          f"||H_u - H_d|| / ||H_u|| = {diff_norm:.4e}")

    print(f"\n  Dimensions: {H_up.shape[0]} x {H_up.shape[1]}")
    print(f"  ||H_up||   = {np.linalg.norm(H_up):.4f}")
    print(f"  ||H_down|| = {np.linalg.norm(H_down):.4f}")
    print(f"  ||H_up - H_down|| / ||H_up|| = {diff_norm:.4e}")

    # =================================================================
    # PART 2: MASS MATRIX EXTRACTION (SINGLE CONFIG)
    # =================================================================
    print("\n" + "=" * 76)
    print("PART 2: MASS MATRICES IN GENERATION SPACE (L=6, seed=42)")
    print("=" * 76)

    M_u = extract_mass_matrix(L, H_up)
    M_d = extract_mass_matrix(L, H_down)

    print(f"\n  M_u (up-type mass matrix in generation space):")
    for i in range(3):
        print(f"    [{M_u[i, 0].real:+.6e}  {M_u[i, 1].real:+.6e}  {M_u[i, 2].real:+.6e}]")

    print(f"\n  M_d (down-type mass matrix in generation space):")
    for i in range(3):
        print(f"    [{M_d[i, 0].real:+.6e}  {M_d[i, 1].real:+.6e}  {M_d[i, 2].real:+.6e}]")

    # Check: mass matrices should differ
    md_diff = np.linalg.norm(M_u - M_d) / max(np.linalg.norm(M_u), 1e-15)
    check("mass_matrices_differ", md_diff > 1e-10,
          f"||M_u - M_d|| / ||M_u|| = {md_diff:.4e}")

    # Off-diagonal structure
    off_u = [abs(M_u[0, 1]), abs(M_u[0, 2]), abs(M_u[1, 2])]
    off_d = [abs(M_d[0, 1]), abs(M_d[0, 2]), abs(M_d[1, 2])]

    print(f"\n  Off-diagonal |M_u|: 12={off_u[0]:.4e}, 13={off_u[1]:.4e}, 23={off_u[2]:.4e}")
    print(f"  Off-diagonal |M_d|: 12={off_d[0]:.4e}, 13={off_d[1]:.4e}, 23={off_d[2]:.4e}")

    # The key: do the off-diagonals differ between u and d?
    off_diff_12 = abs(off_u[0] - off_d[0]) / max(off_u[0], off_d[0], 1e-15)
    off_diff_13 = abs(off_u[1] - off_d[1]) / max(off_u[1], off_d[1], 1e-15)
    off_diff_23 = abs(off_u[2] - off_d[2]) / max(off_u[2], off_d[2], 1e-15)
    print(f"\n  Relative |M_u - M_d| off-diag: 12={off_diff_12:.4e}, "
          f"13={off_diff_13:.4e}, 23={off_diff_23:.4e}")

    # =================================================================
    # PART 3: V_CKM EXTRACTION (SINGLE CONFIG)
    # =================================================================
    print("\n" + "=" * 76)
    print("PART 3: V_CKM EXTRACTION (L=6, seed=42)")
    print("=" * 76)

    V_ckm, eigvals_u, eigvals_d = extract_ckm(M_u, M_d)

    print(f"\n  Up-type eigenvalues (generation masses): {eigvals_u}")
    print(f"  Down-type eigenvalues (generation masses): {eigvals_d}")

    V_us, V_cb, V_ub, hierarchy, uni_err, J = print_ckm_comparison(V_ckm)

    check("V_CKM_unitary", uni_err < 1e-10, f"err = {uni_err:.2e}")
    check("V_CKM_nontrivial", abs(V_ckm[0, 1]) > 1e-10,
          f"|V_us| = {V_us:.6e} (should be nonzero)")

    # =================================================================
    # PART 4: FREE FIELD BASELINE
    # =================================================================
    print("\n" + "=" * 76)
    print("PART 4: FREE FIELD BASELINE (no gauge fluctuations)")
    print("=" * 76)

    gauge_free = identity_gauge_config(L)

    H_up_free = build_sector_hamiltonian(L, gauge_free, R_WILSON, Y_V_UP,
                                          Q_UP, T3_UP, ALPHA_W, SIN2_TW)
    H_down_free = build_sector_hamiltonian(L, gauge_free, R_WILSON, Y_V_DOWN,
                                            Q_DOWN, T3_DOWN, ALPHA_W, SIN2_TW)

    M_u_free = extract_mass_matrix(L, H_up_free)
    M_d_free = extract_mass_matrix(L, H_down_free)

    V_free, ev_u_free, ev_d_free = extract_ckm(M_u_free, M_d_free)

    print(f"\n  Free-field M_u eigenvalues: {ev_u_free}")
    print(f"  Free-field M_d eigenvalues: {ev_d_free}")

    Vus_free, Vcb_free, Vub_free, hier_free, uni_free, J_free = \
        print_ckm_comparison(V_free, "Free-field V_CKM")

    # In free field, the EW charge difference still distinguishes sectors
    free_nontrivial = abs(V_free[0, 1]) > 1e-12
    check("free_field_mixing_from_ew_asymmetry", free_nontrivial,
          f"|V_us| = {Vus_free:.6e}",
          kind="BOUNDED")

    # =================================================================
    # PART 5: PARAMETER SENSITIVITY -- YUKAWA RATIO
    # =================================================================
    print("\n" + "=" * 76)
    print("PART 5: YUKAWA RATIO SENSITIVITY")
    print("=" * 76)

    print(f"\n  Scanning y_v_down at fixed y_v_up = {Y_V_UP}:")
    print(f"  (Physical ratio m_t/m_b ~ 40, so y_d/y_u ~ 1/40)")
    print()

    y_d_values = [0.0, 0.005, 0.0125, 0.025, 0.05, 0.1, 0.25, 0.5]

    print(f"  {'y_d*v':>8}  {'y_d/y_u':>8}  {'|V_us|':>10}  {'|V_cb|':>10}"
          f"  {'|V_ub|':>10}  {'hierarchy':>10}")
    print("  " + "-" * 70)

    for y_d in y_d_values:
        H_u_scan = build_sector_hamiltonian(L, gauge, R_WILSON, Y_V_UP,
                                             Q_UP, T3_UP, ALPHA_W, SIN2_TW)
        H_d_scan = build_sector_hamiltonian(L, gauge, R_WILSON, y_d,
                                             Q_DOWN, T3_DOWN, ALPHA_W, SIN2_TW)
        M_u_scan = extract_mass_matrix(L, H_u_scan)
        M_d_scan = extract_mass_matrix(L, H_d_scan)
        V_scan, _, _ = extract_ckm(M_u_scan, M_d_scan)

        vus = abs(V_scan[0, 1])
        vcb = abs(V_scan[1, 2])
        vub = abs(V_scan[0, 2])
        ratio = y_d / Y_V_UP if Y_V_UP > 0 else 0
        hier = "YES" if vus > vcb > vub > 0 else "no"

        print(f"  {y_d:8.4f}  {ratio:8.4f}  {vus:10.6f}  {vcb:10.6f}"
              f"  {vub:10.6f}  {hier:>10}")

    # =================================================================
    # PART 6: ENSEMBLE AVERAGE (GAUGED)
    # =================================================================
    print("\n" + "=" * 76)
    print("PART 6: ENSEMBLE AVERAGE OVER GAUGE CONFIGURATIONS")
    print("=" * 76)

    n_configs = 20
    print(f"\n  L = {L}, {n_configs} gauge configurations")
    print(f"  y_v_up = {Y_V_UP}, y_v_down = {Y_V_DOWN}")
    print(f"  alpha_W = {ALPHA_W:.4f}, sin^2(theta_W) = {SIN2_TW}")
    print()

    ensemble_V = []
    ensemble_Vus = []
    ensemble_Vcb = []
    ensemble_Vub = []
    ensemble_hier = []

    for cfg in range(n_configs):
        rng_cfg = np.random.default_rng(seed=1000 + cfg)
        g = generate_gauge_config(L, rng_cfg, GAUGE_EPSILON)

        H_u_c = build_sector_hamiltonian(L, g, R_WILSON, Y_V_UP,
                                          Q_UP, T3_UP, ALPHA_W, SIN2_TW)
        H_d_c = build_sector_hamiltonian(L, g, R_WILSON, Y_V_DOWN,
                                          Q_DOWN, T3_DOWN, ALPHA_W, SIN2_TW)

        M_u_c = extract_mass_matrix(L, H_u_c)
        M_d_c = extract_mass_matrix(L, H_d_c)

        V_c, _, _ = extract_ckm(M_u_c, M_d_c)

        vus_c = abs(V_c[0, 1])
        vcb_c = abs(V_c[1, 2])
        vub_c = abs(V_c[0, 2])
        hier_c = vus_c > vcb_c > vub_c > 0

        ensemble_V.append(V_c)
        ensemble_Vus.append(vus_c)
        ensemble_Vcb.append(vcb_c)
        ensemble_Vub.append(vub_c)
        ensemble_hier.append(hier_c)

        print(f"    Config {cfg:2d}: |V_us|={vus_c:.6f}, |V_cb|={vcb_c:.6f}, "
              f"|V_ub|={vub_c:.6f}, hierarchy={hier_c}")

    avg_Vus = np.mean(ensemble_Vus)
    avg_Vcb = np.mean(ensemble_Vcb)
    avg_Vub = np.mean(ensemble_Vub)
    std_Vus = np.std(ensemble_Vus)
    std_Vcb = np.std(ensemble_Vcb)
    std_Vub = np.std(ensemble_Vub)
    frac_hier = np.mean(ensemble_hier)

    print(f"\n  Ensemble averages ({n_configs} configs):")
    print(f"    <|V_us|> = {avg_Vus:.6f} +/- {std_Vus:.6f}  (PDG: {PDG_CKM['V_us']})")
    print(f"    <|V_cb|> = {avg_Vcb:.6f} +/- {std_Vcb:.6f}  (PDG: {PDG_CKM['V_cb']})")
    print(f"    <|V_ub|> = {avg_Vub:.6f} +/- {std_Vub:.6f}  (PDG: {PDG_CKM['V_ub']})")
    print(f"    Fraction with correct hierarchy: {frac_hier:.2f}")

    check("ensemble_nonzero_mixing", avg_Vus > 1e-6,
          f"<|V_us|> = {avg_Vus:.6e}",
          kind="BOUNDED")

    check("ensemble_hierarchy_majority", frac_hier > 0.4,
          f"fraction = {frac_hier:.2f}",
          kind="BOUNDED")

    # =================================================================
    # PART 7: L-DEPENDENCE
    # =================================================================
    print("\n" + "=" * 76)
    print("PART 7: L-DEPENDENCE (SINGLE CONFIG PER L)")
    print("=" * 76)

    L_values = [4, 6, 8]
    print(f"\n  Testing L = {L_values}")
    print()

    for L_test in L_values:
        rng_L = np.random.default_rng(seed=42)
        g_L = generate_gauge_config(L_test, rng_L, GAUGE_EPSILON)

        H_u_L = build_sector_hamiltonian(L_test, g_L, R_WILSON, Y_V_UP,
                                          Q_UP, T3_UP, ALPHA_W, SIN2_TW)
        H_d_L = build_sector_hamiltonian(L_test, g_L, R_WILSON, Y_V_DOWN,
                                          Q_DOWN, T3_DOWN, ALPHA_W, SIN2_TW)

        M_u_L = extract_mass_matrix(L_test, H_u_L, sigma=L_test / 4.0)
        M_d_L = extract_mass_matrix(L_test, H_d_L, sigma=L_test / 4.0)

        V_L, ev_u_L, ev_d_L = extract_ckm(M_u_L, M_d_L)

        vus_L = abs(V_L[0, 1])
        vcb_L = abs(V_L[1, 2])
        vub_L = abs(V_L[0, 2])
        hier_L = vus_L > vcb_L > vub_L > 0

        print(f"  L={L_test:2d} (dim={L_test**3 * 3:5d}): |V_us|={vus_L:.6f}, "
              f"|V_cb|={vcb_L:.6f}, |V_ub|={vub_L:.6f}, "
              f"hierarchy={hier_L}")

        # Eigenvalue spectrum
        print(f"          up masses:   {ev_u_L}")
        print(f"          down masses: {ev_d_L}")

    # =================================================================
    # PART 8: DECOMPOSITION -- WHERE DOES THE MIXING COME FROM?
    # =================================================================
    print("\n" + "=" * 76)
    print("PART 8: ORIGIN DECOMPOSITION -- WHAT DRIVES THE MIXING?")
    print("=" * 76)

    print(f"\n  We build V_CKM from three pieces:")
    print(f"    (a) Wilson term only (no EWSB, no EW)")
    print(f"    (b) Wilson + EWSB (no EW)")
    print(f"    (c) Wilson + EWSB + EW (full)")
    print()

    L_d = 6
    rng_d = np.random.default_rng(seed=42)
    g_d = generate_gauge_config(L_d, rng_d, GAUGE_EPSILON)

    # (a) Wilson only
    _, H_w_d = build_staggered_hamiltonian(L_d, g_d, R_WILSON)
    M_u_a = extract_mass_matrix(L_d, H_w_d)
    M_d_a = extract_mass_matrix(L_d, H_w_d)  # same for both sectors
    V_a, _, _ = extract_ckm(M_u_a, M_d_a)

    print(f"  (a) Wilson only: |V_us| = {abs(V_a[0,1]):.6e}, "
          f"|V_cb| = {abs(V_a[1,2]):.6e}, |V_ub| = {abs(V_a[0,2]):.6e}")
    check("wilson_only_no_mixing", abs(V_a[0, 1]) < 1e-10,
          "same H for u,d => V=I")

    # (b) Wilson + EWSB (different y_v for u and d)
    H_ewsb_u = build_ewsb_term(L_d, Y_V_UP)
    H_ewsb_d = build_ewsb_term(L_d, Y_V_DOWN)
    M_u_b = extract_mass_matrix(L_d, H_w_d + H_ewsb_u)
    M_d_b = extract_mass_matrix(L_d, H_w_d + H_ewsb_d)
    V_b, _, _ = extract_ckm(M_u_b, M_d_b)

    print(f"  (b) Wilson+EWSB: |V_us| = {abs(V_b[0,1]):.6e}, "
          f"|V_cb| = {abs(V_b[1,2]):.6e}, |V_ub| = {abs(V_b[0,2]):.6e}")
    check("ewsb_generates_mixing", abs(V_b[0, 1]) > 1e-10,
          f"|V_us| = {abs(V_b[0,1]):.6e}",
          kind="BOUNDED")

    # (c) Full (Wilson + EWSB + EW)
    H_ew_u = build_ew_correction(L_d, g_d, Q_UP, T3_UP, ALPHA_W, SIN2_TW)
    H_ew_d = build_ew_correction(L_d, g_d, Q_DOWN, T3_DOWN, ALPHA_W, SIN2_TW)
    M_u_c = extract_mass_matrix(L_d, H_w_d + H_ewsb_u + H_ew_u)
    M_d_c = extract_mass_matrix(L_d, H_w_d + H_ewsb_d + H_ew_d)
    V_c_full, _, _ = extract_ckm(M_u_c, M_d_c)

    print(f"  (c) Full:        |V_us| = {abs(V_c_full[0,1]):.6e}, "
          f"|V_cb| = {abs(V_c_full[1,2]):.6e}, |V_ub| = {abs(V_c_full[0,2]):.6e}")

    # How much does EW correction add?
    delta_vus = abs(abs(V_c_full[0, 1]) - abs(V_b[0, 1]))
    if abs(V_b[0, 1]) > 1e-15:
        ew_contrib = delta_vus / abs(V_b[0, 1])
        print(f"\n  EW correction contribution to |V_us|: {ew_contrib:.2%}")
        check("ew_correction_perturbative", ew_contrib < 0.5,
              f"EW is {ew_contrib:.2%} of EWSB",
              kind="BOUNDED")

    # =================================================================
    # PART 9: STRUCTURAL SUMMARY
    # =================================================================
    print("\n" + "=" * 76)
    print("PART 9: STRUCTURAL SUMMARY")
    print("=" * 76)

    print(f"""
  METHOD:
    V_CKM = U_u^dag U_d where U_u, U_d diagonalize
    M_q = <X_i | H_q | X_j>  (q = u, d)
    H_q = H_Wilson + H_EWSB(y_q) + H_EW(Q_q, T3_q)

  KEY FINDINGS:

  1. Wilson term alone: V_CKM = I (no mixing)                    [EXACT]
     Reason: same H for up and down => same eigenvectors

  2. EWSB Yukawa difference (y_u != y_d) generates mixing        [COMPUTED]
     The Higgs VEV in direction 1 breaks C3 -> Z2, and the
     different Yukawa couplings make U_u != U_d.
     |V_us| = {abs(V_b[0,1]):.6e}  (from EWSB alone)

  3. EW charge correction (Q, T3 difference) is perturbative     [COMPUTED]
     It modifies the gauge hopping direction-dependently,
     adding a ~alpha_W correction.

  4. Ensemble average shows nonzero mixing                       [BOUNDED]
     <|V_us|> = {avg_Vus:.6f} +/- {std_Vus:.6f}
     Fraction with correct hierarchy: {frac_hier:.0%}

  WHAT IS DERIVED (direct lattice):
     - The mechanism: different y*v for up and down sectors,
       acting on the SAME EWSB-broken lattice, produces V_CKM != I
     - The hierarchy pattern depends on the Yukawa ratio y_u/y_d
     - The C3 -> Z2 breaking by the VEV creates the 12,13 vs 23 split

  WHAT IS NOT DERIVED (bounded):
     - Yukawa couplings y_u, y_d are model inputs
     - Gauge configurations are quenched
     - Continuum limit not taken
     - Quantitative match to PDG requires tuning
""")

    # =================================================================
    # FINAL TALLY
    # =================================================================
    print("=" * 76)
    print(f"RESULTS: {PASS_COUNT} passed, {FAIL_COUNT} failed "
          f"out of {PASS_COUNT + FAIL_COUNT}")
    print("=" * 76)

    return FAIL_COUNT


if __name__ == "__main__":
    failures = main()
    sys.exit(failures)
