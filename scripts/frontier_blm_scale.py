#!/usr/bin/env python3
"""
BLM Scale for Hierarchy -- alpha_V(q*) Determines v
====================================================

Computes the Brodsky-Lepage-Mackenzie (BLM) optimal scale q* for the
staggered fermion self-energy, evaluates the V-scheme coupling alpha_V(q*),
and determines whether the hierarchy formula yields v = 246 GeV.

PHYSICS:
  The hierarchy formula is:
      v = M_Pl * exp(-8 pi^2 / (N_eff * y_t^2))
      N_eff = 12 * Z_chi^2
      Z_chi = 1 - alpha_V(q*) * C_F * Sigma_1 / (4 pi)

  The BLM prescription (Brodsky, Lepage, Mackenzie 1983) defines the
  optimal scale q* so that the beta_0-dependent piece of the 1-loop
  correction is absorbed into the running coupling.  For the staggered
  fermion self-energy:

      Sigma(p=0) = (C_F * alpha_s / (4 pi)) * [Sigma_1 + beta_0 * Sigma_2]

  where Sigma_1 is the non-running tadpole integral and Sigma_2 contains
  the logarithmic piece.  The BLM scale satisfies:

      ln(q*a)^2 = -Sigma_2 / Sigma_1

  Following Lepage & Mackenzie (1993), Sigma_2 is obtained by inserting
  an extra ln(k^2 a^2) factor in the integrand (with k^2 = sum_mu 4 sin^2(k_mu/2),
  the gluon momentum squared in the Wilson action).

KEY INTEGRALS:
  Sigma_1 = (1/L^4) sum_{k!=0} [sum_mu sin^2(k_mu)] / [sum_nu sin^2(k_nu)]
          = d * I_stag(d) = 4 * I_stag(4)

  Sigma_2 = (1/L^4) sum_{k!=0} [sum_mu sin^2(k_mu)] / [sum_nu sin^2(k_nu)]
            * ln[sum_rho 4 sin^2(k_rho/2)]

  Note: the self-energy numerator simplifies since
  [sum_mu sin^2(k_mu)] / [sum_nu sin^2(k_nu)] = 1
  for the trace part, so Sigma_1 = I_stag(4) * d but actually the
  TRACE of the self-energy is d times the basic integral.

  More precisely:
  I_stag(4) = (1/L^4) sum_{k!=0} 1 / [sum_mu sin^2(k_mu)]
  Sigma_1 = d * I_stag(4) where d=4 is the spacetime dimension

  For the BLM integral:
  I_log = (1/L^4) sum_{k!=0} ln[khat^2] / [sum_mu sin^2(k_mu)]
  Sigma_2_eff = d * I_log
  ln(q*a)^2 = -I_log / I_stag

PStack experiment: blm-scale-hierarchy
Self-contained: numpy + scipy only.
"""

from __future__ import annotations

import math
import sys
import time

import numpy as np

try:
    from scipy.integrate import nquad
    HAS_SCIPY = True
except ImportError:
    HAS_SCIPY = False


np.set_printoptions(precision=10, linewidth=120)

LOG_FILE = "logs/" + time.strftime("%Y-%m-%d") + "-blm_scale.txt"

results = []
def log(msg=""):
    results.append(msg)
    print(msg)


# ============================================================================
# CONSTANTS
# ============================================================================

PI = np.pi
C_F = 4.0 / 3.0              # SU(3) Casimir
N_C = 3
N_F = 6                       # active flavors at Planck scale (all SM quarks)
BETA_0 = (11.0 * N_C - 2.0 * N_F) / (12.0 * PI)  # 1-loop beta function coeff
# beta_0 = (33 - 12)/(12 pi) = 21/(12 pi) = 7/(4 pi)
BETA_0_TRAD = (11.0 * N_C - 2.0 * N_F) / 3.0  # = 7, traditional normalization
M_PLANCK_RED = 2.435e18       # GeV (reduced Planck mass)
V_EW = 246.22                 # GeV (electroweak scale)
ALPHA_PLAQ = 0.092            # plaquette-scheme coupling at lattice/Planck scale


# ============================================================================
# LATTICE INTEGRALS
# ============================================================================

def I_stag_4d(L: int) -> float:
    """
    Staggered propagator at coincident points in d=4:
    I_stag(4) = (1/L^4) sum_{k != 0} 1 / [sum_mu sin^2(k_mu)]
    where k_mu = 2 pi n_mu / L.
    """
    n = np.arange(L)
    k = 2.0 * PI * n / L

    total = 0.0
    for n0 in range(L):
        k0 = 2.0 * PI * n0 / L
        s0 = np.sin(k0)**2
        k1, k2, k3 = np.meshgrid(k, k, k, indexing='ij')
        denom = s0 + np.sin(k1)**2 + np.sin(k2)**2 + np.sin(k3)**2
        flat = denom.ravel()
        mask = flat > 1e-30
        total += np.sum(1.0 / flat[mask])
    return total / L**4


def I_log_4d(L: int) -> float:
    """
    BLM logarithmic integral in d=4:
    I_log(4) = (1/L^4) sum_{k!=0} ln[khat^2] / [sum_mu sin^2(k_mu)]

    where khat^2 = sum_mu 4 sin^2(k_mu/2) is the Wilson gluon propagator
    momentum (the momentum that flows through the gluon line).

    This is the integral whose ratio with I_stag determines the BLM scale.
    """
    n = np.arange(L)
    k = 2.0 * PI * n / L

    total = 0.0
    for n0 in range(L):
        k0 = 2.0 * PI * n0 / L
        s0_stag = np.sin(k0)**2
        s0_wil = 4.0 * np.sin(k0 / 2.0)**2

        k1, k2, k3 = np.meshgrid(k, k, k, indexing='ij')
        denom_stag = s0_stag + np.sin(k1)**2 + np.sin(k2)**2 + np.sin(k3)**2
        khat2 = s0_wil + 4.0 * (np.sin(k1/2)**2 + np.sin(k2/2)**2 + np.sin(k3/2)**2)

        flat_denom = denom_stag.ravel()
        flat_khat2 = khat2.ravel()
        mask = (flat_denom > 1e-30) & (flat_khat2 > 1e-30)

        total += np.sum(np.log(flat_khat2[mask]) / flat_denom[mask])
    return total / L**4


def I_log_stag_4d(L: int) -> float:
    """
    Alternative BLM integral using staggered momentum in the log:
    I_log_stag = (1/L^4) sum_{k!=0} ln[sum_mu sin^2(k_mu)] / [sum_mu sin^2(k_mu)]

    This variant uses the staggered propagator momentum in the logarithm
    rather than the Wilson momentum.  Provides a cross-check.
    """
    n = np.arange(L)
    k = 2.0 * PI * n / L

    total = 0.0
    for n0 in range(L):
        k0 = 2.0 * PI * n0 / L
        s0 = np.sin(k0)**2
        k1, k2, k3 = np.meshgrid(k, k, k, indexing='ij')
        denom = s0 + np.sin(k1)**2 + np.sin(k2)**2 + np.sin(k3)**2
        flat = denom.ravel()
        mask = flat > 1e-30
        total += np.sum(np.log(flat[mask]) / flat[mask])
    return total / L**4


# ============================================================================
# Richardson extrapolation
# ============================================================================

def richardson(L_vals, vals, p=2):
    """Assume corrections ~ 1/L^p, extrapolate to L -> inf."""
    ext = []
    for i in range(len(L_vals) - 1):
        L1, S1 = L_vals[i], vals[i]
        L2, S2 = L_vals[i+1], vals[i+1]
        S_inf = (L2**p * S2 - L1**p * S1) / (L2**p - L1**p)
        ext.append((L1, L2, S_inf))
    return ext


# ============================================================================
# Hierarchy phenomenology
# ============================================================================

def compute_hierarchy(alpha_V, sigma1, y_t, M_Pl=M_PLANCK_RED):
    """
    v = M_Pl * exp(-8 pi^2 / (N_eff * y_t^2))
    N_eff = 12 * Z_chi^2
    Z_chi = 1 - alpha_V * C_F * Sigma_1 / (4 pi)
    """
    Z_chi = 1.0 - alpha_V * C_F * sigma1 / (4.0 * PI)
    if Z_chi <= 0:
        return dict(alpha_V=alpha_V, Z_chi=Z_chi, N_eff=0,
                    v_GeV=0, ratio=0, status="Z_chi <= 0")
    N_eff = 12.0 * Z_chi**2
    exponent = -8.0 * PI**2 / (N_eff * y_t**2)
    v = M_Pl * math.exp(exponent)
    return dict(alpha_V=alpha_V, Z_chi=Z_chi, N_eff=N_eff,
                v_GeV=v, ratio=v / V_EW, exponent=exponent,
                status="ok")


def alpha_V_for_target_v(sigma1, y_t, v_target=V_EW, M_Pl=M_PLANCK_RED):
    """Invert: find alpha_V that gives target v."""
    ln_ratio = math.log(v_target / M_Pl)
    N_eff_needed = -8.0 * PI**2 / (y_t**2 * ln_ratio)
    Z_chi_needed = math.sqrt(N_eff_needed / 12.0)
    alpha_needed = (1.0 - Z_chi_needed) * 4.0 * PI / (C_F * sigma1)
    return alpha_needed, N_eff_needed, Z_chi_needed


# ============================================================================
# V-scheme running coupling
# ============================================================================

def alpha_V_from_plaq(alpha_plaq, ln_q2a2):
    """
    V-scheme coupling from plaquette coupling:
    alpha_V(q) = alpha_plaq / (1 - alpha_plaq * beta_0_trad * ln(q^2 a^2) / (4 pi))

    Uses the standard 1-loop relation between schemes.
    beta_0_trad = (11 N_c - 2 N_f) / 3 = 7 for N_f=6.
    """
    denom = 1.0 - alpha_plaq * BETA_0_TRAD * ln_q2a2 / (4.0 * PI)
    if denom <= 0:
        return float('inf')
    return alpha_plaq / denom


# ============================================================================
# Scipy continuum cross-check
# ============================================================================

def scipy_I_stag():
    """Continuum quadrature for I_stag(4)."""
    if not HAS_SCIPY:
        return None

    def integrand(k0, k1, k2, k3):
        denom = np.sin(k0)**2 + np.sin(k1)**2 + np.sin(k2)**2 + np.sin(k3)**2
        if denom < 1e-30:
            return 0.0
        return 1.0 / denom

    lims = [(0, 2*PI)] * 4
    val, err = nquad(integrand, lims, opts={'limit': 100, 'epsabs': 1e-8})
    return val / (2*PI)**4, err / (2*PI)**4


def scipy_I_log():
    """Continuum quadrature for I_log(4) with Wilson khat^2."""
    if not HAS_SCIPY:
        return None

    def integrand(k0, k1, k2, k3):
        denom = np.sin(k0)**2 + np.sin(k1)**2 + np.sin(k2)**2 + np.sin(k3)**2
        khat2 = 4.0 * (np.sin(k0/2)**2 + np.sin(k1/2)**2
                        + np.sin(k2/2)**2 + np.sin(k3/2)**2)
        if denom < 1e-30 or khat2 < 1e-30:
            return 0.0
        return np.log(khat2) / denom

    lims = [(0, 2*PI)] * 4
    val, err = nquad(integrand, lims, opts={'limit': 100, 'epsabs': 1e-8})
    return val / (2*PI)**4, err / (2*PI)**4


# ============================================================================
# Main computation
# ============================================================================

def main():
    t_start = time.time()

    log("=" * 78)
    log("   BLM SCALE FOR HIERARCHY: alpha_V(q*) DETERMINES v")
    log("   Brodsky-Lepage-Mackenzie optimal scale for staggered self-energy")
    log("=" * 78)
    log()

    # ------------------------------------------------------------------
    # SECTION 1: Lattice integrals -- I_stag and I_log
    # ------------------------------------------------------------------
    log("=" * 78)
    log("1. LATTICE INTEGRALS: I_stag(4) and I_log(4)")
    log("=" * 78)
    log()
    log("  I_stag(4) = (1/L^4) sum_{k!=0} 1/[sum_mu sin^2(k_mu)]")
    log("  I_log(4)  = (1/L^4) sum_{k!=0} ln[khat^2] / [sum_mu sin^2(k_mu)]")
    log("  where khat^2 = sum_mu 4 sin^2(k_mu/2) (Wilson gluon momentum)")
    log()

    # Lattice sizes for computation
    # L=64 takes O(minutes) for three integrals; include if patient
    L_vals = [8, 16, 32]
    I_stag_vals = []
    I_log_vals = []
    I_log_stag_vals = []

    for L in L_vals:
        t0 = time.time()
        Is = I_stag_4d(L)
        Il = I_log_4d(L)
        Ils = I_log_stag_4d(L)
        dt = time.time() - t0
        I_stag_vals.append(Is)
        I_log_vals.append(Il)
        I_log_stag_vals.append(Ils)
        log(f"  L={L:4d}: I_stag = {Is:.12f}  I_log = {Il:.12f}"
            f"  I_log_stag = {Ils:.12f}  ({dt:.1f}s)")

    log()

    # Try L=64 (takes ~2 min for I_stag + I_log)
    log("  Computing L=64 (may take a few minutes)...")
    t0 = time.time()
    Is64 = I_stag_4d(64)
    Il64 = I_log_4d(64)
    dt = time.time() - t0
    L_vals.append(64)
    I_stag_vals.append(Is64)
    I_log_vals.append(Il64)
    I_log_stag_vals.append(0.0)  # placeholder
    log(f"  L={64:4d}: I_stag = {Is64:.12f}  I_log = {Il64:.12f}"
        f"  ({dt:.1f}s)")
    log()

    # Richardson extrapolation
    log("  Richardson extrapolation (corrections ~ 1/L^2):")
    log()

    rich_stag = richardson(L_vals, I_stag_vals, p=2)
    rich_log = richardson(L_vals, I_log_vals, p=2)

    for (L1, L2, Sinf) in rich_stag:
        log(f"    I_stag: ({L1},{L2}) -> {Sinf:.12f}")
    log()

    for (L1, L2, Sinf) in rich_log:
        log(f"    I_log:  ({L1},{L2}) -> {Sinf:.12f}")
    log()

    # Best estimates from largest pair
    I_stag_inf = rich_stag[-1][2]
    I_log_inf = rich_log[-1][2]

    # Also do 2nd-order Richardson if we have enough points
    if len(rich_stag) >= 2:
        L2_stag = [(rich_stag[i][1], rich_stag[i+1][1],
                     (rich_stag[i+1][2] * rich_stag[i+1][1]**2 - rich_stag[i][2] * rich_stag[i][1]**2)
                     / (rich_stag[i+1][1]**2 - rich_stag[i][1]**2))
                    for i in range(len(rich_stag)-1)]
        for (L1, L2, S2) in L2_stag:
            log(f"    I_stag 2nd-order Rich: ({L1},{L2}) -> {S2:.12f}")
        # Use simple Richardson for now
    log()

    Sigma_1 = 4.0 * I_stag_inf   # d * I_stag(d) where d=4
    Sigma_2_eff = 4.0 * I_log_inf

    log(f"  Best estimates:")
    log(f"    I_stag(4)  = {I_stag_inf:.12f}")
    log(f"    I_log(4)   = {I_log_inf:.12f}")
    log(f"    Sigma_1    = d * I_stag = {Sigma_1:.10f}")
    log(f"    Sigma_2    = d * I_log  = {Sigma_2_eff:.10f}")
    log()

    # ------------------------------------------------------------------
    # Scipy cross-check (skipped: 4D quadrature with 1/k^2 singularity
    # is unreliable with nquad; lattice sums with Richardson extrapolation
    # give better precision for these integrals)
    # ------------------------------------------------------------------
    I_stag_best = I_stag_inf
    I_log_best = I_log_inf

    Sigma_1_best = 4.0 * I_stag_best
    Sigma_2_best = 4.0 * I_log_best

    log(f"  FINAL VALUES (best available):")
    log(f"    I_stag(4)  = {I_stag_best:.12f}")
    log(f"    I_log(4)   = {I_log_best:.12f}")
    log(f"    Sigma_1    = {Sigma_1_best:.10f}")
    log(f"    Sigma_2    = {Sigma_2_best:.10f}")
    log()

    # ------------------------------------------------------------------
    # SECTION 2: BLM scale q*
    # ------------------------------------------------------------------
    log("=" * 78)
    log("2. BLM SCALE q*")
    log("=" * 78)
    log()
    log("  The BLM prescription sets:")
    log("    ln(q*a)^2 = -I_log / I_stag")
    log()
    log("  This absorbs all beta_0-dependent terms into the running coupling,")
    log("  leaving a scale- and scheme-independent coefficient.")
    log()

    ratio = I_log_best / I_stag_best

    # BLM prescription: the mean-value theorem gives
    # ln(q*^2 a^2) = <ln(khat^2 a^2)> = I_log / I_stag
    #
    # The SIGN here follows Lepage-Mackenzie (1993) eq. (2.4):
    # The 1-loop self-energy is Sigma = (alpha_s/(4pi)) * [Sigma_1 + beta_0 * Sigma_2]
    # where Sigma_2 = integral with ln(mu^2 a^2) pulled out.
    #
    # Setting mu = q* to absorb Sigma_2:
    #   ln(q*^2 a^2) = Sigma_2 / (beta_0 * Sigma_1)
    # But Sigma_2 as defined here already has the log in the integrand,
    # so the BLM scale is simply the WEIGHTED AVERAGE of ln(khat^2):
    #   ln(q*^2 a^2) = I_log / I_stag  (positive for typical lattice integrals)
    #
    # The NEGATIVE sign convention applies when Sigma_2 is defined with
    # an explicit minus sign from the counterterm. Here we use the positive
    # convention following Lepage-Mackenzie.
    ln_q2a2_pos = ratio   # Positive: q* > 1/a
    ln_q2a2_neg = -ratio  # Negative: q* < 1/a

    log(f"  I_log / I_stag = {ratio:.10f}")
    log()
    log(f"  Convention A (LM eq 2.4, ln(q*^2 a^2) = +ratio):")
    q_star_pos = math.exp(ln_q2a2_pos / 2.0)
    log(f"    ln(q*^2 a^2) = +{ln_q2a2_pos:.10f}")
    log(f"    q* a = {q_star_pos:.10f}")
    log(f"    q* / (pi/a) = {q_star_pos / PI:.10f}")
    log()
    log(f"  Convention B (ln(q*^2 a^2) = -ratio):")
    q_star_neg = math.exp(ln_q2a2_neg / 2.0)
    log(f"    ln(q*^2 a^2) = {ln_q2a2_neg:.10f}")
    log(f"    q* a = {q_star_neg:.10f}")
    log(f"    q* / (pi/a) = {q_star_neg / PI:.10f}")
    log()

    # Use POSITIVE convention (standard LM):
    # q* > 1/a means the relevant gluon momentum is above the lattice scale,
    # which is physically sensible for the UV-dominated tadpole integral
    ln_q2a2 = ln_q2a2_pos
    q_star_a = q_star_pos

    q_star_a = math.exp(ln_q2a2 / 2.0)  # q* in units of 1/a

    log()

    # For reference: Lepage-Mackenzie typical values
    log("  CONTEXT: Lepage-Mackenzie (1993) typical BLM scales:")
    log("    Wilson fermion self-energy: q*a ~ 2.63 (ln(q*a)^2 ~ 1.93)")
    log("    Plaquette:                  q*a ~ 3.41 (ln(q*a)^2 ~ 2.45)")
    log("    Staggered fermion SE:       q*a ~ pi/a (expected near edge)")
    log()

    # ------------------------------------------------------------------
    # SECTION 3: alpha_V(q*)
    # ------------------------------------------------------------------
    log("=" * 78)
    log("3. V-SCHEME COUPLING alpha_V(q*)")
    log("=" * 78)
    log()
    log("  alpha_V(q) = alpha_plaq / (1 - alpha_plaq * beta_0^trad * ln(q^2 a^2) / (4 pi))")
    log()
    log(f"  Input: alpha_plaq = {ALPHA_PLAQ:.4f}")
    log(f"         beta_0^trad = (11*{N_C} - 2*{N_F})/3 = {BETA_0_TRAD:.1f}")
    log(f"         ln(q*^2 a^2) = {ln_q2a2:.10f}")
    log()

    alpha_V_pos = alpha_V_from_plaq(ALPHA_PLAQ, ln_q2a2_pos)
    alpha_V_neg = alpha_V_from_plaq(ALPHA_PLAQ, ln_q2a2_neg)
    alpha_V_star = alpha_V_pos  # positive convention

    log(f"  Convention A (q* > 1/a): alpha_V(q*) = {alpha_V_pos:.10f}")
    log(f"  Convention B (q* < 1/a): alpha_V(q*) = {alpha_V_neg:.10f}")
    log()
    log(f"  USING Convention A: alpha_V(q*) = {alpha_V_star:.10f}")
    log()

    # Also compute at some reference scales for comparison
    log("  alpha_V at various scales:")
    log(f"    q*a = {q_star_a:.4f}  ->  alpha_V = {alpha_V_star:.6f}  [BLM optimal]")
    for qa in [1.0, PI/2, PI, 2*PI, 3.0]:
        lnq = 2.0 * math.log(qa)
        aV = alpha_V_from_plaq(ALPHA_PLAQ, lnq)
        log(f"    q*a = {qa:.4f}  ->  alpha_V = {aV:.6f}")
    log()

    # ------------------------------------------------------------------
    # SECTION 4: Hierarchy formula -> v
    # ------------------------------------------------------------------
    log("=" * 78)
    log("4. HIERARCHY FORMULA: v FROM BLM-DETERMINED alpha_V(q*)")
    log("=" * 78)
    log()

    # Framework-derived top Yukawa at Planck scale
    # y_t(M_Pl) = g_s(M_Pl)/sqrt(6) = 0.414
    # This comes from the ratio y_t/g_s = 1/sqrt(6) being protected
    y_t_planck = 0.414
    g_s_planck = y_t_planck * math.sqrt(6)

    log(f"  Parameters:")
    log(f"    y_t(M_Pl)   = {y_t_planck:.4f} (framework: y_t/g_s = 1/sqrt(6))")
    log(f"    g_s(M_Pl)   = {g_s_planck:.4f}")
    log(f"    Sigma_1     = {Sigma_1_best:.10f}")
    log(f"    alpha_V(q*) = {alpha_V_star:.10f}")
    log(f"    C_F         = {C_F:.6f}")
    log(f"    M_Pl (red)  = {M_PLANCK_RED:.3e} GeV")
    log()

    h = compute_hierarchy(alpha_V_star, Sigma_1_best, y_t_planck)

    log(f"  Z_chi    = 1 - alpha_V * C_F * Sigma_1 / (4 pi)")
    log(f"           = 1 - {alpha_V_star:.6f} * {C_F:.4f} * {Sigma_1_best:.6f} / {4*PI:.6f}")
    log(f"           = {h['Z_chi']:.10f}")
    log()
    log(f"  N_eff    = 12 * Z_chi^2 = {h['N_eff']:.10f}")
    log(f"  exponent = -8 pi^2 / (N_eff * y_t^2) = {h['exponent']:.6f}")
    log()
    log(f"  v = M_Pl * exp(exponent)")
    log(f"    = {M_PLANCK_RED:.3e} * exp({h['exponent']:.6f})")
    log(f"    = {h['v_GeV']:.6f} GeV")
    log()
    log(f"  v / v_EW = {h['ratio']:.6f}")
    log()

    if 0.5 < h['ratio'] < 2.0:
        log("  *** v IS WITHIN FACTOR 2 OF 246 GeV ***")
    if 0.9 < h['ratio'] < 1.1:
        log("  *** v MATCHES 246 GeV TO WITHIN 10% ***")
    if 0.99 < h['ratio'] < 1.01:
        log("  *** v MATCHES 246 GeV TO WITHIN 1% ***")
    log()

    # ------------------------------------------------------------------
    # SECTION 5: What alpha_V would be needed for exact v = 246?
    # ------------------------------------------------------------------
    log("=" * 78)
    log("5. INVERSE: WHAT alpha_V GIVES EXACT v = 246 GeV?")
    log("=" * 78)
    log()

    alpha_needed, N_needed, Z_needed = alpha_V_for_target_v(
        Sigma_1_best, y_t_planck, v_target=V_EW)

    log(f"  For v = {V_EW} GeV exactly:")
    log(f"    N_eff needed  = {N_needed:.10f}")
    log(f"    Z_chi needed  = {Z_needed:.10f}")
    log(f"    alpha_V needed = {alpha_needed:.10f}")
    log()

    # What BLM scale would give this alpha_V?
    # alpha_V = alpha_plaq / (1 - alpha_plaq * beta_0 * ln(q^2 a^2) / (4 pi))
    # => 1 - alpha_plaq * beta_0 * ln(q^2) / (4 pi) = alpha_plaq / alpha_V
    # => ln(q^2 a^2) = (1 - alpha_plaq/alpha_V) * 4 pi / (alpha_plaq * beta_0)
    ln_q2_needed = (1.0 - ALPHA_PLAQ / alpha_needed) * 4.0 * PI / (ALPHA_PLAQ * BETA_0_TRAD)
    q_needed = math.exp(ln_q2_needed / 2.0)
    ratio_needed = -ln_q2_needed * I_stag_best  # The I_log that would give this

    log(f"  Required BLM parameters:")
    log(f"    ln(q^2 a^2) = {ln_q2_needed:.10f}")
    log(f"    q*a          = {q_needed:.10f}")
    log(f"    I_log needed = {-ln_q2_needed * I_stag_best:.10f}")
    log(f"    Actual I_log = {I_log_best:.10f}")
    log()

    # ------------------------------------------------------------------
    # SECTION 6: Sensitivity analysis
    # ------------------------------------------------------------------
    log("=" * 78)
    log("6. SENSITIVITY ANALYSIS")
    log("=" * 78)
    log()

    log("  Variation of v with alpha_V (Sigma_1, y_t fixed):")
    log(f"  {'alpha_V':>10s}  {'Z_chi':>10s}  {'N_eff':>10s}  {'v (GeV)':>14s}  {'v/v_EW':>10s}")
    log("  " + "-" * 60)
    for aV in np.linspace(0.08, 0.25, 18):
        h2 = compute_hierarchy(aV, Sigma_1_best, y_t_planck)
        if h2['status'] == 'ok' and h2['v_GeV'] > 0 and h2['v_GeV'] < 1e30:
            marker = " <-- BLM" if abs(aV - alpha_V_star) < 0.005 else ""
            marker = " <-- TARGET" if abs(aV - alpha_needed) < 0.005 else marker
            log(f"  {aV:10.4f}  {h2['Z_chi']:10.6f}  {h2['N_eff']:10.6f}"
                f"  {h2['v_GeV']:14.4f}  {h2['ratio']:10.6f}{marker}")
    log()

    log("  Variation of v with y_t (alpha_V = BLM value fixed):")
    log(f"  {'y_t':>10s}  {'N_eff':>10s}  {'v (GeV)':>14s}  {'v/v_EW':>10s}")
    log("  " + "-" * 50)
    for yt in np.linspace(0.35, 0.50, 16):
        h3 = compute_hierarchy(alpha_V_star, Sigma_1_best, yt)
        if h3['status'] == 'ok' and h3['v_GeV'] > 0 and h3['v_GeV'] < 1e30:
            marker = " <-- framework" if abs(yt - y_t_planck) < 0.005 else ""
            log(f"  {yt:10.4f}  {h3['N_eff']:10.6f}  {h3['v_GeV']:14.4f}"
                f"  {h3['ratio']:10.6f}{marker}")
    log()

    # ------------------------------------------------------------------
    # SECTION 7: Alternative N_f values
    # ------------------------------------------------------------------
    log("=" * 78)
    log("7. DEPENDENCE ON N_f (NUMBER OF ACTIVE FLAVORS)")
    log("=" * 78)
    log()
    log("  The BLM scale is independent of N_f (it depends only on the")
    log("  self-energy integrals). But alpha_V(q*) depends on beta_0,")
    log("  which depends on N_f.")
    log()

    for nf in [0, 3, 4, 5, 6]:
        b0 = (11.0 * N_C - 2.0 * nf) / 3.0
        aV_nf = ALPHA_PLAQ / (1.0 - ALPHA_PLAQ * b0 * ln_q2a2 / (4.0 * PI))
        h_nf = compute_hierarchy(aV_nf, Sigma_1_best, y_t_planck)
        v_str = f"{h_nf['v_GeV']:.4f}" if h_nf['status'] == 'ok' and 0 < h_nf['v_GeV'] < 1e30 else "divergent"
        log(f"  N_f={nf}: beta_0={b0:.1f}  alpha_V(q*)={aV_nf:.6f}"
            f"  v={v_str} GeV")
    log()

    # ------------------------------------------------------------------
    # SECTION 8: Summary
    # ------------------------------------------------------------------
    log("=" * 78)
    log("8. SUMMARY")
    log("=" * 78)
    log()

    log(f"  Staggered self-energy integrals (d=4):")
    log(f"    I_stag       = {I_stag_best:.12f}")
    log(f"    I_log        = {I_log_best:.12f}")
    log(f"    Sigma_1      = 4 * I_stag = {Sigma_1_best:.10f}")
    log()
    log(f"  BLM scale:")
    log(f"    ln(q*^2 a^2) = I_log/I_stag = {ln_q2a2:.10f}")
    log(f"    q*a           = {q_star_a:.10f}")
    log()
    log(f"  V-scheme coupling at BLM scale:")
    log(f"    alpha_plaq    = {ALPHA_PLAQ:.4f}")
    log(f"    alpha_V(q*)   = {alpha_V_star:.10f}")
    log()
    log(f"  Hierarchy result:")
    log(f"    Z_chi         = {h['Z_chi']:.10f}")
    log(f"    N_eff         = {h['N_eff']:.10f}")
    log(f"    v             = {h['v_GeV']:.6f} GeV")
    log(f"    v / 246.22    = {h['ratio']:.6f}")
    log()
    log(f"  For exact v = 246 GeV:")
    log(f"    alpha_V needed = {alpha_needed:.10f}")
    log(f"    Discrepancy    = {abs(alpha_V_star - alpha_needed) / alpha_needed * 100:.1f}%")
    log()

    close_enough = 0.5 < h['ratio'] < 2.0
    log(f"  VERDICT: alpha_V(q*) = {alpha_V_star:.4f} from BLM prescription")
    if 0.95 < h['ratio'] < 1.05:
        log(f"  -> v = {h['v_GeV']:.2f} GeV  =>  ELECTROWEAK SCALE DERIVED (< 5% error)")
    elif close_enough:
        log(f"  -> v = {h['v_GeV']:.2f} GeV  =>  CORRECT ORDER OF MAGNITUDE")
        log(f"     (factor {h['ratio']:.2f} from 246 GeV)")
    else:
        log(f"  -> v = {h['v_GeV']:.2e} GeV  =>  DOES NOT MATCH")
    log()

    elapsed = time.time() - t_start
    log(f"  Total computation time: {elapsed:.1f}s")

    # Save log
    try:
        import os
        os.makedirs("logs", exist_ok=True)
        with open(LOG_FILE, "w") as f:
            f.write("\n".join(results))
        log(f"\n  Log saved to {LOG_FILE}")
    except Exception as e:
        log(f"\n  Could not save log: {e}")


if __name__ == "__main__":
    main()
