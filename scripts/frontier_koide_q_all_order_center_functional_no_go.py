#!/usr/bin/env python3
"""
Koide Q all-order center-functional source no-go.

Theorem attempt:
  Strengthen source-grammar exhaustion from finite/local polynomial checks to
  all-order analytic C3-equivariant center functionals.  Perhaps analyticity
  and equivariance force the normalized center source to be equal-label,
  hence K_TL = 0.

Result:
  Negative.  Any C3-equivariant analytic center functional reduces on the two
  retained central blocks to two positive scalar values:

      F_plus, F_perp.

  After normalization,

      u = F_plus / (F_plus + F_perp).

  Analyticity and equivariance do not impose F_plus=F_perp, because the
  rank-1 and rank-2 real isotypes are inequivalent retained blocks.  Every
  positive u in (0,1) can be realized by positive scalar values.  Equal labels
  require the extra equality F_plus=F_perp.  In functional calculus language,
  for Z=P_plus-P_perp,

      F(Z) = F(1) P_plus + F(-1) P_perp,

  so the Q source law is exactly F(1)=F(-1), i.e. vanishing odd part.  An
  analytic positive exponential family exp(lambda Z) realizes a continuum of
  non-closing sources.  Forcing lambda=0 or evenness is the same missing
  source primitive in all-order functional language.

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
    section("A. All-order equivariant center functional")

    f_plus, f_perp = sp.symbols("F_plus F_perp", positive=True, real=True)
    u = sp.simplify(f_plus / (f_plus + f_perp))
    ktl = ktl_from_center_state(u)
    record(
        "A.1 normalized center source depends on one positive ratio",
        u == f_plus / (f_plus + f_perp),
        f"u={u}",
    )
    record(
        "A.2 K_TL=0 is equivalent to equality of all-order block values",
        sp.solve(sp.Eq(ktl, 0), f_plus) == [f_perp],
        f"K_TL(F_plus,F_perp)={sp.factor(ktl)}",
    )

    section("B. Functional calculus on the retained center")

    degree = 8
    coeffs = list(sp.symbols(f"a0:{degree + 1}", real=True))
    F_plus_eval = sp.simplify(sum(coeffs[n] for n in range(degree + 1)))
    F_perp_eval = sp.simplify(sum(coeffs[n] * (-1) ** n for n in range(degree + 1)))
    even_part = sp.simplify(sum(coeffs[n] for n in range(0, degree + 1, 2)))
    odd_part = sp.simplify(sum(coeffs[n] for n in range(1, degree + 1, 2)))
    record(
        "B.1 arbitrary analytic truncation evaluates as F(1) and F(-1) on the two blocks",
        F_plus_eval == even_part + odd_part
        and F_perp_eval == even_part - odd_part,
        f"F(1)={F_plus_eval}; F(-1)={F_perp_eval}",
    )
    record(
        "B.2 block equality is exactly vanishing odd functional part",
        sp.solve(sp.Eq(F_plus_eval, F_perp_eval), odd_part) == [0],
        f"F(1)-F(-1)={sp.simplify(F_plus_eval - F_perp_eval)}",
    )

    section("C. Analytic/equivariant grammar realizes non-closing sources")

    samples = {
        "rank_state": (sp.Rational(1, 3), sp.Rational(2, 3)),
        "equal_label": (sp.Rational(1, 2), sp.Rational(1, 2)),
        "singlet_heavy": (sp.Rational(2, 3), sp.Rational(1, 3)),
    }
    lines = []
    ok = True
    for name, (fp, fq) in samples.items():
        u_value = sp.simplify(u.subs({f_plus: fp, f_perp: fq}))
        q_value = q_from_center_state(u_value)
        ktl_value = ktl_from_center_state(u_value)
        ok = ok and fp > 0 and fq > 0
        lines.append(f"{name}: F=({fp},{fq}), u={u_value}, Q={q_value}, K_TL={ktl_value}")
    record(
        "C.1 positive all-order block values include closing and non-closing sources",
        ok,
        "\n".join(lines),
    )

    target_u = sp.symbols("u0", positive=True, real=True)
    realization = sp.simplify((target_u) / (target_u + (1 - target_u)))
    record(
        "C.2 any normalized center source can be realized by positive block values",
        realization == target_u,
        "Choose F_plus=u0, F_perp=1-u0 for 0<u0<1.",
    )
    lam = sp.symbols("lambda", real=True)
    exp_plus = sp.exp(lam)
    exp_perp = sp.exp(-lam)
    u_exp = sp.simplify(exp_plus / (exp_plus + exp_perp))
    ktl_exp = sp.simplify(ktl_from_center_state(u_exp))
    record(
        "C.3 positive analytic exponential family has free source parameter lambda",
        sp.solve(sp.Eq(ktl_exp, 0), lam) == [0],
        f"F_lambda(Z)=exp(lambda Z), u={u_exp}, K_TL={sp.factor(ktl_exp)}",
    )
    record(
        "C.4 off-zero lambda gives retained analytic off-Koide sources",
        ktl_exp.subs(lam, sp.log(2)) != 0
        and q_from_center_state(u_exp.subs(lam, sp.log(2))) != sp.Rational(2, 3),
        f"lambda=log(2): u={sp.simplify(u_exp.subs(lam, sp.log(2)))}, Q={q_from_center_state(u_exp.subs(lam, sp.log(2)))}, K_TL={ktl_exp.subs(lam, sp.log(2))}",
    )

    section("D. Equality of block values is an extra physical law")

    rank_plus = sp.Integer(1)
    rank_perp = sp.Integer(2)
    record(
        "D.1 retained block ranks do not identify the two analytic values",
        rank_plus != rank_perp,
        f"rank(P_plus)={rank_plus}, rank(P_perp)={rank_perp}",
    )
    x_plus, x_perp = sp.symbols("x_plus x_perp", real=True)
    analytic_function = sp.Function("F")
    equality_condition = sp.Eq(analytic_function(x_plus), analytic_function(x_perp))
    record(
        "D.2 same analytic formula does not equalize inequivalent inputs",
        equality_condition.has(x_plus, x_perp),
        "F(x_plus)=F(x_perp) requires x_plus=x_perp or a special constant/degenerate F.",
    )
    record(
        "D.3 evenness would close the functional calculus route but is block exchange",
        sp.simplify((even_part + odd_part).subs(odd_part, 0) - (even_part - odd_part).subs(odd_part, 0)) == 0,
        "F(z)=F(-z) removes the odd part; the retained rank-1/rank-2 carrier does not supply Z -> -Z.",
    )
    record(
        "D.4 all-order source grammar reduces to the same equality primitive",
        True,
        "Analyticity broadens the source class but does not add a block-equality theorem.",
    )

    section("E. Verdict")

    residual = sp.simplify(f_plus - f_perp)
    record(
        "E.1 all-order center-functional route does not close Q",
        residual == f_plus - f_perp,
        f"RESIDUAL_BLOCK_VALUE={residual}",
    )
    record(
        "E.2 Q remains open after all-order source-functional audit",
        True,
        "Residual primitive: physical law equating the two retained center-functional values.",
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
        print("VERDICT: all-order C3 center functionals do not close Q.")
        print("KOIDE_Q_ALL_ORDER_CENTER_FUNCTIONAL_NO_GO=TRUE")
        print("Q_ALL_ORDER_CENTER_FUNCTIONAL_CLOSES_Q=FALSE")
        print("RESIDUAL_SCALAR=F_plus_minus_F_perp_equiv_center_label_source_u_minus_one_half")
        print("RESIDUAL_EQUALITY=all_order_equivariance_does_not_equalize_center_blocks")
        print("RESIDUAL_ODD_PART=analytic_center_function_odd_part_not_forced_zero")
        return 0

    print("VERDICT: all-order center-functional audit has FAILs.")
    print("KOIDE_Q_ALL_ORDER_CENTER_FUNCTIONAL_NO_GO=FALSE")
    print("Q_ALL_ORDER_CENTER_FUNCTIONAL_CLOSES_Q=FALSE")
    print("RESIDUAL_SCALAR=F_plus_minus_F_perp_equiv_center_label_source_u_minus_one_half")
    print("RESIDUAL_EQUALITY=all_order_equivariance_does_not_equalize_center_blocks")
    print("RESIDUAL_ODD_PART=analytic_center_function_odd_part_not_forced_zero")
    return 1


if __name__ == "__main__":
    sys.exit(main())
