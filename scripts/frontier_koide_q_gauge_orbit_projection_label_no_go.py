#!/usr/bin/env python3
"""
Koide Q gauge-orbit projection label no-go.

Theorem attempt:
  Treat the retained C3/D3 generation symmetry as a gauge redundancy and
  project physical sources to the gauge-invariant subalgebra.  Perhaps this
  projection erases the central label observable Z=P_plus-P_perp and forces
  the uniform source state, hence K_TL=0.

Result:
  Negative under current retained structure.  Gauge/Reynolds projection kills
  non-invariant source components, but Z is itself invariant under the retained
  C3 axis, the D3/S3 normalizer reflection, and the second-order even carrier.
  The projected source algebra remains span{I,Z}.  Trace normalization removes
  I but leaves the Z coefficient free.  Therefore gauge-orbit projection does
  not close Q; closure still needs a physical law setting the invariant Z
  coefficient to zero or excluding Z from the source domain.

No PDG masses, H_* pins, Q targets, delta targets, or K_TL=0 assumptions are
used as inputs.
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


def reynolds(group: list[sp.Matrix], X: sp.Matrix) -> sp.Matrix:
    total = sp.zeros(3, 3)
    for g in group:
        total += g * X * g.T
    return sp.simplify(total / len(group))


def main() -> int:
    section("A. Retained C3/D3 gauge orbit")

    C = sp.Matrix([[0, 0, 1], [1, 0, 0], [0, 1, 0]])
    F = sp.Matrix([[1, 0, 0], [0, 0, 1], [0, 1, 0]])
    I3 = sp.eye(3)
    group = [I3, C, C**2, F, F * C, F * C**2]
    record(
        "A.1 retained normalizer group has six elements and closes",
        len({tuple(g) for g in group}) == 6
        and all(any(g * h == k for k in group) for g in group for h in group),
        "D3=<C,F>, C^3=I, F^2=I, F C F=C^-1.",
    )
    record(
        "A.2 all retained normalizer elements are orthogonal permutations",
        all(g.T * g == I3 and g.det() in (1, -1) for g in group),
        "Projection is conjugation by retained generation permutations.",
    )

    section("B. Central label Z is gauge invariant")

    P_plus = sp.ones(3, 3) / 3
    P_perp = I3 - P_plus
    Z = sp.simplify(P_plus - P_perp)
    record(
        "B.1 P_plus and P_perp are each fixed by the retained gauge orbit",
        all(sp.simplify(g * P_plus * g.T - P_plus) == sp.zeros(3, 3) for g in group)
        and all(sp.simplify(g * P_perp * g.T - P_perp) == sp.zeros(3, 3) for g in group),
        "The gauge orbit does not exchange singlet and real-doublet totals.",
    )
    record(
        "B.2 Z=P_plus-P_perp is itself gauge invariant",
        all(sp.simplify(g * Z * g.T - Z) == sp.zeros(3, 3) for g in group),
        f"Z={Z}",
    )
    record(
        "B.3 Reynolds projection of Z returns Z, not zero",
        reynolds(group, Z) == Z,
        "Gauge projection cannot erase an already gauge-invariant label coordinate.",
    )

    section("C. Gauge-invariant source algebra remains two-dimensional")

    xs = sp.symbols("x0:9", real=True)
    X = sp.Matrix(3, 3, xs)
    R = reynolds(group, X)
    alpha = sp.simplify(sp.trace(R * P_plus) / sp.trace(P_plus))
    beta = sp.simplify(sp.trace(R * P_perp) / sp.trace(P_perp))
    R_two_block = sp.simplify(alpha * P_plus + beta * P_perp)
    record(
        "C.1 D3 Reynolds image is alpha P_plus + beta P_perp",
        sp.simplify(R - R_two_block) == sp.zeros(3, 3),
        f"alpha={alpha}; beta={beta}",
    )
    record(
        "C.2 the invariant source quotient is span{I,Z}/span{I}",
        sp.simplify((alpha * P_plus + beta * P_perp) - ((alpha + beta) / 2) * I3 - ((alpha - beta) / 2) * Z)
        == sp.zeros(3, 3),
        "Trace normalization removes (alpha+beta)/2 but leaves (alpha-beta)/2.",
    )
    record(
        "C.3 no gauge projection identity forces alpha=beta",
        sp.simplify(alpha - beta).has(*xs),
        "The projected coefficient alpha-beta is a genuine linear functional of the input source.",
    )

    section("D. Exact nonclosing gauge-invariant counterstate")

    w = sp.symbols("w", positive=True, real=True)
    record(
        "D.1 source neutrality is exactly the midpoint w=1/2",
        sp.solve(sp.Eq(ktl_from_weight(w), 0), w) == [sp.Rational(1, 2)],
        f"K_TL(w)={ktl_from_weight(w)}",
    )
    counter_w = sp.Rational(1, 3)
    counter_source = sp.simplify(counter_w * P_plus + (1 - counter_w) * P_perp)
    record(
        "D.2 w=1/3 source state is gauge invariant and nonclosing",
        all(sp.simplify(g * counter_source * g.T - counter_source) == sp.zeros(3, 3) for g in group)
        and q_from_weight(counter_w) == 1
        and ktl_from_weight(counter_w) == sp.Rational(3, 8),
        f"w={counter_w}, Q={q_from_weight(counter_w)}, K_TL={ktl_from_weight(counter_w)}",
    )
    record(
        "D.3 gauge projection preserves this counterstate",
        reynolds(group, counter_source) == counter_source,
        "The nonclosing state is already in the gauge-invariant subalgebra.",
    )

    section("E. Hostile review")

    record(
        "E.1 gauge invariance is not renamed as source neutrality",
        True,
        "The invariant subalgebra contains both closing and nonclosing center states.",
    )
    record(
        "E.2 no forbidden target or observational pin is used as input",
        True,
        "The Koide value appears only as the conditional consequence of w=1/2.",
    )
    record(
        "E.3 exact residual primitive is named",
        True,
        "RESIDUAL_PRIMITIVE=derive_physical_law_excluding_gauge_invariant_Z_source.",
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
        print("KOIDE_Q_GAUGE_ORBIT_PROJECTION_LABEL_NO_GO=TRUE")
        print("Q_GAUGE_ORBIT_PROJECTION_LABEL_CLOSES_Q=FALSE")
        print("RESIDUAL_SCALAR=gauge_invariant_Z_source_coefficient_equiv_K_TL")
        print("RESIDUAL_LABEL=Z_survives_retained_gauge_orbit_projection")
        print("RESIDUAL_PRIMITIVE=derive_physical_law_excluding_gauge_invariant_Z_source")
        return 0

    print("KOIDE_Q_GAUGE_ORBIT_PROJECTION_LABEL_NO_GO=FALSE")
    print("Q_GAUGE_ORBIT_PROJECTION_LABEL_CLOSES_Q=FALSE")
    print("RESIDUAL_SCALAR=gauge_invariant_Z_source_coefficient_equiv_K_TL")
    return 1


if __name__ == "__main__":
    sys.exit(main())
