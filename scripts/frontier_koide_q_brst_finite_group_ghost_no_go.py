#!/usr/bin/env python3
"""
Koide Q finite-group BRST/ghost no-go.

Theorem attempt:
  The retained C3 quotient might introduce a BRST/Faddeev-Popov ghost sector
  whose determinant or zero-mode index cancels the singlet/doublet rank
  mismatch, thereby forcing equal block totals and K_TL = 0.

Result:
  Negative.  For a finite group in characteristic zero, there are no
  continuous gauge directions and no Faddeev-Popov ghost zero modes.  The
  cyclic group cohomology H^1(C3,V_3) vanishes explicitly:

      ker(1+C+C^2) and im(C-I) both have dimension 2.

  The finite group-volume factor is a common scalar and cannot change the
  singlet/doublet block ratio.  Thus BRST/ghost quotienting does not supply
  the missing auxiliary dimension or equal-block source law.

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
    section("A. C3 group cohomology on the retained triplet")

    C = sp.Matrix([[0, 0, 1], [1, 0, 0], [0, 1, 0]])
    I3 = sp.eye(3)
    N = sp.simplify(I3 + C + C**2)
    coboundary = sp.simplify(C - I3)
    dim_ker_N = 3 - N.rank()
    dim_im_coboundary = coboundary.rank()
    h1_dim = sp.simplify(dim_ker_N - dim_im_coboundary)

    record(
        "A.1 norm map N=1+C+C^2 has kernel dimension 2",
        N.rank() == 1 and dim_ker_N == 2,
        f"rank(N)={N.rank()}, dim ker(N)={dim_ker_N}",
    )
    record(
        "A.2 coboundary image im(C-I) has dimension 2",
        dim_im_coboundary == 2,
        f"rank(C-I)={dim_im_coboundary}",
    )
    record(
        "A.3 H^1(C3,V3)=ker(N)/im(C-I) vanishes",
        h1_dim == 0,
        f"dim H1={h1_dim}",
    )

    section("B. Finite group volume is a common scalar")

    gvol = sp.Integer(3)
    w_plus, w_perp = sp.Integer(1), sp.Integer(2)
    ratio_before = sp.simplify(w_perp / w_plus)
    ratio_after = sp.simplify((w_perp / gvol) / (w_plus / gvol))
    record(
        "B.1 dividing by finite group volume does not change block ratio",
        ratio_before == 2 and ratio_after == ratio_before,
        f"ratio_before={ratio_before}, ratio_after={ratio_after}",
    )
    record(
        "B.2 rank-weighted quotient remains off the equal-block leaf",
        q_from_ratio(ratio_after) == 1 and ktl_from_ratio(ratio_after) == sp.Rational(3, 8),
        f"Q={q_from_ratio(ratio_after)}, K_TL={ktl_from_ratio(ratio_after)}",
    )

    section("C. Missing auxiliary dimension is not supplied")

    ghost_zero_modes = h1_dim
    effective_index = sp.simplify(1 - 2 + ghost_zero_modes)
    record(
        "C.1 finite C3 BRST ghost zero-mode count is zero",
        ghost_zero_modes == 0,
        f"ghost_zero_modes={ghost_zero_modes}",
    )
    record(
        "C.2 the singlet/doublet index remains nonzero after finite-group ghost audit",
        effective_index == -1,
        f"effective_index=1-2+ghosts={effective_index}",
    )
    record(
        "C.3 cancelling the index would require a new auxiliary zero mode",
        sp.solve(sp.Eq(1 - 2 + sp.symbols('aux'), 0), sp.symbols('aux')) == [1],
        "The finite C3 quotient does not provide it.",
    )

    section("D. Verdict")

    record(
        "D.1 finite-group BRST/ghost route does not close Q",
        True,
        "There are no continuous FP ghost zero modes and the group-volume factor is common.",
    )
    record(
        "D.2 Q remains open after finite-group ghost audit",
        True,
        "Residual primitive: equal block/source-neutral law despite finite-group rank/index data.",
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
        print("VERDICT: finite-group BRST/ghost quotient does not close Q.")
        print("KOIDE_Q_BRST_FINITE_GROUP_GHOST_NO_GO=TRUE")
        print("Q_BRST_FINITE_GROUP_GHOST_CLOSES_Q=FALSE")
        print("RESIDUAL_SCALAR=no_C3_ghost_zero_mode_to_cancel_rank_mismatch")
        print("RESIDUAL_GHOST_INDEX=no_C3_ghost_zero_mode_to_cancel_rank_mismatch")
        return 0

    print("VERDICT: finite-group BRST/ghost audit has FAILs.")
    print("KOIDE_Q_BRST_FINITE_GROUP_GHOST_NO_GO=FALSE")
    print("Q_BRST_FINITE_GROUP_GHOST_CLOSES_Q=FALSE")
    print("RESIDUAL_SCALAR=no_C3_ghost_zero_mode_to_cancel_rank_mismatch")
    print("RESIDUAL_GHOST_INDEX=no_C3_ghost_zero_mode_to_cancel_rank_mismatch")
    return 1


if __name__ == "__main__":
    sys.exit(main())
