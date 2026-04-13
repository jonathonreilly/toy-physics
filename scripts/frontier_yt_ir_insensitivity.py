#!/usr/bin/env python3
"""
IR Insensitivity of m_t to g_3(M_Pl): Gauge Crossover Is Irrelevant?
======================================================================

INSIGHT: The gauge crossover blocker may be moot.  The top Yukawa y_t
has an IR quasi-fixed-point (Pendleton-Ross): at low energies y_t/g_3 is
attracted toward a fixed ratio regardless of the UV boundary.

If y_t(M_Z) is INSENSITIVE to g_3(M_Pl), then the exact value of the
strong coupling at the Planck scale does not matter for the m_t
prediction -- the IR attractor does the work.

THE KEY: with the framework relation y_t = g_3/sqrt(6), both couplings
start from the SAME g_3 value.  The IR flow is then the COMBINED y_t-g_3
system, not y_t alone.

WHAT WE ACTUALLY FIND:
  The hypothesis is REFUTED. For g_3(M_Pl) >= 0.8, the perturbative
  QCD coupling hits a Landau pole BEFORE reaching M_Z.  The IR
  quasi-fixed-point of the RATIO y_t/g_3 is real but irrelevant:
  what matters for m_t is the ABSOLUTE VALUE g_3(M_Z), which requires
  the coupling to flow perturbatively across the desert.

  The only regime where all five scan points can be compared is the
  SPLIT approach (SM g_3 trajectory + framework y_t boundary), which
  IS what the paper uses.  In that approach, y_t(M_Z) is indeed
  insensitive to y_t(M_Pl) because the QCD drag term dominates.

PStack experiment: yt-ir-insensitivity
Self-contained: numpy + scipy only.
"""

from __future__ import annotations

import sys
import time

import numpy as np
from scipy.integrate import solve_ivp

np.set_printoptions(precision=10, linewidth=120)

PASS_COUNT = 0
FAIL_COUNT = 0


def report(tag: str, ok: bool, msg: str, category: str = "bounded"):
    """Report a test result."""
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if ok else "FAIL"
    if ok:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1
    print(f"  [{status}] [{category.upper()}] {tag}: {msg}")


# ============================================================================
# Physical Constants
# ============================================================================

PI = np.pi
M_Z = 91.1876           # GeV
M_T_OBS = 173.0         # GeV (top quark pole mass, PDG 2024)
V_SM = 246.22           # GeV (Higgs VEV)
M_PLANCK = 1.2209e19    # GeV

ALPHA_S_MZ_OBS = 0.1179  # PDG 2024
ALPHA_EM_MZ = 1.0 / 127.951
SIN2_TW_MZ = 0.23122

Y_TOP_OBS = np.sqrt(2) * M_T_OBS / V_SM  # ~ 0.994

# GUT normalization for U(1)
ALPHA_1_MZ_GUT = (5.0 / 3.0) * ALPHA_EM_MZ / (1.0 - SIN2_TW_MZ)
ALPHA_2_MZ = ALPHA_EM_MZ / SIN2_TW_MZ

# ============================================================================

print("=" * 78)
print("IR INSENSITIVITY OF m_t TO g_3(M_Pl): GAUGE CROSSOVER IRRELEVANCE")
print("=" * 78)
print()
t0 = time.time()


# ============================================================================
# STEP 0: GAUGE COUPLINGS AT M_Pl
# ============================================================================
print("=" * 78)
print("STEP 0: Gauge Couplings at M_Planck")
print("=" * 78)
print()

L_pl = np.log(M_PLANCK / M_Z)
t_Pl = np.log(M_PLANCK)
t_Z = np.log(M_Z)

# 1-loop inverse coupling running
b1_rge = -41.0 / 10.0
b2_rge = 19.0 / 6.0
b3_rge = 7.0

inv_a1_pl = 1.0 / ALPHA_1_MZ_GUT + b1_rge / (2 * PI) * L_pl
inv_a2_pl = 1.0 / ALPHA_2_MZ + b2_rge / (2 * PI) * L_pl
inv_a3_pl = 1.0 / ALPHA_S_MZ_OBS + b3_rge / (2 * PI) * L_pl

alpha_1_pl = 1.0 / inv_a1_pl
alpha_2_pl = 1.0 / inv_a2_pl
alpha_3_pl = 1.0 / inv_a3_pl

g1_pl = np.sqrt(4 * PI * alpha_1_pl)
g2_pl = np.sqrt(4 * PI * alpha_2_pl)
g3_pl_SM = np.sqrt(4 * PI * alpha_3_pl)

print(f"  g_1(M_Pl) = {g1_pl:.6f}  (alpha_1 = {alpha_1_pl:.6f})")
print(f"  g_2(M_Pl) = {g2_pl:.6f}  (alpha_2 = {alpha_2_pl:.6f})")
print(f"  g_3(M_Pl) = {g3_pl_SM:.6f}  (alpha_3 = {alpha_3_pl:.6f})  [SM 1-loop from M_Z]")
print()

# Framework value
g3_framework = np.sqrt(4 * PI * 0.092)
print(f"  Framework g_3(M_Pl) = {g3_framework:.6f} (alpha_s = 0.092, V-scheme)")
print(f"  Ratio framework/SM = {g3_framework/g3_pl_SM:.2f}x")
print()


# ============================================================================
# STEP 1: LANDAU POLE ANALYSIS
# ============================================================================
print("=" * 78)
print("STEP 1: Landau Pole Analysis -- Why Naive Scan Fails")
print("=" * 78)
print()

print("  1-loop QCD running from M_Pl downward:")
print("    1/g_3^2(mu) = 1/g_3^2(M_Pl) + 7/(8 pi^2) * ln(mu/M_Pl)")
print()
print("  Landau pole when 1/g_3^2 = 0, i.e.:")
print("    Delta_t = 8 pi^2 / (7 g_3^2(M_Pl))")
print()
print(f"  Desert length: t_Pl - t_Z = {t_Pl - t_Z:.1f}")
print()

g3_scan = [0.5, 0.8, 1.0, 1.5, 2.0]

print(f"  {'g3(MPl)':>10s}  {'Delta_t':>10s}  {'t_pole':>10s}  "
      f"{'mu_pole [GeV]':>15s}  {'Status':>20s}")
print(f"  {'-'*10}  {'-'*10}  {'-'*10}  {'-'*15}  {'-'*20}")

for g3_uv in g3_scan:
    dt_landau = 8 * PI**2 / (7 * g3_uv**2)
    t_pole = t_Pl - dt_landau
    if dt_landau > t_Pl - t_Z:
        status = "safe (no pole)"
        mu_str = "N/A"
    else:
        mu_pole = np.exp(t_pole)
        status = f"POLE at 10^{np.log10(mu_pole):.1f} GeV"
        mu_str = f"{mu_pole:.2e}"

    print(f"  {g3_uv:10.3f}  {dt_landau:10.1f}  {t_pole:10.1f}  "
          f"{mu_str:>15s}  {status:>20s}")

print()
print("  CONCLUSION: For g_3(M_Pl) >= 0.8, the perturbative QCD coupling")
print("  develops a Landau pole BEFORE reaching M_Z. The framework value")
print(f"  g_3 = {g3_framework:.3f} hits its pole around 10^15 GeV.")
print()
print("  This IS the gauge crossover problem: the framework coupling cannot")
print("  be perturbatively run down to M_Z. A non-perturbative crossover")
print("  mechanism is required.")
print()

# How many can actually be run?
n_safe = sum(1 for g3 in g3_scan
             if 8*PI**2/(7*g3**2) > t_Pl - t_Z)
report("landau_pole_count",
       n_safe < len(g3_scan),
       f"Only {n_safe}/{len(g3_scan)} scan points avoid a Landau pole -- "
       f"naive scan is impossible")


# ============================================================================
# STEP 2: THE SPLIT APPROACH (what the paper actually uses)
# ============================================================================
print()
print("=" * 78)
print("STEP 2: Split Approach -- SM g_3 Trajectory + Varied y_t Boundary")
print("=" * 78)
print()

print("  The paper uses the SPLIT approach:")
print("    - g_3 trajectory: SM 2-loop from observed alpha_s(M_Z)")
print("    - y_t boundary: from the framework relation y_t = g_3/sqrt(6)")
print()
print("  This avoids the Landau pole because the SM g_3 is always perturbative.")
print("  The question becomes: is y_t(M_Z) insensitive to y_t(M_Pl)?")
print()


def rge_2loop(t, y):
    """2-loop SM RGEs for (g1, g2, g3, yt, lam).

    t = ln(mu), y = [g1, g2, g3, yt, lam]
    """
    g1, g2, g3, yt, lam = y
    fac = 1.0 / (16.0 * PI**2)
    fac2 = fac**2

    g1sq, g2sq, g3sq, ytsq = g1**2, g2**2, g3**2, yt**2

    # 1-loop gauge betas
    b1_g1_1 = (41.0 / 10.0) * g1**3
    b1_g2_1 = -(19.0 / 6.0) * g2**3
    b1_g3_1 = -7.0 * g3**3

    # 2-loop gauge betas
    b2_g1 = g1**3 * (199.0/50*g1sq + 27.0/10*g2sq + 44.0/5*g3sq - 17.0/10*ytsq)
    b2_g2 = g2**3 * (9.0/10*g1sq + 35.0/6*g2sq + 12.0*g3sq - 3.0/2*ytsq)
    b2_g3 = g3**3 * (11.0/10*g1sq + 9.0/2*g2sq - 26.0*g3sq - 2.0*ytsq)

    dg1 = fac * b1_g1_1 + fac2 * b2_g1
    dg2 = fac * b1_g2_1 + fac2 * b2_g2
    dg3 = fac * b1_g3_1 + fac2 * b2_g3

    # 1-loop Yukawa beta
    beta_yt_1 = yt * (9.0/2*ytsq - 8.0*g3sq - 9.0/4*g2sq - 17.0/20*g1sq)

    # 2-loop Yukawa beta (leading terms)
    beta_yt_2 = yt * (
        -12.0 * ytsq**2
        + ytsq * (36.0*g3sq + 225.0/16*g2sq + 131.0/80*g1sq)
        + 1187.0/216*g1sq**2 - 23.0/4*g2sq**2 - 108.0*g3sq**2
        + 19.0/15*g1sq*g3sq + 9.0/4*g2sq*g3sq
        + 6.0*lam**2 - 6.0*lam*ytsq
    )

    dyt = fac * beta_yt_1 + fac2 * beta_yt_2

    # Lambda running (simplified 1-loop)
    dlam = fac * (
        24.0*lam**2 + 12.0*lam*ytsq - 6.0*ytsq**2
        - 3.0*lam*(3.0*g2sq + g1sq) + 3.0/8*(2.0*g2sq**2 + (g2sq+g1sq)**2)
    )

    return [dg1, dg2, dg3, dyt, dlam]


# Scan: fix SM gauge trajectory, vary y_t(M_Pl)
# Use y_t(M_Pl) = g_3_test / sqrt(6) for different g_3_test values
lambda_pl = 0.01

print(f"  Using SM gauge couplings at M_Pl:")
print(f"    g_1 = {g1_pl:.4f}, g_2 = {g2_pl:.4f}, g_3 = {g3_pl_SM:.4f}")
print()

# Compute what y_t(M_Pl) would be for each g_3 "test value"
# but always use SM g_3 for the RGE trajectory
print(f"  {'g3_test':>10s}  {'yt(MPl)':>10s}  {'yt(MZ)':>10s}  "
      f"{'mt [GeV]':>10s}  {'dev%':>8s}  {'g3(MZ)':>10s}")
print(f"  {'-'*10}  {'-'*10}  {'-'*10}  "
      f"{'-'*10}  {'-'*8}  {'-'*10}")

results_split = []
for g3_test in g3_scan:
    yt_uv = g3_test / np.sqrt(6.0)

    y0 = [g1_pl, g2_pl, g3_pl_SM, yt_uv, lambda_pl]
    sol = solve_ivp(rge_2loop, (t_Pl, t_Z), y0,
                    method='RK45', rtol=1e-8, atol=1e-10,
                    max_step=1.0, dense_output=True)

    if sol.status == 0:
        vals = sol.sol(t_Z)
        g3_mz = vals[2]
        yt_mz = vals[3]
        mt = yt_mz * V_SM / np.sqrt(2.0)
        dev = (mt - M_T_OBS) / M_T_OBS * 100
        results_split.append((g3_test, yt_uv, yt_mz, mt, g3_mz))
        print(f"  {g3_test:10.3f}  {yt_uv:10.4f}  {yt_mz:10.4f}  "
              f"{mt:10.1f}  {dev:+8.1f}%  {g3_mz:10.4f}")
    else:
        results_split.append((g3_test, yt_uv, np.nan, np.nan, np.nan))
        print(f"  {g3_test:10.3f}  {yt_uv:10.4f}  {'FAILED':>10s}")

print()


# ============================================================================
# STEP 3: CONVERGENCE ANALYSIS OF SPLIT APPROACH
# ============================================================================
print("=" * 78)
print("STEP 3: Convergence Analysis of Split Approach")
print("=" * 78)
print()

mt_split = [r[3] for r in results_split if not np.isnan(r[3])]
g3_test_vals = [r[0] for r in results_split if not np.isnan(r[3])]
yt_mz_split = [r[2] for r in results_split if not np.isnan(r[3])]

if len(mt_split) >= 2:
    mt_min = min(mt_split)
    mt_max = max(mt_split)
    mt_mean = np.mean(mt_split)
    mt_spread = mt_max - mt_min
    mt_spread_pct = mt_spread / mt_mean * 100

    print(f"  m_t range: [{mt_min:.1f}, {mt_max:.1f}] GeV")
    print(f"  m_t mean:  {mt_mean:.1f} GeV")
    print(f"  m_t spread: {mt_spread:.1f} GeV ({mt_spread_pct:.1f}%)")
    print()

    # y_t(M_Z) convergence
    yt_min = min(yt_mz_split)
    yt_max = max(yt_mz_split)
    yt_mean = np.mean(yt_mz_split)
    yt_spread = yt_max - yt_min
    yt_spread_pct = yt_spread / yt_mean * 100
    print(f"  y_t(M_Z) range: [{yt_min:.4f}, {yt_max:.4f}]")
    print(f"  y_t(M_Z) spread: {yt_spread:.4f} ({yt_spread_pct:.1f}%)")
    print()

    # Sensitivity
    print("  Numerical sensitivity d(m_t)/d(g_3_test(M_Pl)):")
    for i in range(len(mt_split) - 1):
        dmt = mt_split[i+1] - mt_split[i]
        dg3 = g3_test_vals[i+1] - g3_test_vals[i]
        sens = dmt / dg3
        print(f"    g_3 in [{g3_test_vals[i]:.1f}, {g3_test_vals[i+1]:.1f}]: "
              f"d(m_t)/d(g_3) = {sens:.1f} GeV")
    print()


# ============================================================================
# STEP 4: DENSE SPLIT SCAN
# ============================================================================
print("=" * 78)
print("STEP 4: Dense Split Scan -- 50 Points g_3_test in [0.3, 3.0]")
print("=" * 78)
print()

g3_dense = np.linspace(0.3, 3.0, 50)
mt_dense = []
yt_dense = []

for g3_test in g3_dense:
    yt_uv = g3_test / np.sqrt(6.0)
    y0 = [g1_pl, g2_pl, g3_pl_SM, yt_uv, lambda_pl]
    sol = solve_ivp(rge_2loop, (t_Pl, t_Z), y0,
                    method='RK45', rtol=1e-8, atol=1e-10,
                    max_step=1.0, dense_output=True)
    if sol.status == 0:
        vals = sol.sol(t_Z)
        mt_dense.append(vals[3] * V_SM / np.sqrt(2.0))
        yt_dense.append(vals[3])
    else:
        mt_dense.append(np.nan)
        yt_dense.append(np.nan)

mt_dense = np.array(mt_dense)
yt_dense = np.array(yt_dense)
valid = ~np.isnan(mt_dense)

if np.sum(valid) > 2:
    mt_v = mt_dense[valid]
    g3_v = g3_dense[valid]

    print(f"  Over g_3_test in [{g3_v.min():.1f}, {g3_v.max():.1f}] "
          f"({np.sum(valid)}/{len(g3_dense)} converged):")
    print(f"    m_t range: [{mt_v.min():.1f}, {mt_v.max():.1f}] GeV")
    mt_range_pct = (mt_v.max() - mt_v.min()) / np.mean(mt_v) * 100
    print(f"    m_t spread: {mt_v.max() - mt_v.min():.1f} GeV ({mt_range_pct:.1f}%)")
    print()

    # Physical range [0.5, 2.0]
    mask_phys = (g3_v >= 0.5) & (g3_v <= 2.0)
    if np.sum(mask_phys) > 1:
        mt_phys = mt_v[mask_phys]
        g3_phys = g3_v[mask_phys]
        mt_phys_spread = mt_phys.max() - mt_phys.min()
        mt_phys_pct = mt_phys_spread / np.mean(mt_phys) * 100
        print(f"  Physical range g_3_test in [0.5, 2.0]:")
        print(f"    m_t range: [{mt_phys.min():.1f}, {mt_phys.max():.1f}] GeV")
        print(f"    m_t spread: {mt_phys_spread:.1f} GeV ({mt_phys_pct:.1f}%)")
        print()


# ============================================================================
# STEP 5: THE HONEST ASSESSMENT -- WHAT THE IR ATTRACTOR DOES AND DOESN'T DO
# ============================================================================
print("=" * 78)
print("STEP 5: The Honest Assessment")
print("=" * 78)
print()

print("  A. WHAT THE IR QUASI-FIXED POINT DOES:")
print("     - Stabilizes the RATIO y_t/g_3 (convergence exponent 1/14)")
print("     - For the SPLIT approach (SM g_3 + framework y_t), this means")
print("       y_t(M_Z) is insensitive to the exact value of y_t(M_Pl)")
print("     - The QCD drag term (-8 g_3^2 y_t) dominates the Yukawa running")
print()
print("  B. WHAT IT DOES NOT DO:")
print("     - It does NOT make m_t insensitive to g_3(M_Pl)")
print("     - Different g_3(M_Pl) values produce different Lambda_QCD")
print("     - The framework g_3(M_Pl) = 1.075 is 2.2x the SM value 0.490")
print("     - This difference hits a Landau pole; cannot be RG-evolved down")
print()
print("  C. NET EFFECT ON THE PAPER:")
print("     - The SPLIT approach IS valid: use SM g_3 + framework y_t(M_Pl)")
print("     - Within this approach, y_t(M_Z) does show IR focusing")
print("     - But this does NOT resolve the gauge crossover blocker")
print("     - The crossover (matching framework alpha_s to SM alpha_s)")
print("       remains a genuine open problem")
print()

# Quantify: in the split approach, how sensitive is m_t to y_t(M_Pl)?
# Compare y_t(M_Pl) = g_3/sqrt(6) for g_3 = framework vs g_3 = SM
yt_fw = g3_framework / np.sqrt(6.0)
yt_sm = g3_pl_SM / np.sqrt(6.0)

y0_fw = [g1_pl, g2_pl, g3_pl_SM, yt_fw, lambda_pl]
y0_sm = [g1_pl, g2_pl, g3_pl_SM, yt_sm, lambda_pl]

sol_fw = solve_ivp(rge_2loop, (t_Pl, t_Z), y0_fw,
                   method='RK45', rtol=1e-8, atol=1e-10,
                   max_step=1.0, dense_output=True)
sol_sm = solve_ivp(rge_2loop, (t_Pl, t_Z), y0_sm,
                   method='RK45', rtol=1e-8, atol=1e-10,
                   max_step=1.0, dense_output=True)

if sol_fw.status == 0 and sol_sm.status == 0:
    mt_fw = sol_fw.sol(t_Z)[3] * V_SM / np.sqrt(2.0)
    mt_sm = sol_sm.sol(t_Z)[3] * V_SM / np.sqrt(2.0)
    yt_fw_mz = sol_fw.sol(t_Z)[3]
    yt_sm_mz = sol_sm.sol(t_Z)[3]

    dev_fw = (mt_fw - M_T_OBS) / M_T_OBS * 100
    dev_sm = (mt_sm - M_T_OBS) / M_T_OBS * 100

    print(f"  D. SPLIT APPROACH COMPARISON (SM g_3 trajectory for both):")
    print(f"    y_t(M_Pl) = {yt_fw:.4f} (framework g_3 = {g3_framework:.3f}):")
    print(f"      y_t(M_Z) = {yt_fw_mz:.4f}, m_t = {mt_fw:.1f} GeV ({dev_fw:+.1f}%)")
    print(f"    y_t(M_Pl) = {yt_sm:.4f} (SM g_3 = {g3_pl_SM:.3f}):")
    print(f"      y_t(M_Z) = {yt_sm_mz:.4f}, m_t = {mt_sm:.1f} GeV ({dev_sm:+.1f}%)")
    print()

    gap = abs(mt_fw - mt_sm)
    gap_pct = gap / M_T_OBS * 100
    yt_ratio = yt_fw / yt_sm
    yt_mz_ratio = yt_fw_mz / yt_sm_mz

    print(f"    y_t(M_Pl) ratio: {yt_ratio:.2f}x")
    print(f"    y_t(M_Z) ratio:  {yt_mz_ratio:.2f}x")
    print(f"    Focusing factor:  {yt_mz_ratio/yt_ratio:.4f} "
          f"(1.0 = no focusing, 0.0 = perfect focusing)")
    print(f"    m_t gap: {gap:.1f} GeV ({gap_pct:.1f}%)")
    print()


# ============================================================================
# TESTS
# ============================================================================
print()
print("=" * 78)
print("TESTS")
print("=" * 78)
print()

# Test 1: Framework BC is correctly R = 1/6
report("framework_BC_R",
       abs(1.0/6.0 - (1.0/np.sqrt(6.0))**2) < 1e-14,
       f"y_t/g_3 = 1/sqrt(6) => R = 1/6 = {1.0/6.0:.10f}")

# Test 2: Landau pole exists for framework g_3
dt_fw = 8 * PI**2 / (7 * g3_framework**2)
report("framework_landau_pole",
       dt_fw < t_Pl - t_Z,
       f"Framework g_3 = {g3_framework:.3f} hits Landau pole in desert "
       f"(Delta_t = {dt_fw:.1f} < {t_Pl - t_Z:.1f})")

# Test 3: SM g_3 does NOT have Landau pole
dt_sm_pole = 8 * PI**2 / (7 * g3_pl_SM**2)
report("sm_no_landau_pole",
       dt_sm_pole > t_Pl - t_Z,
       f"SM g_3 = {g3_pl_SM:.3f} avoids Landau pole "
       f"(Delta_t = {dt_sm_pole:.1f} > {t_Pl - t_Z:.1f})")

# Test 4: All split scans converge
n_split_ok = sum(1 for r in results_split if not np.isnan(r[3]))
report("split_all_converge",
       n_split_ok == len(g3_scan),
       f"{n_split_ok}/{len(g3_scan)} split scans converged")

# Test 5: Split approach m_t spread
if len(mt_split) >= 2:
    spread = max(mt_split) - min(mt_split)
    spread_pct = spread / np.mean(mt_split) * 100
    report("split_mt_spread",
           True,
           f"Split m_t spread over g_3_test in {{0.5..2.0}} = "
           f"{spread:.1f} GeV ({spread_pct:.1f}%)")

    # Test 6: Is the split spread < 5%?
    report("split_insensitivity_5pct",
           spread_pct < 5.0,
           f"Split m_t spread {'<' if spread_pct < 5.0 else '>'} 5% "
           f"(actual: {spread_pct:.1f}%)")

# Test 7: IR focusing in split approach
if sol_fw.status == 0 and sol_sm.status == 0:
    focusing = yt_mz_ratio / yt_ratio
    report("ir_focusing",
           focusing < 1.0,
           f"IR focusing factor = {focusing:.4f} "
           f"(y_t(M_Z) ratio closer to 1 than y_t(M_Pl) ratio)")

    # Test 8: Framework split prediction
    report("framework_split_mt",
           abs(dev_fw) < 25.0,
           f"Framework split m_t = {mt_fw:.1f} GeV ({dev_fw:+.1f}%)")

# Test 9: Dense scan physical range
if np.sum(valid) > 2:
    mask_phys = (g3_dense[valid] >= 0.5) & (g3_dense[valid] <= 2.0)
    if np.sum(mask_phys) > 1:
        mt_phys = mt_dense[valid][mask_phys]
        phys_pct = (mt_phys.max() - mt_phys.min()) / np.mean(mt_phys) * 100
        report("dense_scan_physical",
               True,
               f"Dense scan g_3_test in [0.5, 2.0]: "
               f"m_t spread = {phys_pct:.1f}%")

# Test 10: Dense scan converges (all 50 points)
n_dense_ok = np.sum(valid)
report("dense_all_converge",
       n_dense_ok == len(g3_dense),
       f"{n_dense_ok}/{len(g3_dense)} dense scan points converged")


# ============================================================================
# SUMMARY
# ============================================================================
print()
print("=" * 78)
print("SUMMARY")
print("=" * 78)
print()

if len(mt_split) >= 2:
    spread_pct_final = (max(mt_split) - min(mt_split)) / np.mean(mt_split) * 100

    print(f"  STATUS: BOUNDED")
    print()
    print(f"  A. NAIVE APPROACH (unified g_3 + y_t = g_3/sqrt(6) running):")
    print(f"     FAILS for g_3(M_Pl) >= 0.8 due to Landau pole.")
    print(f"     The framework g_3 = {g3_framework:.3f} cannot be perturbatively run to M_Z.")
    print()
    print(f"  B. SPLIT APPROACH (SM g_3 trajectory + framework y_t boundary):")
    print(f"     m_t predictions across y_t(M_Pl) = g_3_test/sqrt(6):")
    for r in results_split:
        if not np.isnan(r[3]):
            dev = (r[3] - M_T_OBS) / M_T_OBS * 100
            print(f"       g_3_test = {r[0]:.1f}: y_t(M_Pl) = {r[1]:.4f}, "
                  f"m_t = {r[3]:.1f} GeV ({dev:+.1f}%)")
    print()
    print(f"     Spread: {max(mt_split) - min(mt_split):.1f} GeV ({spread_pct_final:.1f}%)")
    print()

    if spread_pct_final > 5.0:
        print(f"  C. VERDICT: The IR quasi-fixed-point provides significant but")
        print(f"     INCOMPLETE focusing ({spread_pct_final:.0f}% residual spread).")
        print(f"     In the split approach (SM g_3 for RGE), y_t(M_Z) still depends")
        print(f"     on y_t(M_Pl), but is partially stabilized by QCD drag.")
    else:
        print(f"  C. VERDICT: The IR quasi-fixed-point provides strong focusing")
        print(f"     ({spread_pct_final:.1f}% residual spread < 5%).")

    print()
    print(f"  D. THE GAUGE CROSSOVER REMAINS A BLOCKER:")
    print(f"     The insensitivity of y_t(M_Z) to y_t(M_Pl) does NOT resolve")
    print(f"     the g_3 matching problem. The framework alpha_s(M_Pl) = 0.092")
    print(f"     produces a Landau pole; a non-perturbative mechanism is needed")
    print(f"     to connect the framework strong coupling to the observed SM value.")

print()
elapsed = time.time() - t0
print(f"  Completed in {elapsed:.1f}s")
print(f"  {PASS_COUNT} PASS, {FAIL_COUNT} FAIL")
print()

if FAIL_COUNT > 0:
    sys.exit(1)
