#!/usr/bin/env python3
"""
PR #230 physics-loop campaign status certificate.

This runner summarizes the current 12h-campaign work package.  It does not
claim retained closure.  It verifies that the live analytic shortcuts have been
classified and that the remaining closure routes require either production
evidence or a genuinely new theorem/observable.
"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "yt_pr230_campaign_status_certificate_2026-05-01.json"
GENERIC_CHUNK_TARGET_PATTERN = "yt_fh_lsz_chunk*_target_timeseries_generic_checkpoint_2026-05-02.json"
MULTITAU_CHUNK_TARGET_PATTERN = "yt_fh_lsz_chunk*_multitau_target_timeseries_checkpoint_2026-05-03.json"

PASS_COUNT = 0
FAIL_COUNT = 0


def report(tag: str, ok: bool, msg: str) -> None:
    global PASS_COUNT, FAIL_COUNT
    if ok:
        PASS_COUNT += 1
        status = "PASS"
    else:
        FAIL_COUNT += 1
        status = "FAIL"
    print(f"  [{status}] {tag}: {msg}")


def load(rel: str) -> dict:
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


def generic_chunk_target_key(path: Path) -> str:
    stem = path.name.removeprefix("yt_fh_lsz_").removesuffix(
        "_target_timeseries_generic_checkpoint_2026-05-02.json"
    )
    return f"fh_lsz_{stem}_target_timeseries_generic"


def multitau_chunk_target_key(path: Path) -> str:
    stem = path.name.removeprefix("yt_fh_lsz_").removesuffix(
        "_multitau_target_timeseries_checkpoint_2026-05-03.json"
    )
    return f"fh_lsz_{stem}_multitau_target_timeseries"


def main() -> int:
    print("PR #230 campaign status certificate")
    print("=" * 72)

    certificates = {
        "key_blocker": load("outputs/yt_key_blocker_closure_attempt_2026-05-01.json"),
        "source_two_point": load("outputs/yt_scalar_source_two_point_stretch_2026-05-01.json"),
        "hs_rpa": load("outputs/yt_hs_rpa_pole_condition_attempt_2026-05-01.json"),
        "ladder_scout": load("outputs/yt_scalar_ladder_kernel_scout_2026-05-01.json"),
        "ladder_input": load("outputs/yt_scalar_ladder_kernel_input_audit_2026-05-01.json"),
        "projector_norm": load("outputs/yt_scalar_ladder_projector_normalization_obstruction_2026-05-01.json"),
        "hqet": load("outputs/yt_hqet_direct_route_requirements_2026-05-01.json"),
        "static_mass": load("outputs/yt_static_mass_matching_obstruction_2026-05-01.json"),
        "legendre": load("outputs/yt_legendre_kappa_gauge_freedom_2026-05-01.json"),
        "free_bubble": load("outputs/yt_free_scalar_two_point_pole_absence_2026-05-01.json"),
        "same_1pi": load("outputs/yt_same_1pi_scalar_pole_boundary_2026-05-01.json"),
        "lsz_norm": load("outputs/yt_scalar_lsz_normalization_cancellation_2026-05-01.json"),
        "feshbach_response": load("outputs/yt_feshbach_operator_response_boundary_2026-05-01.json"),
        "bridge_stack": load("outputs/yt_bridge_stack_import_audit_2026-05-01.json"),
        "spectral_saturation": load("outputs/yt_scalar_spectral_saturation_no_go_2026-05-01.json"),
        "large_nc": load("outputs/yt_large_nc_pole_dominance_boundary_2026-05-01.json"),
        "production_resource": load("outputs/yt_production_resource_projection_2026-05-01.json"),
        "feynman_hellmann": load("outputs/yt_feynman_hellmann_source_response_route_2026-05-01.json"),
        "mass_response": load("outputs/yt_mass_response_bracket_certificate_2026-05-01.json"),
        "source_reparametrization": load("outputs/yt_source_reparametrization_gauge_no_go_2026-05-01.json"),
        "canonical_scalar_import": load("outputs/yt_canonical_scalar_normalization_import_audit_2026-05-01.json"),
        "source_to_higgs_lsz": load("outputs/yt_source_to_higgs_lsz_closure_attempt_2026-05-01.json"),
        "cl3_source_unit": load("outputs/yt_cl3_source_unit_normalization_no_go_2026-05-01.json"),
        "gauge_vev_source_overlap": load("outputs/yt_gauge_vev_source_overlap_no_go_2026-05-01.json"),
        "scalar_renormalization_condition_overlap": load(
            "outputs/yt_scalar_renormalization_condition_overlap_no_go_2026-05-01.json"
        ),
        "scalar_source_contact_term_scheme": load(
            "outputs/yt_scalar_source_contact_term_scheme_boundary_2026-05-01.json"
        ),
        "scalar_source_response_harness": load("outputs/yt_scalar_source_response_harness_certificate_2026-05-01.json"),
        "fh_production_protocol": load("outputs/yt_fh_production_protocol_certificate_2026-05-01.json"),
        "same_source_scalar_two_point": load("outputs/yt_same_source_scalar_two_point_lsz_measurement_2026-05-01.json"),
        "bs_kernel_residue_degeneracy": load("outputs/yt_scalar_bs_kernel_residue_degeneracy_2026-05-01.json"),
        "scalar_two_point_harness": load("outputs/yt_scalar_two_point_harness_certificate_2026-05-01.json"),
        "fh_lsz_joint_harness": load("outputs/yt_fh_lsz_joint_harness_certificate_2026-05-01.json"),
        "fh_lsz_joint_resource": load("outputs/yt_fh_lsz_joint_resource_projection_2026-05-01.json"),
        "fh_lsz_production_manifest": load("outputs/yt_fh_lsz_production_manifest_2026-05-01.json"),
        "fh_lsz_production_postprocess_gate": load(
            "outputs/yt_fh_lsz_production_postprocess_gate_2026-05-01.json"
        ),
        "fh_lsz_production_checkpoint_granularity": load(
            "outputs/yt_fh_lsz_production_checkpoint_granularity_gate_2026-05-01.json"
        ),
        "fh_lsz_chunked_production_manifest": load(
            "outputs/yt_fh_lsz_chunked_production_manifest_2026-05-01.json"
        ),
        "fh_lsz_chunk_combiner_gate": load("outputs/yt_fh_lsz_chunk_combiner_gate_2026-05-01.json"),
        "fh_lsz_chunk001_checkpoint": load("outputs/yt_fh_lsz_chunk001_checkpoint_certificate_2026-05-02.json"),
        "fh_lsz_chunk002_checkpoint": load("outputs/yt_fh_lsz_chunk002_checkpoint_certificate_2026-05-02.json"),
        "fh_lsz_ready_chunk_set_checkpoint": load(
            "outputs/yt_fh_lsz_ready_chunk_set_checkpoint_2026-05-02.json"
        ),
        "fh_lsz_ready_chunk_response_stability": load(
            "outputs/yt_fh_lsz_ready_chunk_response_stability_2026-05-02.json"
        ),
        "fh_lsz_chunk011_target_timeseries": load(
            "outputs/yt_fh_lsz_chunk011_target_timeseries_checkpoint_2026-05-02.json"
        ),
        "fh_lsz_chunk011_target_timeseries_generic": load(
            "outputs/yt_fh_lsz_chunk011_target_timeseries_generic_checkpoint_2026-05-02.json"
        ),
        "fh_lsz_chunk012_target_timeseries_generic": load(
            "outputs/yt_fh_lsz_chunk012_target_timeseries_generic_checkpoint_2026-05-02.json"
        ),
        "fh_lsz_pole_fit_kinematics": load("outputs/yt_fh_lsz_pole_fit_kinematics_gate_2026-05-01.json"),
        "fh_lsz_pole_fit_postprocessor": load("outputs/yt_fh_lsz_pole_fit_postprocessor_2026-05-01.json"),
        "fh_lsz_finite_shell_identifiability": load(
            "outputs/yt_fh_lsz_finite_shell_identifiability_no_go_2026-05-02.json"
        ),
        "fh_lsz_pole_fit_model_class_gate": load(
            "outputs/yt_fh_lsz_pole_fit_model_class_gate_2026-05-02.json"
        ),
        "fh_lsz_model_class_semantic_firewall": load(
            "outputs/yt_fh_lsz_model_class_semantic_firewall_2026-05-04.json"
        ),
        "fh_lsz_stieltjes_model_class": load(
            "outputs/yt_fh_lsz_stieltjes_model_class_obstruction_2026-05-02.json"
        ),
        "fh_lsz_stieltjes_moment_certificate_gate": load(
            "outputs/yt_fh_lsz_stieltjes_moment_certificate_gate_2026-05-05.json"
        ),
        "fh_lsz_pade_stieltjes_bounds_gate": load(
            "outputs/yt_fh_lsz_pade_stieltjes_bounds_gate_2026-05-05.json"
        ),
        "fh_lsz_polefit8x8_stieltjes_proxy_diagnostic": load(
            "outputs/yt_fh_lsz_polefit8x8_stieltjes_proxy_diagnostic_2026-05-05.json"
        ),
        "fh_lsz_complete_bernstein_inverse_diagnostic": load(
            "outputs/yt_fh_lsz_complete_bernstein_inverse_diagnostic_2026-05-05.json"
        ),
        "pr230_scalar_lsz_holonomic_exact_authority_attempt": load(
            "outputs/yt_pr230_scalar_lsz_holonomic_exact_authority_attempt_2026-05-05.json"
        ),
        "pr230_scalar_lsz_carleman_tauberian_determinacy_attempt": load(
            "outputs/yt_pr230_scalar_lsz_carleman_tauberian_determinacy_attempt_2026-05-05.json"
        ),
        "fh_lsz_contact_subtraction_identifiability": load(
            "outputs/yt_fh_lsz_contact_subtraction_identifiability_2026-05-05.json"
        ),
        "fh_lsz_affine_contact_complete_monotonicity": load(
            "outputs/yt_fh_lsz_affine_contact_complete_monotonicity_no_go_2026-05-05.json"
        ),
        "fh_lsz_polynomial_contact_finite_shell": load(
            "outputs/yt_fh_lsz_polynomial_contact_finite_shell_no_go_2026-05-05.json"
        ),
        "fh_lsz_polynomial_contact_repair": load(
            "outputs/yt_fh_lsz_polynomial_contact_repair_no_go_2026-05-05.json"
        ),
        "pr230_nonchunk_route_family_import_audit": load(
            "outputs/yt_pr230_nonchunk_route_family_import_audit_2026-05-05.json"
        ),
        "pr230_nonchunk_current_surface_exhaustion": load(
            "outputs/yt_pr230_nonchunk_current_surface_exhaustion_gate_2026-05-05.json"
        ),
        "pr230_nonchunk_future_artifact_intake": load(
            "outputs/yt_pr230_nonchunk_future_artifact_intake_gate_2026-05-05.json"
        ),
        "pr230_nonchunk_terminal_route_exhaustion": load(
            "outputs/yt_pr230_nonchunk_terminal_route_exhaustion_gate_2026-05-05.json"
        ),
        "pr230_nonchunk_reopen_admissibility": load(
            "outputs/yt_pr230_nonchunk_reopen_admissibility_gate_2026-05-05.json"
        ),
        "pr230_nonchunk_cycle14_route_selector": load(
            "outputs/yt_pr230_nonchunk_cycle14_route_selector_gate_2026-05-05.json"
        ),
        "pr230_nonchunk_cycle15_independent_route_admission": load(
            "outputs/yt_pr230_nonchunk_cycle15_independent_route_admission_gate_2026-05-05.json"
        ),
        "pr230_nonchunk_cycle16_reopen_source_guard": load(
            "outputs/yt_pr230_nonchunk_cycle16_reopen_source_guard_2026-05-05.json"
        ),
        "pr230_nonchunk_cycle17_stop_condition_gate": load(
            "outputs/yt_pr230_nonchunk_cycle17_stop_condition_gate_2026-05-05.json"
        ),
        "pr230_nonchunk_cycle18_reopen_freshness_gate": load(
            "outputs/yt_pr230_nonchunk_cycle18_reopen_freshness_gate_2026-05-05.json"
        ),
        "pr230_nonchunk_cycle19_no_duplicate_route_gate": load(
            "outputs/yt_pr230_nonchunk_cycle19_no_duplicate_route_gate_2026-05-05.json"
        ),
        "pr230_nonchunk_cycle20_process_gate_continuation_no_go": load(
            "outputs/yt_pr230_nonchunk_cycle20_process_gate_continuation_no_go_2026-05-05.json"
        ),
        "pr230_nonchunk_cycle21_remote_reopen_guard": load(
            "outputs/yt_pr230_nonchunk_cycle21_remote_reopen_guard_2026-05-05.json"
        ),
        "pr230_nonchunk_cycle22_main_audit_drift_guard": load(
            "outputs/yt_pr230_nonchunk_cycle22_main_audit_drift_guard_2026-05-05.json"
        ),
        "pr230_nonchunk_cycle23_main_effective_status_drift_guard": load(
            "outputs/yt_pr230_nonchunk_cycle23_main_effective_status_drift_guard_2026-05-05.json"
        ),
        "pr230_nonchunk_cycle24_post_cycle23_main_status_drift_guard": load(
            "outputs/yt_pr230_nonchunk_cycle24_post_cycle23_main_status_drift_guard_2026-05-05.json"
        ),
        "pr230_nonchunk_cycle25_post_cycle24_main_audit_status_drift_guard": load(
            "outputs/yt_pr230_nonchunk_cycle25_post_cycle24_main_audit_status_drift_guard_2026-05-05.json"
        ),
        "pr230_nonchunk_cycle26_post_cycle25_main_audit_status_drift_guard": load(
            "outputs/yt_pr230_nonchunk_cycle26_post_cycle25_main_audit_status_drift_guard_2026-05-05.json"
        ),
        "pr230_nonchunk_cycle27_post_cycle26_main_audit_status_drift_guard": load(
            "outputs/yt_pr230_nonchunk_cycle27_post_cycle26_main_audit_status_drift_guard_2026-05-05.json"
        ),
        "pr230_nonchunk_cycle28_post_cycle27_main_audit_status_drift_guard": load(
            "outputs/yt_pr230_nonchunk_cycle28_post_cycle27_main_audit_status_drift_guard_2026-05-05.json"
        ),
        "pr230_nonchunk_cycle29_post_cycle28_main_audit_status_drift_guard": load(
            "outputs/yt_pr230_nonchunk_cycle29_post_cycle28_main_audit_status_drift_guard_2026-05-05.json"
        ),
        "pr230_nonchunk_cycle30_post_cycle29_main_audit_status_drift_guard": load(
            "outputs/yt_pr230_nonchunk_cycle30_post_cycle29_main_audit_status_drift_guard_2026-05-05.json"
        ),
        "pr230_nonchunk_cycle31_post_cycle30_main_audit_status_drift_guard": load(
            "outputs/yt_pr230_nonchunk_cycle31_post_cycle30_main_audit_status_drift_guard_2026-05-05.json"
        ),
        "pr230_nonchunk_cycle32_post_cycle31_main_audit_status_drift_guard": load(
            "outputs/yt_pr230_nonchunk_cycle32_post_cycle31_main_audit_status_drift_guard_2026-05-05.json"
        ),
        "pr230_nonchunk_cycle33_post_cycle32_main_audit_status_drift_guard": load(
            "outputs/yt_pr230_nonchunk_cycle33_post_cycle32_main_audit_status_drift_guard_2026-05-05.json"
        ),
        "pr230_nonchunk_cycle34_post_cycle33_main_nonpr230_drift_guard": load(
            "outputs/yt_pr230_nonchunk_cycle34_post_cycle33_main_nonpr230_drift_guard_2026-05-05.json"
        ),
        "pr230_nonchunk_cycle35_post_cycle34_main_audit_ledger_drift_guard": load(
            "outputs/yt_pr230_nonchunk_cycle35_post_cycle34_main_audit_ledger_drift_guard_2026-05-05.json"
        ),
        "fh_lsz_pole_saturation_threshold_gate": load(
            "outputs/yt_fh_lsz_pole_saturation_threshold_gate_2026-05-02.json"
        ),
        "fh_lsz_threshold_authority_audit": load(
            "outputs/yt_fh_lsz_threshold_authority_import_audit_2026-05-02.json"
        ),
        "confinement_gap_threshold_import": load(
            "outputs/yt_confinement_gap_threshold_import_audit_2026-05-02.json"
        ),
        "fh_lsz_finite_volume_pole_saturation": load(
            "outputs/yt_fh_lsz_finite_volume_pole_saturation_obstruction_2026-05-02.json"
        ),
        "fh_lsz_numba_seed_independence": load(
            "outputs/yt_fh_lsz_numba_seed_independence_audit_2026-05-02.json"
        ),
        "fh_lsz_uniform_gap_self_certification": load(
            "outputs/yt_fh_lsz_uniform_gap_self_certification_no_go_2026-05-02.json"
        ),
        "scalar_denominator_theorem_closure": load(
            "outputs/yt_scalar_denominator_theorem_closure_attempt_2026-05-02.json"
        ),
        "fh_lsz_soft_continuum_threshold": load(
            "outputs/yt_fh_lsz_soft_continuum_threshold_no_go_2026-05-02.json"
        ),
        "reflection_positivity_lsz_shortcut": load(
            "outputs/yt_reflection_positivity_lsz_shortcut_no_go_2026-05-02.json"
        ),
        "effective_potential_hessian_source_overlap": load(
            "outputs/yt_effective_potential_hessian_source_overlap_no_go_2026-05-02.json"
        ),
        "brst_nielsen_higgs_identity": load(
            "outputs/yt_brst_nielsen_higgs_identity_no_go_2026-05-02.json"
        ),
        "cl3_automorphism_source_identity": load(
            "outputs/yt_cl3_automorphism_source_identity_no_go_2026-05-02.json"
        ),
        "same_source_pole_data_sufficiency": load(
            "outputs/yt_same_source_pole_data_sufficiency_gate_2026-05-02.json"
        ),
        "source_functional_lsz_identifiability": load(
            "outputs/yt_source_functional_lsz_identifiability_theorem_2026-05-03.json"
        ),
        "isolated_pole_gram_factorization": load(
            "outputs/yt_isolated_pole_gram_factorization_theorem_2026-05-03.json"
        ),
        "osp_oh_assumption_route_audit": load(
            "outputs/yt_osp_oh_assumption_route_audit_2026-05-04.json"
        ),
        "osp_oh_literature_bridge": load(
            "outputs/yt_osp_oh_literature_bridge_2026-05-04.json"
        ),
        "fms_oh_certificate_construction_attempt": load(
            "outputs/yt_fms_oh_certificate_construction_attempt_2026-05-04.json"
        ),
        "complete_source_spectrum_identity_no_go": load(
            "outputs/yt_complete_source_spectrum_identity_no_go_2026-05-02.json"
        ),
        "neutral_scalar_top_coupling_tomography_gate": load(
            "outputs/yt_neutral_scalar_top_coupling_tomography_gate_2026-05-02.json"
        ),
        "non_source_response_rank_repair_sufficiency": load(
            "outputs/yt_non_source_response_rank_repair_sufficiency_2026-05-03.json"
        ),
        "positivity_improving_neutral_scalar_rank_one": load(
            "outputs/yt_positivity_improving_neutral_scalar_rank_one_support_2026-05-03.json"
        ),
        "gauge_perron_neutral_scalar_rank_one_import": load(
            "outputs/yt_gauge_perron_to_neutral_scalar_rank_one_import_audit_2026-05-03.json"
        ),
        "neutral_scalar_positivity_improving_direct_closure": load(
            "outputs/yt_neutral_scalar_positivity_improving_direct_closure_attempt_2026-05-03.json"
        ),
        "neutral_scalar_irreducibility_authority_audit": load(
            "outputs/yt_neutral_scalar_irreducibility_authority_audit_2026-05-04.json"
        ),
        "neutral_scalar_primitive_cone_certificate_gate": load(
            "outputs/yt_neutral_scalar_primitive_cone_certificate_gate_2026-05-05.json"
        ),
        "neutral_scalar_primitive_cone_stretch_no_go": load(
            "outputs/yt_neutral_scalar_primitive_cone_stretch_no_go_2026-05-05.json"
        ),
        "neutral_scalar_burnside_irreducibility_attempt": load(
            "outputs/yt_neutral_scalar_burnside_irreducibility_attempt_2026-05-05.json"
        ),
        "neutral_offdiagonal_generator_derivation_attempt": load(
            "outputs/yt_neutral_offdiagonal_generator_derivation_attempt_2026-05-05.json"
        ),
        "pr230_logdet_hessian_neutral_mixing_attempt": load(
            "outputs/yt_pr230_logdet_hessian_neutral_mixing_attempt_2026-05-05.json"
        ),
        "scalar_carrier_projector_closure": load(
            "outputs/yt_scalar_carrier_projector_closure_attempt_2026-05-02.json"
        ),
        "kprime_closure": load("outputs/yt_kprime_closure_attempt_2026-05-02.json"),
        "pr230_matching_running_bridge_gate": load(
            "outputs/yt_pr230_matching_running_bridge_gate_2026-05-04.json"
        ),
        "schur_complement_kprime_sufficiency": load(
            "outputs/yt_schur_complement_kprime_sufficiency_2026-05-03.json"
        ),
        "schur_kprime_row_absence_guard": load(
            "outputs/yt_schur_kprime_row_absence_guard_2026-05-03.json"
        ),
        "legacy_schur_bridge_import_audit": load(
            "outputs/yt_legacy_schur_bridge_import_audit_2026-05-03.json"
        ),
        "schur_kernel_row_contract_gate": load(
            "outputs/yt_schur_kernel_row_contract_gate_2026-05-03.json"
        ),
        "schur_row_candidate_extraction_attempt": load(
            "outputs/yt_schur_row_candidate_extraction_attempt_2026-05-03.json"
        ),
        "schur_compressed_denominator_row_bootstrap_no_go": load(
            "outputs/yt_schur_compressed_denominator_row_bootstrap_no_go_2026-05-05.json"
        ),
        "pr230_exact_tensor_schur_row_feasibility_attempt": load(
            "outputs/yt_pr230_exact_tensor_schur_row_feasibility_attempt_2026-05-05.json"
        ),
        "pr230_schur_abc_definition_derivation_attempt": load(
            "outputs/yt_pr230_schur_abc_definition_derivation_attempt_2026-05-05.json"
        ),
        "fh_lsz_higgs_pole_identity": load(
            "outputs/yt_fh_lsz_higgs_pole_identity_gate_2026-05-02.json"
        ),
        "fh_gauge_normalized_response": load(
            "outputs/yt_fh_gauge_normalized_response_route_2026-05-02.json"
        ),
        "fh_gauge_mass_response_observable_gap": load(
            "outputs/yt_fh_gauge_mass_response_observable_gap_2026-05-02.json"
        ),
        "fh_gauge_mass_response_manifest": load(
            "outputs/yt_fh_gauge_mass_response_manifest_2026-05-02.json"
        ),
        "fh_gauge_mass_response_certificate_builder": load(
            "outputs/yt_fh_gauge_mass_response_certificate_builder_2026-05-03.json"
        ),
        "same_source_wz_response_certificate_gate": load(
            "outputs/yt_same_source_wz_response_certificate_gate_2026-05-02.json"
        ),
        "wz_response_harness_absence_guard": load(
            "outputs/yt_wz_response_harness_absence_guard_2026-05-02.json"
        ),
        "wz_response_repo_harness_import_audit": load(
            "outputs/yt_wz_response_repo_harness_import_audit_2026-05-03.json"
        ),
        "wz_response_measurement_row_contract_gate": load(
            "outputs/yt_wz_response_measurement_row_contract_gate_2026-05-03.json"
        ),
        "wz_response_row_production_attempt": load(
            "outputs/yt_wz_response_row_production_attempt_2026-05-03.json"
        ),
        "wz_response_harness_implementation_plan": load(
            "outputs/yt_wz_response_harness_implementation_plan_2026-05-04.json"
        ),
        "wz_harness_smoke_schema": load(
            "outputs/yt_pr230_wz_harness_smoke_schema_gate_2026-05-05.json"
        ),
        "wz_smoke_to_production_promotion_no_go": load(
            "outputs/yt_pr230_wz_smoke_to_production_promotion_no_go_2026-05-05.json"
        ),
        "wz_same_source_ew_action_certificate_builder": load(
            "outputs/yt_wz_same_source_ew_action_certificate_builder_2026-05-04.json"
        ),
        "wz_same_source_ew_action_gate": load(
            "outputs/yt_wz_same_source_ew_action_gate_2026-05-04.json"
        ),
        "wz_same_source_ew_action_semantic_firewall": load(
            "outputs/yt_wz_same_source_ew_action_semantic_firewall_2026-05-04.json"
        ),
        "wz_source_coordinate_transport_no_go": load(
            "outputs/yt_wz_source_coordinate_transport_no_go_2026-05-05.json"
        ),
        "wz_goldstone_equivalence_source_identity_no_go": load(
            "outputs/yt_wz_goldstone_equivalence_source_identity_no_go_2026-05-05.json"
        ),
        "same_source_w_response_decomposition": load(
            "outputs/yt_same_source_w_response_decomposition_theorem_2026-05-04.json"
        ),
        "same_source_w_response_orthogonal_correction": load(
            "outputs/yt_same_source_w_response_orthogonal_correction_gate_2026-05-04.json"
        ),
        "one_higgs_completeness_orthogonal_null": load(
            "outputs/yt_one_higgs_completeness_orthogonal_null_gate_2026-05-04.json"
        ),
        "delta_perp_tomography_correction_builder": load(
            "outputs/yt_delta_perp_tomography_correction_builder_2026-05-04.json"
        ),
        "same_source_top_response_identity_builder": load(
            "outputs/yt_same_source_top_response_identity_certificate_builder_2026-05-04.json"
        ),
        "top_wz_matched_covariance_builder": load(
            "outputs/yt_top_wz_matched_covariance_certificate_builder_2026-05-04.json"
        ),
        "top_wz_covariance_marginal_derivation_no_go": load(
            "outputs/yt_top_wz_covariance_marginal_derivation_no_go_2026-05-05.json"
        ),
        "top_wz_factorization_independence_gate": load(
            "outputs/yt_top_wz_factorization_independence_gate_2026-05-05.json"
        ),
        "top_wz_deterministic_response_covariance_gate": load(
            "outputs/yt_top_wz_deterministic_response_covariance_gate_2026-05-05.json"
        ),
        "top_wz_covariance_theorem_import_audit": load(
            "outputs/yt_top_wz_covariance_theorem_import_audit_2026-05-05.json"
        ),
        "same_source_top_response_builder": load(
            "outputs/yt_same_source_top_response_certificate_builder_2026-05-04.json"
        ),
        "same_source_w_response_row_builder": load(
            "outputs/yt_same_source_w_response_row_builder_2026-05-04.json"
        ),
        "same_source_w_response_lightweight_readout": load(
            "outputs/yt_same_source_w_response_lightweight_readout_harness_2026-05-04.json"
        ),
        "wz_mass_fit_response_row_builder": load(
            "outputs/yt_wz_mass_fit_response_row_builder_2026-05-04.json"
        ),
        "electroweak_g2_certificate_builder": load(
            "outputs/yt_electroweak_g2_certificate_builder_2026-05-05.json"
        ),
        "wz_g2_generator_casimir_normalization_no_go": load(
            "outputs/yt_wz_g2_generator_casimir_normalization_no_go_2026-05-05.json"
        ),
        "wz_g2_authority_firewall": load(
            "outputs/yt_wz_g2_authority_firewall_2026-05-05.json"
        ),
        "wz_g2_response_self_normalization_no_go": load(
            "outputs/yt_wz_g2_response_self_normalization_no_go_2026-05-05.json"
        ),
        "pr230_wz_g2_bare_running_bridge_attempt": load(
            "outputs/yt_pr230_wz_g2_bare_running_bridge_attempt_2026-05-05.json"
        ),
        "wz_correlator_mass_fit_path_gate": load(
            "outputs/yt_wz_correlator_mass_fit_path_gate_2026-05-04.json"
        ),
        "same_source_sector_overlap_identity": load(
            "outputs/yt_same_source_sector_overlap_identity_obstruction_2026-05-02.json"
        ),
        "source_pole_canonical_higgs_mixing": load(
            "outputs/yt_source_pole_canonical_higgs_mixing_obstruction_2026-05-02.json"
        ),
        "osp_oh_identity_stretch": load(
            "outputs/yt_osp_oh_identity_stretch_attempt_2026-05-03.json"
        ),
        "source_pole_purity_cross_correlator": load(
            "outputs/yt_source_pole_purity_cross_correlator_gate_2026-05-02.json"
        ),
        "source_higgs_cross_correlator_manifest": load(
            "outputs/yt_source_higgs_cross_correlator_manifest_2026-05-02.json"
        ),
        "source_higgs_cross_correlator_import": load(
            "outputs/yt_source_higgs_cross_correlator_import_audit_2026-05-02.json"
        ),
        "source_higgs_gram_purity_gate": load(
            "outputs/yt_source_higgs_gram_purity_gate_2026-05-02.json"
        ),
        "source_higgs_cross_correlator_harness_extension": load(
            "outputs/yt_source_higgs_cross_correlator_harness_extension_2026-05-03.json"
        ),
        "source_higgs_pole_residue_extractor": load(
            "outputs/yt_source_higgs_pole_residue_extractor_2026-05-03.json"
        ),
        "source_higgs_cross_correlator_certificate_builder": load(
            "outputs/yt_source_higgs_cross_correlator_certificate_builder_2026-05-03.json"
        ),
        "source_higgs_gram_purity_postprocessor": load(
            "outputs/yt_source_higgs_gram_purity_postprocess_2026-05-03.json"
        ),
        "source_higgs_gram_purity_contract_witness": load(
            "outputs/yt_source_higgs_gram_purity_contract_witness_2026-05-03.json"
        ),
        "source_higgs_production_readiness_gate": load(
            "outputs/yt_source_higgs_production_readiness_gate_2026-05-04.json"
        ),
        "full_positive_closure_assembly_gate": load(
            "outputs/yt_pr230_full_positive_closure_assembly_gate_2026-05-04.json"
        ),
        "canonical_higgs_operator_candidate_stress": load(
            "outputs/yt_canonical_higgs_operator_candidate_stress_2026-05-03.json"
        ),
        "canonical_higgs_operator_certificate_gate": load(
            "outputs/yt_canonical_higgs_operator_certificate_gate_2026-05-03.json"
        ),
        "canonical_higgs_operator_semantic_firewall": load(
            "outputs/yt_canonical_higgs_operator_semantic_firewall_2026-05-04.json"
        ),
        "canonical_higgs_operator_realization_gate": load(
            "outputs/yt_canonical_higgs_operator_realization_gate_2026-05-02.json"
        ),
        "canonical_higgs_repo_authority_audit": load(
            "outputs/yt_canonical_higgs_repo_authority_audit_2026-05-03.json"
        ),
        "cross_lane_oh_authority_audit": load(
            "outputs/yt_cross_lane_oh_authority_audit_2026-05-05.json"
        ),
        "canonical_oh_premise_stretch": load(
            "outputs/yt_canonical_oh_premise_stretch_no_go_2026-05-05.json"
        ),
        "pr230_clean_source_higgs_math_tool_route_selector": load(
            "outputs/yt_pr230_clean_source_higgs_math_tool_route_selector_2026-05-05.json"
        ),
        "pr230_fresh_artifact_literature_route_review": load(
            "outputs/yt_pr230_fresh_artifact_literature_route_review_2026-05-05.json"
        ),
        "pr230_action_first_oh_artifact_attempt": load(
            "outputs/yt_pr230_action_first_oh_artifact_attempt_2026-05-05.json"
        ),
        "pr230_holonomic_source_response_feasibility_gate": load(
            "outputs/yt_pr230_holonomic_source_response_feasibility_gate_2026-05-05.json"
        ),
        "pr230_oh_source_higgs_authority_rescan_gate": load(
            "outputs/yt_pr230_oh_source_higgs_authority_rescan_gate_2026-05-05.json"
        ),
        "pr230_minimal_axioms_yukawa_summary_firewall": load(
            "outputs/yt_pr230_minimal_axioms_yukawa_summary_firewall_2026-05-05.json"
        ),
        "pr230_genuine_source_pole_artifact_intake": load(
            "outputs/yt_pr230_genuine_source_pole_artifact_intake_2026-05-06.json"
        ),
        "pr230_l12_chunk_compute_status": load(
            "outputs/yt_pr230_l12_chunk_compute_status_2026-05-06.json"
        ),
        "pr230_negative_route_applicability_review": load(
            "outputs/yt_pr230_negative_route_applicability_review_2026-05-06.json"
        ),
        "pr230_taste_condensate_oh_bridge_audit": load(
            "outputs/yt_pr230_taste_condensate_oh_bridge_audit_2026-05-06.json"
        ),
        "pr230_source_coordinate_transport_gate": load(
            "outputs/yt_pr230_source_coordinate_transport_gate_2026-05-06.json"
        ),
        "pr230_origin_main_composite_higgs_intake_guard": load(
            "outputs/yt_pr230_origin_main_composite_higgs_intake_guard_2026-05-06.json"
        ),
        "pr230_origin_main_ew_m_residual_intake_guard": load(
            "outputs/yt_pr230_origin_main_ew_m_residual_intake_guard_2026-05-06.json"
        ),
        "pr230_same_surface_z3_taste_triplet": load(
            "outputs/yt_pr230_same_surface_z3_taste_triplet_artifact_2026-05-06.json"
        ),
        "pr230_z3_triplet_conditional_primitive_cone": load(
            "outputs/yt_pr230_z3_triplet_conditional_primitive_cone_theorem_2026-05-06.json"
        ),
        "pr230_z3_triplet_positive_cone_support_certificate": load(
            "outputs/yt_pr230_z3_triplet_positive_cone_support_certificate_2026-05-06.json"
        ),
        "pr230_z3_generation_action_lift_attempt": load(
            "outputs/yt_pr230_z3_generation_action_lift_attempt_2026-05-06.json"
        ),
        "pr230_z3_lazy_transfer_promotion_attempt": load(
            "outputs/yt_pr230_z3_lazy_transfer_promotion_attempt_2026-05-06.json"
        ),
        "pr230_z3_lazy_selector_no_go": load(
            "outputs/yt_pr230_z3_lazy_selector_no_go_2026-05-06.json"
        ),
        "pr230_source_coordinate_transport_completion": load(
            "outputs/yt_pr230_source_coordinate_transport_completion_attempt_2026-05-06.json"
        ),
        "pr230_two_source_taste_radial_chart": load(
            "outputs/yt_pr230_two_source_taste_radial_chart_certificate_2026-05-06.json"
        ),
        "pr230_two_source_taste_radial_action": load(
            "outputs/yt_pr230_two_source_taste_radial_action_certificate_2026-05-06.json"
        ),
        "pr230_two_source_taste_radial_row_contract": load(
            "outputs/yt_pr230_two_source_taste_radial_row_contract_2026-05-06.json"
        ),
        "pr230_two_source_taste_radial_row_production_manifest": load(
            "outputs/yt_pr230_two_source_taste_radial_row_production_manifest_2026-05-06.json"
        ),
        "pr230_two_source_taste_radial_row_combiner_gate": load(
            "outputs/yt_pr230_two_source_taste_radial_row_combiner_gate_2026-05-06.json"
        ),
        "pr230_two_source_taste_radial_schur_subblock_witness": load(
            "outputs/yt_pr230_two_source_taste_radial_schur_subblock_witness_2026-05-06.json"
        ),
        "pr230_two_source_taste_radial_schur_kprime_finite_shell_scout": load(
            "outputs/yt_pr230_two_source_taste_radial_schur_kprime_finite_shell_scout_2026-05-06.json"
        ),
        "pr230_two_source_taste_radial_schur_abc_finite_rows": load(
            "outputs/yt_pr230_two_source_taste_radial_schur_abc_finite_rows_2026-05-06.json"
        ),
        "pr230_two_source_taste_radial_schur_pole_lift_gate": load(
            "outputs/yt_pr230_two_source_taste_radial_schur_pole_lift_gate_2026-05-06.json"
        ),
        "pr230_two_source_taste_radial_primitive_transfer_candidate_gate": load(
            "outputs/yt_pr230_two_source_taste_radial_primitive_transfer_candidate_gate_2026-05-07.json"
        ),
        "pr230_orthogonal_top_coupling_exclusion_candidate_gate": load(
            "outputs/yt_pr230_orthogonal_top_coupling_exclusion_candidate_gate_2026-05-07.json"
        ),
        "pr230_strict_scalar_lsz_moment_fv_authority_gate": load(
            "outputs/yt_pr230_strict_scalar_lsz_moment_fv_authority_gate_2026-05-07.json"
        ),
        "pr230_schur_complement_stieltjes_repair_gate": load(
            "outputs/yt_pr230_schur_complement_stieltjes_repair_gate_2026-05-07.json"
        ),
        "pr230_schur_complement_complete_monotonicity_gate": load(
            "outputs/yt_pr230_schur_complement_complete_monotonicity_gate_2026-05-07.json"
        ),
        "pr230_schur_x_given_source_one_pole_scout": load(
            "outputs/yt_pr230_schur_x_given_source_one_pole_scout_2026-05-07.json"
        ),
        "pr230_two_source_taste_radial_chunk_package": load(
            "outputs/yt_pr230_two_source_taste_radial_chunk_package_audit_2026-05-06.json"
        ),
        "pr230_source_higgs_pole_row_acceptance_contract": load(
            "outputs/yt_pr230_source_higgs_pole_row_acceptance_contract_2026-05-06.json"
        ),
        "pr230_two_source_taste_radial_chunk001_checkpoint": load(
            "outputs/yt_pr230_two_source_taste_radial_chunk001_checkpoint_2026-05-06.json"
        ),
        "pr230_two_source_taste_radial_chunk002_checkpoint": load(
            "outputs/yt_pr230_two_source_taste_radial_chunk002_checkpoint_2026-05-06.json"
        ),
        "pr230_two_source_taste_radial_chunk003_checkpoint": load(
            "outputs/yt_pr230_two_source_taste_radial_chunk003_checkpoint_2026-05-06.json"
        ),
        "pr230_two_source_taste_radial_chunk004_checkpoint": load(
            "outputs/yt_pr230_two_source_taste_radial_chunk004_checkpoint_2026-05-06.json"
        ),
        "pr230_two_source_taste_radial_chunk005_checkpoint": load(
            "outputs/yt_pr230_two_source_taste_radial_chunk005_checkpoint_2026-05-06.json"
        ),
        "pr230_two_source_taste_radial_chunk006_checkpoint": load(
            "outputs/yt_pr230_two_source_taste_radial_chunk006_checkpoint_2026-05-06.json"
        ),
        "pr230_two_source_taste_radial_chunk007_checkpoint": load(
            "outputs/yt_pr230_two_source_taste_radial_chunk007_checkpoint_2026-05-06.json"
        ),
        "pr230_two_source_taste_radial_chunk008_checkpoint": load(
            "outputs/yt_pr230_two_source_taste_radial_chunk008_checkpoint_2026-05-06.json"
        ),
        "pr230_two_source_taste_radial_chunk009_checkpoint": load(
            "outputs/yt_pr230_two_source_taste_radial_chunk009_checkpoint_2026-05-06.json"
        ),
        "pr230_two_source_taste_radial_chunk010_checkpoint": load(
            "outputs/yt_pr230_two_source_taste_radial_chunk010_checkpoint_2026-05-06.json"
        ),
        "pr230_taste_radial_canonical_oh_selector_gate": load(
            "outputs/yt_pr230_taste_radial_canonical_oh_selector_gate_2026-05-06.json"
        ),
        "pr230_degree_one_higgs_action_premise_gate": load(
            "outputs/yt_pr230_degree_one_higgs_action_premise_gate_2026-05-06.json"
        ),
        "pr230_degree_one_radial_tangent_oh_theorem": load(
            "outputs/yt_pr230_degree_one_radial_tangent_oh_theorem_2026-05-07.json"
        ),
        "pr230_taste_radial_to_source_higgs_promotion_contract": load(
            "outputs/yt_pr230_taste_radial_to_source_higgs_promotion_contract_2026-05-07.json"
        ),
        "pr230_fms_post_degree_route_rescore": load(
            "outputs/yt_pr230_fms_post_degree_route_rescore_2026-05-06.json"
        ),
        "pr230_fms_composite_oh_conditional_theorem": load(
            "outputs/yt_pr230_fms_composite_oh_conditional_theorem_2026-05-06.json"
        ),
        "pr230_fms_oh_candidate_action_packet": load(
            "outputs/yt_pr230_fms_oh_candidate_action_packet_2026-05-07.json"
        ),
        "pr230_fms_source_overlap_readout_gate": load(
            "outputs/yt_pr230_fms_source_overlap_readout_gate_2026-05-07.json"
        ),
        "pr230_fms_action_adoption_minimal_cut": load(
            "outputs/yt_pr230_fms_action_adoption_minimal_cut_2026-05-07.json"
        ),
        "pr230_higgs_mass_source_action_bridge": load(
            "outputs/yt_pr230_higgs_mass_source_action_bridge_2026-05-06.json"
        ),
        "pr230_same_source_ew_higgs_action_ansatz_gate": load(
            "outputs/yt_pr230_same_source_ew_higgs_action_ansatz_gate_2026-05-06.json"
        ),
        "pr230_same_source_ew_action_adoption_attempt": load(
            "outputs/yt_pr230_same_source_ew_action_adoption_attempt_2026-05-06.json"
        ),
        "pr230_radial_spurion_sector_overlap_theorem": load(
            "outputs/yt_pr230_radial_spurion_sector_overlap_theorem_2026-05-06.json"
        ),
        "pr230_radial_spurion_action_contract": load(
            "outputs/yt_pr230_radial_spurion_action_contract_2026-05-06.json"
        ),
        "pr230_additive_source_radial_spurion_incompatibility": load(
            "outputs/yt_pr230_additive_source_radial_spurion_incompatibility_2026-05-07.json"
        ),
        "pr230_additive_top_subtraction_row_contract": load(
            "outputs/yt_pr230_additive_top_subtraction_row_contract_2026-05-07.json"
        ),
        "pr230_source_higgs_direct_pole_row_contract": load(
            "outputs/yt_pr230_source_higgs_direct_pole_row_contract_2026-05-07.json"
        ),
        "pr230_canonical_oh_hard_residual_equivalence_gate": load(
            "outputs/yt_pr230_canonical_oh_hard_residual_equivalence_gate_2026-05-07.json"
        ),
        "pr230_wz_response_ratio_identifiability_contract": load(
            "outputs/yt_pr230_wz_response_ratio_identifiability_contract_2026-05-07.json"
        ),
        "pr230_wz_same_source_action_minimal_certificate_cut": load(
            "outputs/yt_pr230_wz_same_source_action_minimal_certificate_cut_2026-05-07.json"
        ),
        "pr230_wz_accepted_action_response_root_checkpoint": load(
            "outputs/yt_pr230_wz_accepted_action_response_root_checkpoint_2026-05-07.json"
        ),
        "pr230_wz_physical_response_packet_intake_checkpoint": load(
            "outputs/yt_pr230_wz_physical_response_packet_intake_checkpoint_2026-05-07.json"
        ),
        "pr230_canonical_oh_wz_common_action_cut": load(
            "outputs/yt_pr230_canonical_oh_wz_common_action_cut_2026-05-07.json"
        ),
        "pr230_canonical_oh_accepted_action_stretch_attempt": load(
            "outputs/yt_pr230_canonical_oh_accepted_action_stretch_attempt_2026-05-07.json"
        ),
        "pr230_source_higgs_bridge_aperture_checkpoint": load(
            "outputs/yt_pr230_source_higgs_bridge_aperture_checkpoint_2026-05-07.json"
        ),
        "pr230_fresh_artifact_intake_checkpoint": load(
            "outputs/yt_pr230_fresh_artifact_intake_checkpoint_2026-05-07.json"
        ),
        "pr230_block23_remote_candidate_intake": load(
            "outputs/yt_pr230_block23_remote_candidate_intake_checkpoint_2026-05-11.json"
        ),
        "pr230_block24_queue_pivot_admission": load(
            "outputs/yt_pr230_block24_queue_pivot_admission_checkpoint_2026-05-11.json"
        ),
        "pr230_block25_post_block24_landed": load(
            "outputs/yt_pr230_block25_post_block24_landed_checkpoint_2026-05-11.json"
        ),
        "pr230_block26_post_block25_landed": load(
            "outputs/yt_pr230_block26_post_block25_landed_checkpoint_2026-05-11.json"
        ),
        "pr230_block27_post_block26_landed": load(
            "outputs/yt_pr230_block27_post_block26_landed_checkpoint_2026-05-11.json"
        ),
        "pr230_block28_degree_one_oh_support_intake": load(
            "outputs/yt_pr230_block28_degree_one_oh_support_intake_checkpoint_2026-05-11.json"
        ),
        "pr230_block29_post_block28_wz_pivot_admission": load(
            "outputs/yt_pr230_block29_post_block28_wz_pivot_admission_checkpoint_2026-05-11.json"
        ),
        "pr230_block30_full_approach_assumptions_elon_lit_math_bridge_review": load(
            "outputs/yt_pr230_block30_full_approach_assumptions_elon_lit_math_bridge_review_2026-05-11.json"
        ),
        "pr230_block35_post_block34_physical_bridge_admission": load(
            "outputs/yt_pr230_block35_post_block34_physical_bridge_admission_checkpoint_2026-05-11.json"
        ),
        "pr230_post_fms_source_overlap_necessity_gate": load(
            "outputs/yt_pr230_post_fms_source_overlap_necessity_gate_2026-05-06.json"
        ),
        "pr230_source_higgs_overlap_kappa_contract": load(
            "outputs/yt_pr230_source_higgs_overlap_kappa_contract_2026-05-06.json"
        ),
        "pr230_action_first_route_completion": load(
            "outputs/yt_pr230_action_first_route_completion_2026-05-06.json"
        ),
        "pr230_wz_response_route_completion": load(
            "outputs/yt_pr230_wz_response_route_completion_2026-05-06.json"
        ),
        "pr230_schur_route_completion": load(
            "outputs/yt_pr230_schur_route_completion_2026-05-06.json"
        ),
        "pr230_neutral_primitive_route_completion": load(
            "outputs/yt_pr230_neutral_primitive_route_completion_2026-05-06.json"
        ),
        "pr230_neutral_primitive_h3h4_aperture_checkpoint": load(
            "outputs/yt_pr230_neutral_primitive_h3h4_aperture_checkpoint_2026-05-07.json"
        ),
        "pr230_oh_bridge_candidate_portfolio": load(
            "outputs/yt_pr230_oh_bridge_first_principles_candidate_portfolio_2026-05-06.json"
        ),
        "pr230_same_surface_neutral_multiplicity_one_gate": load(
            "outputs/yt_pr230_same_surface_neutral_multiplicity_one_gate_2026-05-07.json"
        ),
        "pr230_os_transfer_kernel_artifact_gate": load(
            "outputs/yt_pr230_os_transfer_kernel_artifact_gate_2026-05-07.json"
        ),
        "pr230_source_higgs_time_kernel_harness_extension_gate": load(
            "outputs/yt_pr230_source_higgs_time_kernel_harness_extension_gate_2026-05-07.json"
        ),
        "pr230_source_higgs_time_kernel_gevp_contract": load(
            "outputs/yt_pr230_source_higgs_time_kernel_gevp_contract_2026-05-07.json"
        ),
        "pr230_source_higgs_time_kernel_production_manifest": load(
            "outputs/yt_pr230_source_higgs_time_kernel_production_manifest_2026-05-07.json"
        ),
        "pr230_fms_literature_source_overlap_intake": load(
            "outputs/yt_pr230_fms_literature_source_overlap_intake_2026-05-07.json"
        ),
        "pr230_schur_higher_shell_production_contract": load(
            "outputs/yt_pr230_schur_higher_shell_production_contract_2026-05-07.json"
        ),
        "pr230_derived_bridge_rank_one_closure_attempt": load(
            "outputs/yt_pr230_derived_bridge_rank_one_closure_attempt_2026-05-05.json"
        ),
        "pr230_source_sector_pattern_transfer_gate": load(
            "outputs/yt_pr230_source_sector_pattern_transfer_gate_2026-05-05.json"
        ),
        "pr230_det_positivity_bridge_intake_gate": load(
            "outputs/yt_pr230_det_positivity_bridge_intake_gate_2026-05-05.json"
        ),
        "pr230_reflection_det_primitive_upgrade_gate": load(
            "outputs/yt_pr230_reflection_det_primitive_upgrade_gate_2026-05-05.json"
        ),
        "pr230_invariant_ring_oh_certificate_attempt": load(
            "outputs/yt_pr230_invariant_ring_oh_certificate_attempt_2026-05-05.json"
        ),
        "pr230_gns_source_higgs_flat_extension_attempt": load(
            "outputs/yt_pr230_gns_source_higgs_flat_extension_attempt_2026-05-05.json"
        ),
        "sm_one_higgs_oh_import_boundary": load(
            "outputs/yt_sm_one_higgs_oh_import_boundary_2026-05-03.json"
        ),
        "hunit_canonical_higgs_operator_candidate_gate": load(
            "outputs/yt_hunit_canonical_higgs_operator_candidate_gate_2026-05-02.json"
        ),
        "source_higgs_harness_absence_guard": load(
            "outputs/yt_source_higgs_harness_absence_guard_2026-05-02.json"
        ),
        "source_higgs_unratified_operator_smoke": load(
            "outputs/yt_source_higgs_unratified_operator_smoke_checkpoint_2026-05-03.json"
        ),
        "source_higgs_unratified_gram_shortcut_no_go": load(
            "outputs/yt_source_higgs_unratified_gram_shortcut_no_go_2026-05-05.json"
        ),
        "neutral_scalar_rank_one_purity_gate": load(
            "outputs/yt_neutral_scalar_rank_one_purity_gate_2026-05-02.json"
        ),
        "neutral_scalar_commutant_rank_no_go": load(
            "outputs/yt_neutral_scalar_commutant_rank_no_go_2026-05-02.json"
        ),
        "neutral_scalar_dynamical_rank_one_closure": load(
            "outputs/yt_neutral_scalar_dynamical_rank_one_closure_attempt_2026-05-02.json"
        ),
        "orthogonal_neutral_decoupling_no_go": load(
            "outputs/yt_orthogonal_neutral_decoupling_no_go_2026-05-02.json"
        ),
        "fh_gauge_response_mixed_scalar": load(
            "outputs/yt_fh_gauge_response_mixed_scalar_obstruction_2026-05-02.json"
        ),
        "no_orthogonal_top_coupling_import": load(
            "outputs/yt_no_orthogonal_top_coupling_import_audit_2026-05-02.json"
        ),
        "no_orthogonal_top_coupling_selection_rule": load(
            "outputs/yt_no_orthogonal_top_coupling_selection_rule_no_go_2026-05-02.json"
        ),
        "d17_source_pole_identity_closure": load(
            "outputs/yt_d17_source_pole_identity_closure_attempt_2026-05-02.json"
        ),
        "source_overlap_sum_rule_no_go": load(
            "outputs/yt_source_overlap_sum_rule_no_go_2026-05-02.json"
        ),
        "short_distance_ope_lsz_no_go": load(
            "outputs/yt_short_distance_ope_lsz_no_go_2026-05-02.json"
        ),
        "effective_mass_plateau_residue_no_go": load(
            "outputs/yt_effective_mass_plateau_residue_no_go_2026-05-02.json"
        ),
        "finite_source_shift_derivative_no_go": load(
            "outputs/yt_finite_source_shift_derivative_no_go_2026-05-02.json"
        ),
        "fh_lsz_finite_source_linearity_gate": load(
            "outputs/yt_fh_lsz_finite_source_linearity_gate_2026-05-02.json"
        ),
        "fh_lsz_finite_source_linearity_calibration": load(
            "outputs/yt_fh_lsz_finite_source_linearity_calibration_checkpoint_2026-05-03.json"
        ),
        "fh_lsz_target_observable_ess": load(
            "outputs/yt_fh_lsz_target_observable_ess_certificate_2026-05-03.json"
        ),
        "fh_lsz_autocorrelation_ess_gate": load(
            "outputs/yt_fh_lsz_autocorrelation_ess_gate_2026-05-02.json"
        ),
        "fh_lsz_response_window_forensics": load(
            "outputs/yt_fh_lsz_response_window_forensics_2026-05-03.json"
        ),
        "fh_lsz_common_window_response_provenance": load(
            "outputs/yt_fh_lsz_common_window_response_provenance_2026-05-04.json"
        ),
        "fh_lsz_common_window_pooled_response_estimator": load(
            "outputs/yt_fh_lsz_common_window_pooled_response_estimator_2026-05-04.json"
        ),
        "fh_lsz_common_window_replacement_response_stability": load(
            "outputs/yt_fh_lsz_common_window_replacement_response_stability_2026-05-04.json"
        ),
        "fh_lsz_common_window_response_gate": load(
            "outputs/yt_fh_lsz_common_window_response_gate_2026-05-04.json"
        ),
        "fh_lsz_v2_target_response_stability": load(
            "outputs/yt_fh_lsz_v2_target_response_stability_2026-05-04.json"
        ),
        "fh_lsz_response_window_acceptance_gate": load(
            "outputs/yt_fh_lsz_response_window_acceptance_gate_2026-05-03.json"
        ),
        "fh_lsz_legacy_v2_backfill_feasibility": load(
            "outputs/yt_fh_lsz_legacy_v2_backfill_feasibility_2026-05-04.json"
        ),
        "fh_lsz_target_timeseries_replacement_queue": load(
            "outputs/yt_fh_lsz_target_timeseries_replacement_queue_2026-05-02.json"
        ),
        "fh_lsz_target_timeseries_harness": load(
            "outputs/yt_fh_lsz_target_timeseries_harness_certificate_2026-05-02.json"
        ),
        "fh_lsz_multitau_target_timeseries_harness": load(
            "outputs/yt_fh_lsz_multitau_target_timeseries_harness_certificate_2026-05-03.json"
        ),
        "fh_lsz_selected_mass_normal_cache_speedup": load(
            "outputs/yt_fh_lsz_selected_mass_normal_cache_speedup_certificate_2026-05-03.json"
        ),
        "fh_lsz_global_production_collision_guard": load(
            "outputs/yt_fh_lsz_global_production_collision_guard_2026-05-04.json"
        ),
        "fh_lsz_target_timeseries_higgs_identity_no_go": load(
            "outputs/yt_fh_lsz_target_timeseries_higgs_identity_no_go_2026-05-02.json"
        ),
        "higgs_pole_identity_latest_blocker": load(
            "outputs/yt_higgs_pole_identity_latest_blocker_certificate_2026-05-02.json"
        ),
        "fh_lsz_pole_fit_mode_budget": load("outputs/yt_fh_lsz_pole_fit_mode_budget_2026-05-01.json"),
        "fh_lsz_eight_mode_noise_variance": load(
            "outputs/yt_fh_lsz_eight_mode_noise_variance_gate_2026-05-01.json"
        ),
        "fh_lsz_noise_subsample_diagnostics": load(
            "outputs/yt_fh_lsz_noise_subsample_diagnostics_certificate_2026-05-01.json"
        ),
        "fh_lsz_variance_calibration_manifest": load(
            "outputs/yt_fh_lsz_variance_calibration_manifest_2026-05-01.json"
        ),
        "fh_lsz_paired_variance_calibration_gate": load(
            "outputs/yt_fh_lsz_paired_variance_calibration_gate_2026-05-04.json"
        ),
        "fh_lsz_polefit8x8_chunk_manifest": load(
            "outputs/yt_fh_lsz_polefit8x8_chunk_manifest_2026-05-04.json"
        ),
        "fh_lsz_polefit8x8_chunk_combiner_gate": load(
            "outputs/yt_fh_lsz_polefit8x8_chunk_combiner_gate_2026-05-04.json"
        ),
        "fh_lsz_polefit8x8_postprocessor": load(
            "outputs/yt_fh_lsz_polefit8x8_postprocessor_2026-05-04.json"
        ),
        "fh_lsz_invariant_readout": load("outputs/yt_fh_lsz_invariant_readout_theorem_2026-05-01.json"),
        "scalar_pole_determinant_gate": load("outputs/yt_scalar_pole_determinant_gate_2026-05-01.json"),
        "scalar_ladder_eigen_derivative": load("outputs/yt_scalar_ladder_eigen_derivative_gate_2026-05-01.json"),
        "scalar_ladder_total_momentum_derivative": load("outputs/yt_scalar_ladder_total_momentum_derivative_scout_2026-05-01.json"),
        "scalar_ladder_derivative_limit": load("outputs/yt_scalar_ladder_derivative_limit_obstruction_2026-05-01.json"),
        "scalar_ladder_residue_envelope": load("outputs/yt_scalar_ladder_residue_envelope_obstruction_2026-05-01.json"),
        "scalar_kernel_ward_identity": load("outputs/yt_scalar_kernel_ward_identity_obstruction_2026-05-01.json"),
        "scalar_zero_mode_limit_order": load("outputs/yt_scalar_zero_mode_limit_order_theorem_2026-05-01.json"),
        "zero_mode_prescription_import": load("outputs/yt_zero_mode_prescription_import_audit_2026-05-01.json"),
        "flat_toron_denominator": load("outputs/yt_flat_toron_scalar_denominator_obstruction_2026-05-01.json"),
        "flat_toron_washout": load("outputs/yt_flat_toron_thermodynamic_washout_2026-05-01.json"),
        "color_singlet_zero_mode": load("outputs/yt_color_singlet_zero_mode_cancellation_2026-05-01.json"),
        "color_singlet_finite_q_ir": load("outputs/yt_color_singlet_finite_q_ir_regular_2026-05-01.json"),
        "color_singlet_zero_mode_removed_ladder_pole_search": load(
            "outputs/yt_color_singlet_zero_mode_removed_ladder_pole_search_2026-05-01.json"
        ),
        "taste_corner_ladder_pole_obstruction": load(
            "outputs/yt_taste_corner_ladder_pole_obstruction_2026-05-01.json"
        ),
        "taste_carrier_import_audit": load("outputs/yt_taste_carrier_import_audit_2026-05-01.json"),
        "taste_singlet_ladder_normalization": load(
            "outputs/yt_taste_singlet_ladder_normalization_boundary_2026-05-01.json"
        ),
        "scalar_taste_projector_normalization_attempt": load(
            "outputs/yt_scalar_taste_projector_normalization_attempt_2026-05-01.json"
        ),
        "unit_projector_pole_threshold": load(
            "outputs/yt_unit_projector_pole_threshold_obstruction_2026-05-01.json"
        ),
        "scalar_kernel_enhancement_import": load(
            "outputs/yt_scalar_kernel_enhancement_import_audit_2026-05-01.json"
        ),
        "fitted_kernel_residue_selector": load(
            "outputs/yt_fitted_kernel_residue_selector_no_go_2026-05-01.json"
        ),
        "ladder_ir_zero_mode": load("outputs/yt_scalar_ladder_ir_zero_mode_obstruction_2026-05-01.json"),
        "heavy_kinetic": load("outputs/yt_heavy_kinetic_mass_route_2026-05-01.json"),
        "nonzero_momentum": load("outputs/yt_nonzero_momentum_correlator_scout_2026-05-01.json"),
        "momentum_harness": load("outputs/yt_momentum_harness_extension_certificate_2026-05-01.json"),
        "heavy_matching": load("outputs/yt_heavy_kinetic_matching_obstruction_2026-05-01.json"),
        "momentum_pilot": load("outputs/yt_momentum_pilot_scaling_certificate_2026-05-01.json"),
        "assumption_stress": load("outputs/yt_pr230_assumption_import_stress_2026-05-01.json"),
        "free_kinetic": load("outputs/yt_free_staggered_kinetic_coefficient_2026-05-01.json"),
        "interacting_kinetic": load("outputs/yt_interacting_kinetic_background_sensitivity_2026-05-01.json"),
        "direct_scale": load("outputs/yt_direct_measurement_scale_requirements_2026-05-01.json"),
        "retained_closure_route": load("outputs/yt_retained_closure_route_certificate_2026-05-01.json"),
        "negative_route_applicability_review": load(
            "outputs/yt_pr230_negative_route_applicability_review_2026-05-06.json"
        ),
    }
    for path in sorted((ROOT / "outputs").glob(GENERIC_CHUNK_TARGET_PATTERN)):
        certificates[generic_chunk_target_key(path)] = load(str(path.relative_to(ROOT)))
    for path in sorted((ROOT / "outputs").glob(MULTITAU_CHUNK_TARGET_PATTERN)):
        certificates[multitau_chunk_target_key(path)] = load(str(path.relative_to(ROOT)))

    all_present = all(isinstance(cert, dict) for cert in certificates.values())
    all_no_fail = all(int(cert.get("fail_count", 0)) == 0 for cert in certificates.values())
    proposal_allowed = [
        name for name, cert in certificates.items() if cert.get("proposal_allowed") is True
    ]
    statuses = {name: cert.get("actual_current_surface_status") for name, cert in certificates.items()}
    generic_chunk_target_statuses = {
        name: status
        for name, status in statuses.items()
        if name.startswith("fh_lsz_chunk") and name.endswith("_target_timeseries_generic")
    }
    multitau_chunk_target_statuses = {
        name: status
        for name, status in statuses.items()
        if name.startswith("fh_lsz_chunk") and name.endswith("_multitau_target_timeseries")
    }

    report("campaign-certificates-present", all_present, f"count={len(certificates)}")
    report("campaign-runners-have-no-fails", all_no_fail, "all loaded certificates have FAIL=0")
    report("no-retained-proposal-authorized", not proposal_allowed, f"proposal_allowed={proposal_allowed}")
    report(
        "negative-route-applicability-review-preserves-reopen",
        certificates["negative_route_applicability_review"].get("no_retained_negative_overclaim") is True
        and certificates["negative_route_applicability_review"].get("future_reopen_paths_preserved") is True
        and certificates["negative_route_applicability_review"].get("selected_negative_results_apply_on_current_surface") is True,
        statuses["negative_route_applicability_review"],
    )
    report(
        "direct-route-needs-scale-or-heavy-treatment",
        "scale requirement" in str(statuses["direct_scale"]),
        statuses["direct_scale"],
    )
    report(
        "hqet-route-needs-matching",
        "HQET" in str(statuses["hqet"]) or "route requirement" in str(statuses["hqet"]),
        statuses["hqet"],
    )
    report(
        "legendre-route-needs-residue",
        "Legendre" in str(statuses["legendre"]) or "normalization freedom" in str(statuses["legendre"]),
        statuses["legendre"],
    )
    report(
        "free-bubble-route-needs-interaction",
        "free source pole absence" in str(statuses["free_bubble"]),
        statuses["free_bubble"],
    )
    report(
        "same-1pi-route-needs-lsz",
        "same-1PI" in str(statuses["same_1pi"]),
        statuses["same_1pi"],
    )
    report(
        "lsz-normalization-cancellation-still-needs-kernel",
        "LSZ normalization cancellation" in str(statuses["lsz_norm"])
        or "conditional-support" in str(statuses["lsz_norm"]),
        statuses["lsz_norm"],
    )
    report(
        "feshbach-response-not-common-dressing",
        "Feshbach response boundary" in str(statuses["feshbach_response"])
        or "exact support" in str(statuses["feshbach_response"]),
        statuses["feshbach_response"],
    )
    report(
        "bridge-stack-not-pr230-closure",
        "bridge stack not PR230 closure" in str(statuses["bridge_stack"]),
        statuses["bridge_stack"],
    )
    report(
        "spectral-positivity-needs-saturation-theorem",
        "spectral saturation no-go" in str(statuses["spectral_saturation"]),
        statuses["spectral_saturation"],
    )
    report(
        "large-nc-pole-dominance-needs-finite-nc-bound",
        "large-Nc pole dominance" in str(statuses["large_nc"]),
        statuses["large_nc"],
    )
    report(
        "production-resource-projection-not-evidence",
        "production resource projection" in str(statuses["production_resource"]),
        statuses["production_resource"],
    )
    report(
        "feynman-hellmann-still-needs-source-normalization",
        "Feynman-Hellmann" in str(statuses["feynman_hellmann"])
        or "source-response" in str(statuses["feynman_hellmann"]),
        statuses["feynman_hellmann"],
    )
    report(
        "mass-response-bracket-is-bare-source-only",
        "mass-response" in str(statuses["mass_response"]),
        statuses["mass_response"],
    )
    report(
        "source-reparametrization-gauge-blocks-source-only-closure",
        "source reparametrization" in str(statuses["source_reparametrization"]),
        statuses["source_reparametrization"],
    )
    report(
        "canonical-scalar-normalization-not-hidden-proof",
        "canonical scalar normalization" in str(statuses["canonical_scalar_import"]),
        statuses["canonical_scalar_import"],
    )
    report(
        "source-to-higgs-lsz-closure-still-open",
        "source-to-Higgs" in str(statuses["source_to_higgs_lsz"])
        or "LSZ closure attempt" in str(statuses["source_to_higgs_lsz"]),
        statuses["source_to_higgs_lsz"],
    )
    report(
        "cl3-source-unit-does-not-fix-kappa",
        "Cl3 source-unit" in str(statuses["cl3_source_unit"])
        or "source-unit normalization no-go" in str(statuses["cl3_source_unit"]),
        statuses["cl3_source_unit"],
    )
    report(
        "gauge-vev-source-overlap-does-not-fix-kappa",
        "gauge-VEV source-overlap no-go" in str(statuses["gauge_vev_source_overlap"])
        or "exact negative boundary" in str(statuses["gauge_vev_source_overlap"]),
        statuses["gauge_vev_source_overlap"],
    )
    report(
        "canonical-kinetic-renormalization-does-not-fix-source-overlap",
        "renormalization-condition source-overlap no-go"
        in str(statuses["scalar_renormalization_condition_overlap"]),
        statuses["scalar_renormalization_condition_overlap"],
    )
    report(
        "source-contact-term-scheme-does-not-fix-pole-residue",
        "source contact-term scheme boundary" in str(statuses["scalar_source_contact_term_scheme"]),
        statuses["scalar_source_contact_term_scheme"],
    )
    report(
        "scalar-source-response-harness-needs-kappa",
        "scalar source response harness" in str(statuses["scalar_source_response_harness"])
        or "bounded-support" in str(statuses["scalar_source_response_harness"]),
        statuses["scalar_source_response_harness"],
    )
    report(
        "fh-production-protocol-needs-production-and-kappa",
        "Feynman-Hellmann production protocol" in str(statuses["fh_production_protocol"])
        or "bounded-support" in str(statuses["fh_production_protocol"]),
        statuses["fh_production_protocol"],
    )
    report(
        "same-source-scalar-two-point-needs-pole-and-continuum",
        "same-source scalar two-point" in str(statuses["same_source_scalar_two_point"])
        or "bounded-support" in str(statuses["same_source_scalar_two_point"]),
        statuses["same_source_scalar_two_point"],
    )
    report(
        "bs-kernel-residue-degeneracy-needs-denominator-theorem",
        "Bethe-Salpeter" in str(statuses["bs_kernel_residue_degeneracy"])
        or "pole-residue degeneracy" in str(statuses["bs_kernel_residue_degeneracy"]),
        statuses["bs_kernel_residue_degeneracy"],
    )
    report(
        "scalar-two-point-harness-needs-production-and-lsz",
        "scalar two-point production-harness" in str(statuses["scalar_two_point_harness"])
        or "bounded-support" in str(statuses["scalar_two_point_harness"]),
        statuses["scalar_two_point_harness"],
    )
    report(
        "fh-lsz-joint-harness-needs-production-and-kappa",
        "Feynman-Hellmann scalar-LSZ" in str(statuses["fh_lsz_joint_harness"])
        or "bounded-support" in str(statuses["fh_lsz_joint_harness"]),
        statuses["fh_lsz_joint_harness"],
    )
    report(
        "fh-lsz-joint-resource-projection-not-evidence",
        "resource projection" in str(statuses["fh_lsz_joint_resource"])
        or "bounded-support" in str(statuses["fh_lsz_joint_resource"]),
        statuses["fh_lsz_joint_resource"],
    )
    report(
        "fh-lsz-production-manifest-not-evidence",
        "production manifest" in str(statuses["fh_lsz_production_manifest"])
        or "bounded-support" in str(statuses["fh_lsz_production_manifest"]),
        statuses["fh_lsz_production_manifest"],
    )
    report(
        "fh-lsz-production-postprocess-gate-blocks-closure",
        certificates["fh_lsz_production_postprocess_gate"].get("proposal_allowed") is False
        and certificates["fh_lsz_production_postprocess_gate"].get("retained_proposal_gate_ready")
        is False
        and any(
            row.get("satisfied_now") is False
            for row in certificates["fh_lsz_production_postprocess_gate"].get(
                "postprocess_requirements", []
            )
            if isinstance(row, dict)
        ),
        statuses["fh_lsz_production_postprocess_gate"],
    )
    report(
        "fh-lsz-production-checkpoint-granularity-not-foreground-safe",
        "checkpoint granularity gate" in str(statuses["fh_lsz_production_checkpoint_granularity"])
        or "open" in str(statuses["fh_lsz_production_checkpoint_granularity"]),
        statuses["fh_lsz_production_checkpoint_granularity"],
    )
    report(
        "fh-lsz-chunked-production-manifest-not-evidence",
        "chunked production manifest" in str(statuses["fh_lsz_chunked_production_manifest"])
        or "bounded-support" in str(statuses["fh_lsz_chunked_production_manifest"]),
        statuses["fh_lsz_chunked_production_manifest"],
    )
    report(
        "fh-lsz-chunk-combiner-gate-not-evidence",
        "chunk combiner gate" in str(statuses["fh_lsz_chunk_combiner_gate"])
        or "complete L12 chunk summary" in str(statuses["fh_lsz_chunk_combiner_gate"])
        or "open" in str(statuses["fh_lsz_chunk_combiner_gate"]),
        statuses["fh_lsz_chunk_combiner_gate"],
    )
    report(
        "fh-lsz-chunk001-checkpoint-not-closure",
        "chunk001" in str(statuses["fh_lsz_chunk001_checkpoint"])
        and "production checkpoint" in str(statuses["fh_lsz_chunk001_checkpoint"]),
        statuses["fh_lsz_chunk001_checkpoint"],
    )
    report(
        "fh-lsz-chunk002-checkpoint-not-closure",
        "chunk002" in str(statuses["fh_lsz_chunk002_checkpoint"])
        and "production checkpoint" in str(statuses["fh_lsz_chunk002_checkpoint"]),
        statuses["fh_lsz_chunk002_checkpoint"],
    )
    report(
        "fh-lsz-ready-chunk-set-checkpoint-not-closure",
        "ready chunk-set production checkpoint" in str(statuses["fh_lsz_ready_chunk_set_checkpoint"])
        or "complete L12 ready chunk-set checkpoint"
        in str(statuses["fh_lsz_ready_chunk_set_checkpoint"]),
        statuses["fh_lsz_ready_chunk_set_checkpoint"],
    )
    report(
        "fh-lsz-ready-chunk-response-stability-not-closure",
        "ready chunk response-stability diagnostic" in str(statuses["fh_lsz_ready_chunk_response_stability"]),
        statuses["fh_lsz_ready_chunk_response_stability"],
    )
    report(
        "fh-lsz-chunk011-target-timeseries-not-closure",
        "chunk011 target-timeseries production checkpoint"
        in str(statuses["fh_lsz_chunk011_target_timeseries"]),
        statuses["fh_lsz_chunk011_target_timeseries"],
    )
    report(
        "fh-lsz-generic-chunk-target-timeseries-not-closure",
        "chunk011 generic target-timeseries checkpoint"
        in str(statuses["fh_lsz_chunk011_target_timeseries_generic"]),
        statuses["fh_lsz_chunk011_target_timeseries_generic"],
    )
    report(
        "fh-lsz-chunk012-target-timeseries-not-closure",
        "chunk012 generic target-timeseries checkpoint"
        in str(statuses["fh_lsz_chunk012_target_timeseries_generic"]),
        statuses["fh_lsz_chunk012_target_timeseries_generic"],
    )
    report(
        "fh-lsz-generic-chunk-target-checkpoints-discovered",
        bool(generic_chunk_target_statuses)
        and all(
            "generic target-timeseries checkpoint" in str(status)
            for status in generic_chunk_target_statuses.values()
        ),
        f"count={len(generic_chunk_target_statuses)}",
    )
    report(
        "fh-lsz-v2-multitau-chunk-target-checkpoints-discovered",
        bool(multitau_chunk_target_statuses)
        and all(
            "v2 multi-tau target-timeseries checkpoint" in str(status)
            for status in multitau_chunk_target_statuses.values()
        ),
        f"count={len(multitau_chunk_target_statuses)}",
    )
    report(
        "fh-lsz-legacy-v2-backfill-boundary",
        "legacy chunks001-016 cannot be honestly v2-backfilled"
        in str(statuses["fh_lsz_legacy_v2_backfill_feasibility"]),
        statuses["fh_lsz_legacy_v2_backfill_feasibility"],
    )
    report(
        "fh-lsz-pole-fit-kinematics-not-closure",
        "scalar-pole kinematics gate" in str(statuses["fh_lsz_pole_fit_kinematics"])
        or "open" in str(statuses["fh_lsz_pole_fit_kinematics"]),
        statuses["fh_lsz_pole_fit_kinematics"],
    )
    report(
        "fh-lsz-pole-fit-postprocessor-not-evidence",
        "pole fit postprocessor scaffold" in str(statuses["fh_lsz_pole_fit_postprocessor"])
        or "bounded-support" in str(statuses["fh_lsz_pole_fit_postprocessor"]),
        statuses["fh_lsz_pole_fit_postprocessor"],
    )
    report(
        "fh-lsz-finite-shell-pole-fit-not-identified",
        "finite-shell pole-fit identifiability no-go"
        in str(statuses["fh_lsz_finite_shell_identifiability"]),
        statuses["fh_lsz_finite_shell_identifiability"],
    )
    report(
        "fh-lsz-pole-fit-model-class-gate-blocks",
        "model-class gate blocks finite-shell fit"
        in str(statuses["fh_lsz_pole_fit_model_class_gate"]),
        statuses["fh_lsz_pole_fit_model_class_gate"],
    )
    report(
        "fh-lsz-model-class-semantic-firewall-not-closure",
        "model-class semantic firewall passed"
        in str(statuses["fh_lsz_model_class_semantic_firewall"])
        and certificates["fh_lsz_model_class_semantic_firewall"].get("proposal_allowed") is False,
        statuses["fh_lsz_model_class_semantic_firewall"],
    )
    report(
        "fh-lsz-stieltjes-model-class-not-enough",
        "Stieltjes model-class obstruction" in str(statuses["fh_lsz_stieltjes_model_class"]),
        statuses["fh_lsz_stieltjes_model_class"],
    )
    report(
        "fh-lsz-stieltjes-moment-certificate-gate-absent",
        "Stieltjes moment-certificate gate"
        in str(statuses["fh_lsz_stieltjes_moment_certificate_gate"])
        and certificates["fh_lsz_stieltjes_moment_certificate_gate"].get("proposal_allowed")
        is False
        and certificates["fh_lsz_stieltjes_moment_certificate_gate"].get(
            "moment_certificate_gate_passed"
        )
        is False,
        statuses["fh_lsz_stieltjes_moment_certificate_gate"],
    )
    report(
        "fh-lsz-pade-stieltjes-bounds-gate-absent",
        "Pade-Stieltjes bounds gate"
        in str(statuses["fh_lsz_pade_stieltjes_bounds_gate"])
        and certificates["fh_lsz_pade_stieltjes_bounds_gate"].get("proposal_allowed")
        is False
        and certificates["fh_lsz_pade_stieltjes_bounds_gate"].get(
            "pade_stieltjes_bounds_gate_passed"
        )
        is False,
        statuses["fh_lsz_pade_stieltjes_bounds_gate"],
    )
    report(
        "fh-lsz-polefit8x8-stieltjes-proxy-diagnostic-blocks-current-proxy",
        "Stieltjes monotonicity"
        in str(statuses["fh_lsz_polefit8x8_stieltjes_proxy_diagnostic"])
        and certificates["fh_lsz_polefit8x8_stieltjes_proxy_diagnostic"].get(
            "proposal_allowed"
        )
        is False
        and certificates["fh_lsz_polefit8x8_stieltjes_proxy_diagnostic"].get(
            "stieltjes_proxy_certificate_passed"
        )
        is False,
        statuses["fh_lsz_polefit8x8_stieltjes_proxy_diagnostic"],
    )
    report(
        "fh-lsz-complete-bernstein-inverse-diagnostic-blocks-current-denominator",
        "complete-Bernstein monotonicity"
        in str(statuses["fh_lsz_complete_bernstein_inverse_diagnostic"])
        and certificates["fh_lsz_complete_bernstein_inverse_diagnostic"].get(
            "proposal_allowed"
        )
        is False
        and certificates["fh_lsz_complete_bernstein_inverse_diagnostic"].get(
            "complete_bernstein_inverse_certificate_passed"
        )
        is False,
        statuses["fh_lsz_complete_bernstein_inverse_diagnostic"],
    )
    report(
        "pr230-scalar-lsz-holonomic-exact-authority-attempt-blocks-current-finite-shell",
        "scalar-LSZ holonomic exact-authority not derivable"
        in str(statuses["pr230_scalar_lsz_holonomic_exact_authority_attempt"])
        and certificates["pr230_scalar_lsz_holonomic_exact_authority_attempt"].get(
            "proposal_allowed"
        )
        is False
        and certificates["pr230_scalar_lsz_holonomic_exact_authority_attempt"].get(
            "holonomic_exact_authority_passed"
        )
        is False
        and certificates["pr230_scalar_lsz_holonomic_exact_authority_attempt"].get(
            "counterfamily", {}
        ).get("same_finite_shell_values")
        is True
        and certificates["pr230_scalar_lsz_holonomic_exact_authority_attempt"].get(
            "counterfamily", {}
        ).get("residues_differ")
        is True,
        statuses["pr230_scalar_lsz_holonomic_exact_authority_attempt"],
    )
    report(
        "pr230-scalar-lsz-carleman-tauberian-determinacy-attempt-blocks-current-finite-prefix",
        "Carleman/Tauberian scalar-LSZ determinacy not derivable"
        in str(statuses["pr230_scalar_lsz_carleman_tauberian_determinacy_attempt"])
        and certificates[
            "pr230_scalar_lsz_carleman_tauberian_determinacy_attempt"
        ].get("proposal_allowed")
        is False
        and certificates[
            "pr230_scalar_lsz_carleman_tauberian_determinacy_attempt"
        ].get("carleman_tauberian_determinacy_passed")
        is False
        and certificates[
            "pr230_scalar_lsz_carleman_tauberian_determinacy_attempt"
        ].get("finite_prefix_stieltjes_counterfamily_passed")
        is True,
        statuses["pr230_scalar_lsz_carleman_tauberian_determinacy_attempt"],
    )
    report(
        "fh-lsz-contact-subtraction-identifiability-blocks-arbitrary-subtraction",
        "contact-subtraction identifiability obstruction"
        in str(statuses["fh_lsz_contact_subtraction_identifiability"])
        and certificates["fh_lsz_contact_subtraction_identifiability"].get(
            "proposal_allowed"
        )
        is False
        and certificates["fh_lsz_contact_subtraction_identifiability"].get(
            "contact_subtraction_identifiability_obstruction_passed"
        )
        is True
        and certificates["fh_lsz_contact_subtraction_identifiability"].get(
            "contact_subtraction_certificate_present"
        )
        is False,
        statuses["fh_lsz_contact_subtraction_identifiability"],
    )
    report(
        "fh-lsz-affine-contact-complete-monotonicity-blocks",
        "affine contact complete-monotonicity no-go"
        in str(statuses["fh_lsz_affine_contact_complete_monotonicity"])
        and certificates["fh_lsz_affine_contact_complete_monotonicity"].get(
            "proposal_allowed"
        )
        is False
        and certificates["fh_lsz_affine_contact_complete_monotonicity"].get(
            "affine_contact_complete_monotonicity_no_go_passed"
        )
        is True
        and certificates["fh_lsz_affine_contact_complete_monotonicity"].get(
            "affine_contact_stieltjes_certificate_passed"
        )
        is False,
        statuses["fh_lsz_affine_contact_complete_monotonicity"],
    )
    report(
        "fh-lsz-polynomial-contact-finite-shell-blocks",
        "finite-shell polynomial contact non-identifiability no-go"
        in str(statuses["fh_lsz_polynomial_contact_finite_shell"])
        and certificates["fh_lsz_polynomial_contact_finite_shell"].get(
            "proposal_allowed"
        )
        is False
        and certificates["fh_lsz_polynomial_contact_finite_shell"].get(
            "polynomial_contact_finite_shell_no_go_passed"
        )
        is True
        and certificates["fh_lsz_polynomial_contact_finite_shell"].get(
            "stieltjes_certificate_from_polynomial_contact_passed"
        )
        is False,
        statuses["fh_lsz_polynomial_contact_finite_shell"],
    )
    report(
        "fh-lsz-polynomial-contact-repair-no-go-blocks",
        "polynomial contact repair not scalar-LSZ authority"
        in str(statuses["fh_lsz_polynomial_contact_repair"])
        and certificates["fh_lsz_polynomial_contact_repair"].get("proposal_allowed")
        is False
        and certificates["fh_lsz_polynomial_contact_repair"].get(
            "polynomial_contact_repair_no_go_passed"
        )
        is True
        and certificates["fh_lsz_polynomial_contact_repair"].get(
            "stieltjes_certificate_from_polynomial_contact_passed"
        )
        is False,
        statuses["fh_lsz_polynomial_contact_repair"],
    )
    report(
        "nonchunk-route-family-import-audit-complete",
        "non-chunk route-family import audit"
        in str(statuses["pr230_nonchunk_route_family_import_audit"])
        and certificates["pr230_nonchunk_route_family_import_audit"].get(
            "proposal_allowed"
        )
        is False
        and certificates["pr230_nonchunk_route_family_import_audit"]
        .get("selected_route", {})
        .get("id")
        == "no_current_surface_nonchunk_route"
        and certificates["pr230_nonchunk_route_family_import_audit"]
        .get("ranked_future_route", {})
        .get("id")
        == "same_source_wz_response",
        statuses["pr230_nonchunk_route_family_import_audit"],
    )
    report(
        "fh-lsz-pole-saturation-threshold-gate-blocks",
        "pole-saturation threshold gate" in str(statuses["fh_lsz_pole_saturation_threshold_gate"]),
        statuses["fh_lsz_pole_saturation_threshold_gate"],
    )
    report(
        "fh-lsz-threshold-authority-audit-blocks-hidden-import",
        "threshold-authority import audit" in str(statuses["fh_lsz_threshold_authority_audit"]),
        statuses["fh_lsz_threshold_authority_audit"],
    )
    report(
        "confinement-gap-threshold-import-blocks",
        "confinement gap not scalar LSZ threshold"
        in str(statuses["confinement_gap_threshold_import"]),
        statuses["confinement_gap_threshold_import"],
    )
    report(
        "fh-lsz-finite-volume-pole-saturation-blocks",
        "finite-volume pole-saturation obstruction" in str(statuses["fh_lsz_finite_volume_pole_saturation"]),
        statuses["fh_lsz_finite_volume_pole_saturation"],
    )
    report(
        "fh-lsz-numba-seed-independence-blocks-historical-chunks",
        "numba seed-independence audit" in str(statuses["fh_lsz_numba_seed_independence"]),
        statuses["fh_lsz_numba_seed_independence"],
    )
    report(
        "fh-lsz-uniform-gap-self-certification-blocks",
        "uniform-gap self-certification no-go" in str(statuses["fh_lsz_uniform_gap_self_certification"]),
        statuses["fh_lsz_uniform_gap_self_certification"],
    )
    report(
        "scalar-denominator-theorem-closure-attempt-blocked",
        "scalar denominator theorem closure attempt blocked" in str(statuses["scalar_denominator_theorem_closure"]),
        statuses["scalar_denominator_theorem_closure"],
    )
    report(
        "fh-lsz-soft-continuum-threshold-no-go-blocks-ir-shortcut",
        "soft-continuum threshold no-go" in str(statuses["fh_lsz_soft_continuum_threshold"]),
        statuses["fh_lsz_soft_continuum_threshold"],
    )
    report(
        "reflection-positivity-not-scalar-lsz-closure",
        "reflection positivity not scalar LSZ closure"
        in str(statuses["reflection_positivity_lsz_shortcut"]),
        statuses["reflection_positivity_lsz_shortcut"],
    )
    report(
        "effective-potential-hessian-not-source-overlap-identity",
        "effective-potential Hessian not source-overlap identity"
        in str(statuses["effective_potential_hessian_source_overlap"]),
        statuses["effective_potential_hessian_source_overlap"],
    )
    report(
        "brst-nielsen-identities-not-higgs-pole-identity",
        "BRST-Nielsen identities not Higgs-pole identity"
        in str(statuses["brst_nielsen_higgs_identity"]),
        statuses["brst_nielsen_higgs_identity"],
    )
    report(
        "cl3-automorphism-data-not-source-higgs-identity",
        "Cl3 automorphism data not source-Higgs identity"
        in str(statuses["cl3_automorphism_source_identity"]),
        statuses["cl3_automorphism_source_identity"],
    )
    report(
        "same-source-pole-data-sufficiency-gate-not-passed",
        "same-source pole-data sufficiency gate not passed"
        in str(statuses["same_source_pole_data_sufficiency"]),
        statuses["same_source_pole_data_sufficiency"],
    )
    report(
        "source-functional-lsz-identifiability-boundary-loaded",
        "source-functional LSZ identifiability theorem"
        in str(statuses["source_functional_lsz_identifiability"]),
        statuses["source_functional_lsz_identifiability"],
    )
    report(
        "isolated-pole-gram-factorization-exact-support-not-closure",
        "isolated-pole Gram factorization theorem"
        in str(statuses["isolated_pole_gram_factorization"])
        and certificates["isolated_pole_gram_factorization"].get(
            "isolated_pole_gram_factorization_theorem_passed"
        )
        is True,
        statuses["isolated_pole_gram_factorization"],
    )
    report(
        "osp-oh-assumption-route-audit-blocks-overclaim",
        "O_sp-to-O_H assumption-route audit complete"
        in str(statuses["osp_oh_assumption_route_audit"])
        and certificates["osp_oh_assumption_route_audit"].get("assumption_route_audit_passed")
        is True
        and certificates["osp_oh_assumption_route_audit"].get("proposal_allowed") is False,
        statuses["osp_oh_assumption_route_audit"],
    )
    report(
        "osp-oh-literature-bridge-context-not-closure",
        "O_sp/O_H literature bridge" in str(statuses["osp_oh_literature_bridge"])
        and certificates["osp_oh_literature_bridge"].get("literature_bridge_passed") is True
        and certificates["osp_oh_literature_bridge"].get("proposal_allowed") is False,
        statuses["osp_oh_literature_bridge"],
    )
    report(
        "fms-oh-certificate-construction-attempt-blocks-current-surface",
        "FMS O_H certificate construction blocked"
        in str(statuses["fms_oh_certificate_construction_attempt"])
        and certificates["fms_oh_certificate_construction_attempt"].get("proposal_allowed") is False
        and certificates["fms_oh_certificate_construction_attempt"].get(
            "fms_oh_certificate_available"
        )
        is False
        and certificates["fms_oh_certificate_construction_attempt"].get(
            "fms_construction_attempt_passed_as_boundary"
        )
        is True,
        statuses["fms_oh_certificate_construction_attempt"],
    )
    report(
        "complete-source-spectrum-identity-no-go-blocks",
        "complete source spectrum not canonical-Higgs closure"
        in str(statuses["complete_source_spectrum_identity_no_go"]),
        statuses["complete_source_spectrum_identity_no_go"],
    )
    report(
        "neutral-scalar-top-coupling-tomography-gate-blocks",
        "neutral scalar top-coupling tomography gate not passed"
        in str(statuses["neutral_scalar_top_coupling_tomography_gate"]),
        statuses["neutral_scalar_top_coupling_tomography_gate"],
    )
    report(
        "non-source-response-rank-repair-sufficiency-not-closure",
        "non-source response rank-repair sufficiency theorem"
        in str(statuses["non_source_response_rank_repair_sufficiency"])
        and certificates["non_source_response_rank_repair_sufficiency"].get(
            "rank_repair_sufficiency_theorem_passed"
        )
        is True
        and certificates["non_source_response_rank_repair_sufficiency"].get(
            "current_closure_gate_passed"
        )
        is False,
        statuses["non_source_response_rank_repair_sufficiency"],
    )
    report(
        "positivity-improving-neutral-scalar-rank-one-conditional-support-not-closure",
        "positivity-improving neutral-scalar rank-one theorem"
        in str(statuses["positivity_improving_neutral_scalar_rank_one"])
        and certificates["positivity_improving_neutral_scalar_rank_one"].get(
            "positivity_improving_rank_one_theorem_passed"
        )
        is True
        and certificates["positivity_improving_neutral_scalar_rank_one"].get(
            "positivity_improving_certificate_present"
        )
        is False,
        statuses["positivity_improving_neutral_scalar_rank_one"],
    )
    report(
        "gauge-perron-neutral-scalar-rank-one-import-blocked",
        "gauge-vacuum Perron theorem does not certify neutral-scalar rank-one purity"
        in str(statuses["gauge_perron_neutral_scalar_rank_one_import"])
        and certificates["gauge_perron_neutral_scalar_rank_one_import"].get(
            "exact_negative_boundary_passed"
        )
        is True
        and certificates["gauge_perron_neutral_scalar_rank_one_import"].get(
            "gauge_perron_import_closes_neutral_rank_one"
        )
        is False,
        statuses["gauge_perron_neutral_scalar_rank_one_import"],
    )
    report(
        "neutral-scalar-positivity-improving-direct-theorem-not-derived",
        "neutral-scalar positivity-improving direct theorem not derived"
        in str(statuses["neutral_scalar_positivity_improving_direct_closure"])
        and certificates["neutral_scalar_positivity_improving_direct_closure"].get(
            "direct_positivity_improving_theorem_derived"
        )
        is False
        and certificates["neutral_scalar_positivity_improving_direct_closure"].get(
            "exact_negative_boundary_passed"
        )
        is True,
        statuses["neutral_scalar_positivity_improving_direct_closure"],
    )
    report(
        "neutral-scalar-irreducibility-authority-absent",
        "neutral-scalar irreducibility authority absent"
        in str(statuses["neutral_scalar_irreducibility_authority_audit"])
        and certificates["neutral_scalar_irreducibility_authority_audit"].get(
            "authority_audit_passed"
        )
        is True
        and certificates["neutral_scalar_irreducibility_authority_audit"].get(
            "neutral_scalar_irreducibility_certificate_present"
        )
        is False
        and certificates["neutral_scalar_irreducibility_authority_audit"].get(
            "current_closure_gate_passed"
        )
        is False,
        statuses["neutral_scalar_irreducibility_authority_audit"],
    )
    report(
        "neutral-scalar-primitive-cone-certificate-gate-absent",
        "neutral-scalar primitive-cone certificate gate"
        in str(statuses["neutral_scalar_primitive_cone_certificate_gate"])
        and certificates["neutral_scalar_primitive_cone_certificate_gate"].get("proposal_allowed")
        is False
        and certificates["neutral_scalar_primitive_cone_certificate_gate"].get(
            "primitive_cone_certificate_gate_passed"
        )
        is False,
        statuses["neutral_scalar_primitive_cone_certificate_gate"],
    )
    report(
        "neutral-scalar-primitive-cone-stretch-no-go-blocks",
        "neutral-scalar primitive-cone stretch no-go"
        in str(statuses["neutral_scalar_primitive_cone_stretch_no_go"])
        and certificates["neutral_scalar_primitive_cone_stretch_no_go"].get("proposal_allowed")
        is False
        and certificates["neutral_scalar_primitive_cone_stretch_no_go"].get(
            "primitive_cone_stretch_no_go_passed"
        )
        is True,
        statuses["neutral_scalar_primitive_cone_stretch_no_go"],
    )
    report(
        "neutral-scalar-burnside-irreducibility-attempt-blocks-source-only-generators",
        "Burnside neutral irreducibility attempt"
        in str(statuses["neutral_scalar_burnside_irreducibility_attempt"])
        and certificates["neutral_scalar_burnside_irreducibility_attempt"].get(
            "proposal_allowed"
        )
        is False
        and certificates["neutral_scalar_burnside_irreducibility_attempt"].get(
            "burnside_irreducibility_certificate_passed"
        )
        is False
        and certificates["neutral_scalar_burnside_irreducibility_attempt"].get(
            "burnside_certificate_written"
        )
        is False
        and certificates["neutral_scalar_burnside_irreducibility_attempt"].get(
            "exact_negative_boundary_passed"
        )
        is True,
        statuses["neutral_scalar_burnside_irreducibility_attempt"],
    )
    report(
        "neutral-offdiagonal-generator-derivation-attempt-blocks-current-surface",
        "neutral off-diagonal generator not derivable"
        in str(statuses["neutral_offdiagonal_generator_derivation_attempt"])
        and certificates["neutral_offdiagonal_generator_derivation_attempt"].get(
            "proposal_allowed"
        )
        is False
        and certificates["neutral_offdiagonal_generator_derivation_attempt"].get(
            "offdiagonal_generator_certificate_passed"
        )
        is False
        and certificates["neutral_offdiagonal_generator_derivation_attempt"].get(
            "exact_negative_boundary_passed"
        )
        is True,
        statuses["neutral_offdiagonal_generator_derivation_attempt"],
    )
    report(
        "pr230-logdet-hessian-neutral-mixing-attempt-blocks-source-only-determinant-route",
        "source-only staggered logdet Hessian does not derive"
        in str(statuses["pr230_logdet_hessian_neutral_mixing_attempt"])
        and certificates["pr230_logdet_hessian_neutral_mixing_attempt"].get(
            "proposal_allowed"
        )
        is False
        and certificates["pr230_logdet_hessian_neutral_mixing_attempt"].get(
            "exact_negative_boundary_passed"
        )
        is True
        and certificates["pr230_logdet_hessian_neutral_mixing_attempt"].get(
            "logdet_hessian_bridge_closes_pr230"
        )
        is False,
        statuses["pr230_logdet_hessian_neutral_mixing_attempt"],
    )
    report(
        "scalar-carrier-projector-closure-attempt-blocked",
        "scalar carrier-projector closure attempt blocked" in str(statuses["scalar_carrier_projector_closure"]),
        statuses["scalar_carrier_projector_closure"],
    )
    report(
        "kprime-closure-attempt-blocked",
        "K-prime closure attempt blocked" in str(statuses["kprime_closure"]),
        statuses["kprime_closure"],
    )
    report(
        "pr230-matching-running-bridge-gate-open",
        "matching-running bridge awaits certified physical input"
        in str(statuses["pr230_matching_running_bridge_gate"])
        and certificates["pr230_matching_running_bridge_gate"].get("proposal_allowed") is False,
        statuses["pr230_matching_running_bridge_gate"],
    )
    report(
        "schur-complement-kprime-sufficiency-not-closure",
        "Schur-complement K-prime sufficiency theorem"
        in str(statuses["schur_complement_kprime_sufficiency"])
        and certificates["schur_complement_kprime_sufficiency"].get(
            "schur_sufficiency_theorem_passed"
        )
        is True
        and certificates["schur_complement_kprime_sufficiency"].get(
            "current_closure_gate_passed"
        )
        is False,
        statuses["schur_complement_kprime_sufficiency"],
    )
    report(
        "schur-kprime-row-absence-guard-blocks-source-only-import",
        "Schur K-prime row absence guard"
        in str(statuses["schur_kprime_row_absence_guard"])
        and certificates["schur_kprime_row_absence_guard"].get(
            "schur_kprime_row_absence_guard_passed"
        )
        is True
        and certificates["schur_kprime_row_absence_guard"].get(
            "current_schur_kernel_rows_present"
        )
        is False,
        statuses["schur_kprime_row_absence_guard"],
    )
    report(
        "legacy-schur-bridge-import-audit-blocks-hidden-closure",
        "legacy Schur bridge stack is not PR230 y_t closure"
        in str(statuses["legacy_schur_bridge_import_audit"])
        and certificates["legacy_schur_bridge_import_audit"].get(
            "legacy_schur_import_closes_pr230"
        )
        is False
        and certificates["legacy_schur_bridge_import_audit"].get(
            "exact_negative_boundary_passed"
        )
        is True,
        statuses["legacy_schur_bridge_import_audit"],
    )
    report(
        "schur-kernel-row-contract-gate-not-passed",
        "Schur kernel row contract gate not passed"
        in str(statuses["schur_kernel_row_contract_gate"])
        and certificates["schur_kernel_row_contract_gate"].get(
            "schur_kernel_row_contract_gate_passed"
        )
        is False
        and certificates["schur_kernel_row_contract_gate"].get(
            "current_closure_gate_passed"
        )
        is False,
        statuses["schur_kernel_row_contract_gate"],
    )
    report(
        "schur-row-candidate-extraction-blocks-finite-support-import",
        "Schur row candidate extraction" in str(statuses["schur_row_candidate_extraction_attempt"])
        and certificates["schur_row_candidate_extraction_attempt"].get(
            "candidate_extraction_closes_pr230"
        )
        is False
        and certificates["schur_row_candidate_extraction_attempt"].get(
            "finite_ladder_candidate_usable"
        )
        is False
        and certificates["schur_row_candidate_extraction_attempt"].get("exact_negative_boundary_passed")
        is True,
        statuses["schur_row_candidate_extraction_attempt"],
    )
    report(
        "schur-compressed-denominator-bootstrap-no-go-blocks",
        "Schur compressed-denominator row-bootstrap no-go"
        in str(statuses["schur_compressed_denominator_row_bootstrap_no_go"])
        and certificates["schur_compressed_denominator_row_bootstrap_no_go"].get("proposal_allowed")
        is False
        and certificates["schur_compressed_denominator_row_bootstrap_no_go"].get(
            "bootstrap_no_go_passed"
        )
        is True,
        statuses["schur_compressed_denominator_row_bootstrap_no_go"],
    )
    report(
        "pr230-exact-tensor-schur-row-feasibility-blocks-current-surface",
        "exact tensor Schur A/B/C row feasibility"
        in str(statuses["pr230_exact_tensor_schur_row_feasibility_attempt"])
        and certificates["pr230_exact_tensor_schur_row_feasibility_attempt"].get(
            "proposal_allowed"
        )
        is False
        and certificates["pr230_exact_tensor_schur_row_feasibility_attempt"].get(
            "exact_tensor_schur_row_feasibility_passed"
        )
        is False
        and certificates["pr230_exact_tensor_schur_row_feasibility_attempt"].get(
            "schur_rows_written"
        )
        is False
        and not any(
            certificates["pr230_exact_tensor_schur_row_feasibility_attempt"].get(
                "future_file_presence", {}
            ).values()
        ),
        statuses["pr230_exact_tensor_schur_row_feasibility_attempt"],
    )
    report(
        "pr230-schur-abc-definition-derivation-blocks-current-surface",
        "Schur A/B/C definition not derivable"
        in str(statuses["pr230_schur_abc_definition_derivation_attempt"])
        and certificates["pr230_schur_abc_definition_derivation_attempt"].get(
            "proposal_allowed"
        )
        is False
        and certificates["pr230_schur_abc_definition_derivation_attempt"].get(
            "schur_abc_definition_derivation_passed"
        )
        is False
        and certificates["pr230_schur_abc_definition_derivation_attempt"].get(
            "schur_abc_rows_written"
        )
        is False
        and certificates["pr230_schur_abc_definition_derivation_attempt"].get(
            "exact_negative_boundary_passed"
        )
        is True,
        statuses["pr230_schur_abc_definition_derivation_attempt"],
    )
    report(
        "fh-lsz-higgs-pole-identity-gate-blocks",
        "canonical-Higgs pole identity gate blocking" in str(statuses["fh_lsz_higgs_pole_identity"]),
        statuses["fh_lsz_higgs_pole_identity"],
    )
    report(
        "fh-gauge-normalized-response-needs-gauge-mass-slope",
        "FH gauge-normalized response route" in str(statuses["fh_gauge_normalized_response"]),
        statuses["fh_gauge_normalized_response"],
    )
    report(
        "fh-gauge-mass-response-observable-gap-blocks",
        "FH gauge-mass response observable gap" in str(statuses["fh_gauge_mass_response_observable_gap"]),
        statuses["fh_gauge_mass_response_observable_gap"],
    )
    report(
        "fh-gauge-mass-response-manifest-not-evidence",
        "same-source WZ gauge-mass response manifest"
        in str(statuses["fh_gauge_mass_response_manifest"]),
        statuses["fh_gauge_mass_response_manifest"],
    )
    report(
        "fh-gauge-mass-response-builder-rows-absent",
        "same-source WZ response rows absent"
        in str(statuses["fh_gauge_mass_response_certificate_builder"])
        and certificates["fh_gauge_mass_response_certificate_builder"].get("input_present") is False,
        statuses["fh_gauge_mass_response_certificate_builder"],
    )
    report(
        "same-source-wz-response-certificate-gate-not-passed",
        "same-source WZ response certificate gate not passed"
        in str(statuses["same_source_wz_response_certificate_gate"]),
        statuses["same_source_wz_response_certificate_gate"],
    )
    report(
        "wz-response-harness-absence-guard-not-evidence",
        "WZ response harness absence guard"
        in str(statuses["wz_response_harness_absence_guard"]),
        statuses["wz_response_harness_absence_guard"],
    )
    report(
        "wz-response-repo-harness-import-audit-blocks-hidden-harness",
        "repo-wide WZ response harness import audit"
        in str(statuses["wz_response_repo_harness_import_audit"])
        and certificates["wz_response_repo_harness_import_audit"].get(
            "wz_response_repo_import_closes_pr230"
        )
        is False
        and certificates["wz_response_repo_harness_import_audit"].get(
            "repo_wz_response_harness_found"
        )
        is False
        and certificates["wz_response_repo_harness_import_audit"].get(
            "exact_negative_boundary_passed"
        )
        is True,
        statuses["wz_response_repo_harness_import_audit"],
    )
    report(
        "wz-response-measurement-row-contract-not-evidence",
        "WZ response measurement-row contract gate"
        in str(statuses["wz_response_measurement_row_contract_gate"])
        and certificates["wz_response_measurement_row_contract_gate"].get(
            "wz_measurement_row_contract_gate_passed"
        )
        is False,
        statuses["wz_response_measurement_row_contract_gate"],
    )
    report(
        "wz-response-row-production-attempt-blocks-current-surface",
        "WZ response row production attempt on current surface"
        in str(statuses["wz_response_row_production_attempt"])
        and certificates["wz_response_row_production_attempt"].get(
            "production_attempt_closes_pr230"
        )
        is False
        and certificates["wz_response_row_production_attempt"].get("measurement_rows_written")
        is False,
        statuses["wz_response_row_production_attempt"],
    )
    report(
        "wz-response-harness-implementation-plan-support-only",
        "WZ response harness implementation plan"
        in str(statuses["wz_response_harness_implementation_plan"])
        and certificates["wz_response_harness_implementation_plan"].get("proposal_allowed") is False
        and certificates["wz_response_harness_implementation_plan"].get("future_rows_written") is False
        and len(certificates["wz_response_harness_implementation_plan"].get("implementation_work_units", [])) == 5,
        statuses["wz_response_harness_implementation_plan"],
    )
    report(
        "wz-harness-smoke-schema-support-only",
        "WZ harness smoke schema path" in str(statuses["wz_harness_smoke_schema"])
        and certificates["wz_harness_smoke_schema"].get("proposal_allowed") is False
        and certificates["wz_harness_smoke_schema"].get("wz_harness_smoke_schema_gate_passed") is True,
        statuses["wz_harness_smoke_schema"],
    )
    report(
        "wz-smoke-to-production-promotion-no-go-blocks",
        "WZ smoke rows cannot be promoted"
        in str(statuses["wz_smoke_to_production_promotion_no_go"])
        and certificates["wz_smoke_to_production_promotion_no_go"].get("proposal_allowed") is False
        and certificates["wz_smoke_to_production_promotion_no_go"].get(
            "wz_smoke_to_production_promotion_no_go_passed"
        )
        is True,
        statuses["wz_smoke_to_production_promotion_no_go"],
    )
    report(
        "wz-same-source-ew-action-certificate-builder-blocks",
        "same-source EW action certificate absent"
        in str(statuses["wz_same_source_ew_action_certificate_builder"])
        and certificates["wz_same_source_ew_action_certificate_builder"].get("proposal_allowed") is False
        and certificates["wz_same_source_ew_action_certificate_builder"].get("input_present") is False
        and certificates["wz_same_source_ew_action_certificate_builder"].get("same_source_ew_action_certificate_valid") is False,
        statuses["wz_same_source_ew_action_certificate_builder"],
    )
    report(
        "wz-same-source-ew-action-gate-blocks",
        "same-source EW action not defined"
        in str(statuses["wz_same_source_ew_action_gate"])
        and certificates["wz_same_source_ew_action_gate"].get("proposal_allowed") is False
        and certificates["wz_same_source_ew_action_gate"].get("same_source_ew_action_ready") is False
        and certificates["wz_same_source_ew_action_gate"].get("action_block_written") is False,
        statuses["wz_same_source_ew_action_gate"],
    )
    report(
        "wz-same-source-ew-action-semantic-firewall-not-closure",
        "same-source EW action semantic firewall passed"
        in str(statuses["wz_same_source_ew_action_semantic_firewall"])
        and certificates["wz_same_source_ew_action_semantic_firewall"].get("proposal_allowed") is False,
        statuses["wz_same_source_ew_action_semantic_firewall"],
    )
    report(
        "wz-source-coordinate-transport-no-go-blocks",
        "WZ source-coordinate transport shortcut rejected"
        in str(statuses["wz_source_coordinate_transport_no_go"])
        and certificates["wz_source_coordinate_transport_no_go"].get("proposal_allowed") is False
        and certificates["wz_source_coordinate_transport_no_go"].get(
            "wz_source_coordinate_transport_no_go_passed"
        )
        is True
        and certificates["wz_source_coordinate_transport_no_go"].get(
            "future_transport_certificate_present"
        )
        is False,
        statuses["wz_source_coordinate_transport_no_go"],
    )
    report(
        "wz-goldstone-equivalence-source-identity-no-go-blocks",
        "Goldstone equivalence does not identify PR230 source coordinate"
        in str(statuses["wz_goldstone_equivalence_source_identity_no_go"])
        and certificates["wz_goldstone_equivalence_source_identity_no_go"].get("proposal_allowed")
        is False
        and certificates["wz_goldstone_equivalence_source_identity_no_go"].get(
            "goldstone_equivalence_source_identity_no_go_passed"
        )
        is True,
        statuses["wz_goldstone_equivalence_source_identity_no_go"],
    )
    report(
        "same-source-w-response-decomposition-not-closure",
        "same-source W-response decomposition theorem"
        in str(statuses["same_source_w_response_decomposition"])
        and certificates["same_source_w_response_decomposition"].get("proposal_allowed") is False
        and certificates["same_source_w_response_decomposition"].get(
            "same_source_w_response_decomposition_theorem_passed"
        )
        is True
        and certificates["same_source_w_response_decomposition"].get("current_closure_gate_passed") is False,
        statuses["same_source_w_response_decomposition"],
    )
    report(
        "same-source-w-response-orthogonal-correction-gate-blocks",
        "same-source W-response orthogonal-correction gate not passed"
        in str(statuses["same_source_w_response_orthogonal_correction"])
        and certificates["same_source_w_response_orthogonal_correction"].get("proposal_allowed") is False
        and certificates["same_source_w_response_orthogonal_correction"].get(
            "orthogonal_correction_theorem_passed"
        )
        is True
        and certificates["same_source_w_response_orthogonal_correction"].get(
            "orthogonal_correction_gate_passed"
        )
        is False,
        statuses["same_source_w_response_orthogonal_correction"],
    )
    report(
        "one-higgs-completeness-orthogonal-null-premise-absent",
        "one-Higgs completeness orthogonal-null theorem"
        in str(statuses["one_higgs_completeness_orthogonal_null"])
        and certificates["one_higgs_completeness_orthogonal_null"].get("proposal_allowed") is False
        and certificates["one_higgs_completeness_orthogonal_null"].get(
            "one_higgs_completeness_orthogonal_null_theorem_passed"
        )
        is True
        and certificates["one_higgs_completeness_orthogonal_null"].get(
            "one_higgs_completeness_gate_passed"
        )
        is False,
        statuses["one_higgs_completeness_orthogonal_null"],
    )
    report(
        "same-source-w-response-lightweight-readout-open",
        "lightweight same-source W-response readout"
        in str(statuses["same_source_w_response_lightweight_readout"])
        and certificates["same_source_w_response_lightweight_readout"].get("proposal_allowed") is False
        and certificates["same_source_w_response_lightweight_readout"].get(
            "strict_lightweight_readout_gate_passed"
        )
        is False,
        statuses["same_source_w_response_lightweight_readout"],
    )
    report(
        "delta-perp-tomography-correction-builder-open",
        "delta_perp tomography correction"
        in str(statuses["delta_perp_tomography_correction_builder"])
        and certificates["delta_perp_tomography_correction_builder"].get("proposal_allowed") is False
        and certificates["delta_perp_tomography_correction_builder"].get(
            "strict_delta_perp_tomography_gate_passed"
        )
        is False,
        statuses["delta_perp_tomography_correction_builder"],
    )
    report(
        "same-source-top-response-builder-open",
        "same-source top-response"
        in str(statuses["same_source_top_response_builder"])
        and certificates["same_source_top_response_builder"].get("proposal_allowed") is False
        and certificates["same_source_top_response_builder"].get(
            "strict_same_source_top_response_certificate_builder_passed"
        )
        is False,
        statuses["same_source_top_response_builder"],
    )
    report(
        "same-source-top-response-identity-builder-open",
        "same-source top-response identity"
        in str(statuses["same_source_top_response_identity_builder"])
        and certificates["same_source_top_response_identity_builder"].get("proposal_allowed")
        is False
        and certificates["same_source_top_response_identity_builder"].get(
            "strict_same_source_top_response_identity_builder_passed"
        )
        is False,
        statuses["same_source_top_response_identity_builder"],
    )
    report(
        "top-wz-matched-covariance-builder-open",
        "matched top-W"
        in str(statuses["top_wz_matched_covariance_builder"])
        and certificates["top_wz_matched_covariance_builder"].get("proposal_allowed") is False
        and certificates["top_wz_matched_covariance_builder"].get(
            "strict_top_wz_matched_covariance_builder_passed"
        )
        is False,
        statuses["top_wz_matched_covariance_builder"],
    )
    report(
        "top-wz-covariance-marginal-derivation-no-go-blocks",
        "matched top-W covariance not derivable from marginal response support"
        in str(statuses["top_wz_covariance_marginal_derivation_no_go"])
        and certificates["top_wz_covariance_marginal_derivation_no_go"].get("proposal_allowed")
        is False
        and certificates["top_wz_covariance_marginal_derivation_no_go"].get(
            "marginal_derivation_no_go_passed"
        )
        is True,
        statuses["top_wz_covariance_marginal_derivation_no_go"],
    )
    report(
        "top-wz-factorization-independence-gate-blocks",
        "same-source top-W factorization not derived"
        in str(statuses["top_wz_factorization_independence_gate"])
        and certificates["top_wz_factorization_independence_gate"].get("proposal_allowed")
        is False
        and certificates["top_wz_factorization_independence_gate"].get(
            "strict_factorization_independence_gate_passed"
        )
        is False,
        statuses["top_wz_factorization_independence_gate"],
    )
    report(
        "top-wz-deterministic-response-covariance-gate-blocks",
        "deterministic W response covariance shortcut not derived"
        in str(statuses["top_wz_deterministic_response_covariance_gate"])
        and certificates["top_wz_deterministic_response_covariance_gate"].get("proposal_allowed")
        is False
        and certificates["top_wz_deterministic_response_covariance_gate"].get(
            "strict_deterministic_response_covariance_gate_passed"
        )
        is False,
        statuses["top_wz_deterministic_response_covariance_gate"],
    )
    report(
        "top-wz-covariance-theorem-import-audit-blocks",
        "no importable same-surface top-W covariance theorem"
        in str(statuses["top_wz_covariance_theorem_import_audit"])
        and certificates["top_wz_covariance_theorem_import_audit"].get("proposal_allowed")
        is False
        and certificates["top_wz_covariance_theorem_import_audit"].get(
            "covariance_theorem_import_audit_passed"
        )
        is True,
        statuses["top_wz_covariance_theorem_import_audit"],
    )
    report(
        "same-source-w-response-row-builder-open",
        "same-source W-response row builder"
        in str(statuses["same_source_w_response_row_builder"])
        and certificates["same_source_w_response_row_builder"].get("proposal_allowed") is False
        and certificates["same_source_w_response_row_builder"].get(
            "strict_same_source_w_response_row_builder_passed"
        )
        is False,
        statuses["same_source_w_response_row_builder"],
    )
    report(
        "wz-correlator-mass-fit-path-gate-blocks",
        "WZ correlator mass-fit path absent"
        in str(statuses["wz_correlator_mass_fit_path_gate"])
        and certificates["wz_correlator_mass_fit_path_gate"].get("proposal_allowed") is False
        and certificates["wz_correlator_mass_fit_path_gate"].get("wz_correlator_mass_fit_path_ready") is False
        and certificates["wz_correlator_mass_fit_path_gate"].get("future_mass_fit_rows_present") is False
        and certificates["wz_correlator_mass_fit_path_gate"].get("future_response_rows_present") is False,
        statuses["wz_correlator_mass_fit_path_gate"],
    )
    report(
        "wz-mass-fit-response-row-builder-open",
        "WZ mass-fit response-row builder"
        in str(statuses["wz_mass_fit_response_row_builder"])
        and certificates["wz_mass_fit_response_row_builder"].get("proposal_allowed") is False
        and certificates["wz_mass_fit_response_row_builder"].get(
            "strict_wz_mass_fit_response_row_builder_passed"
        )
        is False,
        statuses["wz_mass_fit_response_row_builder"],
    )
    report(
        "electroweak-g2-certificate-builder-open",
        "electroweak g2 certificate builder inputs absent"
        in str(statuses["electroweak_g2_certificate_builder"])
        and certificates["electroweak_g2_certificate_builder"].get("proposal_allowed")
        is False
        and certificates["electroweak_g2_certificate_builder"].get(
            "strict_electroweak_g2_certificate_passed"
        )
        is False,
        statuses["electroweak_g2_certificate_builder"],
    )
    report(
        "wz-g2-generator-casimir-normalization-no-go-blocks",
        "generator-Casimir normalization does not certify PR230 g2"
        in str(statuses["wz_g2_generator_casimir_normalization_no_go"])
        and certificates["wz_g2_generator_casimir_normalization_no_go"].get(
            "proposal_allowed"
        )
        is False
        and certificates["wz_g2_generator_casimir_normalization_no_go"].get(
            "g2_generator_casimir_no_go_passed"
        )
        is True,
        statuses["wz_g2_generator_casimir_normalization_no_go"],
    )
    report(
        "wz-g2-authority-firewall-blocks",
        "WZ response g2 authority absent" in str(statuses["wz_g2_authority_firewall"])
        and certificates["wz_g2_authority_firewall"].get("proposal_allowed") is False
        and certificates["wz_g2_authority_firewall"].get("g2_authority_gate_passed") is False,
        statuses["wz_g2_authority_firewall"],
    )
    report(
        "wz-g2-response-self-normalization-no-go-blocks",
        "WZ response-only g2 self-normalization no-go"
        in str(statuses["wz_g2_response_self_normalization_no_go"])
        and certificates["wz_g2_response_self_normalization_no_go"].get("proposal_allowed")
        is False
        and certificates["wz_g2_response_self_normalization_no_go"].get(
            "g2_response_self_normalization_no_go_passed"
        )
        is True,
        statuses["wz_g2_response_self_normalization_no_go"],
    )
    report(
        "pr230-wz-g2-bare-running-bridge-attempt-blocks",
        "WZ g2 bare-to-low-scale running bridge"
        in str(statuses["pr230_wz_g2_bare_running_bridge_attempt"])
        and certificates["pr230_wz_g2_bare_running_bridge_attempt"].get(
            "proposal_allowed"
        )
        is False
        and certificates["pr230_wz_g2_bare_running_bridge_attempt"].get(
            "wz_g2_bare_running_bridge_passed"
        )
        is False
        and certificates["pr230_wz_g2_bare_running_bridge_attempt"].get(
            "strict_electroweak_g2_certificate_written"
        )
        is False
        and certificates["pr230_wz_g2_bare_running_bridge_attempt"].get(
            "exact_negative_boundary_passed"
        )
        is True,
        statuses["pr230_wz_g2_bare_running_bridge_attempt"],
    )
    report(
        "same-source-sector-overlap-identity-blocks",
        "same-source sector-overlap identity obstruction"
        in str(statuses["same_source_sector_overlap_identity"]),
        statuses["same_source_sector_overlap_identity"],
    )
    report(
        "source-pole-canonical-higgs-mixing-blocks",
        "source-pole canonical-Higgs mixing obstruction"
        in str(statuses["source_pole_canonical_higgs_mixing"]),
        statuses["source_pole_canonical_higgs_mixing"],
    )
    osp_oh = certificates["osp_oh_identity_stretch"]
    report(
        "osp-oh-identity-stretch-blocks",
        "O_sp-to-O_H identity not derived" in str(statuses["osp_oh_identity_stretch"])
        and osp_oh.get("proposal_allowed") is False
        and osp_oh.get("identity_derived") is False,
        statuses["osp_oh_identity_stretch"],
    )
    report(
        "source-pole-purity-cross-correlator-gate-blocks",
        "source-pole purity cross-correlator gate not passed"
        in str(statuses["source_pole_purity_cross_correlator"]),
        statuses["source_pole_purity_cross_correlator"],
    )
    report(
        "source-higgs-cross-correlator-manifest-not-evidence",
        "source-Higgs cross-correlator production manifest"
        in str(statuses["source_higgs_cross_correlator_manifest"]),
        statuses["source_higgs_cross_correlator_manifest"],
    )
    report(
        "source-higgs-cross-correlator-import-blocks",
        "source-Higgs cross-correlator import audit"
        in str(statuses["source_higgs_cross_correlator_import"]),
        statuses["source_higgs_cross_correlator_import"],
    )
    report(
        "source-higgs-gram-purity-gate-blocks",
        "source-Higgs Gram purity gate not passed"
        in str(statuses["source_higgs_gram_purity_gate"]),
        statuses["source_higgs_gram_purity_gate"],
    )
    report(
        "source-higgs-cross-correlator-harness-extension-not-evidence",
        "source-Higgs cross-correlator harness extension"
        in str(statuses["source_higgs_cross_correlator_harness_extension"])
        and certificates["source_higgs_cross_correlator_harness_extension"].get("proposal_allowed") is False,
        statuses["source_higgs_cross_correlator_harness_extension"],
    )
    report(
        "source-higgs-pole-residue-extractor-awaits-valid-production-rows",
        "source-Higgs pole-residue extractor"
        in str(statuses["source_higgs_pole_residue_extractor"])
        and certificates["source_higgs_pole_residue_extractor"].get("proposal_allowed") is False
        and certificates["source_higgs_pole_residue_extractor"].get("rows_written") is False,
        statuses["source_higgs_pole_residue_extractor"],
    )
    report(
        "source-higgs-cross-correlator-builder-rows-absent",
        "source-Higgs cross-correlator rows absent"
        in str(statuses["source_higgs_cross_correlator_certificate_builder"])
        and certificates["source_higgs_cross_correlator_certificate_builder"].get("source_pole_operator_available") is True,
        statuses["source_higgs_cross_correlator_certificate_builder"],
    )
    report(
        "osp-higgs-gram-purity-postprocessor-awaits-production",
        "O_sp-Higgs Gram-purity postprocess awaiting production certificate"
        in str(statuses["source_higgs_gram_purity_postprocessor"])
        and certificates["source_higgs_gram_purity_postprocessor"].get("osp_higgs_gram_purity_gate_passed") is False,
        statuses["source_higgs_gram_purity_postprocessor"],
    )
    report(
        "source-higgs-gram-purity-contract-witness-not-evidence",
        "source-Higgs Gram-purity contract witness"
        in str(statuses["source_higgs_gram_purity_contract_witness"])
        and certificates["source_higgs_gram_purity_contract_witness"].get("contract_witness_passed") is True,
        statuses["source_higgs_gram_purity_contract_witness"],
    )
    report(
        "source-higgs-production-readiness-blocks-launch",
        "source-Higgs production launch blocked"
        in str(statuses["source_higgs_production_readiness_gate"])
        and certificates["source_higgs_production_readiness_gate"].get("proposal_allowed") is False
        and certificates["source_higgs_production_readiness_gate"].get("source_higgs_launch_ready") is False
        and certificates["source_higgs_production_readiness_gate"].get("operator_certificate_present") is False
        and certificates["source_higgs_production_readiness_gate"].get("future_rows_present") is False
        and certificates["source_higgs_production_readiness_gate"].get(
            "current_chunk_wave_can_supply_source_higgs_rows"
        )
        is False
        and certificates["source_higgs_production_readiness_gate"].get(
            "taste_radial_rows_are_c_sx_c_xx_not_c_sH_c_HH"
        )
        is True
        and certificates["source_higgs_production_readiness_gate"].get(
            "taste_radial_rows_lack_canonical_oh_identity"
        )
        is True,
        statuses["source_higgs_production_readiness_gate"],
    )
    report(
        "pr230-clean-source-higgs-math-tool-selector-support-only",
        "clean source-Higgs outside-math route selector"
        in str(statuses["pr230_clean_source_higgs_math_tool_route_selector"])
        and certificates["pr230_clean_source_higgs_math_tool_route_selector"].get(
            "proposal_allowed"
        )
        is False
        and certificates["pr230_clean_source_higgs_math_tool_route_selector"].get(
            "clean_physics_priority"
        )
        == "source_higgs"
        and certificates["pr230_clean_source_higgs_math_tool_route_selector"]
        .get("selected_clean_route", {})
        .get("id")
        == "source_higgs_fms_action_then_gram_pole_rows",
        statuses["pr230_clean_source_higgs_math_tool_route_selector"],
    )
    report(
        "pr230-fresh-artifact-literature-review-selects-oh-contract-not-closure",
        "fresh artifact literature route review"
        in str(statuses["pr230_fresh_artifact_literature_route_review"])
        and certificates["pr230_fresh_artifact_literature_route_review"].get(
            "proposal_allowed"
        )
        is False
        and certificates["pr230_fresh_artifact_literature_route_review"].get(
            "review_passed"
        )
        is True
        and certificates["pr230_fresh_artifact_literature_route_review"].get(
            "genuine_artifact_found_on_current_surface"
        )
        is False
        and certificates["pr230_fresh_artifact_literature_route_review"]
        .get("selected_genuine_artifact_contract", {})
        .get("contract")
        == "O_H/C_sH/C_HH source-Higgs pole rows",
        statuses["pr230_fresh_artifact_literature_route_review"],
    )
    report(
        "pr230-action-first-oh-artifact-attempt-blocks-current-surface",
        "action-first O_H artifact not constructible"
        in str(statuses["pr230_action_first_oh_artifact_attempt"])
        and certificates["pr230_action_first_oh_artifact_attempt"].get(
            "proposal_allowed"
        )
        is False
        and certificates["pr230_action_first_oh_artifact_attempt"].get(
            "exact_negative_boundary_passed"
        )
        is True
        and certificates["pr230_action_first_oh_artifact_attempt"].get(
            "same_source_ew_action_certificate_written"
        )
        is False
        and certificates["pr230_action_first_oh_artifact_attempt"].get(
            "canonical_oh_certificate_written"
        )
        is False,
        statuses["pr230_action_first_oh_artifact_attempt"],
    )
    report(
        "pr230-holonomic-source-response-gate-blocks-missing-oh-h-source",
        "PR541-style holonomic source-response route"
        in str(statuses["pr230_holonomic_source_response_feasibility_gate"])
        and certificates["pr230_holonomic_source_response_feasibility_gate"].get(
            "proposal_allowed"
        )
        is False
        and certificates["pr230_holonomic_source_response_feasibility_gate"].get(
            "exact_negative_boundary_passed"
        )
        is True
        and certificates["pr230_holonomic_source_response_feasibility_gate"].get(
            "two_source_functional_current_surface_defined"
        )
        is False,
        statuses["pr230_holonomic_source_response_feasibility_gate"],
    )
    report(
        "pr230-oh-source-higgs-authority-rescan-finds-no-current-certificate",
        "O_H/source-Higgs authority rescan found no"
        in str(statuses["pr230_oh_source_higgs_authority_rescan_gate"])
        and certificates["pr230_oh_source_higgs_authority_rescan_gate"].get(
            "proposal_allowed"
        )
        is False
        and certificates["pr230_oh_source_higgs_authority_rescan_gate"].get(
            "oh_source_higgs_authority_found"
        )
        is False
        and certificates["pr230_oh_source_higgs_authority_rescan_gate"].get(
            "exact_negative_boundary_passed"
        )
        is True,
        statuses["pr230_oh_source_higgs_authority_rescan_gate"],
    )
    report(
        "pr230-minimal-axioms-yukawa-summary-not-proof-authority",
        "minimal-axioms Yukawa summary is not PR230 proof authority"
        in str(statuses["pr230_minimal_axioms_yukawa_summary_firewall"])
        and certificates["pr230_minimal_axioms_yukawa_summary_firewall"].get(
            "proposal_allowed"
        )
        is False
        and certificates["pr230_minimal_axioms_yukawa_summary_firewall"].get(
            "exact_negative_boundary_passed"
        )
        is True
        and certificates["pr230_minimal_axioms_yukawa_summary_firewall"].get(
            "yt_ward_audit_status", {}
        ).get("effective_status")
        == "audited_renaming",
        statuses["pr230_minimal_axioms_yukawa_summary_firewall"],
    )
    report(
        "pr230-genuine-source-pole-artifact-support-only",
        "genuine same-source O_sp source-pole artifact"
        in str(statuses["pr230_genuine_source_pole_artifact_intake"])
        and certificates["pr230_genuine_source_pole_artifact_intake"].get(
            "proposal_allowed"
        )
        is False
        and certificates["pr230_genuine_source_pole_artifact_intake"].get(
            "artifact_is_genuine_current_surface_support"
        )
        is True
        and certificates["pr230_genuine_source_pole_artifact_intake"].get(
            "artifact_is_physics_closure"
        )
        is False,
        statuses["pr230_genuine_source_pole_artifact_intake"],
    )
    report(
        "pr230-l12-chunk-compute-status-support-only",
        "completed L12 same-source chunk compute status"
        in str(statuses["pr230_l12_chunk_compute_status"])
        and certificates["pr230_l12_chunk_compute_status"].get("proposal_allowed")
        is False
        and certificates["pr230_l12_chunk_compute_status"].get(
            "strict_closure_blockers", {}
        ).get("scalar_lsz_denominator_certificate_absent")
        is True
        and certificates["pr230_l12_chunk_compute_status"].get(
            "strict_closure_blockers", {}
        ).get("canonical_oh_or_source_higgs_overlap_absent")
        is True,
        statuses["pr230_l12_chunk_compute_status"],
    )
    taste_bridge = certificates["pr230_taste_condensate_oh_bridge_audit"]
    report(
        "pr230-taste-condensate-oh-bridge-blocks-current-shortcut",
        "taste-condensate Higgs stack does not supply PR230 O_H bridge"
        in str(statuses["pr230_taste_condensate_oh_bridge_audit"])
        and taste_bridge.get("proposal_allowed") is False
        and taste_bridge.get("taste_condensate_oh_bridge_audit_passed") is True
        and taste_bridge.get("algebra", {}).get(
            "uniform_source_relative_projection_onto_taste_axis_span"
        )
        == 0.0,
        statuses["pr230_taste_condensate_oh_bridge_audit"],
    )
    source_coordinate_transport = certificates["pr230_source_coordinate_transport_gate"]
    report(
        "pr230-source-coordinate-transport-blocks-current-shortcut",
        "source-coordinate transport to canonical O_H not derivable"
        in str(statuses["pr230_source_coordinate_transport_gate"])
        and source_coordinate_transport.get("proposal_allowed") is False
        and source_coordinate_transport.get("source_coordinate_transport_gate_passed")
        is True
        and source_coordinate_transport.get("future_transport_certificate_present")
        is False,
        statuses["pr230_source_coordinate_transport_gate"],
    )
    origin_main_composite_higgs = certificates["pr230_origin_main_composite_higgs_intake_guard"]
    report(
        "pr230-origin-main-composite-higgs-intake-not-closure",
        "origin/main composite-Higgs stretch"
        in str(statuses["pr230_origin_main_composite_higgs_intake_guard"])
        and origin_main_composite_higgs.get("proposal_allowed") is False
        and origin_main_composite_higgs.get(
            "origin_main_composite_higgs_intake_guard_passed"
        )
        is True
        and origin_main_composite_higgs.get("origin_main_composite_higgs_closes_pr230")
        is False,
        statuses["pr230_origin_main_composite_higgs_intake_guard"],
    )
    origin_main_ew_m_residual = certificates[
        "pr230_origin_main_ew_m_residual_intake_guard"
    ]
    report(
        "pr230-origin-main-ew-m-residual-intake-not-closure",
        "origin/main EW M-residual CMT packet"
        in str(statuses["pr230_origin_main_ew_m_residual_intake_guard"])
        and origin_main_ew_m_residual.get("proposal_allowed") is False
        and origin_main_ew_m_residual.get(
            "origin_main_ew_m_residual_intake_guard_passed"
        )
        is True
        and origin_main_ew_m_residual.get("origin_main_ew_m_residual_closes_pr230")
        is False,
        statuses["pr230_origin_main_ew_m_residual_intake_guard"],
    )
    z3_triplet_conditional_primitive = certificates[
        "pr230_z3_triplet_conditional_primitive_cone"
    ]
    report(
        "pr230-z3-triplet-conditional-primitive-support-not-closure",
        "Z3-triplet primitive-cone theorem"
        in str(statuses["pr230_z3_triplet_conditional_primitive_cone"])
        and z3_triplet_conditional_primitive.get("proposal_allowed") is False
        and z3_triplet_conditional_primitive.get(
            "z3_triplet_conditional_primitive_theorem_passed"
        )
        is True
        and z3_triplet_conditional_primitive.get("pr230_closure_authorized")
        is False,
        statuses["pr230_z3_triplet_conditional_primitive_cone"],
    )
    z3_positive_cone_support = certificates[
        "pr230_z3_triplet_positive_cone_support_certificate"
    ]
    report(
        "pr230-z3-triplet-positive-cone-h2-support-not-transfer",
        "Z3-triplet positive-cone H2 support"
        in str(statuses["pr230_z3_triplet_positive_cone_support_certificate"])
        and z3_positive_cone_support.get("proposal_allowed") is False
        and z3_positive_cone_support.get(
            "z3_triplet_positive_cone_h2_support_passed"
        )
        is True
        and z3_positive_cone_support.get("pr230_closure_authorized") is False
        and z3_positive_cone_support.get("supplies_conditional_premises", {}).get(
            "H2_positive_cone_equal_magnitude_support"
        )
        is True
        and z3_positive_cone_support.get("supplies_conditional_premises", {}).get(
            "H3_lazy_positive_physical_transfer"
        )
        is False,
        statuses["pr230_z3_triplet_positive_cone_support_certificate"],
    )
    z3_generation_action_lift = certificates["pr230_z3_generation_action_lift_attempt"]
    report(
        "pr230-z3-generation-action-lift-not-derived",
        "Z3 generation-action lift"
        in str(statuses["pr230_z3_generation_action_lift_attempt"])
        and z3_generation_action_lift.get("proposal_allowed") is False
        and z3_generation_action_lift.get(
            "h1_generation_action_lift_attempt_passed"
        )
        is True
        and z3_generation_action_lift.get("same_surface_h1_derived") is False
        and z3_generation_action_lift.get("pr230_closure_authorized") is False,
        statuses["pr230_z3_generation_action_lift_attempt"],
    )
    z3_lazy_transfer_promotion = certificates[
        "pr230_z3_lazy_transfer_promotion_attempt"
    ]
    report(
        "pr230-z3-lazy-transfer-promotion-not-derived",
        "Z3 lazy-transfer promotion not derivable"
        in str(statuses["pr230_z3_lazy_transfer_promotion_attempt"])
        and z3_lazy_transfer_promotion.get("proposal_allowed") is False
        and z3_lazy_transfer_promotion.get(
            "z3_lazy_transfer_promotion_attempt_passed"
        )
        is True
        and z3_lazy_transfer_promotion.get("physical_lazy_transfer_instantiated")
        is False
        and z3_lazy_transfer_promotion.get("pr230_closure_authorized") is False,
        statuses["pr230_z3_lazy_transfer_promotion_attempt"],
    )
    z3_lazy_selector_no_go = certificates["pr230_z3_lazy_selector_no_go"]
    report(
        "pr230-z3-lazy-selector-no-go-blocks-current-shortcut",
        "Z3 lazy selector shortcuts do not derive"
        in str(statuses["pr230_z3_lazy_selector_no_go"])
        and z3_lazy_selector_no_go.get("proposal_allowed") is False
        and z3_lazy_selector_no_go.get("z3_lazy_selector_no_go_passed") is True
        and z3_lazy_selector_no_go.get("physical_lazy_transfer_instantiated")
        is False
        and z3_lazy_selector_no_go.get("pr230_closure_authorized") is False,
        statuses["pr230_z3_lazy_selector_no_go"],
    )
    same_surface_z3_taste_triplet = certificates["pr230_same_surface_z3_taste_triplet"]
    report(
        "pr230-same-surface-z3-taste-triplet-support-not-closure",
        "same-surface Z3 taste-triplet artifact"
        in str(statuses["pr230_same_surface_z3_taste_triplet"])
        and same_surface_z3_taste_triplet.get("proposal_allowed") is False
        and same_surface_z3_taste_triplet.get(
            "same_surface_z3_triplet_artifact_passed"
        )
        is True
        and same_surface_z3_taste_triplet.get("pr230_closure_authorized")
        is False,
        statuses["pr230_same_surface_z3_taste_triplet"],
    )
    source_transport_completion = certificates["pr230_source_coordinate_transport_completion"]
    report(
        "pr230-source-coordinate-transport-current-surface-closed",
        "source-coordinate transport not derivable from current PR230 surface"
        in str(statuses["pr230_source_coordinate_transport_completion"])
        and source_transport_completion.get("proposal_allowed") is False
        and source_transport_completion.get("source_coordinate_transport_completion_passed")
        is True,
        statuses["pr230_source_coordinate_transport_completion"],
    )
    two_source_taste_radial_chart = certificates["pr230_two_source_taste_radial_chart"]
    report(
        "pr230-two-source-taste-radial-chart-support-not-closure",
        "two-source taste-radial chart"
        in str(statuses["pr230_two_source_taste_radial_chart"])
        and two_source_taste_radial_chart.get("proposal_allowed") is False
        and two_source_taste_radial_chart.get(
            "two_source_taste_radial_chart_support_passed"
        )
        is True
        and two_source_taste_radial_chart.get("forbidden_firewall", {}).get(
            "identified_taste_radial_axis_with_canonical_oh"
        )
        is False,
        statuses["pr230_two_source_taste_radial_chart"],
    )
    two_source_taste_radial_action = certificates["pr230_two_source_taste_radial_action"]
    report(
        "pr230-two-source-taste-radial-action-support-not-closure",
        "two-source taste-radial action source vertex"
        in str(statuses["pr230_two_source_taste_radial_action"])
        and two_source_taste_radial_action.get("proposal_allowed") is False
        and two_source_taste_radial_action.get("two_source_taste_radial_action_passed")
        is True
        and two_source_taste_radial_action.get("operator_certificate_payload", {}).get(
            "canonical_higgs_operator_identity_passed"
        )
        is False,
        statuses["pr230_two_source_taste_radial_action"],
    )
    two_source_taste_radial_row_contract = certificates["pr230_two_source_taste_radial_row_contract"]
    report(
        "pr230-two-source-taste-radial-row-contract-support-not-closure",
        "two-source taste-radial C_sx/C_xx row contract"
        in str(statuses["pr230_two_source_taste_radial_row_contract"])
        and two_source_taste_radial_row_contract.get("proposal_allowed") is False
        and two_source_taste_radial_row_contract.get(
            "two_source_taste_radial_row_contract_passed"
        )
        is True
        and two_source_taste_radial_row_contract.get("future_file_presence", {}).get(
            "taste_radial_production_rows"
        )
        is False,
        statuses["pr230_two_source_taste_radial_row_contract"],
    )
    two_source_taste_radial_row_manifest = certificates[
        "pr230_two_source_taste_radial_row_production_manifest"
    ]
    report(
        "pr230-two-source-taste-radial-row-production-manifest-support-not-closure",
        "two-source taste-radial C_sx/C_xx production manifest"
        in str(statuses["pr230_two_source_taste_radial_row_production_manifest"])
        and two_source_taste_radial_row_manifest.get("proposal_allowed") is False
        and two_source_taste_radial_row_manifest.get("manifest_passed") is True
        and two_source_taste_radial_row_manifest.get("dry_run_only") is True
        and two_source_taste_radial_row_manifest.get("future_combined_rows_present")
        is False,
        statuses["pr230_two_source_taste_radial_row_production_manifest"],
    )
    two_source_taste_radial_row_combiner = certificates[
        "pr230_two_source_taste_radial_row_combiner_gate"
    ]
    two_source_combiner_ready = two_source_taste_radial_row_combiner.get("ready_chunks")
    two_source_combiner_expected = two_source_taste_radial_row_combiner.get("expected_chunks")
    two_source_combiner_support_boundary = (
        isinstance(two_source_combiner_ready, int)
        and isinstance(two_source_combiner_expected, int)
        and (
            (
                two_source_taste_radial_row_combiner.get("combined_rows_written")
                is False
                and 0 < two_source_combiner_ready < two_source_combiner_expected
            )
            or (
                two_source_taste_radial_row_combiner.get("combined_rows_written")
                is True
                and two_source_combiner_ready == two_source_combiner_expected == 63
            )
        )
    )
    report(
        "pr230-two-source-taste-radial-row-combiner-support-not-closure",
        "two-source taste-radial C_sx/C_xx row combiner gate"
        in str(statuses["pr230_two_source_taste_radial_row_combiner_gate"])
        and two_source_taste_radial_row_combiner.get("proposal_allowed") is False
        and two_source_combiner_support_boundary
        and two_source_taste_radial_row_combiner.get("fail_count") == 0,
        statuses["pr230_two_source_taste_radial_row_combiner_gate"],
    )
    two_source_taste_radial_chunk_package = certificates[
        "pr230_two_source_taste_radial_chunk_package"
    ]
    report(
        "pr230-two-source-taste-radial-chunk-package-support-not-closure",
        "two-source taste-radial chunks001-"
        in str(statuses["pr230_two_source_taste_radial_chunk_package"])
        and two_source_taste_radial_chunk_package.get("proposal_allowed") is False
        and two_source_taste_radial_chunk_package.get("chunk_package_audit_passed")
        is True
        and two_source_taste_radial_chunk_package.get(
            "active_chunks_counted_as_evidence"
        )
        is False,
        statuses["pr230_two_source_taste_radial_chunk_package"],
    )
    source_higgs_pole_row_acceptance_contract = certificates[
        "pr230_source_higgs_pole_row_acceptance_contract"
    ]
    report(
        "pr230-source-higgs-pole-row-contract-open",
        "source-Higgs C_ss/C_sH/C_HH pole-row acceptance contract"
        in str(statuses["pr230_source_higgs_pole_row_acceptance_contract"])
        and source_higgs_pole_row_acceptance_contract.get("proposal_allowed") is False
        and source_higgs_pole_row_acceptance_contract.get(
            "source_higgs_pole_row_acceptance_contract_passed"
        )
        is True
        and source_higgs_pole_row_acceptance_contract.get(
            "closure_contract_satisfied"
        )
        is False,
        statuses["pr230_source_higgs_pole_row_acceptance_contract"],
    )
    two_source_taste_radial_schur_subblock = certificates[
        "pr230_two_source_taste_radial_schur_subblock_witness"
    ]
    report(
        "pr230-two-source-taste-radial-schur-subblock-support-not-closure",
        "two-source taste-radial Schur-subblock witness"
        in str(statuses["pr230_two_source_taste_radial_schur_subblock_witness"])
        and two_source_taste_radial_schur_subblock.get("proposal_allowed") is False
        and two_source_taste_radial_schur_subblock.get(
            "two_source_taste_radial_schur_subblock_witness_passed"
        )
        is True
        and two_source_taste_radial_schur_subblock.get(
            "strict_schur_kernel_row_contract_passed"
        )
        is False
        and two_source_taste_radial_schur_subblock.get(
            "canonical_higgs_operator_identity_passed"
        )
        is False,
        statuses["pr230_two_source_taste_radial_schur_subblock_witness"],
    )
    two_source_taste_radial_kprime_scout = certificates[
        "pr230_two_source_taste_radial_schur_kprime_finite_shell_scout"
    ]
    report(
        "pr230-two-source-taste-radial-kprime-finite-shell-scout-not-closure",
        "finite-shell Schur inverse-slope scout"
        in str(statuses["pr230_two_source_taste_radial_schur_kprime_finite_shell_scout"])
        and two_source_taste_radial_kprime_scout.get("proposal_allowed") is False
        and two_source_taste_radial_kprime_scout.get(
            "finite_shell_schur_kprime_scout_passed"
        )
        is True
        and two_source_taste_radial_kprime_scout.get(
            "strict_schur_kprime_authority_passed"
        )
        is False
        and two_source_taste_radial_kprime_scout.get(
            "pole_location_or_derivative_rows_present"
        )
        is False
        and two_source_taste_radial_kprime_scout.get(
            "canonical_higgs_operator_identity_passed"
        )
        is False,
        statuses["pr230_two_source_taste_radial_schur_kprime_finite_shell_scout"],
    )
    two_source_taste_radial_schur_abc_finite_rows = certificates[
        "pr230_two_source_taste_radial_schur_abc_finite_rows"
    ]
    report(
        "pr230-two-source-taste-radial-schur-abc-finite-rows-not-closure",
        "finite Schur A/B/C inverse-block rows"
        in str(statuses["pr230_two_source_taste_radial_schur_abc_finite_rows"])
        and two_source_taste_radial_schur_abc_finite_rows.get("proposal_allowed") is False
        and two_source_taste_radial_schur_abc_finite_rows.get(
            "two_source_taste_radial_schur_abc_finite_rows_passed"
        )
        is True
        and two_source_taste_radial_schur_abc_finite_rows.get(
            "finite_schur_abc_rows_written"
        )
        is True
        and two_source_taste_radial_schur_abc_finite_rows.get(
            "strict_schur_abc_kernel_rows_written"
        )
        is False
        and two_source_taste_radial_schur_abc_finite_rows.get(
            "strict_schur_kprime_authority_passed"
        )
        is False
        and two_source_taste_radial_schur_abc_finite_rows.get(
            "canonical_higgs_operator_identity_passed"
        )
        is False,
        statuses["pr230_two_source_taste_radial_schur_abc_finite_rows"],
    )
    two_source_taste_radial_schur_pole_lift_gate = certificates[
        "pr230_two_source_taste_radial_schur_pole_lift_gate"
    ]
    report(
        "pr230-two-source-taste-radial-schur-pole-lift-gate-blocks-endpoint-promotion",
        "finite Schur A/B/C rows do not lift to strict pole-row authority"
        in str(statuses["pr230_two_source_taste_radial_schur_pole_lift_gate"])
        and two_source_taste_radial_schur_pole_lift_gate.get("proposal_allowed") is False
        and two_source_taste_radial_schur_pole_lift_gate.get(
            "two_source_taste_radial_schur_pole_lift_gate_passed"
        )
        is True
        and two_source_taste_radial_schur_pole_lift_gate.get("strict_pole_lift_passed")
        is False
        and two_source_taste_radial_schur_pole_lift_gate.get(
            "endpoint_derivative_nonidentifiability_witness_passed"
        )
        is True,
        statuses["pr230_two_source_taste_radial_schur_pole_lift_gate"],
    )
    two_source_taste_radial_primitive_transfer_candidate_gate = certificates[
        "pr230_two_source_taste_radial_primitive_transfer_candidate_gate"
    ]
    report(
        "pr230-two-source-taste-radial-primitive-transfer-candidate-not-h3",
        "finite C_sx rows do not certify a physical primitive neutral transfer"
        in str(statuses["pr230_two_source_taste_radial_primitive_transfer_candidate_gate"])
        and two_source_taste_radial_primitive_transfer_candidate_gate.get("proposal_allowed")
        is False
        and two_source_taste_radial_primitive_transfer_candidate_gate.get(
            "physical_transfer_candidate_accepted"
        )
        is False
        and two_source_taste_radial_primitive_transfer_candidate_gate.get(
            "finite_offdiagonal_correlation_support"
        )
        is True
        and two_source_taste_radial_primitive_transfer_candidate_gate.get(
            "finite_correlator_blocks_positive"
        )
        is True,
        statuses["pr230_two_source_taste_radial_primitive_transfer_candidate_gate"],
    )
    orthogonal_top_coupling_exclusion_candidate_gate = certificates[
        "pr230_orthogonal_top_coupling_exclusion_candidate_gate"
    ]
    report(
        "pr230-orthogonal-top-coupling-exclusion-candidate-rejected",
        "orthogonal-neutral top-coupling exclusion candidate rejected"
        in str(statuses["pr230_orthogonal_top_coupling_exclusion_candidate_gate"])
        and orthogonal_top_coupling_exclusion_candidate_gate.get("proposal_allowed")
        is False
        and orthogonal_top_coupling_exclusion_candidate_gate.get(
            "orthogonal_top_coupling_exclusion_candidate_accepted"
        )
        is False
        and orthogonal_top_coupling_exclusion_candidate_gate.get(
            "same_surface_selection_rule_present"
        )
        is False
        and orthogonal_top_coupling_exclusion_candidate_gate.get(
            "finite_c_sx_rows_are_top_coupling_tomography"
        )
        is False,
        statuses["pr230_orthogonal_top_coupling_exclusion_candidate_gate"],
    )
    strict_scalar_lsz_moment_fv_authority_gate = certificates[
        "pr230_strict_scalar_lsz_moment_fv_authority_gate"
    ]
    report(
        "pr230-strict-scalar-lsz-moment-fv-authority-absent",
        "raw C_ss rows do not supply strict scalar-LSZ moment/FV authority"
        in str(statuses["pr230_strict_scalar_lsz_moment_fv_authority_gate"])
        and strict_scalar_lsz_moment_fv_authority_gate.get("proposal_allowed")
        is False
        and strict_scalar_lsz_moment_fv_authority_gate.get(
            "strict_scalar_lsz_moment_fv_authority_gate_passed"
        )
        is True
        and strict_scalar_lsz_moment_fv_authority_gate.get(
            "strict_scalar_lsz_moment_fv_authority_present"
        )
        is False
        and strict_scalar_lsz_moment_fv_authority_gate.get(
            "current_raw_c_ss_proxy_fails_stieltjes_monotonicity"
        )
        is True,
        statuses["pr230_strict_scalar_lsz_moment_fv_authority_gate"],
    )
    schur_complement_stieltjes_repair_gate = certificates[
        "pr230_schur_complement_stieltjes_repair_gate"
    ]
    report(
        "pr230-schur-complement-stieltjes-repair-support-not-closure",
        "Schur-complement Stieltjes repair split"
        in str(statuses["pr230_schur_complement_stieltjes_repair_gate"])
        and schur_complement_stieltjes_repair_gate.get("proposal_allowed") is False
        and schur_complement_stieltjes_repair_gate.get(
            "schur_complement_stieltjes_repair_gate_passed"
        )
        is True
        and schur_complement_stieltjes_repair_gate.get(
            "source_given_x_stieltjes_first_shell_failed"
        )
        is True
        and schur_complement_stieltjes_repair_gate.get(
            "x_given_source_stieltjes_first_shell_passed"
        )
        is True
        and schur_complement_stieltjes_repair_gate.get(
            "strict_scalar_lsz_authority_present"
        )
        is False
        and schur_complement_stieltjes_repair_gate.get(
            "canonical_higgs_operator_identity_passed"
        )
        is False,
        statuses["pr230_schur_complement_stieltjes_repair_gate"],
    )
    schur_complete_monotonicity_gate = certificates[
        "pr230_schur_complement_complete_monotonicity_gate"
    ]
    report(
        "pr230-schur-complement-complete-monotonicity-authority-absent",
        "C_x|s Schur residual passes"
        in str(statuses["pr230_schur_complement_complete_monotonicity_gate"])
        and schur_complete_monotonicity_gate.get("proposal_allowed") is False
        and schur_complete_monotonicity_gate.get(
            "schur_complement_complete_monotonicity_gate_passed"
        )
        is True
        and schur_complete_monotonicity_gate.get(
            "x_given_source_first_shell_stieltjes_support"
        )
        is True
        and schur_complete_monotonicity_gate.get(
            "complete_monotonicity_authority_passed"
        )
        is False
        and schur_complete_monotonicity_gate.get(
            "canonical_higgs_or_physical_response_bridge_present"
        )
        is False,
        statuses["pr230_schur_complement_complete_monotonicity_gate"],
    )
    schur_one_pole_scout = certificates["pr230_schur_x_given_source_one_pole_scout"]
    schur_one_pole_scout_not_authority = (
        "one-pole finite-residue scout"
        in str(statuses["pr230_schur_x_given_source_one_pole_scout"])
        and schur_one_pole_scout.get("proposal_allowed") is False
        and schur_one_pole_scout.get("schur_x_given_source_one_pole_scout_passed")
        is True
        and schur_one_pole_scout.get("one_pole_fit_valid") is True
        and schur_one_pole_scout.get("one_pole_model_class_authority_passed")
        is False
        and schur_one_pole_scout.get("two_pole_counterfamily_present") is True
        and schur_one_pole_scout.get("physical_pole_residue_authority_present")
        is False
        and schur_one_pole_scout.get(
            "canonical_higgs_or_physical_response_bridge_present"
        )
        is False
    )
    report(
        "pr230-schur-x-given-source-one-pole-scout-not-authority",
        schur_one_pole_scout_not_authority,
        statuses["pr230_schur_x_given_source_one_pole_scout"],
    )
    taste_radial_selector_gate = certificates[
        "pr230_taste_radial_canonical_oh_selector_gate"
    ]
    report(
        "pr230-taste-radial-canonical-oh-selector-blocks-symmetry-shortcut",
        "degree-one taste-radial uniqueness"
        in str(statuses["pr230_taste_radial_canonical_oh_selector_gate"])
        and taste_radial_selector_gate.get("proposal_allowed") is False
        and taste_radial_selector_gate.get(
            "taste_radial_canonical_oh_selector_gate_passed"
        )
        is True
        and taste_radial_selector_gate.get("degree_one_radial_unique") is True
        and taste_radial_selector_gate.get("full_invariant_selector_nonunique")
        is True
        and taste_radial_selector_gate.get("canonical_oh_selector_absent") is True,
        statuses["pr230_taste_radial_canonical_oh_selector_gate"],
    )
    degree_one_higgs_action_premise_gate = certificates[
        "pr230_degree_one_higgs_action_premise_gate"
    ]
    report(
        "pr230-degree-one-higgs-action-premise-not-derived",
        "degree-one Higgs-action premise not derived"
        in str(statuses["pr230_degree_one_higgs_action_premise_gate"])
        and degree_one_higgs_action_premise_gate.get("proposal_allowed") is False
        and degree_one_higgs_action_premise_gate.get(
            "degree_one_higgs_action_premise_gate_passed"
        )
        is True
        and degree_one_higgs_action_premise_gate.get(
            "degree_one_premise_authorized_on_current_surface"
        )
        is False
        and degree_one_higgs_action_premise_gate.get("degree_one_filter_selects_e1")
        is True,
        statuses["pr230_degree_one_higgs_action_premise_gate"],
    )
    degree_one_radial_tangent_oh_theorem = certificates[
        "pr230_degree_one_radial_tangent_oh_theorem"
    ]
    report(
        "pr230-degree-one-radial-tangent-oh-theorem-support-not-closure",
        "degree-one radial-tangent O_H uniqueness theorem"
        in str(statuses["pr230_degree_one_radial_tangent_oh_theorem"])
        and degree_one_radial_tangent_oh_theorem.get("proposal_allowed") is False
        and degree_one_radial_tangent_oh_theorem.get(
            "degree_one_radial_tangent_oh_theorem_passed"
        )
        is True
        and degree_one_radial_tangent_oh_theorem.get("degree_one_tangent_unique")
        is True
        and degree_one_radial_tangent_oh_theorem.get(
            "same_surface_linear_tangent_premise_derived"
        )
        is False
        and degree_one_radial_tangent_oh_theorem.get("canonical_oh_identity_derived")
        is False
        and degree_one_radial_tangent_oh_theorem.get("source_higgs_pole_rows_present")
        is False,
        statuses["pr230_degree_one_radial_tangent_oh_theorem"],
    )
    taste_radial_to_source_higgs_promotion_contract = certificates[
        "pr230_taste_radial_to_source_higgs_promotion_contract"
    ]
    report(
        "pr230-taste-radial-to-source-higgs-promotion-contract-support-not-closure",
        "taste-radial-to-source-Higgs promotion contract"
        in str(statuses["pr230_taste_radial_to_source_higgs_promotion_contract"])
        and taste_radial_to_source_higgs_promotion_contract.get(
            "promotion_contract_passed"
        )
        is True
        and taste_radial_to_source_higgs_promotion_contract.get(
            "current_promotion_allowed"
        )
        is False
        and taste_radial_to_source_higgs_promotion_contract.get("proposal_allowed")
        is False
        and "same_surface_canonical_O_H_identity_absent"
        in taste_radial_to_source_higgs_promotion_contract.get(
            "current_promotion_blockers", []
        )
        and taste_radial_to_source_higgs_promotion_contract.get(
            "row_packet_status", {}
        ).get("canonical_source_higgs_rows_present")
        is False,
        statuses["pr230_taste_radial_to_source_higgs_promotion_contract"],
    )
    fms_post_degree_route_rescore = certificates[
        "pr230_fms_post_degree_route_rescore"
    ]
    report(
        "pr230-fms-post-degree-route-rescore-support-not-proof",
        "FMS post-degree route rescore"
        in str(statuses["pr230_fms_post_degree_route_rescore"])
        and fms_post_degree_route_rescore.get("proposal_allowed") is False
        and fms_post_degree_route_rescore.get(
            "fms_post_degree_route_rescore_passed"
        )
        is True
        and fms_post_degree_route_rescore.get("forbidden_firewall", {}).get(
            "used_literature_as_proof_authority"
        )
        is False
        and fms_post_degree_route_rescore.get("forbidden_firewall", {}).get(
            "used_degree_or_odd_parity_as_oh_authority"
        )
        is False,
        statuses["pr230_fms_post_degree_route_rescore"],
    )
    fms_composite_oh_conditional_theorem = certificates[
        "pr230_fms_composite_oh_conditional_theorem"
    ]
    report(
        "pr230-fms-composite-oh-conditional-support-not-proof",
        "FMS composite O_H theorem"
        in str(statuses["pr230_fms_composite_oh_conditional_theorem"])
        and fms_composite_oh_conditional_theorem.get("proposal_allowed") is False
        and fms_composite_oh_conditional_theorem.get(
            "fms_composite_oh_conditional_theorem_passed"
        )
        is True
        and fms_composite_oh_conditional_theorem.get(
            "current_closure_authority_present"
        )
        is False
        and fms_composite_oh_conditional_theorem.get("same_surface_action_absent")
        is True
        and fms_composite_oh_conditional_theorem.get("source_higgs_rows_absent")
        is True,
        statuses["pr230_fms_composite_oh_conditional_theorem"],
    )
    fms_oh_candidate_action_packet = certificates[
        "pr230_fms_oh_candidate_action_packet"
    ]
    report(
        "pr230-fms-oh-candidate-action-packet-support-not-proof",
        "FMS O_H candidate/action packet"
        in str(statuses["pr230_fms_oh_candidate_action_packet"])
        and fms_oh_candidate_action_packet.get("proposal_allowed") is False
        and fms_oh_candidate_action_packet.get(
            "fms_oh_candidate_action_packet_passed"
        )
        is True
        and fms_oh_candidate_action_packet.get("accepted_current_surface")
        is False
        and fms_oh_candidate_action_packet.get("same_surface_cl3_z3_derived")
        is False
        and fms_oh_candidate_action_packet.get("external_extension_required")
        is True
        and fms_oh_candidate_action_packet.get("closure_authorized") is False,
        statuses["pr230_fms_oh_candidate_action_packet"],
    )
    fms_source_overlap_readout_gate = certificates[
        "pr230_fms_source_overlap_readout_gate"
    ]
    report(
        "pr230-fms-source-overlap-readout-gate-support-not-proof",
        "FMS source-overlap readout gate"
        in str(statuses["pr230_fms_source_overlap_readout_gate"])
        and fms_source_overlap_readout_gate.get("proposal_allowed") is False
        and fms_source_overlap_readout_gate.get(
            "fms_source_overlap_readout_gate_passed"
        )
        is True
        and fms_source_overlap_readout_gate.get("readout_executable_now") is False
        and fms_source_overlap_readout_gate.get("strict_rows_present") is False
        and fms_source_overlap_readout_gate.get("closure_authorized") is False,
        statuses["pr230_fms_source_overlap_readout_gate"],
    )
    fms_action_adoption_minimal_cut = certificates[
        "pr230_fms_action_adoption_minimal_cut"
    ]
    report(
        "pr230-fms-action-adoption-minimal-cut-support-not-proof",
        "FMS action-adoption minimal cut"
        in str(statuses["pr230_fms_action_adoption_minimal_cut"])
        and fms_action_adoption_minimal_cut.get("proposal_allowed") is False
        and fms_action_adoption_minimal_cut.get(
            "fms_action_adoption_minimal_cut_passed"
        )
        is True
        and fms_action_adoption_minimal_cut.get("adoption_allowed_now") is False
        and fms_action_adoption_minimal_cut.get("accepted_current_surface") is False
        and fms_action_adoption_minimal_cut.get("same_surface_cl3_z3_derived")
        is False
        and fms_action_adoption_minimal_cut.get("closure_authorized") is False
        and bool(fms_action_adoption_minimal_cut.get("missing_root_vertices")),
        statuses["pr230_fms_action_adoption_minimal_cut"],
    )
    higgs_mass_source_action_bridge = certificates[
        "pr230_higgs_mass_source_action_bridge"
    ]
    report(
        "pr230-higgs-mass-source-action-bridge-support-not-proof",
        "Higgs mass-source action bridge"
        in str(statuses["pr230_higgs_mass_source_action_bridge"])
        and higgs_mass_source_action_bridge.get("proposal_allowed") is False
        and higgs_mass_source_action_bridge.get(
            "higgs_mass_source_action_bridge_passed"
        )
        is True
        and higgs_mass_source_action_bridge.get(
            "same_surface_ew_action_certificate_absent"
        )
        is True
        and higgs_mass_source_action_bridge.get("canonical_oh_absent") is True
        and higgs_mass_source_action_bridge.get("source_higgs_rows_absent") is True,
        statuses["pr230_higgs_mass_source_action_bridge"],
    )
    same_source_ew_higgs_action_ansatz_gate = certificates[
        "pr230_same_source_ew_higgs_action_ansatz_gate"
    ]
    report(
        "pr230-same-source-ew-higgs-action-ansatz-support-not-proof",
        "same-source EW/Higgs action-extension ansatz"
        in str(statuses["pr230_same_source_ew_higgs_action_ansatz_gate"])
        and same_source_ew_higgs_action_ansatz_gate.get("proposal_allowed")
        is False
        and same_source_ew_higgs_action_ansatz_gate.get(
            "same_source_ew_higgs_action_ansatz_gate_passed"
        )
        is True
        and same_source_ew_higgs_action_ansatz_gate.get(
            "current_surface_adoption_passed"
        )
        is False
        and same_source_ew_higgs_action_ansatz_gate.get(
            "future_default_certificates_written"
        )
        is False,
        statuses["pr230_same_source_ew_higgs_action_ansatz_gate"],
    )
    same_source_ew_action_adoption_attempt = certificates[
        "pr230_same_source_ew_action_adoption_attempt"
    ]
    report(
        "pr230-same-source-ew-action-adoption-attempt-blocks-ansatz-only-shortcut",
        "ansatz-only same-source EW action adoption shortcut blocked"
        in str(statuses["pr230_same_source_ew_action_adoption_attempt"])
        and same_source_ew_action_adoption_attempt.get("proposal_allowed")
        is False
        and same_source_ew_action_adoption_attempt.get(
            "same_source_ew_action_adoption_attempt_passed"
        )
        is True
        and same_source_ew_action_adoption_attempt.get("adoption_allowed_now")
        is False
        and same_source_ew_action_adoption_attempt.get(
            "accepted_action_certificate_written_by_this_attempt"
        )
        is False,
        statuses["pr230_same_source_ew_action_adoption_attempt"],
    )
    radial_spurion_sector_overlap_theorem = certificates[
        "pr230_radial_spurion_sector_overlap_theorem"
    ]
    report(
        "pr230-radial-spurion-sector-overlap-support-not-closure",
        "radial-spurion sector-overlap theorem"
        in str(statuses["pr230_radial_spurion_sector_overlap_theorem"])
        and radial_spurion_sector_overlap_theorem.get("proposal_allowed") is False
        and radial_spurion_sector_overlap_theorem.get(
            "radial_spurion_sector_overlap_theorem_passed"
        )
        is True
        and radial_spurion_sector_overlap_theorem.get(
            "current_surface_sector_overlap_identity_supplied"
        )
        is False
        and radial_spurion_sector_overlap_theorem.get(
            "current_surface_closure_authorized"
        )
        is False,
        statuses["pr230_radial_spurion_sector_overlap_theorem"],
    )
    radial_spurion_action_contract = certificates[
        "pr230_radial_spurion_action_contract"
    ]
    report(
        "pr230-radial-spurion-action-contract-support-not-closure",
        "no-independent-top-source radial-spurion action contract"
        in str(statuses["pr230_radial_spurion_action_contract"])
        and radial_spurion_action_contract.get("proposal_allowed") is False
        and radial_spurion_action_contract.get(
            "radial_spurion_action_contract_passed"
        )
        is True
        and radial_spurion_action_contract.get("current_surface_contract_satisfied")
        is False
        and radial_spurion_action_contract.get(
            "accepted_action_certificate_written"
        )
        is False,
        statuses["pr230_radial_spurion_action_contract"],
    )
    additive_source_radial_spurion_incompatibility = certificates[
        "pr230_additive_source_radial_spurion_incompatibility"
    ]
    report(
        "pr230-additive-source-radial-spurion-incompatibility-blocks-current-action",
        "current additive source is incompatible"
        in str(statuses["pr230_additive_source_radial_spurion_incompatibility"])
        and additive_source_radial_spurion_incompatibility.get("proposal_allowed")
        is False
        and additive_source_radial_spurion_incompatibility.get(
            "additive_source_radial_spurion_incompatibility_passed"
        )
        is True
        and all(
            value is False
            for value in additive_source_radial_spurion_incompatibility.get(
                "forbidden_firewall", {}
            ).values()
        ),
        statuses["pr230_additive_source_radial_spurion_incompatibility"],
    )
    additive_top_subtraction_row_contract = certificates[
        "pr230_additive_top_subtraction_row_contract"
    ]
    report(
        "pr230-additive-top-subtraction-row-contract-support-not-closure",
        "additive-top subtraction row contract"
        in str(statuses["pr230_additive_top_subtraction_row_contract"])
        and additive_top_subtraction_row_contract.get("proposal_allowed") is False
        and additive_top_subtraction_row_contract.get(
            "additive_top_subtraction_row_contract_passed"
        )
        is True
        and all(
            value is False
            for value in additive_top_subtraction_row_contract.get(
                "forbidden_firewall", {}
            ).values()
        ),
        statuses["pr230_additive_top_subtraction_row_contract"],
    )
    source_higgs_direct_pole_row_contract = certificates[
        "pr230_source_higgs_direct_pole_row_contract"
    ]
    report(
        "pr230-source-higgs-direct-pole-row-contract-support-not-closure",
        "direct source-Higgs pole-row contract"
        in str(statuses["pr230_source_higgs_direct_pole_row_contract"])
        and source_higgs_direct_pole_row_contract.get("proposal_allowed") is False
        and source_higgs_direct_pole_row_contract.get(
            "source_higgs_direct_pole_row_contract_passed"
        )
        is True
        and all(
            value is False
            for value in source_higgs_direct_pole_row_contract.get(
                "forbidden_firewall", {}
            ).values()
        ),
        statuses["pr230_source_higgs_direct_pole_row_contract"],
    )
    canonical_oh_hard_residual_equivalence_gate = certificates[
        "pr230_canonical_oh_hard_residual_equivalence_gate"
    ]
    report(
        "pr230-canonical-oh-hard-residual-equivalence-gate-blocks-current-surface",
        "canonical O_H hard residual not closed"
        in str(statuses["pr230_canonical_oh_hard_residual_equivalence_gate"])
        and canonical_oh_hard_residual_equivalence_gate.get("proposal_allowed")
        is False
        and canonical_oh_hard_residual_equivalence_gate.get(
            "canonical_oh_hard_residual_equivalence_gate_passed"
        )
        is True
        and all(
            value is False
            for value in canonical_oh_hard_residual_equivalence_gate.get(
                "forbidden_firewall", {}
            ).values()
        ),
        statuses["pr230_canonical_oh_hard_residual_equivalence_gate"],
    )
    wz_response_ratio_contract = certificates[
        "pr230_wz_response_ratio_identifiability_contract"
    ]
    report(
        "pr230-wz-response-ratio-identifiability-contract-support-not-closure",
        "WZ response-ratio identifiability contract"
        in str(statuses["pr230_wz_response_ratio_identifiability_contract"])
        and wz_response_ratio_contract.get("proposal_allowed") is False
        and wz_response_ratio_contract.get(
            "wz_response_ratio_identifiability_contract_passed"
        )
        is True
        and wz_response_ratio_contract.get("current_surface_contract_satisfied")
        is False
        and wz_response_ratio_contract.get("future_response_ratio_row_packet_present")
        is False
        and wz_response_ratio_contract.get("strict_g2_authority_present") is False
        and wz_response_ratio_contract.get("matched_covariance_authority_present")
        is False,
        statuses["pr230_wz_response_ratio_identifiability_contract"],
    )
    wz_same_source_action_minimal_cut = certificates[
        "pr230_wz_same_source_action_minimal_certificate_cut"
    ]
    report(
        "pr230-wz-same-source-action-minimal-certificate-cut-open",
        "WZ accepted same-source action minimal certificate cut"
        in str(statuses["pr230_wz_same_source_action_minimal_certificate_cut"])
        and wz_same_source_action_minimal_cut.get("proposal_allowed") is False
        and wz_same_source_action_minimal_cut.get(
            "wz_same_source_action_minimal_certificate_cut_passed"
        )
        is True
        and wz_same_source_action_minimal_cut.get(
            "current_surface_action_certificate_satisfied"
        )
        is False
        and set(wz_same_source_action_minimal_cut.get("root_certificate_cut_open", []))
        == {
            "same_surface_canonical_higgs_operator_certificate",
            "current_same_source_sector_overlap_identity",
            "wz_correlator_mass_fit_path_certificate",
        },
        statuses["pr230_wz_same_source_action_minimal_certificate_cut"],
    )
    wz_accepted_action_response_root_checkpoint = certificates[
        "pr230_wz_accepted_action_response_root_checkpoint"
    ]
    report(
        "pr230-wz-accepted-action-response-root-checkpoint-blocks-current-root",
        "WZ accepted-action response root not closed"
        in str(statuses["pr230_wz_accepted_action_response_root_checkpoint"])
        and wz_accepted_action_response_root_checkpoint.get("proposal_allowed")
        is False
        and wz_accepted_action_response_root_checkpoint.get(
            "wz_accepted_action_response_root_checkpoint_passed"
        )
        is True
        and wz_accepted_action_response_root_checkpoint.get("current_route_blocked")
        is True
        and wz_accepted_action_response_root_checkpoint.get("root_closures_found")
        == []
        and not any(
            wz_accepted_action_response_root_checkpoint.get(
                "future_artifact_presence", {}
            ).values()
        )
        and all(
            value is False
            for value in wz_accepted_action_response_root_checkpoint.get(
                "forbidden_firewall", {}
            ).values()
        ),
        statuses["pr230_wz_accepted_action_response_root_checkpoint"],
    )
    wz_physical_response_packet_intake = certificates[
        "pr230_wz_physical_response_packet_intake_checkpoint"
    ]
    report(
        "pr230-wz-physical-response-packet-intake-blocks-current-packet",
        "WZ physical-response packet not present"
        in str(statuses["pr230_wz_physical_response_packet_intake_checkpoint"])
        and wz_physical_response_packet_intake.get("proposal_allowed") is False
        and wz_physical_response_packet_intake.get(
            "wz_physical_response_packet_intake_checkpoint_passed"
        )
        is True
        and wz_physical_response_packet_intake.get("current_route_blocked")
        is True
        and wz_physical_response_packet_intake.get("production_packet_present")
        is False
        and not any(
            wz_physical_response_packet_intake.get(
                "production_roots_present", {}
            ).values()
        )
        and all(
            wz_physical_response_packet_intake.get(
                "scout_artifacts_present", {}
            ).values()
        )
        and all(
            value is False
            for value in wz_physical_response_packet_intake.get(
                "forbidden_firewall", {}
            ).values()
        ),
        statuses["pr230_wz_physical_response_packet_intake_checkpoint"],
    )
    canonical_oh_wz_common_action_cut = certificates[
        "pr230_canonical_oh_wz_common_action_cut"
    ]
    report(
        "pr230-canonical-oh-wz-common-action-cut-open",
        "canonical O_H and WZ accepted-action common-cut"
        in str(statuses["pr230_canonical_oh_wz_common_action_cut"])
        and canonical_oh_wz_common_action_cut.get("proposal_allowed") is False
        and canonical_oh_wz_common_action_cut.get("common_action_cut_passed")
        is True
        and canonical_oh_wz_common_action_cut.get(
            "common_canonical_oh_vertex_open"
        )
        is True
        and canonical_oh_wz_common_action_cut.get("aggregate_denies_proposal")
        is True
        and canonical_oh_wz_common_action_cut.get(
            "time_kernel_manifest_not_evidence"
        )
        is True,
        statuses["pr230_canonical_oh_wz_common_action_cut"],
    )
    canonical_oh_accepted_action_stretch_attempt = certificates[
        "pr230_canonical_oh_accepted_action_stretch_attempt"
    ]
    report(
        "pr230-canonical-oh-accepted-action-stretch-blocks-current-stack",
        "canonical O_H accepted-action root not derivable"
        in str(statuses["pr230_canonical_oh_accepted_action_stretch_attempt"])
        and canonical_oh_accepted_action_stretch_attempt.get("proposal_allowed")
        is False
        and canonical_oh_accepted_action_stretch_attempt.get(
            "stretch_attempt_passed"
        )
        is True
        and canonical_oh_accepted_action_stretch_attempt.get(
            "current_route_blocked"
        )
        is True
        and canonical_oh_accepted_action_stretch_attempt.get("root_closures_found")
        == [],
        statuses["pr230_canonical_oh_accepted_action_stretch_attempt"],
    )
    source_higgs_bridge_aperture_checkpoint = certificates[
        "pr230_source_higgs_bridge_aperture_checkpoint"
    ]
    source_higgs_aperture_rows = source_higgs_bridge_aperture_checkpoint.get(
        "two_source_rows", {}
    )
    source_higgs_aperture_ready = source_higgs_aperture_rows.get("ready_chunks")
    source_higgs_aperture_combiner_boundary = (
        isinstance(source_higgs_aperture_ready, int)
        and 42 <= source_higgs_aperture_ready <= 63
        and source_higgs_aperture_rows.get("present_chunks")
        == source_higgs_aperture_ready
        and source_higgs_aperture_rows.get("expected_chunks") == 63
        and (
            (
                source_higgs_aperture_rows.get("combined_rows_written") is False
                and source_higgs_aperture_ready < 63
            )
            or (
                source_higgs_aperture_rows.get("combined_rows_written") is True
                and source_higgs_aperture_ready == 63
            )
        )
    )
    source_higgs_closure_future_absent = not any(
        value
        for name, value in source_higgs_bridge_aperture_checkpoint.get(
            "future_artifact_presence", {}
        ).items()
        if name != "two_source_combined_rows"
    )
    report(
        "pr230-source-higgs-bridge-aperture-checkpoint-support-not-closure",
        "source-Higgs bridge aperture checkpoint"
        in str(statuses["pr230_source_higgs_bridge_aperture_checkpoint"])
        and source_higgs_bridge_aperture_checkpoint.get("proposal_allowed")
        is False
        and source_higgs_bridge_aperture_checkpoint.get(
            "source_higgs_bridge_aperture_checkpoint_passed"
        )
        is True
        and source_higgs_bridge_aperture_checkpoint.get(
            "current_surface_closure_satisfied"
        )
        is False
        and source_higgs_aperture_combiner_boundary
        and source_higgs_closure_future_absent
        and all(
            value is False
            for value in source_higgs_bridge_aperture_checkpoint.get(
                "forbidden_firewall", {}
            ).values()
        ),
        statuses["pr230_source_higgs_bridge_aperture_checkpoint"],
    )
    fresh_artifact_intake_checkpoint = certificates[
        "pr230_fresh_artifact_intake_checkpoint"
    ]
    report(
        "pr230-fresh-artifact-intake-checkpoint-no-new-artifact",
        "fresh-artifact intake checkpoint"
        in str(statuses["pr230_fresh_artifact_intake_checkpoint"])
        and fresh_artifact_intake_checkpoint.get("proposal_allowed") is False
        and fresh_artifact_intake_checkpoint.get("consumed_committed_pr_head_only")
        is True
        and fresh_artifact_intake_checkpoint.get("live_chunk_worker", {}).get(
            "touched"
        )
        is False
        and fresh_artifact_intake_checkpoint.get("live_chunk_worker", {}).get(
            "inspected_active_output"
        )
        is False
        and fresh_artifact_intake_checkpoint.get("checks", {}).get(
            "no_closure_artifact_present"
        )
        is True
        and fresh_artifact_intake_checkpoint.get("source_higgs_route", {}).get(
            "closure_artifact_present"
        )
        is False
        and fresh_artifact_intake_checkpoint.get("wz_route", {}).get(
            "strict_packet_present"
        )
        is False
        and all(
            fresh_artifact_intake_checkpoint.get("checks", {}).values()
        ),
        statuses["pr230_fresh_artifact_intake_checkpoint"],
    )
    block23_remote_candidate_intake = certificates[
        "pr230_block23_remote_candidate_intake"
    ]
    report(
        "pr230-block23-remote-candidate-intake-no-admissible-packet",
        "block23 remote-candidate intake checkpoint"
        in str(statuses["pr230_block23_remote_candidate_intake"])
        and block23_remote_candidate_intake.get("proposal_allowed") is False
        and block23_remote_candidate_intake.get("live_chunk_worker", {}).get(
            "touched"
        )
        is False
        and block23_remote_candidate_intake.get("live_chunk_worker", {}).get(
            "inspected_active_output"
        )
        is False
        and block23_remote_candidate_intake.get("checks", {}).get(
            "no-candidate-ref-has-strict-source-packet"
        )
        is True
        and block23_remote_candidate_intake.get("checks", {}).get(
            "no-candidate-ref-has-strict-wz-packet"
        )
        is True
        and block23_remote_candidate_intake.get("checks", {}).get(
            "no-candidate-ref-has-strict-neutral-packet"
        )
        is True
        and block23_remote_candidate_intake.get("checks", {}).get(
            "no-admissible-remote-required-paths-found"
        )
        is True
        and block23_remote_candidate_intake.get("checks", {}).get(
            "forbidden-firewall-clean"
        )
        is True,
        statuses["pr230_block23_remote_candidate_intake"],
    )
    block24_queue_pivot_admission = certificates[
        "pr230_block24_queue_pivot_admission"
    ]
    report(
        "pr230-block24-queue-pivot-admission-no-route-admitted",
        "block24 queue-pivot admission checkpoint"
        in str(statuses["pr230_block24_queue_pivot_admission"])
        and block24_queue_pivot_admission.get("proposal_allowed") is False
        and block24_queue_pivot_admission.get("live_chunk_worker", {}).get(
            "touched"
        )
        is False
        and block24_queue_pivot_admission.get("live_chunk_worker", {}).get(
            "inspected_active_output"
        )
        is False
        and block24_queue_pivot_admission.get("checks", {}).get(
            "only-block23-checkpoint-since-last-scanned-physics-head"
        )
        is True
        and block24_queue_pivot_admission.get("checks", {}).get(
            "queue-rank1-source-higgs-not-admitted"
        )
        is True
        and block24_queue_pivot_admission.get("checks", {}).get(
            "queue-rank2-wz-not-admitted"
        )
        is True
        and block24_queue_pivot_admission.get("checks", {}).get(
            "queue-rank3-neutral-h3h4-not-admitted"
        )
        is True
        and block24_queue_pivot_admission.get("checks", {}).get(
            "chunk063-and-combined-rows-not-committed"
        )
        is True
        and block24_queue_pivot_admission.get("checks", {}).get(
            "forbidden-firewall-clean"
        )
        is True,
        statuses["pr230_block24_queue_pivot_admission"],
    )
    block25_post_block24_landed = certificates[
        "pr230_block25_post_block24_landed"
    ]
    report(
        "pr230-block25-post-block24-landed-no-route-admitted",
        "block25 post-block24 landed checkpoint"
        in str(statuses["pr230_block25_post_block24_landed"])
        and block25_post_block24_landed.get("proposal_allowed") is False
        and block25_post_block24_landed.get("live_chunk_worker", {}).get(
            "touched"
        )
        is False
        and block25_post_block24_landed.get("live_chunk_worker", {}).get(
            "inspected_active_output"
        )
        is False
        and block25_post_block24_landed.get("checks", {}).get(
            "only-block24-checkpoint-since-block24-input-head"
        )
        is True
        and block25_post_block24_landed.get("checks", {}).get(
            "queue-rank1-source-higgs-not-admitted"
        )
        is True
        and block25_post_block24_landed.get("checks", {}).get(
            "queue-rank2-wz-not-admitted"
        )
        is True
        and block25_post_block24_landed.get("checks", {}).get(
            "queue-rank3-neutral-h3h4-not-admitted"
        )
        is True
        and block25_post_block24_landed.get("checks", {}).get(
            "chunk063-and-combined-rows-not-committed"
        )
        is True
        and block25_post_block24_landed.get("checks", {}).get(
            "forbidden-firewall-clean"
        )
        is True,
        statuses["pr230_block25_post_block24_landed"],
    )
    block26_post_block25_landed = certificates[
        "pr230_block26_post_block25_landed"
    ]
    report(
        "pr230-block26-post-block25-landed-no-route-admitted",
        "block26 post-block25 landed checkpoint"
        in str(statuses["pr230_block26_post_block25_landed"])
        and block26_post_block25_landed.get("proposal_allowed") is False
        and block26_post_block25_landed.get("live_chunk_worker", {}).get(
            "touched"
        )
        is False
        and block26_post_block25_landed.get("live_chunk_worker", {}).get(
            "inspected_active_output"
        )
        is False
        and block26_post_block25_landed.get("checks", {}).get(
            "only-block25-checkpoint-since-block25-input-head"
        )
        is True
        and block26_post_block25_landed.get("checks", {}).get(
            "queue-rank1-source-higgs-not-admitted"
        )
        is True
        and block26_post_block25_landed.get("checks", {}).get(
            "queue-rank2-wz-not-admitted"
        )
        is True
        and block26_post_block25_landed.get("checks", {}).get(
            "queue-rank3-neutral-h3h4-not-admitted"
        )
        is True
        and block26_post_block25_landed.get("checks", {}).get(
            "chunk063-and-combined-rows-not-committed"
        )
        is True
        and block26_post_block25_landed.get("checks", {}).get(
            "forbidden-firewall-clean"
        )
        is True,
        statuses["pr230_block26_post_block25_landed"],
    )
    block27_post_block26_landed = certificates[
        "pr230_block27_post_block26_landed"
    ]
    report(
        "pr230-block27-post-block26-landed-no-route-admitted",
        "block27 post-block26 landed checkpoint"
        in str(statuses["pr230_block27_post_block26_landed"])
        and block27_post_block26_landed.get("proposal_allowed") is False
        and block27_post_block26_landed.get("live_chunk_worker", {}).get(
            "touched"
        )
        is False
        and block27_post_block26_landed.get("live_chunk_worker", {}).get(
            "inspected_active_output"
        )
        is False
        and block27_post_block26_landed.get("checks", {}).get(
            "only-block26-checkpoint-since-block26-input-head"
        )
        is True
        and block27_post_block26_landed.get("checks", {}).get(
            "queue-rank1-source-higgs-not-admitted"
        )
        is True
        and block27_post_block26_landed.get("checks", {}).get(
            "queue-rank2-wz-not-admitted"
        )
        is True
        and block27_post_block26_landed.get("checks", {}).get(
            "queue-rank3-neutral-h3h4-not-admitted"
        )
        is True
        and block27_post_block26_landed.get("checks", {}).get(
            "chunk063-and-combined-rows-not-committed"
        )
        is True
        and block27_post_block26_landed.get("checks", {}).get(
            "forbidden-firewall-clean"
        )
        is True,
        statuses["pr230_block27_post_block26_landed"],
    )
    block28_degree_one_oh_support_intake = certificates[
        "pr230_block28_degree_one_oh_support_intake"
    ]
    report(
        "pr230-block28-degree-one-oh-support-intake-not-closure",
        "block28 degree-one O_H support intake"
        in str(statuses["pr230_block28_degree_one_oh_support_intake"])
        and block28_degree_one_oh_support_intake.get("proposal_allowed") is False
        and block28_degree_one_oh_support_intake.get("live_chunk_worker", {}).get(
            "touched"
        )
        is False
        and block28_degree_one_oh_support_intake.get("live_chunk_worker", {}).get(
            "inspected_active_output"
        )
        is False
        and block28_degree_one_oh_support_intake.get("checks", {}).get(
            "only-block27-checkpoint-since-block27-input-head"
        )
        is True
        and block28_degree_one_oh_support_intake.get("checks", {}).get(
            "degree-one-oh-support-loaded"
        )
        is True
        and block28_degree_one_oh_support_intake.get("checks", {}).get(
            "degree-one-action-premise-still-missing"
        )
        is True
        and block28_degree_one_oh_support_intake.get("checks", {}).get(
            "source-higgs-route-not-admitted"
        )
        is True
        and block28_degree_one_oh_support_intake.get("checks", {}).get(
            "wz-route-not-admitted"
        )
        is True
        and block28_degree_one_oh_support_intake.get("checks", {}).get(
            "neutral-h3h4-route-not-admitted"
        )
        is True
        and block28_degree_one_oh_support_intake.get("checks", {}).get(
            "forbidden-firewall-clean"
        )
        is True,
        statuses["pr230_block28_degree_one_oh_support_intake"],
    )
    block29_post_block28_wz_pivot_admission = certificates[
        "pr230_block29_post_block28_wz_pivot_admission"
    ]
    report(
        "pr230-block29-post-block28-wz-pivot-not-admitted",
        "block29 post-block28 W/Z pivot admission checkpoint"
        in str(statuses["pr230_block29_post_block28_wz_pivot_admission"])
        and block29_post_block28_wz_pivot_admission.get("proposal_allowed")
        is False
        and block29_post_block28_wz_pivot_admission.get(
            "live_chunk_worker", {}
        ).get("touched")
        is False
        and block29_post_block28_wz_pivot_admission.get(
            "live_chunk_worker", {}
        ).get("inspected_active_output")
        is False
        and block29_post_block28_wz_pivot_admission.get("checks", {}).get(
            "only-block28-support-since-block28-input-head"
        )
        is True
        and block29_post_block28_wz_pivot_admission.get("checks", {}).get(
            "block28-exact-support-no-closure"
        )
        is True
        and block29_post_block28_wz_pivot_admission.get("checks", {}).get(
            "source-higgs-route-blocked-after-block28"
        )
        is True
        and block29_post_block28_wz_pivot_admission.get("checks", {}).get(
            "wz-pivot-selected-after-source-higgs-block"
        )
        is True
        and block29_post_block28_wz_pivot_admission.get("checks", {}).get(
            "wz-pivot-not-admitted-without-required-packet"
        )
        is True
        and block29_post_block28_wz_pivot_admission.get("checks", {}).get(
            "forbidden-firewall-clean"
        )
        is True,
        statuses["pr230_block29_post_block28_wz_pivot_admission"],
    )
    block30_full_approach_review = certificates[
        "pr230_block30_full_approach_assumptions_elon_lit_math_bridge_review"
    ]
    report(
        "pr230-block30-full-approach-review-not-closure",
        "full-approach exercise and repo-bridge review"
        in str(
            statuses[
                "pr230_block30_full_approach_assumptions_elon_lit_math_bridge_review"
            ]
        )
        and block30_full_approach_review.get("proposal_allowed") is False
        and block30_full_approach_review.get("bare_retained_allowed") is False
        and block30_full_approach_review.get(
            "audit_required_before_effective_retained"
        )
        is True
        and block30_full_approach_review.get("fails") == 0
        and len(block30_full_approach_review.get("assumptions_exercise", [])) >= 16
        and len(block30_full_approach_review.get("literature_search", [])) >= 5
        and len(block30_full_approach_review.get("math_search", [])) >= 6
        and len(block30_full_approach_review.get("repo_bridge_cross_check", [])) >= 10
        and block30_full_approach_review.get("elon_exercise", {}).get(
            "canonical_skill_section_found"
        )
        is False
        and len(
            block30_full_approach_review.get("elon_exercise", {}).get(
                "zeroth_principles_chain", []
            )
        )
        >= 5
        and all(
            value is True
            for value in block30_full_approach_review.get(
                "parent_presence", {}
            ).values()
        ),
        statuses[
            "pr230_block30_full_approach_assumptions_elon_lit_math_bridge_review"
        ],
    )
    block35_post_block34_bridge_admission = certificates[
        "pr230_block35_post_block34_physical_bridge_admission"
    ]
    report(
        "pr230-block35-post-block34-bridge-admission-not-closure",
        "block35 post-block34 physical-bridge admission checkpoint"
        in str(statuses["pr230_block35_post_block34_physical_bridge_admission"])
        and block35_post_block34_bridge_admission.get("proposal_allowed") is False
        and block35_post_block34_bridge_admission.get("bare_retained_allowed")
        is False
        and block35_post_block34_bridge_admission.get(
            "block35_post_block34_physical_bridge_admission_checkpoint_passed"
        )
        is True
        and block35_post_block34_bridge_admission.get("live_chunk_worker", {}).get(
            "touched"
        )
        is False
        and block35_post_block34_bridge_admission.get("live_chunk_worker", {}).get(
            "inspected_active_output"
        )
        is False
        and block35_post_block34_bridge_admission.get("checks", {}).get(
            "post-block30-inputs-support-only"
        )
        is True
        and block35_post_block34_bridge_admission.get("checks", {}).get(
            "chunk063-package-committed-support-only"
        )
        is True
        and block35_post_block34_bridge_admission.get("checks", {}).get(
            "promotion-contract-committed-support-only"
        )
        is True
        and block35_post_block34_bridge_admission.get("checks", {}).get(
            "os-transfer-alias-firewall-committed-support-only"
        )
        is True
        and block35_post_block34_bridge_admission.get("checks", {}).get(
            "additive-top-support-committed-support-only"
        )
        is True
        and block35_post_block34_bridge_admission.get("checks", {}).get(
            "source-higgs-physical-bridge-not-admitted"
        )
        is True
        and block35_post_block34_bridge_admission.get("checks", {}).get(
            "wz-physical-response-not-admitted"
        )
        is True
        and block35_post_block34_bridge_admission.get("checks", {}).get(
            "neutral-h3h4-not-admitted"
        )
        is True
        and block35_post_block34_bridge_admission.get("checks", {}).get(
            "forbidden-firewall-clean"
        )
        is True,
        statuses["pr230_block35_post_block34_physical_bridge_admission"],
    )
    post_fms_source_overlap_necessity_gate = certificates[
        "pr230_post_fms_source_overlap_necessity_gate"
    ]
    report(
        "pr230-post-fms-source-overlap-necessity-blocks-current-inference",
        "post-FMS source-overlap not derivable"
        in str(statuses["pr230_post_fms_source_overlap_necessity_gate"])
        and post_fms_source_overlap_necessity_gate.get("proposal_allowed")
        is False
        and post_fms_source_overlap_necessity_gate.get(
            "post_fms_source_overlap_necessity_gate_passed"
        )
        is True
        and post_fms_source_overlap_necessity_gate.get(
            "current_source_overlap_authority_present"
        )
        is False
        and post_fms_source_overlap_necessity_gate.get(
            "two_source_rows_are_c_sx_not_c_sH"
        )
        is True,
        statuses["pr230_post_fms_source_overlap_necessity_gate"],
    )
    source_higgs_overlap_kappa_contract = certificates[
        "pr230_source_higgs_overlap_kappa_contract"
    ]
    report(
        "pr230-source-higgs-overlap-kappa-contract-support-not-proof",
        "source-Higgs overlap-kappa row contract"
        in str(statuses["pr230_source_higgs_overlap_kappa_contract"])
        and source_higgs_overlap_kappa_contract.get("proposal_allowed") is False
        and source_higgs_overlap_kappa_contract.get(
            "source_higgs_overlap_kappa_contract_passed"
        )
        is True
        and source_higgs_overlap_kappa_contract.get("current_blockers", {}).get(
            "source_higgs_row_packet_absent"
        )
        is True
        and source_higgs_overlap_kappa_contract.get("forbidden_firewall", {}).get(
            "set_kappa_s_equal_one"
        )
        is False,
        statuses["pr230_source_higgs_overlap_kappa_contract"],
    )
    two_source_chunks = {
        idx: certificates[
            f"pr230_two_source_taste_radial_chunk{idx:03d}_checkpoint"
        ]
        for idx in range(1, 11)
    }
    for idx, two_source_chunk in two_source_chunks.items():
        status_key = f"pr230_two_source_taste_radial_chunk{idx:03d}_checkpoint"
        report(
            f"pr230-two-source-taste-radial-chunk{idx:03d}-checkpoint-not-closure",
            f"two-source taste-radial chunk{idx:03d}" in str(statuses[status_key])
            and two_source_chunk.get("checkpoint_passed") is True
            and two_source_chunk.get("completed") is True
            and two_source_chunk.get("proposal_allowed") is False
            and two_source_chunk.get("chunk_summary", {}).get(
                "pole_residue_rows_count"
            )
            == 0,
            statuses[status_key],
        )
    action_first_route_completion = certificates["pr230_action_first_route_completion"]
    report(
        "pr230-action-first-route-current-surface-closed",
        "action-first O_H/C_sH/C_HH route not complete on current PR230 surface"
        in str(statuses["pr230_action_first_route_completion"])
        and action_first_route_completion.get("proposal_allowed") is False
        and action_first_route_completion.get("action_first_route_completion_passed")
        is True,
        statuses["pr230_action_first_route_completion"],
    )
    wz_response_route_completion = certificates["pr230_wz_response_route_completion"]
    report(
        "pr230-wz-response-route-current-surface-closed",
        "WZ same-source response route not complete on current PR230 surface"
        in str(statuses["pr230_wz_response_route_completion"])
        and wz_response_route_completion.get("proposal_allowed") is False
        and wz_response_route_completion.get("wz_response_route_completion_passed")
        is True,
        statuses["pr230_wz_response_route_completion"],
    )
    schur_route_completion = certificates["pr230_schur_route_completion"]
    report(
        "pr230-schur-route-current-surface-closed",
        "strict Schur A/B/C route not complete"
        in str(statuses["pr230_schur_route_completion"])
        and schur_route_completion.get("proposal_allowed") is False
        and schur_route_completion.get("schur_route_completion_passed") is True,
        statuses["pr230_schur_route_completion"],
    )
    neutral_primitive_route_completion = certificates[
        "pr230_neutral_primitive_route_completion"
    ]
    report(
        "pr230-neutral-primitive-route-current-surface-closed",
        "neutral primitive-rank-one route not complete on current PR230 surface"
        in str(statuses["pr230_neutral_primitive_route_completion"])
        and neutral_primitive_route_completion.get("proposal_allowed") is False
        and neutral_primitive_route_completion.get(
            "neutral_primitive_route_completion_passed"
        )
        is True,
        statuses["pr230_neutral_primitive_route_completion"],
    )
    neutral_primitive_h3h4_aperture_checkpoint = certificates[
        "pr230_neutral_primitive_h3h4_aperture_checkpoint"
    ]
    neutral_h3h4_rows = neutral_primitive_h3h4_aperture_checkpoint.get(
        "two_source_rows", {}
    )
    neutral_h3h4_diagnostics = neutral_h3h4_rows.get("diagnostics", {})
    neutral_h3h4_ready_chunks = neutral_h3h4_rows.get("ready_chunks")
    neutral_h3h4_current_prefix = (
        isinstance(neutral_h3h4_ready_chunks, int)
        and neutral_h3h4_ready_chunks >= 44
        and neutral_h3h4_rows.get("present_chunks") == neutral_h3h4_ready_chunks
        and neutral_h3h4_rows.get("expected_chunks") == 63
        and (
            (
                neutral_h3h4_rows.get("combined_rows_written") is False
                and neutral_h3h4_ready_chunks < 63
            )
            or (
                neutral_h3h4_rows.get("combined_rows_written") is True
                and neutral_h3h4_ready_chunks == 63
            )
        )
        and neutral_h3h4_diagnostics.get("chunk_counts_seen")
        == [neutral_h3h4_ready_chunks]
    )
    report(
        "pr230-neutral-primitive-h3h4-aperture-support-not-closure",
        "neutral primitive H3/H4 aperture checkpoint"
        in str(statuses["pr230_neutral_primitive_h3h4_aperture_checkpoint"])
        and neutral_primitive_h3h4_aperture_checkpoint.get("proposal_allowed")
        is False
        and neutral_primitive_h3h4_aperture_checkpoint.get(
            "neutral_primitive_h3h4_aperture_checkpoint_passed"
        )
        is True
        and neutral_primitive_h3h4_aperture_checkpoint.get(
            "current_surface_closure_satisfied"
        )
        is False
        and neutral_h3h4_current_prefix
        and neutral_h3h4_diagnostics.get("finite_rows_rank_one_flat") is False
        and not any(
            neutral_primitive_h3h4_aperture_checkpoint.get(
                "future_artifact_presence", {}
            ).values()
        )
        and all(
            value is False
            for value in neutral_primitive_h3h4_aperture_checkpoint.get(
                "forbidden_firewall", {}
            ).values()
        ),
        statuses["pr230_neutral_primitive_h3h4_aperture_checkpoint"],
    )
    oh_bridge_candidate_portfolio = certificates["pr230_oh_bridge_candidate_portfolio"]
    report(
        "pr230-oh-bridge-first-principles-candidate-portfolio-open",
        "first-principles O_H bridge positive-candidate portfolio"
        in str(statuses["pr230_oh_bridge_candidate_portfolio"])
        and oh_bridge_candidate_portfolio.get("proposal_allowed") is False
        and oh_bridge_candidate_portfolio.get("candidate_portfolio_passed") is True
        and oh_bridge_candidate_portfolio.get("candidate_count") == 5,
        statuses["pr230_oh_bridge_candidate_portfolio"],
    )
    same_surface_neutral_multiplicity_gate = certificates[
        "pr230_same_surface_neutral_multiplicity_one_gate"
    ]
    report(
        "pr230-same-surface-neutral-multiplicity-one-gate-rejects-current-surface",
        "same-surface neutral multiplicity-one artifact intake gate"
        in str(statuses["pr230_same_surface_neutral_multiplicity_one_gate"])
        and same_surface_neutral_multiplicity_gate.get("proposal_allowed") is False
        and same_surface_neutral_multiplicity_gate.get("candidate_accepted") is False,
        statuses["pr230_same_surface_neutral_multiplicity_one_gate"],
    )
    os_transfer_kernel_artifact_gate = certificates[
        "pr230_os_transfer_kernel_artifact_gate"
    ]
    report(
        "pr230-os-transfer-kernel-artifact-absent",
        "OS transfer-kernel artifact absent"
        in str(statuses["pr230_os_transfer_kernel_artifact_gate"])
        and os_transfer_kernel_artifact_gate.get("proposal_allowed") is False
        and os_transfer_kernel_artifact_gate.get("os_transfer_kernel_artifact_present")
        is False
        and os_transfer_kernel_artifact_gate.get("same_surface_transfer_or_gevp_present")
        is False,
        statuses["pr230_os_transfer_kernel_artifact_gate"],
    )
    source_higgs_time_kernel_harness_extension_gate = certificates[
        "pr230_source_higgs_time_kernel_harness_extension_gate"
    ]
    report(
        "pr230-source-higgs-time-kernel-harness-support-only",
        "source-Higgs time-kernel harness"
        in str(statuses["pr230_source_higgs_time_kernel_harness_extension_gate"])
        and source_higgs_time_kernel_harness_extension_gate.get("proposal_allowed")
        is False
        and source_higgs_time_kernel_harness_extension_gate.get("contract", {}).get(
            "adds_default_off_time_kernel_rows"
        )
        is True
        and source_higgs_time_kernel_harness_extension_gate.get("contract", {}).get(
            "selected_mass_only"
        )
        is True
        and source_higgs_time_kernel_harness_extension_gate.get(
            "used_as_physical_yukawa_readout"
        )
        is False,
        statuses["pr230_source_higgs_time_kernel_harness_extension_gate"],
    )
    source_higgs_time_kernel_gevp_contract = certificates[
        "pr230_source_higgs_time_kernel_gevp_contract"
    ]
    report(
        "pr230-source-higgs-time-kernel-gevp-contract-support-only",
        "source-Higgs time-kernel GEVP contract"
        in str(statuses["pr230_source_higgs_time_kernel_gevp_contract"])
        and source_higgs_time_kernel_gevp_contract.get("proposal_allowed") is False
        and source_higgs_time_kernel_gevp_contract.get(
            "formal_gevp_diagnostic", {}
        ).get("available")
        is True
        and source_higgs_time_kernel_gevp_contract.get(
            "physical_pole_extraction_accepted"
        )
        is False,
        statuses["pr230_source_higgs_time_kernel_gevp_contract"],
    )
    source_higgs_time_kernel_production_manifest = certificates[
        "pr230_source_higgs_time_kernel_production_manifest"
    ]
    report(
        "pr230-source-higgs-time-kernel-production-manifest-not-evidence",
        "source-Higgs time-kernel production manifest"
        in str(statuses["pr230_source_higgs_time_kernel_production_manifest"])
        and source_higgs_time_kernel_production_manifest.get("proposal_allowed")
        is False
        and source_higgs_time_kernel_production_manifest.get(
            "closure_launch_authorized_now"
        )
        is False
        and source_higgs_time_kernel_production_manifest.get(
            "support_launch_authorized_now"
        )
        is False
        and source_higgs_time_kernel_production_manifest.get(
            "operator_certificate_is_canonical_oh"
        )
        is False
        and source_higgs_time_kernel_production_manifest.get(
            "time_kernel_schema_version"
        )
        == "source_higgs_time_kernel_v1"
        and source_higgs_time_kernel_production_manifest.get("chunk_count") == 63,
        statuses["pr230_source_higgs_time_kernel_production_manifest"],
    )
    fms_literature_source_overlap_intake = certificates[
        "pr230_fms_literature_source_overlap_intake"
    ]
    report(
        "pr230-fms-literature-source-overlap-intake-non-authority",
        "FMS literature does not supply PR230 source-overlap"
        in str(statuses["pr230_fms_literature_source_overlap_intake"])
        and fms_literature_source_overlap_intake.get("proposal_allowed") is False
        and fms_literature_source_overlap_intake.get("literature_bridge_scope")
        == "non_derivation_context_only"
        and fms_literature_source_overlap_intake.get("current_blockers", {}).get(
            "canonical_oh_absent"
        )
        is True
        and fms_literature_source_overlap_intake.get("current_blockers", {}).get(
            "source_higgs_rows_absent"
        )
        is True,
        statuses["pr230_fms_literature_source_overlap_intake"],
    )
    schur_higher_shell_contract = certificates[
        "pr230_schur_higher_shell_production_contract"
    ]
    report(
        "pr230-schur-higher-shell-production-contract-not-evidence",
        "higher-shell Schur scalar-LSZ production contract"
        in str(statuses["pr230_schur_higher_shell_production_contract"])
        and schur_higher_shell_contract.get("proposal_allowed") is False
        and schur_higher_shell_contract.get(
            "higher_shell_schur_production_contract_passed"
        )
        is True
        and schur_higher_shell_contract.get("launch_allowed_now") is False
        and schur_higher_shell_contract.get(
            "current_four_mode_campaign_must_remain_unmixed"
        )
        is True,
        statuses["pr230_schur_higher_shell_production_contract"],
    )
    report(
        "pr230-negative-route-applicability-review-preserves-reopen",
        "negative-route applicability review passed"
        in str(statuses["pr230_negative_route_applicability_review"])
        and certificates["pr230_negative_route_applicability_review"].get(
            "proposal_allowed"
        )
        is False
        and certificates["pr230_negative_route_applicability_review"].get(
            "negative_results_are_current_surface_blockers_only"
        )
        is True
        and certificates["pr230_negative_route_applicability_review"].get(
            "future_reopen_paths_preserved"
        )
        is True
        and certificates["pr230_negative_route_applicability_review"].get(
            "no_retained_negative_overclaim"
        )
        is True,
        statuses["pr230_negative_route_applicability_review"],
    )
    report(
        "pr230-derived-bridge-rank-one-attempt-blocks-current-source-only-closure",
        "derived rank-one bridge not closed"
        in str(statuses["pr230_derived_bridge_rank_one_closure_attempt"])
        and certificates["pr230_derived_bridge_rank_one_closure_attempt"].get(
            "proposal_allowed"
        )
        is False
        and certificates["pr230_derived_bridge_rank_one_closure_attempt"].get(
            "derived_bridge_closure_passed"
        )
        is False
        and certificates["pr230_derived_bridge_rank_one_closure_attempt"].get(
            "exact_negative_boundary_passed"
        )
        is True,
        statuses["pr230_derived_bridge_rank_one_closure_attempt"],
    )
    report(
        "pr230-source-sector-pattern-transfer-relevant-not-closure",
        "source-sector pattern is relevant"
        in str(statuses["pr230_source_sector_pattern_transfer_gate"])
        and certificates["pr230_source_sector_pattern_transfer_gate"].get(
            "proposal_allowed"
        )
        is False
        and certificates["pr230_source_sector_pattern_transfer_gate"].get(
            "approach_relevant"
        )
        is True
        and certificates["pr230_source_sector_pattern_transfer_gate"].get(
            "direct_closure_available"
        )
        is False,
        statuses["pr230_source_sector_pattern_transfer_gate"],
    )
    report(
        "pr230-det-positivity-bridge-intake-relevant-not-closure",
        "determinant positivity is useful"
        in str(statuses["pr230_det_positivity_bridge_intake_gate"])
        and certificates["pr230_det_positivity_bridge_intake_gate"].get(
            "proposal_allowed"
        )
        is False
        and certificates["pr230_det_positivity_bridge_intake_gate"].get(
            "determinant_bridge_closes_pr230"
        )
        is False
        and certificates["pr230_det_positivity_bridge_intake_gate"].get(
            "intake_gate_passed"
        )
        is True,
        statuses["pr230_det_positivity_bridge_intake_gate"],
    )
    report(
        "pr230-reflection-det-primitive-upgrade-blocks-combined-positivity-shortcut",
        "reflection plus determinant positivity"
        in str(statuses["pr230_reflection_det_primitive_upgrade_gate"])
        and certificates["pr230_reflection_det_primitive_upgrade_gate"].get(
            "proposal_allowed"
        )
        is False
        and certificates["pr230_reflection_det_primitive_upgrade_gate"].get(
            "primitive_upgrade_passed"
        )
        is False
        and certificates["pr230_reflection_det_primitive_upgrade_gate"].get(
            "exact_negative_boundary_passed"
        )
        is True,
        statuses["pr230_reflection_det_primitive_upgrade_gate"],
    )
    report(
        "pr230-invariant-ring-oh-certificate-attempt-blocks-current-surface",
        "invariant-ring O_H certificate attempt blocked"
        in str(statuses["pr230_invariant_ring_oh_certificate_attempt"])
        and certificates["pr230_invariant_ring_oh_certificate_attempt"].get(
            "proposal_allowed"
        )
        is False
        and certificates["pr230_invariant_ring_oh_certificate_attempt"].get(
            "invariant_ring_certificate_passed"
        )
        is False
        and certificates["pr230_invariant_ring_oh_certificate_attempt"].get(
            "canonical_oh_certificate_written"
        )
        is False
        and certificates["pr230_invariant_ring_oh_certificate_attempt"].get(
            "future_file_presence", {}
        ).get("canonical_oh_certificate")
        is False,
        statuses["pr230_invariant_ring_oh_certificate_attempt"],
    )
    report(
        "pr230-gns-source-higgs-flat-extension-blocks-source-only-projection",
        "GNS source-Higgs flat-extension attempt"
        in str(statuses["pr230_gns_source_higgs_flat_extension_attempt"])
        and certificates["pr230_gns_source_higgs_flat_extension_attempt"].get(
            "proposal_allowed"
        )
        is False
        and certificates["pr230_gns_source_higgs_flat_extension_attempt"].get(
            "gns_flat_extension_passed"
        )
        is False
        and certificates["pr230_gns_source_higgs_flat_extension_attempt"].get(
            "gns_certificate_written"
        )
        is False
        and not any(
            certificates["pr230_gns_source_higgs_flat_extension_attempt"].get(
                "future_file_presence", {}
            ).values()
        ),
        statuses["pr230_gns_source_higgs_flat_extension_attempt"],
    )
    report(
        "canonical-higgs-operator-realization-gate-not-passed",
        "canonical-Higgs operator realization gate not passed"
        in str(statuses["canonical_higgs_operator_realization_gate"]),
        statuses["canonical_higgs_operator_realization_gate"],
    )
    report(
        "canonical-higgs-operator-certificate-gate-blocks",
        "canonical-Higgs operator certificate absent"
        in str(statuses["canonical_higgs_operator_certificate_gate"])
        and certificates["canonical_higgs_operator_certificate_gate"].get("candidate_present") is False
        and certificates["canonical_higgs_operator_certificate_gate"].get("candidate_valid") is False,
        statuses["canonical_higgs_operator_certificate_gate"],
    )
    report(
        "canonical-higgs-operator-semantic-firewall-not-closure",
        "canonical-Higgs operator semantic firewall passed"
        in str(statuses["canonical_higgs_operator_semantic_firewall"])
        and certificates["canonical_higgs_operator_semantic_firewall"].get("proposal_allowed") is False,
        statuses["canonical_higgs_operator_semantic_firewall"],
    )
    report(
        "canonical-higgs-repo-authority-audit-blocks-hidden-oh",
        "repo-wide canonical-Higgs O_H authority audit"
        in str(statuses["canonical_higgs_repo_authority_audit"])
        and certificates["canonical_higgs_repo_authority_audit"].get("proposal_allowed") is False
        and certificates["canonical_higgs_repo_authority_audit"].get("repo_authority_found") is False
        and certificates["canonical_higgs_repo_authority_audit"].get("exact_negative_boundary_passed") is True,
        statuses["canonical_higgs_repo_authority_audit"],
    )
    report(
        "cross-lane-oh-authority-audit-blocks-adjacent-imports",
        "cross-lane O_H authority audit" in str(statuses["cross_lane_oh_authority_audit"])
        and certificates["cross_lane_oh_authority_audit"].get("proposal_allowed") is False
        and certificates["cross_lane_oh_authority_audit"].get("repo_cross_lane_authority_found") is False
        and certificates["cross_lane_oh_authority_audit"].get("cross_lane_oh_authority_audit_passed") is True,
        statuses["cross_lane_oh_authority_audit"],
    )
    report(
        "sm-one-higgs-oh-import-boundary-blocks-shortcut",
        "SM one-Higgs gauge selection is not PR230 O_H identity"
        in str(statuses["sm_one_higgs_oh_import_boundary"])
        and certificates["sm_one_higgs_oh_import_boundary"].get(
            "sm_one_higgs_import_closes_pr230"
        )
        is False,
        statuses["sm_one_higgs_oh_import_boundary"],
    )
    candidate_stress = certificates["canonical_higgs_operator_candidate_stress"]
    report(
        "canonical-higgs-operator-candidate-stress-blocks",
        "canonical-Higgs operator candidate stress rejects current substitutes"
        in str(statuses["canonical_higgs_operator_candidate_stress"])
        and candidate_stress.get("proposal_allowed") is False
        and all(row.get("candidate_valid") is False for row in candidate_stress.get("candidate_rows", [])),
        statuses["canonical_higgs_operator_candidate_stress"],
    )
    report(
        "hunit-canonical-higgs-operator-candidate-gate-blocks",
        "H_unit not canonical-Higgs operator realization"
        in str(statuses["hunit_canonical_higgs_operator_candidate_gate"]),
        statuses["hunit_canonical_higgs_operator_candidate_gate"],
    )
    source_higgs_guard_status = str(statuses["source_higgs_harness_absence_guard"])
    source_higgs_guard_cert = certificates["source_higgs_harness_absence_guard"]
    source_higgs_guard_fields = source_higgs_guard_cert.get("guard_fields", {})
    source_higgs_operator_guarded = (
        source_higgs_guard_fields.get("canonical_higgs_operator_absent") is True
        or (
            source_higgs_guard_fields.get("canonical_higgs_operator_certificate_gated")
            is True
            and source_higgs_guard_fields.get("enabled_false") is True
            and source_higgs_guard_fields.get("used_as_physical_yukawa_readout_false")
            is True
        )
    )
    report(
        "source-higgs-harness-absence-guard-not-evidence",
        (
            "source-Higgs harness absence guard" in source_higgs_guard_status
            or "source-Higgs harness default-off guard" in source_higgs_guard_status
        )
        and source_higgs_guard_cert.get("proposal_allowed") is False
        and source_higgs_guard_fields.get("source_higgs_cross_correlator") is True
        and source_higgs_operator_guarded,
        statuses["source_higgs_harness_absence_guard"],
    )
    source_higgs_smoke_cert = certificates["source_higgs_unratified_operator_smoke"]
    report(
        "source-higgs-unratified-operator-smoke-not-evidence",
        "source-Higgs unratified-operator smoke checkpoint"
        in str(statuses["source_higgs_unratified_operator_smoke"])
        and source_higgs_smoke_cert.get("proposal_allowed") is False
        and source_higgs_smoke_cert.get("source_higgs_metadata", {}).get(
            "canonical_higgs_operator_realization"
        )
        == "certificate_supplied_unratified"
        and source_higgs_smoke_cert.get("source_higgs_metadata", {}).get(
            "used_as_physical_yukawa_readout"
        )
        is False,
        statuses["source_higgs_unratified_operator_smoke"],
    )
    report(
        "source-higgs-unratified-gram-shortcut-no-go",
        "unratified source-Higgs Gram shortcut"
        in str(statuses["source_higgs_unratified_gram_shortcut_no_go"])
        and certificates["source_higgs_unratified_gram_shortcut_no_go"].get(
            "proposal_allowed"
        )
        is False
        and certificates["source_higgs_unratified_gram_shortcut_no_go"].get(
            "unratified_gram_shortcut_no_go_passed"
        )
        is True,
        statuses["source_higgs_unratified_gram_shortcut_no_go"],
    )
    report(
        "neutral-scalar-rank-one-purity-gate-not-passed",
        "neutral scalar rank-one purity gate not passed"
        in str(statuses["neutral_scalar_rank_one_purity_gate"]),
        statuses["neutral_scalar_rank_one_purity_gate"],
    )
    report(
        "neutral-scalar-commutant-rank-no-go-blocks",
        "neutral scalar commutant does not force rank-one purity"
        in str(statuses["neutral_scalar_commutant_rank_no_go"]),
        statuses["neutral_scalar_commutant_rank_no_go"],
    )
    report(
        "neutral-scalar-dynamical-rank-one-closure-blocks",
        "dynamical rank-one neutral scalar theorem not derived"
        in str(statuses["neutral_scalar_dynamical_rank_one_closure"]),
        statuses["neutral_scalar_dynamical_rank_one_closure"],
    )
    report(
        "orthogonal-neutral-decoupling-no-go-blocks",
        "orthogonal neutral decoupling shortcut not derived"
        in str(statuses["orthogonal_neutral_decoupling_no_go"]),
        statuses["orthogonal_neutral_decoupling_no_go"],
    )
    report(
        "fh-gauge-response-mixed-scalar-blocks",
        "FH gauge-response mixed-scalar obstruction"
        in str(statuses["fh_gauge_response_mixed_scalar"]),
        statuses["fh_gauge_response_mixed_scalar"],
    )
    report(
        "no-orthogonal-top-coupling-import-blocks",
        "no-orthogonal-top-coupling import audit"
        in str(statuses["no_orthogonal_top_coupling_import"]),
        statuses["no_orthogonal_top_coupling_import"],
    )
    report(
        "no-orthogonal-top-coupling-selection-rule-blocks",
        "no-orthogonal-top-coupling selection rule not derived"
        in str(statuses["no_orthogonal_top_coupling_selection_rule"]),
        statuses["no_orthogonal_top_coupling_selection_rule"],
    )
    report(
        "d17-source-pole-identity-closure-blocked",
        "D17 source-pole identity closure attempt blocked"
        in str(statuses["d17_source_pole_identity_closure"]),
        statuses["d17_source_pole_identity_closure"],
    )
    report(
        "source-overlap-sum-rule-no-go-blocks",
        "source-overlap spectral sum-rule no-go"
        in str(statuses["source_overlap_sum_rule_no_go"]),
        statuses["source_overlap_sum_rule_no_go"],
    )
    report(
        "short-distance-ope-lsz-no-go-blocks",
        "short-distance OPE not scalar LSZ closure"
        in str(statuses["short_distance_ope_lsz_no_go"]),
        statuses["short_distance_ope_lsz_no_go"],
    )
    report(
        "effective-mass-plateau-residue-no-go-blocks",
        "effective-mass plateau not scalar LSZ residue closure"
        in str(statuses["effective_mass_plateau_residue_no_go"]),
        statuses["effective_mass_plateau_residue_no_go"],
    )
    report(
        "finite-source-shift-derivative-no-go-blocks",
        "finite source-shift slope not zero-source derivative certificate"
        in str(statuses["finite_source_shift_derivative_no_go"]),
        statuses["finite_source_shift_derivative_no_go"],
    )
    report(
        "fh-lsz-finite-source-linearity-gate-not-closure",
        "finite-source-linearity gate"
        in str(statuses["fh_lsz_finite_source_linearity_gate"]),
        statuses["fh_lsz_finite_source_linearity_gate"],
    )
    report(
        "fh-lsz-finite-source-linearity-calibration-not-closure",
        "finite-source-linearity calibration"
        in str(statuses["fh_lsz_finite_source_linearity_calibration"]),
        statuses["fh_lsz_finite_source_linearity_calibration"],
    )
    report(
        "fh-lsz-target-observable-ess-certificate-not-closure",
        "target-observable ESS certificate"
        in str(statuses["fh_lsz_target_observable_ess"]),
        statuses["fh_lsz_target_observable_ess"],
    )
    report(
        "fh-lsz-autocorrelation-ess-gate-not-closure",
        "autocorrelation ESS gate"
        in str(statuses["fh_lsz_autocorrelation_ess_gate"]),
        statuses["fh_lsz_autocorrelation_ess_gate"],
    )
    report(
        "fh-lsz-response-window-forensics-not-closure",
        "response-window forensics" in str(statuses["fh_lsz_response_window_forensics"]),
        statuses["fh_lsz_response_window_forensics"],
    )
    report(
        "fh-lsz-common-window-response-provenance-not-closure",
        "common-window response provenance"
        in str(statuses["fh_lsz_common_window_response_provenance"]),
        statuses["fh_lsz_common_window_response_provenance"],
    )
    report(
        "fh-lsz-common-window-pooled-response-estimator-not-closure",
        "common-window pooled response estimator"
        in str(statuses["fh_lsz_common_window_pooled_response_estimator"]),
        statuses["fh_lsz_common_window_pooled_response_estimator"],
    )
    report(
        "fh-lsz-common-window-replacement-response-stability-not-closure",
        "common-window replacement response-stability passed"
        in str(statuses["fh_lsz_common_window_replacement_response_stability"]),
        statuses["fh_lsz_common_window_replacement_response_stability"],
    )
    report(
        "fh-lsz-common-window-response-gate-not-closure",
        "common-window response gate"
        in str(statuses["fh_lsz_common_window_response_gate"]),
        statuses["fh_lsz_common_window_response_gate"],
    )
    report(
        "fh-lsz-v2-target-response-stability-not-closure",
        "v2 target-response stability passed" in str(statuses["fh_lsz_v2_target_response_stability"]),
        statuses["fh_lsz_v2_target_response_stability"],
    )
    report(
        "fh-lsz-response-window-acceptance-gate-blocks",
        "response-window acceptance gate not passed"
        in str(statuses["fh_lsz_response_window_acceptance_gate"]),
        statuses["fh_lsz_response_window_acceptance_gate"],
    )
    report(
        "fh-lsz-target-timeseries-replacement-queue-not-closure",
        "FH-LSZ target-timeseries replacement queue"
        in str(statuses["fh_lsz_target_timeseries_replacement_queue"]),
        statuses["fh_lsz_target_timeseries_replacement_queue"],
    )
    report(
        "fh-lsz-target-timeseries-harness-support-not-evidence",
        "target time-series harness extension"
        in str(statuses["fh_lsz_target_timeseries_harness"]),
        statuses["fh_lsz_target_timeseries_harness"],
    )
    report(
        "fh-lsz-multitau-target-timeseries-harness-support-not-evidence",
        "multi-tau target time-series harness extension"
        in str(statuses["fh_lsz_multitau_target_timeseries_harness"]),
        statuses["fh_lsz_multitau_target_timeseries_harness"],
    )
    report(
        "fh-lsz-selected-mass-normal-cache-speedup-not-evidence",
        "selected-mass normal-cache speedup"
        in str(statuses["fh_lsz_selected_mass_normal_cache_speedup"]),
        statuses["fh_lsz_selected_mass_normal_cache_speedup"],
    )
    report(
        "fh-lsz-global-production-collision-guard-not-evidence",
        "FH-LSZ global production collision guard"
        in str(statuses["fh_lsz_global_production_collision_guard"])
        and certificates["fh_lsz_global_production_collision_guard"].get("proposal_allowed") is False,
        statuses["fh_lsz_global_production_collision_guard"],
    )
    report(
        "fh-lsz-target-timeseries-higgs-identity-no-go-blocks",
        "target time series not canonical-Higgs identity"
        in str(statuses["fh_lsz_target_timeseries_higgs_identity_no_go"]),
        statuses["fh_lsz_target_timeseries_higgs_identity_no_go"],
    )
    report(
        "higgs-pole-identity-latest-blocker-blocks",
        "latest Higgs-pole identity blocker certificate"
        in str(statuses["higgs_pole_identity_latest_blocker"]),
        statuses["higgs_pole_identity_latest_blocker"],
    )
    report(
        "fh-lsz-pole-fit-mode-budget-not-closure",
        "pole-fit mode-noise budget" in str(statuses["fh_lsz_pole_fit_mode_budget"])
        or "bounded-support" in str(statuses["fh_lsz_pole_fit_mode_budget"]),
        statuses["fh_lsz_pole_fit_mode_budget"],
    )
    report(
        "fh-lsz-eight-mode-noise-variance-gate-not-closure",
        "eight-mode noise variance gate" in str(statuses["fh_lsz_eight_mode_noise_variance"])
        or "open" in str(statuses["fh_lsz_eight_mode_noise_variance"]),
        statuses["fh_lsz_eight_mode_noise_variance"],
    )
    report(
        "fh-lsz-noise-subsample-diagnostics-not-closure",
        "noise-subsample diagnostics" in str(statuses["fh_lsz_noise_subsample_diagnostics"])
        or "bounded-support" in str(statuses["fh_lsz_noise_subsample_diagnostics"]),
        statuses["fh_lsz_noise_subsample_diagnostics"],
    )
    report(
        "fh-lsz-variance-calibration-manifest-not-evidence",
        "variance calibration manifest" in str(statuses["fh_lsz_variance_calibration_manifest"])
        or "bounded-support" in str(statuses["fh_lsz_variance_calibration_manifest"]),
        statuses["fh_lsz_variance_calibration_manifest"],
    )
    report(
        "fh-lsz-paired-variance-calibration-gate-not-closure",
        "paired x8/x16 variance calibration" in str(statuses["fh_lsz_paired_variance_calibration_gate"]),
        statuses["fh_lsz_paired_variance_calibration_gate"],
    )
    report(
        "fh-lsz-polefit8x8-manifest-not-evidence",
        "eight-mode-x8 pole-fit chunk manifest" in str(statuses["fh_lsz_polefit8x8_chunk_manifest"]),
        statuses["fh_lsz_polefit8x8_chunk_manifest"],
    )
    report(
        "fh-lsz-polefit8x8-combiner-not-closure",
        "eight-mode-x8 pole-fit" in str(statuses["fh_lsz_polefit8x8_chunk_combiner_gate"]),
        statuses["fh_lsz_polefit8x8_chunk_combiner_gate"],
    )
    report(
        "fh-lsz-polefit8x8-postprocessor-not-closure",
        "eight-mode-x8" in str(statuses["fh_lsz_polefit8x8_postprocessor"]),
        statuses["fh_lsz_polefit8x8_postprocessor"],
    )
    report(
        "fh-lsz-invariant-readout-still-needs-pole-data",
        "invariant readout formula" in str(statuses["fh_lsz_invariant_readout"])
        or "exact-support" in str(statuses["fh_lsz_invariant_readout"]),
        statuses["fh_lsz_invariant_readout"],
    )
    report(
        "scalar-pole-determinant-gate-still-needs-kernel",
        "determinant gate" in str(statuses["scalar_pole_determinant_gate"])
        or "exact-support" in str(statuses["scalar_pole_determinant_gate"]),
        statuses["scalar_pole_determinant_gate"],
    )
    report(
        "scalar-ladder-eigen-derivative-gate-still-needs-momentum-kernel",
        "eigen-derivative gate" in str(statuses["scalar_ladder_eigen_derivative"])
        or "exact-support" in str(statuses["scalar_ladder_eigen_derivative"]),
        statuses["scalar_ladder_eigen_derivative"],
    )
    report(
        "scalar-ladder-total-momentum-derivative-scout-not-limit",
        "total-momentum derivative scout" in str(statuses["scalar_ladder_total_momentum_derivative"])
        or "bounded-support" in str(statuses["scalar_ladder_total_momentum_derivative"]),
        statuses["scalar_ladder_total_momentum_derivative"],
    )
    report(
        "scalar-ladder-derivative-limit-needs-zero-mode-theorem",
        "limiting-order obstruction" in str(statuses["scalar_ladder_derivative_limit"])
        or "exact negative boundary" in str(statuses["scalar_ladder_derivative_limit"]),
        statuses["scalar_ladder_derivative_limit"],
    )
    report(
        "scalar-ladder-residue-envelope-not-lsz-bound",
        "residue-envelope obstruction" in str(statuses["scalar_ladder_residue_envelope"])
        or "exact negative boundary" in str(statuses["scalar_ladder_residue_envelope"]),
        statuses["scalar_ladder_residue_envelope"],
    )
    report(
        "scalar-kernel-ward-identity-not-k-prime-theorem",
        "Ward-identity obstruction" in str(statuses["scalar_kernel_ward_identity"])
        or "exact negative boundary" in str(statuses["scalar_kernel_ward_identity"]),
        statuses["scalar_kernel_ward_identity"],
    )
    report(
        "scalar-zero-mode-limit-order-needs-prescription",
        "zero-mode limit-order theorem" in str(statuses["scalar_zero_mode_limit_order"])
        or "exact negative boundary" in str(statuses["scalar_zero_mode_limit_order"]),
        statuses["scalar_zero_mode_limit_order"],
    )
    report(
        "zero-mode-prescription-import-audit-not-closure",
        "zero-mode prescription import audit" in str(statuses["zero_mode_prescription_import"])
        or "exact negative boundary" in str(statuses["zero_mode_prescription_import"]),
        statuses["zero_mode_prescription_import"],
    )
    report(
        "flat-toron-sectors-change-scalar-denominator",
        "flat toron scalar-denominator obstruction" in str(statuses["flat_toron_denominator"])
        or "exact negative boundary" in str(statuses["flat_toron_denominator"]),
        statuses["flat_toron_denominator"],
    )
    report(
        "flat-toron-thermodynamic-washout-not-closure",
        "flat toron thermodynamic washout" in str(statuses["flat_toron_washout"])
        or "exact-support" in str(statuses["flat_toron_washout"]),
        statuses["flat_toron_washout"],
    )
    report(
        "color-singlet-zero-mode-cancellation-not-closure",
        "color-singlet gauge-zero-mode cancellation" in str(statuses["color_singlet_zero_mode"])
        or "exact-support" in str(statuses["color_singlet_zero_mode"]),
        statuses["color_singlet_zero_mode"],
    )
    report(
        "color-singlet-finite-q-ir-regularity-not-closure",
        "color-singlet finite-q IR regularity" in str(statuses["color_singlet_finite_q_ir"])
        or "exact-support" in str(statuses["color_singlet_finite_q_ir"]),
        statuses["color_singlet_finite_q_ir"],
    )
    report(
        "color-singlet-zero-mode-removed-ladder-pole-search-not-closure",
        "zero-mode-removed ladder pole search"
        in str(statuses["color_singlet_zero_mode_removed_ladder_pole_search"])
        or "bounded-support" in str(statuses["color_singlet_zero_mode_removed_ladder_pole_search"]),
        statuses["color_singlet_zero_mode_removed_ladder_pole_search"],
    )
    report(
        "taste-corner-ladder-pole-witness-not-closure",
        "taste-corner pole-witness obstruction" in str(statuses["taste_corner_ladder_pole_obstruction"])
        or "exact negative boundary" in str(statuses["taste_corner_ladder_pole_obstruction"]),
        statuses["taste_corner_ladder_pole_obstruction"],
    )
    report(
        "taste-carrier-import-audit-not-closure",
        "taste-corner scalar-carrier import audit" in str(statuses["taste_carrier_import_audit"])
        or "exact negative boundary" in str(statuses["taste_carrier_import_audit"]),
        statuses["taste_carrier_import_audit"],
    )
    report(
        "taste-singlet-normalization-removes-finite-crossings",
        "taste-singlet normalization removes finite ladder crossings"
        in str(statuses["taste_singlet_ladder_normalization"]),
        statuses["taste_singlet_ladder_normalization"],
    )
    report(
        "scalar-taste-projector-normalization-attempt-still-open",
        "scalar taste-projector normalization theorem attempt blocked"
        in str(statuses["scalar_taste_projector_normalization_attempt"]),
        statuses["scalar_taste_projector_normalization_attempt"],
    )
    report(
        "unit-projector-pole-threshold-not-derived",
        "unit-projector finite-ladder pole-threshold obstruction"
        in str(statuses["unit_projector_pole_threshold"]),
        statuses["unit_projector_pole_threshold"],
    )
    report(
        "scalar-kernel-enhancement-import-audit-not-closure",
        "scalar-kernel enhancement import audit" in str(statuses["scalar_kernel_enhancement_import"]),
        statuses["scalar_kernel_enhancement_import"],
    )
    report(
        "fitted-kernel-residue-selector-not-closure",
        "fitted scalar-kernel residue selector no-go" in str(statuses["fitted_kernel_residue_selector"]),
        statuses["fitted_kernel_residue_selector"],
    )
    report(
        "finite-ladder-route-needs-ir-limit",
        "zero-mode" in str(statuses["ladder_ir_zero_mode"]),
        statuses["ladder_ir_zero_mode"],
    )
    report(
        "heavy-kinetic-route-needs-data-and-matching",
        "heavy kinetic" in str(statuses["heavy_kinetic"])
        or "bounded-support" in str(statuses["heavy_kinetic"]),
        statuses["heavy_kinetic"],
    )
    report(
        "nonzero-momentum-scout-needs-production-and-matching",
        "nonzero-momentum" in str(statuses["nonzero_momentum"])
        or "bounded-support" in str(statuses["nonzero_momentum"]),
        statuses["nonzero_momentum"],
    )
    report(
        "momentum-harness-extension-needs-production",
        "momentum harness" in str(statuses["momentum_harness"])
        or "bounded-support" in str(statuses["momentum_harness"]),
        statuses["momentum_harness"],
    )
    report(
        "heavy-kinetic-route-needs-matching-theorem",
        "matching" in str(statuses["heavy_matching"]),
        statuses["heavy_matching"],
    )
    report(
        "momentum-pilot-needs-production",
        "momentum pilot" in str(statuses["momentum_pilot"])
        or "bounded-support" in str(statuses["momentum_pilot"]),
        statuses["momentum_pilot"],
    )
    report(
        "assumption-stress-no-shortcuts",
        "assumption-import" in str(statuses["assumption_stress"]),
        statuses["assumption_stress"],
    )
    report(
        "free-kinetic-support-not-interacting-closure",
        "free staggered kinetic coefficient" in str(statuses["free_kinetic"]),
        statuses["free_kinetic"],
    )
    report(
        "interacting-kinetic-needs-ensemble-or-theorem",
        "interacting kinetic" in str(statuses["interacting_kinetic"]),
        statuses["interacting_kinetic"],
    )
    report(
        "retained-closure-route-certificate-still-open",
        "retained closure not yet reached" in str(statuses["retained_closure_route"]),
        statuses["retained_closure_route"],
    )
    report(
        "full-positive-closure-assembly-gate-still-open",
        "full positive PR230 closure assembly gate not passed"
        in str(statuses["full_positive_closure_assembly_gate"])
        and certificates["full_positive_closure_assembly_gate"].get("proposal_allowed") is False
        and certificates["full_positive_closure_assembly_gate"].get("chunk_only_evaluation", {}).get(
            "assembly_passed"
        )
        is False,
        statuses["full_positive_closure_assembly_gate"],
    )
    report(
        "pr230-nonchunk-current-surface-exhaustion-recorded",
        "current PR230 non-chunk route queue exhausted"
        in str(statuses["pr230_nonchunk_current_surface_exhaustion"])
        and certificates["pr230_nonchunk_current_surface_exhaustion"].get("proposal_allowed")
        is False
        and certificates["pr230_nonchunk_current_surface_exhaustion"].get(
            "current_surface_exhaustion_gate_passed"
        )
        is True,
        statuses["pr230_nonchunk_current_surface_exhaustion"],
    )
    report(
        "pr230-nonchunk-future-artifact-intake-recorded",
        "future-artifact intake" in str(statuses["pr230_nonchunk_future_artifact_intake"])
        and certificates["pr230_nonchunk_future_artifact_intake"].get("proposal_allowed")
        is False
        and certificates["pr230_nonchunk_future_artifact_intake"].get(
            "future_artifact_intake_gate_passed"
        )
        is True
        and certificates["pr230_nonchunk_future_artifact_intake"].get(
            "dramatic_step_gate", {}
        ).get("passed")
        is False,
        statuses["pr230_nonchunk_future_artifact_intake"],
    )
    report(
        "pr230-nonchunk-terminal-route-exhaustion-recorded",
        "terminal route-exhaustion gate"
        in str(statuses["pr230_nonchunk_terminal_route_exhaustion"])
        and certificates["pr230_nonchunk_terminal_route_exhaustion"].get(
            "proposal_allowed"
        )
        is False
        and certificates["pr230_nonchunk_terminal_route_exhaustion"].get(
            "terminal_route_exhaustion_gate_passed"
        )
        is True
        and certificates["pr230_nonchunk_terminal_route_exhaustion"].get(
            "dramatic_step_gate", {}
        ).get("passed")
        is False,
        statuses["pr230_nonchunk_terminal_route_exhaustion"],
    )
    report(
        "pr230-nonchunk-reopen-admissibility-recorded",
        "reopen-admissibility gate"
        in str(statuses["pr230_nonchunk_reopen_admissibility"])
        and certificates["pr230_nonchunk_reopen_admissibility"].get("proposal_allowed")
        is False
        and certificates["pr230_nonchunk_reopen_admissibility"].get(
            "reopen_admissibility_gate_passed"
        )
        is True
        and certificates["pr230_nonchunk_reopen_admissibility"].get(
            "dramatic_step_gate", {}
        ).get("passed")
        is False,
        statuses["pr230_nonchunk_reopen_admissibility"],
    )
    report(
        "pr230-nonchunk-cycle14-route-selector-recorded",
        "cycle-14 route-selector gate"
        in str(statuses["pr230_nonchunk_cycle14_route_selector"])
        and certificates["pr230_nonchunk_cycle14_route_selector"].get("proposal_allowed")
        is False
        and certificates["pr230_nonchunk_cycle14_route_selector"].get(
            "route_selector_gate_passed"
        )
        is True
        and certificates["pr230_nonchunk_cycle14_route_selector"].get(
            "dramatic_step_gate", {}
        ).get("passed")
        is False,
        statuses["pr230_nonchunk_cycle14_route_selector"],
    )
    report(
        "pr230-nonchunk-cycle15-independent-route-admission-recorded",
        "cycle-15 independent-route admission gate"
        in str(statuses["pr230_nonchunk_cycle15_independent_route_admission"])
        and certificates["pr230_nonchunk_cycle15_independent_route_admission"].get(
            "proposal_allowed"
        )
        is False
        and certificates["pr230_nonchunk_cycle15_independent_route_admission"].get(
            "independent_route_admission_gate_passed"
        )
        is True
        and certificates["pr230_nonchunk_cycle15_independent_route_admission"].get(
            "dramatic_step_gate", {}
        ).get("passed")
        is False,
        statuses["pr230_nonchunk_cycle15_independent_route_admission"],
    )
    report(
        "pr230-nonchunk-cycle16-reopen-source-guard-recorded",
        "cycle-16 reopen-source guard"
        in str(statuses["pr230_nonchunk_cycle16_reopen_source_guard"])
        and certificates["pr230_nonchunk_cycle16_reopen_source_guard"].get(
            "proposal_allowed"
        )
        is False
        and certificates["pr230_nonchunk_cycle16_reopen_source_guard"].get(
            "reopen_source_guard_passed"
        )
        is True
        and certificates["pr230_nonchunk_cycle16_reopen_source_guard"].get(
            "dramatic_step_gate", {}
        ).get("passed")
        is False,
        statuses["pr230_nonchunk_cycle16_reopen_source_guard"],
    )
    report(
        "pr230-nonchunk-cycle17-stop-condition-gate-recorded",
        "cycle-17 stop-condition gate"
        in str(statuses["pr230_nonchunk_cycle17_stop_condition_gate"])
        and certificates["pr230_nonchunk_cycle17_stop_condition_gate"].get(
            "proposal_allowed"
        )
        is False
        and certificates["pr230_nonchunk_cycle17_stop_condition_gate"].get(
            "stop_condition_gate_passed"
        )
        is True
        and certificates["pr230_nonchunk_cycle17_stop_condition_gate"].get(
            "dramatic_step_gate", {}
        ).get("passed")
        is False,
        statuses["pr230_nonchunk_cycle17_stop_condition_gate"],
    )
    report(
        "pr230-nonchunk-cycle18-reopen-freshness-gate-recorded",
        "cycle-18 reopen-freshness gate"
        in str(statuses["pr230_nonchunk_cycle18_reopen_freshness_gate"])
        and certificates["pr230_nonchunk_cycle18_reopen_freshness_gate"].get(
            "proposal_allowed"
        )
        is False
        and certificates["pr230_nonchunk_cycle18_reopen_freshness_gate"].get(
            "reopen_freshness_gate_passed"
        )
        is True
        and certificates["pr230_nonchunk_cycle18_reopen_freshness_gate"].get(
            "dramatic_step_gate", {}
        ).get("passed")
        is False,
        statuses["pr230_nonchunk_cycle18_reopen_freshness_gate"],
    )
    report(
        "pr230-nonchunk-cycle19-no-duplicate-route-gate-recorded",
        "cycle-19 no-duplicate-route gate"
        in str(statuses["pr230_nonchunk_cycle19_no_duplicate_route_gate"])
        and certificates["pr230_nonchunk_cycle19_no_duplicate_route_gate"].get(
            "proposal_allowed"
        )
        is False
        and certificates["pr230_nonchunk_cycle19_no_duplicate_route_gate"].get(
            "no_duplicate_route_gate_passed"
        )
        is True
        and certificates["pr230_nonchunk_cycle19_no_duplicate_route_gate"].get(
            "dramatic_step_gate", {}
        ).get("passed")
        is False,
        statuses["pr230_nonchunk_cycle19_no_duplicate_route_gate"],
    )
    report(
        "pr230-nonchunk-cycle20-process-gate-continuation-no-go-recorded",
        "cycle-20 process-gate continuation no-go"
        in str(statuses["pr230_nonchunk_cycle20_process_gate_continuation_no_go"])
        and certificates["pr230_nonchunk_cycle20_process_gate_continuation_no_go"].get(
            "proposal_allowed"
        )
        is False
        and certificates["pr230_nonchunk_cycle20_process_gate_continuation_no_go"].get(
            "process_gate_continuation_no_go_passed"
        )
        is True
        and certificates["pr230_nonchunk_cycle20_process_gate_continuation_no_go"].get(
            "dramatic_step_gate", {}
        ).get("passed")
        is False,
        statuses["pr230_nonchunk_cycle20_process_gate_continuation_no_go"],
    )
    report(
        "pr230-nonchunk-cycle21-remote-reopen-guard-recorded",
        "cycle-21 remote-surface reopen guard"
        in str(statuses["pr230_nonchunk_cycle21_remote_reopen_guard"])
        and certificates["pr230_nonchunk_cycle21_remote_reopen_guard"].get(
            "proposal_allowed"
        )
        is False
        and certificates["pr230_nonchunk_cycle21_remote_reopen_guard"].get(
            "cycle21_remote_reopen_guard_passed"
        )
        is True
        and certificates["pr230_nonchunk_cycle21_remote_reopen_guard"].get(
            "dramatic_step_gate", {}
        ).get("passed")
        is False,
        statuses["pr230_nonchunk_cycle21_remote_reopen_guard"],
    )
    report(
        "pr230-nonchunk-cycle22-main-audit-drift-guard-recorded",
        "cycle-22 main-audit-drift reopen guard"
        in str(statuses["pr230_nonchunk_cycle22_main_audit_drift_guard"])
        and certificates["pr230_nonchunk_cycle22_main_audit_drift_guard"].get(
            "proposal_allowed"
        )
        is False
        and certificates["pr230_nonchunk_cycle22_main_audit_drift_guard"].get(
            "cycle22_main_audit_drift_guard_passed"
        )
        is True
        and certificates["pr230_nonchunk_cycle22_main_audit_drift_guard"].get(
            "dramatic_step_gate", {}
        ).get("passed")
        is False,
        statuses["pr230_nonchunk_cycle22_main_audit_drift_guard"],
    )
    report(
        "pr230-nonchunk-cycle23-main-effective-status-drift-guard-recorded",
        "cycle-23 main-effective-status-drift reopen guard"
        in str(statuses["pr230_nonchunk_cycle23_main_effective_status_drift_guard"])
        and certificates["pr230_nonchunk_cycle23_main_effective_status_drift_guard"].get(
            "proposal_allowed"
        )
        is False
        and certificates["pr230_nonchunk_cycle23_main_effective_status_drift_guard"].get(
            "cycle23_main_effective_status_drift_guard_passed"
        )
        is True
        and certificates["pr230_nonchunk_cycle23_main_effective_status_drift_guard"].get(
            "dramatic_step_gate", {}
        ).get("passed")
        is False,
        statuses["pr230_nonchunk_cycle23_main_effective_status_drift_guard"],
    )
    report(
        "pr230-nonchunk-cycle24-post-cycle23-main-status-drift-guard-recorded",
        "cycle-24 post-cycle-23 main-status-drift reopen guard"
        in str(statuses["pr230_nonchunk_cycle24_post_cycle23_main_status_drift_guard"])
        and certificates[
            "pr230_nonchunk_cycle24_post_cycle23_main_status_drift_guard"
        ].get("proposal_allowed")
        is False
        and certificates[
            "pr230_nonchunk_cycle24_post_cycle23_main_status_drift_guard"
        ].get("cycle24_post_cycle23_main_status_drift_guard_passed")
        is True
        and certificates[
            "pr230_nonchunk_cycle24_post_cycle23_main_status_drift_guard"
        ].get("dramatic_step_gate", {}).get("passed")
        is False,
        statuses["pr230_nonchunk_cycle24_post_cycle23_main_status_drift_guard"],
    )
    report(
        "pr230-nonchunk-cycle25-post-cycle24-main-audit-status-drift-guard-recorded",
        "cycle-25 post-cycle-24 main-audit-status-drift reopen guard"
        in str(statuses["pr230_nonchunk_cycle25_post_cycle24_main_audit_status_drift_guard"])
        and certificates[
            "pr230_nonchunk_cycle25_post_cycle24_main_audit_status_drift_guard"
        ].get("proposal_allowed")
        is False
        and certificates[
            "pr230_nonchunk_cycle25_post_cycle24_main_audit_status_drift_guard"
        ].get("cycle25_post_cycle24_main_audit_status_drift_guard_passed")
        is True
        and certificates[
            "pr230_nonchunk_cycle25_post_cycle24_main_audit_status_drift_guard"
        ].get("dramatic_step_gate", {}).get("passed")
        is False,
        statuses["pr230_nonchunk_cycle25_post_cycle24_main_audit_status_drift_guard"],
    )
    report(
        "pr230-nonchunk-cycle26-post-cycle25-main-audit-status-drift-guard-recorded",
        "cycle-26 post-cycle-25 main-audit-status-drift reopen guard"
        in str(statuses["pr230_nonchunk_cycle26_post_cycle25_main_audit_status_drift_guard"])
        and certificates[
            "pr230_nonchunk_cycle26_post_cycle25_main_audit_status_drift_guard"
        ].get("proposal_allowed")
        is False
        and certificates[
            "pr230_nonchunk_cycle26_post_cycle25_main_audit_status_drift_guard"
        ].get("cycle26_post_cycle25_main_audit_status_drift_guard_passed")
        is True
        and certificates[
            "pr230_nonchunk_cycle26_post_cycle25_main_audit_status_drift_guard"
        ].get("dramatic_step_gate", {}).get("passed")
        is False,
        statuses["pr230_nonchunk_cycle26_post_cycle25_main_audit_status_drift_guard"],
    )
    report(
        "pr230-nonchunk-cycle27-post-cycle26-main-audit-status-drift-guard-recorded",
        "cycle-27 post-cycle-26 main-audit-status-drift reopen guard"
        in str(statuses["pr230_nonchunk_cycle27_post_cycle26_main_audit_status_drift_guard"])
        and certificates[
            "pr230_nonchunk_cycle27_post_cycle26_main_audit_status_drift_guard"
        ].get("proposal_allowed")
        is False
        and certificates[
            "pr230_nonchunk_cycle27_post_cycle26_main_audit_status_drift_guard"
        ].get("cycle27_post_cycle26_main_audit_status_drift_guard_passed")
        is True
        and certificates[
            "pr230_nonchunk_cycle27_post_cycle26_main_audit_status_drift_guard"
        ].get("dramatic_step_gate", {}).get("passed")
        is False,
        statuses["pr230_nonchunk_cycle27_post_cycle26_main_audit_status_drift_guard"],
    )
    report(
        "pr230-nonchunk-cycle28-post-cycle27-main-audit-status-drift-guard-recorded",
        "cycle-28 post-cycle-27 main-audit-status-drift reopen guard"
        in str(statuses["pr230_nonchunk_cycle28_post_cycle27_main_audit_status_drift_guard"])
        and certificates[
            "pr230_nonchunk_cycle28_post_cycle27_main_audit_status_drift_guard"
        ].get("proposal_allowed")
        is False
        and certificates[
            "pr230_nonchunk_cycle28_post_cycle27_main_audit_status_drift_guard"
        ].get("cycle28_post_cycle27_main_audit_status_drift_guard_passed")
        is True
        and certificates[
            "pr230_nonchunk_cycle28_post_cycle27_main_audit_status_drift_guard"
        ].get("dramatic_step_gate", {}).get("passed")
        is False,
        statuses["pr230_nonchunk_cycle28_post_cycle27_main_audit_status_drift_guard"],
    )
    report(
        "pr230-nonchunk-cycle29-post-cycle28-main-audit-status-drift-guard-recorded",
        "cycle-29 post-cycle-28 main-audit-status-drift reopen guard"
        in str(statuses["pr230_nonchunk_cycle29_post_cycle28_main_audit_status_drift_guard"])
        and certificates[
            "pr230_nonchunk_cycle29_post_cycle28_main_audit_status_drift_guard"
        ].get("proposal_allowed")
        is False
        and certificates[
            "pr230_nonchunk_cycle29_post_cycle28_main_audit_status_drift_guard"
        ].get("cycle29_post_cycle28_main_audit_status_drift_guard_passed")
        is True
        and certificates[
            "pr230_nonchunk_cycle29_post_cycle28_main_audit_status_drift_guard"
        ].get("dramatic_step_gate", {}).get("passed")
        is False,
        statuses["pr230_nonchunk_cycle29_post_cycle28_main_audit_status_drift_guard"],
    )
    report(
        "pr230-nonchunk-cycle30-post-cycle29-main-audit-status-drift-guard-recorded",
        "cycle-30 post-cycle-29 main-audit-status-drift reopen guard"
        in str(statuses["pr230_nonchunk_cycle30_post_cycle29_main_audit_status_drift_guard"])
        and certificates[
            "pr230_nonchunk_cycle30_post_cycle29_main_audit_status_drift_guard"
        ].get("proposal_allowed")
        is False
        and certificates[
            "pr230_nonchunk_cycle30_post_cycle29_main_audit_status_drift_guard"
        ].get("cycle30_post_cycle29_main_audit_status_drift_guard_passed")
        is True
        and certificates[
            "pr230_nonchunk_cycle30_post_cycle29_main_audit_status_drift_guard"
        ].get("dramatic_step_gate", {}).get("passed")
        is False,
        statuses["pr230_nonchunk_cycle30_post_cycle29_main_audit_status_drift_guard"],
    )
    report(
        "pr230-nonchunk-cycle31-post-cycle30-main-audit-status-drift-guard-recorded",
        "cycle-31 post-cycle-30 main-audit-status-drift reopen guard"
        in str(statuses["pr230_nonchunk_cycle31_post_cycle30_main_audit_status_drift_guard"])
        and certificates[
            "pr230_nonchunk_cycle31_post_cycle30_main_audit_status_drift_guard"
        ].get("proposal_allowed")
        is False
        and certificates[
            "pr230_nonchunk_cycle31_post_cycle30_main_audit_status_drift_guard"
        ].get("cycle31_post_cycle30_main_audit_status_drift_guard_passed")
        is True
        and certificates[
            "pr230_nonchunk_cycle31_post_cycle30_main_audit_status_drift_guard"
        ].get("dramatic_step_gate", {}).get("passed")
        is False,
        statuses["pr230_nonchunk_cycle31_post_cycle30_main_audit_status_drift_guard"],
    )
    report(
        "pr230-nonchunk-cycle32-post-cycle31-main-audit-status-drift-guard-recorded",
        "cycle-32 post-cycle-31 main-audit-status-drift reopen guard"
        in str(statuses["pr230_nonchunk_cycle32_post_cycle31_main_audit_status_drift_guard"])
        and certificates[
            "pr230_nonchunk_cycle32_post_cycle31_main_audit_status_drift_guard"
        ].get("proposal_allowed")
        is False
        and certificates[
            "pr230_nonchunk_cycle32_post_cycle31_main_audit_status_drift_guard"
        ].get("cycle32_post_cycle31_main_audit_status_drift_guard_passed")
        is True
        and certificates[
            "pr230_nonchunk_cycle32_post_cycle31_main_audit_status_drift_guard"
        ].get("dramatic_step_gate", {}).get("passed")
        is False,
        statuses["pr230_nonchunk_cycle32_post_cycle31_main_audit_status_drift_guard"],
    )
    report(
        "pr230-nonchunk-cycle33-post-cycle32-main-audit-status-drift-guard-recorded",
        "cycle-33 post-cycle-32 main-audit-status-drift reopen guard"
        in str(statuses["pr230_nonchunk_cycle33_post_cycle32_main_audit_status_drift_guard"])
        and certificates[
            "pr230_nonchunk_cycle33_post_cycle32_main_audit_status_drift_guard"
        ].get("proposal_allowed")
        is False
        and certificates[
            "pr230_nonchunk_cycle33_post_cycle32_main_audit_status_drift_guard"
        ].get("cycle33_post_cycle32_main_audit_status_drift_guard_passed")
        is True
        and certificates[
            "pr230_nonchunk_cycle33_post_cycle32_main_audit_status_drift_guard"
        ].get("dramatic_step_gate", {}).get("passed")
        is False,
        statuses["pr230_nonchunk_cycle33_post_cycle32_main_audit_status_drift_guard"],
    )
    report(
        "pr230-nonchunk-cycle34-post-cycle33-main-nonpr230-drift-guard-recorded",
        "cycle-34 post-cycle-33 main non-PR230 drift reopen guard"
        in str(statuses["pr230_nonchunk_cycle34_post_cycle33_main_nonpr230_drift_guard"])
        and certificates[
            "pr230_nonchunk_cycle34_post_cycle33_main_nonpr230_drift_guard"
        ].get("proposal_allowed")
        is False
        and certificates[
            "pr230_nonchunk_cycle34_post_cycle33_main_nonpr230_drift_guard"
        ].get("cycle34_post_cycle33_main_nonpr230_drift_guard_passed")
        is True
        and certificates[
            "pr230_nonchunk_cycle34_post_cycle33_main_nonpr230_drift_guard"
        ].get("dramatic_step_gate", {}).get("passed")
        is False,
        statuses["pr230_nonchunk_cycle34_post_cycle33_main_nonpr230_drift_guard"],
    )
    report(
        "pr230-nonchunk-cycle35-post-cycle34-main-audit-ledger-drift-guard-recorded",
        "cycle-35 post-cycle-34 main audit-ledger drift reopen guard"
        in str(statuses["pr230_nonchunk_cycle35_post_cycle34_main_audit_ledger_drift_guard"])
        and certificates[
            "pr230_nonchunk_cycle35_post_cycle34_main_audit_ledger_drift_guard"
        ].get("proposal_allowed")
        is False
        and certificates[
            "pr230_nonchunk_cycle35_post_cycle34_main_audit_ledger_drift_guard"
        ].get("cycle35_post_cycle34_main_audit_ledger_drift_guard_passed")
        is True
        and certificates[
            "pr230_nonchunk_cycle35_post_cycle34_main_audit_ledger_drift_guard"
        ].get("dramatic_step_gate", {}).get("passed")
        is False,
        statuses["pr230_nonchunk_cycle35_post_cycle34_main_audit_ledger_drift_guard"],
    )

    remaining_routes = [
        {
            "route": "strict production direct measurement",
            "needed": "fine-scale relativistic top campaign or validated heavy-quark treatment with matching",
        },
        {
            "route": "new scalar LSZ/canonical normalization theorem",
            "needed": "interacting scalar two-point denominator, isolated pole/canonical kinetic term, residue kappa_H",
        },
        {
            "route": "new heavy-matching observable/theorem",
            "needed": "nonzero-momentum kinetic-mass correlators plus lattice-HQET/NRQCD-to-SM top mass matching without observed top calibration",
        },
        {
            "route": "Feynman-Hellmann source-response measurement",
            "needed": "production dE/ds data plus scalar LSZ/canonical-Higgs normalization kappa_s and response matching",
        },
        {
            "route": "non-source response rank repair",
            "needed": "certified O_H with C_sH/C_HH pole Gram purity, or same-source top/W/Z response rows with matched covariance, sector-overlap, and canonical-Higgs identity; deterministic W response must include paired top rows or a closed covariance formula",
        },
        {
            "route": "full positive closure assembly",
            "needed": "production response plus scalar-LSZ model/FV/IR control plus one accepted O_H/WZ/Schur/rank-one bridge and retained-route approval",
        },
        {
            "route": "exact tensor/PEPS Schur row production",
            "needed": "same-surface neutral scalar kernel basis, source/orthogonal projector, A/B/C row definitions, and certified exact contraction",
        },
        {
            "route": "GNS source-Higgs flat extension",
            "needed": "same-surface O_H plus production C_ss/C_sH/C_HH pole rows giving a full PSD moment matrix with flat-extension rank stability",
        },
        {
            "route": "current-surface non-chunk queue exhausted",
            "needed": "a new same-surface row, certificate, or theorem before continuing non-chunk shortcut cycling",
        },
        {
            "route": "terminal non-chunk route exhaustion",
            "needed": "do not reopen until a named same-surface artifact exists and aggregate gates are rerun",
        },
        {
            "route": "independent non-chunk route admission",
            "needed": "no independent current route is admissible before a named same-surface artifact exists",
        },
        {
            "route": "post-checkpoint non-chunk reopen source",
            "needed": "no admissible reopen source exists until a named same-surface artifact is present and aggregate gates rerun",
        },
        {
            "route": "non-chunk stop condition",
            "needed": "no executable current-surface non-chunk route remains on this branch before a named same-surface artifact exists",
        },
        {
            "route": "process-gate continuation",
            "needed": "do not continue with process-only gates as science routes before a named same-surface artifact exists",
        },
        {
            "route": "remote-surface reopen guard",
            "needed": "do not reopen from fetched remote drift unless a listed same-surface artifact is present on the target branch",
        },
        {
            "route": "main audit-drift reopen guard",
            "needed": "do not reopen from origin/main audit/effective-status drift unless a listed PR230 same-surface artifact is present",
        },
        {
            "route": "origin/main composite-Higgs packet intake",
            "needed": "treat cross-lane composite-Higgs stretch packets as context only until they produce PR230 same-source O_H/C_sH/C_HH authority or a listed same-surface artifact",
        },
    ]

    result = {
        "actual_current_surface_status": "open / active campaign continuing after current shortcut blocks",
        "verdict": (
            "The current PR #230 physics-loop checkpoint has not reached "
            "retained top-Yukawa closure.  It did retire the visible shortcut "
            "routes: "
            "Ward/H_unit, R_conn-only LSZ, Legendre normalization, free logdet "
            "bubble, contact HS/RPA, simplified ladder projector, same-1PI, "
            "finite ladder IR/zero-mode shortcut, and static/HQET without "
            "matching.  It also isolates a constructive heavy kinetic-mass "
            "route, a tiny nonzero-momentum correlator scout, and production "
            "harness momentum fields.  The negative-route applicability review "
            "confirms these retired shortcut routes are current-surface blockers "
            "only, not permanent retained negative theorems; the named future "
            "source-Higgs, W/Z, Schur, rank-one, scalar-LSZ, and production "
            "routes remain open when their missing artifacts are supplied.  A "
            "bounded two-volume pilot has large "
            "finite-volume drift, so that route still needs production data "
            "and a derived matching theorem.  The free staggered action fixes "
            "its kinetic coefficient, but interacting renormalization remains "
            "open and is gauge-background sensitive.  A covariant scalar LSZ "
            "normalization model shows source scaling can cancel only if the "
            "interacting denominator and residue are derived together.  Exact "
            "Feshbach response preservation removes crossover distortion as the "
            "blocker but does not equate scalar and gauge residues.  The "
            "axiom-first bridge stack is bounded transport support with endpoint "
            "imports, not a missed PR #230 proof.  Spectral positivity and "
            "low-order curvature moments do not fix the isolated pole residue "
            "without saturation/continuum control; large-Nc pole dominance is "
            "not a finite-Nc proof at N_c=3.  The production resource "
            "projection makes the strict direct route concrete as a multi-day "
            "single-worker job, but it is not measurement evidence.  A "
            "Feynman-Hellmann top-energy response can remove additive rest "
            "mass, but still needs scalar source-to-Higgs normalization and "
            "production response data; the reduced mass-bracket response is "
            "bare-source support only.  The source-reparametrization gauge "
            "boundary shows source-only analytic routes cannot close without "
            "canonical scalar normalization, and the strongest existing "
            "EW/Higgs structural notes do not supply that hidden proof.  "
            "The explicit source-to-Higgs LSZ closure attempt finds no allowed "
            "premise that fixes kappa_s.  The harness now supports explicit "
            "uniform scalar-source shifts and emits dE/ds response analysis, "
            "and the gauge-VEV source-overlap no-go blocks using v or gauge "
            "masses to identify the substrate source with canonical h.  The "
            "canonical kinetic renormalization condition also does not close "
            "the bridge: Z_h=1 fixes the h-field residue, not the source "
            "operator overlap <0|O_s|h>.  Source contact-term conventions do "
            "not close it either: C_ss(0) and C_ss'(0) can be fixed while the "
            "isolated pole residue changes.  This advances the Feynman-Hellmann "
            "measurement route but still does not convert to physical dE/dh "
            "without kappa_s.  Remaining "
            "closure requires production evidence or a genuinely new scalar "
            "LSZ/heavy-matching theorem.  The production Feynman-Hellmann "
            "protocol is now specified: common-ensemble symmetric source "
            "shifts, correlated dE/ds fits, and a separate scalar two-point "
            "LSZ measurement to determine kappa_s.  The same-source scalar "
            "two-point object C_ss(q) is now executable on a tiny exact lattice, "
            "but the reduced primitive has no controlled pole/continuum limit "
            "and its finite residue proxy is mass-dependent.  A finite "
            "Wilson-exchange scalar ladder total-momentum derivative can be "
            "computed, but the derivative magnitude is strongly "
            "prescription-sensitive and is not a retained limiting theorem.  "
            "A direct IR-limiting scout shows why: keeping the gauge zero mode "
            "makes the derivative grow and changes the pole-test crossing, "
            "while removing it gives a different stable surface.  The Cl(3)/Z3 "
            "source unit fixes the additive source coordinate but not the "
            "canonical Higgs field normalization.  The joint FH/LSZ production "
            "path now has exact launch commands, but the manifest is not "
            "production evidence; the postprocess gate now blocks any manifest "
            "or partial output from being used until production phase, same-source "
            "dE/ds, Gamma_ss(q), isolated-pole derivative, and FV/IR/zero-mode "
            "control are all present.  The checkpoint-granularity gate also "
            "shows the current harness resumes only completed per-volume "
            "artifacts, so a 12-hour foreground launch cannot produce safely "
            "checkpointed production evidence.  A chunked L12 production "
            "manifest gives foreground-sized launch commands, but it remains "
            "planning support and does not cover L16/L24 or the pole postprocess.  "
            "The chunk combiner gate now blocks absent, partial, or "
            "non-independent chunks and requires run-control plus numba "
            "seed-control provenance before L12 combination; the "
            "chunk commands now use chunk-local artifact directories and "
            "per-chunk resume to avoid cross-chunk artifact collisions.  "
            "Historical chunk001 and chunk002 completed as production-format "
            "L12 chunks, but the seed-independence audit demotes them: their "
            "metadata seeds differ while their gauge-evolution signatures "
            "match, and they lack the numba_gauge_seed_v1 marker.  They are "
            "not independent L12 evidence until rerun under the patched "
            "harness or explicitly excluded.  "
            "The pole-fit kinematics gate shows the current scalar modes give "
            "only one nonzero momentum shell, so four-mode chunk completion is "
            "not by itself an isolated-pole derivative.  "
            "The pole-fit postprocessor scaffold is now present, but the "
            "combined production input is absent/nonready, so it is not "
            "evidence.  A finite-shell identifiability no-go now tightens the "
            "same boundary: finite Euclidean Gamma_ss shell rows, even with a "
            "named pole, do not determine dGamma_ss/dp^2 without a model-class "
            "or analytic-continuation theorem.  The pole-fit model-class gate "
            "now blocks future finite-shell pole fits from retained use unless "
            "that missing theorem or an equivalent production acceptance "
            "certificate is present.  The Stieltjes model-class obstruction "
            "also shows positivity alone is not that certificate: positive "
            "continuum models can preserve finite shell rows and the pole while "
            "moving the residue.  The pole-saturation threshold gate turns the "
            "next repair into an executable condition: finite-shell pole fits "
            "remain blocked until the allowed positive-Stieltjes residue "
            "interval is made tight by pole-saturation, continuum-threshold "
            "control, or a scalar denominator theorem.  The threshold-authority "
            "audit finds no hidden current artifact that supplies that premise.  "
            "The Pade-Stieltjes bounds gate now tests the direct moment-theory "
            "bypass: it is a valid positive route only if a same-surface "
            "moment/threshold/FV certificate is supplied, and the current "
            "surface has no such certificate.  "
            "The finite-volume pole-saturation obstruction also blocks using "
            "finite-L discreteness as a substitute for a uniform gap.  "
            "The numba seed-independence audit closes the adjacent production "
            "quality gap before further chunk evidence is counted.  The "
            "uniform-gap self-certification no-go closes the matching analytic "
            "shortcut: finite shell rows do not prove a continuum threshold, "
            "even when a gapped model could have generated them.  The scalar "
            "denominator closure attempt checks the whole theorem stack and "
            "still finds the zero-mode prescription, scalar carrier/projector, "
            "K'(pole), model class, threshold, and seed-controlled production "
            "open.  The soft-continuum threshold no-go also blocks using "
            "color-singlet q=0 cancellation plus finite-q IR regularity as the "
            "missing threshold premise: local integrability does not exclude "
            "positive continuum spectral weight arbitrarily close to the pole.  "
            "The reflection-positivity shortcut no-go also blocks the broader "
            "OS positivity repair: reflection-positive positive-measure "
            "families can keep the finite shell rows fixed while changing the "
            "same-source pole residue.  The short-distance/OPE shortcut no-go "
            "also blocks UV operator normalization as LSZ closure: finite "
            "large-Q coefficients can stay fixed while the isolated IR "
            "source-pole residue varies.  The effective-mass plateau residue "
            "no-go blocks the finite-time postprocess shortcut too: identical "
            "finite-window effective masses do not identify the ground/source "
            "residue.  "
            "The finite source-shift derivative no-go also blocks treating one "
            "symmetric source radius as a zero-source FH derivative: identical "
            "E(-delta), E(0), E(+delta), and finite slopes can coexist with "
            "different dE/ds at zero.  "
            "The finite-source-linearity gate records the constructive repair "
            "but does not pass it: current chunks have one source radius, and "
            "the three-radius calibration manifest is not foreground evidence.  "
            "The autocorrelation/ESS gate also blocks counting current chunks "
            "as production evidence: plaquette autocorrelation is diagnostic, "
            "but target same-source dE/ds and C_ss(q) time series are absent.  "
            "The target time-series harness extension removes that "
            "instrumentation gap for future chunks, but its reduced smoke is "
            "not production evidence or scalar LSZ normalization.  "
            "The target-time-series Higgs-identity no-go then blocks treating "
            "even perfect same-source target statistics as canonical-Higgs "
            "identity: the source-coordinate limits can stay fixed while the "
            "canonical-Higgs Yukawa changes through an orthogonal top-coupled "
            "scalar.  The no-orthogonal-top-coupling selection-rule no-go "
            "blocks setting that orthogonal coupling to zero from current "
            "charges: an orthogonal neutral scalar with the same listed labels "
            "has the same allowed top-bilinear coupling.  The source-pole "
            "purity cross-correlator gate blocks source-only purity as well: "
            "C_ss and source response can stay fixed while the source-Higgs "
            "overlap changes unless C_sH, W/Z response, or a retained purity "
            "theorem is supplied.  The source-Higgs cross-correlator import "
            "audit confirms that C_sH is not already supplied by the current "
            "production harness or EW/Higgs notes.  The source-Higgs Gram "
            "purity gate records the future acceptance condition, but it is not "
            "passed because C_sH and C_HH pole residues are absent.  The "
            "source-Higgs builder and postprocessor now make the same test "
            "O_sp-normalized: the Legendre/LSZ source-pole operator supplies "
            "the unit-residue source side, and the future production gate must "
            "show Delta_spH = Res(C_HH) - Res(C_sp,H)^2 = 0 with |rho_spH| = 1.  "
            "No certified O_H/C_sH/C_HH pole certificate is present.  The "
            "neutral-scalar rank-one purity gate also fails: D17 carrier "
            "support is not a dynamical rank-one theorem for the neutral "
            "scalar response space.  The primitive-cone certificate gate now "
            "states the exact positive neutral-rank contract: a future "
            "same-surface neutral transfer matrix must be nonnegative, "
            "strongly connected, have a positive primitive power, certify the "
            "isolated pole and overlaps, and pass the shortcut firewall.  No "
            "such certificate is present.  "
            "The effective-potential Hessian/source-overlap no-go blocks using "
            "SSB radial curvature as the source-pole identity: canonical VEV, "
            "W/Z masses, and Hessian eigenvalues still leave the source "
            "operator direction free.  "
            "The scalar carrier/projector closure attempt confirms that the "
            "taste/projector side remains open as well: color-singlet support "
            "and unit taste-singlet algebra do not identify the physical "
            "carrier, preserve finite crossings under unit normalization, or "
            "derive K'(pole).  The K-prime closure attempt confirms the "
            "derivative itself remains named but unclosed: finite derivative "
            "proxies are blocked by limiting order, residue-envelope "
            "dependence, Ward/Feshbach non-identification, carrier/projector "
            "choice, and missing threshold control.  "
            "The mode/noise budget gives a possible eight-mode/eight-noise "
            "foreground launch option, but it is only planning support until "
            "a variance gate and production data exist.  The eight-mode noise "
            "variance gate now rejects the current evidence surface: the "
            "reduced smoke is wrong phase/modes/noises/statistics and the "
            "foreground chunk is absent or four-mode/x16, not an x8 "
            "calibration.  The harness now emits noise-subsample stability "
            "diagnostics for future paired x8/x16 calibrations, but the "
            "current diagnostic smokes are still reduced-scope instrumentation "
            "support only.  A paired x8/x16 calibration manifest now defines "
            "matched commands, but no completed calibration output exists.  "
            "The same-source sector-overlap identity obstruction now blocks a "
            "nearby shortcut in the gauge-normalized response route: common "
            "source-coordinate scaling cancels, but the ratio is physical y_t "
            "only after k_top/k_gauge is derived or measured.  A same-source "
            "label alone is not that theorem.  The W/Z response certificate "
            "builder now defines the candidate certificate and records absent "
            "same-source W/Z rows.  The gate rejects static EW algebra or "
            "slope-only W/Z outputs without production mass fits and identity "
            "certificates.  The top/W covariance gates now also reject deriving "
            "the matched covariance from marginals, native same-source labels, "
            "or deterministic W response alone; a paired row set or closed "
            "same-surface covariance theorem is still required.  The W/Z harness absence guard now "
            "records missing W/Z response rows directly in future production "
            "certificates; that guard is not evidence.  The source-pole/canonical-Higgs "
            "mixing obstruction now blocks the adjacent pole-identity shortcut: "
            "a same-source pole readout is the top coupling to the source pole, "
            "not physical y_t, unless the source pole is proved to be the "
            "canonical Higgs radial mode with no orthogonal scalar admixture.  "
            "The source-Higgs cross-correlator manifest now records the exact "
            "future O_H/C_sH/C_HH production schema, but it is support only "
            "because no such production rows or certificate exist.  "
            "The canonical-Higgs operator realization gate now records the "
            "missing object on the same surface: EW gauge-mass algebra assumes "
            "canonical H after it is supplied, but the PR #230 source harness "
            "does not yet implement O_H, C_sH, or C_HH pole residues.  "
            "The H_unit candidate gate now blocks the direct legacy substitute: "
            "H_unit is a named D17 bilinear, but without pole-purity and "
            "canonical-normalization certificates it is not the canonical O_H.  "
            "The source-Higgs harness absence guard now records missing "
            "O_H/C_sH/C_HH rows directly in future production certificates; "
            "that guard is not evidence.  "
            "The neutral-scalar commutant rank no-go now blocks the symmetry-only "
            "rank-one route: current neutral labels still admit a rank-two "
            "response family unless dynamics or C_sH/C_HH data remove it.  "
            "The dynamical rank-one closure attempt then shows the current "
            "dynamical surface still permits a finite orthogonal neutral pole "
            "with fixed source pole mass/residue and varying canonical-Higgs "
            "overlap.  The orthogonal-neutral decoupling no-go blocks using a "
            "finite/heavy mass gap as source-pole purity without a scaling "
            "theorem.  "
            "The refreshed retained-closure route "
            "certificate still authorizes no proposed-retained wording.  A "
            "pole-tuned finite ladder residue envelope also fails to select a "
            "unique LSZ input across current zero-mode, projector, and volume "
            "choices.  Existing Ward/gauge/Feshbach surfaces also do not fix "
            "the scalar kernel derivative K'(x_pole).  After color-singlet "
            "q=0 cancellation and finite-q IR regularity, zero-mode-removed "
            "finite ladder pole witnesses still remain volume, projector, "
            "taste-corner, and derivative sensitive; filtering non-origin "
            "taste corners removes the crossings, and the current import "
            "audit finds no retained scalar-carrier authority for those "
            "corners.  Normalized taste-singlet source weighting over the 16 "
            "corners rescales the finite witnesses by 1/16 and also removes "
            "every crossing.  Thus the finite ladder witnesses rely on an "
            "unfixed taste/projector normalization; the unit taste-singlet "
            "projector is only algebra until a physical scalar carrier and "
            "pole derivative theorem are derived.  With that unit projector, "
            "the finite ladder would need an underived scalar-kernel "
            "enhancement to cross, and no current retained import supplies it; "
            "fitting the multiplier to force a pole only imports the missing "
            "kernel normalization and leaves the residue proxy finite-row "
            "dependent.  "
            "They do not supply the "
            "interacting scalar pole/LSZ "
            "theorem.  The cycle-8 non-chunk current-surface exhaustion gate "
            "now records the queue-level consequence: without one of the named "
            "future same-surface artifacts, no further current-surface "
            "non-chunk shortcut remains to cycle.  The terminal route-"
            "exhaustion gate records the stop/reopen rule for that state.  "
            "The cycle-12 reopen-admissibility gate rejects a path-only "
            "reopen attempt before aggregate reruns.  The cycle-15 "
            "independent-route admission gate records that no independent "
            "current route is admitted without a new same-surface artifact.  "
            "The cycle-16 reopen-source guard records that the post-checkpoint "
            "surface has no admissible same-surface artifact to consume.  The "
            "cycle-18 reopen-freshness gate records that no post-cycle-17 "
            "same-surface artifact is present for admissible reopen.  The "
            "cycle-19 no-duplicate-route gate records that another "
            "current-surface route selection would only replay a closed "
            "non-chunk family until a fresh parseable same-surface artifact "
            "exists.  The cycle-20 process-gate continuation no-go records "
            "that another process-only gate is also not an admissible science "
            "route until that fresh same-surface artifact exists.  The cycle-21 "
            "remote-surface reopen guard records that fetched remote surfaces "
            "also contain no listed same-surface artifact for admissible reopen.  "
            "The cycle-22 main-audit-drift guard records that the latest "
            "origin/main advance is audit/effective-status drift only and "
            "supplies no listed PR230 same-surface artifact.  The cycle-23 "
            "main-effective-status-drift guard records that origin/main "
            "advanced again only on audit/effective-status surfaces and still "
            "supplies no listed PR230 same-surface artifact.  The cycle-24 "
            "post-cycle-23 main-status-drift guard records that origin/main "
            "advanced again only on audit/effective-status surfaces and still "
            "supplies no listed PR230 same-surface artifact.  The cycle-25 "
            "post-cycle-24 main-audit-status-drift guard records that "
            "origin/main advanced again only on audit/effective-status "
            "surfaces and still supplies no listed PR230 same-surface artifact.  "
            "The cycle-26 post-cycle-25 main-audit-status-drift guard records "
            "that origin/main advanced again only on audit/effective-status "
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
            "surfaces and still supplies no listed PR230 same-surface artifact."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": "Open imports remain across every non-production shortcut route.",
        "certificate_statuses": statuses,
        "remaining_routes": remaining_routes,
        "strict_non_claims": [
            "does not claim retained closure",
            "does not count non-independent historical chunks as production evidence",
            "does not use observed top mass or y_t as proof input",
            "does not allow H_unit matrix-element definition as y_t readout",
            "does not treat chunk completion alone as positive retained closure",
        ],
        "pass_count": PASS_COUNT,
        "fail_count": FAIL_COUNT,
    }
    result["verdict"] = (
        "The current PR #230 physics-loop checkpoint remains open.  All loaded "
        "non-production shortcuts are blocked, support-only, or conditional; "
        "complete chunk evidence alone would still miss scalar-LSZ control, a "
        "same-surface physical-readout bridge, matching/running authority, and "
        "proposal authorization.  The current-surface non-chunk exhaustion, "
        "future-artifact intake, and terminal route-exhaustion gates now record "
        "that no further current-surface non-chunk shortcut may be cycled until "
        "a named same-surface artifact exists and the aggregate gates are rerun.  "
        "The cycle-15 independent-route admission gate also records that no "
        "independent current route is admitted on this branch.  The cycle-16 "
        "reopen-source guard records that no post-checkpoint same-surface "
        "artifact is present for admissible reopen.  The cycle-17 stop-condition "
        "gate records that the refreshed non-chunk queue has no executable "
        "current-surface route on this branch.  The cycle-18 reopen-freshness "
        "gate records that no post-cycle-17 same-surface artifact is present "
        "for admissible reopen.  The cycle-19 no-duplicate-route gate records "
        "that another current-surface route selection would only replay a "
        "closed non-chunk family until a fresh parseable same-surface artifact "
        "exists.  The cycle-20 process-gate continuation no-go records that "
        "another process-only gate is also not an admissible science route "
        "until that fresh same-surface artifact exists.  The cycle-21 "
        "remote-surface reopen guard records that fetched remote surfaces "
        "also contain no listed same-surface artifact for admissible reopen.  "
        "The cycle-22 main-audit-drift guard records that the latest origin/main "
        "advance is audit/effective-status drift only and supplies no listed "
        "PR230 same-surface artifact.  The cycle-23 main-effective-status-drift "
        "guard records that origin/main advanced again only on "
        "audit/effective-status surfaces and still supplies no listed PR230 "
        "same-surface artifact.  The cycle-24 post-cycle-23 main-status-drift "
        "guard records that origin/main advanced again only on "
        "audit/effective-status surfaces and still supplies no listed PR230 "
        "same-surface artifact.  The cycle-25 post-cycle-24 "
        "main-audit-status-drift guard records that origin/main advanced again "
        "only on audit/effective-status surfaces and still supplies no listed "
        "PR230 same-surface artifact.  The cycle-26 post-cycle-25 "
        "main-audit-status-drift guard records that origin/main advanced again "
        "only on audit/effective-status surfaces and still supplies no listed "
        "PR230 same-surface artifact.  The cycle-27 post-cycle-26 "
        "main-audit-status-drift guard records that origin/main advanced again "
        "only on audit/effective-status surfaces and still supplies no listed "
        "PR230 same-surface artifact.  The cycle-28 post-cycle-27 "
        "main-audit-status-drift guard records that origin/main advanced again "
        "only on audit/effective-status surfaces and still supplies no listed "
        "PR230 same-surface artifact.  The cycle-29 post-cycle-28 "
        "main-audit-status-drift guard records that origin/main advanced again "
        "only on audit/effective-status surfaces and still supplies no listed "
        "PR230 same-surface artifact.  The cycle-30 post-cycle-29 "
        "main-audit-status-drift guard records that origin/main advanced again "
        "only on audit/effective-status surfaces and still supplies no listed "
        "PR230 same-surface artifact.  The cycle-31 post-cycle-30 "
        "main-audit-status-drift guard records that origin/main advanced again "
        "only on audit/effective-status surfaces and still supplies no listed "
        "PR230 same-surface artifact.  The cycle-32 post-cycle-31 "
        "main-audit-status-drift guard records that origin/main advanced again "
        "only on audit/effective-status surfaces and still supplies no listed "
        "PR230 same-surface artifact.  The cycle-33 post-cycle-32 "
        "main-audit-status-drift guard records that origin/main advanced again "
        "only on audit/effective-status/runner-cache surfaces and still "
        "supplies no listed PR230 same-surface artifact.  The neutral-scalar "
        "Burnside/double-commutant attempt records that the current source-only "
        "neutral generator algebra is not full and has a non-scalar commutant; "
        "it remains blocked until a same-surface off-diagonal neutral generator "
        "or primitive transfer certificate exists.  The taste-condensate "
        "O_H bridge audit also records that the existing Higgs/taste stack is "
        "not a PR230 O_H bridge on the current source surface: the uniform "
        "mass source has zero projection onto the trace-zero taste-axis Higgs "
        "operators, so that route requires source-coordinate transport or "
        "C_sH/C_HH pole rows before it can reopen.  The Schur and neutral "
        "primitive route completions add the same scoped boundary for two "
        "hard theorem routes: current Schur machinery lacks the neutral kernel "
        "basis plus same-surface A/B/C rows, and current conditional Perron/"
        "positivity support lacks a primitive transfer or off-diagonal "
        "generator theorem.  The same-surface Z3 taste-triplet artifact now "
        "supplies the exact cyclic action on the PR230 taste axes, but it "
        "does not supply the physical lazy transfer, source/Higgs row, or "
        "strict primitive certificate.  The first-principles "
        "O_H bridge candidate portfolio records the surviving positive "
        "candidate routes and keeps them open without authorizing closure.  "
        "The same-surface neutral multiplicity-one intake gate now makes "
        "the cleanest missing positive artifact executable and rejects the "
        "current two-singlet surface without authorizing O_H closure.  "
        "The OS transfer-kernel artifact gate now adds the time-direction "
        "boundary: scalar source/taste-radial rows are configuration "
        "timeseries at fixed finite covariance definitions, not same-surface "
        "C_ij(t) transfer/GEVP kernels, so static C_ss/C_sx/C_xx cannot "
        "determine the off-diagonal generator or source-Higgs pole overlap."
    )
    result["oh_bridge_candidate_portfolio_open"] = (
        oh_bridge_candidate_portfolio.get("candidate_portfolio_passed") is True
        and oh_bridge_candidate_portfolio.get("candidate_count") == 5
    )
    result["same_surface_neutral_multiplicity_one_gate_rejects_current_surface"] = (
        same_surface_neutral_multiplicity_gate.get("candidate_accepted") is False
        and same_surface_neutral_multiplicity_gate.get("proposal_allowed") is False
    )
    result["os_transfer_kernel_artifact_absent"] = (
        os_transfer_kernel_artifact_gate.get("os_transfer_kernel_artifact_present")
        is False
        and os_transfer_kernel_artifact_gate.get("same_surface_transfer_or_gevp_present")
        is False
        and os_transfer_kernel_artifact_gate.get("proposal_allowed") is False
    )
    result["source_higgs_time_kernel_harness_support_only"] = (
        source_higgs_time_kernel_harness_extension_gate.get("contract", {}).get(
            "adds_default_off_time_kernel_rows"
        )
        is True
        and source_higgs_time_kernel_harness_extension_gate.get("contract", {}).get(
            "selected_mass_only"
        )
        is True
        and source_higgs_time_kernel_harness_extension_gate.get("proposal_allowed")
        is False
        and source_higgs_time_kernel_harness_extension_gate.get(
            "used_as_physical_yukawa_readout"
        )
        is False
    )
    result["source_higgs_time_kernel_gevp_contract_support_only"] = (
        source_higgs_time_kernel_gevp_contract.get(
            "formal_gevp_diagnostic", {}
        ).get("available")
        is True
        and source_higgs_time_kernel_gevp_contract.get(
            "physical_pole_extraction_accepted"
        )
        is False
        and source_higgs_time_kernel_gevp_contract.get("proposal_allowed") is False
    )
    result["source_higgs_time_kernel_production_manifest_not_evidence"] = (
        source_higgs_time_kernel_production_manifest.get("proposal_allowed")
        is False
        and source_higgs_time_kernel_production_manifest.get(
            "closure_launch_authorized_now"
        )
        is False
        and source_higgs_time_kernel_production_manifest.get(
            "support_launch_authorized_now"
        )
        is False
        and source_higgs_time_kernel_production_manifest.get(
            "operator_certificate_is_canonical_oh"
        )
        is False
        and source_higgs_time_kernel_production_manifest.get(
            "time_kernel_schema_version"
        )
        == "source_higgs_time_kernel_v1"
        and source_higgs_time_kernel_production_manifest.get("chunk_count") == 63
    )
    result["fms_literature_source_overlap_intake_non_authority"] = (
        fms_literature_source_overlap_intake.get("literature_bridge_scope")
        == "non_derivation_context_only"
        and fms_literature_source_overlap_intake.get("proposal_allowed") is False
        and fms_literature_source_overlap_intake.get("current_blockers", {}).get(
            "canonical_oh_absent"
        )
        is True
        and fms_literature_source_overlap_intake.get("current_blockers", {}).get(
            "source_higgs_rows_absent"
        )
        is True
    )
    result["schur_higher_shell_production_contract_not_evidence"] = (
        "higher-shell Schur scalar-LSZ production contract"
        in str(statuses["pr230_schur_higher_shell_production_contract"])
        and schur_higher_shell_contract.get("proposal_allowed") is False
        and schur_higher_shell_contract.get(
            "higher_shell_schur_production_contract_passed"
        )
        is True
        and schur_higher_shell_contract.get("launch_allowed_now") is False
        and schur_higher_shell_contract.get(
            "current_four_mode_campaign_must_remain_unmixed"
        )
        is True
    )
    result["source_coordinate_transport_completion_blocks"] = (
        source_transport_completion.get("source_coordinate_transport_completion_passed")
        is True
        and source_transport_completion.get("proposal_allowed") is False
    )
    result["two_source_taste_radial_chart_support_not_closure"] = (
        two_source_taste_radial_chart.get("two_source_taste_radial_chart_support_passed")
        is True
        and two_source_taste_radial_chart.get("proposal_allowed") is False
        and two_source_taste_radial_chart.get("forbidden_firewall", {}).get(
            "identified_taste_radial_axis_with_canonical_oh"
        )
        is False
    )
    result["two_source_taste_radial_action_support_not_closure"] = (
        two_source_taste_radial_action.get("two_source_taste_radial_action_passed")
        is True
        and two_source_taste_radial_action.get("proposal_allowed") is False
        and two_source_taste_radial_action.get("operator_certificate_payload", {}).get(
            "canonical_higgs_operator_identity_passed"
        )
        is False
    )
    result["two_source_taste_radial_row_contract_support_not_closure"] = (
        two_source_taste_radial_row_contract.get(
            "two_source_taste_radial_row_contract_passed"
        )
        is True
        and two_source_taste_radial_row_contract.get("proposal_allowed") is False
        and two_source_taste_radial_row_contract.get("future_file_presence", {}).get(
            "taste_radial_production_rows"
        )
        is False
    )
    result["two_source_taste_radial_row_production_manifest_support_not_closure"] = (
        two_source_taste_radial_row_manifest.get("manifest_passed") is True
        and two_source_taste_radial_row_manifest.get("proposal_allowed") is False
        and two_source_taste_radial_row_manifest.get("dry_run_only") is True
        and two_source_taste_radial_row_manifest.get("future_combined_rows_present")
        is False
    )
    result["two_source_taste_radial_row_combiner_support_not_closure"] = (
        two_source_taste_radial_row_combiner.get("proposal_allowed") is False
        and two_source_combiner_support_boundary
        and two_source_taste_radial_row_combiner.get("fail_count") == 0
    )
    result["two_source_taste_radial_schur_subblock_support_not_closure"] = (
        two_source_taste_radial_schur_subblock.get(
            "two_source_taste_radial_schur_subblock_witness_passed"
        )
        is True
        and two_source_taste_radial_schur_subblock.get("proposal_allowed") is False
        and two_source_taste_radial_schur_subblock.get(
            "strict_schur_kernel_row_contract_passed"
        )
        is False
        and two_source_taste_radial_schur_subblock.get(
            "canonical_higgs_operator_identity_passed"
        )
        is False
    )
    result["two_source_taste_radial_kprime_finite_shell_scout_not_closure"] = (
        two_source_taste_radial_kprime_scout.get(
            "finite_shell_schur_kprime_scout_passed"
        )
        is True
        and two_source_taste_radial_kprime_scout.get("proposal_allowed") is False
        and two_source_taste_radial_kprime_scout.get(
            "strict_schur_kprime_authority_passed"
        )
        is False
        and two_source_taste_radial_kprime_scout.get(
            "pole_location_or_derivative_rows_present"
        )
        is False
        and two_source_taste_radial_kprime_scout.get(
            "canonical_higgs_operator_identity_passed"
        )
        is False
    )
    result["two_source_taste_radial_schur_abc_finite_rows_not_closure"] = (
        two_source_taste_radial_schur_abc_finite_rows.get(
            "two_source_taste_radial_schur_abc_finite_rows_passed"
        )
        is True
        and two_source_taste_radial_schur_abc_finite_rows.get("proposal_allowed") is False
        and two_source_taste_radial_schur_abc_finite_rows.get(
            "finite_schur_abc_rows_written"
        )
        is True
        and two_source_taste_radial_schur_abc_finite_rows.get(
            "strict_schur_abc_kernel_rows_written"
        )
        is False
        and two_source_taste_radial_schur_abc_finite_rows.get(
            "strict_schur_kprime_authority_passed"
        )
        is False
        and two_source_taste_radial_schur_abc_finite_rows.get(
            "canonical_higgs_operator_identity_passed"
        )
        is False
    )
    result[
        "two_source_taste_radial_schur_pole_lift_gate_blocks_endpoint_promotion"
    ] = (
        two_source_taste_radial_schur_pole_lift_gate.get(
            "two_source_taste_radial_schur_pole_lift_gate_passed"
        )
        is True
        and two_source_taste_radial_schur_pole_lift_gate.get("proposal_allowed") is False
        and two_source_taste_radial_schur_pole_lift_gate.get("strict_pole_lift_passed")
        is False
        and two_source_taste_radial_schur_pole_lift_gate.get(
            "endpoint_derivative_nonidentifiability_witness_passed"
        )
        is True
    )
    result["two_source_taste_radial_primitive_transfer_candidate_not_h3"] = (
        "finite C_sx rows do not certify a physical primitive neutral transfer"
        in str(statuses["pr230_two_source_taste_radial_primitive_transfer_candidate_gate"])
        and two_source_taste_radial_primitive_transfer_candidate_gate.get("proposal_allowed")
        is False
        and two_source_taste_radial_primitive_transfer_candidate_gate.get(
            "physical_transfer_candidate_accepted"
        )
        is False
        and two_source_taste_radial_primitive_transfer_candidate_gate.get(
            "finite_offdiagonal_correlation_support"
        )
        is True
        and two_source_taste_radial_primitive_transfer_candidate_gate.get(
            "finite_correlator_blocks_positive"
        )
        is True
    )
    result["orthogonal_top_coupling_exclusion_candidate_rejected"] = (
        "orthogonal-neutral top-coupling exclusion candidate rejected"
        in str(statuses["pr230_orthogonal_top_coupling_exclusion_candidate_gate"])
        and orthogonal_top_coupling_exclusion_candidate_gate.get("proposal_allowed")
        is False
        and orthogonal_top_coupling_exclusion_candidate_gate.get(
            "orthogonal_top_coupling_exclusion_candidate_accepted"
        )
        is False
        and orthogonal_top_coupling_exclusion_candidate_gate.get(
            "same_surface_selection_rule_present"
        )
        is False
        and orthogonal_top_coupling_exclusion_candidate_gate.get(
            "finite_c_sx_rows_are_top_coupling_tomography"
        )
        is False
    )
    result["strict_scalar_lsz_moment_fv_authority_absent"] = (
        "raw C_ss rows do not supply strict scalar-LSZ moment/FV authority"
        in str(statuses["pr230_strict_scalar_lsz_moment_fv_authority_gate"])
        and strict_scalar_lsz_moment_fv_authority_gate.get("proposal_allowed")
        is False
        and strict_scalar_lsz_moment_fv_authority_gate.get(
            "strict_scalar_lsz_moment_fv_authority_gate_passed"
        )
        is True
        and strict_scalar_lsz_moment_fv_authority_gate.get(
            "strict_scalar_lsz_moment_fv_authority_present"
        )
        is False
        and strict_scalar_lsz_moment_fv_authority_gate.get(
            "current_raw_c_ss_proxy_fails_stieltjes_monotonicity"
        )
        is True
    )
    result["schur_complement_stieltjes_repair_support_not_closure"] = (
        "Schur-complement Stieltjes repair split"
        in str(statuses["pr230_schur_complement_stieltjes_repair_gate"])
        and schur_complement_stieltjes_repair_gate.get("proposal_allowed") is False
        and schur_complement_stieltjes_repair_gate.get(
            "schur_complement_stieltjes_repair_gate_passed"
        )
        is True
        and schur_complement_stieltjes_repair_gate.get(
            "source_given_x_stieltjes_first_shell_failed"
        )
        is True
        and schur_complement_stieltjes_repair_gate.get(
            "x_given_source_stieltjes_first_shell_passed"
        )
        is True
        and schur_complement_stieltjes_repair_gate.get(
            "strict_scalar_lsz_authority_present"
        )
        is False
        and schur_complement_stieltjes_repair_gate.get(
            "canonical_higgs_operator_identity_passed"
        )
        is False
    )
    result["taste_radial_canonical_oh_selector_blocks_symmetry_shortcut"] = (
        taste_radial_selector_gate.get("taste_radial_canonical_oh_selector_gate_passed")
        is True
        and taste_radial_selector_gate.get("proposal_allowed") is False
        and taste_radial_selector_gate.get("degree_one_radial_unique") is True
        and taste_radial_selector_gate.get("full_invariant_selector_nonunique")
        is True
        and taste_radial_selector_gate.get("canonical_oh_selector_absent") is True
    )
    result["degree_one_higgs_action_premise_not_derived"] = (
        degree_one_higgs_action_premise_gate.get(
            "degree_one_higgs_action_premise_gate_passed"
        )
        is True
        and degree_one_higgs_action_premise_gate.get("proposal_allowed") is False
        and degree_one_higgs_action_premise_gate.get("degree_one_filter_selects_e1")
        is True
        and degree_one_higgs_action_premise_gate.get(
            "degree_one_premise_authorized_on_current_surface"
        )
        is False
    )
    result["fms_post_degree_route_rescore_support_not_proof"] = (
        fms_post_degree_route_rescore.get("fms_post_degree_route_rescore_passed")
        is True
        and fms_post_degree_route_rescore.get("proposal_allowed") is False
        and fms_post_degree_route_rescore.get("forbidden_firewall", {}).get(
            "used_literature_as_proof_authority"
        )
        is False
        and fms_post_degree_route_rescore.get("forbidden_firewall", {}).get(
            "used_degree_or_odd_parity_as_oh_authority"
        )
        is False
    )
    result["fms_composite_oh_conditional_support_not_proof"] = (
        fms_composite_oh_conditional_theorem.get(
            "fms_composite_oh_conditional_theorem_passed"
        )
        is True
        and fms_composite_oh_conditional_theorem.get("proposal_allowed") is False
        and fms_composite_oh_conditional_theorem.get(
            "current_closure_authority_present"
        )
        is False
        and fms_composite_oh_conditional_theorem.get("same_surface_action_absent")
        is True
        and fms_composite_oh_conditional_theorem.get("source_higgs_rows_absent")
        is True
    )
    result["fms_oh_candidate_action_packet_support_not_proof"] = (
        fms_oh_candidate_action_packet.get("fms_oh_candidate_action_packet_passed")
        is True
        and fms_oh_candidate_action_packet.get("proposal_allowed") is False
        and fms_oh_candidate_action_packet.get("accepted_current_surface") is False
        and fms_oh_candidate_action_packet.get("same_surface_cl3_z3_derived")
        is False
        and fms_oh_candidate_action_packet.get("external_extension_required")
        is True
        and fms_oh_candidate_action_packet.get("closure_authorized") is False
    )
    result["fms_source_overlap_readout_gate_support_not_proof"] = (
        fms_source_overlap_readout_gate.get(
            "fms_source_overlap_readout_gate_passed"
        )
        is True
        and fms_source_overlap_readout_gate.get("proposal_allowed") is False
        and fms_source_overlap_readout_gate.get("readout_executable_now") is False
        and fms_source_overlap_readout_gate.get("strict_rows_present") is False
        and fms_source_overlap_readout_gate.get("closure_authorized") is False
    )
    result["fms_action_adoption_minimal_cut_support_not_proof"] = (
        fms_action_adoption_minimal_cut.get(
            "fms_action_adoption_minimal_cut_passed"
        )
        is True
        and fms_action_adoption_minimal_cut.get("proposal_allowed") is False
        and fms_action_adoption_minimal_cut.get("adoption_allowed_now") is False
        and fms_action_adoption_minimal_cut.get("accepted_current_surface") is False
        and fms_action_adoption_minimal_cut.get("same_surface_cl3_z3_derived")
        is False
        and fms_action_adoption_minimal_cut.get("closure_authorized") is False
    )
    result["higgs_mass_source_action_bridge_support_not_proof"] = (
        higgs_mass_source_action_bridge.get("higgs_mass_source_action_bridge_passed")
        is True
        and higgs_mass_source_action_bridge.get("proposal_allowed") is False
        and higgs_mass_source_action_bridge.get(
            "same_surface_ew_action_certificate_absent"
        )
        is True
        and higgs_mass_source_action_bridge.get("canonical_oh_absent") is True
        and higgs_mass_source_action_bridge.get("source_higgs_rows_absent") is True
    )
    result["same_source_ew_higgs_action_ansatz_support_not_proof"] = (
        same_source_ew_higgs_action_ansatz_gate.get(
            "same_source_ew_higgs_action_ansatz_gate_passed"
        )
        is True
        and same_source_ew_higgs_action_ansatz_gate.get("proposal_allowed")
        is False
        and same_source_ew_higgs_action_ansatz_gate.get(
            "current_surface_adoption_passed"
        )
        is False
        and same_source_ew_higgs_action_ansatz_gate.get(
            "future_default_certificates_written"
        )
        is False
    )
    result["same_source_ew_action_adoption_attempt_blocks_ansatz_only_shortcut"] = (
        same_source_ew_action_adoption_attempt.get(
            "same_source_ew_action_adoption_attempt_passed"
        )
        is True
        and same_source_ew_action_adoption_attempt.get("proposal_allowed")
        is False
        and same_source_ew_action_adoption_attempt.get("adoption_allowed_now")
        is False
        and same_source_ew_action_adoption_attempt.get(
            "accepted_action_certificate_written_by_this_attempt"
        )
        is False
    )
    result["radial_spurion_sector_overlap_support_not_closure"] = (
        radial_spurion_sector_overlap_theorem.get(
            "radial_spurion_sector_overlap_theorem_passed"
        )
        is True
        and radial_spurion_sector_overlap_theorem.get("proposal_allowed") is False
        and radial_spurion_sector_overlap_theorem.get(
            "current_surface_sector_overlap_identity_supplied"
        )
        is False
        and radial_spurion_sector_overlap_theorem.get("current_surface_closure_authorized")
        is False
    )
    result["radial_spurion_action_contract_support_not_closure"] = (
        radial_spurion_action_contract.get("radial_spurion_action_contract_passed")
        is True
        and radial_spurion_action_contract.get("proposal_allowed") is False
        and radial_spurion_action_contract.get("current_surface_contract_satisfied")
        is False
        and radial_spurion_action_contract.get("accepted_action_certificate_written")
        is False
    )
    result["wz_response_ratio_identifiability_contract_support_not_closure"] = (
        wz_response_ratio_contract.get(
            "wz_response_ratio_identifiability_contract_passed"
        )
        is True
        and wz_response_ratio_contract.get("proposal_allowed") is False
        and wz_response_ratio_contract.get("current_surface_contract_satisfied")
        is False
        and wz_response_ratio_contract.get("future_response_ratio_row_packet_present")
        is False
        and wz_response_ratio_contract.get("strict_g2_authority_present") is False
        and wz_response_ratio_contract.get("matched_covariance_authority_present")
        is False
    )
    result["wz_same_source_action_minimal_certificate_cut_open"] = (
        wz_same_source_action_minimal_cut.get(
            "wz_same_source_action_minimal_certificate_cut_passed"
        )
        is True
        and wz_same_source_action_minimal_cut.get("proposal_allowed") is False
        and wz_same_source_action_minimal_cut.get(
            "current_surface_action_certificate_satisfied"
        )
        is False
        and set(wz_same_source_action_minimal_cut.get("root_certificate_cut_open", []))
        == {
            "same_surface_canonical_higgs_operator_certificate",
            "current_same_source_sector_overlap_identity",
            "wz_correlator_mass_fit_path_certificate",
        }
    )
    result["wz_physical_response_packet_intake_blocks_current_packet"] = (
        wz_physical_response_packet_intake.get(
            "wz_physical_response_packet_intake_checkpoint_passed"
        )
        is True
        and wz_physical_response_packet_intake.get("proposal_allowed") is False
        and wz_physical_response_packet_intake.get("production_packet_present")
        is False
        and not any(
            wz_physical_response_packet_intake.get(
                "production_roots_present", {}
            ).values()
        )
        and all(
            wz_physical_response_packet_intake.get(
                "scout_artifacts_present", {}
            ).values()
        )
    )
    result["wz_accepted_action_response_root_checkpoint_blocks_current_root"] = (
        wz_accepted_action_response_root_checkpoint.get("proposal_allowed")
        is False
        and wz_accepted_action_response_root_checkpoint.get(
            "wz_accepted_action_response_root_checkpoint_passed"
        )
        is True
        and wz_accepted_action_response_root_checkpoint.get("current_route_blocked")
        is True
        and wz_accepted_action_response_root_checkpoint.get("root_closures_found")
        == []
        and not any(
            wz_accepted_action_response_root_checkpoint.get(
                "future_artifact_presence", {}
            ).values()
        )
    )
    result["canonical_oh_wz_common_action_cut_open"] = (
        canonical_oh_wz_common_action_cut.get("proposal_allowed") is False
        and canonical_oh_wz_common_action_cut.get("common_action_cut_passed")
        is True
        and canonical_oh_wz_common_action_cut.get(
            "common_canonical_oh_vertex_open"
        )
        is True
        and canonical_oh_wz_common_action_cut.get("aggregate_denies_proposal")
        is True
        and canonical_oh_wz_common_action_cut.get("time_kernel_manifest_not_evidence")
        is True
    )
    result["canonical_oh_accepted_action_stretch_blocks_current_stack"] = (
        canonical_oh_accepted_action_stretch_attempt.get("proposal_allowed")
        is False
        and canonical_oh_accepted_action_stretch_attempt.get(
            "stretch_attempt_passed"
        )
        is True
        and canonical_oh_accepted_action_stretch_attempt.get("current_route_blocked")
        is True
        and canonical_oh_accepted_action_stretch_attempt.get("root_closures_found")
        == []
    )
    result["post_fms_source_overlap_necessity_blocks_current_inference"] = (
        post_fms_source_overlap_necessity_gate.get(
            "post_fms_source_overlap_necessity_gate_passed"
        )
        is True
        and post_fms_source_overlap_necessity_gate.get("proposal_allowed")
        is False
        and post_fms_source_overlap_necessity_gate.get(
            "current_source_overlap_authority_present"
        )
        is False
        and post_fms_source_overlap_necessity_gate.get(
            "two_source_rows_are_c_sx_not_c_sH"
        )
        is True
    )
    result["source_higgs_overlap_kappa_contract_support_not_proof"] = (
        source_higgs_overlap_kappa_contract.get(
            "source_higgs_overlap_kappa_contract_passed"
        )
        is True
        and source_higgs_overlap_kappa_contract.get("proposal_allowed") is False
        and source_higgs_overlap_kappa_contract.get("current_blockers", {}).get(
            "source_higgs_row_packet_absent"
        )
        is True
        and source_higgs_overlap_kappa_contract.get("forbidden_firewall", {}).get(
            "set_kappa_s_equal_one"
        )
        is False
    )
    for idx, two_source_chunk in two_source_chunks.items():
        result[f"two_source_taste_radial_chunk{idx:03d}_checkpoint_not_closure"] = (
            two_source_chunk.get("checkpoint_passed") is True
            and two_source_chunk.get("completed") is True
            and two_source_chunk.get("proposal_allowed") is False
            and two_source_chunk.get("chunk_summary", {}).get(
                "pole_residue_rows_count"
            )
            == 0
        )
    result["origin_main_composite_higgs_intake_not_closure"] = (
        origin_main_composite_higgs.get("origin_main_composite_higgs_intake_guard_passed")
        is True
        and origin_main_composite_higgs.get("origin_main_composite_higgs_closes_pr230")
        is False
        and origin_main_composite_higgs.get("proposal_allowed") is False
    )
    result["origin_main_ew_m_residual_intake_not_closure"] = (
        origin_main_ew_m_residual.get("origin_main_ew_m_residual_intake_guard_passed")
        is True
        and origin_main_ew_m_residual.get("origin_main_ew_m_residual_closes_pr230")
        is False
        and origin_main_ew_m_residual.get("proposal_allowed") is False
    )
    result["z3_triplet_conditional_primitive_not_closure"] = (
        z3_triplet_conditional_primitive.get(
            "z3_triplet_conditional_primitive_theorem_passed"
        )
        is True
        and z3_triplet_conditional_primitive.get("pr230_closure_authorized")
        is False
        and z3_triplet_conditional_primitive.get("proposal_allowed") is False
    )
    result["z3_triplet_positive_cone_h2_support_not_transfer"] = (
        z3_positive_cone_support.get("z3_triplet_positive_cone_h2_support_passed")
        is True
        and z3_positive_cone_support.get("pr230_closure_authorized") is False
        and z3_positive_cone_support.get("proposal_allowed") is False
        and z3_positive_cone_support.get("supplies_conditional_premises", {}).get(
            "H2_positive_cone_equal_magnitude_support"
        )
        is True
        and z3_positive_cone_support.get("supplies_conditional_premises", {}).get(
            "H3_lazy_positive_physical_transfer"
        )
        is False
    )
    result["z3_generation_action_lift_not_derived"] = (
        z3_generation_action_lift.get("h1_generation_action_lift_attempt_passed")
        is True
        and z3_generation_action_lift.get("same_surface_h1_derived") is False
        and z3_generation_action_lift.get("pr230_closure_authorized") is False
        and z3_generation_action_lift.get("proposal_allowed") is False
    )
    result["z3_lazy_transfer_promotion_not_derived"] = (
        z3_lazy_transfer_promotion.get("z3_lazy_transfer_promotion_attempt_passed")
        is True
        and z3_lazy_transfer_promotion.get("physical_lazy_transfer_instantiated")
        is False
        and z3_lazy_transfer_promotion.get("pr230_closure_authorized") is False
        and z3_lazy_transfer_promotion.get("proposal_allowed") is False
    )
    result["z3_lazy_selector_no_go_blocks"] = (
        z3_lazy_selector_no_go.get("z3_lazy_selector_no_go_passed") is True
        and z3_lazy_selector_no_go.get("physical_lazy_transfer_instantiated")
        is False
        and z3_lazy_selector_no_go.get("pr230_closure_authorized") is False
        and z3_lazy_selector_no_go.get("proposal_allowed") is False
    )
    result["same_surface_z3_taste_triplet_support_not_closure"] = (
        same_surface_z3_taste_triplet.get("same_surface_z3_triplet_artifact_passed")
        is True
        and same_surface_z3_taste_triplet.get("pr230_closure_authorized")
        is False
        and same_surface_z3_taste_triplet.get("proposal_allowed") is False
    )
    result["action_first_route_completion_blocks"] = (
        action_first_route_completion.get("action_first_route_completion_passed") is True
        and action_first_route_completion.get("proposal_allowed") is False
    )
    result["wz_response_route_completion_blocks"] = (
        wz_response_route_completion.get("wz_response_route_completion_passed") is True
        and wz_response_route_completion.get("proposal_allowed") is False
    )
    result["source_higgs_bridge_aperture_support_not_closure"] = (
        source_higgs_bridge_aperture_checkpoint.get(
            "source_higgs_bridge_aperture_checkpoint_passed"
        )
        is True
        and source_higgs_bridge_aperture_checkpoint.get("proposal_allowed")
        is False
        and source_higgs_bridge_aperture_checkpoint.get(
            "current_surface_closure_satisfied"
        )
        is False
        and source_higgs_aperture_combiner_boundary
    )
    result["fresh_artifact_intake_checkpoint_no_new_artifact"] = (
        fresh_artifact_intake_checkpoint.get("proposal_allowed") is False
        and fresh_artifact_intake_checkpoint.get("consumed_committed_pr_head_only")
        is True
        and fresh_artifact_intake_checkpoint.get("live_chunk_worker", {}).get(
            "touched"
        )
        is False
        and fresh_artifact_intake_checkpoint.get("live_chunk_worker", {}).get(
            "inspected_active_output"
        )
        is False
        and fresh_artifact_intake_checkpoint.get("checks", {}).get(
            "no_closure_artifact_present"
        )
        is True
        and fresh_artifact_intake_checkpoint.get("source_higgs_route", {}).get(
            "closure_artifact_present"
        )
        is False
        and fresh_artifact_intake_checkpoint.get("wz_route", {}).get(
            "strict_packet_present"
        )
        is False
    )
    result["block23_remote_candidate_intake_no_admissible_packet"] = (
        block23_remote_candidate_intake.get("proposal_allowed") is False
        and block23_remote_candidate_intake.get("live_chunk_worker", {}).get(
            "touched"
        )
        is False
        and block23_remote_candidate_intake.get("live_chunk_worker", {}).get(
            "inspected_active_output"
        )
        is False
        and block23_remote_candidate_intake.get("checks", {}).get(
            "no-candidate-ref-has-strict-source-packet"
        )
        is True
        and block23_remote_candidate_intake.get("checks", {}).get(
            "no-candidate-ref-has-strict-wz-packet"
        )
        is True
        and block23_remote_candidate_intake.get("checks", {}).get(
            "no-candidate-ref-has-strict-neutral-packet"
        )
        is True
        and block23_remote_candidate_intake.get("checks", {}).get(
            "no-admissible-remote-required-paths-found"
        )
        is True
        and block23_remote_candidate_intake.get("checks", {}).get(
            "forbidden-firewall-clean"
        )
        is True
    )
    result["block24_queue_pivot_admission_no_route_admitted"] = (
        block24_queue_pivot_admission.get("proposal_allowed") is False
        and block24_queue_pivot_admission.get("live_chunk_worker", {}).get(
            "touched"
        )
        is False
        and block24_queue_pivot_admission.get("live_chunk_worker", {}).get(
            "inspected_active_output"
        )
        is False
        and block24_queue_pivot_admission.get("checks", {}).get(
            "only-block23-checkpoint-since-last-scanned-physics-head"
        )
        is True
        and block24_queue_pivot_admission.get("checks", {}).get(
            "queue-rank1-source-higgs-not-admitted"
        )
        is True
        and block24_queue_pivot_admission.get("checks", {}).get(
            "queue-rank2-wz-not-admitted"
        )
        is True
        and block24_queue_pivot_admission.get("checks", {}).get(
            "queue-rank3-neutral-h3h4-not-admitted"
        )
        is True
        and block24_queue_pivot_admission.get("checks", {}).get(
            "chunk063-and-combined-rows-not-committed"
        )
        is True
        and block24_queue_pivot_admission.get("checks", {}).get(
            "forbidden-firewall-clean"
        )
        is True
    )
    result["block25_post_block24_landed_no_route_admitted"] = (
        block25_post_block24_landed.get("proposal_allowed") is False
        and block25_post_block24_landed.get("live_chunk_worker", {}).get(
            "touched"
        )
        is False
        and block25_post_block24_landed.get("live_chunk_worker", {}).get(
            "inspected_active_output"
        )
        is False
        and block25_post_block24_landed.get("checks", {}).get(
            "only-block24-checkpoint-since-block24-input-head"
        )
        is True
        and block25_post_block24_landed.get("checks", {}).get(
            "queue-rank1-source-higgs-not-admitted"
        )
        is True
        and block25_post_block24_landed.get("checks", {}).get(
            "queue-rank2-wz-not-admitted"
        )
        is True
        and block25_post_block24_landed.get("checks", {}).get(
            "queue-rank3-neutral-h3h4-not-admitted"
        )
        is True
        and block25_post_block24_landed.get("checks", {}).get(
            "chunk063-and-combined-rows-not-committed"
        )
        is True
        and block25_post_block24_landed.get("checks", {}).get(
            "forbidden-firewall-clean"
        )
        is True
    )
    result["block26_post_block25_landed_no_route_admitted"] = (
        block26_post_block25_landed.get("proposal_allowed") is False
        and block26_post_block25_landed.get("live_chunk_worker", {}).get(
            "touched"
        )
        is False
        and block26_post_block25_landed.get("live_chunk_worker", {}).get(
            "inspected_active_output"
        )
        is False
        and block26_post_block25_landed.get("checks", {}).get(
            "only-block25-checkpoint-since-block25-input-head"
        )
        is True
        and block26_post_block25_landed.get("checks", {}).get(
            "queue-rank1-source-higgs-not-admitted"
        )
        is True
        and block26_post_block25_landed.get("checks", {}).get(
            "queue-rank2-wz-not-admitted"
        )
        is True
        and block26_post_block25_landed.get("checks", {}).get(
            "queue-rank3-neutral-h3h4-not-admitted"
        )
        is True
        and block26_post_block25_landed.get("checks", {}).get(
            "chunk063-and-combined-rows-not-committed"
        )
        is True
        and block26_post_block25_landed.get("checks", {}).get(
            "forbidden-firewall-clean"
        )
        is True
    )
    result["block27_post_block26_landed_no_route_admitted"] = (
        block27_post_block26_landed.get("proposal_allowed") is False
        and block27_post_block26_landed.get("live_chunk_worker", {}).get(
            "touched"
        )
        is False
        and block27_post_block26_landed.get("live_chunk_worker", {}).get(
            "inspected_active_output"
        )
        is False
        and block27_post_block26_landed.get("checks", {}).get(
            "only-block26-checkpoint-since-block26-input-head"
        )
        is True
        and block27_post_block26_landed.get("checks", {}).get(
            "queue-rank1-source-higgs-not-admitted"
        )
        is True
        and block27_post_block26_landed.get("checks", {}).get(
            "queue-rank2-wz-not-admitted"
        )
        is True
        and block27_post_block26_landed.get("checks", {}).get(
            "queue-rank3-neutral-h3h4-not-admitted"
        )
        is True
        and block27_post_block26_landed.get("checks", {}).get(
            "chunk063-and-combined-rows-not-committed"
        )
        is True
        and block27_post_block26_landed.get("checks", {}).get(
            "forbidden-firewall-clean"
        )
        is True
    )
    result["block28_degree_one_oh_support_intake_not_closure"] = (
        block28_degree_one_oh_support_intake.get("proposal_allowed") is False
        and block28_degree_one_oh_support_intake.get("live_chunk_worker", {}).get(
            "touched"
        )
        is False
        and block28_degree_one_oh_support_intake.get("live_chunk_worker", {}).get(
            "inspected_active_output"
        )
        is False
        and block28_degree_one_oh_support_intake.get("checks", {}).get(
            "only-block27-checkpoint-since-block27-input-head"
        )
        is True
        and block28_degree_one_oh_support_intake.get("checks", {}).get(
            "degree-one-oh-support-loaded"
        )
        is True
        and block28_degree_one_oh_support_intake.get("checks", {}).get(
            "degree-one-action-premise-still-missing"
        )
        is True
        and block28_degree_one_oh_support_intake.get("checks", {}).get(
            "source-higgs-route-not-admitted"
        )
        is True
        and block28_degree_one_oh_support_intake.get("checks", {}).get(
            "wz-route-not-admitted"
        )
        is True
        and block28_degree_one_oh_support_intake.get("checks", {}).get(
            "neutral-h3h4-route-not-admitted"
        )
        is True
        and block28_degree_one_oh_support_intake.get("checks", {}).get(
            "forbidden-firewall-clean"
        )
        is True
    )
    result["block29_post_block28_wz_pivot_not_admitted"] = (
        block29_post_block28_wz_pivot_admission.get("proposal_allowed") is False
        and block29_post_block28_wz_pivot_admission.get(
            "live_chunk_worker", {}
        ).get("touched")
        is False
        and block29_post_block28_wz_pivot_admission.get(
            "live_chunk_worker", {}
        ).get("inspected_active_output")
        is False
        and block29_post_block28_wz_pivot_admission.get("checks", {}).get(
            "only-block28-support-since-block28-input-head"
        )
        is True
        and block29_post_block28_wz_pivot_admission.get("checks", {}).get(
            "block28-exact-support-no-closure"
        )
        is True
        and block29_post_block28_wz_pivot_admission.get("checks", {}).get(
            "source-higgs-route-blocked-after-block28"
        )
        is True
        and block29_post_block28_wz_pivot_admission.get("checks", {}).get(
            "wz-pivot-selected-after-source-higgs-block"
        )
        is True
        and block29_post_block28_wz_pivot_admission.get("checks", {}).get(
            "wz-pivot-not-admitted-without-required-packet"
        )
        is True
        and block29_post_block28_wz_pivot_admission.get("checks", {}).get(
            "forbidden-firewall-clean"
        )
        is True
    )
    result["block30_full_approach_review_not_closure"] = (
        block30_full_approach_review.get("proposal_allowed") is False
        and block30_full_approach_review.get("bare_retained_allowed") is False
        and block30_full_approach_review.get("audit_required_before_effective_retained")
        is True
        and block30_full_approach_review.get("fails") == 0
        and len(block30_full_approach_review.get("assumptions_exercise", [])) >= 16
        and len(block30_full_approach_review.get("literature_search", [])) >= 5
        and len(block30_full_approach_review.get("math_search", [])) >= 6
        and len(block30_full_approach_review.get("repo_bridge_cross_check", [])) >= 10
        and block30_full_approach_review.get("elon_exercise", {}).get(
            "canonical_skill_section_found"
        )
        is False
        and len(
            block30_full_approach_review.get("elon_exercise", {}).get(
                "zeroth_principles_chain", []
            )
        )
        >= 5
        and all(
            value is True
            for value in block30_full_approach_review.get(
                "parent_presence", {}
            ).values()
        )
    )
    result["block35_post_block34_physical_bridge_not_admitted"] = (
        block35_post_block34_bridge_admission.get("proposal_allowed") is False
        and block35_post_block34_bridge_admission.get("bare_retained_allowed")
        is False
        and block35_post_block34_bridge_admission.get(
            "block35_post_block34_physical_bridge_admission_checkpoint_passed"
        )
        is True
        and block35_post_block34_bridge_admission.get("live_chunk_worker", {}).get(
            "touched"
        )
        is False
        and block35_post_block34_bridge_admission.get("live_chunk_worker", {}).get(
            "inspected_active_output"
        )
        is False
        and block35_post_block34_bridge_admission.get("checks", {}).get(
            "post-block30-inputs-support-only"
        )
        is True
        and block35_post_block34_bridge_admission.get("checks", {}).get(
            "chunk063-package-committed-support-only"
        )
        is True
        and block35_post_block34_bridge_admission.get("checks", {}).get(
            "promotion-contract-committed-support-only"
        )
        is True
        and block35_post_block34_bridge_admission.get("checks", {}).get(
            "os-transfer-alias-firewall-committed-support-only"
        )
        is True
        and block35_post_block34_bridge_admission.get("checks", {}).get(
            "additive-top-support-committed-support-only"
        )
        is True
        and block35_post_block34_bridge_admission.get("checks", {}).get(
            "source-higgs-physical-bridge-not-admitted"
        )
        is True
        and block35_post_block34_bridge_admission.get("checks", {}).get(
            "wz-physical-response-not-admitted"
        )
        is True
        and block35_post_block34_bridge_admission.get("checks", {}).get(
            "neutral-h3h4-not-admitted"
        )
        is True
        and block35_post_block34_bridge_admission.get("checks", {}).get(
            "forbidden-firewall-clean"
        )
        is True
    )
    result["schur_route_completion_blocks"] = (
        schur_route_completion.get("schur_route_completion_passed") is True
        and schur_route_completion.get("proposal_allowed") is False
    )
    result["schur_x_given_source_one_pole_scout_not_authority"] = (
        schur_one_pole_scout_not_authority
    )
    result["neutral_primitive_route_completion_blocks"] = (
        neutral_primitive_route_completion.get("neutral_primitive_route_completion_passed")
        is True
        and neutral_primitive_route_completion.get("proposal_allowed") is False
    )
    result["neutral_primitive_h3h4_aperture_support_not_closure"] = (
        neutral_primitive_h3h4_aperture_checkpoint.get(
            "neutral_primitive_h3h4_aperture_checkpoint_passed"
        )
        is True
        and neutral_primitive_h3h4_aperture_checkpoint.get("proposal_allowed")
        is False
        and neutral_primitive_h3h4_aperture_checkpoint.get(
            "current_surface_closure_satisfied"
        )
        is False
        and neutral_h3h4_current_prefix
        and neutral_h3h4_diagnostics.get("finite_rows_rank_one_flat") is False
    )
    result["strict_non_claims"] = [
        "does not claim retained closure",
        "does not count non-independent historical chunks as production evidence",
        "does not use external target values as proof inputs",
        "does not allow forbidden matrix-element, operator, coupling, target, or unit shortcuts",
        "does not treat chunk completion alone as positive retained closure",
        "does not treat process-only gates as proof inputs",
        "does not treat remote branch drift as same-surface physics evidence",
        "does not treat fetched Higgs/EW remote branches as PR230 same-surface artifacts without parseable required-path certificates",
        "does not treat the block23 checkpoint commit as a new physics packet or admit a queue item without explicit production/certificate inputs",
        "does not treat the block24 checkpoint commit as a new physics packet or admit a queue item without explicit production/certificate inputs",
        "does not treat the block25 checkpoint commit as a new physics packet or admit a queue item without explicit production/certificate inputs",
        "does not treat the block26 checkpoint commit as a new physics packet or admit a queue item without explicit production/certificate inputs",
        "does not treat the block27 checkpoint commit or the degree-one O_H support intake as actual canonical O_H/source-Higgs pole-row closure",
        "does not treat the post-block28 W/Z pivot admission checkpoint as accepted-action response evidence",
        "does not treat the block30 assumptions/first-principles/literature/math/repo-bridge review as PR230 top-Yukawa closure",
        "does not treat the block35 post-block34 physical-bridge admission checkpoint as a new source-Higgs, W/Z, or neutral H3/H4 production artifact",
        "does not treat origin/main audit/effective-status drift as same-surface physics evidence",
        "does not treat repeated origin/main effective-status drift as same-surface physics evidence",
        "does not treat post-cycle-24 origin/main audit/effective-status drift as same-surface physics evidence",
        "does not treat post-cycle-25 origin/main audit/effective-status drift as same-surface physics evidence",
        "does not treat post-cycle-26 origin/main audit/effective-status drift as same-surface physics evidence",
        "does not treat post-cycle-27 origin/main audit/effective-status drift as same-surface physics evidence",
        "does not treat post-cycle-28 origin/main audit/effective-status drift as same-surface physics evidence",
        "does not treat the same-surface neutral multiplicity-one intake gate as accepted O_H authority",
        "does not treat post-cycle-29 origin/main audit/effective-status drift as same-surface physics evidence",
        "does not treat post-cycle-30 origin/main audit/effective-status drift as same-surface physics evidence",
        "does not treat post-cycle-31 origin/main audit/effective-status drift as same-surface physics evidence",
        "does not treat post-cycle-32 origin/main audit/effective-status/runner-cache drift as same-surface physics evidence",
        "does not treat Burnside/double-commutant theorem names as proof without same-surface neutral generators",
        "does not treat the Higgs/taste condensate stack as PR230 O_H authority",
        "does not treat cross-lane composite-Higgs stretch packets as PR230 O_H authority",
        "does not treat conditional Z3-triplet primitive support as a strict PR230 primitive certificate",
        "does not treat Koide/lepton Z3 as a quark-bilinear generation-action certificate",
        "does not treat the two-source taste-radial chart as canonical O_H or source-Higgs production rows",
        "does not treat the two-source taste-radial row production manifest as row data or pole evidence",
        "does not treat degree-one taste-radial uniqueness as canonical O_H without a same-surface degree-one Higgs-action premise",
        "does not treat FMS/lattice literature or method names as PR230 proof authority",
        "does not treat the FMS source-overlap readout formula as executable before accepted action, canonical O_H, and strict C_ss/C_sH/C_HH rows exist",
        "does not treat the same-source EW/Higgs action ansatz as adopted current-surface action authority",
        "does not treat the same-source EW action adoption attempt as an accepted action certificate",
        "does not treat the radial-spurion sector-overlap theorem as current additive-source sector-overlap closure",
        "does not treat two completed taste-radial chunks as combined L12 pole evidence, canonical O_H, or scalar LSZ normalization",
        "does not treat Schur sufficiency or row-definition machinery as proof without same-surface neutral-kernel A/B/C rows",
        "does not treat determinant positivity, conditional Perron support, or source-only generators as a primitive neutral rank-one theorem",
        "does not treat the C_x|s one-pole interpolation as a physical scalar pole or residue authority",
        (
            "does not treat the source-Higgs bridge aperture checkpoint or "
            f"{source_higgs_aperture_ready}/63 C_sx/C_xx chunks as canonical "
            "O_H or C_sH/C_HH closure"
        ),
        (
            "does not treat the neutral primitive H3/H4 aperture checkpoint, "
            "H1/H2 Z3 support, or finite C_sx/C_xx covariance rows as physical "
            "neutral transfer, primitive-cone, or source/canonical-Higgs coupling "
            "authority"
        ),
    ]
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"\nWrote certificate: {OUTPUT.relative_to(ROOT)}")
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
