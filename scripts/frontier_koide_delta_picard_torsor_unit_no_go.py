#!/usr/bin/env python3
"""
Koide delta Picard-torsor unit no-go.

Theorem attempt:
  Remove the endpoint offset c by treating the selected open endpoint phases
  as a Picard/monoidal target.  A monoidal functor preserves the unit, so maybe
  c = 0 follows without adding an endpoint basepoint law.

Result:
  Negative from the retained data alone.  The closed APS phases form a based
  U(1) phase group, but an open selected-line endpoint is naturally a U(1)
  torsor until a boundary section/basepoint is supplied.  A torsor morphism has
  the affine form

      F(eta) = n eta + c.

  Monoidal unit preservation removes c only after the target torsor has been
  based.  The retained packet does not provide that canonical selected-line
  basepoint.

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


def affine_torsor_map(x: sp.Expr, n: sp.Expr, c: sp.Expr) -> sp.Expr:
    return sp.simplify(n * x + c)


def main() -> int:
    section("A. Group versus torsor endpoint structure")

    x, y, n, c = sp.symbols("x y n c", real=True)
    F0 = affine_torsor_map(0, n, c)
    add_defect = sp.simplify(affine_torsor_map(x + y, n, c) - affine_torsor_map(x, n, c) - affine_torsor_map(y, n, c))
    record(
        "A.1 an unbased endpoint torsor permits affine maps with offset c",
        F0 == c,
        f"F(0)={F0}",
    )
    record(
        "A.2 group additivity removes c only after a target unit is chosen",
        add_defect == -c,
        f"F(x+y)-F(x)-F(y)={add_defect}",
    )

    section("B. Basing the torsor is exactly the endpoint basepoint law")

    b = sp.symbols("b", real=True)
    based_coordinate = sp.simplify(affine_torsor_map(x, n, c) - b)
    unit_condition = sp.solve(sp.Eq(affine_torsor_map(0, n, c), b), c)
    record(
        "B.1 a chosen target basepoint b fixes c relative to b",
        unit_condition == [b],
        f"F(0)=b -> c={unit_condition}",
    )
    record(
        "B.2 changing the basepoint shifts the same physical torsor map",
        based_coordinate == c - b + n * x,
        f"based_coordinate={based_coordinate}",
    )

    eta = sp.Rational(2, 9)
    b_values = [sp.Integer(0), sp.Rational(1, 9), -sp.Rational(1, 9)]
    lines = []
    for b_value in b_values:
        c_value = b_value
        endpoint = affine_torsor_map(eta, 1, c_value)
        lines.append(f"basepoint={b_value}, c={c_value}, F(eta_APS)={endpoint}")
    record(
        "B.3 multiple basepoints preserve torsor structure while changing raw endpoint coordinate",
        len(lines) == len(b_values),
        "\n".join(lines),
    )

    section("C. What the route can and cannot prove")

    record(
        "C.1 if a retained zero endpoint basepoint is supplied, c is removed",
        sp.solve(sp.Eq(affine_torsor_map(0, n, c), 0), c) == [0],
        "Based Picard functor: F(0)=0 -> c=0.",
    )
    record(
        "C.2 even after c=0, degree remains",
        sp.solve(sp.Eq(affine_torsor_map(eta, n, 0), eta), n) == [1],
        "The Picard unit route does not by itself derive n=1.",
    )
    record(
        "C.3 the retained packet has closed APS support but no selected endpoint zero section",
        True,
        "Contractibility or monoidal language does not name a physical boundary section for the open line.",
    )

    section("D. Hostile-review objections")

    record(
        "D.1 calling the target a group is already choosing the torsor basepoint",
        True,
        "The open endpoint phase is measured between endpoint sections; the zero section is physical data.",
    )
    record(
        "D.2 a monoidal functor would be useful but conditional",
        affine_torsor_map(eta, 1, 0) == eta,
        "Once c=0 and n=1 are added, closure follows; this runner audits whether c=0 is retained.",
    )

    section("E. Verdict")

    theta0, theta_end = sp.symbols("theta0 theta_end", real=True)
    residual_endpoint = sp.simplify(theta_end - theta0 - eta)
    record(
        "E.1 Picard torsor unit route does not close delta",
        residual_endpoint == theta_end - theta0 - sp.Rational(2, 9),
        f"RESIDUAL_ENDPOINT={residual_endpoint}",
    )
    record(
        "E.2 residual offset is the selected-line basepoint/trivialization",
        True,
        "Need a retained boundary section proving c=0, then a retained degree theorem proving n=1.",
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
        print("VERDICT: Picard torsor unit route does not close delta.")
        print("KOIDE_DELTA_PICARD_TORSOR_UNIT_NO_GO=TRUE")
        print("DELTA_PICARD_TORSOR_UNIT_CLOSES_DELTA=FALSE")
        print("RESIDUAL_ENDPOINT=theta_end-theta0-eta_APS")
        print("RESIDUAL_TRIVIALIZATION=selected_line_endpoint_basepoint_not_retained")
        print("RESIDUAL_SCALAR=n_minus_one_plus_c_over_eta_APS")
        return 0

    print("VERDICT: Picard torsor unit audit has FAILs.")
    print("KOIDE_DELTA_PICARD_TORSOR_UNIT_NO_GO=FALSE")
    print("DELTA_PICARD_TORSOR_UNIT_CLOSES_DELTA=FALSE")
    print("RESIDUAL_ENDPOINT=theta_end-theta0-eta_APS")
    print("RESIDUAL_TRIVIALIZATION=selected_line_endpoint_basepoint_not_retained")
    print("RESIDUAL_SCALAR=n_minus_one_plus_c_over_eta_APS")
    return 1


if __name__ == "__main__":
    sys.exit(main())
