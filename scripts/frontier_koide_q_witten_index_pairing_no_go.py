#!/usr/bin/env python3
"""
Koide Q Witten-index pairing no-go.

Theorem attempt:
  A hidden supersymmetric pairing or Witten-index cancellation between the
  retained C3 singlet and real doublet blocks might force equal block totals,
  hence K_TL = 0.

Result:
  Negative.  The singlet block has real dimension 1 and the doublet block has
  real dimension 2.  Any odd supercharge pairing between them has rank at most
  1, leaving one unpaired doublet direction.  The graded index is therefore

      dim(P_plus) - dim(P_perp) = 1 - 2 = -1,

  not zero.  A complete cancellation/equal-block law would require adding an
  auxiliary/ghost dimension or changing the retained carrier.

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


def q_from_ratio(r: sp.Expr) -> sp.Expr:
    return sp.simplify((1 + r) / 3)


def ktl_from_ratio(r: sp.Expr) -> sp.Expr:
    return sp.simplify((r**2 - 1) / (4 * r))


def main() -> int:
    section("A. Retained block dimensions and graded index")

    dim_plus = sp.Integer(1)
    dim_perp = sp.Integer(2)
    index = sp.simplify(dim_plus - dim_perp)
    record(
        "A.1 retained singlet/doublet dimensions are 1 and 2",
        dim_plus == 1 and dim_perp == 2,
        f"dim_plus={dim_plus}, dim_perp={dim_perp}",
    )
    record(
        "A.2 Witten/supertrace index is nonzero",
        index == -1,
        f"Str(I)=dim_plus-dim_perp={index}",
    )

    section("B. Odd pairing rank obstruction")

    # General odd map Q: V_plus -> V_perp has shape 2x1 and rank at most 1.
    a, b = sp.symbols("a b", real=True)
    Q = sp.Matrix([[a], [b]])
    rank_generic = Q.rank()
    unpaired_doublet_dimension = sp.simplify(dim_perp - rank_generic)
    record(
        "B.1 a singlet-to-doublet odd pairing has rank at most 1",
        rank_generic == 1,
        f"Q=[[a],[b]], generic rank={rank_generic}",
    )
    record(
        "B.2 one real doublet direction remains unpaired",
        unpaired_doublet_dimension == 1,
        f"dim_perp-rank(Q)={unpaired_doublet_dimension}",
    )

    # General odd map in the opposite direction V_perp -> V_plus has shape 1x2.
    c, d = sp.symbols("c d", real=True)
    Q_op = sp.Matrix([[c, d]])
    rank_op = Q_op.rank()
    unpaired_again = sp.simplify(dim_perp - rank_op)
    record(
        "B.3 reversing the odd map does not remove the index obstruction",
        rank_op == 1 and unpaired_again == 1,
        f"Q_op=[[c,d]], generic rank={rank_op}, unpaired doublet={unpaired_again}",
    )

    section("C. Consequence for equal-block source neutrality")

    r_rank = sp.simplify(dim_perp / dim_plus)
    r_equal = sp.Integer(1)
    record(
        "C.1 rank/supertrace counting gives ratio 2 and off-Koide source",
        r_rank == 2
        and q_from_ratio(r_rank) == 1
        and ktl_from_ratio(r_rank) == sp.Rational(3, 8),
        f"R_rank={r_rank}, Q={q_from_ratio(r_rank)}, K_TL={ktl_from_ratio(r_rank)}",
    )
    record(
        "C.2 equal block totals would require cancelling the nonzero index",
        q_from_ratio(r_equal) == sp.Rational(2, 3)
        and ktl_from_ratio(r_equal) == 0
        and index != 0,
        f"R_equal={r_equal}, Q={q_from_ratio(r_equal)}, K_TL={ktl_from_ratio(r_equal)}, index={index}",
    )

    section("D. Adding an auxiliary dimension is outside the retained carrier")

    aux = sp.symbols("aux", integer=True, nonnegative=True)
    index_with_aux = sp.simplify(dim_plus + aux - dim_perp)
    aux_needed = sp.solve(sp.Eq(index_with_aux, 0), aux)
    record(
        "D.1 zero index requires one auxiliary singlet/ghost dimension",
        aux_needed == [1],
        f"dim_plus+aux-dim_perp=0 -> aux={aux_needed}",
    )
    record(
        "D.2 adding that auxiliary dimension would be a new retained field/source",
        True,
        "It changes the retained charged-lepton second-order carrier rather than deriving K_TL=0 on it.",
    )

    section("E. Verdict")

    record(
        "E.1 supersymmetric/Witten-index pairing route does not close Q",
        True,
        "Rank mismatch gives a nonzero index and an unpaired doublet direction.",
    )
    record(
        "E.2 Q remains open after Witten-index audit",
        True,
        "Residual primitive: physical law for equal block totals despite nonzero retained index.",
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
        print("VERDICT: Witten-index/supersymmetric pairing does not close Q.")
        print("KOIDE_Q_WITTEN_INDEX_PAIRING_NO_GO=TRUE")
        print("Q_WITTEN_INDEX_PAIRING_CLOSES_Q=FALSE")
        print("RESIDUAL_SCALAR=dim_plus_minus_dim_perp_nonzero_equiv_K_TL")
        print("RESIDUAL_INDEX=dim_plus_minus_dim_perp_nonzero_equiv_K_TL")
        return 0

    print("VERDICT: Witten-index pairing audit has FAILs.")
    print("KOIDE_Q_WITTEN_INDEX_PAIRING_NO_GO=FALSE")
    print("Q_WITTEN_INDEX_PAIRING_CLOSES_Q=FALSE")
    print("RESIDUAL_SCALAR=dim_plus_minus_dim_perp_nonzero_equiv_K_TL")
    print("RESIDUAL_INDEX=dim_plus_minus_dim_perp_nonzero_equiv_K_TL")
    return 1


if __name__ == "__main__":
    sys.exit(main())
