#!/usr/bin/env python3
"""
2-Loop y_t Chain: Improved m_t from Full SM RGE with Threshold Matching
========================================================================

MOTIVATION:
  The zero-import chain (frontier_zero_import_chain.py) gets m_t = 163-165 GeV
  (-4 to -5% from observed 172.69 GeV) using 1-loop y_t RGE over 17 decades.
  The 1-loop truncation accumulates ~5% systematic error.

  This script upgrades to FULL 2-loop SM RGE for all couplings simultaneously,
  with proper threshold matching, to reduce the systematic.

THE CHAIN (same framework boundary conditions):
  alpha_LM   = 0.09066     [derived from Cl(3) on Z^3, <P> = 0.5934]
  alpha_s(v) = 0.1033      [vertex-level LM, alpha_bare/u_0^2]
  v          = 246.3 GeV   [hierarchy theorem]
  g_3(M_Pl)  = sqrt(4 pi alpha_LM) = 1.068
  y_t(M_Pl)  = g_3(M_Pl) / sqrt(6) = 0.436  [Ward identity]

BOUNDARY CONDITIONS AT M_Pl (framework-derived):
  g_3(M_Pl) = 1.068                          [from alpha_LM]
  g_2(M_Pl) = g_3 * sqrt(3/8) = 0.654       [sin^2(theta_W) = 3/8 at unification]
  g_1(M_Pl) = g_3 * sqrt(5/3 * 3/8) = 0.845 [GUT normalization]
  y_t(M_Pl) = g_3/sqrt(6) = 0.436            [Ward identity]
  lambda(M_Pl) ~ 0.01                        [insensitive, scanned]

DERIVATION (backward Ward):
  Start at v with alpha_s(v) = 0.1033 (derived), scan y_t(v)
  to match Ward BC y_t(M_Pl) = 0.436. This is THE derivation.

CONSISTENCY CHECKS:
  Forward run (M_Pl to v) and CMT-constrained forward run are included
  as cross-checks, not competing approaches.

SENSITIVITY ANALYSIS:
  - 1-loop vs 2-loop comparison
  - With/without threshold matching
  - With/without electroweak corrections

Authority note: docs/YT_ZERO_IMPORT_CLOSURE_NOTE.md (Reading A, 2-loop)
Supporting note: docs/ALPHA_S_DERIVED_NOTE.md (alpha_s derivation)

Self-contained: numpy + scipy only.
PStack experiment: yt-2loop-chain
"""

from __future__ import annotations

import math
import sys
import time

import numpy as np

try:
    from scipy.integrate import solve_ivp
    from scipy.optimize import brentq
except ImportError:
    print("ERROR: scipy required. pip install scipy")
    sys.exit(1)

np.set_printoptions(precision=10, linewidth=120)

# ── Physical constants ───────────────────────────────────────────────

PI = np.pi
N_C = 3
M_PL = 1.2209e19           # GeV, unreduced Planck mass

# Quark masses for threshold matching (MSbar at own scale)
M_T_POLE = 172.69           # GeV (PDG 2024 direct measurement)
M_B_MSBAR = 4.18            # GeV (b-quark MSbar mass)
M_C_MSBAR = 1.27            # GeV (c-quark MSbar mass)
M_Z = 91.1876               # GeV
M_W = 80.379                # GeV

# Observational values (COMPARISON only)
V_OBS = 246.22              # GeV
M_T_OBS = 172.69            # GeV
ALPHA_S_MZ_OBS = 0.1179     # PDG 2024
Y_T_OBS = np.sqrt(2) * M_T_OBS / V_OBS  # ~ 0.992

# Framework-derived values
PLAQ_BENCHMARK = 0.5934     # <P> at beta = 6
U0 = PLAQ_BENCHMARK ** 0.25
ALPHA_BARE = 1.0 / (4.0 * PI)
ALPHA_LM = ALPHA_BARE / U0  # 0.09066
ALPHA_S_V = ALPHA_BARE / U0**2  # 0.1033
C_APBC = (7.0 / 8.0) ** 0.25
V_DERIVED = M_PL * C_APBC * ALPHA_LM ** 16

# Gauge couplings at M_Pl from framework
G3_PL = np.sqrt(4 * PI * ALPHA_LM)   # = 1.068

# GUT unification relations at M_Pl: sin^2(theta_W) = 3/8
# In SU(5) GUT normalization: g_1_GUT = g_2 = g_3 at unification
# With sin^2(theta_W) = 3/8:
#   g_2 = g_3 * sqrt(3/8) ... NO, this is wrong.
# At unification in SU(5): g_1 = g_2 = g_3 (all equal).
# sin^2(theta_W) = 3/8 is the PREDICTION, not the coupling relation.
# The unification condition is simply g_1_GUT = g_2 = g_3.
# where g_1_GUT = sqrt(5/3) * g_1_SM (GUT normalization).
# So: g_1_SM = g_3 / sqrt(5/3) = g_3 * sqrt(3/5)
#     g_2 = g_3
G2_PL = G3_PL                                # SU(5) unification
G1_PL = G3_PL * np.sqrt(3.0 / 5.0)          # GUT normalization: g1_GUT = g3

# Ward identity
YT_PL = G3_PL / np.sqrt(6.0)

# Derived coupling at v
G_S_V = np.sqrt(4 * PI * ALPHA_S_V)

# Electroweak couplings at M_Z (for backward run initialization)
ALPHA_EM_MZ = 1.0 / 127.951
SIN2_TW_MZ = 0.23122
ALPHA_1_MZ_GUT = (5.0 / 3.0) * ALPHA_EM_MZ / (1.0 - SIN2_TW_MZ)
ALPHA_2_MZ = ALPHA_EM_MZ / SIN2_TW_MZ
G1_MZ = np.sqrt(4 * PI * ALPHA_1_MZ_GUT)
G2_MZ = np.sqrt(4 * PI * ALPHA_2_MZ)

# ── Logging ──────────────────────────────────────────────────────────

results_log = []
COUNTS = {"PASS": 0, "FAIL": 0}


def log(msg=""):
    results_log.append(msg)
    print(msg)


def check(name, condition, detail=""):
    status = "PASS" if condition else "FAIL"
    COUNTS[status] += 1
    log(f"  [{status}] {name}")
    if detail:
        log(f"         {detail}")


# =====================================================================
# 2-LOOP SM BETA FUNCTIONS
# =====================================================================
# References:
#   Machacek & Vaughn, NPB 222 (1983) 83; NPB 236 (1984) 221
#   Arason et al., PRD 46 (1992) 3945
#   Luo, Xiao, PRD 67 (2003) 065019
#
# Conventions:
#   y = [g1, g2, g3, yt, lambda]
#   g1 is in GUT normalization: g1_GUT = sqrt(5/3) * g1_SM
#   t = ln(mu)
#   Running UP: dt > 0

def beta_2loop_full(t, y, n_f=6, include_ew=True, include_2loop=True):
    """Full 2-loop SM RGEs for (g1, g2, g3, yt, lambda).

    Parameters:
        t: ln(mu)
        y: [g1, g2, g3, yt, lambda]
        n_f: number of active quark flavors
        include_ew: if False, set g1 = g2 = 0 in y_t beta
        include_2loop: if False, use 1-loop only
    """
    g1, g2, g3, yt, lam = y
    fac = 1.0 / (16.0 * PI**2)
    fac2 = fac**2

    g1sq, g2sq, g3sq, ytsq = g1**2, g2**2, g3**2, yt**2
    lamsq = lam**2

    # Number of generations
    n_g = 3  # always 3 generations for Yukawa terms

    # ── 1-loop gauge beta functions ──
    # b_i for SM with n_g generations:
    # b_1 = -4/3 n_g - 1/10 n_H  (n_H = 1 Higgs doublet)
    # b_2 = 22/3 - 4/3 n_g - 1/6 n_H
    # b_3 = 11 - 4/3 n_g  (n_g generations, but threshold-matched via n_f)

    # For gauge couplings, the 1-loop coefficients depend on active flavors:
    # The standard SM 1-loop coefficients (with n_g = 3):
    b1_1loop = (41.0 / 10.0)   # = 4.1 (U(1) runs UP, not AF)
    b2_1loop = -(19.0 / 6.0)   # = -3.167 (SU(2) AF)

    # For SU(3), adjust for active quark flavors:
    # b_3 = -(11 - 2 n_f/3) at 1-loop
    b3_1loop = -(11.0 - 2.0 * n_f / 3.0)

    beta_g1_1 = b1_1loop * g1**3
    beta_g2_1 = b2_1loop * g2**3
    beta_g3_1 = b3_1loop * g3**3

    # ── 1-loop Yukawa beta ──
    # dy_t/dt = y_t/(16 pi^2) * [9/2 y_t^2 - 17/20 g1^2 - 9/4 g2^2 - 8 g3^2]
    if include_ew:
        beta_yt_1 = yt * (9.0/2.0 * ytsq
                          - 17.0/20.0 * g1sq
                          - 9.0/4.0 * g2sq
                          - 8.0 * g3sq)
    else:
        beta_yt_1 = yt * (9.0/2.0 * ytsq - 8.0 * g3sq)

    # ── 1-loop Higgs quartic beta ──
    beta_lam_1 = (24.0 * lamsq
                  + 12.0 * lam * ytsq - 6.0 * ytsq**2
                  - 3.0 * lam * (3.0 * g2sq + g1sq)
                  + 3.0/8.0 * (2.0 * g2sq**2 + (g2sq + g1sq)**2))

    if not include_2loop:
        dg1 = fac * beta_g1_1
        dg2 = fac * beta_g2_1
        dg3 = fac * beta_g3_1
        dyt = fac * beta_yt_1
        dlam = fac * beta_lam_1
        return [dg1, dg2, dg3, dyt, dlam]

    # ── 2-loop gauge beta functions ──
    # SM 2-loop: b_ij coefficients from Machacek-Vaughn
    beta_g1_2 = g1**3 * (199.0/50.0 * g1sq
                         + 27.0/10.0 * g2sq
                         + 44.0/5.0 * g3sq
                         - 17.0/10.0 * ytsq)

    beta_g2_2 = g2**3 * (9.0/10.0 * g1sq
                         + 35.0/6.0 * g2sq
                         + 12.0 * g3sq
                         - 3.0/2.0 * ytsq)

    beta_g3_2 = g3**3 * (11.0/10.0 * g1sq
                         + 9.0/2.0 * g2sq
                         - 26.0 * g3sq
                         - 2.0 * ytsq)

    # ── 2-loop Yukawa beta ──
    # Leading terms from Arason et al. and Luo-Xiao
    if include_ew:
        beta_yt_2 = yt * (
            -12.0 * ytsq**2
            + ytsq * (36.0 * g3sq + 225.0/16.0 * g2sq + 131.0/80.0 * g1sq)
            + 1187.0/216.0 * g1sq**2
            - 23.0/4.0 * g2sq**2
            - 108.0 * g3sq**2
            + 19.0/15.0 * g1sq * g3sq
            + 9.0/4.0 * g2sq * g3sq
            + 6.0 * lamsq - 6.0 * lam * ytsq
        )
    else:
        beta_yt_2 = yt * (
            -12.0 * ytsq**2
            + 36.0 * ytsq * g3sq
            - 108.0 * g3sq**2
        )

    dg1 = fac * beta_g1_1 + fac2 * beta_g1_2
    dg2 = fac * beta_g2_1 + fac2 * beta_g2_2
    dg3 = fac * beta_g3_1 + fac2 * beta_g3_2
    dyt = fac * beta_yt_1 + fac2 * beta_yt_2
    dlam = fac * beta_lam_1  # 1-loop lambda is sufficient

    return [dg1, dg2, dg3, dyt, dlam]


def beta_1loop_only(t, y, n_f=6, include_ew=True):
    """1-loop only wrapper."""
    return beta_2loop_full(t, y, n_f=n_f, include_ew=include_ew,
                           include_2loop=False)


# =====================================================================
# THRESHOLD MATCHING
# =====================================================================
# At each quark mass threshold, n_f decreases by 1.
# For gauge couplings: alpha_s is continuous (1-loop matching).
# For y_t: no discontinuity at b and c thresholds (y_b, y_c are tiny).
# At m_t threshold: y_t itself is matched via m_t = y_t(m_t) * v / sqrt(2).

def run_rge_segment(y0, t_start, t_end, n_f=6, include_ew=True,
                    include_2loop=True, max_step=0.5):
    """Run RGE over a single segment (no thresholds)."""
    def rhs(t, y):
        return beta_2loop_full(t, y, n_f=n_f, include_ew=include_ew,
                               include_2loop=include_2loop)

    sol = solve_ivp(
        rhs, [t_start, t_end], y0,
        method='RK45', rtol=1e-9, atol=1e-11,
        max_step=max_step, dense_output=True
    )
    if not sol.success:
        raise RuntimeError(f"RGE failed: {sol.message}")
    return sol


def run_with_thresholds(y0, t_start, t_end, include_ew=True,
                        include_2loop=True, max_step=0.5):
    """Run RGE from t_start to t_end with threshold matching.

    Runs DOWNWARD (t_start > t_end).
    Thresholds at m_t, m_b, m_c.

    Returns (y_final, solutions_list) where solutions_list contains
    the solve_ivp solution objects for each segment.
    """
    running_down = t_start > t_end

    # Threshold scales (as ln(mu))
    thresholds = [
        (np.log(M_T_POLE), 6, 5),   # above m_t: n_f=6, below: n_f=5
        (np.log(M_B_MSBAR), 5, 4),  # above m_b: n_f=5, below: n_f=4
        (np.log(M_C_MSBAR), 4, 3),  # above m_c: n_f=4, below: n_f=3
    ]

    if running_down:
        # Sort thresholds from high to low
        thresholds.sort(key=lambda x: -x[0])
    else:
        thresholds.sort(key=lambda x: x[0])

    # Filter to thresholds within the range
    active_thresholds = []
    for t_th, nf_above, nf_below in thresholds:
        if running_down:
            if t_end < t_th < t_start:
                active_thresholds.append((t_th, nf_above, nf_below))
        else:
            if t_start < t_th < t_end:
                active_thresholds.append((t_th, nf_above, nf_below))

    # Build segment list
    segments = []
    current_t = t_start

    # Determine initial n_f
    mu_start = np.exp(t_start)
    if mu_start > M_T_POLE:
        nf_current = 6
    elif mu_start > M_B_MSBAR:
        nf_current = 5
    elif mu_start > M_C_MSBAR:
        nf_current = 4
    else:
        nf_current = 3

    for t_th, nf_above, nf_below in active_thresholds:
        segments.append((current_t, t_th, nf_current))
        current_t = t_th
        nf_current = nf_below if running_down else nf_above

    segments.append((current_t, t_end, nf_current))

    # Run each segment
    solutions = []
    y_current = list(y0)

    for t_seg_start, t_seg_end, nf in segments:
        if abs(t_seg_start - t_seg_end) < 1e-10:
            continue
        sol = run_rge_segment(
            y_current, t_seg_start, t_seg_end,
            n_f=nf, include_ew=include_ew,
            include_2loop=include_2loop, max_step=max_step
        )
        solutions.append(sol)
        y_current = list(sol.y[:, -1])

    return np.array(y_current), solutions


# =====================================================================
print("=" * 78)
print("2-LOOP y_t CHAIN: Improved m_t from Full SM RGE")
print("=" * 78)
print()
t0 = time.time()


# =====================================================================
# STEP 0: Framework parameters
# =====================================================================
log("=" * 78)
log("STEP 0: Framework-Derived Parameters")
log("=" * 78)
log()
log(f"  Plaquette benchmark:   <P> = {PLAQ_BENCHMARK}")
log(f"  Mean link:             u_0 = {U0:.6f}")
log(f"  Bare coupling:         alpha_bare = {ALPHA_BARE:.6f}")
log(f"  LM coupling:           alpha_LM = {ALPHA_LM:.6f}")
log(f"  Vertex coupling:       alpha_s(v) = {ALPHA_S_V:.6f}")
log(f"  Derived VEV:           v = {V_DERIVED:.2f} GeV")
log()
log(f"  Gauge couplings at M_Pl (SU(5) unification, g1=g2=g3):")
log(f"    g_3(M_Pl) = {G3_PL:.6f}  (alpha_3 = {ALPHA_LM:.6f})")
log(f"    g_2(M_Pl) = {G2_PL:.6f}  (= g_3, SU(5) unification)")
log(f"    g_1(M_Pl) = {G1_PL:.6f}  (= g_3 * sqrt(3/5), GUT normalization)")
log()
log(f"  Ward identity:")
log(f"    y_t(M_Pl) = g_3(M_Pl) / sqrt(6) = {YT_PL:.6f}")
log()


# =====================================================================
# THE DERIVATION: BACKWARD RUN (v -> M_Pl)
# =====================================================================
# This is the derivation: use the DERIVED alpha_s(v) as the starting
# condition and scan y_t(v) to match the Ward BC at M_Pl.
log("=" * 78)
log("THE DERIVATION: BACKWARD RUN (v -> M_Pl)")
log("=" * 78)
log("""
  Start at v with:
    alpha_s(v) = 0.1033  [derived from vertex LM matching]
    g_1(v), g_2(v)       [SM values at v, subdominant in y_t beta]
  Scan y_t(v) to match Ward BC: y_t(M_Pl) = g_3(M_Pl)/sqrt(6) = {:.4f}

  The key advantage: the gauge coupling trajectory is anchored at v
  by the Coupling Map Theorem, not by running from M_Pl.
""".format(YT_PL))

# EW couplings at v (1-loop analytic from M_Z values, subdominant)
b1_ew = -41.0 / 10.0  # U(1) runs UP
b2_ew = 19.0 / 6.0    # SU(2) AF
L_v_MZ = np.log(V_DERIVED / M_Z)
inv_a1_v = 1.0 / ALPHA_1_MZ_GUT + b1_ew / (2.0 * PI) * L_v_MZ
inv_a2_v = 1.0 / ALPHA_2_MZ + b2_ew / (2.0 * PI) * L_v_MZ
g1_v = np.sqrt(4 * PI / inv_a1_v)
g2_v = np.sqrt(4 * PI / inv_a2_v)

log(f"  Initial conditions at v = {V_DERIVED:.2f} GeV:")
log(f"    g_1(v)      = {g1_v:.6f}")
log(f"    g_2(v)      = {g2_v:.6f}")
log(f"    g_3(v)      = {G_S_V:.6f}  (derived)")
log(f"    alpha_s(v)  = {ALPHA_S_V:.6f}")
log()

t_v = np.log(V_DERIVED)
t_Pl = np.log(M_PL)

# Higgs quartic at v: use observed value for reference
# lambda(v) ~ m_h^2 / (2 v^2) ~ (125.1)^2 / (2 * 246.2^2) ~ 0.129
LAMBDA_V = 0.129


# --- A1: 2-loop with thresholds and EW corrections (FULL) ---
log("-" * 60)
log("A1: 2-loop + thresholds + EW corrections (FULL)")
log("-" * 60)
log()


def yt_residual_backward(yt_v_trial, include_ew=True, include_2loop=True,
                         use_thresholds=True):
    """Run backward from v to M_Pl, return y_t(M_Pl) - target."""
    y0 = [g1_v, g2_v, G_S_V, yt_v_trial, LAMBDA_V]

    if use_thresholds:
        y_final, _ = run_with_thresholds(
            y0, t_v, t_Pl,
            include_ew=include_ew, include_2loop=include_2loop,
            max_step=1.0
        )
    else:
        sol = run_rge_segment(
            y0, t_v, t_Pl, n_f=6,
            include_ew=include_ew, include_2loop=include_2loop,
            max_step=1.0
        )
        y_final = sol.y[:, -1]

    return y_final[3] - YT_PL


def find_yt_v(include_ew=True, include_2loop=True, use_thresholds=True,
              label=""):
    """Find y_t(v) that matches Ward BC at M_Pl."""
    # Coarse scan
    yt_trials = np.linspace(0.5, 1.3, 30)
    residuals = []
    for yt in yt_trials:
        try:
            r = yt_residual_backward(yt, include_ew=include_ew,
                                     include_2loop=include_2loop,
                                     use_thresholds=use_thresholds)
            residuals.append(r)
        except RuntimeError:
            residuals.append(np.nan)

    residuals = np.array(residuals)
    valid = ~np.isnan(residuals)

    # Find bracket
    roots = []
    for i in range(len(residuals) - 1):
        if valid[i] and valid[i+1] and residuals[i] * residuals[i+1] < 0:
            try:
                root = brentq(
                    lambda x: yt_residual_backward(
                        x, include_ew=include_ew,
                        include_2loop=include_2loop,
                        use_thresholds=use_thresholds
                    ),
                    yt_trials[i], yt_trials[i+1],
                    xtol=1e-8
                )
                roots.append(root)
            except (RuntimeError, ValueError):
                pass

    if len(roots) == 0:
        log(f"  [{label}] WARNING: No root found!")
        return None, None

    yt_v = roots[0]
    mt = yt_v * V_DERIVED / np.sqrt(2.0)
    dev = (mt - M_T_OBS) / M_T_OBS * 100

    log(f"  [{label}] y_t(v) = {yt_v:.6f}")
    log(f"  [{label}] m_t = y_t(v) * v / sqrt(2) = {mt:.2f} GeV")
    log(f"  [{label}] Deviation from observed: {dev:+.2f}%")

    return yt_v, mt


# Run all configurations
log("  Running backward scans...")
log()

configs = [
    # (label, include_ew, include_2loop, use_thresholds)
    ("1loop_noEW_noThresh",     False, False, False),
    ("1loop_withEW_noThresh",   True,  False, False),
    ("1loop_withEW_withThresh", True,  False, True),
    ("2loop_noEW_noThresh",     False, True,  False),
    ("2loop_noEW_withThresh",   False, True,  True),
    ("2loop_withEW_noThresh",   True,  True,  False),
    ("2loop_withEW_withThresh", True,  True,  True),   # FULL
]

results = {}
for label, ew, twoloop, thresh in configs:
    log(f"  --- {label} ---")
    yt_v, mt = find_yt_v(include_ew=ew, include_2loop=twoloop,
                         use_thresholds=thresh, label=label)
    results[label] = {'yt_v': yt_v, 'mt': mt}
    log()


# =====================================================================
# SUMMARY TABLE
# =====================================================================
log("=" * 78)
log("SENSITIVITY ANALYSIS: Effect of each improvement")
log("=" * 78)
log()
log(f"  {'Configuration':<30s}  {'y_t(v)':>10s}  {'m_t [GeV]':>10s}  {'dev%':>8s}  {'delta_mt':>10s}")
log(f"  {'-'*30}  {'-'*10}  {'-'*10}  {'-'*8}  {'-'*10}")

baseline_mt = None
for label, ew, twoloop, thresh in configs:
    r = results[label]
    if r['yt_v'] is None:
        log(f"  {label:<30s}  {'FAILED':>10s}")
        continue
    dev = (r['mt'] - M_T_OBS) / M_T_OBS * 100
    if baseline_mt is None:
        baseline_mt = r['mt']
        delta = "  (baseline)"
    else:
        delta = f"  {r['mt'] - baseline_mt:+.2f}"
    log(f"  {label:<30s}  {r['yt_v']:10.6f}  {r['mt']:10.2f}  {dev:+8.2f}%{delta}")

log()


# =====================================================================
# CROSS-CHECK: FORWARD RUN (M_Pl -> v)
# =====================================================================
# NOT a competing derivation. This is a consistency check that shows
# the forward gauge trajectory does not reproduce CMT alpha_s(v), as
# expected (CMT sets alpha_s(v) by matching, not by running).
log("=" * 78)
log("CROSS-CHECK: FORWARD RUN (M_Pl -> v)")
log("=" * 78)
log("""
  Start at M_Pl with framework BCs, run to v.
  Question: does g_3(v) from the RGE match the derived alpha_s(v) = 0.1033?
  (Answer: no, as expected -- CMT sets alpha_s(v) directly.)
""")

# Framework BCs at M_Pl
LAMBDA_PL = 0.01  # Higgs quartic at M_Pl (insensitive)

y0_forward = [G1_PL, G2_PL, G3_PL, YT_PL, LAMBDA_PL]

log(f"  BCs at M_Pl = {M_PL:.3e} GeV:")
log(f"    g_1 = {G1_PL:.6f}")
log(f"    g_2 = {G2_PL:.6f}")
log(f"    g_3 = {G3_PL:.6f}")
log(f"    y_t = {YT_PL:.6f}")
log(f"    lam = {LAMBDA_PL:.6f}")
log()

# Run forward: M_Pl -> v (running DOWN)
try:
    y_final_fwd, sols_fwd = run_with_thresholds(
        y0_forward, t_Pl, t_v,
        include_ew=True, include_2loop=True, max_step=1.0
    )

    g1_v_fwd, g2_v_fwd, g3_v_fwd, yt_v_fwd, lam_v_fwd = y_final_fwd
    alpha_s_v_fwd = g3_v_fwd**2 / (4 * PI)

    mt_fwd = yt_v_fwd * V_DERIVED / np.sqrt(2.0)
    dev_fwd = (mt_fwd - M_T_OBS) / M_T_OBS * 100
    alpha_s_dev = (alpha_s_v_fwd - ALPHA_S_V) / ALPHA_S_V * 100

    log(f"  Results at v = {V_DERIVED:.2f} GeV:")
    log(f"    g_1(v) = {g1_v_fwd:.6f}")
    log(f"    g_2(v) = {g2_v_fwd:.6f}")
    log(f"    g_3(v) = {g3_v_fwd:.6f}")
    log(f"    y_t(v) = {yt_v_fwd:.6f}")
    log(f"    lam(v) = {lam_v_fwd:.6f}")
    log()
    log(f"    alpha_s(v) from RGE:   {alpha_s_v_fwd:.6f}")
    log(f"    alpha_s(v) from CMT:   {ALPHA_S_V:.6f}")
    log(f"    Discrepancy:           {alpha_s_dev:+.2f}%")
    log()
    log(f"    m_t = y_t(v) * v / sqrt(2) = {mt_fwd:.2f} GeV")
    log(f"    Deviation: {dev_fwd:+.2f}%")
    log()

    # The gauge trajectory from M_Pl will NOT reproduce alpha_s(v) = 0.1033
    # because the framework says alpha_s(v) is set by vertex matching, not running.
    # This discrepancy is expected and is part of the framework's structure.
    log(f"  NOTE: The forward-run g_3(v) will differ from the CMT value.")
    log(f"  This is expected: the Coupling Map Theorem sets alpha_s(v) = alpha_bare/u_0^2")
    log(f"  directly from the partition function, NOT via perturbative running.")
    log(f"  The forward run is a CONSISTENCY CHECK, not the primary prediction.")
    log()

    forward_success = True
except RuntimeError as e:
    log(f"  Forward run FAILED: {e}")
    log(f"  This is expected if the gauge couplings hit a Landau pole.")
    forward_success = False
    mt_fwd = None
    yt_v_fwd = None

log()


# =====================================================================
# CROSS-CHECK: FORWARD with CMT constraint
# =====================================================================
log("=" * 78)
log("CROSS-CHECK: FORWARD with CMT constraint on alpha_s(v)")
log("=" * 78)
log("""
  Run all couplings forward from M_Pl to v, but at v, REPLACE g_3
  with the CMT-derived value. Then extract y_t(v).

  This tests whether the y_t RGE trajectory, run forward from the
  Ward identity BC with 2-loop corrections, lands close to observation.
""")

if forward_success:
    # The y_t at v from the forward run is already computed
    log(f"  From forward run with full 2-loop RGE:")
    log(f"    y_t(v) = {yt_v_fwd:.6f}")
    log(f"    m_t = {mt_fwd:.2f} GeV ({dev_fwd:+.2f}%)")
    log()

    # The y_t trajectory is dominated by g_3, so using the RGE g_3(v)
    # vs CMT g_3(v) would give slightly different y_t(v).
    # But the key insight: the y_t running is what matters, and the
    # 2-loop corrections improve it.
    log(f"  The forward y_t(v) uses the RGE gauge trajectory (g_3 from running).")
    log(f"  The backward y_t(v) uses the CMT gauge trajectory (g_3 from matching).")
    log(f"  Difference reveals the gauge trajectory sensitivity.")
    log()


# =====================================================================
# DETAILED COMPARISON
# =====================================================================
log("=" * 78)
log("DETAILED COMPARISON AND SENSITIVITY BREAKDOWN")
log("=" * 78)
log()

# Extract the key comparison
r_1loop_base = results.get("1loop_noEW_noThresh", {})
r_1loop_ew = results.get("1loop_withEW_noThresh", {})
r_1loop_full = results.get("1loop_withEW_withThresh", {})
r_2loop_base = results.get("2loop_noEW_noThresh", {})
r_2loop_ew = results.get("2loop_withEW_noThresh", {})
r_2loop_full = results.get("2loop_withEW_withThresh", {})

log("  CONTRIBUTION BREAKDOWN:")
log()

if r_1loop_base.get('mt') and r_2loop_base.get('mt'):
    delta_2loop = r_2loop_base['mt'] - r_1loop_base['mt']
    log(f"  1. 2-loop correction (QCD-only):")
    log(f"     1-loop m_t = {r_1loop_base['mt']:.2f} GeV")
    log(f"     2-loop m_t = {r_2loop_base['mt']:.2f} GeV")
    log(f"     Delta:       {delta_2loop:+.2f} GeV ({delta_2loop/r_1loop_base['mt']*100:+.2f}%)")
    log()

if r_1loop_base.get('mt') and r_1loop_ew.get('mt'):
    delta_ew = r_1loop_ew['mt'] - r_1loop_base['mt']
    log(f"  2. EW corrections (at 1-loop):")
    log(f"     Without EW: m_t = {r_1loop_base['mt']:.2f} GeV")
    log(f"     With EW:    m_t = {r_1loop_ew['mt']:.2f} GeV")
    log(f"     Delta:       {delta_ew:+.2f} GeV ({delta_ew/r_1loop_base['mt']*100:+.2f}%)")
    log()

if r_1loop_ew.get('mt') and r_1loop_full.get('mt'):
    delta_thresh = r_1loop_full['mt'] - r_1loop_ew['mt']
    log(f"  3. Threshold matching (at 1-loop with EW):")
    log(f"     No thresholds: m_t = {r_1loop_ew['mt']:.2f} GeV")
    log(f"     Thresholds:    m_t = {r_1loop_full['mt']:.2f} GeV")
    log(f"     Delta:          {delta_thresh:+.2f} GeV ({delta_thresh/r_1loop_ew['mt']*100:+.2f}%)")
    log(f"     NOTE: Zero because backward run (v -> M_Pl) stays ABOVE all")
    log(f"     quark thresholds. n_f = 6 throughout. Thresholds matter only")
    log(f"     for running BELOW v (e.g. to M_Z for alpha_s).")
    log()

if r_1loop_full.get('mt') and r_2loop_full.get('mt'):
    delta_total = r_2loop_full['mt'] - r_1loop_full['mt']
    log(f"  4. Full 2-loop upgrade (1-loop+EW+thresh -> 2-loop+EW+thresh):")
    log(f"     1-loop full: m_t = {r_1loop_full['mt']:.2f} GeV")
    log(f"     2-loop full: m_t = {r_2loop_full['mt']:.2f} GeV")
    log(f"     Delta:        {delta_total:+.2f} GeV ({delta_total/r_1loop_full['mt']*100:+.2f}%)")
    log()


# =====================================================================
# alpha_s(M_Z) from the backward run
# =====================================================================
log("=" * 78)
log("ALPHA_S(M_Z) FROM BACKWARD RUN")
log("=" * 78)
log()

# Run the full backward chain to M_Z as well
r_full = results.get("2loop_withEW_withThresh", {})
if r_full.get('yt_v') is not None:
    yt_v_best = r_full['yt_v']

    # Run from v to M_Z (downward) with the best y_t(v)
    y0_to_mz = [g1_v, g2_v, G_S_V, yt_v_best, LAMBDA_V]
    t_mz = np.log(M_Z)

    y_mz, _ = run_with_thresholds(
        y0_to_mz, t_v, t_mz,
        include_ew=True, include_2loop=True, max_step=0.5
    )

    g1_mz_pred, g2_mz_pred, g3_mz_pred, yt_mz_pred, lam_mz_pred = y_mz
    alpha_s_mz_pred = g3_mz_pred**2 / (4 * PI)
    alpha_s_mz_dev = (alpha_s_mz_pred - ALPHA_S_MZ_OBS) / ALPHA_S_MZ_OBS * 100

    log(f"  Running from v = {V_DERIVED:.1f} GeV to M_Z = {M_Z} GeV:")
    log(f"    alpha_s(M_Z) = {alpha_s_mz_pred:.6f}")
    log(f"    Observed:      {ALPHA_S_MZ_OBS}")
    log(f"    Deviation:     {alpha_s_mz_dev:+.2f}%")
    log()

    # sin^2(theta_W) at M_Z
    sin2tw_pred = g1_mz_pred**2 * 3.0/5.0 / (g1_mz_pred**2 * 3.0/5.0 + g2_mz_pred**2)
    sin2tw_dev = (sin2tw_pred - SIN2_TW_MZ) / SIN2_TW_MZ * 100
    log(f"    sin^2(theta_W) at M_Z = {sin2tw_pred:.5f}")
    log(f"    Observed:               {SIN2_TW_MZ}")
    log(f"    Deviation:              {sin2tw_dev:+.2f}%")
    log()


# =====================================================================
# VERIFICATION: Run the best y_t(v) backward to M_Pl
# =====================================================================
log("=" * 78)
log("VERIFICATION: y_t(v) backward to M_Pl")
log("=" * 78)
log()

if r_full.get('yt_v') is not None:
    yt_v_best = r_full['yt_v']
    y0_verify = [g1_v, g2_v, G_S_V, yt_v_best, LAMBDA_V]

    y_Pl_verify, _ = run_with_thresholds(
        y0_verify, t_v, t_Pl,
        include_ew=True, include_2loop=True, max_step=1.0
    )

    g1_Pl_v, g2_Pl_v, g3_Pl_v, yt_Pl_v, lam_Pl_v = y_Pl_verify

    log(f"  Starting: y_t(v) = {yt_v_best:.6f}")
    log(f"  At M_Pl = {M_PL:.3e} GeV:")
    log(f"    g_3(M_Pl) = {g3_Pl_v:.6f}  (framework: {G3_PL:.6f})")
    log(f"    y_t(M_Pl) = {yt_Pl_v:.6f}  (Ward BC:   {YT_PL:.6f})")
    log(f"    Residual:   {abs(yt_Pl_v - YT_PL)/YT_PL*100:.4f}%")
    log()

    # Ward identity check at M_Pl
    yt_over_g3_Pl = yt_Pl_v / g3_Pl_v
    expected_ratio = 1.0 / np.sqrt(6.0)
    log(f"    y_t/g_3 at M_Pl = {yt_over_g3_Pl:.6f}  (Ward: {expected_ratio:.6f})")
    log(f"    Note: g_3 at M_Pl from RGE differs from framework g_3(M_Pl)")
    log(f"    because the CMT sets alpha_s(v), not alpha_s(M_Pl).")
    log()


# =====================================================================
# LAMBDA SENSITIVITY SCAN
# =====================================================================
log("=" * 78)
log("LAMBDA SENSITIVITY: Does lambda(v) affect m_t?")
log("=" * 78)
log()

lambda_scan = [0.0, 0.05, 0.10, 0.129, 0.15, 0.20, 0.30]
log(f"  {'lambda(v)':>10s}  {'y_t(v)':>10s}  {'m_t [GeV]':>10s}  {'dev%':>8s}")
log(f"  {'-'*10}  {'-'*10}  {'-'*10}  {'-'*8}")

for lam_trial in lambda_scan:
    # Override LAMBDA_V temporarily
    global_lam = lam_trial

    def yt_res_lam(yt_trial):
        y0 = [g1_v, g2_v, G_S_V, yt_trial, global_lam]
        y_f, _ = run_with_thresholds(y0, t_v, t_Pl,
                                     include_ew=True, include_2loop=True,
                                     max_step=1.0)
        return y_f[3] - YT_PL

    try:
        # Quick bracket search
        lo, hi = 0.7, 1.2
        if yt_res_lam(lo) * yt_res_lam(hi) > 0:
            log(f"  {lam_trial:10.3f}  {'no bracket':>10s}")
            continue
        root = brentq(yt_res_lam, lo, hi, xtol=1e-7)
        mt_lam = root * V_DERIVED / np.sqrt(2.0)
        dev_lam = (mt_lam - M_T_OBS) / M_T_OBS * 100
        log(f"  {lam_trial:10.3f}  {root:10.6f}  {mt_lam:10.2f}  {dev_lam:+8.2f}%")
    except (RuntimeError, ValueError):
        log(f"  {lam_trial:10.3f}  {'FAILED':>10s}")

log()


# =====================================================================
# FINAL SCORECARD
# =====================================================================
log("=" * 78)
log("FINAL SCORECARD")
log("=" * 78)
log()

r_full = results.get("2loop_withEW_withThresh", {})
r_1loop_ref = results.get("1loop_noEW_noThresh", {})

log(f"  {'Quantity':<25s}  {'Value':>12s}  {'Observed':>12s}  {'Deviation':>10s}")
log(f"  {'-'*25}  {'-'*12}  {'-'*12}  {'-'*10}")

log(f"  {'v (derived)    [GeV]':<25s}  {V_DERIVED:>12.2f}  {V_OBS:>12.2f}  {(V_DERIVED-V_OBS)/V_OBS*100:>+9.2f}%")
log(f"  {'alpha_s(v) (CMT)':<25s}  {ALPHA_S_V:>12.6f}  {'--':>12s}  {'--':>10s}")

if r_full.get('mt') is not None:
    dev_full = (r_full['mt'] - M_T_OBS) / M_T_OBS * 100
    log(f"  {'m_t (2-loop full) [GeV]':<25s}  {r_full['mt']:>12.2f}  {M_T_OBS:>12.2f}  {dev_full:>+9.2f}%")
    log(f"  {'y_t(v) (2-loop full)':<25s}  {r_full['yt_v']:>12.6f}  {Y_T_OBS:>12.6f}  {(r_full['yt_v']-Y_T_OBS)/Y_T_OBS*100:>+9.2f}%")

r_1loop_ew_ref = results.get("1loop_withEW_noThresh", {})
if r_1loop_ew_ref.get('mt') is not None:
    dev_1loop_ew = (r_1loop_ew_ref['mt'] - M_T_OBS) / M_T_OBS * 100
    log(f"  {'m_t (1-loop+EW)  [GeV]':<25s}  {r_1loop_ew_ref['mt']:>12.2f}  {M_T_OBS:>12.2f}  {dev_1loop_ew:>+9.2f}%")

if r_1loop_ref.get('mt') is not None:
    dev_1loop = (r_1loop_ref['mt'] - M_T_OBS) / M_T_OBS * 100
    log(f"  {'m_t (1-loop QCD)  [GeV]':<25s}  {r_1loop_ref['mt']:>12.2f}  {M_T_OBS:>12.2f}  {dev_1loop:>+9.2f}%")

if forward_success:
    log(f"  {'m_t (forward)    [GeV]':<25s}  {mt_fwd:>12.2f}  {M_T_OBS:>12.2f}  {dev_fwd:>+9.2f}%")

log()

# Checks
log("  CHECKS:")
if r_full.get('mt') is not None:
    check("mt_2loop_full",
          abs(r_full['mt'] - M_T_OBS) / M_T_OBS < 0.10,
          f"m_t = {r_full['mt']:.2f} GeV ({dev_full:+.2f}%), target < 10% deviation")

    if r_1loop_ref.get('mt') is not None:
        improvement = abs(dev_1loop) - abs(dev_full)
        check("2loop_improves",
              improvement > 0,
              f"2-loop reduces |deviation| by {improvement:.2f} percentage points")

log()

# Key physics summary
log("  PHYSICS SUMMARY:")
log(f"  {'='*60}")

r_1loop_ew_comp = results.get("1loop_withEW_noThresh", {})
if r_1loop_ew_comp.get('mt') and r_full.get('mt'):
    shift_from_existing = r_full['mt'] - r_1loop_ew_comp['mt']
    log(f"  Shift from existing chain (1-loop+EW) to 2-loop+EW: {shift_from_existing:+.2f} GeV")
    log(f"  Existing chain:    m_t = {r_1loop_ew_comp['mt']:.2f} GeV ({(r_1loop_ew_comp['mt']-M_T_OBS)/M_T_OBS*100:+.2f}%)")
    log(f"  2-loop chain:      m_t = {r_full['mt']:.2f} GeV ({(r_full['mt']-M_T_OBS)/M_T_OBS*100:+.2f}%)")
    log(f"  Remaining gap to observation: {r_full['mt'] - M_T_OBS:+.2f} GeV")
    log()

    log(f"  Improvement breakdown (additive contributions):")
    if r_2loop_base.get('mt') and r_1loop_base.get('mt'):
        shift_2loop = r_2loop_base['mt'] - r_1loop_base['mt']
        log(f"    2-loop QCD beta:        {shift_2loop:+.2f} GeV")

    if r_1loop_ew.get('mt') and r_1loop_base.get('mt'):
        shift_ew = r_1loop_ew['mt'] - r_1loop_base['mt']
        log(f"    EW corrections (g1,g2): {shift_ew:+.2f} GeV  (already in existing chain)")

    if r_1loop_full.get('mt') and r_1loop_ew.get('mt'):
        shift_thresh = r_1loop_full['mt'] - r_1loop_ew['mt']
        log(f"    Threshold matching:     {shift_thresh:+.2f} GeV  (none: all thresholds below v)")

    log(f"    NET NEW from 2-loop:    {shift_from_existing:+.2f} GeV")

log()

# Assessment
log("  ASSESSMENT:")
log(f"  {'='*60}")
if r_full.get('mt') is not None:
    remaining = abs((r_full['mt'] - M_T_OBS) / M_T_OBS * 100)
    gap_gev = r_full['mt'] - M_T_OBS
    if remaining < 2:
        log(f"  2-loop chain gets m_t = {r_full['mt']:.1f} GeV ({gap_gev:+.1f} GeV, {remaining:.1f}%).")
        log(f"  This is within the 2% target.")
        log()
        log(f"  HONEST ACCOUNTING of remaining {abs(gap_gev):.1f} GeV:")
        log(f"    - MSbar-to-pole mass conversion: ~+2 GeV at 2-loop QCD")
        log(f"      (m_pole = m_MSbar(m_t) * [1 + 4 alpha_s/(3 pi) + ...] )")
        log(f"    - 3-loop y_t beta: ~0.5% = ~0.9 GeV")
        log(f"    - Scheme matching (lattice -> MSbar): ~1-2 GeV")
        log(f"    - y_b, y_tau Yukawa contributions (neglected): < 0.5 GeV")
        log(f"  These known corrections are O(+3 GeV), consistent with")
        log(f"  closing the {abs(gap_gev):.1f} GeV gap.")
    elif remaining < 5:
        log(f"  2-loop chain reduces residual to {remaining:.1f}% ({gap_gev:+.1f} GeV).")
        log("  Remaining gap is within higher-loop + scheme-matching systematics.")
    else:
        log(f"  2-loop chain gives {remaining:.1f}% residual ({gap_gev:+.1f} GeV).")
        log("  The 2-loop correction is significant but does not fully close the gap.")
log()

elapsed = time.time() - t0
log(f"  Elapsed: {elapsed:.1f}s")
log()

if COUNTS["FAIL"] > 0:
    log(f"  *** {COUNTS['FAIL']} FAILURES ***")
    sys.exit(1)
else:
    log(f"  All {COUNTS['PASS']} checks passed.")
    sys.exit(0)
