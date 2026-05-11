#!/usr/bin/env python3
"""Exact-symbolic audit-companion runner for
`ckm_third_row_magnitudes_theorem_note_2026-04-24`.

The parent note's load-bearing content is the algebraic-substitution claim
that the imported atlas inputs

  lambda^2 = alpha_s(v) / 2,
  A^2      = 2 / 3,
  rho      = 1 / 6,
  eta^2    = 5 / 36,

force the closed-form atlas-leading third-row magnitude identities

  (R1) |V_td|_0^2 = (5 / 72) alpha_s(v)^3,
  (R2) |V_ts|_0^2 = (1 / 6) alpha_s(v)^2,
  (R3) |V_tb|_0^2 = 1 - |V_td|_0^2 - |V_ts|_0^2.

The existing primary runner
(`scripts/frontier_ckm_third_row_magnitudes.py`) verifies these identities
at floating-point tolerance using the canonical numerical `alpha_s(v)`
and at `Fraction`-precision rational coefficients. This Pattern B audit
companion adds a `sympy`-based exact-symbolic verification:

  (a) treats `alpha_s(v)` as a free positive real symbol so the algebra
      cannot be passing accidentally on a single numerical value;
  (b) imports the upstream atlas inputs verbatim:
        `lambda^2 = alpha_s(v) / 2`,
        `A^2      = 2 / 3`,
        `rho      = 1 / 6`,
        `eta^2    = 5 / 36`;
  (c) verifies the load-bearing Thales-style distance reduction
        `(1 - rho)^2 + eta^2 == 5 / 6`
      as an exact `sympy.Rational` identity;
  (d) verifies (R1), (R2), (R3) symbolically:
        (R1) `A^2 lambda^6 ((1 - rho)^2 + eta^2) == (5 / 72) alpha_s(v)^3`,
        (R2) `A^2 lambda^4 == alpha_s(v)^2 / 6`,
        (R3) `1 - |V_td|_0^2 - |V_ts|_0^2 == 1 - alpha_s(v)^2/6 - 5 alpha_s(v)^3/72`;
  (e) verifies the Wolfenstein-A-form reduction
        `A^2 lambda^6 (1 - rho) == (5 / 72) alpha_s(v)^3`
      (i.e. the Thales identity `(1 - rho)^2 + eta^2 == 1 - rho` collapses
      the V_td distance factor symbolically);
  (f) verifies the named cross-identities the note tabulates:
        `|V_ts|_0^2 == |V_cb|_0^2 == alpha_s(v)^2 / 6`,
        `|V_td|_0^2 / |V_ub|_0^2 == 5`;
  (g) provides counterfactual probes confirming the 5/72 coefficient is
      forced by the imported eta^2 = 5/36 (substituting eta^2 = 0 collapses
      |V_td|_0^2 to alpha_s^3/72 instead of 5 alpha_s^3/72) and the 1/6
      coefficient on |V_ts|_0^2 is forced by A^2 = 2/3 (substituting
      A^2 = 1 collapses to alpha_s^2/4 instead of alpha_s^2/6).

Companion role: Pattern B audit-acceleration only. Not a new claim row,
not a new source note, and no status promotion. The cited atlas inputs
themselves (`lambda^2 = alpha_s(v)/2`, `A^2 = 2/3`, `rho = 1/6`,
`eta^2 = 5/36`, `(1-rho)^2 + eta^2 = 5/6`) are imported from upstream
authority notes and are not re-derived here. The numerical pin of
`alpha_s(v)` only enters the trailing sanity check, which is not
load-bearing for the algebra.
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
    print("ckm_third_row_magnitudes_theorem_note_2026-04-24")
    print("Goal: sympy-symbolic verification of (R1), (R2), (R3) and the named")
    print("cross-identities |V_ts|_0^2 = |V_cb|_0^2 and |V_td|_0^2 / |V_ub|_0^2 = 5")
    print("at exact precision over a free symbolic alpha_s(v).")
    print("=" * 88)

    # ---------------------------------------------------------------------
    section("Part 0: symbolic setup and imported atlas inputs")
    # ---------------------------------------------------------------------

    # alpha_s(v) is a free positive real symbol; the third-row identities
    # must hold for ARBITRARY positive real alpha_s, not just the canonical
    # numerical pin. The latter only appears in the trailing sanity check.
    alpha_s = Symbol("alpha_s", positive=True, real=True)

    # Imported atlas inputs (cited authorities; not re-derived here):
    #   lambda^2 = alpha_s(v) / 2          (Wolfenstein lambda/A note)
    #   A^2      = 2 / 3                   (Wolfenstein lambda/A note)
    #   rho      = 1 / 6                   (CKM CP-phase identity note)
    #   eta^2    = 5 / 36                  (CKM CP-phase identity note)
    lambda_sq = alpha_s / 2
    A_sq = Rational(2, 3)
    rho = Rational(1, 6)
    eta_sq = Rational(5, 36)

    print(f"  symbolic alpha_s(v) = {alpha_s}")
    print(f"  lambda^2 = {lambda_sq}")
    print(f"  A^2      = {A_sq}")
    print(f"  rho      = {rho}")
    print(f"  eta^2    = {eta_sq}")

    # ---------------------------------------------------------------------
    section("Part 1: cited Thales/distance reduction (1 - rho)^2 + eta^2 = 5/6")
    # ---------------------------------------------------------------------
    # The third-row V_td factor is A^2 lambda^6 [(1-rho)^2 + eta^2]. The note's
    # load-bearing algebra reduces (1-rho)^2 + eta^2 to 5/6 exactly via the
    # imported (rho, eta^2) atlas values. Verify symbolically.
    distance_sq = (1 - rho) ** 2 + eta_sq
    target_distance = Rational(5, 6)

    check(
        "(1 - rho)^2 = 25/36 (rho = 1/6)",
        simplify((1 - rho) ** 2 - Rational(25, 36)) == 0,
        f"sympy reduces (1 - 1/6)^2 - 25/36 to {simplify((1 - rho) ** 2 - Rational(25, 36))}",
    )

    check(
        "Thales-style distance: (1 - rho)^2 + eta^2 == 5/6 (exact rational)",
        simplify(distance_sq - target_distance) == 0,
        f"residual = {simplify(distance_sq - target_distance)}",
    )

    # Cross-check: (1 - rho)^2 + eta^2 == 1 - rho is the Wolfenstein-A
    # right-angle Thales identity. At rho = 1/6, both sides equal 5/6.
    thales_rhs = 1 - rho
    check(
        "Wolfenstein-A Thales identity: (1 - rho)^2 + eta^2 == 1 - rho",
        simplify(distance_sq - thales_rhs) == 0,
        f"residual = {simplify(distance_sq - thales_rhs)}",
    )

    # ---------------------------------------------------------------------
    section("Part 2: (R1) |V_td|_0^2 = (5/72) alpha_s(v)^3 exact-symbolic")
    # ---------------------------------------------------------------------
    # |V_td|_0^2 = A^2 lambda^6 ((1-rho)^2 + eta^2)
    #            = (2/3) (alpha_s/2)^3 (5/6)
    #            = (2/3)(1/8)(5/6) alpha_s^3
    #            = (10/144) alpha_s^3
    #            = (5/72) alpha_s^3.
    Vtd0_sq_full = A_sq * lambda_sq**3 * distance_sq
    Vtd0_sq_target = Rational(5, 72) * alpha_s**3

    check(
        "(R1) |V_td|_0^2 == (5/72) alpha_s(v)^3 (parametric in alpha_s)",
        simplify(Vtd0_sq_full - Vtd0_sq_target) == 0,
        f"residual = {simplify(Vtd0_sq_full - Vtd0_sq_target)}",
    )

    # Same identity reached through the Wolfenstein-A Thales reduction
    # (1 - rho)^2 + eta^2 -> 1 - rho. At rho = 1/6 this gives 5/6 again.
    Vtd0_via_thales = A_sq * lambda_sq**3 * (1 - rho)
    check(
        "(R1) via Thales reduction: A^2 lambda^6 (1 - rho) == (5/72) alpha_s(v)^3",
        simplify(Vtd0_via_thales - Vtd0_sq_target) == 0,
        f"residual = {simplify(Vtd0_via_thales - Vtd0_sq_target)}",
    )

    # The 5/72 coefficient must be free of any unsubstituted symbols other
    # than alpha_s; check that |V_td|_0^2 / alpha_s^3 simplifies to a pure
    # rational.
    coeff_R1 = simplify(Vtd0_sq_full / alpha_s**3)
    check(
        "(R1) coefficient is the pure rational 5/72",
        coeff_R1 == Rational(5, 72),
        f"coefficient = {coeff_R1}",
    )

    # ---------------------------------------------------------------------
    section("Part 3: (R2) |V_ts|_0^2 = alpha_s(v)^2 / 6 exact-symbolic")
    # ---------------------------------------------------------------------
    # |V_ts|_0^2 = A^2 lambda^4
    #            = (2/3)(alpha_s/2)^2
    #            = (2/3)(1/4) alpha_s^2
    #            = alpha_s^2 / 6.
    Vts0_sq_full = A_sq * lambda_sq**2
    Vts0_sq_target = alpha_s**2 / 6

    check(
        "(R2) |V_ts|_0^2 == alpha_s(v)^2 / 6 (parametric in alpha_s)",
        simplify(Vts0_sq_full - Vts0_sq_target) == 0,
        f"residual = {simplify(Vts0_sq_full - Vts0_sq_target)}",
    )

    coeff_R2 = simplify(Vts0_sq_full / alpha_s**2)
    check(
        "(R2) coefficient is the pure rational 1/6",
        coeff_R2 == Rational(1, 6),
        f"coefficient = {coeff_R2}",
    )

    # ---------------------------------------------------------------------
    section("Part 4: (R3) |V_tb|_0^2 = 1 - |V_td|_0^2 - |V_ts|_0^2 unitarity completion")
    # ---------------------------------------------------------------------
    # By third-row unitarity at atlas-leading order,
    #   |V_tb|_0^2 = 1 - |V_td|_0^2 - |V_ts|_0^2
    #              = 1 - (5/72) alpha_s^3 - alpha_s^2 / 6.
    Vtb0_sq_full = 1 - Vtd0_sq_full - Vts0_sq_full
    Vtb0_sq_target = 1 - alpha_s**2 / 6 - Rational(5, 72) * alpha_s**3

    check(
        "(R3) |V_tb|_0^2 == 1 - alpha_s^2/6 - 5 alpha_s^3/72 (parametric in alpha_s)",
        simplify(Vtb0_sq_full - Vtb0_sq_target) == 0,
        f"residual = {simplify(Vtb0_sq_full - Vtb0_sq_target)}",
    )

    # Atlas-leading row sum is identically 1 by construction.
    row_sum = Vtd0_sq_full + Vts0_sq_full + Vtb0_sq_full
    check(
        "(R3) row sum |V_td|_0^2 + |V_ts|_0^2 + |V_tb|_0^2 == 1 (parametric)",
        simplify(row_sum - 1) == 0,
        f"residual = {simplify(row_sum - 1)}",
    )

    # ---------------------------------------------------------------------
    section("Part 5: named cross-identities |V_ts|_0^2 = |V_cb|_0^2 and |V_td|_0^2/|V_ub|_0^2 = 5")
    # ---------------------------------------------------------------------
    # The Wolfenstein lambda/A subtheorem supplies
    #   |V_cb|^2 = alpha_s(v)^2 / 6,
    #   |V_ub|_0^2 = alpha_s(v)^3 / 72.
    Vcb_sq = alpha_s**2 / 6
    Vub0_sq = alpha_s**3 / 72

    check(
        "atlas-leading |V_ts|_0^2 == |V_cb|^2 (alpha_s^2 / 6)",
        simplify(Vts0_sq_full - Vcb_sq) == 0,
        f"residual = {simplify(Vts0_sq_full - Vcb_sq)}",
    )

    ratio_Vtd_Vub = simplify(Vtd0_sq_full / Vub0_sq)
    check(
        "atlas-leading |V_td|_0^2 / |V_ub|_0^2 == 5",
        ratio_Vtd_Vub == 5,
        f"ratio = {ratio_Vtd_Vub}",
    )

    # |V_td|_0 / |V_ub|_0 = sqrt(5) is the sqrt of the squared ratio.
    ratio_mag = simplify(sqrt(Vtd0_sq_full) / sqrt(Vub0_sq))
    check(
        "atlas-leading |V_td|_0 / |V_ub|_0 == sqrt(5)",
        simplify(ratio_mag - sqrt(5)) == 0,
        f"residual = {simplify(ratio_mag - sqrt(5))}",
    )

    # ---------------------------------------------------------------------
    section("Part 6: counterfactual probes")
    # ---------------------------------------------------------------------
    # The 5/72 coefficient on |V_td|_0^2 is forced by the imported
    # eta^2 = 5/36. Confirm: at eta^2 = 0 (rho-only, no CP region), the
    # V_td factor collapses from 5/6 to (5/6)^2 = 25/36 and the squared
    # magnitude becomes (2/3)(1/8)(25/36) alpha_s^3 = 25/432 alpha_s^3,
    # which is NOT 5/72 alpha_s^3.
    eta_sq_zero = Rational(0)
    distance_sq_zero = (1 - rho) ** 2 + eta_sq_zero
    Vtd0_sq_zero_eta = A_sq * lambda_sq**3 * distance_sq_zero
    check(
        "counterfactual: at eta^2 = 0, |V_td|_0^2 != 5 alpha_s^3 / 72",
        simplify(Vtd0_sq_zero_eta - Rational(5, 72) * alpha_s**3) != 0,
        f"alternate form simplifies to {simplify(Vtd0_sq_zero_eta)}",
    )

    # Another counterfactual: at A^2 = 1 (instead of 2/3), |V_ts|_0^2
    # = (alpha_s/2)^2 = alpha_s^2/4 != alpha_s^2/6, so the imported
    # A^2 = 2/3 is load-bearing for (R2).
    Vts0_at_Asq1 = 1 * lambda_sq**2
    check(
        "counterfactual: at A^2 = 1, |V_ts|_0^2 = alpha_s^2/4 != alpha_s^2/6",
        simplify(Vts0_at_Asq1 - alpha_s**2 / 6) != 0,
        f"alternate form simplifies to {simplify(Vts0_at_Asq1)}",
    )

    # Counterfactual on lambda^2: at lambda^2 = alpha_s (not alpha_s/2),
    # |V_ts|_0^2 = (2/3) alpha_s^2 != alpha_s^2/6.
    lambda_sq_alt = alpha_s  # forces n_pair = 1 instead of 2
    Vts0_alt = A_sq * lambda_sq_alt**2
    check(
        "counterfactual: at lambda^2 = alpha_s, |V_ts|_0^2 = 2 alpha_s^2/3 != alpha_s^2/6",
        simplify(Vts0_alt - alpha_s**2 / 6) != 0,
        f"alternate form simplifies to {simplify(Vts0_alt)}",
    )

    # ---------------------------------------------------------------------
    section("Part 7: trailing numerical sanity (canonical alpha_s pin)")
    # ---------------------------------------------------------------------
    # This is the only place the canonical numerical alpha_s(v) value enters.
    # It is NOT load-bearing for the parametric (R1)-(R3) identities above;
    # it is solely a sanity check that the symbolic forms specialize to the
    # expected numerical magnitudes documented in the parent note.
    try:
        from canonical_plaquette_surface import CANONICAL_ALPHA_S_V

        alpha_s_value = float(CANONICAL_ALPHA_S_V)
        Vtd_num = float((Vtd0_sq_full).subs(alpha_s, alpha_s_value)) ** 0.5
        Vts_num = float((Vts0_sq_full).subs(alpha_s, alpha_s_value)) ** 0.5
        Vtb_num = float((Vtb0_sq_full).subs(alpha_s, alpha_s_value)) ** 0.5
        print(f"  canonical alpha_s(v) = {alpha_s_value:.15f}")
        print(f"  atlas-leading |V_td|_0 = {Vtd_num:.7f}")
        print(f"  atlas-leading |V_ts|_0 = {Vts_num:.7f}")
        print(f"  atlas-leading |V_tb|_0 = {Vtb_num:.7f}")

        # Tabulated values from the parent note.
        check(
            "atlas-leading |V_td|_0 ~ 0.0087497 at canonical alpha_s",
            abs(Vtd_num - 0.0087497) < 1e-6,
            f"got {Vtd_num:.7f}",
        )
        check(
            "atlas-leading |V_ts|_0 ~ 0.0421736 at canonical alpha_s",
            abs(Vts_num - 0.0421736) < 1e-6,
            f"got {Vts_num:.7f}",
        )
        check(
            "atlas-leading |V_tb|_0 ~ 0.999072 at canonical alpha_s",
            abs(Vtb_num - 0.999072) < 1e-5,
            f"got {Vtb_num:.7f}",
        )
    except ImportError:
        print("  skipped: canonical_plaquette_surface not on PYTHONPATH")

    # ---------------------------------------------------------------------
    section("Summary")
    # ---------------------------------------------------------------------
    print("  Verified at exact sympy precision:")
    print("    Thales-style distance: (1-rho)^2 + eta^2 == 5/6 == 1 - rho")
    print("    (R1) |V_td|_0^2 == (5/72) alpha_s(v)^3 (parametric in alpha_s)")
    print("    (R2) |V_ts|_0^2 == alpha_s(v)^2 / 6 (parametric in alpha_s)")
    print("    (R3) |V_tb|_0^2 == 1 - |V_td|_0^2 - |V_ts|_0^2 unitarity completion")
    print("    Cross: |V_ts|_0^2 == |V_cb|^2; |V_td|_0^2 / |V_ub|_0^2 == 5")
    print("    Counterfactuals confirm eta^2 = 5/36, A^2 = 2/3, lambda^2 = alpha_s/2")
    print("    are each individually load-bearing for the closed-form coefficients.")

    print()
    print("=" * 88)
    print(f"TOTAL: PASS={PASS}, FAIL={FAIL}")
    print("=" * 88)
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
