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
    "block53_lane1_residual_minimality": "outputs/yt_pr230_block53_lane1_residual_minimality_gate_2026-05-12.json",
    "block54_response_readout_reduction": "outputs/yt_pr230_block54_response_readout_reduction_gate_2026-05-12.json",
    "block55_canonical_neutral_primitive_cut": "outputs/yt_pr230_block55_canonical_neutral_primitive_cut_gate_2026-05-12.json",
    "block56_scalar_pole_fvir_root_cut": "outputs/yt_pr230_block56_scalar_pole_fvir_root_cut_gate_2026-05-12.json",
    "block57_compact_source_functional_foundation": "outputs/yt_pr230_block57_compact_source_functional_foundation_gate_2026-05-12.json",
    "block58_compact_source_spectral_support": "outputs/yt_pr230_block58_compact_source_spectral_support_gate_2026-05-12.json",
    "block59_source_spectral_pole_promotion_obstruction": "outputs/yt_pr230_block59_source_spectral_pole_promotion_obstruction_2026-05-12.json",
    "block60_compact_source_taste_singlet_carrier": "outputs/yt_pr230_block60_compact_source_taste_singlet_carrier_gate_2026-05-12.json",
    "block61_post_carrier_kprime_obstruction": "outputs/yt_pr230_block61_post_carrier_kprime_obstruction_2026-05-12.json",
    "block62_compact_source_kprime_identifiability_obstruction": "outputs/yt_pr230_block62_compact_source_kprime_identifiability_obstruction_2026-05-12.json",
    "fh_lsz_common_window_response": "outputs/yt_fh_lsz_common_window_response_gate_2026-05-04.json",
    "fh_lsz_finite_source_linearity": "outputs/yt_fh_lsz_finite_source_linearity_gate_2026-05-02.json",
    "fh_lsz_response_window_acceptance": "outputs/yt_fh_lsz_response_window_acceptance_gate_2026-05-03.json",
    "fh_lsz_target_ess": "outputs/yt_fh_lsz_target_observable_ess_certificate_2026-05-03.json",
    "fh_lsz_autocorrelation_ess": "outputs/yt_fh_lsz_autocorrelation_ess_gate_2026-05-02.json",
    "fh_lsz_target_timeseries_full_set": "outputs/yt_fh_lsz_target_timeseries_full_set_checkpoint_2026-05-12.json",
    "fh_lsz_polefit8x8_combiner": "outputs/yt_fh_lsz_polefit8x8_chunk_combiner_gate_2026-05-04.json",
    "fh_lsz_polefit8x8_postprocessor": "outputs/yt_fh_lsz_polefit8x8_postprocessor_2026-05-04.json",
    "fh_lsz_model_class": "outputs/yt_fh_lsz_pole_fit_model_class_gate_2026-05-02.json",
    "fh_lsz_model_class_semantic_firewall": "outputs/yt_fh_lsz_model_class_semantic_firewall_2026-05-04.json",
    "fh_lsz_stieltjes_moment_certificate": "outputs/yt_fh_lsz_stieltjes_moment_certificate_gate_2026-05-05.json",
    "fh_lsz_pade_stieltjes_bounds": "outputs/yt_fh_lsz_pade_stieltjes_bounds_gate_2026-05-05.json",
    "fh_lsz_polefit8x8_stieltjes_proxy_diagnostic": "outputs/yt_fh_lsz_polefit8x8_stieltjes_proxy_diagnostic_2026-05-05.json",
    "fh_lsz_complete_bernstein_inverse_diagnostic": "outputs/yt_fh_lsz_complete_bernstein_inverse_diagnostic_2026-05-05.json",
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
    "pr230_wz_mass_response_self_normalization_no_go": "outputs/yt_pr230_wz_mass_response_self_normalization_no_go_2026-05-12.json",
    "wz_g2_bare_running_bridge_attempt": "outputs/yt_pr230_wz_g2_bare_running_bridge_attempt_2026-05-05.json",
    "same_source_sector_overlap": "outputs/yt_same_source_sector_overlap_identity_obstruction_2026-05-02.json",
    "canonical_higgs_operator": "outputs/yt_canonical_higgs_operator_certificate_gate_2026-05-03.json",
    "canonical_higgs_semantic_firewall": "outputs/yt_canonical_higgs_operator_semantic_firewall_2026-05-04.json",
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
    "pr230_same_source_ew_higgs_action_ansatz_gate": "outputs/yt_pr230_same_source_ew_higgs_action_ansatz_gate_2026-05-06.json",
    "pr230_same_source_ew_action_adoption_attempt": "outputs/yt_pr230_same_source_ew_action_adoption_attempt_2026-05-06.json",
    "pr230_radial_spurion_sector_overlap_theorem": "outputs/yt_pr230_radial_spurion_sector_overlap_theorem_2026-05-06.json",
    "pr230_radial_spurion_action_contract": "outputs/yt_pr230_radial_spurion_action_contract_2026-05-06.json",
    "pr230_additive_source_radial_spurion_incompatibility": "outputs/yt_pr230_additive_source_radial_spurion_incompatibility_2026-05-07.json",
    "pr230_additive_top_subtraction_row_contract": "outputs/yt_pr230_additive_top_subtraction_row_contract_2026-05-07.json",
    "pr230_top_mass_scan_response_harness_gate": "outputs/yt_pr230_top_mass_scan_response_harness_gate_2026-05-12.json",
    "pr230_top_mass_scan_subtraction_contract_applicability_audit": "outputs/yt_pr230_top_mass_scan_subtraction_contract_applicability_audit_2026-05-12.json",
    "pr230_higher_shell_source_higgs_operator_certificate_boundary": "outputs/yt_pr230_higher_shell_source_higgs_operator_certificate_boundary_2026-05-12.json",
    "pr230_post_chunks001_002_source_higgs_bridge_intake_guard": "outputs/yt_pr230_post_chunks001_002_source_higgs_bridge_intake_guard_2026-05-12.json",
    "pr230_origin_main_yt_ward_step3_open_gate_intake_guard": "outputs/yt_pr230_origin_main_yt_ward_step3_open_gate_intake_guard_2026-05-12.json",
    "pr230_wz_response_ratio_identifiability_contract": "outputs/yt_pr230_wz_response_ratio_identifiability_contract_2026-05-07.json",
    "pr230_wz_same_source_action_minimal_certificate_cut": "outputs/yt_pr230_wz_same_source_action_minimal_certificate_cut_2026-05-07.json",
    "pr230_wz_accepted_action_response_root_checkpoint": "outputs/yt_pr230_wz_accepted_action_response_root_checkpoint_2026-05-07.json",
    "pr230_canonical_oh_wz_common_action_cut": "outputs/yt_pr230_canonical_oh_wz_common_action_cut_2026-05-07.json",
    "pr230_canonical_oh_accepted_action_stretch_attempt": "outputs/yt_pr230_canonical_oh_accepted_action_stretch_attempt_2026-05-07.json",
    "pr230_post_fms_source_overlap_necessity_gate": "outputs/yt_pr230_post_fms_source_overlap_necessity_gate_2026-05-06.json",
    "pr230_source_higgs_overlap_kappa_contract": "outputs/yt_pr230_source_higgs_overlap_kappa_contract_2026-05-06.json",
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
    "pr230_neutral_rank_one_bypass_post_block37_audit": "outputs/yt_pr230_neutral_rank_one_bypass_post_block37_audit_2026-05-12.json",
    "pr230_source_sector_pattern_transfer_gate": "outputs/yt_pr230_source_sector_pattern_transfer_gate_2026-05-05.json",
    "pr230_det_positivity_bridge_intake_gate": "outputs/yt_pr230_det_positivity_bridge_intake_gate_2026-05-05.json",
    "pr230_reflection_det_primitive_upgrade_gate": "outputs/yt_pr230_reflection_det_primitive_upgrade_gate_2026-05-05.json",
    "pr230_logdet_hessian_neutral_mixing_attempt": "outputs/yt_pr230_logdet_hessian_neutral_mixing_attempt_2026-05-05.json",
    "pr230_hs_logdet_scalar_action_normalization_no_go": "outputs/yt_pr230_hs_logdet_scalar_action_normalization_no_go_2026-05-12.json",
    "pr230_native_scalar_action_lsz_route_exhaustion_after_block40": "outputs/yt_pr230_native_scalar_action_lsz_route_exhaustion_after_block40_2026-05-12.json",
    "pr230_wz_absolute_authority_route_exhaustion_after_block41": "outputs/yt_pr230_wz_absolute_authority_route_exhaustion_after_block41_2026-05-12.json",
    "pr230_full_timeseries_neutral_transfer_lift_no_go_after_block42": "outputs/yt_pr230_full_timeseries_neutral_transfer_lift_no_go_after_block42_2026-05-12.json",
    "pr230_mc_timeseries_krylov_transfer_no_go_after_block43": "outputs/yt_pr230_mc_timeseries_krylov_transfer_no_go_after_block43_2026-05-12.json",
    "pr230_physical_euclidean_source_higgs_row_absence_after_block44": "outputs/yt_pr230_physical_euclidean_source_higgs_row_absence_after_block44_2026-05-12.json",
    "pr230_neutral_offdiagonal_post_block45_applicability_audit": "outputs/yt_pr230_neutral_offdiagonal_post_block45_applicability_audit_2026-05-12.json",
    "cross_lane_oh_authority_audit": "outputs/yt_cross_lane_oh_authority_audit_2026-05-05.json",
    "canonical_oh_premise_stretch": "outputs/yt_canonical_oh_premise_stretch_no_go_2026-05-05.json",
    "source_pole_mixing": "outputs/yt_source_pole_canonical_higgs_mixing_obstruction_2026-05-02.json",
    "source_pole_purity": "outputs/yt_source_pole_purity_cross_correlator_gate_2026-05-02.json",
    "neutral_scalar_irreducibility": "outputs/yt_neutral_scalar_irreducibility_authority_audit_2026-05-04.json",
    "neutral_scalar_primitive_cone": "outputs/yt_neutral_scalar_primitive_cone_certificate_gate_2026-05-05.json",
    "neutral_scalar_primitive_cone_stretch_no_go": "outputs/yt_neutral_scalar_primitive_cone_stretch_no_go_2026-05-05.json",
    "neutral_scalar_burnside_irreducibility": "outputs/yt_neutral_scalar_burnside_irreducibility_attempt_2026-05-05.json",
    "neutral_offdiagonal_generator_derivation": "outputs/yt_neutral_offdiagonal_generator_derivation_attempt_2026-05-05.json",
    "schur_kprime_rows": "outputs/yt_schur_kprime_row_absence_guard_2026-05-03.json",
    "schur_kprime_sufficiency": "outputs/yt_schur_complement_kprime_sufficiency_2026-05-03.json",
    "schur_compressed_bootstrap_no_go": "outputs/yt_schur_compressed_denominator_row_bootstrap_no_go_2026-05-05.json",
    "schur_abc_definition_derivation": "outputs/yt_pr230_schur_abc_definition_derivation_attempt_2026-05-05.json",
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
    "negative_route_applicability_review": "outputs/yt_pr230_negative_route_applicability_review_2026-05-06.json",
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
                "boundaries; strict Stieltjes/Pade moment-threshold certificate is absent; "
                "current inverse proxy fails complete-Bernstein monotonicity"
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
                "Higgs/taste condensate stack has zero projection from the PR230 uniform mass source onto the trace-zero taste-Higgs axes",
                "origin/main composite-Higgs stretch packet is cross-lane conditional context, not PR230 O_H/C_sH/C_HH authority",
            ],
            "parents": [
                PARENTS["source_higgs_readiness"],
                PARENTS["source_higgs_gram"],
                PARENTS["source_higgs_postprocess"],
                PARENTS["source_higgs_unratified_gram_no_go"],
                PARENTS["pr230_genuine_source_pole_artifact_intake"],
                PARENTS["canonical_higgs_semantic_firewall"],
                PARENTS["cross_lane_oh_authority_audit"],
                PARENTS["canonical_oh_premise_stretch"],
                PARENTS["pr230_taste_condensate_oh_bridge_audit"],
                PARENTS["pr230_origin_main_composite_higgs_intake_guard"],
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
                "origin/main EW M-residual CMT/Fierz packet is context-only and admits missing EW Wilson-line construction",
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
                "bare-to-low-scale g2 running bridge not derivable without EW action, scale, thresholds, and matching",
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
                PARENTS["pr230_origin_main_ew_m_residual_intake_guard"],
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
                PARENTS["wz_g2_bare_running_bridge_attempt"],
                PARENTS["same_source_sector_overlap"],
            ],
        },
        "schur_kprime_kernel_rows": {
            "passes_current_surface": truth(certs["schur_kprime_rows"], "schur_kprime_row_gate_passed"),
            "blocked_by": [
                "same-surface Schur A/B/C rows absent",
                "finite FH/LSZ source rows explicitly rejected as kernel rows",
                "compressed scalar denominator and pole derivative do not reconstruct A/B/C rows",
                "outside-math row-definition machinery still lacks a same-surface neutral kernel basis and projector",
                "finite inverse A/B/C rows from C_ss/C_sx/C_xx are bounded support, not strict pole rows",
                "finite endpoint inverse rows do not determine K'(pole) without a model class and FV/IR authority",
                "canonical bridge still required after K-prime sufficiency",
            ],
            "parents": [
                PARENTS["schur_kprime_rows"],
                PARENTS["schur_kprime_sufficiency"],
                PARENTS["schur_compressed_bootstrap_no_go"],
                PARENTS["schur_abc_definition_derivation"],
                PARENTS["pr230_two_source_taste_radial_schur_abc_finite_rows"],
                PARENTS["pr230_two_source_taste_radial_schur_pole_lift_gate"],
                PARENTS["pr230_schur_route_completion"],
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
                "direct off-diagonal generator derivation attempt finds only absent or block-diagonal current rows",
                "source-only logdet Hessian leaves the second neutral source h/O_H underdetermined",
                "formal HS/logdet auxiliary scalar rewrites do not fix canonical O_H normalization or source-Higgs overlap",
                "Z3 entropy/gap/reversibility selectors either import an external principle or select a different transfer",
            ],
            "parents": [
                PARENTS["neutral_scalar_irreducibility"],
                PARENTS["neutral_scalar_primitive_cone"],
                PARENTS["neutral_scalar_primitive_cone_stretch_no_go"],
                PARENTS["neutral_scalar_burnside_irreducibility"],
                PARENTS["neutral_offdiagonal_generator_derivation"],
                PARENTS["pr230_logdet_hessian_neutral_mixing_attempt"],
                PARENTS["pr230_hs_logdet_scalar_action_normalization_no_go"],
                PARENTS["pr230_neutral_primitive_route_completion"],
                PARENTS["pr230_z3_lazy_selector_no_go"],
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
    block53_residual_minimality_not_closure = (
        certs["block53_lane1_residual_minimality"].get("proposal_allowed") is False
        and certs["block53_lane1_residual_minimality"].get("bare_retained_allowed")
        is False
        and certs["block53_lane1_residual_minimality"].get(
            "block53_residual_minimality_gate_passed"
        )
        is True
        and certs["block53_lane1_residual_minimality"].get("current_support_closed")
        is True
        and certs["block53_lane1_residual_minimality"].get("closure_not_authorized")
        is True
    )
    block54_response_readout_reduction_not_closure = (
        certs["block54_response_readout_reduction"].get("proposal_allowed") is False
        and certs["block54_response_readout_reduction"].get("bare_retained_allowed")
        is False
        and certs["block54_response_readout_reduction"].get(
            "response_readout_root_reduction_passed"
        )
        is True
        and certs["block54_response_readout_reduction"].get(
            "response_side_support_closed"
        )
        is True
        and certs["block54_response_readout_reduction"].get(
            "readout_switch_authorized"
        )
        is False
        and set(
            certs["block54_response_readout_reduction"].get(
                "remaining_roots_after_reduction", []
            )
        )
        == {
            "scalar pole/model-class/FV/IR authority",
            "canonical-Higgs pole identity or same-surface neutral-transfer bridge",
        }
    )
    block55_canonical_neutral_cut_not_closure = (
        certs["block55_canonical_neutral_primitive_cut"].get("proposal_allowed")
        is False
        and certs["block55_canonical_neutral_primitive_cut"].get(
            "bare_retained_allowed"
        )
        is False
        and certs["block55_canonical_neutral_primitive_cut"].get(
            "block55_canonical_neutral_primitive_cut_passed"
        )
        is True
        and certs["block55_canonical_neutral_primitive_cut"].get(
            "canonical_neutral_root_closed"
        )
        is False
        and set(
            certs["block55_canonical_neutral_primitive_cut"].get(
                "remaining_canonical_neutral_obligations", []
            )
        )
        == {
            "accepted same-surface canonical O_H/action/LSZ certificate",
            "or same-surface primitive neutral transfer / irreducible cone certificate",
            "strict physical C_ss/C_sH/C_HH(tau) rows or equivalent source-overlap theorem",
        }
    )
    block56_scalar_fvir_cut_not_closure = (
        "scalar-pole-FVIR root cut"
        in statuses["block56_scalar_pole_fvir_root_cut"]
        and certs["block56_scalar_pole_fvir_root_cut"].get("proposal_allowed")
        is False
        and certs["block56_scalar_pole_fvir_root_cut"].get("bare_retained_allowed")
        is False
        and certs["block56_scalar_pole_fvir_root_cut"].get(
            "block56_scalar_pole_fvir_root_cut_passed"
        )
        is True
        and certs["block56_scalar_pole_fvir_root_cut"].get(
            "scalar_pole_fvir_root_closed"
        )
        is False
        and "same-surface scalar denominator/contact/subtraction theorem"
        in certs["block56_scalar_pole_fvir_root_cut"].get(
            "remaining_scalar_authority_obligations", []
        )
    )
    block57_compact_foundation_support_not_closure = (
        "compact finite-volume scalar-source functional foundation"
        in statuses["block57_compact_source_functional_foundation"]
        and certs["block57_compact_source_functional_foundation"].get(
            "proposal_allowed"
        )
        is False
        and certs["block57_compact_source_functional_foundation"].get(
            "bare_retained_allowed"
        )
        is False
        and certs["block57_compact_source_functional_foundation"].get(
            "block57_compact_source_functional_foundation_passed"
        )
        is True
        and certs["block57_compact_source_functional_foundation"].get(
            "finite_volume_compact_source_functional_defined"
        )
        is True
        and certs["block57_compact_source_functional_foundation"].get(
            "exact_denominator_or_pole_authority_present"
        )
        is False
        and certs["block57_compact_source_functional_foundation"].get(
            "scalar_pole_fvir_root_closed"
        )
        is False
    )
    block58_compact_spectral_support_not_closure = (
        "finite-volume compact source-channel spectral support"
        in statuses["block58_compact_source_spectral_support"]
        and certs["block58_compact_source_spectral_support"].get(
            "proposal_allowed"
        )
        is False
        and certs["block58_compact_source_spectral_support"].get(
            "bare_retained_allowed"
        )
        is False
        and certs["block58_compact_source_spectral_support"].get(
            "block58_compact_source_spectral_support_passed"
        )
        is True
        and certs["block58_compact_source_spectral_support"].get(
            "finite_volume_source_spectral_representation_present"
        )
        is True
        and certs["block58_compact_source_spectral_support"].get(
            "thermodynamic_limit_authority_present"
        )
        is False
        and certs["block58_compact_source_spectral_support"].get(
            "isolated_pole_residue_authority_present"
        )
        is False
        and certs["block58_compact_source_spectral_support"].get(
            "canonical_oh_authority_present"
        )
        is False
        and certs["block58_compact_source_spectral_support"].get(
            "scalar_pole_fvir_root_closed"
        )
        is False
    )
    block59_source_spectral_pole_promotion_blocks = (
        "finite-volume source spectral positivity does not promote"
        in statuses["block59_source_spectral_pole_promotion_obstruction"]
        and certs["block59_source_spectral_pole_promotion_obstruction"].get(
            "proposal_allowed"
        )
        is False
        and certs["block59_source_spectral_pole_promotion_obstruction"].get(
            "bare_retained_allowed"
        )
        is False
        and certs["block59_source_spectral_pole_promotion_obstruction"].get(
            "block59_source_spectral_pole_promotion_obstruction_passed"
        )
        is True
        and certs["block59_source_spectral_pole_promotion_obstruction"].get(
            "finite_volume_source_spectral_support_loaded"
        )
        is True
        and certs["block59_source_spectral_pole_promotion_obstruction"].get(
            "thermodynamic_pole_authority_present"
        )
        is False
        and certs["block59_source_spectral_pole_promotion_obstruction"].get(
            "uniform_threshold_gap_authority_present"
        )
        is False
        and certs["block59_source_spectral_pole_promotion_obstruction"].get(
            "residue_lower_bound_certified"
        )
        is False
        and certs["block59_source_spectral_pole_promotion_obstruction"].get(
            "canonical_oh_authority_present"
        )
        is False
    )
    block60_source_carrier_support_not_closure = (
        "compact additive source fixes the source-channel taste-singlet carrier"
        in statuses["block60_compact_source_taste_singlet_carrier"]
        and certs["block60_compact_source_taste_singlet_carrier"].get(
            "proposal_allowed"
        )
        is False
        and certs["block60_compact_source_taste_singlet_carrier"].get(
            "source_channel_taste_carrier_fixed"
        )
        is True
        and certs["block60_compact_source_taste_singlet_carrier"].get(
            "canonical_oh_authority_present"
        )
        is False
        and certs["block60_compact_source_taste_singlet_carrier"].get(
            "pole_residue_authority_present"
        )
        is False
        and certs["block60_compact_source_taste_singlet_carrier"].get(
            "kprime_authority_present"
        )
        is False
        and certs["block60_compact_source_taste_singlet_carrier"].get(
            "threshold_fvir_authority_present"
        )
        is False
    )
    block61_post_carrier_kprime_blocks = (
        "source-carrier support does not fix K-prime or pole residue"
        in statuses["block61_post_carrier_kprime_obstruction"]
        and certs["block61_post_carrier_kprime_obstruction"].get(
            "proposal_allowed"
        )
        is False
        and certs["block61_post_carrier_kprime_obstruction"].get(
            "block61_post_carrier_kprime_obstruction_passed"
        )
        is True
        and certs["block61_post_carrier_kprime_obstruction"].get(
            "source_channel_taste_carrier_fixed"
        )
        is True
        and certs["block61_post_carrier_kprime_obstruction"].get(
            "kprime_authority_present"
        )
        is False
        and certs["block61_post_carrier_kprime_obstruction"].get(
            "pole_residue_authority_present"
        )
        is False
    )
    block62_compact_source_kprime_identifiability_blocks = (
        "compact source support and fixed carrier do not identify K-prime or pole residue"
        in statuses["block62_compact_source_kprime_identifiability_obstruction"]
        and certs["block62_compact_source_kprime_identifiability_obstruction"].get(
            "proposal_allowed"
        )
        is False
        and certs["block62_compact_source_kprime_identifiability_obstruction"].get(
            "block62_compact_source_kprime_identifiability_obstruction_passed"
        )
        is True
        and certs["block62_compact_source_kprime_identifiability_obstruction"].get(
            "compact_source_support_loaded"
        )
        is True
        and certs["block62_compact_source_kprime_identifiability_obstruction"].get(
            "finite_spectral_support_loaded"
        )
        is True
        and certs["block62_compact_source_kprime_identifiability_obstruction"].get(
            "source_channel_taste_carrier_fixed"
        )
        is True
        and certs["block62_compact_source_kprime_identifiability_obstruction"].get(
            "kprime_authority_present"
        )
        is False
        and certs["block62_compact_source_kprime_identifiability_obstruction"].get(
            "pole_residue_authority_present"
        )
        is False
    )
    finite_source_support = (
        certs["fh_lsz_finite_source_linearity"].get("finite_source_linearity_gate_passed") is True
        or "support" in statuses["fh_lsz_finite_source_linearity"]
    )
    ess_support = (
        certs["fh_lsz_target_ess"].get("target_observable_ess_gate_passed") is True
        or "ESS" in statuses["fh_lsz_target_ess"]
    )
    full_target_timeseries_support = (
        certs["fh_lsz_target_timeseries_full_set"].get("proposal_allowed") is False
        and certs["fh_lsz_target_timeseries_full_set"].get("schema_summary", {}).get(
            "checked_chunks"
        )
        == 63
        and certs["fh_lsz_target_timeseries_full_set"].get("replacement_queue") == []
    )
    polefit_support_only = (
        certs["fh_lsz_polefit8x8_combiner"].get("proposal_allowed") is False
        and certs["fh_lsz_polefit8x8_postprocessor"].get("proposal_allowed") is False
        and "eight-mode" in statuses["fh_lsz_polefit8x8_postprocessor"]
    )
    genuine_source_pole_support_only = (
        certs["pr230_genuine_source_pole_artifact_intake"].get(
            "artifact_is_genuine_current_surface_support"
        )
        is True
        and certs["pr230_genuine_source_pole_artifact_intake"].get(
            "artifact_is_physics_closure"
        )
        is False
        and certs["pr230_genuine_source_pole_artifact_intake"].get(
            "proposal_allowed"
        )
        is False
    )
    l12_chunk_compute_support_only = (
        "completed L12 same-source chunk compute status"
        in statuses["pr230_l12_chunk_compute_status"]
        and certs["pr230_l12_chunk_compute_status"].get("proposal_allowed")
        is False
        and certs["pr230_l12_chunk_compute_status"].get(
            "strict_closure_blockers", {}
        ).get("scalar_lsz_denominator_certificate_absent")
        is True
        and certs["pr230_l12_chunk_compute_status"].get(
            "strict_closure_blockers", {}
        ).get("canonical_oh_or_source_higgs_overlap_absent")
        is True
    )
    negative_route_applicability_review_passed = (
        "negative-route applicability review passed"
        in statuses["pr230_negative_route_applicability_review"]
        and certs["pr230_negative_route_applicability_review"].get("proposal_allowed")
        is False
        and certs["pr230_negative_route_applicability_review"].get(
            "negative_results_are_current_surface_blockers_only"
        )
        is True
        and certs["pr230_negative_route_applicability_review"].get(
            "future_reopen_paths_preserved"
        )
        is True
        and certs["pr230_negative_route_applicability_review"].get(
            "no_retained_negative_overclaim"
        )
        is True
    )
    taste_condensate_oh_bridge_blocks_shortcut = (
        "taste-condensate Higgs stack does not supply PR230 O_H bridge"
        in statuses["pr230_taste_condensate_oh_bridge_audit"]
        and certs["pr230_taste_condensate_oh_bridge_audit"].get("proposal_allowed")
        is False
        and certs["pr230_taste_condensate_oh_bridge_audit"].get(
            "taste_condensate_oh_bridge_audit_passed"
        )
        is True
        and certs["pr230_taste_condensate_oh_bridge_audit"].get("algebra", {}).get(
            "uniform_source_relative_projection_onto_taste_axis_span"
        )
        == 0.0
    )
    source_coordinate_transport_blocks_current_shortcut = (
        "source-coordinate transport to canonical O_H not derivable"
        in statuses["pr230_source_coordinate_transport_gate"]
        and certs["pr230_source_coordinate_transport_gate"].get("proposal_allowed")
        is False
        and certs["pr230_source_coordinate_transport_gate"].get(
            "source_coordinate_transport_gate_passed"
        )
        is True
        and certs["pr230_source_coordinate_transport_gate"].get(
            "future_transport_certificate_present"
        )
        is False
    )
    origin_main_composite_higgs_not_closure = (
        "origin/main composite-Higgs stretch"
        in statuses["pr230_origin_main_composite_higgs_intake_guard"]
        and certs["pr230_origin_main_composite_higgs_intake_guard"].get("proposal_allowed")
        is False
        and certs["pr230_origin_main_composite_higgs_intake_guard"].get(
            "origin_main_composite_higgs_intake_guard_passed"
        )
        is True
        and certs["pr230_origin_main_composite_higgs_intake_guard"].get(
            "origin_main_composite_higgs_closes_pr230"
        )
        is False
    )
    origin_main_ew_m_residual_not_closure = (
        "origin/main EW M-residual CMT packet"
        in statuses["pr230_origin_main_ew_m_residual_intake_guard"]
        and certs["pr230_origin_main_ew_m_residual_intake_guard"].get(
            "proposal_allowed"
        )
        is False
        and certs["pr230_origin_main_ew_m_residual_intake_guard"].get(
            "origin_main_ew_m_residual_intake_guard_passed"
        )
        is True
        and certs["pr230_origin_main_ew_m_residual_intake_guard"].get(
            "origin_main_ew_m_residual_closes_pr230"
        )
        is False
    )
    z3_triplet_conditional_primitive_not_closure = (
        "Z3-triplet primitive-cone theorem"
        in statuses["pr230_z3_triplet_conditional_primitive_cone"]
        and certs["pr230_z3_triplet_conditional_primitive_cone"].get(
            "proposal_allowed"
        )
        is False
        and certs["pr230_z3_triplet_conditional_primitive_cone"].get(
            "z3_triplet_conditional_primitive_theorem_passed"
        )
        is True
        and certs["pr230_z3_triplet_conditional_primitive_cone"].get(
            "pr230_closure_authorized"
        )
        is False
        and certs["pr230_z3_triplet_conditional_primitive_cone"].get(
            "writes_strict_future_certificate"
        )
        is False
    )
    z3_triplet_positive_cone_h2_support_not_transfer = (
        "Z3-triplet positive-cone H2 support"
        in statuses["pr230_z3_triplet_positive_cone_support"]
        and certs["pr230_z3_triplet_positive_cone_support"].get("proposal_allowed")
        is False
        and certs["pr230_z3_triplet_positive_cone_support"].get(
            "z3_triplet_positive_cone_h2_support_passed"
        )
        is True
        and certs["pr230_z3_triplet_positive_cone_support"].get(
            "pr230_closure_authorized"
        )
        is False
        and certs["pr230_z3_triplet_positive_cone_support"].get(
            "supplies_conditional_premises", {}
        ).get("H2_positive_cone_equal_magnitude_support")
        is True
        and certs["pr230_z3_triplet_positive_cone_support"].get(
            "supplies_conditional_premises", {}
        ).get("H3_lazy_positive_physical_transfer")
        is False
    )
    z3_generation_action_lift_not_derived = (
        "Z3 generation-action lift"
        in statuses["pr230_z3_generation_action_lift_attempt"]
        and certs["pr230_z3_generation_action_lift_attempt"].get(
            "proposal_allowed"
        )
        is False
        and certs["pr230_z3_generation_action_lift_attempt"].get(
            "h1_generation_action_lift_attempt_passed"
        )
        is True
        and certs["pr230_z3_generation_action_lift_attempt"].get(
            "same_surface_h1_derived"
        )
        is False
        and certs["pr230_z3_generation_action_lift_attempt"].get(
            "pr230_closure_authorized"
        )
        is False
    )
    z3_lazy_transfer_promotion_not_derived = (
        "Z3 lazy-transfer promotion not derivable"
        in statuses["pr230_z3_lazy_transfer_promotion_attempt"]
        and certs["pr230_z3_lazy_transfer_promotion_attempt"].get(
            "proposal_allowed"
        )
        is False
        and certs["pr230_z3_lazy_transfer_promotion_attempt"].get(
            "z3_lazy_transfer_promotion_attempt_passed"
        )
        is True
        and certs["pr230_z3_lazy_transfer_promotion_attempt"].get(
            "physical_lazy_transfer_instantiated"
        )
        is False
        and certs["pr230_z3_lazy_transfer_promotion_attempt"].get(
            "pr230_closure_authorized"
        )
        is False
    )
    z3_lazy_selector_no_go_blocks = (
        "Z3 lazy selector shortcuts do not derive"
        in statuses["pr230_z3_lazy_selector_no_go"]
        and certs["pr230_z3_lazy_selector_no_go"].get("proposal_allowed")
        is False
        and certs["pr230_z3_lazy_selector_no_go"].get(
            "z3_lazy_selector_no_go_passed"
        )
        is True
        and certs["pr230_z3_lazy_selector_no_go"].get(
            "physical_lazy_transfer_instantiated"
        )
        is False
        and certs["pr230_z3_lazy_selector_no_go"].get("pr230_closure_authorized")
        is False
    )
    same_surface_z3_taste_triplet_support_not_closure = (
        "same-surface Z3 taste-triplet artifact"
        in statuses["pr230_same_surface_z3_taste_triplet"]
        and certs["pr230_same_surface_z3_taste_triplet"].get("proposal_allowed")
        is False
        and certs["pr230_same_surface_z3_taste_triplet"].get(
            "same_surface_z3_triplet_artifact_passed"
        )
        is True
        and certs["pr230_same_surface_z3_taste_triplet"].get(
            "pr230_closure_authorized"
        )
        is False
    )
    source_coordinate_transport_completion_blocks = (
        "source-coordinate transport not derivable from current PR230 surface"
        in statuses["pr230_source_coordinate_transport_completion"]
        and certs["pr230_source_coordinate_transport_completion"].get("proposal_allowed")
        is False
        and certs["pr230_source_coordinate_transport_completion"].get(
            "source_coordinate_transport_completion_passed"
        )
        is True
        and certs["pr230_source_coordinate_transport_completion"].get("algebra", {}).get(
            "source_relative_projection_onto_taste_axis_span"
        )
        == 0.0
    )
    two_source_taste_radial_chart_support_not_closure = (
        "two-source taste-radial chart"
        in statuses["pr230_two_source_taste_radial_chart"]
        and certs["pr230_two_source_taste_radial_chart"].get("proposal_allowed")
        is False
        and certs["pr230_two_source_taste_radial_chart"].get(
            "two_source_taste_radial_chart_support_passed"
        )
        is True
        and certs["pr230_two_source_taste_radial_chart"].get(
            "forbidden_firewall", {}
        ).get("identified_taste_radial_axis_with_canonical_oh")
        is False
        and certs["pr230_two_source_taste_radial_chart"].get(
            "future_file_presence", {}
        ).get("taste_radial_measurement_rows")
        is False
    )
    two_source_taste_radial_action_support_not_closure = (
        "two-source taste-radial action source vertex"
        in statuses["pr230_two_source_taste_radial_action"]
        and certs["pr230_two_source_taste_radial_action"].get("proposal_allowed")
        is False
        and certs["pr230_two_source_taste_radial_action"].get(
            "two_source_taste_radial_action_passed"
        )
        is True
        and certs["pr230_two_source_taste_radial_action"].get(
            "operator_certificate_payload", {}
        ).get("canonical_higgs_operator_identity_passed")
        is False
        and certs["pr230_two_source_taste_radial_action"].get(
            "future_file_presence", {}
        ).get("taste_radial_measurement_rows")
        is False
    )
    two_source_taste_radial_row_contract_support_not_closure = (
        "two-source taste-radial C_sx/C_xx row contract"
        in statuses["pr230_two_source_taste_radial_row_contract"]
        and certs["pr230_two_source_taste_radial_row_contract"].get("proposal_allowed")
        is False
        and certs["pr230_two_source_taste_radial_row_contract"].get(
            "two_source_taste_radial_row_contract_passed"
        )
        is True
        and certs["pr230_two_source_taste_radial_row_contract"].get(
            "future_file_presence", {}
        ).get("taste_radial_production_rows")
        is False
    )
    two_source_taste_radial_row_manifest_support_not_closure = (
        "two-source taste-radial C_sx/C_xx production manifest"
        in statuses["pr230_two_source_taste_radial_row_production_manifest"]
        and certs["pr230_two_source_taste_radial_row_production_manifest"].get(
            "proposal_allowed"
        )
        is False
        and certs["pr230_two_source_taste_radial_row_production_manifest"].get(
            "manifest_passed"
        )
        is True
        and certs["pr230_two_source_taste_radial_row_production_manifest"].get(
            "dry_run_only"
        )
        is True
        and certs["pr230_two_source_taste_radial_row_production_manifest"].get(
            "future_combined_rows_present"
        )
        is False
    )
    two_source_taste_radial_schur_subblock_support_not_closure = (
        "two-source taste-radial Schur-subblock witness"
        in statuses["pr230_two_source_taste_radial_schur_subblock_witness"]
        and certs["pr230_two_source_taste_radial_schur_subblock_witness"].get(
            "proposal_allowed"
        )
        is False
        and certs["pr230_two_source_taste_radial_schur_subblock_witness"].get(
            "two_source_taste_radial_schur_subblock_witness_passed"
        )
        is True
        and certs["pr230_two_source_taste_radial_schur_subblock_witness"].get(
            "strict_schur_kernel_row_contract_passed"
        )
        is False
        and certs["pr230_two_source_taste_radial_schur_subblock_witness"].get(
            "canonical_higgs_operator_identity_passed"
        )
        is False
    )
    two_source_taste_radial_kprime_scout_not_closure = (
        "finite-shell Schur inverse-slope scout"
        in statuses["pr230_two_source_taste_radial_schur_kprime_finite_shell_scout"]
        and certs["pr230_two_source_taste_radial_schur_kprime_finite_shell_scout"].get(
            "proposal_allowed"
        )
        is False
        and certs["pr230_two_source_taste_radial_schur_kprime_finite_shell_scout"].get(
            "finite_shell_schur_kprime_scout_passed"
        )
        is True
        and certs["pr230_two_source_taste_radial_schur_kprime_finite_shell_scout"].get(
            "strict_schur_kprime_authority_passed"
        )
        is False
        and certs["pr230_two_source_taste_radial_schur_kprime_finite_shell_scout"].get(
            "pole_location_or_derivative_rows_present"
        )
        is False
        and certs["pr230_two_source_taste_radial_schur_kprime_finite_shell_scout"].get(
            "canonical_higgs_operator_identity_passed"
        )
        is False
    )
    two_source_taste_radial_schur_abc_finite_rows_not_closure = (
        "finite Schur A/B/C inverse-block rows"
        in statuses["pr230_two_source_taste_radial_schur_abc_finite_rows"]
        and certs["pr230_two_source_taste_radial_schur_abc_finite_rows"].get(
            "proposal_allowed"
        )
        is False
        and certs["pr230_two_source_taste_radial_schur_abc_finite_rows"].get(
            "two_source_taste_radial_schur_abc_finite_rows_passed"
        )
        is True
        and certs["pr230_two_source_taste_radial_schur_abc_finite_rows"].get(
            "finite_schur_abc_rows_written"
        )
        is True
        and certs["pr230_two_source_taste_radial_schur_abc_finite_rows"].get(
            "strict_schur_abc_kernel_rows_written"
        )
        is False
        and certs["pr230_two_source_taste_radial_schur_abc_finite_rows"].get(
            "strict_schur_kprime_authority_passed"
        )
        is False
        and certs["pr230_two_source_taste_radial_schur_abc_finite_rows"].get(
            "canonical_higgs_operator_identity_passed"
        )
        is False
    )
    two_source_taste_radial_schur_pole_lift_gate_blocks_endpoint_promotion = (
        "finite Schur A/B/C rows do not lift to strict pole-row authority"
        in statuses["pr230_two_source_taste_radial_schur_pole_lift_gate"]
        and certs["pr230_two_source_taste_radial_schur_pole_lift_gate"].get(
            "proposal_allowed"
        )
        is False
        and certs["pr230_two_source_taste_radial_schur_pole_lift_gate"].get(
            "two_source_taste_radial_schur_pole_lift_gate_passed"
        )
        is True
        and certs["pr230_two_source_taste_radial_schur_pole_lift_gate"].get(
            "strict_pole_lift_passed"
        )
        is False
        and certs["pr230_two_source_taste_radial_schur_pole_lift_gate"].get(
            "endpoint_derivative_nonidentifiability_witness_passed"
        )
        is True
    )
    two_source_taste_radial_primitive_transfer_candidate_not_h3 = (
        "finite C_sx rows do not certify a physical primitive neutral transfer"
        in statuses["pr230_two_source_taste_radial_primitive_transfer_candidate_gate"]
        and certs["pr230_two_source_taste_radial_primitive_transfer_candidate_gate"].get(
            "proposal_allowed"
        )
        is False
        and certs["pr230_two_source_taste_radial_primitive_transfer_candidate_gate"].get(
            "physical_transfer_candidate_accepted"
        )
        is False
        and certs["pr230_two_source_taste_radial_primitive_transfer_candidate_gate"].get(
            "finite_offdiagonal_correlation_support"
        )
        is True
        and certs["pr230_two_source_taste_radial_primitive_transfer_candidate_gate"].get(
            "finite_correlator_blocks_positive"
        )
        is True
    )
    orthogonal_top_coupling_exclusion_candidate_rejected = (
        "orthogonal-neutral top-coupling exclusion candidate rejected"
        in statuses["pr230_orthogonal_top_coupling_exclusion_candidate_gate"]
        and certs["pr230_orthogonal_top_coupling_exclusion_candidate_gate"].get(
            "proposal_allowed"
        )
        is False
        and certs["pr230_orthogonal_top_coupling_exclusion_candidate_gate"].get(
            "orthogonal_top_coupling_exclusion_candidate_accepted"
        )
        is False
        and certs["pr230_orthogonal_top_coupling_exclusion_candidate_gate"].get(
            "finite_c_sx_rows_are_top_coupling_tomography"
        )
        is False
    )
    strict_scalar_lsz_moment_fv_authority_absent = (
        "raw C_ss rows do not supply strict scalar-LSZ moment/FV authority"
        in statuses["pr230_strict_scalar_lsz_moment_fv_authority_gate"]
        and certs["pr230_strict_scalar_lsz_moment_fv_authority_gate"].get(
            "proposal_allowed"
        )
        is False
        and certs["pr230_strict_scalar_lsz_moment_fv_authority_gate"].get(
            "strict_scalar_lsz_moment_fv_authority_gate_passed"
        )
        is True
        and certs["pr230_strict_scalar_lsz_moment_fv_authority_gate"].get(
            "strict_scalar_lsz_moment_fv_authority_present"
        )
        is False
        and certs["pr230_strict_scalar_lsz_moment_fv_authority_gate"].get(
            "current_raw_c_ss_proxy_fails_stieltjes_monotonicity"
        )
        is True
    )
    two_source_taste_radial_chunk_package_support_not_closure = (
        "two-source taste-radial chunks001-"
        in statuses["pr230_two_source_taste_radial_chunk_package"]
        and certs["pr230_two_source_taste_radial_chunk_package"].get(
            "chunk_package_audit_passed"
        )
        is True
        and certs["pr230_two_source_taste_radial_chunk_package"].get(
            "completed_chunk_count", 0
        )
        >= 20
        and certs["pr230_two_source_taste_radial_chunk_package"].get(
            "active_chunks_counted_as_evidence"
        )
        is False
        and certs["pr230_two_source_taste_radial_chunk_package"].get(
            "proposal_allowed"
        )
        is False
    )
    source_higgs_pole_row_contract_open = (
        "source-Higgs C_ss/C_sH/C_HH pole-row acceptance contract"
        in statuses["pr230_source_higgs_pole_row_acceptance_contract"]
        and certs["pr230_source_higgs_pole_row_acceptance_contract"].get(
            "source_higgs_pole_row_acceptance_contract_passed"
        )
        is True
        and certs["pr230_source_higgs_pole_row_acceptance_contract"].get(
            "closure_contract_satisfied"
        )
        is False
        and certs["pr230_source_higgs_pole_row_acceptance_contract"].get(
            "proposal_allowed"
        )
        is False
    )
    schur_complement_stieltjes_repair_support_not_closure = (
        "Schur-complement Stieltjes repair split"
        in statuses["pr230_schur_complement_stieltjes_repair_gate"]
        and certs["pr230_schur_complement_stieltjes_repair_gate"].get(
            "proposal_allowed"
        )
        is False
        and certs["pr230_schur_complement_stieltjes_repair_gate"].get(
            "schur_complement_stieltjes_repair_gate_passed"
        )
        is True
        and certs["pr230_schur_complement_stieltjes_repair_gate"].get(
            "source_given_x_stieltjes_first_shell_failed"
        )
        is True
        and certs["pr230_schur_complement_stieltjes_repair_gate"].get(
            "x_given_source_stieltjes_first_shell_passed"
        )
        is True
        and certs["pr230_schur_complement_stieltjes_repair_gate"].get(
            "strict_scalar_lsz_authority_present"
        )
        is False
        and certs["pr230_schur_complement_stieltjes_repair_gate"].get(
            "canonical_higgs_operator_identity_passed"
        )
        is False
    )
    schur_complement_complete_monotonicity_support_not_closure = (
        "C_x|s Schur residual passes"
        in statuses["pr230_schur_complement_complete_monotonicity_gate"]
        and certs["pr230_schur_complement_complete_monotonicity_gate"].get(
            "proposal_allowed"
        )
        is False
        and certs["pr230_schur_complement_complete_monotonicity_gate"].get(
            "schur_complement_complete_monotonicity_gate_passed"
        )
        is True
        and certs["pr230_schur_complement_complete_monotonicity_gate"].get(
            "complete_monotonicity_authority_passed"
        )
        is False
        and certs["pr230_schur_complement_complete_monotonicity_gate"].get(
            "canonical_higgs_or_physical_response_bridge_present"
        )
        is False
    )
    schur_x_given_source_one_pole_scout_not_authority = (
        "one-pole finite-residue scout"
        in statuses["pr230_schur_x_given_source_one_pole_scout"]
        and certs["pr230_schur_x_given_source_one_pole_scout"].get(
            "proposal_allowed"
        )
        is False
        and certs["pr230_schur_x_given_source_one_pole_scout"].get(
            "schur_x_given_source_one_pole_scout_passed"
        )
        is True
        and certs["pr230_schur_x_given_source_one_pole_scout"].get(
            "one_pole_fit_valid"
        )
        is True
        and certs["pr230_schur_x_given_source_one_pole_scout"].get(
            "one_pole_model_class_authority_passed"
        )
        is False
        and certs["pr230_schur_x_given_source_one_pole_scout"].get(
            "two_pole_counterfamily_present"
        )
        is True
        and certs["pr230_schur_x_given_source_one_pole_scout"].get(
            "physical_pole_residue_authority_present"
        )
        is False
    )
    taste_radial_canonical_oh_selector_blocks_symmetry_shortcut = (
        "degree-one taste-radial uniqueness"
        in statuses["pr230_taste_radial_canonical_oh_selector_gate"]
        and certs["pr230_taste_radial_canonical_oh_selector_gate"].get(
            "proposal_allowed"
        )
        is False
        and certs["pr230_taste_radial_canonical_oh_selector_gate"].get(
            "taste_radial_canonical_oh_selector_gate_passed"
        )
        is True
        and certs["pr230_taste_radial_canonical_oh_selector_gate"].get(
            "degree_one_radial_unique"
        )
        is True
        and certs["pr230_taste_radial_canonical_oh_selector_gate"].get(
            "full_invariant_selector_nonunique"
        )
        is True
        and certs["pr230_taste_radial_canonical_oh_selector_gate"].get(
            "canonical_oh_selector_absent"
        )
        is True
    )
    degree_one_higgs_action_premise_not_derived = (
        "degree-one Higgs-action premise not derived"
        in statuses["pr230_degree_one_higgs_action_premise_gate"]
        and certs["pr230_degree_one_higgs_action_premise_gate"].get(
            "proposal_allowed"
        )
        is False
        and certs["pr230_degree_one_higgs_action_premise_gate"].get(
            "degree_one_higgs_action_premise_gate_passed"
        )
        is True
        and certs["pr230_degree_one_higgs_action_premise_gate"].get(
            "degree_one_filter_selects_e1"
        )
        is True
        and certs["pr230_degree_one_higgs_action_premise_gate"].get(
            "degree_one_premise_authorized_on_current_surface"
        )
        is False
        and certs["pr230_degree_one_higgs_action_premise_gate"].get(
            "odd_parity_filter_nonunique"
        )
        is True
    )
    degree_one_radial_tangent_oh_theorem_support_not_closure = (
        "degree-one radial-tangent O_H uniqueness theorem"
        in statuses["pr230_degree_one_radial_tangent_oh_theorem"]
        and certs["pr230_degree_one_radial_tangent_oh_theorem"].get(
            "proposal_allowed"
        )
        is False
        and certs["pr230_degree_one_radial_tangent_oh_theorem"].get(
            "degree_one_radial_tangent_oh_theorem_passed"
        )
        is True
        and certs["pr230_degree_one_radial_tangent_oh_theorem"].get(
            "degree_one_tangent_unique"
        )
        is True
        and certs["pr230_degree_one_radial_tangent_oh_theorem"].get(
            "same_surface_linear_tangent_premise_derived"
        )
        is False
        and certs["pr230_degree_one_radial_tangent_oh_theorem"].get(
            "canonical_oh_identity_derived"
        )
        is False
        and certs["pr230_degree_one_radial_tangent_oh_theorem"].get(
            "source_higgs_pole_rows_present"
        )
        is False
    )
    taste_radial_to_source_higgs_promotion_contract_support_not_closure = (
        "taste-radial-to-source-Higgs promotion contract"
        in statuses["pr230_taste_radial_to_source_higgs_promotion_contract"]
        and certs["pr230_taste_radial_to_source_higgs_promotion_contract"].get(
            "promotion_contract_passed"
        )
        is True
        and certs["pr230_taste_radial_to_source_higgs_promotion_contract"].get(
            "current_promotion_allowed"
        )
        is False
        and certs["pr230_taste_radial_to_source_higgs_promotion_contract"].get(
            "proposal_allowed"
        )
        is False
        and "same_surface_canonical_O_H_identity_absent"
        in certs["pr230_taste_radial_to_source_higgs_promotion_contract"].get(
            "current_promotion_blockers", []
        )
        and certs["pr230_taste_radial_to_source_higgs_promotion_contract"].get(
            "row_packet_status", {}
        ).get("canonical_source_higgs_rows_present")
        is False
    )
    fms_post_degree_route_support_not_closure = (
        "FMS post-degree route rescore"
        in statuses["pr230_fms_post_degree_route_rescore"]
        and certs["pr230_fms_post_degree_route_rescore"].get("proposal_allowed")
        is False
        and certs["pr230_fms_post_degree_route_rescore"].get(
            "fms_post_degree_route_rescore_passed"
        )
        is True
        and certs["pr230_fms_post_degree_route_rescore"].get(
            "forbidden_firewall", {}
        ).get("used_literature_as_proof_authority")
        is False
        and certs["pr230_fms_post_degree_route_rescore"].get(
            "forbidden_firewall", {}
        ).get("used_degree_or_odd_parity_as_oh_authority")
        is False
    )
    fms_composite_oh_conditional_support_not_closure = (
        "FMS composite O_H theorem"
        in statuses["pr230_fms_composite_oh_conditional_theorem"]
        and certs["pr230_fms_composite_oh_conditional_theorem"].get(
            "proposal_allowed"
        )
        is False
        and certs["pr230_fms_composite_oh_conditional_theorem"].get(
            "fms_composite_oh_conditional_theorem_passed"
        )
        is True
        and certs["pr230_fms_composite_oh_conditional_theorem"].get(
            "current_closure_authority_present"
        )
        is False
        and certs["pr230_fms_composite_oh_conditional_theorem"].get(
            "same_surface_action_absent"
        )
        is True
        and certs["pr230_fms_composite_oh_conditional_theorem"].get(
            "source_higgs_rows_absent"
        )
        is True
    )
    fms_oh_candidate_action_packet_support_not_closure = (
        "FMS O_H candidate/action packet"
        in statuses["pr230_fms_oh_candidate_action_packet"]
        and certs["pr230_fms_oh_candidate_action_packet"].get("proposal_allowed")
        is False
        and certs["pr230_fms_oh_candidate_action_packet"].get(
            "fms_oh_candidate_action_packet_passed"
        )
        is True
        and certs["pr230_fms_oh_candidate_action_packet"].get(
            "accepted_current_surface"
        )
        is False
        and certs["pr230_fms_oh_candidate_action_packet"].get(
            "same_surface_cl3_z3_derived"
        )
        is False
        and certs["pr230_fms_oh_candidate_action_packet"].get(
            "external_extension_required"
        )
        is True
        and certs["pr230_fms_oh_candidate_action_packet"].get(
            "closure_authorized"
        )
        is False
    )
    fms_source_overlap_readout_gate_support_not_closure = (
        "FMS source-overlap readout gate"
        in statuses["pr230_fms_source_overlap_readout_gate"]
        and certs["pr230_fms_source_overlap_readout_gate"].get("proposal_allowed")
        is False
        and certs["pr230_fms_source_overlap_readout_gate"].get(
            "fms_source_overlap_readout_gate_passed"
        )
        is True
        and certs["pr230_fms_source_overlap_readout_gate"].get(
            "readout_executable_now"
        )
        is False
        and certs["pr230_fms_source_overlap_readout_gate"].get(
            "strict_rows_present"
        )
        is False
        and certs["pr230_fms_source_overlap_readout_gate"].get(
            "closure_authorized"
        )
        is False
    )
    fms_action_adoption_minimal_cut_support_not_closure = (
        "FMS action-adoption minimal cut"
        in statuses["pr230_fms_action_adoption_minimal_cut"]
        and certs["pr230_fms_action_adoption_minimal_cut"].get("proposal_allowed")
        is False
        and certs["pr230_fms_action_adoption_minimal_cut"].get(
            "fms_action_adoption_minimal_cut_passed"
        )
        is True
        and certs["pr230_fms_action_adoption_minimal_cut"].get(
            "adoption_allowed_now"
        )
        is False
        and certs["pr230_fms_action_adoption_minimal_cut"].get(
            "accepted_current_surface"
        )
        is False
        and certs["pr230_fms_action_adoption_minimal_cut"].get(
            "same_surface_cl3_z3_derived"
        )
        is False
        and certs["pr230_fms_action_adoption_minimal_cut"].get(
            "closure_authorized"
        )
        is False
        and bool(
            certs["pr230_fms_action_adoption_minimal_cut"].get(
                "missing_root_vertices"
            )
        )
    )
    higgs_mass_source_action_bridge_support_not_closure = (
        "Higgs mass-source action bridge"
        in statuses["pr230_higgs_mass_source_action_bridge"]
        and certs["pr230_higgs_mass_source_action_bridge"].get("proposal_allowed")
        is False
        and certs["pr230_higgs_mass_source_action_bridge"].get(
            "higgs_mass_source_action_bridge_passed"
        )
        is True
        and certs["pr230_higgs_mass_source_action_bridge"].get(
            "same_surface_ew_action_certificate_absent"
        )
        is True
        and certs["pr230_higgs_mass_source_action_bridge"].get("canonical_oh_absent")
        is True
        and certs["pr230_higgs_mass_source_action_bridge"].get("source_higgs_rows_absent")
        is True
    )
    same_source_ew_higgs_action_ansatz_support_not_closure = (
        "same-source EW/Higgs action-extension ansatz"
        in statuses["pr230_same_source_ew_higgs_action_ansatz_gate"]
        and certs["pr230_same_source_ew_higgs_action_ansatz_gate"].get(
            "proposal_allowed"
        )
        is False
        and certs["pr230_same_source_ew_higgs_action_ansatz_gate"].get(
            "same_source_ew_higgs_action_ansatz_gate_passed"
        )
        is True
        and certs["pr230_same_source_ew_higgs_action_ansatz_gate"].get(
            "current_surface_adoption_passed"
        )
        is False
        and certs["pr230_same_source_ew_higgs_action_ansatz_gate"].get(
            "future_default_certificates_written"
        )
        is False
    )
    same_source_ew_action_adoption_attempt_blocks_shortcut = (
        "ansatz-only same-source EW action adoption shortcut blocked"
        in statuses["pr230_same_source_ew_action_adoption_attempt"]
        and certs["pr230_same_source_ew_action_adoption_attempt"].get(
            "proposal_allowed"
        )
        is False
        and certs["pr230_same_source_ew_action_adoption_attempt"].get(
            "same_source_ew_action_adoption_attempt_passed"
        )
        is True
        and certs["pr230_same_source_ew_action_adoption_attempt"].get(
            "adoption_allowed_now"
        )
        is False
        and certs["pr230_same_source_ew_action_adoption_attempt"].get(
            "accepted_action_certificate_written_by_this_attempt"
        )
        is False
    )
    radial_spurion_sector_overlap_support_not_closure = (
        "radial-spurion sector-overlap theorem"
        in statuses["pr230_radial_spurion_sector_overlap_theorem"]
        and certs["pr230_radial_spurion_sector_overlap_theorem"].get(
            "radial_spurion_sector_overlap_theorem_passed"
        )
        is True
        and certs["pr230_radial_spurion_sector_overlap_theorem"].get(
            "current_surface_sector_overlap_identity_supplied"
        )
        is False
        and certs["pr230_radial_spurion_sector_overlap_theorem"].get(
            "current_surface_closure_authorized"
        )
        is False
        and certs["pr230_radial_spurion_sector_overlap_theorem"].get(
            "proposal_allowed"
        )
        is False
    )
    radial_spurion_action_contract_support_not_closure = (
        "no-independent-top-source radial-spurion action contract"
        in statuses["pr230_radial_spurion_action_contract"]
        and certs["pr230_radial_spurion_action_contract"].get(
            "radial_spurion_action_contract_passed"
        )
        is True
        and certs["pr230_radial_spurion_action_contract"].get(
            "current_surface_contract_satisfied"
        )
        is False
        and certs["pr230_radial_spurion_action_contract"].get(
            "accepted_action_certificate_written"
        )
        is False
        and certs["pr230_radial_spurion_action_contract"].get("proposal_allowed")
        is False
    )
    additive_source_radial_spurion_incompatibility_support_not_closure = (
        "current additive source is incompatible"
        in statuses["pr230_additive_source_radial_spurion_incompatibility"]
        and certs["pr230_additive_source_radial_spurion_incompatibility"].get(
            "proposal_allowed"
        )
        is False
        and certs["pr230_additive_source_radial_spurion_incompatibility"].get(
            "additive_source_radial_spurion_incompatibility_passed"
        )
        is True
        and certs["pr230_additive_source_radial_spurion_incompatibility"].get(
            "forbidden_firewall", {}
        ).get("set_kappa_s_equal_one")
        is False
        and certs["pr230_additive_source_radial_spurion_incompatibility"].get(
            "forbidden_firewall", {}
        ).get("used_observed_wz_masses_or_g2")
        is False
    )
    additive_top_subtraction_row_contract_support_not_closure = (
        "additive-top subtraction row contract"
        in statuses["pr230_additive_top_subtraction_row_contract"]
        and certs["pr230_additive_top_subtraction_row_contract"].get(
            "proposal_allowed"
        )
        is False
        and certs["pr230_additive_top_subtraction_row_contract"].get(
            "additive_top_subtraction_row_contract_passed"
        )
        is True
        and certs["pr230_additive_top_subtraction_row_contract"].get(
            "current_surface_contract_satisfied"
        )
        is False
        and certs["pr230_additive_top_subtraction_row_contract"].get(
            "subtraction_identity_exact"
        )
        is True
        and certs["pr230_additive_top_subtraction_row_contract"].get(
            "matched_covariance_delta_method_valid"
        )
        is True
        and (
            certs["pr230_additive_top_subtraction_row_contract"].get(
                "future_artifact_presence", {}
            ).get("additive_top_jacobian_rows")
            is False
            or certs["pr230_additive_top_subtraction_row_contract"].get(
                "additive_top_jacobian_row_status", {}
            ).get("strict")
            is False
        )
        and certs["pr230_additive_top_subtraction_row_contract"].get(
            "future_artifact_presence", {}
        ).get("wz_response_ratio_rows")
        is False
        and certs["pr230_additive_top_subtraction_row_contract"].get(
            "future_artifact_presence", {}
        ).get("strict_electroweak_g2_certificate")
        is False
    )
    top_mass_scan_response_harness_support_not_closure = (
        "top mass-scan response harness schema gate"
        in statuses["pr230_top_mass_scan_response_harness_gate"]
        and certs["pr230_top_mass_scan_response_harness_gate"].get(
            "proposal_allowed"
        )
        is False
        and certs["pr230_top_mass_scan_response_harness_gate"].get(
            "top_mass_scan_response_harness_gate_passed"
        )
        is True
        and certs["pr230_top_mass_scan_response_harness_gate"].get(
            "row_schema_version"
        )
        == "top_mass_scan_response_v1"
    )
    top_mass_scan_subtraction_contract_applicability_blocks = (
        "top mass-scan response harness does not satisfy"
        in statuses["pr230_top_mass_scan_subtraction_contract_applicability_audit"]
        and certs[
            "pr230_top_mass_scan_subtraction_contract_applicability_audit"
        ].get("proposal_allowed")
        is False
        and certs[
            "pr230_top_mass_scan_subtraction_contract_applicability_audit"
        ].get("top_mass_scan_subtraction_contract_applicability_audit_passed")
        is True
        and certs[
            "pr230_top_mass_scan_subtraction_contract_applicability_audit"
        ].get("strict_row_presence", {}).get("wz_response_rows")
        is False
        and certs[
            "pr230_top_mass_scan_subtraction_contract_applicability_audit"
        ].get("strict_row_presence", {}).get("matched_subtraction_covariance")
        is False
        and certs[
            "pr230_top_mass_scan_subtraction_contract_applicability_audit"
        ].get("strict_row_presence", {}).get("strict_electroweak_g2_certificate")
        is False
    )
    higher_shell_source_higgs_operator_certificate_boundary_blocks = (
        "higher-shell source-Higgs cross rows use"
        in statuses["pr230_higher_shell_source_higgs_operator_certificate_boundary"]
        and certs[
            "pr230_higher_shell_source_higgs_operator_certificate_boundary"
        ].get("proposal_allowed")
        is False
        and certs[
            "pr230_higher_shell_source_higgs_operator_certificate_boundary"
        ].get("higher_shell_source_higgs_operator_certificate_boundary_passed")
        is True
        and certs[
            "pr230_higher_shell_source_higgs_operator_certificate_boundary"
        ].get("operator_certificate_summary", {}).get(
            "canonical_higgs_operator_identity_passed"
        )
        is False
    )
    post_chunks001_002_source_higgs_bridge_intake_blocks = (
        "completed higher-shell chunks001-002 are partial taste-radial"
        in statuses["pr230_post_chunks001_002_source_higgs_bridge_intake_guard"]
        and certs["pr230_post_chunks001_002_source_higgs_bridge_intake_guard"].get(
            "proposal_allowed"
        )
        is False
        and certs["pr230_post_chunks001_002_source_higgs_bridge_intake_guard"].get(
            "post_chunks001_002_source_higgs_bridge_intake_guard_passed"
        )
        is True
        and all(
            summary.get("canonical_higgs_operator_identity_passed") is False
            for summary in certs[
                "pr230_post_chunks001_002_source_higgs_bridge_intake_guard"
            ].get("row_summaries", {}).values()
        )
    )
    origin_main_yt_ward_step3_open_gate_not_closure = (
        "origin/main audited YT_WARD Step 3 row is an open_gate"
        in statuses["pr230_origin_main_yt_ward_step3_open_gate_intake_guard"]
        and certs["pr230_origin_main_yt_ward_step3_open_gate_intake_guard"].get(
            "proposal_allowed"
        )
        is False
        and certs["pr230_origin_main_yt_ward_step3_open_gate_intake_guard"].get(
            "origin_main_yt_ward_step3_open_gate_intake_guard_passed"
        )
        is True
        and certs["pr230_origin_main_yt_ward_step3_open_gate_intake_guard"].get(
            "origin_main", {}
        ).get("effective_status")
        == "open_gate"
    )
    neutral_rank_one_bypass_post_block37_blocks = (
        "post-Block37 neutral rank-one bypass not closed"
        in statuses["pr230_neutral_rank_one_bypass_post_block37_audit"]
        and certs["pr230_neutral_rank_one_bypass_post_block37_audit"].get(
            "proposal_allowed"
        )
        is False
        and certs["pr230_neutral_rank_one_bypass_post_block37_audit"].get(
            "exact_negative_boundary_passed"
        )
        is True
        and certs["pr230_neutral_rank_one_bypass_post_block37_audit"].get(
            "rank_one_bypass_closed"
        )
        is False
    )
    wz_response_ratio_identifiability_contract_support_not_closure = (
        "WZ response-ratio identifiability contract"
        in statuses["pr230_wz_response_ratio_identifiability_contract"]
        and certs["pr230_wz_response_ratio_identifiability_contract"].get(
            "wz_response_ratio_identifiability_contract_passed"
        )
        is True
        and certs["pr230_wz_response_ratio_identifiability_contract"].get(
            "current_surface_contract_satisfied"
        )
        is False
        and certs["pr230_wz_response_ratio_identifiability_contract"].get(
            "future_response_ratio_row_packet_present"
        )
        is False
        and certs["pr230_wz_response_ratio_identifiability_contract"].get(
            "strict_g2_authority_present"
        )
        is False
        and certs["pr230_wz_response_ratio_identifiability_contract"].get(
            "matched_covariance_authority_present"
        )
        is False
        and certs["pr230_wz_response_ratio_identifiability_contract"].get(
            "proposal_allowed"
        )
        is False
    )
    wz_same_source_action_minimal_certificate_cut_open = (
        "WZ accepted same-source action minimal certificate cut"
        in statuses["pr230_wz_same_source_action_minimal_certificate_cut"]
        and certs["pr230_wz_same_source_action_minimal_certificate_cut"].get(
            "wz_same_source_action_minimal_certificate_cut_passed"
        )
        is True
        and certs["pr230_wz_same_source_action_minimal_certificate_cut"].get(
            "proposal_allowed"
        )
        is False
        and certs["pr230_wz_same_source_action_minimal_certificate_cut"].get(
            "current_surface_action_certificate_satisfied"
        )
        is False
        and set(
            certs["pr230_wz_same_source_action_minimal_certificate_cut"].get(
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
        in statuses["pr230_wz_accepted_action_response_root_checkpoint"]
        and certs["pr230_wz_accepted_action_response_root_checkpoint"].get(
            "proposal_allowed"
        )
        is False
        and certs["pr230_wz_accepted_action_response_root_checkpoint"].get(
            "wz_accepted_action_response_root_checkpoint_passed"
        )
        is True
        and certs["pr230_wz_accepted_action_response_root_checkpoint"].get(
            "current_route_blocked"
        )
        is True
        and certs["pr230_wz_accepted_action_response_root_checkpoint"].get(
            "root_closures_found"
        )
        == []
        and not any(
            certs["pr230_wz_accepted_action_response_root_checkpoint"].get(
                "future_artifact_presence", {}
            ).values()
        )
    )
    canonical_oh_wz_common_action_cut_open = (
        "canonical O_H and WZ accepted-action common-cut"
        in statuses["pr230_canonical_oh_wz_common_action_cut"]
        and certs["pr230_canonical_oh_wz_common_action_cut"].get(
            "proposal_allowed"
        )
        is False
        and certs["pr230_canonical_oh_wz_common_action_cut"].get(
            "common_action_cut_passed"
        )
        is True
        and certs["pr230_canonical_oh_wz_common_action_cut"].get(
            "common_canonical_oh_vertex_open"
        )
        is True
        and certs["pr230_canonical_oh_wz_common_action_cut"].get(
            "aggregate_denies_proposal"
        )
        is True
        and certs["pr230_canonical_oh_wz_common_action_cut"].get(
            "time_kernel_manifest_not_evidence"
        )
        is True
    )
    canonical_oh_accepted_action_stretch_blocks_current_stack = (
        "canonical O_H accepted-action root not derivable"
        in statuses["pr230_canonical_oh_accepted_action_stretch_attempt"]
        and certs["pr230_canonical_oh_accepted_action_stretch_attempt"].get(
            "proposal_allowed"
        )
        is False
        and certs["pr230_canonical_oh_accepted_action_stretch_attempt"].get(
            "stretch_attempt_passed"
        )
        is True
        and certs["pr230_canonical_oh_accepted_action_stretch_attempt"].get(
            "current_route_blocked"
        )
        is True
        and certs["pr230_canonical_oh_accepted_action_stretch_attempt"].get(
            "root_closures_found"
        )
        == []
    )
    post_fms_source_overlap_necessity_blocks_current_inference = (
        "post-FMS source-overlap not derivable"
        in statuses["pr230_post_fms_source_overlap_necessity_gate"]
        and certs["pr230_post_fms_source_overlap_necessity_gate"].get(
            "proposal_allowed"
        )
        is False
        and certs["pr230_post_fms_source_overlap_necessity_gate"].get(
            "post_fms_source_overlap_necessity_gate_passed"
        )
        is True
        and certs["pr230_post_fms_source_overlap_necessity_gate"].get(
            "current_source_overlap_authority_present"
        )
        is False
        and certs["pr230_post_fms_source_overlap_necessity_gate"].get(
            "two_source_rows_are_c_sx_not_c_sH"
        )
        is True
    )
    source_higgs_overlap_kappa_contract_support_not_closure = (
        "source-Higgs overlap-kappa row contract"
        in statuses["pr230_source_higgs_overlap_kappa_contract"]
        and certs["pr230_source_higgs_overlap_kappa_contract"].get(
            "proposal_allowed"
        )
        is False
        and certs["pr230_source_higgs_overlap_kappa_contract"].get(
            "source_higgs_overlap_kappa_contract_passed"
        )
        is True
        and certs["pr230_source_higgs_overlap_kappa_contract"].get(
            "current_blockers", {}
        ).get("source_higgs_row_packet_absent")
        is True
        and certs["pr230_source_higgs_overlap_kappa_contract"].get(
            "forbidden_firewall", {}
        ).get("set_kappa_s_equal_one")
        is False
    )
    kinetic_taste_mixing_bridge_blocks_shortcut = (
        "current staggered kinetic taste symmetry"
        in statuses["pr230_kinetic_taste_mixing_bridge"]
        and certs["pr230_kinetic_taste_mixing_bridge"].get("proposal_allowed")
        is False
        and certs["pr230_kinetic_taste_mixing_bridge"].get(
            "kinetic_taste_mixing_bridge_closes_pr230"
        )
        is False
        and certs["pr230_kinetic_taste_mixing_bridge"].get(
            "exact_negative_boundary_passed"
        )
        is True
        and all(
            abs(row.get("C_sH_proxy", 1.0)) < 1.0e-12
            for row in certs["pr230_kinetic_taste_mixing_bridge"]
            .get("taste_symmetry_model", {})
            .get("cross_rows_for_representative_even_transfer", [])
        )
    )
    one_higgs_taste_axis_completeness_blocks_shortcut = (
        "one-Higgs taste-axis completeness not derived"
        in statuses["pr230_one_higgs_taste_axis_completeness"]
        and certs["pr230_one_higgs_taste_axis_completeness"].get("proposal_allowed")
        is False
        and certs["pr230_one_higgs_taste_axis_completeness"].get(
            "one_higgs_taste_axis_completeness_derived"
        )
        is False
        and certs["pr230_one_higgs_taste_axis_completeness"].get(
            "exact_negative_boundary_passed"
        )
        is True
        and certs["pr230_one_higgs_taste_axis_completeness"]
        .get("axis_permutation_checks", {})
        .get("all_axes_same_orbit")
        is True
    )
    action_first_route_completion_blocks = (
        "action-first O_H/C_sH/C_HH route not complete on current PR230 surface"
        in statuses["pr230_action_first_route_completion"]
        and certs["pr230_action_first_route_completion"].get("proposal_allowed")
        is False
        and certs["pr230_action_first_route_completion"].get(
            "action_first_route_completion_passed"
        )
        is True
    )
    wz_response_route_completion_blocks = (
        "WZ same-source response route not complete on current PR230 surface"
        in statuses["pr230_wz_response_route_completion"]
        and certs["pr230_wz_response_route_completion"].get("proposal_allowed")
        is False
        and certs["pr230_wz_response_route_completion"].get(
            "wz_response_route_completion_passed"
        )
        is True
    )
    schur_route_completion_blocks = (
        "strict Schur A/B/C route not complete"
        in statuses["pr230_schur_route_completion"]
        and certs["pr230_schur_route_completion"].get("proposal_allowed")
        is False
        and certs["pr230_schur_route_completion"].get("schur_route_completion_passed")
        is True
    )
    neutral_primitive_route_completion_blocks = (
        "neutral primitive-rank-one route not complete on current PR230 surface"
        in statuses["pr230_neutral_primitive_route_completion"]
        and certs["pr230_neutral_primitive_route_completion"].get("proposal_allowed")
        is False
        and certs["pr230_neutral_primitive_route_completion"].get(
            "neutral_primitive_route_completion_passed"
        )
        is True
    )
    oh_bridge_candidate_portfolio_open = (
        "first-principles O_H bridge positive-candidate portfolio"
        in statuses["pr230_oh_bridge_candidate_portfolio"]
        and certs["pr230_oh_bridge_candidate_portfolio"].get("proposal_allowed")
        is False
        and certs["pr230_oh_bridge_candidate_portfolio"].get(
            "candidate_portfolio_passed"
        )
        is True
        and certs["pr230_oh_bridge_candidate_portfolio"].get("candidate_count")
        == 5
    )
    same_surface_neutral_multiplicity_gate_rejects_current_surface = (
        "same-surface neutral multiplicity-one artifact intake gate"
        in statuses["pr230_same_surface_neutral_multiplicity_one_gate"]
        and certs["pr230_same_surface_neutral_multiplicity_one_gate"].get(
            "proposal_allowed"
        )
        is False
        and certs["pr230_same_surface_neutral_multiplicity_one_gate"].get(
            "candidate_accepted"
        )
        is False
    )
    os_transfer_kernel_artifact_absent = (
        "OS transfer-kernel artifact absent"
        in statuses["pr230_os_transfer_kernel_artifact_gate"]
        and certs["pr230_os_transfer_kernel_artifact_gate"].get("proposal_allowed")
        is False
        and certs["pr230_os_transfer_kernel_artifact_gate"].get(
            "os_transfer_kernel_artifact_present"
        )
        is False
        and certs["pr230_os_transfer_kernel_artifact_gate"].get(
            "same_surface_transfer_or_gevp_present"
        )
        is False
    )
    source_higgs_time_kernel_harness_support_only = (
        "source-Higgs time-kernel harness"
        in statuses["pr230_source_higgs_time_kernel_harness_extension_gate"]
        and certs["pr230_source_higgs_time_kernel_harness_extension_gate"].get(
            "proposal_allowed"
        )
        is False
        and certs["pr230_source_higgs_time_kernel_harness_extension_gate"].get(
            "contract", {}
        ).get("adds_default_off_time_kernel_rows")
        is True
        and certs["pr230_source_higgs_time_kernel_harness_extension_gate"].get(
            "contract", {}
        ).get("selected_mass_only")
        is True
        and certs["pr230_source_higgs_time_kernel_harness_extension_gate"].get(
            "used_as_physical_yukawa_readout"
        )
        is False
    )
    source_higgs_time_kernel_gevp_contract_support_only = (
        "source-Higgs time-kernel GEVP contract"
        in statuses["pr230_source_higgs_time_kernel_gevp_contract"]
        and certs["pr230_source_higgs_time_kernel_gevp_contract"].get(
            "proposal_allowed"
        )
        is False
        and certs["pr230_source_higgs_time_kernel_gevp_contract"].get(
            "formal_gevp_diagnostic", {}
        ).get("available")
        is True
        and certs["pr230_source_higgs_time_kernel_gevp_contract"].get(
            "physical_pole_extraction_accepted"
        )
        is False
    )
    source_higgs_time_kernel_production_manifest_not_evidence = (
        "source-Higgs time-kernel production manifest"
        in statuses["pr230_source_higgs_time_kernel_production_manifest"]
        and certs["pr230_source_higgs_time_kernel_production_manifest"].get(
            "proposal_allowed"
        )
        is False
        and certs["pr230_source_higgs_time_kernel_production_manifest"].get(
            "closure_launch_authorized_now"
        )
        is False
        and certs["pr230_source_higgs_time_kernel_production_manifest"].get(
            "support_launch_authorized_now"
        )
        is False
        and certs["pr230_source_higgs_time_kernel_production_manifest"].get(
            "operator_certificate_is_canonical_oh"
        )
        is False
        and certs["pr230_source_higgs_time_kernel_production_manifest"].get(
            "time_kernel_schema_version"
        )
        == "source_higgs_time_kernel_v1"
        and certs["pr230_source_higgs_time_kernel_production_manifest"].get(
            "chunk_count"
        )
        == 63
    )
    fms_literature_source_overlap_intake_non_authority = (
        "FMS literature does not supply PR230 source-overlap"
        in statuses["pr230_fms_literature_source_overlap_intake"]
        and certs["pr230_fms_literature_source_overlap_intake"].get(
            "proposal_allowed"
        )
        is False
        and certs["pr230_fms_literature_source_overlap_intake"].get(
            "literature_bridge_scope"
        )
        == "non_derivation_context_only"
        and certs["pr230_fms_literature_source_overlap_intake"].get(
            "current_blockers", {}
        ).get("canonical_oh_absent")
        is True
        and certs["pr230_fms_literature_source_overlap_intake"].get(
            "current_blockers", {}
        ).get("source_higgs_rows_absent")
        is True
    )
    schur_higher_shell_production_contract_not_evidence = (
        "higher-shell Schur scalar-LSZ production contract"
        in statuses["pr230_schur_higher_shell_production_contract"]
        and certs["pr230_schur_higher_shell_production_contract"].get(
            "proposal_allowed"
        )
        is False
        and certs["pr230_schur_higher_shell_production_contract"].get(
            "higher_shell_schur_production_contract_passed"
        )
        is True
        and certs["pr230_schur_higher_shell_production_contract"].get(
            "rows_written_by_contract"
        )
        is False
        and certs["pr230_schur_higher_shell_production_contract"].get(
            "current_four_mode_campaign_must_remain_unmixed"
        )
        is True
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
        and certs["fh_lsz_complete_bernstein_inverse_diagnostic"].get(
            "proposal_allowed"
        )
        is False
        and certs["fh_lsz_complete_bernstein_inverse_diagnostic"].get(
            "complete_bernstein_inverse_certificate_passed"
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
        and certs["pr230_action_first_oh_artifact_attempt"].get("proposal_allowed") is False
        and certs["pr230_action_first_oh_artifact_attempt"].get(
            "exact_negative_boundary_passed"
        )
        is True
        and certs["pr230_holonomic_source_response_feasibility_gate"].get("proposal_allowed")
        is False
        and certs["pr230_holonomic_source_response_feasibility_gate"].get(
            "two_source_functional_current_surface_defined"
        )
        is False
        and certs["pr230_oh_source_higgs_authority_rescan_gate"].get(
            "proposal_allowed"
        )
        is False
        and certs["pr230_oh_source_higgs_authority_rescan_gate"].get(
            "oh_source_higgs_authority_found"
        )
        is False
        and certs["pr230_oh_source_higgs_authority_rescan_gate"].get(
            "exact_negative_boundary_passed"
        )
        is True
        and certs["pr230_derived_bridge_rank_one_closure_attempt"].get(
            "proposal_allowed"
        )
        is False
        and certs["pr230_derived_bridge_rank_one_closure_attempt"].get(
            "derived_bridge_closure_passed"
        )
        is False
        and certs["pr230_derived_bridge_rank_one_closure_attempt"].get(
            "exact_negative_boundary_passed"
        )
        is True
        and certs["pr230_source_sector_pattern_transfer_gate"].get("proposal_allowed")
        is False
        and certs["pr230_source_sector_pattern_transfer_gate"].get(
            "direct_closure_available"
        )
        is False
        and certs["pr230_det_positivity_bridge_intake_gate"].get("proposal_allowed")
        is False
        and certs["pr230_det_positivity_bridge_intake_gate"].get(
            "determinant_bridge_closes_pr230"
        )
        is False
        and certs["pr230_reflection_det_primitive_upgrade_gate"].get(
            "proposal_allowed"
        )
        is False
        and certs["pr230_reflection_det_primitive_upgrade_gate"].get(
            "primitive_upgrade_passed"
        )
        is False
        and certs["pr230_reflection_det_primitive_upgrade_gate"].get(
            "exact_negative_boundary_passed"
        )
        is True
        and certs["pr230_hs_logdet_scalar_action_normalization_no_go"].get(
            "proposal_allowed"
        )
        is False
        and certs["pr230_hs_logdet_scalar_action_normalization_no_go"].get(
            "hs_logdet_scalar_action_normalization_no_go_passed"
        )
        is True
        and certs[
            "pr230_native_scalar_action_lsz_route_exhaustion_after_block40"
        ].get("proposal_allowed")
        is False
        and certs[
            "pr230_native_scalar_action_lsz_route_exhaustion_after_block40"
        ].get("native_scalar_action_lsz_route_exhaustion_passed")
        is True
        and certs["canonical_oh_premise_stretch"].get("proposal_allowed") is False
        and certs["canonical_oh_premise_stretch"].get("premise_lattice_stretch_no_go_passed")
        is True
        and certs["source_higgs_unratified_gram_no_go"].get("proposal_allowed") is False
        and certs["source_higgs_unratified_gram_no_go"].get(
            "unratified_gram_shortcut_no_go_passed"
        )
        is True
        and taste_condensate_oh_bridge_blocks_shortcut
        and source_coordinate_transport_blocks_current_shortcut
        and origin_main_composite_higgs_not_closure
        and origin_main_ew_m_residual_not_closure
        and z3_triplet_conditional_primitive_not_closure
        and z3_triplet_positive_cone_h2_support_not_transfer
        and z3_generation_action_lift_not_derived
        and z3_lazy_transfer_promotion_not_derived
        and z3_lazy_selector_no_go_blocks
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
    negative_route_review_passed = (
        certs["negative_route_applicability_review"].get("no_retained_negative_overclaim") is True
        and certs["negative_route_applicability_review"].get("future_reopen_paths_preserved") is True
        and certs["negative_route_applicability_review"].get("selected_negative_results_apply_on_current_surface") is True
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
    report(
        "block53-residual-minimality-not-closure",
        block53_residual_minimality_not_closure,
        statuses["block53_lane1_residual_minimality"],
    )
    report(
        "block54-response-readout-reduction-not-closure",
        block54_response_readout_reduction_not_closure,
        statuses["block54_response_readout_reduction"],
    )
    report(
        "block55-canonical-neutral-cut-not-closure",
        block55_canonical_neutral_cut_not_closure,
        statuses["block55_canonical_neutral_primitive_cut"],
    )
    report(
        "block56-scalar-fvir-cut-not-closure",
        block56_scalar_fvir_cut_not_closure,
        statuses["block56_scalar_pole_fvir_root_cut"],
    )
    report(
        "block57-compact-source-foundation-support-not-closure",
        block57_compact_foundation_support_not_closure,
        statuses["block57_compact_source_functional_foundation"],
    )
    report(
        "block58-compact-source-spectral-support-not-closure",
        block58_compact_spectral_support_not_closure,
        statuses["block58_compact_source_spectral_support"],
    )
    report(
        "block59-source-spectral-pole-promotion-blocks",
        block59_source_spectral_pole_promotion_blocks,
        statuses["block59_source_spectral_pole_promotion_obstruction"],
    )
    report(
        "block60-source-carrier-support-not-closure",
        block60_source_carrier_support_not_closure,
        statuses["block60_compact_source_taste_singlet_carrier"],
    )
    report(
        "block61-post-carrier-kprime-obstruction-blocks",
        block61_post_carrier_kprime_blocks,
        statuses["block61_post_carrier_kprime_obstruction"],
    )
    report(
        "block62-compact-source-kprime-identifiability-obstruction-blocks",
        block62_compact_source_kprime_identifiability_blocks,
        statuses["block62_compact_source_kprime_identifiability_obstruction"],
    )
    report("finite-source-support-present", finite_source_support, statuses["fh_lsz_finite_source_linearity"])
    report("target-ess-support-present", ess_support, statuses["fh_lsz_target_ess"])
    report(
        "target-timeseries-full-set-support-not-closure",
        full_target_timeseries_support,
        statuses["fh_lsz_target_timeseries_full_set"],
    )
    report("polefit8x8-support-only", polefit_support_only, statuses["fh_lsz_polefit8x8_postprocessor"])
    report(
        "genuine-source-pole-artifact-support-only",
        genuine_source_pole_support_only,
        statuses["pr230_genuine_source_pole_artifact_intake"],
    )
    report(
        "completed-l12-chunk-compute-status-support-only",
        l12_chunk_compute_support_only,
        statuses["pr230_l12_chunk_compute_status"],
    )
    report(
        "negative-route-applicability-review-preserves-reopen",
        negative_route_applicability_review_passed,
        statuses["pr230_negative_route_applicability_review"],
    )
    report(
        "taste-condensate-oh-bridge-blocks-current-shortcut",
        taste_condensate_oh_bridge_blocks_shortcut,
        statuses["pr230_taste_condensate_oh_bridge_audit"],
    )
    report(
        "source-coordinate-transport-blocks-current-shortcut",
        source_coordinate_transport_blocks_current_shortcut,
        statuses["pr230_source_coordinate_transport_gate"],
    )
    report(
        "origin-main-composite-higgs-intake-not-closure",
        origin_main_composite_higgs_not_closure,
        statuses["pr230_origin_main_composite_higgs_intake_guard"],
    )
    report(
        "origin-main-ew-m-residual-intake-not-closure",
        origin_main_ew_m_residual_not_closure,
        statuses["pr230_origin_main_ew_m_residual_intake_guard"],
    )
    report(
        "z3-triplet-conditional-primitive-support-not-closure",
        z3_triplet_conditional_primitive_not_closure,
        statuses["pr230_z3_triplet_conditional_primitive_cone"],
    )
    report(
        "z3-triplet-positive-cone-h2-support-not-transfer",
        z3_triplet_positive_cone_h2_support_not_transfer,
        statuses["pr230_z3_triplet_positive_cone_support"],
    )
    report(
        "z3-generation-action-lift-not-derived",
        z3_generation_action_lift_not_derived,
        statuses["pr230_z3_generation_action_lift_attempt"],
    )
    report(
        "z3-lazy-transfer-promotion-not-derived",
        z3_lazy_transfer_promotion_not_derived,
        statuses["pr230_z3_lazy_transfer_promotion_attempt"],
    )
    report(
        "z3-lazy-selector-no-go-blocks-current-shortcut",
        z3_lazy_selector_no_go_blocks,
        statuses["pr230_z3_lazy_selector_no_go"],
    )
    report(
        "same-surface-z3-taste-triplet-support-not-closure",
        same_surface_z3_taste_triplet_support_not_closure,
        statuses["pr230_same_surface_z3_taste_triplet"],
    )
    report(
        "source-coordinate-transport-current-surface-closed",
        source_coordinate_transport_completion_blocks,
        statuses["pr230_source_coordinate_transport_completion"],
    )
    report(
        "two-source-taste-radial-chart-support-not-closure",
        two_source_taste_radial_chart_support_not_closure,
        statuses["pr230_two_source_taste_radial_chart"],
    )
    report(
        "two-source-taste-radial-action-support-not-closure",
        two_source_taste_radial_action_support_not_closure,
        statuses["pr230_two_source_taste_radial_action"],
    )
    report(
        "two-source-taste-radial-row-contract-support-not-closure",
        two_source_taste_radial_row_contract_support_not_closure,
        statuses["pr230_two_source_taste_radial_row_contract"],
    )
    report(
        "two-source-taste-radial-row-production-manifest-support-not-closure",
        two_source_taste_radial_row_manifest_support_not_closure,
        statuses["pr230_two_source_taste_radial_row_production_manifest"],
    )
    report(
        "two-source-taste-radial-schur-subblock-support-not-closure",
        two_source_taste_radial_schur_subblock_support_not_closure,
        statuses["pr230_two_source_taste_radial_schur_subblock_witness"],
    )
    report(
        "two-source-taste-radial-kprime-finite-shell-scout-not-closure",
        two_source_taste_radial_kprime_scout_not_closure,
        statuses["pr230_two_source_taste_radial_schur_kprime_finite_shell_scout"],
    )
    report(
        "two-source-taste-radial-schur-abc-finite-rows-not-closure",
        two_source_taste_radial_schur_abc_finite_rows_not_closure,
        statuses["pr230_two_source_taste_radial_schur_abc_finite_rows"],
    )
    report(
        "two-source-taste-radial-schur-pole-lift-gate-blocks-endpoint-promotion",
        two_source_taste_radial_schur_pole_lift_gate_blocks_endpoint_promotion,
        statuses["pr230_two_source_taste_radial_schur_pole_lift_gate"],
    )
    report(
        "two-source-taste-radial-primitive-transfer-candidate-not-h3",
        two_source_taste_radial_primitive_transfer_candidate_not_h3,
        statuses["pr230_two_source_taste_radial_primitive_transfer_candidate_gate"],
    )
    report(
        "orthogonal-top-coupling-exclusion-candidate-rejected",
        orthogonal_top_coupling_exclusion_candidate_rejected,
        statuses["pr230_orthogonal_top_coupling_exclusion_candidate_gate"],
    )
    report(
        "strict-scalar-lsz-moment-fv-authority-absent",
        strict_scalar_lsz_moment_fv_authority_absent,
        statuses["pr230_strict_scalar_lsz_moment_fv_authority_gate"],
    )
    report(
        "schur-complement-stieltjes-repair-support-not-closure",
        schur_complement_stieltjes_repair_support_not_closure,
        statuses["pr230_schur_complement_stieltjes_repair_gate"],
    )
    report(
        "schur-complement-complete-monotonicity-support-not-closure",
        schur_complement_complete_monotonicity_support_not_closure,
        statuses["pr230_schur_complement_complete_monotonicity_gate"],
    )
    report(
        "schur-x-given-source-one-pole-scout-not-authority",
        schur_x_given_source_one_pole_scout_not_authority,
        statuses["pr230_schur_x_given_source_one_pole_scout"],
    )
    report(
        "two-source-taste-radial-chunk-package-support-not-closure",
        two_source_taste_radial_chunk_package_support_not_closure,
        statuses["pr230_two_source_taste_radial_chunk_package"],
    )
    report(
        "source-higgs-pole-row-contract-open",
        source_higgs_pole_row_contract_open,
        statuses["pr230_source_higgs_pole_row_acceptance_contract"],
    )
    report(
        "taste-radial-canonical-oh-selector-blocks-symmetry-shortcut",
        taste_radial_canonical_oh_selector_blocks_symmetry_shortcut,
        statuses["pr230_taste_radial_canonical_oh_selector_gate"],
    )
    report(
        "degree-one-higgs-action-premise-not-derived",
        degree_one_higgs_action_premise_not_derived,
        statuses["pr230_degree_one_higgs_action_premise_gate"],
    )
    report(
        "degree-one-radial-tangent-oh-theorem-support-not-closure",
        degree_one_radial_tangent_oh_theorem_support_not_closure,
        statuses["pr230_degree_one_radial_tangent_oh_theorem"],
    )
    report(
        "taste-radial-to-source-higgs-promotion-contract-support-not-closure",
        taste_radial_to_source_higgs_promotion_contract_support_not_closure,
        statuses["pr230_taste_radial_to_source_higgs_promotion_contract"],
    )
    report(
        "fms-post-degree-route-rescore-support-not-closure",
        fms_post_degree_route_support_not_closure,
        statuses["pr230_fms_post_degree_route_rescore"],
    )
    report(
        "fms-composite-oh-conditional-support-not-closure",
        fms_composite_oh_conditional_support_not_closure,
        statuses["pr230_fms_composite_oh_conditional_theorem"],
    )
    report(
        "fms-oh-candidate-action-packet-support-not-closure",
        fms_oh_candidate_action_packet_support_not_closure,
        statuses["pr230_fms_oh_candidate_action_packet"],
    )
    report(
        "fms-source-overlap-readout-gate-support-not-closure",
        fms_source_overlap_readout_gate_support_not_closure,
        statuses["pr230_fms_source_overlap_readout_gate"],
    )
    report(
        "fms-action-adoption-minimal-cut-support-not-closure",
        fms_action_adoption_minimal_cut_support_not_closure,
        statuses["pr230_fms_action_adoption_minimal_cut"],
    )
    report(
        "higgs-mass-source-action-bridge-support-not-closure",
        higgs_mass_source_action_bridge_support_not_closure,
        statuses["pr230_higgs_mass_source_action_bridge"],
    )
    report(
        "same-source-ew-higgs-action-ansatz-support-not-closure",
        same_source_ew_higgs_action_ansatz_support_not_closure,
        statuses["pr230_same_source_ew_higgs_action_ansatz_gate"],
    )
    report(
        "same-source-ew-action-adoption-attempt-blocks-shortcut",
        same_source_ew_action_adoption_attempt_blocks_shortcut,
        statuses["pr230_same_source_ew_action_adoption_attempt"],
    )
    report(
        "radial-spurion-sector-overlap-support-not-closure",
        radial_spurion_sector_overlap_support_not_closure,
        statuses["pr230_radial_spurion_sector_overlap_theorem"],
    )
    report(
        "radial-spurion-action-contract-support-not-closure",
        radial_spurion_action_contract_support_not_closure,
        statuses["pr230_radial_spurion_action_contract"],
    )
    report(
        "additive-source-radial-spurion-incompatibility-support-not-closure",
        additive_source_radial_spurion_incompatibility_support_not_closure,
        statuses["pr230_additive_source_radial_spurion_incompatibility"],
    )
    report(
        "additive-top-subtraction-row-contract-support-not-closure",
        additive_top_subtraction_row_contract_support_not_closure,
        statuses["pr230_additive_top_subtraction_row_contract"],
    )
    report(
        "top-mass-scan-response-harness-support-not-closure",
        top_mass_scan_response_harness_support_not_closure,
        statuses["pr230_top_mass_scan_response_harness_gate"],
    )
    report(
        "top-mass-scan-subtraction-contract-applicability-blocks",
        top_mass_scan_subtraction_contract_applicability_blocks,
        statuses["pr230_top_mass_scan_subtraction_contract_applicability_audit"],
    )
    report(
        "higher-shell-source-higgs-operator-certificate-boundary-blocks",
        higher_shell_source_higgs_operator_certificate_boundary_blocks,
        statuses["pr230_higher_shell_source_higgs_operator_certificate_boundary"],
    )
    report(
        "post-chunks001-002-source-higgs-bridge-intake-blocks",
        post_chunks001_002_source_higgs_bridge_intake_blocks,
        statuses["pr230_post_chunks001_002_source_higgs_bridge_intake_guard"],
    )
    report(
        "origin-main-yt-ward-step3-open-gate-not-closure",
        origin_main_yt_ward_step3_open_gate_not_closure,
        statuses["pr230_origin_main_yt_ward_step3_open_gate_intake_guard"],
    )
    report(
        "wz-response-ratio-identifiability-contract-support-not-closure",
        wz_response_ratio_identifiability_contract_support_not_closure,
        statuses["pr230_wz_response_ratio_identifiability_contract"],
    )
    report(
        "wz-same-source-action-minimal-certificate-cut-open",
        wz_same_source_action_minimal_certificate_cut_open,
        statuses["pr230_wz_same_source_action_minimal_certificate_cut"],
    )
    report(
        "wz-accepted-action-response-root-checkpoint-blocks",
        wz_accepted_action_response_root_checkpoint_blocks,
        statuses["pr230_wz_accepted_action_response_root_checkpoint"],
    )
    report(
        "canonical-oh-wz-common-action-cut-open",
        canonical_oh_wz_common_action_cut_open,
        statuses["pr230_canonical_oh_wz_common_action_cut"],
    )
    report(
        "canonical-oh-accepted-action-stretch-blocks-current-stack",
        canonical_oh_accepted_action_stretch_blocks_current_stack,
        statuses["pr230_canonical_oh_accepted_action_stretch_attempt"],
    )
    report(
        "post-fms-source-overlap-necessity-blocks-current-inference",
        post_fms_source_overlap_necessity_blocks_current_inference,
        statuses["pr230_post_fms_source_overlap_necessity_gate"],
    )
    report(
        "source-higgs-overlap-kappa-contract-support-not-closure",
        source_higgs_overlap_kappa_contract_support_not_closure,
        statuses["pr230_source_higgs_overlap_kappa_contract"],
    )
    report(
        "kinetic-taste-mixing-shortcut-closed",
        kinetic_taste_mixing_bridge_blocks_shortcut,
        statuses["pr230_kinetic_taste_mixing_bridge"],
    )
    report(
        "one-higgs-taste-axis-completeness-shortcut-closed",
        one_higgs_taste_axis_completeness_blocks_shortcut,
        statuses["pr230_one_higgs_taste_axis_completeness"],
    )
    report(
        "action-first-route-current-surface-closed",
        action_first_route_completion_blocks,
        statuses["pr230_action_first_route_completion"],
    )
    report(
        "wz-response-route-current-surface-closed",
        wz_response_route_completion_blocks,
        statuses["pr230_wz_response_route_completion"],
    )
    report(
        "schur-route-current-surface-closed",
        schur_route_completion_blocks,
        statuses["pr230_schur_route_completion"],
    )
    report(
        "neutral-primitive-route-current-surface-closed",
        neutral_primitive_route_completion_blocks,
        statuses["pr230_neutral_primitive_route_completion"],
    )
    report(
        "oh-bridge-first-principles-candidate-portfolio-open",
        oh_bridge_candidate_portfolio_open,
        statuses["pr230_oh_bridge_candidate_portfolio"],
    )
    report(
        "same-surface-neutral-multiplicity-one-gate-rejects-current-surface",
        same_surface_neutral_multiplicity_gate_rejects_current_surface,
        statuses["pr230_same_surface_neutral_multiplicity_one_gate"],
    )
    report(
        "os-transfer-kernel-artifact-absent",
        os_transfer_kernel_artifact_absent,
        statuses["pr230_os_transfer_kernel_artifact_gate"],
    )
    report(
        "source-higgs-time-kernel-harness-support-only",
        source_higgs_time_kernel_harness_support_only,
        statuses["pr230_source_higgs_time_kernel_harness_extension_gate"],
    )
    report(
        "source-higgs-time-kernel-gevp-contract-support-only",
        source_higgs_time_kernel_gevp_contract_support_only,
        statuses["pr230_source_higgs_time_kernel_gevp_contract"],
    )
    report(
        "source-higgs-time-kernel-production-manifest-not-evidence",
        source_higgs_time_kernel_production_manifest_not_evidence,
        statuses["pr230_source_higgs_time_kernel_production_manifest"],
    )
    report(
        "fms-literature-source-overlap-intake-non-authority",
        fms_literature_source_overlap_intake_non_authority,
        statuses["pr230_fms_literature_source_overlap_intake"],
    )
    report(
        "schur-higher-shell-production-contract-not-evidence",
        schur_higher_shell_production_contract_not_evidence,
        statuses["pr230_schur_higher_shell_production_contract"],
    )
    report(
        "canonical-higgs-semantic-firewall-support-only",
        "semantic firewall passed" in statuses["canonical_higgs_semantic_firewall"]
        and certs["canonical_higgs_semantic_firewall"].get("proposal_allowed") is False,
        statuses["canonical_higgs_semantic_firewall"],
    )
    report(
        "action-first-oh-artifact-attempt-blocks-current-surface",
        "action-first O_H artifact not constructible"
        in statuses["pr230_action_first_oh_artifact_attempt"]
        and certs["pr230_action_first_oh_artifact_attempt"].get("proposal_allowed") is False
        and certs["pr230_action_first_oh_artifact_attempt"].get(
            "exact_negative_boundary_passed"
        )
        is True,
        statuses["pr230_action_first_oh_artifact_attempt"],
    )
    report(
        "holonomic-source-response-gate-blocks-missing-oh-h-source",
        "PR541-style holonomic source-response route"
        in statuses["pr230_holonomic_source_response_feasibility_gate"]
        and certs["pr230_holonomic_source_response_feasibility_gate"].get(
            "proposal_allowed"
        )
        is False
        and certs["pr230_holonomic_source_response_feasibility_gate"].get(
            "two_source_functional_current_surface_defined"
        )
        is False,
        statuses["pr230_holonomic_source_response_feasibility_gate"],
    )
    report(
        "oh-source-higgs-authority-rescan-finds-no-current-certificate",
        "O_H/source-Higgs authority rescan found no"
        in statuses["pr230_oh_source_higgs_authority_rescan_gate"]
        and certs["pr230_oh_source_higgs_authority_rescan_gate"].get(
            "proposal_allowed"
        )
        is False
        and certs["pr230_oh_source_higgs_authority_rescan_gate"].get(
            "oh_source_higgs_authority_found"
        )
        is False
        and certs["pr230_oh_source_higgs_authority_rescan_gate"].get(
            "exact_negative_boundary_passed"
        )
        is True,
        statuses["pr230_oh_source_higgs_authority_rescan_gate"],
    )
    report(
        "minimal-axioms-yukawa-summary-not-proof-authority",
        "minimal-axioms Yukawa summary is not PR230 proof authority"
        in statuses["pr230_minimal_axioms_yukawa_summary_firewall"]
        and certs["pr230_minimal_axioms_yukawa_summary_firewall"].get(
            "proposal_allowed"
        )
        is False
        and certs["pr230_minimal_axioms_yukawa_summary_firewall"].get(
            "exact_negative_boundary_passed"
        )
        is True
        and certs["pr230_minimal_axioms_yukawa_summary_firewall"].get(
            "yt_ward_audit_status", {}
        ).get("effective_status")
        == "audited_renaming",
        statuses["pr230_minimal_axioms_yukawa_summary_firewall"],
    )
    report(
        "derived-bridge-rank-one-attempt-blocks-current-source-only-closure",
        "derived rank-one bridge not closed"
        in statuses["pr230_derived_bridge_rank_one_closure_attempt"]
        and certs["pr230_derived_bridge_rank_one_closure_attempt"].get(
            "proposal_allowed"
        )
        is False
        and certs["pr230_derived_bridge_rank_one_closure_attempt"].get(
            "derived_bridge_closure_passed"
        )
        is False
        and certs["pr230_derived_bridge_rank_one_closure_attempt"].get(
            "exact_negative_boundary_passed"
        )
        is True,
        statuses["pr230_derived_bridge_rank_one_closure_attempt"],
    )
    report(
        "neutral-rank-one-bypass-post-block37-blocks-current-surface",
        neutral_rank_one_bypass_post_block37_blocks,
        statuses["pr230_neutral_rank_one_bypass_post_block37_audit"],
    )
    report(
        "source-sector-pattern-transfer-relevant-not-closure",
        "source-sector pattern is relevant"
        in statuses["pr230_source_sector_pattern_transfer_gate"]
        and certs["pr230_source_sector_pattern_transfer_gate"].get(
            "proposal_allowed"
        )
        is False
        and certs["pr230_source_sector_pattern_transfer_gate"].get(
            "bounded_support_passed"
        )
        is True
        and certs["pr230_source_sector_pattern_transfer_gate"].get(
            "direct_closure_available"
        )
        is False,
        statuses["pr230_source_sector_pattern_transfer_gate"],
    )
    report(
        "det-positivity-bridge-intake-relevant-not-closure",
        "determinant positivity is useful"
        in statuses["pr230_det_positivity_bridge_intake_gate"]
        and certs["pr230_det_positivity_bridge_intake_gate"].get(
            "proposal_allowed"
        )
        is False
        and certs["pr230_det_positivity_bridge_intake_gate"].get(
            "intake_gate_passed"
        )
        is True
        and certs["pr230_det_positivity_bridge_intake_gate"].get(
            "determinant_bridge_closes_pr230"
        )
        is False,
        statuses["pr230_det_positivity_bridge_intake_gate"],
    )
    report(
        "reflection-det-primitive-upgrade-blocks-combined-positivity-shortcut",
        "reflection plus determinant positivity"
        in statuses["pr230_reflection_det_primitive_upgrade_gate"]
        and certs["pr230_reflection_det_primitive_upgrade_gate"].get(
            "proposal_allowed"
        )
        is False
        and certs["pr230_reflection_det_primitive_upgrade_gate"].get(
            "primitive_upgrade_passed"
        )
        is False
        and certs["pr230_reflection_det_primitive_upgrade_gate"].get(
            "exact_negative_boundary_passed"
        )
        is True,
        statuses["pr230_reflection_det_primitive_upgrade_gate"],
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
        "complete-bernstein-inverse-diagnostic-blocks-current-denominator",
        "complete-Bernstein monotonicity"
        in statuses["fh_lsz_complete_bernstein_inverse_diagnostic"]
        and certs["fh_lsz_complete_bernstein_inverse_diagnostic"].get(
            "proposal_allowed"
        )
        is False
        and certs["fh_lsz_complete_bernstein_inverse_diagnostic"].get(
            "complete_bernstein_inverse_certificate_passed"
        )
        is False,
        statuses["fh_lsz_complete_bernstein_inverse_diagnostic"],
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
    wz_mass_response_self_normalization_no_go_blocks = (
        "WZ top-W-Z mass-plus-response self-normalization"
        in statuses["pr230_wz_mass_response_self_normalization_no_go"]
        and certs["pr230_wz_mass_response_self_normalization_no_go"].get(
            "proposal_allowed"
        )
        is False
        and certs["pr230_wz_mass_response_self_normalization_no_go"].get(
            "wz_mass_response_self_normalization_no_go_passed"
        )
        is True
    )
    report(
        "pr230-wz-mass-response-self-normalization-no-go-blocks",
        wz_mass_response_self_normalization_no_go_blocks,
        statuses["pr230_wz_mass_response_self_normalization_no_go"],
    )
    hs_logdet_scalar_action_normalization_no_go_blocks = (
        "HS-logdet auxiliary scalar action normalization"
        in statuses["pr230_hs_logdet_scalar_action_normalization_no_go"]
        and certs["pr230_hs_logdet_scalar_action_normalization_no_go"].get(
            "proposal_allowed"
        )
        is False
        and certs["pr230_hs_logdet_scalar_action_normalization_no_go"].get(
            "hs_logdet_scalar_action_normalization_no_go_passed"
        )
        is True
    )
    report(
        "pr230-hs-logdet-scalar-action-normalization-no-go-blocks",
        hs_logdet_scalar_action_normalization_no_go_blocks,
        statuses["pr230_hs_logdet_scalar_action_normalization_no_go"],
    )
    native_scalar_action_lsz_route_exhaustion_blocks = (
        "native scalar/action/LSZ current-surface route exhausted"
        in statuses["pr230_native_scalar_action_lsz_route_exhaustion_after_block40"]
        and certs[
            "pr230_native_scalar_action_lsz_route_exhaustion_after_block40"
        ].get("proposal_allowed")
        is False
        and certs[
            "pr230_native_scalar_action_lsz_route_exhaustion_after_block40"
        ].get("native_scalar_action_lsz_route_exhaustion_passed")
        is True
    )
    report(
        "pr230-native-scalar-action-lsz-route-exhaustion-blocks",
        native_scalar_action_lsz_route_exhaustion_blocks,
        statuses["pr230_native_scalar_action_lsz_route_exhaustion_after_block40"],
    )
    wz_absolute_authority_route_exhaustion_blocks = (
        "W/Z absolute-authority current-surface route exhausted"
        in statuses["pr230_wz_absolute_authority_route_exhaustion_after_block41"]
        and certs[
            "pr230_wz_absolute_authority_route_exhaustion_after_block41"
        ].get("proposal_allowed")
        is False
        and certs[
            "pr230_wz_absolute_authority_route_exhaustion_after_block41"
        ].get("wz_absolute_authority_route_exhaustion_passed")
        is True
    )
    report(
        "pr230-wz-absolute-authority-route-exhaustion-blocks",
        wz_absolute_authority_route_exhaustion_blocks,
        statuses["pr230_wz_absolute_authority_route_exhaustion_after_block41"],
    )
    full_timeseries_neutral_transfer_lift_no_go_blocks = (
        "full FH-LSZ target-timeseries packet does not lift PR230"
        in statuses["pr230_full_timeseries_neutral_transfer_lift_no_go_after_block42"]
        and certs[
            "pr230_full_timeseries_neutral_transfer_lift_no_go_after_block42"
        ].get("proposal_allowed")
        is False
        and certs[
            "pr230_full_timeseries_neutral_transfer_lift_no_go_after_block42"
        ].get("full_timeseries_neutral_transfer_lift_no_go_passed")
        is True
    )
    report(
        "pr230-full-timeseries-neutral-transfer-lift-no-go-blocks",
        full_timeseries_neutral_transfer_lift_no_go_blocks,
        statuses["pr230_full_timeseries_neutral_transfer_lift_no_go_after_block42"],
    )
    mc_timeseries_krylov_transfer_no_go_blocks = (
        "MC target time series are not"
        in statuses["pr230_mc_timeseries_krylov_transfer_no_go_after_block43"]
        and certs[
            "pr230_mc_timeseries_krylov_transfer_no_go_after_block43"
        ].get("proposal_allowed")
        is False
        and certs[
            "pr230_mc_timeseries_krylov_transfer_no_go_after_block43"
        ].get("mc_timeseries_krylov_transfer_no_go_passed")
        is True
    )
    report(
        "pr230-mc-timeseries-krylov-transfer-no-go-blocks",
        mc_timeseries_krylov_transfer_no_go_blocks,
        statuses["pr230_mc_timeseries_krylov_transfer_no_go_after_block43"],
    )
    physical_euclidean_source_higgs_row_absence_blocks = (
        "tau-keyed production correlators are not"
        in statuses["pr230_physical_euclidean_source_higgs_row_absence_after_block44"]
        and certs[
            "pr230_physical_euclidean_source_higgs_row_absence_after_block44"
        ].get("proposal_allowed")
        is False
        and certs[
            "pr230_physical_euclidean_source_higgs_row_absence_after_block44"
        ].get("physical_euclidean_source_higgs_row_absence_passed")
        is True
    )
    report(
        "pr230-physical-euclidean-source-higgs-row-absence-blocks",
        physical_euclidean_source_higgs_row_absence_blocks,
        statuses["pr230_physical_euclidean_source_higgs_row_absence_after_block44"],
    )
    neutral_offdiagonal_post_block45_applicability_blocks = (
        "post-Block45 artifacts do not reopen"
        in statuses["pr230_neutral_offdiagonal_post_block45_applicability_audit"]
        and certs[
            "pr230_neutral_offdiagonal_post_block45_applicability_audit"
        ].get("proposal_allowed")
        is False
        and certs[
            "pr230_neutral_offdiagonal_post_block45_applicability_audit"
        ].get("post_block45_neutral_offdiagonal_applicability_audit_passed")
        is True
    )
    report(
        "pr230-neutral-offdiagonal-post-block45-applicability-blocks",
        neutral_offdiagonal_post_block45_applicability_blocks,
        statuses["pr230_neutral_offdiagonal_post_block45_applicability_audit"],
    )
    report(
        "wz-g2-bare-running-bridge-attempt-blocks",
        "WZ g2 bare-to-low-scale running bridge"
        in statuses["wz_g2_bare_running_bridge_attempt"]
        and certs["wz_g2_bare_running_bridge_attempt"].get("proposal_allowed") is False
        and certs["wz_g2_bare_running_bridge_attempt"].get(
            "wz_g2_bare_running_bridge_passed"
        )
        is False
        and certs["wz_g2_bare_running_bridge_attempt"].get(
            "strict_electroweak_g2_certificate_written"
        )
        is False
        and certs["wz_g2_bare_running_bridge_attempt"].get("exact_negative_boundary_passed")
        is True,
        statuses["wz_g2_bare_running_bridge_attempt"],
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
        "schur-abc-definition-derivation-blocks-current-surface",
        "Schur A/B/C definition not derivable"
        in statuses["schur_abc_definition_derivation"]
        and certs["schur_abc_definition_derivation"].get("proposal_allowed") is False
        and certs["schur_abc_definition_derivation"].get(
            "schur_abc_definition_derivation_passed"
        )
        is False
        and certs["schur_abc_definition_derivation"].get("schur_abc_rows_written")
        is False
        and certs["schur_abc_definition_derivation"].get("exact_negative_boundary_passed")
        is True,
        statuses["schur_abc_definition_derivation"],
    )
    report(
        "schur-route-completion-blocks-current-surface",
        schur_route_completion_blocks,
        statuses["pr230_schur_route_completion"],
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
        "neutral-offdiagonal-generator-derivation-attempt-blocks-current-surface",
        "neutral off-diagonal generator not derivable"
        in statuses["neutral_offdiagonal_generator_derivation"]
        and certs["neutral_offdiagonal_generator_derivation"].get("proposal_allowed")
        is False
        and certs["neutral_offdiagonal_generator_derivation"].get(
            "offdiagonal_generator_certificate_passed"
        )
        is False
        and certs["neutral_offdiagonal_generator_derivation"].get(
            "exact_negative_boundary_passed"
        )
        is True,
        statuses["neutral_offdiagonal_generator_derivation"],
    )
    report(
        "neutral-primitive-route-completion-blocks-current-surface",
        neutral_primitive_route_completion_blocks,
        statuses["pr230_neutral_primitive_route_completion"],
    )
    report(
        "logdet-hessian-neutral-mixing-attempt-blocks-source-only-determinant-route",
        "source-only staggered logdet Hessian does not derive"
        in statuses["pr230_logdet_hessian_neutral_mixing_attempt"]
        and certs["pr230_logdet_hessian_neutral_mixing_attempt"].get(
            "proposal_allowed"
        )
        is False
        and certs["pr230_logdet_hessian_neutral_mixing_attempt"].get(
            "exact_negative_boundary_passed"
        )
        is True
        and certs["pr230_logdet_hessian_neutral_mixing_attempt"].get(
            "logdet_hessian_bridge_closes_pr230"
        )
        is False,
        statuses["pr230_logdet_hessian_neutral_mixing_attempt"],
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
    report(
        "negative-route-applicability-review-preserves-reopen",
        negative_route_review_passed,
        statuses["negative_route_applicability_review"],
    )
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
            " The taste-condensate/Higgs stack has also been checked directly: "
            "on the current PR230 surface the uniform FH/LSZ mass source is "
            "orthogonal to the trace-zero taste-axis Higgs operators, so that "
            "stack is not an O_H bridge without a new source-coordinate "
            "transport theorem or production C_sH/C_HH rows."
            " The origin/main composite-Higgs stretch packet has also been "
            "intaken: it is a conditional cross-lane candidate with named "
            "Z3/equal-condensate/strong-coupling residuals, not a PR230 "
            "uniform-source transport certificate, canonical O_H authority, "
            "or C_sH/C_HH row set."
            " The Z3-triplet primitive-cone theorem adds exact conditional "
            "support for a lazy cyclic neutral transfer, but it does not supply "
            "the missing same-surface PR230 action/off-diagonal generator or "
            "strict primitive certificate."
            " The Z3-triplet positive-cone H2 support certificate now supplies "
            "the equal-magnitude PSD cone row for the taste triplet exactly, "
            "but it is algebraic support only and does not instantiate a "
            "physical neutral transfer or source/Higgs coupling."
            " The H1 generation-action lift attempt shows that Koide/lepton Z3 "
            "does not yet select cyclic quark-bilinear action over the trivial "
            "action on the PR230 surface."
            " The same-surface Z3 taste-triplet artifact now supplies the "
            "cyclic triplet action on the PR230 taste axes exactly; it still "
            "does not supply the physical lazy transfer or source/Higgs row."
            " A separate kinetic taste-mixing check now closes the adjacent "
            "shortcut: taste-even Wilson-staggered dynamics also gives zero "
            "C_sH against one trace-zero taste-axis insertion unless a real "
            "symmetry-breaking EW/Higgs source or measured source-Higgs row is "
            "supplied."
            " The one-Higgs taste-axis completeness check also blocks using "
            "SM one-Higgs notation plus the taste scalar theorem as an "
            "orthogonal-null proof: the taste axes remain in one permutation "
            "orbit until a same-source axis/completeness certificate is "
            "supplied."
            " The first-principles O_H bridge candidate portfolio now ranks "
            "the surviving source-transport, action-first O_H, W/Z response, "
            "Schur-row, and neutral-primitive routes as open positive "
            "candidates; it is not closure authority."
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
        "negative_route_applicability_review_passed": negative_route_review_passed,
        "taste_condensate_oh_bridge_blocks_shortcut": taste_condensate_oh_bridge_blocks_shortcut,
        "source_coordinate_transport_blocks_current_shortcut": source_coordinate_transport_blocks_current_shortcut,
        "origin_main_composite_higgs_not_closure": origin_main_composite_higgs_not_closure,
        "origin_main_ew_m_residual_not_closure": origin_main_ew_m_residual_not_closure,
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
        "same_source_ew_higgs_action_ansatz_support_not_closure": same_source_ew_higgs_action_ansatz_support_not_closure,
        "same_source_ew_action_adoption_attempt_blocks_shortcut": same_source_ew_action_adoption_attempt_blocks_shortcut,
        "radial_spurion_sector_overlap_support_not_closure": radial_spurion_sector_overlap_support_not_closure,
        "radial_spurion_action_contract_support_not_closure": radial_spurion_action_contract_support_not_closure,
        "additive_source_radial_spurion_incompatibility_support_not_closure": additive_source_radial_spurion_incompatibility_support_not_closure,
        "additive_top_subtraction_row_contract_support_not_closure": additive_top_subtraction_row_contract_support_not_closure,
        "top_mass_scan_response_harness_support_not_closure": top_mass_scan_response_harness_support_not_closure,
        "top_mass_scan_subtraction_contract_applicability_blocks": top_mass_scan_subtraction_contract_applicability_blocks,
        "higher_shell_source_higgs_operator_certificate_boundary_blocks": higher_shell_source_higgs_operator_certificate_boundary_blocks,
        "post_chunks001_002_source_higgs_bridge_intake_blocks": post_chunks001_002_source_higgs_bridge_intake_blocks,
        "origin_main_yt_ward_step3_open_gate_not_closure": origin_main_yt_ward_step3_open_gate_not_closure,
        "wz_response_ratio_identifiability_contract_support_not_closure": wz_response_ratio_identifiability_contract_support_not_closure,
        "wz_same_source_action_minimal_certificate_cut_open": wz_same_source_action_minimal_certificate_cut_open,
        "wz_accepted_action_response_root_checkpoint_blocks": wz_accepted_action_response_root_checkpoint_blocks,
        "canonical_oh_wz_common_action_cut_open": canonical_oh_wz_common_action_cut_open,
        "canonical_oh_accepted_action_stretch_blocks_current_stack": canonical_oh_accepted_action_stretch_blocks_current_stack,
        "post_fms_source_overlap_necessity_blocks_current_inference": post_fms_source_overlap_necessity_blocks_current_inference,
        "source_higgs_overlap_kappa_contract_support_not_closure": source_higgs_overlap_kappa_contract_support_not_closure,
        "kinetic_taste_mixing_bridge_blocks_shortcut": kinetic_taste_mixing_bridge_blocks_shortcut,
        "one_higgs_taste_axis_completeness_blocks_shortcut": one_higgs_taste_axis_completeness_blocks_shortcut,
        "action_first_route_completion_blocks": action_first_route_completion_blocks,
        "wz_response_route_completion_blocks": wz_response_route_completion_blocks,
        "schur_route_completion_blocks": schur_route_completion_blocks,
        "neutral_primitive_route_completion_blocks": neutral_primitive_route_completion_blocks,
        "neutral_rank_one_bypass_post_block37_blocks": neutral_rank_one_bypass_post_block37_blocks,
        "wz_mass_response_self_normalization_no_go_blocks": wz_mass_response_self_normalization_no_go_blocks,
        "hs_logdet_scalar_action_normalization_no_go_blocks": hs_logdet_scalar_action_normalization_no_go_blocks,
        "native_scalar_action_lsz_route_exhaustion_blocks": native_scalar_action_lsz_route_exhaustion_blocks,
        "wz_absolute_authority_route_exhaustion_blocks": wz_absolute_authority_route_exhaustion_blocks,
        "full_timeseries_neutral_transfer_lift_no_go_blocks": full_timeseries_neutral_transfer_lift_no_go_blocks,
        "mc_timeseries_krylov_transfer_no_go_blocks": mc_timeseries_krylov_transfer_no_go_blocks,
        "physical_euclidean_source_higgs_row_absence_blocks": physical_euclidean_source_higgs_row_absence_blocks,
        "neutral_offdiagonal_post_block45_applicability_blocks": neutral_offdiagonal_post_block45_applicability_blocks,
        "oh_bridge_candidate_portfolio_open": oh_bridge_candidate_portfolio_open,
        "same_surface_neutral_multiplicity_one_gate_rejects_current_surface": same_surface_neutral_multiplicity_gate_rejects_current_surface,
        "os_transfer_kernel_artifact_absent": os_transfer_kernel_artifact_absent,
        "source_higgs_time_kernel_harness_support_only": source_higgs_time_kernel_harness_support_only,
        "source_higgs_time_kernel_gevp_contract_support_only": source_higgs_time_kernel_gevp_contract_support_only,
        "source_higgs_time_kernel_production_manifest_not_evidence": source_higgs_time_kernel_production_manifest_not_evidence,
        "fms_literature_source_overlap_intake_non_authority": fms_literature_source_overlap_intake_non_authority,
        "schur_higher_shell_production_contract_not_evidence": schur_higher_shell_production_contract_not_evidence,
        "block53_residual_minimality_not_closure": block53_residual_minimality_not_closure,
        "block54_response_readout_reduction_not_closure": block54_response_readout_reduction_not_closure,
        "block55_canonical_neutral_cut_not_closure": block55_canonical_neutral_cut_not_closure,
        "block56_scalar_fvir_cut_not_closure": block56_scalar_fvir_cut_not_closure,
        "block57_compact_foundation_support_not_closure": block57_compact_foundation_support_not_closure,
        "block58_compact_spectral_support_not_closure": block58_compact_spectral_support_not_closure,
        "block59_source_spectral_pole_promotion_blocks": block59_source_spectral_pole_promotion_blocks,
        "block60_source_carrier_support_not_closure": block60_source_carrier_support_not_closure,
        "block61_post_carrier_kprime_blocks": block61_post_carrier_kprime_blocks,
        "block62_compact_source_kprime_identifiability_blocks": block62_compact_source_kprime_identifiability_blocks,
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
            "does not treat a formal HS/logdet auxiliary scalar rewrite as canonical O_H or scalar LSZ authority",
            "does not treat current native scalar/action/LSZ route exhaustion as a permanent no-go against future primitives",
            "does not treat current W/Z absolute-authority route exhaustion as permanent no-go or as closure",
            "does not treat complete FH-LSZ target time series as same-surface neutral transfer or C_sH/C_HH pole rows",
            "does not treat MC configuration-index target time series as Euclidean transfer, OS kernel, Krylov generator, or source-Higgs pole evidence",
            "does not treat ordinary top/scalar-source tau correlators or reduced source-Higgs smoke as strict C_sH/C_HH production pole evidence",
            "does not treat finite C_sx covariance, active worker intent, or post-Block45 support as a neutral off-diagonal generator",
            "does not treat W/Z smoke-schema rows as production EW response evidence",
            "does not treat current-surface non-chunk exhaustion as retained closure",
            "does not treat the Higgs/taste condensate stack as PR230 O_H authority",
            "does not treat conditional Z3-triplet primitive support as a strict PR230 primitive certificate",
            "does not treat Z3 H2 positive-cone support as physical neutral transfer, primitive irreducibility, or source-Higgs coupling authority",
            "does not treat Koide/lepton Z3 as a quark-bilinear generation-action certificate",
            "does not treat the two-source taste-radial chart as canonical O_H or production source-Higgs rows",
            "does not treat the two-source taste-radial row production manifest as C_sx/C_xx row data or pole evidence",
            "does not treat degree-one taste-radial uniqueness as canonical O_H without a same-surface degree-one Higgs-action premise",
            "does not treat the radial-spurion sector-overlap theorem as current additive-source sector-overlap closure",
            "does not treat the current additive top source as a no-independent-top radial spurion",
            "does not treat the additive-top subtraction formula as closure before additive Jacobian rows, W/Z rows, matched covariance, strict g2, and accepted action exist",
            "does not treat top mass-scan dE/dm_bare rows as dE/dh, W/Z response, kappa_s, or y_t closure",
            "does not treat top mass-scan dE/dm_bare rows as satisfying the additive-top subtraction contract",
            "does not treat higher-shell source-Higgs cross rows emitted under the taste-radial second-source certificate as strict C_sH/C_HH source-Higgs rows",
            "does not treat the W/Z same-source minimal certificate cut as accepted action authority or response rows",
            "does not treat current Schur sufficiency or row-definition machinery as proof without a neutral kernel basis plus same-surface A/B/C rows",
            "does not treat conditional Perron support, determinant positivity, or source-only generators as a primitive neutral rank-one theorem",
            "does not treat terminal non-chunk route exhaustion as positive closure",
            "does not treat the same-surface neutral multiplicity-one intake gate as accepted O_H authority",
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
            "does not treat packaged C_sx/C_xx chunks as canonical C_sH/C_HH pole rows",
            "does not treat a source-Higgs pole-row acceptance contract as evidence that such rows exist",
            "does not treat the Block53 residual-minimality checkpoint as positive closure",
            "does not treat the Block54 response-readout reduction as scalar/FVIR authority, canonical-Higgs identity, or positive closure",
            "does not treat the Block55 canonical-neutral primitive cut as canonical O_H, neutral transfer, or positive closure",
            "does not treat the Block56 scalar/FVIR root cut as scalar-pole authority or positive closure",
            "does not treat the Block57 compact source-functional foundation as an isolated-pole, FVIR, or canonical-O_H theorem",
            "does not treat the Block58 finite-volume source-channel spectral sum as thermodynamic pole saturation, LSZ residue authority, or canonical O_H",
            "does not treat finite-volume source spectral positivity as thermodynamic isolated-pole authority after Block59",
            "does not treat the Block60 source-channel taste-singlet carrier as canonical O_H or scalar LSZ residue authority",
            "does not treat the Block60 source-channel carrier as K-prime or pole-residue authority after Block61",
            "does not treat compact source support plus fixed source carrier as K-prime or pole-residue authority after Block62",
        ],
        "exact_next_action": (
            "Keep the chunk worker on homogeneous production chunks and launch "
            "the taste-radial C_sx/C_xx row chunks only under the no-resume "
            "manifest/collision guard.  In parallel, "
            "pursue one non-chunk bridge that can satisfy this gate: a real "
            "same-surface neutral multiplicity-one certificate accepted by "
            "outputs/yt_pr230_same_surface_neutral_multiplicity_one_gate_2026-05-07.json, "
            "or physical primitive-transfer authority accepted by "
            "outputs/yt_pr230_two_source_taste_radial_primitive_transfer_candidate_gate_2026-05-07.json, "
            "then a same-surface O_H certificate plus C_sH/C_HH pole rows, a same-source "
            "EW action plus top/W/Z mass-response rows, matched covariance or "
            "a real top/W factorization theorem, and sector-overlap identity, "
            "with source identity supplied by real rows or a certificate rather "
            "than Goldstone bookkeeping, a strict Stieltjes moment certificate "
            "or a thermodynamic transfer/spectral theorem built from the exact "
            "compact finite-volume source functional, yielding scalar denominator "
            "closure, "
            "or a neutral-sector irreducibility theorem.  After Block58, the "
            "most direct non-chunk target is now stricter: a new microscopic "
            "scalar denominator/contact theorem or strict physical rows that "
            "supply uniform thermodynamic/FVIR pole, threshold, residue, and "
            "canonical-O_H/response authority.  Rerun this assembly "
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
