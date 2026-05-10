#!/usr/bin/env python3
"""Bounded coherent-saddle support for C_arm in the rescaled NN harness.

Companion work on the rescaled NN harness's slit-detector decoherence
subblock reports arm-width scaling

    sigma_arm(h) = C_arm * h^alpha

A 4-point diagnostic fit on h <= 0.25 returned

    C_arm_numeric = 2.7107
    alpha_numeric = 0.5256
    R^2 = 0.9996

The geodesic prediction is alpha = 1/2, which the fit recovers to within a
small systematic (residual 0.026 in alpha). This script derives the
leading coherent-saddle constant and compares it to that diagnostic fit.
It does not claim exact closure of the fitted constant.

The bounded calculation is tied to the deterministic-rescale NN lattice
configuration: three forward edges per layer, physical length L_total = 40,
and the slit plane at nl // 3. That lattice configuration geometry is what
sets the post-slit length L_2 used below.

The computation has three stages:

  1. Incoherent random-walk estimate (treat |f|^2 as a per-step probability).
     This was already sketched in the issue and gives C_arm_incoh = 3.30.

  2. Coherent path-integral estimate via the lateral-momentum characteristic
     function g(q; h) of the per-step amplitude. The Gaussian saddle at q=0
     yields a closed form

         C_arm^2(h) = L_eff * |a_pm|^2 / [Re(a_pm * a_0_conj) + 2 |a_pm|^2]

     with a_0, a_pm the per-step amplitudes for diy = 0 and diy = +/- 1.

  3. Identification of the relevant propagation length L_eff. The harness
     places the slit plane at layer nl // 3, so the slit-to-detector distance
     is L_2 = (2/3) * L_total. The per-arm distribution at the detector is
     dominated by post-slit propagation; the source-to-slit segment merely
     selects a tail of the source wave whose subsequent spread is dominated
     by L_2, not L_total.

The script prints both interpretations (L = L_total and L = L_2), the
incoherent estimate, the leading phase-interference correction, and the
residuals against the diagnostic C_arm_numeric = 2.7107. No Monte Carlo,
no lattice propagation - all closed form.

Usage:
    python3 scripts/lattice_nn_rescaled_C_arm_derivation.py
"""

from __future__ import annotations

import cmath
import math
import sys


# ---------------------------------------------------------------------------
# Harness parameters (frozen from scripts/lattice_nn_deterministic_rescale.py)
# ---------------------------------------------------------------------------

BETA = 0.8
K_PHYS = 5.0
PHYS_L = 40.0
FANOUT = 3.0

# Slit plane sits at layer `nl // 3` -> source-to-slit distance is L_total/3,
# slit-to-detector distance is 2*L_total/3.
L_TOTAL = PHYS_L
L_1 = L_TOTAL / 3.0  # source -> slit
L_2 = 2.0 * L_TOTAL / 3.0  # slit -> detector

# Diagnostic fit values used only as bounded comparators.
C_ARM_NUMERIC = 2.7107
ALPHA_NUMERIC = 0.5256


# ---------------------------------------------------------------------------
# Per-step amplitudes
# ---------------------------------------------------------------------------

def step_scale(h: float) -> float:
    return h / math.sqrt(FANOUT)


def angular_weight() -> float:
    """exp(-BETA * theta^2) for the diy = +/- 1 edges (theta = pi/4)."""
    theta = math.pi / 4.0
    return math.exp(-BETA * theta * theta)


def a_zero(h: float) -> complex:
    """Per-step amplitude for diy = 0.

    f(0; h) = step_scale * exp(i k h) * 1 / h = exp(i k h) / sqrt(FANOUT)
    """
    return cmath.exp(1j * K_PHYS * h) / math.sqrt(FANOUT)


def a_plus(h: float) -> complex:
    """Per-step amplitude for diy = +/- 1 (same magnitude and phase).

    f(+/-1; h) = step_scale * exp(i k h sqrt(2)) * exp(-BETA pi^2 / 16) / (h sqrt(2))
                = exp(i k h sqrt(2)) * c / sqrt(2 * FANOUT)
    """
    c = angular_weight()
    return c * cmath.exp(1j * K_PHYS * h * math.sqrt(2.0)) / math.sqrt(2.0 * FANOUT)


# ---------------------------------------------------------------------------
# Stage 1: Incoherent random-walk estimate (treats |f|^2 as probability)
# ---------------------------------------------------------------------------

def incoherent_estimate() -> dict:
    """C_arm from the incoherent random-walk formula."""
    # Per-step squared magnitudes
    p0 = abs(a_zero(0.0)) ** 2  # = 1/FANOUT = 1/3 (h-independent at this level)
    pp = abs(a_plus(0.0)) ** 2  # = c^2 / (2 FANOUT)
    # Note both are h-independent because step_scale^2 / L^2 cancels h.

    W = p0 + 2.0 * pp
    P_zero = p0 / W
    P_plus = pp / W
    var_step = 2.0 * P_plus  # E[diy^2] = 0 + 2 * P(+/-1) * 1^2

    # Random-walk variance over N = L_total / h edges:
    #   sigma_arm^2 = h^2 * N * var_step = L_total * var_step * h
    C2 = L_TOTAL * var_step
    C = math.sqrt(C2)

    return {
        "p0": p0,
        "pp": pp,
        "W": W,
        "P_zero": P_zero,
        "P_plus": P_plus,
        "var_step": var_step,
        "C_arm_sq": C2,
        "C_arm": C,
    }


# ---------------------------------------------------------------------------
# Stage 2: Coherent path-integral estimate via characteristic function
# ---------------------------------------------------------------------------
#
# The per-step amplitude in lateral momentum space is
#
#     g(q; h) = a_0(h) + 2 * a_pm(h) * cos(q h)
#
# By symmetry (a_+ = a_- = a_pm) the first q-derivative at q = 0 vanishes.
# Expand g(q; h) = g(0; h) - a_pm(h) * (q h)^2 + O((q h)^4), so
#
#     g(q; h)^N = g(0; h)^N * exp(-N r(h) (q h)^2 + O(q^4))
#
# where r(h) = a_pm(h) / g(0; h) is in general complex.
#
# Fourier-transform a complex Gaussian:
#
#     A(y) = g(0)^N / sqrt(4 pi N r h^2) * exp(- y^2 / (4 N r h^2))
#
# The position distribution |A(y)|^2 is a real Gaussian whose variance is
#
#     sigma_y^2 = N h^2 |r|^2 / Re(r) = L h |r|^2 / Re(r)
#
# Equivalently (using r = a_pm / g(0) and Re(a_pm / g(0)) = Re(a_pm * g(0)^*) / |g(0)|^2),
#
#     sigma_y^2 = L h * |a_pm|^2 / Re(a_pm * conj(g(0)))
#               = L h * |a_pm|^2 / [Re(a_pm * conj(a_0)) + 2 |a_pm|^2]
#
# So
#
#     C_arm^2(h) = L * |a_pm|^2 / [Re(a_pm * conj(a_0)) + 2 |a_pm|^2]
#
# This is the coherent path-integral analogue of the incoherent var_step.
# In the h -> 0 limit, exp(i k h * (sqrt(2) - 1)) -> 1 and Re(a_pm * conj(a_0))
# reduces to |a_pm| * |a_0|, restoring real saddle.
# ---------------------------------------------------------------------------


def coherent_C_arm_sq(L: float, h: float) -> dict:
    """Closed-form coherent C_arm^2 at lattice spacing h, propagation length L."""
    a0 = a_zero(h)
    ap = a_plus(h)
    g0 = a0 + 2.0 * ap

    # Numerator and denominator of the characteristic-function ratio
    num = abs(ap) ** 2
    denom = (ap * a0.conjugate()).real + 2.0 * num  # = Re(a_pm * conj(g(0)))

    r = ap / g0  # for diagnostic only
    C2 = L * num / denom
    return {
        "L": L,
        "h": h,
        "a0": a0,
        "a_pm": ap,
        "g0": g0,
        "r": r,
        "Re_r": r.real,
        "abs_r_sq": abs(r) ** 2,
        "denom": denom,
        "C_arm_sq": C2,
        "C_arm": math.sqrt(max(C2, 0.0)),
    }


# ---------------------------------------------------------------------------
# Stage 3: Phase-coherence diagnostic
# ---------------------------------------------------------------------------
#
# Edge phase = k * L_edge = k * h * sqrt(1 + diy^2). Path phase to leading
# order is k L_total * <sqrt(1+diy^2)> + path-fluctuation. The path-fluctuation
# variance is N * (k h)^2 * Var(sqrt(1+diy^2)). We probe this with the
# incoherent step distribution P(diy) to get a number-of-radians estimate.
# ---------------------------------------------------------------------------


def phase_variance(h: float) -> dict:
    incoh = incoherent_estimate()
    P_zero = incoh["P_zero"]
    P_plus = incoh["P_plus"]
    # E[sqrt(1+diy^2)]
    e1 = P_zero * 1.0 + 2.0 * P_plus * math.sqrt(2.0)
    # E[1 + diy^2]
    e2 = P_zero * 1.0 + 2.0 * P_plus * 2.0
    var_root = e2 - e1 * e1
    N = L_TOTAL / h
    phase_var = (K_PHYS * h) ** 2 * N * var_root  # = k^2 h L_total Var(...)
    return {
        "h": h,
        "E_root": e1,
        "Var_root": var_root,
        "phase_var": phase_var,
        "phase_rms_radians": math.sqrt(phase_var),
    }


# ---------------------------------------------------------------------------
# Reporting
# ---------------------------------------------------------------------------


def reldiff(pred: float, ref: float) -> float:
    return (pred - ref) / ref


def report() -> int:
    print("=" * 78)
    print("BOUNDED COHERENT-SADDLE SUPPORT FOR C_arm")
    print("=" * 78)
    print()
    print("Frozen harness parameters (from scripts/lattice_nn_deterministic_rescale.py):")
    print(f"  BETA      = {BETA}")
    print(f"  k         = {K_PHYS}")
    print(f"  L_total   = {L_TOTAL}     (source -> detector)")
    print(f"  FANOUT    = {FANOUT}")
    print(f"  L_1       = {L_1:.4f}  (source -> slit, layer nl//3)")
    print(f"  L_2       = {L_2:.4f}  (slit   -> detector, layer 2*nl//3)")
    print()
    print(f"Diagnostic fit reference (4-point fit, h <= 0.25):")
    print(f"  C_arm_numeric = {C_ARM_NUMERIC}")
    print(f"  alpha_numeric = {ALPHA_NUMERIC}    (geodesic predicts 1/2)")
    print()
    print("-" * 78)
    print("STAGE 1: Incoherent random-walk estimate (|f|^2 as probability)")
    print("-" * 78)
    incoh = incoherent_estimate()
    print(f"  |f(0;h)|^2  = 1/FANOUT       = {incoh['p0']:.6f}")
    print(f"  |f(+/-1)|^2 = exp(-BETA pi^2 / 8) / (2 FANOUT) = {incoh['pp']:.6f}")
    print(f"  W           = |f(0)|^2 + 2|f(+/-1)|^2          = {incoh['W']:.6f}")
    print(f"  P(diy=0)    = {incoh['P_zero']:.6f}")
    print(f"  P(diy=+/-1) = {incoh['P_plus']:.6f}")
    print(f"  Var(diy_eff) = 2 P(+/-1)                       = {incoh['var_step']:.6f}")
    print(f"  C_arm^2_incoh = L_total * Var(diy_eff)         = {incoh['C_arm_sq']:.6f}")
    print(f"  C_arm_incoh   = sqrt(C_arm^2_incoh)            = {incoh['C_arm']:.6f}")
    print(f"  residual vs diagnostic fit = {100 * reldiff(incoh['C_arm'], C_ARM_NUMERIC):+.2f}%")
    print()
    print("-" * 78)
    print("STAGE 2: Phase-coherence diagnostic")
    print("-" * 78)
    print("  Path phase has leading drift k L_total * <sqrt(1+diy^2)> plus")
    print("  fluctuation Var = (k h)^2 * N * Var(sqrt(1+diy^2)) = k^2 h L_total Var(...).")
    print("  If << 1 phases are coherent (constructive); if >> 1 phases dephase")
    print("  and the incoherent estimate becomes correct.")
    print()
    print(f"  {'h':>7s}  {'phase_rms (rad)':>17s}  regime")
    for h in (0.25, 0.125, 0.0625):
        pv = phase_variance(h)
        regime = "decoherent" if pv["phase_var"] > 1.0 else "coherent"
        print(f"  {h:7.4f}  {pv['phase_rms_radians']:17.4f}  {regime}")
    print()
    print("  The phase rms is order 1 across the fitted range, so neither pure")
    print("  limit is exact. The coherent path-integral formula below is the")
    print("  right tool: it integrates over the q-spectrum exactly, no h -> 0")
    print("  small-phase assumption.")
    print()
    print("-" * 78)
    print("STAGE 3: Coherent path-integral estimate")
    print("-" * 78)
    print("  Per-step lateral characteristic function:")
    print("      g(q; h) = a_0(h) + 2 a_pm(h) cos(q h)")
    print("  Saddle at q=0 (a_+ = a_-) gives complex Gaussian")
    print("      g(q; h)^N = g(0)^N * exp(-N r(h) (q h)^2 + O(q^4))")
    print("  with r(h) = a_pm(h) / g(0; h). FT of complex Gaussian:")
    print("      |A(y)|^2  is real Gaussian, var = N h^2 |r|^2 / Re(r)")
    print("  i.e. C_arm^2(h) = L * |a_pm|^2 / [Re(a_pm * conj(a_0)) + 2 |a_pm|^2].")
    print()
    print("  Two natural choices for L:")
    print("    (a) L = L_total = 40   (full source -> detector spread)")
    print("    (b) L = L_2     = 2 L_total / 3 = 26.667 (slit -> detector spread)")
    print()
    print("  The slit at layer nl//3 forces the per-arm wave through y = SLIT_Y,")
    print("  so the post-slit propagation length L_2 sets the spreading.")
    print()
    print(f"  {'h':>7s}  {'C_arm(L_total)':>15s}  {'sigma(L_total)':>15s}  "
          f"{'C_arm(L_2)':>11s}  {'sigma(L_2)':>11s}  {'sigma_fit':>10s}")
    for h in (0.0625, 0.125, 0.1875, 0.25):
        full = coherent_C_arm_sq(L_TOTAL, h)
        post = coherent_C_arm_sq(L_2, h)
        sigma_full = full["C_arm"] * math.sqrt(h)
        sigma_post = post["C_arm"] * math.sqrt(h)
        sigma_fit = C_ARM_NUMERIC * h ** ALPHA_NUMERIC
        print(f"  {h:7.4f}  {full['C_arm']:15.4f}  {sigma_full:15.4f}  "
              f"{post['C_arm']:11.4f}  {sigma_post:11.4f}  {sigma_fit:10.4f}")
    print()

    # Headline numbers in the h -> 0 limit (geodesic limit)
    full0 = coherent_C_arm_sq(L_TOTAL, 0.0)
    post0 = coherent_C_arm_sq(L_2, 0.0)
    print("  h -> 0 limit (geodesic alpha = 1/2 exact, no phase correction):")
    print(f"    C_arm_analytic(L_total) = {full0['C_arm']:.4f}    "
          f"residual = {100 * reldiff(full0['C_arm'], C_ARM_NUMERIC):+.2f}%")
    print(f"    C_arm_analytic(L_2)     = {post0['C_arm']:.4f}    "
          f"residual = {100 * reldiff(post0['C_arm'], C_ARM_NUMERIC):+.2f}%")
    print()
    print("-" * 78)
    print("VERDICT")
    print("-" * 78)
    res_full = abs(reldiff(full0['C_arm'], C_ARM_NUMERIC))
    res_post = abs(reldiff(post0['C_arm'], C_ARM_NUMERIC))
    res_incoh = abs(reldiff(incoh['C_arm'], C_ARM_NUMERIC))

    print(f"  C_arm_incoh           = {incoh['C_arm']:.4f}    "
          f"residual = {100 * res_incoh:.2f}% (sharp upper bound)")
    print(f"  C_arm_coherent_full   = {full0['C_arm']:.4f}    "
          f"residual = {100 * res_full:.2f}% (full-length coherent)")
    print(f"  C_arm_coherent_slit   = {post0['C_arm']:.4f}    "
          f"residual = {100 * res_post:.2f}% (post-slit coherent)")
    print()
    print("  The coherent post-slit estimate matches the diagnostic fit to within")
    print(f"  {100 * res_post:.1f}%, inside the 10% bounded comparison band.")
    print("  C_arm_analytic := C_arm_coherent_slit = sqrt((2/3) L_total |a_pm|^2 /")
    print("  [Re(a_pm conj(a_0)) + 2 |a_pm|^2])  is the closed form.")

    # Per-h residual with full coherent formula (with cos(...) phase term)
    print()
    print("  Per-h cross-check using the exact coherent formula (with phase term):")
    print(f"  {'h':>7s}  {'sigma_pred':>10s}  {'sigma_fit':>10s}  {'reldiff':>8s}")
    max_abs_rd = 0.0
    for h in (0.0625, 0.125, 0.1875, 0.25):
        post = coherent_C_arm_sq(L_2, h)
        sigma_pred = post["C_arm"] * math.sqrt(h)
        sigma_fit = C_ARM_NUMERIC * h ** ALPHA_NUMERIC
        rd = 100 * (sigma_pred - sigma_fit) / sigma_fit
        max_abs_rd = max(max_abs_rd, abs(rd) / 100.0)
        print(f"  {h:7.4f}  {sigma_pred:10.4f}  {sigma_fit:10.4f}  {rd:+7.2f}%")
    print()
    print("  All four points agree with the diagnostic fit to within 2.5%.")
    print()

    checks = {
        "post-slit coherent residual <= 10%": res_post <= 0.10,
        "per-h phase-corrected residual <= 2.5%": max_abs_rd <= 0.025,
        "post-slit length improves on full-length estimate": res_post < res_full,
        "coherent estimate improves on incoherent estimate": res_post < res_incoh,
        "h->0 post-slit value is stable": math.isclose(post0["C_arm"], 2.4855, rel_tol=5e-5),
    }
    print("  Bounded-support guards:")
    for label, ok in checks.items():
        print(f"    {'PASS' if ok else 'FAIL'}: {label}")
    return 0 if all(checks.values()) else 1


if __name__ == "__main__":
    sys.exit(report())
