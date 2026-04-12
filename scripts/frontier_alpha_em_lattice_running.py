#!/usr/bin/env python3
"""
alpha_EM from Lattice-Specific Particle Content
================================================

THE PROBLEM: Previous computation (frontier_fine_structure_constant.py) ran
alpha_GUT = 1/(4*pi) from M_Planck to M_Z using STANDARD MODEL beta functions
and got alpha_EM(M_Z) ~ 1/62, far from the observed 1/127.95.

THE KEY INSIGHT: The SM beta functions encode the SM particle content:
3 generations of 15 Weyl fermions = 45 total. But the staggered lattice
produces 2^d = 8 taste doublers in d=3. These 8 tastes have DIFFERENT
quantum numbers than 45 Weyl fermions, so the beta functions change.

From frontier_generations_rigorous.py: the 8 taste states decompose under
Z_3 cyclic permutation as 8 = 1 + 1 + 3 + 3. The two triplets are the
candidate fermion generations. The two singlets (0,0,0) and (1,1,1)
have opposite chirality and form the gauge bosons / Higgs sector.

This script:
  1. Identifies the lattice particle content from taste decomposition
  2. Computes beta function coefficients for the lattice content
  3. Runs couplings from M_Planck to M_Z with lattice beta functions
  4. Compares SM vs lattice running
  5. Scans particle content to find what gives alpha_EM = 1/137

Self-contained: numpy + scipy only.
PStack experiment: alpha-em-lattice-running
"""

from __future__ import annotations

import math
import os
import sys
import time

import numpy as np

try:
    from scipy.optimize import brentq, minimize_scalar
except ImportError:
    print("ERROR: scipy required. pip install scipy")
    sys.exit(1)

np.set_printoptions(precision=8, linewidth=120)

LOG_FILE = "logs/" + time.strftime("%Y-%m-%d") + "-alpha_em_lattice_running.txt"

results = []
def log(msg=""):
    results.append(msg)
    print(msg)


# =============================================================================
# PHYSICAL CONSTANTS (PDG 2024 / CODATA 2022)
# =============================================================================

PI = np.pi

ALPHA_EM_OBS = 1.0 / 137.035999084    # CODATA 2022 (q^2 = 0)
ALPHA_EM_MZ  = 1.0 / 127.951          # at M_Z (PDG 2024)
ALPHA_S_MZ   = 0.1179                  # PDG 2024
SIN2_TW_MZ   = 0.23122                # sin^2(theta_W) at M_Z, MS-bar
M_Z          = 91.1876                 # GeV
M_PLANCK     = 1.2209e19              # GeV (full Planck mass)
M_PLANCK_RED = 2.435e18               # GeV (reduced)

# Framework bare coupling
ALPHA_GUT = 1.0 / (4 * PI)            # = 0.07958

# SM couplings at M_Z (GUT normalization)
ALPHA_1_MZ = (5.0 / 3.0) * ALPHA_EM_MZ / (1.0 - SIN2_TW_MZ)
ALPHA_2_MZ = ALPHA_EM_MZ / SIN2_TW_MZ
ALPHA_3_MZ = ALPHA_S_MZ

# Vacuum polarization shift (M_Z -> q^2 = 0)
DELTA_INV_ALPHA = 1.0 / ALPHA_EM_OBS - 1.0 / ALPHA_EM_MZ  # ~ 9.085


log("=" * 78)
log("alpha_EM FROM LATTICE-SPECIFIC PARTICLE CONTENT")
log("=" * 78)
log()
log("TARGET: alpha_EM(M_Z) = 1/127.95 = {:.8f}".format(ALPHA_EM_MZ))
log("        alpha_EM(q=0) = 1/137.04 = {:.8f}".format(ALPHA_EM_OBS))
log()
log("FRAMEWORK: alpha_GUT = 1/(4*pi) = {:.6f}  at M_Planck".format(ALPHA_GUT))
log()


# =============================================================================
# SECTION 1: STANDARD MODEL PARTICLE CONTENT AND BETA FUNCTIONS
# =============================================================================

log("=" * 78)
log("SECTION 1: SM PARTICLE CONTENT (REFERENCE)")
log("=" * 78)
log()

log("  The SM has 3 generations. Each generation contains:")
log("    Q_L  = (u_L, d_L)    : (3, 2, +1/6)   -- color triplet, weak doublet")
log("    u_R                  : (3, 1, +2/3)   -- color triplet, weak singlet")
log("    d_R                  : (3, 1, -1/3)   -- color triplet, weak singlet")
log("    L_L  = (nu_L, e_L)  : (1, 2, -1/2)   -- color singlet, weak doublet")
log("    e_R                  : (1, 1, -1)     -- color singlet, weak singlet")
log()
log("  Per generation: 5 Weyl multiplets = 15 Weyl fermions")
log("  Total: 3 * 15 = 45 Weyl fermions")
log()

# SM 1-loop beta coefficients
# b_i defined via: d(1/alpha_i)/d(ln mu) = b_i / (2*pi)
# Positive b_i -> asymptotically free (coupling decreases at high energy)
# Negative b_i -> coupling increases at high energy (Landau pole)

# For SU(N) with n_f Dirac fermions in the fundamental:
#   b_SU(N) = (11*N/3 - 2*n_f/3) -- in terms of Dirac fermions
#   For Weyl fermions: each Weyl = 1/2 Dirac, so 2*n_f/3 -> n_Weyl/3

# For U(1)_Y (GUT normalized):
#   b_1 = -(2/3) * sum_i n_i * Y_i^2 * (5/3)
#   where sum is over Weyl fermions, Y_i is hypercharge

def compute_sm_beta_coefficients(n_gen):
    """Compute 1-loop beta coefficients for n_gen SM generations.

    Returns (b1, b2, b3) with GUT-normalized U(1).
    Convention: d(1/alpha_i)/d(ln mu) = b_i / (2*pi)
    Positive b means asymptotic freedom (coupling decreases at high energy).

    Standard SM results (n_gen = 3):
      b1 = -41/10, b2 = 19/6, b3 = 7

    Derivation:
      SU(N): b = 11*N/3 - 2*n_f/3  (n_f = Dirac fermions in fundamental)
      U(1)_Y GUT: b1 = -n_Higgs/10 - (2/3)*n_gen * sum_f(5/3 * Y_f^2 * d_f)
        where d_f is the multiplicity and Y_f is the standard hypercharge.
        The per-generation contribution: -(2/3) * (5/3) * sum(Y^2 * d) = -4*n_gen/3

    We match to the known analytical results by using the standard decomposition:
      b_i = b_i^gauge + b_i^Higgs + n_gen * b_i^fermion
    """
    # Pure gauge contributions:
    #   SU(3): 11*3/3 = 11
    #   SU(2): 11*2/3 = 22/3
    #   U(1):  0 (abelian, no self-interaction)

    # Higgs contributions (1 complex SU(2) doublet with Y = 1/2):
    #   SU(3): 0 (Higgs is color singlet)
    #   SU(2): -1/6 (one complex scalar doublet)
    #   U(1)_GUT: -1/10

    # Per-generation fermion contributions:
    #   SU(3): each gen has 2 Dirac color-triplet fermions -> -2*2/3 = -4/3
    #   SU(2): each gen has 2 Dirac weak-doublet fermions -> -2*2/3 = -4/3
    #          (Q_L has 3 colors + L_L = 4 Weyl doublets = 2 Dirac doublets)
    #   U(1)_GUT: -(2/3) * (5/3) * sum_Weyl(Y^2)
    #     sum_Weyl(Y^2) = 6*(1/6)^2 + 3*(2/3)^2 + 3*(1/3)^2 + 2*(1/2)^2 + 1*1^2
    #                   = 1/6 + 4/3 + 1/3 + 1/2 + 1 = 10/3
    #     -> -(2/3)*(5/3)*(10/3) = -100/27
    #     For 3 gen: -300/27 = -100/9

    # Known analytical results for n_gen = 3:
    #   b3 = 11 + 0 + 3*(-4/3) = 11 - 4 = 7
    #   b2 = 22/3 - 1/6 + 3*(-4/3) = 22/3 - 1/6 - 4 = 44/6 - 1/6 - 24/6 = 19/6
    #   b1 = 0 - 1/10 + 3*(-100/27) ??? NO, this gives -100/9 - 1/10 != -41/10

    # The correct formula uses DIRAC fermions and their FULL representation:
    # For U(1)_GUT:
    #   b1 = -1/10 - n_gen * sum_Dirac(4/3 * Y_GUT^2 * T_R)
    # where Y_GUT = sqrt(5/3)*Y and T_R accounts for color multiplicity.
    #
    # Actually, the standard formula (Cheng & Li, Langacker review):
    #   b_1 = -(4/3)*n_gen*(5/3)*(Y_Q^2*6 + Y_u^2*3 + Y_d^2*3 + Y_L^2*2 + Y_e^2*1)/(2*15/(5/3))
    #
    # Let's just use the decomposition that matches the known SM result directly:
    #   b1(n_gen) = -1/10 + n_gen * db1_per_gen
    #   b1(3) = -41/10 -> db1_per_gen = (-41/10 + 1/10) / 3 = -40/30 = -4/3

    b3 = 11.0 - (4.0/3.0) * n_gen

    b2 = 22.0/3.0 - 1.0/6.0 - (4.0/3.0) * n_gen

    # For U(1)_GUT: the per-generation contribution is -4/3
    # (verified: b1(3) = 0 - 1/10 + 3*(-4/3) = -4 - 1/10 = -41/10)
    b1 = -1.0/10.0 - (4.0/3.0) * n_gen

    return b1, b2, b3


b1_sm, b2_sm, b3_sm = compute_sm_beta_coefficients(3)

log("  SM beta coefficients (3 generations):")
log("    b1 = {:.6f}  (analytic: -41/10 = {:.6f})".format(b1_sm, -41.0/10.0))
log("    b2 = {:.6f}  (analytic:  19/6  = {:.6f})".format(b2_sm, 19.0/6.0))
log("    b3 = {:.6f}  (analytic:   7    = {:.6f})".format(b3_sm, 7.0))
log()

# Verify against known values
assert abs(b1_sm - (-41.0/10.0)) < 1e-10, f"b1 mismatch: {b1_sm} vs {-41.0/10.0}"
assert abs(b2_sm - 19.0/6.0) < 1e-10, f"b2 mismatch: {b2_sm} vs {19.0/6.0}"
assert abs(b3_sm - 7.0) < 1e-10, f"b3 mismatch: {b3_sm} vs {7.0}"
log("  VERIFIED: SM beta coefficients match analytic values.")
log()


# =============================================================================
# SECTION 2: SM RUNNING (REPRODUCING THE 1/62 RESULT)
# =============================================================================

log("=" * 78)
log("SECTION 2: SM RUNNING (REPRODUCING PREVIOUS RESULT)")
log("=" * 78)
log()

def run_gut_to_mz(alpha_gut, b1, b2, b3, mu_gut=M_PLANCK):
    """Run three couplings from mu_gut to M_Z at 1-loop.

    Returns (alpha_1, alpha_2, alpha_3, alpha_em, sin2_tw) at M_Z.
    Convention: 1/alpha_i(M_Z) = 1/alpha_GUT + b_i * ln(M_GUT/M_Z) / (2*pi)
    Note: running DOWN means mu decreases, so ln(M_GUT/M_Z) > 0.
    For AF couplings (b > 0): 1/alpha decreases as we go down -> alpha increases.
    For U(1) (b < 0): 1/alpha increases as we go down -> alpha decreases.
    """
    L = np.log(mu_gut / M_Z)
    inv_ag = 1.0 / alpha_gut

    # Running DOWN from high scale to M_Z:
    # 1/alpha_i(M_Z) = 1/alpha_GUT - b_i * ln(M_GUT/M_Z) / (2*pi)
    # For AF (b > 0): 1/alpha decreases -> alpha increases at low energy
    # For U(1) (b < 0): 1/alpha increases -> alpha decreases at low energy
    inv_a1 = inv_ag - b1 * L / (2 * PI)
    inv_a2 = inv_ag - b2 * L / (2 * PI)
    inv_a3 = inv_ag - b3 * L / (2 * PI)

    # alpha_EM^{-1} = (3/5) * alpha_1^{-1} + alpha_2^{-1}
    inv_aem = (3.0/5.0) * inv_a1 + inv_a2

    alpha_1 = 1.0 / inv_a1 if inv_a1 > 0 else float('inf')
    alpha_2 = 1.0 / inv_a2 if inv_a2 > 0 else float('inf')
    alpha_3 = 1.0 / inv_a3 if inv_a3 > 0 else float('inf')
    alpha_em = 1.0 / inv_aem if inv_aem > 0 else float('inf')

    # sin^2(theta_W) = (3/5)*alpha_1 / ((3/5)*alpha_1 + alpha_2)
    a1_phys = (3.0/5.0) * alpha_1
    sin2_tw = a1_phys / (a1_phys + alpha_2) if (a1_phys + alpha_2) > 0 else 0

    return alpha_1, alpha_2, alpha_3, alpha_em, sin2_tw


# SM running from M_Planck
a1_sm, a2_sm, a3_sm, aem_sm, s2tw_sm = run_gut_to_mz(
    ALPHA_GUT, b1_sm, b2_sm, b3_sm
)

log("  alpha_GUT = 1/(4*pi) = {:.6f} at M_Planck = {:.3e} GeV".format(
    ALPHA_GUT, M_PLANCK))
log("  Running to M_Z with SM beta functions (3 generations):")
log()
log("  {:>15s}  {:>12s}  {:>12s}".format("Quantity", "Predicted", "Observed"))
log("  " + "-" * 45)
log("  {:>15s}  {:>12.2f}  {:>12.2f}".format(
    "1/alpha_1", 1/a1_sm, 1/ALPHA_1_MZ))
log("  {:>15s}  {:>12.2f}  {:>12.2f}".format(
    "1/alpha_2", 1/a2_sm, 1/ALPHA_2_MZ))
log("  {:>15s}  {:>12.2f}  {:>12.2f}".format(
    "1/alpha_3", 1/a3_sm, 1/ALPHA_3_MZ))
log("  {:>15s}  {:>12.2f}  {:>12.2f}".format(
    "1/alpha_EM", 1/aem_sm, 1/ALPHA_EM_MZ))
log("  {:>15s}  {:>12.5f}  {:>12.5f}".format(
    "sin^2(thetaW)", s2tw_sm, SIN2_TW_MZ))
log()
log("  SM result: alpha_EM(M_Z) = 1/{:.2f}".format(1/aem_sm))
log("  This is the '1/62' problem: too large by factor {:.2f}".format(
    aem_sm / ALPHA_EM_MZ))
log()


# =============================================================================
# SECTION 3: LATTICE PARTICLE CONTENT
# =============================================================================

log("=" * 78)
log("SECTION 3: LATTICE PARTICLE CONTENT FROM TASTE DOUBLING")
log("=" * 78)
log()

log("  The d=3 staggered lattice produces 2^3 = 8 taste states.")
log("  Under Z_3 cyclic permutation (from frontier_generations_rigorous.py):")
log("    8 = 1 + 1 + 3 + 3")
log()
log("  Singlets: (0,0,0) with Gamma_5 = +1, (1,1,1) with Gamma_5 = -1")
log("  Triplet T1: {(1,0,0), (0,1,0), (0,0,1)} -- Hamming weight 1, Gamma_5 = -1")
log("  Triplet T2: {(0,1,1), (1,1,0), (1,0,1)} -- Hamming weight 2, Gamma_5 = +1")
log()

log("  MAPPING TO SM REPRESENTATIONS:")
log("  The 8 tastes must carry SM quantum numbers. The key question is")
log("  HOW they organize into (SU(3)_c, SU(2)_L, U(1)_Y) representations.")
log()

log("  SCENARIO A: Each triplet orbit = one generation of SM fermions")
log("  ----------------------------------------------------------------")
log("  If T1 and T2 are two separate generations, we have 2 generations")
log("  from the triplets, plus the two singlets could provide a partial")
log("  third generation or the Higgs/gauge sector.")
log()
log("  In this scenario, the lattice produces ~2 generations, not 3.")
log("  Each generation contributes to beta functions as in the SM.")
log()

log("  SCENARIO B: Triplet members = different SM multiplets within one gen")
log("  -------------------------------------------------------------------")
log("  Each member of a triplet carries DIFFERENT gauge quantum numbers:")
log("  Within T1 = {(1,0,0), (0,1,0), (0,0,1)}:")
log("    The 3 states map to different SM multiplets (Q_L, u_R, d_R, etc.)")
log("  This requires only 1-2 generations from 8 tastes total.")
log()

log("  SCENARIO C: 8 tastes as Dirac fermions with reduced content")
log("  -----------------------------------------------------------")
log("  The 8 taste doublers, each a single Dirac fermion, carry charges")
log("  based on their BZ corner momentum. In the simplest case:")
log("    - 8 tastes = 8 Dirac fermions (or 16 Weyl fermions)")
log("    - Compare to SM: 3 gen x 15 Weyl = 45 Weyl fermions")
log("    - The lattice content is SPARSER than the SM")
log()

# The crucial computation: what beta functions does each scenario give?

log("  Per-generation contribution to beta coefficients:")
log()

# Compute for n_gen = 1 to extract per-generation contribution
b1_1gen, b2_1gen, b3_1gen = compute_sm_beta_coefficients(1)
b1_0gen, b2_0gen, b3_0gen = compute_sm_beta_coefficients(0)

db1_per_gen = b1_1gen - b1_0gen
db2_per_gen = b2_1gen - b2_0gen
db3_per_gen = b3_1gen - b3_0gen

log("  Pure gauge (0 generations):")
log("    b1 = {:.6f}, b2 = {:.6f}, b3 = {:.6f}".format(b1_0gen, b2_0gen, b3_0gen))
log()
log("  Per-generation fermion contribution (delta_b):")
log("    db1 = {:.6f}, db2 = {:.6f}, db3 = {:.6f}".format(
    db1_per_gen, db2_per_gen, db3_per_gen))
log()

# Verify: b(3gen) = b(0gen) + 3 * db
assert abs((b1_0gen + 3*db1_per_gen) - b1_sm) < 1e-10
assert abs((b2_0gen + 3*db2_per_gen) - b2_sm) < 1e-10
assert abs((b3_0gen + 3*db3_per_gen) - b3_sm) < 1e-10
log("  VERIFIED: b(3gen) = b(0gen) + 3 * db_per_gen")
log()


# =============================================================================
# SECTION 4: LATTICE BETA FUNCTIONS -- SCENARIO ANALYSIS
# =============================================================================

log("=" * 78)
log("SECTION 4: RUNNING WITH VARIOUS PARTICLE CONTENTS")
log("=" * 78)
log()

log("  Scan n_gen from 0 to 5 and compute alpha_EM(M_Z) from")
log("  alpha_GUT = 1/(4*pi) at M_Planck.")
log()
log("  {:>6s}  {:>10s}  {:>10s}  {:>10s}  {:>10s}  {:>10s}".format(
    "n_gen", "b1", "b2", "b3", "1/alpha_EM", "sin^2(tW)"))
log("  " + "-" * 65)

scan_results = {}
for n_gen_scan in np.arange(0, 5.5, 0.5):
    b1_n, b2_n, b3_n = compute_sm_beta_coefficients(n_gen_scan)
    a1_n, a2_n, a3_n, aem_n, s2tw_n = run_gut_to_mz(
        ALPHA_GUT, b1_n, b2_n, b3_n
    )
    inv_aem_n = 1.0 / aem_n if aem_n > 0 and aem_n < 1 else float('nan')
    scan_results[n_gen_scan] = (aem_n, inv_aem_n, s2tw_n, b1_n, b2_n, b3_n)

    log("  {:>6.1f}  {:>10.4f}  {:>10.4f}  {:>10.4f}  {:>10.2f}  {:>10.5f}".format(
        n_gen_scan, b1_n, b2_n, b3_n, inv_aem_n, s2tw_n))

log()
log("  Observed: 1/alpha_EM(M_Z) = {:.2f},  sin^2(tW) = {:.5f}".format(
    1/ALPHA_EM_MZ, SIN2_TW_MZ))
log()


# =============================================================================
# SECTION 5: FIND EXACT n_gen FOR alpha_EM = 1/127.95
# =============================================================================

log("=" * 78)
log("SECTION 5: WHAT n_gen GIVES alpha_EM(M_Z) = 1/127.95?")
log("=" * 78)
log()

def alpha_em_vs_ngen(n_gen_val):
    """Return alpha_EM(M_Z) as a function of (continuous) n_gen."""
    b1_v, b2_v, b3_v = compute_sm_beta_coefficients(n_gen_val)
    _, _, _, aem_v, _ = run_gut_to_mz(ALPHA_GUT, b1_v, b2_v, b3_v)
    return aem_v

def inv_alpha_em_vs_ngen(n_gen_val):
    """Return 1/alpha_EM(M_Z) as a function of n_gen."""
    aem = alpha_em_vs_ngen(n_gen_val)
    return 1.0 / aem if aem > 0 else float('inf')

# Find n_gen that gives alpha_EM(M_Z) = 1/127.95
# We need inv_alpha_em = 127.95
try:
    n_gen_for_127 = brentq(
        lambda n: inv_alpha_em_vs_ngen(n) - 127.95,
        0.1, 5.0
    )
    log("  n_gen for 1/alpha_EM = 127.95: {:.4f}".format(n_gen_for_127))
    log()

    b1_opt, b2_opt, b3_opt = compute_sm_beta_coefficients(n_gen_for_127)
    a1_opt, a2_opt, a3_opt, aem_opt, s2tw_opt = run_gut_to_mz(
        ALPHA_GUT, b1_opt, b2_opt, b3_opt
    )
    log("  At n_gen = {:.4f}:".format(n_gen_for_127))
    log("    1/alpha_EM  = {:.2f}  (target: 127.95)".format(1/aem_opt))
    log("    1/alpha_s   = {:.2f}  (observed: {:.2f})".format(1/a3_opt, 1/ALPHA_S_MZ))
    log("    sin^2(tW)   = {:.5f}  (observed: {:.5f})".format(s2tw_opt, SIN2_TW_MZ))
    log()
except ValueError as e:
    log("  Could not find n_gen for alpha_EM target: {}".format(e))
    n_gen_for_127 = float('nan')
    log()

# Also find n_gen for alpha_EM(q=0) = 1/137
log("  Now find n_gen for alpha_EM(q=0) = 1/137.036:")
log("  (requires adding vacuum polarization shift of {:.3f})".format(DELTA_INV_ALPHA))
log()

try:
    n_gen_for_137 = brentq(
        lambda n: inv_alpha_em_vs_ngen(n) + DELTA_INV_ALPHA - 137.036,
        0.1, 5.0
    )
    log("  n_gen for 1/alpha_EM(q=0) = 137.04: {:.4f}".format(n_gen_for_137))

    b1_137, b2_137, b3_137 = compute_sm_beta_coefficients(n_gen_for_137)
    a1_137, a2_137, a3_137, aem_137, s2tw_137 = run_gut_to_mz(
        ALPHA_GUT, b1_137, b2_137, b3_137
    )
    log("  At n_gen = {:.4f}:".format(n_gen_for_137))
    log("    1/alpha_EM(M_Z) = {:.2f}".format(1/aem_137))
    log("    1/alpha_EM(q=0) = {:.2f}  (target: 137.04)".format(
        1/aem_137 + DELTA_INV_ALPHA))
    log("    1/alpha_s(M_Z)  = {:.2f}  (observed: {:.2f})".format(1/a3_137, 1/ALPHA_S_MZ))
    log()
except ValueError as e:
    log("  Could not find n_gen for alpha_EM(q=0) target: {}".format(e))
    n_gen_for_137 = float('nan')
    log()


# =============================================================================
# SECTION 6: LATTICE CONTENT -- DIRECT COMPUTATION
# =============================================================================

log("=" * 78)
log("SECTION 6: DIRECT LATTICE CONTENT BETA FUNCTIONS")
log("=" * 78)
log()

log("  Instead of parameterizing by 'effective n_gen', compute the beta")
log("  functions directly from the lattice taste content.")
log()
log("  The 8 taste doublers on the staggered lattice each produce one")
log("  Dirac fermion in the continuum limit. The question is what SM")
log("  representations these 8 Dirac fermions carry.")
log()

log("  MODEL 1: Minimal -- 8 Dirac fermions, all fundamental")
log("  -------------------------------------------------------")
log("  If all 8 tastes are color triplets, SU(2) doublets:")
log("    - n_f(SU3) = 8 Dirac in fundamental")
log("    - n_f(SU2) = 8 Dirac in fundamental")
log("    - U(1): 8 fermions with various hypercharges")
log()

# Compute beta functions for 8 color-triplet Dirac fermions
b3_8color = 11.0 * 3.0 / 3.0 - 2.0 * 8.0 / 3.0
log("  b3(8 flavors) = 11 - 16/3 = {:.4f}".format(b3_8color))
log("  (Compare SM: b3 = 7.0 with n_f = 6)")
log()

log("  MODEL 2: Orbifold mapping 8 = 1 + 1 + 3 + 3")
log("  -----------------------------------------------")
log("  From the Z_3 orbifold decomposition:")
log("  - 2 singlets: spectator/Higgs sector (do not contribute to fermion loops)")
log("  - 2 triplets of 3: each triplet = one set of 3 generation-like fermions")
log()
log("  If each triplet member carries the quantum numbers of a FULL SM generation:")
log("  - Triplet T1: 3 members, each = 1 SM generation -> 3 generations")
log("  - Triplet T2: 3 members, conjugate rep -> 3 anti-generations")
log("  Total effective: 3 + 3 = 6 generations (if both T1 and T2 active)")
log("  Or: 3 generations (if T2 is the CPT conjugate, not independent)")
log()

log("  MODEL 3: Reduced content -- 8 Dirac fermions as specific SM multiplets")
log("  -----------------------------------------------------------------------")
log("  If each of the 8 tastes maps to a DIFFERENT SM multiplet:")
log("    Taste (0,0,0): gauge/Higgs (singlet, Gamma_5 = +1)")
log("    Taste (1,1,1): gauge/Higgs (singlet, Gamma_5 = -1)")
log("    T1 member 1 (1,0,0): Q_L = (3, 2, +1/6)")
log("    T1 member 2 (0,1,0): u_R = (3, 1, +2/3)")
log("    T1 member 3 (0,0,1): d_R = (3, 1, -1/3)")
log("    T2 member 1 (0,1,1): L_L = (1, 2, -1/2)")
log("    T2 member 2 (1,1,0): e_R = (1, 1, -1)")
log("    T2 member 3 (1,0,1): nu_R = (1, 1, 0)   [sterile]")
log()
log("  This maps the 8 tastes to EXACTLY ONE SM generation (+ one sterile nu)!")
log("  With the two singlets as non-fermion modes.")
log()

# Compute beta functions for Model 3 (1 generation content)
# This is the SM with n_gen = 1, plus a sterile neutrino
# Sterile neutrino: (1,1,0) -- no gauge charges, does not contribute to beta functions
b1_model3, b2_model3, b3_model3 = compute_sm_beta_coefficients(1)
# The nu_R has Y = 0, so it does not contribute to b1 either.

log("  Model 3 beta coefficients (1 SM generation + sterile nu):")
log("    b1 = {:.6f}".format(b1_model3))
log("    b2 = {:.6f}".format(b2_model3))
log("    b3 = {:.6f}".format(b3_model3))
log()

a1_m3, a2_m3, a3_m3, aem_m3, s2tw_m3 = run_gut_to_mz(
    ALPHA_GUT, b1_model3, b2_model3, b3_model3
)
log("  Model 3 predictions at M_Z:")
log("    1/alpha_EM  = {:.2f}  (observed: {:.2f})".format(1/aem_m3, 1/ALPHA_EM_MZ))
log("    1/alpha_s   = {:.2f}  (observed: {:.2f})".format(1/a3_m3, 1/ALPHA_S_MZ))
log("    sin^2(tW)   = {:.5f}  (observed: {:.5f})".format(s2tw_m3, SIN2_TW_MZ))
log("    1/alpha(q=0)= {:.2f}  (observed: {:.3f})".format(
    1/aem_m3 + DELTA_INV_ALPHA, 1/ALPHA_EM_OBS))
log()

log("  MODEL 4: Two full generations from T1 + T2")
log("  -------------------------------------------")
log("  If T1 maps to generation 1 and T2 maps to generation 2,")
log("  (with singlets as the Higgs/gauge sector):")
log()

b1_m4, b2_m4, b3_m4 = compute_sm_beta_coefficients(2)
a1_m4, a2_m4, a3_m4, aem_m4, s2tw_m4 = run_gut_to_mz(
    ALPHA_GUT, b1_m4, b2_m4, b3_m4
)
log("  Model 4 beta coefficients (2 generations):")
log("    b1 = {:.6f}, b2 = {:.6f}, b3 = {:.6f}".format(b1_m4, b2_m4, b3_m4))
log("  Model 4 predictions at M_Z:")
log("    1/alpha_EM  = {:.2f}  (observed: {:.2f})".format(1/aem_m4, 1/ALPHA_EM_MZ))
log("    1/alpha_s   = {:.2f}  (observed: {:.2f})".format(1/a3_m4, 1/ALPHA_S_MZ))
log("    sin^2(tW)   = {:.5f}  (observed: {:.5f})".format(s2tw_m4, SIN2_TW_MZ))
log("    1/alpha(q=0)= {:.2f}  (observed: {:.3f})".format(
    1/aem_m4 + DELTA_INV_ALPHA, 1/ALPHA_EM_OBS))
log()


# =============================================================================
# SECTION 7: CUSTOM BETA FUNCTIONS FROM RAW TASTE CONTENT
# =============================================================================

log("=" * 78)
log("SECTION 7: RAW TASTE CONTENT -- DIRECT BETA FUNCTION COMPUTATION")
log("=" * 78)
log()

log("  Instead of assuming tastes map to SM generations, compute beta")
log("  functions from the RAW content: 8 Dirac fermions that each couple")
log("  to all gauge fields with specific representations.")
log()

log("  In the staggered lattice, all 8 tastes couple IDENTICALLY to the")
log("  gauge fields. The gauge coupling is universal -- it does not depend")
log("  on the taste index. This means:")
log()

# The fundamental question: what SU(3)xSU(2)xU(1) representation does
# each taste fermion carry?
# In QCD lattice calculations, staggered fermions are placed in the
# fundamental of SU(3)_color. Each taste = 1 Dirac fermion in the (3).
# For the full SM: the fermion content depends on how SU(2)xU(1) is embedded.

log("  OPTION A: All 8 tastes in (3, 2, Y) -- maximal coupling")
log("  Each taste = 1 Dirac fermion in (3, 2) of SU(3)xSU(2), with some Y.")
log("  This gives n_f(SU3) = 8 Dirac fundamentals, n_f(SU2) = 24 Dirac fundamentals.")
log("  This is TOO MUCH -- it would destroy asymptotic freedom.")
log()

# Compute: how many Dirac fundamentals can SU(3) support before losing AF?
n_f_max_su3 = 11.0 * 3.0 / 2.0  # b3 = 0 at n_f = 33/2 = 16.5
log("  SU(3) asymptotic freedom limit: n_f < {:.1f} Dirac fundamentals".format(n_f_max_su3))
log("  SU(2) asymptotic freedom limit: n_f < {:.1f} Dirac fundamentals".format(
    11.0 * 2.0 / 2.0))
log()

log("  OPTION B: Minimal embedding consistent with anomaly cancellation")
log("  The 8 Dirac taste fermions must satisfy anomaly cancellation.")
log("  In the SM, anomaly cancellation requires specific combinations")
log("  of representations per generation. The minimal anomaly-free set")
log("  IS one SM generation: Q_L, u_R, d_R, L_L, e_R (15 Weyl).")
log()
log("  With 8 Dirac fermions = 16 Weyl fermions, we can fit:")
log("    Option B1: 1 SM generation (15 Weyl) + 1 sterile (1 Weyl)")
log("    Option B2: Different anomaly-free combination using 16 Weyl")
log()

log("  OPTION B1 is exactly Model 3 from Section 6.")
log("  Let us also try a genuinely different assignment:")
log()

log("  OPTION C: SO(10)-inspired -- 8 tastes in the 16 of SO(10)")
log("  In SO(10) GUT, one generation = spinor rep 16 = 16 Weyl fermions.")
log("  This decomposes under SU(5) as 16 = 10 + 5* + 1.")
log("  Under SU(3)xSU(2)xU(1):")
log("    10 = (3,2,1/6) + (3*,1,-2/3) + (1,1,1)  [Q_L, u_R^c, e_R^c]")
log("    5* = (3*,1,1/3) + (1,2,-1/2)              [d_R^c, L_L]")
log("    1  = (1,1,0)                               [nu_R]")
log()
log("  The 16 Weyl fermions (= 8 Dirac) of one SO(10) generation")
log("  matches EXACTLY the 8 taste doublers from the lattice!")
log()
log("  8 Dirac = 16 Weyl = 1 SO(10) generation = 1 SM generation + nu_R")
log()

# This is the key observation: 2^3 = 8 Dirac = 16 Weyl = 16 of SO(10)

log("  THIS IS THE CENTRAL RESULT:")
log("  The staggered lattice in d=3 produces 2^3 = 8 Dirac fermions")
log("  = 16 Weyl fermions = the spinor representation of SO(10).")
log("  This is EXACTLY one generation of SM fermions in the SO(10) GUT.")
log()
log("  The number 16 = 2^4 comes from the spinor rep of SO(10) = SO(2*5).")
log("  Here, 8 = 2^3 comes from the taste doubling in d = 3 spatial dims.")
log("  The match 2^3 Dirac = 2^4 Weyl = 16_SO(10) is STRUCTURAL,")
log("  not a numerical coincidence.")
log()


# =============================================================================
# SECTION 8: EFFECTIVE NUMBER OF GENERATIONS
# =============================================================================

log("=" * 78)
log("SECTION 8: GENERATIONS FROM THE Z_3 ORBIFOLD")
log("=" * 78)
log()

log("  The 8 tastes give ONE SO(10) generation worth of fermion content.")
log("  But frontier_generations_rigorous.py showed the Z_3 orbifold creates")
log("  TRIPLET orbits. How do we reconcile?")
log()
log("  Resolution: The Z_3 acts WITHIN the single generation, organizing")
log("  the 16 Weyl fermions into subgroups, not creating 3 copies of it.")
log()
log("  The 8 = 1 + 1 + 3 + 3 decomposition means:")
log("    1 + 1 = 2 states (Higgs/gauge sector or 2 Weyl)")
log("    3 + 3 = 6 states, each a Dirac fermion = 12 Weyl")
log("    Total: 2 + 12 = 14 Weyl (close to 15 Weyl of 1 SM gen)")
log()
log("  OR more precisely: all 8 Dirac = 16 Weyl contribute to RG running.")
log("  The Z_3 organizes them but does NOT change the total number.")
log()

log("  To get 3 physical generations from the lattice, we need the")
log("  FULL framework mechanism (from frontier_su3_generations.py):")
log("  - Z_3 staggered lattice produces 3^3 = 27 species")
log("  - These organize into 3 x 9 = 3 families")
log("  - Or: Z_3 orbifold of 8 tastes -> 3 triplet generations,")
log("    each INHERITING the full gauge quantum numbers")
log()
log("  If 3 generations, each with full SM content = 3 * 15 Weyl = 45:")
log("  This is the STANDARD MODEL. beta functions are standard SM.")
log()
log("  If instead the lattice gives only n_eff generations:")

# Compute n_eff from the actual taste content
# 8 Dirac = 16 Weyl = 1 SO(10) generation
# If the Z_3 orbifold acts to CREATE 3 copies, each of 8 Dirac:
# 3 * 8 = 24 Dirac = 48 Weyl ~ 3 generations + extras
# If the orbifold REDUCES 8 to 8/3 ~ 2.67 per generation:
# Effective n_gen is somewhere between 1 and 3.

for n_eff in [1.0, 16.0/15.0, 2.0, 3.0]:
    b1_e, b2_e, b3_e = compute_sm_beta_coefficients(n_eff)
    _, _, a3_e, aem_e, s2tw_e = run_gut_to_mz(ALPHA_GUT, b1_e, b2_e, b3_e)
    log("  n_eff = {:.3f}: 1/alpha_EM = {:.2f}, 1/alpha_s = {:.2f}, sin^2(tW) = {:.5f}".format(
        n_eff, 1/aem_e, 1/a3_e, s2tw_e))

log()
log("  Note: n_eff = 16/15 = {:.4f} corresponds to the SO(10) content".format(16.0/15.0))
log("  (16 Weyl instead of 15 per generation -- the extra is nu_R).")
log()


# =============================================================================
# SECTION 9: COMPREHENSIVE PARAMETER SCAN
# =============================================================================

log("=" * 78)
log("SECTION 9: PARAMETER SCAN -- n_gen vs OBSERVABLES")
log("=" * 78)
log()

log("  Fine scan to determine exactly what n_gen matches observations.")
log()

# High-resolution scan
n_gen_array = np.linspace(0.5, 4.5, 401)
inv_aem_array = np.zeros_like(n_gen_array)
inv_as_array = np.zeros_like(n_gen_array)
s2tw_array = np.zeros_like(n_gen_array)

for i, ng in enumerate(n_gen_array):
    b1_i, b2_i, b3_i = compute_sm_beta_coefficients(ng)
    a1_i, a2_i, a3_i, aem_i, s2tw_i = run_gut_to_mz(ALPHA_GUT, b1_i, b2_i, b3_i)
    inv_aem_array[i] = 1.0 / aem_i if aem_i > 0 else float('nan')
    inv_as_array[i] = 1.0 / a3_i if a3_i > 0 else float('nan')
    s2tw_array[i] = s2tw_i

# Find where each observable matches
log("  Observable targets and required n_gen:")
log()

targets = [
    ("1/alpha_EM(M_Z) = 127.95", inv_aem_array, 127.95),
    ("1/alpha_s(M_Z) = 8.48", inv_as_array, 1.0/ALPHA_S_MZ),
    ("sin^2(tW) = 0.2312", s2tw_array, SIN2_TW_MZ),
]

for label, arr, target in targets:
    # Find crossing point
    diffs = arr - target
    crossings = []
    for j in range(len(diffs) - 1):
        if diffs[j] * diffs[j+1] < 0:
            # Linear interpolation
            n_cross = n_gen_array[j] + (n_gen_array[j+1] - n_gen_array[j]) * (
                -diffs[j] / (diffs[j+1] - diffs[j]))
            crossings.append(n_cross)

    if crossings:
        log("  {}: n_gen = {}".format(label, ", ".join(
            "{:.4f}".format(c) for c in crossings)))
    else:
        log("  {}: NO CROSSING in range [0.5, 4.5]".format(label))

log()

# Find the n_gen that simultaneously best fits alpha_EM and alpha_s
log("  Joint fit: minimize chi^2 = (delta alpha_EM)^2 + (delta alpha_s)^2")
log()

def chi2_joint(n_gen_val):
    b1_v, b2_v, b3_v = compute_sm_beta_coefficients(n_gen_val)
    _, _, a3_v, aem_v, _ = run_gut_to_mz(ALPHA_GUT, b1_v, b2_v, b3_v)
    r_em = (1.0/aem_v - 1.0/ALPHA_EM_MZ) / (1.0/ALPHA_EM_MZ)
    r_s = (1.0/a3_v - 1.0/ALPHA_S_MZ) / (1.0/ALPHA_S_MZ)
    return r_em**2 + r_s**2

result = minimize_scalar(chi2_joint, bounds=(0.5, 4.5), method='bounded')
n_gen_joint = result.x
chi2_min = result.fun

b1_j, b2_j, b3_j = compute_sm_beta_coefficients(n_gen_joint)
a1_j, a2_j, a3_j, aem_j, s2tw_j = run_gut_to_mz(ALPHA_GUT, b1_j, b2_j, b3_j)

log("  Best joint fit: n_gen = {:.4f}  (chi^2 = {:.6f})".format(
    n_gen_joint, chi2_min))
log("    1/alpha_EM = {:.2f}  (target: 127.95)".format(1/aem_j))
log("    1/alpha_s  = {:.2f}  (target: {:.2f})".format(1/a3_j, 1/ALPHA_S_MZ))
log("    sin^2(tW)  = {:.5f}  (target: {:.5f})".format(s2tw_j, SIN2_TW_MZ))
log()
log("  Note: chi^2 = {:.6f} means residuals of {:.2f}% on average.".format(
    chi2_min, np.sqrt(chi2_min/2) * 100))
log("  This reflects the fundamental failure of EXACT SM unification:")
log("  no single n_gen gives both alpha_EM and alpha_s correctly when")
log("  starting from a single alpha_GUT at M_Planck.")
log()


# =============================================================================
# SECTION 10: DOES THE LATTICE PREDICTION MATCH?
# =============================================================================

log("=" * 78)
log("SECTION 10: LATTICE PREDICTION vs OBSERVATION")
log("=" * 78)
log()

log("  LATTICE PREDICTION: 8 Dirac tastes = 16 Weyl = ~1 SM generation")
log()
log("  Required for alpha_EM: n_gen = {:.4f}".format(n_gen_for_127))
log("  Required for alpha_s:  n_gen = ???")
log()

# Find n_gen for alpha_s separately
try:
    n_gen_for_as = brentq(
        lambda n: 1.0/run_gut_to_mz(ALPHA_GUT, *compute_sm_beta_coefficients(n))[2] - 1.0/ALPHA_S_MZ,
        0.1, 10.0
    )
    log("  n_gen for alpha_s(M_Z) = 0.1179: {:.4f}".format(n_gen_for_as))
except ValueError:
    n_gen_for_as = float('nan')
    log("  n_gen for alpha_s: no solution in range")
log()

log("  COMPARISON TABLE:")
log()
log("  +------+-------------------------------------------+----------+-----------+")
log("  | Model| Description                               | n_eff    | 1/alpha_EM|")
log("  +------+-------------------------------------------+----------+-----------+")

models = [
    ("SM", "Standard Model (3 generations)", 3.0),
    ("SO10", "1 SO(10) generation (8 Dirac = 16 Weyl)", 16.0/15.0),
    ("1gen", "1 SM generation (15 Weyl)", 1.0),
    ("2gen", "2 SM generations (30 Weyl)", 2.0),
    ("Opt", "Optimal for alpha_EM = 1/128", n_gen_for_127),
]

for label, desc, n_eff in models:
    b1_m, b2_m, b3_m = compute_sm_beta_coefficients(n_eff)
    _, _, a3_m, aem_m, _ = run_gut_to_mz(ALPHA_GUT, b1_m, b2_m, b3_m)
    log("  | {:<4s} | {:<41s} | {:>8.4f} | {:>9.2f} |".format(
        label, desc, n_eff, 1/aem_m))

log("  +------+-------------------------------------------+----------+-----------+")
log("  |  Obs | Observed                                  |    3     |    127.95 |")
log("  +------+-------------------------------------------+----------+-----------+")
log()


# =============================================================================
# SECTION 11: UNIFICATION SCALE DEPENDENCE
# =============================================================================

log("=" * 78)
log("SECTION 11: SENSITIVITY TO UNIFICATION SCALE")
log("=" * 78)
log()

log("  The result depends on where we place the unification scale.")
log("  With n_gen = 1 (lattice prediction), scan M_GUT:")
log()
log("  {:>14s}  {:>12s}  {:>12s}  {:>12s}".format(
    "M_GUT (GeV)", "1/alpha_EM", "1/alpha_s", "sin^2(tW)"))
log("  " + "-" * 55)

for log10_mgut in [10, 12, 14, 15, 16, 17, 18, np.log10(M_PLANCK)]:
    mgut_v = 10**log10_mgut
    b1_v, b2_v, b3_v = compute_sm_beta_coefficients(1.0)
    L_v = np.log(mgut_v / M_Z)
    inv_ag = 1.0 / ALPHA_GUT
    inv_a1_v = inv_ag - b1_v * L_v / (2 * PI)
    inv_a2_v = inv_ag - b2_v * L_v / (2 * PI)
    inv_a3_v = inv_ag - b3_v * L_v / (2 * PI)
    inv_aem_v = (3.0/5.0) * inv_a1_v + inv_a2_v
    a1_v = 1.0/inv_a1_v if inv_a1_v > 0 else 1e10
    a2_v = 1.0/inv_a2_v if inv_a2_v > 0 else 1e-10
    s2tw_v = (3.0/5.0)*a1_v / ((3.0/5.0)*a1_v + a2_v)
    log("  {:>14.2e}  {:>12.2f}  {:>12.2f}  {:>12.5f}".format(
        mgut_v, inv_aem_v, inv_a3_v, s2tw_v))

log()

# Find the M_GUT that gives alpha_EM = 1/128 with n_gen = 1
log("  Find M_GUT that gives alpha_EM(M_Z) = 1/128 with n_gen = 1:")

try:
    def inv_aem_at_mgut(log10_mg):
        mg = 10**log10_mg
        b1_v, b2_v, b3_v = compute_sm_beta_coefficients(1.0)
        L_v = np.log(mg / M_Z)
        inv_ag = 1.0 / ALPHA_GUT
        inv_a1_v = inv_ag - b1_v * L_v / (2 * PI)
        inv_a2_v = inv_ag - b2_v * L_v / (2 * PI)
        return (3.0/5.0) * inv_a1_v + inv_a2_v

    log10_mgut_1gen = brentq(
        lambda x: inv_aem_at_mgut(x) - 127.95,
        4, 20
    )
    mgut_1gen = 10**log10_mgut_1gen
    log("    M_GUT = {:.3e} GeV  (log10 = {:.2f})".format(mgut_1gen, log10_mgut_1gen))

    # What alpha_s does this give?
    b1_v, b2_v, b3_v = compute_sm_beta_coefficients(1.0)
    L_v = np.log(mgut_1gen / M_Z)
    inv_ag = 1.0 / ALPHA_GUT
    inv_a3_1gen = inv_ag - b3_v * L_v / (2 * PI)
    log("    At this scale: 1/alpha_s = {:.2f}  (observed: {:.2f})".format(
        inv_a3_1gen, 1/ALPHA_S_MZ))
    log()
except ValueError:
    log("    No solution found.")
    log()


# =============================================================================
# SECTION 12: TWO-LOOP CORRECTIONS
# =============================================================================

log("=" * 78)
log("SECTION 12: TWO-LOOP CORRECTIONS (SM, n_gen = 3 as reference)")
log("=" * 78)
log()

log("  The 1-loop running misses O(alpha^2) effects. For completeness,")
log("  compare 1-loop and 2-loop results with n_gen = 3 (SM).")
log()

# 2-loop beta coefficients for the SM
# b_ij (2-loop) with GUT normalization:
# From Machacek & Vaughn (1984):
b11_2loop = -199.0/50.0
b12_2loop = -27.0/10.0
b13_2loop = -44.0/5.0
b21_2loop = -9.0/10.0
b22_2loop = -35.0/6.0
b23_2loop = -12.0
b31_2loop = -11.0/10.0
b32_2loop = -9.0/2.0
b33_2loop = 26.0

def run_2loop_rk4(alpha_gut, mu_gut, mu_target, n_steps=10000):
    """Run SM couplings using 2-loop RGE with RK4 integrator."""
    # Use t = ln(mu/M_Z) as the integration variable
    t_start = np.log(mu_gut / M_Z)
    t_end = 0.0  # M_Z
    dt = (t_end - t_start) / n_steps

    # State: (1/alpha_1, 1/alpha_2, 1/alpha_3)
    inv_a = np.array([1.0/alpha_gut, 1.0/alpha_gut, 1.0/alpha_gut])

    # 1-loop coefficients (SM, 3 gen)
    b = np.array([b1_sm, b2_sm, b3_sm])

    # 2-loop coefficient matrix
    B = np.array([
        [b11_2loop, b12_2loop, b13_2loop],
        [b21_2loop, b22_2loop, b23_2loop],
        [b31_2loop, b32_2loop, b33_2loop]
    ])

    def deriv(inv_alpha):
        """d(1/alpha_i)/dt at 2-loop."""
        alphas = 1.0 / inv_alpha
        # 1-loop: d(1/alpha_i)/dt = b_i / (2*pi)
        # 2-loop: d(1/alpha_i)/dt = b_i/(2*pi) + sum_j B_ij * alpha_j / (8*pi^2)
        d_inv = b / (2 * PI)
        for i in range(3):
            for j in range(3):
                d_inv[i] += B[i, j] * alphas[j] / (8 * PI**2)
        return d_inv

    # RK4 integration
    t = t_start
    for _ in range(n_steps):
        k1 = dt * deriv(inv_a)
        k2 = dt * deriv(inv_a + k1/2)
        k3 = dt * deriv(inv_a + k2/2)
        k4 = dt * deriv(inv_a + k3)
        inv_a = inv_a + (k1 + 2*k2 + 2*k3 + k4) / 6
        t += dt

    inv_a1, inv_a2, inv_a3 = inv_a
    inv_aem = (3.0/5.0) * inv_a1 + inv_a2
    a1 = 1.0/inv_a1
    a2 = 1.0/inv_a2
    s2tw = (3.0/5.0)*a1 / ((3.0/5.0)*a1 + a2)

    return 1.0/inv_a1, 1.0/inv_a2, 1.0/inv_a3, 1.0/inv_aem, s2tw


a1_2l, a2_2l, a3_2l, aem_2l, s2tw_2l = run_2loop_rk4(ALPHA_GUT, M_PLANCK, M_Z)

log("  {:>15s}  {:>12s}  {:>12s}  {:>12s}".format("Quantity", "1-loop", "2-loop", "Observed"))
log("  " + "-" * 55)
log("  {:>15s}  {:>12.2f}  {:>12.2f}  {:>12.2f}".format(
    "1/alpha_1", 1/a1_sm, 1/a1_2l, 1/ALPHA_1_MZ))
log("  {:>15s}  {:>12.2f}  {:>12.2f}  {:>12.2f}".format(
    "1/alpha_2", 1/a2_sm, 1/a2_2l, 1/ALPHA_2_MZ))
log("  {:>15s}  {:>12.2f}  {:>12.2f}  {:>12.2f}".format(
    "1/alpha_3", 1/a3_sm, 1/a3_2l, 1/ALPHA_3_MZ))
log("  {:>15s}  {:>12.2f}  {:>12.2f}  {:>12.2f}".format(
    "1/alpha_EM", 1/aem_sm, 1/aem_2l, 1/ALPHA_EM_MZ))
log("  {:>15s}  {:>12.5f}  {:>12.5f}  {:>12.5f}".format(
    "sin^2(tW)", s2tw_sm, s2tw_2l, SIN2_TW_MZ))
log()
log("  2-loop correction to 1/alpha_EM: {:.2f} (= {:.1f}%)".format(
    1/aem_2l - 1/aem_sm, (1/aem_2l - 1/aem_sm)/(1/aem_sm) * 100))
log("  2-loop effects are SMALL (~few percent) and do not resolve the gap.")
log()


# =============================================================================
# VERDICT
# =============================================================================

log("=" * 78)
log("VERDICT")
log("=" * 78)
log()

log("  SUMMARY TABLE: alpha_EM(M_Z) from alpha_GUT = 1/(4*pi) at M_Planck")
log()
log("  +-----+--------------------------------------------+-----------+--------+")
log("  | #   | Particle content                           | 1/alpha_EM| Error  |")
log("  +-----+--------------------------------------------+-----------+--------+")

verdict_rows = [
    ("SM", "Standard Model (3 gen, 45 Weyl)", aem_sm),
    ("1gen", "1 SM generation (15 Weyl)", aem_m3),
    ("2gen", "2 SM generations (30 Weyl)", aem_m4),
    ("SO10", "1 SO(10) gen = 8 Dirac = 16 Weyl",
     run_gut_to_mz(ALPHA_GUT, *compute_sm_beta_coefficients(16.0/15.0))[3]),
    ("2L", "SM 3 gen, 2-loop", aem_2l),
]

for label, desc, aem_val in verdict_rows:
    inv_val = 1.0 / aem_val if aem_val > 0 else float('nan')
    err_val = abs(inv_val - 127.95) / 127.95 * 100
    log("  | {:<3s} | {:<42s} | {:>9.2f} | {:>5.1f}% |".format(
        label, desc, inv_val, err_val))

log("  +-----+--------------------------------------------+-----------+--------+")
log("  | OBS | Observed (PDG 2024)                        |    127.95 |        |")
log("  +-----+--------------------------------------------+-----------+--------+")
log()

log("  REQUIRED n_gen FOR EACH OBSERVABLE:")
log("    alpha_EM(M_Z) = 1/128: n_gen = {:.4f}".format(n_gen_for_127))
if not np.isnan(n_gen_for_as):
    log("    alpha_s(M_Z)  = 0.118: n_gen = {:.4f}".format(n_gen_for_as))
log("    alpha_EM(q=0) = 1/137: n_gen = {:.4f}".format(n_gen_for_137))
log()

log("  KEY FINDINGS:")
log()
log("  1. The SM (3 generations) gives 1/alpha_EM ~ {:.0f} (not 128).".format(1/aem_sm))
log("     This is the well-known failure of non-SUSY SM unification.")
log()
log("  2. The lattice produces 8 Dirac = 16 Weyl fermions per SO(10)")
log("     generation. This matches n_eff ~ {:.2f} SM generations.".format(16.0/15.0))
log("     With n_eff ~ 1: 1/alpha_EM ~ {:.0f}, FURTHER from observation.".format(
    1/aem_m3))
log()
log("  3. Reducing the fermion content makes the problem WORSE, not better.")
log("     Fewer fermions -> larger beta coefficients -> MORE running")
log("     -> alpha_EM at M_Z is SMALLER (1/alpha larger) than the SM prediction.")
log()
log("  4. To get 1/alpha_EM = 128, need n_gen = {:.2f}, which is BETWEEN".format(
    n_gen_for_127))
log("     the SM value (3) and the lattice value (1).")
log()
log("  5. The lattice content gives 1/alpha_EM ~ {:.0f} at M_Z.".format(1/aem_m3))
log("     This is {:.0f}% off from observation ({:.0f}% off for the SM).".format(
    abs(1/aem_m3 - 127.95)/127.95 * 100,
    abs(1/aem_sm - 127.95)/127.95 * 100))
log()
log("  CONCLUSION:")
log("  The lattice-specific particle content (8 Dirac fermions = 1 SO(10)")
log("  generation) gives a DIFFERENT alpha_EM than the SM, but in the WRONG")
log("  direction -- further from observation, not closer. The result")
log("  1/alpha_EM ~ {:.0f} (lattice) vs 1/alpha_EM ~ {:.0f} (SM) vs 128 (observed)".format(
    1/aem_m3, 1/aem_sm))
log("  shows that FEWER fermion generations push 1/alpha_EM higher.")
log()
log("  The path to alpha_EM = 1/137 requires either:")
log("    a) n_gen ~ {:.1f} at the unification scale (between SM and lattice)".format(
    n_gen_for_137))
log("    b) A unification scale M_GUT < M_Planck (reduces the running)")
log("    c) Threshold corrections from new particles between M_Z and M_Planck")
log("    d) A fundamentally different mechanism for U(1)_Y coupling")
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
    log("\nLog saved to {}".format(LOG_FILE))
except Exception as e:
    log("\nCould not save log: {}".format(e))
