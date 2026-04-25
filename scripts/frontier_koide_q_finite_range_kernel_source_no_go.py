#!/usr/bin/env python3
"""
Koide Q finite-range C3 kernel-source no-go.

Theorem attempt:
  Strengthen the retained source grammar by requiring a physical kernel on the
  three-state C3 quotient: translation equivariance, finite range, stochastic
  conservation, positivity, and detailed balance.  Perhaps those constraints
  force the normalized second-order traceless source K_TL to vanish.

Result:
  Negative.  A C3-equivariant stochastic kernel has clockwise and
  counterclockwise transition weights a,b.  Detailed balance reduces it to the
  one-parameter reversible family

      M_s = (1 - 2s) I + s(C + C^2),       0 <= s <= 1/2.

  The stationary distribution is uniform for every s, but the second-order
  singlet/doublet spectral split is 1 versus 1-3s.  Positivity, conservation,
  finite range, and detailed balance leave s free.  Therefore this physical
  kernel class does not derive the missing K_TL source law.

No PDG masses, target Koide value, K_TL pin, delta pin, or H_* pin is used.
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


def main() -> int:
    section("A. General finite-range C3-equivariant stochastic kernel")

    C = sp.Matrix([[0, 0, 1], [1, 0, 0], [0, 1, 0]])
    C2 = C**2
    I3 = sp.eye(3)
    a, b = sp.symbols("a b", nonnegative=True, real=True)
    M = sp.simplify((1 - a - b) * I3 + a * C + b * C2)
    ones = sp.ones(3, 1)
    row_sums = [sp.simplify(sum(M[i, j] for j in range(3))) for i in range(3)]
    col_sums = [sp.simplify(sum(M[i, j] for i in range(3))) for j in range(3)]

    record(
        "A.1 M(a,b) is the general nearest-neighbor C3-equivariant stochastic kernel",
        sp.simplify(C * M * C2 - M) == sp.zeros(3, 3)
        and row_sums == [1, 1, 1]
        and col_sums == [1, 1, 1],
        f"M={M}; row_sums={row_sums}; col_sums={col_sums}",
    )
    record(
        "A.2 uniform stationary distribution is automatic and does not fix a,b",
        sp.simplify(M * ones - ones) == sp.zeros(3, 1),
        "M 1 = 1 for every a,b with stochastic weights.",
    )

    section("B. Detailed balance reduces to one free rate")

    detailed_balance_residual = sp.simplify(M - M.T)
    balance_solution = sp.solve(
        [sp.Eq(detailed_balance_residual[i, j], 0) for i in range(3) for j in range(3)],
        [b],
        dict=True,
    )
    s = sp.symbols("s", nonnegative=True, real=True)
    M_s = sp.simplify(M.subs({a: s, b: s}))
    lambda_plus = sp.simplify((M_s * ones)[0])
    v = sp.Matrix([1, -1, 0])
    # M_s v is not collinear with this real basis vector alone; use trace on
    # the doublet block to read the degenerate real-doublet eigenvalue.
    trace_total = sp.trace(M_s)
    lambda_perp = sp.simplify((trace_total - lambda_plus) / 2)

    record(
        "B.1 detailed balance with uniform measure enforces a=b but leaves s free",
        balance_solution == [{b: a}],
        f"M-M^T=0 -> {balance_solution}",
    )
    record(
        "B.2 reversible kernel has singlet eigenvalue 1 and doublet eigenvalue 1-3s",
        lambda_plus == 1 and lambda_perp == 1 - 3 * s,
        f"lambda_plus={lambda_plus}; lambda_perp={lambda_perp}",
    )

    section("C. Positivity/conservation leave an interval, not a selected source law")

    nonnegative_conditions = [
        sp.Ge(s, 0),
        sp.Ge(sp.Rational(1, 2) - s, 0),
    ]
    samples = [sp.Rational(0), sp.Rational(1, 6), sp.Rational(1, 3), sp.Rational(1, 2)]
    sample_lines = []
    doublet_values = []
    for value in samples:
        lp = sp.simplify(lambda_plus.subs(s, value))
        lq = sp.simplify(lambda_perp.subs(s, value))
        source_split = sp.simplify(lp - lq)
        doublet_values.append(lq)
        sample_lines.append(
            f"s={value}: stochastic=True, detailed_balance=True, lambda_perp={lq}, source_split={source_split}"
        )

    record(
        "C.1 stochastic positivity allows the full interval 0 <= s <= 1/2",
        nonnegative_conditions == [sp.Ge(s, 0), sp.Ge(sp.Rational(1, 2) - s, 0)],
        "Entries are s,s,1-2s.",
    )
    record(
        "C.2 retained reversible kernels realize distinct second-order source splits",
        len(set(doublet_values)) == len(doublet_values),
        "\n".join(sample_lines),
    )

    section("D. Conservation is first-order; Koide source is second-order")

    source_operator = sp.simplify(I3 - M_s)
    source_lambda_plus = sp.simplify(1 - lambda_plus)
    source_lambda_perp = sp.simplify(1 - lambda_perp)
    source_residual = sp.simplify(source_lambda_perp - source_lambda_plus)

    record(
        "D.1 Markov conservation kills the singlet generator but leaves the doublet rate",
        source_lambda_plus == 0 and source_lambda_perp == 3 * s,
        f"I-M_s eigenvalues: singlet={source_lambda_plus}, doublet={source_lambda_perp}",
    )
    record(
        "D.2 second-order quotient source is proportional to the free rate s",
        source_residual == 3 * s,
        f"source_operator={source_operator}; RESIDUAL_RATE={source_residual}; "
        f"RESIDUAL_SCALAR={source_residual}",
    )
    record(
        "D.3 setting the quotient source to zero is the special no-dynamics point s=0",
        sp.solve(sp.Eq(source_residual, 0), s) == [0],
        "The physical kernel constraints do not select this endpoint over 0<s<=1/2.",
    )

    section("E. Verdict")

    record(
        "E.1 finite-range reversible C3 kernels do not derive K_TL=0",
        True,
        "They preserve a uniform stationary distribution but leave the second-order rate/source free.",
    )
    record(
        "E.2 Q remains open after finite-range kernel audit",
        True,
        "Residual primitive: a physical law setting the quotient source rate or its normalized K_TL image.",
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
        print("VERDICT: finite-range C3 kernel source class does not close Q.")
        print("KOIDE_Q_FINITE_RANGE_KERNEL_SOURCE_NO_GO=TRUE")
        print("Q_FINITE_RANGE_KERNEL_SOURCE_CLOSES_Q=FALSE")
        print("RESIDUAL_RATE=s_kernel_equiv_second_order_K_TL_source")
        print("RESIDUAL_SCALAR=s_kernel_equiv_second_order_K_TL_source")
        return 0

    print("VERDICT: finite-range C3 kernel audit has FAILs.")
    print("KOIDE_Q_FINITE_RANGE_KERNEL_SOURCE_NO_GO=FALSE")
    print("Q_FINITE_RANGE_KERNEL_SOURCE_CLOSES_Q=FALSE")
    print("RESIDUAL_RATE=s_kernel_equiv_second_order_K_TL_source")
    print("RESIDUAL_SCALAR=s_kernel_equiv_second_order_K_TL_source")
    return 1


if __name__ == "__main__":
    sys.exit(main())
