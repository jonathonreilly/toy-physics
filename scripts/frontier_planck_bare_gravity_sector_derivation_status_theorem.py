#!/usr/bin/env python3
"""Verifier for the B3 bare gravity-sector derivation status theorem."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(rel: str) -> str:
    return (ROOT / rel).read_text()


def expect(name: str, cond: bool, detail: str) -> int:
    if cond:
        print(f"PASS: {name} - {detail}")
        return 1
    print(f"FAIL: {name} - {detail}")
    return 0


def main() -> int:
    note = read("docs/PLANCK_SCALE_BARE_GRAVITY_SECTOR_DERIVATION_STATUS_THEOREM_2026-04-23.md")
    qg = read("docs/UNIVERSAL_QG_CANONICAL_TEXTBOOK_CONTINUUM_GR_CLOSURE_NOTE.md")
    same_surface = read("docs/PLANCK_SCALE_GRAVITY_SECTOR_SAME_SURFACE_CLOSURE_THEOREM_2026-04-23.md")
    program = read("docs/PLANCK_SCALE_BARE_CELL_ALONE_CLOSURE_PROGRAM_2026-04-23.md")
    reviewer = read("docs/PLANCK_SCALE_REVIEWER_CANONICAL_SUBMISSION_PACKET_2026-04-23.md")

    passed = 0
    total = 0

    total += 1
    passed += expect(
        "b3-not-overclaimed",
        "Not yet as a bare-cell-alone theorem" in note
        and "B3 is not closed" in note,
        "B3 remains a reduction target rather than a claimed closure",
    )

    total += 1
    passed += expect(
        "existing-gravity-stack-recorded",
        "canonical local gravitational boundary/action family" in note
        and "Lorentzian Einstein/Regge stationary action family" in note
        and "canonical textbook continuum\ngravity" not in note
        and "chosen canonical textbook target" in qg,
        "the existing accepted gravity stack is acknowledged",
    )

    total += 1
    passed += expect(
        "exact-b3-target-present",
        "Exact B3 Target" in note
        and "unique nontrivial long-distance\n> geometric action sector" in note,
        "the missing theorem is stated precisely",
    )

    total += 1
    passed += expect(
        "b4-waits-on-b3",
        "B4 is waiting only on B3" in note
        and "`N_grav = P_A`" in same_surface,
        "boundary representative is not the current hard part",
    )

    total += 1
    passed += expect(
        "hardness-criteria-listed",
        "locality" in note
        and "tensorial covariance" in note
        and "second-order continuum/stationary consistency" in note,
        "the uniqueness criteria are exposed",
    )

    total += 1
    passed += expect(
        "program-b3-consistent",
        "B3. Gravity Sector From Algebra" in program
        and "Gravity-from-algebra theorem" in program,
        "bare-cell program points to the same B3 target",
    )

    total += 1
    passed += expect(
        "reviewer-links-b3-status",
        "PLANCK_SCALE_BARE_GRAVITY_SECTOR_DERIVATION_STATUS_THEOREM_2026-04-23.md" in reviewer,
        "canonical packet links the B3 status theorem",
    )

    print(f"SUMMARY: PASS={passed} FAIL={total - passed}")
    return 0 if passed == total else 1


if __name__ == "__main__":
    raise SystemExit(main())
