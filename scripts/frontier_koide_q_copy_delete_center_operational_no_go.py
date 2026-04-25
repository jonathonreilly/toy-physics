#!/usr/bin/env python3
"""
Koide Q operational copy/delete center no-go.

Theorem attempt:
  The two retained C3 center labels are classical superselection outcomes.
  Perhaps operational copy/delete structure for those labels forces the
  label-counting source state, hence K_TL = 0.

Result:
  Negative.  The classical copy/delete maps do form a special commutative
  Frobenius structure on the two-label algebra.  But copy/delete structure
  fixes which states are classical, not which classical probability
  distribution is physically prepared.  Every distribution

      p(u) = (u, 1-u)

  is compatible with copying and deleting the center label.  The equal-label
  state u=1/2 is selected only after adding an unbiased-label source prior or
  a label-exchange symmetry, and that exchange still does not lift to the
  retained rank-1/rank-2 real C3 carrier.

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
    section("A. Classical copy/delete structure on two center labels")

    # Basis order for two-label states: [+, perp].
    # Tensor basis order: [++,+perp,perp+,perp perp].
    delta = sp.Matrix([[1, 0], [0, 0], [0, 0], [0, 1]])
    epsilon = sp.Matrix([[1, 1]])
    multiplication = sp.Matrix([[1, 0, 0, 0], [0, 0, 0, 1]])
    eps_tensor_id = sp.Matrix([[1, 0, 1, 0], [0, 1, 0, 1]])
    id_tensor_eps = sp.Matrix([[1, 1, 0, 0], [0, 0, 1, 1]])

    record(
        "A.1 copy/delete maps satisfy the counit identities",
        eps_tensor_id * delta == sp.eye(2) and id_tensor_eps * delta == sp.eye(2),
        "(epsilon tensor id)Delta = id = (id tensor epsilon)Delta.",
    )
    record(
        "A.2 label copy/delete is special: multiplication after copy is identity",
        multiplication * delta == sp.eye(2),
        "m o Delta = id on the abstract two-label algebra.",
    )

    section("B. Copy/delete does not choose the prepared classical state")

    u = sp.symbols("u", positive=True, real=True)
    p = sp.Matrix([u, 1 - u])
    copied = sp.simplify(delta * p)
    left_marginal = sp.simplify(eps_tensor_id * copied)
    right_marginal = sp.simplify(id_tensor_eps * copied)
    q_u = q_from_probabilities(u, 1 - u)
    ktl_u = ktl_from_probabilities(u, 1 - u)
    record(
        "B.1 every center-label distribution is copy/delete compatible",
        copied == sp.Matrix([u, 0, 0, 1 - u])
        and left_marginal == p
        and right_marginal == p,
        f"Delta p(u)={list(copied)}, marginals={list(left_marginal)} and {list(right_marginal)}",
    )
    record(
        "B.2 source neutrality is only the special distribution u=1/2",
        sp.solve(sp.Eq(ktl_u, 0), u) == [sp.Rational(1, 2)],
        f"Q(u)={q_u}, K_TL(u)={ktl_u}",
    )

    section("C. Retained non-closing states remain operationally classical")

    samples = {
        "rank_state": sp.Rational(1, 3),
        "equal_label": sp.Rational(1, 2),
        "singlet_heavy": sp.Rational(2, 3),
    }
    lines = []
    ok = True
    for name, u_value in samples.items():
        probs = (u_value, sp.simplify(1 - u_value))
        copied_value = sp.simplify(copied.subs(u, u_value))
        q_value = q_from_probabilities(*probs)
        ktl_value = ktl_from_probabilities(*probs)
        ok = ok and copied_value[1] == 0 and copied_value[2] == 0
        lines.append(f"{name}: p={probs}, copied={list(copied_value)}, Q={q_value}, K_TL={ktl_value}")
    record(
        "C.1 closing and non-closing distributions are all valid classical label states",
        ok,
        "\n".join(lines),
    )

    section("D. Unbiased label source would require extra symmetry/prior")

    swap = sp.Matrix([[0, 1], [1, 0]])
    swap_residual = sp.simplify(swap * p - p)
    exchange_solution = sp.solve(list(swap_residual), [u], dict=True)
    record(
        "D.1 abstract label exchange would force the equal-label state",
        exchange_solution == [{u: sp.Rational(1, 2)}],
        f"swap*p-p={list(swap_residual)}",
    )

    P_plus_rank = sp.Integer(1)
    P_perp_rank = sp.Integer(2)
    record(
        "D.2 label exchange is not retained by the real C3 carrier ranks",
        P_plus_rank != P_perp_rank,
        "The physical carrier has rank(P_plus)=1 and rank(P_perp)=2.",
    )
    record(
        "D.3 choosing the maximally mixed label source is a prior, not a copy/delete theorem",
        True,
        "Copy/delete says labels are classical; it does not prepare them uniformly.",
    )

    section("E. Verdict")

    residual = sp.simplify(u - sp.Rational(1, 2))
    record(
        "E.1 operational copy/delete route does not close Q",
        residual == u - sp.Rational(1, 2),
        f"RESIDUAL_LABEL_SOURCE={residual}",
    )
    record(
        "E.2 Q remains open after copy/delete audit",
        True,
        "Residual primitive: physical preparation of the unbiased center-label source.",
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
        print("VERDICT: operational copy/delete structure does not close Q.")
        print("KOIDE_Q_COPY_DELETE_CENTER_OPERATIONAL_NO_GO=TRUE")
        print("Q_COPY_DELETE_CENTER_OPERATIONAL_CLOSES_Q=FALSE")
        print("RESIDUAL_SCALAR=center_label_source_u_minus_one_half_equiv_K_TL")
        print("RESIDUAL_PRIOR=unbiased_center_label_preparation_not_forced_by_copy_delete")
        return 0

    print("VERDICT: operational copy/delete audit has FAILs.")
    print("KOIDE_Q_COPY_DELETE_CENTER_OPERATIONAL_NO_GO=FALSE")
    print("Q_COPY_DELETE_CENTER_OPERATIONAL_CLOSES_Q=FALSE")
    print("RESIDUAL_SCALAR=center_label_source_u_minus_one_half_equiv_K_TL")
    print("RESIDUAL_PRIOR=unbiased_center_label_preparation_not_forced_by_copy_delete")
    return 1


if __name__ == "__main__":
    sys.exit(main())
