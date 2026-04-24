#!/usr/bin/env python3
"""Verifier for the B4 boundary representative after-gravity theorem."""

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
    note = read("docs/PLANCK_SCALE_BARE_BOUNDARY_REPRESENTATIVE_AFTER_GRAVITY_THEOREM_2026-04-23.md")
    same_surface = read("docs/PLANCK_SCALE_GRAVITY_SECTOR_SAME_SURFACE_CLOSURE_THEOREM_2026-04-23.md")
    carrier = read("docs/PLANCK_SCALE_GRAVITY_CARRIER_FROM_SECTOR_IDENTIFICATION_THEOREM_2026-04-23.md")
    state = read("docs/PLANCK_SCALE_BARE_FINITE_CELL_CANONICAL_STATE_THEOREM_2026-04-23.md")
    reviewer = read("docs/PLANCK_SCALE_REVIEWER_CANONICAL_SUBMISSION_PACKET_2026-04-23.md")

    passed = 0
    total = 0

    total += 1
    passed += expect(
        "b4-conditional-closure",
        "Once B3 is closed, B4 follows" in note
        and "conditional only on B3" in note,
        "B4 is explicitly conditional on deriving gravity",
    )

    total += 1
    passed += expect(
        "representative-is-pa",
        "`N_grav = P_A`" in note
        and "`N_grav = P_A`" in same_surface
        and "`N_grav = P_A`" in carrier,
        "same-surface representative is P_A",
    )

    total += 1
    passed += expect(
        "admissibility-conditions-listed",
        "time-complete" in note
        and "spatially isotropic" in note
        and "unit-valued" in note
        and "free of quotienting" in note,
        "the primitive representative conditions are stated",
    )

    total += 1
    passed += expect(
        "quarter-follows-with-bare-state",
        "`rho_cell = I_16 / 16`" in note
        and "`c_cell = Tr(rho_cell N_grav) = Tr((I_16/16) P_A) = 1/4`" in note
        and "This closes B2" in state,
        "B4 plus B2 gives the Planck quarter",
    )

    total += 1
    passed += expect(
        "no-gravity-overclaim",
        "B4 alone derives the gravity/action sector" in note
        and "remaining bare-cell-alone gap is exactly B3, not B4" in note,
        "B4 does not pretend to derive gravity",
    )

    total += 1
    passed += expect(
        "reviewer-links-b4",
        "PLANCK_SCALE_BARE_BOUNDARY_REPRESENTATIVE_AFTER_GRAVITY_THEOREM_2026-04-23.md" in reviewer,
        "canonical packet links the B4 theorem",
    )

    print(f"SUMMARY: PASS={passed} FAIL={total - passed}")
    return 0 if passed == total else 1


if __name__ == "__main__":
    raise SystemExit(main())
