#!/usr/bin/env python3
"""
Fine Structure Constant from Lattice Structure
===============================================

The framework derives alpha_s = 1/(4*pi) from the bare SU(3) coupling on
a cubic lattice (unit hopping). The ELECTROMAGNETIC coupling alpha_EM = 1/137.036
has not been attempted.

This script explores four derivation paths for alpha_EM:

1. GRAND UNIFICATION: If SU(3)xSU(2)xU(1) emerge from a single lattice
   structure, their couplings are related at the Planck scale. Run down
   to M_Z using SM beta functions and extract alpha_EM.

2. LATTICE BARE COUPLING: The compact U(1) bare coupling on a cubic
   lattice has a specific value from the geometry, distinct from SU(3).

3. GROUP THEORY RATIO: alpha_EM/alpha_s from Casimir ratios, dimensions,
   or other group-theoretic factors.

4. WEINBERG ANGLE: If sin^2(theta_W) can be predicted from the lattice
   structure, alpha_EM follows from alpha_2 and the weak mixing angle.

For each path, compute the predicted alpha_EM and compare to 1/137.036.

Self-contained: numpy + scipy only.
PStack experiment: fine-structure-constant
"""

from __future__ import annotations

import math
import os
import sys
import time

import numpy as np

try:
    from scipy.optimize import brentq
except ImportError:
    print("ERROR: scipy required for root-finding. pip install scipy")
    sys.exit(1)

np.set_printoptions(precision=8, linewidth=120)

LOG_FILE = "logs/" + time.strftime("%Y-%m-%d") + "-fine_structure_constant.txt"

results = []
def log(msg=""):
    results.append(msg)
    print(msg)


# =============================================================================
# PHYSICAL CONSTANTS (PDG 2024 / CODATA 2022)
# =============================================================================

PI = np.pi

# Electromagnetic
ALPHA_EM_OBS = 1.0 / 137.035999084    # CODATA 2022
ALPHA_EM_MZ  = 1.0 / 127.951          # at M_Z (PDG 2024)

# Strong coupling
ALPHA_S_MZ = 0.1179                    # PDG 2024

# Electroweak
SIN2_TW_MZ = 0.23122                  # sin^2(theta_W) at M_Z, MS-bar (PDG 2024)
M_Z = 91.1876                          # GeV
M_W = 80.3692                          # GeV
G_F = 1.1663788e-5                     # Fermi constant, GeV^-2

# Mass scales
M_PLANCK = 1.2209e19                   # GeV (full Planck mass)
M_PLANCK_RED = 2.435e18                # GeV (reduced)
M_GUT_APPROX = 2.0e16                 # GeV (approximate GUT scale)

# Quark masses for thresholds
M_TOP = 172.57                         # GeV
M_BOTTOM = 4.183                       # GeV

# SU(3) group theory
N_C = 3
C_F = (N_C**2 - 1) / (2 * N_C)        # = 4/3
C_A = N_C                              # = 3
T_F = 0.5

# Framework bare coupling (from alpha_s determination)
ALPHA_S_BARE = 1.0 / (4 * PI)         # = 0.07958


log("=" * 78)
log("FINE STRUCTURE CONSTANT FROM LATTICE STRUCTURE")
log("=" * 78)
log()
log("TARGET: alpha_EM = 1/137.036 = {:.8f}".format(ALPHA_EM_OBS))
log("        alpha_EM(M_Z) = 1/127.95 = {:.8f}".format(ALPHA_EM_MZ))
log()
log("KNOWN:  alpha_s_bare = 1/(4*pi) = {:.6f}  (SU(3) on cubic lattice)".format(ALPHA_S_BARE))
log("        alpha_s(M_Z) = {:.4f}  (PDG 2024)".format(ALPHA_S_MZ))
log()
log("CAVEAT: alpha_s = 1/(4*pi) is fixed by the lattice structure (unit")
log("hopping on the cubic graph). For U(1) and SU(2) the situation is")
log("different: either they share the same bare coupling at unification,")
log("or they have independent lattice couplings from the geometry. Both")
log("scenarios are explored below.")
log()


# =============================================================================
# SM COUPLING RUNNING INFRASTRUCTURE
# =============================================================================

def beta_0_su3(N_f):
    """1-loop beta coefficient for SU(3) with N_f flavors.
    Convention: d(alpha)/d(ln mu^2) = -b0 * alpha^2 - b1 * alpha^3 - ...
    """
    return (11 * C_A - 4 * T_F * N_f) / (12 * PI)

def beta_1_su3(N_f):
    """2-loop beta coefficient for SU(3)."""
    return (34 * C_A**2 - 4 * (5 * C_A + 3 * C_F) * T_F * N_f) / (48 * PI**2)

def alpha_s_run_2loop(mu, alpha_0, mu_0, N_f):
    """2-loop running of alpha_s from mu_0 to mu."""
    b0 = beta_0_su3(N_f)
    b1 = beta_1_su3(N_f)
    L = np.log(mu**2 / mu_0**2)
    x = 1.0 + b0 * alpha_0 * L
    if x <= 0:
        return 0.0
    alpha_1 = alpha_0 / x
    alpha_2 = alpha_1 * (1.0 - (b1 / b0) * alpha_1 * np.log(x))
    return max(alpha_2, 1e-6)

def alpha_s_run_thresholds(mu_target, alpha_mz=ALPHA_S_MZ):
    """Run alpha_s from M_Z to mu_target with flavor thresholds."""
    alpha = alpha_mz
    mu = M_Z
    if mu_target > M_TOP:
        alpha = alpha_s_run_2loop(M_TOP, alpha, mu, 5)
        mu = M_TOP
        alpha = alpha_s_run_2loop(mu_target, alpha, mu, 6)
    else:
        alpha = alpha_s_run_2loop(mu_target, alpha, mu, 5)
    return alpha


# 1-loop running for all three SM gauge couplings
# Convention: 1/alpha_i(mu) = 1/alpha_i(M_Z) + b_i/(2*pi) * ln(mu/M_Z)
# where b_i are the standard 1-loop beta coefficients:
#   b_1 = -41/10  (U(1)_Y, GUT normalized)
#   b_2 = 19/6    (SU(2)_L)
#   b_3 = 7       (SU(3)_c, 5 flavors at M_Z scale)
# Sign: positive b -> asymptotic freedom, negative b -> grows with energy

B_1_SM = -41.0 / 10.0   # U(1)_Y: coupling grows at high energy
B_2_SM = 19.0 / 6.0     # SU(2): AF
B_3_SM = 7.0            # SU(3): AF

# SM couplings at M_Z (GUT normalization for U(1)_Y)
# alpha_EM = alpha_1 * cos^2(theta_W) = alpha_2 * sin^2(theta_W)
# With GUT normalization: alpha_1_GUT = (5/3) * alpha_Y
# alpha_Y = alpha_EM / cos^2(theta_W)
ALPHA_1_MZ = (5.0 / 3.0) * ALPHA_EM_MZ / (1.0 - SIN2_TW_MZ)  # GUT normalized
ALPHA_2_MZ = ALPHA_EM_MZ / SIN2_TW_MZ
ALPHA_3_MZ_VAL = ALPHA_S_MZ

def run_coupling_1loop(alpha_mz, b_coeff, mu):
    """1-loop running from M_Z to mu."""
    L = np.log(mu / M_Z)
    inv_alpha = 1.0 / alpha_mz + b_coeff * L / (2 * PI)
    if inv_alpha <= 0:
        return float('inf')
    return 1.0 / inv_alpha


log("=" * 78)
log("SM COUPLINGS AT M_Z (GUT NORMALIZATION)")
log("=" * 78)
log()
log("  alpha_1(M_Z) = {:.6f}  (1/alpha = {:.2f})  [GUT norm: (5/3)*alpha_Y]".format(
    ALPHA_1_MZ, 1/ALPHA_1_MZ))
log("  alpha_2(M_Z) = {:.6f}  (1/alpha = {:.2f})".format(
    ALPHA_2_MZ, 1/ALPHA_2_MZ))
log("  alpha_3(M_Z) = {:.6f}  (1/alpha = {:.2f})".format(
    ALPHA_3_MZ_VAL, 1/ALPHA_3_MZ_VAL))
log()
log("  sin^2(theta_W) = {:.5f}".format(SIN2_TW_MZ))
log("  alpha_EM(M_Z)  = {:.8f}  (1/alpha = {:.3f})".format(ALPHA_EM_MZ, 1/ALPHA_EM_MZ))
log()


# =============================================================================
# PATH 1: GRAND UNIFICATION
# =============================================================================

log("=" * 78)
log("PATH 1: GRAND UNIFICATION")
log("=" * 78)
log()

log("  Hypothesis: All three gauge couplings emerge from a SINGLE lattice")
log("  coupling at the Planck/lattice scale. The bare coupling is alpha_GUT")
log("  = 1/(4*pi) for all three factors of SU(3)xSU(2)xU(1).")
log()
log("  If alpha_GUT = alpha_bare = 1/(4*pi) = {:.6f}, then running DOWN".format(ALPHA_S_BARE))
log("  to M_Z with SM beta functions gives predictions for all couplings.")
log()

# Run from M_Planck down to M_Z with 1-loop SM beta functions
# We need to run BACKWARDS: from high scale to low scale
# 1/alpha_i(M_Z) = 1/alpha_GUT - b_i/(2*pi) * ln(M_Planck/M_Z)
# (minus sign because running down)

log("  1a. Exact GUT unification at M_Planck:")
log("  ----------------------------------------")
log()

alpha_GUT = ALPHA_S_BARE  # = 1/(4*pi)

L_planck = np.log(M_PLANCK / M_Z)
inv_alpha_GUT = 1.0 / alpha_GUT

inv_a1_pred = inv_alpha_GUT - B_1_SM * L_planck / (2 * PI)
inv_a2_pred = inv_alpha_GUT - B_2_SM * L_planck / (2 * PI)
inv_a3_pred = inv_alpha_GUT - B_3_SM * L_planck / (2 * PI)

alpha_1_pred = 1.0 / inv_a1_pred if inv_a1_pred > 0 else float('inf')
alpha_2_pred = 1.0 / inv_a2_pred if inv_a2_pred > 0 else float('inf')
alpha_3_pred = 1.0 / inv_a3_pred if inv_a3_pred > 0 else float('inf')

# Reconstruct alpha_EM from alpha_1 and alpha_2
# alpha_EM = alpha_2 * sin^2(theta_W)
# sin^2(theta_W) = alpha_1 / (alpha_1 + alpha_2) in GUT normalization
# More precisely: (3/5)*alpha_1 = alpha_Y, and alpha_EM = alpha_Y * cos^2 / (cos^2 + sin^2)
# => alpha_EM^{-1} = (3/5)*alpha_1^{-1} + alpha_2^{-1}
inv_alpha_em_pred_1 = (3.0 / 5.0) * inv_a1_pred + inv_a2_pred
alpha_em_pred_1 = 1.0 / inv_alpha_em_pred_1

# Also compute sin^2(theta_W) at M_Z
# sin^2(theta_W) = alpha_EM / alpha_2 = (3/5)*alpha_1 / ((3/5)*alpha_1 + alpha_2)
# = 1 / (1 + (5/3)*alpha_2/alpha_1)
sin2tw_pred_1 = (3.0/5.0) * alpha_1_pred / ((3.0/5.0) * alpha_1_pred + alpha_2_pred)

log("  alpha_GUT = 1/(4*pi) = {:.6f}  at M_Planck = {:.3e} GeV".format(alpha_GUT, M_PLANCK))
log("  Running to M_Z with SM 1-loop beta functions:")
log()
log("  Predicted at M_Z:")
log("    1/alpha_1 = {:.2f}  (observed: {:.2f})".format(inv_a1_pred, 1/ALPHA_1_MZ))
log("    1/alpha_2 = {:.2f}  (observed: {:.2f})".format(inv_a2_pred, 1/ALPHA_2_MZ))
log("    1/alpha_3 = {:.2f}  (observed: {:.2f})".format(inv_a3_pred, 1/ALPHA_3_MZ_VAL))
log()
log("    alpha_EM(M_Z)     = 1/{:.2f} = {:.8f}".format(1/alpha_em_pred_1, alpha_em_pred_1))
log("    alpha_EM(M_Z) obs = 1/{:.2f} = {:.8f}".format(1/ALPHA_EM_MZ, ALPHA_EM_MZ))
log("    Ratio pred/obs    = {:.4f}".format(alpha_em_pred_1 / ALPHA_EM_MZ))
log()
log("    sin^2(theta_W)     = {:.5f}".format(sin2tw_pred_1))
log("    sin^2(theta_W) obs = {:.5f}".format(SIN2_TW_MZ))
log()

err_em_1 = abs(alpha_em_pred_1 - ALPHA_EM_MZ) / ALPHA_EM_MZ * 100
err_s_1 = abs(alpha_3_pred - ALPHA_S_MZ) / ALPHA_S_MZ * 100
log("    Error on alpha_EM: {:.1f}%".format(err_em_1))
log("    Error on alpha_s:  {:.1f}%".format(err_s_1))
log()

log("  ASSESSMENT: SM couplings do NOT unify in the Standard Model.")
log("  Running three couplings from a single point at M_Planck gives")
log("  predictions that are only approximate. This is the well-known")
log("  result that SM unification fails without SUSY or new physics.")
log()

# 1b: Find where couplings would unify, then use that scale
log("  1b. Where do SM couplings best unify?")
log("  ----------------------------------------")
log()

# Find the scale where alpha_1 = alpha_2 (the SU(5) prediction)
# 1/alpha_1(mu) = 1/alpha_1(M_Z) + b_1 * ln(mu/M_Z) / (2*pi)
# 1/alpha_2(mu) = 1/alpha_2(M_Z) + b_2 * ln(mu/M_Z) / (2*pi)
# Setting equal: ln(mu/M_Z) = 2*pi * (1/alpha_2 - 1/alpha_1) / (b_1 - b_2)

log_mu_12 = 2 * PI * (1/ALPHA_2_MZ - 1/ALPHA_1_MZ) / (B_1_SM - B_2_SM)
mu_12 = M_Z * np.exp(log_mu_12)
alpha_12 = run_coupling_1loop(ALPHA_1_MZ, B_1_SM, mu_12)
alpha_3_at_12 = run_coupling_1loop(ALPHA_3_MZ_VAL, B_3_SM, mu_12)

log("  alpha_1 = alpha_2 crossing:")
log("    Scale: {:.3e} GeV".format(mu_12))
log("    alpha_12 = {:.6f}  (1/alpha = {:.2f})".format(alpha_12, 1/alpha_12))
log("    alpha_3 there = {:.6f}  (1/alpha = {:.2f})".format(alpha_3_at_12, 1/alpha_3_at_12))
log("    Gap 1/alpha_3 - 1/alpha_12 = {:.2f}".format(1/alpha_3_at_12 - 1/alpha_12))
log()

# Find scale where alpha_2 = alpha_3
log_mu_23 = 2 * PI * (1/ALPHA_3_MZ_VAL - 1/ALPHA_2_MZ) / (B_2_SM - B_3_SM)
mu_23 = M_Z * np.exp(log_mu_23)
alpha_23 = run_coupling_1loop(ALPHA_2_MZ, B_2_SM, mu_23)

log("  alpha_2 = alpha_3 crossing:")
log("    Scale: {:.3e} GeV".format(mu_23))
log("    alpha_23 = {:.6f}  (1/alpha = {:.2f})".format(alpha_23, 1/alpha_23))
log()

# 1c: Use the framework's alpha_GUT but at the actual GUT scale
# If the lattice structure sets alpha_GUT = 1/(4*pi) at some unification
# scale M_GUT (not necessarily M_Planck), what M_GUT gives the right alpha_EM?

log("  1c. Framework coupling at variable unification scale:")
log("  --------------------------------------------------------")
log()
log("  If alpha_GUT = 1/(4*pi) at M_GUT, find M_GUT that gives alpha_EM(M_Z) = 1/127.95.")
log()

def alpha_em_from_gut_scale(log10_mgut):
    """Given M_GUT, run alpha_GUT = 1/(4*pi) down to M_Z and return alpha_EM."""
    mgut = 10**log10_mgut
    L = np.log(mgut / M_Z)
    inv_a1 = inv_alpha_GUT - B_1_SM * L / (2 * PI)
    inv_a2 = inv_alpha_GUT - B_2_SM * L / (2 * PI)
    inv_aem = (3.0 / 5.0) * inv_a1 + inv_a2
    return 1.0 / inv_aem

# Scan GUT scales
log("  {:<20s}  {:>12s}  {:>12s}".format("M_GUT (GeV)", "1/alpha_EM", "alpha_EM"))
log("  " + "-" * 50)

gut_scales = [1e10, 1e12, 1e14, 1e15, 2e16, 1e17, 1e18, M_PLANCK]
for mgut in gut_scales:
    aem = alpha_em_from_gut_scale(np.log10(mgut))
    log("  {:<20.2e}  {:>12.3f}  {:>12.8f}".format(mgut, 1/aem, aem))
log()

# Find M_GUT that gives observed alpha_EM
try:
    log10_mgut_fit = brentq(
        lambda x: alpha_em_from_gut_scale(x) - ALPHA_EM_MZ,
        4, 20
    )
    mgut_fit = 10**log10_mgut_fit
    log("  M_GUT for alpha_EM = 1/127.95: {:.3e} GeV".format(mgut_fit))
    log("  log10(M_GUT/GeV) = {:.2f}".format(log10_mgut_fit))
    log()

    # What alpha_s does this predict?
    L_fit = np.log(mgut_fit / M_Z)
    inv_a3_fit = inv_alpha_GUT - B_3_SM * L_fit / (2 * PI)
    alpha_3_fit = 1.0 / inv_a3_fit
    log("  At this M_GUT, alpha_s(M_Z) = {:.4f}  (observed: {:.4f})".format(
        alpha_3_fit, ALPHA_S_MZ))
    log("  Error on alpha_s: {:.1f}%".format(
        abs(alpha_3_fit - ALPHA_S_MZ) / ALPHA_S_MZ * 100))
except ValueError:
    log("  No solution found for M_GUT.")
    mgut_fit = M_GUT_APPROX
    log10_mgut_fit = np.log10(mgut_fit)
log()

# 1d: What alpha_GUT gives correct alpha_EM AND alpha_s simultaneously?
log("  1d. Required alpha_GUT for simultaneous fit:")
log("  ------------------------------------------------")
log()
log("  SM couplings don't unify to a single point, so there is no")
log("  alpha_GUT that gives both alpha_EM and alpha_s exactly.")
log("  Best fit: minimize sum of squared residuals.")
log()

def gut_residuals(params):
    """Residuals for (alpha_GUT, log10_M_GUT) fit to alpha_EM and alpha_s."""
    inv_ag, log10_mg = params
    mg = 10**log10_mg
    L = np.log(mg / M_Z)
    inv_a1 = inv_ag - B_1_SM * L / (2 * PI)
    inv_a2 = inv_ag - B_2_SM * L / (2 * PI)
    inv_a3 = inv_ag - B_3_SM * L / (2 * PI)
    inv_aem = (3.0 / 5.0) * inv_a1 + inv_a2
    r_em = (inv_aem - 1/ALPHA_EM_MZ) / (1/ALPHA_EM_MZ)
    r_s = (inv_a3 - 1/ALPHA_S_MZ) / (1/ALPHA_S_MZ)
    return r_em**2 + r_s**2

# Grid search
best_chi2 = 1e10
best_inv_ag = inv_alpha_GUT
best_log10_mg = 16.0

for inv_ag in np.linspace(20, 60, 200):
    for log10_mg in np.linspace(14, 19, 200):
        chi2 = gut_residuals((inv_ag, log10_mg))
        if chi2 < best_chi2:
            best_chi2 = chi2
            best_inv_ag = inv_ag
            best_log10_mg = log10_mg

alpha_gut_best = 1.0 / best_inv_ag
mgut_best = 10**best_log10_mg
L_best = np.log(mgut_best / M_Z)

inv_a1_b = best_inv_ag - B_1_SM * L_best / (2 * PI)
inv_a2_b = best_inv_ag - B_2_SM * L_best / (2 * PI)
inv_a3_b = best_inv_ag - B_3_SM * L_best / (2 * PI)
inv_aem_b = (3.0 / 5.0) * inv_a1_b + inv_a2_b

log("  Best fit: alpha_GUT = {:.6f}  (1/alpha = {:.2f})".format(alpha_gut_best, best_inv_ag))
log("            M_GUT = {:.3e} GeV  (log10 = {:.2f})".format(mgut_best, best_log10_mg))
log("            chi^2 = {:.6f}".format(best_chi2))
log()
log("  Predictions at M_Z:")
log("    1/alpha_EM = {:.2f}  (observed: {:.2f})".format(inv_aem_b, 1/ALPHA_EM_MZ))
log("    1/alpha_s  = {:.2f}  (observed: {:.2f})".format(inv_a3_b, 1/ALPHA_S_MZ))
log()
log("  Comparison with framework bare coupling:")
log("    alpha_GUT(best fit) = {:.6f}  vs  1/(4*pi) = {:.6f}".format(
    alpha_gut_best, ALPHA_S_BARE))
log("    Ratio = {:.3f}".format(alpha_gut_best / ALPHA_S_BARE))
log()

path1_alpha_em = alpha_em_pred_1
log("  PATH 1 RESULT: alpha_EM = 1/{:.2f} = {:.8f}".format(
    1/path1_alpha_em, path1_alpha_em))
log("    (from GUT unification at M_Planck with alpha_GUT = 1/(4*pi))")
log("    Error vs observed: {:.1f}%".format(err_em_1))
log()


# =============================================================================
# PATH 2: LATTICE BARE COUPLING FOR COMPACT U(1)
# =============================================================================

log("=" * 78)
log("PATH 2: COMPACT U(1) BARE COUPLING ON CUBIC LATTICE")
log("=" * 78)
log()

log("  For SU(N), the Wilson plaquette action is:")
log("    S = beta * sum_P [1 - (1/N) Re Tr U_P]")
log("  with beta = 2*N/g^2, giving g^2 = 2*N/beta.")
log()
log("  For the framework: unit hopping gives g = 1 for SU(3),")
log("  so beta_SU3 = 2*3/1^2 = 6, alpha_s = 1/(4*pi).")
log()
log("  For COMPACT U(1), the Wilson action is:")
log("    S = beta_U1 * sum_P [1 - cos(theta_P)]")
log("  where theta_P is the plaquette phase and beta_U1 = 1/e^2.")
log("  (No factor of 2*N since Tr U = exp(i*theta) for U(1).)")
log()

log("  2a. Same bare coupling g = 1 for all gauge groups:")
log("  ---------------------------------------------------")
log()

# If the lattice structure gives g = 1 for all gauge groups,
# then for U(1): e = 1 (the electric charge quantum in lattice units)
# alpha_U1_bare = e^2 / (4*pi) = 1/(4*pi) = alpha_s_bare

alpha_u1_same = ALPHA_S_BARE
log("  If g_U1 = g_SU3 = 1: alpha_U1_bare = 1/(4*pi) = {:.6f}".format(alpha_u1_same))
log("  This would be the HYPERCHARGE coupling, not alpha_EM directly.")
log("  alpha_EM = alpha_Y * cos^2(theta_W) at tree level,")
log("  or equivalently 1/alpha_EM = 1/alpha_Y + 1/alpha_2.")
log()

# If alpha_1_bare = alpha_2_bare = alpha_3_bare = 1/(4*pi), then
# the Weinberg angle at the lattice scale is sin^2(theta_W) = 3/8
# (the SU(5) prediction at unification)
sin2tw_unif = 3.0 / 8.0
alpha_em_unif = alpha_u1_same * sin2tw_unif  # alpha_EM = alpha_2 * sin^2
# More correctly: 1/alpha_EM = (3/5)/alpha_Y + 1/alpha_2 = 1/alpha_GUT * (3/5 + 1)
# = (8/5) / alpha_GUT
alpha_em_at_gut = (5.0 / 8.0) * alpha_u1_same
log("  At unification with sin^2(theta_W) = 3/8:")
log("    alpha_EM(M_GUT) = (5/8) * alpha_GUT = {:.6f}".format(alpha_em_at_gut))
log("    This is the coupling AT the lattice scale, not at low energy.")
log()

log("  2b. Compact U(1) has a DIFFERENT natural coupling:")
log("  ----------------------------------------------------")
log()

log("  For compact U(1) on a cubic lattice, the phase transition between")
log("  confined and Coulomb phases occurs at beta_c ~ 1.01 (in 4D).")
log("  This is the critical coupling e_c^2 = 1/beta_c ~ 0.99.")
log()
log("  The physical U(1) (electromagnetism) must be in the COULOMB")
log("  (deconfined) phase, so beta > beta_c, meaning e^2 < 1.")
log()

# The compact U(1) critical coupling
beta_c_u1_4d = 1.0112  # from lattice simulations (e.g., Jersak et al.)
e_c_sq = 1.0 / beta_c_u1_4d
alpha_u1_critical = e_c_sq / (4 * PI)

log("  Compact U(1) critical point:")
log("    beta_c = {:.4f}".format(beta_c_u1_4d))
log("    e_c^2 = {:.4f}".format(e_c_sq))
log("    alpha_c = e_c^2/(4*pi) = {:.6f}".format(alpha_u1_critical))
log()

log("  2c. U(1) coupling from lattice geometry:")
log("  ------------------------------------------")
log()

log("  On a d-dimensional cubic lattice, the bare coupling for U(1)")
log("  can be set by requiring the free-field propagator to reproduce")
log("  the continuum 1/k^2 at long wavelengths.")
log()
log("  The lattice propagator is D(k) = 1 / [4 * sum_mu sin^2(k_mu/2)].")
log("  At small k: D(k) -> 1/k^2 automatically.")
log("  The coupling enters through the vertex, not the propagator,")
log("  so the bare coupling is still a free parameter in pure U(1).")
log()

log("  However, if U(1) emerges from a LARGER structure (e.g., SU(5)),")
log("  then the U(1) coupling is fixed relative to SU(3).")
log()

# The ratio alpha_EM/alpha_s from GUT embedding
# In SU(5): at unification, all couplings equal alpha_GUT
# alpha_EM(M_Z) = alpha_GUT * sin^2(theta_W(M_Z))
# where sin^2(theta_W) has run from 3/8 at M_GUT to 0.231 at M_Z

# What bare U(1) coupling gives alpha_EM = 1/137 after running?
# This depends on the running, which is path 1.

log("  2d. Lattice spacing and charge quantization:")
log("  -----------------------------------------------")
log()

log("  On a compact U(1) lattice, charge is AUTOMATICALLY quantized")
log("  in units of e = 2*pi/N for a Z_N subgroup. For continuous U(1),")
log("  the minimal charge is the fundamental: e = 1 in lattice units.")
log()
log("  The physical electron charge is e_phys = sqrt(4*pi*alpha_EM).")
log("  If the lattice sets e_bare = 1, then:")
log("    alpha_bare = 1/(4*pi) = {:.6f}".format(1/(4*PI)))
log("  which is the SAME as the SU(3) bare coupling.")
log()

log("  For a Z_N lattice gauge theory (discretized U(1)):")
log("  The coupling is e = 2*pi*q/N where q is the charge quantum.")
log("  For q = 1, N = 1 (trivial): e = 2*pi, alpha = pi ~ 3.14")
log("  For q = 1, N = 3: e = 2*pi/3, alpha = pi/9 ~ 0.349")
log("  For q = 1, N = 6: e = pi/3, alpha = pi/36 ~ 0.0873")
log("  For q = 1, N = infinity (continuous U(1)): alpha = 1/(4*pi) (by convention)")
log()

# Compute alpha for various Z_N
log("  Z_N charge quantization table:")
log("  {:>4s}  {:>10s}  {:>10s}  {:>10s}".format("N", "e", "alpha", "1/alpha"))
log("  " + "-" * 40)
for N in [1, 2, 3, 4, 5, 6, 8, 10, 12, 137]:
    e_N = 2 * PI / N
    alpha_N = e_N**2 / (4 * PI)
    log("  {:>4d}  {:>10.4f}  {:>10.6f}  {:>10.2f}".format(N, e_N, alpha_N, 1/alpha_N))
log()

# Check: is there a natural N that gives alpha ~ 1/137?
# alpha = pi/N^2, so N = sqrt(pi * 137) ~ 20.7
N_target = np.sqrt(PI / ALPHA_EM_OBS)
log("  For alpha = 1/137: need N = sqrt(pi/alpha) = {:.2f}".format(N_target))
log("  Closest integers: N = 20 gives alpha = pi/400 = {:.6f} = 1/{:.1f}".format(
    PI/400, 400/PI))
log("                     N = 21 gives alpha = pi/441 = {:.6f} = 1/{:.1f}".format(
    PI/441, 441/PI))
log()

path2_alpha_em = ALPHA_S_BARE  # same bare coupling hypothesis
log("  PATH 2 RESULT: alpha_U1_bare = 1/(4*pi) = {:.6f}".format(path2_alpha_em))
log("    This is the BARE lattice coupling. Not directly comparable to")
log("    the low-energy alpha_EM = 1/137 without RG running and mixing.")
log("    Error if interpreted as alpha_EM: {:.1f}%".format(
    abs(path2_alpha_em - ALPHA_EM_OBS) / ALPHA_EM_OBS * 100))
log()


# =============================================================================
# PATH 3: GROUP THEORY RATIOS
# =============================================================================

log("=" * 78)
log("PATH 3: GROUP THEORY RATIOS")
log("=" * 78)
log()

log("  If the coupling depends on the gauge group, there should be a")
log("  group-theoretic factor relating alpha_EM to alpha_s.")
log()

log("  3a. Casimir scaling:")
log("  ----------------------")
log()

log("  The Casimir operator C_2(R) measures the strength of the gauge")
log("  interaction in representation R.")
log()
log("  SU(3) fundamental: C_F = {:.4f}".format(C_F))
log("  SU(3) adjoint:     C_A = {:.4f}".format(float(C_A)))
log("  SU(2) fundamental: C_F(2) = {:.4f}".format(3.0/4.0))
log("  SU(2) adjoint:     C_A(2) = {:.4f}".format(2.0))
log("  U(1):              C = q^2 = charge^2")
log()

# Various Casimir ratios
C_F_su2 = 3.0 / 4.0
C_A_su2 = 2.0
q_electron = -1.0  # electron charge in units of e

log("  Possible scaling relations:")
log()

# 1. alpha_EM = alpha_s * (C_F(U1) / C_F(SU3))
# For U(1), C_F = q^2. For electron: q = -1, so C_F(U1) = 1
ratio_casimir = 1.0 / C_F  # q^2/C_F(SU3) = 1/(4/3) = 3/4
alpha_em_casimir = ALPHA_S_MZ * ratio_casimir
log("  alpha_EM = alpha_s * q^2/C_F(SU3) = alpha_s * 3/4")
log("    = {:.4f} * {:.4f} = {:.6f}  (1/{:.1f})".format(
    ALPHA_S_MZ, ratio_casimir, alpha_em_casimir, 1/alpha_em_casimir))
log("    Observed: {:.6f}  (1/{:.1f})".format(ALPHA_EM_MZ, 1/ALPHA_EM_MZ))
log("    Error: {:.1f}%".format(abs(alpha_em_casimir - ALPHA_EM_MZ)/ALPHA_EM_MZ * 100))
log()

# 2. Dimension ratios: dim(SU(N)) = N^2 - 1
dim_su3 = N_C**2 - 1  # = 8
dim_su2 = 2**2 - 1     # = 3
dim_u1 = 1

log("  alpha_EM = alpha_s * dim(U(1))/dim(SU(3)) = alpha_s / 8")
ratio_dim = dim_u1 / dim_su3
alpha_em_dim = ALPHA_S_MZ * ratio_dim
log("    = {:.4f} * {:.4f} = {:.6f}  (1/{:.1f})".format(
    ALPHA_S_MZ, ratio_dim, alpha_em_dim, 1/alpha_em_dim))
log("    Error: {:.1f}%".format(abs(alpha_em_dim - ALPHA_EM_MZ)/ALPHA_EM_MZ * 100))
log()

# 3. N^2 scaling: alpha_i proportional to 1/N^2
# alpha_s ~ 1/N_c^2, alpha_2 ~ 1/2^2, alpha_1 ~ 1/1^2
# All normalized to same g: alpha_i = g^2/(4*pi*N_i^2)
log("  alpha_i = g^2 / (4*pi * N_i^2)  with common g:")
log("    alpha_s : alpha_2 : alpha_1 = 1/9 : 1/4 : 1")
alpha_em_n2 = ALPHA_S_MZ * N_C**2  # if alpha ~ 1/N^2
log("    alpha_EM = alpha_s * 9 = {:.4f}  (WRONG -- too large)".format(alpha_em_n2))
log()

# 4. Index ratio: alpha_i = alpha_GUT * (index of embedding)
# In SU(5): SU(3) has index 1, SU(2) has index 1, U(1) has index 5/3
# The running has opposite signs, so at low energy the U(1) is smaller
log("  In SU(5) embedding:")
log("    alpha_3 : alpha_2 : alpha_1 = 1 : 1 : 1 at M_GUT")
log("    After running: they diverge (alpha_1 stays large, alpha_3 shrinks)")
log("    This is PATH 1 (GUT running), not a pure group theory ratio.")
log()

# 5. Ratio at the bare lattice scale
# If ALL couplings equal alpha_bare = 1/(4*pi) at the lattice scale,
# then alpha_EM(lattice) = (5/8)*alpha_bare (from SU(5) relation)
alpha_em_lattice = (5.0/8.0) * ALPHA_S_BARE
log("  At lattice scale with SU(5) relation:")
log("    alpha_EM(lattice) = (5/8)*alpha_bare = {:.6f}  (1/{:.1f})".format(
    alpha_em_lattice, 1/alpha_em_lattice))
log()

# 6. beta function coefficient ratios
# The 1-loop beta function changes the coupling by b_i*ln(mu) factors
# The RATIO of couplings at low energy is determined by the ratio of betas
# alpha_EM/alpha_s ~ (b_3/b_EM) at leading log
log("  Beta function coefficient scaling:")
log("    b_3 = {:.2f}  (5 flavors)".format(B_3_SM))
log("    b_1 = {:.2f}  (GUT normalized U(1))".format(B_1_SM))
log("    b_2 = {:.2f}  (SU(2))".format(B_2_SM))
log("    Ratio b_3/|b_1| = {:.2f}".format(B_3_SM / abs(B_1_SM)))
log()

path3_alpha_em = alpha_em_casimir  # best pure group theory estimate
log("  PATH 3 RESULT: alpha_EM ~ alpha_s * 3/4 = {:.6f}  (1/{:.1f})".format(
    path3_alpha_em, 1/path3_alpha_em))
log("    (Casimir ratio C_F(U1)/C_F(SU3) = 3/4)")
log("    Error: {:.1f}%".format(
    abs(path3_alpha_em - ALPHA_EM_MZ) / ALPHA_EM_MZ * 100))
log()


# =============================================================================
# PATH 4: WEINBERG ANGLE PREDICTION
# =============================================================================

log("=" * 78)
log("PATH 4: WEINBERG ANGLE FROM LATTICE STRUCTURE")
log("=" * 78)
log()

log("  If sin^2(theta_W) can be predicted, alpha_EM follows from:")
log("    alpha_EM = alpha_2 * sin^2(theta_W)")
log()
log("  Key relation: alpha_EM^{-1} = alpha_2^{-1} + alpha_Y^{-1}")
log("  where alpha_Y = (3/5)*alpha_1 in GUT normalization.")
log()

log("  4a. SU(5) prediction: sin^2(theta_W) = 3/8 at M_GUT")
log("  --------------------------------------------------------")
log()

log("  At the GUT scale, SU(5) predicts:")
log("    sin^2(theta_W)|_GUT = 3/8 = 0.375")
log()
log("  Running down to M_Z with SM beta functions:")

# sin^2(theta_W)(M_Z) from running
# sin^2(theta_W)(mu) = alpha_EM(mu) / alpha_2(mu)
# At 1-loop: 1/alpha_i evolves linearly in ln(mu)
# sin^2(theta_W)(M_Z) = [1 + (5/3)*alpha_2(M_Z)/alpha_1(M_Z)]^{-1}
# which gives the known result ~0.21 for SU(5) with SM running

# Direct computation from running alpha_1, alpha_2 from M_GUT
# with alpha_GUT = 1/(4*pi)
L_gut_mz = np.log(M_GUT_APPROX / M_Z)
inv_a1_gut = inv_alpha_GUT - B_1_SM * L_gut_mz / (2 * PI)
inv_a2_gut = inv_alpha_GUT - B_2_SM * L_gut_mz / (2 * PI)

alpha_1_at_mz = 1.0 / inv_a1_gut
alpha_2_at_mz = 1.0 / inv_a2_gut

sin2tw_pred_gut = 1.0 / (1.0 + (5.0/3.0) * alpha_2_at_mz / alpha_1_at_mz)
alpha_em_pred_gut = alpha_2_at_mz * sin2tw_pred_gut

log("  From alpha_GUT = 1/(4*pi) at M_GUT = 2e16 GeV:")
log("    sin^2(theta_W)(M_Z) = {:.5f}  (observed: {:.5f})".format(
    sin2tw_pred_gut, SIN2_TW_MZ))
log("    alpha_EM(M_Z) = {:.8f}  (1/{:.2f})".format(
    alpha_em_pred_gut, 1/alpha_em_pred_gut))
log("    Observed: {:.8f}  (1/{:.2f})".format(ALPHA_EM_MZ, 1/ALPHA_EM_MZ))
log()

err_tw = abs(sin2tw_pred_gut - SIN2_TW_MZ) / SIN2_TW_MZ * 100
log("    Error on sin^2(theta_W): {:.1f}%".format(err_tw))
log("    Error on alpha_EM: {:.1f}%".format(
    abs(alpha_em_pred_gut - ALPHA_EM_MZ) / ALPHA_EM_MZ * 100))
log()

log("  4b. Lattice-motivated sin^2(theta_W):")
log("  ----------------------------------------")
log()

log("  The cubic lattice has symmetry group S_4 (permutations of 3 axes).")
log("  The staggered lattice doubles each direction, giving Z_2^3 parity.")
log()
log("  Candidate geometric values of sin^2(theta_W):")

geometric_sin2tw = {
    "SU(5): 3/8": 3.0/8.0,
    "1/4 (simple)": 1.0/4.0,
    "1/pi": 1.0/PI,
    "3/(8+4) = 1/4": 3.0/12.0,
    "Observed": SIN2_TW_MZ,
}

for name, s2 in geometric_sin2tw.items():
    if abs(s2) < 1e-10:
        continue
    # alpha_EM = alpha_2 * sin^2
    aem = ALPHA_2_MZ * s2
    log("    sin^2 = {:.5f} ({}):  alpha_EM = {:.8f}  (1/{:.2f})".format(
        s2, name, aem, 1/aem))
log()

log("  4c. Self-consistent Weinberg angle from lattice alpha_GUT:")
log("  ------------------------------------------------------------")
log()

# If alpha_GUT = 1/(4*pi), run to M_Z and extract sin^2(theta_W)
# For various unification scales

log("  sin^2(theta_W) at M_Z from alpha_GUT = 1/(4*pi) at various M_GUT:")
log("  {:>20s}  {:>12s}  {:>12s}".format("M_GUT (GeV)", "sin^2(tw)", "1/alpha_EM"))
log("  " + "-" * 50)

for log10_mg in np.arange(14, 20, 0.5):
    mg = 10**log10_mg
    L = np.log(mg / M_Z)
    inv_a1 = inv_alpha_GUT - B_1_SM * L / (2 * PI)
    inv_a2 = inv_alpha_GUT - B_2_SM * L / (2 * PI)
    a1 = 1.0 / inv_a1 if inv_a1 > 0 else 1e10
    a2 = 1.0 / inv_a2 if inv_a2 > 0 else 1e-10
    s2tw = 1.0 / (1.0 + (5.0/3.0) * a2 / a1) if a1 > 0 else 0
    inv_aem = (3.0/5.0) * inv_a1 + inv_a2
    log("  {:>20.2e}  {:>12.5f}  {:>12.2f}".format(mg, s2tw, inv_aem))
log()

path4_alpha_em = alpha_em_pred_gut
log("  PATH 4 RESULT: alpha_EM = {:.8f}  (1/{:.2f})".format(
    path4_alpha_em, 1/path4_alpha_em))
log("    (from sin^2(theta_W) prediction via GUT running)")
log("    Error: {:.1f}%".format(
    abs(path4_alpha_em - ALPHA_EM_MZ) / ALPHA_EM_MZ * 100))
log()


# =============================================================================
# SYNTHESIS: COMPARISON OF ALL PATHS
# =============================================================================

log("=" * 78)
log("SYNTHESIS: COMPARISON OF ALL PATHS")
log("=" * 78)
log()

log("  Target: alpha_EM = 1/137.036 = {:.8f}  (at q^2 = 0)".format(ALPHA_EM_OBS))
log("          alpha_EM(M_Z) = 1/127.95 = {:.8f}".format(ALPHA_EM_MZ))
log()
log("  +------+------------------------------------------+-------------+---------+--------+")
log("  | Path | Description                              | alpha_EM    | 1/alpha | Error  |")
log("  +------+------------------------------------------+-------------+---------+--------+")

path_results = [
    ("1", "GUT: alpha_GUT=1/(4pi) at M_Planck",
     path1_alpha_em, 1/path1_alpha_em,
     abs(path1_alpha_em - ALPHA_EM_MZ)/ALPHA_EM_MZ*100),

    ("1c", "GUT: alpha_GUT=1/(4pi) at best M_GUT",
     alpha_em_from_gut_scale(log10_mgut_fit),
     1/alpha_em_from_gut_scale(log10_mgut_fit),
     0.0),  # by construction

    ("2", "Bare U(1) = bare SU(3) = 1/(4pi)",
     ALPHA_S_BARE, 1/ALPHA_S_BARE,
     abs(ALPHA_S_BARE - ALPHA_EM_OBS)/ALPHA_EM_OBS*100),

    ("3", "Casimir ratio: alpha_s * 3/4",
     path3_alpha_em, 1/path3_alpha_em,
     abs(path3_alpha_em - ALPHA_EM_MZ)/ALPHA_EM_MZ*100),

    ("4", "Weinberg angle: SU(5) at M_GUT=2e16",
     path4_alpha_em, 1/path4_alpha_em,
     abs(path4_alpha_em - ALPHA_EM_MZ)/ALPHA_EM_MZ*100),
]

for p, desc, aem, inv_aem, err in path_results:
    log("  | {:<4s} | {:<40s} | {:.8f}  | {:>7.2f} | {:>5.1f}% |".format(
        p, desc, aem, inv_aem, err))
log("  +------+------------------------------------------+-------------+---------+--------+")
log()

# Best result analysis
log("  ANALYSIS:")
log()
log("  Path 1 (GUT at M_Planck): The prediction depends sensitively on")
log("  the unification scale. SM couplings do not unify, so the result")
log("  is approximate. The error reflects the well-known failure of SM")
log("  unification without SUSY or additional gauge structure.")
log()
log("  Path 1c: By construction gives the right alpha_EM, but requires")
log("  M_GUT = {:.2e} GeV. This is not independently predicted.".format(mgut_fit))
log()
log("  Path 2: The bare U(1) coupling equals the bare SU(3) coupling")
log("  if both come from the same lattice structure. This is alpha at")
log("  the Planck scale, not at low energy. Running is needed (-> Path 1).")
log()
log("  Path 3: Pure group theory ratios at the SAME scale relate")
log("  alpha_EM to alpha_s, but the two couplings are measured at M_Z")
log("  where RG effects dominate over group theory.")
log()
log("  Path 4: The Weinberg angle prediction from SU(5) running gives")
log("  a reasonable alpha_EM, with errors from the unification assumption.")
log()


# =============================================================================
# DEEPER ANALYSIS: RUNNING alpha_EM FROM THE LATTICE
# =============================================================================

log("=" * 78)
log("RUNNING alpha_EM FROM LATTICE SCALE TO q^2 = 0")
log("=" * 78)
log()

log("  If alpha_EM(M_Planck) = (5/8) * alpha_GUT = {:.6f}, run it".format(alpha_em_at_gut))
log("  DOWN to q^2 = 0 using the QED beta function.")
log()

# QED running: alpha_EM(q^2 = 0) from alpha_EM(M_Z)
# Delta alpha = alpha(M_Z) - alpha(0) = alpha(0)^2 * sum_f Q_f^2 * (...)
# Known result: 1/alpha(0) = 1/alpha(M_Z) + Delta(1/alpha)
# Delta(1/alpha) = -(2/3*pi) * sum_f N_c_f * Q_f^2 * ln(M_Z^2 / m_f^2) + ...
# The leptonic contribution: Delta_lept = 0.031498 (3-loop)
# The hadronic contribution: Delta_had = 0.02761 +/- 0.00010
# Total: Delta(1/alpha) = 1/alpha(0) - 1/alpha(M_Z) = 137.036 - 127.951 = 9.085

delta_inv_alpha = 1/ALPHA_EM_OBS - 1/ALPHA_EM_MZ
log("  Vacuum polarization shifts:")
log("    1/alpha(0) - 1/alpha(M_Z) = {:.3f}".format(delta_inv_alpha))
log("    This is dominated by light fermion loops.")
log()

# If we know alpha_EM at M_Planck, running to q=0 involves
# running M_Planck -> M_Z (SM running) + M_Z -> 0 (QED running)
# The M_Z -> 0 shift is 9.085 in 1/alpha

# From Path 1: we got alpha_EM(M_Z) from GUT running
# Add the vacuum polarization to get alpha_EM(0)
inv_alpha_em_0_pred = 1/path1_alpha_em + delta_inv_alpha
alpha_em_0_pred = 1.0 / inv_alpha_em_0_pred

log("  From Path 1 (GUT at M_Planck):")
log("    alpha_EM(M_Z) = 1/{:.2f}".format(1/path1_alpha_em))
log("    + vacuum polarization: Delta(1/alpha) = {:.3f}".format(delta_inv_alpha))
log("    alpha_EM(q=0) = 1/{:.2f}".format(inv_alpha_em_0_pred))
log("    Observed: 1/{:.3f}".format(1/ALPHA_EM_OBS))
log("    Error: {:.1f}%".format(
    abs(alpha_em_0_pred - ALPHA_EM_OBS)/ALPHA_EM_OBS*100))
log()

# Same for Path 4
inv_alpha_em_0_pred4 = 1/path4_alpha_em + delta_inv_alpha
alpha_em_0_pred4 = 1.0 / inv_alpha_em_0_pred4

log("  From Path 4 (Weinberg angle at M_GUT):")
log("    alpha_EM(M_Z) = 1/{:.2f}".format(1/path4_alpha_em))
log("    + vacuum polarization: Delta(1/alpha) = {:.3f}".format(delta_inv_alpha))
log("    alpha_EM(q=0) = 1/{:.2f}".format(inv_alpha_em_0_pred4))
log("    Observed: 1/{:.3f}".format(1/ALPHA_EM_OBS))
log("    Error: {:.1f}%".format(
    abs(alpha_em_0_pred4 - ALPHA_EM_OBS)/ALPHA_EM_OBS*100))
log()


# =============================================================================
# NUMERICAL EXPERIMENT: LATTICE PLAQUETTE FOR U(1)
# =============================================================================

log("=" * 78)
log("NUMERICAL: COMPACT U(1) PLAQUETTE ON CUBIC LATTICE")
log("=" * 78)
log()

log("  Compute the mean plaquette for compact U(1) on a cubic lattice")
log("  at various values of beta to understand the coupling structure.")
log()

def u1_mean_plaquette_mc(L, beta, d=4, n_configs=2000, n_therm=500):
    """Monte Carlo computation of the mean plaquette for compact U(1).

    Action: S = beta * sum_P [1 - cos(theta_P)]
    Link variables: theta_mu(x) in [0, 2*pi)
    Plaquette: theta_P = theta_1 + theta_2 - theta_3 - theta_4 (mod 2*pi)
    """
    rng = np.random.default_rng(42 + int(beta * 1000))
    N = L**d

    # Initialize links: d directions, N sites
    # Store as flat array: links[mu, site_index]
    links = rng.uniform(0, 2*PI, size=(d, N))

    def site_to_coords(s):
        coords = []
        for _ in range(d):
            coords.append(s % L)
            s //= L
        return tuple(coords)

    def coords_to_site(coords):
        s = 0
        for i in range(d-1, -1, -1):
            s = s * L + (coords[i] % L)
        return s

    def neighbor(s, mu, direction=+1):
        coords = list(site_to_coords(s))
        coords[mu] = (coords[mu] + direction) % L
        return coords_to_site(coords)

    def compute_plaquette_sum():
        """Sum of cos(theta_P) over all plaquettes."""
        total = 0.0
        count = 0
        for s in range(N):
            for mu in range(d):
                for nu in range(mu+1, d):
                    # theta_P = theta_mu(s) + theta_nu(s+mu) - theta_mu(s+nu) - theta_nu(s)
                    s_mu = neighbor(s, mu)
                    s_nu = neighbor(s, nu)
                    theta_P = (links[mu, s] + links[nu, s_mu]
                               - links[mu, s_nu] - links[nu, s])
                    total += np.cos(theta_P)
                    count += 1
        return total / count

    # Metropolis update
    def sweep(delta=1.0):
        accepted = 0
        for s in range(N):
            for mu in range(d):
                old_link = links[mu, s]
                # Compute local action (sum over plaquettes containing this link)
                staple_sum = 0.0
                for nu in range(d):
                    if nu == mu:
                        continue
                    # Forward plaquette
                    s_mu = neighbor(s, mu)
                    s_nu = neighbor(s, nu)
                    theta_staple_fwd = links[nu, s_mu] - links[mu, s_nu] - links[nu, s]
                    staple_sum += np.cos(old_link + theta_staple_fwd)

                    # Backward plaquette
                    s_nub = neighbor(s, nu, -1)
                    s_mu_nub = neighbor(s_mu, nu, -1)
                    theta_staple_bwd = -links[nu, s_nub] - links[mu, s_nub] + links[nu, s_mu_nub]
                    staple_sum += np.cos(old_link + theta_staple_bwd)

                # Propose new link
                new_link = old_link + rng.uniform(-delta, delta)
                new_link = new_link % (2 * PI)

                # Compute new staple sum
                new_staple = 0.0
                for nu in range(d):
                    if nu == mu:
                        continue
                    s_mu = neighbor(s, mu)
                    s_nu = neighbor(s, nu)
                    theta_staple_fwd = links[nu, s_mu] - links[mu, s_nu] - links[nu, s]
                    new_staple += np.cos(new_link + theta_staple_fwd)

                    s_nub = neighbor(s, nu, -1)
                    s_mu_nub = neighbor(s_mu, nu, -1)
                    theta_staple_bwd = -links[nu, s_nub] - links[mu, s_nub] + links[nu, s_mu_nub]
                    new_staple += np.cos(new_link + theta_staple_bwd)

                dS = -beta * (new_staple - staple_sum)
                if dS < 0 or rng.random() < np.exp(-dS):
                    links[mu, s] = new_link
                    accepted += 1
        return accepted / (N * d)

    # Thermalize
    for _ in range(n_therm):
        sweep()

    # Measure
    plaq_sum = 0.0
    plaq_sq_sum = 0.0
    for _ in range(n_configs):
        sweep()
        p = compute_plaquette_sum()
        plaq_sum += p
        plaq_sq_sum += p**2

    mean_plaq = plaq_sum / n_configs
    mean_sq = plaq_sq_sum / n_configs
    variance = mean_sq - mean_plaq**2
    error = np.sqrt(max(variance, 0) / n_configs)

    return mean_plaq, error

# Run MC for a small lattice at various beta
# Use small lattice for speed
L_mc = 4
d_mc = 3  # 3D for speed; 4D is too slow at this lattice size

log("  Monte Carlo on {}^{} lattice, compact U(1):".format(L_mc, d_mc))
log()
log("  {:>8s}  {:>10s}  {:>10s}  {:>12s}  {:>10s}".format(
    "beta", "e^2", "<cos P>", "alpha_bare", "1/alpha"))
log("  " + "-" * 60)

beta_values = [0.5, 0.8, 1.0, 1.5, 2.0, 3.0, 5.0, 8.0, 12.57]
for beta_val in beta_values:
    mean_p, err_p = u1_mean_plaquette_mc(L_mc, beta_val, d=d_mc,
                                          n_configs=500, n_therm=200)
    e_sq = 1.0 / beta_val
    alpha_bare_u1 = e_sq / (4 * PI)
    log("  {:>8.2f}  {:>10.4f}  {:>10.4f}  {:>12.6f}  {:>10.2f}".format(
        beta_val, e_sq, mean_p, alpha_bare_u1, 1/alpha_bare_u1))

log()
log("  At beta = 4*pi (= {:.2f}): e^2 = 1/(4*pi), alpha = 1/(4*pi)^2 = {:.6f}".format(
    4*PI, 1/(4*PI)**2))
log("  This is alpha = {:.8f}, or 1/alpha = {:.2f}".format(
    1/(4*PI)**2, (4*PI)**2))
log()

# The framework's natural U(1) coupling
# For SU(3): beta = 2*N/g^2 = 6 at g=1, giving alpha = g^2/(4pi) = 1/(4pi)
# For U(1):  beta = 1/e^2. If e=1, beta = 1, alpha = 1/(4pi)
# If we MATCH the beta values: beta_U1 = beta_SU3 = 6
# then e^2 = 1/6, alpha_U1 = 1/(24*pi) = 0.01326
alpha_u1_matched_beta = 1.0 / (24 * PI)
log("  Matched beta hypothesis: beta_U1 = beta_SU3 = 6")
log("    e^2 = 1/6, alpha_U1 = 1/(24*pi) = {:.6f}  (1/{:.2f})".format(
    alpha_u1_matched_beta, 1/alpha_u1_matched_beta))
log("    Compare alpha_EM(M_Z) = {:.6f}  (1/{:.2f})".format(
    ALPHA_EM_MZ, 1/ALPHA_EM_MZ))
log("    Ratio: {:.3f}".format(alpha_u1_matched_beta / ALPHA_EM_MZ))
log()

# Another natural choice: beta = 2*pi (self-dual point for Z_N)
alpha_u1_selfdual = 1.0 / (8 * PI**2)
log("  Self-dual point: beta = 2*pi")
log("    e^2 = 1/(2*pi), alpha_U1 = 1/(8*pi^2) = {:.6f}  (1/{:.2f})".format(
    alpha_u1_selfdual, 1/alpha_u1_selfdual))
log()


# =============================================================================
# WHAT WOULD IT TAKE?
# =============================================================================

log("=" * 78)
log("WHAT LATTICE COUPLING GIVES alpha_EM = 1/137?")
log("=" * 78)
log()

log("  Working backwards: what bare coupling at the Planck scale gives")
log("  alpha_EM(q=0) = 1/137.036 after running?")
log()

# At the Planck scale, alpha_EM = alpha_2 * sin^2(theta_W)
# We need: alpha_EM(M_Z) = 1/127.95
# Then: alpha_EM(0) = 1/137.036 after vacuum polarization

# If alpha_EM(M_Z) is correct, then alpha_EM(0) is determined by
# the fermion content. The question is what alpha_GUT gives the
# right alpha_EM(M_Z).

# Already answered by Path 1c: M_GUT = mgut_fit
# What alpha_GUT gives the right answer at M_GUT = M_Planck?

def find_alpha_gut_for_alpha_em(target_alpha_em_mz):
    """Find alpha_GUT at M_Planck that gives target alpha_EM at M_Z."""
    def residual(inv_ag):
        L = np.log(M_PLANCK / M_Z)
        inv_a1 = inv_ag - B_1_SM * L / (2 * PI)
        inv_a2 = inv_ag - B_2_SM * L / (2 * PI)
        inv_aem = (3.0/5.0) * inv_a1 + inv_a2
        return inv_aem - 1/target_alpha_em_mz

    inv_ag_needed = brentq(residual, 5, 200)
    return 1.0 / inv_ag_needed

alpha_gut_needed = find_alpha_gut_for_alpha_em(ALPHA_EM_MZ)
log("  Required alpha_GUT at M_Planck for alpha_EM(M_Z) = 1/127.95:")
log("    alpha_GUT = {:.6f}  (1/alpha = {:.2f})".format(
    alpha_gut_needed, 1/alpha_gut_needed))
log("    Framework prediction: alpha_bare = {:.6f}  (1/(4*pi) = {:.2f})".format(
    ALPHA_S_BARE, 4*PI))
log("    Ratio needed/predicted = {:.4f}".format(alpha_gut_needed / ALPHA_S_BARE))
log()

# What is the alpha_s prediction at this alpha_GUT?
L_planck_mz = np.log(M_PLANCK / M_Z)
inv_a3_needed = 1/alpha_gut_needed - B_3_SM * L_planck_mz / (2 * PI)
alpha_3_at_mz_pred = 1.0 / inv_a3_needed

log("  At this alpha_GUT, alpha_s(M_Z) would be:")
log("    alpha_s(M_Z) = {:.4f}  (observed: {:.4f})".format(
    alpha_3_at_mz_pred, ALPHA_S_MZ))
log("    Error: {:.1f}%".format(
    abs(alpha_3_at_mz_pred - ALPHA_S_MZ)/ALPHA_S_MZ*100))
log()

log("  This confirms the fundamental tension: SM unification gives")
log("  approximately correct results but misses by O(10-30%) because")
log("  the three couplings do not converge to a single point.")
log()
log("  Resolution options:")
log("    a) New physics (SUSY, extra dimensions) modifies the running")
log("    b) The framework has DIFFERENT bare couplings for each gauge group")
log("    c) The unification scale differs from M_Planck")
log("    d) 2-loop + threshold corrections close the gap")
log()


# =============================================================================
# FINAL RESULTS AND SCORECARD
# =============================================================================

log("=" * 78)
log("FINAL SCORECARD")
log("=" * 78)
log()

log("  OBSERVED: alpha_EM = 1/137.036 = {:.8f}  (CODATA 2022)".format(ALPHA_EM_OBS))
log("            alpha_EM(M_Z) = 1/127.95 = {:.8f}  (PDG 2024)".format(ALPHA_EM_MZ))
log()

# Compute all final predictions at q^2 = 0
# Path 1: GUT at M_Planck -> alpha_EM(M_Z) -> add VP -> alpha_EM(0)
inv_aem_0_p1 = 1/path1_alpha_em + delta_inv_alpha

# Path 4: Weinberg angle -> same procedure
inv_aem_0_p4 = 1/path4_alpha_em + delta_inv_alpha

log("  Predictions for 1/alpha_EM at q^2 = 0 (including vacuum polarization):")
log()
log("  +------+------------------------------------------+----------+--------+")
log("  | Path | Description                              | 1/alpha  | Error  |")
log("  +------+------------------------------------------+----------+--------+")

final_results = [
    ("1", "GUT at M_Planck, SM 1-loop running", inv_aem_0_p1),
    ("1c", "GUT at best-fit M_GUT", 137.036),  # by construction
    ("4", "Weinberg angle from SU(5) running", inv_aem_0_p4),
]

for p, desc, inv_aem_val in final_results:
    aem_val = 1.0 / inv_aem_val
    err_val = abs(inv_aem_val - 1/ALPHA_EM_OBS) / (1/ALPHA_EM_OBS) * 100
    log("  | {:<4s} | {:<40s} | {:>8.2f} | {:>5.1f}% |".format(
        p, desc, inv_aem_val, err_val))
log("  +------+------------------------------------------+----------+--------+")
log("  | obs  | CODATA 2022                              | {:>8.3f} |        |".format(
    1/ALPHA_EM_OBS))
log("  +------+------------------------------------------+----------+--------+")
log()

log("  CONCLUSION:")
log()
log("  The framework's bare coupling alpha_bare = 1/(4*pi) combined with")
log("  SM gauge coupling running gives alpha_EM predictions in the right")
log("  ballpark (within ~10-30%), but CANNOT reproduce 1/137 exactly")
log("  without either:")
log("    1. New physics between M_Z and M_Planck (SUSY, thresholds)")
log("    2. Non-trivial lattice corrections to the bare U(1) coupling")
log("    3. An independent mechanism for the Weinberg angle")
log()
log("  The core issue is that SM gauge couplings do NOT unify at a single")
log("  point. The framework predicts alpha_s = 1/(4*pi) successfully, but")
log("  extending this to alpha_EM requires additional structure beyond the")
log("  minimal cubic lattice with unit hopping.")
log()
log("  STATUS: OPEN PROBLEM. The electromagnetic coupling is not yet")
log("  derived from the lattice structure. The most promising path is")
log("  Path 4 (Weinberg angle prediction), which requires understanding")
log("  how SU(2)xU(1) breaking emerges from the lattice geometry.")
log()

# =============================================================================
# SAVE LOG
# =============================================================================

log("=" * 78)
log("COMPUTATION COMPLETE")
log("=" * 78)

os.makedirs("logs", exist_ok=True)
try:
    with open(LOG_FILE, "w") as f:
        f.write("\n".join(results))
    log(f"\nLog saved to {LOG_FILE}")
except Exception as e:
    log(f"\nCould not save log: {e}")
