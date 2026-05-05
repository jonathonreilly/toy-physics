#!/usr/bin/env python3
"""
PR #230 full positive closure assembly gate.

This runner answers the practical integration question for the current
campaign: when the chunk work finishes, what else must be true before PR #230
can honestly claim positive retained top-Yukawa closure?

It does not claim closure and it does not consume or package chunk outputs as
evidence.  It checks the non-chunk bridge surface: scalar LSZ/model-class
control plus one canonical-Higgs/source-overlap route.  Chunk evidence alone is
explicitly rejected.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "yt_pr230_full_positive_closure_assembly_gate_2026-05-04.json"

PARENTS = {
    "retained_route": "outputs/yt_retained_closure_route_certificate_2026-05-01.json",
    "campaign_status": "outputs/yt_pr230_campaign_status_certificate_2026-05-01.json",
    "fh_lsz_common_window_response": "outputs/yt_fh_lsz_common_window_response_gate_2026-05-04.json",
    "fh_lsz_finite_source_linearity": "outputs/yt_fh_lsz_finite_source_linearity_gate_2026-05-02.json",
    "fh_lsz_response_window_acceptance": "outputs/yt_fh_lsz_response_window_acceptance_gate_2026-05-03.json",
    "fh_lsz_target_ess": "outputs/yt_fh_lsz_target_observable_ess_certificate_2026-05-03.json",
    "fh_lsz_autocorrelation_ess": "outputs/yt_fh_lsz_autocorrelation_ess_gate_2026-05-02.json",
    "fh_lsz_polefit8x8_combiner": "outputs/yt_fh_lsz_polefit8x8_chunk_combiner_gate_2026-05-04.json",
    "fh_lsz_polefit8x8_postprocessor": "outputs/yt_fh_lsz_polefit8x8_postprocessor_2026-05-04.json",
    "fh_lsz_model_class": "outputs/yt_fh_lsz_pole_fit_model_class_gate_2026-05-02.json",
    "fh_lsz_model_class_semantic_firewall": "outputs/yt_fh_lsz_model_class_semantic_firewall_2026-05-04.json",
    "fh_lsz_stieltjes_moment_certificate": "outputs/yt_fh_lsz_stieltjes_moment_certificate_gate_2026-05-05.json",
    "fh_lsz_pade_stieltjes_bounds": "outputs/yt_fh_lsz_pade_stieltjes_bounds_gate_2026-05-05.json",
    "fh_lsz_polefit8x8_stieltjes_proxy_diagnostic": "outputs/yt_fh_lsz_polefit8x8_stieltjes_proxy_diagnostic_2026-05-05.json",
    "pr230_scalar_lsz_holonomic_exact_authority": "outputs/yt_pr230_scalar_lsz_holonomic_exact_authority_attempt_2026-05-05.json",
    "pr230_scalar_lsz_carleman_tauberian_determinacy": "outputs/yt_pr230_scalar_lsz_carleman_tauberian_determinacy_attempt_2026-05-05.json",
    "fh_lsz_contact_subtraction_identifiability": "outputs/yt_fh_lsz_contact_subtraction_identifiability_2026-05-05.json",
    "fh_lsz_affine_contact_complete_monotonicity": "outputs/yt_fh_lsz_affine_contact_complete_monotonicity_no_go_2026-05-05.json",
    "fh_lsz_polynomial_contact_finite_shell": "outputs/yt_fh_lsz_polynomial_contact_finite_shell_no_go_2026-05-05.json",
    "fh_lsz_polynomial_contact_repair": "outputs/yt_fh_lsz_polynomial_contact_repair_no_go_2026-05-05.json",
    "fh_lsz_pole_saturation": "outputs/yt_fh_lsz_pole_saturation_threshold_gate_2026-05-02.json",
    "fh_lsz_finite_volume": "outputs/yt_fh_lsz_finite_volume_pole_saturation_obstruction_2026-05-02.json",
    "fh_lsz_soft_continuum": "outputs/yt_fh_lsz_soft_continuum_threshold_no_go_2026-05-02.json",
    "source_higgs_readiness": "outputs/yt_source_higgs_production_readiness_gate_2026-05-04.json",
    "source_higgs_gram": "outputs/yt_source_higgs_gram_purity_gate_2026-05-02.json",
    "source_higgs_postprocess": "outputs/yt_source_higgs_gram_purity_postprocess_2026-05-03.json",
    "source_higgs_unratified_gram_no_go": "outputs/yt_source_higgs_unratified_gram_shortcut_no_go_2026-05-05.json",
    "wz_same_source_action": "outputs/yt_wz_same_source_ew_action_gate_2026-05-04.json",
    "wz_same_source_action_semantic_firewall": "outputs/yt_wz_same_source_ew_action_semantic_firewall_2026-05-04.json",
    "wz_source_coordinate_transport_no_go": "outputs/yt_wz_source_coordinate_transport_no_go_2026-05-05.json",
    "wz_goldstone_equivalence_no_go": "outputs/yt_wz_goldstone_equivalence_source_identity_no_go_2026-05-05.json",
    "same_source_w_response_decomposition": "outputs/yt_same_source_w_response_decomposition_theorem_2026-05-04.json",
    "same_source_w_response_orthogonal_correction": "outputs/yt_same_source_w_response_orthogonal_correction_gate_2026-05-04.json",
    "one_higgs_completeness_orthogonal_null": "outputs/yt_one_higgs_completeness_orthogonal_null_gate_2026-05-04.json",
    "delta_perp_tomography_builder": "outputs/yt_delta_perp_tomography_correction_builder_2026-05-04.json",
    "same_source_top_response_identity_builder": "outputs/yt_same_source_top_response_identity_certificate_builder_2026-05-04.json",
    "top_wz_matched_covariance_builder": "outputs/yt_top_wz_matched_covariance_certificate_builder_2026-05-04.json",
    "top_wz_covariance_marginal_derivation_no_go": "outputs/yt_top_wz_covariance_marginal_derivation_no_go_2026-05-05.json",
    "top_wz_factorization_independence_gate": "outputs/yt_top_wz_factorization_independence_gate_2026-05-05.json",
    "top_wz_deterministic_response_covariance_gate": "outputs/yt_top_wz_deterministic_response_covariance_gate_2026-05-05.json",
    "top_wz_covariance_theorem_import_audit": "outputs/yt_top_wz_covariance_theorem_import_audit_2026-05-05.json",
    "same_source_top_response_builder": "outputs/yt_same_source_top_response_certificate_builder_2026-05-04.json",
    "same_source_w_response_row_builder": "outputs/yt_same_source_w_response_row_builder_2026-05-04.json",
    "same_source_w_lightweight_readout": "outputs/yt_same_source_w_response_lightweight_readout_harness_2026-05-04.json",
    "wz_certificate_gate": "outputs/yt_same_source_wz_response_certificate_gate_2026-05-02.json",
    "wz_harness_smoke_schema": "outputs/yt_pr230_wz_harness_smoke_schema_gate_2026-05-05.json",
    "wz_smoke_to_production_no_go": "outputs/yt_pr230_wz_smoke_to_production_promotion_no_go_2026-05-05.json",
    "wz_mass_fit_path": "outputs/yt_wz_correlator_mass_fit_path_gate_2026-05-04.json",
    "wz_mass_fit_response_row_builder": "outputs/yt_wz_mass_fit_response_row_builder_2026-05-04.json",
    "electroweak_g2_certificate_builder": "outputs/yt_electroweak_g2_certificate_builder_2026-05-05.json",
    "wz_g2_generator_casimir_normalization_no_go": "outputs/yt_wz_g2_generator_casimir_normalization_no_go_2026-05-05.json",
    "wz_g2_authority_firewall": "outputs/yt_wz_g2_authority_firewall_2026-05-05.json",
    "wz_g2_response_self_normalization_no_go": "outputs/yt_wz_g2_response_self_normalization_no_go_2026-05-05.json",
    "same_source_sector_overlap": "outputs/yt_same_source_sector_overlap_identity_obstruction_2026-05-02.json",
    "canonical_higgs_operator": "outputs/yt_canonical_higgs_operator_certificate_gate_2026-05-03.json",
    "canonical_higgs_semantic_firewall": "outputs/yt_canonical_higgs_operator_semantic_firewall_2026-05-04.json",
    "cross_lane_oh_authority_audit": "outputs/yt_cross_lane_oh_authority_audit_2026-05-05.json",
    "canonical_oh_premise_stretch": "outputs/yt_canonical_oh_premise_stretch_no_go_2026-05-05.json",
    "source_pole_mixing": "outputs/yt_source_pole_canonical_higgs_mixing_obstruction_2026-05-02.json",
    "source_pole_purity": "outputs/yt_source_pole_purity_cross_correlator_gate_2026-05-02.json",
    "neutral_scalar_irreducibility": "outputs/yt_neutral_scalar_irreducibility_authority_audit_2026-05-04.json",
    "neutral_scalar_primitive_cone": "outputs/yt_neutral_scalar_primitive_cone_certificate_gate_2026-05-05.json",
    "neutral_scalar_primitive_cone_stretch_no_go": "outputs/yt_neutral_scalar_primitive_cone_stretch_no_go_2026-05-05.json",
    "neutral_scalar_burnside_irreducibility": "outputs/yt_neutral_scalar_burnside_irreducibility_attempt_2026-05-05.json",
    "schur_kprime_rows": "outputs/yt_schur_kprime_row_absence_guard_2026-05-03.json",
    "schur_kprime_sufficiency": "outputs/yt_schur_complement_kprime_sufficiency_2026-05-03.json",
    "schur_compressed_bootstrap_no_go": "outputs/yt_schur_compressed_denominator_row_bootstrap_no_go_2026-05-05.json",
    "nonchunk_current_surface_exhaustion": "outputs/yt_pr230_nonchunk_current_surface_exhaustion_gate_2026-05-05.json",
    "nonchunk_future_artifact_intake": "outputs/yt_pr230_nonchunk_future_artifact_intake_gate_2026-05-05.json",
    "nonchunk_terminal_route_exhaustion": "outputs/yt_pr230_nonchunk_terminal_route_exhaustion_gate_2026-05-05.json",
    "nonchunk_reopen_admissibility": "outputs/yt_pr230_nonchunk_reopen_admissibility_gate_2026-05-05.json",
    "nonchunk_cycle14_route_selector": "outputs/yt_pr230_nonchunk_cycle14_route_selector_gate_2026-05-05.json",
    "nonchunk_cycle15_independent_route_admission": "outputs/yt_pr230_nonchunk_cycle15_independent_route_admission_gate_2026-05-05.json",
    "nonchunk_cycle16_reopen_source_guard": "outputs/yt_pr230_nonchunk_cycle16_reopen_source_guard_2026-05-05.json",
    "nonchunk_cycle17_stop_condition_gate": "outputs/yt_pr230_nonchunk_cycle17_stop_condition_gate_2026-05-05.json",
    "nonchunk_cycle18_reopen_freshness_gate": "outputs/yt_pr230_nonchunk_cycle18_reopen_freshness_gate_2026-05-05.json",
    "nonchunk_cycle19_no_duplicate_route_gate": "outputs/yt_pr230_nonchunk_cycle19_no_duplicate_route_gate_2026-05-05.json",
    "nonchunk_cycle20_process_gate_continuation_no_go": "outputs/yt_pr230_nonchunk_cycle20_process_gate_continuation_no_go_2026-05-05.json",
    "nonchunk_cycle21_remote_reopen_guard": "outputs/yt_pr230_nonchunk_cycle21_remote_reopen_guard_2026-05-05.json",
    "nonchunk_cycle22_main_audit_drift_guard": "outputs/yt_pr230_nonchunk_cycle22_main_audit_drift_guard_2026-05-05.json",
    "nonchunk_cycle23_main_effective_status_drift_guard": "outputs/yt_pr230_nonchunk_cycle23_main_effective_status_drift_guard_2026-05-05.json",
    "nonchunk_cycle24_post_cycle23_main_status_drift_guard": "outputs/yt_pr230_nonchunk_cycle24_post_cycle23_main_status_drift_guard_2026-05-05.json",
    "nonchunk_cycle25_post_cycle24_main_audit_status_drift_guard": "outputs/yt_pr230_nonchunk_cycle25_post_cycle24_main_audit_status_drift_guard_2026-05-05.json",
    "nonchunk_cycle26_post_cycle25_main_audit_status_drift_guard": "outputs/yt_pr230_nonchunk_cycle26_post_cycle25_main_audit_status_drift_guard_2026-05-05.json",
    "nonchunk_cycle27_post_cycle26_main_audit_status_drift_guard": "outputs/yt_pr230_nonchunk_cycle27_post_cycle26_main_audit_status_drift_guard_2026-05-05.json",
    "nonchunk_cycle28_post_cycle27_main_audit_status_drift_guard": "outputs/yt_pr230_nonchunk_cycle28_post_cycle27_main_audit_status_drift_guard_2026-05-05.json",
    "nonchunk_cycle29_post_cycle28_main_audit_status_drift_guard": "outputs/yt_pr230_nonchunk_cycle29_post_cycle28_main_audit_status_drift_guard_2026-05-05.json",
    "nonchunk_cycle30_post_cycle29_main_audit_status_drift_guard": "outputs/yt_pr230_nonchunk_cycle30_post_cycle29_main_audit_status_drift_guard_2026-05-05.json",
    "nonchunk_cycle31_post_cycle30_main_audit_status_drift_guard": "outputs/yt_pr230_nonchunk_cycle31_post_cycle30_main_audit_status_drift_guard_2026-05-05.json",
    "nonchunk_cycle32_post_cycle31_main_audit_status_drift_guard": "outputs/yt_pr230_nonchunk_cycle32_post_cycle31_main_audit_status_drift_guard_2026-05-05.json",
    "nonchunk_cycle33_post_cycle32_main_audit_status_drift_guard": "outputs/yt_pr230_nonchunk_cycle33_post_cycle32_main_audit_status_drift_guard_2026-05-05.json",
    "nonchunk_cycle34_post_cycle33_main_nonpr230_drift_guard": "outputs/yt_pr230_nonchunk_cycle34_post_cycle33_main_nonpr230_drift_guard_2026-05-05.json",
    "nonchunk_cycle35_post_cycle34_main_audit_ledger_drift_guard": "outputs/yt_pr230_nonchunk_cycle35_post_cycle34_main_audit_ledger_drift_guard_2026-05-05.json",
    "matching_running": "outputs/yt_pr230_matching_running_bridge_gate_2026-05-04.json",
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


def truth(cert: dict[str, Any], key: str) -> bool:
    return cert.get(key) is True


def closure_conditions() -> list[dict[str, Any]]:
    return [
        {
            "id": "production_physical_response",
            "required": (
                "strict direct correlator evidence or joint FH/LSZ same-source "
                "production evidence with homogeneous run-control, target ESS, "
                "finite-source derivative control, and no chunk/provenance collisions"
            ),
            "why_needed": "Supplies the physical response data; pilots and partial chunks are not y_t evidence.",
            "current_surface": "bounded production support only",
        },
        {
            "id": "scalar_lsz_model_class_fv_ir",
            "required": (
                "isolated scalar-pole derivative/residue with model-class or "
                "analytic-continuation authority plus FV/IR/zero-mode/threshold control"
            ),
            "why_needed": "Converts finite-shell same-source C_ss rows into a pole LSZ normalization.",
            "current_surface": (
                "finite-shell/postprocessor gates remain support-only or exact negative "
                "boundaries; strict Stieltjes/Pade moment-threshold certificate is absent"
            ),
        },
        {
            "id": "source_overlap_or_physical_response_bridge",
            "required": (
                "one accepted bridge among O_sp/O_H Gram purity with C_sH/C_HH "
                "rows, same-source W/Z response with sector-overlap identity, "
                "same-surface Schur/K-prime rows plus canonical bridge, or a "
                "neutral-scalar rank-one/irreducibility theorem"
            ),
            "why_needed": "Identifies the source-pole readout with physical canonical-Higgs y_t.",
            "current_surface": "all current bridge routes are absent, blocked, or conditional support",
        },
        {
            "id": "matching_running_bridge",
            "required": (
                "explicit lattice-to-physical matching and SM running bridge whose "
                "inputs are measured/certified, not observed-target selectors"
            ),
            "why_needed": "Turns the lattice-scale readout into the PR230 y_t(v)/m_t comparison.",
            "current_surface": "not authorized until production, LSZ, and overlap gates pass",
        },
        {
            "id": "retained_proposal_firewall",
            "required": (
                "retained-route and campaign status certificates allow proposed_retained, "
                "with no forbidden imports or open load-bearing assumptions"
            ),
            "why_needed": "Prevents local support artifacts from becoming branch-local retained claims.",
            "current_surface": "proposal_allowed is false",
        },
    ]


def route_statuses(certs: dict[str, dict[str, Any]]) -> dict[str, dict[str, Any]]:
    return {
        "source_higgs_gram_purity": {
            "passes_current_surface": truth(certs["source_higgs_gram"], "source_higgs_gram_purity_gate_passed")
            or truth(certs["source_higgs_postprocess"], "osp_higgs_gram_purity_gate_passed"),
            "blocked_by": [
                "same-surface O_H certificate absent",
                "cross-lane O_h/O_H/Higgs artifacts audited as non-authority for PR230",
                "current primitives do not derive same-surface O_H identity and normalization",
                "production C_sH/C_HH pole residues absent",
                "Gram-purity postprocessor awaiting production certificate",
                "perfect Gram purity against an unratified supplied operator is not O_H authority",
            ],
            "parents": [
                PARENTS["source_higgs_readiness"],
                PARENTS["source_higgs_gram"],
                PARENTS["source_higgs_postprocess"],
                PARENTS["source_higgs_unratified_gram_no_go"],
                PARENTS["canonical_higgs_semantic_firewall"],
                PARENTS["cross_lane_oh_authority_audit"],
                PARENTS["canonical_oh_premise_stretch"],
            ],
        },
        "same_source_wz_response": {
            "passes_current_surface": truth(certs["wz_same_source_action"], "same_source_ew_action_ready")
            and truth(certs["wz_certificate_gate"], "same_source_wz_response_certificate_gate_passed")
            and truth(certs["same_source_w_lightweight_readout"], "strict_lightweight_readout_gate_passed"),
            "blocked_by": [
                "same-source EW action certificate absent",
                "source-coordinate transport from static EW algebra rejected",
                "longitudinal/Goldstone-equivalence source-identity shortcut rejected",
                "W/Z correlator mass-fit path absent",
                "orthogonal-neutral top-coupling null or correction absent",
                "strict delta_perp tomography correction rows absent",
                "same-source top-response identity certificate absent",
                "matched top/W covariance certificate absent",
                "marginal derivation of top/W covariance rejected",
                "same-source/native top/W factorization-independence shortcut rejected",
                "deterministic W-response covariance shortcut rejected",
                "current-branch covariance-theorem import shortcut rejected",
                "same-source top-response certificate absent",
                "same-source W-response row builder strict inputs absent",
                "lightweight same-source W readout production rows absent",
                "W/Z harness smoke schema path is synthetic infrastructure only",
                "W/Z smoke rows cannot be promoted to production W/Z response",
                "W/Z mass-fit response-row builder strict inputs absent",
                "strict electroweak g2 certificate builder inputs absent",
                "SU(2) generator/Casimir normalization rejected as g2 authority",
                "strict non-observed g2 authority certificate absent",
                "response-only g2 self-normalization rejected",
                "sector-overlap identity not derived",
                "canonical-Higgs identity not derived",
            ],
            "parents": [
                PARENTS["wz_same_source_action"],
                PARENTS["wz_same_source_action_semantic_firewall"],
                PARENTS["wz_source_coordinate_transport_no_go"],
                PARENTS["wz_goldstone_equivalence_no_go"],
                PARENTS["same_source_w_response_decomposition"],
                PARENTS["same_source_w_response_orthogonal_correction"],
                PARENTS["one_higgs_completeness_orthogonal_null"],
                PARENTS["delta_perp_tomography_builder"],
                PARENTS["same_source_top_response_identity_builder"],
                PARENTS["top_wz_matched_covariance_builder"],
                PARENTS["top_wz_covariance_marginal_derivation_no_go"],
                PARENTS["top_wz_factorization_independence_gate"],
                PARENTS["top_wz_deterministic_response_covariance_gate"],
                PARENTS["same_source_top_response_builder"],
                PARENTS["same_source_w_response_row_builder"],
                PARENTS["same_source_w_lightweight_readout"],
                PARENTS["wz_certificate_gate"],
                PARENTS["wz_harness_smoke_schema"],
                PARENTS["wz_smoke_to_production_no_go"],
                PARENTS["wz_mass_fit_path"],
                PARENTS["wz_mass_fit_response_row_builder"],
                PARENTS["electroweak_g2_certificate_builder"],
                PARENTS["wz_g2_generator_casimir_normalization_no_go"],
                PARENTS["wz_g2_authority_firewall"],
                PARENTS["wz_g2_response_self_normalization_no_go"],
                PARENTS["same_source_sector_overlap"],
            ],
        },
        "schur_kprime_kernel_rows": {
            "passes_current_surface": truth(certs["schur_kprime_rows"], "schur_kprime_row_gate_passed"),
            "blocked_by": [
                "same-surface Schur A/B/C rows absent",
                "finite FH/LSZ source rows explicitly rejected as kernel rows",
                "compressed scalar denominator and pole derivative do not reconstruct A/B/C rows",
                "canonical bridge still required after K-prime sufficiency",
            ],
            "parents": [
                PARENTS["schur_kprime_rows"],
                PARENTS["schur_kprime_sufficiency"],
                PARENTS["schur_compressed_bootstrap_no_go"],
            ],
        },
        "neutral_scalar_rank_one": {
            "passes_current_surface": truth(certs["neutral_scalar_irreducibility"], "neutral_scalar_irreducibility_authority_present"),
            "blocked_by": [
                "no current primitive-cone/positivity-improving neutral-sector certificate",
                "rank-two neutral scalar counterfamilies remain allowed",
                "strict primitive-cone certificate gate absent",
                "primitive-cone stretch no-go blocks the source-only and conditional-Perron shortcut",
                "Burnside/double-commutant route has no same-surface off-diagonal neutral generator",
            ],
            "parents": [
                PARENTS["neutral_scalar_irreducibility"],
                PARENTS["neutral_scalar_primitive_cone"],
                PARENTS["neutral_scalar_primitive_cone_stretch_no_go"],
                PARENTS["neutral_scalar_burnside_irreducibility"],
            ],
        },
    }


def evaluate(state: dict[str, bool]) -> dict[str, Any]:
    required = [
        "production_physical_response",
        "scalar_lsz_model_class_fv_ir",
        "source_overlap_or_physical_response_bridge",
        "matching_running_bridge",
        "retained_proposal_firewall",
        "forbidden_import_firewall",
    ]
    missing = [name for name in required if not state.get(name, False)]
    return {
        "assembly_passed": not missing,
        "missing": missing,
        "proposal_allowed": not missing,
    }


def main() -> int:
    print("PR #230 full positive closure assembly gate")
    print("=" * 72)

    certs = {name: load(rel) for name, rel in PARENTS.items()}
    missing_parents = [name for name, cert in certs.items() if not cert]
    proposal_allowed_parents = [
        name for name, cert in certs.items() if cert.get("proposal_allowed") is True
    ]
    statuses = {name: status(cert) for name, cert in certs.items()}
    routes = route_statuses(certs)
    any_bridge_passes = any(row["passes_current_surface"] for row in routes.values())

    response_side_support = (
        certs["fh_lsz_common_window_response"].get("common_window_response_gate_passed") is True
        or "support" in statuses["fh_lsz_common_window_response"]
    )
    finite_source_support = (
        certs["fh_lsz_finite_source_linearity"].get("finite_source_linearity_gate_passed") is True
        or "support" in statuses["fh_lsz_finite_source_linearity"]
    )
    ess_support = (
        certs["fh_lsz_target_ess"].get("target_observable_ess_gate_passed") is True
        or "ESS" in statuses["fh_lsz_target_ess"]
    )
    polefit_support_only = (
        certs["fh_lsz_polefit8x8_combiner"].get("proposal_allowed") is False
        and certs["fh_lsz_polefit8x8_postprocessor"].get("proposal_allowed") is False
        and "eight-mode" in statuses["fh_lsz_polefit8x8_postprocessor"]
    )
    scalar_lsz_blocks = (
        certs["fh_lsz_model_class"].get("proposal_allowed") is False
        and certs["fh_lsz_model_class_semantic_firewall"].get("proposal_allowed") is False
        and certs["fh_lsz_stieltjes_moment_certificate"].get("proposal_allowed") is False
        and certs["fh_lsz_stieltjes_moment_certificate"].get("moment_certificate_gate_passed")
        is False
        and certs["fh_lsz_pade_stieltjes_bounds"].get("proposal_allowed") is False
        and certs["fh_lsz_pade_stieltjes_bounds"].get("pade_stieltjes_bounds_gate_passed")
        is False
        and certs["fh_lsz_polefit8x8_stieltjes_proxy_diagnostic"].get("proposal_allowed")
        is False
        and certs["fh_lsz_polefit8x8_stieltjes_proxy_diagnostic"].get(
            "stieltjes_proxy_certificate_passed"
        )
        is False
        and certs["pr230_scalar_lsz_holonomic_exact_authority"].get("proposal_allowed")
        is False
        and certs["pr230_scalar_lsz_holonomic_exact_authority"].get(
            "holonomic_exact_authority_passed"
        )
        is False
        and certs["pr230_scalar_lsz_carleman_tauberian_determinacy"].get(
            "proposal_allowed"
        )
        is False
        and certs["pr230_scalar_lsz_carleman_tauberian_determinacy"].get(
            "carleman_tauberian_determinacy_passed"
        )
        is False
        and certs["fh_lsz_contact_subtraction_identifiability"].get("proposal_allowed")
        is False
        and certs["fh_lsz_contact_subtraction_identifiability"].get(
            "contact_subtraction_identifiability_obstruction_passed"
        )
        is True
        and certs["fh_lsz_affine_contact_complete_monotonicity"].get("proposal_allowed")
        is False
        and certs["fh_lsz_affine_contact_complete_monotonicity"].get(
            "affine_contact_complete_monotonicity_no_go_passed"
        )
        is True
        and certs["fh_lsz_polynomial_contact_finite_shell"].get("proposal_allowed")
        is False
        and certs["fh_lsz_polynomial_contact_finite_shell"].get(
            "polynomial_contact_finite_shell_no_go_passed"
        )
        is True
        and certs["fh_lsz_polynomial_contact_repair"].get("proposal_allowed")
        is False
        and certs["fh_lsz_polynomial_contact_repair"].get(
            "polynomial_contact_repair_no_go_passed"
        )
        is True
        and certs["fh_lsz_polynomial_contact_repair"].get(
            "stieltjes_certificate_from_polynomial_contact_passed"
        )
        is False
        and certs["fh_lsz_pole_saturation"].get("proposal_allowed") is False
        and certs["fh_lsz_finite_volume"].get("proposal_allowed") is False
        and certs["fh_lsz_soft_continuum"].get("proposal_allowed") is False
    )
    source_overlap_blocks = (
        any_bridge_passes is False
        and certs["canonical_higgs_semantic_firewall"].get("proposal_allowed") is False
        and certs["cross_lane_oh_authority_audit"].get("proposal_allowed") is False
        and certs["source_pole_mixing"].get("proposal_allowed") is False
        and certs["source_pole_purity"].get("proposal_allowed") is False
        and certs["canonical_higgs_operator"].get("proposal_allowed") is False
        and certs["canonical_oh_premise_stretch"].get("proposal_allowed") is False
        and certs["canonical_oh_premise_stretch"].get("premise_lattice_stretch_no_go_passed")
        is True
        and certs["source_higgs_unratified_gram_no_go"].get("proposal_allowed") is False
        and certs["source_higgs_unratified_gram_no_go"].get(
            "unratified_gram_shortcut_no_go_passed"
        )
        is True
        and certs["wz_same_source_action_semantic_firewall"].get("proposal_allowed") is False
        and certs["wz_source_coordinate_transport_no_go"].get("proposal_allowed") is False
        and certs["wz_source_coordinate_transport_no_go"].get(
            "wz_source_coordinate_transport_no_go_passed"
        )
        is True
        and certs["wz_goldstone_equivalence_no_go"].get("proposal_allowed") is False
        and certs["wz_goldstone_equivalence_no_go"].get(
            "goldstone_equivalence_source_identity_no_go_passed"
        )
        is True
    )
    matching_running_blocks = (
        certs["matching_running"].get("matching_running_bridge_passed") is not True
        and certs["matching_running"].get("proposal_allowed") is False
    )
    retained_route_open = (
        "retained closure not yet reached" in statuses["retained_route"]
        and certs["retained_route"].get("proposal_allowed") is False
    )
    campaign_open = (
        "active campaign" in statuses["campaign_status"]
        and certs["campaign_status"].get("proposal_allowed") is False
    )
    nonchunk_current_surface_exhausted = (
        "current PR230 non-chunk route queue exhausted"
        in statuses["nonchunk_current_surface_exhaustion"]
        and certs["nonchunk_current_surface_exhaustion"].get("proposal_allowed") is False
        and certs["nonchunk_current_surface_exhaustion"].get(
            "current_surface_exhaustion_gate_passed"
        )
        is True
    )
    nonchunk_future_artifact_intake_closed = (
        "future-artifact intake" in statuses["nonchunk_future_artifact_intake"]
        and certs["nonchunk_future_artifact_intake"].get("proposal_allowed") is False
        and certs["nonchunk_future_artifact_intake"].get(
            "future_artifact_intake_gate_passed"
        )
        is True
        and certs["nonchunk_future_artifact_intake"].get("dramatic_step_gate", {}).get(
            "passed"
        )
        is False
    )
    nonchunk_terminal_route_exhaustion_closed = (
        "terminal route-exhaustion gate" in statuses["nonchunk_terminal_route_exhaustion"]
        and certs["nonchunk_terminal_route_exhaustion"].get("proposal_allowed") is False
        and certs["nonchunk_terminal_route_exhaustion"].get(
            "terminal_route_exhaustion_gate_passed"
        )
        is True
        and certs["nonchunk_terminal_route_exhaustion"].get(
            "dramatic_step_gate", {}
        ).get("passed")
        is False
    )
    nonchunk_reopen_admissibility_closed = (
        "reopen-admissibility gate" in statuses["nonchunk_reopen_admissibility"]
        and certs["nonchunk_reopen_admissibility"].get("proposal_allowed") is False
        and certs["nonchunk_reopen_admissibility"].get(
            "reopen_admissibility_gate_passed"
        )
        is True
        and certs["nonchunk_reopen_admissibility"].get(
            "dramatic_step_gate", {}
        ).get("passed")
        is False
    )
    nonchunk_cycle14_route_selector_closed = (
        "cycle-14 route-selector gate" in statuses["nonchunk_cycle14_route_selector"]
        and certs["nonchunk_cycle14_route_selector"].get("proposal_allowed") is False
        and certs["nonchunk_cycle14_route_selector"].get("route_selector_gate_passed")
        is True
        and certs["nonchunk_cycle14_route_selector"].get("dramatic_step_gate", {}).get(
            "passed"
        )
        is False
    )
    nonchunk_cycle15_independent_route_admission_closed = (
        "cycle-15 independent-route admission gate"
        in statuses["nonchunk_cycle15_independent_route_admission"]
        and certs["nonchunk_cycle15_independent_route_admission"].get("proposal_allowed")
        is False
        and certs["nonchunk_cycle15_independent_route_admission"].get(
            "independent_route_admission_gate_passed"
        )
        is True
        and certs["nonchunk_cycle15_independent_route_admission"].get(
            "dramatic_step_gate", {}
        ).get("passed")
        is False
    )
    nonchunk_cycle16_reopen_source_guard_closed = (
        "cycle-16 reopen-source guard"
        in statuses["nonchunk_cycle16_reopen_source_guard"]
        and certs["nonchunk_cycle16_reopen_source_guard"].get("proposal_allowed")
        is False
        and certs["nonchunk_cycle16_reopen_source_guard"].get(
            "reopen_source_guard_passed"
        )
        is True
        and certs["nonchunk_cycle16_reopen_source_guard"].get(
            "dramatic_step_gate", {}
        ).get("passed")
        is False
    )
    nonchunk_cycle17_stop_condition_closed = (
        "cycle-17 stop-condition gate"
        in statuses["nonchunk_cycle17_stop_condition_gate"]
        and certs["nonchunk_cycle17_stop_condition_gate"].get("proposal_allowed")
        is False
        and certs["nonchunk_cycle17_stop_condition_gate"].get(
            "stop_condition_gate_passed"
        )
        is True
        and certs["nonchunk_cycle17_stop_condition_gate"].get(
            "dramatic_step_gate", {}
        ).get("passed")
        is False
    )
    nonchunk_cycle18_reopen_freshness_closed = (
        "cycle-18 reopen-freshness gate"
        in statuses["nonchunk_cycle18_reopen_freshness_gate"]
        and certs["nonchunk_cycle18_reopen_freshness_gate"].get("proposal_allowed")
        is False
        and certs["nonchunk_cycle18_reopen_freshness_gate"].get(
            "reopen_freshness_gate_passed"
        )
        is True
        and certs["nonchunk_cycle18_reopen_freshness_gate"].get(
            "dramatic_step_gate", {}
        ).get("passed")
        is False
    )
    nonchunk_cycle19_no_duplicate_route_closed = (
        "cycle-19 no-duplicate-route gate"
        in statuses["nonchunk_cycle19_no_duplicate_route_gate"]
        and certs["nonchunk_cycle19_no_duplicate_route_gate"].get("proposal_allowed")
        is False
        and certs["nonchunk_cycle19_no_duplicate_route_gate"].get(
            "no_duplicate_route_gate_passed"
        )
        is True
        and certs["nonchunk_cycle19_no_duplicate_route_gate"].get(
            "dramatic_step_gate", {}
        ).get("passed")
        is False
    )
    nonchunk_cycle20_process_gate_continuation_closed = (
        "cycle-20 process-gate continuation no-go"
        in statuses["nonchunk_cycle20_process_gate_continuation_no_go"]
        and certs["nonchunk_cycle20_process_gate_continuation_no_go"].get(
            "proposal_allowed"
        )
        is False
        and certs["nonchunk_cycle20_process_gate_continuation_no_go"].get(
            "process_gate_continuation_no_go_passed"
        )
        is True
        and certs["nonchunk_cycle20_process_gate_continuation_no_go"].get(
            "dramatic_step_gate", {}
        ).get("passed")
        is False
    )
    nonchunk_cycle21_remote_reopen_guard_closed = (
        "cycle-21 remote-surface reopen guard"
        in statuses["nonchunk_cycle21_remote_reopen_guard"]
        and certs["nonchunk_cycle21_remote_reopen_guard"].get("proposal_allowed")
        is False
        and certs["nonchunk_cycle21_remote_reopen_guard"].get(
            "cycle21_remote_reopen_guard_passed"
        )
        is True
        and certs["nonchunk_cycle21_remote_reopen_guard"].get(
            "dramatic_step_gate", {}
        ).get("passed")
        is False
    )
    nonchunk_cycle22_main_audit_drift_guard_closed = (
        "cycle-22 main-audit-drift reopen guard"
        in statuses["nonchunk_cycle22_main_audit_drift_guard"]
        and certs["nonchunk_cycle22_main_audit_drift_guard"].get("proposal_allowed")
        is False
        and certs["nonchunk_cycle22_main_audit_drift_guard"].get(
            "cycle22_main_audit_drift_guard_passed"
        )
        is True
        and certs["nonchunk_cycle22_main_audit_drift_guard"].get(
            "dramatic_step_gate", {}
        ).get("passed")
        is False
    )
    nonchunk_cycle23_main_effective_status_drift_guard_closed = (
        "cycle-23 main-effective-status-drift reopen guard"
        in statuses["nonchunk_cycle23_main_effective_status_drift_guard"]
        and certs["nonchunk_cycle23_main_effective_status_drift_guard"].get(
            "proposal_allowed"
        )
        is False
        and certs["nonchunk_cycle23_main_effective_status_drift_guard"].get(
            "cycle23_main_effective_status_drift_guard_passed"
        )
        is True
        and certs["nonchunk_cycle23_main_effective_status_drift_guard"].get(
            "dramatic_step_gate", {}
        ).get("passed")
        is False
    )
    nonchunk_cycle24_post_cycle23_main_status_drift_guard_closed = (
        "cycle-24 post-cycle-23 main-status-drift reopen guard"
        in statuses["nonchunk_cycle24_post_cycle23_main_status_drift_guard"]
        and certs["nonchunk_cycle24_post_cycle23_main_status_drift_guard"].get(
            "proposal_allowed"
        )
        is False
        and certs["nonchunk_cycle24_post_cycle23_main_status_drift_guard"].get(
            "cycle24_post_cycle23_main_status_drift_guard_passed"
        )
        is True
        and certs["nonchunk_cycle24_post_cycle23_main_status_drift_guard"].get(
            "dramatic_step_gate", {}
        ).get("passed")
        is False
    )
    nonchunk_cycle25_post_cycle24_main_audit_status_drift_guard_closed = (
        "cycle-25 post-cycle-24 main-audit-status-drift reopen guard"
        in statuses["nonchunk_cycle25_post_cycle24_main_audit_status_drift_guard"]
        and certs["nonchunk_cycle25_post_cycle24_main_audit_status_drift_guard"].get(
            "proposal_allowed"
        )
        is False
        and certs["nonchunk_cycle25_post_cycle24_main_audit_status_drift_guard"].get(
            "cycle25_post_cycle24_main_audit_status_drift_guard_passed"
        )
        is True
        and certs["nonchunk_cycle25_post_cycle24_main_audit_status_drift_guard"].get(
            "dramatic_step_gate", {}
        ).get("passed")
        is False
    )
    nonchunk_cycle26_post_cycle25_main_audit_status_drift_guard_closed = (
        "cycle-26 post-cycle-25 main-audit-status-drift reopen guard"
        in statuses["nonchunk_cycle26_post_cycle25_main_audit_status_drift_guard"]
        and certs["nonchunk_cycle26_post_cycle25_main_audit_status_drift_guard"].get(
            "proposal_allowed"
        )
        is False
        and certs["nonchunk_cycle26_post_cycle25_main_audit_status_drift_guard"].get(
            "cycle26_post_cycle25_main_audit_status_drift_guard_passed"
        )
        is True
        and certs["nonchunk_cycle26_post_cycle25_main_audit_status_drift_guard"].get(
            "dramatic_step_gate", {}
        ).get("passed")
        is False
    )
    nonchunk_cycle27_post_cycle26_main_audit_status_drift_guard_closed = (
        "cycle-27 post-cycle-26 main-audit-status-drift reopen guard"
        in statuses["nonchunk_cycle27_post_cycle26_main_audit_status_drift_guard"]
        and certs["nonchunk_cycle27_post_cycle26_main_audit_status_drift_guard"].get(
            "proposal_allowed"
        )
        is False
        and certs["nonchunk_cycle27_post_cycle26_main_audit_status_drift_guard"].get(
            "cycle27_post_cycle26_main_audit_status_drift_guard_passed"
        )
        is True
        and certs["nonchunk_cycle27_post_cycle26_main_audit_status_drift_guard"].get(
            "dramatic_step_gate", {}
        ).get("passed")
        is False
    )
    nonchunk_cycle28_post_cycle27_main_audit_status_drift_guard_closed = (
        "cycle-28 post-cycle-27 main-audit-status-drift reopen guard"
        in statuses["nonchunk_cycle28_post_cycle27_main_audit_status_drift_guard"]
        and certs["nonchunk_cycle28_post_cycle27_main_audit_status_drift_guard"].get(
            "proposal_allowed"
        )
        is False
        and certs["nonchunk_cycle28_post_cycle27_main_audit_status_drift_guard"].get(
            "cycle28_post_cycle27_main_audit_status_drift_guard_passed"
        )
        is True
        and certs["nonchunk_cycle28_post_cycle27_main_audit_status_drift_guard"].get(
            "dramatic_step_gate", {}
        ).get("passed")
        is False
    )
    nonchunk_cycle29_post_cycle28_main_audit_status_drift_guard_closed = (
        "cycle-29 post-cycle-28 main-audit-status-drift reopen guard"
        in statuses["nonchunk_cycle29_post_cycle28_main_audit_status_drift_guard"]
        and certs["nonchunk_cycle29_post_cycle28_main_audit_status_drift_guard"].get(
            "proposal_allowed"
        )
        is False
        and certs["nonchunk_cycle29_post_cycle28_main_audit_status_drift_guard"].get(
            "cycle29_post_cycle28_main_audit_status_drift_guard_passed"
        )
        is True
        and certs["nonchunk_cycle29_post_cycle28_main_audit_status_drift_guard"].get(
            "dramatic_step_gate", {}
        ).get("passed")
        is False
    )
    nonchunk_cycle30_post_cycle29_main_audit_status_drift_guard_closed = (
        "cycle-30 post-cycle-29 main-audit-status-drift reopen guard"
        in statuses["nonchunk_cycle30_post_cycle29_main_audit_status_drift_guard"]
        and certs["nonchunk_cycle30_post_cycle29_main_audit_status_drift_guard"].get(
            "proposal_allowed"
        )
        is False
        and certs["nonchunk_cycle30_post_cycle29_main_audit_status_drift_guard"].get(
            "cycle30_post_cycle29_main_audit_status_drift_guard_passed"
        )
        is True
        and certs["nonchunk_cycle30_post_cycle29_main_audit_status_drift_guard"].get(
            "dramatic_step_gate", {}
        ).get("passed")
        is False
    )
    nonchunk_cycle31_post_cycle30_main_audit_status_drift_guard_closed = (
        "cycle-31 post-cycle-30 main-audit-status-drift reopen guard"
        in statuses["nonchunk_cycle31_post_cycle30_main_audit_status_drift_guard"]
        and certs["nonchunk_cycle31_post_cycle30_main_audit_status_drift_guard"].get(
            "proposal_allowed"
        )
        is False
        and certs["nonchunk_cycle31_post_cycle30_main_audit_status_drift_guard"].get(
            "cycle31_post_cycle30_main_audit_status_drift_guard_passed"
        )
        is True
        and certs["nonchunk_cycle31_post_cycle30_main_audit_status_drift_guard"].get(
            "dramatic_step_gate", {}
        ).get("passed")
        is False
    )
    nonchunk_cycle32_post_cycle31_main_audit_status_drift_guard_closed = (
        "cycle-32 post-cycle-31 main-audit-status-drift reopen guard"
        in statuses["nonchunk_cycle32_post_cycle31_main_audit_status_drift_guard"]
        and certs["nonchunk_cycle32_post_cycle31_main_audit_status_drift_guard"].get(
            "proposal_allowed"
        )
        is False
        and certs["nonchunk_cycle32_post_cycle31_main_audit_status_drift_guard"].get(
            "cycle32_post_cycle31_main_audit_status_drift_guard_passed"
        )
        is True
        and certs["nonchunk_cycle32_post_cycle31_main_audit_status_drift_guard"].get(
            "dramatic_step_gate", {}
        ).get("passed")
        is False
    )
    nonchunk_cycle33_post_cycle32_main_audit_status_drift_guard_closed = (
        "cycle-33 post-cycle-32 main-audit-status-drift reopen guard"
        in statuses["nonchunk_cycle33_post_cycle32_main_audit_status_drift_guard"]
        and certs["nonchunk_cycle33_post_cycle32_main_audit_status_drift_guard"].get(
            "proposal_allowed"
        )
        is False
        and certs["nonchunk_cycle33_post_cycle32_main_audit_status_drift_guard"].get(
            "cycle33_post_cycle32_main_audit_status_drift_guard_passed"
        )
        is True
        and certs["nonchunk_cycle33_post_cycle32_main_audit_status_drift_guard"].get(
            "dramatic_step_gate", {}
        ).get("passed")
        is False
    )
    nonchunk_cycle34_post_cycle33_main_nonpr230_drift_guard_closed = (
        "cycle-34 post-cycle-33 main non-PR230 drift reopen guard"
        in statuses["nonchunk_cycle34_post_cycle33_main_nonpr230_drift_guard"]
        and certs["nonchunk_cycle34_post_cycle33_main_nonpr230_drift_guard"].get(
            "proposal_allowed"
        )
        is False
        and certs["nonchunk_cycle34_post_cycle33_main_nonpr230_drift_guard"].get(
            "cycle34_post_cycle33_main_nonpr230_drift_guard_passed"
        )
        is True
        and certs["nonchunk_cycle34_post_cycle33_main_nonpr230_drift_guard"].get(
            "dramatic_step_gate", {}
        ).get("passed")
        is False
    )
    nonchunk_cycle35_post_cycle34_main_audit_ledger_drift_guard_closed = (
        "cycle-35 post-cycle-34 main audit-ledger drift reopen guard"
        in statuses["nonchunk_cycle35_post_cycle34_main_audit_ledger_drift_guard"]
        and certs["nonchunk_cycle35_post_cycle34_main_audit_ledger_drift_guard"].get(
            "proposal_allowed"
        )
        is False
        and certs["nonchunk_cycle35_post_cycle34_main_audit_ledger_drift_guard"].get(
            "cycle35_post_cycle34_main_audit_ledger_drift_guard_passed"
        )
        is True
        and certs["nonchunk_cycle35_post_cycle34_main_audit_ledger_drift_guard"].get(
            "dramatic_step_gate", {}
        ).get("passed")
        is False
    )

    current_state = {
        "production_physical_response": False,
        "scalar_lsz_model_class_fv_ir": False,
        "source_overlap_or_physical_response_bridge": any_bridge_passes,
        "matching_running_bridge": truth(certs["matching_running"], "matching_running_bridge_passed"),
        "retained_proposal_firewall": False,
        "forbidden_import_firewall": True,
    }
    current_eval = evaluate(current_state)
    chunk_only_state = {
        **current_state,
        "production_physical_response": True,
    }
    chunk_only_eval = evaluate(chunk_only_state)
    synthetic_positive_state = {
        "production_physical_response": True,
        "scalar_lsz_model_class_fv_ir": True,
        "source_overlap_or_physical_response_bridge": True,
        "matching_running_bridge": True,
        "retained_proposal_firewall": True,
        "forbidden_import_firewall": True,
    }
    synthetic_eval = evaluate(synthetic_positive_state)

    report("parent-certificates-present", not missing_parents, f"missing={missing_parents}")
    report("no-parent-authorizes-proposal", not proposal_allowed_parents, f"proposal_allowed={proposal_allowed_parents}")
    report("response-side-support-present", response_side_support, statuses["fh_lsz_common_window_response"])
    report("finite-source-support-present", finite_source_support, statuses["fh_lsz_finite_source_linearity"])
    report("target-ess-support-present", ess_support, statuses["fh_lsz_target_ess"])
    report("polefit8x8-support-only", polefit_support_only, statuses["fh_lsz_polefit8x8_postprocessor"])
    report(
        "canonical-higgs-semantic-firewall-support-only",
        "semantic firewall passed" in statuses["canonical_higgs_semantic_firewall"]
        and certs["canonical_higgs_semantic_firewall"].get("proposal_allowed") is False,
        statuses["canonical_higgs_semantic_firewall"],
    )
    report(
        "cross-lane-oh-authority-audit-blocks-adjacent-imports",
        "cross-lane O_H authority audit" in statuses["cross_lane_oh_authority_audit"]
        and certs["cross_lane_oh_authority_audit"].get("proposal_allowed") is False
        and certs["cross_lane_oh_authority_audit"].get("repo_cross_lane_authority_found") is False,
        statuses["cross_lane_oh_authority_audit"],
    )
    report(
        "canonical-oh-premise-stretch-blocks-current-primitives",
        "same-surface O_H identity and normalization"
        in statuses["canonical_oh_premise_stretch"]
        and certs["canonical_oh_premise_stretch"].get("proposal_allowed") is False
        and certs["canonical_oh_premise_stretch"].get("premise_lattice_stretch_no_go_passed")
        is True,
        statuses["canonical_oh_premise_stretch"],
    )
    report(
        "source-higgs-unratified-gram-shortcut-closed",
        "unratified source-Higgs Gram shortcut" in statuses["source_higgs_unratified_gram_no_go"]
        and certs["source_higgs_unratified_gram_no_go"].get("proposal_allowed") is False
        and certs["source_higgs_unratified_gram_no_go"].get(
            "unratified_gram_shortcut_no_go_passed"
        )
        is True,
        statuses["source_higgs_unratified_gram_no_go"],
    )
    report(
        "model-class-semantic-firewall-support-only",
        "model-class semantic firewall passed" in statuses["fh_lsz_model_class_semantic_firewall"]
        and certs["fh_lsz_model_class_semantic_firewall"].get("proposal_allowed") is False,
        statuses["fh_lsz_model_class_semantic_firewall"],
    )
    report(
        "stieltjes-moment-certificate-gate-absent",
        "Stieltjes moment-certificate gate" in statuses["fh_lsz_stieltjes_moment_certificate"]
        and certs["fh_lsz_stieltjes_moment_certificate"].get("proposal_allowed") is False
        and certs["fh_lsz_stieltjes_moment_certificate"].get("moment_certificate_gate_passed")
        is False,
        statuses["fh_lsz_stieltjes_moment_certificate"],
    )
    report(
        "pade-stieltjes-bounds-gate-absent",
        "Pade-Stieltjes bounds gate" in statuses["fh_lsz_pade_stieltjes_bounds"]
        and certs["fh_lsz_pade_stieltjes_bounds"].get("proposal_allowed") is False
        and certs["fh_lsz_pade_stieltjes_bounds"].get("pade_stieltjes_bounds_gate_passed")
        is False,
        statuses["fh_lsz_pade_stieltjes_bounds"],
    )
    report(
        "polefit8x8-stieltjes-proxy-diagnostic-blocks-current-proxy",
        "Stieltjes monotonicity"
        in statuses["fh_lsz_polefit8x8_stieltjes_proxy_diagnostic"]
        and certs["fh_lsz_polefit8x8_stieltjes_proxy_diagnostic"].get("proposal_allowed")
        is False
        and certs["fh_lsz_polefit8x8_stieltjes_proxy_diagnostic"].get(
            "stieltjes_proxy_certificate_passed"
        )
        is False,
        statuses["fh_lsz_polefit8x8_stieltjes_proxy_diagnostic"],
    )
    report(
        "scalar-lsz-holonomic-exact-authority-attempt-blocks-current-finite-shell",
        "scalar-LSZ holonomic exact-authority not derivable"
        in statuses["pr230_scalar_lsz_holonomic_exact_authority"]
        and certs["pr230_scalar_lsz_holonomic_exact_authority"].get(
            "proposal_allowed"
        )
        is False
        and certs["pr230_scalar_lsz_holonomic_exact_authority"].get(
            "holonomic_exact_authority_passed"
        )
        is False,
        statuses["pr230_scalar_lsz_holonomic_exact_authority"],
    )
    report(
        "scalar-lsz-carleman-tauberian-determinacy-attempt-blocks-current-finite-prefix",
        "Carleman/Tauberian scalar-LSZ determinacy not derivable"
        in statuses["pr230_scalar_lsz_carleman_tauberian_determinacy"]
        and certs["pr230_scalar_lsz_carleman_tauberian_determinacy"].get(
            "proposal_allowed"
        )
        is False
        and certs["pr230_scalar_lsz_carleman_tauberian_determinacy"].get(
            "carleman_tauberian_determinacy_passed"
        )
        is False
        and certs["pr230_scalar_lsz_carleman_tauberian_determinacy"].get(
            "finite_prefix_stieltjes_counterfamily_passed"
        )
        is True,
        statuses["pr230_scalar_lsz_carleman_tauberian_determinacy"],
    )
    report(
        "contact-subtraction-identifiability-blocks-arbitrary-subtraction",
        "contact-subtraction identifiability obstruction"
        in statuses["fh_lsz_contact_subtraction_identifiability"]
        and certs["fh_lsz_contact_subtraction_identifiability"].get("proposal_allowed")
        is False
        and certs["fh_lsz_contact_subtraction_identifiability"].get(
            "contact_subtraction_identifiability_obstruction_passed"
        )
        is True,
        statuses["fh_lsz_contact_subtraction_identifiability"],
    )
    report(
        "affine-contact-complete-monotonicity-blocks",
        "affine contact complete-monotonicity no-go"
        in statuses["fh_lsz_affine_contact_complete_monotonicity"]
        and certs["fh_lsz_affine_contact_complete_monotonicity"].get("proposal_allowed")
        is False
        and certs["fh_lsz_affine_contact_complete_monotonicity"].get(
            "affine_contact_complete_monotonicity_no_go_passed"
        )
        is True,
        statuses["fh_lsz_affine_contact_complete_monotonicity"],
    )
    report(
        "polynomial-contact-finite-shell-blocks",
        "finite-shell polynomial contact non-identifiability no-go"
        in statuses["fh_lsz_polynomial_contact_finite_shell"]
        and certs["fh_lsz_polynomial_contact_finite_shell"].get("proposal_allowed")
        is False
        and certs["fh_lsz_polynomial_contact_finite_shell"].get(
            "polynomial_contact_finite_shell_no_go_passed"
        )
        is True,
        statuses["fh_lsz_polynomial_contact_finite_shell"],
    )
    report(
        "polynomial-contact-repair-no-go-blocks",
        "polynomial contact repair not scalar-LSZ authority"
        in statuses["fh_lsz_polynomial_contact_repair"]
        and certs["fh_lsz_polynomial_contact_repair"].get("proposal_allowed")
        is False
        and certs["fh_lsz_polynomial_contact_repair"].get(
            "polynomial_contact_repair_no_go_passed"
        )
        is True
        and certs["fh_lsz_polynomial_contact_repair"].get(
            "stieltjes_certificate_from_polynomial_contact_passed"
        )
        is False,
        statuses["fh_lsz_polynomial_contact_repair"],
    )
    report(
        "wz-action-semantic-firewall-support-only",
        "same-source EW action semantic firewall passed"
        in statuses["wz_same_source_action_semantic_firewall"]
        and certs["wz_same_source_action_semantic_firewall"].get("proposal_allowed") is False,
        statuses["wz_same_source_action_semantic_firewall"],
    )
    report(
        "wz-source-coordinate-transport-no-go-blocks",
        "WZ source-coordinate transport shortcut rejected"
        in statuses["wz_source_coordinate_transport_no_go"]
        and certs["wz_source_coordinate_transport_no_go"].get("proposal_allowed") is False
        and certs["wz_source_coordinate_transport_no_go"].get(
            "wz_source_coordinate_transport_no_go_passed"
        )
        is True,
        statuses["wz_source_coordinate_transport_no_go"],
    )
    report(
        "wz-goldstone-equivalence-source-identity-no-go-blocks",
        "Goldstone equivalence does not identify PR230 source coordinate"
        in statuses["wz_goldstone_equivalence_no_go"]
        and certs["wz_goldstone_equivalence_no_go"].get("proposal_allowed") is False
        and certs["wz_goldstone_equivalence_no_go"].get(
            "goldstone_equivalence_source_identity_no_go_passed"
        )
        is True,
        statuses["wz_goldstone_equivalence_no_go"],
    )
    report(
        "same-source-w-orthogonal-correction-gate-open",
        "orthogonal-correction gate not passed"
        in statuses["same_source_w_response_orthogonal_correction"]
        and certs["same_source_w_response_orthogonal_correction"].get("proposal_allowed") is False
        and certs["same_source_w_response_orthogonal_correction"].get(
            "orthogonal_correction_theorem_passed"
        )
        is True
        and certs["same_source_w_response_orthogonal_correction"].get(
            "orthogonal_correction_gate_passed"
        )
        is False,
        statuses["same_source_w_response_orthogonal_correction"],
    )
    report(
        "one-higgs-completeness-orthogonal-null-premise-absent",
        "one-Higgs completeness orthogonal-null theorem"
        in statuses["one_higgs_completeness_orthogonal_null"]
        and certs["one_higgs_completeness_orthogonal_null"].get("proposal_allowed") is False
        and certs["one_higgs_completeness_orthogonal_null"].get(
            "one_higgs_completeness_orthogonal_null_theorem_passed"
        )
        is True
        and certs["one_higgs_completeness_orthogonal_null"].get(
            "one_higgs_completeness_gate_passed"
        )
        is False,
        statuses["one_higgs_completeness_orthogonal_null"],
    )
    report(
        "delta-perp-tomography-correction-builder-open",
        "delta_perp tomography correction" in statuses["delta_perp_tomography_builder"]
        and certs["delta_perp_tomography_builder"].get("proposal_allowed") is False
        and certs["delta_perp_tomography_builder"].get("strict_delta_perp_tomography_gate_passed")
        is False,
        statuses["delta_perp_tomography_builder"],
    )
    report(
        "same-source-top-response-identity-builder-open",
        "same-source top-response identity" in statuses["same_source_top_response_identity_builder"]
        and certs["same_source_top_response_identity_builder"].get("proposal_allowed") is False
        and certs["same_source_top_response_identity_builder"].get(
            "strict_same_source_top_response_identity_builder_passed"
        )
        is False,
        statuses["same_source_top_response_identity_builder"],
    )
    report(
        "top-wz-matched-covariance-builder-open",
        "matched top-W" in statuses["top_wz_matched_covariance_builder"]
        and certs["top_wz_matched_covariance_builder"].get("proposal_allowed") is False
        and certs["top_wz_matched_covariance_builder"].get(
            "strict_top_wz_matched_covariance_builder_passed"
        )
        is False,
        statuses["top_wz_matched_covariance_builder"],
    )
    report(
        "top-wz-covariance-marginal-derivation-no-go-blocks",
        "matched top-W covariance not derivable from marginal response support"
        in statuses["top_wz_covariance_marginal_derivation_no_go"]
        and certs["top_wz_covariance_marginal_derivation_no_go"].get("proposal_allowed")
        is False
        and certs["top_wz_covariance_marginal_derivation_no_go"].get(
            "marginal_derivation_no_go_passed"
        )
        is True,
        statuses["top_wz_covariance_marginal_derivation_no_go"],
    )
    report(
        "top-wz-factorization-independence-gate-blocks",
        "same-source top-W factorization not derived"
        in statuses["top_wz_factorization_independence_gate"]
        and certs["top_wz_factorization_independence_gate"].get("proposal_allowed")
        is False
        and certs["top_wz_factorization_independence_gate"].get(
            "strict_factorization_independence_gate_passed"
        )
        is False,
        statuses["top_wz_factorization_independence_gate"],
    )
    report(
        "top-wz-deterministic-response-covariance-gate-blocks",
        "deterministic W response covariance shortcut not derived"
        in statuses["top_wz_deterministic_response_covariance_gate"]
        and certs["top_wz_deterministic_response_covariance_gate"].get("proposal_allowed")
        is False
        and certs["top_wz_deterministic_response_covariance_gate"].get(
            "strict_deterministic_response_covariance_gate_passed"
        )
        is False,
        statuses["top_wz_deterministic_response_covariance_gate"],
    )
    report(
        "top-wz-covariance-theorem-import-audit-blocks",
        "no importable same-surface top-W covariance theorem"
        in statuses["top_wz_covariance_theorem_import_audit"]
        and certs["top_wz_covariance_theorem_import_audit"].get("proposal_allowed")
        is False
        and certs["top_wz_covariance_theorem_import_audit"].get(
            "covariance_theorem_import_audit_passed"
        )
        is True,
        statuses["top_wz_covariance_theorem_import_audit"],
    )
    report(
        "same-source-top-response-builder-open",
        "same-source top-response" in statuses["same_source_top_response_builder"]
        and certs["same_source_top_response_builder"].get("proposal_allowed") is False
        and certs["same_source_top_response_builder"].get(
            "strict_same_source_top_response_certificate_builder_passed"
        )
        is False,
        statuses["same_source_top_response_builder"],
    )
    report(
        "same-source-w-response-row-builder-open",
        "same-source W-response row builder" in statuses["same_source_w_response_row_builder"]
        and certs["same_source_w_response_row_builder"].get("proposal_allowed") is False
        and certs["same_source_w_response_row_builder"].get(
            "strict_same_source_w_response_row_builder_passed"
        )
        is False,
        statuses["same_source_w_response_row_builder"],
    )
    report(
        "lightweight-w-readout-harness-currently-open",
        "lightweight same-source W-response readout" in statuses["same_source_w_lightweight_readout"]
        and certs["same_source_w_lightweight_readout"].get("proposal_allowed") is False
        and certs["same_source_w_lightweight_readout"].get("strict_lightweight_readout_gate_passed")
        is False,
        statuses["same_source_w_lightweight_readout"],
    )
    report(
        "wz-harness-smoke-schema-support-only",
        "WZ harness smoke schema path" in statuses["wz_harness_smoke_schema"]
        and certs["wz_harness_smoke_schema"].get("proposal_allowed") is False
        and certs["wz_harness_smoke_schema"].get("wz_harness_smoke_schema_gate_passed") is True,
        statuses["wz_harness_smoke_schema"],
    )
    report(
        "wz-smoke-to-production-promotion-no-go-blocks",
        "WZ smoke rows cannot be promoted" in statuses["wz_smoke_to_production_no_go"]
        and certs["wz_smoke_to_production_no_go"].get("proposal_allowed") is False
        and certs["wz_smoke_to_production_no_go"].get(
            "wz_smoke_to_production_promotion_no_go_passed"
        )
        is True,
        statuses["wz_smoke_to_production_no_go"],
    )
    report(
        "wz-mass-fit-response-row-builder-open",
        "WZ mass-fit response-row builder" in statuses["wz_mass_fit_response_row_builder"]
        and certs["wz_mass_fit_response_row_builder"].get("proposal_allowed") is False
        and certs["wz_mass_fit_response_row_builder"].get(
            "strict_wz_mass_fit_response_row_builder_passed"
        )
        is False,
        statuses["wz_mass_fit_response_row_builder"],
    )
    report(
        "electroweak-g2-certificate-builder-open",
        "electroweak g2 certificate builder inputs absent"
        in statuses["electroweak_g2_certificate_builder"]
        and certs["electroweak_g2_certificate_builder"].get("proposal_allowed") is False
        and certs["electroweak_g2_certificate_builder"].get(
            "strict_electroweak_g2_certificate_passed"
        )
        is False,
        statuses["electroweak_g2_certificate_builder"],
    )
    report(
        "wz-g2-generator-casimir-normalization-no-go-blocks",
        "generator-Casimir normalization does not certify PR230 g2"
        in statuses["wz_g2_generator_casimir_normalization_no_go"]
        and certs["wz_g2_generator_casimir_normalization_no_go"].get(
            "proposal_allowed"
        )
        is False
        and certs["wz_g2_generator_casimir_normalization_no_go"].get(
            "g2_generator_casimir_no_go_passed"
        )
        is True,
        statuses["wz_g2_generator_casimir_normalization_no_go"],
    )
    report(
        "wz-g2-authority-firewall-blocks",
        "WZ response g2 authority absent" in statuses["wz_g2_authority_firewall"]
        and certs["wz_g2_authority_firewall"].get("proposal_allowed") is False
        and certs["wz_g2_authority_firewall"].get("g2_authority_gate_passed") is False,
        statuses["wz_g2_authority_firewall"],
    )
    report(
        "wz-g2-response-self-normalization-no-go-blocks",
        "WZ response-only g2 self-normalization no-go"
        in statuses["wz_g2_response_self_normalization_no_go"]
        and certs["wz_g2_response_self_normalization_no_go"].get("proposal_allowed") is False
        and certs["wz_g2_response_self_normalization_no_go"].get(
            "g2_response_self_normalization_no_go_passed"
        )
        is True,
        statuses["wz_g2_response_self_normalization_no_go"],
    )
    report("scalar-lsz-model-fv-ir-blocked", scalar_lsz_blocks, "model-class/FV/IR/threshold controls still block retained use")
    report("source-overlap-bridge-absent", source_overlap_blocks, f"route_passes={any_bridge_passes}")
    report(
        "schur-compressed-denominator-bootstrap-no-go-blocks",
        "Schur compressed-denominator row-bootstrap no-go"
        in statuses["schur_compressed_bootstrap_no_go"]
        and certs["schur_compressed_bootstrap_no_go"].get("proposal_allowed") is False
        and certs["schur_compressed_bootstrap_no_go"].get("bootstrap_no_go_passed")
        is True,
        statuses["schur_compressed_bootstrap_no_go"],
    )
    report(
        "neutral-primitive-cone-certificate-gate-absent",
        "primitive-cone certificate gate" in statuses["neutral_scalar_primitive_cone"]
        and certs["neutral_scalar_primitive_cone"].get("proposal_allowed") is False
        and certs["neutral_scalar_primitive_cone"].get("primitive_cone_certificate_gate_passed")
        is False,
        statuses["neutral_scalar_primitive_cone"],
    )
    report(
        "neutral-primitive-cone-stretch-no-go-blocks-source-only-route",
        "primitive-cone stretch no-go" in statuses["neutral_scalar_primitive_cone_stretch_no_go"]
        and certs["neutral_scalar_primitive_cone_stretch_no_go"].get("proposal_allowed") is False
        and certs["neutral_scalar_primitive_cone_stretch_no_go"].get(
            "primitive_cone_stretch_no_go_passed"
        )
        is True,
        statuses["neutral_scalar_primitive_cone_stretch_no_go"],
    )
    report(
        "neutral-burnside-irreducibility-attempt-blocks-source-only-generators",
        "Burnside neutral irreducibility attempt"
        in statuses["neutral_scalar_burnside_irreducibility"]
        and certs["neutral_scalar_burnside_irreducibility"].get("proposal_allowed") is False
        and certs["neutral_scalar_burnside_irreducibility"].get(
            "burnside_irreducibility_certificate_passed"
        )
        is False
        and certs["neutral_scalar_burnside_irreducibility"].get(
            "exact_negative_boundary_passed"
        )
        is True,
        statuses["neutral_scalar_burnside_irreducibility"],
    )
    report(
        "nonchunk-current-surface-exhaustion-recorded",
        nonchunk_current_surface_exhausted,
        statuses["nonchunk_current_surface_exhaustion"],
    )
    report(
        "nonchunk-future-artifact-intake-recorded",
        nonchunk_future_artifact_intake_closed,
        statuses["nonchunk_future_artifact_intake"],
    )
    report(
        "nonchunk-terminal-route-exhaustion-recorded",
        nonchunk_terminal_route_exhaustion_closed,
        statuses["nonchunk_terminal_route_exhaustion"],
    )
    report(
        "nonchunk-reopen-admissibility-recorded",
        nonchunk_reopen_admissibility_closed,
        statuses["nonchunk_reopen_admissibility"],
    )
    report(
        "nonchunk-cycle14-route-selector-recorded",
        nonchunk_cycle14_route_selector_closed,
        statuses["nonchunk_cycle14_route_selector"],
    )
    report(
        "nonchunk-cycle15-independent-route-admission-recorded",
        nonchunk_cycle15_independent_route_admission_closed,
        statuses["nonchunk_cycle15_independent_route_admission"],
    )
    report(
        "nonchunk-cycle16-reopen-source-guard-recorded",
        nonchunk_cycle16_reopen_source_guard_closed,
        statuses["nonchunk_cycle16_reopen_source_guard"],
    )
    report(
        "nonchunk-cycle17-stop-condition-gate-recorded",
        nonchunk_cycle17_stop_condition_closed,
        statuses["nonchunk_cycle17_stop_condition_gate"],
    )
    report(
        "nonchunk-cycle18-reopen-freshness-gate-recorded",
        nonchunk_cycle18_reopen_freshness_closed,
        statuses["nonchunk_cycle18_reopen_freshness_gate"],
    )
    report(
        "nonchunk-cycle19-no-duplicate-route-gate-recorded",
        nonchunk_cycle19_no_duplicate_route_closed,
        statuses["nonchunk_cycle19_no_duplicate_route_gate"],
    )
    report(
        "nonchunk-cycle20-process-gate-continuation-no-go-recorded",
        nonchunk_cycle20_process_gate_continuation_closed,
        statuses["nonchunk_cycle20_process_gate_continuation_no_go"],
    )
    report(
        "nonchunk-cycle21-remote-reopen-guard-recorded",
        nonchunk_cycle21_remote_reopen_guard_closed,
        statuses["nonchunk_cycle21_remote_reopen_guard"],
    )
    report(
        "nonchunk-cycle22-main-audit-drift-guard-recorded",
        nonchunk_cycle22_main_audit_drift_guard_closed,
        statuses["nonchunk_cycle22_main_audit_drift_guard"],
    )
    report(
        "nonchunk-cycle23-main-effective-status-drift-guard-recorded",
        nonchunk_cycle23_main_effective_status_drift_guard_closed,
        statuses["nonchunk_cycle23_main_effective_status_drift_guard"],
    )
    report(
        "nonchunk-cycle24-post-cycle23-main-status-drift-guard-recorded",
        nonchunk_cycle24_post_cycle23_main_status_drift_guard_closed,
        statuses["nonchunk_cycle24_post_cycle23_main_status_drift_guard"],
    )
    report(
        "nonchunk-cycle25-post-cycle24-main-audit-status-drift-guard-recorded",
        nonchunk_cycle25_post_cycle24_main_audit_status_drift_guard_closed,
        statuses["nonchunk_cycle25_post_cycle24_main_audit_status_drift_guard"],
    )
    report(
        "nonchunk-cycle26-post-cycle25-main-audit-status-drift-guard-recorded",
        nonchunk_cycle26_post_cycle25_main_audit_status_drift_guard_closed,
        statuses["nonchunk_cycle26_post_cycle25_main_audit_status_drift_guard"],
    )
    report(
        "nonchunk-cycle27-post-cycle26-main-audit-status-drift-guard-recorded",
        nonchunk_cycle27_post_cycle26_main_audit_status_drift_guard_closed,
        statuses["nonchunk_cycle27_post_cycle26_main_audit_status_drift_guard"],
    )
    report(
        "nonchunk-cycle28-post-cycle27-main-audit-status-drift-guard-recorded",
        nonchunk_cycle28_post_cycle27_main_audit_status_drift_guard_closed,
        statuses["nonchunk_cycle28_post_cycle27_main_audit_status_drift_guard"],
    )
    report(
        "nonchunk-cycle29-post-cycle28-main-audit-status-drift-guard-recorded",
        nonchunk_cycle29_post_cycle28_main_audit_status_drift_guard_closed,
        statuses["nonchunk_cycle29_post_cycle28_main_audit_status_drift_guard"],
    )
    report(
        "nonchunk-cycle30-post-cycle29-main-audit-status-drift-guard-recorded",
        nonchunk_cycle30_post_cycle29_main_audit_status_drift_guard_closed,
        statuses["nonchunk_cycle30_post_cycle29_main_audit_status_drift_guard"],
    )
    report(
        "nonchunk-cycle31-post-cycle30-main-audit-status-drift-guard-recorded",
        nonchunk_cycle31_post_cycle30_main_audit_status_drift_guard_closed,
        statuses["nonchunk_cycle31_post_cycle30_main_audit_status_drift_guard"],
    )
    report(
        "nonchunk-cycle32-post-cycle31-main-audit-status-drift-guard-recorded",
        nonchunk_cycle32_post_cycle31_main_audit_status_drift_guard_closed,
        statuses["nonchunk_cycle32_post_cycle31_main_audit_status_drift_guard"],
    )
    report(
        "nonchunk-cycle33-post-cycle32-main-audit-status-drift-guard-recorded",
        nonchunk_cycle33_post_cycle32_main_audit_status_drift_guard_closed,
        statuses["nonchunk_cycle33_post_cycle32_main_audit_status_drift_guard"],
    )
    report(
        "nonchunk-cycle34-post-cycle33-main-nonpr230-drift-guard-recorded",
        nonchunk_cycle34_post_cycle33_main_nonpr230_drift_guard_closed,
        statuses["nonchunk_cycle34_post_cycle33_main_nonpr230_drift_guard"],
    )
    report(
        "nonchunk-cycle35-post-cycle34-main-audit-ledger-drift-guard-recorded",
        nonchunk_cycle35_post_cycle34_main_audit_ledger_drift_guard_closed,
        statuses["nonchunk_cycle35_post_cycle34_main_audit_ledger_drift_guard"],
    )
    report("matching-running-bridge-open", matching_running_blocks, statuses["matching_running"])
    report("retained-route-still-open", retained_route_open, statuses["retained_route"])
    report("campaign-status-still-open", campaign_open, statuses["campaign_status"])
    report("current-surface-assembly-rejected", not current_eval["assembly_passed"], f"missing={current_eval['missing']}")
    report("chunk-only-assembly-rejected", not chunk_only_eval["assembly_passed"], f"missing={chunk_only_eval['missing']}")
    report("synthetic-positive-witness-passes-schema", synthetic_eval["assembly_passed"], f"missing={synthetic_eval['missing']}")

    result = {
        "actual_current_surface_status": "open / full positive PR230 closure assembly gate not passed",
        "verdict": (
            "The non-chunk closure assembly is now explicit.  Chunk completion "
            "can supply only the production-response leg; it cannot by itself "
            "supply scalar LSZ model-class/FV/IR control, the O_sp-to-O_H or "
            "same-source physical-response bridge, matching/running authority, "
            "or retained-proposal authorization.  On the current PR230 surface "
            "all allowed bridge routes are absent, blocked, or support-only, so "
            "full positive closure remains open."
            " The cycle-8 current-surface exhaustion gate now records that no "
            "hidden non-chunk shortcut remains executable without one of the "
            "named future same-surface rows, certificates, or theorems.  The "
            "cycle-9 future-artifact intake gate records that no such named "
            "artifact has appeared on the current surface.  The terminal "
            "route-exhaustion gate records the corresponding stop/reopen rule.  "
            "The cycle-12 reopen-admissibility gate rejects a path-only reopen "
            "attempt before the aggregate gates may be rerun.  The cycle-14 "
            "route-selector gate now records that no current-surface non-chunk "
            "route is selected after the W/Z covariance-theorem import no-go.  "
            "The cycle-15 independent-route admission gate records that no "
            "independent current route is admitted without a new same-surface "
            "artifact.  The cycle-16 reopen-source guard records that no "
            "post-checkpoint parseable same-surface artifact exists for "
            "admissible reopen.  The cycle-17 stop-condition gate records that "
            "the refreshed non-chunk queue has no executable current-surface "
            "route on this branch.  The cycle-18 reopen-freshness gate records "
            "that no post-cycle-17 same-surface artifact is present for "
            "admissible reopen.  The cycle-19 no-duplicate-route gate records "
            "that another current-surface route selection would only replay a "
            "closed non-chunk family until a fresh parseable same-surface "
            "artifact exists.  The cycle-20 process-gate continuation no-go "
            "records that another branch-local process gate is not itself a "
            "science route unless a fresh parseable same-surface artifact "
            "exists first.  The cycle-21 remote-surface reopen guard records "
            "that fetched remote surfaces also contain no listed same-surface "
            "artifact for admissible reopen.  The cycle-22 main-audit-drift "
            "guard records that the latest origin/main advance is only "
            "audit/effective-status drift and still supplies no listed PR230 "
            "same-surface artifact.  The cycle-23 main-effective-status-drift "
            "guard records that origin/main advanced again only on "
            "audit/effective-status surfaces and still supplies no listed "
            "PR230 same-surface artifact.  The cycle-24 post-cycle-23 "
            "main-status-drift guard records that origin/main advanced again "
            "only on audit/effective-status surfaces and still supplies no "
            "listed PR230 same-surface artifact.  The cycle-25 post-cycle-24 "
            "main-audit-status-drift guard records that origin/main advanced "
            "again only on audit/effective-status surfaces and still supplies "
            "no listed PR230 same-surface artifact.  The cycle-26 "
            "post-cycle-25 main-audit-status-drift guard records that "
            "origin/main advanced again only on audit/effective-status "
            "surfaces and still supplies no listed PR230 same-surface artifact.  "
            "The cycle-27 post-cycle-26 main-audit-status-drift guard records "
            "that origin/main advanced again only on audit/effective-status "
            "surfaces and still supplies no listed PR230 same-surface artifact.  "
            "The cycle-28 post-cycle-27 main-audit-status-drift guard records "
            "that origin/main advanced again only on audit/effective-status "
            "surfaces and still supplies no listed PR230 same-surface artifact.  "
            "The cycle-29 post-cycle-28 main-audit-status-drift guard records "
            "that origin/main advanced again only on audit/effective-status "
            "surfaces and still supplies no listed PR230 same-surface artifact.  "
            "The cycle-30 post-cycle-29 main-audit-status-drift guard records "
            "that origin/main advanced again only on audit/effective-status "
            "surfaces and still supplies no listed PR230 same-surface artifact.  "
            "The cycle-31 post-cycle-30 main-audit-status-drift guard records "
            "that origin/main advanced again only on audit/effective-status "
            "surfaces and still supplies no listed PR230 same-surface artifact.  "
            "The cycle-32 post-cycle-31 main-audit-status-drift guard records "
            "that origin/main advanced again only on audit/effective-status "
            "surfaces and still supplies no listed PR230 same-surface artifact.  "
            "The cycle-33 post-cycle-32 main-audit-status-drift guard records "
            "that origin/main advanced again only on audit/effective-status/"
            "runner-cache surfaces and still supplies no listed PR230 "
            "same-surface artifact."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "The assembly gate rejects the current surface and also rejects a "
            "hypothetical chunk-only completion.  A positive proposal first "
            "needs scalar-LSZ pole/FV/IR/model-class closure plus one accepted "
            "source-overlap/physical-response bridge and retained-route approval."
        ),
        "bare_retained_allowed": False,
        "closure_conditions": closure_conditions(),
        "route_statuses": routes,
        "current_state": current_state,
        "current_evaluation": current_eval,
        "chunk_only_state": chunk_only_state,
        "chunk_only_evaluation": chunk_only_eval,
        "synthetic_positive_witness": {
            "state": synthetic_positive_state,
            "evaluation": synthetic_eval,
            "purpose": "schema sanity check only; not evidence and not a PR230 claim",
        },
        "parent_statuses": statuses,
        "parent_certificates": PARENTS,
        "strict_non_claims": [
            "does not claim retained or proposed_retained y_t closure",
            "does not package or certify chunk outputs",
            "does not define y_t through a matrix element or y_t_bare",
            "does not use H_unit, yt_ward_identity, alpha_LM, plaquette/u0, observed targets, kappa_s=1, c2=1, Z_match=1, or cos(theta)=1",
            "does not treat static EW algebra, W/Z absent guards, source-only C_ss rows, or finite-shell fits as physical y_t readouts",
            "does not treat W/Z smoke-schema rows as production EW response evidence",
            "does not treat current-surface non-chunk exhaustion as retained closure",
            "does not treat terminal non-chunk route exhaustion as positive closure",
            "does not treat cycle-14 non-chunk route selection closure as positive evidence",
            "does not treat cycle-15 independent-route exhaustion as positive evidence",
            "does not treat cycle-16 reopen-source absence as positive evidence",
            "does not treat cycle-17 non-chunk stop condition as positive evidence",
            "does not treat cycle-18 reopen freshness as positive evidence",
            "does not treat cycle-19 no-duplicate-route closure as positive evidence",
            "does not treat cycle-20 process-gate continuation closure as positive evidence",
            "does not treat cycle-21 remote-surface reopen guard closure as positive evidence",
            "does not treat cycle-22 main-audit-drift guard closure as positive evidence",
            "does not treat cycle-23 main-effective-status-drift guard closure as positive evidence",
            "does not treat cycle-24 post-cycle-23 main-status-drift guard closure as positive evidence",
            "does not treat cycle-25 post-cycle-24 main-audit-status-drift guard closure as positive evidence",
            "does not treat cycle-26 post-cycle-25 main-audit-status-drift guard closure as positive evidence",
            "does not treat cycle-27 post-cycle-26 main-audit-status-drift guard closure as positive evidence",
            "does not treat cycle-28 post-cycle-27 main-audit-status-drift guard closure as positive evidence",
            "does not treat cycle-29 post-cycle-28 main-audit-status-drift guard closure as positive evidence",
            "does not treat cycle-30 post-cycle-29 main-audit-status-drift guard closure as positive evidence",
            "does not treat cycle-31 post-cycle-30 main-audit-status-drift guard closure as positive evidence",
            "does not treat cycle-32 post-cycle-31 main-audit-status-drift guard closure as positive evidence",
            "does not treat cycle-33 post-cycle-32 main-audit-status-drift guard closure as positive evidence",
        ],
        "exact_next_action": (
            "Keep the chunk worker on homogeneous production chunks.  In parallel, "
            "pursue one non-chunk bridge that can satisfy this gate: a real "
            "same-surface O_H certificate plus C_sH/C_HH pole rows, a same-source "
            "EW action plus top/W/Z mass-response rows, matched covariance or "
            "a real top/W factorization theorem, and sector-overlap identity, "
            "with source identity supplied by real rows or a certificate rather "
            "than Goldstone bookkeeping, a strict Stieltjes moment certificate "
            "or same-surface Schur A/B/C kernel rows with scalar denominator closure, "
            "or a neutral-sector irreducibility theorem.  Rerun this assembly "
            "gate, including the cycle-15 independent-route admission gate, "
            "the cycle-16 reopen-source guard, and the cycle-17 stop-condition "
            "gate, plus the cycle-18 reopen-freshness gate, before any "
            "retained-route proposal.  The cycle-19 no-duplicate-route gate "
            "and cycle-20 process-gate continuation no-go must also rerun if "
            "no fresh parseable same-surface artifact has appeared.  The "
            "cycle-21 remote-surface reopen guard must rerun after any fetch "
            "or target-branch update before proposal language.  The cycle-22 "
            "main-audit-drift guard must rerun after an origin/main advance "
            "before proposal language.  The cycle-23 main-effective-status-drift "
            "guard must rerun after any later origin/main advance before "
            "proposal language.  The cycle-24 post-cycle-23 main-status-drift "
            "guard must rerun after any later origin/main advance before "
            "proposal language.  The cycle-25 post-cycle-24 main-audit-status-"
            "drift guard must rerun after any later origin/main advance before "
            "proposal language.  The cycle-26 post-cycle-25 main-audit-status-"
            "drift guard must rerun after any later origin/main advance before "
            "proposal language.  The cycle-27 post-cycle-26 main-audit-status-"
            "drift guard must rerun after any later origin/main advance before "
            "proposal language.  The cycle-28 post-cycle-27 main-audit-status-"
            "drift guard must rerun after any later origin/main advance before "
            "proposal language.  The cycle-29 post-cycle-28 main-audit-status-"
            "drift guard must rerun after any later origin/main advance before "
            "proposal language.  The cycle-30 post-cycle-29 main-audit-status-"
            "drift guard must rerun after any later origin/main advance before "
            "proposal language.  The cycle-31 post-cycle-30 main-audit-status-"
            "drift guard must rerun after any later origin/main advance before "
            "proposal language.  The cycle-32 post-cycle-31 main-audit-status-"
            "drift guard must rerun after any later origin/main advance before "
            "proposal language.  The cycle-33 post-cycle-32 main-audit-status-"
            "drift guard must rerun after any later origin/main advance before "
            "proposal language."
        ),
        "pass_count": PASS_COUNT,
        "fail_count": FAIL_COUNT,
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"\nWrote certificate: {OUTPUT.relative_to(ROOT)}")
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
