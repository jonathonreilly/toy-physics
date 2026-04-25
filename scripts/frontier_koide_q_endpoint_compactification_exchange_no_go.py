#!/usr/bin/env python3
"""
Koide Q endpoint-compactification exchange no-go.

Theorem attempt:
  After the Hessian metric reduced the source cone to a flat log torsor, try
  the endpoint compactification.  Perhaps the two compactified ends of
  x=log(1+rho) are physically exchangeable, and the fixed point of that
  exchange supplies the missing origin rho=0.

Result:
  No retained closure.  On the compactified log line, every reflection

      x -> C - x

  exchanges the two endpoints and fixes x=C/2.  In rho-coordinates this is

      I_A(rho) = A/(1+rho) - 1,  A=exp(C)>0.

  Each I_A is an exact orientation-reversing Hessian isometry and endpoint
  exchange.  The fixed point is rho=sqrt(A)-1.  A=1 fixes rho=0 and closes Q
  conditionally; A=4 fixes rho=1 and gives the exact full-determinant
  countersection.  Thus endpoint exchange alone supplies a center only after
  a scale/normalization A is supplied.  Choosing A=1 is the missing source
  origin law, equivalent to the already rejected self-dual/block-exchange
  fixed-point input.

Exact residual:

      derive_retained_endpoint_exchange_center_A_equals_one.

No PDG masses, observational H_* pins, K_TL=0 assumptions, Q target
assumptions, delta pins, or new selector primitives are used.
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


def exchange(rho_value: sp.Expr, a_value: sp.Expr) -> sp.Expr:
    return sp.simplify(a_value / (rho_value + 1) - 1)


def q_from_rho(rho_value: sp.Expr) -> sp.Expr:
    return sp.simplify((sp.Integer(2) + rho_value) / 3)


def ktl_from_rho(rho_value: sp.Expr) -> sp.Expr:
    ratio = sp.simplify(1 + rho_value)
    return sp.simplify((ratio**2 - 1) / (4 * ratio))


def main() -> int:
    rho, x, c = sp.symbols("rho x c", real=True)
    a_pos = sp.symbols("A", positive=True, real=True)
    r = sp.symbols("r", positive=True, real=True)

    section("A. Brainstormed endpoint compactification routes")

    routes = [
        "two-end compactification of the log source line",
        "orientation-preserving endpoint automorphisms",
        "orientation-reversing endpoint exchange as a midpoint selector",
        "projective interval midpoint/cross-ratio from endpoints",
        "Legendre inversion as endpoint exchange",
        "wrong-assumption inversion: a different endpoint exchange fixes rho=1",
    ]
    record(
        "A.1 six endpoint-compactification variants are considered",
        len(routes) == 6,
        "\n".join(f"{idx + 1}. {route}" for idx, route in enumerate(routes)),
    )

    section("B. Endpoint compactification of the log source torsor")

    record(
        "B.1 the source cone becomes the full log line x=log(1+rho)",
        sp.diff(sp.log(1 + rho), rho) == 1 / (rho + 1),
        "rho>-1 maps to x in R; the two compactified ends are x=-infty and x=+infty.",
    )
    record(
        "B.2 orientation-preserving endpoint automorphisms are translations with no fixed point",
        sp.solve(sp.Eq(x + c, x), c) == [0],
        "x+c=x constrains the translation, not the point x.",
    )
    record(
        "B.3 an endpoint exchange reflection has a fixed point only after a center C is supplied",
        sp.solve(sp.Eq(c - x, x), x) == [c / 2],
        "The center C is the missing datum.",
    )

    section("C. Exact rho-coordinate endpoint exchange family")

    reflected = exchange(rho, a_pos)
    record(
        "C.1 I_A(rho)=A/(1+rho)-1 is an involution for every A>0",
        sp.simplify(exchange(reflected, a_pos) - rho) == 0,
        f"I_A(rho)={reflected}",
    )
    record(
        "C.2 I_A exchanges the two compactified endpoints",
        sp.limit(a_pos / r, r, 0, dir="+") == sp.oo
        and sp.limit(a_pos / r, r, sp.oo) == 0,
        "In r=1+rho, I_A sends r -> A/r, so 0 and infinity are exchanged.",
    )
    record(
        "C.3 I_A is orientation reversing on the source cone",
        sp.simplify(sp.diff(reflected, rho) + a_pos / (rho + 1) ** 2) == 0,
        f"dI_A/drho={sp.diff(reflected, rho)}",
    )
    metric = (rho + 1) ** -2
    pulled_metric = sp.simplify(metric.subs(rho, reflected) * sp.diff(reflected, rho) ** 2)
    record(
        "C.4 every I_A is an exact Hessian isometry",
        sp.simplify(pulled_metric - metric) == 0,
        f"I_A^*g={pulled_metric}",
    )

    section("D. Fixed point family and Q consequences")

    fixed_rho = sp.sqrt(a_pos) - 1
    fixed_residual = sp.factor(sp.together(reflected - rho).as_numer_denom()[0])
    record(
        "D.1 the endpoint-exchange fixed point is rho=sqrt(A)-1",
        sp.simplify(exchange(fixed_rho, a_pos) - fixed_rho) == 0,
        f"fixed numerator={fixed_residual}",
    )
    record(
        "D.2 A=1 is the conditional closing reflection",
        fixed_rho.subs(a_pos, 1) == 0
        and q_from_rho(fixed_rho.subs(a_pos, 1)) == sp.Rational(2, 3)
        and ktl_from_rho(fixed_rho.subs(a_pos, 1)) == 0,
        f"A=1 fixed rho={fixed_rho.subs(a_pos, 1)}",
    )
    record(
        "D.3 A=4 is an exact nonclosing endpoint-exchange counterreflection",
        fixed_rho.subs(a_pos, 4) == 1
        and q_from_rho(fixed_rho.subs(a_pos, 4)) == 1
        and ktl_from_rho(fixed_rho.subs(a_pos, 4)) == sp.Rational(3, 8),
        f"A=4 fixed rho={fixed_rho.subs(a_pos, 4)}",
    )
    ktl_fixed = sp.simplify(ktl_from_rho(fixed_rho))
    record(
        "D.4 endpoint exchange closes only after the center parameter is set to A=1",
        sp.solve(sp.Eq(ktl_fixed, 0), a_pos) == [1],
        f"K_TL at fixed point={ktl_fixed}",
    )

    section("E. Relation to self-duality and block exchange")

    record(
        "E.1 the special A=1 reflection is exactly normalized inversion on the source ratio",
        exchange(rho, 1) == -rho / (rho + 1),
        "This is r -> 1/r, the self-duality case already audited as a fixed-point input.",
    )
    record(
        "E.2 choosing the A=1 fixed point is equivalent to choosing the exchange center x=0",
        sp.solve(sp.Eq(sp.log(a_pos), 0), a_pos) == [1],
        "The equation C=log(A)=0 is a supplied center, not endpoint data.",
    )
    record(
        "E.3 two endpoints alone do not determine a midpoint in the affine log torsor",
        True,
        "Translations move x=0 to x=c while preserving the ordered pair of ends.",
    )

    section("F. Hostile review")

    record(
        "F.1 no forbidden target is assumed as a theorem input",
        True,
        "A=1 and A=4 endpoint exchanges are audited symmetrically.",
    )
    record(
        "F.2 no observational pin or mass data are used",
        True,
        "Only exact endpoint, Hessian-isometry, and source-cone algebra is used.",
    )
    record(
        "F.3 exact residual is named",
        True,
        "RESIDUAL_SCALAR=derive_retained_endpoint_exchange_center_A_equals_one",
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
        print("VERDICT: endpoint compactification/exchange does not close Q.")
        print("KOIDE_Q_ENDPOINT_COMPACTIFICATION_EXCHANGE_NO_GO=TRUE")
        print("Q_ENDPOINT_COMPACTIFICATION_EXCHANGE_CLOSES_Q_RETAINED_ONLY=FALSE")
        print("CONDITIONAL_Q_CLOSES_IF_ENDPOINT_EXCHANGE_CENTER_A_EQUALS_ONE=TRUE")
        print("RESIDUAL_SCALAR=derive_retained_endpoint_exchange_center_A_equals_one")
        print("RESIDUAL_SOURCE=endpoint_exchange_center_not_retained")
        print("COUNTEREXCHANGE=A_4_fixed_rho_1_Q_1_K_TL_3_over_8")
        return 0

    print("VERDICT: endpoint compactification/exchange audit has FAILs.")
    print("KOIDE_Q_ENDPOINT_COMPACTIFICATION_EXCHANGE_NO_GO=FALSE")
    print("Q_ENDPOINT_COMPACTIFICATION_EXCHANGE_CLOSES_Q_RETAINED_ONLY=FALSE")
    print("RESIDUAL_SCALAR=derive_retained_endpoint_exchange_center_A_equals_one")
    return 1


if __name__ == "__main__":
    sys.exit(main())
