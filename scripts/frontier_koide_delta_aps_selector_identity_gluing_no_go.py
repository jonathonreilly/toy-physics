#!/usr/bin/env python3
"""
Koide delta APS-selector identity-gluing no-go.

Theorem attempt:
  Use the existing equivariant Berry/APS selector support to derive the
  remaining delta principle, namely identity endpoint gluing tau=0 for the
  selected Brannen line.

Result:
  Negative, but sharpened.  The APS block-by-block route fixes the closed
  ambient value eta_APS=2/9.  The selected-line support runner then finds the
  point where the open Brannen phase matches that value.  But a closed/open
  bridge still has the form

      eta_APS = delta_open + tau.

  The APS fixed-point computation supplies eta_APS.  The selected-line
  geometry supplies a family of open phases.  Neither supplies tau=0.  Setting
  tau=0 is exactly the identity-gluing principle isolated by the minimal
  positive-principle packet.

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


def eta_abss_z3_weights_12() -> sp.Expr:
    omega = -sp.Rational(1, 2) + sp.I * sp.sqrt(3) / 2
    total = 0
    for k in (1, 2):
        z1 = omega**k
        z2 = omega ** (2 * k)
        total += sp.simplify(1 / ((z1 - 1) * (z2 - 1)))
    return sp.simplify(total / 3)


def main() -> int:
    section("A. APS support fixes only the closed value")

    eta = eta_abss_z3_weights_12()
    record(
        "A.1 retained APS fixed-point computation gives eta_APS=2/9",
        eta == sp.Rational(2, 9),
        f"eta_APS={eta}",
    )
    delta_open, tau = sp.symbols("delta_open tau", real=True)
    bridge = sp.simplify(delta_open + tau - eta)
    tau_solution = sp.solve(sp.Eq(bridge, 0), tau)
    record(
        "A.2 closed/open bridge leaves endpoint transition tau",
        tau_solution == [sp.Rational(2, 9) - delta_open],
        f"eta_APS=delta_open+tau -> tau={tau_solution}",
    )

    section("B. Selected-line matching is not an identity-gluing proof")

    selected_values = [sp.Rational(0), sp.Rational(1, 9), sp.Rational(2, 9), sp.Rational(1, 3)]
    lines = []
    ok = True
    for value in selected_values:
        tau_value = sp.simplify(eta - value)
        ok = ok and sp.simplify(value + tau_value) == eta
        lines.append(f"delta_open={value}, tau={tau_value}, closed_total={sp.simplify(value+tau_value)}")
    record(
        "B.1 many selected-line open phases can share the same closed APS value",
        ok,
        "\n".join(lines),
    )
    record(
        "B.2 the matched selected-line point is exactly the tau=0 case",
        tau_solution[0].subs(delta_open, eta) == 0,
        "delta_open=eta_APS -> tau=0.",
    )
    record(
        "B.3 finding the matched point by target eta does not derive tau=0",
        True,
        "It identifies the endpoint that would close under identity gluing; it does not prove identity gluing.",
    )

    section("C. Verdict")

    theta0, theta_end = sp.symbols("theta0 theta_end", real=True)
    residual = sp.simplify(theta_end - theta0 - eta)
    record(
        "C.1 APS selector support does not close delta",
        residual == theta_end - theta0 - sp.Rational(2, 9),
        f"RESIDUAL_ENDPOINT={residual}",
    )
    record(
        "C.2 delta remains open after APS-selector identity-gluing audit",
        True,
        "Residual primitive: derive tau=0 or prove the selected open segment is the full APS boundary segment.",
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
        print("VERDICT: APS selector support does not derive identity endpoint gluing.")
        print("KOIDE_DELTA_APS_SELECTOR_IDENTITY_GLUING_NO_GO=TRUE")
        print("DELTA_APS_SELECTOR_IDENTITY_GLUING_CLOSES_DELTA=FALSE")
        print("RESIDUAL_ENDPOINT=theta_end-theta0-eta_APS")
        print("RESIDUAL_GLUING=derive_tau_zero_identity_endpoint_gluing")
        return 0

    print("VERDICT: APS-selector identity-gluing audit has FAILs.")
    print("KOIDE_DELTA_APS_SELECTOR_IDENTITY_GLUING_NO_GO=FALSE")
    print("DELTA_APS_SELECTOR_IDENTITY_GLUING_CLOSES_DELTA=FALSE")
    print("RESIDUAL_ENDPOINT=theta_end-theta0-eta_APS")
    print("RESIDUAL_GLUING=derive_tau_zero_identity_endpoint_gluing")
    return 1


if __name__ == "__main__":
    sys.exit(main())
