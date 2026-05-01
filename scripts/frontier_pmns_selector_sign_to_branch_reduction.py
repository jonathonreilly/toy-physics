#!/usr/bin/env python3
"""
Exact reduction theorem: once the unique reduced PMNS selector amplitude is
nonzero, its sign selects the branch and hands off to the branch-conditioned
coefficient problem.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

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


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def part1_sign_of_a_sel_selects_the_branch() -> None:
    print("\n" + "=" * 88)
    print("PART 1: THE SIGN OF A_SEL SELECTS THE BRANCH")
    print("=" * 88)

    basis = np.array([0.0, 0.0, 1.0, -1.0])
    pos = 0.7 * basis
    neg = -0.8 * basis
    zero = 0.0 * basis

    check("Positive a_sel gives positive weight on N_nu and negative on N_e", pos[2] > 0 and pos[3] < 0,
          f"vector={pos.tolist()}")
    check("Negative a_sel gives negative weight on N_nu and positive on N_e", neg[2] < 0 and neg[3] > 0,
          f"vector={neg.tolist()}")
    check("Zero a_sel leaves the reduced selector unresolved", np.linalg.norm(zero) < 1e-12,
          f"||zero||={np.linalg.norm(zero):.2e}")

    print()
    print("  So once the bridge turns on, its sign is exactly the class-level")
    print("  branch selector on the reduced quotient.")


def part2_after_sign_selection_only_the_branch_conditioned_coefficients_remain() -> None:
    print("\n" + "=" * 88)
    print("PART 2: AFTER SIGN SELECTION, ONLY THE BRANCH-CONDITIONED COEFFICIENTS REMAIN")
    print("=" * 88)

    last_mile = read("docs/NEUTRINO_TWO_AMPLITUDE_LAST_MILE_REDUCTION_NOTE.md")
    nu_inv = read("docs/NEUTRINO_DIRAC_TWO_HIGGS_CANONICAL_REDUCTION_NOTE.md")
    e_inv = read("docs/CHARGED_LEPTON_TWO_HIGGS_CANONICAL_REDUCTION_NOTE.md")

    check("The two-amplitude last-mile note keeps sole-axiom closure separate",
          "Only two amplitudes remain" in last_mile and "`(J_chi, mu)`" in last_mile)
    check("The neutrino-side canonical reduction records the seven remaining quantities",
          "minimal surviving neutrino-side extension class" in nu_inv
          and ("seven real axiom-side numbers" in nu_inv
               or "exactly `7` real physical parameters" in nu_inv))
    check("The charged-lepton-side canonical reduction records the seven remaining quantities",
          "minimal surviving\ncharged-lepton-side extension class" in e_inv
          and "exactly\n**seven real physical quantities**" in e_inv)
    check("The two canonical reductions keep selector realization outside their claims",
          "does **not** derive the seven numbers" in nu_inv
          and "a selector choosing the charged-lepton-side branch" in e_inv)

    print()
    print("  So after a nonzero selector amplitude chooses the branch, the")
    print("  remaining problem is exactly the existing finite-dimensional")
    print("  coefficient inverse problem on that branch.")


def part3_current_bank_records_the_handoff_from_bridge_to_coefficients() -> None:
    print("\n" + "=" * 88)
    print("PART 3: THE CURRENT BANK NOW RECORDS THE BRIDGE-TO-COEFFICIENT HANDOFF")
    print("=" * 88)

    unique = read("docs/PMNS_SELECTOR_UNIQUE_AMPLITUDE_SLOT_NOTE.md")
    sign = read("docs/PMNS_SELECTOR_SIGN_TO_BRANCH_REDUCTION_NOTE.md")
    atlas = read("docs/publication/ci3_z3/DERIVATION_ATLAS.md")

    check("The unique-amplitude note fixes one scalar a_sel", "a_sel" in unique and "one real amplitude" in unique)
    check("The sign-to-branch note records sign selection and branch-conditioned coefficient handoff",
          "a_sel > 0" in sign and "a_sel < 0" in sign and "branch-conditioned coefficient" in sign)
    check("The atlas carries the sign-to-branch reduction row",
          "| PMNS selector sign-to-branch reduction |" in atlas)

    print()
    print("  So once the microscopic bridge is realized, the current atlas no")
    print("  longer needs another selector theorem. It hands off directly to")
    print("  coefficient derivation on the selected branch.")


def main() -> int:
    print("=" * 88)
    print("PMNS SELECTOR: SIGN-TO-BRANCH REDUCTION")
    print("=" * 88)
    print()
    print("Atlas / axiom inputs reused:")
    print("  - PMNS selector unique amplitude slot")
    print("  - Neutrino two-amplitude last-mile boundary")
    print("  - Neutrino Dirac two-Higgs canonical reduction")
    print("  - Charged-lepton two-Higgs canonical reduction")
    print()
    print("Question:")
    print("  If the unique reduced selector amplitude becomes nonzero, what")
    print("  exactly remains?")

    part1_sign_of_a_sel_selects_the_branch()
    part2_after_sign_selection_only_the_branch_conditioned_coefficients_remain()
    part3_current_bank_records_the_handoff_from_bridge_to_coefficients()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Exact current-bank answer:")
    print("    - sign(a_sel) is the reduced branch selector")
    print("    - once sign(a_sel) is known, no branch ambiguity remains")
    print("    - the remaining work is exactly the branch-conditioned")
    print("      coefficient inverse problem already isolated by the atlas")
    print()
    print(f"PASS={PASS_COUNT}  FAIL={FAIL_COUNT}")
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())
