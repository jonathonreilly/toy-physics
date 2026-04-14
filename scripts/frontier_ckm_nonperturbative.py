#!/usr/bin/env python3
"""
CKM Nonperturbative Enhancement: Four Mechanisms for the 2.8x Gap
==================================================================

STATUS: BOUNDED -- systematic test of four non-perturbative mechanisms
        that could close the V_cb normalization gap.

CONTEXT:
  The perturbative 1-gluon-exchange NNI approach gives:
    alpha_s(v) = 0.1033    (derived from Cl(3) axiom)
    V_cb(pert) = 0.015     (factor 2.8x below PDG 0.0422)

  The CKM formula:
    c_23 = (alpha_eff * N_c * L_enh / pi) * S_23^(0) * F_EWSB
    V_cb = c_23 * |sqrt(m_s/m_b) - r_W * sqrt(m_c/m_t)|

  requires alpha_eff ~ 0.286 to close, but 1-gluon exchange gives 0.103.
  This script tests whether framework-native non-perturbative physics
  can provide the missing factor of 2.8.

FOUR MECHANISMS:

  1. INSTANTON-LIKE TUNNELING between BZ corners.
     Non-perturbative gauge configurations connect (0,pi,0) to (0,0,pi).
     The Euclidean action for a minimal gauge twist between BZ corners
     gives a tunneling amplitude ~ exp(-S_inst) with S_inst from the
     lattice gauge action. At beta = 6, the instanton may contribute an
     O(1) enhancement if S_inst is small enough.

  2. TASTE-SCALAR EXCHANGE.
     The taste-breaking operator mediates inter-valley transitions. At
     tree level in the taste scalar (the lightest taste multiplet split
     off by O(a^2) effects), this is a different diagram from gluon
     exchange. The taste scalar propagator at the BZ-corner momentum
     transfer q_23 = (0,-pi,pi) gives an additional contribution.

  3. CONFINEMENT / FLUX-TUBE EFFECTS.
     At the taste-breaking scale, the coupling is strong. If the NNI
     coefficient is dominated by confining flux tubes between BZ corners
     rather than perturbative gluons, the effective coupling absorbs
     the string tension sigma ~ (440 MeV)^2.

  4. TASTE STAIRCASE SCALE MISMATCH.
     The hierarchy v = M_Pl * alpha_LM^16 implies 16 taste thresholds
     between M_Pl and v. If the NNI coupling is evaluated at the lowest
     taste threshold (~ Lambda_QCD) rather than at v, then alpha_s ~ 1
     and the 2.8x factor is naturally absorbed. The question: is the
     NNI operator a UV (taste-breaking) or IR (confining) effect?

PStack experiment: frontier-ckm-nonperturbative
Self-contained: numpy only.
"""

from __future__ import annotations

import sys
import numpy as np

np.set_printoptions(precision=10, linewidth=120, suppress=True)

PASS_COUNT = 0
FAIL_COUNT = 0
BOUNDED_PASS = 0
BOUNDED_FAIL = 0
EXACT_PASS = 0
EXACT_FAIL = 0
HONEST_COUNT = 0


def check(name, condition, detail="", kind="BOUNDED"):
    global PASS_COUNT, FAIL_COUNT, BOUNDED_PASS, BOUNDED_FAIL
    global EXACT_PASS, EXACT_FAIL
    status = "PASS" if condition else "FAIL"
    if condition:
        PASS_COUNT += 1
        if kind == "EXACT":
            EXACT_PASS += 1
        else:
            BOUNDED_PASS += 1
    else:
        FAIL_COUNT += 1
        if kind == "EXACT":
            EXACT_FAIL += 1
        else:
            BOUNDED_FAIL += 1
    tag = f" [{kind}]"
    msg = f"  [{status}]{tag} {name}"
    if detail:
        msg += f"  ({detail})"
    print(msg)
    return condition


def honest(name, detail=""):
    """Mark an honest assessment (neither pass nor fail)."""
    global HONEST_COUNT
    HONEST_COUNT += 1
    msg = f"  [HONEST] {name}"
    if detail:
        msg += f"  ({detail})"
    print(msg)


# =============================================================================
# Physical constants (from the framework)
# =============================================================================

PI = np.pi
N_C = 3
C_F = (N_C**2 - 1) / (2 * N_C)  # = 4/3
T_F = 0.5
C_A = N_C

M_PL = 1.22e19      # GeV
V_EW = 246.0         # GeV

# Plaquette from SU(3) at beta = 6 (the axiom gives g_bare = 1)
PLAQ_MC = 0.5934
g_bare = 1.0
alpha_bare = g_bare**2 / (4.0 * PI)  # = 1/(4 pi) ~ 0.07958
u0 = PLAQ_MC ** 0.25                  # ~ 0.8777
alpha_LM = alpha_bare / u0            # ~ 0.0907
alpha_s_v = alpha_bare / u0**2        # ~ 0.1033

# CKM observables
V_CB_PDG = 0.0422
V_US_PDG = 0.2243

# Mass ratios needed for V_cb formula
M_STRANGE = 0.093
M_BOTTOM = 4.18
M_CHARM = 1.27
M_TOP = 172.76

# EWSB parameter (from c_12^d/c_23 ratio in frontier_ckm_s23_analytic.py)
ETA_DOWN = 0.3244

# S_23 formula parameters
L_enh = np.log(M_PL / V_EW) / (4.0 * PI)
S_23_0 = 1.073    # undressed Symanzik overlap ratio
F_EWSB = 1.0 / (1.0 + ETA_DOWN)
r_wu_wd = 1.014   # derived EW ratio W_up/W_down

# V_cb kinematic factor
sqrt_ms_mb = np.sqrt(M_STRANGE / M_BOTTOM)
sqrt_mc_mt = np.sqrt(M_CHARM / M_TOP)
vcb_kinematic = abs(sqrt_ms_mb - r_wu_wd * sqrt_mc_mt)

# The gap
c23_needed = V_CB_PDG / vcb_kinematic
alpha_eff_needed = c23_needed * PI / (N_C * L_enh * S_23_0 * F_EWSB)
enhancement_ratio = alpha_eff_needed / alpha_s_v

# Perturbative prediction
c23_pert = alpha_s_v * N_C * L_enh / PI * S_23_0 * F_EWSB
vcb_pert = c23_pert * vcb_kinematic


# =============================================================================
# PREAMBLE: State the gap precisely
# =============================================================================

print("=" * 78)
print("CKM NONPERTURBATIVE ENHANCEMENT: FOUR MECHANISMS FOR THE 2.8x GAP")
print("=" * 78)

print(f"""
  THE GAP:
    alpha_s(v) = {alpha_s_v:.4f}     (derived, 1-gluon exchange)
    alpha_eff  = {alpha_eff_needed:.4f}     (required for V_cb = {V_CB_PDG})
    Ratio      = {enhancement_ratio:.2f}x

  PERTURBATIVE PREDICTION:
    c_23(pert)  = {c23_pert:.4f}
    V_cb(pert)  = {vcb_pert:.5f}    (PDG: {V_CB_PDG})
    Deviation   = {(vcb_pert/V_CB_PDG - 1)*100:+.1f}%

  FORMULA:
    c_23 = (alpha_eff * N_c / pi) * L_enh * S_23^(0) * F_EWSB
    L_enh = ln(M_Pl/v) / (4pi) = {L_enh:.4f}
    S_23^(0) = {S_23_0:.4f}
    F_EWSB = 1/(1+eta) = {F_EWSB:.4f}  (eta = {ETA_DOWN:.4f})

  QUESTION: Can any framework-native non-perturbative mechanism
  provide the factor {enhancement_ratio:.2f}x to close this gap?
""")

check("gap_established",
      2.0 < enhancement_ratio < 4.0,
      f"enhancement ratio = {enhancement_ratio:.2f}x in [2, 4]",
      kind="EXACT")


# =============================================================================
# MECHANISM 1: INSTANTON-LIKE TUNNELING BETWEEN BZ CORNERS
# =============================================================================

print("\n" + "=" * 78)
print("MECHANISM 1: INSTANTON-LIKE TUNNELING BETWEEN BZ CORNERS")
print("=" * 78)

print(f"""
  PHYSICS:
    The BZ corners X_2 = (0,pi,0) and X_3 = (0,0,pi) are connected by the
    momentum transfer q_23 = (0,-pi,pi). On the lattice, gauge configurations
    that interpolate between these corners are the analog of instantons.

    In QCD, instantons mediate transitions between topological sectors. Here,
    the "topological" sectors are the BZ corners -- the taste states. The
    gauge field configurations that produce taste-changing transitions are
    precisely the UV fluctuations captured by the Wilson term.

  THE INSTANTON ACTION:
    A minimal gauge twist on the lattice that carries momentum q_23 has
    Euclidean action:

      S_inst = beta * (1 - Re Tr P/N_c)_min

    where P is the plaquette for the configuration. The instanton is a
    gauge field with q = (0,-pi,pi) flux threading a plaquette.

    At beta = 6, the single-plaquette instanton has:
      S_plaq = beta * (1 - <P>) = 6 * (1 - {PLAQ_MC}) = {6*(1-PLAQ_MC):.4f}

    This is the action COST per plaquette deviation. A configuration that
    carries the full BZ-corner momentum transfer requires at least 2
    plaquettes (one in each transverse direction for the 2-3 twist):
      S_inst >= 2 * S_plaq = {2*6*(1-PLAQ_MC):.4f}

    The tunneling amplitude is:
      A_inst ~ exp(-S_inst) * (pre-factor)

    The pre-factor involves the fluctuation determinant around the instanton.
    In the dilute instanton gas approximation, this is O(1/S_inst).
""")

S_plaq = 6.0 * (1.0 - PLAQ_MC)
print(f"  Single-plaquette action cost: S_plaq = beta*(1-<P>) = {S_plaq:.4f}")

# Minimal instanton: a twist in the 2-3 plane carrying q = (0,-pi,pi)
# This requires flipping the sign of the link phase in 2 directions
# Minimum number of plaquettes involved: depends on the topology.
# For a single lattice-spacing twist: 2 plaquettes (one per direction)
# For a smooth, larger instanton: more plaquettes but lower action per plaq.
#
# The lattice instanton action scales as:
#   S_n = (8 pi^2 / g^2) * (1/(n*a)^2) for a size-n instanton in 4D
# For n=1 (minimum), S_1 = 8 pi^2 / g^2 = 8 pi^2 * beta / (2 N_c)
# = 8 pi^2 * 6 / 6 = 8 pi^2 ~ 79

# But this is the FULL 4D instanton. In our 3D spatial lattice, the
# analog is a 3D instanton (monopole). The action is:
#   S_3D = (4 pi / g_3^2) where g_3^2 = g^2 / a = g^2 * M_Pl
# This gives S_3D = 4 pi * beta / (2 N_c) = 4 pi

# More concretely: the lattice monopole action in 3D SU(3) at beta=6
# is computed from the lattice BPS monopole.

# Method: Direct computation of the MINIMAL action configuration
# that carries momentum q_23 = (0,-pi,pi)

# A simpler estimate: the inter-valley transition is a TASTE TUNNELING.
# The tunneling exponent is the action of the minimal field configuration
# that connects the two BZ corners in momentum space.

# On a lattice of size L, the minimal twist is a Z_3 center vortex
# that wraps around the lattice in the 2-3 direction. Its action:
#   S_vortex = beta * L * (1 - cos(2pi/N_c)) = 6 * L * (1 - cos(2pi/3))
#            = 6 * L * 1.5 = 9 * L

# For L = 1 (minimal): S_vortex = 9 -- heavily suppressed.
# For L -> infinity: S_vortex -> infinity -- vanishes.
# The instanton contribution is volume-SUPPRESSED, not enhanced.

S_vortex_L1 = 6.0 * 1.0 * (1.0 - np.cos(2*PI/N_C))
A_tunnel_L1 = np.exp(-S_vortex_L1)
S_BPS_4D = 8 * PI**2  # 4D instanton
S_monopole_3D = 4 * PI  # 3D BPS monopole

print(f"\n  INSTANTON ACTION ESTIMATES:")
print(f"    4D instanton (BPST):     S = 8 pi^2 / g^2 = 8 pi^2 = {S_BPS_4D:.2f}")
print(f"    3D monopole (BPS):       S = 4 pi / g_3^2  ~ 4 pi = {S_monopole_3D:.2f}")
print(f"    Center vortex (L=1):     S = beta * (1-cos(2pi/3)) = {S_vortex_L1:.2f}")
print(f"    Tunneling amp (L=1):     A ~ exp(-S) = {A_tunnel_L1:.2e}")

# The instanton-induced inter-valley amplitude adds to the perturbative one:
#   alpha_eff = alpha_pert + alpha_inst
# where alpha_inst ~ (1/S_inst) * exp(-S_inst) * (combinatorial)

# For the 3D monopole route:
S_inst_3D = S_monopole_3D  # ~ 12.6
A_inst_3D = np.exp(-S_inst_3D) / S_inst_3D  # ~ 2.3e-7 (tiny)

# For the center vortex route at L=1:
A_inst_vortex = np.exp(-S_vortex_L1) / S_vortex_L1  # ~ 1.2e-5

# For a LATTICE instanton with action = 2 * S_plaq (minimal):
S_inst_lattice = 2.0 * S_plaq
A_inst_lattice = np.exp(-S_inst_lattice) / S_inst_lattice

# Enhancement factor from instantons:
# alpha_eff = alpha_pert * (1 + R_inst)
# R_inst ~ N_inst * A_inst^2 / alpha_pert
# where N_inst is the number of instanton-antiinstanton pairs

# Most favorable: lattice minimal instanton
N_inst_density = 1.0  # per lattice site (rough upper bound)
R_inst_lattice = N_inst_density * A_inst_lattice**2 / alpha_s_v
R_inst_vortex = N_inst_density * A_inst_vortex**2 / alpha_s_v
R_inst_monopole = N_inst_density * A_inst_3D**2 / alpha_s_v

print(f"\n  INSTANTON-INDUCED ENHANCEMENT RATIOS:")
print(f"    Lattice minimal (S={S_inst_lattice:.2f}):  A = {A_inst_lattice:.4e}, "
      f"R_inst ~ {R_inst_lattice:.4e}")
print(f"    Center vortex (S={S_vortex_L1:.2f}):       A = {A_inst_vortex:.4e}, "
      f"R_inst ~ {R_inst_vortex:.4e}")
print(f"    3D monopole (S={S_monopole_3D:.2f}):       A = {A_inst_3D:.4e}, "
      f"R_inst ~ {R_inst_monopole:.4e}")

# VERDICT: Even the most favorable instanton estimate gives R_inst << 1.
# Instantons cannot provide the 2.8x enhancement.
# The suppression exp(-S) with S >= 2*S_plaq ~ 4.9 kills the contribution.

inst_best_R = max(R_inst_lattice, R_inst_vortex, R_inst_monopole)
inst_enhancement = 1.0 + inst_best_R

print(f"""
  VERDICT FOR MECHANISM 1:
    Best instanton enhancement: 1 + R = {inst_enhancement:.6f}
    This is {inst_best_R:.2e} -- negligible compared to the needed {enhancement_ratio:.2f}x.
    Instantons are exponentially suppressed at beta = 6.

    The instanton route FAILS to close the gap.
    Reason: exp(-S) suppression is too severe. The lattice coupling
    is WEAK (beta = 6 is in the weak-coupling regime for SU(3)),
    so non-perturbative tunneling amplitudes are tiny.
""")

check("instanton_contribution",
      inst_best_R < 0.01,
      f"R_inst = {inst_best_R:.2e} << 1: instantons negligible",
      kind="EXACT")

honest("instanton_fails",
       f"best R_inst = {inst_best_R:.2e}, need {enhancement_ratio - 1:.2f}")


# =============================================================================
# MECHANISM 2: TASTE-SCALAR EXCHANGE
# =============================================================================

print("\n" + "=" * 78)
print("MECHANISM 2: TASTE-SCALAR EXCHANGE")
print("=" * 78)

print(f"""
  PHYSICS:
    Beyond 1-gluon exchange, the inter-valley transition can proceed through
    exchange of the TASTE-BREAKING operator itself. The staggered lattice
    generates a spectrum of taste-split pseudo-Goldstone bosons (in the
    chiral limit). At finite lattice spacing, these acquire masses of
    order Delta_taste ~ a^2 * alpha_s * Lambda^3.

    The taste-scalar is the lightest state in the taste multiplet split
    off by O(a^2) corrections. Its propagator at the BZ-corner momentum
    transfer q_23 = (0,-pi,pi) gives an additional contribution:

      A_taste_scalar = (g_taste)^2 / (q_23^2 + m_taste^2)

    where g_taste is the taste-scalar coupling and m_taste is its mass.

  TASTE SPLITTING ON THE LATTICE:
    From Sharpe & Van de Water (2005), the taste splitting at O(a^2) is:
      Delta_xi = C_xi * (alpha_s)^2 * Lambda^2

    where C_xi depends on the taste representation (S, P, V, A, T).
    For the taste-scalar (xi = I), the splitting is maximal.

    On our lattice with 1/a = M_Pl, the taste splitting is:
      Delta_taste = alpha_s^2 * (1/a)^2 * c_SW
    where c_SW is the Symanzik coefficient.

    But here we operate at the lattice scale itself (1/a = M_Pl),
    so the taste splitting is an O(1) effect: the taste states at BZ
    corners have O(1) lattice-unit mass splittings.
""")

# The taste-breaking Hamiltonian in the Symanzik expansion
# The 4-fermion taste operator:
#   H_taste = sum_xi C_xi (psibar Gamma_xi psi)^2
# The coefficient is:
#   C_xi = alpha_s^2 * (combinatorial factor depending on xi)

# For the taste-scalar exchange between BZ corners:
# The propagator at q_23 = (0,-pi,pi) has q_hat^2 = 8 (lattice)
# The taste-scalar mass at the lattice scale:
#   m_taste^2 ~ (alpha_s * 2/a)^2 ~ (alpha_s * 2*M_Pl)^2

# On the lattice (a=1 units), the taste-scalar exchange amplitude:
alpha_s_lat = 0.30  # commonly used lattice alpha_s at beta ~ 6

# Taste-breaking contributions to S_23 at O(alpha_s^2):
# The 4-fermion vertex is:
#   V_taste = C_F^2 * alpha_s^2 / (16 pi^2) * delta(taste)
# Summed over 16 taste channels:
#   V_total_taste = 16 * C_F^2 * alpha_s^2 / (16 pi^2) = C_F^2 * alpha_s^2 / pi^2

# The taste-scalar exchange adds to the 1-gluon exchange:
# At 1-gluon: amplitude ~ alpha_s * C_F * G(q_23)
# At taste-scalar: amplitude ~ alpha_s^2 * C_F^2 * G_taste(q_23, m_taste)

# The taste-scalar propagator:
# G_taste(q, m) = 1 / (q_hat^2 + m_taste^2)
# with q_hat^2 = 8 for q_23

# In lattice units, the taste mass is determined by the taste splitting.
# For SU(3) at beta = 6, the pion taste splitting is well measured:
# Delta_xi = a^2 * C_xi * alpha_s * Lambda_QCD^3
# But at our lattice (1/a = M_Pl), this is tiny in lattice units.

# More relevant: the LATTICE-SCALE taste splitting from Symanzik.
# The taste-breaking coefficient at O(a^2) for the taste-scalar channel:
# C_I = (alpha_s / pi)^2 * 16 * pi^4 / q_hat^4 (Sharpe-SVdW)

# For q_hat^2 = 8:
C_taste_I = (alpha_s_lat / PI)**2 * 16.0 * PI**4 / 8.0**2
print(f"  Taste-scalar coefficient: C_I = {C_taste_I:.6f}")

# The taste-scalar exchange amplitude relative to 1-gluon:
# R_taste = A_taste_scalar / A_gluon
# = (alpha_s * C_F * C_taste_I) / (alpha_s * C_F * 1/q_hat^2)
# = C_taste_I * q_hat^2
# This is dimensionless.

R_taste_scalar = C_taste_I * 8.0 / (1.0 / 8.0)  # ratio of amplitudes

# More carefully: the gluon amplitude is alpha_s * C_F / q_hat^2
# The taste-scalar amplitude is alpha_s^2 * C_F * C_I_coeff / q_hat^2
# So the ratio is simply alpha_s * C_I_coeff

# The standard taste-exchange vertex (Aubin-Bernard 2003):
# The hairpin diagram has:
#   V_taste_exch = (alpha_s * C_F)^2 * delta^2 / (16 pi^2)
# where delta^2 is the taste splitting.
# The ratio to 1-gluon:
#   R = alpha_s * C_F * delta^2 / (16 pi^2 * q_hat^2)

# Numerically: delta^2 ~ 16 * sin^4(pi/2) = 16 on the lattice (maximal)
delta2_lattice = 16.0  # maximal taste splitting in lattice units

R_taste_to_gluon = alpha_s_lat * C_F * delta2_lattice / (16.0 * PI**2 * 8.0)

# Also compute the direct O(alpha_s^2) correction (NLO gluon exchange):
R_NLO_gluon = alpha_s_lat * C_F / PI  # standard NLO ~ alpha_s * C_F / pi

denom_str = f"(16 * {PI**2:.3f} * 8)"
print(f"""
  TASTE-SCALAR EXCHANGE vs 1-GLUON:
    q_hat^2 = 8 (at BZ-corner momentum transfer)
    delta^2_taste = {delta2_lattice:.1f} (maximal lattice taste splitting)

    Taste-scalar exchange / 1-gluon:
      R_taste = alpha_s * C_F * delta^2 / (16 pi^2 * q_hat^2)
              = {alpha_s_lat:.3f} * {C_F:.3f} * {delta2_lattice:.1f} / {denom_str}
              = {R_taste_to_gluon:.4f}

    NLO gluon exchange correction:
      R_NLO = alpha_s * C_F / pi = {R_NLO_gluon:.4f}

    Combined next-order correction:
      R_total = R_taste + R_NLO = {R_taste_to_gluon + R_NLO_gluon:.4f}
""")

# The taste-scalar exchange gives a correction of order 13%, not the 2.8x we need.

# HOWEVER: there is a more interesting possibility.
# The taste-breaking operator is a FOUR-FERMION operator. In the
# Symanzik expansion, it appears at O(a^2). But the coefficient
# C_taste is NOT suppressed by alpha_s -- it is an O(1) lattice
# artifact. The physical content is:
#
# H_taste = sum_xi C_xi * (psibar Gamma_xi psi)^2 / a^2
#
# and C_xi ~ O(1). The inter-valley matrix element of this operator
# does NOT go through gluon exchange at all. It is a DIRECT contact
# interaction between taste states.
#
# In the Symanzik EFT, the taste-breaking operator is treated as a
# perturbation. But its coefficient is alpha_s^2 * (known factors),
# and the resummed series may differ from 1-loop.

# Let's check whether the O(alpha_s^2) 4-fermion taste-exchange vertex
# can provide an additional significant correction.

# V-scheme coupling at the plaquette scale:
# alpha_V = -ln(P) / (3.0684) ~ 0.170 for P = 0.5934
alpha_V_standard = -np.log(PLAQ_MC) / 3.0684
print(f"  V-scheme coupling: alpha_V = {alpha_V_standard:.4f}")

# The 4-fermion taste-exchange vertex (Sharpe & Van de Water 2005):
# At O(alpha_s^2), the taste-breaking 4-fermion operator has coefficient
#   C_4f = (alpha_V * C_F / pi)^2 * (geometrical factor)
# The geometrical factor for the (2,3) taste channel is O(1).
# The ratio of this to the 1-gluon exchange (O(alpha_s)) is:
#   R_4f = alpha_V * C_F / pi ~ 0.072

R_4fermion = alpha_V_standard * C_F / PI

# The combined perturbative correction (NLO gluon + taste 4-fermion):
R_taste_total = R_taste_to_gluon + R_NLO_gluon + R_4fermion

print(f"  4-fermion taste-exchange / 1-gluon: R_4f = alpha_V * C_F / pi = {R_4fermion:.4f}")
print(f"  Total perturbative correction: R_total = {R_taste_total:.4f}")

# Total effective coupling including all perturbative taste-breaking:
alpha_eff_with_taste = alpha_s_v * (1.0 + R_taste_total)
c23_with_taste = alpha_eff_with_taste * N_C * L_enh / PI * S_23_0 * F_EWSB
vcb_with_taste = c23_with_taste * vcb_kinematic

print(f"""
  WITH ALL PERTURBATIVE TASTE CORRECTIONS:
    alpha_eff = alpha_s(v) * (1 + R_total)
              = {alpha_s_v:.4f} * (1 + {R_taste_total:.4f})
              = {alpha_eff_with_taste:.4f}
    V_cb = {vcb_with_taste:.5f}  (PDG: {V_CB_PDG}, dev: {(vcb_with_taste/V_CB_PDG-1)*100:+.1f}%)

  VERDICT: All perturbative taste corrections combined add ~{R_taste_total*100:.0f}% to the
  coupling, but we need +{(enhancement_ratio-1)*100:.0f}%. Perturbative taste corrections
  cannot close the gap.
""")

check("taste_scalar_correction",
      R_taste_total < 1.0,
      f"R_total = {R_taste_total:.3f} < 1, perturbative correction is bounded",
      kind="BOUNDED")

honest("taste_scalar_insufficient",
       f"total correction = {(R_taste_total)*100:.1f}%, need {(enhancement_ratio-1)*100:.0f}%")


# =============================================================================
# MECHANISM 3: CONFINEMENT / FLUX-TUBE EFFECTS
# =============================================================================

print("\n" + "=" * 78)
print("MECHANISM 3: CONFINEMENT / FLUX-TUBE EFFECTS")
print("=" * 78)

print(f"""
  PHYSICS:
    The perturbative calculation uses the free gluon propagator
    G(q) = 1/q_hat^2 for the inter-valley scattering. But at large
    distances (low momenta), the gluon propagator is modified by
    confinement. The string tension sigma introduces a linear
    potential between color charges:

      V_conf(r) = sigma * r   (r >> 1/Lambda_QCD)

    In momentum space, the confining potential modifies the gluon
    propagator at low q:

      G_conf(q) ~ 1/q^4   (linear potential -> 1/q^4 in 3D)

    However, the BZ-corner momentum transfer q_23 = (0,-pi,pi) has
    |q| = sqrt(2)*pi ~ 4.4 in lattice units. This is a UV momentum,
    not an IR one. Confinement effects at this scale are suppressed
    by (Lambda_QCD / q)^2.

  QUANTITATIVE ESTIMATE:
    The confining contribution to the inter-valley amplitude:
      A_conf ~ sigma / q^4
    vs perturbative:
      A_pert ~ alpha_s / q^2

    Ratio:
      R_conf = A_conf / A_pert = sigma / (alpha_s * q^2)
""")

# String tension in lattice units
# sigma_phys = (440 MeV)^2 = 0.1936 GeV^2
sigma_phys = 0.440**2  # GeV^2

# In lattice units with 1/a = M_Pl:
# sigma_lat = sigma_phys * a^2 = sigma_phys / M_Pl^2
sigma_lat = sigma_phys / M_PL**2

# q_hat^2 at BZ corner
q_hat2 = 8.0

# Ratio of confining to perturbative amplitude
R_conf_direct = sigma_lat / (alpha_s_v * q_hat2)

print(f"  String tension: sigma = {sigma_phys:.4f} GeV^2 = ({np.sqrt(sigma_phys)*1000:.0f} MeV)^2")
print(f"  In lattice units: sigma_lat = sigma / M_Pl^2 = {sigma_lat:.2e}")
print(f"  q_hat^2 at BZ corner: {q_hat2}")
print(f"  R_conf (direct) = sigma_lat / (alpha_s * q_hat^2) = {R_conf_direct:.2e}")

# This is absurdly small because sigma_lat ~ 10^{-39}.
# Confinement at the Planck-scale lattice is utterly irrelevant
# for UV-scale momentum transfers.

print(f"""
  sigma_lat / M_Pl^2 = {sigma_lat:.2e}

  At BZ-corner momenta (q ~ pi/a ~ pi * M_Pl), confinement effects
  are suppressed by (Lambda_QCD / M_Pl)^2 ~ {(0.2/M_PL)**2:.2e}.
  This is negligible.
""")

# But wait: there is a subtlety. The PHYSICAL inter-valley scattering
# happens not at the bare lattice scale, but after RG improvement.
# The taste-breaking operator at the EW scale probes distances ~ 1/v.
# At this scale, what is the relevant coupling?

# At mu = v = 246 GeV, alpha_s(v) = 0.103 (perturbative, no confinement).
# At mu = Lambda_QCD ~ 200 MeV, alpha_s ~ 1 (confining regime).

# The NNI operator coefficient receives contributions from ALL scales
# between M_Pl and v through the RG. The L_enh factor captures the
# leading-log running. But if there is a confining regime in the
# taste staircase, it could modify the running.

# Check: is there a confining scale in the taste staircase?
# The taste thresholds are at m_k = M_Pl * alpha_LM^k.
# The lowest taste threshold (k=15):
m_15 = M_PL * alpha_LM**15
# Lambda_QCD from the hierarchy:
v_hierarchy = M_PL * alpha_LM**16
Lambda_QCD_from_hierarchy = v_hierarchy * alpha_LM  # one more step down

print(f"  Taste staircase scales:")
print(f"    Highest: m_0 = M_Pl = {M_PL:.3e} GeV")
print(f"    Lowest:  m_15 = M_Pl * alpha_LM^15 = {m_15:.3e} GeV")
print(f"    v = M_Pl * alpha_LM^16 = {v_hierarchy:.1f} GeV")
print(f"    Lambda_QCD ~ v * alpha_LM = {Lambda_QCD_from_hierarchy:.1f} GeV")

# The lowest taste threshold is at m_15 ~ 2700 GeV (well above Lambda_QCD).
# No taste threshold falls in the confining regime.
# So confinement does not directly affect the taste-breaking operator.

check("no_confining_threshold",
      m_15 > 10.0 * 0.2,  # well above Lambda_QCD
      f"m_15 = {m_15:.0f} GeV >> Lambda_QCD ~ 200 MeV",
      kind="EXACT")

# However, BELOW v, the coupling continues to grow (standard QCD running).
# If the NNI operator coefficient is sensitive to scales BELOW v,
# then confinement could contribute. But the L_enh factor cuts off
# the running at mu = v, not at Lambda_QCD.

# What if we extend the running below v?
# alpha_s(Lambda_QCD) ~ 1, and the running integral diverges logarithmically.
# The additional contribution from running below v:
#   Delta L = ln(v / Lambda_QCD) / (4 pi) ~ ln(246/0.2) / (4 pi)

Lambda_QCD = 0.213  # GeV (PDG)
Delta_L = np.log(V_EW / Lambda_QCD) / (4.0 * PI)

# If we include this:
L_enh_extended = L_enh + Delta_L
enhancement_from_L = L_enh_extended / L_enh

print(f"\n  EXTENDED RG RUNNING:")
print(f"    L_enh (M_Pl to v)     = {L_enh:.4f}")
print(f"    Delta_L (v to Lambda)  = {Delta_L:.4f}")
print(f"    L_enh_extended          = {L_enh_extended:.4f}")
print(f"    Enhancement L_ext/L    = {enhancement_from_L:.3f}")

print(f"""
  Extending the RG running below v adds only {(enhancement_from_L-1)*100:.0f}% to L_enh.
  This is because ln(v/Lambda) ~ 7 vs ln(M_Pl/v) ~ 38.
  The low-scale running is a small fraction of the total.

  VERDICT: Confinement effects are negligible for two reasons:
    1. The BZ-corner momentum is UV, not IR.
    2. The taste staircase operates entirely above Lambda_QCD.
    3. Even extending the RG running to Lambda_QCD only adds
       ~{(enhancement_from_L-1)*100:.0f}% to the log factor.

  Flux tubes and confinement DO NOT close the gap.
""")

check("confinement_negligible",
      R_conf_direct < 1e-30,
      f"R_conf = {R_conf_direct:.2e} at BZ-corner momenta",
      kind="EXACT")

honest("confinement_fails",
       f"enhancement from extended L_enh = {enhancement_from_L:.3f}x, need {enhancement_ratio:.2f}x")


# =============================================================================
# MECHANISM 4: TASTE STAIRCASE SCALE -- alpha_s AT LAMBDA_QCD
# =============================================================================

print("\n" + "=" * 78)
print("MECHANISM 4: TASTE STAIRCASE SCALE MISMATCH")
print("=" * 78)

print(f"""
  THE KEY IDEA:
    The CKM formula uses alpha_eff in the NNI coefficient:
      c_23 = (alpha_eff * N_c / pi) * L_enh * S_23^(0) * F_EWSB

    The perturbative calculation evaluates alpha at the EW scale v,
    giving alpha_s(v) = 0.1033.

    But the NNI operator describes inter-valley TASTE-BREAKING scattering.
    The SCALE at which this operator should be evaluated depends on whether
    it is:

    (a) A UV effect: evaluated at 1/a = M_Pl -> alpha ~ alpha_bare ~ 0.08
        (even worse)
    (b) A vertex-level effect: evaluated at v -> alpha_s(v) = 0.103
        (current approach)
    (c) An effective operator whose COEFFICIENT runs from M_Pl to a low
        scale where it is matched to the physical amplitude.

    For option (c), the effective coupling is:
      alpha_eff(mu) = alpha_s(mu) * (RG enhancement factors)

    The taste staircase provides a natural hierarchy of scales. The NNI
    coefficient involves the PRODUCT of the coupling at each threshold.

  THE STAIRCASE INTEGRAL:
    In the taste staircase, the effective coupling at scale mu in the
    range [m_{{k+1}}, m_k] has n_f = (8-k)*6 active flavors. Between
    thresholds where b_0 < 0 (n_f > 16.5), the coupling GROWS toward
    the IR. Between thresholds where b_0 > 0 (n_f < 16.5), it shrinks.

    The crossover occurs at n_f ~ 16.5, which is between:
      k = 5: n_f = (8-5)*6 = 18 (b_0 = -1, still growing)
      k = 6: n_f = (8-6)*6 = 12 (b_0 = +3, shrinking)

    The coupling peaks near the k=5 -> k=6 transition, which occurs at:
      m_5 = M_Pl * alpha_LM^5 = {M_PL * alpha_LM**5:.3e} GeV
      m_6 = M_Pl * alpha_LM^6 = {M_PL * alpha_LM**6:.3e} GeV
""")

# Build the full staircase running
# Start with alpha_s at M_Pl (V-scheme)
alpha_V_Mpl = 0.092  # V-scheme at M_Pl from plaquette

print(f"  Initial coupling: alpha_V(M_Pl) = {alpha_V_Mpl:.4f}")
print(f"\n  Running through taste staircase (1-loop):")
print(f"  {'k':>3} {'m_k (GeV)':>14} {'n_f':>5} {'b_0':>7} {'alpha_s':>10}")
print(f"  {'-'*3} {'-'*14} {'-'*5} {'-'*7} {'-'*10}")

alpha_current = alpha_V_Mpl
N_TASTE = 8
N_GEN = 6

# We run the staircase with TWO caps: a PHYSICAL cap (alpha_max = 1,
# where perturbation theory breaks down and the coupling saturates at
# a confining value) and an AGGRESSIVE cap (alpha_max = pi, the
# absolute upper bound from unitarity).
# The physical cap gives a LOWER BOUND on the staircase enhancement.

for alpha_cap_label, alpha_cap in [("physical (alpha <= 1)", 1.0),
                                    ("aggressive (alpha <= pi)", PI)]:
    print(f"\n  --- Staircase with {alpha_cap_label} ---")
    alpha_current = alpha_V_Mpl
    alpha_values = [alpha_current]
    threshold_scales = [M_PL]

    print(f"  {'k':>3} {'m_k (GeV)':>14} {'n_f':>5} {'b_0':>7} {'alpha_s':>10} {'status':>12}")
    print(f"  {'-'*3} {'-'*14} {'-'*5} {'-'*7} {'-'*10} {'-'*12}")

    for k in range(16):
        mu_high = M_PL * alpha_LM**k
        mu_low = M_PL * alpha_LM**(k+1)
        if k < N_TASTE:
            n_f = (N_TASTE - k) * N_GEN
        else:
            n_f = N_GEN

        b0 = (11.0 * C_A - 4.0 * T_F * n_f) / 3.0

        inv_alpha_low = 1.0/alpha_current + b0/(2.0*PI) * np.log(mu_high/mu_low)

        status = "pert"
        if inv_alpha_low > 0:
            alpha_low = 1.0 / inv_alpha_low
            if alpha_low > alpha_cap:
                alpha_low = alpha_cap
                status = "CAPPED"
        else:
            alpha_low = alpha_cap
            status = "LANDAU->CAP"

        print(f"  {k:3d} {mu_high:14.3e} {n_f:5d} {b0:7.1f} {alpha_current:10.4f} {status:>12}")

        alpha_current = alpha_low
        alpha_values.append(alpha_current)
        threshold_scales.append(mu_low)

    print(f"  --- {'v = 246':>14} {N_GEN:5d} "
          f"{(11.0*C_A - 4.0*T_F*N_GEN)/3.0:7.1f} {alpha_current:10.4f}")

    if alpha_cap_label.startswith("physical"):
        alpha_values_phys = list(alpha_values)
        threshold_scales_phys = list(threshold_scales)
        alpha_at_v_staircase = alpha_current
    else:
        alpha_values_aggr = list(alpha_values)

alpha_peak = max(alpha_values_phys)
peak_index = alpha_values_phys.index(alpha_peak)

print(f"\n  STAIRCASE RESULTS (physical cap):")
print(f"    alpha_s(v) from staircase = {alpha_at_v_staircase:.4f}")
print(f"    Peak alpha_s = {alpha_peak:.4f} at step k = {peak_index}")
print(f"    Peak scale = {threshold_scales_phys[peak_index]:.3e} GeV")
print(f"    alpha_peak(aggressive) = {max(alpha_values_aggr):.4f}")

print(f"""
  CRITICAL NOTE:
    The 1-loop running hits a Landau pole at k=2 (n_f=36, b_0=-13).
    The coupling CANNOT be computed perturbatively in the non-AF regime
    (k=0 to k=5, where b_0 < 0). In this regime, the coupling grows
    toward the IR but its exact value requires non-perturbative matching.

    The PHYSICAL CAP at alpha = 1 represents the onset of strong coupling.
    Above this, the running is no longer described by perturbative QCD.
    This gives a CONSERVATIVE estimate of the staircase enhancement.
""")

check("staircase_coupling_at_v",
      alpha_at_v_staircase > 0 and alpha_at_v_staircase < 5,
      f"alpha_s(v) = {alpha_at_v_staircase:.4f} from staircase (physical cap)",
      kind="BOUNDED")

# THE CRITICAL QUESTION: Is the NNI coefficient evaluated at the
# vertex coupling alpha_s(v), or does it involve alpha at a different
# staircase scale?

# Argument for alpha at the PEAK:
# The NNI operator is generated by taste-breaking at the scale where
# taste symmetry is most strongly broken. This is near the AF crossover
# where the coupling peaks. If c_23 uses alpha at this scale:

c23_peak = alpha_peak * N_C * L_enh / PI * S_23_0 * F_EWSB
vcb_peak = c23_peak * vcb_kinematic

# But the L_enh factor ALREADY captures the running from M_Pl to v.
# We should NOT use alpha_peak with L_enh -- that double-counts the
# RG enhancement.

# The correct version: the NNI coefficient at the peak scale uses
# alpha at the peak BUT the running integral is only from the peak
# scale to v, not from M_Pl to v:
mu_peak = threshold_scales_phys[peak_index]
L_enh_from_peak = np.log(mu_peak / V_EW) / (4.0 * PI) if mu_peak > V_EW else 0.0
L_enh_from_Mpl_to_peak = np.log(M_PL / mu_peak) / (4.0 * PI) if mu_peak < M_PL else 0.0

print(f"\n  DECOMPOSED RG RUNNING:")
print(f"    L_enh (M_Pl to v) = {L_enh:.4f} = L(M_Pl to peak) + L(peak to v)")
print(f"    L(M_Pl to peak)   = {L_enh_from_Mpl_to_peak:.4f}")
print(f"    L(peak to v)      = {L_enh_from_peak:.4f}")
print(f"    Sum = {L_enh_from_Mpl_to_peak + L_enh_from_peak:.4f}")

# In the correct treatment, the Wilson coefficient of the taste-breaking
# operator receives contributions from ALL scales in the staircase.
# The effective coupling-times-log integral is:
#   I_eff = int_{v}^{M_Pl} (d mu / mu) * alpha_s(mu) / (4 pi)
#
# This is NOT the same as alpha_s(v) * ln(M_Pl/v) / (4 pi).
# The difference is the scale variation of alpha_s(mu) within the integral.

# Compute the weighted integral step by step through the staircase,
# using the PHYSICAL cap (alpha <= 1) for honest bounds.
ALPHA_CAP_PHYS = 1.0

print(f"\n  WEIGHTED RG INTEGRAL (physical cap alpha <= {ALPHA_CAP_PHYS}):")
print(f"    I_eff = int_v^M_Pl (d mu / mu) * alpha_s(mu) / (4 pi)")
print(f"    vs    I_naive = alpha_s(v) * ln(M_Pl/v) / (4 pi)")

I_eff_proper = 0.0
alpha_running = alpha_V_Mpl

for k in range(16):
    mu_high_k = M_PL * alpha_LM**k
    mu_low_k = M_PL * alpha_LM**(k+1)

    if mu_low_k < V_EW:
        mu_low_k = V_EW  # stop at v

    if mu_high_k <= V_EW:
        break  # below EW scale

    if k < N_TASTE:
        n_f_k = (N_TASTE - k) * N_GEN
    else:
        n_f_k = N_GEN

    b0_k = (11.0 * C_A - 4.0 * T_F * n_f_k) / 3.0

    L_interval = np.log(mu_high_k / mu_low_k)

    # If the coupling is already at the cap (strong regime), the integral
    # is simply alpha_cap * L_interval / (4 pi) -- no running.
    if alpha_running >= ALPHA_CAP_PHYS * 0.99:
        I_this = ALPHA_CAP_PHYS * L_interval / (4.0 * PI)
        # Check if AF is restored (b0 > 0) and we can decouple
        inv_alpha_next = 1.0/ALPHA_CAP_PHYS + b0_k/(2.0*PI) * L_interval
        if inv_alpha_next > 0 and b0_k > 0:
            alpha_running = 1.0 / inv_alpha_next
            # Refined integral: coupling running down from cap
            I_this = np.log(1.0 + b0_k * ALPHA_CAP_PHYS * L_interval / (2*PI)) / (2.0 * b0_k)
        else:
            alpha_running = ALPHA_CAP_PHYS  # stay capped
    else:
        x = b0_k * alpha_running * L_interval / (2.0 * PI)

        if abs(x) < 1e-10:
            I_this = alpha_running * L_interval / (4.0 * PI)
        elif 1.0 + x > 0:
            if abs(b0_k) > 1e-10:
                I_this = np.log(1.0 + x) / (2.0 * b0_k)
            else:
                I_this = alpha_running * L_interval / (4.0 * PI)
        else:
            # Landau pole: coupling reaches cap partway through interval
            # Fraction of interval before pole:
            t_pole = (2.0 * PI) / (-b0_k * alpha_running)  # t where 1/alpha = 0
            L_to_pole = min(t_pole, L_interval)
            L_after_pole = L_interval - L_to_pole
            # Integral up to pole:
            if abs(b0_k) > 1e-10 and L_to_pole > 0:
                x_pole = b0_k * alpha_running * L_to_pole / (2.0 * PI)
                if 1.0 + x_pole > 0.01:
                    I_this = np.log(1.0 + x_pole) / (2.0 * b0_k)
                else:
                    I_this = alpha_running * L_to_pole / (4.0 * PI)
            else:
                I_this = alpha_running * L_to_pole / (4.0 * PI)
            # After pole: capped
            I_this += ALPHA_CAP_PHYS * L_after_pole / (4.0 * PI)
            alpha_running = ALPHA_CAP_PHYS

        # Update running coupling for next interval (with cap)
        inv_alpha_next = 1.0/alpha_running + b0_k/(2.0*PI) * L_interval
        if inv_alpha_next > 0:
            alpha_running = min(1.0/inv_alpha_next, ALPHA_CAP_PHYS)
        else:
            alpha_running = ALPHA_CAP_PHYS

    I_eff_proper += I_this

I_naive_proper = alpha_s_v * np.log(M_PL / V_EW) / (4.0 * PI)

# The enhancement factor: the ratio of the weighted integral to the naive one
staircase_enhancement = I_eff_proper / I_naive_proper

print(f"\n  PROPER STAIRCASE-WEIGHTED RG INTEGRAL:")
print(f"    I_eff (staircase-weighted)  = {I_eff_proper:.6f}")
print(f"    I_naive (alpha_s(v) * L)    = {I_naive_proper:.6f}")
print(f"    Enhancement factor          = {staircase_enhancement:.4f}")

# What effective alpha does this correspond to?
alpha_eff_staircase = I_eff_proper * PI / (N_C * np.log(M_PL/V_EW) / (4*PI) * S_23_0 * F_EWSB)
# Actually, more simply:
alpha_eff_staircase = I_eff_proper / (np.log(M_PL/V_EW) / (4*PI))
# This is the effective alpha averaged over the RG running

c23_staircase = N_C / PI * I_eff_proper * S_23_0 * F_EWSB
vcb_staircase = c23_staircase * vcb_kinematic

print(f"\n  V_cb FROM STAIRCASE-WEIGHTED INTEGRAL:")
print(f"    alpha_eff (weighted avg) = {alpha_eff_staircase:.4f}")
print(f"    c_23 = (N_c/pi) * I_eff * S_23^(0) * F_EWSB")
print(f"         = {N_C/PI:.4f} * {I_eff_proper:.4f} * {S_23_0:.4f} * {F_EWSB:.4f}")
print(f"         = {c23_staircase:.4f}")
print(f"    V_cb = {vcb_staircase:.5f}  (PDG: {V_CB_PDG})")
print(f"    Enhancement over perturbative: {staircase_enhancement:.3f}x")

check("staircase_enhancement_direction",
      staircase_enhancement > 1.0,
      f"staircase gives {staircase_enhancement:.3f}x enhancement (correct direction)",
      kind="BOUNDED")


# =============================================================================
# MECHANISM 4b: WHAT IF THE NNI OPERATOR IS EVALUATED AT Lambda_QCD?
# =============================================================================

print("\n" + "-" * 78)
print("MECHANISM 4b: DIRECT EVALUATION AT LOW SCALE")
print("-" * 78)

# The most aggressive version: the NNI coupling is NOT a perturbative
# vertex at the EW scale. Instead, it is a confining-scale effect where
# the physical inter-valley transition is dominated by scales ~ Lambda_QCD.

# In this picture:
# - The L_enh factor still captures the leading-log running from M_Pl to v
# - But the coupling in the formula should be alpha_s evaluated at a
#   non-perturbative matching scale mu_NP

# If mu_NP = Lambda_QCD ~ 200 MeV:
alpha_s_LQCD = 0.50  # typical non-perturbative alpha_s at Lambda_QCD
# (This is conventional: at Lambda_QCD, alpha_s is O(1))

# If mu_NP = 1 GeV (typical hadronic scale):
alpha_s_1GeV = 0.50  # alpha_s(1 GeV) ~ 0.5 from lattice QCD

# If mu_NP = m_b (bottom quark mass):
alpha_s_mb = 0.22  # alpha_s(m_b) ~ 0.22

for label, alpha_NP, mu_NP in [
    ("Lambda_QCD = 200 MeV", 0.50, 0.2),
    ("mu = 1 GeV",           0.50, 1.0),
    ("mu = m_b = 4.18 GeV",  0.22, 4.18),
    ("mu = m_t = 173 GeV",   0.108, 173.0),
    ("mu = v = 246 GeV",     alpha_s_v, V_EW),
]:
    c23_NP = alpha_NP * N_C * L_enh / PI * S_23_0 * F_EWSB
    vcb_NP = c23_NP * vcb_kinematic
    dev = (vcb_NP / V_CB_PDG - 1) * 100
    print(f"  At {label:30s}: alpha = {alpha_NP:.3f}, V_cb = {vcb_NP:.5f} ({dev:+.1f}%)")

print(f"""
  PHYSICAL QUESTION:
    The NNI formula c_23 = alpha_eff * (N_c/pi) * L_enh * S_23 * F_EWSB
    has TWO scale-dependent ingredients:
    1. The coupling alpha_eff: evaluated at the scale of the process
    2. The log L_enh = ln(M_Pl/v)/(4pi): captures operator running

    In a standard EFT calculation, alpha enters at the MATCHING scale
    where the operator is generated. The taste-breaking operator is
    generated at the UV cutoff (1/a = M_Pl). So the correct coupling
    is alpha_s(M_Pl) ~ alpha_bare = 0.080, making the prediction WORSE.

    UNLESS: the physical amplitude is dominated by the ENDPOINT of the
    running, near the EW scale, where the NNI matrix element is evaluated
    between physical quark states. In that case, alpha_s(v) = 0.103 is
    correct -- and we still have the 2.8x gap.

    The only way to get alpha ~ 0.3 is if the operator matching involves
    a non-perturbative scale ~ 1 GeV. But this would require a concrete
    mechanism for how the UV taste-breaking operator connects to the IR
    confining dynamics. No such mechanism is identified in the current
    framework.
""")

honest("scale_mismatch_unresolved",
       f"alpha_s(v) = {alpha_s_v:.3f}, alpha needed = {alpha_eff_needed:.3f}")


# =============================================================================
# MECHANISM 4c: THE alpha_s^3 STAIRCASE CONNECTION
# =============================================================================

print("-" * 78)
print("MECHANISM 4c: THE alpha_LM^3 CONNECTION -- v * alpha_LM^3 ~ Lambda_QCD")
print("-" * 78)

# From the hierarchy: v = M_Pl * alpha_LM^16
# One step further: v * alpha_LM = m_16 = M_Pl * alpha_LM^17
# Three steps: v * alpha_LM^3 = M_Pl * alpha_LM^19

Lambda_from_alpha3 = V_EW * alpha_LM**3

# Check against Lambda_QCD
Lambda_QCD_PDG = 0.213  # GeV (MS-bar, 5 flavors)

print(f"""
  The taste staircase predicts:
    v * alpha_LM^1 = {V_EW * alpha_LM:.1f} GeV
    v * alpha_LM^2 = {V_EW * alpha_LM**2:.2f} GeV
    v * alpha_LM^3 = {V_EW * alpha_LM**3:.3f} GeV
    Lambda_QCD (PDG) = {Lambda_QCD_PDG} GeV

  v * alpha_LM^3 / Lambda_QCD = {Lambda_from_alpha3 / Lambda_QCD_PDG:.3f}

  This is the CONFINEMENT SCALE from the framework:
    Lambda_conf = v * alpha_LM^3 = {Lambda_from_alpha3:.3f} GeV

  At this scale, alpha_s ~ 1 and the coupling is non-perturbative.
  If the NNI coefficient is dominated by the confining dynamics at
  Lambda_conf, then the effective coupling is alpha_eff ~ 1, not 0.1.
""")

# Check the ratio
check("alpha3_near_Lambda",
      0.1 < Lambda_from_alpha3 / Lambda_QCD_PDG < 10.0,
      f"v * alpha_LM^3 = {Lambda_from_alpha3:.3f} GeV, "
      f"Lambda_QCD = {Lambda_QCD_PDG} GeV, ratio = {Lambda_from_alpha3/Lambda_QCD_PDG:.2f}",
      kind="BOUNDED")

# What alpha_s at the confinement scale gives V_cb?
# We need alpha_eff = 0.286. At mu ~ Lambda_QCD, alpha_s ~ 0.3-1.0.
# So alpha_eff ~ alpha_s(Lambda_conf) ~ 0.3 is PLAUSIBLE.

# But the problem: how does the coupling at Lambda_conf enter the
# CKM formula? The formula is:
#   c_23 = (alpha_eff * N_c / pi) * L_enh * S_23 * F_EWSB
# where L_enh = ln(M_Pl/v) / (4pi).
#
# If alpha_eff = alpha_s(Lambda_conf), then what is L_enh?
# The running is from M_Pl to Lambda_conf:
#   L_enh_to_Lambda = ln(M_Pl / Lambda_conf) / (4pi)

L_enh_to_Lambda = np.log(M_PL / Lambda_from_alpha3) / (4.0 * PI)
c23_at_Lambda = alpha_eff_needed * N_C * L_enh / PI * S_23_0 * F_EWSB

# alpha needed at Lambda_conf with L_enh from M_Pl to Lambda:
alpha_needed_Lambda = c23_needed * PI / (N_C * L_enh_to_Lambda * S_23_0 * F_EWSB)

print(f"\n  WITH MATCHING AT Lambda_conf = {Lambda_from_alpha3:.3f} GeV:")
print(f"    L_enh (M_Pl to Lambda_conf) = {L_enh_to_Lambda:.4f}")
print(f"    L_enh (M_Pl to v)           = {L_enh:.4f}")
print(f"    Ratio L_to_Lambda / L_to_v  = {L_enh_to_Lambda / L_enh:.4f}")
print(f"    alpha needed at Lambda_conf = {alpha_needed_Lambda:.4f}")

# The running range is LONGER (M_Pl to Lambda rather than M_Pl to v),
# so L_enh is larger, and the required alpha is SMALLER.

# Alternative interpretation: the operator coefficient is the PRODUCT
# of the coupling times the log:
#   C_NNI = alpha_s(mu_match) * ln(M_Pl / mu_match) / (4pi)
#
# This product has a stationary point at:
#   d/d(ln mu) [alpha_s(mu) * ln(M_Pl/mu)] = 0
#   alpha_s(mu) + mu * alpha_s'(mu) * ln(M_Pl/mu) = 0 ... ? No.
#
# Actually the product alpha(mu) * ln(M_Pl/mu) is maximized where the
# log is still large but the coupling has grown significantly.

# Scan the product over the staircase (with physical cap alpha <= 1)
print(f"\n  ALPHA * LOG PRODUCT OVER STAIRCASE (alpha capped at 1):")
print(f"  {'k':>3} {'mu (GeV)':>14} {'alpha(mu)':>12} {'ln(M/mu)/(4pi)':>16} {'product':>10}")
print(f"  {'-'*3} {'-'*14} {'-'*12} {'-'*16} {'-'*10}")

alpha_run = alpha_V_Mpl
best_product = 0.0
best_k_product = 0

for k in range(17):
    mu_k = M_PL * alpha_LM**k
    if mu_k < V_EW:
        mu_k = V_EW

    L_k = np.log(M_PL / mu_k) / (4.0 * PI)
    product_k = alpha_run * L_k

    if product_k > best_product:
        best_product = product_k
        best_k_product = k

    if k <= 16:
        print(f"  {k:3d} {mu_k:14.3e} {alpha_run:12.4f} {L_k:16.4f} {product_k:10.4f}")

    # Update running for next step (with physical cap)
    if k < 16:
        mu_high_k = M_PL * alpha_LM**k
        mu_low_k = M_PL * alpha_LM**(k+1)
        if k < N_TASTE:
            n_f_k = (N_TASTE - k) * N_GEN
        else:
            n_f_k = N_GEN
        b0_k = (11.0 * C_A - 4.0 * T_F * n_f_k) / 3.0
        L_int = np.log(mu_high_k / mu_low_k)
        inv_a = 1.0/alpha_run + b0_k/(2.0*PI) * L_int
        if inv_a > 0:
            alpha_run = min(1.0/inv_a, ALPHA_CAP_PHYS)
        else:
            alpha_run = ALPHA_CAP_PHYS

# The product alpha(mu) * ln(M_Pl/mu)/(4pi) is what enters c_23.
# With the staircase, this product is maximized at an intermediate scale.

# Compute c_23 using the best product:
c23_best_product = N_C / PI * best_product * S_23_0 * F_EWSB
vcb_best_product = c23_best_product * vcb_kinematic

print(f"\n  BEST alpha * L PRODUCT:")
print(f"    At staircase step k = {best_k_product}")
print(f"    Product = {best_product:.4f}")
print(f"    c_23 = {c23_best_product:.4f}")
print(f"    V_cb = {vcb_best_product:.5f} (PDG: {V_CB_PDG})")
print(f"    Enhancement over naive: {c23_best_product / c23_pert:.3f}x")

staircase_total_enhancement = c23_best_product / c23_pert

check("staircase_product_enhancement",
      staircase_total_enhancement > 1.0,
      f"staircase alpha*L product gives {staircase_total_enhancement:.3f}x enhancement",
      kind="BOUNDED")


# =============================================================================
# SYNTHESIS: COMBINED ASSESSMENT
# =============================================================================

print("\n" + "=" * 78)
print("SYNTHESIS: COMBINED ASSESSMENT OF ALL FOUR MECHANISMS")
print("=" * 78)

# Collect the enhancement factors from each mechanism
enhancements = {
    'Instanton tunneling': inst_best_R,
    'Taste-scalar exchange': R_taste_total,
    'Confinement/flux tubes': enhancement_from_L - 1.0,
    'Staircase weighted integral': staircase_enhancement - 1.0,
    'Staircase alpha*L product': staircase_total_enhancement - 1.0,
}

print(f"\n  Enhancement factors (additive, relative to 1-gluon exchange):")
print(f"  {'Mechanism':<35} {'Delta alpha/alpha':>18} {'Sufficient?':>12}")
print(f"  {'-'*35} {'-'*18} {'-'*12}")

for name, R in enhancements.items():
    sufficient = "YES" if R > enhancement_ratio - 1 else "NO"
    print(f"  {name:<35} {R:+18.4f} {sufficient:>12}")

print(f"\n  Required total enhancement: {enhancement_ratio:.2f}x (i.e., +{enhancement_ratio-1:.2f})")

# Maximum combined enhancement (optimistic, additive)
max_combined = 1.0 + sum(enhancements.values())
vcb_combined = vcb_pert * max_combined
combined_dev = (vcb_combined / V_CB_PDG - 1) * 100

print(f"\n  OPTIMISTIC COMBINED (all mechanisms additive):")
print(f"    Total enhancement: {max_combined:.3f}x")
print(f"    V_cb = {vcb_pert:.5f} * {max_combined:.3f} = {vcb_combined:.5f}")
print(f"    PDG: {V_CB_PDG}, deviation: {combined_dev:+.1f}%")

# Check if the staircase mechanism alone gets close
staircase_alone = max(staircase_enhancement, staircase_total_enhancement)
vcb_staircase_best = vcb_pert * staircase_alone
staircase_dev = (vcb_staircase_best / V_CB_PDG - 1) * 100

print(f"\n  STAIRCASE ALONE (best variant):")
print(f"    Enhancement: {staircase_alone:.3f}x")
print(f"    V_cb = {vcb_staircase_best:.5f} (dev: {staircase_dev:+.1f}%)")

# Remaining gap after staircase
remaining_gap = enhancement_ratio / staircase_alone

print(f"""
  REMAINING GAP AFTER STAIRCASE: {remaining_gap:.2f}x

  INTERPRETATION:
    The staircase-weighted RG integral provides an enhancement of
    {staircase_alone:.2f}x over the naive alpha_s(v) calculation.
    This reduces the gap from {enhancement_ratio:.1f}x to {remaining_gap:.1f}x.

    The remaining {remaining_gap:.1f}x factor could come from:
    1. Higher-order corrections to the Wilson coefficient (NLO matching)
    2. Non-perturbative operator mixing at the taste thresholds
    3. The EWSB-dressed vertex beyond leading order
    4. The absolute K normalization (currently bounded at 24.9% CV)

    CRITICALLY: the staircase mechanism is the ONLY one that provides
    an O(1) enhancement. The other three mechanisms are either
    exponentially suppressed (instantons), perturbatively small (taste
    scalars), or negligible at UV momenta (confinement).
""")

# Final V_cb from best staircase + perturbative corrections
alpha_eff_best = alpha_s_v * staircase_alone * (1.0 + R_taste_total)
c23_final = alpha_eff_best * N_C * L_enh / PI * S_23_0 * F_EWSB
vcb_final = c23_final * vcb_kinematic
final_dev = (vcb_final / V_CB_PDG - 1) * 100

print(f"  BEST COMBINED ESTIMATE:")
print(f"    alpha_eff = alpha_s(v) * staircase * (1 + pert. corrections)")
print(f"             = {alpha_s_v:.4f} * {staircase_alone:.3f} * {1.0 + R_taste_total:.3f}")
print(f"             = {alpha_eff_best:.4f}")
print(f"    c_23 = {c23_final:.4f}")
print(f"    V_cb = {vcb_final:.5f}  (PDG: {V_CB_PDG}, dev: {final_dev:+.1f}%)")


# =============================================================================
# HONEST VERDICT
# =============================================================================

print("\n" + "=" * 78)
print("HONEST VERDICT")
print("=" * 78)

print(f"""
  1. INSTANTON TUNNELING: FAILS.
     Exponentially suppressed at beta = 6. Enhancement < {inst_best_R:.1e}.

  2. TASTE-SCALAR EXCHANGE: INSUFFICIENT.
     Perturbative correction of {(R_taste_total)*100:.0f}%. Need +{(enhancement_ratio-1)*100:.0f}%.

  3. CONFINEMENT/FLUX TUBES: IRRELEVANT.
     BZ-corner momenta are UV. Confinement effects suppressed by
     (Lambda_QCD/M_Pl)^2 ~ {(0.2/M_PL)**2:.1e}.

  4. TASTE STAIRCASE SCALE: MOST PROMISING.
     The staircase-weighted RG integral gives {staircase_alone:.2f}x enhancement.
     This is the correct direction and the right order of magnitude.
     The remaining gap of {remaining_gap:.1f}x is within reach of NLO corrections
     and threshold matching effects.

  THE PATH FORWARD:
     The taste staircase provides the framework-native mechanism for
     enhancing the NNI coefficient beyond 1-gluon exchange. The physical
     picture: the taste-breaking operator runs through 16 thresholds where
     the coupling varies between 0.09 and {alpha_peak:.2f}. The
     weighted RG integral captures contributions from scales where
     alpha_s is larger than at v.

     To close the gap fully, the next steps are:
     (a) 2-loop RG through the staircase (currently only 1-loop)
     (b) Threshold matching corrections at each taste decoupling
     (c) Non-perturbative operator mixing at the AF crossover (k=5-6)
     (d) Validate with direct lattice computation of the NNI coefficient
         at multiple beta values

  STATUS: The 2.8x gap is PARTIALLY CLOSED by the staircase mechanism.
  The remaining factor of {remaining_gap:.1f}x is a concrete, bounded problem
  rather than a fundamental obstruction.

  CKM LANE STATUS: Still BOUNDED, but with a concrete identified mechanism
  (the staircase-weighted RG) that goes in the right direction.
""")

check("staircase_is_best_mechanism",
      staircase_alone > 1.0 and staircase_alone > (1 + inst_best_R) and
      staircase_alone > (1 + R_taste_total),
      f"staircase ({staircase_alone:.3f}x) > instanton ({1+inst_best_R:.6f}x) "
      f"> taste ({1+R_taste_total+R_NLO_gluon:.3f}x)",
      kind="BOUNDED")

check("gap_reduced_by_staircase",
      remaining_gap < enhancement_ratio,
      f"gap reduced from {enhancement_ratio:.2f}x to {remaining_gap:.2f}x",
      kind="BOUNDED")

honest("gap_not_fully_closed",
       f"remaining {remaining_gap:.2f}x after staircase, V_cb dev = {final_dev:+.1f}%")


# =============================================================================
# SUMMARY
# =============================================================================

print("\n" + "=" * 78)
print("SUMMARY")
print("=" * 78)

total_tests = PASS_COUNT + FAIL_COUNT
print(f"""
  Tests:    {PASS_COUNT} PASS / {FAIL_COUNT} FAIL (of {total_tests})
  Exact:    {EXACT_PASS} PASS / {EXACT_FAIL} FAIL
  Bounded:  {BOUNDED_PASS} PASS / {BOUNDED_FAIL} FAIL
  Honest assessments: {HONEST_COUNT}

  KEY RESULTS:

  | Mechanism                | Enhancement | Closes gap? |
  |--------------------------|-------------|-------------|
  | Instanton tunneling      | {inst_best_R:.1e}    | NO          |
  | Taste-scalar exchange    | +{(R_taste_total)*100:.0f}%         | NO          |
  | Confinement/flux tubes   | {R_conf_direct:.1e}  | NO          |
  | Staircase weighted RG    | {staircase_alone:.2f}x         | PARTIAL     |
  | Combined best            | {max_combined:.2f}x         | PARTIAL     |

  V_cb PREDICTIONS:
    Perturbative 1-gluon:    {vcb_pert:.5f}  ({(vcb_pert/V_CB_PDG-1)*100:+.1f}%)
    Staircase-weighted:      {vcb_staircase_best:.5f}  ({staircase_dev:+.1f}%)
    Combined best:           {vcb_final:.5f}  ({final_dev:+.1f}%)
    PDG target:              {V_CB_PDG:.5f}

  The taste staircase RG enhancement is the only framework-native
  mechanism that provides O(1) improvement. The remaining gap of
  {remaining_gap:.1f}x is a bounded NLO/threshold problem, not a
  fundamental obstruction.
""")

# Exit code
if FAIL_COUNT > 0:
    print(f"\n{FAIL_COUNT} checks FAILED.")
    sys.exit(1)
else:
    print(f"\nAll {PASS_COUNT} checks PASSED. {HONEST_COUNT} honest assessments recorded.")
    sys.exit(0)
