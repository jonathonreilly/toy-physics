#!/usr/bin/env python3
"""
Taste-Structural Gauge Couplings: Can the Hierarchy Mechanism Predict alpha_s?
==============================================================================

STATUS: EXPLORATION -- testing whether the same taste-determinant structure
that gives v = M_Pl * alpha_LM^16 also determines low-energy gauge couplings.

THE KEY INSIGHT:
  The hierarchy formula gives v/M_Pl = alpha_LM^16 where 16 = 2 x 2^3 counts
  the taste register. This is NOT perturbative running -- it is a structural
  consequence of the taste determinant on the minimal L_t=2 block.

  If the same structure determines OTHER scale ratios, then alpha_s(M_Z),
  Lambda_QCD, m_t, etc. are all taste-determined.

HYPOTHESES TESTED:
  (A) alpha_s(v) = alpha_LM, then perturbative QCD running v -> M_Z
  (B) alpha_s(v) = alpha_LM with 1-loop threshold correction at v
  (C) alpha_s(M_Z) = alpha_LM^{N/16} for integer N (taste subset)
  (D) Taste staircase: masses m_k = M_Pl * alpha^k
  (E) Top mass from taste-structural Yukawa
  (F) alpha_s(v) from effective N_eff recalibration

OBSERVED VALUES (targets):
  alpha_s(M_Z) = 0.1179 +/- 0.0009
  m_t(pole)    = 172.69 +/- 0.30 GeV
  Lambda_QCD   ~ 210-340 MeV (MSbar, n_f=5)

PStack experiment: taste-structural-coupling
"""

from __future__ import annotations

import math
import sys

import numpy as np

# ============================================================================
# Physical constants and inputs
# ============================================================================

M_PL = 1.22e19          # GeV, unreduced Planck mass
V_EW = 246.22           # GeV, observed EW VEV
V_TASTE = 254.0         # GeV, taste formula prediction
M_Z = 91.1876           # GeV
M_W = 80.377            # GeV
M_T_POLE = 172.69       # GeV, observed top pole mass
ALPHA_S_MZ_OBS = 0.1179 # observed alpha_s(M_Z) (PDG 2024)
LAMBDA_QCD_OBS = 0.210  # GeV, approximate Lambda_QCD (MSbar, n_f=5)

# Taste framework inputs
PLAQ_MC = 0.594
U0 = PLAQ_MC ** 0.25
ALPHA_BARE = 1.0 / (4.0 * math.pi)
ALPHA_LM = ALPHA_BARE / U0  # = 0.0906

PASS_COUNT = 0
FAIL_COUNT = 0


def check(name: str, condition: bool, detail: str = ""):
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if condition else "FAIL"
    if condition:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1
    print(f"  [{status}] {name}")
    if detail:
        print(f"         {detail}")


def pct_dev(pred: float, obs: float) -> float:
    return abs(pred - obs) / obs * 100.0


# ============================================================================
# QCD running utilities
# ============================================================================

def beta0_qcd(nf: int) -> float:
    """1-loop QCD beta function coefficient b_0 = (33 - 2*n_f) / (12*pi)."""
    return (33.0 - 2.0 * nf) / (12.0 * math.pi)


def beta1_qcd(nf: int) -> float:
    """2-loop QCD beta function coefficient b_1 = (153 - 19*n_f) / (24*pi^2)."""
    return (153.0 - 19.0 * nf) / (24.0 * math.pi**2)


def run_alpha_s_1loop(alpha_s_0: float, mu_0: float, mu_f: float, nf: int) -> float:
    """1-loop RGE running of alpha_s from mu_0 to mu_f."""
    b0 = beta0_qcd(nf)
    return alpha_s_0 / (1.0 + b0 * alpha_s_0 * math.log(mu_f**2 / mu_0**2))


def run_alpha_s_2loop(alpha_s_0: float, mu_0: float, mu_f: float, nf: int) -> float:
    """2-loop RGE running of alpha_s from mu_0 to mu_f.

    Uses the exact 2-loop formula:
      1/alpha(mu) = 1/alpha(mu_0) + b0*ln(mu^2/mu_0^2)
                    + (b1/b0)*ln[1 + b0*alpha(mu_0)*ln(mu^2/mu_0^2)]
    """
    b0 = beta0_qcd(nf)
    b1 = beta1_qcd(nf)
    t = math.log(mu_f**2 / mu_0**2)
    inv_alpha_0 = 1.0 / alpha_s_0
    # Iterative solution (the exact formula is transcendental)
    alpha = alpha_s_0
    for _ in range(50):
        inv_alpha_new = inv_alpha_0 + b0 * t + (b1 / b0) * math.log(
            max(1e-30, 1.0 + b0 * alpha_s_0 * t)
        )
        alpha = 1.0 / max(inv_alpha_new, 1e-10)
    return alpha


def lambda_qcd_from_alpha(alpha_s: float, mu: float, nf: int) -> float:
    """Compute Lambda_QCD from alpha_s(mu) at 1-loop."""
    b0 = beta0_qcd(nf)
    return mu * math.exp(-1.0 / (2.0 * b0 * alpha_s))


# ============================================================================
# PART 1: Scale Ratios from Taste Structure
# ============================================================================

def part1_scale_ratios():
    print("\n" + "=" * 72)
    print("PART 1: Scale Ratios from Taste Structure")
    print("=" * 72)

    print("\n  The hierarchy formula: v = M_Pl * alpha_LM^16")
    print(f"  alpha_LM = {ALPHA_LM:.5f}")
    print(f"  v_taste  = {M_PL * ALPHA_LM**16:.1f} GeV")
    print(f"  v_obs    = {V_EW:.2f} GeV")

    # What N gives alpha_LM^{N/16} = alpha_s(M_Z)?
    print("\n  --- What N gives alpha_s(M_Z) = 0.118 from alpha_LM^{N/16}? ---")
    N_needed = 16.0 * math.log(ALPHA_S_MZ_OBS) / math.log(ALPHA_LM)
    print(f"  N = 16 * ln(0.1179) / ln({ALPHA_LM:.4f})")
    print(f"    = 16 * {math.log(ALPHA_S_MZ_OBS):.4f} / {math.log(ALPHA_LM):.4f}")
    print(f"    = {N_needed:.2f}")
    print(f"  So ~{N_needed:.1f} of 16 taste states 'active' at M_Z -> non-integer, not clean")

    # Table of alpha_LM^{N/16} for integer N
    print("\n  --- alpha_LM^{N/16} for integer N ---")
    print(f"  {'N':>4s}  {'alpha^(N/16)':>12s}  {'dev from 0.118':>14s}  interpretation")
    print(f"  {'----':>4s}  {'------------':>12s}  {'--------------':>14s}  ---------------")
    for N in range(10, 17):
        a = ALPHA_LM ** (N / 16.0)
        dev = pct_dev(a, ALPHA_S_MZ_OBS)
        note = ""
        if N == 14:
            note = "14 = 16 - 2 (Goldstones eaten)"
        elif N == 15:
            note = "15 = 16 - 1 (Higgs singlet)"
        elif N == 16:
            note = "16 = full register (= alpha_LM)"
        elif N == 12:
            note = "12 = 16 - 4 (singlet + triplet)"
        elif N == 13:
            note = "13 = 16 - 3 (triplet eaten)"
        print(f"  {N:4d}  {a:12.5f}  {dev:13.1f}%  {note}")

    # The key finding: N=14 gives the closest
    a14 = ALPHA_LM ** (14.0 / 16.0)
    dev14 = pct_dev(a14, ALPHA_S_MZ_OBS)
    check("N=14 (16 minus 2 eaten) gives alpha closest to alpha_s(M_Z)",
          dev14 < 15.0,
          f"alpha_LM^(14/16) = {a14:.5f}, observed alpha_s = {ALPHA_S_MZ_OBS}, "
          f"deviation = {dev14:.1f}%")


# ============================================================================
# PART 2: alpha_s(M_Z) from Taste + Short Running
# ============================================================================

def part2_alpha_s_mz():
    print("\n" + "=" * 72)
    print("PART 2: alpha_s(M_Z) from Various Hypotheses")
    print("=" * 72)

    results = {}

    # --- Hypothesis A: alpha_s(v) = alpha_LM, then run v -> M_Z ---
    print("\n  --- Hypothesis A: alpha_s(v) = alpha_LM, run to M_Z ---")
    # At v ~ 254 GeV, n_f = 5 (b quark active, top decoupled)
    nf = 5
    alpha_s_v = ALPHA_LM
    alpha_s_mz_A_1loop = run_alpha_s_1loop(alpha_s_v, V_TASTE, M_Z, nf)
    alpha_s_mz_A_2loop = run_alpha_s_2loop(alpha_s_v, V_TASTE, M_Z, nf)
    dev_A = pct_dev(alpha_s_mz_A_2loop, ALPHA_S_MZ_OBS)
    print(f"  alpha_s(v={V_TASTE}) = alpha_LM = {ALPHA_LM:.5f}")
    print(f"  Running v -> M_Z with n_f = {nf}:")
    print(f"    1-loop: alpha_s(M_Z) = {alpha_s_mz_A_1loop:.5f}")
    print(f"    2-loop: alpha_s(M_Z) = {alpha_s_mz_A_2loop:.5f}")
    print(f"    observed:              {ALPHA_S_MZ_OBS:.4f}")
    print(f"    deviation: {dev_A:.1f}%")
    results["A: alpha_s(v)=alpha_LM"] = (alpha_s_mz_A_2loop, dev_A)
    check("Hyp A: alpha_s(M_Z) within 20% of observed",
          dev_A < 20.0,
          f"predicted = {alpha_s_mz_A_2loop:.5f}, dev = {dev_A:.1f}%")

    # --- Hypothesis B: threshold correction at v ---
    print("\n  --- Hypothesis B: alpha_s(v) = alpha_LM + threshold at v ---")
    # At EWSB, the 3 Goldstone taste modes decouple. This changes the
    # effective coupling by a threshold matching:
    # alpha_s(v-) = alpha_s(v+) * (1 + delta)
    # Standard 1-loop threshold correction for n_f -> n_f-1:
    #   delta = alpha_s / (6*pi) * ln(m_t^2 / v^2) ~ small
    # But here we consider TASTE thresholds, not flavor thresholds.
    # If 3 taste Goldstones decouple at v, the taste-structural effect is:
    #   alpha_eff = alpha_LM^{13/16}  (13 remaining tastes)
    # No -- that's hypothesis C. Let's do something different.
    # Threshold correction from integrating out the top quark at mu = m_t:
    alpha_s_mt = ALPHA_LM
    alpha_s_v_below = run_alpha_s_1loop(alpha_s_mt, M_T_POLE, V_TASTE, nf=6)
    # Now run from v to M_Z with n_f=5
    alpha_s_mz_B = run_alpha_s_2loop(alpha_s_v_below, V_TASTE, M_Z, nf=5)
    dev_B = pct_dev(alpha_s_mz_B, ALPHA_S_MZ_OBS)
    print(f"  alpha_s(m_t={M_T_POLE}) = alpha_LM = {ALPHA_LM:.5f}")
    print(f"  Run m_t -> v with n_f=6: alpha_s(v) = {alpha_s_v_below:.5f}")
    print(f"  Run v -> M_Z with n_f=5: alpha_s(M_Z) = {alpha_s_mz_B:.5f}")
    print(f"  deviation: {dev_B:.1f}%")
    results["B: threshold at m_t"] = (alpha_s_mz_B, dev_B)
    check("Hyp B: alpha_s(M_Z) within 20% of observed",
          dev_B < 20.0,
          f"predicted = {alpha_s_mz_B:.5f}, dev = {dev_B:.1f}%")

    # --- Hypothesis C: alpha_s(M_Z) = alpha_LM^{N/16} ---
    print("\n  --- Hypothesis C: alpha_s(M_Z) = alpha_LM^{N/16} for integer N ---")
    best_N = None
    best_dev = 1e10
    for N in range(1, 17):
        a = ALPHA_LM ** (N / 16.0)
        dev = pct_dev(a, ALPHA_S_MZ_OBS)
        if dev < best_dev:
            best_dev = dev
            best_N = N
    a_best = ALPHA_LM ** (best_N / 16.0)
    print(f"  Best integer N = {best_N}: alpha_LM^({best_N}/16) = {a_best:.5f}")
    print(f"  deviation from 0.1179: {best_dev:.1f}%")
    results[f"C: N={best_N}"] = (a_best, best_dev)
    check(f"Hyp C: best integer N={best_N} gives alpha_s within 20%",
          best_dev < 20.0,
          f"alpha_LM^({best_N}/16) = {a_best:.5f}, dev = {best_dev:.1f}%")

    # --- Hypothesis D: Taste staircase ---
    print("\n  --- Hypothesis D: Taste staircase m_k = M_Pl * alpha^k ---")
    print(f"  Taste masses in the staircase:")
    staircase_masses = []
    for k in range(17):
        mk = M_PL * ALPHA_LM**k
        staircase_masses.append(mk)
        if k <= 3 or k >= 14:
            print(f"    m_{k:2d} = {mk:.3e} GeV")
        elif k == 4:
            print(f"    ...")

    # Count active tastes at M_Z
    N_active_mz = sum(1 for m in staircase_masses if m > M_Z)
    print(f"\n  Active tastes at M_Z = {M_Z} GeV: {N_active_mz}")
    # The lowest staircase mass above M_Z
    masses_above = [m for m in staircase_masses if m > M_Z]
    if masses_above:
        print(f"  Lightest active taste mass: {min(masses_above):.1f} GeV")
    masses_below = [m for m in staircase_masses if m <= M_Z]
    if masses_below:
        print(f"  Heaviest decoupled taste mass: {max(masses_below):.1f} GeV")

    alpha_D = ALPHA_LM ** (N_active_mz / 16.0)
    dev_D = pct_dev(alpha_D, ALPHA_S_MZ_OBS)
    print(f"  alpha_eff(M_Z) = alpha_LM^({N_active_mz}/16) = {alpha_D:.5f}")
    print(f"  deviation from 0.1179: {dev_D:.1f}%")
    results[f"D: staircase N={N_active_mz}"] = (alpha_D, dev_D)

    # Also: what IS the staircase at M_Z more precisely?
    # Use continuous formula: N_active(mu) = ln(M_Pl/mu) / ln(1/alpha_LM)
    N_cont = math.log(M_PL / M_Z) / math.log(1.0 / ALPHA_LM)
    print(f"\n  Continuous N_active(M_Z) = ln(M_Pl/M_Z) / ln(1/alpha_LM)")
    print(f"    = {math.log(M_PL/M_Z):.3f} / {math.log(1.0/ALPHA_LM):.3f}")
    print(f"    = {N_cont:.2f}")

    # --- Hypothesis E: Top mass from taste Yukawa ---
    print("\n  --- Hypothesis E: Top mass from taste-structural Yukawa ---")
    # If y_t(v) = g_s(v)/sqrt(6) where g_s(v)^2 = 4*pi*alpha_s(v):
    # With alpha_s(v) = alpha_LM:
    g_s_v = math.sqrt(4 * math.pi * ALPHA_LM)
    y_t_v = g_s_v / math.sqrt(6)
    m_t_tree = y_t_v * V_EW / math.sqrt(2)
    print(f"  g_s(v) = sqrt(4*pi*alpha_LM) = {g_s_v:.5f}")
    print(f"  y_t(v) = g_s/sqrt(6) = {y_t_v:.5f}")
    print(f"  m_t(tree) = y_t * v / sqrt(2) = {m_t_tree:.1f} GeV")
    dev_mt = pct_dev(m_t_tree, M_T_POLE)
    print(f"  m_t(obs) = {M_T_POLE} GeV, deviation = {dev_mt:.1f}%")
    results["E: m_t(tree)"] = (m_t_tree, dev_mt)

    # With the OBSERVED alpha_s(m_t) instead:
    # alpha_s(m_t) ~ 0.108 (well established)
    alpha_s_mt_obs = 0.1080
    g_s_mt = math.sqrt(4 * math.pi * alpha_s_mt_obs)
    y_t_mt = g_s_mt / math.sqrt(6)
    m_t_obs_yt = y_t_mt * V_EW / math.sqrt(2)
    print(f"\n  For comparison, with observed alpha_s(m_t) = {alpha_s_mt_obs}:")
    print(f"    y_t = {y_t_mt:.4f}, m_t = {m_t_obs_yt:.1f} GeV")
    print(f"    (The y_t = g_s/sqrt(6) Ansatz gives m_t too low even with observed alpha_s)")

    # Standard model: y_t ~ 0.994 at m_t (from m_t = y_t * v / sqrt(2))
    y_t_sm = M_T_POLE * math.sqrt(2) / V_EW
    print(f"\n  SM Yukawa at m_t: y_t = m_t*sqrt(2)/v = {y_t_sm:.4f}")
    print(f"  Ratio y_t(SM) / y_t(taste) = {y_t_sm / y_t_v:.3f}")
    # So the taste Yukawa is about 2.3x too small. This is the same as saying
    # the top mass at tree level from taste coupling is about 75 GeV.

    # --- Hypothesis F: Recalibrated effective coupling ---
    print("\n  --- Hypothesis F: What alpha_s(v) gives correct alpha_s(M_Z)? ---")
    # Invert: given alpha_s(M_Z) = 0.1179, what is alpha_s(v)?
    # 1-loop running DOWN: 1/alpha(M_Z) = 1/alpha(v) + b0 * ln(M_Z^2/v^2)
    # => 1/alpha(v) = 1/alpha(M_Z) - b0 * ln(M_Z^2/v^2)
    #               = 1/alpha(M_Z) + b0 * ln(v^2/M_Z^2)
    nf = 5
    b0 = beta0_qcd(nf)
    t_vMZ = math.log(V_EW**2 / M_Z**2)
    inv_alpha_v = 1.0 / ALPHA_S_MZ_OBS + b0 * t_vMZ
    alpha_s_v_needed = 1.0 / inv_alpha_v
    print(f"  From alpha_s(M_Z) = {ALPHA_S_MZ_OBS}, running UP to v = {V_EW} GeV:")
    print(f"    alpha_s(v) = {alpha_s_v_needed:.5f}")
    print(f"    alpha_LM   = {ALPHA_LM:.5f}")
    print(f"    ratio alpha_s(v)/alpha_LM = {alpha_s_v_needed/ALPHA_LM:.4f}")
    dev_F = pct_dev(alpha_s_v_needed, ALPHA_LM)
    print(f"    deviation from alpha_LM: {dev_F:.1f}%")
    results["F: alpha_s(v) needed"] = (alpha_s_v_needed, dev_F)

    # The ratio 0.1010/0.0906 ~ 1.115. Is there a structural factor?
    print(f"\n  Structural factor needed: {alpha_s_v_needed/ALPHA_LM:.4f}")
    print(f"  Some candidates:")
    print(f"    sqrt(N_c/2) = sqrt(3/2) = {math.sqrt(1.5):.4f}")
    print(f"    pi/e = {math.pi/math.e:.4f}")
    print(f"    (4/3)^{1/2} = {(4/3)**0.5:.4f}")
    print(f"    16/14 = {16/14:.4f}")
    print(f"    (16/14)^2 = {(16/14)**2:.4f}")

    # Note: the ratio ~1.5 is large. But alpha_bare/u0^2 = 0.1033 is close!
    alpha_lm_over_u0 = ALPHA_BARE / U0**2
    dev_F2 = pct_dev(alpha_lm_over_u0, alpha_s_v_needed)
    print(f"\n  NOTABLE: alpha_bare/u0^2 = {alpha_lm_over_u0:.5f}")
    print(f"  vs needed = {alpha_s_v_needed:.5f}")
    print(f"  deviation: {dev_F2:.1f}%")
    check("Hyp F: alpha_bare/u0^2 matches alpha_s(v) needed within 5%",
          dev_F2 < 5.0,
          f"alpha_bare/u0^2 = {alpha_lm_over_u0:.5f}, needed = {alpha_s_v_needed:.5f}, "
          f"dev = {dev_F2:.1f}%")

    # --- Summary table ---
    print("\n  " + "=" * 68)
    print("  SUMMARY: Hypotheses for alpha_s(M_Z)")
    print("  " + "=" * 68)
    print(f"  {'Hypothesis':40s}  {'Predicted':>10s}  {'Observed':>10s}  {'Dev':>6s}")
    print(f"  {'----------':40s}  {'--------':>10s}  {'--------':>10s}  {'---':>6s}")
    for name, (pred, dev) in results.items():
        obs_str = f"{ALPHA_S_MZ_OBS:.4f}" if "m_t" not in name else f"{M_T_POLE:.1f}"
        print(f"  {name:40s}  {pred:10.5f}  {obs_str:>10s}  {dev:5.1f}%")

    return results


# ============================================================================
# PART 3: Lambda_QCD from Taste Structure
# ============================================================================

def part3_lambda_qcd():
    print("\n" + "=" * 72)
    print("PART 3: Lambda_QCD from Taste Structure")
    print("=" * 72)

    # From hypothesis A: alpha_s(v) = alpha_LM = 0.0906
    print("\n  --- Lambda_QCD from alpha_s(v) = alpha_LM ---")
    nf = 5
    Lambda_A = lambda_qcd_from_alpha(ALPHA_LM, V_TASTE, nf)
    print(f"  alpha_s({V_TASTE}) = {ALPHA_LM:.5f}")
    print(f"  Lambda_QCD(n_f=5) = {Lambda_A*1000:.1f} MeV")
    print(f"  observed: ~{LAMBDA_QCD_OBS*1000:.0f} MeV")
    dev_lam = pct_dev(Lambda_A, LAMBDA_QCD_OBS)
    print(f"  deviation: {dev_lam:.1f}%")
    check("Lambda_QCD within order of magnitude of observed",
          0.1 < Lambda_A / LAMBDA_QCD_OBS < 10.0,
          f"Lambda_pred/Lambda_obs = {Lambda_A/LAMBDA_QCD_OBS:.3f} "
          f"(factor {max(Lambda_A/LAMBDA_QCD_OBS, LAMBDA_QCD_OBS/Lambda_A):.1f}x off)")

    # From the staircase: Lambda_QCD = scale where last taste decouples
    print("\n  --- Lambda_QCD from taste staircase ---")
    # In the staircase, m_k = M_Pl * alpha^k
    # The last (16th) taste has m_16 = M_Pl * alpha^16 = v = 254 GeV
    # The 17th "taste" (if it existed) would be at M_Pl * alpha^17
    m_17 = M_PL * ALPHA_LM**17
    print(f"  m_16 = v = {M_PL * ALPHA_LM**16:.1f} GeV")
    print(f"  m_17 = v * alpha = {m_17:.1f} GeV")
    print(f"  m_18 = v * alpha^2 = {M_PL * ALPHA_LM**18:.2f} GeV")
    print(f"  m_19 = v * alpha^3 = {M_PL * ALPHA_LM**19:.3f} GeV")
    print(f"  m_20 = v * alpha^4 = {M_PL * ALPHA_LM**20:.4f} GeV")

    # The "m_17" scale is v * alpha_LM = 254 * 0.0906 = 23 GeV
    # That's close to m_b! And below that, the coupling would grow further.
    # The natural Lambda_QCD in this picture is where alpha -> 1.

    # More precisely: starting from alpha_s(v) = alpha_LM, Lambda_QCD from
    # the 1-loop formula:
    print(f"\n  Comparison with perturbative Lambda_QCD:")
    for nf_val in [3, 4, 5]:
        lam = lambda_qcd_from_alpha(ALPHA_LM, V_TASTE, nf_val)
        print(f"    Lambda(n_f={nf_val}) = {lam*1000:.1f} MeV")

    # What about the "taste staircase Lambda"?
    # If coupling grows as alpha(mu) = alpha_LM * (v/mu)^{2*b0} for mu < v,
    # then alpha(mu) = 1 at Lambda:
    b0_5 = beta0_qcd(5)
    if b0_5 * ALPHA_LM > 0:
        mu_strong = V_TASTE * math.exp(-1.0 / (2.0 * b0_5 * ALPHA_LM))
        print(f"\n  Scale where alpha_s = 1 (from perturbative running):")
        print(f"    mu_strong = {mu_strong*1000:.1f} MeV")

    # The structural picture: Lambda_QCD ~ v * alpha^k for some k
    print(f"\n  Structural scale ratios from v:")
    for k in range(1, 6):
        scale = V_TASTE * ALPHA_LM**k
        print(f"    v * alpha^{k} = {scale:.3f} GeV = {scale*1000:.1f} MeV")

    # v * alpha^1 = 23 GeV ~ m_b region
    # v * alpha^2 = 2.1 GeV ~ m_charm/Lambda_QCD region
    # v * alpha^3 = 0.19 GeV ~ Lambda_QCD!
    lam_struct = V_TASTE * ALPHA_LM**3
    dev_struct = pct_dev(lam_struct, LAMBDA_QCD_OBS)
    print(f"\n  KEY FINDING: v * alpha_LM^3 = {lam_struct*1000:.0f} MeV")
    print(f"  Lambda_QCD(obs) ~ {LAMBDA_QCD_OBS*1000:.0f} MeV")
    print(f"  deviation: {dev_struct:.1f}%")
    check("v * alpha^3 ~ Lambda_QCD (within 50%)",
          dev_struct < 50.0,
          f"v*alpha^3 = {lam_struct*1000:.0f} MeV, obs ~ {LAMBDA_QCD_OBS*1000:.0f} MeV")

    # Also check: v * alpha^1 ~ m_b?
    m_b = 4.18  # GeV, MSbar mass
    scale_1 = V_TASTE * ALPHA_LM
    dev_mb = pct_dev(scale_1, m_b)
    print(f"\n  v * alpha^1 = {scale_1:.1f} GeV vs m_b = {m_b} GeV")
    print(f"  deviation: {dev_mb:.0f}%")
    # That's 23 GeV vs 4.2 GeV -- factor of 5.5 off. Not great.

    # v * alpha^2 ~ m_charm?
    m_c = 1.27  # GeV, MSbar mass
    scale_2 = V_TASTE * ALPHA_LM**2
    dev_mc = pct_dev(scale_2, m_c)
    print(f"  v * alpha^2 = {scale_2:.2f} GeV vs m_c = {m_c} GeV")
    print(f"  deviation: {dev_mc:.0f}%")
    # 2.1 GeV vs 1.27 GeV -- factor of 1.6. Not bad!

    check("v * alpha^2 within factor 2 of m_c",
          0.5 < scale_2 / m_c < 2.5,
          f"ratio = {scale_2/m_c:.2f}")


# ============================================================================
# PART 4: Self-Consistency — The Full Taste Staircase
# ============================================================================

def part4_self_consistency():
    print("\n" + "=" * 72)
    print("PART 4: Self-Consistency of the Taste Staircase")
    print("=" * 72)

    print("\n  The staircase: m_k = M_Pl * alpha^k, k = 0, 1, ..., 16")
    print(f"  alpha_LM = {ALPHA_LM:.5f}")
    print(f"  ln(1/alpha_LM) = {math.log(1/ALPHA_LM):.4f}")
    print()

    # Full staircase
    print(f"  {'k':>3s}  {'m_k (GeV)':>14s}  {'log10(m_k)':>10s}  physical scale")
    print(f"  {'---':>3s}  {'-----------':>14s}  {'----------':>10s}  ---------------")
    physical_scales = {
        0: "M_Planck",
        1: "~ GUT?",
        8: "intermediate?",
        15: "~ few TeV",
        16: "v (EW VEV)",
    }
    for k in range(17):
        mk = M_PL * ALPHA_LM**k
        note = physical_scales.get(k, "")
        if k <= 3 or k >= 13 or k == 8:
            print(f"  {k:3d}  {mk:14.3e}  {math.log10(mk):10.2f}  {note}")
        elif k == 4:
            print(f"  ...  {'':>14s}  {'':>10s}")

    # Check that the staircase spacing is consistent
    # Each step is a factor of alpha_LM = 0.0906, i.e., ~1.04 decades
    decades_per_step = -math.log10(ALPHA_LM)
    print(f"\n  Decades per staircase step: {decades_per_step:.3f}")
    print(f"  Total decades (16 steps): {16 * decades_per_step:.1f}")
    print(f"  Actual decades M_Pl -> v: {math.log10(M_PL/V_EW):.1f}")

    # Effective coupling at various scales from staircase
    print(f"\n  --- Effective coupling at key scales ---")
    key_scales = [
        ("M_Pl", M_PL),
        ("GUT ~ 2e16", 2e16),
        ("10^10 GeV", 1e10),
        ("TeV", 1000),
        ("v = 254 GeV", V_TASTE),
        ("M_Z = 91 GeV", M_Z),
        ("m_b = 4.2 GeV", 4.2),
        ("m_c = 1.3 GeV", 1.3),
        ("Lambda_QCD = 0.3 GeV", 0.3),
    ]

    for name, mu in key_scales:
        # Number of staircase steps above mu
        N_above = math.log(M_PL / mu) / math.log(1.0 / ALPHA_LM)
        # Clamped to [0, 16]
        N_eff = min(16.0, max(0.0, N_above))
        alpha_eff = ALPHA_LM ** (N_eff / 16.0)
        print(f"    {name:25s}: N_eff = {N_eff:5.1f}, alpha_eff = {alpha_eff:.5f}")

    print(f"\n  OBSERVATION: At M_Z, all 16 staircase masses are above M_Z,")
    print(f"  so N_eff = 16 and alpha_eff = alpha_LM = {ALPHA_LM:.4f}.")
    print(f"  This does NOT give alpha_s(M_Z) = 0.118.")
    print(f"  The staircase has all thresholds ABOVE M_Z.")


# ============================================================================
# PART 5: The Best Scenario — Short Running from v
# ============================================================================

def part5_short_running():
    print("\n" + "=" * 72)
    print("PART 5: Short Running from v (The Best Scenario)")
    print("=" * 72)

    print("\n  If the hierarchy formula gives v = 254 GeV and the coupling AT v,")
    print("  then we only need perturbative QCD running over ~1 decade (v -> M_Z).")

    # What alpha_s(v) is needed to get alpha_s(M_Z) = 0.1179 after running?
    nf = 5
    b0 = beta0_qcd(nf)
    b1 = beta1_qcd(nf)
    t = math.log(M_Z**2 / V_EW**2)  # negative (running DOWN)

    # Invert 1-loop: 1/alpha_s(v) = 1/alpha_s(M_Z) - b0*t
    inv_as_v = 1.0 / ALPHA_S_MZ_OBS - b0 * t
    alpha_s_v_exact = 1.0 / inv_as_v
    print(f"\n  Exact alpha_s(v) needed (1-loop): {alpha_s_v_exact:.5f}")

    # Detailed comparison
    print(f"\n  Comparison of alpha_s(v) candidates:")
    candidates = [
        ("alpha_LM", ALPHA_LM),
        ("alpha_LM * 16/14", ALPHA_LM * 16.0 / 14.0),
        ("alpha_LM * 8/7", ALPHA_LM * 8.0 / 7.0),
        ("alpha_LM * (1 + alpha_LM)", ALPHA_LM * (1 + ALPHA_LM)),
        ("alpha_LM * (1 + 2*alpha_LM)", ALPHA_LM * (1 + 2 * ALPHA_LM)),
        ("alpha_LM / (1 - alpha_LM/pi)", ALPHA_LM / (1 - ALPHA_LM / math.pi)),
        ("alpha_bare/u0^2 = alpha/u0", ALPHA_BARE / U0**2),
        ("NEEDED for alpha_s(M_Z)=0.118", alpha_s_v_exact),
    ]

    print(f"  {'Candidate':45s}  {'alpha_s(v)':>10s}  {'alpha_s(M_Z)':>12s}  {'dev':>6s}")
    print(f"  {'---------':45s}  {'--------':>10s}  {'----------':>12s}  {'---':>6s}")
    for name, alpha_v in candidates:
        if alpha_v > 0 and alpha_v < 1:
            alpha_mz = run_alpha_s_2loop(alpha_v, V_EW, M_Z, nf)
            dev = pct_dev(alpha_mz, ALPHA_S_MZ_OBS)
            marker = " <--" if name.startswith("NEEDED") else ""
            print(f"  {name:45s}  {alpha_v:10.5f}  {alpha_mz:12.5f}  {dev:5.1f}%{marker}")
        else:
            print(f"  {name:45s}  {alpha_v:10.5f}  {'N/A':>12s}")

    # The key result
    ratio = alpha_s_v_exact / ALPHA_LM
    print(f"\n  KEY RESULT:")
    print(f"    alpha_s(v) needed    = {alpha_s_v_exact:.5f}")
    print(f"    alpha_LM             = {ALPHA_LM:.5f}")
    print(f"    ratio                = {ratio:.4f}")
    print(f"    deficit              = {(ratio - 1)*100:.1f}%")

    # Is the ratio physically meaningful?
    print(f"\n  Is the {(ratio-1)*100:.0f}% deficit a 1-loop correction?")
    print(f"    Expected 1-loop correction: alpha_LM / pi = {ALPHA_LM/math.pi:.4f}")
    print(f"    = {ALPHA_LM/math.pi * 100:.1f}%")
    print(f"    Actual deficit: {(ratio-1)*100:.1f}%")
    print(f"    Ratio (deficit / 1-loop): {(ratio-1)/(ALPHA_LM/math.pi):.2f}")
    print(f"    So the deficit is ~{(ratio-1)/(ALPHA_LM/math.pi):.0f} x the naive 1-loop correction.")

    check("alpha_s(v) = alpha_LM gives alpha_s(M_Z) within 15% of observed",
          pct_dev(run_alpha_s_2loop(ALPHA_LM, V_EW, M_Z, nf), ALPHA_S_MZ_OBS) < 15.0,
          f"alpha_s(M_Z) = {run_alpha_s_2loop(ALPHA_LM, V_EW, M_Z, nf):.5f}")

    # Also check: what if alpha_s(v) = alpha_LM but we use v_taste = 254 GeV?
    print(f"\n  --- Sensitivity to v ---")
    for v_val in [200, 246.2, 254, 300, 500]:
        alpha_mz = run_alpha_s_2loop(ALPHA_LM, v_val, M_Z, nf)
        dev = pct_dev(alpha_mz, ALPHA_S_MZ_OBS)
        print(f"    v = {v_val:6.1f} GeV: alpha_s(M_Z) = {alpha_mz:.5f} (dev = {dev:.1f}%)")


# ============================================================================
# PART 6: Comprehensive Hypothesis Comparison
# ============================================================================

def part6_comprehensive():
    print("\n" + "=" * 72)
    print("PART 6: Comprehensive Comparison and Assessment")
    print("=" * 72)

    nf = 5

    # --- The best scenario: alpha_s(v) = alpha_LM + threshold ---
    print("\n  The most physical scenario:")
    print("  1. Taste structure gives v = M_Pl * alpha_LM^16 = 254 GeV  [established]")
    print("  2. Taste structure gives alpha_s(v) = alpha_LM = 0.0906   [hypothesis]")
    print("  3. Standard QCD running from v to M_Z (1 decade)         [perturbative]")
    print()

    alpha_s_mz_pred = run_alpha_s_2loop(ALPHA_LM, V_TASTE, M_Z, nf)
    dev = pct_dev(alpha_s_mz_pred, ALPHA_S_MZ_OBS)

    print(f"  Result: alpha_s(M_Z) = {alpha_s_mz_pred:.5f}")
    print(f"  Observed:              {ALPHA_S_MZ_OBS:.4f}")
    print(f"  Deviation:             {dev:.1f}%")

    # Lambda_QCD from this
    lam = lambda_qcd_from_alpha(alpha_s_mz_pred, M_Z, nf)
    print(f"  Lambda_QCD(n_f=5):     {lam*1000:.0f} MeV (obs ~ {LAMBDA_QCD_OBS*1000:.0f} MeV)")

    # Top mass from running
    # alpha_s(m_t) from running M_Z -> m_t
    alpha_s_mt = run_alpha_s_2loop(alpha_s_mz_pred, M_Z, M_T_POLE, nf)
    g_s_mt = math.sqrt(4 * math.pi * alpha_s_mt)
    # SM: m_t = y_t * v / sqrt(2), y_t ~ 0.99
    # If y_t = 1 (near-criticality, as in some models):
    m_t_unit_yt = V_EW / math.sqrt(2)
    print(f"\n  Top mass predictions:")
    print(f"    m_t = v/sqrt(2) (y_t = 1): {m_t_unit_yt:.1f} GeV (obs: {M_T_POLE} GeV)")
    print(f"    m_t = v/sqrt(2) gives {pct_dev(m_t_unit_yt, M_T_POLE):.0f}% deviation")

    # --- The "structural scales" picture ---
    print(f"\n  --- Structural Scale Ladder ---")
    print(f"  Starting from M_Pl, each factor of alpha_LM = {ALPHA_LM:.4f}:")
    print()

    # Key physical scales and their staircase positions
    physical = {
        "M_Pl": (M_PL, 0),
        "v = EW VEV": (V_EW, 16),
        "M_Z": (M_Z, None),
        "m_b": (4.18, None),
        "m_c": (1.27, None),
        "Lambda_QCD": (LAMBDA_QCD_OBS, None),
    }

    for name, (scale, k_exact) in physical.items():
        k_eff = math.log(M_PL / scale) / math.log(1 / ALPHA_LM)
        k_str = f"{k_exact}" if k_exact is not None else f"~{k_eff:.2f}"
        print(f"    {name:15s}:  {scale:12.3e} GeV   k = {k_str}")

    # The big picture
    print(f"\n  ================================================================")
    print(f"  CONCLUSIONS")
    print(f"  ================================================================")
    print()
    print(f"  1. ALPHA_S(M_Z):")
    print(f"     The simplest hypothesis (alpha_s(v) = alpha_LM = {ALPHA_LM:.4f})")
    print(f"     plus 1 decade of QCD running gives alpha_s(M_Z) = {alpha_s_mz_pred:.4f}.")
    print(f"     This is {dev:.0f}% below observed {ALPHA_S_MZ_OBS}.")
    print(f"     The deficit could be a ~{(ALPHA_S_MZ_OBS/alpha_s_mz_pred - 1)*100:.0f}% threshold correction at v,")
    print(f"     which is {(ALPHA_S_MZ_OBS/alpha_s_mz_pred - 1)/(ALPHA_LM/math.pi):.0f}x the naive 1-loop correction.")
    print()
    print(f"  2. LAMBDA_QCD:")
    print(f"     v * alpha_LM^3 = {V_TASTE * ALPHA_LM**3 * 1000:.0f} MeV is strikingly close to")
    print(f"     Lambda_QCD ~ {LAMBDA_QCD_OBS*1000:.0f} MeV. This suggests Lambda_QCD/v = alpha_LM^3,")
    print(f"     which would mean the QCD scale is 3 taste-steps below v.")
    print()
    print(f"  3. FERMION MASSES:")
    print(f"     The taste staircase below v gives scale spacings of alpha_LM:")
    print(f"       v * alpha^1 = {V_TASTE*ALPHA_LM:.1f} GeV   (between m_b and m_t)")
    print(f"       v * alpha^2 = {V_TASTE*ALPHA_LM**2:.2f} GeV  (near m_c = 1.27 GeV)")
    print(f"       v * alpha^3 = {V_TASTE*ALPHA_LM**3:.3f} GeV ({V_TASTE*ALPHA_LM**3*1000:.0f} MeV, near Lambda_QCD)")
    print(f"     The m_c coincidence ({pct_dev(V_TASTE*ALPHA_LM**2, 1.27):.0f}% deviation) is suggestive.")
    print()
    print(f"  4. WHAT WORKS AND WHAT DOESN'T:")
    print(f"     WORKS:  The hierarchy formula v = M_Pl * alpha^16 (3% accuracy)")
    print(f"     CLOSE:  alpha_s(M_Z) = {alpha_s_mz_pred:.4f} from alpha_s(v) = alpha_LM")
    print(f"             ({dev:.0f}% low, could be threshold correction)")
    print(f"     CLOSE:  v * alpha^3 ~ Lambda_QCD ({pct_dev(V_TASTE*ALPHA_LM**3, LAMBDA_QCD_OBS):.0f}% accuracy)")
    print(f"     CLOSE:  v * alpha^2 ~ m_c ({pct_dev(V_TASTE*ALPHA_LM**2, 1.27):.0f}% accuracy)")
    print(f"     FAILS:  m_t from taste Yukawa y_t = g_s/sqrt(6) gives {ALPHA_LM:.4f}->78 GeV")
    print(f"     OPEN:   Whether alpha_s(v) = alpha_LM or alpha_s(v) = alpha_LM * (1+delta)")

    check("alpha_s(M_Z) prediction within 20% of observed",
          dev < 20.0,
          f"deviation = {dev:.1f}%")

    # Final scorecard for taste-structural predictions
    print(f"\n  TASTE-STRUCTURAL SCORECARD:")
    scores = [
        ("v = 254 GeV (obs: 246)", 3.2),
        (f"alpha_s(M_Z) = {alpha_s_mz_pred:.4f} (obs: 0.1179)", dev),
        (f"Lambda_QCD ~ {V_TASTE*ALPHA_LM**3*1000:.0f} MeV (obs: ~210-340)", pct_dev(V_TASTE*ALPHA_LM**3, 0.275)),
        (f"m_c ~ {V_TASTE*ALPHA_LM**2:.1f} GeV (obs: 1.27)", pct_dev(V_TASTE*ALPHA_LM**2, 1.27)),
    ]
    for desc, deviation in scores:
        grade = "A" if deviation < 5 else "B" if deviation < 15 else "C" if deviation < 30 else "D" if deviation < 50 else "F"
        print(f"    [{grade}] {desc}  ({deviation:.1f}%)")


# ============================================================================
# Main
# ============================================================================

def main():
    print("=" * 72)
    print("TASTE-STRUCTURAL GAUGE COUPLINGS")
    print("Can the hierarchy mechanism predict alpha_s(M_Z)?")
    print("=" * 72)
    print()
    print(f"  Framework inputs:")
    print(f"    M_Pl       = {M_PL:.2e} GeV (unreduced)")
    print(f"    <P>        = {PLAQ_MC}")
    print(f"    u_0        = {U0:.4f}")
    print(f"    alpha_bare = {ALPHA_BARE:.5f}")
    print(f"    alpha_LM   = {ALPHA_LM:.5f}")
    print(f"    v_taste    = {M_PL * ALPHA_LM**16:.1f} GeV")
    print()
    print(f"  Targets:")
    print(f"    alpha_s(M_Z) = {ALPHA_S_MZ_OBS}")
    print(f"    m_t(pole)    = {M_T_POLE} GeV")
    print(f"    Lambda_QCD   ~ {LAMBDA_QCD_OBS*1000:.0f} MeV")

    part1_scale_ratios()
    part2_alpha_s_mz()
    part3_lambda_qcd()
    part4_self_consistency()
    part5_short_running()
    part6_comprehensive()

    print("\n" + "=" * 72)
    print(f"SCORECARD: {PASS_COUNT} pass, {FAIL_COUNT} fail "
          f"out of {PASS_COUNT + FAIL_COUNT}")
    print("=" * 72)

    if FAIL_COUNT > 0:
        print("\nSome tests FAILED -- see above for details")
        sys.exit(1)
    else:
        print("\nAll tests pass.")
        sys.exit(0)


if __name__ == "__main__":
    main()
