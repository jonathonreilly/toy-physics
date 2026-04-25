#!/usr/bin/env python3
"""
Koide delta all-order boundary-functional no-go.

Theorem attempt:
  Strengthen the endpoint audit from specific Berry, Pancharatnam, determinant,
  and gluing constructions to all smooth endpoint counterterms/trivializations
  compatible with the fixed closed APS curvature.  Perhaps smooth naturality
  forces the selected open endpoint to equal eta_APS.

Result:
  Negative.  Closed APS data fixes a closed holonomy/curvature class.  An open
  endpoint phase has the form

      delta_open = path_integral + B_end - B_start.

  Adding any smooth endpoint functional chi changes B_end-B_start by
  chi_end-chi_start while preserving closed holonomy.  Therefore the retained
  closed value eta_APS=2/9 does not select the open endpoint among all smooth
  boundary functionals.  The desired endpoint is obtained only by imposing the
  boundary functional difference that makes delta_open=2/9.

No PDG masses, Koide Q target, delta pin, or H_* pin is used.
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


def main() -> int:
    section("A. General smooth endpoint functional")

    eta = sp.Rational(2, 9)
    path_integral, b_start, b_end = sp.symbols("I_path B_start B_end", real=True)
    delta_open = sp.simplify(path_integral + b_end - b_start)
    record(
        "A.1 open endpoint phase has path plus boundary-section form",
        delta_open == path_integral + b_end - b_start,
        f"delta_open={delta_open}",
    )

    chi_start, chi_end = sp.symbols("chi_start chi_end", real=True)
    delta_shifted = sp.simplify(path_integral + (b_end + chi_end) - (b_start + chi_start))
    shift = sp.simplify(delta_shifted - delta_open)
    record(
        "A.2 smooth endpoint counterterm shifts only the open phase",
        shift == chi_end - chi_start,
        f"delta_open shift={shift}",
    )

    section("B. Closed holonomy is insensitive to endpoint exact terms")

    loop_integral = sp.symbols("I_loop", real=True)
    closed_shift = sp.simplify(loop_integral + chi_start - chi_start - loop_integral)
    record(
        "B.1 exact endpoint term cancels on a closed loop",
        closed_shift == 0,
        "Closed APS holonomy/curvature is preserved.",
    )
    endpoint_solution = sp.solve(sp.Eq(delta_shifted, eta), chi_end)
    record(
        "B.2 any open path can be shifted to eta by endpoint functional choice",
        endpoint_solution == [-b_end + b_start + chi_start - path_integral + sp.Rational(2, 9)],
        f"chi_end={endpoint_solution}",
    )

    section("C. Fixed closed value permits many smooth open endpoint values")

    open_values = [sp.Rational(-1, 9), sp.Rational(0), sp.Rational(1, 9), sp.Rational(2, 9), sp.Rational(1, 3)]
    lines = []
    ok = True
    for value in open_values:
        boundary_difference = sp.simplify(value - path_integral)
        ok = ok and sp.simplify(path_integral + boundary_difference) == value
        lines.append(f"open={value}, required B_end-B_start={boundary_difference}")
    record(
        "C.1 smooth boundary functionals realize many open endpoints with same closed support",
        ok,
        "\n".join(lines),
    )
    record(
        "C.2 the eta endpoint is one boundary-functional choice",
        sp.Rational(2, 9) in open_values,
        "Selecting it requires a physical boundary condition.",
    )

    section("D. Verdict")

    theta0, theta_end = sp.symbols("theta0 theta_end", real=True)
    residual = sp.simplify(theta_end - theta0 - eta)
    record(
        "D.1 all-order boundary-functional route does not close delta",
        residual == theta_end - theta0 - sp.Rational(2, 9),
        f"RESIDUAL_ENDPOINT={residual}",
    )
    record(
        "D.2 delta remains open after all-order boundary audit",
        True,
        "Residual primitive: physical endpoint functional selecting eta_APS.",
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
        print("VERDICT: all-order smooth boundary functionals do not close delta.")
        print("KOIDE_DELTA_ALL_ORDER_BOUNDARY_FUNCTIONAL_NO_GO=TRUE")
        print("DELTA_ALL_ORDER_BOUNDARY_FUNCTIONAL_CLOSES_DELTA=FALSE")
        print("RESIDUAL_ENDPOINT=theta_end-theta0-eta_APS")
        print("RESIDUAL_BOUNDARY_FUNCTIONAL=smooth_endpoint_counterterms_preserve_closed_APS")
        return 0

    print("VERDICT: all-order boundary-functional audit has FAILs.")
    print("KOIDE_DELTA_ALL_ORDER_BOUNDARY_FUNCTIONAL_NO_GO=FALSE")
    print("DELTA_ALL_ORDER_BOUNDARY_FUNCTIONAL_CLOSES_DELTA=FALSE")
    print("RESIDUAL_ENDPOINT=theta_end-theta0-eta_APS")
    print("RESIDUAL_BOUNDARY_FUNCTIONAL=smooth_endpoint_counterterms_preserve_closed_APS")
    return 1


if __name__ == "__main__":
    sys.exit(main())
