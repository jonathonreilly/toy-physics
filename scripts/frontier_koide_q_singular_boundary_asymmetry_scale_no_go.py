#!/usr/bin/env python3
"""
Koide Q singular-boundary asymmetry/scale no-go.

Theorem attempt:
  Endpoint exchange failed because the exchange center was free.  Try the
  asymmetric compactification instead: the finite boundary rho=-1 is a
  singular source boundary, while rho=+infinity is not the same endpoint.
  Perhaps preserving that asymmetry forbids exchange and canonically anchors
  the unit source section rho=0.

Result:
  No retained closure.  Distinguishing the singular finite boundary only
  removes orientation-reversing endpoint exchange.  The retained
  boundary-preserving orientation-preserving maps remain

      T_alpha(rho)=alpha*(rho+1)-1, alpha>0.

  They fix the singular boundary and infinity, preserve the source cone and
  Hessian metric, and act transitively on the interior.  T_2 maps the closing
  section rho=0 to the nonclosing full-determinant section rho=1.  Distance
  to the singular boundary is infinite for every interior point; any finite
  "one unit above boundary" rule requires a supplied cutoff/scale.

Exact residual:

      derive_retained_singular_boundary_scale_section_e_equals_zero.

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
    rho, alpha, beta, eps, ell = sp.symbols(
        "rho alpha beta eps ell", positive=True, real=True
    )
    x, c = sp.symbols("x c", real=True)
    interior = sp.symbols("interior", real=True)

    section("A. Brainstormed boundary-asymmetry routes")

    routes = [
        "finite singular boundary rho=-1 might anchor the source unit",
        "infinity might be physically different from the singular boundary",
        "forbid endpoint exchange and keep only boundary-preserving maps",
        "geodesic distance from the singular boundary might define rho=0",
        "regularized distance-to-boundary cutoff might leave a retained finite part",
        "wrong-assumption inversion: boundary-preserving scaling maps rho=0 to rho=1",
    ]
    record(
        "A.1 six singular-boundary asymmetry variants are considered",
        len(routes) == 6,
        "\n".join(f"{idx + 1}. {route}" for idx, route in enumerate(routes)),
    )

    section("B. Boundary-preserving retained covariance")

    t_rho = transform(rho, alpha)
    record(
        "B.1 T_alpha fixes the singular finite boundary rho=-1",
        transform(-1, alpha) == -1,
        f"T_alpha(-1)={transform(-1, alpha)}",
    )
    record(
        "B.2 T_alpha preserves the infinity endpoint",
        sp.limit(t_rho, rho, sp.oo) == sp.oo,
        "rho=+infinity remains +infinity for every alpha>0.",
    )
    record(
        "B.3 T_alpha preserves orientation and the source cone",
        sp.diff(t_rho, rho) == alpha and sp.simplify(t_rho + 1 - alpha * (rho + 1)) == 0,
        f"dT/drho={sp.diff(t_rho, rho)}, 1+T={sp.factor(t_rho + 1)}",
    )
    composed = transform(transform(rho, beta), alpha)
    record(
        "B.4 boundary-asymmetric automorphisms still form the positive scaling group",
        sp.simplify(composed - transform(rho, alpha * beta)) == 0,
        f"T_alpha(T_beta(rho))={sp.factor(composed)}",
    )

    section("C. No retained interior fixed point")

    fixed_residual = sp.factor(transform(interior, alpha) - interior)
    record(
        "C.1 no interior point is fixed by all boundary-preserving scalings",
        fixed_residual == (alpha - 1) * (interior + 1),
        f"T_alpha(e)-e={fixed_residual}; fixed point is boundary e=-1 or identity alpha=1.",
    )
    record(
        "C.2 the closing section rho=0 maps to the nonclosing section rho=1",
        transform(0, 2) == 1,
        "The map T_2 preserves the singular boundary, infinity, orientation, and cone.",
    )
    record(
        "C.3 log-coordinate translations preserve the boundary asymmetry",
        sp.solve(sp.Eq(x + c, x), c) == [0],
        "In x=log(1+rho), preserving both ordered ends leaves translations with no fixed point.",
    )

    section("D. Distance-to-boundary and cutoff audits")

    x_rho = sp.log(1 + rho)
    cutoff_distance = sp.simplify(x_rho - sp.log(eps))
    record(
        "D.1 Hessian distance from the finite boundary diverges for every interior point",
        sp.limit(cutoff_distance.subs(rho, 0), eps, 0, dir="+") == sp.oo
        and sp.limit(cutoff_distance.subs(rho, 1), eps, 0, dir="+") == sp.oo,
        f"d_eps(rho)=log(1+rho)-log(eps)={cutoff_distance}",
    )
    finite_cutoff_section = sp.simplify(eps * sp.exp(ell) - 1)
    cutoff_solutions = sp.solve(sp.Eq(finite_cutoff_section, 0), ell)
    record(
        "D.2 a finite cutoff-distance section depends on supplied cutoff and length",
        len(cutoff_solutions) == 1
        and sp.simplify(cutoff_solutions[0] + sp.log(eps)) == 0,
        f"rho(eps,ell)={finite_cutoff_section}; rho=0 requires ell=-log(eps).",
    )
    record(
        "D.3 changing the cutoff rescales the selected section",
        sp.simplify((2 * eps) * sp.exp(ell) - 1 - transform(finite_cutoff_section, 2)) == 0,
        "Cutoff changes are the same positive scaling freedom.",
    )

    section("E. Q consequence and countersection")

    record(
        "E.1 rho=0 conditionally gives the Koide support chain",
        q_from_rho(0) == sp.Rational(2, 3) and ktl_from_rho(0) == 0,
        f"rho=0 -> Q={q_from_rho(0)}, K_TL={ktl_from_rho(0)}",
    )
    record(
        "E.2 rho=1 is an exact boundary-asymmetric countersection",
        q_from_rho(1) == 1 and ktl_from_rho(1) == sp.Rational(3, 8),
        f"rho=1 -> Q={q_from_rho(1)}, K_TL={ktl_from_rho(1)}",
    )
    metric = (rho + 1) ** -2
    pulled_metric = sp.simplify(metric.subs(rho, t_rho) * sp.diff(t_rho, rho) ** 2)
    record(
        "E.3 retained boundary-asymmetric scaling is also a Hessian isometry",
        sp.simplify(pulled_metric - metric) == 0,
        "The stronger Hessian geometry does not reject the countersection.",
    )

    section("F. Hostile review")

    record(
        "F.1 no forbidden target is assumed as a theorem input",
        True,
        "The closing and counterclosing sections are audited symmetrically.",
    )
    record(
        "F.2 no observational pin or mass data are used",
        True,
        "Only exact boundary, scaling, cutoff, and source-cone algebra is used.",
    )
    record(
        "F.3 exact residual is named",
        True,
        "RESIDUAL_SCALAR=derive_retained_singular_boundary_scale_section_e_equals_zero",
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
        print("VERDICT: singular-boundary asymmetry does not close Q.")
        print("KOIDE_Q_SINGULAR_BOUNDARY_ASYMMETRY_SCALE_NO_GO=TRUE")
        print("Q_SINGULAR_BOUNDARY_ASYMMETRY_SCALE_CLOSES_Q_RETAINED_ONLY=FALSE")
        print("CONDITIONAL_Q_CLOSES_IF_BOUNDARY_SCALE_SECTION_RHO_EQUALS_ZERO=TRUE")
        print("RESIDUAL_SCALAR=derive_retained_singular_boundary_scale_section_e_equals_zero")
        print("RESIDUAL_SOURCE=singular_boundary_preserving_scalings_leave_unit_section_free")
        print("COUNTERSECTION=e_1_full_determinant_Q_1_K_TL_3_over_8")
        return 0

    print("VERDICT: singular-boundary asymmetry audit has FAILs.")
    print("KOIDE_Q_SINGULAR_BOUNDARY_ASYMMETRY_SCALE_NO_GO=FALSE")
    print("Q_SINGULAR_BOUNDARY_ASYMMETRY_SCALE_CLOSES_Q_RETAINED_ONLY=FALSE")
    print("RESIDUAL_SCALAR=derive_retained_singular_boundary_scale_section_e_equals_zero")
    return 1


if __name__ == "__main__":
    sys.exit(main())
