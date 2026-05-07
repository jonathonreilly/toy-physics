#!/usr/bin/env python3
"""Verify the gauge-scalar temporal observable-bridge stretch-attempt note.
Verifies note structure, A_min and forbidden imports declared, three named
obstruction routes (O1, O2, O3), and explicit non-closure.
"""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
NOTE_PATH = ROOT / "docs" / "GAUGE_SCALAR_TEMPORAL_OBSERVABLE_BRIDGE_STRETCH_NOTE_2026-05-02.md"

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


section("Part 1: stretch-attempt note structure")

note_text = NOTE_PATH.read_text()
required = [
    "Gauge-Scalar Temporal Observable Bridge Stretch Attempt",
    "named obstruction packet",
    "A_min",
    "Forbidden imports",
    "Wilson gauge action with β = 6",
    "K_O(ω) = 3w(3 + sin²ω)",
    "A_inf / A_2 = 2/√3",
    "(O1)",
    "(O2)",
    "(O3)",
    "Schwinger-Dyson",
    "effective-action",
    "Renormalization-group",
    "non-analytically-derivable",
    "does not set an",
]
for s in required:
    check(f"note contains: {s!r}", s in note_text)

section("Part 2: 3 obstruction routes documented")

obstructions = [
    "(O1) Schwinger-Dyson approach",
    "(O2) Effective-action approach",
    "(O3) Renormalization-group approach",
]
for o in obstructions:
    check(f"obstruction route: {o}",
          o in note_text, detail="present in §3.4")

failure_modes = [
    "non-perturbative input",
    "analytically",
    "perturbatively",
]
for fm in failure_modes:
    check(f"failure mode keyword: {fm}",
          fm in note_text, detail="failure mode")

section("Part 3: forbidden imports listed")

forbidden = [
    "PDG observed",
    "Lattice MC empirical",
    "Fitted β_eff(β) from data",
    "Same-surface family arguments",
]
for f in forbidden:
    check(f"forbidden import: {f}",
          f in note_text, detail="§2 forbidden imports")

section("Part 4: explicit non-closure")

non_closures = [
    "not analytically derived from `A_min`",
    "honest tier",
    "still open",
    "still conditional",
]
for nc in non_closures:
    check(f"non-closure: {nc}",
          nc in note_text or nc.lower() in note_text.lower())

section("Part 5: A_min explicitly enumerated")

amin_items = [
    "Wilson gauge action with β = 6",
    "K_O(ω) = 3w(3 + sin²ω)",
    "A_inf / A_2 = 2/√3",
    "1/N_c topological expansion",
]
for a in amin_items:
    check(f"A_min item: {a}",
          a in note_text, detail="§1 A_min table")

section("Part 6: 2026-05-07 stretch-attempt bounded verdict (no-go route)")

closure_section_items = [
    "Closure-attempt verdict (2026-05-07 stretch-attempt closure pass)",
    "Bounded verdict for the open question",
    "GAUGE_SCALAR_TEMPORAL_OBSERVABLE_BRIDGE_NO_GO_THEOREM_NOTE_2026-05-03",
    "two-witness argument",
    "Companion bounded result",
    "GAUGE_SCALAR_TEMPORAL_OBSERVABLE_BRIDGE_IMPLICIT_FLOW_THEOREM_NOTE_2026-05-03",
    "definition or fit",
    "audit ratification ≠ demotion",
    "Escape hatches",
    "no new axioms",
    "import → bounded → retire import",
    "attempted positive bridge is bounded",
]
for item in closure_section_items:
    check(f"closure section item: {item!r}",
          item in note_text, detail="§9 closure verdict")

print(f"\n{'='*88}\n  TOTAL: PASS={PASS_COUNT}, FAIL={FAIL_COUNT}\n{'='*88}")
sys.exit(1 if FAIL_COUNT > 0 else 0)
