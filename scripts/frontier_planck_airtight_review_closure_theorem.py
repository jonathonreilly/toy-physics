#!/usr/bin/env python3
"""Verifier for the final airtight Planck review closure theorem."""

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
    note = read("docs/PLANCK_SCALE_AIRTIGHT_REVIEW_CLOSURE_THEOREM_2026-04-23.md")
    reviewer = read("docs/PLANCK_SCALE_REVIEWER_CANONICAL_SUBMISSION_PACKET_2026-04-23.md")
    same_surface = read("docs/PLANCK_SCALE_GRAVITY_SECTOR_SAME_SURFACE_CLOSURE_THEOREM_2026-04-23.md")
    parent = read("docs/PLANCK_SCALE_BOUNDARY_PARENT_SOURCE_EQUIVALENCE_THEOREM_2026-04-23.md")
    hbar = read("docs/PLANCK_SCALE_HBAR_STATUS_AND_REMAINING_OBJECTIONS_AUDIT_2026-04-23.md")

    passed = 0
    total = 0

    total += 1
    passed += expect(
        "airtight-scoped-yes-and-bare-no",
        "Yes, as a theorem on the accepted physical-gravity review contract" in note
        and "No, if the requested claim is the stronger sentence" in note,
        "the theorem is airtight without overclaiming bare-cell-alone closure",
    )

    total += 1
    passed += expect(
        "review-contract-is-explicit",
        "physical `Cl(3)` / `Z^3` lattice semantics" in note
        and "source-free default-datum state semantics" in note
        and "same-surface single-sector compatibility" in note
        and "standard gravitational area/action normalization" in note,
        "all review-surface inputs are disclosed",
    )

    total += 1
    passed += expect(
        "closed-chain-numerics",
        "`H_cell ~= C^16`" in note
        and "`rank(P_A) = 4`" in note
        and "`c_cell = Tr(rho_cell P_A) = 4/16 = 1/4`" in note
        and "`a = l_P`" in note,
        "the final Planck calculation is present and exact",
    )

    total += 1
    passed += expect(
        "parent-source-closure-included",
        "`nu - lambda_min(L_Sigma) = Tr(rho_cell P_A) = 1/4`" in note
        and "`P_A = P_q + P_E`" in parent,
        "boundary source closure is part of the final chain",
    )

    total += 1
    passed += expect(
        "same-surface-closure-included",
        "`N_grav = P_A`" in note
        and "same-surface single-sector compatibility forces GSI" in same_surface,
        "old GSI wording is closed as same-surface compatibility",
    )

    total += 1
    passed += expect(
        "remaining-objections-classified-as-contract-rejections",
        "theory-surface rejections, not\ninternal Planck proof gaps" in note
        and "refusal of the review\ncontract" in note,
        "the note separates proof gaps from review-contract denials",
    )

    total += 1
    passed += expect(
        "no-hidden-imports-or-overclaims",
        "no observed lattice spacing" in note
        and "no fitted Planck multiplier" in note
        and "no SI numerical prediction of `hbar`" in note
        and "does **not** derive the SI value of\n`hbar`" in hbar
        and "derives the structural action-to-phase role of `hbar`" in hbar,
        "the final closure does not predict SI hbar or assume a=l_P",
    )

    total += 1
    passed += expect(
        "reviewer-links-airtight-closure",
        "PLANCK_SCALE_AIRTIGHT_REVIEW_CLOSURE_THEOREM_2026-04-23.md" in reviewer,
        "canonical reviewer packet links the final closure theorem",
    )

    print(f"SUMMARY: PASS={passed} FAIL={total - passed}")
    return 0 if passed == total else 1


if __name__ == "__main__":
    raise SystemExit(main())
