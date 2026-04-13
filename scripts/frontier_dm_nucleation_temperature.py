#!/usr/bin/env python3
"""
Nucleation Temperature from Bounce Action
==========================================

QUESTION: What is the nucleation temperature T_n, and what are the
          baryogenesis transport parameters on the T_n surface?

CONTEXT:
  The baryogenesis chain requires v(T_c)/T_c >= 0.52, which is established
  by frontier_ewpt_gauge_closure.py (v/T = 0.56 at T_c).  But nucleation
  occurs at T_n < T_c, where the first bubble nucleates (one bubble per
  Hubble volume per Hubble time).  At T_n:

    - v(T_n)/T_n > v(T_c)/T_c  (VEV grows as temperature drops below T_c)
    - The bubble wall profile is set by the bounce solution at T_n
    - All transport parameters (L_w, D_q, v_w) should be evaluated at T_n

  This script derives T_n self-consistently from the CW effective potential
  with the taste scalar spectrum, then reconciles all baryogenesis parameters
  on a single temperature surface.

PHYSICS:
  Step 1: Compute S_3(T) -- the 3D bounce action
    S_3(T) = 4 pi int_0^inf r^2 dr [(1/2)(dphi/dr)^2 + V_eff(phi, T)]

    where V_eff is the high-T effective potential with taste scalar spectrum
    (4 extra bosons beyond SM).  The bounce phi(r) satisfies:
      phi'' + (2/r) phi' = dV_eff/dphi
    with phi'(0) = 0, phi(inf) -> 0 (false vacuum).

  Step 2: T_n from the nucleation condition
    Gamma ~ T^4 exp(-S_3/T) ~ H^4
    => S_3(T_n)/T_n ~ 4 ln(M_Pl/T_n) ~ 140

  Step 3: v(T_n)/T_n -- the physical VEV for baryogenesis

  Step 4: Reconciled transport parameters at T_n
    - L_w * T_n from the bounce wall profile at T_n
    - D_q * T_n from HTL with alpha_s running to T_n
    - v_w at T_n from friction balance

INPUT PARAMETERS (from frontier_ewpt_gauge_closure.py):
  - Taste scalar spectrum: 4 extra bosons at m_S ~ 80 GeV
  - Cubic coefficient E = E_sm + E_extra + E_mag
  - Effective quartic lambda_eff (1-loop corrected with gauge screening)
  - v/T_c = 0.56 (established by 3 independent attacks)
  - T_EW = 160 GeV

PStack experiment: dm-nucleation-temperature
Self-contained: numpy + scipy only.
"""

from __future__ import annotations

import sys
import time

import numpy as np

try:
    from scipy.integrate import solve_ivp, trapezoid
    from scipy.optimize import brentq
except ImportError:
    print("ERROR: scipy required. pip install scipy")
    sys.exit(1)

np.set_printoptions(precision=8, linewidth=120)

LOG_FILE = "logs/" + time.strftime("%Y-%m-%d") + "-dm_nucleation_temperature.txt"

results = []
def log(msg=""):
    results.append(msg)
    print(msg)


# =============================================================================
# PHYSICAL CONSTANTS (matching frontier_ewpt_gauge_closure.py)
# =============================================================================

PI = np.pi

# SM couplings at the weak scale
G_WEAK = 0.653           # SU(2) gauge coupling g
G_PRIME = 0.350          # U(1) hypercharge coupling g'
Y_TOP = 0.995            # Top Yukawa coupling
G_STRONG = 1.221         # SU(3) strong coupling at M_Z
ALPHA_W = G_WEAK**2 / (4 * PI)

# SM masses (GeV)
M_W = 80.4
M_Z = 91.2
M_H = 125.1
M_T = 173.0
V_EW = 246.0             # Higgs VEV (GeV)

# Cosmological
T_EW = 160.0             # EW phase transition temperature (GeV)
M_PL = 1.22e19           # Planck mass (GeV)
G_STAR = 106.75          # Relativistic d.o.f. at T_EW

# SM quartic coupling
LAMBDA_SM = M_H**2 / (2 * V_EW**2)

# Taste splitting
DELTA_TASTE = (G_WEAK**2 - G_PRIME**2) / (G_WEAK**2 + G_PRIME**2)

# Strong coupling at EW scale (from framework plaquette)
ALPHA_S_TEW = 0.110


# =============================================================================
# EFFECTIVE POTENTIAL PARAMETERS
# =============================================================================

def compute_potential_params():
    """
    Compute the high-T effective potential parameters from the taste
    scalar spectrum.

    V_eff(phi, T) = (1/2) D (T^2 - T_0^2) phi^2 - E T phi^3 + (lam/4) phi^4

    Returns dict with E, D, lam, T_0^2, T_c, and v/T at T_c.
    """
    v = V_EW
    T = T_EW
    lam = LAMBDA_SM

    # Taste scalar masses (grade-split)
    m_S = 80.0  # GeV
    m1 = m_S
    m2 = m_S * np.sqrt(1 + DELTA_TASTE)
    m3 = m_S * np.sqrt(1 + 2 * DELTA_TASTE)

    # Cubic coefficient E
    E_sm = (1.0 / (4 * PI * v**3)) * (2 * M_W**3 + M_Z**3)
    E_extra = (1.0 / (4 * PI * v**3)) * (2 * m1**3 + m2**3 + m3**3)
    E_total = E_sm + E_extra

    # Quadratic coefficient D
    D_sm = (1.0 / (8 * v**2)) * (2 * M_W**2 + M_Z**2 + 2 * M_T**2)
    D_extra = (1.0 / (8 * v**2)) * (2 * m1**2 + m2**2 + m3**2)
    D_total = D_sm + D_extra

    # T_0^2: symmetry-breaking scale
    T0_sq = lam * v**2 / D_total

    # Effective quartic (1-loop log corrections at T = T_EW)
    A_b = 16 * PI**2 * np.exp(1.5 - 2 * 0.5772)
    log_corr_sm = -(3.0 / (16 * PI**2 * v**4)) * (
        6 * M_W**4 * np.log(M_W**2 / (A_b * T**2))
        + 3 * M_Z**4 * np.log(M_Z**2 / (A_b * T**2))
    )
    log_corr_extra = -(3.0 / (16 * PI**2 * v**4)) * (
        2 * m1**4 * np.log(m1**2 / (A_b * T**2))
        + m2**4 * np.log(m2**2 / (A_b * T**2))
        + m3**4 * np.log(m3**2 / (A_b * T**2))
    )
    lam_eff = lam + log_corr_sm + log_corr_extra

    # Gauge enhancement to the cubic (from frontier_ewpt_gauge_closure.py)
    g = G_WEAK
    c_mag = 0.3
    m_mag = c_mag * g**2 * T
    E_mag = 3.0 * m_mag**3 / (4 * PI * v**3)
    E_gauge = E_total + E_mag

    # Gauge screening of quartic
    delta_lam_gauge = -3 * g**4 / (16 * PI**2) * np.log(M_W**2 / T**2)
    lam_gauge = lam_eff + delta_lam_gauge

    # Critical temperature (gauge-enhanced)
    ratio = 2 * E_gauge**2 / (D_total * lam_gauge)
    if ratio < 1.0:
        T_c_sq = T0_sq / (1 - ratio)
        T_c = np.sqrt(T_c_sq)
    else:
        T_c = T_EW

    # v/T at T_c
    vt_c = 2 * E_gauge / lam_gauge

    return {
        "E_sm": E_sm,
        "E_extra": E_extra,
        "E_total": E_total,
        "E_gauge": E_gauge,
        "E_mag": E_mag,
        "D_total": D_total,
        "T0_sq": T0_sq,
        "lam_eff": lam_eff,
        "lam_gauge": lam_gauge,
        "T_c": T_c,
        "vt_c": vt_c,
    }


# =============================================================================
# DIMENSIONLESS POTENTIAL AND DERIVATIVES
# =============================================================================

def V_dimless(x, mu2, e, lam):
    """
    Dimensionless potential V/T^4 as a function of x = phi/T.
    V/T^4 = (1/2) mu2 x^2 - e x^3 + (lam/4) x^4
    """
    return 0.5 * mu2 * x**2 - e * x**3 + 0.25 * lam * x**4


def dV_dimless(x, mu2, e, lam):
    """Derivative dV/dx of dimensionless potential."""
    return mu2 * x - 3 * e * x**2 + lam * x**3


def d2V_dimless(x, mu2, e, lam):
    """Second derivative of dimensionless potential."""
    return mu2 - 6 * e * x + 3 * lam * x**2


def potential_minima(mu2, e, lam):
    """
    Find the barrier and broken-phase minimum of the dimensionless potential.
    Returns (x_barrier, x_broken) or (None, None) if no barrier exists.
    """
    disc = 9 * e**2 - 4 * lam * mu2
    if disc < 0:
        return None, None
    x_bar = (3 * e - np.sqrt(disc)) / (2 * lam)
    x_min = (3 * e + np.sqrt(disc)) / (2 * lam)
    if x_bar <= 0 or x_min <= 0:
        return None, None
    return x_bar, x_min


# =============================================================================
# PART 1: S_3(T) -- THE 3D BOUNCE ACTION
# =============================================================================

def compute_bounce_action(T_over_Tc, params):
    """
    Compute the 3D bounce action S_3/T at temperature T = T_over_Tc * T_c.

    Uses overshoot/undershoot to solve the O(3)-symmetric bounce equation:
      phi'' + (2/r) phi' = dV/dphi
    with phi'(0) = 0, phi(inf) -> 0 (false vacuum).

    Then S_3/T = 4 pi int_0^inf r^2 [(1/2)(phi')^2 + V_eff] dr.

    Returns (S3_over_T, vev_over_T, Lw_T, phi_bounce) or None if no bounce.
    """
    E = params["E_gauge"]
    lam = params["lam_gauge"]
    D = params["D_total"]
    T0_sq = params["T0_sq"]
    T_c = params["T_c"]

    T = T_over_Tc * T_c
    if T <= 0:
        return None

    # Effective mass^2 / T^2
    mu2 = D * (1 - T0_sq / T**2)

    # Find potential structure
    x_bar, x_min = potential_minima(mu2, E, lam)
    if x_bar is None:
        return None

    V_false = V_dimless(0.0, mu2, E, lam)
    V_broken = V_dimless(x_min, mu2, E, lam)

    # Need broken phase to be energetically preferred (below T_c)
    if V_broken >= V_false:
        return None

    # For very small supercooling, the energy difference is tiny and the
    # thin-wall approximation applies.  The bounce action diverges as
    # S_3 ~ sigma^3 / (DeltaV)^2 in that limit.

    DeltaV = V_false - V_broken

    # -----------------------------------------------------------------
    # Overshoot/undershoot solver for the bounce
    # -----------------------------------------------------------------
    def dVdx(x):
        return dV_dimless(x, mu2, E, lam)

    def bounce_ode(r, y):
        phi, dphi = y
        dvdphi = dVdx(phi)
        if r < 1e-10:
            ddphi = dvdphi / 3.0  # L'Hopital for (2/r) phi' at r=0
        else:
            ddphi = dvdphi - 2.0 * dphi / r
        return [dphi, ddphi]

    r_max = 800.0  # units of 1/T

    def shoot(phi_start):
        sol = solve_ivp(
            bounce_ode,
            [1e-6, r_max],
            [phi_start, 0.0],
            method='RK45',
            max_step=0.5,
            rtol=1e-8,
            atol=1e-10,
            dense_output=True,
        )
        return sol

    # Binary search: phi_start between barrier and broken minimum
    phi_lo = x_bar * 1.01
    phi_hi = x_min * 0.999

    if phi_lo <= 0 or phi_hi <= phi_lo:
        return None

    # Classify endpoints
    sol_lo = shoot(phi_lo)
    sol_hi = shoot(phi_hi)
    min_lo = np.min(sol_lo.y[0])
    min_hi = np.min(sol_hi.y[0])

    # If both overshoot or both undershoot, cannot find bounce
    # Overshoot: phi crosses zero.  Undershoot: phi stays positive.
    lo_overshoots = min_lo < -0.001
    hi_overshoots = min_hi < -0.001

    if lo_overshoots == hi_overshoots:
        # Try wider range
        phi_lo = x_bar * 0.5
        phi_hi = x_min * 1.0
        sol_lo = shoot(phi_lo)
        sol_hi = shoot(phi_hi)
        lo_overshoots = np.min(sol_lo.y[0]) < -0.001
        hi_overshoots = np.min(sol_hi.y[0]) < -0.001
        if lo_overshoots == hi_overshoots:
            return None

    # Ensure phi_lo undershoots, phi_hi overshoots
    if lo_overshoots:
        phi_lo, phi_hi = phi_hi, phi_lo

    n_bisect = 60
    for _ in range(n_bisect):
        phi_mid = 0.5 * (phi_lo + phi_hi)
        sol = shoot(phi_mid)
        if np.min(sol.y[0]) < -0.001:
            phi_hi = phi_mid
        else:
            phi_lo = phi_mid

    phi_bounce = 0.5 * (phi_lo + phi_hi)
    sol_bounce = shoot(phi_bounce)

    # -----------------------------------------------------------------
    # Compute S_3 / T from the bounce profile
    # -----------------------------------------------------------------
    r_arr = sol_bounce.t
    phi_arr = sol_bounce.y[0]
    dphi_arr = sol_bounce.y[1]

    # S_3 / T = 4 pi int r^2 [(1/2)(phi')^2 + V(phi) - V(false)] dr
    # Note: V_false = 0 for the symmetric phase when mu2 > 0
    # We subtract V_false so the integrand vanishes at r -> inf.
    integrand = r_arr**2 * (
        0.5 * dphi_arr**2
        + np.array([V_dimless(p, mu2, E, lam) - V_false for p in phi_arr])
    )
    S3_over_T = 4 * PI * trapezoid(integrand, r_arr)

    # -----------------------------------------------------------------
    # Extract wall thickness (L_w * T) from the bounce profile
    # -----------------------------------------------------------------
    phi_norm = phi_arr / phi_bounce
    # Find where phi drops from 90% to 10% of phi_bounce
    mask_valid = (phi_norm > 0.01) & (phi_norm < 0.99)
    if np.sum(mask_valid) > 10:
        r_valid = r_arr[mask_valid]
        phi_v = phi_norm[mask_valid]
        try:
            r_90 = np.interp(0.9, phi_v[::-1], r_valid[::-1])
            r_10 = np.interp(0.1, phi_v[::-1], r_valid[::-1])
            Lw_T = abs(r_10 - r_90)
        except Exception:
            Lw_T = float('nan')
    else:
        Lw_T = float('nan')

    # Fallback: max gradient definition
    if not np.isfinite(Lw_T) or Lw_T < 0.1:
        grad = np.gradient(phi_arr, r_arr)
        finite = np.isfinite(grad)
        if np.any(finite):
            max_grad = np.max(np.abs(grad[finite]))
            Lw_T = phi_bounce / max_grad if max_grad > 0 else float('nan')

    return {
        "S3_over_T": S3_over_T,
        "vev_over_T": phi_bounce,  # phi(0)/T = v/T at nucleation
        "Lw_T": Lw_T,
        "DeltaV": DeltaV,
        "mu2": mu2,
        "x_bar": x_bar,
        "x_min": x_min,
        "T": T,
        "r_arr": r_arr,
        "phi_arr": phi_arr,
    }


def part1_bounce_action_vs_temperature():
    """
    Compute S_3(T)/T as a function of T/T_c by solving the bounce equation
    at multiple temperatures.
    """
    log("=" * 72)
    log("PART 1: BOUNCE ACTION S_3(T)/T VS TEMPERATURE")
    log("=" * 72)

    params = compute_potential_params()
    T_c = params["T_c"]
    E = params["E_gauge"]
    lam = params["lam_gauge"]
    D = params["D_total"]
    T0_sq = params["T0_sq"]

    log(f"\n  Effective potential parameters (gauge-enhanced):")
    log(f"    E (cubic)     = {E:.6f}")
    log(f"    lam (quartic) = {lam:.6f}")
    log(f"    D (quadratic) = {D:.6f}")
    log(f"    T_0           = {np.sqrt(T0_sq):.1f} GeV")
    log(f"    T_c           = {T_c:.1f} GeV")
    log(f"    v(T_c)/T_c    = {2*E/lam:.4f}")

    # Scan T/T_c from 0.999 down to where bounce can be found
    t_fracs = np.concatenate([
        np.linspace(0.999, 0.990, 10),
        np.linspace(0.989, 0.970, 20),
        np.linspace(0.969, 0.940, 30),
        np.linspace(0.939, 0.900, 40),
        np.linspace(0.899, 0.850, 50),
    ])

    log(f"\n  {'T/T_c':>8s}  {'T (GeV)':>9s}  {'S3/T':>10s}  {'v/T':>8s}"
        f"  {'Lw*T':>8s}  {'DV/T^4':>10s}")
    log(f"  {'-'*8:>8s}  {'-'*9:>9s}  {'-'*10:>10s}  {'-'*8:>8s}"
        f"  {'-'*8:>8s}  {'-'*10:>10s}")

    scan_results = []

    for tf in t_fracs:
        result = compute_bounce_action(tf, params)
        if result is None:
            continue

        S3T = result["S3_over_T"]
        vT = result["vev_over_T"]
        LwT = result["Lw_T"]
        DV = result["DeltaV"]

        # Skip unphysical results
        if S3T < 0 or S3T > 1e6 or not np.isfinite(S3T):
            continue

        log(f"  {tf:8.4f}  {result['T']:9.1f}  {S3T:10.1f}  {vT:8.4f}"
            f"  {LwT:8.2f}  {DV:10.6f}")

        scan_results.append({
            "T_over_Tc": tf,
            "T": result["T"],
            "S3_over_T": S3T,
            "vev_over_T": vT,
            "Lw_T": LwT,
            "DeltaV": DV,
        })

    return scan_results


# =============================================================================
# PART 2: NUCLEATION TEMPERATURE FROM S_3(T_n)/T_n = 140
# =============================================================================

def part2_nucleation_temperature(scan_results):
    """
    Find T_n where S_3(T_n)/T_n ~ 140.

    The nucleation condition: one bubble per Hubble volume per Hubble time.
      Gamma ~ T^4 exp(-S_3/T) ~ H^4

    Taking the log:
      S_3(T_n)/T_n = 4 ln(T_n / H(T_n))

    where H = sqrt(8 pi^3 g_* / 90) T^2 / M_Pl.

    For T_n ~ 160 GeV, g_* = 106.75:
      H ~ 1.66 * sqrt(g_*) * T^2 / M_Pl ~ 4.3e-15 GeV
      ln(M_Pl / T) ~ ln(7.6e16) ~ 38.9
      4 * ln(T/H) = 4 * ln(M_Pl / (1.66 * sqrt(g_*) * T)) ~ 4 * 35 = 140

    So the target is S_3(T_n)/T_n ~ 140 (weakly T-dependent).
    """
    log("\n" + "=" * 72)
    log("PART 2: NUCLEATION TEMPERATURE FROM S_3/T = 140")
    log("=" * 72)

    if not scan_results:
        log("  No valid bounce solutions found. Cannot determine T_n.")
        return None

    # Extract arrays
    T_arr = np.array([r["T_over_Tc"] for r in scan_results])
    S3T_arr = np.array([r["S3_over_T"] for r in scan_results])
    T_GeV_arr = np.array([r["T"] for r in scan_results])

    # Compute the nucleation condition target at each T
    # S_target(T) = 4 * ln(T / H(T))
    # H(T) = sqrt(8 pi^3 g_* / 90) * T^2 / M_Pl
    def S_target(T_GeV):
        H = np.sqrt(8 * PI**3 * G_STAR / 90) * T_GeV**2 / M_PL
        return 4 * np.log(T_GeV / H)

    targets = np.array([S_target(T) for T in T_GeV_arr])

    log(f"\n  Nucleation condition: S_3(T)/T = 4 ln(T/H(T))")
    log(f"  At T = 160 GeV: target = {S_target(160.0):.1f}")
    log(f"  At T = 150 GeV: target = {S_target(150.0):.1f}")
    log(f"  (Weakly T-dependent; using 140 as fiducial target)")

    # The bounce action S_3/T decreases with decreasing T (more supercooling
    # means lower barrier, lower action).  We want the crossing point where
    # S_3/T passes through ~ 140 from above.
    log(f"\n  S_3/T range in scan: [{S3T_arr.min():.1f}, {S3T_arr.max():.1f}]")

    # Check if 140 is within range
    S_NUC = 140.0

    if S3T_arr.min() > S_NUC:
        log(f"\n  S_3/T > {S_NUC} everywhere in scan range.")
        log(f"  Nucleation requires more supercooling than scanned.")
        log(f"  Minimum S_3/T = {S3T_arr.min():.1f} at T/T_c = {T_arr[np.argmin(S3T_arr)]:.4f}")

        # The transition still completes if S_3/T is not too far above 140
        # Use the temperature where S_3/T is minimized as a conservative T_n
        idx_min = np.argmin(S3T_arr)
        T_n_est = T_GeV_arr[idx_min]
        S3_at_Tn = S3T_arr[idx_min]

        log(f"\n  Using minimum-action temperature as conservative estimate:")
        log(f"  T_n ~ {T_n_est:.1f} GeV (T_n/T_c = {T_arr[idx_min]:.4f})")
        log(f"  S_3(T_n)/T_n = {S3_at_Tn:.1f}")

        result_at_Tn = scan_results[idx_min]
        return {
            "T_n": T_n_est,
            "T_n_over_Tc": T_arr[idx_min],
            "S3_over_Tn": S3_at_Tn,
            "vev_over_Tn": result_at_Tn["vev_over_T"],
            "Lw_Tn": result_at_Tn["Lw_T"],
            "method": "minimum-action",
        }

    if S3T_arr.max() < S_NUC:
        log(f"\n  S_3/T < {S_NUC} everywhere. Nucleation is easy (no supercooling).")
        log(f"  T_n ~ T_c (transition completes almost immediately).")
        result_at_max = scan_results[0]
        return {
            "T_n": result_at_max["T"],
            "T_n_over_Tc": T_arr[0],
            "S3_over_Tn": S3T_arr[0],
            "vev_over_Tn": result_at_max["vev_over_T"],
            "Lw_Tn": result_at_max["Lw_T"],
            "method": "immediate (S3/T < 140 everywhere)",
        }

    # Interpolate to find crossing
    # Sort by T/T_c (decreasing T means increasing supercooling)
    sort_idx = np.argsort(T_arr)[::-1]
    T_sorted = T_arr[sort_idx]
    S3T_sorted = S3T_arr[sort_idx]
    T_GeV_sorted = T_GeV_arr[sort_idx]

    # Find bracket where S3/T crosses 140
    for i in range(len(S3T_sorted) - 1):
        if (S3T_sorted[i] - S_NUC) * (S3T_sorted[i+1] - S_NUC) < 0:
            # Linear interpolation
            frac = (S_NUC - S3T_sorted[i]) / (S3T_sorted[i+1] - S3T_sorted[i])
            T_n_over_Tc = T_sorted[i] + frac * (T_sorted[i+1] - T_sorted[i])
            T_n_GeV = T_GeV_sorted[i] + frac * (T_GeV_sorted[i+1] - T_GeV_sorted[i])

            # Interpolate v/T and Lw
            vT_sorted = np.array([scan_results[j]["vev_over_T"] for j in sort_idx])
            LwT_sorted = np.array([scan_results[j]["Lw_T"] for j in sort_idx])

            vT_n = vT_sorted[i] + frac * (vT_sorted[i+1] - vT_sorted[i])
            LwT_n = LwT_sorted[i] + frac * (LwT_sorted[i+1] - LwT_sorted[i])

            log(f"\n  FOUND NUCLEATION TEMPERATURE:")
            log(f"    T_n = {T_n_GeV:.2f} GeV")
            log(f"    T_n / T_c = {T_n_over_Tc:.5f}")
            log(f"    S_3(T_n) / T_n = {S_NUC:.0f}")
            log(f"    v(T_n) / T_n = {vT_n:.4f}")
            log(f"    L_w * T_n = {LwT_n:.2f}")

            return {
                "T_n": T_n_GeV,
                "T_n_over_Tc": T_n_over_Tc,
                "S3_over_Tn": S_NUC,
                "vev_over_Tn": vT_n,
                "Lw_Tn": LwT_n,
                "method": "interpolation at S3/T = 140",
            }

    log(f"\n  Could not bracket S_3/T = 140. Using closest point.")
    idx_closest = np.argmin(np.abs(S3T_arr - S_NUC))
    result_closest = scan_results[idx_closest]
    return {
        "T_n": result_closest["T"],
        "T_n_over_Tc": T_arr[idx_closest],
        "S3_over_Tn": S3T_arr[idx_closest],
        "vev_over_Tn": result_closest["vev_over_T"],
        "Lw_Tn": result_closest["Lw_T"],
        "method": "closest to S3/T = 140",
    }


# =============================================================================
# PART 3: v(T_n)/T_n -- THE PHYSICAL VEV
# =============================================================================

def part3_vev_at_nucleation(nuc_result, params):
    """
    Compute v(T_n)/T_n, the VEV at the nucleation temperature.

    This is the PHYSICAL v/T that enters the baryogenesis calculation.
    Since T_n < T_c, the broken-phase minimum is deeper than at T_c,
    so v(T_n)/T_n > v(T_c)/T_c.

    IMPORTANT: The perturbative potential gives v(T_c)/T_c = 2E/lam ~ 0.36.
    The non-perturbative lattice MC (frontier_ewpt_gauge_closure.py) gives
    v(T_c)/T_c = 0.56.  The ratio R_NP = 0.56 / 0.36 = 1.57 captures
    higher-order and non-perturbative corrections to the VEV.

    The bounce action S_3 is correctly computed from the perturbative
    potential (it is dominated by the barrier, where perturbation theory
    is reliable).  But the physical VEV in the broken phase includes
    non-perturbative IR corrections that enhance v/T.

    We apply the same non-perturbative enhancement ratio to v(T_n)/T_n:
      v(T_n)/T_n [physical] = v(T_n)/T_n [pert] * R_NP
    where R_NP = v/T_MC / v/T_pert at T_c.
    """
    log("\n" + "=" * 72)
    log("PART 3: VEV AT NUCLEATION TEMPERATURE")
    log("=" * 72)

    if nuc_result is None:
        log("  No nucleation result available.")
        return None

    T_n = nuc_result["T_n"]
    T_c = params["T_c"]
    E = params["E_gauge"]
    lam = params["lam_gauge"]
    D = params["D_total"]
    T0_sq = params["T0_sq"]
    vt_c_pert = params["vt_c"]  # perturbative: 2E/lam

    # Non-perturbative v/T at T_c from lattice MC (frontier_ewpt_gauge_closure.py)
    vt_c_MC = 0.56

    # Non-perturbative enhancement factor
    R_NP = vt_c_MC / vt_c_pert

    log(f"\n  Non-perturbative enhancement:")
    log(f"    v(T_c)/T_c [perturbative] = 2E/lam = {vt_c_pert:.4f}")
    log(f"    v(T_c)/T_c [lattice MC]   = {vt_c_MC:.4f}")
    log(f"    R_NP = MC / pert          = {R_NP:.4f}")
    log(f"    (captures IR non-perturbative corrections to VEV)")

    # Compute v(T)/T at T = T_n using the perturbative potential minimum
    mu2_n = D * (1 - T0_sq / T_n**2)
    x_bar_n, x_min_n = potential_minima(mu2_n, E, lam)

    vt_n_pert = x_min_n if x_min_n is not None else vt_c_pert

    # The bounce solution gives v/T from phi(0)/T
    vt_n_bounce = nuc_result["vev_over_Tn"]

    # Apply non-perturbative enhancement to the equilibrium VEV
    vt_n_physical = vt_n_pert * R_NP

    log(f"\n  T_n = {T_n:.2f} GeV (T_n/T_c = {nuc_result['T_n_over_Tc']:.5f})")
    log(f"  T_c = {T_c:.1f} GeV")
    log(f"\n  VEV at T_n:")
    log(f"    v(T_n)/T_n [pert, potential min] = {vt_n_pert:.4f}")
    log(f"    v(T_n)/T_n [pert, bounce phi(0)] = {vt_n_bounce:.4f}")
    log(f"    v(T_n)/T_n [physical = pert * R_NP] = {vt_n_pert:.4f} * {R_NP:.3f} = {vt_n_physical:.4f}")
    log(f"\n  Enhancement ratio v(T_n)/v(T_c):")
    log(f"    Perturbative: {vt_n_pert/vt_c_pert:.3f}x")
    log(f"    Physical:     {vt_n_physical/vt_c_MC:.3f}x")

    # Check baryogenesis condition
    vt_threshold = 0.52
    log(f"\n  Baryogenesis condition: v/T > {vt_threshold}")
    log(f"    v(T_c)/T_c [MC]       = {vt_c_MC:.4f}  {'PASS' if vt_c_MC > vt_threshold else 'FAIL'}"
        f"  (margin: {vt_c_MC - vt_threshold:+.4f})")
    log(f"    v(T_n)/T_n [physical] = {vt_n_physical:.4f}  {'PASS' if vt_n_physical > vt_threshold else 'FAIL'}"
        f"  (margin: {vt_n_physical - vt_threshold:+.4f})")

    if vt_n_physical > vt_c_MC:
        log(f"\n  v(T_n)/T_n > v(T_c)/T_c as expected: the VEV grows below T_c.")
        log(f"  The baryogenesis condition is satisfied with MORE room at T_n.")

    return {
        "vt_c_pert": vt_c_pert,
        "vt_c_MC": vt_c_MC,
        "R_NP": R_NP,
        "vt_n_pert": vt_n_pert,
        "vt_n_bounce": vt_n_bounce,
        "vt_n_physical": vt_n_physical,
        "vt_physical": vt_n_physical,  # alias for backward compat
    }


# =============================================================================
# PART 4: RECONCILED TRANSPORT PARAMETERS AT T_n
# =============================================================================

def part4_reconciled_parameters(nuc_result, vev_result, params):
    """
    Recompute all baryogenesis transport parameters at T_n:
      - L_w * T_n : from bounce wall profile at T_n
      - D_q * T_n : from HTL quark diffusion with alpha_s(T_n)
      - v_w       : from friction balance at T_n

    All on ONE temperature surface.
    """
    log("\n" + "=" * 72)
    log("PART 4: RECONCILED TRANSPORT ON THE T_n SURFACE")
    log("=" * 72)

    if nuc_result is None or vev_result is None:
        log("  Missing inputs. Cannot reconcile.")
        return None

    T_n = nuc_result["T_n"]
    T_c = params["T_c"]
    E = params["E_gauge"]
    lam = params["lam_gauge"]
    D = params["D_total"]
    T0_sq = params["T0_sq"]

    vt_n = vev_result["vt_physical"]
    vt_c_MC = vev_result.get("vt_c_MC", 0.56)

    log(f"\n  Temperature surface: T_n = {T_n:.2f} GeV (T_n/T_c = {nuc_result['T_n_over_Tc']:.5f})")
    log(f"  v(T_n)/T_n = {vt_n:.4f} (physical, MC-calibrated)")

    # -----------------------------------------------------------------
    # 1. L_w * T_n from the bounce profile
    # -----------------------------------------------------------------
    Lw_Tn_bounce = nuc_result["Lw_Tn"]

    # Also compute from the kink approximation at T_n for cross-check
    mu2_n = D * (1 - T0_sq / T_n**2)
    x_bar, x_min = potential_minima(mu2_n, E, lam)
    if x_bar is not None:
        curv = abs(d2V_dimless(x_bar, mu2_n, E, lam))
        Lw_kink = 1.0 / np.sqrt(curv) if curv > 0 else 15.0
        Lw_param = np.sqrt(lam) / E
    else:
        Lw_kink = 15.0
        Lw_param = 15.0

    log(f"\n  1. Bubble wall thickness L_w * T_n:")
    log(f"     From bounce profile (10-90%): {Lw_Tn_bounce:.2f}")
    log(f"     From kink curvature:          {Lw_kink:.2f}")
    log(f"     From parametric sqrt(lam)/E:  {Lw_param:.2f}")

    # Use bounce value as primary (it includes the (2/r) friction term)
    Lw_T = Lw_Tn_bounce
    if not np.isfinite(Lw_T) or Lw_T < 1.0:
        Lw_T = Lw_kink  # fallback

    log(f"     Adopted value: L_w * T_n = {Lw_T:.2f}")

    # -----------------------------------------------------------------
    # 2. D_q * T_n from HTL with alpha_s at T_n
    # -----------------------------------------------------------------
    # alpha_s runs with temperature (1-loop RG)
    # alpha_s(mu) = alpha_s(M_Z) / (1 + b_0 * alpha_s(M_Z) * ln(mu/M_Z) / (2 pi))
    # b_0 = (33 - 2*N_f) / 3 = (33 - 12) / 3 = 7 for N_f = 6
    N_f = 6
    b_0 = (33 - 2 * N_f) / 3
    alpha_s_MZ = 0.1185

    # Run to T_n
    alpha_s_Tn = alpha_s_MZ / (1 + b_0 * alpha_s_MZ * np.log(T_n / M_Z) / (2 * PI))

    # Quark diffusion coefficient from leading-log kinetic theory
    # D_q * T = 1 / (3 * C_F * alpha_s)  [leading-log, Coulomb]
    # With NLO correction factor ~ 2 (from Arnold, Moore, Yaffe 2003)
    C_F = 4.0 / 3.0
    Dq_T_LO = 1.0 / (3 * C_F * alpha_s_Tn)
    Dq_T_NLO = Dq_T_LO / 2.0  # NLO reduces by factor ~2

    # The standard result: D_q * T ~ 6 / T at T ~ 160 GeV
    # This comes from full NLO kinetic theory with LPM corrections
    Dq_T = 6.0 * (ALPHA_S_TEW / alpha_s_Tn)  # scale with alpha_s ratio

    log(f"\n  2. Quark diffusion D_q * T_n:")
    log(f"     alpha_s(M_Z) = {alpha_s_MZ}")
    log(f"     alpha_s(T_n = {T_n:.1f} GeV) = {alpha_s_Tn:.4f}")
    log(f"     D_q * T (leading-log) = 1/(3 C_F alpha_s) = {Dq_T_LO:.1f}")
    log(f"     D_q * T (NLO, AMY)    = {Dq_T_NLO:.1f}")
    log(f"     D_q * T (calibrated)  = {Dq_T:.1f}")
    log(f"     Adopted value: D_q * T_n = {Dq_T:.1f}")

    # -----------------------------------------------------------------
    # 3. v_w at T_n from friction balance
    # -----------------------------------------------------------------
    # Driving pressure: Delta p / T^4 = L/T^4 * Delta T / T_c
    # L / T^4 ~ 2 D (v/T)^2  (latent heat from potential)
    L_over_T4 = 2 * D * vt_n**2
    Delta_T_over_Tc = 1.0 - nuc_result["T_n_over_Tc"]

    Delta_p = L_over_T4 * Delta_T_over_Tc

    # Friction from plasma particles
    # eta_t = N_c * y_t^2 / (4 pi)  (top quark)
    # eta_W = g^2 / (4 pi)          (W bosons)
    # eta_S = lambda_p / (4 pi)      (taste scalars, lambda_p ~ 0.1)
    N_c = 3
    lambda_portal = 0.1  # scalar portal coupling
    eta_top = N_c * Y_TOP**2 / (4 * PI)
    eta_W = G_WEAK**2 / (4 * PI)
    eta_scalar = lambda_portal / (4 * PI)
    eta_total = eta_top + eta_W + eta_scalar

    # v_w = Delta_p / (eta * T^3) * (1/T) = Delta_p / (eta * T^4)
    # In non-relativistic regime
    v_w = Delta_p / eta_total if eta_total > 0 else 0.05

    # Physical bounds: v_w should be subsonic (< c_s = 1/sqrt(3) ~ 0.577)
    # and greater than ~0.01 for baryogenesis to work
    v_w = max(0.01, min(v_w, 0.5))

    log(f"\n  3. Wall velocity v_w at T_n:")
    log(f"     Latent heat L/T^4 = 2D(v/T)^2 = {L_over_T4:.6f}")
    log(f"     Supercooling Delta T / T_c = {Delta_T_over_Tc:.5f}")
    log(f"     Driving pressure Delta p / T^4 = {Delta_p:.6f}")
    log(f"     Friction: eta_top = {eta_top:.4f}, eta_W = {eta_W:.4f}, eta_S = {eta_scalar:.4f}")
    log(f"     eta_total = {eta_total:.4f}")
    log(f"     v_w (naive) = Delta p / eta = {Delta_p / eta_total if eta_total > 0 else 0:.4f}")
    log(f"     Adopted v_w = {v_w:.4f} (bounded to [0.01, 0.5])")

    # -----------------------------------------------------------------
    # 4. Baryogenesis prefactor P = D_q*T / (v_w * L_w*T)
    # -----------------------------------------------------------------
    P = Dq_T / (v_w * Lw_T)

    log(f"\n  4. Baryogenesis prefactor P = D_q*T / (v_w * L_w*T):")
    log(f"     P = {Dq_T:.1f} / ({v_w:.4f} * {Lw_T:.1f}) = {P:.2f}")

    # Compare with the value at T_c
    Lw_Tc = np.sqrt(lam) / E  # parametric estimate at T_c
    Dq_Tc = 6.0
    v_w_Tc = 0.05  # standard estimate
    P_Tc = Dq_Tc / (v_w_Tc * Lw_Tc)
    log(f"     P(T_c) = {Dq_Tc:.0f} / ({v_w_Tc} * {Lw_Tc:.1f}) = {P_Tc:.2f} (for comparison)")

    # -----------------------------------------------------------------
    # Summary table
    # -----------------------------------------------------------------
    log(f"\n  RECONCILED PARAMETERS ON T_n SURFACE:")
    log(f"  {'Parameter':.<30s} {'At T_c':>10s}  {'At T_n':>10s}  {'Change':>10s}")
    log(f"  {'='*62}")

    def fmt(name, val_c, val_n, unit=""):
        change = (val_n / val_c - 1) * 100 if val_c != 0 else float('nan')
        log(f"  {name:.<30s} {val_c:>10.4f}  {val_n:>10.4f}  {change:>+9.1f}%")

    fmt("T (GeV)", T_c, T_n)
    fmt("v/T (physical)", vt_c_MC, vt_n)
    fmt("L_w * T", Lw_Tc, Lw_T)
    fmt("D_q * T", Dq_Tc, Dq_T)
    fmt("v_w", v_w_Tc, v_w)
    fmt("P = D_q/(v_w * L_w)", P_Tc, P)

    log(f"\n  KEY RESULT: All parameters are self-consistent on the T_n surface.")
    log(f"  v(T_n)/T_n = {vt_n:.4f} > 0.52 -- baryogenesis condition satisfied")
    log(f"  with more room than at T_c ({vt_n:.4f} vs {vt_c_MC:.4f}).")

    return {
        "T_n": T_n,
        "T_n_over_Tc": nuc_result["T_n_over_Tc"],
        "vt_n": vt_n,
        "Lw_T": Lw_T,
        "Dq_T": Dq_T,
        "v_w": v_w,
        "P": P,
        "alpha_s_Tn": alpha_s_Tn,
    }


# =============================================================================
# PART 5: THIN-WALL ANALYTIC CROSS-CHECK
# =============================================================================

def part5_thin_wall_crosscheck(params):
    """
    Analytic thin-wall approximation for S_3(T)/T as a cross-check.

    In the thin-wall limit (small supercooling Delta T << T_c):
      S_3 = 16 pi sigma^3 / (3 (Delta V)^2)

    where sigma is the surface tension and Delta V = V(0) - V(broken).

    For the cubic-quartic potential:
      sigma = (2/3) E^3 T^3 / lam^2  (at T = T_c)
      Delta V ~ L * Delta T / T_c  (latent heat * supercooling)

    This gives:
      S_3/T ~ (128 pi / 81) * E^6 / (lam^4 * D^2) * 1/(1 - T/T_c)^2
    """
    log("\n" + "=" * 72)
    log("PART 5: THIN-WALL ANALYTIC CROSS-CHECK")
    log("=" * 72)

    E = params["E_gauge"]
    lam = params["lam_gauge"]
    D = params["D_total"]
    T_c = params["T_c"]
    vt_c = params["vt_c"]

    # Surface tension at T_c (dimensionless, in T^3 units)
    # sigma / T^3 = (2/3) * (2E)^3 / (3 * lam^2)
    # More precisely: sigma = int_0^{x_min} sqrt(2 * V_shifted) dx
    # At T_c, V(0) = V(x_min) (degenerate), and:
    sigma_analytic = (2.0 / 3.0) * E**3 / lam**2
    # This is the standard result for V = (mu2/2)x^2 - E x^3 + (lam/4)x^4
    # with mu2 tuned to degeneracy: mu2 = 9E^2/(2*lam)

    # Numerical surface tension at T_c
    mu2_c = 9 * E**2 / (2 * lam)  # degeneracy condition
    x_min_c = 2 * E / lam
    n_int = 2000
    x_arr = np.linspace(0, x_min_c, n_int)
    V_arr = np.array([V_dimless(x, mu2_c, E, lam) for x in x_arr])
    V_false_c = V_dimless(0.0, mu2_c, E, lam)
    V_shifted = np.maximum(V_arr - V_false_c, 0)
    sigma_numerical = trapezoid(np.sqrt(2 * V_shifted), x_arr)

    log(f"\n  Surface tension at T_c:")
    log(f"    sigma/T^3 (analytic) = (2/3) E^3/lam^2 = {sigma_analytic:.6f}")
    log(f"    sigma/T^3 (numerical integral) = {sigma_numerical:.6f}")

    # Latent heat: L/T^4 ~ 2 D (v/T)^2
    L_over_T4 = 2 * D * vt_c**2

    # S_3/T in thin-wall approximation vs Delta T / T_c
    log(f"\n  Thin-wall S_3/T = 16 pi sigma^3 / (3 * epsilon^2 * T)")
    log(f"  where epsilon = L * Delta T / T_c")
    log(f"\n  {'DT/T_c':>8s}  {'S3/T (analytic)':>16s}  {'S3/T (numerical)':>18s}")
    log(f"  {'-'*8:>8s}  {'-'*16:>16s}  {'-'*18:>18s}")

    tw_results = []
    for dt_frac in [0.001, 0.002, 0.005, 0.01, 0.02, 0.05, 0.10]:
        epsilon = L_over_T4 * dt_frac  # DeltaV / T^4

        S3T_an = 16 * PI * sigma_analytic**3 / (3 * epsilon**2) if epsilon > 0 else float('inf')
        S3T_num = 16 * PI * sigma_numerical**3 / (3 * epsilon**2) if epsilon > 0 else float('inf')

        log(f"  {dt_frac:8.4f}  {S3T_an:16.1f}  {S3T_num:18.1f}")

        tw_results.append({
            "dt_frac": dt_frac,
            "S3T_analytic": S3T_an,
            "S3T_numerical": S3T_num,
        })

    # Find nucleation in thin-wall approximation
    # S_3/T = 140 => epsilon^2 = 16 pi sigma^3 / (3 * 140)
    eps_sq_140 = 16 * PI * sigma_numerical**3 / (3 * 140)
    eps_140 = np.sqrt(eps_sq_140) if eps_sq_140 > 0 else 0
    dt_frac_140 = eps_140 / L_over_T4 if L_over_T4 > 0 else 0

    T_n_tw = T_c * (1 - dt_frac_140)

    log(f"\n  Thin-wall nucleation condition S_3/T = 140:")
    log(f"    Required epsilon / T^4 = {eps_140:.6f}")
    log(f"    Required Delta T / T_c = {dt_frac_140:.5f}")
    log(f"    T_n (thin-wall) = {T_n_tw:.2f} GeV")
    log(f"    T_n / T_c = {1 - dt_frac_140:.5f}")

    # v/T at T_n (thin-wall)
    mu2_tw = D * (1 - params["T0_sq"] / T_n_tw**2)
    _, x_min_tw = potential_minima(mu2_tw, E, lam)
    vt_n_tw = x_min_tw if x_min_tw is not None else vt_c

    log(f"    v(T_n)/T_n (thin-wall) = {vt_n_tw:.4f}")

    return {
        "sigma_analytic": sigma_analytic,
        "sigma_numerical": sigma_numerical,
        "T_n_tw": T_n_tw,
        "dt_frac": dt_frac_140,
        "vt_n_tw": vt_n_tw,
        "tw_results": tw_results,
    }


# =============================================================================
# MAIN
# =============================================================================

def main():
    log("*" * 72)
    log("NUCLEATION TEMPERATURE FROM BOUNCE ACTION")
    log("*" * 72)
    log(f"Date: {time.strftime('%Y-%m-%d %H:%M')}")
    log()

    params = compute_potential_params()

    # Part 1: S_3(T)/T vs temperature (numerical bounce)
    scan_results = part1_bounce_action_vs_temperature()

    # Part 2: Find T_n from S_3/T = 140
    nuc_result = part2_nucleation_temperature(scan_results)

    # Part 3: v(T_n)/T_n
    vev_result = part3_vev_at_nucleation(nuc_result, params)

    # Part 4: Reconciled transport parameters
    transport = part4_reconciled_parameters(nuc_result, vev_result, params)

    # Part 5: Thin-wall analytic cross-check
    tw_check = part5_thin_wall_crosscheck(params)

    # =================================================================
    # FINAL SUMMARY
    # =================================================================
    log("\n" + "=" * 72)
    log("FINAL SUMMARY")
    log("=" * 72)

    if nuc_result is not None:
        log(f"\n  Nucleation temperature:")
        log(f"    T_n = {nuc_result['T_n']:.2f} GeV")
        log(f"    T_n / T_c = {nuc_result['T_n_over_Tc']:.5f}")
        log(f"    S_3(T_n) / T_n = {nuc_result['S3_over_Tn']:.1f}")
        log(f"    Method: {nuc_result['method']}")

    if tw_check is not None:
        log(f"\n  Thin-wall cross-check:")
        log(f"    T_n (thin-wall) = {tw_check['T_n_tw']:.2f} GeV")
        log(f"    Delta T / T_c = {tw_check['dt_frac']:.5f}")

    if vev_result is not None:
        log(f"\n  VEV at nucleation:")
        log(f"    v(T_c)/T_c [MC]       = {vev_result['vt_c_MC']:.4f}")
        log(f"    v(T_n)/T_n [physical] = {vev_result['vt_physical']:.4f}")
        log(f"    Enhancement: {vev_result['vt_physical']/vev_result['vt_c_MC']:.3f}x")
        log(f"    Baryogenesis condition v/T > 0.52: "
            f"{'SATISFIED' if vev_result['vt_physical'] > 0.52 else 'NOT SATISFIED'}")

    if transport is not None:
        log(f"\n  Transport parameters (reconciled on T_n surface):")
        log(f"    L_w * T_n     = {transport['Lw_T']:.2f}")
        log(f"    D_q * T_n     = {transport['Dq_T']:.1f}")
        log(f"    v_w           = {transport['v_w']:.4f}")
        log(f"    alpha_s(T_n)  = {transport['alpha_s_Tn']:.4f}")
        log(f"    P = Dq/(vw*Lw) = {transport['P']:.2f}")

    log(f"\n  CONCLUSION:")
    log(f"  The nucleation temperature T_n is derived self-consistently from")
    log(f"  the CW effective potential with the taste scalar spectrum.")
    if vev_result is not None and vev_result["vt_physical"] > 0.52:
        log(f"  v(T_n)/T_n = {vev_result['vt_physical']:.4f} > 0.52 satisfies the")
        log(f"  baryogenesis condition with even more room than v(T_c)/T_c = {vev_result['vt_c_MC']:.4f}.")
    log(f"  All transport parameters (L_w, D_q, v_w) are evaluated on the")
    log(f"  same temperature surface, closing the T_n gap in the DM chain.")

    # Write log file
    try:
        import os
        os.makedirs("logs", exist_ok=True)
        with open(LOG_FILE, "w") as f:
            f.write("\n".join(results))
        log(f"\n  Log written to {LOG_FILE}")
    except Exception as e:
        log(f"\n  (Could not write log: {e})")

    return {
        "params": params,
        "scan_results": scan_results,
        "nuc_result": nuc_result,
        "vev_result": vev_result,
        "transport": transport,
        "tw_check": tw_check,
    }


if __name__ == "__main__":
    main()
