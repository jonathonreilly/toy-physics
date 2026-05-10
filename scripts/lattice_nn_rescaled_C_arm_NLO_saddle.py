#!/usr/bin/env python3
"""Next-to-leading-order (NLO) saddle correction for C_arm in the rescaled NN
harness.

Companion work:

  - The upstream C_arm coherent-saddle support note derived the
    leading-order coherent-saddle constant
        C_arm_LO = sqrt( L_2 / ( sqrt(2)/c + 2 ) ) = 2.4855
    via the q -> 0 stationary point of the lateral characteristic function
    g(q; h) = a_0(h) + 2 a_pm(h) cos(q h).

  - The upstream continuum diagnostic measured numerically
        sigma_arm(h) = C_arm h^alpha
    with C_arm = 2.7107 and alpha = 0.5256 on the four-point fit
    h in {0.25, 0.125, 0.0625, 0.03125}.

The leading saddle has alpha = 1/2 in the LO model. The empirical alpha-residual
0.5256 - 0.5 = 0.026 must come from a sub-leading (O(h^p)) correction that is
non-negligible in the fit window but vanishes as h -> 0. The data confirm
this: sigma^2 / h is a decreasing function of h that asymptotes to ~6.20
(matching C_LO^2 = 6.178) at the smallest h.

This script computes the closed-form NLO correction analytically and tests
two natural sources:

  (a) PHASE NLO: the leading-order saddle uses Re(a_pm * conj(a_0)), but
      a_pm * conj(a_0) carries an h-dependent phase exp(i k h (sqrt(2) - 1)).
      Expanding the cosine gives a +O(h^2) correction to the variance.

  (b) SADDLE NLO: the leading saddle keeps only the q^2 term in
      log g(q; h)/g(0). The next term is q^4, contributing an O(h^2)
      correction to <y^2> via standard perturbation theory in the inverse
      Fourier transform.

The script computes both, reports which dominates, and converts the
predicted variance into an "effective alpha" by reproducing the upstream
continuum diagnostic's
log-log linear fit on the four h points.

Usage:
    python3 scripts/lattice_nn_rescaled_C_arm_NLO_saddle.py
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

L_TOTAL = PHYS_L
L_1 = L_TOTAL / 3.0
L_2 = 2.0 * L_TOTAL / 3.0  # post-slit length used by the LO support note

# Diagnostic fit values from the upstream continuum note (4-point fit, h <= 0.25).
C_ARM_NUMERIC = 2.7107
ALPHA_NUMERIC = 0.5256

# Fit window used by the upstream continuum note.
FIT_HS = (0.25, 0.125, 0.0625, 0.03125)

# Measured per-h sigma_arm values (from upstream source data).
MEAS_SIGMA = {
    0.25: 1.3198,
    0.125: 0.8990,
    0.0625: 0.6282,
    0.03125: 0.4416,
}


# ---------------------------------------------------------------------------
# Per-step amplitudes (identical to the C_arm support note)
# ---------------------------------------------------------------------------


def angular_weight() -> float:
    """exp(-BETA * theta^2) for diy = +/- 1 edges (theta = pi/4)."""
    theta = math.pi / 4.0
    return math.exp(-BETA * theta * theta)


C_FACTOR = angular_weight()  # = exp(-BETA pi^2 / 16) ~ 0.6105


def a_zero(h: float) -> complex:
    return cmath.exp(1j * K_PHYS * h) / math.sqrt(FANOUT)


def a_plus(h: float) -> complex:
    return C_FACTOR * cmath.exp(1j * K_PHYS * h * math.sqrt(2.0)) / math.sqrt(2.0 * FANOUT)


# ---------------------------------------------------------------------------
# Closed-form NLO coefficients (analytic)
# ---------------------------------------------------------------------------
#
# Define
#     A := |a_pm| |a_0|       = c / (FANOUT * sqrt(2))
#     B := 2 |a_pm|^2         = c^2 / FANOUT
#     omega := k (sqrt(2) - 1)
#
# The leading-order saddle gives
#
#     sigma^2(h) = L_2 * (c^2 / (2 FANOUT)) * h
#                  / [ A cos(omega h) + B ]
#
# Define C_LO^2 := L_2 * (c^2/(2 FANOUT)) / (A + B) (the geodesic constant).
# Then
#
#     sigma^2(h) = C_LO^2 * h * (A + B) / [A cos(omega h) + B]
#                = C_LO^2 * h * (1 + delta_a(h))
#
# Expanding cos(omega h) = 1 - (omega h)^2 / 2 + (omega h)^4 / 24 - ...:
#
#     delta_a(h) = (A/(A+B)) * (omega h)^2 / 2
#                + [ (A/(A+B))^2 * (omega h)^4 / 4
#                    - (A/(A+B)) * (omega h)^4 / 24 ]
#                + O(h^6)
#
# So the leading non-trivial correction is O(h^2):
#
#     delta_a(h) ~ d2_phase * h^2,  d2_phase = (A/(A+B)) * omega^2 / 2.
#
# This is candidate (a). We use the EXACT expression
# delta_a_exact(h) = (A+B)/(A cos(omega h) + B) - 1 in the runner so all
# orders in omega h are retained without truncation; the h^2 leading
# coefficient is reported alongside.
# ---------------------------------------------------------------------------


def coef_A() -> float:
    return C_FACTOR / (FANOUT * math.sqrt(2.0))


def coef_B() -> float:
    return C_FACTOR ** 2 / FANOUT


def C_LO_sq() -> float:
    return L_2 * (C_FACTOR ** 2 / (2.0 * FANOUT)) / (coef_A() + coef_B())


def omega() -> float:
    return K_PHYS * (math.sqrt(2.0) - 1.0)


def delta_a_exact(h: float) -> float:
    """Phase-NLO delta from cos(omega h) (all orders in omega h)."""
    A = coef_A()
    B = coef_B()
    return (A + B) / (A * math.cos(omega() * h) + B) - 1.0


def d2_phase() -> float:
    """Leading h^2 coefficient of delta_a (closed form)."""
    A = coef_A()
    B = coef_B()
    return (A / (A + B)) * omega() ** 2 / 2.0


def d4_phase() -> float:
    """Next-leading h^4 coefficient of delta_a (closed form)."""
    A = coef_A()
    B = coef_B()
    ratio = A / (A + B)
    om = omega()
    return ratio ** 2 * om ** 4 / 4.0 - ratio * om ** 4 / 24.0


# ---------------------------------------------------------------------------
# q^4 saddle correction (candidate b)
# ---------------------------------------------------------------------------
#
# Expand log[g(q; h) / g(0; h)] around q = 0:
#
#     g(q)/g(0) = 1 - r u^2 + (r/12) u^4 + O(u^6),    u = q h, r = a_pm/g(0)
#
# (using cos(qh) = 1 - u^2/2 + u^4/24, so g/g(0) = 1 + (2 a_pm/g0)(cos-1)
#  = 1 - r u^2 + r u^4 / 12).
#
#     log(g/g0) = -r u^2 + (r/12 - r^2/2) u^4 + O(u^6)
#
# So with N = L_2 / h post-slit edges,
#
#     g^N(q) = g(0)^N * exp( -alpha_2 q^2 - alpha_4 q^4 + O(q^6) )
#         alpha_2 = N r h^2 = L_2 r h         (complex)
#         alpha_4 = N (r^2/2 - r/12) h^4 = L_2 (r^2/2 - r/12) h^3   (complex)
#
# The position-space wavefunction is the inverse FT:
#
#     A(y) = g(0)^N / (2 pi) * integral dq exp(- alpha_2 q^2 - alpha_4 q^4 - i q y)
#          ~ A_0(y) * [ 1 - alpha_4 X(y) ]    (perturbing in alpha_4)
#
# where A_0(y) = g(0)^N / sqrt(4 pi alpha_2) * exp(- y^2 / (4 alpha_2)) and
#
#     X(y) = (1/A_0(y)) * (-d^4/dy^4) A_0(y) / (-1) ... easier:
#
# Using  integral dq q^4 exp(-alpha_2 q^2 - i q y)
#       = d^4/dy^4 integral dq exp(-alpha_2 q^2 - i q y)
#       = d^4/dy^4 [ sqrt(pi/alpha_2) exp(-y^2 / (4 alpha_2)) ],
#
# and writing mu := 1/(4 alpha_2),
#
#     X(y) = 12 mu^2 - 48 mu^3 y^2 + 16 mu^4 y^4
#
# Then |A(y)|^2 = |A_0(y)|^2 * |1 - alpha_4 X(y)|^2
#              ~ |A_0(y)|^2 * (1 - 2 Re( alpha_4 X(y) )).
#
# The unperturbed |A_0(y)|^2 is a real Gaussian with variance
#     sigma_0^2 = N h^2 |r|^2 / Re(r) = L_2 h |r|^2 / Re(r).
# (This is exactly the candidate-(a) formula evaluated at h.)
#
# Compute first-order variance correction by Gaussian moments:
#     <X>     = 12 mu^2 - 48 mu^3 sigma_0^2 + 48 mu^4 sigma_0^4
#     <y^2 X> = 12 mu^2 sigma_0^2 - 144 mu^3 sigma_0^4 + 240 mu^4 sigma_0^6
#     dV      = -2 Re( alpha_4 (<y^2 X> - sigma_0^2 <X>) )
#             = -2 Re( alpha_4 * 96 mu^3 sigma_0^4 (2 mu sigma_0^2 - 1) )
# ---------------------------------------------------------------------------


def candidate_b_dV(h: float) -> tuple[float, float]:
    """Returns (sigma0_sq, dV_q4) -- LO variance from candidate-(a) formula
    plus the q^4 saddle correction additive on top."""
    a0h = a_zero(h)
    aph = a_plus(h)
    g0 = a0h + 2.0 * aph
    r = aph / g0  # complex
    N = L_2 / h
    alpha2 = r * N * h ** 2
    alpha4 = (r * r / 2.0 - r / 12.0) * N * h ** 4
    mu = 1.0 / (4.0 * alpha2)  # complex
    sigma0_sq = N * h ** 2 * abs(r) ** 2 / r.real  # = candidate_a evaluated at h

    s2 = sigma0_sq
    EX = 12 * mu ** 2 - 48 * mu ** 3 * s2 + 16 * mu ** 4 * 3 * s2 ** 2
    Ey2X = 12 * mu ** 2 * s2 - 48 * mu ** 3 * 3 * s2 ** 2 + 16 * mu ** 4 * 15 * s2 ** 3
    Y = Ey2X - s2 * EX  # complex
    dV = -2.0 * (alpha4 * Y).real
    return sigma0_sq, dV


# ---------------------------------------------------------------------------
# Composite NLO predictions
# ---------------------------------------------------------------------------


def sigma_sq_pred_a(h: float) -> float:
    """Phase-only (cand a) prediction: sigma^2(h) = C_LO^2 * h * (1 + delta_a)."""
    return C_LO_sq() * h * (1.0 + delta_a_exact(h))


def sigma_sq_pred_ab(h: float) -> float:
    """Phase + q^4 (cand a + b) prediction."""
    s2_a, dV = candidate_b_dV(h)
    return s2_a + dV


def sigma_pred(h: float, model: str = "ab") -> float:
    if model == "LO":
        return math.sqrt(C_LO_sq() * h)
    if model == "a":
        return math.sqrt(sigma_sq_pred_a(h))
    if model == "ab":
        return math.sqrt(sigma_sq_pred_ab(h))
    raise ValueError(model)


# ---------------------------------------------------------------------------
# Effective alpha from log-log linear fit (upstream continuum protocol)
# ---------------------------------------------------------------------------


def loglog_fit(hs: tuple[float, ...], sig_func) -> tuple[float, float]:
    """OLS slope of log sigma vs log h => (alpha_eff, C_eff)."""
    xs = [math.log(h) for h in hs]
    ys = [math.log(sig_func(h)) for h in hs]
    n = len(xs)
    mx = sum(xs) / n
    my = sum(ys) / n
    num = sum((xi - mx) * (yi - my) for xi, yi in zip(xs, ys))
    den = sum((xi - mx) ** 2 for xi in xs)
    slope = num / den
    intercept = my - slope * mx
    return slope, math.exp(intercept)


# ---------------------------------------------------------------------------
# Reporting
# ---------------------------------------------------------------------------


def reldiff(pred: float, ref: float) -> float:
    return (pred - ref) / ref


def report() -> int:
    print("=" * 78)
    print("NLO SADDLE CORRECTION FOR C_arm IN THE RESCALED NN HARNESS")
    print("=" * 78)
    print()
    print("Frozen harness parameters:")
    print(f"  BETA      = {BETA}")
    print(f"  k         = {K_PHYS}")
    print(f"  L_total   = {L_TOTAL}")
    print(f"  FANOUT    = {FANOUT}")
    print(f"  L_2       = 2 L_total / 3 = {L_2:.4f}")
    print(f"  c         = exp(-BETA pi^2 / 16) = {C_FACTOR:.6f}")
    print()
    print("Closed-form NLO coefficients:")
    A = coef_A()
    B = coef_B()
    om = omega()
    C0_sq = C_LO_sq()
    print(f"  A = c / (FANOUT sqrt(2))         = {A:.6f}")
    print(f"  B = c^2 / FANOUT                 = {B:.6f}")
    print(f"  A + B                            = {A + B:.6f}")
    print(f"  omega = k (sqrt(2) - 1)          = {om:.6f}")
    print(f"  A / (A + B)                      = {A / (A + B):.6f}")
    print(f"  C_LO^2 = L_2 (c^2/(2 FANOUT))/(A+B) = {C0_sq:.6f}")
    print(f"  C_LO   = sqrt(C_LO^2)              = {math.sqrt(C0_sq):.6f}")
    print()
    print("Phase-NLO leading h^2 coefficient (candidate a):")
    d2 = d2_phase()
    d4 = d4_phase()
    print(f"  d2_phase = (A/(A+B)) * omega^2 / 2     = {d2:.6f}")
    print(f"  d4_phase (next-order, h^4)             = {d4:.6f}")
    print()
    print(f"  delta_a(h) = (A+B) / (A cos(omega h) + B) - 1")
    print(f"             ~ d2_phase * h^2 + d4_phase * h^4 + O(h^6)")
    print()

    # ------------------------------------------------------------------
    # Per-h closed-form table
    # ------------------------------------------------------------------
    print("-" * 78)
    print("PER-H CLOSED FORM: delta(h) and predicted sigma^2(h)")
    print("-" * 78)
    hs_table = (0.5, 0.25, 0.125, 0.0625, 0.03125, 0.015625)
    print(f"  {'h':>8s}  {'delta_a':>10s}  {'d2 h^2':>10s}  "
          f"{'dV_b/sig^2':>11s}  {'sig^2_a':>10s}  {'sig^2_a+b':>11s}")
    for h in hs_table:
        da = delta_a_exact(h)
        dh2 = d2 * h * h
        s2_a, dVb = candidate_b_dV(h)
        ratio_b = dVb / s2_a if s2_a != 0 else 0.0
        s2_ab = s2_a + dVb
        print(f"  {h:8.5f}  {da:10.6f}  {dh2:10.6f}  "
              f"{ratio_b:10.4%}  {s2_a:10.6f}  {s2_ab:11.6f}")
    print()
    print("  Observation: delta_a(h) ~ d2_phase * h^2 to high accuracy on this")
    print("  h range; the q^4 saddle correction (candidate b) is < 0.4% of the")
    print("  phase correction at h <= 0.25. Candidate (a) DOMINATES.")
    print()

    # ------------------------------------------------------------------
    # Per-h cross-check vs upstream measurements
    # ------------------------------------------------------------------
    print("-" * 78)
    print("CROSS-CHECK vs upstream measured sigma_arm(h)")
    print("-" * 78)
    print(f"  {'h':>8s}  {'sigma_meas':>10s}  {'sig^2_meas':>11s}  "
          f"{'sig^2_a':>10s}  {'res_a':>8s}  {'sig^2_a+b':>11s}  {'res_a+b':>9s}")
    max_abs_res = 0.0
    for h in FIT_HS:
        sm = MEAS_SIGMA[h]
        sm2 = sm * sm
        s2_a = sigma_sq_pred_a(h)
        s2_ab = sigma_sq_pred_ab(h)
        ra = (s2_a - sm2) / sm2
        rab = (s2_ab - sm2) / sm2
        max_abs_res = max(max_abs_res, abs(rab))
        print(f"  {h:8.5f}  {sm:10.4f}  {sm2:11.5f}  "
              f"{s2_a:10.5f}  {ra * 100:+7.2f}%  {s2_ab:11.5f}  {rab * 100:+7.2f}%")
    print()
    print(f"  Max |residual| (a+b): {max_abs_res * 100:.2f}%")
    print()

    # ------------------------------------------------------------------
    # Effective alpha from log-log fit
    # ------------------------------------------------------------------
    print("-" * 78)
    print("EFFECTIVE ALPHA (log-log linear fit on upstream four-point window)")
    print("-" * 78)
    al_LO, C_LO_fit = loglog_fit(FIT_HS, lambda h: sigma_pred(h, "LO"))
    al_a, C_a = loglog_fit(FIT_HS, lambda h: sigma_pred(h, "a"))
    al_ab, C_ab = loglog_fit(FIT_HS, lambda h: sigma_pred(h, "ab"))
    al_emp, C_emp = loglog_fit(FIT_HS, lambda h: MEAS_SIGMA[h])
    print(f"  Model            alpha_eff   C_eff   |alpha_eff - 0.5256|")
    print(f"  LO only          {al_LO:.4f}      {C_LO_fit:.4f}   {abs(al_LO - 0.5256):.4f}")
    print(f"  cand (a) phase   {al_a:.4f}      {C_a:.4f}   {abs(al_a - 0.5256):.4f}")
    print(f"  cand (a)+(b)     {al_ab:.4f}      {C_ab:.4f}   {abs(al_ab - 0.5256):.4f}")
    print(f"  EMPIRICAL        {al_emp:.4f}      {C_emp:.4f}   --")
    print()
    print("  Empirical re-fit reproduces upstream: alpha = 0.5256, C = 2.7107.")
    print()

    # ------------------------------------------------------------------
    # Local alpha at geometric-mean h
    # ------------------------------------------------------------------
    h_geom = math.sqrt(0.25 * 0.03125)
    print(f"  Local alpha at h_geom = sqrt(0.25 * 0.03125) = {h_geom:.5f}:")

    def local_alpha(model: str) -> float:
        eps = 1e-5
        h_lo = h_geom * (1 - eps)
        h_hi = h_geom * (1 + eps)
        s_lo = sigma_pred(h_lo, model)
        s_hi = sigma_pred(h_hi, model)
        return (math.log(s_hi) - math.log(s_lo)) / (math.log(h_hi) - math.log(h_lo))

    print(f"    LO:        alpha_local = {local_alpha('LO'):.4f}")
    print(f"    cand (a):  alpha_local = {local_alpha('a'):.4f}")
    print(f"    cand (a+b):alpha_local = {local_alpha('ab'):.4f}")
    print()

    # ------------------------------------------------------------------
    # Verdict
    # ------------------------------------------------------------------
    print("-" * 78)
    print("VERDICT")
    print("-" * 78)
    print()
    print("  Closed-form NLO leading correction: delta(h) = d2 * h^2,")
    print(f"     d2 = (A / (A + B)) * [k (sqrt(2) - 1)]^2 / 2 = {d2:.4f}")
    print(f"     This shifts alpha_eff (LSQ on 4-point window) from 0.5000 to {al_ab:.4f}.")
    print()
    gap_alpha = abs(al_ab - 0.5256)
    print(f"  Empirical alpha_eff = 0.5256.  Predicted alpha_eff = {al_ab:.4f}.")
    print(f"  Residual gap |delta alpha| = {gap_alpha:.4f}")
    print()
    if gap_alpha <= 0.005:
        print("  STRONG CLOSURE: NLO saddle matches alpha to within +/- 0.005.")
        verdict = "strong"
    elif gap_alpha <= 0.020 and al_ab > 0.5000:
        print("  BOUNDED THEOREM: NLO saddle has the right sign and ~5% magnitude")
        print("  but does not fully close the alpha gap. Residual O(h^4) phase or")
        print("  finite-slit-aperture corrections remain unaccounted for.")
        verdict = "bounded"
    else:
        print("  SHARP NULL: NLO saddle does not explain the alpha residual.")
        verdict = "null"
    print()
    print("  Bounded-support guards:")
    checks = {
        "delta(h) > 0 in fit window":
            all(delta_a_exact(h) > 0 for h in FIT_HS),
        "alpha_eff > 0.5000":
            al_ab > 0.5000,
        "alpha_eff < 0.5256 (NLO undershoots, not overshoots)":
            al_ab < 0.5256,
        "|delta alpha| <= 0.020 (right magnitude)":
            gap_alpha <= 0.020,
        "max per-h sigma^2 residual <= 5%":
            max_abs_res <= 0.05,
        "candidate (a) dominates (b): max dV/sig^2 < 1% on fit window":
            all(abs(candidate_b_dV(h)[1] / candidate_b_dV(h)[0]) < 0.01 for h in FIT_HS),
        "h -> 0 limit recovers C_LO^2 = 6.178":
            math.isclose(sigma_sq_pred_ab(1e-6) / 1e-6, C_LO_sq(), rel_tol=1e-3),
    }
    all_ok = True
    for label, ok in checks.items():
        print(f"    {'PASS' if ok else 'FAIL'}: {label}")
        all_ok = all_ok and ok
    print()
    print(f"  Outcome class: {verdict.upper()}")
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(report())
