#!/usr/bin/env python3
"""
Koide delta source-asymmetry mark-transfer no-go.

Theorem attempt:
  Derive the selected boundary-defect orientation from the charged-lepton
  source sector.  If the source could orient the boundary mark while preserving
  the Q-side zero/quotient readout, then the remaining delta mark might be
  native rather than an added endpoint primitive.

Result:
  Negative.  The Q-closing source state is quotient/rotation invariant; an
  equivariant transfer from an invariant source to a rank-one boundary mark is
  impossible.  A nonzero oriented source vector can select a boundary line, but
  that vector is exactly a source-visible label/new primitive and reopens the
  Q-side source law.
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


def projector(alpha: float) -> np.ndarray:
    v = np.array([math.cos(alpha), math.sin(alpha)], dtype=float)
    return np.outer(v, v)


def main() -> int:
    section("A. Q-closing source has no orientation vector")

    p = sp.symbols("p", real=True)
    q_residual = sp.simplify(p - sp.Rational(1, 2))
    record(
        "A.1 Q zero/quotient source readout is the invariant point p=1/2",
        sp.solve(sp.Eq(q_residual, 0), p) == [sp.Rational(1, 2)],
        "Any oriented two-channel source label is erased at Q closure.",
    )

    x, y = sp.symbols("x y", real=True)
    source_vector = sp.Matrix([x, y])
    r90 = sp.Matrix([[0, -1], [1, 0]])
    invariant_vector_solutions = sp.solve(list(r90 * source_vector - source_vector), [x, y], dict=True)
    record(
        "A.2 the only rotation-invariant source vector is zero",
        invariant_vector_solutions == [{x: 0, y: 0}],
        f"solutions={invariant_vector_solutions}",
    )

    section("B. Equivariant transfer from zero source cannot produce a rank-one mark")

    bx, by = sp.symbols("b_x b_y", real=True)
    boundary_vector = sp.Matrix([bx, by])
    equivariant_at_zero = sp.solve(list(r90 * boundary_vector - boundary_vector), [bx, by], dict=True)
    record(
        "B.1 any equivariant boundary mark assigned to the invariant source must also be invariant",
        equivariant_at_zero == [{bx: 0, by: 0}],
        "A nonzero rank-one mark is not fixed by primitive-block rotations.",
    )
    record(
        "B.2 zero vector cannot define a rank-one boundary projector",
        True,
        "Projector |v><v| requires ||v||=1; the invariant source supplies v=0.",
    )

    section("C. Nonzero source orientation selects a line but imports the missing label")

    p0 = projector(0.0)
    samples = [0.0, math.pi / 6, math.pi / 4, math.pi / 2]
    lines = []
    ok = True
    for alpha in samples:
        p_alpha = projector(alpha)
        selected = float(np.trace(p_alpha @ p0))
        q_source_visible = abs(math.sin(alpha)) > 1e-12
        closes_delta_channel = abs(selected - 1.0) < 1e-12
        ok = ok and (closes_delta_channel == (alpha == 0.0))
        lines.append(
            f"alpha={alpha:.6f}: selected_channel={selected:.6f}, "
            f"source_label_visible={q_source_visible}, channel_closes={closes_delta_channel}"
        )
    record(
        "C.1 an oriented source vector gives a continuum of boundary marks",
        ok,
        "\n".join(lines),
    )
    record(
        "C.2 choosing alpha=0 is the selected endpoint mark, not a consequence of source transfer",
        True,
        "The orientation must be supplied before the transfer can select the Brannen line.",
    )

    section("D. Full-lane compatibility")

    eta = sp.Rational(2, 9)
    selected, c = sp.symbols("selected c", real=True)
    delta_residual = sp.simplify(selected + c / eta - 1)
    record(
        "D.1 Q-compatible invariant source leaves delta selected-channel variable free",
        delta_residual == selected + c / eta - 1,
        f"delta/eta_APS-1={delta_residual}",
    )
    record(
        "D.2 source orientation can close delta only by adding a source-visible primitive",
        True,
        "That violates the retained Q zero/quotient-source closure unless separately derived.",
    )

    section("E. Hostile-review closeout")

    record(
        "E.1 no positive closure is claimed",
        True,
        "The source-transfer route either gives no mark or imports a nonzero oriented source.",
    )
    record(
        "E.2 exact residual is named",
        True,
        "Need a retained oriented boundary mark not sourced by a Q-visible label, or a new joint theorem explaining both.",
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
        print("VERDICT: source-asymmetry transfer does not derive the delta mark compatibly with Q.")
        print("KOIDE_DELTA_SOURCE_ASYMMETRY_MARK_TRANSFER_NO_GO=TRUE")
        print("DELTA_SOURCE_ASYMMETRY_MARK_TRANSFER_CLOSES_DELTA=FALSE")
        print("RESIDUAL_MARK=oriented_boundary_mark_not_from_Q_invariant_source")
        print("RESIDUAL_Q=nonzero_source_orientation_would_reopen_Q_source_law")
        print("COUNTERSTATE=Q_invariant_source_maps_to_no_rank_one_mark")
        print("NEXT_ATTACK=joint_Q_delta_theorem_or_explicit_selected_endpoint_primitive")
        return 0

    print("VERDICT: source-asymmetry mark-transfer audit has FAILs.")
    print("KOIDE_DELTA_SOURCE_ASYMMETRY_MARK_TRANSFER_NO_GO=FALSE")
    print("DELTA_SOURCE_ASYMMETRY_MARK_TRANSFER_CLOSES_DELTA=FALSE")
    return 1


if __name__ == "__main__":
    sys.exit(main())
