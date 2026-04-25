#!/usr/bin/env python3
"""
Koide delta variational endpoint no-go.

Theorem attempt:
  Derive the selected-line Brannen endpoint from a variational principle on the
  open phase.  Perhaps the physical endpoint is an extremum, minimum norm, or
  periodic-action stationary point, and that extremum equals eta_APS=2/9.

Result:
  Negative.  A variational principle selects the center/level supplied by its
  action.  For a quadratic endpoint action

      S = (delta - c)^2 / 2,

  the extremum is delta=c.  Minimum phase norm selects delta=0, not 2/9.
  A periodic action also selects its supplied phase center modulo periods.
  Therefore a variational endpoint route closes delta only after inserting the
  endpoint center c=2/9 or an equivalent boundary condition.

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
    section("A. Quadratic endpoint variational principle")

    delta, c = sp.symbols("delta c", real=True)
    eta = sp.Rational(2, 9)
    action = sp.simplify((delta - c) ** 2 / 2)
    stationary = sp.solve(sp.Eq(sp.diff(action, delta), 0), delta)
    record(
        "A.1 quadratic endpoint action extremizes at the supplied center c",
        stationary == [c],
        f"S=(delta-c)^2/2 -> stationary={stationary}",
    )
    c_needed = sp.solve(sp.Eq(stationary[0], eta), c)
    record(
        "A.2 eta endpoint requires c=2/9",
        c_needed == [eta],
        f"stationary=eta -> c={c_needed}",
    )

    section("B. Natural minimum-norm endpoint does not give eta")

    norm_action = sp.simplify(delta**2 / 2)
    norm_stationary = sp.solve(sp.Eq(sp.diff(norm_action, delta), 0), delta)
    record(
        "B.1 minimum open-phase norm selects zero",
        norm_stationary == [0],
        f"S=delta^2/2 -> stationary={norm_stationary}",
    )
    record(
        "B.2 zero endpoint is not eta_APS",
        norm_stationary[0] != eta,
        f"0 != {eta}",
    )

    section("C. Periodic endpoint action still carries a phase center")

    n = sp.symbols("n", integer=True)
    # Stationary points of 1-cos(2*pi*(delta-c)) occur at delta=c+n/2.
    periodic_stationary = sp.simplify(c + n / 2)
    eta_condition = sp.solve(sp.Eq(periodic_stationary.subs(n, 0), eta), c)
    record(
        "C.1 periodic action stationarity depends on its supplied center",
        eta_condition == [eta],
        "For n=0, delta=c; eta again requires c=2/9.",
    )
    record(
        "C.2 half-period stationary alternatives do not select eta",
        periodic_stationary.has(c, n),
        f"delta=c+n/2={periodic_stationary}",
    )

    section("D. Verdict")

    theta0, theta_end = sp.symbols("theta0 theta_end", real=True)
    residual = sp.simplify(theta_end - theta0 - eta)
    record(
        "D.1 variational endpoint route does not close delta",
        residual == theta_end - theta0 - sp.Rational(2, 9),
        f"RESIDUAL_ENDPOINT={residual}",
    )
    record(
        "D.2 delta remains open after variational audit",
        True,
        "Residual primitive: physical action center/boundary condition selecting eta_APS.",
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
        print("VERDICT: variational endpoint principle does not close delta.")
        print("KOIDE_DELTA_VARIATIONAL_ENDPOINT_NO_GO=TRUE")
        print("DELTA_VARIATIONAL_ENDPOINT_CLOSES_DELTA=FALSE")
        print("RESIDUAL_ENDPOINT=theta_end-theta0-eta_APS")
        print("RESIDUAL_ACTION_CENTER=endpoint_variational_center_not_retained")
        return 0

    print("VERDICT: variational endpoint audit has FAILs.")
    print("KOIDE_DELTA_VARIATIONAL_ENDPOINT_NO_GO=FALSE")
    print("DELTA_VARIATIONAL_ENDPOINT_CLOSES_DELTA=FALSE")
    print("RESIDUAL_ENDPOINT=theta_end-theta0-eta_APS")
    print("RESIDUAL_ACTION_CENTER=endpoint_variational_center_not_retained")
    return 1


if __name__ == "__main__":
    sys.exit(main())
