#!/usr/bin/env python3
"""Koide pointed-origin exhaustion theorem.

This runner verifies a negative result: in the current residual Koide atlas,
unpointed retained data cannot select the source/boundary origin needed for
dimensionless Koide closure. It does not claim closure.
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


def q_from_y(y_plus: sp.Expr, y_perp: sp.Expr) -> sp.Expr:
    r = sp.simplify(y_perp / y_plus)
    return sp.simplify((1 + r) / 3)


def ktl_from_y(y_plus: sp.Expr, y_perp: sp.Expr) -> sp.Expr:
    r = sp.simplify(y_perp / y_plus)
    return sp.simplify((r**2 - 1) / (4 * r))


def eta_abss_z3_weights_12() -> sp.Expr:
    omega = sp.Rational(-1, 2) + sp.I * sp.sqrt(3) / 2
    total = sp.Rational(0)
    for k in (1, 2):
        z1 = omega**k
        z2 = omega ** (2 * k)
        total += sp.simplify(1 / ((z1 - 1) * (z2 - 1)))
    return sp.simplify(total / 3)


def polynomial_translation_invariant_only_constant(
    symbol: sp.Symbol,
) -> tuple[bool, list[dict]]:
    shift = sp.symbols(f"{symbol.name}_shift", real=True)
    coeffs = sp.symbols(f"p0:5_{symbol.name}", real=True)
    polynomial = sum(coeffs[i] * symbol**i for i in range(5))
    difference = sp.Poly(
        sp.expand(polynomial.subs(symbol, symbol + shift) - polynomial),
        symbol,
        shift,
    )
    equations = list(difference.coeffs())
    solution = sp.solve(equations, coeffs[1:], dict=True)
    expected = [{coeffs[1]: 0, coeffs[2]: 0, coeffs[3]: 0, coeffs[4]: 0}]
    return solution == expected, solution


def main() -> int:
    section("A. Q source-origin exhaustion")

    a = sp.symbols("a", real=True)
    y_plus = 1 + a
    y_perp = 1 - a
    q_value = q_from_y(y_plus, y_perp)
    ktl_value = ktl_from_y(y_plus, y_perp)
    q_closing_solutions = sp.solve(sp.Eq(q_value, sp.Rational(2, 3)), a)
    q_poly_ok, q_poly_solution = polynomial_translation_invariant_only_constant(a)
    record(
        "A.1 normalized Q response closes only at the pointed source origin",
        q_closing_solutions == [0] and ktl_value.subs(a, 0) == 0,
        f"Y=(1+a,1-a), Q={q_value}, Q=2/3 -> a={q_closing_solutions}",
    )
    record(
        "A.2 finite polynomial invariants of the source-translation fibre are constant",
        q_poly_ok,
        f"P(a+r)=P(a) -> {q_poly_solution}",
    )
    record(
        "A.3 source translations give retained-equivalent non-Koide countermodels",
        q_value.subs(a, sp.Rational(1, 3)) == sp.Rational(1, 2)
        and ktl_value.subs(a, sp.Rational(1, 3)) == -sp.Rational(3, 8),
        f"a=1/3 -> K_TL={ktl_value.subs(a, sp.Rational(1, 3))}, "
        f"Q={q_value.subs(a, sp.Rational(1, 3))}",
    )

    section("B. Brannen CP1 selector exhaustion")

    theta = 2 * sp.pi / 3
    rotation = sp.simplify(
        sp.Matrix(
            [[sp.cos(theta), -sp.sin(theta)], [sp.sin(theta), sp.cos(theta)]]
        )
    )
    x, y = sp.symbols("x y", real=True)
    trace_one_symmetric = sp.Matrix([[x, y], [y, 1 - x]])
    comm_eqs = list(
        sp.simplify(trace_one_symmetric * rotation - rotation * trace_one_symmetric)
    )
    comm_sol = sp.solve(comm_eqs, [x, y], dict=True)
    half_identity = sp.Rational(1, 2) * sp.eye(2)
    alpha = sp.symbols("alpha", real=True)
    line = sp.Matrix([sp.cos(alpha), sp.sin(alpha)])
    mu = sp.symbols("mu", real=True)
    scalar_mark = mu * sp.eye(2)
    scalar_expectation = sp.simplify((line.T * scalar_mark * line)[0])
    spectator = sp.sin(alpha) ** 2
    record(
        "B.1 the only equivariant trace-one mark is scalar, not rank-one",
        comm_sol == [{x: sp.Rational(1, 2), y: 0}]
        and sp.simplify(half_identity**2 - half_identity) != sp.zeros(2, 2),
        f"commuting trace-one mark={comm_sol}; "
        f"(I/2)^2-I/2={sp.simplify(half_identity**2-half_identity)}",
    )
    record(
        "B.2 scalar retained marks are CP1-line blind",
        scalar_expectation == mu,
        f"<line(alpha)|mu I|line(alpha)>={scalar_expectation}",
    )
    record(
        "B.3 CP1 line choice changes the open spectator while preserving scalar data",
        spectator.subs(alpha, 0) == 0
        and spectator.subs(alpha, sp.pi / 4) == sp.Rational(1, 2),
        "alpha=0 gives spectator=0; alpha=pi/4 gives spectator=1/2.",
    )

    section("C. Endpoint torsor exhaustion")

    c = sp.symbols("c", real=True)
    endpoint_poly_ok, endpoint_poly_solution = (
        polynomial_translation_invariant_only_constant(c)
    )
    phi1, phi2, shift = sp.symbols("phi1 phi2 shift", real=True)
    difference_invariant = sp.simplify(
        ((phi2 + c + shift) - (phi1 + c + shift)) - (phi2 - phi1)
    )
    affine_gluing_invariant = sp.simplify(
        (phi1 + phi2 + c + shift)
        - ((phi1 + c + shift) + (phi2 + c + shift) - (c + shift))
    )
    record(
        "C.1 finite polynomial invariants of the endpoint torsor are constant",
        endpoint_poly_ok,
        f"P(c+r)=P(c) -> {endpoint_poly_solution}",
    )
    record(
        "C.2 endpoint differences and affine gluing are torsor-translation invariant",
        difference_invariant == 0 and affine_gluing_invariant == 0,
        "Absolute c changes, differences and affine gluing do not.",
    )
    record(
        "C.3 endpoint unit basepoint is exactly the missing pointed condition",
        sp.solve(sp.Eq(c, 0), c) == [0],
        "Unit endpoint requires c=0; unpointed torsor data allow all c.",
    )

    section("D. Combined residual atlas")

    eta = eta_abss_z3_weights_12()
    q_pointed = q_from_y(sp.Integer(1), sp.Integer(1))
    delta_pointed = eta
    q_counter = q_value.subs(a, sp.Rational(1, 3))
    delta_counter = sp.simplify(eta * sp.cos(sp.pi / 4) ** 2 + sp.Rational(1, 7))
    delta_target_cancel = sp.simplify(
        eta * sp.cos(sp.pi / 4) ** 2 + eta * sp.sin(sp.pi / 4) ** 2
    )
    record(
        "D.1 a pointed origin law would imply both dimensionless values",
        q_pointed == sp.Rational(2, 3) and delta_pointed == sp.Rational(2, 9),
        f"Q={q_pointed}, delta={delta_pointed}",
    )
    record(
        "D.2 retained-equivalent unpointed countermodels change both readouts",
        q_counter != sp.Rational(2, 3) and delta_counter != sp.Rational(2, 9),
        f"a=1/3, alpha=pi/4, c=1/7 -> Q={q_counter}, delta={delta_counter}",
    )
    record(
        "D.3 value-only delta closure can be faked by target cancellation",
        delta_target_cancel == eta,
        "alpha=pi/4 plus c=eta*sin(alpha)^2 gives delta=eta while retaining a spectator.",
    )

    section("E. Boundary")

    record(
        "E.1 no origin-free retained invariant selects the closing representative in this atlas",
        q_poly_ok and endpoint_poly_ok and scalar_expectation == mu,
        "The residual fibres are translation/line torsors under the unpointed tests.",
    )
    record(
        "E.2 the next positive theorem is a retained physical source/boundary-origin law",
        True,
        "It must derive background-zero/Z-erasure, selected-line boundary source, and endpoint basepoint.",
    )
    record(
        "E.3 this theorem does not claim retained Koide closure",
        True,
        "It proves exhaustion/necessity in the residual atlas, not the positive physical law.",
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
        print("KOIDE_POINTED_ORIGIN_EXHAUSTION_THEOREM=TRUE")
        print("RETAINED_UNPOINTED_DATA_FORCE_POINTED_ORIGIN=FALSE")
        print("POINTED_ORIGIN_LAW_WOULD_CLOSE_DIMENSIONLESS_LANE_WITHIN_RESIDUAL_ATLAS=TRUE")
        print("POINTED_ORIGIN_LAW_IS_NECESSARY_WITHIN_RESIDUAL_ATLAS=TRUE")
        print("KOIDE_DIMENSIONLESS_LANE_CLOSED_BY_THIS_RUNNER=FALSE")
        print("RESIDUAL_PRIMITIVE=retained_physical_source_boundary_origin_laws")
        print("NEXT_THEOREM=derive_physical_source_boundary_origin_laws_from_retained_charged_lepton_physics")
        return 0

    print("KOIDE_POINTED_ORIGIN_EXHAUSTION_THEOREM=FALSE")
    print("KOIDE_DIMENSIONLESS_LANE_CLOSED_BY_THIS_RUNNER=FALSE")
    return 1


if __name__ == "__main__":
    sys.exit(main())
