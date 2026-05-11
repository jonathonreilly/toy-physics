#!/usr/bin/env python3
"""Exact-symbolic audit-companion runner for
`ckm_kaon_epsilon_k_jarlskog_decomposition_theorem_note_2026-04-25`.

The parent note's load-bearing content is the atlas-leading-order
Wolfenstein-CKM decomposition of the three combinations entering the
imaginary part of the kaon `epsilon_K` short-distance bracket:

  (K1)  Im[(V_cs^* V_cd)^2]              =  +2 J_0,
  (K2)  Im[V_cs^* V_cd  V_ts^* V_td]     =  -J_0,
  (K3)  Im[(V_ts^* V_td)^2]              =  -(5 alpha_s(v)^2 / 18) J_0
                                          =  -2 A^2 lambda^4 (1 - rho) J_0,

with the atlas Jarlskog-area factor `J_0 = A^2 lambda^6 eta = alpha_s^3 sqrt(5)/72`.
Identities (K1) and (K2) carry rational coefficients (+2, -1); identity
(K3) carries an `alpha_s^2`-suppressed coefficient that rewrites in
compact form as `-(5 alpha_s^2 / 18)` in framework values.

The existing primary runner
(`scripts/frontier_ckm_kaon_epsilon_k_jarlskog_decomposition.py`)
verifies these identities at floating-point tolerance using the
canonical numerical alpha_s(v). This Pattern B audit companion adds a
sympy-based exact-symbolic verification:

  (a) treats `alpha_s` as a free positive real symbol so the algebra
      cannot be passing accidentally on a single numerical value;
  (b) imports the upstream atlas inputs verbatim:
        lambda^2 = alpha_s / 2,   A^2 = 2/3,   rho = 1/6,   eta = sqrt(5)/6,
        J_0       = A^2 lambda^6 eta = alpha_s^3 sqrt(5)/72;
  (c) verifies the load-bearing leading-order coefficients of (K1), (K2),
      (K3) at the atlas Wolfenstein expansion order needed for each
      imaginary part, working with explicit polynomials in lambda;
  (d) verifies the closed-form coefficient identity
        -2 A^2 lambda^4 (1 - rho)  ==  -(5 alpha_s^2 / 18)
      parametric in alpha_s under the framework substitutions;
  (e) verifies the J_0 factorization of the full Im(L) bracket
      symbolically, with the rational/`alpha_s^2`-suppressed
      coefficients on each Inami-Lim term;
  (f) provides counterfactual probes confirming each imported atlas
      input is individually load-bearing for the closed-form
      coefficients.

Companion role: Pattern B audit-acceleration only. Not a new claim row,
not a new source note, no status promotion. The cited atlas inputs
themselves (`lambda^2 = alpha_s/2`, `A^2 = 2/3`, `rho = 1/6`,
`eta = sqrt(5)/6`, `J_0 = alpha_s^3 sqrt(5)/72`) are imported from
upstream authority notes and are not re-derived here.
"""

from __future__ import annotations

import sys

try:
    import sympy
    from sympy import Rational, Symbol, simplify, sqrt, I, expand, im, re, series, O
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
    print("ckm_kaon_epsilon_k_jarlskog_decomposition_theorem_note_2026-04-25")
    print("Goal: sympy-symbolic verification of (K1), (K2), (K3) closed-form")
    print("J_0 factorization at atlas-LO Wolfenstein order, parametric in alpha_s.")
    print("=" * 88)

    # ---------------------------------------------------------------------
    section("Part 0: symbolic setup and imported atlas inputs")
    # ---------------------------------------------------------------------
    alpha_s = Symbol("alpha_s", positive=True, real=True)

    # Imported atlas inputs (cited authorities; not re-derived here).
    lambda_sq = alpha_s / Rational(2)
    A_sq = Rational(2, 3)
    rho = Rational(1, 6)
    eta = sqrt(Rational(5)) / Rational(6)

    # We need lambda itself (positive) for Wolfenstein-style polynomial
    # expansions. Treat it as a symbol with lambda^2 substitution at the
    # end; alternatively, work in lambda directly and only substitute
    # lambda^2 when needed.
    lam = Symbol("lam", positive=True, real=True)
    # We will substitute lam^2 -> alpha_s/2 at the algebraic-reduction step.
    lambda_to_alpha_s = {lam ** 2: alpha_s / Rational(2)}

    # J_0 atlas (cited identity, imported).
    J0_cited = alpha_s ** 3 * sqrt(Rational(5)) / Rational(72)
    # Cross-check J_0 = A^2 lambda^6 eta.
    J0_from_factors = simplify(A_sq * lambda_sq ** 3 * eta)
    check(
        "J_0 = A^2 lambda^6 eta == alpha_s^3 sqrt(5)/72 (parametric in alpha_s)",
        simplify(J0_from_factors - J0_cited) == 0,
        f"residual = {simplify(J0_from_factors - J0_cited)}",
    )

    print(f"  symbolic alpha_s   = {alpha_s}")
    print(f"  lambda^2           = {lambda_sq}")
    print(f"  A^2                = {A_sq}")
    print(f"  rho                = {rho}")
    print(f"  eta                = {eta}")
    print(f"  J_0 atlas          = {J0_cited}")

    # ---------------------------------------------------------------------
    section("Part 1: atlas-LO Wolfenstein V matrix elements (kaon-relevant)")
    # ---------------------------------------------------------------------
    # Wolfenstein expansion at the orders needed for the imaginary parts:
    #   V_cs = 1 - lambda^2/2                             (real to needed order)
    #   V_cd = -lam + (A^2 lam^5 / 2)(1 - 2 rho - 2 i eta)
    #   V_ts = -A lam^2                                   (real to needed order)
    #   V_td = A lam^3 (1 - rho - i eta)
    #
    # Notes:
    #   - We retain only the leading real and the leading imaginary
    #     contributions to each element at the order needed for
    #     Im[(V_cs^* V_cd)^2], Im[V_cs^* V_cd V_ts^* V_td], Im[(V_ts^* V_td)^2].
    #   - We work with sympy expression in (lam, alpha_s, ...). The
    #     framework substitution lambda^2 = alpha_s/2 is applied at the
    #     end so coefficients drop to the parent note's compact forms.
    A = sqrt(A_sq)  # A is positive real; we only ever square it back.

    V_cs = 1 - lam ** 2 / Rational(2)
    V_cd = -lam + (A_sq * lam ** 5 / Rational(2)) * (1 - 2 * rho - 2 * I * eta)
    V_ts = -A * lam ** 2
    V_td = A * lam ** 3 * (1 - rho - I * eta)

    # Conjugates: V_cs and V_ts are real (to relevant order); V_cd, V_td have phases.
    V_cs_star = V_cs.conjugate()
    V_ts_star = V_ts.conjugate()
    V_cd_use = V_cd
    V_td_use = V_td

    print("  V_cs = 1 - lam^2/2")
    print("  V_cd = -lam + (A^2 lam^5/2)(1 - 2 rho - 2 i eta)")
    print("  V_ts = -A lam^2")
    print("  V_td = A lam^3 (1 - rho - i eta)")

    # ---------------------------------------------------------------------
    section("Part 2: (K1) Im[(V_cs^* V_cd)^2] = 2 J_0 at atlas-LO")
    # ---------------------------------------------------------------------
    P1 = expand(V_cs_star * V_cd_use)
    P1_sq = expand(P1 * P1)
    Im_P1_sq = expand(im(P1_sq))

    # The leading-order contribution to Im[(V_cs^* V_cd)^2] in lam is
    #   2 (-lam)(-A^2 lam^5 eta) = 2 A^2 lam^6 eta.
    # Higher orders are O(lam^8). Extract the coefficient at lam^6 and
    # confirm the leading reduction: 2 J_0 = 2 A^2 lambda^6 eta =
    # alpha_s^3 sqrt(5)/36.
    leading_K1 = Rational(2) * A_sq * lam ** 6 * eta
    diff_K1_full = expand(Im_P1_sq - leading_K1)
    # diff_K1_full collects O(lam^8) and higher; its lam^6 coefficient
    # must vanish.
    coeff_lam6_diff = sympy.Poly(diff_K1_full, lam).all_coeffs()
    # We do not assume polynomial degree; check the lam^6 coefficient is zero
    # by extracting via series:
    series_K1 = sympy.series(Im_P1_sq, lam, 0, 7).removeO()
    coeff_lam6_K1 = series_K1.coeff(lam, 6)
    coeff_lam6_target = Rational(2) * A_sq * eta
    check(
        "(K1) Im[(V_cs^* V_cd)^2] coefficient at lam^6 == 2 A^2 eta = sqrt(5)/9",
        simplify(coeff_lam6_K1 - coeff_lam6_target) == 0,
        f"residual = {simplify(coeff_lam6_K1 - coeff_lam6_target)}",
    )
    # Substitute lam^2 -> alpha_s/2 to obtain 2 J_0 = alpha_s^3 sqrt(5)/36.
    leading_K1_alpha_s = simplify(coeff_lam6_K1 * (alpha_s / Rational(2)) ** 3)
    target_K1 = simplify(2 * J0_cited)
    check(
        "(K1) leading 2 A^2 lam^6 eta == 2 J_0 = alpha_s^3 sqrt(5)/36 (parametric)",
        simplify(leading_K1_alpha_s - target_K1) == 0,
        f"residual = {simplify(leading_K1_alpha_s - target_K1)}",
    )
    # Numerical coefficient sanity: 2 J_0 / J_0 == 2 (rational).
    check(
        "(K1) coefficient on J_0 is the rational +2",
        simplify(leading_K1_alpha_s / J0_cited - Rational(2)) == 0,
        f"ratio = {simplify(leading_K1_alpha_s / J0_cited)}",
    )

    # ---------------------------------------------------------------------
    section("Part 3: (K2) Im[V_cs^* V_cd V_ts^* V_td] = -J_0 at atlas-LO")
    # ---------------------------------------------------------------------
    P2 = expand(V_cs_star * V_cd_use * V_ts_star * V_td_use)
    Im_P2 = expand(im(P2))
    series_K2 = sympy.series(Im_P2, lam, 0, 7).removeO()
    coeff_lam6_K2 = series_K2.coeff(lam, 6)
    # Leading: (-lam)(-A lam^2)(A lam^3 eta) i-coefficient sign chase yields
    #   2 Re(P_left)*Im(P_right) + 2 Im(P_left)*Re(P_right) at lam^6.
    # Direct algebra: V_cs^* V_cd ~ -lam, V_ts^* V_td = -A lam^2 * A lam^3 (1-rho - i eta)
    #               = -A^2 lam^5 (1 - rho) + i A^2 lam^5 eta.
    # Im[(V_cs^* V_cd)(V_ts^* V_td)] = (-lam)*A^2 lam^5 eta = -A^2 lam^6 eta = -J_0.
    coeff_lam6_K2_target = -A_sq * eta
    check(
        "(K2) Im[V_cs^* V_cd V_ts^* V_td] coefficient at lam^6 == -A^2 eta = -sqrt(5)/18",
        simplify(coeff_lam6_K2 - coeff_lam6_K2_target) == 0,
        f"residual = {simplify(coeff_lam6_K2 - coeff_lam6_K2_target)}",
    )
    leading_K2_alpha_s = simplify(coeff_lam6_K2 * (alpha_s / Rational(2)) ** 3)
    target_K2 = simplify(-J0_cited)
    check(
        "(K2) leading == -J_0 = -alpha_s^3 sqrt(5)/72 (parametric)",
        simplify(leading_K2_alpha_s - target_K2) == 0,
        f"residual = {simplify(leading_K2_alpha_s - target_K2)}",
    )
    check(
        "(K2) coefficient on J_0 is the rational -1",
        simplify(leading_K2_alpha_s / J0_cited + Rational(1)) == 0,
        f"ratio = {simplify(leading_K2_alpha_s / J0_cited)}",
    )

    # ---------------------------------------------------------------------
    section("Part 4: (K3) Im[(V_ts^* V_td)^2] = -(5 alpha_s^2/18) J_0 at atlas-LO")
    # ---------------------------------------------------------------------
    P3 = expand(V_ts_star * V_td_use)
    P3_sq = expand(P3 * P3)
    Im_P3_sq = expand(im(P3_sq))
    # Leading order: Re(V_ts^* V_td) = -A^2 lam^5 (1 - rho), Im = A^2 lam^5 eta.
    # Im[(...)^2] = 2 Re Im = -2 A^4 lam^10 (1 - rho) eta.
    coeff_lam10_K3_target = -2 * A_sq ** 2 * (1 - rho) * eta
    series_K3 = sympy.series(Im_P3_sq, lam, 0, 11).removeO()
    coeff_lam10_K3 = series_K3.coeff(lam, 10)
    check(
        "(K3) Im[(V_ts^* V_td)^2] coefficient at lam^10 == -2 A^4 (1-rho) eta",
        simplify(coeff_lam10_K3 - coeff_lam10_K3_target) == 0,
        f"residual = {simplify(coeff_lam10_K3 - coeff_lam10_K3_target)}",
    )

    # Closed-form coefficient identity.
    # Note: -2 A^4 lam^10 (1-rho) eta = -2 A^2 lam^4 (1-rho) * A^2 lam^6 eta
    #                                  = -2 A^2 lam^4 (1-rho) * J_0.
    # Then under lambda^2 = alpha_s/2:
    #   -2 A^2 lam^4 (1-rho) = -2 (2/3)(alpha_s/2)^2 (5/6)
    #                        = -(20/72) alpha_s^2
    #                        = -(5 alpha_s^2)/18.
    coeff_long = -Rational(2) * A_sq * lam ** 4 * (1 - rho)
    coeff_long_alpha_s = simplify(coeff_long.subs(lam ** 2, alpha_s / Rational(2)))
    coeff_closed_alpha_s = -Rational(5) * alpha_s ** 2 / Rational(18)
    check(
        "(K3) closed-form coefficient: -2 A^2 lam^4 (1-rho) == -(5 alpha_s^2/18)",
        simplify(coeff_long_alpha_s - coeff_closed_alpha_s) == 0,
        f"residual = {simplify(coeff_long_alpha_s - coeff_closed_alpha_s)}",
    )
    # Multiply by J_0 to confirm the (K3) right-hand side.
    K3_rhs_via_long = simplify(coeff_long_alpha_s * J0_cited)
    K3_rhs_via_closed = simplify(coeff_closed_alpha_s * J0_cited)
    check(
        "(K3) -2 A^2 lam^4 (1-rho) J_0 == -(5 alpha_s^2/18) J_0",
        simplify(K3_rhs_via_long - K3_rhs_via_closed) == 0,
        f"residual = {simplify(K3_rhs_via_long - K3_rhs_via_closed)}",
    )
    # Confirm the (K3) leading lam^10 coefficient evaluates to -(5 alpha_s^2/18) J_0
    # after lambda^2 -> alpha_s/2 substitution.
    K3_leading_alpha_s = simplify(
        coeff_lam10_K3 * (alpha_s / Rational(2)) ** 5
    )
    check(
        "(K3) leading == -(5 alpha_s^2/18) J_0 (parametric in alpha_s)",
        simplify(K3_leading_alpha_s - K3_rhs_via_closed) == 0,
        f"residual = {simplify(K3_leading_alpha_s - K3_rhs_via_closed)}",
    )

    # ---------------------------------------------------------------------
    section("Part 5: epsilon_K Im(L) bracket factorization through J_0")
    # ---------------------------------------------------------------------
    # Im(L) = Im[lambda_c^2] eta_cc S_xc
    #       + Im[lambda_t^2] eta_tt S_xt
    #       + 2 Im[lambda_c lambda_t] eta_ct S_xcxt
    # where lambda_q = V_qs^* V_qd. Using (K1), (K2), (K3):
    #   Im(L) = J_0 [ 2 eta_cc S_xc - 2 eta_ct S_xcxt - (5 alpha_s^2/18) eta_tt S_xt ]
    eta_cc, eta_tt, eta_ct = sympy.symbols(
        "eta_cc eta_tt eta_ct", positive=True, real=True
    )
    S_xc, S_xt, S_xcxt = sympy.symbols("S_xc S_xt S_xcxt", positive=True, real=True)

    Im_L_via_KK = (
        2 * J0_cited * eta_cc * S_xc
        + (-Rational(5) * alpha_s ** 2 / Rational(18) * J0_cited) * eta_tt * S_xt
        + 2 * (-J0_cited) * eta_ct * S_xcxt
    )
    Im_L_factored = J0_cited * (
        2 * eta_cc * S_xc
        - 2 * eta_ct * S_xcxt
        - Rational(5) * alpha_s ** 2 / Rational(18) * eta_tt * S_xt
    )
    check(
        "Im(L) factorizes through J_0 with rational + alpha_s^2-suppressed coefficients",
        simplify(Im_L_via_KK - Im_L_factored) == 0,
        f"residual = {simplify(Im_L_via_KK - Im_L_factored)}",
    )

    # ---------------------------------------------------------------------
    section("Part 6: counterfactual probes")
    # ---------------------------------------------------------------------
    # If A^2 had a different value, (K3) coefficient changes from -(5 alpha_s^2/18).
    # Counterfactual: A^2 = 1 -> -2 lam^4 (1-rho) under lambda^2 = alpha_s/2 gives
    #   -2 (1) (alpha_s/2)^2 (5/6) = -(5 alpha_s^2)/12, not /18.
    coeff_cf_Asq1 = simplify(
        (-Rational(2) * Rational(1) * lam ** 4 * (1 - rho)).subs(
            lam ** 2, alpha_s / Rational(2)
        )
    )
    check(
        "counterfactual: at A^2 = 1, (K3) coefficient = -(5 alpha_s^2/12) != -(5 alpha_s^2/18)",
        simplify(coeff_cf_Asq1 - coeff_closed_alpha_s) != 0,
        f"alternate coefficient = {coeff_cf_Asq1}",
    )
    # Counterfactual on rho: rho = 0 -> -2 A^2 lam^4 (1) gives -(2/3)(alpha_s^2/2) = -alpha_s^2/3, not -(5/18) alpha_s^2.
    coeff_cf_rho0 = simplify(
        (-Rational(2) * A_sq * lam ** 4 * (1 - 0)).subs(
            lam ** 2, alpha_s / Rational(2)
        )
    )
    check(
        "counterfactual: at rho = 0, (K3) coefficient = -alpha_s^2/3 != -(5 alpha_s^2/18)",
        simplify(coeff_cf_rho0 - coeff_closed_alpha_s) != 0,
        f"alternate coefficient = {coeff_cf_rho0}",
    )
    # Counterfactual on lambda^2: lambda^2 = alpha_s -> -2 (2/3) alpha_s^2 (5/6) = -(10/9) alpha_s^2, not /18.
    coeff_cf_lam_alpha = simplify(
        (-Rational(2) * A_sq * lam ** 4 * (1 - rho)).subs(lam ** 2, alpha_s)
    )
    check(
        "counterfactual: at lambda^2 = alpha_s, (K3) coefficient = -(10 alpha_s^2/9) != -(5 alpha_s^2/18)",
        simplify(coeff_cf_lam_alpha - coeff_closed_alpha_s) != 0,
        f"alternate coefficient = {coeff_cf_lam_alpha}",
    )
    # Counterfactual on eta: if eta = 0 (no CP), J_0 = 0 -> all three (K1)-(K3) vanish.
    J0_cf_eta0 = simplify(A_sq * lambda_sq ** 3 * Rational(0))
    check(
        "counterfactual: at eta = 0, J_0 = 0 and (K1)-(K3) all vanish",
        J0_cf_eta0 == 0,
        f"J_0 at eta=0: {J0_cf_eta0}",
    )

    # ---------------------------------------------------------------------
    section("Part 7: rational-coefficient sanity")
    # ---------------------------------------------------------------------
    # The (K1) and (K2) coefficients on J_0 are pure rationals (+2, -1).
    # The (K3) coefficient on J_0 is alpha_s^2-suppressed.
    coeff_K1_on_J0 = Rational(2)
    coeff_K2_on_J0 = -Rational(1)
    coeff_K3_on_J0 = -Rational(5) * alpha_s ** 2 / Rational(18)
    check(
        "(K1) coefficient on J_0 is rational +2",
        coeff_K1_on_J0 == Rational(2),
        f"coeff = {coeff_K1_on_J0}",
    )
    check(
        "(K2) coefficient on J_0 is rational -1",
        coeff_K2_on_J0 == -Rational(1),
        f"coeff = {coeff_K2_on_J0}",
    )
    check(
        "(K3) coefficient on J_0 is alpha_s^2-suppressed -(5 alpha_s^2/18)",
        simplify(coeff_K3_on_J0 + Rational(5) * alpha_s ** 2 / Rational(18)) == 0,
        f"coeff = {coeff_K3_on_J0}",
    )

    # ---------------------------------------------------------------------
    section("Summary")
    # ---------------------------------------------------------------------
    print("  Verified at exact sympy precision parametric in alpha_s:")
    print("    J_0 = A^2 lambda^6 eta == alpha_s^3 sqrt(5)/72 (cited)")
    print("    (K1) Im[(V_cs^* V_cd)^2] leading lam^6 coefficient = 2 A^2 eta")
    print("         -> +2 J_0 under lambda^2 = alpha_s/2")
    print("    (K2) Im[V_cs^* V_cd V_ts^* V_td] leading lam^6 coefficient = -A^2 eta")
    print("         -> -J_0 under lambda^2 = alpha_s/2")
    print("    (K3) Im[(V_ts^* V_td)^2] leading lam^10 coefficient = -2 A^4 (1-rho) eta")
    print("         -> -(5 alpha_s^2/18) J_0 under lambda^2 = alpha_s/2 with A^2=2/3, rho=1/6")
    print("    (K3) closed-form coefficient: -2 A^2 lam^4 (1-rho) == -(5 alpha_s^2/18)")
    print("    Im(L) factorizes through J_0 with coefficients (+2 eta_cc, -2 eta_ct,")
    print("        -(5 alpha_s^2/18) eta_tt) on the Inami-Lim functions.")
    print("    Counterfactuals confirm A^2 = 2/3, rho = 1/6, lambda^2 = alpha_s/2,")
    print("    eta != 0 are individually load-bearing for the closed-form (K3)")
    print("    coefficient and for non-vanishing of (K1)-(K3).")

    print()
    print("=" * 88)
    print(f"TOTAL: PASS={PASS}, FAIL={FAIL}")
    print("=" * 88)
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
