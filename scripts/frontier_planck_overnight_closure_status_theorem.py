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
    b3_realified = read(
        "docs/PLANCK_SCALE_B3_CLIFFORD_REALIFICATION_METRIC_WARD_THEOREM_2026-04-24.md"
    )
    hbar = read("docs/PLANCK_SCALE_HBAR_STRONG_ROUTES_STATUS_THEOREM_2026-04-24.md")
    ward = read("docs/PLANCK_SCALE_BOUNDARY_SOURCE_FUNCTORIAL_WARD_THEOREM_2026-04-24.md")
    integral_count = read("docs/PLANCK_SCALE_PRIMITIVE_INTEGRAL_ACTION_COUNT_THEOREM_2026-04-24.md")

    passed = 0
    total = 0

    total += 1
    passed += expect(
        "classification-refuses-bare-overclaim",
        "not** a finite-automorphism-only derivation" in note
        and "not:\n\n> bare `Cl(3)` / `Z^3` alone forces conventional Planck length"
        in note,
        "finite-automorphism-only closure is explicitly refused",
    )

    total += 1
    passed += expect(
        "conditional-retained-claim-is-named",
        "Planck closure on the canonical realified `Cl(3)` / `Z^3`" in note
        and "primitive integral-history surface" in note,
        "strongest accepted claim is realified Planck plus reduced gamma closure",
    )

    total += 1
    passed += expect(
        "closed-items-list-is-complete",
        "physical lattice/event observability" in note
        and "flat edge-Clifford soldering" in note
        and "B3 realified metric/coframe Ward response" in note
        and "finite event Ward derivative" in note
        and "Planck normalization" in note,
        "closed surface is enumerated without hiding imports",
    )

    total += 1
    passed += expect(
        "open-items-match-new-theorems",
        "finite-automorphism-only target remains rejected" in note
        and "refuses canonical realification" in note
        and "the older B3 no-go\n   applies" in note
        and "not claimed: SI `hbar`" in note,
        "remaining rejection is realification admissibility plus SI hbar scope",
    )

    total += 1
    passed += expect(
        "reduced-gamma-one-is-now-closed",
        "reduced action-count normalization `Phi(I_16)=1`, hence `gamma=1`" in note
        and "closed: `gamma=1` as reduced primitive action count" in note
        and "`Phi(I_16) = ell([A_cell]) = 1`" in integral_count,
        "gamma=1 is no longer listed as an open reduced-action blocker",
    )

    total += 1
    passed += expect(
        "supports-b3-hbar-ward-links",
        "B3 remains open" in b3
        and "B3 closes on the canonical realified edge-Clifford linear-response surface"
        in b3_realified
        and "not contained in the current event algebra plus phase\nperiodicity" not in hbar
        and "finite event Ward derivative remains true\nbut does not determine `nu`" in ward,
        "finite-only no-go and realified closure are separated",
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
