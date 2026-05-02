#!/usr/bin/env python3
"""Verify the Kubo Fam2 non-convergence stretch-attempt note."""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
NOTE_PATH = ROOT / "docs" / "KUBO_FAM2_NON_CONVERGENCE_STRETCH_ATTEMPT_NOTE_2026-05-02.md"

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


section("Part 1: stretch note structure")
note_text = NOTE_PATH.read_text()
required = [
    "Kubo Fam2 Non-Convergence Stretch Attempt",
    "named obstruction packet",
    "A_min",
    "Forbidden imports",
    "Fam2",
    "Fam1",
    "Fam3",
    "(O1)",
    "(O2)",
    "(O3)",
    "non-perturbative",
    "proposal_allowed: false",
]
for s in required:
    check(f"contains: {s!r}", s in note_text)

section("Part 2: 3 obstruction routes documented")
obstructions = [
    "Microscopic dynamics depend on (drift, restore) non-trivially",
    "Phase transition or critical regime",
    "Discretization artifact",
]
for o in obstructions:
    check(f"obstruction: {o[:50]}",
          o in note_text)

section("Part 3: Fam parameters enumerated")
fam_params = [
    "drift=0.20, restore=0.70",  # Fam1
    "drift=0.05, restore=0.30",  # Fam2
    "drift=0.50, restore=0.90",  # Fam3
]
for fp in fam_params:
    check(f"family parameter: {fp}", fp in note_text)

section("Part 4: explicit non-closure")
non_closures = [
    "Fam2 non-convergence itself",
    "kubo_continuum_limit_families_note",
    "honest tier",
]
for nc in non_closures:
    check(f"non-closure: {nc}", nc in note_text)

print(f"\n{'='*88}\n  TOTAL: PASS={PASS_COUNT}, FAIL={FAIL_COUNT}\n{'='*88}")
sys.exit(1 if FAIL_COUNT > 0 else 0)
