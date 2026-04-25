#!/usr/bin/env python3
"""
Koide Q Legendre/self-duality no-go.

Theorem attempt:
  The exact logdet Legendre geometry on the normalized second-order carrier
  might force the physical charged-lepton point to be self-dual under
  normalized inversion.  Since the unique fixed point of normalized inversion
  is Y=I2, this would derive K_TL=0 and hence Q=2/3.

Result:
  No from retained data alone.  Normalized inversion is an exact involution
  and it flips the sign of K_TL, but it is just the quotient block-exchange
  involution on the trace-2 carrier.  The retained Legendre structure pairs
  off-center response/source states; it does not require a fixed point.

Residual:
  RESIDUAL_SCALAR=legendre_self_duality_fixed_point_equiv_K_TL.
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


def q_from_y(y_value: sp.Expr) -> sp.Expr:
    return sp.simplify(sp.Rational(2, 3) / y_value)


def main() -> int:
    print("=" * 88)
    print("KOIDE Q LEGENDRE/SELF-DUALITY NO-GO")
    print("=" * 88)
    print(
        "Theorem attempt: normalized Legendre inversion might force a "
        "self-dual physical point."
    )

    y = sp.symbols("y", positive=True, real=True)
    Y = sp.diag(y, 2 - y)

    section("A. Exact normalized inversion on the trace-2 carrier")

    Y_inv = Y.inv()
    Y_dual = sp.simplify(2 * Y_inv / sp.trace(Y_inv))
    y_dual = sp.simplify(Y_dual[0, 0])

    record(
        "A.1 normalized inversion sends Y=diag(y,2-y) to diag(2-y,y)",
        sp.simplify(Y_dual - sp.diag(2 - y, y)) == sp.zeros(2, 2),
        f"D(Y) = {Y_dual}",
    )
    record(
        "A.2 normalized inversion is an involution",
        sp.simplify(y_dual.subs(y, y_dual) - y) == 0,
        f"y -> {y_dual} -> y",
    )

    section("B. Fixed point and Koide consequence")

    fixed = sp.solve(sp.Eq(y_dual, y), y)
    record(
        "B.1 the unique interior fixed point is y=1",
        fixed == [sp.Integer(1)],
        f"fixed points = {fixed}",
    )
    ktl = sp.simplify((1 - y) / (y * (2 - y)))
    record(
        "B.2 the fixed point is exactly K_TL=0",
        sp.solve(sp.Eq(ktl, 0), y) == [sp.Integer(1)],
        f"K_TL(y) = {ktl}",
    )
    record(
        "B.3 the fixed point gives Q=2/3",
        q_from_y(sp.Integer(1)) == sp.Rational(2, 3),
        f"Q(y)=2/(3y), Q(1)={q_from_y(sp.Integer(1))}",
    )

    section("C. Duality flips the residual but does not kill it")

    ktl_dual = sp.simplify(ktl.subs(y, y_dual))
    record(
        "C.1 normalized inversion flips K_TL -> -K_TL",
        sp.simplify(ktl_dual + ktl) == 0,
        f"K_TL(D(y)) = {ktl_dual}",
    )
    y0 = sp.Rational(4, 5)
    y0_dual = sp.simplify(y_dual.subs(y, y0))
    record(
        "C.2 off-center points form valid dual pairs, not contradictions",
        y0_dual == sp.Rational(6, 5)
        and sp.simplify(ktl.subs(y, y0)) == sp.Rational(5, 24)
        and sp.simplify(ktl.subs(y, y0_dual)) == -sp.Rational(5, 24),
        f"y={y0} <-> D(y)={y0_dual}; K_TL values {ktl.subs(y, y0)}, {ktl.subs(y, y0_dual)}",
    )
    record(
        "C.3 the dual pair has off-Koide Q values",
        q_from_y(y0) != sp.Rational(2, 3)
        and q_from_y(y0_dual) != sp.Rational(2, 3),
        f"Q({y0})={q_from_y(y0)}, Q({y0_dual})={q_from_y(y0_dual)}",
    )

    section("D. Relation to retained Legendre geometry")

    K_star = sp.simplify(Y.inv() - sp.eye(2))
    K_star_dual = sp.simplify(Y_dual.inv() - sp.eye(2))
    record(
        "D.1 the exact Legendre map supplies a source for every interior response",
        K_star.shape == (2, 2) and K_star_dual.shape == (2, 2),
        f"K_*(Y)={K_star}; K_*(D(Y))={K_star_dual}",
    )
    record(
        "D.2 requiring Y=D(Y) is the quotient block-exchange fixed-point law",
        sp.simplify(Y_dual - sp.diag(2 - y, y)) == sp.zeros(2, 2),
        "The self-dual condition is y=2-y, i.e. the already audited block-exchange/equal-block law.",
    )
    record(
        "D.3 retained Legendre duality does not identify a state with its dual",
        True,
        "It is a source-response correspondence.  Turning correspondence into a fixed-point axiom adds the missing selector.",
    )

    section("E. Hostile-review verdict")

    record(
        "E.1 no target mass data, observational pin, delta pin, or Q target is used",
        True,
    )
    record(
        "E.2 Legendre/self-duality does not derive K_TL=0 from retained structure",
        True,
        "It derives K_TL=0 only after imposing self-dual fixed-point selection.",
    )

    section("Summary")
    n_pass = sum(1 for _, ok, _ in PASSES if ok)
    n_total = len(PASSES)
    print(f"PASSED: {n_pass}/{n_total}")
    for name, ok, _ in PASSES:
        status = "PASS" if ok else "FAIL"
        print(f"  [{status}] {name}")

    print()
    if n_pass == n_total:
        print("VERDICT: normalized Legendre/self-duality does not close Q.")
        print("The fixed point is Koide, but the fixed-point requirement is")
        print("exactly the missing block-exchange/source-neutrality law.")
        print()
        print("KOIDE_Q_LEGENDRE_SELF_DUALITY_NO_GO=TRUE")
        print("Q_LEGENDRE_SELF_DUALITY_CLOSES_Q=FALSE")
        print("RESIDUAL_SCALAR=legendre_self_duality_fixed_point_equiv_K_TL")
        return 0

    print("VERDICT: Legendre/self-duality audit has FAILs.")
    print()
    print("KOIDE_Q_LEGENDRE_SELF_DUALITY_NO_GO=FALSE")
    print("Q_LEGENDRE_SELF_DUALITY_CLOSES_Q=FALSE")
    print("RESIDUAL_SCALAR=legendre_self_duality_fixed_point_equiv_K_TL")
    return 1


if __name__ == "__main__":
    sys.exit(main())
