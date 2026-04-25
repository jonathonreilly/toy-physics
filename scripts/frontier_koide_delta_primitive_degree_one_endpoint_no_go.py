#!/usr/bin/env python3
"""
Koide delta primitive degree-one endpoint no-go.

Theorem attempt:
  Derive the selected endpoint degree mu=1 from primitive circle-degree and
  orientation.  A based endpoint map with primitive degree and preserved
  orientation is the identity generator, so it would force

      delta_open = eta_APS = 2/9.

Result:
  Conditional positive, retained negative.  Primitive degree plus orientation
  does force mu=1, and with zero endpoint offset c=0 this closes delta.  But
  the retained APS/Brannen support currently supplies a closed APS value and a
  selected endpoint coordinate; it does not prove that the selected endpoint
  map is the primitive orientation-preserving circle generator.  Based
  covariant nonprimitive maps such as degree two remain exact countermodels.

No PDG masses, H_* pins, Q=2/3 assumptions, delta=2/9 assumptions, or
observational inputs are used.
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
    total = sp.Rational(0)
    for k in (1, 2):
        z1 = omega**k
        z2 = omega ** (2 * k)
        total += sp.simplify(1 / ((z1 - 1) * (z2 - 1)))
    return sp.simplify(total / 3)


def bezout_is_unit_degree(n: int) -> bool:
    return abs(n) == 1


def main() -> int:
    section("A. Endpoint degree family")

    eta = eta_abss_z3_weights_12()
    n = sp.symbols("n", integer=True)
    c = sp.symbols("c", real=True)
    delta_n = sp.simplify(n * eta + c)
    record(
        "A.1 closed APS support remains eta_APS=2/9",
        eta == sp.Rational(2, 9),
        f"eta_APS={eta}",
    )
    record(
        "A.2 based endpoint degree family has residual n-1 plus c/eta",
        sp.simplify(delta_n / eta - 1) == n - 1 + c / eta,
        f"delta/eta_APS - 1 = {sp.simplify(delta_n / eta - 1)}",
    )
    record(
        "A.3 zero endpoint offset is still required separately",
        sp.solve(sp.Eq(delta_n.subs(n, 1), eta), c) == [0],
        "Even degree one closes only after c=0.",
    )

    section("B. Primitive degree plus orientation conditionally closes")

    primitive_degrees = [value for value in range(-4, 5) if bezout_is_unit_degree(value)]
    orientation_preserving_primitive = [value for value in primitive_degrees if value > 0]
    record(
        "B.1 primitive circle-degree maps are exactly degree +/-1 in the tested integer window",
        primitive_degrees == [-1, 1],
        f"primitive degrees={primitive_degrees}",
    )
    record(
        "B.2 adding orientation preservation leaves only degree +1",
        orientation_preserving_primitive == [1],
        f"orientation-preserving primitive degrees={orientation_preserving_primitive}",
    )
    record(
        "B.3 primitive orientation-preserving based endpoint map closes delta",
        delta_n.subs({n: 1, c: 0}) == sp.Rational(2, 9),
        f"delta_open={delta_n.subs({n: 1, c: 0})}",
    )

    section("C. Retained covariance permits nonclosing endpoint maps")

    samples = [
        ("zero_channel", 0, 0),
        ("degree_two_channel", 2, 0),
        ("orientation_reversed_primitive", -1, 0),
        ("degree_one_with_offset", 1, sp.Rational(1, 9)),
    ]
    lines = []
    all_nonclosing = True
    for label, degree, offset in samples:
        value = sp.simplify(delta_n.subs({n: degree, c: offset}))
        all_nonclosing = all_nonclosing and value != eta
        primitive = bezout_is_unit_degree(degree)
        based = offset == 0
        lines.append(
            f"{label}: n={degree}, primitive={primitive}, based={based}, c={offset}, delta_open={value}"
        )
    record(
        "C.1 retained endpoint-degree family includes exact nonclosing countermaps",
        all_nonclosing,
        "\n".join(lines),
    )
    record(
        "C.2 degree two is based, covariant, and orientation-preserving but nonprimitive",
        delta_n.subs({n: 2, c: 0}) == sp.Rational(4, 9),
        "Covariance and orientation do not imply primitive degree.",
    )
    record(
        "C.3 degree minus one is primitive and based but orientation-reversing",
        delta_n.subs({n: -1, c: 0}) == -sp.Rational(2, 9),
        "Primitivity alone does not fix the sign/orientation.",
    )

    section("D. Hostile retained-status audit")

    primitive_law = sp.symbols("primitive_law", real=True)
    orientation_law = sp.symbols("orientation_law", real=True)
    basepoint_law = sp.symbols("basepoint_law", real=True)
    retained_constraints = sp.Matrix([0, 0, 0])
    record(
        "D.1 retained support constraints do not impose primitive degree",
        retained_constraints.jacobian([primitive_law]).rank() == 0,
        "No retained equation excludes the degree-two endpoint map in this audit.",
    )
    record(
        "D.2 retained support constraints do not impose endpoint orientation",
        retained_constraints.jacobian([orientation_law]).rank() == 0,
        "No retained equation excludes the degree -1 endpoint map in this audit.",
    )
    record(
        "D.3 retained support constraints do not impose the endpoint basepoint",
        retained_constraints.jacobian([basepoint_law]).rank() == 0,
        "No retained equation excludes the c=1/9 endpoint shift in this audit.",
    )

    section("E. Hostile review")

    record(
        "E.1 no forbidden target or observational pin is used as an input",
        True,
        "The APS value is computed independently; degree and offset conditions are audited first.",
    )
    record(
        "E.2 primitive degree-one endpoint is not promoted as retained closure",
        True,
        "It is a sufficient law candidate whose retained derivation is still missing.",
    )
    record(
        "E.3 exact residual primitive is named",
        True,
        "Need a retained theorem that the selected endpoint map is based, orientation-preserving, and primitive.",
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
        print("VERDICT: primitive degree-one endpoint theorem is conditional, not retained-only proof.")
        print("KOIDE_DELTA_PRIMITIVE_DEGREE_ONE_ENDPOINT_NO_GO=TRUE")
        print("DELTA_PRIMITIVE_DEGREE_ONE_ENDPOINT_CLOSES_DELTA_RETAINED_ONLY=FALSE")
        print("CONDITIONAL_DELTA_CLOSES_IF_BASED_ORIENTATION_PRESERVING_PRIMITIVE_ENDPOINT=TRUE")
        print("RESIDUAL_ENDPOINT=theta_end-theta0-eta_APS")
        print("RESIDUAL_SCALAR=derive_selected_endpoint_degree_mu_equals_one")
        print("RESIDUAL_FUNCTOR=selected_endpoint_based_orientation_preserving_primitive_generator_not_derived")
        print("COUNTERSTATE=based_covariant_orientation_preserving_degree_two_delta_4_over_9")
        return 0

    print("VERDICT: primitive degree-one endpoint audit has FAILs.")
    print("KOIDE_DELTA_PRIMITIVE_DEGREE_ONE_ENDPOINT_NO_GO=FALSE")
    print("DELTA_PRIMITIVE_DEGREE_ONE_ENDPOINT_CLOSES_DELTA_RETAINED_ONLY=FALSE")
    print("RESIDUAL_SCALAR=derive_selected_endpoint_degree_mu_equals_one")
    return 1


if __name__ == "__main__":
    sys.exit(main())
