#!/usr/bin/env python3
"""
PR #230 block36 source-Higgs / W/Z bridge dispatch checkpoint.

Block35 established that the committed PR head contains support-only row and
contract updates, but no physical bridge.  The PR head then added the lane-1
O_H root theorem attempt, a top mass-scan response harness gate, the lane-1
action-premise derivation attempt, and a higher-shell Schur/scalar-LSZ launch
preflight.  These are respectively an exact negative boundary for deriving the
canonical O_H/action root, bounded bare-mass support, an exact negative
boundary for deriving accepted EW/Higgs action from the current minimal
substrate, and future-production infrastructure support.  A later neutral
rank-one bypass audit also landed as an exact negative boundary for the
fallback neutral route, followed by a W/Z mass-response self-normalization
no-go for the active fallback and a higher-shell Schur/scalar-LSZ wave-launch
run-control checkpoint.  A later HS/logdet scalar-action normalization no-go
also blocks a source-Higgs shortcut to canonical O_H/action authority.  This
checkpoint records the next campaign move
without reopening shortcut gates: the action-first O_H/source-Higgs route stays
rank 1 but waiting on accepted action plus strict pole rows, and the active
fallback dispatch is the W/Z accepted-action response route with its exact
production packet requirements.
"""

from __future__ import annotations

import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = (
    ROOT
    / "outputs"
    / "yt_pr230_block36_source_higgs_wz_dispatch_checkpoint_2026-05-12.json"
)

PR_REF = "origin/claude/yt-direct-lattice-correlator-2026-04-30"
BLOCK35_HEAD = "d46708be7bcb0d7545392f224ab4c7ddd38b9645"
BLOCK35_SUBJECT = "Record PR230 block35 physical bridge admission checkpoint"
LANE1_OH_ROOT_HEAD = "7644411e812d046753cdf345e0ce0e446b340bbe"
LANE1_OH_ROOT_SUBJECT = "Record PR230 lane1 O_H root theorem attempt"
TOP_MASS_SCAN_HEAD = "41d0292a8736092cc7d9969af1d953f3993e8f1d"
TOP_MASS_SCAN_SUBJECT = "Refresh PR230 top mass-scan response harness"
LANE1_ACTION_PREMISE_HEAD = "63a3cce58f735050e942c154fe8853338aac112a"
LANE1_ACTION_PREMISE_SUBJECT = "Record PR230 lane1 action premise boundary"
HIGHER_SHELL_PREFLIGHT_HEAD = "ab89c6e401a922873a8e2ddf21956b617b100117"
HIGHER_SHELL_PREFLIGHT_SUBJECT = "Refresh PR230 higher-shell launch preflight"
NEUTRAL_RANK_ONE_BYPASS_HEAD = "77a10cc50c7ade6eda507190e2210a67c7fde36d"
NEUTRAL_RANK_ONE_BYPASS_SUBJECT = "Record PR230 neutral rank-one bypass boundary"
WZ_MASS_RESPONSE_NO_GO_HEAD = "557507ea8279f8e8b3f2c7c1b417235c3fced5b7"
WZ_MASS_RESPONSE_NO_GO_SUBJECT = "Record PR230 WZ mass-response normalization boundary"
SCHUR_HIGHER_SHELL_WAVE_HEAD = "5c93d0c5eee84776d50cdd45c1f117812d240af4"
SCHUR_HIGHER_SHELL_WAVE_SUBJECT = "Launch PR230 higher-shell Schur wave"
HS_LOGDET_SCALAR_NORMALIZATION_HEAD = "56a1e671063b00c1b1e6f5e2d5bd7390f92c7fbe"
HS_LOGDET_SCALAR_NORMALIZATION_SUBJECT = (
    "Record PR230 HS logdet scalar normalization boundary"
)
BLOCK36_SUBJECT = "Record PR230 block36 bridge dispatch checkpoint"

PARENTS = {
    "hs_logdet_scalar_action_normalization_no_go": "outputs/yt_pr230_hs_logdet_scalar_action_normalization_no_go_2026-05-12.json",
    "schur_higher_shell_wave_launcher": "outputs/yt_pr230_schur_higher_shell_wave_launcher_2026-05-12.json",
    "wz_mass_response_self_normalization_no_go": "outputs/yt_pr230_wz_mass_response_self_normalization_no_go_2026-05-12.json",
    "neutral_rank_one_bypass_post_block37_audit": "outputs/yt_pr230_neutral_rank_one_bypass_post_block37_audit_2026-05-12.json",
    "higher_shell_schur_production_contract": "outputs/yt_pr230_schur_higher_shell_production_contract_2026-05-07.json",
    "lane1_action_premise_derivation_attempt": "outputs/yt_pr230_lane1_action_premise_derivation_attempt_2026-05-12.json",
    "top_mass_scan_response_harness_gate": "outputs/yt_pr230_top_mass_scan_response_harness_gate_2026-05-12.json",
    "lane1_oh_root_theorem_attempt": "outputs/yt_pr230_lane1_oh_root_theorem_attempt_2026-05-12.json",
    "block35_physical_bridge_admission": "outputs/yt_pr230_block35_post_block34_physical_bridge_admission_checkpoint_2026-05-11.json",
    "block30_full_approach_review": "outputs/yt_pr230_block30_full_approach_assumptions_elon_lit_math_bridge_review_2026-05-11.json",
    "block28_degree_one_oh_support": "outputs/yt_pr230_block28_degree_one_oh_support_intake_checkpoint_2026-05-11.json",
    "fms_candidate_action_packet": "outputs/yt_pr230_fms_oh_candidate_action_packet_2026-05-07.json",
    "fms_action_adoption_minimal_cut": "outputs/yt_pr230_fms_action_adoption_minimal_cut_2026-05-07.json",
    "fms_source_overlap_readout": "outputs/yt_pr230_fms_source_overlap_readout_gate_2026-05-07.json",
    "source_higgs_pole_row_acceptance_contract": "outputs/yt_pr230_source_higgs_pole_row_acceptance_contract_2026-05-06.json",
    "taste_radial_promotion_contract": "outputs/yt_pr230_taste_radial_to_source_higgs_promotion_contract_2026-05-07.json",
    "os_transfer_kernel_artifact_gate": "outputs/yt_pr230_os_transfer_kernel_artifact_gate_2026-05-07.json",
    "wz_same_source_action_minimal_cut": "outputs/yt_pr230_wz_same_source_action_minimal_certificate_cut_2026-05-07.json",
    "wz_response_ratio_contract": "outputs/yt_pr230_wz_response_ratio_identifiability_contract_2026-05-07.json",
    "wz_physical_response_intake": "outputs/yt_pr230_wz_physical_response_packet_intake_checkpoint_2026-05-07.json",
    "additive_top_jacobian_rows": "outputs/yt_pr230_additive_top_jacobian_rows_2026-05-07.json",
    "additive_top_subtraction_contract": "outputs/yt_pr230_additive_top_subtraction_row_contract_2026-05-07.json",
    "campaign_status": "outputs/yt_pr230_campaign_status_certificate_2026-05-01.json",
}

SOURCE_HIGGS_REQUIRED_PATHS = {
    "accepted_same_surface_ew_higgs_action": "outputs/yt_pr230_same_surface_ew_higgs_action_certificate_2026-05-07.json",
    "accepted_same_source_ew_action": "outputs/yt_wz_same_source_ew_action_certificate_2026-05-04.json",
    "canonical_oh_certificate": "outputs/yt_pr230_canonical_oh_certificate_2026-05-07.json",
    "canonical_higgs_operator_certificate": "outputs/yt_canonical_higgs_operator_certificate_2026-05-03.json",
    "strict_source_higgs_pole_rows": "outputs/yt_pr230_source_higgs_pole_rows_2026-05-06.json",
    "source_higgs_cross_correlator_rows": "outputs/yt_source_higgs_cross_correlator_measurement_rows_2026-05-03.json",
    "source_higgs_production_certificate": "outputs/yt_source_higgs_cross_correlator_production_certificate_2026-05-03.json",
    "source_higgs_gram_fv_ir_authority": "outputs/yt_pr230_source_higgs_gram_fv_ir_authority_certificate_2026-05-11.json",
}

WZ_REQUIRED_PATHS = {
    "accepted_same_source_ew_action": "outputs/yt_wz_same_source_ew_action_certificate_2026-05-04.json",
    "canonical_higgs_operator_certificate": "outputs/yt_canonical_higgs_operator_certificate_2026-05-03.json",
    "wz_correlator_mass_fit_rows": "outputs/yt_wz_correlator_mass_fit_rows_2026-05-04.json",
    "same_source_top_response_certificate": "outputs/yt_same_source_top_response_certificate_2026-05-04.json",
    "strict_electroweak_g2_certificate": "outputs/yt_electroweak_g2_certificate_2026-05-04.json",
    "fh_gauge_mass_response_rows": "outputs/yt_fh_gauge_mass_response_measurement_rows_2026-05-03.json",
    "fh_gauge_mass_response_certificate": "outputs/yt_fh_gauge_mass_response_certificate_2026-05-02.json",
    "top_wz_matched_covariance_certificate": "outputs/yt_top_wz_matched_covariance_certificate_2026-05-04.json",
    "delta_perp_correction_certificate": "outputs/yt_same_source_w_response_orthogonal_correction_certificate_2026-05-04.json",
    "same_source_w_response_rows": "outputs/yt_same_source_w_response_rows_2026-05-04.json",
}

NEUTRAL_H3H4_REQUIRED_PATHS = {
    "neutral_h3_physical_transfer": "outputs/yt_pr230_neutral_h3_physical_transfer_certificate_2026-05-11.json",
    "neutral_h4_source_higgs_coupling": "outputs/yt_pr230_neutral_h4_source_higgs_coupling_certificate_2026-05-11.json",
}

FORBIDDEN_FIREWALL = {
    "used_yt_ward_identity": False,
    "used_hunit_matrix_element_or_operator": False,
    "used_y_t_bare": False,
    "used_observed_y_t_or_top_mass": False,
    "used_observed_wz_or_g2": False,
    "used_alpha_lm_plaquette_or_u0": False,
    "set_kappa_s_equal_one": False,
    "set_c2_equal_one": False,
    "set_z_match_equal_one": False,
    "set_g2_equal_one": False,
    "aliased_c_sx_to_c_sh_before_canonical_oh": False,
    "promoted_wz_scout_or_smoke_rows": False,
    "assumed_k_top_equals_k_gauge": False,
    "assumed_top_wz_covariance": False,
    "touched_live_chunk_worker": False,
    "inspected_active_chunk_output": False,
    "claimed_retained_or_proposed_retained": False,
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


def run_git(args: list[str]) -> str:
    try:
        return subprocess.check_output(
            ["git", *args],
            cwd=ROOT,
            stderr=subprocess.DEVNULL,
            text=True,
        ).strip()
    except subprocess.CalledProcessError:
        return ""


def git_ok(args: list[str]) -> bool:
    return (
        subprocess.run(
            ["git", *args],
            cwd=ROOT,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
        ).returncode
        == 0
    )


def ref_path_exists(ref: str, relpath: str) -> bool:
    return git_ok(["cat-file", "-e", f"{ref}:{relpath}"])


def present_at_ref(ref: str, paths: dict[str, str]) -> dict[str, bool]:
    return {name: ref_path_exists(ref, path) for name, path in paths.items()}


def load_json(relpath: str) -> dict[str, Any]:
    path = ROOT / relpath
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def status(cert: dict[str, Any]) -> str:
    return str(cert.get("actual_current_surface_status", ""))


def commits(base: str, head: str) -> list[str]:
    raw = run_git(["log", "--format=%H%x09%s", f"{base}..{head}"])
    return [line for line in raw.splitlines() if line]


def missing_roots(presence: dict[str, bool]) -> list[str]:
    return sorted(name for name, is_present in presence.items() if not is_present)


def source_higgs_admitted(presence: dict[str, bool]) -> bool:
    action = presence["accepted_same_surface_ew_higgs_action"] or presence[
        "accepted_same_source_ew_action"
    ]
    operator = presence["canonical_oh_certificate"] or presence[
        "canonical_higgs_operator_certificate"
    ]
    rows = presence["strict_source_higgs_pole_rows"] or (
        presence["source_higgs_cross_correlator_rows"]
        and presence["source_higgs_production_certificate"]
    )
    return action and operator and rows and presence["source_higgs_gram_fv_ir_authority"]


def all_present(presence: dict[str, bool]) -> bool:
    return bool(presence) and all(presence.values())


def main() -> int:
    print("PR #230 block36 source-Higgs / W/Z bridge dispatch checkpoint")
    print("=" * 82)

    parents = {name: load_json(path) for name, path in PARENTS.items()}
    missing_parents = [name for name, cert in parents.items() if not cert]
    failing_parents = [
        name
        for name, cert in parents.items()
        if int(cert.get("fail_count", cert.get("fails", 0)) or 0) != 0
    ]
    proposal_parents = [
        name for name, cert in parents.items() if cert.get("proposal_allowed") is True
    ]

    local_head = run_git(["rev-parse", "HEAD"])
    local_subject = run_git(["log", "-1", "--format=%s", "HEAD"])
    inspection_ref = "HEAD^" if local_subject == BLOCK36_SUBJECT else "HEAD"
    inspection_head = run_git(["rev-parse", inspection_ref])
    inspection_subject = run_git(["log", "-1", "--format=%s", inspection_ref])
    pr_head = run_git(["rev-parse", "--verify", PR_REF])
    commits_since_block35 = commits(BLOCK35_HEAD, inspection_ref)
    post_block35_subjects = {line.split("\t", 1)[1] for line in commits_since_block35}
    required_post_block35_subjects = {
        LANE1_OH_ROOT_SUBJECT,
        TOP_MASS_SCAN_SUBJECT,
        LANE1_ACTION_PREMISE_SUBJECT,
        HIGHER_SHELL_PREFLIGHT_SUBJECT,
        NEUTRAL_RANK_ONE_BYPASS_SUBJECT,
        WZ_MASS_RESPONSE_NO_GO_SUBJECT,
        SCHUR_HIGHER_SHELL_WAVE_SUBJECT,
        HS_LOGDET_SCALAR_NORMALIZATION_SUBJECT,
    }

    source_presence = present_at_ref(inspection_ref, SOURCE_HIGGS_REQUIRED_PATHS)
    wz_presence = present_at_ref(inspection_ref, WZ_REQUIRED_PATHS)
    neutral_presence = present_at_ref(inspection_ref, NEUTRAL_H3H4_REQUIRED_PATHS)

    block35_clean = (
        parents["block35_physical_bridge_admission"].get("proposal_allowed") is False
        and parents["block35_physical_bridge_admission"].get("bare_retained_allowed")
        is False
        and parents["block35_physical_bridge_admission"].get(
            "block35_post_block34_physical_bridge_admission_checkpoint_passed"
        )
        is True
        and parents["block35_physical_bridge_admission"].get("checks", {}).get(
            "source-higgs-physical-bridge-not-admitted"
        )
        is True
        and parents["block35_physical_bridge_admission"].get("checks", {}).get(
            "wz-physical-response-not-admitted"
        )
        is True
    )
    lane1_root_attempt_consumed = (
        LANE1_OH_ROOT_SUBJECT in post_block35_subjects
        and parents["lane1_oh_root_theorem_attempt"].get("exact_negative_boundary_passed")
        is True
        and parents["lane1_oh_root_theorem_attempt"].get("proposal_allowed") is False
        and parents["lane1_oh_root_theorem_attempt"].get("accepted_current_surface")
        is False
        and parents["lane1_oh_root_theorem_attempt"].get(
            "canonical_oh_identity_derived"
        )
        is False
    )
    lane1_action_premise_boundary_consumed = (
        LANE1_ACTION_PREMISE_SUBJECT in post_block35_subjects
        and parents["lane1_action_premise_derivation_attempt"].get(
            "exact_negative_boundary_passed"
        )
        is True
        and parents["lane1_action_premise_derivation_attempt"].get(
            "proposal_allowed"
        )
        is False
        and parents["lane1_action_premise_derivation_attempt"].get(
            "same_surface_ew_higgs_action_derived"
        )
        is False
        and parents["lane1_action_premise_derivation_attempt"].get(
            "canonical_oh_action_premise_derived"
        )
        is False
    )
    top_mass_scan_support_only = (
        TOP_MASS_SCAN_SUBJECT in post_block35_subjects
        and parents["top_mass_scan_response_harness_gate"].get(
            "top_mass_scan_response_harness_gate_passed"
        )
        is True
        and parents["top_mass_scan_response_harness_gate"].get("proposal_allowed")
        is False
        and parents["top_mass_scan_response_harness_gate"]
        .get("metadata_top_mass_scan_response", {})
        .get("used_as_physical_yukawa_readout")
        is False
        and parents["top_mass_scan_response_harness_gate"]
        .get("metadata_top_mass_scan_response", {})
        .get("physical_higgs_normalization")
        == "not_derived"
    )
    higher_shell_preflight_support_only = (
        HIGHER_SHELL_PREFLIGHT_SUBJECT in post_block35_subjects
        and parents["higher_shell_schur_production_contract"].get(
            "higher_shell_schur_production_contract_passed"
        )
        is True
        and parents["higher_shell_schur_production_contract"].get("proposal_allowed")
        is False
        and parents["higher_shell_schur_production_contract"].get(
            "jobs_launched_by_contract"
        )
        is False
        and parents["higher_shell_schur_production_contract"].get(
            "rows_written_by_contract"
        )
        is False
    )
    neutral_rank_one_bypass_boundary_consumed = (
        NEUTRAL_RANK_ONE_BYPASS_SUBJECT in post_block35_subjects
        and parents["neutral_rank_one_bypass_post_block37_audit"].get(
            "exact_negative_boundary_passed"
        )
        is True
        and parents["neutral_rank_one_bypass_post_block37_audit"].get(
            "rank_one_bypass_closed"
        )
        is False
        and parents["neutral_rank_one_bypass_post_block37_audit"].get(
            "proposal_allowed"
        )
        is False
    )
    wz_mass_response_self_normalization_no_go_consumed = (
        WZ_MASS_RESPONSE_NO_GO_SUBJECT in post_block35_subjects
        and parents["wz_mass_response_self_normalization_no_go"].get(
            "wz_mass_response_self_normalization_no_go_passed"
        )
        is True
        and parents["wz_mass_response_self_normalization_no_go"].get(
            "proposal_allowed"
        )
        is False
        and parents["wz_mass_response_self_normalization_no_go"].get(
            "strict_g2_certificate_present"
        )
        is False
    )
    higher_shell_wave_run_control_only = (
        SCHUR_HIGHER_SHELL_WAVE_SUBJECT in post_block35_subjects
        and parents["schur_higher_shell_wave_launcher"].get("wave_launcher_passed")
        is True
        and parents["schur_higher_shell_wave_launcher"].get("proposal_allowed")
        is False
        and parents["schur_higher_shell_wave_launcher"].get("launch_mode") is False
        and parents["schur_higher_shell_wave_launcher"].get("active_chunk_indices")
        == [1, 2]
        and parents["schur_higher_shell_wave_launcher"].get("max_concurrent") == 2
    )
    hs_logdet_scalar_normalization_no_go_consumed = (
        HS_LOGDET_SCALAR_NORMALIZATION_SUBJECT in post_block35_subjects
        and parents["hs_logdet_scalar_action_normalization_no_go"].get(
            "hs_logdet_scalar_action_normalization_no_go_passed"
        )
        is True
        and parents["hs_logdet_scalar_action_normalization_no_go"].get(
            "proposal_allowed"
        )
        is False
        and parents["hs_logdet_scalar_action_normalization_no_go"].get(
            "canonical_oh_identity_derived"
        )
        is False
    )
    source_admitted = source_higgs_admitted(source_presence)
    wz_admitted = all_present(wz_presence)
    neutral_admitted = all_present(neutral_presence)

    fms_cut_support_only = (
        parents["fms_action_adoption_minimal_cut"].get(
            "fms_action_adoption_minimal_cut_passed"
        )
        is True
        and parents["fms_action_adoption_minimal_cut"].get("adoption_allowed_now")
        is False
        and parents["fms_action_adoption_minimal_cut"].get(
            "current_surface_action_adopted"
        )
        is False
    )
    pole_contract_waiting = (
        parents["source_higgs_pole_row_acceptance_contract"].get(
            "source_higgs_pole_row_acceptance_contract_passed"
        )
        is True
        and parents["source_higgs_pole_row_acceptance_contract"].get(
            "closure_contract_satisfied"
        )
        is False
        and parents["source_higgs_pole_row_acceptance_contract"].get("rows_present")
        is False
    )
    source_route_checkpointed = (
        block35_clean
        and lane1_root_attempt_consumed
        and lane1_action_premise_boundary_consumed
        and fms_cut_support_only
        and pole_contract_waiting
        and not source_admitted
    )
    wz_action_cut_waiting = (
        parents["wz_same_source_action_minimal_cut"].get(
            "wz_same_source_action_minimal_certificate_cut_passed"
        )
        is True
        and parents["wz_same_source_action_minimal_cut"].get(
            "current_surface_action_certificate_satisfied"
        )
        is False
    )
    wz_packet_waiting = (
        parents["wz_physical_response_intake"].get(
            "wz_physical_response_packet_intake_checkpoint_passed"
        )
        is True
        and parents["wz_physical_response_intake"].get("production_packet_present")
        is False
        and bool(
            parents["wz_physical_response_intake"].get("missing_production_roots")
        )
    )
    wz_pivot_selected = source_route_checkpointed and wz_action_cut_waiting
    wz_pivot_not_admitted = wz_pivot_selected and wz_packet_waiting and not wz_admitted
    neutral_remains_fallback = not neutral_admitted
    firewall_clean = all(value is False for value in FORBIDDEN_FIREWALL.values())
    no_route_admitted = not (source_admitted or wz_admitted or neutral_admitted)

    report("parent-certificates-present", not missing_parents, f"missing={missing_parents}")
    report("parent-certificates-have-no-fails", not failing_parents, f"failing={failing_parents}")
    report("no-parent-authorizes-proposal", not proposal_parents, f"proposal_allowed={proposal_parents}")
    report("block35-clean-open-checkpoint", block35_clean, status(parents["block35_physical_bridge_admission"]))
    report(
        "post-block35-commits-consumed",
        required_post_block35_subjects.issubset(post_block35_subjects),
        str(commits_since_block35),
    )
    report("lane1-oh-root-attempt-consumed", lane1_root_attempt_consumed, str(commits_since_block35))
    report(
        "lane1-action-premise-boundary-consumed",
        lane1_action_premise_boundary_consumed,
        status(parents["lane1_action_premise_derivation_attempt"]),
    )
    report(
        "top-mass-scan-response-support-only",
        top_mass_scan_support_only,
        status(parents["top_mass_scan_response_harness_gate"]),
    )
    report(
        "higher-shell-preflight-support-only",
        higher_shell_preflight_support_only,
        status(parents["higher_shell_schur_production_contract"]),
    )
    report(
        "neutral-rank-one-bypass-boundary-consumed",
        neutral_rank_one_bypass_boundary_consumed,
        status(parents["neutral_rank_one_bypass_post_block37_audit"]),
    )
    report(
        "wz-mass-response-self-normalization-no-go-consumed",
        wz_mass_response_self_normalization_no_go_consumed,
        status(parents["wz_mass_response_self_normalization_no_go"]),
    )
    report(
        "higher-shell-wave-launch-run-control-only",
        higher_shell_wave_run_control_only,
        status(parents["schur_higher_shell_wave_launcher"]),
    )
    report(
        "hs-logdet-scalar-normalization-no-go-consumed",
        hs_logdet_scalar_normalization_no_go_consumed,
        status(parents["hs_logdet_scalar_action_normalization_no_go"]),
    )
    report("source-higgs-route-checkpointed", source_route_checkpointed, str(source_presence))
    report("fms-action-cut-support-only", fms_cut_support_only, status(parents["fms_action_adoption_minimal_cut"]))
    report("source-higgs-pole-contract-waiting", pole_contract_waiting, status(parents["source_higgs_pole_row_acceptance_contract"]))
    report("wz-pivot-selected-after-source-higgs-block", wz_pivot_selected, "rank2 W/Z accepted-action response selected as active fallback")
    report("wz-action-cut-waiting", wz_action_cut_waiting, status(parents["wz_same_source_action_minimal_cut"]))
    report("wz-physical-response-packet-waiting", wz_packet_waiting, status(parents["wz_physical_response_intake"]))
    report("wz-pivot-not-admitted", wz_pivot_not_admitted, str(wz_presence))
    report("neutral-h3h4-remains-fallback-only", neutral_remains_fallback, str(neutral_presence))
    report("forbidden-firewall-clean", firewall_clean, str(FORBIDDEN_FIREWALL))
    report("no-route-admitted-without-explicit-input", no_route_admitted, "dispatch only; no closure")

    result = {
        "actual_current_surface_status": (
            "open / block36 source-Higgs route checkpointed and W/Z accepted-action "
            "response pivot selected; no physical bridge packet is admitted"
        ),
        "conditional_surface_status": (
            "source-Higgs support if a future accepted same-surface EW/Higgs action "
            "certifies canonical O_H and supplies strict C_ss/C_sH/C_HH pole rows "
            "with Gram/FV/IR authority; W/Z support if a future strict packet "
            "supplies accepted action, production W/Z rows, same-source top rows, "
            "matched covariance, strict non-observed g2, delta_perp authority, and "
            "final W-response rows"
        ),
        "hypothetical_axiom_status": None,
        "admitted_observation_status": None,
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "Block36 is a dispatch checkpoint.  It checkpoints the blocked "
            "canonical O_H/source-Higgs route after consuming the lane-1 O_H "
            "root theorem attempt and lane-1 action-premise boundary, treats "
            "top mass-scan response rows, higher-shell preflight, and the "
            "higher-shell wave launch as support/run-control only, consumes "
            "the HS/logdet scalar-normalization no-go as a source-Higgs "
            "shortcut boundary, selects strict W/Z accepted-action response as the active "
            "fallback, and confirms that neither route has the required "
            "accepted action, production rows, matched covariance, strict g2, "
            "or source-Higgs pole authority."
        ),
        "audit_required_before_effective_retained": True,
        "bare_retained_allowed": False,
        "block36_source_higgs_wz_dispatch_checkpoint_passed": FAIL_COUNT == 0,
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "local_head": local_head,
        "local_subject": local_subject,
        "inspection_ref": inspection_ref,
        "inspection_head": inspection_head,
        "inspection_subject": inspection_subject,
        "pr_ref": PR_REF,
        "pr_head": pr_head,
        "block35_head": BLOCK35_HEAD,
        "lane1_oh_root_head": LANE1_OH_ROOT_HEAD,
        "top_mass_scan_head": TOP_MASS_SCAN_HEAD,
        "lane1_action_premise_head": LANE1_ACTION_PREMISE_HEAD,
        "higher_shell_preflight_head": HIGHER_SHELL_PREFLIGHT_HEAD,
        "neutral_rank_one_bypass_head": NEUTRAL_RANK_ONE_BYPASS_HEAD,
        "wz_mass_response_no_go_head": WZ_MASS_RESPONSE_NO_GO_HEAD,
        "schur_higher_shell_wave_head": SCHUR_HIGHER_SHELL_WAVE_HEAD,
        "hs_logdet_scalar_normalization_head": HS_LOGDET_SCALAR_NORMALIZATION_HEAD,
        "commits_since_block35_head": commits_since_block35,
        "parent_statuses": {name: status(cert) for name, cert in parents.items()},
        "source_higgs_route": {
            "rank": 1,
            "checkpointed": source_route_checkpointed,
            "admitted": source_admitted,
            "required_paths": SOURCE_HIGGS_REQUIRED_PATHS,
            "committed_path_presence": source_presence,
            "missing_roots": missing_roots(source_presence),
            "support_loaded": [
                "lane-1 O_H root theorem attempt exact negative boundary",
                "lane-1 action-premise derivation exact negative boundary",
                "degree-one O_H radial tangent support",
                "FMS O_H candidate/action packet",
                "FMS action-adoption minimal cut",
                "source-Higgs pole-row acceptance contract",
                "higher-shell Schur/scalar-LSZ preflight as support only",
                "higher-shell Schur/scalar-LSZ wave launch as run-control only",
                "HS/logdet scalar-action normalization no-go",
                "taste-radial promotion and OS alias firewalls",
            ],
            "decision": (
                "checkpointed as blocked on accepted same-surface action/operator "
                "authority, canonical O_H, strict C_ss/C_sH/C_HH pole rows, and "
                "Gram/FV/IR authority after the lane-1 O_H root attempt failed "
                "and the lane-1 action-premise attempt failed on the current "
                "surface"
            ),
        },
        "wz_accepted_action_response_route": {
            "rank": 2,
            "selected_active_fallback": wz_pivot_selected,
            "admitted": wz_admitted,
            "required_paths": WZ_REQUIRED_PATHS,
            "committed_path_presence": wz_presence,
            "missing_roots": missing_roots(wz_presence),
            "missing_production_roots_from_intake": parents[
                "wz_physical_response_intake"
            ].get("missing_production_roots", []),
            "support_loaded": [
                "W/Z response-ratio identifiability contract",
                "W/Z same-source action minimal certificate cut",
                "additive-top subtraction contract",
                "coarse additive-top Jacobian support",
                "top mass-scan response harness gate as bare-mass support only",
                "W/Z physical-response packet intake firewall",
                "W/Z mass-response self-normalization no-go",
            ],
            "decision": (
                "selected as active fallback but not admitted; build accepted "
                "same-source action first, then production W/Z rows, same-source "
                "top rows, matched covariance, strict non-observed g2, delta_perp, "
                "and final W-response rows; mass-plus-response self-normalization "
                "still does not remove the strict g2/absolute-normalization need"
            ),
        },
        "neutral_h3h4_route": {
            "rank": 3,
            "fallback_only": neutral_remains_fallback,
            "admitted": neutral_admitted,
            "neutral_rank_one_bypass_boundary_consumed": neutral_rank_one_bypass_boundary_consumed,
            "required_paths": NEUTRAL_H3H4_REQUIRED_PATHS,
            "committed_path_presence": neutral_presence,
            "missing_roots": missing_roots(neutral_presence),
            "decision": (
                "do not reopen without same-surface physical neutral transfer "
                "and source/canonical-Higgs coupling authority; the post-block37 "
                "neutral rank-one bypass audit is an exact negative boundary "
                "on the current surface"
            ),
        },
        "campaign_decision": {
            "current_route_checkpointed": "canonical O_H / source-Higgs bridge",
            "active_pivot": "strict W/Z accepted-action physical response",
            "yield_for_supervisor": True,
            "next_exact_action": (
                "For W/Z, supply accepted same-source EW/Higgs action plus "
                "production W/Z mass-response rows, same-source top rows, matched "
                "covariance, strict non-observed g2, delta_perp authority, and "
                "final W-response rows.  Reopen source-Higgs only with accepted "
                "same-surface O_H/action plus strict C_ss/C_sH/C_HH pole rows."
            ),
        },
        "live_chunk_worker": {
            "touched": False,
            "inspected_active_output": False,
        },
        "forbidden_firewall": FORBIDDEN_FIREWALL,
        "checks": {
            "parent-certificates-present": not missing_parents,
            "parent-certificates-have-no-fails": not failing_parents,
            "no-parent-authorizes-proposal": not proposal_parents,
            "block35-clean-open-checkpoint": block35_clean,
            "post-block35-commits-consumed": required_post_block35_subjects.issubset(
                post_block35_subjects
            ),
            "lane1-oh-root-attempt-consumed": lane1_root_attempt_consumed,
            "lane1-action-premise-boundary-consumed": lane1_action_premise_boundary_consumed,
            "top-mass-scan-response-support-only": top_mass_scan_support_only,
            "higher-shell-preflight-support-only": higher_shell_preflight_support_only,
            "neutral-rank-one-bypass-boundary-consumed": neutral_rank_one_bypass_boundary_consumed,
            "wz-mass-response-self-normalization-no-go-consumed": wz_mass_response_self_normalization_no_go_consumed,
            "higher-shell-wave-launch-run-control-only": higher_shell_wave_run_control_only,
            "hs-logdet-scalar-normalization-no-go-consumed": hs_logdet_scalar_normalization_no_go_consumed,
            "source-higgs-route-checkpointed": source_route_checkpointed,
            "fms-action-cut-support-only": fms_cut_support_only,
            "source-higgs-pole-contract-waiting": pole_contract_waiting,
            "wz-pivot-selected-after-source-higgs-block": wz_pivot_selected,
            "wz-action-cut-waiting": wz_action_cut_waiting,
            "wz-physical-response-packet-waiting": wz_packet_waiting,
            "wz-pivot-not-admitted": wz_pivot_not_admitted,
            "neutral-h3h4-remains-fallback-only": neutral_remains_fallback,
            "forbidden-firewall-clean": firewall_clean,
            "no-route-admitted-without-explicit-input": no_route_admitted,
        },
        "strict_non_claims": [
            "does not claim retained or proposed_retained top-Yukawa closure",
            "does not treat the FMS candidate/action packet as adopted PR230 action",
            "does not treat degree-one O_H support as canonical O_H without same-surface action authority",
            "does not relabel C_sx/C_xx as C_sH/C_HH before x=O_H is certified",
            "does not promote W/Z scout, smoke, or schema rows to production evidence",
            "does not treat higher-shell Schur/scalar-LSZ launch preflight as measured rows or pole authority",
            "does not treat higher-shell Schur/scalar-LSZ wave-launch status or active workers as row evidence",
            "does not treat HS/logdet auxiliary scalar normalization as canonical O_H/action authority",
            "does not assume top/W covariance or k_top = k_gauge",
            "does not set kappa_s, c2, Z_match, g2, or delta_perp by convention",
            "does not use Ward, H_unit, y_t_bare, observed targets, observed g2, alpha_LM, plaquette, or u0",
            "does not inspect live or untracked chunk-worker output",
        ],
        "passes": PASS_COUNT,
        "fails": FAIL_COUNT,
        "pass_count": PASS_COUNT,
        "fail_count": FAIL_COUNT,
    }

    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"\nWrote certificate: {OUTPUT.relative_to(ROOT)}")
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
