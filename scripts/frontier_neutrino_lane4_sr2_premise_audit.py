#!/usr/bin/env python3
"""Lane 4 SR-2 premise audit verification.

Verifies the structural content of
``docs/NEUTRINO_LANE4_SR2_PREMISE_AUDIT_NOTE_2026-04-30.md``: the retained
free-scalar 2-point closure and admissible Pfaffian extensions live on
distinct substrate sectors, so the 2026-04-28 fan-out's recommendation of
SR-2 as a single-cycle attempt is over-optimistic without a connecting
primitive.

This is a premise-audit verification harness. It does NOT close (C2-X), does
NOT prove or falsify SR-2, and does NOT retire any open primitive.
"""

from __future__ import annotations

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


SR2_AUDIT_NOTE = "docs/NEUTRINO_LANE4_SR2_PREMISE_AUDIT_NOTE_2026-04-30.md"
TWO_PT_2D_NOTE = "docs/LORENTZ_BOOST_COVARIANCE_2D_THEOREM_NOTE.md"
TWO_PT_3PLUS1D_NOTE = "docs/LORENTZ_BOOST_COVARIANCE_3PLUS1D_THEOREM_NOTE.md"
FAN_OUT_NOTE = "docs/NEUTRINO_AXIOM3_READING_STUCK_FANOUT_NOTE_2026-04-28.md"
PFAFFIAN_NO_FORCING_NOTE = "docs/NEUTRINO_MAJORANA_PFAFFIAN_NO_FORCING_THEOREM_NOTE.md"


def part1_referenced_notes_exist() -> None:
    section("Part 1: referenced retained-surface notes exist")
    for rel in [
        SR2_AUDIT_NOTE,
        TWO_PT_2D_NOTE,
        TWO_PT_3PLUS1D_NOTE,
        FAN_OUT_NOTE,
        PFAFFIAN_NO_FORCING_NOTE,
    ]:
        check(f"note exists: {rel}", (ROOT / rel).is_file())


def part2_audit_note_structure() -> None:
    section("Part 2: SR-2 audit note structure")
    note = read(SR2_AUDIT_NOTE)
    check(
        "audit note title is correct",
        "Neutrino Lane 4 — SR-2 Premise Audit" in note,
    )
    check(
        "audit note status is support / premise-audit",
        "support / premise-audit" in note,
    )
    check(
        "audit note explicitly does NOT close (C2-X)",
        "does **not** close `(C2-X)`" in note or "does **not**\nclose `(C2-X)`" in note,
    )
    check(
        "audit note explicitly does NOT prove or falsify SR-2",
        "does **not** prove or falsify `(SR-2)`" in note,
    )
    check(
        "audit note does NOT use bare retained/promoted",
        "Status: retained" not in note and "Status: promoted" not in note,
    )


def part3_structural_gap_claim() -> None:
    section("Part 3: structural-gap claim is self-consistent")
    note_2pt_2d = read(TWO_PT_2D_NOTE)
    note_2pt_3p1d = read(TWO_PT_3PLUS1D_NOTE)
    note_pfaffian = read(PFAFFIAN_NO_FORCING_NOTE)

    # The retained 2-point notes should NOT reference Pfaffian extensions
    # (that's the structural gap).
    check(
        "1+1D 2-point note does not reference Pfaffian extensions",
        "Pfaffian" not in note_2pt_2d,
    )
    check(
        "3+1D 2-point note does not reference Pfaffian extensions",
        "Pfaffian" not in note_2pt_3p1d,
    )

    # The Pfaffian no-forcing note should NOT reference the free-scalar 2-point
    # closure as a load-bearing constraint (that's the missing link).
    check(
        "Pfaffian no-forcing note does not load-bear on free-scalar 2-point closure",
        "free-scalar 2-point closure" not in note_pfaffian
        and "Lorentz-boost-covariant 2-point" not in note_pfaffian,
    )


def part4_fan_out_claim_audited() -> None:
    section("Part 4: 2026-04-28 fan-out claim is faithfully cited")
    fanout = read(FAN_OUT_NOTE)
    audit = read(SR2_AUDIT_NOTE)
    # The fan-out should contain SR-2 framing
    check(
        "fan-out note contains (SR-2) recommendation",
        "(SR-2)" in fanout and "single-cycle" in fanout,
    )
    # The audit should quote the fan-out's recommendation language
    check(
        "audit note cites fan-out's 'single-cycle' framing as the audited claim",
        "single-cycle" in audit and "most promising" in audit,
    )


def part5_three_prerequisite_primitives() -> None:
    section("Part 5: three candidate prerequisite primitives named")
    audit = read(SR2_AUDIT_NOTE)
    for label in ["### 4A.", "### 4B.", "### 4C."]:
        check(f"prerequisite primitive {label} present", label in audit)
    # Each should name what it would supply
    check(
        "4A names direct fermionic 2-point closure",
        "fermionic 2-point closure" in audit or "staggered-Dirac fermion" in audit,
    )
    check(
        "4B names admitted scalar-fermion coupling",
        "scalar-fermion coupling" in audit or "Yukawa" in audit,
    )


def part6_block_count_revision() -> None:
    section("Part 6: block-count revision (1-block -> 2-block program)")
    audit = read(SR2_AUDIT_NOTE)
    check(
        "audit note re-times SR-2 from 1-block to 2-block program",
        "2-block program" in audit or "two-block program" in audit,
    )
    check(
        "audit note explicitly does NOT invalidate SR-2 as a target",
        "does not invalidate SR-2" in audit,
    )


def part7_forbidden_imports() -> None:
    section("Part 7: forbidden-import role check")
    audit = read(SR2_AUDIT_NOTE)
    check(
        "audit note states no new physical claims",
        "no new physical claims" in audit.lower(),
    )
    check(
        "audit note states no new numerical comparators",
        "no new numerical comparators" in audit.lower(),
    )
    check(
        "audit note states no new admitted observations",
        "no new admitted observations" in audit.lower(),
    )


def main() -> int:
    section("Lane 4 SR-2 premise audit verification")
    part1_referenced_notes_exist()
    part2_audit_note_structure()
    part3_structural_gap_claim()
    part4_fan_out_claim_audited()
    part5_three_prerequisite_primitives()
    part6_block_count_revision()
    part7_forbidden_imports()

    print()
    print("-" * 88)
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    print("-" * 88)
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
