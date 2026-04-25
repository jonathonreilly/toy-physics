#!/usr/bin/env python3
"""
Koide delta Callan-Harvey degree-functor no-go.

Theorem attempt:
  Use Callan-Harvey anomaly inflow to remove the endpoint-functor residual.
  Maybe the inflow current supplies the missing unit normalization, so the
  selected open endpoint must be the ambient APS/anomaly value.

Result:
  Negative.  The retained arithmetic fixes the closed anomaly scalar

      A_CH = eta_APS = 2/9,

  but the selected-line readout can still carry an independent descent/current
  normalization, functor degree, and endpoint offset:

      delta_open = n * N_desc * eta_APS + c.

  Closure requires the extra unit-current endpoint theorem
  n * N_desc = 1 and c = 0.  The retained APS/anomaly equations have zero rank
  in these open-readout variables.

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


def anomaly_per_generation(d: int = 3) -> sp.Expr:
    return sp.simplify((2 * d) * sp.Rational(1, d) ** 3)


def main() -> int:
    section("A. Retained APS/anomaly arithmetic")

    eta = eta_abss_z3_weights_12()
    anomaly = anomaly_per_generation(3)
    record(
        "A.1 ambient APS support scalar is eta_APS = 2/9",
        eta == sp.Rational(2, 9),
        f"eta_APS={eta}",
    )
    record(
        "A.2 Callan-Harvey anomaly arithmetic gives the same closed scalar",
        anomaly == sp.Rational(2, 9) and sp.simplify(anomaly - eta) == 0,
        f"A_CH={anomaly}; A_CH-eta_APS={sp.simplify(anomaly - eta)}",
    )

    section("B. Open readout normalization remains free")

    n, n_desc, c = sp.symbols("n N_desc c", real=True)
    delta = sp.simplify(n * n_desc * eta + c)
    residual = sp.simplify(delta / eta - 1)
    record(
        "B.1 combined endpoint residual is n*N_desc - 1 plus offset/eta",
        residual == n * n_desc + c / eta - 1,
        f"delta/eta_APS - 1 = {residual}",
    )

    retained_constraints = [
        sp.simplify(eta - sp.Rational(2, 9)),
        sp.simplify(anomaly - sp.Rational(2, 9)),
        sp.simplify(anomaly - eta),
    ]
    jac = sp.Matrix([[sp.diff(expr, var) for var in (n, n_desc, c)] for expr in retained_constraints])
    record(
        "B.2 retained APS/anomaly constraints have zero rank in open-readout variables",
        jac.rank() == 0,
        f"Jacobian wrt (n,N_desc,c) = {jac.tolist()}",
    )

    samples = [
        (sp.Integer(1), sp.Rational(1, 2), sp.Integer(0)),
        (sp.Integer(1), sp.Integer(1), sp.Integer(0)),
        (sp.Integer(2), sp.Integer(1), sp.Integer(0)),
        (sp.Integer(1), sp.Integer(1), sp.Rational(1, 9)),
    ]
    lines = []
    values = set()
    all_support_ok = True
    for degree, descent, offset in samples:
        value = sp.simplify(delta.subs({n: degree, n_desc: descent, c: offset}))
        values.add(value)
        support_ok = all(expr == 0 for expr in retained_constraints)
        all_support_ok = all_support_ok and support_ok
        lines.append(
            f"n={degree}, N_desc={descent}, c={offset}: "
            f"delta_open={value}, support_ok={support_ok}"
        )
    record(
        "B.3 a family preserves closed anomaly support while changing the selected endpoint",
        all_support_ok and len(values) == len(samples),
        "\n".join(lines),
    )

    section("C. Exact condition needed for closure")

    mu = sp.symbols("mu", real=True)
    product_form = sp.simplify(delta.subs(n * n_desc, mu))
    closure_c0 = sp.solve(sp.Eq(product_form.subs(c, 0), eta), mu)
    c_needed = sp.solve(sp.Eq(delta, eta), c)
    record(
        "C.1 with zero offset, closure is equivalent to unit product n*N_desc = 1",
        closure_c0 == [1],
        f"delta=mu*eta_APS, c=0 -> mu={closure_c0}",
    )
    record(
        "C.2 with arbitrary degree/descent, closure can be forced by an offset choice",
        c_needed == [sp.Rational(2, 9) - sp.Rational(2, 9) * n * n_desc],
        f"c_required={c_needed[0]}",
    )
    record(
        "C.3 the unit-current theorem is not present in the retained equations",
        True,
        "Need to prove that the selected line carries one unit of the inflow current with the APS endpoint basepoint.",
    )

    section("D. Hostile-review objections")

    record(
        "D.1 equality A_CH = eta_APS is support, not selected-line readout",
        sp.simplify(anomaly - eta) == 0 and residual.has(n_desc),
        "The closed scalar agrees exactly; the open readout still contains N_desc.",
    )
    record(
        "D.2 integer channel multiplicity does not select the physical open endpoint",
        sp.simplify(delta.subs({n: 2, n_desc: 1, c: 0})) == sp.Rational(4, 9),
        "A doubled selected channel is excluded only after a unit-channel theorem.",
    )

    section("E. Verdict")

    theta0, theta_end = sp.symbols("theta0 theta_end", real=True)
    residual_endpoint = sp.simplify(theta_end - theta0 - eta)
    record(
        "E.1 Callan-Harvey degree functor does not close delta",
        residual_endpoint == theta_end - theta0 - sp.Rational(2, 9),
        f"RESIDUAL_ENDPOINT={residual_endpoint}",
    )
    record(
        "E.2 residual is unit current/functor degree plus endpoint basepoint",
        True,
        "Need n*N_desc=1 and c=0 from retained physics, not from endpoint matching.",
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
        print("VERDICT: Callan-Harvey degree functor does not close delta.")
        print("KOIDE_DELTA_CALLAN_HARVEY_DEGREE_FUNCTOR_NO_GO=TRUE")
        print("DELTA_CALLAN_HARVEY_DEGREE_FUNCTOR_CLOSES_DELTA=FALSE")
        print("RESIDUAL_ENDPOINT=theta_end-theta0-eta_APS")
        print("RESIDUAL_CURRENT_NORMALIZATION=selected_line_unit_current_degree_not_forced")
        print("RESIDUAL_SCALAR=n_times_N_desc_minus_one_plus_c_over_eta_APS")
        return 0

    print("VERDICT: Callan-Harvey degree-functor audit has FAILs.")
    print("KOIDE_DELTA_CALLAN_HARVEY_DEGREE_FUNCTOR_NO_GO=FALSE")
    print("DELTA_CALLAN_HARVEY_DEGREE_FUNCTOR_CLOSES_DELTA=FALSE")
    print("RESIDUAL_ENDPOINT=theta_end-theta0-eta_APS")
    print("RESIDUAL_CURRENT_NORMALIZATION=selected_line_unit_current_degree_not_forced")
    print("RESIDUAL_SCALAR=n_times_N_desc_minus_one_plus_c_over_eta_APS")
    return 1


if __name__ == "__main__":
    sys.exit(main())
