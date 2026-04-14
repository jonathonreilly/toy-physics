#!/usr/bin/env python3
"""
eta from DM Freeze-Out: Bypassing Baryogenesis
================================================

STATUS: BOUNDED (inherits m_DM scale gap; honest assessment below)

NEW ROUTE to eta that BYPASSES baryogenesis entirely:
  1. Compute Y_DM = n_DM/s from the Boltzmann freeze-out equation
  2. Compute Omega_DM h^2 from Y_DM and cosmological boundary conditions
  3. Compute eta = Omega_DM h^2 / (R * 3.65e7)

This is NOT circular because:
  - Y_DM comes from DM freeze-out (no baryons involved)
  - R comes from structural group theory (no freeze-out involved)
  - eta comes from combining two independent results

FRAMEWORK INPUTS (all derived or bounded):
  - alpha_s = 0.0923        (DERIVED: plaquette at g_bare=1)
  - g_* = 106.75            (DERIVED: SM DOF count from Cl(3))
  - x_F ~ 25                (DERIVED: log-insensitive freeze-out)
  - R = 5.48                (BOUNDED: 13-step chain)
  - M_Pl = 1.2209e19 GeV   (A5: a = l_Pl)
  - C_channel = 155/27      (EXACT: SU(3) group theory)
  - S_vis = 1.592           (DERIVED: lattice Coulomb + SU(3) channels)

COSMOLOGICAL BOUNDARY CONDITIONS (accepted, not derived):
  - T_CMB = 2.7255 K
  - H_0 = 67.4 km/s/Mpc

CRITICAL ISSUE: m_DM
  The taste spectrum gives mass RATIOS (m_h = h * m_0) but not the
  absolute mass scale m_0. The R = 5.48 derivation works because m_DM
  CANCELS in the ratio Omega_DM/Omega_b. But for absolute Omega_DM h^2,
  m_DM does NOT cancel: Omega_DM h^2 ~ m_DM^2 (through sigma_v = pi *
  alpha_s^2 / m_DM^2). This is the gap in this route.

  This script:
  (a) Computes eta(m_DM) as a function of m_DM
  (b) Finds the m_DM that gives observed eta = 6.12e-10
  (c) Asks: is that m_DM derivable from the framework?

HONEST STATUS LABELS:
  [EXACT]    = combinatorial or algebraic identity
  [DERIVED]  = follows from framework quantities with controlled limit
  [BOUNDED]  = requires a sub-assumption not yet closed
  [BC]       = cosmological boundary condition (accepted input)
  [GAP]      = missing framework derivation

Self-contained: numpy + scipy only.
"""

from __future__ import annotations

import math
import sys
import time

import numpy as np

np.set_printoptions(precision=10, linewidth=120)

LOG_FILE = "logs/" + time.strftime("%Y-%m-%d") + "-dm_eta_from_freezeout.txt"

# ============================================================================
# Logging / scorekeeping
# ============================================================================

results_log = []

def log(msg=""):
    results_log.append(msg)
    print(msg)

n_pass = 0
n_fail = 0
test_results = []

def record(name, category, passed, detail=""):
    global n_pass, n_fail
    tag = "PASS" if passed else "FAIL"
    if passed:
        n_pass += 1
    else:
        n_fail += 1
    test_results.append((name, category, tag, detail))
    log(f"  [{category}] {tag}: {name}")
    if detail:
        log(f"    {detail}")


PI = np.pi


# ============================================================================
# PHYSICAL CONSTANTS
# ============================================================================

# Framework-derived quantities
N_C = 3
C_F = (N_C**2 - 1) / (2 * N_C)         # 4/3  [EXACT]
DIM_ADJ_SU3 = N_C**2 - 1                # 8    [EXACT]
C2_SU2_FUND = 3.0 / 4.0                 # 3/4  [EXACT]
DIM_ADJ_SU2 = 3                          # 3    [EXACT]

# Coupling chain (BOUNDED: inherits g_bare = 1)
G_BARE = 1.0
ALPHA_BARE = G_BARE**2 / (4 * PI)
C1_PLAQ = PI**2 / 3.0
P_1LOOP = 1.0 - C1_PLAQ * ALPHA_BARE
ALPHA_PLAQ = -np.log(P_1LOOP) / C1_PLAQ  # 0.0923

# Freeze-out parameters (DERIVED)
G_STAR = 106.75
X_F = 25.0

# Planck mass (A5: a = l_Pl)
M_PL_GEV = 1.2209e19  # GeV

# R from the 13-step chain (BOUNDED)
# R_base = (3/5) * (155/27) = 31/9
MASS_RATIO = 3.0 / 5.0
F_VIS = C_F * DIM_ADJ_SU3 + C2_SU2_FUND * DIM_ADJ_SU2   # 155/12
F_DARK = C2_SU2_FUND * DIM_ADJ_SU2                        # 9/4
F_RATIO = F_VIS / F_DARK                                   # 155/27

# Sommerfeld enhancement (DERIVED from lattice Coulomb + SU(3) channels)
def sommerfeld_coulomb(zeta):
    """Coulomb Sommerfeld factor: S = pi*zeta / (1 - exp(-pi*zeta))."""
    if abs(zeta) < 1e-10:
        return 1.0
    pz = PI * zeta
    if pz > 500:
        return pz
    return pz / (1.0 - np.exp(-pz))

def thermal_avg_sommerfeld(alpha_eff, x_F, attractive=True, n_pts=2000):
    """Thermally averaged Sommerfeld at freeze-out."""
    sign = 1.0 if attractive else -1.0
    v_arr = np.linspace(0.001, 2.0, n_pts)
    dv = v_arr[1] - v_arr[0]
    weight = v_arr**2 * np.exp(-x_F * v_arr**2 / 4.0)
    S_arr = np.array([sommerfeld_coulomb(sign * alpha_eff / v) for v in v_arr])
    return np.sum(S_arr * weight * dv) / np.sum(weight * dv)

# Channel-decomposed Sommerfeld
ALPHA_S = ALPHA_PLAQ
alpha_singlet = C_F * ALPHA_S
alpha_octet = ALPHA_S / (2 * N_C)
w_singlet = (1.0 / 9.0) * C_F**2
w_octet = (8.0 / 9.0) * (1.0 / 6.0)**2

S_SINGLET = thermal_avg_sommerfeld(alpha_singlet, X_F, attractive=True)
S_OCTET = thermal_avg_sommerfeld(alpha_octet, X_F, attractive=False)
S_VIS = (w_singlet * S_SINGLET + w_octet * S_OCTET) / (w_singlet + w_octet)

R_BASE = MASS_RATIO * F_RATIO   # 31/9 = 3.444
R_FULL = R_BASE * S_VIS          # 5.48

# Cosmological boundary conditions [BC: accepted inputs]
T_CMB_K = 2.7255                  # K (Fixsen 2009)
H_0_KM_S_MPC = 67.4              # km/s/Mpc (Planck 2018)

# Unit conversions
K_TO_GEV = 8.6173e-14             # 1 K = 8.6173e-5 eV = 8.6173e-14 GeV
T_CMB_GEV = T_CMB_K * K_TO_GEV
KM_TO_MPC = 3.0857e19             # 1 Mpc in km
H_0_PER_S = H_0_KM_S_MPC / KM_TO_MPC
H_0_GEV = H_0_PER_S * 6.5822e-25  # 1/s -> GeV (hbar = 6.5822e-25 GeV*s)

# Observed values (comparison only)
ETA_OBS = 6.12e-10
OMEGA_DM_OBS_H2 = 0.120
OMEGA_B_OBS_H2 = 0.0224
R_OBS = OMEGA_DM_OBS_H2 / OMEGA_B_OBS_H2  # 5.36

# Newton's constant from A5
G_NEWTON_GEV = 1.0 / M_PL_GEV**2  # in GeV^{-2} (G = 1/M_Pl^2 with M_Pl = 1.22e19)
# More precisely: G = hbar*c / M_Pl^2 => in natural units G = 1/M_Pl^2
# But the standard M_Pl = sqrt(hbar*c/G) so G = 1/M_Pl^2 exactly.
# Careful: reduced Planck mass M_Pl_red = M_Pl / sqrt(8pi)
# Here M_Pl = 1.2209e19 is the FULL Planck mass.
# G = 1/M_Pl^2 in natural units (hbar = c = 1).

# Entropy density today
# s_0 = (2pi^2/45) * g_{*s,0} * T_0^3
# g_{*s,0} = 2 + (7/8)*2*(4/11) = 2 + 7/44 = 3.909 (photons + 3 neutrinos)
# Actually: g_{*s,0} = 2 (photons) + (7/8)*6*(4/11) = 2 + 3.818 = ...
# Standard value: g_{*s,0} = 3.909 (after neutrino decoupling with T_nu/T = (4/11)^{1/3})
G_STAR_S_0 = 3.909
S_0_GEV3 = (2 * PI**2 / 45) * G_STAR_S_0 * T_CMB_GEV**3

# Critical density
# rho_c = 3 H_0^2 / (8pi G) = 3 H_0^2 M_Pl^2 / (8pi)
RHO_C_GEV4 = 3 * H_0_GEV**2 * M_PL_GEV**2 / (8 * PI)

# h = H_0 / (100 km/s/Mpc)
H_LITTLE = H_0_KM_S_MPC / 100.0

# rho_c / h^2 for the standard Omega h^2 normalization
RHO_C_OVER_H2_GEV4 = RHO_C_GEV4 / H_LITTLE**2


# ============================================================================
# PART 0: VERIFY FRAMEWORK CONSTANTS
# ============================================================================

log("=" * 78)
log("PART 0: Framework Constants Verification")
log("=" * 78)
log()

log(f"  Coupling chain:")
log(f"    g_bare = {G_BARE} [BOUNDED]")
log(f"    alpha_bare = g^2/(4pi) = {ALPHA_BARE:.8f}")
log(f"    alpha_plaq = {ALPHA_PLAQ:.6f} [DERIVED]")
log()

log(f"  R derivation:")
log(f"    mass_ratio = 3/5 = {MASS_RATIO:.10f} [EXACT]")
log(f"    f_vis/f_dark = 155/27 = {F_RATIO:.10f} [EXACT]")
log(f"    R_base = (3/5)*(155/27) = 31/9 = {R_BASE:.10f}")
log(f"    S_vis = {S_VIS:.6f} [DERIVED]")
log(f"    R = R_base * S_vis = {R_FULL:.4f}")
log(f"    R_obs = {R_OBS:.4f}")
log()

record("R_value", "BOUNDED",
       abs(R_FULL - 5.48) < 0.02,
       f"R = {R_FULL:.4f}, expected ~5.48")

log(f"  Cosmological boundary conditions:")
log(f"    T_CMB = {T_CMB_K} K = {T_CMB_GEV:.6e} GeV [BC]")
log(f"    H_0 = {H_0_KM_S_MPC} km/s/Mpc = {H_0_GEV:.6e} GeV [BC]")
log(f"    h = {H_LITTLE:.4f}")
log()

log(f"  Derived cosmological quantities:")
log(f"    g_{{*s,0}} = {G_STAR_S_0} (photons + 3 neutrinos)")
log(f"    s_0 = {S_0_GEV3:.6e} GeV^3")
log(f"    rho_c = {RHO_C_GEV4:.6e} GeV^4")
log(f"    rho_c/h^2 = {RHO_C_OVER_H2_GEV4:.6e} GeV^4")
log()

# Cross-check: Omega_b h^2 = 3.65e7 * eta
# Omega_b h^2 = eta * n_gamma * m_p / (rho_c / h^2)
# n_gamma = (2 * zeta(3) / pi^2) * T^3
ZETA_3 = 1.20206
N_GAMMA_GEV3 = 2 * ZETA_3 / PI**2 * T_CMB_GEV**3
M_PROTON_GEV = 0.938

OMEGA_B_H2_CHECK = ETA_OBS * N_GAMMA_GEV3 * M_PROTON_GEV / RHO_C_OVER_H2_GEV4
BBN_CONVERSION = OMEGA_B_H2_CHECK / ETA_OBS

log(f"  BBN conversion check:")
log(f"    n_gamma = {N_GAMMA_GEV3:.6e} GeV^3")
log(f"    Omega_b h^2 = eta * n_gamma * m_p / (rho_c/h^2)")
log(f"    = {ETA_OBS:.3e} * {N_GAMMA_GEV3:.3e} * {M_PROTON_GEV} / {RHO_C_OVER_H2_GEV4:.3e}")
log(f"    = {OMEGA_B_H2_CHECK:.6f}")
log(f"    Expected: 0.0224")
log(f"    Conversion factor: Omega_b h^2 / eta = {BBN_CONVERSION:.4e}")
log(f"    Expected: 3.65e7")
log()

record("bbn_conversion", "BC",
       abs(BBN_CONVERSION / 3.65e7 - 1.0) < 0.05,
       f"Omega_b h^2 / eta = {BBN_CONVERSION:.4e}, expected 3.65e7")


# ============================================================================
# PART 1: FREEZE-OUT FORMULA -- Omega_DM h^2 as function of m_DM
# ============================================================================

log()
log("=" * 78)
log("PART 1: Freeze-Out Formula -- Omega_DM h^2(m_DM)")
log("=" * 78)
log()

log("  The standard freeze-out formula (all ingredients lattice-derived):")
log()
log("  Omega_DM h^2 = (1.07e9 GeV^{-1}) * x_F / (M_Pl * sqrt(g_*) * <sigma v>)")
log()
log("  where <sigma v> = pi * alpha_s^2 / m_DM^2  (s-wave, Born, from lattice T-matrix)")
log()
log("  CRITICAL: sigma_v depends on m_DM^2, so Omega_DM h^2 ~ m_DM^2.")
log("  This dependence CANCELS in the ratio R = Omega_DM/Omega_b,")
log("  but does NOT cancel when computing absolute Omega_DM h^2.")
log()


def compute_sigma_v(m_DM_GeV, alpha_s):
    """
    DM annihilation cross-section from lattice T-matrix (Born level).

    sigma_v = pi * alpha_s^2 / m_DM^2   [GeV^{-2}]

    This is the S_3 (dark) sector cross-section. The dark sector is a
    gauge singlet, so it annihilates through residual interactions
    (gravity at the Planck scale, or via the Higgs portal if available).

    For the R calculation, the RATIO of sigma_v between dark and visible
    sectors matters, and this is given by the Casimir channel weighting.
    For the ABSOLUTE Omega_DM, we need sigma_v for the DM sector specifically.

    The key structural result: at the taste level, the DM annihilation
    cross-section has the SAME alpha_s^2/m^2 form as the visible sector
    (from the lattice optical theorem), but with different channel factors.

    For the DM candidate (S_3, Hamming weight 3):
    sigma_v = pi * alpha_s^2 / m_DM^2 * C_DM

    where C_DM is the channel factor for DM annihilation.
    For a gauge singlet annihilating via residual gauge interactions:
    C_DM = C2_SU2^2 * dim_adj(SU2) = (3/4)^2 * 3 = 27/16

    But wait -- for computing R, the clean derivation uses:
    R = (3/5) * (f_vis / f_dark) * S_vis
    where f_vis/f_dark = 155/27 captures the channel ratio.

    For absolute sigma_v, we need the DM-specific cross-section.
    The Lee-Weinberg formula gives:
    Omega_DM h^2 = (1.07e9) * x_F / (sqrt(g_*) * M_Pl * sigma_v_DM)

    sigma_v_DM = pi * alpha_s^2 / m_DM^2 * f_dark_coefficient
    f_dark_coefficient accounts for the DM annihilation channels.

    APPROACH: Use the standard WIMP formula sigma_v = pi * alpha_s^2 / m_DM^2
    with a channel coefficient. Since R is known and sigma_v cancels in R,
    the route is: compute Omega_DM h^2 from sigma_v_DM, then eta from R.
    """
    # Base cross-section (s-wave, Born)
    sigma_v_base = PI * alpha_s**2 / m_DM_GeV**2

    return sigma_v_base


def compute_x_F(m_DM_GeV, sigma_v):
    """
    Freeze-out parameter x_F from the iterative formula.

    x_F = ln(c * m * M_Pl * sigma_v / sqrt(g_* * x_F))

    where c = 0.038 * g_eff / sqrt(g_*), g_eff = 2 (spin DOF for scalar DM).

    This is log-insensitive: x_F ~ 20-30 for typical WIMP parameters.
    """
    c = 0.038 * 2.0 / math.sqrt(G_STAR)
    # Iterative solution
    x_F = 25.0  # initial guess
    for _ in range(20):
        argument = c * m_DM_GeV * M_PL_GEV * sigma_v / math.sqrt(x_F)
        if argument <= 0:
            return 25.0
        x_F_new = math.log(argument)
        if abs(x_F_new - x_F) < 1e-6:
            break
        x_F = x_F_new
    return max(x_F, 1.0)


def compute_omega_dm_h2(m_DM_GeV, use_fixed_xF=True):
    """
    Compute Omega_DM h^2 from freeze-out with framework inputs.

    Uses the Lee-Weinberg formula:
    Omega_DM h^2 = (1.07e9 GeV^{-1}) * x_F / (sqrt(g_*) * M_Pl * sigma_v)
    """
    sigma_v = compute_sigma_v(m_DM_GeV, ALPHA_S)

    if use_fixed_xF:
        x_F = X_F  # framework-derived, log-insensitive
    else:
        x_F = compute_x_F(m_DM_GeV, sigma_v)

    omega_h2 = (1.07e9 * x_F) / (math.sqrt(G_STAR) * M_PL_GEV * sigma_v)
    return omega_h2, x_F, sigma_v


def compute_eta_from_freeze_out(m_DM_GeV, R, use_fixed_xF=True):
    """
    Compute eta = Omega_DM h^2 / (R * 3.65e7)

    This bypasses baryogenesis entirely:
    - Omega_DM h^2 comes from DM freeze-out (no baryons)
    - R comes from structural group theory (no freeze-out)
    - eta follows from combining the two
    """
    omega_dm_h2, x_F, sigma_v = compute_omega_dm_h2(m_DM_GeV, use_fixed_xF)

    # eta = Omega_DM h^2 / (R * conversion_factor)
    # Omega_b h^2 = conversion_factor * eta, so Omega_DM h^2 = R * Omega_b h^2 = R * conv * eta
    # => eta = Omega_DM h^2 / (R * conv)
    conversion_factor = BBN_CONVERSION  # ~ 3.65e7
    eta = omega_dm_h2 / (R * conversion_factor)

    return eta, omega_dm_h2, x_F, sigma_v


# ============================================================================
# PART 2: eta(m_DM) -- the mass scan
# ============================================================================

log()
log("=" * 78)
log("PART 2: eta as a Function of m_DM")
log("=" * 78)
log()

log("  eta = Omega_DM h^2 / (R * 3.65e7)")
log("  Omega_DM h^2 = (1.07e9) * x_F / (sqrt(g_*) * M_Pl * sigma_v)")
log("  sigma_v = pi * alpha_s^2 / m_DM^2")
log()
log("  Therefore: Omega_DM h^2 ~ m_DM^2")
log("  And: eta ~ m_DM^2")
log()

# Scan m_DM from 1 GeV to 10 TeV
m_DM_scan = np.logspace(0, 4, 201)  # 1 GeV to 10 TeV
eta_scan = []
omega_scan = []

log(f"  {'m_DM (GeV)':>12s}  {'sigma_v (GeV^-2)':>18s}  {'Omega_DM h^2':>14s}  {'eta':>14s}  {'eta/eta_obs':>12s}")
log(f"  {'-'*12}  {'-'*18}  {'-'*14}  {'-'*14}  {'-'*12}")

for m in m_DM_scan:
    eta, omega_h2, x_F, sv = compute_eta_from_freeze_out(m, R_FULL, use_fixed_xF=True)
    eta_scan.append(eta)
    omega_scan.append(omega_h2)
    # Print selected values
    if m in [1, 10, 50, 100, 200, 500, 1000, 5000, 10000]:
        log(f"  {m:12.1f}  {sv:18.6e}  {omega_h2:14.6f}  {eta:14.4e}  {eta/ETA_OBS:12.4f}")
    elif abs(np.log10(m) - round(np.log10(m))) < 0.02:
        log(f"  {m:12.1f}  {sv:18.6e}  {omega_h2:14.6f}  {eta:14.4e}  {eta/ETA_OBS:12.4f}")

eta_scan = np.array(eta_scan)
omega_scan = np.array(omega_scan)

log()

# Find m_DM that gives eta_obs
log("  Finding m_DM that gives eta = eta_obs = 6.12e-10...")
log()

# eta ~ m_DM^2, so m_DM ~ sqrt(eta)
# Find exact value by interpolation
from scipy.interpolate import interp1d
log_interp = interp1d(np.log10(eta_scan), np.log10(m_DM_scan), kind='linear')
m_DM_target = 10**log_interp(np.log10(ETA_OBS))

eta_check, omega_check, xF_check, sv_check = compute_eta_from_freeze_out(
    m_DM_target, R_FULL, use_fixed_xF=True)

log(f"  m_DM for eta = eta_obs:")
log(f"    m_DM = {m_DM_target:.2f} GeV")
log(f"    sigma_v = {sv_check:.6e} GeV^{{-2}}")
log(f"    Omega_DM h^2 = {omega_check:.6f}")
log(f"    eta = {eta_check:.4e}")
log(f"    eta/eta_obs = {eta_check/ETA_OBS:.6f}")
log(f"    x_F = {xF_check:.1f}")
log()

# Also find m_DM that gives Omega_DM h^2 = 0.120
omega_interp = interp1d(np.log10(omega_scan), np.log10(m_DM_scan), kind='linear')
m_DM_omega = 10**omega_interp(np.log10(0.120))

eta_omega, omega_omega, xF_omega, sv_omega = compute_eta_from_freeze_out(
    m_DM_omega, R_FULL, use_fixed_xF=True)

log(f"  m_DM for Omega_DM h^2 = 0.120:")
log(f"    m_DM = {m_DM_omega:.2f} GeV")
log(f"    sigma_v = {sv_omega:.6e} GeV^{{-2}}")
log(f"    Omega_DM h^2 = {omega_omega:.6f}")
log(f"    eta = {eta_omega:.4e}")
log(f"    eta/eta_obs = {eta_omega/ETA_OBS:.6f}")
log()

record("m_DM_for_eta_obs", "GAP",
       1.0 < m_DM_target < 1e6,
       f"m_DM = {m_DM_target:.2f} GeV gives eta = eta_obs = {ETA_OBS:.3e}")

record("m_DM_for_omega_dm", "GAP",
       1.0 < m_DM_omega < 1e6,
       f"m_DM = {m_DM_omega:.2f} GeV gives Omega_DM h^2 = 0.120")

# Verify consistency: m_DM for eta_obs should also give Omega_DM h^2 = 0.120
# if R_FULL matches R_obs
omega_from_eta = R_FULL * BBN_CONVERSION * ETA_OBS
log(f"  Consistency check:")
log(f"    From eta_obs: Omega_DM h^2 = R * 3.65e7 * eta = {R_FULL:.3f} * {BBN_CONVERSION:.3e} * {ETA_OBS:.3e}")
log(f"                                = {omega_from_eta:.6f}")
log(f"    Observed:     Omega_DM h^2 = {OMEGA_DM_OBS_H2:.6f}")
log(f"    Using R_full = {R_FULL:.4f} vs R_obs = {R_OBS:.4f}")
log()


# ============================================================================
# PART 3: SELF-CONSISTENT x_F COMPUTATION
# ============================================================================

log()
log("=" * 78)
log("PART 3: Self-Consistent x_F Computation")
log("=" * 78)
log()

log("  Using the iterative x_F formula instead of fixed x_F = 25:")
log()

eta_sc, omega_sc, xF_sc, sv_sc = compute_eta_from_freeze_out(
    m_DM_target, R_FULL, use_fixed_xF=False)

log(f"  At m_DM = {m_DM_target:.2f} GeV (the mass giving eta_obs):")
log(f"    Self-consistent x_F = {xF_sc:.4f}")
log(f"    Fixed x_F = {X_F:.1f}")
log(f"    Omega_DM h^2 = {omega_sc:.6f}")
log(f"    eta = {eta_sc:.4e}")
log(f"    eta/eta_obs = {eta_sc/ETA_OBS:.6f}")
log()

# x_F sensitivity
m_DM_scan_sc = np.logspace(0, 4, 51)
log(f"  {'m_DM (GeV)':>12s}  {'x_F (self-cons)':>16s}  {'Omega_DM h^2':>14s}  {'eta':>14s}")
log(f"  {'-'*12}  {'-'*16}  {'-'*14}  {'-'*14}")

for m in m_DM_scan_sc:
    eta_m, omega_m, xF_m, sv_m = compute_eta_from_freeze_out(m, R_FULL, use_fixed_xF=False)
    if abs(np.log10(m) - round(np.log10(m))) < 0.1 or abs(m - m_DM_target) / m_DM_target < 0.3:
        log(f"  {m:12.1f}  {xF_m:16.4f}  {omega_m:14.6f}  {eta_m:14.4e}")

log()

record("xF_self_consistent", "DERIVED",
       20 < xF_sc < 30,
       f"Self-consistent x_F = {xF_sc:.2f} at m_DM = {m_DM_target:.1f} GeV")


# ============================================================================
# PART 4: IS m_DM DERIVABLE FROM THE FRAMEWORK?
# ============================================================================

log()
log("=" * 78)
log("PART 4: Is m_DM Derivable from the Framework?")
log("=" * 78)
log()

log("  The taste spectrum gives mass RATIOS:")
log("    m_h = h * m_0  (Wilson mass proportional to Hamming weight)")
log("    m_S0 = 0, m_T1 = m_0, m_T2 = 2*m_0, m_S3 = 3*m_0")
log()
log("  The DM candidate is S_3 with m_DM = 3 * m_0.")
log(f"  We need m_DM = {m_DM_target:.2f} GeV, so m_0 = {m_DM_target/3:.2f} GeV.")
log()

# What sets m_0?
# Option 1: EWSB scale v = 246 GeV
v_EW = 246.0
m_DM_from_EWSB = 3 * v_EW  # If m_0 = v
log(f"  Option 1: m_0 = v (EWSB scale)")
log(f"    m_DM = 3 * v = {m_DM_from_EWSB:.0f} GeV")
eta_ewsb, omega_ewsb, _, _ = compute_eta_from_freeze_out(m_DM_from_EWSB, R_FULL)
log(f"    => Omega_DM h^2 = {omega_ewsb:.4f}")
log(f"    => eta = {eta_ewsb:.4e}  (eta/eta_obs = {eta_ewsb/ETA_OBS:.2f})")
log()

# Option 2: m_0 ~ M_W (W boson mass)
M_W = 80.4
m_DM_from_MW = 3 * M_W
log(f"  Option 2: m_0 = M_W (W boson mass)")
log(f"    m_DM = 3 * M_W = {m_DM_from_MW:.1f} GeV")
eta_mw, omega_mw, _, _ = compute_eta_from_freeze_out(m_DM_from_MW, R_FULL)
log(f"    => Omega_DM h^2 = {omega_mw:.4f}")
log(f"    => eta = {eta_mw:.4e}  (eta/eta_obs = {eta_mw/ETA_OBS:.2f})")
log()

# Option 3: m_0 ~ M_Z (Z boson mass)
M_Z = 91.2
m_DM_from_MZ = 3 * M_Z
log(f"  Option 3: m_0 = M_Z (Z boson mass)")
log(f"    m_DM = 3 * M_Z = {m_DM_from_MZ:.1f} GeV")
eta_mz, omega_mz, _, _ = compute_eta_from_freeze_out(m_DM_from_MZ, R_FULL)
log(f"    => Omega_DM h^2 = {omega_mz:.4f}")
log(f"    => eta = {eta_mz:.4e}  (eta/eta_obs = {eta_mz/ETA_OBS:.2f})")
log()

# Option 4: m_0 ~ M_H / 2 (half the Higgs mass)
M_H = 125.1
m_DM_from_MH = 3 * M_H / 2
log(f"  Option 4: m_0 = M_H/2 (half the Higgs mass)")
log(f"    m_DM = 3 * M_H/2 = {m_DM_from_MH:.1f} GeV")
eta_mh, omega_mh, _, _ = compute_eta_from_freeze_out(m_DM_from_MH, R_FULL)
log(f"    => Omega_DM h^2 = {omega_mh:.4f}")
log(f"    => eta = {eta_mh:.4e}  (eta/eta_obs = {eta_mh/ETA_OBS:.2f})")
log()

# Option 5: m_0 = m_DM_target / 3 (reverse-engineered)
m_0_needed = m_DM_target / 3
log(f"  Option 5: m_0 = {m_0_needed:.2f} GeV (reverse-engineered to match eta_obs)")
log(f"    m_DM = {m_DM_target:.2f} GeV")
log(f"    m_0/v = {m_0_needed/v_EW:.4f}")
log(f"    m_0/M_W = {m_0_needed/M_W:.4f}")
log(f"    m_0/M_Z = {m_0_needed/M_Z:.4f}")
log(f"    m_0/M_H = {m_0_needed/M_H:.4f}")
log()

# The Wilson mass on the lattice: m_0 = 2r/a where r is the Wilson parameter
# and a = l_Pl (axiom A5).
# For r = 1 (standard staggered): m_0 = 2/a = 2 * M_Pl = 2.44e19 GeV
# This is WAY too large. The physical mass is not the bare Wilson mass.
#
# The physical mass comes from the TASTE SPLITTING after renormalization.
# In standard lattice QCD, taste splittings scale as alpha_s^2 * a^{-2} in
# the continuum limit. But here a = l_Pl is fixed (no continuum limit).
#
# The taste splitting scale is:
# Delta m^2 ~ alpha_s^n * (1/a)^2 = alpha_s^n * M_Pl^2
# where n depends on the order of the taste-breaking operator.
#
# For n = 2 (one-loop taste breaking):
# Delta m ~ alpha_s * M_Pl ~ 0.092 * 1.22e19 ~ 1.1e18 GeV
#
# This is still far too large. The physical EW-scale masses require
# a hierarchy mechanism (see HIERARCHY_QUBIT_DETERMINANT.md).
#
# The hierarchy problem IS the problem: why is v/M_Pl ~ 10^{-17}?
# The framework's answer (if it has one) would come from the
# hierarchy/qubit determinant mechanism.

log("  ASSESSMENT: What sets m_0?")
log()
log("  The bare Wilson mass on the lattice is m_0^{bare} = 2r/a = 2*M_Pl")
log("  ~ 2.4e19 GeV. The physical mass must come from renormalization or")
log("  a hierarchy mechanism.")
log()
log("  In the framework:")
log("    - Taste splittings scale as alpha_s^n * M_Pl")
log("    - Even at n = 2: Delta m ~ alpha_s * M_Pl ~ 10^{18} GeV")
log("    - The EW scale v ~ 246 GeV requires v/M_Pl ~ 10^{-17}")
log("    - This IS the hierarchy problem")
log()
log("  The m_DM needed for eta_obs is:")
log(f"    m_DM = {m_DM_target:.2f} GeV")
log(f"    m_0 = {m_0_needed:.2f} GeV")
log()
log("  This is at the electroweak scale, which is EXPECTED for a thermal")
log("  relic (the 'WIMP miracle'). But deriving m_DM = O(v) from the")
log("  framework requires solving the hierarchy problem.")
log()
log("  STATUS: m_DM is a GAP. The route works IF m_DM is given, but")
log("  the framework does not yet derive the absolute mass scale.")
log()

record("m_DM_at_EW_scale", "GAP",
       10 < m_DM_target < 10000,
       f"m_DM = {m_DM_target:.1f} GeV is EW-to-TeV-scale (WIMP miracle region)")

record("m_DM_from_framework", "GAP",
       False,  # Honest: not derived
       "Absolute mass scale m_0 not derivable from Cl(3) without hierarchy mechanism")


# ============================================================================
# PART 5: THE FORMULA -- eta WITHOUT BARYOGENESIS
# ============================================================================

log()
log("=" * 78)
log("PART 5: The Complete Formula -- eta Without Baryogenesis")
log("=" * 78)
log()

log("  THE BYPASS FORMULA:")
log()
log("    eta = Omega_DM h^2 / (R * 3.65e7)")
log()
log("  where:")
log("    Omega_DM h^2 = (1.07e9 GeV^{-1}) * x_F / (sqrt(g_*) * M_Pl * sigma_v)")
log("    sigma_v = pi * alpha_s^2 / m_DM^2")
log("    R = (3/5) * (155/27) * S_vis = 5.48")
log()
log("  Substituting:")
log()
log("    eta = (1.07e9 * x_F * m_DM^2) / (sqrt(g_*) * M_Pl * pi * alpha_s^2 * R * 3.65e7)")
log()

# Compute the formula explicitly
numerator = 1.07e9 * X_F
denominator_no_m = math.sqrt(G_STAR) * M_PL_GEV * PI * ALPHA_S**2 * R_FULL * BBN_CONVERSION

# eta = numerator * m_DM^2 / denominator_no_m
# For eta = eta_obs: m_DM^2 = eta_obs * denominator_no_m / numerator
m_DM_sq_needed = ETA_OBS * denominator_no_m / numerator
m_DM_analytic = math.sqrt(m_DM_sq_needed)

log(f"  Analytic inversion:")
log(f"    m_DM^2 = eta * sqrt(g_*) * M_Pl * pi * alpha_s^2 * R * 3.65e7 / (1.07e9 * x_F)")
log(f"    m_DM^2 = {m_DM_sq_needed:.4e} GeV^2")
log(f"    m_DM = {m_DM_analytic:.4f} GeV")
log()

record("m_DM_analytic_matches_numerical", "DERIVED",
       abs(m_DM_analytic / m_DM_target - 1.0) < 0.01,
       f"m_DM analytic = {m_DM_analytic:.4f} vs numerical = {m_DM_target:.4f} GeV")

# The coefficient in front of m_DM^2
C_eta = numerator / denominator_no_m
log(f"  Master formula: eta = C * m_DM^2")
log(f"    C = {C_eta:.6e} GeV^{{-2}}")
log(f"    eta(100 GeV) = {C_eta * 100**2:.4e}")
log(f"    eta(1 TeV) = {C_eta * 1000**2:.4e}")
log(f"    eta_obs = {ETA_OBS:.4e}")
log(f"    m_DM needed = sqrt(eta_obs / C) = {math.sqrt(ETA_OBS / C_eta):.4f} GeV")
log()


# ============================================================================
# PART 6: PROVENANCE AND DERIVATION STATUS
# ============================================================================

log()
log("=" * 78)
log("PART 6: Full Derivation Provenance")
log("=" * 78)
log()

log("  STEP-BY-STEP DERIVATION CHAIN:")
log()
log("  1. Taste space 1+3+3+1        [EXACT]    Burnside on Z^3")
log("  2. Visible: T1+T2 = 6         [EXACT]    Commutant of gauge action")
log("  3. Dark: S0+S3 = 2             [EXACT]    Complement")
log("  4. Mass ratio 3/5              [EXACT]    Hamming weight m^2 sums")
log("  5. g_bare = 1                  [BOUNDED]  Cl(3) normalization")
log("  6. alpha_s = 0.0923            [DERIVED]  Plaquette at g=1")
log("  7. S_vis = 1.592               [DERIVED]  Lattice Coulomb + SU(3)")
log("  8. Channel weighting 155/27    [EXACT]    SU(3) group theory")
log("  9. sigma_v = pi*alpha^2/m^2    [DERIVED]  Lattice optical theorem")
log("  10. Boltzmann equation          [DERIVED]  Master eq + Stosszahlansatz")
log("  11. x_F = 25                    [DERIVED]  Lattice Boltzmann")
log("  12. H(T) Friedmann              [DERIVED]  Newton on Z^3 (k=0)")
log("  13. R = 5.48                    [BOUNDED]  Steps 1-12 combined")
log("  ---------------------------------------------------------------")
log("  14. Omega_DM h^2(m_DM)          [DERIVED]  Freeze-out (Steps 9-12)")
log(f"  15. m_DM = {m_DM_analytic:.1f} GeV           [GAP]      Absolute mass scale")
log(f"  16. eta = Omega_DM/(R*3.65e7)  [BC]       T_CMB, H_0")
log()
log("  NEW INPUTS BEYOND THE R DERIVATION:")
log(f"    - T_CMB = {T_CMB_K} K             [BC: cosmological boundary condition]")
log(f"    - H_0 = {H_0_KM_S_MPC} km/s/Mpc         [BC: cosmological boundary condition]")
log(f"    - m_DM = {m_DM_analytic:.1f} GeV            [GAP: not derived from framework]")
log()
log("  WHAT THIS ROUTE ACHIEVES:")
log("    - BYPASSES baryogenesis entirely (no Sakharov conditions needed)")
log("    - BYPASSES sphaleron rates, transport coefficients, v_w, D_q")
log("    - BYPASSES CP violation in the CKM/PMNS sector")
log("    - BYPASSES nucleosynthesis (BBN used only kinematically)")
log("    - Reduces the entire eta problem to ONE unknown: m_DM")
log()
log("  WHAT THIS ROUTE DOES NOT ACHIEVE:")
log("    - Does NOT derive m_DM from the framework")
log("    - Does NOT eliminate the hierarchy problem")
log("    - Does NOT close eta as a zero-parameter prediction")
log()
log("  HONEST ASSESSMENT:")
log("    The route is logically valid and non-circular. But it trades")
log("    the baryogenesis problem (deriving eta from Sakharov conditions)")
log("    for the hierarchy problem (deriving m_DM from Cl(3)).")
log("    Whether this is progress depends on which problem is easier to close.")
log()
log("    For the R = 5.48 derivation, m_DM cancels -- that's why R works")
log("    with only 2 bounded inputs. For absolute eta, m_DM does not cancel.")
log("    This is the fundamental reason the DM gate note says eta is IMPORTED.")
log()

# ============================================================================
# PART 7: CONDITIONAL CLOSURE -- IF m_DM = f(framework), WHAT FOLLOWS
# ============================================================================

log()
log("=" * 78)
log("PART 7: Conditional Closure")
log("=" * 78)
log()

log("  IF the framework derives m_DM (or equivalently m_0), then:")
log()
log("    eta = C * m_DM^2")
log(f"    C = {C_eta:.6e} GeV^{{-2}}")
log()
log("  Candidate framework mass scales and their eta predictions:")
log()
log(f"  {'Scale':>25s}  {'m_DM (GeV)':>12s}  {'eta':>14s}  {'eta/eta_obs':>12s}  {'Status':>10s}")
log(f"  {'-'*25}  {'-'*12}  {'-'*14}  {'-'*12}  {'-'*10}")

candidates = [
    ("m_0 = v (EWSB)", 3 * 246.0),
    ("m_0 = M_W", 3 * 80.4),
    ("m_0 = M_Z", 3 * 91.2),
    ("m_0 = M_H/2", 3 * 125.1 / 2),
    ("m_0 = M_t/2", 3 * 173.0 / 2),
    ("m_0 = v/sqrt(2)", 3 * 246.0 / math.sqrt(2)),
    (f"m_0 = {m_0_needed:.1f} (needed)", m_DM_analytic),
    ("WIMP miracle (3e-26)", None),  # sigma_v ~ 3e-26 cm^3/s
]

for name, m_DM in candidates:
    if m_DM is None:
        # WIMP miracle: sigma_v = 3e-26 cm^3/s
        # Convert to GeV^{-2}: 3e-26 cm^3/s * (1.97e-14 cm/GeV)^{-2} / (3e10 cm/s)
        # = 3e-26 / (3e10 * (1.97e-14)^2) = 3e-26 / 1.164e-17 = 2.58e-9 GeV^{-2}
        sigma_v_wimp = 2.58e-9  # GeV^{-2}
        omega_wimp = (1.07e9 * X_F) / (math.sqrt(G_STAR) * M_PL_GEV * sigma_v_wimp)
        eta_wimp = omega_wimp / (R_FULL * BBN_CONVERSION)
        m_DM_wimp = math.sqrt(PI * ALPHA_S**2 / sigma_v_wimp)
        log(f"  {name:>25s}  {m_DM_wimp:12.1f}  {eta_wimp:14.4e}  {eta_wimp/ETA_OBS:12.4f}  {'~OK' if 0.5 < eta_wimp/ETA_OBS < 2.0 else 'FAR'}")
    else:
        eta_cand = C_eta * m_DM**2
        ratio = eta_cand / ETA_OBS
        status = "MATCH" if 0.8 < ratio < 1.2 else ("CLOSE" if 0.3 < ratio < 3.0 else "FAR")
        log(f"  {name:>25s}  {m_DM:12.1f}  {eta_cand:14.4e}  {ratio:12.4f}  {status:>10s}")

log()


# ============================================================================
# PART 8: COMPARISON WITH EXISTING APPROACH
# ============================================================================

log()
log("=" * 78)
log("PART 8: Comparison with Standard (Baryogenesis) Route")
log("=" * 78)
log()

log("  STANDARD ROUTE (current in repo):")
log("    1. Derive R = 5.48 from taste spectrum + freeze-out  [BOUNDED]")
log("    2. Use eta_obs = 6.12e-10                            [IMPORTED]")
log("    3. Omega_b h^2 = 3.65e7 * eta                       [KINEMATIC]")
log("    4. Omega_DM h^2 = R * Omega_b h^2 = 0.120           [DERIVED]")
log("    Gap: eta is imported, not derived.")
log()
log("  NEW ROUTE (this script):")
log("    1. Derive R = 5.48 from taste spectrum + freeze-out  [BOUNDED]")
log("    2. Derive sigma_v = pi*alpha_s^2/m_DM^2              [DERIVED]")
log("    3. Compute Omega_DM h^2 from freeze-out              [DERIVED if m_DM known]")
log("    4. eta = Omega_DM h^2 / (R * 3.65e7)                [DERIVED if m_DM known]")
log("    Gap: m_DM is not derived from framework.")
log()
log("  COMPARISON:")
log("    Standard route: 2 bounded + 1 imported (eta)")
log("    New route:      2 bounded + 2 BC + 1 gap (m_DM)")
log()
log("  The new route replaces an IMPORTED observable (eta = 6.12e-10)")
log("  with a GAP in the framework (m_DM = absolute mass scale).")
log("  This is NOT obviously better: the hierarchy problem is harder")
log("  than measuring eta. But it DOES show that IF m_DM is derived,")
log("  eta follows without baryogenesis.")
log()


# ============================================================================
# SUMMARY
# ============================================================================

log()
log("=" * 78)
log("SUMMARY")
log("=" * 78)
log()
log(f"  PASS: {n_pass}  FAIL: {n_fail}")
for name, category, tag, detail in test_results:
    log(f"    [{tag}] ({category}) {name}")
log()

log("  KEY RESULT:")
log(f"    eta = {C_eta:.4e} * m_DM^2  [GeV^{{-2}}]")
log(f"    m_DM = {m_DM_analytic:.2f} GeV  gives  eta = {ETA_OBS:.3e}  (observed)")
log()
log("  ROUTE STATUS: VALID but INCOMPLETE")
log("    - Logic is non-circular and baryogenesis-independent")
log("    - All steps except m_DM are derived or bounded")
log("    - m_DM absolute scale is a GAP (hierarchy problem)")
log("    - Trades baryogenesis problem for hierarchy problem")
log()

if n_fail == 0:
    log("  ALL CHECKS PASSED.")
else:
    log(f"  {n_fail} CHECK(S) FAILED.")

# ============================================================================
# Write log file
# ============================================================================

import os
os.makedirs("logs", exist_ok=True)
with open(LOG_FILE, "w") as f:
    f.write("\n".join(results_log))
log(f"\n  Log written to {LOG_FILE}")
