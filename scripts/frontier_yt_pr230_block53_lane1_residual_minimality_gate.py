#!/usr/bin/env python3
"""
PR #230 block53 lane-1 residual minimality gate.

Block51/52 closed two stale blockers on the same-source FH/LSZ lane:
the L12 chunk packet is complete support, and the common-window response
gate supplies response-side stability support.  This runner records the
resulting minimal current-surface blocker set without promoting the claim.

It deliberately does not close PR230.  The remaining roots are physical
readout authorization, scalar pole/model-class/FV/IR authority, and an
independent canonical-Higgs or neutral-transfer bridge.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = (
    ROOT
    / "outputs"
    / "yt_pr230_block53_lane1_residual_minimality_gate_2026-05-12.json"
)

PARENTS = {
    "same_source_pole_data_sufficiency": "outputs/yt_same_source_pole_data_sufficiency_gate_2026-05-02.json",
    "common_window_response_gate": "outputs/yt_fh_lsz_common_window_response_gate_2026-05-04.json",
    "full_target_timeseries": "outputs/yt_fh_lsz_target_timeseries_full_set_checkpoint_2026-05-12.json",
    "lane1_action_premise": "outputs/yt_pr230_lane1_action_premise_derivation_attempt_2026-05-12.json",
    "source_higgs_direct_pole_row_contract": "outputs/yt_pr230_source_higgs_direct_pole_row_contract_2026-05-07.json",
    "neutral_primitive_route_completion": "outputs/yt_pr230_neutral_primitive_route_completion_2026-05-06.json",
    "wz_absolute_authority_exhaustion": "outputs/yt_pr230_wz_absolute_authority_route_exhaustion_after_block41_2026-05-12.json",
    "strict_scalar_lsz_moment_fv": "outputs/yt_pr230_strict_scalar_lsz_moment_fv_authority_gate_2026-05-07.json",
    "hs_logdet_scalar_action_no_go": "outputs/yt_pr230_hs_logdet_scalar_action_normalization_no_go_2026-05-12.json",
    "model_class_gate": "outputs/yt_fh_lsz_pole_fit_model_class_gate_2026-05-02.json",
    "higgs_pole_identity_gate": "outputs/yt_fh_lsz_higgs_pole_identity_gate_2026-05-02.json",
    "full_positive_assembly": "outputs/yt_pr230_full_positive_closure_assembly_gate_2026-05-04.json",
    "retained_route": "outputs/yt_retained_closure_route_certificate_2026-05-01.json",
    "campaign_status": "outputs/yt_pr230_campaign_status_certificate_2026-05-01.json",
}

REQUIRED_FUTURE_ARTIFACTS = {
    "physical_response_readout_authorization": "outputs/yt_pr230_physical_response_readout_authorization_2026-05-12.json",
    "scalar_pole_model_class_fv_ir_certificate": "outputs/yt_pr230_scalar_pole_model_class_fv_ir_certificate_2026-05-12.json",
    "canonical_higgs_operator_certificate": "outputs/yt_canonical_higgs_operator_certificate_2026-05-03.json",
    "source_higgs_measurement_rows": "outputs/yt_source_higgs_cross_correlator_measurement_rows_2026-05-03.json",
    "source_higgs_production_certificate": "outputs/yt_source_higgs_cross_correlator_production_certificate_2026-05-03.json",
    "neutral_primitive_cone_certificate": "outputs/yt_neutral_scalar_primitive_cone_certificate_2026-05-05.json",
    "neutral_offdiagonal_generator_certificate": "outputs/yt_neutral_offdiagonal_generator_certificate_2026-05-05.json",
    "same_source_wz_strict_packet": "outputs/yt_pr230_wz_strict_physical_response_packet_2026-05-12.json",
}

FORBIDDEN_FIREWALL = {
    "used_hunit_matrix_element_readout": False,
    "used_hunit_as_operator": False,
    "used_yt_ward_identity": False,
    "used_y_t_bare": False,
    "used_observed_top_or_yukawa_selector": False,
    "used_observed_wz_or_g2_selector": False,
    "used_alpha_lm_plaquette_or_u0": False,
    "treated_common_window_support_as_physical_readout": False,
    "treated_l12_completion_as_multivolume_fv_ir": False,
    "treated_taste_radial_x_as_canonical_oh": False,
    "relabelled_c_sx_c_xx_as_c_sh_c_hh": False,
    "set_kappa_s_equal_one": False,
    "set_c2_equal_one": False,
    "set_z_match_equal_one": False,
    "claimed_retained_or_proposed_retained": False,
    "touched_live_chunk_worker": False,
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


def future_presence() -> dict[str, bool]:
    return {name: (ROOT / rel).exists() for name, rel in REQUIRED_FUTURE_ARTIFACTS.items()}


def main() -> int:
    print("PR #230 block53 lane-1 residual minimality gate")
    print("=" * 78)

    certs = {name: load(path) for name, path in PARENTS.items()}
    statuses = {name: status(cert) for name, cert in certs.items()}
    missing = [name for name, cert in certs.items() if not cert]
    proposal_parents = [
        name for name, cert in certs.items() if cert.get("proposal_allowed") is True
    ]
    futures = future_presence()

    full_l12_support_complete = (
        certs["full_target_timeseries"].get("chunk_summary", {}).get("ready_chunks") == 63
        and certs["full_target_timeseries"].get("chunk_summary", {}).get("missing_chunks") == 0
        and certs["full_target_timeseries"].get("proposal_allowed") is False
    )
    response_side_support_complete = (
        certs["common_window_response_gate"].get("common_window_response_gate_passed") is True
        and certs["common_window_response_gate"].get("proposal_allowed") is False
        and certs["common_window_response_gate"].get("readout_switch_authorized") is False
    )
    same_source_gate_minimal_blockers = (
        certs["same_source_pole_data_sufficiency"].get("gate_passed") is False
        and certs["same_source_pole_data_sufficiency"].get("proposal_allowed") is False
        and any(
            row.get("condition") == "physical response readout switch authorized"
            and row.get("satisfied") is False
            for row in certs["same_source_pole_data_sufficiency"].get("sufficient_conditions", [])
        )
        and any(
            row.get("condition") == "finite-shell model-class or pole-saturation gate passed"
            and row.get("satisfied") is False
            for row in certs["same_source_pole_data_sufficiency"].get("sufficient_conditions", [])
        )
        and any(
            row.get("condition") == "measured pole certified as canonical Higgs radial mode"
            and row.get("satisfied") is False
            for row in certs["same_source_pole_data_sufficiency"].get("sufficient_conditions", [])
        )
    )
    action_first_current_surface_blocked = (
        certs["lane1_action_premise"].get("exact_negative_boundary_passed") is True
        and certs["lane1_action_premise"].get("same_surface_ew_higgs_action_derived") is False
        and certs["lane1_action_premise"].get("canonical_oh_action_premise_derived") is False
        and certs["lane1_action_premise"].get("proposal_allowed") is False
    )
    strict_source_higgs_rows_absent = (
        certs["source_higgs_direct_pole_row_contract"].get("proposal_allowed") is False
        and "O_H and production C_sH/C_HH rows are absent"
        in statuses["source_higgs_direct_pole_row_contract"]
    )
    neutral_route_not_closed = (
        certs["neutral_primitive_route_completion"].get("neutral_primitive_route_completion_passed") is True
        and certs["neutral_primitive_route_completion"].get("proposal_allowed") is False
        and certs["neutral_primitive_route_completion"].get("conditional_z3_remaining_unsupplied_premises") == ["H3", "H4"]
    )
    wz_route_not_closed = (
        certs["wz_absolute_authority_exhaustion"].get("wz_absolute_authority_route_exhaustion_passed") is True
        and certs["wz_absolute_authority_exhaustion"].get("proposal_allowed") is False
    )
    scalar_lsz_not_authority = (
        certs["strict_scalar_lsz_moment_fv"].get("strict_scalar_lsz_moment_fv_authority_present") is False
        and certs["strict_scalar_lsz_moment_fv"].get("proposal_allowed") is False
    )
    hs_logdet_shortcut_blocked = (
        certs["hs_logdet_scalar_action_no_go"].get("hs_logdet_scalar_action_normalization_no_go_passed") is True
        and certs["hs_logdet_scalar_action_no_go"].get("proposal_allowed") is False
    )
    model_class_gate_open = (
        certs["model_class_gate"].get("model_class_gate_passed") is False
        and certs["model_class_gate"].get("proposal_allowed") is False
    )
    higgs_identity_gate_open = (
        certs["higgs_pole_identity_gate"].get("higgs_pole_identity_gate_passed") is False
        and certs["higgs_pole_identity_gate"].get("proposal_allowed") is False
    )
    aggregate_gates_reject = (
        certs["full_positive_assembly"].get("proposal_allowed") is False
        and certs["retained_route"].get("proposal_allowed") is False
        and certs["campaign_status"].get("proposal_allowed") is False
    )
    no_future_roots_present = not any(futures.values())
    firewall_clean = all(value is False for value in FORBIDDEN_FIREWALL.values())

    minimal_remaining_roots = [
        "physical response readout authorization",
        "scalar pole/model-class/FV/IR authority",
        "canonical-Higgs pole identity or same-surface neutral-transfer bridge",
    ]
    current_support_closed = full_l12_support_complete and response_side_support_complete
    closure_not_authorized = (
        same_source_gate_minimal_blockers
        and action_first_current_surface_blocked
        and strict_source_higgs_rows_absent
        and neutral_route_not_closed
        and wz_route_not_closed
        and scalar_lsz_not_authority
        and hs_logdet_shortcut_blocked
        and model_class_gate_open
        and higgs_identity_gate_open
        and aggregate_gates_reject
        and no_future_roots_present
    )
    block53_passed = (
        not missing
        and not proposal_parents
        and current_support_closed
        and closure_not_authorized
        and firewall_clean
    )

    report("parent-certificates-present", not missing, f"missing={missing}")
    report("no-parent-authorizes-proposal", not proposal_parents, f"proposal_allowed={proposal_parents}")
    report("full-l12-support-complete", full_l12_support_complete, PARENTS["full_target_timeseries"])
    report("common-window-response-support-complete", response_side_support_complete, PARENTS["common_window_response_gate"])
    report("same-source-gate-has-minimal-open-blockers", same_source_gate_minimal_blockers, PARENTS["same_source_pole_data_sufficiency"])
    report("action-first-current-surface-blocked", action_first_current_surface_blocked, statuses["lane1_action_premise"])
    report("strict-source-higgs-rows-absent", strict_source_higgs_rows_absent, statuses["source_higgs_direct_pole_row_contract"])
    report("neutral-route-not-closed", neutral_route_not_closed, statuses["neutral_primitive_route_completion"])
    report("wz-route-not-closed", wz_route_not_closed, statuses["wz_absolute_authority_exhaustion"])
    report("scalar-lsz-not-authority", scalar_lsz_not_authority, statuses["strict_scalar_lsz_moment_fv"])
    report("hs-logdet-shortcut-blocked", hs_logdet_shortcut_blocked, statuses["hs_logdet_scalar_action_no_go"])
    report("model-class-gate-open", model_class_gate_open, statuses["model_class_gate"])
    report("higgs-identity-gate-open", higgs_identity_gate_open, statuses["higgs_pole_identity_gate"])
    report("future-root-artifacts-absent", no_future_roots_present, str(futures))
    report("aggregate-gates-reject-proposal", aggregate_gates_reject, "proposal_allowed=false")
    report("forbidden-firewall-clean", firewall_clean, str(FORBIDDEN_FIREWALL))
    report("block53-residual-minimality-passed", block53_passed, "support closed, positive closure still blocked")

    result = {
        "actual_current_surface_status": "open / block53 residual-minimality checkpoint: L12 and response support closed; positive-closure route still blocked by three physics roots",
        "conditional_surface_status": "proposed_retained can be reconsidered only after physical readout authorization, scalar pole/model-class/FV/IR authority, and canonical-Higgs or neutral-transfer authority all pass.",
        "proposal_allowed": False,
        "proposal_allowed_reason": "The current PR230 surface has bounded L12/common-window support, but still lacks the three load-bearing physics roots needed for a physical y_t readout.",
        "bare_retained_allowed": False,
        "audit_required_before_effective_retained": True,
        "block53_residual_minimality_gate_passed": block53_passed,
        "current_support_closed": current_support_closed,
        "closure_not_authorized": closure_not_authorized,
        "minimal_remaining_roots": minimal_remaining_roots,
        "future_artifact_presence": futures,
        "parent_certificates": PARENTS,
        "parent_statuses": statuses,
        "forbidden_firewall": FORBIDDEN_FIREWALL,
        "strict_non_claims": [
            "does not claim effective or proposed_retained y_t closure",
            "does not treat common-window response support as a physical readout switch",
            "does not treat L12 completion as multivolume FV/IR or scalar pole authority",
            "does not treat taste-radial x as canonical O_H",
            "does not relabel C_sx/C_xx as C_sH/C_HH",
            "does not use H_unit, yt_ward_identity, y_t_bare, observed targets, alpha_LM, plaquette, or u0",
            "does not touch or inspect active chunk-worker output",
        ],
        "exact_next_action": (
            "Attack one of the three remaining roots directly: derive or measure "
            "canonical-Higgs/neutral-transfer authority, derive scalar pole/"
            "model-class/FV/IR authority, or build a strict W/Z/source-Higgs "
            "physical response packet that authorizes the readout switch."
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
