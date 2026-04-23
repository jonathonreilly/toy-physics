#!/usr/bin/env python3
"""Audit the reduced boundary-density route honestly.

This is not a derivation harness. It encodes the sharper route statement:
  - the current free-fermion RT route is ruled out by the Widom no-go
  - the current bounded boundary-law probe is too weak
  - any surviving boundary-density theorem must use a new gravitational carrier
"""

from __future__ import annotations

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
NOTE = ROOT / "docs/PLANCK_SCALE_BOUNDARY_DENSITY_ROUTE_REDUCTION_NOTE_2026-04-23.md"
CLASS = ROOT / "docs/PLANCK_SCALE_UNIT_BEARING_CANDIDATE_CLASSIFICATION_THEOREM_2026-04-23.md"
BH = ROOT / "docs/BH_ENTROPY_RT_RATIO_WIDOM_NO_GO_NOTE.md"
HOLO = ROOT / "docs/HOLOGRAPHIC_PROBE_NOTE_2026-04-11.md"
ROBUST = ROOT / "docs/BOUNDARY_LAW_ROBUSTNESS_NOTE_2026-04-11.md"


def section(title: str) -> None:
    print("\n" + "=" * 78)
    print(title)
    print("=" * 78)


def check(label: str, passed: bool, detail: str) -> bool:
    tag = "PASS" if passed else "FAIL"
    print(f"  [{tag}] {label}")
    print(f"         {detail}")
    return passed


def normalized(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").split()).lower()


def main() -> int:
    note = normalized(NOTE)
    cls = normalized(CLASS)
    bh = normalized(BH)
    holo = normalized(HOLO)
    robust = normalized(ROBUST)

    n_pass = 0
    n_fail = 0

    print("Planck boundary-density route reduction audit")
    print("=" * 78)

    section("PART 1: UPSTREAM ELIMINATION")
    p = check(
        "classification theorem leaves boundary-density as one surviving class",
        "boundary-density theorem" in cls,
        "the broader candidate menu already narrowed to a boundary-density target class",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "BH Widom no-go rules out the current free-fermion RT route",
        "c_widom = 1/6" in bh
        and ("1 / 4" in bh or "1/4" in bh)
        and ("free-fermion" in bh or "current carrier" in bh),
        "the current free-fermion horizon carrier cannot land the BH coefficient exactly",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("PART 2: CURRENT BOUNDARY-LAW SURFACES")
    p = check(
        "holographic probe is bounded and explicitly non-BH",
        "bounded companion" in holo and "establish a bekenstein-hawking law" in holo,
        "boundary preference exists, but the note explicitly refuses a BH-law claim",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "boundary-law robustness note is only a support addendum",
        "supporting robustness note" in robust and "not, by itself, a holography proof" in robust,
        "robustness of boundary scaling does not upgrade the coefficient theorem",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("PART 3: REDUCED ROUTE VERDICT")
    p = check(
        "route-reduction note requires a new gravitational carrier",
        "new gravitational carrier theorem" in note
        or "new admissible same-surface carrier" in note,
        "the surviving route cannot be a relabeling of current free-fermion/boundary-law surfaces",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "route-reduction note rejects reuse of the current free-fermion machinery",
        "free-fermion" in note and "answer: no." in note,
        "the strategy statement is now explicit rather than implied",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("FINAL VERDICT")
    verdict = (
        "Boundary-density route survives only as a NEW gravitational-carrier "
        "theorem target. The current free-fermion RT and bounded boundary-law "
        "surfaces are not sufficient."
    )
    print(f"  {verdict}")

    print("\n" + "=" * 78)
    print(f"SCORECARD: {n_pass} pass, {n_fail} fail out of {n_pass + n_fail}")
    print("=" * 78)

    return 0 if n_fail == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
