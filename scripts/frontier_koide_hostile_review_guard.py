#!/usr/bin/env python3
"""
Koide hostile-review guard.

This runner automates the recurring Nature-grade review checks that became
mechanical after the recent no-go cycles.  It does not prove a physics theorem;
it prevents the package from accidentally promoting a no-go or importing a
forbidden target as a theorem.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

DOC_GLOBS = [
    "docs/KOIDE_Q_*NO_GO_NOTE_2026-04-24.md",
    "docs/KOIDE_DELTA_*NO_GO_NOTE_2026-04-24.md",
    "docs/KOIDE_DIMENSIONLESS_OBJECTION_CLOSURE_REVIEW_PACKET_2026-04-24.md",
]
SCRIPT_GLOBS = [
    "scripts/frontier_koide_q_*no_go.py",
    "scripts/frontier_koide_delta_*no_go.py",
    "scripts/frontier_koide_dimensionless_objection_closure_review.py",
]

FORBIDDEN_PROMOTION_PATTERNS = [
    re.compile(r"\bKOIDE(?:[_ -]Q)?(?:[_ -]CLOS(?:URE|ES)|[_ -]CLOSES[_ -]Q)\s*=\s*TRUE\b", re.I),
    re.compile(r"\bDELTA(?:[_ -]CLOS(?:URE|ES)|[_ -]CLOSES[_ -]DELTA)\s*=\s*TRUE\b", re.I),
    re.compile(r"\bQ[_ -]CLOSES[_ -]Q\s*=\s*TRUE\b", re.I),
    re.compile(r"\bCLOSES[_ -]DELTA\s*=\s*TRUE\b", re.I),
]

FORBIDDEN_INPUT_PATTERNS = [
    re.compile(r"\bassumes?\s+K_TL\s*=\s*0\b", re.I),
    re.compile(r"\bassumes?\s+K\s*=\s*0\b", re.I),
    re.compile(r"\bassumes?\s+P_Q\s*=\s*1/2\b", re.I),
    re.compile(r"\bassumes?\s+Q\s*=\s*2/3\b", re.I),
    re.compile(r"\bassumes?\s+delta\s*=\s*2/9\b", re.I),
    re.compile(r"\bPDG\b.*\b(input|assumption|pin)\b", re.I),
    re.compile(r"\bH_\*\b.*\b(input|assumption|pin)\b", re.I),
]


PASS_COUNT = 0
FAIL_COUNT = 0


def check(name: str, condition: bool, detail: str = "") -> bool:
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if condition else "FAIL"
    if condition:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1
    print(f"  [{status}] {name}")
    if detail:
        print(f"       {detail}")
    return condition


def section(title: str) -> None:
    print()
    print("=" * 88)
    print(title)
    print("=" * 88)


def gather_files(globs: list[str]) -> list[Path]:
    files: list[Path] = []
    for pattern in globs:
        files.extend(ROOT.glob(pattern))
    return sorted(set(files))


def pattern_hits(text: str, patterns: list[re.Pattern[str]]) -> list[str]:
    hits: list[str] = []
    for pattern in patterns:
        match = pattern.search(text)
        if match:
            hits.append(match.group(0))
    return hits


def audit_no_go_docs() -> None:
    section("A. No-go notes retain residuals and do not promote closure")

    docs = gather_files(DOC_GLOBS)
    check(
        "A.1 no-go note set is non-empty",
        len(docs) > 0,
        detail=f"notes={len(docs)}",
    )

    missing_residual: list[str] = []
    promotion_hits: list[str] = []
    forbidden_inputs: list[str] = []
    for path in docs:
        text = path.read_text(encoding="utf-8")
        rel = str(path.relative_to(ROOT))
        if "RESIDUAL" not in text and "residual" not in text:
            missing_residual.append(rel)
        hits = pattern_hits(text, FORBIDDEN_PROMOTION_PATTERNS)
        if hits:
            promotion_hits.append(f"{rel}: {hits}")
        input_hits = pattern_hits(text, FORBIDDEN_INPUT_PATTERNS)
        if input_hits:
            # Hostile-review sections may say a proof does not assume a target.
            # Only flag direct "assumes ..." patterns, not negative disclosures.
            forbidden_inputs.append(f"{rel}: {input_hits}")

    check(
        "A.2 every no-go note names a residual scalar or residual primitive",
        not missing_residual,
        detail="\n".join(missing_residual),
    )
    check(
        "A.3 no no-go note promotes closure with a TRUE closeout flag",
        not promotion_hits,
        detail="\n".join(promotion_hits),
    )
    check(
        "A.4 no no-go note states a forbidden target as an assumption",
        not forbidden_inputs,
        detail="\n".join(forbidden_inputs),
    )


def audit_no_go_scripts() -> None:
    section("B. No-go scripts expose negative closeout flags")

    scripts = gather_files(SCRIPT_GLOBS)
    check(
        "B.1 no-go script set is non-empty",
        len(scripts) > 0,
        detail=f"scripts={len(scripts)}",
    )

    missing_false_flag: list[str] = []
    promotion_hits: list[str] = []
    missing_residual: list[str] = []
    for path in scripts:
        text = path.read_text(encoding="utf-8")
        rel = str(path.relative_to(ROOT))
        if "CLOSES" in text and "FALSE" not in text:
            missing_false_flag.append(rel)
        if "CLOSES" not in text:
            missing_false_flag.append(rel)
        if "RESIDUAL" not in text:
            missing_residual.append(rel)
        hits = pattern_hits(text, FORBIDDEN_PROMOTION_PATTERNS)
        if hits:
            promotion_hits.append(f"{rel}: {hits}")

    check(
        "B.2 every no-go script prints an explicit negative CLOSES flag",
        not missing_false_flag,
        detail="\n".join(missing_false_flag),
    )
    check(
        "B.3 every no-go script prints an explicit residual label",
        not missing_residual,
        detail="\n".join(missing_residual),
    )
    check(
        "B.4 no no-go script promotes closure with a TRUE closeout flag",
        not promotion_hits,
        detail="\n".join(promotion_hits),
    )


def main() -> int:
    print("=" * 88)
    print("Koide hostile-review guard")
    print("=" * 88)
    print(
        "Purpose: mechanically reject no-go packet drift where a failed route "
        "is accidentally promoted as closure or lacks a named residual scalar."
    )

    audit_no_go_docs()
    audit_no_go_scripts()

    print()
    print("=" * 88)
    print("Summary")
    print("=" * 88)
    print(f"PASSED: {PASS_COUNT}/{PASS_COUNT + FAIL_COUNT}")
    print()
    print("KOIDE_HOSTILE_REVIEW_GUARD_PASSED=" + ("TRUE" if FAIL_COUNT == 0 else "FALSE"))
    print("HOSTILE_REVIEW_GUARD_CLOSES_Q=FALSE")
    print("HOSTILE_REVIEW_GUARD_CLOSES_DELTA=FALSE")
    print("RESIDUAL_SCALAR=not_applicable_review_guard")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
