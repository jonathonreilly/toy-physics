#!/usr/bin/env python3
"""
Alpha_EM from Independent Edge Couplings
=========================================

All previous attempts to derive alpha_EM from a single GUT coupling have FAILED.
The GUT approach assumes alpha_GUT = 1/(4*pi) at M_Planck for all three gauge
groups. But the lattice has THREE DISTINCT structures:

  - Z_3 coloring (SU(3)): vertex coloring -> clock-shift algebra -> g^2 = 1
  - Z_2 bipartite (SU(2)): even/odd sublattice -> Cl(3) -> hopping amplitude
  - Edge phases (U(1)): exp(i*q*A_ij) on edges -> edge graph geometry

These structures are DIFFERENT, and there is no reason their bare couplings
should be equal at the lattice scale.

THE NEW IDEA: derive each bare coupling INDEPENDENTLY from its lattice
structure, then run them down to M_Z using SM beta functions.

For SU(3): alpha_3(bare) = 1/(4*pi), already established.
For SU(2): alpha_2(bare) = TBD, from Cl(3) hopping on bipartite lattice.
For U(1):  alpha_1(bare) = TBD, from edge graph geometry of the cubic lattice.

This script scans multiple geometric hypotheses for the bare U(1) and SU(2)
couplings, runs each to M_Z, and identifies which combinations reproduce
the observed alpha_EM(M_Z) = 1/127.95 and sin^2(theta_W) = 0.2312.

Self-contained: numpy + scipy only.
PStack experiment: alpha-em-edge-coupling
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

LOG_FILE = "logs/" + time.strftime("%Y-%m-%d") + "-alpha_em_edge_coupling.txt"

results = []
def log(msg=""):
    results.append(msg)
    print(msg)


# =============================================================================
# PHYSICAL CONSTANTS (PDG 2024 / CODATA 2022)
# =============================================================================

PI = np.pi

# Electromagnetic
ALPHA_EM_OBS = 1.0 / 137.035999084    # CODATA 2022 (low energy)
ALPHA_EM_MZ  = 1.0 / 127.951          # at M_Z (PDG 2024)

# Strong coupling
ALPHA_S_MZ = 0.1179                    # PDG 2024

# Electroweak
SIN2_TW_MZ = 0.23122                  # sin^2(theta_W) at M_Z, MS-bar (PDG 2024)
M_Z = 91.1876                          # GeV
M_W = 80.3692                          # GeV

# Mass scales
M_PLANCK = 1.2209e19                   # GeV (full Planck mass)
M_PLANCK_RED = 2.435e18                # GeV (reduced)

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
log("ALPHA_EM FROM INDEPENDENT EDGE COUPLINGS")
log("Deriving each gauge coupling from its own lattice structure")
log("=" * 78)
log()
log("TARGET: alpha_EM(M_Z) = 1/{:.3f} = {:.8f}".format(1/ALPHA_EM_MZ, ALPHA_EM_MZ))
log("        sin^2(theta_W)(M_Z) = {:.5f}".format(SIN2_TW_MZ))
log("        alpha_s(M_Z) = {:.4f}".format(ALPHA_S_MZ))
log()
log("KNOWN:  alpha_3(bare) = 1/(4*pi) = {:.6f}  (Z_3 clock-shift algebra)".format(ALPHA_S_BARE))
log()


# =============================================================================
# SM COUPLING RUNNING INFRASTRUCTURE
# =============================================================================

# 1-loop beta coefficients for SM with N_f = 6 (above M_top)
# Convention: 1/alpha_i(mu) = 1/alpha_i(mu_0) + b_i/(2*pi) * ln(mu/mu_0)
# where b_i > 0 for asymptotic freedom
#
# Standard SM 1-loop coefficients (GUT normalization for U(1)):
#   b_1 = -41/10  (U(1)_Y, GUT normalized: grows at high energy)
#   b_2 = 19/6    (SU(2)_L: AF)
#   b_3 = 7       (SU(3)_c: AF, with 5 flavors below top)
#
# These are for N_f = 5 active flavors. Above M_top, b_3 = 23/3.
# For rough estimates from Planck to M_Z, we use effective values.

B_1_SM = -41.0 / 10.0   # U(1)_Y: coupling GROWS at high energy
B_2_SM = 19.0 / 6.0     # SU(2): asymptotic freedom
B_3_SM = 7.0            # SU(3): asymptotic freedom (5 flavors)

# Above M_top: b_3 = 7 - 2/3 = 23/3 for 6 flavors
B_3_SM_6F = 23.0 / 3.0

# SM couplings at M_Z (GUT normalization for U(1)_Y)
# alpha_Y = alpha_EM / cos^2(theta_W)
# alpha_1_GUT = (5/3) * alpha_Y
# alpha_2 = alpha_EM / sin^2(theta_W)
ALPHA_1_MZ = (5.0 / 3.0) * ALPHA_EM_MZ / (1.0 - SIN2_TW_MZ)  # GUT normalized
ALPHA_2_MZ = ALPHA_EM_MZ / SIN2_TW_MZ
ALPHA_3_MZ_VAL = ALPHA_S_MZ

log("=" * 78)
log("SM COUPLINGS AT M_Z (GUT NORMALIZATION)")
log("=" * 78)
log()
log("  alpha_1(M_Z) = {:.6f}  (1/alpha = {:.2f})  [GUT norm]".format(
    ALPHA_1_MZ, 1/ALPHA_1_MZ))
log("  alpha_2(M_Z) = {:.6f}  (1/alpha = {:.2f})".format(
    ALPHA_2_MZ, 1/ALPHA_2_MZ))
log("  alpha_3(M_Z) = {:.6f}  (1/alpha = {:.2f})".format(
    ALPHA_3_MZ_VAL, 1/ALPHA_3_MZ_VAL))
log()
log("  Relation: 1/alpha_EM = (5/3) * (1/alpha_1) + 1/alpha_2")
log("  (because alpha_Y = (3/5)*alpha_1, so 1/alpha_Y = (5/3)/alpha_1)")
log("  Check: (5/3)*{:.2f} + {:.2f} = {:.2f}  (should be {:.2f})".format(
    1/ALPHA_1_MZ, 1/ALPHA_2_MZ,
    (5.0/3.0) * (1/ALPHA_1_MZ) + 1/ALPHA_2_MZ,
    1.0/ALPHA_EM_MZ))
log()


# =============================================================================
# RUNNING MACHINERY
# =============================================================================

def run_coupling_1loop(alpha_high, b_coeff, mu_high, mu_low):
    """1-loop running from mu_high down to mu_low.

    Convention: d(1/alpha)/d(ln mu) = b/(2*pi)
    So: 1/alpha(mu_low) = 1/alpha(mu_high) - b/(2*pi) * ln(mu_high/mu_low)

    For AF couplings (b > 0): 1/alpha decreases going down -> alpha GROWS
    For U(1) (b < 0): 1/alpha increases going down -> alpha SHRINKS
    """
    L = np.log(mu_high / mu_low)
    inv_alpha = 1.0 / alpha_high - b_coeff * L / (2 * PI)
    if inv_alpha <= 0:
        return float('inf')
    return 1.0 / inv_alpha


def run_all_from_planck(alpha_1_bare, alpha_2_bare, alpha_3_bare,
                        mu_uv=M_PLANCK, mu_ir=M_Z):
    """Run three SM gauge couplings from UV scale to M_Z.

    Uses 1-loop SM beta functions. For a rough scan this is sufficient.
    The bare couplings are in GUT normalization for alpha_1.

    Returns dict with all derived quantities at M_Z.
    """
    # Simple 1-loop running from mu_uv to mu_ir
    # For more precision we could add 2-loop and threshold corrections
    # but 1-loop is sufficient for scanning geometric hypotheses.

    alpha_1 = run_coupling_1loop(alpha_1_bare, B_1_SM, mu_uv, mu_ir)
    alpha_2 = run_coupling_1loop(alpha_2_bare, B_2_SM, mu_uv, mu_ir)
    alpha_3 = run_coupling_1loop(alpha_3_bare, B_3_SM, mu_uv, mu_ir)

    # Reconstruct electroweak observables
    # alpha_Y = (3/5)*alpha_1, so 1/alpha_Y = (5/3)/alpha_1
    # alpha_EM^{-1} = 1/alpha_Y + 1/alpha_2 = (5/3)/alpha_1 + 1/alpha_2
    if alpha_1 < float('inf') and alpha_2 < float('inf'):
        inv_alpha_em = (5.0 / 3.0) / alpha_1 + 1.0 / alpha_2
        alpha_em = 1.0 / inv_alpha_em if inv_alpha_em > 0 else float('inf')
    else:
        alpha_em = 0.0
        inv_alpha_em = float('inf')

    # sin^2(theta_W) = (3/5)*alpha_1 / ((3/5)*alpha_1 + alpha_2)
    # = alpha_EM / alpha_2
    if alpha_2 > 0 and alpha_em > 0 and alpha_em < float('inf'):
        sin2tw = alpha_em / alpha_2
    else:
        sin2tw = 0.0

    return {
        "alpha_1": alpha_1,
        "alpha_2": alpha_2,
        "alpha_3": alpha_3,
        "alpha_em": alpha_em,
        "inv_alpha_em": inv_alpha_em,
        "sin2tw": sin2tw,
    }


def run_with_thresholds(alpha_1_bare, alpha_2_bare, alpha_3_bare,
                        mu_uv=M_PLANCK):
    """2-step running with top quark threshold for alpha_3.

    Runs from mu_uv to M_top with 6 flavors, then M_top to M_Z with 5.
    For U(1) and SU(2) the flavor thresholds have smaller effects but
    we include them for completeness.
    """
    # Beta coefficients with 6 flavors
    b1_6f = -(41.0 / 10.0) - (1.0 / 10.0)  # extra fermion doublet
    b2_6f = (19.0 / 6.0) - (1.0 / 6.0)
    b3_6f = B_3_SM_6F

    # Above M_top: 6 flavors
    a1_top = run_coupling_1loop(alpha_1_bare, b1_6f, mu_uv, M_TOP)
    a2_top = run_coupling_1loop(alpha_2_bare, b2_6f, mu_uv, M_TOP)
    a3_top = run_coupling_1loop(alpha_3_bare, b3_6f, mu_uv, M_TOP)

    # Below M_top: 5 flavors
    a1_mz = run_coupling_1loop(a1_top, B_1_SM, M_TOP, M_Z)
    a2_mz = run_coupling_1loop(a2_top, B_2_SM, M_TOP, M_Z)
    a3_mz = run_coupling_1loop(a3_top, B_3_SM, M_TOP, M_Z)

    if a1_mz < float('inf') and a2_mz < float('inf'):
        inv_alpha_em = (3.0 / 5.0) / a1_mz + 1.0 / a2_mz
        alpha_em = 1.0 / inv_alpha_em if inv_alpha_em > 0 else float('inf')
    else:
        alpha_em = 0.0
        inv_alpha_em = float('inf')

    if a2_mz > 0 and alpha_em > 0 and alpha_em < float('inf'):
        sin2tw = alpha_em / a2_mz
    else:
        sin2tw = 0.0

    return {
        "alpha_1": a1_mz,
        "alpha_2": a2_mz,
        "alpha_3": a3_mz,
        "alpha_em": alpha_em,
        "inv_alpha_em": inv_alpha_em,
        "sin2tw": sin2tw,
    }


# =============================================================================
# VERIFY: REPRODUCE OBSERVED COUPLINGS FROM M_Z VALUES
# =============================================================================

log("=" * 78)
log("VERIFICATION: RUN OBSERVED M_Z COUPLINGS TO M_PLANCK AND BACK")
log("=" * 78)
log()

# Run observed M_Z couplings UP to M_Planck
# d(1/alpha)/d(ln mu) = b/(2*pi), so going UP:
# 1/alpha(M_Pl) = 1/alpha(M_Z) + b * ln(M_Pl/M_Z) / (2*pi)
L_planck = np.log(M_PLANCK / M_Z)

inv_a1_planck = 1.0/ALPHA_1_MZ + B_1_SM * L_planck / (2 * PI)
inv_a2_planck = 1.0/ALPHA_2_MZ + B_2_SM * L_planck / (2 * PI)
inv_a3_planck = 1.0/ALPHA_3_MZ_VAL + B_3_SM * L_planck / (2 * PI)

log("  Running observed couplings M_Z -> M_Planck (1-loop):")
log("    1/alpha_1(M_Pl) = {:.2f}   alpha_1 = {:.6f}".format(
    inv_a1_planck, 1/inv_a1_planck))
log("    1/alpha_2(M_Pl) = {:.2f}   alpha_2 = {:.6f}".format(
    inv_a2_planck, 1/inv_a2_planck))
log("    1/alpha_3(M_Pl) = {:.2f}   alpha_3 = {:.6f}".format(
    inv_a3_planck, 1/inv_a3_planck))
log()
log("  NOTE: These do NOT converge to a single value (no SM unification).")
log("  This MOTIVATES independent bare couplings.")
log()
log("  For reference, the bare couplings IMPLIED by observation:")
log("    alpha_1(bare,obs) = {:.6f}  = 1/(4*pi*{:.4f})".format(
    1/inv_a1_planck, inv_a1_planck / (4*PI)))
log("    alpha_2(bare,obs) = {:.6f}  = 1/(4*pi*{:.4f})".format(
    1/inv_a2_planck, inv_a2_planck / (4*PI)))
log("    alpha_3(bare,obs) = {:.6f}  = 1/(4*pi*{:.4f})".format(
    1/inv_a3_planck, inv_a3_planck / (4*PI)))
log()

# Cross-check: run these back down
check = run_all_from_planck(1/inv_a1_planck, 1/inv_a2_planck, 1/inv_a3_planck)
log("  Cross-check (run back to M_Z):")
log("    1/alpha_EM = {:.2f}  (should be {:.2f})".format(
    check["inv_alpha_em"], 1/ALPHA_EM_MZ))
log("    sin^2(theta_W) = {:.5f}  (should be {:.5f})".format(
    check["sin2tw"], SIN2_TW_MZ))
log()

# Note on the SU(3) Landau pole issue
# alpha_3(bare) = 1/(4*pi) = 0.0796 at M_Planck.
# Running down with b_3 = 7 (AF): 1/alpha decreases.
# 1/alpha_3(mu) = 1/alpha_3(Planck) - b_3*ln(M_Planck/mu)/(2*pi)
# Landau pole when 1/alpha = 0:
# ln(M_Planck/mu_pole) = 2*pi / (b_3 * alpha_3(Planck))
# mu_pole = M_Planck * exp(-2*pi / (b_3 * 0.0796))
landau_exp = 2*PI / (B_3_SM * ALPHA_S_BARE)
mu_landau = M_PLANCK * np.exp(-landau_exp)
log("  IMPORTANT: SU(3) Landau pole analysis")
log("    alpha_3(bare) = 1/(4*pi) at M_Planck")
log("    Running down, 1/alpha_3 -> 0 at mu = {:.3e} GeV".format(mu_landau))
log("    This is ABOVE M_Z = {:.1f} GeV!".format(M_Z))
log("    => alpha_3(bare) = 1/(4*pi) does NOT survive running to M_Z")
log("    => The framework coupling 1/(4*pi) is NOT the perturbative bare")
log("       coupling at M_Planck. It may be a LATTICE coupling that requires")
log("       non-perturbative matching to the continuum MS-bar scheme.")
log()
log("  For the electroweak sector, we REVERSE-ENGINEER the bare couplings")
log("  that give the correct low-energy values, independent of whether")
log("  alpha_3 = 1/(4*pi) is the physical bare coupling or not.")
log()


# =============================================================================
# SECTION 1: LATTICE GEOMETRY OF THE CUBIC GRAPH
# =============================================================================

log("=" * 78)
log("SECTION 1: CUBIC LATTICE GEOMETRY")
log("=" * 78)
log()

# Cubic lattice in d=3:
# - Coordination number z = 2d = 6 (edges per vertex)
# - Edge-to-vertex ratio: #edges / #vertices = d = 3
# - Faces (plaquettes) per vertex: d*(d-1)/2 = 3
# - Each face has 4 edges
# - Each edge belongs to 2*(d-1) = 4 plaquettes
# - Dual lattice: also cubic (self-dual in this sense)
# - Edge graph: each edge connects to 2*(2d-2) = 2*4 = 8 other edges
#   (at each end, the edge meets 2d-1 = 5 other edges, but shares no end
#    with 1 of them -- actually: each end has z-1 = 5 neighbors)

d = 3
z = 2 * d  # coordination number = 6
n_plaq_per_vert = d * (d - 1) // 2  # = 3
edges_per_plaq = 4
plaq_per_edge = 2 * (d - 1)  # = 4

log("  Cubic lattice (d = {}):".format(d))
log("    Coordination number z = {}".format(z))
log("    Edge/vertex ratio = d = {}".format(d))
log("    Plaquettes per vertex = {}".format(n_plaq_per_vert))
log("    Edges per plaquette = {}".format(edges_per_plaq))
log("    Plaquettes per edge = {}".format(plaq_per_edge))
log()

# The edge graph has its own structure:
# Each edge in the d=3 cubic lattice has 2 endpoints.
# At each endpoint, there are z-1 = 5 other edges.
# But the same edge at the other end also has 5 neighbors.
# Total neighbors in edge graph = 2*(z-1) = 10, minus overcounting = ?
# Actually for the edge graph of a regular graph with coordination z:
# each edge is adjacent to 2*(z-1) edges (sharing at least one vertex).
# No overcounting since the graph is simple (no multi-edges).
z_edge = 2 * (z - 1)  # = 10 for cubic
log("    Edge graph coordination number = {}".format(z_edge))
log()


# =============================================================================
# SECTION 2: SU(3) BARE COUPLING (established)
# =============================================================================

log("=" * 78)
log("SECTION 2: SU(3) BARE COUPLING (Z_3 clock-shift algebra)")
log("=" * 78)
log()
log("  The Z_3 vertex coloring of the cubic lattice generates SU(3).")
log("  Unit hopping amplitude -> g^2 = 1 -> alpha_3 = g^2/(4*pi) = 1/(4*pi)")
log("  alpha_3(bare) = {:.8f}".format(1/(4*PI)))
log()


# =============================================================================
# SECTION 3: SU(2) BARE COUPLING HYPOTHESES
# =============================================================================

log("=" * 78)
log("SECTION 3: SU(2) BARE COUPLING HYPOTHESES")
log("=" * 78)
log()
log("  The Z_2 bipartite structure gives Cl(3) -> SU(2).")
log("  The hopping amplitude between even/odd sublattices determines g_2.")
log()

# Hypothesis A: Same as SU(3) -- unit hopping -> alpha_2 = 1/(4*pi)
# This is the simplest assumption.
alpha_2_hypotheses = {
    "A: same as SU(3), 1/(4*pi)": 1.0 / (4 * PI),
}

# Hypothesis B: Cl(3) normalization
# The Clifford algebra Cl(3) has 2^3 = 8 basis elements.
# The SU(2) subalgebra is generated by {e_1, e_2, e_3} (grade-1 elements).
# The hopping operator in the bipartite structure maps even -> odd.
# On a cubic lattice, the hop amplitude could include a 1/sqrt(z) factor
# for normalization, giving g_2^2 = 1/z = 1/6.
alpha_2_hypotheses["B: 1/(z * 4*pi) = 1/(24*pi)"] = 1.0 / (z * 4 * PI)

# Hypothesis C: The bipartite structure has 2 sublattices.
# Each sublattice is an FCC lattice (for cubic). The inter-sublattice
# hopping in d=3 involves z=6 links, but each link connects to only
# ONE neighbor, so the effective coupling per link is g_2^2/z.
# Total coupling: g_2^2 = z * (coupling per link).
# If coupling per link = 1/(4*pi*z), then g_2^2 = 1/(4*pi).
# This reduces to hypothesis A. Instead try: sqrt(2) factor from
# the two sublattices.
alpha_2_hypotheses["C: sqrt(2)/(4*pi)"] = np.sqrt(2) / (4 * PI)

# Hypothesis D: Cl(3) has dimension 8, SU(2) has dimension 3.
# Ratio 3/8 gives a natural factor.
alpha_2_hypotheses["D: (3/8)/(4*pi)"] = (3.0 / 8.0) / (4 * PI)

for name, val in alpha_2_hypotheses.items():
    log("  {}: alpha_2 = {:.8f} = 1/{:.4f}".format(name, val, 1/val))
log()


# =============================================================================
# SECTION 4: U(1) BARE COUPLING HYPOTHESES
# =============================================================================

log("=" * 78)
log("SECTION 4: U(1) BARE COUPLING HYPOTHESES (edge geometry)")
log("=" * 78)
log()
log("  U(1) gauge fields live on EDGES as phases exp(i*q*A_ij).")
log("  The edge structure differs from the vertex structure.")
log("  The bare U(1) coupling should reflect EDGE geometry.")
log()

# These are in GUT normalization: alpha_1_GUT = (5/3) * alpha_Y
# The factor of 5/3 comes from SU(5) embedding.
# Our lattice may or may not have this factor -- we scan both conventions.

# Raw geometric candidates for alpha_Y (hypercharge coupling):
alpha_Y_hypotheses = {}

# H1: Same as SU(3) -> alpha_Y = 1/(4*pi)
alpha_Y_hypotheses["H1: same, 1/(4*pi)"] = 1.0 / (4 * PI)

# H2: Edge normalization: 1/(z * 4*pi) = 1/(24*pi)
# Each vertex has z=6 edges; the coupling per edge is 1/z of vertex coupling
alpha_Y_hypotheses["H2: 1/(6 * 4*pi)"] = 1.0 / (6 * 4 * PI)

# H3: Dimension factor: 1/(d * 4*pi) = 1/(12*pi)
# d=3 edges emanate from each vertex in each direction pair
alpha_Y_hypotheses["H3: 1/(3 * 4*pi)"] = 1.0 / (3 * 4 * PI)

# H4: 1/(2*pi) -- edge has a factor of 2 (two endpoints)
alpha_Y_hypotheses["H4: 1/(2*pi)"] = 1.0 / (2 * PI)

# H5: From sin^2(theta_W) = 3/8 at GUT scale
# This is the SU(5) prediction. If it holds at the lattice scale:
# alpha_Y = alpha_2 * (3/8) / (1 - 3/8) = alpha_2 * (3/5)
# With alpha_2 = 1/(4*pi): alpha_Y = 3/(5*4*pi) = 3/(20*pi)
alpha_Y_hypotheses["H5: SU(5) ratio, 3/(20*pi)"] = 3.0 / (20 * PI)

# H6: Plaquette structure: compact U(1) on cubic lattice
# Wilson action: S = beta * sum_P (1 - cos theta_P)
# beta = 1/g^2. On cubic lattice, each plaquette has 4 edges.
# Standard compact U(1): beta = 1/e^2 where e is the bare charge.
# Critical coupling for confinement-deconfinement: beta_c ~ 1.01
# Just above the transition: g^2 ~ 1/1.01 ~ 0.99 -> alpha ~ 1/(4*pi)
# This is close to H1. Instead use the self-dual point:
# beta_sd = 1 -> g^2 = 1 -> alpha = 1/(4*pi). Same as H1.
# Try beta = d = 3 (one per dimension):
alpha_Y_hypotheses["H6: beta=d, 1/(3*4*pi)"] = 1.0 / (3 * 4 * PI)  # same as H3

# H7: Edge graph coordination
# The edge graph has z_edge = 10. Use 1/(z_edge * 4*pi)
alpha_Y_hypotheses["H7: 1/(z_edge * 4*pi) = 1/(40*pi)"] = 1.0 / (z_edge * 4 * PI)

# H8: Ratio of vertex to edge counting
# #edges/#vertices = d = 3 in the cubic lattice.
# alpha_Y = 1/(4*pi) * 1/d = 1/(12*pi). Same as H3.

# H9: Factor from U(1) vs SU(N) normalization
# In SU(N), Tr(T^a T^b) = delta_{ab}/2. For U(1), the generator is
# the identity with normalization 1. The ratio is 1/(2*T_F) = 1.
# But for the hypercharge embedding, Y = diag(1/3, 1/3, ...) etc.
# The canonical normalization gives Tr(Y^2) = 5/3 for one generation.
# alpha_Y = alpha_bare / (5/3) perhaps?
alpha_Y_hypotheses["H9: 3/(5*4*pi) = 3/(20*pi)"] = 3.0 / (20 * PI)  # same as H5

# H10: Pure edge counting in d=3.
# There are d=3 edge directions. Each direction is independent.
# The U(1) field on each edge is one degree of freedom.
# The bare coupling per direction: alpha_Y = 1/(4*pi*d^2) (power counting)
alpha_Y_hypotheses["H10: 1/(d^2 * 4*pi) = 1/(36*pi)"] = 1.0 / (9 * 4 * PI)

# H11: Empirical reverse-engineering
# What alpha_Y(bare) is needed to get alpha_EM(M_Z) = 1/127.95?
# We'll solve for this below.

# Remove duplicates by value
unique_hypotheses = {}
for name, val in alpha_Y_hypotheses.items():
    key = round(val, 10)
    if key not in unique_hypotheses:
        unique_hypotheses[key] = (name, val)
    else:
        existing_name = unique_hypotheses[key][0]
        unique_hypotheses[key] = (existing_name + " = " + name, val)

alpha_Y_hypotheses_unique = {v[0]: v[1] for v in unique_hypotheses.values()}

for name, val in sorted(alpha_Y_hypotheses_unique.items(), key=lambda x: -x[1]):
    log("  {}: alpha_Y = {:.8f} = 1/{:.4f}".format(name, val, 1/val))
log()


# =============================================================================
# SECTION 5: SCAN ALL COMBINATIONS
# =============================================================================

log("=" * 78)
log("SECTION 5: SCAN -- INDEPENDENT BARE COUPLINGS -> alpha_EM(M_Z)")
log("=" * 78)
log()

log("  For each (alpha_2_bare, alpha_Y_bare) hypothesis:")
log("    - Convert alpha_Y to GUT-normalized alpha_1 = (5/3)*alpha_Y")
log("    - Set alpha_3_bare = 1/(4*pi)")
log("    - Run to M_Z with 1-loop SM beta functions")
log("    - Compute alpha_EM(M_Z), sin^2(theta_W), alpha_s(M_Z)")
log()

scan_results = []

for su2_name, alpha_2_bare in sorted(alpha_2_hypotheses.items()):
    for u1_name, alpha_Y_bare in sorted(alpha_Y_hypotheses_unique.items(), key=lambda x: -x[1]):

        # GUT normalization
        alpha_1_bare = (5.0 / 3.0) * alpha_Y_bare

        alpha_3_bare = ALPHA_S_BARE

        # Run to M_Z
        result = run_all_from_planck(alpha_1_bare, alpha_2_bare, alpha_3_bare)

        err_em = abs(result["inv_alpha_em"] - 1/ALPHA_EM_MZ) / (1/ALPHA_EM_MZ) * 100
        err_s = abs(result["alpha_3"] - ALPHA_S_MZ) / ALPHA_S_MZ * 100
        err_tw = abs(result["sin2tw"] - SIN2_TW_MZ) / SIN2_TW_MZ * 100

        scan_results.append({
            "su2_name": su2_name,
            "u1_name": u1_name,
            "alpha_2_bare": alpha_2_bare,
            "alpha_Y_bare": alpha_Y_bare,
            "alpha_1_bare": alpha_1_bare,
            "result": result,
            "err_em": err_em,
            "err_s": err_s,
            "err_tw": err_tw,
        })

# Sort by alpha_EM error
scan_results.sort(key=lambda x: x["err_em"])

log("  {:60s} | 1/a_EM  | sin2tW  | a_s     | err_EM% | err_tW%".format(
    "Hypothesis"))
log("  " + "-" * 60 + "-+---------+---------+---------+---------+--------")

for r in scan_results:
    label = "SU2:{} / U1:{}".format(
        r["su2_name"][:20], r["u1_name"][:30])
    log("  {:60s} | {:7.2f} | {:7.5f} | {:7.4f} | {:6.1f}% | {:5.1f}%".format(
        label,
        r["result"]["inv_alpha_em"],
        r["result"]["sin2tw"],
        r["result"]["alpha_3"],
        r["err_em"],
        r["err_tw"],
    ))

log()
log("  Best match for alpha_EM(M_Z):")
best = scan_results[0]
log("    SU(2): {}".format(best["su2_name"]))
log("    U(1):  {}".format(best["u1_name"]))
log("    alpha_2(bare) = {:.8f}".format(best["alpha_2_bare"]))
log("    alpha_Y(bare) = {:.8f}".format(best["alpha_Y_bare"]))
log("    alpha_1(bare) = {:.8f}  [GUT norm]".format(best["alpha_1_bare"]))
log()
log("    Predicted at M_Z:")
log("      1/alpha_EM = {:.3f}  (observed: {:.3f})  error: {:.2f}%".format(
    best["result"]["inv_alpha_em"], 1/ALPHA_EM_MZ, best["err_em"]))
log("      sin^2(tW)  = {:.5f}  (observed: {:.5f})  error: {:.2f}%".format(
    best["result"]["sin2tw"], SIN2_TW_MZ, best["err_tw"]))
log("      alpha_s    = {:.4f}  (observed: {:.4f})  error: {:.2f}%".format(
    best["result"]["alpha_3"], ALPHA_S_MZ, best["err_s"]))
log()


# =============================================================================
# SECTION 6: REVERSE ENGINEERING -- WHAT BARE alpha_Y IS NEEDED?
# =============================================================================

log("=" * 78)
log("SECTION 6: REVERSE ENGINEERING")
log("What bare alpha_Y is needed to match alpha_EM(M_Z) = 1/127.95?")
log("=" * 78)
log()

for su2_name, alpha_2_bare in sorted(alpha_2_hypotheses.items()):

    log("  --- SU(2) hypothesis: {} ---".format(su2_name))

    def target_fn(log_alpha_Y):
        """Find alpha_Y that gives correct alpha_EM at M_Z."""
        alpha_Y = np.exp(log_alpha_Y)
        alpha_1 = (5.0 / 3.0) * alpha_Y
        result = run_all_from_planck(alpha_1, alpha_2_bare, ALPHA_S_BARE)
        return result["inv_alpha_em"] - 1.0 / ALPHA_EM_MZ

    # Scan for bracket
    try:
        alpha_Y_needed = np.exp(brentq(target_fn, np.log(1e-6), np.log(10.0)))

        log("    alpha_Y(bare) needed   = {:.8f} = 1/{:.4f}".format(
            alpha_Y_needed, 1/alpha_Y_needed))
        log("    alpha_1_GUT(bare)      = {:.8f} = 1/{:.4f}".format(
            (5.0/3.0)*alpha_Y_needed, 1/((5.0/3.0)*alpha_Y_needed)))

        # Check what geometric factor this corresponds to
        ratio_to_su3 = alpha_Y_needed / ALPHA_S_BARE
        log("    alpha_Y / alpha_3      = {:.6f}".format(ratio_to_su3))
        log("    alpha_Y * (4*pi)       = {:.6f}  (= g_Y^2)".format(
            alpha_Y_needed * 4 * PI))

        # Verify
        alpha_1_needed = (5.0 / 3.0) * alpha_Y_needed
        verify = run_all_from_planck(alpha_1_needed, alpha_2_bare, ALPHA_S_BARE)
        log("    Verification:")
        log("      1/alpha_EM(M_Z) = {:.3f}  (target: {:.3f})".format(
            verify["inv_alpha_em"], 1/ALPHA_EM_MZ))
        log("      sin^2(theta_W)  = {:.5f}  (observed: {:.5f})".format(
            verify["sin2tw"], SIN2_TW_MZ))
        log("      alpha_s(M_Z)    = {:.4f}  (observed: {:.4f})".format(
            verify["alpha_3"], ALPHA_S_MZ))

        # Check if sin^2(theta_W) at bare scale is a nice number
        sin2tw_bare = (3.0/5.0) * alpha_1_needed / (
            (3.0/5.0) * alpha_1_needed + alpha_2_bare)
        log("    sin^2(theta_W) at bare = {:.6f}".format(sin2tw_bare))

        # Check common fractions
        nice_fracs = [
            (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 8),
            (2, 3), (2, 5), (3, 4), (3, 5), (3, 8), (5, 8),
            (1, 7), (2, 7), (3, 7),
        ]
        log("    Looking for simple fraction matches:")
        for p, q in nice_fracs:
            frac = p / q
            if abs(sin2tw_bare - frac) / frac < 0.05:
                log("      sin^2(tW,bare) ~ {}/{} = {:.6f}  (err {:.2f}%)".format(
                    p, q, frac, abs(sin2tw_bare - frac)/frac*100))
            if abs(ratio_to_su3 - frac) / max(frac, 1e-10) < 0.05:
                log("      alpha_Y/alpha_3 ~ {}/{} = {:.6f}  (err {:.2f}%)".format(
                    p, q, frac, abs(ratio_to_su3 - frac)/frac*100))

    except ValueError:
        log("    Could not find solution (no root in search range)")

    log()


# =============================================================================
# SECTION 7: WEINBERG ANGLE FROM INDEPENDENT COUPLINGS
# =============================================================================

log("=" * 78)
log("SECTION 7: WEINBERG ANGLE AT BARE (LATTICE) SCALE")
log("=" * 78)
log()
log("  If the three gauge groups have independent bare couplings, the")
log("  Weinberg angle at the lattice scale is NOT 3/8 (the SU(5) value).")
log("  Instead:")
log("    sin^2(theta_W) = g'^2 / (g^2 + g'^2)")
log("  where g' is the hypercharge coupling and g is the SU(2) coupling.")
log()

# With GUT normalization:
# sin^2(theta_W) = (3/5)*alpha_1 / ((3/5)*alpha_1 + alpha_2)
# The SU(5) value 3/8 comes from alpha_1 = alpha_2 and the 3/5 factor:
# sin^2 = (3/5) / (3/5 + 1) = 3/8
log("  SU(5) prediction (alpha_1 = alpha_2): sin^2(tW) = 3/8 = {:.6f}".format(3/8))
log()

# What happens with different alpha_1?
log("  sin^2(theta_W) at bare scale for various alpha_Y/alpha_2 ratios:")
log()
ratios = [0.1, 0.2, 0.3, 0.5, 0.6, 0.8, 1.0, 1.5, 2.0, 3.0, 5.0]
for r in ratios:
    # alpha_Y = r * alpha_2_bare
    # alpha_1_GUT = (5/3) * alpha_Y = (5/3)*r*alpha_2
    # sin^2 = (3/5)*alpha_1 / ((3/5)*alpha_1 + alpha_2)
    #       = (3/5)*(5/3)*r / ((3/5)*(5/3)*r + 1)
    #       = r / (r + 1)
    sin2 = r / (r + 1)
    log("    alpha_Y/alpha_2 = {:.1f}  ->  sin^2(tW,bare) = {:.6f}".format(r, sin2))
log()
log("  Note: sin^2(tW,bare) = alpha_Y / (alpha_Y + alpha_2)")
log("  This is independent of the 5/3 GUT normalization factor!")
log()


# =============================================================================
# SECTION 8: WITHOUT GUT NORMALIZATION
# =============================================================================

log("=" * 78)
log("SECTION 8: RUNNING WITHOUT GUT NORMALIZATION")
log("=" * 78)
log()
log("  The (5/3) factor in alpha_1_GUT comes from SU(5) embedding.")
log("  If the lattice does NOT have SU(5) structure, this factor may")
log("  not apply. We scan with RAW hypercharge coupling (no 5/3).")
log()

# Redefine: alpha_1 = alpha_Y (no GUT normalization)
# Then 1/alpha_EM = 1/alpha_Y + 1/alpha_2
# (this is the tree-level relation without the 3/5 factor)
# But the beta function changes: b_1_raw = (3/5) * b_1_GUT = (3/5)*(-41/10) = -41*3/50

# Actually, the beta function for the PHYSICAL hypercharge coupling is:
# b_Y = -(41/6) * (1/(16*pi^2)) ... wait, let's be careful.
#
# In terms of alpha_Y (not GUT normalized):
# d(1/alpha_Y)/d(ln mu) = -b_Y/(2*pi)
# where b_Y = -(3/5)*b_1_GUT_in_our_convention = -(3/5)*(-41/10) = 41*3/50
# Wait, let me re-derive.
#
# The standard SM 1-loop result (Langacker convention):
# d(1/alpha_i)/d(ln mu) = b_i / (2*pi)
#
# For GUT normalized alpha_1: b_1 = -41/10 (our convention above, with negative
# meaning NOT AF). Running: 1/alpha_1(mu) = 1/alpha_1(M_Z) + b_1*ln(mu/M_Z)/(2*pi)
#
# Since alpha_1_GUT = (5/3)*alpha_Y, we have 1/alpha_Y = (5/3)/alpha_1_GUT
# d(1/alpha_Y)/d(ln mu) = (5/3) * d(1/alpha_1)/d(ln mu) = (5/3)*b_1/(2*pi)
# Wait that's not right either. If alpha_1 = (5/3)*alpha_Y then
# 1/alpha_1 = (3/5)/alpha_Y, so d(1/alpha_1)/d(ln mu) = (3/5)*d(1/alpha_Y)/d(ln mu)
# => d(1/alpha_Y)/d(ln mu) = (5/3)*b_1/(2*pi) = (5/3)*(-41/10)/(2*pi) = -41/(6*2*pi)
#
# So b_Y_raw = (5/3)*(-41/10) = -41/6 in our convention.
# Hmm, but that changes the running significantly.
#
# Actually, the standard result is that the SM hypercharge coupling runs with:
# b_Y = -41/6 when defined as d(1/alpha_Y)/d(ln mu) = b_Y/(2*pi)
# And the GUT normalization absorbs the 5/3 into the definition of alpha_1.

B_Y_RAW = (5.0 / 3.0) * B_1_SM  # = (5/3)*(-41/10) = -41/6

log("  Beta coefficient for raw alpha_Y: b_Y = {:.4f}".format(B_Y_RAW))
log("  (vs GUT-normalized b_1 = {:.4f})".format(B_1_SM))
log()

def run_raw_from_planck(alpha_Y_bare, alpha_2_bare, alpha_3_bare,
                        mu_uv=M_PLANCK, mu_ir=M_Z):
    """Run with raw (non-GUT-normalized) hypercharge coupling."""
    alpha_Y = run_coupling_1loop(alpha_Y_bare, B_Y_RAW, mu_uv, mu_ir)
    alpha_2 = run_coupling_1loop(alpha_2_bare, B_2_SM, mu_uv, mu_ir)
    alpha_3 = run_coupling_1loop(alpha_3_bare, B_3_SM, mu_uv, mu_ir)

    # Without GUT normalization: 1/alpha_EM = 1/alpha_Y + 1/alpha_2
    # (the standard relation alpha_EM = alpha_2 * sin^2(tW) = alpha_Y * cos^2(tW))
    # Wait -- that's not right either. The relation is:
    # e = g * sin(tW) = g' * cos(tW)
    # alpha_EM = alpha_2 * sin^2(tW) = alpha_Y * cos^2(tW)
    # 1/alpha_EM = 1/alpha_Y + 1/alpha_2  (this IS correct, it's e^{-2} = g^{-2} + g'^{-2})

    if alpha_Y < float('inf') and alpha_2 < float('inf'):
        inv_alpha_em = 1.0 / alpha_Y + 1.0 / alpha_2
        alpha_em = 1.0 / inv_alpha_em
    else:
        alpha_em = 0.0
        inv_alpha_em = float('inf')

    if alpha_2 > 0:
        sin2tw = alpha_em / alpha_2
    else:
        sin2tw = 0.0

    return {
        "alpha_Y": alpha_Y,
        "alpha_2": alpha_2,
        "alpha_3": alpha_3,
        "alpha_em": alpha_em,
        "inv_alpha_em": inv_alpha_em,
        "sin2tw": sin2tw,
    }

# Verify: observed values should round-trip
alpha_Y_mz_obs = ALPHA_EM_MZ / (1.0 - SIN2_TW_MZ)  # raw hypercharge at M_Z
log("  alpha_Y(M_Z) obs (raw) = {:.6f} = 1/{:.2f}".format(
    alpha_Y_mz_obs, 1/alpha_Y_mz_obs))
log("  Check: 1/alpha_Y + 1/alpha_2 = {:.2f}  (should be {:.2f})".format(
    1/alpha_Y_mz_obs + 1/ALPHA_2_MZ, 1/ALPHA_EM_MZ))
log()

# Scan with raw normalization
log("  Scanning with RAW hypercharge (no 5/3 GUT factor):")
log()

raw_scan = []

for su2_name, alpha_2_bare in sorted(alpha_2_hypotheses.items()):
    for u1_name, alpha_Y_bare in sorted(alpha_Y_hypotheses_unique.items(), key=lambda x: -x[1]):

        result = run_raw_from_planck(alpha_Y_bare, alpha_2_bare, ALPHA_S_BARE)

        err_em = abs(result["inv_alpha_em"] - 1/ALPHA_EM_MZ) / (1/ALPHA_EM_MZ) * 100
        err_tw = abs(result["sin2tw"] - SIN2_TW_MZ) / SIN2_TW_MZ * 100

        raw_scan.append({
            "su2_name": su2_name,
            "u1_name": u1_name,
            "alpha_2_bare": alpha_2_bare,
            "alpha_Y_bare": alpha_Y_bare,
            "result": result,
            "err_em": err_em,
            "err_tw": err_tw,
        })

raw_scan.sort(key=lambda x: x["err_em"])

log("  {:60s} | 1/a_EM  | sin2tW  | err_EM%".format("Hypothesis"))
log("  " + "-" * 60 + "-+---------+---------+--------")

for r in raw_scan[:15]:  # top 15
    label = "SU2:{} / U1:{}".format(
        r["su2_name"][:20], r["u1_name"][:30])
    log("  {:60s} | {:7.2f} | {:7.5f} | {:6.1f}%".format(
        label,
        r["result"]["inv_alpha_em"],
        r["result"]["sin2tw"],
        r["err_em"],
    ))

log()

# Reverse-engineer raw alpha_Y needed
log("  Reverse-engineering raw alpha_Y(bare) for each SU(2) hypothesis:")
log()

for su2_name, alpha_2_bare in sorted(alpha_2_hypotheses.items()):

    log("  --- {} ---".format(su2_name))

    def target_fn_raw(log_alpha_Y):
        alpha_Y = np.exp(log_alpha_Y)
        result = run_raw_from_planck(alpha_Y, alpha_2_bare, ALPHA_S_BARE)
        return result["inv_alpha_em"] - 1.0 / ALPHA_EM_MZ

    try:
        alpha_Y_needed = np.exp(brentq(target_fn_raw, np.log(1e-6), np.log(10.0)))

        log("    alpha_Y(bare) needed = {:.8f} = 1/{:.4f}".format(
            alpha_Y_needed, 1/alpha_Y_needed))
        log("    g_Y^2 = 4*pi*alpha_Y = {:.6f}".format(4*PI*alpha_Y_needed))

        ratio = alpha_Y_needed / ALPHA_S_BARE
        log("    alpha_Y / alpha_3    = {:.6f}".format(ratio))

        # Check sin^2(tW) at bare scale
        sin2_bare = alpha_Y_needed / (alpha_Y_needed + alpha_2_bare)
        log("    sin^2(tW) at bare    = {:.6f}".format(sin2_bare))

        # Verify
        verify = run_raw_from_planck(alpha_Y_needed, alpha_2_bare, ALPHA_S_BARE)
        log("    Verification: 1/alpha_EM = {:.3f}  sin^2(tW) = {:.5f}".format(
            verify["inv_alpha_em"], verify["sin2tw"]))

        # Check fractions
        for p, q in [(1,2),(1,3),(1,4),(1,5),(1,6),(2,3),(2,5),(3,4),(3,5),
                      (3,8),(5,8),(1,8),(2,7),(3,7),(4,7),(5,12),(7,12),
                      (1,9),(2,9),(4,9),(5,9),(7,9),(8,9)]:
            frac = p/q
            if abs(sin2_bare - frac)/frac < 0.03:
                log("    ** sin^2(tW,bare) ~ {}/{} = {:.6f}  (err {:.2f}%)".format(
                    p, q, frac, abs(sin2_bare-frac)/frac*100))
            if abs(ratio - frac)/max(frac,1e-10) < 0.03:
                log("    ** alpha_Y/alpha_3 ~ {}/{} = {:.6f}  (err {:.2f}%)".format(
                    p, q, frac, abs(ratio-frac)/frac*100))

        # Check against multiples of pi, 1/pi, etc
        for desc, val in [("1/pi", 1/PI), ("2/pi", 2/PI), ("pi/6", PI/6),
                          ("1/e", 1/np.e), ("1/sqrt(2*pi)", 1/np.sqrt(2*PI)),
                          ("1/(2*pi)", 1/(2*PI)), ("3/(4*pi)", 3/(4*PI))]:
            if abs(ratio - val)/val < 0.05:
                log("    ** alpha_Y/alpha_3 ~ {} = {:.6f}  (err {:.2f}%)".format(
                    desc, val, abs(ratio-val)/val*100))

    except ValueError:
        log("    Could not find solution")

    log()


# =============================================================================
# SECTION 9: FINE SCAN AROUND BEST CANDIDATES
# =============================================================================

log("=" * 78)
log("SECTION 9: FINE SCAN -- BOTH ALPHA_2 AND ALPHA_Y FREE")
log("=" * 78)
log()
log("  Both alpha_2(bare) and alpha_Y(bare) may differ from 1/(4*pi).")
log("  Scan a 2D grid and find the (alpha_2, alpha_Y) pair that simultaneously")
log("  matches BOTH alpha_EM(M_Z) and sin^2(theta_W)(M_Z).")
log()

# Use raw normalization (no 5/3 factor)
# We need to match TWO observables: alpha_EM and sin^2(tW)
# So we have exactly TWO unknowns (alpha_2_bare, alpha_Y_bare) -- determined.

# From the running: alpha_2(M_Z) is determined by alpha_2_bare and b_2.
# We need alpha_2(M_Z) = alpha_EM(M_Z) / sin^2(tW) = observed value.
# So alpha_2_bare is fixed by the observed alpha_2(M_Z).
# Similarly for alpha_Y.

# The UNIQUE solution:
# Running UP from M_Z: 1/alpha(M_Pl) = 1/alpha(M_Z) + b*L/(2*pi)
# So: 1/alpha_bare = 1/alpha(M_Z) + b*L/(2*pi)
# => alpha_bare = 1/(1/alpha(M_Z) + b*L/(2*pi))
inv_a2_bare_exact = 1.0/ALPHA_2_MZ + B_2_SM * L_planck / (2*PI)
alpha_2_bare_exact = 1.0 / inv_a2_bare_exact if inv_a2_bare_exact > 0 else float('inf')

inv_aY_bare_exact = 1.0/alpha_Y_mz_obs + B_Y_RAW * L_planck / (2*PI)
alpha_Y_bare_exact = 1.0 / inv_aY_bare_exact if inv_aY_bare_exact > 0 else float('inf')

log("  EXACT bare couplings implied by observation (raw normalization):")
log()
log("    alpha_2(bare)  = {:.8f} = 1/{:.4f} = 1/(4*pi*{:.6f})".format(
    alpha_2_bare_exact, 1/alpha_2_bare_exact,
    1/(4*PI*alpha_2_bare_exact)))
log("    alpha_Y(bare)  = {:.8f} = 1/{:.4f} = 1/(4*pi*{:.6f})".format(
    alpha_Y_bare_exact, 1/alpha_Y_bare_exact,
    1/(4*PI*alpha_Y_bare_exact)))
log("    alpha_3(bare)  = {:.8f} = 1/{:.4f} = 1/(4*pi*{:.6f})".format(
    ALPHA_S_BARE, 1/ALPHA_S_BARE, 1/(4*PI*ALPHA_S_BARE)))
log()

# Ratios
r_2_3 = alpha_2_bare_exact / ALPHA_S_BARE
r_Y_3 = alpha_Y_bare_exact / ALPHA_S_BARE
r_Y_2 = alpha_Y_bare_exact / alpha_2_bare_exact

log("  Ratios of bare couplings:")
log("    alpha_2 / alpha_3 = {:.6f}".format(r_2_3))
log("    alpha_Y / alpha_3 = {:.6f}".format(r_Y_3))
log("    alpha_Y / alpha_2 = {:.6f}".format(r_Y_2))
log()

# sin^2(tW) at bare scale (raw normalization)
sin2_bare_exact = alpha_Y_bare_exact / (alpha_Y_bare_exact + alpha_2_bare_exact)
log("    sin^2(theta_W) at bare = {:.6f}".format(sin2_bare_exact))
log()

# g^2 values
g2_sq = 4 * PI * alpha_2_bare_exact
gY_sq = 4 * PI * alpha_Y_bare_exact
g3_sq = 4 * PI * ALPHA_S_BARE

log("  Bare coupling constants g^2 = 4*pi*alpha:")
log("    g_3^2 = {:.6f}  (= 1, by construction)".format(g3_sq))
log("    g_2^2 = {:.6f}".format(g2_sq))
log("    g_Y^2 = {:.6f}".format(gY_sq))
log()

# Check for simple relationships
log("  Looking for geometric/algebraic patterns:")
log()

# Check if g_2^2 or g_Y^2 are simple fractions or functions of lattice geometry
for desc, val in [
    ("1", 1.0),
    ("1/2", 0.5),
    ("1/3", 1/3),
    ("1/4", 0.25),
    ("1/6", 1/6),
    ("1/d = 1/3", 1/3),
    ("1/z = 1/6", 1/6),
    ("1/(d+1) = 1/4", 0.25),
    ("d/(d+1) = 3/4", 0.75),
    ("2/z = 1/3", 1/3),
    ("(d-1)/d = 2/3", 2/3),
    ("d/z = 1/2", 0.5),
    ("pi/4", PI/4),
    ("pi/6", PI/6),
    ("1/pi", 1/PI),
    ("2/pi", 2/PI),
    ("sqrt(2)", np.sqrt(2)),
    ("1/sqrt(2)", 1/np.sqrt(2)),
    ("1/sqrt(3)", 1/np.sqrt(3)),
    ("3/8", 3/8),
    ("5/8", 5/8),
    ("3/5", 3/5),
]:
    err_g2 = abs(g2_sq - val) / max(abs(val), 1e-10) * 100
    err_gY = abs(gY_sq - val) / max(abs(val), 1e-10) * 100
    if err_g2 < 5:
        log("    g_2^2 ~ {} = {:.6f}  (err {:.2f}%)".format(desc, val, err_g2))
    if err_gY < 5:
        log("    g_Y^2 ~ {} = {:.6f}  (err {:.2f}%)".format(desc, val, err_gY))

log()

# Check ratios against simple fractions
log("  Checking ratios against simple fractions and lattice constants:")
for desc, val in [
    ("1/2", 0.5), ("1/3", 1/3), ("2/3", 2/3), ("1/4", 0.25),
    ("3/4", 0.75), ("1/5", 0.2), ("2/5", 0.4), ("3/5", 0.6),
    ("1/6", 1/6), ("5/6", 5/6), ("1/d", 1/3), ("1/z", 1/6),
    ("d/z", 0.5), ("(d-1)/z", 1/3), ("2d/(z+2d)", 0.5),
    ("1/(d-1)", 0.5), ("(d-1)/d", 2/3),
    ("3/8", 3/8), ("5/8", 5/8), ("5/3", 5/3), ("8/3", 8/3),
]:
    err_r23 = abs(r_2_3 - val) / max(abs(val), 1e-10) * 100
    err_rY3 = abs(r_Y_3 - val) / max(abs(val), 1e-10) * 100
    err_rY2 = abs(r_Y_2 - val) / max(abs(val), 1e-10) * 100
    if err_r23 < 3:
        log("    alpha_2/alpha_3 ~ {} = {:.6f}  (err {:.2f}%)".format(desc, val, err_r23))
    if err_rY3 < 3:
        log("    alpha_Y/alpha_3 ~ {} = {:.6f}  (err {:.2f}%)".format(desc, val, err_rY3))
    if err_rY2 < 3:
        log("    alpha_Y/alpha_2 ~ {} = {:.6f}  (err {:.2f}%)".format(desc, val, err_rY2))
log()


# Verify exact solution
log("  Verification (running exact bare couplings to M_Z):")
verify_exact = run_raw_from_planck(alpha_Y_bare_exact, alpha_2_bare_exact, ALPHA_S_BARE)
log("    1/alpha_EM(M_Z) = {:.4f}  (target: {:.4f})".format(
    verify_exact["inv_alpha_em"], 1/ALPHA_EM_MZ))
log("    sin^2(theta_W)  = {:.6f}  (target: {:.6f})".format(
    verify_exact["sin2tw"], SIN2_TW_MZ))
log("    alpha_s(M_Z)    = {:.5f}  (target: {:.5f})".format(
    verify_exact["alpha_3"], ALPHA_S_MZ))
log()


# =============================================================================
# SECTION 10: GUT-NORMALIZED ANALYSIS
# =============================================================================

log("=" * 78)
log("SECTION 10: SAME ANALYSIS WITH GUT NORMALIZATION")
log("=" * 78)
log()

# With GUT normalization, alpha_1 = (5/3)*alpha_Y
# 1/alpha_EM = (3/5)/alpha_1 + 1/alpha_2
inv_a1_bare_gut = 1.0/ALPHA_1_MZ + B_1_SM * L_planck / (2*PI)
alpha_1_bare_gut = 1.0/inv_a1_bare_gut if inv_a1_bare_gut > 0 else float('inf')

log("  Exact bare couplings (GUT normalization):")
log("    alpha_1(bare) = {:.8f} = 1/{:.4f}  [GUT norm]".format(
    alpha_1_bare_gut, 1/alpha_1_bare_gut))
log("    alpha_2(bare) = {:.8f} = 1/{:.4f}".format(
    alpha_2_bare_exact, 1/alpha_2_bare_exact))
log("    alpha_3(bare) = {:.8f} = 1/{:.4f}".format(
    ALPHA_S_BARE, 1/ALPHA_S_BARE))
log()

r_1_3_gut = alpha_1_bare_gut / ALPHA_S_BARE
r_1_2_gut = alpha_1_bare_gut / alpha_2_bare_exact

log("  Ratios (GUT norm):")
log("    alpha_1/alpha_3 = {:.6f}".format(r_1_3_gut))
log("    alpha_1/alpha_2 = {:.6f}".format(r_1_2_gut))
log("    alpha_2/alpha_3 = {:.6f}".format(r_2_3))
log()

sin2_gut_bare = (3.0/5.0)*alpha_1_bare_gut / (
    (3.0/5.0)*alpha_1_bare_gut + alpha_2_bare_exact)
log("    sin^2(theta_W) at bare (GUT norm) = {:.6f}".format(sin2_gut_bare))
log("    (should equal raw value: {:.6f})".format(sin2_bare_exact))
log()

# Verify
verify_gut = run_all_from_planck(alpha_1_bare_gut, alpha_2_bare_exact, ALPHA_S_BARE)
log("  Verification (GUT normalization):")
log("    1/alpha_EM(M_Z) = {:.4f}  (target: {:.4f})".format(
    verify_gut["inv_alpha_em"], 1/ALPHA_EM_MZ))
log("    sin^2(theta_W)  = {:.6f}  (target: {:.6f})".format(
    verify_gut["sin2tw"], SIN2_TW_MZ))
log()


# =============================================================================
# SECTION 11: SUMMARY AND GEOMETRIC INTERPRETATION
# =============================================================================

log("=" * 78)
log("SECTION 11: SUMMARY AND GEOMETRIC INTERPRETATION")
log("=" * 78)
log()

log("  THE KEY RESULT:")
log("  ===============")
log()
log("  If each gauge group gets its bare coupling from its own lattice")
log("  structure at the Planck scale, the EXACT bare couplings needed")
log("  to reproduce observation are (raw normalization):")
log()
log("    g_3^2 = {:.6f}  (SU(3), Z_3 vertex coloring)".format(g3_sq))
log("    g_2^2 = {:.6f}  (SU(2), Z_2 bipartite hopping)".format(g2_sq))
log("    g_Y^2 = {:.6f}  (U(1), edge phases)".format(gY_sq))
log()
log("    alpha_3(bare) = 1/(4*pi) = {:.8f}".format(ALPHA_S_BARE))
log("    alpha_2(bare) = {:.8f} = {:.4f} * alpha_3".format(
    alpha_2_bare_exact, r_2_3))
log("    alpha_Y(bare) = {:.8f} = {:.4f} * alpha_3".format(
    alpha_Y_bare_exact, r_Y_3))
log()
log("    sin^2(theta_W) at Planck = {:.6f}".format(sin2_bare_exact))
log()
log("  QUESTION: Can g_2^2 = {:.6f} and g_Y^2 = {:.6f} be derived".format(
    g2_sq, gY_sq))
log("  from the Z_2 bipartite and edge structures of the cubic lattice?")
log()

# Check the best discrete hypothesis from the scan
log("  FROM THE SCAN (GUT normalized):")
log("  Best discrete hypothesis: {} / {}".format(
    best["su2_name"], best["u1_name"]))
log("  gave 1/alpha_EM = {:.2f} (err {:.1f}%)".format(
    best["result"]["inv_alpha_em"], best["err_em"]))
log()

# Summary of all scanned hypotheses sorted by combined error
log("  TOP 5 CLOSEST HYPOTHESES (sorted by alpha_EM error):")
log()
for i, r in enumerate(scan_results[:5]):
    log("  {}. SU2: {} / U1: {}".format(
        i+1, r["su2_name"], r["u1_name"]))
    log("     1/alpha_EM = {:.2f} (err {:.1f}%), sin^2(tW) = {:.5f} (err {:.1f}%)".format(
        r["result"]["inv_alpha_em"], r["err_em"],
        r["result"]["sin2tw"], r["err_tw"]))
    log()

log()


# =============================================================================
# SECTION 12: STATUS AND NEXT STEPS
# =============================================================================

log("=" * 78)
log("SECTION 12: STATUS AND NEXT STEPS")
log("=" * 78)
log()
log("  STATUS: The framework CAN accommodate alpha_EM = 1/137 if the three")
log("  gauge groups have different bare couplings at the Planck scale.")
log("  The required bare couplings are determined by 1-loop RG running.")
log()
log("  The OPEN QUESTION is whether these bare couplings can be DERIVED")
log("  from the lattice structures:")
log()
log("  1. alpha_3 = 1/(4*pi) from Z_3 clock-shift algebra [DONE]")
log("  2. alpha_2 = {:.6f} from Z_2 bipartite structure [NEEDED]".format(
    alpha_2_bare_exact))
log("     - g_2^2 = {:.6f} -- what lattice property gives this?".format(g2_sq))
log("     - Ratio alpha_2/alpha_3 = {:.4f}".format(r_2_3))
log()
log("  3. alpha_Y = {:.6f} from edge phase structure [NEEDED]".format(
    alpha_Y_bare_exact))
log("     - g_Y^2 = {:.6f} -- what edge geometry gives this?".format(gY_sq))
log("     - Ratio alpha_Y/alpha_3 = {:.4f}".format(r_Y_3))
log()
log("  NEXT STEPS:")
log("  a) Compute hopping matrix norms for Cl(3) on bipartite cubic lattice")
log("  b) Compute edge Laplacian eigenvalues and relate to U(1) bare coupling")
log("  c) Check if ratios match any lattice-theory constants")
log("  d) Add 2-loop running and threshold corrections for precision")
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
