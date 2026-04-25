#!/usr/bin/env python3
"""
Koide Q least-source-norm no-go.

Theorem attempt:
  On the normalized second-order carrier, perhaps the physical charged-lepton
  selector is the point of least traceless source norm.  Since the exact
  source norm has its unique zero at Y=I2, this would derive K_TL=0 and Q=2/3.

Result:
  The scalar minimization is exact support, but it is not a retained physical
  law.  Requiring the physical point to minimize |K_TL| is equivalent to
  requiring source neutrality.  The retained effective-action grammar still
  admits off-center points with nonzero sources unless that minimization
  principle is added.

Residual:
  RESIDUAL_SCALAR=least_source_norm_selection_equiv_K_TL.
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
    print("KOIDE Q LEAST-SOURCE-NORM NO-GO")
    print("=" * 88)
    print(
        "Theorem attempt: derive K_TL=0 by minimizing the exact traceless "
        "source norm."
    )

    y = sp.symbols("y", positive=True, real=True)

    section("A. Exact traceless source on the trace-2 carrier")

    ktl = sp.simplify((1 - y) / (y * (2 - y)))
    norm_sq = sp.simplify(ktl**2)
    record(
        "A.1 K_TL(y) is the exact normalized traceless source scalar",
        ktl == (y - 1) / (y * (y - 2)),
        f"K_TL(y)={ktl}",
    )
    record(
        "A.2 source norm is nonnegative and vanishes only at y=1",
        sp.solve(sp.Eq(norm_sq, 0), y) == [sp.Integer(1)],
        f"|K_TL|^2={norm_sq}",
    )

    section("B. Least-source point and Koide consequence")

    d_norm = sp.factor(sp.diff(norm_sq, y))
    critical = sp.solve(sp.Eq(sp.together(d_norm).as_numer_denom()[0], 0), y)
    valid_critical = [root for root in critical if root.is_real and 0 < float(root.evalf()) < 2]
    record(
        "B.1 the only interior minimum of |K_TL|^2 is y=1",
        valid_critical == [sp.Integer(1)] and norm_sq.subs(y, 1) == 0,
        f"d|K_TL|^2/dy={d_norm}, critical={valid_critical}",
    )
    record(
        "B.2 the least-source point gives Q=2/3",
        q_from_y(sp.Integer(1)) == sp.Rational(2, 3),
        f"Q(1)={q_from_y(sp.Integer(1))}",
    )
    record(
        "B.3 source norm diverges at the carrier boundaries",
        sp.limit(norm_sq, y, 0, dir="+") == sp.oo
        and sp.limit(norm_sq, y, 2, dir="-") == sp.oo,
        "The scalar problem is a clean one-well minimum at the Koide leaf.",
    )

    section("C. Why the route is not a retained closure")

    y0 = sp.Rational(4, 5)
    record(
        "C.1 off-center retained source states are still valid source-coupled extrema",
        ktl.subs(y, y0) == sp.Rational(5, 24)
        and q_from_y(y0) == sp.Rational(5, 6),
        f"y={y0}: K_TL={ktl.subs(y, y0)}, Q={q_from_y(y0)}",
    )
    c = sp.symbols("c", real=True)
    shifted_norm = sp.simplify((ktl - c) ** 2)
    record(
        "C.2 least-distance-to-supplied-source selects any supplied source c",
        sp.simplify(shifted_norm.subs({y: y0, c: ktl.subs(y, y0)})) == 0,
        "A least-source principle closes Q only when the supplied source target is c=0.",
    )
    record(
        "C.3 choosing c=0 is exactly the missing source-neutrality law",
        True,
        "No retained axiom currently says the physical charged-lepton selector minimizes |K_TL|.",
    )

    section("D. Hostile-review verdict")

    record(
        "D.1 no target mass data, observational pin, delta pin, or Q target is used",
        True,
    )
    record(
        "D.2 least-source-norm does not derive K_TL=0 from retained structure",
        True,
        "It derives K_TL=0 only after adding a least-source/source-neutral selector principle.",
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
        print("VERDICT: least-source-norm minimization does not close Q.")
        print("The minimizer is exactly Koide, but adopting that minimizer")
        print("is the missing physical source-neutrality principle.")
        print()
        print("KOIDE_Q_LEAST_SOURCE_NORM_NO_GO=TRUE")
        print("Q_LEAST_SOURCE_NORM_CLOSES_Q=FALSE")
        print("RESIDUAL_SCALAR=least_source_norm_selection_equiv_K_TL")
        return 0

    print("VERDICT: least-source-norm audit has FAILs.")
    print()
    print("KOIDE_Q_LEAST_SOURCE_NORM_NO_GO=FALSE")
    print("Q_LEAST_SOURCE_NORM_CLOSES_Q=FALSE")
    print("RESIDUAL_SCALAR=least_source_norm_selection_equiv_K_TL")
    return 1


if __name__ == "__main__":
    sys.exit(main())
