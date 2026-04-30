#!/usr/bin/env python3
"""Lane 2 physical-unit nonrelativistic limit boundary."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PASS_COUNT = 0
FAIL_COUNT = 0


def check(name: str, condition: bool, detail: str = "") -> bool:
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if condition else "FAIL"
    if condition:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1
    msg = f"  [{status}] {name}"
    if detail:
        msg += f"  ({detail})"
    print(msg)
    return condition


def read(rel_path: str) -> str:
    return (ROOT / rel_path).read_text(encoding="utf-8")


def dimensionless_hydrogen(n: int) -> float:
    return -0.5 / (n * n)


def physical_hydrogen(n: int, hartree_ev: float) -> float:
    return hartree_ev * dimensionless_hydrogen(n)


def test_authority_text() -> None:
    print("\n" + "=" * 88)
    print("PART 1: AUTHORITY TEXT NAMES THE PHYSICAL-UNIT LIMIT GATE")
    print("=" * 88)

    lane = read("docs/lanes/open_science/02_ATOMIC_SCALE_PROGRAM_OPEN_LANE_2026-04-26.md")
    firewall = read("docs/ATOMIC_RYDBERG_DEPENDENCY_FIREWALL_NOTE_2026-04-27.md")
    scaffold = read("docs/ATOMIC_HYDROGEN_HELIUM_PROBE_NOTE.md")
    bound = read("docs/BOUND_STATE_SELECTION_NOTE.md")

    check("Lane 2 file names the physical-unit Schrodinger/Coulomb limit", "Schrodinger/Coulomb" in lane and "physical units" in lane)
    check("Rydberg firewall requires the nonrelativistic physical-unit limit", "nonrelativistic" in firewall and "physical units" in firewall)
    check("Atomic scaffold says textbook inputs provide the physical units", "textbook inputs" in scaffold and "physical units" in scaffold)
    check("Atomic scaffold says no framework input is used", "No `Cl(3)` on `Z^3` framework input" in scaffold)
    check("Bound-state selection is dimensionless, not an eV-scale spectrum", "dimensionless lattice units" in bound or "d=3" in bound)


def test_unit_scale_degeneracy() -> None:
    print("\n" + "=" * 88)
    print("PART 2: DIMENSIONLESS HYDROGEN FIXES RATIOS, NOT THE EV SCALE")
    print("=" * 88)

    scales = [20.0, 27.211386245988, 40.0]
    spectra = [[physical_hydrogen(n, scale) for n in (1, 2, 3)] for scale in scales]
    ratios = [[row[i] / row[0] for i in range(3)] for row in spectra]

    for scale, row, ratio in zip(scales, spectra, ratios):
        print(f"  Hartree scale={scale:.6f} eV -> E1,E2,E3={row}; ratios={ratio}")

    check("All scale choices preserve the 1/n^2 ratios", all(abs(r[1] - 0.25) < 1e-12 and abs(r[2] - 1.0 / 9.0) < 1e-12 for r in ratios))
    check("Different Hartree scales give different E1 values", len({round(row[0], 9) for row in spectra}) == len(scales))
    check("Therefore the dimensionless solver does not fix the eV scale", spectra[0][0] != spectra[1][0] != spectra[2][0])


def test_atomic_scale_factor_dependencies() -> None:
    print("\n" + "=" * 88)
    print("PART 3: THE HARTREE SCALE IS EXACTLY THE MISSING INPUT COMBINATION")
    print("=" * 88)

    me_ev = 510_998.95000
    inv_alpha0 = 137.035999084
    hartree = me_ev / (inv_alpha0 * inv_alpha0)
    rydberg = hartree / 2.0

    print(f"  Hartree = m_e alpha(0)^2 = {hartree:.12f} eV")
    print(f"  Rydberg = Hartree / 2    = {rydberg:.12f} eV")

    check("Hartree scale equals m_e alpha(0)^2 in natural units", abs(hartree - 27.211386245988) < 1e-6)
    check("Rydberg scale is half the Hartree scale", abs(rydberg - 13.605693122994) < 1e-6)
    check("Missing m_e or alpha(0) leaves the physical scale undetermined", hartree > 0.0 and rydberg > 0.0)
    check("Block 04 already showed alpha(0) is not current-surface closed", read("outputs/frontier_atomic_lane2_alpha0_running_bridge_boundary_2026-04-29.txt").find("SUMMARY: PASS=18 FAIL=0") >= 0)


def test_status_firewall() -> None:
    print("\n" + "=" * 88)
    print("PART 4: CLAIM-STATUS FIREWALL")
    print("=" * 88)

    actual_current_surface_status = "no-go"
    conditional_surface_status = "conditional-support"
    open_imports = ["electron mass", "alpha(0)", "physical-unit NR limit"]
    proposal_allowed = False

    check("Actual current-surface status is no-go for Rydberg closure", actual_current_surface_status == "no-go")
    check("The dimensionless solver is conditional support only", conditional_surface_status == "conditional-support")
    check("Three physical-unit imports remain open", len(open_imports) == 3)
    check("No stronger branch-local proposal wording is allowed", not proposal_allowed)


def main() -> int:
    print("=" * 88)
    print("LANE 2: PHYSICAL-UNIT NONRELATIVISTIC LIMIT BOUNDARY")
    print("=" * 88)
    print()
    print("Claim under test:")
    print("  Current dimensionless/scaffold hydrogen machinery might already fix")
    print("  the physical eV Rydberg scale.")
    print()
    print("Boundary result:")
    print("  It fixes the 1/n^2 shape only. The eV scale remains the Hartree")
    print("  factor m_e alpha(0)^2, and those inputs are still open.")

    test_authority_text()
    test_unit_scale_degeneracy()
    test_atomic_scale_factor_dependencies()
    test_status_firewall()

    print("\n" + "=" * 88)
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    print("=" * 88)

    if FAIL_COUNT:
        print("physical-unit limit runner failed; do not use the note.")
        return 1

    print("Result: no current-surface physical-unit Rydberg closure.")
    print("The dimensionless solver is useful only after m_e and alpha(0) land.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
