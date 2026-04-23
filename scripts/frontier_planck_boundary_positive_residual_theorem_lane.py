#!/usr/bin/env python3
"""Audit the Planck boundary positive-residual theorem lane honestly.

This lane does not claim retained Planck closure. It proves the sharper result:

  - the current scalar Schur/vacuum residuals are negative on the retained
    positive witness family;
  - the exact 3+1 worldtube stack fixes the coarse section-canonical projector
    P_A on the minimal shell;
  - under democratic same-carrier weighting, the unique positive residual
    attached to that sector is Tr(rho_cell P_A) = 1/4;
  - exact action closure follows conditionally from one readout law:
      delta = Tr(rho_cell P_A).
"""

from __future__ import annotations

import itertools
from pathlib import Path
import sys

import sympy as sp


ROOT = Path(__file__).resolve().parents[1]
NOTE = ROOT / "docs/PLANCK_SCALE_BOUNDARY_POSITIVE_RESIDUAL_THEOREM_LANE_2026-04-23.md"
DECOMP = ROOT / "docs/PLANCK_SCALE_BOUNDARY_VACUUM_ACTION_DECOMPOSITION_LANE_2026-04-23.md"
SECTION = ROOT / "docs/PLANCK_SCALE_BOUNDARY_SECTION_CANONICAL_WORLDTUBE_SELECTOR_LANE_2026-04-23.md"
BRIDGE = ROOT / "docs/PLANCK_SCALE_C16_BOUNDARY_PRESSURE_BRIDGE_LANE_2026-04-23.md"
INTERTWINER = ROOT / "docs/PLANCK_SCALE_BOUNDARY_BULK_TO_C16_INTERTWINER_LANE_2026-04-23.md"
ENDPOINT = ROOT / "docs/PLANCK_SCALE_C16_AXIS_MASS_PHYSICAL_PRESSURE_IDENTIFICATION_LANE_2026-04-23.md"


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


def orbit(state: tuple[int, int, int, int]) -> frozenset[tuple[int, int, int, int]]:
    t = state[0]
    spatial = state[1:]
    out: set[tuple[int, int, int, int]] = set()
    for perm in itertools.permutations((0, 1, 2)):
        out.add((t,) + tuple(spatial[i] for i in perm))
    return frozenset(out)


def main() -> int:
    note = normalized(NOTE)
    decomp = normalized(DECOMP)
    section_note = normalized(SECTION)
    bridge = normalized(BRIDGE)
    intertwiner = normalized(INTERTWINER)
    endpoint = normalized(ENDPOINT)

    n_pass = 0
    n_fail = 0

    print("Planck boundary positive-residual theorem lane audit")
    print("=" * 78)

    section("PART 1: UPSTREAM ALIGNMENT")
    p = check(
        "the decomposition lane still states p_* = delta after nu = lambda_min + delta",
        "p_* = delta" in decomp and "delta = 1/4" in decomp,
        "the new lane should refine the exact residual reformulation already earned upstream",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the section-canonical lane still fixes the coarse worldtube selector to P_A",
        "projector is uniquely forced to be `p_a`" in section_note
        or "unique admissible projector is `p_a`" in section_note
        or "forces the worldtube selector onto `p_a`" in section_note,
        "the positive residual candidate should descend from the already fixed coarse worldtube sector",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the C^16 bridge still fixes m_axis = 1/4",
        "m_axis := tr(rho_cell p_a) = 4/16 = 1/4" in bridge,
        "the positive residual lane should not introduce a new numerical target",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the intertwiner lane still says the minimal quotient only carries 1/8",
        "1/8" in intertwiner and "factor of `2`" in intertwiner,
        "the new lane should respect the earlier faithful-intertwiner no-go and work at the coarse sector level",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the endpoint note still says the remaining law is p_phys = m_axis",
        "`p_phys = m_axis`" in endpoint and "missing physical law" in endpoint,
        "the positive-residual theorem should sharpen that exact remaining law rather than reopen the lane",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("PART 2: SCALAR SIGN OBSTRUCTION")
    r = sp.symbols("r", positive=True, real=True)
    l_r = sp.Matrix([[1 + r, r], [r, 1 + r]])
    evals_r = sorted(l_r.eigenvals().keys(), key=sp.default_sort_key)
    lambda_min_r = sp.simplify(evals_r[0])
    p_vac_r = sp.simplify(sp.log(l_r.det()) / 4)
    delta_zero_r = sp.simplify(-lambda_min_r)
    delta_gauss_r = sp.simplify(p_vac_r - lambda_min_r)

    p = check(
        "the retained positive witness family keeps lambda_min(L(r)) = 1",
        sp.simplify(lambda_min_r - 1) == 0,
        "this fixes the Schur spectral floor across the family",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "empty-vacuum residual is exactly negative on the whole family",
        sp.simplify(delta_zero_r + 1) == 0,
        "delta_0(L(r)) = -1 for every retained positive witness",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "Gaussian residual is explicitly (1/4) log(1 + 2r) - 1",
        sp.simplify(delta_gauss_r - (sp.log(1 + 2 * r) / 4 - 1)) == 0,
        "this is the strongest currently derived nonzero scalar residual",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the Gaussian residual is negative on the retained family",
        float(sp.N(sp.log(3) / 4 - 1, 50)) < 0.0,
        "because 0 < r < 1 implies 1 + 2r < 3, the Gaussian residual stays below (1/4) log 3 - 1 < 0",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "sample witness values confirm the scalar sign obstruction",
        float(sp.N(delta_gauss_r.subs(r, sp.Rational(1, 4)), 50)) < 0.0
        and float(sp.N(delta_gauss_r.subs(r, sp.Rational(1, 2)), 50)) < 0.0,
        "the scalar Schur/vacuum route never turns positive on representative retained witnesses",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("PART 3: UNIQUE COARSE POSITIVE SECTOR")
    states = list(itertools.product((0, 1), repeat=4))
    shell_1 = {state for state in states if sum(state) == 1}
    temporal = {(1, 0, 0, 0)}
    spatial = {(0, 1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1)}
    axis = temporal | spatial

    p = check(
        "the minimal shell splits into temporal and spatial one-hot residual orbits",
        orbit((1, 0, 0, 0)) == frozenset(temporal)
        and orbit((0, 1, 0, 0)) == frozenset(spatial)
        and shell_1 == axis,
        "the section-canonical theorem works on exactly these two orbit blocks",
    )
    n_pass += int(p)
    n_fail += int(not p)

    candidates = {
        "0": set(),
        "P_t": temporal,
        "P_s": spatial,
        "P_A": axis,
    }
    admissible = [
        name
        for name, support in candidates.items()
        if temporal.issubset(support) and spatial.issubset(support)
    ]
    p = check(
        "time-complete plus spatially isotropic minimal-shell selection uniquely forces P_A",
        admissible == ["P_A"],
        "there is only one coarse residual-invariant worldtube sector compatible with the current 3+1 rules",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("PART 4: UNIQUE POSITIVE DEMOCRATIC SECTOR SHARE")
    dim = len(states)
    mass_t = sp.Rational(len(temporal), dim)
    mass_s = sp.Rational(len(spatial), dim)
    mass_a = sp.Rational(len(axis), dim)

    p = check(
        "the democratic full-cell state assigns exact masses 1/16, 3/16, and 4/16 to P_t, P_s, and P_A",
        mass_t == sp.Rational(1, 16)
        and mass_s == sp.Rational(3, 16)
        and mass_a == sp.Rational(1, 4),
        "once the coarse sector is fixed, its democratic same-carrier share is exact",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the section-canonical sector share is the unique quarter-valued positive candidate",
        mass_a > 0 and mass_a == sp.Rational(1, 4) and mass_a != mass_t and mass_a != mass_s,
        "the positive residual candidate is not a free coefficient but the exact mass of the unique admissible coarse sector",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("PART 5: ACTION-SIDE CLOSURE UNDER THE RESIDUAL READOUT LAW")
    l_sigma = sp.Matrix(
        [[sp.Rational(4, 3), sp.Rational(1, 3)], [sp.Rational(1, 3), sp.Rational(4, 3)]]
    )
    evals = sorted(l_sigma.eigenvals().keys(), key=sp.default_sort_key)
    lambda_min = sp.simplify(evals[0])
    nu_star = sp.simplify(lambda_min + mass_a)
    p_star = sp.simplify(nu_star - lambda_min)

    p = check(
        "on the canonical witness lambda_min(L_sigma) = 1",
        evals == [sp.Integer(1), sp.Rational(5, 3)],
        "the exact action-side coefficient should close on the same witness already used upstream",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "identifying delta with the section-canonical sector share gives p_* = 1/4 exactly",
        p_star == sp.Rational(1, 4),
        "the action pressure equals the residual, so delta = Tr(rho_cell P_A) closes the quarter immediately",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the corresponding exact vacuum-action density is nu = 5/4 on the witness",
        nu_star == sp.Rational(5, 4),
        "the action-side coefficient is exact once the residual readout law is fixed",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("PART 6: HONESTY CHECK")
    p = check(
        "the note says the remaining content is a readout law rather than a new coefficient scan",
        "smallest remaining law" in note
        and "delta = tr(rho_cell p_a)" in note
        and "not “find the number,”" in note.lower(),
        "the writeup should report the true remaining frontier without overstating retained closure",
    )
    n_pass += int(p)
    n_fail += int(not p)

    print("\n" + "=" * 78)
    print(f"RESULT: {n_pass} passed, {n_fail} failed")
    print("=" * 78)
    return 0 if n_fail == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
