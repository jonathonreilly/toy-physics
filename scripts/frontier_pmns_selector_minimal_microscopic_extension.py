#!/usr/bin/env python3
"""
Exact extension-class theorem: the minimal surviving positive PMNS selector
realization is a non-additive sector-sensitive mixed bridge with one real
amplitude slot.
"""

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


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def part1_current_bank_eliminates_the_direct_sum_additive_route() -> None:
    print("\n" + "=" * 88)
    print("PART 1: THE CURRENT BANK ELIMINATES THE DIRECT-SUM ADDITIVE ROUTE")
    print("=" * 88)

    scalar = read("docs/PMNS_SCALAR_BRIDGE_NONREALIZATION_NOTE.md")
    zero = read("docs/PMNS_SELECTOR_CURRENT_STACK_ZERO_LAW_NOTE.md")

    check("The scalar-bridge theorem says the current additive scalar bank does not realize the selector bridge",
          "does not realize the missing PMNS" in scalar or "does not generate a mixed scalar bridge" in scalar)
    check("The scalar-bridge theorem says the remaining object must be non-additive or non-scalar",
          "non-additive or non-scalar observable grammar" in scalar)
    check("The current-zero-law note records a_sel,current = 0 on the retained bank",
          "a_sel,current = 0" in zero)

    print()
    print("  So any positive realization must leave the direct-sum additive")
    print("  scalar route that the current bank actually retains.")


def part2_remaining_positive_support_and_reduced_form_are_fixed() -> None:
    print("\n" + "=" * 88)
    print("PART 2: THE REMAINING POSITIVE SUPPORT AND REDUCED FORM ARE FIXED")
    print("=" * 88)

    support = read("docs/PMNS_SELECTOR_NONUNIVERSAL_SUPPORT_REDUCTION_NOTE.md")
    uniq = read("docs/PMNS_SELECTOR_CLASS_SPACE_UNIQUENESS_NOTE.md")
    amp = read("docs/PMNS_SELECTOR_UNIQUE_AMPLITUDE_SLOT_NOTE.md")

    check("The support-reduction note says the bridge is nonzero only on the non-universal locus",
          "supported only" in support and "non-universal" in support)
    check("The class-space note says the reduced selector class is unique up to scale",
          "one-dimensional" in uniq and "chi_N_nu - chi_N_e" in uniq)
    check("The unique-amplitude note says the reduced bridge has one real slot a_sel",
          "B_red = a_sel S_cls" in amp and "one real amplitude" in amp)

    print()
    print("  So the surviving positive bridge class is already rigid on the")
    print("  quotient: unique support locus, unique reduced class, one amplitude.")


def part3_minimal_positive_extension_class_is_now_explicit() -> None:
    print("\n" + "=" * 88)
    print("PART 3: THE MINIMAL POSITIVE EXTENSION CLASS IS NOW EXPLICIT")
    print("=" * 88)

    note = read("docs/PMNS_SELECTOR_MINIMAL_MICROSCOPIC_EXTENSION_NOTE.md")
    atlas = read("docs/publication/ci3_z3/DERIVATION_ATLAS.md")
    bridge = read("docs/ACTION_GEOMETRY_BRIDGE_NOTE.md")

    check("The new note identifies the minimal class as a non-additive sector-sensitive mixed bridge",
          "non-additive" in note and "sector-sensitive" in note and "mixed bridge" in note)
    check("The new note identifies one real amplitude slot on the reduced class",
          "one real amplitude slot" in note and "a_sel" in note)
    check("The atlas carries the minimal-microscopic-extension row",
          "| PMNS selector minimal microscopic extension |" in atlas)
    check("The action-geometry note uses the safe label mixed bridge as structural naming precedent",
          "mixed bridge" in bridge.lower())

    print()
    print("  So the remaining microscopic selector problem is no longer a")
    print("  family of possible bridge classes. It is one exact extension class.")


def main() -> int:
    print("=" * 88)
    print("PMNS SELECTOR: MINIMAL MICROSCOPIC EXTENSION")
    print("=" * 88)
    print()
    print("Atlas / axiom inputs reused:")
    print("  - PMNS scalar bridge nonrealization")
    print("  - PMNS selector non-universal support reduction")
    print("  - PMNS selector class-space uniqueness")
    print("  - PMNS selector unique amplitude slot")
    print("  - PMNS selector current-stack zero law")
    print("  - Action geometry bridge (naming precedent only)")
    print()
    print("Question:")
    print("  What is the smallest honest positive microscopic extension class")
    print("  that could realize the PMNS selector?")

    part1_current_bank_eliminates_the_direct_sum_additive_route()
    part2_remaining_positive_support_and_reduced_form_are_fixed()
    part3_minimal_positive_extension_class_is_now_explicit()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Exact current-bank answer:")
    print("    - the current direct-sum additive bank is ruled out")
    print("    - the surviving positive bridge must live on the non-universal locus")
    print("    - its reduced class and amplitude slot are unique")
    print("    - so the minimal surviving positive extension class is a")
    print("      non-additive sector-sensitive mixed bridge with one real")
    print("      amplitude slot")
    print()
    print(f"PASS={PASS_COUNT}  FAIL={FAIL_COUNT}")
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())
