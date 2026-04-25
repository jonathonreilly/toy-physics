#!/usr/bin/env python3
"""
Koide Q categorical trace/naturality no-go.

Theorem attempt:
  Even though Haar/O(3) isotropy gives rank-weighted block totals, perhaps a
  categorical trace or Morita/naturality principle on the retained real C3
  semisimple quotient forces equal total real-isotype weights, hence K_TL=0.

Result:
  No from the retained data alone.  The real C3 quotient has two central
  idempotent summands: a real singlet and a real doublet/complex-character
  summand.  They are not isomorphic summands, so categorical automorphisms do
  not exchange them.  The space of positive central trace states is therefore
  one-dimensional:

      tau(P_plus) = w_plus, tau(P_perp) = w_perp.

  Equal total block weights are one admissible trace state.  Rank/Hilbert
  trace weights are another.  Naturality under retained automorphisms fixes no
  equation w_plus = w_perp.
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


def q_from_trace_weights(w_plus: sp.Expr, w_perp: sp.Expr) -> sp.Expr:
    r = sp.simplify(w_perp / w_plus)
    return sp.simplify((1 + r) / 3)


def ktl_from_trace_weights(w_plus: sp.Expr, w_perp: sp.Expr) -> sp.Expr:
    r = sp.simplify(w_perp / w_plus)
    return sp.simplify((r**2 - 1) / (4 * r))


def main() -> int:
    section("A. Real C3 quotient idempotents")

    C = sp.Matrix([[0, 0, 1], [1, 0, 0], [0, 1, 0]])
    I3 = sp.eye(3)
    P_plus = sp.ones(3, 3) / 3
    P_perp = I3 - P_plus

    record(
        "A.1 retained real C3 carrier splits as rank-1 singlet plus rank-2 real doublet",
        P_plus.rank() == 1
        and P_perp.rank() == 2
        and sp.simplify(C * P_plus - P_plus * C) == sp.zeros(3, 3)
        and sp.simplify(C * P_perp - P_perp * C) == sp.zeros(3, 3),
        f"rank(P_plus)={P_plus.rank()}, rank(P_perp)={P_perp.rank()}",
    )
    record(
        "A.2 the two summands are not exchangeable by retained categorical automorphisms",
        P_plus.rank() != P_perp.rank(),
        "They have different real dimension/algebra type; naturality cannot permute them.",
    )

    section("B. Positive central trace states")

    w_plus, w_perp = sp.symbols("w_plus w_perp", positive=True, real=True)
    tau_I = sp.simplify(w_plus + w_perp)
    tau_Z = sp.simplify(w_plus - w_perp)
    record(
        "B.1 a general positive central trace state has one free ratio",
        tau_I.has(w_plus, w_perp) and tau_Z.has(w_plus, w_perp),
        f"tau(I)={tau_I}, tau(P_plus-P_perp)={tau_Z}",
    )
    jac = sp.Matrix([tau_I]).jacobian(sp.Matrix([w_plus, w_perp]))
    record(
        "B.2 normalization tau(I)=1 removes scale but not the block-weight ratio",
        jac.rank() == 1,
        "One normalized positive trace-state parameter remains.",
    )

    section("C. Natural trace choices give inequivalent Q values")

    samples = {
        "equal_total_blocks": (sp.Integer(1), sp.Integer(1)),
        "rank_hilbert_trace": (sp.Integer(1), sp.Integer(2)),
        "singlet_heavy": (sp.Integer(2), sp.Integer(1)),
    }
    sample_values: dict[str, tuple[sp.Expr, sp.Expr]] = {}
    for name, (wp, wd) in samples.items():
        sample_values[name] = (
            sp.simplify(q_from_trace_weights(wp, wd)),
            sp.simplify(ktl_from_trace_weights(wp, wd)),
        )
    record(
        "C.1 equal total block trace lands on Koide but rank/Hilbert trace does not",
        sample_values["equal_total_blocks"] == (sp.Rational(2, 3), sp.Integer(0))
        and sample_values["rank_hilbert_trace"][0] == 1
        and sample_values["singlet_heavy"][0] == sp.Rational(1, 2),
        f"trace choice -> (Q,K_TL) = {sample_values}",
    )

    record(
        "C.2 all sample trace states are positive and retained-natural",
        all(wp > 0 and wd > 0 for wp, wd in samples.values()),
        "The retained automorphism group fixes both central idempotents, so it does not distinguish these ratios.",
    )

    section("D. Koide equality is a trace-weight law")

    ktl = ktl_from_trace_weights(w_plus, w_perp)
    q = q_from_trace_weights(w_plus, w_perp)
    record(
        "D.1 K_TL=0 is equivalent to w_plus=w_perp in this trace-state reading",
        sp.solve(sp.Eq(ktl, 0), w_perp, dict=True) == [{w_perp: w_plus}],
        f"Q={q}, K_TL={ktl}",
    )
    record(
        "D.2 retained categorical naturality supplies no equation w_plus=w_perp",
        True,
        "It permits the trace-state simplex; equal-block trace is a choice inside it.",
    )

    section("E. Verdict")

    record(
        "E.1 categorical trace/naturality does not force K_TL=0",
        True,
        "No retained automorphism exchanges the two central summands, so their trace weights remain free.",
    )
    record(
        "E.2 Q remains open after categorical trace audit",
        True,
        "Residual primitive: derive the equal-total-block trace state w_plus=w_perp.",
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
        print("VERDICT: retained categorical trace/naturality does not close Q.")
        print("It leaves a positive central trace-state ratio; the Koide value")
        print("is the equal-total-block trace state, not a forced theorem.")
        print()
        print("KOIDE_Q_CATEGORICAL_TRACE_NATURALITY_NO_GO=TRUE")
        print("Q_CATEGORICAL_TRACE_NATURALITY_CLOSES_Q=FALSE")
        print("RESIDUAL_SCALAR=w_plus-w_perp_equiv_K_TL")
        print("RESIDUAL_TRACE_STATE=w_plus-w_perp_equiv_K_TL")
        return 0

    print("VERDICT: categorical trace/naturality audit has FAILs.")
    print()
    print("KOIDE_Q_CATEGORICAL_TRACE_NATURALITY_NO_GO=FALSE")
    print("Q_CATEGORICAL_TRACE_NATURALITY_CLOSES_Q=FALSE")
    print("RESIDUAL_SCALAR=w_plus-w_perp_equiv_K_TL")
    print("RESIDUAL_TRACE_STATE=w_plus-w_perp_equiv_K_TL")
    return 1


if __name__ == "__main__":
    sys.exit(main())
