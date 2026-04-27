#!/usr/bin/env python3
"""Lane 2 Rydberg dependency firewall.

This runner checks whether the current repo state can honestly promote the
atomic hydrogen Rydberg scale to a framework-derived prediction.

Result:
  No. The standard formula is exact once the physical electron mass and the
  low-energy Coulomb coupling are supplied, but the current framework has not
  retained those atomic-scale inputs. Directly substituting the retained
  electroweak-scale alpha_EM(M_Z) for alpha(0) shifts the hydrogen ground
  energy by O(15%), so the QED running / low-energy Coulomb bridge is a
  load-bearing import, not notation.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

PASS_COUNT = 0
FAIL_COUNT = 0

ROOT = Path(__file__).resolve().parents[1]


def check(name: str, condition: bool, detail: str = "") -> bool:
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if condition else "FAIL"
    if condition:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1
    line = f"  [{status}] {name}"
    if detail:
        line += f"  ({detail})"
    print(line)
    return condition


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def section(title: str) -> None:
    print()
    print("-" * 88)
    print(title)
    print("-" * 88)


# Textbook/standard comparator constants. These are used only to measure the
# dependency firewall, not as framework-derived inputs.
M_E_TEXTBOOK_EV = 510_998.95000
ALPHA_0_INV_TEXTBOOK = 137.035999084
RYDBERG_TEXTBOOK_EV = 13.605693122994

# Current repo reusable electroweak-scale alpha from USABLE_DERIVED_VALUES_INDEX.
ALPHA_MZ_INV_REPO = 127.67

# Retained electroweak scale from USABLE_DERIVED_VALUES_INDEX.
V_EW_GEV = 246.282818290129


def bohr_ground_energy_ev(m_e_ev: float, alpha: float) -> float:
    """Hydrogen nonrelativistic ground-state energy in natural units."""
    return -0.5 * m_e_ev * alpha * alpha


def part1_standard_formula_is_ready_but_input_dependent() -> None:
    section("Part 1: standard Rydberg formula and dependency sensitivity")
    alpha0 = 1.0 / ALPHA_0_INV_TEXTBOOK
    e1 = bohr_ground_energy_ev(M_E_TEXTBOOK_EV, alpha0)
    print(f"  m_e textbook comparator       = {M_E_TEXTBOOK_EV:.5f} eV")
    print(f"  alpha(0) textbook comparator  = 1/{ALPHA_0_INV_TEXTBOOK:.9f}")
    print(f"  E_1 = -m_e alpha(0)^2 / 2     = {e1:.12f} eV")

    check(
        "standard formula reproduces the textbook Rydberg scale",
        abs(abs(e1) - RYDBERG_TEXTBOOK_EV) / RYDBERG_TEXTBOOK_EV < 1.0e-10,
        f"|E1|={abs(e1):.12f} eV",
    )
    check(
        "Rydberg scale is linear in m_e",
        abs(bohr_ground_energy_ev(2.0 * M_E_TEXTBOOK_EV, alpha0) / e1 - 2.0) < 1.0e-12,
        "doubling m_e doubles |E1|",
    )
    check(
        "Rydberg scale is quadratic in alpha",
        abs(bohr_ground_energy_ev(M_E_TEXTBOOK_EV, 2.0 * alpha0) / e1 - 4.0) < 1.0e-12,
        "doubling alpha quadruples |E1|",
    )


def part2_alpha_mz_is_not_atomic_alpha0() -> None:
    section("Part 2: alpha_EM(M_Z) direct substitution firewall")
    alpha0 = 1.0 / ALPHA_0_INV_TEXTBOOK
    alpha_mz = 1.0 / ALPHA_MZ_INV_REPO
    e_alpha0 = bohr_ground_energy_ev(M_E_TEXTBOOK_EV, alpha0)
    e_alpha_mz = bohr_ground_energy_ev(M_E_TEXTBOOK_EV, alpha_mz)
    rel_shift = (abs(e_alpha_mz) - abs(e_alpha0)) / abs(e_alpha0)
    required_me_with_alpha_mz = 2.0 * RYDBERG_TEXTBOOK_EV / (alpha_mz * alpha_mz)
    me_shift = (required_me_with_alpha_mz - M_E_TEXTBOOK_EV) / M_E_TEXTBOOK_EV

    print(f"  repo alpha_EM(M_Z)            = 1/{ALPHA_MZ_INV_REPO:.2f}")
    print(f"  direct E_1 with alpha(M_Z)    = {e_alpha_mz:.6f} eV")
    print(f"  textbook E_1 with alpha(0)    = {e_alpha0:.6f} eV")
    print(f"  relative direct-substitution shift = {rel_shift:+.2%}")
    print(f"  m_e required if alpha(M_Z) were used = {required_me_with_alpha_mz:.2f} eV")

    check(
        "direct alpha_EM(M_Z) substitution misses the Rydberg scale by > 10%",
        rel_shift > 0.10,
        f"shift={rel_shift:+.2%}",
    )
    check(
        "alpha(0) transport is load-bearing, not notation",
        abs(me_shift) > 0.10,
        f"would require m_e shift={me_shift:+.2%}",
    )
    check(
        "repo alpha_EM(M_Z) remains useful only after a low-energy bridge",
        ALPHA_MZ_INV_REPO < ALPHA_0_INV_TEXTBOOK and abs(e_alpha_mz) > abs(e_alpha0),
        "running direction gives stronger alpha at M_Z than alpha(0)",
    )


def part3_electron_mass_gate() -> None:
    section("Part 3: electron-mass activation gate")
    y_e_required = math.sqrt(2.0) * (M_E_TEXTBOOK_EV * 1.0e-9) / V_EW_GEV
    print(f"  v_EW retained scale           = {V_EW_GEV:.12f} GeV")
    print(f"  textbook m_e comparator       = {M_E_TEXTBOOK_EV * 1e-6:.9f} MeV")
    print(f"  y_e required by m = y v/sqrt(2) = {y_e_required:.12e}")

    lane2 = read("docs/lanes/open_science/02_ATOMIC_SCALE_PROGRAM_OPEN_LANE_2026-04-26.md")
    scaffold = read("docs/ATOMIC_HYDROGEN_HELIUM_PROBE_NOTE.md")
    missing_me_declared = "m_e from framework" in lane2 and "Absent" in lane2
    scaffold_imports_me = "textbook inputs" in scaffold and "m_e" in scaffold

    check(
        "Lane 2 open stub explicitly marks framework m_e as absent",
        missing_me_declared,
    )
    check(
        "current atomic scaffold imports textbook m_e",
        scaffold_imports_me,
    )
    check(
        "atomic closure therefore requires a tiny charged-lepton activation law",
        1.0e-6 < y_e_required < 1.0e-5,
        f"y_e={y_e_required:.3e}",
    )


def part4_current_claim_state() -> None:
    section("Part 4: Lane 2 claim-state consequence")
    lane2 = read("docs/lanes/open_science/02_ATOMIC_SCALE_PROGRAM_OPEN_LANE_2026-04-26.md")
    usable = read("docs/publication/ci3_z3/USABLE_DERIVED_VALUES_INDEX.md")

    has_alpha_mz = "1/alpha_EM(M_Z)" in usable and "127.67" in usable
    alpha0_not_promoted = "alpha_EM(0)" not in usable and "alpha(0)" not in usable
    lane2_says_scaffold = "scaffold-only" in lane2 and "textbook inputs" in lane2

    check(
        "repo has a reusable alpha_EM(M_Z) value, not an atomic alpha(0) closure",
        has_alpha_mz and alpha0_not_promoted,
    )
    check(
        "Lane 2 is explicitly scaffold-only before retained dependencies land",
        lane2_says_scaffold,
    )
    check(
        "honest Lane 2 status after this artifact is open, not retained closure",
        True,
        "m_e and alpha(0) bridge remain load-bearing",
    )

    print()
    print("  Exact dependency firewall:")
    print("    Hydrogen Rydberg closure requires at least:")
    print("      1. retained electron mass or y_e activation law;")
    print("      2. low-energy Coulomb alpha(0), or a QED-running bridge from alpha(M_Z);")
    print("      3. retained nonrelativistic Schrodinger/Coulomb limit in physical units.")
    print()
    print("  The existing scaffold is useful, but it is not a framework-derived")
    print("  atomic prediction until those gates are closed.")


def main() -> int:
    print("=" * 88)
    print("LANE 2 ATOMIC RYDBERG DEPENDENCY FIREWALL")
    print("=" * 88)
    print()
    print("Question:")
    print("  Can the current repo honestly claim a framework-derived hydrogen")
    print("  Rydberg scale by substituting retained high-energy quantities into")
    print("  the standard formula?")
    print()
    print("Answer:")
    print("  No. m_e and alpha(0) remain load-bearing imports.")

    part1_standard_formula_is_ready_but_input_dependent()
    part2_alpha_mz_is_not_atomic_alpha0()
    part3_electron_mass_gate()
    part4_current_claim_state()

    print()
    print("=" * 88)
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    print("=" * 88)
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())
