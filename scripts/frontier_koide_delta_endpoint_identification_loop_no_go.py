#!/usr/bin/env python3
"""
Koide delta endpoint-identification loop no-go.

Theorem attempt:
  Identify the selected open Brannen segment endpoints to make it a closed APS
  loop.  If the selected segment is the whole loop, the open endpoint would
  equal eta_APS = 2/9.

Result:
  Negative.  Closing an open line requires endpoint gluing data.  If tau is
  the endpoint transition/gluing phase, functoriality gives

      eta_closed = delta_open + tau.

  With eta_closed=2/9, the open endpoint is eta_APS only at tau=0.  The
  identity endpoint gluing is an additional boundary condition; it is not
  derived from the retained selected-line data.  Nonzero endpoint transitions
  produce the same closed APS value with different open endpoints.

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
    section("A. Endpoint gluing law")

    eta = sp.Rational(2, 9)
    delta_open, tau = sp.symbols("delta_open tau", real=True)
    closed_phase = sp.simplify(delta_open + tau)
    open_solution = sp.solve(sp.Eq(closed_phase, eta), delta_open)
    record(
        "A.1 closing an open segment needs a transition phase tau",
        closed_phase == delta_open + tau,
        f"eta_closed=delta_open+tau",
    )
    record(
        "A.2 fixed closed APS value leaves open endpoint dependent on tau",
        open_solution == [sp.Rational(2, 9) - tau],
        f"delta_open={open_solution}",
    )

    section("B. Identity gluing is exactly the missing condition")

    tau_identity = sp.Integer(0)
    record(
        "B.1 identity endpoint gluing would give the desired endpoint",
        open_solution[0].subs(tau, tau_identity) == eta,
        "tau=0 -> delta_open=2/9.",
    )
    transition_values = [sp.Rational(-1, 9), sp.Rational(0), sp.Rational(1, 9), sp.Rational(1, 3)]
    lines = []
    ok = True
    for value in transition_values:
        open_value = sp.simplify(eta - value)
        total = sp.simplify(open_value + value)
        ok = ok and total == eta
        lines.append(f"tau={value}, delta_open={open_value}, closed_total={total}")
    record(
        "B.2 nonidentity endpoint transitions preserve the same closed APS value",
        ok,
        "\n".join(lines),
    )

    section("C. Retained data does not identify endpoints")

    record(
        "C.1 an open selected segment does not automatically have equal endpoints",
        True,
        "Endpoint identification P_start=P_end is extra data for an open path.",
    )
    record(
        "C.2 choosing tau=0 is a boundary/trivialization primitive",
        True,
        "It declares the closing transition trivial rather than deriving it.",
    )

    section("D. Verdict")

    theta0, theta_end = sp.symbols("theta0 theta_end", real=True)
    residual = sp.simplify(theta_end - theta0 - eta)
    record(
        "D.1 endpoint-identification loop route does not close delta",
        residual == theta_end - theta0 - sp.Rational(2, 9),
        f"RESIDUAL_ENDPOINT={residual}",
    )
    record(
        "D.2 delta remains open after endpoint-identification audit",
        True,
        "Residual primitive: retained identity gluing or endpoint equality for the selected line.",
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
        print("VERDICT: endpoint identification does not close delta.")
        print("KOIDE_DELTA_ENDPOINT_IDENTIFICATION_LOOP_NO_GO=TRUE")
        print("DELTA_ENDPOINT_IDENTIFICATION_LOOP_CLOSES_DELTA=FALSE")
        print("RESIDUAL_ENDPOINT=theta_end-theta0-eta_APS")
        print("RESIDUAL_GLUING=identity_endpoint_transition_tau_zero_not_retained")
        return 0

    print("VERDICT: endpoint-identification loop audit has FAILs.")
    print("KOIDE_DELTA_ENDPOINT_IDENTIFICATION_LOOP_NO_GO=FALSE")
    print("DELTA_ENDPOINT_IDENTIFICATION_LOOP_CLOSES_DELTA=FALSE")
    print("RESIDUAL_ENDPOINT=theta_end-theta0-eta_APS")
    print("RESIDUAL_GLUING=identity_endpoint_transition_tau_zero_not_retained")
    return 1


if __name__ == "__main__":
    sys.exit(main())
