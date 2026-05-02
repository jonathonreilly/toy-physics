#!/usr/bin/env python3
"""Verify the higgs_mass_from_axiom status-correction audit packet."""

from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parent.parent
NOTE_PATH = ROOT / "docs" / "HIGGS_MASS_FROM_AXIOM_STATUS_CORRECTION_AUDIT_NOTE_2026-05-02.md"

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


section("Part 1: audit packet structure")
note_text = NOTE_PATH.read_text()
required = [
    "Higgs Mass From Axiom Note — Status Correction Audit",
    "HIGGS_MASS_FROM_AXIOM_NOTE.md",
    "lattice curvature",
    "(m_H/v)²",
    "Same-shape obstruction as cycles 5 and 9",
    "lattice → continuum",  # → arrow
    "bounded support theorem",
    "proposal_allowed: false",
]
for s in required:
    check(f"contains: {s!r}", s in note_text)

section("Part 2: 4 issues identified")
issues = [
    "Lattice curvature → physical",
    "Taste polynomial",
    "EW-color and Higgs authority notes are conditional",
    "deps=[] in ledger",
]
for iss in issues:
    check(f"issue: {iss}", iss in note_text)

section("Part 3: 7 cert criteria assessed")
for i in range(1, 8):
    pattern = rf"\|\s*{i}\s*\|"
    check(f"Criterion {i}", bool(re.search(pattern, note_text)))

section("Part 4: same-shape obstruction with cycles 5 and 9")
sister_refs = ["#260", "#268", "M residual", "observable bridge"]
for s in sister_refs:
    check(f"sister cross-ref: {s}", s in note_text)

print(f"\n{'='*88}\n  TOTAL: PASS={PASS_COUNT}, FAIL={FAIL_COUNT}\n{'='*88}")
sys.exit(1 if FAIL_COUNT > 0 else 0)
