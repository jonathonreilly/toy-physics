#!/usr/bin/env python3
"""Verify the g_bare_derivation status-correction audit packet.
Verifies note structure, missing-runner claim, constraint vs convention
ambiguity discussion, A → A/g rescaling freedom analysis, 7 cert criteria,
and recommended status correction.
"""

from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parent.parent
NOTE_PATH = ROOT / "docs" / "G_BARE_DERIVATION_STATUS_CORRECTION_AUDIT_NOTE_2026-05-02.md"
CLAIMED_MISSING_RUNNER = ROOT / "scripts" / "frontier_g_bare_derivation.py"

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
    print("\n" + "-" * 88 + f"\n{title}\n" + "-" * 88)


section("Part 1: audit-packet structure")

note_text = NOTE_PATH.read_text()
required = [
    "g_bare Derivation Note — Status Correction Audit",
    "G_BARE_DERIVATION_NOTE.md",
    "constraint vs. convention",
    "A → A/g rescaling freedom",
    "missing primary runner",
    "frontier_g_bare_derivation.py",
    "bounded normalization proposal",
    "proposal_allowed: false",
]
for s in required:
    check(f"audit packet contains: {s!r}", s in note_text)

section("Part 2: confirm missing runner")

check("claimed missing runner is actually missing",
      not CLAIMED_MISSING_RUNNER.exists(),
      detail=f"path = {CLAIMED_MISSING_RUNNER}")

section("Part 3: constraint vs convention ambiguity discussion")

ambiguity_points = [
    "(a) Structural constraint",
    "(b) Convention choice",
    "load-bearing for retention",
    "admitted convention with narrow non-derivation role",
]
for ap in ambiguity_points:
    check(f"ambiguity point: {ap}",
          ap in note_text, detail="§2 ambiguity discussion")

section("Part 4: A → A/g rescaling freedom analysis")

rescaling_points = [
    "S_gauge[A; g]",
    "1/4 g²",
    "g_bare × |A|",
    "structural identity in the Cl(3) framework",
]
for rp in rescaling_points:
    check(f"rescaling analysis: {rp}",
          rp in note_text, detail="§3 rescaling discussion")

section("Part 5: 7 cert criteria assessment")

for i in range(1, 8):
    pattern = rf"\|\s*{i}\s*\|"
    check(f"audit packet explicitly assesses Criterion {i}",
          bool(re.search(pattern, note_text)))

section("Part 6: G_BARE_* sister family enumerated")

g_bare_family = [
    "G_BARE_STRUCTURAL_NORMALIZATION_THEOREM_NOTE_2026-04-18",
    "G_BARE_RIGIDITY_THEOREM_NOTE",
    "G_BARE_TWO_WARD_CLOSURE_NOTE_2026-04-18",
    "G_BARE_DYNAMICAL_FIXATION_OBSTRUCTION_NOTE_2026-04-18",
]
for gb in g_bare_family:
    check(f"G_BARE_* family member: {gb}",
          gb in note_text, detail="§8 cross-references")

print(f"\n{'='*88}\n  TOTAL: PASS={PASS_COUNT}, FAIL={FAIL_COUNT}\n{'='*88}")
sys.exit(1 if FAIL_COUNT > 0 else 0)
