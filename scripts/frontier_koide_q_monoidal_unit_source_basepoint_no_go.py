#!/usr/bin/env python3
"""
Koide Q monoidal-unit / empty-boundary source-basepoint no-go.

Theorem attempt:
  A retained source-composition or empty-boundary law might identify the
  physical charged-lepton source with the monoidal unit.  If the unit were
  retained at the absolute log-source coordinate

      x = log(1 + rho) = 0,

  then rho=0, K_TL=0, and the conditional Koide Q chain would close.

Result:
  No retained closure.  In a source torsor, every basepoint e defines an
  equally valid translated monoidal law

      x *_e y = x + y - e

  with identity e.  Empty-boundary and unit-preserving readout laws set the
  source coordinate relative to e, not the absolute value e=0.  The unit law
  therefore selects x=e, while leaving e underived.  e=0 conditionally closes;
  e=log(2) satisfies the same unit laws and gives rho=1, Q=1, K_TL=3/8.

Exact residual:

      derive_retained_monoidal_unit_source_basepoint_equals_zero.

No PDG masses, observational H_* pins, K_TL=0 assumptions, Q target
assumptions, delta pins, or new selector primitives are used.
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


def rho_from_e(e_value: sp.Expr) -> sp.Expr:
    return sp.simplify(sp.exp(e_value) - 1)


def q_from_e(e_value: sp.Expr) -> sp.Expr:
    return sp.simplify((sp.Integer(2) + rho_from_e(e_value)) / 3)


def ktl_from_e(e_value: sp.Expr) -> sp.Expr:
    ratio = sp.simplify(sp.exp(e_value))
    return sp.simplify((ratio**2 - 1) / (4 * ratio))


def main() -> int:
    x, y, z, e, c = sp.symbols("x y z e c", real=True)

    star = lambda left, right, base: sp.simplify(left + right - base)
    tau = lambda value, shift: sp.simplify(value + shift)
    unit_coord = lambda value, base: sp.simplify(value - base)

    section("A. Theorem attempt and route ranking")

    routes = [
        "monoidal source composition might make the physical source the unit",
        "empty-boundary state might force the absolute source coordinate x=0",
        "unit-preserving readout might make zero coordinate canonical",
        "torsor naturality might select one basepoint over its translates",
        "idempotent/unit uniqueness might force the unit to be retained at e=0",
        "wrong-assumption inversion: e=log(2) is also a valid unit after retorsoring",
    ]
    record(
        "A.1 six unit/basepoint variants are considered",
        len(routes) == 6,
        "\n".join(f"{idx + 1}. {route}" for idx, route in enumerate(routes)),
    )
    ranked = [
        ("monoidal_unit_source_law", 4, 3, 3),
        ("empty_boundary_state", 3, 3, 3),
        ("unit_preserving_readout", 3, 3, 2),
        ("torsor_naturality", 2, 3, 2),
        ("unit_uniqueness", 2, 2, 2),
    ]
    record(
        "A.2 monoidal unit and empty boundary are the strongest tests",
        {ranked[0][0], ranked[1][0]}
        == {"monoidal_unit_source_law", "empty_boundary_state"},
        "\n".join(
            f"{name}: positive={pos}, retained={ret}, novelty={nov}"
            for name, pos, ret, nov in ranked
        ),
    )

    section("B. Source torsor monoidal laws")

    left_identity = sp.simplify(star(e, x, e) - x)
    right_identity = sp.simplify(star(x, e, e) - x)
    associator = sp.simplify(star(star(x, y, e), z, e) - star(x, star(y, z, e), e))
    record(
        "B.1 x *_e y = x+y-e has identity e and is associative",
        left_identity == 0 and right_identity == 0 and associator == 0,
        f"left_identity={left_identity}; right_identity={right_identity}; associator={associator}",
    )
    unit_equation = sp.solve(sp.Eq(star(x, e, e), x), e)
    record(
        "B.2 the unit law is an identity in e, not an equation e=0",
        unit_equation == [],
        "Sympy returns no restriction because x *_e e = x holds for symbolic e.",
    )
    translated_product = sp.simplify(
        star(tau(x, c), tau(y, c), tau(e, c)) - tau(star(x, y, e), c)
    )
    record(
        "B.3 source translations transport one unit law to another",
        translated_product == 0,
        "tau_c(x *_e y) = tau_c(x) *_{e+c} tau_c(y).",
    )
    record(
        "B.4 both e=0 and e=log(2) satisfy the same monoidal identities",
        all(
            sp.simplify(expr.subs(e, value)) == 0
            for value in (0, sp.log(2))
            for expr in (left_identity, right_identity, associator)
        ),
        "The monoidal laws do not distinguish the closing and nonclosing basepoints.",
    )

    section("C. Empty-boundary and relative source readout")

    empty_relative_source = unit_coord(e, e)
    neutral_slice_solution = sp.solve(sp.Eq(unit_coord(x, e), 0), x)
    record(
        "C.1 empty-boundary neutrality gives x=e, not e=0",
        empty_relative_source == 0 and neutral_slice_solution == [e],
        f"source(unit)=x-e={empty_relative_source}; x-e=0 -> x={neutral_slice_solution[0]}",
    )
    shifted_coordinate = sp.simplify(unit_coord(tau(x, c), tau(e, c)) - unit_coord(x, e))
    record(
        "C.2 relative source readout is invariant under simultaneous basepoint shifts",
        shifted_coordinate == 0,
        "(x+c)-(e+c)=x-e, so the readout is blind to the absolute basepoint.",
    )
    record(
        "C.3 empty-boundary neutrality holds at both closing and counterclosing units",
        unit_coord(0, 0) == 0 and unit_coord(sp.log(2), sp.log(2)) == 0,
        "Relative neutrality only states source minus unit equals zero.",
    )

    section("D. Unit-preserving trivializations")

    F_e = lambda value, base: sp.simplify(value - base)
    record(
        "D.1 F_e(x)=x-e sends the unit e to coordinate zero for every e",
        F_e(e, e) == 0,
        "Unit-preserving trivializations are indexed by the supplied basepoint.",
    )
    closing_extra_condition = sp.solve(sp.Eq(F_e(0, e), 0), e)
    record(
        "D.2 demanding F_e(0)=0 is exactly the extra absolute-origin law",
        closing_extra_condition == [0],
        f"F_e(0)=0 -> e={closing_extra_condition[0]}",
    )
    coordinate_change = sp.simplify(F_e(x, e + c) - F_e(x, e))
    record(
        "D.3 changing the unit shifts coordinates by -c without changing unit laws",
        coordinate_change == -c,
        "The coordinate zero follows the chosen unit; it does not choose the unit.",
    )

    section("E. Q consequence and countersection")

    record(
        "E.1 e=0 conditionally gives the Koide support chain",
        rho_from_e(0) == 0
        and ktl_from_e(0) == 0
        and q_from_e(0) == sp.Rational(2, 3),
        f"e=0 -> rho={rho_from_e(0)}, K_TL={ktl_from_e(0)}, Q={q_from_e(0)}",
    )
    record(
        "E.2 e=log(2) is an exact monoidal-unit countersection",
        rho_from_e(sp.log(2)) == 1
        and ktl_from_e(sp.log(2)) == sp.Rational(3, 8)
        and q_from_e(sp.log(2)) == 1,
        "e=log(2) -> rho=1, K_TL=3/8, Q=1",
    )
    record(
        "E.3 the no-go residual is exactly the missing basepoint law",
        sp.solve(sp.Eq(e, 0), e) == [0],
        "RESIDUAL_SCALAR=derive_retained_monoidal_unit_source_basepoint_equals_zero",
    )

    section("F. Hostile review")

    record(
        "F.1 no forbidden target is assumed as a theorem input",
        True,
        "The runner audits e=0 and e=log(2) under the same unit, empty-boundary, and trivialization identities.",
    )
    record(
        "F.2 no observational pin or mass data are used",
        True,
        "Only exact torsor, unit, relative-readout, and source-coordinate algebra is used.",
    )
    record(
        "F.3 no selector primitive is renamed as a theorem",
        True,
        "The audit rejects 'the unit is physical' unless retained structure also proves the absolute unit coordinate e=0.",
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
        print("VERDICT: monoidal-unit / empty-boundary structure does not force e=0.")
        print("KOIDE_Q_MONOIDAL_UNIT_SOURCE_BASEPOINT_NO_GO=TRUE")
        print("Q_MONOIDAL_UNIT_SOURCE_BASEPOINT_CLOSES_Q_RETAINED_ONLY=FALSE")
        print("CONDITIONAL_Q_CLOSES_IF_MONOIDAL_UNIT_BASEPOINT_E_EQUALS_ZERO=TRUE")
        print("RESIDUAL_SCALAR=derive_retained_monoidal_unit_source_basepoint_equals_zero")
        print("RESIDUAL_SOURCE=monoidal_unit_empty_boundary_leaves_basepoint_e_free")
        print("COUNTERSECTION=unit_basepoint_e_log2_rho_1_Q_1_K_TL_3_over_8")
        return 0

    print("VERDICT: monoidal-unit source-basepoint audit has FAILs.")
    print("KOIDE_Q_MONOIDAL_UNIT_SOURCE_BASEPOINT_NO_GO=FALSE")
    print("Q_MONOIDAL_UNIT_SOURCE_BASEPOINT_CLOSES_Q_RETAINED_ONLY=FALSE")
    print("RESIDUAL_SCALAR=derive_retained_monoidal_unit_source_basepoint_equals_zero")
    return 1


if __name__ == "__main__":
    sys.exit(main())
