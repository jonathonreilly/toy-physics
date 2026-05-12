#!/usr/bin/env python3
"""
PR #230 retained-closure route certificate.

This runner answers the operational question: what is the shortest honest path
from the current PR #230 state to retained top-Yukawa closure?  It does not
claim closure.  It verifies that all non-MC shortcuts currently tested are
blocked or conditional, then records the only remaining closure routes.
"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "yt_retained_closure_route_certificate_2026-05-01.json"
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


def load_json(path: str) -> dict:
    full = ROOT / path
    if not full.exists():
        return {}
    return json.loads(full.read_text(encoding="utf-8"))


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
    print("PR #230 retained-closure route certificate")
    print("=" * 72)

    required_certificates = {
        "global_proof_audit": "outputs/yt_pr230_global_proof_audit_2026-05-01.json",
        "direct_cutoff_obstruction": "outputs/yt_top_mass_cutoff_obstruction_2026-05-01.json",
        "beta_lambda_no_go": "outputs/yt_beta_lambda_planck_stationarity_no_go_2026-05-01.json",
        "queue_exhaustion": "outputs/yt_pr230_queue_exhaustion_certificate_2026-05-01.json",
        "ward_repair_audit": "outputs/yt_ward_physical_readout_repair_audit_2026-05-01.json",
        "scalar_pole_residue_no_go": "outputs/yt_scalar_pole_residue_current_surface_no_go_2026-05-01.json",
        "key_blocker_closure_attempt": "outputs/yt_key_blocker_closure_attempt_2026-05-01.json",
        "lsz_normalization_cancellation": "outputs/yt_scalar_lsz_normalization_cancellation_2026-05-01.json",
        "feshbach_response_boundary": "outputs/yt_feshbach_operator_response_boundary_2026-05-01.json",
        "interacting_kinetic_sensitivity": "outputs/yt_interacting_kinetic_background_sensitivity_2026-05-01.json",
        "fh_lsz_invariant_readout": "outputs/yt_fh_lsz_invariant_readout_theorem_2026-05-01.json",
        "scalar_ladder_derivative_limit": "outputs/yt_scalar_ladder_derivative_limit_obstruction_2026-05-01.json",
        "scalar_ladder_residue_envelope": "outputs/yt_scalar_ladder_residue_envelope_obstruction_2026-05-01.json",
        "scalar_kernel_ward_identity": "outputs/yt_scalar_kernel_ward_identity_obstruction_2026-05-01.json",
        "scalar_zero_mode_limit_order": "outputs/yt_scalar_zero_mode_limit_order_theorem_2026-05-01.json",
        "zero_mode_prescription_import": "outputs/yt_zero_mode_prescription_import_audit_2026-05-01.json",
        "flat_toron_denominator": "outputs/yt_flat_toron_scalar_denominator_obstruction_2026-05-01.json",
        "flat_toron_washout": "outputs/yt_flat_toron_thermodynamic_washout_2026-05-01.json",
        "color_singlet_zero_mode": "outputs/yt_color_singlet_zero_mode_cancellation_2026-05-01.json",
        "color_singlet_finite_q_ir": "outputs/yt_color_singlet_finite_q_ir_regular_2026-05-01.json",
        "color_singlet_zero_mode_removed_ladder_pole_search": "outputs/yt_color_singlet_zero_mode_removed_ladder_pole_search_2026-05-01.json",
        "taste_corner_ladder_pole_obstruction": "outputs/yt_taste_corner_ladder_pole_obstruction_2026-05-01.json",
        "taste_carrier_import_audit": "outputs/yt_taste_carrier_import_audit_2026-05-01.json",
        "taste_singlet_ladder_normalization": "outputs/yt_taste_singlet_ladder_normalization_boundary_2026-05-01.json",
        "scalar_taste_projector_normalization_attempt": "outputs/yt_scalar_taste_projector_normalization_attempt_2026-05-01.json",
        "unit_projector_pole_threshold": "outputs/yt_unit_projector_pole_threshold_obstruction_2026-05-01.json",
        "scalar_kernel_enhancement_import": "outputs/yt_scalar_kernel_enhancement_import_audit_2026-05-01.json",
        "fitted_kernel_residue_selector": "outputs/yt_fitted_kernel_residue_selector_no_go_2026-05-01.json",
        "cl3_source_unit": "outputs/yt_cl3_source_unit_normalization_no_go_2026-05-01.json",
        "gauge_vev_source_overlap": "outputs/yt_gauge_vev_source_overlap_no_go_2026-05-01.json",
        "scalar_renormalization_condition_overlap": "outputs/yt_scalar_renormalization_condition_overlap_no_go_2026-05-01.json",
        "scalar_source_contact_term_scheme": "outputs/yt_scalar_source_contact_term_scheme_boundary_2026-05-01.json",
        "fh_lsz_production_manifest": "outputs/yt_fh_lsz_production_manifest_2026-05-01.json",
        "fh_lsz_production_postprocess_gate": "outputs/yt_fh_lsz_production_postprocess_gate_2026-05-01.json",
        "fh_lsz_production_checkpoint_granularity": "outputs/yt_fh_lsz_production_checkpoint_granularity_gate_2026-05-01.json",
        "fh_lsz_chunked_production_manifest": "outputs/yt_fh_lsz_chunked_production_manifest_2026-05-01.json",
        "fh_lsz_chunk_combiner_gate": "outputs/yt_fh_lsz_chunk_combiner_gate_2026-05-01.json",
        "fh_lsz_chunk001_checkpoint": "outputs/yt_fh_lsz_chunk001_checkpoint_certificate_2026-05-02.json",
        "fh_lsz_chunk002_checkpoint": "outputs/yt_fh_lsz_chunk002_checkpoint_certificate_2026-05-02.json",
        "fh_lsz_ready_chunk_set_checkpoint": "outputs/yt_fh_lsz_ready_chunk_set_checkpoint_2026-05-02.json",
        "fh_lsz_ready_chunk_response_stability": "outputs/yt_fh_lsz_ready_chunk_response_stability_2026-05-02.json",
        "fh_lsz_chunk011_target_timeseries": "outputs/yt_fh_lsz_chunk011_target_timeseries_checkpoint_2026-05-02.json",
        "fh_lsz_chunk011_target_timeseries_generic": "outputs/yt_fh_lsz_chunk011_target_timeseries_generic_checkpoint_2026-05-02.json",
        "fh_lsz_chunk012_target_timeseries_generic": "outputs/yt_fh_lsz_chunk012_target_timeseries_generic_checkpoint_2026-05-02.json",
        "fh_lsz_pole_fit_kinematics": "outputs/yt_fh_lsz_pole_fit_kinematics_gate_2026-05-01.json",
        "fh_lsz_pole_fit_postprocessor": "outputs/yt_fh_lsz_pole_fit_postprocessor_2026-05-01.json",
        "fh_lsz_finite_shell_identifiability": "outputs/yt_fh_lsz_finite_shell_identifiability_no_go_2026-05-02.json",
        "fh_lsz_pole_fit_model_class_gate": "outputs/yt_fh_lsz_pole_fit_model_class_gate_2026-05-02.json",
        "fh_lsz_model_class_semantic_firewall": "outputs/yt_fh_lsz_model_class_semantic_firewall_2026-05-04.json",
        "fh_lsz_stieltjes_model_class": "outputs/yt_fh_lsz_stieltjes_model_class_obstruction_2026-05-02.json",
        "fh_lsz_stieltjes_moment_certificate_gate": "outputs/yt_fh_lsz_stieltjes_moment_certificate_gate_2026-05-05.json",
        "fh_lsz_pade_stieltjes_bounds_gate": "outputs/yt_fh_lsz_pade_stieltjes_bounds_gate_2026-05-05.json",
        "fh_lsz_polefit8x8_stieltjes_proxy_diagnostic": "outputs/yt_fh_lsz_polefit8x8_stieltjes_proxy_diagnostic_2026-05-05.json",
        "fh_lsz_complete_bernstein_inverse_diagnostic": "outputs/yt_fh_lsz_complete_bernstein_inverse_diagnostic_2026-05-05.json",
        "pr230_scalar_lsz_holonomic_exact_authority_attempt": "outputs/yt_pr230_scalar_lsz_holonomic_exact_authority_attempt_2026-05-05.json",
        "pr230_scalar_lsz_carleman_tauberian_determinacy_attempt": "outputs/yt_pr230_scalar_lsz_carleman_tauberian_determinacy_attempt_2026-05-05.json",
        "fh_lsz_contact_subtraction_identifiability": "outputs/yt_fh_lsz_contact_subtraction_identifiability_2026-05-05.json",
        "fh_lsz_affine_contact_complete_monotonicity": "outputs/yt_fh_lsz_affine_contact_complete_monotonicity_no_go_2026-05-05.json",
        "fh_lsz_polynomial_contact_finite_shell": "outputs/yt_fh_lsz_polynomial_contact_finite_shell_no_go_2026-05-05.json",
        "fh_lsz_polynomial_contact_repair": "outputs/yt_fh_lsz_polynomial_contact_repair_no_go_2026-05-05.json",
        "fh_lsz_pole_saturation_threshold_gate": "outputs/yt_fh_lsz_pole_saturation_threshold_gate_2026-05-02.json",
        "fh_lsz_threshold_authority_audit": "outputs/yt_fh_lsz_threshold_authority_import_audit_2026-05-02.json",
        "confinement_gap_threshold_import": "outputs/yt_confinement_gap_threshold_import_audit_2026-05-02.json",
        "fh_lsz_finite_volume_pole_saturation": "outputs/yt_fh_lsz_finite_volume_pole_saturation_obstruction_2026-05-02.json",
        "fh_lsz_numba_seed_independence": "outputs/yt_fh_lsz_numba_seed_independence_audit_2026-05-02.json",
        "fh_lsz_uniform_gap_self_certification": "outputs/yt_fh_lsz_uniform_gap_self_certification_no_go_2026-05-02.json",
        "scalar_denominator_theorem_closure": "outputs/yt_scalar_denominator_theorem_closure_attempt_2026-05-02.json",
        "fh_lsz_soft_continuum_threshold": "outputs/yt_fh_lsz_soft_continuum_threshold_no_go_2026-05-02.json",
        "reflection_positivity_lsz_shortcut": "outputs/yt_reflection_positivity_lsz_shortcut_no_go_2026-05-02.json",
        "effective_potential_hessian_source_overlap": "outputs/yt_effective_potential_hessian_source_overlap_no_go_2026-05-02.json",
        "brst_nielsen_higgs_identity": "outputs/yt_brst_nielsen_higgs_identity_no_go_2026-05-02.json",
        "cl3_automorphism_source_identity": "outputs/yt_cl3_automorphism_source_identity_no_go_2026-05-02.json",
        "same_source_pole_data_sufficiency": "outputs/yt_same_source_pole_data_sufficiency_gate_2026-05-02.json",
        "source_functional_lsz_identifiability": "outputs/yt_source_functional_lsz_identifiability_theorem_2026-05-03.json",
        "isolated_pole_gram_factorization": "outputs/yt_isolated_pole_gram_factorization_theorem_2026-05-03.json",
        "osp_oh_assumption_route_audit": "outputs/yt_osp_oh_assumption_route_audit_2026-05-04.json",
        "osp_oh_literature_bridge": "outputs/yt_osp_oh_literature_bridge_2026-05-04.json",
        "fms_oh_certificate_construction_attempt": "outputs/yt_fms_oh_certificate_construction_attempt_2026-05-04.json",
        "pr230_action_first_oh_artifact_attempt": "outputs/yt_pr230_action_first_oh_artifact_attempt_2026-05-05.json",
        "pr230_holonomic_source_response_feasibility_gate": "outputs/yt_pr230_holonomic_source_response_feasibility_gate_2026-05-05.json",
        "pr230_oh_source_higgs_authority_rescan_gate": "outputs/yt_pr230_oh_source_higgs_authority_rescan_gate_2026-05-05.json",
        "pr230_minimal_axioms_yukawa_summary_firewall": "outputs/yt_pr230_minimal_axioms_yukawa_summary_firewall_2026-05-05.json",
        "pr230_genuine_source_pole_artifact_intake": "outputs/yt_pr230_genuine_source_pole_artifact_intake_2026-05-06.json",
        "pr230_l12_chunk_compute_status": "outputs/yt_pr230_l12_chunk_compute_status_2026-05-06.json",
        "pr230_negative_route_applicability_review": "outputs/yt_pr230_negative_route_applicability_review_2026-05-06.json",
        "pr230_taste_condensate_oh_bridge_audit": "outputs/yt_pr230_taste_condensate_oh_bridge_audit_2026-05-06.json",
        "pr230_source_coordinate_transport_gate": "outputs/yt_pr230_source_coordinate_transport_gate_2026-05-06.json",
        "pr230_origin_main_composite_higgs_intake_guard": "outputs/yt_pr230_origin_main_composite_higgs_intake_guard_2026-05-06.json",
        "pr230_origin_main_ew_m_residual_intake_guard": "outputs/yt_pr230_origin_main_ew_m_residual_intake_guard_2026-05-06.json",
        "pr230_same_surface_z3_taste_triplet": "outputs/yt_pr230_same_surface_z3_taste_triplet_artifact_2026-05-06.json",
        "pr230_z3_triplet_conditional_primitive_cone": "outputs/yt_pr230_z3_triplet_conditional_primitive_cone_theorem_2026-05-06.json",
        "pr230_z3_triplet_positive_cone_support": "outputs/yt_pr230_z3_triplet_positive_cone_support_certificate_2026-05-06.json",
        "pr230_z3_generation_action_lift_attempt": "outputs/yt_pr230_z3_generation_action_lift_attempt_2026-05-06.json",
        "pr230_z3_lazy_transfer_promotion_attempt": "outputs/yt_pr230_z3_lazy_transfer_promotion_attempt_2026-05-06.json",
        "pr230_z3_lazy_selector_no_go": "outputs/yt_pr230_z3_lazy_selector_no_go_2026-05-06.json",
        "pr230_source_coordinate_transport_completion": "outputs/yt_pr230_source_coordinate_transport_completion_attempt_2026-05-06.json",
        "pr230_two_source_taste_radial_chart": "outputs/yt_pr230_two_source_taste_radial_chart_certificate_2026-05-06.json",
        "pr230_two_source_taste_radial_action": "outputs/yt_pr230_two_source_taste_radial_action_certificate_2026-05-06.json",
        "pr230_two_source_taste_radial_row_contract": "outputs/yt_pr230_two_source_taste_radial_row_contract_2026-05-06.json",
        "pr230_two_source_taste_radial_row_production_manifest": "outputs/yt_pr230_two_source_taste_radial_row_production_manifest_2026-05-06.json",
        "pr230_two_source_taste_radial_row_combiner_gate": "outputs/yt_pr230_two_source_taste_radial_row_combiner_gate_2026-05-06.json",
        "pr230_two_source_taste_radial_schur_subblock_witness": "outputs/yt_pr230_two_source_taste_radial_schur_subblock_witness_2026-05-06.json",
        "pr230_two_source_taste_radial_schur_kprime_finite_shell_scout": "outputs/yt_pr230_two_source_taste_radial_schur_kprime_finite_shell_scout_2026-05-06.json",
        "pr230_two_source_taste_radial_schur_abc_finite_rows": "outputs/yt_pr230_two_source_taste_radial_schur_abc_finite_rows_2026-05-06.json",
        "pr230_two_source_taste_radial_schur_pole_lift_gate": "outputs/yt_pr230_two_source_taste_radial_schur_pole_lift_gate_2026-05-06.json",
        "pr230_two_source_taste_radial_primitive_transfer_candidate_gate": "outputs/yt_pr230_two_source_taste_radial_primitive_transfer_candidate_gate_2026-05-07.json",
        "pr230_orthogonal_top_coupling_exclusion_candidate_gate": "outputs/yt_pr230_orthogonal_top_coupling_exclusion_candidate_gate_2026-05-07.json",
        "pr230_strict_scalar_lsz_moment_fv_authority_gate": "outputs/yt_pr230_strict_scalar_lsz_moment_fv_authority_gate_2026-05-07.json",
        "pr230_schur_complement_stieltjes_repair_gate": "outputs/yt_pr230_schur_complement_stieltjes_repair_gate_2026-05-07.json",
        "pr230_schur_complement_complete_monotonicity_gate": "outputs/yt_pr230_schur_complement_complete_monotonicity_gate_2026-05-07.json",
        "pr230_schur_x_given_source_one_pole_scout": "outputs/yt_pr230_schur_x_given_source_one_pole_scout_2026-05-07.json",
        "pr230_two_source_taste_radial_chunk_package": "outputs/yt_pr230_two_source_taste_radial_chunk_package_audit_2026-05-06.json",
        "pr230_source_higgs_pole_row_acceptance_contract": "outputs/yt_pr230_source_higgs_pole_row_acceptance_contract_2026-05-06.json",
        "pr230_two_source_taste_radial_chunk001_checkpoint": "outputs/yt_pr230_two_source_taste_radial_chunk001_checkpoint_2026-05-06.json",
        "pr230_two_source_taste_radial_chunk002_checkpoint": "outputs/yt_pr230_two_source_taste_radial_chunk002_checkpoint_2026-05-06.json",
        "pr230_two_source_taste_radial_chunk003_checkpoint": "outputs/yt_pr230_two_source_taste_radial_chunk003_checkpoint_2026-05-06.json",
        "pr230_two_source_taste_radial_chunk004_checkpoint": "outputs/yt_pr230_two_source_taste_radial_chunk004_checkpoint_2026-05-06.json",
        "pr230_two_source_taste_radial_chunk005_checkpoint": "outputs/yt_pr230_two_source_taste_radial_chunk005_checkpoint_2026-05-06.json",
        "pr230_two_source_taste_radial_chunk006_checkpoint": "outputs/yt_pr230_two_source_taste_radial_chunk006_checkpoint_2026-05-06.json",
        "pr230_two_source_taste_radial_chunk007_checkpoint": "outputs/yt_pr230_two_source_taste_radial_chunk007_checkpoint_2026-05-06.json",
        "pr230_two_source_taste_radial_chunk008_checkpoint": "outputs/yt_pr230_two_source_taste_radial_chunk008_checkpoint_2026-05-06.json",
        "pr230_two_source_taste_radial_chunk009_checkpoint": "outputs/yt_pr230_two_source_taste_radial_chunk009_checkpoint_2026-05-06.json",
        "pr230_two_source_taste_radial_chunk010_checkpoint": "outputs/yt_pr230_two_source_taste_radial_chunk010_checkpoint_2026-05-06.json",
        "pr230_taste_radial_canonical_oh_selector_gate": "outputs/yt_pr230_taste_radial_canonical_oh_selector_gate_2026-05-06.json",
        "pr230_degree_one_higgs_action_premise_gate": "outputs/yt_pr230_degree_one_higgs_action_premise_gate_2026-05-06.json",
        "pr230_degree_one_radial_tangent_oh_theorem": "outputs/yt_pr230_degree_one_radial_tangent_oh_theorem_2026-05-07.json",
        "pr230_taste_radial_to_source_higgs_promotion_contract": "outputs/yt_pr230_taste_radial_to_source_higgs_promotion_contract_2026-05-07.json",
        "pr230_fms_post_degree_route_rescore": "outputs/yt_pr230_fms_post_degree_route_rescore_2026-05-06.json",
        "pr230_fms_composite_oh_conditional_theorem": "outputs/yt_pr230_fms_composite_oh_conditional_theorem_2026-05-06.json",
        "pr230_fms_oh_candidate_action_packet": "outputs/yt_pr230_fms_oh_candidate_action_packet_2026-05-07.json",
        "pr230_fms_source_overlap_readout_gate": "outputs/yt_pr230_fms_source_overlap_readout_gate_2026-05-07.json",
        "pr230_fms_action_adoption_minimal_cut": "outputs/yt_pr230_fms_action_adoption_minimal_cut_2026-05-07.json",
        "pr230_higgs_mass_source_action_bridge": "outputs/yt_pr230_higgs_mass_source_action_bridge_2026-05-06.json",
        "pr230_post_fms_source_overlap_necessity_gate": "outputs/yt_pr230_post_fms_source_overlap_necessity_gate_2026-05-06.json",
        "pr230_source_higgs_overlap_kappa_contract": "outputs/yt_pr230_source_higgs_overlap_kappa_contract_2026-05-06.json",
        "pr230_radial_spurion_action_contract": "outputs/yt_pr230_radial_spurion_action_contract_2026-05-06.json",
        "pr230_additive_source_radial_spurion_incompatibility": "outputs/yt_pr230_additive_source_radial_spurion_incompatibility_2026-05-07.json",
        "pr230_additive_top_subtraction_row_contract": "outputs/yt_pr230_additive_top_subtraction_row_contract_2026-05-07.json",
        "pr230_wz_response_ratio_identifiability_contract": "outputs/yt_pr230_wz_response_ratio_identifiability_contract_2026-05-07.json",
        "pr230_wz_same_source_action_minimal_certificate_cut": "outputs/yt_pr230_wz_same_source_action_minimal_certificate_cut_2026-05-07.json",
        "pr230_wz_accepted_action_response_root_checkpoint": "outputs/yt_pr230_wz_accepted_action_response_root_checkpoint_2026-05-07.json",
        "pr230_canonical_oh_wz_common_action_cut": "outputs/yt_pr230_canonical_oh_wz_common_action_cut_2026-05-07.json",
        "pr230_canonical_oh_accepted_action_stretch_attempt": "outputs/yt_pr230_canonical_oh_accepted_action_stretch_attempt_2026-05-07.json",
        "pr230_kinetic_taste_mixing_bridge": "outputs/yt_pr230_kinetic_taste_mixing_bridge_attempt_2026-05-06.json",
        "pr230_one_higgs_taste_axis_completeness": "outputs/yt_pr230_one_higgs_taste_axis_completeness_attempt_2026-05-06.json",
        "pr230_action_first_route_completion": "outputs/yt_pr230_action_first_route_completion_2026-05-06.json",
        "pr230_wz_response_route_completion": "outputs/yt_pr230_wz_response_route_completion_2026-05-06.json",
        "pr230_schur_route_completion": "outputs/yt_pr230_schur_route_completion_2026-05-06.json",
        "pr230_neutral_primitive_route_completion": "outputs/yt_pr230_neutral_primitive_route_completion_2026-05-06.json",
        "pr230_oh_bridge_candidate_portfolio": "outputs/yt_pr230_oh_bridge_first_principles_candidate_portfolio_2026-05-06.json",
        "pr230_same_surface_neutral_multiplicity_one_gate": "outputs/yt_pr230_same_surface_neutral_multiplicity_one_gate_2026-05-07.json",
        "pr230_os_transfer_kernel_artifact_gate": "outputs/yt_pr230_os_transfer_kernel_artifact_gate_2026-05-07.json",
        "pr230_source_higgs_time_kernel_harness_extension_gate": "outputs/yt_pr230_source_higgs_time_kernel_harness_extension_gate_2026-05-07.json",
        "pr230_source_higgs_time_kernel_gevp_contract": "outputs/yt_pr230_source_higgs_time_kernel_gevp_contract_2026-05-07.json",
        "pr230_source_higgs_time_kernel_production_manifest": "outputs/yt_pr230_source_higgs_time_kernel_production_manifest_2026-05-07.json",
        "pr230_fms_literature_source_overlap_intake": "outputs/yt_pr230_fms_literature_source_overlap_intake_2026-05-07.json",
        "pr230_schur_higher_shell_production_contract": "outputs/yt_pr230_schur_higher_shell_production_contract_2026-05-07.json",
        "pr230_derived_bridge_rank_one_closure_attempt": "outputs/yt_pr230_derived_bridge_rank_one_closure_attempt_2026-05-05.json",
        "pr230_source_sector_pattern_transfer_gate": "outputs/yt_pr230_source_sector_pattern_transfer_gate_2026-05-05.json",
        "pr230_det_positivity_bridge_intake_gate": "outputs/yt_pr230_det_positivity_bridge_intake_gate_2026-05-05.json",
        "pr230_reflection_det_primitive_upgrade_gate": "outputs/yt_pr230_reflection_det_primitive_upgrade_gate_2026-05-05.json",
        "complete_source_spectrum_identity_no_go": "outputs/yt_complete_source_spectrum_identity_no_go_2026-05-02.json",
        "neutral_scalar_top_coupling_tomography_gate": "outputs/yt_neutral_scalar_top_coupling_tomography_gate_2026-05-02.json",
        "non_source_response_rank_repair_sufficiency": "outputs/yt_non_source_response_rank_repair_sufficiency_2026-05-03.json",
        "positivity_improving_neutral_scalar_rank_one": "outputs/yt_positivity_improving_neutral_scalar_rank_one_support_2026-05-03.json",
        "gauge_perron_neutral_scalar_rank_one_import": "outputs/yt_gauge_perron_to_neutral_scalar_rank_one_import_audit_2026-05-03.json",
        "neutral_scalar_positivity_improving_direct_closure": "outputs/yt_neutral_scalar_positivity_improving_direct_closure_attempt_2026-05-03.json",
        "neutral_scalar_irreducibility_authority_audit": "outputs/yt_neutral_scalar_irreducibility_authority_audit_2026-05-04.json",
        "neutral_scalar_primitive_cone_certificate_gate": "outputs/yt_neutral_scalar_primitive_cone_certificate_gate_2026-05-05.json",
        "neutral_scalar_primitive_cone_stretch_no_go": "outputs/yt_neutral_scalar_primitive_cone_stretch_no_go_2026-05-05.json",
        "neutral_scalar_burnside_irreducibility_attempt": "outputs/yt_neutral_scalar_burnside_irreducibility_attempt_2026-05-05.json",
        "neutral_offdiagonal_generator_derivation_attempt": "outputs/yt_neutral_offdiagonal_generator_derivation_attempt_2026-05-05.json",
        "pr230_logdet_hessian_neutral_mixing_attempt": "outputs/yt_pr230_logdet_hessian_neutral_mixing_attempt_2026-05-05.json",
        "scalar_carrier_projector_closure": "outputs/yt_scalar_carrier_projector_closure_attempt_2026-05-02.json",
        "kprime_closure": "outputs/yt_kprime_closure_attempt_2026-05-02.json",
        "pr230_matching_running_bridge_gate": "outputs/yt_pr230_matching_running_bridge_gate_2026-05-04.json",
        "schur_complement_kprime_sufficiency": "outputs/yt_schur_complement_kprime_sufficiency_2026-05-03.json",
        "schur_kprime_row_absence_guard": "outputs/yt_schur_kprime_row_absence_guard_2026-05-03.json",
        "legacy_schur_bridge_import_audit": "outputs/yt_legacy_schur_bridge_import_audit_2026-05-03.json",
        "schur_kernel_row_contract_gate": "outputs/yt_schur_kernel_row_contract_gate_2026-05-03.json",
        "schur_row_candidate_extraction_attempt": "outputs/yt_schur_row_candidate_extraction_attempt_2026-05-03.json",
        "schur_compressed_denominator_row_bootstrap_no_go": "outputs/yt_schur_compressed_denominator_row_bootstrap_no_go_2026-05-05.json",
        "pr230_schur_abc_definition_derivation_attempt": "outputs/yt_pr230_schur_abc_definition_derivation_attempt_2026-05-05.json",
        "pr230_nonchunk_current_surface_exhaustion": "outputs/yt_pr230_nonchunk_current_surface_exhaustion_gate_2026-05-05.json",
        "pr230_nonchunk_future_artifact_intake": "outputs/yt_pr230_nonchunk_future_artifact_intake_gate_2026-05-05.json",
        "pr230_nonchunk_terminal_route_exhaustion": "outputs/yt_pr230_nonchunk_terminal_route_exhaustion_gate_2026-05-05.json",
        "pr230_nonchunk_reopen_admissibility": "outputs/yt_pr230_nonchunk_reopen_admissibility_gate_2026-05-05.json",
        "pr230_nonchunk_cycle14_route_selector": "outputs/yt_pr230_nonchunk_cycle14_route_selector_gate_2026-05-05.json",
        "pr230_nonchunk_cycle15_independent_route_admission": "outputs/yt_pr230_nonchunk_cycle15_independent_route_admission_gate_2026-05-05.json",
        "pr230_nonchunk_cycle16_reopen_source_guard": "outputs/yt_pr230_nonchunk_cycle16_reopen_source_guard_2026-05-05.json",
        "pr230_nonchunk_cycle17_stop_condition_gate": "outputs/yt_pr230_nonchunk_cycle17_stop_condition_gate_2026-05-05.json",
        "pr230_nonchunk_cycle18_reopen_freshness_gate": "outputs/yt_pr230_nonchunk_cycle18_reopen_freshness_gate_2026-05-05.json",
        "pr230_nonchunk_cycle19_no_duplicate_route_gate": "outputs/yt_pr230_nonchunk_cycle19_no_duplicate_route_gate_2026-05-05.json",
        "pr230_nonchunk_cycle20_process_gate_continuation_no_go": "outputs/yt_pr230_nonchunk_cycle20_process_gate_continuation_no_go_2026-05-05.json",
        "pr230_nonchunk_cycle21_remote_reopen_guard": "outputs/yt_pr230_nonchunk_cycle21_remote_reopen_guard_2026-05-05.json",
        "pr230_nonchunk_cycle22_main_audit_drift_guard": "outputs/yt_pr230_nonchunk_cycle22_main_audit_drift_guard_2026-05-05.json",
        "pr230_nonchunk_cycle23_main_effective_status_drift_guard": "outputs/yt_pr230_nonchunk_cycle23_main_effective_status_drift_guard_2026-05-05.json",
        "pr230_nonchunk_cycle24_post_cycle23_main_status_drift_guard": "outputs/yt_pr230_nonchunk_cycle24_post_cycle23_main_status_drift_guard_2026-05-05.json",
        "pr230_nonchunk_cycle25_post_cycle24_main_audit_status_drift_guard": "outputs/yt_pr230_nonchunk_cycle25_post_cycle24_main_audit_status_drift_guard_2026-05-05.json",
        "pr230_nonchunk_cycle26_post_cycle25_main_audit_status_drift_guard": "outputs/yt_pr230_nonchunk_cycle26_post_cycle25_main_audit_status_drift_guard_2026-05-05.json",
        "pr230_nonchunk_cycle27_post_cycle26_main_audit_status_drift_guard": "outputs/yt_pr230_nonchunk_cycle27_post_cycle26_main_audit_status_drift_guard_2026-05-05.json",
        "pr230_nonchunk_cycle28_post_cycle27_main_audit_status_drift_guard": "outputs/yt_pr230_nonchunk_cycle28_post_cycle27_main_audit_status_drift_guard_2026-05-05.json",
        "pr230_nonchunk_cycle29_post_cycle28_main_audit_status_drift_guard": "outputs/yt_pr230_nonchunk_cycle29_post_cycle28_main_audit_status_drift_guard_2026-05-05.json",
        "pr230_nonchunk_cycle30_post_cycle29_main_audit_status_drift_guard": "outputs/yt_pr230_nonchunk_cycle30_post_cycle29_main_audit_status_drift_guard_2026-05-05.json",
        "pr230_nonchunk_cycle31_post_cycle30_main_audit_status_drift_guard": "outputs/yt_pr230_nonchunk_cycle31_post_cycle30_main_audit_status_drift_guard_2026-05-05.json",
        "pr230_nonchunk_cycle32_post_cycle31_main_audit_status_drift_guard": "outputs/yt_pr230_nonchunk_cycle32_post_cycle31_main_audit_status_drift_guard_2026-05-05.json",
        "pr230_nonchunk_cycle33_post_cycle32_main_audit_status_drift_guard": "outputs/yt_pr230_nonchunk_cycle33_post_cycle32_main_audit_status_drift_guard_2026-05-05.json",
        "pr230_nonchunk_cycle34_post_cycle33_main_nonpr230_drift_guard": "outputs/yt_pr230_nonchunk_cycle34_post_cycle33_main_nonpr230_drift_guard_2026-05-05.json",
        "pr230_nonchunk_cycle35_post_cycle34_main_audit_ledger_drift_guard": "outputs/yt_pr230_nonchunk_cycle35_post_cycle34_main_audit_ledger_drift_guard_2026-05-05.json",
        "fh_lsz_higgs_pole_identity": "outputs/yt_fh_lsz_higgs_pole_identity_gate_2026-05-02.json",
        "fh_gauge_normalized_response": "outputs/yt_fh_gauge_normalized_response_route_2026-05-02.json",
        "fh_gauge_mass_response_observable_gap": "outputs/yt_fh_gauge_mass_response_observable_gap_2026-05-02.json",
        "fh_gauge_mass_response_manifest": "outputs/yt_fh_gauge_mass_response_manifest_2026-05-02.json",
        "fh_gauge_mass_response_certificate_builder": "outputs/yt_fh_gauge_mass_response_certificate_builder_2026-05-03.json",
        "same_source_wz_response_certificate_gate": "outputs/yt_same_source_wz_response_certificate_gate_2026-05-02.json",
        "wz_response_harness_absence_guard": "outputs/yt_wz_response_harness_absence_guard_2026-05-02.json",
        "wz_response_repo_harness_import_audit": "outputs/yt_wz_response_repo_harness_import_audit_2026-05-03.json",
        "wz_response_measurement_row_contract_gate": "outputs/yt_wz_response_measurement_row_contract_gate_2026-05-03.json",
        "wz_response_row_production_attempt": "outputs/yt_wz_response_row_production_attempt_2026-05-03.json",
        "wz_response_harness_implementation_plan": "outputs/yt_wz_response_harness_implementation_plan_2026-05-04.json",
        "wz_harness_smoke_schema": "outputs/yt_pr230_wz_harness_smoke_schema_gate_2026-05-05.json",
        "wz_smoke_to_production_promotion_no_go": (
            "outputs/yt_pr230_wz_smoke_to_production_promotion_no_go_2026-05-05.json"
        ),
        "wz_same_source_ew_action_certificate_builder": "outputs/yt_wz_same_source_ew_action_certificate_builder_2026-05-04.json",
        "wz_same_source_ew_action_gate": "outputs/yt_wz_same_source_ew_action_gate_2026-05-04.json",
        "wz_same_source_ew_action_semantic_firewall": "outputs/yt_wz_same_source_ew_action_semantic_firewall_2026-05-04.json",
        "wz_source_coordinate_transport_no_go": "outputs/yt_wz_source_coordinate_transport_no_go_2026-05-05.json",
        "wz_goldstone_equivalence_source_identity_no_go": "outputs/yt_wz_goldstone_equivalence_source_identity_no_go_2026-05-05.json",
        "same_source_w_response_decomposition": "outputs/yt_same_source_w_response_decomposition_theorem_2026-05-04.json",
        "same_source_w_response_orthogonal_correction": "outputs/yt_same_source_w_response_orthogonal_correction_gate_2026-05-04.json",
        "one_higgs_completeness_orthogonal_null": "outputs/yt_one_higgs_completeness_orthogonal_null_gate_2026-05-04.json",
        "delta_perp_tomography_correction_builder": "outputs/yt_delta_perp_tomography_correction_builder_2026-05-04.json",
        "same_source_top_response_identity_builder": "outputs/yt_same_source_top_response_identity_certificate_builder_2026-05-04.json",
        "top_wz_matched_covariance_builder": "outputs/yt_top_wz_matched_covariance_certificate_builder_2026-05-04.json",
        "top_wz_covariance_marginal_derivation_no_go": "outputs/yt_top_wz_covariance_marginal_derivation_no_go_2026-05-05.json",
        "top_wz_factorization_independence_gate": "outputs/yt_top_wz_factorization_independence_gate_2026-05-05.json",
        "top_wz_deterministic_response_covariance_gate": "outputs/yt_top_wz_deterministic_response_covariance_gate_2026-05-05.json",
        "top_wz_covariance_theorem_import_audit": "outputs/yt_top_wz_covariance_theorem_import_audit_2026-05-05.json",
        "same_source_top_response_builder": "outputs/yt_same_source_top_response_certificate_builder_2026-05-04.json",
        "same_source_w_response_row_builder": "outputs/yt_same_source_w_response_row_builder_2026-05-04.json",
        "same_source_w_response_lightweight_readout": "outputs/yt_same_source_w_response_lightweight_readout_harness_2026-05-04.json",
        "wz_mass_fit_response_row_builder": "outputs/yt_wz_mass_fit_response_row_builder_2026-05-04.json",
        "electroweak_g2_certificate_builder": "outputs/yt_electroweak_g2_certificate_builder_2026-05-05.json",
        "wz_g2_generator_casimir_normalization_no_go": "outputs/yt_wz_g2_generator_casimir_normalization_no_go_2026-05-05.json",
        "wz_g2_authority_firewall": "outputs/yt_wz_g2_authority_firewall_2026-05-05.json",
        "wz_g2_response_self_normalization_no_go": "outputs/yt_wz_g2_response_self_normalization_no_go_2026-05-05.json",
        "pr230_wz_g2_bare_running_bridge_attempt": "outputs/yt_pr230_wz_g2_bare_running_bridge_attempt_2026-05-05.json",
        "wz_correlator_mass_fit_path_gate": "outputs/yt_wz_correlator_mass_fit_path_gate_2026-05-04.json",
        "same_source_sector_overlap_identity": "outputs/yt_same_source_sector_overlap_identity_obstruction_2026-05-02.json",
        "source_pole_canonical_higgs_mixing": "outputs/yt_source_pole_canonical_higgs_mixing_obstruction_2026-05-02.json",
        "osp_oh_identity_stretch": "outputs/yt_osp_oh_identity_stretch_attempt_2026-05-03.json",
        "source_pole_purity_cross_correlator": "outputs/yt_source_pole_purity_cross_correlator_gate_2026-05-02.json",
        "source_higgs_cross_correlator_manifest": "outputs/yt_source_higgs_cross_correlator_manifest_2026-05-02.json",
        "source_higgs_cross_correlator_import": "outputs/yt_source_higgs_cross_correlator_import_audit_2026-05-02.json",
        "source_higgs_gram_purity_gate": "outputs/yt_source_higgs_gram_purity_gate_2026-05-02.json",
        "source_higgs_cross_correlator_harness_extension": "outputs/yt_source_higgs_cross_correlator_harness_extension_2026-05-03.json",
        "source_higgs_pole_residue_extractor": "outputs/yt_source_higgs_pole_residue_extractor_2026-05-03.json",
        "source_higgs_cross_correlator_certificate_builder": "outputs/yt_source_higgs_cross_correlator_certificate_builder_2026-05-03.json",
        "source_higgs_gram_purity_postprocessor": "outputs/yt_source_higgs_gram_purity_postprocess_2026-05-03.json",
        "source_higgs_gram_purity_contract_witness": "outputs/yt_source_higgs_gram_purity_contract_witness_2026-05-03.json",
        "source_higgs_production_readiness_gate": "outputs/yt_source_higgs_production_readiness_gate_2026-05-04.json",
        "canonical_higgs_operator_candidate_stress": "outputs/yt_canonical_higgs_operator_candidate_stress_2026-05-03.json",
        "canonical_higgs_operator_certificate_gate": "outputs/yt_canonical_higgs_operator_certificate_gate_2026-05-03.json",
        "canonical_higgs_operator_semantic_firewall": "outputs/yt_canonical_higgs_operator_semantic_firewall_2026-05-04.json",
        "canonical_higgs_operator_realization_gate": "outputs/yt_canonical_higgs_operator_realization_gate_2026-05-02.json",
        "canonical_higgs_repo_authority_audit": "outputs/yt_canonical_higgs_repo_authority_audit_2026-05-03.json",
        "cross_lane_oh_authority_audit": "outputs/yt_cross_lane_oh_authority_audit_2026-05-05.json",
        "canonical_oh_premise_stretch": "outputs/yt_canonical_oh_premise_stretch_no_go_2026-05-05.json",
        "sm_one_higgs_oh_import_boundary": "outputs/yt_sm_one_higgs_oh_import_boundary_2026-05-03.json",
        "hunit_canonical_higgs_operator_candidate_gate": "outputs/yt_hunit_canonical_higgs_operator_candidate_gate_2026-05-02.json",
        "source_higgs_harness_absence_guard": "outputs/yt_source_higgs_harness_absence_guard_2026-05-02.json",
        "source_higgs_unratified_operator_smoke": "outputs/yt_source_higgs_unratified_operator_smoke_checkpoint_2026-05-03.json",
        "source_higgs_unratified_gram_shortcut_no_go": "outputs/yt_source_higgs_unratified_gram_shortcut_no_go_2026-05-05.json",
        "neutral_scalar_rank_one_purity_gate": "outputs/yt_neutral_scalar_rank_one_purity_gate_2026-05-02.json",
        "neutral_scalar_commutant_rank_no_go": "outputs/yt_neutral_scalar_commutant_rank_no_go_2026-05-02.json",
        "neutral_scalar_dynamical_rank_one_closure": "outputs/yt_neutral_scalar_dynamical_rank_one_closure_attempt_2026-05-02.json",
        "orthogonal_neutral_decoupling_no_go": "outputs/yt_orthogonal_neutral_decoupling_no_go_2026-05-02.json",
        "fh_gauge_response_mixed_scalar": "outputs/yt_fh_gauge_response_mixed_scalar_obstruction_2026-05-02.json",
        "no_orthogonal_top_coupling_import": "outputs/yt_no_orthogonal_top_coupling_import_audit_2026-05-02.json",
        "no_orthogonal_top_coupling_selection_rule": "outputs/yt_no_orthogonal_top_coupling_selection_rule_no_go_2026-05-02.json",
        "d17_source_pole_identity_closure": "outputs/yt_d17_source_pole_identity_closure_attempt_2026-05-02.json",
        "source_overlap_sum_rule_no_go": "outputs/yt_source_overlap_sum_rule_no_go_2026-05-02.json",
        "short_distance_ope_lsz_no_go": "outputs/yt_short_distance_ope_lsz_no_go_2026-05-02.json",
        "effective_mass_plateau_residue_no_go": "outputs/yt_effective_mass_plateau_residue_no_go_2026-05-02.json",
        "finite_source_shift_derivative_no_go": "outputs/yt_finite_source_shift_derivative_no_go_2026-05-02.json",
        "fh_lsz_finite_source_linearity_gate": "outputs/yt_fh_lsz_finite_source_linearity_gate_2026-05-02.json",
        "fh_lsz_finite_source_linearity_calibration": "outputs/yt_fh_lsz_finite_source_linearity_calibration_checkpoint_2026-05-03.json",
        "fh_lsz_target_observable_ess": "outputs/yt_fh_lsz_target_observable_ess_certificate_2026-05-03.json",
        "fh_lsz_autocorrelation_ess_gate": "outputs/yt_fh_lsz_autocorrelation_ess_gate_2026-05-02.json",
        "fh_lsz_response_window_forensics": "outputs/yt_fh_lsz_response_window_forensics_2026-05-03.json",
        "fh_lsz_common_window_response_provenance": "outputs/yt_fh_lsz_common_window_response_provenance_2026-05-04.json",
        "fh_lsz_common_window_pooled_response_estimator": "outputs/yt_fh_lsz_common_window_pooled_response_estimator_2026-05-04.json",
        "fh_lsz_common_window_replacement_response_stability": "outputs/yt_fh_lsz_common_window_replacement_response_stability_2026-05-04.json",
        "fh_lsz_common_window_response_gate": "outputs/yt_fh_lsz_common_window_response_gate_2026-05-04.json",
        "fh_lsz_v2_target_response_stability": "outputs/yt_fh_lsz_v2_target_response_stability_2026-05-04.json",
        "fh_lsz_response_window_acceptance_gate": "outputs/yt_fh_lsz_response_window_acceptance_gate_2026-05-03.json",
        "fh_lsz_legacy_v2_backfill_feasibility": "outputs/yt_fh_lsz_legacy_v2_backfill_feasibility_2026-05-04.json",
        "fh_lsz_target_timeseries_replacement_queue": "outputs/yt_fh_lsz_target_timeseries_replacement_queue_2026-05-02.json",
        "fh_lsz_target_timeseries_full_set_checkpoint": "outputs/yt_fh_lsz_target_timeseries_full_set_checkpoint_2026-05-12.json",
        "fh_lsz_target_timeseries_harness": "outputs/yt_fh_lsz_target_timeseries_harness_certificate_2026-05-02.json",
        "fh_lsz_multitau_target_timeseries_harness": "outputs/yt_fh_lsz_multitau_target_timeseries_harness_certificate_2026-05-03.json",
        "fh_lsz_selected_mass_normal_cache_speedup": "outputs/yt_fh_lsz_selected_mass_normal_cache_speedup_certificate_2026-05-03.json",
        "top_mass_scan_response_harness_gate": "outputs/yt_pr230_top_mass_scan_response_harness_gate_2026-05-12.json",
        "fh_lsz_global_production_collision_guard": "outputs/yt_fh_lsz_global_production_collision_guard_2026-05-04.json",
        "fh_lsz_target_timeseries_higgs_identity_no_go": "outputs/yt_fh_lsz_target_timeseries_higgs_identity_no_go_2026-05-02.json",
        "higgs_pole_identity_latest_blocker": "outputs/yt_higgs_pole_identity_latest_blocker_certificate_2026-05-02.json",
        "fh_lsz_pole_fit_mode_budget": "outputs/yt_fh_lsz_pole_fit_mode_budget_2026-05-01.json",
        "fh_lsz_eight_mode_noise_variance": "outputs/yt_fh_lsz_eight_mode_noise_variance_gate_2026-05-01.json",
        "fh_lsz_noise_subsample_diagnostics": "outputs/yt_fh_lsz_noise_subsample_diagnostics_certificate_2026-05-01.json",
        "fh_lsz_variance_calibration_manifest": "outputs/yt_fh_lsz_variance_calibration_manifest_2026-05-01.json",
        "fh_lsz_paired_variance_calibration_gate": "outputs/yt_fh_lsz_paired_variance_calibration_gate_2026-05-04.json",
        "fh_lsz_polefit8x8_chunk_manifest": "outputs/yt_fh_lsz_polefit8x8_chunk_manifest_2026-05-04.json",
        "fh_lsz_polefit8x8_chunk_combiner_gate": "outputs/yt_fh_lsz_polefit8x8_chunk_combiner_gate_2026-05-04.json",
        "fh_lsz_polefit8x8_postprocessor": "outputs/yt_fh_lsz_polefit8x8_postprocessor_2026-05-04.json",
        "joint_resource_projection": "outputs/yt_fh_lsz_joint_resource_projection_2026-05-01.json",
        "full_positive_closure_assembly_gate": "outputs/yt_pr230_full_positive_closure_assembly_gate_2026-05-04.json",
        "negative_route_applicability_review": "outputs/yt_pr230_negative_route_applicability_review_2026-05-06.json",
    }
    for path in sorted((ROOT / "outputs").glob(GENERIC_CHUNK_TARGET_PATTERN)):
        required_certificates[generic_chunk_target_key(path)] = str(path.relative_to(ROOT))
    for path in sorted((ROOT / "outputs").glob(MULTITAU_CHUNK_TARGET_PATTERN)):
        required_certificates[multitau_chunk_target_key(path)] = str(path.relative_to(ROOT))
    certificates = {name: load_json(path) for name, path in required_certificates.items()}

    direct_certificates = [
        "outputs/yt_direct_lattice_correlator_certificate_2026-04-30.json",
        "outputs/yt_direct_lattice_correlator_pilot_certificate_2026-04-30.json",
        "outputs/yt_direct_lattice_correlator_pilot_plus_certificate_2026-05-01.json",
        "outputs/yt_direct_lattice_correlator_mass_bracket_certificate_2026-05-01.json",
    ]
    direct_meta = []
    for path in direct_certificates:
        data = load_json(path)
        metadata = data.get("metadata", {})
        direct_meta.append(
            {
                "path": path,
                "exists": bool(data),
                "phase": metadata.get("phase") or data.get("phase"),
                "strict_pass": data.get("strict_pass") or data.get("strict_validation", {}).get("pass"),
            }
        )

    missing = [name for name, data in certificates.items() if not data]
    no_hidden_proof = certificates["global_proof_audit"].get("retained_y_t_rows") == {}
    direct_strict_pass = any(item.get("phase") == "production" and item.get("strict_pass") is True for item in direct_meta)
    ward_open = certificates["ward_repair_audit"].get("closure_allowed") is False
    scalar_residue_blocked = (
        certificates["scalar_pole_residue_no_go"].get("actual_current_surface_status")
        == "exact negative boundary / retained closure unavailable on current analytic surface"
    )
    key_blocker_open = (
        certificates["key_blocker_closure_attempt"].get("actual_current_surface_status")
        == "open / key blocker not closed"
    )
    key_blocker_has_no_retained_authority = (
        certificates["key_blocker_closure_attempt"].get("retained_authorities") == []
    )
    lsz_norm_conditional = (
        certificates["lsz_normalization_cancellation"].get("actual_current_surface_status")
        == "conditional-support / scalar LSZ normalization cancellation"
        and certificates["lsz_normalization_cancellation"].get("proposal_allowed") is False
    )
    feshbach_boundary_not_common_dressing = (
        certificates["feshbach_response_boundary"].get("actual_current_surface_status")
        == "exact support / Feshbach response boundary"
        and certificates["feshbach_response_boundary"].get("proposal_allowed") is False
    )
    invariant_readout_not_closure = (
        "invariant readout" in certificates["fh_lsz_invariant_readout"].get("actual_current_surface_status", "")
        and certificates["fh_lsz_invariant_readout"].get("proposal_allowed") is False
    )
    derivative_limit_blocks_ladder = (
        "limiting-order obstruction" in certificates["scalar_ladder_derivative_limit"].get("actual_current_surface_status", "")
        and certificates["scalar_ladder_derivative_limit"].get("proposal_allowed") is False
    )
    residue_envelope_blocks_ladder = (
        "residue-envelope obstruction" in certificates["scalar_ladder_residue_envelope"].get("actual_current_surface_status", "")
        and certificates["scalar_ladder_residue_envelope"].get("proposal_allowed") is False
    )
    ward_identity_does_not_fix_kernel = (
        "Ward-identity obstruction" in certificates["scalar_kernel_ward_identity"].get("actual_current_surface_status", "")
        and certificates["scalar_kernel_ward_identity"].get("proposal_allowed") is False
    )
    zero_mode_limit_order_blocks_denominator = (
        "zero-mode limit-order theorem" in certificates["scalar_zero_mode_limit_order"].get("actual_current_surface_status", "")
        and certificates["scalar_zero_mode_limit_order"].get("proposal_allowed") is False
    )
    zero_mode_import_audit_blocks_hidden_authority = (
        "zero-mode prescription import audit" in certificates["zero_mode_prescription_import"].get("actual_current_surface_status", "")
        and certificates["zero_mode_prescription_import"].get("proposal_allowed") is False
    )
    flat_toron_blocks_trivial_selection = (
        "flat toron scalar-denominator obstruction" in certificates["flat_toron_denominator"].get("actual_current_surface_status", "")
        and certificates["flat_toron_denominator"].get("proposal_allowed") is False
    )
    flat_toron_washout_not_closure = (
        "flat toron thermodynamic washout" in certificates["flat_toron_washout"].get("actual_current_surface_status", "")
        and certificates["flat_toron_washout"].get("proposal_allowed") is False
    )
    color_singlet_zero_mode_not_closure = (
        "color-singlet gauge-zero-mode cancellation" in certificates["color_singlet_zero_mode"].get("actual_current_surface_status", "")
        and certificates["color_singlet_zero_mode"].get("proposal_allowed") is False
    )
    color_singlet_finite_q_ir_not_closure = (
        "color-singlet finite-q IR regularity" in certificates["color_singlet_finite_q_ir"].get("actual_current_surface_status", "")
        and certificates["color_singlet_finite_q_ir"].get("proposal_allowed") is False
    )
    color_singlet_ladder_pole_search_not_closure = (
        "zero-mode-removed ladder pole search"
        in certificates["color_singlet_zero_mode_removed_ladder_pole_search"].get("actual_current_surface_status", "")
        and certificates["color_singlet_zero_mode_removed_ladder_pole_search"].get("proposal_allowed") is False
    )
    taste_corner_ladder_pole_obstruction_not_closure = (
        "taste-corner pole-witness obstruction"
        in certificates["taste_corner_ladder_pole_obstruction"].get("actual_current_surface_status", "")
        and certificates["taste_corner_ladder_pole_obstruction"].get("proposal_allowed") is False
    )
    taste_carrier_import_audit_blocks_hidden_authority = (
        "taste-corner scalar-carrier import audit"
        in certificates["taste_carrier_import_audit"].get("actual_current_surface_status", "")
        and certificates["taste_carrier_import_audit"].get("proposal_allowed") is False
    )
    taste_singlet_normalization_removes_crossings = (
        "taste-singlet normalization removes finite ladder crossings"
        in certificates["taste_singlet_ladder_normalization"].get("actual_current_surface_status", "")
        and certificates["taste_singlet_ladder_normalization"].get("proposal_allowed") is False
        and certificates["taste_singlet_ladder_normalization"].get("summary", {}).get("raw_over_normalized") == 16
        and float(
            certificates["taste_singlet_ladder_normalization"].get("summary", {}).get(
                "normalized_lambda_max", 1.0
            )
        )
        < 1.0
    )
    scalar_taste_projector_attempt_blocked = (
        "scalar taste-projector normalization theorem attempt blocked"
        in certificates["scalar_taste_projector_normalization_attempt"].get(
            "actual_current_surface_status", ""
        )
        and certificates["scalar_taste_projector_normalization_attempt"].get("proposal_allowed") is False
        and certificates["scalar_taste_projector_normalization_attempt"].get("taste_space", {}).get(
            "corner_count"
        )
        == 16
    )
    unit_projector_pole_threshold_blocks_finite_ladder = (
        "unit-projector finite-ladder pole-threshold obstruction"
        in certificates["unit_projector_pole_threshold"].get("actual_current_surface_status", "")
        and certificates["unit_projector_pole_threshold"].get("proposal_allowed") is False
        and float(
            certificates["unit_projector_pole_threshold"].get("summary", {}).get(
                "required_kernel_multiplier_min", 0.0
            )
        )
        > 2.0
    )
    scalar_kernel_enhancement_import_blocks_hidden_authority = (
        "scalar-kernel enhancement import audit"
        in certificates["scalar_kernel_enhancement_import"].get("actual_current_surface_status", "")
        and certificates["scalar_kernel_enhancement_import"].get("proposal_allowed") is False
        and not any(
            candidate.get("chain_closes")
            for candidate in certificates["scalar_kernel_enhancement_import"].get("candidates", [])
        )
    )
    fitted_kernel_selector_not_closure = (
        "fitted scalar-kernel residue selector no-go"
        in certificates["fitted_kernel_residue_selector"].get("actual_current_surface_status", "")
        and certificates["fitted_kernel_residue_selector"].get("proposal_allowed") is False
        and float(
            certificates["fitted_kernel_residue_selector"].get("summary", {}).get(
                "fitted_multiplier_min", 0.0
            )
        )
        > 1.0
    )
    cl3_source_unit_blocks_kappa = (
        "source-unit normalization no-go" in certificates["cl3_source_unit"].get("actual_current_surface_status", "")
        and certificates["cl3_source_unit"].get("proposal_allowed") is False
    )
    gauge_vev_source_overlap_blocks_kappa = (
        "gauge-VEV source-overlap no-go"
        in certificates["gauge_vev_source_overlap"].get("actual_current_surface_status", "")
        and certificates["gauge_vev_source_overlap"].get("proposal_allowed") is False
    )
    scalar_renormalization_condition_overlap_blocks_kappa = (
        "renormalization-condition source-overlap no-go"
        in certificates["scalar_renormalization_condition_overlap"].get("actual_current_surface_status", "")
        and certificates["scalar_renormalization_condition_overlap"].get("proposal_allowed") is False
    )
    scalar_source_contact_term_scheme_not_lsz = (
        "source contact-term scheme boundary"
        in certificates["scalar_source_contact_term_scheme"].get("actual_current_surface_status", "")
        and certificates["scalar_source_contact_term_scheme"].get("proposal_allowed") is False
    )
    production_manifest_not_evidence = (
        "production manifest" in certificates["fh_lsz_production_manifest"].get("actual_current_surface_status", "")
        and certificates["fh_lsz_production_manifest"].get("proposal_allowed") is False
    )
    production_postprocess_gate_blocks_closure = (
        "FH-LSZ" in certificates["fh_lsz_production_postprocess_gate"].get("actual_current_surface_status", "")
        and certificates["fh_lsz_production_postprocess_gate"].get("proposal_allowed") is False
        and certificates["fh_lsz_production_postprocess_gate"].get("retained_proposal_gate_ready") is False
        and any(
            row.get("satisfied_now") is False
            for row in certificates["fh_lsz_production_postprocess_gate"].get("postprocess_requirements", [])
            if isinstance(row, dict)
        )
    )
    production_checkpoint_not_foreground_safe = (
        "checkpoint granularity gate"
        in certificates["fh_lsz_production_checkpoint_granularity"].get("actual_current_surface_status", "")
        and certificates["fh_lsz_production_checkpoint_granularity"].get("proposal_allowed") is False
        and certificates["fh_lsz_production_checkpoint_granularity"].get("resume_semantics", {}).get(
            "foreground_launch_safe"
        )
        is False
    )
    chunked_manifest_not_evidence = (
        "chunked production manifest"
        in certificates["fh_lsz_chunked_production_manifest"].get("actual_current_surface_status", "")
        and certificates["fh_lsz_chunked_production_manifest"].get("proposal_allowed") is False
        and float(
            certificates["fh_lsz_chunked_production_manifest"].get("chunk_policy", {}).get(
                "estimated_l12_chunk_hours", 0.0
            )
        )
        < 12.0
    )
    chunk_combiner_status = certificates["fh_lsz_chunk_combiner_gate"].get(
        "actual_current_surface_status", ""
    )
    chunk_combiner_not_evidence = (
        (
            "chunk combiner gate" in chunk_combiner_status
            or "complete L12 chunk summary" in chunk_combiner_status
        )
        and certificates["fh_lsz_chunk_combiner_gate"].get("proposal_allowed") is False
    )
    chunk001_checkpoint_not_closure = (
        "chunk001" in certificates["fh_lsz_chunk001_checkpoint"].get("actual_current_surface_status", "")
        and "production checkpoint"
        in certificates["fh_lsz_chunk001_checkpoint"].get("actual_current_surface_status", "")
        and certificates["fh_lsz_chunk001_checkpoint"].get("proposal_allowed") is False
    )
    chunk002_checkpoint_not_closure = (
        "chunk002" in certificates["fh_lsz_chunk002_checkpoint"].get("actual_current_surface_status", "")
        and "production checkpoint"
        in certificates["fh_lsz_chunk002_checkpoint"].get("actual_current_surface_status", "")
        and certificates["fh_lsz_chunk002_checkpoint"].get("proposal_allowed") is False
    )
    ready_chunk_set_status = certificates["fh_lsz_ready_chunk_set_checkpoint"].get(
        "actual_current_surface_status", ""
    )
    ready_chunk_set_not_closure = (
        (
            "ready chunk-set production checkpoint" in ready_chunk_set_status
            or "complete L12 ready chunk-set checkpoint" in ready_chunk_set_status
        )
        and certificates["fh_lsz_ready_chunk_set_checkpoint"].get("proposal_allowed") is False
    )
    ready_chunk_response_not_closure = (
        "ready chunk response-stability diagnostic"
        in certificates["fh_lsz_ready_chunk_response_stability"].get("actual_current_surface_status", "")
        and certificates["fh_lsz_ready_chunk_response_stability"].get("proposal_allowed") is False
        and certificates["fh_lsz_ready_chunk_response_stability"].get("stability_summary", {}).get(
            "stability_passed"
        )
        is False
    )
    chunk011_target_timeseries_not_closure = (
        "chunk011 target-timeseries production checkpoint"
        in certificates["fh_lsz_chunk011_target_timeseries"].get("actual_current_surface_status", "")
        and certificates["fh_lsz_chunk011_target_timeseries"].get("proposal_allowed") is False
        and certificates["fh_lsz_chunk011_target_timeseries"]
        .get("chunk_summary", {})
        .get("target_timeseries_summary", {})
        .get("complete_for_all_ready_chunks")
        is False
    )
    chunk011_generic_target_timeseries_not_closure = (
        "chunk011 generic target-timeseries checkpoint"
        in certificates["fh_lsz_chunk011_target_timeseries_generic"].get("actual_current_surface_status", "")
        and certificates["fh_lsz_chunk011_target_timeseries_generic"].get("proposal_allowed") is False
        and certificates["fh_lsz_chunk011_target_timeseries_generic"].get("chunk_index") == 11
        and certificates["fh_lsz_chunk011_target_timeseries_generic"]
        .get("chunk_summary", {})
        .get("target_timeseries_summary", {})
        .get("complete_for_all_ready_chunks")
        is False
    )
    chunk012_generic_target_timeseries_not_closure = (
        "chunk012 generic target-timeseries checkpoint"
        in certificates["fh_lsz_chunk012_target_timeseries_generic"].get("actual_current_surface_status", "")
        and certificates["fh_lsz_chunk012_target_timeseries_generic"].get("proposal_allowed") is False
        and certificates["fh_lsz_chunk012_target_timeseries_generic"].get("chunk_index") == 12
        and certificates["fh_lsz_chunk012_target_timeseries_generic"]
        .get("chunk_summary", {})
        .get("target_timeseries_summary", {})
        .get("complete_for_all_ready_chunks")
        is False
    )
    generic_chunk_target_certificates = {
        name: cert
        for name, cert in certificates.items()
        if name.startswith("fh_lsz_chunk") and name.endswith("_target_timeseries_generic")
    }
    generic_chunk_targets_not_closure = bool(generic_chunk_target_certificates) and all(
        "generic target-timeseries checkpoint" in cert.get("actual_current_surface_status", "")
        and cert.get("proposal_allowed") is False
        for cert in generic_chunk_target_certificates.values()
    )
    multitau_chunk_target_certificates = {
        name: cert
        for name, cert in certificates.items()
        if name.startswith("fh_lsz_chunk") and name.endswith("_multitau_target_timeseries")
    }
    multitau_chunk_targets_not_closure = bool(multitau_chunk_target_certificates) and all(
        "v2 multi-tau target-timeseries checkpoint" in cert.get("actual_current_surface_status", "")
        and cert.get("proposal_allowed") is False
        for cert in multitau_chunk_target_certificates.values()
    )
    legacy_v2_backfill_not_possible = (
        "legacy chunks001-016 cannot be honestly v2-backfilled"
        in certificates["fh_lsz_legacy_v2_backfill_feasibility"].get("actual_current_surface_status", "")
        and certificates["fh_lsz_legacy_v2_backfill_feasibility"].get("proposal_allowed") is False
        and certificates["fh_lsz_legacy_v2_backfill_feasibility"]
        .get("legacy_summary", {})
        .get("honest_v2_backfill_possible")
        is False
    )
    pole_fit_kinematics_not_closure = (
        "scalar-pole kinematics gate"
        in certificates["fh_lsz_pole_fit_kinematics"].get("actual_current_surface_status", "")
        and certificates["fh_lsz_pole_fit_kinematics"].get("proposal_allowed") is False
    )
    pole_fit_postprocessor_not_evidence = (
        "pole fit postprocessor scaffold"
        in certificates["fh_lsz_pole_fit_postprocessor"].get("actual_current_surface_status", "")
        and certificates["fh_lsz_pole_fit_postprocessor"].get("proposal_allowed") is False
        and certificates["fh_lsz_pole_fit_postprocessor"].get("readiness", {}).get("fit_ready") is False
    )
    finite_shell_identifiability_not_closure = (
        "finite-shell pole-fit identifiability no-go"
        in certificates["fh_lsz_finite_shell_identifiability"].get("actual_current_surface_status", "")
        and certificates["fh_lsz_finite_shell_identifiability"].get("proposal_allowed") is False
        and float(
            certificates["fh_lsz_finite_shell_identifiability"].get("construction", {}).get("checks", {}).get(
                "derivative_span_factor", 0.0
            )
        )
        >= 4.0
    )
    pole_fit_model_class_gate_blocks = (
        "model-class gate blocks finite-shell fit"
        in certificates["fh_lsz_pole_fit_model_class_gate"].get("actual_current_surface_status", "")
        and certificates["fh_lsz_pole_fit_model_class_gate"].get("proposal_allowed") is False
        and certificates["fh_lsz_pole_fit_model_class_gate"].get("model_class_gate_passed") is False
    )
    model_class_semantic_firewall_not_closure = (
        "model-class semantic firewall passed"
        in certificates["fh_lsz_model_class_semantic_firewall"].get("actual_current_surface_status", "")
        and certificates["fh_lsz_model_class_semantic_firewall"].get("proposal_allowed") is False
    )
    stieltjes_model_class_not_enough = (
        "Stieltjes model-class obstruction"
        in certificates["fh_lsz_stieltjes_model_class"].get("actual_current_surface_status", "")
        and certificates["fh_lsz_stieltjes_model_class"].get("proposal_allowed") is False
        and float(
            certificates["fh_lsz_stieltjes_model_class"].get("family", {}).get("checks", {}).get(
                "inverse_derivative_span_factor", 0.0
            )
        )
        >= 8.0
    )
    stieltjes_moment_certificate_absent = (
        "Stieltjes moment-certificate gate"
        in certificates["fh_lsz_stieltjes_moment_certificate_gate"].get(
            "actual_current_surface_status", ""
        )
        and certificates["fh_lsz_stieltjes_moment_certificate_gate"].get("proposal_allowed")
        is False
        and certificates["fh_lsz_stieltjes_moment_certificate_gate"].get(
            "moment_certificate_gate_passed"
        )
        is False
    )
    pade_stieltjes_bounds_certificate_absent = (
        "Pade-Stieltjes bounds gate"
        in certificates["fh_lsz_pade_stieltjes_bounds_gate"].get(
            "actual_current_surface_status", ""
        )
        and certificates["fh_lsz_pade_stieltjes_bounds_gate"].get("proposal_allowed")
        is False
        and certificates["fh_lsz_pade_stieltjes_bounds_gate"].get(
            "pade_stieltjes_bounds_gate_passed"
        )
        is False
    )
    stieltjes_proxy_diagnostic_blocks = (
        "Stieltjes monotonicity"
        in certificates["fh_lsz_polefit8x8_stieltjes_proxy_diagnostic"].get(
            "actual_current_surface_status", ""
        )
        and certificates["fh_lsz_polefit8x8_stieltjes_proxy_diagnostic"].get(
            "proposal_allowed"
        )
        is False
        and certificates["fh_lsz_polefit8x8_stieltjes_proxy_diagnostic"].get(
            "stieltjes_proxy_certificate_passed"
        )
        is False
    )
    complete_bernstein_inverse_diagnostic_blocks = (
        "complete-Bernstein monotonicity"
        in certificates["fh_lsz_complete_bernstein_inverse_diagnostic"].get(
            "actual_current_surface_status", ""
        )
        and certificates["fh_lsz_complete_bernstein_inverse_diagnostic"].get(
            "proposal_allowed"
        )
        is False
        and certificates["fh_lsz_complete_bernstein_inverse_diagnostic"].get(
            "complete_bernstein_inverse_certificate_passed"
        )
        is False
    )
    scalar_lsz_holonomic_exact_authority_blocks = (
        "scalar-LSZ holonomic exact-authority not derivable"
        in certificates["pr230_scalar_lsz_holonomic_exact_authority_attempt"].get(
            "actual_current_surface_status", ""
        )
        and certificates["pr230_scalar_lsz_holonomic_exact_authority_attempt"].get(
            "proposal_allowed"
        )
        is False
        and certificates["pr230_scalar_lsz_holonomic_exact_authority_attempt"].get(
            "holonomic_exact_authority_passed"
        )
        is False
        and certificates["pr230_scalar_lsz_holonomic_exact_authority_attempt"]
        .get("counterfamily", {})
        .get("residues_differ")
        is True
    )
    scalar_lsz_carleman_tauberian_determinacy_blocks = (
        "Carleman/Tauberian scalar-LSZ determinacy not derivable"
        in certificates[
            "pr230_scalar_lsz_carleman_tauberian_determinacy_attempt"
        ].get("actual_current_surface_status", "")
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
        is True
    )
    contact_subtraction_identifiability_blocks = (
        "contact-subtraction identifiability obstruction"
        in certificates["fh_lsz_contact_subtraction_identifiability"].get(
            "actual_current_surface_status", ""
        )
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
        is False
    )
    affine_contact_complete_monotonicity_blocks = (
        "affine contact complete-monotonicity no-go"
        in certificates["fh_lsz_affine_contact_complete_monotonicity"].get(
            "actual_current_surface_status", ""
        )
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
        is False
    )
    polynomial_contact_finite_shell_blocks = (
        "finite-shell polynomial contact non-identifiability no-go"
        in certificates["fh_lsz_polynomial_contact_finite_shell"].get(
            "actual_current_surface_status", ""
        )
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
        is False
    )
    polynomial_contact_repair_blocks = (
        "polynomial contact repair not scalar-LSZ authority"
        in certificates["fh_lsz_polynomial_contact_repair"].get(
            "actual_current_surface_status", ""
        )
        and certificates["fh_lsz_polynomial_contact_repair"].get("proposal_allowed")
        is False
        and certificates["fh_lsz_polynomial_contact_repair"].get(
            "polynomial_contact_repair_no_go_passed"
        )
        is True
        and certificates["fh_lsz_polynomial_contact_repair"].get(
            "stieltjes_certificate_from_polynomial_contact_passed"
        )
        is False
    )
    pole_saturation_threshold_gate_blocks = (
        "pole-saturation threshold gate"
        in certificates["fh_lsz_pole_saturation_threshold_gate"].get("actual_current_surface_status", "")
        and certificates["fh_lsz_pole_saturation_threshold_gate"].get("proposal_allowed") is False
        and certificates["fh_lsz_pole_saturation_threshold_gate"].get("pole_saturation_threshold_gate_passed")
        is False
    )
    threshold_authority_audit_blocks = (
        "threshold-authority import audit"
        in certificates["fh_lsz_threshold_authority_audit"].get("actual_current_surface_status", "")
        and certificates["fh_lsz_threshold_authority_audit"].get("proposal_allowed") is False
    )
    confinement_gap_threshold_import_blocks = (
        "confinement gap not scalar LSZ threshold"
        in certificates["confinement_gap_threshold_import"].get("actual_current_surface_status", "")
        and certificates["confinement_gap_threshold_import"].get("proposal_allowed") is False
        and certificates["confinement_gap_threshold_import"].get("threshold_closed") is False
    )
    finite_volume_pole_saturation_blocks = (
        "finite-volume pole-saturation obstruction"
        in certificates["fh_lsz_finite_volume_pole_saturation"].get("actual_current_surface_status", "")
        and certificates["fh_lsz_finite_volume_pole_saturation"].get("proposal_allowed") is False
    )
    numba_seed_independence_blocks_historical_chunks = (
        "numba seed-independence audit"
        in certificates["fh_lsz_numba_seed_independence"].get("actual_current_surface_status", "")
        and certificates["fh_lsz_numba_seed_independence"].get("proposal_allowed") is False
        and int(
            certificates["fh_lsz_numba_seed_independence"].get(
                "historical_independent_chunks_counted_for_evidence", -1
            )
        )
        == 0
    )
    uniform_gap_self_certification_blocks = (
        "uniform-gap self-certification no-go"
        in certificates["fh_lsz_uniform_gap_self_certification"].get("actual_current_surface_status", "")
        and certificates["fh_lsz_uniform_gap_self_certification"].get("proposal_allowed") is False
    )
    scalar_denominator_closure_attempt_blocked = (
        "scalar denominator theorem closure attempt blocked"
        in certificates["scalar_denominator_theorem_closure"].get("actual_current_surface_status", "")
        and certificates["scalar_denominator_theorem_closure"].get("proposal_allowed") is False
        and certificates["scalar_denominator_theorem_closure"].get("theorem_closed") is False
    )
    soft_continuum_threshold_blocks = (
        "soft-continuum threshold no-go"
        in certificates["fh_lsz_soft_continuum_threshold"].get("actual_current_surface_status", "")
        and certificates["fh_lsz_soft_continuum_threshold"].get("proposal_allowed") is False
        and certificates["fh_lsz_soft_continuum_threshold"].get("uniform_threshold_gap_certified") is False
    )
    reflection_positivity_shortcut_blocks = (
        "reflection positivity not scalar LSZ closure"
        in certificates["reflection_positivity_lsz_shortcut"].get("actual_current_surface_status", "")
        and certificates["reflection_positivity_lsz_shortcut"].get("proposal_allowed") is False
        and certificates["reflection_positivity_lsz_shortcut"]
        .get("reflection_positive_family", {})
        .get("all_reflection_matrices_positive")
        is True
        and float(
            certificates["reflection_positivity_lsz_shortcut"]
            .get("reflection_positive_family", {})
            .get("inverse_derivative_span_factor", 0.0)
        )
        >= 8.0
    )
    effective_potential_hessian_blocks = (
        "effective-potential Hessian not source-overlap identity"
        in certificates["effective_potential_hessian_source_overlap"].get(
            "actual_current_surface_status", ""
        )
        and certificates["effective_potential_hessian_source_overlap"].get("proposal_allowed") is False
        and certificates["effective_potential_hessian_source_overlap"]
        .get("hessian_family", {})
        .get("checks", {})
        .get("canonical_data_fixed")
        is True
        and float(
            certificates["effective_potential_hessian_source_overlap"]
            .get("hessian_family", {})
            .get("checks", {})
            .get("source_overlap_varies", 0.0)
        )
        > 0.4
    )
    brst_nielsen_higgs_identity_blocks = (
        "BRST-Nielsen identities not Higgs-pole identity"
        in certificates["brst_nielsen_higgs_identity"].get("actual_current_surface_status", "")
        and certificates["brst_nielsen_higgs_identity"].get("proposal_allowed") is False
        and certificates["brst_nielsen_higgs_identity"]
        .get("identity_family", {})
        .get("checks", {})
        .get("gauge_identity_surface_fixed")
        is True
        and float(
            certificates["brst_nielsen_higgs_identity"]
            .get("identity_family", {})
            .get("checks", {})
            .get("source_overlap_span", 0.0)
        )
        > 0.5
    )
    cl3_automorphism_source_identity_blocks = (
        "Cl3 automorphism data not source-Higgs identity"
        in certificates["cl3_automorphism_source_identity"].get("actual_current_surface_status", "")
        and certificates["cl3_automorphism_source_identity"].get("proposal_allowed") is False
        and certificates["cl3_automorphism_source_identity"]
        .get("orbit_witness", {})
        .get("checks", {})
        .get("finite_invariants_fixed")
        is True
        and float(
            certificates["cl3_automorphism_source_identity"]
            .get("orbit_witness", {})
            .get("checks", {})
            .get("dprime_span_factor", 0.0)
        )
        >= 8.0
    )
    same_source_pole_data_sufficiency_not_passed = (
        "same-source pole-data sufficiency gate not passed"
        in certificates["same_source_pole_data_sufficiency"].get("actual_current_surface_status", "")
        and certificates["same_source_pole_data_sufficiency"].get("proposal_allowed") is False
        and certificates["same_source_pole_data_sufficiency"].get("gate_passed") is False
    )
    source_functional_lsz_identifiability_blocks = (
        "source-functional LSZ identifiability theorem"
        in certificates["source_functional_lsz_identifiability"].get("actual_current_surface_status", "")
        and certificates["source_functional_lsz_identifiability"].get("proposal_allowed") is False
        and certificates["source_functional_lsz_identifiability"].get("theorem_closed") is False
    )
    isolated_pole_gram_factorization_support = (
        "isolated-pole Gram factorization theorem"
        in certificates["isolated_pole_gram_factorization"].get("actual_current_surface_status", "")
        and certificates["isolated_pole_gram_factorization"].get("proposal_allowed") is False
        and certificates["isolated_pole_gram_factorization"].get(
            "isolated_pole_gram_factorization_theorem_passed"
        )
        is True
    )
    osp_oh_assumption_route_audit_blocks = (
        "O_sp-to-O_H assumption-route audit complete"
        in certificates["osp_oh_assumption_route_audit"].get("actual_current_surface_status", "")
        and certificates["osp_oh_assumption_route_audit"].get("proposal_allowed") is False
        and certificates["osp_oh_assumption_route_audit"].get("assumption_route_audit_passed")
        is True
    )
    osp_oh_literature_bridge_not_closure = (
        "O_sp/O_H literature bridge" in certificates["osp_oh_literature_bridge"].get(
            "actual_current_surface_status", ""
        )
        and certificates["osp_oh_literature_bridge"].get("proposal_allowed") is False
        and certificates["osp_oh_literature_bridge"].get("literature_bridge_passed") is True
    )
    fms_oh_certificate_construction_attempt_blocks = (
        "FMS O_H certificate construction blocked"
        in certificates["fms_oh_certificate_construction_attempt"].get(
            "actual_current_surface_status", ""
        )
        and certificates["fms_oh_certificate_construction_attempt"].get("proposal_allowed") is False
        and certificates["fms_oh_certificate_construction_attempt"].get(
            "fms_oh_certificate_available"
        )
        is False
        and certificates["fms_oh_certificate_construction_attempt"].get(
            "fms_construction_attempt_passed_as_boundary"
        )
        is True
    )
    action_first_oh_artifact_attempt_blocks = (
        "action-first O_H artifact not constructible"
        in certificates["pr230_action_first_oh_artifact_attempt"].get(
            "actual_current_surface_status", ""
        )
        and certificates["pr230_action_first_oh_artifact_attempt"].get("proposal_allowed")
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
        is False
    )
    holonomic_source_response_gate_blocks = (
        "PR541-style holonomic source-response route"
        in certificates["pr230_holonomic_source_response_feasibility_gate"].get(
            "actual_current_surface_status", ""
        )
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
        is False
    )
    oh_source_higgs_authority_rescan_blocks = (
        "O_H/source-Higgs authority rescan found no"
        in certificates["pr230_oh_source_higgs_authority_rescan_gate"].get(
            "actual_current_surface_status", ""
        )
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
        is True
    )
    minimal_axioms_yukawa_summary_firewall_blocks = (
        "minimal-axioms Yukawa summary is not PR230 proof authority"
        in certificates["pr230_minimal_axioms_yukawa_summary_firewall"].get(
            "actual_current_surface_status", ""
        )
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
        == "audited_renaming"
    )
    genuine_source_pole_artifact_support_only = (
        "genuine same-source O_sp source-pole artifact"
        in certificates["pr230_genuine_source_pole_artifact_intake"].get(
            "actual_current_surface_status", ""
        )
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
        is False
    )
    l12_chunk_compute_status_support_only = (
        "completed L12 same-source chunk compute status"
        in certificates["pr230_l12_chunk_compute_status"].get(
            "actual_current_surface_status", ""
        )
        and certificates["pr230_l12_chunk_compute_status"].get("proposal_allowed")
        is False
        and certificates["pr230_l12_chunk_compute_status"].get(
            "strict_closure_blockers", {}
        ).get("scalar_lsz_denominator_certificate_absent")
        is True
        and certificates["pr230_l12_chunk_compute_status"].get(
            "strict_closure_blockers", {}
        ).get("canonical_oh_or_source_higgs_overlap_absent")
        is True
    )
    negative_route_applicability_review_passed = (
        "negative-route applicability review passed"
        in certificates["pr230_negative_route_applicability_review"].get(
            "actual_current_surface_status", ""
        )
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
        is True
    )
    taste_condensate_oh_bridge_blocks_shortcut = (
        "taste-condensate Higgs stack does not supply PR230 O_H bridge"
        in certificates["pr230_taste_condensate_oh_bridge_audit"].get(
            "actual_current_surface_status", ""
        )
        and certificates["pr230_taste_condensate_oh_bridge_audit"].get(
            "proposal_allowed"
        )
        is False
        and certificates["pr230_taste_condensate_oh_bridge_audit"].get(
            "taste_condensate_oh_bridge_audit_passed"
        )
        is True
        and certificates["pr230_taste_condensate_oh_bridge_audit"].get(
            "algebra", {}
        ).get("uniform_source_relative_projection_onto_taste_axis_span")
        == 0.0
    )
    source_coordinate_transport_blocks_current_shortcut = (
        "source-coordinate transport to canonical O_H not derivable"
        in certificates["pr230_source_coordinate_transport_gate"].get(
            "actual_current_surface_status", ""
        )
        and certificates["pr230_source_coordinate_transport_gate"].get(
            "proposal_allowed"
        )
        is False
        and certificates["pr230_source_coordinate_transport_gate"].get(
            "source_coordinate_transport_gate_passed"
        )
        is True
        and certificates["pr230_source_coordinate_transport_gate"].get(
            "future_transport_certificate_present"
        )
        is False
    )
    origin_main_composite_higgs_intake_not_closure = (
        "origin/main composite-Higgs stretch"
        in certificates["pr230_origin_main_composite_higgs_intake_guard"].get(
            "actual_current_surface_status", ""
        )
        and certificates["pr230_origin_main_composite_higgs_intake_guard"].get(
            "proposal_allowed"
        )
        is False
        and certificates["pr230_origin_main_composite_higgs_intake_guard"].get(
            "origin_main_composite_higgs_intake_guard_passed"
        )
        is True
        and certificates["pr230_origin_main_composite_higgs_intake_guard"].get(
            "origin_main_composite_higgs_closes_pr230"
        )
        is False
    )
    origin_main_ew_m_residual_intake_not_closure = (
        "origin/main EW M-residual CMT packet"
        in certificates["pr230_origin_main_ew_m_residual_intake_guard"].get(
            "actual_current_surface_status", ""
        )
        and certificates["pr230_origin_main_ew_m_residual_intake_guard"].get(
            "proposal_allowed"
        )
        is False
        and certificates["pr230_origin_main_ew_m_residual_intake_guard"].get(
            "origin_main_ew_m_residual_intake_guard_passed"
        )
        is True
        and certificates["pr230_origin_main_ew_m_residual_intake_guard"].get(
            "origin_main_ew_m_residual_closes_pr230"
        )
        is False
    )
    z3_triplet_conditional_primitive_not_closure = (
        "Z3-triplet primitive-cone theorem"
        in certificates["pr230_z3_triplet_conditional_primitive_cone"].get(
            "actual_current_surface_status", ""
        )
        and certificates["pr230_z3_triplet_conditional_primitive_cone"].get(
            "proposal_allowed"
        )
        is False
        and certificates["pr230_z3_triplet_conditional_primitive_cone"].get(
            "z3_triplet_conditional_primitive_theorem_passed"
        )
        is True
        and certificates["pr230_z3_triplet_conditional_primitive_cone"].get(
            "pr230_closure_authorized"
        )
        is False
        and certificates["pr230_z3_triplet_conditional_primitive_cone"].get(
            "writes_strict_future_certificate"
        )
        is False
    )
    z3_triplet_positive_cone_h2_support_not_transfer = (
        "Z3-triplet positive-cone H2 support"
        in certificates["pr230_z3_triplet_positive_cone_support"].get(
            "actual_current_surface_status", ""
        )
        and certificates["pr230_z3_triplet_positive_cone_support"].get(
            "proposal_allowed"
        )
        is False
        and certificates["pr230_z3_triplet_positive_cone_support"].get(
            "z3_triplet_positive_cone_h2_support_passed"
        )
        is True
        and certificates["pr230_z3_triplet_positive_cone_support"].get(
            "pr230_closure_authorized"
        )
        is False
        and certificates["pr230_z3_triplet_positive_cone_support"].get(
            "supplies_conditional_premises", {}
        ).get("H2_positive_cone_equal_magnitude_support")
        is True
        and certificates["pr230_z3_triplet_positive_cone_support"].get(
            "supplies_conditional_premises", {}
        ).get("H3_lazy_positive_physical_transfer")
        is False
    )
    z3_generation_action_lift_not_derived = (
        "Z3 generation-action lift"
        in certificates["pr230_z3_generation_action_lift_attempt"].get(
            "actual_current_surface_status", ""
        )
        and certificates["pr230_z3_generation_action_lift_attempt"].get(
            "proposal_allowed"
        )
        is False
        and certificates["pr230_z3_generation_action_lift_attempt"].get(
            "h1_generation_action_lift_attempt_passed"
        )
        is True
        and certificates["pr230_z3_generation_action_lift_attempt"].get(
            "same_surface_h1_derived"
        )
        is False
        and certificates["pr230_z3_generation_action_lift_attempt"].get(
            "pr230_closure_authorized"
        )
        is False
    )
    z3_lazy_transfer_promotion_not_derived = (
        "Z3 lazy-transfer promotion not derivable"
        in certificates["pr230_z3_lazy_transfer_promotion_attempt"].get(
            "actual_current_surface_status", ""
        )
        and certificates["pr230_z3_lazy_transfer_promotion_attempt"].get(
            "proposal_allowed"
        )
        is False
        and certificates["pr230_z3_lazy_transfer_promotion_attempt"].get(
            "z3_lazy_transfer_promotion_attempt_passed"
        )
        is True
        and certificates["pr230_z3_lazy_transfer_promotion_attempt"].get(
            "physical_lazy_transfer_instantiated"
        )
        is False
        and certificates["pr230_z3_lazy_transfer_promotion_attempt"].get(
            "pr230_closure_authorized"
        )
        is False
    )
    z3_lazy_selector_no_go_blocks = (
        "Z3 lazy selector shortcuts do not derive"
        in certificates["pr230_z3_lazy_selector_no_go"].get(
            "actual_current_surface_status", ""
        )
        and certificates["pr230_z3_lazy_selector_no_go"].get("proposal_allowed")
        is False
        and certificates["pr230_z3_lazy_selector_no_go"].get(
            "z3_lazy_selector_no_go_passed"
        )
        is True
        and certificates["pr230_z3_lazy_selector_no_go"].get(
            "physical_lazy_transfer_instantiated"
        )
        is False
        and certificates["pr230_z3_lazy_selector_no_go"].get(
            "pr230_closure_authorized"
        )
        is False
    )
    same_surface_z3_taste_triplet_support_not_closure = (
        "same-surface Z3 taste-triplet artifact"
        in certificates["pr230_same_surface_z3_taste_triplet"].get(
            "actual_current_surface_status", ""
        )
        and certificates["pr230_same_surface_z3_taste_triplet"].get(
            "proposal_allowed"
        )
        is False
        and certificates["pr230_same_surface_z3_taste_triplet"].get(
            "same_surface_z3_triplet_artifact_passed"
        )
        is True
        and certificates["pr230_same_surface_z3_taste_triplet"].get(
            "pr230_closure_authorized"
        )
        is False
    )
    source_coordinate_transport_completion_blocks = (
        "source-coordinate transport not derivable from current PR230 surface"
        in certificates["pr230_source_coordinate_transport_completion"].get(
            "actual_current_surface_status", ""
        )
        and certificates["pr230_source_coordinate_transport_completion"].get(
            "proposal_allowed"
        )
        is False
        and certificates["pr230_source_coordinate_transport_completion"].get(
            "source_coordinate_transport_completion_passed"
        )
        is True
        and certificates["pr230_source_coordinate_transport_completion"].get(
            "algebra", {}
        ).get("source_relative_projection_onto_taste_axis_span")
        == 0.0
    )
    two_source_taste_radial_chart_support_not_closure = (
        "two-source taste-radial chart"
        in certificates["pr230_two_source_taste_radial_chart"].get(
            "actual_current_surface_status", ""
        )
        and certificates["pr230_two_source_taste_radial_chart"].get(
            "proposal_allowed"
        )
        is False
        and certificates["pr230_two_source_taste_radial_chart"].get(
            "two_source_taste_radial_chart_support_passed"
        )
        is True
        and certificates["pr230_two_source_taste_radial_chart"].get(
            "forbidden_firewall", {}
        ).get("identified_taste_radial_axis_with_canonical_oh")
        is False
    )
    two_source_taste_radial_action_support_not_closure = (
        "two-source taste-radial action source vertex"
        in certificates["pr230_two_source_taste_radial_action"].get(
            "actual_current_surface_status", ""
        )
        and certificates["pr230_two_source_taste_radial_action"].get(
            "proposal_allowed"
        )
        is False
        and certificates["pr230_two_source_taste_radial_action"].get(
            "two_source_taste_radial_action_passed"
        )
        is True
        and certificates["pr230_two_source_taste_radial_action"].get(
            "operator_certificate_payload", {}
        ).get("canonical_higgs_operator_identity_passed")
        is False
    )
    two_source_taste_radial_row_contract_support_not_closure = (
        "two-source taste-radial C_sx/C_xx row contract"
        in certificates["pr230_two_source_taste_radial_row_contract"].get(
            "actual_current_surface_status", ""
        )
        and certificates["pr230_two_source_taste_radial_row_contract"].get(
            "proposal_allowed"
        )
        is False
        and certificates["pr230_two_source_taste_radial_row_contract"].get(
            "two_source_taste_radial_row_contract_passed"
        )
        is True
        and certificates["pr230_two_source_taste_radial_row_contract"].get(
            "future_file_presence", {}
        ).get("taste_radial_production_rows")
        is False
    )
    two_source_taste_radial_row_manifest_support_not_closure = (
        "two-source taste-radial C_sx/C_xx production manifest"
        in certificates["pr230_two_source_taste_radial_row_production_manifest"].get(
            "actual_current_surface_status", ""
        )
        and certificates["pr230_two_source_taste_radial_row_production_manifest"].get(
            "proposal_allowed"
        )
        is False
        and certificates["pr230_two_source_taste_radial_row_production_manifest"].get(
            "manifest_passed"
        )
        is True
        and certificates["pr230_two_source_taste_radial_row_production_manifest"].get(
            "dry_run_only"
        )
        is True
        and certificates["pr230_two_source_taste_radial_row_production_manifest"].get(
            "future_combined_rows_present"
        )
        is False
    )
    two_source_combiner = certificates["pr230_two_source_taste_radial_row_combiner_gate"]
    two_source_combiner_ready = two_source_combiner.get("ready_chunks")
    two_source_combiner_expected = two_source_combiner.get("expected_chunks")
    two_source_combiner_support_boundary = (
        isinstance(two_source_combiner_ready, int)
        and isinstance(two_source_combiner_expected, int)
        and (
            (
                two_source_combiner.get("combined_rows_written") is False
                and 0 < two_source_combiner_ready < two_source_combiner_expected
            )
            or (
                two_source_combiner.get("combined_rows_written") is True
                and two_source_combiner_ready == two_source_combiner_expected == 63
            )
        )
    )
    two_source_taste_radial_row_combiner_support_not_closure = (
        "two-source taste-radial C_sx/C_xx row combiner gate"
        in two_source_combiner.get("actual_current_surface_status", "")
        and two_source_combiner.get("proposal_allowed") is False
        and two_source_combiner_support_boundary
        and two_source_combiner.get("fail_count") == 0
    )
    two_source_taste_radial_schur_subblock_support_not_closure = (
        "two-source taste-radial Schur-subblock witness"
        in certificates["pr230_two_source_taste_radial_schur_subblock_witness"].get(
            "actual_current_surface_status", ""
        )
        and certificates["pr230_two_source_taste_radial_schur_subblock_witness"].get(
            "proposal_allowed"
        )
        is False
        and certificates["pr230_two_source_taste_radial_schur_subblock_witness"].get(
            "two_source_taste_radial_schur_subblock_witness_passed"
        )
        is True
        and certificates["pr230_two_source_taste_radial_schur_subblock_witness"].get(
            "strict_schur_kernel_row_contract_passed"
        )
        is False
        and certificates["pr230_two_source_taste_radial_schur_subblock_witness"].get(
            "canonical_higgs_operator_identity_passed"
        )
        is False
    )
    two_source_taste_radial_kprime_scout_not_closure = (
        "finite-shell Schur inverse-slope scout"
        in certificates[
            "pr230_two_source_taste_radial_schur_kprime_finite_shell_scout"
        ].get("actual_current_surface_status", "")
        and certificates[
            "pr230_two_source_taste_radial_schur_kprime_finite_shell_scout"
        ].get("proposal_allowed")
        is False
        and certificates[
            "pr230_two_source_taste_radial_schur_kprime_finite_shell_scout"
        ].get("finite_shell_schur_kprime_scout_passed")
        is True
        and certificates[
            "pr230_two_source_taste_radial_schur_kprime_finite_shell_scout"
        ].get("strict_schur_kprime_authority_passed")
        is False
        and certificates[
            "pr230_two_source_taste_radial_schur_kprime_finite_shell_scout"
        ].get("pole_location_or_derivative_rows_present")
        is False
        and certificates[
            "pr230_two_source_taste_radial_schur_kprime_finite_shell_scout"
        ].get("canonical_higgs_operator_identity_passed")
        is False
    )
    two_source_taste_radial_schur_abc_finite_rows_not_closure = (
        "finite Schur A/B/C inverse-block rows"
        in certificates[
            "pr230_two_source_taste_radial_schur_abc_finite_rows"
        ].get("actual_current_surface_status", "")
        and certificates[
            "pr230_two_source_taste_radial_schur_abc_finite_rows"
        ].get("proposal_allowed")
        is False
        and certificates[
            "pr230_two_source_taste_radial_schur_abc_finite_rows"
        ].get("two_source_taste_radial_schur_abc_finite_rows_passed")
        is True
        and certificates[
            "pr230_two_source_taste_radial_schur_abc_finite_rows"
        ].get("finite_schur_abc_rows_written")
        is True
        and certificates[
            "pr230_two_source_taste_radial_schur_abc_finite_rows"
        ].get("strict_schur_abc_kernel_rows_written")
        is False
        and certificates[
            "pr230_two_source_taste_radial_schur_abc_finite_rows"
        ].get("strict_schur_kprime_authority_passed")
        is False
        and certificates[
            "pr230_two_source_taste_radial_schur_abc_finite_rows"
        ].get("canonical_higgs_operator_identity_passed")
        is False
    )
    two_source_taste_radial_schur_pole_lift_gate_blocks_endpoint_promotion = (
        "finite Schur A/B/C rows do not lift to strict pole-row authority"
        in certificates[
            "pr230_two_source_taste_radial_schur_pole_lift_gate"
        ].get("actual_current_surface_status", "")
        and certificates[
            "pr230_two_source_taste_radial_schur_pole_lift_gate"
        ].get("proposal_allowed")
        is False
        and certificates[
            "pr230_two_source_taste_radial_schur_pole_lift_gate"
        ].get("two_source_taste_radial_schur_pole_lift_gate_passed")
        is True
        and certificates[
            "pr230_two_source_taste_radial_schur_pole_lift_gate"
        ].get("strict_pole_lift_passed")
        is False
        and certificates[
            "pr230_two_source_taste_radial_schur_pole_lift_gate"
        ].get("endpoint_derivative_nonidentifiability_witness_passed")
        is True
    )
    two_source_taste_radial_primitive_transfer_candidate_not_h3 = (
        "finite C_sx rows do not certify a physical primitive neutral transfer"
        in certificates[
            "pr230_two_source_taste_radial_primitive_transfer_candidate_gate"
        ].get("actual_current_surface_status", "")
        and certificates[
            "pr230_two_source_taste_radial_primitive_transfer_candidate_gate"
        ].get("proposal_allowed")
        is False
        and certificates[
            "pr230_two_source_taste_radial_primitive_transfer_candidate_gate"
        ].get("physical_transfer_candidate_accepted")
        is False
        and certificates[
            "pr230_two_source_taste_radial_primitive_transfer_candidate_gate"
        ].get("finite_offdiagonal_correlation_support")
        is True
        and certificates[
            "pr230_two_source_taste_radial_primitive_transfer_candidate_gate"
        ].get("finite_correlator_blocks_positive")
        is True
    )
    orthogonal_top_coupling_exclusion_candidate_rejected = (
        "orthogonal-neutral top-coupling exclusion candidate rejected"
        in certificates[
            "pr230_orthogonal_top_coupling_exclusion_candidate_gate"
        ].get("actual_current_surface_status", "")
        and certificates[
            "pr230_orthogonal_top_coupling_exclusion_candidate_gate"
        ].get("proposal_allowed")
        is False
        and certificates[
            "pr230_orthogonal_top_coupling_exclusion_candidate_gate"
        ].get("orthogonal_top_coupling_exclusion_candidate_accepted")
        is False
        and certificates[
            "pr230_orthogonal_top_coupling_exclusion_candidate_gate"
        ].get("finite_c_sx_rows_are_top_coupling_tomography")
        is False
    )
    strict_scalar_lsz_moment_fv_authority_absent = (
        "raw C_ss rows do not supply strict scalar-LSZ moment/FV authority"
        in certificates[
            "pr230_strict_scalar_lsz_moment_fv_authority_gate"
        ].get("actual_current_surface_status", "")
        and certificates[
            "pr230_strict_scalar_lsz_moment_fv_authority_gate"
        ].get("proposal_allowed")
        is False
        and certificates[
            "pr230_strict_scalar_lsz_moment_fv_authority_gate"
        ].get("strict_scalar_lsz_moment_fv_authority_gate_passed")
        is True
        and certificates[
            "pr230_strict_scalar_lsz_moment_fv_authority_gate"
        ].get("strict_scalar_lsz_moment_fv_authority_present")
        is False
        and certificates[
            "pr230_strict_scalar_lsz_moment_fv_authority_gate"
        ].get("current_raw_c_ss_proxy_fails_stieltjes_monotonicity")
        is True
    )
    two_source_taste_radial_chunk_package_support_not_closure = (
        "two-source taste-radial chunks001-"
        in certificates["pr230_two_source_taste_radial_chunk_package"].get(
            "actual_current_surface_status", ""
        )
        and certificates["pr230_two_source_taste_radial_chunk_package"].get(
            "chunk_package_audit_passed"
        )
        is True
        and certificates["pr230_two_source_taste_radial_chunk_package"].get(
            "active_chunks_counted_as_evidence"
        )
        is False
        and certificates["pr230_two_source_taste_radial_chunk_package"].get(
            "proposal_allowed"
        )
        is False
    )
    source_higgs_pole_row_contract_open = (
        "source-Higgs C_ss/C_sH/C_HH pole-row acceptance contract"
        in certificates["pr230_source_higgs_pole_row_acceptance_contract"].get(
            "actual_current_surface_status", ""
        )
        and certificates["pr230_source_higgs_pole_row_acceptance_contract"].get(
            "source_higgs_pole_row_acceptance_contract_passed"
        )
        is True
        and certificates["pr230_source_higgs_pole_row_acceptance_contract"].get(
            "closure_contract_satisfied"
        )
        is False
        and certificates["pr230_source_higgs_pole_row_acceptance_contract"].get(
            "proposal_allowed"
        )
        is False
    )
    schur_complement_stieltjes_repair_support_not_closure = (
        "Schur-complement Stieltjes repair split"
        in certificates[
            "pr230_schur_complement_stieltjes_repair_gate"
        ].get("actual_current_surface_status", "")
        and certificates[
            "pr230_schur_complement_stieltjes_repair_gate"
        ].get("proposal_allowed")
        is False
        and certificates[
            "pr230_schur_complement_stieltjes_repair_gate"
        ].get("schur_complement_stieltjes_repair_gate_passed")
        is True
        and certificates[
            "pr230_schur_complement_stieltjes_repair_gate"
        ].get("source_given_x_stieltjes_first_shell_failed")
        is True
        and certificates[
            "pr230_schur_complement_stieltjes_repair_gate"
        ].get("x_given_source_stieltjes_first_shell_passed")
        is True
        and certificates[
            "pr230_schur_complement_stieltjes_repair_gate"
        ].get("strict_scalar_lsz_authority_present")
        is False
        and certificates[
            "pr230_schur_complement_stieltjes_repair_gate"
        ].get("canonical_higgs_operator_identity_passed")
        is False
    )
    schur_complement_complete_monotonicity_support_not_closure = (
        "C_x|s Schur residual passes"
        in certificates[
            "pr230_schur_complement_complete_monotonicity_gate"
        ].get("actual_current_surface_status", "")
        and certificates[
            "pr230_schur_complement_complete_monotonicity_gate"
        ].get("proposal_allowed")
        is False
        and certificates[
            "pr230_schur_complement_complete_monotonicity_gate"
        ].get("schur_complement_complete_monotonicity_gate_passed")
        is True
        and certificates[
            "pr230_schur_complement_complete_monotonicity_gate"
        ].get("complete_monotonicity_authority_passed")
        is False
        and certificates[
            "pr230_schur_complement_complete_monotonicity_gate"
        ].get("canonical_higgs_or_physical_response_bridge_present")
        is False
    )
    schur_x_given_source_one_pole_scout_not_authority = (
        "one-pole finite-residue scout"
        in certificates[
            "pr230_schur_x_given_source_one_pole_scout"
        ].get("actual_current_surface_status", "")
        and certificates[
            "pr230_schur_x_given_source_one_pole_scout"
        ].get("proposal_allowed")
        is False
        and certificates[
            "pr230_schur_x_given_source_one_pole_scout"
        ].get("schur_x_given_source_one_pole_scout_passed")
        is True
        and certificates[
            "pr230_schur_x_given_source_one_pole_scout"
        ].get("one_pole_fit_valid")
        is True
        and certificates[
            "pr230_schur_x_given_source_one_pole_scout"
        ].get("one_pole_model_class_authority_passed")
        is False
        and certificates[
            "pr230_schur_x_given_source_one_pole_scout"
        ].get("two_pole_counterfamily_present")
        is True
        and certificates[
            "pr230_schur_x_given_source_one_pole_scout"
        ].get("physical_pole_residue_authority_present")
        is False
    )
    taste_radial_canonical_oh_selector_blocks_symmetry_shortcut = (
        "degree-one taste-radial uniqueness"
        in certificates["pr230_taste_radial_canonical_oh_selector_gate"].get(
            "actual_current_surface_status", ""
        )
        and certificates["pr230_taste_radial_canonical_oh_selector_gate"].get(
            "proposal_allowed"
        )
        is False
        and certificates["pr230_taste_radial_canonical_oh_selector_gate"].get(
            "taste_radial_canonical_oh_selector_gate_passed"
        )
        is True
        and certificates["pr230_taste_radial_canonical_oh_selector_gate"].get(
            "degree_one_radial_unique"
        )
        is True
        and certificates["pr230_taste_radial_canonical_oh_selector_gate"].get(
            "full_invariant_selector_nonunique"
        )
        is True
        and certificates["pr230_taste_radial_canonical_oh_selector_gate"].get(
            "canonical_oh_selector_absent"
        )
        is True
    )
    degree_one_higgs_action_premise_not_derived = (
        "degree-one Higgs-action premise not derived"
        in certificates["pr230_degree_one_higgs_action_premise_gate"].get(
            "actual_current_surface_status", ""
        )
        and certificates["pr230_degree_one_higgs_action_premise_gate"].get(
            "proposal_allowed"
        )
        is False
        and certificates["pr230_degree_one_higgs_action_premise_gate"].get(
            "degree_one_higgs_action_premise_gate_passed"
        )
        is True
        and certificates["pr230_degree_one_higgs_action_premise_gate"].get(
            "degree_one_filter_selects_e1"
        )
        is True
        and certificates["pr230_degree_one_higgs_action_premise_gate"].get(
            "degree_one_premise_authorized_on_current_surface"
        )
        is False
    )
    degree_one_radial_tangent_oh_theorem_support_not_closure = (
        "degree-one radial-tangent O_H uniqueness theorem"
        in certificates["pr230_degree_one_radial_tangent_oh_theorem"].get(
            "actual_current_surface_status", ""
        )
        and certificates["pr230_degree_one_radial_tangent_oh_theorem"].get(
            "proposal_allowed"
        )
        is False
        and certificates["pr230_degree_one_radial_tangent_oh_theorem"].get(
            "degree_one_radial_tangent_oh_theorem_passed"
        )
        is True
        and certificates["pr230_degree_one_radial_tangent_oh_theorem"].get(
            "degree_one_tangent_unique"
        )
        is True
        and certificates["pr230_degree_one_radial_tangent_oh_theorem"].get(
            "same_surface_linear_tangent_premise_derived"
        )
        is False
        and certificates["pr230_degree_one_radial_tangent_oh_theorem"].get(
            "canonical_oh_identity_derived"
        )
        is False
        and certificates["pr230_degree_one_radial_tangent_oh_theorem"].get(
            "source_higgs_pole_rows_present"
        )
        is False
    )
    taste_radial_to_source_higgs_promotion_contract_support_not_closure = (
        "taste-radial-to-source-Higgs promotion contract"
        in certificates["pr230_taste_radial_to_source_higgs_promotion_contract"].get(
            "actual_current_surface_status", ""
        )
        and certificates["pr230_taste_radial_to_source_higgs_promotion_contract"].get(
            "promotion_contract_passed"
        )
        is True
        and certificates["pr230_taste_radial_to_source_higgs_promotion_contract"].get(
            "current_promotion_allowed"
        )
        is False
        and certificates["pr230_taste_radial_to_source_higgs_promotion_contract"].get(
            "proposal_allowed"
        )
        is False
        and "same_surface_canonical_O_H_identity_absent"
        in certificates["pr230_taste_radial_to_source_higgs_promotion_contract"].get(
            "current_promotion_blockers", []
        )
        and certificates["pr230_taste_radial_to_source_higgs_promotion_contract"].get(
            "row_packet_status", {}
        ).get("canonical_source_higgs_rows_present")
        is False
    )
    fms_post_degree_route_support_not_closure = (
        "FMS post-degree route rescore"
        in certificates["pr230_fms_post_degree_route_rescore"].get(
            "actual_current_surface_status", ""
        )
        and certificates["pr230_fms_post_degree_route_rescore"].get(
            "proposal_allowed"
        )
        is False
        and certificates["pr230_fms_post_degree_route_rescore"].get(
            "fms_post_degree_route_rescore_passed"
        )
        is True
        and certificates["pr230_fms_post_degree_route_rescore"].get(
            "forbidden_firewall", {}
        ).get("used_literature_as_proof_authority")
        is False
        and certificates["pr230_fms_post_degree_route_rescore"].get(
            "forbidden_firewall", {}
        ).get("used_degree_or_odd_parity_as_oh_authority")
        is False
    )
    fms_composite_oh_conditional_support_not_closure = (
        "FMS composite O_H theorem"
        in certificates["pr230_fms_composite_oh_conditional_theorem"].get(
            "actual_current_surface_status", ""
        )
        and certificates["pr230_fms_composite_oh_conditional_theorem"].get(
            "proposal_allowed"
        )
        is False
        and certificates["pr230_fms_composite_oh_conditional_theorem"].get(
            "fms_composite_oh_conditional_theorem_passed"
        )
        is True
        and certificates["pr230_fms_composite_oh_conditional_theorem"].get(
            "current_closure_authority_present"
        )
        is False
        and certificates["pr230_fms_composite_oh_conditional_theorem"].get(
            "same_surface_action_absent"
        )
        is True
        and certificates["pr230_fms_composite_oh_conditional_theorem"].get(
            "source_higgs_rows_absent"
        )
        is True
    )
    fms_oh_candidate_action_packet_support_not_closure = (
        "FMS O_H candidate/action packet"
        in certificates["pr230_fms_oh_candidate_action_packet"].get(
            "actual_current_surface_status", ""
        )
        and certificates["pr230_fms_oh_candidate_action_packet"].get(
            "proposal_allowed"
        )
        is False
        and certificates["pr230_fms_oh_candidate_action_packet"].get(
            "fms_oh_candidate_action_packet_passed"
        )
        is True
        and certificates["pr230_fms_oh_candidate_action_packet"].get(
            "accepted_current_surface"
        )
        is False
        and certificates["pr230_fms_oh_candidate_action_packet"].get(
            "same_surface_cl3_z3_derived"
        )
        is False
        and certificates["pr230_fms_oh_candidate_action_packet"].get(
            "external_extension_required"
        )
        is True
        and certificates["pr230_fms_oh_candidate_action_packet"].get(
            "closure_authorized"
        )
        is False
    )
    fms_source_overlap_readout_gate_support_not_closure = (
        "FMS source-overlap readout gate"
        in certificates["pr230_fms_source_overlap_readout_gate"].get(
            "actual_current_surface_status", ""
        )
        and certificates["pr230_fms_source_overlap_readout_gate"].get(
            "proposal_allowed"
        )
        is False
        and certificates["pr230_fms_source_overlap_readout_gate"].get(
            "fms_source_overlap_readout_gate_passed"
        )
        is True
        and certificates["pr230_fms_source_overlap_readout_gate"].get(
            "readout_executable_now"
        )
        is False
        and certificates["pr230_fms_source_overlap_readout_gate"].get(
            "strict_rows_present"
        )
        is False
        and certificates["pr230_fms_source_overlap_readout_gate"].get(
            "closure_authorized"
        )
        is False
    )
    fms_action_adoption_minimal_cut_support_not_closure = (
        "FMS action-adoption minimal cut"
        in certificates["pr230_fms_action_adoption_minimal_cut"].get(
            "actual_current_surface_status", ""
        )
        and certificates["pr230_fms_action_adoption_minimal_cut"].get(
            "proposal_allowed"
        )
        is False
        and certificates["pr230_fms_action_adoption_minimal_cut"].get(
            "fms_action_adoption_minimal_cut_passed"
        )
        is True
        and certificates["pr230_fms_action_adoption_minimal_cut"].get(
            "adoption_allowed_now"
        )
        is False
        and certificates["pr230_fms_action_adoption_minimal_cut"].get(
            "accepted_current_surface"
        )
        is False
        and certificates["pr230_fms_action_adoption_minimal_cut"].get(
            "same_surface_cl3_z3_derived"
        )
        is False
        and certificates["pr230_fms_action_adoption_minimal_cut"].get(
            "closure_authorized"
        )
        is False
        and bool(
            certificates["pr230_fms_action_adoption_minimal_cut"].get(
                "missing_root_vertices"
            )
        )
    )
    higgs_mass_source_action_bridge_support_not_closure = (
        "Higgs mass-source action bridge"
        in certificates["pr230_higgs_mass_source_action_bridge"].get(
            "actual_current_surface_status", ""
        )
        and certificates["pr230_higgs_mass_source_action_bridge"].get(
            "proposal_allowed"
        )
        is False
        and certificates["pr230_higgs_mass_source_action_bridge"].get(
            "higgs_mass_source_action_bridge_passed"
        )
        is True
        and certificates["pr230_higgs_mass_source_action_bridge"].get(
            "same_surface_ew_action_certificate_absent"
        )
        is True
        and certificates["pr230_higgs_mass_source_action_bridge"].get(
            "canonical_oh_absent"
        )
        is True
        and certificates["pr230_higgs_mass_source_action_bridge"].get(
            "source_higgs_rows_absent"
        )
        is True
    )
    post_fms_source_overlap_necessity_blocks_current_inference = (
        "post-FMS source-overlap not derivable"
        in certificates["pr230_post_fms_source_overlap_necessity_gate"].get(
            "actual_current_surface_status", ""
        )
        and certificates["pr230_post_fms_source_overlap_necessity_gate"].get(
            "proposal_allowed"
        )
        is False
        and certificates["pr230_post_fms_source_overlap_necessity_gate"].get(
            "post_fms_source_overlap_necessity_gate_passed"
        )
        is True
        and certificates["pr230_post_fms_source_overlap_necessity_gate"].get(
            "current_source_overlap_authority_present"
        )
        is False
        and certificates["pr230_post_fms_source_overlap_necessity_gate"].get(
            "two_source_rows_are_c_sx_not_c_sH"
        )
        is True
    )
    source_higgs_overlap_kappa_contract_support_not_closure = (
        "source-Higgs overlap-kappa row contract"
        in certificates["pr230_source_higgs_overlap_kappa_contract"].get(
            "actual_current_surface_status", ""
        )
        and certificates["pr230_source_higgs_overlap_kappa_contract"].get(
            "proposal_allowed"
        )
        is False
        and certificates["pr230_source_higgs_overlap_kappa_contract"].get(
            "source_higgs_overlap_kappa_contract_passed"
        )
        is True
        and certificates["pr230_source_higgs_overlap_kappa_contract"].get(
            "current_blockers", {}
        ).get("source_higgs_row_packet_absent")
        is True
        and certificates["pr230_source_higgs_overlap_kappa_contract"].get(
            "forbidden_firewall", {}
        ).get("set_kappa_s_equal_one")
        is False
    )
    radial_spurion_action_contract_support_not_closure = (
        "no-independent-top-source radial-spurion action contract"
        in certificates["pr230_radial_spurion_action_contract"].get(
            "actual_current_surface_status", ""
        )
        and certificates["pr230_radial_spurion_action_contract"].get(
            "proposal_allowed"
        )
        is False
        and certificates["pr230_radial_spurion_action_contract"].get(
            "radial_spurion_action_contract_passed"
        )
        is True
        and certificates["pr230_radial_spurion_action_contract"].get(
            "current_surface_contract_satisfied"
        )
        is False
        and certificates["pr230_radial_spurion_action_contract"].get(
            "accepted_action_certificate_written"
        )
        is False
    )
    additive_source_radial_spurion_incompatibility_support_not_closure = (
        "current additive source is incompatible"
        in certificates["pr230_additive_source_radial_spurion_incompatibility"].get(
            "actual_current_surface_status", ""
        )
        and certificates["pr230_additive_source_radial_spurion_incompatibility"].get(
            "proposal_allowed"
        )
        is False
        and certificates["pr230_additive_source_radial_spurion_incompatibility"].get(
            "additive_source_radial_spurion_incompatibility_passed"
        )
        is True
        and certificates["pr230_additive_source_radial_spurion_incompatibility"].get(
            "forbidden_firewall", {}
        ).get("set_kappa_s_equal_one")
        is False
        and certificates["pr230_additive_source_radial_spurion_incompatibility"].get(
            "forbidden_firewall", {}
        ).get("used_observed_wz_masses_or_g2")
        is False
    )
    additive_top_subtraction_row_contract_support_not_closure = (
        "additive-top subtraction row contract"
        in certificates["pr230_additive_top_subtraction_row_contract"].get(
            "actual_current_surface_status", ""
        )
        and certificates["pr230_additive_top_subtraction_row_contract"].get(
            "proposal_allowed"
        )
        is False
        and certificates["pr230_additive_top_subtraction_row_contract"].get(
            "additive_top_subtraction_row_contract_passed"
        )
        is True
        and certificates["pr230_additive_top_subtraction_row_contract"].get(
            "current_surface_contract_satisfied"
        )
        is False
        and certificates["pr230_additive_top_subtraction_row_contract"].get(
            "subtraction_identity_exact"
        )
        is True
        and certificates["pr230_additive_top_subtraction_row_contract"].get(
            "matched_covariance_delta_method_valid"
        )
        is True
        and (
            certificates["pr230_additive_top_subtraction_row_contract"].get(
                "future_artifact_presence", {}
            ).get("additive_top_jacobian_rows")
            is False
            or certificates["pr230_additive_top_subtraction_row_contract"].get(
                "additive_top_jacobian_row_status", {}
            ).get("strict")
            is False
        )
        and certificates["pr230_additive_top_subtraction_row_contract"].get(
            "future_artifact_presence", {}
        ).get("wz_response_ratio_rows")
        is False
        and certificates["pr230_additive_top_subtraction_row_contract"].get(
            "future_artifact_presence", {}
        ).get("strict_electroweak_g2_certificate")
        is False
    )
    wz_response_ratio_identifiability_contract_support_not_closure = (
        "WZ response-ratio identifiability contract"
        in certificates["pr230_wz_response_ratio_identifiability_contract"].get(
            "actual_current_surface_status", ""
        )
        and certificates["pr230_wz_response_ratio_identifiability_contract"].get(
            "wz_response_ratio_identifiability_contract_passed"
        )
        is True
        and certificates["pr230_wz_response_ratio_identifiability_contract"].get(
            "current_surface_contract_satisfied"
        )
        is False
        and certificates["pr230_wz_response_ratio_identifiability_contract"].get(
            "future_response_ratio_row_packet_present"
        )
        is False
        and certificates["pr230_wz_response_ratio_identifiability_contract"].get(
            "strict_g2_authority_present"
        )
        is False
        and certificates["pr230_wz_response_ratio_identifiability_contract"].get(
            "matched_covariance_authority_present"
        )
        is False
        and certificates["pr230_wz_response_ratio_identifiability_contract"].get(
            "proposal_allowed"
        )
        is False
    )
    wz_same_source_action_minimal_certificate_cut_open = (
        "WZ accepted same-source action minimal certificate cut"
        in certificates["pr230_wz_same_source_action_minimal_certificate_cut"].get(
            "actual_current_surface_status", ""
        )
        and certificates["pr230_wz_same_source_action_minimal_certificate_cut"].get(
            "wz_same_source_action_minimal_certificate_cut_passed"
        )
        is True
        and certificates["pr230_wz_same_source_action_minimal_certificate_cut"].get(
            "proposal_allowed"
        )
        is False
        and certificates["pr230_wz_same_source_action_minimal_certificate_cut"].get(
            "current_surface_action_certificate_satisfied"
        )
        is False
        and set(
            certificates["pr230_wz_same_source_action_minimal_certificate_cut"].get(
                "root_certificate_cut_open", []
            )
        )
        == {
            "same_surface_canonical_higgs_operator_certificate",
            "current_same_source_sector_overlap_identity",
            "wz_correlator_mass_fit_path_certificate",
        }
    )
    wz_accepted_action_response_root_checkpoint_blocks = (
        "WZ accepted-action response root not closed"
        in certificates["pr230_wz_accepted_action_response_root_checkpoint"].get(
            "actual_current_surface_status", ""
        )
        and certificates["pr230_wz_accepted_action_response_root_checkpoint"].get(
            "proposal_allowed"
        )
        is False
        and certificates["pr230_wz_accepted_action_response_root_checkpoint"].get(
            "wz_accepted_action_response_root_checkpoint_passed"
        )
        is True
        and certificates["pr230_wz_accepted_action_response_root_checkpoint"].get(
            "current_route_blocked"
        )
        is True
        and certificates["pr230_wz_accepted_action_response_root_checkpoint"].get(
            "root_closures_found"
        )
        == []
        and not any(
            certificates["pr230_wz_accepted_action_response_root_checkpoint"].get(
                "future_artifact_presence", {}
            ).values()
        )
    )
    canonical_oh_wz_common_action_cut_open = (
        "canonical O_H and WZ accepted-action common-cut"
        in certificates["pr230_canonical_oh_wz_common_action_cut"].get(
            "actual_current_surface_status", ""
        )
        and certificates["pr230_canonical_oh_wz_common_action_cut"].get(
            "proposal_allowed"
        )
        is False
        and certificates["pr230_canonical_oh_wz_common_action_cut"].get(
            "common_action_cut_passed"
        )
        is True
        and certificates["pr230_canonical_oh_wz_common_action_cut"].get(
            "common_canonical_oh_vertex_open"
        )
        is True
        and certificates["pr230_canonical_oh_wz_common_action_cut"].get(
            "aggregate_denies_proposal"
        )
        is True
        and certificates["pr230_canonical_oh_wz_common_action_cut"].get(
            "time_kernel_manifest_not_evidence"
        )
        is True
    )
    canonical_oh_accepted_action_stretch_blocks_current_stack = (
        "canonical O_H accepted-action root not derivable"
        in certificates["pr230_canonical_oh_accepted_action_stretch_attempt"].get(
            "actual_current_surface_status", ""
        )
        and certificates["pr230_canonical_oh_accepted_action_stretch_attempt"].get(
            "proposal_allowed"
        )
        is False
        and certificates["pr230_canonical_oh_accepted_action_stretch_attempt"].get(
            "stretch_attempt_passed"
        )
        is True
        and certificates["pr230_canonical_oh_accepted_action_stretch_attempt"].get(
            "current_route_blocked"
        )
        is True
        and certificates["pr230_canonical_oh_accepted_action_stretch_attempt"].get(
            "root_closures_found"
        )
        == []
    )
    two_source_taste_radial_chunk_checkpoint_not_closure = {}
    for idx in range(1, 11):
        cert_key = f"pr230_two_source_taste_radial_chunk{idx:03d}_checkpoint"
        cert = certificates[cert_key]
        two_source_taste_radial_chunk_checkpoint_not_closure[idx] = (
            f"two-source taste-radial chunk{idx:03d}"
            in cert.get("actual_current_surface_status", "")
            and cert.get("checkpoint_passed") is True
            and cert.get("completed") is True
            and cert.get("proposal_allowed") is False
            and cert.get("chunk_summary", {}).get("pole_residue_rows_count") == 0
        )
    kinetic_taste_mixing_bridge_blocks_shortcut = (
        "current staggered kinetic taste symmetry"
        in certificates["pr230_kinetic_taste_mixing_bridge"].get(
            "actual_current_surface_status", ""
        )
        and certificates["pr230_kinetic_taste_mixing_bridge"].get("proposal_allowed")
        is False
        and certificates["pr230_kinetic_taste_mixing_bridge"].get(
            "kinetic_taste_mixing_bridge_closes_pr230"
        )
        is False
        and certificates["pr230_kinetic_taste_mixing_bridge"].get(
            "exact_negative_boundary_passed"
        )
        is True
    )
    one_higgs_taste_axis_completeness_blocks_shortcut = (
        "one-Higgs taste-axis completeness not derived"
        in certificates["pr230_one_higgs_taste_axis_completeness"].get(
            "actual_current_surface_status", ""
        )
        and certificates["pr230_one_higgs_taste_axis_completeness"].get(
            "proposal_allowed"
        )
        is False
        and certificates["pr230_one_higgs_taste_axis_completeness"].get(
            "one_higgs_taste_axis_completeness_derived"
        )
        is False
        and certificates["pr230_one_higgs_taste_axis_completeness"].get(
            "exact_negative_boundary_passed"
        )
        is True
    )
    action_first_route_completion_blocks = (
        "action-first O_H/C_sH/C_HH route not complete on current PR230 surface"
        in certificates["pr230_action_first_route_completion"].get(
            "actual_current_surface_status", ""
        )
        and certificates["pr230_action_first_route_completion"].get("proposal_allowed")
        is False
        and certificates["pr230_action_first_route_completion"].get(
            "action_first_route_completion_passed"
        )
        is True
    )
    wz_response_route_completion_blocks = (
        "WZ same-source response route not complete on current PR230 surface"
        in certificates["pr230_wz_response_route_completion"].get(
            "actual_current_surface_status", ""
        )
        and certificates["pr230_wz_response_route_completion"].get("proposal_allowed")
        is False
        and certificates["pr230_wz_response_route_completion"].get(
            "wz_response_route_completion_passed"
        )
        is True
    )
    schur_route_completion_blocks = (
        "strict Schur A/B/C route not complete"
        in certificates["pr230_schur_route_completion"].get(
            "actual_current_surface_status", ""
        )
        and certificates["pr230_schur_route_completion"].get("proposal_allowed")
        is False
        and certificates["pr230_schur_route_completion"].get(
            "schur_route_completion_passed"
        )
        is True
    )
    neutral_primitive_route_completion_blocks = (
        "neutral primitive-rank-one route not complete on current PR230 surface"
        in certificates["pr230_neutral_primitive_route_completion"].get(
            "actual_current_surface_status", ""
        )
        and certificates["pr230_neutral_primitive_route_completion"].get(
            "proposal_allowed"
        )
        is False
        and certificates["pr230_neutral_primitive_route_completion"].get(
            "neutral_primitive_route_completion_passed"
        )
        is True
    )
    oh_bridge_candidate_portfolio_open = (
        "first-principles O_H bridge positive-candidate portfolio"
        in certificates["pr230_oh_bridge_candidate_portfolio"].get(
            "actual_current_surface_status", ""
        )
        and certificates["pr230_oh_bridge_candidate_portfolio"].get(
            "proposal_allowed"
        )
        is False
        and certificates["pr230_oh_bridge_candidate_portfolio"].get(
            "candidate_portfolio_passed"
        )
        is True
        and certificates["pr230_oh_bridge_candidate_portfolio"].get(
            "candidate_count"
        )
        == 5
    )
    same_surface_neutral_multiplicity_gate_rejects_current_surface = (
        "same-surface neutral multiplicity-one artifact intake gate"
        in certificates["pr230_same_surface_neutral_multiplicity_one_gate"].get(
            "actual_current_surface_status", ""
        )
        and certificates["pr230_same_surface_neutral_multiplicity_one_gate"].get(
            "proposal_allowed"
        )
        is False
        and certificates["pr230_same_surface_neutral_multiplicity_one_gate"].get(
            "candidate_accepted"
        )
        is False
    )
    os_transfer_kernel_artifact_absent = (
        "OS transfer-kernel artifact absent"
        in certificates["pr230_os_transfer_kernel_artifact_gate"].get(
            "actual_current_surface_status", ""
        )
        and certificates["pr230_os_transfer_kernel_artifact_gate"].get(
            "proposal_allowed"
        )
        is False
        and certificates["pr230_os_transfer_kernel_artifact_gate"].get(
            "os_transfer_kernel_artifact_present"
        )
        is False
        and certificates["pr230_os_transfer_kernel_artifact_gate"].get(
            "same_surface_transfer_or_gevp_present"
        )
        is False
    )
    source_higgs_time_kernel_harness_support_only = (
        "source-Higgs time-kernel harness"
        in certificates["pr230_source_higgs_time_kernel_harness_extension_gate"].get(
            "actual_current_surface_status", ""
        )
        and certificates["pr230_source_higgs_time_kernel_harness_extension_gate"].get(
            "proposal_allowed"
        )
        is False
        and certificates["pr230_source_higgs_time_kernel_harness_extension_gate"].get(
            "contract", {}
        ).get("adds_default_off_time_kernel_rows")
        is True
        and certificates["pr230_source_higgs_time_kernel_harness_extension_gate"].get(
            "contract", {}
        ).get("selected_mass_only")
        is True
        and certificates["pr230_source_higgs_time_kernel_harness_extension_gate"].get(
            "used_as_physical_yukawa_readout"
        )
        is False
    )
    source_higgs_time_kernel_gevp_contract_support_only = (
        "source-Higgs time-kernel GEVP contract"
        in certificates["pr230_source_higgs_time_kernel_gevp_contract"].get(
            "actual_current_surface_status", ""
        )
        and certificates["pr230_source_higgs_time_kernel_gevp_contract"].get(
            "proposal_allowed"
        )
        is False
        and certificates["pr230_source_higgs_time_kernel_gevp_contract"].get(
            "formal_gevp_diagnostic", {}
        ).get("available")
        is True
        and certificates["pr230_source_higgs_time_kernel_gevp_contract"].get(
            "physical_pole_extraction_accepted"
        )
        is False
    )
    source_higgs_time_kernel_production_manifest_not_evidence = (
        "source-Higgs time-kernel production manifest"
        in certificates["pr230_source_higgs_time_kernel_production_manifest"].get(
            "actual_current_surface_status", ""
        )
        and certificates["pr230_source_higgs_time_kernel_production_manifest"].get(
            "proposal_allowed"
        )
        is False
        and certificates["pr230_source_higgs_time_kernel_production_manifest"].get(
            "closure_launch_authorized_now"
        )
        is False
        and certificates["pr230_source_higgs_time_kernel_production_manifest"].get(
            "support_launch_authorized_now"
        )
        is False
        and certificates["pr230_source_higgs_time_kernel_production_manifest"].get(
            "operator_certificate_is_canonical_oh"
        )
        is False
        and certificates["pr230_source_higgs_time_kernel_production_manifest"].get(
            "time_kernel_schema_version"
        )
        == "source_higgs_time_kernel_v1"
        and certificates["pr230_source_higgs_time_kernel_production_manifest"].get(
            "chunk_count"
        )
        == 63
    )
    fms_literature_source_overlap_intake_non_authority = (
        "FMS literature does not supply PR230 source-overlap"
        in certificates["pr230_fms_literature_source_overlap_intake"].get(
            "actual_current_surface_status", ""
        )
        and certificates["pr230_fms_literature_source_overlap_intake"].get(
            "proposal_allowed"
        )
        is False
        and certificates["pr230_fms_literature_source_overlap_intake"].get(
            "literature_bridge_scope"
        )
        == "non_derivation_context_only"
        and certificates["pr230_fms_literature_source_overlap_intake"].get(
            "current_blockers", {}
        ).get("canonical_oh_absent")
        is True
        and certificates["pr230_fms_literature_source_overlap_intake"].get(
            "current_blockers", {}
        ).get("source_higgs_rows_absent")
        is True
    )
    schur_higher_shell_production_contract_not_evidence = (
        "higher-shell Schur scalar-LSZ production contract"
        in certificates["pr230_schur_higher_shell_production_contract"].get(
            "actual_current_surface_status", ""
        )
        and certificates["pr230_schur_higher_shell_production_contract"].get(
            "proposal_allowed"
        )
        is False
        and certificates["pr230_schur_higher_shell_production_contract"].get(
            "higher_shell_schur_production_contract_passed"
        )
        is True
        and certificates["pr230_schur_higher_shell_production_contract"].get(
            "rows_written_by_contract"
        )
        is False
        and certificates["pr230_schur_higher_shell_production_contract"].get(
            "current_four_mode_campaign_must_remain_unmixed"
        )
        is True
    )
    derived_bridge_rank_one_closure_attempt_blocks = (
        "derived rank-one bridge not closed"
        in certificates["pr230_derived_bridge_rank_one_closure_attempt"].get(
            "actual_current_surface_status", ""
        )
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
        is True
    )
    source_sector_pattern_transfer_gate_not_closure = (
        "source-sector pattern is relevant"
        in certificates["pr230_source_sector_pattern_transfer_gate"].get(
            "actual_current_surface_status", ""
        )
        and certificates["pr230_source_sector_pattern_transfer_gate"].get(
            "proposal_allowed"
        )
        is False
        and certificates["pr230_source_sector_pattern_transfer_gate"].get(
            "bounded_support_passed"
        )
        is True
        and certificates["pr230_source_sector_pattern_transfer_gate"].get(
            "direct_closure_available"
        )
        is False
    )
    det_positivity_bridge_intake_gate_not_closure = (
        "determinant positivity is useful"
        in certificates["pr230_det_positivity_bridge_intake_gate"].get(
            "actual_current_surface_status", ""
        )
        and certificates["pr230_det_positivity_bridge_intake_gate"].get(
            "proposal_allowed"
        )
        is False
        and certificates["pr230_det_positivity_bridge_intake_gate"].get(
            "intake_gate_passed"
        )
        is True
        and certificates["pr230_det_positivity_bridge_intake_gate"].get(
            "determinant_bridge_closes_pr230"
        )
        is False
    )
    reflection_det_primitive_upgrade_gate_blocks = (
        "reflection plus determinant positivity"
        in certificates["pr230_reflection_det_primitive_upgrade_gate"].get(
            "actual_current_surface_status", ""
        )
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
        is True
    )
    complete_source_spectrum_identity_no_go_blocks = (
        "complete source spectrum not canonical-Higgs closure"
        in certificates["complete_source_spectrum_identity_no_go"].get("actual_current_surface_status", "")
        and certificates["complete_source_spectrum_identity_no_go"].get("proposal_allowed") is False
        and certificates["complete_source_spectrum_identity_no_go"]
        .get("witness_family", {})
        .get("checks", {})
        .get("source_spectrum_identical_across_rows")
        is True
        and certificates["complete_source_spectrum_identity_no_go"]
        .get("witness_family", {})
        .get("checks", {})
        .get("same_source_top_response_identical")
        is True
        and float(
            certificates["complete_source_spectrum_identity_no_go"]
            .get("witness_family", {})
            .get("checks", {})
            .get("canonical_higgs_y_span_factor", 0.0)
        )
        > 4.0
    )
    neutral_scalar_top_coupling_tomography_gate_blocks = (
        "neutral scalar top-coupling tomography gate not passed"
        in certificates["neutral_scalar_top_coupling_tomography_gate"].get("actual_current_surface_status", "")
        and certificates["neutral_scalar_top_coupling_tomography_gate"].get("proposal_allowed") is False
        and certificates["neutral_scalar_top_coupling_tomography_gate"].get("gate_passed") is False
        and certificates["neutral_scalar_top_coupling_tomography_gate"]
        .get("tomography_witness", {})
        .get("checks", {})
        .get("current_rank_insufficient")
        is True
    )
    non_source_response_rank_repair_sufficiency_not_closure = (
        "non-source response rank-repair sufficiency theorem"
        in certificates["non_source_response_rank_repair_sufficiency"].get(
            "actual_current_surface_status", ""
        )
        and certificates["non_source_response_rank_repair_sufficiency"].get("proposal_allowed") is False
        and certificates["non_source_response_rank_repair_sufficiency"].get(
            "rank_repair_sufficiency_theorem_passed"
        )
        is True
        and certificates["non_source_response_rank_repair_sufficiency"].get(
            "current_closure_gate_passed"
        )
        is False
    )
    positivity_improving_neutral_scalar_rank_one_conditional = (
        "positivity-improving neutral-scalar rank-one theorem"
        in certificates["positivity_improving_neutral_scalar_rank_one"].get(
            "actual_current_surface_status", ""
        )
        and certificates["positivity_improving_neutral_scalar_rank_one"].get("proposal_allowed") is False
        and certificates["positivity_improving_neutral_scalar_rank_one"].get(
            "positivity_improving_rank_one_theorem_passed"
        )
        is True
        and certificates["positivity_improving_neutral_scalar_rank_one"].get(
            "positivity_improving_certificate_present"
        )
        is False
        and certificates["positivity_improving_neutral_scalar_rank_one"].get(
            "current_closure_gate_passed"
        )
        is False
    )
    gauge_perron_neutral_scalar_import_blocks = (
        "gauge-vacuum Perron theorem does not certify neutral-scalar rank-one purity"
        in certificates["gauge_perron_neutral_scalar_rank_one_import"].get(
            "actual_current_surface_status", ""
        )
        and certificates["gauge_perron_neutral_scalar_rank_one_import"].get("proposal_allowed") is False
        and certificates["gauge_perron_neutral_scalar_rank_one_import"].get(
            "exact_negative_boundary_passed"
        )
        is True
        and certificates["gauge_perron_neutral_scalar_rank_one_import"].get(
            "gauge_perron_import_closes_neutral_rank_one"
        )
        is False
    )
    neutral_scalar_positivity_improving_direct_blocks = (
        "neutral-scalar positivity-improving direct theorem not derived"
        in certificates["neutral_scalar_positivity_improving_direct_closure"].get(
            "actual_current_surface_status", ""
        )
        and certificates["neutral_scalar_positivity_improving_direct_closure"].get("proposal_allowed") is False
        and certificates["neutral_scalar_positivity_improving_direct_closure"].get(
            "direct_positivity_improving_theorem_derived"
        )
        is False
        and certificates["neutral_scalar_positivity_improving_direct_closure"].get(
            "exact_negative_boundary_passed"
        )
        is True
    )
    neutral_scalar_irreducibility_authority_absent = (
        "neutral-scalar irreducibility authority absent"
        in certificates["neutral_scalar_irreducibility_authority_audit"].get(
            "actual_current_surface_status", ""
        )
        and certificates["neutral_scalar_irreducibility_authority_audit"].get("proposal_allowed") is False
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
        is False
    )
    neutral_scalar_primitive_cone_certificate_absent = (
        "neutral-scalar primitive-cone certificate gate"
        in certificates["neutral_scalar_primitive_cone_certificate_gate"].get(
            "actual_current_surface_status", ""
        )
        and certificates["neutral_scalar_primitive_cone_certificate_gate"].get("proposal_allowed")
        is False
        and certificates["neutral_scalar_primitive_cone_certificate_gate"].get(
            "primitive_cone_certificate_gate_passed"
        )
        is False
    )
    neutral_scalar_primitive_cone_stretch_blocks = (
        "neutral-scalar primitive-cone stretch no-go"
        in certificates["neutral_scalar_primitive_cone_stretch_no_go"].get(
            "actual_current_surface_status", ""
        )
        and certificates["neutral_scalar_primitive_cone_stretch_no_go"].get("proposal_allowed")
        is False
        and certificates["neutral_scalar_primitive_cone_stretch_no_go"].get(
            "primitive_cone_stretch_no_go_passed"
        )
        is True
    )
    neutral_scalar_burnside_irreducibility_blocks = (
        "Burnside neutral irreducibility attempt"
        in certificates["neutral_scalar_burnside_irreducibility_attempt"].get(
            "actual_current_surface_status", ""
        )
        and certificates["neutral_scalar_burnside_irreducibility_attempt"].get("proposal_allowed")
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
        is True
    )
    neutral_offdiagonal_generator_derivation_blocks = (
        "neutral off-diagonal generator not derivable"
        in certificates["neutral_offdiagonal_generator_derivation_attempt"].get(
            "actual_current_surface_status", ""
        )
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
        is True
    )
    logdet_hessian_neutral_mixing_blocks = (
        "source-only staggered logdet Hessian does not derive"
        in certificates["pr230_logdet_hessian_neutral_mixing_attempt"].get(
            "actual_current_surface_status", ""
        )
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
        is False
    )
    scalar_carrier_projector_closure_blocked = (
        "scalar carrier-projector closure attempt blocked"
        in certificates["scalar_carrier_projector_closure"].get("actual_current_surface_status", "")
        and certificates["scalar_carrier_projector_closure"].get("proposal_allowed") is False
        and certificates["scalar_carrier_projector_closure"].get("theorem_closed") is False
    )
    kprime_closure_blocked = (
        "K-prime closure attempt blocked"
        in certificates["kprime_closure"].get("actual_current_surface_status", "")
        and certificates["kprime_closure"].get("proposal_allowed") is False
        and certificates["kprime_closure"].get("kprime_closed") is False
    )
    matching_running_bridge_gate_open = (
        "matching-running bridge awaits certified physical input"
        in certificates["pr230_matching_running_bridge_gate"].get("actual_current_surface_status", "")
        and certificates["pr230_matching_running_bridge_gate"].get("proposal_allowed") is False
        and certificates["pr230_matching_running_bridge_gate"].get("matching_running_bridge_passed") is False
    )
    schur_complement_kprime_sufficiency_not_closure = (
        "Schur-complement K-prime sufficiency theorem"
        in certificates["schur_complement_kprime_sufficiency"].get("actual_current_surface_status", "")
        and certificates["schur_complement_kprime_sufficiency"].get("proposal_allowed") is False
        and certificates["schur_complement_kprime_sufficiency"].get("schur_sufficiency_theorem_passed") is True
        and certificates["schur_complement_kprime_sufficiency"].get("current_closure_gate_passed") is False
    )
    schur_kprime_row_absence_guard_blocks_source_only_import = (
        "Schur K-prime row absence guard"
        in certificates["schur_kprime_row_absence_guard"].get("actual_current_surface_status", "")
        and certificates["schur_kprime_row_absence_guard"].get("proposal_allowed") is False
        and certificates["schur_kprime_row_absence_guard"].get("schur_kprime_row_absence_guard_passed") is True
        and certificates["schur_kprime_row_absence_guard"].get("current_schur_kernel_rows_present") is False
        and certificates["schur_kprime_row_absence_guard"].get("finite_source_only_counterfamily_passed") is True
    )
    legacy_schur_bridge_import_audit_blocks_hidden_closure = (
        "legacy Schur bridge stack is not PR230 y_t closure"
        in certificates["legacy_schur_bridge_import_audit"].get("actual_current_surface_status", "")
        and certificates["legacy_schur_bridge_import_audit"].get("proposal_allowed") is False
        and certificates["legacy_schur_bridge_import_audit"].get("legacy_schur_import_closes_pr230") is False
        and certificates["legacy_schur_bridge_import_audit"].get("exact_negative_boundary_passed") is True
    )
    schur_kernel_row_contract_gate_not_passed = (
        "Schur kernel row contract gate not passed"
        in certificates["schur_kernel_row_contract_gate"].get("actual_current_surface_status", "")
        and certificates["schur_kernel_row_contract_gate"].get("proposal_allowed") is False
        and certificates["schur_kernel_row_contract_gate"].get("schur_kernel_row_contract_gate_passed") is False
        and certificates["schur_kernel_row_contract_gate"].get("current_closure_gate_passed") is False
    )
    schur_row_candidate_extraction_blocks_finite_support_import = (
        "Schur row candidate extraction"
        in certificates["schur_row_candidate_extraction_attempt"].get("actual_current_surface_status", "")
        and certificates["schur_row_candidate_extraction_attempt"].get("proposal_allowed") is False
        and certificates["schur_row_candidate_extraction_attempt"].get("candidate_extraction_closes_pr230")
        is False
        and certificates["schur_row_candidate_extraction_attempt"].get("finite_ladder_candidate_usable")
        is False
        and certificates["schur_row_candidate_extraction_attempt"].get("candidate_rows_written") is False
        and certificates["schur_row_candidate_extraction_attempt"].get("exact_negative_boundary_passed")
        is True
    )
    schur_compressed_denominator_bootstrap_blocks_hidden_rows = (
        "Schur compressed-denominator row-bootstrap no-go"
        in certificates["schur_compressed_denominator_row_bootstrap_no_go"].get(
            "actual_current_surface_status", ""
        )
        and certificates["schur_compressed_denominator_row_bootstrap_no_go"].get("proposal_allowed")
        is False
        and certificates["schur_compressed_denominator_row_bootstrap_no_go"].get(
            "bootstrap_no_go_passed"
        )
        is True
    )
    schur_abc_definition_derivation_blocks_current_surface = (
        "Schur A/B/C definition not derivable"
        in certificates["pr230_schur_abc_definition_derivation_attempt"].get(
            "actual_current_surface_status", ""
        )
        and certificates["pr230_schur_abc_definition_derivation_attempt"].get("proposal_allowed")
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
        is True
    )
    higgs_pole_identity_gate_blocks = (
        "canonical-Higgs pole identity gate blocking"
        in certificates["fh_lsz_higgs_pole_identity"].get("actual_current_surface_status", "")
        and certificates["fh_lsz_higgs_pole_identity"].get("proposal_allowed") is False
        and certificates["fh_lsz_higgs_pole_identity"].get("higgs_pole_identity_gate_passed") is False
    )
    gauge_normalized_response_not_closure = (
        "FH gauge-normalized response route"
        in certificates["fh_gauge_normalized_response"].get("actual_current_surface_status", "")
        and certificates["fh_gauge_normalized_response"].get("proposal_allowed") is False
        and certificates["fh_gauge_normalized_response"].get("gauge_normalized_response_gate_passed") is False
    )
    gauge_mass_response_observable_gap_blocks = (
        "FH gauge-mass response observable gap"
        in certificates["fh_gauge_mass_response_observable_gap"].get("actual_current_surface_status", "")
        and certificates["fh_gauge_mass_response_observable_gap"].get("proposal_allowed") is False
        and certificates["fh_gauge_mass_response_observable_gap"].get("gauge_mass_response_observable_ready") is False
    )
    gauge_mass_response_manifest_not_evidence = (
        "same-source WZ gauge-mass response manifest"
        in certificates["fh_gauge_mass_response_manifest"].get("actual_current_surface_status", "")
        and certificates["fh_gauge_mass_response_manifest"].get("proposal_allowed") is False
        and certificates["fh_gauge_mass_response_manifest"].get("manifest_is_evidence") is False
    )
    gauge_mass_response_builder_rows_absent = (
        "same-source WZ response rows absent"
        in certificates["fh_gauge_mass_response_certificate_builder"].get("actual_current_surface_status", "")
        and certificates["fh_gauge_mass_response_certificate_builder"].get("proposal_allowed") is False
        and certificates["fh_gauge_mass_response_certificate_builder"].get("input_present") is False
    )
    same_source_wz_response_certificate_gate_blocks = (
        "same-source WZ response certificate gate not passed"
        in certificates["same_source_wz_response_certificate_gate"].get("actual_current_surface_status", "")
        and certificates["same_source_wz_response_certificate_gate"].get("proposal_allowed") is False
        and certificates["same_source_wz_response_certificate_gate"].get(
            "same_source_wz_response_certificate_gate_passed"
        )
        is False
    )
    wz_response_harness_absence_guard_not_evidence = (
        "WZ response harness absence guard"
        in certificates["wz_response_harness_absence_guard"].get("actual_current_surface_status", "")
        and certificates["wz_response_harness_absence_guard"].get("proposal_allowed") is False
        and certificates["wz_response_harness_absence_guard"].get("guard_fields", {}).get("wz_mass_response")
        is True
        and certificates["wz_response_harness_absence_guard"].get("guard_fields", {}).get("enabled_false") is True
    )
    wz_response_repo_harness_import_audit_blocks_hidden_harness = (
        "repo-wide WZ response harness import audit"
        in certificates["wz_response_repo_harness_import_audit"].get(
            "actual_current_surface_status", ""
        )
        and certificates["wz_response_repo_harness_import_audit"].get("proposal_allowed")
        is False
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
        is True
    )
    wz_response_measurement_row_contract_not_evidence = (
        "WZ response measurement-row contract gate"
        in certificates["wz_response_measurement_row_contract_gate"].get(
            "actual_current_surface_status", ""
        )
        and certificates["wz_response_measurement_row_contract_gate"].get("proposal_allowed") is False
        and certificates["wz_response_measurement_row_contract_gate"].get(
            "wz_measurement_row_contract_gate_passed"
        )
        is False
    )
    wz_response_row_production_attempt_blocks_current_surface = (
        "WZ response row production attempt on current surface"
        in certificates["wz_response_row_production_attempt"].get(
            "actual_current_surface_status", ""
        )
        and certificates["wz_response_row_production_attempt"].get("proposal_allowed") is False
        and certificates["wz_response_row_production_attempt"].get(
            "production_attempt_closes_pr230"
        )
        is False
        and certificates["wz_response_row_production_attempt"].get("measurement_rows_written")
        is False
    )
    wz_response_harness_implementation_plan_support_only = (
        "WZ response harness implementation plan"
        in certificates["wz_response_harness_implementation_plan"].get(
            "actual_current_surface_status", ""
        )
        and certificates["wz_response_harness_implementation_plan"].get("proposal_allowed") is False
        and certificates["wz_response_harness_implementation_plan"].get("future_rows_written") is False
        and len(
            certificates["wz_response_harness_implementation_plan"].get(
                "implementation_work_units", []
            )
        )
        == 5
    )
    wz_harness_smoke_schema_support_only = (
        "WZ harness smoke schema path"
        in certificates["wz_harness_smoke_schema"].get("actual_current_surface_status", "")
        and certificates["wz_harness_smoke_schema"].get("proposal_allowed") is False
        and certificates["wz_harness_smoke_schema"].get("wz_harness_smoke_schema_gate_passed") is True
    )
    wz_smoke_to_production_promotion_no_go_blocks = (
        "WZ smoke rows cannot be promoted"
        in certificates["wz_smoke_to_production_promotion_no_go"].get(
            "actual_current_surface_status", ""
        )
        and certificates["wz_smoke_to_production_promotion_no_go"].get("proposal_allowed") is False
        and certificates["wz_smoke_to_production_promotion_no_go"].get(
            "wz_smoke_to_production_promotion_no_go_passed"
        )
        is True
    )
    wz_same_source_ew_action_certificate_builder_blocks = (
        "same-source EW action certificate absent"
        in certificates["wz_same_source_ew_action_certificate_builder"].get(
            "actual_current_surface_status", ""
        )
        and certificates["wz_same_source_ew_action_certificate_builder"].get("proposal_allowed") is False
        and certificates["wz_same_source_ew_action_certificate_builder"].get("input_present") is False
        and certificates["wz_same_source_ew_action_certificate_builder"].get(
            "same_source_ew_action_certificate_valid"
        )
        is False
    )
    wz_same_source_ew_action_gate_blocks = (
        "same-source EW action not defined"
        in certificates["wz_same_source_ew_action_gate"].get(
            "actual_current_surface_status", ""
        )
        and certificates["wz_same_source_ew_action_gate"].get("proposal_allowed") is False
        and certificates["wz_same_source_ew_action_gate"].get("same_source_ew_action_ready") is False
        and certificates["wz_same_source_ew_action_gate"].get("action_block_written") is False
    )
    wz_same_source_ew_action_semantic_firewall_not_closure = (
        "same-source EW action semantic firewall passed"
        in certificates["wz_same_source_ew_action_semantic_firewall"].get(
            "actual_current_surface_status", ""
        )
        and certificates["wz_same_source_ew_action_semantic_firewall"].get("proposal_allowed") is False
    )
    wz_source_coordinate_transport_no_go_blocks = (
        "WZ source-coordinate transport shortcut rejected"
        in certificates["wz_source_coordinate_transport_no_go"].get(
            "actual_current_surface_status", ""
        )
        and certificates["wz_source_coordinate_transport_no_go"].get("proposal_allowed") is False
        and certificates["wz_source_coordinate_transport_no_go"].get(
            "wz_source_coordinate_transport_no_go_passed"
        )
        is True
        and certificates["wz_source_coordinate_transport_no_go"].get(
            "future_transport_certificate_present"
        )
        is False
        and certificates["wz_source_coordinate_transport_no_go"].get("future_wz_rows_present")
        is False
    )
    wz_goldstone_equivalence_source_identity_no_go_blocks = (
        "Goldstone equivalence does not identify PR230 source coordinate"
        in certificates["wz_goldstone_equivalence_source_identity_no_go"].get(
            "actual_current_surface_status", ""
        )
        and certificates["wz_goldstone_equivalence_source_identity_no_go"].get("proposal_allowed")
        is False
        and certificates["wz_goldstone_equivalence_source_identity_no_go"].get(
            "goldstone_equivalence_source_identity_no_go_passed"
        )
        is True
    )
    same_source_w_response_decomposition_not_closure = (
        "same-source W-response decomposition theorem"
        in certificates["same_source_w_response_decomposition"].get(
            "actual_current_surface_status", ""
        )
        and certificates["same_source_w_response_decomposition"].get("proposal_allowed") is False
        and certificates["same_source_w_response_decomposition"].get(
            "same_source_w_response_decomposition_theorem_passed"
        )
        is True
        and certificates["same_source_w_response_decomposition"].get("current_closure_gate_passed") is False
    )
    same_source_w_response_orthogonal_correction_gate_blocks = (
        "same-source W-response orthogonal-correction gate not passed"
        in certificates["same_source_w_response_orthogonal_correction"].get(
            "actual_current_surface_status", ""
        )
        and certificates["same_source_w_response_orthogonal_correction"].get("proposal_allowed") is False
        and certificates["same_source_w_response_orthogonal_correction"].get(
            "orthogonal_correction_theorem_passed"
        )
        is True
        and certificates["same_source_w_response_orthogonal_correction"].get(
            "orthogonal_correction_gate_passed"
        )
        is False
    )
    one_higgs_completeness_orthogonal_null_premise_absent = (
        "one-Higgs completeness orthogonal-null theorem"
        in certificates["one_higgs_completeness_orthogonal_null"].get(
            "actual_current_surface_status", ""
        )
        and certificates["one_higgs_completeness_orthogonal_null"].get("proposal_allowed") is False
        and certificates["one_higgs_completeness_orthogonal_null"].get(
            "one_higgs_completeness_orthogonal_null_theorem_passed"
        )
        is True
        and certificates["one_higgs_completeness_orthogonal_null"].get(
            "one_higgs_completeness_gate_passed"
        )
        is False
    )
    same_source_w_response_lightweight_readout_open = (
        "lightweight same-source W-response readout"
        in certificates["same_source_w_response_lightweight_readout"].get(
            "actual_current_surface_status", ""
        )
        and certificates["same_source_w_response_lightweight_readout"].get("proposal_allowed") is False
        and certificates["same_source_w_response_lightweight_readout"].get(
            "strict_lightweight_readout_gate_passed"
        )
        is False
    )
    delta_perp_tomography_correction_builder_open = (
        "delta_perp tomography correction"
        in certificates["delta_perp_tomography_correction_builder"].get(
            "actual_current_surface_status", ""
        )
        and certificates["delta_perp_tomography_correction_builder"].get("proposal_allowed") is False
        and certificates["delta_perp_tomography_correction_builder"].get(
            "strict_delta_perp_tomography_gate_passed"
        )
        is False
    )
    same_source_w_response_row_builder_open = (
        "same-source W-response row builder"
        in certificates["same_source_w_response_row_builder"].get(
            "actual_current_surface_status", ""
        )
        and certificates["same_source_w_response_row_builder"].get("proposal_allowed") is False
        and certificates["same_source_w_response_row_builder"].get(
            "strict_same_source_w_response_row_builder_passed"
        )
        is False
    )
    same_source_top_response_builder_open = (
        "same-source top-response"
        in certificates["same_source_top_response_builder"].get(
            "actual_current_surface_status", ""
        )
        and certificates["same_source_top_response_builder"].get("proposal_allowed") is False
        and certificates["same_source_top_response_builder"].get(
            "strict_same_source_top_response_certificate_builder_passed"
        )
        is False
    )
    same_source_top_response_identity_builder_open = (
        "same-source top-response identity"
        in certificates["same_source_top_response_identity_builder"].get(
            "actual_current_surface_status", ""
        )
        and certificates["same_source_top_response_identity_builder"].get("proposal_allowed")
        is False
        and certificates["same_source_top_response_identity_builder"].get(
            "strict_same_source_top_response_identity_builder_passed"
        )
        is False
    )
    top_wz_matched_covariance_builder_open = (
        "matched top-W"
        in certificates["top_wz_matched_covariance_builder"].get(
            "actual_current_surface_status", ""
        )
        and certificates["top_wz_matched_covariance_builder"].get("proposal_allowed") is False
        and certificates["top_wz_matched_covariance_builder"].get(
            "strict_top_wz_matched_covariance_builder_passed"
        )
        is False
    )
    top_wz_covariance_marginal_derivation_no_go_blocks = (
        "matched top-W covariance not derivable from marginal response support"
        in certificates["top_wz_covariance_marginal_derivation_no_go"].get(
            "actual_current_surface_status", ""
        )
        and certificates["top_wz_covariance_marginal_derivation_no_go"].get("proposal_allowed")
        is False
        and certificates["top_wz_covariance_marginal_derivation_no_go"].get(
            "marginal_derivation_no_go_passed"
        )
        is True
    )
    top_wz_factorization_independence_gate_blocks = (
        "same-source top-W factorization not derived"
        in certificates["top_wz_factorization_independence_gate"].get(
            "actual_current_surface_status", ""
        )
        and certificates["top_wz_factorization_independence_gate"].get("proposal_allowed")
        is False
        and certificates["top_wz_factorization_independence_gate"].get(
            "strict_factorization_independence_gate_passed"
        )
        is False
    )
    top_wz_deterministic_response_covariance_gate_blocks = (
        "deterministic W response covariance shortcut not derived"
        in certificates["top_wz_deterministic_response_covariance_gate"].get(
            "actual_current_surface_status", ""
        )
        and certificates["top_wz_deterministic_response_covariance_gate"].get("proposal_allowed")
        is False
        and certificates["top_wz_deterministic_response_covariance_gate"].get(
            "strict_deterministic_response_covariance_gate_passed"
        )
        is False
    )
    top_wz_covariance_theorem_import_audit_blocks = (
        "no importable same-surface top-W covariance theorem"
        in certificates["top_wz_covariance_theorem_import_audit"].get(
            "actual_current_surface_status", ""
        )
        and certificates["top_wz_covariance_theorem_import_audit"].get("proposal_allowed")
        is False
        and certificates["top_wz_covariance_theorem_import_audit"].get(
            "covariance_theorem_import_audit_passed"
        )
        is True
    )
    wz_correlator_mass_fit_path_gate_blocks = (
        "WZ correlator mass-fit path absent"
        in certificates["wz_correlator_mass_fit_path_gate"].get(
            "actual_current_surface_status", ""
        )
        and certificates["wz_correlator_mass_fit_path_gate"].get("proposal_allowed") is False
        and certificates["wz_correlator_mass_fit_path_gate"].get(
            "wz_correlator_mass_fit_path_ready"
        )
        is False
        and certificates["wz_correlator_mass_fit_path_gate"].get("future_mass_fit_rows_present")
        is False
        and certificates["wz_correlator_mass_fit_path_gate"].get("future_response_rows_present")
        is False
    )
    wz_mass_fit_response_row_builder_open = (
        "WZ mass-fit response-row builder"
        in certificates["wz_mass_fit_response_row_builder"].get(
            "actual_current_surface_status", ""
        )
        and certificates["wz_mass_fit_response_row_builder"].get("proposal_allowed") is False
        and certificates["wz_mass_fit_response_row_builder"].get(
            "strict_wz_mass_fit_response_row_builder_passed"
        )
        is False
    )
    electroweak_g2_certificate_builder_open = (
        "electroweak g2 certificate builder inputs absent"
        in certificates["electroweak_g2_certificate_builder"].get(
            "actual_current_surface_status", ""
        )
        and certificates["electroweak_g2_certificate_builder"].get("proposal_allowed")
        is False
        and certificates["electroweak_g2_certificate_builder"].get(
            "strict_electroweak_g2_certificate_passed"
        )
        is False
    )
    wz_g2_generator_casimir_normalization_no_go_blocks = (
        "generator-Casimir normalization does not certify PR230 g2"
        in certificates["wz_g2_generator_casimir_normalization_no_go"].get(
            "actual_current_surface_status", ""
        )
        and certificates["wz_g2_generator_casimir_normalization_no_go"].get(
            "proposal_allowed"
        )
        is False
        and certificates["wz_g2_generator_casimir_normalization_no_go"].get(
            "g2_generator_casimir_no_go_passed"
        )
        is True
    )
    wz_g2_authority_firewall_blocks = (
        "WZ response g2 authority absent"
        in certificates["wz_g2_authority_firewall"].get("actual_current_surface_status", "")
        and certificates["wz_g2_authority_firewall"].get("proposal_allowed") is False
        and certificates["wz_g2_authority_firewall"].get("g2_authority_gate_passed") is False
    )
    wz_g2_response_self_normalization_no_go_blocks = (
        "WZ response-only g2 self-normalization no-go"
        in certificates["wz_g2_response_self_normalization_no_go"].get(
            "actual_current_surface_status", ""
        )
        and certificates["wz_g2_response_self_normalization_no_go"].get("proposal_allowed")
        is False
        and certificates["wz_g2_response_self_normalization_no_go"].get(
            "g2_response_self_normalization_no_go_passed"
        )
        is True
    )
    wz_g2_bare_running_bridge_attempt_blocks = (
        "WZ g2 bare-to-low-scale running bridge"
        in certificates["pr230_wz_g2_bare_running_bridge_attempt"].get(
            "actual_current_surface_status", ""
        )
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
        is True
    )
    same_source_sector_overlap_identity_blocks = (
        "same-source sector-overlap identity obstruction"
        in certificates["same_source_sector_overlap_identity"].get("actual_current_surface_status", "")
        and certificates["same_source_sector_overlap_identity"].get("proposal_allowed") is False
        and certificates["same_source_sector_overlap_identity"].get("sector_overlap_identity_gate_passed") is False
    )
    source_pole_canonical_higgs_mixing_blocks = (
        "source-pole canonical-Higgs mixing obstruction"
        in certificates["source_pole_canonical_higgs_mixing"].get("actual_current_surface_status", "")
        and certificates["source_pole_canonical_higgs_mixing"].get("proposal_allowed") is False
        and certificates["source_pole_canonical_higgs_mixing"].get("source_pole_canonical_identity_gate_passed")
        is False
    )
    osp_oh_identity_stretch_blocks = (
        "O_sp-to-O_H identity not derived"
        in certificates["osp_oh_identity_stretch"].get("actual_current_surface_status", "")
        and certificates["osp_oh_identity_stretch"].get("proposal_allowed") is False
        and certificates["osp_oh_identity_stretch"].get("identity_derived") is False
    )
    source_pole_purity_cross_correlator_gate_blocks = (
        "source-pole purity cross-correlator gate not passed"
        in certificates["source_pole_purity_cross_correlator"].get("actual_current_surface_status", "")
        and certificates["source_pole_purity_cross_correlator"].get("proposal_allowed") is False
        and certificates["source_pole_purity_cross_correlator"].get("source_pole_purity_gate_passed")
        is False
    )
    source_higgs_cross_correlator_manifest_not_evidence = (
        "source-Higgs cross-correlator production manifest"
        in certificates["source_higgs_cross_correlator_manifest"].get("actual_current_surface_status", "")
        and certificates["source_higgs_cross_correlator_manifest"].get("proposal_allowed") is False
        and certificates["source_higgs_cross_correlator_manifest"].get("manifest_is_evidence") is False
    )
    source_higgs_cross_correlator_import_blocks = (
        "source-Higgs cross-correlator import audit"
        in certificates["source_higgs_cross_correlator_import"].get("actual_current_surface_status", "")
        and certificates["source_higgs_cross_correlator_import"].get("proposal_allowed") is False
        and certificates["source_higgs_cross_correlator_import"].get(
            "source_higgs_cross_correlator_authority_found"
        )
        is False
    )
    source_higgs_gram_purity_gate_blocks = (
        "source-Higgs Gram purity gate not passed"
        in certificates["source_higgs_gram_purity_gate"].get("actual_current_surface_status", "")
        and certificates["source_higgs_gram_purity_gate"].get("proposal_allowed") is False
        and certificates["source_higgs_gram_purity_gate"].get("source_higgs_gram_purity_gate_passed")
        is False
    )
    source_higgs_harness_extension_not_evidence = (
        "source-Higgs cross-correlator harness extension"
        in certificates["source_higgs_cross_correlator_harness_extension"].get("actual_current_surface_status", "")
        and certificates["source_higgs_cross_correlator_harness_extension"].get("proposal_allowed") is False
    )
    source_higgs_pole_residue_extractor_not_evidence = (
        "source-Higgs pole-residue extractor"
        in certificates["source_higgs_pole_residue_extractor"].get("actual_current_surface_status", "")
        and certificates["source_higgs_pole_residue_extractor"].get("proposal_allowed") is False
        and certificates["source_higgs_pole_residue_extractor"].get("rows_written") is False
        and certificates["source_higgs_pole_residue_extractor"].get("gate_passed") is False
    )
    source_higgs_builder_rows_absent = (
        "source-Higgs cross-correlator rows absent"
        in certificates["source_higgs_cross_correlator_certificate_builder"].get("actual_current_surface_status", "")
        and certificates["source_higgs_cross_correlator_certificate_builder"].get("proposal_allowed") is False
        and certificates["source_higgs_cross_correlator_certificate_builder"].get("input_present") is False
        and certificates["source_higgs_cross_correlator_certificate_builder"].get("source_pole_operator_available") is True
    )
    source_higgs_osp_postprocessor_waits = (
        "O_sp-Higgs Gram-purity postprocess awaiting production certificate"
        in certificates["source_higgs_gram_purity_postprocessor"].get("actual_current_surface_status", "")
        and certificates["source_higgs_gram_purity_postprocessor"].get("proposal_allowed") is False
        and certificates["source_higgs_gram_purity_postprocessor"].get("osp_higgs_gram_purity_gate_passed") is False
    )
    source_higgs_gram_purity_contract_witness_not_evidence = (
        "source-Higgs Gram-purity contract witness"
        in certificates["source_higgs_gram_purity_contract_witness"].get("actual_current_surface_status", "")
        and certificates["source_higgs_gram_purity_contract_witness"].get("proposal_allowed") is False
        and certificates["source_higgs_gram_purity_contract_witness"].get("contract_witness_passed") is True
    )
    source_higgs_production_readiness_blocks_launch = (
        "source-Higgs production launch blocked"
        in certificates["source_higgs_production_readiness_gate"].get("actual_current_surface_status", "")
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
        is True
    )
    canonical_higgs_operator_semantic_firewall_not_closure = (
        "canonical-Higgs operator semantic firewall passed"
        in certificates["canonical_higgs_operator_semantic_firewall"].get("actual_current_surface_status", "")
        and certificates["canonical_higgs_operator_semantic_firewall"].get("proposal_allowed") is False
    )
    canonical_higgs_operator_realization_gate_blocks = (
        "canonical-Higgs operator realization gate not passed"
        in certificates["canonical_higgs_operator_realization_gate"].get("actual_current_surface_status", "")
        and certificates["canonical_higgs_operator_realization_gate"].get("proposal_allowed") is False
        and certificates["canonical_higgs_operator_realization_gate"].get(
            "canonical_higgs_operator_realization_gate_passed"
        )
        is False
    )
    canonical_higgs_operator_certificate_gate_blocks = (
        "canonical-Higgs operator certificate absent"
        in certificates["canonical_higgs_operator_certificate_gate"].get("actual_current_surface_status", "")
        and certificates["canonical_higgs_operator_certificate_gate"].get("proposal_allowed") is False
        and certificates["canonical_higgs_operator_certificate_gate"].get("candidate_present") is False
        and certificates["canonical_higgs_operator_certificate_gate"].get("candidate_valid") is False
    )
    canonical_higgs_repo_authority_audit_blocks_hidden_oh = (
        "repo-wide canonical-Higgs O_H authority audit"
        in certificates["canonical_higgs_repo_authority_audit"].get(
            "actual_current_surface_status", ""
        )
        and certificates["canonical_higgs_repo_authority_audit"].get("proposal_allowed")
        is False
        and certificates["canonical_higgs_repo_authority_audit"].get("repo_authority_found")
        is False
        and certificates["canonical_higgs_repo_authority_audit"].get(
            "exact_negative_boundary_passed"
        )
        is True
    )
    cross_lane_oh_authority_audit_blocks_adjacent_imports = (
        "cross-lane O_H authority audit"
        in certificates["cross_lane_oh_authority_audit"].get(
            "actual_current_surface_status", ""
        )
        and certificates["cross_lane_oh_authority_audit"].get("proposal_allowed")
        is False
        and certificates["cross_lane_oh_authority_audit"].get(
            "repo_cross_lane_authority_found"
        )
        is False
        and certificates["cross_lane_oh_authority_audit"].get(
            "cross_lane_oh_authority_audit_passed"
        )
        is True
    )
    sm_one_higgs_oh_import_boundary_blocks_shortcut = (
        "SM one-Higgs gauge selection is not PR230 O_H identity"
        in certificates["sm_one_higgs_oh_import_boundary"].get(
            "actual_current_surface_status", ""
        )
        and certificates["sm_one_higgs_oh_import_boundary"].get("proposal_allowed") is False
        and certificates["sm_one_higgs_oh_import_boundary"].get(
            "sm_one_higgs_import_closes_pr230"
        )
        is False
    )
    canonical_higgs_operator_candidate_stress_blocks = (
        "canonical-Higgs operator candidate stress rejects current substitutes"
        in certificates["canonical_higgs_operator_candidate_stress"].get(
            "actual_current_surface_status", ""
        )
        and certificates["canonical_higgs_operator_candidate_stress"].get("proposal_allowed")
        is False
        and all(
            row.get("candidate_valid") is False
            for row in certificates["canonical_higgs_operator_candidate_stress"].get(
                "candidate_rows", []
            )
        )
    )
    hunit_canonical_higgs_operator_candidate_gate_blocks = (
        "H_unit not canonical-Higgs operator realization"
        in certificates["hunit_canonical_higgs_operator_candidate_gate"].get("actual_current_surface_status", "")
        and certificates["hunit_canonical_higgs_operator_candidate_gate"].get("proposal_allowed") is False
        and certificates["hunit_canonical_higgs_operator_candidate_gate"].get(
            "hunit_canonical_higgs_operator_gate_passed"
        )
        is False
    )
    source_higgs_guard_status = certificates["source_higgs_harness_absence_guard"].get(
        "actual_current_surface_status", ""
    )
    source_higgs_guard_fields = certificates["source_higgs_harness_absence_guard"].get(
        "guard_fields", {}
    )
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
    source_higgs_harness_absence_guard_not_evidence = (
        (
            "source-Higgs harness absence guard" in source_higgs_guard_status
            or "source-Higgs harness default-off guard" in source_higgs_guard_status
        )
        and certificates["source_higgs_harness_absence_guard"].get("proposal_allowed") is False
        and source_higgs_guard_fields.get("source_higgs_cross_correlator") is True
        and source_higgs_operator_guarded
    )
    source_higgs_unratified_operator_smoke_not_evidence = (
        "source-Higgs unratified-operator smoke checkpoint"
        in certificates["source_higgs_unratified_operator_smoke"].get(
            "actual_current_surface_status", ""
        )
        and certificates["source_higgs_unratified_operator_smoke"].get("proposal_allowed")
        is False
        and certificates["source_higgs_unratified_operator_smoke"].get(
            "source_higgs_metadata", {}
        ).get("canonical_higgs_operator_realization")
        == "certificate_supplied_unratified"
        and certificates["source_higgs_unratified_operator_smoke"].get(
            "source_higgs_metadata", {}
        ).get("used_as_physical_yukawa_readout")
        is False
    )
    source_higgs_unratified_gram_shortcut_no_go_blocks = (
        "unratified source-Higgs Gram shortcut"
        in certificates["source_higgs_unratified_gram_shortcut_no_go"].get(
            "actual_current_surface_status", ""
        )
        and certificates["source_higgs_unratified_gram_shortcut_no_go"].get("proposal_allowed")
        is False
        and certificates["source_higgs_unratified_gram_shortcut_no_go"].get(
            "unratified_gram_shortcut_no_go_passed"
        )
        is True
    )
    neutral_scalar_rank_one_purity_gate_blocks = (
        "neutral scalar rank-one purity gate not passed"
        in certificates["neutral_scalar_rank_one_purity_gate"].get("actual_current_surface_status", "")
        and certificates["neutral_scalar_rank_one_purity_gate"].get("proposal_allowed") is False
        and certificates["neutral_scalar_rank_one_purity_gate"].get(
            "neutral_scalar_rank_one_purity_gate_passed"
        )
        is False
    )
    neutral_scalar_commutant_rank_no_go_blocks = (
        "neutral scalar commutant does not force rank-one purity"
        in certificates["neutral_scalar_commutant_rank_no_go"].get("actual_current_surface_status", "")
        and certificates["neutral_scalar_commutant_rank_no_go"].get("proposal_allowed") is False
        and certificates["neutral_scalar_commutant_rank_no_go"].get("rank_one_theorem_derived") is False
    )
    neutral_scalar_dynamical_rank_one_closure_blocks = (
        "dynamical rank-one neutral scalar theorem not derived"
        in certificates["neutral_scalar_dynamical_rank_one_closure"].get("actual_current_surface_status", "")
        and certificates["neutral_scalar_dynamical_rank_one_closure"].get("proposal_allowed") is False
        and certificates["neutral_scalar_dynamical_rank_one_closure"].get(
            "rank_one_dynamical_theorem_derived"
        )
        is False
    )
    orthogonal_neutral_decoupling_no_go_blocks = (
        "orthogonal neutral decoupling shortcut not derived"
        in certificates["orthogonal_neutral_decoupling_no_go"].get("actual_current_surface_status", "")
        and certificates["orthogonal_neutral_decoupling_no_go"].get("proposal_allowed") is False
        and certificates["orthogonal_neutral_decoupling_no_go"].get(
            "decoupling_scaling_theorem_derived"
        )
        is False
    )
    fh_gauge_response_mixed_scalar_blocks = (
        "FH gauge-response mixed-scalar obstruction"
        in certificates["fh_gauge_response_mixed_scalar"].get("actual_current_surface_status", "")
        and certificates["fh_gauge_response_mixed_scalar"].get("proposal_allowed") is False
    )
    no_orthogonal_top_coupling_import_blocks = (
        "no-orthogonal-top-coupling import audit"
        in certificates["no_orthogonal_top_coupling_import"].get("actual_current_surface_status", "")
        and certificates["no_orthogonal_top_coupling_import"].get("proposal_allowed") is False
        and certificates["no_orthogonal_top_coupling_import"].get(
            "no_orthogonal_top_coupling_theorem_found"
        )
        is False
    )
    no_orthogonal_top_coupling_selection_rule_blocks = (
        "no-orthogonal-top-coupling selection rule not derived"
        in certificates["no_orthogonal_top_coupling_selection_rule"].get(
            "actual_current_surface_status", ""
        )
        and certificates["no_orthogonal_top_coupling_selection_rule"].get("proposal_allowed") is False
        and certificates["no_orthogonal_top_coupling_selection_rule"].get(
            "no_orthogonal_top_coupling_selection_rule_gate_passed"
        )
        is False
    )
    d17_source_pole_identity_closure_blocked = (
        "D17 source-pole identity closure attempt blocked"
        in certificates["d17_source_pole_identity_closure"].get("actual_current_surface_status", "")
        and certificates["d17_source_pole_identity_closure"].get("proposal_allowed") is False
        and certificates["d17_source_pole_identity_closure"].get("theorem_closed") is False
    )
    source_overlap_sum_rule_no_go_blocks = (
        "source-overlap spectral sum-rule no-go"
        in certificates["source_overlap_sum_rule_no_go"].get("actual_current_surface_status", "")
        and certificates["source_overlap_sum_rule_no_go"].get("proposal_allowed") is False
    )
    short_distance_ope_lsz_no_go_blocks = (
        "short-distance OPE not scalar LSZ closure"
        in certificates["short_distance_ope_lsz_no_go"].get("actual_current_surface_status", "")
        and certificates["short_distance_ope_lsz_no_go"].get("proposal_allowed") is False
        and certificates["short_distance_ope_lsz_no_go"].get("short_distance_ope_shortcut_closed")
        is False
    )
    effective_mass_plateau_residue_no_go_blocks = (
        "effective-mass plateau not scalar LSZ residue closure"
        in certificates["effective_mass_plateau_residue_no_go"].get("actual_current_surface_status", "")
        and certificates["effective_mass_plateau_residue_no_go"].get("proposal_allowed") is False
        and certificates["effective_mass_plateau_residue_no_go"].get(
            "effective_mass_plateau_residue_gate_passed"
        )
        is False
    )
    finite_source_shift_derivative_no_go_blocks = (
        "finite source-shift slope not zero-source derivative certificate"
        in certificates["finite_source_shift_derivative_no_go"].get("actual_current_surface_status", "")
        and certificates["finite_source_shift_derivative_no_go"].get("proposal_allowed") is False
        and certificates["finite_source_shift_derivative_no_go"].get(
            "finite_source_shift_derivative_gate_passed"
        )
        is False
    )
    finite_source_linearity_gate_not_closure = (
        "finite-source-linearity gate"
        in certificates["fh_lsz_finite_source_linearity_gate"].get("actual_current_surface_status", "")
        and certificates["fh_lsz_finite_source_linearity_gate"].get("proposal_allowed") is False
    )
    finite_source_linearity_calibration_not_closure = (
        "finite-source-linearity calibration"
        in certificates["fh_lsz_finite_source_linearity_calibration"].get("actual_current_surface_status", "")
        and certificates["fh_lsz_finite_source_linearity_calibration"].get("proposal_allowed") is False
    )
    target_observable_ess_not_closure = (
        "target-observable ESS certificate"
        in certificates["fh_lsz_target_observable_ess"].get("actual_current_surface_status", "")
        and certificates["fh_lsz_target_observable_ess"].get("proposal_allowed") is False
    )
    autocorrelation_ess_gate_not_closure = (
        "autocorrelation ESS gate"
        in certificates["fh_lsz_autocorrelation_ess_gate"].get("actual_current_surface_status", "")
        and certificates["fh_lsz_autocorrelation_ess_gate"].get("proposal_allowed") is False
    )
    response_window_forensics_not_closure = (
        "response-window forensics"
        in certificates["fh_lsz_response_window_forensics"].get("actual_current_surface_status", "")
        and certificates["fh_lsz_response_window_forensics"].get("proposal_allowed") is False
        and certificates["fh_lsz_response_window_forensics"].get("readout_switch_authorized") is False
    )
    common_window_response_provenance_not_closure = (
        "common-window response provenance"
        in certificates["fh_lsz_common_window_response_provenance"].get(
            "actual_current_surface_status", ""
        )
        and certificates["fh_lsz_common_window_response_provenance"].get("proposal_allowed")
        is False
        and certificates["fh_lsz_common_window_response_provenance"].get(
            "readout_switch_authorized"
        )
        is False
        and certificates["fh_lsz_common_window_response_provenance"].get(
            "common_window_stability_passed"
        )
        is True
        and certificates["fh_lsz_common_window_response_provenance"].get(
            "common_window_production_grade"
        )
        is False
    )
    common_window_response_gate_not_closure = (
        "common-window response gate"
        in certificates["fh_lsz_common_window_response_gate"].get(
            "actual_current_surface_status", ""
        )
        and certificates["fh_lsz_common_window_response_gate"].get("proposal_allowed")
        is False
        and certificates["fh_lsz_common_window_response_gate"].get(
            "readout_switch_authorized"
        )
        is False
    )
    common_window_pooled_response_estimator_not_closure = (
        "common-window pooled response estimator"
        in certificates["fh_lsz_common_window_pooled_response_estimator"].get(
            "actual_current_surface_status", ""
        )
        and certificates["fh_lsz_common_window_pooled_response_estimator"].get(
            "proposal_allowed"
        )
        is False
        and certificates["fh_lsz_common_window_pooled_response_estimator"].get(
            "pooled_common_window_response_production_grade"
        )
        is True
        and certificates["fh_lsz_common_window_pooled_response_estimator"].get(
            "readout_switch_authorized"
        )
        is False
    )
    common_window_replacement_response_stability_not_closure = (
        "common-window replacement response-stability passed"
        in certificates["fh_lsz_common_window_replacement_response_stability"].get(
            "actual_current_surface_status", ""
        )
        and certificates["fh_lsz_common_window_replacement_response_stability"].get(
            "proposal_allowed"
        )
        is False
        and certificates["fh_lsz_common_window_replacement_response_stability"].get(
            "replacement_response_stability_passed"
        )
        is True
        and certificates["fh_lsz_common_window_replacement_response_stability"].get(
            "readout_switch_authorized"
        )
        is False
    )
    v2_target_response_stability_not_closure = (
        "v2 target-response stability passed"
        in certificates["fh_lsz_v2_target_response_stability"].get("actual_current_surface_status", "")
        and certificates["fh_lsz_v2_target_response_stability"].get("proposal_allowed") is False
        and certificates["fh_lsz_v2_target_response_stability"].get("readout_switch_authorized") is False
    )
    response_window_acceptance_gate_blocks = (
        "response-window acceptance gate not passed"
        in certificates["fh_lsz_response_window_acceptance_gate"].get("actual_current_surface_status", "")
        and certificates["fh_lsz_response_window_acceptance_gate"].get("proposal_allowed") is False
        and certificates["fh_lsz_response_window_acceptance_gate"].get(
            "response_window_acceptance_gate_passed"
        )
        is False
    )
    target_timeseries_replacement_queue_cert = certificates[
        "fh_lsz_target_timeseries_replacement_queue"
    ]
    target_timeseries_replacement_queue_not_closure = (
        "FH-LSZ target-timeseries replacement queue"
        in target_timeseries_replacement_queue_cert.get("actual_current_surface_status", "")
        and target_timeseries_replacement_queue_cert.get("proposal_allowed") is False
        and (
            bool(target_timeseries_replacement_queue_cert.get("replacement_queue"))
            or target_timeseries_replacement_queue_cert.get("target_timeseries_summary", {}).get(
                "complete_for_all_ready_chunks"
            )
            is True
        )
    )
    target_timeseries_full_set_checkpoint_cert = certificates[
        "fh_lsz_target_timeseries_full_set_checkpoint"
    ]
    target_timeseries_full_set_checkpoint_not_closure = (
        "FH-LSZ full L12 target-timeseries packet checkpoint"
        in target_timeseries_full_set_checkpoint_cert.get("actual_current_surface_status", "")
        and target_timeseries_full_set_checkpoint_cert.get("proposal_allowed") is False
        and target_timeseries_full_set_checkpoint_cert.get("schema_summary", {}).get(
            "checked_chunks"
        )
        == 63
        and target_timeseries_full_set_checkpoint_cert.get("replacement_queue") == []
    )
    target_timeseries_harness_support_not_evidence = (
        "target time-series harness extension"
        in certificates["fh_lsz_target_timeseries_harness"].get("actual_current_surface_status", "")
        and certificates["fh_lsz_target_timeseries_harness"].get("proposal_allowed") is False
        and certificates["fh_lsz_target_timeseries_harness"].get("target_timeseries_harness_supported") is True
    )
    multitau_target_timeseries_harness_support_not_evidence = (
        "multi-tau target time-series harness extension"
        in certificates["fh_lsz_multitau_target_timeseries_harness"].get(
            "actual_current_surface_status", ""
        )
        and certificates["fh_lsz_multitau_target_timeseries_harness"].get("proposal_allowed") is False
    )
    selected_mass_normal_cache_speedup_not_evidence = (
        "selected-mass normal-cache speedup"
        in certificates["fh_lsz_selected_mass_normal_cache_speedup"].get("actual_current_surface_status", "")
        and certificates["fh_lsz_selected_mass_normal_cache_speedup"].get("proposal_allowed") is False
    )
    top_mass_scan_response_harness_support_not_evidence = (
        "top mass-scan response harness schema gate"
        in certificates["top_mass_scan_response_harness_gate"].get("actual_current_surface_status", "")
        and certificates["top_mass_scan_response_harness_gate"].get("proposal_allowed") is False
        and certificates["top_mass_scan_response_harness_gate"].get(
            "top_mass_scan_response_harness_gate_passed"
        )
        is True
    )
    global_production_collision_guard_not_evidence = (
        "FH-LSZ global production collision guard"
        in certificates["fh_lsz_global_production_collision_guard"].get("actual_current_surface_status", "")
        and certificates["fh_lsz_global_production_collision_guard"].get("proposal_allowed") is False
        and certificates["fh_lsz_global_production_collision_guard"].get("global_cap") == 6
    )
    target_timeseries_higgs_identity_no_go_blocks = (
        "target time series not canonical-Higgs identity"
        in certificates["fh_lsz_target_timeseries_higgs_identity_no_go"].get(
            "actual_current_surface_status", ""
        )
        and certificates["fh_lsz_target_timeseries_higgs_identity_no_go"].get("proposal_allowed") is False
        and certificates["fh_lsz_target_timeseries_higgs_identity_no_go"].get(
            "target_timeseries_higgs_identity_gate_passed"
        )
        is False
    )
    higgs_pole_identity_latest_blocker_blocks = (
        "latest Higgs-pole identity blocker certificate"
        in certificates["higgs_pole_identity_latest_blocker"].get("actual_current_surface_status", "")
        and certificates["higgs_pole_identity_latest_blocker"].get("proposal_allowed") is False
        and certificates["higgs_pole_identity_latest_blocker"].get("identity_closed") is False
    )
    pole_fit_mode_budget_not_closure = (
        "pole-fit mode-noise budget"
        in certificates["fh_lsz_pole_fit_mode_budget"].get("actual_current_surface_status", "")
        and certificates["fh_lsz_pole_fit_mode_budget"].get("proposal_allowed") is False
    )
    eight_mode_noise_variance_not_closure = (
        "eight-mode noise variance gate"
        in certificates["fh_lsz_eight_mode_noise_variance"].get("actual_current_surface_status", "")
        and certificates["fh_lsz_eight_mode_noise_variance"].get("proposal_allowed") is False
    )
    noise_subsample_diagnostics_not_closure = (
        "noise-subsample diagnostics"
        in certificates["fh_lsz_noise_subsample_diagnostics"].get("actual_current_surface_status", "")
        and certificates["fh_lsz_noise_subsample_diagnostics"].get("proposal_allowed") is False
    )
    variance_calibration_manifest_not_evidence = (
        "variance calibration manifest"
        in certificates["fh_lsz_variance_calibration_manifest"].get("actual_current_surface_status", "")
        and certificates["fh_lsz_variance_calibration_manifest"].get("proposal_allowed") is False
    )
    paired_variance_calibration_gate_not_closure = (
        "paired x8/x16 variance calibration"
        in certificates["fh_lsz_paired_variance_calibration_gate"].get("actual_current_surface_status", "")
        and certificates["fh_lsz_paired_variance_calibration_gate"].get("proposal_allowed") is False
    )
    polefit8x8_manifest_not_evidence = (
        "eight-mode-x8 pole-fit chunk manifest"
        in certificates["fh_lsz_polefit8x8_chunk_manifest"].get("actual_current_surface_status", "")
        and certificates["fh_lsz_polefit8x8_chunk_manifest"].get("proposal_allowed") is False
    )
    polefit8x8_combiner_not_closure = (
        (
            "eight-mode-x8 pole-fit combiner"
            in certificates["fh_lsz_polefit8x8_chunk_combiner_gate"].get("actual_current_surface_status", "")
            or "eight-mode-x8 pole-fit stream"
            in certificates["fh_lsz_polefit8x8_chunk_combiner_gate"].get("actual_current_surface_status", "")
            or "complete L12 eight-mode-x8 pole-fit summary"
            in certificates["fh_lsz_polefit8x8_chunk_combiner_gate"].get("actual_current_surface_status", "")
        )
        and certificates["fh_lsz_polefit8x8_chunk_combiner_gate"].get("proposal_allowed") is False
    )
    polefit8x8_postprocessor_not_closure = (
        "eight-mode-x8"
        in certificates["fh_lsz_polefit8x8_postprocessor"].get("actual_current_surface_status", "")
        and certificates["fh_lsz_polefit8x8_postprocessor"].get("proposal_allowed") is False
    )
    joint_resource_multiday = (
        float(certificates["joint_resource_projection"].get("projection", {}).get("joint_mass_scaled_hours", 0.0)) > 1000.0
        and certificates["joint_resource_projection"].get("proposal_allowed") is False
    )
    full_positive_assembly_gate_open = (
        "full positive PR230 closure assembly gate not passed"
        in certificates["full_positive_closure_assembly_gate"].get("actual_current_surface_status", "")
        and certificates["full_positive_closure_assembly_gate"].get("proposal_allowed") is False
        and certificates["full_positive_closure_assembly_gate"].get("chunk_only_evaluation", {}).get(
            "assembly_passed"
        )
        is False
    )
    negative_route_applicability_review_passed = (
        "negative-route applicability review passed"
        in certificates["negative_route_applicability_review"].get("actual_current_surface_status", "")
        and certificates["negative_route_applicability_review"].get("no_retained_negative_overclaim")
        is True
        and certificates["negative_route_applicability_review"].get("future_reopen_paths_preserved")
        is True
        and certificates["negative_route_applicability_review"].get(
            "selected_negative_results_apply_on_current_surface"
        )
        is True
        and certificates["negative_route_applicability_review"].get("proposal_allowed") is False
    )
    pr230_nonchunk_current_surface_exhaustion_blocks = (
        "current PR230 non-chunk route queue exhausted"
        in certificates["pr230_nonchunk_current_surface_exhaustion"].get(
            "actual_current_surface_status", ""
        )
        and certificates["pr230_nonchunk_current_surface_exhaustion"].get("proposal_allowed")
        is False
        and certificates["pr230_nonchunk_current_surface_exhaustion"].get(
            "current_surface_exhaustion_gate_passed"
        )
        is True
    )
    pr230_nonchunk_future_artifact_intake_blocks = (
        "future-artifact intake"
        in certificates["pr230_nonchunk_future_artifact_intake"].get(
            "actual_current_surface_status", ""
        )
        and certificates["pr230_nonchunk_future_artifact_intake"].get("proposal_allowed")
        is False
        and certificates["pr230_nonchunk_future_artifact_intake"].get(
            "future_artifact_intake_gate_passed"
        )
        is True
        and certificates["pr230_nonchunk_future_artifact_intake"].get(
            "dramatic_step_gate", {}
        ).get("passed")
        is False
    )
    pr230_nonchunk_terminal_route_exhaustion_blocks = (
        "terminal route-exhaustion gate"
        in certificates["pr230_nonchunk_terminal_route_exhaustion"].get(
            "actual_current_surface_status", ""
        )
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
        is False
    )
    pr230_nonchunk_reopen_admissibility_blocks = (
        "reopen-admissibility gate"
        in certificates["pr230_nonchunk_reopen_admissibility"].get(
            "actual_current_surface_status", ""
        )
        and certificates["pr230_nonchunk_reopen_admissibility"].get(
            "proposal_allowed"
        )
        is False
        and certificates["pr230_nonchunk_reopen_admissibility"].get(
            "reopen_admissibility_gate_passed"
        )
        is True
        and certificates["pr230_nonchunk_reopen_admissibility"].get(
            "dramatic_step_gate", {}
        ).get("passed")
        is False
    )
    pr230_nonchunk_cycle14_route_selector_blocks = (
        "cycle-14 route-selector gate"
        in certificates["pr230_nonchunk_cycle14_route_selector"].get(
            "actual_current_surface_status", ""
        )
        and certificates["pr230_nonchunk_cycle14_route_selector"].get(
            "proposal_allowed"
        )
        is False
        and certificates["pr230_nonchunk_cycle14_route_selector"].get(
            "route_selector_gate_passed"
        )
        is True
        and certificates["pr230_nonchunk_cycle14_route_selector"].get(
            "dramatic_step_gate", {}
        ).get("passed")
        is False
    )
    pr230_nonchunk_cycle15_independent_route_admission_blocks = (
        "cycle-15 independent-route admission gate"
        in certificates["pr230_nonchunk_cycle15_independent_route_admission"].get(
            "actual_current_surface_status", ""
        )
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
        is False
    )
    pr230_nonchunk_cycle16_reopen_source_guard_blocks = (
        "cycle-16 reopen-source guard"
        in certificates["pr230_nonchunk_cycle16_reopen_source_guard"].get(
            "actual_current_surface_status", ""
        )
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
        is False
    )
    pr230_nonchunk_cycle17_stop_condition_blocks = (
        "cycle-17 stop-condition gate"
        in certificates["pr230_nonchunk_cycle17_stop_condition_gate"].get(
            "actual_current_surface_status", ""
        )
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
        is False
    )
    pr230_nonchunk_cycle18_reopen_freshness_blocks = (
        "cycle-18 reopen-freshness gate"
        in certificates["pr230_nonchunk_cycle18_reopen_freshness_gate"].get(
            "actual_current_surface_status", ""
        )
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
        is False
    )
    pr230_nonchunk_cycle19_no_duplicate_route_blocks = (
        "cycle-19 no-duplicate-route gate"
        in certificates["pr230_nonchunk_cycle19_no_duplicate_route_gate"].get(
            "actual_current_surface_status", ""
        )
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
        is False
    )
    pr230_nonchunk_cycle20_process_gate_continuation_blocks = (
        "cycle-20 process-gate continuation no-go"
        in certificates["pr230_nonchunk_cycle20_process_gate_continuation_no_go"].get(
            "actual_current_surface_status", ""
        )
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
        is False
    )
    pr230_nonchunk_cycle21_remote_reopen_guard_blocks = (
        "cycle-21 remote-surface reopen guard"
        in certificates["pr230_nonchunk_cycle21_remote_reopen_guard"].get(
            "actual_current_surface_status", ""
        )
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
        is False
    )
    pr230_nonchunk_cycle22_main_audit_drift_guard_blocks = (
        "cycle-22 main-audit-drift reopen guard"
        in certificates["pr230_nonchunk_cycle22_main_audit_drift_guard"].get(
            "actual_current_surface_status", ""
        )
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
        is False
    )
    pr230_nonchunk_cycle23_main_effective_status_drift_guard_blocks = (
        "cycle-23 main-effective-status-drift reopen guard"
        in certificates["pr230_nonchunk_cycle23_main_effective_status_drift_guard"].get(
            "actual_current_surface_status", ""
        )
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
        is False
    )
    pr230_nonchunk_cycle24_post_cycle23_main_status_drift_guard_blocks = (
        "cycle-24 post-cycle-23 main-status-drift reopen guard"
        in certificates[
            "pr230_nonchunk_cycle24_post_cycle23_main_status_drift_guard"
        ].get("actual_current_surface_status", "")
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
        is False
    )
    pr230_nonchunk_cycle25_post_cycle24_main_audit_status_drift_guard_blocks = (
        "cycle-25 post-cycle-24 main-audit-status-drift reopen guard"
        in certificates[
            "pr230_nonchunk_cycle25_post_cycle24_main_audit_status_drift_guard"
        ].get("actual_current_surface_status", "")
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
        is False
    )
    pr230_nonchunk_cycle26_post_cycle25_main_audit_status_drift_guard_blocks = (
        "cycle-26 post-cycle-25 main-audit-status-drift reopen guard"
        in certificates[
            "pr230_nonchunk_cycle26_post_cycle25_main_audit_status_drift_guard"
        ].get("actual_current_surface_status", "")
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
        is False
    )
    pr230_nonchunk_cycle27_post_cycle26_main_audit_status_drift_guard_blocks = (
        "cycle-27 post-cycle-26 main-audit-status-drift reopen guard"
        in certificates[
            "pr230_nonchunk_cycle27_post_cycle26_main_audit_status_drift_guard"
        ].get("actual_current_surface_status", "")
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
        is False
    )
    pr230_nonchunk_cycle28_post_cycle27_main_audit_status_drift_guard_blocks = (
        "cycle-28 post-cycle-27 main-audit-status-drift reopen guard"
        in certificates[
            "pr230_nonchunk_cycle28_post_cycle27_main_audit_status_drift_guard"
        ].get("actual_current_surface_status", "")
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
        is False
    )
    pr230_nonchunk_cycle29_post_cycle28_main_audit_status_drift_guard_blocks = (
        "cycle-29 post-cycle-28 main-audit-status-drift reopen guard"
        in certificates[
            "pr230_nonchunk_cycle29_post_cycle28_main_audit_status_drift_guard"
        ].get("actual_current_surface_status", "")
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
        is False
    )
    pr230_nonchunk_cycle30_post_cycle29_main_audit_status_drift_guard_blocks = (
        "cycle-30 post-cycle-29 main-audit-status-drift reopen guard"
        in certificates[
            "pr230_nonchunk_cycle30_post_cycle29_main_audit_status_drift_guard"
        ].get("actual_current_surface_status", "")
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
        is False
    )
    pr230_nonchunk_cycle31_post_cycle30_main_audit_status_drift_guard_blocks = (
        "cycle-31 post-cycle-30 main-audit-status-drift reopen guard"
        in certificates[
            "pr230_nonchunk_cycle31_post_cycle30_main_audit_status_drift_guard"
        ].get("actual_current_surface_status", "")
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
        is False
    )
    pr230_nonchunk_cycle32_post_cycle31_main_audit_status_drift_guard_blocks = (
        "cycle-32 post-cycle-31 main-audit-status-drift reopen guard"
        in certificates[
            "pr230_nonchunk_cycle32_post_cycle31_main_audit_status_drift_guard"
        ].get("actual_current_surface_status", "")
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
        is False
    )
    pr230_nonchunk_cycle33_post_cycle32_main_audit_status_drift_guard_blocks = (
        "cycle-33 post-cycle-32 main-audit-status-drift reopen guard"
        in certificates[
            "pr230_nonchunk_cycle33_post_cycle32_main_audit_status_drift_guard"
        ].get("actual_current_surface_status", "")
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
        is False
    )
    pr230_nonchunk_cycle34_post_cycle33_main_nonpr230_drift_guard_blocks = (
        "cycle-34 post-cycle-33 main non-PR230 drift reopen guard"
        in certificates[
            "pr230_nonchunk_cycle34_post_cycle33_main_nonpr230_drift_guard"
        ].get("actual_current_surface_status", "")
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
        is False
    )
    pr230_nonchunk_cycle35_post_cycle34_main_audit_ledger_drift_guard_blocks = (
        "cycle-35 post-cycle-34 main audit-ledger drift reopen guard"
        in certificates[
            "pr230_nonchunk_cycle35_post_cycle34_main_audit_ledger_drift_guard"
        ].get("actual_current_surface_status", "")
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
        is False
    )
    interacting_kinetic_still_open = (
        certificates["interacting_kinetic_sensitivity"].get("actual_current_surface_status")
        == "bounded-support / interacting kinetic background sensitivity"
        and certificates["interacting_kinetic_sensitivity"].get("proposal_allowed") is False
    )
    beta_blocked = "no-go" in certificates["beta_lambda_no_go"].get("actual_current_surface_status", "")
    queue_text = (
        certificates["queue_exhaustion"].get("actual_current_surface_status", "")
        + " "
        + certificates["queue_exhaustion"].get("verdict", "")
    ).lower()
    queue_open = "queue exhausted" in queue_text and "no retained" in queue_text

    report("required-certificates-present", not missing, f"missing={missing}")
    report("no-hidden-retained-yt-proof", no_hidden_proof, "global audit retained_y_t_rows empty")
    report("direct-strict-production-not-yet-passed", not direct_strict_pass, f"direct_meta={direct_meta}")
    report("ward-repair-still-open", ward_open, f"closure_allowed={certificates['ward_repair_audit'].get('closure_allowed')}")
    report("scalar-pole-residue-blocked-on-current-surface", scalar_residue_blocked, certificates["scalar_pole_residue_no_go"].get("actual_current_surface_status", ""))
    report(
        "key-blocker-closure-attempt-open",
        key_blocker_open,
        certificates["key_blocker_closure_attempt"].get("actual_current_surface_status", ""),
    )
    report(
        "key-blocker-no-retained-authority",
        key_blocker_has_no_retained_authority,
        "no retained authority supplies pole residue plus common dressing",
    )
    report(
        "lsz-normalization-cancellation-not-closure",
        lsz_norm_conditional,
        certificates["lsz_normalization_cancellation"].get("actual_current_surface_status", ""),
    )
    report(
        "feshbach-response-boundary-not-common-dressing",
        feshbach_boundary_not_common_dressing,
        certificates["feshbach_response_boundary"].get("actual_current_surface_status", ""),
    )
    report(
        "fh-lsz-invariant-readout-not-closure",
        invariant_readout_not_closure,
        certificates["fh_lsz_invariant_readout"].get("actual_current_surface_status", ""),
    )
    report(
        "scalar-ladder-derivative-limit-blocks-lsz",
        derivative_limit_blocks_ladder,
        certificates["scalar_ladder_derivative_limit"].get("actual_current_surface_status", ""),
    )
    report(
        "scalar-ladder-residue-envelope-blocks-lsz",
        residue_envelope_blocks_ladder,
        certificates["scalar_ladder_residue_envelope"].get("actual_current_surface_status", ""),
    )
    report(
        "scalar-kernel-ward-identity-does-not-fix-k-prime",
        ward_identity_does_not_fix_kernel,
        certificates["scalar_kernel_ward_identity"].get("actual_current_surface_status", ""),
    )
    report(
        "scalar-zero-mode-limit-order-not-selected",
        zero_mode_limit_order_blocks_denominator,
        certificates["scalar_zero_mode_limit_order"].get("actual_current_surface_status", ""),
    )
    report(
        "zero-mode-prescription-not-hidden-import",
        zero_mode_import_audit_blocks_hidden_authority,
        certificates["zero_mode_prescription_import"].get("actual_current_surface_status", ""),
    )
    report(
        "flat-toron-sectors-block-trivial-zero-mode-selection",
        flat_toron_blocks_trivial_selection,
        certificates["flat_toron_denominator"].get("actual_current_surface_status", ""),
    )
    report(
        "flat-toron-washout-support-not-closure",
        flat_toron_washout_not_closure,
        certificates["flat_toron_washout"].get("actual_current_surface_status", ""),
    )
    report(
        "color-singlet-zero-mode-cancellation-not-closure",
        color_singlet_zero_mode_not_closure,
        certificates["color_singlet_zero_mode"].get("actual_current_surface_status", ""),
    )
    report(
        "color-singlet-finite-q-ir-regularity-not-closure",
        color_singlet_finite_q_ir_not_closure,
        certificates["color_singlet_finite_q_ir"].get("actual_current_surface_status", ""),
    )
    report(
        "color-singlet-zero-mode-removed-ladder-pole-search-not-closure",
        color_singlet_ladder_pole_search_not_closure,
        certificates["color_singlet_zero_mode_removed_ladder_pole_search"].get("actual_current_surface_status", ""),
    )
    report(
        "taste-corner-ladder-pole-witness-not-closure",
        taste_corner_ladder_pole_obstruction_not_closure,
        certificates["taste_corner_ladder_pole_obstruction"].get("actual_current_surface_status", ""),
    )
    report(
        "taste-carrier-import-audit-blocks-hidden-authority",
        taste_carrier_import_audit_blocks_hidden_authority,
        certificates["taste_carrier_import_audit"].get("actual_current_surface_status", ""),
    )
    report(
        "taste-singlet-normalization-removes-finite-crossings",
        taste_singlet_normalization_removes_crossings,
        certificates["taste_singlet_ladder_normalization"].get("actual_current_surface_status", ""),
    )
    report(
        "scalar-taste-projector-normalization-attempt-blocked",
        scalar_taste_projector_attempt_blocked,
        certificates["scalar_taste_projector_normalization_attempt"].get(
            "actual_current_surface_status", ""
        ),
    )
    report(
        "unit-projector-pole-threshold-blocks-finite-ladder",
        unit_projector_pole_threshold_blocks_finite_ladder,
        certificates["unit_projector_pole_threshold"].get("actual_current_surface_status", ""),
    )
    report(
        "scalar-kernel-enhancement-import-audit-blocks-hidden-authority",
        scalar_kernel_enhancement_import_blocks_hidden_authority,
        certificates["scalar_kernel_enhancement_import"].get("actual_current_surface_status", ""),
    )
    report(
        "fitted-kernel-residue-selector-not-closure",
        fitted_kernel_selector_not_closure,
        certificates["fitted_kernel_residue_selector"].get("actual_current_surface_status", ""),
    )
    report(
        "cl3-source-unit-does-not-fix-kappa",
        cl3_source_unit_blocks_kappa,
        certificates["cl3_source_unit"].get("actual_current_surface_status", ""),
    )
    report(
        "gauge-vev-source-overlap-does-not-fix-kappa",
        gauge_vev_source_overlap_blocks_kappa,
        certificates["gauge_vev_source_overlap"].get("actual_current_surface_status", ""),
    )
    report(
        "canonical-kinetic-renormalization-does-not-fix-source-overlap",
        scalar_renormalization_condition_overlap_blocks_kappa,
        certificates["scalar_renormalization_condition_overlap"].get("actual_current_surface_status", ""),
    )
    report(
        "source-contact-term-scheme-does-not-fix-pole-residue",
        scalar_source_contact_term_scheme_not_lsz,
        certificates["scalar_source_contact_term_scheme"].get("actual_current_surface_status", ""),
    )
    report(
        "fh-lsz-production-manifest-not-evidence",
        production_manifest_not_evidence,
        certificates["fh_lsz_production_manifest"].get("actual_current_surface_status", ""),
    )
    report(
        "fh-lsz-production-postprocess-gate-blocks-closure",
        production_postprocess_gate_blocks_closure,
        certificates["fh_lsz_production_postprocess_gate"].get("actual_current_surface_status", ""),
    )
    report(
        "fh-lsz-production-checkpoint-not-foreground-safe",
        production_checkpoint_not_foreground_safe,
        certificates["fh_lsz_production_checkpoint_granularity"].get("actual_current_surface_status", ""),
    )
    report(
        "fh-lsz-chunked-production-manifest-not-evidence",
        chunked_manifest_not_evidence,
        certificates["fh_lsz_chunked_production_manifest"].get("actual_current_surface_status", ""),
    )
    report(
        "fh-lsz-chunk-combiner-gate-not-evidence",
        chunk_combiner_not_evidence,
        certificates["fh_lsz_chunk_combiner_gate"].get("actual_current_surface_status", ""),
    )
    report(
        "fh-lsz-chunk001-checkpoint-not-closure",
        chunk001_checkpoint_not_closure,
        certificates["fh_lsz_chunk001_checkpoint"].get("actual_current_surface_status", ""),
    )
    report(
        "fh-lsz-chunk002-checkpoint-not-closure",
        chunk002_checkpoint_not_closure,
        certificates["fh_lsz_chunk002_checkpoint"].get("actual_current_surface_status", ""),
    )
    report(
        "fh-lsz-ready-chunk-set-checkpoint-not-closure",
        ready_chunk_set_not_closure,
        certificates["fh_lsz_ready_chunk_set_checkpoint"].get("actual_current_surface_status", ""),
    )
    report(
        "fh-lsz-ready-chunk-response-stability-not-closure",
        ready_chunk_response_not_closure,
        certificates["fh_lsz_ready_chunk_response_stability"].get("actual_current_surface_status", ""),
    )
    report(
        "fh-lsz-chunk011-target-timeseries-not-closure",
        chunk011_target_timeseries_not_closure,
        certificates["fh_lsz_chunk011_target_timeseries"].get("actual_current_surface_status", ""),
    )
    report(
        "fh-lsz-generic-chunk-target-timeseries-not-closure",
        chunk011_generic_target_timeseries_not_closure,
        certificates["fh_lsz_chunk011_target_timeseries_generic"].get("actual_current_surface_status", ""),
    )
    report(
        "fh-lsz-chunk012-target-timeseries-not-closure",
        chunk012_generic_target_timeseries_not_closure,
        certificates["fh_lsz_chunk012_target_timeseries_generic"].get("actual_current_surface_status", ""),
    )
    report(
        "fh-lsz-generic-chunk-target-checkpoints-discovered",
        generic_chunk_targets_not_closure,
        f"count={len(generic_chunk_target_certificates)}",
    )
    report(
        "fh-lsz-v2-multitau-chunk-target-checkpoints-discovered",
        multitau_chunk_targets_not_closure,
        f"count={len(multitau_chunk_target_certificates)}",
    )
    report(
        "fh-lsz-legacy-v2-backfill-boundary",
        legacy_v2_backfill_not_possible,
        certificates["fh_lsz_legacy_v2_backfill_feasibility"].get("actual_current_surface_status", ""),
    )
    report(
        "fh-lsz-pole-fit-kinematics-not-closure",
        pole_fit_kinematics_not_closure,
        certificates["fh_lsz_pole_fit_kinematics"].get("actual_current_surface_status", ""),
    )
    report(
        "fh-lsz-pole-fit-postprocessor-not-evidence",
        pole_fit_postprocessor_not_evidence,
        certificates["fh_lsz_pole_fit_postprocessor"].get("actual_current_surface_status", ""),
    )
    report(
        "fh-lsz-finite-shell-pole-fit-not-identified",
        finite_shell_identifiability_not_closure,
        certificates["fh_lsz_finite_shell_identifiability"].get("actual_current_surface_status", ""),
    )
    report(
        "fh-lsz-pole-fit-model-class-gate-blocks",
        pole_fit_model_class_gate_blocks,
        certificates["fh_lsz_pole_fit_model_class_gate"].get("actual_current_surface_status", ""),
    )
    report(
        "fh-lsz-model-class-semantic-firewall-not-closure",
        model_class_semantic_firewall_not_closure,
        certificates["fh_lsz_model_class_semantic_firewall"].get("actual_current_surface_status", ""),
    )
    report(
        "fh-lsz-stieltjes-model-class-not-enough",
        stieltjes_model_class_not_enough,
        certificates["fh_lsz_stieltjes_model_class"].get("actual_current_surface_status", ""),
    )
    report(
        "fh-lsz-stieltjes-moment-certificate-gate-absent",
        stieltjes_moment_certificate_absent,
        certificates["fh_lsz_stieltjes_moment_certificate_gate"].get(
            "actual_current_surface_status", ""
        ),
    )
    report(
        "fh-lsz-pade-stieltjes-bounds-gate-absent",
        pade_stieltjes_bounds_certificate_absent,
        certificates["fh_lsz_pade_stieltjes_bounds_gate"].get(
            "actual_current_surface_status", ""
        ),
    )
    report(
        "fh-lsz-polefit8x8-stieltjes-proxy-diagnostic-blocks-current-proxy",
        stieltjes_proxy_diagnostic_blocks,
        certificates["fh_lsz_polefit8x8_stieltjes_proxy_diagnostic"].get(
            "actual_current_surface_status", ""
        ),
    )
    report(
        "fh-lsz-complete-bernstein-inverse-diagnostic-blocks-current-denominator",
        complete_bernstein_inverse_diagnostic_blocks,
        certificates["fh_lsz_complete_bernstein_inverse_diagnostic"].get(
            "actual_current_surface_status", ""
        ),
    )
    report(
        "pr230-scalar-lsz-holonomic-exact-authority-attempt-blocks-current-finite-shell",
        scalar_lsz_holonomic_exact_authority_blocks,
        certificates["pr230_scalar_lsz_holonomic_exact_authority_attempt"].get(
            "actual_current_surface_status", ""
        ),
    )
    report(
        "pr230-scalar-lsz-carleman-tauberian-determinacy-attempt-blocks-current-finite-prefix",
        scalar_lsz_carleman_tauberian_determinacy_blocks,
        certificates[
            "pr230_scalar_lsz_carleman_tauberian_determinacy_attempt"
        ].get("actual_current_surface_status", ""),
    )
    report(
        "fh-lsz-contact-subtraction-identifiability-blocks-arbitrary-subtraction",
        contact_subtraction_identifiability_blocks,
        certificates["fh_lsz_contact_subtraction_identifiability"].get(
            "actual_current_surface_status", ""
        ),
    )
    report(
        "fh-lsz-affine-contact-complete-monotonicity-blocks",
        affine_contact_complete_monotonicity_blocks,
        certificates["fh_lsz_affine_contact_complete_monotonicity"].get(
            "actual_current_surface_status", ""
        ),
    )
    report(
        "fh-lsz-polynomial-contact-finite-shell-blocks",
        polynomial_contact_finite_shell_blocks,
        certificates["fh_lsz_polynomial_contact_finite_shell"].get(
            "actual_current_surface_status", ""
        ),
    )
    report(
        "fh-lsz-polynomial-contact-repair-no-go-blocks",
        polynomial_contact_repair_blocks,
        certificates["fh_lsz_polynomial_contact_repair"].get(
            "actual_current_surface_status", ""
        ),
    )
    report(
        "fh-lsz-pole-saturation-threshold-gate-blocks",
        pole_saturation_threshold_gate_blocks,
        certificates["fh_lsz_pole_saturation_threshold_gate"].get("actual_current_surface_status", ""),
    )
    report(
        "fh-lsz-threshold-authority-audit-blocks-hidden-import",
        threshold_authority_audit_blocks,
        certificates["fh_lsz_threshold_authority_audit"].get("actual_current_surface_status", ""),
    )
    report(
        "confinement-gap-threshold-import-blocks",
        confinement_gap_threshold_import_blocks,
        certificates["confinement_gap_threshold_import"].get("actual_current_surface_status", ""),
    )
    report(
        "fh-lsz-finite-volume-pole-saturation-blocks",
        finite_volume_pole_saturation_blocks,
        certificates["fh_lsz_finite_volume_pole_saturation"].get("actual_current_surface_status", ""),
    )
    report(
        "fh-lsz-numba-seed-independence-blocks-historical-chunks",
        numba_seed_independence_blocks_historical_chunks,
        certificates["fh_lsz_numba_seed_independence"].get("actual_current_surface_status", ""),
    )
    report(
        "fh-lsz-uniform-gap-self-certification-blocks",
        uniform_gap_self_certification_blocks,
        certificates["fh_lsz_uniform_gap_self_certification"].get("actual_current_surface_status", ""),
    )
    report(
        "scalar-denominator-theorem-closure-attempt-blocked",
        scalar_denominator_closure_attempt_blocked,
        certificates["scalar_denominator_theorem_closure"].get("actual_current_surface_status", ""),
    )
    report(
        "fh-lsz-soft-continuum-threshold-no-go-blocks-ir-shortcut",
        soft_continuum_threshold_blocks,
        certificates["fh_lsz_soft_continuum_threshold"].get("actual_current_surface_status", ""),
    )
    report(
        "reflection-positivity-not-scalar-lsz-closure",
        reflection_positivity_shortcut_blocks,
        certificates["reflection_positivity_lsz_shortcut"].get("actual_current_surface_status", ""),
    )
    report(
        "effective-potential-hessian-not-source-overlap-identity",
        effective_potential_hessian_blocks,
        certificates["effective_potential_hessian_source_overlap"].get(
            "actual_current_surface_status", ""
        ),
    )
    report(
        "brst-nielsen-identities-not-higgs-pole-identity",
        brst_nielsen_higgs_identity_blocks,
        certificates["brst_nielsen_higgs_identity"].get("actual_current_surface_status", ""),
    )
    report(
        "cl3-automorphism-data-not-source-higgs-identity",
        cl3_automorphism_source_identity_blocks,
        certificates["cl3_automorphism_source_identity"].get("actual_current_surface_status", ""),
    )
    report(
        "same-source-pole-data-sufficiency-gate-not-passed",
        same_source_pole_data_sufficiency_not_passed,
        certificates["same_source_pole_data_sufficiency"].get("actual_current_surface_status", ""),
    )
    report(
        "source-functional-lsz-identifiability-blocks-source-only-closure",
        source_functional_lsz_identifiability_blocks,
        certificates["source_functional_lsz_identifiability"].get("actual_current_surface_status", ""),
    )
    report(
        "isolated-pole-gram-factorization-exact-support-not-closure",
        isolated_pole_gram_factorization_support,
        certificates["isolated_pole_gram_factorization"].get("actual_current_surface_status", ""),
    )
    report(
        "osp-oh-assumption-route-audit-blocks-overclaim",
        osp_oh_assumption_route_audit_blocks,
        certificates["osp_oh_assumption_route_audit"].get("actual_current_surface_status", ""),
    )
    report(
        "osp-oh-literature-bridge-context-not-closure",
        osp_oh_literature_bridge_not_closure,
        certificates["osp_oh_literature_bridge"].get("actual_current_surface_status", ""),
    )
    report(
        "fms-oh-certificate-construction-attempt-blocks-current-surface",
        fms_oh_certificate_construction_attempt_blocks,
        certificates["fms_oh_certificate_construction_attempt"].get(
            "actual_current_surface_status", ""
        ),
    )
    report(
        "action-first-oh-artifact-attempt-blocks-current-surface",
        action_first_oh_artifact_attempt_blocks,
        certificates["pr230_action_first_oh_artifact_attempt"].get(
            "actual_current_surface_status", ""
        ),
    )
    report(
        "holonomic-source-response-gate-blocks-missing-oh-h-source",
        holonomic_source_response_gate_blocks,
        certificates["pr230_holonomic_source_response_feasibility_gate"].get(
            "actual_current_surface_status", ""
        ),
    )
    report(
        "oh-source-higgs-authority-rescan-finds-no-current-certificate",
        oh_source_higgs_authority_rescan_blocks,
        certificates["pr230_oh_source_higgs_authority_rescan_gate"].get(
            "actual_current_surface_status", ""
        ),
    )
    report(
        "minimal-axioms-yukawa-summary-firewall-blocks-hidden-summary-authority",
        minimal_axioms_yukawa_summary_firewall_blocks,
        certificates["pr230_minimal_axioms_yukawa_summary_firewall"].get(
            "actual_current_surface_status", ""
        ),
    )
    report(
        "genuine-source-pole-artifact-support-only",
        genuine_source_pole_artifact_support_only,
        certificates["pr230_genuine_source_pole_artifact_intake"].get(
            "actual_current_surface_status", ""
        ),
    )
    report(
        "completed-l12-chunk-compute-status-support-only",
        l12_chunk_compute_status_support_only,
        certificates["pr230_l12_chunk_compute_status"].get(
            "actual_current_surface_status", ""
        ),
    )
    report(
        "negative-route-applicability-review-preserves-future-reopen",
        negative_route_applicability_review_passed,
        certificates["pr230_negative_route_applicability_review"].get(
            "actual_current_surface_status", ""
        ),
    )
    report(
        "taste-condensate-oh-bridge-blocks-current-shortcut",
        taste_condensate_oh_bridge_blocks_shortcut,
        certificates["pr230_taste_condensate_oh_bridge_audit"].get(
            "actual_current_surface_status", ""
        ),
    )
    report(
        "source-coordinate-transport-blocks-current-shortcut",
        source_coordinate_transport_blocks_current_shortcut,
        certificates["pr230_source_coordinate_transport_gate"].get(
            "actual_current_surface_status", ""
        ),
    )
    report(
        "origin-main-composite-higgs-intake-not-closure",
        origin_main_composite_higgs_intake_not_closure,
        certificates["pr230_origin_main_composite_higgs_intake_guard"].get(
            "actual_current_surface_status", ""
        ),
    )
    report(
        "origin-main-ew-m-residual-intake-not-closure",
        origin_main_ew_m_residual_intake_not_closure,
        certificates["pr230_origin_main_ew_m_residual_intake_guard"].get(
            "actual_current_surface_status", ""
        ),
    )
    report(
        "z3-triplet-conditional-primitive-support-not-closure",
        z3_triplet_conditional_primitive_not_closure,
        certificates["pr230_z3_triplet_conditional_primitive_cone"].get(
            "actual_current_surface_status", ""
        ),
    )
    report(
        "z3-triplet-positive-cone-h2-support-not-transfer",
        z3_triplet_positive_cone_h2_support_not_transfer,
        certificates["pr230_z3_triplet_positive_cone_support"].get(
            "actual_current_surface_status", ""
        ),
    )
    report(
        "z3-generation-action-lift-not-derived",
        z3_generation_action_lift_not_derived,
        certificates["pr230_z3_generation_action_lift_attempt"].get(
            "actual_current_surface_status", ""
        ),
    )
    report(
        "z3-lazy-transfer-promotion-not-derived",
        z3_lazy_transfer_promotion_not_derived,
        certificates["pr230_z3_lazy_transfer_promotion_attempt"].get(
            "actual_current_surface_status", ""
        ),
    )
    report(
        "z3-lazy-selector-no-go-blocks-current-shortcut",
        z3_lazy_selector_no_go_blocks,
        certificates["pr230_z3_lazy_selector_no_go"].get(
            "actual_current_surface_status", ""
        ),
    )
    report(
        "same-surface-z3-taste-triplet-support-not-closure",
        same_surface_z3_taste_triplet_support_not_closure,
        certificates["pr230_same_surface_z3_taste_triplet"].get(
            "actual_current_surface_status", ""
        ),
    )
    report(
        "source-coordinate-transport-current-surface-closed",
        source_coordinate_transport_completion_blocks,
        certificates["pr230_source_coordinate_transport_completion"].get(
            "actual_current_surface_status", ""
        ),
    )
    report(
        "two-source-taste-radial-chart-support-not-closure",
        two_source_taste_radial_chart_support_not_closure,
        certificates["pr230_two_source_taste_radial_chart"].get(
            "actual_current_surface_status", ""
        ),
    )
    report(
        "two-source-taste-radial-action-support-not-closure",
        two_source_taste_radial_action_support_not_closure,
        certificates["pr230_two_source_taste_radial_action"].get(
            "actual_current_surface_status", ""
        ),
    )
    report(
        "two-source-taste-radial-row-contract-support-not-closure",
        two_source_taste_radial_row_contract_support_not_closure,
        certificates["pr230_two_source_taste_radial_row_contract"].get(
            "actual_current_surface_status", ""
        ),
    )
    report(
        "two-source-taste-radial-row-production-manifest-support-not-closure",
        two_source_taste_radial_row_manifest_support_not_closure,
        certificates["pr230_two_source_taste_radial_row_production_manifest"].get(
            "actual_current_surface_status", ""
        ),
    )
    report(
        "two-source-taste-radial-row-combiner-support-not-closure",
        two_source_taste_radial_row_combiner_support_not_closure,
        certificates["pr230_two_source_taste_radial_row_combiner_gate"].get(
            "actual_current_surface_status", ""
        ),
    )
    report(
        "two-source-taste-radial-schur-subblock-support-not-closure",
        two_source_taste_radial_schur_subblock_support_not_closure,
        certificates["pr230_two_source_taste_radial_schur_subblock_witness"].get(
            "actual_current_surface_status", ""
        ),
    )
    report(
        "two-source-taste-radial-kprime-finite-shell-scout-not-closure",
        two_source_taste_radial_kprime_scout_not_closure,
        certificates[
            "pr230_two_source_taste_radial_schur_kprime_finite_shell_scout"
        ].get("actual_current_surface_status", ""),
    )
    report(
        "two-source-taste-radial-schur-abc-finite-rows-not-closure",
        two_source_taste_radial_schur_abc_finite_rows_not_closure,
        certificates[
            "pr230_two_source_taste_radial_schur_abc_finite_rows"
        ].get("actual_current_surface_status", ""),
    )
    report(
        "two-source-taste-radial-schur-pole-lift-gate-blocks-endpoint-promotion",
        two_source_taste_radial_schur_pole_lift_gate_blocks_endpoint_promotion,
        certificates[
            "pr230_two_source_taste_radial_schur_pole_lift_gate"
        ].get("actual_current_surface_status", ""),
    )
    report(
        "two-source-taste-radial-primitive-transfer-candidate-not-h3",
        two_source_taste_radial_primitive_transfer_candidate_not_h3,
        certificates[
            "pr230_two_source_taste_radial_primitive_transfer_candidate_gate"
        ].get("actual_current_surface_status", ""),
    )
    report(
        "orthogonal-top-coupling-exclusion-candidate-rejected",
        orthogonal_top_coupling_exclusion_candidate_rejected,
        certificates[
            "pr230_orthogonal_top_coupling_exclusion_candidate_gate"
        ].get("actual_current_surface_status", ""),
    )
    report(
        "strict-scalar-lsz-moment-fv-authority-absent",
        strict_scalar_lsz_moment_fv_authority_absent,
        certificates[
            "pr230_strict_scalar_lsz_moment_fv_authority_gate"
        ].get("actual_current_surface_status", ""),
    )
    report(
        "schur-complement-stieltjes-repair-support-not-closure",
        schur_complement_stieltjes_repair_support_not_closure,
        certificates[
            "pr230_schur_complement_stieltjes_repair_gate"
        ].get("actual_current_surface_status", ""),
    )
    report(
        "schur-complement-complete-monotonicity-support-not-closure",
        schur_complement_complete_monotonicity_support_not_closure,
        certificates[
            "pr230_schur_complement_complete_monotonicity_gate"
        ].get("actual_current_surface_status", ""),
    )
    report(
        "schur-x-given-source-one-pole-scout-not-authority",
        schur_x_given_source_one_pole_scout_not_authority,
        certificates[
            "pr230_schur_x_given_source_one_pole_scout"
        ].get("actual_current_surface_status", ""),
    )
    report(
        "pr230-two-source-taste-radial-chunk-package-support-not-closure",
        two_source_taste_radial_chunk_package_support_not_closure,
        certificates["pr230_two_source_taste_radial_chunk_package"].get(
            "actual_current_surface_status", ""
        ),
    )
    report(
        "pr230-source-higgs-pole-row-contract-open",
        source_higgs_pole_row_contract_open,
        certificates["pr230_source_higgs_pole_row_acceptance_contract"].get(
            "actual_current_surface_status", ""
        ),
    )
    report(
        "taste-radial-canonical-oh-selector-blocks-symmetry-shortcut",
        taste_radial_canonical_oh_selector_blocks_symmetry_shortcut,
        certificates["pr230_taste_radial_canonical_oh_selector_gate"].get(
            "actual_current_surface_status", ""
        ),
    )
    report(
        "degree-one-higgs-action-premise-not-derived",
        degree_one_higgs_action_premise_not_derived,
        certificates["pr230_degree_one_higgs_action_premise_gate"].get(
            "actual_current_surface_status", ""
        ),
    )
    report(
        "degree-one-radial-tangent-oh-theorem-support-not-closure",
        degree_one_radial_tangent_oh_theorem_support_not_closure,
        certificates["pr230_degree_one_radial_tangent_oh_theorem"].get(
            "actual_current_surface_status", ""
        ),
    )
    report(
        "taste-radial-to-source-higgs-promotion-contract-support-not-closure",
        taste_radial_to_source_higgs_promotion_contract_support_not_closure,
        certificates["pr230_taste_radial_to_source_higgs_promotion_contract"].get(
            "actual_current_surface_status", ""
        ),
    )
    report(
        "fms-post-degree-route-rescore-support-not-closure",
        fms_post_degree_route_support_not_closure,
        certificates["pr230_fms_post_degree_route_rescore"].get(
            "actual_current_surface_status", ""
        ),
    )
    report(
        "fms-composite-oh-conditional-support-not-closure",
        fms_composite_oh_conditional_support_not_closure,
        certificates["pr230_fms_composite_oh_conditional_theorem"].get(
            "actual_current_surface_status", ""
        ),
    )
    report(
        "fms-oh-candidate-action-packet-support-not-closure",
        fms_oh_candidate_action_packet_support_not_closure,
        certificates["pr230_fms_oh_candidate_action_packet"].get(
            "actual_current_surface_status", ""
        ),
    )
    report(
        "fms-source-overlap-readout-gate-support-not-closure",
        fms_source_overlap_readout_gate_support_not_closure,
        certificates["pr230_fms_source_overlap_readout_gate"].get(
            "actual_current_surface_status", ""
        ),
    )
    report(
        "fms-action-adoption-minimal-cut-support-not-closure",
        fms_action_adoption_minimal_cut_support_not_closure,
        certificates["pr230_fms_action_adoption_minimal_cut"].get(
            "actual_current_surface_status", ""
        ),
    )
    report(
        "higgs-mass-source-action-bridge-support-not-closure",
        higgs_mass_source_action_bridge_support_not_closure,
        certificates["pr230_higgs_mass_source_action_bridge"].get(
            "actual_current_surface_status", ""
        ),
    )
    report(
        "post-fms-source-overlap-necessity-blocks-current-inference",
        post_fms_source_overlap_necessity_blocks_current_inference,
        certificates["pr230_post_fms_source_overlap_necessity_gate"].get(
            "actual_current_surface_status", ""
        ),
    )
    report(
        "source-higgs-overlap-kappa-contract-support-not-closure",
        source_higgs_overlap_kappa_contract_support_not_closure,
        certificates["pr230_source_higgs_overlap_kappa_contract"].get(
            "actual_current_surface_status", ""
        ),
    )
    report(
        "radial-spurion-action-contract-support-not-closure",
        radial_spurion_action_contract_support_not_closure,
        certificates["pr230_radial_spurion_action_contract"].get(
            "actual_current_surface_status", ""
        ),
    )
    report(
        "additive-source-radial-spurion-incompatibility-support-not-closure",
        additive_source_radial_spurion_incompatibility_support_not_closure,
        certificates["pr230_additive_source_radial_spurion_incompatibility"].get(
            "actual_current_surface_status", ""
        ),
    )
    report(
        "additive-top-subtraction-row-contract-support-not-closure",
        additive_top_subtraction_row_contract_support_not_closure,
        certificates["pr230_additive_top_subtraction_row_contract"].get(
            "actual_current_surface_status", ""
        ),
    )
    report(
        "wz-response-ratio-identifiability-contract-support-not-closure",
        wz_response_ratio_identifiability_contract_support_not_closure,
        certificates["pr230_wz_response_ratio_identifiability_contract"].get(
            "actual_current_surface_status", ""
        ),
    )
    report(
        "wz-same-source-action-minimal-certificate-cut-open",
        wz_same_source_action_minimal_certificate_cut_open,
        certificates["pr230_wz_same_source_action_minimal_certificate_cut"].get(
            "actual_current_surface_status", ""
        ),
    )
    report(
        "wz-accepted-action-response-root-checkpoint-blocks",
        wz_accepted_action_response_root_checkpoint_blocks,
        certificates["pr230_wz_accepted_action_response_root_checkpoint"].get(
            "actual_current_surface_status", ""
        ),
    )
    report(
        "canonical-oh-wz-common-action-cut-open",
        canonical_oh_wz_common_action_cut_open,
        certificates["pr230_canonical_oh_wz_common_action_cut"].get(
            "actual_current_surface_status", ""
        ),
    )
    report(
        "canonical-oh-accepted-action-stretch-blocks-current-stack",
        canonical_oh_accepted_action_stretch_blocks_current_stack,
        certificates["pr230_canonical_oh_accepted_action_stretch_attempt"].get(
            "actual_current_surface_status", ""
        ),
    )
    for idx, not_closure in two_source_taste_radial_chunk_checkpoint_not_closure.items():
        cert_key = f"pr230_two_source_taste_radial_chunk{idx:03d}_checkpoint"
        report(
            f"two-source-taste-radial-chunk{idx:03d}-checkpoint-not-closure",
            not_closure,
            certificates[cert_key].get("actual_current_surface_status", ""),
        )
    report(
        "kinetic-taste-mixing-shortcut-closed",
        kinetic_taste_mixing_bridge_blocks_shortcut,
        certificates["pr230_kinetic_taste_mixing_bridge"].get(
            "actual_current_surface_status", ""
        ),
    )
    report(
        "one-higgs-taste-axis-completeness-shortcut-closed",
        one_higgs_taste_axis_completeness_blocks_shortcut,
        certificates["pr230_one_higgs_taste_axis_completeness"].get(
            "actual_current_surface_status", ""
        ),
    )
    report(
        "action-first-route-current-surface-closed",
        action_first_route_completion_blocks,
        certificates["pr230_action_first_route_completion"].get(
            "actual_current_surface_status", ""
        ),
    )
    report(
        "wz-response-route-current-surface-closed",
        wz_response_route_completion_blocks,
        certificates["pr230_wz_response_route_completion"].get(
            "actual_current_surface_status", ""
        ),
    )
    report(
        "schur-route-current-surface-closed",
        schur_route_completion_blocks,
        certificates["pr230_schur_route_completion"].get(
            "actual_current_surface_status", ""
        ),
    )
    report(
        "neutral-primitive-route-current-surface-closed",
        neutral_primitive_route_completion_blocks,
        certificates["pr230_neutral_primitive_route_completion"].get(
            "actual_current_surface_status", ""
        ),
    )
    report(
        "oh-bridge-first-principles-candidate-portfolio-open",
        oh_bridge_candidate_portfolio_open,
        certificates["pr230_oh_bridge_candidate_portfolio"].get(
            "actual_current_surface_status", ""
        ),
    )
    report(
        "same-surface-neutral-multiplicity-one-gate-rejects-current-surface",
        same_surface_neutral_multiplicity_gate_rejects_current_surface,
        certificates["pr230_same_surface_neutral_multiplicity_one_gate"].get(
            "actual_current_surface_status", ""
        ),
    )
    report(
        "os-transfer-kernel-artifact-absent",
        os_transfer_kernel_artifact_absent,
        certificates["pr230_os_transfer_kernel_artifact_gate"].get(
            "actual_current_surface_status", ""
        ),
    )
    report(
        "source-higgs-time-kernel-harness-support-only",
        source_higgs_time_kernel_harness_support_only,
        certificates["pr230_source_higgs_time_kernel_harness_extension_gate"].get(
            "actual_current_surface_status", ""
        ),
    )
    report(
        "source-higgs-time-kernel-gevp-contract-support-only",
        source_higgs_time_kernel_gevp_contract_support_only,
        certificates["pr230_source_higgs_time_kernel_gevp_contract"].get(
            "actual_current_surface_status", ""
        ),
    )
    report(
        "source-higgs-time-kernel-production-manifest-not-evidence",
        source_higgs_time_kernel_production_manifest_not_evidence,
        certificates["pr230_source_higgs_time_kernel_production_manifest"].get(
            "actual_current_surface_status", ""
        ),
    )
    report(
        "fms-literature-source-overlap-intake-non-authority",
        fms_literature_source_overlap_intake_non_authority,
        certificates["pr230_fms_literature_source_overlap_intake"].get(
            "actual_current_surface_status", ""
        ),
    )
    report(
        "schur-higher-shell-production-contract-not-evidence",
        schur_higher_shell_production_contract_not_evidence,
        certificates["pr230_schur_higher_shell_production_contract"].get(
            "actual_current_surface_status", ""
        ),
    )
    report(
        "derived-bridge-rank-one-attempt-blocks-current-source-only-closure",
        derived_bridge_rank_one_closure_attempt_blocks,
        certificates["pr230_derived_bridge_rank_one_closure_attempt"].get(
            "actual_current_surface_status", ""
        ),
    )
    report(
        "source-sector-pattern-transfer-gate-relevant-not-closure",
        source_sector_pattern_transfer_gate_not_closure,
        certificates["pr230_source_sector_pattern_transfer_gate"].get(
            "actual_current_surface_status", ""
        ),
    )
    report(
        "det-positivity-bridge-intake-gate-relevant-not-closure",
        det_positivity_bridge_intake_gate_not_closure,
        certificates["pr230_det_positivity_bridge_intake_gate"].get(
            "actual_current_surface_status", ""
        ),
    )
    report(
        "reflection-det-primitive-upgrade-gate-blocks-combined-positivity-shortcut",
        reflection_det_primitive_upgrade_gate_blocks,
        certificates["pr230_reflection_det_primitive_upgrade_gate"].get(
            "actual_current_surface_status", ""
        ),
    )
    report(
        "complete-source-spectrum-identity-no-go-blocks",
        complete_source_spectrum_identity_no_go_blocks,
        certificates["complete_source_spectrum_identity_no_go"].get("actual_current_surface_status", ""),
    )
    report(
        "neutral-scalar-top-coupling-tomography-gate-blocks",
        neutral_scalar_top_coupling_tomography_gate_blocks,
        certificates["neutral_scalar_top_coupling_tomography_gate"].get("actual_current_surface_status", ""),
    )
    report(
        "non-source-response-rank-repair-sufficiency-not-closure",
        non_source_response_rank_repair_sufficiency_not_closure,
        certificates["non_source_response_rank_repair_sufficiency"].get("actual_current_surface_status", ""),
    )
    report(
        "positivity-improving-neutral-scalar-rank-one-conditional-support-not-closure",
        positivity_improving_neutral_scalar_rank_one_conditional,
        certificates["positivity_improving_neutral_scalar_rank_one"].get("actual_current_surface_status", ""),
    )
    report(
        "gauge-perron-neutral-scalar-rank-one-import-blocked",
        gauge_perron_neutral_scalar_import_blocks,
        certificates["gauge_perron_neutral_scalar_rank_one_import"].get("actual_current_surface_status", ""),
    )
    report(
        "neutral-scalar-positivity-improving-direct-theorem-not-derived",
        neutral_scalar_positivity_improving_direct_blocks,
        certificates["neutral_scalar_positivity_improving_direct_closure"].get("actual_current_surface_status", ""),
    )
    report(
        "neutral-scalar-irreducibility-authority-absent",
        neutral_scalar_irreducibility_authority_absent,
        certificates["neutral_scalar_irreducibility_authority_audit"].get("actual_current_surface_status", ""),
    )
    report(
        "neutral-scalar-primitive-cone-certificate-gate-absent",
        neutral_scalar_primitive_cone_certificate_absent,
        certificates["neutral_scalar_primitive_cone_certificate_gate"].get(
            "actual_current_surface_status", ""
        ),
    )
    report(
        "neutral-scalar-primitive-cone-stretch-no-go-blocks",
        neutral_scalar_primitive_cone_stretch_blocks,
        certificates["neutral_scalar_primitive_cone_stretch_no_go"].get(
            "actual_current_surface_status", ""
        ),
    )
    report(
        "neutral-scalar-burnside-irreducibility-attempt-blocks-source-only-generators",
        neutral_scalar_burnside_irreducibility_blocks,
        certificates["neutral_scalar_burnside_irreducibility_attempt"].get(
            "actual_current_surface_status", ""
        ),
    )
    report(
        "neutral-offdiagonal-generator-derivation-attempt-blocks-current-surface",
        neutral_offdiagonal_generator_derivation_blocks,
        certificates["neutral_offdiagonal_generator_derivation_attempt"].get(
            "actual_current_surface_status", ""
        ),
    )
    report(
        "logdet-hessian-neutral-mixing-blocks-source-only-determinant-route",
        logdet_hessian_neutral_mixing_blocks,
        certificates["pr230_logdet_hessian_neutral_mixing_attempt"].get(
            "actual_current_surface_status", ""
        ),
    )
    report(
        "scalar-carrier-projector-closure-attempt-blocked",
        scalar_carrier_projector_closure_blocked,
        certificates["scalar_carrier_projector_closure"].get("actual_current_surface_status", ""),
    )
    report(
        "kprime-closure-attempt-blocked",
        kprime_closure_blocked,
        certificates["kprime_closure"].get("actual_current_surface_status", ""),
    )
    report(
        "pr230-matching-running-bridge-gate-open",
        matching_running_bridge_gate_open,
        certificates["pr230_matching_running_bridge_gate"].get("actual_current_surface_status", ""),
    )
    report(
        "schur-complement-kprime-sufficiency-not-closure",
        schur_complement_kprime_sufficiency_not_closure,
        certificates["schur_complement_kprime_sufficiency"].get("actual_current_surface_status", ""),
    )
    report(
        "schur-kprime-row-absence-guard-blocks-source-only-import",
        schur_kprime_row_absence_guard_blocks_source_only_import,
        certificates["schur_kprime_row_absence_guard"].get("actual_current_surface_status", ""),
    )
    report(
        "legacy-schur-bridge-import-audit-blocks-hidden-closure",
        legacy_schur_bridge_import_audit_blocks_hidden_closure,
        certificates["legacy_schur_bridge_import_audit"].get("actual_current_surface_status", ""),
    )
    report(
        "schur-kernel-row-contract-gate-not-passed",
        schur_kernel_row_contract_gate_not_passed,
        certificates["schur_kernel_row_contract_gate"].get("actual_current_surface_status", ""),
    )
    report(
        "schur-row-candidate-extraction-blocks-finite-support-import",
        schur_row_candidate_extraction_blocks_finite_support_import,
        certificates["schur_row_candidate_extraction_attempt"].get("actual_current_surface_status", ""),
    )
    report(
        "schur-compressed-denominator-bootstrap-blocks-hidden-rows",
        schur_compressed_denominator_bootstrap_blocks_hidden_rows,
        certificates["schur_compressed_denominator_row_bootstrap_no_go"].get(
            "actual_current_surface_status", ""
        ),
    )
    report(
        "schur-abc-definition-derivation-blocks-current-surface",
        schur_abc_definition_derivation_blocks_current_surface,
        certificates["pr230_schur_abc_definition_derivation_attempt"].get(
            "actual_current_surface_status", ""
        ),
    )
    report(
        "fh-lsz-higgs-pole-identity-gate-blocks",
        higgs_pole_identity_gate_blocks,
        certificates["fh_lsz_higgs_pole_identity"].get("actual_current_surface_status", ""),
    )
    report(
        "fh-gauge-normalized-response-not-closure",
        gauge_normalized_response_not_closure,
        certificates["fh_gauge_normalized_response"].get("actual_current_surface_status", ""),
    )
    report(
        "fh-gauge-mass-response-observable-gap-blocks",
        gauge_mass_response_observable_gap_blocks,
        certificates["fh_gauge_mass_response_observable_gap"].get("actual_current_surface_status", ""),
    )
    report(
        "fh-gauge-mass-response-manifest-not-evidence",
        gauge_mass_response_manifest_not_evidence,
        certificates["fh_gauge_mass_response_manifest"].get("actual_current_surface_status", ""),
    )
    report(
        "fh-gauge-mass-response-builder-rows-absent",
        gauge_mass_response_builder_rows_absent,
        certificates["fh_gauge_mass_response_certificate_builder"].get("actual_current_surface_status", ""),
    )
    report(
        "same-source-wz-response-certificate-gate-blocks",
        same_source_wz_response_certificate_gate_blocks,
        certificates["same_source_wz_response_certificate_gate"].get("actual_current_surface_status", ""),
    )
    report(
        "wz-response-harness-absence-guard-not-evidence",
        wz_response_harness_absence_guard_not_evidence,
        certificates["wz_response_harness_absence_guard"].get("actual_current_surface_status", ""),
    )
    report(
        "wz-response-repo-harness-import-audit-blocks-hidden-harness",
        wz_response_repo_harness_import_audit_blocks_hidden_harness,
        certificates["wz_response_repo_harness_import_audit"].get("actual_current_surface_status", ""),
    )
    report(
        "wz-response-measurement-row-contract-not-evidence",
        wz_response_measurement_row_contract_not_evidence,
        certificates["wz_response_measurement_row_contract_gate"].get("actual_current_surface_status", ""),
    )
    report(
        "wz-response-row-production-attempt-blocks-current-surface",
        wz_response_row_production_attempt_blocks_current_surface,
        certificates["wz_response_row_production_attempt"].get("actual_current_surface_status", ""),
    )
    report(
        "wz-response-harness-implementation-plan-support-only",
        wz_response_harness_implementation_plan_support_only,
        certificates["wz_response_harness_implementation_plan"].get("actual_current_surface_status", ""),
    )
    report(
        "wz-harness-smoke-schema-support-only",
        wz_harness_smoke_schema_support_only,
        certificates["wz_harness_smoke_schema"].get("actual_current_surface_status", ""),
    )
    report(
        "wz-smoke-to-production-promotion-no-go-blocks",
        wz_smoke_to_production_promotion_no_go_blocks,
        certificates["wz_smoke_to_production_promotion_no_go"].get(
            "actual_current_surface_status", ""
        ),
    )
    report(
        "wz-same-source-ew-action-certificate-builder-blocks",
        wz_same_source_ew_action_certificate_builder_blocks,
        certificates["wz_same_source_ew_action_certificate_builder"].get("actual_current_surface_status", ""),
    )
    report(
        "wz-same-source-ew-action-gate-blocks",
        wz_same_source_ew_action_gate_blocks,
        certificates["wz_same_source_ew_action_gate"].get("actual_current_surface_status", ""),
    )
    report(
        "wz-same-source-ew-action-semantic-firewall-not-closure",
        wz_same_source_ew_action_semantic_firewall_not_closure,
        certificates["wz_same_source_ew_action_semantic_firewall"].get("actual_current_surface_status", ""),
    )
    report(
        "wz-source-coordinate-transport-no-go-blocks",
        wz_source_coordinate_transport_no_go_blocks,
        certificates["wz_source_coordinate_transport_no_go"].get("actual_current_surface_status", ""),
    )
    report(
        "wz-goldstone-equivalence-source-identity-no-go-blocks",
        wz_goldstone_equivalence_source_identity_no_go_blocks,
        certificates["wz_goldstone_equivalence_source_identity_no_go"].get(
            "actual_current_surface_status", ""
        ),
    )
    report(
        "same-source-w-response-decomposition-not-closure",
        same_source_w_response_decomposition_not_closure,
        certificates["same_source_w_response_decomposition"].get("actual_current_surface_status", ""),
    )
    report(
        "same-source-w-response-orthogonal-correction-gate-blocks",
        same_source_w_response_orthogonal_correction_gate_blocks,
        certificates["same_source_w_response_orthogonal_correction"].get("actual_current_surface_status", ""),
    )
    report(
        "one-higgs-completeness-orthogonal-null-premise-absent",
        one_higgs_completeness_orthogonal_null_premise_absent,
        certificates["one_higgs_completeness_orthogonal_null"].get("actual_current_surface_status", ""),
    )
    report(
        "same-source-w-response-lightweight-readout-open",
        same_source_w_response_lightweight_readout_open,
        certificates["same_source_w_response_lightweight_readout"].get("actual_current_surface_status", ""),
    )
    report(
        "delta-perp-tomography-correction-builder-open",
        delta_perp_tomography_correction_builder_open,
        certificates["delta_perp_tomography_correction_builder"].get("actual_current_surface_status", ""),
    )
    report(
        "same-source-w-response-row-builder-open",
        same_source_w_response_row_builder_open,
        certificates["same_source_w_response_row_builder"].get("actual_current_surface_status", ""),
    )
    report(
        "same-source-top-response-builder-open",
        same_source_top_response_builder_open,
        certificates["same_source_top_response_builder"].get("actual_current_surface_status", ""),
    )
    report(
        "same-source-top-response-identity-builder-open",
        same_source_top_response_identity_builder_open,
        certificates["same_source_top_response_identity_builder"].get("actual_current_surface_status", ""),
    )
    report(
        "top-wz-matched-covariance-builder-open",
        top_wz_matched_covariance_builder_open,
        certificates["top_wz_matched_covariance_builder"].get("actual_current_surface_status", ""),
    )
    report(
        "top-wz-covariance-marginal-derivation-no-go-blocks",
        top_wz_covariance_marginal_derivation_no_go_blocks,
        certificates["top_wz_covariance_marginal_derivation_no_go"].get("actual_current_surface_status", ""),
    )
    report(
        "top-wz-factorization-independence-gate-blocks",
        top_wz_factorization_independence_gate_blocks,
        certificates["top_wz_factorization_independence_gate"].get("actual_current_surface_status", ""),
    )
    report(
        "top-wz-deterministic-response-covariance-gate-blocks",
        top_wz_deterministic_response_covariance_gate_blocks,
        certificates["top_wz_deterministic_response_covariance_gate"].get("actual_current_surface_status", ""),
    )
    report(
        "top-wz-covariance-theorem-import-audit-blocks",
        top_wz_covariance_theorem_import_audit_blocks,
        certificates["top_wz_covariance_theorem_import_audit"].get("actual_current_surface_status", ""),
    )
    report(
        "wz-correlator-mass-fit-path-gate-blocks",
        wz_correlator_mass_fit_path_gate_blocks,
        certificates["wz_correlator_mass_fit_path_gate"].get("actual_current_surface_status", ""),
    )
    report(
        "wz-mass-fit-response-row-builder-open",
        wz_mass_fit_response_row_builder_open,
        certificates["wz_mass_fit_response_row_builder"].get("actual_current_surface_status", ""),
    )
    report(
        "electroweak-g2-certificate-builder-open",
        electroweak_g2_certificate_builder_open,
        certificates["electroweak_g2_certificate_builder"].get("actual_current_surface_status", ""),
    )
    report(
        "wz-g2-generator-casimir-normalization-no-go-blocks",
        wz_g2_generator_casimir_normalization_no_go_blocks,
        certificates["wz_g2_generator_casimir_normalization_no_go"].get(
            "actual_current_surface_status", ""
        ),
    )
    report(
        "wz-g2-authority-firewall-blocks",
        wz_g2_authority_firewall_blocks,
        certificates["wz_g2_authority_firewall"].get("actual_current_surface_status", ""),
    )
    report(
        "wz-g2-response-self-normalization-no-go-blocks",
        wz_g2_response_self_normalization_no_go_blocks,
        certificates["wz_g2_response_self_normalization_no_go"].get(
            "actual_current_surface_status", ""
        ),
    )
    report(
        "wz-g2-bare-running-bridge-attempt-blocks",
        wz_g2_bare_running_bridge_attempt_blocks,
        certificates["pr230_wz_g2_bare_running_bridge_attempt"].get(
            "actual_current_surface_status", ""
        ),
    )
    report(
        "same-source-sector-overlap-identity-blocks",
        same_source_sector_overlap_identity_blocks,
        certificates["same_source_sector_overlap_identity"].get("actual_current_surface_status", ""),
    )
    report(
        "source-pole-canonical-higgs-mixing-blocks",
        source_pole_canonical_higgs_mixing_blocks,
        certificates["source_pole_canonical_higgs_mixing"].get("actual_current_surface_status", ""),
    )
    report(
        "osp-oh-identity-stretch-blocks",
        osp_oh_identity_stretch_blocks,
        certificates["osp_oh_identity_stretch"].get("actual_current_surface_status", ""),
    )
    report(
        "source-pole-purity-cross-correlator-gate-blocks",
        source_pole_purity_cross_correlator_gate_blocks,
        certificates["source_pole_purity_cross_correlator"].get("actual_current_surface_status", ""),
    )
    report(
        "source-higgs-cross-correlator-manifest-not-evidence",
        source_higgs_cross_correlator_manifest_not_evidence,
        certificates["source_higgs_cross_correlator_manifest"].get("actual_current_surface_status", ""),
    )
    report(
        "source-higgs-cross-correlator-import-blocks",
        source_higgs_cross_correlator_import_blocks,
        certificates["source_higgs_cross_correlator_import"].get("actual_current_surface_status", ""),
    )
    report(
        "source-higgs-gram-purity-gate-blocks",
        source_higgs_gram_purity_gate_blocks,
        certificates["source_higgs_gram_purity_gate"].get("actual_current_surface_status", ""),
    )
    report(
        "source-higgs-cross-correlator-harness-extension-not-evidence",
        source_higgs_harness_extension_not_evidence,
        certificates["source_higgs_cross_correlator_harness_extension"].get("actual_current_surface_status", ""),
    )
    report(
        "source-higgs-pole-residue-extractor-awaits-valid-production-rows",
        source_higgs_pole_residue_extractor_not_evidence,
        certificates["source_higgs_pole_residue_extractor"].get("actual_current_surface_status", ""),
    )
    report(
        "source-higgs-cross-correlator-builder-rows-absent",
        source_higgs_builder_rows_absent,
        certificates["source_higgs_cross_correlator_certificate_builder"].get("actual_current_surface_status", ""),
    )
    report(
        "osp-higgs-gram-purity-postprocessor-waits",
        source_higgs_osp_postprocessor_waits,
        certificates["source_higgs_gram_purity_postprocessor"].get("actual_current_surface_status", ""),
    )
    report(
        "source-higgs-gram-purity-contract-witness-not-evidence",
        source_higgs_gram_purity_contract_witness_not_evidence,
        certificates["source_higgs_gram_purity_contract_witness"].get("actual_current_surface_status", ""),
    )
    report(
        "source-higgs-production-readiness-blocks-launch",
        source_higgs_production_readiness_blocks_launch,
        certificates["source_higgs_production_readiness_gate"].get("actual_current_surface_status", ""),
    )
    report(
        "canonical-higgs-operator-semantic-firewall-not-closure",
        canonical_higgs_operator_semantic_firewall_not_closure,
        certificates["canonical_higgs_operator_semantic_firewall"].get("actual_current_surface_status", ""),
    )
    report(
        "canonical-higgs-operator-realization-gate-blocks",
        canonical_higgs_operator_realization_gate_blocks,
        certificates["canonical_higgs_operator_realization_gate"].get("actual_current_surface_status", ""),
    )
    report(
        "canonical-higgs-operator-certificate-gate-blocks",
        canonical_higgs_operator_certificate_gate_blocks,
        certificates["canonical_higgs_operator_certificate_gate"].get("actual_current_surface_status", ""),
    )
    report(
        "canonical-higgs-repo-authority-audit-blocks-hidden-oh",
        canonical_higgs_repo_authority_audit_blocks_hidden_oh,
        certificates["canonical_higgs_repo_authority_audit"].get("actual_current_surface_status", ""),
    )
    report(
        "cross-lane-oh-authority-audit-blocks-adjacent-imports",
        cross_lane_oh_authority_audit_blocks_adjacent_imports,
        certificates["cross_lane_oh_authority_audit"].get("actual_current_surface_status", ""),
    )
    report(
        "sm-one-higgs-oh-import-boundary-blocks-shortcut",
        sm_one_higgs_oh_import_boundary_blocks_shortcut,
        certificates["sm_one_higgs_oh_import_boundary"].get("actual_current_surface_status", ""),
    )
    report(
        "canonical-higgs-operator-candidate-stress-blocks",
        canonical_higgs_operator_candidate_stress_blocks,
        certificates["canonical_higgs_operator_candidate_stress"].get("actual_current_surface_status", ""),
    )
    report(
        "hunit-canonical-higgs-operator-candidate-gate-blocks",
        hunit_canonical_higgs_operator_candidate_gate_blocks,
        certificates["hunit_canonical_higgs_operator_candidate_gate"].get("actual_current_surface_status", ""),
    )
    report(
        "source-higgs-harness-absence-guard-not-evidence",
        source_higgs_harness_absence_guard_not_evidence,
        certificates["source_higgs_harness_absence_guard"].get("actual_current_surface_status", ""),
    )
    report(
        "source-higgs-unratified-operator-smoke-not-evidence",
        source_higgs_unratified_operator_smoke_not_evidence,
        certificates["source_higgs_unratified_operator_smoke"].get("actual_current_surface_status", ""),
    )
    report(
        "source-higgs-unratified-gram-shortcut-no-go-blocks",
        source_higgs_unratified_gram_shortcut_no_go_blocks,
        certificates["source_higgs_unratified_gram_shortcut_no_go"].get("actual_current_surface_status", ""),
    )
    report(
        "neutral-scalar-rank-one-purity-gate-blocks",
        neutral_scalar_rank_one_purity_gate_blocks,
        certificates["neutral_scalar_rank_one_purity_gate"].get("actual_current_surface_status", ""),
    )
    report(
        "neutral-scalar-commutant-rank-no-go-blocks",
        neutral_scalar_commutant_rank_no_go_blocks,
        certificates["neutral_scalar_commutant_rank_no_go"].get("actual_current_surface_status", ""),
    )
    report(
        "neutral-scalar-dynamical-rank-one-closure-blocks",
        neutral_scalar_dynamical_rank_one_closure_blocks,
        certificates["neutral_scalar_dynamical_rank_one_closure"].get("actual_current_surface_status", ""),
    )
    report(
        "orthogonal-neutral-decoupling-no-go-blocks",
        orthogonal_neutral_decoupling_no_go_blocks,
        certificates["orthogonal_neutral_decoupling_no_go"].get("actual_current_surface_status", ""),
    )
    report(
        "fh-gauge-response-mixed-scalar-blocks",
        fh_gauge_response_mixed_scalar_blocks,
        certificates["fh_gauge_response_mixed_scalar"].get("actual_current_surface_status", ""),
    )
    report(
        "no-orthogonal-top-coupling-import-blocks",
        no_orthogonal_top_coupling_import_blocks,
        certificates["no_orthogonal_top_coupling_import"].get("actual_current_surface_status", ""),
    )
    report(
        "no-orthogonal-top-coupling-selection-rule-blocks",
        no_orthogonal_top_coupling_selection_rule_blocks,
        certificates["no_orthogonal_top_coupling_selection_rule"].get("actual_current_surface_status", ""),
    )
    report(
        "d17-source-pole-identity-closure-blocked",
        d17_source_pole_identity_closure_blocked,
        certificates["d17_source_pole_identity_closure"].get("actual_current_surface_status", ""),
    )
    report(
        "source-overlap-sum-rule-no-go-blocks",
        source_overlap_sum_rule_no_go_blocks,
        certificates["source_overlap_sum_rule_no_go"].get("actual_current_surface_status", ""),
    )
    report(
        "short-distance-ope-lsz-no-go-blocks",
        short_distance_ope_lsz_no_go_blocks,
        certificates["short_distance_ope_lsz_no_go"].get("actual_current_surface_status", ""),
    )
    report(
        "effective-mass-plateau-residue-no-go-blocks",
        effective_mass_plateau_residue_no_go_blocks,
        certificates["effective_mass_plateau_residue_no_go"].get("actual_current_surface_status", ""),
    )
    report(
        "finite-source-shift-derivative-no-go-blocks",
        finite_source_shift_derivative_no_go_blocks,
        certificates["finite_source_shift_derivative_no_go"].get("actual_current_surface_status", ""),
    )
    report(
        "fh-lsz-finite-source-linearity-gate-not-closure",
        finite_source_linearity_gate_not_closure,
        certificates["fh_lsz_finite_source_linearity_gate"].get("actual_current_surface_status", ""),
    )
    report(
        "fh-lsz-finite-source-linearity-calibration-not-closure",
        finite_source_linearity_calibration_not_closure,
        certificates["fh_lsz_finite_source_linearity_calibration"].get("actual_current_surface_status", ""),
    )
    report(
        "fh-lsz-target-observable-ess-certificate-not-closure",
        target_observable_ess_not_closure,
        certificates["fh_lsz_target_observable_ess"].get("actual_current_surface_status", ""),
    )
    report(
        "fh-lsz-autocorrelation-ess-gate-not-closure",
        autocorrelation_ess_gate_not_closure,
        certificates["fh_lsz_autocorrelation_ess_gate"].get("actual_current_surface_status", ""),
    )
    report(
        "fh-lsz-response-window-forensics-not-closure",
        response_window_forensics_not_closure,
        certificates["fh_lsz_response_window_forensics"].get("actual_current_surface_status", ""),
    )
    report(
        "fh-lsz-common-window-response-provenance-not-closure",
        common_window_response_provenance_not_closure,
        certificates["fh_lsz_common_window_response_provenance"].get(
            "actual_current_surface_status", ""
        ),
    )
    report(
        "fh-lsz-common-window-pooled-response-estimator-not-closure",
        common_window_pooled_response_estimator_not_closure,
        certificates["fh_lsz_common_window_pooled_response_estimator"].get(
            "actual_current_surface_status", ""
        ),
    )
    report(
        "fh-lsz-common-window-replacement-response-stability-not-closure",
        common_window_replacement_response_stability_not_closure,
        certificates["fh_lsz_common_window_replacement_response_stability"].get(
            "actual_current_surface_status", ""
        ),
    )
    report(
        "fh-lsz-common-window-response-gate-not-closure",
        common_window_response_gate_not_closure,
        certificates["fh_lsz_common_window_response_gate"].get(
            "actual_current_surface_status", ""
        ),
    )
    report(
        "fh-lsz-v2-target-response-stability-not-closure",
        v2_target_response_stability_not_closure,
        certificates["fh_lsz_v2_target_response_stability"].get("actual_current_surface_status", ""),
    )
    report(
        "fh-lsz-response-window-acceptance-gate-blocks",
        response_window_acceptance_gate_blocks,
        certificates["fh_lsz_response_window_acceptance_gate"].get("actual_current_surface_status", ""),
    )
    report(
        "fh-lsz-target-timeseries-replacement-queue-not-closure",
        target_timeseries_replacement_queue_not_closure,
        certificates["fh_lsz_target_timeseries_replacement_queue"].get("actual_current_surface_status", ""),
    )
    report(
        "fh-lsz-target-timeseries-full-set-checkpoint-not-closure",
        target_timeseries_full_set_checkpoint_not_closure,
        certificates["fh_lsz_target_timeseries_full_set_checkpoint"].get("actual_current_surface_status", ""),
    )
    report(
        "fh-lsz-target-timeseries-harness-support-not-evidence",
        target_timeseries_harness_support_not_evidence,
        certificates["fh_lsz_target_timeseries_harness"].get("actual_current_surface_status", ""),
    )
    report(
        "fh-lsz-multitau-target-timeseries-harness-support-not-evidence",
        multitau_target_timeseries_harness_support_not_evidence,
        certificates["fh_lsz_multitau_target_timeseries_harness"].get(
            "actual_current_surface_status", ""
        ),
    )
    report(
        "fh-lsz-selected-mass-normal-cache-speedup-not-evidence",
        selected_mass_normal_cache_speedup_not_evidence,
        certificates["fh_lsz_selected_mass_normal_cache_speedup"].get("actual_current_surface_status", ""),
    )
    report(
        "top-mass-scan-response-harness-support-not-evidence",
        top_mass_scan_response_harness_support_not_evidence,
        certificates["top_mass_scan_response_harness_gate"].get(
            "actual_current_surface_status", ""
        ),
    )
    report(
        "fh-lsz-global-production-collision-guard-not-evidence",
        global_production_collision_guard_not_evidence,
        certificates["fh_lsz_global_production_collision_guard"].get("actual_current_surface_status", ""),
    )
    report(
        "fh-lsz-target-timeseries-higgs-identity-no-go-blocks",
        target_timeseries_higgs_identity_no_go_blocks,
        certificates["fh_lsz_target_timeseries_higgs_identity_no_go"].get("actual_current_surface_status", ""),
    )
    report(
        "higgs-pole-identity-latest-blocker-blocks",
        higgs_pole_identity_latest_blocker_blocks,
        certificates["higgs_pole_identity_latest_blocker"].get("actual_current_surface_status", ""),
    )
    report(
        "fh-lsz-pole-fit-mode-budget-not-closure",
        pole_fit_mode_budget_not_closure,
        certificates["fh_lsz_pole_fit_mode_budget"].get("actual_current_surface_status", ""),
    )
    report(
        "fh-lsz-eight-mode-noise-variance-not-closure",
        eight_mode_noise_variance_not_closure,
        certificates["fh_lsz_eight_mode_noise_variance"].get("actual_current_surface_status", ""),
    )
    report(
        "fh-lsz-noise-subsample-diagnostics-not-closure",
        noise_subsample_diagnostics_not_closure,
        certificates["fh_lsz_noise_subsample_diagnostics"].get("actual_current_surface_status", ""),
    )
    report(
        "fh-lsz-variance-calibration-manifest-not-evidence",
        variance_calibration_manifest_not_evidence,
        certificates["fh_lsz_variance_calibration_manifest"].get("actual_current_surface_status", ""),
    )
    report(
        "fh-lsz-paired-variance-calibration-gate-not-closure",
        paired_variance_calibration_gate_not_closure,
        certificates["fh_lsz_paired_variance_calibration_gate"].get("actual_current_surface_status", ""),
    )
    report(
        "fh-lsz-polefit8x8-manifest-not-evidence",
        polefit8x8_manifest_not_evidence,
        certificates["fh_lsz_polefit8x8_chunk_manifest"].get("actual_current_surface_status", ""),
    )
    report(
        "fh-lsz-polefit8x8-combiner-not-closure",
        polefit8x8_combiner_not_closure,
        certificates["fh_lsz_polefit8x8_chunk_combiner_gate"].get("actual_current_surface_status", ""),
    )
    report(
        "fh-lsz-polefit8x8-postprocessor-not-closure",
        polefit8x8_postprocessor_not_closure,
        certificates["fh_lsz_polefit8x8_postprocessor"].get("actual_current_surface_status", ""),
    )
    report(
        "joint-fh-lsz-resource-is-multiday",
        joint_resource_multiday,
        f"hours={certificates['joint_resource_projection'].get('projection', {}).get('joint_mass_scaled_hours')}",
    )
    report(
        "full-positive-closure-assembly-gate-open",
        full_positive_assembly_gate_open,
        certificates["full_positive_closure_assembly_gate"].get("actual_current_surface_status", ""),
    )
    report(
        "negative-route-applicability-review-preserves-reopen",
        negative_route_applicability_review_passed,
        certificates["negative_route_applicability_review"].get("actual_current_surface_status", ""),
    )
    report(
        "pr230-nonchunk-current-surface-exhaustion-blocks-shortcuts",
        pr230_nonchunk_current_surface_exhaustion_blocks,
        certificates["pr230_nonchunk_current_surface_exhaustion"].get(
            "actual_current_surface_status", ""
        ),
    )
    report(
        "pr230-nonchunk-future-artifact-intake-blocks-shortcuts",
        pr230_nonchunk_future_artifact_intake_blocks,
        certificates["pr230_nonchunk_future_artifact_intake"].get(
            "actual_current_surface_status", ""
        ),
    )
    report(
        "pr230-nonchunk-terminal-route-exhaustion-blocks-shortcuts",
        pr230_nonchunk_terminal_route_exhaustion_blocks,
        certificates["pr230_nonchunk_terminal_route_exhaustion"].get(
            "actual_current_surface_status", ""
        ),
    )
    report(
        "pr230-nonchunk-reopen-admissibility-blocks-path-only-reopen",
        pr230_nonchunk_reopen_admissibility_blocks,
        certificates["pr230_nonchunk_reopen_admissibility"].get(
            "actual_current_surface_status", ""
        ),
    )
    report(
        "pr230-nonchunk-cycle14-route-selector-blocks-current-selection",
        pr230_nonchunk_cycle14_route_selector_blocks,
        certificates["pr230_nonchunk_cycle14_route_selector"].get(
            "actual_current_surface_status", ""
        ),
    )
    report(
        "pr230-nonchunk-cycle15-independent-route-admission-blocks-pivot",
        pr230_nonchunk_cycle15_independent_route_admission_blocks,
        certificates["pr230_nonchunk_cycle15_independent_route_admission"].get(
            "actual_current_surface_status", ""
        ),
    )
    report(
        "pr230-nonchunk-cycle16-reopen-source-guard-blocks-reopen",
        pr230_nonchunk_cycle16_reopen_source_guard_blocks,
        certificates["pr230_nonchunk_cycle16_reopen_source_guard"].get(
            "actual_current_surface_status", ""
        ),
    )
    report(
        "pr230-nonchunk-cycle17-stop-condition-blocks-route-cycling",
        pr230_nonchunk_cycle17_stop_condition_blocks,
        certificates["pr230_nonchunk_cycle17_stop_condition_gate"].get(
            "actual_current_surface_status", ""
        ),
    )
    report(
        "pr230-nonchunk-cycle18-reopen-freshness-blocks-reopen",
        pr230_nonchunk_cycle18_reopen_freshness_blocks,
        certificates["pr230_nonchunk_cycle18_reopen_freshness_gate"].get(
            "actual_current_surface_status", ""
        ),
    )
    report(
        "pr230-nonchunk-cycle19-no-duplicate-route-blocks-replay",
        pr230_nonchunk_cycle19_no_duplicate_route_blocks,
        certificates["pr230_nonchunk_cycle19_no_duplicate_route_gate"].get(
            "actual_current_surface_status", ""
        ),
    )
    report(
        "pr230-nonchunk-cycle20-process-gate-continuation-blocks-churn",
        pr230_nonchunk_cycle20_process_gate_continuation_blocks,
        certificates["pr230_nonchunk_cycle20_process_gate_continuation_no_go"].get(
            "actual_current_surface_status", ""
        ),
    )
    report(
        "pr230-nonchunk-cycle21-remote-reopen-guard-blocks-remote-reopen",
        pr230_nonchunk_cycle21_remote_reopen_guard_blocks,
        certificates["pr230_nonchunk_cycle21_remote_reopen_guard"].get(
            "actual_current_surface_status", ""
        ),
    )
    report(
        "pr230-nonchunk-cycle22-main-audit-drift-guard-blocks-main-drift-reopen",
        pr230_nonchunk_cycle22_main_audit_drift_guard_blocks,
        certificates["pr230_nonchunk_cycle22_main_audit_drift_guard"].get(
            "actual_current_surface_status", ""
        ),
    )
    report(
        "pr230-nonchunk-cycle23-main-effective-status-drift-guard-blocks-main-drift-reopen",
        pr230_nonchunk_cycle23_main_effective_status_drift_guard_blocks,
        certificates["pr230_nonchunk_cycle23_main_effective_status_drift_guard"].get(
            "actual_current_surface_status", ""
        ),
    )
    report(
        "pr230-nonchunk-cycle24-post-cycle23-main-status-drift-guard-blocks-main-drift-reopen",
        pr230_nonchunk_cycle24_post_cycle23_main_status_drift_guard_blocks,
        certificates[
            "pr230_nonchunk_cycle24_post_cycle23_main_status_drift_guard"
        ].get("actual_current_surface_status", ""),
    )
    report(
        "pr230-nonchunk-cycle25-post-cycle24-main-audit-status-drift-guard-blocks-main-drift-reopen",
        pr230_nonchunk_cycle25_post_cycle24_main_audit_status_drift_guard_blocks,
        certificates[
            "pr230_nonchunk_cycle25_post_cycle24_main_audit_status_drift_guard"
        ].get("actual_current_surface_status", ""),
    )
    report(
        "pr230-nonchunk-cycle26-post-cycle25-main-audit-status-drift-guard-blocks-main-drift-reopen",
        pr230_nonchunk_cycle26_post_cycle25_main_audit_status_drift_guard_blocks,
        certificates[
            "pr230_nonchunk_cycle26_post_cycle25_main_audit_status_drift_guard"
        ].get("actual_current_surface_status", ""),
    )
    report(
        "pr230-nonchunk-cycle27-post-cycle26-main-audit-status-drift-guard-blocks-main-drift-reopen",
        pr230_nonchunk_cycle27_post_cycle26_main_audit_status_drift_guard_blocks,
        certificates[
            "pr230_nonchunk_cycle27_post_cycle26_main_audit_status_drift_guard"
        ].get("actual_current_surface_status", ""),
    )
    report(
        "pr230-nonchunk-cycle28-post-cycle27-main-audit-status-drift-guard-blocks-main-drift-reopen",
        pr230_nonchunk_cycle28_post_cycle27_main_audit_status_drift_guard_blocks,
        certificates[
            "pr230_nonchunk_cycle28_post_cycle27_main_audit_status_drift_guard"
        ].get("actual_current_surface_status", ""),
    )
    report(
        "pr230-nonchunk-cycle29-post-cycle28-main-audit-status-drift-guard-blocks-main-drift-reopen",
        pr230_nonchunk_cycle29_post_cycle28_main_audit_status_drift_guard_blocks,
        certificates[
            "pr230_nonchunk_cycle29_post_cycle28_main_audit_status_drift_guard"
        ].get("actual_current_surface_status", ""),
    )
    report(
        "pr230-nonchunk-cycle30-post-cycle29-main-audit-status-drift-guard-blocks-main-drift-reopen",
        pr230_nonchunk_cycle30_post_cycle29_main_audit_status_drift_guard_blocks,
        certificates[
            "pr230_nonchunk_cycle30_post_cycle29_main_audit_status_drift_guard"
        ].get("actual_current_surface_status", ""),
    )
    report(
        "pr230-nonchunk-cycle31-post-cycle30-main-audit-status-drift-guard-blocks-main-drift-reopen",
        pr230_nonchunk_cycle31_post_cycle30_main_audit_status_drift_guard_blocks,
        certificates[
            "pr230_nonchunk_cycle31_post_cycle30_main_audit_status_drift_guard"
        ].get("actual_current_surface_status", ""),
    )
    report(
        "pr230-nonchunk-cycle32-post-cycle31-main-audit-status-drift-guard-blocks-main-drift-reopen",
        pr230_nonchunk_cycle32_post_cycle31_main_audit_status_drift_guard_blocks,
        certificates[
            "pr230_nonchunk_cycle32_post_cycle31_main_audit_status_drift_guard"
        ].get("actual_current_surface_status", ""),
    )
    report(
        "pr230-nonchunk-cycle33-post-cycle32-main-audit-status-drift-guard-blocks-main-drift-reopen",
        pr230_nonchunk_cycle33_post_cycle32_main_audit_status_drift_guard_blocks,
        certificates[
            "pr230_nonchunk_cycle33_post_cycle32_main_audit_status_drift_guard"
        ].get("actual_current_surface_status", ""),
    )
    report(
        "pr230-nonchunk-cycle34-post-cycle33-main-nonpr230-drift-guard-blocks-main-drift-reopen",
        pr230_nonchunk_cycle34_post_cycle33_main_nonpr230_drift_guard_blocks,
        certificates[
            "pr230_nonchunk_cycle34_post_cycle33_main_nonpr230_drift_guard"
        ].get("actual_current_surface_status", ""),
    )
    report(
        "pr230-nonchunk-cycle35-post-cycle34-main-audit-ledger-drift-guard-blocks-main-drift-reopen",
        pr230_nonchunk_cycle35_post_cycle34_main_audit_ledger_drift_guard_blocks,
        certificates[
            "pr230_nonchunk_cycle35_post_cycle34_main_audit_ledger_drift_guard"
        ].get("actual_current_surface_status", ""),
    )
    report(
        "interacting-kinetic-route-still-needs-ensemble-or-theorem",
        interacting_kinetic_still_open,
        certificates["interacting_kinetic_sensitivity"].get("actual_current_surface_status", ""),
    )
    report("planck-beta-route-blocked-on-current-surface", beta_blocked, certificates["beta_lambda_no_go"].get("actual_current_surface_status", ""))
    report("prior-route-queue-exhausted", queue_open, "queue exhaustion certificate says no full retained closure")

    closure_routes = [
        {
            "route": "direct_or_joint_physical_measurement",
            "retained_closure_condition": (
                "run strict production correlator or joint FH/LSZ evidence on a "
                "physically suitable scale/heavy-quark treatment, derive or "
                "measure the scalar pole derivative and any interacting "
                "kinetic/matching bridge, produce production certificates, and "
                "pass a retained-proposal gate"
            ),
            "why_shortest": "It bypasses Ward/H_unit and scalar-pole analytic normalization.",
            "current_blocker": "existing certificates are reduced-scope/pilot or manifests; the postprocess gate has no production outputs, pole fit, or FV/IR/zero-mode control, and the joint route projects to multi-day single-worker compute",
        },
        {
            "route": "analytic_scalar_residue",
            "retained_closure_condition": (
                "derive scalar source two-point pole residue, scalar carrier map, "
                "and common scalar/gauge dressing from retained dynamics, then "
                "re-run the Ward physical-readout repair audit"
            ),
            "why_shortest": "It directly repairs the audit's physical-readout objection.",
            "current_blocker": "source scaling and Feshbach projection are controlled, but the interacting scalar denominator/residue, zero-mode/IR/finite-volume limiting prescription, taste/projector normalization, fitted-kernel selector, and common dressing are still not derived",
        },
        {
            "route": "new_selector_or_axiom",
            "retained_closure_condition": (
                "derive beta_lambda(M_Pl)=0 or explicitly add a new selector/premise; "
                "the latter is not retained closure under the current one-axiom surface"
            ),
            "why_shortest": "It can reproduce numerical y_t if the selector is accepted.",
            "current_blocker": "all current stationarity shortcuts are no-go/conditional",
        },
    ]

    result = {
        "actual_current_surface_status": "open / retained closure not yet reached",
        "verdict": (
            "The current PR #230 surface has no retained top-Yukawa closure.  "
            "All tested non-MC shortcuts are blocked or conditional.  The shortest "
            "honest retained routes are: strict direct or joint FH/LSZ physical "
            "measurement, a new scalar pole-residue/common-dressing theorem, or "
            "a newly derived Planck stationarity selector.  Newer support shows "
            "source-scaling, Feshbach projection, same-source invariant readout, "
            "and substrate source units are not the hard blockers.  The hard "
            "blockers are production pole/matching evidence or the microscopic "
            "interacting scalar denominator, zero-mode/IR limiting order, pole "
            "residue envelope, Ward/gauge kernel derivative gap, exact zero-mode "
            "limit-order prescription, absence of a hidden zero-mode import, "
            "and common dressing.  Flat toron finite-volume dependence washes "
            "out for the local massive bubble in the thermodynamic limit, and "
            "the exact q=0 gauge mode cancels in a color singlet when self and "
            "exchange terms are included.  The remaining finite-q kernel is "
            "IR-regular in four dimensions.  Zero-mode-removed finite ladder "
            "pole witnesses exist at small mass, but they are volume, "
            "projector, taste-corner, and derivative sensitive; filtering "
            "non-origin taste corners removes the finite crossings, and the "
            "current taste-carrier import audit finds no retained authority "
            "that admits those corners as the physical scalar carrier.  A "
            "normalized taste-singlet source over the 16 corners also rescales "
            "the finite ladder eigenvalues by 1/16 and removes every finite "
            "crossing, so unnormalized taste multiplicity is load-bearing.  A "
            "unit taste singlet can be constructed algebraically, but the "
            "source functional still permits source-coordinate rescaling and "
            "does not identify the physical scalar carrier or K'(x_pole).  At "
            "unit-projector normalization the finite ladder has no crossing; "
            "forcing one would require an underived scalar-kernel multiplier "
            "larger than two, and the kernel-enhancement import audit finds no "
            "hidden retained authority for that factor.  Fitting such a "
            "multiplier to force the pole only moves the missing scalar "
            "normalization into g_eff; the resulting residue proxy remains "
            "finite-row dependent.  The "
            "FH/LSZ production manifest is now guarded by an explicit "
            "postprocess acceptance gate: the production outputs, same-source "
            "dE/ds and Gamma_ss(q) data, isolated-pole inverse derivative, and "
            "FV/IR/zero-mode control are still absent.  The current production "
            "harness also resumes only completed per-volume artifacts, while "
            "the smallest joint shard exceeds the foreground campaign window.  "
            "A chunked L12 launch manifest is available as scheduling support, "
            "but it is not production evidence and does not cover L16/L24.  "
            "The chunk combiner gate now rejects absent or partial chunks and "
            "requires production metadata plus run-control provenance before "
            "even an L12 combined summary can be constructed.  Chunk001 has "
            "now completed and is combiner-ready, but it is only one of 63 L12 "
            "chunks and no combined L12 summary exists.  Chunk launch "
            "commands now isolate per-volume artifacts in chunk-local output "
            "directories and use per-chunk resume.  "
            "The scalar pole-fit kinematics gate also shows the current four "
            "modes give only one nonzero p_hat^2 shell, so a completed chunk "
            "set would still need richer pole-fit kinematics or a theorem.  "
            "A pole-fit postprocessor scaffold now exists, but it has no "
            "combined production input and is not evidence.  Even with a "
            "future finite shell set and a named pole, finite Euclidean "
            "Gamma_ss rows do not identify the pole derivative by themselves: "
            "analytic deformations can vanish on all sampled shells and at "
            "the pole while changing dGamma_ss/dp^2.  The model-class gate "
            "now makes this executable: a future finite-shell pole fit remains "
            "non-evidence unless a model-class, analytic-continuation, "
            "pole-saturation, continuum, or microscopic scalar-denominator "
            "certificate excludes those deformations.  Positive Stieltjes "
            "spectral form by itself is not enough: positive continuum models "
            "can keep the same finite shell rows and pole while changing the "
            "pole residue.  The pole-saturation threshold gate now makes the "
            "next acceptance condition explicit: a future finite-shell fit "
            "needs a tight positive-Stieltjes residue interval certified by "
            "pole-saturation, continuum-threshold control, or a scalar "
            "denominator theorem.  The threshold-authority audit finds no "
            "hidden current artifact that supplies that premise.  The "
            "Pade-Stieltjes bounds gate sharpens the non-compute bypass: "
            "moment theory can certify the pole residue only after a strict "
            "same-surface moment/threshold/FV certificate exists, and the "
            "current surface has no such certificate.  The "
            "finite-volume pole-saturation obstruction blocks using finite-L "
            "discreteness as a substitute for a uniform gap.  The numba "
            "seed-independence audit also demotes historical chunk001/chunk002: "
            "their metadata seeds differ, but their gauge-evolution signatures "
            "match and they lack the numba_gauge_seed_v1 marker.  They must be "
            "rerun under the patched harness or excluded before L12 combination.  "
            "The uniform-gap self-certification no-go closes another adjacent "
            "shortcut: finite Euclidean shell rows, even if generated by a "
            "gapped Stieltjes model, are also reproducible by a near-pole "
            "positive continuum model with zero pole-residue lower bound.  "
            "The scalar-denominator theorem closure attempt checks the full "
            "dependency stack and still finds open blockers: zero-mode/flat "
            "sector prescription, scalar taste/projector carrier, K'(pole), "
            "model class, uniform threshold, and seed-controlled production.  "
            "The soft-continuum threshold no-go also blocks promoting "
            "color-singlet q=0 cancellation plus finite-q IR regularity into "
            "that threshold premise: IR integrability is compatible with "
            "positive continuum spectral weight arbitrarily close to the pole.  "
            "The reflection-positivity shortcut no-go blocks the broader OS "
            "positivity repair too: a reflection-positive positive-measure "
            "family can preserve the same finite shell rows while moving the "
            "same-source pole residue.  "
            "The short-distance/OPE shortcut no-go blocks the UV-operator "
            "normalization repair as well: finite large-Q coefficients and "
            "operator matching can stay fixed while the isolated IR source-pole "
            "residue varies by a factor of ten.  "
            "The effective-mass plateau residue no-go closes the finite-time "
            "postprocess shortcut: positive multi-exponential correlators can "
            "share a finite plateau window while changing the ground/source "
            "residue by a factor of ten.  "
            "The finite source-shift derivative no-go closes the adjacent FH "
            "shortcut: one symmetric finite source radius can keep "
            "E(-delta), E(0), E(+delta), and the finite slope fixed while "
            "changing dE/ds at zero through odd nonlinear response.  "
            "The finite-source-linearity gate turns the repair into an "
            "acceptance condition: current chunks still have one nonzero "
            "source radius, while a three-radius calibration is planning "
            "support only and projects beyond the foreground window.  "
            "The autocorrelation/ESS gate blocks another production shortcut: "
            "plaquette histories exist, but the current chunk outputs do not "
            "retain per-configuration same-source dE/ds or C_ss(q) target "
            "time series, so target ESS cannot be certified.  "
            "The effective-potential Hessian/source-overlap no-go blocks the "
            "radial-curvature repair: canonical VEV, W/Z masses, and scalar "
            "Hessian eigenvalues do not fix the source operator direction.  "
            "The BRST/Nielsen Higgs-identity no-go blocks the gauge-identity "
            "repair too: BRST/ST residuals and physical pole "
            "gauge-parameter independence can stay fixed while the neutral "
            "source direction and source overlap rotate.  "
            "The Cl(3)/Z3 automorphism/source-identity no-go blocks finite "
            "substrate orbit data as the missing continuous LSZ input: finite "
            "orbit sizes, D17 carrier count, and source unit can stay fixed "
            "while source overlap, D'(pole), and residue vary.  "
            "The same-source pole-data sufficiency gate records the positive "
            "side too: (dE/ds)*sqrt(D'_ss) is source-rescaling invariant, but "
            "current production, model-class/FV/IR, and Higgs-identity gates "
            "are not passed.  "
            "The complete source-spectrum identity no-go sharpens the same "
            "boundary: even full source-only C_ss(p) pole masses/residues plus "
            "dE_top/ds can be held fixed while the canonical-Higgs y_t varies "
            "through a finite orthogonal scalar top coupling.  "
            "The neutral-scalar top-coupling tomography gate gives the linear "
            "algebra acceptance rule: the current source-only response matrix "
            "has rank one, so a two-component neutral top-coupling vector has "
            "a null direction unless a rank-one theorem, O_H/C_sH/C_HH row, "
            "or independent W/Z response row is supplied.  "
            "The scalar carrier/projector closure attempt confirms the "
            "remaining taste/carrier side is also open: unit taste algebra and "
            "color-singlet support do not admit non-origin corners, preserve "
            "unit-projector crossings, or derive K'(pole).  "
            "The K-prime closure attempt then confirms the derivative itself "
            "is still named but not derived: finite derivative scouts remain "
            "blocked by limiting order, residue-envelope dependence, "
            "Ward/Feshbach non-identification, carrier/projector choice, and "
            "missing threshold control.  "
            "The canonical-Higgs pole identity gate also remains open: the "
            "same-source invariant formula cancels source-coordinate scaling, "
            "but it does not identify the measured source pole with the "
            "canonical Higgs radial mode used by v.  "
            "A gauge-normalized response ratio could cancel kappa_s with a "
            "same-source W/Z mass slope, but that gauge response observable and "
            "the shared canonical-Higgs identity are absent.  The observable-gap "
            "gate confirms the present production harness is QCD top-only and "
            "does not emit dM_W/ds or dM_Z/ds.  The W/Z response builder now "
            "defines the future candidate certificate and records that no "
            "same-source W/Z rows are present.  The W/Z response certificate "
            "gate rejects static EW algebra and any slope-only certificate "
            "without production W/Z mass fits, sector-overlap, and canonical-"
            "Higgs identity.  The W/Z harness absence guard now records that "
            "missing response path directly in future production certificates; "
            "that guard is not evidence.  The same-source sector-overlap "
            "identity obstruction further blocks treating a common source label "
            "as proof that the top and gauge responses have equal canonical-Higgs "
            "overlap; without k_top = k_gauge, the gauge-normalized ratio reads "
            "y_t times k_top/k_gauge.  The source-pole/canonical-Higgs mixing "
            "obstruction also blocks treating a completed same-source pole "
            "residue as physical y_t unless the source pole has unit overlap "
            "with the canonical Higgs radial mode; otherwise the readout is "
            "y_t times cos(theta).  "
            "A mode/noise budget identifies an eight-mode/eight-noise L12 "
            "option that keeps the foreground estimate, but it needs a "
            "variance gate and cannot be treated as evidence.  The variance "
            "gate now rejects the current evidence surface: the reduced smoke "
            "has the wrong phase, modes, noises, volume, and statistics, while "
            "the foreground chunk is absent or four-mode/x16 rather than an "
            "eight-mode/x8 calibration.  The harness now emits "
            "noise-subsample stability diagnostics for future paired x8/x16 "
            "calibrations, but the current diagnostics are reduced-scope "
            "instrumentation support only.  The harness also now serializes "
            "per-configuration source-response and scalar two-point target "
            "time series for future autocorrelation/ESS gates, but that is "
            "instrumentation support, not production evidence or scalar LSZ "
            "normalization.  The target-time-series Higgs-identity no-go "
            "then shows that even perfect same-source target time series "
            "remain source-coordinate data unless source-pole purity, "
            "no-orthogonal-top-coupling, sector-overlap equality, or an "
            "independent canonical-Higgs response observable is supplied.  "
            "The no-orthogonal-top-coupling selection-rule no-go blocks one "
            "of those escape hatches: current listed substrate/gauge charges "
            "cannot allow h tbar t while forbidding an orthogonal neutral "
            "chi tbar t coupling with the same labels.  "
            "The source-pole purity cross-correlator gate blocks another: "
            "C_ss and source response can stay fixed while the source-Higgs "
            "overlap changes unless a C_sH cross-correlator, W/Z response, "
            "or retained purity theorem is supplied.  The source-Higgs "
            "cross-correlator manifest now records the exact future O_H/C_sH/"
            "C_HH production schema, but it is not evidence because no such "
            "rows or production certificate exist.  The source-Higgs "
            "cross-correlator import audit then confirms that C_sH is not "
            "already hidden in the current harness or EW/Higgs notes; it is a "
            "future observable/theorem, not current closure.  The Gram purity "
            "gate gives that future route an acceptance condition, "
            "C_sH^2 = C_ss C_HH at the isolated pole, but current C_sH/C_HH "
            "residues are absent.  The source-Higgs builder and postprocessor "
            "now attach the Legendre/LSZ source-pole operator O_sp as the "
            "unit-residue source side, so the sharp future test is "
            "Delta_spH = Res(C_HH) - Res(C_sp,H)^2 = 0 and |rho_spH| = 1; "
            "no production O_H/C_sH/C_HH pole certificate is present.  "
            "The canonical-Higgs operator realization "
            "gate adds the adjacent object-level blocker: existing EW "
            "gauge-mass artifacts assume canonical H after it is supplied, "
            "while the PR #230 harness has no same-surface O_H, C_sH, or C_HH "
            "operator path.  The H_unit candidate gate blocks the obvious "
            "legacy substitute: H_unit is a named D17/substrate bilinear, but "
            "without pole-purity and canonical-normalization certificates it "
            "is not O_H and re-enters the forbidden matrix-element readout.  "
            "The cross-lane O_H authority audit blocks another hidden-import "
            "shortcut: gravity O_h shell notes, lepton/DM two-Higgs reductions, "
            "Higgs mass/vacuum summaries, EW one-Higgs algebra, and Koide O_h "
            "support/no-go surfaces are framework-native context, but none "
            "supplies the PR230 same-surface O_H identity, canonical LSZ "
            "normalization, or C_sH/C_HH pole residues.  "
            "The taste-condensate O_H bridge audit blocks the strongest "
            "remaining Higgs/taste-stack shortcut: the exact taste-Higgs "
            "operators are trace-zero taste shifts, while the current PR230 "
            "FH/LSZ source is the uniform additive mass source with zero "
            "projection onto those axes.  It is framework-native context, but "
            "not PR230 O_H authority without source-coordinate transport or "
            "C_sH/C_HH pole rows.  "
            "The same-surface Z3 taste-triplet artifact now supplies the exact "
            "cyclic action on the PR230 taste axes, but it remains support only: "
            "the physical lazy neutral transfer, source/Higgs row, and strict "
            "primitive certificate are still absent.  "
            "The Z3-triplet positive-cone H2 support certificate now supplies "
            "the equal-magnitude PSD cone row for that triplet exactly, but it "
            "is still algebraic support only and not a physical transfer, "
            "primitive irreducibility theorem, or source-Higgs coupling row.  "
            "The first-principles O_H bridge candidate portfolio ranks the "
            "surviving source-transport, action-first O_H, W/Z response, "
            "Schur-row, and neutral-primitive routes as open positive "
            "candidates; it is route selection, not retained closure.  "
            "The source-Higgs harness absence guard now records missing "
            "O_H/C_sH/C_HH rows directly in future production certificates; "
            "that guard is an instrumentation firewall, not evidence.  "
            "The neutral-scalar rank-one purity gate "
            "also fails: D17 carrier support is not a dynamical rank-one "
            "theorem, and a rank-two neutral scalar witness still preserves "
            "the listed labels while changing the source-pole readout.  The "
            "commutant rank no-go sharpens that boundary: symmetry/D17 labels "
            "still allow a rank-two neutral scalar response family, so rank "
            "one requires dynamics or C_sH/C_HH data.  The dynamical rank-one "
            "closure attempt also fails on the current surface: a positive "
            "two-pole neutral scalar family keeps the source pole mass and "
            "residue fixed while a finite orthogonal pole and varying "
            "canonical-Higgs overlap remain allowed.  The orthogonal-neutral "
            "decoupling no-go also blocks dismissing that pole by finite mass "
            "gap alone; no current theorem ties the overlap or top coupling to "
            "inverse orthogonal mass.  The primitive-cone certificate gate "
            "now makes the only positive rank-one theorem route executable: a "
            "future same-surface neutral transfer matrix must be nonnegative, "
            "strongly connected, have a positive primitive power, certify the "
            "isolated pole and overlaps, and pass the forbidden-import "
            "firewall.  No such certificate is present.  "
            "The same-surface neutral multiplicity-one gate now records the "
            "clean source-Higgs artifact contract and rejects the current "
            "two-singlet completion without authorizing O_H closure.  "
            "A paired x8/x16 calibration "
            "manifest now exists, but it is still launch planning rather than "
            "completed same-source production variance evidence.  The "
            "gauge-VEV source-overlap no-go also blocks using the canonical "
            "electroweak VEV or gauge-boson masses to identify the Cl(3)/Z3 "
            "source with the canonical Higgs field.  Canonical kinetic "
            "renormalization is likewise insufficient: Z_h=1 fixes the Higgs "
            "field residue, not the source-operator overlap <0|O_s|h>.  "
            "Source contact-term renormalization is also only a scheme "
            "choice: it can fix C_ss(0) and C_ss'(0) while leaving the pole "
            "residue and source overlap different.  "
            "The actual interacting "
            "scalar pole derivative theorem and production evidence remain open.  "
            "These cannot be assumed."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": "No route currently satisfies retained-proposal conditions.",
        "negative_route_applicability_review_passed": negative_route_applicability_review_passed,
        "direct_certificates": direct_meta,
        "required_certificates": required_certificates,
        "closure_routes": closure_routes,
        "exact_next_action": (
            "Do not run more small pilot MC for closure.  Either run the strict "
            "production physical-response manifest and follow it with pole/LSZ "
            "and matching analysis through the FH/LSZ postprocess gate, or derive "
            "the same-surface neutral multiplicity-one certificate accepted by "
            "outputs/yt_pr230_same_surface_neutral_multiplicity_one_gate_2026-05-07.json "
            "and then the microscopic interacting scalar denominator/residue "
            "theorem from the retained action, including the canonical-Higgs pole identity, "
            "a source-pole mixing exclusion, a same-source sector-overlap "
            "identity, or a same-source gauge-mass response observable.  "
            "For the same-source W/Z response route, first build a strict "
            "same-source top-response certificate from a closed identity "
            "certificate and matched top/W covariance rows; the current builder "
            "is open and does not emit the production top-response certificate.  "
            "The identity certificate builder now exposes the first sub-blocker: "
            "sector overlap, canonical-Higgs pole identity, an accepted purity/"
            "WZ/rank-one identity route, and retained-route authorization are "
            "all still absent.  The matched covariance builder exposes the "
            "second sub-blocker: no paired top/W response rows exist on a "
            "matched configuration set.  The covariance marginal-derivation "
            "no-go now blocks deriving that covariance from separate top and "
            "W response marginals; the factorization-independence gate now "
            "also blocks treating the Cl(3)/Z^3 same-source label or "
            "3+derived-time locality as independence authority.  A real "
            "paired row set or a strict same-surface product-measure/"
            "conditional-independence theorem is required; the deterministic "
            "W-response gate further shows deterministic W alone is not "
            "covariance authority without paired top rows or a closed "
            "same-surface covariance formula.  The Goldstone-equivalence "
            "source-identity no-go now also blocks treating longitudinal-"
            "equivalence bookkeeping as source-coordinate authority.  "
            "The W/Z same-source minimal certificate cut records that the "
            "accepted action certificate still needs canonical O_H, current "
            "sector-overlap identity, and W/Z mass-fit path roots before any "
            "W/Z physical-response readout can be assembled.  "
            "Continue chunked production only with "
            "seed-controlled replacement chunks or scheduler handoff; do not "
            "treat historical chunk001/chunk002 as independent evidence.  "
            "Before treating any finite-shell pole fit as "
            "load-bearing, add a model-class/analytic-continuation gate or a "
            "theorem excluding shell-vanishing derivative deformations.  If "
            "using the eight-mode/eight-noise foreground "
            "option, first add a same-source x8/x16 variance calibration with "
            "noise-subsample diagnostics.  Before using finite source-shift "
            "slopes as FH derivatives, add multiple source radii or a retained "
            "analytic response-bound theorem; the current finite-source-"
            "linearity gate is not passed, and the multi-radius calibration "
            "checkpoint is response-window support only."
            " Before treating chunked FH/LSZ as production evidence, also "
            "emit target-observable autocorrelation/ESS or blocking/bootstrap "
            "certificates.  For the source-Higgs lane, use the O_sp-normalized "
            "builder/postprocessor and supply a certified O_H with production "
            "C_sH/C_HH pole residues before running retained-route gating; "
            "the current Gram-purity contract witness is schema support, not "
            "production evidence.  Before any retained/proposed-retained "
            "wording, rerun the full positive closure assembly gate; it "
            "currently rejects both the current surface and a hypothetical "
            "chunk-only completion.  The non-chunk current-surface exhaustion "
            "gate also records that no hidden branch-local shortcut remains "
            "without a named future same-surface row, certificate, or theorem.  "
            "The future-artifact intake gate records that no such named input "
            "is present on the current surface.  The terminal route-exhaustion "
            "gate records the stop/reopen rule for further non-chunk work.  "
            "The negative-route applicability review then scopes the no-go stack: "
            "selected blockers are correct for their current surfaces, no retained "
            "negative YT row is being used, and future source-Higgs, W/Z, Schur, "
            "rank-one, scalar-LSZ, or production evidence can reopen the route.  "
            "The two-source taste-radial chart is a fresh same-surface support "
            "artifact for the source-coordinate family, but it is not a listed "
            "closure artifact for these gates until a production action/row "
            "certificate or canonical O_H identity lands.  "
            "The two-source taste-radial row-production manifest records exact "
            "no-resume chunk commands and a collision guard for C_sx/C_xx rows, "
            "but it is run-control support only until rows are actually run, "
            "combined, pole-tested, and bridged to O_H or physical response.  "
            "The completed two-source taste-radial chunks001-006 checkpoints "
            "are bounded row support only: they validate seed-controlled "
            "timeseries rows but do not supply combined L12 pole evidence, "
            "FV/IR authority, canonical O_H, or scalar-LSZ normalization.  "
            "The taste-radial canonical-O_H selector gate proves uniqueness only "
            "inside the degree-one source-axis subspace and blocks the "
            "symmetry-only selector because the full Z3 trace-zero taste algebra "
            "remains three-dimensional.  "
            "The cycle-14 through cycle-17 gates record that no current route, "
            "independent pivot, reopen source, or executable non-chunk queue "
            "item remains on this branch.  The cycle-18 reopen-freshness gate "
            "records that no post-cycle-17 same-surface artifact is present for "
            "admissible reopen.  The cycle-19 no-duplicate-route gate records "
            "that another current-surface route selection would only replay a "
            "closed non-chunk family until a fresh parseable same-surface "
            "artifact exists.  The cycle-20 process-gate continuation no-go "
            "records that another process-only gate is also not an admissible "
            "science route until that fresh same-surface artifact exists.  The "
            "cycle-21 remote-surface reopen guard records that fetched remote "
            "surfaces also contain no listed same-surface artifact for "
            "admissible reopen.  The cycle-22 main-audit-drift guard records "
            "that the latest origin/main advance is audit/effective-status "
            "drift only and supplies no listed PR230 same-surface artifact.  "
            "The cycle-23 main-effective-status-drift guard records that "
            "origin/main advanced again only on audit/effective-status "
            "surfaces and still supplies no listed PR230 same-surface artifact.  "
            "The cycle-24 post-cycle-23 main-status-drift guard records that "
            "origin/main advanced again only on audit/effective-status "
            "surfaces and still supplies no listed PR230 same-surface artifact.  "
            "The cycle-25 post-cycle-24 main-audit-status-drift guard records "
            "that origin/main advanced again only on audit/effective-status "
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
        "source_coordinate_transport_blocks_current_shortcut": source_coordinate_transport_blocks_current_shortcut,
        "origin_main_composite_higgs_intake_not_closure": origin_main_composite_higgs_intake_not_closure,
        "origin_main_ew_m_residual_intake_not_closure": origin_main_ew_m_residual_intake_not_closure,
        "z3_triplet_conditional_primitive_not_closure": z3_triplet_conditional_primitive_not_closure,
        "z3_triplet_positive_cone_h2_support_not_transfer": z3_triplet_positive_cone_h2_support_not_transfer,
        "z3_generation_action_lift_not_derived": z3_generation_action_lift_not_derived,
        "z3_lazy_transfer_promotion_not_derived": z3_lazy_transfer_promotion_not_derived,
        "z3_lazy_selector_no_go_blocks": z3_lazy_selector_no_go_blocks,
        "same_surface_z3_taste_triplet_support_not_closure": same_surface_z3_taste_triplet_support_not_closure,
        "source_coordinate_transport_completion_blocks": source_coordinate_transport_completion_blocks,
        "two_source_taste_radial_chart_support_not_closure": two_source_taste_radial_chart_support_not_closure,
        "two_source_taste_radial_action_support_not_closure": two_source_taste_radial_action_support_not_closure,
        "two_source_taste_radial_row_contract_support_not_closure": two_source_taste_radial_row_contract_support_not_closure,
        "two_source_taste_radial_row_manifest_support_not_closure": two_source_taste_radial_row_manifest_support_not_closure,
        "two_source_taste_radial_row_combiner_support_not_closure": two_source_taste_radial_row_combiner_support_not_closure,
        "two_source_taste_radial_schur_subblock_support_not_closure": two_source_taste_radial_schur_subblock_support_not_closure,
        "two_source_taste_radial_kprime_finite_shell_scout_not_closure": two_source_taste_radial_kprime_scout_not_closure,
        "two_source_taste_radial_schur_abc_finite_rows_not_closure": two_source_taste_radial_schur_abc_finite_rows_not_closure,
        "two_source_taste_radial_schur_pole_lift_gate_blocks_endpoint_promotion": two_source_taste_radial_schur_pole_lift_gate_blocks_endpoint_promotion,
        "two_source_taste_radial_primitive_transfer_candidate_not_h3": two_source_taste_radial_primitive_transfer_candidate_not_h3,
        "orthogonal_top_coupling_exclusion_candidate_rejected": orthogonal_top_coupling_exclusion_candidate_rejected,
        "strict_scalar_lsz_moment_fv_authority_absent": strict_scalar_lsz_moment_fv_authority_absent,
        "schur_complement_stieltjes_repair_support_not_closure": schur_complement_stieltjes_repair_support_not_closure,
        "schur_x_given_source_one_pole_scout_not_authority": schur_x_given_source_one_pole_scout_not_authority,
        "two_source_taste_radial_chunk_package_support_not_closure": two_source_taste_radial_chunk_package_support_not_closure,
        "source_higgs_pole_row_contract_open": source_higgs_pole_row_contract_open,
        "taste_radial_canonical_oh_selector_blocks_symmetry_shortcut": taste_radial_canonical_oh_selector_blocks_symmetry_shortcut,
        "degree_one_higgs_action_premise_not_derived": degree_one_higgs_action_premise_not_derived,
        "degree_one_radial_tangent_oh_theorem_support_not_closure": degree_one_radial_tangent_oh_theorem_support_not_closure,
        "taste_radial_to_source_higgs_promotion_contract_support_not_closure": taste_radial_to_source_higgs_promotion_contract_support_not_closure,
        "fms_post_degree_route_support_not_closure": fms_post_degree_route_support_not_closure,
        "fms_composite_oh_conditional_support_not_closure": fms_composite_oh_conditional_support_not_closure,
        "fms_oh_candidate_action_packet_support_not_closure": fms_oh_candidate_action_packet_support_not_closure,
        "fms_source_overlap_readout_gate_support_not_closure": fms_source_overlap_readout_gate_support_not_closure,
        "fms_action_adoption_minimal_cut_support_not_closure": fms_action_adoption_minimal_cut_support_not_closure,
        "higgs_mass_source_action_bridge_support_not_closure": higgs_mass_source_action_bridge_support_not_closure,
        "post_fms_source_overlap_necessity_blocks_current_inference": post_fms_source_overlap_necessity_blocks_current_inference,
        "radial_spurion_action_contract_support_not_closure": radial_spurion_action_contract_support_not_closure,
        "additive_source_radial_spurion_incompatibility_support_not_closure": additive_source_radial_spurion_incompatibility_support_not_closure,
        "additive_top_subtraction_row_contract_support_not_closure": additive_top_subtraction_row_contract_support_not_closure,
        "top_mass_scan_response_harness_support_not_closure": top_mass_scan_response_harness_support_not_evidence,
        "wz_response_ratio_identifiability_contract_support_not_closure": wz_response_ratio_identifiability_contract_support_not_closure,
        "wz_same_source_action_minimal_certificate_cut_open": wz_same_source_action_minimal_certificate_cut_open,
        "wz_accepted_action_response_root_checkpoint_blocks": wz_accepted_action_response_root_checkpoint_blocks,
        "canonical_oh_wz_common_action_cut_open": canonical_oh_wz_common_action_cut_open,
        "canonical_oh_accepted_action_stretch_blocks_current_stack": canonical_oh_accepted_action_stretch_blocks_current_stack,
        "two_source_taste_radial_chunk_checkpoint_not_closure": {
            f"chunk{idx:03d}": not_closure
            for idx, not_closure in two_source_taste_radial_chunk_checkpoint_not_closure.items()
        },
        "kinetic_taste_mixing_bridge_blocks_shortcut": kinetic_taste_mixing_bridge_blocks_shortcut,
        "one_higgs_taste_axis_completeness_blocks_shortcut": one_higgs_taste_axis_completeness_blocks_shortcut,
        "action_first_route_completion_blocks": action_first_route_completion_blocks,
        "wz_response_route_completion_blocks": wz_response_route_completion_blocks,
        "schur_route_completion_blocks": schur_route_completion_blocks,
        "neutral_primitive_route_completion_blocks": neutral_primitive_route_completion_blocks,
        "oh_bridge_candidate_portfolio_open": oh_bridge_candidate_portfolio_open,
        "same_surface_neutral_multiplicity_one_gate_rejects_current_surface": same_surface_neutral_multiplicity_gate_rejects_current_surface,
        "os_transfer_kernel_artifact_absent": os_transfer_kernel_artifact_absent,
        "source_higgs_time_kernel_harness_support_only": source_higgs_time_kernel_harness_support_only,
        "source_higgs_time_kernel_gevp_contract_support_only": source_higgs_time_kernel_gevp_contract_support_only,
        "source_higgs_time_kernel_production_manifest_not_evidence": source_higgs_time_kernel_production_manifest_not_evidence,
        "fms_literature_source_overlap_intake_non_authority": fms_literature_source_overlap_intake_non_authority,
        "schur_higher_shell_production_contract_not_evidence": schur_higher_shell_production_contract_not_evidence,
        "pass_count": PASS_COUNT,
        "fail_count": FAIL_COUNT,
    }
    for idx, not_closure in two_source_taste_radial_chunk_checkpoint_not_closure.items():
        result[
            f"two_source_taste_radial_chunk{idx:03d}_checkpoint_not_closure"
        ] = not_closure
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"\nWrote certificate: {OUTPUT.relative_to(ROOT)}")
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
