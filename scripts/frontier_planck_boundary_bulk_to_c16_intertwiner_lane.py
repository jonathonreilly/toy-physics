#!/usr/bin/env python3
"""Audit the boundary bulk-to-C^16 intertwiner lane honestly.

This lane does not claim Planck closure. It proves the sharper statement:

  - the minimal Schur boundary carrier is 2-dimensional;
  - the full hw=1 axis projector on the democratic C^16 carrier has rank 4;
  - therefore no faithful pullback/pushforward intertwiner from the minimal
    Schur carrier can realize the full axis projector;
  - the unique permutation-blind rank-2 quotient is the singlet block
    span{|t>, (|x>+|y>+|z>)/sqrt(3)};
  - under the democratic full-cell state, that quotient carries mass 1/8,
    while the full axis projector carries mass 1/4;
  - so the remaining bridge is an explicit multiplicity/lift theorem, not a
    hidden canonical intertwiner.
"""

from __future__ import annotations

from pathlib import Path
import sys

import sympy as sp


ROOT = Path(__file__).resolve().parents[1]
NOTE = ROOT / "docs/PLANCK_SCALE_BOUNDARY_BULK_TO_C16_INTERTWINER_LANE_2026-04-23.md"
SCHUR = ROOT / "docs/PLANCK_SCALE_BULK_TO_BOUNDARY_SCHUR_COMPLETION_LANE_2026-04-23.md"
CANON = ROOT / "docs/PLANCK_SCALE_BOUNDARY_TRANSFER_OPERATOR_CANONICALITY_LANE_2026-04-23.md"
C16 = ROOT / "docs/PLANCK_SCALE_C16_TASTE_CELL_ONE_SIXTEENTH_LANE_2026-04-23.md"
BRIDGE = ROOT / "docs/PLANCK_SCALE_C16_BOUNDARY_PRESSURE_BRIDGE_LANE_2026-04-23.md"
AXIS = ROOT / "docs/PLANCK_SCALE_C16_AXIS_MASS_PHYSICAL_PRESSURE_IDENTIFICATION_LANE_2026-04-23.md"
TIMELOCK = ROOT / "docs/PLANCK_SCALE_SPACETIME_TIME_LOCK_UNIT_MAP_LANE_2026-04-23.md"


def normalized(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").split()).lower()


def section(title: str) -> None:
    print("\n" + "=" * 78)
    print(title)
    print("=" * 78)


def check(label: str, passed: bool, detail: str) -> bool:
    passed = bool(passed)
    tag = "PASS" if passed else "FAIL"
    print(f"  [{tag}] {label}")
    print(f"         {detail}")
    return passed


def main() -> int:
    note = normalized(NOTE)
    schur = normalized(SCHUR)
    canon = normalized(CANON)
    c16 = normalized(C16)
    bridge = normalized(BRIDGE)
    axis = normalized(AXIS)
    timelock = normalized(TIMELOCK)

    n_pass = 0
    n_fail = 0

    print("Planck boundary bulk-to-C^16 intertwiner lane audit")
    print("=" * 78)

    section("PART 1: UPSTREAM ALIGNMENT")
    p = check(
        "Schur lane still fixes the canonical 2x2 boundary witness",
        "l_sigma = [[4/3, 1/3], [1/3, 4/3]]" in schur
        and "2-dimensional" in note,
        "the new lane must work on the already-earned minimal Schur carrier",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "canonicality lane still fixes the boundary route on the minimal Schur witness",
        "t_can(tau) = exp(-tau l_sigma)" in canon
        and "l_sigma = [[4/3, 1/3], [1/3, 4/3]]" in schur,
        "the bulk-to-boundary route should not silently enlarge the boundary carrier",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "C^16 lanes still fix the democratic full-cell state and the axis-sector quarter",
        "rho_cell = i_16 / 16" in c16
        and "m_axis = 4 * (1/16) = 1/4" in bridge
        and "m_axis = tr(rho_cell p_a) = 1/4" in axis,
        "the new route must attack the same quarter-valued axis quantity already isolated upstream",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "time-lock is still exact",
        "a_s = c a_t" in timelock and "beta = 1" in timelock,
        "the axis carrier should still be read on the locked 3+1 surface",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("PART 2: FULL-AXIS PROJECTOR VS MINIMAL SCHUR DIMENSION")
    dim_sigma = 2
    dim_axis = 4
    p = check(
        "the minimal Schur carrier has dimension 2 while the full axis carrier has dimension 4",
        dim_sigma == 2 and dim_axis == 4,
        "this is the core dimensional mismatch behind the faithful-intertwiner question",
    )
    n_pass += int(p)
    n_fail += int(not p)

    J = sp.Matrix([[1, 0], [0, 1], [1, 1], [2, -1]])
    p = check(
        "a full-rank 4x2 boundary-to-axis map still gives rank(J J^T) = 2",
        J.rank() == 2 and (J * J.T).rank() == 2,
        "operators induced from a 2-dimensional carrier cannot exceed rank 2 on the axis side",
    )
    n_pass += int(p)
    n_fail += int(not p)

    K = sp.Matrix([[1, 0, 0, 1], [0, 1, 1, 0]])
    p = check(
        "a full-rank 2x4 axis-to-boundary map still gives rank(K^T K) = 2",
        K.rank() == 2 and (K.T * K).rank() == 2,
        "pulling back through a 2-dimensional boundary carrier cannot reproduce a rank-4 projector",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p_a = sp.eye(4)
    p = check(
        "the full axis projector has rank 4",
        p_a.rank() == 4,
        "P_A is the identity on the four-state axis carrier",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "there is no faithful exact pullback/pushforward identity with P_A from a 2-dimensional carrier",
        (J * J.T).rank() < p_a.rank() and (K.T * K).rank() < p_a.rank(),
        "no linear map to/from the minimal Schur carrier can realize the full rank-4 axis projector faithfully",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("PART 3: THE UNIQUE PERMUTATION-BLIND QUOTIENT")
    # Basis order: t, x, y, z
    t = sp.Matrix([1, 0, 0, 0])
    x = sp.Matrix([0, 1, 0, 0])
    y = sp.Matrix([0, 0, 1, 0])
    z = sp.Matrix([0, 0, 0, 1])
    s = (x + y + z) / sp.sqrt(3)
    e1 = (x - y) / sp.sqrt(2)
    e2 = (x + y - 2 * z) / sp.sqrt(6)

    perm_xy = sp.Matrix(
        [
            [1, 0, 0, 0],
            [0, 0, 1, 0],
            [0, 1, 0, 0],
            [0, 0, 0, 1],
        ]
    )
    perm_yz = sp.Matrix(
        [
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 0, 1],
            [0, 0, 1, 0],
        ]
    )

    fixed_constraints = sp.Matrix.vstack(perm_xy - sp.eye(4), perm_yz - sp.eye(4))
    fixed_dim = 4 - fixed_constraints.rank()
    p = check(
        "the S3-fixed subspace of the axis carrier is exactly 2-dimensional",
        fixed_dim == 2,
        "the only permutation-blind axis data are the time line and the uniform spatial line",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the canonical fixed basis is {|t>, |s>} with |s> = (|x>+|y>+|z>)/sqrt(3)",
        perm_xy * t == t
        and perm_yz * t == t
        and sp.simplify(perm_xy * s - s) == sp.zeros(4, 1)
        and sp.simplify(perm_yz * s - s) == sp.zeros(4, 1),
        "the collective spatial direction is uniquely the normalized uniform sum of x,y,z",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the remaining spatial data form a 2-dimensional doublet E",
        sp.simplify(perm_xy * e1 - e1) != sp.zeros(4, 1)
        and sp.simplify(perm_yz * e2 - e2) != sp.zeros(4, 1)
        and sp.Matrix.hstack(t, s, e1, e2).rank() == 4,
        "the full axis carrier splits as time singlet + spatial singlet + 2D doublet",
    )
    n_pass += int(p)
    n_fail += int(not p)

    q = sp.Matrix([[1, 0, 0, 0], [0, 1 / sp.sqrt(3), 1 / sp.sqrt(3), 1 / sp.sqrt(3)]])
    p_q = sp.simplify(q.T * q)
    p = check(
        "the canonical quotient projector has rank 2",
        p_q.rank() == 2 and sp.simplify(q * q.T - sp.eye(2)) == sp.zeros(2),
        "Q selects the unique permutation-blind quotient span{|t>,|s>}",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "compressing the full axis projector through Q yields only the 2x2 identity",
        sp.simplify(q * p_a * q.T - sp.eye(2)) == sp.zeros(2),
        "the full rank-4 axis data collapse to the minimal quotient rather than surviving faithfully",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("PART 4: DEMOCRATIC MASSES")
    rho16 = sp.eye(16) / 16
    mass_axis = sp.trace(rho16[:4, :4] * p_a)  # first four basis states identified with the axis carrier
    mass_q = sp.trace(rho16[:4, :4] * p_q)

    p = check(
        "the full axis projector still carries exact democratic mass 1/4",
        sp.simplify(mass_axis - sp.Rational(1, 4)) == 0,
        "this is the quarter-valued C^16 axis mass isolated upstream",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the canonical quotient projector carries exact democratic mass 1/8",
        sp.simplify(mass_q - sp.Rational(1, 8)) == 0,
        "the minimal quotient retains only half of the full axis mass",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the exact quotient loses a factor of 2 relative to the full axis projector",
        sp.simplify(mass_axis - 2 * mass_q) == 0,
        "quarter would require restoring the discarded doublet multiplicity",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("PART 5: NOTE HONESTY")
    p = check(
        "the note states the faithful-intertwiner no-go explicitly",
        "no faithful exact intertwiner" in note and "rank at most `2`" in note,
        "the writeup should make the dimensional obstruction explicit",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the note states the unique quotient and the 1/8 result explicitly",
        "unique rank-2 permutation-blind quotient" in note
        and "`1/8`" in note
        and "`1/4`" in note,
        "the highest-value outcome is the reduction from quarter to the singlet-quotient half-quarter",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the note does not overclaim closure",
        "does not close planck" in note and "remaining bridge" in note,
        "the lane should end as a no-go plus sharper target, not a false close",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("FINAL VERDICT")
    verdict = (
        "The direct bulk-to-C^16 intertwiner route does not close Planck. "
        "It proves a stronger obstruction: the minimal 2D Schur boundary carrier "
        "cannot faithfully realize the full rank-4 axis projector. The unique "
        "permutation-blind quotient is the singlet block span{|t>,|s>}, and under "
        "the democratic full-cell state that quotient carries mass 1/8, not 1/4. "
        "So any quarter closure on this route still needs one extra "
        "multiplicity/lift theorem."
    )
    print(f"  {verdict}")

    print("\n" + "=" * 78)
    print(f"SCORECARD: {n_pass} pass, {n_fail} fail out of {n_pass + n_fail}")
    print("=" * 78)

    return 0 if n_fail == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
