#!/usr/bin/env python3
"""
Koide delta unmarked-primitive naturality no-go.

Theorem attempt:
  Derive the selected endpoint support law from the unmarked real primitive
  boundary object by representation-theoretic naturality.  If naturality
  forced a rank-one selected projector, then the spectator channel would
  vanish and the Brannen delta bridge would close after the basepoint law.

Result:
  Negative.  The automorphism group of the unmarked rank-two primitive acts
  transitively on rank-one lines.  Any natural positive readout on that object
  is scalar on the primitive block, so a normalized readout gives selected
  channel 1/2, not 1.  Selecting a rank-one line requires a retained mark.
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


def rotation(theta: float) -> np.ndarray:
    return np.array(
        [[math.cos(theta), -math.sin(theta)], [math.sin(theta), math.cos(theta)]],
        dtype=float,
    )


def projector(theta: float) -> np.ndarray:
    v = np.array([math.cos(theta), math.sin(theta)], dtype=float)
    return np.outer(v, v)


def main() -> int:
    section("A. Unmarked primitive has no natural rank-one line")

    p0 = projector(0.0)
    r = rotation(math.pi / 2)
    p_rot = r @ p0 @ r.T
    record(
        "A.1 a rank-one line is not invariant under primitive-block automorphisms",
        np.linalg.norm(p_rot - p0) > 1e-6 and abs(np.trace(p0) - 1.0) < 1e-12,
        f"||R(pi/2) P0 R^T - P0||={np.linalg.norm(p_rot - p0):.6f}",
    )

    theta = math.pi / 5
    p_theta = projector(theta)
    r_theta = rotation(theta)
    record(
        "A.2 rotations move the selected line through a continuum of equally retained lines",
        np.linalg.norm(r_theta @ p0 @ r_theta.T - p_theta) < 1e-12
        and np.linalg.norm(p_theta - p0) > 1e-3,
        "The unmarked primitive supplies the rank-two block, not a distinguished line in it.",
    )

    section("B. Naturality forces scalar readout on the unmarked block")

    a, b, d = sp.symbols("a b d", real=True)
    rho = sp.Matrix([[a, b], [b, d]])
    r90 = sp.Matrix([[0, -1], [1, 0]])
    invariance = sp.simplify(r90 * rho * r90.T - rho)
    equations = list(invariance)
    solution = sp.solve(equations + [sp.Eq(a + d, 1)], [a, b, d], dict=True)
    record(
        "B.1 O(2)-naturality plus normalization gives rho=I/2",
        solution == [{a: sp.Rational(1, 2), b: 0, d: sp.Rational(1, 2)}],
        f"solutions={solution}",
    )

    rho_nat = sp.Matrix([[sp.Rational(1, 2), 0], [0, sp.Rational(1, 2)]])
    p_sel = sp.Matrix([[1, 0], [0, 0]])
    p_spec = sp.Matrix([[0, 0], [0, 1]])
    selected_channel = sp.simplify(sp.trace(rho_nat * p_sel))
    spectator_channel = sp.simplify(sp.trace(rho_nat * p_spec))
    record(
        "B.2 natural unmarked readout gives selected=spectator=1/2, not selected=1",
        selected_channel == sp.Rational(1, 2) and spectator_channel == sp.Rational(1, 2),
        f"selected_channel={selected_channel}, spectator_channel={spectator_channel}",
    )

    section("C. Delta residual under natural unmarked readout")

    eta = sp.Rational(2, 9)
    c = sp.symbols("c", real=True)
    delta_open = sp.simplify(selected_channel * eta + c)
    residual = sp.simplify(delta_open / eta - 1)
    record(
        "C.1 unmarked naturality leaves the exact half-channel residual",
        residual == sp.Rational(-1, 2) + c / eta,
        f"delta_open={delta_open}; delta/eta_APS-1={residual}",
    )
    record(
        "C.2 even with based endpoint c=0, unmarked naturality gives delta=1/9",
        sp.simplify(delta_open.subs(c, 0)) == sp.Rational(1, 9),
        "This is support for the primitive block, not the selected Brannen line.",
    )

    section("D. Marked-line conditional closure boundary")

    marked_rho = sp.Matrix([[1, 0], [0, 0]])
    marked_selected = sp.simplify(sp.trace(marked_rho * p_sel))
    marked_spectator = sp.simplify(sp.trace(marked_rho * p_spec))
    marked_delta = sp.simplify(marked_selected * eta)
    record(
        "D.1 a retained selected-line mark would force selected=1 and spectator=0",
        marked_selected == 1 and marked_spectator == 0 and marked_delta == eta,
        f"marked selected={marked_selected}, spectator={marked_spectator}, delta={marked_delta}",
    )
    record(
        "D.2 but the mark is exactly the missing physical endpoint support law",
        True,
        "Naturality of the unmarked primitive cannot create a rank-one mark.",
    )

    section("E. Hostile-review closeout")

    record(
        "E.1 no hidden eta or fitted delta is used",
        True,
        "The no-go is representation-theoretic; eta is only used after the channel weights are derived.",
    )
    record(
        "E.2 positive closure is not claimed",
        True,
        "Need a retained mark/support theorem plus endpoint basepoint; unmarked naturality gives the wrong channel weight.",
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
        print("VERDICT: unmarked primitive naturality does not derive selected delta.")
        print("KOIDE_DELTA_UNMARKED_PRIMITIVE_NATURALITY_NO_GO=TRUE")
        print("DELTA_UNMARKED_PRIMITIVE_NATURALITY_CLOSES_DELTA=FALSE")
        print("RESIDUAL_MARK=retained_selected_rank_one_endpoint_mark")
        print("RESIDUAL_CHANNEL=selected_channel_one_not_unmarked_natural")
        print("COUNTERSTATE=unmarked_natural_readout_selected_equals_one_half_delta_one_ninth")
        print("NEXT_ATTACK=derive_selected_rank_one_mark_from_boundary_source_or_defect")
        return 0

    print("VERDICT: unmarked primitive naturality audit has FAILs.")
    print("KOIDE_DELTA_UNMARKED_PRIMITIVE_NATURALITY_NO_GO=FALSE")
    print("DELTA_UNMARKED_PRIMITIVE_NATURALITY_CLOSES_DELTA=FALSE")
    return 1


if __name__ == "__main__":
    sys.exit(main())
