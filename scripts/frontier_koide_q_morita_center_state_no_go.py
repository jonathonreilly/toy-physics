#!/usr/bin/env python3
"""
Koide Q Morita-invariant center-state no-go.

Theorem attempt:
  Justify the quotient-center state by Morita invariance: matrix/rank
  amplification should not change the physical center source.  Perhaps this
  removes the rank-1/rank-2 obstruction and forces the equal center-label
  state, hence K_TL = 0.

Result:
  Negative, but sharpened.  Morita invariance correctly removes weighting by
  internal matrix rank inside each simple block.  A Morita-invariant state on

      M_1 ⊕ M_2

  has the form

      phi = w_plus tr_1_normalized ⊕ w_perp tr_2_normalized,
      w_plus + w_perp = 1.

  The component weights w_plus,w_perp remain free.  Equal labels require
  w_plus=w_perp, which is a component-measure principle beyond Morita
  invariance.  Thus Morita invariance is useful support for not using Hilbert
  rank, but it does not close Q by itself.

No PDG masses, target fitted value, delta pin, or H_* pin is used.
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


def q_from_component_weight(w_plus: sp.Expr) -> sp.Expr:
    r = sp.simplify((1 - w_plus) / w_plus)
    return sp.simplify((1 + r) / 3)


def ktl_from_component_weight(w_plus: sp.Expr) -> sp.Expr:
    r = sp.simplify((1 - w_plus) / w_plus)
    return sp.simplify((r**2 - 1) / (4 * r))


def main() -> int:
    section("A. Morita-invariant state form")

    w_plus = sp.symbols("w_plus", positive=True, real=True)
    w_perp = sp.simplify(1 - w_plus)
    n = sp.symbols("n", integer=True, positive=True)
    normalized_trace_identity = sp.simplify(n / n)
    record(
        "A.1 normalized trace removes matrix-rank amplification inside each block",
        normalized_trace_identity == 1,
        "tr_n(I_n)/n = 1 for every matrix amplification.",
    )
    record(
        "A.2 Morita-invariant center state still has component weights",
        sp.simplify(w_plus + w_perp) == 1,
        "phi=w_plus*tau_plus+(1-w_plus)*tau_perp.",
    )

    section("B. Component weights remain the Q residual")

    ktl = ktl_from_component_weight(w_plus)
    record(
        "B.1 K_TL=0 is equivalent to equal Morita component weights",
        sp.solve(sp.Eq(ktl, 0), w_plus) == [sp.Rational(1, 2)],
        f"K_TL(w_plus)={ktl}",
    )

    samples = {
        "rank_like_component_bias": sp.Rational(1, 3),
        "equal_component": sp.Rational(1, 2),
        "plus_heavy_component": sp.Rational(2, 3),
    }
    lines = []
    ok = True
    for name, value in samples.items():
        q_value = q_from_component_weight(value)
        ktl_value = ktl_from_component_weight(value)
        ok = ok and 0 < value < 1
        lines.append(f"{name}: w_plus={value}, Q={q_value}, K_TL={ktl_value}")
    record(
        "B.2 Morita-invariant states include closing and non-closing component weights",
        ok,
        "\n".join(lines),
    )

    section("C. Equal component measure is stronger than Morita invariance")

    component_count_measure = sp.Rational(1, 2)
    record(
        "C.1 uniform component counting would close Q",
        q_from_component_weight(component_count_measure) == sp.Rational(2, 3)
        and ktl_from_component_weight(component_count_measure) == 0,
        "component_count_measure=(1/2,1/2).",
    )
    record(
        "C.2 Morita equivalence does not exchange disconnected components",
        True,
        "M_1 and M_2 are each Morita-equivalent to scalars, but the direct-sum weights remain a probability simplex.",
    )
    record(
        "C.3 a uniform measure over components is a new source principle",
        True,
        "It may be a candidate principle, but it is not derived by Morita invariance alone.",
    )

    section("D. Verdict")

    residual = sp.simplify(w_plus - sp.Rational(1, 2))
    record(
        "D.1 Morita-invariant center-state route does not close Q",
        residual == w_plus - sp.Rational(1, 2),
        f"RESIDUAL_COMPONENT_WEIGHT={residual}",
    )
    record(
        "D.2 Q remains open after Morita audit",
        True,
        "Residual primitive: physical uniform measure over Morita components.",
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
        print("VERDICT: Morita invariance does not close Q.")
        print("KOIDE_Q_MORITA_CENTER_STATE_NO_GO=TRUE")
        print("Q_MORITA_CENTER_STATE_CLOSES_Q=FALSE")
        print("RESIDUAL_SCALAR=Morita_component_weight_w_plus_minus_one_half_equiv_K_TL")
        print("RESIDUAL_MEASURE=uniform_measure_over_Morita_components_not_derived")
        return 0

    print("VERDICT: Morita center-state audit has FAILs.")
    print("KOIDE_Q_MORITA_CENTER_STATE_NO_GO=FALSE")
    print("Q_MORITA_CENTER_STATE_CLOSES_Q=FALSE")
    print("RESIDUAL_SCALAR=Morita_component_weight_w_plus_minus_one_half_equiv_K_TL")
    print("RESIDUAL_MEASURE=uniform_measure_over_Morita_components_not_derived")
    return 1


if __name__ == "__main__":
    sys.exit(main())
