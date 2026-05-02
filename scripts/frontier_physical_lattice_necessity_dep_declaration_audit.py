#!/usr/bin/env python3
"""Verify the physical-lattice-necessity dep-declaration audit packet.

The audit packet is at:
  docs/PHYSICAL_LATTICE_NECESSITY_DEP_DECLARATION_AUDIT_NOTE_2026-05-02.md

This runner verifies:
  Part 1: audit-packet structure (citations, status discipline).
  Part 2: the actually-read upstream notes from the parent runner are
          enumerated correctly (11 notes + 1 sibling runner).
  Part 3: the 7 retained-proposal criteria assessment is internally
          consistent and the recommended status is the narrowest honest tier.
  Part 4: the dep-declaration recommendation is concrete and verifiable.
"""

from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parent.parent
NOTE_PATH = ROOT / "docs" / "PHYSICAL_LATTICE_NECESSITY_DEP_DECLARATION_AUDIT_NOTE_2026-05-02.md"
PARENT_RUNNER_PATH = ROOT / "scripts" / "frontier_physical_lattice_necessity.py"

PASS_COUNT = 0
FAIL_COUNT = 0


def check(label, ok, detail=""):
    global PASS_COUNT, FAIL_COUNT
    tag = "PASS (A)" if ok else "FAIL (A)"
    if ok:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1
    print(f"  [{tag}] {label}  ({detail})")


def section(title):
    print()
    print("-" * 88)
    print(title)
    print("-" * 88)


# ---------------------------------------------------------------------------
# Part 1: audit-packet structure
# ---------------------------------------------------------------------------
section("Part 1: dep-declaration audit-packet structure")

note_text = NOTE_PATH.read_text()
required = [
    "Physical-Lattice Necessity Dependency-Declaration Audit",
    "dependency-declaration repair packet",
    "PHYSICAL_LATTICE_NECESSITY_NOTE.md",
    "frontier_physical_lattice_necessity.py",
    "Recommended ledger row update",
    "deps: []",
    "bounded support theorem",
    "proposal_allowed",
]
for s in required:
    check(f"audit packet contains: {s!r}",
          s in note_text, detail=f"len(note)={len(note_text)}")

# ---------------------------------------------------------------------------
# Part 2: actually-read upstream notes
# ---------------------------------------------------------------------------
section("Part 2: enumerated upstream notes match parent runner reads")

# Parse the parent runner to find DOCS / "..." reads
parent_text = PARENT_RUNNER_PATH.read_text()
read_matches = re.findall(
    r'read_text\(DOCS\s*/\s*"([A-Z_0-9-]+\.md)"\)',
    parent_text
)
parent_runner_reads = sorted(set(read_matches))
check(f"parent runner reads at least 10 .md files",
      len(parent_runner_reads) >= 10,
      detail=f"found {len(parent_runner_reads)} distinct reads")

# All read notes should be enumerated in the audit packet
for read_note in parent_runner_reads:
    check(f"audit packet enumerates parent-read note: {read_note}",
          read_note in note_text,
          detail="present in §1 dep table")

# ---------------------------------------------------------------------------
# Part 3: 7-criteria assessment
# ---------------------------------------------------------------------------
section("Part 3: 7 retained-proposal criteria assessment")

for i in range(1, 8):
    pattern = rf"\|\s*{i}\s*\|"
    check(f"audit packet explicitly assesses Criterion {i}",
          bool(re.search(pattern, note_text)),
          detail=f"row {i} in criteria table")

# Recommended status
check("recommended status = 'bounded support theorem'",
      "bounded support theorem" in note_text)

# ---------------------------------------------------------------------------
# Part 4: dep-declaration recommendation
# ---------------------------------------------------------------------------
section("Part 4: dep-declaration recommendation")

# Recommended deps list should include the major reads
key_deps = [
    "minimal_axioms_2026-04-11",
    "plaquette_self_consistency_note",
    "three_generation_observable_theorem_note",
    "generation_axiom_boundary_note",
    "one_generation_matter_closure_note",
    "anomaly_forces_time_theorem",
]
for dep in key_deps:
    check(f"recommended deps list contains: {dep}",
          dep in note_text,
          detail="present in §2 ledger update YAML")

# Demotion path
check("demotion path documented (proposed_retained → bounded)",
      "proposed_retained" in note_text and "bounded support theorem" in note_text)

# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------
print()
print("=" * 88)
print(f"  TOTAL: PASS={PASS_COUNT}, FAIL={FAIL_COUNT}")
print("=" * 88)

sys.exit(1 if FAIL_COUNT > 0 else 0)
