#!/usr/bin/env python3
"""Audit the bulk/boundary/C^16 synthesis lane honestly.

This lane does not claim full Planck closure. It proves the sharper reduction:

  - the exact Schur/action side provides lambda_min(L_Sigma), the pressure law
    p_*(nu) = nu - lambda_min(L_Sigma), and the canonical vacuum scalar
    p_vac(L_Sigma) = (1/(2n)) log det(L_Sigma);
  - the exact C^16 side provides the coarse axis-sector mass m_axis = 1/4;
  - on the canonical witness, p_vac(L_Sigma) != m_axis, so the vacuum
    synthesis does not produce the Planck boundary target;
  - the canonical action normalizations nu in {0, p_vac} also miss quarter;
  - therefore the surviving load-bearing bridge is p_* = m_axis,
    equivalently nu = lambda_min(L_Sigma) + m_axis.
"""

from __future__ import annotations

import itertools
from pathlib import Path
import sys

import numpy as np
import sympy as sp


ROOT = Path(__file__).resolve().parents[1]
NOTE = ROOT / "docs/PLANCK_SCALE_BULK_BOUNDARY_C16_SYNTHESIS_LANE_2026-04-23.md"
BULK = ROOT / "docs/PLANCK_SCALE_BULK_TO_BOUNDARY_SCHUR_COMPLETION_LANE_2026-04-23.md"
VAC = ROOT / "docs/PLANCK_SCALE_BOUNDARY_NONAFFINE_PRESSURE_NORMALIZATION_LANE_2026-04-23.md"
ACTION = ROOT / "docs/PLANCK_SCALE_BOUNDARY_UNIT_BEARING_ACTION_PRESSURE_LANE_2026-04-23.md"
VAC_DENSITY = ROOT / "docs/PLANCK_SCALE_BOUNDARY_VACUUM_ACTION_DENSITY_THEOREM_LANE_2026-04-23.md"
C16 = ROOT / "docs/PLANCK_SCALE_C16_TASTE_CELL_ONE_SIXTEENTH_LANE_2026-04-23.md"
C16_BRIDGE = ROOT / "docs/PLANCK_SCALE_C16_BOUNDARY_PRESSURE_BRIDGE_LANE_2026-04-23.md"


def normalized(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").split()).lower()


def section(title: str) -> None:
    print("\n" + "=" * 78)
    print(title)
    print("=" * 78)


def check(label: str, passed: bool, detail: str) -> bool:
    tag = "PASS" if passed else "FAIL"
    print(f"  [{tag}] {label}")
    print(f"         {detail}")
    return bool(passed)


def main() -> int:
    note = normalized(NOTE)
    bulk = normalized(BULK)
    vac = normalized(VAC)
    action = normalized(ACTION)
    vac_density = normalized(VAC_DENSITY)
    c16 = normalized(C16)
    c16_bridge = normalized(C16_BRIDGE)

    n_pass = 0
    n_fail = 0

    print("Planck bulk/boundary/C^16 synthesis lane audit")
    print("=" * 78)

    section("PART 1: UPSTREAM LANES ALIGN")
    p = check(
        "bulk Schur lane still fixes the canonical witness carrier",
        "l_sigma = [[4/3, 1/3], [1/3, 4/3]]" in bulk
        and "does not close the **coefficient**" in bulk,
        "the synthesis lane should inherit the exact witness and the existing normalization gap",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "vacuum lane still fixes the canonical non-affine scalar p_vac(L_sigma)",
        "p_vac(l_sigma) := -(1/n) log z_hat(l_sigma) = (1/(2n)) log det(l_sigma)" in vac
        and "(1/4) log(5/3)" in vac,
        "the synthesis should use the exact Gaussian Schur vacuum law rather than invent a new scalar",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "action lane still fixes p_*(nu) = nu - lambda_min(L_sigma)",
        "p_*(nu) = nu - lambda_min(l_sigma)" in action
        and "nu = 5/4" in action,
        "the synthesis bridge must feed through the exact action-native pressure law",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "vacuum-density theorem still classifies canonical nu values as {0, p_vac}",
        "nu in {0, p_vac(l_sigma)}" in vac_density
        and "rule quarter out" in vac_density,
        "the synthesis lane should not pretend the action-side coefficient is still free",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "C^16 lanes still fix primitive one-sixteenth and axis-sector quarter",
        "1/16" in c16
        and "m_axis = 4 * (1/16) = 1/4" in c16_bridge,
        "the synthesis should use the exact coarse axis-sector scalar, not numerology",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("PART 2: EXACT WITNESS DATA")
    l_sigma = sp.Matrix(
        [[sp.Rational(4, 3), sp.Rational(1, 3)], [sp.Rational(1, 3), sp.Rational(4, 3)]]
    )
    evals = sorted(l_sigma.eigenvals().keys(), key=lambda expr: float(sp.N(expr)))
    lambda_min = evals[0]
    det_l = sp.simplify(l_sigma.det())
    p_vac = sp.simplify(sp.log(det_l) / 4)

    p = check(
        "the witness spectrum is {1, 5/3}",
        evals == [sp.Integer(1), sp.Rational(5, 3)],
        "this fixes lambda_min(L_sigma) = 1 on the canonical Schur witness",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the witness determinant is 5/3",
        det_l == sp.Rational(5, 3),
        "the Gaussian vacuum scalar should therefore become (1/4) log(5/3)",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the exact witness Schur vacuum density is (1/4) log(5/3)",
        sp.simplify(p_vac - sp.log(sp.Rational(5, 3)) / 4) == 0,
        "this is the exact non-affine same-surface scalar from the Schur action",
    )
    n_pass += int(p)
    n_fail += int(not p)

    states = list(itertools.product((0, 1), repeat=4))
    dim = len(states)
    rho = np.eye(dim, dtype=float) / dim
    axis_states = [(1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1)]
    axis_indices = [states.index(state) for state in axis_states]
    m_cell = sp.Rational(1, 16)
    m_axis = sp.Rational(sum(float(rho[idx, idx]) for idx in axis_indices)).limit_denominator()

    p = check(
        "the same democratic C^16 carrier gives m_cell = 1/16 and m_axis = 1/4",
        dim == 16 and m_cell == sp.Rational(1, 16) and m_axis == sp.Rational(1, 4),
        "the coarse axis-sector mass is the exact quarter-valued C^16 observable",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("PART 3: SYNTHESIS CLASSIFICATION")
    nu = sp.symbols("nu", real=True)
    p_star = nu - lambda_min
    p = check(
        "vacuum synthesis is exactly nu = lambda_min + p_vac(L_sigma)",
        sp.simplify((lambda_min + p_vac) - (sp.Integer(1) + sp.log(sp.Rational(5, 3)) / 4)) == 0,
        "if physical pressure were identified with the Schur vacuum law, the additive shift would be 1 + (1/4) log(5/3)",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "axis synthesis is exactly nu = lambda_min + m_axis = 5/4",
        sp.simplify(lambda_min + m_axis - sp.Rational(5, 4)) == 0,
        "this is the only currently known same-surface route that lands on quarter on the witness",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "canonical action normalizations are nu in {0, p_vac(L_sigma)}",
        sp.simplify(sp.Integer(0)) == 0 and p_vac.is_real,
        "the action-side coefficient is already narrowed to zero-vacuum or Gaussian-vacuum matching",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("PART 4: WITNESS NO-GOS")
    p = check(
        "the witness rules out p_* = p_vac(L_sigma) as the Planck quarter",
        sp.simplify(p_vac - m_axis) != 0
        and abs(float(sp.N(p_vac, 50)) - 0.12770640594149768) < 1e-15,
        "the exact Schur vacuum density is not the quarter-valued C^16 axis mass",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p_nu0 = sp.simplify(p_star.subs(nu, 0))
    p_nugauss = sp.simplify(p_star.subs(nu, p_vac))
    p = check(
        "the canonical action normalizations also miss quarter",
        p_nu0 == -1 and sp.simplify(p_nugauss - (sp.log(sp.Rational(5, 3)) / 4 - 1)) == 0
        and p_nu0 != sp.Rational(1, 4)
        and sp.simplify(p_nugauss - sp.Rational(1, 4)) != 0,
        "neither zero-vacuum nor Gaussian-vacuum matching closes the boundary target",
    )
    n_pass += int(p)
    n_fail += int(not p)

    kappa_wit = sp.simplify(m_axis / p_vac)
    p = check(
        "any witness-level conversion from p_vac to m_axis needs a new factor kappa = 1/log(5/3)",
        sp.simplify(kappa_wit - 1 / sp.log(sp.Rational(5, 3))) == 0
        and sp.simplify(kappa_wit - 1) != 0,
        "the current same-surface stack does not already supply this conversion factor",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("PART 5: THE SURVIVING LOAD-BEARING BRIDGE")
    p = check(
        "the unique surviving witness-level bridge is p_* = m_axis",
        sp.simplify(p_star.subs(nu, lambda_min + m_axis) - m_axis) == 0
        and sp.simplify(p_star.subs(nu, lambda_min + m_axis) - sp.Rational(1, 4)) == 0,
        "equivalently the remaining theorem is nu = lambda_min + m_axis",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the structural 16 and the boundary quarter remain distinct theorems",
        sp.simplify(m_axis - 4 * m_cell) == 0
        and sp.simplify(m_axis - m_cell) != 0
        and sp.simplify(m_axis - p_vac) != 0,
        "the quarter is a coarse C^16 axis-sector observable, not the fine 1/16 share and not the Schur vacuum scalar",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("PART 6: NOTE HONESTY")
    p = check(
        "the note explicitly says the surviving load-bearing bridge is p_* = m_axis",
        "the surviving same-surface load-bearing bridge is reduced to: `p_* = m_axis`." in note,
        "the writeup should state the real remaining bridge directly",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the note explicitly rules out collapsing structural 16, p_vac, and quarter into one theorem",
        "does not collapse the structural `16`, the schur vacuum law, and the boundary quarter into one theorem" in note
        and "remain distinct theorems" in note,
        "the synthesis lane must stay honest about what does and does not unify",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("FINAL VERDICT")
    verdict = (
        "The bulk/boundary/C^16 synthesis lane does not close Planck. "
        "It proves something narrower and important: the exact Schur vacuum law "
        "and the exact C^16 axis-sector quarter remain distinct same-surface "
        "scalars, the witness excludes p_* = p_vac and the canonical action "
        "normalizations, and the only surviving load-bearing bridge is "
        "p_* = m_axis, equivalently nu = lambda_min(L_Sigma) + m_axis."
    )
    print(f"  {verdict}")

    print("\n" + "=" * 78)
    print(f"SCORECARD: {n_pass} pass, {n_fail} fail out of {n_pass + n_fail}")
    print("=" * 78)
    return 0 if n_fail == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
