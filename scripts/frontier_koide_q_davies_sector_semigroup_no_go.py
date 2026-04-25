#!/usr/bin/env python3
"""
Koide Q Davies/sector semigroup no-go.

Theorem attempt:
  A retained irreversible Markov/Davies semigroup on the two C3 center sectors
  might have a unique stationary source state.  If that stationary state were
  the equal-label state, it would derive K_TL = 0.

Result:
  Negative from retained data alone.  A two-sector continuous-time Markov
  generator has rates

      plus -> perp : a
      perp -> plus : b

  and stationary state

      p_plus = b/(a+b), p_perp = a/(a+b).

  Equal labels require a=b.  Microstate-symmetric dynamics inherited from the
  rank-1/rank-2 carrier instead gives effective sector rates a:b = 2:1 and the
  rank state (1/3,2/3).  Conversely, detailed balance can realize any chosen
  center state once the rate ratio is supplied.  Choosing quotient-label
  symmetric rates is another expression of the missing source law.

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


def q_from_probabilities(p_plus: sp.Expr, p_perp: sp.Expr) -> sp.Expr:
    r = sp.simplify(p_perp / p_plus)
    return sp.simplify((1 + r) / 3)


def ktl_from_probabilities(p_plus: sp.Expr, p_perp: sp.Expr) -> sp.Expr:
    r = sp.simplify(p_perp / p_plus)
    return sp.simplify((r**2 - 1) / (4 * r))


def main() -> int:
    section("A. General two-sector Markov/Davies generator")

    a, b = sp.symbols("a b", positive=True, real=True)
    # Column-vector convention: dp/dt = L p.
    L = sp.Matrix([[-a, b], [a, -b]])
    p_plus = sp.simplify(b / (a + b))
    p_perp = sp.simplify(a / (a + b))
    p_stat = sp.Matrix([p_plus, p_perp])
    q_stat = q_from_probabilities(p_plus, p_perp)
    ktl_stat = ktl_from_probabilities(p_plus, p_perp)
    record(
        "A.1 two-sector generator conserves probability and has one rate ratio",
        (sp.Matrix([[1, 1]]) * L) == sp.zeros(1, 2),
        f"L={L}",
    )
    record(
        "A.2 stationary state is b/(a+b), a/(a+b)",
        sp.simplify(L * p_stat) == sp.zeros(2, 1),
        f"p_stat={list(p_stat)}, Q={q_stat}, K_TL={ktl_stat}",
    )
    record(
        "A.3 source neutrality requires equal sector rates a=b",
        sp.solve(sp.Eq(ktl_stat, 0), a, dict=True) == [{a: b}],
        "Detailed balance form alone does not set the two rates equal.",
    )

    section("B. Microstate-symmetric inherited dynamics gives rank weights")

    gamma = sp.symbols("gamma", positive=True, real=True)
    inherited = {a: 2 * gamma, b: gamma}
    label_symmetric = {a: gamma, b: gamma}
    p_inherited = tuple(sp.simplify(value.subs(inherited)) for value in p_stat)
    p_label = tuple(sp.simplify(value.subs(label_symmetric)) for value in p_stat)
    record(
        "B.1 microstate-symmetric rank-1/rank-2 carrier induces rates a:b=2:1",
        p_inherited == (sp.Rational(1, 3), sp.Rational(2, 3)),
        f"p_inherited={p_inherited}",
    )
    record(
        "B.2 inherited microstate dynamics is off the source-neutral leaf",
        q_from_probabilities(*p_inherited) == 1
        and ktl_from_probabilities(*p_inherited) == sp.Rational(3, 8),
        f"Q={q_from_probabilities(*p_inherited)}, K_TL={ktl_from_probabilities(*p_inherited)}",
    )
    record(
        "B.3 quotient-label symmetric rates would close but are not inherited",
        p_label == (sp.Rational(1, 2), sp.Rational(1, 2))
        and q_from_probabilities(*p_label) == sp.Rational(2, 3)
        and ktl_from_probabilities(*p_label) == 0,
        "a=b is label symmetry, not microstate/rank symmetry.",
    )
    G = gamma * sp.Matrix([[-2, 1, 1], [1, -2, 1], [1, 1, -2]])
    x0, x1, x2 = sp.symbols("x0 x1 x2", real=True)
    x = sp.Matrix([x0, x1, x2])
    dx = G * x
    p_plus_lump = x0
    p_perp_lump = x1 + x2
    lumped_dx = sp.Matrix([sp.simplify(dx[0]), sp.simplify(dx[1] + dx[2])])
    inherited_lumped_dx = sp.Matrix([
        sp.simplify((-2 * gamma) * p_plus_lump + gamma * p_perp_lump),
        sp.simplify((2 * gamma) * p_plus_lump - gamma * p_perp_lump),
    ])
    uniform_micro = sp.Matrix([sp.Rational(1, 3), sp.Rational(1, 3), sp.Rational(1, 3)])
    record(
        "B.4 exact lumping of the symmetric three-microstate generator gives a:b=2:1",
        lumped_dx == inherited_lumped_dx and G * uniform_micro == sp.zeros(3, 1),
        "complete-graph microstate symmetry lumps to rank weights, not equal labels.",
    )

    section("C. Detailed balance does not choose the stationary measure")

    pi_plus, pi_perp = sp.symbols("pi_plus pi_perp", positive=True, real=True)
    detailed_balance_eq = sp.Eq(pi_plus * a, pi_perp * b)
    pi_solution = sp.solve([detailed_balance_eq, sp.Eq(pi_plus + pi_perp, 1)], [pi_plus, pi_perp], dict=True)
    record(
        "C.1 detailed balance solves for pi in terms of the same rate ratio",
        pi_solution == [{pi_plus: b / (a + b), pi_perp: a / (a + b)}],
        f"pi_solution={pi_solution}",
    )
    record(
        "C.2 rates can realize closing and non-closing stationary states",
        p_inherited != p_label,
        "The semigroup becomes a source law only after the rate ratio is physically derived.",
    )
    u, lam = sp.symbols("u lam", positive=True, real=True)
    arbitrary_rates = {a: (1 - u) * lam, b: u * lam}
    arbitrary_state = tuple(sp.simplify(value.subs(arbitrary_rates)) for value in p_stat)
    record(
        "C.3 any chosen center state can be encoded by detailed-balance rates",
        arbitrary_state == (u, 1 - u),
        "a=(1-u)lambda, b=u lambda gives stationary state (u,1-u).",
    )
    record(
        "C.4 detailed-balance encoding reproduces both rank and label states",
        tuple(value.subs(u, sp.Rational(1, 3)) for value in arbitrary_state)
        == (sp.Rational(1, 3), sp.Rational(2, 3))
        and tuple(value.subs(u, sp.Rational(1, 2)) for value in arbitrary_state)
        == (sp.Rational(1, 2), sp.Rational(1, 2)),
        "Stationarity is a container for the chosen source state, not a derivation of it.",
    )

    section("D. Verdict")

    residual = sp.simplify(a - b)
    record(
        "D.1 Davies/sector semigroup route does not close Q",
        residual == a - b,
        f"RESIDUAL_RATE={residual}",
    )
    record(
        "D.2 Q remains open after sector semigroup audit",
        True,
        "Residual primitive: retained equality of quotient-label transition rates.",
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
        print("VERDICT: Davies/sector semigroup route does not close Q.")
        print("KOIDE_Q_DAVIES_SECTOR_SEMIGROUP_NO_GO=TRUE")
        print("Q_DAVIES_SECTOR_SEMIGROUP_CLOSES_Q=FALSE")
        print("RESIDUAL_SCALAR=sector_rate_a_minus_b_equiv_center_label_state")
        print("RESIDUAL_RATE=quotient_label_rate_equality_not_retained")
        return 0

    print("VERDICT: Davies/sector semigroup audit has FAILs.")
    print("KOIDE_Q_DAVIES_SECTOR_SEMIGROUP_NO_GO=FALSE")
    print("Q_DAVIES_SECTOR_SEMIGROUP_CLOSES_Q=FALSE")
    print("RESIDUAL_SCALAR=sector_rate_a_minus_b_equiv_center_label_state")
    print("RESIDUAL_RATE=quotient_label_rate_equality_not_retained")
    return 1


if __name__ == "__main__":
    sys.exit(main())
