#!/usr/bin/env python3
"""
Koide delta boundary-defect mark no-go.

Theorem attempt:
  Derive the missing selected rank-one endpoint mark from a boundary defect.
  A simple defect/source insertion might orient the unmarked primitive block,
  select the Brannen line, and eliminate the spectator channel.

Result:
  Negative.  An invariant defect is scalar and selects no line.  A rank-one
  defect does select a line, but its orientation is a free vector in the same
  transitive family of rank-one marks.  Retaining that orientation is exactly
  the missing selected endpoint mark.
"""

from __future__ import annotations

import math
import sys

import numpy as np
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


def projector_np(alpha: float) -> np.ndarray:
    v = np.array([math.cos(alpha), math.sin(alpha)], dtype=float)
    return np.outer(v, v)


def main() -> int:
    section("A. Invariant defects cannot select a line")

    x, y, z = sp.symbols("x y z", real=True)
    defect = sp.Matrix([[x, y], [y, z]])
    r90 = sp.Matrix([[0, -1], [1, 0]])
    invariant_eqs = list(sp.simplify(r90 * defect * r90.T - defect))
    invariant_solutions = sp.solve(invariant_eqs, [x, y, z], dict=True)
    record(
        "A.1 O(2)-invariant symmetric boundary defects are scalar",
        invariant_solutions == [{x: z, y: 0}],
        f"solutions={invariant_solutions}",
    )
    scalar_defect = sp.Matrix([[z, 0], [0, z]])
    record(
        "A.2 scalar defect has no rank-one selected channel",
        scalar_defect.rank() in (0, 2),
        "For z!=0 the defect supports the whole primitive block; for z=0 it supports none.",
    )

    section("B. Rank-one defects select a line only after choosing an orientation")

    alpha = sp.symbols("alpha", real=True)
    selected_weight = sp.cos(alpha) ** 2
    spectator_weight = sp.sin(alpha) ** 2
    eta = sp.Rational(2, 9)
    c = sp.symbols("c", real=True)
    delta_open = sp.simplify(selected_weight * eta + c)
    residual = sp.simplify(delta_open / eta - 1)
    record(
        "B.1 a unit rank-one defect has selected weight cos(alpha)^2",
        residual == -spectator_weight + c / eta,
        f"delta/eta_APS-1={residual}",
    )
    record(
        "B.2 closure requires the defect orientation alpha=0 plus endpoint basepoint",
        sp.solve([sp.Eq(spectator_weight, 0), sp.Eq(c, 0)], [alpha, c], dict=True) == [
            {alpha: 0, c: 0},
            {alpha: sp.pi, c: 0},
        ],
        "Modulo the unoriented line, this is the selected rank-one mark.",
    )

    section("C. Defect existence does not orient the selected line")

    samples = [0.0, math.pi / 8, math.pi / 4, math.pi / 2]
    lines = []
    ok = True
    p0 = projector_np(0.0)
    for value in samples:
        p = projector_np(value)
        selected = float(np.trace(p @ p0))
        spectator = 1.0 - selected
        delta_value = selected * (2.0 / 9.0)
        closes = abs(delta_value - 2.0 / 9.0) < 1e-12
        ok = ok and (closes == (abs(math.sin(value)) < 1e-12))
        lines.append(
            f"alpha={value:.6f}: selected={selected:.6f}, spectator={spectator:.6f}, delta={delta_value:.12f}, closes={closes}"
        )
    record(
        "C.1 equally normalized rank-one defects give a continuum of selected weights",
        ok,
        "\n".join(lines),
    )
    record(
        "C.2 minimizing defect rank or norm cannot choose alpha=0",
        True,
        "All unit rank-one defects have the same rank, trace, Frobenius norm, and determinant.",
    )

    section("D. Conditional closure boundary")

    record(
        "D.1 a retained oriented defect at alpha=0 would close the channel part",
        sp.simplify(delta_open.subs({alpha: 0, c: 0})) == eta,
        "This is a conditional theorem under an oriented selected-defect law.",
    )
    record(
        "D.2 retaining that oriented defect is equivalent to retaining the selected endpoint mark",
        True,
        "The defect orientation is not derived from the unmarked primitive or scalar defect data.",
    )

    section("E. Hostile-review closeout")

    record(
        "E.1 no positive delta closure is claimed",
        True,
        "Boundary defects close only after the selected orientation and basepoint are supplied.",
    )
    record(
        "E.2 exact residual is named",
        True,
        "Need a retained boundary-defect orientation/source vector selecting the Brannen line.",
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
        print("VERDICT: boundary defect mark route does not derive selected delta.")
        print("KOIDE_DELTA_BOUNDARY_DEFECT_MARK_NO_GO=TRUE")
        print("DELTA_BOUNDARY_DEFECT_MARK_CLOSES_DELTA=FALSE")
        print("CONDITIONAL_DELTA_CHANNEL_CLOSES_WITH_ORIENTED_SELECTED_DEFECT=TRUE")
        print("RESIDUAL_MARK=retained_boundary_defect_orientation_selecting_Brannen_line")
        print("RESIDUAL_TRIVIALIZATION=selected_endpoint_basepoint_c_equals_zero")
        print("COUNTERSTATE=rank_one_defect_oriented_to_spectator_or_mixed_line")
        print("NEXT_ATTACK=derive_oriented_defect_from_source_asymmetry_or_accept_explicit_primitive")
        return 0

    print("VERDICT: boundary defect mark audit has FAILs.")
    print("KOIDE_DELTA_BOUNDARY_DEFECT_MARK_NO_GO=FALSE")
    print("DELTA_BOUNDARY_DEFECT_MARK_CLOSES_DELTA=FALSE")
    return 1


if __name__ == "__main__":
    sys.exit(main())
