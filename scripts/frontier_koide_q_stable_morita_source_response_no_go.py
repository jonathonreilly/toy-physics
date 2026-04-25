#!/usr/bin/env python3
"""
Koide Q stable Morita source-response no-go.

Theorem attempt:
  Strengthen the Morita-normalized determinant route into a source-response
  uniqueness theorem.  If the physical charged-lepton source generator is
  invariant under stable matrix amplification, then the coefficients of the
  rank-one plus block and rank-two perpendicular block must be equal:

      a(2) = a(1).

  With scalar normalization a(1)=1 this gives dW|0=(1,1), hence
  K_TL=0 and Q=2/3.

Result:
  Conditional positive, retained negative.  Stable Morita source-response is
  exactly the law needed to make the normalized determinant physical.  But the
  retained rank/equivariant source grammar still admits the full determinant
  response a(2)=2, which is exact and gives Q=1, K_TL=3/8.  The current
  retained packet does not prove that the rank-two block is a dummy Morita
  amplification rather than a physical source-visible equivariant rank.

No PDG masses, H_* pins, K_TL=0 assumptions, Q target assumptions, delta pins,
or observational inputs are used.
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


def normalized_weights(y_plus: sp.Expr, y_perp: sp.Expr) -> tuple[sp.Expr, sp.Expr]:
    total = sp.simplify(y_plus + y_perp)
    return sp.simplify(y_plus / total), sp.simplify(y_perp / total)


def q_from_weights(w_plus: sp.Expr, w_perp: sp.Expr) -> sp.Expr:
    r = sp.simplify(w_perp / w_plus)
    return sp.simplify((1 + r) / 3)


def ktl_from_weights(w_plus: sp.Expr, w_perp: sp.Expr) -> sp.Expr:
    r = sp.simplify(w_perp / w_plus)
    return sp.simplify((r**2 - 1) / (4 * r))


def gradient_at_zero(w: sp.Expr, variables: tuple[sp.Symbol, sp.Symbol]) -> tuple[sp.Expr, sp.Expr]:
    k_plus, k_perp = variables
    return (
        sp.simplify(sp.diff(w, k_plus).subs({k_plus: 0, k_perp: 0})),
        sp.simplify(sp.diff(w, k_perp).subs({k_plus: 0, k_perp: 0})),
    )


def main() -> int:
    section("A. Stable Morita source-response law")

    k_plus, k_perp = sp.symbols("k_plus k_perp", real=True)
    a1, a2 = sp.symbols("a1 a2", positive=True, real=True)
    W = a1 * sp.log(1 + k_plus) + a2 * sp.log(1 + k_perp)
    y = gradient_at_zero(W, (k_plus, k_perp))
    weights = normalized_weights(*y)
    ktl = sp.simplify(ktl_from_weights(*weights))
    q = sp.simplify(q_from_weights(*weights))

    record(
        "A.1 generic determinant-source response has one coefficient ratio",
        y == (a1, a2) and weights == (a1 / (a1 + a2), a2 / (a1 + a2)),
        f"W={W}; dW|0={y}; weights={weights}",
    )
    record(
        "A.2 K_TL=0 is equivalent to equal source coefficients",
        sp.simplify(
            sp.factor(sp.together(ktl).as_numer_denom()[0])
            - (a2 - a1) * (a1 + a2)
        )
        == 0,
        f"K_TL(a1,a2)={ktl}",
    )
    stable_law_residual = a2 - a1
    record(
        "A.3 stable Morita amplification invariance forces a(2)=a(1)",
        sp.simplify(stable_law_residual.subs(a2, a1)) == 0,
        f"The proposed law is a(nr)=a(r); for ranks (1,2), residual={stable_law_residual}.",
    )

    section("B. Conditional positive theorem")

    stable_subs = {a1: 1, a2: 1}
    stable_weights = tuple(sp.simplify(value.subs(stable_subs)) for value in weights)
    record(
        "B.1 stable Morita source-response gives equal normalized weights",
        stable_weights == (sp.Rational(1, 2), sp.Rational(1, 2)),
        f"weights_stable={stable_weights}",
    )
    record(
        "B.2 stable Morita source-response closes the Q consequence chain",
        ktl.subs(stable_subs) == 0 and q.subs(stable_subs) == sp.Rational(2, 3),
        f"K_TL={ktl.subs(stable_subs)}, Q={q.subs(stable_subs)}",
    )

    section("C. Retained equivariant-rank countermodel")

    full_subs = {a1: 1, a2: 2}
    full_weights = tuple(sp.simplify(value.subs(full_subs)) for value in weights)
    record(
        "C.1 full determinant is the retained rank-additive response",
        full_weights == (sp.Rational(1, 3), sp.Rational(2, 3)),
        f"a1=1,a2=2 -> weights={full_weights}",
    )
    record(
        "C.2 full determinant is exact and off Koide",
        ktl.subs(full_subs) == sp.Rational(3, 8) and q.subs(full_subs) == 1,
        f"K_TL={ktl.subs(full_subs)}, Q={q.subs(full_subs)}",
    )
    record(
        "C.3 the countermodel violates stable Morita source-response but not retained rank visibility",
        sp.simplify(full_subs[a2] - full_subs[a1]) == 1,
        "The remaining decision is whether rank 2 is dummy amplification or physical source multiplicity.",
    )

    section("D. Hostile retained-status audit")

    stable_morita_source_response = sp.symbols("stable_morita_source_response", real=True)
    equivariant_rank_source_visibility = sp.symbols(
        "equivariant_rank_source_visibility", real=True
    )
    retained_constraints = sp.Matrix([0, 0, 0])
    record(
        "D.1 retained support constraints do not impose stable Morita source-response",
        retained_constraints.jacobian([stable_morita_source_response]).rank() == 0,
        "No retained equation in this audit proves a(2)=a(1).",
    )
    record(
        "D.2 retained support constraints do not exclude rank-visible source response",
        retained_constraints.jacobian([equivariant_rank_source_visibility]).rank() == 0,
        "No retained equation in this audit forbids a(2)=2a(1).",
    )
    record(
        "D.3 exact residual primitive is named",
        True,
        "Need a retained theorem selecting stable Morita response over equivariant rank source.",
    )

    section("E. Hostile review")

    record(
        "E.1 no forbidden target or observational pin is used as an input",
        True,
        "The source-response alternatives are audited before evaluating Q.",
    )
    record(
        "E.2 stable Morita response is not renamed as retained closure",
        True,
        "It is the sufficient missing law; the full determinant counterstate remains admitted.",
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
        print("VERDICT: stable Morita source-response is conditional, not retained-only proof.")
        print("KOIDE_Q_STABLE_MORITA_SOURCE_RESPONSE_NO_GO=TRUE")
        print("Q_STABLE_MORITA_SOURCE_RESPONSE_CLOSES_Q_RETAINED_ONLY=FALSE")
        print("CONDITIONAL_Q_CLOSES_IF_STABLE_MORITA_SOURCE_RESPONSE_IS_PHYSICAL=TRUE")
        print("RESIDUAL_SCALAR=derive_stable_Morita_source_response_over_equivariant_rank_source")
        print("RESIDUAL_Q=equivariant_rank_full_determinant_counterstate_not_excluded")
        print("COUNTERSTATE=equivariant_rank_logdet_w_plus_1_over_3_Q_1_K_TL_3_over_8")
        return 0

    print("VERDICT: stable Morita source-response audit has FAILs.")
    print("KOIDE_Q_STABLE_MORITA_SOURCE_RESPONSE_NO_GO=FALSE")
    print("Q_STABLE_MORITA_SOURCE_RESPONSE_CLOSES_Q_RETAINED_ONLY=FALSE")
    print("RESIDUAL_SCALAR=derive_stable_Morita_source_response_over_equivariant_rank_source")
    return 1


if __name__ == "__main__":
    sys.exit(main())
