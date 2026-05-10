#!/usr/bin/env python3
"""Exact-symbolic audit-companion runner for
`ckm_first_row_magnitudes_theorem_note_2026-04-24`.

The parent note's load-bearing content is the algebraic-substitution
claim that the imported atlas inputs

  lambda^2 = alpha_s(v) / 2,
  A^2      = 2 / 3,
  rho      = 1 / 6,
  eta^2    = 5 / 36,
  rho^2 + eta^2 = 1/6,

force the closed-form atlas-leading first-row magnitude identities

  (F1) |V_us|_0^2 = lambda^2          = alpha_s(v) / 2,
  (F2) |V_ub|_0^2 = A^2 lambda^6 (rho^2 + eta^2)
                  = alpha_s(v)^3 / 72,
  (F3) |V_ud|_0^2 = 1 - |V_us|_0^2 - |V_ub|_0^2
                  = 1 - alpha_s(v)/2 - alpha_s(v)^3/72.

The existing primary runner
(`scripts/frontier_ckm_first_row_magnitudes.py`) verifies these
identities at floating-point tolerance using the canonical numerical
alpha_s(v) and at Fraction-precision rational coefficients. This
Pattern B audit companion adds a sympy-based exact-symbolic
verification:

  (a) treats alpha_s(v) as a free positive real symbol so the algebra
      cannot be passing accidentally on a single numerical value;
  (b) imports the upstream atlas inputs verbatim:
        lambda^2 = alpha_s(v) / 2,
        A^2      = 2 / 3,
        rho      = 1 / 6,
        eta^2    = 5 / 36,
        rho^2 + eta^2 = 1 / 6;
  (c) verifies the cited CP-radius reduction
        rho^2 + eta^2 == 1/6
      as an exact sympy.Rational identity;
  (d) verifies (F1), (F2), (F3) symbolically:
        (F1) lambda^2                  == alpha_s(v) / 2,
        (F2) A^2 lambda^6 (rho^2+eta^2) == alpha_s(v)^3 / 72,
        (F3) 1 - lambda^2 - A^2 lambda^6 (rho^2+eta^2)
             == 1 - alpha_s(v)/2 - alpha_s(v)^3/72;
  (e) verifies the row-sum closure (F1)+(F2)+(F3) == 1 parametric;
  (f) provides counterfactual probes confirming each imported input
      is individually load-bearing (eta^2 = 0 -> coefficient changes;
      A^2 = 1 -> coefficient changes; lambda^2 = alpha_s -> coefficient
      changes).

Companion role: Pattern B audit-acceleration only. Not a new claim row,
not a new source note, no status promotion. The cited atlas inputs
themselves (lambda^2 = alpha_s(v)/2, A^2 = 2/3, rho = 1/6, eta^2 = 5/36,
rho^2 + eta^2 = 1/6) are imported from upstream authority notes and are
not re-derived here. The numerical pin of alpha_s(v) only enters the
trailing sanity check, which is not load-bearing for the algebra.
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
    print("ckm_first_row_magnitudes_theorem_note_2026-04-24")
    print("Goal: sympy-symbolic verification of (F1), (F2), (F3) and the")
    print("row-sum closure at exact precision over a free symbolic alpha_s(v).")
    print("=" * 88)

    # ---------------------------------------------------------------------
    section("Part 0: symbolic setup and imported atlas inputs")
    # ---------------------------------------------------------------------
    alpha_s = Symbol("alpha_s", positive=True, real=True)

    # Imported atlas inputs (cited authorities; not re-derived here).
    lambda_sq = alpha_s / Rational(2)
    A_sq = Rational(2, 3)
    rho = Rational(1, 6)
    eta_sq = Rational(5, 36)
    cp_radius_sq = Rational(1, 6)  # rho^2 + eta^2 = 1/6

    print(f"  symbolic alpha_s(v) = {alpha_s}")
    print(f"  lambda^2 = {lambda_sq}")
    print(f"  A^2      = {A_sq}")
    print(f"  rho      = {rho}")
    print(f"  eta^2    = {eta_sq}")
    print(f"  rho^2 + eta^2 = {cp_radius_sq}")

    # ---------------------------------------------------------------------
    section("Part 1: cited CP-radius reduction rho^2 + eta^2 = 1/6")
    # ---------------------------------------------------------------------
    cp_lhs = simplify(rho ** 2 + eta_sq)
    check(
        "rho^2 + eta^2 == 1/6 (exact rational)",
        simplify(cp_lhs - cp_radius_sq) == 0,
        f"residual = {simplify(cp_lhs - cp_radius_sq)}",
    )

    # ---------------------------------------------------------------------
    section("Part 2: (F1) |V_us|_0^2 = lambda^2 = alpha_s(v)/2")
    # ---------------------------------------------------------------------
    Vus_sq = lambda_sq
    Vus_sq_target = alpha_s / Rational(2)
    check(
        "(F1) |V_us|_0^2 == alpha_s(v)/2 (parametric)",
        simplify(Vus_sq - Vus_sq_target) == 0,
        f"residual = {simplify(Vus_sq - Vus_sq_target)}",
    )

    coeff_F1 = simplify(Vus_sq / alpha_s)
    check(
        "(F1) coefficient is the pure rational 1/2",
        coeff_F1 == Rational(1, 2),
        f"coefficient = {coeff_F1}",
    )

    # ---------------------------------------------------------------------
    section("Part 3: (F2) |V_ub|_0^2 = A^2 lambda^6 (rho^2 + eta^2) = alpha_s(v)^3/72")
    # ---------------------------------------------------------------------
    Vub_sq_full = A_sq * lambda_sq ** 3 * cp_radius_sq
    Vub_sq_target = alpha_s ** 3 / Rational(72)

    check(
        "(F2) A^2 lambda^6 (rho^2+eta^2) == alpha_s(v)^3/72 (parametric)",
        simplify(Vub_sq_full - Vub_sq_target) == 0,
        f"residual = {simplify(Vub_sq_full - Vub_sq_target)}",
    )

    coeff_F2 = simplify(Vub_sq_full / alpha_s ** 3)
    check(
        "(F2) coefficient is the pure rational 1/72",
        coeff_F2 == Rational(1, 72),
        f"coefficient = {coeff_F2}",
    )

    # |V_ub|_0 = alpha_s^(3/2)/(6 sqrt(2)).
    Vub_mag = simplify(sqrt(Vub_sq_full))
    Vub_mag_target = alpha_s ** Rational(3, 2) / (Rational(6) * sqrt(2))
    check(
        "(F2) |V_ub|_0 == alpha_s(v)^(3/2)/(6 sqrt(2))",
        simplify(Vub_mag - Vub_mag_target) == 0,
        f"residual = {simplify(Vub_mag - Vub_mag_target)}",
    )

    # ---------------------------------------------------------------------
    section("Part 4: (F3) |V_ud|_0^2 = 1 - |V_us|_0^2 - |V_ub|_0^2")
    # ---------------------------------------------------------------------
    Vud_sq_full = 1 - Vus_sq - Vub_sq_full
    Vud_sq_target = 1 - alpha_s / Rational(2) - alpha_s ** 3 / Rational(72)

    check(
        "(F3) |V_ud|_0^2 == 1 - alpha_s(v)/2 - alpha_s(v)^3/72 (parametric)",
        simplify(Vud_sq_full - Vud_sq_target) == 0,
        f"residual = {simplify(Vud_sq_full - Vud_sq_target)}",
    )

    # First-row sum identically 1 by construction.
    row_sum = simplify(Vus_sq + Vub_sq_full + Vud_sq_full)
    check(
        "(F3) row-sum closure |V_us|_0^2 + |V_ub|_0^2 + |V_ud|_0^2 == 1 (parametric)",
        simplify(row_sum - 1) == 0,
        f"residual = {simplify(row_sum - 1)}",
    )

    # ---------------------------------------------------------------------
    section("Part 5: cross-check |V_us|_0^2 / |V_ub|_0^2 = 36/alpha_s^2")
    # ---------------------------------------------------------------------
    # |V_us|^2/|V_ub|^2 = (alpha_s/2)/(alpha_s^3/72) = 36/alpha_s^2.
    ratio = simplify(Vus_sq / Vub_sq_full)
    check(
        "|V_us|_0^2 / |V_ub|_0^2 == 36/alpha_s^2",
        simplify(ratio - 36 / alpha_s ** 2) == 0,
        f"residual = {simplify(ratio - 36/alpha_s**2)}",
    )

    # ---------------------------------------------------------------------
    section("Part 6: counterfactual probes")
    # ---------------------------------------------------------------------
    # The 1/72 coefficient on |V_ub|^2 is fixed by rho^2 + eta^2 = 1/6
    # and A^2 = 2/3 and lambda^2 = alpha_s/2 jointly.
    # Counterfactual: at rho^2 + eta^2 = 1 (no CP suppression), the
    # closed form would be (2/3)(1/8) alpha_s^3 = alpha_s^3 / 12, not /72.
    cp_alt = Rational(1)
    Vub_sq_alt = A_sq * lambda_sq ** 3 * cp_alt
    check(
        "counterfactual: at rho^2 + eta^2 = 1, |V_ub|^2 = alpha_s^3/12 != alpha_s^3/72",
        simplify(Vub_sq_alt - Vub_sq_target) != 0,
        f"alternate form simplifies to {simplify(Vub_sq_alt)}",
    )

    # Counterfactual on A^2: at A^2 = 1, |V_ub|^2 = alpha_s^3/48, not /72.
    Vub_sq_at_Asq1 = Rational(1) * lambda_sq ** 3 * cp_radius_sq
    check(
        "counterfactual: at A^2 = 1, |V_ub|^2 = alpha_s^3/48 != alpha_s^3/72",
        simplify(Vub_sq_at_Asq1 - Vub_sq_target) != 0,
        f"alternate form simplifies to {simplify(Vub_sq_at_Asq1)}",
    )

    # Counterfactual on lambda^2: at lambda^2 = alpha_s, |V_ub|^2 = alpha_s^3/9, not /72.
    lambda_sq_alt = alpha_s
    Vub_sq_at_lambda_alt = A_sq * lambda_sq_alt ** 3 * cp_radius_sq
    check(
        "counterfactual: at lambda^2 = alpha_s, |V_ub|^2 = alpha_s^3/9 != alpha_s^3/72",
        simplify(Vub_sq_at_lambda_alt - Vub_sq_target) != 0,
        f"alternate form simplifies to {simplify(Vub_sq_at_lambda_alt)}",
    )

    # |V_us|^2 counterfactual: at lambda^2 = alpha_s, |V_us|^2 = alpha_s, not alpha_s/2.
    Vus_sq_alt = lambda_sq_alt
    check(
        "counterfactual: at lambda^2 = alpha_s, |V_us|^2 = alpha_s != alpha_s/2",
        simplify(Vus_sq_alt - Vus_sq_target) != 0,
        f"alternate form simplifies to {simplify(Vus_sq_alt)}",
    )

    # ---------------------------------------------------------------------
    section("Part 7: trailing numerical sanity (canonical alpha_s pin)")
    # ---------------------------------------------------------------------
    try:
        from canonical_plaquette_surface import CANONICAL_ALPHA_S_V

        alpha_s_value = float(CANONICAL_ALPHA_S_V)
        Vus_num = float(Vus_sq.subs(alpha_s, alpha_s_value)) ** 0.5
        Vub_num = float(Vub_sq_full.subs(alpha_s, alpha_s_value)) ** 0.5
        Vud_num = float(Vud_sq_full.subs(alpha_s, alpha_s_value)) ** 0.5
        print(f"  canonical alpha_s(v) = {alpha_s_value:.15f}")
        print(f"  atlas-leading |V_us|_0 = {Vus_num:.7f}")
        print(f"  atlas-leading |V_ub|_0 = {Vub_num:.7f}")
        print(f"  atlas-leading |V_ud|_0 = {Vud_num:.7f}")
        check(
            "atlas-leading |V_us|_0 ~ 0.2272706 at canonical alpha_s",
            abs(Vus_num - 0.2272706) < 1e-6,
            f"got {Vus_num:.7f}",
        )
        check(
            "atlas-leading |V_ub|_0 ~ 0.0039130 at canonical alpha_s",
            abs(Vub_num - 0.0039130) < 1e-6,
            f"got {Vub_num:.7f}",
        )
        check(
            "atlas-leading |V_ud|_0 ~ 0.9738238 at canonical alpha_s",
            abs(Vud_num - 0.9738238) < 1e-6,
            f"got {Vud_num:.7f}",
        )
    except ImportError:
        print("  skipped: canonical_plaquette_surface not on PYTHONPATH")

    # ---------------------------------------------------------------------
    section("Summary")
    # ---------------------------------------------------------------------
    print("  Verified at exact sympy precision:")
    print("    rho^2 + eta^2 == 1/6 (CP-radius reduction)")
    print("    (F1) |V_us|_0^2 == alpha_s(v)/2 (parametric in alpha_s)")
    print("    (F2) |V_ub|_0^2 == alpha_s(v)^3/72 (parametric in alpha_s)")
    print("    (F3) |V_ud|_0^2 == 1 - alpha_s(v)/2 - alpha_s(v)^3/72")
    print("    Row-sum closure (F1) + (F2) + (F3) == 1 (parametric)")
    print("    Cross-ratio |V_us|_0^2 / |V_ub|_0^2 == 36/alpha_s^2")
    print("    Counterfactuals confirm rho^2+eta^2=1/6, A^2=2/3, lambda^2=alpha_s/2")
    print("    are individually load-bearing for the closed-form coefficients.")

    print()
    print("=" * 88)
    print(f"TOTAL: PASS={PASS}, FAIL={FAIL}")
    print("=" * 88)
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
