#!/usr/bin/env python3
"""Audit the Planck gravity/action unit-map lane honestly.

This is not a derivation harness. It checks the repo evidence for the lane
verdict:
  - gravity closes in lattice units, not SI
  - action normalization still consumes observation
  - the textbook EH equivalence is already closed, but as a geometric/action
    comparison, not a physical unit-map theorem
  - therefore the route remains a pinned-observable lane
"""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
NOTE = ROOT / "docs/PLANCK_SCALE_GRAVITY_ACTION_UNIT_MAP_LANE_2026-04-23.md"
GRAVITY = ROOT / "docs/GRAVITY_CLEAN_DERIVATION_NOTE.md"
ACTION = ROOT / "docs/ACTION_NORMALIZATION_NOTE.md"
GEOM = ROOT / "docs/UNIVERSAL_QG_CANONICAL_TEXTBOOK_GEOMETRIC_ACTION_EQUIVALENCE_NOTE.md"


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
    return path.read_text(encoding="utf-8")


def main() -> None:
    n_pass = 0
    n_fail = 0

    note = read_text(NOTE)
    gravity = read_text(GRAVITY)
    action = read_text(ACTION)
    geom = read_text(GEOM)

    section("PART 1: LANE NOTE VERDICT")
    if check(
        "lane note says the route remains pinned-observable",
        "pinned-observable lane" in note.lower(),
        "the note must not claim the physical unit map is already derived",
    ):
        n_pass += 1
    else:
        n_fail += 1

    if check(
        "lane note names the discrete gravity/action unit-map theorem as the strongest candidate",
        "discrete gravity/action unit-map theorem" in note.lower(),
        "this is the only candidate theorem that could close the remaining unit gap",
    ):
        n_pass += 1
    else:
        n_fail += 1

    section("PART 2: SOURCE EVIDENCE")
    if check(
        "gravity note stops at lattice units",
        "g_n = 1/(4 pi) in lattice units" in gravity.lower(),
        "the clean gravity chain does not yet fix SI units",
    ):
        n_pass += 1
    else:
        n_fail += 1

    if check(
        "gravity note requires one calibration for SI conversion",
        "converting to si requires one" in gravity.lower()
        and "identifying the lattice spacing with a physical length" in gravity.lower(),
        "the note explicitly defers the physical length anchor",
    ):
        n_pass += 1
    else:
        n_fail += 1

    if check(
        "action normalization still uses observation at the last step",
        "observed light bending ratio" in action.lower() and "define g as newton's constant" in action.lower(),
        "the coefficient is fixed after observational normalization",
    ):
        n_pass += 1
    else:
        n_fail += 1

    if check(
        "canonical EH equivalence is packaging-only, not a unit-map theorem",
        "packaging-only comparison note" in geom.lower() and "not a theorem problem" in geom.lower(),
        "the equivalence note closes the comparison target, not the absolute scale",
    ):
        n_pass += 1
    else:
        n_fail += 1

    section("PART 3: VERDICT")
    can_derive_unit_map = all(
        [
            "g_n = 1/(4 pi) in lattice units" in gravity.lower(),
            "converting to si requires one" in gravity.lower(),
            "observed light bending ratio" in action.lower(),
            "define g as newton's constant" in action.lower(),
            "packaging-only comparison note" in geom.lower(),
        ]
    )
    verdict = "PINNED_OBSERVABLE" if can_derive_unit_map else "UNDECIDED"
    print(f"  verdict: {verdict}")
    if check(
        "current evidence supports pinned-observable status",
        verdict == "PINNED_OBSERVABLE",
        "the lane still lacks a framework-native physical scale anchor",
    ):
        n_pass += 1
    else:
        n_fail += 1

    print("\n" + "=" * 78)
    print(f"SCORECARD: {n_pass} pass, {n_fail} fail out of {n_pass + n_fail}")
    print("=" * 78)

    if n_fail:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
