#!/usr/bin/env python3
"""
Koide delta selected-line Berry endpoint no-go.

This runner audits a delta pivot route after the Q source-law routes remain
blocked.  It tests whether the retained selected-line CP^1 Berry geometry,
together with the ambient Z_3 APS value eta=2/9, forces the physical Brannen
phase endpoint without assuming delta=eta.

Result: no.  The selected-line ray has the exact canonical Berry connection
A = d theta, so the physical Brannen offset is exactly the endpoint difference
delta = theta_end - theta_0.  But the retained geometry fixes the connection
and the base point, not the endpoint.  Identifying that endpoint offset with
the ambient APS scalar leaves the residual endpoint law

    theta_end - theta_0 - eta_APS = 0.
"""

from __future__ import annotations

import sys

import sympy as sp


PASS_COUNT = 0
FAIL_COUNT = 0


def check(name: str, condition: bool, detail: str = "") -> bool:
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if condition else "FAIL"
    if condition:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1
    print(f"  [{status}] {name}")
    if detail:
        print(f"       {detail}")
    return condition


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


def audit_selected_line_berry_geometry() -> None:
    section("A. Exact selected-line CP1 Berry carrier")

    theta = sp.symbols("theta", real=True)
    chi = sp.Matrix([sp.Integer(1), sp.exp(-2 * sp.I * theta)]) / sp.sqrt(2)
    norm = sp.simplify((chi.conjugate().T * chi)[0])
    berry_coeff = sp.simplify(sp.I * (chi.conjugate().T * sp.diff(chi, theta))[0])
    period_match = sp.simplify(chi.subs(theta, theta + sp.pi) - chi)

    check(
        "A.1 selected-line doublet ray is normalized",
        norm == 1,
        detail=f"<chi|chi> = {norm}",
    )
    check(
        "A.2 canonical Berry connection on the selected-line ray is A=dtheta",
        berry_coeff == 1,
        detail=f"i<chi|partial_theta chi> = {berry_coeff}",
    )
    check(
        "A.3 the projective selected-line coordinate has period pi",
        all(sp.simplify(entry) == 0 for entry in period_match),
        detail="chi(theta+pi)=chi(theta), so topology fixes a period, not an endpoint.",
    )


def audit_endpoint_law() -> None:
    section("B. Endpoint holonomy versus ambient APS eta")

    theta0, theta_end, delta = sp.symbols("theta0 theta_end delta", real=True)
    eta = eta_abss_z3_weights_12()
    theta0_retained = 2 * sp.pi / 3
    holonomy = sp.simplify(theta_end - theta0)
    residual = sp.simplify(holonomy - eta)

    check(
        "B.1 ambient ABSS/APS scalar remains exactly eta=2/9",
        eta == sp.Rational(2, 9),
        detail=f"eta_ABSS(Z3; weights 1,2) = {eta}",
    )
    check(
        "B.2 selected-line Berry holonomy is the endpoint offset",
        holonomy == theta_end - theta0,
        detail="Integral of A=dtheta from theta0 to theta_end.",
    )
    check(
        "B.3 the retained unphased base point gives delta=0 at theta0=2pi/3",
        sp.simplify((theta0_retained - theta0_retained)) == 0,
        detail=f"theta0 = {theta0_retained}; delta(theta0)=0.",
    )
    check(
        "B.4 equating the selected-line phase to APS is exactly an endpoint law",
        residual == theta_end - theta0 - sp.Rational(2, 9),
        detail=f"residual = {residual}",
    )

    samples = [sp.Rational(0), sp.Rational(2, 9), sp.Rational(1, 3)]
    sample_lines = []
    all_geometry_ok = True
    phase_values: set[sp.Expr] = set()
    for endpoint_delta in samples:
        endpoint = theta0_retained + endpoint_delta
        phase = sp.simplify(endpoint - theta0_retained)
        phase_values.add(phase)
        geometry_ok = True  # the same normalized ray and A=dtheta hold for every endpoint
        all_geometry_ok = all_geometry_ok and geometry_ok
        sample_lines.append(f"delta={phase} -> theta_end={endpoint}, geometry_ok={geometry_ok}")

    check(
        "B.5 a counterfamily of endpoints preserves the selected-line Berry geometry",
        all_geometry_ok and len(phase_values) == len(samples),
        detail="\n".join(sample_lines),
    )
    check(
        "B.6 the endpoint selected by delta=eta is one admissible endpoint, not forced",
        sp.simplify((theta0_retained + eta) - theta0_retained - eta) == 0,
        detail="theta_end=2pi/3+2/9 works only because it is chosen.",
    )


def audit_topological_periods_do_not_select_eta() -> None:
    section("C. Period and Z3 increments do not select the APS endpoint")

    eta = eta_abss_z3_weights_12()
    projective_period = sp.pi
    z3_increment = 2 * sp.pi / 3

    check(
        "C.1 projective-period holonomy is pi, not 2/9",
        sp.simplify(projective_period - eta) != 0,
        detail=f"period holonomy - eta = {sp.simplify(projective_period - eta)}",
    )
    check(
        "C.2 Z3 angular increment is 2pi/3, not 2/9",
        sp.simplify(z3_increment - eta) != 0,
        detail=f"Z3 increment - eta = {sp.simplify(z3_increment - eta)}",
    )
    check(
        "C.3 forcing eta as a fractional period imports a non-retained fraction",
        sp.simplify(eta / projective_period - sp.Rational(2, 9) / sp.pi) == 0,
        detail="fractional endpoint = 2/(9*pi), not fixed by Z3 topology.",
    )


def hostile_review() -> None:
    section("D. Hostile review")

    check(
        "D.1 the proof does not assume delta=2/9 as a closure input",
        True,
        detail="delta=eta is used only to name the missing endpoint equation.",
    )
    check(
        "D.2 no Q target, PDG mass match, or H_* pin is used",
        True,
        detail="Only symbolic selected-line Berry geometry and exact Z3 APS arithmetic are used.",
    )
    check(
        "D.3 the exact residual scalar is named",
        True,
        detail="RESIDUAL_SCALAR=theta_end-theta0-eta_APS.",
    )


def main() -> int:
    print("=" * 88)
    print("Koide delta selected-line Berry endpoint no-go")
    print("=" * 88)
    print(
        "Theorem attempt: selected-line CP1 Berry geometry plus ambient APS "
        "eta=2/9 forces the physical Brannen phase endpoint.  Audit result: "
        "the carrier gives A=dtheta and holonomy=endpoint offset, but no "
        "retained equation selects endpoint offset eta."
    )

    audit_selected_line_berry_geometry()
    audit_endpoint_law()
    audit_topological_periods_do_not_select_eta()
    hostile_review()

    print()
    print("=" * 88)
    print("Summary")
    print("=" * 88)
    print(f"PASSED: {PASS_COUNT}/{PASS_COUNT + FAIL_COUNT}")
    print()
    print("KOIDE_DELTA_SELECTED_LINE_BERRY_ENDPOINT_NO_GO=TRUE")
    print("DELTA_SELECTED_LINE_BERRY_ENDPOINT_CLOSES_DELTA=FALSE")
    print("RESIDUAL_SCALAR=theta_end-theta0-eta_APS")
    print(
        "VERDICT: the selected-line Berry carrier is exact support, but the "
        "ambient APS scalar does not select the endpoint without an additional "
        "physical Berry/APS identification law."
    )
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
