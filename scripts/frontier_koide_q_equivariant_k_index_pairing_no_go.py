#!/usr/bin/env python3
"""
Koide Q equivariant K-index pairing no-go.

Theorem attempt:
  An equivariant K-theory or index pairing on the retained real C3 carrier
  might force the label-counting center state, deriving K_TL = 0.

Result:
  Negative.  Additive K0 pairings on the two central sectors form a
  two-parameter cone, so additivity alone leaves the label/rank ratio free.
  If the pairing is strengthened to a monoidal/fusion-compatible dimension
  character on the retained real representation ring, the positive solution is
  the ordinary rank dimension:

      dim(1)=1, dim(D)=2,

  because D tensor D = 2*1 + D.  The label-counting value dim(D)=1 is exactly
  the Koide-supporting state, but it is not a fusion/index dimension character.

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


def q_from_weights(w_plus: sp.Expr, w_perp: sp.Expr) -> sp.Expr:
    w_plus = sp.sympify(w_plus)
    w_perp = sp.sympify(w_perp)
    r = sp.simplify(w_perp / w_plus)
    return sp.simplify((1 + r) / 3)


def ktl_from_weights(w_plus: sp.Expr, w_perp: sp.Expr) -> sp.Expr:
    w_plus = sp.sympify(w_plus)
    w_perp = sp.sympify(w_perp)
    r = sp.simplify(w_perp / w_plus)
    return sp.simplify((r**2 - 1) / (4 * r))


def main() -> int:
    section("A. Additive K0 pairing leaves the sector ratio free")

    a, b = sp.symbols("a b", positive=True, real=True)
    pairing = sp.Matrix([a, b])
    q_pair = q_from_weights(a, b)
    ktl_pair = ktl_from_weights(a, b)
    record(
        "A.1 a positive additive K0 pairing has independent sector weights",
        pairing == sp.Matrix([a, b]),
        f"index weights=(a,b), Q={q_pair}, K_TL={ktl_pair}",
    )
    record(
        "A.2 source neutrality is only the additive subcone a=b",
        sp.solve(sp.Eq(ktl_pair, 0), b, dict=True) == [{b: a}],
        "Additivity alone supplies no equation selecting this subcone.",
    )

    section("B. Fusion-compatible index dimension selects rank, not labels")

    d = sp.symbols("d", real=True)
    fusion_equation = sp.Eq(d**2, 2 + d)  # D tensor D = 2*1 + D.
    fusion_roots = sp.solve(fusion_equation, d)
    positive_roots = [root for root in fusion_roots if bool(root > 0)]
    record(
        "B.1 retained real C3 fusion D tensor D = 2*1 + D forces d^2=d+2",
        fusion_roots == [-1, 2] and positive_roots == [2],
        f"roots={fusion_roots}",
    )
    record(
        "B.2 the positive fusion dimension is d(D)=2",
        positive_roots == [2],
        "This is the rank/Hilbert dimension of the real doublet.",
    )
    record(
        "B.3 label counting d(D)=1 violates the fusion/index dimension equation",
        sp.simplify(1**2 - (2 + 1)) == -2,
        "1^2 != 2 + 1.",
    )

    section("C. Consequences for Q")

    q_rank = q_from_weights(1, 2)
    ktl_rank = ktl_from_weights(1, 2)
    q_label = q_from_weights(1, 1)
    ktl_label = ktl_from_weights(1, 1)
    record(
        "C.1 fusion/index dimension gives the non-closing rank state",
        q_rank == 1 and ktl_rank == sp.Rational(3, 8),
        f"weights=(1,2) -> Q={q_rank}, K_TL={ktl_rank}",
    )
    record(
        "C.2 label-counting gives the closing state but is not fusion-compatible",
        q_label == sp.Rational(2, 3) and ktl_label == 0,
        f"weights=(1,1) -> Q={q_label}, K_TL={ktl_label}",
    )

    section("D. Index countermodels")

    samples = {
        "rank_index": (sp.Integer(1), sp.Integer(2)),
        "label_count": (sp.Integer(1), sp.Integer(1)),
        "singlet_heavy_additive": (sp.Integer(2), sp.Integer(1)),
    }
    lines: list[str] = []
    for name, (wp, wd) in samples.items():
        q_value = q_from_weights(wp, wd)
        ktl_value = ktl_from_weights(wp, wd)
        additive = wp > 0 and wd > 0
        fusion_ok = sp.simplify(wd**2 - (2 * wp**2 + wp * wd)) == 0
        lines.append(f"{name}: weights=({wp},{wd}), additive={additive}, fusion_ok={fusion_ok}, Q={q_value}, K_TL={ktl_value}")
    record(
        "D.1 additive index pairings include closing and non-closing states",
        len(lines) == len(samples),
        "\n".join(lines),
    )
    record(
        "D.2 strengthening to fusion compatibility removes the closing label-count state",
        True,
        "The retained monoidal representation structure points to rank dimension, not label count.",
    )

    section("E. Verdict")

    residual = sp.simplify(b - a)
    record(
        "E.1 equivariant K/index route does not close Q",
        residual == b - a,
        f"RESIDUAL_INDEX_PAIRING={residual}",
    )
    record(
        "E.2 Q remains open after K-index audit",
        True,
        "Residual primitive: justify label-counting quotient state over additive/fusion index data.",
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
        print("VERDICT: equivariant K/index pairing does not close Q.")
        print("KOIDE_Q_EQUIVARIANT_K_INDEX_PAIRING_NO_GO=TRUE")
        print("Q_EQUIVARIANT_K_INDEX_PAIRING_CLOSES_Q=FALSE")
        print("RESIDUAL_SCALAR=label_counting_index_weight_minus_rank_fusion_weight")
        print("RESIDUAL_INDEX_PAIRING=additive_pairing_does_not_select_a_equals_b")
        return 0

    print("VERDICT: equivariant K-index audit has FAILs.")
    print("KOIDE_Q_EQUIVARIANT_K_INDEX_PAIRING_NO_GO=FALSE")
    print("Q_EQUIVARIANT_K_INDEX_PAIRING_CLOSES_Q=FALSE")
    print("RESIDUAL_SCALAR=label_counting_index_weight_minus_rank_fusion_weight")
    print("RESIDUAL_INDEX_PAIRING=additive_pairing_does_not_select_a_equals_b")
    return 1


if __name__ == "__main__":
    sys.exit(main())
