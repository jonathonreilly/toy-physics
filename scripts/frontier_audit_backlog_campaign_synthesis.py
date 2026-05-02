#!/usr/bin/env python3
"""Verify the audit-backlog campaign progress synthesis."""

from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parent.parent
NOTE_PATH = ROOT / "docs" / "AUDIT_BACKLOG_CAMPAIGN_PROGRESS_SYNTHESIS_2026-05-02.md"

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


section("Part 1: synthesis structure")
note_text = NOTE_PATH.read_text()
required = [
    "Audit-Backlog Retained Campaign — Progress Synthesis",
    "Cycles 1-19",
    "audit-backlog-campaign-20260502",
    "LHCM closure chain",
    "Lattice → physical matching cluster",
    "SM-definition conventions reclassification",
    "G_BARE_* family closure",
]
for s in required:
    check(f"contains: {s!r}", s in note_text)


section("Part 2: all 19 cycle PRs cited")
prs = [254, 255, 256, 258, 260, 262, 264, 267, 268, 270, 271, 273, 274,
       276, 278, 279, 280, 281, 282]
for pr in prs:
    pattern = rf"#{pr}"
    check(f"cycle PR #{pr} cited",
          bool(re.search(pattern, note_text)),
          detail=f"PR {pr}")
check(f"19 PR numbers total cited", len(prs) == 19)


section("Part 3: 4 cluster instances enumerated")
cluster_lanes = [
    "yt_ew matching M",
    "gauge-scalar observable bridge",
    "Higgs mass scalar normalization",
    "Koide-Brannen-phase bridge",
]
for c in cluster_lanes:
    check(f"cluster lane: {c}", c in note_text)


section("Part 4: 6 LHCM repair items + closure cycles")
lhcm_items = [
    "(1) matter assignment",
    "(2) U(1)_Y normalization",
    "(3) anomaly LH SU(2)²×Y",
    "(3) anomaly R-A SU(3)²×Y",
    "(3) anomaly R-B Y³",
    "(3) anomaly R-C grav²×Y",
]
for item in lhcm_items:
    check(f"LHCM item: {item}", item in note_text)


section("Part 5: open Nature-grade targets enumerated")
nature_grade_targets = [
    "SM-definition conventions reclassification",
    "Lattice → physical matching cluster",
    "G_BARE_* family closure",
    "SU(5) GUT embedding",
    "Sommer-scale",
    "Brannen-phase bridge",
]
for t in nature_grade_targets:
    check(f"Nature-grade target: {t}", t in note_text)


section("Part 6: forbidden imports compliance")
forbidden_compliance = [
    "No PDG observed values",
    "No literature numerical comparators",
    "No fitted selectors",
    "No same-surface family arguments",
]
for f in forbidden_compliance:
    check(f"compliance: {f}", f in note_text)


print(f"\n{'='*88}\n  TOTAL: PASS={PASS_COUNT}, FAIL={FAIL_COUNT}\n{'='*88}")
sys.exit(1 if FAIL_COUNT > 0 else 0)
