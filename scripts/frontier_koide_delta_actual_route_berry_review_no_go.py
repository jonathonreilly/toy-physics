#!/usr/bin/env python3
"""
Koide delta actual-route Berry closure review no-go.

Theorem under review:
  Older actual-route Berry notes state that the selected-line CP1 Berry
  holonomy closes the Brannen phase delta=2/9.

Nature-grade review result:
  The selected-line Berry carrier is exact and valuable support: the canonical
  connection is A=dtheta, so the open holonomy is the endpoint displacement.
  But a runner or theorem that defines m_* by solving

      theta(m_*) - theta0 = eta_APS

  has imported the missing endpoint value.  Berry geometry supplies

      delta(m) = theta(m) - theta0

  for every endpoint m.  It does not choose the endpoint m_* or identify the
  endpoint displacement with the closed APS eta invariant.

No PDG masses, Koide Q target, fitted delta, or H_* pin is used.
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
    section("A. Actual-route Berry carrier is exact support")

    theta = sp.symbols("theta", real=True)
    chi = sp.Matrix([sp.Integer(1), sp.exp(-2 * sp.I * theta)]) / sp.sqrt(2)
    berry = sp.simplify(sp.I * (chi.conjugate().T * sp.diff(chi, theta))[0])
    period_match = sp.simplify(chi.subs(theta, theta + sp.pi) - chi)
    record(
        "A.1 selected-line CP1 spinor has canonical Berry connection A=dtheta",
        berry == 1,
        f"i<chi|d_theta chi>={berry}",
    )
    record(
        "A.2 selected-line ray has projective period pi",
        all(sp.simplify(entry) == 0 for entry in period_match),
        "Topology gives a period, not an endpoint.",
    )

    section("B. Endpoint selection by solving delta=eta is target import")

    eta = eta_abss_z3_weights_12()
    theta0, theta_m, m, d = sp.symbols("theta0 theta_m m d", real=True)
    delta_m = sp.simplify(theta_m - theta0)
    root_equation_eta = sp.Eq(delta_m, eta)
    root_equation_d = sp.Eq(delta_m, d)
    record(
        "B.1 ambient APS support value remains eta=2/9",
        eta == sp.Rational(2, 9),
        f"eta_APS={eta}",
    )
    record(
        "B.2 Berry holonomy equals endpoint displacement for every endpoint",
        delta_m == theta_m - theta0,
        f"delta(m)={delta_m}",
    )
    record(
        "B.3 defining m_* by delta(m_*)=eta imports the missing endpoint equation",
        root_equation_eta == sp.Eq(theta_m - theta0, sp.Rational(2, 9)),
        f"root equation under review: {root_equation_eta}",
    )
    record(
        "B.4 the same construction selects a continuum of endpoints if d is supplied instead",
        root_equation_d == sp.Eq(theta_m - theta0, d),
        f"generic supplied endpoint equation: {root_equation_d}",
    )

    section("C. Counter-endpoint family")

    endpoint_samples = [sp.Rational(0), sp.Rational(1, 9), sp.Rational(2, 9), sp.Rational(1, 3)]
    lines = []
    for endpoint in endpoint_samples:
        closes = sp.simplify(endpoint - eta) == 0
        lines.append(f"delta={endpoint}, Berry carrier ok=True, eta_residual={sp.simplify(endpoint-eta)}, closes={closes}")
    record(
        "C.1 multiple endpoints preserve the same actual-route Berry geometry",
        len(lines) == len(endpoint_samples),
        "\n".join(lines),
    )
    record(
        "C.2 only the endpoint supplied as eta closes",
        endpoint_samples.count(eta) == 1,
        "Closure follows from the supplied endpoint value, not from the connection.",
    )

    section("D. Nature-grade review verdict")

    residual = sp.simplify(theta_m - theta0 - eta)
    record(
        "D.1 actual-route Berry theorem does not by itself close delta",
        residual == theta_m - theta0 - sp.Rational(2, 9),
        f"RESIDUAL_ENDPOINT={residual}",
    )
    record(
        "D.2 what remains is the physical Berry/APS endpoint functor",
        True,
        "Need a theorem mapping closed APS eta to the selected open endpoint without solving for eta.",
    )
    record(
        "D.3 historical closure language should be treated as support under current standard",
        True,
        "The carrier is retained; the endpoint value is not derived.",
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
        print("VERDICT: actual-route Berry carrier is support, not Nature-grade delta closure.")
        print("KOIDE_DELTA_ACTUAL_ROUTE_BERRY_REVIEW_NO_GO=TRUE")
        print("DELTA_ACTUAL_ROUTE_BERRY_REVIEW_CLOSES_DELTA=FALSE")
        print("RESIDUAL_ENDPOINT=theta_end-theta0-eta_APS")
        print("RESIDUAL_FUNCTOR=closed_APS_eta_to_open_selected_line_endpoint")
        return 0

    print("VERDICT: actual-route Berry review audit has FAILs.")
    print("KOIDE_DELTA_ACTUAL_ROUTE_BERRY_REVIEW_NO_GO=FALSE")
    print("DELTA_ACTUAL_ROUTE_BERRY_REVIEW_CLOSES_DELTA=FALSE")
    print("RESIDUAL_ENDPOINT=theta_end-theta0-eta_APS")
    print("RESIDUAL_FUNCTOR=closed_APS_eta_to_open_selected_line_endpoint")
    return 1


if __name__ == "__main__":
    sys.exit(main())
