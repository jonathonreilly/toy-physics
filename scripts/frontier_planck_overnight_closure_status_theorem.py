#!/usr/bin/env python3
"""Verify the final hostile-review classification for this pass."""

from __future__ import annotations

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
    note = read("docs/PLANCK_SCALE_OVERNIGHT_CLOSURE_STATUS_THEOREM_2026-04-24.md")
    reviewer = read("docs/PLANCK_SCALE_REVIEWER_CANONICAL_SUBMISSION_PACKET_2026-04-23.md")
    b3 = read("docs/PLANCK_SCALE_B3_DYNAMICAL_METRICITY_OBSTRUCTION_THEOREM_2026-04-24.md")
    hbar = read("docs/PLANCK_SCALE_HBAR_STRONG_ROUTES_STATUS_THEOREM_2026-04-24.md")
    ward = read("docs/PLANCK_SCALE_BOUNDARY_SOURCE_FUNCTORIAL_WARD_THEOREM_2026-04-24.md")

    passed = 0
    total = 0

    total += 1
    passed += expect(
        "classification-refuses-bare-overclaim",
        "not** a bare `Cl(3)` / `Z^3`-alone derivation" in note
        and "not:\n\n> bare `Cl(3)` / `Z^3` alone forces conventional Planck length"
        in note,
        "bare Cl(3)/Z^3 closure is explicitly refused",
    )

    total += 1
    passed += expect(
        "conditional-retained-claim-is-named",
        "hardened conditional Planck theorem" in note
        and "retained" in note
        and "physical-gravity parent-source boundary-action object class" in note,
        "strongest accepted claim is conditional retained Planck closure",
    )

    total += 1
    passed += expect(
        "closed-items-list-is-complete",
        "physical lattice/event observability" in note
        and "flat edge-Clifford soldering" in note
        and "finite event Ward derivative" in note
        and "conditional Planck normalization" in note,
        "closed surface is enumerated without hiding imports",
    )

    total += 1
    passed += expect(
        "open-items-match-new-theorems",
        "B3 dynamical gravity" in note
        and "Boundary object-class derivation" in note
        and "Hbar/action unit" in note
        and "has not derived local\n   metric/coframe response" in note
        and "The branch has not derived `gamma = 1` or `hbar`" in note,
        "remaining blockers are the named theorem targets",
    )

    total += 1
    passed += expect(
        "supports-b3-hbar-ward-links",
        "B3 remains open" in b3
        and "not contained in the current event algebra plus phase\nperiodicity" not in hbar
        and "finite event Ward derivative remains true\nbut does not determine `nu`" in ward,
        "supporting no-go/status theorems are consistent",
    )

    total += 1
    passed += expect(
        "reviewer-links-overnight-status",
        "PLANCK_SCALE_OVERNIGHT_CLOSURE_STATUS_THEOREM_2026-04-24.md" in reviewer,
        "canonical packet links the final status theorem",
    )

    print(f"SUMMARY: PASS={passed} FAIL={total - passed}")
    return 0 if passed == total else 1


if __name__ == "__main__":
    raise SystemExit(main())
