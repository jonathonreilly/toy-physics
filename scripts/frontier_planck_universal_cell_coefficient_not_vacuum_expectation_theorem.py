#!/usr/bin/env python3
"""Audit the universal-vs-vacuum classification theorem for the Planck lane.

Claim under audit:

  A universal elementary coefficient attached to the primitive physical cell
  cannot coherently be a *generic* reduced-vacuum expectation value.

What should survive:
  - the direct lane already fixes the local operator N_cell = P_A;
  - different admissible local states give different values on P_A;
  - therefore a generic state-dependent vacuum expectation is not universal;
  - scalar/free-energy vacuum observables are a negative control and do not
    land the Planck quarter.
"""

from __future__ import annotations

from itertools import product
from pathlib import Path
import sys

import sympy as sp


ROOT = Path(__file__).resolve().parents[1]
NOTE = ROOT / "docs/PLANCK_SCALE_UNIVERSAL_CELL_COEFFICIENT_NOT_VACUUM_EXPECTATION_THEOREM_2026-04-23.md"
COUNTING = ROOT / "docs/PLANCK_SCALE_WORLDTUBE_TO_BOUNDARY_CELL_COUNTING_THEOREM_LANE_2026-04-23.md"
NO_GO = ROOT / "docs/PLANCK_SCALE_SOURCE_FREE_CELL_STATE_RETAINED_DERIVATION_LANE_2026-04-23.md"
KIN = ROOT / "docs/PLANCK_SCALE_KINEMATIC_CELL_COEFFICIENT_THEOREM_CANDIDATE_2026-04-23.md"
DEFAULT = ROOT / "docs/PLANCK_SCALE_SOURCE_FREE_DEFAULT_DATUM_THEOREM_CANDIDATE_2026-04-23.md"
OBS = ROOT / "docs/PLANCK_SCALE_BOUNDARY_OBSERVABLE_PRINCIPLE_PRESSURE_IDENTIFICATION_LANE_2026-04-23.md"


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


def packet_mass(weights: dict[tuple[int, int, int, int], sp.Rational]) -> sp.Rational:
    return sum(weight for state, weight in weights.items() if sum(state) == 1)


def main() -> int:
    note = normalized(NOTE)
    counting = normalized(COUNTING)
    no_go = normalized(NO_GO)
    kin = normalized(KIN)
    default = normalized(DEFAULT)
    obs = normalized(OBS)

    states = list(product((0, 1), repeat=4))
    one_hot = [state for state in states if sum(state) == 1]
    complement = [state for state in states if sum(state) != 1]

    rho_tr = {state: sp.Rational(1, 16) for state in states}
    rho_lt = {state: sp.Rational(1, 32) for state in one_hot}
    rho_lt.update({state: sp.Rational(7, 96) for state in complement})

    alpha_tr = packet_mass(rho_tr)
    alpha_lt = packet_mass(rho_lt)
    p_vac = sp.log(sp.Rational(5, 3)) / 4

    n_pass = 0
    n_fail = 0

    print("Planck universal-cell-coefficient not-vacuum-expectation audit")
    print("=" * 78)

    section("PART 1: UPSTREAM ALIGNMENT")
    p = check(
        "the counting lane already fixes the local operator N_cell = P_A",
        "n_cell = p_a" in counting and "c_cell(rho) = tr(rho n_cell) = tr(rho p_a)" in counting,
        "the theorem should start from an already-fixed kinematic local operator",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the retained-state lane already records admissible distinct packet masses",
        "1/4" in no_go and "1/8" in no_go and "7-parameter family" in no_go,
        "generic reduced-state dependence is only relevant if distinct admissible values are already present",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the earlier kinematic note already frames the coefficient as non-vacuum in class",
        "not a dynamical vacuum-state observable" in kin
        and "the only coherent universal interpretation is" in kin,
        "the new theorem should sharpen, not reverse, the existing branch direction",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("PART 2: EXPLICIT STATE-DEPENDENCE")
    p = check(
        "the tracial witness gives the Planck quarter",
        alpha_tr == sp.Rational(1, 4),
        "Tr((I_16/16) P_A) must equal 4/16 = 1/4",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the packet-light witness gives a different coefficient",
        alpha_lt == sp.Rational(1, 8),
        "the branch needs a concrete distinct admissible local witness",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "generic Tr(rho P_A) is therefore not universal across admissible local states",
        alpha_tr != alpha_lt,
        "a universal primitive-cell coefficient cannot be identified with a generic state-dependent expectation unless another theorem fixes rho",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("PART 3: NEGATIVE CONTROL FROM THE SCALAR/VACUUM CLASS")
    p = check(
        "the scalar boundary observable note is the right negative control",
        "p_vac(l_sigma)" in obs and "1/4) log(5/3" in obs,
        "the old scalar/vacuum route should already be on record as numerically different",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the scalar/vacuum control is not the Planck quarter",
        sp.simplify(p_vac - sp.Rational(1, 4)) != 0,
        "log(5/3)/4 is exactly distinct from 1/4",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("PART 4: THEOREM CONTENT")
    p = check(
        "the new note states the correct sharp reduction",
        "generic dynamical reduced-vacuum expectation value" in note
        and "the only coherent surviving interpretations are" in note,
        "the theorem should end at a reduction: either kinematic data or a separately justified distinguished state law",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the new note does not overclaim full closure",
        "does **not** by itself prove the direct planck route fully closed" in note
        and "remaining open content is entirely in the distinguished source-free state law" in note,
        "hostile review requires keeping the state-law burden explicit",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("SUMMARY")
    print(f"Passed: {n_pass}")
    print(f"Failed: {n_fail}")
    return 0 if n_fail == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
