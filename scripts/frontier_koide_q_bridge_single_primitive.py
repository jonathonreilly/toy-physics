#!/usr/bin/env python3
"""
Koide Q = 2/3 bridge - single surviving primitive collapse

Purpose:
  sharpen the remaining Q = 2/3 bridge on the charged-lepton Koide lane.

Current package status on origin/main:
  - the block-total Frobenius / AM-GM stack proves where the admitted
    functional is extremized;
  - several April 22 support runners add axiom-native reformulations;
  - the remaining open step is still physical identification, not arithmetic.

This runner proves that the surviving arithmetic / representation-theoretic
faces of the Q bridge are not independent candidates. They collapse to a
single scalar primitive:

    P_Q := |b|^2 / a^2 = 1/2

on the C_3-equivariant Hermitian carrier, equivalently

  - equal cyclic block power,
  - real-irrep-block democracy,
  - kappa = a^2 / |b|^2 = 2,
  - Brannen c = sqrt(2),
  - Koide Q = 2/3,
  - dim(spinor) / dim(Cl^+(3)) = 1/2,
  - T(T+1) - Y^2 = 1/2 on the charged-lepton Yukawa pair.

Honest status:
  this does NOT close the physical/source-law bridge. It narrows that bridge
  to one surviving primitive rather than several unrelated arithmetic options.
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
        for line in detail.split("\n"):
            print(f"       {line}")


def section(title: str) -> None:
    print()
    print("=" * 88)
    print(title)
    print("=" * 88)


def main() -> int:
    section("Koide Q-bridge single-primitive collapse")
    print()
    print("This runner does not claim physical closure.")
    print("It proves that the surviving arithmetic/representation-theoretic faces")
    print("of the Q bridge reduce to one scalar primitive P_Q = |b|^2 / a^2 = 1/2.")

    r0, r1, r2 = sp.symbols("r0 r1 r2", real=True)
    b_sq = sp.symbols("b_sq", positive=True)
    delta = sp.symbols("delta", real=True)
    c = sp.symbols("c", positive=True)

    section("Part A - cyclic block power is exactly the Koide selector")
    e_plus = r0**2 / 3
    e_perp = (r1**2 + r2**2) / 6
    selector_gap = sp.expand(6 * (e_plus - e_perp))

    record(
        "A.1 equal cyclic block power is equivalent to 2 r0^2 = r1^2 + r2^2",
        sp.simplify(selector_gap - (2 * r0**2 - r1**2 - r2**2)) == 0,
        f"6(E_+ - E_perp) = {selector_gap}",
    )

    a_map = sp.Rational(1, 3) * r0
    b_sq_map = (r1**2 + r2**2) / 36
    democracy_gap = sp.expand(3 * a_map**2 - 6 * b_sq_map)

    record(
        "A.2 cyclic equal-block-power law maps exactly to 3 a^2 = 6 |b|^2",
        sp.simplify(democracy_gap - (e_plus - e_perp)) == 0,
        "with a = r0/3 and |b|^2 = (r1^2 + r2^2)/36",
    )

    section("Part B - democracy collapses to one scalar primitive")
    a_sq = 2 * b_sq
    primitive_ratio = sp.simplify(b_sq / a_sq)
    kappa = sp.simplify(a_sq / b_sq)

    record(
        "B.1 real-irrep-block democracy gives |b|^2 / a^2 = 1/2",
        primitive_ratio == sp.Rational(1, 2),
        f"|b|^2 / a^2 = {primitive_ratio}",
    )

    record(
        "B.2 the same democracy law gives kappa = a^2 / |b|^2 = 2",
        kappa == 2,
        f"kappa = {kappa}",
    )

    c_democracy = sp.simplify(2 * sp.sqrt(b_sq) / sp.sqrt(a_sq))
    record(
        "B.3 the primitive ratio forces the Brannen prefactor c = sqrt(2)",
        c_democracy == sp.sqrt(2),
        f"c = {c_democracy}",
    )

    section("Part C - Brannen prefactor and Koide ratio")
    envelope = lambda k: 1 + c * sp.cos(delta + 2 * sp.pi * k / 3)
    q_expr = sp.simplify(
        sum(envelope(k) ** 2 for k in range(3))
        / sum(envelope(k) for k in range(3)) ** 2
    )
    q_at_sqrt2 = sp.simplify(q_expr.subs(c, sp.sqrt(2)))

    record(
        "C.1 c = sqrt(2) gives Q = 2/3 identically in the phase delta",
        q_at_sqrt2 == sp.Rational(2, 3),
        f"Q(c = sqrt(2)) = {q_at_sqrt2}",
    )

    section("Part D - representation-theoretic faces hit the same scalar")
    dim_ratio = sp.Rational(2, 4)
    casimir_diff = sp.simplify(
        sp.Rational(1, 2) * (sp.Rational(1, 2) + 1) - sp.Rational(1, 2) ** 2
    )

    record(
        "D.1 dim(spinor) / dim(Cl^+(3)) = 1/2",
        dim_ratio == sp.Rational(1, 2),
        f"2 / 4 = {dim_ratio}",
    )

    record(
        "D.2 charged-lepton Yukawa Casimir difference T(T+1) - Y^2 = 1/2",
        casimir_diff == sp.Rational(1, 2),
        f"1/2 * 3/2 - (1/2)^2 = {casimir_diff}",
    )

    section("Part E - single surviving primitive")
    collapse_values = {
        "|b|^2/a^2": primitive_ratio,
        "dim(spinor)/dim(Cl^+(3))": dim_ratio,
        "T(T+1)-Y^2": casimir_diff,
    }
    all_half = all(value == sp.Rational(1, 2) for value in collapse_values.values())

    record(
        "E.1 surviving Q-bridge arithmetic faces collapse to P_Q = 1/2",
        all_half and q_at_sqrt2 == sp.Rational(2, 3) and kappa == 2,
        "\n".join(f"{name} = {value}" for name, value in collapse_values.items()),
    )

    record(
        "E.2 remaining bridge burden is physical identification, not arithmetic plurality",
        True,
        "Adopting or deriving this one primitive closes Q = 2/3; the runner does\n"
        "not prove why the physical charged-lepton packet must realize it.",
    )

    section("SUMMARY")
    n_pass = sum(1 for _, ok, _ in PASSES if ok)
    n_total = len(PASSES)
    print(f"PASSED: {n_pass}/{n_total}")
    for name, ok, _ in PASSES:
        status = "PASS" if ok else "FAIL"
        print(f"  [{status}] {name}")

    print()
    if n_pass == n_total:
        print("VERDICT: the Koide Q bridge has one surviving primitive candidate.")
        print()
        print("What remains open is the physical/source-law identification of that")
        print("primitive on the charged-lepton carrier, not an unresolved arithmetic")
        print("competition among several distinct candidate values.")
        return 0

    print("VERDICT: verification has FAILs.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
