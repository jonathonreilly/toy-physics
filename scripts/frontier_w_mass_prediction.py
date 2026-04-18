#!/usr/bin/env python3
"""
W-boson same-surface consistency probe on the retained Cl(3)/Z^3 EW lane.
==========================================================================

New lane. Combines the retained framework numerics
    v        = 246.282818290129 GeV          [OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE]
    g_2(v)   = 0.6480                         [YT_EW_COLOR_PROJECTION_THEOREM]
    g_1(v)   = 0.4644   (GUT normalization)   [YT_EW_COLOR_PROJECTION_THEOREM]

with the SM 1-loop SU(2) beta coefficient b_2 = 19/6 as a pure group-theory
input (the same coefficient used by the retained sin^2(theta_W) / alpha_EM
running bridge and by the retained alpha_s lane).

Two readouts:

    M_W^tree = g_2(v) * v / 2
    M_W^RGE  = fixed point of  M_W = g_2(M_W) * v / 2   (no pole import)

and the M_Z consistency cross-check,

    M_Z^tree = sqrt(g_1_Y^2 + g_2^2) * v / 2,   g_1_Y^2 = (3/5) * g_1_GUT^2.

Lane status: package-captured bounded same-surface consistency probe. The
residual against pole measurements tracks the precision already present in
the retained g_2(v) readout (YT_EW_COLOR_PROJECTION: g_2(v)_framework vs
g_2(v)_observed is at the 0.26% level) and is NOT of the few-MeV size that
ordinary missing SM 2-loop / Delta r_rem corrections carry on the SM
indirect M_W surface.

Self-contained: numpy only.
PStack lane: w-mass-prediction
"""

from __future__ import annotations

import os
import time

import numpy as np

np.set_printoptions(precision=6, linewidth=120)

LOG_FILE = "logs/" + time.strftime("%Y-%m-%d") + "-w-mass-prediction.txt"

results: list[str] = []


def log(msg: str = "") -> None:
    results.append(msg)
    print(msg)


# =============================================================================
# RETAINED FRAMEWORK INPUTS (same-surface values on main)
# =============================================================================

V_EW = 246.282818290129           # GeV, retained OBSERVABLE_PRINCIPLE lane
G_2_V = 0.6480                     # retained YT_EW_COLOR_PROJECTION_THEOREM
G_1_GUT_V = 0.4644                 # retained (GUT normalization)
SIN2_THW_MZ = 0.2306               # retained running-bridge readout (reported only)

# Hypercharge gauge coupling at v in the SM convention:
#     g_Y^2 = (3/5) * g_1_GUT^2
G_Y_V = G_1_GUT_V * np.sqrt(3.0 / 5.0)


# =============================================================================
# EXPERIMENTAL COMPARATORS (not inputs to the derivation)
# =============================================================================

# Pole masses
M_Z_PDG = 91.1876                  # GeV, PDG 2024, reference only

# W-mass measurements (central +/- combined uncertainty)
M_W_PDG = (80.3692, 0.0133)        # GeV, PDG 2024 world average
M_W_CDF2022 = (80.4335, 0.0094)    # GeV, CDF-II 2022
M_W_ATLAS2024 = (80.3665, 0.0159)  # GeV, ATLAS 7 TeV reanalysis
M_W_CMS2024 = (80.3602, 0.0099)    # GeV, CMS first measurement
M_W_LHCB2022 = (80.354, 0.032)     # GeV, LHCb


def pct(pred: float, obs: float) -> float:
    return 100.0 * (pred - obs) / obs


# =============================================================================
# TREE-LEVEL READOUT
# =============================================================================

log("=" * 78)
log("W-BOSON MASS ON THE RETAINED Cl(3)/Z^3 EW NORMALIZATION SURFACE")
log("=" * 78)
log()
log("Package-captured bounded same-surface probe.")
log("NOT on the retained quantitative / prediction surface.")
log("The residual against pole measurements tracks the precision already")
log("present in the retained g_2(v) readout and is NOT absorbed by SM")
log("2-loop / Delta r_rem corrections, which are at the few-MeV level.")
log()

log("-" * 78)
log("1. Retained framework inputs")
log("-" * 78)
log(f"  v (EW scale)        = {V_EW:.12f} GeV")
log(f"  g_2(v)              = {G_2_V:.4f}")
log(f"  g_1(v) [GUT norm]   = {G_1_GUT_V:.4f}")
log(f"  g_Y(v) = g_1*sqrt(3/5) = {G_Y_V:.4f}")
log(f"  sin^2 theta_W(M_Z)  = {SIN2_THW_MZ:.4f}   (reported, not used in solve)")
log()

log("-" * 78)
log("2. Tree-level readouts")
log("-" * 78)
MW_TREE = G_2_V * V_EW / 2.0
MZ_TREE = np.sqrt(G_Y_V**2 + G_2_V**2) * V_EW / 2.0
SIN2_ONSHELL_TREE = 1.0 - (MW_TREE / MZ_TREE) ** 2

log(f"  M_W^tree = g_2(v) * v / 2")
log(f"           = {G_2_V:.4f} * {V_EW:.6f} / 2")
log(f"           = {MW_TREE:.4f} GeV")
log()
log(f"  M_Z^tree = sqrt(g_Y^2 + g_2^2) * v / 2")
log(f"           = sqrt({G_Y_V**2:.6f} + {G_2_V**2:.6f}) * {V_EW:.6f} / 2")
log(f"           = {MZ_TREE:.4f} GeV")
log()
log(f"  sin^2(theta_W)^OS(tree) = 1 - (M_W/M_Z)^2 = {SIN2_ONSHELL_TREE:.4f}")
log(f"  (compare retained MS-bar readout = {SIN2_THW_MZ:.4f})")
log()

log("  Tree-level consistency against PDG pole masses:")
log(f"    M_W^tree vs PDG 80.3692: {pct(MW_TREE, M_W_PDG[0]):+.3f}%")
log(f"    M_Z^tree vs PDG {M_Z_PDG:.4f}: {pct(MZ_TREE, M_Z_PDG):+.3f}%")
log()


# =============================================================================
# ONE-LOOP RGE READOUT: SELF-CONSISTENT g_2(M_W) * v / 2 FIXED POINT
# =============================================================================
#
# The retained g_2(v) is at scale mu = v = 246 GeV. Running g_2 down
# with the SM 1-loop SU(2) beta coefficient (no active top at the W
# scale, so b_2 = 19/6) gives
#
#     1/alpha_2(mu) = 1/alpha_2(v) + (b_2 / (2 pi)) * ln(mu / v)
#
# The framework-side RGE readout is the fixed point of
#
#     M_W = g_2(M_W) * v / 2
#
# solved iteratively. No SM pole value enters the solve; the only
# experimental quantities in the runner (PDG / CDF / ATLAS / CMS / LHCb
# central values) are used exclusively for the comparison table below.
# =============================================================================

log("-" * 78)
log("3. One-loop RGE readout (same-surface consistency probe)")
log("-" * 78)
log()
log("  Self-consistent fixed-point solve (NO pole value imported):")
log("    M_W = g_2(M_W) * v / 2")
log("    1/alpha_2(M_W) = 1/alpha_2(v) + (b_2/(2 pi)) * ln(M_W / v)")
log("    b_2 = 19/6     (SM 1-loop SU(2), no active top at W scale)")
log()

# G_F from retained v (reported for completeness; not used in the
# framework-side readout).
G_F = 1.0 / (np.sqrt(2.0) * V_EW**2)   # GeV^-2

B_2 = 19.0 / 6.0                        # SM SU(2) 1-loop beta coefficient
ALPHA_2_V = G_2_V**2 / (4.0 * np.pi)


def g2_at(mu: float) -> float:
    inv = 1.0 / ALPHA_2_V + B_2 / (2.0 * np.pi) * np.log(mu / V_EW)
    return float(np.sqrt(4.0 * np.pi / inv))


# Fixed-point iteration, anchored only by the tree readout M_W^tree = g_2(v)*v/2.
MW_RGE = MW_TREE
iterations = 0
for iterations in range(1, 101):
    mw_next = g2_at(MW_RGE) * V_EW / 2.0
    if abs(mw_next - MW_RGE) < 1.0e-10:
        MW_RGE = mw_next
        break
    MW_RGE = mw_next

G_2_MW = g2_at(MW_RGE)
ALPHA_2_MW = G_2_MW**2 / (4.0 * np.pi)

log(f"  alpha_2(v)       = g_2(v)^2/(4 pi) = {ALPHA_2_V:.6f}")
log(f"  1/alpha_2(v)     = {1.0/ALPHA_2_V:.4f}")
log(f"  b_2 / (2 pi)     = {B_2 / (2.0 * np.pi):.6f}")
log(f"  iterations to converge (|dM| < 1e-10 GeV) = {iterations}")
log(f"  self-consistent g_2(M_W)  = {G_2_MW:.6f}")
log(f"  self-consistent alpha_2(M_W) = {ALPHA_2_MW:.6f}")
log(f"  ln(M_W / v) at fixed point = {np.log(MW_RGE / V_EW):+.6f}")
log()
log(f"  M_W^RGE = g_2(M_W) * v / 2 = {MW_RGE:.4f} GeV")
log(f"  delta_RGE relative to tree: {pct(MW_RGE, MW_TREE):+.3f}%")
log()
log(f"  G_F from retained v = 1/(sqrt(2) v^2) = {G_F:.6e} GeV^-2  (not used)")
log()


# =============================================================================
# EXPERIMENTAL COMPARISON
# =============================================================================

log("-" * 78)
log("4. Comparison table")
log("-" * 78)
log()
log(f"  {'Measurement':<22s} {'value (GeV)':>14s} {'sigma':>8s}   "
    f"{'M_W^tree Delta':>16s} {'M_W^RGE Delta':>16s}")
log("  " + "-" * 80)


def delta_row(label: str, central: float, sigma: float) -> None:
    d_tree = MW_TREE - central
    d_rge = MW_RGE - central
    log(f"  {label:<22s} {central:>14.4f} {sigma:>8.4f}   "
        f"{d_tree:>+8.4f} GeV    {d_rge:>+8.4f} GeV")


delta_row("PDG 2024 average",     *M_W_PDG)
delta_row("CDF-II 2022",          *M_W_CDF2022)
delta_row("ATLAS 2024 reanalysis", *M_W_ATLAS2024)
delta_row("CMS 2024",             *M_W_CMS2024)
delta_row("LHCb 2022",            *M_W_LHCB2022)
log()
log(f"  Tree gap to PDG:    {pct(MW_TREE, M_W_PDG[0]):+.3f}%")
log(f"  RGE gap to PDG:     {pct(MW_RGE, M_W_PDG[0]):+.3f}%")
log(f"  Tree gap to CDF:    {pct(MW_TREE, M_W_CDF2022[0]):+.3f}%")
log(f"  RGE gap to CDF:     {pct(MW_RGE, M_W_CDF2022[0]):+.3f}%")
log()


# =============================================================================
# SUMMARY
# =============================================================================

log("=" * 78)
log("5. Summary")
log("=" * 78)
log()
log(f"  Framework-side tree readout:  M_W^tree = {MW_TREE:.4f} GeV")
log(f"  Framework-side RGE readout:   M_W^RGE  = {MW_RGE:.4f} GeV")
log("  (both are bounded same-surface probes, NOT retained claims)")
log()

# Cross-check that the residual inherits the retained g_2(v) precision.
# The retained YT_EW_COLOR_PROJECTION row is
#     g_2(v)_framework = 0.64795  vs  g_2(v)_observed = 0.64629  (+0.26%)
# That 0.26% gap feeds directly into M_W at the same scale.
G_2_V_OBSERVED = 0.64629
g2_gap_pct = 100.0 * (G_2_V - G_2_V_OBSERVED) / G_2_V_OBSERVED
mw_rge_vs_pdg_pct = pct(MW_RGE, M_W_PDG[0])
log(f"  Retained g_2(v) lane precision vs observed: {g2_gap_pct:+.3f}%")
log(f"  M_W^RGE gap to PDG:                          {mw_rge_vs_pdg_pct:+.3f}%")
log("  => the RGE residual is consistent with the retained g_2(v) precision")
log("     being inherited at the W scale; it is NOT absorbable by SM 2-loop")
log("     / Delta r_rem corrections (which are O(few MeV)).")
log()
log()

log("=" * 78)
log("COMPUTATION COMPLETE")
log("=" * 78)

os.makedirs("logs", exist_ok=True)
try:
    with open(LOG_FILE, "w") as fh:
        fh.write("\n".join(results))
    log(f"\nLog saved to {LOG_FILE}")
except Exception as exc:  # pragma: no cover
    log(f"\nCould not save log: {exc}")
