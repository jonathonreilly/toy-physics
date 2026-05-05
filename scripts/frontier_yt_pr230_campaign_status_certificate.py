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
        "fh-lsz-production-postprocess-gate-not-ready",
        "postprocess gate" in str(statuses["fh_lsz_production_postprocess_gate"])
        or "open" in str(statuses["fh_lsz_production_postprocess_gate"]),
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
        is False,
        statuses["source_higgs_production_readiness_gate"],
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
            "route": "current-surface non-chunk queue exhausted",
            "needed": "a new same-surface row, certificate, or theorem before continuing non-chunk shortcut cycling",
        },
        {
            "route": "terminal non-chunk route exhaustion",
            "needed": "do not reopen until a named same-surface artifact exists and aggregate gates are rerun",
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
            "harness momentum fields.  A bounded two-volume pilot has large "
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
            "reopen attempt before aggregate reruns."
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
        "a named same-surface artifact exists and the aggregate gates are rerun."
    )
    result["strict_non_claims"] = [
        "does not claim retained closure",
        "does not count non-independent historical chunks as production evidence",
        "does not use external target values as proof inputs",
        "does not allow forbidden matrix-element, operator, coupling, target, or unit shortcuts",
        "does not treat chunk completion alone as positive retained closure",
    ]
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"\nWrote certificate: {OUTPUT.relative_to(ROOT)}")
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
