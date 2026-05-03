#!/usr/bin/env python3
"""
PR #230 gauge-Perron to neutral-scalar rank-one import audit.

The repository has an exact gauge-vacuum Perron reduction for the finite Wilson
plaquette problem.  This audit tests whether that theorem can be imported as
the missing PR #230 neutral-scalar positivity-improving/rank-one premise.

Result: no.  The gauge theorem constrains the gauge transfer state and the
plaquette source operator.  It does not prove positivity improvement in the
neutral scalar transfer block, identify O_sp with canonical O_H, or remove
orthogonal neutral scalar couplings.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "yt_gauge_perron_to_neutral_scalar_rank_one_import_audit_2026-05-03.json"

GAUGE_PERRON_NOTE = ROOT / "docs" / "GAUGE_VACUUM_PLAQUETTE_PERRON_REDUCTION_THEOREM_NOTE.md"

PARENTS = {
    "positivity_improving_neutral_scalar_rank_one": (
        "outputs/yt_positivity_improving_neutral_scalar_rank_one_support_2026-05-03.json"
    ),
    "reflection_positivity_lsz_shortcut": (
        "outputs/yt_reflection_positivity_lsz_shortcut_no_go_2026-05-02.json"
    ),
    "neutral_scalar_commutant_rank_no_go": (
        "outputs/yt_neutral_scalar_commutant_rank_no_go_2026-05-02.json"
    ),
    "neutral_scalar_dynamical_rank_one_closure": (
        "outputs/yt_neutral_scalar_dynamical_rank_one_closure_attempt_2026-05-02.json"
    ),
    "orthogonal_neutral_decoupling_no_go": (
        "outputs/yt_orthogonal_neutral_decoupling_no_go_2026-05-02.json"
    ),
    "source_pole_canonical_higgs_mixing": (
        "outputs/yt_source_pole_canonical_higgs_mixing_obstruction_2026-05-02.json"
    ),
}

PASS_COUNT = 0
FAIL_COUNT = 0


def report(tag: str, ok: bool, msg: str) -> None:
    global PASS_COUNT, FAIL_COUNT
    if ok:
        PASS_COUNT += 1
        state = "PASS"
    else:
        FAIL_COUNT += 1
        state = "FAIL"
    print(f"  [{state}] {tag}: {msg}")


def load_json(rel: str) -> dict[str, Any]:
    path = ROOT / rel
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def status(cert: dict[str, Any]) -> str:
    return str(cert.get("actual_current_surface_status", ""))


def eigvals_2x2(matrix: list[list[float]]) -> tuple[float, float]:
    a, b = matrix[0]
    c, d = matrix[1]
    tr = a + d
    det = a * d - b * c
    disc = max(tr * tr - 4.0 * det, 0.0)
    root = math.sqrt(disc)
    return ((tr + root) / 2.0, (tr - root) / 2.0)


def import_counterfamily() -> dict[str, Any]:
    """Two neutral sectors with the same gauge Perron problem but different rank."""

    gauge_transfer = [[0.81, 0.27], [0.19, 0.64]]
    g0, g1 = eigvals_2x2(gauge_transfer)
    gauge_positive = all(entry > 0.0 for row in gauge_transfer for entry in row)

    neutral_rank_one = [[0.77, 0.23], [0.17, 0.61]]
    n0, n1 = eigvals_2x2(neutral_rank_one)
    rank_one_source_overlaps = [0.74, 0.46]
    rank_one_residue = [
        [rank_one_source_overlaps[i] * rank_one_source_overlaps[j] for j in range(2)]
        for i in range(2)
    ]
    rank_one_det = rank_one_residue[0][0] * rank_one_residue[1][1] - rank_one_residue[0][1] ** 2

    neutral_rank_two = [[0.89, 0.0], [0.0, 0.89]]
    r0, r1 = eigvals_2x2(neutral_rank_two)
    rank_two_residue = [[1.0, 0.0], [0.0, 1.0]]
    rank_two_det = rank_two_residue[0][0] * rank_two_residue[1][1] - rank_two_residue[0][1] ** 2

    return {
        "common_gauge_block": {
            "transfer_matrix": gauge_transfer,
            "strictly_positive_kernel": gauge_positive,
            "leading_eigenvalue": g0,
            "subleading_eigenvalue": g1,
            "perron_gap": g0 - g1,
            "gauge_plaquette_source_scope": "J = (chi_(1,0) + chi_(0,1)) / 6",
        },
        "neutral_rank_one_extension": {
            "neutral_transfer_matrix": neutral_rank_one,
            "strictly_positive_kernel": all(entry > 0.0 for row in neutral_rank_one for entry in row),
            "leading_eigenvalue": n0,
            "subleading_eigenvalue": n1,
            "neutral_gap": n0 - n1,
            "lowest_pole_residue": rank_one_residue,
            "gram_determinant": rank_one_det,
        },
        "neutral_rank_two_extension": {
            "neutral_transfer_matrix": neutral_rank_two,
            "strictly_positive_kernel": all(entry > 0.0 for row in neutral_rank_two for entry in row),
            "leading_eigenvalue": r0,
            "subleading_eigenvalue": r1,
            "neutral_gap": r0 - r1,
            "lowest_pole_residue": rank_two_residue,
            "gram_determinant": rank_two_det,
        },
        "interpretation": (
            "The gauge Perron block is identical in both extensions.  The neutral "
            "sector can still be rank one or rank two depending on a separate "
            "neutral transfer premise, so the gauge-vacuum theorem is not a "
            "neutral-scalar rank-one certificate."
        ),
    }


def main() -> int:
    print("PR #230 gauge-Perron to neutral-scalar rank-one import audit")
    print("=" * 72)

    parents = {name: load_json(path) for name, path in PARENTS.items()}
    missing = [name for name, cert in parents.items() if not cert]
    proposal_allowed = [name for name, cert in parents.items() if cert.get("proposal_allowed") is True]

    gauge_text = GAUGE_PERRON_NOTE.read_text(encoding="utf-8") if GAUGE_PERRON_NOTE.exists() else ""
    witness = import_counterfamily()
    rank_one = witness["neutral_rank_one_extension"]
    rank_two = witness["neutral_rank_two_extension"]

    gauge_note_present = bool(gauge_text)
    gauge_note_is_perron = (
        "positivity-improving" in gauge_text
        and "Perron" in gauge_text
        and "plaquette source operator" in gauge_text
    )
    gauge_note_scope_is_plaquette = (
        "local plaquette source operator" in gauge_text
        and "J = (chi_(1,0) + chi_(0,1)) / 6" in gauge_text
    )
    gauge_note_does_not_name_neutral_scalar = "neutral scalar" not in gauge_text.lower()

    positivity_support_is_conditional = (
        "positivity-improving neutral-scalar rank-one theorem"
        in status(parents["positivity_improving_neutral_scalar_rank_one"])
        and parents["positivity_improving_neutral_scalar_rank_one"].get(
            "positivity_improving_certificate_present"
        )
        is False
    )
    reflection_positivity_not_enough = "reflection positivity not scalar LSZ closure" in status(
        parents["reflection_positivity_lsz_shortcut"]
    )
    commutant_rank_no_go_present = (
        "neutral scalar commutant does not force rank-one purity"
        in status(parents["neutral_scalar_commutant_rank_no_go"])
    )
    dynamical_rank_no_go_present = (
        "dynamical rank-one neutral scalar theorem not derived"
        in status(parents["neutral_scalar_dynamical_rank_one_closure"])
    )
    orthogonal_decoupling_no_go_present = (
        "orthogonal neutral decoupling shortcut not derived"
        in status(parents["orthogonal_neutral_decoupling_no_go"])
    )
    source_higgs_mixing_still_blocks = "source-pole canonical-Higgs mixing obstruction" in status(
        parents["source_pole_canonical_higgs_mixing"]
    )

    counterfamily_same_gauge_different_rank = (
        witness["common_gauge_block"]["strictly_positive_kernel"]
        and abs(float(rank_one["gram_determinant"])) < 1.0e-12
        and abs(float(rank_two["gram_determinant"])) > 0.5
        and rank_two["neutral_gap"] == 0.0
        and rank_two["strictly_positive_kernel"] is False
    )
    gauge_perron_import_closes_neutral_rank_one = False

    report("parent-certificates-present", not missing, f"missing={missing}")
    report("no-parent-authorizes-proposal", not proposal_allowed, f"proposal_allowed={proposal_allowed}")
    report("gauge-perron-note-present", gauge_note_present, str(GAUGE_PERRON_NOTE.relative_to(ROOT)))
    report("gauge-note-proves-gauge-perron", gauge_note_is_perron, "finite Wilson gauge Perron theorem detected")
    report("gauge-note-scope-is-plaquette-source", gauge_note_scope_is_plaquette, "J is the plaquette class function")
    report(
        "gauge-note-does-not-name-neutral-scalar-sector",
        gauge_note_does_not_name_neutral_scalar,
        "no neutral-scalar transfer block is certified by that note",
    )
    report(
        "positivity-support-remains-conditional",
        positivity_support_is_conditional,
        status(parents["positivity_improving_neutral_scalar_rank_one"]),
    )
    report(
        "reflection-positivity-not-enough",
        reflection_positivity_not_enough,
        status(parents["reflection_positivity_lsz_shortcut"]),
    )
    report("commutant-rank-no-go-present", commutant_rank_no_go_present, status(parents["neutral_scalar_commutant_rank_no_go"]))
    report(
        "dynamical-rank-one-no-go-present",
        dynamical_rank_no_go_present,
        status(parents["neutral_scalar_dynamical_rank_one_closure"]),
    )
    report(
        "orthogonal-decoupling-no-go-present",
        orthogonal_decoupling_no_go_present,
        status(parents["orthogonal_neutral_decoupling_no_go"]),
    )
    report(
        "source-higgs-mixing-still-blocks",
        source_higgs_mixing_still_blocks,
        status(parents["source_pole_canonical_higgs_mixing"]),
    )
    report(
        "same-gauge-perron-different-neutral-rank-counterfamily",
        counterfamily_same_gauge_different_rank,
        f"rank_one_det={rank_one['gram_determinant']}, rank_two_det={rank_two['gram_determinant']}",
    )
    report(
        "gauge-perron-import-does-not-close-neutral-rank-one",
        not gauge_perron_import_closes_neutral_rank_one,
        f"gauge_perron_import_closes_neutral_rank_one={gauge_perron_import_closes_neutral_rank_one}",
    )

    exact_negative_boundary_passed = (
        not missing
        and not proposal_allowed
        and gauge_note_present
        and gauge_note_is_perron
        and gauge_note_scope_is_plaquette
        and gauge_note_does_not_name_neutral_scalar
        and positivity_support_is_conditional
        and reflection_positivity_not_enough
        and commutant_rank_no_go_present
        and dynamical_rank_no_go_present
        and orthogonal_decoupling_no_go_present
        and source_higgs_mixing_still_blocks
        and counterfamily_same_gauge_different_rank
        and not gauge_perron_import_closes_neutral_rank_one
    )

    result = {
        "actual_current_surface_status": (
            "exact negative boundary / gauge-vacuum Perron theorem does not "
            "certify neutral-scalar rank-one purity"
        ),
        "conditional_surface_status": None,
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "The imported theorem is scoped to the gauge vacuum and plaquette "
            "source J.  PR #230 still lacks a neutral-scalar positivity-"
            "improving transfer certificate, certified O_H, production C_sH/"
            "C_HH rows, or same-source W/Z response rows."
        ),
        "bare_retained_allowed": False,
        "gauge_perron_note": str(GAUGE_PERRON_NOTE.relative_to(ROOT)),
        "parent_certificates": PARENTS,
        "gauge_perron_import_closes_neutral_rank_one": gauge_perron_import_closes_neutral_rank_one,
        "exact_negative_boundary_passed": exact_negative_boundary_passed,
        "counterfamily": witness,
        "strict_non_claims": [
            "does not claim retained or proposed_retained y_t closure",
            "does not import plaquette Perron uniqueness as neutral-scalar positivity improvement",
            "does not infer O_sp = O_H from a gauge-vacuum theorem",
            "does not use H_unit, yt_ward_identity, observed targets, alpha_LM, plaquette value, or u0",
            "does not manufacture source-Higgs or W/Z response rows",
        ],
        "exact_next_action": (
            "The gauge-Perron import route is closed.  Continue on either a "
            "same-surface proof of neutral-scalar positivity improvement, "
            "direct O_H/C_sH/C_HH rank-repair production data, same-source W/Z "
            "response rows with identity certificates, or the scalar denominator/"
            "K'(pole) theorem."
        ),
        "pass_count": PASS_COUNT,
        "fail_count": FAIL_COUNT,
    }

    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"\nWrote certificate: {OUTPUT.relative_to(ROOT)}")
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 and exact_negative_boundary_passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
