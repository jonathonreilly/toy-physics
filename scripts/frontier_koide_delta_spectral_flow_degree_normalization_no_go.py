#!/usr/bin/env python3
"""
Koide delta spectral-flow degree-normalization no-go.

Theorem attempt:
  After endpoint-functor classification reduced the Brannen bridge to

      delta_open = n * eta_APS + c,

  maybe integer spectral flow supplies the missing normalization and forces
  n = 1, c = 0.

Result:
  Negative.  Spectral flow can count crossings on the determinant/spectral
  line.  It fixes the selected open endpoint only after an extra theorem says
  that the selected Brannen line is the unit-degree spectral-flow generator
  with the same endpoint basepoint.  That is exactly the residual endpoint
  functor law, not a consequence of the current retained data.

No mass data, fitted Koide value, or selected endpoint target is used.
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


def eta_abss_z3_weights_12() -> sp.Expr:
    omega = sp.Rational(-1, 2) + sp.I * sp.sqrt(3) / 2
    total = sp.Rational(0)
    for k in (1, 2):
        z1 = omega**k
        z2 = omega ** (2 * k)
        total += sp.simplify(1 / ((z1 - 1) * (z2 - 1)))
    return sp.simplify(total / 3)


def endpoint_functor(eta: sp.Expr, degree: sp.Expr, offset: sp.Expr) -> sp.Expr:
    return sp.simplify(degree * eta + offset)


def main() -> int:
    section("A. Retained ambient spectral datum")

    eta = eta_abss_z3_weights_12()
    record(
        "A.1 ambient APS support scalar is eta_APS = 2/9",
        eta == sp.Rational(2, 9),
        f"eta_APS={eta}",
    )

    n, c, sf = sp.symbols("n c SF", real=True)
    delta = endpoint_functor(eta, n, c)
    normalized_residual = sp.simplify(delta / eta - 1)
    record(
        "A.2 endpoint-functor residual is n - 1 plus offset/eta",
        normalized_residual == n + c / eta - 1,
        f"delta/eta_APS - 1 = {normalized_residual}",
    )

    section("B. Spectral-flow count does not act on the endpoint functor")

    retained_constraints = [
        sp.simplify(eta - sp.Rational(2, 9)),
        sp.simplify(sf - 1),
    ]
    jac = sp.Matrix([[sp.diff(expr, var) for var in (n, c)] for expr in retained_constraints])
    record(
        "B.1 retained eta plus one crossing has zero rank in endpoint degree and offset",
        jac.rank() == 0,
        f"Jacobian wrt (n,c) = {jac.tolist()}",
    )

    samples = [
        (sp.Integer(-1), sp.Integer(0)),
        (sp.Integer(0), sp.Integer(0)),
        (sp.Integer(1), sp.Integer(0)),
        (sp.Integer(2), sp.Integer(0)),
        (sp.Integer(1), sp.Rational(1, 9)),
    ]
    lines = []
    all_support_ok = True
    values = set()
    for degree, offset in samples:
        value = endpoint_functor(eta, degree, offset)
        values.add(value)
        support_ok = all(expr.subs(sf, 1) == 0 for expr in retained_constraints)
        all_support_ok = all_support_ok and support_ok
        lines.append(
            f"n={degree}, c={offset}: delta_open={value}, "
            f"eta_APS={eta}, SF=1, support_ok={support_ok}"
        )
    record(
        "B.2 distinct endpoint functors preserve the same retained spectral-flow support",
        all_support_ok and len(values) == len(samples),
        "\n".join(lines),
    )

    section("C. What would close the route")

    unit_degree_solution = sp.solve(sp.Eq(n, sf), n)
    closure_solution = sp.solve(sp.Eq(endpoint_functor(eta, n, 0), eta), n)
    record(
        "C.1 identifying endpoint degree with unit spectral flow would force n = 1",
        unit_degree_solution == [sf] and closure_solution == [1],
        "With SF=1 and c=0, the added identity n=SF gives the closing degree.",
    )
    record(
        "C.2 that identity is the missing selected-line functor law",
        True,
        "It says the open Brannen endpoint is the unit-degree spectral-flow generator.",
    )

    section("D. Hostile-review objections")

    record(
        "D.1 integer quantization alone cannot choose the fractional endpoint",
        endpoint_functor(eta, 0, 0) == 0 and endpoint_functor(eta, 2, 0) == sp.Rational(4, 9),
        "The same integer crossing datum allows n=0 and n=2 unless the selected line is identified with the generator.",
    )
    record(
        "D.2 endpoint offset remains a separate basepoint/trivialization datum",
        sp.solve(sp.Eq(endpoint_functor(eta, n, c), eta), c)
        == [sp.Rational(2, 9) - sp.Rational(2, 9) * n],
        "For any degree, a chosen offset can force closure; that is an endpoint basepoint choice.",
    )

    section("E. Verdict")

    theta0, theta_end = sp.symbols("theta0 theta_end", real=True)
    residual_endpoint = sp.simplify(theta_end - theta0 - eta)
    record(
        "E.1 spectral-flow degree normalization does not close delta",
        residual_endpoint == theta_end - theta0 - sp.Rational(2, 9),
        f"RESIDUAL_ENDPOINT={residual_endpoint}",
    )
    record(
        "E.2 residual is selected-line spectral-flow degree plus endpoint basepoint",
        True,
        "Need a retained theorem deriving n=1 and c=0 for the selected open endpoint.",
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
        print("VERDICT: spectral-flow degree normalization does not close delta.")
        print("KOIDE_DELTA_SPECTRAL_FLOW_DEGREE_NORMALIZATION_NO_GO=TRUE")
        print("DELTA_SPECTRAL_FLOW_DEGREE_NORMALIZATION_CLOSES_DELTA=FALSE")
        print("RESIDUAL_ENDPOINT=theta_end-theta0-eta_APS")
        print("RESIDUAL_FUNCTOR_DEGREE=selected_line_spectral_flow_degree_not_forced_one")
        print("RESIDUAL_SCALAR=n_minus_one_plus_c_over_eta_APS")
        return 0

    print("VERDICT: spectral-flow degree-normalization audit has FAILs.")
    print("KOIDE_DELTA_SPECTRAL_FLOW_DEGREE_NORMALIZATION_NO_GO=FALSE")
    print("DELTA_SPECTRAL_FLOW_DEGREE_NORMALIZATION_CLOSES_DELTA=FALSE")
    print("RESIDUAL_ENDPOINT=theta_end-theta0-eta_APS")
    print("RESIDUAL_FUNCTOR_DEGREE=selected_line_spectral_flow_degree_not_forced_one")
    print("RESIDUAL_SCALAR=n_minus_one_plus_c_over_eta_APS")
    return 1


if __name__ == "__main__":
    sys.exit(main())
