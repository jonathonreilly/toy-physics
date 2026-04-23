#!/usr/bin/env python3
"""Audit the Planck information/action quantum lane.

This is a verdict-checker, not a derivation harness.
It encodes the current honest posture:
  - the single-axiom object is structurally useful
  - the physical unit map is not yet retained
  - the lane remains open / speculative
"""

from __future__ import annotations

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
LANE_NOTE = ROOT / "docs" / "PLANCK_SCALE_INFORMATION_ACTION_QUANTUM_LANE_2026-04-23.md"
SINGLE_AXIOM_NOTE = ROOT / "docs" / "SINGLE_AXIOM_INFORMATION_NOTE.md"
ACTION_NORMALIZATION_NOTE = ROOT / "docs" / "ACTION_NORMALIZATION_NOTE.md"
PROGRAM_NOTE = ROOT / "docs" / "PLANCK_SCALE_DERIVATION_PROGRAM_2026-04-23.md"


def section(title: str) -> None:
    print("\n" + "=" * 78)
    print(title)
    print("=" * 78)


def check(label: str, passed: bool, detail: str) -> bool:
    tag = "PASS" if passed else "FAIL"
    print(f"  [{tag}] {label}")
    print(f"         {detail}")
    return passed


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def normalized(text: str) -> str:
    return " ".join(text.split()).lower()


def main() -> int:
    lane_text = read_text(LANE_NOTE)
    single_text = read_text(SINGLE_AXIOM_NOTE)
    action_text = read_text(ACTION_NORMALIZATION_NOTE)
    program_text = read_text(PROGRAM_NOTE)

    print("Planck information/action quantum lane audit")
    print("=" * 78)

    n_pass = 0
    n_fail = 0

    section("PART 1: LANE VERDICT")
    lane_norm = normalized(lane_text)
    single_norm = normalized(single_text)
    action_norm = normalized(action_text)
    program_norm = normalized(program_text)

    p1 = check(
        "lane note stays open / speculative",
        "open / speculative" in lane_norm
        and "physical unit map" in lane_norm
        and "no retained theorem" in lane_norm,
        "the note explicitly treats the object as a candidate carrier, not a closed unit map",
    )
    n_pass += int(p1)
    n_fail += int(not p1)

    section("PART 2: SINGLE-AXIOM SCOPE")
    p2 = check(
        "single-axiom note is structural, not a unit-map theorem",
        "graph + unitarity" in single_norm
        and "finite-dimensional hilbert space" in single_norm
        and "not a proof that h must be sparse" in single_norm,
        "the note supports conserved flow, graph support, and unitarity; it does not introduce a physical unit map",
    )
    n_pass += int(p2)
    n_fail += int(not p2)

    section("PART 3: ACTION NORMALIZATION BOUNDARY")
    p3 = check(
        "action normalization still uses external gravitational calibration",
        "define g as newton's constant" in action_norm
        and "once g is fixed by laboratory measurement" in action_norm,
        "the action coefficient is fixed after measurement of G, so the unit map is still external there",
    )
    n_pass += int(p3)
    n_fail += int(not p3)

    section("PART 4: PROGRAM POSTURE")
    p4 = check(
        "program note keeps route e open and speculative",
        "open and speculative" in program_norm
        and "no retained theorem yet ties conserved information flow to a physical unit map" in program_norm,
        "the top-level program still classifies this route as open rather than derived",
    )
    n_pass += int(p4)
    n_fail += int(not p4)

    section("FINAL VERDICT")
    verdict = (
        "The irreducible information-flow object is a plausible structural "
        "candidate, but the missing physical unit map is not yet retained. "
        "Lane verdict: OPEN / SPECULATIVE."
    )
    print(f"  {verdict}")

    print("\n" + "=" * 78)
    print(f"SCORECARD: {n_pass} pass, {n_fail} fail out of {n_pass + n_fail}")
    print("=" * 78)

    return 0 if n_fail == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
