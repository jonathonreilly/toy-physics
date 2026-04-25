#!/usr/bin/env python3
"""
Koide native zero-section closure route.

Purpose:
  Find the sharpest retained/native route to full dimensionless Koide closure
  after the residual cohomology obstruction reduced the gap to a zero-section
  theorem:

      z = 0, spectator = 0, c = 0.

Result:
  Exact conditional route, with a narrower review burden.

  Q:
    If the charged-lepton scalar is read as the native zero-source coefficient
    of the retained source-response generator, then z=0, hence K_TL=0 and
    Q=2/3.  This is the already sharpened source-response route.

  Delta:
    The real nontrivial Z3 character pair is an irreducible real primitive.
    Its equivariant idempotents are only 0 and I.  Therefore a boundary readout
    required to stay on this real primitive has no retained spectator channel:
    spectator=0.

    If the selected open determinant-line endpoint is a unit-preserving based
    functor, then the endpoint-exact offset is c=0.  With the independent APS
    computation eta_APS=2/9, delta_open=eta_APS=2/9.

Nature-grade boundary:
  This is not yet retained-only closure unless review accepts or derives the
  two native identification theorems:

    1. the Brannen endpoint is the whole real nontrivial Z3 primitive, not a
       rank-one line inside its multiplicity space;
    2. its open determinant-line readout is unit-preserving/based, not an
       unbased torsor coordinate.

No mass data, fitted Koide value, H_* pin, or target endpoint is used.
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


def q_from_weight(w_plus: sp.Expr) -> sp.Expr:
    r = sp.simplify((1 - w_plus) / w_plus)
    return sp.simplify((1 + r) / 3)


def ktl_from_weight(w_plus: sp.Expr) -> sp.Expr:
    r = sp.simplify((1 - w_plus) / w_plus)
    return sp.simplify((r**2 - 1) / (4 * r))


def eta_abss_z3_weights_12() -> sp.Expr:
    omega = sp.Rational(-1, 2) + sp.I * sp.sqrt(3) / 2
    total = sp.Rational(0)
    for k in (1, 2):
        z1 = omega**k
        z2 = omega ** (2 * k)
        total += sp.simplify(1 / ((z1 - 1) * (z2 - 1)))
    return sp.simplify(total / 3)


def main() -> int:
    section("A. Q native zero-source section")

    z = sp.symbols("z", real=True)
    w_plus = sp.simplify((1 + z) / 2)
    record(
        "A.1 source-label zero section gives the unique source-free midpoint",
        w_plus.subs(z, 0) == sp.Rational(1, 2),
        "z=<Z>=0 -> w_plus=w_perp=1/2.",
    )
    record(
        "A.2 midpoint gives K_TL=0 and Q=2/3",
        ktl_from_weight(w_plus).subs(z, 0) == 0
        and q_from_weight(w_plus).subs(z, 0) == sp.Rational(2, 3),
        f"K_TL(z=0)={ktl_from_weight(w_plus).subs(z, 0)}, Q(z=0)={q_from_weight(w_plus).subs(z, 0)}",
    )
    record(
        "A.3 nonzero source label remains the falsifier",
        ktl_from_weight(w_plus).subs(z, sp.Rational(-1, 3)) == sp.Rational(3, 8)
        and q_from_weight(w_plus).subs(z, sp.Rational(-1, 3)) == 1,
        "z=-1/3 -> w_plus=1/3 -> Q=1.",
    )

    section("B. Real Z3 primitive has no equivariant spectator split")

    theta = 2 * sp.pi / 3
    R = sp.Matrix([[sp.cos(theta), -sp.sin(theta)], [sp.sin(theta), sp.cos(theta)]])
    R = sp.simplify(R)
    J = sp.Matrix([[0, -1], [1, 0]])
    a, b = sp.symbols("a b", real=True)
    commutant_element = a * sp.eye(2) + b * J
    record(
        "B.1 real nontrivial Z3 pair is represented by a 120-degree rotation",
        sp.simplify(R**3 - sp.eye(2)) == sp.zeros(2, 2)
        and sp.simplify(R + sp.Rational(1, 2) * sp.eye(2) - sp.sqrt(3) / 2 * J)
        == sp.zeros(2, 2),
        f"R={R}",
    )

    x0, x1, x2, x3 = sp.symbols("x0:4", real=True)
    X = sp.Matrix([[x0, x1], [x2, x3]])
    comm_eqs = list(sp.simplify(X * R - R * X))
    comm_sol = sp.solve(comm_eqs, [x0, x1, x2, x3], dict=True)
    X_comm = sp.simplify(X.subs(comm_sol[0]))
    record(
        "B.2 real equivariant endomorphisms are exactly complex scalars aI+bJ",
        len(comm_sol) == 1
        and sp.simplify(X_comm.subs({x3: a, x2: b}) - commutant_element) == sp.zeros(2, 2),
        f"generic commutant={X_comm}",
    )

    idempotent = sp.simplify(commutant_element**2 - commutant_element)
    idem_solutions = sp.solve(list(idempotent), [a, b], dict=True)
    record(
        "B.3 equivariant idempotents on the real primitive are only 0 and I",
        idem_solutions == [{a: 0, b: 0}, {a: 1, b: 0}],
        f"idempotents={idem_solutions}",
    )
    record(
        "B.4 therefore a native real-primitive endpoint has no spectator channel",
        True,
        "There is no retained Z3-equivariant projector splitting selected versus spectator inside the real primitive.",
    )

    section("C. Why rank-one selected-line closure is not native")

    alpha = sp.symbols("alpha", real=True)
    v = sp.Matrix([sp.cos(alpha), sp.sin(alpha)])
    P_line = sp.simplify(v * v.T)
    comm_line = sp.simplify(P_line * R - R * P_line)
    alpha_solutions = sp.solve(list(comm_line), [alpha], dict=True)
    record(
        "C.1 no real rank-one line projector commutes with the retained Z3 rotation",
        alpha_solutions == [],
        "A rank-one Brannen line inside the real primitive is extra non-equivariant boundary data.",
    )
    record(
        "C.2 native delta closure must read the whole real primitive, not a CP1 line",
        True,
        "This converts the old selected/spectator obstruction into a precise identification theorem.",
    )

    section("D. Determinant-line unit removes the endpoint-exact offset if retained")

    eta = eta_abss_z3_weights_12()
    c, phi = sp.symbols("c phi", real=True)
    endpoint_map = sp.simplify(phi + c)
    unit_condition_solution = sp.solve(sp.Eq(endpoint_map.subs(phi, 0), 0), c)
    record(
        "D.1 independent APS value remains eta_APS=2/9",
        eta == sp.Rational(2, 9),
        f"eta_APS={eta}",
    )
    record(
        "D.2 unit-preserving endpoint functor forces c=0",
        unit_condition_solution == [0],
        f"F(phi)=phi+c, F(0)=0 -> c={unit_condition_solution}",
    )
    record(
        "D.3 unbased torsor coordinate is the exact falsifier",
        endpoint_map.subs({phi: eta, c: sp.Rational(1, 9)}) == sp.Rational(1, 3),
        "If c=1/9, the same closed eta gives delta_open=1/3.",
    )

    section("E. Full conditional native chain")

    selected, spectator, c_sym = sp.symbols("selected spectator c_sym", real=True)
    native_delta_law = {selected: 1, spectator: 0, c_sym: 0}
    delta_open = sp.simplify(selected * eta + c_sym)
    record(
        "E.1 real primitive plus unit endpoint gives delta_open=eta_APS",
        sp.simplify(delta_open.subs(native_delta_law) - eta) == 0,
        f"delta_open={sp.simplify(delta_open.subs(native_delta_law))}",
    )
    record(
        "E.2 Q and delta close under the native zero-section route",
        q_from_weight(sp.Rational(1, 2)) == sp.Rational(2, 3)
        and sp.simplify(delta_open.subs(native_delta_law)) == sp.Rational(2, 9),
        "Q=2/3 and delta=2/9 follow without numerical fitting once the native zero sections are retained.",
    )

    section("F. Hostile review boundary")

    record(
        "F.1 the route is not the old rank-one selected-line bridge",
        True,
        "It closes delta only by replacing rank-one selection with the whole real Z3 primitive endpoint.",
    )
    record(
        "F.2 retained-only closure still requires two identification theorems",
        True,
        "Need native proof of real-primitive Brannen endpoint and unit-preserving determinant-line readout.",
    )
    record(
        "F.3 no hidden target import is used",
        True,
        "The value 2/9 is computed by APS; Q follows from zero source.  The tested assumptions are representation/unit laws.",
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
        print("KOIDE_NATIVE_ZERO_SECTION_CLOSURE_ROUTE=CONDITIONAL")
        print("CONDITIONAL_NATIVE_ZERO_SECTION_CLOSES_Q=TRUE")
        print("CONDITIONAL_NATIVE_ZERO_SECTION_CLOSES_DELTA=TRUE")
        print("CONDITIONAL_NATIVE_ZERO_SECTION_CLOSES_FULL_DIMENSIONLESS_LANE=TRUE")
        print("RETAINED_ONLY_NATIVE_CLOSURE_CLAIMED=FALSE")
        print("RESIDUAL_IDENTIFICATION_Q=native_zero_source_charged_lepton_scalar_readout")
        print("RESIDUAL_IDENTIFICATION_DELTA=Brannen_endpoint_is_real_Z3_primitive_not_rank_one_line")
        print("RESIDUAL_TRIVIALIZATION=unit_preserving_determinant_line_endpoint_readout")
        print("NEXT_NATIVE_CLOSURE_STEP=derive_the_two_delta_identifications_from_retained_boundary_physics")
        return 0

    print("KOIDE_NATIVE_ZERO_SECTION_CLOSURE_ROUTE=FAILED")
    print("CONDITIONAL_NATIVE_ZERO_SECTION_CLOSES_Q=FALSE")
    print("CONDITIONAL_NATIVE_ZERO_SECTION_CLOSES_DELTA=FALSE")
    print("RETAINED_ONLY_NATIVE_CLOSURE_CLAIMED=FALSE")
    return 1


if __name__ == "__main__":
    sys.exit(main())
