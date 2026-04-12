#!/usr/bin/env python3
"""
U(1) Hypercharge Coupling from Edge Geometry
=============================================

THE LAST MISSING PIECE: deriving g_Y^2 from the cubic lattice edge structure
to complete the gauge coupling triad:

  SU(3): g_3^2 = 1             from Z_3 clock-shift algebra       [DONE]
  SU(2): g_2^2 = 1/(d+1) = 1/4 from Z_2 bipartite geometry       [DONE, 1.6%]
  U(1):  g_Y^2 = ???           from edge graph structure           [THIS SCRIPT]

STRATEGY:
  1. Catalog cubic lattice edge graph properties (d=3)
  2. Enumerate ~30 candidate formulas f(d) for g_Y^2
  3. For each candidate:
     a) Compute sin^2(theta_W) at the bare (Planck) scale
     b) Run to M_Z using 1-loop SM beta functions
     c) Run to M_Z using 2-loop SM beta functions
     d) Compare to sin^2(theta_W)(M_Z) = 0.23122 and alpha_EM(M_Z) = 1/127.95
  4. Rank candidates by combined accuracy
  5. Test dimensional consistency: does the best formula work for d=2,3,4,5?
  6. Special focus: sin^2(theta_W)(bare) = (d-1)/(d+1) = 1/2 hypothesis

TARGET VALUES (reverse-engineered from observation):
  g_Y^2(bare) ~ 0.230 at M_Planck (from 1-loop running)
  sin^2(theta_W)(bare) ~ 0.479 at M_Planck

Self-contained: numpy + scipy only.
PStack experiment: u1-coupling-derivation
"""

from __future__ import annotations

import math
import os
import sys
import time
from collections import OrderedDict

import numpy as np

try:
    from scipy.optimize import brentq
except ImportError:
    print("ERROR: scipy required for root-finding. pip install scipy")
    sys.exit(1)

np.set_printoptions(precision=8, linewidth=120)

LOG_FILE = "logs/" + time.strftime("%Y-%m-%d") + "-u1_coupling_derivation.txt"

results = []
def log(msg=""):
    results.append(msg)
    print(msg)


# =============================================================================
# PHYSICAL CONSTANTS (PDG 2024 / CODATA 2022)
# =============================================================================

PI = np.pi

# Electromagnetic
ALPHA_EM_OBS = 1.0 / 137.035999084     # CODATA 2022 (low energy)
ALPHA_EM_MZ  = 1.0 / 127.951           # at M_Z (PDG 2024)

# Strong coupling
ALPHA_S_MZ = 0.1179                     # PDG 2024

# Electroweak
SIN2_TW_MZ = 0.23122                    # sin^2(theta_W) at M_Z, MS-bar (PDG 2024)
SIN2_TW_MZ_ERR = 0.00003
M_Z = 91.1876                           # GeV
M_W = 80.3692                           # GeV

# Mass scales
M_PLANCK = 1.2209e19                    # GeV (full Planck mass)
M_PLANCK_RED = 2.435e18                 # GeV (reduced)

# Quark masses for thresholds
M_TOP = 172.57                          # GeV
M_BOTTOM = 4.183                        # GeV

# Framework bare couplings (established)
ALPHA_S_BARE = 1.0 / (4 * PI)           # SU(3): g_3^2 = 1
G2_SQ = 0.25                            # SU(2): g_2^2 = 1/(d+1) = 1/4
ALPHA_2_BARE = G2_SQ / (4 * PI)         # = 1/(16*pi)

# SM couplings at M_Z
ALPHA_2_MZ = ALPHA_EM_MZ / SIN2_TW_MZ
ALPHA_Y_MZ = ALPHA_EM_MZ / (1.0 - SIN2_TW_MZ)
ALPHA_1_MZ = (5.0 / 3.0) * ALPHA_Y_MZ  # GUT normalized

# Spatial dimension
D = 3


# =============================================================================
# 1-LOOP BETA COEFFICIENTS
# =============================================================================

# SM 1-loop beta coefficients (N_f = 5 active flavors below M_top)
# Convention: d(1/alpha_i)/d(ln mu) = b_i / (2*pi)
B1_1LOOP = -41.0 / 10.0    # U(1)_Y GUT normalized: coupling GROWS at high E
B2_1LOOP = 19.0 / 6.0      # SU(2)_L: asymptotically free
B3_1LOOP = 7.0              # SU(3)_c: AF, 5 flavors

# With 6 flavors (above M_top)
B1_1LOOP_6F = B1_1LOOP - 1.0 / 10.0
B2_1LOOP_6F = B2_1LOOP - 1.0 / 6.0
B3_1LOOP_6F = 23.0 / 3.0


# =============================================================================
# 2-LOOP BETA COEFFICIENTS
# =============================================================================

# SM 2-loop beta coefficient matrix b_ij (N_f = 5)
# Convention: d(1/alpha_i)/d(ln mu) = b_i/(2*pi) + sum_j b_ij * alpha_j / (8*pi^2)
#
# From Machacek & Vaughn (1984), Jones (1982):
# For U(1)_Y (GUT normalized), SU(2)_L, SU(3)_c with N_f fermion generations:
#
# b_ij matrix (5 generations of fermions, i.e. N_g = 3 generations, N_f = 5 quarks):
# Actually standard SM with N_g = 3 generations:

# 2-loop coefficients for SM with N_g = 3 generations
# b_ij where i,j in {1,2,3} (GUT normalized for U(1))
# From Arason et al. (1992), Luo & Xiao (2003)
B_2LOOP = np.array([
    [ -199.0/50.0,  -27.0/10.0,  -44.0/5.0 ],   # d alpha_1
    [   -9.0/10.0,  -35.0/6.0,   -12.0     ],    # d alpha_2
    [  -11.0/10.0,   -9.0/2.0,    26.0      ],    # d alpha_3
], dtype=float)


# =============================================================================
# RUNNING MACHINERY
# =============================================================================

def run_1loop(alpha_high, b_coeff, mu_high, mu_low):
    """1-loop running from mu_high down to mu_low.

    1/alpha(mu_low) = 1/alpha(mu_high) - b/(2*pi) * ln(mu_high/mu_low)
    """
    L = np.log(mu_high / mu_low)
    inv_alpha = 1.0 / alpha_high - b_coeff * L / (2 * PI)
    if inv_alpha <= 0:
        return float('inf')
    return 1.0 / inv_alpha


def run_2loop_step(alphas, b1, b2, dt):
    """Single Euler step of 2-loop RG equations.

    alphas = [alpha_1, alpha_2, alpha_3] (GUT normalized for alpha_1)
    b1 = [b_1, b_2, b_3] 1-loop coefficients
    b2 = 3x3 2-loop coefficient matrix
    dt = d(ln mu) step size

    Returns updated alphas after step dt.

    If alpha_3 hits a Landau pole, it is frozen at a large value (alpha_max)
    so the electroweak sector can continue running. The alpha_3 Landau pole
    is a known issue with the framework's bare coupling alpha_3 = 1/(4*pi),
    but it does not affect the U(1)/SU(2) sector at leading order.
    """
    ALPHA_MAX = 5.0  # cap to prevent inf propagation
    new_alphas = np.zeros(3)
    for i in range(3):
        # d(1/alpha_i)/d(ln mu) = b_i/(2*pi) + sum_j b_ij * alpha_j / (8*pi^2)
        # Use capped alphas for 2-loop cross-terms to prevent blowup
        deriv = b1[i] / (2 * PI)
        for j in range(3):
            a_j = min(alphas[j], ALPHA_MAX)
            deriv += b2[i, j] * a_j / (8 * PI**2)
        inv_alpha_new = 1.0 / alphas[i] + deriv * dt
        if inv_alpha_new <= 0:
            new_alphas[i] = ALPHA_MAX
        else:
            new_alphas[i] = min(1.0 / inv_alpha_new, ALPHA_MAX)
    return new_alphas


def run_2loop_full(alpha_1_bare, alpha_2_bare, alpha_3_bare,
                   mu_uv=M_PLANCK, mu_ir=M_Z, n_steps=2000):
    """2-loop running from mu_uv down to mu_ir with threshold at M_top.

    Uses Euler integration of the 2-loop beta functions.

    IMPORTANT: alpha_3 = 1/(4*pi) hits a Landau pole before reaching M_Z.
    For the electroweak sector, we use a HYBRID approach:
      - Run alpha_1, alpha_2 with their own 2-loop terms (including mutual mixing)
      - For the alpha_3 contribution to 2-loop EW running, use the OBSERVED
        alpha_3 trajectory (known from lattice QCD / experiment) instead of
        the framework's bare value. This is justified because the alpha_3
        2-loop correction to EW running is small (~1%) and we want to isolate
        the effect of the U(1)/SU(2) bare couplings.
    """
    # Strategy: run alpha_1 and alpha_2 with 2-loop EW mixing but use
    # an interpolated alpha_3(mu) from observation for the cross terms.
    # alpha_3(mu) from M_Z to M_Planck (1-loop, using observed alpha_s(M_Z)):
    # 1/alpha_3(mu) = 1/alpha_3(M_Z) + b_3 * ln(mu/M_Z) / (2*pi)

    def alpha_3_obs(mu):
        """Observed alpha_3(mu) trajectory for 2-loop cross-term."""
        if mu <= M_Z:
            return ALPHA_S_MZ
        elif mu <= M_TOP:
            L = np.log(mu / M_Z)
            inv_a = 1.0 / ALPHA_S_MZ + B3_1LOOP * L / (2 * PI)
            return 1.0 / inv_a if inv_a > 0 else 0.5
        else:
            # First run to M_top with 5 flavors
            L1 = np.log(M_TOP / M_Z)
            inv_a_top = 1.0 / ALPHA_S_MZ + B3_1LOOP * L1 / (2 * PI)
            # Then run above M_top with 6 flavors
            L2 = np.log(mu / M_TOP)
            inv_a = inv_a_top + B3_1LOOP_6F * L2 / (2 * PI)
            return 1.0 / inv_a if inv_a > 0 else 0.01

    alphas_12 = np.array([alpha_1_bare, alpha_2_bare])

    # 2-loop EW sub-matrix (2x2)
    b2_ew = B_2LOOP[:2, :2]

    def step_ew(a12, b1_ew, mu, dt):
        """Single step for EW sector with alpha_3 from observation."""
        a3 = alpha_3_obs(mu)
        new = np.zeros(2)
        for i in range(2):
            deriv = b1_ew[i] / (2 * PI)
            # 2-loop EW mixing
            for j in range(2):
                deriv += b2_ew[i, j] * a12[j] / (8 * PI**2)
            # 2-loop alpha_3 cross-term
            deriv += B_2LOOP[i, 2] * a3 / (8 * PI**2)
            inv_new = 1.0 / a12[i] + deriv * dt
            if inv_new <= 0:
                new[i] = 5.0
            else:
                new[i] = 1.0 / inv_new
        return new

    # Phase 1: mu_uv -> M_top (6 flavors)
    if mu_uv > M_TOP:
        b1_6f_ew = np.array([B1_1LOOP_6F, B2_1LOOP_6F])
        L1 = np.log(mu_uv / M_TOP)
        dt1 = -L1 / n_steps
        for k in range(n_steps):
            mu_k = mu_uv * np.exp(dt1 * k)
            alphas_12 = step_ew(alphas_12, b1_6f_ew, mu_k, dt1)

    # Phase 2: M_top -> mu_ir (5 flavors)
    mu_top_eff = min(mu_uv, M_TOP)
    if mu_top_eff > mu_ir:
        b1_5f_ew = np.array([B1_1LOOP, B2_1LOOP])
        L2 = np.log(mu_top_eff / mu_ir)
        dt2 = -L2 / n_steps
        for k in range(n_steps):
            mu_k = mu_top_eff * np.exp(dt2 * k)
            alphas_12 = step_ew(alphas_12, b1_5f_ew, mu_k, dt2)

    # Return with a placeholder alpha_3
    return np.array([alphas_12[0], alphas_12[1], ALPHA_S_MZ])


def electroweak_observables(alpha_1, alpha_2):
    """Compute alpha_EM and sin^2(theta_W) from GUT-normalized alpha_1 and alpha_2."""
    if alpha_1 >= 5.0 or alpha_2 >= 5.0 or alpha_1 <= 0 or alpha_2 <= 0:
        return float('inf'), 0.0, 0.0

    # alpha_Y = (3/5) * alpha_1
    alpha_Y = (3.0 / 5.0) * alpha_1
    # 1/alpha_EM = 1/alpha_Y + 1/alpha_2
    inv_alpha_em = 1.0 / alpha_Y + 1.0 / alpha_2
    alpha_em = 1.0 / inv_alpha_em if inv_alpha_em > 0 else float('inf')
    # sin^2(theta_W) = alpha_EM / alpha_2 = g'^2 / (g^2 + g'^2)
    sin2tw = alpha_em / alpha_2 if alpha_2 > 0 else 0.0

    return alpha_em, inv_alpha_em, sin2tw


def run_and_evaluate(g_Y_sq, g_2_sq=G2_SQ, g_3_sq=1.0,
                     mu_uv=M_PLANCK, use_2loop=False):
    """Full evaluation pipeline for a candidate g_Y^2.

    Converts bare g^2 to alpha, runs to M_Z, computes observables.
    Returns dict with all results and errors.
    """
    # Bare couplings
    alpha_3_bare = g_3_sq / (4 * PI)
    alpha_2_bare = g_2_sq / (4 * PI)
    alpha_Y_bare = g_Y_sq / (4 * PI)
    alpha_1_bare = (5.0 / 3.0) * alpha_Y_bare  # GUT normalization

    # Bare-scale electroweak
    sin2tw_bare = g_Y_sq / (g_Y_sq + g_2_sq)

    if use_2loop:
        alphas_mz = run_2loop_full(alpha_1_bare, alpha_2_bare, alpha_3_bare,
                                   mu_uv=mu_uv)
        alpha_1_mz, alpha_2_mz, alpha_3_mz = alphas_mz
    else:
        # 1-loop with threshold
        # Above M_top: 6 flavors
        a1_top = run_1loop(alpha_1_bare, B1_1LOOP_6F, mu_uv, M_TOP)
        a2_top = run_1loop(alpha_2_bare, B2_1LOOP_6F, mu_uv, M_TOP)
        a3_top = run_1loop(alpha_3_bare, B3_1LOOP_6F, mu_uv, M_TOP)
        # Below M_top: 5 flavors
        alpha_1_mz = run_1loop(a1_top, B1_1LOOP, M_TOP, M_Z)
        alpha_2_mz = run_1loop(a2_top, B2_1LOOP, M_TOP, M_Z)
        alpha_3_mz = run_1loop(a3_top, B3_1LOOP, M_TOP, M_Z)

    alpha_em, inv_alpha_em, sin2tw_mz = electroweak_observables(alpha_1_mz, alpha_2_mz)

    # Errors relative to observation
    err_sin2tw = abs(sin2tw_mz - SIN2_TW_MZ) / SIN2_TW_MZ * 100
    err_alpha_em = abs(inv_alpha_em - 1.0/ALPHA_EM_MZ) / (1.0/ALPHA_EM_MZ) * 100 \
        if inv_alpha_em < float('inf') else float('inf')
    err_combined = np.sqrt(err_sin2tw**2 + err_alpha_em**2)

    return {
        "g_Y_sq": g_Y_sq,
        "g_2_sq": g_2_sq,
        "sin2tw_bare": sin2tw_bare,
        "alpha_1_mz": alpha_1_mz,
        "alpha_2_mz": alpha_2_mz,
        "alpha_3_mz": alpha_3_mz,
        "alpha_em": alpha_em,
        "inv_alpha_em": inv_alpha_em,
        "sin2tw_mz": sin2tw_mz,
        "err_sin2tw": err_sin2tw,
        "err_alpha_em": err_alpha_em,
        "err_combined": err_combined,
    }


# =============================================================================
# BEGIN
# =============================================================================

log("=" * 78)
log("U(1) HYPERCHARGE COUPLING FROM EDGE GEOMETRY")
log("The last missing piece for lattice-derived gauge couplings")
log("=" * 78)
log()
log("ESTABLISHED:")
log("  SU(3): g_3^2 = 1              alpha_3 = 1/(4*pi) = {:.8f}".format(ALPHA_S_BARE))
log("  SU(2): g_2^2 = 1/(d+1) = 1/4  alpha_2 = 1/(16*pi) = {:.8f}".format(ALPHA_2_BARE))
log()
log("TARGET (observation):")
log("  sin^2(theta_W)(M_Z) = {:.5f}".format(SIN2_TW_MZ))
log("  alpha_EM(M_Z)       = 1/{:.3f} = {:.8f}".format(1/ALPHA_EM_MZ, ALPHA_EM_MZ))
log()


# =============================================================================
# SECTION 1: CUBIC LATTICE EDGE GEOMETRY
# =============================================================================

log("=" * 78)
log("SECTION 1: CUBIC LATTICE EDGE GEOMETRY (d = {})".format(D))
log("=" * 78)
log()

# Catalog of edge graph properties
z = 2 * D                           # coordination number = 6
n_edges_per_vert = D                 # edge/vertex ratio = 3
n_plaq_per_vert = D * (D - 1) // 2  # plaquettes per vertex = 3
edges_per_plaq = 4                   # edges around a plaquette
plaq_per_edge = 2 * (D - 1)         # plaquettes sharing an edge = 4
z_edge = 2 * (z - 1)                # edge graph coordination = 10

# Line graph properties
# For a regular graph with coordination z, the line graph has:
#   z_line = 2(z - 1) = 10  (edge-to-edge adjacency)
#   Each edge has 2 endpoints, each endpoint has z-1 = 5 other edges
# The line graph eigenvalues relate to the original graph eigenvalues

# The edge Laplacian
# On the cubic lattice, the edge Laplacian L_e = B^T B where B is the
# incidence matrix. Its spectrum differs from the vertex Laplacian.
# For the infinite d-dimensional cubic lattice:
#   vertex Laplacian spectrum: [0, 4d] (bandwidth = 4d = 12)
#   edge Laplacian spectrum:   [0, 2(d+1)] = [0, 8] (bandwidth = 2(d+1))

edge_laplacian_bandwidth = 2 * (D + 1)   # = 8 for d=3
vertex_laplacian_bandwidth = 4 * D        # = 12 for d=3

log("  Vertex structure:")
log("    Coordination number z = 2d = {}".format(z))
log("    Vertex Laplacian bandwidth = 4d = {}".format(vertex_laplacian_bandwidth))
log()
log("  Edge structure:")
log("    Edge/vertex ratio = d = {}".format(n_edges_per_vert))
log("    Edge graph coordination z_edge = 2(z-1) = {}".format(z_edge))
log("    Edge Laplacian bandwidth = 2(d+1) = {}".format(edge_laplacian_bandwidth))
log()
log("  Plaquette structure:")
log("    Plaquettes per vertex = d(d-1)/2 = {}".format(n_plaq_per_vert))
log("    Edges per plaquette = {}".format(edges_per_plaq))
log("    Plaquettes per edge = 2(d-1) = {}".format(plaq_per_edge))
log()

# Key geometric ratios
ratios = {
    "d": D,
    "d+1": D + 1,
    "2d": 2 * D,
    "2d+1": 2 * D + 1,
    "d(d-1)/2": D * (D - 1) // 2,
    "d(d+1)/2": D * (D + 1) // 2,
    "2(d-1)": 2 * (D - 1),
    "2(d+1)": 2 * (D + 1),
    "z_edge": z_edge,
    "z_edge+1": z_edge + 1,
}

log("  Key integer quantities:")
for name, val in ratios.items():
    log("    {} = {}".format(name, val))
log()


# =============================================================================
# SECTION 2: REVERSE-ENGINEER THE REQUIRED g_Y^2
# =============================================================================

log("=" * 78)
log("SECTION 2: REQUIRED g_Y^2 FROM OBSERVATION")
log("=" * 78)
log()

# Run observed M_Z couplings UP to M_Planck to find required bare couplings
L_planck = np.log(M_PLANCK / M_Z)
L_top = np.log(M_TOP / M_Z)
L_planck_top = np.log(M_PLANCK / M_TOP)

# 1-loop: run M_Z -> M_top (5 flavors) -> M_Planck (6 flavors)
inv_a1_top = 1.0/ALPHA_1_MZ + B1_1LOOP * L_top / (2 * PI)
inv_a2_top = 1.0/ALPHA_2_MZ + B2_1LOOP * L_top / (2 * PI)

inv_a1_planck = inv_a1_top + B1_1LOOP_6F * L_planck_top / (2 * PI)
inv_a2_planck = inv_a2_top + B2_1LOOP_6F * L_planck_top / (2 * PI)

alpha_1_bare_obs = 1.0 / inv_a1_planck
alpha_2_bare_obs = 1.0 / inv_a2_planck
alpha_Y_bare_obs = (3.0 / 5.0) * alpha_1_bare_obs
g_Y_sq_obs = alpha_Y_bare_obs * 4 * PI
g_2_sq_obs = alpha_2_bare_obs * 4 * PI

sin2tw_bare_obs = g_Y_sq_obs / (g_Y_sq_obs + g_2_sq_obs)

log("  Running observed couplings M_Z -> M_Planck (1-loop + threshold):")
log()
log("  Required bare couplings for exact match:")
log("    alpha_1(bare) = {:.8f}   (GUT norm, 1/alpha = {:.2f})".format(
    alpha_1_bare_obs, 1/alpha_1_bare_obs))
log("    alpha_2(bare) = {:.8f}   (1/alpha = {:.2f})".format(
    alpha_2_bare_obs, 1/alpha_2_bare_obs))
log()
log("    g_2^2(bare,obs) = {:.6f}".format(g_2_sq_obs))
log("    g_2^2(lattice)  = {:.6f}  (1/(d+1) = 1/4)".format(G2_SQ))
log("    Discrepancy: {:.2f}%".format(abs(g_2_sq_obs - G2_SQ) / g_2_sq_obs * 100))
log()
log("    g_Y^2(bare,obs) = {:.6f}".format(g_Y_sq_obs))
log("    alpha_Y(bare)   = {:.8f}".format(alpha_Y_bare_obs))
log()
log("    sin^2(theta_W)(bare) = {:.6f}".format(sin2tw_bare_obs))
log()

# Cross-check: run back down
check_1loop = run_and_evaluate(g_Y_sq_obs, g_2_sq_obs, 1.0, use_2loop=False)
log("  Cross-check (run back to M_Z, 1-loop):")
log("    sin^2(theta_W) = {:.6f} (target {:.5f})".format(
    check_1loop["sin2tw_mz"], SIN2_TW_MZ))
log("    1/alpha_EM = {:.2f} (target {:.2f})".format(
    check_1loop["inv_alpha_em"], 1/ALPHA_EM_MZ))
log()

# Also find what the lattice g_2^2 = 1/4 requires for g_Y^2
log("  With g_2^2 = 1/4 FIXED, find g_Y^2 to match sin^2(theta_W)(M_Z):")
log()

def objective_gY(gY_sq_trial):
    """Residual for root-finding: sin^2(theta_W)(M_Z) - target."""
    r = run_and_evaluate(gY_sq_trial, G2_SQ, 1.0, use_2loop=False)
    return r["sin2tw_mz"] - SIN2_TW_MZ

try:
    g_Y_sq_exact = brentq(objective_gY, 0.01, 2.0, xtol=1e-12)
    r_exact = run_and_evaluate(g_Y_sq_exact, G2_SQ, 1.0, use_2loop=False)
    log("    g_Y^2(exact, 1-loop) = {:.10f}".format(g_Y_sq_exact))
    log("    sin^2(tW)(M_Z) = {:.8f}".format(r_exact["sin2tw_mz"]))
    log("    1/alpha_EM = {:.4f} (obs: {:.4f})".format(
        r_exact["inv_alpha_em"], 1/ALPHA_EM_MZ))
    log("    alpha_EM error = {:.2f}%".format(r_exact["err_alpha_em"]))
except ValueError:
    g_Y_sq_exact = g_Y_sq_obs
    log("    Root-finding failed; using reverse-engineered value.")
log()

# 2-loop version
log("  With g_2^2 = 1/4 FIXED, find g_Y^2 using 2-loop running:")

def objective_gY_2loop(gY_sq_trial):
    r = run_and_evaluate(gY_sq_trial, G2_SQ, 1.0, use_2loop=True)
    return r["sin2tw_mz"] - SIN2_TW_MZ

try:
    g_Y_sq_exact_2loop = brentq(objective_gY_2loop, 0.01, 2.0, xtol=1e-12)
    r_exact_2l = run_and_evaluate(g_Y_sq_exact_2loop, G2_SQ, 1.0, use_2loop=True)
    log("    g_Y^2(exact, 2-loop) = {:.10f}".format(g_Y_sq_exact_2loop))
    log("    sin^2(tW)(M_Z) = {:.8f}".format(r_exact_2l["sin2tw_mz"]))
    log("    1/alpha_EM = {:.4f} (obs: {:.4f})".format(
        r_exact_2l["inv_alpha_em"], 1/ALPHA_EM_MZ))
    log("    alpha_EM error = {:.2f}%".format(r_exact_2l["err_alpha_em"]))
except ValueError:
    g_Y_sq_exact_2loop = g_Y_sq_exact
    log("    2-loop root-finding failed; using 1-loop value.")
log()

log("  SUMMARY OF TARGETS:")
log("    g_Y^2 needed (1-loop): {:.8f}".format(g_Y_sq_exact))
log("    g_Y^2 needed (2-loop): {:.8f}".format(g_Y_sq_exact_2loop))
log("    sin^2(tW)(bare, 1-loop target): {:.6f}".format(
    g_Y_sq_exact / (g_Y_sq_exact + G2_SQ)))
log("    sin^2(tW)(bare, 2-loop target): {:.6f}".format(
    g_Y_sq_exact_2loop / (g_Y_sq_exact_2loop + G2_SQ)))
log()


# =============================================================================
# SECTION 3: SYSTEMATIC CANDIDATE ENUMERATION
# =============================================================================

log("=" * 78)
log("SECTION 3: SYSTEMATIC CANDIDATE ENUMERATION")
log("30+ geometric formulas for g_Y^2(d) evaluated at d = 3")
log("=" * 78)
log()

def make_candidates(d):
    """Generate candidate g_Y^2 formulas as functions of spatial dimension d.

    Returns OrderedDict of {name: (value, formula_string)}.
    """
    z = 2 * d
    z_e = 2 * (z - 1)
    candidates = OrderedDict()

    # --- Category A: Simple polynomial ratios ---
    candidates["A1: 1/(d+1)"] = (
        1.0 / (d + 1),
        "same as g_2^2, equal couplings"
    )
    candidates["A2: 1/(d+2)"] = (
        1.0 / (d + 2),
        "next integer denominator"
    )
    candidates["A3: d/(d+1)^2"] = (
        d / (d + 1)**2,
        "node-edge ratio normalized"
    )
    candidates["A4: d/(d+1)(d+2)"] = (
        d / ((d + 1) * (d + 2)),
        "SU(5)-like normalization"
    )
    candidates["A5: (d-1)/(d+1)^2"] = (
        (d - 1) / (d + 1)**2,
        "d-1 edges minus self"
    )
    candidates["A6: d/(2d+1)"] = (
        d / (2 * d + 1),
        "total spacetime directions"
    )
    candidates["A7: (2d-1)/(2d(d+1))"] = (
        (2 * d - 1) / (2 * d * (d + 1)),
        "edge neighbors normalized"
    )
    candidates["A8: 1/z = 1/(2d)"] = (
        1.0 / z,
        "inverse coordination"
    )
    candidates["A9: 2/z = 1/d"] = (
        2.0 / z,
        "per-direction coupling"
    )
    candidates["A10: d^2/(d+1)^3"] = (
        d**2 / (d + 1)**3,
        "quadratic edge factor"
    )

    # --- Category B: Edge graph specific ---
    candidates["B1: 1/(z_edge+1)"] = (
        1.0 / (z_e + 1),
        "bipartite-like on edge graph"
    )
    candidates["B2: z_edge/(z_edge+1)^2"] = (
        z_e / (z_e + 1)**2,
        "edge graph analog of A3"
    )
    candidates["B3: 1/z_edge"] = (
        1.0 / z_e,
        "inverse edge coordination"
    )
    candidates["B4: 2/z_edge"] = (
        2.0 / z_e,
        "per-endpoint on edge graph"
    )
    candidates["B5: (z-1)/z_edge"] = (
        (z - 1) / z_e,
        "vertex-edge ratio"
    )

    # --- Category C: Plaquette-based ---
    candidates["C1: 1/plaq_per_edge = 1/(2(d-1))"] = (
        1.0 / (2 * (d - 1)),
        "one plaquette per edge"
    )
    candidates["C2: 1/(d(d-1)/2)"] = (
        2.0 / (d * (d - 1)) if d > 1 else float('inf'),
        "inverse plaquettes per vertex"
    )
    candidates["C3: 2/(d(d-1))"] = (
        2.0 / (d * (d - 1)) if d > 1 else float('inf'),
        "same as C2"
    )
    candidates["C4: edges/plaquettes = 2d/(d(d-1)/2)"] = (
        4.0 / (d - 1) if d > 1 else float('inf'),
        "edge-to-plaquette ratio"
    )

    # --- Category D: Laplacian-based ---
    candidates["D1: 1/edge_Lap_bw = 1/(2(d+1))"] = (
        1.0 / (2 * (d + 1)),
        "inverse edge Laplacian bandwidth"
    )
    candidates["D2: edge_bw/vert_bw = (d+1)/(2d)"] = (
        (d + 1) / (2.0 * d),
        "bandwidth ratio edge/vertex"
    )
    candidates["D3: vert_bw/edge_bw^2"] = (
        4.0 * d / (2 * (d + 1))**2,
        "vertex bandwidth / edge bandwidth^2"
    )

    # --- Category E: Weinberg angle motivated ---
    # If sin^2(theta_W)(bare) = f(d), then g_Y^2 = g_2^2 * f/(1-f)
    # = (1/(d+1)) * f/(1-f)
    g2sq = 1.0 / (d + 1)

    candidates["E1: sin2tW = 3/8 (GUT)"] = (
        g2sq * (3.0 / 8.0) / (1.0 - 3.0 / 8.0),
        "GUT prediction at Planck"
    )
    candidates["E2: sin2tW = (d-1)/(d+1)"] = (
        g2sq * ((d - 1.0) / (d + 1.0)) / (1.0 - (d - 1.0) / (d + 1.0)),
        "dimension-dependent Weinberg"
    )
    candidates["E3: sin2tW = d/(2d+1)"] = (
        g2sq * (d / (2.0 * d + 1)) / (1.0 - d / (2.0 * d + 1)),
        "spacetime Weinberg"
    )
    candidates["E4: sin2tW = (d-1)/2d"] = (
        g2sq * ((d - 1.0) / (2.0 * d)) / (1.0 - (d - 1.0) / (2.0 * d)),
        "half-integer Weinberg"
    )
    candidates["E5: sin2tW = d/(d+2)"] = (
        g2sq * (d / (d + 2.0)) / (1.0 - d / (d + 2.0)),
        "d/(d+2) Weinberg"
    )
    candidates["E6: sin2tW = 1/2"] = (
        g2sq,
        "equal couplings -> sin2tW = 1/2"
    )
    candidates["E7: sin2tW = (d-1)/(2(d+1))"] = (
        g2sq * ((d - 1.0) / (2.0 * (d + 1))) / (1.0 - (d - 1.0) / (2.0 * (d + 1))),
        "half of E2"
    )
    candidates["E8: sin2tW = d^2/(d^2+d+1)"] = (
        g2sq * (d**2 / (d**2 + d + 1.0)) / (1.0 - d**2 / (d**2 + d + 1.0)),
        "quadratic Weinberg"
    )

    # --- Category F: GUT normalization factor variants ---
    # If the lattice gives g_1^2(GUT) = some formula, g_Y^2 = (3/5)*g_1^2
    candidates["F1: g1_GUT^2 = 1/(d+1), g_Y = (3/5)*g1"] = (
        (3.0 / 5.0) * g2sq,
        "GUT norm with equal g1=g2"
    )
    candidates["F2: g1_GUT^2 = 5/(3(d+1))"] = (
        (1.0 / (d + 1)),
        "same as A1 (GUT rescaled)"
    )

    return candidates


candidates_d3 = make_candidates(D)

log("  {:45s} {:>10s} {:>12s}".format("Candidate", "g_Y^2", "sin2tW(bare)"))
log("  " + "-" * 70)
for name, (val, desc) in candidates_d3.items():
    if val < float('inf') and val > 0:
        sin2tw_b = val / (val + G2_SQ)
        log("  {:45s} {:10.6f} {:12.6f}".format(name, val, sin2tw_b))
    else:
        log("  {:45s} {:>10s} {:>12s}".format(name, "inf", "N/A"))
log()


# =============================================================================
# SECTION 4: RUN ALL CANDIDATES TO M_Z (1-LOOP)
# =============================================================================

log("=" * 78)
log("SECTION 4: RUN ALL CANDIDATES TO M_Z (1-loop + threshold)")
log("=" * 78)
log()

scan_results_1loop = []

for name, (gY_sq, desc) in candidates_d3.items():
    if gY_sq <= 0 or gY_sq == float('inf') or gY_sq > 10:
        continue
    r = run_and_evaluate(gY_sq, G2_SQ, 1.0, use_2loop=False)
    r["name"] = name
    r["desc"] = desc
    scan_results_1loop.append(r)

scan_results_1loop.sort(key=lambda x: x["err_combined"])

log("  RANKING BY COMBINED ERROR (1-loop):")
log()
log("  {:4s} {:45s} {:>8s} {:>10s} {:>8s} {:>10s} {:>8s}".format(
    "Rank", "Candidate", "g_Y^2", "sin2tW(MZ)", "err(%)", "1/a_EM", "err(%)"))
log("  " + "-" * 100)

for i, r in enumerate(scan_results_1loop):
    log("  {:4d} {:45s} {:8.5f} {:10.5f} {:8.2f} {:10.2f} {:8.2f}".format(
        i + 1, r["name"], r["g_Y_sq"],
        r["sin2tw_mz"], r["err_sin2tw"],
        r["inv_alpha_em"], r["err_alpha_em"]))

log()
log("  Target: sin^2(tW) = {:.5f}, 1/alpha_EM = {:.3f}".format(
    SIN2_TW_MZ, 1/ALPHA_EM_MZ))
log("  Required: g_Y^2 = {:.8f}".format(g_Y_sq_exact))
log()


# =============================================================================
# SECTION 5: RUN ALL CANDIDATES TO M_Z (2-LOOP)
# =============================================================================

log("=" * 78)
log("SECTION 5: RUN ALL CANDIDATES TO M_Z (2-loop)")
log("=" * 78)
log()

scan_results_2loop = []

for name, (gY_sq, desc) in candidates_d3.items():
    if gY_sq <= 0 or gY_sq == float('inf') or gY_sq > 10:
        continue
    r = run_and_evaluate(gY_sq, G2_SQ, 1.0, use_2loop=True)
    r["name"] = name
    r["desc"] = desc
    scan_results_2loop.append(r)

scan_results_2loop.sort(key=lambda x: x["err_combined"])

log("  RANKING BY COMBINED ERROR (2-loop):")
log()
log("  {:4s} {:45s} {:>8s} {:>10s} {:>8s} {:>10s} {:>8s}".format(
    "Rank", "Candidate", "g_Y^2", "sin2tW(MZ)", "err(%)", "1/a_EM", "err(%)"))
log("  " + "-" * 100)

for i, r in enumerate(scan_results_2loop):
    log("  {:4d} {:45s} {:8.5f} {:10.5f} {:8.2f} {:10.2f} {:8.2f}".format(
        i + 1, r["name"], r["g_Y_sq"],
        r["sin2tw_mz"], r["err_sin2tw"],
        r["inv_alpha_em"], r["err_alpha_em"]))

log()
log("  Required: g_Y^2(2-loop) = {:.8f}".format(g_Y_sq_exact_2loop))
log()


# =============================================================================
# SECTION 6: DEEP DIVE ON TOP CANDIDATES
# =============================================================================

log("=" * 78)
log("SECTION 6: DEEP DIVE ON TOP 5 CANDIDATES")
log("=" * 78)
log()

for rank, r in enumerate(scan_results_2loop[:5]):
    log("  --- Candidate #{}: {} ---".format(rank + 1, r["name"]))
    log("  Description: {}".format(r["desc"]))
    log()
    log("  Bare coupling:")
    log("    g_Y^2 = {:.8f}".format(r["g_Y_sq"]))
    log("    g_2^2 = {:.8f}".format(r["g_2_sq"]))
    log("    sin^2(theta_W)(bare) = {:.6f}".format(r["sin2tw_bare"]))
    log()
    log("  At M_Z (2-loop):")
    log("    sin^2(theta_W) = {:.6f}  (obs: {:.5f}, err: {:.2f}%)".format(
        r["sin2tw_mz"], SIN2_TW_MZ, r["err_sin2tw"]))
    log("    1/alpha_EM     = {:.4f}  (obs: {:.3f}, err: {:.2f}%)".format(
        r["inv_alpha_em"], 1/ALPHA_EM_MZ, r["err_alpha_em"]))
    log("    alpha_2(M_Z)   = {:.6f}  (obs: {:.6f})".format(
        r["alpha_2_mz"], ALPHA_2_MZ))
    log()
    log("  Combined error: {:.2f}%".format(r["err_combined"]))
    log()


# =============================================================================
# SECTION 7: THE (d-1)/(d+1) HYPOTHESIS
# =============================================================================

log("=" * 78)
log("SECTION 7: SPECIAL ANALYSIS -- sin^2(theta_W)(bare) = (d-1)/(d+1)")
log("=" * 78)
log()

log("  This is the most elegant candidate:")
log("    sin^2(theta_W)(bare) = (d-1)/(d+1)")
log("    For d=3: (3-1)/(3+1) = 2/4 = 1/2")
log("    g_Y^2 = g_2^2 * sin2/(1-sin2) = (1/4) * (1/2)/(1/2) = 1/4 = g_2^2")
log("    => EQUAL COUPLINGS at the Planck scale!")
log()

g_Y_sq_e2 = G2_SQ  # equal couplings for d=3

r_e2_1loop = run_and_evaluate(g_Y_sq_e2, G2_SQ, 1.0, use_2loop=False)
r_e2_2loop = run_and_evaluate(g_Y_sq_e2, G2_SQ, 1.0, use_2loop=True)

log("  1-loop result:")
log("    sin^2(theta_W)(M_Z) = {:.6f}  (obs: {:.5f})".format(
    r_e2_1loop["sin2tw_mz"], SIN2_TW_MZ))
log("    1/alpha_EM(M_Z)     = {:.4f}  (obs: {:.3f})".format(
    r_e2_1loop["inv_alpha_em"], 1/ALPHA_EM_MZ))
log("    Errors: sin2tW = {:.2f}%, alpha_EM = {:.2f}%".format(
    r_e2_1loop["err_sin2tw"], r_e2_1loop["err_alpha_em"]))
log()

log("  2-loop result:")
log("    sin^2(theta_W)(M_Z) = {:.6f}  (obs: {:.5f})".format(
    r_e2_2loop["sin2tw_mz"], SIN2_TW_MZ))
log("    1/alpha_EM(M_Z)     = {:.4f}  (obs: {:.3f})".format(
    r_e2_2loop["inv_alpha_em"], 1/ALPHA_EM_MZ))
log("    Errors: sin2tW = {:.2f}%, alpha_EM = {:.2f}%".format(
    r_e2_2loop["err_sin2tw"], r_e2_2loop["err_alpha_em"]))
log()

# How much would 2-loop corrections need to shift sin2tW?
shift_needed = SIN2_TW_MZ - r_e2_2loop["sin2tw_mz"]
relative_shift = shift_needed / SIN2_TW_MZ * 100
log("  Shift needed from higher-order/threshold corrections:")
log("    Delta sin^2(tW) = {:.6f} ({:.2f}% of observed value)".format(
    shift_needed, relative_shift))
log()

# Physical interpretation
log("  PHYSICAL INTERPRETATION:")
log("    If sin^2(theta_W)(bare) = (d-1)/(d+1) = 1/2 in d=3,")
log("    then g_Y^2 = g_2^2 = 1/(d+1) at the lattice scale.")
log("    The U(1) and SU(2) start as EQUAL couplings, and the")
log("    Weinberg angle is entirely generated by RUNNING.")
log()
log("    This would mean ALL gauge couplings come from ONE formula:")
log("      g_3^2 = 1,  g_2^2 = g_Y^2 = 1/(d+1)")
log("    With d = 3 spatial dimensions as the ONLY input.")
log()


# =============================================================================
# SECTION 8: DIMENSIONAL CONSISTENCY CHECK
# =============================================================================

log("=" * 78)
log("SECTION 8: DIMENSIONAL CONSISTENCY")
log("Top candidates evaluated at d = 2, 3, 4, 5")
log("=" * 78)
log()

# For each d, compute g_2^2 = 1/(d+1) and try top candidates
top_formulas = [
    ("E2: sin2tW=(d-1)/(d+1)",
     lambda d: (1.0/(d+1)) * ((d-1.0)/(d+1.0)) / (1.0 - (d-1.0)/(d+1.0)),
     lambda d: (d-1.0)/(d+1.0)),
    ("E3: sin2tW=d/(2d+1)",
     lambda d: (1.0/(d+1)) * (d/(2.0*d+1)) / (1.0 - d/(2.0*d+1)),
     lambda d: d/(2.0*d+1)),
    ("E1: sin2tW=3/8 (GUT)",
     lambda d: (1.0/(d+1)) * (3.0/8.0) / (5.0/8.0),
     lambda d: 3.0/8.0),
    ("A1: g_Y^2=1/(d+1) (equal)",
     lambda d: 1.0/(d+1),
     lambda d: 0.5),
    ("F1: g_Y^2=(3/5)/(d+1)",
     lambda d: (3.0/5.0)/(d+1),
     lambda d: (3.0/5.0)/((3.0/5.0)+1.0)),
]

log("  {:35s} {:>6s} {:>10s} {:>10s} {:>10s} {:>10s}".format(
    "Formula", "d", "g_Y^2", "sin2(bare)", "sin2(MZ)", "err(%)"))
log("  " + "-" * 85)

for formula_name, gY_func, sin2_func in top_formulas:
    for d in [2, 3, 4, 5]:
        g2sq_d = 1.0 / (d + 1)
        gY_sq_d = gY_func(d)
        sin2_bare = gY_sq_d / (gY_sq_d + g2sq_d) if (gY_sq_d + g2sq_d) > 0 else 0

        # Only run to M_Z for d=3 (the physical dimension)
        if d == 3:
            r = run_and_evaluate(gY_sq_d, g2sq_d, 1.0, use_2loop=True)
            log("  {:35s} {:6d} {:10.6f} {:10.6f} {:10.6f} {:10.2f}".format(
                formula_name, d, gY_sq_d, sin2_bare,
                r["sin2tw_mz"], r["err_sin2tw"]))
        else:
            log("  {:35s} {:6d} {:10.6f} {:10.6f} {:>10s} {:>10s}".format(
                formula_name, d, gY_sq_d, sin2_bare, "N/A", "N/A"))
    log()

log("  NOTE: RG running only meaningful for d=3. Other dimensions shown")
log("  to check if the formula gives 'reasonable' bare-scale values.")
log()


# =============================================================================
# SECTION 9: THE GUT VALUE sin^2 = 3/8
# =============================================================================

log("=" * 78)
log("SECTION 9: COMPARISON WITH GUT VALUE sin^2(theta_W) = 3/8")
log("=" * 78)
log()

# The GUT value 3/8 at the unification scale is the standard prediction.
# Our framework has the lattice scale at M_Planck, not M_GUT ~ 10^16 GeV.
# Let's check what 3/8 at M_Planck gives.

g_Y_sq_gut = G2_SQ * (3.0 / 8.0) / (5.0 / 8.0)  # = 3/(5(d+1)) = 3/20

r_gut_1loop = run_and_evaluate(g_Y_sq_gut, G2_SQ, 1.0, use_2loop=False)
r_gut_2loop = run_and_evaluate(g_Y_sq_gut, G2_SQ, 1.0, use_2loop=True)

log("  GUT: sin^2(theta_W) = 3/8 = 0.375 at M_Planck")
log("  => g_Y^2 = (3/5) * g_2^2 = 3/(5*4) = 3/20 = {:.6f}".format(g_Y_sq_gut))
log()
log("  1-loop result at M_Z:")
log("    sin^2(theta_W) = {:.6f}  (obs: {:.5f}, err: {:.2f}%)".format(
    r_gut_1loop["sin2tw_mz"], SIN2_TW_MZ, r_gut_1loop["err_sin2tw"]))
log("    1/alpha_EM = {:.4f}  (obs: {:.3f}, err: {:.2f}%)".format(
    r_gut_1loop["inv_alpha_em"], 1/ALPHA_EM_MZ, r_gut_1loop["err_alpha_em"]))
log()
log("  2-loop result at M_Z:")
log("    sin^2(theta_W) = {:.6f}  (obs: {:.5f}, err: {:.2f}%)".format(
    r_gut_2loop["sin2tw_mz"], SIN2_TW_MZ, r_gut_2loop["err_sin2tw"]))
log("    1/alpha_EM = {:.4f}  (obs: {:.3f}, err: {:.2f}%)".format(
    r_gut_2loop["inv_alpha_em"], 1/ALPHA_EM_MZ, r_gut_2loop["err_alpha_em"]))
log()

# Compare: 3/8 at M_GUT vs 3/8 at M_Planck
# Standard GUT has M_GUT ~ 2e16 GeV
M_GUT = 2e16
r_gut_mgut_1loop = run_and_evaluate(g_Y_sq_gut, G2_SQ, 1.0,
                                    mu_uv=M_GUT, use_2loop=False)
r_gut_mgut_2loop = run_and_evaluate(g_Y_sq_gut, G2_SQ, 1.0,
                                    mu_uv=M_GUT, use_2loop=True)

log("  For comparison: sin^2 = 3/8 at M_GUT = {:.0e} GeV:".format(M_GUT))
log("    1-loop: sin^2(M_Z) = {:.6f}  (err: {:.2f}%)".format(
    r_gut_mgut_1loop["sin2tw_mz"], r_gut_mgut_1loop["err_sin2tw"]))
log("    2-loop: sin^2(M_Z) = {:.6f}  (err: {:.2f}%)".format(
    r_gut_mgut_2loop["sin2tw_mz"], r_gut_mgut_2loop["err_sin2tw"]))
log()


# =============================================================================
# SECTION 10: UV SCALE SENSITIVITY
# =============================================================================

log("=" * 78)
log("SECTION 10: UV SCALE SENSITIVITY")
log("How sensitive are the results to M_UV choice?")
log("=" * 78)
log()

# The lattice scale could be M_Planck or M_Planck_reduced or something else.
# Check the top candidate at different UV scales.

best_name = scan_results_2loop[0]["name"]
best_gY = scan_results_2loop[0]["g_Y_sq"]

uv_scales = [
    ("M_Planck (full)", M_PLANCK),
    ("M_Planck (reduced)", M_PLANCK_RED),
    ("10^18 GeV", 1e18),
    ("10^17 GeV", 1e17),
    ("M_GUT = 2e16 GeV", M_GUT),
]

log("  Testing best candidate: {} (g_Y^2 = {:.6f})".format(best_name, best_gY))
log()
log("  {:25s} {:>12s} {:>10s} {:>10s}".format(
    "UV scale", "sin2tW(MZ)", "1/a_EM", "err(%)"))
log("  " + "-" * 60)

for scale_name, mu_uv in uv_scales:
    r = run_and_evaluate(best_gY, G2_SQ, 1.0, mu_uv=mu_uv, use_2loop=True)
    log("  {:25s} {:12.6f} {:10.4f} {:10.2f}".format(
        scale_name, r["sin2tw_mz"], r["inv_alpha_em"], r["err_combined"]))

log()

# Also check the equal coupling hypothesis
log("  Testing equal couplings g_Y^2 = g_2^2 = 1/4:")
log()
log("  {:25s} {:>12s} {:>10s} {:>10s}".format(
    "UV scale", "sin2tW(MZ)", "1/a_EM", "err(%)"))
log("  " + "-" * 60)

for scale_name, mu_uv in uv_scales:
    r = run_and_evaluate(G2_SQ, G2_SQ, 1.0, mu_uv=mu_uv, use_2loop=True)
    log("  {:25s} {:12.6f} {:10.4f} {:10.2f}".format(
        scale_name, r["sin2tw_mz"], r["inv_alpha_em"], r["err_combined"]))

log()


# =============================================================================
# SECTION 11: PLAQUETTE-BASED SELF-CONSISTENT COUPLING
# =============================================================================

log("=" * 78)
log("SECTION 11: PLAQUETTE-BASED SELF-CONSISTENT U(1) COUPLING")
log("=" * 78)
log()

log("  On a d-dimensional cubic lattice with compact U(1):")
log("    Wilson action: S = beta * sum_P (1 - cos theta_P)")
log("    beta = 1/g^2 = inverse bare coupling squared")
log()
log("  Each link participates in 2(d-1) = {} plaquettes.".format(plaq_per_edge))
log("  The mean-field improved coupling satisfies:")
log("    g^2_MF = g^2_bare / <P>")
log("    <P> = 1 - g^2 / (4*d*(d-1))  (free U(1) approximation)")
log()

# Self-consistent equation: g^2 = g0^2 / (1 - g^2/(4*d*(d-1)))
# Let x = g^2, g0^2 = 1 (unit coupling):
# x = 1 / (1 - x/(4*d*(d-1)))
# x * (1 - x/(4*d*(d-1))) = 1
# x - x^2/(4*d*(d-1)) = 1
# x^2/(4*d*(d-1)) - x + 1 = 0
# Quadratic: a = 1/(4*d*(d-1)), b = -1, c = 1
# x = (1 +/- sqrt(1 - 4/(4*d*(d-1)))) * 4*d*(d-1)/2

a_coeff = 1.0 / (4 * D * (D - 1))
discriminant = 1.0 - 4 * a_coeff
if discriminant >= 0:
    g_sq_mf_plus = (1 + np.sqrt(discriminant)) / (2 * a_coeff)
    g_sq_mf_minus = (1 - np.sqrt(discriminant)) / (2 * a_coeff)
    log("  Self-consistent solutions for g0^2 = 1:")
    log("    g^2_MF(+) = {:.6f}".format(g_sq_mf_plus))
    log("    g^2_MF(-) = {:.6f}".format(g_sq_mf_minus))
    log()

    # The physical solution is the smaller one
    g_sq_mf = g_sq_mf_minus
    log("  Taking the perturbative branch: g^2_MF = {:.6f}".format(g_sq_mf))

    r_mf = run_and_evaluate(g_sq_mf, G2_SQ, 1.0, use_2loop=True)
    log("    sin^2(tW)(MZ) = {:.6f} (err {:.2f}%)".format(
        r_mf["sin2tw_mz"], r_mf["err_sin2tw"]))
    log("    1/alpha_EM    = {:.4f} (err {:.2f}%)".format(
        r_mf["inv_alpha_em"], r_mf["err_alpha_em"]))
else:
    log("  No real solution (discriminant < 0).")

log()


# =============================================================================
# SECTION 12: CONTINUOUS SCAN AROUND TARGET
# =============================================================================

log("=" * 78)
log("SECTION 12: CONTINUOUS SCAN -- g_Y^2 AROUND TARGET VALUE")
log("Which simple fraction is closest to the required g_Y^2?")
log("=" * 78)
log()

# Scan simple rational numbers p/q with small p, q
simple_fractions = []
for q in range(1, 31):
    for p in range(1, q + 1):
        if math.gcd(p, q) == 1:  # reduced fraction
            val = p / q
            if 0.05 < val < 1.5:
                simple_fractions.append((p, q, val))

# Sort by distance to target
simple_fractions.sort(key=lambda x: abs(x[2] - g_Y_sq_exact_2loop))

log("  Target g_Y^2 (2-loop) = {:.8f}".format(g_Y_sq_exact_2loop))
log()
log("  {:6s} {:>10s} {:>10s} {:>12s} {:>10s} {:>8s}".format(
    "p/q", "g_Y^2", "dist", "sin2tW(MZ)", "1/a_EM", "err(%)"))
log("  " + "-" * 60)

for p, q, val in simple_fractions[:20]:
    r = run_and_evaluate(val, G2_SQ, 1.0, use_2loop=True)
    dist = val - g_Y_sq_exact_2loop
    log("  {:2d}/{:<3d} {:10.6f} {:+10.6f} {:12.6f} {:10.4f} {:8.2f}".format(
        p, q, val, dist, r["sin2tw_mz"], r["inv_alpha_em"], r["err_combined"]))

log()

# Also check fractions with common lattice denominators
log("  Fractions with lattice-related denominators:")
log()
lattice_fracs = [
    ("1/4", 1, 4),
    ("1/5", 1, 5),
    ("3/16", 3, 16),
    ("5/24", 5, 24),
    ("7/30", 7, 30),
    ("3/13", 3, 13),
    ("5/21", 5, 21),
    ("2/9", 2, 9),
    ("3/14", 3, 14),
    ("4/17", 4, 17),
    ("5/22", 5, 22),
    ("1/3", 1, 3),
    ("2/7", 2, 7),
    ("3/10", 3, 10),
    ("4/15", 4, 15),
]

log("  {:8s} {:>10s} {:>10s} {:>12s} {:>10s} {:>8s}".format(
    "Frac", "g_Y^2", "dist", "sin2tW(MZ)", "1/a_EM", "err(%)"))
log("  " + "-" * 62)

for name, p, q in lattice_fracs:
    val = p / q
    r = run_and_evaluate(val, G2_SQ, 1.0, use_2loop=True)
    dist = val - g_Y_sq_exact_2loop
    log("  {:8s} {:10.6f} {:+10.6f} {:12.6f} {:10.4f} {:8.2f}".format(
        name, val, dist, r["sin2tw_mz"], r["inv_alpha_em"], r["err_combined"]))

log()


# =============================================================================
# SECTION 13: COMPLETE GAUGE COUPLING TRIAD SUMMARY
# =============================================================================

log("=" * 78)
log("SECTION 13: COMPLETE GAUGE COUPLING TRIAD")
log("=" * 78)
log()

# Identify the overall best candidate
best_2loop = scan_results_2loop[0]

log("  THE FRAMEWORK (d = {} spatial dimensions):".format(D))
log()
log("  SU(3): g_3^2 = 1               [Z_3 clock-shift algebra]")
log("         alpha_3(bare) = 1/(4*pi) = {:.8f}".format(ALPHA_S_BARE))
log()
log("  SU(2): g_2^2 = 1/(d+1) = 1/4   [Z_2 bipartite geometry]")
log("         alpha_2(bare) = 1/(16*pi) = {:.8f}".format(ALPHA_2_BARE))
log()
log("  U(1):  BEST CANDIDATE: {}".format(best_2loop["name"]))
log("         g_Y^2 = {:.8f}".format(best_2loop["g_Y_sq"]))
log("         sin^2(theta_W)(bare) = {:.6f}".format(best_2loop["sin2tw_bare"]))
log()

log("  PREDICTIONS AT M_Z (2-loop):")
log("    sin^2(theta_W) = {:.6f}  (obs: {:.5f}, err: {:.2f}%)".format(
    best_2loop["sin2tw_mz"], SIN2_TW_MZ, best_2loop["err_sin2tw"]))
log("    1/alpha_EM     = {:.4f}  (obs: {:.3f}, err: {:.2f}%)".format(
    best_2loop["inv_alpha_em"], 1/ALPHA_EM_MZ, best_2loop["err_alpha_em"]))
log()

# The equal coupling result
log("  EQUAL COUPLING HYPOTHESIS (g_Y^2 = g_2^2 = 1/(d+1)):")
log("    sin^2(theta_W)(bare) = 1/2")
log("    sin^2(theta_W)(M_Z, 2-loop) = {:.6f} (err: {:.2f}%)".format(
    r_e2_2loop["sin2tw_mz"], r_e2_2loop["err_sin2tw"]))
log("    1/alpha_EM(M_Z)              = {:.4f} (err: {:.2f}%)".format(
    r_e2_2loop["inv_alpha_em"], r_e2_2loop["err_alpha_em"]))
log()

# Required value for exact match
log("  EXACT MATCH REQUIRES:")
log("    g_Y^2 = {:.10f} (1-loop)".format(g_Y_sq_exact))
log("    g_Y^2 = {:.10f} (2-loop)".format(g_Y_sq_exact_2loop))
log()

# Check: is any simple formula within 2-loop uncertainty?
# Typical 2-loop vs 1-loop difference gives a sense of perturbative uncertainty
diff_1_2 = abs(g_Y_sq_exact - g_Y_sq_exact_2loop)
log("  Perturbative uncertainty estimate:")
log("    |g_Y^2(1-loop) - g_Y^2(2-loop)| = {:.8f}".format(diff_1_2))
log("    Relative: {:.2f}%".format(diff_1_2 / g_Y_sq_exact * 100))
log()

# Check which candidates fall within this uncertainty band of the 2-loop target
log("  Candidates within perturbative uncertainty of exact value:")
for r in scan_results_2loop:
    if abs(r["g_Y_sq"] - g_Y_sq_exact_2loop) < 2 * diff_1_2:
        log("    {} (g_Y^2 = {:.6f}, err: {:.2f}%)".format(
            r["name"], r["g_Y_sq"], r["err_combined"]))

log()


# =============================================================================
# SECTION 14: IMPLICATIONS AND NEXT STEPS
# =============================================================================

log("=" * 78)
log("SECTION 14: IMPLICATIONS AND NEXT STEPS")
log("=" * 78)
log()

log("  KEY FINDINGS:")
log()
log("  1. The required g_Y^2 at M_Planck for exact sin^2(tW)(M_Z) = 0.23122")
log("     is g_Y^2 = {:.6f} (2-loop), very close to {:.6f} (1-loop).".format(
    g_Y_sq_exact_2loop, g_Y_sq_exact))
log()
log("  2. The EQUAL COUPLING hypothesis g_Y^2 = g_2^2 = 1/4 gives:")
log("     sin^2(tW)(M_Z) = {:.6f} ({:.1f}% error)".format(
    r_e2_2loop["sin2tw_mz"], r_e2_2loop["err_sin2tw"]))
log("     This corresponds to sin^2(tW)(bare) = 1/2 = (d-1)/(d+1) for d=3.")
log()
log("  3. The GUT value 3/8 at M_Planck (not M_GUT) gives:")
log("     sin^2(tW)(M_Z) = {:.6f} ({:.1f}% error)".format(
    r_gut_2loop["sin2tw_mz"], r_gut_2loop["err_sin2tw"]))
log()
log("  4. The best discrete geometric candidate is:")
log("     {} with {:.2f}% combined error".format(
    best_2loop["name"], best_2loop["err_combined"]))
log()

log("  NEXT STEPS:")
log()
log("  a) If the equal coupling hypothesis is close but not exact:")
log("     - Investigate whether threshold corrections at M_top close the gap")
log("     - Check if 3-loop beta functions improve the match")
log("     - Consider non-perturbative lattice-to-continuum matching corrections")
log()
log("  b) For a rigorous lattice derivation of g_Y^2:")
log("     - Compute the edge Laplacian spectrum on finite cubic lattices")
log("     - Identify which spectral property determines the bare U(1) coupling")
log("     - Prove or disprove g_Y^2 = 1/(d+1) from the edge structure")
log()
log("  c) Phenomenological tests:")
log("     - With all three bare couplings fixed, predict M_W/M_Z ratio")
log("     - Run alpha_s to M_Z and compare (currently blocked by Landau pole)")
log("     - Compute proton decay rate if the lattice has GUT-like structure")
log()


# =============================================================================
# SAVE RESULTS
# =============================================================================

os.makedirs("logs", exist_ok=True)
with open(LOG_FILE, "w") as f:
    for line in results:
        f.write(line + "\n")

log()
log("=" * 78)
log("Results saved to {}".format(LOG_FILE))
log("=" * 78)
