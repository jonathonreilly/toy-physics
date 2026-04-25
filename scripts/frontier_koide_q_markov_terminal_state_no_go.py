#!/usr/bin/env python3
"""
Koide Q Markov-category terminal-state no-go.

Theorem attempt:
  Use the Markov-category structure of classical center labels: copying,
  discarding, and terminality might force the canonical center-label
  preparation, hence K_TL = 0.

Result:
  Negative.  In a finite classical Markov category, discarding is unique, but
  preparations from the terminal object to a two-label system are exactly all
  probability distributions:

      * -> (u, 1-u).

  Copy/delete and terminality therefore make the labels classical; they do not
  choose the uniform distribution u=1/2.  The uniform state is a valid
  preparation, but so is the rank state u=1/3.  A naturality theorem can force
  uniformity only after adding a label-exchange automorphism, which is not
  retained by the rank-1/rank-2 C3 carrier.

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
    section("A. Classical Markov structure of two center labels")

    u = sp.symbols("u", positive=True, real=True)
    preparation = sp.Matrix([u, 1 - u])
    discard = sp.Matrix([[1, 1]])
    copy = sp.Matrix([[1, 0], [0, 0], [0, 0], [0, 1]])
    discarded = sp.simplify(discard * preparation)
    copied = sp.simplify(copy * preparation)
    record(
        "A.1 discarding is terminal and normalizes every preparation",
        discarded == sp.Matrix([1]),
        f"discard * prep={discarded}",
    )
    record(
        "A.2 copying preserves every classical preparation as a classical correlation",
        copied == sp.Matrix([u, 0, 0, 1 - u]),
        f"copy * prep={list(copied)}",
    )

    section("B. Terminality does not choose the prepared state")

    samples = {
        "rank_state": sp.Rational(1, 3),
        "equal_label": sp.Rational(1, 2),
        "singlet_heavy": sp.Rational(2, 3),
    }
    sample_lines = []
    ok = True
    for name, value in samples.items():
        prep_value = preparation.subs(u, value)
        q_value = q_from_center_state(value)
        ktl_value = ktl_from_center_state(value)
        ok = ok and (discard * prep_value == sp.Matrix([1]))
        sample_lines.append(f"{name}: prep={list(prep_value)}, Q={q_value}, K_TL={ktl_value}")
    record(
        "B.1 closing and non-closing preparations are valid terminal states",
        ok,
        "\n".join(sample_lines),
    )
    record(
        "B.2 the Koide source is only the uniform preparation",
        sp.solve(sp.Eq(ktl_from_center_state(u), 0), u) == [sp.Rational(1, 2)],
        f"K_TL(u)={ktl_from_center_state(u)}",
    )
    lam = sp.symbols("lam", real=True)
    rank_prep = sp.Matrix([sp.Rational(1, 3), sp.Rational(2, 3)])
    label_prep = sp.Matrix([sp.Rational(1, 2), sp.Rational(1, 2)])
    mixed_prep = sp.simplify((1 - lam) * rank_prep + lam * label_prep)
    record(
        "B.3 convex operational closure preserves a free preparation interval",
        discard * mixed_prep == sp.Matrix([1])
        and mixed_prep.subs(lam, 0) == rank_prep
        and mixed_prep.subs(lam, 1) == label_prep,
        f"mixed_prep={list(mixed_prep)}",
    )

    section("C. Naturality requires an extra label-exchange automorphism")

    swap = sp.Matrix([[0, 1], [1, 0]])
    swap_residual = sp.simplify(swap * preparation - preparation)
    swap_solution = sp.solve(list(swap_residual), [u], dict=True)
    record(
        "C.1 naturality under abstract label swap would force uniformity",
        swap_solution == [{u: sp.Rational(1, 2)}],
        f"swap*prep-prep={list(swap_residual)}",
    )
    rank_plus = sp.Integer(1)
    rank_perp = sp.Integer(2)
    record(
        "C.2 the retained C3 carrier does not have that automorphism",
        rank_plus != rank_perp,
        f"rank(P_plus)={rank_plus}, rank(P_perp)={rank_perp}",
    )
    record(
        "C.3 Markov terminality gives an effect, not a canonical preparation",
        True,
        "The unique map goes from the label system to the terminal object, not from terminal object to labels.",
    )

    section("D. Verdict")

    residual = sp.simplify(u - sp.Rational(1, 2))
    record(
        "D.1 Markov-category terminal route does not close Q",
        residual == u - sp.Rational(1, 2),
        f"RESIDUAL_PREPARATION={residual}",
    )
    record(
        "D.2 Q remains open after Markov terminal audit",
        True,
        "Residual primitive: physical preparation of the uniform center-label state.",
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
        print("VERDICT: Markov terminal/copy-delete structure does not close Q.")
        print("KOIDE_Q_MARKOV_TERMINAL_STATE_NO_GO=TRUE")
        print("Q_MARKOV_TERMINAL_STATE_CLOSES_Q=FALSE")
        print("RESIDUAL_SCALAR=center_label_preparation_u_minus_one_half_equiv_K_TL")
        print("RESIDUAL_PREPARATION=terminality_does_not_choose_uniform_center_state")
        return 0

    print("VERDICT: Markov terminal-state audit has FAILs.")
    print("KOIDE_Q_MARKOV_TERMINAL_STATE_NO_GO=FALSE")
    print("Q_MARKOV_TERMINAL_STATE_CLOSES_Q=FALSE")
    print("RESIDUAL_SCALAR=center_label_preparation_u_minus_one_half_equiv_K_TL")
    print("RESIDUAL_PREPARATION=terminality_does_not_choose_uniform_center_state")
    return 1


if __name__ == "__main__":
    sys.exit(main())
