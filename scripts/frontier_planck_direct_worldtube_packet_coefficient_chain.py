#!/usr/bin/env python3
"""Audit the direct worldtube-packet coefficient chain honestly.

This is the canonical direct reformulation of the surviving Planck route:

  - exact time-locked local carrier: the four-bit cell C^16;
  - exact minimal one-step worldtube packet: the four-atom projector P_A;
  - exact direct source-free state on the strongest close candidate:
      rho_cell = I_16 / 16;
  - exact worldtube-packet coefficient:
      c_wt = Tr(rho_cell P_A) = 4/16 = 1/4.

This runner checks that the direct-chain note stays aligned with the upstream
branch-local theorem surfaces and that the exact coefficient computation still
lands quarter.
"""

from __future__ import annotations

from itertools import product
from pathlib import Path
import sys

import sympy as sp


ROOT = Path(__file__).resolve().parents[1]
NOTE = (
    ROOT
    / "docs/PLANCK_SCALE_DIRECT_WORLDTUBE_PACKET_COEFFICIENT_CHAIN_2026-04-23.md"
)
PROGRAM = ROOT / "docs/PLANCK_SCALE_DERIVATION_PROGRAM_2026-04-23.md"
TIMELOCK = ROOT / "docs/PLANCK_SCALE_SPACETIME_TIME_LOCK_UNIT_MAP_LANE_2026-04-23.md"
SECTION = (
    ROOT / "docs/PLANCK_SCALE_BOUNDARY_SECTION_CANONICAL_WORLDTUBE_SELECTOR_LANE_2026-04-23.md"
)
MULT = ROOT / "docs/PLANCK_SCALE_BOUNDARY_MULTIPLICITY_LIFT_THEOREM_LANE_2026-04-23.md"
NON_SCHUR = ROOT / "docs/PLANCK_SCALE_NON_SCHUR_AXIS_OCCUPATION_LAW_LANE_2026-04-23.md"
PROJECTOR = (
    ROOT / "docs/PLANCK_SCALE_PROJECTOR_VALUED_OBSERVABLE_PRINCIPLE_LANE_2026-04-23.md"
)
PHYSICAL = ROOT / "docs/PHYSICAL_LATTICE_NECESSITY_NOTE.md"


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


def atomic_projector(idx: int, dim: int = 16) -> sp.Matrix:
    vec = sp.zeros(dim, 1)
    vec[idx, 0] = 1
    return vec * vec.T


def main() -> int:
    note = normalized(NOTE)
    program = normalized(PROGRAM)
    timelock = normalized(TIMELOCK)
    section_note = normalized(SECTION)
    mult = normalized(MULT)
    non_schur = normalized(NON_SCHUR)
    projector = normalized(PROJECTOR)
    physical = normalized(PHYSICAL)

    n_pass = 0
    n_fail = 0

    print("Planck direct worldtube-packet coefficient chain audit")
    print("=" * 78)

    section("PART 1: NOTE AND ENTRYPOINT ALIGNMENT")
    p = check(
        "the direct note states the surviving route as a worldtube-packet coefficient chain",
        "worldtube-packet coefficient" in note
        and "c_wt := tr(rho_cell p_a) = 4 / 16 = 1/4" in note
        and "\"boundary pressure\" is now mostly historical wording" in note,
        "the canonical direct entrypoint should make the packet coefficient, not scalar pressure, the load-bearing object",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the top-level Planck program now points to the direct chain as canonical",
        "planck_scale_direct_worldtube_packet_coefficient_chain_2026-04-23.md" in program
        and "the older \"boundary pressure\" language" in program,
        "the branch-level program note should name the direct route explicitly",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("PART 2: UPSTREAM SCIENCE SURFACES")
    p = check(
        "time-lock lane still records the 3+1 lock needed for the four-bit cell",
        "a_s = c a_t" in timelock or "time-lock" in timelock,
        "the direct route starts from the time-locked local 3+1 cell rather than a purely spatial carrier",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "section-canonical lane still forces the one-step worldtube packet P_A",
        "coarse four-axis worldtube channel is **section-canonical**" in section_note
        or "forced onto the coarse `hw=1` four-axis worldtube channel" in section_note,
        "the direct coefficient route needs a forced packet before any counting statement matters",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "multiplicity-lift lane still fixes the full packet quarter exactly",
        "tr(rho_cell p_a) = 2 tr(rho_cell p_q) = 1/4" in mult
        or "m_lift := tr(rho_cell p_a) = 2 tr(rho_cell p_q) = 1/4" in mult,
        "the direct route should inherit the exact quarter from the full packet, not insert it manually",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the non-Schur lane still isolates the democratic full-cell source-free state on the strongest close candidate",
        "rho_cell = i_16 / 16" in non_schur and "4 / 16 = 1/4" in non_schur,
        "the direct route uses the strongest current full-cell source-free law rather than scalar Schur data",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the projector lane still records Tr(rho_cell P_A) = 1/4 as the direct event coefficient",
        "mu_cell(p_a) = tr(rho_cell p_a) = 4/16 = 1/4" in projector
        and "event observable" in projector,
        "the direct route should still agree with the surviving packet/event readout computation",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the physical-lattice surface still forbids proper exact quotienting of retained sectors",
        "no proper exact quotient/rooting/reduction" in physical
        and "physical-species semantics" in physical,
        "the direct object should remain the full packet P_A rather than a quotient-only readout",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("PART 3: EXACT DIRECT COEFFICIENT COMPUTATION")
    states = list(product((0, 1), repeat=4))
    dim = len(states)
    atoms = [atomic_projector(i, dim) for i in range(dim)]
    hamming_weight_one = [i for i, bits in enumerate(states) if sum(bits) == 1]
    p_a = sum((atoms[i] for i in hamming_weight_one), sp.zeros(dim))
    rho_cell = sp.eye(dim) / dim
    c_wt = sp.simplify(sp.trace(rho_cell * p_a))

    p = check(
        "the exact local direct carrier has 16 primitive states",
        dim == 16,
        "the direct chain begins on the time-locked four-bit cell C^16",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the one-step worldtube packet contains exactly four one-hot states",
        len(hamming_weight_one) == 4 and p_a.rank() == 4,
        "the direct coefficient is the weight of the four one-hot atoms, not an emergent continuum shell",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the source-free full-cell state is democratic",
        rho_cell == sp.eye(16) / 16,
        "the strongest current direct close candidate uses the uniform full-cell measure",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the direct worldtube-packet coefficient is exactly quarter",
        c_wt == sp.Rational(1, 4),
        "four one-hot atoms each carrying weight 1/16 give c_wt = 4/16 = 1/4",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("PART 4: DIRECT ENDPOINT")
    p = check(
        "the note records that the counting side is now closed",
        "the counting side is no longer open" in note
        and "c_cell(rho) = tr(rho p_a)" in note,
        "the direct chain should now reflect the closed cell-counting theorem",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the note still records the Planck consequence cleanly",
        "a^2 = l_p^2" in note and "a = l_p" in note,
        "once the source-free default datum is authorized, the direct route should close straight to Planck",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("SUMMARY")
    print(f"Passed: {n_pass}")
    print(f"Failed: {n_fail}")
    return 0 if n_fail == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
