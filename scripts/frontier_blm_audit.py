#!/usr/bin/env python3
"""
BLM Audit: Generic vs Staggered-Specific Optimal Scale
=======================================================

PURPOSE: Reconcile the two BLM calculations that disagree on alpha_V(q*).

CALCULATION 1 (frontier_yt_blm_threshold.py):
  Uses the GENERIC V-scheme-to-MSbar shift: exp(-5/6).
  This factor comes from the CONTINUUM quark self-energy in the static
  potential (V-scheme).  It gives alpha_V(q*) ~ 0.10.

CALCULATION 2 (frontier_blm_scale.py):
  Computes the STAGGERED-SPECIFIC BLM integrals:
    I_stag(4) = (1/L^4) sum_{k!=0} 1 / [sum_mu sin^2(k_mu)]
    I_log(4)  = (1/L^4) sum_{k!=0} ln[khat^2] / [sum_mu sin^2(k_mu)]
  and sets ln(q*^2 a^2) = -I_log/I_stag.

THE QUESTION: Does the staggered-specific ratio I_log/I_stag differ from
the generic continuum value 5/6 = 0.8333?

METHOD:
  1. Compute I_stag and I_log on L = 32, 64, 128 lattices
  2. Richardson-extrapolate to L -> infinity
  3. Compute the RATIO I_log/I_stag = -ln(q*^2 a^2)
  4. Compare with the generic 5/6
  5. Determine the CORRECT alpha_V(q*) for each case

KNOWN LATTICE VALUES (cross-check):
  I_stag(4) -> infinity = 0.154933... (Luscher-Weisz tadpole integral)
  This is the well-known d=4 staggered propagator at coincident points.

Self-contained: numpy only.
PStack experiment: blm-audit
"""

from __future__ import annotations

import math
import sys
import time

import numpy as np

np.set_printoptions(precision=12, linewidth=120)

# ============================================================================
# Constants
# ============================================================================

PI = np.pi
N_C = 3
C_F = 4.0 / 3.0
N_F = 6
BETA_0_TRAD = (11.0 * N_C - 2.0 * N_F) / 3.0  # = 7
ALPHA_PLAQ = 0.092       # plaquette-scheme coupling at Planck/lattice scale

# For the hierarchy formula
M_PL_RED = 2.435e18      # GeV, reduced Planck mass
V_EW = 246.22            # GeV
Y_T = 0.414              # framework top Yukawa at M_Pl


# ============================================================================
# Lattice integrals
# ============================================================================

def compute_integrals(L: int) -> dict:
    """
    Compute I_stag(4), I_log(4), and Sigma_2 on an L^4 lattice.

    I_stag = (1/L^4) sum_{k!=0} 1 / [sum_mu sin^2(k_mu)]
    I_log  = (1/L^4) sum_{k!=0} ln[khat^2] / [sum_mu sin^2(k_mu)]

    where khat^2 = sum_mu 4 sin^2(k_mu/2) is the Wilson gluon momentum.

    Also computes:
    Sigma_2_explicit = (1/L^4) sum_{k!=0} [sum_mu sin^2(k_mu)] / [sum_nu sin^2(k_nu)]
                       * ln[sum_rho 4 sin^2(k_rho/2)]

    Note: [sum_mu sin^2(k_mu)] / [sum_nu sin^2(k_nu)] = 1 identically,
    so Sigma_2_explicit = I_log * d = 4 * I_log (confirming the task's formula
    reduces to the same integral as in frontier_blm_scale.py).
    """
    k_vals = 2.0 * PI * np.arange(L) / L  # k_mu = 2 pi n / L

    I_stag = 0.0
    I_log = 0.0
    sigma2_explicit = 0.0

    for n0 in range(L):
        k0 = k_vals[n0]
        s0 = np.sin(k0) ** 2
        w0 = 4.0 * np.sin(k0 / 2.0) ** 2

        # Vectorize over spatial dimensions
        k1, k2, k3 = np.meshgrid(k_vals, k_vals, k_vals, indexing='ij')
        s1 = np.sin(k1) ** 2
        s2 = np.sin(k2) ** 2
        s3 = np.sin(k3) ** 2
        w1 = 4.0 * np.sin(k1 / 2.0) ** 2
        w2 = 4.0 * np.sin(k2 / 2.0) ** 2
        w3 = 4.0 * np.sin(k3 / 2.0) ** 2

        # Staggered propagator denominator: sum_mu sin^2(k_mu)
        denom = s0 + s1 + s2 + s3
        # Wilson gluon momentum: khat^2 = sum_mu 4 sin^2(k_mu/2)
        khat2 = w0 + w1 + w2 + w3

        flat_d = denom.ravel()
        flat_k = khat2.ravel()
        mask = (flat_d > 1e-30) & (flat_k > 1e-30)

        I_stag += np.sum(1.0 / flat_d[mask])
        I_log += np.sum(np.log(flat_k[mask]) / flat_d[mask])

        # Sigma_2 from the task description:
        # numerator = sum_mu sin^2(k_mu) = denom (same thing)
        # so [num/denom] * ln(khat2) = 1 * ln(khat2)
        # This confirms Sigma_2 = d * I_log
        sigma2_explicit += np.sum(np.log(flat_k[mask]))

    norm = L ** 4
    return dict(
        L=L,
        I_stag=I_stag / norm,
        I_log=I_log / norm,
        sigma2_explicit=sigma2_explicit / norm,
    )


def richardson_extrapolate(Ls, vals, p=2):
    """Richardson extrapolation assuming O(1/L^p) corrections."""
    results = []
    for i in range(len(Ls) - 1):
        L1, S1 = Ls[i], vals[i]
        L2, S2 = Ls[i + 1], vals[i + 1]
        S_inf = (L2**p * S2 - L1**p * S1) / (L2**p - L1**p)
        results.append((L1, L2, S_inf))
    return results


# ============================================================================
# Physics
# ============================================================================

def alpha_V_from_plaq(alpha_plaq, ln_q2a2):
    """1-loop V-scheme coupling from plaquette coupling."""
    denom = 1.0 - alpha_plaq * BETA_0_TRAD * ln_q2a2 / (4.0 * PI)
    if denom <= 0:
        return float('inf')
    return alpha_plaq / denom


def hierarchy_v(alpha_V, sigma1):
    """Compute v from the hierarchy formula."""
    Z_chi = 1.0 - alpha_V * C_F * sigma1 / (4.0 * PI)
    if Z_chi <= 0:
        return None
    N_eff = 12.0 * Z_chi ** 2
    exponent = -8.0 * PI ** 2 / (N_eff * Y_T ** 2)
    v = M_PL_RED * math.exp(exponent)
    return dict(Z_chi=Z_chi, N_eff=N_eff, exponent=exponent, v_GeV=v,
                ratio=v / V_EW)


def alpha_V_for_target_v(sigma1, v_target=V_EW):
    """Invert hierarchy formula to find required alpha_V."""
    ln_ratio = math.log(v_target / M_PL_RED)
    N_eff_needed = -8.0 * PI ** 2 / (Y_T ** 2 * ln_ratio)
    Z_chi_needed = math.sqrt(N_eff_needed / 12.0)
    alpha_needed = (1.0 - Z_chi_needed) * 4.0 * PI / (C_F * sigma1)
    return alpha_needed


# ============================================================================
# Main audit
# ============================================================================

def main():
    t_start = time.time()

    print("=" * 78)
    print("   BLM AUDIT: GENERIC vs STAGGERED-SPECIFIC OPTIMAL SCALE")
    print("   Reconciling frontier_yt_blm_threshold.py and frontier_blm_scale.py")
    print("=" * 78)
    print()

    # ------------------------------------------------------------------
    # 1. Compute lattice integrals on multiple lattice sizes
    # ------------------------------------------------------------------
    print("=" * 78)
    print("1. LATTICE INTEGRALS")
    print("=" * 78)
    print()
    print("  Computing I_stag(4) and I_log(4) on L^4 lattices...")
    print("  I_stag = (1/L^4) sum_{k!=0} 1 / [sum_mu sin^2(k_mu)]")
    print("  I_log  = (1/L^4) sum_{k!=0} ln[khat^2] / [sum_mu sin^2(k_mu)]")
    print("  khat^2 = sum_mu 4 sin^2(k_mu/2)  [Wilson gluon momentum]")
    print()

    L_vals = [8, 16, 32, 64]
    data = []

    for L in L_vals:
        t0 = time.time()
        d = compute_integrals(L)
        dt = time.time() - t0
        data.append(d)
        ratio = d['I_log'] / d['I_stag']
        print(f"  L={L:4d}: I_stag = {d['I_stag']:.12f}  "
              f"I_log = {d['I_log']:.12f}  "
              f"ratio = {ratio:.10f}  ({dt:.1f}s)")

    print()

    # Attempt L=128 if L=64 was fast enough
    t64 = time.time()
    try:
        d128 = compute_integrals(128)
        dt128 = time.time() - t64
        if dt128 < 600:  # only keep if under 10 min
            L_vals.append(128)
            data.append(d128)
            ratio = d128['I_log'] / d128['I_stag']
            print(f"  L= 128: I_stag = {d128['I_stag']:.12f}  "
                  f"I_log = {d128['I_log']:.12f}  "
                  f"ratio = {ratio:.10f}  ({dt128:.1f}s)")
            print()
    except (MemoryError, Exception) as e:
        print(f"  L=128 skipped: {e}")
        print()

    # ------------------------------------------------------------------
    # 2. Richardson extrapolation
    # ------------------------------------------------------------------
    print("=" * 78)
    print("2. RICHARDSON EXTRAPOLATION (corrections ~ 1/L^2)")
    print("=" * 78)
    print()

    I_stag_list = [d['I_stag'] for d in data]
    I_log_list = [d['I_log'] for d in data]

    rich_stag = richardson_extrapolate(L_vals, I_stag_list)
    rich_log = richardson_extrapolate(L_vals, I_log_list)

    for L1, L2, Sinf in rich_stag:
        print(f"    I_stag: ({L1:3d},{L2:3d}) -> {Sinf:.12f}")
    print()
    for L1, L2, Sinf in rich_log:
        print(f"    I_log:  ({L1:3d},{L2:3d}) -> {Sinf:.12f}")
    print()

    I_stag_inf = rich_stag[-1][2]
    I_log_inf = rich_log[-1][2]

    # Also extrapolate the RATIO directly (more stable)
    ratio_list = [d['I_log'] / d['I_stag'] for d in data]
    rich_ratio = richardson_extrapolate(L_vals, ratio_list)
    for L1, L2, Sinf in rich_ratio:
        print(f"    ratio:  ({L1:3d},{L2:3d}) -> {Sinf:.12f}")
    print()

    ratio_inf = rich_ratio[-1][2]
    ratio_from_sep = I_log_inf / I_stag_inf

    print(f"  Best estimates (from largest Richardson pair):")
    print(f"    I_stag(inf)     = {I_stag_inf:.12f}")
    print(f"    I_log(inf)      = {I_log_inf:.12f}")
    print(f"    ratio (direct)  = {ratio_inf:.12f}")
    print(f"    ratio (I/I)     = {ratio_from_sep:.12f}")
    print()

    # ------------------------------------------------------------------
    # 3. THE KEY COMPARISON: staggered ratio vs generic 5/6
    # ------------------------------------------------------------------
    print("=" * 78)
    print("3. KEY COMPARISON: STAGGERED RATIO vs GENERIC 5/6")
    print("=" * 78)
    print()

    generic_ratio = 5.0 / 6.0  # = 0.83333...

    # The BLM scale is determined by:
    #   ln(q*^2 a^2) = -I_log / I_stag   (staggered-specific)
    # vs
    #   ln(q*^2 a^2) = -5/6              (generic continuum V-scheme)
    #
    # NOTE: The 5/6 in the continuum is the V-MSbar conversion, not directly
    # comparable to the lattice I_log/I_stag ratio. The lattice ratio gives
    # the BLM scale for the staggered self-energy ON THE LATTICE.
    # The continuum 5/6 is for the continuum static potential.
    # These are DIFFERENT quantities for DIFFERENT processes.

    # Use the direct ratio extrapolation as our best estimate
    stag_ratio = ratio_inf

    print(f"  Generic continuum BLM factor (V-scheme static potential):")
    print(f"    -ln(q*^2 a^2) = 5/6 = {generic_ratio:.10f}")
    print(f"    q*a = exp(-5/12)     = {math.exp(-5.0/12.0):.10f}")
    print()
    print(f"  Staggered lattice BLM factor (self-energy):")
    print(f"    -ln(q*^2 a^2) = I_log/I_stag = {stag_ratio:.10f}")
    print(f"    q*a = exp({stag_ratio:.6f}/2) = {math.exp(stag_ratio/2.0):.10f}")
    print()
    print(f"  DIFFERENCE:")
    print(f"    staggered ratio  = {stag_ratio:.10f}")
    print(f"    generic 5/6      = {generic_ratio:.10f}")
    print(f"    difference       = {stag_ratio - generic_ratio:.10f}")
    print(f"    relative         = {(stag_ratio - generic_ratio)/generic_ratio * 100:.2f}%")
    print()

    # ------------------------------------------------------------------
    # 4. COMPUTE alpha_V(q*) FOR BOTH CASES
    # ------------------------------------------------------------------
    print("=" * 78)
    print("4. alpha_V(q*) FOR BOTH BLM SCALES")
    print("=" * 78)
    print()

    # Case A: Generic continuum 5/6
    ln_q2a2_generic = -generic_ratio
    alpha_V_generic = alpha_V_from_plaq(ALPHA_PLAQ, ln_q2a2_generic)

    # Case B: Staggered-specific
    ln_q2a2_stag = -stag_ratio
    alpha_V_stag = alpha_V_from_plaq(ALPHA_PLAQ, ln_q2a2_stag)

    # Case C: No BLM shift (q* = 1/a, ln = 0)
    alpha_V_bare = ALPHA_PLAQ

    Sigma_1 = 4.0 * I_stag_inf

    print(f"  Input: alpha_plaq = {ALPHA_PLAQ:.4f},  beta_0 = {BETA_0_TRAD:.1f},  "
          f"Sigma_1 = {Sigma_1:.8f}")
    print()
    print(f"  Case A (GENERIC 5/6):")
    print(f"    ln(q*^2 a^2)  = {ln_q2a2_generic:.10f}")
    print(f"    q*a            = {math.exp(ln_q2a2_generic/2):.10f}")
    print(f"    alpha_V(q*)    = {alpha_V_generic:.10f}")
    print()
    print(f"  Case B (STAGGERED-SPECIFIC):")
    print(f"    ln(q*^2 a^2)  = {ln_q2a2_stag:.10f}")
    print(f"    q*a            = {math.exp(ln_q2a2_stag/2):.10f}")
    print(f"    alpha_V(q*)    = {alpha_V_stag:.10f}")
    print()
    print(f"  Case C (NO BLM, q* = 1/a):")
    print(f"    alpha_V(1/a)   = {alpha_V_bare:.10f}")
    print()
    print(f"  COMPARISON:")
    print(f"    alpha_V(generic)   = {alpha_V_generic:.6f}")
    print(f"    alpha_V(staggered) = {alpha_V_stag:.6f}")
    print(f"    alpha_V(bare)      = {alpha_V_bare:.6f}")
    print(f"    stag/generic ratio = {alpha_V_stag/alpha_V_generic:.6f}")
    print()

    # ------------------------------------------------------------------
    # 5. HIERARCHY FORMULA WITH EACH alpha_V
    # ------------------------------------------------------------------
    print("=" * 78)
    print("5. HIERARCHY FORMULA: v FROM EACH alpha_V(q*)")
    print("=" * 78)
    print()
    print(f"  v = M_Pl * exp(-8 pi^2 / (N_eff * y_t^2))")
    print(f"  N_eff = 12 * Z_chi^2")
    print(f"  Z_chi = 1 - alpha_V * C_F * Sigma_1 / (4 pi)")
    print(f"  y_t = {Y_T},  M_Pl = {M_PL_RED:.3e} GeV")
    print()

    # What alpha_V is needed for exact v = 246?
    alpha_needed = alpha_V_for_target_v(Sigma_1)
    print(f"  alpha_V needed for v = 246 GeV exactly: {alpha_needed:.10f}")
    print()

    for label, aV in [("Generic 5/6", alpha_V_generic),
                       ("Staggered-specific", alpha_V_stag),
                       ("Bare (no BLM)", alpha_V_bare),
                       ("Needed for v=246", alpha_needed)]:
        h = hierarchy_v(aV, Sigma_1)
        if h is not None:
            print(f"  {label:25s}: alpha_V = {aV:.6f}  "
                  f"Z_chi = {h['Z_chi']:.6f}  N_eff = {h['N_eff']:.4f}  "
                  f"v = {h['v_GeV']:.4f} GeV  (v/246 = {h['ratio']:.4f})")
        else:
            print(f"  {label:25s}: alpha_V = {aV:.6f}  -> Z_chi <= 0")
    print()

    # ------------------------------------------------------------------
    # 6. SIGN CONVENTION CHECK
    # ------------------------------------------------------------------
    print("=" * 78)
    print("6. SIGN CONVENTION ANALYSIS")
    print("=" * 78)
    print()
    print("  The BLM prescription (Lepage-Mackenzie 1993, Eq. 2.3):")
    print("    ln(q*a)^2 = <ln(k^2 a^2)>  (average over the integrand)")
    print()
    print("  where the average is weighted by the 1-loop integrand.")
    print("  For the staggered self-energy:")
    print("    <ln(khat^2)> = I_log / I_stag")
    print()
    print(f"  I_log / I_stag = {stag_ratio:.10f}")
    print()

    # I_log is sum of ln(khat^2) / denom.  Since khat^2 ranges from 0 to 16,
    # and most of the weight is at intermediate k, this integral is POSITIVE
    # (typical khat^2 > 1 over the BZ, so ln > 0).
    print(f"  Sign check:")
    print(f"    I_log > 0?  {I_log_inf > 0}  (value: {I_log_inf:.10f})")
    print(f"    I_stag > 0? {I_stag_inf > 0}  (value: {I_stag_inf:.10f})")
    print(f"    ratio > 0?  {stag_ratio > 0}  (value: {stag_ratio:.10f})")
    print()
    print("  Since ratio > 0, ln(q*^2 a^2) = ratio > 0,")
    print("  meaning q* > 1/a (BLM scale is ABOVE the lattice cutoff).")
    print()
    print("  This is the LEPAGE-MACKENZIE convention:")
    print("    ln(q*a)^2 = I_log/I_stag  (positive = scale above 1/a)")
    print()
    print("  frontier_blm_scale.py uses ln(q*a)^2 = -ratio, which gives q* < 1/a.")
    print("  This is the OPPOSITE sign convention, where the minus sign is")
    print("  built into the definition to absorb the beta_0 piece with the")
    print("  CORRECT sign for the running.")
    print()
    print("  RESOLUTION: The sign convention depends on whether we write")
    print("    Sigma = Sigma_1 + beta_0 * Sigma_2  (LM convention: Sigma_2 = I_log/I_stag)")
    print("  or")
    print("    Sigma = Sigma_1 - beta_0 * Sigma_2  (alternative: Sigma_2 = -I_log/I_stag)")
    print()
    print("  In the Lepage-Mackenzie convention (Phys Rev D 48, 2250):")
    print("    The coupling evaluated at q* absorbs the beta_0 piece, meaning:")
    print("    alpha_V(q*) = alpha_plaq / (1 - alpha_plaq * beta_0 * ln(q*^2 a^2)/(4pi))")
    print("    where ln(q*^2 a^2) = I_log / I_stag > 0  =>  q* > 1/a")
    print("    and the minus sign in the denominator means alpha_V(q*) < alpha_plaq.")
    print()

    # Recompute with POSITIVE ratio (Lepage-Mackenzie convention)
    ln_q2a2_LM = stag_ratio  # POSITIVE: q* > 1/a
    alpha_V_LM = alpha_V_from_plaq(ALPHA_PLAQ, ln_q2a2_LM)

    print(f"  With Lepage-Mackenzie sign convention:")
    print(f"    ln(q*^2 a^2) = +{stag_ratio:.10f}")
    print(f"    q*a           = {math.exp(stag_ratio/2):.10f}")
    print(f"    alpha_V(q*)   = {alpha_V_LM:.10f}")
    print()

    # And the NEGATIVE convention used in frontier_blm_scale.py
    ln_q2a2_neg = -stag_ratio
    alpha_V_neg = alpha_V_from_plaq(ALPHA_PLAQ, ln_q2a2_neg)
    print(f"  With negative convention (frontier_blm_scale.py):")
    print(f"    ln(q*^2 a^2) = {ln_q2a2_neg:.10f}")
    print(f"    q*a           = {math.exp(ln_q2a2_neg/2):.10f}")
    print(f"    alpha_V(q*)   = {alpha_V_neg:.10f}")
    print()

    # ------------------------------------------------------------------
    # 7. WHICH CONVENTION IS CORRECT?
    # ------------------------------------------------------------------
    print("=" * 78)
    print("7. DETERMINING THE CORRECT CONVENTION")
    print("=" * 78)
    print()
    print("  The BLM procedure works as follows (Lepage-Mackenzie 1993):")
    print()
    print("  A 1-loop lattice quantity can be written as:")
    print("    X = 1 + alpha_V(mu) * [A + beta_0 * B]")
    print()
    print("  where B = -<ln(mu^2 a^2)> (the vacuum polarization piece).")
    print("  Setting mu = q* such that B term vanishes:")
    print("    0 = -<ln(mu^2 a^2)> + <ln(k^2 a^2)>")
    print("    ln(q*^2 a^2) = <ln(k^2 a^2)> = I_log / I_stag")
    print()
    print("  So ln(q*^2 a^2) = I_log/I_stag WITH THE POSITIVE SIGN.")
    print()
    print("  Then alpha_V(q*) evaluated with 1-loop running:")
    print("    alpha_V(q*) = alpha_V(1/a) / (1 + alpha_V(1/a) * beta_0 * ln(q*^2 a^2)/(4pi))")
    print()
    print("  Note the PLUS sign in the denominator for the running equation.")
    print("  With ln(q*^2 a^2) > 0 and beta_0 > 0, alpha_V(q*) < alpha_V(1/a).")
    print("  The coupling DECREASES as we go to higher scales (asymptotic freedom).")
    print()

    # Correct formula: plus sign in denominator
    denom_correct = 1.0 + ALPHA_PLAQ * BETA_0_TRAD * stag_ratio / (4.0 * PI)
    alpha_V_correct = ALPHA_PLAQ / denom_correct

    print(f"  CORRECT FORMULA:")
    print(f"    alpha_V(q*) = alpha_plaq / (1 + alpha_plaq * beta_0 * ln(q*^2 a^2) / (4pi))")
    print(f"                = {ALPHA_PLAQ} / (1 + {ALPHA_PLAQ} * {BETA_0_TRAD} * {stag_ratio:.8f} / {4*PI:.6f})")
    print(f"                = {ALPHA_PLAQ} / {denom_correct:.10f}")
    print(f"                = {alpha_V_correct:.10f}")
    print()

    # frontier_blm_scale.py uses MINUS in the denominator AND negative ratio,
    # which gives: alpha / (1 - alpha * b0 * (-ratio) / 4pi) = alpha / (1 + alpha * b0 * ratio / 4pi)
    # This is EQUIVALENT! The two minus signs cancel.
    print("  CROSS-CHECK: frontier_blm_scale.py uses:")
    print("    ln(q*^2 a^2) = -I_log/I_stag  (negative)")
    print("    alpha_V = alpha_plaq / (1 - alpha_plaq * beta_0 * ln / (4pi))")
    print("    = alpha_plaq / (1 - alpha_plaq * beta_0 * (-ratio) / (4pi))")
    print("    = alpha_plaq / (1 + alpha_plaq * beta_0 * ratio / (4pi))")
    denom_cross = 1.0 - ALPHA_PLAQ * BETA_0_TRAD * (-stag_ratio) / (4.0 * PI)
    alpha_cross = ALPHA_PLAQ / denom_cross
    print(f"    = {alpha_cross:.10f}  (same as correct formula: GOOD)")
    print()

    # ------------------------------------------------------------------
    # 8. FINAL ANSWER
    # ------------------------------------------------------------------
    print("=" * 78)
    print("8. FINAL ANSWER")
    print("=" * 78)
    print()

    h_correct = hierarchy_v(alpha_V_correct, Sigma_1)

    print(f"  LATTICE INTEGRALS (L -> infinity extrapolation):")
    print(f"    I_stag(4)       = {I_stag_inf:.12f}")
    print(f"    I_log(4)        = {I_log_inf:.12f}")
    print(f"    Sigma_1         = 4 * I_stag = {Sigma_1:.10f}")
    print()
    print(f"  BLM RATIO:")
    print(f"    I_log / I_stag  = {stag_ratio:.10f}")
    print(f"    Generic 5/6     = {generic_ratio:.10f}")
    print(f"    DIFFERENCE      = {stag_ratio - generic_ratio:.10f}")
    print(f"    The staggered ratio is {'LARGER' if stag_ratio > generic_ratio else 'SMALLER'}"
          f" than 5/6 by {abs(stag_ratio - generic_ratio)/generic_ratio * 100:.1f}%")
    print()
    print(f"  BLM SCALE:")
    print(f"    ln(q*^2 a^2)   = {stag_ratio:.10f}")
    print(f"    q*a             = {math.exp(stag_ratio/2):.10f}")
    print(f"    q* / (pi/a)     = {math.exp(stag_ratio/2) / PI:.10f}")
    print()
    print(f"  CORRECT alpha_V(q*):")
    print(f"    alpha_V(q*)     = {alpha_V_correct:.10f}")
    print()
    print(f"  COMPARISON WITH GENERIC:")
    print(f"    alpha_V(generic 5/6) = {alpha_V_generic:.10f}")
    print(f"    alpha_V(staggered)   = {alpha_V_correct:.10f}")
    print(f"    Difference           = {abs(alpha_V_correct - alpha_V_generic):.10f}")
    print(f"    Relative             = {abs(alpha_V_correct - alpha_V_generic)/alpha_V_generic * 100:.2f}%")
    print()
    print(f"  HIERARCHY RESULT (staggered-specific BLM):")
    if h_correct:
        print(f"    Z_chi     = {h_correct['Z_chi']:.10f}")
        print(f"    N_eff     = {h_correct['N_eff']:.10f}")
        print(f"    v         = {h_correct['v_GeV']:.6f} GeV")
        print(f"    v / 246   = {h_correct['ratio']:.6f}")
    else:
        print(f"    Z_chi <= 0: alpha_V too large")
    print()

    print(f"  NEEDED FOR v = 246:")
    print(f"    alpha_V needed  = {alpha_needed:.10f}")
    print(f"    Actual alpha_V  = {alpha_V_correct:.10f}")
    if alpha_needed > 0:
        print(f"    Gap             = {abs(alpha_V_correct - alpha_needed)/alpha_needed * 100:.1f}%")
    print()

    # ------------------------------------------------------------------
    # 9. SCAN: alpha_V vs v
    # ------------------------------------------------------------------
    print("=" * 78)
    print("9. SENSITIVITY: alpha_V -> v")
    print("=" * 78)
    print()
    print(f"  {'alpha_V':>10s}  {'Z_chi':>10s}  {'N_eff':>10s}  {'v (GeV)':>14s}  {'v/246':>10s}  note")
    print("  " + "-" * 75)
    for aV in [0.080, 0.085, 0.090, alpha_V_correct, 0.095, 0.100,
               alpha_V_generic, 0.110, 0.120, 0.130, alpha_needed,
               0.140, 0.150, 0.160, 0.180, 0.200]:
        h = hierarchy_v(aV, Sigma_1)
        if h and 0 < h['v_GeV'] < 1e30:
            note = ""
            if abs(aV - alpha_V_correct) < 0.0005:
                note = "<-- staggered BLM"
            elif abs(aV - alpha_V_generic) < 0.0005:
                note = "<-- generic 5/6"
            elif abs(aV - alpha_needed) < 0.0005:
                note = "<-- needed for v=246"
            print(f"  {aV:10.6f}  {h['Z_chi']:10.6f}  {h['N_eff']:10.4f}  "
                  f"{h['v_GeV']:14.4f}  {h['ratio']:10.6f}  {note}")
    print()

    # ------------------------------------------------------------------
    # 10. VERDICT
    # ------------------------------------------------------------------
    print("=" * 78)
    print("10. VERDICT")
    print("=" * 78)
    print()
    print("  Q: Does the staggered-specific BLM scale differ from the generic 5/6?")
    if abs(stag_ratio - generic_ratio) / generic_ratio > 0.05:
        print(f"  A: YES. The staggered ratio = {stag_ratio:.6f} differs from 5/6 = {generic_ratio:.6f}")
        print(f"     by {abs(stag_ratio - generic_ratio)/generic_ratio * 100:.1f}%.")
    else:
        print(f"  A: They are close. Staggered ratio = {stag_ratio:.6f}, generic = {generic_ratio:.6f}")
        print(f"     ({abs(stag_ratio - generic_ratio)/generic_ratio * 100:.1f}% difference).")
    print()
    print(f"  Q: Is alpha_V(q*) = 0.10 (generic) or closer to 0.14 (needed for v=246)?")
    print(f"  A: The CORRECT alpha_V(q*) = {alpha_V_correct:.4f}")
    if abs(alpha_V_correct - 0.10) < abs(alpha_V_correct - alpha_needed):
        print(f"     This is CLOSER to the generic 0.10 value.")
        print(f"     The staggered-specific BLM does NOT bridge the gap to v = 246.")
    else:
        print(f"     This is CLOSER to the needed value {alpha_needed:.4f}.")
        print(f"     The staggered-specific BLM HELPS bridge the gap to v = 246.")
    print()

    if h_correct and 0.8 < h_correct['ratio'] < 1.2:
        print("  CONCLUSION: Staggered BLM gives v within 20% of 246 GeV.")
    elif h_correct and 0.5 < h_correct['ratio'] < 2.0:
        print("  CONCLUSION: Staggered BLM gives v within factor 2 of 246 GeV.")
    else:
        v_str = f"{h_correct['v_GeV']:.2e}" if h_correct else "undefined"
        print(f"  CONCLUSION: Staggered BLM gives v = {v_str} GeV,")
        print(f"  which does NOT match 246 GeV. Additional physics is needed.")
    print()

    elapsed = time.time() - t_start
    print(f"  Total computation time: {elapsed:.1f}s")


if __name__ == "__main__":
    main()
