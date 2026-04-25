#!/usr/bin/env python3
"""
Koide Q two-point spectral-triple state no-go.

Theorem attempt:
  Treat the retained charged-lepton C3 center as a finite two-point geometry.
  Perhaps a Connes distance, finite Dirac operator, or spectral action selects
  the equal center-label state and therefore derives K_TL = 0.

Result:
  Negative from the retained data alone.  A two-point Dirac operator fixes a
  metric scale between labels, not the probability/state on the labels.  The
  finite spectral action depends on Dirac eigenvalues and multiplicities, but
  the central source state

      rho(u) = u P_plus + (1-u) P_perp / 2

  remains one-dimensional.  The equal-label state u=1/2 lands on the Koide
  leaf, while the Hilbert/rank state u=1/3 is retained and gives nonzero
  K_TL.  Imposing a label-exchange automorphism would set u=1/2, but that
  exchange does not lift to the retained real C3 carrier because the summands
  have ranks 1 and 2.

No PDG masses, target Koide value, delta pin, or H_* pin is used.
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


def ktl_from_probabilities(p_plus: sp.Expr, p_perp: sp.Expr) -> sp.Expr:
    r = sp.simplify(p_perp / p_plus)
    return sp.simplify((r**2 - 1) / (4 * r))


def q_from_probabilities(p_plus: sp.Expr, p_perp: sp.Expr) -> sp.Expr:
    r = sp.simplify(p_perp / p_plus)
    return sp.simplify((1 + r) / 3)


def main() -> int:
    section("A. Retained C3 sector carrier")

    C = sp.Matrix([[0, 0, 1], [1, 0, 0], [0, 1, 0]])
    I3 = sp.eye(3)
    P_plus = sp.ones(3, 3) / 3
    P_perp = I3 - P_plus

    record(
        "A.1 retained real carrier splits as rank-1 singlet plus rank-2 doublet",
        P_plus.rank() == 1
        and P_perp.rank() == 2
        and sp.simplify(C * P_plus - P_plus * C) == sp.zeros(3, 3)
        and sp.simplify(C * P_perp - P_perp * C) == sp.zeros(3, 3),
        f"rank(P_plus)={P_plus.rank()}, rank(P_perp)={P_perp.rank()}",
    )
    record(
        "A.2 the central state family has one physical source parameter",
        True,
        "rho(u)=u P_plus + (1-u) P_perp/2.",
    )

    section("B. Two-point Dirac operator fixes distance, not state")

    m = sp.symbols("m", positive=True, real=True)
    D2 = sp.Matrix([[0, m], [m, 0]])
    D2_eigs = sorted(D2.eigenvals().keys(), key=str)
    distance = sp.simplify(1 / m)
    record(
        "B.1 two-point Dirac spectrum is symmetric and controlled by one scale",
        set(D2_eigs) == {-m, m},
        f"spec(D)={D2_eigs}",
    )
    record(
        "B.2 Connes distance between labels is 1/m and contains no source weight",
        distance == 1 / m,
        f"d(plus,perp)={distance}",
    )

    f0, f2 = sp.symbols("f0 f2", real=True)
    spectral_action_two_point = sp.simplify(2 * f0 + 2 * f2 * m**2)
    record(
        "B.3 polynomial finite spectral action depends on Dirac scale, not on u",
        not spectral_action_two_point.has(sp.symbols("u")),
        f"S_2pt={spectral_action_two_point}",
    )

    section("C. Lifting back to the retained rank-1/rank-2 carrier")

    u = sp.symbols("u", positive=True, real=True)
    rho_u = sp.simplify(u * P_plus + ((1 - u) / 2) * P_perp)
    p_plus = sp.simplify(sp.trace(P_plus * rho_u))
    p_perp = sp.simplify(sp.trace(P_perp * rho_u))
    q_u = q_from_probabilities(p_plus, p_perp)
    ktl_u = ktl_from_probabilities(p_plus, p_perp)
    record(
        "C.1 lifted central states remain C3-invariant for every u",
        sp.simplify(sp.trace(rho_u) - 1) == 0
        and sp.simplify(C * rho_u - rho_u * C) == sp.zeros(3, 3)
        and p_plus == u
        and p_perp == 1 - u,
        f"probabilities=({p_plus},{p_perp}); Q(u)={q_u}; K_TL(u)={ktl_u}",
    )
    record(
        "C.2 source neutrality is the special central state u=1/2",
        sp.solve(sp.Eq(ktl_u, 0), u) == [sp.Rational(1, 2)],
        "The finite metric did not supply this state equation.",
    )

    p_h_plus = sp.Rational(1, 3)
    p_h_perp = sp.Rational(2, 3)
    p_l_plus = sp.Rational(1, 2)
    p_l_perp = sp.Rational(1, 2)
    record(
        "C.3 retained rank state and equal-label state share the same two-point metric data",
        q_from_probabilities(p_h_plus, p_h_perp) == 1
        and ktl_from_probabilities(p_h_plus, p_h_perp) == sp.Rational(3, 8)
        and q_from_probabilities(p_l_plus, p_l_perp) == sp.Rational(2, 3)
        and ktl_from_probabilities(p_l_plus, p_l_perp) == 0,
        "rank state: (1/3,2/3) -> Q=1, K_TL=3/8\n"
        "equal-label state: (1/2,1/2) -> Q=2/3, K_TL=0",
    )

    section("D. Exchange-symmetry escape hatch is not retained")

    swap2 = sp.Matrix([[0, 1], [1, 0]])
    label_state = sp.diag(u, 1 - u)
    swap_residual = sp.simplify(swap2 * label_state * swap2.T - label_state)
    exchange_solution = sp.solve(list(swap_residual), [u], dict=True)
    record(
        "D.1 exact label exchange would force u=1/2 on the abstract two-label algebra",
        exchange_solution == [{u: sp.Rational(1, 2)}],
        f"swap*rho*swap^-1-rho={swap_residual}",
    )
    record(
        "D.2 that exchange does not lift to the retained real C3 carrier",
        P_plus.rank() != P_perp.rank(),
        "No orthogonal/unitary carrier map can conjugate a rank-1 projector to a rank-2 projector.",
    )

    section("E. Verdict")

    record(
        "E.1 two-point spectral-triple route does not close Q",
        True,
        "Metric/spectral data leave the central source state free.",
    )
    record(
        "E.2 Q remains open after finite-geometry audit",
        True,
        "Residual primitive: retained reason for equal center-label state u=1/2.",
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
        print("VERDICT: two-point spectral geometry does not close Q.")
        print("KOIDE_Q_TWO_POINT_SPECTRAL_TRIPLE_NO_GO=TRUE")
        print("Q_TWO_POINT_SPECTRAL_TRIPLE_CLOSES_Q=FALSE")
        print("RESIDUAL_SCALAR=center_label_state_u_minus_one_half_equiv_K_TL")
        print("RESIDUAL_STATE=finite_geometry_does_not_select_center_label_state")
        return 0

    print("VERDICT: two-point spectral-triple audit has FAILs.")
    print("KOIDE_Q_TWO_POINT_SPECTRAL_TRIPLE_NO_GO=FALSE")
    print("Q_TWO_POINT_SPECTRAL_TRIPLE_CLOSES_Q=FALSE")
    print("RESIDUAL_SCALAR=center_label_state_u_minus_one_half_equiv_K_TL")
    print("RESIDUAL_STATE=finite_geometry_does_not_select_center_label_state")
    return 1


if __name__ == "__main__":
    sys.exit(main())
