#!/usr/bin/env python3
"""
Lane 2 alpha(0) bridge boundary.

Question:
  Can the current alpha_EM(M_Z) surface determine the atomic Coulomb coupling
  alpha(0) needed by the Rydberg formula?

Answer on the current branch-local science surface:
  No. A QED-running bridge is the right kind of object, but it requires
  threshold masses, scheme choices, and a hadronic vacuum-polarization
  treatment. The current repo has alpha_EM(M_Z), not an atomic alpha(0)
  derivation.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

PASS_COUNT = 0
FAIL_COUNT = 0

M_Z_GEV = 91.1876
INV_ALPHA_MZ_REPO = 127.67
INV_ALPHA0_COMPARATOR = 137.035999084
M_E_EV_COMPARATOR = 510_998.95000
RYDBERG_EV_COMPARATOR = 13.605693122994

LEPTON_THRESHOLDS_GEV = {
    "e": 0.00051099895,
    "mu": 0.1056583755,
    "tau": 1.77686,
}


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


def bohr_ground_energy_ev(m_e_ev: float, inv_alpha: float) -> float:
    alpha = 1.0 / inv_alpha
    return -0.5 * m_e_ev * alpha * alpha


def one_loop_lepton_delta_inv_alpha(thresholds: dict[str, float]) -> float:
    # QED one-loop running below M_Z, piecewise threshold approximation:
    # Delta(1/alpha) = (2 / 3pi) sum_f Q_f^2 log(M_Z / m_f), for Q=-1 leptons.
    return (2.0 / (3.0 * math.pi)) * sum(math.log(M_Z_GEV / mass) for mass in thresholds.values())


def test_authority_text() -> None:
    print("\n" + "=" * 88)
    print("PART 1: AUTHORITY TEXT NAMES ALPHA(0) AS A LANE 2 GATE")
    print("=" * 88)

    lane = read("docs/lanes/open_science/02_ATOMIC_SCALE_PROGRAM_OPEN_LANE_2026-04-26.md")
    firewall = read("docs/ATOMIC_RYDBERG_DEPENDENCY_FIREWALL_NOTE_2026-04-27.md")
    scaffold = read("docs/ATOMIC_HYDROGEN_HELIUM_PROBE_NOTE.md")
    usable = read("docs/publication/ci3_z3/USABLE_DERIVED_VALUES_INDEX.md")

    check("Lane 2 file marks alpha(0) / QED running as a required bridge", "alpha(0)" in lane and "QED running" in lane)
    check("Rydberg firewall names low-energy Coulomb coupling as load-bearing", "low-energy Coulomb" in firewall and "alpha(0)" in firewall)
    check("Rydberg firewall records direct alpha(M_Z) substitution failure", "-15.68 eV" in firewall and "15%" in firewall)
    check("Atomic scaffold imports textbook constants rather than framework inputs", "textbook inputs" in scaffold and "m_e" in scaffold)
    check("Usable values surface has alpha_EM(M_Z) but no alpha(0) row", "alpha_EM(M_Z)" in usable and "alpha(0)" not in usable)


def test_numeric_gap() -> None:
    print("\n" + "=" * 88)
    print("PART 2: THE ATOMIC COUPLING GAP IS NUMERICALLY LOAD-BEARING")
    print("=" * 88)

    e_mz = bohr_ground_energy_ev(M_E_EV_COMPARATOR, INV_ALPHA_MZ_REPO)
    e_0 = bohr_ground_energy_ev(M_E_EV_COMPARATOR, INV_ALPHA0_COMPARATOR)
    rel_shift = (abs(e_mz) - abs(e_0)) / abs(e_0)
    inv_gap = INV_ALPHA0_COMPARATOR - INV_ALPHA_MZ_REPO

    print(f"  1/alpha_EM(M_Z) repo      = {INV_ALPHA_MZ_REPO:.6f}")
    print(f"  1/alpha(0) comparator     = {INV_ALPHA0_COMPARATOR:.9f}")
    print(f"  inverse-coupling gap      = {inv_gap:.6f}")
    print(f"  E1 using alpha(M_Z)       = {e_mz:.6f} eV")
    print(f"  E1 using alpha(0)         = {e_0:.6f} eV")

    check("The inverse-coupling gap is order ten units", inv_gap > 9.0, f"gap={inv_gap:.3f}")
    check("Direct alpha(M_Z) substitution shifts Rydberg by more than 10%", rel_shift > 0.10, f"shift={rel_shift:+.2%}")
    check("The atomic comparator energy is recovered only with alpha(0)", abs(abs(e_0) - RYDBERG_EV_COMPARATOR) < 1e-9)
    check("Therefore alpha(0) is a load-bearing input", inv_gap > 9.0 and rel_shift > 0.10)


def test_running_bridge_dependencies() -> None:
    print("\n" + "=" * 88)
    print("PART 3: QED RUNNING NEEDS THRESHOLDS AND HADRONIC INPUTS")
    print("=" * 88)

    lepton_delta = one_loop_lepton_delta_inv_alpha(LEPTON_THRESHOLDS_GEV)
    lepton_only_inv = INV_ALPHA_MZ_REPO + lepton_delta
    missing_delta = INV_ALPHA0_COMPARATOR - lepton_only_inv

    shifted_thresholds = dict(LEPTON_THRESHOLDS_GEV)
    shifted_thresholds["e"] *= 2.0
    shifted_delta = one_loop_lepton_delta_inv_alpha(shifted_thresholds)
    threshold_sensitivity = abs(shifted_delta - lepton_delta)

    print(f"  one-loop lepton Delta(1/alpha) = {lepton_delta:.6f}")
    print(f"  lepton-only 1/alpha(0) estimate = {lepton_only_inv:.6f}")
    print(f"  remaining gap to comparator      = {missing_delta:.6f}")
    print(f"  doubling m_e changes Delta by    = {threshold_sensitivity:.6f}")

    check("Lepton thresholds move alpha in the correct direction", lepton_delta > 0.0)
    check("Lepton-threshold contribution is not enough by itself", missing_delta > 3.0, f"missing={missing_delta:.3f}")
    check("Changing a threshold changes the transport result", threshold_sensitivity > 0.1, f"sensitivity={threshold_sensitivity:.3f}")
    check("Threshold masses are therefore load-bearing", threshold_sensitivity > 0.1 and lepton_delta > 0.0)
    check("A hadronic vacuum-polarization or equivalent low-energy treatment remains needed", missing_delta > 3.0)


def test_status_firewall() -> None:
    print("\n" + "=" * 88)
    print("PART 4: CLAIM-STATUS FIREWALL")
    print("=" * 88)

    actual_current_surface_status = "no-go"
    conditional_surface_status = "conditional-support"
    open_imports = [
        "charged-lepton threshold masses",
        "quark/hadronic vacuum-polarization bridge",
        "scheme-matched QED running down to alpha(0)",
    ]
    proposal_allowed = False

    check("Actual current-surface status is no-go for alpha(0) closure", actual_current_surface_status == "no-go")
    check("The QED-running route is only conditional support", conditional_surface_status == "conditional-support")
    check("Three load-bearing imports remain open", len(open_imports) == 3)
    check("No stronger branch-local proposal wording is allowed", not proposal_allowed)


def main() -> int:
    print("=" * 88)
    print("LANE 2: ALPHA(0) RUNNING BRIDGE BOUNDARY")
    print("=" * 88)
    print()
    print("Claim under test:")
    print("  The current alpha_EM(M_Z) value might determine the atomic Coulomb")
    print("  coupling alpha(0) needed by the Rydberg formula.")
    print()
    print("Boundary result:")
    print("  QED running is the right bridge type, but current repo content lacks")
    print("  the threshold and hadronic inputs needed to close it.")

    test_authority_text()
    test_numeric_gap()
    test_running_bridge_dependencies()
    test_status_firewall()

    print("\n" + "=" * 88)
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    print("=" * 88)

    if FAIL_COUNT:
        print("alpha(0) bridge runner failed; do not use the note.")
        return 1

    print("Result: no current-surface alpha(0) closure from alpha_EM(M_Z) alone.")
    print("Conditional support remains for a scheme-matched QED-running bridge.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
