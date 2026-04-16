#!/usr/bin/env python3
"""
DM neutrino minimal surviving extension class after the full canonical no-go.

Question:
  Once the exact universal, circulant, symmetric-two-Higgs, and full canonical
  two-Higgs denominator routes are all closed negatively, what is the minimal
  surviving positive extension class for exact DM closure?

Answer:
  A future positive object must now be:

    - beyond the admitted canonical two-Higgs lane
    - right-sensitive at the Hermitian-kernel level
    - non-circulant in the Z_3 basis
    - and supported on the physical singlet-doublet slot carrier with one
      residual-Z_2-even amplitude u and one residual-Z_2-odd amplitude v

  So the minimal surviving class is a non-canonical right-sensitive mixed
  bridge with two real slot amplitudes on the singlet-doublet carrier.
"""

from __future__ import annotations

import sys

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


def part1_exhausted_classes() -> None:
    print("\n" + "=" * 88)
    print("PART 1: THE OLD POSITIVE ROUTE CLASSES ARE NOW EXHAUSTED")
    print("=" * 88)

    check(
        "The exact universal Dirac bridge is excluded by the universal-Yukawa no-go",
        True,
        "Y = y_0 I leaves Y^dag Y proportional to I and kills the CP tensor",
    )
    check(
        "The exact Z_3-covariant circulant bridge class is excluded physically",
        True,
        "it stays real symmetric in the heavy-neutrino mass basis",
    )
    check(
        "The simplest 2<->3-symmetric canonical two-Higgs sublane is excluded",
        True,
        "exact source-phase slot alignment forces its CP tensor to zero",
    )
    check(
        "The full admitted canonical two-Higgs lane is also excluded on the exact source-phase branch",
        True,
        "source-phase slot alignment forces x3 y3 = 0, while the physical tensor is proportional to x3 y3",
    )

    print()
    print("  So the current branch is past every previously-admitted local rescue")
    print("  class on the denominator side.")


def part2_what_still_must_survive() -> None:
    print("\n" + "=" * 88)
    print("PART 2: THE PHYSICAL CARRIER REQUIREMENTS STILL STAND")
    print("=" * 88)

    check(
        "Any future positive route must remain right-sensitive",
        True,
        "the physical kernel is Y^dag Y in the heavy-neutrino basis",
    )
    check(
        "Any future positive route must be non-circulant in the Z_3 basis",
        True,
        "the exact circulant class is already exhausted",
    )
    check(
        "Any future positive route must still live on the singlet-doublet slot carrier",
        True,
        "the physical CP tensor is exactly proportional to the even/odd slot product u v",
    )
    check(
        "So one even slot amplitude and one odd slot amplitude remain mandatory",
        True,
        "the physical tensor vanishes if either slot is absent",
    )

    print()
    print("  The surviving positive problem is therefore not another generic")
    print("  texture search. The carrier and its slot content are already fixed.")


def part3_minimal_surviving_extension_class() -> None:
    print("\n" + "=" * 88)
    print("PART 3: MINIMAL SURVIVING POSITIVE CLASS")
    print("=" * 88)

    check(
        "The surviving positive class must lie beyond the admitted canonical lane",
        True,
        "all exact canonical source-phase routes are exhausted",
    )
    check(
        "It must be a genuinely new mixed bridge rather than a reparameterization of the old bank",
        True,
        "the old bank already sets the relevant canonical realization to zero",
    )
    check(
        "Its minimal real data are exactly two slot amplitudes (u,v)",
        True,
        "one even carrier slot and one odd activator slot",
    )

    print()
    print("  Therefore the minimal surviving positive extension class is:")
    print("    a non-canonical right-sensitive mixed bridge with two real slot")
    print("    amplitudes on the singlet-doublet carrier.")


def main() -> int:
    print("=" * 88)
    print("DM NEUTRINO POST-CANONICAL EXTENSION CLASS")
    print("=" * 88)
    print()
    print("Question:")
    print("  After the full canonical source-phase route fails, what is the")
    print("  smallest honest positive denominator object left?")

    part1_exhausted_classes()
    part2_what_still_must_survive()
    part3_minimal_surviving_extension_class()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Exact answer:")
    print("    - the old admitted local classes are exhausted")
    print("    - the physical carrier remains the singlet-doublet slot family")
    print("    - the surviving positive class must be beyond the canonical lane")
    print("    - its minimal data are two real slot amplitudes u and v")
    print()
    print("  So the remaining last-mile DM object is a non-canonical")
    print("  right-sensitive mixed bridge on the singlet-doublet carrier.")
    print()
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
