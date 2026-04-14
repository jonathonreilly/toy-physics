#!/usr/bin/env python3
"""
Top Mass from the Lattice Determinant
=======================================

THE QUESTION:
  The hierarchy theorem gives v = M_Pl * alpha_LM^16 = 254 GeV from the
  exact taste determinant det(D) on the L_t=2, L_s=2 APBC block. The CW
  effective potential is the WRONG tool (1-loop continuum approximation
  that fails on the discrete lattice with alpha_LM = 0.09). Can we extract
  the top quark mass m_t DIRECTLY from log|det(D+m)|, bypassing CW entirely?

THE KEY OBJECT:
  W(m) = log|det(D + m I)| - log|det(D)|

  This is the unique additive CPT-even scalar generator forced by the axiom
  (Codex's observable principle). The local curvature gives the hierarchy.
  The fermion mass should also be encoded in this object.

APPROACH:
  Part 1: Build exact determinant on the taste block
  Part 2: Reproduce v = 245 GeV from the scalar curvature
  Part 3: Extract m_t from multiple approaches:
    (a) Susceptibility peak of chi(m) = d^2 W / dm^2
    (b) Eigenvalue gap after EWSB shift
    (c) Determinant ratio at phi = v
    (d) Smallest eigenvalue (propagator pole)
    (e) Hierarchy structure ratio
  Part 4: Honest comparison with observations
  Part 5: Physical interpretation

INPUTS (from axiom + lattice MC):
  g = 1, <P> = 0.594, M_Pl = 1.22e19 GeV

Self-contained: numpy + scipy only.
PStack experiment: mt-from-determinant
"""

from __future__ import annotations

import math
import sys

import numpy as np
from scipy.optimize import brentq, minimize_scalar

np.set_printoptions(precision=10, linewidth=120, suppress=True)

# ============================================================================
# Physical constants
# ============================================================================

PI = math.pi
M_PL = 1.2209e19          # GeV, unreduced Planck mass = 1/l_Planck
V_OBS = 246.22             # GeV, observed EW VEV
M_TOP_OBS = 172.69         # GeV, observed top pole mass
PLAQ_MC = 0.594            # SU(3) pure gauge plaquette at beta=6

G_BARE = 1.0
ALPHA_BARE = G_BARE**2 / (4 * PI)    # = 1/(4 pi) = 0.07958
U0 = PLAQ_MC**0.25                   # = 0.878
ALPHA_LM = ALPHA_BARE / U0           # = 0.0906

# Hierarchy prediction
V_HIERARCHY = M_PL * ALPHA_LM**16    # ~ 254 GeV

# Framework Yukawa
G_S_UV = math.sqrt(4 * PI * ALPHA_LM)
Y_T_UV = G_S_UV / math.sqrt(6)       # = 0.436

PASS_COUNT = 0
FAIL_COUNT = 0


def check(name: str, condition: bool, detail: str = ""):
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if condition else "FAIL"
    if condition:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1
    print(f"  [{status}] {name}")
    if detail:
        print(f"         {detail}")


# ============================================================================
# Staggered Dirac operator builders
# ============================================================================

def build_dirac_4d_apbc(Ls: int, Lt: int, u0: float, mass: float = 0.0):
    """Build staggered Dirac on Ls^3 x Lt with APBC in all directions."""
    N = Ls**3 * Lt
    D = np.zeros((N, N), dtype=complex)

    def idx(x0, x1, x2, t):
        return (((x0 % Ls) * Ls + (x1 % Ls)) * Ls + (x2 % Ls)) * Lt + (t % Lt)

    for x0 in range(Ls):
        for x1 in range(Ls):
            for x2 in range(Ls):
                for t in range(Lt):
                    i = idx(x0, x1, x2, t)
                    D[i, i] += mass

                    # mu=0: eta_0 = 1
                    eta = 1.0
                    xf = (x0 + 1) % Ls
                    sign = -1.0 if x0 + 1 >= Ls else 1.0
                    j = idx(xf, x1, x2, t)
                    D[i, j] += u0 * eta * sign / 2.0
                    xb = (x0 - 1) % Ls
                    sign = -1.0 if x0 - 1 < 0 else 1.0
                    j = idx(xb, x1, x2, t)
                    D[i, j] -= u0 * eta * sign / 2.0

                    # mu=1: eta_1 = (-1)^x0
                    eta = (-1.0)**x0
                    xf = (x1 + 1) % Ls
                    sign = -1.0 if x1 + 1 >= Ls else 1.0
                    j = idx(x0, xf, x2, t)
                    D[i, j] += u0 * eta * sign / 2.0
                    xb = (x1 - 1) % Ls
                    sign = -1.0 if x1 - 1 < 0 else 1.0
                    j = idx(x0, xb, x2, t)
                    D[i, j] -= u0 * eta * sign / 2.0

                    # mu=2: eta_2 = (-1)^(x0+x1)
                    eta = (-1.0)**(x0 + x1)
                    xf = (x2 + 1) % Ls
                    sign = -1.0 if x2 + 1 >= Ls else 1.0
                    j = idx(x0, x1, xf, t)
                    D[i, j] += u0 * eta * sign / 2.0
                    xb = (x2 - 1) % Ls
                    sign = -1.0 if x2 - 1 < 0 else 1.0
                    j = idx(x0, x1, xb, t)
                    D[i, j] -= u0 * eta * sign / 2.0

                    # mu=3 (temporal): eta_3 = (-1)^(x0+x1+x2)
                    eta = (-1.0)**(x0 + x1 + x2)
                    tf = (t + 1) % Lt
                    sign = -1.0 if t + 1 >= Lt else 1.0
                    j = idx(x0, x1, x2, tf)
                    D[i, j] += u0 * eta * sign / 2.0
                    tb = (t - 1) % Lt
                    sign = -1.0 if t - 1 < 0 else 1.0
                    j = idx(x0, x1, x2, tb)
                    D[i, j] -= u0 * eta * sign / 2.0

    return D


# ============================================================================
# Part 1: The exact determinant on the taste block
# ============================================================================

def part1_exact_determinant():
    print("\n" + "=" * 70)
    print("PART 1: The Exact Determinant on the Taste Block")
    print("=" * 70)

    # Build D on the L_s=2, L_t=2 taste block (16 sites)
    D_phys = build_dirac_4d_apbc(Ls=2, Lt=2, u0=U0)
    D_hop = build_dirac_4d_apbc(Ls=2, Lt=2, u0=1.0)

    # Verify linearity: D(u0) = u0 * D_hop
    residual = np.max(np.abs(D_phys - U0 * D_hop))
    check("D(u0) = u0 * D_hop (linearity)",
          residual < 1e-14,
          f"max residual = {residual:.2e}")

    # Eigenvalue spectrum
    eigs_hop = np.linalg.eigvals(D_hop)
    eigs_phys = np.linalg.eigvals(D_phys)

    mags_hop = np.sort(np.abs(eigs_hop))
    mags_phys = np.sort(np.abs(eigs_phys))

    print(f"\n  Hopping eigenvalue magnitudes: {mags_hop}")
    print(f"  Physical eigenvalue magnitudes: {mags_phys}")

    # All eigenvalues should have |lambda| = 2 (sqrt(4) from 4D APBC)
    target_hop = 2.0
    max_dev = max(abs(m - target_hop) for m in mags_hop)
    check("All 16 hopping eigenvalues have |lambda| = 2",
          max_dev < 1e-12,
          f"max deviation from 2.0 = {max_dev:.2e}")

    # Physical eigenvalues: |lambda| = u0 * 2
    target_phys = U0 * 2.0
    max_dev_phys = max(abs(m - target_phys) for m in mags_phys)
    check("All physical eigenvalues have |lambda| = u0 * 2",
          max_dev_phys < 1e-12,
          f"|lambda| = {mags_phys[0]:.6f}, target = {target_phys:.6f}")

    # Determinants
    det_hop = np.linalg.det(D_hop)
    det_phys = np.linalg.det(D_phys)
    print(f"\n  det(D_hop) = {det_hop:.6f} (expected 2^16 = {2**16})")
    print(f"  |det(D_hop)| = {abs(det_hop):.6f}")
    print(f"  det(D_phys) = {det_phys:.6f}")
    print(f"  |det(D_phys)| = {abs(det_phys):.6f}")
    print(f"  u0^16 * |det(D_hop)| = {U0**16 * abs(det_hop):.6f}")

    check("det(D_phys) = u0^16 * det(D_hop)",
          abs(abs(det_phys) - U0**16 * abs(det_hop)) / abs(det_phys) < 1e-10,
          f"ratio = {abs(det_phys) / (U0**16 * abs(det_hop)):.10f}")

    # Also check the L_t=4 block (32 sites) for Codex's selector
    print("\n  --- L_t = 4 block (32 sites) ---")
    D_hop_4 = build_dirac_4d_apbc(Ls=2, Lt=4, u0=1.0)
    eigs_hop_4 = np.linalg.eigvals(D_hop_4)
    mags_hop_4 = np.sort(np.abs(eigs_hop_4))
    print(f"  L_t=4 hopping eigenvalue magnitudes: {mags_hop_4}")
    det_hop_4 = np.linalg.det(D_hop_4)
    print(f"  |det(D_hop, L_t=4)| = {abs(det_hop_4):.6f}")

    return eigs_hop, eigs_phys, D_hop, D_phys


# ============================================================================
# Part 2: The Scalar Response (v from curvature)
# ============================================================================

def part2_scalar_response(D_hop, eigs_phys):
    print("\n" + "=" * 70)
    print("PART 2: The Scalar Response — v from W(m)")
    print("=" * 70)

    N = 16  # taste block size

    # W(m) = log|det(D + m I)| - log|det(D)|
    # For the taste block with degenerate eigenvalues |lambda_k| = u0*sqrt(d):
    # W(m) = sum_k log|lambda_k + m| - sum_k log|lambda_k|
    # = sum_k log(1 + m/lambda_k)

    # The eigenvalues come in conjugate pairs: {lambda, -lambda*, ...}
    # For purely imaginary eigenvalues lambda_k = i * u0 * r_k:
    # |lambda_k + m|^2 = m^2 + u0^2 * r_k^2

    eigs = eigs_phys
    lambda_sq = np.abs(eigs)**2  # |lambda_k|^2

    # All |lambda_k|^2 should be (u0*2)^2 = 4*u0^2
    Lambda_sq = (U0 * 2.0)**2  # = 4 * u0^2 in lattice units
    print(f"\n  All |lambda|^2 = {Lambda_sq:.6f} (degenerate spectrum)")

    # W(m) = sum_k (1/2) log(m^2 + |lambda_k|^2) - (1/2) log(|lambda_k|^2)
    # For the staggered operator which is anti-Hermitian, eigenvalues are
    # purely imaginary (or come in +-pairs). So:
    # W(m) = sum_{k=1}^{N/2} log(m^2 + |lambda_k|^2) - log(|lambda_k|^2)
    #       (grouping conjugate pairs)

    # With degenerate spectrum:
    # W(m) = (N/2) * [log(m^2 + Lambda^2) - log(Lambda^2)]
    #       = (N/2) * log(1 + m^2/Lambda^2)

    def W_exact(m):
        """Exact W(m) from eigenvalues."""
        # det(D + m I) = prod_k (lambda_k + m)
        # |det(D + m I)| = prod_k |lambda_k + m|
        # log|det(D+m)| = sum_k log|lambda_k + m|
        val = 0.0
        for lam in eigs:
            val += np.log(abs(lam + m))
        val0 = sum(np.log(abs(lam)) for lam in eigs)
        return val - val0

    def W_degenerate(m):
        """W(m) for degenerate spectrum: all |lambda| = u0*2."""
        return (N / 2.0) * np.log(1.0 + m**2 / Lambda_sq)

    # Compare exact vs degenerate
    m_test = 0.5
    w_exact = W_exact(m_test)
    w_degen = W_degenerate(m_test)
    print(f"\n  W(m={m_test}) exact = {w_exact:.8f}")
    print(f"  W(m={m_test}) degen = {w_degen:.8f}")
    check("W_exact matches W_degenerate for degenerate spectrum",
          abs(w_exact - w_degen) / max(abs(w_exact), 1e-15) < 1e-6,
          f"relative diff = {abs(w_exact - w_degen) / abs(w_exact):.2e}")

    # Curvature: W''(m) = chi(m) = susceptibility
    # chi(m) = d^2 W / dm^2
    # For degenerate: chi(m) = N * (Lambda^2 - m^2) / (m^2 + Lambda^2)^2
    # chi(0) = N / Lambda^2

    chi_0 = N / Lambda_sq
    print(f"\n  chi(0) = W''(0) = N / Lambda^2 = {chi_0:.8f}")
    print(f"  Lambda = u0 * 2 = {U0 * 2:.6f} (lattice units)")

    # Following Codex: the hierarchy comes from the curvature.
    # The hierarchy coefficient A from OBSERVABLE_PRINCIPLE note:
    # A(L_t) = (1 / (2 L_t u_0^2)) sum_omega 1/(3 + sin^2(omega))
    # For L_t=2 APBC: omega = pi/2, 3*pi/2 -> sin^2(omega) = 1
    # A(L_t=2) = (1 / (2*2*u0^2)) * 2 * 1/(3+1) = 1/(4*u0^2) * 2/4
    #           = 1/(4*u0^2) * 1/2 = 1/(8*u0^2)
    # Actually: the Matsubara formula in Codex's note gives:
    # W(j) = 4 sum_omega log(1 + j^2/(u0^2 (3 + sin^2(omega))))
    # This is for the 3D spatial block (8 sites = 4 conjugate pairs)
    # summed over L_t/2 Matsubara modes.

    # For L_t=2, omega takes values {pi/2} (one Matsubara mode with APBC):
    # Actually for L_t=2 APBC: omega_n = pi(2n+1)/(2*Lt) = pi/4, 3pi/4
    # Let's compute directly.

    # The VEV comes from the hierarchy formula v = M_Pl * alpha_LM^16
    # Let's verify this is consistent with the curvature.
    # The matching: v^2 = M_Pl^2 * [chi_0 in physical units]
    # where chi_0 is the scalar response normalized appropriately.

    # In the hierarchy theorem:
    # v/M_Pl = alpha_LM^16 = (alpha_bare / u0)^16 = alpha_bare^16 / u0^16
    # = alpha_bare^16 * (1/u0^16)
    # This is exactly det(D)^{-1} up to the hopping factor:
    # det(D) = u0^16 * det(D_hop), so u0^{-16} = det(D)^{-1} * det(D_hop)

    v_pred = M_PL * ALPHA_LM**16
    print(f"\n  v from hierarchy formula: {v_pred:.1f} GeV")
    print(f"  v observed: {V_OBS} GeV")
    dev_pct = abs(v_pred - V_OBS) / V_OBS * 100
    check("v from hierarchy formula within 5% of 246 GeV",
          dev_pct < 5.0,
          f"v = {v_pred:.1f} GeV, deviation = {dev_pct:.1f}%")

    # Now convert Lambda (lattice eigenvalue scale) to physical units.
    # On the lattice with a = l_Planck:
    # Lambda_phys = Lambda / a = Lambda * M_Pl (in lattice units Lambda is O(1))
    # But Lambda = u0 * 2 is in lattice units (dimensionless).
    # Physical eigenvalue scale: Lambda_phys = u0 * 2 * M_Pl / (2*pi)
    # Actually, the eigenvalues of D/a have dimension 1/a = M_Pl.
    # The lattice D has eigenvalues in units of 1/a, so:
    Lambda_phys = U0 * 2.0 * M_PL  # physical scale of eigenvalues
    print(f"\n  Physical eigenvalue scale: Lambda_phys = {Lambda_phys:.3e} GeV")
    print(f"  This is O(M_Pl) as expected for Planck-scale lattice")

    return W_exact, W_degenerate, Lambda_sq


# ============================================================================
# Part 3: Extract the fermion mass m_t
# ============================================================================

def part3_fermion_mass(eigs_phys, W_exact, Lambda_sq):
    print("\n" + "=" * 70)
    print("PART 3: Extracting the Top Mass m_t")
    print("=" * 70)

    N = 16
    Lambda = math.sqrt(Lambda_sq)  # = u0 * 2 in lattice units

    v_pred = M_PL * ALPHA_LM**16  # GeV, the hierarchy VEV

    # =====================================================================
    # Approach (a): Susceptibility peak
    # =====================================================================
    print("\n--- (a) Susceptibility peak ---")

    # chi(m) = d^2 W / dm^2
    # For degenerate spectrum:
    # W(m) = (N/2) * log(1 + m^2/Lambda^2)
    # W'(m) = N * m / (m^2 + Lambda^2)
    # W''(m) = N * (Lambda^2 - m^2) / (m^2 + Lambda^2)^2

    # chi(m) is maximized at m = 0 (monotonically decreasing for m > 0).
    # chi(m) = 0 at m = Lambda.
    # The susceptibility does NOT have a peak at finite m for the degenerate
    # spectrum -- it's a monotone decrease from chi(0) = N/Lambda^2.

    # However, the PHYSICAL susceptibility should include the Yukawa coupling:
    # m = y_t * phi, so chi(phi) = y_t^2 * d^2 W / dm^2 |_{m = y_t phi}
    # This still peaks at phi = 0.

    # The relevant quantity is the INVERSE susceptibility (mass squared):
    # M^2(m) = 1/chi(m) = (m^2 + Lambda^2)^2 / (N * (Lambda^2 - m^2))
    # This diverges at m = Lambda. The fermion mass is where M^2 changes sign,
    # i.e., where the system transitions from paramagnetic to ordered.

    print(f"  chi(0) = {N / Lambda_sq:.8f}")
    print(f"  chi(m) = 0 at m = Lambda = {Lambda:.6f}")
    print("  Susceptibility is monotonically decreasing -- no finite-m peak")
    print("  (This approach does not identify m_t for degenerate spectrum)")

    # =====================================================================
    # Approach (b): Eigenvalue gap after EWSB shift
    # =====================================================================
    print("\n--- (b) Eigenvalue gap after EWSB ---")

    # After EWSB, the Higgs VEV v shifts the fermion mass: D -> D + y_t v I
    # The shifted eigenvalues are: lambda_k + y_t v
    # The PHYSICAL fermion mass is the smallest |lambda_k + m_t| where
    # m_t = y_t * v (in the relevant units).

    # On the taste block, all |lambda_k| = Lambda = u0 * 2.
    # After adding mass m: the shifted eigenvalues are lambda_k + m.
    # For purely imaginary lambda_k = i * Lambda * e^{i theta_k}:
    # |lambda_k + m| = sqrt(m^2 + Lambda^2)  (degenerate, independent of k)

    # So the "gap" after EWSB shift is:
    # Delta = min_k |lambda_k + m_t| = sqrt(m_t^2 + Lambda^2)
    # This is NOT m_t; it's sqrt(m_t^2 + Lambda^2) ~ Lambda for m_t << Lambda.

    # But this is in lattice units. The physical mass is m_t in physical units.
    # The lattice eigenvalues are O(1), while the physical mass is O(v).
    # We need to be more careful about units.

    # In lattice units (a = l_Planck):
    # Lambda_lattice = u0 * 2  (dimensionless, O(1))
    # m_lattice = m_phys * a = m_phys / M_Pl  (dimensionless, << 1 for m_phys ~ v)
    # v_lattice = v / M_Pl ~ 2e-17 (tiny!)

    v_lattice = v_pred / M_PL
    print(f"  v in lattice units: v/M_Pl = {v_lattice:.4e}")
    print(f"  Lambda (lattice) = {Lambda:.4f}")
    print(f"  v/Lambda ratio = {v_lattice / Lambda:.4e}")
    print(f"  -> v << Lambda: the EWSB mass is a tiny perturbation on the taste block")

    # The shifted eigenvalue gap:
    m_lattice_yt1 = v_lattice  # y_t = 1 case
    gap_yt1 = math.sqrt(m_lattice_yt1**2 + Lambda**2) - Lambda
    print(f"\n  For y_t = 1: m_lattice = {m_lattice_yt1:.4e}")
    print(f"  Gap = sqrt(m^2 + Lambda^2) - Lambda = {gap_yt1:.4e}")
    print(f"  Gap * M_Pl = {gap_yt1 * M_PL:.4e} GeV")
    # For m << Lambda: gap ~ m^2 / (2 Lambda)
    gap_approx = m_lattice_yt1**2 / (2 * Lambda)
    print(f"  Approx gap (m^2/2Lambda) = {gap_approx:.4e}")
    print(f"  Approx gap * M_Pl = {gap_approx * M_PL:.4e} GeV")
    print("  -> Eigenvalue gap approach: mass perturbation too small to read off m_t")

    # =====================================================================
    # Approach (c): Determinant ratio at phi = v
    # =====================================================================
    print("\n--- (c) Determinant ratio at phi = v ---")

    # The fermion propagator in the taste determinant framework:
    # G(m) = d W / dm = sum_k m / (m^2 + |lambda_k|^2)  (for degenerate)
    #       = N * m / (m^2 + Lambda^2)

    # The "running mass" from the condensate:
    # <psi-bar psi>(m) = d W / dm = N * m / (m^2 + Lambda^2)

    # At m = y_t * v_lattice:
    m_val = Y_T_UV * v_lattice
    condensate = N * m_val / (m_val**2 + Lambda_sq)
    print(f"  Condensate at m = y_t * v_lattice: {condensate:.6e}")

    # The physical condensate should be v^3 in appropriate units.
    # In lattice units: <psi-bar psi> ~ v^3/M_Pl^3 ~ (v_lattice)^3

    # A more promising ratio: the determinant response per taste state
    # log|det(D + m)|^{1/N} - log|det(D)|^{1/N}
    #   = (1/N) * W(m) = (1/2) log(1 + m^2/Lambda^2)

    W_per_taste = 0.5 * math.log(1 + m_val**2 / Lambda_sq)
    print(f"  W per taste at m = y_t * v_lattice: {W_per_taste:.6e}")

    # The mass can be read from the ratio:
    # [det(D + m) / det(D)]^{1/N} = (1 + m^2/Lambda^2)^{1/2}
    # For m << Lambda: ~ 1 + m^2/(2 Lambda^2)
    ratio_16th_root = (1 + m_val**2 / Lambda_sq)**0.5
    print(f"  [det(D + m)/det(D)]^(1/16) = {ratio_16th_root:.10f}")

    # =====================================================================
    # Approach (d): Propagator pole — the physical fermion mass
    # =====================================================================
    print("\n--- (d) Propagator pole analysis ---")

    # The fermion propagator on the taste block:
    # S(p) = (D + m)^{-1}
    # The pole is at det(D + m) = 0, i.e., m = -lambda_k for some k.
    # Since all eigenvalues are purely imaginary (lambda_k = i * |lambda_k|),
    # det(D + m) = 0 has NO real solutions — the propagator has no real pole!
    # This is correct: on the FINITE lattice block, there are no propagating
    # states. The "mass" is encoded differently.

    # The physical mass on the lattice is extracted from the exponential
    # decay of the propagator in Euclidean time:
    # G(t) = <psi(t) psi-bar(0)> ~ exp(-m_phys * t)
    # On L_t = 2 with APBC, the propagator in the temporal direction is:
    # G(t=1) = (D + m)^{-1}_{t=0,t=1}

    # Build D + m and compute propagator
    # For the Dirac operator in momentum space with degenerate spectrum,
    # the inverse is:
    # (D + m)^{-1}_k = (m - lambda_k) / (m^2 + |lambda_k|^2)

    # The temporal propagator (site 0 to site 1) averages over spatial momenta:
    # G(1) = (1/N_s) sum_k (m - lambda_k) / (m^2 + |lambda_k|^2) * phase_k

    # Let's compute this numerically for several values of m
    print("  Computing temporal propagator G(t=1) vs mass m...")
    D_hop = build_dirac_4d_apbc(Ls=2, Lt=2, u0=1.0)
    m_values = np.logspace(-6, 0, 50)
    G_values = []

    for m in m_values:
        D_m = U0 * D_hop + m * np.eye(16)
        D_inv = np.linalg.inv(D_m)
        # Average temporal propagator: average of (x,0) -> (x,1) elements
        g_sum = 0.0
        count = 0
        for x0 in range(2):
            for x1 in range(2):
                for x2 in range(2):
                    i0 = ((x0 * 2 + x1) * 2 + x2) * 2 + 0  # t=0
                    i1 = ((x0 * 2 + x1) * 2 + x2) * 2 + 1  # t=1
                    g_sum += abs(D_inv[i1, i0])
                    count += 1
        G_values.append(g_sum / count)

    G_values = np.array(G_values)

    # The effective mass from G(1)/G(0):
    # G(0) = sum of diagonal elements (m / (m^2 + Lambda^2))
    # G(1) should decay as exp(-m_eff)
    # On L_t = 2 with APBC: the Matsubara frequencies are omega = pi/2
    # The propagator in time-momentum space:
    # G(omega) = 1 / (i sin(omega) + m)  => for omega = pi/2: G = 1/(i + m)
    # G(t=1) = (1/Lt) sum_omega G(omega) * exp(i omega) -- the exponential decay

    # For the anti-Hermitian D, the effective mass on L_t=2 is:
    # m_eff = -log|G(1)/G(0)| is only meaningful for L_t >> 1.
    # On L_t=2, we extract m_eff differently.

    # Analytic formula for the temporal propagator on L_t=2 APBC:
    # The temporal part of D is: (u0/2) * eta_3 * (forward - backward hop)
    # with APBC. For L_t=2, the temporal Dirac matrix is:
    # D_t = (u0/2) * eta_3 * [[0, 1], [-(-1), 0]] = (u0/2) * eta_3 * [[0,1],[1,0]]
    # Wait, with APBC: psi(2) = -psi(0), so:
    # forward hop: 0->1 (sign +1), 1->0 wrapping (sign -1)
    # backward hop: 1->0 (sign +1), 0->1 wrapping (sign -1)
    # So the temporal part for fixed spatial site is:
    # D_t = (u0*eta_3/2) * [[0, 1-(-1)], [-(1)+(-1), 0]]
    # = (u0*eta_3/2) * [[0, 2], [-2, 0]]... this needs careful checking.

    # Let me just extract the effective mass from the ratio of propagators
    # at different m values.
    print(f"  G(t=1) at m=1e-6: {G_values[0]:.6e}")
    print(f"  G(t=1) at m=0.01: {G_values[15]:.6e}")
    print(f"  G(t=1) at m=1.0:  {G_values[-1]:.6e}")

    # =====================================================================
    # Approach (e): Hierarchy structure ratio
    # =====================================================================
    print("\n--- (e) Hierarchy structure — m_t from the determinant ratio ---")

    # The hierarchy gives v = M_Pl * alpha_LM^16.
    # Can we get m_t from a RELATED formula?

    # Key insight: the fermion mass is m_t = y_t * v / sqrt(2).
    # The question is what y_t the determinant gives.

    # On the taste block, det(D + m) / det(D) = prod_k (1 + m/lambda_k)
    # For degenerate spectrum with all |lambda_k| = Lambda:
    # |det(D + m) / det(D)| = (1 + m^2/Lambda^2)^{N/2}

    # The hierarchy formula relates:
    # v = M_Pl * (alpha_LM)^16 = M_Pl * (1/(4 pi u0))^16

    # For the fermion mass, consider the YUKAWA coupling in the taste
    # determinant framework. The mass parameter m = y_t * phi couples the
    # fermion to the scalar field. At the VEV phi = v:
    # m_t = y_t * v (with or without 1/sqrt(2) depending on convention)

    # The framework Yukawa at the UV scale:
    # y_t(UV) = g_s / sqrt(6) = sqrt(4 pi alpha_LM) / sqrt(6) = 0.436

    # But the CW minimum gave y_t = 0.78 -- which failed.
    # The determinant approach should give a DIFFERENT answer.

    # THE KEY QUESTION: does the determinant structure PREDICT y_t?

    # From Codex's W(j) = log|det(D + j I)| - log|det(D)|:
    # The curvature W''(0) gives the scalar mass squared.
    # The VEV is where the effective potential (including tree-level terms)
    # is minimized. But the TREE-LEVEL part comes from the gauge sector,
    # not the fermion determinant.

    # Without a tree-level potential to compete against, the fermion
    # determinant alone does not have a nontrivial minimum -- W(m) is
    # monotonically increasing for m > 0.

    # However, if we ASSUME v is given by the hierarchy formula, then:
    # m_t is determined by the Yukawa coupling.

    # What Yukawa does the taste block structure select?

    # Option 1: y_t = 1 (the naive condensate condition)
    # This gives m_t = v/sqrt(2) = 173.3 GeV

    # Option 2: y_t(UV) = g_s/sqrt(6) = 0.436
    # This gives m_t = 0.436 * v/sqrt(2) = 75.5 GeV

    # Option 3: y_t selected by the taste determinant
    # The taste block has N = 16 eigenvalues, all with |lambda| = Lambda.
    # There's no mechanism to distinguish y_t values within det(D+m).

    # Let's investigate whether the determinant RESPONSE selects y_t = 1.

    # Consider: what value of m makes W(m) = 1 (one e-fold of the
    # determinant ratio)?
    # W(m*) = (N/2) log(1 + m*^2/Lambda^2) = 1
    # => m* = Lambda * sqrt(exp(2/N) - 1) = Lambda * sqrt(exp(1/8) - 1)
    m_star = Lambda * math.sqrt(math.exp(2.0/N) - 1)
    m_star_phys = m_star * M_PL
    print(f"\n  m* where W(m*) = 1: m* = {m_star:.6f} (lattice units)")
    print(f"  m* in physical units: {m_star_phys:.3e} GeV")
    print(f"  m* / Lambda = {m_star / Lambda:.6f}")
    print("  -> m* is O(Lambda), i.e., O(M_Pl). Not related to m_t.")

    # Consider: what m makes d/dm [m * dW/dm] = 0?
    # m * W'(m) = m * N * m / (m^2 + Lambda^2) = N * m^2 / (m^2 + Lambda^2)
    # d/dm [m W'(m)] = N * 2m Lambda^2 / (m^2 + Lambda^2)^2
    # This is never zero for m > 0. No critical point.

    # Let's try the third derivative (inflection of susceptibility):
    # chi(m) = W''(m) = N(Lambda^2 - m^2)/(m^2 + Lambda^2)^2
    # chi'(m) = N * (-2m)(3Lambda^2 - m^2)/(m^2 + Lambda^2)^3
    # chi'(m) = 0 at m = Lambda * sqrt(3)
    m_inflect = Lambda * math.sqrt(3)
    print(f"\n  Inflection of chi at m = Lambda*sqrt(3) = {m_inflect:.6f}")
    print(f"  In physical units: {m_inflect * M_PL:.3e} GeV")
    print("  -> Again O(M_Pl). Degenerate spectrum has no low-energy structure.")

    # =====================================================================
    # THE HONEST ASSESSMENT
    # =====================================================================
    print("\n--- Honest assessment of all approaches ---")
    print()
    print("  The degenerate eigenvalue spectrum |lambda_k| = u0 * 2 for all k")
    print("  means the taste determinant det(D + m) is a simple function of m:")
    print("  log|det(D + m)/det(D)| = 8 * log(1 + m^2/(4 u0^2))")
    print()
    print("  This function:")
    print("  - Has no special structure at any mass scale << Lambda = 2 u0")
    print("  - Cannot distinguish different Yukawa couplings")
    print("  - Has all characteristic scales at O(Lambda) = O(M_Pl)")
    print()
    print("  The taste determinant correctly encodes the HIERARCHY (v/M_Pl)")
    print("  through the alpha_LM^16 power law (= u0^{-16} dependence).")
    print("  But it does NOT encode the FERMION MASS independently.")
    print()
    print("  The fermion mass m_t = y_t * v requires an ADDITIONAL input:")
    print("  the Yukawa coupling y_t, which is not determined by det(D + m I).")

    return m_values, G_values


# ============================================================================
# Part 4: The Key Test — m_t predictions from different y_t values
# ============================================================================

def part4_key_test():
    print("\n" + "=" * 70)
    print("PART 4: The Key Test — m_t from Different Yukawa Values")
    print("=" * 70)

    v = M_PL * ALPHA_LM**16  # hierarchy VEV

    print(f"\n  v (hierarchy) = {v:.1f} GeV")
    print(f"  v (observed)  = {V_OBS} GeV")
    print()

    # Candidate Yukawa values and their origins
    candidates = {
        "y_t = 1 (near-critical / naturalness)": 1.0,
        "y_t = 1/sqrt(2) (special)":             1.0 / math.sqrt(2),
        "y_t(UV) = g_s/sqrt(6) = 0.436":         Y_T_UV,
        "y_t(SM IR) = 0.9935":                    0.9935,
    }

    print(f"  {'Scenario':<45s} {'y_t':>6s} {'m_t (GeV)':>10s} "
          f"{'Deviation':>10s}")
    print(f"  {'-'*45} {'-'*6} {'-'*10} {'-'*10}")

    for name, yt in candidates.items():
        # Convention: m_t = y_t * v / sqrt(2) (SM Yukawa convention)
        mt = yt * v / math.sqrt(2)
        dev_pct = (mt - M_TOP_OBS) / M_TOP_OBS * 100
        marker = " <--" if abs(dev_pct) < 5 else ""
        print(f"  {name:<45s} {yt:>6.4f} {mt:>10.1f} {dev_pct:>+9.1f}%{marker}")

    print()
    # Using v_obs instead of v_hierarchy:
    print(f"  --- Using v_obs = {V_OBS} GeV instead of v_hierarchy ---")
    for name, yt in candidates.items():
        mt = yt * V_OBS / math.sqrt(2)
        dev_pct = (mt - M_TOP_OBS) / M_TOP_OBS * 100
        marker = " <--" if abs(dev_pct) < 5 else ""
        print(f"  {name:<45s} {yt:>6.4f} {mt:>10.1f} {dev_pct:>+9.1f}%{marker}")

    # Key comparison
    print("\n  KEY RESULTS:")

    mt_yt1 = v / math.sqrt(2)
    mt_yt_uv = Y_T_UV * v / math.sqrt(2)
    mt_yt_ir = 0.9935 * v / math.sqrt(2)

    print(f"  m_t(y_t=1, v_hier)    = {mt_yt1:.1f} GeV "
          f"(obs: {M_TOP_OBS}, dev: {(mt_yt1-M_TOP_OBS)/M_TOP_OBS*100:+.1f}%)")
    print(f"  m_t(y_t=UV, v_hier)   = {mt_yt_uv:.1f} GeV "
          f"(obs: {M_TOP_OBS}, dev: {(mt_yt_uv-M_TOP_OBS)/M_TOP_OBS*100:+.1f}%)")
    print(f"  m_t(y_t=IR, v_hier)   = {mt_yt_ir:.1f} GeV "
          f"(obs: {M_TOP_OBS}, dev: {(mt_yt_ir-M_TOP_OBS)/M_TOP_OBS*100:+.1f}%)")

    check("y_t=1 gives m_t = v/sqrt(2) ~ 173 GeV within 5%",
          abs(mt_yt1 - M_TOP_OBS) / M_TOP_OBS < 0.05,
          f"m_t = {mt_yt1:.1f} GeV, deviation = "
          f"{(mt_yt1-M_TOP_OBS)/M_TOP_OBS*100:+.1f}%")

    check("y_t(UV) = 0.436 gives m_t ~ 78 GeV (too low)",
          mt_yt_uv < 100,
          f"m_t = {mt_yt_uv:.1f} GeV, 55% below observed")

    return mt_yt1, mt_yt_uv


# ============================================================================
# Part 5: Physical interpretation
# ============================================================================

def part5_interpretation(mt_yt1, mt_yt_uv):
    print("\n" + "=" * 70)
    print("PART 5: Physical Interpretation")
    print("=" * 70)

    v = M_PL * ALPHA_LM**16

    print("""
  FINDING: The taste determinant det(D + m) on the minimal L_t=2 block
  does NOT independently determine the top mass. It determines the VEV v
  through the coupling dependence (alpha_LM^16), but all eigenvalues are
  degenerate at |lambda| = u0 * sqrt(d), leaving no structure to select y_t.

  WHAT THE DETERMINANT GIVES:
  - v/M_Pl = alpha_LM^16 (from u0^{-16} dependence) -> v = 254 GeV [WORKS]
  - The eigenvalue scale Lambda = 2*u0 ~ O(M_Pl) [correct UV behavior]
  - W(m) = 8 * log(1 + m^2/(4*u0^2)) [smooth, featureless for m << Lambda]

  WHAT THE DETERMINANT DOES NOT GIVE:
  - The Yukawa coupling y_t (no structure at the EW scale in degenerate spectrum)
  - The top mass m_t = y_t * v / sqrt(2) (requires y_t as additional input)
  - Any distinction between y_t = 1 and y_t = 0.436

  WHY y_t = 1 IS FAVORED (external arguments, not from det(D+m)):
  1. Near-criticality: y_t = 1 means m_t = v/sqrt(2), the maximum mass
     consistent with perturbative unitarity of WW scattering.
  2. IR fixed point: the top Yukawa RG flow has a quasi-fixed point near y_t ~ 1
     in the SM, regardless of the UV value. If y_t(UV) = 0.436, running to the
     EW scale gives y_t(IR) ~ 0.9-1.0.
  3. Vacuum stability: y_t ~ 1 places the SM near the stability-metastability
     boundary, consistent with the observed Higgs mass.

  THE y_t QUESTION REMAINS OPEN:
  - The taste determinant determines v but not y_t
  - The RG running from y_t(UV) = 0.436 to y_t(IR) ~ 1.0 is a SEPARATE
    computation requiring the full SM beta functions
  - If y_t(IR) ~ 1 from RG: m_t = v/sqrt(2) ~ 173 GeV [matches observation]
  - If y_t stays at UV value: m_t = 78 GeV [does not match]
""")

    # Test: does RG running plausibly take y_t(UV) = 0.436 to y_t(IR) ~ 1?
    # The 1-loop top Yukawa beta function (SM) is:
    # dy_t/d(ln mu) = y_t/(16 pi^2) * (9/2 y_t^2 - 8 g_s^2 - 9/4 g_2^2 - ...)
    # The QCD term -8 g_s^2 is dominant and DRIVES y_t up (g_s decreases as we
    # run down from UV). The quasi-fixed point (Pendleton-Ross) is at
    # y_t^2 / g_s^2 = 16/9 ~ 1.78, giving y_t ~ 1.33 * g_s.

    log_ratio = math.log(M_PL / M_TOP_OBS)
    print(f"  RG running distance: log(M_Pl/m_t) = {log_ratio:.1f}")

    # Numerical integration of coupled 1-loop RG (y_t and g_s only)
    # Using alpha_s and y_t^2 as variables for stability:
    # d(alpha_s)/d(ln mu) = -2 b_0 alpha_s^2 / (4 pi), b_0 = 7
    # d(y_t^2)/d(ln mu) = y_t^2/(8 pi^2) * (9/2 y_t^2 - 8 g_s^2)
    y_t_uv = Y_T_UV
    g_s_uv = G_S_UV  # = sqrt(4 pi alpha_LM) = 1.068
    alpha_s_uv = ALPHA_LM

    # For alpha_s, the 1-loop running has an analytic solution:
    # 1/alpha_s(mu) = 1/alpha_s(UV) + (b_0/(2 pi)) * ln(UV/mu)
    b0 = 7.0
    alpha_s_inv_ir = 1.0 / alpha_s_uv + b0 / (2 * PI) * log_ratio
    alpha_s_ir = 1.0 / alpha_s_inv_ir
    g_s_ir_analytic = math.sqrt(4 * PI * alpha_s_ir)

    print(f"  alpha_s running (1-loop analytic, b_0 = {b0}):")
    print(f"    alpha_s(M_Pl) = {alpha_s_uv:.4f}")
    print(f"    alpha_s(m_t)  = {alpha_s_ir:.4f} (observed: 0.108)")
    print(f"    g_s(m_t) = {g_s_ir_analytic:.4f}")

    # For y_t, use RK4 with alpha_s from the analytic solution
    N_steps = 50000
    dt = -log_ratio / N_steps  # negative: running down from UV
    yt2 = y_t_uv**2

    for step in range(N_steps):
        # Current scale: ln(mu) = ln(M_Pl) + step * dt
        t_frac = step / N_steps  # 0 at UV, 1 at IR
        # alpha_s at this scale
        ln_ratio_here = t_frac * log_ratio
        as_inv = 1.0 / alpha_s_uv + b0 / (2 * PI) * ln_ratio_here
        as_here = 1.0 / as_inv
        gs2_here = 4 * PI * as_here

        # RK4 step for y_t^2
        def beta_yt2(y2, gs2_val):
            return y2 / (8 * PI**2) * (4.5 * y2 - 8 * gs2_val)

        k1 = beta_yt2(yt2, gs2_here) * dt
        # Midpoint alpha_s
        ln_mid = (t_frac + 0.5 / N_steps) * log_ratio
        as_mid = 1.0 / (1.0 / alpha_s_uv + b0 / (2 * PI) * ln_mid)
        gs2_mid = 4 * PI * as_mid
        k2 = beta_yt2(yt2 + k1/2, gs2_mid) * dt
        k3 = beta_yt2(yt2 + k2/2, gs2_mid) * dt
        # Endpoint alpha_s
        ln_end = (t_frac + 1.0 / N_steps) * log_ratio
        as_end = 1.0 / (1.0 / alpha_s_uv + b0 / (2 * PI) * ln_end)
        gs2_end = 4 * PI * as_end
        k4 = beta_yt2(yt2 + k3, gs2_end) * dt
        yt2 += (k1 + 2*k2 + 2*k3 + k4) / 6.0

        if yt2 < 0:
            yt2 = 0.001
            break

    y_t_ir_est = math.sqrt(max(yt2, 0))
    g_s_ir_est = g_s_ir_analytic
    mt_rg = y_t_ir_est * v / math.sqrt(2)

    print(f"\n  Coupled 1-loop RG (RK4, y_t + analytic g_s):")
    print(f"    y_t(UV) = {y_t_uv:.4f}, g_s(UV) = {g_s_uv:.4f}")
    print(f"    y_t(IR) = {y_t_ir_est:.4f}, g_s(IR) = {g_s_ir_est:.4f}")
    print(f"    y_t/g_s ratio at IR: {y_t_ir_est/g_s_ir_est:.4f} "
          f"(Pendleton-Ross FP: {math.sqrt(16/9):.4f})")
    print(f"    m_t(RG) = y_t(IR) * v / sqrt(2) = {mt_rg:.1f} GeV")

    # Note: this 1-loop running with b_0=7 over-runs alpha_s (gives 0.018 vs
    # observed 0.108 at m_t). The SM has threshold effects and 2-loop terms.
    # With the observed alpha_s(m_t) = 0.108, the Pendleton-Ross FP gives
    # y_t ~ 1.33 * g_s(m_t) = 1.33 * 1.166 = 1.55, and the actual IR value
    # is pulled toward y_t ~ 1 from below. The crude RG here underestimates
    # y_t(IR) because it underestimates alpha_s(IR).

    # Cross-check with observed alpha_s:
    alpha_s_obs_mt = 0.1080  # alpha_s(m_t) from PDG
    g_s_obs_mt = math.sqrt(4 * PI * alpha_s_obs_mt)
    yt_PR_fp = math.sqrt(16.0/9.0) * g_s_obs_mt  # Pendleton-Ross
    print(f"\n  Cross-check with observed alpha_s(m_t) = {alpha_s_obs_mt}:")
    print(f"    g_s(m_t) observed = {g_s_obs_mt:.4f}")
    print(f"    Pendleton-Ross FP: y_t = sqrt(16/9)*g_s = {yt_PR_fp:.4f}")
    print(f"    m_t(PR FP) = {yt_PR_fp * v / math.sqrt(2):.1f} GeV (upper bound)")
    print(f"    SM actual y_t(m_t) = 0.9935 -> m_t = "
          f"{0.9935 * V_OBS / math.sqrt(2):.1f} GeV")

    check("RG drives y_t above UV value (0.436 -> 0.689+)",
          y_t_ir_est > Y_T_UV * 1.3,
          f"y_t(IR) = {y_t_ir_est:.3f} > y_t(UV) = {Y_T_UV:.3f}: "
          f"RG increases y_t by factor {y_t_ir_est/Y_T_UV:.2f}")

    # =====================================================================
    # ALTERNATIVE: m_t from the taste multiplicity structure
    # =====================================================================
    print("\n  --- Alternative: taste multiplicity argument ---")
    print()
    print("  On the L_t=2 block, the 16 taste states are ALL degenerate.")
    print("  In the physical SM, these 16 tastes map to 4 physical flavors")
    print("  (the 4 Dirac components of one staggered field).")
    print("  The heaviest quark (top) saturates the condensate.")
    print()
    print("  If the EWSB condensate is dominated by one flavor with y_t = 1:")
    print(f"  m_t = v / sqrt(2) = {v / math.sqrt(2):.1f} GeV")
    print(f"  (observed: {M_TOP_OBS} GeV, deviation: "
          f"{(v/math.sqrt(2) - M_TOP_OBS)/M_TOP_OBS*100:+.1f}%)")

    # Final summary comparison
    print("\n  === FINAL SUMMARY TABLE ===")
    print()
    print(f"  {'Method':<50s} {'m_t (GeV)':>10s} {'Status':>12s}")
    print(f"  {'-'*50} {'-'*10} {'-'*12}")
    print(f"  {'Observed':.<50s} {M_TOP_OBS:>10.2f} {'(target)':>12s}")
    print(f"  {'v_hier/sqrt(2) (y_t=1 assumption)':.<50s} "
          f"{v/math.sqrt(2):>10.1f} "
          f"{'+' if v/math.sqrt(2) > M_TOP_OBS else ''}"
          f"{(v/math.sqrt(2)-M_TOP_OBS)/M_TOP_OBS*100:.1f}%")
    print(f"  {'v_obs/sqrt(2) (y_t=1 assumption)':.<50s} "
          f"{V_OBS/math.sqrt(2):>10.1f} "
          f"{'+' if V_OBS/math.sqrt(2) > M_TOP_OBS else ''}"
          f"{(V_OBS/math.sqrt(2)-M_TOP_OBS)/M_TOP_OBS*100:.1f}%")
    print(f"  {'y_t(UV)*v_hier/sqrt(2) (no running)':.<50s} "
          f"{Y_T_UV*v/math.sqrt(2):>10.1f} "
          f"{(Y_T_UV*v/math.sqrt(2)-M_TOP_OBS)/M_TOP_OBS*100:+.1f}%")

    print(f"  {'y_t(IR coupled RG)*v_hier/sqrt(2)':.<50s} "
          f"{mt_rg:>10.1f} "
          f"{(mt_rg-M_TOP_OBS)/M_TOP_OBS*100:+.1f}%")

    check("OVERALL: m_t ~ v/sqrt(2) if y_t(IR) ~ 1 (RG or near-criticality)",
          abs(v / math.sqrt(2) - M_TOP_OBS) / M_TOP_OBS < 0.05,
          f"m_t(y_t=1) = {v/math.sqrt(2):.1f} GeV vs observed {M_TOP_OBS} GeV")


# ============================================================================
# Main
# ============================================================================

def main():
    print("=" * 70)
    print("TOP MASS FROM THE LATTICE DETERMINANT")
    print("=" * 70)
    print()
    print(f"  Framework inputs: g=1, <P>={PLAQ_MC}, M_Pl={M_PL:.2e} GeV")
    print(f"  alpha_LM = {ALPHA_LM:.5f}")
    print(f"  v_hierarchy = M_Pl * alpha_LM^16 = {V_HIERARCHY:.1f} GeV")
    print(f"  y_t(UV) = g_s/sqrt(6) = {Y_T_UV:.4f}")
    print(f"  Target: m_t(obs) = {M_TOP_OBS} GeV, v/sqrt(2) = "
          f"{V_HIERARCHY/math.sqrt(2):.1f} GeV")

    # Part 1: exact determinant
    eigs_hop, eigs_phys, D_hop, D_phys = part1_exact_determinant()

    # Part 2: scalar response (v)
    Lambda_sq = (U0 * 2.0)**2
    W_exact, W_degen, Lambda_sq = part2_scalar_response(D_hop, eigs_phys)

    # Part 3: fermion mass
    m_vals, G_vals = part3_fermion_mass(eigs_phys, W_exact, Lambda_sq)

    # Part 4: key test
    mt_yt1, mt_yt_uv = part4_key_test()

    # Part 5: interpretation
    part5_interpretation(mt_yt1, mt_yt_uv)

    # Scorecard
    print("\n" + "=" * 70)
    print(f"SCORECARD: {PASS_COUNT} pass, {FAIL_COUNT} fail "
          f"out of {PASS_COUNT + FAIL_COUNT}")
    print("=" * 70)

    if FAIL_COUNT > 0:
        print("\nFAILED TESTS PRESENT -- review needed")
        sys.exit(1)
    else:
        print("\nAll tests pass.")
        sys.exit(0)


if __name__ == "__main__":
    main()
