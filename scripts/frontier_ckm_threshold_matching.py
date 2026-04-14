#!/usr/bin/env python3
"""
CKM Threshold Matching: V_cb from the Taste Staircase with 2-Loop RG
======================================================================

STATUS: BOUNDED -- 2-loop RG through the taste staircase, with the
        correct sign convention verified against ODE integration.

CRITICAL FINDING:
  The 1-loop running formulas in frontier_ckm_nonperturbative.py and
  frontier_yt_ward_staircase.py used the WRONG sign convention:

    WRONG:   1/alpha(lo) = 1/alpha(hi) + b_0/(2pi) * ln(mu_hi/mu_lo)
    CORRECT: 1/alpha(lo) = 1/alpha(hi) + b_0/(2pi) * ln(mu_lo/mu_hi)
           = 1/alpha(hi) - b_0/(2pi) * ln(mu_hi/mu_lo)

  The correct formula (verified by ODE integration) shows that in the
  non-AF regime (b_0 < 0), the coupling DECREASES running from M_Pl
  to lower scales. This is physically correct: non-AF means the coupling
  grows toward the UV (like QED), not the IR.

  Consequence: the taste staircase does NOT amplify the coupling.
  The V_cb bracket [0.015, 0.060] from frontier_ckm_nonperturbative.py
  was based on this sign error. The correct staircase gives an
  EVEN SMALLER effective coupling than the naive perturbative one.

WHAT THIS SCRIPT DOES:
  1. Verifies the sign convention against exact ODE integration
  2. Builds the full staircase RG from M_Pl to v with 2-LOOP running
  3. Computes V_cb and V_us with the correct coupling
  4. Identifies what mechanism IS needed to close the gap
  5. Tests whether the coupling should be evaluated at a DIFFERENT scale

PStack experiment: frontier-ckm-threshold-matching
Self-contained: numpy + scipy only.
"""

from __future__ import annotations

import sys
import time

import numpy as np

try:
    from scipy.integrate import solve_ivp
except ImportError:
    print("ERROR: scipy required for 2-loop ODE integration. pip install scipy")
    sys.exit(1)

np.set_printoptions(precision=10, linewidth=120, suppress=True)

# -- Test infrastructure -----------------------------------------------

PASS_COUNT = 0
FAIL_COUNT = 0
EXACT_PASS = 0
EXACT_FAIL = 0
BOUNDED_PASS = 0
BOUNDED_FAIL = 0
HONEST_COUNT = 0


def check(name, condition, detail="", kind="BOUNDED"):
    global PASS_COUNT, FAIL_COUNT, EXACT_PASS, EXACT_FAIL
    global BOUNDED_PASS, BOUNDED_FAIL
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


# ======================================================================
# Physical constants (from the framework -- zero imports)
# ======================================================================

PI = np.pi
N_C = 3
C_A = N_C                            # = 3
C_F = (N_C**2 - 1) / (2 * N_C)      # = 4/3
T_F = 0.5

M_PL = 1.2209e19      # GeV (unreduced Planck mass = 1/a)
V_EW = 246.22         # GeV (measured Higgs VEV)

# Framework couplings from the axiom g_bare = 1
PLAQ_MC = 0.5934      # SU(3) plaquette at beta = 6
U0 = PLAQ_MC**0.25    # tadpole improvement ~ 0.8777
ALPHA_LM = 1.0 / (4.0 * PI * U0)    # Lepage-Mackenzie ~ 0.0907
ALPHA_V_MPL = 1.0 / (4.0 * PI * U0**2)  # V-scheme at M_Pl ~ 0.1033

# Taste staircase parameters
N_TASTE = 8       # 2^3 spatial tastes
N_GEN = 6         # 6 quark flavors per taste
N_STEPS = 16      # number of taste thresholds (hierarchy formula exponent)

# CKM observables (for comparison only)
V_CB_PDG = 0.0422
V_US_PDG = 0.2243
V_UB_PDG = 0.00394

# Quark masses
M_UP = 2.16e-3
M_CHARM = 1.27
M_TOP = 172.76
M_DOWN = 4.67e-3
M_STRANGE = 0.093
M_BOTTOM = 4.18

# S_23 formula parameters (from frontier_ckm_s23_analytic.py)
S_23_0 = 1.073    # undressed Symanzik overlap ratio
ETA_DOWN = 0.3244  # EWSB parameter from c_12^d/c_23 ratio
F_EWSB = 1.0 / (1.0 + ETA_DOWN)  # EWSB suppression
r_wu_wd = 1.014   # derived EW ratio W_up/W_down

# V_cb kinematic factor
sqrt_ms_mb = np.sqrt(M_STRANGE / M_BOTTOM)
sqrt_mc_mt = np.sqrt(M_CHARM / M_TOP)
vcb_kinematic = abs(sqrt_ms_mb - r_wu_wd * sqrt_mc_mt)

# V_us kinematic factor (GST relation)
vus_gst = np.sqrt(M_DOWN / M_STRANGE)

# Perturbative V_cb (baseline, using alpha_s(v) directly)
L_enh = np.log(M_PL / V_EW) / (4.0 * PI)
c23_pert = ALPHA_V_MPL * N_C * L_enh / PI * S_23_0 * F_EWSB
vcb_pert = c23_pert * vcb_kinematic


# ======================================================================
# Beta function coefficients
# ======================================================================

def beta_coefficients(n_f):
    """1-loop and 2-loop QCD beta function coefficients.

    Beta function: d(alpha)/d(ln mu) = -b0/(2pi)*alpha^2 - b1/(4pi^2)*alpha^3
    """
    b_0 = (11.0 * C_A - 4.0 * T_F * n_f) / 3.0
    b_1 = 34.0 / 3.0 * C_A**2 - (20.0 / 3.0 * C_A + 4.0 * C_F) * T_F * n_f
    return b_0, b_1


def run_1loop_correct(alpha_high, mu_high, mu_low, n_f):
    """CORRECT 1-loop running from mu_high to mu_low.

    From d(alpha)/d(ln mu) = -b_0/(2 pi) alpha^2:
        1/alpha(mu) = 1/alpha(mu_0) + b_0/(2 pi) * ln(mu/mu_0)

    Setting mu_0 = mu_high, mu = mu_low:
        1/alpha(mu_low) = 1/alpha(mu_high) + b_0/(2 pi) * ln(mu_low/mu_high)
    """
    b_0, _ = beta_coefficients(n_f)
    inv_alpha_low = 1.0 / alpha_high + b_0 / (2.0 * PI) * np.log(mu_low / mu_high)
    if inv_alpha_low <= 0:
        return np.inf  # Landau pole
    return 1.0 / inv_alpha_low


def run_2loop(alpha_high, mu_high, mu_low, n_f, max_alpha=50.0):
    """Run alpha_s from mu_high to mu_low at 2-loop via ODE integration."""
    if mu_high <= mu_low:
        return alpha_high

    lnmu_high = np.log(mu_high)
    lnmu_low = np.log(mu_low)

    def rhs(t, y):
        a = min(max(y[0], 0.0), max_alpha)
        b_0, b_1 = beta_coefficients(n_f)
        return [-b_0 / (2.0 * PI) * a**2 - b_1 / (4.0 * PI**2) * a**3]

    sol = solve_ivp(
        rhs,
        [lnmu_high, lnmu_low],
        [alpha_high],
        method='RK45',
        rtol=1e-12, atol=1e-15,
        max_step=0.5,
    )

    if not sol.success:
        return max_alpha

    result = sol.y[0, -1]
    return min(max(result, 0.0), max_alpha)


def threshold_correction(alpha_s, n_f_decouple):
    """O(alpha^2) threshold matching correction when fermions decouple.

    At a threshold mu = m_heavy:
      alpha_s(mu-) = alpha_s(mu+) * (1 + delta)
    where delta = (alpha_s/pi)^2 * (11/72) * n_f_decouple
    """
    delta = (alpha_s / PI)**2 * (11.0 / 72.0) * n_f_decouple
    return delta


# ======================================================================
print("=" * 78)
print("CKM THRESHOLD MATCHING: V_cb FROM THE TASTE STAIRCASE")
print("=" * 78)
t0 = time.time()

print(f"""
  FRAMEWORK PARAMETERS:
    M_Pl = {M_PL:.4e} GeV
    v    = {V_EW} GeV
    alpha_LM = {ALPHA_LM:.6f}
    alpha_V(M_Pl) = {ALPHA_V_MPL:.6f}

  PERTURBATIVE BASELINE:
    c_23(pert)  = {c23_pert:.4f}
    V_cb(pert)  = {vcb_pert:.5f}  (PDG: {V_CB_PDG})
    shortfall   = {(vcb_pert/V_CB_PDG - 1)*100:+.1f}%
    Need alpha_eff ~ {V_CB_PDG / vcb_kinematic * PI / (N_C * L_enh * S_23_0 * F_EWSB):.3f} to match PDG
""")


# ======================================================================
# PART 1: SIGN CONVENTION VERIFICATION
# ======================================================================
print("=" * 78)
print("PART 1: SIGN CONVENTION VERIFICATION")
print("=" * 78)

print("""
  The beta function ODE: d(alpha)/d(ln mu) = -b_0/(2pi) alpha^2
  Exact solution:
    1/alpha(mu) = 1/alpha(mu_0) + b_0/(2pi) * ln(mu/mu_0)

  For AF (b_0 > 0): running from UV to IR (mu decreasing),
    ln(mu/mu_0) < 0, so 1/alpha(mu) < 1/alpha(mu_0), alpha(mu) > alpha(mu_0)
    => coupling GROWS toward IR. Correct.

  For non-AF (b_0 < 0): running from UV to IR (mu decreasing),
    ln(mu/mu_0) < 0 and b_0 < 0, so b_0*ln < 0 but wait...
    b_0 < 0 and ln(mu_lo/mu_hi) < 0 => b_0 * ln > 0
    So 1/alpha(mu_lo) > 1/alpha(mu_hi) => alpha(mu_lo) < alpha(mu_hi)
    => coupling SHRINKS toward IR. Correct (non-AF = coupling grows in UV).
""")

# Verify: known QCD running
alpha_mz = 0.118
mu_mz = 91.2
mu_1gev = 1.0
n_f_5 = 5

alpha_1gev_1loop = run_1loop_correct(alpha_mz, mu_mz, mu_1gev, n_f_5)
alpha_1gev_2loop = run_2loop(alpha_mz, mu_mz, mu_1gev, n_f_5)

print(f"  QCD VERIFICATION (known physics):")
print(f"    alpha_s(M_Z) = {alpha_mz} -> alpha_s(1 GeV):")
print(f"    1-loop formula: {alpha_1gev_1loop:.4f}  (should be ~0.3-0.5)")
print(f"    2-loop ODE:     {alpha_1gev_2loop:.4f}")

check("qcd_running_correct_direction",
      alpha_1gev_1loop > alpha_mz and alpha_1gev_2loop > alpha_mz,
      f"alpha grows from {alpha_mz} to {alpha_1gev_1loop:.3f} (1L) / "
      f"{alpha_1gev_2loop:.3f} (2L) going to IR",
      kind="EXACT")

check("1loop_2loop_same_direction_qcd",
      alpha_1gev_1loop > alpha_mz and alpha_1gev_2loop > alpha_mz
      and alpha_1gev_1loop < alpha_1gev_2loop,
      f"1L={alpha_1gev_1loop:.4f} < 2L={alpha_1gev_2loop:.4f}, both > {alpha_mz} "
      f"(2-loop runs faster due to b_1 > 0 for n_f=5, large range to 1 GeV)",
      kind="EXACT")

# Verify: non-AF regime
alpha_nonaf_1loop = run_1loop_correct(ALPHA_V_MPL, M_PL, M_PL * ALPHA_LM, 45)
alpha_nonaf_2loop = run_2loop(ALPHA_V_MPL, M_PL, M_PL * ALPHA_LM, 45)

print(f"\n  NON-AF VERIFICATION (n_f=45, b_0={(11*C_A - 4*T_F*45)/3:.1f}):")
print(f"    alpha(M_Pl) = {ALPHA_V_MPL:.6f} -> alpha(m_1 = {M_PL*ALPHA_LM:.3e} GeV):")
print(f"    1-loop formula: {alpha_nonaf_1loop:.6f}")
print(f"    2-loop ODE:     {alpha_nonaf_2loop:.6f}")

check("nonaf_coupling_decreases",
      alpha_nonaf_1loop < ALPHA_V_MPL and alpha_nonaf_2loop < ALPHA_V_MPL,
      f"alpha DECREASES from {ALPHA_V_MPL:.4f} to {alpha_nonaf_1loop:.4f} (1L) / "
      f"{alpha_nonaf_2loop:.4f} (2L) in non-AF regime",
      kind="EXACT")

check("formula_matches_ode_nonaf",
      abs(alpha_nonaf_1loop - alpha_nonaf_2loop) / alpha_nonaf_1loop < 0.30,
      f"1L={alpha_nonaf_1loop:.6f} vs 2L={alpha_nonaf_2loop:.6f} "
      f"({abs(alpha_nonaf_1loop/alpha_nonaf_2loop - 1)*100:.1f}% diff)",
      kind="BOUNDED")

# Cross-check: the OLD wrong formula
b0_45, _ = beta_coefficients(45)
inv_wrong = 1.0 / ALPHA_V_MPL + b0_45 / (2 * PI) * np.log(M_PL / (M_PL * ALPHA_LM))
alpha_wrong = 1.0 / inv_wrong if inv_wrong > 0 else float('inf')

print(f"\n  SIGN ERROR DIAGNOSIS:")
print(f"    OLD (wrong) formula: alpha = {alpha_wrong:.6f} (coupling GROWS -- wrong for non-AF)")
print(f"    NEW (correct) formula: alpha = {alpha_nonaf_1loop:.6f} (coupling SHRINKS -- correct)")
print(f"    2-loop ODE (ground truth): alpha = {alpha_nonaf_2loop:.6f}")

check("old_formula_is_wrong",
      abs(alpha_wrong - ALPHA_V_MPL) > 0.05 and alpha_wrong > ALPHA_V_MPL,
      f"old formula gives {alpha_wrong:.4f} > {ALPHA_V_MPL:.4f} (wrong direction)",
      kind="EXACT")


# ======================================================================
# PART 2: FULL 2-LOOP STAIRCASE RG
# ======================================================================
print("\n" + "=" * 78)
print("PART 2: FULL 2-LOOP STAIRCASE RG WITH CORRECT SIGN CONVENTION")
print("=" * 78)


def build_staircase_2loop(alpha_start, n_steps=N_STEPS,
                          include_threshold_corr=True, verbose=True):
    """Run alpha_s through the taste staircase with 2-loop RG.

    Each threshold m_k = M_Pl * alpha_LM^k.
    Between threshold k and k+1: n_f = max(6, 48 - 3*(k+1)).
    """
    thresholds = [M_PL * ALPHA_LM**k for k in range(n_steps + 1)]

    alpha_values = [alpha_start]
    mu_values = [M_PL]
    n_f_values = []
    alpha_current = alpha_start

    if verbose:
        print(f"\n  {'k':>3} {'mu_hi (GeV)':>14} {'mu_lo (GeV)':>14} "
              f"{'n_f':>5} {'b_0':>7} {'b_1':>8} "
              f"{'alpha_in':>10} {'a_out(1L)':>10} {'a_out(2L)':>10}")
        print(f"  {'---':>3} {'-'*14} {'-'*14} "
              f"{'-'*5} {'-'*7} {'-'*8} "
              f"{'-'*10} {'-'*10} {'-'*10}")

    for k in range(n_steps):
        mu_high = thresholds[k]
        mu_low = thresholds[k + 1]
        n_f = max(6, 48 - 3 * (k + 1))
        b_0, b_1 = beta_coefficients(n_f)

        # 1-loop (correct sign) for comparison
        alpha_1L = run_1loop_correct(alpha_current, mu_high, mu_low, n_f)

        # 2-loop ODE (ground truth)
        alpha_2L = run_2loop(alpha_current, mu_high, mu_low, n_f)

        # Threshold matching correction
        n_f_decouple = 3
        if include_threshold_corr and k < n_steps - 1:
            delta = threshold_correction(alpha_2L, n_f_decouple)
            alpha_matched = alpha_2L * (1.0 + delta)
        else:
            alpha_matched = alpha_2L

        n_f_values.append(n_f)

        if verbose:
            print(f"  {k:3d} {mu_high:14.4e} {mu_low:14.4e} "
                  f"{n_f:5d} {b_0:7.1f} {b_1:8.1f} "
                  f"{alpha_current:10.6f} {alpha_1L:10.6f} {alpha_2L:10.6f}")

        alpha_values.append(alpha_matched)
        mu_values.append(mu_low)
        alpha_current = alpha_matched

    return {
        'alpha_values': alpha_values,
        'mu_values': mu_values,
        'n_f_values': n_f_values,
        'alpha_at_v': alpha_values[-1],
        'thresholds': thresholds,
    }


staircase = build_staircase_2loop(ALPHA_V_MPL)

alpha_v_staircase = staircase['alpha_at_v']

print(f"""
  STAIRCASE RESULT:
    alpha_s(M_Pl)        = {ALPHA_V_MPL:.6f}
    alpha_s(v) staircase = {alpha_v_staircase:.6f}
    Ratio: {alpha_v_staircase/ALPHA_V_MPL:.3f}x

  The coupling {
    'DECREASES' if alpha_v_staircase < ALPHA_V_MPL
    else 'INCREASES'} from M_Pl to v.
  The non-AF regime (k=0 to k~5) pulls the coupling DOWN.
  The AF regime (k~6 to k=15) pulls the coupling back UP.
""")

# Identify the AF crossover
print(f"  COUPLING AT KEY THRESHOLDS:")
for k in range(N_STEPS):
    n_f = max(6, 48 - 3 * (k + 1))
    b_0, _ = beta_coefficients(n_f)
    af_str = "AF" if b_0 > 0 else "non-AF"
    alpha_k = staircase['alpha_values'][k + 1]
    mu_k = staircase['mu_values'][k + 1]
    print(f"    k={k:2d}: mu = {mu_k:10.3e} GeV, alpha = {alpha_k:.6f}, "
          f"n_f={n_f:2d}, b_0={b_0:+5.1f} ({af_str})")

# Find the minimum coupling (the trough)
alpha_arr = np.array(staircase['alpha_values'])
min_idx = np.argmin(alpha_arr)
print(f"\n  Minimum coupling: alpha = {alpha_arr[min_idx]:.6f} at step k={min_idx}")

check("2loop_finite",
      0 < alpha_v_staircase < 10,
      f"alpha_s(v) = {alpha_v_staircase:.6f} finite (no Landau pole at 2-loop)",
      kind="EXACT")

check("staircase_sign_correct",
      alpha_v_staircase < ALPHA_V_MPL,
      f"alpha_s(v) = {alpha_v_staircase:.6f} < alpha_s(M_Pl) = {ALPHA_V_MPL:.6f} "
      f"(non-AF staircase DECREASES coupling, now correctly computed)",
      kind="EXACT")


# ======================================================================
# PART 3: V_cb WITH CORRECT COUPLING
# ======================================================================
print("\n" + "=" * 78)
print("PART 3: V_cb WITH CORRECT STAIRCASE COUPLING")
print("=" * 78)


def compute_c23_rg_integral(staircase_data):
    """Compute c_23 from the RG-improved Wilson coefficient.

    c_23 = (N_c / pi) * S_23 * F_EWSB * integral

    where integral = int_{v}^{M_Pl} (d mu / mu) * alpha_s(mu) / (4 pi)

    This integral is the RG log-enhanced Wilson coefficient. It equals
    alpha_eff * ln(M_Pl/v) / (4 pi) where alpha_eff is the log-space
    averaged coupling.
    """
    alpha_vals = staircase_data['alpha_values']
    mu_vals = staircase_data['mu_values']
    n_steps = len(alpha_vals) - 1

    I_rg = 0.0
    for k in range(n_steps):
        mu_hi = mu_vals[k]
        mu_lo = mu_vals[k + 1]
        if mu_lo < V_EW:
            mu_lo = V_EW
        if mu_hi <= V_EW:
            break

        alpha_avg = (alpha_vals[k] + alpha_vals[k + 1]) / 2.0
        L_k = np.log(mu_hi / mu_lo)
        I_rg += alpha_avg * L_k / (4.0 * PI)

    c_23 = N_C / PI * I_rg * S_23_0 * F_EWSB
    alpha_eff = I_rg / (np.log(M_PL / V_EW) / (4 * PI))

    return I_rg, c_23, alpha_eff


I_rg, c23_staircase, alpha_eff = compute_c23_rg_integral(staircase)
vcb_staircase = c23_staircase * vcb_kinematic

# Also compute with alpha_s evaluated DIRECTLY at v (the old approach)
c23_at_v = alpha_v_staircase * N_C * L_enh / PI * S_23_0 * F_EWSB
vcb_at_v = c23_at_v * vcb_kinematic

# The needed effective alpha
alpha_needed = V_CB_PDG / (vcb_kinematic * N_C * L_enh / PI * S_23_0 * F_EWSB)

print(f"""
  METHOD 1: alpha_s(v) directly (coupling at EW scale from staircase)
    alpha_s(v) = {alpha_v_staircase:.6f}
    c_23 = {c23_at_v:.6f}
    V_cb = {vcb_at_v:.5f}  (PDG: {V_CB_PDG})
    Deviation: {(vcb_at_v/V_CB_PDG - 1)*100:+.1f}%

  METHOD 2: RG-improved integral (log-space weighted average)
    alpha_eff = {alpha_eff:.6f}
    c_23 = {c23_staircase:.6f}
    V_cb = {vcb_staircase:.5f}
    Deviation: {(vcb_staircase/V_CB_PDG - 1)*100:+.1f}%

  METHOD 3: Naive perturbative (alpha_V(M_Pl) without running)
    alpha = {ALPHA_V_MPL:.6f}
    c_23 = {c23_pert:.6f}
    V_cb = {vcb_pert:.5f}
    Deviation: {(vcb_pert/V_CB_PDG - 1)*100:+.1f}%

  NEEDED:
    alpha_eff ~ {alpha_needed:.4f}
    Enhancement factor needed: {alpha_needed/ALPHA_V_MPL:.1f}x over alpha_V(M_Pl)

  THE GAP: all three methods give V_cb far below PDG.
    The staircase makes it WORSE, not better.
""")


# ======================================================================
# PART 4: WHERE DOES THE 2.8x NEED TO COME FROM?
# ======================================================================
print("=" * 78)
print("PART 4: DIAGNOSING THE V_cb GAP")
print("=" * 78)

print(f"""
  The V_cb formula:
    V_cb = c_23 * |sqrt(m_s/m_b) - r_W * sqrt(m_c/m_t)|
    c_23 = (alpha_eff * N_c / pi) * L_enh * S_23 * F_EWSB

  Breaking down the needed vs. derived values:

    kinematic factor = {vcb_kinematic:.6f}
    L_enh = ln(M_Pl/v)/(4 pi) = {L_enh:.4f}
    S_23  = {S_23_0:.4f}  (undressed Symanzik)
    F_EWSB = {F_EWSB:.4f}  (eta = {ETA_DOWN:.4f})
    N_c/pi = {N_C/PI:.4f}

    c_23(needed) = V_cb(PDG) / kinematic = {V_CB_PDG/vcb_kinematic:.4f}
    alpha_needed = c_23(needed) * pi / (N_c * L_enh * S_23 * F_EWSB) = {alpha_needed:.4f}
    alpha_s(v) from staircase = {alpha_v_staircase:.6f}

    Gap factor: alpha_needed / alpha_s(v) = {alpha_needed/alpha_v_staircase:.1f}x

  POSSIBLE RESOLUTIONS:

  A. The coupling used for the NNI operator is NOT the running coupling
     at the EW scale. It is the LATTICE coupling at the taste-breaking
     scale (= 1/a = M_Pl). At that scale, the coupling is alpha_V(M_Pl)
     = {ALPHA_V_MPL:.4f}. With the L_enh factor capturing the running,
     the perturbative result V_cb = {vcb_pert:.5f} is the correct
     baseline. The gap is then {alpha_needed/ALPHA_V_MPL:.1f}x.

  B. The NNI coefficient receives non-perturbative contributions beyond
     1-gluon exchange (instanton, taste-scalar, confinement effects).
     frontier_ckm_nonperturbative.py tested these and found them small.

  C. The S_23 overlap integral is larger than the free-field value.
     Strong-coupling gauge configurations could enhance the inter-valley
     overlap.

  D. Higher-order perturbative corrections. The c_23 formula is only
     1-loop. NLO corrections to the Wilson coefficient could be O(1).

  E. The correct picture is that alpha_s should be evaluated at
     Lambda_QCD ~ 200 MeV (the confinement scale), where alpha_s ~ 1.
     The NNI operator is a confining-scale effect.
""")

# Test resolution E: evaluate at Lambda_QCD
alpha_at_lambda = 0.30  # alpha_s at ~2 GeV from PDG
c23_at_lambda = alpha_at_lambda * N_C * L_enh / PI * S_23_0 * F_EWSB
vcb_at_lambda = c23_at_lambda * vcb_kinematic

alpha_at_2gev = 0.30
alpha_at_1gev = 0.50

print(f"  Resolution E test: evaluate alpha_s at a low scale")
print(f"    alpha_s(2 GeV) ~ {alpha_at_2gev}: V_cb = {vcb_at_lambda:.5f} "
      f"({(vcb_at_lambda/V_CB_PDG - 1)*100:+.1f}%)")
c23_1gev = alpha_at_1gev * N_C * L_enh / PI * S_23_0 * F_EWSB
vcb_1gev = c23_1gev * vcb_kinematic
print(f"    alpha_s(1 GeV) ~ {alpha_at_1gev}: V_cb = {c23_1gev * vcb_kinematic:.5f} "
      f"({(vcb_1gev/V_CB_PDG - 1)*100:+.1f}%)")

# Resolution E actually works! alpha_s ~ 0.3 gives V_cb close to PDG.
# But this is NOT derived -- it uses the SM value of alpha_s.

# What alpha_s at v should we get from proper framework running?
# Using the CORRECT staircase + AF running from the taste scale to v:
# After all tastes decouple, n_f = 6 (AF). The coupling grows toward IR.
# But it starts from a very small value after the non-AF staircase.

# The question: does the AF running from the last taste threshold to v
# amplify the coupling enough?
last_taste_scale = M_PL * ALPHA_LM**N_TASTE  # after all 8 tastes decouple
alpha_after_tastes = staircase['alpha_values'][N_TASTE]  # at step 8
print(f"\n  After all tastes decouple:")
print(f"    mu = {last_taste_scale:.3e} GeV")
print(f"    alpha_s = {alpha_after_tastes:.6f}")

# Run from there to v with n_f = 6 (AF)
alpha_v_af = run_2loop(alpha_after_tastes, last_taste_scale, V_EW, 6)
print(f"    alpha_s(v) after AF running = {alpha_v_af:.6f}")


# ======================================================================
# PART 5: V_us (CABIBBO ANGLE) -- STRUCTURAL PREDICTION
# ======================================================================
print("\n" + "=" * 78)
print("PART 5: V_us FROM THE GST RELATION")
print("=" * 78)

print(f"""
  The Cabibbo angle is dominated by the Gatto-Sartori-Tonin relation:
    |V_us| = sqrt(m_d / m_s) = {vus_gst:.4f}
  compared to PDG {V_US_PDG} ({(vus_gst/V_US_PDG - 1)*100:+.2f}%)

  This is a structural prediction that does NOT depend on the absolute
  coupling normalization. It follows purely from the NNI texture and
  the mass hierarchy. The staircase coupling enters only through O(1)
  corrections to the texture coefficients.

  V_us is the STRONGEST CKM prediction of the framework.
""")

check("vus_gst",
      abs(vus_gst / V_US_PDG - 1) < 0.01,
      f"|V_us| = {vus_gst:.4f} vs PDG {V_US_PDG} ({(vus_gst/V_US_PDG - 1)*100:+.2f}%)",
      kind="BOUNDED")


# ======================================================================
# PART 6: SENSITIVITY ANALYSIS
# ======================================================================
print("\n" + "=" * 78)
print("PART 6: SENSITIVITY ANALYSIS")
print("=" * 78)

print("""
  How does V_cb depend on the staircase parameters?
""")

# (a) Starting coupling
print(f"  --- (a) Starting coupling alpha_V(M_Pl) variation ---")
for alpha_start in [0.05, 0.08, 0.092, 0.1033, 0.12, 0.15]:
    sc = build_staircase_2loop(alpha_start, verbose=False)
    _, _, a_eff = compute_c23_rg_integral(sc)
    c23_v = a_eff * N_C * L_enh / PI * S_23_0 * F_EWSB
    # Actually use the integral directly
    _, c23_v, _ = compute_c23_rg_integral(sc)
    vcb_v = c23_v * vcb_kinematic
    print(f"    alpha_V(M_Pl) = {alpha_start:.4f}: alpha_s(v) = {sc['alpha_at_v']:.6f}, "
          f"V_cb = {vcb_v:.5f} ({(vcb_v/V_CB_PDG - 1)*100:+.1f}%)")

# (b) Number of thresholds
print(f"\n  --- (b) 8-step staircase (one per taste, n_f drops by 6) ---")
thresholds_8 = [M_PL * ALPHA_LM**(2*k) for k in range(9)]
thresholds_8[-1] = V_EW

alpha_8_vals = [ALPHA_V_MPL]
alpha_8_run = ALPHA_V_MPL
for k in range(8):
    mu_hi = thresholds_8[k]
    mu_lo = thresholds_8[k + 1]
    n_f_k = max(6, (8 - k - 1) * 6)
    alpha_8_run = run_2loop(alpha_8_run, mu_hi, mu_lo, n_f_k)
    alpha_8_vals.append(alpha_8_run)
    b_0_k, _ = beta_coefficients(n_f_k)
    print(f"    k={k}: n_f={n_f_k}, b_0={b_0_k:+5.1f}, "
          f"alpha: {alpha_8_vals[k]:.6f} -> {alpha_8_run:.6f}")

print(f"    alpha_s(v) [8-step] = {alpha_8_run:.6f}")

# (c) What if we use alpha_bare instead of alpha_V?
alpha_bare = 1.0 / (4 * PI)  # g^2/(4pi) with g=1
print(f"\n  --- (c) Starting from alpha_bare = g^2/(4pi) = {alpha_bare:.6f} ---")
sc_bare = build_staircase_2loop(alpha_bare, verbose=False)
print(f"    alpha_s(v) = {sc_bare['alpha_at_v']:.6f}")

# (d) What if we use the wrong convention (for comparison)?
print(f"\n  --- (d) WRONG sign convention (what the old scripts computed) ---")
alpha_wrong = ALPHA_V_MPL
for k in range(N_STEPS):
    mu_hi = M_PL * ALPHA_LM**k
    mu_lo = M_PL * ALPHA_LM**(k + 1)
    n_f_k = max(6, 48 - 3 * (k + 1))
    b_0_k, _ = beta_coefficients(n_f_k)
    inv_wrong = 1.0 / alpha_wrong + b_0_k / (2 * PI) * np.log(mu_hi / mu_lo)
    if inv_wrong <= 0:
        alpha_wrong = 10.0  # cap at Landau pole
    else:
        alpha_wrong = 1.0 / inv_wrong
        alpha_wrong = min(alpha_wrong, 1.0)  # cap at 1 as old script did

print(f"    alpha_s(v) [wrong sign, capped] = {alpha_wrong:.6f}")
print(f"    This is what frontier_ckm_nonperturbative.py computed.")
print(f"    With the correct sign: alpha_s(v) = {alpha_v_staircase:.6f}")
print(f"    Ratio wrong/correct = {alpha_wrong/alpha_v_staircase:.1f}x")


# ======================================================================
# PART 7: HONEST ASSESSMENT
# ======================================================================
print("\n" + "=" * 78)
print("PART 7: HONEST ASSESSMENT")
print("=" * 78)

print(f"""
  SUMMARY:

  1. SIGN CONVENTION FIX: The 1-loop running formula in
     frontier_ckm_nonperturbative.py had the wrong sign:
       WRONG:   1/alpha(lo) = 1/alpha(hi) + b_0/(2pi) * ln(hi/lo)
       CORRECT: 1/alpha(lo) = 1/alpha(hi) - b_0/(2pi) * ln(hi/lo)
     This is verified by exact ODE integration.

  2. CONSEQUENCE: In the non-AF regime (b_0 < 0), the coupling
     DECREASES from M_Pl toward lower scales. The taste staircase
     does NOT amplify the coupling -- it weakens it.

  3. CORRECT V_cb FROM STAIRCASE:
     alpha_s(v)   = {alpha_v_staircase:.6f}
     alpha_eff(RG) = {alpha_eff:.6f}
     V_cb(staircase) = {vcb_staircase:.5f}
     V_cb(at v)      = {vcb_at_v:.5f}
     V_cb(pert)      = {vcb_pert:.5f}
     V_cb(PDG)       = {V_CB_PDG}

  4. THE GAP IS LARGER THAN PREVIOUSLY THOUGHT:
     The previous bracket [0.015, 0.060] was based on the wrong sign.
     The correct staircase gives V_cb even further from PDG.
     The gap factor is now {alpha_needed/alpha_v_staircase:.0f}x (was claimed to be 2.8x).

  5. V_us REMAINS CORRECTLY PREDICTED:
     |V_us| = {vus_gst:.4f} vs PDG {V_US_PDG} ({(vus_gst/V_US_PDG - 1)*100:+.2f}%)
     This structural prediction is independent of the coupling.

  6. THE REMAINING PATH TO V_cb:
     The gap cannot be closed by the staircase RG mechanism. The NNI
     coefficient c_23 must receive its dominant contribution from a
     non-perturbative mechanism (confinement, instantons, or strong-
     coupling taste-breaking) that operates at the low scale where
     alpha_s is large. The perturbative 1-gluon-exchange picture
     with the M_Pl coupling is insufficient.
""")

honest("staircase_does_not_help",
       f"correct 2-loop staircase gives alpha_s(v) = {alpha_v_staircase:.4f} < "
       f"alpha_V(M_Pl) = {ALPHA_V_MPL:.4f}")

honest("vcb_gap_widened",
       f"V_cb = {vcb_staircase:.5f} vs PDG {V_CB_PDG}, "
       f"gap factor = {alpha_needed/alpha_eff:.1f}x")

honest("sign_error_in_old_scripts",
       "frontier_ckm_nonperturbative.py 1-loop formula has wrong sign; "
       "its V_cb bracket [0.015, 0.060] is invalidated")

# Final checks
check("2loop_staircase_well_defined",
      0 < alpha_v_staircase < 1,
      f"alpha_s(v) = {alpha_v_staircase:.6f}",
      kind="EXACT")

check("vus_structural_prediction",
      abs(vus_gst / V_US_PDG - 1) < 0.005,
      f"|V_us| = {vus_gst:.4f} ({(vus_gst/V_US_PDG - 1)*100:+.2f}%)",
      kind="BOUNDED")

check("vcb_gap_is_real",
      vcb_staircase < V_CB_PDG * 0.5,
      f"V_cb = {vcb_staircase:.5f} is {(1 - vcb_staircase/V_CB_PDG)*100:.0f}% below PDG: "
      f"gap requires non-perturbative mechanism",
      kind="BOUNDED")


# ======================================================================
# SCOREBOARD
# ======================================================================
print("\n" + "=" * 78)
elapsed = time.time() - t0
total = PASS_COUNT + FAIL_COUNT
print(f"SCOREBOARD: {PASS_COUNT}/{total} PASS  "
      f"({EXACT_PASS} exact + {BOUNDED_PASS} bounded, "
      f"{FAIL_COUNT} FAIL, {HONEST_COUNT} HONEST)")
print(f"Time: {elapsed:.1f}s")
print("=" * 78)

if FAIL_COUNT > 0:
    print(f"\n  WARNING: {FAIL_COUNT} checks FAILED")
    sys.exit(1)
else:
    print(f"\n  All {PASS_COUNT} checks passed.")
    sys.exit(0)
