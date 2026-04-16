#!/usr/bin/env python3
"""
Physical-lattice necessity theorem attempt
=========================================

STATUS: theorem attempt on the global physical-lattice boundary

QUESTION:
  Can the physical-lattice reading be derived from the remaining accepted
  framework inputs, or does it still stand as an explicit global minimal input?

CURRENT RESULT:
  NOT CLOSED.

  The current package shows that regulator reinterpretation is not free:
    1. the minimal accepted input stack explicitly includes the physical-
       lattice reading;
    2. regulator reinterpretation requires extra structure not present in that
       minimal stack (continuum-limit family, rooting/continuum machinery,
       external renormalization interpretation);
    3. the current boundary note still treats the physical-lattice reading as
       irreducible rather than derived.

  Therefore the exact retained-generation theorem removes the remaining
  generation-surface reduction loophole, but the separate global
  physical-lattice premise is not yet absorbed into an axiom-internal theorem.

PStack experiment: frontier-physical-lattice-necessity
Dependencies: standard library only.
"""

from __future__ import annotations

import sys
from pathlib import Path


PASS_COUNT = 0
FAIL_COUNT = 0


def check(name: str, condition: bool, detail: str = "", kind: str = "EXACT") -> bool:
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if condition else "FAIL"
    if condition:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1
    tag = f" [{kind}]" if kind != "EXACT" else ""
    msg = f"  [{status}]{tag} {name}"
    if detail:
        msg += f"  ({detail})"
    print(msg)
    return condition


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def part1_minimal_input_stack(minimal_text: str) -> None:
    print("=" * 88)
    print("PART 1: MINIMAL INPUT STACK AUDIT")
    print("=" * 88)
    print()

    expected_inputs = [
        "1. **Local algebra:** the physical local algebra is `Cl(3)`.",
        "2. **Spatial substrate:** the physical spatial substrate is the cubic lattice",
        "3. **Microscopic dynamics:** the package works with the finite local",
        "4. **Physical-lattice reading:** the lattice is treated as physical rather",
        "5. **Canonical normalization and evaluation surface:** the current package uses",
    ]
    for idx, snippet in enumerate(expected_inputs, start=1):
        check(
            f"minimal_input_{idx}_present",
            snippet in minimal_text,
            snippet.splitlines()[0],
        )

    check(
        "physical_lattice_reading_is_explicit_minimal_input",
        "Physical-lattice reading:" in minimal_text,
        "the current package still lists this as accepted input #4",
    )

    check(
        "continuum_limit_family_not_in_minimal_input_stack",
        "continuum-limit family" not in minimal_text.lower(),
        "no tunable a -> 0 family appears in the minimal accepted inputs",
    )
    check(
        "rooting_machinery_not_in_minimal_input_stack",
        "rooting" not in minimal_text.lower(),
        "rooting/continuum removal is not part of the accepted minimal stack",
    )
    check(
        "renormalization_interpretation_not_in_minimal_input_stack",
        "renormalization" not in minimal_text.lower(),
        "no external renormalization interpretation appears in the accepted inputs",
    )
    print()


def part2_regulator_side_extra_structure(boundary_text: str, continuum_text: str) -> None:
    print("=" * 88)
    print("PART 2: REGULATOR REINTERPRETATION REQUIRES EXTRA STRUCTURE")
    print("=" * 88)
    print()

    check(
        "boundary_note_records_regulator_escape_route",
        "without it, an explicit escape route remains through regulator-style interpretation" in boundary_text,
        "the current boundary note still records the regulator-side escape",
    )
    check(
        "continuum_note_uses_continuum_limit_family",
        "continuum limit" in continuum_text.lower(),
        "regulator reinterpretation requires a continuum-limit family",
    )
    check(
        "continuum_note_uses_external_eft_bridge",
        "external technique" in continuum_text.lower() and "bounded" in continuum_text.lower(),
        "the continuum bridge is still labeled bounded/external",
    )
    check(
        "continuum_note_uses_renormalization_interpretation",
        "renormalization" in continuum_text.lower() or "rg flow" in continuum_text.lower(),
        "continuum reading requires a renormalization / RG interpretation",
    )
    print()


def part3_current_boundary_status(boundary_text: str, generation_text: str) -> bool:
    print("=" * 88)
    print("PART 3: CURRENT STATUS OF THE NECESSITY THEOREM ATTEMPT")
    print("=" * 88)
    print()

    irreducible = "that axiom is irreducible" in boundary_text.lower()
    exact_generation = "no proper quotient / rooting / reduction" in generation_text.lower()

    check(
        "generation_surface_reduction_loophole_is_closed",
        exact_generation,
        "the retained generation theorem already removes the quotient loophole",
    )
    check(
        "boundary_note_still_treats_physical_lattice_as_irreducible",
        irreducible,
        "the current authority surface still says the premise is not derived",
    )

    exact_necessity = (not irreducible) and exact_generation
    if exact_necessity:
        print("  RESULT: EXACT NECESSITY")
        print("    the global physical-lattice reading would now be forced internally.")
    else:
        print("  RESULT: NOT CLOSED")
        print("    the retained-generation theorem is exact, but the global")
        print("    physical-lattice premise is still carried as a separate")
        print("    minimal input rather than as a derived theorem.")
    print()
    return exact_necessity


def main() -> int:
    print("=" * 88)
    print("PHYSICAL-LATTICE NECESSITY THEOREM ATTEMPT")
    print("=" * 88)
    print()
    print("Question:")
    print("  Is the physical-lattice reading already forced by the remaining")
    print("  accepted framework inputs, or is it still a separate global input?")
    print()

    minimal_text = read_text(DOCS / "MINIMAL_AXIOMS_2026-04-11.md")
    boundary_text = read_text(DOCS / "GENERATION_AXIOM_BOUNDARY_NOTE.md")
    continuum_text = read_text(DOCS / "CONTINUUM_IDENTIFICATION_NOTE.md")
    generation_text = read_text(DOCS / "THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md")

    part1_minimal_input_stack(minimal_text)
    part2_regulator_side_extra_structure(boundary_text, continuum_text)
    exact_necessity = part3_current_boundary_status(boundary_text, generation_text)

    print("=" * 88)
    print("SYNTHESIS")
    print("=" * 88)
    print()
    print("  Audit result:")
    print("    - the minimal input stack still lists the physical-lattice reading")
    print("      explicitly")
    print("    - regulator reinterpretation still requires extra structure absent")
    print("      from that stack")
    print("    - the current authority note still marks the premise irreducible")
    print()
    print(f"  TOTAL: PASS = {PASS_COUNT}, FAIL = {FAIL_COUNT}")
    print(f"  FINAL STATUS: {'EXACT NECESSITY' if exact_necessity else 'NOT CLOSED'}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
