#!/usr/bin/env python3
"""Verify the lattice→physical matching cluster obstruction synthesis."""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
NOTE_PATH = ROOT / "docs" / "LATTICE_PHYSICAL_MATCHING_CLUSTER_OBSTRUCTION_NOTE_2026-05-02.md"

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


section("Part 1: cluster note structure")
note_text = NOTE_PATH.read_text()
required = [
    "Lattice → Physical Matching Cluster Obstruction Theorem",
    "named-obstruction synthesis theorem",
    "yt_ew matching rule M",
    "gauge-scalar observable bridge",
    "Higgs mass from axiom",
    "(O1) Schwinger-Dyson",
    "(O2) Effective-action",
    "(O3) Renormalization-group",
    "Nature-grade target",
    "proposal_allowed: false",
]
for s in required:
    check(f"contains: {s!r}", s in note_text)

section("Part 2: 3 sister cycles cited")
sister_prs = ["#260", "#268", "#271"]
for pr in sister_prs:
    check(f"sister PR: {pr}", pr in note_text)

sister_cycles = ["Cycle 5", "Cycle 9", "Cycle 11"]
for c in sister_cycles:
    check(f"sister cycle: {c}", c in note_text)

section("Part 3: 3 resolution routes documented")
resolutions = [
    "Resolution A:",
    "Resolution B:",
    "Resolution C:",
    "novel non-perturbative matching theorem",
    "renormalization-scheme classification",
    "lattice MC computation",
]
for r in resolutions:
    check(f"resolution path: {r}",
          r in note_text)

section("Part 4: A_min and forbidden imports")
amin = [
    "graph-first SU(N_c) integration",
    "Wilson gauge action",
    "1/N_c topological expansion",
    "Fierz identity",
    "OZI rule",
]
for a in amin:
    check(f"A_min: {a}", a in note_text)

forbidden = [
    "PDG observed values",
    "Lattice MC empirical",
    "Fitted matching coefficients",
]
for f in forbidden:
    check(f"forbidden: {f}", f in note_text)

print(f"\n{'='*88}\n  TOTAL: PASS={PASS_COUNT}, FAIL={FAIL_COUNT}\n{'='*88}")
sys.exit(1 if FAIL_COUNT > 0 else 0)
