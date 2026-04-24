#!/usr/bin/env python3
"""Verifier for the bare-cell-alone Planck closure program note."""

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
    note = read("docs/PLANCK_SCALE_BARE_CELL_ALONE_CLOSURE_PROGRAM_2026-04-23.md")
    airtight = read("docs/PLANCK_SCALE_AIRTIGHT_REVIEW_CLOSURE_THEOREM_2026-04-23.md")
    source_free = read("docs/PLANCK_SCALE_SOURCE_FREE_DEFAULT_DATUM_FROM_ONE_AXIOM_THEOREM_2026-04-23.md")
    same_surface = read("docs/PLANCK_SCALE_GRAVITY_SECTOR_SAME_SURFACE_CLOSURE_THEOREM_2026-04-23.md")
    reviewer = read("docs/PLANCK_SCALE_REVIEWER_CANONICAL_SUBMISSION_PACKET_2026-04-23.md")

    passed = 0
    total = 0

    total += 1
    passed += expect(
        "not-submitted-as-current-planck-theorem",
        "not the submitted Planck theorem" in note
        and "Yes, as a theorem on the accepted physical-gravity review contract" in airtight,
        "the stronger target is separated from the submitted closure",
    )

    total += 1
    passed += expect(
        "undefinability-without-semantics",
        "no physical lattice semantics means `a` is only an index spacing" in note
        and "no state semantics means `Tr(rho P_A)` has no canonical `rho`" in note
        and "no gravity-sector semantics means there is no `G`" in note,
        "the note explains why bare algebra alone is not yet a Planck statement",
    )

    total += 1
    passed += expect(
        "four-upgrade-targets-present",
        "B1. Physical-Lattice Semantics From Algebra" in note
        and "B2. Source-Free State From Algebra" in note
        and "B3. Gravity Sector From Algebra" in note
        and "B4. Same-Surface Boundary Representative From Algebra" in note,
        "all required semantic derivations are enumerated",
    )

    total += 1
    passed += expect(
        "canonical-state-route-identified",
        "unique automorphism-natural finite-cell state" in note
        and "rho_cell = I_16/16" in note
        and "`rho_cell = I_16 / 16`" in source_free,
        "source-free state premise has a concrete algebraic upgrade route",
    )

    total += 1
    passed += expect(
        "gravity-hardest-step-identified",
        "Gravity-from-algebra theorem" in note
        and "Still open: derive soldered metricity" in note
        and "same-surface single-sector compatibility forces GSI" in same_surface,
        "the note does not pretend gravity-sector derivation is already done",
    )

    total += 1
    passed += expect(
        "pure-algebra-scale-obstruction",
        "the replacement `a -> lambda a` leaves the abstract `Z^3` incidence algebra" in note
        and "unchanged" in note
        and "`l_P^2 = hbar G/c_light^3` contains dimensional physical constants" in note,
        "the no-free-lunch scale obstruction is explicit",
    )

    total += 1
    passed += expect(
        "current-versus-future-claim-separated",
        "Planck is closed on the accepted physical-gravity review contract" in note
        and "Do not claim the stronger sentence until B1-B4 are theorem-grade" in note,
        "the note gives safe current and future claims",
    )

    total += 1
    passed += expect(
        "where-when-pins-are-address-not-units",
        "Where/When Pins" in note
        and "address pins" in note
        and "choose a microscopic tick count" in note
        and "not fair as hidden unit\nmaps" in note,
        "where/when pins are admitted only as address data",
    )

    total += 1
    passed += expect(
        "reviewer-packet-links-program",
        "PLANCK_SCALE_BARE_CELL_ALONE_CLOSURE_PROGRAM_2026-04-23.md" in reviewer,
        "canonical packet links the stronger-target program as non-current scope",
    )

    print(f"SUMMARY: PASS={passed} FAIL={total - passed}")
    return 0 if passed == total else 1


if __name__ == "__main__":
    raise SystemExit(main())
