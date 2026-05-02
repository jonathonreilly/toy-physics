#!/usr/bin/env python3
"""Verify three-generation observable dep-chain audit packet."""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
NOTE_PATH = ROOT / "docs" / "THREE_GENERATION_OBSERVABLE_DEP_CHAIN_AUDIT_NOTE_2026-05-02.md"
LEDGER = ROOT / "docs" / "audit" / "data" / "audit_ledger.json"

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
    "Three-Generation Observable Theorem — Dep-Chain Audit",
    "audited_conditional",
    "audited_clean",
    "generation_axiom_boundary_note",
    "physical_lattice_necessity_note",
    "Cycle 7",
]
for s in required:
    check(f"contains: {s!r}", s in note_text)

section("Part 2: dep status verification against ledger")
with open(LEDGER) as f:
    ledger = json.load(f)
rows = ledger['rows']

target = 'three_generation_observable_theorem_note'
r = rows[target]
deps = r.get('deps', [])
check(f"parent has 5 deps", len(deps) == 5,
      detail=f"deps count = {len(deps)}")

clean_count = 0
conditional_count = 0
for d in deps:
    dr = rows.get(d, {})
    au = dr.get('audit_status')
    if au == 'audited_clean':
        clean_count += 1
    elif au == 'audited_conditional':
        conditional_count += 1
check(f"4 of 5 deps audited_clean", clean_count == 4,
      detail=f"clean = {clean_count}")
check(f"1 of 5 deps audited_conditional", conditional_count == 1,
      detail=f"conditional = {conditional_count}")
check(f"generation_axiom_boundary_note is the conditional dep",
      rows.get('generation_axiom_boundary_note', {}).get('audit_status') == 'audited_conditional')

section("Part 3: cluster identification")
cluster_refs = [
    "Cycle 7",
    "PR [#264]",
    "physical_lattice_necessity_note",
    "same-shape",
]
for c in cluster_refs:
    check(f"cluster ref: {c}", c in note_text)

section("Part 4: 7 cert criteria")
for i in range(1, 8):
    pattern = rf"\|\s*{i}\s*\|"
    check(f"Criterion {i}", bool(re.search(pattern, note_text)))

print(f"\n{'='*88}\n  TOTAL: PASS={PASS_COUNT}, FAIL={FAIL_COUNT}\n{'='*88}")
sys.exit(1 if FAIL_COUNT > 0 else 0)
