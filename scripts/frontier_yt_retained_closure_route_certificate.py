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
        "fh_lsz_stieltjes_model_class": "outputs/yt_fh_lsz_stieltjes_model_class_obstruction_2026-05-02.json",
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
        "complete_source_spectrum_identity_no_go": "outputs/yt_complete_source_spectrum_identity_no_go_2026-05-02.json",
        "neutral_scalar_top_coupling_tomography_gate": "outputs/yt_neutral_scalar_top_coupling_tomography_gate_2026-05-02.json",
        "non_source_response_rank_repair_sufficiency": "outputs/yt_non_source_response_rank_repair_sufficiency_2026-05-03.json",
        "positivity_improving_neutral_scalar_rank_one": "outputs/yt_positivity_improving_neutral_scalar_rank_one_support_2026-05-03.json",
        "gauge_perron_neutral_scalar_rank_one_import": "outputs/yt_gauge_perron_to_neutral_scalar_rank_one_import_audit_2026-05-03.json",
        "neutral_scalar_positivity_improving_direct_closure": "outputs/yt_neutral_scalar_positivity_improving_direct_closure_attempt_2026-05-03.json",
        "scalar_carrier_projector_closure": "outputs/yt_scalar_carrier_projector_closure_attempt_2026-05-02.json",
        "kprime_closure": "outputs/yt_kprime_closure_attempt_2026-05-02.json",
        "schur_complement_kprime_sufficiency": "outputs/yt_schur_complement_kprime_sufficiency_2026-05-03.json",
        "schur_kprime_row_absence_guard": "outputs/yt_schur_kprime_row_absence_guard_2026-05-03.json",
        "fh_lsz_higgs_pole_identity": "outputs/yt_fh_lsz_higgs_pole_identity_gate_2026-05-02.json",
        "fh_gauge_normalized_response": "outputs/yt_fh_gauge_normalized_response_route_2026-05-02.json",
        "fh_gauge_mass_response_observable_gap": "outputs/yt_fh_gauge_mass_response_observable_gap_2026-05-02.json",
        "fh_gauge_mass_response_manifest": "outputs/yt_fh_gauge_mass_response_manifest_2026-05-02.json",
        "fh_gauge_mass_response_certificate_builder": "outputs/yt_fh_gauge_mass_response_certificate_builder_2026-05-03.json",
        "same_source_wz_response_certificate_gate": "outputs/yt_same_source_wz_response_certificate_gate_2026-05-02.json",
        "wz_response_harness_absence_guard": "outputs/yt_wz_response_harness_absence_guard_2026-05-02.json",
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
        "canonical_higgs_operator_candidate_stress": "outputs/yt_canonical_higgs_operator_candidate_stress_2026-05-03.json",
        "canonical_higgs_operator_realization_gate": "outputs/yt_canonical_higgs_operator_realization_gate_2026-05-02.json",
        "hunit_canonical_higgs_operator_candidate_gate": "outputs/yt_hunit_canonical_higgs_operator_candidate_gate_2026-05-02.json",
        "source_higgs_harness_absence_guard": "outputs/yt_source_higgs_harness_absence_guard_2026-05-02.json",
        "source_higgs_unratified_operator_smoke": "outputs/yt_source_higgs_unratified_operator_smoke_checkpoint_2026-05-03.json",
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
        "fh_lsz_target_observable_ess": "outputs/yt_fh_lsz_target_observable_ess_certificate_2026-05-03.json",
        "fh_lsz_autocorrelation_ess_gate": "outputs/yt_fh_lsz_autocorrelation_ess_gate_2026-05-02.json",
        "fh_lsz_response_window_forensics": "outputs/yt_fh_lsz_response_window_forensics_2026-05-03.json",
        "fh_lsz_response_window_acceptance_gate": "outputs/yt_fh_lsz_response_window_acceptance_gate_2026-05-03.json",
        "fh_lsz_target_timeseries_replacement_queue": "outputs/yt_fh_lsz_target_timeseries_replacement_queue_2026-05-02.json",
        "fh_lsz_target_timeseries_harness": "outputs/yt_fh_lsz_target_timeseries_harness_certificate_2026-05-02.json",
        "fh_lsz_multitau_target_timeseries_harness": "outputs/yt_fh_lsz_multitau_target_timeseries_harness_certificate_2026-05-03.json",
        "fh_lsz_selected_mass_normal_cache_speedup": "outputs/yt_fh_lsz_selected_mass_normal_cache_speedup_certificate_2026-05-03.json",
        "fh_lsz_target_timeseries_higgs_identity_no_go": "outputs/yt_fh_lsz_target_timeseries_higgs_identity_no_go_2026-05-02.json",
        "higgs_pole_identity_latest_blocker": "outputs/yt_higgs_pole_identity_latest_blocker_certificate_2026-05-02.json",
        "fh_lsz_pole_fit_mode_budget": "outputs/yt_fh_lsz_pole_fit_mode_budget_2026-05-01.json",
        "fh_lsz_eight_mode_noise_variance": "outputs/yt_fh_lsz_eight_mode_noise_variance_gate_2026-05-01.json",
        "fh_lsz_noise_subsample_diagnostics": "outputs/yt_fh_lsz_noise_subsample_diagnostics_certificate_2026-05-01.json",
        "fh_lsz_variance_calibration_manifest": "outputs/yt_fh_lsz_variance_calibration_manifest_2026-05-01.json",
        "joint_resource_projection": "outputs/yt_fh_lsz_joint_resource_projection_2026-05-01.json",
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
    production_postprocess_gate_not_ready = (
        "postprocess gate" in certificates["fh_lsz_production_postprocess_gate"].get("actual_current_surface_status", "")
        and certificates["fh_lsz_production_postprocess_gate"].get("proposal_allowed") is False
        and certificates["fh_lsz_production_postprocess_gate"].get("retained_proposal_gate_ready") is False
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
    chunk_combiner_not_evidence = (
        "chunk combiner gate"
        in certificates["fh_lsz_chunk_combiner_gate"].get("actual_current_surface_status", "")
        and certificates["fh_lsz_chunk_combiner_gate"].get("proposal_allowed") is False
        and int(certificates["fh_lsz_chunk_combiner_gate"].get("chunk_summary", {}).get("ready_chunks", 0))
        < int(certificates["fh_lsz_chunk_combiner_gate"].get("chunk_summary", {}).get("expected_chunks", 1))
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
    ready_chunk_set_not_closure = (
        "ready chunk-set production checkpoint"
        in certificates["fh_lsz_ready_chunk_set_checkpoint"].get("actual_current_surface_status", "")
        and certificates["fh_lsz_ready_chunk_set_checkpoint"].get("proposal_allowed") is False
        and int(certificates["fh_lsz_ready_chunk_set_checkpoint"].get("chunk_summary", {}).get("ready_chunks", 0))
        < int(
            certificates["fh_lsz_ready_chunk_set_checkpoint"].get("chunk_summary", {}).get(
                "expected_chunks", 1
            )
        )
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
    canonical_higgs_operator_realization_gate_blocks = (
        "canonical-Higgs operator realization gate not passed"
        in certificates["canonical_higgs_operator_realization_gate"].get("actual_current_surface_status", "")
        and certificates["canonical_higgs_operator_realization_gate"].get("proposal_allowed") is False
        and certificates["canonical_higgs_operator_realization_gate"].get(
            "canonical_higgs_operator_realization_gate_passed"
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
    finite_source_linearity_gate_blocks = (
        "finite-source-linearity gate not passed"
        in certificates["fh_lsz_finite_source_linearity_gate"].get("actual_current_surface_status", "")
        and certificates["fh_lsz_finite_source_linearity_gate"].get("proposal_allowed") is False
        and certificates["fh_lsz_finite_source_linearity_gate"].get(
            "finite_source_linearity_gate_passed"
        )
        is False
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
    eight_mode_noise_variance_not_passed = (
        "eight-mode noise variance gate"
        in certificates["fh_lsz_eight_mode_noise_variance"].get("actual_current_surface_status", "")
        and certificates["fh_lsz_eight_mode_noise_variance"].get("proposal_allowed") is False
        and certificates["fh_lsz_eight_mode_noise_variance"].get("variance_gate_passed") is False
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
    joint_resource_multiday = (
        float(certificates["joint_resource_projection"].get("projection", {}).get("joint_mass_scaled_hours", 0.0)) > 1000.0
        and certificates["joint_resource_projection"].get("proposal_allowed") is False
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
        "fh-lsz-production-postprocess-gate-not-ready",
        production_postprocess_gate_not_ready,
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
        "fh-lsz-stieltjes-model-class-not-enough",
        stieltjes_model_class_not_enough,
        certificates["fh_lsz_stieltjes_model_class"].get("actual_current_surface_status", ""),
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
        "canonical-higgs-operator-realization-gate-blocks",
        canonical_higgs_operator_realization_gate_blocks,
        certificates["canonical_higgs_operator_realization_gate"].get("actual_current_surface_status", ""),
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
        "fh-lsz-finite-source-linearity-gate-blocks",
        finite_source_linearity_gate_blocks,
        certificates["fh_lsz_finite_source_linearity_gate"].get("actual_current_surface_status", ""),
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
        "fh-lsz-eight-mode-noise-variance-not-passed",
        eight_mode_noise_variance_not_passed,
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
        "joint-fh-lsz-resource-is-multiday",
        joint_resource_multiday,
        f"hours={certificates['joint_resource_projection'].get('projection', {}).get('joint_mass_scaled_hours')}",
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
            "inverse orthogonal mass.  "
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
        "direct_certificates": direct_meta,
        "required_certificates": required_certificates,
        "closure_routes": closure_routes,
        "exact_next_action": (
            "Do not run more small pilot MC for closure.  Either run the strict "
            "production physical-response manifest and follow it with pole/LSZ "
            "and matching analysis through the FH/LSZ postprocess gate, or derive "
            "the microscopic interacting scalar denominator/residue theorem from "
            "the retained action, including the canonical-Higgs pole identity, "
            "a source-pole mixing exclusion, a same-source sector-overlap "
            "identity, or a same-source gauge-mass response observable.  "
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
            "linearity gate is not passed."
            " Before treating chunked FH/LSZ as production evidence, also "
            "emit target-observable autocorrelation/ESS or blocking/bootstrap "
            "certificates.  For the source-Higgs lane, use the O_sp-normalized "
            "builder/postprocessor and supply a certified O_H with production "
            "C_sH/C_HH pole residues before running retained-route gating."
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
