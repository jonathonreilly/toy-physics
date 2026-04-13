#!/usr/bin/env python3
"""
R = Omega_DM / Omega_b : Sensitivity to Transport Parameters
================================================================

QUESTION: The transport parameters D_q*T and v_w carry wide uncertainty
bands (D_q*T = 3.1 +/- 30%, v_w in [0.006, 0.048]).  Does this
uncertainty propagate significantly into R = Omega_DM / Omega_b?

INSIGHT: R depends on eta LOGARITHMICALLY through x_F = ln(...).
If dR/R < 10% across the full transport range, the transport
precision doesn't matter -- R is derived to the same precision
as the Sommerfeld factor and the mass ratio.

METHOD:
  1. eta as a function of D_q*T (holding v_w, L_w*T, v/T fixed)
  2. eta as a function of v_w (holding D_q*T, L_w*T, v/T fixed)
  3. R as a function of eta (the freeze-out chain)
  4. Total sensitivity: dR/R from the transport uncertainty band

INPUTS (all framework-derived):
  D_q*T = 3.1 +/- 30%  (HTL-resummed, DM_DQT_HTL_NOTE.md)
  v_w   = 0.014 [0.006, 0.048]  (Boltzmann closure, DM_VW_DERIVATION_NOTE.md)
  L_w*T = 13 [10, 18]  (CW bounce, DM_BOUNCE_WALL_NOTE.md)
  v/T   = 0.56 +/- 0.05  (gauge-effective MC)

PStack experiment: dm-r-sensitivity
Self-contained: numpy + scipy only.
"""

from __future__ import annotations

import math
import sys
import time

import numpy as np

try:
    from scipy.optimize import brentq
except ImportError:
    print("ERROR: scipy required. pip install scipy")
    sys.exit(1)

np.set_printoptions(precision=8, linewidth=120)

LOG_FILE = "logs/" + time.strftime("%Y-%m-%d") + "-dm_r_sensitivity.txt"

results = []
def log(msg=""):
    results.append(msg)
    print(msg)


# =============================================================================
# PHYSICAL CONSTANTS (same as frontier_eta_from_framework.py)
# =============================================================================

PI = np.pi

# SM couplings at the weak scale
G_WEAK = 0.653           # SU(2) gauge coupling g
G_PRIME = 0.350          # U(1) hypercharge coupling g'
Y_TOP = 0.995            # Top Yukawa coupling
ALPHA_W = G_WEAK**2 / (4 * PI)   # ~ 0.0339

# SM masses (GeV)
M_W = 80.4
M_Z = 91.2
M_H = 125.1
M_T = 173.0
V_EW = 246.0             # Higgs VEV (GeV)

# Cosmological
T_EW = 160.0             # EW phase transition temperature (GeV)
M_PL_RED = 2.435e18      # Reduced Planck mass (GeV)
G_STAR = 106.75           # Effective relativistic degrees of freedom at T_EW

# Observed
ETA_OBS = 6.12e-10       # Planck 2018: n_B / n_gamma
R_OBS = 5.47             # Omega_DM / Omega_b (Planck 2018)

# DM parameters (from framework)
M_DM_OVER_MP = 3.0       # Hamming weight ratio (S_3 / visible)
STRUCTURAL_FACTOR = 3.0 / 5.0  # from Lee-Weinberg on Z^3

# =============================================================================
# BARYOGENESIS CONSTANTS
# =============================================================================

N_F = 3                  # Number of quark families
KAPPA_SPH = 20.0         # Sphaleron rate prefactor (d'Onofrio et al.)
GAMMA_WS = KAPPA_SPH * ALPHA_W**5  # Gamma_sph / T^4
S_OVER_NGAMMA = 7.04     # entropy-to-photon ratio
SIN_DELTA = np.sin(2 * PI / 3)  # Z_3 CP phase: sqrt(3)/2
CP_COUPLING = Y_TOP**2 / (4 * PI**2)  # y_t^2 / (4 pi^2)
ESPH_COEFF = (4 * PI / G_WEAK) * 1.87  # ~ 36 (sphaleron exponent)

# Hubble rate at T_EW
RHO_EW = (PI**2 / 30) * G_STAR * T_EW**4
H_EW = np.sqrt(8 * PI * RHO_EW / (3 * M_PL_RED**2))
SPH_OVER_H_SYMM = GAMMA_WS * T_EW / H_EW

# Framework prefactor (all derived quantities)
A_FRAMEWORK = S_OVER_NGAMMA * (N_F / 4.0) * GAMMA_WS * CP_COUPLING * SIN_DELTA


# =============================================================================
# PART 1: eta as a function of D_q*T
# =============================================================================

def compute_eta(D_q_T, v_w, L_w_T, vt):
    """
    Compute the surviving baryon-to-photon ratio eta.

    eta = A_framework * P_transport * (v/T) * exp(-washout)

    where P_transport = D_q*T / (v_w * L_w*T)
    and washout = Gamma_sph(broken) / H
                = (Gamma_sph(symm)/H) * exp(-36 * v/T)
    """
    P_transport = D_q_T / (v_w * L_w_T)
    eta_prod = A_FRAMEWORK * P_transport * vt
    gbh = SPH_OVER_H_SYMM * np.exp(-ESPH_COEFF * vt)
    if gbh > 500:
        return 0.0
    survival = np.exp(-gbh)
    return eta_prod * survival


def part1_eta_vs_dqt():
    """Scan eta as a function of D_q*T, holding everything else fixed."""
    log("=" * 72)
    log("PART 1: eta vs D_q*T")
    log("=" * 72)

    # Fixed parameters (framework central values)
    v_w = 0.014       # Boltzmann closure central
    L_w_T = 13.0      # CW bounce central
    vt = 0.56         # gauge-effective MC central

    log(f"\n  Fixed: v_w = {v_w}, L_w*T = {L_w_T}, v/T = {vt}")
    log(f"\n  {'D_q*T':>8s}  {'P_transport':>12s}  {'eta':>12s}  {'eta/eta_obs':>12s}")
    log(f"  {'-'*8}  {'-'*12}  {'-'*12}  {'-'*12}")

    D_q_T_values = np.linspace(1.0, 10.0, 19)
    eta_values_dqt = []

    for dqt in D_q_T_values:
        P = dqt / (v_w * L_w_T)
        eta = compute_eta(dqt, v_w, L_w_T, vt)
        eta_values_dqt.append(eta)
        log(f"  {dqt:8.1f}  {P:12.1f}  {eta:12.3e}  {eta/ETA_OBS:12.3f}")

    # HTL range: 3.1 +/- 30% -> [2.17, 4.03]
    dqt_lo, dqt_hi = 2.17, 4.03
    eta_lo = compute_eta(dqt_lo, v_w, L_w_T, vt)
    eta_hi = compute_eta(dqt_hi, v_w, L_w_T, vt)
    log(f"\n  HTL range D_q*T = [{dqt_lo:.2f}, {dqt_hi:.2f}]:")
    log(f"    eta_lo = {eta_lo:.3e}  (ratio {eta_lo/ETA_OBS:.3f})")
    log(f"    eta_hi = {eta_hi:.3e}  (ratio {eta_hi/ETA_OBS:.3f})")
    log(f"    eta variation: {(eta_hi - eta_lo) / (0.5*(eta_hi + eta_lo)) * 100:.1f}%")

    return D_q_T_values, np.array(eta_values_dqt)


# =============================================================================
# PART 2: eta as a function of v_w
# =============================================================================

def part2_eta_vs_vw():
    """Scan eta as a function of v_w, holding everything else fixed."""
    log("\n" + "=" * 72)
    log("PART 2: eta vs v_w")
    log("=" * 72)

    # Fixed parameters
    D_q_T = 3.1       # HTL central
    L_w_T = 13.0
    vt = 0.56

    log(f"\n  Fixed: D_q*T = {D_q_T}, L_w*T = {L_w_T}, v/T = {vt}")
    log(f"\n  {'v_w':>8s}  {'P_transport':>12s}  {'eta':>12s}  {'eta/eta_obs':>12s}")
    log(f"  {'-'*8}  {'-'*12}  {'-'*12}  {'-'*12}")

    v_w_values = np.linspace(0.005, 0.05, 19)
    eta_values_vw = []

    for vw in v_w_values:
        P = D_q_T / (vw * L_w_T)
        eta = compute_eta(D_q_T, vw, L_w_T, vt)
        eta_values_vw.append(eta)
        log(f"  {vw:8.4f}  {P:12.1f}  {eta:12.3e}  {eta/ETA_OBS:12.3f}")

    # Boltzmann closure range: [0.006, 0.048]
    vw_lo, vw_hi = 0.006, 0.048
    eta_lo = compute_eta(D_q_T, vw_hi, L_w_T, vt)  # Note: eta ~ 1/v_w
    eta_hi = compute_eta(D_q_T, vw_lo, L_w_T, vt)
    log(f"\n  Boltzmann closure range v_w = [{vw_lo:.3f}, {vw_hi:.3f}]:")
    log(f"    eta(v_w=0.048) = {eta_lo:.3e}  (ratio {eta_lo/ETA_OBS:.3f})")
    log(f"    eta(v_w=0.006) = {eta_hi:.3e}  (ratio {eta_hi/ETA_OBS:.3f})")
    log(f"    eta variation: {(eta_hi - eta_lo) / (0.5*(eta_hi + eta_lo)) * 100:.1f}%")
    log(f"    eta spans factor {eta_hi/eta_lo:.1f}")

    return v_w_values, np.array(eta_values_vw)


# =============================================================================
# PART 3: R as a function of eta (the freeze-out chain)
# =============================================================================

def compute_R_from_eta(eta):
    """
    Compute R = Omega_DM / Omega_b from the baryon-to-photon ratio eta.

    The key chain:
      Omega_b * h^2 = 3.65e7 * eta  (BBN standard relation)
      Omega_DM follows from freeze-out (framework-derived, independent of eta)
      R = Omega_DM / Omega_b

    Since Omega_DM is fixed by the framework freeze-out calculation,
    R = Omega_DM / Omega_b ~ 1/eta (at fixed Omega_DM).

    More precisely, the freeze-out abundance gives:
      Omega_DM * h^2 = (m_DM * s_0 * Y_inf) / rho_crit
    where Y_inf = n_DM/s at freeze-out, and:
      Y_inf = (45 / (2 pi^4)) * (1/g_star) * (x_F / (M_Pl * m_DM * <sigma v>))

    x_F = ln(c * m_DM * M_Pl * <sigma v> / sqrt(g_star * x_F))
    This is the logarithmic dependence on everything.

    For R specifically:
      R = (Omega_DM * h^2) / (Omega_b * h^2)
        = (Omega_DM * h^2) / (3.65e7 * eta)

    Since Omega_DM * h^2 is fixed by framework freeze-out, R ~ 1/eta.
    """
    # Framework freeze-out gives Omega_DM * h^2 (the DM relic density)
    # This is INDEPENDENT of eta -- it depends on sigma_v, m_DM, x_F.
    #
    # From the 13-step derivation (DM_CLEAN_DERIVATION_NOTE.md):
    # sigma_v = 2.2e-26 cm^3/s (from T-matrix, Step 9)
    # m_DM = 3 * m_0 (Hamming weight)
    # x_F ~ 25 (from Boltzmann + Gamma = H)
    #
    # The standard freeze-out result:
    # Omega_DM * h^2 = (1.07e9 GeV^{-1}) * x_F / (M_Pl * sqrt(g_star) * sigma_v)
    #
    # We use the framework-derived value directly.

    # sigma_v in natural units (GeV^{-2})
    # 2.2e-26 cm^3/s = 2.2e-26 * (1/(3e10))^{-1} * (1/(1.97e-14))^2 GeV^{-2}
    # = 2.2e-26 / (3e10 * (1.97e-14)^2) = 2.2e-26 / (1.164e-17) = 1.89e-9 GeV^{-2}
    sigma_v_nat = 1.89e-9   # GeV^{-2}

    # Standard freeze-out formula
    # Omega * h^2 = (1.07e9 / M_Pl) * x_F / (sqrt(g_star) * sigma_v)
    M_Pl_GeV = 1.22e19
    x_F = 25.0  # framework-derived (log-insensitive)

    Omega_DM_h2 = (1.07e9 / M_Pl_GeV) * x_F / (np.sqrt(G_STAR) * sigma_v_nat)

    # BBN relation
    Omega_b_h2 = 3.65e7 * eta

    R = Omega_DM_h2 / Omega_b_h2

    return R, Omega_DM_h2, Omega_b_h2, x_F


def part3_R_vs_eta():
    """Compute R as a function of eta."""
    log("\n" + "=" * 72)
    log("PART 3: R vs eta")
    log("=" * 72)

    # First, verify the reference point
    R_ref, OmDM, OmB, xF = compute_R_from_eta(ETA_OBS)
    log(f"\n  Reference point (eta = eta_obs = {ETA_OBS:.3e}):")
    log(f"    Omega_DM * h^2 = {OmDM:.4f}")
    log(f"    Omega_b * h^2  = {OmB:.4f}")
    log(f"    R = {R_ref:.2f}")
    log(f"    R_obs = {R_OBS:.2f}")
    log(f"    x_F = {xF:.0f}")

    # Now scan
    eta_scan = np.logspace(-11, -8, 61)
    log(f"\n  {'eta':>12s}  {'Omega_b h^2':>12s}  {'R':>8s}  {'R/R_obs':>10s}")
    log(f"  {'-'*12}  {'-'*12}  {'-'*8}  {'-'*10}")

    R_values = []
    for eta in eta_scan:
        R, _, OmB, _ = compute_R_from_eta(eta)
        R_values.append(R)
        if abs(np.log10(eta) - np.log10(ETA_OBS)) < 0.15 or \
           eta in [eta_scan[0], eta_scan[-1]] or \
           abs(np.log10(eta) - round(np.log10(eta))) < 0.05:
            log(f"  {eta:12.3e}  {OmB:12.4f}  {R:8.2f}  {R/R_OBS:10.3f}")

    R_values = np.array(R_values)

    # The key: R = const / eta, so dR/R = -d(eta)/eta
    log(f"\n  KEY STRUCTURAL RESULT:")
    log(f"  R = Omega_DM_h2 / (3.65e7 * eta)")
    log(f"  Since Omega_DM_h2 is fixed by framework freeze-out,")
    log(f"  R is EXACTLY inversely proportional to eta:")
    log(f"  dR/R = -d(eta)/eta")

    return eta_scan, R_values


# =============================================================================
# PART 4: Total sensitivity -- dR/R from transport uncertainty
# =============================================================================

def part4_total_sensitivity():
    """
    Combine Parts 1-3: how much does R vary across the transport range?

    The chain: transport params -> eta -> R

    Since R ~ 1/eta and eta ~ D_q*T / (v_w * L_w*T) * [framework stuff],
    R ~ v_w * L_w*T / (D_q*T * [framework stuff]).

    The transport prefactor P = D_q*T / (v_w * L_w*T) enters linearly in eta.
    So dR/R = |d(eta)/eta| = |dP/P|.

    But wait -- this is only for the DIRECT linear dependence.
    The indirect dependence through x_F is logarithmic:
      x_F = ln(0.038 * m * M_Pl * sigma_v / sqrt(g_star * x_F))
    x_F does NOT depend on eta at all (freeze-out is in the DM sector).

    So the question reduces to: what is the variation of the transport
    prefactor P across the uncertainty bands?
    """
    log("\n" + "=" * 72)
    log("PART 4: TOTAL SENSITIVITY dR/R FROM TRANSPORT UNCERTAINTY")
    log("=" * 72)

    # Framework-derived central values and ranges
    D_q_T_central = 3.1
    D_q_T_lo = 3.1 * 0.70   # -30%
    D_q_T_hi = 3.1 * 1.30   # +30%

    v_w_central = 0.014
    v_w_lo = 0.006
    v_w_hi = 0.048

    L_w_T_central = 13.0
    L_w_T_lo = 10.0
    L_w_T_hi = 18.0

    vt = 0.56  # framework-derived, NOT a transport parameter

    log(f"\n  Transport parameter ranges (all framework-derived):")
    log(f"    D_q*T = {D_q_T_central:.1f} [{D_q_T_lo:.2f}, {D_q_T_hi:.2f}] (HTL, +/-30%)")
    log(f"    v_w   = {v_w_central:.3f} [{v_w_lo:.3f}, {v_w_hi:.3f}] (Boltzmann closure)")
    log(f"    L_w*T = {L_w_T_central:.0f} [{L_w_T_lo:.0f}, {L_w_T_hi:.0f}] (CW bounce)")
    log(f"    v/T   = {vt:.2f} (fixed, framework-derived)")

    # Transport prefactor at central values
    P_central = D_q_T_central / (v_w_central * L_w_T_central)
    log(f"\n  Central transport prefactor P = D_q*T / (v_w * L_w*T)")
    log(f"    P_central = {P_central:.1f}")

    # Compute eta at central
    eta_central = compute_eta(D_q_T_central, v_w_central, L_w_T_central, vt)
    R_central, _, _, _ = compute_R_from_eta(eta_central)
    log(f"\n  Central values:")
    log(f"    eta = {eta_central:.3e}")
    log(f"    R   = {R_central:.2f}")

    # ---------------------------------------------------------------
    # Individual parameter sweeps -> dR/R
    # ---------------------------------------------------------------
    log(f"\n  --- Individual parameter sensitivity ---")

    # D_q*T sweep
    log(f"\n  D_q*T sweep [{D_q_T_lo:.2f}, {D_q_T_hi:.2f}]:")
    dqt_scan = np.linspace(D_q_T_lo, D_q_T_hi, 21)
    R_dqt = []
    log(f"  {'D_q*T':>8s}  {'eta':>12s}  {'R':>8s}  {'dR/R':>10s}")
    log(f"  {'-'*8}  {'-'*12}  {'-'*8}  {'-'*10}")
    for dqt in dqt_scan:
        eta = compute_eta(dqt, v_w_central, L_w_T_central, vt)
        R, _, _, _ = compute_R_from_eta(eta)
        R_dqt.append(R)
        dR_over_R = (R - R_central) / R_central
        log(f"  {dqt:8.2f}  {eta:12.3e}  {R:8.2f}  {dR_over_R:+10.3f}")

    R_dqt = np.array(R_dqt)
    dR_dqt = (R_dqt.max() - R_dqt.min()) / R_central
    log(f"\n  D_q*T: total dR/R = {dR_dqt:.3f} = {dR_dqt*100:.1f}%")

    # v_w sweep
    log(f"\n  v_w sweep [{v_w_lo:.3f}, {v_w_hi:.3f}]:")
    vw_scan = np.linspace(v_w_lo, v_w_hi, 21)
    R_vw = []
    log(f"  {'v_w':>8s}  {'eta':>12s}  {'R':>8s}  {'dR/R':>10s}")
    log(f"  {'-'*8}  {'-'*12}  {'-'*8}  {'-'*10}")
    for vw in vw_scan:
        eta = compute_eta(D_q_T_central, vw, L_w_T_central, vt)
        R, _, _, _ = compute_R_from_eta(eta)
        R_vw.append(R)
        dR_over_R = (R - R_central) / R_central
        log(f"  {vw:8.4f}  {eta:12.3e}  {R:8.2f}  {dR_over_R:+10.3f}")

    R_vw = np.array(R_vw)
    dR_vw = (R_vw.max() - R_vw.min()) / R_central
    log(f"\n  v_w: total dR/R = {dR_vw:.3f} = {dR_vw*100:.1f}%")

    # L_w*T sweep
    log(f"\n  L_w*T sweep [{L_w_T_lo:.0f}, {L_w_T_hi:.0f}]:")
    lwt_scan = np.linspace(L_w_T_lo, L_w_T_hi, 21)
    R_lwt = []
    log(f"  {'L_w*T':>8s}  {'eta':>12s}  {'R':>8s}  {'dR/R':>10s}")
    log(f"  {'-'*8}  {'-'*12}  {'-'*8}  {'-'*10}")
    for lwt in lwt_scan:
        eta = compute_eta(D_q_T_central, v_w_central, lwt, vt)
        R, _, _, _ = compute_R_from_eta(eta)
        R_lwt.append(R)
        dR_over_R = (R - R_central) / R_central
        log(f"  {lwt:8.1f}  {eta:12.3e}  {R:8.2f}  {dR_over_R:+10.3f}")

    R_lwt = np.array(R_lwt)
    dR_lwt = (R_lwt.max() - R_lwt.min()) / R_central
    log(f"\n  L_w*T: total dR/R = {dR_lwt:.3f} = {dR_lwt*100:.1f}%")

    # ---------------------------------------------------------------
    # Combined extreme corners
    # ---------------------------------------------------------------
    log(f"\n  --- Combined extreme corners ---")

    corners = [
        ("Central",
         D_q_T_central, v_w_central, L_w_T_central),
        ("Max eta (large D, small v_w, small L)",
         D_q_T_hi, v_w_lo, L_w_T_lo),
        ("Min eta (small D, large v_w, large L)",
         D_q_T_lo, v_w_hi, L_w_T_hi),
    ]

    log(f"\n  {'Case':<45s}  {'P':>8s}  {'eta':>12s}  {'R':>8s}  {'dR/R':>10s}")
    log(f"  {'-'*45}  {'-'*8}  {'-'*12}  {'-'*8}  {'-'*10}")

    R_corners = []
    for name, dqt, vw, lwt in corners:
        P = dqt / (vw * lwt)
        eta = compute_eta(dqt, vw, lwt, vt)
        R, _, _, _ = compute_R_from_eta(eta)
        dR = (R - R_central) / R_central
        R_corners.append(R)
        log(f"  {name:<45s}  {P:8.1f}  {eta:12.3e}  {R:8.2f}  {dR:+10.3f}")

    R_corners = np.array(R_corners)
    dR_combined = (R_corners.max() - R_corners.min()) / R_central
    log(f"\n  Combined corners: total dR/R = {dR_combined:.3f} = {dR_combined*100:.1f}%")

    # ---------------------------------------------------------------
    # WHY this is small: the logarithmic chain
    # ---------------------------------------------------------------
    log(f"\n  --- WHY: the insensitivity chain ---")
    log(f"")
    log(f"  The chain from transport to R has TWO suppression stages:")
    log(f"")
    log(f"  STAGE 1: Transport -> eta")
    log(f"    eta ~ P_transport * (v/T) * exp(-washout)")
    log(f"    At fixed v/T, eta is LINEAR in P = D_q*T / (v_w * L_w*T).")
    log(f"    So d(eta)/eta = dP/P.")
    log(f"")

    # Compute P range
    P_max = D_q_T_hi / (v_w_lo * L_w_T_lo)
    P_min = D_q_T_lo / (v_w_hi * L_w_T_hi)
    log(f"    P ranges from {P_min:.1f} to {P_max:.1f}")
    log(f"    P_max / P_min = {P_max/P_min:.1f}")
    log(f"    So d(eta)/eta spans a factor {P_max/P_min:.1f} at fixed v/T.")
    log(f"")

    log(f"  STAGE 2: eta -> R")
    log(f"    R = Omega_DM / Omega_b = (fixed freeze-out) / (3.65e7 * eta)")
    log(f"    R ~ 1/eta exactly (Omega_DM is independent of eta).")
    log(f"    So dR/R = |d(eta)/eta| = |dP/P|.")
    log(f"")
    log(f"    BUT the question is: does the FULL baryogenesis chain really")
    log(f"    give R varying by this factor? YES -- because at fixed v/T,")
    log(f"    eta is exactly proportional to P, and R is exactly 1/eta.")
    log(f"")
    log(f"    The combined range: R spans [{R_corners.min():.2f}, {R_corners.max():.2f}]")
    log(f"    This is dR/R = {dR_combined*100:.1f}%")

    # ---------------------------------------------------------------
    # But now the REAL question: does this matter?
    # ---------------------------------------------------------------
    log(f"\n  --- THE REAL QUESTION: Does the transport precision matter? ---")
    log(f"")

    # The Sommerfeld factor uncertainty
    S_uncertainty = 0.10  # ~10% from Sommerfeld
    mass_uncertainty = 0.00  # exact (Hamming weights)
    log(f"  Other uncertainty sources in R:")
    log(f"    Sommerfeld factor S: ~10% (from Coulomb approximation)")
    log(f"    Mass ratio m_DM/m_p: EXACT (Hamming weights)")
    log(f"    x_F (freeze-out): ~4% (log-insensitive)")
    log(f"    Boltzmann equation: <1% (proved Stosszahlansatz)")
    log(f"")

    log(f"  Transport contribution to dR/R:")
    log(f"    From D_q*T alone:  {dR_dqt*100:.1f}%")
    log(f"    From v_w alone:    {dR_vw*100:.1f}%")
    log(f"    From L_w*T alone:  {dR_lwt*100:.1f}%")
    log(f"    Combined corners:  {dR_combined*100:.1f}%")
    log(f"")

    # ---------------------------------------------------------------
    # HOWEVER: the above analysis assumed v/T is fixed.
    # The REAL sensitivity is through the baryogenesis self-consistency:
    # at what v/T does eta = eta_obs?
    # ---------------------------------------------------------------
    log(f"\n  --- CRITICAL: THE SELF-CONSISTENCY ARGUMENT ---")
    log(f"")
    log(f"  The above analysis holds v/T FIXED at 0.56.")
    log(f"  But in the full framework, v/T is DERIVED (not adjustable).")
    log(f"  The question is NOT 'at what v/T does eta = eta_obs?'")
    log(f"  The question IS 'what eta does the framework predict at v/T = 0.56?'")
    log(f"")
    log(f"  At fixed v/T = 0.56, the washout factor is FIXED:")
    gbh_fixed = SPH_OVER_H_SYMM * np.exp(-ESPH_COEFF * 0.56)
    surv_fixed = np.exp(-gbh_fixed)
    log(f"    exp(-Gamma_sph(broken)/H) = exp(-{gbh_fixed:.4f}) = {surv_fixed:.6f}")
    log(f"")
    log(f"  So eta = A_framework * P_transport * 0.56 * {surv_fixed:.6f}")
    log(f"  This is EXACTLY proportional to P_transport.")
    log(f"  And R is EXACTLY inversely proportional to eta.")
    log(f"")
    log(f"  CONCLUSION:")
    log(f"  At fixed v/T = 0.56, the transport uncertainty propagates")
    log(f"  LINEARLY into eta and hence into R.")
    log(f"")
    log(f"  The combined transport prefactor P spans [{P_min:.1f}, {P_max:.1f}],")
    log(f"  a factor of {P_max/P_min:.1f}x.")
    log(f"")

    if dR_combined < 0.10:
        log(f"  *** RESULT: dR/R = {dR_combined*100:.1f}% < 10% ***")
        log(f"  The transport precision DOES NOT MATTER.")
        log(f"  R is derived to within 10%, matching the precision of")
        log(f"  the Sommerfeld factor and the mass ratio.")
        lane_closes = True
    else:
        log(f"  *** RESULT: dR/R = {dR_combined*100:.1f}% ***")
        log(f"  The transport uncertainty IS significant.")
        log(f"  R is NOT yet derived to 10% precision from transport alone.")
        log(f"  The lane does NOT close from this argument alone.")
        lane_closes = False

    return {
        "dR_dqt": dR_dqt,
        "dR_vw": dR_vw,
        "dR_lwt": dR_lwt,
        "dR_combined": dR_combined,
        "P_min": P_min,
        "P_max": P_max,
        "R_central": R_central,
        "R_corners": R_corners,
        "eta_central": eta_central,
        "lane_closes": lane_closes,
    }


# =============================================================================
# PART 5: What WOULD close the lane
# =============================================================================

def part5_what_closes(sensitivity):
    """
    If the lane doesn't close from insensitivity, what would close it?
    """
    log("\n" + "=" * 72)
    log("PART 5: HONEST ASSESSMENT AND WHAT WOULD CLOSE THE LANE")
    log("=" * 72)

    dR = sensitivity["dR_combined"]
    P_min = sensitivity["P_min"]
    P_max = sensitivity["P_max"]

    log(f"\n  Transport prefactor P spans [{P_min:.1f}, {P_max:.1f}]")
    log(f"  This is a factor {P_max/P_min:.1f}x range.")
    log(f"  dR/R = {dR*100:.1f}%")

    log(f"\n  The dominant contributor to the P range is v_w:")
    log(f"    v_w spans [0.006, 0.048] -- a factor {0.048/0.006:.0f}x")
    log(f"    D_q*T spans [2.17, 4.03] -- a factor {4.03/2.17:.1f}x")
    log(f"    L_w*T spans [10, 18] -- a factor {18/10:.1f}x")

    # Check: what P range gives dR/R < 10%?
    # dR/R = (P_max - P_min) / P_central
    # For dR/R < 0.10, need P_max/P_min < ~1.10 at central
    # More precisely: (R_max - R_min)/R_central < 0.10
    # Since R ~ 1/P: R_max/R_min = P_max/P_min
    # (R_max - R_min)/R_central ~ (P_max - P_min)/P_central
    # For ~10%: need factor span < ~1.10

    log(f"\n  To get dR/R < 10%, need the P range to span < factor 1.10.")
    log(f"  Current P range spans factor {P_max/P_min:.1f}.")

    if sensitivity["lane_closes"]:
        log(f"\n  THE LANE CLOSES: Transport precision is sufficient.")
        log(f"  R = {sensitivity['R_central']:.2f} +/- {dR*100:.0f}%")
        log(f"  This matches the precision of other derived quantities")
        log(f"  (Sommerfeld factor ~10%, mass ratio EXACT).")
    else:
        log(f"\n  THE LANE DOES NOT CLOSE from insensitivity alone.")
        log(f"  The transport prefactor varies too much ({P_max/P_min:.1f}x).")
        log(f"")
        log(f"  However, the framework DOES derive all transport parameters:")
        log(f"  - D_q*T = 3.1 from HTL lattice (DM_DQT_HTL_NOTE.md)")
        log(f"  - v_w = 0.014 from Boltzmann closure (DM_VW_DERIVATION_NOTE.md)")
        log(f"  - L_w*T = 13 from CW bounce (DM_BOUNCE_WALL_NOTE.md)")
        log(f"")
        log(f"  The wide RANGES come from systematic uncertainties:")
        log(f"  - D_q*T: one-loop skeleton (higher loops ~30%)")
        log(f"  - v_w: nucleation temperature T_n/T_c = 0.95-0.99")
        log(f"  - L_w*T: CW potential uncertainty")
        log(f"")
        log(f"  What would narrow the ranges:")
        log(f"  - NLO D_q*T: ladder resummation (AMY integral equation)")
        log(f"  - Precise T_n: nucleation rate calculation from framework V_eff")
        log(f"  - Or: accept that eta is derived to within a factor ~{P_max/P_min:.0f}x,")
        log(f"    giving R to the same factor. This is an O(1) prediction,")
        log(f"    not a 10% prediction.")

    # Final summary table
    log(f"\n  ============================================================")
    log(f"  FINAL SUMMARY: R UNCERTAINTY BUDGET")
    log(f"  ============================================================")
    log(f"")
    log(f"  {'Source':<35s}  {'dR/R':>8s}  {'Status':<20s}")
    log(f"  {'-'*35}  {'-'*8}  {'-'*20}")
    log(f"  {'Sommerfeld factor':<35s}  {'~10%':>8s}  {'bounded':<20s}")
    log(f"  {'Mass ratio (Hamming)':<35s}  {'0%':>8s}  {'EXACT':<20s}")
    log(f"  {'x_F (freeze-out)':<35s}  {'~4%':>8s}  {'derived (log)':<20s}")
    log(f"  {'Boltzmann equation':<35s}  {'<1%':>8s}  {'proved':<20s}")
    log(f"  {'v/T (EWPT strength)':<35s}  {'~9%':>8s}  {'derived (MC)':<20s}")
    dR_dqt_str = f"{sensitivity['dR_dqt']*100:.0f}%"
    dR_vw_str = f"{sensitivity['dR_vw']*100:.0f}%"
    dR_lwt_str = f"{sensitivity['dR_lwt']*100:.0f}%"
    dR_comb_str = f"{dR*100:.0f}%"
    log(f"  {'D_q*T (quark diffusion)':<35s}  {dR_dqt_str:>8s}  {'derived (HTL)':<20s}")
    log(f"  {'v_w (wall velocity)':<35s}  {dR_vw_str:>8s}  {'derived (Boltzmann)':<20s}")
    log(f"  {'L_w*T (wall thickness)':<35s}  {dR_lwt_str:>8s}  {'derived (CW bounce)':<20s}")
    log(f"  {'COMBINED transport':<35s}  {dR_comb_str:>8s}  {'derived (wide band)':<20s}")
    log(f"  {'-'*35}  {'-'*8}  {'-'*20}")

    # Quadrature for independent uncertainties
    # Note: transport params are NOT independent of each other (they
    # combine into P), so we use the combined corner result, not quadrature.
    other_quad = np.sqrt(0.10**2 + 0.04**2 + 0.09**2)
    total = np.sqrt(other_quad**2 + dR**2)
    log(f"")
    log(f"  Non-transport (quadrature): {other_quad*100:.0f}%")
    log(f"  Total (quadrature):         {total*100:.0f}%")

    return sensitivity["lane_closes"]


# =============================================================================
# MAIN
# =============================================================================

def main():
    log("R = Omega_DM / Omega_b : Sensitivity to Transport Parameters")
    log(f"Date: {time.strftime('%Y-%m-%d %H:%M')}")
    log(f"Script: frontier_dm_r_sensitivity.py")
    log("")

    part1_eta_vs_dqt()
    part2_eta_vs_vw()
    part3_R_vs_eta()
    sensitivity = part4_total_sensitivity()
    closes = part5_what_closes(sensitivity)

    log(f"\n{'=' * 72}")
    if closes:
        log("VERDICT: Lane closes. Transport precision does not limit R.")
    else:
        log("VERDICT: Lane does NOT close from insensitivity. Transport")
        log("prefactor variation is too large. R is an O(1) prediction,")
        log("not a 10% prediction, from transport alone.")
    log(f"{'=' * 72}")

    # Write log
    import os
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    with open(LOG_FILE, "w") as f:
        for line in results:
            f.write(line + "\n")
    log(f"\nLog written to {LOG_FILE}")


if __name__ == "__main__":
    main()
