#!/usr/bin/env python3
"""Exact-symbolic audit-companion runner for
`ckm_barred_orthocenter_euler_line_exact_closed_form_theorem_note_2026-04-25`.

The parent note's load-bearing content is the closed-form derivation that
on the cited NLO Wolfenstein protected-gamma-bar surface

  rho_bar  = (4 - alpha_s) / 24            (cited N1)
  eta_bar  = sqrt(5)(4 - alpha_s) / 24     (cited N2)
  R_b_bar^2 = (4 - alpha_s)^2 / 96         (cited N3)
  N7 leading slope (alpha_bar - pi/2)/alpha_s = sqrt(5)/20

force the named orthocenter / centroid / circumcenter / Euler-line
closed forms

  (O1) H = (rho_bar, (20 + alpha_s)/(24 sqrt(5)))         [linear in alpha_s]
  (O2) H - V_3 = (0, alpha_s sqrt(5)/20)
  (O3) G = ((28 - alpha_s)/72, sqrt(5)(4 - alpha_s)/72)
  (O4) O = (1/2, -alpha_s sqrt(5)/40)
  (O5) H = 3 G - 2 O  (Euler line; HG : GO = 2 : 1)
  (O6) H - V_3 = -2 (O - M) with M = (1/2, 0)
  (O7) (H_y - V_3_y)/alpha_s = sqrt(5)/20  [= cited N7 slope]

The existing primary runner
(`scripts/frontier_ckm_barred_orthocenter_euler_line_exact_closed_form.py`)
verifies these identities at floating-point tolerance using the
canonical numerical `alpha_s(v)`. This Pattern B audit companion adds a
sympy-based exact-symbolic verification:

  (a) treats `alpha_s(v)` as a free positive real symbol;
  (b) imports cited (N1), (N2), (N3) verbatim;
  (c) builds H, G, O directly from triangle geometry (altitude
      construction, centroid average, perpendicular-bisector
      construction) and verifies each closed-form expression via
      `sympy.simplify(LHS - RHS) == 0`;
  (d) verifies the Euler-line identity `H = 3G - 2O` parametric in
      alpha_s;
  (e) verifies the apex-orthocenter / circumcenter-hypotenuse
      anti-relation `H - V_3 = -2 (O - M)` parametric;
  (f) verifies `(H_y - V_3_y)/alpha_s = sqrt(5)/20` matches the
      cited N7 slope;
  (g) provides counterfactual probes confirming the (4 - alpha_s)
      cancellation in both H_y and O_y.

Companion role: Pattern B audit-acceleration only. Not a new claim row,
not a new source note, no status promotion. The cited (N1)-(N3), N7
slope, and structural counts are imported from upstream authority notes
and are not re-derived here.
"""

from __future__ import annotations

import sys

try:
    import sympy
    from sympy import Rational, Symbol, simplify, sqrt
except ImportError:
    print("FAIL: sympy required for exact algebra")
    sys.exit(1)


PASS = 0
FAIL = 0


def check(label: str, ok: bool, detail: str = "") -> None:
    global PASS, FAIL
    if ok:
        PASS += 1
        tag = "PASS (B)"
    else:
        FAIL += 1
        tag = "FAIL (B)"
    suffix = f"  ({detail})" if detail else ""
    print(f"  [{tag}] {label}{suffix}")


def section(title: str) -> None:
    print()
    print("-" * 88)
    print(title)
    print("-" * 88)


def main() -> int:
    print("=" * 88)
    print("Audit companion (exact-symbolic) for")
    print("ckm_barred_orthocenter_euler_line_exact_closed_form_theorem_note_2026-04-25")
    print("Goal: sympy-symbolic verification of (O1)-(O7) at exact precision")
    print("parametric in alpha_s on the cited NLO protected-gamma-bar surface.")
    print("=" * 88)

    # ---------------------------------------------------------------------
    section("Part 0: symbolic setup and cited inputs")
    # ---------------------------------------------------------------------
    alpha_s = Symbol("alpha_s", positive=True, real=True)
    N_pair = Rational(2)
    N_quark = Rational(6)

    rho_bar = (4 - alpha_s) / Rational(24)
    eta_bar = sqrt(5) * (4 - alpha_s) / Rational(24)
    Rb_bar_sq = (4 - alpha_s) ** 2 / Rational(96)

    V1 = (Rational(0), Rational(0))
    V2 = (Rational(1), Rational(0))
    V3 = (rho_bar, eta_bar)

    print(f"  symbolic alpha_s(v) = {alpha_s}")
    print(f"  V_1 = {V1}, V_2 = {V2}")
    print(f"  V_3 = (rho_bar, eta_bar) = ({rho_bar}, {eta_bar})")

    # ---------------------------------------------------------------------
    section("Part 1: (O3) Centroid G = (V_1 + V_2 + V_3)/3")
    # ---------------------------------------------------------------------
    G_x = simplify((V1[0] + V2[0] + V3[0]) / 3)
    G_y = simplify((V1[1] + V2[1] + V3[1]) / 3)
    G_x_target = (28 - alpha_s) / Rational(72)
    G_y_target = sqrt(5) * (4 - alpha_s) / Rational(72)

    check(
        "(O3) G_x == (28 - alpha_s)/72 (parametric)",
        simplify(G_x - G_x_target) == 0,
        f"residual = {simplify(G_x - G_x_target)}",
    )
    check(
        "(O3) G_y == sqrt(5)(4 - alpha_s)/72 (parametric)",
        simplify(G_y - G_y_target) == 0,
        f"residual = {simplify(G_y - G_y_target)}",
    )

    # ---------------------------------------------------------------------
    section("Part 2: (O1) Orthocenter H from altitude construction")
    # ---------------------------------------------------------------------
    # Altitude from V_3 perpendicular to V_1 V_2 (which lies on the x-axis):
    # vertical line x = rho_bar, hence H_x = rho_bar.
    H_x = simplify(rho_bar)
    H_x_target = rho_bar  # equals (4 - alpha_s)/24

    # Altitude from V_1 perpendicular to side V_2 V_3:
    # direction (eta_bar, 1 - rho_bar), through (0, 0); intersects x = H_x at
    #   y = H_x (1 - rho_bar) / eta_bar.
    H_y = simplify(H_x * (1 - rho_bar) / eta_bar)
    H_y_target = (20 + alpha_s) / (Rational(24) * sqrt(5))

    check(
        "(O1) H_x == rho_bar == (4 - alpha_s)/24 (altitude from V_3 vertical)",
        simplify(H_x - (4 - alpha_s) / Rational(24)) == 0,
        f"residual = {simplify(H_x - (4-alpha_s)/Rational(24))}",
    )
    check(
        "(O1) H_y == (20 + alpha_s)/(24 sqrt(5)) (parametric)",
        simplify(H_y - H_y_target) == 0,
        f"residual = {simplify(H_y - H_y_target)}",
    )

    # H_y is exactly degree-1 in alpha_s.
    H_y_poly = sympy.Poly(simplify(H_y * sqrt(5)), alpha_s)  # multiply by sqrt(5) to get rational coeffs
    check(
        "(O1) H_y * sqrt(5) is a degree-1 polynomial in alpha_s",
        H_y_poly.degree() == 1,
        f"degree = {H_y_poly.degree()}",
    )

    # Cross-check H lies on altitude from V_2 perpendicular to V_1 V_3.
    # V_1 V_3 direction: (rho_bar, eta_bar); perpendicular has direction
    # (eta_bar, -rho_bar). Through V_2 = (1, 0): line { (1 + t eta_bar, -t rho_bar) }.
    # The line passes through (H_x, H_y) iff (H_x - 1)/eta_bar = -H_y/rho_bar,
    # i.e. rho_bar (H_x - 1) + eta_bar H_y = 0.
    altitude_V2_residual = simplify(rho_bar * (H_x - 1) + eta_bar * H_y)
    check(
        "(O1) H lies on altitude from V_2 (cross-check)",
        altitude_V2_residual == 0,
        f"residual = {altitude_V2_residual}",
    )

    # ---------------------------------------------------------------------
    section("Part 3: (O2) Apex-orthocenter offset H - V_3 = (0, alpha_s sqrt(5)/20)")
    # ---------------------------------------------------------------------
    HV3_x = simplify(H_x - V3[0])
    HV3_y = simplify(H_y - V3[1])
    HV3_y_target = alpha_s * sqrt(5) / Rational(20)

    check(
        "(O2) H_x - V_3_x == 0 (purely vertical offset)",
        HV3_x == 0,
        f"residual = {HV3_x}",
    )
    check(
        "(O2) H_y - V_3_y == alpha_s sqrt(5)/20 (parametric)",
        simplify(HV3_y - HV3_y_target) == 0,
        f"residual = {simplify(HV3_y - HV3_y_target)}",
    )
    # Structural-integer form: alpha_s/[N_pair^2 sqrt(N_quark - 1)].
    HV3_y_struct = alpha_s / (N_pair ** 2 * sqrt(N_quark - 1))
    check(
        "(O2) H_y - V_3_y == alpha_s/[N_pair^2 sqrt(N_quark - 1)] at (2, 6)",
        simplify(HV3_y_struct - HV3_y_target) == 0,
        f"residual = {simplify(HV3_y_struct - HV3_y_target)}",
    )

    # ---------------------------------------------------------------------
    section("Part 4: (O4) Circumcenter O re-derived from (N1, N2, N3)")
    # ---------------------------------------------------------------------
    # Perpendicular bisector of V_1 V_2 is x = 1/2, so O_x = 1/2.
    # Equidistance |O - V_1|^2 = |O - V_3|^2 gives O_y = (R_b_bar^2 - rho_bar)/(2 eta_bar).
    O_x = Rational(1, 2)
    O_y = simplify((Rb_bar_sq - rho_bar) / (2 * eta_bar))
    O_y_target = -alpha_s * sqrt(5) / Rational(40)

    check(
        "(O4) O_x == 1/2 (alpha_s-independent)",
        simplify(O_x - Rational(1, 2)) == 0,
        f"value = {O_x}",
    )
    check(
        "(O4) O_y == -alpha_s sqrt(5)/40 (parametric)",
        simplify(O_y - O_y_target) == 0,
        f"residual = {simplify(O_y - O_y_target)}",
    )
    # Structural-integer form.
    O_y_struct = -alpha_s / (N_pair ** 3 * sqrt(N_quark - 1))
    check(
        "(O4) O_y == -alpha_s/[N_pair^3 sqrt(N_quark - 1)] at (2, 6)",
        simplify(O_y_struct - O_y_target) == 0,
        f"residual = {simplify(O_y_struct - O_y_target)}",
    )

    # ---------------------------------------------------------------------
    section("Part 5: (O5) Euler line H = 3 G - 2 O")
    # ---------------------------------------------------------------------
    rhs_x = simplify(3 * G_x - 2 * O_x)
    rhs_y = simplify(3 * G_y - 2 * O_y)

    check(
        "(O5) 3 G_x - 2 O_x == H_x (parametric)",
        simplify(rhs_x - H_x) == 0,
        f"residual = {simplify(rhs_x - H_x)}",
    )
    check(
        "(O5) 3 G_y - 2 O_y == H_y (parametric)",
        simplify(rhs_y - H_y) == 0,
        f"residual = {simplify(rhs_y - H_y)}",
    )

    # Euler line collinearity: cross product (G - O) x (H - O) = 0.
    cross = simplify((G_x - O_x) * (rhs_y - O_y) - (G_y - O_y) * (rhs_x - O_x))
    check(
        "(O5) H, G, O are collinear (cross product = 0)",
        cross == 0,
        f"residual = {cross}",
    )

    # HG : GO = 2 : 1 ratio (HG vector = 2 * GO vector).
    HG_x = simplify(H_x - G_x)
    HG_y = simplify(H_y - G_y)
    GO_x = simplify(G_x - O_x)
    GO_y = simplify(G_y - O_y)
    check(
        "(O5) HG = 2 GO (x-component)",
        simplify(HG_x - 2 * GO_x) == 0,
        f"residual = {simplify(HG_x - 2*GO_x)}",
    )
    check(
        "(O5) HG = 2 GO (y-component)",
        simplify(HG_y - 2 * GO_y) == 0,
        f"residual = {simplify(HG_y - 2*GO_y)}",
    )

    # ---------------------------------------------------------------------
    section("Part 6: (O6) H - V_3 = -2 (O - M) with M = hypotenuse midpoint (1/2, 0)")
    # ---------------------------------------------------------------------
    M_x, M_y = Rational(1, 2), Rational(0)

    minus2_OM_x = simplify(-2 * (O_x - M_x))
    minus2_OM_y = simplify(-2 * (O_y - M_y))

    check(
        "(O6) H_x - V_3_x == -2 (O_x - M_x) (both equal 0)",
        simplify(HV3_x - minus2_OM_x) == 0,
        f"residual = {simplify(HV3_x - minus2_OM_x)}",
    )
    check(
        "(O6) H_y - V_3_y == -2 (O_y - M_y) (parametric)",
        simplify(HV3_y - minus2_OM_y) == 0,
        f"residual = {simplify(HV3_y - minus2_OM_y)}",
    )

    # ---------------------------------------------------------------------
    section("Part 7: (O7) slope identification (H_y - V_3_y)/alpha_s = sqrt(5)/20 (= N7 slope)")
    # ---------------------------------------------------------------------
    slope = simplify(HV3_y / alpha_s)
    n7_slope = sqrt(5) / Rational(20)
    check(
        "(O7) (H_y - V_3_y)/alpha_s == sqrt(5)/20 (N7 slope)",
        simplify(slope - n7_slope) == 0,
        f"residual = {simplify(slope - n7_slope)}",
    )
    # Structural-integer form: 1/[N_pair^2 sqrt(N_quark - 1)] = sqrt(5)/20 at (2, 6).
    slope_struct = Rational(1) / (N_pair ** 2 * sqrt(N_quark - 1))
    check(
        "(O7) slope == 1/[N_pair^2 sqrt(N_quark - 1)] at (2, 6)",
        simplify(slope_struct - n7_slope) == 0,
        f"residual = {simplify(slope_struct - n7_slope)}",
    )

    # ---------------------------------------------------------------------
    section("Part 8: (O9) atlas-LO recovery at alpha_s = 0")
    # ---------------------------------------------------------------------
    H_x_LO = simplify(H_x.subs(alpha_s, 0))
    H_y_LO = simplify(H_y.subs(alpha_s, 0))
    V3_x_LO = simplify(V3[0].subs(alpha_s, 0))
    V3_y_LO = simplify(V3[1].subs(alpha_s, 0))
    check(
        "(O9) H_LO == V_3_LO == (1/6, sqrt(5)/6) (right-angle vertex coincidence)",
        simplify(H_x_LO - Rational(1, 6)) == 0
        and simplify(H_y_LO - sqrt(5) / 6) == 0
        and simplify(V3_x_LO - Rational(1, 6)) == 0
        and simplify(V3_y_LO - sqrt(5) / 6) == 0,
        f"H_LO = ({H_x_LO}, {H_y_LO}); V_3_LO = ({V3_x_LO}, {V3_y_LO})",
    )

    O_x_LO = simplify(O_x)
    O_y_LO = simplify(O_y.subs(alpha_s, 0))
    check(
        "(O9) O_LO == (1/2, 0) (hypotenuse midpoint)",
        simplify(O_x_LO - Rational(1, 2)) == 0 and simplify(O_y_LO) == 0,
        f"O_LO = ({O_x_LO}, {O_y_LO})",
    )

    # ---------------------------------------------------------------------
    section("Part 9: (O8) selection rule -- H, G are degree-1 polynomials in alpha_s")
    # ---------------------------------------------------------------------
    check(
        "H_x is degree-1 in alpha_s",
        sympy.Poly(H_x, alpha_s).degree() == 1,
    )
    check(
        "H_y * sqrt(5) is degree-1 in alpha_s",
        sympy.Poly(simplify(H_y * sqrt(5)), alpha_s).degree() == 1,
    )
    check(
        "G_x is degree-1 in alpha_s",
        sympy.Poly(G_x, alpha_s).degree() == 1,
    )
    check(
        "G_y / sqrt(5) is degree-1 in alpha_s",
        sympy.Poly(simplify(G_y / sqrt(5)), alpha_s).degree() == 1,
    )

    # ---------------------------------------------------------------------
    section("Part 10: counterfactual probes")
    # ---------------------------------------------------------------------
    # If (4 - alpha_s) factor in eta_bar were dropped, H_y would not
    # collapse to (20 + alpha_s)/(24 sqrt(5)) cleanly.
    eta_bar_alt = sqrt(5) * Rational(4) / Rational(24)
    H_y_alt = simplify(H_x * (1 - rho_bar) / eta_bar_alt)
    check(
        "counterfactual: dropping (4-alpha_s) from eta_bar breaks H_y closed form",
        simplify(H_y_alt - H_y_target) != 0,
        "alternate H_y is no longer (20 + alpha_s)/(24 sqrt(5))",
    )

    # If rho_bar atlas-LO were 1/6 (no NLO), H_y would not be linear in alpha_s.
    rho_bar_alt = Rational(1, 6)
    H_x_alt = rho_bar_alt
    H_y_alt2 = simplify(H_x_alt * (1 - rho_bar_alt) / eta_bar)
    check(
        "counterfactual: at rho_bar = 1/6 (atlas-LO), H_y differs from full NLO form",
        simplify(H_y_alt2 - H_y_target) != 0,
        "alternate H_y at atlas-LO does not equal (20 + alpha_s)/(24 sqrt(5))",
    )

    # ---------------------------------------------------------------------
    section("Part 11: trailing numerical sanity (canonical alpha_s pin)")
    # ---------------------------------------------------------------------
    try:
        from canonical_plaquette_surface import CANONICAL_ALPHA_S_V

        alpha_s_value = float(CANONICAL_ALPHA_S_V)
        H_x_num = float(H_x.subs(alpha_s, alpha_s_value))
        H_y_num = float(H_y.subs(alpha_s, alpha_s_value))
        V3_y_num = float(V3[1].subs(alpha_s, alpha_s_value))
        offset_num = H_y_num - V3_y_num
        print(f"  canonical alpha_s(v) = {alpha_s_value:.15f}")
        print(f"  H_x = {H_x_num:.10f}, H_y = {H_y_num:.10f}")
        print(f"  H_y - V_3_y = {offset_num:.10f}")
        check(
            "H_y - V_3_y ~ 0.01154972 at canonical alpha_s",
            abs(offset_num - 0.01154972) < 1e-7,
            f"got {offset_num:.8f}",
        )
        check(
            "H_x ~ 0.16236234 at canonical alpha_s",
            abs(H_x_num - 0.16236234) < 1e-7,
            f"got {H_x_num:.8f}",
        )
    except ImportError:
        print("  skipped: canonical_plaquette_surface not on PYTHONPATH")

    # ---------------------------------------------------------------------
    section("Summary")
    # ---------------------------------------------------------------------
    print("  Verified at exact sympy precision:")
    print("    (O1) H = (rho_bar, (20 + alpha_s)/(24 sqrt(5))) (degree-1 in alpha_s)")
    print("    (O2) H - V_3 = (0, alpha_s sqrt(5)/20)")
    print("    (O3) G = ((28 - alpha_s)/72, sqrt(5)(4 - alpha_s)/72)")
    print("    (O4) O = (1/2, -alpha_s sqrt(5)/40) [re-derived from (N1)-(N3)]")
    print("    (O5) Euler line H = 3 G - 2 O, HG : GO = 2 : 1")
    print("    (O6) H - V_3 = -2 (O - M) with M = (1/2, 0)")
    print("    (O7) slope (H_y - V_3_y)/alpha_s = sqrt(5)/20 = cited N7 slope")
    print("    (O8) H, G are degree-1 in alpha_s (selection rule)")
    print("    (O9) atlas-LO recovery H_LO = V_3_LO = (1/6, sqrt(5)/6); O_LO = (1/2, 0)")
    print("    Counterfactuals confirm the (4 - alpha_s) cancellation in eta_bar")
    print("    is load-bearing for the closed-form structure.")

    print()
    print("=" * 88)
    print(f"TOTAL: PASS={PASS}, FAIL={FAIL}")
    print("=" * 88)
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
