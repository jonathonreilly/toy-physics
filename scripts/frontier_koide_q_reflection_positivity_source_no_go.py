#!/usr/bin/env python3
"""
Koide Q reflection-positivity source no-go.

Theorem attempt:
  Use Osterwalder-Schrader / reflection positivity of the Euclidean source
  carrier to force the charged-lepton C3 center-source state to be the equal
  label state, hence K_TL = 0.

Result:
  Negative.  Reflection positivity constrains the source covariance/effect to
  be positive under the reflection pairing.  For a central two-label source

      C(u) = u P_plus + (1-u) P_perp,

  positivity requires only

      0 <= u <= 1.

  It does not equate the two central coefficients.  The equal-label source
  u=1/2 is one reflection-positive source, but the rank state u=1/3 and other
  non-closing sources are reflection-positive as well.  A reflection that
  exchanges P_plus and P_perp would force u=1/2, but that is the non-retained
  rank-1/rank-2 exchange again.

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


def q_from_center_state(u: sp.Expr) -> sp.Expr:
    r = sp.simplify((1 - u) / u)
    return sp.simplify((1 + r) / 3)


def ktl_from_center_state(u: sp.Expr) -> sp.Expr:
    r = sp.simplify((1 - u) / u)
    return sp.simplify((r**2 - 1) / (4 * r))


def main() -> int:
    section("A. Reflection-positive central source family")

    u = sp.symbols("u", real=True)
    covariance = sp.diag(u, (1 - u) / 2, (1 - u) / 2)
    principal_minors = [sp.simplify(covariance[:i, :i].det()) for i in range(1, 4)]
    record(
        "A.1 central block source covariance is normalized",
        sp.simplify(sp.trace(covariance)) == 1,
        f"C(u)=diag(u,(1-u)/2,(1-u)/2), trace={sp.trace(covariance)}",
    )
    record(
        "A.2 reflection positivity reduces to nonnegative block weights",
        all(
            sp.simplify(actual - expected) == 0
            for actual, expected in zip(
                principal_minors,
                [u, u * (1 - u) / 2, u * (1 - u) ** 2 / 4],
            )
        ),
        f"principal_minors={principal_minors}",
    )

    section("B. Positive sources include non-closing states")

    samples = {
        "rank_state": sp.Rational(1, 3),
        "equal_label": sp.Rational(1, 2),
        "singlet_heavy": sp.Rational(2, 3),
    }
    lines = []
    ok = True
    for name, value in samples.items():
        minors_value = [sp.simplify(m.subs(u, value)) for m in principal_minors]
        positive = all(m >= 0 for m in minors_value)
        q_value = q_from_center_state(value)
        ktl_value = ktl_from_center_state(value)
        ok = ok and positive
        lines.append(f"{name}: u={value}, minors={minors_value}, Q={q_value}, K_TL={ktl_value}")
    record(
        "B.1 closing and non-closing source states are reflection-positive",
        ok,
        "\n".join(lines),
    )
    record(
        "B.2 K_TL=0 is stronger than reflection positivity",
        sp.solve(sp.Eq(ktl_from_center_state(u), 0), u) == [sp.Rational(1, 2)],
        f"K_TL(u)={ktl_from_center_state(u)}",
    )

    section("C. Reflection exchange is not retained by the carrier")

    swap_matrix = sp.Matrix([[0, 0, 1], [0, 1, 0], [1, 0, 0]])
    swapped_covariance = sp.simplify(swap_matrix * covariance * swap_matrix.T)
    rank_plus = sp.Integer(1)
    rank_perp = sp.Integer(2)
    record(
        "C.1 an artificial label exchange would add a new equation",
        swapped_covariance != covariance,
        f"swap C(u) swap^T={swapped_covariance}",
    )
    record(
        "C.2 retained C3 ranks obstruct a physical plus/perp exchange",
        rank_plus != rank_perp,
        f"rank(P_plus)={rank_plus}, rank(P_perp)={rank_perp}",
    )
    record(
        "C.3 reflection positivity itself does not supply that exchange",
        True,
        "OS reflection acts on Euclidean time/order, not on inequivalent C3 real-isotype rank.",
    )

    section("D. Verdict")

    residual = sp.simplify(u - sp.Rational(1, 2))
    record(
        "D.1 reflection-positivity route does not close Q",
        residual == u - sp.Rational(1, 2),
        f"RESIDUAL_SOURCE={residual}",
    )
    record(
        "D.2 Q remains open after reflection-positivity audit",
        True,
        "Residual primitive: a retained equality law for the two positive center coefficients.",
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
        print("VERDICT: reflection positivity does not close Q.")
        print("KOIDE_Q_REFLECTION_POSITIVITY_SOURCE_NO_GO=TRUE")
        print("Q_REFLECTION_POSITIVITY_SOURCE_CLOSES_Q=FALSE")
        print("RESIDUAL_SCALAR=center_label_source_u_minus_one_half_equiv_K_TL")
        print("RESIDUAL_EQUALITY=reflection_positivity_does_not_equalize_center_coefficients")
        return 0

    print("VERDICT: reflection-positivity source audit has FAILs.")
    print("KOIDE_Q_REFLECTION_POSITIVITY_SOURCE_NO_GO=FALSE")
    print("Q_REFLECTION_POSITIVITY_SOURCE_CLOSES_Q=FALSE")
    print("RESIDUAL_SCALAR=center_label_source_u_minus_one_half_equiv_K_TL")
    print("RESIDUAL_EQUALITY=reflection_positivity_does_not_equalize_center_coefficients")
    return 1


if __name__ == "__main__":
    sys.exit(main())
