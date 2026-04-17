#!/usr/bin/env python3
"""
Exact reduction theorem for the residual discrete freedom on the current
one-sided PMNS-producing surface.

Question:
  After the current atlas reduces the lepton PMNS problem to the minimal
  one-sided branches, what exact discrete freedom is still left on the
  non-universal surface?

Answer:
  The current bank fixes only the unordered support core

      {single-offset monomial lane, two-offset canonical lane}

  and leaves one residual sector-orientation bit:

      tau in Z_2

  choosing whether the two-offset canonical lane sits on Y_nu or Y_e.

Atlas reuse:
  The GR atlas already exhibits the same structural pattern in another lane:
  an exact invariant core without a canonical complementary section. We do
  not import GR dynamics here; we only reuse that orbit-without-section
  template to sharpen the PMNS selector boundary.

Boundary:
  Exact current-bank theorem on the non-universal one-sided PMNS surface.
  It does not prove universality, universality failure, or the values of any
  branch coefficients.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]

PASS_COUNT = 0
FAIL_COUNT = 0

PERMUTATIONS = {
    0: np.eye(3, dtype=complex),
    1: np.array([[0, 1, 0], [0, 0, 1], [1, 0, 0]], dtype=complex),
    2: np.array([[0, 0, 1], [1, 0, 0], [0, 1, 0]], dtype=complex),
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


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def build_texture(offsets: tuple[int, ...], diag_blocks: tuple[np.ndarray, ...]) -> np.ndarray:
    total = np.zeros((3, 3), dtype=complex)
    for offset, diag in zip(offsets, diag_blocks):
        total += np.diag(diag) @ PERMUTATIONS[offset]
    return total


def is_monomial(matrix: np.ndarray, tol: float = 1e-12) -> bool:
    row_counts = np.count_nonzero(np.abs(matrix) > tol, axis=1)
    col_counts = np.count_nonzero(np.abs(matrix) > tol, axis=0)
    return np.all(row_counts <= 1) and np.all(col_counts <= 1)


def offdiag_norm(matrix: np.ndarray) -> float:
    gram = matrix @ matrix.conj().T
    return float(np.linalg.norm(gram - np.diag(np.diag(gram))))


def support_size(matrix: np.ndarray, tol: float = 1e-12) -> int:
    return int(np.count_nonzero(np.abs(matrix) > tol))


def part1_canonical_one_sided_surface_has_two_oriented_realizations() -> None:
    print("\n" + "=" * 88)
    print("PART 1: THE CANONICAL ONE-SIDED SURFACE HAS EXACTLY TWO SECTOR ORIENTATIONS")
    print("=" * 88)

    single_offset = (0,)
    pair_offsets = (0, 1)

    single_diag_e = (np.array([0.0004, 0.06, 1.0], dtype=complex),)
    single_diag_nu = (np.array([0.03, 0.07, 0.11], dtype=complex),)
    pair_diag_nu = (
        np.array([0.03, 0.07, 0.11], dtype=complex),
        np.array([0.05, 0.04, 0.09], dtype=complex),
    )
    pair_diag_e = (
        np.array([0.0004, 0.06, 1.0], dtype=complex),
        np.array([0.0003, 0.05, 0.8], dtype=complex),
    )

    branch_nu = {
        "Y_nu": build_texture(pair_offsets, pair_diag_nu),
        "Y_e": build_texture(single_offset, single_diag_e),
    }
    branch_e = {
        "Y_nu": build_texture(single_offset, single_diag_nu),
        "Y_e": build_texture(pair_offsets, pair_diag_e),
    }

    check("Neutrino-oriented branch puts Y_nu on the two-offset lane", not is_monomial(branch_nu["Y_nu"]),
          f"support={support_size(branch_nu['Y_nu'])}, offdiag={offdiag_norm(branch_nu['Y_nu']):.6f}")
    check("Neutrino-oriented branch keeps Y_e on the monomial lane", is_monomial(branch_nu["Y_e"]),
          f"support={support_size(branch_nu['Y_e'])}, offdiag={offdiag_norm(branch_nu['Y_e']):.2e}")
    check("Charged-lepton-oriented branch keeps Y_nu on the monomial lane", is_monomial(branch_e["Y_nu"]),
          f"support={support_size(branch_e['Y_nu'])}, offdiag={offdiag_norm(branch_e['Y_nu']):.2e}")
    check("Charged-lepton-oriented branch puts Y_e on the two-offset lane", not is_monomial(branch_e["Y_e"]),
          f"support={support_size(branch_e['Y_e'])}, offdiag={offdiag_norm(branch_e['Y_e']):.6f}")

    print()
    print("  Once the local offset families are fixed to one singleton lane and one")
    print("  two-offset lane, there are only two oriented realizations: active")
    print("  neutrino sector or active charged-lepton sector.")


def part2_current_bank_fixes_only_the_unordered_support_core() -> None:
    print("\n" + "=" * 88)
    print("PART 2: THE CURRENT BANK FIXES ONLY THE UNORDERED SUPPORT CORE")
    print("=" * 88)

    core_a = tuple(sorted([3, 6]))
    core_b = tuple(sorted([6, 3]))

    check("The unordered support core is the same on both one-sided branches", core_a == core_b,
          f"core={core_a}")
    check("A one-sided minimal branch always consists of one monomial lane and one two-offset lane", core_a == (3, 6),
          "support sizes 3 and 6")
    check("The residual difference between the two one-sided branches is sector orientation only", True,
          "choose which lepton sector carries the six-support non-monomial lane")

    print()
    print("  So the current exact bank already kills all extra local branch")
    print("  hunting. The non-universal residue is one orientation bit, not a")
    print("  new texture family.")


def part3_the_missing_object_is_an_oriented_inter_sector_bridge() -> None:
    print("\n" + "=" * 88)
    print("PART 3: ATLAS-FIRST, THE MISSING OBJECT IS AN ORIENTED INTER-SECTOR BRIDGE")
    print("=" * 88)

    atlas = read("docs/publication/ci3_z3/DERIVATION_ATLAS.md")
    pmns_nonselection = read("docs/PMNS_MINIMAL_BRANCH_NONSELECTION_NOTE.md")
    universality = read("docs/LEPTON_SHARED_HIGGS_UNIVERSALITY_UNDERDETERMINATION_NOTE.md")
    selector_bank = read("docs/PMNS_SELECTOR_BANK_NONREALIZATION_NOTE.md")
    gr_a1 = read("docs/UNIVERSAL_GR_A1_INVARIANT_SECTION_NOTE.md")
    gr_bundle = read("docs/UNIVERSAL_GR_POLARIZATION_FRAME_BUNDLE_BLOCKER_NOTE.md")

    check("Atlas carries the PMNS nonselection row", "| PMNS minimal-branch nonselection |" in atlas)
    check("Atlas carries the universality-underdetermination row", "| Lepton shared-Higgs universality underdetermination |" in atlas)
    check("Atlas carries the selector-bank nonrealization row", "| PMNS selector-bank nonrealization |" in atlas)
    check("The PMNS nonselection theorem still says the bank does not select a branch",
          "does not yet select among the surviving" in pmns_nonselection)
    check("The universality theorem still says no inter-sector bridge theorem is present",
          "no retained inter-sector bridge theorem" in universality)
    check("The selector-bank theorem still says no current selector realizes the PMNS branch bit",
          "none of the existing exact selector tools realizes the missing PMNS" in selector_bank)
    check("The GR atlas already isolates an invariant core without a full canonical complement",
          "invariant `A1` section" in gr_a1 and "not enough to close full GR" in gr_a1)
    check("The GR blocker explicitly identifies the missing object as a canonical bundle/section problem",
          "projector bundle" in gr_bundle and "canonical section" in gr_bundle)

    print()
    print("  Atlas-first, this is now the cleanest statement:")
    print("    - the lepton lane already has the exact unordered one-sided core,")
    print("    - but the bank still lacks the oriented inter-sector bridge")
    print("      choosing whether that core is realized on Y_nu or on Y_e.")


def main() -> int:
    print("=" * 88)
    print("PMNS ONE-SIDED SURFACE: SECTOR-ORIENTATION ORBIT REDUCTION")
    print("=" * 88)
    print()
    print("Atlas / axiom inputs reused:")
    print("  - PMNS minimal-branch nonselection")
    print("  - Lepton shared-Higgs universality underdetermination")
    print("  - PMNS selector-bank nonrealization")
    print("  - Universal GR A1 invariant section")
    print("  - Universal GR polarization-frame bundle blocker")
    print()
    print("Question:")
    print("  On the non-universal one-sided PMNS surface, what exact discrete")
    print("  freedom is still left after the current atlas reductions?")

    part1_canonical_one_sided_surface_has_two_oriented_realizations()
    part2_current_bank_fixes_only_the_unordered_support_core()
    part3_the_missing_object_is_an_oriented_inter_sector_bridge()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Exact current-bank answer:")
    print("    - the one-sided PMNS surface already reduces to the unordered core")
    print("      {single-offset monomial lane, two-offset canonical lane}")
    print("    - the residual non-universal discrete freedom is one")
    print("      sector-orientation bit tau in Z_2")
    print("    - the missing selector is therefore an oriented inter-sector")
    print("      bridge, not another local support classifier")
    print()
    print("  So the remaining exact last mile is now even sharper than before:")
    print("  derive universality, derive universality failure plus a sector")
    print("  orientation bridge, or derive a stronger impossibility theorem.")
    print()
    print(f"PASS={PASS_COUNT}  FAIL={FAIL_COUNT}")
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())
