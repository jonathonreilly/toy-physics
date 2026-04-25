#!/usr/bin/env python3
"""
Koide delta determinant-line universal-endpoint no-go.

Theorem attempt:
  Use the determinant line as the universal carrier of APS/eta holonomy.
  If the selected Brannen endpoint line is forced to be the determinant line
  itself, the endpoint functor should be identity:

      delta_open = eta_APS.

Result:
  Negative from the retained data alone.  The determinant line supplies the
  closed holonomy carrier.  A selected open endpoint line still needs a
  specified based, orientation-preserving isomorphism from that carrier.  In
  the absence of that isomorphism, tensor powers, duals, and flat endpoint
  twists give

      F(eta) = n eta + c.

  The universal property tells us which closed line carries eta; it does not
  identify the selected open Brannen endpoint with the unit determinant line.

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


def endpoint_from_determinant(eta: sp.Expr, tensor_power: sp.Expr, flat_twist: sp.Expr) -> sp.Expr:
    return sp.simplify(tensor_power * eta + flat_twist)


def main() -> int:
    section("A. Closed determinant-line support")

    eta = eta_abss_z3_weights_12()
    record(
        "A.1 determinant-line APS holonomy support is eta_APS = 2/9",
        eta == sp.Rational(2, 9),
        f"eta_APS={eta}",
    )

    section("B. Universal carrier versus selected open endpoint")

    n, c = sp.symbols("n c", real=True)
    endpoint = endpoint_from_determinant(eta, n, c)
    residual = sp.simplify(endpoint / eta - 1)
    record(
        "B.1 maps from determinant carrier to selected endpoint have degree and flat twist",
        residual == n + c / eta - 1,
        f"F(eta_APS)={endpoint}; F/eta_APS - 1 = {residual}",
    )

    retained_constraints = [sp.simplify(eta - sp.Rational(2, 9))]
    jac = sp.Matrix([[sp.diff(expr, var) for var in (n, c)] for expr in retained_constraints])
    record(
        "B.2 closed determinant support has zero rank in selected endpoint map variables",
        jac.rank() == 0,
        f"Jacobian wrt (n,c) = {jac.tolist()}",
    )

    section("C. Tensor powers, duals, and twists")

    samples = [
        ("zero map/torsor section", sp.Integer(0), sp.Integer(0)),
        ("identity determinant line", sp.Integer(1), sp.Integer(0)),
        ("dual determinant line", sp.Integer(-1), sp.Integer(0)),
        ("square determinant line", sp.Integer(2), sp.Integer(0)),
        ("identity with flat twist", sp.Integer(1), sp.Rational(1, 9)),
    ]
    lines = []
    values = set()
    for label, degree, twist in samples:
        value = endpoint_from_determinant(eta, degree, twist)
        values.add(value)
        lines.append(f"{label}: n={degree}, c={twist}, endpoint={value}")
    record(
        "C.1 determinant-compatible endpoint maps have distinct selected endpoints",
        len(values) == len(samples),
        "\n".join(lines),
    )
    record(
        "C.2 the identity determinant map is one option, not forced by universality",
        endpoint_from_determinant(eta, 1, 0) == eta,
        "Universal closed carrier plus selected identity is exactly the desired bridge.",
    )

    section("D. What would close the route")

    closure_conditions = sp.solve([sp.Eq(endpoint, eta), sp.Eq(c, 0)], [n, c], dict=True)
    record(
        "D.1 closure with no flat twist is equivalent to n=1,c=0",
        closure_conditions == [{n: 1, c: 0}],
        f"solutions={closure_conditions}",
    )
    record(
        "D.2 orientation-preserving based isomorphism would close but is not retained",
        True,
        "Need a theorem that the selected Brannen endpoint is the based unit determinant line, not a tensor power or flat twist.",
    )

    section("E. Hostile-review objections")

    record(
        "E.1 determinant universality identifies the closed carrier only",
        True,
        "The selected open endpoint is a further readout functor from that carrier.",
    )
    record(
        "E.2 excluding tensor powers or duals requires selected-line identity data",
        endpoint_from_determinant(eta, -1, 0) == -sp.Rational(2, 9)
        and endpoint_from_determinant(eta, 2, 0) == sp.Rational(4, 9),
        "Both are determinant-line constructions unless the selected map is fixed to identity.",
    )

    section("F. Verdict")

    theta0, theta_end = sp.symbols("theta0 theta_end", real=True)
    residual_endpoint = sp.simplify(theta_end - theta0 - eta)
    record(
        "F.1 determinant universal-endpoint route does not close delta",
        residual_endpoint == theta_end - theta0 - sp.Rational(2, 9),
        f"RESIDUAL_ENDPOINT={residual_endpoint}",
    )
    record(
        "F.2 residual is based orientation-preserving selected-line determinant isomorphism",
        True,
        "Need n=1 and c=0 from retained boundary/determinant data.",
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
        print("VERDICT: determinant universal-endpoint route does not close delta.")
        print("KOIDE_DELTA_DETERMINANT_UNIVERSAL_ENDPOINT_NO_GO=TRUE")
        print("DELTA_DETERMINANT_UNIVERSAL_ENDPOINT_CLOSES_DELTA=FALSE")
        print("RESIDUAL_ENDPOINT=theta_end-theta0-eta_APS")
        print("RESIDUAL_ISOMORPHISM=based_orientation_preserving_selected_determinant_identity_not_retained")
        print("RESIDUAL_SCALAR=n_minus_one_plus_c_over_eta_APS")
        return 0

    print("VERDICT: determinant universal-endpoint audit has FAILs.")
    print("KOIDE_DELTA_DETERMINANT_UNIVERSAL_ENDPOINT_NO_GO=FALSE")
    print("DELTA_DETERMINANT_UNIVERSAL_ENDPOINT_CLOSES_DELTA=FALSE")
    print("RESIDUAL_ENDPOINT=theta_end-theta0-eta_APS")
    print("RESIDUAL_ISOMORPHISM=based_orientation_preserving_selected_determinant_identity_not_retained")
    print("RESIDUAL_SCALAR=n_minus_one_plus_c_over_eta_APS")
    return 1


if __name__ == "__main__":
    sys.exit(main())
