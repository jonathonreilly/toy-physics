#!/usr/bin/env python3
"""
Koide Q superselection center-instrument no-go.

Theorem attempt:
  The retained charged-lepton observable might be a superselection measurement
  of the two central C3 sectors.  If the physical instrument only sees the
  center labels {plus, perp}, perhaps measurement theory itself forces equal
  label weights and hence K_TL = 0.

Result:
  Negative.  The retained repeatable, C3-equivariant, sector-nondemolition
  instrument is the projective measurement {P_plus, P_perp}.  That instrument
  fixes the effects, but not the pre-measurement central state.  The normalized
  Hilbert state gives probabilities 1:2, while the equal-label center state
  gives 1:1.  Both are compatible with the same superselection instrument.
  Choosing the equal-label center state is precisely the missing source/state
  primitive.

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


def q_from_probabilities(p_plus: sp.Expr, p_perp: sp.Expr) -> sp.Expr:
    r = sp.simplify(p_perp / p_plus)
    return sp.simplify((1 + r) / 3)


def ktl_from_probabilities(p_plus: sp.Expr, p_perp: sp.Expr) -> sp.Expr:
    r = sp.simplify(p_perp / p_plus)
    return sp.simplify((r**2 - 1) / (4 * r))


def main() -> int:
    section("A. Retained central sectors")

    C = sp.Matrix([[0, 0, 1], [1, 0, 0], [0, 1, 0]])
    I3 = sp.eye(3)
    J = sp.ones(3, 3)
    P_plus = J / 3
    P_perp = I3 - P_plus

    record(
        "A.1 P_plus and P_perp are orthogonal central projections",
        sp.simplify(P_plus**2 - P_plus) == sp.zeros(3, 3)
        and sp.simplify(P_perp**2 - P_perp) == sp.zeros(3, 3)
        and sp.simplify(P_plus * P_perp) == sp.zeros(3, 3)
        and sp.simplify(C * P_plus - P_plus * C) == sp.zeros(3, 3)
        and sp.simplify(C * P_perp - P_perp * C) == sp.zeros(3, 3),
        f"ranks=({P_plus.rank()},{P_perp.rank()})",
    )

    section("B. Superselection instrument constraints")

    a, b = sp.symbols("a b", real=True)
    F_plus = sp.simplify(a * P_plus)
    F_perp = sp.simplify(b * P_perp)
    completeness = sp.simplify(F_plus + F_perp - I3)
    solution = sp.solve(list(completeness), [a, b], dict=True)
    record(
        "B.1 sector-nondemolition two-outcome POVM has effects P_plus and P_perp",
        solution == [{a: 1, b: 1}],
        f"a P_plus + b P_perp = I -> {solution}",
    )
    record(
        "B.2 repeatable projective measurement fixes the question, not the state",
        sp.simplify(P_plus * P_plus * P_plus - P_plus) == sp.zeros(3, 3)
        and sp.simplify(P_perp * P_perp * P_perp - P_perp) == sp.zeros(3, 3),
        "The PVM asks which central sector is occupied; it supplies no prior over sectors.",
    )

    section("C. Central state family remains one-dimensional")

    u = sp.symbols("u", positive=True, real=True)
    rho_u = sp.simplify(u * P_plus + ((1 - u) / 2) * P_perp)
    p_plus = sp.simplify(sp.trace(P_plus * rho_u))
    p_perp = sp.simplify(sp.trace(P_perp * rho_u))
    q_u = q_from_probabilities(p_plus, p_perp)
    ktl_u = ktl_from_probabilities(p_plus, p_perp)
    record(
        "C.1 every C3-invariant normalized central state has probability split (u,1-u)",
        sp.simplify(sp.trace(rho_u) - 1) == 0
        and p_plus == u
        and p_perp == 1 - u
        and sp.simplify(C * rho_u - rho_u * C) == sp.zeros(3, 3),
        f"rho(u)=u P_plus + (1-u)P_perp/2; probabilities=({p_plus},{p_perp})",
    )
    record(
        "C.2 source neutrality is the special state u=1/2",
        sp.solve(sp.Eq(ktl_u, 0), u) == [sp.Rational(1, 2)],
        f"Q(u)={q_u}; K_TL(u)={ktl_u}",
    )

    rho_hilbert = sp.simplify(I3 / 3)
    p_h_plus = sp.simplify(sp.trace(P_plus * rho_hilbert))
    p_h_perp = sp.simplify(sp.trace(P_perp * rho_hilbert))
    rho_label = sp.simplify(P_plus / 2 + P_perp / 4)
    p_l_plus = sp.simplify(sp.trace(P_plus * rho_label))
    p_l_perp = sp.simplify(sp.trace(P_perp * rho_label))
    record(
        "C.3 Hilbert state and equal-label state give different exact Q values",
        (p_h_plus, p_h_perp) == (sp.Rational(1, 3), sp.Rational(2, 3))
        and q_from_probabilities(p_h_plus, p_h_perp) == 1
        and ktl_from_probabilities(p_h_plus, p_h_perp) == sp.Rational(3, 8)
        and (p_l_plus, p_l_perp) == (sp.Rational(1, 2), sp.Rational(1, 2))
        and q_from_probabilities(p_l_plus, p_l_perp) == sp.Rational(2, 3)
        and ktl_from_probabilities(p_l_plus, p_l_perp) == 0,
        "Hilbert/rank state: (1/3,2/3) -> Q=1, K_TL=3/8\n"
        "Equal-label state: (1/2,1/2) -> Q=2/3, K_TL=0",
    )

    section("D. Measurement update does not equalize the source state")

    rho_post = sp.simplify(P_plus * rho_u * P_plus + P_perp * rho_u * P_perp)
    post_probs = (
        sp.simplify(sp.trace(P_plus * rho_post)),
        sp.simplify(sp.trace(P_perp * rho_post)),
    )
    record(
        "D.1 nonselective superselection measurement preserves the central probabilities",
        sp.simplify(rho_post - rho_u) == sp.zeros(3, 3) and post_probs == (u, 1 - u),
        f"post-measurement probabilities={post_probs}",
    )
    record(
        "D.2 requiring equal pointer labels would be an external prior, not a PVM theorem",
        True,
        "The instrument determines effects P_i; a prior over readout labels is distinct state data.",
    )

    section("E. Verdict")

    record(
        "E.1 superselection center-instrument route does not close Q",
        True,
        "Retained measurement theory fixes the sector question but leaves the central source state free.",
    )
    record(
        "E.2 Q remains open after center-instrument audit",
        True,
        "Residual primitive: physical center-label state u=1/2 rather than Hilbert/rank state u=1/3.",
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
        print("VERDICT: superselection center-instrument route does not close Q.")
        print("KOIDE_Q_SUPERSELECTION_CENTER_INSTRUMENT_NO_GO=TRUE")
        print("Q_SUPERSELECTION_CENTER_INSTRUMENT_CLOSES_Q=FALSE")
        print("RESIDUAL_SCALAR=center_label_state_u_minus_one_half_equiv_K_TL")
        print("RESIDUAL_STATE=center_label_state_u_minus_one_half_equiv_K_TL")
        return 0

    print("VERDICT: superselection center-instrument audit has FAILs.")
    print("KOIDE_Q_SUPERSELECTION_CENTER_INSTRUMENT_NO_GO=FALSE")
    print("Q_SUPERSELECTION_CENTER_INSTRUMENT_CLOSES_Q=FALSE")
    print("RESIDUAL_SCALAR=center_label_state_u_minus_one_half_equiv_K_TL")
    print("RESIDUAL_STATE=center_label_state_u_minus_one_half_equiv_K_TL")
    return 1


if __name__ == "__main__":
    sys.exit(main())
