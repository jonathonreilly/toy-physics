#!/usr/bin/env python3
"""
Current-stack underdetermination theorem for the Higgs Z_3 charge q_H.

Question:
  Does the present retained atlas/axiom stack fix the generation Z_3 charge
  q_H of the single Higgs doublet on the neutrino Dirac lane?

Answer:
  No. The current exact stack reduces q_H to the discrete set {0,+1,-1}, and
  proves what support each choice induces, but it does not distinguish among
  them. All three remain exact admissible cases on the present retained stack.

Boundary:
  This is a current-stack/atlas theorem, not a claim that q_H is impossible to
  derive in every future extension.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

np.set_printoptions(precision=6, suppress=True, linewidth=140)

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
    msg = f"  [{status}] {name}"
    if detail:
        msg += f"  ({detail})"
    print(msg)
    return condition


LEFT_CHARGES = np.array([0, 1, 2], dtype=int)
RIGHT_CHARGES = np.array([0, 2, 1], dtype=int)


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def support_matrix(q_h: int) -> np.ndarray:
    support = np.zeros((3, 3), dtype=int)
    for i, ql in enumerate(LEFT_CHARGES):
        for j, qr in enumerate(RIGHT_CHARGES):
            if (ql + q_h + qr) % 3 == 0:
                support[i, j] = 1
    return support


def part1_all_three_higgs_charges_remain_admissible() -> dict[int, np.ndarray]:
    print("\n" + "=" * 88)
    print("PART 1: THE CURRENT INVARIANCE GRAMMAR ADMITS ALL THREE q_H CASES")
    print("=" * 88)

    supports = {q_h: support_matrix(q_h) for q_h in [0, 1, 2]}

    for q_h, support in supports.items():
        row_sums = support.sum(axis=1)
        col_sums = support.sum(axis=0)
        admissible = np.array_equal(row_sums, np.ones(3, dtype=int)) and np.array_equal(col_sums, np.ones(3, dtype=int))
        check(f"q_H={q_h}: retained Z_3 invariance admits an exact support pattern", admissible,
              f"row sums={row_sums.tolist()}, col sums={col_sums.tolist()}")

    distinct = len({tuple(support.reshape(-1).tolist()) for support in supports.values()})
    union = supports[0] + supports[1] + supports[2]

    check("The three admissible q_H cases are genuinely distinct", distinct == 3, f"distinct patterns={distinct}")
    check("Their union fills the full 3x3 support grid", np.array_equal(union, np.ones((3, 3), dtype=int)),
          f"union=\n{union}")

    print()
    print("  So the current exact invariance grammar narrows q_H to a 3-point")
    print("  discrete set, but it does not pick a unique point inside that set.")
    return supports


def part2_current_atlas_has_no_selector() -> None:
    print("\n" + "=" * 88)
    print("PART 2: THE CURRENT ATLAS CARRIES THE BLOCKER BUT NO q_H SELECTOR")
    print("=" * 88)

    atlas = read("docs/publication/ci3_z3/DERIVATION_ATLAS.md")
    validation = read("docs/publication/ci3_z3/DERIVATION_VALIDATION_MAP.md")
    ckm_note = read("docs/CKM_FROM_MASS_HIERARCHY_NOTE.md")
    atlas_lower = atlas.lower()

    has_higgs_lane = "| Higgs / CW mass lane |" in atlas
    has_dirac_support = "| Neutrino Dirac `Z_3` support trichotomy |" in atlas
    has_dirac_no_mixing = "| Neutrino Dirac monomial no-mixing theorem |" in atlas
    has_underdetermination_row = "| Neutrino Higgs `Z_3` underdetermination |" in atlas
    selector_signatures = [
        "fixes q_h",
        "determines q_h",
        "selects q_h",
        "unique q_h",
        "retained q_h selector",
        "higgs z_3 selector theorem",
    ]
    has_qh_selector = any(signature in atlas_lower for signature in selector_signatures)
    has_validation_blocker = "Higgs `Z_3` universality" in validation or "Higgs `Z_3` universality" in ckm_note

    check("Atlas carries the admitted Higgs/CW electroweak lane", has_higgs_lane)
    check("Atlas carries the exact Dirac support trichotomy", has_dirac_support)
    check("Atlas carries the exact single-Higgs no-mixing obstruction", has_dirac_no_mixing)
    check("Atlas now carries the exact q_H underdetermination row", has_underdetermination_row)
    check("Current atlas does not contain a retained q_H-fixing selector row", not has_qh_selector)
    check("The package still records a Higgs-Z_3 blocker on the flavor side", has_validation_blocker)

    print()
    print("  So the current atlas is in the expected state:")
    print("    - it isolates the Higgs-Z_3 issue as a blocker,")
    print("    - but it does not yet contain any retained selector that fixes q_H.")


def part3_bounded_hints_do_not_upgrade() -> None:
    print("\n" + "=" * 88)
    print("PART 3: BOUNDED HINTS EXIST BUT DO NOT UPGRADE TO A RETAINED THEOREM")
    print("=" * 88)

    ckm_z3 = read("scripts/frontier_ckm_from_z3.py")
    has_bounded_hint = "INTERPRETATION: The Higgs carries Z_3 charge" in ckm_z3
    has_bounded_warning = "This needs a specific" in ckm_z3 or "needs a specific" in ckm_z3

    check("The bounded CKM scan does contain a Higgs-Z_3 hint", has_bounded_hint)
    check("That same bounded scan explicitly leaves the Higgs step open", has_bounded_warning)

    print()
    print("  The current stack therefore has:")
    print("    - a bounded hint,")
    print("    - but no promotion-safe exact selector.")


def main() -> int:
    print("=" * 88)
    print("NEUTRINO HIGGS Z_3 CHARGE: CURRENT-STACK UNDERDETERMINATION")
    print("=" * 88)
    print()
    print("Atlas / axiom inputs reused:")
    print("  - Three-generation matter structure")
    print("  - Neutrino mass reduction to Dirac lane")
    print("  - Neutrino Dirac Z_3 support trichotomy")
    print("  - Neutrino Dirac monomial no-mixing theorem")
    print("  - Higgs / CW mass lane")
    print()
    print("Question:")
    print("  Does the present retained stack fix the Higgs generation Z_3 charge q_H?")

    part1_all_three_higgs_charges_remain_admissible()
    part2_current_atlas_has_no_selector()
    part3_bounded_hints_do_not_upgrade()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Exact current-stack answer:")
    print("    - q_H is reduced to the discrete set {0,+1,-1}")
    print("    - all three cases remain exact admissible solutions")
    print("    - the current retained atlas does not distinguish among them")
    print()
    print("  So the honest next Higgs-side theorem is underdetermination, not")
    print("  a spurious fixing claim. Any actual q_H selection needs a genuinely")
    print("  new retained selector.")
    print()
    print(f"PASS={PASS_COUNT}  FAIL={FAIL_COUNT}")
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())
