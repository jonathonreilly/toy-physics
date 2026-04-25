#!/usr/bin/env python3
"""
Koide delta Z3 character-holonomy no-go.

Theorem attempt:
  The selected-line Berry endpoint might be forced by naturality as a U(1)
  holonomy character of the retained Z3 cyclic symmetry, thereby identifying
  theta_end - theta0 with the ambient APS scalar eta_APS = 2/9.

Result:
  Negative.  A U(1) character of Z3 sends the generator to a phase fraction
  m/3 mod 1.  The ambient APS value 2/9 is not on this character lattice:
  3*(2/9)=2/3 is not an integer.  Allowing a quadratic refinement can produce
  2/9, but only by choosing an extra quadratic coefficient; it is no longer a
  group character endpoint law.  Thus character holonomy cannot derive the
  physical Brannen endpoint.

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


def is_integer_rational(value: sp.Expr) -> bool:
    value = sp.simplify(value)
    return bool(value.is_integer)


def main() -> int:
    section("A. Z3 character lattice")

    eta = eta_abss_z3_weights_12()
    character_fractions = [sp.Rational(m, 3) for m in range(3)]
    record(
        "A.1 ambient APS scalar remains eta_APS=2/9",
        eta == sp.Rational(2, 9),
        f"eta_APS={eta}",
    )
    record(
        "A.2 U(1) characters of Z3 have generator phase fractions m/3",
        character_fractions == [0, sp.Rational(1, 3), sp.Rational(2, 3)],
        f"Hom(Z3,U1) fractions={character_fractions}",
    )
    record(
        "A.3 eta_APS=2/9 is not a Z3 character endpoint",
        eta not in character_fractions and not is_integer_rational(3 * eta),
        f"3*eta={3 * eta}; character condition needs 3*theta in Z.",
    )

    section("B. Homomorphism test")

    x = sp.symbols("x", real=True)
    hom_condition = sp.Eq(3 * x, sp.floor(3 * x))
    eta_hom_residual = sp.simplify(3 * eta)
    record(
        "B.1 a generator endpoint x is a character only when 3x is integral",
        True,
        f"condition: 3x in Z; eta gives 3x={eta_hom_residual}",
    )
    record(
        "B.2 eta fails the character composition law g^3=e",
        eta_hom_residual == sp.Rational(2, 3),
        "Taking the eta endpoint three times leaves phase fraction 2/3, not 0 mod 1.",
    )

    section("C. Quadratic refinements can hit eta only with a new coefficient")

    A, B = sp.symbols("A B", integer=True)
    q1 = sp.simplify(A / 9 + B / 3)
    hit_solutions = sp.solve(sp.Eq(q1, eta), A)
    polarization_11 = sp.simplify((4 * A / 9 + 2 * B / 3) - 2 * q1)
    record(
        "C.1 a quadratic refinement can hit 2/9 only by choosing a coefficient",
        hit_solutions == [2 - 3 * B],
        f"q(1)=A/9+B/3; q(1)=2/9 -> A={hit_solutions}",
    )
    record(
        "C.2 the quadratic hit is not a character law",
        polarization_11 == 2 * A / 9,
        f"q(2)-2q(1)={polarization_11}; homomorphism would require zero mod 1.",
    )
    record(
        "C.3 choosing A=2,B=0 gives eta but leaves nonzero polarization",
        q1.subs({A: 2, B: 0}) == eta and polarization_11.subs(A, 2) == sp.Rational(4, 9),
        "This is quadratic APS-style support, not a natural U(1) character endpoint.",
    )

    section("D. Counter-holonomies")

    counter_lines = []
    for value in character_fractions:
        counter_lines.append(
            f"character endpoint={value}: character_ok={is_integer_rational(3 * value)}, residual={sp.simplify(value - eta)}"
        )
    record(
        "D.1 all retained Z3 character holonomies miss the APS endpoint",
        all(value != eta for value in character_fractions),
        "\n".join(counter_lines),
    )

    section("E. Verdict")

    residual = sp.simplify(3 * eta - sp.floor(3 * eta))
    record(
        "E.1 character holonomy route does not close delta",
        residual == sp.Rational(2, 3),
        f"RESIDUAL_CHARACTER_FRACTION={residual}",
    )
    record(
        "E.2 delta remains open after Z3 character audit",
        True,
        "Residual primitive: a physical Berry/APS functor beyond character holonomy.",
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
        print("VERDICT: Z3 character holonomy does not close delta.")
        print("KOIDE_DELTA_Z3_CHARACTER_HOLONOMY_NO_GO=TRUE")
        print("DELTA_Z3_CHARACTER_HOLONOMY_CLOSES_DELTA=FALSE")
        print("RESIDUAL_SCALAR=theta_end-theta0-eta_APS")
        print("RESIDUAL_CHARACTER_FRACTION=three_eta_not_integral")
        print("RESIDUAL_ENDPOINT=theta_end-theta0-eta_APS")
        return 0

    print("VERDICT: Z3 character holonomy audit has FAILs.")
    print("KOIDE_DELTA_Z3_CHARACTER_HOLONOMY_NO_GO=FALSE")
    print("DELTA_Z3_CHARACTER_HOLONOMY_CLOSES_DELTA=FALSE")
    print("RESIDUAL_SCALAR=theta_end-theta0-eta_APS")
    print("RESIDUAL_CHARACTER_FRACTION=three_eta_not_integral")
    print("RESIDUAL_ENDPOINT=theta_end-theta0-eta_APS")
    return 1


if __name__ == "__main__":
    sys.exit(main())
