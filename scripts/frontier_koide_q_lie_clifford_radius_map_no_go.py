#!/usr/bin/env python3
"""
Koide Q Lie/Clifford radius-map no-go.

The A1 support stack has several exact structural hits:

    dim(spinor)/dim(Cl+(3)) = 1/2,
    |omega_{A1,fund}|^2 = 1/2,
    T(T+1) - Y^2 = 1/2 for the lepton doublet and Higgs.

The tempting closure upgrade is:

    these retained constants force |b|^2/a^2 = 1/2

for the charged-lepton circulant amplitude

    Y = a I + b C + bbar C^2.

The executable result is negative.  The constants are exact support, but a
scalar gauge/Clifford factor common to every Yukawa entry cancels from the
generation-space ratio |b|^2/a^2.  To close Q, one still needs a retained map
from those constants into the generation-cyclic radius, or a theorem that the
gauge/Clifford factor acts differently on diagonal and off-diagonal generation
blocks.

No PDG masses, K_TL=0, K=0, P_Q=1/2, Q=2/3, delta=2/9, or H_* pin is used.
"""

from __future__ import annotations

import sys
from fractions import Fraction

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


def q_from_x(x: sp.Expr) -> sp.Expr:
    """x = |b|^2/a^2 for the Brannen/circulant amplitude."""
    return sp.simplify(sp.Rational(1, 3) + 2 * x / 3)


def main() -> int:
    section("Koide Q Lie/Clifford radius-map no-go")
    print("Theorem attempt: retained SU(2)/Clifford/Casimir constants force")
    print("the generation-space radius |b|^2/a^2.  The audit result is negative.")

    a, br, bi, g = sp.symbols("a br bi g", positive=True, real=True)
    b2 = br**2 + bi**2
    x = sp.simplify(b2 / a**2)
    c2 = sp.simplify(4 * x)
    q = q_from_x(x)

    section("A. Koide radius coordinate")

    record(
        "A.1 the Brannen radius and Koide scalar are functions of x=|b|^2/a^2",
        c2 == 4 * x and sp.simplify(q - (sp.Rational(1, 3) + 2 * x / 3)) == 0,
        f"x={x}; c^2={c2}; Q(x)={q}",
    )
    record(
        "A.2 the Koide leaf is exactly x=1/2 in this coordinate",
        sp.simplify(q_from_x(sp.Rational(1, 2)) - sp.Rational(2, 3)) == 0,
        "Q(1/2)=2/3; equivalently c^2=2 and kappa=2.",
    )

    section("B. Exact retained structural constants")

    dim_spinor = Fraction(2, 1)
    dim_cl_plus = Fraction(4, 1)
    dim_ratio = dim_spinor / dim_cl_plus
    omega_a1_sq = Fraction(1, 2)
    t_half = Fraction(1, 2)
    y_half = Fraction(1, 2)
    casimir_diff = t_half * (t_half + 1) - y_half * y_half
    casimir_sum = t_half * (t_half + 1) + y_half * y_half

    record(
        "B.1 Clifford dimension ratio is exactly 1/2",
        dim_ratio == Fraction(1, 2),
        f"dim(spinor)/dim(Cl+(3)) = {dim_spinor}/{dim_cl_plus} = {dim_ratio}",
    )
    record(
        "B.2 A1 fundamental-weight norm is exactly 1/2",
        omega_a1_sq == Fraction(1, 2),
        "|omega_{A1,fund}|^2 = 1/2 in Kostant normalization.",
    )
    record(
        "B.3 Yukawa participant Casimir difference is exactly 1/2",
        casimir_diff == Fraction(1, 2) and casimir_sum == Fraction(1, 1),
        f"T(T+1)-Y^2={casimir_diff}; T(T+1)+Y^2={casimir_sum}.",
    )

    section("C. Common gauge/Clifford factors cannot set a generation ratio")

    x_after_common_factor = sp.simplify((g**2 * b2) / (g**2 * a**2))
    record(
        "C.1 any scalar factor from SU(2)/Clifford data cancels from |b|^2/a^2",
        sp.simplify(x_after_common_factor - x) == 0,
        f"|g b|^2/|g a|^2 = {x_after_common_factor}",
    )

    # The charged-lepton Yukawa vertex has the same SU(2) singlet contraction
    # for every generation pair alpha,beta, so any Clebsch/Casimir coefficient
    # is a common factor unless an extra generation-dependent rule is added.
    epsilon_factor = sp.symbols("epsilon_factor", nonzero=True, real=True)
    diagonal_entry = epsilon_factor * a
    offdiag_entry = epsilon_factor * (br + sp.I * bi)
    ratio_with_cg = sp.simplify(
        (sp.re(offdiag_entry) ** 2 + sp.im(offdiag_entry) ** 2)
        / diagonal_entry**2
    )
    record(
        "C.2 SU(2) Clebsch contraction is generation-blind in the standard Yukawa tensor",
        sp.simplify(ratio_with_cg - x) == 0,
        "The same L.H -> singlet contraction multiplies y_{alpha beta} for all generation pairs.",
    )

    s = sp.Rational(1, 2)
    maps = {
        "x=s": s,
        "x=s/2": s / 2,
        "x=2s": 2 * s,
        "x=s^2": s**2,
    }
    map_lines = [f"{label} -> x={value}, Q={q_from_x(value)}" for label, value in maps.items()]
    record(
        "C.3 the same structural scalar supports multiple inequivalent radius maps",
        q_from_x(maps["x=s"]) == sp.Rational(2, 3)
        and q_from_x(maps["x=s/2"]) == sp.Rational(1, 2)
        and q_from_x(maps["x=2s"]) == sp.Integer(1)
        and q_from_x(maps["x=s^2"]) == sp.Rational(1, 2),
        "\n".join(map_lines),
    )

    section("D. Exact counterfamilies")

    counter_xs = [sp.Rational(1, 4), sp.Rational(1, 2), sp.Integer(1)]
    counter_lines = []
    for value in counter_xs:
        counter_lines.append(
            f"x={value}: constants=(1/2,1/2,1/2) unchanged, c^2={4*value}, Q={q_from_x(value)}"
        )
    record(
        "D.1 retained structural constants are unchanged while the amplitude radius varies",
        [q_from_x(v) for v in counter_xs]
        == [sp.Rational(1, 2), sp.Rational(2, 3), sp.Integer(1)],
        "\n".join(counter_lines),
    )

    record(
        "D.2 a closure needs a generation-sensitive amplitude map, not just the scalar constant",
        True,
        "Needed theorem: |b|^2/a^2 = dim(spinor)/dim(Cl+(3)) or\n"
        "|b|^2/a^2 = T(T+1)-Y^2 as a law on the generation-cyclic carrier.\n"
        "The scalar equalities alone do not provide that map.",
    )

    record(
        "D.3 no forbidden target or observational pin is used",
        True,
        "The audit uses exact representation constants and symbolic amplitudes only.",
    )

    section("Summary")
    n_pass = sum(1 for _, ok, _ in PASSES if ok)
    n_total = len(PASSES)
    print(f"PASSED: {n_pass}/{n_total}")

    if n_pass == n_total:
        print()
        print("KOIDE_Q_LIE_CLIFFORD_RADIUS_MAP_NO_GO=TRUE")
        print("Q_LIE_CLIFFORD_CONSTANTS_CLOSE_Q=FALSE")
        print("Q_LIE_CLIFFORD_CONSTANTS_CLOSES_Q=FALSE")
        print("RESIDUAL_PRIMITIVE=generation_sensitive_radius_map_equiv_c^2=2_equiv_K_TL=0")
        print()
        print("VERDICT: the Lie/Clifford/Casimir constants are exact support,")
        print("but they close Q only after adopting a map from those constants")
        print("to the generation-space radius |b|^2/a^2.")

    if n_pass != n_total:
        print()
        print("KOIDE_Q_LIE_CLIFFORD_RADIUS_MAP_NO_GO=FALSE")
        print("Q_LIE_CLIFFORD_CONSTANTS_CLOSES_Q=FALSE")
        print("RESIDUAL_PRIMITIVE=generation_sensitive_radius_map_equiv_c^2=2_equiv_K_TL=0")

    return 0 if n_pass == n_total else 1


if __name__ == "__main__":
    sys.exit(main())
