#!/usr/bin/env python3
"""
Weinberg Angle Threshold Corrections from Taste Spectrum
=========================================================

The gauge unification script (frontier_gauge_unification.py) shows that
running from sin^2(theta_W) = 3/8 at M_Planck to M_Z with SM beta functions
gives sin^2(theta_W) = 0.176, about 24% below the measured 0.231.
(Note: the gauge unification note's value of 0.263 used an incorrect
normalization formula for the Weinberg angle.)

This is the SAME problem that SU(5) GUTs face. Standard GUTs solve it with
threshold corrections from heavy particles at the unification scale.

This script does NOT derive the taste assignments from the retained cubic
lane. It evaluates several candidate threshold patterns for an 8-state taste
multiplet and checks how sensitive sin^2(theta_W) is to that unresolved
mapping. The results are therefore scenario-dependent and review-only.

This script computes:
1. Candidate taste decompositions and threshold patterns
2. Beta function modifications under those candidate assignments
3. Two-stage running: SM below M_taste, candidate threshold above M_taste
4. The corrected sin^2(theta_W) at M_Z vs M_taste
5. Comparison with MSSM threshold corrections

Self-contained: numpy + scipy only.
PStack experiment: weinberg-angle-correction
"""

from __future__ import annotations

import math
import os
import sys
import time

import numpy as np

np.set_printoptions(precision=8, linewidth=120)

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR,
                        time.strftime("%Y-%m-%d") + "-weinberg_angle_correction.txt")

results = []


def log(msg=""):
    results.append(msg)
    print(msg)


# =============================================================================
# PHYSICAL CONSTANTS
# =============================================================================

PI = np.pi

# Masses in GeV
M_Z = 91.1876
M_W = 80.377
M_H = 125.25
M_TOP = 173.0
M_PLANCK = 1.2209e19       # full Planck mass
M_PLANCK_RED = 2.435e18    # reduced Planck mass

# Measured SM couplings at M_Z (PDG 2024)
ALPHA_EM_MZ = 1.0 / 127.951
SIN2_TW_MZ = 0.23122             # weak mixing angle (MS-bar)
ALPHA_S_MZ = 0.1179              # strong coupling

# Derived couplings at M_Z with GUT normalization
# alpha_1^{GUT} = (5/3) * alpha_Y = (5/3) * alpha_em / cos^2(theta_W)
ALPHA_1_MZ = (5.0 / 3.0) * ALPHA_EM_MZ / (1.0 - SIN2_TW_MZ)
ALPHA_2_MZ = ALPHA_EM_MZ / SIN2_TW_MZ
ALPHA_3_MZ = ALPHA_S_MZ


def sin2_from_gut_couplings(alpha_1_gut, alpha_2):
    """Compute sin^2(theta_W) from GUT-normalized couplings.

    sin^2_W = alpha_Y / (alpha_Y + alpha_2) = (3/5)*alpha_1 / ((3/5)*alpha_1 + alpha_2)

    At unification (alpha_1 = alpha_2): sin^2_W = 3/8.
    """
    alpha_Y = (3.0 / 5.0) * alpha_1_gut
    return alpha_Y / (alpha_Y + alpha_2)

# SM 1-loop beta coefficients
# Convention: d(1/alpha_i)/d(ln mu) = b_i/(2*pi)
# b > 0 means coupling DECREASES going up (asymptotic freedom)
b_1_SM = -41.0 / 10.0   # = -4.1
b_2_SM = 19.0 / 6.0     # = +3.167
b_3_SM = 7.0             # = +7.0

# Decomposition: b = b_gauge + b_Higgs + N_g * b_matter_per_gen
b_gauge = np.array([0.0, 22.0/3.0, 11.0])
b_higgs = np.array([-1.0/10.0, -1.0/6.0, 0.0])
b_matter_per_gen = np.array([-4.0/3.0, -4.0/3.0, -4.0/3.0])
N_g = 3

L_full = np.log(M_PLANCK / M_Z) / (2 * PI)  # log factor for full running


# =============================================================================
# Derived quantities
# =============================================================================

# Inverse couplings at M_Z
ia1_mz = 1.0 / ALPHA_1_MZ
ia2_mz = 1.0 / ALPHA_2_MZ
ia3_mz = 1.0 / ALPHA_3_MZ

# "Required" unified coupling at M_Planck (run UP from M_Z)
# 1/alpha_i(M_Planck) = 1/alpha_i(M_Z) + b_i * L_full
inv_aU_from_1 = ia1_mz + b_1_SM * L_full
inv_aU_from_2 = ia2_mz + b_2_SM * L_full
inv_aU_from_3 = ia3_mz + b_3_SM * L_full
inv_alpha_U = (inv_aU_from_1 + inv_aU_from_2 + inv_aU_from_3) / 3.0
alpha_U = 1.0 / inv_alpha_U


# #############################################################################
#                            PART 1
#              THE TASTE SPECTRUM AND ITS PHYSICS
# #############################################################################

log("=" * 78)
log("WEINBERG ANGLE THRESHOLD CORRECTIONS FROM TASTE SPECTRUM")
log("=" * 78)
log()

log("=" * 78)
log("1. THE TASTE SPECTRUM AND ITS PHYSICS")
log("=" * 78)
log()

log("  In the Cl(3) framework, staggered fermions on the cubic lattice Z^3")
log("  are modeled with 2^3 = 8 taste components. The mapping of those")
log("  taste states to SM fields is NOT derived here; it is scanned below.")
log()
log("  One illustrative decomposition by Hamming weight h is:")
log()
log("    h=0: |000>              -- 1 state  (scalar taste)")
log("    h=1: |100>,|010>,|001>  -- 3 states (vector taste) -> SU(3)_c fund")
log("    h=2: |110>,|101>,|011>  -- 3 states (tensor taste) -> SU(3)_c antifund")
log("    h=3: |111>              -- 1 state  (pseudoscalar taste)")
log()

log("  KEY INSIGHT: Taste partners and SM quantum numbers")
log("  " + "-" * 60)
log("  Each candidate assignment treats the 8 tastes as a staggered field.")
log("  The light/heavy split and the SM quantum numbers are hypothesis choices")
log("  that this script scans rather than derives.")
log()
log("  In the modeled scenarios below, the heavy states are taken to carry")
log("  the same gauge quantum numbers as the light field. That is a modeling")
log("  assumption, not a derived result of this note.")
log()
log("  This is directly analogous to SUSY threshold scans, where extra matter")
log("  shifts the beta functions once it is activated above a threshold.")
log()

# Taste-breaking mass spectrum
log("  TASTE-BREAKING MASS SPECTRUM:")
log()
log("  The taste-breaking Hamiltonian from lattice perturbation theory")
log("  splits the 8 degenerate states. The splitting is parametrized by")
log("  the Hamming distance from the chosen reference state.")
log()
log("  From frontier_su3_taste_breaking.py:")
log("    Delta m^2(h) = c_1 * h + c_2 * h*(h-1)/2")
log("    with c_1 = 1.0, c_2 = 0.3 (normalized units)")
log()

c1, c2 = 1.0, 0.3

for h in range(4):
    dm2 = c1 * h + c2 * h * (h - 1) / 2
    dm2_ref = c1 * 1  # h=1 reference
    dm2_rel = dm2 - dm2_ref
    mult = int(math.comb(3, h))
    log(f"    h={h}: mult={mult}, Delta m^2 = {dm2:.3f}, "
        f"relative to h=1: {dm2_rel:+.3f}")

log()
log("  These masses are illustrative inputs, not a derived taste assignment.")
log()


# #############################################################################
#                            PART 2
#        BETA FUNCTION MODIFICATIONS FROM TASTE PARTNERS
# #############################################################################

log("=" * 78)
log("2. BETA FUNCTION MODIFICATIONS FROM TASTE PARTNERS")
log("=" * 78)
log()

log("  SM beta function decomposition:")
log(f"    b_i = b_gauge + b_Higgs + N_g * b_matter/gen")
log()
log(f"  {'':>15s}  {'b_1':>10s}  {'b_2':>10s}  {'b_3':>10s}")
log("  " + "-" * 48)
log(f"  {'Gauge':>15s}  {b_gauge[0]:10.4f}  {b_gauge[1]:10.4f}  {b_gauge[2]:10.4f}")
log(f"  {'Higgs':>15s}  {b_higgs[0]:10.4f}  {b_higgs[1]:10.4f}  {b_higgs[2]:10.4f}")
log(f"  {'Matter/gen':>15s}  {b_matter_per_gen[0]:10.4f}  {b_matter_per_gen[1]:10.4f}  {b_matter_per_gen[2]:10.4f}")
b_SM = b_gauge + b_higgs + N_g * b_matter_per_gen
log(f"  {'SM total':>15s}  {b_SM[0]:10.4f}  {b_SM[1]:10.4f}  {b_SM[2]:10.4f}")
log()

# Verify against known values
assert abs(b_SM[0] - b_1_SM) < 1e-10
assert abs(b_SM[1] - b_2_SM) < 1e-10
assert abs(b_SM[2] - b_3_SM) < 1e-10
log("  Verification: SM beta coefficients match known values.")
log()

# Above the taste-breaking scale M_taste, the extra taste partners are active.
# Since taste partners carry the SAME gauge quantum numbers as SM fermions,
# they contribute additional matter content identical to extra generations.
#
# The NUMBER of extra taste partners depends on the taste decomposition:
#
# Scenario A: "Minimal taste" -- only the directly analogous partners
#   Each SM fermion has 1 light taste + 7 heavy tastes.
#   The heavy tastes collectively form (1 + 3* + 1) under SU(3)_c.
#   The 3* (h=2) carries CONJUGATE color charge.
#   The singlets (h=0, h=3) are color singlets.
#   These DO NOT simply multiply the matter content.
#
# Scenario B: "Taste doubling" -- full taste restoration
#   Above M_taste, all 8 tastes are degenerate.
#   The effective number of fermion degrees of freedom is 8x the SM.
#   Since the SM counts 1 taste per fermion (the light one), the
#   extra contribution is 7x the SM matter content.
#   delta_b_i = 7 * N_g * b_matter_per_gen[i]
#
# Scenario C: "SU(3) taste partners" -- only the 3+3* contribute
#   The h=1 (3) is the SM. The h=2 (3*) contributes as conjugate.
#   The 3* has the same Dynkin index as the 3 for all groups.
#   So the 3* partners contribute the same as 3 more generations:
#   delta_b_i = 1 * N_g * b_matter_per_gen[i]  (one extra "generation-equivalent")
#   Plus the singlets (h=0, h=3) which contribute to b_1 and b_2 only.

log("  TASTE PARTNER CONTRIBUTIONS TO BETA FUNCTIONS:")
log()

# Scenario B is the cleanest and most principled:
# Above M_taste, taste symmetry is restored, so all 8 tastes run equally.
# This multiplies the matter sector by 8, adding 7x the SM contribution.

delta_b_taste_full = 7 * N_g * b_matter_per_gen  # full taste restoration
log("  Scenario B (full taste restoration above M_taste):")
log(f"    delta_b = 7 * N_g * b_matter/gen")
log(f"    delta_b_1 = 7 * 3 * ({b_matter_per_gen[0]:.4f}) = {delta_b_taste_full[0]:.4f}")
log(f"    delta_b_2 = 7 * 3 * ({b_matter_per_gen[1]:.4f}) = {delta_b_taste_full[1]:.4f}")
log(f"    delta_b_3 = 7 * 3 * ({b_matter_per_gen[2]:.4f}) = {delta_b_taste_full[2]:.4f}")
log()

# Modified betas above M_taste
b_above_full = b_SM + delta_b_taste_full
log(f"  Modified betas above M_taste (Scenario B):")
log(f"    b_1 = {b_SM[0]:.4f} + ({delta_b_taste_full[0]:.4f}) = {b_above_full[0]:.4f}")
log(f"    b_2 = {b_SM[1]:.4f} + ({delta_b_taste_full[1]:.4f}) = {b_above_full[1]:.4f}")
log(f"    b_3 = {b_SM[2]:.4f} + ({delta_b_taste_full[2]:.4f}) = {b_above_full[2]:.4f}")
log()

log("  IMPORTANT: With 7 extra taste partners per SM fermion, b_2 and b_3")
log("  may lose asymptotic freedom. This constrains M_taste to be near M_Planck.")
log(f"    b_2(above) = {b_above_full[1]:.4f} ({'AF' if b_above_full[1] > 0 else 'NOT AF'})")
log(f"    b_3(above) = {b_above_full[2] :.4f} ({'AF' if b_above_full[2] > 0 else 'NOT AF'})")
log()

# For reference: also compute with fewer extra tastes
# Scenario A: only the 3* antitriplet (3 states) contribute as extra matter.
# The 3* has the same Dynkin index as the 3 for SU(3) and SU(2), but here
# it is only used as part of the chosen scenario definition.

# The h=2 (3*) partner of a quark is treated here as a taste copy in the
# same charge class. That is an assumption of this scenario scan.

# Scenario A: h=2 antitriplet partners only (most conservative)
delta_b_3star = N_g * b_matter_per_gen
log("  Scenario A (only h=2 antitriplet partners):")
log(f"    delta_b = {delta_b_3star}")
log()

# Scenario C: h=2 (3*) + h=0 singlet + h=3 singlet
# The singlets have the same SU(2)_L and U(1)_Y charges as the SM fermion
# but are SU(3)_c singlets. Their contribution to b_3 is 0, but they
# still contribute to b_1 and b_2.
#
# For each SM fermion f with (SU(3), SU(2), Y) = (R, T, Y):
# - h=2 partner: (3*, T, Y) -- same b_1, b_2 contribution, same b_3
# - h=0 partner: (1, T, Y) -- same b_1, b_2 contribution, zero b_3
# - h=3 partner: (1, T, Y) -- same b_1, b_2 contribution, zero b_3
#
# So the extra partners add:
# delta_b_1 = (1 + 1 + 1) * (SM matter b_1/gen) * N_g = 3 * Ng * b_matter[0]
# delta_b_2 = (1 + 1 + 1) * (SM matter b_2/gen) * N_g = 3 * Ng * b_matter[1]
# delta_b_3 = 1 * (SM matter b_3/gen) * N_g              (only 3* contributes)
#           + some reduced contribution from the SU(3) singlet pieces
#
# Wait, the h=0 and h=3 singlets are color singlets, so for SM quarks
# (which are color triplets), the h=0 and h=3 taste partners would be
# color SINGLETS carrying the quark's electroweak charges.
# For SM leptons (which are color singlets), ALL taste partners are
# color singlets.
#
# Per SM generation, the matter contributions to b_3 come ONLY from
# colored fermions (quarks). The h=0 and h=3 taste partners of quarks
# are color singlets and contribute ZERO to b_3.
# The h=2 (3*) taste partners of quarks contribute T(3*)=1/2, same as quarks.
#
# For b_1 and b_2, the modeled taste partners are taken to carry the
# same electroweak charges. That is a scenario choice.

# Let me compute this properly per generation.
# Per SM generation:
#   Quarks: Q_L(3,2,1/3), u_R(3,1,4/3), d_R(3,1,-2/3)
#   Leptons: L_L(1,2,-1), e_R(1,1,-2)
#
# The MATTER contribution to b_i per generation is -4/3 for all i.
# This is because the SM is anomaly-free and the sum of charges is balanced.
#
# The b_1 contribution decomposes into quark and lepton parts:
# b_1^{quarks/gen} = -(2/3)*(3/5) * [3*2*(1/6)^2 + 3*1*(2/3)^2 + 3*1*(1/3)^2]
#                  = -(2/5) * [3*2/36 + 3*4/9 + 3*1/9]
#                  = -(2/5) * [1/6 + 4/3 + 1/3]
#                  = -(2/5) * [1/6 + 5/3]
#                  = -(2/5) * [1/6 + 10/6]
#                  = -(2/5) * 11/6
#                  = -22/30 = -11/15

# Actually, I'll just parametrize the contributions directly.
# Per generation, the contributions to b_i from quarks and leptons separately:

# For b_1 (GUT normalization, factor of 3/5 included):
# Per Weyl fermion with GUT-normalized Y, color dim d_c, weak dim d_w:
#   contribution = -(2/3) * (Y/2)^2 * d_c * d_w
# GUT normalization: Y_GUT = sqrt(3/5) * Y_standard
# So (Y_GUT/2)^2 = (3/5)*(Y_std/2)^2
# => contribution = -(2/3) * (3/5) * (Y_std/2)^2 * d_c * d_w

# SM generation quarks: Q_L(3,2,1/3), u_R(3,1,4/3), d_R(3,1,-2/3)
# b_1 from quarks: -(2/3)*(3/5)*[3*2*(1/6)^2 + 3*1*(2/3)^2 + 3*1*(1/3)^2]
b1_quarks_per_gen = -(2.0/3)*(3.0/5)*( 3*2*(1.0/6)**2 + 3*1*(2.0/3)**2 + 3*1*(1.0/3)**2 )
# SM generation leptons: L_L(1,2,-1), e_R(1,1,-2)
b1_leptons_per_gen = -(2.0/3)*(3.0/5)*( 1*2*(1.0/2)**2 + 1*1*(1.0)**2 )

# b_2: -(2/3)*T_2(R)*d_c for SU(2) doublets only
# Quarks: Q_L is (3,2): T_2(2)=1/2, d_c=3
b2_quarks_per_gen = -(2.0/3)*(1.0/2)*3  # from Q_L only
# Leptons: L_L is (1,2): T_2(2)=1/2, d_c=1
b2_leptons_per_gen = -(2.0/3)*(1.0/2)*1  # from L_L only

# b_3: -(2/3)*T_3(R)*d_w for SU(3) non-singlets only
# Quarks: Q_L(3,2), u_R(3,1), d_R(3,1): T_3(3)=1/2
b3_quarks_per_gen = -(2.0/3)*(1.0/2)*(2 + 1 + 1)  # Q_L has d_w=2, u_R,d_R have d_w=1
# Leptons: all SU(3) singlets, contribute 0
b3_leptons_per_gen = 0.0

log("  Per-generation matter contributions to b_i:")
log(f"    b_1(quarks/gen) = {b1_quarks_per_gen:.6f}")
log(f"    b_1(leptons/gen) = {b1_leptons_per_gen:.6f}")
log(f"    b_1(total/gen) = {b1_quarks_per_gen + b1_leptons_per_gen:.6f}")
log(f"    Expected: {b_matter_per_gen[0]:.6f}")
log()
log(f"    b_2(quarks/gen) = {b2_quarks_per_gen:.6f}")
log(f"    b_2(leptons/gen) = {b2_leptons_per_gen:.6f}")
log(f"    b_2(total/gen) = {b2_quarks_per_gen + b2_leptons_per_gen:.6f}")
log(f"    Expected: {b_matter_per_gen[1]:.6f}")
log()
log(f"    b_3(quarks/gen) = {b3_quarks_per_gen:.6f}")
log(f"    b_3(leptons/gen) = {b3_leptons_per_gen:.6f}")
log(f"    b_3(total/gen) = {b3_quarks_per_gen + b3_leptons_per_gen:.6f}")
log(f"    Expected: {b_matter_per_gen[2]:.6f}")
log()

# Now define the different taste threshold scenarios:
# Each heavy taste partner of a SM fermion contributes to the betas.
# The question is WHICH taste partners carry WHICH representations.

# SCENARIO A: Only the 3* (h=2) partners are colored.
# The h=0 and h=3 partners of quarks are color singlets.
# Counting per generation:
# - 3 heavy tastes of quarks (h=2): same as extra generation of quarks in 3*
#   T(3*) = T(3), so same contribution to b_3.
#   Same EW charges, so same b_1, b_2.
# - 2 heavy tastes of quarks (h=0, h=3): color singlets with quark EW charges
#   Contribute to b_1, b_2 but NOT b_3.
# - 4 heavy tastes of leptons (h=0,2,3, plus the h=2 triplet is 3 states but
#   leptons are already color singlets, so all 7 heavy partners are singlets)
#   Actually ALL heavy lepton partners are color singlets (since leptons are).
#   They contribute to b_1, b_2 but not b_3.

# Total number of extra heavy tastes per field:
# Each staggered field has 8 tastes; 1 is light, 7 are heavy.
# For a quark field: 7 heavy partners
#   - h=0 (1 state): (1, same SU(2), same Y)
#   - h=2 (3 states): (3*, same SU(2), same Y)
#   - h=3 (1 state): (1, same SU(2), same Y)
#   Wait -- the 3 states of h=2 ARE the 3* representation.
#   So there's 1 Weyl fermion in the 3* with SU(2)xU(1) charges matching the quark.
#   Plus 2 Weyl fermions as singlets (h=0 and h=3) with same SU(2)xU(1).
#
# But we also need the REMAINING taste states from h=1.
# h=1 has 3 states forming the 3 of SU(3). ONE of these is the light SM quark.
# Wait -- h=1 has 3 states, and these form the color triplet.
# ALL THREE are the light SM quark's color components. They're not 3 separate fermions.
# The SM quark IS the h=1 triplet.
#
# So the heavy states are: h=0 (1), h=2 (3*), h=3 (1) = 5 states total.
# These 5 states come from 1 + 3 + 1 under SU(3), i.e., 3 Weyl fermions
# (1 singlet at h=0, 1 antitriplet at h=2, 1 singlet at h=3).

log("  SCENARIO A: Structured taste partners")
log("  " + "-" * 60)
log("  Per SM quark field (in color 3):")
log("    h=0: 1 Weyl fermion in (1, T, Y)   -- color singlet")
log("    h=2: 1 Weyl fermion in (3*, T, Y)  -- color antitriplet")
log("    h=3: 1 Weyl fermion in (1, T, Y)   -- color singlet")
log()
log("  Per SM lepton field (in color 1):")
log("    All 7 heavy partners are color singlets:")
log("    h=0: 1 Weyl fermion in (1, T, Y)")
log("    h=2: 3 states forming some rep of SU(3) -> but leptons are")
log("          already singlets, so this is 3 * (1, T, Y)")
log("          Actually these 3 form a 3 under the residual symmetry")
log("          But as color singlets, they just give 3 Weyl (1, T, Y)")
log("    h=3: 1 Weyl fermion in (1, T, Y)")
log()

# For Scenario A, the extra contributions to b_i per generation:
# Quarks: 1*(singlet) + 1*(3*) + 1*(singlet) = 2 singlet + 1 antitriplet
# with same SU(2)xU(1) charges as the quark
#
# b_1 contribution from quark taste partners:
#   - 2 singlets: each contributes b1 of a quark with d_c=1 instead of 3
#   - 1 antitriplet: contributes b1 of a quark with d_c=3 (same as SM)
# Total extra b_1 from quark tastes = 2*(b1_quarks/gen with d_c=1) + 1*(b1_quarks/gen)
#
# Actually, let me think about this more carefully.
# Per quark Weyl fermion Q_L (in the SM: (3,2,1/3)):
# b_1 contribution = -(2/3)*(3/5)*(1/6)^2 * d_c * d_w = -(2/3)*(3/5)*(1/36)*3*2
#
# For the h=2 (3*) taste partner of Q_L:
# b_1 = -(2/3)*(3/5)*(1/6)^2 * 3 * 2   (same, since d_c(3*)=3)
# b_2 = -(2/3)*(1/2) * 3                (same)
# b_3 = -(2/3)*(1/2) * 2                (same, T_3(3*) = T_3(3) = 1/2)
#
# For the h=0 or h=3 (singlet) taste partner of Q_L:
# b_1 = -(2/3)*(3/5)*(1/6)^2 * 1 * 2   (d_c = 1 instead of 3)
# b_2 = -(2/3)*(1/2) * 1                (d_c = 1 instead of 3)
# b_3 = 0                                (color singlet)

# Let me compute the per-generation extra contributions numerically.
# Per generation, quark sector (Q_L, u_R, d_R):

# For the h=2 (3*) partner of each quark Weyl fermion:
# Same b_i contribution as the original quark.
extra_b1_3star_quarks = b1_quarks_per_gen  # same charges, same contribution
extra_b2_3star_quarks = b2_quarks_per_gen
extra_b3_3star_quarks = b3_quarks_per_gen

# For each singlet partner (h=0, h=3) of a quark:
# b_1 and b_2: replace d_c=3 with d_c=1 (factor of 1/3)
extra_b1_singlet_quarks = b1_quarks_per_gen / 3.0  # each singlet
extra_b2_singlet_quarks = b2_quarks_per_gen / 3.0
extra_b3_singlet_quarks = 0.0  # color singlets

# 2 singlet partners per generation of quarks (h=0, h=3)
# 1 antitriplet partner per generation (h=2)

# For lepton sector (L_L, e_R): all heavy partners are color singlets
# Each lepton already has d_c=1, so all 5 heavy lepton partners have d_c=1
# (Actually, for leptons the h=1 triplet makes less sense since leptons
# are color singlets. The taste decomposition 1+3+3*+1 under SU(3) means
# the h=1 triplet would be a color TRIPLET taste partner of the lepton.
# But leptons are color singlets! So the mapping is different for leptons.)
#
# CLARIFICATION: The taste decomposition is in TASTE space, not color space.
# The SU(3)_c that acts on taste is the SAME SU(3) that acts on color.
# So the h=1 triplet IS the color triplet.
# But leptons are color singlets in the SM!
#
# This means: for leptons, the h=1 triplet is NOT the light SM lepton.
# Instead, the h=0 singlet (|000>) is the natural light lepton (color singlet).
# The h=1 triplet of a lepton would be a colored exotic!
#
# This is actually a deep point about the framework. Let me reconsider.

log("  IMPORTANT SUBTLETY: Lepton-quark taste assignment")
log("  " + "-" * 60)
log("  The taste decomposition 1 + 3 + 3* + 1 is under SU(3)_c.")
log("  For QUARKS (color triplets): the h=1 triplet is the light SM quark.")
log("  For LEPTONS (color singlets): the light lepton should be the h=0")
log("  or h=3 SINGLET, not the h=1 triplet.")
log()
log("  This means quarks and leptons emerge from DIFFERENT taste sectors!")
log("  Quarks = h=1 (3), Leptons = h=0 or h=3 (1)")
log()
log("  Consequence: the heavy taste partners are:")
log("    Per quark: (1, 3*, 1) -> 5 heavy partners")
log("    Per lepton: (3, 3*, 1) or similar -> 7 heavy partners")
log("  And some of the lepton's heavy partners are COLORED EXOTICS.")
log()

# This is model-dependent territory. Define candidate scenarios.

log("  We define three clean scenarios for the threshold correction:")
log()

# SCENARIO I: "Universal taste factor"
# Above M_taste, the full 8-fold taste degeneracy is restored.
# Every SM fermion has 8 copies, so the matter sector is multiplied by 8.
# The extra 7 copies contribute 7x the SM matter to the betas.
# This is an illustrative hypothesis, not a derived mapping.

delta_b_I = 7 * N_g * b_matter_per_gen
b_I = b_SM + delta_b_I

log("  SCENARIO I: Universal 8-fold taste (illustrative model)")
log(f"    delta_b = 7 * {N_g} * b_matter/gen = {delta_b_I}")
log(f"    b_above = {b_I}")
log()

# SCENARIO II: "Partial taste" -- only SU(3)-charged partners contribute
# The h=2 antitriplet adds 1 extra generation equivalent
# (same quantum numbers as SM quarks, with 3* instead of 3 for color).
# Plus 2 color-singlet partners of quarks, and 7 lepton partners (all singlets).
# This is more conservative.

# Per generation, the extra contribution:
# From quark 3* partner: same as 1 extra generation of quarks
extra_b_quark_3star = np.array([b1_quarks_per_gen, b2_quarks_per_gen, b3_quarks_per_gen])
# From 2 quark singlet partners (h=0, h=3):
extra_b_quark_singlets = 2 * np.array([b1_quarks_per_gen/3, b2_quarks_per_gen/3, 0])
# From lepton partners: all 7 are color singlets (or some are colored exotics)
# Conservative: assume 7 copies of lepton b_i
extra_b_lepton_partners = 7 * np.array([b1_leptons_per_gen, b2_leptons_per_gen, 0])

delta_b_II = N_g * (extra_b_quark_3star + extra_b_quark_singlets + extra_b_lepton_partners)
b_II = b_SM + delta_b_II

log("  SCENARIO II: Structured taste (illustrative model)")
log(f"    delta_b = {delta_b_II}")
log(f"    b_above = {b_II}")
log()

# SCENARIO III: "Minimal taste" -- only the 3* quark partner
# Just 1 extra antitriplet per generation with quark quantum numbers
delta_b_III = N_g * extra_b_quark_3star
b_III = b_SM + delta_b_III

log("  SCENARIO III: Minimal (illustrative model)")
log(f"    delta_b = {delta_b_III}")
log(f"    b_above = {b_III}")
log()

# Collect all scenarios
scenarios = [
    {"name": "SM only (no correction)", "delta_b": np.zeros(3), "b_above": b_SM},
    {"name": "III: Minimal (3* only)", "delta_b": delta_b_III, "b_above": b_III},
    {"name": "II: Structured taste", "delta_b": delta_b_II, "b_above": b_II},
    {"name": "I: Full 8-fold taste", "delta_b": delta_b_I, "b_above": b_I},
]

log("  SCENARIO SUMMARY:")
log(f"  {'Scenario':>30s}  {'db_1':>8s}  {'db_2':>8s}  {'db_3':>8s}")
log("  " + "-" * 60)
for sc in scenarios:
    log(f"  {sc['name']:>30s}  {sc['delta_b'][0]:8.4f}  {sc['delta_b'][1]:8.4f}  {sc['delta_b'][2]:8.4f}")
log()


# #############################################################################
#                            PART 3
#      TWO-STAGE RUNNING AND sin^2(theta_W) vs M_taste
# #############################################################################

log("=" * 78)
log("3. TWO-STAGE RUNNING: sin^2(theta_W) vs M_taste")
log("=" * 78)
log()

log("  Running prescription:")
log("    Stage 1 (M_Z -> M_taste): SM beta functions")
log("    Stage 2 (M_taste -> M_Planck): SM + taste partner betas")
log()
log("  Starting from a unified coupling at M_Planck:")
log(f"    alpha_U = {alpha_U:.6f} (1/{inv_alpha_U:.1f})")
log(f"    (mean of extrapolated 1/alpha_i at M_Planck)")
log()

# For each scenario, compute sin^2_W as a function of M_taste

header = f"  {'M_taste':>12s}"
for sc in scenarios:
    header += f"  {sc['name'][:12]:>12s}"
log(header)
log("  " + "-" * (12 + 14 * len(scenarios)))

taste_scales = [
    ("M_Planck", M_PLANCK),
    ("3e18", 3e18),
    ("1e18", 1e18),
    ("3e17", 3e17),
    ("1e17", 1e17),
    ("3e16", 3e16),
    ("1e16", 1e16),
    ("3e15", 3e15),
    ("1e15", 1e15),
    ("1e14", 1e14),
    ("1e13", 1e13),
    ("1e12", 1e12),
]

for label, M_taste in taste_scales:
    L_above = np.log(M_PLANCK / max(M_taste, M_Z + 1)) / (2 * PI)
    L_below = np.log(max(M_taste, M_Z + 1) / M_Z) / (2 * PI)

    line = f"  {label:>12s}"
    for sc in scenarios:
        b_ab = sc["b_above"]
        # Running DOWN from M_Planck:
        # 1/alpha_i(M_Z) = 1/alpha_U - b_above * L_above - b_SM * L_below
        ia1 = inv_alpha_U - b_ab[0] * L_above - b_1_SM * L_below
        ia2 = inv_alpha_U - b_ab[1] * L_above - b_2_SM * L_below

        if ia1 > 0 and ia2 > 0:
            a1 = 1.0 / ia1
            a2 = 1.0 / ia2
            sin2 = sin2_from_gut_couplings(a1, a2)
            line += f"  {sin2:12.6f}"
        else:
            line += f"  {'nan':>12s}"
    log(line)

log()
log(f"  Measured: sin^2(theta_W) = {SIN2_TW_MZ:.5f}")
log()

# For each scenario, find the M_taste that best matches measured value
log("  REQUIRED M_taste FOR sin^2(theta_W) = 0.23122:")
log()

for sc in scenarios[1:]:  # skip SM-only
    b_ab = sc["b_above"]

    best_sin2 = None
    best_M = None
    best_dev = 1e10

    for log10_m in np.linspace(10, np.log10(M_PLANCK), 200000):
        M_t = 10**log10_m
        L_above = np.log(M_PLANCK / M_t) / (2 * PI)
        L_below = np.log(M_t / M_Z) / (2 * PI)

        ia1 = inv_alpha_U - b_ab[0] * L_above - b_1_SM * L_below
        ia2 = inv_alpha_U - b_ab[1] * L_above - b_2_SM * L_below

        if ia1 > 0 and ia2 > 0:
            a1 = 1.0 / ia1
            a2 = 1.0 / ia2
            sin2 = sin2_from_gut_couplings(a1, a2)
            dev = abs(sin2 - SIN2_TW_MZ)
            if dev < best_dev:
                best_dev = dev
                best_sin2 = sin2
                best_M = M_t

    if best_M is not None and best_dev < 0.01:
        log(f"  {sc['name']:>30s}:")
        log(f"    Best sin^2_W = {best_sin2:.6f} at M_taste = {best_M:.2e} GeV")
        log(f"    log10(M_taste) = {np.log10(best_M):.2f}")
        log(f"    M_taste / M_Planck = {best_M / M_PLANCK:.6f}")
        achieves = abs(best_sin2 - SIN2_TW_MZ) < 0.001
        log(f"    Achieves target: {'YES' if achieves else 'NO'}"
            f" (dev = {(best_sin2/SIN2_TW_MZ - 1)*100:+.3f}%)")
        sc["best_M"] = best_M
        sc["best_sin2"] = best_sin2
    else:
        log(f"  {sc['name']:>30s}: no match found (min dev = {best_dev:.4f})")
        sc["best_M"] = None
        sc["best_sin2"] = None
    log()


# #############################################################################
#                            PART 4
#         SELF-CONSISTENT DETERMINATION OF alpha_U
# #############################################################################

log("=" * 78)
log("4. SELF-CONSISTENT DETERMINATION OF alpha_U")
log("=" * 78)
log()

log("  The previous analysis used alpha_U from the SM-only extrapolation.")
log("  With taste partners active above M_taste, the unification coupling")
log("  itself changes. We solve self-consistently for the scenario that")
log("  gives EXACT unification at M_Planck.")
log()

# For each scenario, find the M_taste AND alpha_U that simultaneously
# give unification at M_Planck AND reproduce the measured couplings at M_Z.
#
# Constraints:
# 1/alpha_i(M_Z) = 1/alpha_U + b_above_i * L_above + b_SM_i * L_below
# for i = 1, 2, 3.
#
# We have 3 equations and 2 unknowns (alpha_U, M_taste).
# This is overdetermined -- perfect unification requires all 3 to agree.
# We minimize the chi-squared.

log("  Self-consistent scan: minimize chi^2 for all 3 couplings")
log()

for sc in scenarios[1:]:
    b_ab = np.array(sc["b_above"])
    b_sm = np.array([b_1_SM, b_2_SM, b_3_SM])
    ia_mz = np.array([ia1_mz, ia2_mz, ia3_mz])

    best_chi2 = 1e10
    best_au_sc = None
    best_Mt_sc = None
    best_sin2_sc = None

    for log10_m in np.linspace(10, np.log10(M_PLANCK), 5000):
        M_t = 10**log10_m
        L_above = np.log(M_PLANCK / M_t) / (2 * PI)
        L_below = np.log(M_t / M_Z) / (2 * PI)

        # For a given M_taste, alpha_U is determined by running UP:
        # 1/alpha_U = 1/alpha_i(M_Z) + b_SM * L_below + b_above * L_above
        inv_au_arr = ia_mz + b_sm * L_below + b_ab * L_above
        if np.any(inv_au_arr <= 0):
            continue
        inv_au_mean = np.mean(inv_au_arr)
        if inv_au_mean <= 0:
            continue

        # Predicted couplings at M_Z (running DOWN from M_Planck)
        ia_pred = inv_au_mean - b_ab * L_above - b_sm * L_below
        if np.any(ia_pred <= 0):
            continue

        chi2 = np.sum(((ia_pred - ia_mz) / ia_mz)**2)

        a1_p = 1.0 / ia_pred[0]
        a2_p = 1.0 / ia_pred[1]
        sin2_p = sin2_from_gut_couplings(a1_p, a2_p)

        if chi2 < best_chi2:
            best_chi2 = chi2
            best_au_sc = 1.0 / inv_au_mean
            best_Mt_sc = M_t
            best_sin2_sc = sin2_p

    if best_au_sc is not None:
        log(f"  {sc['name']:>30s}:")
        log(f"    Best alpha_U = {best_au_sc:.6f} (1/{1/best_au_sc:.1f})")
        log(f"    M_taste = {best_Mt_sc:.2e} GeV (log10 = {np.log10(best_Mt_sc):.2f})")
        log(f"    sin^2_W = {best_sin2_sc:.6f} (measured: {SIN2_TW_MZ:.5f})")
        log(f"    chi^2 = {best_chi2:.2e}")
        log(f"    Deviation: {(best_sin2_sc/SIN2_TW_MZ - 1)*100:+.3f}%")
        sc["sc_au"] = best_au_sc
        sc["sc_Mt"] = best_Mt_sc
        sc["sc_sin2"] = best_sin2_sc
    else:
        log(f"  {sc['name']:>30s}: no valid solution found")
    log()


# #############################################################################
#                            PART 5
#           COMPARISON WITH MSSM THRESHOLD CORRECTIONS
# #############################################################################

log("=" * 78)
log("5. COMPARISON WITH MSSM THRESHOLD CORRECTIONS")
log("=" * 78)
log()

# MSSM beta coefficients
b_MSSM = np.array([-33.0/5.0, -1.0, 3.0])

log("  MSSM beta function coefficients:")
log(f"    b_1(MSSM) = {b_MSSM[0]:.4f}  (vs SM: {b_1_SM:.4f})")
log(f"    b_2(MSSM) = {b_MSSM[1]:.4f}  (vs SM: {b_2_SM:.4f})")
log(f"    b_3(MSSM) = {b_MSSM[2]:.4f}  (vs SM: {b_3_SM:.4f})")
log()

# MSSM running: SM below M_SUSY, MSSM above
M_SUSY = 1000.0  # 1 TeV
M_GUT = 2e16

L_susy_mz = np.log(M_SUSY / M_Z) / (2 * PI)
L_gut_susy = np.log(M_GUT / M_SUSY) / (2 * PI)

# Extrapolate to M_GUT
ia_gut = ia_mz + b_SM * L_susy_mz + b_MSSM * L_gut_susy
inv_au_mssm = np.mean([ia_gut[0], ia_gut[1], ia_gut[2]])

log(f"  MSSM with M_SUSY = {M_SUSY:.0f} GeV, M_GUT = {M_GUT:.0e} GeV:")
log(f"    1/alpha_i at M_GUT: {ia_gut}")
log(f"    Mean 1/alpha_U = {inv_au_mssm:.2f}")
log(f"    Spread: {np.std(ia_gut):.2f}")
log()

# MSSM prediction for sin^2_W
ia_pred_mssm = inv_au_mssm - b_MSSM * L_gut_susy - b_SM * L_susy_mz
if ia_pred_mssm[0] > 0 and ia_pred_mssm[1] > 0:
    a1_mssm = 1.0 / ia_pred_mssm[0]
    a2_mssm = 1.0 / ia_pred_mssm[1]
    sin2_mssm = sin2_from_gut_couplings(a1_mssm, a2_mssm)
else:
    sin2_mssm = float('nan')

log(f"  MSSM sin^2(theta_W) = {sin2_mssm:.6f}")
log(f"  Shift from SM-only (0.176): {sin2_mssm - 0.176:.4f}")
log()

# MSSM delta_b from SUSY threshold
delta_b_mssm = b_MSSM - b_SM
log(f"  MSSM delta_b (above M_SUSY):")
log(f"    delta_b_1 = {delta_b_mssm[0]:.4f}")
log(f"    delta_b_2 = {delta_b_mssm[1]:.4f}")
log(f"    delta_b_3 = {delta_b_mssm[2]:.4f}")
log()

# Note: the key difference between sin^2 in the two frameworks is
# the DIFFERENTIAL shift delta_b_2 - (3/5)*delta_b_1, times the log.
# For the Weinberg angle:
# sin^2_W ~ 3/8 * [1 - (something) * (b_2-3/5*b_1)/(b_2+3/5*b_1) * ...]
# The relevant combination is (delta_b_1 - delta_b_2).

log("  KEY COMPARISON: The Weinberg angle correction depends primarily")
log("  on the DIFFERENCE (delta_b_1 - delta_b_2) * L_threshold.")
log()
log(f"  {'Framework':>30s}  {'db1-db2':>8s}  {'L_thresh':>10s}  {'(db1-db2)*L':>12s}")
log("  " + "-" * 66)

# MSSM
db12_mssm = delta_b_mssm[0] - delta_b_mssm[1]
log(f"  {'MSSM (M_SUSY=1 TeV)':>30s}  {db12_mssm:8.4f}  {L_gut_susy:10.4f}  {db12_mssm*L_gut_susy:12.4f}")

# Our scenarios
for sc in scenarios[1:]:
    db = sc["delta_b"]
    db12 = db[0] - db[1]
    # Use the taste-breaking scale
    M_t = sc.get("best_M", 1e17)
    if M_t is None:
        M_t = 1e17
    L_t = np.log(M_PLANCK / M_t) / (2 * PI)
    log(f"  {sc['name'][:30]:>30s}  {db12:8.4f}  {L_t:10.4f}  {db12*L_t:12.4f}")

log()


# #############################################################################
#                            PART 6
#                  SUMMARY AND CONCLUSIONS
# #############################################################################

log("=" * 78)
log("6. SUMMARY AND CONCLUSIONS")
log("=" * 78)
log()

log("  THE WEINBERG ANGLE CORRECTION PICTURE:")
log("  " + "=" * 60)
log()
log("  1. STARTING POINT:")
log("     sin^2(theta_W) = 3/8 = 0.375 at M_Planck (from Cl(3))")
log("     SM-only running (correct formula) gives 0.176 at M_Z (-24% below 0.231)")
log()
log("  2. TASTE SPECTRUM:")
log("     Each SM fermion field has 8 taste components on the cubic lattice.")
log("     1 taste is light (SM particle), 7 are heavy (M ~ M_taste).")
log("     Taste partners carry the SAME gauge quantum numbers as SM partners")
log("     (analogous to SUSY partners).")
log()
log("  3. MECHANISM:")
log("     Above the taste-breaking scale M_taste, the extra 7 copies per")
log("     SM fermion become active. This changes the beta functions and")
log("     modifies the running from M_Planck to M_Z.")
log()
log("  4. RESULTS:")
log()

log(f"     {'Scenario':>30s}  {'sin^2_W':>10s}  {'M_taste (GeV)':>14s}  {'dev':>8s}")
log("     " + "-" * 68)
log(f"     {'SM only (no correction)':>30s}  {'0.1759':>10s}  {'N/A':>14s}  {'-24%':>8s}")

for sc in scenarios[1:]:
    # Use Part 3 results (fixed alpha_U, scan M_taste) as primary
    sin2 = sc.get("best_sin2")
    Mt = sc.get("best_M")
    if sin2 is not None and Mt is not None:
        dev = (sin2 / SIN2_TW_MZ - 1) * 100
        log(f"     {sc['name'][:30]:>30s}  {sin2:10.6f}  {Mt:14.2e}  {dev:+8.2f}%")
    else:
        # Fall back to self-consistent results
        sin2 = sc.get("sc_sin2")
        Mt = sc.get("sc_Mt")
        if sin2 is not None and Mt is not None:
            dev = (sin2 / SIN2_TW_MZ - 1) * 100
            log(f"     {sc['name'][:30]:>30s}  {sin2:10.6f}  {Mt:14.2e}  {dev:+8.2f}%")
        else:
            log(f"     {sc['name'][:30]:>30s}  {'no match':>10s}  {'---':>14s}  {'---':>8s}")

log(f"     {'MSSM (M_SUSY = 1 TeV)':>30s}  {sin2_mssm:10.6f}  {M_SUSY:14.2e}  {(sin2_mssm/SIN2_TW_MZ-1)*100:+8.2f}%")
log(f"     {'Measured (PDG 2024)':>30s}  {SIN2_TW_MZ:10.5f}  {'---':>14s}  {'+0.00%':>8s}")
log()

log("  5. KEY FINDINGS:")
log("     - IMPORTANT: The correct Weinberg angle formula with GUT-normalized")
log("       couplings gives sin^2_W = 0.176 from Planck unification (not 0.263")
log("       as reported in the gauge unification note, which used a wrong formula).")
log("     - The correction needs to RAISE sin^2_W from 0.176 to 0.231.")
log("     - The taste spectrum provides this: extra matter above M_taste")
log("       makes the couplings diverge less, keeping sin^2_W closer to 3/8.")
log("     - Scenario II (structured taste) achieves exact match in the")
log("       fixed-alpha scan at M_taste ~ 6x10^11 GeV.")
log("     - Full 8-fold taste (Scenario I) matches in the fixed-alpha scan")
log("       at M_taste ~ 10^17 GeV.")
log()
log("  6. COMPARISON WITH MSSM:")
log("     - MSSM: threshold at M_SUSY ~ 1 TeV, runs to M_GUT ~ 2x10^16 GeV")
log("     - Taste: threshold is scenario-dependent and not yet derived")
log("     - Both use threshold matter to shift beta functions in the scan")
log("     - MSSM requires NEW particle content (sparticles)")
log("     - Taste uses a modeled lattice threshold, not a retained derivation")
log()
log("  HONEST ASSESSMENT:")
log("  " + "-" * 60)
log("  The corrected calculation reveals that Planck-scale unification with")
log("  SM-only running gives sin^2_W = 0.176, BELOW the measured 0.231.")
log("  (The gauge unification note's 0.263 used an incorrect normalization.)")
log("  Some candidate taste assignments can hit 0.231 in the fixed-alpha scan,")
log("  but the self-consistent alpha_U solve does not preserve that match.")
log("  Therefore this lane is a scenario-dependent threshold study, not a")
log("  retained derivation of the Weinberg angle.")
log()


# =============================================================================
# SAVE LOG
# =============================================================================

try:
    with open(LOG_FILE, "w") as f:
        f.write("\n".join(results))
    log(f"  Log saved to {LOG_FILE}")
except Exception as e:
    log(f"  Could not save log: {e}")

log()
log("DONE.")
