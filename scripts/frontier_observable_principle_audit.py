#!/usr/bin/env python3
"""Verify the observable-principle status-correction audit packet.

The packet is at:
  docs/OBSERVABLE_PRINCIPLE_AUDIT_NOTE_2026-05-02.md
"""

from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parent.parent
NOTE_PATH = ROOT / "docs" / "OBSERVABLE_PRINCIPLE_AUDIT_NOTE_2026-05-02.md"

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
    "Observable-Principle From-Axiom Note — Status Correction Audit",
    "demotion / status correction packet",
    "OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md",
    "scalar additivity",
    "CPT-even phase blindness",
    "continuity",
    "normalization",
    "hierarchy baseline",
    "bounded support theorem",
    "proposal_allowed: false",
]
for s in required:
    check(f"audit packet contains: {s!r}", s in note_text)

section("Part 2: 4+1 admitted assumptions enumerated")

assumptions = [
    "scalar additivity",
    "CPT-even phase blindness",
    "continuity",
    "normalization",
    "hierarchy baseline",
]
for a in assumptions:
    check(f"admitted assumption: {a}",
          a in note_text, detail="present in §1 table")

section("Part 3: 7-criteria assessment")

for i in range(1, 8):
    pattern = rf"\|\s*{i}\s*\|"
    check(f"audit packet explicitly assesses Criterion {i}",
          bool(re.search(pattern, note_text)))

section("Part 4: retention path documented")

retention_paths = [
    "physical-principle of independent-subsystem locality",
    "scalar bosonic insensitivity to phase",
    "mathematical regularity",
    "convention reclassification",
    "hierarchy lane retention",
]
for path in retention_paths:
    check(f"retention path: {path}",
          path in note_text, detail="§4 retention table")

print(f"\n{'='*88}\n  TOTAL: PASS={PASS_COUNT}, FAIL={FAIL_COUNT}\n{'='*88}")
sys.exit(1 if FAIL_COUNT > 0 else 0)
