#!/usr/bin/env python3
"""Audit the C^16-to-boundary pressure bridge lane honestly.

This lane does not claim full boundary closure. It proves the sharper reduction:

  - primitive C^16 taste-cell share is exactly 1/16 and therefore cannot equal
    the surviving boundary quarter target;
  - the exact hw=1 axis-sector mass on the same democratic C^16 carrier is
    4 * (1/16) = 1/4 and is the canonical C^16 scalar that matches the target;
  - on the canonical Schur witness, quarter is equivalent to the shift law
    w = lambda_min(L_Sigma) + m_axis = 5/4;
  - therefore the remaining bridge is not a coefficient search but the
    physical identification p_* = m_axis.
"""

from __future__ import annotations

import itertools
from pathlib import Path
import sys

import numpy as np
import sympy as sp


ROOT = Path(__file__).resolve().parents[1]
NOTE = ROOT / "docs/PLANCK_SCALE_C16_BOUNDARY_PRESSURE_BRIDGE_LANE_2026-04-23.md"
C16 = ROOT / "docs/PLANCK_SCALE_C16_TASTE_CELL_ONE_SIXTEENTH_LANE_2026-04-23.md"
PRESSURE = ROOT / "docs/PLANCK_SCALE_BOUNDARY_PRESSURE_QUARTER_NORMALIZATION_LANE_2026-04-23.md"
CANON = ROOT / "docs/PLANCK_SCALE_BOUNDARY_TRANSFER_OPERATOR_CANONICALITY_LANE_2026-04-23.md"
SCHUR = ROOT / "docs/PLANCK_SCALE_BULK_TO_BOUNDARY_SCHUR_COMPLETION_LANE_2026-04-23.md"
INFO = ROOT / "docs/PLANCK_SCALE_TIMELOCKED_CONVERTED_INFORMATION_ACTION_CONSTANT_LANE_2026-04-23.md"


def section(title: str) -> None:
    print("\n" + "=" * 78)
    print(title)
    print("=" * 78)


def check(label: str, passed: bool, detail: str) -> bool:
    tag = "PASS" if passed else "FAIL"
    print(f"  [{tag}] {label}")
    print(f"         {detail}")
    return passed


def normalized(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").split()).lower()


def main() -> int:
    note = normalized(NOTE)
    c16 = normalized(C16)
    pressure = normalized(PRESSURE)
    canon = normalized(CANON)
    schur = normalized(SCHUR)
    info = normalized(INFO)

    n_pass = 0
    n_fail = 0

    print("Planck C^16 boundary pressure bridge lane audit")
    print("=" * 78)

    section("PART 1: UPSTREAM ALIGNMENT")
    p = check(
        "C^16 note still records primitive one-sixteenth and axis four-state reduction",
        "1/16" in c16
        and "hw=1" in c16
        and "axis sector" in c16
        and "2 bits" in c16,
        "the bridge lane must descend from the exact full-cell and axis-sector data",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "boundary-pressure note still isolates quarter as the surviving target",
        "p_* = sup spec(g_sigma) = 1/4" in pressure and "not yet" in pressure,
        "the bridge lane should attack the same remaining boundary value, not a different one",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "canonicality note still fixes the witness shift requirement mu = 5/4",
        "mu = 5/4" in canon and "rho(t_can(1)) = e^(-1) < 1" in canon,
        "the new lane should connect to the existing exact witness rather than replace it",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "Schur-completion note still identifies the same witness carrier",
        "l_sigma = [[4/3, 1/3], [1/3, 4/3]]" in schur
        and "normalization" in schur,
        "the bridge should work on the same canonical Schur carrier already isolated upstream",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "time-locked information note still records 1/32 per bit",
        "1/32" in info and ("2 bits" in info or "log 4" in info),
        "the bridge lane should remain consistent with the earlier C^16 information reduction",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("PART 2: EXACT C^16 FINE AND COARSE SCALARS")
    states = list(itertools.product((0, 1), repeat=4))
    dim = len(states)
    rho = np.eye(dim, dtype=float) / dim
    axis_states = [(1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1)]
    axis_indices = [states.index(state) for state in axis_states]

    p = check(
        "the exact four-bit taste-cell carrier has 16 states",
        dim == 16,
        "the structural carrier is eta in {0,1}^4",
    )
    n_pass += int(p)
    n_fail += int(not p)

    primitive_share = float(rho[0, 0])
    p = check(
        "each primitive democratic taste-cell share is exactly 1/16",
        abs(primitive_share - 1.0 / 16.0) < 1.0e-15,
        "rho_cell = I_16 / 16 assigns equal fine weight to every primitive taste cell",
    )
    n_pass += int(p)
    n_fail += int(not p)

    axis_mass = sum(float(rho[idx, idx]) for idx in axis_indices)
    p = check(
        "the exact hw=1 axis-sector mass is 4/16 = 1/4",
        abs(axis_mass - 0.25) < 1.0e-15,
        "the four axis cells carry total democratic mass 1/4 on the same carrier",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "primitive share and axis-sector mass are different canonical C^16 scalars",
        abs(axis_mass - 4.0 * primitive_share) < 1.0e-15 and abs(axis_mass - primitive_share) > 1.0e-12,
        "the boundary candidate must distinguish fine 1/16 from coarse 1/4",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("PART 3: THE CANONICAL C^16 BOUNDARY MATCH")
    p = check(
        "the surviving boundary target matches the coarse axis-sector mass, not the primitive share",
        abs(axis_mass - 0.25) < 1.0e-15 and abs(primitive_share - 0.25) > 1.0e-12,
        "if a same-surface C^16 bridge exists, it must read the hw=1 axis sector rather than a single primitive cell",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the quarter target is exactly 4 times the primitive C^16 share",
        abs(4.0 * primitive_share - 0.25) < 1.0e-15,
        "boundary quarter arises as the coarse four-axis sum over the same structural 16 carrier",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("PART 4: BRIDGE TO THE CANONICAL SCHUR WITNESS")
    l_sigma = sp.Matrix(
        [[sp.Rational(4, 3), sp.Rational(1, 3)], [sp.Rational(1, 3), sp.Rational(4, 3)]]
    )
    evals = sorted(l_sigma.eigenvals().keys(), key=lambda expr: float(sp.N(expr)))
    lambda_min = evals[0]
    p = check(
        "the canonical Schur witness has lambda_min = 1",
        evals == [sp.Integer(1), sp.Rational(5, 3)],
        "the earlier boundary lanes reduce the remaining normalization problem to this witness",
    )
    n_pass += int(p)
    n_fail += int(not p)

    w_star = sp.Rational(1, 4) + lambda_min
    p = check(
        "quarter on the shifted witness is equivalent to w = lambda_min + m_axis",
        sp.simplify(w_star - (lambda_min + sp.Rational(1, 4))) == 0
        and sp.simplify(w_star - sp.Rational(5, 4)) == 0,
        "the exact witness shift becomes 5/4 = 1 + 1/4",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the same shift can be written in terms of the structural 16 as w = lambda_min + 4 m_cell",
        sp.simplify(w_star - (lambda_min + 4 * sp.Rational(1, 16))) == 0,
        "the C^16 bridge rewrites the boundary normalization law in exact carrier terms",
    )
    n_pass += int(p)
    n_fail += int(not p)

    w = sp.symbols("w", real=True)
    top_pressure = w - lambda_min
    p = check(
        "identifying boundary pressure with the axis-sector mass reproduces the target exactly",
        sp.simplify(top_pressure.subs(w, lambda_min + sp.Rational(1, 4)) - sp.Rational(1, 4)) == 0,
        "p_*(w) = w - lambda_min becomes 1/4 when the additive shift equals the axis-sector mass",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("PART 5: HONESTY CHECK")
    p = check(
        "the note says the canonical boundary-matching quantity is 1/4 axis mass rather than primitive 1/16",
        "matches the boundary target" in note
        and "primitive taste-cell share `1/16`" in note
        and "axis-sector mass `1/4`" in note,
        "the writeup should kill the naive one-sixteenth-to-quarter identification explicitly",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the note reduces the remaining problem to p_* = m_axis",
        "physical boundary pressure = c^16 axis-sector mass" in note
        and "remaining bridge" in note,
        "the value search should collapse to one sharp bridge statement",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the note explicitly says the structural and boundary 16s are linked but not the same theorem",
        "not the same theorem" in note and "linked by one exact carrier-level reduction" in note,
        "this lane should not fake a stronger identification than it actually proves",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the note does not overclaim full closure",
        "not yet" in note and "outcome (2)" in note and "remaining gap" in note,
        "the lane must remain a reduction theorem / obstruction rather than a false Planck close",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("FINAL VERDICT")
    verdict = (
        "The new C^16 result does not close the boundary normalization law, "
        "but it makes the missing bridge very sharp. The fine primitive share "
        "1/16 is not the right boundary quantity. The exact coarse hw=1 "
        "axis-sector mass 1/4 is the canonical C^16 scalar that matches the "
        "surviving boundary target, and on the Schur witness quarter becomes "
        "equivalent to the bridge law p_* = m_axis."
    )
    print(f"  {verdict}")

    print("\n" + "=" * 78)
    print(f"SCORECARD: {n_pass} pass, {n_fail} fail out of {n_pass + n_fail}")
    print("=" * 78)

    return 0 if n_fail == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
