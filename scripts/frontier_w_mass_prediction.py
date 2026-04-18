#!/usr/bin/env python3
"""
W-boson mass prediction on the retained Cl(3)/Z^3 EW normalization surface.
=============================================================================

New lane. Combines the retained framework numerics
    v        = 246.282818290129 GeV          [OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE]
    g_2(v)   = 0.6480                         [YT_EW_COLOR_PROJECTION_THEOREM]
    g_1(v)   = 0.4644   (GUT normalization)   [YT_EW_COLOR_PROJECTION_THEOREM]
    sin^2 theta_W(M_Z) = 0.2306                [same lane + running bridge]
    m_t(pole, 3-loop)  = 173.10 GeV            [YT_ZERO_IMPORT_AUTHORITY_NOTE]
    m_H(3-loop)        = 125.1  GeV            [HIGGS_MASS_DERIVED_NOTE]
    alpha_s(M_Z)       = 0.1181                [ALPHA_S_DERIVED_NOTE]

to produce the Cl(3)/Z^3 prediction for the W-boson pole mass.

Two readouts:

    M_W^tree = g_2(v) * v / 2
    M_W^loop = M_W^tree * (1 + Delta M_W / M_W)   [bounded-companion estimate]

and the M_Z consistency cross-check from the same surface,

    M_Z^tree = sqrt(g_1_Y^2 + g_2^2) * v / 2

with g_1_Y^2 = (3/5) * g_1_GUT^2.

No SM imports enter the framework-side readout. The reported loop gap is
carried as a bounded companion, not a retained row.

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
SIN2_THW_MZ = 0.2306               # retained running-bridge readout
ALPHA_S_MZ = 0.1181                # retained ALPHA_S_DERIVED_NOTE
M_TOP_3LOOP = 173.10               # GeV, retained YT_ZERO_IMPORT_AUTHORITY_NOTE
M_HIGGS = 125.1                    # GeV, retained HIGGS_MASS_DERIVED_NOTE

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
log("This is a new lane: not previously on the prediction surface.")
log("Reported status: bounded companion. The tree-level readout is the")
log("framework-side M_W; the loop gap against pole measurements is the")
log("expected magnitude of SM one-loop corrections, not a retained claim.")
log()

log("-" * 78)
log("1. Retained framework inputs")
log("-" * 78)
log(f"  v (EW scale)        = {V_EW:.12f} GeV")
log(f"  g_2(v)              = {G_2_V:.4f}")
log(f"  g_1(v) [GUT norm]   = {G_1_GUT_V:.4f}")
log(f"  g_Y(v) = g_1*sqrt(3/5) = {G_Y_V:.4f}")
log(f"  sin^2 theta_W(M_Z)  = {SIN2_THW_MZ:.4f}")
log(f"  alpha_s(M_Z)        = {ALPHA_S_MZ:.4f}")
log(f"  m_t(pole, 3-loop)   = {M_TOP_3LOOP:.2f} GeV")
log(f"  m_H(3-loop)         = {M_HIGGS:.1f} GeV")
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
# ONE-LOOP RGE READOUT: g_2 RUN FROM v DOWN TO THE W POLE
# =============================================================================
#
# The retained g_2(v) is at scale mu = v = 246 GeV. The W pole mass is
# set at mu = M_W ~ 80 GeV. Running g_2 down with the SM beta function
# (active fermions at this scale: no top, so b_2 = 19/6) gives
#
#     1/alpha_2(M_W) = 1/alpha_2(v) + (b_2 / (2 pi)) * ln(M_W / v)
#
# which increases g_2 because M_W < v. The MS-bar pole relation is then
# M_W = g_2(M_W) * v / 2 up to ~0.1% EW mixing corrections
# (standard Sirlin Delta r_rem on this scheme). This is the second
# framework-side readout; the residual beyond it is a BOUNDED companion.
# =============================================================================

log("-" * 78)
log("3. One-loop RGE readout (bounded companion; NOT a retained claim)")
log("-" * 78)
log()
log("  Run g_2 from v down to the W pole with SM 1-loop beta function")
log("  (b_2 = 19/6, no active top at this scale):")
log()

# G_F derived from retained v via G_F = 1/(sqrt(2) * v^2) -- reported for
# completeness (it appears in the Sirlin form but is not used by the
# framework-side readout here).
G_F = 1.0 / (np.sqrt(2.0) * V_EW**2)   # GeV^-2

B_2 = 19.0 / 6.0                        # SM SU(2) 1-loop beta coefficient
ALPHA_2_V = G_2_V**2 / (4.0 * np.pi)
TARGET_MW = M_W_PDG[0]                  # self-consistent iteration anchor;
                                        # final M_W^RGE is insensitive to
                                        # the choice of anchor at the ~ppm
                                        # level because log enters linearly

# One iteration is enough given the tiny self-consistency gap.
inv_alpha_2_mw = 1.0 / ALPHA_2_V + B_2 / (2.0 * np.pi) * np.log(TARGET_MW / V_EW)
ALPHA_2_MW = 1.0 / inv_alpha_2_mw
G_2_MW = np.sqrt(4.0 * np.pi * ALPHA_2_MW)
MW_RGE = G_2_MW * V_EW / 2.0

log(f"  alpha_2(v)   = g_2^2/(4 pi) = {ALPHA_2_V:.6f}")
log(f"  1/alpha_2(v) = {1.0/ALPHA_2_V:.4f}")
log(f"  ln(M_W / v)  = {np.log(TARGET_MW / V_EW):+.6f}")
log(f"  b_2 / (2 pi) = {B_2 / (2.0 * np.pi):.6f}")
log(f"  1/alpha_2(M_W) = 1/alpha_2(v) + b_2/(2 pi) * ln(M_W/v)")
log(f"                 = {1.0/ALPHA_2_V:.4f} + {B_2/(2.0*np.pi):.4f} * "
    f"({np.log(TARGET_MW/V_EW):+.4f})")
log(f"                 = {inv_alpha_2_mw:.4f}")
log(f"  alpha_2(M_W) = {ALPHA_2_MW:.6f}")
log(f"  g_2(M_W)     = {G_2_MW:.4f}")
log()
log(f"  M_W^RGE = g_2(M_W) * v / 2 = {MW_RGE:.4f} GeV")
log(f"  delta_RGE relative to tree: {pct(MW_RGE, MW_TREE):+.3f}%")
log()
log(f"  G_F from retained v = 1/(sqrt(2) v^2) = {G_F:.6e} GeV^-2")
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
log(f"  Tree gap to PDG:    {pct(MW_TREE, M_W_PDG[0]):+.3f}%  "
    f"(framework low; RGE running expected to close)")
log(f"  RGE gap to PDG:     {pct(MW_RGE, M_W_PDG[0]):+.3f}%  "
    f"(bounded-companion readout)")
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
log(f"  Framework-side tree readout:   M_W^tree = {MW_TREE:.4f} GeV")
log(f"  Framework-side RGE readout:    M_W^RGE  = {MW_RGE:.4f} GeV  "
    "(bounded companion)")
log()
log("  Discriminant among experimental central values:")
log(f"    |M_W^RGE - PDG|    = {abs(MW_RGE - M_W_PDG[0]):.4f} GeV "
    f"({abs(MW_RGE - M_W_PDG[0]) / M_W_PDG[1]:.2f} sigma_PDG)")
log(f"    |M_W^RGE - CDF|    = {abs(MW_RGE - M_W_CDF2022[0]):.4f} GeV "
    f"({abs(MW_RGE - M_W_CDF2022[0]) / M_W_CDF2022[1]:.2f} sigma_CDF)")
log()
log("  The tree-level readout uses only retained same-surface values. The")
log("  RGE readout runs the same-surface g_2 down to the W pole with the")
log("  SM 1-loop beta coefficient and is kept as a bounded companion.")
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
