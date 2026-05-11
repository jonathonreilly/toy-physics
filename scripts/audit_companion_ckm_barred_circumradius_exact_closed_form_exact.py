#!/usr/bin/env python3
"""Exact-symbolic audit-companion runner for
`ckm_barred_circumradius_exact_closed_form_theorem_note_2026-04-25`.

The parent note's load-bearing content is the closed-form derivation that
on the cited NLO Wolfenstein protected-gamma-bar surface

  rho_bar  = (4 - alpha_s) / 24            (cited N1)
  eta_bar  = sqrt(5)(4 - alpha_s) / 24     (cited N2)
  R_b_bar^2 = (4 - alpha_s)^2 / 96         (cited N3)
  tan(gamma_bar) = sqrt(5)                 (cited N4 / N8, alpha_s-protected)
  tan(beta_bar)  = sqrt(5)(4 - alpha_s)/(20 + alpha_s)  (cited N5)
  alpha_bar = pi - gamma_0 - beta_bar      (cited N6 angle sum, with gamma_bar = gamma_0 by N4)

force the named circumradius / circumcenter closed forms

  (C1) R_bar^2     = 1/4 + alpha_s^2 / 320   [exact degree-2 polynomial]
       R_bar^2     = 1/N_pair^2 + alpha_s^2 / [N_pair^6 (N_quark - 1)]
  (C2) R_bar       = (1/2) sqrt(1 + alpha_s^2 / 80)
  (C3) (x_cc, y_cc) = (1/2, -alpha_s sqrt(5)/40)
                    = (1/N_pair, -alpha_s/[N_pair^3 sqrt(N_quark - 1)])
  (C4) R_bar^2     = x_cc^2 + y_cc^2
  (C7) R_bar cos(alpha_bar) = y_cc

The existing primary runner
(`scripts/frontier_ckm_barred_circumradius_exact_closed_form.py`) verifies
these identities at floating-point tolerance using the canonical
numerical `alpha_s(v)`. This Pattern B audit companion adds a
sympy-based exact-symbolic verification:

  (a) treats `alpha_s(v)` as a free positive real symbol so the algebra
      cannot be passing accidentally on a single numerical value;
  (b) imports the upstream cited inputs (N1)-(N6) verbatim;
  (c) verifies (C1) by computing
        4 sin^2(alpha_bar) = 320 / (80 + alpha_s^2)
        R_bar^2 = 1 / [4 sin^2(alpha_bar)] = (80 + alpha_s^2)/320
                 = 1/4 + alpha_s^2 / 320
      with `simplify(LHS - RHS) == 0` parametric in alpha_s;
  (d) verifies (C2) `R_bar = (1/2) sqrt(1 + alpha_s^2/80)` symbolically;
  (e) verifies (C3) the circumcenter coordinates by direct algebra from
      cited (N1), (N2), (N3) and the perpendicular-bisector
      construction;
  (f) verifies (C4) `R_bar^2 = x_cc^2 + y_cc^2` (Pythagorean);
  (g) verifies (C7) `R_bar cos(alpha_bar) = y_cc` (chord-distance);
  (h) verifies the structural-integer factorization
        320 = N_pair^6 (N_quark - 1)
        N_pair^3 sqrt(N_quark - 1) = 40
      at cited N_pair = 2, N_quark = 6;
  (i) provides counterfactual probes confirming the (4 - alpha_s) factor
      cancellation in y_cc is what fixes the linear-in-alpha_s form, and
      that the protected `tan(gamma_bar) = sqrt(5)` is what fixes the
      degree-2 polynomial structure of R_bar^2.

Companion role: Pattern B audit-acceleration only. Not a new claim row,
not a new source note, and no status promotion. The cited inputs
themselves ((N1)-(N6), N_pair = 2, N_quark = 6) are imported from
upstream authority notes and are not re-derived here.
"""

from __future__ import annotations

import sys

try:
    import sympy
    from sympy import Rational, Symbol, simplify, sqrt, cos, atan, expand, together
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
    print("ckm_barred_circumradius_exact_closed_form_theorem_note_2026-04-25")
    print("Goal: sympy-symbolic verification of (C1)-(C4) and (C7) at exact")
    print("precision parametric in alpha_s on the cited NLO protected-gamma-bar surface.")
    print("=" * 88)

    # ---------------------------------------------------------------------
    section("Part 0: symbolic setup and imported cited inputs (N1)-(N6)")
    # ---------------------------------------------------------------------

    alpha_s = Symbol("alpha_s", positive=True, real=True)

    # Cited N1, N2 apex coordinates of the barred unitarity triangle.
    rho_bar = (4 - alpha_s) / Rational(24)
    eta_bar = sqrt(5) * (4 - alpha_s) / Rational(24)

    # Cited N3 side length squared.
    Rb_bar_sq = (4 - alpha_s) ** 2 / Rational(96)

    # Cited N5 protected-gamma-bar tangents.
    tan_beta_bar = sqrt(5) * (4 - alpha_s) / (20 + alpha_s)
    tan_gamma_bar = sqrt(5)  # cited N4

    # Structural counts.
    N_pair = Rational(2)
    N_quark = Rational(6)

    print(f"  symbolic alpha_s(v) = {alpha_s}")
    print(f"  rho_bar           = {rho_bar}")
    print(f"  eta_bar           = {eta_bar}")
    print(f"  R_b_bar^2 (N3)    = {Rb_bar_sq}")
    print(f"  tan(beta_bar) (N5)  = {tan_beta_bar}")
    print(f"  tan(gamma_bar) (N4) = {tan_gamma_bar}")
    print(f"  N_pair = {N_pair}, N_quark = {N_quark}")

    # ---------------------------------------------------------------------
    section("Part 1: derive tan(alpha_bar) = -4 sqrt(5)/alpha_s via tangent-of-sum")
    # ---------------------------------------------------------------------
    # alpha_bar = pi - gamma_bar - beta_bar (N6, with gamma_bar = gamma_0 by N4),
    # so tan(alpha_bar) = -tan(beta_bar + gamma_bar).
    tan_sum_num = tan_beta_bar + tan_gamma_bar
    tan_sum_den = 1 - tan_beta_bar * tan_gamma_bar
    tan_alpha_bar = simplify(-tan_sum_num / tan_sum_den)
    tan_alpha_bar_target = -4 * sqrt(5) / alpha_s

    check(
        "tan(alpha_bar) == -4 sqrt(5)/alpha_s (parametric in alpha_s)",
        simplify(tan_alpha_bar - tan_alpha_bar_target) == 0,
        f"residual = {simplify(tan_alpha_bar - tan_alpha_bar_target)}",
    )

    # ---------------------------------------------------------------------
    section("Part 2: sin^2(alpha_bar), cos^2(alpha_bar) closed forms")
    # ---------------------------------------------------------------------
    # tan^2 = 80/alpha_s^2
    tan_sq = simplify(tan_alpha_bar ** 2)
    check(
        "tan^2(alpha_bar) == 80/alpha_s^2",
        simplify(tan_sq - 80 / alpha_s ** 2) == 0,
        f"residual = {simplify(tan_sq - 80/alpha_s**2)}",
    )

    cos_sq_alpha_bar = simplify(1 / (1 + tan_sq))
    sin_sq_alpha_bar = simplify(1 - cos_sq_alpha_bar)

    cos_sq_target = alpha_s ** 2 / (alpha_s ** 2 + 80)
    sin_sq_target = 80 / (80 + alpha_s ** 2)

    check(
        "cos^2(alpha_bar) == alpha_s^2/(80 + alpha_s^2)",
        simplify(cos_sq_alpha_bar - cos_sq_target) == 0,
        f"residual = {simplify(cos_sq_alpha_bar - cos_sq_target)}",
    )
    check(
        "sin^2(alpha_bar) == 80/(80 + alpha_s^2)",
        simplify(sin_sq_alpha_bar - sin_sq_target) == 0,
        f"residual = {simplify(sin_sq_alpha_bar - sin_sq_target)}",
    )

    # ---------------------------------------------------------------------
    section("Part 3: (C1) R_bar^2 = 1/4 + alpha_s^2/320 via law of sines")
    # ---------------------------------------------------------------------
    # 2 R_bar = 1 / sin(alpha_bar) so R_bar^2 = 1 / (4 sin^2(alpha_bar)).
    R_bar_sq_via_sines = simplify(1 / (4 * sin_sq_alpha_bar))
    R_bar_sq_target = Rational(1, 4) + alpha_s ** 2 / Rational(320)

    check(
        "(C1) R_bar^2 = 1/(4 sin^2 alpha_bar) == 1/4 + alpha_s^2/320 (parametric)",
        simplify(R_bar_sq_via_sines - R_bar_sq_target) == 0,
        f"residual = {simplify(R_bar_sq_via_sines - R_bar_sq_target)}",
    )

    # Structural-integer form: 1/N_pair^2 + alpha_s^2 / (N_pair^6 (N_quark - 1)).
    R_bar_sq_struct = 1 / N_pair ** 2 + alpha_s ** 2 / (N_pair ** 6 * (N_quark - 1))
    check(
        "(C1) R_bar^2 == 1/N_pair^2 + alpha_s^2/[N_pair^6 (N_quark-1)] at N_pair=2, N_quark=6",
        simplify(R_bar_sq_struct - R_bar_sq_target) == 0,
        f"residual = {simplify(R_bar_sq_struct - R_bar_sq_target)}",
    )
    check(
        "structural-integer factorization: N_pair^6 (N_quark - 1) == 320",
        simplify(N_pair ** 6 * (N_quark - 1) - 320) == 0,
        f"value = {N_pair**6 * (N_quark - 1)}",
    )

    # No higher-order terms in alpha_s in R_bar^2 itself (degree 2 polynomial).
    R_bar_sq_poly = sympy.Poly(R_bar_sq_target, alpha_s)
    check(
        "R_bar^2 is a degree-2 polynomial in alpha_s (no alpha_s^3, alpha_s^4, ...)",
        R_bar_sq_poly.degree() == 2,
        f"degree = {R_bar_sq_poly.degree()}, coeffs = {R_bar_sq_poly.all_coeffs()}",
    )

    # ---------------------------------------------------------------------
    section("Part 4: (C2) R_bar = (1/2) sqrt(1 + alpha_s^2/80)")
    # ---------------------------------------------------------------------
    R_bar_target = Rational(1, 2) * sqrt(1 + alpha_s ** 2 / Rational(80))
    R_bar_sq_from_C2 = simplify(R_bar_target ** 2)
    check(
        "(C2) [(1/2) sqrt(1 + alpha_s^2/80)]^2 == R_bar^2 (parametric)",
        simplify(R_bar_sq_from_C2 - R_bar_sq_target) == 0,
        f"residual = {simplify(R_bar_sq_from_C2 - R_bar_sq_target)}",
    )

    # ---------------------------------------------------------------------
    section("Part 5: (C3) circumcenter coordinates")
    # ---------------------------------------------------------------------
    # x_cc = 1/2 (perpendicular bisector of unit base V_1 V_2, alpha_s-independent).
    # y_cc derived from equidistance |O - V_1|^2 = |O - V_3|^2:
    #   y_cc = (R_b_bar^2 - rho_bar) / (2 eta_bar)
    x_cc_target = Rational(1, 2)
    y_cc_target = -alpha_s * sqrt(5) / Rational(40)

    y_cc_from_perp_bisector = simplify((Rb_bar_sq - rho_bar) / (2 * eta_bar))
    check(
        "(C3) y_cc = (R_b_bar^2 - rho_bar)/(2 eta_bar) == -alpha_s sqrt(5)/40 (parametric)",
        simplify(y_cc_from_perp_bisector - y_cc_target) == 0,
        f"residual = {simplify(y_cc_from_perp_bisector - y_cc_target)}",
    )

    # Structural-integer form of y_cc: -alpha_s / [N_pair^3 sqrt(N_quark - 1)].
    y_cc_struct = -alpha_s / (N_pair ** 3 * sqrt(N_quark - 1))
    check(
        "(C3) y_cc == -alpha_s / [N_pair^3 sqrt(N_quark - 1)] at N_pair=2, N_quark=6",
        simplify(y_cc_struct - y_cc_target) == 0,
        f"residual = {simplify(y_cc_struct - y_cc_target)}",
    )

    # x_cc structural form 1/N_pair.
    check(
        "(C3) x_cc == 1/N_pair == 1/2 (alpha_s-independent)",
        simplify(Rational(1) / N_pair - x_cc_target) == 0,
        f"value = {Rational(1)/N_pair}",
    )

    # ---------------------------------------------------------------------
    section("Part 6: (C4) Pythagorean check R_bar^2 = x_cc^2 + y_cc^2")
    # ---------------------------------------------------------------------
    pythag = simplify(x_cc_target ** 2 + y_cc_target ** 2)
    check(
        "(C4) x_cc^2 + y_cc^2 == R_bar^2 (parametric)",
        simplify(pythag - R_bar_sq_target) == 0,
        f"residual = {simplify(pythag - R_bar_sq_target)}",
    )

    # ---------------------------------------------------------------------
    section("Part 7: (C7) R_bar cos(alpha_bar) = y_cc (chord-distance theorem)")
    # ---------------------------------------------------------------------
    # cos(alpha_bar) is negative (alpha_bar > pi/2); take cos = -sqrt(cos^2)
    # to keep the right sign branch.
    cos_alpha_bar_signed = -sqrt(cos_sq_alpha_bar)
    R_bar_cos = simplify(R_bar_target * cos_alpha_bar_signed)
    check(
        "(C7) R_bar * cos(alpha_bar) == y_cc (parametric, signed)",
        simplify(R_bar_cos - y_cc_target) == 0,
        f"residual = {simplify(R_bar_cos - y_cc_target)}",
    )

    # Unsigned chord-distance |y_cc| = R_bar |cos(alpha_bar)|.
    check(
        "(C7) |y_cc| == R_bar * |cos(alpha_bar)| (chord-distance, unsigned)",
        simplify(simplify(R_bar_target ** 2 * cos_sq_alpha_bar) - y_cc_target ** 2) == 0,
        "squared form residual = 0",
    )

    # ---------------------------------------------------------------------
    section("Part 8: chord length 2 R_bar sin(alpha_bar) = 1 (unit-base) ")
    # ---------------------------------------------------------------------
    chord_sq = simplify(4 * R_bar_sq_target * sin_sq_alpha_bar)
    check(
        "[2 R_bar sin(alpha_bar)]^2 == 1 (unit-base length, parametric)",
        simplify(chord_sq - 1) == 0,
        f"residual = {simplify(chord_sq - 1)}",
    )

    # ---------------------------------------------------------------------
    section("Part 9: counterfactual probes")
    # ---------------------------------------------------------------------
    # (4 - alpha_s) cancellation in y_cc is load-bearing: if eta_bar were
    # not the matched form sqrt(5)(4-alpha_s)/24, y_cc would not be
    # exactly linear in alpha_s.
    eta_bar_alt = sqrt(5) * Rational(4) / Rational(24)  # drops the (4-alpha_s) term
    y_cc_alt = simplify((Rb_bar_sq - rho_bar) / (2 * eta_bar_alt))
    check(
        "counterfactual: dropping (4-alpha_s) from eta_bar breaks the linear y_cc form",
        simplify(y_cc_alt - y_cc_target) != 0,
        f"alt y_cc simplifies to {simplify(y_cc_alt)}",
    )

    # The protected tan(gamma_bar) = sqrt(5) is what gives the 4 sqrt(5)
    # in tan(alpha_bar). If tan(gamma_bar) were instead 1 (no protection),
    # the cancellation would not produce a single alpha_s monomial.
    tan_gamma_alt = Rational(1)
    tan_sum_num_alt = tan_beta_bar + tan_gamma_alt
    tan_sum_den_alt = 1 - tan_beta_bar * tan_gamma_alt
    tan_alpha_alt = simplify(-tan_sum_num_alt / tan_sum_den_alt)
    check(
        "counterfactual: at tan(gamma_bar) = 1, tan(alpha_bar) is no longer -4 sqrt(5)/alpha_s",
        simplify(tan_alpha_alt - tan_alpha_bar_target) != 0,
        "tan_alpha (with tan_gamma=1) does not collapse to single alpha_s monomial",
    )

    # ---------------------------------------------------------------------
    section("Part 10: trailing numerical sanity (canonical alpha_s pin)")
    # ---------------------------------------------------------------------
    try:
        from canonical_plaquette_surface import CANONICAL_ALPHA_S_V

        alpha_s_value = float(CANONICAL_ALPHA_S_V)
        R_bar_sq_num = float(R_bar_sq_target.subs(alpha_s, alpha_s_value))
        R_bar_num = R_bar_sq_num ** 0.5
        y_cc_num = float(y_cc_target.subs(alpha_s, alpha_s_value))
        print(f"  canonical alpha_s(v) = {alpha_s_value:.15f}")
        print(f"  R_bar^2 = {R_bar_sq_num:.12f}")
        print(f"  R_bar   = {R_bar_num:.12f}")
        print(f"  y_cc    = {y_cc_num:.12f}")
        check(
            "R_bar^2 ~ 0.250033349 at canonical alpha_s",
            abs(R_bar_sq_num - 0.250033349) < 1e-7,
            f"got {R_bar_sq_num:.9f}",
        )
        check(
            "y_cc ~ -5.7748 e-3 at canonical alpha_s",
            abs(y_cc_num - (-5.7748e-3)) < 1e-5,
            f"got {y_cc_num:.6e}",
        )
    except ImportError:
        print("  skipped: canonical_plaquette_surface not on PYTHONPATH")

    # ---------------------------------------------------------------------
    section("Summary")
    # ---------------------------------------------------------------------
    print("  Verified at exact sympy precision:")
    print("    tan(alpha_bar) == -4 sqrt(5)/alpha_s (from N5, N4, N6)")
    print("    sin^2(alpha_bar), cos^2(alpha_bar) closed forms")
    print("    (C1) R_bar^2 == 1/4 + alpha_s^2/320 (degree-2 polynomial)")
    print("    (C2) R_bar   == (1/2) sqrt(1 + alpha_s^2/80)")
    print("    (C3) (x_cc, y_cc) == (1/2, -alpha_s sqrt(5)/40)")
    print("    (C4) R_bar^2 == x_cc^2 + y_cc^2 (Pythagorean)")
    print("    (C7) R_bar cos(alpha_bar) == y_cc (chord-distance)")
    print("    Structural-integer factorization N_pair^6 (N_quark - 1) = 320")
    print("    Counterfactuals confirm (4 - alpha_s) cancellation and tan(gamma_bar)=sqrt(5)")
    print("    are individually load-bearing for the closed-form structure.")

    print()
    print("=" * 88)
    print(f"TOTAL: PASS={PASS}, FAIL={FAIL}")
    print("=" * 88)
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
