#!/usr/bin/env python3
"""
PR #230 orthogonal-neutral top-coupling exclusion candidate gate.

The same-surface multiplicity-one candidate can be repaired by any one of
several genuine artifacts.  This runner targets the selection-rule option:
does the current post-FMS/two-source/finite-row surface now exclude a top
coupling for the orthogonal neutral singlet?

It does not.  The finite two-source rows measure source/complement
correlator entries, while the post-FMS counterfamily shows the same measured
source response is compatible with different canonical y_t values after an
orthogonal top coupling is adjusted.  No current same-surface charge,
representation, action, or row packet forces that orthogonal coupling to
zero.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = (
    ROOT
    / "outputs"
    / "yt_pr230_orthogonal_top_coupling_exclusion_candidate_gate_2026-05-07.json"
)

PARENTS = {
    "legacy_selection_rule_no_go": "outputs/yt_no_orthogonal_top_coupling_selection_rule_no_go_2026-05-02.json",
    "same_surface_candidate": "outputs/yt_pr230_same_surface_neutral_multiplicity_one_certificate_2026-05-07.json",
    "same_surface_gate": "outputs/yt_pr230_same_surface_neutral_multiplicity_one_gate_2026-05-07.json",
    "post_fms_source_overlap": "outputs/yt_pr230_post_fms_source_overlap_necessity_gate_2026-05-06.json",
    "primitive_transfer_candidate": "outputs/yt_pr230_two_source_taste_radial_primitive_transfer_candidate_gate_2026-05-07.json",
    "source_higgs_overlap_kappa_contract": "outputs/yt_pr230_source_higgs_overlap_kappa_contract_2026-05-06.json",
    "source_higgs_builder": "outputs/yt_source_higgs_cross_correlator_certificate_builder_2026-05-03.json",
    "source_higgs_gram": "outputs/yt_source_higgs_gram_purity_gate_2026-05-02.json",
    "neutral_primitive_route_completion": "outputs/yt_pr230_neutral_primitive_route_completion_2026-05-06.json",
    "retained_route": "outputs/yt_retained_closure_route_certificate_2026-05-01.json",
    "campaign_status": "outputs/yt_pr230_campaign_status_certificate_2026-05-01.json",
}

FORBIDDEN_FIREWALL = {
    "sets_orthogonal_top_coupling_to_zero_by_assumption": False,
    "uses_H_unit_matrix_element_readout": False,
    "uses_yt_ward_identity": False,
    "uses_observed_targets": False,
    "uses_alpha_lm_plaquette_u0": False,
    "uses_reduced_pilot_evidence": False,
    "treats_C_sx_as_top_coupling_tomography": False,
    "treats_taste_radial_x_as_canonical_O_H": False,
    "sets_kappa_s_c2_or_Z_match_to_one": False,
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


def load(rel: str) -> dict[str, Any]:
    path = ROOT / rel
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def status(cert: dict[str, Any]) -> str:
    return str(cert.get("actual_current_surface_status", ""))


def finite(value: Any) -> bool:
    return isinstance(value, (int, float)) and math.isfinite(float(value))


def orthogonal_counterfamily_ok(rows: list[dict[str, Any]]) -> bool:
    if len(rows) < 2:
        return False
    same_source = {row.get("same_source_y") for row in rows}
    canonical = {row.get("canonical_y_t") for row in rows}
    return (
        len(same_source) == 1
        and len(canonical) > 1
        and all(finite(row.get("orthogonal_y_chi_required")) for row in rows)
    )


def mode_sign_mixture(mode_summary: dict[str, Any]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for mode, row in sorted(mode_summary.items()):
        if not isinstance(row, dict):
            continue
        signs = row.get("C_sx_sign_counts", {})
        if not isinstance(signs, dict):
            continue
        result[mode] = {
            "positive": signs.get("positive"),
            "negative": signs.get("negative"),
            "zero": signs.get("zero"),
            "mixed_signs": bool(signs.get("positive")) and bool(signs.get("negative")),
            "all_blocks_positive_definite": row.get("all_blocks_positive_definite"),
            "offdiagonal_entry_observed": row.get("offdiagonal_entry_observed"),
        }
    return result


def main() -> int:
    print("PR #230 orthogonal-neutral top-coupling exclusion candidate gate")
    print("=" * 78)

    parents = {name: load(path) for name, path in PARENTS.items()}
    statuses = {name: status(cert) for name, cert in parents.items()}
    missing = [name for name, cert in parents.items() if not cert]
    proposal_allowed = [
        name for name, cert in parents.items() if cert.get("proposal_allowed") is True
    ]

    primitive = parents["primitive_transfer_candidate"]
    mode_summary = primitive.get("mode_summary", {})
    sign_summary = mode_sign_mixture(mode_summary if isinstance(mode_summary, dict) else {})
    counterfamily = parents["post_fms_source_overlap"].get(
        "orthogonal_top_counterfamily", []
    )
    if not isinstance(counterfamily, list):
        counterfamily = []

    legacy_selection_rule_still_blocks = (
        "no-orthogonal-top-coupling selection rule not derived"
        in statuses["legacy_selection_rule_no_go"]
        and parents["legacy_selection_rule_no_go"].get(
            "no_orthogonal_top_coupling_selection_rule_gate_passed"
        )
        is False
        and parents["legacy_selection_rule_no_go"].get("proposal_allowed") is False
    )
    same_surface_candidate_rejected = (
        "same-surface neutral multiplicity-one candidate attempt rejected"
        in statuses["same_surface_candidate"]
        and parents["same_surface_candidate"].get("candidate_accepted") is False
        and parents["same_surface_candidate"].get("proposal_allowed") is False
    )
    same_surface_gate_rejects_current = (
        "same-surface neutral multiplicity-one artifact intake gate"
        in statuses["same_surface_gate"]
        and parents["same_surface_gate"].get("candidate_accepted") is False
        and parents["same_surface_gate"].get("proposal_allowed") is False
    )
    post_fms_counterfamily_blocks = (
        "post-FMS source-overlap not derivable" in statuses["post_fms_source_overlap"]
        and parents["post_fms_source_overlap"].get("proposal_allowed") is False
        and orthogonal_counterfamily_ok(counterfamily)
    )
    finite_rows_not_top_tomography = (
        "finite C_sx rows do not certify a physical primitive neutral transfer"
        in statuses["primitive_transfer_candidate"]
        and primitive.get("proposal_allowed") is False
        and primitive.get("physical_transfer_candidate_accepted") is False
        and primitive.get("finite_offdiagonal_correlation_support") is True
        and primitive.get("finite_correlator_blocks_positive") is True
        and all(row.get("mixed_signs") is True for row in sign_summary.values())
    )
    source_higgs_rows_absent = (
        parents["source_higgs_builder"].get("input_present") is False
        and parents["source_higgs_builder"].get("candidate_written") is False
        and parents["source_higgs_gram"].get("source_higgs_gram_purity_gate_passed")
        is False
        and parents["source_higgs_overlap_kappa_contract"]
        .get("current_blockers", {})
        .get("source_higgs_row_packet_absent")
        is True
    )
    neutral_primitive_still_missing_h3_h4 = (
        "neutral primitive-rank-one route not complete"
        in statuses["neutral_primitive_route_completion"]
        and parents["neutral_primitive_route_completion"].get("proposal_allowed")
        is False
        and "H3" in str(parents["neutral_primitive_route_completion"])
        and "H4" in str(parents["neutral_primitive_route_completion"])
    )
    aggregate_denies_proposal = (
        parents["retained_route"].get("proposal_allowed") is False
        and parents["campaign_status"].get("proposal_allowed") is False
    )
    firewall_clean = all(value is False for value in FORBIDDEN_FIREWALL.values())
    exclusion_candidate_accepted = False

    report("parent-certificates-present", not missing, f"missing={missing}")
    report("no-parent-authorizes-proposal", not proposal_allowed, f"proposal_allowed={proposal_allowed}")
    report("legacy-selection-rule-still-blocks", legacy_selection_rule_still_blocks, statuses["legacy_selection_rule_no_go"])
    report("same-surface-candidate-still-rejected", same_surface_candidate_rejected, statuses["same_surface_candidate"])
    report("same-surface-gate-rejects-current-surface", same_surface_gate_rejects_current, statuses["same_surface_gate"])
    report("post-fms-counterfamily-keeps-source-response", post_fms_counterfamily_blocks, str(counterfamily))
    report("finite-csx-rows-not-top-coupling-tomography", finite_rows_not_top_tomography, str(sign_summary))
    report("source-higgs-pole-rows-still-absent", source_higgs_rows_absent, statuses["source_higgs_builder"])
    report("neutral-primitive-still-missing-h3-h4", neutral_primitive_still_missing_h3_h4, statuses["neutral_primitive_route_completion"])
    report("aggregate-denies-proposal", aggregate_denies_proposal, "retained/campaign proposal_allowed=false")
    report("forbidden-firewall-clean", firewall_clean, str(FORBIDDEN_FIREWALL))
    report("orthogonal-top-exclusion-candidate-not-accepted", not exclusion_candidate_accepted, "selection-rule obligation remains open")

    result = {
        "actual_current_surface_status": (
            "exact negative boundary / orthogonal-neutral top-coupling exclusion "
            "candidate rejected on current PR230 surface"
        ),
        "conditional_surface_status": (
            "conditional-support if a future same-surface charge/representation "
            "theorem, physical response row, source-Higgs Gram-purity packet, or "
            "neutral primitive transfer proves the orthogonal neutral top "
            "component is absent or measured"
        ),
        "hypothetical_axiom_status": None,
        "admitted_observation_status": None,
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "Current labels, FMS support, finite C_sx rows, and primitive-cone "
            "support do not force the orthogonal neutral scalar top coupling to "
            "zero or measure it."
        ),
        "bare_retained_allowed": False,
        "audit_required_before_effective_retained": True,
        "orthogonal_top_coupling_exclusion_candidate_accepted": exclusion_candidate_accepted,
        "same_surface_selection_rule_present": False,
        "finite_c_sx_rows_are_top_coupling_tomography": False,
        "orthogonal_top_counterfamily": counterfamily,
        "finite_mode_sign_summary": sign_summary,
        "current_blockers": {
            "legacy_selection_rule_still_blocks": legacy_selection_rule_still_blocks,
            "same_surface_candidate_rejected": same_surface_candidate_rejected,
            "post_fms_counterfamily_blocks": post_fms_counterfamily_blocks,
            "finite_rows_not_top_tomography": finite_rows_not_top_tomography,
            "source_higgs_rows_absent": source_higgs_rows_absent,
            "neutral_primitive_still_missing_h3_h4": neutral_primitive_still_missing_h3_h4,
        },
        "parent_statuses": statuses,
        "strict_non_claims": [
            "does not claim retained or proposed_retained closure",
            "does not set the orthogonal neutral top coupling to zero",
            "does not use finite C_sx/C_xx rows as top-coupling tomography",
            "does not use finite C_sx/C_xx rows as C_sH/C_HH pole rows",
            "does not set kappa_s, c2, or Z_match to one",
            "does not use H_unit, Ward identity, observed targets, alpha_LM, plaquette, u0, reduced pilots, or value recognition",
        ],
        "exact_next_action": (
            "Supply a same-surface charge/representation theorem that forbids "
            "orthogonal neutral top couplings while allowing the Higgs radial "
            "top coupling, or measure/source-Higgs-purify the orthogonal "
            "component through real C_spH/C_HH or W/Z response rows."
        ),
        "pass_count": PASS_COUNT,
        "fail_count": FAIL_COUNT,
    }
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"\nWrote certificate: {OUTPUT.relative_to(ROOT)}")
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
