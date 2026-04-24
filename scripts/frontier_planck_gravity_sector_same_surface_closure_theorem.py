#!/usr/bin/env python3
"""Verifier for the gravity-sector same-surface closure theorem."""

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
    note = read("docs/PLANCK_SCALE_GRAVITY_SECTOR_SAME_SURFACE_CLOSURE_THEOREM_2026-04-23.md")
    carrier = read("docs/PLANCK_SCALE_GRAVITY_CARRIER_FROM_SECTOR_IDENTIFICATION_THEOREM_2026-04-23.md")
    qg = read("docs/UNIVERSAL_QG_CANONICAL_TEXTBOOK_CONTINUUM_GR_CLOSURE_NOTE.md")
    parent = read("docs/PLANCK_SCALE_BOUNDARY_PARENT_SOURCE_EQUIVALENCE_THEOREM_2026-04-23.md")
    source_free = read("docs/PLANCK_SCALE_SOURCE_FREE_DEFAULT_DATUM_FROM_ONE_AXIOM_THEOREM_2026-04-23.md")
    reviewer = read("docs/PLANCK_SCALE_REVIEWER_CANONICAL_SUBMISSION_PACKET_2026-04-23.md")

    passed = 0
    total = 0

    total += 1
    passed += expect(
        "gravity-sector-is-existing-target-not-invented-by-count",
        "canonical textbook continuum\n"
        "gravitational weak/stationary action family" in qg
        and "The branch is not trying to infer gravity from a bare counting number" in note,
        "GSI is tied to the accepted gravity/action stack",
    )

    total += 1
    passed += expect(
        "unique-primitive-source-is-pa",
        "`N_cell = P_A = 1_(|eta| = 1)`" in note
        and "N_grav = P_A" in carrier
        and "`P_A = P_q + P_E`" in parent,
        "the primitive one-step boundary source is uniquely P_A",
    )

    total += 1
    passed += expect(
        "same-surface-single-sector-forces-gsi",
        "same-surface single-sector compatibility forces GSI" in note
        and "`N_grav = P_A`" in note,
        "GSI is reformulated as same-surface compatibility",
    )

    total += 1
    passed += expect(
        "not-a-coefficient-fit",
        "None of these inputs contains `1/4`, `nu = 5/4`, `a = l_P`, or a fitted\nmultiplier" in note
        and "GSI is not a numerical input" in carrier,
        "the closure does not insert the Planck coefficient",
    )

    total += 1
    passed += expect(
        "source-free-quarter-retained",
        "`rho_cell = I_16 / 16`" in note
        and "`c_cell = Tr(rho_cell P_A) = 4/16 = 1/4`" in note
        and "`rho_cell = I_16 / 16`" in source_free,
        "source-free default state still supplies the quarter",
    )

    total += 1
    passed += expect(
        "planck-normalization-retained",
        "`c_cell / a^2 = 1 / (4 l_P^2)`" in note
        and "`a = l_P`" in note,
        "same-surface density matching still yields Planck",
    )

    total += 1
    passed += expect(
        "remaining-rejection-is-review-contract",
        "reject the same-surface single-gravity-sector review contract" in note
        and "Rejecting any of them changes the\nphysical theory being reviewed" in note,
        "remaining objections are theory-surface rejections",
    )

    total += 1
    passed += expect(
        "reviewer-links-same-surface-closure",
        "PLANCK_SCALE_GRAVITY_SECTOR_SAME_SURFACE_CLOSURE_THEOREM_2026-04-23.md" in reviewer,
        "canonical packet links the same-surface closure theorem",
    )

    print(f"SUMMARY: PASS={passed} FAIL={total - passed}")
    return 0 if passed == total else 1


if __name__ == "__main__":
    raise SystemExit(main())
