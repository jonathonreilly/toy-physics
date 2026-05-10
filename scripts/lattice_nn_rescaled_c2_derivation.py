#!/usr/bin/env python3
"""Bounded phase-saddle support for c2_inf in the T_infinity kernel.

The rescaled NN no-slit source note computes a single-source field-free
amplitude pattern whose A(y_d) has Gaussian magnitude and quadratic phase
at every refinement h tested. The quadratic-phase coefficient

    c2(h) = (d^2/dy^2) arg A(y_d) / 2

converges as h -> 0 to a finite limit

    c2_inf_numeric ~= 0.02995    (runner cache, h = 0.0625)

and satisfies c2_inf ~= K_PHYS / (4 L_total) = 0.03125 to within ~4%.
The factor /(4L), rather than the naive ray-optics /(2L), and the
residual ~4% gap are the diagnostic targets here.

This script applies the same saddle-point machinery as the bounded
C_arm support note, but to the IMAGINARY part of the Gaussian covariance
r(h) = a_pm(h)/g(0;h) rather than its real part. The real part of r gives
sigma_arm^2; the imaginary part of r gives c2(h).

Closed form:

    c2(h)  =  Im( a_pm(h) * conj(a_0(h)) )
              / [ 4 * L * h * |a_pm(h)|^2 ]

For the harness's per-step amplitudes
  a_0(h)   = exp(i k h)              / sqrt(FANOUT)
  a_pm(h)  = c * exp(i k h sqrt(2))  / sqrt(2 * FANOUT),   c = exp(-BETA pi^2/16)

this evaluates to

    c2(h)  =  sin( k h (sqrt(2) - 1) )  /  ( 2 sqrt(2) * c * L * h )

In the h -> 0 limit (sin x -> x):

    c2_inf =  k * (sqrt(2) - 1) / (2 sqrt(2) * c * L)
           =  k * (2 - sqrt(2)) / (4 * c * L)

With harness parameters BETA=0.8, k=5, L_total=40, FANOUT=3:

    c2_inf_analytic  =  0.029985

versus

    c2_inf_diagnostic =  0.02995   (runner cache, ~3% above K/(4L)*c/(2-sqrt(2)))
    K_PHYS / (4 L)    =  0.03125   (diagnostic approximation, off by ~4%)

The residual versus the diagnostic runner value is ~0.12%, and the formula
is ~30x sharper than the K/(4L) heuristic. The factor (2 - sqrt(2)) / c
~= 0.9596 carries the 4% gap between K/(4L) = 0.03125 and the computed
c2_inf = 0.02995.

This is a bounded lattice-configuration calculation for the no-slit
deterministic-rescale NN harness, not an exact retained-status claim.

Length identification (the load-bearing physics step):
the single-source kernel-identification runner uses NO slits, so the slit
re-anchoring that motivated L_2 = 2 L_total / 3 in the companion support
note does NOT apply here. The propagation length entering the phase saddle is L_total = 40,
which is what the formula uses. As cross-check, the script also reports
the value the formula would give with L = L_2 (which lands ~50% off).
This is the asymmetry between the magnitude and phase saddles: the
magnitude saddle in the companion support note was applied to a slit-anchored harness; the
phase saddle here is applied to a slit-free harness.

Usage:
    python3 scripts/lattice_nn_rescaled_c2_derivation.py
"""

from __future__ import annotations

import cmath
import math
import sys


# ---------------------------------------------------------------------------
# Harness parameters (frozen from the landed no-slit kernel runner)
# ---------------------------------------------------------------------------

BETA = 0.8
K_PHYS = 5.0
PHYS_L = 40.0
FANOUT = 3.0

L_TOTAL = PHYS_L
# Slit fraction is irrelevant for the no-slit kernel-identification harness;
# we include L_2 only as a cross-check against the companion support note's
# slit-length identification.
SLIT_LAYER_FRACTION = 1.0 / 3.0
L_2 = (1.0 - SLIT_LAYER_FRACTION) * L_TOTAL  # = 2 L_total / 3 = 26.667

# Diagnostic reference values from the landed no-slit runner cache.
C2_INF_EMPIRICAL = 0.02995  # h -> 0 extrapolation across h = 0.5..0.0625
C2_PER_H_EMPIRICAL = {
    0.5: 0.025062,
    0.25: 0.028768,
    0.125: 0.029676,
    0.0625: 0.029886,
}


# ---------------------------------------------------------------------------
# Per-step amplitudes (same local harness convention as the C_arm support note)
# ---------------------------------------------------------------------------

def angular_weight() -> float:
    """exp(-BETA * theta^2) for the diy = +/- 1 edges (theta = pi/4)."""
    theta = math.pi / 4.0
    return math.exp(-BETA * theta * theta)


def a_zero(h: float) -> complex:
    """Per-step amplitude for diy = 0.

    f(0; h)  =  step_scale * exp(i k h) / h    with step_scale = h / sqrt(FANOUT)
             =  exp(i k h) / sqrt(FANOUT)
    """
    return cmath.exp(1j * K_PHYS * h) / math.sqrt(FANOUT)


def a_plus(h: float) -> complex:
    """Per-step amplitude for diy = +/- 1.

    f(+/-1; h) = step_scale * exp(i k h sqrt(2)) * c / (h sqrt(2))
              = c * exp(i k h sqrt(2)) / sqrt(2 * FANOUT)
    """
    c = angular_weight()
    return c * cmath.exp(1j * K_PHYS * h * math.sqrt(2.0)) / math.sqrt(2.0 * FANOUT)


def g_zero(h: float) -> complex:
    """Lateral characteristic function at q=0: g(0;h) = a_0(h) + 2 a_pm(h)."""
    return a_zero(h) + 2.0 * a_plus(h)


# ---------------------------------------------------------------------------
# Closed-form c2(h) from the saddle-point complex-Gaussian formula
# ---------------------------------------------------------------------------

def c2_from_saddle(L: float, h: float) -> dict:
    """Closed-form c2(h) at lattice spacing h, propagation length L.

    From A(y) = g(0)^N / sqrt(4 pi N r h^2) * exp(-y^2 / (4 N r h^2)) with
    r = a_pm/g(0) and N = L/h:

        arg A(y)  =  (phase constant)  +  y^2 * Im(r) / (4 N h^2 |r|^2)

    So c2(h) := (1/2) * d^2/dy^2 arg A(y)
              =  Im(r) / (4 N h^2 |r|^2)
              =  Im( a_pm * conj(a_0) )  /  ( 4 L h |a_pm|^2 ).

    The second equality uses Im(a_pm * conj(g(0))) = Im(a_pm * conj(a_0))
    because 2 |a_pm|^2 is real, and Im(r)/|r|^2 = Im(a_pm * conj(g(0)))/|a_pm|^2.
    """
    a0 = a_zero(h)
    ap = a_plus(h)
    g0 = g_zero(h)

    # Im(a_pm * conj(g(0))) = Im(a_pm * conj(a_0) + 2 |a_pm|^2)
    #                      = Im(a_pm * conj(a_0))
    num = (ap * a0.conjugate()).imag
    den = 4.0 * L * h * (abs(ap) ** 2)
    c2 = num / den

    # Also expose r and its imaginary part for diagnostic transparency
    r = ap / g0
    return {
        "L": L,
        "h": h,
        "a0": a0,
        "a_pm": ap,
        "g0": g0,
        "r": r,
        "Im_r": r.imag,
        "abs_r_sq": abs(r) ** 2,
        "Im_apm_conj_a0": num,
        "denom": den,
        "c2": c2,
    }


def c2_continuum(L: float) -> float:
    """h -> 0 limit of c2(h).

    sin(k h (sqrt(2)-1)) -> k h (sqrt(2)-1), so

        c2_inf = k (sqrt(2)-1) / (2 sqrt(2) c L)
              = k (2 - sqrt(2)) / (4 c L)
    """
    c = angular_weight()
    return K_PHYS * (2.0 - math.sqrt(2.0)) / (4.0 * c * L)


def c2_closed_form_per_h(L: float, h: float) -> float:
    """Equivalent closed form using sin(k h (sqrt(2)-1)) directly."""
    c = angular_weight()
    return math.sin(K_PHYS * h * (math.sqrt(2.0) - 1.0)) / (
        2.0 * math.sqrt(2.0) * c * L * h
    )


# ---------------------------------------------------------------------------
# Hessian determinant of the saddle (sanity check)
# ---------------------------------------------------------------------------

def saddle_hessian(L: float, h: float) -> dict:
    """The lateral saddle is a 1-D complex Gaussian with covariance 1/(2 N r h^2).

    The "Hessian" of -log g(q;h)^N at q=0 is

        H  =  d^2/dq^2 [ -N log g(q;h) ] |_{q=0}
            =  2 N r(h) h^2.

    So Re(H) controls the magnitude width, Im(H) controls the phase curvature.
    Both decompose into one-dimensional pieces (no off-diagonal coupling
    in 1+1 lattice). We expose them for transparency.
    """
    a0 = a_zero(h)
    ap = a_plus(h)
    g0 = g_zero(h)
    r = ap / g0
    N = L / h
    H = 2.0 * N * r * (h ** 2)
    # det H = H itself for 1-D
    return {
        "N": N,
        "r": r,
        "H": H,
        "Re_H": H.real,
        "Im_H": H.imag,
        "|H|": abs(H),
    }


# ---------------------------------------------------------------------------
# Reporting
# ---------------------------------------------------------------------------

def reldiff(pred: float, ref: float) -> float:
    return (pred - ref) / ref


def report() -> int:
    print("=" * 78)
    print("BOUNDED PHASE-SADDLE SUPPORT FOR c2_inf")
    print("=" * 78)
    print()
    print("Frozen harness parameters (landed no-slit kernel runner):")
    print(f"  BETA      = {BETA}")
    print(f"  k         = {K_PHYS}")
    print(f"  L_total   = {L_TOTAL}     (source -> detector)")
    print(f"  FANOUT    = {FANOUT}")
    print(f"  slit_layer_fraction = {SLIT_LAYER_FRACTION:.4f}  (companion support only;")
    print(f"                        NOT used for the no-slit phase saddle)")
    print(f"  L_2       = {L_2:.4f}  (companion magnitude saddle; cross-check only)")
    print()
    print(f"Diagnostic reference (landed no-slit runner cache):")
    print(f"  c2_inf_diagnostic ~= {C2_INF_EMPIRICAL}")
    print(f"  K_PHYS / (4 L)   =  {K_PHYS / (4.0 * L_TOTAL):.6f}  (off by ~4%)")
    print(f"  K_PHYS / (2 L)   =  {K_PHYS / (2.0 * L_TOTAL):.6f}  (ray-optics, off by 2x)")
    print()
    print("-" * 78)
    print("STAGE 1: Saddle-point closed form")
    print("-" * 78)
    print()
    print("  Per-step lateral characteristic function (C_arm support note):")
    print("      g(q; h) = a_0(h) + 2 a_pm(h) cos(q h)")
    print()
    print("  Saddle at q=0 (a_+ = a_-) gives complex Gaussian")
    print("      g(q; h)^N = g(0)^N * exp(-N r(h) (q h)^2 + O(q^4))")
    print("  with r(h) = a_pm(h) / g(0; h)  (complex).")
    print()
    print("  Fourier transform:")
    print("      A(y) = g(0)^N / sqrt(4 pi N r h^2) * exp(-y^2 / (4 N r h^2))")
    print()
    print("  Real part of -y^2/(4 N r h^2) gives the Gaussian magnitude")
    print("  (sigma_arm^2 = N h^2 |r|^2 / Re(r); C_arm support note).")
    print("  Imaginary part of -y^2/(4 N r h^2) gives the quadratic phase:")
    print()
    print("      arg A(y) ⊇ y^2 * Im(r) / (4 N h^2 |r|^2)")
    print()
    print("  So  c2(h) = (1/2) d^2/dy^2 arg A(y)")
    print("            = Im(r) / (4 N h^2 |r|^2)")
    print("            = Im(a_pm * conj(a_0)) / (4 L h |a_pm|^2).")
    print()
    print("-" * 78)
    print("STAGE 2: Reduction with harness amplitudes")
    print("-" * 78)
    print()
    c = angular_weight()
    print(f"  c                = exp(-BETA pi^2 / 16) = {c:.6f}")
    print(f"  |a_pm|^2         = c^2 / (2 FANOUT)    = {c*c/(2*FANOUT):.6f}")
    print(f"  a_pm * conj(a_0) = c/(sqrt(2)*FANOUT) * exp(i k h (sqrt(2)-1))")
    print(f"  Im(a_pm * conj(a_0)) = c/(sqrt(2)*FANOUT) * sin(k h (sqrt(2)-1))")
    print()
    print("  Substitute:")
    print("      c2(h) = [c/(sqrt(2)*FANOUT) * sin(k h (sqrt(2)-1))]")
    print("               / [4 L h * c^2 / (2 FANOUT)]")
    print("            = sin(k h (sqrt(2)-1)) / (2 sqrt(2) c L h)")
    print()
    print("  Continuum limit (sin x -> x):")
    print("      c2_inf = k (sqrt(2)-1) / (2 sqrt(2) c L)")
    print("             = k (2 - sqrt(2)) / (4 c L)")
    print()
    print(f"  Numerical reduction at harness parameters:")
    print(f"    sqrt(2) - 1                =  {math.sqrt(2)-1:.6f}")
    print(f"    2 - sqrt(2)                =  {2-math.sqrt(2):.6f}")
    print(f"    (2-sqrt(2))/c              =  {(2-math.sqrt(2))/c:.6f}  (->1 in c->1 limit)")
    print(f"    c2_inf_analytic            =  k (2-sqrt(2)) / (4 c L)")
    print(f"                                = {K_PHYS} * {2-math.sqrt(2):.6f}")
    print(f"                                  / (4 * {c:.6f} * {L_TOTAL})")
    print(f"                                =  {c2_continuum(L_TOTAL):.6f}")
    print()
    print("-" * 78)
    print("STAGE 3: Length identification (no-slit harness)")
    print("-" * 78)
    print()
    print("  The no-slit kernel-identification harness propagates from a single")
    print("  source at the origin to the detector at x = L_total with NO slits")
    print("  and NO blocked nodes. The slit re-anchoring that forced")
    print("  L_eff = L_2 = 2 L_total / 3 in the C_arm support note does NOT apply here.")
    print("  The propagation length entering the phase saddle is L_total.")
    print()
    print("  Cross-check: evaluate the same closed form with L = L_2 to confirm")
    print("  it does NOT match the no-slit numerics:")
    print()
    c2_L = c2_continuum(L_TOTAL)
    c2_L2 = c2_continuum(L_2)
    print(f"    c2_inf(L = L_total = 40)   =  {c2_L:.6f}   "
          f"residual = {100*reldiff(c2_L, C2_INF_EMPIRICAL):+.2f}%")
    print(f"    c2_inf(L = L_2     = 26.67) = {c2_L2:.6f}   "
          f"residual = {100*reldiff(c2_L2, C2_INF_EMPIRICAL):+.2f}%")
    print()
    print("  L = L_total wins by a factor of ~400 in residual.")
    print("  -> The phase saddle is anchored by L_total, not L_2.")
    print()
    print("-" * 78)
    print("STAGE 4: Per-h cross-check with finite-h sin(...) formula")
    print("-" * 78)
    print()
    print("  Retain the full sin(k h (sqrt(2)-1)) instead of its small-x limit:")
    print("      c2(h) = sin(k h (sqrt(2)-1)) / (2 sqrt(2) c L_total h)")
    print()
    print(f"  {'h':>7s}  {'c2_analytic':>12s}  {'c2_diagnostic':>13s}  "
          f"{'residual':>10s}")
    max_per_h_residual = 0.0
    previous_abs_residual = None
    residuals_shrink = True
    for h in (0.5, 0.25, 0.125, 0.0625):
        c2_pred = c2_closed_form_per_h(L_TOTAL, h)
        c2_emp = C2_PER_H_EMPIRICAL[h]
        rd = reldiff(c2_pred, c2_emp)
        abs_rd = abs(rd)
        max_per_h_residual = max(max_per_h_residual, abs_rd)
        if previous_abs_residual is not None and abs_rd > previous_abs_residual + 1e-12:
            residuals_shrink = False
        previous_abs_residual = abs_rd
        # Sanity: confirm the saddle-machinery formula gives the same number
        c2_via_saddle = c2_from_saddle(L_TOTAL, h)["c2"]
        assert abs(c2_pred - c2_via_saddle) < 1e-12, (
            f"c2 closed form / saddle disagree at h={h}: "
            f"{c2_pred} vs {c2_via_saddle}"
        )
        print(f"  {h:7.4f}  {c2_pred:12.6f}  {c2_emp:13.6f}  {100*rd:+9.3f}%")
    print()
    print("  All four points agree with the diagnostic runner fit to within ~1%.")
    print()
    print("-" * 78)
    print("STAGE 5: Hessian of the saddle (diagnostic)")
    print("-" * 78)
    print()
    print("  H = d^2/dq^2 [-N log g(q;h)] at q=0 = 2 N r(h) h^2 = 2 L r(h) h.")
    print("  Re(H) sets Gaussian width (sigma^2 = h^2 * N * |r|^2/Re(r) =")
    print("  L h |r|^2/Re(r), so width^2 scales like L h).")
    print("  Im(H) sets quadratic phase: c2 = Im(H) / (4 L^2 h^2 |r|^2/N)")
    print("  Equivalently c2 = Im(r) / (4 L h |r|^2), independent of h in the")
    print("  continuum limit because Im(r) -> Im(r)|_{h->0} like O(h^0).")
    print()
    print(f"  {'h':>7s}  {'Re H':>10s}  {'Im H':>10s}  {'|H|':>10s}  "
          f"{'Re H / h':>10s}  {'Im H / h':>10s}")
    for h in (0.5, 0.25, 0.125, 0.0625):
        hess = saddle_hessian(L_TOTAL, h)
        print(f"  {h:7.4f}  {hess['Re_H']:10.4f}  {hess['Im_H']:10.4f}  "
              f"{hess['|H|']:10.4f}  {hess['Re_H']/h:10.4f}  "
              f"{hess['Im_H']/h:10.4f}")
    print()
    print("  H ~ h linearly as h -> 0 (since N = L/h and r is bounded), so")
    print("  Re(H)/h and Im(H)/h stabilize to continuum limits. The phase")
    print("  Hessian Im(H)/h -> 2 L * Im(r)|_{h->0}, which is finite, giving")
    print("  c2_inf -> Im(r)|_0 / (4 L |r|_0^2) -- the 0.029985 result.")
    print()
    print("-" * 78)
    print("VERDICT")
    print("-" * 78)
    print()
    print(f"  c2_inf_analytic   =  k (2 - sqrt(2)) / (4 c L_total)")
    print(f"                    =  {c2_continuum(L_TOTAL):.6f}")
    print()
    print(f"  c2_inf_diagnostic =  {C2_INF_EMPIRICAL}")
    print(f"  K_PHYS / (4 L)    =  {K_PHYS / (4.0 * L_TOTAL):.6f}  "
          f"(diagnostic approximation)")
    print()
    res_analytic = abs(reldiff(c2_continuum(L_TOTAL), C2_INF_EMPIRICAL))
    res_naive = abs(reldiff(K_PHYS / (4.0 * L_TOTAL), C2_INF_EMPIRICAL))
    print(f"  Residual (analytic vs diagnostic):      {100*res_analytic:.3f}%")
    print(f"  Residual (K/(4L) vs diagnostic):        {100*res_naive:.3f}%")
    print()
    print("  BOUNDED SUPPORT: the phase-saddle closed form")
    print()
    print("      c2_inf  =  k (2 - sqrt(2)) / (4 c L_total)")
    print()
    print("  matches the diagnostic c2_inf to 0.12%, ~30x sharper than")
    print("  the K/(4L) heuristic. The factor (2 - sqrt(2))/c")
    print(f"  ~= {(2-math.sqrt(2))/c:.4f} carries the ~4% gap between K/(4L)")
    print("  and the computed 0.02995.")
    print()

    res_wrong_L2 = abs(reldiff(c2_continuum(L_2), C2_INF_EMPIRICAL))
    res_ray = abs(reldiff(K_PHYS / (2.0 * L_TOTAL), C2_INF_EMPIRICAL))
    checks = {
        "phase-saddle residual <= 1%": res_analytic <= 0.01,
        "per-h finite-h residual <= 1%": max_per_h_residual <= 0.01,
        "per-h residuals shrink toward h -> 0": residuals_shrink,
        "K/(4L) heuristic is worse than saddle formula": res_naive > res_analytic,
        "wrong L_2 length is decisively worse": res_wrong_L2 > 0.25,
        "ray-optics K/(2L) is decisively worse": res_ray > 1.0,
    }
    print("  Bounded-support guards:")
    for label, ok in checks.items():
        print(f"    {'PASS' if ok else 'FAIL'}: {label}")
    return 0 if all(checks.values()) else 1


if __name__ == "__main__":
    sys.exit(report())
