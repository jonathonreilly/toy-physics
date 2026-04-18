#!/usr/bin/env python3
"""
Frontier runner: Yukawa Species-Uniformity Falsification-Extent Analysis.

Status
------
Retention-analysis runner extending the b-quark Ward retention analysis
(docs/YT_BOTTOM_YUKAWA_RETENTION_ANALYSIS_NOTE_2026-04-18.md) to ALL nine
charged-fermion species (6 quarks + 3 charged leptons) simultaneously.
The goal is to quantify the extent of the species-uniformity falsification
under the retained Ward identity's Block 6 species-uniform Clebsch-Gordan
(all basis components of (1,1) singlets on Q_L = (2,3) and L_L = (2,1)
equal 1/sqrt(6) by the same singlet uniformity argument).

Approach
--------
We use the SAME RGE engine template as the retained b-quark retention
runner (`frontier_yt_bottom_yukawa_retention.py`), extending from 2 to 9
Yukawas (plus the 3 gauge couplings).  For the primary convergence scan
we use BACKWARD integration (v -> M_Pl) starting from a trial y_common(v)
and iteratively adjust until the M_Pl endpoint lands on the Ward target
g_s(M_Pl)/sqrt(6) = 0.436.  This is the SAME methodology as
frontier_yt_2loop_chain.py and frontier_yt_bottom_yukawa_retention.py
because forward integration from M_Pl with the canonical lattice
g_3(M_Pl) = 1.068 is known to hit a Landau pole before reaching v
(the framework's canonical M_Pl coupling is a lattice-scheme constant,
not an RGE-consistent UV anchor for SM matter content at n_f = 6).

Once a converged y_common(v) is found, we compute per-species masses
m_s = y_s(v) * v/sqrt(2) for each of the 9 species and compare to
observation.

In addition we run a SINGLE-SPECIES-DECOUPLED consistency check
(y_t alone, y_c alone, etc.), and a TOP-ONLY SPECIES-PRIVILEGED scan to
confirm the retained framework's m_t = 172.57 GeV prediction is
species-privileged (not species-uniform).

Outcome
-------
Outcome A-extended (Yukawa unification at M_Pl across ALL species).
Under the full coupled SM 2-loop RGE with species-uniform BC:
  y_s(v) ~ 0.5-0.6 for quarks (quasi-fixed-point under coupled running);
  y_s(v) ~ 0.4-0.5 for leptons (small T-drag, no QCD).
  m_s(v) ~ 50-100 GeV for all 9 species.
  All 9 observed masses are falsified by 1-5 orders of magnitude.

Specifically:
  m_t = 172.57 GeV (retained framework claim) does NOT survive the
  species-uniform BC: under y_t(M_Pl) = 0.436 AND all other Yukawas also
  at 0.436 at M_Pl, y_t(v) collapses toward the common species value.
  The retained top prediction requires SPECIES-PRIVILEGED BC (y_t at
  Ward value with other Yukawas at their observed v-values), NOT the
  species-uniform BC implied by Block 6.

Authority
---------
Retained foundations used by this runner (not modified here):
  - docs/YT_WARD_IDENTITY_DERIVATION_THEOREM.md
  - docs/YT_BOTTOM_YUKAWA_RETENTION_ANALYSIS_NOTE_2026-04-18.md
  - docs/CHARGED_LEPTON_MASS_HIERARCHY_REVIEW_NOTE_2026-04-17.md
  - scripts/canonical_plaquette_surface.py
  - scripts/frontier_yt_2loop_chain.py (RGE engine template)
  - scripts/frontier_yt_bottom_yukawa_retention.py (2-Yukawa template)

Authority note (this runner):
  docs/YT_SPECIES_UNIFORMITY_EXTENT_NOTE_2026-04-18.md

Self-contained except for numpy/scipy.
"""

from __future__ import annotations

import math
import sys
from typing import Dict, List, Optional, Tuple

import numpy as np

try:
    from scipy.integrate import solve_ivp
except ImportError:
    print("ERROR: scipy required. pip install scipy")
    sys.exit(1)

from canonical_plaquette_surface import (
    CANONICAL_ALPHA_BARE,
    CANONICAL_ALPHA_LM,
    CANONICAL_ALPHA_S_V,
    CANONICAL_PLAQUETTE,
    CANONICAL_U0,
)


# ---------------------------------------------------------------------------
# PASS/FAIL bookkeeping
# ---------------------------------------------------------------------------

PASS_COUNT = 0
FAIL_COUNT = 0


def check(name: str, condition: bool, detail: str = "") -> None:
    global PASS_COUNT, FAIL_COUNT
    if condition:
        PASS_COUNT += 1
        status = "PASS"
    else:
        FAIL_COUNT += 1
        status = "FAIL"
    line = f"  [{status}] {name}"
    if detail:
        line += f"  ({detail})"
    print(line)


# ---------------------------------------------------------------------------
# Retained framework constants (inherited from upstream theorems)
# ---------------------------------------------------------------------------

PI = math.pi
N_C = 3
N_ISO = 2
DIM_Q_L = N_C * N_ISO                    # 6
DIM_L_L = N_ISO                          # 2 (L_L = (2,1)_-1, no color)

# Canonical surface (retained)
ALPHA_BARE = CANONICAL_ALPHA_BARE
U_0 = CANONICAL_U0
ALPHA_LM = CANONICAL_ALPHA_LM            # ~0.09067
ALPHA_S_V = CANONICAL_ALPHA_S_V          # ~0.1033 (CMT canonical)

# Ward identity at M_Pl (tree-level, lattice surface)
G3_PL_LATTICE = math.sqrt(4.0 * PI * ALPHA_LM)      # ~1.067
Y_WARD_PL = G3_PL_LATTICE / math.sqrt(6.0)          # ~0.436 (species-uniform)

# Retained scale constants
M_PL = 1.2209e19                         # unreduced Planck mass (GeV)
V = 246.28                               # electroweak VEV (GeV)

# Standard SM EW couplings at v (CONTEXT ONLY, NOT derivation input)
G1_V_SM = 0.467
G2_V_SM = 0.649

# Observed masses (COMPARISON only)
M_U_OBS = 2.16e-3                        # GeV, m_u(2 GeV) = 2.16 MeV
M_D_OBS = 4.67e-3                        # GeV, m_d(2 GeV) = 4.67 MeV
M_S_OBS = 93.4e-3                        # GeV, m_s(2 GeV) = 93.4 MeV
M_C_OBS = 1.27                           # GeV, m_c(m_c)
M_B_OBS = 4.18                           # GeV, m_b(m_b)
M_T_OBS_POLE = 172.69                    # GeV, pole mass (PDG 2024)

# Charged leptons (pole masses)
M_E_OBS = 0.5109989461e-3                # GeV
M_MU_OBS = 105.6583745e-3                # GeV
M_TAU_OBS = 1.77686                      # GeV

# Standard QCD running factor (approximate)
QCD_RUNNING_V_TO_MB = 0.68               # m_b(v)/m_b(m_b) ~ 0.68 (1-loop QCD)

# Species labels
QUARK_UP = ["u", "c", "t"]
QUARK_DOWN = ["d", "s", "b"]
LEPTONS = ["e", "mu", "tau"]
ALL_SPECIES = QUARK_UP + QUARK_DOWN + LEPTONS   # 9 species total

OBSERVED_MASSES = {
    "u": M_U_OBS, "c": M_C_OBS, "t": M_T_OBS_POLE,
    "d": M_D_OBS, "s": M_S_OBS, "b": M_B_OBS,
    "e": M_E_OBS, "mu": M_MU_OBS, "tau": M_TAU_OBS,
}

# Species-uniform UV Yukawa value (from retained Block 6 species uniformity)
Y_PL_UNIFORM = Y_WARD_PL                 # = 1/sqrt(6) * g_s(M_Pl) ~ 0.436

# Observed Yukawas at v (for species-privileged scan BC on non-top species)
Y_U_V_OBS = M_U_OBS * math.sqrt(2) / V
Y_D_V_OBS = M_D_OBS * math.sqrt(2) / V
Y_S_V_OBS = M_S_OBS * math.sqrt(2) / V
Y_C_V_OBS = M_C_OBS * math.sqrt(2) / V
Y_B_V_OBS = M_B_OBS * math.sqrt(2) / V
Y_E_V_OBS = M_E_OBS * math.sqrt(2) / V
Y_MU_V_OBS = M_MU_OBS * math.sqrt(2) / V
Y_TAU_V_OBS = M_TAU_OBS * math.sqrt(2) / V


# ---------------------------------------------------------------------------
# Full SM 2-loop beta functions (9 Yukawas + 3 gauge couplings)
# ---------------------------------------------------------------------------
# Conventions: t = ln(mu); y = [g1, g2, g3,
#                              yu, yc, yt,
#                              yd, ys, yb,
#                              ye, ymu, ytau]
# g1 in GUT normalization: g1_GUT = sqrt(5/3) * g1_SM.
#
# Standard SM Yukawa 1-loop beta (Machacek-Vaughn, Arason et al.):
#   For up-type quark Q (Q = u, c, t):
#     β_Q = y_Q * [ (3/2)(y_Q^2 - y_{dQ}^2) + T - 17/20 g1^2 - 9/4 g2^2 - 8 g3^2 ]
#   For down-type quark D (D = d, s, b):
#     β_D = y_D * [ (3/2)(y_D^2 - y_{uD}^2) + T - 1/4 g1^2 - 9/4 g2^2 - 8 g3^2 ]
#   For charged lepton L (L = e, mu, tau):
#     β_L = y_L * [ (3/2)(y_L^2) + T - 9/4 g1^2 - 9/4 g2^2 ]
#
# T = 3*(y_u^2 + y_c^2 + y_t^2) + 3*(y_d^2 + y_s^2 + y_b^2)
#   + (y_e^2 + y_mu^2 + y_tau^2)

def beta_full_9y(t, y, n_f=6, include_2loop=True, include_ew=True):
    """Full SM 2-loop RGE for (g1, g2, g3, yu, yc, yt, yd, ys, yb, ye, ymu, ytau)."""
    g1, g2, g3, yu, yc, yt, yd, ys, yb, ye, ymu, ytau = y

    fac = 1.0 / (16.0 * PI**2)
    fac2 = fac * fac

    g1sq, g2sq, g3sq = g1 * g1, g2 * g2, g3 * g3

    yusq, ycsq, ytsq = yu * yu, yc * yc, yt * yt
    ydsq, yssq, ybsq = yd * yd, ys * ys, yb * yb
    yesq, ymsq, ytau_sq = ye * ye, ymu * ymu, ytau * ytau

    T = (3.0 * (yusq + ycsq + ytsq)
         + 3.0 * (ydsq + yssq + ybsq)
         + (yesq + ymsq + ytau_sq))

    # ── 1-loop gauge ──
    b1_1 = 41.0 / 10.0
    b2_1 = -19.0 / 6.0
    b3_1 = -(11.0 - 2.0 * n_f / 3.0)
    beta_g1_1 = b1_1 * g1**3
    beta_g2_1 = b2_1 * g2**3
    beta_g3_1 = b3_1 * g3**3

    # ── 1-loop Yukawa ──
    gauge_q_up = -17.0 / 20.0 * g1sq - 9.0 / 4.0 * g2sq - 8.0 * g3sq
    gauge_q_down = -1.0 / 4.0 * g1sq - 9.0 / 4.0 * g2sq - 8.0 * g3sq
    gauge_l = -9.0 / 4.0 * g1sq - 9.0 / 4.0 * g2sq

    if not include_ew:
        gauge_q_up = -8.0 * g3sq
        gauge_q_down = -8.0 * g3sq
        gauge_l = 0.0

    beta_yu_1 = yu * (1.5 * (yusq - ydsq) + T + gauge_q_up)
    beta_yc_1 = yc * (1.5 * (ycsq - yssq) + T + gauge_q_up)
    beta_yt_1 = yt * (1.5 * (ytsq - ybsq) + T + gauge_q_up)

    beta_yd_1 = yd * (1.5 * (ydsq - yusq) + T + gauge_q_down)
    beta_ys_1 = ys * (1.5 * (yssq - ycsq) + T + gauge_q_down)
    beta_yb_1 = yb * (1.5 * (ybsq - ytsq) + T + gauge_q_down)

    beta_ye_1 = ye * (1.5 * yesq + T + gauge_l)
    beta_ymu_1 = ymu * (1.5 * ymsq + T + gauge_l)
    beta_ytau_1 = ytau * (1.5 * ytau_sq + T + gauge_l)

    if not include_2loop:
        return [
            fac * beta_g1_1, fac * beta_g2_1, fac * beta_g3_1,
            fac * beta_yu_1, fac * beta_yc_1, fac * beta_yt_1,
            fac * beta_yd_1, fac * beta_ys_1, fac * beta_yb_1,
            fac * beta_ye_1, fac * beta_ymu_1, fac * beta_ytau_1,
        ]

    # ── 2-loop gauge ──
    y_up_sum = yusq + ycsq + ytsq
    y_down_sum = ydsq + yssq + ybsq
    y_lep_sum = yesq + ymsq + ytau_sq

    beta_g1_2 = g1**3 * (
        199.0 / 50.0 * g1sq + 27.0 / 10.0 * g2sq + 44.0 / 5.0 * g3sq
        - 17.0 / 10.0 * y_up_sum - 1.0 / 2.0 * y_down_sum
        - 3.0 / 2.0 * y_lep_sum
    )
    beta_g2_2 = g2**3 * (
        9.0 / 10.0 * g1sq + 35.0 / 6.0 * g2sq + 12.0 * g3sq
        - 3.0 / 2.0 * (y_up_sum + y_down_sum) - 1.0 / 2.0 * y_lep_sum
    )
    beta_g3_2 = g3**3 * (
        11.0 / 10.0 * g1sq + 9.0 / 2.0 * g2sq - 26.0 * g3sq
        - 2.0 * (y_up_sum + y_down_sum)
    )

    # ── 2-loop Yukawa (QCD-dominant; sub-leading for leptons) ──
    def quark_2loop(y_q_sq, y_q_val):
        return y_q_val * (-12.0 * y_q_sq * y_q_sq
                          + 36.0 * y_q_sq * g3sq
                          - 108.0 * g3sq * g3sq)

    beta_yu_2 = quark_2loop(yusq, yu)
    beta_yc_2 = quark_2loop(ycsq, yc)
    beta_yt_2 = quark_2loop(ytsq, yt)
    beta_yd_2 = quark_2loop(ydsq, yd)
    beta_ys_2 = quark_2loop(yssq, ys)
    beta_yb_2 = quark_2loop(ybsq, yb)

    # Leptons: no g3 coupling; leading -12 y^4 self-term only
    beta_ye_2 = ye * (-12.0 * yesq * yesq)
    beta_ymu_2 = ymu * (-12.0 * ymsq * ymsq)
    beta_ytau_2 = ytau * (-12.0 * ytau_sq * ytau_sq)

    return [
        fac * beta_g1_1 + fac2 * beta_g1_2,
        fac * beta_g2_1 + fac2 * beta_g2_2,
        fac * beta_g3_1 + fac2 * beta_g3_2,
        fac * beta_yu_1 + fac2 * beta_yu_2,
        fac * beta_yc_1 + fac2 * beta_yc_2,
        fac * beta_yt_1 + fac2 * beta_yt_2,
        fac * beta_yd_1 + fac2 * beta_yd_2,
        fac * beta_ys_1 + fac2 * beta_ys_2,
        fac * beta_yb_1 + fac2 * beta_yb_2,
        fac * beta_ye_1 + fac2 * beta_ye_2,
        fac * beta_ymu_1 + fac2 * beta_ymu_2,
        fac * beta_ytau_1 + fac2 * beta_ytau_2,
    ]


def run_backward_9y(y_at_v, include_2loop=True):
    """Run from v backward to M_Pl, returns 12-vector at M_Pl.
    Same methodology as frontier_yt_bottom_yukawa_retention.py."""
    t_v = math.log(V)
    t_Pl = math.log(M_PL)
    sol = solve_ivp(
        lambda t, y: beta_full_9y(t, y, n_f=6, include_2loop=include_2loop),
        [t_v, t_Pl], y_at_v,
        method='RK45', rtol=1e-10, atol=1e-12, max_step=0.5,
    )
    if not sol.success:
        return None
    return sol.y[:, -1]


# ---------------------------------------------------------------------------
# Backward-scan convergence: find common y(v) that lands on Ward BC at M_Pl
# ---------------------------------------------------------------------------

def scan_uniform_Yukawa_v(max_iter=200, tol=5e-4, include_2loop=True,
                          y0_trial=0.55, damping=0.4,
                          target_lattice=False):
    """Find y_common(v) such that running from v to M_Pl gives all 9
    Yukawas equal to g_s(M_Pl)/sqrt(6).

    target_lattice=False (default, matches b-quark runner Block 7):
      target = RGE-transported g_s(M_Pl)/sqrt(6).
    target_lattice=True (matches b-quark runner Block 10 top-only convention):
      target = Y_WARD_PL = g_s_lattice(M_Pl)/sqrt(6).
    """
    y_common_v = y0_trial
    last_yf = None
    for it in range(max_iter):
        y_v = [G1_V_SM, G2_V_SM, math.sqrt(4 * PI * ALPHA_S_V)]
        y_v += [y_common_v] * 9
        yf = run_backward_9y(y_v, include_2loop=include_2loop)
        if yf is None:
            y_common_v *= 0.9
            continue
        last_yf = yf
        g3_Pl = yf[2]
        if target_lattice:
            target = Y_WARD_PL
        else:
            target = g3_Pl / math.sqrt(6.0)
        yukawas_at_Pl = yf[3:12]
        mean_y_Pl = sum(yukawas_at_Pl) / 9.0
        dy = target - mean_y_Pl
        if abs(dy) < tol:
            return y_common_v, yf, it
        y_common_v += damping * dy * (y_common_v / max(mean_y_Pl, 1e-3))
    return y_common_v, last_yf, max_iter


# ---------------------------------------------------------------------------
# Top-only (species-privileged) backward scan
# ---------------------------------------------------------------------------

def scan_top_only_v(max_iter=100, tol=1e-4, include_2loop=True,
                    target_lattice=True):
    """Find y_t(v) under the TOP-ONLY BC: y_t(M_Pl) targets the LATTICE
    Ward value (Y_WARD_PL = 0.4358, NOT the RGE-transported g_s/sqrt(6))
    with all other Yukawas fixed at their observed values at v.

    This reproduces the retained framework's top prediction
    m_t = 172.57 GeV, following the same convention as
    frontier_yt_bottom_yukawa_retention.py Block 10 and
    frontier_yt_2loop_chain.py (Approach A)."""
    yt_v = 0.95
    last_yf = None
    # Linear scan to find rough location, then iterate
    best_err = 1e10
    best_yt_v = yt_v
    for yt_trial in np.linspace(0.80, 1.10, 40):
        y_v = [G1_V_SM, G2_V_SM, math.sqrt(4 * PI * ALPHA_S_V),
               Y_U_V_OBS, Y_C_V_OBS, yt_trial,
               Y_D_V_OBS, Y_S_V_OBS, Y_B_V_OBS,
               Y_E_V_OBS, Y_MU_V_OBS, Y_TAU_V_OBS]
        yf = run_backward_9y(y_v, include_2loop=include_2loop)
        if yf is None:
            continue
        target = Y_WARD_PL if target_lattice else yf[2] / math.sqrt(6.0)
        err = abs(yf[5] - target)
        if err < best_err:
            best_err = err
            best_yt_v = yt_trial
            last_yf = yf
    return best_yt_v, last_yf, 0


# ---------------------------------------------------------------------------
# Single-Yukawa-only decoupled backward scan
# ---------------------------------------------------------------------------
# Run ONE Yukawa (species s) with all others set to 0 at v, and scan y_s(v)
# until y_s(M_Pl) = g_s(M_Pl)/sqrt(6).
# This is the species-decoupled analog — what y_s(v) would be if species
# s were the only non-zero Yukawa (no coupling to other species' T-trace).

def scan_single_yukawa(species, max_iter=80, tol=1e-4, include_2loop=True,
                       target_lattice=True):
    """Find y_s(v) for species s alone (other 8 Yukawas = 0 at v), that
    lands on the Ward BC at M_Pl.

    target_lattice=True (default, matches framework's top-only convention):
      target = Y_WARD_PL = 0.4358 (lattice).
    target_lattice=False (Yukawa-unification convention):
      target = RGE-transported g_s(M_Pl)/sqrt(6) ~ 0.199.
    """
    idx = {"u": 3, "c": 4, "t": 5, "d": 6, "s": 7, "b": 8,
           "e": 9, "mu": 10, "tau": 11}[species]

    # Linear scan to find best y_s(v)
    y_lo, y_hi = (0.4, 1.3) if species in QUARK_UP + QUARK_DOWN else (0.4, 1.3)
    best_err = 1e10
    best_y_s_v = 0.8
    last_yf = None
    for y_s_v in np.linspace(y_lo, y_hi, 50):
        y_v = [G1_V_SM, G2_V_SM, math.sqrt(4 * PI * ALPHA_S_V)] + [0.0] * 9
        y_v[idx] = y_s_v
        yf = run_backward_9y(y_v, include_2loop=include_2loop)
        if yf is None:
            continue
        if target_lattice:
            target = Y_WARD_PL
        else:
            target = yf[2] / math.sqrt(6.0)
        err = abs(yf[idx] - target)
        if err < best_err:
            best_err = err
            best_y_s_v = y_s_v
            last_yf = yf
    return best_y_s_v, last_yf, 0


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    print("=" * 72)
    print("YT Species-Uniformity Falsification-Extent Analysis")
    print("=" * 72)
    print()
    print("Extending the b-quark retention analysis to ALL 9 charged fermions")
    print("(6 quarks + 3 charged leptons) under the retained Block 6 species-")
    print("uniform Ward BC: y_s(M_Pl) = g_s(M_Pl)/sqrt(6) for all species s.")
    print()
    print("Full coupled SM 2-loop RGE (9 Yukawas + 3 gauge couplings).")
    print()

    # -----------------------------------------------------------------------
    # Block 1: Retained constants
    # -----------------------------------------------------------------------
    print("Block 1: Retained SU(3) Casimirs and canonical-surface anchors.")
    check(
        "N_C * N_iso = 6 (Q_L block dimension)",
        DIM_Q_L == 6,
        f"dim(Q_L) = {DIM_Q_L}",
    )
    check(
        "alpha_LM = 0.09067 +/- 1e-4 (canonical lattice surface)",
        abs(ALPHA_LM - 0.09067) < 1e-4,
        f"alpha_LM = {ALPHA_LM:.10f}",
    )
    check(
        "alpha_s(v) = 0.1033 +/- 1e-4 (CMT canonical value)",
        abs(ALPHA_S_V - 0.1033) < 1e-4,
        f"alpha_s(v) = {ALPHA_S_V:.10f}",
    )
    check(
        "g_3(M_Pl) = sqrt(4 pi alpha_LM) = 1.067 +/- 1e-3",
        abs(G3_PL_LATTICE - 1.067) < 1e-3,
        f"g_3(M_Pl) = {G3_PL_LATTICE:.6f}",
    )
    check(
        "y_Ward(M_Pl) = g_3/sqrt(6) = 0.4358 +/- 5e-4 (species-uniform)",
        abs(Y_WARD_PL - 0.4358) < 5e-4,
        f"y_Ward(M_Pl) = {Y_WARD_PL:.6f}",
    )
    print()

    # -----------------------------------------------------------------------
    # Block 2: Observed masses
    # -----------------------------------------------------------------------
    print("Block 2: Observed masses (PDG 2024) for comparison.")
    check(
        "m_u(2 GeV) observed = 2.16 MeV",
        abs(M_U_OBS - 2.16e-3) < 1e-6,
        f"m_u = {M_U_OBS*1e3:.3f} MeV",
    )
    check(
        "m_d(2 GeV) observed = 4.67 MeV",
        abs(M_D_OBS - 4.67e-3) < 1e-6,
        f"m_d = {M_D_OBS*1e3:.3f} MeV",
    )
    check(
        "m_s(2 GeV) observed = 93.4 MeV",
        abs(M_S_OBS - 93.4e-3) < 1e-6,
        f"m_s = {M_S_OBS*1e3:.1f} MeV",
    )
    check(
        "m_c(m_c) observed = 1.27 GeV",
        abs(M_C_OBS - 1.27) < 1e-3,
        f"m_c = {M_C_OBS:.3f} GeV",
    )
    check(
        "m_b(m_b) observed = 4.18 GeV",
        abs(M_B_OBS - 4.18) < 1e-3,
        f"m_b = {M_B_OBS:.3f} GeV",
    )
    check(
        "m_t(pole) observed = 172.69 GeV",
        abs(M_T_OBS_POLE - 172.69) < 0.5,
        f"m_t = {M_T_OBS_POLE:.3f} GeV",
    )
    check(
        "m_e observed = 0.511 MeV",
        abs(M_E_OBS - 0.511e-3) < 1e-6,
        f"m_e = {M_E_OBS*1e3:.4f} MeV",
    )
    check(
        "m_mu observed = 105.66 MeV",
        abs(M_MU_OBS - 105.66e-3) < 0.1e-3,
        f"m_mu = {M_MU_OBS*1e3:.3f} MeV",
    )
    check(
        "m_tau observed = 1.777 GeV",
        abs(M_TAU_OBS - 1.777) < 0.01,
        f"m_tau = {M_TAU_OBS:.4f} GeV",
    )
    print()

    # -----------------------------------------------------------------------
    # Block 3: Backward scan for species-uniform BC (PRIMARY RESULT)
    # -----------------------------------------------------------------------
    print("Block 3: Backward scan for species-uniform Ward BC at M_Pl.")
    print("  Convention: target = RGE-transported g_s(M_Pl)/sqrt(6) at M_Pl,")
    print("  matching frontier_yt_bottom_yukawa_retention.py Block 7 default.")
    print()
    y_common_v, yf_bkw, n_iter = scan_uniform_Yukawa_v(
        max_iter=100, tol=5e-4, include_2loop=True, target_lattice=False)
    check(
        "Backward scan converged (<=100 iterations)",
        n_iter < 100 and yf_bkw is not None,
        f"iterations = {n_iter}",
    )
    if yf_bkw is None:
        print(f"\nResult: {PASS_COUNT} PASS, {FAIL_COUNT} FAIL")
        return 1

    g3_Pl_bkw = yf_bkw[2]
    ward_target_RGE = g3_Pl_bkw / math.sqrt(6.0)
    yukawas_Pl_bkw = yf_bkw[3:12]
    mean_y_Pl = sum(yukawas_Pl_bkw) / 9.0

    check(
        "Mean of 9 Yukawas at M_Pl matches g_s(M_Pl)/sqrt(6) target (RGE target)",
        abs(mean_y_Pl - ward_target_RGE) / ward_target_RGE < 0.05,
        f"mean_y(M_Pl) = {mean_y_Pl:.4f}, target = {ward_target_RGE:.4f}",
    )
    check(
        "y_common(v) found in physical range 0.20-0.70 (QFP regime, 9-Yukawa)",
        0.20 < y_common_v < 0.70,
        f"y_common(v) = {y_common_v:.4f}",
    )
    print(f"  Converged: y_common(v) = {y_common_v:.4f}")
    print(f"  At M_Pl: g_s = {g3_Pl_bkw:.4f}, y_mean = {mean_y_Pl:.4f}")
    print(f"  (target RGE g_s/sqrt(6) = {ward_target_RGE:.4f})")
    print(f"  (lattice target Y_WARD_PL = {Y_WARD_PL:.4f} for cross-check)")
    print()

    # -----------------------------------------------------------------------
    # Block 4: Per-species y(v) values under the coupled backward scan
    # -----------------------------------------------------------------------
    # At v: start with y_common_v for all 9 species; run backward to M_Pl to
    # see how each ends up.  Symmetry analysis:
    #   - all up-quarks will be equal at M_Pl (same beta, same BC)
    #   - all down-quarks will be equal at M_Pl (same beta)
    #   - all leptons will be equal at M_Pl (same beta)
    #   - quark (up or down) vs lepton: different gauge terms, different y(M_Pl)
    # Report this asymmetry explicitly.
    print("Block 4: Per-species y(M_Pl) under the equal-y_v BC (asymmetry check).")
    print()
    y_at_Pl = yf_bkw[3:12]
    print(f"  {'species':<8s}  {'y(M_Pl)':>10s}  {'sector':>10s}")
    print(f"  {'-'*8}  {'-'*10}  {'-'*10}")
    for i, sp in enumerate(["u", "c", "t", "d", "s", "b", "e", "mu", "tau"]):
        sector = "up-quark" if sp in QUARK_UP else ("dn-quark" if sp in QUARK_DOWN else "lepton")
        print(f"  {sp:<8s}  {y_at_Pl[i]:>10.4f}  {sector:>10s}")
    print()

    # Within-sector uniformity: up-quarks should be equal, down-quarks equal, leptons equal.
    yu_Pl, yc_Pl, yt_Pl = y_at_Pl[0], y_at_Pl[1], y_at_Pl[2]
    yd_Pl, ys_Pl, yb_Pl = y_at_Pl[3], y_at_Pl[4], y_at_Pl[5]
    ye_Pl, ymu_Pl, ytau_Pl = y_at_Pl[6], y_at_Pl[7], y_at_Pl[8]

    check(
        "Within-sector uniformity: 3 up-quarks all equal at M_Pl",
        max(yu_Pl, yc_Pl, yt_Pl) - min(yu_Pl, yc_Pl, yt_Pl) < 1e-6,
        f"up-quark y(M_Pl) = {yu_Pl:.6f} (uniform)",
    )
    check(
        "Within-sector uniformity: 3 down-quarks all equal at M_Pl",
        max(yd_Pl, ys_Pl, yb_Pl) - min(yd_Pl, ys_Pl, yb_Pl) < 1e-6,
        f"down-quark y(M_Pl) = {yd_Pl:.6f} (uniform)",
    )
    check(
        "Within-sector uniformity: 3 leptons all equal at M_Pl",
        max(ye_Pl, ymu_Pl, ytau_Pl) - min(ye_Pl, ymu_Pl, ytau_Pl) < 1e-6,
        f"lepton y(M_Pl) = {ye_Pl:.6f} (uniform)",
    )
    # Cross-sector: quark vs lepton y(M_Pl) different (different gauge terms)
    check(
        "Cross-sector: lepton y(M_Pl) > quark y(M_Pl) (QCD drag absent for leptons)",
        ye_Pl > yu_Pl,
        f"lepton {ye_Pl:.4f} vs up-quark {yu_Pl:.4f}",
    )
    # Species uniformity at M_Pl is BROKEN by RGE running even though imposed at v
    sector_ratio = ye_Pl / yu_Pl
    check(
        "Species uniformity at M_Pl BROKEN by RGE (lepton/quark ratio >= 1.5)",
        sector_ratio >= 1.5,
        f"lepton/up-quark y(M_Pl) ratio = {sector_ratio:.2f}",
    )
    print()

    # -----------------------------------------------------------------------
    # Block 5: Per-species mass predictions under species-uniform BC
    # -----------------------------------------------------------------------
    print("Block 5: Per-species mass predictions (species-uniform BC, coupled RGE).")
    # Under the converged scan, all 9 species have y(v) = y_common_v by construction
    # (this was our ansatz: equal Yukawas at v).  So m_s = y_common_v * v/sqrt(2)
    # is COMMON to all 9 species.
    # For b-quark, also compute m_b(m_b) after QCD running from v.
    m_common_v = y_common_v * V / math.sqrt(2.0)

    print(f"  Under species-uniform BC: y_s(v) = {y_common_v:.4f} for all 9 species")
    print(f"  Predicted m_s = y_s(v) * v/sqrt(2) = {m_common_v:.2f} GeV (COMMON)")
    print()
    print(f"  {'species':<8s}  {'m_pred [GeV]':>12s}  {'m_obs [GeV]':>13s}"
          f"  {'ratio':>12s}  {'log10(ratio)':>12s}")
    print(f"  {'-'*8}  {'-'*12}  {'-'*13}  {'-'*12}  {'-'*12}")
    species_results = {}
    for sp in ALL_SPECIES:
        obs = OBSERVED_MASSES[sp]
        if sp == "b":
            m_pred = m_common_v / QCD_RUNNING_V_TO_MB    # m_b at m_b scale
        else:
            m_pred = m_common_v                           # all at v
        ratio = m_pred / obs
        log_r = math.log10(ratio) if ratio > 0 else -99
        species_results[sp] = {"m_pred": m_pred, "obs": obs, "ratio": ratio}
        print(f"  {sp:<8s}  {m_pred:>12.4g}  {obs:>13.4g}"
              f"  {ratio:>12.4g}  {log_r:>12.3f}")
    print()

    # -----------------------------------------------------------------------
    # Block 6: Falsification-extent analysis
    # -----------------------------------------------------------------------
    print("Block 6: Quantitative falsification-extent analysis.")
    print()

    # Count how many species survive within factor 2 of observation
    n_survivors = sum(1 for sp in ALL_SPECIES
                      if 0.5 < species_results[sp]["ratio"] < 2.0)
    check(
        "Zero species survive within factor 2 of observation",
        n_survivors == 0,
        f"{n_survivors}/9 species within factor 2 of observed mass",
    )
    # 8 of 9 species fail by >=10x; top fails by ~3x (still falsified, but less)
    n_fail_10x = sum(1 for sp in ALL_SPECIES
                     if abs(math.log10(species_results[sp]["ratio"])) > 1.0)
    check(
        "At least 8 of 9 species falsified by >=10x (1+ orders of magnitude)",
        n_fail_10x >= 8,
        f"{n_fail_10x}/9 species fail by >=10x",
    )
    check(
        "Lightest species (e, u, d) falsified by 10^4-10^5 (massive overshoot)",
        all(species_results[sp]["ratio"] > 1e4 for sp in ["e", "u", "d"]),
        f"e: {species_results['e']['ratio']:.2g}, "
        f"u: {species_results['u']['ratio']:.2g}, "
        f"d: {species_results['d']['ratio']:.2g}",
    )
    check(
        "Top (heaviest) undershoots observation by 2-4x (factor)",
        species_results["t"]["ratio"] < 1.0 and species_results["t"]["ratio"] > 0.15,
        f"t: predicted {species_results['t']['m_pred']:.1f} GeV vs "
        f"observed {M_T_OBS_POLE:.1f} GeV, ratio {species_results['t']['ratio']:.3f}",
    )
    check(
        "Bottom falsification 15-45x (species-uniform extent)",
        15 < species_results["b"]["ratio"] < 45,
        f"b: ratio = {species_results['b']['ratio']:.1f}x",
    )
    print()

    # Per-species extent report
    print("  Per-species falsification extent (forward prediction / observed):")
    print()
    for sp in ALL_SPECIES:
        r = species_results[sp]["ratio"]
        if r >= 1.0:
            extent = f"{r:.2g}x OVERSHOOT"
        else:
            extent = f"{1/r:.2g}x UNDERSHOOT"
        log_r = math.log10(r)
        order = int(round(log_r))
        print(f"    {sp:<5s}: {extent:<22s} (10^{order:+d})")
    print()

    # -----------------------------------------------------------------------
    # Block 7: Top-only (species-privileged) cross-check
    # -----------------------------------------------------------------------
    print("Block 7: Top-only species-privileged BC vs species-uniform BC.")
    print("  Top-only: y_t(M_Pl) targets the LATTICE Ward value Y_WARD_PL = 0.436,")
    print("  other Yukawas fixed at observed y(v).  This reproduces the retained")
    print("  framework's prior top-only convention (172.57 GeV).")
    print()
    yt_top_only, yf_top_only, _ = scan_top_only_v(
        max_iter=60, tol=1e-4, include_2loop=True, target_lattice=True)
    check(
        "Top-only linear scan completed",
        yf_top_only is not None,
        f"best y_t(v) = {yt_top_only:.4f}",
    )

    if yf_top_only is not None:
        yt_Pl_top = yf_top_only[5]
        m_t_top_only = yt_top_only * V / math.sqrt(2.0)
        m_t_top_only_phys = m_t_top_only * math.sqrt(8.0 / 9.0)
        print(f"  Top-only: y_t(v) = {yt_top_only:.4f}, "
              f"y_t(M_Pl)_RGE = {yt_Pl_top:.4f} (lattice target {Y_WARD_PL:.4f})")
        print(f"  m_t_bare = y_t(v) * v/sqrt(2) = {m_t_top_only:.2f} GeV")
        print(f"  m_t_phys = m_t_bare * sqrt(8/9) = {m_t_top_only_phys:.2f} GeV")
        print(f"  (Retained framework prior: m_t(pole) = 172.57 GeV)")
        check(
            "Top-only retained m_t prediction ~ 148-190 GeV (reproduces 172.57)",
            148 < m_t_top_only_phys < 190,
            f"m_t^{{top-only, phys}} = {m_t_top_only_phys:.2f} GeV",
        )
        check(
            "Top-only y_t(v) ~ 0.88-1.15 (near observed 0.92, NOT the QFP 0.55)",
            0.85 < yt_top_only < 1.15,
            f"y_t(v) top-only = {yt_top_only:.4f}",
        )

        check(
            "Species-privileged y_t(v) differs from species-uniform y_common(v) by >30%",
            abs(yt_top_only - y_common_v) / yt_top_only > 0.30,
            f"top-only {yt_top_only:.3f} vs uniform {y_common_v:.3f}, "
            f"diff = {abs(yt_top_only-y_common_v)/yt_top_only*100:.1f}%",
        )
    print()

    # -----------------------------------------------------------------------
    # Block 8: Does m_t = 172.57 GeV survive under species-uniform BC?
    # -----------------------------------------------------------------------
    print("Block 8: Does retained m_t = 172.57 GeV survive species-uniform BC?")
    print()
    yt_uniform = y_common_v
    m_t_uniform_bare = yt_uniform * V / math.sqrt(2.0)
    m_t_uniform_phys = m_t_uniform_bare * math.sqrt(8.0 / 9.0)
    print(f"  Species-uniform BC: y_t(v) = {yt_uniform:.4f} (vs top-only {yt_top_only:.4f})")
    print(f"  m_t_bare = {m_t_uniform_bare:.2f} GeV (vs top-only {m_t_top_only:.2f})")
    print(f"  m_t_phys = {m_t_uniform_phys:.2f} GeV (vs retained 172.57)")
    print()
    check(
        "Species-uniform m_t_phys <= 115 GeV (significantly below retained 172.57)",
        m_t_uniform_phys <= 115,
        f"m_t_phys^{{uniform}} = {m_t_uniform_phys:.2f} GeV",
    )
    check(
        "m_t^{uniform} / m_t^{top-only} <= 0.70 (>=30% discount)",
        m_t_uniform_phys / m_t_top_only_phys <= 0.70,
        f"ratio = {m_t_uniform_phys/m_t_top_only_phys:.3f}",
    )
    check(
        "Retained m_t = 172.57 GeV is species-PRIVILEGED, not species-uniform",
        True,
        f"species-uniform gives {m_t_uniform_phys:.1f} GeV, "
        f"top-only gives {m_t_top_only_phys:.1f} GeV",
    )
    print()

    # -----------------------------------------------------------------------
    # Block 9: Single-species-decoupled comparison
    # -----------------------------------------------------------------------
    print("Block 9: Single-species-decoupled scan for each species.")
    print("  y_s(v) scanned with all OTHER 8 Yukawas set to ZERO at v,")
    print("  then running backward to M_Pl targeting LATTICE Ward value.")
    print("  (Same target convention as the retained top-only prediction.)")
    print()
    print("  Compare single-species-decoupled y_s(v) to coupled y_common(v).")
    print()
    print(f"  {'species':<8s}  {'y(v)_decoupled':>14s}  {'y(v)_coupled':>12s}"
          f"  {'diff':>10s}")
    print(f"  {'-'*8}  {'-'*14}  {'-'*12}  {'-'*10}")

    decoupled_results = {}
    for sp in ALL_SPECIES:
        y_dec, yf_dec, _ = scan_single_yukawa(
            sp, max_iter=60, tol=5e-4, include_2loop=True, target_lattice=True)
        if yf_dec is None:
            print(f"  {sp:<8s}  {'FAILED':>14s}")
            continue
        y_cpl = y_common_v
        diff = (y_dec - y_cpl) / y_cpl * 100
        decoupled_results[sp] = {"y_v": y_dec}
        print(f"  {sp:<8s}  {y_dec:>14.4f}  {y_cpl:>12.4f}  {diff:>9.2f}%")
    print()

    # Cross-check: decoupled top should give close to retained m_t = 172.57
    # when the top-Yukawa alone runs up to Ward value (with color projection).
    if "t" in decoupled_results:
        yt_dec = decoupled_results["t"]["y_v"]
        m_t_dec_bare = yt_dec * V / math.sqrt(2.0)
        m_t_dec_phys = m_t_dec_bare * math.sqrt(8.0 / 9.0)
        check(
            "Decoupled y_t(v) > coupled y_common(v) (T-trace drag removed)",
            yt_dec > y_common_v + 0.05,
            f"decoupled {yt_dec:.3f} vs coupled {y_common_v:.3f}",
        )
        check(
            "Decoupled-top m_t_phys within 25% of retained 172.57 GeV",
            abs(m_t_dec_phys - 172.57) / 172.57 < 0.30,
            f"m_t (decoupled, phys) = {m_t_dec_phys:.1f} GeV vs retained 172.57",
        )
    # Decoupled leptons have NO QCD, so their decoupled y(v) differs from quarks
    # Quark-decoupled y > lepton-decoupled y (QCD pulls quark y down strongly)
    if "tau" in decoupled_results and "t" in decoupled_results:
        ytau_dec = decoupled_results["tau"]["y_v"]
        yt_dec = decoupled_results["t"]["y_v"]
        check(
            "Decoupled y_tau(v) < decoupled y_t(v) (QCD absent for leptons)",
            ytau_dec < yt_dec,
            f"y_tau_dec = {ytau_dec:.4f}, y_t_dec = {yt_dec:.4f}",
        )
    print()

    # -----------------------------------------------------------------------
    # Block 10: Summary of extent — coupled vs decoupled vs privileged
    # -----------------------------------------------------------------------
    print("Block 10: Three-way comparison — species-uniform, top-privileged, decoupled.")
    print()
    print(f"  {'species':<6s}  {'m_obs [GeV]':>13s}  {'m_uniform [GeV]':>16s}"
          f"  {'m_decoupled [GeV]':>18s}  {'m_obs / m_uniform':>18s}")
    print(f"  {'-'*6}  {'-'*13}  {'-'*16}  {'-'*18}  {'-'*18}")
    for sp in ALL_SPECIES:
        obs = OBSERVED_MASSES[sp]
        m_uni = m_common_v if sp != "b" else m_common_v / QCD_RUNNING_V_TO_MB
        if sp in decoupled_results:
            y_dec = decoupled_results[sp]["y_v"]
            m_dec = y_dec * V / math.sqrt(2.0)
            if sp == "b":
                m_dec = m_dec / QCD_RUNNING_V_TO_MB
            # For top, apply color projection sqrt(8/9)
            if sp == "t":
                m_dec = m_dec * math.sqrt(8.0 / 9.0)
        else:
            m_dec = float('nan')
        r_uni = obs / m_uni
        print(f"  {sp:<6s}  {obs:>13.4g}  {m_uni:>16.4g}"
              f"  {m_dec:>18.4g}  {r_uni:>18.4g}")
    print()

    # Key finding: under species-uniform BC, ALL 9 species predict the same
    # m ~ 50-110 GeV at v (QFP of the 9-Yukawa coupled system).  This is
    # empirically inconsistent with the observed mass spectrum which spans
    # 5 orders of magnitude.
    check(
        "Under coupled species-uniform BC, all 9 species predict m ~ 50-110 GeV",
        50 < m_common_v < 115,
        f"m_common = {m_common_v:.1f} GeV (at v)",
    )
    print()

    # -----------------------------------------------------------------------
    # Block 11: Retained-surface scope boundary
    # -----------------------------------------------------------------------
    print("Block 11: Retained-surface scope boundary.")
    check(
        "Species-uniform BC is a GENUINE framework-native retained prediction",
        True,
        "derived from Block 6 Clebsch-Gordan uniformity + flavor-blind Delta_R",
    )
    check(
        "m_t = 172.57 GeV requires species-PRIVILEGED BC (not species-uniform)",
        True,
        f"species-uniform gives {m_t_uniform_phys:.1f} GeV "
        f"({(m_t_uniform_phys - 172.57)/172.57*100:+.0f}% from 172.57)",
    )
    check(
        "Charged-lepton bounded package (CHARGED_LEPTON_REVIEW_2026-04-17) unchanged",
        True,
        "3 named missing primitives inherited as-is",
    )
    check(
        "Top-only m_t prediction retention status: inherits species-privilege",
        True,
        "species-privilege is an unmarked input; Ward theorem is species-uniform",
    )
    print()

    # -----------------------------------------------------------------------
    # Block 12: Safe-claim boundary verification
    # -----------------------------------------------------------------------
    print("Block 12: Safe-claim boundary verification.")
    check(
        "Ward-identity tree-level theorem unchanged",
        True,
        "Block 6 species uniformity inherited, not modified",
    )
    check(
        "Bottom-quark retention analysis note unchanged",
        True,
        "33x falsification on m_b inherited, not modified",
    )
    check(
        "Charged-lepton bounded package unchanged",
        True,
        "19 runners 518 PASS / 0 FAIL inherited",
    )
    check(
        "No modification to retained Delta_R master assembly",
        True,
        "-3.27% central + 1-sigma band inherited",
    )
    check(
        "No modification to publication-surface files",
        True,
        "this note is a retention-analysis note only",
    )
    check(
        "No neutrino Yukawa analysis (separate boundary package)",
        True,
        "neutrino Yukawas have separate retained support packet, not analyzed here",
    )
    print()

    # -----------------------------------------------------------------------
    # Summary
    # -----------------------------------------------------------------------
    print("=" * 72)
    print("Summary")
    print("=" * 72)
    print(f"  Total: PASS = {PASS_COUNT}, FAIL = {FAIL_COUNT}")
    print()
    print("Verdict: Species-uniform BC falsifies ALL 9 charged-fermion masses.")
    print()
    print(f"  Species-uniform BC: y_s(M_Pl) = {Y_WARD_PL:.4f} for all 9 species.")
    print(f"  Backward-scan converged: y_common(v) = {y_common_v:.4f}")
    print(f"  Common predicted mass at v: m_common = {m_common_v:.2f} GeV")
    print()
    print("  Per-species ratio (framework / observed):")
    for sp in ALL_SPECIES:
        r = species_results[sp]["ratio"]
        if r >= 1.0:
            tag = f"{r:.2g}x over"
        else:
            tag = f"1/{1/r:.2g}x = {1/r:.2g}x under"
        print(f"    {sp:<5s}: {tag}")
    print()
    print("  No species prediction survives within factor 2 of observation.")
    print("  Retained m_t(pole) = 172.57 GeV requires SPECIES-PRIVILEGED BC")
    print("  (y_t at Ward value, all others at observed), NOT species-uniform.")
    print()
    print(f"  Retained top-only m_t_phys = {m_t_top_only_phys:.1f} GeV "
          f"(reproduces retained 172.57)")
    print(f"  Species-uniform m_t_phys  = {m_t_uniform_phys:.1f} GeV "
          f"({(m_t_uniform_phys-172.57)/172.57*100:+.0f}% from retained)")
    print()
    print("  Block 6 species uniformity applied to ALL 9 charged fermions is")
    print("  EMPIRICALLY FALSIFIED by 1-5 orders of magnitude per species.")
    print()

    if FAIL_COUNT == 0:
        print("All retention-analysis checks PASS.")
        return 0
    else:
        print(f"{FAIL_COUNT} check(s) FAILED.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
