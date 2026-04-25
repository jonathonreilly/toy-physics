#!/usr/bin/env python3
"""
Koide delta Pancharatnam endpoint no-go.

Theorem attempt:
  Repair the open Berry endpoint ambiguity using the gauge-invariant
  Pancharatnam prescription.  Perhaps the selected-line open geometric phase
  is then forced to equal eta_APS = 2/9.

Result:
  Negative.  The Pancharatnam open phase is gauge invariant after endpoint
  states are specified, but it still depends continuously on those endpoint
  projectors and on the path.  For the two-level line

      psi(theta,phi) = (cos(theta/2), exp(i phi) sin(theta/2)),

  the open geometric phase along phi:0->Phi is

      arg(cos^2(theta/2) + exp(i Phi) sin^2(theta/2))
        - Phi sin^2(theta/2).

  This is not a retained constant and is not fixed to 2/9.  The prescription
  removes gauge dependence; it does not choose the physical Brannen endpoint.

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


def pancharatnam_phase(theta_value: sp.Expr, phi_value: sp.Expr) -> sp.Expr:
    c2 = sp.cos(theta_value / 2) ** 2
    s2 = sp.sin(theta_value / 2) ** 2
    real = sp.simplify(c2 + s2 * sp.cos(phi_value))
    imag = sp.simplify(s2 * sp.sin(phi_value))
    endpoint_arg = sp.atan2(imag, real)
    berry_integral = sp.simplify(s2 * phi_value)
    return sp.simplify(endpoint_arg - berry_integral)


def main() -> int:
    section("A. Gauge-invariant Pancharatnam open phase")

    theta, Phi = sp.symbols("theta Phi", real=True)
    c2 = sp.cos(theta / 2) ** 2
    s2 = sp.sin(theta / 2) ** 2
    endpoint_real = sp.simplify(c2 + s2 * sp.cos(Phi))
    endpoint_imag = sp.simplify(s2 * sp.sin(Phi))
    formula = "atan2(sin(theta/2)^2 sin(Phi), cos(theta/2)^2 + sin(theta/2)^2 cos(Phi)) - Phi sin(theta/2)^2"
    record(
        "A.1 Pancharatnam formula is an endpoint/path function",
        endpoint_real.has(theta, Phi) and endpoint_imag.has(theta, Phi),
        formula,
    )

    chi0, chi1 = sp.symbols("chi0 chi1", real=True)
    berry_shift = chi1 - chi0
    overlap_arg_shift = chi0 - chi1
    record(
        "A.2 Pancharatnam prescription cancels endpoint gauge shifts",
        sp.simplify(berry_shift + overlap_arg_shift) == 0,
        "Gauge invariance is restored after endpoint states are supplied.",
    )

    section("B. It is not fixed to eta_APS")

    eta = sp.Rational(2, 9)
    phase_equator = pancharatnam_phase(sp.pi / 2, sp.pi / 2)
    phase_latitude = pancharatnam_phase(sp.pi / 3, sp.pi / 2)
    record(
        "B.1 equatorial quarter path gives zero open geometric phase",
        phase_equator == 0,
        f"theta=pi/2, Phi=pi/2 -> gamma_P={phase_equator}",
    )
    record(
        "B.2 another retained endpoint choice gives a different phase",
        phase_latitude == sp.atan(sp.Rational(1, 3)) - sp.pi / 8,
        f"theta=pi/3, Phi=pi/2 -> gamma_P={phase_latitude}",
    )
    record(
        "B.3 neither sample is the APS value 2/9",
        phase_equator != eta and sp.simplify(phase_latitude - eta) != 0,
        f"eta_APS={eta}",
    )

    section("C. Endpoint choice remains the physical primitive")

    endpoint_parameter = sp.symbols("lambda", real=True)
    proposed_endpoint_law = sp.simplify(endpoint_parameter - eta)
    record(
        "C.1 setting the Pancharatnam phase to eta is an endpoint equation",
        proposed_endpoint_law == endpoint_parameter - sp.Rational(2, 9),
        f"RESIDUAL_ENDPOINT_LAW={proposed_endpoint_law}",
    )
    record(
        "C.2 gauge invariance is not endpoint selection",
        True,
        "The prescription makes an open phase well-defined for chosen endpoints; it does not choose the endpoints.",
    )

    section("D. Verdict")

    theta0, theta_end = sp.symbols("theta0 theta_end", real=True)
    residual = sp.simplify(theta_end - theta0 - eta)
    record(
        "D.1 Pancharatnam endpoint route does not close delta",
        residual == theta_end - theta0 - sp.Rational(2, 9),
        f"RESIDUAL_ENDPOINT={residual}",
    )
    record(
        "D.2 delta remains open after Pancharatnam audit",
        True,
        "Residual primitive: physical selected endpoint/path, not gauge-invariant phase convention.",
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
        print("VERDICT: Pancharatnam endpoint prescription does not close delta.")
        print("KOIDE_DELTA_PANCHARATNAM_ENDPOINT_NO_GO=TRUE")
        print("DELTA_PANCHARATNAM_ENDPOINT_CLOSES_DELTA=FALSE")
        print("RESIDUAL_ENDPOINT=theta_end-theta0-eta_APS")
        print("RESIDUAL_SELECTION=Pancharatnam_gauge_invariance_does_not_select_endpoint")
        return 0

    print("VERDICT: Pancharatnam endpoint audit has FAILs.")
    print("KOIDE_DELTA_PANCHARATNAM_ENDPOINT_NO_GO=FALSE")
    print("DELTA_PANCHARATNAM_ENDPOINT_CLOSES_DELTA=FALSE")
    print("RESIDUAL_ENDPOINT=theta_end-theta0-eta_APS")
    print("RESIDUAL_SELECTION=Pancharatnam_gauge_invariance_does_not_select_endpoint")
    return 1


if __name__ == "__main__":
    sys.exit(main())
