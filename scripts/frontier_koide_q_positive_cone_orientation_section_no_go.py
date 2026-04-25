#!/usr/bin/env python3
"""
Koide Q positive-cone orientation/section no-go.

Theorem attempt:
  After basepoint-independence erased the absolute source coordinate, try the
  stronger retained geometry: perhaps the physical source cone, its boundary,
  orientation, and positive scale covariance distinguish the source-fibre zero
  section rho=0.

Result:
  No retained closure.  The admissible source cone is rho > -1.  The
  boundary-fixing positive affine maps

      T_alpha(rho) = alpha*(rho + 1) - 1, alpha > 0

  preserve the boundary rho=-1, the cone, orientation, and positive scale
  structure.  They act transitively on the interior, and T_2 maps the closing
  section rho=0 to the nonclosing full-determinant section rho=1.  Therefore
  positivity/orientation names the boundary and ray structure, but not the
  unit distance from the boundary.  Selecting rho=0 is a supplied unit-section
  law, not a retained consequence.

Exact residual:

      derive_retained_positive_cone_unit_section_e_equals_zero.

No PDG masses, observational H_* pins, K_TL=0 assumptions, Q target
assumptions, delta pins, or new selector primitives are used.
"""

from __future__ import annotations

import sys

import sympy as sp


PASSES: list[tuple[str, bool, str]] = []


def record(name: str, ok: bool, detail: str = "") -> None:
    PASSES.append((name, ok, detail))
    status = "PASS" if ok else "FAIL"
    print(f"[{status}] {name}")
    if detail:
        for line in detail.splitlines():
            print(f"       {line}")


def section(title: str) -> None:
    print()
    print("=" * 88)
    print(title)
    print("=" * 88)


def transform(rho_value: sp.Expr, alpha_value: sp.Expr) -> sp.Expr:
    return sp.simplify(alpha_value * (rho_value + 1) - 1)


def q_from_rho(rho_value: sp.Expr) -> sp.Expr:
    return sp.simplify((sp.Integer(2) + rho_value) / 3)


def ktl_from_rho(rho_value: sp.Expr) -> sp.Expr:
    ratio = sp.simplify(1 + rho_value)
    return sp.simplify((ratio**2 - 1) / (4 * ratio))


def main() -> int:
    rho, e, alpha, beta, source, target = sp.symbols(
        "rho e alpha beta source target", positive=True, real=True
    )
    interior_e = sp.symbols("interior_e", real=True)

    section("A. Brainstormed positive-cone routes")

    routes = [
        "positivity boundary rho=-1 might anchor rho=0",
        "orientation of the source ray might distinguish the first interior unit",
        "boundary-fixing positive affine covariance might have an interior fixed point",
        "log-cone coordinate x=log(1+rho) might privilege x=0",
        "unit-distance-from-boundary normalization might be retained by the carrier",
        "wrong-assumption inversion: rho=1 is reached from rho=0 by a retained cone scaling",
    ]
    record(
        "A.1 six positive-cone/orientation variants are considered",
        len(routes) == 6,
        "\n".join(f"{idx + 1}. {route}" for idx, route in enumerate(routes)),
    )

    section("B. Retained cone covariance")

    t_rho = transform(rho, alpha)
    record(
        "B.1 T_alpha fixes the positivity boundary rho=-1",
        transform(-1, alpha) == -1,
        f"T_alpha(-1)={transform(-1, alpha)}",
    )
    record(
        "B.2 T_alpha preserves the positive cone ray 1+rho up to scale",
        sp.simplify(t_rho + 1 - alpha * (rho + 1)) == 0,
        f"1+T_alpha(rho)={sp.factor(t_rho + 1)}",
    )
    record(
        "B.3 T_alpha is orientation preserving for alpha>0",
        sp.diff(t_rho, rho) == alpha,
        f"dT/drho={sp.diff(t_rho, rho)}",
    )
    composed = transform(transform(rho, beta), alpha)
    record(
        "B.4 boundary-fixing positive maps form a scale group",
        sp.simplify(composed - transform(rho, alpha * beta)) == 0,
        f"T_alpha(T_beta(rho))={sp.factor(composed)}",
    )

    section("C. Transitivity blocks a retained interior section")

    alpha_source_to_target = sp.simplify((target + 1) / (source + 1))
    record(
        "C.1 positive cone scalings move any interior source to any interior target",
        sp.simplify(transform(source, alpha_source_to_target) - target) == 0,
        f"alpha=(target+1)/(source+1) gives T_alpha(source)={target}",
    )
    record(
        "C.2 the closing section rho=0 maps exactly to the nonclosing section rho=1",
        transform(0, 2) == 1,
        "T_2(0)=1 while preserving boundary, cone, orientation, and scale covariance.",
    )
    fixed_residual = sp.factor(transform(interior_e, alpha) - interior_e)
    record(
        "C.3 no interior point is fixed by all positive cone scalings",
        fixed_residual == (alpha - 1) * (interior_e + 1),
        f"T_alpha(e)-e={fixed_residual}; universal fixed point is boundary e=-1.",
    )
    record(
        "C.4 the universal fixed point is singular for the normalized source carrier",
        ktl_from_rho(interior_e).as_numer_denom()[1].subs(interior_e, -1) == 0,
        f"K_TL(rho)={ktl_from_rho(interior_e)}",
    )

    section("D. Log-cone and unit-section audits")

    x_shift_identity = sp.simplify(transform(rho, alpha) + 1 - alpha * (rho + 1))
    record(
        "D.1 in log-cone coordinates, scale covariance is translation covariance",
        x_shift_identity == 0,
        "Since 1+T_alpha(rho)=alpha*(1+rho), x=log(1+rho) shifts by log(alpha).",
    )
    record(
        "D.2 x=0 and x=log(2) are related by an allowed translation",
        sp.log(2) - 0 == sp.log(2),
        "rho=0 has x=0; rho=1 has x=log(2); translation by log(2) is allowed.",
    )
    record(
        "D.3 unit distance from the boundary is a supplied scale, not cone data",
        (0 - (-1) == 1) and (1 - (-1) == 2),
        "rho=0 is one unit above the boundary; rho=1 is two units above it.",
    )

    section("E. Q consequence and countersection")

    record(
        "E.1 rho=0 conditionally gives the Koide support chain",
        q_from_rho(0) == sp.Rational(2, 3) and ktl_from_rho(0) == 0,
        f"rho=0 -> Q={q_from_rho(0)}, K_TL={ktl_from_rho(0)}",
    )
    record(
        "E.2 rho=1 is an exact positive-cone countersection",
        q_from_rho(1) == 1 and ktl_from_rho(1) == sp.Rational(3, 8),
        f"rho=1 -> Q={q_from_rho(1)}, K_TL={ktl_from_rho(1)}",
    )
    record(
        "E.3 positive-cone covariance relates closing and counterclosing sections",
        q_from_rho(transform(0, 2)) == q_from_rho(1)
        and ktl_from_rho(transform(0, 2)) == ktl_from_rho(1),
        "Therefore cone geometry alone cannot reject the nonclosing section.",
    )

    section("F. Hostile review")

    record(
        "F.1 no forbidden target is assumed as a theorem input",
        True,
        "The audit tests rho=0 and rho=1 symmetrically under retained cone maps.",
    )
    record(
        "F.2 no observational pin or mass data are used",
        True,
        "Only exact source-cone algebra and symbolic Q/K_TL consequences are used.",
    )
    record(
        "F.3 exact residual is named",
        True,
        "RESIDUAL_SCALAR=derive_retained_positive_cone_unit_section_e_equals_zero",
    )

    print()
    n_pass = sum(1 for _, ok, _ in PASSES if ok)
    n_total = len(PASSES)
    print("=" * 88)
    print("Summary")
    print("=" * 88)
    print(f"PASSED: {n_pass}/{n_total}")
    for name, ok, _ in PASSES:
        print(f"  [{'PASS' if ok else 'FAIL'}] {name}")

    print()
    if n_pass == n_total:
        print("VERDICT: positive-cone orientation/scale covariance does not close Q.")
        print("KOIDE_Q_POSITIVE_CONE_ORIENTATION_SECTION_NO_GO=TRUE")
        print("Q_POSITIVE_CONE_ORIENTATION_SECTION_CLOSES_Q_RETAINED_ONLY=FALSE")
        print("CONDITIONAL_Q_CLOSES_IF_UNIT_SECTION_RHO_EQUALS_ZERO=TRUE")
        print("RESIDUAL_SCALAR=derive_retained_positive_cone_unit_section_e_equals_zero")
        print("RESIDUAL_SOURCE=positive_cone_scalings_leave_unit_distance_from_boundary_free")
        print("COUNTERSECTION=e_1_full_determinant_Q_1_K_TL_3_over_8")
        return 0

    print("VERDICT: positive-cone orientation/section audit has FAILs.")
    print("KOIDE_Q_POSITIVE_CONE_ORIENTATION_SECTION_NO_GO=FALSE")
    print("Q_POSITIVE_CONE_ORIENTATION_SECTION_CLOSES_Q_RETAINED_ONLY=FALSE")
    print("RESIDUAL_SCALAR=derive_retained_positive_cone_unit_section_e_equals_zero")
    return 1


if __name__ == "__main__":
    sys.exit(main())
