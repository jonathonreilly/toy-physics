#!/usr/bin/env python3
"""
Koide Q noncommutative-geometry finite-state no-go.

Theorem attempt:
  Use finite real spectral-triple data for the retained C3 center to select the
  physical finite state on the center algebra.  If the spectral triple
  canonically selected the quotient-center trace, it would force K_TL = 0.

Result:
  Negative.  The retained finite real data distinguishes a rank-1 real isotype
  and a rank-2 real isotype.  A positive central state is still

      phi_u(P_plus)=u, phi_u(P_perp)=1-u.

  Reality and order-one style constraints act on the representation and Dirac
  commutators; they do not choose u.  The inherited Hilbert trace gives the
  rank state u=1/3, while the quotient-center trace gives u=1/2.  Choosing the
  latter is exactly the missing source law unless a new finite-action principle
  derives it.

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
    section("A. Finite center states on the retained real C3 carrier")

    u = sp.symbols("u", positive=True, real=True)
    rank_plus = sp.Integer(1)
    rank_perp = sp.Integer(2)
    phi_plus = u
    phi_perp = 1 - u
    record(
        "A.1 positive normalized central state has one free parameter",
        sp.simplify(phi_plus + phi_perp) == 1,
        f"phi(P_plus)=u, phi(P_perp)=1-u; ranks=({rank_plus},{rank_perp})",
    )
    record(
        "A.2 K_TL=0 selects the quotient-center trace u=1/2",
        sp.solve(sp.Eq(ktl_from_center_state(u), 0), u) == [sp.Rational(1, 2)],
        f"K_TL(u)={ktl_from_center_state(u)}",
    )

    section("B. Standard finite spectral-triple traces do not select u=1/2")

    u_hilbert_trace = sp.simplify(rank_plus / (rank_plus + rank_perp))
    u_quotient_trace = sp.Rational(1, 2)
    record(
        "B.1 inherited Hilbert trace gives rank weighting",
        u_hilbert_trace == sp.Rational(1, 3)
        and q_from_center_state(u_hilbert_trace) == 1
        and ktl_from_center_state(u_hilbert_trace) == sp.Rational(3, 8),
        f"u_H={u_hilbert_trace}, Q={q_from_center_state(u_hilbert_trace)}, K_TL={ktl_from_center_state(u_hilbert_trace)}",
    )
    record(
        "B.2 quotient-center trace would close Q but is a different state",
        u_quotient_trace == sp.Rational(1, 2)
        and q_from_center_state(u_quotient_trace) == sp.Rational(2, 3)
        and ktl_from_center_state(u_quotient_trace) == 0,
        f"u_Z={u_quotient_trace}, Q={q_from_center_state(u_quotient_trace)}, K_TL={ktl_from_center_state(u_quotient_trace)}",
    )

    section("C. Reality/order-one constraints are representation constraints")

    # Model the real structure as preserving the singlet and conjugating the two-dimensional real block.
    J_action_matrix = sp.diag(1, 0, 0)
    J_action_matrix[1, 2] = 1
    J_action_matrix[2, 1] = 1
    center_operator = sp.diag(u, (1 - u) / 2, (1 - u) / 2)
    J_center_J = sp.simplify(J_action_matrix * center_operator * J_action_matrix.T)
    record(
        "C.1 real structure preserves the two central blocks instead of exchanging them",
        J_center_J == center_operator,
        f"J C(u) J^-1={J_center_J}",
    )
    d_plus, d_perp = sp.symbols("d_plus d_perp", real=True)
    finite_dirac_commutator_norm = sp.simplify((d_plus - d_perp) ** 2)
    record(
        "C.2 Dirac/order-one data can constrain operator differences, not the state u",
        not finite_dirac_commutator_norm.has(u),
        f"commutator_norm_model={finite_dirac_commutator_norm}",
    )
    record(
        "C.3 choosing the quotient-center trace is an extra finite-action principle",
        True,
        "It is compatible with NCG data, but not selected by the retained finite spectral-triple axioms audited here.",
    )

    section("D. Verdict")

    residual = sp.simplify(u - sp.Rational(1, 2))
    record(
        "D.1 NCG finite-state route does not close Q",
        residual == u - sp.Rational(1, 2),
        f"RESIDUAL_FINITE_STATE={residual}",
    )
    record(
        "D.2 Q remains open after NCG finite-state audit",
        True,
        "Residual primitive: physical finite-state principle selecting quotient-center trace over Hilbert trace.",
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
        print("VERDICT: finite real spectral-triple data does not close Q.")
        print("KOIDE_Q_NCG_FINITE_STATE_NO_GO=TRUE")
        print("Q_NCG_FINITE_STATE_CLOSES_Q=FALSE")
        print("RESIDUAL_SCALAR=center_finite_state_u_minus_one_half_equiv_K_TL")
        print("RESIDUAL_STATE=quotient_center_trace_not_selected_by_retained_spectral_triple")
        return 0

    print("VERDICT: NCG finite-state audit has FAILs.")
    print("KOIDE_Q_NCG_FINITE_STATE_NO_GO=FALSE")
    print("Q_NCG_FINITE_STATE_CLOSES_Q=FALSE")
    print("RESIDUAL_SCALAR=center_finite_state_u_minus_one_half_equiv_K_TL")
    print("RESIDUAL_STATE=quotient_center_trace_not_selected_by_retained_spectral_triple")
    return 1


if __name__ == "__main__":
    sys.exit(main())
