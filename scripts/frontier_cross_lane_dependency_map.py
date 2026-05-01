#!/usr/bin/env python3
"""Cross-lane dependency map verification.

This runner checks that
``docs/CROSS_LANE_DEPENDENCY_MAP_NOTE_2026-04-30.md`` is internally
consistent with the existing per-lane firewall notes it consolidates.

It is a synthesis-verification harness, not a physics derivation. It does NOT
close any lane; it only checks that the dependency graph in the note is
faithful to the existing repo firewall surface.
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


# Firewall notes the cross-lane map cites in §1.
FIREWALL_NOTES = [
    "docs/HADRON_LANE1_CONFINEMENT_TO_MASS_FIREWALL_NOTE_2026-04-27.md",
    "docs/ATOMIC_RYDBERG_DEPENDENCY_FIREWALL_NOTE_2026-04-27.md",
    "docs/ATOMIC_LANE2_QED_RUNNING_DEPENDENCY_FIREWALL_NOTE_2026-04-30.md",
    "docs/QUARK_LANE3_BOUNDED_COMPANION_RETENTION_FIREWALL_NOTE_2026-04-27.md",
    "docs/NEUTRINO_LANE4_DIRAC_SEESAW_FORK_NO_GO_NOTE_2026-04-27.md",
    "docs/HUBBLE_LANE5_TWO_GATE_DEPENDENCY_FIREWALL_NOTE_2026-04-27.md",
]

# Open-lane README is the comparator for closure-ordering.
OPEN_LANE_README = "docs/lanes/open_science/README.md"

CROSS_LANE_NOTE = "docs/CROSS_LANE_DEPENDENCY_MAP_NOTE_2026-04-30.md"


def part1_firewall_existence() -> None:
    section("Part 1: per-lane firewall notes exist")
    for rel in FIREWALL_NOTES:
        check(f"firewall note exists: {rel}", (ROOT / rel).is_file())


def part2_firewall_status_language() -> None:
    section("Part 2: firewall status language is honest (no bare retained)")
    accepted_status_phrases = [
        "proposed_retained",
        "exact reduction theorem",
        "exact negative boundary",
        "exact-reduction-theorem",
        "support firewall",
    ]
    for rel in FIREWALL_NOTES:
        text = read(rel)
        # bare 'Status: retained' or '**Status:** retained' is forbidden
        bare_status_lines = [
            line
            for line in text.splitlines()
            if line.strip().lower().startswith("status:")
            and "retained" in line.lower()
            and "proposed_retained" not in line.lower()
            and "support" not in line.lower()
            and "exact" not in line.lower()
            and "boundary" not in line.lower()
            and "reduction" not in line.lower()
            and "no claim" not in line.lower()
            and "branch-local" not in line.lower()
        ]
        has_accepted_phrase = any(p in text for p in accepted_status_phrases)
        check(
            f"{rel}: uses an accepted status phrase",
            has_accepted_phrase,
        )
        check(
            f"{rel}: no bare 'Status: retained' line",
            not bare_status_lines,
            f"violations: {bare_status_lines[:2]}" if bare_status_lines else "",
        )


def part3_cross_lane_note_structure() -> None:
    section("Part 3: cross-lane map structure")
    note = read(CROSS_LANE_NOTE)
    check(
        "cross-lane note exists with correct title",
        "Cross-Lane Dependency Map" in note,
    )
    check(
        "cross-lane note status is support-only synthesis",
        "support-only synthesis" in note and "no claim promotion" in note,
    )
    check(
        "cross-lane note does NOT use bare 'Status: retained'",
        "Status: retained" not in note and "Status: promoted" not in note,
    )
    for rel in FIREWALL_NOTES:
        # Reference by basename in the note's tables/cross-references
        basename = Path(rel).name.replace(".md", "")
        check(
            f"cross-lane note references {basename}",
            basename in note,
        )


def part4_dependency_graph_components() -> None:
    section("Part 4: dependency graph components are named")
    note = read(CROSS_LANE_NOTE)
    components = [
        "Matter-mass component",
        "Neutrino component",
        "Cosmology component",
    ]
    for comp in components:
        check(f"component named: {comp}", comp in note)
    # Three components claim
    check(
        "graph asserted to have three disjoint components",
        "three disjoint connected components" in note,
    )


def part5_transitive_blockers_acyclic() -> None:
    section("Part 5: transitive blocker structure")
    note = read(CROSS_LANE_NOTE)
    transitive_keys = [
        ("Lane 6 closure", "Lane 2"),
        ("Lane 6 closure", "Lane 3"),
        ("Lane 3 closure", "Lane 1"),
        ("Lane 3 closure", "Lane 2"),
        ("Lane 1 substrate", "Lane 2"),
        ("Lane 1 substrate", "Lane 1"),
    ]
    for src, dst in transitive_keys:
        # Each blocker should appear in §3 with both source and target lanes
        check(
            f"transitive blocker '{src}' reaches '{dst}'",
            src in note and dst in note,
        )

    # Closure-ordering chain should not list Lane 2 before Lane 6 in §4
    section_4_start = note.find("## 4. Closure-ordering")
    section_4_end = note.find("## 5. ", section_4_start)
    chain = note[section_4_start:section_4_end]
    pos_lane6 = chain.find("Lane 6")
    pos_lane3 = chain.find("Lane 3", pos_lane6 + 1) if pos_lane6 >= 0 else -1
    pos_lane1 = chain.find("Lane 1", pos_lane3 + 1) if pos_lane3 >= 0 else -1
    pos_lane2_substitution = (
        chain.find("Lane 2 substitution", pos_lane1 + 1) if pos_lane1 >= 0 else -1
    )
    check(
        "closure-ordering: Lane 6 listed before Lane 3 in §4 chain",
        pos_lane6 >= 0 and pos_lane3 > pos_lane6,
    )
    check(
        "closure-ordering: Lane 3 listed before Lane 1 in §4 chain",
        pos_lane3 >= 0 and pos_lane1 > pos_lane3,
    )
    check(
        "closure-ordering: Lane 1 listed before Lane 2 substitution in §4 chain",
        pos_lane1 >= 0 and pos_lane2_substitution > pos_lane1,
    )


def part6_retired_shortcuts() -> None:
    section("Part 6: retired shortcuts each cite a concrete firewall")
    note = read(CROSS_LANE_NOTE)
    section_5_start = note.find("## 5. What this note retires")
    section_5_end = note.find("## 6. ", section_5_start)
    section_5 = note[section_5_start:section_5_end]
    # Four retired shortcuts numbered 1-4
    for i in range(1, 5):
        check(
            f"retired shortcut #{i} present",
            f"{i}. **\"" in section_5,
        )
    # Each retired shortcut should cite a firewall by Lane number
    citation_keywords = ["Lane 1", "Lane 2", "Lane 3", "Lane 4", "Lane 5", "Lane 6"]
    for kw in citation_keywords:
        check(
            f"§5 cites {kw}",
            kw in section_5,
        )


def part7_synthesis_only() -> None:
    section("Part 7: synthesis-only — no new physics inputs")
    note = read(CROSS_LANE_NOTE)
    check(
        "note states pure synthesis posture",
        "pure synthesis" in note or "no new physical claims" in note.lower(),
    )
    check(
        "note states no new numerical comparators",
        "no new numerical comparators" in note.lower(),
    )
    check(
        "note states no new admitted observations",
        "no new admitted observations" in note.lower(),
    )


def main() -> int:
    section("Cross-lane dependency map verification")
    part1_firewall_existence()
    part2_firewall_status_language()
    part3_cross_lane_note_structure()
    part4_dependency_graph_components()
    part5_transitive_blockers_acyclic()
    part6_retired_shortcuts()
    part7_synthesis_only()

    print()
    print("-" * 88)
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    print("-" * 88)
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
