# Audit Ledger

**Generated:** 2026-04-28T12:23:24.351635+00:00
**Source of truth:** `data/audit_ledger.json`
**Schema:** see [README.md](README.md), [FRESH_LOOK_REQUIREMENTS.md](FRESH_LOOK_REQUIREMENTS.md), and [ALGEBRAIC_DECORATION_POLICY.md](ALGEBRAIC_DECORATION_POLICY.md).

This file is auto-generated. Do not edit by hand. Apply audits via `scripts/apply_audit.py`, then re-run `scripts/compute_effective_status.py` and `scripts/render_audit_ledger.py`.

## Reading rule

- **Bold** = audit-ratified (`retained`, `promoted`).
- _Italic_ = author-proposed but not yet audit-ratified (`proposed_retained`, `proposed_promoted`).
- ~~Strikethrough~~ = audit returned a failure verdict.
- Plain = `support`, `bounded`, `open`, or `unknown`.

Publication-facing tables MUST read `effective_status`, not `current_status`.

## Summary

| effective_status | count |
|---|---:|
| **retained** | 79 |
| _proposed_retained_ | 3 |
| _proposed_promoted_ | 1 |
| bounded | 184 |
| support | 103 |
| open | 15 |
| unknown | 703 |
| ~~audited_decoration~~ | 3 |
| ~~audited_numerical_match~~ | 5 |
| ~~audited_renaming~~ | 3 |
| ~~audited_conditional~~ | 383 |
| ~~audited_failed~~ | 148 |

| audit_status | count |
|---|---:|
| `audited_clean` | 79 |
| `audited_conditional` | 151 |
| `audited_decoration` | 3 |
| `audited_failed` | 76 |
| `audited_numerical_match` | 5 |
| `audited_renaming` | 3 |
| `unaudited` | 1313 |

| criticality | count |
|---|---:|
| `critical` | 94 |
| `high` | 595 |
| `medium` | 97 |
| `leaf` | 844 |

- **Proposed claims demoted by upstream:** 140
- **Citation cycles detected:** 288

### Runner classification (static heuristic)

- runners classified: 695
- runners with (C) first-principles compute hits: 414
- runners with (D) external comparator hits: 186
- decoration candidates (no C, no D): 71

## Top 25 by load-bearing score (topology only)

Criticality and load-bearing score are computed from the citation graph alone. The audit lane intentionally does not use author-declared flagship status — that would let unratified framing drive audit cost on upstream support claims.

| # | claim_id | criticality | desc | score | audit_status | effective |
|---:|---|---|---:|---:|---|---|
| 1 | `ckm_cp_phase_structural_identity_theorem_note_2026-04-24` | critical | 175 | 33.96 | `unaudited` | ~~audited_conditional~~ |
| 2 | `wolfenstein_lambda_a_structural_identities_theorem_note_2026-04-24` | critical | 175 | 33.46 | `unaudited` | ~~audited_conditional~~ |
| 3 | `alpha_s_derived_note` | critical | 280 | 32.63 | `unaudited` | ~~audited_conditional~~ |
| 4 | `observable_principle_from_axiom_note` | critical | 282 | 29.14 | `audited_conditional` | ~~audited_conditional~~ |
| 5 | `ckm_magnitudes_structural_counts_theorem_note_2026-04-25` | critical | 175 | 28.46 | `unaudited` | ~~audited_conditional~~ |
| 6 | `ckm_atlas_axiom_closure_note` | critical | 175 | 25.96 | `unaudited` | ~~audited_conditional~~ |
| 7 | `ckm_atlas_triangle_right_angle_theorem_note_2026-04-24` | critical | 175 | 25.46 | `unaudited` | _proposed_promoted_ |
| 8 | `three_generation_structure_note` | critical | 278 | 25.12 | `unaudited` | ~~audited_conditional~~ |
| 9 | `one_generation_matter_closure_note` | critical | 278 | 24.62 | `unaudited` | ~~audited_conditional~~ |
| 10 | `three_generation_observable_theorem_note` | critical | 278 | 24.62 | `unaudited` | ~~audited_conditional~~ |
| 11 | `ckm_nlo_barred_triangle_protected_gamma_theorem_note_2026-04-25` | critical | 175 | 24.46 | `unaudited` | ~~audited_conditional~~ |
| 12 | `yt_ew_color_projection_theorem` | critical | 283 | 24.15 | `audited_conditional` | ~~audited_conditional~~ |
| 13 | `graph_first_su3_integration_note` | critical | 281 | 23.64 | `audited_clean` | **retained** |
| 14 | `yt_ward_identity_derivation_theorem` | critical | 278 | 23.62 | `unaudited` | ~~audited_conditional~~ |
| 15 | `anomaly_forces_time_theorem` | critical | 278 | 22.62 | `unaudited` | ~~audited_conditional~~ |
| 16 | `minimal_axioms_2026-04-11` | critical | 278 | 22.12 | `unaudited` | ~~audited_conditional~~ |
| 17 | `ckm_third_row_magnitudes_theorem_note_2026-04-24` | critical | 175 | 21.96 | `unaudited` | ~~audited_conditional~~ |
| 18 | `left_handed_charge_matching_note` | critical | 278 | 21.12 | `unaudited` | ~~audited_conditional~~ |
| 19 | `standard_model_hypercharge_uniqueness_theorem_note_2026-04-24` | critical | 278 | 20.62 | `unaudited` | ~~audited_conditional~~ |
| 20 | `higgs_mass_derived_note` | critical | 281 | 20.14 | `unaudited` | ~~audited_conditional~~ |
| 21 | `physical_lattice_necessity_note` | critical | 278 | 20.12 | `unaudited` | ~~audited_conditional~~ |
| 22 | `planck_parent_source_hidden_character_no_go_note_2026-04-24` | high | 124 | 19.97 | `audited_clean` | **retained** |
| 23 | `ckm_bs_mixing_phase_derivation_theorem_note_2026-04-25` | critical | 175 | 19.96 | `unaudited` | ~~audited_conditional~~ |
| 24 | `ckm_first_row_magnitudes_theorem_note_2026-04-24` | critical | 175 | 19.96 | `unaudited` | ~~audited_conditional~~ |
| 25 | `native_gauge_closure_note` | critical | 279 | 19.63 | `unaudited` | ~~audited_conditional~~ |


## Applied audits

| claim_id | current | audit_status | effective | independence | auditor_family | load-bearing class | decoration parent |
|---|---|---|---|---|---|---|---|
| `action_power_note` | _proposed_retained_ | ~~audited_clean~~ | **retained** | cross_family | codex-current | C | - |
| `alt_connectivity_family_basin_note` | _proposed_retained_ | ~~audited_clean~~ | **retained** | cross_family | codex-current | C | - |
| `alt_connectivity_family_fm_transfer_note` | _proposed_retained_ | ~~audited_clean~~ | **retained** | cross_family | codex-current | C | - |
| `alt_connectivity_family_sign_note` | _proposed_retained_ | ~~audited_clean~~ | **retained** | cross_family | codex-current | C | - |
| `atomic_rydberg_dependency_firewall_note_2026-04-27` | _proposed_retained_ | ~~audited_clean~~ | **retained** | fresh_context | codex-current | A | - |
| `charged_lepton_direct_ward_free_yukawa_no_go_note_2026-04-26` | _proposed_retained_ | ~~audited_clean~~ | **retained** | cross_family | codex-current | A | - |
| `charged_lepton_koide_ratio_source_selector_firewall_note_2026-04-27` | _proposed_retained_ | ~~audited_clean~~ | **retained** | cross_family | codex-current | A | - |
| `charged_lepton_op_local_source_selected_line_selector_no_go_note_2026-04-27` | _proposed_retained_ | ~~audited_clean~~ | **retained** | cross_family | codex-current | A | - |
| `charged_lepton_radiative_tau_selector_firewall_note_2026-04-26` | _proposed_retained_ | ~~audited_clean~~ | **retained** | cross_family | codex-current | A | - |
| `charged_lepton_selected_line_generation_selector_no_go_note_2026-04-27` | _proposed_retained_ | ~~audited_clean~~ | **retained** | cross_family | codex-current | A | - |
| `charged_lepton_typeb_radian_readout_generation_selector_no_go_note_2026-04-27` | _proposed_retained_ | ~~audited_clean~~ | **retained** | cross_family | codex-current | A | - |
| `claude_complex_action_carryover_note` | _proposed_retained_ | ~~audited_clean~~ | **retained** | cross_family | codex-current | C | - |
| `claude_complex_action_grown_companion_note` | _proposed_retained_ | ~~audited_clean~~ | **retained** | cross_family | codex-current | C | - |
| `composite_source_additivity_note` | _proposed_retained_ | ~~audited_clean~~ | **retained** | cross_family | codex-current | C | - |
| `distance_law_3d_64_closure_note_2026-04-11` | _proposed_retained_ | ~~audited_clean~~ | **retained** | cross_family | codex-current | C | - |
| `distance_law_preserving_third_family_note` | _proposed_retained_ | ~~audited_clean~~ | **retained** | cross_family | codex-current | C | - |
| `dm_neutrino_source_surface_p3_sylvester_linear_path_signature_theorem_note_2026-04-18` | _proposed_retained_ | ~~audited_clean~~ | **retained** | cross_family | codex-current | A | - |
| `electric_sign_law_note` | _proposed_retained_ | ~~audited_clean~~ | **retained** | cross_family | codex-current | C | - |
| `electrostatics_card_note` | _proposed_retained_ | ~~audited_clean~~ | **retained** | cross_family | codex-current | C | - |
| `electrostatics_superposition_proxy_note` | _proposed_retained_ | ~~audited_clean~~ | **retained** | cross_family | codex-current | C | - |
| `equivalence_principle_harness_note` | _proposed_retained_ | ~~audited_clean~~ | **retained** | cross_family | codex-current | C | - |
| `fixed_field_complex_grown_basin_v2_note` | _proposed_retained_ | ~~audited_clean~~ | **retained** | cross_family | codex-current | C | - |
| `fixed_field_family_unification_note` | _proposed_retained_ | ~~audited_clean~~ | **retained** | cross_family | codex-current | C | - |
| `fixed_field_grown_transfer_scout_note` | _proposed_retained_ | ~~audited_clean~~ | **retained** | cross_family | codex-current | C | - |
| `fm_transfer_note` | _proposed_retained_ | ~~audited_clean~~ | **retained** | cross_family | codex-current | C | - |
| `fourth_family_quadrant_note` | _proposed_retained_ | ~~audited_clean~~ | **retained** | cross_family | codex-current | C | - |
| `gate_b_grown_propagating_field_note` | _proposed_retained_ | ~~audited_clean~~ | **retained** | cross_family | codex-current | C | - |
| `gate_b_grown_propagating_field_v2_note` | _proposed_retained_ | ~~audited_clean~~ | **retained** | cross_family | codex-current | C | - |
| `gate_b_grown_propagating_field_v3_note` | _proposed_retained_ | ~~audited_clean~~ | **retained** | cross_family | codex-current | C | - |
| `gate_b_grown_trapping_frontier_note` | _proposed_retained_ | ~~audited_clean~~ | **retained** | cross_family | codex-current | C | - |
| `gate_b_grown_trapping_frontier_v2_note` | _proposed_retained_ | ~~audited_clean~~ | **retained** | cross_family | codex-current | C | - |
| `gate_b_grown_trapping_frontier_v3_note` | _proposed_retained_ | ~~audited_clean~~ | **retained** | cross_family | codex-current | C | - |
| `gate_b_grown_trapping_transport_note` | _proposed_retained_ | ~~audited_clean~~ | **retained** | cross_family | codex-current | C | - |
| `gate_b_grown_wavefield_companion_note` | _proposed_retained_ | ~~audited_clean~~ | **retained** | cross_family | codex-current | C | - |
| `gate_b_v6_nearfield_comparator_note` | _proposed_retained_ | ~~audited_clean~~ | **retained** | cross_family | codex-current | C | - |
| `gauge_vacuum_plaquette_first_sector_minimal_bulk_completion_3plus1_full_packet_no_go_theorem_note_2026-04-20` | _proposed_retained_ | ~~audited_clean~~ | **retained** | cross_family | codex-current | A | - |
| `graph_first_su3_integration_note` | _proposed_retained_ | ~~audited_clean~~ | **retained** | fresh_context | codex-current | C | - |
| `growing_graph_static_control_audit_note` | _proposed_retained_ | ~~audited_clean~~ | **retained** | cross_family | codex-current | C | - |
| `hadron_lane1_confinement_to_mass_firewall_note_2026-04-27` | _proposed_retained_ | ~~audited_clean~~ | **retained** | fresh_context | codex-current | A | - |
| `hubble_lane5_two_gate_dependency_firewall_note_2026-04-27` | _proposed_retained_ | ~~audited_clean~~ | **retained** | fresh_context | codex-current | A | - |
| `i3_zero_exact_theorem_note` | _proposed_retained_ | ~~audited_clean~~ | **retained** | cross_family | codex-current | A | - |
| `independent_generators_heldout_note` | _proposed_retained_ | ~~audited_clean~~ | **retained** | cross_family | codex-current | C | - |
| `koide_q_delta_residual_cohomology_obstruction_no_go_note_2026-04-24` | _proposed_retained_ | ~~audited_clean~~ | **retained** | cross_family | codex-current | A | - |
| `lattice_3d_dense_refinement_reconciliation_note` | _proposed_retained_ | ~~audited_clean~~ | **retained** | cross_family | codex-current | C | - |
| `lattice_3d_dense_window_extension_note` | _proposed_retained_ | ~~audited_clean~~ | **retained** | cross_family | codex-current | C | - |
| `lattice_3d_nyquist_diffraction_note` | _proposed_retained_ | ~~audited_clean~~ | **retained** | cross_family | codex-current | C | - |
| `lattice_3d_tapered_refinement_note` | _proposed_retained_ | ~~audited_clean~~ | **retained** | cross_family | codex-current | C | - |
| `lattice_distance_law_note` | _proposed_retained_ | ~~audited_clean~~ | **retained** | cross_family | codex-current | C | - |
| `lattice_nn_mass_response_note` | _proposed_retained_ | ~~audited_clean~~ | **retained** | cross_family | codex-current | C | - |
| `lattice_weak_field_mass_scaling_note` | _proposed_retained_ | ~~audited_clean~~ | **retained** | cross_family | codex-current | C | - |
| `lattice_weak_field_purity_scaling_note` | _proposed_retained_ | ~~audited_clean~~ | **retained** | cross_family | codex-current | C | - |
| `lensing_adjoint_kernel_reduced_model_note` | _proposed_retained_ | ~~audited_clean~~ | **retained** | cross_family | codex-current | C | - |
| `mirror_2d_validation_note` | _proposed_retained_ | ~~audited_clean~~ | **retained** | cross_family | codex-current | C | - |
| `mirror_chokepoint_boundary_fit_note` | _proposed_retained_ | ~~audited_clean~~ | **retained** | cross_family | codex-current | C | - |
| `moving_source_cross_family_note` | _proposed_retained_ | ~~audited_clean~~ | **retained** | cross_family | codex-current | C | - |
| `multipole_tidal_response_note` | _proposed_retained_ | ~~audited_clean~~ | **retained** | cross_family | codex-current | C | - |
| `neutrino_lane4_dirac_seesaw_fork_no_go_note_2026-04-27` | _proposed_retained_ | ~~audited_clean~~ | **retained** | fresh_context | codex-current | A | - |
| `nonlabel_grown_basin_note` | _proposed_retained_ | ~~audited_clean~~ | **retained** | cross_family | codex-current | C | - |
| `nonlabel_grown_drift_basin_note` | _proposed_retained_ | ~~audited_clean~~ | **retained** | cross_family | codex-current | C | - |
| `packet_memory_note` | _proposed_retained_ | ~~audited_clean~~ | **retained** | cross_family | codex-current | C | - |
| `persistent_inertial_object_probe_note` | _proposed_retained_ | ~~audited_clean~~ | **retained** | cross_family | codex-current | C | - |
| `planck_finite_response_no_go_note_2026-04-24` | _proposed_retained_ | ~~audited_clean~~ | **retained** | cross_family | codex-current | A | - |
| `planck_parent_source_hidden_character_no_go_note_2026-04-24` | _proposed_retained_ | ~~audited_clean~~ | **retained** | cross_family | codex-current | A | - |
| `planck_target3_phase_unit_edge_statistics_boundary_note_2026-04-25` | _proposed_retained_ | ~~audited_clean~~ | **retained** | cross_family | codex-current | C | - |
| `quark_bicac_endpoint_obstruction_theorem_note_2026-04-19` | _proposed_retained_ | ~~audited_clean~~ | **retained** | cross_family | codex-current | A | - |
| `quark_lane3_bounded_companion_retention_firewall_note_2026-04-27` | _proposed_retained_ | ~~audited_clean~~ | **retained** | fresh_context | codex-current | A | - |
| `s3_mass_matrix_no_go_note` | _proposed_retained_ | ~~audited_clean~~ | **retained** | fresh_context | codex-current | A | - |
| `self_gravity_entropy_note_2026-04-11` | _proposed_retained_ | ~~audited_clean~~ | **retained** | cross_family | codex-current | C | - |
| `shapiro_static_discriminator_note` | _proposed_retained_ | ~~audited_clean~~ | **retained** | cross_family | codex-current | C | - |
| `vector_magnetic_extension_note` | _proposed_retained_ | ~~audited_clean~~ | **retained** | cross_family | codex-current | C | - |
| `wave_amplification_near_horizon_note` | _proposed_retained_ | ~~audited_clean~~ | **retained** | cross_family | codex-current | C | - |
| `wave_retardation_lab_prediction_note` | _proposed_retained_ | ~~audited_clean~~ | **retained** | cross_family | codex-current | C | - |
| `wave_static_boundary_sensitivity_note` | _proposed_retained_ | ~~audited_clean~~ | **retained** | cross_family | codex-current | C | - |
| `wave_static_direct_probe_fine_note` | _proposed_retained_ | ~~audited_clean~~ | **retained** | cross_family | codex-current | C | - |
| `wave_static_fixed_beam_boundary_sensitivity_note` | _proposed_retained_ | ~~audited_clean~~ | **retained** | cross_family | codex-current | C | - |
| `wave_static_matrixfree_fixed_beam_boundary_note` | _proposed_retained_ | ~~audited_clean~~ | **retained** | cross_family | codex-current | C | - |
| `wave_static_matrixfree_moving_source_fixed_beam_boundary_note` | _proposed_retained_ | ~~audited_clean~~ | **retained** | cross_family | codex-current | C | - |
| `wave_static_single_source_compare_note` | _proposed_retained_ | ~~audited_clean~~ | **retained** | cross_family | codex-current | C | - |
| `wide_lattice_h2t_distance_law_note` | _proposed_retained_ | ~~audited_clean~~ | **retained** | cross_family | codex-current | C | - |
| `area_law_primitive_edge_entropy_selector_no_go_note_2026-04-25` | _proposed_retained_ | ~~audited_conditional~~ | ~~audited_conditional~~ | cross_family | codex-current | A | - |
| `area_law_quarter_broader_no_go_note_2026-04-25` | _proposed_retained_ | ~~audited_conditional~~ | ~~audited_conditional~~ | cross_family | codex-current | A | - |
| `broad_surrogate_point_source_compare_note` | _proposed_retained_ | ~~audited_conditional~~ | ~~audited_conditional~~ | cross_family | codex-current | C | - |
| `broken_graph_action_power_robustness_note` | _proposed_retained_ | ~~audited_conditional~~ | ~~audited_conditional~~ | cross_family | codex-current | C | - |
| `causal_escape_window_note` | _proposed_retained_ | ~~audited_conditional~~ | ~~audited_conditional~~ | cross_family | codex-current | C | - |
| `causal_field_canonical_chain_note` | _proposed_retained_ | ~~audited_conditional~~ | ~~audited_conditional~~ | cross_family | codex-current | B | - |
| `complex_action_note` | _proposed_retained_ | ~~audited_conditional~~ | ~~audited_conditional~~ | cross_family | codex-current | E | - |
| `composite_source_additivity_2d_note` | _proposed_retained_ | ~~audited_conditional~~ | ~~audited_conditional~~ | cross_family | codex-current | C | - |
| `confinement_string_tension_note` | _proposed_retained_ | ~~audited_conditional~~ | ~~audited_conditional~~ | cross_family | codex-current | B | - |
| `continuum_limit_note` | _proposed_retained_ | ~~audited_conditional~~ | ~~audited_conditional~~ | cross_family | codex-current | C | - |
| `cosmology_single_ratio_inverse_reconstruction_theorem_note_2026-04-25` | _proposed_retained_ | ~~audited_conditional~~ | ~~audited_conditional~~ | cross_family | codex-current | A | - |
| `cross_family_universality_note` | _proposed_retained_ | ~~audited_conditional~~ | ~~audited_conditional~~ | cross_family | codex-current | C | - |
| `diamond_nv_phase_ramp_signal_budget_note` | _proposed_retained_ | ~~audited_conditional~~ | ~~audited_conditional~~ | cross_family | codex-current | F | - |
| `diamond_signal_budget_hardening_note` | _proposed_retained_ | ~~audited_conditional~~ | ~~audited_conditional~~ | cross_family | codex-current | B | - |
| `distance_law_breakpoint_note` | _proposed_retained_ | ~~audited_conditional~~ | ~~audited_conditional~~ | cross_family | codex-current | B | - |
| `distance_law_frontier_audit_note` | _proposed_retained_ | ~~audited_conditional~~ | ~~audited_conditional~~ | cross_family | codex-current | B | - |
| `dm_abcc_chamber_bound_derivation_note_2026-04-20` | _proposed_retained_ | ~~audited_conditional~~ | ~~audited_conditional~~ | cross_family | codex-current | B | - |
| `dm_abcc_retained_measurement_closure_theorem_note_2026-04-21` | _proposed_retained_ | ~~audited_conditional~~ | ~~audited_conditional~~ | cross_family | codex-current | C | - |
| `dm_neutrino_bosonic_normalization_theorem_note_2026-04-15` | _proposed_retained_ | ~~audited_conditional~~ | ~~audited_conditional~~ | cross_family | codex-current | B | - |
| `dm_neutrino_schur_suppression_theorem_note_2026-04-15` | _proposed_retained_ | ~~audited_conditional~~ | ~~audited_conditional~~ | cross_family | codex-current | B | - |
| `dm_pmns_graph_first_ordered_chain_nonzero_current_activation_theorem_note_2026-04-21` | _proposed_retained_ | ~~audited_conditional~~ | ~~audited_conditional~~ | cross_family | codex-current | B | - |
| `early_family_transfer_connectivity_diagnosis` | _proposed_retained_ | ~~audited_conditional~~ | ~~audited_conditional~~ | cross_family | codex-current | B | - |
| `electrostatics_grown_sign_law_note` | _proposed_retained_ | ~~audited_conditional~~ | ~~audited_conditional~~ | cross_family | codex-current | C | - |
| `emergent_lorentz_invariance_note` | _proposed_retained_ | ~~audited_conditional~~ | ~~audited_conditional~~ | cross_family | codex-current | B | - |
| `family_companion_compare_note` | _proposed_retained_ | ~~audited_conditional~~ | ~~audited_conditional~~ | cross_family | codex-current | B | - |
| `fine_h_family_universality_note` | _proposed_retained_ | ~~audited_conditional~~ | ~~audited_conditional~~ | cross_family | codex-current | C | - |
| `four_d_distance_width_probe_note` | _proposed_retained_ | ~~audited_conditional~~ | ~~audited_conditional~~ | cross_family | codex-current | C | - |
| `gate_b_complex_action_falsifier_note` | _proposed_retained_ | ~~audited_conditional~~ | ~~audited_conditional~~ | cross_family | codex-current | C | - |
| `gate_b_grown_distance_law_note` | _proposed_retained_ | ~~audited_conditional~~ | ~~audited_conditional~~ | cross_family | codex-current | C | - |
| `gate_b_h025_distance_law_note` | _proposed_retained_ | ~~audited_conditional~~ | ~~audited_conditional~~ | cross_family | codex-current | C | - |
| `gate_b_h025_farfield_note` | _proposed_retained_ | ~~audited_conditional~~ | ~~audited_conditional~~ | cross_family | codex-current | C | - |
| `gate_b_strong_field_observable_split_note` | _proposed_retained_ | ~~audited_conditional~~ | ~~audited_conditional~~ | cross_family | codex-current | B | - |
| `gauge_scalar_temporal_completion_theorem_note` | support | ~~audited_conditional~~ | ~~audited_conditional~~ | fresh_context | codex-current | A | - |
| `gauge_vacuum_plaquette_constant_lift_obstruction_note` | unknown | ~~audited_conditional~~ | ~~audited_conditional~~ | fresh_context | codex-current | A | - |
| `gauge_vacuum_plaquette_first_sector_minimal_bulk_completion_3plus1_reduced_packet_complex_givens_selector_theorem_note_2026-04-20` | _proposed_retained_ | ~~audited_conditional~~ | ~~audited_conditional~~ | cross_family | codex-current | C | - |
| `gauge_vacuum_plaquette_first_sector_truncated_environment_packet_note_2026-04-19` | _proposed_retained_ | ~~audited_conditional~~ | ~~audited_conditional~~ | cross_family | codex-current | A | - |
| `gauge_vacuum_plaquette_first_sector_zero_extension_factorized_class_theorem_note_2026-04-19` | _proposed_retained_ | ~~audited_conditional~~ | ~~audited_conditional~~ | cross_family | codex-current | A | - |
| `gauge_vacuum_plaquette_mixed_cumulant_audit_note` | support | ~~audited_conditional~~ | ~~audited_conditional~~ | fresh_context | codex-current | A | - |
| `gauge_vacuum_plaquette_spatial_environment_tensor_transfer_theorem_note` | support | ~~audited_conditional~~ | ~~audited_conditional~~ | fresh_context | codex-current | A | - |
| `global_coherence_off_scaffold_note` | _proposed_retained_ | ~~audited_conditional~~ | ~~audited_conditional~~ | cross_family | codex-current | C | - |
| `graph_first_selector_derivation_note` | _proposed_retained_ | ~~audited_conditional~~ | ~~audited_conditional~~ | fresh_context | codex-current | A | - |
| `graph_phase_diagram_scout_note` | _proposed_retained_ | ~~audited_conditional~~ | ~~audited_conditional~~ | cross_family | codex-current | C | - |
| `gravitomagnetic_note` | _proposed_retained_ | ~~audited_conditional~~ | ~~audited_conditional~~ | cross_family | codex-current | C | - |
| `gravity_clean_derivation_note` | _proposed_retained_ | ~~audited_conditional~~ | ~~audited_conditional~~ | cross_family | codex-current | E | - |
| `growing_graph_frontier_architecture_transfer_note` | _proposed_retained_ | ~~audited_conditional~~ | ~~audited_conditional~~ | cross_family | codex-current | B | - |
| `grown_wavefield_failure_diagnosis_note` | _proposed_retained_ | ~~audited_conditional~~ | ~~audited_conditional~~ | cross_family | codex-current | B | - |
| `higgs_mass_retention_analysis_note_2026-04-18` | _proposed_retained_ | ~~audited_conditional~~ | ~~audited_conditional~~ | cross_family | codex-current | D | - |
| `higgs_z3_charge_pmns_gauge_redundancy_theorem_note_2026-04-17` | _proposed_retained_ | ~~audited_conditional~~ | ~~audited_conditional~~ | cross_family | codex-current | C | - |
| `higher_symmetry_joint_validation_note` | _proposed_retained_ | ~~audited_conditional~~ | ~~audited_conditional~~ | cross_family | codex-current | C | - |
| `impact_parameter_lensing_note` | _proposed_retained_ | ~~audited_conditional~~ | ~~audited_conditional~~ | cross_family | codex-current | C | - |
| `impact_parameter_portability_note` | _proposed_retained_ | ~~audited_conditional~~ | ~~audited_conditional~~ | cross_family | codex-current | C | - |
| `koide_a1_physical_bridge_attempt_2026-04-22` | _proposed_retained_ | ~~audited_conditional~~ | ~~audited_conditional~~ | cross_family | codex-current | A | - |
| `koide_a1_radian_bridge_irreducibility_audit_note_2026-04-24` | _proposed_retained_ | ~~audited_conditional~~ | ~~audited_conditional~~ | cross_family | codex-current | A | - |
| `koide_berry_phase_theorem_note_2026-04-19` | _proposed_retained_ | ~~audited_conditional~~ | ~~audited_conditional~~ | cross_family | codex-current | C | - |
| `koide_delta_marked_relative_cobordism_no_go_note_2026-04-24` | _proposed_retained_ | ~~audited_conditional~~ | ~~audited_conditional~~ | cross_family | codex-current | B | - |
| `koide_dimensionless_objection_closure_review_packet_2026-04-24` | _proposed_retained_ | ~~audited_conditional~~ | ~~audited_conditional~~ | cross_family | codex-current | A | - |
| `koide_kappa_block_total_frobenius_measure_theorem_note_2026-04-19` | _proposed_retained_ | ~~audited_conditional~~ | ~~audited_conditional~~ | cross_family | codex-current | C | - |
| `koide_kappa_spectrum_operator_bridge_theorem_note_2026-04-19` | _proposed_retained_ | ~~audited_conditional~~ | ~~audited_conditional~~ | cross_family | codex-current | A | - |
| `koide_native_dimensionless_review_packet_2026-04-24` | _proposed_retained_ | ~~audited_conditional~~ | ~~audited_conditional~~ | cross_family | codex-current | A | - |
| `koide_native_zero_section_closure_route_note_2026-04-24` | _proposed_retained_ | ~~audited_conditional~~ | ~~audited_conditional~~ | cross_family | codex-current | B | - |
| `koide_native_zero_section_nature_review_note_2026-04-24` | _proposed_retained_ | ~~audited_conditional~~ | ~~audited_conditional~~ | cross_family | codex-current | B | - |
| `koide_p_one_clock_3plus1_transport_reduction_note_2026-04-20` | _proposed_retained_ | ~~audited_conditional~~ | ~~audited_conditional~~ | cross_family | codex-current | B | - |
| `koide_pointed_origin_exhaustion_theorem_note_2026-04-24` | _proposed_retained_ | ~~audited_conditional~~ | ~~audited_conditional~~ | cross_family | codex-current | A | - |
| `koide_q_delta_readout_retention_split_no_go_note_2026-04-24` | _proposed_retained_ | ~~audited_conditional~~ | ~~audited_conditional~~ | cross_family | codex-current | B | - |
| `koide_selected_line_provenance_note_2026-04-20` | _proposed_retained_ | ~~audited_conditional~~ | ~~audited_conditional~~ | cross_family | codex-current | C | - |
| `koide_z3_qubit_radian_bridge_no_go_note_2026-04-20` | _proposed_retained_ | ~~audited_conditional~~ | ~~audited_conditional~~ | cross_family | codex-current | C | - |
| `lattice_complementarity_note` | _proposed_retained_ | ~~audited_conditional~~ | ~~audited_conditional~~ | cross_family | codex-current | C | - |
| `lattice_nn_distance_law_note` | _proposed_retained_ | ~~audited_conditional~~ | ~~audited_conditional~~ | cross_family | codex-current | C | - |
| `lensing_beta_sweep_note` | _proposed_retained_ | ~~audited_conditional~~ | ~~audited_conditional~~ | cross_family | codex-current | C | - |
| `lensing_deflection_note` | _proposed_retained_ | ~~audited_conditional~~ | ~~audited_conditional~~ | cross_family | codex-current | C | - |
| `lensing_k_sweep_note` | _proposed_retained_ | ~~audited_conditional~~ | ~~audited_conditional~~ | cross_family | codex-current | C | - |
| `linear_response_derivation_note` | _proposed_retained_ | ~~audited_conditional~~ | ~~audited_conditional~~ | cross_family | codex-current | C | - |
| `linear_response_second_order_kubo_note` | _proposed_retained_ | ~~audited_conditional~~ | ~~audited_conditional~~ | cross_family | codex-current | C | - |
| `linear_response_true_kubo_note` | _proposed_retained_ | ~~audited_conditional~~ | ~~audited_conditional~~ | cross_family | codex-current | A | - |
| `local_zsym_predictor_note` | _proposed_retained_ | ~~audited_conditional~~ | ~~audited_conditional~~ | cross_family | codex-current | C | - |
| `matter_inertial_closure_note` | _proposed_retained_ | ~~audited_conditional~~ | ~~audited_conditional~~ | cross_family | codex-current | C | - |
| `mirror_chokepoint_note` | _proposed_retained_ | ~~audited_conditional~~ | ~~audited_conditional~~ | cross_family | codex-current | C | - |
| `mirror_mutual_information_chokepoint_note` | _proposed_retained_ | ~~audited_conditional~~ | ~~audited_conditional~~ | cross_family | codex-current | C | - |
| `neutrino_dirac_z3_support_trichotomy_note` | _proposed_retained_ | ~~audited_conditional~~ | ~~audited_conditional~~ | cross_family | codex-current | B | - |
| `newton_derivation_note` | _proposed_retained_ | ~~audited_conditional~~ | ~~audited_conditional~~ | cross_family | codex-current | A | - |
| `observable_principle_from_axiom_note` | unknown | ~~audited_conditional~~ | ~~audited_conditional~~ | fresh_context | codex-current | A | - |
| `omega_lambda_matter_bridge_theorem_note_2026-04-22` | _proposed_retained_ | ~~audited_conditional~~ | ~~audited_conditional~~ | cross_family | codex-current | A | - |
| `persistent_object_blended_readout_transfer_sweep_note_2026-04-16` | _proposed_retained_ | ~~audited_conditional~~ | ~~audited_conditional~~ | cross_family | codex-current | C | - |
| `persistent_object_top4_multistage_outer_transfer_sweep_note_2026-04-16` | _proposed_retained_ | ~~audited_conditional~~ | ~~audited_conditional~~ | cross_family | codex-current | C | - |
| `planck_boundary_density_extension_theorem_note_2026-04-24` | _proposed_retained_ | ~~audited_conditional~~ | ~~audited_conditional~~ | cross_family | codex-current | A | - |
| `planck_source_unit_normalization_support_theorem_note_2026-04-25` | _proposed_retained_ | ~~audited_conditional~~ | ~~audited_conditional~~ | cross_family | codex-current | A | - |
| `pmns_hw1_source_transfer_boundary_note` | _proposed_retained_ | ~~audited_conditional~~ | ~~audited_conditional~~ | cross_family | codex-current | A | - |
| `pmns_selector_three_identity_support_note_2026-04-21` | _proposed_retained_ | ~~audited_conditional~~ | ~~audited_conditional~~ | cross_family | codex-current | G | - |
| `poisson_3d_self_field_note` | _proposed_retained_ | ~~audited_conditional~~ | ~~audited_conditional~~ | cross_family | codex-current | C | - |
| `poisson_self_field_note` | _proposed_retained_ | ~~audited_conditional~~ | ~~audited_conditional~~ | cross_family | codex-current | C | - |
| `propagator_family_unification_note` | _proposed_retained_ | ~~audited_conditional~~ | ~~audited_conditional~~ | cross_family | codex-current | B | - |
| `quantum_horizon_note` | _proposed_retained_ | ~~audited_conditional~~ | ~~audited_conditional~~ | cross_family | codex-current | C | - |
| `quark_bimodule_lo_shell_normalization_theorem_note_2026-04-19` | _proposed_retained_ | ~~audited_conditional~~ | ~~audited_conditional~~ | cross_family | codex-current | F | - |
| `quark_bimodule_norm_existence_theorem_note_2026-04-19` | _proposed_retained_ | ~~audited_conditional~~ | ~~audited_conditional~~ | cross_family | codex-current | A | - |
| `retardation_discriminator_note` | _proposed_retained_ | ~~audited_conditional~~ | ~~audited_conditional~~ | cross_family | codex-current | C | - |
| `retarded_field_compact_refinement_note` | _proposed_retained_ | ~~audited_conditional~~ | ~~audited_conditional~~ | cross_family | codex-current | C | - |
| `s3_taste_cube_decomposition_note` | support | ~~audited_conditional~~ | ~~audited_conditional~~ | fresh_context | codex-current | C | - |
| `second_grown_family_complex_note` | _proposed_retained_ | ~~audited_conditional~~ | ~~audited_conditional~~ | cross_family | codex-current | C | - |
| `shapiro_delay_note` | _proposed_retained_ | ~~audited_conditional~~ | ~~audited_conditional~~ | cross_family | codex-current | B | - |
| `shapiro_family_portability_note` | _proposed_retained_ | ~~audited_conditional~~ | ~~audited_conditional~~ | cross_family | codex-current | C | - |
| `sign_portability_invariant_note` | _proposed_retained_ | ~~audited_conditional~~ | ~~audited_conditional~~ | cross_family | codex-current | B | - |
| `sixth_family_distance_law_third_vs_sixth_quick_note` | _proposed_retained_ | ~~audited_conditional~~ | ~~audited_conditional~~ | cross_family | codex-current | C | - |
| `source_resolved_generated_support_recovery_basin_note` | _proposed_retained_ | ~~audited_conditional~~ | ~~audited_conditional~~ | cross_family | codex-current | C | - |
| `source_resolved_propagating_green_pocket_note` | _proposed_retained_ | ~~audited_conditional~~ | ~~audited_conditional~~ | cross_family | codex-current | C | - |
| `source_resolved_wavefield_escalation_note` | _proposed_retained_ | ~~audited_conditional~~ | ~~audited_conditional~~ | cross_family | codex-current | C | - |
| `source_resolved_wavefield_green_pocket_note` | _proposed_retained_ | ~~audited_conditional~~ | ~~audited_conditional~~ | cross_family | codex-current | C | - |
| `source_resolved_wavefield_mechanism_note` | _proposed_retained_ | ~~audited_conditional~~ | ~~audited_conditional~~ | cross_family | codex-current | C | - |
| `source_resolved_wavefield_v2_note` | _proposed_retained_ | ~~audited_conditional~~ | ~~audited_conditional~~ | cross_family | codex-current | C | - |
| `staggered_backreaction_shell_spectral_note` | _proposed_retained_ | ~~audited_conditional~~ | ~~audited_conditional~~ | cross_family | codex-current | C | - |
| `staggered_graph_failure_map_note` | _proposed_retained_ | ~~audited_conditional~~ | ~~audited_conditional~~ | cross_family | codex-current | C | - |
| `staggered_graph_gauge_closure_note` | _proposed_retained_ | ~~audited_conditional~~ | ~~audited_conditional~~ | cross_family | codex-current | C | - |
| `staggered_graph_gauge_closure_results_2026-04-10` | _proposed_retained_ | ~~audited_conditional~~ | ~~audited_conditional~~ | cross_family | codex-current | C | - |
| `staggered_graph_observables_note` | _proposed_retained_ | ~~audited_conditional~~ | ~~audited_conditional~~ | cross_family | codex-current | C | - |
| `staggered_graph_portability_note` | _proposed_retained_ | ~~audited_conditional~~ | ~~audited_conditional~~ | cross_family | codex-current | C | - |
| `staggered_graph_portability_stress_note` | _proposed_retained_ | ~~audited_conditional~~ | ~~audited_conditional~~ | cross_family | codex-current | C | - |
| `staggered_layered_gauge_engineering_note` | _proposed_retained_ | ~~audited_conditional~~ | ~~audited_conditional~~ | cross_family | codex-current | C | - |
| `staggered_layered_gauge_phase_diagram_note` | _proposed_retained_ | ~~audited_conditional~~ | ~~audited_conditional~~ | cross_family | codex-current | C | - |
| `strong_cp_theta_zero_note` | _proposed_retained_ | ~~audited_conditional~~ | ~~audited_conditional~~ | cross_family | codex-current | E | - |
| `structured_chokepoint_bridge_extension_note` | _proposed_retained_ | ~~audited_conditional~~ | ~~audited_conditional~~ | cross_family | codex-current | C | - |
| `structured_chokepoint_bridge_note` | _proposed_retained_ | ~~audited_conditional~~ | ~~audited_conditional~~ | cross_family | codex-current | C | - |
| `symmetry_head_to_head_note` | _proposed_retained_ | ~~audited_conditional~~ | ~~audited_conditional~~ | cross_family | codex-current | C | - |
| `taste_scalar_isotropy_theorem_note` | bounded | ~~audited_conditional~~ | ~~audited_conditional~~ | fresh_context | codex-current | A | - |
| `tensor_scalar_ratio_consolidation_theorem_note_2026-04-22` | _proposed_retained_ | ~~audited_conditional~~ | ~~audited_conditional~~ | cross_family | codex-current | B | - |
| `third_grown_family_sign_note` | _proposed_retained_ | ~~audited_conditional~~ | ~~audited_conditional~~ | cross_family | codex-current | C | - |
| `unpromoted_branch_retainability_audit_note` | _proposed_retained_ | ~~audited_conditional~~ | ~~audited_conditional~~ | cross_family | codex-current | B | - |
| `valley_linear_continuum_synthesis_note` | _proposed_retained_ | ~~audited_conditional~~ | ~~audited_conditional~~ | cross_family | codex-current | C | - |
| `vector_sector_note` | _proposed_retained_ | ~~audited_conditional~~ | ~~audited_conditional~~ | cross_family | codex-current | C | - |
| `wave_3plus1d_promotions_note` | _proposed_retained_ | ~~audited_conditional~~ | ~~audited_conditional~~ | cross_family | codex-current | C | - |
| `wave_equation_self_field_note` | _proposed_retained_ | ~~audited_conditional~~ | ~~audited_conditional~~ | cross_family | codex-current | C | - |
| `wave_radiation_note` | _proposed_retained_ | ~~audited_conditional~~ | ~~audited_conditional~~ | cross_family | codex-current | C | - |
| `wave_retardation_continuum_limit_note` | _proposed_retained_ | ~~audited_conditional~~ | ~~audited_conditional~~ | cross_family | codex-current | C | - |
| `wave_retarded_gravity_note` | _proposed_retained_ | ~~audited_conditional~~ | ~~audited_conditional~~ | cross_family | codex-current | C | - |
| `wave_static_matrixfree_shared_geometry_compare_note` | _proposed_retained_ | ~~audited_conditional~~ | ~~audited_conditional~~ | cross_family | codex-current | C | - |
| `weak_coupling_retention_note_2026-04-11` | _proposed_retained_ | ~~audited_conditional~~ | ~~audited_conditional~~ | cross_family | codex-current | C | - |
| `yt_class_6_c3_breaking_operator_note_2026-04-18` | _proposed_retained_ | ~~audited_conditional~~ | ~~audited_conditional~~ | cross_family | codex-current | A | - |
| `yt_ew_color_projection_theorem` | _proposed_retained_ | ~~audited_conditional~~ | ~~audited_conditional~~ | cross_family | codex-current | B | - |
| `yt_ew_delta_r_retention_analysis_note_2026-04-18` | _proposed_retained_ | ~~audited_conditional~~ | ~~audited_conditional~~ | cross_family | codex-current | D | - |
| `yt_generation_hierarchy_primitive_analysis_note_2026-04-18` | _proposed_retained_ | ~~audited_conditional~~ | ~~audited_conditional~~ | cross_family | codex-current | A | - |
| `yt_h_unit_flavor_column_decomposition_note_2026-04-18` | _proposed_retained_ | ~~audited_conditional~~ | ~~audited_conditional~~ | cross_family | codex-current | A | - |
| `yt_p1_bz_quadrature_full_staggered_pt_note_2026-04-18` | _proposed_retained_ | ~~audited_conditional~~ | ~~audited_conditional~~ | cross_family | codex-current | C | - |
| `yt_p1_bz_quadrature_numerical_note_2026-04-18` | _proposed_retained_ | ~~audited_conditional~~ | ~~audited_conditional~~ | cross_family | codex-current | C | - |
| `yt_p1_color_factor_retention_note_2026-04-17` | _proposed_retained_ | ~~audited_conditional~~ | ~~audited_conditional~~ | cross_family | codex-current | B | - |
| `yt_p1_delta_3_bz_computation_note_2026-04-17` | _proposed_retained_ | ~~audited_conditional~~ | ~~audited_conditional~~ | cross_family | codex-current | B | - |
| `yt_p1_delta_r_2_loop_extension_note_2026-04-18` | _proposed_retained_ | ~~audited_conditional~~ | ~~audited_conditional~~ | cross_family | codex-current | A | - |
| `yt_p1_delta_r_sm_rge_crosscheck_note_2026-04-18` | _proposed_retained_ | ~~audited_conditional~~ | ~~audited_conditional~~ | cross_family | codex-current | D | - |
| `yt_p1_i_s_lattice_pt_citation_note_2026-04-17` | _proposed_retained_ | ~~audited_conditional~~ | ~~audited_conditional~~ | cross_family | codex-current | B | - |
| `yt_p1_loop_geometric_bound_note_2026-04-17` | _proposed_retained_ | ~~audited_conditional~~ | ~~audited_conditional~~ | cross_family | codex-current | B | - |
| `yt_p1_shared_fierz_no_go_sub_theorem_note_2026-04-17` | _proposed_retained_ | ~~audited_conditional~~ | ~~audited_conditional~~ | cross_family | codex-current | B | - |
| `yt_p2_f_yt_loop_geometric_bound_note_2026-04-17` | _proposed_retained_ | ~~audited_conditional~~ | ~~audited_conditional~~ | cross_family | codex-current | B | - |
| `yt_p2_v_matching_theorem_note_2026-04-17` | _proposed_retained_ | ~~audited_conditional~~ | ~~audited_conditional~~ | cross_family | codex-current | B | - |
| `yt_p3_k_series_geometric_bound_note_2026-04-17` | _proposed_retained_ | ~~audited_conditional~~ | ~~audited_conditional~~ | cross_family | codex-current | B | - |
| `alpha_lm_geometric_mean_identity_theorem_note_2026-04-24` | _proposed_retained_ | ~~audited_decoration~~ | ~~audited_decoration~~ | cross_family | codex-current | A | - |
| `koide_q_eq_3delta_identity_note_2026-04-21` | _proposed_retained_ | ~~audited_decoration~~ | ~~audited_decoration~~ | cross_family | codex-current | A | - |
| `retained_cross_lane_consistency_support_note_2026-04-22` | _proposed_retained_ | ~~audited_decoration~~ | ~~audited_decoration~~ | cross_family | codex-current | B | - |
| `ai_methodology.raw.prompts_session_ebae4639_jonreilly` | _proposed_retained_ | ~~audited_failed~~ | ~~audited_failed~~ | cross_family | codex-current | B | - |
| `backreaction_note` | _proposed_retained_ | ~~audited_failed~~ | ~~audited_failed~~ | cross_family | codex-current | C | - |
| `causal_field_reconciliation_note` | _proposed_retained_ | ~~audited_failed~~ | ~~audited_failed~~ | cross_family | codex-current | C | - |
| `causal_propagating_field_note` | _proposed_retained_ | ~~audited_failed~~ | ~~audited_failed~~ | cross_family | codex-current | C | - |
| `clifford_bimodule_ray_saturation_future_target_note_2026-04-19` | _proposed_retained_ | ~~audited_failed~~ | ~~audited_failed~~ | cross_family | codex-current | E | - |
| `connectivity_family_v2_elliptical_duplicate_note` | _proposed_retained_ | ~~audited_failed~~ | ~~audited_failed~~ | cross_family | codex-current | C | - |
| `critical_exponents_topology_note_2026-04-10` | _proposed_retained_ | ~~audited_failed~~ | ~~audited_failed~~ | cross_family | codex-current | C | - |
| `distance_law_note` | _proposed_retained_ | ~~audited_failed~~ | ~~audited_failed~~ | cross_family | codex-current | C | - |
| `dm_abcc_basin_enumeration_completeness_theorem_note_2026-04-20` | _proposed_retained_ | ~~audited_failed~~ | ~~audited_failed~~ | cross_family | codex-current | C | - |
| `evolving_network_prototype_v2_note` | _proposed_promoted_ | ~~audited_failed~~ | ~~audited_failed~~ | cross_family | codex-current | C | - |
| `evolving_network_prototype_v3_note` | _proposed_promoted_ | ~~audited_failed~~ | ~~audited_failed~~ | cross_family | codex-current | C | - |
| `fifth_family_complex_note` | _proposed_retained_ | ~~audited_failed~~ | ~~audited_failed~~ | cross_family | codex-current | C | - |
| `fifth_family_radial_fm_transfer_note` | _proposed_retained_ | ~~audited_failed~~ | ~~audited_failed~~ | cross_family | codex-current | C | - |
| `fifth_family_radial_note` | _proposed_retained_ | ~~audited_failed~~ | ~~audited_failed~~ | cross_family | codex-current | C | - |
| `framework_bare_alpha_3_alpha_em_dimension_fixed_ratio_support_note_2026-04-25` | _proposed_retained_ | ~~audited_failed~~ | ~~audited_failed~~ | cross_family | codex-current | A | - |
| `gauge_vacuum_plaquette_first_sector_rank_one_factorized_class_boundary_note_2026-04-19` | _proposed_retained_ | ~~audited_failed~~ | ~~audited_failed~~ | cross_family | codex-current | A | - |
| `gauge_vacuum_plaquette_first_sector_tail_underdetermination_theorem_note_2026-04-19` | _proposed_retained_ | ~~audited_failed~~ | ~~audited_failed~~ | cross_family | codex-current | A | - |
| `geometry_superposition_dag_ensemble_note_2026-04-11` | _proposed_retained_ | ~~audited_failed~~ | ~~audited_failed~~ | cross_family | codex-current | C | - |
| `gravitomagnetic_portability_note` | _proposed_retained_ | ~~audited_failed~~ | ~~audited_failed~~ | cross_family | codex-current | C | - |
| `gravity_observable_hierarchy_note` | _proposed_retained_ | ~~audited_failed~~ | ~~audited_failed~~ | cross_family | codex-current | C | - |
| `grown_transfer_basin_note` | _proposed_retained_ | ~~audited_failed~~ | ~~audited_failed~~ | cross_family | codex-current | C | - |
| `h0125_failure_derivation` | _proposed_retained_ | ~~audited_failed~~ | ~~audited_failed~~ | cross_family | codex-current | C | - |
| `h2t_h0125_narrow_bridge_note` | _proposed_retained_ | ~~audited_failed~~ | ~~audited_failed~~ | cross_family | codex-current | C | - |
| `if_program_closing_note` | _proposed_retained_ | ~~audited_failed~~ | ~~audited_failed~~ | cross_family | codex-current | B | - |
| `inverse_problem_graph_requirements_note` | _proposed_retained_ | ~~audited_failed~~ | ~~audited_failed~~ | cross_family | codex-current | C | - |
| `kernel_vs_gravity_note` | _proposed_retained_ | ~~audited_failed~~ | ~~audited_failed~~ | cross_family | codex-current | C | - |
| `lattice_3d_dense_spent_delay_note` | _proposed_retained_ | ~~audited_failed~~ | ~~audited_failed~~ | cross_family | codex-current | C | - |
| `lattice_kernel_transfer_norm_note` | _proposed_promoted_ | ~~audited_failed~~ | ~~audited_failed~~ | cross_family | codex-current | C | - |
| `lattice_synthesis_guard_note` | _proposed_promoted_ | ~~audited_failed~~ | ~~audited_failed~~ | cross_family | codex-current | B | - |
| `localized_source_response_sweep_note` | _proposed_retained_ | ~~audited_failed~~ | ~~audited_failed~~ | cross_family | codex-current | C | - |
| `mesoscopic_surrogate_annular_tapered_sweep_note` | _proposed_retained_ | ~~audited_failed~~ | ~~audited_failed~~ | cross_family | codex-current | C | - |
| `mesoscopic_surrogate_compact_floor_sweep_note` | _proposed_retained_ | ~~audited_failed~~ | ~~audited_failed~~ | cross_family | codex-current | C | - |
| `mesoscopic_surrogate_h025_constrained_localization_note` | _proposed_retained_ | ~~audited_failed~~ | ~~audited_failed~~ | cross_family | codex-current | C | - |
| `mesoscopic_surrogate_threshold_2d_note` | _proposed_retained_ | ~~audited_failed~~ | ~~audited_failed~~ | cross_family | codex-current | C | - |
| `minimal_absorbing_horizon_probe_note` | _proposed_retained_ | ~~audited_failed~~ | ~~audited_failed~~ | cross_family | codex-current | C | - |
| `minimal_bidirectional_trapping_probe_note` | _proposed_retained_ | ~~audited_failed~~ | ~~audited_failed~~ | cross_family | codex-current | C | - |
| `mirror_2d_gravity_law_note` | _proposed_promoted_ | ~~audited_failed~~ | ~~audited_failed~~ | cross_family | codex-current | C | - |
| `mirror_grown_combined_note` | _proposed_retained_ | ~~audited_failed~~ | ~~audited_failed~~ | cross_family | codex-current | C | - |
| `mirror_vs_lattice_program_note` | _proposed_retained_ | ~~audited_failed~~ | ~~audited_failed~~ | cross_family | codex-current | B | - |
| `moonshot_other_testables_note` | _proposed_retained_ | ~~audited_failed~~ | ~~audited_failed~~ | cross_family | codex-current | B | - |
| `persistent_inertial_response_readiness_note` | _proposed_retained_ | ~~audited_failed~~ | ~~audited_failed~~ | cross_family | codex-current | B | - |
| `poisson_self_gravity_mechanism_note` | _proposed_retained_ | ~~audited_failed~~ | ~~audited_failed~~ | cross_family | codex-current | B | - |
| `portable_card_extension_note` | _proposed_retained_ | ~~audited_failed~~ | ~~audited_failed~~ | cross_family | codex-current | B | - |
| `portable_package_extension_note` | _proposed_retained_ | ~~audited_failed~~ | ~~audited_failed~~ | cross_family | codex-current | B | - |
| `qnm_control_hardening_note` | _proposed_retained_ | ~~audited_failed~~ | ~~audited_failed~~ | cross_family | codex-current | B | - |
| `quark_strc_observable_principle_note_2026-04-19` | _proposed_retained_ | ~~audited_failed~~ | ~~audited_failed~~ | cross_family | codex-current | E | - |
| `replay_environment_note` | _proposed_retained_ | ~~audited_failed~~ | ~~audited_failed~~ | cross_family | codex-current | B | - |
| `second_grown_family_note` | _proposed_retained_ | ~~audited_failed~~ | ~~audited_failed~~ | cross_family | codex-current | C | - |
| `session_summary_2026-04-01_topology` | _proposed_retained_ | ~~audited_failed~~ | ~~audited_failed~~ | cross_family | codex-current | B | - |
| `session_synthesis_2026-04-10_graph_axioms` | _proposed_retained_ | ~~audited_failed~~ | ~~audited_failed~~ | cross_family | codex-current | B | - |
| `shapiro_complex_interaction_note` | _proposed_retained_ | ~~audited_failed~~ | ~~audited_failed~~ | cross_family | codex-current | A | - |
| `shapiro_diamond_bridge_note` | _proposed_retained_ | ~~audited_failed~~ | ~~audited_failed~~ | cross_family | codex-current | F | - |
| `shapiro_diamond_frequency_bridge_note` | _proposed_retained_ | ~~audited_failed~~ | ~~audited_failed~~ | cross_family | codex-current | F | - |
| `shapiro_five_family_portability_note` | _proposed_retained_ | ~~audited_failed~~ | ~~audited_failed~~ | cross_family | codex-current | C | - |
| `shapiro_scaling_direct_replay_note` | _proposed_retained_ | ~~audited_failed~~ | ~~audited_failed~~ | cross_family | codex-current | B | - |
| `source_resolved_retarded_green_pocket_note` | _proposed_retained_ | ~~audited_failed~~ | ~~audited_failed~~ | cross_family | codex-current | C | - |
| `source_resolved_transverse_propagating_green_note` | _proposed_retained_ | ~~audited_failed~~ | ~~audited_failed~~ | cross_family | codex-current | C | - |
| `staggered_backreaction_capture_closure_note` | _proposed_retained_ | ~~audited_failed~~ | ~~audited_failed~~ | cross_family | codex-current | C | - |
| `staggered_backreaction_green_closure_note` | _proposed_retained_ | ~~audited_failed~~ | ~~audited_failed~~ | cross_family | codex-current | C | - |
| `staggered_backreaction_iterative_note` | _proposed_retained_ | ~~audited_failed~~ | ~~audited_failed~~ | cross_family | codex-current | C | - |
| `staggered_backreaction_nonlocal_closure_note` | _proposed_retained_ | ~~audited_failed~~ | ~~audited_failed~~ | cross_family | codex-current | C | - |
| `staggered_backreaction_results_2026-04-10` | _proposed_retained_ | ~~audited_failed~~ | ~~audited_failed~~ | cross_family | codex-current | C | - |
| `staggered_backreaction_scale_closure_note` | _proposed_retained_ | ~~audited_failed~~ | ~~audited_failed~~ | cross_family | codex-current | C | - |
| `structured_mirror_bornsafe_scan_note` | _proposed_retained_ | ~~audited_failed~~ | ~~audited_failed~~ | cross_family | codex-current | C | - |
| `testable_predictions_map_note` | _proposed_retained_ | ~~audited_failed~~ | ~~audited_failed~~ | cross_family | codex-current | B | - |
| `three_family_card_note` | _proposed_retained_ | ~~audited_failed~~ | ~~audited_failed~~ | cross_family | codex-current | B | - |
| `triage_no_promotion_note` | _proposed_retained_ | ~~audited_failed~~ | ~~audited_failed~~ | cross_family | codex-current | B | - |
| `unified_basin_freeze_note` | _proposed_retained_ | ~~audited_failed~~ | ~~audited_failed~~ | cross_family | codex-current | B | - |
| `work_history.repo.review_feedback.architecture_portability_audit_2026-04-11` | _proposed_retained_ | ~~audited_failed~~ | ~~audited_failed~~ | cross_family | codex-current | B | - |
| `yt_p1_delta_2_bz_computation_note_2026-04-17` | _proposed_retained_ | ~~audited_failed~~ | ~~audited_failed~~ | cross_family | codex-current | B | - |
| `yt_p1_delta_r_master_assembly_theorem_note_2026-04-18` | _proposed_retained_ | ~~audited_failed~~ | ~~audited_failed~~ | cross_family | codex-current | B | - |
| `yt_p1_h_unit_renormalization_framework_native_note_2026-04-17` | _proposed_retained_ | ~~audited_failed~~ | ~~audited_failed~~ | cross_family | codex-current | B | - |
| `yt_p1_rep_a_rep_b_cancellation_theorem_note_2026-04-17` | _proposed_retained_ | ~~audited_failed~~ | ~~audited_failed~~ | cross_family | codex-current | B | - |
| `yt_p3_msbar_to_pole_k1_framework_native_derivation_note_2026-04-17` | _proposed_retained_ | ~~audited_failed~~ | ~~audited_failed~~ | cross_family | codex-current | B | - |
| `yt_p3_msbar_to_pole_k2_color_factor_retention_note_2026-04-17` | _proposed_retained_ | ~~audited_failed~~ | ~~audited_failed~~ | cross_family | codex-current | B | - |
| `yt_p3_msbar_to_pole_k3_color_factor_retention_note_2026-04-17` | _proposed_retained_ | ~~audited_failed~~ | ~~audited_failed~~ | cross_family | codex-current | B | - |
| `bell_inequality_derived_note` | _proposed_retained_ | ~~audited_numerical_match~~ | ~~audited_numerical_match~~ | cross_family | codex-current | G | - |
| `ckm_down_type_scale_convention_support_note_2026-04-22` | _proposed_retained_ | ~~audited_numerical_match~~ | ~~audited_numerical_match~~ | cross_family | codex-current | G | - |
| `ew_coupling_derivation_note` | _proposed_retained_ | ~~audited_numerical_match~~ | ~~audited_numerical_match~~ | cross_family | codex-current | G | - |
| `koide_higgs_dressed_resolvent_root_theorem_note_2026-04-20` | _proposed_retained_ | ~~audited_numerical_match~~ | ~~audited_numerical_match~~ | cross_family | codex-current | G | - |
| `yt_p1_delta_1_bz_computation_note_2026-04-17` | _proposed_retained_ | ~~audited_numerical_match~~ | ~~audited_numerical_match~~ | cross_family | codex-current | G | - |
| `complex_selectivity_predictor_note` | _proposed_retained_ | ~~audited_renaming~~ | ~~audited_renaming~~ | cross_family | codex-current | F | - |
| `lattice_nn_light_cone_note` | _proposed_retained_ | ~~audited_renaming~~ | ~~audited_renaming~~ | cross_family | codex-current | F | - |
| `yt_ssb_matching_gap_analysis_note_2026-04-18` | _proposed_retained_ | ~~audited_renaming~~ | ~~audited_renaming~~ | cross_family | codex-current | F | - |


## Audit findings (full)

### `action_power_note`

- **Note:** [`ACTION_POWER_NOTE.md`](../../docs/ACTION_POWER_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_clean~~
- **effective_status:** **retained**  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** For the axiom-fork action S = L*|f|^0.5, the canonical harness supports a bounded 3D close-slit barrier card for Born/k=0/MI/d_TV/decoherence, a same-family no-barrier distance and mass-response companion, and a bounded negative for 3D barrier attraction on the ordered-family sweeps.  _(class `C`)_
- **chain closes:** True — The registered/source-note canonical harness reproduces the 2D and 3D action-power tables, and the source-note gravity-sign closure runner reproduces the 0/14 strength, 0/3 density, and 0/8 jitter negative sweeps. The source note explicitly scopes the result as an axiom fork and excludes same-harness Newtonian closure, 3D barrier attraction, continuum limits, and multi-spacing robustness.
- **rationale:** The bounded finite claim closes on its own terms: the action-power harness reproduces Born-clean and k=0-clean 3D barrier values, MI/d_TV/decoherence diagnostics, the no-barrier distance exponent about -1.84 with F proportional to M near 1.00, and the live gravity-sign closure reproduces the all-away ordered-family sweeps. This clean audit ratifies only the finite axiom-fork card and its stated negative boundary, not a replacement for the spent-delay flagship, not attraction on the barrier card, and not a continuum or robustness theorem. Residual boundary: the later dimensional-interpretation comparison row for the 3D spent-delay exponent is not needed for the retained action-power card and should not be treated as the audited result; the canonical runner's current spent-delay 3D no-barrier output is +0.74.
- **auditor confidence:** high

### `ai_methodology.raw.prompts_session_ebae4639_jonreilly`

- **Note:** [`ai_methodology/raw/prompts_session_ebae4639_jonreilly.md`](../../docs/ai_methodology/raw/prompts_session_ebae4639_jonreilly.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_failed~~
- **effective_status:** ~~audited_failed~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The raw prompt transcript records the ISSR1/BICAC/JTS chain and runner as proposed-retained support for quark endpoint closure.  _(class `B`)_
- **chain closes:** False — The queued source is a raw methodology transcript, not a canonical theorem note; it contains stale and contradictory embedded statuses for the ISSR1/JTS chain, while the live runner supports a different current theorem packet.
- **rationale:** Issue: the audited source artifact is a raw prompt transcript that quotes multiple inconsistent states of the ISSR1/BICAC/JTS work, including stale PASS=41/JTS-residue language and later task text asking for JTS proof work, whereas the live runner now reports PASS=13 for a separate current theorem packet. Why this blocks: a hostile physicist cannot ratify a stable proposed-retained theorem from a raw conversation transcript whose embedded status disagrees with the current runner and whose real theorem content lives in canonical QUARK_* notes outside this queue row. Repair target: remove or demote raw prompt transcripts from the proposed_retained audit queue, then register and audit docs/QUARK_ISSR1_BICAC_FORCING_THEOREM_NOTE_2026-04-19.md with its JTS and shell-normalization dependencies as the canonical claim. Claim boundary until fixed: it is safe to say the live ISSR1 runner verifies its finite affine-carrier/JTS/BICAC algebra with PASS=13 FAIL=0; it is not safe to retain this raw transcript as a scientific theorem.
- **open / conditional deps cited:**
  - `ai_methodology/raw/prompts_session_ebae4639_jonreilly.md is raw transcript rather than canonical theorem note`
  - `stale embedded PASS=41/JTS-residue transcript state conflicts with live PASS=13/JTS-derived runner state`
  - `canonical ISSR1/JTS theorem notes are not registered as this row's one-hop dependencies`
- **auditor confidence:** high

### `alpha_lm_geometric_mean_identity_theorem_note_2026-04-24`

- **Note:** [`ALPHA_LM_GEOMETRIC_MEAN_IDENTITY_THEOREM_NOTE_2026-04-24.md`](../../docs/ALPHA_LM_GEOMETRIC_MEAN_IDENTITY_THEOREM_NOTE_2026-04-24.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_decoration~~
- **effective_status:** ~~audited_decoration~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** By the retained definitions, alpha_LM^2 = (alpha_bare / u_0)^2 = alpha_bare^2 / u_0^2 = alpha_bare * (alpha_bare / u_0^2) = alpha_bare * alpha_s(v).  _(class `A`)_
- **chain closes:** True — The identity follows exactly from the coupling definitions stated in the source note, but it is only an algebraic restatement of the accepted coupling chain and has no independent comparator or physical observable.
- **rationale:** Issue: The load-bearing step is exact algebra from the definitions alpha_LM = alpha_bare/u_0 and alpha_s(v) = alpha_bare/u_0^2, but the row presents this bookkeeping corollary as a separate proposed-retained theorem and registers no parent dependency or primary runner. Why this blocks: A definition-level geometric-mean identity adds no independent observable, comparator, falsifiability, or new physical bridge beyond the upstream plaquette/coupling surface, so it should not inflate the retained claim surface as a standalone theorem. Repair target: Box this identity under the retained plaquette/coupling-chain parent, or re-promote only if it is shown to be genuine compression used load-bearing by downstream claims with an explicit parent dependency. Claim boundary until fixed: It is safe to state the exact identity as a bookkeeping corollary of the accepted coupling definitions and to use it to avoid double-counting alpha_LM and alpha_s(v) as independent knobs.
- **open / conditional deps cited:**
  - `accepted_plaquette_coupling_chain_parent_not_registered`
- **auditor confidence:** high

### `alt_connectivity_family_basin_note`

- **Note:** [`ALT_CONNECTIVITY_FAMILY_BASIN_NOTE.md`](../../docs/ALT_CONNECTIVITY_FAMILY_BASIN_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_clean~~
- **effective_status:** **retained**  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The note's load-bearing finite claim is that the parity-rotated sector-transition family has a bounded basin on the no-restore grown slice, with 32 of 45 drift/seed rows passing exact zero, neutral-cancellation, sign-orientation, and near-linear charge-scaling gates.  _(class `C`)_
- **chain closes:** True — The live basin runner reproduces the 9-drift by 5-seed sweep and the 32/45 passing-row count, and the printed row table shows exact zero/neutral controls plus near-linear exponents on the passing rows. The conclusion is narrow: it covers only this runner-defined alternative connectivity family on the tested no-restore grown slice, not seed-wide closure or a geometry-generic theorem.
- **rationale:** The source note is deliberately bounded and the live runner computes the disputed finite surface rather than importing the 32/45 result: it builds each drift/seed geometry, applies the parity-rotated connectivity, propagates zero, plus, minus, neutral, and double-charge sources, and gates rows on zero response, neutral cancellation, sign orientation, and exponent closeness to one. The safe conclusion follows as a finite computational basin statement and explicitly excludes seed-wide closure, a geometry-generic theorem, and uniqueness of the surviving family. Residual risk: the runner's final printed aggregate mean-exponent line uses the neutral column and prints 0.000000, but the per-row exponents and ok predicate carry the note's near-linear scaling statement.
- **auditor confidence:** high

### `alt_connectivity_family_fm_transfer_note`

- **Note:** [`ALT_CONNECTIVITY_FAMILY_FM_TRANSFER_NOTE.md`](../../docs/ALT_CONNECTIVITY_FAMILY_FM_TRANSFER_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_clean~~
- **effective_status:** **retained**  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The note's load-bearing finite claim is that the parity-rotated alternative connectivity family preserves weak-field F~M linearity over the tested no-restore grown-slice drift/seed grid, with 15 of 15 rows passing and mean F~M = 0.999994.  _(class `C`)_
- **chain closes:** True — The live runner rebuilds each stated drift/seed geometry, applies the alternative connectivity family, compares response at source strengths 5e-5 and 1e-4, and reproduces 15/15 passing rows with mean F~M = 0.999994. The result closes only as a finite weak-field transfer computation on the tested grid, not as an all-strength, all-seed, or geometry-generic theorem.
- **rationale:** The runner computes the load-bearing exponent from two independently propagated weak source amplitudes on each listed drift/seed row and gates the result at |F~M - 1| < 0.05; the current output matches the source note's 15/15 count and 0.999994 mean. The conclusion is correctly bounded to weak-field linearity across the stated tested drift range and does not assert family-wide sign closure, geometry genericity, or uniqueness. Residual risk is registration hygiene rather than science closure: the queue row has no runner_path or registered deps for the sign/basin notes even though the source note names those artifacts.
- **auditor confidence:** high

### `alt_connectivity_family_sign_note`

- **Note:** [`ALT_CONNECTIVITY_FAMILY_SIGN_NOTE.md`](../../docs/ALT_CONNECTIVITY_FAMILY_SIGN_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_clean~~
- **effective_status:** **retained**  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The note's load-bearing finite claim is that the parity-rotated sector-transition connectivity family is a bounded positive signed-source candidate on the no-restore grown slice, with 10 of 15 drift/seed rows passing exact zero, neutral cancellation, sign orientation, and near-linear charge-response gates.  _(class `C`)_
- **chain closes:** True — The live sign-sweep runner rebuilds the listed five-drift by three-seed grid, applies the alternative sector-transition connectivity, and reproduces 10/15 passing rows with drift coverage [0.0, 0.1, 0.2, 0.3, 0.5] and mean exponent 1.000035. The result closes only as a finite bounded positive candidate on this slice, not as seed-wide closure or a geometry-generic theorem.
- **rationale:** The source note's bounded claim is exactly what the runner checks: zero-source response, neutral +/- cancellation, sign orientation, and a double-to-single charge exponent near one for each drift/seed row. The current output matches the archived note values, including 10/15 passing rows, the per-drift pass pattern, and mean exponent 1.000035, while the source explicitly rejects family-wide and geometry-generic closure. Residual boundary: this is a finite computational lane candidate, not an analytic classification of all structured connectivity families.
- **auditor confidence:** high

### `area_law_primitive_edge_entropy_selector_no_go_note_2026-04-25`

- **Note:** [`AREA_LAW_PRIMITIVE_EDGE_ENTROPY_SELECTOR_NO_GO_NOTE_2026-04-25.md`](../../docs/AREA_LAW_PRIMITIVE_EDGE_ENTROPY_SELECTOR_NO_GO_NOTE_2026-04-25.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_conditional~~
- **effective_status:** ~~audited_conditional~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** Within the finite primitive-edge class with H_cell=C^16, rho=I_16/16, rank(P_A)=4, locality/additivity, and standard von Neumann or binary entropy, none of the canonical entropy constructions gives the coefficient 1/4, and a gapped edge needs an extra Schmidt-spectrum selector.  _(class `A`)_
- **chain closes:** False — The runner verifies the finite-cell entropy arithmetic and the tunable gapped-edge counterexample, but the primitive cell, Planck Target 2 entropy requirement, and claimed exhaustiveness of the allowed finite primitive-edge entropy class are not registered one-hop dependencies. The no-go therefore closes for the supplied standard entropy constructions, not as a retained framework-wide Target 2 obstruction.
- **rationale:** Issue: the note correctly separates the primitive trace 4/16 from several standard von Neumann/binary entropy values, but it relies on unregistered authority for the source-free C^16 primitive cell, the rank-four boundary projector, the Planck Target 2 entanglement-entropy interpretation, and the claim that the listed finite-cell entropy constructions exhaust the canonical primitive-edge class. Why this blocks: the runner proves the arithmetic for the listed constructions and shows a same-gap two-level edge can be tuned through entropy 1/4, but it does not derive the physical entropy carrier, prove that no other retained entropy/readout functional is allowed, or register the finite-boundary density/action-side 1/4 authority it is distinguishing from entanglement entropy. Repair target: register the Planck conditional packet, finite-boundary density extension/primitive trace theorem, Target 2 entropy-carrier definition, and any allowed entropy functional class as dependencies; add an exhaustion theorem or runner proving that every retained primitive-edge entropy candidate reduces to the checked cases unless a named selector is supplied. Claim boundary until fixed: it is safe to claim a conditional no-go: for the stated C^16/rank-4 primitive data and standard entropy choices, the canonical entropies are log16, log4, log2, H(1/4), or 1/2, not 1/4, and hitting 1/4 in a gapped edge requires an additional Schmidt-spectrum selector; it is not yet an audited retained proof that Target 2 cannot be closed by any CL3 primitive-edge entropy construction.
- **open / conditional deps cited:**
  - `Planck_conditional_packet_primitive_trace_c_cell_equals_1_over_4_not_registered`
  - `finite_boundary_density_extension_theorem_not_registered_or_audited_conditional`
  - `source_free_C16_primitive_cell_and_rank_four_projector_authority_not_registered`
  - `Planck_Target_2_entanglement_entropy_carrier_definition_not_registered`
  - `canonical_primitive_edge_entropy_functional_class_exhaustiveness_not_registered`
  - `gapped_edge_Schmidt_spectrum_selector_open`
  - `operational_primitive_boundary_entropy_theorem_open`
- **auditor confidence:** high

### `area_law_quarter_broader_no_go_note_2026-04-25`

- **Note:** [`AREA_LAW_QUARTER_BROADER_NO_GO_NOTE_2026-04-25.md`](../../docs/AREA_LAW_QUARTER_BROADER_NO_GO_NOTE_2026-04-25.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_conditional~~
- **effective_status:** ~~audited_conditional~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** Under the single-interval fiber hypothesis, N_Gamma(q) <= 2 almost everywhere, so I_x <= 2(2*pi)^(d-1) and c_Widom <= 1/6; c_Widom = 1/4 would require average crossing count 3.  _(class `A`)_
- **chain closes:** False — The local coarea/fiber-count no-go proof closes within the stated simple-fiber Widom assumptions, but the row's registered one-hop dependency is the bounded BH entropy lane, so retained propagation is not closed through the audit graph.
- **rationale:** Issue: the simple-fiber no-go algebra is correct, but the claim is registered as depending on `bh_entropy_derived_note`, whose current/effective status is bounded rather than retained. Why this blocks: the audit graph cannot ratify this proposed-retained row as clean while its only registered one-hop dependency remains a bounded companion lane, even though the local fiber-count theorem itself excludes 1/4 inside the stated class. Repair target: either register and clean-audit the actual retained Widom/no-go and boundary-rank normalization authorities needed by this theorem, or remove the bounded BH companion from the load-bearing dependency set if it is only contextual. Claim boundary until fixed: it is safe to claim an exact conditional no-go for flat-cut simple-fiber Widom carriers and Schur/direct-sum descendants under consistent boundary-rank normalization: they have c_Widom <= 1/6 and cannot yield 1/4; the result does not rule out multi-pocket/multi-band, non-Fermi-liquid, gapped horizon-sector, or separately derived primitive-boundary carriers.
- **open / conditional deps cited:**
  - `BH_ENTROPY_DERIVED_NOTE.md_registered_dependency_effective_status_bounded`
- **auditor confidence:** high

### `atomic_rydberg_dependency_firewall_note_2026-04-27`

- **Note:** [`ATOMIC_RYDBERG_DEPENDENCY_FIREWALL_NOTE_2026-04-27.md`](../../docs/ATOMIC_RYDBERG_DEPENDENCY_FIREWALL_NOTE_2026-04-27.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_clean~~
- **effective_status:** **retained**  (reason: `self`)
- **auditor:** `codex-audit-loop:fresh-2026-04-28-atomic_rydberg_dependency_firewall_note_2026-04-27`  (codex-current; independence=fresh_context)
- **load-bearing step:** Without these, the existing hydrogen/helium harness remains scaffold-only.  _(class `A`)_
- **chain closes:** True — The claim is a negative boundary: the note does not derive the Rydberg scale, but shows that direct use of the retained electroweak-scale alpha with textbook m_e gives the wrong atomic energy and that m_e, alpha(0), and the nonrelativistic physical-unit limit remain required inputs. The live runner verifies the dependency sensitivity and current scaffold-only state with PASS=12 FAIL=0.
- **rationale:** The retained content is the dependency firewall, not a Rydberg derivation. The note's load-bearing step closes because the standard formula is explicitly input-sensitive and direct substitution of alpha_EM(M_Z) gives -15.675 eV rather than the textbook -13.6057 eV, so the low-energy Coulomb coupling bridge is not a notation change. The live runner also confirms the current atomic scaffold imports textbook m_e and lacks an alpha(0) closure. Residual risk is downstream misuse: this audit does not ratify hydrogen, Lamb-shift, fine-structure, hyperfine, helium, or larger-atom predictions.
- **auditor confidence:** high

### `backreaction_note`

- **Note:** [`BACKREACTION_NOTE.md`](../../docs/BACKREACTION_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_failed~~
- **effective_status:** ~~audited_failed~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The note's load-bearing claim is that Poisson self-gravity produces a gravitational absorption threshold at G_crit ~ 0.011, with TOWARD deflection preserved and escape decreasing smoothly from above one to below one.  _(class `C`)_
- **chain closes:** False — The current Poisson runner does not reproduce the source-note threshold table: at G=0.010 the live escape is 1.0502, not 1.002, the first listed sub-unity escape is at G=0.050 with 0.9631, and the runner no longer samples the note's G=0.011/0.012/0.020 rows or field-strength-dependence check.
- **rationale:** Issue: the source note's quantitative absorption-threshold claim is stale against the live Poisson/self-consistency runners; the current Poisson output gives escape 1.0498 at G=0.005, 1.0502 at G=0.010, 0.9631 at G=0.050, and 0.7547 at G=0.100, not the note's 1.025, 1.002, 0.751, and 0.486 trend with G_crit ~ 0.011. Why this blocks: a hostile physicist cannot retain a claimed horizon-like threshold at G_crit ~ 0.011 or a smooth table-driven collapse transition when the current computation places the first listed sub-unity escape much later and shows unstable/away behavior at larger G. Repair target: restore the exact runner/version and sweep grid that generated the note, or update the note with a live asserted sweep including G=0.011, 0.012, 0.020, the field-strength-dependence rows, convergence gates, escape monotonicity checks, and Born checks on the same converged field. Claim boundary until fixed: it is safe to claim only that the current Poisson runner shows TOWARD deflection for G <= 0.1, escape below one by G=0.050 at s_ext=0.004, and a linear fixed-field Born check of 2.45e-16 in the separate self-consistency script; it is not safe to retain the note's G_crit ~ 0.011 gravitational-collapse threshold or its exact table.
- **open / conditional deps cited:**
  - `source_note_threshold_table_stale_against_scripts/backreaction_poisson.py`
  - `Gcrit_0.011_not_sampled_or_reproduced_by_live_runner`
  - `field_strength_dependence_rows_s_0.001_and_s_0.016_not_present_in_current_runner`
  - `high_G_live_runner_shows_unstable_away_behavior_not_smooth_threshold_table`
- **auditor confidence:** high

### `bell_inequality_derived_note`

- **Note:** [`BELL_INEQUALITY_DERIVED_NOTE.md`](../../docs/BELL_INEQUALITY_DERIVED_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_numerical_match~~
- **effective_status:** ~~audited_numerical_match~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** For the hard-coded two-species tensor product Hamiltonian H=H1⊗I+I⊗H1+G V(i,j)|i><i|⊗|j><j|, selected small-lattice/large-G points give Horodecki CHSH values above 2 while G=0 gives |S|=2.000.  _(class `G`)_
- **chain closes:** False — The runner reproduces CHSH violations for selected model parameters, but the physical tensor species, D5 Poisson coupling, and large-G/continuum scale selection are not derived or registered as one-hop retained inputs.
- **rationale:** Issue: the runner cleanly computes CHSH>2 for the specified two-species staggered-lattice Hamiltonian, but the retained claim is load-bearing on selected small lattices and large chosen G values, plus unregistered assumptions that two distinguishable retained species supply the bipartition and that the diagonal periodic-Poisson density coupling is the relevant gravitational interaction. Why this blocks: G=0 is a good null control, but the violations are parameter-surface results, not a derived physical Bell prediction; in 3D the runner itself shows no violation at G=1000 and violation only at G=2000/5000, while the note states that the physical interpretation of these couplings and the continuum limit are not established. Repair target: register the Hilbert/two-species matter theorem and D5 Poisson-coupling authority as one-hop dependencies, derive the physical normalization of G and its continuum scaling, and add a runner that tests a fixed derived coupling/continuum-refinement family rather than sweeping to violation. Claim boundary until fixed: it is safe to claim a reproducible model-surface CHSH violation for the listed finite lattices and selected couplings, with explicit Cl(3) taste-operator checks and G=0 null controls; it is not yet an audited retained framework-native or physical gravitational Bell-violation theorem.
- **open / conditional deps cited:**
  - `SINGLE_AXIOM_HILBERT_NOTE_not_registered_one_hop`
  - `retained_multi_species_matter_content_not_registered_one_hop`
  - `D5_periodic_Poisson_coupling_not_registered_one_hop`
  - `physical_G_normalization_and_continuum_limit_not_derived`
- **auditor confidence:** high

### `broad_surrogate_point_source_compare_note`

- **Note:** [`BROAD_SURROGATE_POINT_SOURCE_COMPARE_NOTE.md`](../../docs/BROAD_SURROGATE_POINT_SOURCE_COMPARE_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_conditional~~
- **effective_status:** ~~audited_conditional~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The note's load-bearing diagnostic claim is that, on the retained h=0.5, W=8, L=12 ordered-lattice family, the broad surrogate and equivalent-centroid point source give effectively identical probe-packet responses, with max TV distance 0.000051.  _(class `C`)_
- **chain closes:** False — The finite broad-vs-point comparison itself replays cleanly, but the source note is explicitly a bounded interpretive diagnostic resting on unregistered ordered-lattice and quasi-persistent relaunch controls, not a standalone retained theorem or persistent-mass claim.
- **rationale:** Issue: the runner cleanly verifies the five-probe broad-source versus point-source diagnostic, but the source row is only a bounded interpretive diagnostic on an upstream proposed/bounded ordered-lattice surrogate lane and has no registered dependencies for those carrier and relaunch controls. Why this blocks: a hostile physicist can accept max TV distance 0.000051 for the scripted probes without accepting a retained persistent-mass, inertial-response, or geometry-generic theorem, because the source itself says it compares two source representations rather than producing a self-maintaining object. Repair target: either demote/register this row as bounded support, or register the ordered-lattice packet reidentification and quasi-persistent relaunch notes as dependencies and state an explicit retained proposition with threshold, scale, probe-grid, and upstream carrier statuses. Claim boundary until fixed: it is safe to claim that the live runner reproduces the finite h=0.5, W=8, L=12 diagnostic in which the broad surrogate and centroid point source have max TV distance 5.1e-5 over probes z=0, +/-1, +/-2; it is not safe to retain more than that diagnostic.
- **open / conditional deps cited:**
  - `ORDERED_LATTICE_PACKET_REIDENTIFICATION_NOTE.md`
  - `ORDERED_LATTICE_QUASI_PERSISTENT_RELAUNCH_NOTE.md`
  - `ORDERED_LATTICE_QUASI_PERSISTENT_RELAUNCH_2D_NOTE.md`
  - `QUASI_PERSISTENT_RELAUNCH_PROBE_NOTE.md`
  - `scripts/broad_surrogate_point_source_compare.py_not_registered_as_runner_path`
- **auditor confidence:** high

### `broken_graph_action_power_robustness_note`

- **Note:** [`BROKEN_GRAPH_ACTION_POWER_ROBUSTNESS_NOTE.md`](../../docs/BROKEN_GRAPH_ACTION_POWER_ROBUSTNESS_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_conditional~~
- **effective_status:** ~~audited_conditional~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The note's load-bearing bounded claim is that the graph-damage ladder does not crown p=1 as the most robust action power: p=1 keeps the cleanest exponent when it survives, while p=2 survives more signed-damage cases.  _(class `C`)_
- **chain closes:** False — The live runner reproduces the summary-level bounded negative result, but the source note is a graph-damage replay on an upstream proposed/bounded ordered-lattice family, has a missing linked frozen log, and explicitly rejects a universal or structural uniqueness theorem.
- **rationale:** Issue: the finite replay supports the bounded negative summary, but the row is not a standalone retained theorem; it is a bounded graph-damage diagnostic on an upstream proposed_retained ordered-lattice family, its cited frozen log is absent from logs/, and its relation notes are themselves bounded fixed-family controls rather than registered retained dependencies. Why this blocks: a hostile physicist can accept the live summary toward/6 counts 3, 3, and 5 and mean |F~M-p| values 0.004, 0.000, and 0.057 without accepting any project-level robustness, uniqueness, or graph theorem. Repair target: either demote/register the row as bounded support, or register the ordered-lattice/action-power dependencies and add asserted runner gates for the intended finite proposition, including damage ladder, action powers, TOWARD counts, exponent deviations, and provenance for the frozen log. Claim boundary until fixed: it is safe to claim the current script's bounded replay says p=1 is exponent-clean but not the most sign-robust under this damage ladder; it is not safe to retain a stronger robustness or uniqueness claim.
- **open / conditional deps cited:**
  - `logs/2026-04-04-broken-graph-action-power-robustness.txt_missing`
  - `INVERSE_PROBLEM_NOTE.md`
  - `ACTION_UNIQUENESS_NOTE.md`
  - `ACTION_POWER_SCALING_SWEEP_NOTE.md`
  - `scripts/broken_graph_action_power_robustness.py_not_registered_as_runner_path`
- **auditor confidence:** high

### `causal_escape_window_note`

- **Note:** [`CAUSAL_ESCAPE_WINDOW_NOTE.md`](../../docs/CAUSAL_ESCAPE_WINDOW_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_conditional~~
- **effective_status:** ~~audited_conditional~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The note's load-bearing claim is that a causal-escape regime exists: at eta=20, s=0.004, the instantaneous field traps the beam while dynamic finite-speed fields escape, and the mechanism is average-exposure reduction rather than irreducible cone geometry.  _(class `C`)_
- **chain closes:** False — The live runner reproduces the headline instantaneous/forward/dynamic escape window and three-family portability, but it does not compute the note's boundary-law tables, four-seed robustness claim, or exposure-matched static proxy that carries the mechanism attribution.
- **rationale:** Issue: the headline causal escape window replays, but the retained mechanism and boundary package goes beyond the current runner: exposure-matched static escape is printed as a note rather than computed, the c_crit/eta_max/s-dependence tables are not replayed, and the listed four-seed robustness gate is not present in the live script. Why this blocks: a hostile physicist can accept the finite eta=20 window values inst=0.3907, fwd=0.5631, dyn0.5=0.9006, dyn0.25=0.9743, plus three-family dynamic portability near 0.98, without accepting the broader retained claim that the mechanism and boundary law have been computed and gated. Repair target: add asserted runner sections for exposure-matched static fields, seed-robust sweeps, c_crit, eta_max(c), s-dependence, and acceptance thresholds, then register scripts/causal_escape_window.py as the row's runner_path. Claim boundary until fixed: it is safe to claim a finite scripted escape-window example and three-family portability at eta=20, s=0.004; it is not safe to retain the full mechanism and boundary-law package from this note.
- **open / conditional deps cited:**
  - `exposure_matched_static_proxy_not_computed_by_live_runner`
  - `c_crit_eta_max_s_dependence_tables_not_replayed_by_live_runner`
  - `four_seed_robustness_gate_absent_from_live_runner`
  - `scripts/causal_escape_window.py_not_registered_as_runner_path`
- **auditor confidence:** high

### `causal_field_canonical_chain_note`

- **Note:** [`CAUSAL_FIELD_CANONICAL_CHAIN_NOTE.md`](../../docs/CAUSAL_FIELD_CANONICAL_CHAIN_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_conditional~~
- **effective_status:** ~~audited_conditional~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The package elevates the Shapiro phase lag and related causal-field observables as the canonical lab bridge while acknowledging that matched static cone/exposure proxies can reproduce the retained phase and escape effects and that c remains a free parameter.  _(class `B`)_
- **chain closes:** False — The note depends on multiple artifact notes/logs and lab-bridge claims that are not registered as one-hop dependencies, has no primary runner, and explicitly lacks a unique causal discriminator or absolute lab transfer/noise budget.
- **rationale:** Issue: the note is a proposed_retained causal-field package summary, but its numerical hierarchy and lab-facing Shapiro bridge rely on unregistered artifact scripts/logs/notes, and the source itself says the Shapiro phase and trapping escape are not uniquely causal because matched static proxies can reproduce them. Why this blocks: a retained canonical lab bridge cannot rest on a free cone speed c, missing transfer/noise/systematics budgets, no registered primary runner, and no one-hop retained support for the listed Shapiro, gravitomagnetic, escape, boundary-law, or diamond/NV bridge artifacts; the causal interpretation is underdetermined by the observable. Repair target: register the primary runners and logs for each retained observable, register the bridge notes as one-hop dependencies with their current statuses, derive or externally fix the field speed c, and add a discriminator runner comparing causal cone predictions against best matched static proxies plus a lab transfer/noise budget. Claim boundary until fixed: it is safe to treat this as a conditional inventory saying the causal-cone model naturally produces the listed phase/escape/gravitomagnetic signatures and that Shapiro phase is a shape-sensitive observable; it is not yet an audited retained causal-field lab prediction or unique causal discriminator.
- **open / conditional deps cited:**
  - `SHAPIRO_DELAY_NOTE.md_not_registered_one_hop`
  - `SHAPIRO_STATIC_DISCRIMINATOR_NOTE.md_not_registered_one_hop`
  - `GRAVITOMAGNETIC_NOTE.md_not_registered_one_hop`
  - `CAUSAL_ESCAPE_WINDOW_NOTE.md_not_registered_one_hop`
  - `diamond_NV_lab_bridge_notes_not_registered_one_hop`
  - `causal_field_primary_runner_not_registered`
- **auditor confidence:** high

### `causal_field_reconciliation_note`

- **Note:** [`CAUSAL_FIELD_RECONCILIATION_NOTE.md`](../../docs/CAUSAL_FIELD_RECONCILIATION_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_failed~~
- **effective_status:** ~~audited_failed~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The note concludes that the low-SNR fixed-anchor cross-family replay diagnoses a harness boundary and is not a refutation of the retained center-family causal-field result.  _(class `C`)_
- **chain closes:** False — The live portability runner reproduces the fixed-anchor exact-null and family-boundary table, but the retained center-family result is not replayable from its cited runner and the reconciliation diagnostic logs needed for source-placement and field-strength-scan claims are absent.
- **rationale:** Issue: the reconciliation note preserves a proposed-retained center-family causal-field result while the cited causal-field runner emits no executable verification, and the cited reconciliation diagnostic logs for source-node shifts and field-strength scans are missing from the audit packet. Why this blocks: a hostile physicist can replay the portability runner and accept the exact-null control plus fixed-anchor family-boundary table, but cannot verify the original 0.45 center-family dynamic-cone observable, its claimed seed/strength stability, or the diagnosis that source placement rather than another artifact causes the mismatch. Repair target: restore an executable center-family causal-field runner with archived output and hard assertions for instantaneous/forward/dynamic ratios and seed/strength stability; restore or recreate the reconciliation diagnostic runner/log showing selected source-node shifts and the field-strength scan; then register the causal-field and portability notes as explicit one-hop dependencies. Claim boundary until fixed: it is safe to claim that the current fixed-anchor portability runner has exact zero-source control and shows nonportable forward/dynamic ratios across three grown families; it is not safe to retain the center-family causal-field result or the reconciliation diagnosis as an audited retained conclusion.
- **open / conditional deps cited:**
  - `CAUSAL_PROPAGATING_FIELD_NOTE.md_center_family_result_not_replayable`
  - `scripts/causal_propagating_field.py_contains_no_executable_computation`
  - `logs/2026-04-06-causal-field-portability-probe.txt_missing`
  - `logs/2026-04-06-causal-field-reconciliation-diagnostic.txt_missing`
  - `source_placement_and_field_strength_scan_diagnosis_not_reproducible`
- **auditor confidence:** high

### `causal_propagating_field_note`

- **Note:** [`CAUSAL_PROPAGATING_FIELD_NOTE.md`](../../docs/CAUSAL_PROPAGATING_FIELD_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_failed~~
- **effective_status:** ~~audited_failed~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The note claims that an imposed causal cone field produces distinct stable deflection ratios on grown geometry: forward-only and dynamic c=1 near 0.63 of instantaneous, dynamic c=0.5 near 0.45, stable across strengths and seeds.  _(class `C`)_
- **chain closes:** False — The artifact chain names scripts/causal_propagating_field.py, but the live file is a 23-line docstring/comment stub with no computation, no main routine, and zero bytes of runner output. No archived output for this note is named or present in the source-note artifact chain.
- **rationale:** Issue: the retained positive depends on numerical ratios, seed/strength stability, and a geometry-independence claim, but the named runner contains no executable computation and produces no output. Why this blocks: a hostile auditor cannot verify the instantaneous, forward-only, c=1, or c=0.5 deflection ratios; cannot check the stated 0.63/0.45 numbers; cannot inspect the grown geometry, source placement, field definition, propagation speed convention, or seed/strength sweep; and cannot distinguish a true causal-cone observable from an imposed-field parameterization artifact. Repair target: restore or add a primary runner that builds the stated grown geometry, computes all four field cases, sweeps the stated strengths and seeds, archives deterministic output, and asserts the table values and stability tolerances; if the claim remains geometry-independent, include a registered portability sweep or theorem explaining why the ratio is not specific to the chosen generator/action. Claim boundary until fixed: it is safe only to say that the note reports an unverified inline calculation suggesting a finite-cone field may change deflection ratios; it is not safe to retain a positive observable, stability result, geometry-independence claim, or physical speed-of-field interpretation.
- **open / conditional deps cited:**
  - `scripts/causal_propagating_field.py_contains_no_executable_computation`
  - `runner_output_empty`
  - `archived_session_log_or_named_numeric_output_missing`
  - `seed_strength_and_geometry_independence_sweeps_not_reproducible`
- **auditor confidence:** high

### `charged_lepton_direct_ward_free_yukawa_no_go_note_2026-04-26`

- **Note:** [`CHARGED_LEPTON_DIRECT_WARD_FREE_YUKAWA_NO_GO_NOTE_2026-04-26.md`](../../docs/CHARGED_LEPTON_DIRECT_WARD_FREE_YUKAWA_NO_GO_NOTE_2026-04-26.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_clean~~
- **effective_status:** **retained**  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The gauge-allowed charged-lepton operator contains an arbitrary complex 3 x 3 Y_e matrix, so one-Higgs gauge selection does not determine y_tau or any charged-lepton eigenvalue.  _(class `A`)_
- **chain closes:** True — The negative claim closes as gauge bookkeeping: the allowed monomial is generation-blind and every Y_e entry remains gauge invariant. The note does not promote a mass theorem or import PDG masses as proof inputs.
- **rationale:** The no-go is narrow and supported by the runner: wrong-Higgs rejection is checked, arbitrary diagonal/off-diagonal Y_e entries remain allowed, and the top Ward 1/sqrt(6) normalization is shown to be tied to the Q_L color x isospin surface rather than the colorless charged-lepton monomial. PDG masses are comparator-only. This clean audit applies only to the negative boundary, not to charged-lepton mass closure.
- **auditor confidence:** high

### `charged_lepton_koide_ratio_source_selector_firewall_note_2026-04-27`

- **Note:** [`CHARGED_LEPTON_KOIDE_RATIO_SOURCE_SELECTOR_FIREWALL_NOTE_2026-04-27.md`](../../docs/CHARGED_LEPTON_KOIDE_RATIO_SOURCE_SELECTOR_FIREWALL_NOTE_2026-04-27.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_clean~~
- **effective_status:** **retained**  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** On the Brannen carrier Q=(c^2+2)/6 is independent of delta, and cyclic relabelings preserve Q and unordered ratios while moving the largest slot label.  _(class `A`)_
- **chain closes:** True — The negative firewall closes: even granting the Q and Brannen support values, the data do not select a physical generation or tau-scale label. The note explicitly leaves Q source selection, selected-line endpoint/readout, and generation selection as residuals.
- **rationale:** The runner verifies phase-erasure of Q, conditional status of the source and endpoint support, cyclic relabeling of the largest slot, and comparator-only use of PDG masses. That is sufficient for the no-go that Q plus Brannen phase support is not a standalone generation/tau-scale selector. It does not audit or retain native Q closure or delta/radian closure.
- **auditor confidence:** high

### `charged_lepton_op_local_source_selected_line_selector_no_go_note_2026-04-27`

- **Note:** [`CHARGED_LEPTON_OP_LOCAL_SOURCE_SELECTED_LINE_SELECTOR_NO_GO_NOTE_2026-04-27.md`](../../docs/CHARGED_LEPTON_OP_LOCAL_SOURCE_SELECTED_LINE_SELECTOR_NO_GO_NOTE_2026-04-27.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_clean~~
- **effective_status:** **retained**  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The granted C3-fixed onsite source is J=sI, a common scalar with no label coordinate, so adding it to the unbased selected-line orbit still supplies no C3-natural generation selector.  _(class `A`)_
- **chain closes:** True — The negative result closes: even under the granted OP-local source premise, the source is generation-symmetric and cannot base the selected-line orbit. The note does not derive the physical source premise or claim mass closure.
- **rationale:** The runner verifies J=sI, z=0, Q(z=0)=2/3 under the granted premise, then separately verifies that the source scalar plus selected-line orbit lacks a fixed singleton label. PDG masses remain comparator-only. This ratifies only the stronger-premise generation-selector no-go, not native Koide Q closure.
- **auditor confidence:** high

### `charged_lepton_radiative_tau_selector_firewall_note_2026-04-26`

- **Note:** [`CHARGED_LEPTON_RADIATIVE_TAU_SELECTOR_FIREWALL_NOTE_2026-04-26.md`](../../docs/CHARGED_LEPTON_RADIATIVE_TAU_SELECTOR_FIREWALL_NOTE_2026-04-26.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_clean~~
- **effective_status:** **retained**  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The electroweak charged-lepton Casimir vector is (1, 1, 1) across e, mu, tau, so the radiative alpha_LM/(4pi) scale is generation-blind and cannot select tau without an extra primitive.  _(class `A`)_
- **chain closes:** True — The no-go closes because the radiative factor is identical under generation relabeling. The note preserves the tau numerical match as support/comparator only and does not turn it into a standalone y_tau theorem.
- **rationale:** The runner checks that the Casimir and radiative y value are identical for all three charged-lepton generations, and that applying the same rule universally cannot fit electron and muon masses. The PDG tau agreement is explicitly fenced as comparator-only. The audited-clean result is only the standalone tau-selector no-go, not charged-lepton mass closure.
- **auditor confidence:** high

### `charged_lepton_selected_line_generation_selector_no_go_note_2026-04-27`

- **Note:** [`CHARGED_LEPTON_SELECTED_LINE_GENERATION_SELECTOR_NO_GO_NOTE_2026-04-27.md`](../../docs/CHARGED_LEPTON_SELECTED_LINE_GENERATION_SELECTOR_NO_GO_NOTE_2026-04-27.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_clean~~
- **effective_status:** **retained**  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** A natural single-label selector from the unbased C3 quotient would need a C3-fixed label, but the C3 action on the three labels is free and no fixed singleton exists.  _(class `A`)_
- **chain closes:** True — The no-go closes as finite C3 action algebra: unbased selected-line data can determine a sorted orbit but not a physical generation label. Based selectors exist only after extra basepoint/source/generation data are supplied.
- **rationale:** The runner checks that Q and unordered ratios survive cyclic relabeling while the largest slot moves through all labels, and it enumerates invariant subsets to show no singleton selector exists. PDG masses are comparator-only. The clean verdict is limited to the unbased selected-line generation-selector no-go.
- **auditor confidence:** high

### `charged_lepton_typeb_radian_readout_generation_selector_no_go_note_2026-04-27`

- **Note:** [`CHARGED_LEPTON_TYPEB_RADIAN_READOUT_GENERATION_SELECTOR_NO_GO_NOTE_2026-04-27.md`](../../docs/CHARGED_LEPTON_TYPEB_RADIAN_READOUT_GENERATION_SELECTOR_NO_GO_NOTE_2026-04-27.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_clean~~
- **effective_status:** **retained**  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** Granting scalar P_RADIAN and P_SOURCE data fixes Q, delta, and z as C3-invariant quotient data, but no label is fixed by the free C3 action, so no natural generation selector exists without a basepoint.  _(class `A`)_
- **chain closes:** True — The no-go closes because the stronger scalar readout premise remains label-free. The runner shows based endpoint-to-label maps exist only after choosing extra physical basepoint data.
- **rationale:** The runner grants the scalar Type-B-to-radian readout and z=0 support, then checks that cyclic relabeling preserves scalar data while moving the heaviest slot and leaving no invariant singleton. PDG masses are comparator-only. This clean audit ratifies the scalar-readout generation-selector no-go, not delta/radian closure or mass retention.
- **auditor confidence:** high

### `ckm_down_type_scale_convention_support_note_2026-04-22`

- **Note:** [`CKM_DOWN_TYPE_SCALE_CONVENTION_SUPPORT_NOTE_2026-04-22.md`](../../docs/CKM_DOWN_TYPE_SCALE_CONVENTION_SUPPORT_NOTE_2026-04-22.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_numerical_match~~
- **effective_status:** ~~audited_numerical_match~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The bounded lane's current live support uses threshold-local because R_pred matches R_thresh at +0.20% but is +15.0% above R_common; the scale split is exactly the transport factor.  _(class `G`)_
- **chain closes:** False — The runner verifies a coherent numerical relation among PDG scale conventions, but the threshold-local comparator and the 5/6 bridge are explicitly not derived by this note.
- **rationale:** Issue: The load-bearing support comes from choosing the threshold-local mass-ratio comparator, where the framework prediction is +0.20%, while the common-scale comparator gives a +15% mismatch; the note explicitly says the 5/6 bridge and the natural scale convention remain open. Why this blocks: A proposed-retained support claim cannot be ratified as structural closure when the sharp evidence depends on a selected comparator scale plus PDG running inputs, and no one-hop dependencies for alpha_s(v), CKM atlas, the 5/6 bridge, or the down-type lane are registered. Repair target: Derive the 5/6 bridge and a framework-natural scale-convention theorem, register those as clean dependencies, and keep the runner's exact transport identity separate from PDG comparator checks. Claim boundary until fixed: It is safe to claim that the threshold-local and common-scale comparisons differ by the QCD transport factor and that the threshold-local comparison gives a sub-percent numerical support check; it is not a retained theorem-grade down-type mass-ratio closure.
- **open / conditional deps cited:**
  - `DOWN_TYPE_MASS_RATIO_CKM_DUAL_NOTE.md`
  - `CKM_FIVE_SIXTHS_BRIDGE_SUPPORT_NOTE.md`
  - `ALPHA_S_DERIVED_NOTE.md`
  - `CKM_ATLAS_AXIOM_CLOSURE_NOTE.md`
  - `PDG_2024_mass_and_alpha_s_inputs`
- **auditor confidence:** high

### `claude_complex_action_carryover_note`

- **Note:** [`CLAUDE_COMPLEX_ACTION_CARRYOVER_NOTE.md`](../../docs/CLAUDE_COMPLEX_ACTION_CARRYOVER_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_clean~~
- **effective_status:** **retained**  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The note's load-bearing narrow claim is that the branch exact-lattice complex-action harness carries over on main: gamma=0 exactly reduces to the baseline, Born remains machine-clean on the frozen field, and increasing gamma drives a TOWARD-to-AWAY crossover while escape falls.  _(class `C`)_
- **chain closes:** True — The live runner reproduces the exact-lattice h=0.5, W=6, L=30 table in the source note, including gamma=0 delta +9.339748e-02, Born values 2.409e-15/3.941e-16/1.236e-16, and the gamma crossover between 0.05 and 0.10. The result is narrow to this exact-lattice frozen-field harness and does not imply geometry independence, continuum closure, or a self-gravity effective-theory derivation.
- **rationale:** The source note deliberately scopes the claim to a finite exact-lattice carryover, and the live runner computes all load-bearing quantities rather than importing the table: the gamma=0 reduction, three Born tests, and six gamma sweep rows all match the note. The note explicitly excludes geometry-generic, continuum, and Poisson-self-gravity effective-theory claims, so the retained result is only the narrow harness replay. Residual risk is provenance hygiene: the linked frozen log is absent from logs/, but the current runner output reproduces the frozen result.
- **auditor confidence:** high

### `claude_complex_action_grown_companion_note`

- **Note:** [`CLAUDE_COMPLEX_ACTION_GROWN_COMPANION_NOTE.md`](../../docs/CLAUDE_COMPLEX_ACTION_GROWN_COMPANION_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_clean~~
- **effective_status:** **retained**  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The note's load-bearing narrow claim is that the exact-lattice complex-action carryover survives on the retained grown row: gamma=0 reduction is exact, the Born proxy is machine-clean, weak-field F~M stays 1.000, and the gamma sweep has a TOWARD-to-AWAY crossover.  _(class `C`)_
- **chain closes:** True — The live runner reproduces the retained grown-row replay in the source note, including seed-0 gamma=0 delta +2.460475e-01, Born proxy 1.456e-15, F~M = 1.000 for all checked gammas, and the two-seed gamma crossover between 0.10 and 0.20. The result is scoped only to drift=0.2, restore=0.7, seeds 0 and 1 on this runner-defined grown row.
- **rationale:** The source note is intentionally narrow and the current runner recomputes each load-bearing quantity on the grown row rather than importing the table: exact gamma=0 reduction, one Born proxy, six weak-field F~M readouts, and six gamma-sweep rows match the note. The note explicitly excludes geometry-generic, continuum, and self-gravity-mechanism claims, so the clean result retains only the finite grown-row companion. Residual boundary: the Born check is a proxy on the grown graph and the runner path is not registered in the queue row.
- **auditor confidence:** high

### `clifford_bimodule_ray_saturation_future_target_note_2026-04-19`

- **Note:** [`CLIFFORD_BIMODULE_RAY_SATURATION_FUTURE_TARGET_NOTE_2026-04-19.md`](../../docs/CLIFFORD_BIMODULE_RAY_SATURATION_FUTURE_TARGET_NOTE_2026-04-19.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_failed~~
- **effective_status:** ~~audited_failed~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The source note explicitly says the ray-saturation theorem is a future mathematical target, not a proposed_retained theorem, and that no retention is claimed.  _(class `E`)_
- **chain closes:** False — There is no theorem, proof, runner, or retained result to audit; the queued proposed_retained status contradicts the source note's explicit status and honest-status sections.
- **rationale:** Issue: the queue presents this row as proposed_retained, but the source note repeatedly states it is a future target, not a theorem, not proposed_retained, and not part of the current publishable claim. Why this blocks: a hostile physicist cannot audit or retain a theorem that the source explicitly says has not been proven and is only a named research target for possibly deriving STRC later. Repair target: demote this row to open/future-target/support metadata, or replace it with an actual theorem note containing a proof or runner that derives STRC-LO from the stated Clifford bimodule inputs. Claim boundary until fixed: it is safe to cite this note only as a pre-registered research target and gap statement for Scenario C; it is not safe to treat it as retained, proposed_retained, or theorem-grade evidence.
- **open / conditional deps cited:**
  - `source_status_explicitly_not_proposed_retained`
  - `no_proof_or_runner_for_ray_saturation_theorem`
  - `STRC_remains_observable_principle_under_current_state`
- **auditor confidence:** high

### `complex_action_note`

- **Note:** [`COMPLEX_ACTION_NOTE.md`](../../docs/COMPLEX_ACTION_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_conditional~~
- **effective_status:** ~~audited_conditional~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The note introduces the ansatz S=L(1-f)+i gamma L f, so exp(i k S)=exp(i k L(1-f)) exp(-k gamma L f), and uses a free gamma sweep to interpolate between Newtonian deflection and absorption-biased centroid shifts.  _(class `E`)_
- **chain closes:** False — The complex-action form and gamma parameter are imposed rather than derived, the claimed horizon interpretation is not tied to black-hole observables, and the audit ledger has no registered runner/output for the numerical tables.
- **rationale:** Issue: the load-bearing step is an introduced complex-action ansatz with a free gamma parameter, not a retained derivation of a horizon term from Cl(3)/Z^3 or from the gravity chain; the registered audit packet also has no primary runner/output even though the note names a script and log. Why this blocks: Born preservation follows structurally from linearity once the kernel is accepted, and the tabulated centroid/escape behavior may be a valid model sweep, but a free imaginary coupling cannot support the retained claim that gravity and horizons are unified, nor can an absorption-biased AWAY centroid shift be identified with horizon physics without photon-sphere/Schwarzschild/Hawking or causal-horizon tests. Repair target: register scripts/complex_action_harness.py as the primary runner with deterministic output, derive gamma or the imaginary action term from retained primitives, run resolution/geometry checks around the exceptional point, and add horizon-specific observables rather than centroid-shift proxies. Claim boundary until fixed: it is safe to claim a conditional one-parameter complex-kernel model where gamma=0 reduces to the real-action propagator, linearity keeps I3 near machine zero, and positive gamma produces absorption-biased escape/centroid behavior in the listed setup; it is not yet an audited retained gravity-horizon unification theorem.
- **open / conditional deps cited:**
  - `complex_action_imaginary_term_derivation_not_registered`
  - `gamma_selection_theorem_not_registered`
  - `scripts/complex_action_harness.py_not_registered_primary_runner`
  - `logs/2026-04-05-complex-action-harness.txt_not_registered_primary_output`
  - `horizon_observable_bridge_not_derived`
- **auditor confidence:** high

### `complex_selectivity_predictor_note`

- **Note:** [`COMPLEX_SELECTIVITY_PREDICTOR_NOTE.md`](../../docs/COMPLEX_SELECTIVITY_PREDICTOR_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_renaming~~
- **effective_status:** ~~audited_renaming~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The note's load-bearing claim is that complex-action survival requires an anchor-local TOWARD-to-AWAY crossover and that coarser basin geometry does not predict survival.  _(class `F`)_
- **chain closes:** False — The script renders a hard-coded table of six family labels and identifies survival with the same anchor-local crossover used to decide whether the complex-action companion survived; it does not compute an independent predictor from held-out features or audited dependencies.
- **rationale:** Issue: the proposed predictor is not independent of the target label; it equates complex-action survival with the anchor-local TOWARD-to-AWAY crossover that defines the retained complex companion in the cited family cards, and the runner merely prints hard-coded rows rather than recomputing or validating them. Why this blocks: a hostile physicist can accept the table as a summary of six prior cards without accepting a retained predictor, because the discriminator includes the outcome it is meant to predict and depends on unregistered, mixed-status source notes. Repair target: register the family cards as dependencies, recompute their features and labels from runners, pre-specify predictor features that exclude the survival-defining crossover or test the crossover on held-out families, and restore/generate the cited log. Claim boundary until fixed: it is safe to say this static table summarizes that the currently retained complex-positive examples have local crossovers and the diagnosed boundaries do not; it is not safe to call that an independent retained predictor.
- **open / conditional deps cited:**
  - `logs/2026-04-06-complex-selectivity-predictor.txt_missing`
  - `GROWN_TRANSFER_BASIN_NOTE.md`
  - `SECOND_GROWN_FAMILY_COMPLEX_NOTE.md`
  - `ALT_CONNECTIVITY_FAMILY_COMPLEX_FAILURE_NOTE.md`
  - `THIRD_GROWN_FAMILY_COMPLEX_BOUNDARY_NOTE.md`
  - `FOURTH_FAMILY_COMPLEX_BOUNDARY_NOTE.md`
  - `FIFTH_FAMILY_COMPLEX_NOTE.md`
  - `FIFTH_FAMILY_COMPLEX_BOUNDARY_NOTE.md`
- **auditor confidence:** high

### `composite_source_additivity_2d_note`

- **Note:** [`COMPOSITE_SOURCE_ADDITIVITY_2D_NOTE.md`](../../docs/COMPOSITE_SOURCE_ADDITIVITY_2D_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_conditional~~
- **effective_status:** ~~audited_conditional~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The note's load-bearing bounded claim is that on the 2D ordered-lattice family, valley-linear remains source-additive to printed precision while spent-delay shows large non-additive deviations.  _(class `C`)_
- **chain closes:** False — The finite 2D additivity replay closes, but the source note is a bounded test-particle cross-family support card on an upstream proposed_retained 2D ordered-lattice lane and explicitly does not close persistent-pattern or inertial-mass derivation.
- **rationale:** Issue: the runner verifies the finite 2D additivity comparison, but the source row is a bounded support probe, not a standalone retained theorem; it depends on an unregistered proposed_retained 2D ordered-lattice/continuum lane and the 3D additivity note, and it explicitly leaves persistent-pattern inertia open. Why this blocks: a hostile physicist can accept the five valley-linear relative errors (0.04%, 0.04%, 0.08%, 0.00%, 0.01%) and five spent-delay deviations (about 25-29%) without accepting a first-principles Newton or inertial-mass closure. Repair target: register the 2D ordered-lattice lane and 3D additivity note as dependencies, register the runner path, and state the retained proposition as a bounded test-particle additivity theorem with explicit error thresholds and no persistent-mass implication. Claim boundary until fixed: it is safe to claim the current runner's finite 2D cross-family additivity support for valley-linear and non-additivity for spent-delay; it is not safe to retain a broader source/mass derivation.
- **open / conditional deps cited:**
  - `COMPOSITE_SOURCE_ADDITIVITY_NOTE.md`
  - `proposed_retained_2D_ordered_lattice_lane_not_registered_as_dependency`
  - `scripts/composite_source_additivity_2d_cross_family.py_not_registered_as_runner_path`
  - `persistent_pattern_inertia_explicitly_open`
- **auditor confidence:** high

### `composite_source_additivity_note`

- **Note:** [`COMPOSITE_SOURCE_ADDITIVITY_NOTE.md`](../../docs/COMPOSITE_SOURCE_ADDITIVITY_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_clean~~
- **effective_status:** **retained**  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The note's load-bearing narrow claim is that on the fixed weak-field 3D ordered-lattice test-particle family, valley-linear is genuinely additive under same-site source-strength and disjoint-source field composition while spent-delay is not.  _(class `C`)_
- **chain closes:** True — The live runner reproduces all five valley-linear additivity checks at 0.00% printed relative error and all five spent-delay non-additivity checks at about 24-29% relative error. The conclusion is restricted to the fixed weak-field test-particle family and explicitly does not derive persistent-pattern inertial mass or one-parameter mass closure.
- **rationale:** The runner computes the disputed finite comparisons directly on the stated 3D ordered-lattice family: three same-site strength-additivity rows and two disjoint-source field-additivity rows for both valley-linear and spent-delay. The source note keeps the retained statement narrow to test-particle source-response additivity and explicitly excludes persistent-pattern inertial mass and beyond-family one-parameter mass closure, so the chain closes only at that bounded surface. Residual boundary: downstream Newton or inertial-response claims must still carry their own open-step audits.
- **auditor confidence:** high

### `confinement_string_tension_note`

- **Note:** [`CONFINEMENT_STRING_TENSION_NOTE.md`](../../docs/CONFINEMENT_STRING_TENSION_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_conditional~~
- **effective_status:** ~~audited_conditional~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The framework's graph-first SU(3) gauge sector is SU(3) Yang-Mills at beta = 6.0, SU(3) YM confines at T = 0, and the string tension follows from the framework alpha_s(M_Z) = 0.1181 through standard lattice/EFT inputs.  _(class `B`)_
- **chain closes:** False — The note and runner combine unregistered upstream framework claims with external lattice-QCD and EFT inputs; the runner checks consistency after setting those premises rather than deriving the physical bridge from the allowed audit packet.
- **rationale:** Issue: The failed step is claiming retained confinement/string-tension closure from graph-first SU(3), alpha_s(M_Z), Wilson confinement, Sommer-scale lattice inputs, and quark-screening corrections while none of those load-bearing authorities are registered one-hop dependencies for this row; several runner PASS lines are hard-coded `True` physical premises or external comparator checks. Why this blocks: The current packet demonstrates a bounded consistency story, not a derivation that the framework gauge sector is the relevant SU(3) YM theory with a computed string tension; the numerical match depends on imported lattice/EFT constants and a screening factor. Repair target: Register clean dependencies for graph-first SU(3), g_bare/beta normalization, the alpha_s lane, and the lattice/EFT string-tension bridge, and replace hard-coded True checks with a runner that computes only the bridge quantities from declared inputs while labeling external comparators separately. Claim boundary until fixed: It is safe to say that, conditional on the framework gauge sector being SU(3) YM at beta = 6.0 and on the standard lattice/EFT bridge, the numbers are consistent with confinement and a 435-484 MeV string-tension range; it is not audit-retained as a zero-parameter confinement theorem.
- **open / conditional deps cited:**
  - `GRAPH_FIRST_SU3_INTEGRATION_NOTE.md`
  - `scripts/canonical_plaquette_surface.py`
  - `standard_lattice_qcd_sommer_and_string_tension_inputs`
- **auditor confidence:** high

### `connectivity_family_v2_elliptical_duplicate_note`

- **Note:** [`CONNECTIVITY_FAMILY_V2_ELLIPTICAL_DUPLICATE_NOTE.md`](../../docs/CONNECTIVITY_FAMILY_V2_ELLIPTICAL_DUPLICATE_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_failed~~
- **effective_status:** ~~audited_failed~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The source note's load-bearing conclusion is that the parity-tapered elliptical-shell rule is a diagnostic duplicate of the portable sign-law fixed point, not a new proposed_retained family.  _(class `C`)_
- **chain closes:** False — The source note explicitly denies a new proposed_retained family, and the live basin runner supports that boundary read: it finds a finite 12/18 signed-control surface inside the portable sign-law invariant, with sign-orientation failures on nearby rows.
- **rationale:** Issue: the queued proposed_retained status contradicts the source note, which states this is a diagnostic duplicate and not a new retained family; the live runner likewise says the elliptical-shell slice sits inside the portable sign-law invariant and is not counted as a new retained family. Why this blocks: a hostile physicist can accept the finite controls and 12/18 passing rows without accepting independent retained-family status, because the result is explicitly downstream of the already retained/conditional sign-portability invariant and adds no new order parameter. Repair target: demote or classify this row as duplicate/bounded diagnostic support, or produce a new theorem/runner showing an independent invariant or family-wide surface distinct from sign portability. Claim boundary until fixed: it is safe to claim the current basin runner finds exact zero/neutral controls, sign-law passes on 12/18 rows, mean exponent 0.999972 among passes, and sign-orientation boundary failures; it is not safe to call this a new proposed_retained family.
- **open / conditional deps cited:**
  - `source_status_explicitly_not_new_proposed_retained_family`
  - `sign_portability_invariant_note`
  - `logs/2026-04-06-connectivity-family-v2-elliptical-targeted.txt_missing`
  - `scripts/CONNECTIVITY_FAMILY_V2_BASIN.py_not_registered_as_runner_path`
- **auditor confidence:** high

### `continuum_limit_note`

- **Note:** [`CONTINUUM_LIMIT_NOTE.md`](../../docs/CONTINUUM_LIMIT_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_conditional~~
- **effective_status:** ~~audited_conditional~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The note claims a proposed-retained positive continuum-limit result for the h^2+T normalized dense 3D lattice: weak-field deflection changes only about 3% from h=0.25 to h=0.125 and F~M brackets 1.000.  _(class `C`)_
- **chain closes:** False — The live primary runner reproduces the finite h ladder, including T = 4.2735, 5.0807, 5.8019, 6.4683; F~M = 0.979, 0.991, 0.998, 1.018; and weak-field deflection +1.369007e-02 to +1.406306e-02 from h=0.25 to h=0.125. The clean continuum-limit chain does not close because P_det underflows toward zero, Born is skipped at h=0.25 and h=0.125, the final convergence step is a finite two-point diagnostic rather than an asymptotic proof, and the runner has no hard pass/fail assertions.
- **rationale:** Issue: the h^2+T replay is a strong finite refinement diagnostic, but the note overreads it as a well-defined continuum limit. Why this blocks: a hostile auditor can verify the four h rows and the +2.7% weak-field final-step change, but cannot certify a continuum limit while detector probability decays from 9.31e-20 to 1.30e-137, fine-h Born checks are skipped, strong-field gravity is nonmonotone, T grows logarithmically rather than converging, and the note itself says boundary leakage and <1% refinement remain unresolved. Repair target: implement the per-node T normalization or another boundary-leakage repair, rerun at least one finer h with stable P_det, add a fine-h Born/linearity proof or computation, include uncertainty/extrapolation for the weak-field limit, and make the runner assert the exact retained gates. Claim boundary until fixed: it is safe to claim a finite h^2+T weak-field convergence diagnostic on h=1, 0.5, 0.25, 0.125 with TOWARD sign, k=0 zero, F~M bracketing 1, and final weak-field deflection change about +2.7%; it is not yet a clean retained continuum-limit theorem.
- **open / conditional deps cited:**
  - `P_det_underflows_to_1.30e-137_at_h0.125`
  - `Born_skipped_at_h0.25_and_h0.125`
  - `only_four_h_values_and_final_two_point_2.7_percent_convergence_diagnostic`
  - `strong_field_gravity_nonmonotone_across_h`
  - `per_node_T_boundary_leakage_repair_not_implemented`
  - `runner_prints_SAFE_READ_without_hard_assertions`
- **auditor confidence:** high

### `cosmology_single_ratio_inverse_reconstruction_theorem_note_2026-04-25`

- **Note:** [`COSMOLOGY_SINGLE_RATIO_INVERSE_RECONSTRUCTION_THEOREM_NOTE_2026-04-25.md`](../../docs/COSMOLOGY_SINGLE_RATIO_INVERSE_RECONSTRUCTION_THEOREM_NOTE_2026-04-25.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_conditional~~
- **effective_status:** ~~audited_conditional~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** On the retained/admitted flat-FRW w_Lambda=-1 surface, the four inverse reconstructions L_H(a), L_q, L_mL, and L_acc must agree and equal (H_inf/H_0)^2.  _(class `A`)_
- **chain closes:** False — The inverse formulas close as exact algebra once the flat-FRW matter+radiation+Lambda surface and L=(H_inf/H_0)^2 bridge are assumed, but those authorities are not registered as one-hop dependencies for this audit row. The runner reads and status-checks those notes directly, so the retained/admitted surface is imported rather than supplied by the constrained audit packet.
- **rationale:** Issue: the theorem's exact inverse identities are algebraically correct on a flat matter+radiation+Lambda FRW surface with w_Lambda=-1 and L=Omega_Lambda,0=(H_inf/H_0)^2, but the audit row registers no one-hop dependencies for the FRW forward theorem, matter-bridge theorem, dark-energy EOS corollary, or cosmological-constant/spectral-gap identity that define that surface. Why this blocks: the result is not an unconditional retained theorem from the source note alone; the runner's authority-status PASSes read external notes and publication wiring files outside the ledger dependency packet, and the note itself says the matter-content bridge and numerical ratio remain open. Repair target: register the FRW kinematic reduction, Omega_Lambda matter bridge, dark-energy EOS, and spectral-gap authority notes as one-hop dependencies, audit or demote their statuses explicitly, and make the runner validate the inverse identities only after loading the registered authority set and its allowed status. Claim boundary until fixed: it is safe to claim a conditional algebraic certificate: given the stated flat-FRW w_Lambda=-1 surface, fixed R, nonnegative M,L, and the L=(H_inf/H_0)^2 bridge, each listed observable reconstructs the same L and cross-consistency can falsify that surface; it is not yet an audited retained cosmology closure or independent derivation of H_inf/H_0, Omega_Lambda, Omega_m, or the matter bridge.
- **open / conditional deps cited:**
  - `COSMOLOGY_FRW_KINEMATIC_REDUCTION_THEOREM_NOTE_2026-04-24.md_not_registered_one_hop_dependency`
  - `OMEGA_LAMBDA_MATTER_BRIDGE_THEOREM_NOTE_2026-04-22.md_not_registered_one_hop_dependency`
  - `DARK_ENERGY_EOS_RETAINED_COROLLARY_THEOREM_NOTE.md_not_registered_one_hop_dependency`
  - `COSMOLOGICAL_CONSTANT_SPECTRAL_GAP_IDENTITY_THEOREM_NOTE.md_not_registered_one_hop_dependency`
  - `flat_FRW_wLambda_minus_one_surface_is_admitted_not_independently_audited_here`
  - `matter_content_bridge_and_numerical_H_inf_over_H0_remain_open`
- **auditor confidence:** high

### `critical_exponents_topology_note_2026-04-10`

- **Note:** [`CRITICAL_EXPONENTS_TOPOLOGY_NOTE_2026-04-10.md`](../../docs/CRITICAL_EXPONENTS_TOPOLOGY_NOTE_2026-04-10.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_failed~~
- **effective_status:** ~~audited_failed~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The note's load-bearing finite-size scout claim is the current-output table of fitted G_crit and beta values across graph topologies, used as evidence for topology-dependent localization-onset behavior.  _(class `C`)_
- **chain closes:** False — The live runner no longer reproduces the source note's table: random_geometric_s8 and both causal-DAG rows are now degenerate, and the fitted G_crit/beta values for the remaining rows differ from the note.
- **rationale:** Issue: the source note's current-output table is stale relative to scripts/frontier_critical_exponents.py; the live output gives random_geometric_s8 degenerate at G_crit=1.0, random_geometric_s10 beta=0.7328 at G_crit=2.0, growing_n64 beta=0.3675 at G_crit=14.0, layered_cycle_8x8 beta=0.3348 at G_crit=5.0, and both causal-DAG rows degenerate. Why this blocks: a hostile physicist cannot retain the note's specific beta table or six-family interpretation when half the current rows are degenerate and the fit values have changed. Repair target: update the note to the live runner output, fix the runner path registration to scripts/frontier_critical_exponents.py, add assertions for fit/degenerate acceptance criteria, and rerun any intended multi-size or multi-seed checks before promoting topology-dependence beyond a scout. Claim boundary until fixed: it is safe to say the current runner is a finite-size scout with three nondegenerate fits whose beta values differ across topology labels; it is not safe to retain the stale table or any universality-class inference.
- **open / conditional deps cited:**
  - `source_note_table_stale_against_live_runner`
  - `runner_path_registered_without_scripts_prefix`
  - `three_of_six_live_rows_degenerate`
  - `finite_size_scaling_and_multiseed_robustness_open`
- **auditor confidence:** high

### `cross_family_universality_note`

- **Note:** [`CROSS_FAMILY_UNIVERSALITY_NOTE.md`](../../docs/CROSS_FAMILY_UNIVERSALITY_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_conditional~~
- **effective_status:** ~~audited_conditional~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** At H=0.5, the seed-mean dispersion (m_eff approx 5.9) and lensing slope (approx -1.3) show no detectable family effect across Fam1/Fam2/Fam3; the Schroedinger/KG near-tie persists in all families, though the winner flips across individual seeds.  _(class `C`)_
- **chain closes:** False — The named artifact scripts reproduce the seed-mean dispersion and lensing tables, but the statistical detection claim does not close because the runners do not emit per-seed slope/m_eff distributions, confidence intervals, or a formal family-effect/power test.
- **rationale:** Issue: the live scripts reproduce the H=0.5 seed-mean values, but the proposed-retained wording says there is no detectable family effect; that detection/noise statement relies on per-seed variance and statistical power that the current runners do not report or test. Why this blocks: close seed-mean fits across five seeds show finite-runner consistency, not a closed exclusion of family effects at the sampled size, and not universality beyond the three chosen grown-DAG parameter sets. Repair target: register the two artifact scripts as runners and add a computation that outputs per-seed m_eff and lensing-slope distributions with confidence intervals or a bootstrap/ANOVA/mixed-effects family test; test Fam2/Fam3 at H=0.25 before making any fine-H statement. Claim boundary until fixed: the safe claim is that scripts/dispersion_all_families.py and scripts/lensing_all_families.py currently reproduce the seed-mean H=0.5 tables: m_eff 5.98/5.90/5.88, Schroedinger/KG delta R2 below 0.01, and lensing slopes -1.3132/-1.3085/-1.2697 for the three named grown-DAG parameter families.
- **auditor confidence:** high

### `diamond_nv_phase_ramp_signal_budget_note`

- **Note:** [`DIAMOND_NV_PHASE_RAMP_SIGNAL_BUDGET_NOTE.md`](../../docs/DIAMOND_NV_PHASE_RAMP_SIGNAL_BUDGET_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_conditional~~
- **effective_status:** ~~audited_conditional~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The retained phase-sensitive / retarded / wavefield lane predicts a nonzero quadrature channel Y, a nonzero phase lag phi, and, in widefield readout, a coherent spatial phase ramp.  _(class `F`)_
- **chain closes:** False — The note bridges a framework phase-ramp proxy to real NV lock-in observables, but its own one-hop inputs include bounded or unaudited supports and the note explicitly says the validated map to a real NV coupling strength is still missing.
- **rationale:** Issue: the note presents a diamond/NV quadrature and spatial phase-ramp prediction by identifying the retained wavefield phase-ramp proxy with NV lock-in observables, but no runner or theorem constructs the NV forward model or the coupling-strength map. Why this blocks: without that physical-observable bridge, a nonzero framework phase ramp does not by itself imply measurable NV Y, phi, or widefield phase gradient, and the one-hop support includes unaudited proposed wavefield/unification notes plus bounded diamond protocol notes. Repair target: provide an ideal-detector forward model that maps the same driven source history to X, Y, phi, and spatial phase profile, with an explicit NV coupling theorem or calibrated input and with the wavefield/unification dependencies audited clean. Claim boundary until fixed: the safe claim is a bounded lab protocol proposal and discriminator design: measure lock-in quadrature and spatial phase profile, use the listed null/control stack, and do not claim absolute detectability or a closed NV prediction.
- **open / conditional deps cited:**
  - `SOURCE_RESOLVED_WAVEFIELD_MECHANISM_NOTE.md`
  - `SOURCE_RESOLVED_WAVEFIELD_ESCALATION_NOTE.md`
  - `PROPAGATOR_FAMILY_UNIFICATION_NOTE.md`
  - `DIAMOND_SENSOR_PROTOCOL_NOTE.md`
  - `DIAMOND_SENSOR_PREDICTION_NOTE.md`
- **auditor confidence:** high

### `diamond_signal_budget_hardening_note`

- **Note:** [`DIAMOND_SIGNAL_BUDGET_HARDENING_NOTE.md`](../../docs/DIAMOND_SIGNAL_BUDGET_HARDENING_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_conditional~~
- **effective_status:** ~~audited_conditional~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** Using a conservative 3sigma readout target, the weakest retained nonzero proxy rows imply centroid-noise target <= 2.888572e-07 and phase-noise target <= 4.363583e-06 rad.  _(class `B`)_
- **chain closes:** False — The arithmetic proxy-budget thresholds replay exactly, but they are computed from hard-coded rows imported from a bounded moving-source proxy note and do not include the transfer coefficient into real NV readout units.
- **rationale:** Issue: the note hardens the diamond/NV lane by dividing the weakest nonzero proxy observables by three, but the runner hard-codes the moving-source proxy rows and the cited source note is bounded, not audited-retained. Why this blocks: a proxy-unit 3sigma threshold is not a real lab signal budget unless a theorem or calibrated input maps the proxy centroid/phase units into NV readout units and noise floor. Repair target: audit or replace the moving-source proxy input with a retained source computation, then add the missing transfer calibration from proxy units to NV X/Y/phi readout units and rerun the budget from those calibrated quantities. Claim boundary until fixed: the safe claim is a bounded proxy-budget card for the specified grown-row geometry: if the copied proxy values are taken literally, the calculator gives centroid target 2.888572e-07 and phase target 4.363583e-06 rad; it does not establish absolute detectability or a completed lab budget.
- **open / conditional deps cited:**
  - `MOVING_SOURCE_RETARDED_PORTABILITY_NOTE.md`
- **auditor confidence:** high

### `distance_law_3d_64_closure_note_2026-04-11`

- **Note:** [`DISTANCE_LAW_3D_64_CLOSURE_NOTE_2026-04-11.md`](../../docs/DISTANCE_LAW_3D_64_CLOSURE_NOTE_2026-04-11.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_clean~~
- **effective_status:** **retained**  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The retained signal is the 31^3 through 64^3 grid sweep with largest-grid far-field exponent alpha = -1.023 +/- 0.012, finite-size extrapolation alpha_inf = -0.976 +/- 0.019, and largest-grid mass-linearity spread below 0.1%.  _(class `C`)_
- **chain closes:** True — The named runner directly recomputes the Poisson field, path-sum deflections, far-field fits, finite-size extrapolation, and largest-grid mass scaling, and its live output reproduces the note's bounded numerical values.
- **rationale:** The clean verdict is narrow. The live runner reproduces alpha(64^3) = -1.0233 +/- 0.0115, alpha_inf = -0.9762 +/- 0.0193, and delta/M spread 0.0010 on the specified Dirichlet 3D path-sum setup. The note explicitly limits the claim to a bounded numerical continuation and states that it is not full Newton closure, not architecture portability, and not a two-body M1 M2 theorem. Residual risk is therefore scope-bound: the result should only be cited for this finite path-sum surface and its stated convergence trend.
- **auditor confidence:** high

### `distance_law_breakpoint_note`

- **Note:** [`DISTANCE_LAW_BREAKPOINT_NOTE.md`](../../docs/DISTANCE_LAW_BREAKPOINT_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_conditional~~
- **effective_status:** ~~audited_conditional~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The distance tail survives only in open directed transport families; shell-locking, reflection closure, and deep branch routing break or flatten it.  _(class `B`)_
- **chain closes:** False — The runner prints a hard-coded comparison table and feature classifier; it does not recompute the alpha/direction rows or perform ablations that isolate the listed architecture features.
- **rationale:** Issue: the note turns a static breakpoint table into a causal architecture-feature diagnosis, but the runner only reprints hard-coded alpha/direction rows and labels. Why this blocks: the conclusion that open directed transport preserves the tail while shell routing, reflection closure, or deep branch routing break it requires either clean upstream rows or matched ablation computations; the cited distance-law portability note is unknown and the sign-invariant context is already conditional. Repair target: register and audit the upstream row computations, then add an ablation runner that toggles shell routing, dense fallback, reflection symmetry, branch depth, and radial confinement on matched geometries while recomputing alpha and direction. Claim boundary until fixed: it is safe to present the printed six-row comparison as a bounded diagnostic table; it is not an audited retained theorem that the named architecture features are the causal order parameters for distance-tail preservation.
- **open / conditional deps cited:**
  - `DISTANCE_LAW_PORTABILITY_NOTE.md`
  - `SIGN_PORTABILITY_INVARIANT_NOTE.md`
- **auditor confidence:** high

### `distance_law_frontier_audit_note`

- **Note:** [`DISTANCE_LAW_FRONTIER_AUDIT_NOTE.md`](../../docs/DISTANCE_LAW_FRONTIER_AUDIT_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_conditional~~
- **effective_status:** ~~audited_conditional~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The honest current frontier is compact grown-geometry transfer plus the independently replayed wide-lattice ordered h^2+T far-tail replay, both retained on main.  _(class `B`)_
- **chain closes:** False — The note is a cross-note frontier summary with no runner of its own, and its cited distance-law frontier inputs are unaudited proposed-retained rows rather than audit-retained authorities.
- **rationale:** Issue: the note claims the compact grown-geometry and wide-lattice distance-law pieces are the retained current frontier, but it provides no runner and depends entirely on three unaudited proposed-retained source notes. Why this blocks: an audit-lane retained summary cannot outrank its inputs; until the cited distance-law notes are audited clean, this note can only summarize proposed frontier candidates. Repair target: audit the Gate B grown, Gate B h=0.25, and wide-lattice h^2+T notes clean, or add a registered runner that independently recomputes the frontier comparison from those artifacts. Claim boundary until fixed: it is safe to say the note is a roadmap/synthesis identifying compact grown transfer and wide-lattice h^2+T replay as proposed distance-law frontier pieces, not that both are audit-retained.
- **open / conditional deps cited:**
  - `GATE_B_GROWN_DISTANCE_LAW_NOTE.md`
  - `GATE_B_H025_DISTANCE_LAW_NOTE.md`
  - `WIDE_LATTICE_H2T_DISTANCE_LAW_NOTE.md`
- **auditor confidence:** high

### `distance_law_note`

- **Note:** [`DISTANCE_LAW_NOTE.md`](../../docs/DISTANCE_LAW_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_failed~~
- **effective_status:** ~~audited_failed~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** Status headline: alpha ~ -1.5 in far field, steepening at larger b; later conclusion: the model produces a distance law of approximately 1/b with grown-geometry alpha = -0.96.  _(class `C`)_
- **chain closes:** False — The source note contains incompatible retained surfaces, and the current artifact set does not reproduce the W=40 alpha ~ -1.5 table from the status headline.
- **rationale:** Issue: the note's proposed-retained status claims a far-field alpha around -1.5 and continued steepening, but the note's own later conclusion claims an approximately 1/b law from the grown-geometry runner, and the current named artifacts do not reproduce the W=40 far-field table that carries the -1.5 headline. Why this blocks: the retained claim surface is internally contradictory and stale relative to the current artifact set; a reader cannot tell whether the proposed retained result is a steep non-Newtonian wide-lattice law or the grown-geometry alpha = -0.962 near-1/b result. Repair target: split or rewrite the note so the status, artifact chain, and runner output name one exact claim; either restore a runner that reproduces the W=40 b>=15/local-exponent table or demote that old table and retain only the current grown-geometry alpha = -0.962 result under its own bounded note. Claim boundary until fixed: it is safe to claim that scripts/distance_law_grown_geometry.py currently reproduces the grown-geometry table with all sampled b rows TOWARD and alpha(all b) = -0.962; the alpha ~ -1.5 far-field steepening headline is not audit-retained.
- **auditor confidence:** high

### `distance_law_preserving_third_family_note`

- **Note:** [`DISTANCE_LAW_PRESERVING_THIRD_FAMILY_NOTE.md`](../../docs/DISTANCE_LAW_PRESERVING_THIRD_FAMILY_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_clean~~
- **effective_status:** **retained**  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The high-drift/high-restore third family passes both gates on the direct test: exact zero and neutral controls, sign orientation, weak charge exponent 1.000, distance tail alpha = -1.150 with R^2 = 0.971, and 5/5 TOWARD.  _(class `C`)_
- **chain closes:** True — The live direct runner recomputes the specified drift=0.50, restore=0.90 family and reproduces the sign gate, weak scaling, tail alpha/R2, and direction count stated in the note.
- **rationale:** The clean verdict is limited to the direct high-drift/high-restore family tested by the runner. The live output gives zero = 0, neutral = 0, plus/minus antisymmetry, weak charge exponent 0.99998, tail alpha = -1.1501, R2 = 0.9714, and 5/5 TOWARD, matching the note. The distance-law portability context is not load-bearing here because it describes a different structured-family row; this note's own runner establishes the claimed direct preservation result. Residual risk is the stated scope: one family, finite seeds, and no geometry-universal theorem.
- **auditor confidence:** high

### `dm_abcc_basin_enumeration_completeness_theorem_note_2026-04-20`

- **Note:** [`DM_ABCC_BASIN_ENUMERATION_COMPLETENESS_THEOREM_NOTE_2026-04-20.md`](../../docs/DM_ABCC_BASIN_ENUMERATION_COMPLETENESS_THEOREM_NOTE_2026-04-20.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_failed~~
- **effective_status:** ~~audited_failed~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** Every chi2=0 chart point in the active chamber under any retained sigma lies within chart distance 0.15 of one of the five retained basins, so no additional chi2=0 chart point exists in the enclosure to the stated tolerance.  _(class `C`)_
- **chain closes:** False — The live runner reproduces PASS=30/FAIL=0, but the global exclusion is empirical multistart evidence, not a certified covering proof: it uses random far-field sampling, a 99.5-percentile finite-difference Lipschitz estimate, and an unproved comparable-attractor assumption for unknown basins.
- **rationale:** Issue: the runner verifies a large finite search and reproduces 30 PASS stamps, but the note promotes that search to a theorem-grade exhaustiveness certificate. Why this blocks: a dense grid plus Nelder-Mead can miss a narrow basin between seeds; the empirical 99.5-percentile Lipschitz estimate is not a worst-case bound, the far-field exclusion is random sampling rather than an analytic lower bound, and the claim that any unknown candidate basin would be reached analogously is exactly the missing theorem. Repair target: replace the heuristic certificate with an interval/branch-and-bound proof over the R=50 box, or a computer-algebra/root-isolation enumeration with certified eigenvalue-gap/Lipschitz bounds and a deterministic far-field asymptotic exclusion. Claim boundary until fixed: it is safe to claim that the current runner found only Basin 1, Basin 2, and Basin X in the active chamber under the retained sigma set, clustered them to the five-basin chart, and found no additional basin in this finite multistart/random-sampling scan; it is not an audited retained completeness theorem.
- **open / conditional deps cited:**
  - `DM_ABCC_CLOSURE_VIA_CHAMBER_BOUND_AND_DPLE_F4_NOTE_2026-04-19.md`
  - `DM_PNS_ATTACK_CASCADE_NOTE_2026-04-19.md`
  - `DM_ABCC_SIGNATURE_FORCING_THEOREM_NOTE_2026-04-19.md`
  - `SIGMA_HIER_UNIQUENESS_THEOREM_NOTE_2026-04-19.md`
  - `DM_ABCC_FIVE_BASIN_CHAMBER_DPLE_SUPPORT_THEOREM_NOTE_2026-04-21.md`
- **auditor confidence:** high

### `dm_abcc_chamber_bound_derivation_note_2026-04-20`

- **Note:** [`DM_ABCC_CHAMBER_BOUND_DERIVATION_NOTE_2026-04-20.md`](../../docs/DM_ABCC_CHAMBER_BOUND_DERIVATION_NOTE_2026-04-20.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_conditional~~
- **effective_status:** ~~audited_conditional~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The source-oriented-sheet branch of the carrier normal form fixes s = +sqrt(r31^2 - 1/4) >= 0, hence q_+ + delta >= sqrt(8/3).  _(class `B`)_
- **chain closes:** False — The algebraic implication from s >= 0 to the chamber bound is correct and the runner reproduces PASS=15/FAIL=0, but the sign/branch selection s >= 0 is imported from unaudited or already-conditional source-surface/carrier-normal-form notes.
- **rationale:** Issue: the proof's algebra is fine after the live branch is assumed, but the load-bearing choice of the positive branch s = +sqrt(r31^2 - 1/4) is delegated to source-oriented-sheet and carrier-normal-form authorities that are not audit-retained. Why this blocks: without an audited theorem fixing that branch orientation and excluding the mirror branch, the modulus identity r31^2 = s^2 + 1/4 only gives |s|, not q_+ + delta >= sqrt(8/3). Repair target: audit-clean the active affine/source-surface, active half-plane, Z3 doublet-block, intrinsic-slot, and slot-torsion boundary inputs, or reproduce the branch-selection proof fully here from retained primitives. Claim boundary until fixed: it is safe to claim the runner verifies the constants, chamber arithmetic on the listed basins, and the algebraic consequence s >= 0 => q_+ + delta >= sqrt(8/3); the structural chamber bound remains conditional on the branch-selection theorem.
- **open / conditional deps cited:**
  - `DM_NEUTRINO_SOURCE_SURFACE_ACTIVE_AFFINE_POINT_SELECTION_BOUNDARY_NOTE_2026-04-16.md`
  - `DM_NEUTRINO_SOURCE_SURFACE_ACTIVE_HALF_PLANE_THEOREM_NOTE_2026-04-16.md`
  - `DM_NEUTRINO_SOURCE_SURFACE_Z3_DOUBLET_BLOCK_POINT_SELECTION_THEOREM_NOTE_2026-04-16.md`
  - `DM_NEUTRINO_SOURCE_SURFACE_INTRINSIC_SLOT_THEOREM_NOTE_2026-04-16.md`
  - `DM_NEUTRINO_SOURCE_SURFACE_SLOT_TORSION_BOUNDARY_THEOREM_NOTE_2026-04-16.md`
- **auditor confidence:** high

### `dm_abcc_retained_measurement_closure_theorem_note_2026-04-21`

- **Note:** [`DM_ABCC_RETAINED_MEASUREMENT_CLOSURE_THEOREM_NOTE_2026-04-21.md`](../../docs/DM_ABCC_RETAINED_MEASUREMENT_CLOSURE_THEOREM_NOTE_2026-04-21.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_conditional~~
- **effective_status:** ~~audited_conditional~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The integration theorem claims A-BCC is closed on the retained measurement framework because the retained dependency stack selects J_phys=Basin 1, the P3 Sylvester/non-singularity path puts Basin 1 in C_base, Basin 2 and Basin X are in C_neg, and the signature-forcing/PNS implications then identify the physical endpoint with C_base.  _(class `C`)_
- **chain closes:** False — The primary runner passes 15/15 checks: seven dependency runners return rc=0/FAIL=0, direct determinant checks put Basin 1 in C_base and Basin 2/X in C_neg, and the captured dependency outputs contain the expected PNS and A-BCC implication strings. However, the audit row has no registered one-hop dependencies even though the proof explicitly rests on chamber completeness, upper-octant/source-cubic selection, sigma-hier selection, P3 Sylvester, PMNS non-singularity, Sylvester signature forcing, and the sigma-chain attack cascade. Without those dependencies registered and audited clean, this is a conditional integration result on the retained measurement surface, not a closed theorem-grade audit.
- **rationale:** The runner successfully verifies the integration theorem under its supplied retained-measurement stack: all seven nested runners pass, the hard-coded Basin 1 point satisfies the chamber bound and has positive endpoint determinant, Basin 2 and Basin X have negative endpoint determinants, and the captured dependency logs expose the asserted PNS/A-BCC reduction phrases. The conditional blocker is exact: the source note says it adds no new scientific input, yet the ledger records no one-hop dependency list for the input stack. A hostile audit therefore cannot independently promote the closure, because the active-chamber completeness theorem, sigma-chain selector, P3 Sylvester linear-path theorem, PMNS Non-Singularity theorem, signature-forcing theorem, and basin coordinate/source-family authorities are imported rather than audited here. It also remains explicitly outside an axiom-native Cl(3)/Z^3 derivation and leaves the microscopic right-sensitive selector outside this note's closure grade. To repair the claim, register every theorem/runner in the integration chain as one-hop dependencies with audited-clean status or include their theorem statements and hashes in the ledger snapshot; separately certify the full linear-path determinant minimum and the source-family/basin coordinates, not just endpoint signs, and register the microscopic selector stack if the current-package flagship closure is being claimed. What can still be safely claimed is conditional: on the retained measurement framework, if the seven dependency theorems are accepted, the integration runner verifies that A-BCC is no longer the live branch-choice blocker and that the remaining burden at this stage is the microscopic selector law. It does not prove a pure algebraic A-BCC theorem from Cl(3)/Z^3 alone.
- **open / conditional deps cited:**
  - `active_chamber_chi2_zero_completeness_theorem_not_registered_one_hop_dependency`
  - `exact_upper_octant_source_cubic_selector_theorem_not_registered_one_hop_dependency`
  - `sigma_hier_upper_octant_selector_theorem_not_registered_one_hop_dependency`
  - `P3_Sylvester_linear_path_physical_basin_theorem_not_registered_one_hop_dependency`
  - `PMNS_non_singularity_reduction_theorem_not_registered_one_hop_dependency`
  - `Sylvester_signature_forcing_theorem_not_registered_one_hop_dependency`
  - `sigma_chain_attack_cascade_runner_not_registered_one_hop_dependency`
  - `retained_affine_Hermitian_source_family_and_H_base_J_basin_coordinates_not_registered`
  - `five_route_assumptions_audit_boundary_for_pure_algebraic_A_BCC_not_registered_here`
  - `right_sensitive_microscopic_selector_law_later_same_day_stack_not_audited_in_this_claim`
- **auditor confidence:** high

### `dm_neutrino_bosonic_normalization_theorem_note_2026-04-15`

- **Note:** [`DM_NEUTRINO_BOSONIC_NORMALIZATION_THEOREM_NOTE_2026-04-15.md`](../../docs/DM_NEUTRINO_BOSONIC_NORMALIZATION_THEOREM_NOTE_2026-04-15.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_conditional~~
- **effective_status:** ~~audited_conditional~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** Physical local scalar observables must be source-response coefficients of the unique additive CPT-even generator W[J], so the physical normalization surface is Gamma_1 rather than the raw chiral bridge Y.  _(class `B`)_
- **chain closes:** False — The runner verifies the determinant and trace algebra, but the physical observable principle and retained local Higgs-family selection are imported as unregistered premises rather than proved or supplied as one-hop authorities.
- **rationale:** Issue: the algebraic checks close after accepting the observable-principle premise, but the note does not register or reproduce the theorem that physical local scalar observables are exactly W[J] source-response coefficients on the retained local Higgs family. Why this blocks: without that physical selection theorem, the runner only shows that Y has zero log-det response and Gamma_1 has nonzero even response; it does not by itself prove that the active-space ratio 1 is inadmissible or that 1/sqrt(2) is the physical normalization. Repair target: cite and audit-clean the observable-principle/local-Higgs-family theorem, or derive the admissibility criterion directly from retained primitives inside this note. Claim boundary until fixed: it is safe to claim the C^16 algebra, nilpotency, determinant response, and trace-ratio facts, including full-space ratio 1/sqrt(2) versus active-space ratio 1; the physical selection of 1/sqrt(2) remains conditional on the observable principle.
- **open / conditional deps cited:**
  - `observable_principle_unique_additive_CPT_even_generator_not_registered`
  - `retained_local_Higgs_family_not_registered`
- **auditor confidence:** high

### `dm_neutrino_schur_suppression_theorem_note_2026-04-15`

- **Note:** [`DM_NEUTRINO_SCHUR_SUPPRESSION_THEOREM_NOTE_2026-04-15.md`](../../docs/DM_NEUTRINO_SCHUR_SUPPRESSION_THEOREM_NOTE_2026-04-15.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_conditional~~
- **effective_status:** ~~audited_conditional~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** Assume the retained weak-axis local Higgs family, exact selector potential, direct Gamma_1 bridge, and bosonic-normalization theorem selecting j = g_weak/sqrt(2); then y_nu^eff = j^2 / 32 = g_weak^2 / 64.  _(class `B`)_
- **chain closes:** False — The runner verifies the local Schur complement algebra for the specified matrices, but the retained conclusion imports unregistered assumptions about the weak-axis local lane, Gamma_1 bridge, bosonic normalization, and DM staircase mapping.
- **rationale:** Issue: The exact Schur identity is proved for the chosen local block, but the theorem's retained claim depends on unregistered upstream inputs: the retained weak-axis Higgs family, the direct post-EWSB Gamma_1 bridge, the bosonic-normalization result j = g_weak/sqrt(2), and the staircase conversion from y_eff to k_eff. Why this blocks: Without those dependencies in the audit packet and clean in the ledger, the result is conditional algebra on selected inputs rather than an independently retained local neutrino suppression theorem. Repair target: Register clean dependency notes for the selector curvature, Gamma_1 bridge, bosonic normalization, and DM staircase relation, and make the runner read or compute those declared inputs while separating the exact Schur complement theorem from the downstream k_eff comparison. Claim boundary until fixed: It is safe to claim that for the specified projectors and block M(m,j), the Schur return gives j^2/m and therefore gives g_weak^2/64 if m = 32 and j = g_weak/sqrt(2); it is not audit-retained as a closed DM denominator result.
- **open / conditional deps cited:**
  - `weak_axis_local_higgs_family_dependency_not_registered`
  - `gamma_1_direct_bridge_dependency_not_registered`
  - `bosonic_normalization_dependency_not_registered`
  - `dm_staircase_relation_dependency_not_registered`
- **auditor confidence:** high

### `dm_neutrino_source_surface_p3_sylvester_linear_path_signature_theorem_note_2026-04-18`

- **Note:** [`DM_NEUTRINO_SOURCE_SURFACE_P3_SYLVESTER_LINEAR_PATH_SIGNATURE_THEOREM_NOTE_2026-04-18.md`](../../docs/DM_NEUTRINO_SOURCE_SURFACE_P3_SYLVESTER_LINEAR_PATH_SIGNATURE_THEOREM_NOTE_2026-04-18.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_clean~~
- **effective_status:** **retained**  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** For the specified H_base, affine generators, and P3 pin J_*, the runner constructs H(t)=H_base+tJ_*, proves det(H(t)) is an exact cubic, checks the closed-interval extremum set {0,1,t1}, finds min det(H(t))=0.878309>0 on [0,1], and applies Sylvester inertia continuity to conclude signature(H_base+J_*)=signature(H_base)=(2,0,1).  _(class `A`)_
- **chain closes:** True — The claim is narrowly local and the runner closes exactly that claim. It proves Hermiticity, exact cubic determinant form, atlas A0=32*sqrt(2)/9, p(1)=0.959174, closed-form critical points, positive minimum 0.878309 on the full interval, and direct signatures at H_base and the P3 pin, with PASS=11 FAIL=0. The note explicitly excludes A-BCC, sigma_hier, chamber-wide source selection, and the DM flagship closure, so those are not load-bearing requirements for this local theorem.
- **rationale:** Clean for the narrow local theorem at the stated P3 pin. The determinant positivity certificate is not a sampling argument: the runner constructs the exact symbolic cubic p(t), solves p'(t)=0 as a quadratic, evaluates the finite extremum set on [0,1], and obtains a strictly positive minimum before invoking Sylvester's law. Direct eigenvalue checks independently match the retained signature convention (n_-, n_0, n_+)=(2,0,1) at both endpoints. This clean audit does not promote any wider physical branch-choice statement: A-BCC, sigma_hier=(2,1,0), chamber-wide source selection, and the DM flagship lane remain outside the claim and are not closed here.
- **auditor confidence:** high

### `dm_pmns_graph_first_ordered_chain_nonzero_current_activation_theorem_note_2026-04-21`

- **Note:** [`DM_PMNS_GRAPH_FIRST_ORDERED_CHAIN_NONZERO_CURRENT_ACTIVATION_THEOREM_NOTE_2026-04-21.md`](../../docs/DM_PMNS_GRAPH_FIRST_ORDERED_CHAIN_NONZERO_CURRENT_ACTIVATION_THEOREM_NOTE_2026-04-21.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_conditional~~
- **effective_status:** ~~audited_conditional~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** By the graph-first cycle-frame theorem and adjacent-chain path-algebra theorem, A_ord = diag(1,2,3) + (E12 + E23 + E31) is canonical and produces J_chi(A_ord) = 1 on the retained hw=1 response family.  _(class `B`)_
- **chain closes:** False — The live runner verifies the ordered-chain algebra and nonzero current, but the graph-first frame, adjacent-chain projector system, native current readout, and reduction target are imported from support or unknown one-hop authorities.
- **rationale:** Issue: the runner proves that the supplied ordered-chain law has J_chi = 1 and survives response-column reconstruction, but the canonicality and 'sole-axiom' status of that law rely on imported graph-first cycle-frame, adjacent-chain path-algebra, and native last-mile-reduction notes. Why this blocks: those one-hop inputs are not audit-retained, and the runner's B-style checks partly verify that their notes contain expected strings rather than independently deriving the ordered carrier and current readout. Repair target: audit-clean or inline the graph-first cycle-frame support, adjacent-chain path algebra, native C3 current definition, and last-mile reduction theorem; then rerun this proof as an algebraic corollary over retained inputs. Claim boundary until fixed: given the imported ordered frame and current definition, it is safe to claim A_ord = diag(1,2,3)+C has J_chi = 1 and reconstructs exactly on the hw=1 response family; it is not yet a retained sole-axiom current-activation theorem.
- **open / conditional deps cited:**
  - `PMNS_GRAPH_FIRST_CYCLE_FRAME_SUPPORT_NOTE.md`
  - `DM_WILSON_TO_DWEH_LOCAL_CHAIN_PATH_ALGEBRA_TARGET_NOTE_2026-04-18.md`
  - `DM_PMNS_NATIVE_CURRENT_LAST_MILE_REDUCTION_THEOREM_NOTE_2026-04-21.md`
- **auditor confidence:** high

### `early_family_transfer_connectivity_diagnosis`

- **Note:** [`EARLY_FAMILY_TRANSFER_CONNECTIVITY_DIAGNOSIS.md`](../../docs/EARLY_FAMILY_TRANSFER_CONNECTIVITY_DIAGNOSIS.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_conditional~~
- **effective_status:** ~~audited_conditional~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The origin architecture transfers as a connectivity design prior, not a broad geometry-generic transport law; the surviving comparison is position-based sector matching on a retained grown row.  _(class `B`)_
- **chain closes:** False — The note is a synthesis over prior family/connectivity diagnostics with no runner of its own, and its one-hop support includes unknown, bounded, and unaudited proposed notes.
- **rationale:** Issue: the note promotes a cross-note interpretation of old family architecture as a retained connectivity-design guide, but it does not compute the comparison and its cited support is not audit-clean. Why this blocks: a synthesis cannot be retained while its inputs include unknown and bounded rows, and the causal diagnosis 'position-based sector matching survives' requires either clean upstream artifacts or a direct runner comparing the named architectures. Repair target: audit-clean the fixed-field grown transfer, nonlabel sign transfer, weak/connectivity controls, and generated-geometry synthesis, or add a direct runner that reproduces the table and tests the connectivity-design diagnosis. Claim boundary until fixed: it is safe to present this as a bounded historical synthesis: the listed notes suggest structured sector matching matters and weak rewiring fails; it is not an audited retained transfer-positive theorem.
- **open / conditional deps cited:**
  - `GATE_B_NONLABEL_SIGN_GROWN_TRANSFER_NOTE.md`
  - `FIXED_FIELD_GROWN_TRANSFER_SCOUT_NOTE.md`
  - `GATE_B_NONLABEL_CONNECTIVITY_V1_NOTE.md`
  - `GATE_B_WEAK_CONNECTIVITY_NOTE.md`
  - `GENERATED_GEOMETRY_SYNTHESIS_NOTE.md`
- **auditor confidence:** high

### `electric_sign_law_note`

- **Note:** [`ELECTRIC_SIGN_LAW_NOTE.md`](../../docs/ELECTRIC_SIGN_LAW_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_clean~~
- **effective_status:** **retained**  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** On the fixed 3D ordered dense lattice with h=0.5, W=8, L=12, a sign-flipped scalar phase coupling gives like-charge repulsion, unlike-charge attraction, and no measurable neutral response.  _(class `C`)_
- **chain closes:** True — The live named harness recomputes the fixed finite packet propagation and prints PASS for all six source/test charge cases with centroid shifts of the stated signs. The conclusion closes only for the explicitly sign-flipped scalar phase-law setup and does not derive full electromagnetism.
- **rationale:** The source note's retained statement is bounded to a representability test under an explicitly sign-flipped scalar phase coupling on one fixed ordered-lattice family. The live runner output matches the frozen qualitative replay: like-charge cases have negative centroid shifts, unlike-charge cases have positive centroid shifts, and neutral cases are zero to printed precision. The note's referenced frozen log is absent from this worktree, which should be repaired as an archival artifact, but the live finite computation is enough to close the narrow sign-law claim audited here.
- **auditor confidence:** high

### `electrostatics_card_note`

- **Note:** [`ELECTROSTATICS_CARD_NOTE.md`](../../docs/ELECTROSTATICS_CARD_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_clean~~
- **effective_status:** **retained**  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** On the fixed ordered 3D lattice, the scalar sign-coupled source field produces sign antisymmetry, exact same-node opposite-charge cancellation, dipole orientation sign flip, near-linear charge scaling, and strong symmetric-shell screening attenuation.  _(class `C`)_
- **chain closes:** True — The frozen log is present and the live named runner reproduces the note's numerical surface exactly to the printed precision for all five target observables. The closure is only for the finite scalar electrostatic-like card, with Maxwell, gauge, magnetic, and radiation claims explicitly excluded.
- **rationale:** The source note makes a bounded scalar sign-law claim and keeps the physical scope explicit: it does not assert a vector field, Maxwell equations, magnetic effects, or radiation. The live runner recomputes the stated ordered-lattice card and matches the frozen result: like/unlike signs are antisymmetric, the same-node +1/-1 source cancels to zero, the dipole orientation reverses the response sign, the fitted charge exponent is 1.000, and the screening ratio is 0.018. Residual risk is only the stated finite-probe scope, not a break in the presented chain.
- **auditor confidence:** high

### `electrostatics_grown_sign_law_note`

- **Note:** [`ELECTROSTATICS_GROWN_SIGN_LAW_NOTE.md`](../../docs/ELECTROSTATICS_GROWN_SIGN_LAW_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_conditional~~
- **effective_status:** ~~audited_conditional~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** On the fixed retained grown row drift=0.2, restore=0.7, the tabulated single-source, neutral-pair, like-pair, dipole, and double-charge cases have the expected sign response and a +1 to +2 charge exponent of 1.000.  _(class `C`)_
- **chain closes:** False — The claim is a narrow numerical grown-geometry compute, but the ledger has no registered runner/output and the artifact paths in the note are absolute external paths rather than audit-registered evidence.
- **rationale:** Issue: the retained sign-law companion rests on frozen numerical results for one fixed grown geometry row, but the audit ledger registers no primary runner or output, and the note's artifact links are absolute local paths outside the audit packet. Why this blocks: a hostile auditor cannot reproduce the printed delta_z signs, neutral cancellation, dipole partial cancellation, or +1/+2 linearity threshold from registered evidence; moreover the note explicitly limits the result to fixed-field, no graph update, one source layer, and one final-layer centroid on a single grown row. Repair target: register scripts/ELECTROSTATICS_GROWN_SIGN_LAW.py as the claim runner with deterministic output and explicit PASS thresholds for sign, cancellation, and charge-linearity; either keep the note scoped to the single grown row or add sweeps over grown-geometry parameters, graph update, source layers, and detector definitions. Claim boundary until fixed: it is safe to say the source note reports a conditional fixed-row sign-law transfer check with neutral cancellation and approximate charge linearity; it is not yet an audited retained grown-geometry theorem or geometry-generic electrostatics result.
- **open / conditional deps cited:**
  - `scripts/ELECTROSTATICS_GROWN_SIGN_LAW.py_not_registered_primary_runner`
  - `logs/2026-04-05-electrostatics-grown-sign-law.txt_not_registered_primary_output`
  - `grown_geometry_parameter_sweep_not_performed`
  - `graph_update_case_not_tested`
- **auditor confidence:** high

### `electrostatics_superposition_proxy_note`

- **Note:** [`ELECTROSTATICS_SUPERPOSITION_PROXY_NOTE.md`](../../docs/ELECTROSTATICS_SUPERPOSITION_PROXY_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_clean~~
- **effective_status:** **retained**  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** Using the same sign-coupled ordered-lattice propagator with an explicitly linear multi-source field, same-point opposite charges cancel, like charges reinforce, a dipole gives a reduced signed response, and doubling the source approximately doubles the response.  _(class `C`)_
- **chain closes:** True — The live primary script reproduces the note's five printed replay cases to the shown precision: single +1, same-point +1/-1 null, symmetric +1/+1 reinforcement, +1/-1 dipole partial cancellation, and +2 source scaling. The closure is only for the explicit scalar source-superposition proxy and not for Maxwell, gauge, magnetic, or radiation structure.
- **rationale:** The note's load-bearing claim is a finite compatibility probe, not a derivation of electromagnetism or of linear superposition from deeper retained axioms. Within that scope, the live runner recomputes the stated source combinations and matches the printed replay: exact same-point cancellation, reinforced like-pair shift, reduced signed dipole response, and nearly doubled +2 response. Residual boundary: downstream uses must treat the linear source field and scalar sign-coupled propagator as the tested setup, not as an audited Maxwell theory.
- **auditor confidence:** high

### `emergent_lorentz_invariance_note`

- **Note:** [`EMERGENT_LORENTZ_INVARIANCE_NOTE.md`](../../docs/EMERGENT_LORENTZ_INVARIANCE_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_conditional~~
- **effective_status:** ~~audited_conditional~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** On the retained hierarchy surface a ~ 1/M_Planck, the dimension-6 cubic-lattice correction is suppressed by (E/M_Planck)^2, so Lorentz invariance is emergent to all currently accessible precision.  _(class `B`)_
- **chain closes:** False — The runner verifies the staggered/bosonic dispersion expansion and cubic-harmonic angular structure, but the broad emergent-observable conclusion relies on CPT exactness, parity protection, and a ~ 1/M_Planck as imported bridges. Those bridges are not registered as one-hop dependencies for this claim and are asserted in the runner rather than derived or read from audited inputs.
- **rationale:** Issue: the source note's structural dispersion and cubic-harmonic checks are reproduced by the registered runner, but the retained conclusion that Lorentz invariance holds to all accessible precision depends on unregistered bridge premises: exact CPT, exact/tree-level parity protection against odd-dimension LV, and the hierarchy-scale identification a ~ 1/M_Planck. Why this blocks: without ledger one-hop dependencies and a runner that constructs or verifies those bridges, a hostile auditor cannot distinguish a theorem from a calculation performed on an assumed symmetry/scale surface; the runner's CPT, P, and hierarchy checks are hard-coded assertions downstream of the contested inputs. Repair target: register the CPT_EXACT_NOTE, a parity/operator-basis theorem forbidding dimension-5 LV on the relevant action surface, and the hierarchy theorem fixing the physical lattice spacing as dependencies, then update the runner to read/verify those inputs and fail if any bridge is absent or conditional. Claim boundary until fixed: it is safe to claim the conditional lattice result that the implemented Z^3 staggered and Laplacian dispersions have leading O(a^2 p^4) cubic-harmonic anisotropy and exact cubic isotropy at leading order; the Planck-suppressed observable-Lorentz-invariance theorem remains conditional on the unregistered symmetry and scale bridges.
- **open / conditional deps cited:**
  - `CPT_EXACT_NOTE.md_not_registered_one_hop_dependency`
  - `parity_operator_basis_dimension5_LV_no_go_theorem_not_registered`
  - `hierarchy_scale_a_equals_planck_length_theorem_not_registered`
- **auditor confidence:** high

### `equivalence_principle_harness_note`

- **Note:** [`EQUIVALENCE_PRINCIPLE_HARNESS_NOTE.md`](../../docs/EQUIVALENCE_PRINCIPLE_HARNESS_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_clean~~
- **effective_status:** **retained**  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** On the fixed ordered 3D family, global amplitude rescaling leaves the detector centroid shift invariant for both valley-linear and spent-delay actions, while normalized packet shape changes the response strongly.  _(class `C`)_
- **chain closes:** True — The live named harness reproduces the note's amplitude-invariance values and packet-shape relative spreads for both actions to the printed precision. The chain closes only for the test-particle amplitude-level statement and the explicit negative boundary that shape/composition dependence remains.
- **rationale:** The note is careful not to claim a full equivalence principle or persistent-pattern inertial-mass law. The live runner supports the bounded result: both actions are invariant under global amplitude scaling to machine precision, and both actions show large packet-shape spreads of about 159.21% and 155.21%. The referenced frozen log is absent from this worktree, but the live finite computation closes the narrow claim and the note itself preserves the open persistent-pattern boundary.
- **auditor confidence:** high

### `evolving_network_prototype_v2_note`

- **Note:** [`EVOLVING_NETWORK_PROTOTYPE_V2_NOTE.md`](../../docs/EVOLVING_NETWORK_PROTOTYPE_V2_NOTE.md)
- **current_status:** _proposed_promoted_
- **audit_status:** ~~audited_failed~~
- **effective_status:** ~~audited_failed~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The note's actual load-bearing result is that self-regulating pruning produces a measurable generated gap signal, but it does not converge to a fixed point and does not close a generated-vs-imposed Gate B dynamics theorem.  _(class `C`)_
- **chain closes:** False — The frozen log and live runner reproduce generated gaps of about 0.88 to 4.09, but every tested row has conv = 0.00 and the same-budget imposed control has nan detector purity, so the promoted dynamics claim does not close. The source status also explicitly says this is a bounded prototype note, not a proposed_promoted dynamics theorem.
- **rationale:** Issue: the queue's proposed_promoted status contradicts the source note and runner output; the note says this is not a promoted dynamics theorem, and the runner shows no convergence plus an undefined imposed-control purity comparator. Why this blocks: a hostile referee cannot promote Gate B dynamics from a rule that hits the removal cap, lacks a stable fixed point, and cannot produce the promised generated-vs-imposed purity comparison. Repair target: produce a deterministic runner/theorem where the local rule converges under stated thresholds, the same-budget imposed control has defined detector signal, and the promoted criterion is asserted across seeds and layer sizes; also resolve the script's band-vs-random wording mismatch for the imposed control. Claim boundary until fixed: it is safe to claim a bounded negative/prototype result in which local pruning creates a measurable post-barrier gap distinct from baseline, but not a closed Gate B dynamics solution or proposed_promoted theorem.
- **open / conditional deps cited:**
  - `promoted_dynamics_theorem_denied_by_source_note`
  - `fixed_point_convergence_not_observed`
  - `same_budget_imposed_control_detector_purity_nan`
- **auditor confidence:** high

### `evolving_network_prototype_v3_note`

- **Note:** [`EVOLVING_NETWORK_PROTOTYPE_V3_NOTE.md`](../../docs/EVOLVING_NETWORK_PROTOTYPE_V3_NOTE.md)
- **current_status:** _proposed_promoted_
- **audit_status:** ~~audited_failed~~
- **effective_status:** ~~audited_failed~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The v3 note shows a fairer backbone-preserving imposed control with spine_ok = 1.00, but the imposed detector purity remains nan and the Gate B generated-vs-imposed dynamics comparison remains negative or inconclusive.  _(class `C`)_
- **chain closes:** False — The frozen log and live runner reproduce the methodological improvement, including finite imposed gaps and spine_ok = 1.00, but every row still has conv = 0.00 and imposed_pur = nan. The source status explicitly says this is a public control audit, not a proposed_promoted dynamics result.
- **rationale:** Issue: the queued proposed_promoted status is contradicted by the source note and by the v3 runner; the control is cleaner, but the detector-side purity comparison is still undefined and the self-regulating rule still does not converge. Why this blocks: a promoted Gate B dynamics result requires a measurable generated-vs-imposed comparator and stable rule behavior, while this packet only shows that the imposed control preserves a backbone corridor before losing finite detector purity. Repair target: produce a runner/theorem with finite imposed_pur, explicit generated-vs-imposed pass thresholds, convergence or a justified non-convergence criterion, and seed/layer robustness under the same-budget control. Claim boundary until fixed: it is safe to claim v3 improves the control discipline and preserves a source-to-detector backbone while generated pruning produces finite gap signals; it is not safe to claim Gate B is solved or that v3 is a proposed_promoted dynamics result.
- **open / conditional deps cited:**
  - `promoted_dynamics_result_denied_by_source_note`
  - `imposed_detector_purity_nan`
  - `fixed_point_convergence_not_observed`
  - `generated_vs_imposed_positive_comparator_not_established`
- **auditor confidence:** high

### `ew_coupling_derivation_note`

- **Note:** [`EW_COUPLING_DERIVATION_NOTE.md`](../../docs/EW_COUPLING_DERIVATION_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_numerical_match~~
- **effective_status:** ~~audited_numerical_match~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The registered runner closes the weak-angle gap only by scanning an effective taste_weight and choosing about 0.390 to match observed sin^2(theta_W), while the source note is superseded and leaves g_2(v) and lambda(v) bounded rather than derived.  _(class `G`)_
- **chain closes:** False — The live runner reproduces its own near-match to sin^2(theta_W), but it does so after a target scan over taste_weight and states that taste_weight = 0.390 still requires a physical derivation. The source note itself is superseded, has stale coupling numbers relative to the runner, and explicitly says g_2(v) and lambda(v) are not derived.
- **rationale:** Issue: the proposed_retained EW-coupling derivation is not a closed derivation from retained inputs; the runner selects a fitted taste_weight against the observed weak angle, and the note says the packet is superseded support work with g_2 and lambda still bounded/open. Why this blocks: a hostile referee cannot treat a scanned value, a 12.22% miss in 1/alpha_EM, and open SU(2)/Higgs matching as a retained derivation of g_1(v), g_2(v), or lambda(v). Repair target: derive the taste-gauge coupling/taste_weight from registered lattice representation theory or Monte Carlo, register the superseding complete-chain note as the governing one-hop authority, and update the runner so it predicts sin^2(theta_W), g_1, g_2, and lambda without fitting to the target. Claim boundary until fixed: it is safe to claim a support scan showing that bare geometric couplings plus a tuned taste-threshold parameter can numerically match sin^2(theta_W) and that EW imports remain important; it is not safe to claim a retained EW-coupling derivation.
- **open / conditional deps cited:**
  - `COMPLETE_PREDICTION_CHAIN_2026_04_15.md_superseding_authority_not_registered`
  - `taste_weight_physical_derivation_missing`
  - `su2_nonperturbative_matching_open`
  - `higgs_lambda_from_g5_condensate_open`
  - `source_note_stale_relative_to_registered_runner`
- **auditor confidence:** high

### `family_companion_compare_note`

- **Note:** [`FAMILY_COMPANION_COMPARE_NOTE.md`](../../docs/FAMILY_COMPANION_COMPARE_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_conditional~~
- **effective_status:** ~~audited_conditional~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The note infers a shared fixed-companion weak-field law across the grown transfer basin, the alternative connectivity basin, and the second grown-family complex anchor, while isolating that the second-family branch uses a gamma=0/crossover control surface rather than the same zero/neutral signed-source surface.  _(class `B`)_
- **chain closes:** False — The live script reproduces the comparison table, but it is a hard-coded renderer and does not verify the three source families from registered one-hop runner outputs. Two cited source notes remain unaudited proposed_retained in the ledger, and the second-family row is explicitly on a different control surface.
- **rationale:** Issue: the retained cross-family comparison rests on a static summary of source notes, not on an audit-registered dependency chain or a runner that recomputes the controls and F~M values. Why this blocks: a hostile referee cannot accept a retained shared-law claim while two cited families are still unaudited proposed_retained and the second-family complex branch is compared by gamma=0/crossover rather than the same zero/neutral signed-source observable. Repair target: audit/register the grown-transfer and second-family source notes as one-hop dependencies, add the fixed-field/FM-transfer/sign companion notes named by the renderer, and replace the static comparison script with thresholded checks that ingest or recompute each row's controls and weak-field linearity. Claim boundary until fixed: it is safe to use this as a conditional comparison map saying the named accepted source notes report weak-field linearity and an isolated control-surface mismatch; it is not yet an audited retained cross-family law.
- **open / conditional deps cited:**
  - `GROWN_TRANSFER_BASIN_NOTE.md_unaudited_source`
  - `SECOND_GROWN_FAMILY_COMPLEX_NOTE.md_unaudited_source`
  - `FIXED_FIELD_GROWN_TRANSFER_SCOUT_NOTE.md_not_registered_one_hop`
  - `ALT_CONNECTIVITY_FAMILY_FM_TRANSFER_NOTE.md_not_registered_one_hop`
  - `SECOND_GROWN_FAMILY_SIGN_NOTE.md_not_registered_one_hop`
  - `logs/2026-04-06-family-companion-compare.txt_missing_frozen_output`
  - `control_surface_mismatch_for_second_family_complex`
- **auditor confidence:** high

### `fifth_family_complex_note`

- **Note:** [`FIFTH_FAMILY_COMPLEX_NOTE.md`](../../docs/FIFTH_FAMILY_COMPLEX_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_failed~~
- **effective_status:** ~~audited_failed~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The note claims that the radial-shell fifth-family anchor row at drift 0.20, seed 0 carries a narrow complex-action companion with Born proxy 0, TOWARD-to-AWAY crossover, and weak-field F~M = 1.000 at gamma = 0 and gamma = 0.5.  _(class `C`)_
- **chain closes:** False — The frozen log reports one passing anchor row, but the live targeted script fails before running because it imports _field_from_sources from CONNECTIVITY_FAMILY_V2_QUADRANT_SWEEP.py and that symbol is absent in the current repo. The cited radial-shell base note is also unaudited, so the current audit packet cannot reproduce the retained anchor-row claim.
- **rationale:** Issue: the live runner for the retained fifth-family complex companion is broken by an import mismatch, so the claimed anchor-row positive cannot be reproduced from the current source. Why this blocks: a hostile referee cannot accept a retained finite-computation claim from a stale frozen log when the present runner exits before computing Born, crossover, or F~M, and the upstream radial-shell family note has not itself been audited. Repair target: update FIFTH_FAMILY_COMPLEX_TARGETED.py to the current connectivity helper API or restore the missing _field_from_sources helper, rerun the anchor-row computation with explicit PASS thresholds for Born, crossover, and F~M, and audit/register FIFTH_FAMILY_RADIAL_NOTE.md as the base family dependency. Claim boundary until fixed: it is safe only to say a historical frozen log reported one drift=0.20, seed=0 complex companion candidate; it is not currently an audited retained anchor-row positive.
- **open / conditional deps cited:**
  - `scripts/FIFTH_FAMILY_COMPLEX_TARGETED.py_import_error_missing__field_from_sources`
  - `FIFTH_FAMILY_RADIAL_NOTE.md_unaudited_base_family`
  - `live_runner_output_not_reproducible`
- **auditor confidence:** high

### `fifth_family_radial_fm_transfer_note`

- **Note:** [`FIFTH_FAMILY_RADIAL_FM_TRANSFER_NOTE.md`](../../docs/FIFTH_FAMILY_RADIAL_FM_TRANSFER_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_failed~~
- **effective_status:** ~~audited_failed~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The note claims weak-field F~M transfer on two sampled radial-shell fifth-family rows: drift 0.05 seed 0 with F~M = 0.999040 and drift 0.30 seed 1 with F~M = 0.999839.  _(class `C`)_
- **chain closes:** False — The frozen log reports 2/2 passing rows, but the live script fails before running because CONNECTIVITY_FAMILY_V2_QUADRANT_SWEEP.py no longer exports _build_radial_shell_connectivity. The cited radial-shell base note is unaudited, so the current source packet cannot reproduce the proposed_retained F~M transfer.
- **rationale:** Issue: the current runner for the fifth-family radial F~M transfer is broken by an import/API mismatch, so the sampled weak-field rows cannot be recomputed from the live repo. Why this blocks: a retained finite-computation claim cannot rest only on a stale frozen log when the present script exits before calculating either F~M value, especially with the base radial-family note still unaudited. Repair target: restore or relocate _build_radial_shell_connectivity, _field_from_sources, _centroid_z, and _propagate under the imported API or update this runner to its current helper module, then rerun with explicit PASS thresholds and audit/register FIFTH_FAMILY_RADIAL_NOTE.md as the base family dependency. Claim boundary until fixed: it is safe to say the historical log reported two sampled rows with near-unit F~M; it is not currently an audited retained weak-field transfer.
- **open / conditional deps cited:**
  - `scripts/FIFTH_FAMILY_RADIAL_FM_TRANSFER.py_import_error_missing__build_radial_shell_connectivity`
  - `FIFTH_FAMILY_RADIAL_NOTE.md_unaudited_base_family`
  - `live_runner_output_not_reproducible`
- **auditor confidence:** high

### `fifth_family_radial_note`

- **Note:** [`FIFTH_FAMILY_RADIAL_NOTE.md`](../../docs/FIFTH_FAMILY_RADIAL_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_failed~~
- **effective_status:** ~~audited_failed~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The note claims a narrow radial-shell fifth-family basin on sampled no-restore grown rows, with drift 0.05 seed 0 and drift 0.30 seed 1 passing exact zero-source, neutral cancellation, sign orientation, and near-unit F~M while drift 0.20 seed 0 is a sign-orientation boundary.  _(class `C`)_
- **chain closes:** False — The frozen logs report the stated narrow-basin pattern, but all three live artifact scripts fail before computing because CONNECTIVITY_FAMILY_V2_QUADRANT_SWEEP.py no longer exports _build_radial_shell_connectivity. The current repo therefore cannot reproduce the proposed_retained base-family claim.
- **rationale:** Issue: the current radial-shell fifth-family artifact chain is broken by a shared helper import mismatch across the sweep, basin, and F~M transfer scripts. Why this blocks: a retained finite basin cannot be audited from stale frozen logs when the present scripts exit before checking zero-source control, neutral cancellation, sign orientation, or F~M, and downstream companion notes already fail for the same reason. Repair target: restore or move the radial-shell helper API used by these scripts, or update the scripts to import the current implementation, then rerun the sweep, basin, and F~M transfer with explicit PASS thresholds for the two retained rows and the boundary row. Claim boundary until fixed: it is safe only to say historical logs reported a narrow sampled radial-shell basin; it is not currently an audited retained fifth structured family.
- **open / conditional deps cited:**
  - `scripts/FIFTH_FAMILY_RADIAL_SWEEP.py_import_error_missing__build_radial_shell_connectivity`
  - `scripts/FIFTH_FAMILY_RADIAL_BASIN.py_import_error_missing__build_radial_shell_connectivity`
  - `scripts/FIFTH_FAMILY_RADIAL_FM_TRANSFER.py_import_error_missing__build_radial_shell_connectivity`
  - `live_runner_output_not_reproducible`
- **auditor confidence:** high

### `fine_h_family_universality_note`

- **Note:** [`FINE_H_FAMILY_UNIVERSALITY_NOTE.md`](../../docs/FINE_H_FAMILY_UNIVERSALITY_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_conditional~~
- **effective_status:** ~~audited_conditional~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The note claims bounded three-family portability of the H=0.25 lensing slope, with all 15 seed fits in the -1.38 to -1.43 band, all R^2 > 0.997, and a borderline Fam2-vs-Fam3 family-mean offset at t = 2.37.  _(class `C`)_
- **chain closes:** False — The source note gives a detailed finite-sweep table, but the cited raw log is missing from the worktree and the only listed runner is a slow per-family/seed batch tool rather than an aggregate replay of the 15-seed statistics. A live audit run did not complete even the first family/seed within the audit window, so the current packet does not provide reproducible runner output for the table or the t-tests.
- **rationale:** Issue: the proposed_retained portability claim rests on a finite numerical sweep whose raw output is not present and whose listed runner does not provide a practical aggregate replay of the reported slopes, R^2 values, gap statistics, and family-mean significance tests. Why this blocks: a hostile referee cannot verify the 15 per-seed slopes, the grand sigma = 0.036, or the Fam2/Fam3 t = 2.37 result from source text alone, and the note title still says universality even though the note correctly narrows the claim to three-family portability. Repair target: add the missing raw log or a deterministic aggregate runner that executes/caches all 15 family/seed cases, computes the slopes, R^2 values, eikonal gaps, population/sample statistics, and t-tests, and emits explicit PASS thresholds for the bounded portability claim. Claim boundary until fixed: it is safe to say the source note reports a bounded H=0.25 three-family portability table and explicitly disclaims universality/kernel-independence; it is not yet an audited retained portability result.
- **open / conditional deps cited:**
  - `logs/2026-04-09-lensing-fine-h-families.txt_missing_raw_output`
  - `aggregate_15_seed_replay_runner_missing`
  - `live_runner_output_not_completed_in_audit_window`
  - `title_uses_universality_while_claim_disclaims_universality`
- **auditor confidence:** medium

### `fixed_field_complex_grown_basin_v2_note`

- **Note:** [`FIXED_FIELD_COMPLEX_GROWN_BASIN_V2_NOTE.md`](../../docs/FIXED_FIELD_COMPLEX_GROWN_BASIN_V2_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_clean~~
- **effective_status:** **retained**  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The note claims that the retained grown-row complex-action anchor at drift 0.20 restore 0.70 and one nearby row at drift 0.20 restore 0.60 preserve the tiny-basin package: center Born proxy, center and neighbor weak-field F~M near 1, and TOWARD-to-AWAY crossover.  _(class `C`)_
- **chain closes:** True — The live V2 runner reproduces the frozen two-row table, with center Born proxy 1.456e-15, F~M = 1.000 on both rows at gamma=0 and gamma=0.5, and t01=1/t05=0 crossover on both rows. The cited grown companion parent is already audited clean, and the conclusion is restricted to the center row plus one immediate neighbor.
- **rationale:** The claim is intentionally tiny and the live runner recomputes the disputed finite surface rather than only rendering a static table. It confirms the center-row Born proxy, center and nearby weak-field F~M gates, and nearby crossover survival, while the source note explicitly excludes family-wide or geometry-generic transfer. Residual boundary: the result is a two-row basin around the audited grown-row companion, not a broad grown-family theorem.
- **auditor confidence:** high

### `fixed_field_family_unification_note`

- **Note:** [`FIXED_FIELD_FAMILY_UNIFICATION_NOTE.md`](../../docs/FIXED_FIELD_FAMILY_UNIFICATION_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_clean~~
- **effective_status:** **retained**  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** On the same retained grown row at drift 0.2 restore 0.7 seed 0, the runner checks both the signed-source branch with exact zero/neutral controls and near-linear charge response, and the complex-action branch with the gamma=0 baseline plus absorptive gamma=0.2 and gamma=0.5 responses.  _(class `C`)_
- **chain closes:** True — The live runner reproduces the frozen row: zero and neutral sign-source controls are exactly 0, plus/minus signs are opposite, the charge exponent is 0.999833, and the complex branch gives the stated gamma=0 baseline, negative gamma=0.2/gamma=0.5 deltas, and escape values. The conclusion is restricted to the single retained grown row and does not claim geometry-generic or continuum unification.
- **rationale:** The artifact is a direct same-row computation rather than a static synthesis: it recomputes the sign-law controls and the complex-action responses under the same grown-row parameters. The source note keeps the claim compact and explicitly excludes geometry-generic and continuum extensions, so the chain closes at that finite comparison surface. Residual boundary: the cited sign-transfer companion note is not itself audited retained in the ledger, but this row's load-bearing sign-law quantities are recomputed directly here rather than imported.
- **auditor confidence:** high

### `fixed_field_grown_transfer_scout_note`

- **Note:** [`FIXED_FIELD_GROWN_TRANSFER_SCOUT_NOTE.md`](../../docs/FIXED_FIELD_GROWN_TRANSFER_SCOUT_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_clean~~
- **effective_status:** **retained**  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** the retained grown row preserves the scalar sign response in the fixed-field scout; zero-source and neutral same-point controls reduce to printed zero; the single-source response is approximately linear in source charge  _(class `C`)_
- **chain closes:** True — The live runner recomputes the finite grown-row signed-source table, exact zero/neutral controls, and charge-linearity exponent from the specified row rather than importing the table. The source note explicitly limits the claim to drift=0.2, restore=0.7 fixed-field propagation and excludes geometry-generic or Maxwell-level claims.
- **rationale:** The load-bearing claim is a bounded finite computation: on the specified grown row, the runner reproduces zero-source and neutral cancellation, opposite signs for +1 and -1 sources, like/dipole controls, and near-linear +1 to +2 scaling. The companion grown-geometry control values are consistent with the one-hop companion note already audited clean, while the present source note does not use them to derive a geometry-generic theorem. Residual boundary: the source cites a stale companion replay log filename, but the signed-source claim itself closes through the current scout runner and the available companion artifact.
- **auditor confidence:** high

### `fm_transfer_note`

- **Note:** [`FM_TRANSFER_NOTE.md`](../../docs/FM_TRANSFER_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_clean~~
- **effective_status:** **retained**  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** Mass-law transfer agrees within uncertainty on the retained grown-row neighborhood (drift=0.2, restore=0.7).  _(class `C`)_
- **chain closes:** True — The live runner recomputes the fixed-lattice F~M exponent, six grown-seed F~M exponents at drift=0.2 and restore=0.7, their mean/spread, and the fixed-grown sigma comparison. The note explicitly excludes geometry-generic transfer, other drift/restore values, and other observables.
- **rationale:** The claim is a bounded numerical computation, not a broad universality theorem: the current runner reproduces the frozen fixed exponent, all six grown-seed exponents, the grown aggregate, and the 0.3 sigma fixed-grown comparison. The source note keeps the conclusion on the specified grown row and explicitly does not claim other geometries, drift/restore values, or observables. Residual boundary: the quoted uncertainty is the finite six-seed grown spread used by the runner, so the retained content is only this finite transfer check.
- **auditor confidence:** high

### `four_d_distance_width_probe_note`

- **Note:** [`FOUR_D_DISTANCE_WIDTH_PROBE_NOTE.md`](../../docs/FOUR_D_DISTANCE_WIDTH_PROBE_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_conditional~~
- **effective_status:** ~~audited_conditional~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** TOWARD survives across the tested widths, but the measured exponent still moves enough that the law is not yet width-stable and the width ladder is too small to close the asymptotic law.  _(class `C`)_
- **chain closes:** False — The live runner reproduces the finite W=5..7 TOWARD counts and width-sensitive tail fits, and the frozen W=8 companion log is supportive. The row does not close a proposed-retained 4D family or asymptotic distance law because the evidence is explicitly width-limited and the dimensional-table relation is unaudited/unknown.
- **rationale:** Issue: the source note is queued as proposed_retained, but its own load-bearing result is a bounded width-limited support chain, with W=5..7 reproduced live, W=8 present only as a frozen companion log, and the dimensional-table relation still unaudited/unknown. Why this blocks: the finite probe supports attraction in the tested window, but it cannot ratify a retained 4D valley-linear family or any asymptotic distance-law closure. Repair target: either change the source status to a bounded/support claim, or provide a registered current runner covering the heavier width ladder plus an audited dimensional-table/family theorem and a convergence criterion for width-stable tail behavior. Claim boundary until fixed: the safe claim is that W=5..7 live and W=8 frozen evidence are TOWARD on the tested window, while the 4D tail remains width-sensitive and not Newtonian/asymptotically closed.
- **open / conditional deps cited:**
  - `DIMENSIONAL_GRAVITY_TABLE.md_unknown_or_unaudited`
  - `logs/2026-04-04-4d-wide-distance-law.txt_frozen_companion_without_registered_current_runner`
- **auditor confidence:** high

### `fourth_family_quadrant_note`

- **Note:** [`FOURTH_FAMILY_QUADRANT_NOTE.md`](../../docs/FOURTH_FAMILY_QUADRANT_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_clean~~
- **effective_status:** **retained**  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The quick diagnostic sweep gives a real but narrow basin: exact zero and neutral controls pass, sign orientation is correct on the passing rows, weak charge scaling stays near linear, and 5/9 tested rows pass.  _(class `C`)_
- **chain closes:** True — The live --quick runner recomputes the nine-row quadrant-reflection sweep and reproduces the frozen 5/9 passing basin with exact zero/neutral controls and near-linear charge scaling. The source note explicitly excludes family-wide, seed-universal, and geometry-generic claims.
- **rationale:** The claim is narrow enough to close: the runner constructs the quadrant-reflection connectivity rule, evaluates the declared drift/seed grid, and reproduces the finite signed-source basin rather than importing it. The exact zero-source and neutral-cancellation controls hold on all evaluated rows, while the sign gate restricts retention to the printed 5/9 narrow basin. Residual boundary: distinctness is algorithmic for this connectivity construction, not evidence for a geometry-generic or seed-universal family law.
- **auditor confidence:** high

### `framework_bare_alpha_3_alpha_em_dimension_fixed_ratio_support_note_2026-04-25`

- **Note:** [`FRAMEWORK_BARE_ALPHA_3_ALPHA_EM_DIMENSION_FIXED_RATIO_SUPPORT_NOTE_2026-04-25.md`](../../docs/FRAMEWORK_BARE_ALPHA_3_ALPHA_EM_DIMENSION_FIXED_RATIO_SUPPORT_NOTE_2026-04-25.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_failed~~
- **effective_status:** ~~audited_failed~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The support corollary claims that the retained EW-normalization authority surface plus the Cl(3)->SM support-count bookkeeping authorize the exact bare identity alpha_3(bare)/alpha_em(bare)=2d+3, hence 9 at d=3, as a package-consistency support result rather than a direct low-energy observable.  _(class `A`)_
- **chain closes:** False — The primary verifier named by the note returns nonzero: PASS=46, FAIL=1. The exact algebraic checks pass, including g2^2=1/4, gY^2=1/5, g_em^2=1/9, sin^2(theta_W)=4/9, alpha_3/alpha_em=9, alpha_em=1/(36*pi), and the SU(5) offset 5/72. The failing check is the authority-surface gate `EW normalization retained lane exists`, so the runner does not validate the note's required retained-EW-lane premise. The queue also has runner_path=null and no registered one-hop dependencies for the EW normalization lane or Cl(3)->SM support packet.
- **rationale:** The claim fails as a proposed_retained support corollary because its own primary verifier rejects the authority boundary. The algebraic identity is trivial and correct once the inputs g3^2=1, g2^2=1/(d+1), gY^2=1/(d+2), and d=3 are assumed: the bare electromagnetic inverse sum is 2d+3=9 and therefore alpha_3/alpha_em=9. But the note's load-bearing scientific claim is stronger than arithmetic; it asserts this identity is a support corollary on the retained EW-normalization surface while not promoting the Cl(3)->SM support packet. The verifier's failed `EW normalization retained lane exists` check means that required package authority was not established under the note's own audit gate. To repair the claim, either update/register the retained EW-normalization authority so the verifier can find the intended status and bare-coupling bookkeeping, or narrow the note to a pure conditional algebra lemma with explicit assumptions and no proposed_retained package-surface authority. Also register the primary verifier in the audit queue and add one-hop dependencies for the EW normalization lane and Cl(3)->SM support packet. What can still be safely claimed is: if the bare bookkeeping inputs are assumed, then alpha_3(bare)/alpha_em(bare)=2d+3 and equals 9 at d=3, and the bare sin^2(theta_W)=4/9 differs from SU(5)'s 3/8 by 5/72. The audit does not support retained package authority, direct low-energy alpha_3/alpha_em phenomenology, or minimal-stack promotion.
- **open / conditional deps cited:**
  - `primary_verifier_fails_EW_normalization_retained_lane_exists`
  - `YT_EW_COLOR_PROJECTION_THEOREM.md_retained_EW_normalization_authority_not_verified_by_runner`
  - `CL3_SM_EMBEDDING_THEOREM.md_support_only_not_accepted_minimal_input_stack`
  - `audit_queue_runner_path_null_for_named_primary_verifier`
  - `retained_EW_bare_coupling_bookkeeping_not_registered_one_hop_dependency`
  - `Cl3_to_SM_dimension_count_d_plus_1_d_plus_2_support_packet_not_registered_one_hop_dependency`
- **auditor confidence:** high

### `gate_b_complex_action_falsifier_note`

- **Note:** [`GATE_B_COMPLEX_ACTION_FALSIFIER_NOTE.md`](../../docs/GATE_B_COMPLEX_ACTION_FALSIFIER_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_conditional~~
- **effective_status:** ~~audited_conditional~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** gamma = 0 reproduces the retained Gate B row exactly, while increasing gamma suppresses detector escape sharply on the same row.  _(class `C`)_
- **chain closes:** False — The live runner reproduces the finite gamma sweep and detector-escape suppression on drift=0.2, restore=0.7. Retained closure does not propagate because the note inherits the retained-row/Born guardrail from an unaudited bounded Gate B joint-package note and itself states this is only a tiny bounded falsification probe.
- **rationale:** Issue: the runner verifies a finite detector-effect sweep, but the proposed_retained queue status is stronger than the source note's own bounded-falsifier scope, and the retained Gate B/Born guardrail is imported from docs/GATE_B_GROWN_JOINT_PACKAGE_NOTE.md, which is bounded and unaudited. Why this blocks: the audit can retain the local fact that gamma attenuates detector escape on this row, but it cannot ratify a retained complex-action branch or inherited retained-row guardrail through a bounded unaudited dependency. Repair target: either re-scope the note as bounded/support, or add a registered current runner and audited Gate B row/Born dependency that closes gamma=0, Born, and retained-row status on the same surface. Claim boundary until fixed: on the specified drift=0.2, restore=0.7 row, the live runner shows escape suppression from 0.215 at gamma=0.05 to effectively zero at gamma=0.5, with AWAY centroid shifts; no broader generated-geometry complex-action theory is established.
- **open / conditional deps cited:**
  - `GATE_B_GROWN_JOINT_PACKAGE_NOTE.md_bounded_unaudited_guardrail`
- **auditor confidence:** high

### `gate_b_grown_distance_law_note`

- **Note:** [`GATE_B_GROWN_DISTANCE_LAW_NOTE.md`](../../docs/GATE_B_GROWN_DISTANCE_LAW_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_conditional~~
- **effective_status:** ~~audited_conditional~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** the distance-law tail transfers from the exact grid to the retained moderate-drift grown geometry on this tested family, with both rows 20/20 TOWARD and comparable declining far-field tails  _(class `C`)_
- **chain closes:** False — The live runner closes the finite exact-vs-grown distance-tail replay on the declared h=0.5, z=3..7 surface. Retained closure does not propagate because the source note is explicitly a bounded companion and its Gate B far-field/dynamics context is bounded or unknown in the audit ledger.
- **rationale:** Issue: the live harness verifies the finite distance-tail replay, but the note is queued as proposed_retained while its own status and safe read describe a bounded companion, and the direct Gate B context is not audit-retained. Why this blocks: the finite comparison can support a bounded transfer statement, but cannot ratify the retained grown-geometry family or a broader Gate B closure through bounded/unknown one-hop context. Repair target: either re-scope this source as bounded/support, or audit-retain the far-field sign/F~M and Gate B grown-family dependencies and add a closure theorem for the generated-geometry parameter space. Claim boundary until fixed: on the declared h=0.5 exact-vs-grown replay, both rows are 20/20 TOWARD with comparable post-peak declining tails, exact grid b^(-0.90) and grown drift=0.2 b^(-0.83); exact Newtonian equality and full Gate B closure are not established.
- **open / conditional deps cited:**
  - `GATE_B_FARFIELD_NOTE.md_bounded_unaudited`
  - `GATE_B_DYNAMICS_NOTE.md_unknown_unaudited`
- **auditor confidence:** high

### `gate_b_grown_propagating_field_note`

- **Note:** [`GATE_B_GROWN_PROPAGATING_FIELD_NOTE.md`](../../docs/GATE_B_GROWN_PROPAGATING_FIELD_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_clean~~
- **effective_status:** **retained**  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** finite gamma does not produce a coherent detector-line phase ramp on this retained grown row, the escape ratio stays at 1.000 to three decimals, and only a tiny centroid shift survives.  _(class `C`)_
- **chain closes:** True — The live runner recomputes the gamma=0 reduction and the full gamma sweep on the declared drift=0.2, restore=0.7 row. The negative result closes because the note only claims a bounded no-go for this minimal retarded-like field state and explicitly excludes broader field-theory, transfer, horizon, or trapping claims.
- **rationale:** The runner directly checks the load-bearing failure mode: gamma=0 has zero field and amplitude error relative to the static baseline, while nonzero gamma leaves escape at 1.000 to three decimals and produces no coherent detector-line phase ramp. The source note scopes the result as a bounded no-go for one minimal causal-memory update, so it does not overclaim a generated-family transfer or self-consistent propagating field theory. Residual boundary: this clean verdict retains only the negative result for this particular retarded-like field ansatz on the specified grown row.
- **auditor confidence:** high

### `gate_b_grown_propagating_field_v2_note`

- **Note:** [`GATE_B_GROWN_PROPAGATING_FIELD_V2_NOTE.md`](../../docs/GATE_B_GROWN_PROPAGATING_FIELD_V2_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_clean~~
- **effective_status:** **retained**  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** the stronger transport-envelope architecture does not produce a meaningful escape signal or detector-line phase ramp on the retained grown row; only a tiny centroid shift survives.  _(class `C`)_
- **chain closes:** True — The live runner recomputes the exact gamma=0 reduction, four nonzero-gamma escape/phase rows, and F~M sanity checks on the declared moderate-drift grown row. The source note scopes the result as a bounded no-go for this specific stronger architecture and excludes generated-family transfer, horizon, trapping, or full field-theory claims.
- **rationale:** The no-go closes on its own terms: gamma=0 exactly reduces to the static grown baseline, nonzero gamma leaves escape at 1.000 down to 0.999, detector-line phase slope/span remain tiny, and F~M stays 1.000 at gamma=0 and gamma=0.5. The source does not use this as positive evidence for a causal-field theory; it explicitly records failure of the intended causal-observable bar. Residual boundary: the retained content is only this negative result for the tested transport-envelope ansatz on the specified grown row.
- **auditor confidence:** high

### `gate_b_grown_propagating_field_v3_note`

- **Note:** [`GATE_B_GROWN_PROPAGATING_FIELD_V3_NOTE.md`](../../docs/GATE_B_GROWN_PROPAGATING_FIELD_V3_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_clean~~
- **effective_status:** **retained**  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** the exact matched-null reduction is real, but the frontier-echo feedback does not produce a meaningful causal observable beyond a tiny transport modulation.  _(class `C`)_
- **chain closes:** True — The live runner recomputes the chi=0 matched-null reduction, five nonzero-chi matched escape/shell/phase rows, residuals, and weak-field sanity check on the declared grown row. The source note scopes the result as a bounded no-go for this frontier-echo architecture and does not claim a general propagating-field sector.
- **rationale:** The no-go closes on its own terms: chi=0 exactly reproduces the matched trap/control baseline, all matched shifts vanish at chi=0, nonzero chi produces only tiny matched shell and phase shifts, and F~M at chi=0.5 is essentially flat rather than a useful mass-scaling signal. The source explicitly treats this as a bounded failure of the frontier-echo architecture, not as a retained causal-field theory. Residual boundary: the retained content is only the negative result for this tested matched-null frontier-echo ansatz on the specified grown row.
- **auditor confidence:** high

### `gate_b_grown_trapping_frontier_note`

- **Note:** [`GATE_B_GROWN_TRAPPING_FRONTIER_NOTE.md`](../../docs/GATE_B_GROWN_TRAPPING_FRONTIER_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_clean~~
- **effective_status:** **retained**  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** the detector-layer frontier bias rises steadily with eta while eta = 0 reproduces the grown baseline exactly, so the trap is doing more than simple attenuation on the tested row.  _(class `C`)_
- **chain closes:** True — The live runner recomputes the declared eta sweep on the drift=0.2, restore=0.7 row, including exact eta=0 reduction, falling escape, and monotone frontier-bias increase. The note explicitly limits the result to a bounded transport observable and excludes horizon theory, bidirectional field equations, and generated-family transfer.
- **rationale:** The finite bounded positive closes through the current runner: eta=0 is the baseline by construction, escape falls monotonically from 0.919 to 0.557 over the nonzero eta sweep, and frontier_bias rises monotonically from +0.0227 to +0.1509. The source does not claim a horizon theory, generated-family transfer, or general field equation, so the retained content is only this transport/frontier observable on the specified grown row. Residual boundary: the frozen log path named in the note is missing from the repo, but the live runner fully recomputes the table and is the load-bearing artifact here.
- **auditor confidence:** high

### `gate_b_grown_trapping_frontier_v2_note`

- **Note:** [`GATE_B_GROWN_TRAPPING_FRONTIER_V2_NOTE.md`](../../docs/GATE_B_GROWN_TRAPPING_FRONTIER_V2_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_clean~~
- **effective_status:** **retained**  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** the escape ratio falls steadily as eta grows while frontier_radius_shift rises steadily, so surviving detector mass is pushed outward on the detector shell.  _(class `C`)_
- **chain closes:** True — The live runner recomputes the eta sweep on the declared grown row, including exact eta=0 reduction, monotone escape attenuation, and monotone outward frontier-radius shift. The source note limits the result to a bounded transport/frontier probe and excludes horizon theory, bidirectional field equations, and generated-family transfer.
- **rationale:** The bounded positive closes through the current runner: eta=0 reproduces the baseline, escape decreases from 0.919 to 0.557 over the nonzero eta sweep, and frontier_radius_shift increases from +0.0684 to +0.4480. The note keeps the claim on this finite transport/frontier observable and does not promote a horizon theory or generated-family transfer. Residual boundary: the frozen log path named in the note is missing, but the live runner fully recomputes the table and is the load-bearing artifact here.
- **auditor confidence:** high

### `gate_b_grown_trapping_frontier_v3_note`

- **Note:** [`GATE_B_GROWN_TRAPPING_FRONTIER_V3_NOTE.md`](../../docs/GATE_B_GROWN_TRAPPING_FRONTIER_V3_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_clean~~
- **effective_status:** **retained**  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The new structural target is the shell-contrast shift, and it also rises steadily with trap coupling while eta = 0 reproduces the retained grown baseline exactly.  _(class `C`)_
- **chain closes:** True — The live runner recomputes the declared eta sweep on the grown row, including the exact eta=0 reduction, monotone escape attenuation, positive frontier-radius shift, and monotone frontier-shell-contrast shift. The note limits the result to this bounded frontier probe and excludes horizon theory, generated-family transfer, bidirectional field equations, and force-law claims.
- **rationale:** The bounded positive closes through the current runner: eta=0 reproduces the baseline, escape decreases monotonically across the nonzero eta sweep, frontier_radius_shift remains positive and rising, and frontier_shell_contrast_shift rises monotonically. The promoted observable in the note is the same detector-layer shell-contrast observable computed by the runner. The claim is not promoted beyond this finite shell-structure probe, and the note explicitly declines horizon theory, generated-family transfer, and force-law claims. Residual boundary: the frozen log path named in the note is missing, but the live runner fully recomputes the table and is the load-bearing artifact here.
- **auditor confidence:** high

### `gate_b_grown_trapping_transport_note`

- **Note:** [`GATE_B_GROWN_TRAPPING_TRANSPORT_NOTE.md`](../../docs/GATE_B_GROWN_TRAPPING_TRANSPORT_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_clean~~
- **effective_status:** **retained**  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The exact zero-coupling reduction passes, and the escape observable is bounded and monotone in the tested sweep.  _(class `C`)_
- **chain closes:** True — The live runner recomputes the declared grown-row eta sweep, reproducing eta=0 escape exactly and the monotone fall in detector escape across the five nonzero trap couplings. The source note limits the result to a bounded trap-sensitive transport probe and explicitly excludes horizon theory, a general bidirectional field equation, and generated-family transfer.
- **rationale:** The bounded positive closes through the current runner and frozen log: eta=0 returns escape=1.000, while the aggregate escape ratio falls monotonically from 0.799 at eta=0.05 to 0.205 at eta=0.50 on the declared grown row and trap slab. The note promotes only the detector escape ratio, which is exactly the observable computed by the runner. No cited dependency is needed for this finite computation, and the note does not claim a horizon theory, generated-family transfer, or general field equation. Residual boundary: the result remains a bounded transport probe for this row, static field, trap geometry, seeds, and eta sweep.
- **auditor confidence:** high

### `gate_b_grown_wavefield_companion_note`

- **Note:** [`GATE_B_GROWN_WAVEFIELD_COMPANION_NOTE.md`](../../docs/GATE_B_GROWN_WAVEFIELD_COMPANION_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_clean~~
- **effective_status:** **retained**  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The detector-line phase-ramp mechanism itself does not cleanly carry over on the retained grown row: the phase-ramp slopes are small and the R^2 values are low, while zero-source reduction is exact.  _(class `C`)_
- **chain closes:** True — The live runner recomputes the fixed-field grown-row companion scan, reproducing exact zero-source same-site and wavefield spans and low-R2 phase-ramp fits for both source layers. The source note frames the result as a bounded no-go for phase-ramp transfer and does not claim a geometry-generic or self-consistent field mechanism.
- **rationale:** The negative claim closes on its own terms: the current runner and frozen log agree that the zero-source guardrail is exactly zero for both same-site and wavefield updates, while the phase-ramp fits remain weak with R2 = 0.294 and 0.298 on the two tested source layers. The note's retained surface is the bounded no-go, not a transfer of the exact-lattice wavefield mechanism. The distinguishability comparator also reproduces as wave/same > 1 in both rows, but it is not promoted into a coherent phase-ramp law. Residual boundary: the result is limited to this fixed-field runner, its imported grown-row constructor, central detector-line readout, source layers, strengths, and two-seed scan.
- **auditor confidence:** high

### `gate_b_h025_distance_law_note`

- **Note:** [`GATE_B_H025_DISTANCE_LAW_NOTE.md`](../../docs/GATE_B_H025_DISTANCE_LAW_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_conditional~~
- **effective_status:** ~~audited_conditional~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The h=0.25 grown row keeps a positive declining tail on the compact retained family, so the grown-geometry distance-law story survives at the finer h = 0.25 scale.  _(class `C`)_
- **chain closes:** False — The runner closes the compact h=0.25 table itself, but the note frames that table as a transfer replay on a proposed-retained grown-geometry family and asks the reader to take it with bounded Gate B far-field and grown-joint companion notes. Those one-hop companions are still bounded/unaudited, so the promoted transfer framing does not close from retained inputs.
- **rationale:** Issue: the live runner reproduces the finite h=0.25 distance-tail table, but the source's transfer wording depends on Gate B far-field and grown-joint companion context that is bounded/unaudited rather than retained/audited clean. Why this blocks: a compact two-seed W=6 replay cannot by itself ratify the proposed-retained generated-geometry family or promote the distance-law transfer as retained upstream physics. Repair target: audit or prove the cited Gate B far-field and grown-joint generated-family inputs as retained, then rerun an h=0.25 transfer computation whose claim is explicitly scoped to those ratified inputs. Claim boundary until fixed: safely claim only that this runner reproduces a bounded compact h=0.25 replay with exact grid 10/10 TOWARD tail b^(-0.42) and grown drift=0.2 10/10 TOWARD tail b^(-0.54), not full Gate B closure or retained-family transfer.
- **open / conditional deps cited:**
  - `GATE_B_FARFIELD_NOTE.md`
  - `GATE_B_GROWN_JOINT_PACKAGE_NOTE.md`
- **auditor confidence:** high

### `gate_b_h025_farfield_note`

- **Note:** [`GATE_B_H025_FARFIELD_NOTE.md`](../../docs/GATE_B_H025_FARFIELD_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_conditional~~
- **effective_status:** ~~audited_conditional~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The exact grid and grown drift=0.2 rows both return 12/12 TOWARD with F~M = 1.00 at h = 0.25, so the grown-geometry far-field package survives the refinement on this bounded family.  _(class `C`)_
- **chain closes:** False — The live runner closes the finite h=0.25 far-field replay, but the source frames it as survival of a retained generated-geometry package and cites Gate B companion context that is bounded, unaudited, or already audited conditional. That dependency boundary prevents clean retained propagation.
- **rationale:** Issue: the current runner reproduces the h=0.25 far-field table, but the note's refinement-survival wording depends on Gate B far-field, h=0.5 grown distance-law, and grown-joint companion context that is bounded/unaudited or already conditional. Why this blocks: the finite 4-seed W=6 replay verifies a compact check, but it does not independently ratify the generated-geometry family as retained or close the broader Gate B package. Repair target: first audit-retain the cited Gate B far-field, grown distance-law, and grown-joint inputs or replace the transfer framing with a theorem scoped only to this h=0.25 runner. Claim boundary until fixed: safely claim only that this live harness reproduces a bounded h=0.25 replay with exact grid 12/12 TOWARD, grown drift=0.2 12/12 TOWARD, and F~M = 1.00 in both rows.
- **open / conditional deps cited:**
  - `GATE_B_FARFIELD_NOTE.md`
  - `GATE_B_GROWN_DISTANCE_LAW_NOTE.md`
  - `GATE_B_GROWN_JOINT_PACKAGE_NOTE.md`
- **auditor confidence:** high

### `gate_b_strong_field_observable_split_note`

- **Note:** [`GATE_B_STRONG_FIELD_OBSERVABLE_SPLIT_NOTE.md`](../../docs/GATE_B_STRONG_FIELD_OBSERVABLE_SPLIT_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_conditional~~
- **effective_status:** ~~audited_conditional~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The absorptive proxy is a real strong-field amplitude effect, while the minimal causal-memory probe is a clean no-go for propagating causality in that exact form, so the two probes are not testing the same mechanism.  _(class `B`)_
- **chain closes:** False — The synthesis is faithful to the two cited notes, but one cited input, the complex-action falsifier, is already audited conditional because its retained-row/Born guardrail depends on bounded unaudited Gate B context. A cross-note split cannot be cleaner than that input.
- **rationale:** Issue: the split note synthesizes two upstream probes, but the absorptive/complex-action input is audited conditional while only the causal-memory no-go input is audited clean. Why this blocks: the claim that the absorptive proxy is a separate useful strong-field observable inherits the unresolved retained-row and Born-guardrail boundary from the complex-action falsifier, so the synthesis cannot be ratified as clean retained science. Repair target: audit-retain or re-scope the complex-action falsifier and its Gate B grown-row guardrail, then rerun this synthesis against two clean or explicitly bounded inputs. Claim boundary until fixed: safely claim only that the two cited finite probes test different implemented mechanisms and that the minimal causal-memory ansatz is a clean no-go; the absorptive proxy remains a bounded conditional amplitude-effect probe, not evidence for a causal field.
- **open / conditional deps cited:**
  - `GATE_B_COMPLEX_ACTION_FALSIFIER_NOTE.md`
- **auditor confidence:** high

### `gate_b_v6_nearfield_comparator_note`

- **Note:** [`GATE_B_V6_NEARFIELD_COMPARATOR_NOTE.md`](../../docs/GATE_B_V6_NEARFIELD_COMPARATOR_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_clean~~
- **effective_status:** **retained**  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The v6 mixed result is not a case where the grown rule collapses while the exact grid stays clean: the ordered-lattice control is already worse on the closest bucket, and the retained grown row is better there though not universal across all seeds.  _(class `C`)_
- **chain closes:** True — The live comparator recomputes the exact-vs-grown near-field control on the declared v6 setup, reproducing the overall counts, bucket localization, and closest-bucket seed split. The source note keeps the claim bounded and explicitly declines full Gate B closure or universal generated-row dominance.
- **rationale:** The bounded comparator closes through the current runner: exact grid is 6/9 TOWARD with mean delta +0.000007, grown row is 33/36 TOWARD with mean delta +0.000021, and the closest y=1.0 bucket is worse on the exact grid while only one of four grown seeds flips. The observable in the note is the same detector-centroid shift and TOWARD count computed by the runner, and the note does not claim full Gate B closure or universal generated-row superiority. Residual boundary: the frozen log named by the note is missing, but the live runner fully regenerates the table and is the load-bearing artifact here.
- **auditor confidence:** high

### `gauge_scalar_temporal_completion_theorem_note`

- **Note:** [`GAUGE_SCALAR_TEMPORAL_COMPLETION_THEOREM_NOTE.md`](../../docs/GAUGE_SCALAR_TEMPORAL_COMPLETION_THEOREM_NOTE.md)
- **current_status:** support
- **audit_status:** ~~audited_conditional~~
- **effective_status:** ~~audited_conditional~~  (reason: `self`)
- **auditor:** `codex-audit-loop:fresh-2026-04-28-gauge_scalar_temporal_completion_theorem_note`  (codex-current; independence=fresh_context)
- **load-bearing step:** What still remains is the observable-level reduction step: why the full interacting gauge-vacuum plaquette expectation is exactly the local one-plaquette response evaluated at the completed effective coupling.  _(class `A`)_
- **chain closes:** False — The algebraic temporal-ratio computation closes on the stated accepted Wilson nearest-neighbor source grammar, and the live runner reports PASS=8 FAIL=0. It does not close the observable-level reduction from the full interacting plaquette expectation to this local one-plaquette response, which the note itself leaves open.
- **rationale:** Issue: the exact A_inf/A_2 = 2/sqrt(3) ratio is proved only for the stated accepted Wilson nearest-neighbor local bosonic scalar gauge-source class, while the note itself says the observable-level reduction from the full interacting gauge-vacuum plaquette expectation to the completed local response remains open.
Why this blocks: downstream plaquette or alpha_s claims need that observable bridge; this support theorem alone cannot promote the analytic plaquette candidate or any dependent proposed-retained claim.
Repair target: supply and audit a theorem deriving the interacting plaquette expectation/readout as the local one-plaquette response at the completed effective coupling, with a runner that computes that bridge rather than only the temporal kernel ratio.
Claim boundary until fixed: safe to claim the conditional exact temporal-completion law on the accepted Wilson local gauge-source class, not full plaquette observable closure.
- **open / conditional deps cited:**
  - `observable_level_interacting_plaquette_to_local_response_reduction_missing`
- **auditor confidence:** high

### `gauge_vacuum_plaquette_constant_lift_obstruction_note`

- **Note:** [`GAUGE_VACUUM_PLAQUETTE_CONSTANT_LIFT_OBSTRUCTION_NOTE.md`](../../docs/GAUGE_VACUUM_PLAQUETTE_CONSTANT_LIFT_OBSTRUCTION_NOTE.md)
- **current_status:** unknown
- **audit_status:** ~~audited_conditional~~
- **effective_status:** ~~audited_conditional~~  (reason: `self`)
- **auditor:** `codex-audit-loop:fresh-2026-04-28-gauge_vacuum_plaquette_constant_lift_obstruction_note`  (codex-current; independence=fresh_context)
- **load-bearing step:** This obstruction does not rule out analytic plaquette closure entirely. It rules out only the simplest constant-lift ansatz.  _(class `A`)_
- **chain closes:** False — The exact obstruction to the constant-lift ansatz closes, and the live runner reports THEOREM PASS=6 SUPPORT=1 FAIL=0. It does not close the remaining beta-dependent full-vacuum plaquette reduction law, which the note explicitly leaves as the open target.
- **rationale:** Issue: the note proves an exact no-go only for the constant-lift ansatz P(beta)=P_1plaq(Gamma beta); it explicitly leaves the nontrivial beta-dependent reduction law and its beta=6 continuation open.
Why this blocks: downstream plaquette or alpha_s claims cannot cite this row as positive analytic plaquette closure; it only removes one false closure route.
Repair target: derive and audit the beta-dependent full-vacuum reduction law beta_eff(beta), including its nonperturbative continuation/evaluation at beta=6 with a runner that computes that law.
Claim boundary until fixed: safe to claim the constant-lift obstruction Gamma_cand != 1 from the strong-coupling slope, not full plaquette observable closure.
- **open / conditional deps cited:**
  - `beta_dependent_full_vacuum_plaquette_reduction_law_missing`
- **auditor confidence:** high

### `gauge_vacuum_plaquette_first_sector_minimal_bulk_completion_3plus1_full_packet_no_go_theorem_note_2026-04-20`

- **Note:** [`GAUGE_VACUUM_PLAQUETTE_FIRST_SECTOR_MINIMAL_BULK_COMPLETION_3PLUS1_FULL_PACKET_NO_GO_THEOREM_NOTE_2026-04-20.md`](../../docs/GAUGE_VACUUM_PLAQUETTE_FIRST_SECTOR_MINIMAL_BULK_COMPLETION_3PLUS1_FULL_PACKET_NO_GO_THEOREM_NOTE_2026-04-20.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_clean~~
- **effective_status:** **retained**  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The full sparse-face target Hermitian block violates Cauchy interlacing against the selected retained 4x4 Wilson block, so no real or complex 3d compression of that ambient can reproduce the full target packet exactly.  _(class `A`)_
- **chain closes:** True — The live runner constructs the selected 4x4 block and full sparse-face target block, computes their spectra, and verifies a direct Cauchy-interlacing violation with wide margins: mu1=0.087544 exceeds lambda2=0.004214 and mu2=0.235017 exceeds lambda3=0.023920.
- **rationale:** The no-go closes on its stated finite-matrix boundary: full packet equality would require a 3d compression of the selected Hermitian 4x4 block to have the full target Hermitian block's eigenvalues, and the runner verifies that those eigenvalues violate the necessary Cauchy interlacing bounds. The fourth runner check also rules out rescuing the selected real slice by internal U(3) dressing because unitary similarity preserves the slice spectrum. This clean verdict is narrow: it certifies the exact full-packet impossibility for the runner-constructed selected 4x4 ambient and full sparse-face target block, not the independent physical retention of the surrounding gauge-vacuum selector program.
- **auditor confidence:** high

### `gauge_vacuum_plaquette_first_sector_minimal_bulk_completion_3plus1_reduced_packet_complex_givens_selector_theorem_note_2026-04-20`

- **Note:** [`GAUGE_VACUUM_PLAQUETTE_FIRST_SECTOR_MINIMAL_BULK_COMPLETION_3PLUS1_REDUCED_PACKET_COMPLEX_GIVENS_SELECTOR_THEOREM_NOTE_2026-04-20.md`](../../docs/GAUGE_VACUUM_PLAQUETTE_FIRST_SECTOR_MINIMAL_BULK_COMPLETION_3PLUS1_REDUCED_PACKET_COMPLEX_GIVENS_SELECTOR_THEOREM_NOTE_2026-04-20.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_conditional~~
- **effective_status:** ~~audited_conditional~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** Inside the fixed selected slice, solve the reduced projected-source packet equation in the ordered complex-Givens grammar G12*G13*G23 and choose the exact solution with least Frobenius distortion to the identity basis.  _(class `C`)_
- **chain closes:** False — The live runner finds exact reduced-packet solutions and a strict nearest-identity minimum among the found solutions, but it is a finite multi-seed numerical solve over a continuous six-angle grammar, not an exhaustive/global selector proof or a derivation that this grammar and Frobenius metric are physically forced.
- **rationale:** Issue: the runner verifies an impressive finite solve, but the note promotes it to an exact retained-slice selector theorem without proving that the sampled exact-solution list exhausts the continuous G12*G13*G23 grammar or that least Frobenius distortion to identity is a physically forced selector. Why this blocks: a hostile physicist can accept the replayed numbers, including 40 found exact solutions, packet error 8.15e-12, live-target error 4.47e-12, and a 0.01376 nearest-identity gap among those found solutions, but cannot infer a global canonical selector law or retained physical closure from a seeded least-squares search and chosen metric. Repair target: add an analytic or interval-certified enumeration of all exact solutions on the bounded six-angle domain, prove the selected solution is the global unique Frobenius minimizer, and register a retained theorem deriving the ordered complex-Givens grammar and Frobenius-to-identity metric from the selected ambient rather than choosing them after the target is known. Claim boundary until fixed: it is safe to claim that the current runner finds many exact reduced-packet dressings on the selected slice and identifies the nearest-to-identity solution among the audited found set; it is not yet an audited retained canonical selector theorem or a full physical derivation of the reduced-packet law.
- **open / conditional deps cited:**
  - `global_exact_solution_enumeration_for_continuous_G12_G13_G23_domain_missing`
  - `least_Frobenius_to_identity_selector_not_physically_derived`
  - `ordered_complex_Givens_grammar_not_derived_as_unique_retained_grammar`
  - `selected_slice_and_target_authorities_not_registered_one_hop_dependencies`
- **auditor confidence:** high

### `gauge_vacuum_plaquette_first_sector_rank_one_factorized_class_boundary_note_2026-04-19`

- **Note:** [`GAUGE_VACUUM_PLAQUETTE_FIRST_SECTOR_RANK_ONE_FACTORIZED_CLASS_BOUNDARY_NOTE_2026-04-19.md`](../../docs/GAUGE_VACUUM_PLAQUETTE_FIRST_SECTOR_RANK_ONE_FACTORIZED_CLASS_BOUNDARY_NOTE_2026-04-19.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_failed~~
- **effective_status:** ~~audited_failed~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The explicit rank-one witness is not itself a factorized Wilson realization because the back-conjugated operator is non-diagonal, and the best positive conjugation-symmetric diagonal fit still misses the completed target.  _(class `A`)_
- **chain closes:** False — The source note's load-bearing numerical checks require the declared runner, but `scripts/frontier_gauge_vacuum_plaquette_first_sector_rank_one_factorized_class_boundary_2026_04_19.py` is absent from the worktree. Without that executable artifact or one-hop source data constructing M, T_min, Z_min, and the diagonal fit, the stated off-diagonal norm and residuals cannot be audited.
- **rationale:** Issue: the note declares a runner and expected PASS=6, but the runner path is missing, so the off-diagonal norm 0.250338180104 and diagonal-fit residuals 0.135462193897 / 0.228465896152 are not reproducible from the allowed artifacts. Why this blocks: those numbers are the proof that the rank-one witness lies outside the canonical Wilson factorized class and that the audited diagonal family misses the completed triple; without the runner or equivalent one-hop derivation, the theorem is unsupported. Repair target: restore the exact runner or replace the note with a current executable proof that constructs M, T_min, Z_min, performs the positive conjugation-symmetric diagonal search, and reproduces PASS=6 from cited retained inputs. Claim boundary until fixed: safely claim only that the remaining Wilson target is intended to be stricter than generic transfer existence; do not claim the specific non-factorization theorem, residual bounds, or retained-sector boundary.
- **open / conditional deps cited:**
  - `scripts/frontier_gauge_vacuum_plaquette_first_sector_rank_one_factorized_class_boundary_2026_04_19.py`
- **auditor confidence:** high

### `gauge_vacuum_plaquette_first_sector_tail_underdetermination_theorem_note_2026-04-19`

- **Note:** [`GAUGE_VACUUM_PLAQUETTE_FIRST_SECTOR_TAIL_UNDERDETERMINATION_THEOREM_NOTE_2026-04-19.md`](../../docs/GAUGE_VACUUM_PLAQUETTE_FIRST_SECTOR_TAIL_UNDERDETERMINATION_THEOREM_NOTE_2026-04-19.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_failed~~
- **effective_status:** ~~audited_failed~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** Two full extensions agree exactly on the retained first-sector packet and reconstruct the same retained three-sample triple, but induce different Perron states and different Perron/Jacobi packets for the same source operator J.  _(class `A`)_
- **chain closes:** False — The source note's underdetermination theorem depends on the declared PASS=6 runner, but `scripts/frontier_gauge_vacuum_plaquette_first_sector_tail_underdetermination_theorem_2026_04_19.py` is absent from the worktree. Without that executable construction or one-hop source data for both extensions and their Perron/Jacobi packets, the claimed inequivalence cannot be audited.
- **rationale:** Issue: the note declares an exact runner and expected PASS=6, but the runner path is missing, so the two-extension underdetermination construction is not reproducible from the allowed artifacts. Why this blocks: the theorem requires verifying exact agreement on the retained packet and triple while showing different Perron states and Perron/Jacobi packets; prose alone does not establish those equalities and separations. Repair target: restore the runner or replace it with a current executable proof that constructs the zero extension and positive decaying tail extension, checks retained-packet/triple equality, and prints the Perron/Perron-Jacobi separation checks. Claim boundary until fixed: safely claim only that tail completion is posed as the remaining framework-point seam; do not claim a retained underdetermination theorem or explicit inequivalent extension pair.
- **open / conditional deps cited:**
  - `scripts/frontier_gauge_vacuum_plaquette_first_sector_tail_underdetermination_theorem_2026_04_19.py`
- **auditor confidence:** high

### `gauge_vacuum_plaquette_first_sector_truncated_environment_packet_note_2026-04-19`

- **Note:** [`GAUGE_VACUUM_PLAQUETTE_FIRST_SECTOR_TRUNCATED_ENVIRONMENT_PACKET_NOTE_2026-04-19.md`](../../docs/GAUGE_VACUUM_PLAQUETTE_FIRST_SECTOR_TRUNCATED_ENVIRONMENT_PACKET_NOTE_2026-04-19.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_conditional~~
- **effective_status:** ~~audited_conditional~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** Normalizing the completed first-sector coefficient vector by its trivial-channel coefficient gives rho_ret = (1, 0.267139565315, 0.267139565315, 0), and z00_min E_3 rho_ret reconstructs Z_min exactly.  _(class `A`)_
- **chain closes:** False — The live runner reproduces PASS=6 and the algebraic reconstruction gap, but it imports the completed-sector data and checks canonical environment language from one-hop notes whose audit/effective states are unknown or support. The retained theorem therefore depends on upstream inputs that are not audit-retained.
- **rationale:** Issue: the runner verifies the normalization and reconstruction algebra, but the completion vector v_min/Z_min comes from an unaudited unknown note and the canonical environment description comes from support notes rather than retained/audited-clean inputs. Why this blocks: the claim that the completed triple determines a retained diagonal/environment packet cannot be stronger than the upstream completion and environment-identification theorems it imports. Repair target: audit-retain the minimal positive completion note and the source-sector factorization / spatial environment character-measure inputs, or make this runner construct those inputs directly from retained authorities. Claim boundary until fixed: conditionally, given v_min and the canonical environment definitions, rho_ret is normalized, nonnegative, conjugation-symmetric, and reconstructs Z_min with gap 1.777e-16; the full beta=6 environment extension remains open.
- **open / conditional deps cited:**
  - `GAUGE_VACUUM_PLAQUETTE_FIRST_SYMMETRIC_THREE_SAMPLE_MINIMAL_POSITIVE_COMPLETION_NOTE_2026-04-19.md`
  - `GAUGE_VACUUM_PLAQUETTE_SOURCE_SECTOR_MATRIX_ELEMENT_FACTORIZATION_NOTE.md`
  - `GAUGE_VACUUM_PLAQUETTE_SPATIAL_ENVIRONMENT_CHARACTER_MEASURE_THEOREM_NOTE.md`
- **auditor confidence:** high

### `gauge_vacuum_plaquette_first_sector_zero_extension_factorized_class_theorem_note_2026-04-19`

- **Note:** [`GAUGE_VACUUM_PLAQUETTE_FIRST_SECTOR_ZERO_EXTENSION_FACTORIZED_CLASS_THEOREM_NOTE_2026-04-19.md`](../../docs/GAUGE_VACUUM_PLAQUETTE_FIRST_SECTOR_ZERO_EXTENSION_FACTORIZED_CLASS_THEOREM_NOTE_2026-04-19.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_conditional~~
- **effective_status:** ~~audited_conditional~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** Extending rho_ret by zero outside the retained first-symmetric weights gives a nonnegative conjugation-symmetric full coefficient sequence whose factorized operator is self-adjoint, conjugation-symmetric, positive semidefinite, and still reconstructs the retained completed triple.  _(class `A`)_
- **chain closes:** False — The live runner reproduces PASS=6, but it depends on a conditional truncated-packet input, a support character-measure input, an unknown completion input, and a boundary note now audited failed. The zero-extension algebra is current, but the retained theorem does not close through audit-retained dependencies.
- **rationale:** Issue: the runner verifies the zero-extension construction, but the rho_ret packet is imported from an audited-conditional truncated-packet theorem, the canonical character-measure class is still support, the completion input is unknown, and the runner's final seam check cites a boundary note that is audited failed because its runner is missing. Why this blocks: the local matrix algebra can show a PSD zero-extension only after accepting those upstream objects, so it cannot be promoted as a retained Wilson factorized-class theorem. Repair target: audit-retain the completion, character-measure, truncated-packet, and factorized-class boundary inputs or make this runner construct them from retained authorities without relying on failed/support notes. Claim boundary until fixed: conditionally, given rho_ret and the canonical factorized-class definitions, the zero extension has symmetry errors below 1e-15, min eigenvalue -2.038e-16, and reconstructs Z_min with gap 1.777e-16; the actual beta=6 environment packet and retained class-existence claim remain unratified.
- **open / conditional deps cited:**
  - `GAUGE_VACUUM_PLAQUETTE_FIRST_SECTOR_TRUNCATED_ENVIRONMENT_PACKET_NOTE_2026-04-19.md`
  - `GAUGE_VACUUM_PLAQUETTE_SPATIAL_ENVIRONMENT_CHARACTER_MEASURE_THEOREM_NOTE.md`
  - `GAUGE_VACUUM_PLAQUETTE_FIRST_SYMMETRIC_THREE_SAMPLE_MINIMAL_POSITIVE_COMPLETION_NOTE_2026-04-19.md`
  - `GAUGE_VACUUM_PLAQUETTE_FIRST_SECTOR_RANK_ONE_FACTORIZED_CLASS_BOUNDARY_NOTE_2026-04-19.md`
- **auditor confidence:** high

### `gauge_vacuum_plaquette_mixed_cumulant_audit_note`

- **Note:** [`GAUGE_VACUUM_PLAQUETTE_MIXED_CUMULANT_AUDIT_NOTE.md`](../../docs/GAUGE_VACUUM_PLAQUETTE_MIXED_CUMULANT_AUDIT_NOTE.md)
- **current_status:** support
- **audit_status:** ~~audited_conditional~~
- **effective_status:** ~~audited_conditional~~  (reason: `self`)
- **auditor:** `codex-audit-loop:fresh-2026-04-28-gauge_vacuum_plaquette_mixed_cumulant_audit_note`  (codex-current; independence=fresh_context)
- **load-bearing step:** The onset of the full-vacuum reduction law is now exact, but the nonperturbative continuation to the framework point `beta = 6` is still open.  _(class `A`)_
- **chain closes:** False — The exact small-beta onset coefficient closes, and the live runner reports THEOREM PASS=6 SUPPORT=1 FAIL=0. It does not close the full nonperturbative beta-dependent reduction law or its beta=6 evaluation, which the note explicitly leaves open.
- **rationale:** Issue: the note closes the first nonlinear small-beta coefficient beta_eff(beta)=beta+beta^5/26244+O(beta^6), but explicitly does not close the full nonperturbative beta_eff(beta) or its beta=6 value.
Why this blocks: downstream plaquette or alpha_s claims need the framework-point reduction, not only the onset coefficient, so this support theorem cannot promote analytic plaquette closure.
Repair target: derive and audit the full beta-dependent reduction law and its nonperturbative continuation/evaluation at beta=6 with a runner that computes the framework-point plaquette readout.
Claim boundary until fixed: safe to claim the exact first nonlocal coefficient and beta_eff onset, not full plaquette observable closure.
- **open / conditional deps cited:**
  - `nonperturbative_beta6_continuation_of_beta_eff_missing`
- **auditor confidence:** high

### `gauge_vacuum_plaquette_spatial_environment_tensor_transfer_theorem_note`

- **Note:** [`GAUGE_VACUUM_PLAQUETTE_SPATIAL_ENVIRONMENT_TENSOR_TRANSFER_THEOREM_NOTE.md`](../../docs/GAUGE_VACUUM_PLAQUETTE_SPATIAL_ENVIRONMENT_TENSOR_TRANSFER_THEOREM_NOTE.md)
- **current_status:** support
- **audit_status:** ~~audited_conditional~~
- **effective_status:** ~~audited_conditional~~  (reason: `self`)
- **auditor:** `codex-audit-loop:fresh-2026-04-28-gauge_vacuum_plaquette_spatial_environment_tensor_transfer_theorem_note`  (codex-current; independence=fresh_context)
- **load-bearing step:** The theorem above is structural and exact. The linked runner is intentionally a finite support packet only.  _(class `A`)_
- **chain closes:** False — The explicit positive tensor-transfer class closes structurally on the truncated audited support packet, and the live runner reports THEOREM PASS=4 SUPPORT=3 FAIL=0. It does not evaluate the full beta=6 tensor-transfer matrix elements, Perron state, boundary coefficients rho_(p,q)(6), or canonical P(6).
- **rationale:** Issue: the note sharpens the remaining spatial-environment problem to an explicit positive tensor-transfer class, but it does not evaluate the full beta=6 tensor-transfer matrix elements, Perron state, or rho_(p,q)(6) boundary data.
Why this blocks: downstream plaquette or alpha_s claims need the actual framework-point environment readout; a truncated support packet cannot promote analytic P(6) closure.
Repair target: compute and audit the full beta=6 tensor-transfer operator/Perron state and resulting boundary coefficients, with a runner that evaluates the canonical plaquette observable.
Claim boundary until fixed: safe to claim explicit positive tensor-transfer structure for the spatial environment, not full beta=6 plaquette closure.
- **open / conditional deps cited:**
  - `full_beta6_tensor_transfer_perron_state_missing`
- **auditor confidence:** high

### `geometry_superposition_dag_ensemble_note_2026-04-11`

- **Note:** [`GEOMETRY_SUPERPOSITION_DAG_ENSEMBLE_NOTE_2026-04-11.md`](../../docs/GEOMETRY_SUPERPOSITION_DAG_ENSEMBLE_NOTE_2026-04-11.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_failed~~
- **effective_status:** ~~audited_failed~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** This is a real bounded path-sum geometry-superposition signal, but it is not a staggered proposed_retained result and not part of the current staggered headline package.  _(class `C`)_
- **chain closes:** False — The source note explicitly disclaims proposed-retained status, while the audit queue classified it as proposed_retained because the phrase appears in a negative sentence. The declared runner path `frontier_geometry_superposition.py` is also stale; only a moved script under `scripts/` reproduces the bounded exploratory numbers.
- **rationale:** Issue: the source status says this is an exploratory DAG-ensemble path-sum result, not a staggered proposed_retained result, and the runner path recorded in the note/ledger does not exist at the declared location. Why this blocks: a claim that explicitly disclaims retained status and lacks its registered runner cannot be audit-ratified as proposed_retained, even though a moved script reproduces the bounded exploratory output. Repair target: re-scope the note/queue as bounded or support, update the runner path to `scripts/frontier_geometry_superposition.py`, preserve a current log, and build a separate staggered geometry-superposition harness before any retained promotion. Claim boundary until fixed: safely claim only the toy DAG path-sum signal from the moved script: normalized contrast 3.93%, centroid shift 0.0574, width change 0.0211, and detector phase differences up to about 0.323 rad; do not claim a retained staggered or BMV-style closure.
- **open / conditional deps cited:**
  - `frontier_geometry_superposition.py`
- **auditor confidence:** high

### `global_coherence_off_scaffold_note`

- **Note:** [`GLOBAL_COHERENCE_OFF_SCAFFOLD_NOTE.md`](../../docs/GLOBAL_COHERENCE_OFF_SCAFFOLD_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_conditional~~
- **effective_status:** ~~audited_conditional~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The off-scaffold batch of 9 continuous-position generators is used to show that the frozen free_coh >= 7.9597e-04 rule achieves only 5/9 accuracy, exactly matching the old two-property node-level rule, while the pre-committed structural pass/fail intuition achieves 8/9.  _(class `C`)_
- **chain closes:** False — The live source-note runner reproduces the 9-family table, the 5/9 frozen-rule accuracy, the 5/9 old-rule comparison, and the 8/9 structural-intuition count. The broader retained conclusion does not close because the executable labels the result PARTIAL, has no hard assertions, and the packet does not prove exhaustion of simple classifiers beyond this finite free_coh/old-rule card.
- **rationale:** Issue: the runner and archived log support the finite off-scaffold negative for the frozen free_coh threshold, but the source note promotes that finite card to a decisive closure of the simple-classifier line and a statement that no single node-level or global scalar metric carries the weight off-scaffold. Why this blocks: the allowed evidence tests one frozen free_coh threshold against one old two-property rule on 9 hand-specified off-scaffold generators; it does not constitute a theorem or exhaustive computation over simple metrics, generator distributions, thresholds, or readouts, and the runner itself prints PARTIAL rather than the source note's stronger decisive framing. Repair target: register scripts/global_coherence_off_scaffold.py as the primary runner, add hard assertions for the 9-family roster, no-refit threshold, L1=4/9, L2=5/9, old-rule=5/9, L3=8/9, and the intended retained/negative verdict, then either add a no-go theorem or exhaustive metric-search computation for the broad classifier-exhaustion claim or narrow the note to the finite off-scaffold free_coh result. Claim boundary until fixed: it is safe to claim that on the specified 9-generator continuous-position off-scaffold batch, the frozen free_coh >= 7.9597e-04 rule predicts PASS for all generators and matches the battery on 5/9, the same accuracy as the old node-level rule, while the hard-coded structural pass/fail expectations match 8/9; it is not safe to claim a general no-go for all simple classifiers or a law-level off-scaffold theorem.
- **open / conditional deps cited:**
  - `scripts/global_coherence_off_scaffold.py_not_registered_as_primary_runner`
  - `runner_prints_partial_verdict_and_diagnostics_without_hard_assertions`
  - `simple_classifier_exhaustion_no_go_theorem_or_exhaustive_metric_search_missing`
- **auditor confidence:** high

### `graph_first_selector_derivation_note`

- **Note:** [`GRAPH_FIRST_SELECTOR_DERIVATION_NOTE.md`](../../docs/GRAPH_FIRST_SELECTOR_DERIVATION_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_conditional~~
- **effective_status:** ~~audited_conditional~~  (reason: `self`)
- **auditor:** `codex-audit-loop:fresh-2026-04-27-graph_first_selector_derivation_note`  (codex-current; independence=fresh_context)
- **load-bearing step:** The first nontrivial even invariant V_sel(phi) = Tr H(phi)^4 - (1/8)(Tr H(phi)^2)^2 is treated as a selector potential whose normalized form F(p) has the three axis vertices as minima.  _(class `A`)_
- **chain closes:** False — The finite graph algebra closes for the displayed invariant and its axis minima, but the note does not derive a source law or variational principle that selects this invariant with the positive sign as the physical selector potential.
- **rationale:** Issue: The algebraic trace invariant is real and has axis minima, but the step from invariant to derived weak-axis selector assumes that this particular positive quartic is the potential/source law to minimize. Why this blocks: Without a retained theorem forcing that variational choice, the graph supplies an admissible axis-favoring invariant rather than a derived selector. Repair target: Derive the selector functional, coefficient sign, and normalization from the graph/taste axiom or an audited action principle, and update the runner so it constructs the selected variational functional rather than checking consequences after V_sel is chosen. Claim boundary until fixed: The note may claim that the canonical cube shifts admit an S3-symmetric quartic invariant whose normalized form has exactly the three axis minima with residual Z2 stabilizer.
- **auditor confidence:** high

### `graph_first_su3_integration_note`

- **Note:** [`GRAPH_FIRST_SU3_INTEGRATION_NOTE.md`](../../docs/GRAPH_FIRST_SU3_INTEGRATION_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_clean~~
- **effective_status:** **retained**  (reason: `self`)
- **auditor:** `codex-audit-loop:fresh-2026-04-27-graph_first_su3_integration_note`  (codex-current; independence=fresh_context)
- **load-bearing step:** Imposing the residual swap restricts the weak-su(2) commutant to operators preserving the 3 \oplus 1 base split, so Comm(su(2)_weak, tau) is gl(3) \oplus gl(1) and its compact semisimple part is su(3).  _(class `C`)_
- **chain closes:** True — The note states the selected-axis cube projection, constructs the fiber Pauli generators and complementary-axis swap, and the runner independently verifies the resulting joint commutant and embedded su(3) closure for all three selected axes. No one-hop dependencies are required for this bounded structural claim.
- **rationale:** The load-bearing construction is not a symbol rename or tuned numerical comparator: it builds graph-native shift, parity, projection, residual swap, commutant dimension, block ranks, and explicit su(3) generators directly from the 3-cube with a selected axis. The live runner reports PASS=111 FAIL=0, and the classified runner checks are first-principles structural computations. Residual risk is limited to the upstream existence/selection of the weak axis, which this note explicitly treats as an input boundary rather than deriving here.
- **auditor confidence:** high

### `graph_phase_diagram_scout_note`

- **Note:** [`GRAPH_PHASE_DIAGRAM_SCOUT_NOTE.md`](../../docs/GRAPH_PHASE_DIAGRAM_SCOUT_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_conditional~~
- **effective_status:** ~~audited_conditional~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** In this bounded sweep, sign fails first at delete_70 while Born remains machine-clean; exponent fidelity survives until the sign collapse and then becomes unavailable.  _(class `C`)_
- **chain closes:** False — The live runner reproduces the bounded scout table, but the note asks to read it through graph requirements, broken-graph robustness, and edge-deletion boundary notes whose current/effective statuses are unaudited proposed-retained, audited conditional, and unknown. The retained-family phase-diagram framing therefore does not close from audited-retained inputs.
- **rationale:** Issue: the runner verifies the short scout ladder, but the retained-family interpretation depends on one-hop graph notes that are not audit-clean, and the edge-deletion boundary note specifically says the 0.75-1.00 replay does not support a stable sign-flip threshold. Why this blocks: the finite delete_70 sign failure is not enough to ratify a retained phase diagram or a stable first-failure boundary for the family. Repair target: audit-retain the graph-requirements and edge-deletion inputs, then run a multi-seed harsher damage ladder or a distinct graph-family sweep that determines whether the sign boundary is stable. Claim boundary until fixed: safely claim only this bounded scout result: baseline/asymmetry/jitter/sparse/delete_10-50 preserve sign, Born, and F~M, while delete_70 flips sign with Born still clean; no retained graph phase diagram or stable threshold is established.
- **open / conditional deps cited:**
  - `INVERSE_PROBLEM_GRAPH_REQUIREMENTS_NOTE.md`
  - `BROKEN_GRAPH_ACTION_POWER_ROBUSTNESS_NOTE.md`
  - `EDGE_DELETION_BOUNDARY_SWEEP_NOTE.md`
- **auditor confidence:** high

### `gravitomagnetic_note`

- **Note:** [`GRAVITOMAGNETIC_NOTE.md`](../../docs/GRAVITOMAGNETIC_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_conditional~~
- **effective_status:** ~~audited_conditional~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The phase delay table at c=0.5, s=0.004, z0=3.0 shows an odd-in-v correction relative to the static v=0 row that is portable across three grown families.  _(class `C`)_
- **chain closes:** False — The source-note runner reproduces the mean phase table, from which the odd-in-v deltas can be manually reconstructed. It does not close as a retained gravitomagnetic law because the runner is not registered in the audit row, emits an incorrect zero delta column for negative velocities, has no PASS assertions or threshold checks, and uses an imposed moving source/proxy phase readout rather than a derived self-consistent tensor field.
- **rationale:** Issue: the note establishes a finite proxy replay of an odd-in-v phase delay, not a retained gravitomagnetic theorem. Why this blocks: the live runner's phase values support the source-note table, but the runner's delta column is stale/bugged for negative velocities because it prints zero before the static baseline is seen, and it never asserts antisymmetry, portability, monotonicity, or threshold residuals; the source trajectory is imposed and the source/readout/action authorities are not registered as one-hop dependencies. Repair target: register the primary runner, fix the delta computation to compare every row against v=0 after all phases are known, emit explicit PASS assertions for antisymmetry and cross-family portability, and add retained source-motion/phase-readout theorems if the claim is to be promoted beyond a proxy. Claim boundary until fixed: it is safe to claim a bounded numerical proxy in which the mean Shapiro phase varies oddly with imposed source velocity across three grown families; it is not safe to claim a retained gravitomagnetic effect or GR frame-dragging analogue.
- **open / conditional deps cited:**
  - `scripts/gravitomagnetic_portable.py_runner_not_registered_in_audit_queue`
  - `logs/2026-04-06-gravitomagnetic-portable.txt_runner_delta_column_bug_for_negative_velocities`
  - `static_Shapiro_delay_authority_not_registered_one_hop_dependency`
  - `causal_field_cone_and_phase_readout_theorem_not_registered`
  - `self_consistent_moving_source_dynamics_open`
  - `tensor_gravitomagnetic_frame_dragging_bridge_open_or_explicitly_out_of_scope`
- **auditor confidence:** high

### `gravitomagnetic_portability_note`

- **Note:** [`GRAVITOMAGNETIC_PORTABILITY_NOTE.md`](../../docs/GRAVITOMAGNETIC_PORTABILITY_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_failed~~
- **effective_status:** ~~audited_failed~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The odd-in-v phase correction is portable across the three retained grown families, with antisymmetry residual below 4% of the peak-to-peak odd signal.  _(class `C`)_
- **chain closes:** False — The two cited dependencies are audit-clean but narrower than this claim. The declared runner does not recompute moving-source propagation or the three-family portability table; it hard-codes the family rows and renders them, so the load-bearing third-family portability result is not checked by the allowed artifacts.
- **rationale:** Issue: `scripts/gravitomagnetic_portability.py` is a static report renderer with hard-coded delta(+v), delta(-v), odd-component, and residual values; it does not construct the three grown families, run zero/static controls, or propagate the signed moving-source observable. Why this blocks: the headline portability claim depends on exactly those computed rows, especially the third family that is not covered by the two clean dependencies, so the runner cannot distinguish a real portability result from copied constants. Repair target: replace the renderer with an executable probe that builds all three drift/restore families, recomputes exact zero and v=0 controls, runs +v/-v moving-source propagation, and derives the odd/residual table from live amplitudes. Claim boundary until fixed: the clean dependencies support only their own bounded signed-response results; this note may be treated as a static summary of alleged values, not as an audited three-family gravitomagnetic portability positive.
- **open / conditional deps cited:**
  - `scripts/gravitomagnetic_portability.py`
- **auditor confidence:** high

### `gravity_clean_derivation_note`

- **Note:** [`GRAVITY_CLEAN_DERIVATION_NOTE.md`](../../docs/GRAVITY_CLEAN_DERIVATION_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_conditional~~
- **effective_status:** ~~audited_conditional~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** Self-consistency is imposed as L^{-1}=G_0; since G_0=(-Delta_lat)^{-1}, the field operator is set to L=G_0^{-1}=-Delta_lat, yielding the Poisson equation and then Newton's 1/r^2 law.  _(class `E`)_
- **chain closes:** False — The decisive closure condition L^{-1}=G_0, the source law rho=|psi|^2 as mass density, and the test-mass/action response are physical premises in the note, not derived or registered one-hop retained inputs; no primary runner is registered for the claim.
- **rationale:** Issue: the note advertises a zero-free-parameter derivation of Newton gravity from Cl(3) on Z^3, but the load-bearing step is the imposed physical closure condition L^{-1}=G_0, followed by unregistered identifications of rho=|psi|^2 as gravitational mass density and test-mass response via S=L(1-phi). Why this blocks: the algebra L=G_0^{-1} is valid once the closure condition is granted, and the Z^3 Green-function asymptotic is standard mathematics, but the audit packet does not derive or register the physical law that the gravitational field operator must have the same Green function as the propagator, nor the source/readout/mass-coupling maps needed to turn the Poisson equation into F=G_N M_1 M_2/r^2; the ledger also has no registered runner despite the note naming a command. Repair target: register a primary gravity-clean runner and one-hop retained theorems deriving the self-consistency condition, the Born/mass-density source map, the weak-field action/test-mass response, and the lattice Green-function normalization/asymptotic with controlled finite-lattice checks. Claim boundary until fixed: it is safe to claim a conditional weak-field chain: if the framework imposes L^{-1}=G_0 and the stated source/response maps, then the Z^3 Laplacian Green function gives a Newtonian 1/r potential and inverse-square force in lattice units; it is not yet an audited retained derivation of Newton gravity from the single axiom alone.
- **open / conditional deps cited:**
  - `self_consistency_L_inverse_equals_G0_theorem_not_registered`
  - `rho_equals_abs_psi_squared_mass_density_bridge_not_registered`
  - `weak_field_action_test_mass_response_not_registered`
  - `lattice_green_function_normalization_runner_not_registered`
  - `scripts/frontier_gravity_clean_derivation.py_not_registered_primary_runner`
- **auditor confidence:** high

### `gravity_observable_hierarchy_note`

- **Note:** [`GRAVITY_OBSERVABLE_HIERARCHY_NOTE.md`](../../docs/GRAVITY_OBSERVABLE_HIERARCHY_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_failed~~
- **effective_status:** ~~audited_failed~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** On the current retained examples, 2D ultra-weak dense spent-delay is genuinely attractive, 3D action-power close-slit barrier is genuinely away, and 3D dense spent-delay is genuinely attractive on the retained tested z = 2..6 window.  _(class `C`)_
- **chain closes:** False — The live runner reproduces only five hierarchy rows, including dense 3D cases at z=3 and z=5. The source note claims and tabulates a denser z=2..6 retained window, while the cited dense-spent-delay note is already audited failed for a stale endpoint/window mismatch.
- **rationale:** Issue: the note's load-bearing retained dense-3D attraction claim covers z=2..6, but the current runner and log report only dense z=3 and z=5, and the one cited dense-spent-delay note is itself audited failed for an endpoint/window mismatch. Why this blocks: a canonical sign-interpretation note cannot retain an example table that the executable artifact does not compute, especially when a cited source for that example has already failed audit. Repair target: update the runner to compute and assert every source-note row, including z=2,4,6 and the z=7 null boundary, or narrow the note to the five rows the current runner actually emits and repair/audit the dense-spent-delay dependency. Claim boundary until fixed: safely claim only the live five-row hierarchy output: 2D ultra-weak attraction, 2D strong-field depletion, 3D power-action away/depletion, and dense 3D attraction at z=3 and z=5; do not claim the z=2..6 retained dense window or a canonical hierarchy over all listed retained examples.
- **open / conditional deps cited:**
  - `LATTICE_3D_DENSE_SPENT_DELAY_NOTE.md`
- **auditor confidence:** high

### `growing_graph_frontier_architecture_transfer_note`

- **Note:** [`GROWING_GRAPH_FRONTIER_ARCHITECTURE_TRANSFER_NOTE.md`](../../docs/GROWING_GRAPH_FRONTIER_ARCHITECTURE_TRANSFER_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_conditional~~
- **effective_status:** ~~audited_conditional~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** Old graph-ladder architecture applies as a connectivity-design guide, not as a rescued transport law.  _(class `B`)_
- **chain closes:** False — The note is a cross-note synthesis with no runner of its own. Its cited inputs are bounded, unknown, unaudited proposed-retained, or audited conditional, so the proposed-retained architecture-transfer lesson cannot close through audited-retained dependencies.
- **rationale:** Issue: the source promotes a retained architecture lesson, but it is a doc-only synthesis over graph/Gate B notes whose audit states are bounded, unknown, unaudited proposed-retained, or already conditional. Why this blocks: without audit-clean inputs or an executable synthesis check, the claim that the old graph ladder transfers to the current cleanup lane is guidance, not a retained theorem. Repair target: audit-retain the cited connectivity, graph-requirements, frontier-expansion, dynamic-limit, and graph-phase inputs, or rewrite this note as an explicitly bounded design memo. Claim boundary until fixed: safely claim only that the cited bounded notes motivate connectivity-design priorities: keep frontier delay as the promoted observable, treat dynamic propagation as a current static-control no-go, and require new connectivity rules to preserve signed far-field behavior before promotion.
- **open / conditional deps cited:**
  - `GATE_B_CONNECTIVITY_TOLERANCE_NOTE.md`
  - `GATE_B_WEAK_CONNECTIVITY_NOTE.md`
  - `GATE_B_NONLABEL_CONNECTIVITY_V1_NOTE.md`
  - `GATE_B_NONLABEL_CONNECTIVITY_V2_NOTE.md`
  - `GATE_B_NONLABEL_CONNECTIVITY_V3_NOTE.md`
  - `INVERSE_PROBLEM_GRAPH_REQUIREMENTS_NOTE.md`
  - `GROWING_GRAPH_FRONTIER_EXPANSION_PROXY_NOTE.md`
  - `GROWING_GRAPH_DYNAMIC_LIMIT_DIAGNOSTIC_NOTE.md`
  - `GRAPH_PHASE_DIAGRAM_SCOUT_NOTE.md`
- **auditor confidence:** high

### `growing_graph_static_control_audit_note`

- **Note:** [`GROWING_GRAPH_STATIC_CONTROL_AUDIT_NOTE.md`](../../docs/GROWING_GRAPH_STATIC_CONTROL_AUDIT_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_clean~~
- **effective_status:** **retained**  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The review-safe conclusion is to promote the frontier-delay proxy only and keep dynamic propagation as a static-control failure, not as a transport or cosmology statement.  _(class `C`)_
- **chain closes:** True — The live runner recomputes the growing-frontier graph distances from the seed graph, reproduces the 3.000 -> 22.000 frontier-delay increase and positive slopes, and separately recomputes the weak, non-monotone visibility-drop table against a static graph control. The source note keeps the conclusion inside that computed graph-distance/static-control boundary.
- **rationale:** The load-bearing computation is current with the live runner: frontier delay grows from 3.000 to 22.000 with frontier/RMS/width slopes +0.9325, +0.5981, and +0.2129, while the dynamic-propagation visibility drops are small and non-monotone across n_layers = 10, 15, 20. The runner constructs these quantities from graph snapshots, generated DAGs, propagation amplitudes, and frozen controls rather than hard-coding the contested conclusion. The source note's final claim is exactly the bounded safe read supported by the computation: retain graph-distance expansion and freeze dynamic-propagation repair as a no-go, with no transport, cosmology, unitarity, or field-theory extension.
- **auditor confidence:** high

### `grown_transfer_basin_note`

- **Note:** [`GROWN_TRANSFER_BASIN_NOTE.md`](../../docs/GROWN_TRANSFER_BASIN_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_failed~~
- **effective_status:** ~~audited_failed~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The nearby grown rows preserve both the signed-source sign law and the complex-action TOWARD -> AWAY crossover plus near-linear F~M, so the narrow grown-row basin is retained.  _(class `C`)_
- **chain closes:** False — The one-row diagnostic supports the new middle row under the corrected criterion, but a declared targeted basin runner still applies the rejected gamma0-zero criterion and emits the opposite SAFE READ: 0/4 nearby rows survive. The artifact chain is therefore stale/internally inconsistent for the plural basin promotion.
- **rationale:** Issue: `scripts/GROWN_TRANSFER_BASIN_TARGETED.py` still requires `abs(row.action_gamma0) < 1e-12`, the exact complex-action survival criterion that the source note says is wrong. Its live output for the four declared nearby rows prints zero/neutral controls, charge exponent 1.000, F0/F05 = 1.000, and toward = (3, 0), but then reports `nearby rows surviving both observables: 0/4` and `the retained positives do not survive this nearby basin`. Why this blocks: the headline retained basin claim depends on the same-row signed-source plus complex-action survival decision, and the declared artifact chain currently gives a contradictory pass/fail verdict for that decision rather than a clean regenerated basin log. Repair target: patch the targeted basin checker to use the source note's stated criterion, require same-row intersection of signed-source and complex-action survival, rerun/archive the targeted and full basin outputs, and update the note only after the executable SAFE READ matches the retained claim. Claim boundary until fixed: safely claim that the central retained grown row and the single middle diagnostic row at drift=0.20, restore=0.60 pass the corrected signed-source and complex-action checks; do not claim a retained nearby basin or graph-ladder transfer beyond that repaired runner output.
- **open / conditional deps cited:**
  - `GATE_B_CONNECTIVITY_TOLERANCE_NOTE.md`
  - `INVERSE_PROBLEM_GRAPH_REQUIREMENTS_NOTE.md`
  - `GATE_B_NONLABEL_CONNECTIVITY_V1_NOTE.md`
  - `GATE_B_NONLABEL_CONNECTIVITY_V2_NOTE.md`
  - `GATE_B_NONLABEL_CONNECTIVITY_V3_NOTE.md`
- **auditor confidence:** high

### `grown_wavefield_failure_diagnosis_note`

- **Note:** [`GROWN_WAVEFIELD_FAILURE_DIAGNOSIS_NOTE.md`](../../docs/GROWN_WAVEFIELD_FAILURE_DIAGNOSIS_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_conditional~~
- **effective_status:** ~~audited_conditional~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The strongest retained diagnosis is geometry-induced phase dephasing on the detector line: the grown geometry preserves amplitude response but does not preserve the linear phase accumulation needed for a coherent ramp.  _(class `B`)_
- **chain closes:** False — The live runner closes the grown-row no-go table itself, but the causal diagnosis compares that table to exact-lattice wavefield controls that are still unaudited and not held in a paired same-parameter geometry-isolation runner. The evidence supports a grown-row phase-ramp failure, not yet a retained causal attribution to geometry-induced dephasing.
- **rationale:** Issue: the source upgrades the clean grown-row no-go table into a retained diagnosis that the failure is caused by geometry-induced dephasing, but the allowed runner recomputes only the grown row and the exact-lattice comparison notes remain unaudited controls with different lattice/source/readout settings. Why this blocks: low grown-row ramp R2 values show that the phase-ramp observable fails on the retained grown row, but they do not by themselves isolate geometry as the causal variable or ratify the exact-lattice phase-ramp benchmark. Repair target: audit-retain the exact-lattice wavefield controls and add a paired exact-vs-grown comparator that holds the wavefield update, source placement, strengths, detector line, and ramp metric fixed while changing only the geometry family. Claim boundary until fixed: safely claim the already computed grown-row no-go: zero-source reduction survives, wave/same remains large, and ramp_R2 is low at 0.294 and 0.298; treat the geometry-dephasing explanation as a conditional diagnosis.
- **open / conditional deps cited:**
  - `SOURCE_RESOLVED_WAVEFIELD_GREEN_POCKET_NOTE.md`
  - `SOURCE_RESOLVED_WAVEFIELD_ESCALATION_NOTE.md`
- **auditor confidence:** high

### `h0125_failure_derivation`

- **Note:** [`H0125_FAILURE_DERIVATION.md`](../../docs/H0125_FAILURE_DERIVATION.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_failed~~
- **effective_status:** ~~audited_failed~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The h=0.125 failure is diagnosed and quantified by boundary leakage, beam-width growth, exponentially compounded probability loss, and an SNR=0.5 noise explanation of the AWAY result.  _(class `C`)_
- **chain closes:** False — The source note has no runner, no artifact chain, and no cited authority for the transfer norms, beam widths, detector probabilities, or SNR. Its stated probability formula also fails internally: retention^nl gives about 8.18e-4, 1.14e-11, and 4.26e-34 for the three rows, not 3.7e-59, 1.1e-88, and 1.6e-136.
- **rationale:** Issue: the note's load-bearing numerical diagnosis is unsupported by any declared runner or one-hop derivation, and the explicit formula `P_det = (retention)^nl` is inconsistent with the printed P_det table by tens to more than one hundred orders of magnitude. Why this blocks: the retained negative claim depends on those numbers to distinguish boundary leakage, beam spreading, compounded loss, and statistical-noise AWAY behavior; without a reproducible computation or internally consistent formula, the diagnosis is not auditable. Repair target: add an executable h=0.125 failure diagnostic that computes T_interior/T_corner, beam sigma, detector probability including any geometric-spreading factor, and centroid SNR from the same propagation model, then update the note so every table entry follows from that runner. Claim boundary until fixed: safely claim only that boundary leakage and beam spreading are plausible failure hypotheses and that h=0.125 has not been retained by this note; do not retain the quantified root-cause diagnosis or SNR=0.5 noise conclusion.
- **auditor confidence:** high

### `h2t_h0125_narrow_bridge_note`

- **Note:** [`H2T_H0125_NARROW_BRIDGE_NOTE.md`](../../docs/H2T_H0125_NARROW_BRIDGE_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_failed~~
- **effective_status:** ~~audited_failed~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The narrow h=0.125 bridge claim does not currently survive on main: the reduced family lacks enough TOWARD points for F~M, and the bridge family reaches h=0.125 with F~M about 0.50 rather than near 1.  _(class `C`)_
- **chain closes:** False — The live reduced-family runner reproduces the bounded negative table through h=0.125, but the source status and final verdict explicitly reject rather than retain the narrow h=0.125 bridge claim. The row is in the proposed-retained queue only because the status line mentions a proposed_retained claim that the note is auditing down.
- **rationale:** Issue: the source is not a proposed-retained bridge result; it is explicitly a bounded negative for a proposed-retained h=0.125 bridge claim. Why this blocks: applying a retained/proposed-retained audit result would promote the opposite of the note's own final verdict, and the reproduced reduced-family runner gives AWAY/no-F~M rows rather than a retained h=0.125 bridge. Repair target: change the note status/ledger classification to bounded negative, or if a retained negative theorem is intended, declare that status and include the focused h=0.125 single-row decision artifact plus the limit-diagnosis scripts/logs in the artifact chain. Claim boundary until fixed: safely claim only the bounded negative: Born is clean where measured, the reduced family reaches h=0.125 but has no TOWARD/F~M bridge, and the focused bridge row does not meet the F~M near-1 bar.
- **auditor confidence:** high

### `hadron_lane1_confinement_to_mass_firewall_note_2026-04-27`

- **Note:** [`HADRON_LANE1_CONFINEMENT_TO_MASS_FIREWALL_NOTE_2026-04-27.md`](../../docs/HADRON_LANE1_CONFINEMENT_TO_MASS_FIREWALL_NOTE_2026-04-27.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_clean~~
- **effective_status:** **retained**  (reason: `self`)
- **auditor:** `codex-audit-loop:fresh-2026-04-28-hadron_lane1_confinement_to_mass_firewall_note_2026-04-27`  (codex-current; independence=fresh_context)
- **load-bearing step:** Absent those premises, `sqrt(sigma)` can be used only as a bounded scale comparator or support input.  _(class `A`)_
- **chain closes:** True — The claim is a negative boundary: the note does not derive hadron masses, but shows that confinement plus one bounded string-tension scale leaves channel-dependent coefficients and the GMOR/nucleon inputs unretained. The live runner verifies the repo guardrails, the coefficient separation, the GMOR dependencies, and the safe open endpoint with PASS=16 FAIL=0.
- **rationale:** The retained content is the firewall itself, not a hadron-mass derivation. The note's load-bearing step is the exact underdetermination that a single bounded scale leaves independent dimensionless spectral coefficients and cannot supply the GMOR or nucleon-correlator inputs. The live runner confirms the current repository boundary and uses observed hadron masses only to expose coefficient freedom. Residual risk is downstream misuse: this audit does not ratify any pion, proton, neutron, or spectrum mass prediction.
- **auditor confidence:** high

### `higgs_mass_retention_analysis_note_2026-04-18`

- **Note:** [`HIGGS_MASS_RETENTION_ANALYSIS_NOTE_2026-04-18.md`](../../docs/HIGGS_MASS_RETENTION_ANALYSIS_NOTE_2026-04-18.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_conditional~~
- **effective_status:** ~~audited_conditional~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The retained band m_H = 125.04 GeV +/- 3.17 GeV is obtained by propagating the inherited YT through-2-loop Delta_R uncertainty with A_MH=2.67 and combining it in quadrature with loop-transport, classicality-BC, and threshold-matching retention gaps.  _(class `D`)_
- **chain closes:** False — The runner reproduces the stated budget arithmetic and an RGE sensitivity probe, but it consumes many unregistered inherited authorities as constants and uses a local 2-loop RGE replica while the note's central claim is the canonical 3-loop route. The audit packet therefore does not independently close the retained Higgs-band derivation or the observed-mass comparator claim.
- **rationale:** Issue: the Higgs retention band is a propagated budget built from inherited YT Delta_R bands, canonical Higgs authority centrals, hierarchy/canonical-surface constants, loop-geometric assumptions, quadrature independence, and the observed Higgs comparator, but none of these authorities are registered as one-hop dependencies for this row. Why this blocks: the runner can verify arithmetic after those inputs are supplied, but it does not derive the YT +/-0.70% band, the 125.1/119.8 GeV Higgs authority centrals, the 3-loop canonical RGE route, the loop-tail/geometric-gap model, the lambda(M_Pl)=0 classicality correction, or the independence assumptions behind the 3.17 GeV quadrature band; moreover its local compute_mh probe is documented as a 2-loop replica, not the canonical 3-loop runner that the note cites as authority. Repair target: register the YT Delta_R stack, canonical Higgs 3-loop runner/output, 2-loop authority, canonical plaquette/hierarchy constants, loop-geometric bound, classicality-BC theorem, threshold-matching source, and observed-mass comparator as dependencies; update the primary runner to call or reproduce the canonical 3-loop implementation and assert the 3.17 GeV band from registered outputs with explicit covariance/quadrature assumptions. Claim boundary until fixed: it is safe to claim a conditional retention-budget calculation: given the supplied inherited inputs and quadrature model, the script reproduces m_H about 125.04 GeV with a roughly 3.17 GeV 1-sigma budget and includes the observed 125.25 GeV value; it is not yet an audited retained first-principles Higgs-mass precision theorem or an independent validation of the YT/Higgs authority chain.
- **open / conditional deps cited:**
  - `YT_P1_DELTA_R_MASTER_ASSEMBLY_THEOREM_NOTE_2026-04-18.md_not_registered_one_hop_dependency`
  - `YT_P1_BZ_QUADRATURE_FULL_STAGGERED_PT_NOTE_2026-04-18.md_not_registered_one_hop_dependency`
  - `YT_P1_DELTA_R_2_LOOP_EXTENSION_NOTE_2026-04-18.md_not_registered_one_hop_dependency`
  - `HIGGS_MASS_DERIVED_NOTE.md_not_registered_one_hop_dependency`
  - `HIGGS_VACUUM_EXPLICIT_SYSTEMATIC_NOTE.md_not_registered_one_hop_dependency`
  - `scripts/frontier_higgs_mass_full_3loop.py_not_registered_dependency_output`
  - `quadrature_independence_model_for_retention_gaps_not_registered`
  - `observed_higgs_mass_comparator_not_registered`
- **auditor confidence:** high

### `higgs_z3_charge_pmns_gauge_redundancy_theorem_note_2026-04-17`

- **Note:** [`HIGGS_Z3_CHARGE_PMNS_GAUGE_REDUNDANCY_THEOREM_NOTE_2026-04-17.md`](../../docs/HIGGS_Z3_CHARGE_PMNS_GAUGE_REDUNDANCY_THEOREM_NOTE_2026-04-17.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_conditional~~
- **effective_status:** ~~audited_conditional~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The theorem demotes q_H=0 from a physical PMNS conditional to a gauge representative by showing that the q_H=0,+1,-1 Z3-trichotomy supports are right-handed cyclic column relabelings, so Y_e Y_e^dagger is identical on the same left-handed axes and PMNS moduli are insensitive to q_H up to the separately tracked sigma_hier row permutation.  _(class `C`)_
- **chain closes:** False — The primary runner passes 73/73 checks and verifies the advertised support masks, diagonal Y_eY_e^dagger structure, branch-wise PMNS modulus invariance on representative coupling choices, and explicit right-handed cyclic absorption. The chain does not close at retained theorem grade because the runner and note import the conjugate Z3 triplets, the retained Z3 support trichotomy, and the PMNS convention U_PMNS=U_nu^dagger U_e without registered one-hop dependencies; one of those upstream inputs has already been audited only conditionally. The final status-upgrade checks are also literal True summary assertions, not independent verification that the package citation chain has been repaired.
- **rationale:** The linear-algebra mechanism is credible: for the stated Z3 triplet charges and single-Higgs definite charge, the three allowed charged-lepton Yukawa supports are diagonal/forward-cyclic/backward-cyclic, and the cyclic branches are right-multiplications of the diagonal branch by e_R permutation matrices. That makes Y_eY_e^dagger and hence the left-handed PMNS contribution insensitive to q_H. The runner passes every numerical and structural check. The blocker is authority and scope. The audit row has no registered one-hop dependencies for the three retained inputs the note explicitly relies on, and the status claim that q_H=0 is now GAUGE(retained) in the DM flagship closure chain is asserted by the runner rather than audited against a registered citation-chain state. To repair the claim, register and audit the three-generation Z3 triplets, the Z3 support trichotomy, and the charged-lepton U_e/PMNS convention as one-hop dependencies; add a symbolic universal check or proof over arbitrary complex y_i rather than only representative samples; and separately verify the package-state update that removes q_H from the flagship conditionals. What can safely be claimed now is conditional: assuming the retained trichotomy and PMNS convention, q_H branches are PMNS-equivalent under right-handed basis relabeling, while sigma_hier, branch-choice/A-BCC, Yukawa magnitudes, and the flagship closure remain open or separate.
- **open / conditional deps cited:**
  - `THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md_not_registered_one_hop_dependency`
  - `NEUTRINO_DIRAC_Z3_SUPPORT_TRICHOTOMY_NOTE.md_not_registered_or_prior_audited_conditional`
  - `CHARGED_LEPTON_UE_IDENTITY_VIA_Z3_TRICHOTOMY_NOTE_2026-04-17.md_not_registered_one_hop_dependency`
  - `single_Higgs_definite_Z3_charge_premise_not_independently_audited_here`
  - `package_citation_chain_status_upgrade_CONDITIONAL_to_GAUGE_not_independently_verified`
  - `sigma_hier_observational_row_permutation_remains_open`
  - `branch_choice_A_BCC_or_basin_signature_condition_remains_open`
- **auditor confidence:** high

### `higher_symmetry_joint_validation_note`

- **Note:** [`HIGHER_SYMMETRY_JOINT_VALIDATION_NOTE.md`](../../docs/HIGHER_SYMMETRY_JOINT_VALIDATION_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_conditional~~
- **effective_status:** ~~audited_conditional~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The note claims a bounded Z2 x Z2 higher-symmetry coexistence lane: Born-clean, k=0-clean, band-gravity-positive, and with slower decoherence decay through N=80 on the discovery geometry and through N=120 on a denser narrow probe.  _(class `C`)_
- **chain closes:** False — The archived discovery-geometry log matches the first table, and the live validator reproduces the dense N=80/100/120 table when run with the stated dense arguments. The retained chain is still conditional because the named dense joint-validation log is absent, the validator imports the mirror joint readout as an unregistered one-hop dependency, and the scripts print diagnostics rather than asserting retained gates.
- **rationale:** Issue: the finite Z2 x Z2 tables are reproducible, but the source packet does not provide a registered, assertion-based primary runner/log pair for the retained N=120 joint card. Why this blocks: a hostile auditor can verify the printed finite rows, but cannot promote them to a clean retained higher-symmetry lane while the dense joint log path is missing, the mirror_chokepoint_joint readout is imported without registration as a one-hop authority, and the pass criteria for Born cleanliness, k=0, band-gravity positivity, and decoherence advantage are not hard runner gates. Repair target: register scripts/higher_symmetry_dag.py and scripts/mirror_chokepoint_joint.py or inline the audited readout assumptions, archive the dense joint-validation output at the named path, and add assertions for the family roster, seed counts, N windows, Born/k0 tolerances, band-positive counts, and exponent-fit boundaries. Claim boundary until fixed: it is safe to claim a finite diagnostic result: with the stated discovery and dense parameters, Z2 x Z2 reports machine-scale Born, zero k=0, positive mean band gravity on the tested N values, slower discovery-geometry decoherence decay than random/ring, and dense N=80/100/120 rows matching the live runner; it is not yet a clean retained asymptotic higher-symmetry theorem or gravity-law contender.
- **open / conditional deps cited:**
  - `logs/2026-04-03-higher-symmetry-joint-validation-z2z2-dense-n80-n120.txt_missing`
  - `scripts/mirror_chokepoint_joint.py_readout_not_registered_one_hop_dependency`
  - `scripts/higher_symmetry_dag.py_generator_family_not_registered_one_hop_dependency`
  - `runner_prints_diagnostics_without_hard_retention_assertions`
- **auditor confidence:** high

### `hubble_lane5_two_gate_dependency_firewall_note_2026-04-27`

- **Note:** [`HUBBLE_LANE5_TWO_GATE_DEPENDENCY_FIREWALL_NOTE_2026-04-27.md`](../../docs/HUBBLE_LANE5_TWO_GATE_DEPENDENCY_FIREWALL_NOTE_2026-04-27.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_clean~~
- **effective_status:** **retained**  (reason: `self`)
- **auditor:** `codex-audit-loop:fresh-2026-04-28-hubble_lane5_two_gate_dependency_firewall_note_2026-04-27`  (codex-current; independence=fresh_context)
- **load-bearing step:** So numerical Lane 5 closure requires a retained absolute-scale premise and a retained dimensionless cosmic-history premise: `(C1) AND ((C2) OR (C3))`.  _(class `A`)_
- **chain closes:** True — The claim is a negative boundary: the note does not derive numerical H_0, but shows that H_0 = H_inf/sqrt(L) remains sensitive to both an absolute-scale input and a dimensionless-history input. The live runner verifies the symbolic identity, one-gate counterexample families, structural-lock rescaling, and current gate inventory with PASS=18 FAIL=0.
- **rationale:** The retained content is the two-gate firewall, not a numerical H_0 derivation. The note's load-bearing algebra closes: solving L = (H_inf/H_0)^2 gives H_0 = H_inf/sqrt(L), and the live runner verifies nonzero sensitivity to both H_inf and L plus explicit one-gate counterexample families. The structural lock is correctly treated as a dimensionless form invariant under common rescaling, not as a scalar H_0 prediction. Residual risk is downstream misuse: this audit does not ratify Omega_Lambda, R_Lambda, Planck normalization, or a numerical Hubble-tension resolution.
- **auditor confidence:** high

### `i3_zero_exact_theorem_note`

- **Note:** [`I3_ZERO_EXACT_THEOREM_NOTE.md`](../../docs/I3_ZERO_EXACT_THEOREM_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_clean~~
- **effective_status:** **retained**  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** Given linear amplitude composition and quadratic probability P=|A|^2, the inclusion-exclusion expression I_3=|A+B+C|^2-|A+B|^2-|A+C|^2-|B+C|^2+|A|^2+|B|^2+|C|^2 cancels identically.  _(class `A`)_
- **chain closes:** True — The source note is explicitly scoped to the Hilbert/Born surface, and the algebraic cancellation follows for arbitrary complex amplitudes without additional lattice assumptions.
- **rationale:** The retained claim is the scoped exact theorem that I_3 vanishes once amplitudes add linearly and probabilities are quadratic, not a freestanding derivation of the Born rule. The runner verifies the identity for arbitrary complex amplitudes, higher Sorkin orders under the Born rule, a non-Born control, and concrete 1D/3D lattice propagator cross-checks, with 6 computed passes and no failures. Residual boundary: this audit ratifies the Hilbert-surface no-third-order-interference theorem only; it does not promote any claim that P=|A|^2 itself has been derived from the lattice axioms alone.
- **auditor confidence:** high

### `if_program_closing_note`

- **Note:** [`IF_PROGRAM_CLOSING_NOTE.md`](../../docs/IF_PROGRAM_CLOSING_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_failed~~
- **effective_status:** ~~audited_failed~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The IF / CL route works when the topology preserves branch separation, while the old dense connected local-architecture search is closed and should not be reopened.  _(class `B`)_
- **chain closes:** False — The note is a program-level synthesis with no declared runner, artifact chain, or cited one-hop notes/logs. The retained topology conclusion, large-N visibility caveat, seven failed emergence attempts, and IF/CL closure therefore cannot be audited from the allowed materials.
- **rationale:** Issue: the source promotes a retained repo-facing IF/CL topology outcome, but it provides no executable artifact, no runner output, and no explicit one-hop source notes for the dense-DAG failures, modular/gap-controlled positives, large-N visibility caveat, or seven failed local emergence attempts. Why this blocks: a program-closing retained claim cannot be verified from uncited narrative summaries; a hostile reviewer cannot check whether the same observable, topology family, IF/CL machinery, and gravity/decoherence criteria are being compared consistently. Repair target: split the memo into explicit cited inputs, add or cite the runners/logs for dense-uniform failure, modular-gap positive, large-N visibility, and local-emergence failures, then state a narrower claim whose conclusion follows from those one-hop artifacts. Claim boundary until fixed: safely treat this as a planning/triage memo: IF/CL and gap-controlled topology are current working hypotheses, while broad dense-connected architecture search should not be reopened without new cited evidence.
- **auditor confidence:** high

### `impact_parameter_lensing_note`

- **Note:** [`IMPACT_PARAMETER_LENSING_NOTE.md`](../../docs/IMPACT_PARAMETER_LENSING_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_conditional~~
- **effective_status:** ~~audited_conditional~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The strongest portable grown row has exact zero-field control, positive TOWARD deflection at every sampled impact parameter, and a near-Newtonian fit delta ~= C b^(-0.962) with R^2 = 0.870.  _(class `C`)_
- **chain closes:** False — The live runner reproduces the finite b-sweep and zero-field control for grown family 1, but it does not establish the upstream portability selection. The source's retained portability context includes one unknown note and one audited-conditional breakpoint diagnosis, so the strongest-portable-row framing does not close from retained inputs.
- **rationale:** Issue: the runner recomputes the one-family impact-parameter table, but the source promotes it as the strongest portable grown row using portability context that is not audit-clean: `DISTANCE_LAW_PORTABILITY_NOTE` is unknown and `DISTANCE_LAW_BREAKPOINT_NOTE` is already audited conditional. Why this blocks: a hard-coded one-family lensing probe cannot by itself ratify the row-selection claim or inherit a retained portability/breakpoint classification. Repair target: audit-retain the portability and breakpoint inputs, or replace the runner with a selector that recomputes all candidate portable grown families and proves that this row uniquely satisfies the stated impact-parameter law criteria. Claim boundary until fixed: safely claim the finite runner result only: zero-field delta is exactly zero at b=8, grown family 1 is 5/5 TOWARD on b = 5,6,7,8,10, and the fitted exponent is -0.962 with R2 = 0.870.
- **open / conditional deps cited:**
  - `DISTANCE_LAW_PORTABILITY_NOTE.md`
  - `DISTANCE_LAW_BREAKPOINT_NOTE.md`
- **auditor confidence:** high

### `impact_parameter_portability_note`

- **Note:** [`IMPACT_PARAMETER_PORTABILITY_NOTE.md`](../../docs/IMPACT_PARAMETER_PORTABILITY_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_conditional~~
- **effective_status:** ~~audited_conditional~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The retained impact-parameter law ports cleanly onto the second grown family: both tested portable rows have exact null controls, 5/5 TOWARD b-sweeps, and near-Newtonian exponents alpha = -0.962 and -0.947.  _(class `C`)_
- **chain closes:** False — The live runner reproduces the two-family finite table, but the retained portability framing depends on upstream context that is not audit-clean: the one-family lensing note is audited conditional, the portable-card extension is unaudited proposed-retained, and the impact-parameter portability extension is unknown.
- **rationale:** Issue: the runner recomputes the two hard-coded grown-family b-sweeps, but the source frames them as retained portable grown families using context that is conditional, unaudited, or unknown. Why this blocks: a two-row runner can establish the finite table for those two parameter rows, but it cannot by itself ratify the retained lensing parent, the portable-card family classification, or the family-3 holdout boundary. Repair target: audit-retain `IMPACT_PARAMETER_LENSING_NOTE`, `PORTABLE_CARD_EXTENSION_NOTE`, and `IMPACT_PARAMETER_PORTABILITY_EXTENSION_NOTE`, or replace this runner with a self-contained selector/comparator over the candidate portable families and explicit holdout criteria. Claim boundary until fixed: safely claim only the finite result: both tested rows have zero-field delta exactly zero at b=8, both are 5/5 TOWARD, the fitted exponents are -0.962 and -0.947 with R2 = 0.870 and 0.875, and the two-row alpha span is 0.015.
- **open / conditional deps cited:**
  - `IMPACT_PARAMETER_LENSING_NOTE.md`
  - `PORTABLE_CARD_EXTENSION_NOTE.md`
  - `IMPACT_PARAMETER_PORTABILITY_EXTENSION_NOTE.md`
- **auditor confidence:** high

### `independent_generators_heldout_note`

- **Note:** [`INDEPENDENT_GENERATORS_HELDOUT_NOTE.md`](../../docs/INDEPENDENT_GENERATORS_HELDOUT_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_clean~~
- **effective_status:** **retained**  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The in-sample classifier rule (avg_deg >= 10.415 and reach_frac >= 0.859) is applied without refit to nine scripted independent generator families, yielding only 2/9 full-battery passes, 4/9 hard-coded prediction accuracy, and 6/9 no-refit rule accuracy.  _(class `C`)_
- **chain closes:** True — The live runner rebuilds the nine named generator families, applies the same five-condition battery and frozen rule, and reproduces the negative table: only E1_er_p005 and E2_er_p020 pass, hard-coded predictions score 4/9, and the no-refit classifier rule scores 6/9.
- **rationale:** The finite negative result closes on its own terms: the checked-in runner contains the nine generator constructors, the hard-coded prediction dictionary, the five-condition battery, and the frozen avg_deg/reach_frac rule, and live replay matches the source note's pass/fail and accuracy claims. The decisive rule failures R1, R3, and X1 all satisfy the frozen structural thresholds but fail the actual battery, while only the two Erdős-Rényi families pass the full package. This clean verdict is narrow: it certifies this deterministic nine-family held-out replay and the checked-in prediction table, not an exhaustive statistical theorem over all independent generator laws or independent timestamp proof beyond the artifact chain.
- **auditor confidence:** high

### `inverse_problem_graph_requirements_note`

- **Note:** [`INVERSE_PROBLEM_GRAPH_REQUIREMENTS_NOTE.md`](../../docs/INVERSE_PROBLEM_GRAPH_REQUIREMENTS_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_failed~~
- **effective_status:** ~~audited_failed~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The retained family is robust to several natural perturbations, but heavy 70% edge deletion is too much and can reverse the sign, so the graph requirement is a bounded tested-perturbation statement rather than a universal theorem.  _(class `C`)_
- **chain closes:** False — The live runner reproduces the finite mixed perturbation table, including baseline/asymmetry/jitter/sparse TOWARD rows and a heavy_delete_70 AWAY row. That closes a bounded harness result, but not the proposed-retained queue interpretation or a retained inverse-problem theorem.
- **rationale:** Issue: the source status is explicitly `bounded graph-requirements harness`, and the live runner is mixed: heavy 70% edge deletion flips AWAY even though Born and controls remain clean. Why this blocks: the queued proposed-retained interpretation would promote a graph-requirements theorem, but the source and runner only support a bounded perturbation-slice result, with one tested perturbation failing. Repair target: change the row status/classification to bounded, or produce a theorem/runner that states the exact graph-perturbation class for which Newton+Born survive and audits the cited derivation inputs. Claim boundary until fixed: safely claim only the finite harness output: baseline, asym_zpos_removed, jitter_0.5h, and sparse_nn_only are TOWARD; heavy_delete_70 is AWAY; Born is machine-clean and k=0/no-field controls are zero on all tested rows.
- **open / conditional deps cited:**
  - `NEWTON_DERIVATION_NOTE.md`
  - `ACTION_UNIQUENESS_NOTE.md`
  - `PERSISTENT_INERTIAL_RESPONSE_READINESS_NOTE.md`
- **auditor confidence:** high

### `kernel_vs_gravity_note`

- **Note:** [`KERNEL_VS_GRAVITY_NOTE.md`](../../docs/KERNEL_VS_GRAVITY_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_failed~~
- **effective_status:** ~~audited_failed~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** Kernel-generic absorption occurs under any nonzero field for gamma > 0, while only the localized 1/r gravity field produces the TOWARD -> AWAY deflection crossover.  _(class `C`)_
- **chain closes:** False — The live runner supports the gravity-specific crossover and gamma=0.5 escape suppression, but it contradicts the source's stronger detector-escape claim for any gamma > 0: several nonzero-field rows at gamma=0.1 or 0.2 still have escape ratios above 1.
- **rationale:** Issue: the source conflates link-level imaginary-action damping with the detector escape observable. The factor exp(-k gamma L f) is below 1 for f > 0 and gamma > 0, but the runner's detector escape ratios are still above 1 for UNIFORM f=0.005 at gamma=0.1 and 0.2, UNIFORM f=0.01 at gamma=0.1 and 0.2, and GRAVITY at gamma=0.1 and 0.2. Why this blocks: the retained separation claim says kernel-generic absorption occurs under any nonzero field at gamma > 0, but the measured observable used by the note only shows suppression at sufficiently large gamma in this setup. Repair target: distinguish local per-link attenuation from total detector escape, or add a theorem/runner proving a thresholded escape-suppression criterion across gamma and field families. Claim boundary until fixed: safely claim only that gamma=0.5 suppresses detector escape for the tested nonzero fields, and that the 1/r gravity field uniquely shows the tested TOWARD -> AWAY centroid crossover by gamma=0.2.
- **auditor confidence:** high

### `koide_a1_physical_bridge_attempt_2026-04-22`

- **Note:** [`KOIDE_A1_PHYSICAL_BRIDGE_ATTEMPT_2026-04-22.md`](../../docs/KOIDE_A1_PHYSICAL_BRIDGE_ATTEMPT_2026-04-22.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_conditional~~
- **effective_status:** ~~audited_conditional~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** None of the tested standard mechanisms, W[J=0], Coleman-Weinberg, Gaussian max-entropy at fixed Frobenius, or continuous CV=1 max-entropy, supplies the physical source-law bridge selecting the A1/S_block extremum.  _(class `A`)_
- **chain closes:** False — The note gives hand algebra showing four candidate bridges fail or remain incomplete, and it explicitly says the A1 physical bridge is genuinely open. There is no registered runner, no one-hop dependency packet for the review-branch theorems, and no theorem proving either exhaustion of bridge mechanisms or a retained physical law selecting S_block.
- **rationale:** Issue: the note is a useful failed-attempt map, not a retained physical bridge for A1. Why this blocks: it confirms that several familiar mechanisms do not select the A1/Frobenius equipartition point, but the claimed internal A1 chain is referenced to unregistered review-branch material and the note offers no executable runner or exhaustive no-go theorem; its own recommendation is to adopt S_block as a new primitive, import Koide-Nishiura V(Phi), or keep researching the measure. Repair target: register the A1 internal-chain authorities and add runners for the four failed bridge attempts, then either derive a retained source law selecting S_block or explicitly demote the note to open bridge-landscape documentation. Claim boundary until fixed: it is safe to say these four attempted physical mechanisms do not currently close the A1 bridge; it is not safe to claim a proposed-retained physical derivation of A1.
- **open / conditional deps cited:**
  - `review_branch_KOIDE_FROBENIUS_ISOTYPE_SPLIT_UNIQUENESS_not_registered_one_hop_dependency`
  - `review_branch_KOIDE_KAPPA_BLOCK_TOTAL_FROBENIUS_MEASURE_not_registered_one_hop_dependency`
  - `review_branch_KOIDE_Q_DELTA_CLOSURE_PACKAGE_README_not_registered_one_hop_dependency`
  - `runner_for_WJ_Coleman_Weinberg_max_entropy_CV_attempts_not_registered`
  - `physical_source_law_selecting_S_block_open`
  - `Koide_Nishiura_VPhi_import_not_retained`
- **auditor confidence:** high

### `koide_a1_radian_bridge_irreducibility_audit_note_2026-04-24`

- **Note:** [`KOIDE_A1_RADIAN_BRIDGE_IRREDUCIBILITY_AUDIT_NOTE_2026-04-24.md`](../../docs/KOIDE_A1_RADIAN_BRIDGE_IRREDUCIBILITY_AUDIT_NOTE_2026-04-24.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_conditional~~
- **effective_status:** ~~audited_conditional~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** Retained periodic phase sources give only q*pi phases, while the Brannen selected-line target is the pure rational 2/9 used as a radian, so a Type-B rational-to-radian observable law remains primitive.  _(class `A`)_
- **chain closes:** False — The runner verifies the rational-pi versus pure-rational arithmetic and several finite-Wilson/A1 no-go probes, but the audit packet does not register the authority that this list exhausts retained phase sources or that the selected-line Koide/Brannen target is the required observable. Thus the no-go is valid for the supplied source taxonomy, not closed as a retained framework-wide irreducibility theorem.
- **rationale:** Issue: the no-go rests on an unregistered taxonomy asserting that all retained periodic phase sources are Type-A q*pi objects, while the Koide/Brannen selected-line delta target is a Type-B pure rational 2/9 to be read as radians; the note also imports branch-local no-go probes and Type-B witnesses without one-hop dependency registration. Why this blocks: the runner proves exact arithmetic for the listed examples and the mathematical separation q*pi in Q only at zero, but it does not prove the retained source list is exhaustive, that no allowed retained observable law can set a period-1-rad convention, or that the selected-line Brannen target is the physical readout. Repair target: register the retained phase-source classification, Brannen selected-line parameterization, April 24 Koide packet, APS/ABSS eta and other 2/9 witness authorities, plus the fractional-topology no-go probes as dependencies; add an exhaustive theorem or runner showing every retained phase/readout source factors through q*pi unless a named new primitive is added. Claim boundary until fixed: it is safe to claim conditional no-go support: for the listed finite lattice/APBC/BZ/Z3/C9/Wilson/Berry phase sources, phases are q*pi and cannot equal nonzero 2/9 radians, and the listed rational witnesses do not by themselves supply a unit map; it is not yet an audited retained proof that all possible CL3 retained routes to the Koide A1 radian bridge are irreducible.
- **open / conditional deps cited:**
  - `retained_periodic_phase_source_exhaustiveness_theorem_not_registered`
  - `Type_A_Type_B_phase_vs_rational_taxonomy_not_registered`
  - `Brannen_selected_line_delta_target_not_registered`
  - `period_1_rad_vs_2pi_rad_observable_convention_law_not_registered`
  - `KOIDE_DIMENSIONLESS_OBJECTION_CLOSURE_REVIEW_PACKET_2026-04-24.md_not_registered_and_audited_conditional`
  - `APS_ABSS_eta_2_over_9_authority_not_registered`
  - `SU3_Casimir_hypercharge_charge_product_2_over_9_witness_authorities_not_registered`
  - `fractional_topology_no_go_probe_bundle_not_registered`
  - `equivariant_index_A1_no_go_authority_not_registered`
  - `minimal_heat_kernel_multitrace_no_go_authority_not_registered`
- **auditor confidence:** high

### `koide_berry_phase_theorem_note_2026-04-19`

- **Note:** [`KOIDE_BERRY_PHASE_THEOREM_NOTE_2026-04-19.md`](../../docs/KOIDE_BERRY_PHASE_THEOREM_NOTE_2026-04-19.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_conditional~~
- **effective_status:** ~~audited_conditional~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** On the exact charged-lepton selected line, the physical phase offset delta(m) is the tautological CP^1 Berry holonomy of the projective C3 doublet ray from the unique unphased point, so solving delta = 2/9 fixes the first-branch point and kappa_sel.  _(class `C`)_
- **chain closes:** False — The live runner verifies the exact selected-line Berry geometry and scalar-phase bridge with 24 PASS and 0 FAIL. The clean mathematical route does not yet close as a retained physical Brannen-phase claim because the note itself states that the current package has not adopted this theorem stack and that the physical Brannen-phase bridge remains open.
- **rationale:** Issue: the runner closes the selected-line Berry theorem as an exact mathematical construction, but the source still conditions physical closure on an unretained Brannen-phase bridge and current-main adoption of the theorem stack. Why this blocks: a Berry holonomy equality on the constructed selected route is not by itself a retained physical charged-lepton phase theorem unless the selected route and Brannen phase observable are themselves retained as the physical carrier. Repair target: audit-retain the selected-line physical bridge and the Brannen phase observable mapping, or reclassify this note explicitly as mathematical/provenance support rather than proposed-retained physical closure. Claim boundary until fixed: safely claim the runner-verified exact route facts: the ambient S2 monopole closure is false, the actual selected-line projective C3 doublet has tautological connection A=dtheta, the holonomy from m0 equals delta, delta=2/9 gives m_Berry=-1.160443440065, and the old H_* witness is only near-coincident compatibility data.
- **auditor confidence:** high

### `koide_delta_marked_relative_cobordism_no_go_note_2026-04-24`

- **Note:** [`KOIDE_DELTA_MARKED_RELATIVE_COBORDISM_NO_GO_NOTE_2026-04-24.md`](../../docs/KOIDE_DELTA_MARKED_RELATIVE_COBORDISM_NO_GO_NOTE_2026-04-24.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_conditional~~
- **effective_status:** ~~audited_conditional~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** On the relevant rank-two zero-mode character multiplicity space, the retained Wilson/APS data act as lambda I, so the derived mark commutes with every candidate rank-one selector and has the same expectation on every line.  _(class `B`)_
- **chain closes:** False — The runner proves the linear-algebra consequence of a scalar mark: lambda I cannot select a unique rank-one line, and endpoint shifts leave c unfixed. It does not derive from registered one-hop retained Wilson/APS data that the only available derived boundary mark is scalar on the relevant multiplicity space.
- **rationale:** Issue: the no-go's decisive premise is that the derived retained Wilson/APS boundary mark restricts to lambda I on the rank-two zero-mode character multiplicity space. Why this blocks: the primary runner hard-codes retained_mark = lambda I and then checks the downstream commutator, expectation-value, endpoint-shift, and countermodel algebra; it does not construct the Wilson/APS operators, prove the multiplicity-space representation, or exhaust retained boundary marks from registered authorities. Repair target: register and run a theorem deriving the rank-two zero-mode multiplicity space and proving that every retained Wilson/APS-derived mark acts scalar there, or else exhibit a retained non-scalar mark and revise the no-go. Claim boundary until fixed: it is safe to claim the conditional obstruction that a scalar derived mark plus unbased endpoint section cannot select the Brannen line or force c=0; it is not yet an audited retained theorem that retained Wilson/APS data alone force that scalar-mark situation.
- **open / conditional deps cited:**
  - `retained_Wilson_APS_scalar_action_on_rank_two_zero_mode_multiplicity_theorem_not_registered`
  - `rank_two_zero_mode_character_multiplicity_space_construction_not_registered`
  - `derived_boundary_mark_exhaustion_theorem_not_registered`
  - `based_endpoint_section_no_go_theorem_or_boundary_section_theorem_not_registered`
  - `frontier_koide_lane_regression.py_rc_1_due_to_frontier_koide_q_so2_phase_erasure_support_22_of_23`
- **auditor confidence:** high

### `koide_dimensionless_objection_closure_review_packet_2026-04-24`

- **Note:** [`KOIDE_DIMENSIONLESS_OBJECTION_CLOSURE_REVIEW_PACKET_2026-04-24.md`](../../docs/KOIDE_DIMENSIONLESS_OBJECTION_CLOSURE_REVIEW_PACKET_2026-04-24.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_conditional~~
- **effective_status:** ~~audited_conditional~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The packet's safe retained-support statement is that KOIDE_DIMENSIONLESS_RETAINED_CLOSURE=FALSE because traceless Z backgrounds and ambient/spectator endpoint sources remain counterdomains unless extra source-domain and boundary laws are derived.  _(class `A`)_
- **chain closes:** False — The runner verifies the algebraic countermodels and conditional Q/delta closures, but the retained source carrier, Z label, APS eta value, selected-line endpoint law, and based endpoint section are imported premises rather than registered one-hop dependencies. The primary runner also does not emit every expected closeout line in the note, so the support packet is not fully closed by the registered runner output.
- **rationale:** Issue: the packet correctly avoids claiming full dimensionless Koide closure, but its proposed-retained support/no-go status relies on unregistered authorities for the normalized two-channel source-response carrier, retained central/projected commutant source grammar with Z, the April 25 background-zero/Z-erasure and onsite-source-domain results, the APS eta_APS=2/9 value, and the physical selected-line/based-endpoint boundary setup. Why this blocks: the primary runner proves rational counterexamples inside a supplied model, not that the supplied model is the retained physical source domain or that no retained boundary law elsewhere selects the closing quotient; it also omits several expected closeout declarations from the note, including the onsite-source-domain conditional and residual source-domain line. Repair target: register the source-response, onsite-source-domain, Q/delta split no-go, pointed-origin/endpoint, APS eta, and hostile-review guard authorities as one-hop dependencies; make the primary runner or registered runner bundle assert every expected closeout line and fail if any residual authority is missing. Claim boundary until fixed: it is safe to claim conditional support/no-go evidence: within the supplied two-channel source-response and endpoint-source toy algebra, z=0 gives Q=2/3, traceless Z and ambient endpoint sources give exact counterdomains, selected-line plus based endpoint would give delta=2/9, and full retained closure remains unestablished; it is not yet an audited retained proof of the physical dimensionless Koide obstruction or of all listed residual boundaries.
- **open / conditional deps cited:**
  - `retained_two_channel_source_response_carrier_not_registered`
  - `central_projected_commutant_Z_source_grammar_not_registered`
  - `april_25_background_zero_Z_erasure_criterion_theorem_not_registered`
  - `april_25_onsite_source_domain_synthesis_not_registered`
  - `APS_eta_APS_equals_2_over_9_authority_not_registered`
  - `selected_line_local_boundary_source_law_not_registered`
  - `based_endpoint_section_theorem_not_registered`
  - `scripts/frontier_koide_q_delta_readout_retention_split_no_go.py_not_registered_runner_dependency`
  - `scripts/frontier_koide_pointed_origin_exhaustion_theorem.py_not_registered_runner_dependency`
  - `scripts/frontier_koide_hostile_review_guard.py_not_registered_runner_dependency`
  - `scripts/frontier_koide_q_onsite_source_domain_no_go_synthesis.py_not_registered_runner_dependency`
- **auditor confidence:** high

### `koide_higgs_dressed_resolvent_root_theorem_note_2026-04-20`

- **Note:** [`KOIDE_HIGGS_DRESSED_RESOLVENT_ROOT_THEOREM_NOTE_2026-04-20.md`](../../docs/KOIDE_HIGGS_DRESSED_RESOLVENT_ROOT_THEOREM_NOTE_2026-04-20.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_numerical_match~~
- **effective_status:** ~~audited_numerical_match~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** For the fixed missing-axis lift W_4(h_0)=diag(h_0,H_*) at h_0=0, the scalar equation Q(abs eig Sigma_lambda(0))=2/3 has a unique small positive root lambda_* near chamber slack, and that root gives a PDG charged-lepton direction cosine above 0.996.  _(class `G`)_
- **chain closes:** False — The runner verifies the numerical root structure of a chosen resolvent family and shows that one selected root enforces Q=2/3 with a strong PDG direction cosine. It does not derive the missing-axis lift, h_0=0 baseline, lambda_* law, or chamber-slack relation from registered one-hop authorities.
- **rationale:** Issue: the load-bearing scalar lambda_* is selected by solving the target Koide equation Q=2/3 on a fixed imported lift, then the charged-lepton direction match is checked afterward. Why this blocks: root existence is a useful reduction of a search space, but the runner does not derive the natural missing-axis lift, prove h_0=0, compute lambda_* from a microscopic transport law, or derive its near-equality to chamber slack; exact Koide is guaranteed by construction because lambda_* is defined as a root of the Koide residual. Repair target: register the Higgs-dressed avenue/H_* authority, prove uniqueness of the missing-axis lift and h_0 baseline, and add a theorem/runner deriving lambda_* or the chamber-slack relation before imposing Q=2/3. Claim boundary until fixed: it is safe to claim that this chosen resolvent avenue reduces to isolated scalar roots and has a unique small positive root near chamber slack with strong PDG-direction cosine; it is not safe to claim a retained Koide derivation or a first-principles lambda law.
- **open / conditional deps cited:**
  - `scripts/frontier_higgs_dressed_propagator_v1.py_H_star_and_missing_axis_lift_authority_not_registered`
  - `missing_axis_lift_uniqueness_theorem_open`
  - `h0_zero_baseline_theorem_open`
  - `lambda_star_transport_law_from_Cl3_Z3_open`
  - `chamber_slack_to_resolvent_scalar_theorem_open`
  - `PDG_sqrt_mass_direction_comparator_not_registered_one_hop_dependency`
- **auditor confidence:** high

### `koide_kappa_block_total_frobenius_measure_theorem_note_2026-04-19`

- **Note:** [`KOIDE_KAPPA_BLOCK_TOTAL_FROBENIUS_MEASURE_THEOREM_NOTE_2026-04-19.md`](../../docs/KOIDE_KAPPA_BLOCK_TOTAL_FROBENIUS_MEASURE_THEOREM_NOTE_2026-04-19.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_conditional~~
- **effective_status:** ~~audited_conditional~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The block-total Frobenius-squared functional E_I(H) = ||pi_I(H)||_F^2 is claimed to be the retained 1:1 real-isotype measure that discharges the MRU measure-choice residue and supplies an independent operator-side kappa = 2 closure route.  _(class `C`)_
- **chain closes:** False — The runner closes the exact Herm_circ(3) block-total algebra and the finite d scan, but the retained closure claim depends on unaudited MRU/bridge notes and on a canonical choice between block-total and determinant log-laws that the source itself still lists as a residue.
- **rationale:** Issue: the live runner verifies the block-total Frobenius formulas, kappa = 2 equal-weight extremum, d = 3 multiplicity pattern, and PDG consistency, but the note promotes this to a no-residue retained closure while citing MRU/bridge authorities that are not audit-clean and while later admitting a remaining choice between block-total and det log-laws. Why this blocks: existence of a natural (1,1) Frobenius functional does not by itself select that functional as the canonical physical extremal principle, discharge the determinant-law alternative, or close the spectrum-side Koide input. Repair target: audit-retain the MRU quotient/weight-class and spectrum-operator bridge inputs, and add a theorem plus runner that selects block-total over the determinant/rank law without importing the target kappa. Claim boundary until fixed: safely claim the runner-verified exact algebra on Herm_circ(3): E_+ = 3a^2, E_perp = 6|b|^2, equal-weight block-total extremum gives kappa = 2, d = 3 has the checked one-trivial-plus-one-doublet pattern, and PDG masses are consistent; do not claim the measure-choice residue is discharged or that the operator-side closure is retained.
- **open / conditional deps cited:**
  - `KOIDE_MRU_WEIGHT_CLASS_OBSTRUCTION_THEOREM_NOTE_2026-04-19.md`
  - `KOIDE_MOMENT_RATIO_UNIFORMITY_THEOREM_NOTE_2026-04-19.md`
  - `KOIDE_KAPPA_SPECTRUM_OPERATOR_BRIDGE_THEOREM_NOTE_2026-04-19.md`
  - `KOIDE_CYCLIC_PROJECTOR_BLOCK_DEMOCRACY_NOTE_2026-04-18.md`
  - `KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md`
- **auditor confidence:** high

### `koide_kappa_spectrum_operator_bridge_theorem_note_2026-04-19`

- **Note:** [`KOIDE_KAPPA_SPECTRUM_OPERATOR_BRIDGE_THEOREM_NOTE_2026-04-19.md`](../../docs/KOIDE_KAPPA_SPECTRUM_OPERATOR_BRIDGE_THEOREM_NOTE_2026-04-19.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_conditional~~
- **effective_status:** ~~audited_conditional~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The exact identity a_0^2 - 2|z|^2 = 3(a^2 - 2|b|^2) is used to make spectrum-side Koide Q = 2/3 equivalent to operator-side kappa = 2 under the cyclic-compression bridge.  _(class `A`)_
- **chain closes:** False — The symbolic bridge identity closes, but the retained operator-side closure claim imports spectrum-side Koide closure, P1 sqrt-mass identification, and cyclic-response/Berry bridge inputs that are unaudited or already conditional.
- **rationale:** Issue: the runner verifies the zero-residual algebraic bridge on Herm_circ(3), but the note promotes the bridge into retained operator-side kappa = 2 closure while depending on non-clean spectrum-side Koide, P1 square-root, selected-line/Berry, and companion MRU inputs. Why this blocks: an exact equivalence transfers closure only if the physical sqrt-mass vector, cyclic-compression readout, and spectrum-side Q = 2/3 condition are themselves retained; the bridge does not derive or audit-retain those inputs. Repair target: audit-retain the spectrum-side Q/sigma theorem, P1 square-root amplitude/readout, selected-line cyclic-response bridge, and Berry/Brannen phase route, or narrow this note to a conditional bridge theorem. Claim boundary until fixed: safely claim the runner-verified identity a_0 = sqrt(3)a, |z|^2 = 3|b|^2, and a_0^2 - 2|z|^2 = 3(a^2 - 2|b|^2) on Herm_circ(3), plus PDG consistency; do not claim retained physical operator-side closure from Koide until the upstream physical inputs are clean.
- **open / conditional deps cited:**
  - `KOIDE_MRU_WEIGHT_CLASS_OBSTRUCTION_THEOREM_NOTE_2026-04-19.md`
  - `KOIDE_MOMENT_RATIO_UNIFORMITY_THEOREM_NOTE_2026-04-19.md`
  - `KOIDE_BERRY_PHASE_THEOREM_NOTE_2026-04-19.md`
  - `KOIDE_SELECTED_LINE_CYCLIC_RESPONSE_BRIDGE_NOTE_2026-04-18.md`
  - `KOIDE_SQRTM_AMPLITUDE_PRINCIPLE_NOTE_2026-04-18.md`
  - `CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md`
  - `KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md`
  - `KOIDE_KAPPA_BLOCK_TOTAL_FROBENIUS_MEASURE_THEOREM_NOTE_2026-04-19.md`
- **auditor confidence:** high

### `koide_native_dimensionless_review_packet_2026-04-24`

- **Note:** [`KOIDE_NATIVE_DIMENSIONLESS_REVIEW_PACKET_2026-04-24.md`](../../docs/KOIDE_NATIVE_DIMENSIONLESS_REVIEW_PACKET_2026-04-24.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_conditional~~
- **effective_status:** ~~audited_conditional~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The review packet demotes the strong native dimensionless Koide closure to a no-go/conditional support boundary: exact cohomology and readout data identify residual zero-section kernels but do not select the physical zero section, while the Q route and delta route remain conditional on physical background-zero/Z-erasure, selected-line boundary-source, and based endpoint-section laws.  _(class `A`)_
- **chain closes:** False — The packet's listed verification commands all return rc=0, with 163 total PASS-equivalent checks and no failure tokens, and they support the broad boundary that native dimensionless closure is false while the zero-section route implies the target values conditionally. The chain does not close because the queue has runner_path=null, the ledger lists no one-hop dependencies for the ten-runner review stack, and the packet is explicitly a support/no-go synthesis rather than a closure theorem. One expected boundary line in the packet also does not match the actual residual-cohomology runner name: the note expects KOIDE_Q_DELTA_RESIDUAL_COHOMOLOGY_CLOSES_FULL_LANE=FALSE, while the runner emits Q_DELTA_RESIDUAL_COHOMOLOGY_CLOSES_FULL_LANE=FALSE.
- **rationale:** The hostile audit agrees with the packet's bounded conclusion, not with any native closure claim. The runner set verifies exact residual-kernel/no-go statements, pointed-origin exhaustion, objection-closure review, native-zero-section conditional route, nature-review boundary flags, A1 radian-bridge irreducibility, and hostile-review guards. Those outputs support KOIDE_DIMENSIONLESS_NATIVE_CLOSURE=FALSE and NATIVE_ROUTE_IMPLIES_VALUES_CONDITIONALLY=TRUE. The blocker is that this is an integration/review packet with no primary runner registered in the audit queue and no one-hop dependency list in the ledger, even though it relies on ten separate runners and several underlying Koide theorems; some of those component claims are already only conditional. The note also has a verification-text mismatch for the residual-cohomology full-lane flag. To repair the claim, register the review packet's ten verification runners or their theorem notes as one-hop dependencies with audited statuses, fix the expected flag name, and provide clean retained theorems for the named residuals: physical background source zero equivalent to Z-erasure, selected-line local boundary source law, and based open-endpoint section. What can safely be claimed now is the negative/conditional boundary: the reviewed data do not close the dimensionless Koide lane; Q is reduced to a physical source-free reduced-carrier selection problem, delta remains conditional on selected-line and endpoint-source laws, and the native zero-section route is a next theorem target rather than current retained closure.
- **open / conditional deps cited:**
  - `scripts/frontier_koide_q_delta_residual_cohomology_obstruction_no_go.py_not_registered_primary_or_one_hop_runner`
  - `scripts/frontier_koide_q_delta_readout_retention_split_no_go.py_not_registered_primary_or_one_hop_runner`
  - `scripts/frontier_koide_delta_marked_relative_cobordism_no_go.py_not_registered_primary_or_one_hop_runner`
  - `scripts/frontier_koide_delta_lattice_wilson_selected_eigenline_no_go.py_not_registered_primary_or_one_hop_runner`
  - `scripts/frontier_koide_pointed_origin_exhaustion_theorem.py_not_registered_and_prior_audited_conditional`
  - `scripts/frontier_koide_dimensionless_objection_closure_review.py_not_registered_and_prior_audited_conditional`
  - `scripts/frontier_koide_native_zero_section_closure_route.py_not_registered_primary_or_one_hop_runner`
  - `scripts/frontier_koide_native_zero_section_nature_review.py_not_registered_primary_or_one_hop_runner`
  - `scripts/frontier_koide_a1_radian_bridge_irreducibility_audit.py_not_registered_and_prior_audited_conditional`
  - `scripts/frontier_koide_hostile_review_guard.py_not_registered_primary_or_one_hop_runner`
  - `physical_background_source_zero_equiv_Z_erasure_theorem_open`
  - `selected_line_local_boundary_source_law_open`
  - `based_open_endpoint_section_theorem_open`
  - `verification_flag_name_mismatch_KOIDE_Q_DELTA_RESIDUAL_COHOMOLOGY_CLOSES_FULL_LANE`
- **auditor confidence:** high

### `koide_native_zero_section_closure_route_note_2026-04-24`

- **Note:** [`KOIDE_NATIVE_ZERO_SECTION_CLOSURE_ROUTE_NOTE_2026-04-24.md`](../../docs/KOIDE_NATIVE_ZERO_SECTION_CLOSURE_ROUTE_NOTE_2026-04-24.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_conditional~~
- **effective_status:** ~~audited_conditional~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** Under the native zero-section identifications z = 0, spectator = 0, and c = 0, the runner verifies Q = 2/3 and delta_open = eta_APS = 2/9.  _(class `B`)_
- **chain closes:** False — The runner passes 17/17 and proves the algebraic consequences of the proposed native identifications. It explicitly labels the route conditional and does not derive the physical Brannen endpoint as the whole real Z3 primitive, the unit-preserving determinant-line endpoint readout, or the charged-lepton zero-source scalar readout.
- **rationale:** Issue: the route closes only after assuming the three zero-section identifications z=0, spectator=0, and c=0. Why this blocks: the primary runner proves exact representation and endpoint algebra once the native real-primitive endpoint, based determinant-line readout, and zero-source scalar readout are accepted, but it does not derive those physical identifications from registered retained authorities; the source note also states that retained-only closure is not claimed, and the broader Koide lane regression currently fails one q_so2 phase-erasure support check. Repair target: add retained theorems/runners deriving the charged-lepton zero-source scalar readout, proving the Brannen endpoint is the whole real nontrivial Z3 primitive rather than a rank-one line, and proving the determinant-line endpoint readout is unit-preserving/based. Claim boundary until fixed: it is safe to claim this exact conditional native route and its representation-theoretic no-spectator consequence; it is not safe to claim proposed-retained-only Koide closure.
- **open / conditional deps cited:**
  - `native_zero_source_charged_lepton_scalar_readout_theorem_open`
  - `Brannen_endpoint_is_real_Z3_primitive_not_rank_one_line_theorem_open`
  - `unit_preserving_determinant_line_endpoint_readout_theorem_open`
  - `APS_eta_fixed_point_authority_not_registered_one_hop_dependency`
  - `frontier_koide_lane_regression.py_rc_1_due_to_frontier_koide_q_so2_phase_erasure_support_22_of_23`
- **auditor confidence:** high

### `koide_native_zero_section_nature_review_note_2026-04-24`

- **Note:** [`KOIDE_NATIVE_ZERO_SECTION_NATURE_REVIEW_NOTE_2026-04-24.md`](../../docs/KOIDE_NATIVE_ZERO_SECTION_NATURE_REVIEW_NOTE_2026-04-24.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_conditional~~
- **effective_status:** ~~audited_conditional~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The review note accepts the native zero-section route only conditionally: if the physical Brannen endpoint is the whole real nontrivial Z3 primitive and the open determinant endpoint readout is unit-preserving/based, then the spectator and endpoint offset vanish, giving delta=2/9 alongside the Q zero-source route; without those identification theorems, retained/native Koide closure remains false.  _(class `B`)_
- **chain closes:** False — The primary runner passes 12/12 and emits KOIDE_NATIVE_ZERO_SECTION_NATURE_REVIEW=PASS_AS_ROUTE, KOIDE_NATIVE_ZERO_SECTION_RETAINED_CLOSURE=FALSE, and NATIVE_ROUTE_IMPLIES_VALUES_CONDITIONALLY=TRUE. The additional verification commands named by the note show the route runner and hostile guard passing, but the full Koide lane regression exits rc=1 with 380/381 checks because frontier_koide_q_so2_phase_erasure_support.py has 22/23. More importantly, the note itself identifies the missing retained theorems: real-primitive Brannen endpoint identification and a unit-preserving open determinant-line readout. Therefore the route is not a closed retained/native theorem.
- **rationale:** The review is useful and correctly scoped. Its primary runner confirms that the route passes as a route, not as closure: it checks the native route artifacts, verifies the route runner closeout, confirms Q and delta are implied under the stated hypotheses, identifies retained real-doublet support plus rank-one/CP1 tension, and records the remaining objections as identification theorems. The blockers are explicit. A Nature-grade audit cannot retain closure until a theorem derives that the physical Brannen endpoint is the real nontrivial Z3 primitive rather than a rank-one CP1 selector, and another theorem derives a based/unit-preserving open determinant endpoint readout rather than an unbased torsor coordinate. The broader lane regression also currently fails one check in q_so2 phase erasure support, so the note's full verification list is not green. Repair requires those two identification theorems, a fixed/understood lane regression, and registered one-hop dependencies for the route packet, Brannen geometry support, phase-reduction support, hostile guard, and any Q-side source-response theorem. What can safely be claimed is conditional: this is the strongest native route found so far and it implies the Koide Q/delta values if the real-primitive endpoint and unit endpoint readout are accepted; it does not close the full dimensionless Koide lane as retained/native theorem today.
- **open / conditional deps cited:**
  - `KOIDE_NATIVE_ZERO_SECTION_CLOSURE_ROUTE_NOTE_2026-04-24.md_not_registered_one_hop_dependency`
  - `scripts/frontier_koide_native_zero_section_closure_route.py_route_runner_not_registered_one_hop_dependency`
  - `KOIDE_BRANNEN_GEOMETRY_DIRAC_SUPPORT_NOTE_2026-04-22.md_not_registered_one_hop_dependency`
  - `KOIDE_BRANNEN_PHASE_REDUCTION_THEOREM_NOTE_2026-04-20.md_not_registered_one_hop_dependency`
  - `Brannen_endpoint_real_nontrivial_Z3_primitive_identification_theorem_open`
  - `unit_preserving_open_determinant_line_readout_theorem_open`
  - `rank_one_CP1_language_vs_real_primitive_endpoint_residual_open`
  - `zero_source_charged_lepton_scalar_readout_identification_not_closed_here`
  - `frontier_koide_lane_regression.py_rc_1_due_to_frontier_koide_q_so2_phase_erasure_support_22_of_23`
- **auditor confidence:** high

### `koide_p_one_clock_3plus1_transport_reduction_note_2026-04-20`

- **Note:** [`KOIDE_P_ONE_CLOCK_3PLUS1_TRANSPORT_REDUCTION_NOTE_2026-04-20.md`](../../docs/KOIDE_P_ONE_CLOCK_3PLUS1_TRANSPORT_REDUCTION_NOTE_2026-04-20.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_conditional~~
- **effective_status:** ~~audited_conditional~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** Assuming R1-R4, any framework-native closure of P must be branch-global/ambient in the one-clock 3+1 grammar, or use extra retained Wilson/lattice phase data; no intrinsic local selected-line law can close P.  _(class `B`)_
- **chain closes:** False — The runner verifies the selected-line target point and local-packet no-go calculations, but the reduction depends on Berry, selected-line bridge, local no-go, and anomaly-forced-time inputs that are support, unaudited, or already conditional.
- **rationale:** Issue: the reduction theorem is explicitly built from R1-R4, but those cited inputs are not audit-clean: Berry is conditional, the selected-line cyclic-response bridge is unaudited, the local radian no-go is support, and anomaly-forces-time is effective conditional; the runner also checks the anomaly input by doc-string presence and marks the final ambient-category consequence with a hard-coded True. Why this blocks: the note can only inherit the status of its assumptions, and a branch-global/ambient exclusion theorem cannot be retained until the local no-go and 3+1 one-clock ambient grammar are themselves retained computations. Repair target: audit-retain R1, R2, R3, and R4, and replace the doc-string/True consequence checks with runners that execute or import the audited theorem outputs and mechanically verify the exclusion/taxonomy. Claim boundary until fixed: safely claim that, conditional on R1-R4, the live runner finds a unique first-branch point with delta = 2/9 and shows the tested local selected-line packet is constant while delta varies; do not claim a retained one-clock 3+1 transport reduction of P.
- **open / conditional deps cited:**
  - `KOIDE_BERRY_PHASE_THEOREM_NOTE_2026-04-19.md`
  - `KOIDE_SELECTED_LINE_CYCLIC_RESPONSE_BRIDGE_NOTE_2026-04-18.md`
  - `KOIDE_SELECTED_LINE_LOCAL_RADIAN_BRIDGE_NO_GO_NOTE_2026-04-20.md`
  - `ANOMALY_FORCES_TIME_THEOREM.md`
- **auditor confidence:** high

### `koide_pointed_origin_exhaustion_theorem_note_2026-04-24`

- **Note:** [`KOIDE_POINTED_ORIGIN_EXHAUSTION_THEOREM_NOTE_2026-04-24.md`](../../docs/KOIDE_POINTED_ORIGIN_EXHAUSTION_THEOREM_NOTE_2026-04-24.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_conditional~~
- **effective_status:** ~~audited_conditional~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** Within the residual dimensionless Koide atlas, unpointed retained tests are invariant along the Q source-translation, CP1 selected-line, and endpoint-torsor fibres while the open charged-lepton readouts change, so origin-free retained data do not force the closing representative.  _(class `A`)_
- **chain closes:** False — The runner proves exact algebraic/torsor countermodels inside the supplied residual atlas, but that atlas, its three fibres, the eta_APS readout, and the claim that these are the retained unpointed tests are not registered as one-hop dependencies. The theorem therefore closes conditionally inside the modeled atlas, not as an audited retained exhaustion theorem for the full Koide lane.
- **rationale:** Issue: the no-go/exhaustion theorem assumes a residual Koide atlas with exactly three unpointed freedoms: Q source-origin translation, CP1 selected-line source choice, and endpoint torsor translation, but the audit row registers no one-hop authority that this atlas is complete or retained. Why this blocks: the runner proves that polynomial invariants, scalar equivariant marks, and torsor-invariant data cannot choose the pointed representative in the supplied model, but it does not derive that the physical charged-lepton readout is restricted to that model or that no retained source/boundary law already selects the needed origin. Repair target: register the residual Koide atlas, source-response carrier, CP1/selected-line primitive, endpoint torsor, eta_APS readout, April 24 Koide packet, and background-zero/Z-erasure authorities as dependencies; add an exhaustion theorem showing these fibres are complete for retained unpointed data. Claim boundary until fixed: it is safe to claim conditional necessity inside the stated atlas: a pointed origin law would close Q=2/3 and delta=2/9, while unpointed invariant data admit countermodels; it is not yet an audited retained proof that all CL3 Koide dimensionless closure routes require exactly those physical source/boundary-origin laws.
- **open / conditional deps cited:**
  - `residual_dimensionless_Koide_atlas_not_registered`
  - `Q_source_response_background_translation_fibre_not_registered`
  - `CP1_selected_line_rank_two_primitive_not_registered`
  - `endpoint_torsor_readout_model_not_registered`
  - `eta_APS_Z3_1_2_equals_2_over_9_authority_not_registered`
  - `KOIDE_DIMENSIONLESS_OBJECTION_CLOSURE_REVIEW_PACKET_2026-04-24.md_not_registered_and_audited_conditional`
  - `background_zero_Z_erasure_criterion_authority_not_registered`
  - `selected_line_local_boundary_source_law_not_registered`
  - `based_endpoint_section_theorem_not_registered`
  - `retained_physical_source_boundary_origin_law_open`
- **auditor confidence:** high

### `koide_q_delta_readout_retention_split_no_go_note_2026-04-24`

- **Note:** [`KOIDE_Q_DELTA_READOUT_RETENTION_SPLIT_NO_GO_NOTE_2026-04-24.md`](../../docs/KOIDE_Q_DELTA_READOUT_RETENTION_SPLIT_NO_GO_NOTE_2026-04-24.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_conditional~~
- **effective_status:** ~~audited_conditional~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** Source-response coefficients are zero-probe coefficients around a chosen background, so the current retained packet does not prove that the physical charged-lepton background source is zero; closed APS readout also leaves eta_APS = delta_open + tau with the selected open endpoint split free.  _(class `B`)_
- **chain closes:** False — The runner verifies the conditional algebra: zero-background source-response gives K_TL=0 and Q=2/3, while closed APS fixes eta_APS=2/9 but not the open endpoint split. The chain does not close as retained-only because the runner imports unregistered source-response notes and still requires a physical background-zero/Z-erasure theorem plus a closed-APS-to-open-endpoint functor.
- **rationale:** Issue: the note establishes conditional support, not retained closure: the Q side only closes if the physical charged-lepton background source is zero, and the delta side still needs a functor from closed APS holonomy to the selected open endpoint coordinate. Why this blocks: the primary runner reads OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md and HIERARCHY_BOSONIC_BILINEAR_SELECTOR_NOTE.md directly even though the audit row has no registered one-hop dependencies, then proves downstream algebra under the zero-background condition; it does not derive the physical background-zero law or the closed-to-open endpoint bridge. Repair target: register the source-response and hierarchy authorities, add a theorem/runner deriving physical background-source zero equivalently to Z-erasure, and add a theorem/runner deriving the closed APS to open selected-line endpoint functor. Claim boundary until fixed: it is safe to claim that strict source-response readout conditionally gives Q=2/3 at zero background and that closed APS alone leaves the delta split free; it is not safe to claim proposed-retained full Koide readout closure.
- **open / conditional deps cited:**
  - `OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md_not_registered_one_hop_dependency`
  - `HIERARCHY_BOSONIC_BILINEAR_SELECTOR_NOTE.md_not_registered_one_hop_dependency`
  - `derive_physical_background_source_zero_equiv_Z_erasure`
  - `closed_APS_to_open_selected_line_endpoint_functor_or_descent_theorem`
- **auditor confidence:** high

### `koide_q_delta_residual_cohomology_obstruction_no_go_note_2026-04-24`

- **Note:** [`KOIDE_Q_DELTA_RESIDUAL_COHOMOLOGY_OBSTRUCTION_NO_GO_NOTE_2026-04-24.md`](../../docs/KOIDE_Q_DELTA_RESIDUAL_COHOMOLOGY_OBSTRUCTION_NO_GO_NOTE_2026-04-24.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_clean~~
- **effective_status:** **retained**  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** Exactness gives fibres, not canonical splittings; the closing section is the special case a = 0, b1 = 0, b2 = 0, so that choice is exactly the missing primitive-based readout/basepoint law.  _(class `A`)_
- **chain closes:** True — The note and primary runner prove the stated no-go at the level claimed: the retained Q and delta projections have nontrivial kernels, kernel translations preserve the retained totals, and sections form non-unique families. Therefore exactness alone names the residual directions but does not canonically select the zero representative.
- **rationale:** The load-bearing claim is a negative exactness claim, not a positive Koide closure claim. The primary runner passes 15/15 symbolic checks: it computes ker(pi_Q)=span{Z}, ker(pi_delta)=span{selected-spectator, endpoint-exact}, verifies nonzero kernel representatives preserve the retained totals while moving the Q/delta readouts, and exhibits non-unique section families. No cited upstream physical bridge is needed for the narrow no-go that exactness alone does not pick z=0, spectator=0, c=0. The broader Koide lane regression currently fails one q_so2 phase-erasure support check, but that is not load-bearing for this exact cohomology obstruction.
- **auditor confidence:** high

### `koide_q_eq_3delta_identity_note_2026-04-21`

- **Note:** [`KOIDE_Q_EQ_3DELTA_IDENTITY_NOTE_2026-04-21.md`](../../docs/KOIDE_Q_EQ_3DELTA_IDENTITY_NOTE_2026-04-21.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_decoration~~
- **effective_status:** ~~audited_decoration~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** Combining Q = 2/d, delta = 2/p^2, and p = d = 3 gives Q/delta = p^2/d = p, so Q = p * delta and numerically Q = 3 * delta.  _(class `A`)_
- **chain closes:** False — The arithmetic identity closes exactly once the current Q=2/3, delta=2/9, and p=d=3 support-route values are supplied. As an independent proposed-retained claim, however, the runner hard-codes those upstream values and the p=d same-Z3 identification rather than deriving or registering them as one-hop authorities.
- **rationale:** Issue: the note is an exact arithmetic corollary of the current Koide support-route values, not an independent physical theorem. Why this blocks: the runner verifies Q = 3 delta after setting Q=2/3, delta=2/9, p=3, and d=3, and it treats the same-Z3 p=d bridge as an input; there is no new observable, comparator, falsifiable prediction, or first-principles computation beyond those upstream values. Repair target: box this identity under the audited Koide Q/delta parent packet, or re-promote only if a registered theorem proves the p=d same-Z3 structural bridge and the identity materially compresses downstream claims. Claim boundary until fixed: it is safe to state that accepted Q=2/3 and delta=2/9 values obey the exact bookkeeping identity Q=3 delta; it is not safe to count this as a separate retained theorem-grade result.
- **open / conditional deps cited:**
  - `Koide_Q_support_route_value_Q_2_over_3_not_registered_one_hop_dependency`
  - `Koide_delta_APS_support_route_value_delta_2_over_9_not_registered_one_hop_dependency`
  - `same_Z3_p_equals_d_structural_bridge_not_registered_one_hop_dependency`
- **auditor confidence:** high

### `koide_selected_line_provenance_note_2026-04-20`

- **Note:** [`KOIDE_SELECTED_LINE_PROVENANCE_NOTE_2026-04-20.md`](../../docs/KOIDE_SELECTED_LINE_PROVENANCE_NOTE_2026-04-20.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_conditional~~
- **effective_status:** ~~audited_conditional~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The retained parity-compatible observable-selector theorem is used to minimize delta^2 + q_+^2 on q_+ = sqrt(8/3) - delta, yielding delta_* = q_+* = sqrt(6)/3 and therefore H_sel(m) = H(m, sqrt(6)/3, sqrt(6)/3).  _(class `C`)_
- **chain closes:** False — The source runner derives the slot values from the stated chart and selector assumptions, but the claimed retained provenance depends on observable-principle, active-affine, half-plane, parity-baseline, selector, and frozen-bank notes that are unknown or effective-conditional rather than audit-clean.
- **rationale:** Issue: the live runner reproduces the selected-line slot derivation, but it hard-codes the atlas constants and only checks provenance-file presence instead of importing audited theorem outputs; the one-hop provenance stack is mostly unknown or effective-conditional. Why this blocks: the note claims a complete retained-on-main provenance for the numeric slots, but retained status cannot propagate through unaudited/conditional selector, half-plane, parity-baseline, observable-principle, and frozen-bank inputs. Repair target: audit-retain the cited source-surface and observable-principle theorems, and update the provenance runner to consume their runner outputs or generated constants rather than restating them. Claim boundary until fixed: safely claim that, given the stated active-affine chart, parity-compatible baseline family, active half-plane, and quadratic selector law, the minimizer is delta_* = q_+* = sqrt(6)/3 and reconstructs H_sel(m); do not claim I3 is closed by retained provenance.
- **open / conditional deps cited:**
  - `OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md`
  - `DM_NEUTRINO_SOURCE_SURFACE_ACTIVE_AFFINE_POINT_SELECTION_BOUNDARY_NOTE_2026-04-16.md`
  - `DM_NEUTRINO_SOURCE_SURFACE_ACTIVE_HALF_PLANE_THEOREM_NOTE_2026-04-16.md`
  - `DM_NEUTRINO_SOURCE_SURFACE_ACTIVE_PARITY_COMPATIBLE_DIAGONAL_BASELINE_THEOREM_NOTE_2026-04-17.md`
  - `DM_NEUTRINO_SOURCE_SURFACE_PARITY_COMPATIBLE_OBSERVABLE_SELECTOR_THEOREM_NOTE_2026-04-17.md`
  - `DM_NEUTRINO_SOURCE_SURFACE_ACTIVE_CURVATURE_23_SYMMETRIC_BASELINE_BOUNDARY_THEOREM_NOTE_2026-04-17.md`
  - `KOIDE_SELECTED_SLICE_FROZEN_BANK_DECOMPOSITION_NOTE_2026-04-18.md`
- **auditor confidence:** high

### `koide_z3_qubit_radian_bridge_no_go_note_2026-04-20`

- **Note:** [`KOIDE_Z3_QUBIT_RADIAN_BRIDGE_NO_GO_NOTE_2026-04-20.md`](../../docs/KOIDE_Z3_QUBIT_RADIAN_BRIDGE_NO_GO_NOTE_2026-04-20.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_conditional~~
- **effective_status:** ~~audited_conditional~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** Every retained radian on Cl(3)/Z_3 + d=3 is asserted to be a rational multiple of pi while 2/d^2 is a pure dimensionless rational, so P requires an extra radian bridge beyond the tested retained candidates.  _(class `C`)_
- **chain closes:** False — The runner verifies that the four named candidate closures fail, but the universal no-go depends on non-clean R1-R3 inputs and on an exhaustive classification of retained radians/dimensionless ratios that is asserted and finitely sampled rather than proved.
- **rationale:** Issue: the runner supports the diagnostic failures of candidates A-D, but the source promotes them to a retained universal no-go over all Cl(3)/Z_3 radian bridges; the exhaustive taxonomy that every retained angle is rational-times-pi and every retained count is dimensionless rational is not itself a retained theorem, and R1-R3 are non-clean. Why this blocks: a hostile reviewer can accept the four candidate failures while rejecting the stronger impossibility/minimal-input claim without an audited classification of all native angle-producing constructions. Repair target: audit-retain the Berry selected-line, bundle-obstruction, and circulant-character inputs, then add a theorem/runner that classifies all allowed retained angle and Plancherel constructions on the selected-line CP1 base; also fix the F9 summary table, which prints misleading 'matches 2/9?' labels despite correct PASS checks. Claim boundary until fixed: safely claim the runner-verified no-go for the four tested closures: per-Z3 PB gives pi/3, closed Bargmann gives pi, Pancharatnam midpoint gives pi/24, and Plancherel 2/d^2 is dimensionless; do not claim a retained exhaustive no-go for every possible Cl(3)/Z3 radian bridge.
- **open / conditional deps cited:**
  - `KOIDE_Q_DELTA_LINKING_RELATION_THEOREM_NOTE_2026-04-20.md`
  - `KOIDE_BERRY_PHASE_THEOREM_NOTE_2026-04-19.md`
  - `KOIDE_BERRY_BUNDLE_OBSTRUCTION_THEOREM_NOTE_2026-04-19.md`
  - `KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md`
  - `KOIDE_CYCLIC_WILSON_DESCENDANT_LAW_NOTE_2026-04-18.md`
  - `KOIDE_CIRCULANT_WILSON_TARGET_NOTE_2026-04-18.md`
  - `SCALAR_SELECTOR_CYCLE1_SCIENCE_REVIEW_NOTE_2026-04-19.md`
- **auditor confidence:** high

### `lattice_3d_dense_refinement_reconciliation_note`

- **Note:** [`LATTICE_3D_DENSE_REFINEMENT_RECONCILIATION_NOTE.md`](../../docs/LATTICE_3D_DENSE_REFINEMENT_RECONCILIATION_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_clean~~
- **effective_status:** **retained**  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** With corrected physical indexing and fixed physical connectivity, the ordered 3D dense spent-delay h=0.5 refinement point fails to preserve the older positive-refinement narrative: the barrier read remains mixed and the no-barrier distance companion has 0/5 hierarchy-aligned attractive rows.  _(class `C`)_
- **chain closes:** True — The named runner and archived log match the note: h=1.0 gives a mixed barrier read but 5/5 attractive no-barrier distance rows with b^(-0.94), while h=0.5 gives a mixed barrier read, no distance fit, and 0/5 attractive no-barrier distance rows. The runner verdict is explicitly FAILS for the older h=0.5 positive-refinement narrative.
- **rationale:** The negative reconciliation closes for the stated finite comparison: the live runner verifies the corrected h mapping, span=3 at h=1.0 and span=6 at h=0.5, the barrier-card summaries, the h=1.0 distance fit, the h=0.5 absence of positive hierarchy-aligned distance rows, and the final FAILS verdict for the older refinement-positive story. This clean audit ratifies only that corrected h=1.0 versus h=0.5 finite reconciliation; it does not promote a refinement theorem, continuum theorem, 4D result, action-power result, or a broad retained theorem for the ordered 3D dense branch.
- **auditor confidence:** high

### `lattice_3d_dense_spent_delay_note`

- **Note:** [`LATTICE_3D_DENSE_SPENT_DELAY_NOTE.md`](../../docs/LATTICE_3D_DENSE_SPENT_DELAY_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_failed~~
- **effective_status:** ~~audited_failed~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The gravity hierarchy confirms a real attractive window on the retained tested z = 2..6 range.  _(class `C`)_
- **chain closes:** False — The live runner reproduces the 10-property card for z=2..5, but it does not evaluate or print the note's claimed z=6 hierarchy endpoint, so the stated z=2..6 retained window is not supported by the runner output.
- **rationale:** Issue: the source note's load-bearing attractive-window claim includes z=6, but the named live runner and checked log only test z=2,3,4,5 and report hierarchy-aligned support as 4/4 points. Why this blocks: a hostile auditor cannot ratify a retained z=2..6 window when the allowed runner output omits one endpoint; the exact retained wording is stale relative to the executable artifact even though the z=2..5 card is reproducible. Repair target: update the runner to include z=6 with assertions for centroid, P_near, bias, and hierarchy sign, or revise the note's retained window and table to z=2..5; register the runner path in the audit ledger if this card remains load-bearing. Claim boundary until fixed: it is safe to claim the current runner's finite 3D dense spent-delay card: Born 7.39e-16, d_TV=0.3785, k=0 controls zero, F~M alpha about 0.34, nonzero MI/decoherence, N=12/15 positive centroid response after N=10 away, and hierarchy-aligned attraction at z=2..5; it is not safe to claim the z=2..6 window or any broader/asymptotic attraction theorem.
- **open / conditional deps cited:**
  - `z_equals_6_hierarchy_endpoint_missing_from_live_runner_and_log`
  - `runner_path_not_registered_in_audit_ledger`
  - `asymptotic_or_all_distance_attraction_theorem_not_provided`
- **auditor confidence:** high

### `lattice_3d_dense_window_extension_note`

- **Note:** [`LATTICE_3D_DENSE_WINDOW_EXTENSION_NOTE.md`](../../docs/LATTICE_3D_DENSE_WINDOW_EXTENSION_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_clean~~
- **effective_status:** **retained**  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** On the ordered 3D dense spent-delay family, the live sweep shows z = 2 through 6 remain attractive, z = 7 is mixed/signal-free, detector-window widening preserves z = 6's sign, and wider slit thresholds do not extend the window further.  _(class `C`)_
- **chain closes:** True — The live script reproduces the source table and decision on the same declared family, action, geometry, slit threshold, detector-window scan, and z range; the source keeps the conclusion bounded and does not promote an all-distance or new-action theorem.
- **rationale:** The source claim is a bounded computational extension, and the live artifact reproduces the canonical z sweep, detector-window sensitivity rows, slit-threshold spot checks, Born companion value, MI/decoherence values, and final bounded-extension decision. The conclusion is limited to the ordered 3D dense spent-delay family with the declared geometry and explicitly excludes all-distance, 4D, NN, and action-law claims, so the runner checks the load-bearing step without hidden promotion. Residual risk is only ordinary finite-sweep scope: this clean audit does not say anything beyond the tested family and parameter grid.
- **auditor confidence:** high

### `lattice_3d_nyquist_diffraction_note`

- **Note:** [`LATTICE_3D_NYQUIST_DIFFRACTION_NOTE.md`](../../docs/LATTICE_3D_NYQUIST_DIFFRACTION_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_clean~~
- **effective_status:** **retained**  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The first positive-to-negative gravity-side centroid flip tracks the lattice Nyquist scale pi/h at h = 0.5 and h = 0.25, with similar flip locations across field strengths, so the effect is a bounded discrete-lattice UV artifact rather than a continuum prediction.  _(class `C`)_
- **chain closes:** True — The live artifact reproduces the source's h = 0.5 and h = 0.25 flip tables, field-strength comparisons, mean flip ratios, and bounded safe read; the note explicitly excludes continuum and macroscopic-gravity claims.
- **rationale:** The source claim is a finite Nyquist probe, and the live script reproduces the first-flip values 6.199467 and 6.107077 at h = 0.5, 11.932917 and 12.085990 at h = 0.25, plus the reported mean/pi-over-h ratios. The interpretation is bounded to the retained ordered-lattice harness and explicitly says the flip is a lattice artifact in the continuum limit, not a low-energy gravity law. Residual risk is limited to the declared coarse k grid and two tested h values; the audited claim should not be widened beyond that finite probe.
- **auditor confidence:** high

### `lattice_3d_tapered_refinement_note`

- **Note:** [`LATTICE_3D_TAPERED_REFINEMENT_NOTE.md`](../../docs/LATTICE_3D_TAPERED_REFINEMENT_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_clean~~
- **effective_status:** **retained**  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The y-only tapered 3D branch preserves Born and k=0 controls and improves MI/decoherence under h = 0.5 refinement, but all gravity hierarchy observables remain AWAY and there is no positive distance-law support.  _(class `C`)_
- **chain closes:** True — The live artifact reproduces the h = 1.0 and h = 0.5 table values and the negative refinement conclusion on the declared y-only tapered topology branch; the source explicitly avoids claiming dense-branch rescue or a positive distance-law theorem.
- **rationale:** The source is a bounded negative topology-branch card, and the live script reproduces its Born, k=0, MI, d_TV, decoherence, gravity-hierarchy, and distance-support values at h = 1.0 and h = 0.5. The note's retained read is appropriately limited: the tapered branch is a real tested topology branch and a useful negative control, not a hierarchy-clean attraction result, dense-branch rescue, distance-law branch, or promoted refinement theorem. Residual risk is only the ordinary finite-harness scope of the two tested spacings.
- **auditor confidence:** high

### `lattice_complementarity_note`

- **Note:** [`LATTICE_COMPLEMENTARITY_NOTE.md`](../../docs/LATTICE_COMPLEMENTARITY_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_conditional~~
- **effective_status:** ~~audited_conditional~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The ordered lattice supports a continuous tradeoff between decoherence/which-slit structure and distance-law quality, with a bounded sweet spot where both are simultaneously present.  _(class `C`)_
- **chain closes:** False — The runner reproduces the finite canonical sweep, but the promoted complementarity claim depends on selected proxy observables, the chosen sweet-spot guard, and a Born check on a same-family companion aperture rather than the same two-slit card.
- **rationale:** Issue: the note promotes a bounded complementarity sweet spot from a finite N=40, half_width=20 slit-gap sweep with chosen centroid, mass-placement, distance-fit, and threshold guards, while Born cleanliness is checked only on a same-family companion aperture. Why this blocks: those choices demonstrate an internally reproducible scenario, but they do not by themselves establish a retained lattice complementarity theorem or same-card coexistence of Born, which-slit/decoherence, distance-law quality, and attractive gravity. Repair target: provide a theorem or registered runner proving the observable/readout and guard selection from retained primitives, and compute Born plus the distance-law/decoherence observables on the same aperture card or explicitly prove the companion-aperture transfer. Claim boundary until fixed: the current runner safely supports the reported canonical finite sweep, the monotone MI/d_TV rise, the R^2 degradation, the gap=2 thresholded sweet-spot row, clean companion Born residuals, zero k=0 response, and away-signed same-card gravity.
- **auditor confidence:** high

### `lattice_distance_law_note`

- **Note:** [`LATTICE_DISTANCE_LAW_NOTE.md`](../../docs/LATTICE_DISTANCE_LAW_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_clean~~
- **effective_status:** **retained**  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** On the ordered 2D no-barrier lattice with N=40 and half-width 20, the detector-centroid magnitude follows |delta| ~= 23.5071*b^(-1.052) with R^2=0.9850 on the far-field window b>=7, while the k=0 control is zero.  _(class `C`)_
- **chain closes:** True — The named no-barrier runner and archived log reproduce the saved b rows, the k=0 zero control, and the far-field power-law fit. The note explicitly limits the claim to |delta| on the no-barrier ordered-lattice harness and excludes a signed attractive deflection law, the barrier geometry, and the mirror/random-connected family.
- **rationale:** The finite ordered-lattice distance-magnitude claim closes on its own terms: the live runner exactly reproduces the seven b rows, k=0 gives +0.000000e+00, and the b>=7 fit is |delta| ~= 23.5071*b^(-1.052) with R^2=0.9850. This clean audit ratifies only the N=40, half-width-20, no-barrier ordered-lattice magnitude law and its stated scope limits; it does not ratify a signed attractive law, a barrier-harness law, a continuum theorem, or a rescue of the random-connected mirror-family distance claim.
- **auditor confidence:** high

### `lattice_kernel_transfer_norm_note`

- **Note:** [`LATTICE_KERNEL_TRANSFER_NORM_NOTE.md`](../../docs/LATTICE_KERNEL_TRANSFER_NORM_NOTE.md)
- **current_status:** _proposed_promoted_
- **audit_status:** ~~audited_failed~~
- **effective_status:** ~~audited_failed~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The local 3D transfer-norm probe reports that, after h^2 measure normalization over h=1.0,0.5,0.25,0.125, p=1.5 is closest to marginality and p=2.0 still drifts; the source note explicitly says this is a bounded discrimination probe, not a proposed_promoted branch claim.  _(class `C`)_
- **chain closes:** False — The named runner reproduces the finite transfer-norm ranking when invoked with the h=0.125 argument used by the archived log, but the audit queue row is proposed_promoted even though the source status line explicitly disclaims a proposed_promoted branch claim. The script itself is a local kernel-only discrimination harness and does not run same-harness propagation or prove a continuum kernel power.
- **rationale:** Issue: the audit target is classified as proposed_promoted, but the source note states that this is a bounded discrimination probe and not a proposed_promoted branch claim. Why this blocks: a local outgoing transfer norm over four h values can warn that p=2.0 is not singled out, but it does not establish a promoted 3D kernel branch, a continuum limit, or same-harness propagation behavior; treating this note as a promoted branch would contradict the note's own scope. Repair target: revise the Status line so the queue does not parse this as proposed_promoted, or create a separate promotion note with a registered runner that proves the selected kernel power on same-harness propagation, Born/controls, refinement, and continuum criteria. Claim boundary until fixed: it is safe to claim only the finite local discriminator: with h^2 normalization and h={1.0,0.5,0.25,0.125}, p=1.5 has measured slope +0.102, p=2.0 has -0.204, p=2.5 has -0.598, and p=3.0 has -1.046; this is a warning signal, not a promoted law.
- **open / conditional deps cited:**
  - `source_status_explicitly_says_not_a_proposed_promoted_branch_claim`
  - `local_transfer_norm_not_same_harness_propagation_or_continuum_proof`
  - `runner_default_h_values_do_not_include_h_0_125_without_explicit_arguments`
- **auditor confidence:** high

### `lattice_nn_distance_law_note`

- **Note:** [`LATTICE_NN_DISTANCE_LAW_NOTE.md`](../../docs/LATTICE_NN_DISTANCE_LAW_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_conditional~~
- **effective_status:** ~~audited_conditional~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** On the raw NN barrier harness, fixed strength gives positive far-field distance-law signal at h = 0.5 and h = 0.25 with slopes -0.966 and -0.929, while alpha = 1.5 preserves the sign but flattens the decay.  _(class `C`)_
- **chain closes:** False — The live distance-law script reproduces the note's far-field rows and fits, but the proposed-retained framing depends on the upstream Born-clean NN continuum note, which is unaudited/unknown, and the distance runner does not verify those Born/k=0 controls.
- **rationale:** Issue: the source's live distance-law numbers reproduce, but the retained claim is explicitly on a refinement path inherited from an upstream Born-clean NN branch whose note is not audit-clean; the archived logs named by the source are also absent from this worktree, and the distance runner does not check Born or k=0. Why this blocks: a meaningful far-field distance-law fit cannot be promoted as a retained Born-safe refinement-path result until the upstream refinement controls are independently retained or included in the same runner. Repair target: audit-retain LATTICE_NN_CONTINUUM_NOTE.md or extend this runner to recompute the Born/k=0/MI/decoherence controls for the same h values and restore/register the archived logs if they remain part of the artifact chain. Claim boundary until fixed: safely claim the live runner's finite barrier-harness table: fixed strength has positive far-field signal at h=0.5 and h=0.25 with slopes near -1, alpha=1.5 keeps the far-field sign but flattens the exponent, and near-field/coarse-sign behavior remains mixed.
- **open / conditional deps cited:**
  - `LATTICE_NN_CONTINUUM_NOTE.md`
- **auditor confidence:** high

### `lattice_nn_light_cone_note`

- **Note:** [`LATTICE_NN_LIGHT_CONE_NOTE.md`](../../docs/LATTICE_NN_LIGHT_CONE_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_renaming~~
- **effective_status:** ~~audited_renaming~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The NN light-cone branch is frozen as a topological causal-bound statement: influence is confined to the relevant forward causal neighborhood in the graph/DAG sense, with no emergent-relativity or physical spacetime light-cone claim retained.  _(class `F`)_
- **chain closes:** False — After the explicit retirement of the emergent-relativity claim, the remaining proposed-retained content is a relabeling of directed-graph forward reachability; the note has no separate NN light-cone runner/log and one named fixed-mass log is absent.
- **rationale:** Issue: the note correctly demotes the physical light-cone/emergent-relativity interpretation, but the only proposed-retained residue is the statement that the NN/DAG branch has a topological forward causal neighborhood. Why this blocks: that is a graph-reachability label, not an independent retained light-cone theorem, and the cited fixed-mass verification log is missing while the causal-field script itself is marked retracted for distance-law purposes. Repair target: either keep this as an administrative branch-freeze/support note, or add a theorem and runner that defines the graph causal cone from the propagation operator and verifies finite-support/reachability claims without using relativistic language. Claim boundary until fixed: safely claim that emergent relativity, Lorentz invariance, physical spacetime light-cone, and universal speed-law readings are not retained; the NN harness only has a topological DAG forward-reachability bound.
- **open / conditional deps cited:**
  - `SESSION_SUMMARY_2026-04-01_DIMENSIONAL.md`
  - `work_history/repo/backlog/OVERNIGHT_WORK_BACKLOG.md`
- **auditor confidence:** high

### `lattice_nn_mass_response_note`

- **Note:** [`LATTICE_NN_MASS_RESPONSE_NOTE.md`](../../docs/LATTICE_NN_MASS_RESPONSE_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_clean~~
- **effective_status:** **retained**  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The NN fixed-node field-strength mass-response table stays positive on the deterministic Born-safe refinement path after h = 0.5, and the alpha-scaled probe makes the h = 0.5 to h = 0.25 response less spacing-sensitive without promoting F proportional to M.  _(class `C`)_
- **chain closes:** True — The live mass-response script recomputes the deterministic refinement table, Born values, alpha-scaled gravity rows, and Born spot-check from the canonical harnesses; the note keeps the conclusion bounded and explicitly rejects an F proportional to M continuum claim.
- **rationale:** The live runner reproduces the source table: deterministic h = 1.0 through 0.0625 has machine-precision Born values, MI and d_TV rising toward 1, and positive gravity after h = 0.5 while shrinking toward zero. It also reproduces the alpha-scaled probe, where alpha = 1.0 and 1.5 are less spacing-sensitive and remain Born-clean on the checked rows. The source does not overstate this as F proportional to M or a continuum theorem, so the finite bounded mass-response claim closes; the missing archived log is a reproducibility hygiene issue, not a blocker because the live runner reproduces the artifact.
- **auditor confidence:** high

### `lattice_synthesis_guard_note`

- **Note:** [`LATTICE_SYNTHESIS_GUARD_NOTE.md`](../../docs/LATTICE_SYNTHESIS_GUARD_NOTE.md)
- **current_status:** _proposed_promoted_
- **audit_status:** ~~audited_failed~~
- **effective_status:** ~~audited_failed~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The note says the NN refinement branch is a bounded bridge and explicitly not a proposed_promoted continuum theorem; further promotion requires a canonical NN refinement/RG artifact chain.  _(class `B`)_
- **chain closes:** False — The queued proposed_promoted status is a parser false positive from the phrase 'not a proposed_promoted continuum theorem'; the note itself is a conservative synthesis guard, has no runner, and cites UNIFIED_PROGRAM_NOTE.md, whose effective status is audited_failed.
- **rationale:** Issue: the source explicitly disclaims the promoted-continuum claim that caused it to enter the proposed_promoted queue, and it provides no independent runner or artifact chain for a project-level promotion. Why this blocks: an audit cannot ratify a promoted claim that the source itself says is not being made, especially when the cited synthesis note is effective audited_failed and the underlying lattice/NN branches remain bounded or conditional. Repair target: change the status text so the audit parser does not classify this guard note as proposed_promoted, and promote only after the NN refinement/RG chain has audit-clean artifact-backed notes. Claim boundary until fixed: safely claim this as conservative synthesis guidance: mirror remains flagship, ordered lattice is a secondary bounded branch, NN refinement is a promising bounded bridge, and no blanket one-family or continuum lattice theorem is retained.
- **open / conditional deps cited:**
  - `UNIFIED_PROGRAM_NOTE.md`
- **auditor confidence:** high

### `lattice_weak_field_mass_scaling_note`

- **Note:** [`LATTICE_WEAK_FIELD_MASS_SCALING_NOTE.md`](../../docs/LATTICE_WEAK_FIELD_MASS_SCALING_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_clean~~
- **effective_status:** **retained**  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** On the ordered 2D weak-field pocket, the fixed-node field-strength sweep stays Born-clean, k=0-clean, MI/decoherence-positive, and gravity-positive across all six strengths, with gravity = 2.6960 * strength^0.353 and R^2 = 0.971, so the response is positive but sub-linear rather than F proportional to M.  _(class `C`)_
- **chain closes:** True — The live artifact reproduces the mass-proxy sweep, canonical row, tail fit, power-law fit, retention counts, and bounded sub-linear decision on the declared weak-field ordered-lattice pocket.
- **rationale:** The runner recomputes the load-bearing sweep: all six field-strength rows are Born-clean at 4.24e-16, k=0 is zero, MI/decoherence remain nontrivial, gravity is positive, and each row is retained by the script's criteria. The fitted response exponent is 0.353 with R^2 = 0.971, and the source correctly treats that as a bounded sub-linear mass response rather than promoting F proportional to M or a one-card lattice unification theorem. Residual risk is limited to the declared weak-field pocket and fixed-node field-strength mass proxy.
- **auditor confidence:** high

### `lattice_weak_field_purity_scaling_note`

- **Note:** [`LATTICE_WEAK_FIELD_PURITY_SCALING_NOTE.md`](../../docs/LATTICE_WEAK_FIELD_PURITY_SCALING_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_clean~~
- **effective_status:** **retained**  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** On the weak-field ordered-lattice pocket, the retained N = 30 through 100 rows are Born-clean, k=0-clean, MI/decoherence-positive, and gravity-positive, and fit 1 - pur_cl ~= 1.0467 * N^-0.222 with R^2 = 0.9683.  _(class `C`)_
- **chain closes:** True — The live artifact reproduces the N sweep, canonical N=40 row, retained/all-row purity fits, retention counts, and bounded retained-window interpretation from the source note.
- **rationale:** The runner recomputes the load-bearing table: N=30 through 100 are retained, all seven rows are Born-clean and positive-gravity, and the retained-row purity-complement fit matches the source coefficient, exponent, and R^2. The note correctly treats the result as a bounded scaling law on the tested weak-field pocket, with N=20 excluded and no universal/asymptotic lattice theorem claimed. The runner's final 'PROMOTED' line is clean only under that bounded retained-window meaning.
- **auditor confidence:** high

### `lensing_adjoint_kernel_reduced_model_note`

- **Note:** [`LENSING_ADJOINT_KERNEL_REDUCED_MODEL_NOTE.md`](../../docs/LENSING_ADJOINT_KERNEL_REDUCED_MODEL_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_clean~~
- **effective_status:** **retained**  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The one-term-per-layer reduction fails badly while the exact edge replay matches the first-order observable at the stated H=0.35 setup.  _(class `C`)_
- **chain closes:** True — The source makes only a bounded negative claim about the first reduced surrogate. The live H=0.35 runner reproduces the archived exact-edge/full-harness spot-check and the layer_signed/layer_abs failures against the exact edge series, with no cited dependencies needed.
- **rationale:** The retained content is a bounded negative inside the stated harness, not a derivation of the reference lensing slope or a continuum physics claim. The live runner with --h 0.35 reproduces true_kubo=+5.972756 and exact_edge=+5.972756 at b=3 with |Delta|=4.228e-13, then shows the signed and absolute one-term-per-layer reductions miss the b=3..6 exact-edge series by about 98-100%. Because the note explicitly keeps the exact edge factorization as the reference object and rejects only the first reduced surrogate, the claim closes on its own terms.
- **auditor confidence:** high

### `lensing_beta_sweep_note`

- **Note:** [`LENSING_BETA_SWEEP_NOTE.md`](../../docs/LENSING_BETA_SWEEP_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_conditional~~
- **effective_status:** ~~audited_conditional~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The note asserts that beta=5 at H=0.5 is an isolated near-1/b coarse-grid spike because beta=7 and beta=10 leave it and the beta=5 refinement at H=0.35 flips sign with slope -0.7930.  _(class `C`)_
- **chain closes:** False — The falsification depends on numerical sweep/refinement tables, but the ledger has no registered primary runner or output and the note gives only absolute local artifact paths.
- **rationale:** Issue: the proposed_retained negative rests on a beta sweep and H-refinement numerical battery, but the audit ledger registers no primary runner/output, and the source note's artifacts are absolute local paths outside the audit packet. Why this blocks: a hostile auditor cannot reproduce the key beta=5 coarse slope, the beta=7/10 sign/shape departures, or the H=0.35 sign flip/slope -0.7930 from registered evidence; the result is also scoped to Fam1 b={3,4,5,6} and does not register the adjoint-kernel authority it uses for interpretation. Repair target: register scripts/lensing_beta_sweep.py and the deterministic log as primary evidence, add explicit PASS thresholds for slopes/sign patterns/shape spread, extend or explicitly bound the beta-neighborhood and H-refinement checks, and register the adjoint-kernel note if it remains interpretive support. Claim boundary until fixed: it is safe to say the source note reports a conditional numerical negative that the beta=5 coarse-grid near-1/b point did not survive nearby beta checks or one H=0.35 refinement; it is not yet an audited retained closure of the narrow-beam/ray-optics rescue.
- **open / conditional deps cited:**
  - `scripts/lensing_beta_sweep.py_not_registered_primary_runner`
  - `logs/2026-04-08-lensing-beta-sweep.txt_not_registered_primary_output`
  - `LENSING_ADJOINT_KERNEL_NOTE.md_not_registered_one_hop`
  - `multi_family_or_broader_H_refinement_not_registered`
- **auditor confidence:** high

### `lensing_deflection_note`

- **Note:** [`LENSING_DEFLECTION_NOTE.md`](../../docs/LENSING_DEFLECTION_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_conditional~~
- **effective_status:** ~~audited_conditional~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** At H=0.25 on b in {3,4,5,6}, kubo_true(b) follows a clean power law with slope about -1.43 and R^2 = 0.998, so the retained gravity-side result is a non-standard power law rather than Newton/Einstein 1/b lensing.  _(class `C`)_
- **chain closes:** False — The claim rests on numerical lensing sweeps, fine single-b runs, and combined log-log fits, but the ledger registers no primary runner or runner output. The quoted slopes, R^2 values, H-refinement drift, and b=3 reference match cannot be reproduced from the audit packet.
- **rationale:** Issue: the retained partial positive depends on a numerical Lane L/L+ sweep -- H=0.25 fine b in {3,4,5,6}, kubo_true slope -1.4335, dM slope -1.5162, R^2 near 0.998/0.995, and a b=3 match to the Lane-alpha reference -- but the ledger runner_path is null even though the note names multiple scripts and logs. Why this blocks: without a registered deterministic runner and output, a hostile auditor cannot verify the grown-DAG setup, b/H sampling, OOM workaround, fit subset choices, Kubo/finite-difference agreement, reference-point comparison, or the downgrade from 1/b to a steeper non-standard exponent. Repair target: register the primary lensing-deflection runner or a deterministic L+ aggregate runner, include the fine-single outputs and combined-analysis log as primary outputs, and make the runner assert the per-b table, slope/R^2 fits, H-drift table, b=3 reference agreement, and the failure of the -1 exponent under explicit thresholds. Claim boundary until fixed: it is safe to say the source note reports a conditional non-standard power-law signal in the tested Fam1 lensing harness and downgrades the old 1/b headline; it is not yet an audited retained gravity-side functional-form theorem or continuum-stable lensing prediction.
- **open / conditional deps cited:**
  - `scripts/lensing_deflection_sweep.py_not_registered_primary_runner`
  - `scripts/lensing_deflection_fine_single.py_not_registered_primary_runner`
  - `scripts/lensing_deflection_lane_lplus.py_not_registered_primary_runner`
  - `logs/2026-04-07-lensing-deflection-sweep.txt_not_registered_primary_output`
  - `logs/2026-04-07-lensing-fine-asymptotic.txt_not_registered_primary_output`
  - `logs/2026-04-07-lensing-deflection-lane-lplus.txt_not_registered_primary_output`
- **auditor confidence:** high

### `lensing_k_sweep_note`

- **Note:** [`LENSING_K_SWEEP_NOTE.md`](../../docs/LENSING_K_SWEEP_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_conditional~~
- **effective_status:** ~~audited_conditional~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The note asserts that the mean lensing slope varies from +0.58 to about -1.43 across k*H values, with sign flips at k*H=0.5 and 5.0, so the earlier -1.40 slope at k*H=2.5 is configuration-specific rather than a geometric invariant.  _(class `C`)_
- **chain closes:** False — The diagnostic depends on numerical k-sweep tables and an eikonal comparison, but the ledger has no registered primary runner/output and no one-hop dependency for the eikonal/mechanism interpretation.
- **rationale:** Issue: the proposed_retained diagnostic rests on a numerical k-sweep over one Fam1 setup with three seeds per k*H value, but the audit ledger registers no primary runner/output for scripts/lensing_k_sweep.py or its log. Why this blocks: a hostile auditor cannot reproduce the reported slope range, sign flips, R^2 ranges, seed spread, or eikonal-gap oscillation from registered evidence; additionally, the inference that the correction is a wave-interference mechanism is stronger than the table alone unless supported by registered kernel/mode analysis. Repair target: register the k-sweep runner and deterministic output with PASS thresholds for slopes/signs/seed spread, register the eikonal baseline and adjoint-kernel/mode analysis used to infer mechanism, and extend or explicitly bound family/H/b-range coverage. Claim boundary until fixed: it is safe to say the source note reports a conditional numerical diagnostic that the reference k*H=2.5 slope is not invariant within the tested sweep; it is not yet an audited retained theorem that lensing is a k-dependent wave-interference phenomenon.
- **open / conditional deps cited:**
  - `scripts/lensing_k_sweep.py_not_registered_primary_runner`
  - `logs/2026-04-09-lensing-k-sweep.txt_not_registered_primary_output`
  - `eikonal_baseline_not_registered_one_hop`
  - `kernel_or_mode_interference_analysis_not_registered`
- **auditor confidence:** high

### `linear_response_derivation_note`

- **Note:** [`LINEAR_RESPONSE_DERIVATION_NOTE.md`](../../docs/LINEAR_RESPONSE_DERIVATION_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_conditional~~
- **effective_status:** ~~audited_conditional~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The first-moment Kubo predictor is defined as cz_weighted_by_1/|z-z_src| - cz_free and treated as a no-fit, derivation-adjacent predictor for measured d(cz)/ds across 44 families.  _(class `C`)_
- **chain closes:** False — The live runner reproduces the reported correlations and sign agreement, but the note itself says this detector-only reweighting is not the literal first-order Kubo term <z*deltaH>_0 and omits the edge action perturbation and path-phase cross terms.
- **rationale:** Issue: The source elevates a detector-only |amp|^2/|z-z_src| reweighting into a proposed-retained first-moment Kubo/first-principles predictor while explicitly admitting it is not the literal first-order Kubo expression <z*deltaH>_0. Why this blocks: the replayed r=0.5605 overall, r=0.7248 off-scaffold, and 36/44 sign agreement establish a no-fit heuristic correlation, but they do not derive the predictor from the propagator plus action or include the missing deltaH=kL delta f edge/path-phase terms. Repair target: provide a symbolic or numerical true-Kubo derivation that differentiates the path-sum at s=0, includes the edge action perturbation and phase cross-terms, and compares that literal first-order observable on the same 44-family set. Claim boundary until fixed: it is safe to claim the archived/live heuristic replay gives r=0.56 overall, r=0.72 off-scaffold, 81.8% no-fit sign agreement, and a 79.5% in-sample tuned threshold result; it is not yet safe to claim a retained derivation-grade or literal first-order Kubo predictor from this note alone.
- **auditor confidence:** high

### `linear_response_second_order_kubo_note`

- **Note:** [`LINEAR_RESPONSE_SECOND_ORDER_KUBO_NOTE.md`](../../docs/LINEAR_RESPONSE_SECOND_ORDER_KUBO_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_conditional~~
- **effective_status:** ~~audited_conditional~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** Adding the second-order term 1/2*kubo2*s^2 does not increase the strict linearity-regime subset and slightly worsens the aggregate residual at s=0.008 in the 44-family replay.  _(class `C`)_
- **chain closes:** False — The live runner reproduces the second-order null result, but the note extrapolates that finite computation into a boundary claim about the Taylor-expansion approach and higher Taylor orders without a convergence/no-go theorem.
- **rationale:** Issue: The runner verifies that the specific second-order correction does not improve the 44-family battery, but the note also claims a broader boundary of the Kubo-Taylor approach and says the failing nonlinearities are not fixed by more Taylor terms at s=0. Why this blocks: a second-order replay cannot rule out third or higher orders, prove non-analyticity, or establish that all Taylor expansions around s=0 fail for the structural families. Repair target: either narrow the source claim to the computed second-order null result, or add a theorem/computation bounding the Taylor remainder or demonstrating non-convergence/non-analyticity for the failing families, with the first-order and range-of-validity inputs explicitly audited. Claim boundary until fixed: it is safe to claim the live artifact reproduces +0 growth in the linearity-regime subset (15/44 to 15/44), sum |residual| worsening from 5.6090 to 5.7221 at s=0.008, and the listed per-family second-order pathologies; it is not safe to claim a retained no-go for all higher Taylor terms from this note alone.
- **auditor confidence:** high

### `linear_response_true_kubo_note`

- **Note:** [`LINEAR_RESPONSE_TRUE_KUBO_NOTE.md`](../../docs/LINEAR_RESPONSE_TRUE_KUBO_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_conditional~~
- **effective_status:** ~~audited_conditional~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The first-order recurrence gives d(cz)/ds = (1/T) sum_j (z_j - cz_free) 2 Re[A_j* B_j], and the note asserts that this derivative matches measured finite-difference responses across 44 families with r=0.9716 overall, r=0.9995 off-scaffold, and 42/44 sign agreement.  _(class `A`)_
- **chain closes:** False — The algebraic first-order recurrence can be read from the note, but the empirical 44-family finite-difference comparison is not reproducible from registered audit evidence because the ledger has no primary runner or runner output for this claim.
- **rationale:** Issue: the source note gives a plausible first-order derivative recurrence for the specified propagator and field, but the retained claim rests on a 44-family empirical finite-difference comparison and sign-agreement battery for which the audit packet has no registered primary runner, deterministic output, or ledger-recognized log. The note names scripts/linear_response_true_kubo.py and a log, but the ledger/queue runner_path is null, so those artifacts are not available as the registered primary evidence for this audit. Why this blocks the claim: Nature-grade retention requires the stated r=0.9716 overall, r=0.9995 off-scaffold, 42/44 sign agreement, and edge-case corrections to be reproducible from registered evidence; the analytic recurrence alone does not verify that the implementation computed the same derivative, used the claimed 44 families, compared against the finite-difference battery correctly, or supports the broad compact-principle interpretation. Repair target: register scripts/linear_response_true_kubo.py as the claim's primary runner, include or regenerate the deterministic 44-family dataset/log, and make the runner independently check both the recurrence derivative and the finite-difference comparison with exact thresholds for the reported correlations, sign counts, scaffold exclusions, and residual sign cases. Claim boundary until fixed: it is safe to claim a conditional first-order response formula for the specified propagator/field, subject to the derivation assumptions in the note; the 44-family correlation/sign-agreement result is unratified numerical support, not a retained physical theorem or retained compact-principle explanation.
- **open / conditional deps cited:**
  - `runner_not_registered_for_linear_response_true_kubo_note`
  - `logs/2026-04-07-linear-response-true-kubo.txt_not_registered_primary_output`
- **auditor confidence:** high

### `local_zsym_predictor_note`

- **Note:** [`LOCAL_ZSYM_PREDICTOR_NOTE.md`](../../docs/LOCAL_ZSYM_PREDICTOR_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_conditional~~
- **effective_status:** ~~audited_conditional~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** Adding local_z_asym to the 3-property classifier search is rejected on the swept set and leaves cross-generator accuracy unchanged at 6/9, so the note concludes that the simple node-level classifier line is exhausted.  _(class `C`)_
- **chain closes:** False — The live runner reproduces the finite local_z_asym negative exactly, but it tests one added node-level metric inside a fixed 3-property AND search; that does not prove the broader exhaustion of simple classifiers or all node-level metrics.
- **rationale:** Issue: the runner supports rejecting local_z_asym as the missing third predictor, but the source promotes that finite rejection to closure of the simple-classifier line of attack. Why this blocks: a hostile physicist can verify the distributions, the vacuous z_sym >= 0 third clause, and unchanged 6/9 cross-generator accuracy, but cannot infer an exhaustive no-go over other node-level metrics, thresholds, Boolean forms, multi-metric rules, or global path/spectral summaries from this one 3-property AND search. Repair target: either narrow the note to the local_z_asym negative, or add an exhaustive classifier-search theorem/computation specifying the metric universe, Boolean grammar, train/held-out protocol, and multiple-testing control that rules out the claimed simple-classifier class. Claim boundary until fixed: it is safe to claim that local_z_asym fails to improve the frozen classifier program on the 26-family swept set and nine independent generators; it is not safe to claim theorem-grade exhaustion of simple classifiers.
- **open / conditional deps cited:**
  - `simple_classifier_exhaustion_theorem_missing`
  - `metric_universe_for_node_level_classifier_search_not_defined`
  - `only_local_z_asym_added_to_fixed_3_property_AND_search`
  - `no_multiple_testing_or_global_search_certificate`
- **auditor confidence:** high

### `localized_source_response_sweep_note`

- **Note:** [`LOCALIZED_SOURCE_RESPONSE_SWEEP_NOTE.md`](../../docs/LOCALIZED_SOURCE_RESPONSE_SWEEP_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_failed~~
- **effective_status:** ~~audited_failed~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The live sweep shows no smaller source-response family beats the broad topN=196 control under the stated support/capture floors on the single h=0.25 ordered-lattice setup.  _(class `C`)_
- **chain closes:** False — The bounded numerical result closes, but the audit row is a parser false positive: the source Status line declares a bounded sweep on a proposed_retained family, not a proposed_retained claim.
- **rationale:** Issue: The audit queue treats this note as proposed_retained because the Status line says it is a bounded sweep on the proposed_retained 3D h=0.25 family, but the note's actual claim is explicitly bounded and negative. Why this blocks: the audit lane cannot ratify a retained claim that the source note does not make; doing so would promote a single-family source-response control sweep into retained physics. Repair target: rewrite the Status line so the parser records this as bounded/proposed_bounded, or author a separate proposed_retained theorem with a load-bearing derivation beyond this single h=0.25 sweep. Claim boundary until fixed: it is safe to claim the live artifact reproduces the bounded result that topN=169 remains admissible but does not beat broad topN=196, and that localized persistent-inertial response remains open; it is not safe to present this note as a retained source-response theorem.
- **auditor confidence:** high

### `matter_inertial_closure_note`

- **Note:** [`MATTER_INERTIAL_CLOSURE_NOTE.md`](../../docs/MATTER_INERTIAL_CLOSURE_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_conditional~~
- **effective_status:** ~~audited_conditional~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** Gaussian packets under the same uniform linear force give Newton-linear delta_z(g) per packet but equivalence-principle slopes differing by 123% across packets, so generator-invariant inertial mass fails at the persistent-object level.  _(class `C`)_
- **chain closes:** False — The retained negative depends on numerical packet-propagator measurements, but the audit ledger registers no primary runner or runner output for this claim. The source note's quoted slopes, R^2 values, spread ratios, and family-portability numbers are therefore not reproducible from the audit packet.
- **rationale:** Issue: the source note reports a concrete numerical negative for Gaussian-packet matter closure, but the load-bearing values -- slopes -73.5, -7.05, -18.3; R^2 > 0.96; 123% slope spread; persistence ratios; and Fam1/2/3 portability -- are backed only by an artifact chain named in the note, while the ledger runner_path is null. Why this blocks: a Nature-grade audit cannot verify that the same grown-DAG propagator, packet definitions, force coupling, baseline subtraction, and slope fits produced the quoted failure; the qualitative 'fields but no matter' conclusion depends on those exact computations rather than on an analytic theorem in the note. Repair target: register scripts/matter_inertial_closure.py as the primary runner, preserve or regenerate logs/2026-04-07-matter-inertial-closure.txt, and make the runner assert the null response, per-packet R^2 thresholds, slope table, 123% equivalence failure metric, persistence ratios, and Fam1/2/3 portability thresholds deterministically. Claim boundary until fixed: it is safe to say that the source note reports a conditional negative for the specific Gaussian-packet plus uniform-linear-force closure attempt; it is not yet an audited retained theorem that the grown-DAG propagator lacks generator-invariant inertial mass, and it does not exclude other persistent-object definitions or modified actions.
- **open / conditional deps cited:**
  - `scripts/matter_inertial_closure.py_not_registered_primary_runner`
  - `logs/2026-04-07-matter-inertial-closure.txt_not_registered_primary_output`
- **auditor confidence:** high

### `mesoscopic_surrogate_annular_tapered_sweep_note`

- **Note:** [`MESOSCOPIC_SURROGATE_ANNULAR_TAPERED_SWEEP_NOTE.md`](../../docs/MESOSCOPIC_SURROGATE_ANNULAR_TAPERED_SWEEP_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_failed~~
- **effective_status:** ~~audited_failed~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The bounded sweep shows annular, hollow-square, and tapered localized source families do not beat the admissible topN source-control frontier under the stated support/capture floors.  _(class `C`)_
- **chain closes:** False — The bounded negative conclusion is reproduced, but the audit row is a parser false positive: the source Status declares a bounded localization sweep on a proposed_retained surrogate family, not a proposed_retained claim. The live runner also reports a different topN tie representative than the frozen note while preserving the same frontier conclusion.
- **rationale:** Issue: The source note is explicitly a bounded localization sweep, but the queue records it as proposed_retained because the Status line mentions the proposed_retained 3D mesoscopic surrogate family being tested. The current runner also returns topN 121 as the best overall tie representative, while the note names topN 225; this does not change the frontier result but makes the frozen row stale at the exact-row level. Why this blocks: a retained audit cannot ratify a bounded single-family control sweep, and the exact frozen best-row statement is not current with the runner. Repair target: rewrite the Status line so the parser records bounded/proposed_bounded status and update the note/log or tie-break rule for the topN best-row representative; a retained theorem would need a derivation beyond this finite sweep. Claim boundary until fixed: it is safe to claim the live artifact reproduces that no non-degenerate annular, hollow-square, or tapered family beats the admissible topN frontier under the floors; it is not safe to present this as a retained localization theorem or to rely on the stale topN 225 best-row wording without qualification.
- **auditor confidence:** high

### `mesoscopic_surrogate_compact_floor_sweep_note`

- **Note:** [`MESOSCOPIC_SURROGATE_COMPACT_FLOOR_SWEEP_NOTE.md`](../../docs/MESOSCOPIC_SURROGATE_COMPACT_FLOOR_SWEEP_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_failed~~
- **effective_status:** ~~audited_failed~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The compact-floor sweep shows compact Gaussian and tapered candidates can pass the floors, but the best compact survivor does not meaningfully improve on the broad topN benchmark under the same support/capture constraints.  _(class `C`)_
- **chain closes:** False — The finite negative control-sweep result closes numerically, but the audit row is a parser/status false positive: the source describes a constrained sweep for a proposed_retained lane, not a proposed_retained theorem.
- **rationale:** Issue: The queue records this as proposed_retained because the Status line mentions the proposed_retained 3D surrogate lane, while the note itself is a narrow constrained compact-family control sweep. Why this blocks: a finite h=0.5 ordered-lattice comparison cannot be ratified as a retained theorem merely because it informs a proposed_retained lane; promoting it would inflate bounded provenance into retained physics. Repair target: rewrite the Status/current_status as bounded or proposed_bounded, or author a separate retained theorem deriving the compact-source frontier beyond this finite sweep. Claim boundary until fixed: it is safe to claim the live artifact reproduces topN 49 with capture2=1.000, score=0.9994, best compact tapered radius 2 with capture2=0.638, score=1.0000, and meaningful improvement over topN=False; it is not safe to present this note as a retained compact-source theorem.
- **auditor confidence:** high

### `mesoscopic_surrogate_h025_constrained_localization_note`

- **Note:** [`MESOSCOPIC_SURROGATE_H025_CONSTRAINED_LOCALIZATION_NOTE.md`](../../docs/MESOSCOPIC_SURROGATE_H025_CONSTRAINED_LOCALIZATION_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_failed~~
- **effective_status:** ~~audited_failed~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The h=0.25 constrained localization replay shows the best annulus remains below the broad topN=196 control under the same support/capture floors, with meaningful improvement over topN=False.  _(class `C`)_
- **chain closes:** False — The finite bounded-negative result closes numerically, but the row is queued as proposed_retained only because the Status line describes a final localization attempt on a proposed_retained family. The note itself does not supply a retained theorem.
- **rationale:** Issue: The source is a final constrained localization control sweep on one h=0.25 ordered-lattice family, but the audit queue records it as proposed_retained because the Status line mentions the proposed_retained family being tested. Why this blocks: the runner can close the bounded negative comparison, but it cannot turn a finite single-family localization sweep into a retained theorem about localized inertial sources. Repair target: correct the Status/current_status to bounded/proposed_bounded, or provide a separate retained theorem deriving the broad-source frontier beyond this finite h=0.25 sweep. Claim boundary until fixed: it is safe to claim the live artifact reproduces topN 196 as overall best admissible, annulus 1:6 as best annulus with capture2=0.916 and score=0.9947, and meaningful improvement over topN=False; it is not safe to present this note as a retained localization theorem.
- **auditor confidence:** high

### `mesoscopic_surrogate_threshold_2d_note`

- **Note:** [`MESOSCOPIC_SURROGATE_THRESHOLD_2D_NOTE.md`](../../docs/MESOSCOPIC_SURROGATE_THRESHOLD_2D_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_failed~~
- **effective_status:** ~~audited_failed~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The 2D threshold sweep shows every scanned topN from 1 through 81 remains stable, so support shrinkage does not expose a sharp two-stage sourced-response threshold in this retained 2D family.  _(class `C`)_
- **chain closes:** False — The bounded control result closes numerically, but the note explicitly says it remains a bounded control and not a persistent-mass theorem; the proposed_retained queue status is a parser/status false positive.
- **rationale:** Issue: The source Status begins with 'bounded control note' and later states the test remains a bounded control, not a persistent-mass theorem, but the audit queue records it as proposed_retained because the Status line also mentions a proposed_retained 2D support sweep. Why this blocks: the live runner verifies a finite support sweep, not a retained theorem about localized persistent mass or inertial response. Repair target: correct the Status/current_status to bounded/proposed_bounded, or provide a separate retained theorem deriving a persistent-mass object from the sweep. Claim boundary until fixed: it is safe to claim the live artifact reproduces all scanned topN values stable, first stable topN=1, and no sharp support threshold in this 2D companion family; it is not safe to present this note as a retained persistent-mass or localization theorem.
- **auditor confidence:** high

### `minimal_absorbing_horizon_probe_note`

- **Note:** [`MINIMAL_ABSORBING_HORIZON_PROBE_NOTE.md`](../../docs/MINIMAL_ABSORBING_HORIZON_PROBE_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_failed~~
- **effective_status:** ~~audited_failed~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The live probe shows escape_fraction(alpha) falls below 50% by alpha=0.10 while the alpha=0 weak-field recovery check gives 3/3 TOWARD and F~M=1.00 on the tested generated-geometry family.  _(class `C`)_
- **chain closes:** False — The bounded proxy computation closes, but the queued proposed_retained claim does not: the note itself calls this a bounded moonshot trapping probe, and the absorption parameter is an inserted proxy rather than a derived horizon mechanism.
- **rationale:** Issue: The source is explicitly a bounded moonshot trapping probe on a proposed_retained generated-geometry family, but its branch verdict says it produces a retained threshold. The live runner inserts an absorptive parameter alpha and measures escape fraction; it does not derive an absorbing horizon law or black-hole observable from retained inputs. Why this blocks: a hand-added absorption proxy with one finite family, four seeds, and three source positions cannot be ratified as a retained horizon/trapping theorem. Repair target: either correct the Status/current_status to bounded/proposed_bounded, or derive the absorption law from retained dynamics and show the threshold is a framework-native strong-field observable with clean weak-field reduction and audited dependencies. Claim boundary until fixed: it is safe to claim the live artifact reproduces alpha=0 weak-field recovery and a proxy escape threshold below 50% at alpha ~= 0.10 on this setup; it is not safe to call this a retained horizon theorem or full black-hole mechanism.
- **auditor confidence:** high

### `minimal_bidirectional_trapping_probe_note`

- **Note:** [`MINIMAL_BIDIRECTIONAL_TRAPPING_PROBE_NOTE.md`](../../docs/MINIMAL_BIDIRECTIONAL_TRAPPING_PROBE_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_failed~~
- **effective_status:** ~~audited_failed~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The live bidirectional trapping probe shows escape_fraction(alpha) falls below 50% by alpha=0.10 while alpha=0 recovers 3/3 TOWARD and F~M=1.00 on the tested geometry-sector family.  _(class `C`)_
- **chain closes:** False — The live proxy computation reproduces the table, but the named frozen log is missing and the queued proposed_retained claim overpromotes a hand-added trapping parameter into a retained no-return threshold.
- **rationale:** Issue: The source names logs/2026-04-05-minimal-bidirectional-trapping-probe.txt, but that frozen artifact is absent, and the note's branch verdict says the proxy produces a retained threshold even though the Status calls it a bounded moonshot probe. Why this blocks: a live rerun of a hand-added alpha trapping proxy can support bounded evidence, but missing frozen output plus no derivation of the trapping law prevents retained ratification. Repair target: restore or regenerate the frozen log, correct the Status/current_status to bounded/proposed_bounded, or derive the trapping parameter from retained dynamics and audit the weak-field dependencies. Claim boundary until fixed: it is safe to claim the live runner reproduces alpha=0 weak-field recovery and escape below 50% at alpha ~= 0.10 on this finite setup; it is not safe to call this a retained no-return or black-hole threshold theorem.
- **auditor confidence:** high

### `mirror_2d_gravity_law_note`

- **Note:** [`MIRROR_2D_GRAVITY_LAW_NOTE.md`](../../docs/MIRROR_2D_GRAVITY_LAW_NOTE.md)
- **current_status:** _proposed_promoted_
- **audit_status:** ~~audited_failed~~
- **effective_status:** ~~audited_failed~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The cleanup sweep reports that exact 2D mirror gravity-side mass and distance fits remain weak and fit-dependent, with no clean 2D mirror mass or distance law proposed for promotion.  _(class `C`)_
- **chain closes:** False — The named cleanup runner reproduces the weak best-fit rows for N=60,80,100 and its interpretation says to keep the result bounded unless the fit is visibly clean. The audit queue row is proposed_promoted only because the source status line contains the phrase 'no clean 2D mirror law proposed_promoted', which is an explicit non-promotion statement.
- **rationale:** Issue: the target is classified as proposed_promoted, but the source note and runner both say the cleanup found no clean promoted 2D mirror gravity law. Why this blocks: the best mass exponents are weak or deteriorating and the distance-tail fits are absent or low quality, so promoting a law would invert the actual result of the source packet. Repair target: change the Status line so the audit queue reads this as a bounded cleanup/non-promotion note, or create a separate promotion packet with a registered runner that demonstrates a stable mass or distance law with hard fit-quality thresholds. Claim boundary until fixed: it is safe to claim that the exact 2D mirror family remains a bounded coexistence pocket and that the cleanup sweep found N=60 mass-window R^2=0.923, N=60 distance-tail R^2=0.872, N=80 no review-safe distance tail, and N=100 weak mass/distance fits; it is not safe to claim a promoted 2D mirror gravity law.
- **open / conditional deps cited:**
  - `source_status_explicitly_says_no_clean_2d_mirror_law_proposed_promoted`
  - `cleanup_runner_interpretation_keeps_result_bounded_not_promoted`
  - `mass_and_distance_fits_not_review_safe_for_promotion`
- **auditor confidence:** high

### `mirror_2d_validation_note`

- **Note:** [`MIRROR_2D_VALIDATION_NOTE.md`](../../docs/MIRROR_2D_VALIDATION_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_clean~~
- **effective_status:** **retained**  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The exact 2D mirror family gives a bounded coexistence pocket over N=25,40,60,80,100, with the strongest row at N=60: MI=0.756118, 1-pur_min=0.4420, d_TV=0.8572, gravity=+2.5687, Born=1.08e-15, and k=0=0.  _(class `C`)_
- **chain closes:** True — The named validator and archived log reproduce the retained rows, the matched random baseline, the Born and k=0 controls, and the weak gravity-law follow-up fits. Running the validator with the note's N window reproduces the table exactly; the script default includes an extra N=15 row, which is outside the note's retained window and does not change the retained claim.
- **rationale:** The bounded exact-2D mirror pocket closes on its own terms: the runner verifies machine-scale Born residuals, zero k=0 response, positive gravity, and substantially stronger MI/decoherence/d_TV than the matched random baseline on the reported N window. The same runner also verifies that the mass-window and distance-tail fits are weak, so this clean audit ratifies only the bounded coexistence pocket, strongest at N=60; it does not ratify a promoted mass law, distance law, continuum law, or flagship replacement.
- **auditor confidence:** high

### `mirror_chokepoint_boundary_fit_note`

- **Note:** [`MIRROR_CHOKEPOINT_BOUNDARY_FIT_NOTE.md`](../../docs/MIRROR_CHOKEPOINT_BOUNDARY_FIT_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_clean~~
- **effective_status:** **retained**  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The canonical NPL_HALF=60, connect_radius=5.0 mirror chokepoint replay is Born-clean and gravity-positive through N=100, has a gravity wall at N=120, and its retained-row decoherence fit is only a weak descriptive fit with no asymptotic claim.  _(class `C`)_
- **chain closes:** True — The live canonical runner reproduces the frozen retained-window table, including Born and k=0 controls, and direct arithmetic on the retained rows reproduces the weak fit coefficient, exponent, R2, and illustrative extrapolations. The source explicitly refuses a robust asymptotic law.
- **rationale:** The claim is finite and descriptive: a Born-clean, gravity-positive mirror boundary pocket through N=100, a gravity wall at N=120 for this fixed configuration, and a weak non-monotone decoherence fit. The live runner matches the canonical table and the fit recomputation gives coefficient 0.3901, exponent -0.245, and R2=0.126. Because the note explicitly says the fit is not a clean asymptotic law, the retained content closes within the stated bounded scope; residual risk is only ordinary finite-window generalization risk, which the note does not overclaim.
- **auditor confidence:** high

### `mirror_chokepoint_note`

- **Note:** [`MIRROR_CHOKEPOINT_NOTE.md`](../../docs/MIRROR_CHOKEPOINT_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_conditional~~
- **effective_status:** ~~audited_conditional~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The note claims a retained bounded mirror chokepoint pocket through N = 100, with Born-clean and k=0-clean rows, positive gravity, decoherence advantage, and N = 120 losing gravity.  _(class `C`)_
- **chain closes:** False — The live runner supports a finite bounded mirror pocket and reproduces the dense NPL_HALF=60, connect_radius=5.0 N=80/N=100 rows plus N=120 gravity collapse, but the retained table is stitched across parameter surfaces and the cited primary logs for several rows are absent. A clean chain would need a registered per-row parameter card or archived logs and hard pass/fail gates for the retained criteria.
- **rationale:** Issue: the finite mirror-chokepoint pocket is partly reproducible, but the proposed-retained packet depends on a stitched table whose N=40/N=60 values are not recovered by the strict NPL_HALF=25 radius-4.0 baseline or by NPL_HALF=25 radius-5.0, and several cited log files for the joint, scaling, sparse-rescue, and boundary scans are missing. Why this blocks: a hostile auditor can verify N=15/N=25 on the strict baseline and the dense NPL_HALF=60 radius-5.0 N=40/60/80/100 positive-gravity window with N=120 collapse, but cannot certify the exact retained table or the through-N=100 retention story as a single closed claim without knowing which archived parameter surface supports each row and without assertion-gated retention criteria. Repair target: register one primary runner/log packet or per-row parameter-card table, archive the named logs, and add hard checks for seed counts, NPL_HALF/connect_radius/layer2_prob, Born tolerance, k=0, gravity positivity/significance, decoherence ceiling, and N=120 failure. Claim boundary until fixed: it is safe to claim a finite diagnostic pocket: strict NPL_HALF=25 radius-4.0 reproduces retained N=15/N=25, dense NPL_HALF=60 radius-5.0 reproduces positive-gravity Born-clean k=0-clean mirror rows through N=100 and zero-gravity collapse at N=120; it is not yet a clean retained asymptotic or single-surface mirror-chokepoint theorem.
- **open / conditional deps cited:**
  - `logs/2026-04-03-mirror-chokepoint-joint.txt_missing`
  - `logs/2026-04-03-mirror-chokepoint-scale-r5p0-n50.txt_missing`
  - `logs/2026-04-03-mirror-chokepoint-scale-r5p0-p2p02-n50.txt_missing`
  - `logs/2026-04-03-mirror-chokepoint-boundary-n45-r5p0.txt_missing`
  - `logs/2026-04-03-mirror-chokepoint-boundary-n50-r5p2.txt_missing`
  - `logs/2026-04-03-mirror-chokepoint-boundary-n55-r5p0.txt_missing`
  - `logs/2026-04-03-mirror-chokepoint-boundary-n55-r5p0-N100.txt_missing`
  - `logs/2026-04-03-mirror-chokepoint-boundary-n55-r5p2-N100.txt_missing`
  - `logs/2026-04-03-mirror-chokepoint-boundary-n60-r5p0-N100.txt_missing`
  - `logs/2026-04-03-mirror-chokepoint-boundary-n60-r5p0-N120.txt_missing`
  - `mixed_parameter_surface_not_registered_per_retained_row`
  - `runner_prints_diagnostics_without_hard_retention_assertions`
- **auditor confidence:** high

### `mirror_grown_combined_note`

- **Note:** [`MIRROR_GROWN_COMBINED_NOTE.md`](../../docs/MIRROR_GROWN_COMBINED_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_failed~~
- **effective_status:** ~~audited_failed~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The grown Z2 mirror scaffold remains Born-safe where it runs but does not reproduce the retained mirror chokepoint pocket or approximate the retained Z2xZ2 joint benefit.  _(class `C`)_
- **chain closes:** False — The exploratory negative result closes numerically, but the audit row is a parser false positive: the source Status explicitly says exploratory only and does not approximate the proposed_retained higher-symmetry benefit.
- **rationale:** Issue: The queue records this as proposed_retained because the Status line mentions the proposed_retained higher-symmetry benefit, but the source explicitly states 'exploratory only' and concludes this grown mirror scaffold is not the successor lane. Why this blocks: an exploratory negative control cannot be ratified as retained; doing so would invert the source's conclusion. Repair target: correct the Status/current_status to exploratory, bounded, or support, or author a separate retained grown-symmetry theorem with a runner that actually reproduces the mirror/Z2xZ2 benefit. Claim boundary until fixed: it is safe to claim the live runner reproduces the weak scout table and the negative conclusion that grown mirror does not approximate the retained benefit; it is not safe to present this note as a retained long-term vector.
- **auditor confidence:** high

### `mirror_mutual_information_chokepoint_note`

- **Note:** [`MIRROR_MUTUAL_INFORMATION_CHOKEPOINT_NOTE.md`](../../docs/MIRROR_MUTUAL_INFORMATION_CHOKEPOINT_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_conditional~~
- **effective_status:** ~~audited_conditional~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The note claims a canonical exact-mirror mutual-information artifact chain on the proposed-retained dense chokepoint family, with a bounded mid-N mirror MI advantage over matched random but no clean asymptotic law.  _(class `C`)_
- **chain closes:** False — The named log exists and the live runner exactly reproduces the finite N=40/60/80/100 MI, d_TV, purity, and descriptive exponent table, including the N=100 MI reversal against mirror. The retained chain is still conditional because the claim is explicitly built on the proposed-retained dense mirror-chokepoint family, whose audit remains conditional, and the runner prints diagnostics rather than enforcing the retained/mid-N boundaries as hard gates.
- **rationale:** Issue: the finite MI table is live-reproducible, but the proposed-retained claim rests on the dense exact-mirror chokepoint family rather than an independently audited family theorem, and its canonical-line wording can be read as a whole-window mirror advantage even though the N=100 row has mirror MI 0.0408 below random MI 0.0574. Why this blocks: a hostile auditor can certify the printed mid-N diagnostic rows, but cannot promote the artifact chain to a clean retained claim while the underlying mirror-chokepoint family is conditional and the pass criteria for mid-N advantage, N=100 reversal, purity interpretation, and non-asymptotic exponent use are not assertion-gated. Repair target: make docs/MIRROR_CHOKEPOINT_NOTE.md or an equivalent family-definition packet clean, add runner assertions for N=40/60/80 mirror MI > random, N=100 non-advantage, seed counts, npl_half/connect_radius/k/layer2_prob, and descriptive-only fits, and revise the canonical retained sentence to say advantage on N=40/60/80 rather than the whole retained dense window. Claim boundary until fixed: it is safe to claim an exact finite diagnostic: for npl_half=60, connect_radius=5.0, k=5.0, 16 seeds, mirror MI exceeds matched random at N=40/60/80, loses at N=100, mirror purity is lower than random at N=60/80/100 but not N=40, and the power-law fits are descriptive only.
- **open / conditional deps cited:**
  - `MIRROR_CHOKEPOINT_NOTE.md_audited_conditional_family_basis`
  - `scripts/mirror_chokepoint_joint.py_imported_generator_not_registered_as_clean_one_hop_dependency`
  - `runner_prints_diagnostics_without_hard_mid_N_or_non_asymptotic_assertions`
  - `canonical_dense_window_wording_overstates_N100_MI_advantage_boundary`
- **auditor confidence:** high

### `mirror_vs_lattice_program_note`

- **Note:** [`MIRROR_VS_LATTICE_PROGRAM_NOTE.md`](../../docs/MIRROR_VS_LATTICE_PROGRAM_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_failed~~
- **effective_status:** ~~audited_failed~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The note ranks mirror as the flagship coexistence lane, ordered lattice as the strongest secondary law-side branch, and NN refinement as a bounded continuum-side frontier using the named canonical references.  _(class `B`)_
- **chain closes:** False — The comparison depends on cited program notes whose current audit/effective statuses are unaudited, conditional, or failed, and there is no runner or ledger-derived check that recomputes the ranking from clean retained inputs.
- **rationale:** Issue: The retained comparison imports multiple named authorities that are not audit-clean, including unaudited/unknown synthesis and lattice notes, a conditional mirror MI note, and failed lattice-side notes such as LATTICE_3D_DENSE_SPENT_DELAY_NOTE and LATTICE_SYNTHESIS_GUARD_NOTE. Why this blocks: the note's flagship/secondary/frontier ranking is a cross-note synthesis, so it cannot be retained while load-bearing source rows are unaudited, conditional, or failed. Repair target: first audit or repair the cited authorities, remove failed inputs from the retained comparison, and ideally generate the comparison table from audit_ledger effective_status so only retained dependencies can support retained wording. Claim boundary until fixed: it is safe to use this as a provisional editorial map of intended program lanes, with mirror_2D_validation and lattice_distance_law called out as clean where applicable; it is not safe to present the whole mirror-vs-lattice ranking as an audit-retained canonical comparison.
- **open / conditional deps cited:**
  - `AUDITED_SYMMETRY_SYNTHESIS_NOTE.md`
  - `UNIFIED_PROGRAM_NOTE.md`
  - `MIRROR_MUTUAL_INFORMATION_CHOKEPOINT_NOTE.md`
  - `LATTICE_FAMILY_VALIDATION_NOTE.md`
  - `LATTICE_FIELD_STRENGTH_UNIFICATION_NOTE.md`
  - `LATTICE_3D_DENSE_SPENT_DELAY_NOTE.md`
  - `LATTICE_NN_CONTINUUM_NOTE.md`
  - `LATTICE_SYNTHESIS_GUARD_NOTE.md`
- **auditor confidence:** high

### `moonshot_other_testables_note`

- **Note:** [`MOONSHOT_OTHER_TESTABLES_NOTE.md`](../../docs/MOONSHOT_OTHER_TESTABLES_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_failed~~
- **effective_status:** ~~audited_failed~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The best non-diamond moonshot is the interferometric / waveguide phase-ramp analog because it maps directly onto the strongest retained phase-sensitive observable.  _(class `B`)_
- **chain closes:** False — The source note names retained connections and an R^2 ~ 0.96 phase-ramp result, but supplies no one-hop cited authority or runner that verifies those inputs or derives the ranking criterion.
- **rationale:** Issue: The retained shortlist/ranking imports unnamed retained artifacts and an R^2 ~ 0.96 phase-ramp result, then declares the interferometric / waveguide analog the best non-diamond testable without a cited authority set, ranking metric, or runner. Why this blocks: the audit input contains no dependency theorem or computation from which the top-testable conclusion follows, so the proposed_retained claim cannot be verified from the allowed source context. Repair target: add explicit audited-retained one-hop citations for each retained connection, define the ranking criteria, and provide a table or runner that recomputes the ordering from those inputs; otherwise demote the note to open brainstorming. Claim boundary until fixed: it is safe to present these as possible non-diamond analog directions and the waveguide phase-ramp as an author-prioritized candidate, but not as an audit-retained best testable grounded in retained science.
- **auditor confidence:** high

### `moving_source_cross_family_note`

- **Note:** [`MOVING_SOURCE_CROSS_FAMILY_NOTE.md`](../../docs/MOVING_SOURCE_CROSS_FAMILY_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_clean~~
- **effective_status:** **retained**  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The note claims a narrow proposed-retained extension: the moving-source centroid-bias observable survives on two portable grown families under exact zero-source and matched static controls.  _(class `C`)_
- **chain closes:** True — The live runner exactly reproduces the source-note table: both families have zero-source static and moving baselines at 0.000e+00, v=0 matched-static deltas at +0.000000e+00, and signed delta_y vs static responses that flip with v on both drift/restore families. The runner itself states the correct boundary: this is a bounded moving-source proxy on grown geometries, not a wave theory.
- **rationale:** The finite extension closes on its own terms: the runner builds both named portable grown families, applies exact zero-source and v=0 static controls, and reproduces the signed moving-source centroid-bias rows with six seeds per velocity. This clean audit is narrow: it certifies only the two displayed drift/restore family cards, the signed delta_y-vs-static pattern, exact zero baselines, and flat v=0 control; it does not certify a wave theory, asymptotic portability law, or broader class of generated families.
- **auditor confidence:** high

### `multipole_tidal_response_note`

- **Note:** [`MULTIPOLE_TIDAL_RESPONSE_NOTE.md`](../../docs/MULTIPOLE_TIDAL_RESPONSE_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_clean~~
- **effective_status:** **retained**  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The centered quadrupole keeps the centroid essentially pinned but opens a real width/tidal channel, and the width response grows with quadrupole separation.  _(class `C`)_
- **chain closes:** True — The live probe reproduces the frozen controls and finite quadrupole rows: same-site and neutral controls are zero, the dipole mainly shifts centroid, and the centered quadrupoles give near-zero centroid change with positive width response at a = 1.0 and a = 2.0. The source explicitly excludes full tensor gravity and a general multipole theory.
- **rationale:** The retained content is a narrow finite-runner claim, not a physical tidal-field theorem: the current runner recomputes the same-site cancellation, q_test = 0 inert control, dipole baseline, and two centered quadrupole width responses. The quadrupole rows support the stated shape-sensitive width channel while the note explicitly disclaims full tensor gravity, relativistic tidal fields, and a general multipole expansion. Residual risk is only finite-configuration scope, plus a harmless rounded-ratio mismatch where the prose says 1.969 and the live runner prints +1.968; the audit does not retain anything beyond the tested ordered-lattice configuration.
- **auditor confidence:** high

### `neutrino_dirac_z3_support_trichotomy_note`

- **Note:** [`NEUTRINO_DIRAC_Z3_SUPPORT_TRICHOTOMY_NOTE.md`](../../docs/NEUTRINO_DIRAC_Z3_SUPPORT_TRICHOTOMY_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_conditional~~
- **effective_status:** ~~audited_conditional~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** Assume the retained three-generation matter structure, the retained reduction of neutrino mass to the Dirac lane, and a single Higgs doublet with definite generation Z_3 charge q_H; then the allowed support of Y_nu is exactly one of three permutation patterns.  _(class `B`)_
- **chain closes:** False — The runner verifies the Z_3 support trichotomy once the left/right generation charges and single-Higgs q_H condition are supplied, but those retained atlas inputs are not registered as one-hop dependencies for this row.
- **rationale:** Issue: The exact support classification depends on unregistered upstream inputs: one-generation matter closure, three-generation matter structure, reduction to the Dirac neutrino lane, and the explicit single-Higgs definite-Z_3-charge condition. Why this blocks: The matrix-support trichotomy is valid algebra after those charges are supplied, but the audit packet does not establish the charges, the Dirac-lane reduction, or the Higgs charge bridge as clean retained dependencies, so the proposed-retained lane cannot close from this row alone. Repair target: Register clean dependency notes for the generation charges and Dirac-lane reduction, and either derive or keep explicitly bounded the single-Higgs q_H assumption; make the runner read those declared charges rather than hard-coding them as retained. Claim boundary until fixed: It is safe to claim the conditional theorem that given q_L=(0,+1,-1), q_R=(0,-1,+1), and one definite q_H, Y_nu support reduces from nine entries to one of three three-entry permutation patterns.
- **open / conditional deps cited:**
  - `one_generation_matter_closure_dependency_not_registered`
  - `three_generation_matter_structure_dependency_not_registered`
  - `neutrino_dirac_lane_reduction_dependency_not_registered`
  - `single_higgs_z3_charge_condition_not_derived`
- **auditor confidence:** high

### `neutrino_lane4_dirac_seesaw_fork_no_go_note_2026-04-27`

- **Note:** [`NEUTRINO_LANE4_DIRAC_SEESAW_FORK_NO_GO_NOTE_2026-04-27.md`](../../docs/NEUTRINO_LANE4_DIRAC_SEESAW_FORK_NO_GO_NOTE_2026-04-27.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_clean~~
- **effective_status:** **retained**  (reason: `self`)
- **auditor:** `codex-audit-loop:fresh-2026-04-28-neutrino_lane4_dirac_seesaw_fork_no_go_note_2026-04-27`  (codex-current; independence=fresh_context)
- **load-bearing step:** At least one additional positive premise is required: a nonzero charge-2 Majorana primitive or equivalent admitted Majorana/seesaw extension, or a separate tiny Dirac `Y_nu` activation law on the surviving Dirac lane.  _(class `A`)_
- **chain closes:** True — The claim is a negative boundary: the note does not close neutrino masses, but separates the current-stack mu_current=0 surface from the nonzero invertible seesaw benchmark and from a direct one-Higgs Dirac reading of y_nu^eff. The live runner verifies the non-invertibility, direct-Dirac overshoot, benchmark status, and remaining fork with PASS=10 FAIL=0.
- **rationale:** The retained content is the fork no-go, not full neutrino quantitative closure. The note's load-bearing algebra closes because the current-stack Majorana zero law has det(M_R)=0 while the type-I seesaw benchmark uses a nonzero invertible M_R, so the two surfaces cannot be silently identified. The direct Dirac route also fails on its own terms: y_nu^eff v/sqrt(2) gives about 1.16e9 eV, while the benchmark meV scale would require a separate Yukawa of about 2.9e-13. Residual risk is downstream misuse: this audit does not ratify a final no-go against Majorana or Dirac neutrinos, the solar gap, PMNS quantities, or full Lane 4 mass closure.
- **auditor confidence:** high

### `newton_derivation_note`

- **Note:** [`NEWTON_DERIVATION_NOTE.md`](../../docs/NEWTON_DERIVATION_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_conditional~~
- **effective_status:** ~~audited_conditional~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** If the inertial quantity of a persistent pattern is an extensive quantity attached to the same composition law as the field-source parameter s, then m is proportional to s and momentum conservation selects p = 1.  _(class `A`)_
- **chain closes:** False — The p = 1 selection is algebraic once m is proportional to s is assumed, but the source and support runners explicitly leave the persistent-pattern inertial-mass identification open.
- **rationale:** Issue: The Newtonian selection step still depends on Principle 3: a persistent-pattern inertial quantity must be extensive under the same composition law as the field-source parameter s. Why this blocks: the live support runners close only amplitude invariance and test-particle source additivity, and the source note itself says no persistent-pattern inertial object has been produced, so the mass map m proportional to s is an explicit conditional premise rather than a retained theorem. Repair target: construct a persistent or quasi-persistent localized lattice state, measure its inertial response and sourced field parameter under the same composition law, and show that the same extensive quantity controls both before rerunning the p = 1 momentum-selection argument. Claim boundary until fixed: it is safe to retain the conditional algebra that linear propagation, phase valley, extensive m proportional to s, and momentum conservation select p = 1 on the ordered-lattice family; it is not safe to claim a closed Newtonian mass-scaling derivation from current inputs.
- **open / conditional deps cited:**
  - `EQUIVALENCE_PRINCIPLE_HARNESS_NOTE.md`
  - `COMPOSITE_SOURCE_ADDITIVITY_NOTE.md`
  - `COMPOSITE_SOURCE_ADDITIVITY_2D_NOTE.md`
- **auditor confidence:** high

### `nonlabel_grown_basin_note`

- **Note:** [`NONLABEL_GROWN_BASIN_NOTE.md`](../../docs/NONLABEL_GROWN_BASIN_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_clean~~
- **effective_status:** **retained**  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The geometry-sector / non-label architecture survives the nearest restore neighborhood at fixed drift = 0.2 with zero-source and neutral controls, correct sign orientation, and linear charge response.  _(class `C`)_
- **chain closes:** True — The live targeted runner reproduces the frozen seed-0 restore sweep at drift = 0.2: all three rows have zero baseline, neutral cancellation, opposite single-source signs, and charge exponent approximately 1.0.
- **rationale:** The source makes a bounded finite-runner claim: a tiny positive basin at drift = 0.2 for restore values 0.60, 0.70, and 0.80 on seed 0. The current runner recomputes the zero-source baseline, neutral +1/-1 cancellation, sign orientation, double-charge response, and exponent checks for those rows, and all three rows pass. Residual risk is fixed-configuration scope only; this clean audit does not retain a general grown-graph basin, a label-independent theory, or any claim beyond the tested restore neighborhood.
- **auditor confidence:** high

### `nonlabel_grown_drift_basin_note`

- **Note:** [`NONLABEL_GROWN_DRIFT_BASIN_NOTE.md`](../../docs/NONLABEL_GROWN_DRIFT_BASIN_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_clean~~
- **effective_status:** **retained**  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** All checked rows across seeds 0, 1, 2 pass, so the geometry-sector / non-label architecture survives the nearest drift neighborhood at fixed restore = 0.7.  _(class `C`)_
- **chain closes:** True — The live full sweep reproduces the 3 by 3 drift/seed table: every row has zero baseline, neutral cancellation, opposite signed response, double-charge response, and exponent near 1.0. The source keeps the conclusion to a narrow local drift basin and cites the now-clean restore-basin anchor.
- **rationale:** The load-bearing claim is finite and runner-backed: at restore = 0.7, drifts 0.15, 0.20, and 0.25 pass for seeds 0, 1, and 2 under the stated zero, neutral, sign, and charge-scaling checks. The live sweep reproduces all nine rows, and the directly named restore-basin anchor is already audited_clean for its own fixed neighborhood. Residual risk is only the declared local-sweep scope; this does not retain a family-wide transfer theorem, multi-restore/multi-drift basin, or architecture-independent non-label law.
- **auditor confidence:** high

### `observable_principle_from_axiom_note`

- **Note:** [`OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md`](../../docs/OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md)
- **current_status:** unknown
- **audit_status:** ~~audited_conditional~~
- **effective_status:** ~~audited_conditional~~  (reason: `self`)
- **auditor:** `codex-audit-loop:fresh-2026-04-28-observable_principle_from_axiom_note`  (codex-current; independence=fresh_context)
- **load-bearing step:** Under continuity, additivity on independent subsystems and CPT-even phase blindness force W = c log|Z| + const, normalized to W[J] = log|det(D+J)| - log|det D|.  _(class `A`)_
- **chain closes:** False — The finite Grassmann/log-det response chain closes under the note's stated scalar-observable assumptions, and the live runner reports 13 pass and 0 fail. It does not derive scalar additivity, CPT-even phase blindness, continuity, normalization, or the downstream hierarchy baseline from the bare lattice axiom alone.
- **rationale:** Issue: the note proves the log|det(D+J)| source-response result only after adding scalar additivity, CPT-even phase blindness, continuity, and normalization assumptions, and its electroweak-scale consequence imports the current hierarchy baseline rather than deriving that normalization here.
Why this blocks: downstream proposed-retained/promoted claims need a bare-axiom observable bridge; this row supplies a conditional scalar-source rule, not a standalone derivation of the physical scalar observable principle.
Repair target: either derive the scalar-observable selection assumptions and hierarchy normalization chain from the accepted axiom package with a runner that excludes competing generators, or narrow the claim to an explicit conditional source-response theorem.
Claim boundary until fixed: safe to claim finite-block log|det| curvature and the Lt=4 selector under the stated scalar-observable assumptions, not axiom-only observable closure or electroweak-scale derivation.
- **open / conditional deps cited:**
  - `scalar_observable_selection_assumptions_not_derived_from_bare_axiom`
  - `canonical_hierarchy_baseline_and_plaquette_normalization_chain_imported`
- **auditor confidence:** high

### `omega_lambda_matter_bridge_theorem_note_2026-04-22`

- **Note:** [`OMEGA_LAMBDA_MATTER_BRIDGE_THEOREM_NOTE_2026-04-22.md`](../../docs/OMEGA_LAMBDA_MATTER_BRIDGE_THEOREM_NOTE_2026-04-22.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_conditional~~
- **effective_status:** ~~audited_conditional~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The theorem identifies the de Sitter vacuum density rho_Lambda=3 H_inf^2/(8*pi*G) and present critical density rho_crit=3 H_0^2/(8*pi*G), then cancels the common factors to obtain Omega_Lambda=(H_inf/H_0)^2 and, under flat FRW, Omega_m=1-(H_inf/H_0)^2-Omega_r.  _(class `A`)_
- **chain closes:** False — The runner verifies the symbolic cancellations and FRW algebra exactly, and its numerical Planck checks are consistent. But the proof chain imports the retained spectral-gap Lambda=3/R_Lambda^2 identity, the H_inf=c/R_Lambda scale identification, w=-1/constant-vacuum interpretation, standard flat FRW critical-density relation, H_0/Omega observational anchors, and the radiation fraction without any registered one-hop dependencies in the audit row. The note also explicitly leaves the key ratio H_inf/H_0 open, so it reduces the cosmology closure burden but does not close Omega_Lambda or Omega_m from CL3 data.
- **rationale:** The internal algebra is correct: assuming the retained de Sitter spectral-gap radius and standard FRW definitions, Omega_Lambda=(H_inf/H_0)^2 follows immediately, and flatness gives Omega_m=1-Omega_Lambda-Omega_r. The runner passes all 9 checks, including exact SymPy identities and Planck 2018 consistency arithmetic. The blocking issue is authority, not algebra. A Nature-grade audit cannot treat this as closed on the package surface because the spectral-gap identity, scale-identification note, dark-energy EOS corollary, flat-FRW cosmology, observed H_0/Omega_Lambda/Omega_m values, and Omega_r are imported rather than registered and audited as one-hop dependencies. More importantly, the note does not derive H_inf/H_0; it states that closure of Omega_Lambda and Omega_m reduces to that one open number. Repair requires audited one-hop registration of the spectral-gap, EOS, scale-identification, and FRW-density assumptions, plus a retained matter-content or cosmology-scale theorem deriving H_inf/H_0 (and Omega_r if used beyond negligible error). What can safely be claimed is the conditional structural bridge: given the de Sitter spectral-gap and flat-FRW assumptions, Omega_Lambda is exactly the square of H_inf/H_0 and Omega_m follows algebraically; this is not a retained numerical prediction of Omega_Lambda, Omega_m, R_Lambda, or the cosmological hierarchy.
- **open / conditional deps cited:**
  - `COSMOLOGICAL_CONSTANT_SPECTRAL_GAP_IDENTITY_THEOREM_NOTE.md_not_registered_one_hop_dependency`
  - `DARK_ENERGY_EOS_RETAINED_COROLLARY_THEOREM_NOTE.md_not_registered_one_hop_dependency`
  - `COSMOLOGY_SCALE_IDENTIFICATION_AND_REDUCTION_NOTE.md_not_registered_one_hop_dependency`
  - `standard_flat_FRW_critical_density_and_budget_assumptions_not_CL3_registered`
  - `H_inf_over_H_0_ratio_matter_content_bridge_open`
  - `Planck_2018_H0_OmegaLambda_OmegaM_observational_comparators_external`
  - `radiation_fraction_Omega_r_observational_input_not_derived`
- **auditor confidence:** high

### `packet_memory_note`

- **Note:** [`PACKET_MEMORY_NOTE.md`](../../docs/PACKET_MEMORY_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_clean~~
- **effective_status:** **retained**  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The model supports detector-readable packet memory: separated initial packets remain distinguishable at the detector, and packet identity changes the gravitational deflection, while persistent inertial response remains open.  _(class `C`)_
- **chain closes:** True — The live harness reproduces the frozen overlap-vs-offset, overlap-vs-NL, gravity-by-packet, and width/centroid rows. The note explicitly keeps Tier C inertial response open and does not claim persistent localized objects.
- **rationale:** The retained surface is a finite computational memory claim: at the tested NL values and packet offsets, detector overlaps remain distinguishable, packet identity changes the imposed-field deflection, and width/centroid rows reproduce the stated partial shape result. The live runner matches the frozen source numbers, and the source explicitly excludes Tier C inertial response and persistent localized-object closure. Residual risk is finite-configuration and asymptotic-scope risk only; this clean audit does not retain the unsupported NL-to-infinity extrapolation as a theorem or any claim of persistent inertial mass.
- **auditor confidence:** high

### `persistent_inertial_object_probe_note`

- **Note:** [`PERSISTENT_INERTIAL_OBJECT_PROBE_NOTE.md`](../../docs/PERSISTENT_INERTIAL_OBJECT_PROBE_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_clean~~
- **effective_status:** **retained**  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** No top-N class met the capture/carry/shift thresholds, so the honest read is broad-surrogate steering, not a closed persistent-mass object.  _(class `C`)_
- **chain closes:** True — The live probe reproduces the relaunch sweep and the threshold test: every top-N row fails at least one admissibility threshold, and the leading surrogate is broad topN=361 with rel_shift_err 0.271.
- **rationale:** The retained claim is a negative diagnostic, not a positive persistent-mass theorem. The live runner recomputes the full top-N sweep, finds no admissible class under capture >= 0.80, carry >= 0.90, and rel_shift_err <= 0.05, and identifies only a broad topN=361 surrogate with capture 0.839, carry 0.954, and rel_shift_err 0.271. Residual risk is threshold/scope risk only; this clean audit retains the no-go/broad-surrogate read and explicitly does not retain persistent inertial mass closure.
- **auditor confidence:** high

### `persistent_inertial_response_readiness_note`

- **Note:** [`PERSISTENT_INERTIAL_RESPONSE_READINESS_NOTE.md`](../../docs/PERSISTENT_INERTIAL_RESPONSE_READINESS_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_failed~~
- **effective_status:** ~~audited_failed~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The localization lane is now frozen as a bounded broad-source control result, not an open hidden-winner search, even though no persistent-mass theorem exists yet.  _(class `B`)_
- **chain closes:** False — The note is a cross-artifact readiness synthesis with no synthesis runner, and several named support rows are unaudited, conditional, or already audited_failed.
- **rationale:** Issue: The retained-style readiness synthesis imports a large set of surrogate, relaunch, localization, and threshold artifacts, but those named support rows are not all audit-clean; they include bounded/unaudited notes, audited_conditional rows, and audited_failed rows such as MESOSCOPIC_SURROGATE_THRESHOLD_2D_NOTE, LOCALIZED_SOURCE_RESPONSE_SWEEP_NOTE, MESOSCOPIC_SURROGATE_COMPACT_FLOOR_SWEEP_NOTE, MESOSCOPIC_SURROGATE_ANNULAR_TAPERED_SWEEP_NOTE, and MESOSCOPIC_SURROGATE_H025_CONSTRAINED_LOCALIZATION_NOTE. Why this blocks: a canonical retained readiness/frontier summary cannot be ratified from a mixed or failed support set, and there is no runner or ledger-derived computation in this note that recomputes the frontier using only audit-clean inputs. Repair target: audit or repair the named support notes first, remove failed inputs from the retained synthesis, and preferably generate the readiness table from audit_ledger effective_status so the frontier statement cannot overstate unratified rows. Claim boundary until fixed: it is safe to say the current audited record still lacks a persistent-pattern inertial-mass theorem and that packet memory plus the persistent-object no-go/broad-surrogate diagnostic are clean within their local scopes; it is not safe to retain this whole readiness synthesis or the claimed frozen localization frontier.
- **open / conditional deps cited:**
  - `ORDERED_LATTICE_PACKET_REIDENTIFICATION_NOTE.md`
  - `ORDERED_LATTICE_QUASI_PERSISTENT_RELAUNCH_NOTE.md`
  - `ORDERED_LATTICE_QUASI_PERSISTENT_RELAUNCH_2D_NOTE.md`
  - `QUASI_PERSISTENT_RELAUNCH_PROBE_NOTE.md`
  - `MESOSCOPIC_SURROGATE_BACKREACTION_NOTE.md`
  - `BROAD_SURROGATE_POINT_SOURCE_COMPARE_NOTE.md`
  - `MESOSCOPIC_SURROGATE_SOURCE_2D_NOTE.md`
  - `MESOSCOPIC_SURROGATE_THRESHOLD_2D_NOTE.md`
  - `LOCALIZED_SOURCE_RESPONSE_SWEEP_NOTE.md`
  - `MESOSCOPIC_SURROGATE_COMPACT_FLOOR_SWEEP_NOTE.md`
  - `MESOSCOPIC_SURROGATE_ANNULAR_TAPERED_SWEEP_NOTE.md`
  - `MESOSCOPIC_SURROGATE_H025_CONSTRAINED_LOCALIZATION_NOTE.md`
  - `PERSISTENT_OBJECT_BLENDED_READOUT_TRANSFER_SWEEP_NOTE_2026-04-16.md`
  - `PERSISTENT_OBJECT_TOP4_MULTISTAGE_OUTER_TRANSFER_SWEEP_NOTE_2026-04-16.md`
- **auditor confidence:** high

### `persistent_object_blended_readout_transfer_sweep_note_2026-04-16`

- **Note:** [`PERSISTENT_OBJECT_BLENDED_READOUT_TRANSFER_SWEEP_NOTE_2026-04-16.md`](../../docs/PERSISTENT_OBJECT_BLENDED_READOUT_TRANSFER_SWEEP_NOTE_2026-04-16.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_conditional~~
- **effective_status:** ~~audited_conditional~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The exact-lattice top3 object plus one retained blended readout architecture transfers across the tested nearby exact-family neighborhood.  _(class `C`)_
- **chain closes:** False — The transfer runner reproduces the six-case finite sweep, but the retained-readout conclusion depends on a scan-selected blend, chosen gates, fixed per-case field calibration, and an unratified detector/readout-to-inertial-response interpretation.
- **rationale:** Issue: the note elevates the scan-selected blend=0.25 readout and top3 compact object to a retained local transfer architecture after a finite nearby-family sweep. Why this blocks: the live runners reproduce the table, but they do not derive the readout blend, source kernel, field-max calibration, top3 object selection, or overlap/alpha/drift gates from retained primitives, and they do not establish a persistent inertial-mass or matter-closure observable. Repair target: provide a theorem or registered computation deriving the readout architecture and admissibility gates independently of the pass/fail scan, plus a persistence/inertial-response bridge that makes the detector shift a retained physical observable rather than a local diagnostic. Claim boundary until fixed: it is safe to claim that, in the frozen exact-lattice setup with h=0.25, Green-like source kernel, field max 0.02, three updates, and blend=0.25, top3 passes all six tested nearby cases while top2 passes only 1/6; this is a bounded local compact-object response transfer regime, not retained matter or inertial-mass closure.
- **auditor confidence:** high

### `persistent_object_top4_multistage_outer_transfer_sweep_note_2026-04-16`

- **Note:** [`PERSISTENT_OBJECT_TOP4_MULTISTAGE_OUTER_TRANSFER_SWEEP_NOTE_2026-04-16.md`](../../docs/PERSISTENT_OBJECT_TOP4_MULTISTAGE_OUTER_TRANSFER_SWEEP_NOTE_2026-04-16.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_conditional~~
- **effective_status:** ~~audited_conditional~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** With h=0.25, top4, blend=0.25, three updates per segment, and three chained segments fixed, the one-ring-farther sweep is multistage-admissible on 4/5 cases, with only source0.50 closed.  _(class `C`)_
- **chain closes:** False — The source-note runner reproduced the stated 4/5 bounded sweep result after a long live run. The chain does not close as a retained law because the queue has no primary runner registered, the archived log is absent in this worktree, the prior sweep/diagnosis authorities are not registered as one-hop dependencies, and the result remains a finite fixed-protocol transfer sweep with a persistent inward-source boundary.
- **rationale:** Issue: the note establishes a bounded finite sweep, not a direction-independent transfer theorem or matter closure. Why this blocks: the live source-note runner took about 700 seconds and reproduced the case table, but it tests only five frozen one-ring-farther cases under a fixed exact-lattice architecture, top4 floor, blended readout, update protocol, and admissibility gates; one inward-source case remains closed, and the audit row has no registered runner or one-hop dependencies for the prior widened-pocket and inward-boundary notes. Repair target: register the runner and reproducible log, register the prior sweep/diagnosis notes as dependencies, add PASS-style assertions for the 4/5 expected result, and derive an inward-source directional law or broader transfer envelope before claiming anything beyond bounded support. Claim boundary until fixed: it is safe to claim that this frozen exact-lattice top4 protocol has a bounded beyond-pocket 4/5 transfer region with a persistent inward-source directional boundary; it is not safe to claim a retained transfer law, self-maintaining inertial mass, or matter closure.
- **open / conditional deps cited:**
  - `scripts/persistent_object_top4_multistage_outer_transfer_sweep.py_runner_not_registered_in_audit_queue`
  - `logs/2026-04-16-persistent-object-top4-multistage-outer-transfer-sweep.txt_missing_from_worktree`
  - `PERSISTENT_OBJECT_TOP4_MULTISTAGE_TRANSFER_SWEEP_NOTE_2026-04-16.md_not_registered_one_hop_dependency`
  - `PERSISTENT_OBJECT_INWARD_BOUNDARY_FLOOR_DIAGNOSIS_NOTE_2026-04-16.md_not_registered_one_hop_dependency`
  - `inward_source_directional_law_open`
  - `direction_independent_transfer_law_open`
  - `self_maintaining_inertial_mass_or_matter_closure_open`
- **auditor confidence:** high

### `planck_boundary_density_extension_theorem_note_2026-04-24`

- **Note:** [`PLANCK_BOUNDARY_DENSITY_EXTENSION_THEOREM_NOTE_2026-04-24.md`](../../docs/PLANCK_BOUNDARY_DENSITY_EXTENSION_THEOREM_NOTE_2026-04-24.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_conditional~~
- **effective_status:** ~~audited_conditional~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** Any local additive rule agreeing with c_cell = 1/4 on one primitive face must give N_A(P) = n * c_cell = c_cell * A(P) / a^2 on every finite boundary patch tiled by n primitive faces.  _(class `A`)_
- **chain closes:** False — The finite-union additivity proof closes as algebra once locality, additivity, cubic orientation symmetry, and c_cell = 1/4 are assumed. The proposed Planck-lane conclusion still depends on the unregistered primitive-coefficient authority and the explicitly open gravitational carrier premise.
- **rationale:** Issue: the runner verifies the finite-patch additive extension, but the source note is explicitly a support theorem inside a conditional Planck packet: it assumes c_cell = 1/4 and states that the primitive boundary/worldtube count has not yet been derived as the microscopic carrier of gravitational boundary/action density. Why this blocks: the algebra N_A(P)=n c_cell and the conditional a/l_P=1 normalization are valid only after those premises are granted; with no ledger one-hop dependency for the primitive coefficient and no retained carrier-identification theorem, the result cannot be promoted as a closed Planck-boundary density derivation. Repair target: register the primitive c_cell=1/4 theorem as a dependency, add a retained carrier-identification theorem deriving that the one-step boundary/worldtube count is the gravitational boundary/action carrier, and make the runner fail unless those inputs are present and retained. Claim boundary until fixed: it is safe to claim the exact finite-face extension: given locality, additivity, cubic-frame orientation symmetry, and primitive c_cell=1/4, every finite face-union patch has density c_cell/a^2, and if the gravitational carrier premise is later derived this extension preserves the conditional a/l_P=1 normalization.
- **open / conditional deps cited:**
  - `primitive_c_cell_equals_one_fourth_theorem_not_registered`
  - `gravitational_boundary_action_carrier_identification_theorem_open`
- **auditor confidence:** high

### `planck_finite_response_no_go_note_2026-04-24`

- **Note:** [`PLANCK_FINITE_RESPONSE_NO_GO_NOTE_2026-04-24.md`](../../docs/PLANCK_FINITE_RESPONSE_NO_GO_NOTE_2026-04-24.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_clean~~
- **effective_status:** **retained**  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The signed-permutation finite frame B_4 has min_{g != I} ||g-I||_F = 2 and therefore zero infinitesimal tangent, while linearized metric/coframe response requires nonzero Sym^2(R^4) directions of dimension 10.  _(class `A`)_
- **chain closes:** True — The note is scoped to a finite-automorphism-only no-go, and the source plus runner give an exact group-theoretic identity-gap/tangent-dimension obstruction. The retained parent-source hidden-character no-go is already audited clean and is cited only as an independent remaining-route boundary, not as a missing premise for this finite-response no-go.
- **rationale:** The claim is a bounded negative theorem about the finite-automorphism-only Planck route, not a positive Planck-scale derivation. The runner explicitly enumerates B_4, verifies |B_4|=384, proves the nearest nonidentity element is Frobenius distance 2, checks the empty infinitesimal neighborhood, contrasts zero finite-group tangent with the 10-dimensional symmetric metric-response space, and confirms the finite-dimensional trace obstruction for canonical commutators. Residual boundary: this clean audit only closes the finite automorphism route; it does not derive the gravitational carrier identification or rule out realified/canonical response surfaces.
- **auditor confidence:** high

### `planck_parent_source_hidden_character_no_go_note_2026-04-24`

- **Note:** [`PLANCK_PARENT_SOURCE_HIDDEN_CHARACTER_NO_GO_NOTE_2026-04-24.md`](../../docs/PLANCK_PARENT_SOURCE_HIDDEN_CHARACTER_NO_GO_NOTE_2026-04-24.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_clean~~
- **effective_status:** **retained**  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** Because C(c_cell, delta)=c_cell is constant on the affine hidden-character fiber while p_Schur(c_cell, delta)=c_cell+delta varies, p_Schur=p_event holds iff delta=0 and no carrier-only function can recover the Schur scalar on that fiber.  _(class `A`)_
- **chain closes:** True — The source note and runner prove the bounded no-go by an explicit two-point affine-fiber counterexample: identical carrier data produce different Schur scalars, so carrier commutation alone cannot force scalar equality.
- **rationale:** The claim is scoped as a negative no-go for the unconstrained carrier-only parent-source scalar route, not as a positive Planck coefficient derivation. The load-bearing hidden-character fiber is explicit in the source note and the runner verifies the kernel, two-parent counterexample, carrier-only non-recoverability, equivalence of scalar equality to delta=0, and normalization sensitivity. Residual boundary: this clean audit does not rule out a future no-hidden-character law or a direct gravitational carrier-identification theorem; it only closes the carrier-only route without such an extra law.
- **auditor confidence:** high

### `planck_source_unit_normalization_support_theorem_note_2026-04-25`

- **Note:** [`PLANCK_SOURCE_UNIT_NORMALIZATION_SUPPORT_THEOREM_NOTE_2026-04-25.md`](../../docs/PLANCK_SOURCE_UNIT_NORMALIZATION_SUPPORT_THEOREM_NOTE_2026-04-25.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_conditional~~
- **effective_status:** ~~audited_conditional~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The theorem converts the retained bare Green coefficient G_kernel=1/(4*pi) into a physical lattice Newton coefficient G_Newton,lat=1 by asserting that the primitive boundary/Wald area carrier identifies c_cell=1/4 with 1/(4G_lambda)=lambda/4, thereby fixing the exterior monopole mass scale lambda=1.  _(class `A`)_
- **chain closes:** False — The runner verifies the algebra of the source-unit family, the 4*pi conversion, the old bare-source mismatch, and the Planck-unit map after lambda=1. However, the audit has no registered one-hop dependency establishing the primitive boundary/Wald carrier identification, the exterior-observable additive source-charge theorem, the lattice Green theorem authority, or the Target 3 coframe-response bridge as audited clean. The note itself labels the result as a support theorem on a conditional Planck packet, so the chain remains conditional rather than closed.
- **rationale:** The internal calculation is coherent and the runner passes 14/14 checks: treating 1/(4*pi) as the bare unit-delta Green coefficient, parameterizing physical active mass as M_lambda=lambda C, matching c_cell=1/4 to lambda/4, and then obtaining q_bare=4*pi M_phys, G_Newton,lat=1, EH=c_cell/(4*pi), and a/l_P=1. The blocker is not arithmetic; it is the unproved load-bearing identification of the primitive cell count with the gravitational boundary/Wald area carrier and the unregistered exterior-source readout that gives the one-parameter mass family. Without those inputs, the audit can only say that the conditional Planck support packet is internally normalized. To repair the claim, register and audit a theorem proving that the primitive boundary/Wald carrier is the gravitational area/action carrier, register and audit the exterior-observable additive monopole source-charge theorem, and close or audit the Target 3 Clifford/coframe bridge that supplies the carrier route. What remains safe is the conditional statement: if the primitive boundary/Wald carrier premise and exterior source-charge theorem are accepted, then lambda=1 uniquely, the physical Newton coefficient in lattice units is one, and the previous 2*sqrt(pi) result is specifically the bare-source mislabeling failure mode. The audit does not support a standalone derivation of a=l_P, M_Pl, SI constants, hbar, or the primitive carrier itself.
- **open / conditional deps cited:**
  - `PLANCK_BOUNDARY_DENSITY_EXTENSION_THEOREM_NOTE_2026-04-24.md_audited_conditional_not_clean`
  - `PLANCK_PRIMITIVE_COFRAME_BOUNDARY_CARRIER_THEOREM_NOTE_2026-04-25.md_not_registered_or_not_audited_clean`
  - `PLANCK_TARGET3_CLIFFORD_PHASE_BRIDGE_THEOREM_NOTE_2026-04-25.md_not_registered_or_not_audited_clean`
  - `retained_lattice_Green_kernel_asymptotic_theorem_not_registered_as_one_hop_dependency`
  - `Gauss_asymptotic_monopole_readout_and_exterior_observability_additivity_source_charge_theorem_not_registered`
  - `primitive_boundary_Wald_carrier_identification_c_cell_equals_1_over_4_to_1_over_4G_lambda_not_registered_as_audited_clean`
  - `conventional_lP_squared_equals_Gphys_target_definition_external_not_a_CL3_derivation`
- **auditor confidence:** high

### `planck_target3_phase_unit_edge_statistics_boundary_note_2026-04-25`

- **Note:** [`PLANCK_TARGET3_PHASE_UNIT_EDGE_STATISTICS_BOUNDARY_NOTE_2026-04-25.md`](../../docs/PLANCK_TARGET3_PHASE_UNIT_EDGE_STATISTICS_BOUNDARY_NOTE_2026-04-25.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_clean~~
- **effective_status:** **retained**  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The boundary theorem shows that finite Hilbert/unitary flow supplies only U(1) phase data, is invariant under common action/action-quantum rescalings, and that the same rank-four active block supports both CAR/Majorana and non-CAR two-qubit or ququart semantics, so Hilbert flow alone cannot force an absolute action unit or primitive CAR edge statistics.  _(class `C`)_
- **chain closes:** True — The runner passes 27/27 checks and closes the stated boundary claim. It verifies phase periodicity, dependence only on S/kappa, rescaling invariance, inverse H/t scaling, scalar-action global phases, finite commutator trace obstruction, a valid two-mode CAR realization on C^4, Clifford/Majorana generation of M_4(C), CAR parity grading, and explicit non-CAR two-qubit and ququart semantics on the same rank-four Hilbert block with the same allowed unitary flow. These countermodels establish the no-go/boundary theorem without requiring a positive Target 2 or Target 3 closure.
- **rationale:** Clean for the bounded Target 3 statement. The positive part is exactly the native dimensionless U(1) phase unit. The negative parts are established by invariance and counterexample: amplitudes depend only on S/kappa, finite matrices cannot realize a nonzero exact canonical commutator by trace, and the rank-four block admits both CAR and non-CAR semantics while satisfying the same Hilbert-flow axioms. This clean audit does not derive hbar, a physical dimensional action unit, primitive CAR statistics, Target 2 c=1/4 unconditionality, or the later Clifford/coframe bridge; it only certifies that the current one-axiom Hilbert-flow surface is insufficient without additional edge-statistics/action-unit structure.
- **auditor confidence:** high

### `pmns_hw1_source_transfer_boundary_note`

- **Note:** [`PMNS_HW1_SOURCE_TRANSFER_BOUNDARY_NOTE.md`](../../docs/PMNS_HW1_SOURCE_TRANSFER_BOUNDARY_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_conditional~~
- **effective_status:** ~~audited_conditional~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** If the hw=1 source/transfer pack is supplied, the retained PMNS lane closes exactly; if only the sole axiom is supplied, the current exact bank still does not select the nontrivial source/transfer pack.  _(class `A`)_
- **chain closes:** False — The runner verifies a finite interface theorem: supplied transfer/source-response data recover the active/passive blocks and expose that transfer-only data are blind to the five-real active corner source. It does not derive the actual hw=1 source/transfer observables from Cl(3) on Z^3 or register the retained PMNS pair/readout authorities as one-hop dependencies.
- **rationale:** Issue: the proof closes only at the supplied-interface level; the source/transfer pack itself remains an external input to the runner. Why this blocks: the runner constructs synthetic neutral/charge sector fixtures, recovers blocks from response columns, and checks downstream closure by comparing the same closure routine against itself; it demonstrates that the interface is sufficient and that transfer-only summaries are insufficient, but it does not construct the physical hw=1 source/transfer observables from Cl(3) on Z^3 or independently identify the retained PMNS pair. Repair target: add a retained theorem and runner deriving the nontrivial hw=1 source/transfer pack from the sole axiom and registering the retained active/passive PMNS readout authorities as one-hop dependencies. Claim boundary until fixed: it is safe to claim a sharp conditional boundary that supplied hw=1 source/transfer columns remove the interface ambiguity while transfer-only data do not; it is not safe to claim retained PMNS closure from the sole axiom.
- **open / conditional deps cited:**
  - `Cl3_Z3_to_hw1_source_transfer_pack_derivation_not_registered`
  - `retained_PMNS_pair_readout_authority_not_registered_one_hop_dependency`
  - `physical_active_passive_source_transfer_observables_authority_not_registered`
  - `lower_level_source_transfer_observables_to_PMNS_readout_theorem_not_registered`
- **auditor confidence:** high

### `pmns_selector_three_identity_support_note_2026-04-21`

- **Note:** [`PMNS_SELECTOR_THREE_IDENTITY_SUPPORT_NOTE_2026-04-21.md`](../../docs/PMNS_SELECTOR_THREE_IDENTITY_SUPPORT_NOTE_2026-04-21.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_conditional~~
- **effective_status:** ~~audited_conditional~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The proposed three-equation system Tr(H) = Q_Koide, delta * q_+ = Q_Koide, and det(H) = E2 recovers one interior point whose PMNS observables lie in the runner's NuFit 5.3 normal-ordering 1 sigma bands.  _(class `G`)_
- **chain closes:** False — The runner verifies the candidate point and fit, but the two selector equations delta * q_+ = Q_Koide and det(H) = E2 are explicitly proposed laws rather than retained derivations, and uniqueness is only bounded multi-start evidence.
- **rationale:** Issue: The PMNS selector package depends on two proposed selector equations, delta * q_+ = Q_Koide and det(H) = E2, plus a bounded numerical uniqueness search; the runner then checks that the recovered point fits NuFit bands. Why this blocks: a retained PMNS selector theorem cannot rest on unproved candidate laws or heuristic one-cluster evidence, even though the numerical packet is reproducible. Repair target: derive both selector equations from retained framework structure, prove basin uniqueness analytically on the relevant chamber, and then rerun the PMNS observable comparison without treating the selector laws as assumptions. Claim boundary until fixed: it is safe to keep this as a support proposal with exact chart identities, a reproducible candidate point, and a strong numerical PMNS fit; it is not safe to claim retained PMNS selector closure.
- **open / conditional deps cited:**
  - `PMNS_SELECTOR_THREE_IDENTITY_SUPPORT_PROPOSAL_README_2026-04-21.md`
- **auditor confidence:** high

### `poisson_3d_self_field_note`

- **Note:** [`POISSON_3D_SELF_FIELD_NOTE.md`](../../docs/POISSON_3D_SELF_FIELD_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_conditional~~
- **effective_status:** ~~audited_conditional~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The scalar field is now fully a consequence of one local PDE on the lattice, not a starting assumption in any axis, and the 1/r profile, gravity TOWARD result, F proportional to M, and Born preservation all emerge from the same single equation.  _(class `C`)_
- **chain closes:** False — The runner solves a chosen finite 6-point static Poisson problem and reproduces the tested responses, but the Poisson equation, source normalization, boundary problem, and static-field interpretation are imposed rather than derived from retained axioms.
- **rationale:** Issue: The note treats the imposed 3D Poisson equation, delta-source normalization, finite-boundary solve, and static field as if they were derived scalar-field consequences of the model's axiom set. Why this blocks: the live runner verifies a finite computation after those choices are supplied, but it does not derive the Poisson law, source carrier, boundary conditions, normalization, or convergence theorem needed for retained field-derivation language. Repair target: prove or cite a retained theorem deriving the static Poisson equation and source/boundary normalization from the framework, add convergence/residual checks for the finite solve, and separate the computed finite Green-field response from the physical field-law claim. Claim boundary until fixed: it is safe to claim that, on the tested finite lattice and families, a chosen 6-point 3D Poisson stencil removes the explicit longitudinal 1/(dx+0.1) factor and reproduces TOWARD response, near-linear F versus M, Born preservation, and the s=0 null; it is not safe to claim the scalar field or 1/r law is retained as an axiom-derived theorem.
- **open / conditional deps cited:**
  - `POISSON_SELF_FIELD_NOTE.md`
  - `GATE_B_POISSON_SELF_GRAVITY_NOTE.md`
- **auditor confidence:** high

### `poisson_self_field_note`

- **Note:** [`POISSON_SELF_FIELD_NOTE.md`](../../docs/POISSON_SELF_FIELD_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_conditional~~
- **effective_status:** ~~audited_conditional~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The model's transverse field is no longer an input because it is a consequence of a local 2D Poisson PDE on each layer, while the longitudinal axis remains imposed.  _(class `C`)_
- **chain closes:** False — The live runner reproduces the finite Poisson-branch response, but the 2D Poisson equation, source normalization, boundary solve, and explicit 1/(dx+0.1) longitudinal factor are still supplied inputs rather than retained derivations.
- **rationale:** Issue: The note presents the transverse profile as derived from a local equation, but the local 2D Poisson equation, source normalization, boundary conditions, iteration budget, and the longitudinal 1/(dx+0.1) factor are still chosen inputs. Why this blocks: the live runner verifies a finite Poisson-branch computation after those premises are supplied, but it does not derive the field law or source carrier from retained framework structure, so the retained derivation claim is conditional. Repair target: derive or cite a retained theorem for the Poisson equation and source/boundary normalization, remove the explicit longitudinal factor or prove its retained origin, and add convergence/residual checks for the solver. Claim boundary until fixed: it is safe to claim that the tested runner replaces the transverse imposed profile with a chosen 2D Poisson stencil while preserving TOWARD response, near-linear F versus M, Born behavior, and the s=0 null; it is not safe to claim the gravitational field is retained as an axiom-derived consequence.
- **open / conditional deps cited:**
  - `GATE_B_POISSON_SELF_GRAVITY_NOTE.md`
- **auditor confidence:** high

### `poisson_self_gravity_mechanism_note`

- **Note:** [`POISSON_SELF_GRAVITY_MECHANISM_NOTE.md`](../../docs/POISSON_SELF_GRAVITY_MECHANISM_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_failed~~
- **effective_status:** ~~audited_failed~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The exact-lattice Poisson-like backreaction loop is a useful sanity check and an honest audit target, but it does not yet beat the bounded-control status.  _(class `B`)_
- **chain closes:** False — The note is a cross-note mechanism summary over unaudited or unknown support rows, and the only mechanism script is a hard-coded report rather than a runner that recomputes the controls.
- **rationale:** Issue: The queued proposed-retained row is not a retained mechanism claim on its own terms: the source status says control-only and not a proposed_retained self-gravity mechanism, the evidence notes it cites are unaudited or unknown, and the companion script only prints a hard-coded verdict. Why this blocks: the audit cannot ratify a proposed-retained mechanism or even a retained synthesis from unaudited support rows and a non-computational report script. Repair target: demote the source status to bounded/control-only or rebuild it as a ledger-generated synthesis after auditing POISSON_SELF_GRAVITY_LOOP_NOTE, POISSON_SELF_GRAVITY_BORN_AUDIT_NOTE, and POISSON_SELF_GRAVITY_LOOP_V3_NOTE; remove the embedded patch text from the markdown and make the runner recompute the controls. Claim boundary until fixed: it is safe to use this as an editorial control-only handoff saying no retained self-gravity mechanism has closed; it is not safe to treat it as an audit-retained self-gravity mechanism or retained mechanism synthesis.
- **open / conditional deps cited:**
  - `POISSON_SELF_GRAVITY_LOOP_NOTE.md`
  - `POISSON_SELF_GRAVITY_BORN_AUDIT_NOTE.md`
  - `POISSON_SELF_GRAVITY_LOOP_V3_NOTE.md`
- **auditor confidence:** high

### `portable_card_extension_note`

- **Note:** [`PORTABLE_CARD_EXTENSION_NOTE.md`](../../docs/PORTABLE_CARD_EXTENSION_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_failed~~
- **effective_status:** ~~audited_failed~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The portable package extends cleanly onto the three-family card, while the distance law remains the main holdout subset on the current family-3 probe.  _(class `B`)_
- **chain closes:** False — The runner computes only the family-3 source-placement collapse; it hard-codes the retained card baseline, and the named card/portability dependencies are unaudited, conditional, or unknown.
- **rationale:** Issue: The claimed retained extension imports the three-family card and portable package as retained authorities, but THREE_FAMILY_CARD_NOTE and PORTABLE_PACKAGE_EXTENSION_NOTE are unaudited, SIGN_PORTABILITY_INVARIANT_NOTE and DISTANCE_LAW_BREAKPOINT_NOTE are audited_conditional, DISTANCE_LAW_PORTABILITY_NOTE is unknown, and the frozen log named by the source is absent. Why this blocks: the live runner verifies only that the family-3 distance-law probe collapses to one selected source node; it does not recompute or prove the portable package core across the three-family card, so the retained extension conclusion is unsupported. Repair target: audit or repair the card and portability dependencies, restore the frozen log, and replace the hard-coded retained table with a runner that recomputes the portable-core checks from first principles for all three families. Claim boundary until fixed: it is safe to say the current family-3 distance-law harness has a source-placement coverage failure and therefore is not a physics contradiction; it is not safe to claim an audit-retained portable package extension onto the three-family card.
- **open / conditional deps cited:**
  - `THREE_FAMILY_CARD_NOTE.md`
  - `PORTABLE_PACKAGE_EXTENSION_NOTE.md`
  - `SIGN_PORTABILITY_INVARIANT_NOTE.md`
  - `DISTANCE_LAW_BREAKPOINT_NOTE.md`
  - `DISTANCE_LAW_PORTABILITY_NOTE.md`
- **auditor confidence:** high

### `portable_package_extension_note`

- **Note:** [`PORTABLE_PACKAGE_EXTENSION_NOTE.md`](../../docs/PORTABLE_PACKAGE_EXTENSION_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_failed~~
- **effective_status:** ~~audited_failed~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The portable fixed-field package extends beyond the first two grown families, but only the sign-law core is broadly portable while the distance law and complex-action branches are stricter subsets.  _(class `B`)_
- **chain closes:** False — The runner is a static summary table and does not recompute the sign, distance, or complex-action rows; the named authorities are conditional, unaudited, or unknown.
- **rationale:** Issue: The retained comparison treats sign portability, distance-law portability, and complex-action selectivity as already established across multiple families, but the cited authorities are not audit-clean: SIGN_PORTABILITY_INVARIANT_NOTE is audited_conditional, DISTANCE_LAW_PORTABILITY_NOTE and COMPLEX_SELECTIVITY_COMPARE_NOTE are unknown/unaudited, and the runner only prints a hard-coded comparison table. Why this blocks: a retained cross-family package extension requires computed or audited-clean support for every family row, not a static table over unratified inputs. Repair target: audit or repair the sign, distance-law, and complex-action source notes, then replace the static table with a runner that recomputes the zero/neutral/sign/slope, distance-tail, and complex-action checks for each listed family. Claim boundary until fixed: it is safe to present this as an editorial portability taxonomy or worklist; it is not safe to claim an audit-retained portable fixed-field package extension beyond the first two grown families.
- **open / conditional deps cited:**
  - `SIGN_PORTABILITY_INVARIANT_NOTE.md`
  - `DISTANCE_LAW_PORTABILITY_NOTE.md`
  - `COMPLEX_SELECTIVITY_COMPARE_NOTE.md`
- **auditor confidence:** high

### `propagator_family_unification_note`

- **Note:** [`PROPAGATOR_FAMILY_UNIFICATION_NOTE.md`](../../docs/PROPAGATOR_FAMILY_UNIFICATION_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_conditional~~
- **effective_status:** ~~audited_conditional~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The retained wavefield, complex-action, and electrostatics results all share a common fixed-propagator skeleton with scalar edge-level coupling laws.  _(class `B`)_
- **chain closes:** False — The synthesis depends on SOURCE_RESOLVED_WAVEFIELD_MECHANISM_NOTE, which is still unaudited, and there is no synthesis runner that recomputes the common skeleton only from audit-clean inputs.
- **rationale:** Issue: The unification note imports SOURCE_RESOLVED_WAVEFIELD_MECHANISM_NOTE as a retained wavefield authority, but that source row is still unaudited while the synthesis has no runner or ledger-derived table. Why this blocks: the common-propagator taxonomy may be plausible, but a retained unification claim cannot depend on an unaudited load-bearing lane. Repair target: audit or repair the source-resolved wavefield mechanism note, then rebuild this synthesis from audit_ledger effective_status or add a small runner/table that only includes audit-clean lanes. Claim boundary until fixed: it is safe to say the already clean complex-action and electrostatics lanes share a fixed-propagator/scalar-coupling pattern, and that the source-resolved wavefield lane is a candidate member; it is not safe to retain the full three-lane propagator-family unification.
- **open / conditional deps cited:**
  - `SOURCE_RESOLVED_WAVEFIELD_MECHANISM_NOTE.md`
- **auditor confidence:** high

### `qnm_control_hardening_note`

- **Note:** [`QNM_CONTROL_HARDENING_NOTE.md`](../../docs/QNM_CONTROL_HARDENING_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_failed~~
- **effective_status:** ~~audited_failed~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** QNM remains a hardening target, not a retained spectral claim, until the listed control program is frozen.  _(class `B`)_
- **chain closes:** False — The source is a roadmap/checklist with no runner, no cited audited controls, and an explicit statement that there is no proposed-retained spectral claim yet.
- **rationale:** Issue: The queued row is proposed_retained only because the status line contains that token in a negation; the note itself says this is a bounded control program only and not a proposed_retained spectral claim. Why this blocks: there is no runner, frozen null, matched control, Born audit, Nyquist exclusion, or refinement/threshold stability result to audit as a retained QNM claim. Repair target: demote the source status to bounded/open roadmap language, then add the five named controls and a runner that computes them before proposing a spectral claim. Claim boundary until fixed: it is safe to cite this as a QNM hardening checklist and as evidence that the branch-side QNM story remains blocked; it is not safe to treat it as an audit-retained QNM result or retained spectral-control theorem.
- **open / conditional deps cited:**
  - `QNM_HARDENING_FEASIBILITY_NOTE.md`
- **auditor confidence:** high

### `quantum_horizon_note`

- **Note:** [`QUANTUM_HORIZON_NOTE.md`](../../docs/QUANTUM_HORIZON_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_conditional~~
- **effective_status:** ~~audited_conditional~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** On this horizon observable, alpha_crit is nearly flat in k, so the retained family does not support a strong wavelength-dependent horizon shift.  _(class `C`)_
- **chain closes:** False — The live k-sweep closes as a finite proxy no-go, but it inherits the absorbing-horizon proxy from MINIMAL_ABSORBING_HORIZON_PROBE_NOTE, which is audited_failed as a retained horizon/trapping theorem.
- **rationale:** Issue: The k-sweep verifies flat alpha_crit only for the hand-inserted absorbing proxy inherited from the minimal absorbing-horizon probe, whose retained horizon/trapping interpretation has already failed audit. Why this blocks: the result can kill a stronger wavelength-dependent story for this proxy observable, but it cannot be retained as a quantum-horizon or retained-absorbing-family statement until the underlying absorption law and family claim are repaired. Repair target: either demote this note to a bounded proxy no-go, or first derive and audit the absorption/horizon law in the minimal probe, then rerun the k-sweep as a retained-family observable. Claim boundary until fixed: it is safe to say the live proxy sweep gives alpha_crit around 0.08 to 0.09 with exponent about 0.03 across the tested k values; it is not safe to claim a retained quantum-horizon law or retained absorbing-horizon mechanism.
- **open / conditional deps cited:**
  - `MINIMAL_ABSORBING_HORIZON_PROBE_NOTE.md`
- **auditor confidence:** high

### `quark_bicac_endpoint_obstruction_theorem_note_2026-04-19`

- **Note:** [`QUARK_BICAC_ENDPOINT_OBSTRUCTION_THEOREM_NOTE_2026-04-19.md`](../../docs/QUARK_BICAC_ENDPOINT_OBSTRUCTION_THEOREM_NOTE_2026-04-19.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_clean~~
- **effective_status:** **retained**  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The current retained ray/support packet leaves kappa unfixed because the same packet identities remain true at sqrt(6/7), 48/49, and 1, giving a positive-width bridge interval rather than forcing the BICAC endpoint.  _(class `A`)_
- **chain closes:** True — The source theorem is exact algebra over its stated packet atoms, and the live runner verifies all twelve identities: support endpoint, target point, BICAC endpoint, ordering, positive interval width, and kappa-independence of the packet invariants.
- **rationale:** The claim is a negative algebraic obstruction, not a positive BICAC derivation. Given the stated packet atoms p, r, a_d, supp, and delta_A1, the runner verifies three distinct exact kappa points and shows the retained packet invariants do not select among them. Residual risk is limited to provenance of the packet atoms outside this note; this audit retains only the obstruction that the present ray/support packet does not force kappa = 1.
- **auditor confidence:** high

### `quark_bimodule_lo_shell_normalization_theorem_note_2026-04-19`

- **Note:** [`QUARK_BIMODULE_LO_SHELL_NORMALIZATION_THEOREM_NOTE_2026-04-19.md`](../../docs/QUARK_BIMODULE_LO_SHELL_NORMALIZATION_THEOREM_NOTE_2026-04-19.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_conditional~~
- **effective_status:** ~~audited_conditional~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** Because the shell slot is the common unit LO channel, the retained down amplitude a_d = rho forces the physical LO down action D_LO(x) = rho x and therefore kappa = 1.  _(class `F`)_
- **chain closes:** False — The runner verifies the algebra after identifying the exact shell carrier coefficient with the physical LO down amplitude rho, but the carrier/readout map and rho provenance rows are not audit-clean retained inputs.
- **rationale:** Issue: The proof selects kappa = 1 by requiring the shell-normalized carrier coefficient to equal the retained physical down amplitude rho, but the physical bridge from the exact Route-2 carrier/readout map to the LO down action is not itself audit-retained, and rho provenance is imported from non-clean rows. Why this blocks: the runner checks exact algebra after the identification is supplied; it does not independently derive that the shell coefficient is the physical down-amplitude readout, nor does it close the unaudited/conditional CKM and quark projector inputs. Repair target: audit or repair CKM_ATLAS_AXIOM_CLOSURE_NOTE, QUARK_PROJECTOR_PARAMETER_AUDIT_NOTE, and QUARK_ROUTE2_EXACT_READOUT_MAP_NOTE, and add a theorem deriving the shell-carrier-to-physical-down-action map before promoting BICAC closure. Claim boundary until fixed: it is safe to say that, given the stated shell carrier and rho readout premise, only kappa = 1 preserves the shell coefficient and yields STRC-LO; it is not safe to claim retained physical BICAC derivation from the current audited inputs.
- **open / conditional deps cited:**
  - `CKM_ATLAS_AXIOM_CLOSURE_NOTE.md`
  - `QUARK_PROJECTOR_PARAMETER_AUDIT_NOTE_2026-04-19.md`
  - `QUARK_ROUTE2_EXACT_READOUT_MAP_NOTE_2026-04-19.md`
- **auditor confidence:** high

### `quark_bimodule_norm_existence_theorem_note_2026-04-19`

- **Note:** [`QUARK_BIMODULE_NORM_EXISTENCE_THEOREM_NOTE_2026-04-19.md`](../../docs/QUARK_BIMODULE_NORM_EXISTENCE_THEOREM_NOTE_2026-04-19.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_conditional~~
- **effective_status:** ~~audited_conditional~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** For any retained kappa in [sqrt(6/7), 1], define D_kappa := rho*kappa*Id_I and U_kappa := (1 - rho*kappa)*Id_I, so U_kappa + D_kappa = Id_I and U_kappa(Im(p)) reproduces a_u(kappa).  _(class `A`)_
- **chain closes:** False — The one-dimensional scalar-map construction closes algebraically, but the source note imports the retained CKM projector ray, rho, and physical bridge/readout family without an audit-clean cited chain.
- **rationale:** Issue: The proof constructs complementary scalar endomorphisms on I once the CKM projector ray, rho, and bridge family a_u(kappa) are supplied, but those physical inputs and the readout identifying the scalar maps with LO quark ownership response are not closed by audit-clean dependencies in this note. Why this blocks: the runner verifies algebra after the bridge family and channel/readout interpretation have been supplied; it does not derive that I = R*Im(p), rho = 1/sqrt(42), or the kappa interval are retained physical inputs for an LO bimodule law. Repair target: add or cite an audit-clean theorem deriving the CKM projector/rho data and the Route-2 carrier/readout map into the LO bimodule channel, then rerun the NORM-existence runner as a consequence of those inputs. Claim boundary until fixed: it is safe to claim that, conditional on the stated one-dimensional channel and bridge-family premises, the displayed D_kappa and U_kappa are complementary positive contractions and reproduce the three scalar amplitudes; it is not safe to claim retained physical LO split-law existence from the current audited chain.
- **open / conditional deps cited:**
  - `CKM_ATLAS_AXIOM_CLOSURE_NOTE.md`
  - `QUARK_PROJECTOR_PARAMETER_AUDIT_NOTE_2026-04-19.md`
  - `QUARK_ROUTE2_EXACT_READOUT_MAP_NOTE_2026-04-19.md`
- **auditor confidence:** high

### `quark_lane3_bounded_companion_retention_firewall_note_2026-04-27`

- **Note:** [`QUARK_LANE3_BOUNDED_COMPANION_RETENTION_FIREWALL_NOTE_2026-04-27.md`](../../docs/QUARK_LANE3_BOUNDED_COMPANION_RETENTION_FIREWALL_NOTE_2026-04-27.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_clean~~
- **effective_status:** **retained**  (reason: `self`)
- **auditor:** `codex-audit-loop:fresh-2026-04-28-quark_lane3_bounded_companion_retention_firewall_note_2026-04-27`  (codex-current; independence=fresh_context)
- **load-bearing step:** Absent those premises, the existing packet remains bounded companion support.  _(class `A`)_
- **chain closes:** True — The claim is a negative boundary: the note does not derive non-top quark masses, but shows that the current package supplies bounded ratio/support surfaces, not absolute five-mass retention. The live runner verifies repo status guardrails, arbitrary bottom-anchor freedom for down-type ratios, up-type partition dependence, species-uniform Ward failure for m_b, and the safe open endpoint with PASS=17 FAIL=0.
- **rationale:** The retained content is the Lane 3 firewall, not five-mass retention. The note's load-bearing step closes because the down-type formulas are ratios that preserve an arbitrary bottom anchor, the up-type branch remains partition/scalar-law selected, and the top Ward identity cannot be reused species-uniformly because the b reading overshoots by about 34.7x. The live runner confirms the relevant repo guardrails and comparator-only use of observed masses. Residual risk is downstream misuse: this audit does not ratify m_u, m_d, m_s, m_c, m_b, the 5/6 bridge, up-sector amplitude selection, or non-top Yukawa Ward identities.
- **auditor confidence:** high

### `quark_strc_observable_principle_note_2026-04-19`

- **Note:** [`QUARK_STRC_OBSERVABLE_PRINCIPLE_NOTE_2026-04-19.md`](../../docs/QUARK_STRC_OBSERVABLE_PRINCIPLE_NOTE_2026-04-19.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_failed~~
- **effective_status:** ~~audited_failed~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** Retention of STRC as an observable principle is the minimal path to closing the quark up-amplitude gate, with a_u + rho*sin(delta_std) = sin(delta_std) taken as the STRC-LO relation.  _(class `E`)_
- **chain closes:** False — The note explicitly frames STRC as an observable principle rather than a theorem and says it is superseded route history; the runner assumes a_u_LO = sin_d*(1-rho) before checking STRC and RPSR consequences.
- **rationale:** Issue: The proposed-retained claim is a superseded route-history observable-principle framing, and its runner hard-codes a_u_LO = sin_d*(1-rho) before verifying STRC and RPSR identities. Why this blocks: finite rule-outs of several candidate sources plus algebraic consequences of an assumed relation do not derive the STRC relation or justify retaining this note as the primary source, and the note itself directs readers to a separate collinearity theorem for derivation. Repair target: demote this note to route-history/support, or audit and promote an explicit theorem such as STRC_LO_COLLINEARITY_THEOREM_NOTE with audit-clean CKM/projector/scalar-ray inputs and a runner that derives a_u rather than setting it. Claim boundary until fixed: it is safe to say that if STRC-LO is assumed then the displayed identities, RPSR closure, and finite candidate rule-outs in the runner hold; it is not safe to claim this note retains or derives STRC as a physical observable principle.
- **open / conditional deps cited:**
  - `STRC_LO_COLLINEARITY_THEOREM_NOTE_2026-04-19.md`
  - `QUARK_UP_AMPLITUDE_RPSR_CONDITIONAL_THEOREM_NOTE_2026-04-19.md`
  - `QUARK_PROJECTOR_PARAMETER_AUDIT_NOTE_2026-04-19.md`
  - `CKM_ATLAS_AXIOM_CLOSURE_NOTE.md`
  - `SCALAR_TENSOR_RAY_MAGNITUDE_BRIDGE_NOTE_2026-04-19.md`
- **auditor confidence:** high

### `replay_environment_note`

- **Note:** [`REPLAY_ENVIRONMENT_NOTE.md`](../../docs/REPLAY_ENVIRONMENT_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_failed~~
- **effective_status:** ~~audited_failed~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** Retained numpy replay scripts on this machine should either be launched with /usr/bin/python3 or call scripts/numpy_replay_bootstrap.py before importing numpy-heavy modules.  _(class `B`)_
- **chain closes:** False — The note is a host-specific reproducibility convention, not a retained physics result, and it has no runner or audit-clean environment check proving the interpreter/numpy claims are stable across replay contexts.
- **rationale:** Issue: The row is parsed as proposed_retained from a note whose own content says the scientific claims do not change and records a local machine interpreter convention rather than a physics theorem. Why this blocks: a host-specific PATH/numpy observation without a runner, lockfile, or CI check cannot carry retained-claim status in the audit ledger, and retaining it would confuse operational reproducibility guidance with scientific evidence. Repair target: demote the note to support/replay documentation, or add a deterministic environment-check runner plus a pinned replay environment contract if a retained reproducibility artifact is actually intended. Claim boundary until fixed: it is safe to say that on the documented machine the replay convention is to use /usr/bin/python3 or the bootstrap helper; it is not safe to claim this note as retained physics or retained scientific support beyond local replay hygiene.
- **auditor confidence:** high

### `retained_cross_lane_consistency_support_note_2026-04-22`

- **Note:** [`RETAINED_CROSS_LANE_CONSISTENCY_SUPPORT_NOTE_2026-04-22.md`](../../docs/RETAINED_CROSS_LANE_CONSISTENCY_SUPPORT_NOTE_2026-04-22.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_decoration~~
- **effective_status:** ~~audited_decoration~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The support runner cross-checks 26 proposed_retained numerical and algebraic identities across eight separately proposed_retained lanes in a single executable, but does not derive anything new.  _(class `B`)_
- **chain closes:** False — The runner passes 26/26 as a regression harness over supplied lane anchors. It hard-codes numerical and algebraic inputs from multiple lanes, registers no one-hop dependencies, and includes tolerance/True checks, so it does not close as an independent proposed-retained theorem.
- **rationale:** Issue: the note is a cross-lane bookkeeping and drift-detection harness, not an independent physical derivation. Why this blocks: the primary runner supplies anchors such as alpha_s(v), alpha_LM, Q_Koide, delta_Brannen, v_EW, anomaly traces, cosmological identities, and neutrino staircase values, then checks algebraic/tolerance consistency; the row has no registered one-hop authorities and the source note itself says it derives nothing new and discharges no residual. Repair target: keep it as a support/regression harness or box it under the relevant parent audit packet; re-promote only if it registers every upstream authority, all upstream lanes are audited clean, and the runner proves a genuine compression theorem rather than restating supplied constants. Claim boundary until fixed: it is safe to cite this as a useful executable coherence checklist for supplied lane values; it is not safe to count it as a separate retained theorem-grade result.
- **open / conditional deps cited:**
  - `ALPHA_S_DERIVED_NOTE.md_not_registered_one_hop_dependency`
  - `PLAQUETTE_SELF_CONSISTENCY_NOTE.md_not_registered_one_hop_dependency`
  - `CKM_ATLAS_AXIOM_CLOSURE_NOTE.md_not_registered_one_hop_dependency`
  - `KOIDE_SELECTED_LINE_PROVENANCE_NOTE_2026-04-20.md_not_registered_one_hop_dependency`
  - `PMNS_SELECTOR_THREE_IDENTITY_SUPPORT_NOTE_2026-04-21.md_not_registered_one_hop_dependency`
  - `ANOMALY_FORCES_TIME_THEOREM.md_not_registered_one_hop_dependency`
  - `COSMOLOGICAL_CONSTANT_SPECTRAL_GAP_IDENTITY_THEOREM_NOTE.md_not_registered_one_hop_dependency`
  - `DARK_ENERGY_EOS_RETAINED_COROLLARY_THEOREM_NOTE.md_not_registered_one_hop_dependency`
  - `NEUTRINO_MASS_DERIVED_NOTE.md_not_registered_one_hop_dependency`
  - `KOIDE_Q_EQ_3DELTA_IDENTITY_NOTE_2026-04-21.md_not_registered_one_hop_dependency`
- **auditor confidence:** high

### `retardation_discriminator_note`

- **Note:** [`RETARDATION_DISCRIMINATOR_NOTE.md`](../../docs/RETARDATION_DISCRIMINATOR_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_conditional~~
- **effective_status:** ~~audited_conditional~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The retardation discriminator is a retained, portable observable that distinguishes finite-propagation-speed field response from instantaneous response to the same oscillating source.  _(class `C`)_
- **chain closes:** False — The artifact chain computes a nonzero delayed-vs-instantaneous phase difference for the implemented toy harness, but the retained/general discriminator claim is not backed by a fast assertion runner or a theorem excluding all instantaneous emulator models.
- **rationale:** Issue: The source and frozen log show a delayed-source toy harness with nonzero frequency- and delay-dependent phase differences, but the canonical script has no PASS/FAIL assertion contract and the live audit run did not complete the full global-delay/family/seed sections before interruption after more than ten minutes. Why this blocks: a finite parameter sweep in one implemented propagation model does not by itself prove a retained, portable observable or rule out all instantaneous responses with memory, phase offsets, or fitted transfer functions. Repair target: add a fast deterministic runner with explicit assertions for the nulls, delay law, family/seed robustness, and global-delay fit residual, and add a theorem specifying the model class in which no instantaneous/static response can reproduce the first-harmonic delayed-response observable. Claim boundary until fixed: it is safe to claim that the frozen harness output and partial live run show a delayed-vs-instantaneous phase difference for the stated oscillating-source model and parameters; it is not safe to claim a retained general finite-propagation discriminator across physical response models.
- **auditor confidence:** medium

### `retarded_field_compact_refinement_note`

- **Note:** [`RETARDED_FIELD_COMPACT_REFINEMENT_NOTE.md`](../../docs/RETARDED_FIELD_COMPACT_REFINEMENT_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_conditional~~
- **effective_status:** ~~audited_conditional~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The retarded field does not collapse to the instantaneous row on refinement, but the split is not uniformly one-directional across the compact and refined rows.  _(class `C`)_
- **chain closes:** False — The runner reproduces a bounded two-family smoke-probe readout, but the proposed-retained surface is stronger than the evidence because the result is partial, row-sign-dependent, and not attached as an assertion runner in the ledger.
- **rationale:** Issue: The script and frozen log support only partial survival of a retarded-vs-instantaneous centroid-shift split on two retained DAG-family parameter choices, with nonuniform row signs and sizable standard errors, while the audit queue exposes the row as proposed_retained. Why this blocks: a two-family smoke probe without assertion tolerances or a stated statistical/refinement theorem cannot establish a retained retarded-field law or a robust universal discriminator. Repair target: change the source status to bounded/support, or add a ledger-attached assertion runner plus a refinement theorem/statistical criterion showing noncollapse over a specified family class with tolerances. Claim boundary until fixed: it is safe to claim that the current script reproduces nonzero mean splits for the compact and refined families and that the refined split is not uniformly one-directional; it is not safe to claim retained universal retarded-field behavior from this probe.
- **auditor confidence:** high

### `s3_mass_matrix_no_go_note`

- **Note:** [`S3_MASS_MATRIX_NO_GO_NOTE.md`](../../docs/S3_MASS_MATRIX_NO_GO_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_clean~~
- **effective_status:** **retained**  (reason: `self`)
- **auditor:** `codex-audit-loop:fresh-2026-04-27-s3_mass_matrix_no_go_note`  (codex-current; independence=fresh_context)
- **load-bearing step:** Since V ~= A_1 + E for the natural S_3 action on the hw=1 triplet, every S_3-invariant Hermitian operator has the form M = alpha I_3 + beta P_(A_1), hence spectrum {alpha, alpha, alpha + beta}.  _(class `A`)_
- **chain closes:** True — The source note states a conditional representation-theory theorem on the hw=1 triplet, and the runner constructs the S_3 action, invariant algebra, two-value spectrum, and Z_2 dimension jump directly. The claim does not require a phenomenological mass identification beyond its explicit carrier boundary.
- **rationale:** The retained content is an exact, bounded no-go theorem: on the stated hw=1 S_3 permutation carrier, Schur decomposition and direct invariant-algebra computation force only a singlet projector plus identity and therefore at most two spectral values. The live runner reports PASS=13 FAIL=0, including the S_3 invariant dimension, projector form, spectrum checks, and residual Z_2 dimension 5. Residual risk is only misuse downstream: this audit does not ratify that hw=1 is the physical generation carrier or any numerical flavor fit.
- **auditor confidence:** high

### `s3_taste_cube_decomposition_note`

- **Note:** [`S3_TASTE_CUBE_DECOMPOSITION_NOTE.md`](../../docs/S3_TASTE_CUBE_DECOMPOSITION_NOTE.md)
- **current_status:** support
- **audit_status:** ~~audited_conditional~~
- **effective_status:** ~~audited_conditional~~  (reason: `self`)
- **auditor:** `codex-audit-loop:fresh-2026-04-28-s3_taste_cube_decomposition_note`  (codex-current; independence=fresh_context)
- **load-bearing step:** The exact S3 character calculation on the full taste cube gives C^8 ~= 4 A_1 + 2 E, with no A_2 component.  _(class `C`)_
- **chain closes:** False — The S3 axis-permutation representation calculation on C^8 closes exactly, and the live runner reports PASS=57 FAIL=0. The note explicitly limits the result to canonical carrier-content support and does not close any downstream flavor or generation claim.
- **rationale:** Issue: the full-cube S3 decomposition is exact, but the note itself says it does not prove any flavor claim and only fixes the carrier content later tools may use.
Why this blocks: downstream proposed-retained/promoted claims cannot treat this row as a physical generation/flavor derivation; it supplies representation support, not an observable bridge.
Repair target: add and audit the missing theorem that maps the S3 carrier decomposition to the claimed physical flavor or generation observable, with a runner checking that bridge.
Claim boundary until fixed: safe to claim C^8 ~= 4 A_1 + 2 E and no A_2 under axis permutations on the taste cube, not any standalone flavor, CKM, or generation closure.
- **open / conditional deps cited:**
  - `downstream_flavor_generation_claim_not_closed_by_carrier_decomposition`
  - `physical_observable_mapping_from_s3_carrier_content_missing`
- **auditor confidence:** high

### `second_grown_family_complex_note`

- **Note:** [`SECOND_GROWN_FAMILY_COMPLEX_NOTE.md`](../../docs/SECOND_GROWN_FAMILY_COMPLEX_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_conditional~~
- **effective_status:** ~~audited_conditional~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The retained anchor row does carry the complex-action companion, while the support is selective and not family-wide.  _(class `C`)_
- **chain closes:** False — The script reproduces the narrow anchor-row diagnostics, but the second-family provenance/sign note is unaudited and the runner prints booleans rather than enforcing an audit assertion contract.
- **rationale:** Issue: The complex-action script and frozen log support the drift=0.20 anchor-row diagnostics, but the note relies on SECOND_GROWN_FAMILY_SIGN_NOTE for the independent second-family provenance and that dependency is currently unaudited/unknown; the runner also has no PASS/FAIL assertion contract. Why this blocks: a selective anchor-row positive cannot be promoted as retained until the family slice it rests on is audit-clean and the acceptance gates are executable assertions rather than printed diagnostics. Repair target: audit the second grown-family sign/provenance note, attach an assertion runner with tolerances for Born proxy, gamma=0, F~M, and TOWARD->AWAY gates, and state the anchor-selection rule explicitly. Claim boundary until fixed: it is safe to claim that the current script/log show the no-restore geometry-sector drift=0.20 anchor row passes the listed complex-action diagnostics; it is not safe to claim a retained second grown-family complex-action result beyond that conditional anchor slice.
- **open / conditional deps cited:**
  - `SECOND_GROWN_FAMILY_SIGN_NOTE.md`
- **auditor confidence:** high

### `second_grown_family_note`

- **Note:** [`SECOND_GROWN_FAMILY_NOTE.md`](../../docs/SECOND_GROWN_FAMILY_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_failed~~
- **effective_status:** ~~audited_failed~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** 9 candidate families tested, with best second candidate drift=0.05, restore=0.30, passing the full control battery for F~M, Born, gravity TOWARD, and complex-action crossover.  _(class `C`)_
- **chain closes:** False — The only cited battery script is absent from the repository and is described as 'to be frozen', so the numeric control battery cannot be rerun or checked from the provided artifact chain.
- **rationale:** Issue: The note's retained positive result rests on a missing artifact, scripts/second_grown_family_battery.py, explicitly labeled as not yet frozen, and no frozen output is provided in the artifact chain. Why this blocks: the quoted F~M, Born, gravity, and complex-action control-battery numbers are unreviewable from the allowed source and artifacts, so the proposed-retained second-family claim cannot be independently reproduced or checked. Repair target: restore or recreate the exact battery script, add a frozen log and preferably a PASS/FAIL assertion runner, or replace this note with audit-clean sign/complex second-family notes that actually carry the evidence. Claim boundary until fixed: it is safe to say this note records a historical candidate at drift=0.05, restore=0.30; it is not safe to claim a retained second independent grown family from the current artifact chain.
- **auditor confidence:** high

### `self_gravity_entropy_note_2026-04-11`

- **Note:** [`SELF_GRAVITY_ENTROPY_NOTE_2026-04-11.md`](../../docs/SELF_GRAVITY_ENTROPY_NOTE_2026-04-11.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_clean~~
- **effective_status:** **retained**  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** This simple entropy observable does not currently support an area-law claim; it is capped at ln(2) and controlled primarily by the mass split p_A rather than boundary complexity.  _(class `C`)_
- **chain closes:** True — The runner reproduces the exact table values and the cautious negative readout: boundary correlations are inconsistent across families and the observable is a binary single-particle occupancy entropy capped by ln(2).
- **rationale:** The claim is a negative/inconclusive boundary, not a positive area-law theorem. The current runner reproduces the note's entropy shifts and mixed boundary correlations, and the note explicitly limits the conclusion to topology-sensitive occupancy entropy with no robust boundary-controlled scaling. Residual risk is only that the broader self-gravity lane remains a model context; the audited claim here is the narrower no-area-law diagnostic for this simple observable.
- **auditor confidence:** high

### `session_summary_2026-04-01_topology`

- **Note:** [`SESSION_SUMMARY_2026-04-01_TOPOLOGY.md`](../../docs/SESSION_SUMMARY_2026-04-01_TOPOLOGY.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_failed~~
- **effective_status:** ~~audited_failed~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** Both gravity and decoherence work on the same graph family, with a broad joint modular window and soft-pruning emergence closed asymptotically.  _(class `B`)_
- **chain closes:** False — The file is a broad session-summary synthesis over many scripts/logs, has no runner, and points to unaudited or failed companion notes rather than audit-clean dependencies.
- **rationale:** Issue: The proposed-retained architecture result is a session summary aggregating many gravity, decoherence, topology, pruning, and emergence claims without a single retained theorem, runner, frozen assertion surface, or audit-clean dependency chain. Why this blocks: a synthesis note that even flags optimistic standard-error wording and provisional follow-ups cannot itself establish the broad claim that gravity and decoherence work on the same graph family or that emergence lanes are closed. Repair target: split the summary into auditable claim notes, each with its own runner/log and explicit dependencies, then retain only the scoped results that survive audit; leave this file as session history. Claim boundary until fixed: it is safe to use this note as a dated roadmap and index of scripts/logs from the topology-pivot session; it is not safe to cite it as retained evidence for the architecture claims.
- **open / conditional deps cited:**
  - `HIGHER_DIMENSION_STATUS_2026-04-01.md`
  - `IF_PROGRAM_CLOSING_NOTE.md`
  - `DECOHERENCE_FAILURE_ANALYSIS.md`
- **auditor confidence:** high

### `session_synthesis_2026-04-10_graph_axioms`

- **Note:** [`SESSION_SYNTHESIS_2026-04-10_GRAPH_AXIOMS.md`](../../docs/SESSION_SYNTHESIS_2026-04-10_GRAPH_AXIOMS.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_failed~~
- **effective_status:** ~~audited_failed~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** This session ended with a new axiom set that passes the full 16-row audited core card on three different graph topologies, but current proposed-retained staggered status is tracked by successor force-based cards.  _(class `B`)_
- **chain closes:** False — The specified runner passes its legacy proxy checks, but both the note and runner state that this is historical and not a current-main evidence surface for retained status.
- **rationale:** Issue: The row is a historical synthesis note whose declared runner is explicitly labeled a legacy proxy harness and prints 'Do not use this script as a current-main evidence surface.' Why this blocks: a 16/16 legacy proxy run cannot ratify the broad graph-axiom or current staggered proposed-retained claim, especially when the note says current status is tracked by successor cards with different semantics. Repair target: demote this file to historical synthesis/support and audit the current force-based staggered card, corrected graph-KG card, and any portability cards as separate runner-backed claims. Claim boundary until fixed: it is safe to say the legacy harness currently reproduces 16/16 proxy scores on cubic, random geometric, and growing graphs; it is not safe to cite this synthesis as retained current evidence for graph axioms or staggered physics.
- **open / conditional deps cited:**
  - `STAGGERED_FERMION_CARD_2026-04-10.md`
- **auditor confidence:** high

### `shapiro_complex_interaction_note`

- **Note:** [`SHAPIRO_COMPLEX_INTERACTION_NOTE.md`](../../docs/SHAPIRO_COMPLEX_INTERACTION_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_failed~~
- **effective_status:** ~~audited_failed~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The complex-action factor is a real attenuation term, so it does not rotate the phase phasor, and the retained causal phase lag survives the complex-action crossover.  _(class `A`)_
- **chain closes:** False — The phasor statement is algebraic given a supplied real attenuation factor, but the runner hard-codes the phase and complex-action rows and the causal phase-lag dependencies are failed, renaming, unknown, or unaudited.
- **rationale:** Issue: The script is a static renderer with hard-coded phase rows, complex-action rows, and summary booleans; it does not derive the Shapiro phase lag, the complex-action crossover, or their interaction from audit-clean inputs. Why this blocks: the retained bridge claim depends on causal/diamond/selector notes that are failed, renaming, unknown, or unaudited, so the fact that a real scalar attenuation would preserve a supplied phase angle cannot promote the phase lag to a retained broad causal observable. Repair target: audit or repair the Shapiro/causal phase-lag chain and the complex-action selector chain, then add a runner that constructs the phase observable and applies the complex-action operator rather than rendering stored numbers. Claim boundary until fixed: it is safe to say that if the listed phase rows are supplied and the complex-action factor is strictly real positive, the phase angle is algebraically unchanged; it is not safe to claim retained survival of a causal phase-lag observable through the current complex-action architecture.
- **open / conditional deps cited:**
  - `SHAPIRO_DIAMOND_BRIDGE_NOTE.md`
  - `CAUSAL_PROPAGATING_FIELD_NOTE.md`
  - `CAUSAL_FIELD_RECONCILIATION_NOTE.md`
  - `CAUSAL_MOVING_UNIFICATION_NOTE.md`
  - `COMPLEX_SELECTIVITY_PREDICTOR_NOTE.md`
  - `DIAMOND_PHASE_RAMP_BRIDGE_CARD_NOTE.md`
- **auditor confidence:** high

### `shapiro_delay_note`

- **Note:** [`SHAPIRO_DELAY_NOTE.md`](../../docs/SHAPIRO_DELAY_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_conditional~~
- **effective_status:** ~~audited_conditional~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The retained c-dependent phase lag is a portable, seed-stable discrete Shapiro-delay observable with an exact zero control and family spread below 2e-4 rad.  _(class `B`)_
- **chain closes:** False — The runner is a canonical replay of hard-coded phase rows, not a derivation from the causal-field machinery; the Shapiro-delay and NV/phase-ramp bridge remains explicitly proxy-level in the one-hop notes.
- **rationale:** Issue: the source note treats the hard-coded c-dependent phase-lag table as a retained portable Shapiro-delay observable. Why this blocks: the live runner only replays fixed rows and does not recompute phase lag from the causal cone, grown-family seeds, complex-action crossover, or diamond phase-ramp bridge; the one-hop notes also state that the cone is imposed and that the NV/phase-ramp interpretation is proxy-level with missing absolute calibration. Repair target: register the artifact-chain notes as explicit dependencies and add a runner that derives the phase rows from the causal-field setup across seeds/families, proves the zero control, and supplies a theorem mapping the proxy phase lag to the claimed Shapiro-delay observable. Claim boundary until fixed: it is safe to claim that the current replay table contains an exact inst-null row and the listed c-dependent proxy phase-lag rows with <=2e-4 rad family spread; it is not yet an audited retained derivation of a physical Shapiro-delay observable or calibrated NV readout.
- **open / conditional deps cited:**
  - `SHAPIRO_COMPLEX_INTERACTION_NOTE.md_not_registered_one_hop_dependency`
  - `SHAPIRO_DIAMOND_BRIDGE_NOTE.md_proxy_level_bridge`
  - `DIAMOND_PHASE_RAMP_BRIDGE_CARD_NOTE.md_proxy_level_no_absolute_NV_claim`
  - `CAUSAL_PROPAGATING_FIELD_NOTE.md_imposed_cone_not_self_consistent_field`
  - `CAUSAL_FIELD_RECONCILIATION_NOTE.md_fixed_anchor_portability_boundary`
  - `scripts/shapiro_phase_lag_probe.py_hard_coded_replay_not_derivation`
- **auditor confidence:** high

### `shapiro_diamond_bridge_note`

- **Note:** [`SHAPIRO_DIAMOND_BRIDGE_NOTE.md`](../../docs/SHAPIRO_DIAMOND_BRIDGE_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_failed~~
- **effective_status:** ~~audited_failed~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The Shapiro-style phase lag should be read as the same class of proxy phasor observable in X/Y/phi and phase-ramp language as the diamond/NV bridge card.  _(class `F`)_
- **chain closes:** False — The note translates a supplied causal phase-lag table into proxy phasor language, but the causal-field dependencies are audited failed and the diamond bridge/unit dependencies are unknown and unaudited.
- **rationale:** Issue: The bridge claim identifies the Shapiro phase lag with diamond/NV proxy phasor language without a runner or audit-clean causal and diamond-unit inputs. Why this blocks: failed causal-field dependencies cannot support a proposed-retained c-dependent phase lag, and unknown diamond bridge/unit notes cannot justify even proxy-level lab-facing translation beyond notation. Repair target: repair and audit the causal phase-lag derivation, audit the diamond phase-ramp and absolute-unit bridge notes, and add a runner constructing X, Y, phi, and phase-ramp quantities from the same data pipeline. Claim boundary until fixed: it is safe to say this note proposes X/Y/phi language as a handoff vocabulary for a supplied phase-lag table; it is not safe to claim a retained Shapiro-to-diamond bridge or lab-facing causal discriminator.
- **open / conditional deps cited:**
  - `DIAMOND_PHASE_RAMP_BRIDGE_CARD_NOTE.md`
  - `DIAMOND_ABSOLUTE_UNIT_BRIDGE_NOTE.md`
  - `CAUSAL_PROPAGATING_FIELD_NOTE.md`
  - `CAUSAL_FIELD_RECONCILIATION_NOTE.md`
- **auditor confidence:** high

### `shapiro_diamond_frequency_bridge_note`

- **Note:** [`SHAPIRO_DIAMOND_FREQUENCY_BRIDGE_NOTE.md`](../../docs/SHAPIRO_DIAMOND_FREQUENCY_BRIDGE_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_failed~~
- **effective_status:** ~~audited_failed~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The retained Shapiro delay is frequency-sensitive in the same X/Y/phi and phase-ramp language as the diamond bridge card, so phi and phase-ramp slope should scale with k.  _(class `F`)_
- **chain closes:** False — The note translates a supplied k-scaling claim into diamond proxy language, but the Shapiro delay is only conditional, the Shapiro-diamond bridge is failed, and the diamond phase/unit/protocol inputs are unknown, conditional, or bounded.
- **rationale:** Issue: The frequency bridge depends on a conditional Shapiro-delay result, a failed Shapiro-diamond bridge, and unaudited/conditional diamond phase-ramp and signal-budget notes, with no runner constructing phi, k-scaling, or normalized phase-ramp quantities. Why this blocks: translating an unratified proxy scaling into lab-facing X/Y/phi language does not establish a retained frequency-sensitive diamond/NV prediction or a calibrated comparison surface. Repair target: audit or repair SHAPIRO_DELAY_NOTE and SHAPIRO_DIAMOND_BRIDGE_NOTE, audit the diamond phase-ramp and signal-budget notes, and add a runner that varies k at fixed geometry and verifies phi/k and slope/k collapse from generated data. Claim boundary until fixed: it is safe to say this note proposes a proxy-level frequency-bridge test to run; it is not safe to claim retained k-linear diamond/NV phase-ramp behavior.
- **open / conditional deps cited:**
  - `SHAPIRO_DELAY_NOTE.md`
  - `SHAPIRO_DIAMOND_BRIDGE_NOTE.md`
  - `DIAMOND_PHASE_RAMP_BRIDGE_CARD_NOTE.md`
  - `DIAMOND_NV_PHASE_RAMP_SIGNAL_BUDGET_NOTE.md`
  - `DIAMOND_SENSOR_PROTOCOL_NOTE.md`
  - `DIAMOND_SENSOR_PREDICTION_NOTE.md`
- **auditor confidence:** high

### `shapiro_family_portability_note`

- **Note:** [`SHAPIRO_FAMILY_PORTABILITY_NOTE.md`](../../docs/SHAPIRO_FAMILY_PORTABILITY_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_conditional~~
- **effective_status:** ~~audited_conditional~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The c-dependent phase lag reproduces cleanly across the three portable grown families with seed-stable values and exact zero controls.  _(class `C`)_
- **chain closes:** False — The runner recomputes the three-family proxy phase table, but the underlying Shapiro-delay result is only audited conditional and the linked complex/diamond bridge dependencies are failed or unknown.
- **rationale:** Issue: The script verifies portability of the proxy phase-lag table across the three chosen grown-family parameters, but the base Shapiro-delay claim is audited conditional and the associated complex/diamond bridge notes are failed or unknown. Why this blocks: family-to-family stability of a proxy computed inside the same model does not by itself ratify the causal phase-lag observable as retained physics or a lab-facing bridge. Repair target: repair/audit SHAPIRO_DELAY_NOTE as the base phase-lag theorem, remove non-load-bearing failed bridge dependencies or repair them, and add explicit assertion thresholds for family spread and zero controls. Claim boundary until fixed: it is safe to claim that the current runner reproduces a seed-stable, three-family proxy phase table with exact zero controls; it is not safe to claim a retained causal phase-lag observable or diamond/NV portability from this row alone.
- **open / conditional deps cited:**
  - `SHAPIRO_DELAY_NOTE.md`
  - `SHAPIRO_COMPLEX_INTERACTION_NOTE.md`
  - `DIAMOND_PHASE_RAMP_BRIDGE_CARD_NOTE.md`
- **auditor confidence:** high

### `shapiro_five_family_portability_note`

- **Note:** [`SHAPIRO_FIVE_FAMILY_PORTABILITY_NOTE.md`](../../docs/SHAPIRO_FIVE_FAMILY_PORTABILITY_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_failed~~
- **effective_status:** ~~audited_failed~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** Exact zero-source control stays exact on all five families and the c-dependent phase lag extends onto the additional retained quadrant and radial families.  _(class `C`)_
- **chain closes:** False — The frozen log is missing and the current runner contradicts the note's zero-control gate, printing zero lags around 0.065-0.071 rad while labeling them exact.
- **rationale:** Issue: The note claims exact zero-source control on all five families, but the current runner reports zero lags of about 0.065-0.071 rad for every family, and the cited frozen log is absent. Why this blocks: the zero control is the stated first gate for portability; if it fails or is miscomputed, the few-milliradian cross-family spread table cannot be interpreted as a retained causal phase-lag extension, especially with the three-family core only conditional and the fifth-family radial dependency already failed. Repair target: fix the zero-control computation and labeling, restore a frozen log, add PASS/FAIL assertions for zero controls and family spread, and re-audit the sign/fourth/fifth-family dependencies before reasserting five-family portability. Claim boundary until fixed: it is safe to say the current script prints similar c-dependent phase rows for five sampled families; it is not safe to claim exact controls or retained five-family Shapiro portability.
- **open / conditional deps cited:**
  - `SHAPIRO_FAMILY_PORTABILITY_NOTE.md`
  - `SIGN_PORTABILITY_INVARIANT_NOTE.md`
  - `FOURTH_FAMILY_QUADRANT_NOTE.md`
  - `FIFTH_FAMILY_RADIAL_NOTE.md`
- **auditor confidence:** high

### `shapiro_scaling_direct_replay_note`

- **Note:** [`SHAPIRO_SCALING_DIRECT_REPLAY_NOTE.md`](../../docs/SHAPIRO_SCALING_DIRECT_REPLAY_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_failed~~
- **effective_status:** ~~audited_failed~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The Shapiro scaling lane can close as a direct data-bearing replay: the retained s, b, and k laws are frozen from repo data, and exact zero controls remain explicit.  _(class `B`)_
- **chain closes:** False — The replay script renders embedded rows rather than recomputing the scaling laws, while the experimental card source is unaudited/unknown and the frequency bridge dependency is audited failed.
- **rationale:** Issue: The direct replay script is a static data renderer whose s, b, and k laws are imported from SHAPIRO_EXPERIMENTAL_CARD.md, which is unaudited/unknown, and it also cites the failed Shapiro diamond frequency bridge. Why this blocks: freezing unaudited table entries is not a retained replay unless the source card is audit-clean or the runner recomputes the laws from raw inputs with zero-control checks. Repair target: audit SHAPIRO_EXPERIMENTAL_CARD.md or replace this with a runner that directly recomputes the s, b, and k scaling sweeps and asserts the source-off and instantaneous-field controls. Claim boundary until fixed: it is safe to say the script renders the stored scaling and portable-delay tables; it is not safe to claim retained Shapiro scaling-law closure from this row.
- **open / conditional deps cited:**
  - `SHAPIRO_EXPERIMENTAL_CARD.md`
  - `SHAPIRO_DIAMOND_FREQUENCY_BRIDGE_NOTE.md`
- **auditor confidence:** high

### `shapiro_static_discriminator_note`

- **Note:** [`SHAPIRO_STATIC_DISCRIMINATOR_NOTE.md`](../../docs/SHAPIRO_STATIC_DISCRIMINATOR_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_clean~~
- **effective_status:** **retained**  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** Static cone shape can mimic the c-dependent causal phase curve exactly, while static scheduling remains near-flat and does not reproduce the curve.  _(class `C`)_
- **chain closes:** True — The current runner computes the causal, static-cone, and static-schedule curves across three families and shows zero RMSE for the static-cone mimic and nonzero scheduling mismatch.
- **rationale:** The audited claim is the negative boundary: detector-line phase lag is not a unique causal-propagation discriminator because a static cone-shape field reproduces the same c-dependent curve in this model. The runner reproduces the note's table and the safe read, including exact zero controls and the static-scheduling mismatch. Residual risk is limited to the missing frozen log; the current executable artifact is sufficient for the scoped boundary result.
- **auditor confidence:** high

### `sign_portability_invariant_note`

- **Note:** [`SIGN_PORTABILITY_INVARIANT_NOTE.md`](../../docs/SIGN_PORTABILITY_INVARIANT_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_conditional~~
- **effective_status:** ~~audited_conditional~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The note infers a portable signed-control fixed point across retained sign-law basins from exact zero-source/neutral cancellation, plus-minus antisymmetry, and weak-field exponents near 1.0 in multiple family notes and a comparison runner.  _(class `B`)_
- **chain closes:** False — The synthesis depends on multiple family notes, a comparison script/log, and a holdout package, but the ledger lists no one-hop dependencies and no registered primary runner/output for this claim.
- **rationale:** Issue: the proposed_retained portability invariant is a cross-family comparison, but the audit packet provides no registered one-hop family notes and no primary runner/output for SIGN_PORTABILITY_INVARIANT_COMPARE.py. Why this blocks: a hostile auditor cannot verify that the named families are themselves retained, that their exact controls and weak-field exponents use compatible protocols, or that the claimed signed-control fixed point is independent of basin width/seed selectivity rather than a summary label imposed after filtering passing rows. Repair target: register the comparison runner/log, add the family and holdout notes as one-hop dependencies with their current audit statuses, and make the runner assert common thresholds for zero-source cancellation, neutral same-point cancellation, antisymmetry, unit-slope tolerance, and basin/seed exclusions. Claim boundary until fixed: it is safe to say the source note proposes a conditional comparison invariant across reported sign-law families; it is not yet an audited retained portability theorem or independent order parameter.
- **open / conditional deps cited:**
  - `scripts/SIGN_PORTABILITY_INVARIANT_COMPARE.py_not_registered_primary_runner`
  - `logs/2026-04-06-sign-portability-invariant.txt_not_registered_primary_output`
  - `retained_sign_family_notes_not_registered_one_hop`
  - `fifth_family_holdout_notes_not_registered_one_hop`
  - `common_threshold_protocol_not_registered`
- **auditor confidence:** high

### `sixth_family_distance_law_third_vs_sixth_quick_note`

- **Note:** [`SIXTH_FAMILY_DISTANCE_LAW_THIRD_VS_SIXTH_QUICK_NOTE.md`](../../docs/SIXTH_FAMILY_DISTANCE_LAW_THIRD_VS_SIXTH_QUICK_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_conditional~~
- **effective_status:** ~~audited_conditional~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The sixth-family row preserves the near-Newtonian tail on the sampled retained row, while the third-family interior row misses the tail and remains consistent with the breakpoint classifier.  _(class `C`)_
- **chain closes:** False — The runner reproduces the two-row contrast, but the sixth-family sheared-basin provenance is unaudited/unknown and the breakpoint classifier dependency is only audited conditional.
- **rationale:** Issue: The script verifies the targeted row comparison, but the claim labels both rows as retained family rows while the sixth sheared-basin provenance remains unaudited/unknown and the distance-law breakpoint classifier is conditional. Why this blocks: a reproducible spot check can establish this script's row-level outcome, but it cannot promote sixth-family tail survival as retained until the family and classifier inputs are audit-clean. Repair target: audit the sixth-family sheared family notes and the distance-law breakpoint classifier, then add assertion thresholds for alpha, R^2, and toward counts in this quick runner. Claim boundary until fixed: it is safe to claim that this runner finds alpha=-1.077, R^2=0.911, 5/5 toward for the sampled sixth row and alpha=-2.158 for the sampled third row; it is not safe to claim retained sixth-family distance-law survival beyond this conditional spot check.
- **open / conditional deps cited:**
  - `SIXTH_FAMILY_SHEARED_NOTE.md`
  - `SIXTH_FAMILY_SHEARED_BOUNDARY_NOTE.md`
  - `DISTANCE_LAW_BREAKPOINT_NOTE.md`
- **auditor confidence:** high

### `source_resolved_generated_support_recovery_basin_note`

- **Note:** [`SOURCE_RESOLVED_GENERATED_SUPPORT_RECOVERY_BASIN_NOTE.md`](../../docs/SOURCE_RESOLVED_GENERATED_SUPPORT_RECOVERY_BASIN_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_conditional~~
- **effective_status:** ~~audited_conditional~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The tiny k_nearest/min_edges grid around the generated-family kNN-floor tweak remains positive in mean centroid shift and keeps detector support fraction above the generated-family baseline, so the support recovery is not a one-point fluke.  _(class `C`)_
- **chain closes:** False — The current runner reproduces the basin table, but the upstream generated-family support recovery is bounded/unaudited and several grid points are not seed-unanimous despite the stronger retained-basin framing.
- **rationale:** Issue: The executable basin probe verifies a tiny grid of kNN-floor tweaks, but the parent generated-family support recovery is only bounded/unaudited and the source's 'every point remains TOWARD' wording is mean-positive per grid row, not all-seed TOWARD for every row. Why this blocks: a nine-point neighborhood with 2/4 or 3/4 seed sign counts at several points cannot promote retained generated-family recovery unless the parent recovery and the basin acceptance criterion are independently closed. Repair target: audit the generated-family recovery and generated-family probe notes, then add assertion thresholds specifying whether basin stability means positive mean delta, minimum seed count, support fraction above baseline, or all of these. Claim boundary until fixed: it is safe to claim that the current runner finds all nine grid rows have positive mean centroid shift, support_frac 0.427-0.458 above baseline 0.311, and zero-source shift 0; it is not safe to claim retained generated-family recovery beyond this conditional basin probe.
- **open / conditional deps cited:**
  - `SOURCE_RESOLVED_GENERATED_SUPPORT_RECOVERY_NOTE.md`
  - `SOURCE_RESOLVED_GENERATED_FAMILY_PROBE_NOTE.md`
  - `SOURCE_RESOLVED_GENERATED_SUPPORT_MASS_SCALING_NOTE.md`
- **auditor confidence:** high

### `source_resolved_propagating_green_pocket_note`

- **Note:** [`SOURCE_RESOLVED_PROPAGATING_GREEN_POCKET_NOTE.md`](../../docs/SOURCE_RESOLVED_PROPAGATING_GREEN_POCKET_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_conditional~~
- **effective_status:** ~~audited_conditional~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The exact-lattice same-site-memory Green recurrence with mix=0.9 preserves zero-source reduction, 4/4 TOWARD sign, near-linear source scaling, and nonzero offsets versus instantaneous and static Green controls on the tested source ladder.  _(class `C`)_
- **chain closes:** False — The runner reproduces the frozen exact-lattice table, but the retained interpretation depends on a selected same-site memory recurrence, fixed mix/calibration, and bounded/unaudited exact-lattice control probes rather than a closed field-evolution theorem.
- **rationale:** Issue: The executable artifact verifies the stated same-site-memory pocket, but the load-bearing memory rule, mix=0.9 choice, calibration to target max |f|=0.02, and static Green control are selected inputs from bounded/unaudited field-probe scaffolding rather than retained derived physics. Why this blocks: the note may retain the deterministic row-level computation, but it cannot promote a proposed_retained propagating Green field result from an arbitrary same-site recurrence and calibration without an independent theorem fixing the carrier, update rule, and normalization. Repair target: derive the same-site memory recurrence and mix/normalization from retained lattice field dynamics, audit the exact Green/source-driven control notes, and add assertion gates for zero-source reduction, sign count, mass exponent, and ratio bands. Claim boundary until fixed: it is safe to claim that this script, with the stated exact lattice, source cluster, gain, and mix, gives zero-source shift 0, 4/4 TOWARD rows, propagating F~M exponent 1.00, mean |prop/inst| 1.420, and mean |prop/green| 1.149; it is not safe to claim a retained propagating-field mechanism beyond this conditional pocket.
- **open / conditional deps cited:**
  - `MINIMAL_SOURCE_DRIVEN_FIELD_PROBE_NOTE.md`
  - `SOURCE_RESOLVED_EXACT_GREEN_POCKET_NOTE.md`
- **auditor confidence:** high

### `source_resolved_retarded_green_pocket_note`

- **Note:** [`SOURCE_RESOLVED_RETARDED_GREEN_POCKET_NOTE.md`](../../docs/SOURCE_RESOLVED_RETARDED_GREEN_POCKET_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_failed~~
- **effective_status:** ~~audited_failed~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The finite-lag retarded-like update is claimed to be a small positive correction relative to the same-site-memory control, with the frozen table reporting a ret/same ratio near 1.20 plus positive ret-minus-same and small spread changes.  _(class `C`)_
- **chain closes:** False — The current runner reproduces the note, but the column labeled ret/same is actually computed as ret/instantaneous; the true ret/same ratio is about 1.026, and the support-fraction delta is exactly 0.000e+00.
- **rationale:** Issue: The load-bearing same-site comparison is misidentified: scripts/source_resolved_retarded_green_pocket.py prints a column labeled ret/same but fills it with ret_delta / inst_delta, and the source note freezes those same mislabeled values around 1.20. The true retarded/same-site ratio from the printed rows is about 1.026, while mean ret support - same support is 0.000e+00. Why this blocks: a claim whose main observable is improvement relative to same-site memory cannot be retained when the headline ratio is against the instantaneous comparator and the stated support broadening is only an N_eff nudge, not support-fraction broadening. Repair target: correct the runner and note to compute and label ret/same, ret/inst, ret-same, support_frac delta, and N_eff delta separately, then add assertion thresholds for which of those observables constitutes a finite-lag positive. Claim boundary until fixed: it is safe to claim that the current rows have zero-source shifts 0, 4/4 TOWARD, linear fitted exponents, positive ret-same differences of 6.32e-05 to 5.09e-04, true ret/same about 1.026, unchanged support fraction, and mean N_eff increase +4.493e-02; it is not safe to claim the frozen ret/same ~1.20 same-site improvement or a retained retarded-pocket result.
- **open / conditional deps cited:**
  - `SOURCE_RESOLVED_PROPAGATING_GREEN_POCKET_NOTE.md`
  - `SOURCE_RESOLVED_EXACT_GREEN_POCKET_NOTE.md`
  - `MINIMAL_SOURCE_DRIVEN_FIELD_PROBE_NOTE.md`
- **auditor confidence:** high

### `source_resolved_transverse_propagating_green_note`

- **Note:** [`SOURCE_RESOLVED_TRANSVERSE_PROPAGATING_GREEN_NOTE.md`](../../docs/SOURCE_RESOLVED_TRANSVERSE_PROPAGATING_GREEN_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_failed~~
- **effective_status:** ~~audited_failed~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The transverse-smoothed exact-lattice field is claimed to give a positive, detectable centroid nudge relative to same-site memory while preserving zero-source reduction, 4/4 TOWARD sign, and linear scaling.  _(class `C`)_
- **chain closes:** False — The current runner contradicts the frozen table: transverse-minus-same is negative in every row, the frozen numerical values are stale, and the column labeled trans/same is actually transverse/instantaneous.
- **rationale:** Issue: The note's load-bearing positive transverse correction is stale relative to scripts/source_resolved_transverse_propagating_green.py. Current output gives transverse - same = -2.30e-05, -4.60e-05, -9.23e-05, -1.86e-04, not the positive values frozen in the note; support-fraction delta is 0.000e+00; and the printed trans/same column is actually trans_delta / inst_delta, with true trans/same about 0.990. Why this blocks: the proposed_retained claim depends on transverse transport being a detectable positive correction relative to same-site memory, but the current executable artifact shows a small negative centroid correction and no support-fraction broadening. Repair target: update or fix the runner/note pair, compute true trans/same and trans/inst separately, add assertion gates for the intended centroid/support observable, and rerun from the exact artifact that produced the frozen rows if they are meant to be retained. Claim boundary until fixed: it is safe to claim only that the current runner preserves zero-source reduction, 4/4 TOWARD sign, and F~M exponent 1.00 while producing a small negative transverse-minus-same centroid shift and unchanged support fraction; it is not safe to claim a retained positive transverse-transport pocket.
- **open / conditional deps cited:**
  - `SOURCE_RESOLVED_PROPAGATING_GREEN_POCKET_NOTE.md`
  - `SOURCE_RESOLVED_EXACT_GREEN_POCKET_NOTE.md`
  - `MINIMAL_SOURCE_DRIVEN_FIELD_PROBE_NOTE.md`
- **auditor confidence:** high

### `source_resolved_wavefield_escalation_note`

- **Note:** [`SOURCE_RESOLVED_WAVEFIELD_ESCALATION_NOTE.md`](../../docs/SOURCE_RESOLVED_WAVEFIELD_ESCALATION_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_conditional~~
- **effective_status:** ~~audited_conditional~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The larger exact-lattice wavefield runner preserves zero-source reduction, 4/4 TOWARD sign, near-linear F~M scaling, and a coherent detector-line phase ramp with R^2 near 0.96 and multi-radian span.  _(class `C`)_
- **chain closes:** False — The current runner reproduces the phase-ramp table, but the finite-speed wavefield rule and parameters are selected rather than derived, its compact-pocket parent is unaudited, and the table's wave/same column is actually wave/instantaneous.
- **rationale:** Issue: The executable artifact supports a runner-specific wavefield escalation, but the proposed_retained claim rests on a hand-selected local update rule and parameter set rather than an audited field-dynamics theorem; additionally, the frozen column labeled wave/same is computed as wave_delta / inst_delta, with true wave/same about 45-49 instead of 56-61. Why this blocks: a coherent phase ramp in one calibrated exact-lattice update is not enough to retain a physical wavefield mechanism unless the update rule, normalization, and comparator are fixed by retained inputs and the same-site ratio is reported correctly. Repair target: audit the compact wavefield parent, derive or independently justify WAVE_LAG_BLEND, WAVE_SPEED2, WAVE_DAMP, WAVE_SOURCE_BLEND, and FIELD_TARGET_MAX, and correct the runner/note to report wave/inst and wave/same separately with assertion gates for ramp slope, R^2, span, overlap, sign, and exponent. Claim boundary until fixed: it is safe to claim that the current runner gives zero-source shifts 0, 4/4 TOWARD rows, wavefield F~M exponent 0.98, mean ramp R^2 0.961, mean ramp span 3.330 rad, and wave/same ratios still large at about 45-49; it is not safe to claim a retained wavefield mechanism beyond this conditional exact-lattice escalation.
- **open / conditional deps cited:**
  - `SOURCE_RESOLVED_WAVEFIELD_GREEN_POCKET_NOTE.md`
  - `SOURCE_RESOLVED_PROPAGATING_GREEN_POCKET_NOTE.md`
  - `SOURCE_RESOLVED_EXACT_GREEN_POCKET_NOTE.md`
  - `MINIMAL_SOURCE_DRIVEN_FIELD_PROBE_NOTE.md`
- **auditor confidence:** high

### `source_resolved_wavefield_green_pocket_note`

- **Note:** [`SOURCE_RESOLVED_WAVEFIELD_GREEN_POCKET_NOTE.md`](../../docs/SOURCE_RESOLVED_WAVEFIELD_GREEN_POCKET_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_conditional~~
- **effective_status:** ~~audited_conditional~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The compact exact-lattice wavefield runner preserves zero-source reduction, 4/4 TOWARD sign, near-linear scaling, and a measurable detector phase/overlap difference relative to same-site memory.  _(class `C`)_
- **chain closes:** False — The current runner reproduces the main table, but the finite-speed wavefield update and parameter set are selected rather than derived, and the wave/same column is actually wave/instantaneous.
- **rationale:** Issue: The executable supports a specific compact exact-lattice wavefield pocket, but the proposed_retained physical reading depends on hand-selected wavefield parameters and calibrated normalization; the table also labels wave_delta / inst_delta as wave/same, while true wave/same from the printed rows is about 33-34. Why this blocks: a retained finite-speed wavefield mechanism requires an audited derivation of the local update rule, carrier, parameter choices, and normalization, not just one calibrated runner pocket with a mislabeled comparator column. Repair target: derive or independently justify WAVE_LAG_BLEND, WAVE_SPEED2, WAVE_DAMP, WAVE_SOURCE_BLEND, and FIELD_TARGET_MAX from retained field dynamics, fix the runner/note to report wave/inst and wave/same separately, and add assertion gates for zero-source reduction, sign, exponent, phase lag, overlap, and comparator ratios. Claim boundary until fixed: it is safe to claim that the current runner gives zero-source shifts 0, 4/4 TOWARD rows, wavefield F~M exponent 0.99, mean phase lag -0.249 rad, mean overlap 0.827, and true wave/same ratios about 33-34; it is not safe to claim a retained finite-speed wavefield mechanism beyond this conditional exact-lattice pocket.
- **open / conditional deps cited:**
  - `SOURCE_RESOLVED_PROPAGATING_GREEN_POCKET_NOTE.md`
  - `SOURCE_RESOLVED_EXACT_GREEN_POCKET_NOTE.md`
  - `MINIMAL_SOURCE_DRIVEN_FIELD_PROBE_NOTE.md`
- **auditor confidence:** high

### `source_resolved_wavefield_mechanism_note`

- **Note:** [`SOURCE_RESOLVED_WAVEFIELD_MECHANISM_NOTE.md`](../../docs/SOURCE_RESOLVED_WAVEFIELD_MECHANISM_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_conditional~~
- **effective_status:** ~~audited_conditional~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The larger exact-lattice source-depth scan shows coherent phase-ramp slopes whose magnitude increases monotonically as source depth decreases, while zero-source reduction and near-linear weak-field scaling persist.  _(class `C`)_
- **chain closes:** False — The current runner reproduces the source-depth table, but the mechanism claim depends on the exact-lattice wavefield lane and its selected update parameters, whose parent cards are only audited conditional.
- **rationale:** Issue: The source-depth scan is reproducible, but it imports the wavefield escalation machinery as a retained wavefield lane even though the compact and larger wavefield parent cards remain conditional and the finite-speed update rule/normalization are not derived from retained field dynamics. Why this blocks: monotone depth dependence of a runner-specific phase-ramp coefficient is evidence for a conditional mechanism probe, not a retained causal-field mechanism, until the wavefield carrier, parameters, and parent observable are audit-clean. Repair target: first close or demote the wavefield green pocket and escalation notes; then add assertion gates for monotone ramp slope versus depth, ramp R^2, depth exponents, zero-source reduction, TOWARD sign, and F~M exponents, all using correctly separated wave/same and wave/instantaneous comparators. Claim boundary until fixed: it is safe to claim that this runner finds zero-source shifts 0, source-layer mean ramp slopes -0.2422, -0.2718, -0.2989, -0.3226 with R^2 about 0.965-0.969, wave/same ratios 36.092-44.431, and depth exponents -2.77 and -2.65; it is not safe to claim a retained exact-lattice wavefield mechanism beyond this conditional depth probe.
- **open / conditional deps cited:**
  - `SOURCE_RESOLVED_WAVEFIELD_ESCALATION_NOTE.md`
  - `SOURCE_RESOLVED_WAVEFIELD_GREEN_POCKET_NOTE.md`
  - `SOURCE_RESOLVED_PROPAGATING_GREEN_POCKET_NOTE.md`
  - `MINIMAL_SOURCE_DRIVEN_FIELD_PROBE_NOTE.md`
- **auditor confidence:** high

### `source_resolved_wavefield_v2_note`

- **Note:** [`SOURCE_RESOLVED_WAVEFIELD_V2_NOTE.md`](../../docs/SOURCE_RESOLVED_WAVEFIELD_V2_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_conditional~~
- **effective_status:** ~~audited_conditional~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The larger exact-lattice v2 runner shows that the detector-line phase-ramp slope and span scale close to linearly with source strength while zero-source reduction, TOWARD sign, and near-linear centroid scaling persist.  _(class `C`)_
- **chain closes:** False — The current runner reproduces the phase-ramp law table, but the law is conditional on the selected wavefield update inherited from the conditional escalation lane, and the row table labels wave/instantaneous ratios as wave/same.
- **rationale:** Issue: The source-strength phase-ramp fit is reproducible, but it is built on the same underived finite-speed wavefield update and calibrated normalization as the conditional wavefield parent; additionally, the table's wave/same column is wave_delta / inst_delta, while the true mean wave/same ratio appears only in the summary as 47.680. Why this blocks: a retained exact-lattice phase-ramp law requires the wavefield carrier/update/normalization and comparator definitions to be audit-clean; otherwise the fitted slope/span exponents are a conditional property of one selected runner architecture. Repair target: close the wavefield green pocket and escalation notes, correct the table to report wave/inst and wave/same separately, and add hard assertions for zero-source reduction, 5/5 TOWARD, centroid exponents, phase-ramp slope/span exponents, R^2, and comparator ratios. Claim boundary until fixed: it is safe to claim that the current runner gives zero-source shifts 0, 5/5 TOWARD, wavefield F~M exponent 0.99, phase-ramp slope exponent 1.02, span exponent 1.01, mean R^2 0.961, and true mean wave/same 47.680; it is not safe to claim a retained phase-ramp law beyond this conditional exact-lattice wavefield v2 probe.
- **open / conditional deps cited:**
  - `SOURCE_RESOLVED_WAVEFIELD_ESCALATION_NOTE.md`
  - `SOURCE_RESOLVED_WAVEFIELD_GREEN_POCKET_NOTE.md`
  - `SOURCE_RESOLVED_PROPAGATING_GREEN_POCKET_NOTE.md`
  - `MINIMAL_SOURCE_DRIVEN_FIELD_PROBE_NOTE.md`
- **auditor confidence:** high

### `staggered_backreaction_capture_closure_note`

- **Note:** [`STAGGERED_BACKREACTION_CAPTURE_CLOSURE_NOTE.md`](../../docs/STAGGERED_BACKREACTION_CAPTURE_CLOSURE_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_failed~~
- **effective_status:** ~~audited_failed~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The capture-closure rule is claimed to preserve the retained cycle battery while moving the endogenous closed force much closer to the external-kernel force scale, with cycle mean gap improvement 4.03x and a layered holdout improvement 5.15x.  _(class `C`)_
- **chain closes:** False — The current runner materially disagrees with the frozen result: cycle mean gap improves only 2.08x, random_geometric closed gap is 41.5% rather than 6.88%, growing closed gap is 53.2% rather than 41.78%, and the holdout improvement is 2.02x rather than 5.15x.
- **rationale:** Issue: The source note's load-bearing force/gap/gain table is stale relative to scripts/frontier_staggered_backreaction_capture_closure_harness.py. Current output gives random_geometric F_closed=+6.443e-01, F_ext=+1.101e+00, closed gap 41.5%, gain 15.221; growing F_closed=+3.304e-01, F_ext=+7.062e-01, closed gap 53.2%, gain 27.734; cycle mean gap 9.828e-01 -> 4.734e-01 (2.08x); holdout gap 9.191e-01 -> 4.559e-01 (2.02x). Why this blocks: the proposed_retained closure depends on the claimed near-capture of the external-kernel force scale, but the live runner shows a much weaker and numerically different closure than the note freezes. Repair target: determine whether the note or runner drifted, rerun the intended artifact, update the frozen table, and add assertion gates for closed gap, improvement factor, gains, R^2, score, and holdout gap before any retained closure claim. Claim boundary until fixed: it is safe to claim that the current runner preserves the two 9/9 cycle-battery scores, zero-source controls, additivity, TOWARD sign, and high linearity while improving force-scale gaps by about 2x; it is not safe to claim the frozen 4.03x/5.15x closure or a retained near-capture of the external-kernel scale.
- **open / conditional deps cited:**
  - `STAGGERED_BACKREACTION_ITERATIVE_NOTE.md`
  - `STAGGERED_LAYERED_BACKREACTION_NOTE.md`
  - `STAGGERED_GRAPH_GAUGE_CLOSURE_NOTE.md`
  - `STAGGERED_BACKREACTION_SCALE_CLOSURE_NOTE.md`
- **auditor confidence:** high

### `staggered_backreaction_green_closure_note`

- **Note:** [`STAGGERED_BACKREACTION_GREEN_CLOSURE_NOTE.md`](../../docs/STAGGERED_BACKREACTION_GREEN_CLOSURE_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_failed~~
- **effective_status:** ~~audited_failed~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The note promotes resistance_yukawa as a graph-native Green map that closes the cycle-bearing force-scale gap by nearly an order of magnitude and transfers cleanly to the layered holdout without blow-up.  _(class `C`)_
- **chain closes:** False — The current runner does not reproduce the source note's load-bearing numbers: resistance_yukawa now reports gain 1.517, raw cycle gap 3.425e-01, calibrated cycle gap 1.059e-01, raw holdout gap 1.534e-02, and calibrated holdout gap 5.371e-01, not the note's 0.980, 9.889e-02, 9.688e-02, 1.680e-02, and 3.714e-03.
- **rationale:** Issue: the archived source note is stale relative to the live Green-closure runner, and the stale fields are exactly the claimed force-scale closure and holdout-transfer numbers. Why this blocks: a hostile physicist can no longer claim nearly order-of-magnitude cycle closure or clean calibrated holdout transfer, because the current runner gives only a 2.81x raw cycle improvement over screened_poisson and the calibrated layered holdout gap blows up to 5.371e-01 rather than 3.714e-03. Repair target: either restore the old runner/environment that generated the note's table, or update the note to the current runner output and rerun the comparison with hard assertions for the intended acceptance gates, including raw/calibrated cycle gaps, raw/calibrated holdout gaps, gain, retained checks, and self-gap. Claim boundary until fixed: it is safe to claim only that the current resistance_yukawa runner is the best of the three frozen maps by its balance score, preserves source-linearity/additivity/TOWARD/norm checks, improves the raw cycle gap from 9.618e-01 to 3.425e-01, and has a small raw holdout gap of 1.534e-02; it is not safe to retain the note's stronger Green-closure or clean calibrated-holdout claim.
- **open / conditional deps cited:**
  - `source_note_numbers_stale_against_live_runner`
  - `calibrated_holdout_gap_now_5.371e-01_not_3.714e-03`
  - `raw_cycle_improvement_now_2.81x_not_9.00x`
  - `acceptance_gates_not_asserted_in_runner`
- **auditor confidence:** high

### `staggered_backreaction_iterative_note`

- **Note:** [`STAGGERED_BACKREACTION_ITERATIVE_NOTE.md`](../../docs/STAGGERED_BACKREACTION_ITERATIVE_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_failed~~
- **effective_status:** ~~audited_failed~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The note claims a bounded negative result: linear source maps improve the cycle-bearing force-scale gap only modestly, with best mean gap 6.099e-01 at invheat_b2p00 and no material endogenous closure.  _(class `C`)_
- **chain closes:** False — The live runner preserves the qualitative no-go but materially changes the frozen table, best map, baseline gap, improvement factor, and self-gap values.
- **rationale:** Issue: The exact numerical result in the note is stale relative to scripts/frontier_staggered_backreaction_iterative.py. Current output gives baseline cycle-bearing mean gap 9.618e-01, best mean gap 4.314e-01 at invheat_b3p00, improvement 2.23x, baseline self-gap mean 3.822e-01, and best-map self-gap mean 1.581e+01; the note instead freezes baseline 8.899e-01, best 6.099e-01 at invheat_b2p00, improvement 1.46x, and best-map self-gap 2.275e+00. Why this blocks: the retained negative readout depends on the exact source-map ranking and gap table, and those values now identify a different best map and much larger self-update failure. Repair target: update the note from the current runner or restore the intended artifact, then add assertions for baseline gap, best-map identity, best gap, improvement factor, R^2, two-body residual, TOWARD counts, norm drift, and self-gap. Claim boundary until fixed: it is safe to claim that the current runner still finds no clean cycle-bearing closure from linear source preconditioning, with all rows TOWARD and stable but best self-gap exploding to 1.581e+01; it is not safe to retain the frozen invheat_b2p00 table or the stated 1.46x no-go numerics.
- **open / conditional deps cited:**
  - `STAGGERED_BACKREACTION_NOTE.md`
  - `STAGGERED_LAYERED_BACKREACTION_NOTE.md`
- **auditor confidence:** high

### `staggered_backreaction_nonlocal_closure_note`

- **Note:** [`STAGGERED_BACKREACTION_NONLOCAL_CLOSURE_NOTE.md`](../../docs/STAGGERED_BACKREACTION_NONLOCAL_CLOSURE_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_failed~~
- **effective_status:** ~~audited_failed~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The note claims the fractional-Green nonlocal source sector improves over the local screened baseline but does not materially beat the prior calibrated linear benchmark, with best alpha=0.00 cycle gap 8.590e-02 and holdout gap 5.964e-02.  _(class `C`)_
- **chain closes:** False — The live runner contradicts both the best nonlocal point and the conclusion: current best is alpha=0.40 with cycle gap 1.620e-02, while the layered holdout gap is 7.035e-01, not 5.964e-02.
- **rationale:** Issue: The source note is stale relative to scripts/frontier_staggered_backreaction_nonlocal_closure.py and the drift changes the claim. Current output gives baseline alpha=1.00 cycle gap 3.881e-02, best alpha=0.40 cycle gap 1.620e-02, improvement 2.40x, best holdout gap 7.035e-01, and best shell-fit R^2 values 0.7857/0.8291; the note freezes alpha=0.00 best gap 8.590e-02, holdout 5.964e-02, and concludes no material improvement over the prior calibrated linear benchmark. Why this blocks: the retained negative claim says the nonlocal family does not beat the calibrated linear map, but the current runner says it beats the frozen prior benchmark on cycle-bearing rows while failing the holdout much more severely. Repair target: reconcile the runner and note, define the comparator benchmark from current audited data, update the alpha/gain/gap table and holdout/spectral summaries, and add assertions for best alpha, cycle gap, holdout gap, improvement factor, R^2, additivity, norm drift, and shell/spectral metrics. Claim boundary until fixed: it is safe to claim that the current runner finds a calibrated cycle-bearing improvement at alpha=0.40 with all TOWARD/linearity/additivity/norm checks intact, but a poor layered holdout and continued low-mode bias; it is not safe to claim the frozen alpha=0.00 negative readout or the stated holdout success.
- **open / conditional deps cited:**
  - `STAGGERED_BACKREACTION_ITERATIVE_NOTE.md`
  - `STAGGERED_BACKREACTION_SHELL_SPECTRAL_NOTE.md`
  - `STAGGERED_LAYERED_BACKREACTION_NOTE.md`
- **auditor confidence:** high

### `staggered_backreaction_results_2026-04-10`

- **Note:** [`STAGGERED_BACKREACTION_RESULTS_2026-04-10.md`](../../docs/STAGGERED_BACKREACTION_RESULTS_2026-04-10.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_failed~~
- **effective_status:** ~~audited_failed~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The prototype is claimed to preserve zero-source reduction, machine-precision linear source response, two-body additivity, TOWARD force sign, and one-step endogenous TOWARD behavior while exposing a force-scale gap to the external kernel.  _(class `C`)_
- **chain closes:** False — The live runner contradicts the frozen table and one retained check: only 1/3 source-response rows exceed R^2 > 0.99, and the force/external/self-gap values are materially different from the note.
- **rationale:** Issue: The source note is stale relative to scripts/frontier_staggered_backreaction_prototype.py. Current output gives cycle-row R^2 values 0.9830 and 0.9864, so the runner summary reports only 1/3 families with R^2 > 0.99, not machine-precision linearity on all three; current force values are F_ext=+1.488e+00/+1.750e+00/+1.852e+00, F_solve=+5.593e-02/+6.788e-02/+2.183e-01, mean force gap 9.353e-01, and mean self-gap 2.887e-01, all materially different from the frozen table. Why this blocks: the proposed_retained prototype depends on its retained checks and exact force table, and the current artifact fails the stated all-family source-response check while moving the scale-gap numerics. Repair target: update the note from the current runner or restore the historical artifact, then add assertions for zero-source, R^2 thresholds, two-body residual, TOWARD counts, force gaps, self-gaps, and norm drift. Claim boundary until fixed: it is safe to claim that the current runner still has exact zero-source reduction, TOWARD force sign, additivity, and one-step endogenous TOWARD behavior, but with weak cycle-row source-response linearity and a large mean force gap 9.353e-01; it is not safe to retain the frozen prototype table or the all-family machine-precision linearity claim.
- **open / conditional deps cited:**
  - `STAGGERED_BACKREACTION_NOTE.md`
- **auditor confidence:** high

### `staggered_backreaction_scale_closure_note`

- **Note:** [`STAGGERED_BACKREACTION_SCALE_CLOSURE_NOTE.md`](../../docs/STAGGERED_BACKREACTION_SCALE_CLOSURE_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_failed~~
- **effective_status:** ~~audited_failed~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The note claims one global scalar gain materially closes the cycle-bearing force-scale gap, with best invheat_b1p00 gain 5.374 and calibrated cycle gap 5.869e-02 while retained checks remain intact.  _(class `C`)_
- **chain closes:** False — The live runner materially changes the best map and closure strength: current best is invheat_b3p00 with gain 0.621, calibrated cycle gap 2.053e-01, and holdout gap 7.249e+00.
- **rationale:** Issue: The frozen scale-closure table is stale relative to scripts/frontier_staggered_backreaction_scale_closure.py. Current output gives best map invheat_b3p00, gain 0.621, raw cycle gap 4.314e-01, calibrated cycle gap 2.053e-01, improvement 4.69x, best holdout gap 7.249e+00, and source-response R^2 mean 0.9945; the note claims invheat_b1p00, gain 5.374, calibrated cycle gap 5.869e-02, improvement 15.16x, holdout 1.678e+00, and R^2 mean 0.9998. Why this blocks: the proposed_retained scale-closure claim is exactly about the best calibrated map and size of the force-scale closure, and the current runner shows a much weaker closure with a different map and severe holdout divergence. Repair target: update the note from the current runner or restore the historical artifact, then add assertions for best map identity, fitted gain, raw/calibrated cycle gaps, improvement factor, holdout gap, self-gap, R^2, two-body residual, TOWARD count, and norm drift. Claim boundary until fixed: it is safe to claim that the current runner finds a 4.69x calibrated cycle-gap reduction with checks still passing, but no universal scale closure because the best holdout gap is 7.249e+00; it is not safe to retain the frozen 15.16x invheat_b1p00 closure claim.
- **open / conditional deps cited:**
  - `STAGGERED_BACKREACTION_ITERATIVE_NOTE.md`
  - `STAGGERED_BACKREACTION_RESULTS_2026-04-10.md`
  - `STAGGERED_LAYERED_BACKREACTION_NOTE.md`
- **auditor confidence:** high

### `staggered_backreaction_shell_spectral_note`

- **Note:** [`STAGGERED_BACKREACTION_SHELL_SPECTRAL_NOTE.md`](../../docs/STAGGERED_BACKREACTION_SHELL_SPECTRAL_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_conditional~~
- **effective_status:** ~~audited_conditional~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The note diagnoses the staggered source-to-field miss as structural over-smoothing: phi_solved has much smaller depth span and stronger low-mode concentration than the external-kernel control while the force remains positive but too weak.  _(class `C`)_
- **chain closes:** False — The live runner reproduces the shell/spectral over-smoothing diagnosis, including shell span ratios 0.123 and 0.229 and solved/external low-mode fractions 0.958/0.453 and 0.809/0.355, but the note's exact force readouts are stale against current output.
- **rationale:** Issue: the structural shell/spectral diagnosis survives, but the source note's exact force numbers no longer match the live runner. Why this blocks: a hostile physicist can accept the over-smoothing readout, but cannot cite the note's cycle-family F_ext=+3.247e-01, F_solve=+4.002e-02, gap=8.767e-01 or layered F_ext=+1.714e+00, F_solve=+2.127e-01, gap=8.759e-01 when the current runner reports +1.488e+00, +5.593e-02, 9.624e-01 and +1.852e+00, +2.183e-01, 8.822e-01. Repair target: update the note and archived output to the current force readouts, or restore the old runner state; add assertions for the shell span ratios, low-mode fractions, spectral centroids, force gaps, and norm drift so future drift is caught. Claim boundary until fixed: it is safe to claim that the current runner diagnoses screened graph-Poisson over-smoothing by depth-shell and spectral measures on the two named families; it is not safe to retain the stale exact force table as written.
- **open / conditional deps cited:**
  - `force_readouts_stale_against_live_runner`
  - `cycle_force_gap_now_9.624e-01_not_8.767e-01`
  - `layered_force_gap_now_8.822e-01_not_8.759e-01`
  - `runner_has_no_assertions_for_exact_diagnostics`
- **auditor confidence:** high

### `staggered_graph_failure_map_note`

- **Note:** [`STAGGERED_GRAPH_FAILURE_MAP_NOTE.md`](../../docs/STAGGERED_GRAPH_FAILURE_MAP_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_conditional~~
- **effective_status:** ~~audited_conditional~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The failure-map runner injects odd-cycle/parity defects, dense shortcuts, and high-degree contamination, then classifies same-color parity violations as structural breaks and shortcut/hub cases as graceful degradation when the retained battery remains 8/8.  _(class `C`)_
- **chain closes:** False — The runner reproduces the frozen boundary map, but the retained staggered portability battery it reuses is unaudited and the structural-break labels are assumption-violation classifications rather than empirical battery failures.
- **rationale:** Issue: The table is current, but the claim imports the staggered graph portability battery as a retained authority while that parent remains unaudited; additionally, the odd-cycle and parity-wrap rows are labeled structural_break despite retained=8/8 because they violate bipartite/parity assumptions, not because the measured battery fails. Why this blocks: a retained adversarial boundary map must separate empirical battery failure from assumption-boundary classification and must rest on an audit-clean portability battery. Repair target: audit the graph portability note and the graph-Dirac requirements/bipartite parity assumptions, then add explicit assertions distinguishing same-color-edge structural invalidity from retained-battery pass/fail. Claim boundary until fixed: it is safe to claim that the current runner reproduces the five-row map with odd-cycle and parity-wrap defects flagged as assumption-level structural breaks, dense shortcuts and hub contamination as graceful degradation, and all rows retained=8/8; it is not safe to claim an audit-clean retained portability boundary without the parent battery audit.
- **open / conditional deps cited:**
  - `STAGGERED_GRAPH_PORTABILITY_NOTE.md`
  - `GRAPH_DIRAC_REQUIREMENTS_2026-04-10.md`
- **auditor confidence:** high

### `staggered_graph_gauge_closure_note`

- **Note:** [`STAGGERED_GRAPH_GAUGE_CLOSURE_NOTE.md`](../../docs/STAGGERED_GRAPH_GAUGE_CLOSURE_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_conditional~~
- **effective_status:** ~~audited_conditional~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The note defines a native gauge/current closure criterion: a cycle-bearing graph must show nontrivial persistent-current span and periodic residual closure under flux threaded through the detected cycle edge.  _(class `C`)_
- **chain closes:** False — The source note is a harness/criteria card and does not freeze the measured closure rows or best geometry; the live runner and separate results note carry that evidence.
- **rationale:** Issue: The note is marked proposed_retained but contains expected readout and closure criteria, not the actual measured gauge/current closure table or best-geometry result. Why this blocks: a retained closure claim must state the observed family, current span, residual, and side-battery status in the source note being audited; otherwise the note only defines the acceptance test. Repair target: either demote this card to support/harness status or merge in the frozen runner table and best-geometry readout from the results note, with assertions for current span, residual, cycle/N/A status, and retained side-battery checks. Claim boundary until fixed: it is safe to claim that this note defines the native flux-threaded persistent-current closure criterion and that the current runner can be used to evaluate it; it is not safe to treat this harness note alone as a retained gauge/current closure result.
- **open / conditional deps cited:**
  - `STAGGERED_GRAPH_GAUGE_CLOSURE_RESULTS_2026-04-10.md`
  - `STAGGERED_GRAPH_PORTABILITY_NOTE.md`
- **auditor confidence:** high

### `staggered_graph_gauge_closure_results_2026-04-10`

- **Note:** [`STAGGERED_GRAPH_GAUGE_CLOSURE_RESULTS_2026-04-10.md`](../../docs/STAGGERED_GRAPH_GAUGE_CLOSURE_RESULTS_2026-04-10.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_conditional~~
- **effective_status:** ~~audited_conditional~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The native flux-threaded staggered graph runner shows nontrivial persistent-current span with periodic residual closure on the cycle-bearing stress families, while DAG-compatible gauge rows are N/A or fail when the current span is below threshold.  _(class `C`)_
- **chain closes:** False — The live runner preserves the closure conclusion, but the source freezes stale exact current-span/residual values and the retained side battery comes from the unaudited graph portability machinery.
- **rationale:** Issue: The gauge/current result is qualitatively reproduced, but the exact table is not current: the live runner gives J_span values 6.933e-04, 2.042e-03, 1.343e-04 for the three stress rows and 5.015e-35 for layered s29, while the note freezes 6.922e-04, 2.050e-03, 1.342e-04, and 4.769e-06. The retained side battery is also imported from the unaudited graph portability lane. Why this blocks: the closure result is plausible as a runner-level native gauge/current finding, but an audit-clean retained result needs current exact values and an audit-clean side battery. Repair target: refresh the frozen table from the current runner, add hard assertions for current span > 1e-4, residual < 1e-8, cycle/N/A status, and retained side-battery gates, and audit the graph portability parent. Claim boundary until fixed: it is safe to claim that the current runner closes native gauge/current on the three cycle-bearing stress families and identifies bipartite_growing_stress_s23_n82 as the largest-span row, with layered s29 failing gauge; it is not safe to claim audit-clean retained gauge closure from this note until the table and parent battery are cleaned.
- **open / conditional deps cited:**
  - `STAGGERED_GRAPH_GAUGE_CLOSURE_NOTE.md`
  - `STAGGERED_GRAPH_PORTABILITY_NOTE.md`
- **auditor confidence:** high

### `staggered_graph_observables_note`

- **Note:** [`STAGGERED_GRAPH_OBSERVABLES_NOTE.md`](../../docs/STAGGERED_GRAPH_OBSERVABLES_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_conditional~~
- **effective_status:** ~~audited_conditional~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The graph-observables runner classifies force/current rows as retained observables on graph families, with centroid shift and shell bias treated as secondary diagnostics, and reproduces 8/8 retained rows across the three tested families.  _(class `C`)_
- **chain closes:** False — The runner reproduces the table exactly, but the retained observable split depends on the unaudited staggered graph portability battery and its force/current criteria.
- **rationale:** Issue: The computational table is current, but the note promotes a retained observable taxonomy whose force/current side battery is inherited from the unaudited graph portability lane. Why this blocks: the runner can classify these three rows, but an audit-clean retained observable rule needs the parent force/current battery and gauge-current thresholds closed independently. Repair target: audit the graph portability note and add explicit assertions tying retained rows to force sign, F~M, achromatic force, equivalence, robustness, and gauge-current thresholds while keeping centroid/shell diagnostics secondary. Claim boundary until fixed: it is safe to claim that the current runner reproduces the three-row observable split with retained=8/8, gauge PASS on cycle-bearing graphs, gauge N/A on the layered DAG, and centroid/shell as secondary diagnostics; it is not safe to claim an audit-clean retained graph-observable taxonomy until the parent battery is clean.
- **open / conditional deps cited:**
  - `STAGGERED_GRAPH_PORTABILITY_NOTE.md`
  - `STAGGERED_GRAPH_GAUGE_CLOSURE_RESULTS_2026-04-10.md`
- **auditor confidence:** high

### `staggered_graph_portability_note`

- **Note:** [`STAGGERED_GRAPH_PORTABILITY_NOTE.md`](../../docs/STAGGERED_GRAPH_PORTABILITY_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_conditional~~
- **effective_status:** ~~audited_conditional~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The retained staggered force battery survives on all three graph families, with gauge response on cycle-bearing families and force treated as the primary gravity observable.  _(class `C`)_
- **chain closes:** False — The runner reproduces the three-family battery exactly, but the note and runner only establish a bounded portability probe over constructed graph families and selected force/current readouts, not a retained graph-portability theorem.
- **rationale:** Issue: The runner reproduces the frozen three-family table, but the claim promotes graph portability from a constructed graph-depth force/current battery without a retained theorem tying that readout to the physical gravity observable on arbitrary non-cubic graphs. Why this blocks: a successful three-family smoke battery is not a universal portability closure; it is conditional on the named generated families, threshold choices, parity-coupled potential, and selected force/gauge readouts. Repair target: state this as bounded support, or add an audited theorem and acceptance harness deriving the graph-depth force observable and gauge-current thresholds before broadening to stress and holdout graph families. Claim boundary until fixed: safe to claim the current runner reproduces 8/8 retained-battery rows on the three named graph families with TOWARD force and gauge PASS/N/A; not safe to claim audit-clean retained portability beyond this checkpoint.
- **auditor confidence:** high

### `staggered_graph_portability_stress_note`

- **Note:** [`STAGGERED_GRAPH_PORTABILITY_STRESS_NOTE.md`](../../docs/STAGGERED_GRAPH_PORTABILITY_STRESS_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_conditional~~
- **effective_status:** ~~audited_conditional~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The retained staggered force battery survives the larger, more irregular bipartite families, with no retained-row failure in the stress run.  _(class `C`)_
- **chain closes:** False — The runner preserves all PASS/N/A row statuses on the four stress families, but this is a stress probe built from the same conditional graph-depth force/current readout as the baseline portability note, not a standalone retained portability theorem.
- **rationale:** Issue: The stress runner has no retained-row failures, but the claim strengthens portability by reusing the baseline graph-depth force/current battery before that battery has a retained derivation as the physical gravity observable on arbitrary non-cubic graphs; additionally, the live gauge magnitudes drift slightly from the frozen table while keeping PASS status. Why this blocks: larger stress families test robustness of a selected probe, but they do not close the missing observable/readout theorem or turn finite-family evidence into audit-clean retained portability. Repair target: first audit-clean the baseline graph force/current observable and thresholds, then make the stress note an asserted holdout battery with exact current output or toleranced assertions. Claim boundary until fixed: safe to claim the current stress runner gives 8/8 retained-row PASS/N/A on the four named stress graph families, with current gauge values about 6.193e-04, 1.861e-03, 1.176e-04, and N/A; not safe to claim clean retained graph-portability closure from this stress run alone.
- **open / conditional deps cited:**
  - `STAGGERED_GRAPH_PORTABILITY_NOTE.md`
- **auditor confidence:** high

### `staggered_layered_gauge_engineering_note`

- **Note:** [`STAGGERED_LAYERED_GAUGE_ENGINEERING_NOTE.md`](../../docs/STAGGERED_LAYERED_GAUGE_ENGINEERING_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_conditional~~
- **effective_status:** ~~audited_conditional~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** Native gauge/current closure is possible on a layered graph when the loop geometry is made explicit and well-conditioned.  _(class `C`)_
- **chain closes:** False — The live runner preserves the N/A/FAIL/PASS/PASS gauge classification and engineered brickwall closure, but the frozen exact current table is stale and the retained force side battery is reused from the conditional graph-portability lane.
- **rationale:** Issue: The qualitative engineered-gauge conclusion reproduces, but the note's exact current table is stale for the sparse layered holdout: the live runner gives J_span about 5.015e-35 rather than 4.769e-06, and the force side battery is imported from the conditional staggered graph portability probe. Why this blocks: an audit-clean retained claim cannot freeze incorrect exact numerics or promote a gauge/current engineering result while the underlying graph force/current readout remains conditional. Repair target: update the note to the current runner output with toleranced assertions, and close or explicitly bound the inherited graph-portability observable theorem. Claim boundary until fixed: safe to claim the current runner classifies the acyclic control as N/A, the sparse cycle holdout as gauge FAIL, and the two engineered brickwall geometries as gauge PASS with current spans about 2.279e-03 and 2.151e-03; not safe to claim clean retained gauge engineering with the frozen exact table as written.
- **open / conditional deps cited:**
  - `STAGGERED_GRAPH_PORTABILITY_NOTE.md`
- **auditor confidence:** high

### `staggered_layered_gauge_phase_diagram_note`

- **Note:** [`STAGGERED_LAYERED_GAUGE_PHASE_DIAGRAM_NOTE.md`](../../docs/STAGGERED_LAYERED_GAUGE_PHASE_DIAGRAM_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_conditional~~
- **effective_status:** ~~audited_conditional~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The practical pass/fail boundary is that nearest-neighbor layered brickwall/plaquette graphs pass, sparse layered holdouts and most long-shift layered loops fail, and acyclic DAG controls are N/A.  _(class `C`)_
- **chain closes:** False — The live runner preserves the finite PASS/FAIL/N/A classification, but the exact current-span table is stale and the promoted geometry criterion is an empirical finite-sweep rule over the conditional graph-current readout, not a retained theorem.
- **rationale:** Issue: The current runner reproduces the qualitative phase map, but many frozen J_span values are stale, the sparse holdout is now about 5.015e-35 rather than 4.769e-06, and the claimed plaquette-quality criterion is a finite empirical classification over a conditional graph-current observable. Why this blocks: a proposed_retained phase-diagram criterion needs either exact current output and toleranced assertions, or a theorem deriving the boundary; the runner shows PASS rows with square-plaquette density 0.00 and FAIL rows with density up to 0.25, so the scalar criterion is not closed as stated. Repair target: update the table to live output, define the actual graph feature used by the criterion, and prove or assert-test the boundary on holdouts after the graph force/current observable is audited clean. Claim boundary until fixed: safe to claim the live runner gives 15 PASS, 10 FAIL, and 1 N/A rows, with all step-1 brickwall/defect rows passing and step-2 rows failing; not safe to claim an audit-clean retained geometry criterion from this sweep alone.
- **open / conditional deps cited:**
  - `STAGGERED_GRAPH_PORTABILITY_NOTE.md`
  - `STAGGERED_LAYERED_GAUGE_ENGINEERING_NOTE.md`
- **auditor confidence:** high

### `strong_cp_theta_zero_note`

- **Note:** [`STRONG_CP_THETA_ZERO_NOTE.md`](../../docs/STRONG_CP_THETA_ZERO_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_conditional~~
- **effective_status:** ~~audited_conditional~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The note sets the retained action class to S_ret = S_Wilson + psi_bar(D[U]+m)psi with no bare θ slot, so θ_bare = 0 by the retained action-surface definition and arg det(M_u M_d)=0 on an explicit positive-mass surface gives θ_eff = 0.  _(class `E`)_
- **chain closes:** False — The runner verifies many consistency checks on the θ-free Wilson-plus-staggered scalar-mass surface, but the absence of a CP-odd F tilde F/θ operator and the positive real quark-mass surface are selected as retained action-class premises rather than derived from registered one-hop authorities.
- **rationale:** Issue: the decisive step is not a computed strong-CP cancellation but the retained-action-surface selection: the runner/support text takes 'no bare θ slot' and θ_bare = 0 from the action-class definition, and it uses an explicit positive real quark-mass surface for arg det(M_u M_d)=0. Why this blocks: the 13 theorem and 30 retained-surface compute passes show internal consistency of that restricted θ-free Wilson-plus-staggered scalar-mass surface, but they do not derive from the provided audit packet that the physical Cl(3)/Z^3 action forbids an allowed CP-odd F tilde F term, fixes the real-mass orientation, or dynamically selects θ=0 rather than merely evaluating the θ-free surface; the sampled topological positivity check also demonstrates the triangle-inequality minimum, not a derivation of the missing action-slot theorem. Repair target: add a retained operator-basis/action-surface theorem deriving from Cl(3)/Z^3 primitives and canonical normalization that no gauge-invariant CP-odd θ term is an admissible slot, register the positive real quark-mass orientation/arg-det theorem as a dependency, and update the runner so it constructs the allowed action basis and fails if an F tilde F term or complex mass phase is admitted. Claim boundary until fixed: it is safe to claim that on the explicitly θ-free Wilson-plus-staggered scalar-mass surface, the implemented determinant, axial-grid, effective-action, and sampled positive-weight checks find no generated strong-sector phase; it is not yet an audited retained solution of strong CP beyond that selected action surface.
- **open / conditional deps cited:**
  - `retained_action_surface_no_theta_slot_theorem_not_registered`
  - `positive_real_quark_mass_orientation_theorem_not_registered`
  - `theta_free_surface_selection_not_dynamical_theta_minimization`
- **auditor confidence:** high

### `structured_chokepoint_bridge_extension_note`

- **Note:** [`STRUCTURED_CHOKEPOINT_BRIDGE_EXTENSION_NOTE.md`](../../docs/STRUCTURED_CHOKEPOINT_BRIDGE_EXTENSION_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_conditional~~
- **effective_status:** ~~audited_conditional~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The larger-N replay widened the retained pocket on the same structured family while keeping the canonical mirror readout fixed.  _(class `C`)_
- **chain closes:** False — The runner reproduces the N=60,80,100 table exactly, but the extension depends on the base structured chokepoint bridge and canonical mirror readout, both currently conditional rather than audit-clean retained inputs.
- **rationale:** Issue: The live runner matches the frozen larger-N replay, but the claim is an extension of the structured chokepoint bridge pocket, whose base bridge and canonical mirror chokepoint readout remain audited_conditional. Why this blocks: the extension can show that the same harness continues to give Born-clean, k=0-pinned, positive-gravity rows at N=60,80,100, but it cannot promote the underlying bridge/readout to a clean retained physical result. Repair target: close the base structured chokepoint bridge and mirror chokepoint readout as audited-clean inputs, or restate this note as bounded support conditional on those harness definitions. Claim boundary until fixed: safe to claim the current runner exactly reproduces the three larger-N rows with 16/16 usable seeds, zero Born/k=0 readouts, and positive gravity through N=100; not safe to claim an audit-clean widened retained bridge independent of the conditional parent pocket.
- **open / conditional deps cited:**
  - `STRUCTURED_CHOKEPOINT_BRIDGE_NOTE.md`
  - `MIRROR_CHOKEPOINT_NOTE.md`
- **auditor confidence:** high

### `structured_chokepoint_bridge_note`

- **Note:** [`STRUCTURED_CHOKEPOINT_BRIDGE_NOTE.md`](../../docs/STRUCTURED_CHOKEPOINT_BRIDGE_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_conditional~~
- **effective_status:** ~~audited_conditional~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The structured bridge pocket is Born-clean at machine precision and keeps positive gravity across the narrow probe set.  _(class `C`)_
- **chain closes:** False — The live runner reproduces the finite table, but the retained bridge claim depends on a selected structured-placement slice and an imported canonical mirror readout that are not registered as audited dependencies or asserted as hard gates.
- **rationale:** Issue: the runner supports the finite N=25,40,60 structured chokepoint card, but the note promotes that selected slice as a retained bridge pocket without a registered canonical-readout dependency or theorem selecting the graph parameters. Why this blocks: a hostile auditor can verify the printed table, but cannot infer architecture-level bridge closure, asymptotic behavior, or readout-independent survival from the current packet; the runner also prints diagnostics rather than enforcing hard assertions for Born, k=0, gravity significance, and decoherence gates. Repair target: register the canonical mirror chokepoint harness as a one-hop dependency, add hard assertions/tolerances for the retained gates, and either derive the structured placement/readout selection or state the claim strictly as a finite parameter-card result. Claim boundary until fixed: it is safe to claim the current finite card: for the specified structured placement with NPL_HALF=25, connect_radius=3.5, layer_jitter=0.25, 16 seeds, and N=25/40/60, the runner reports machine-clean Born, zero k=0, positive mean gravity, nontrivial d_TV, and N=60 pur_cl around 0.803; it is not a broader structured-architecture or asymptotic bridge theorem.
- **open / conditional deps cited:**
  - `scripts/mirror_chokepoint_joint.py_canonical_readout_not_registered_one_hop_dependency`
  - `structured_placement_parameter_selection_not_derived`
  - `runner_prints_diagnostics_without_hard_gate_assertions`
- **auditor confidence:** high

### `structured_mirror_bornsafe_scan_note`

- **Note:** [`STRUCTURED_MIRROR_BORNSAFE_SCAN_NOTE.md`](../../docs/STRUCTURED_MIRROR_BORNSAFE_SCAN_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_failed~~
- **effective_status:** ~~audited_failed~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The queue treats the note as proposed_retained, but the source note's load-bearing result is that no proposed-retained Born-safe structured-mirror pocket was found in the scanned linear family.  _(class `C`)_
- **chain closes:** False — The positive proposed-retained chain does not close because the source note and runner output explicitly report no retained Born-safe pocket. The broad two-seed scan measured all 540 grid rows and printed no retained pocket, and the six-seed replay of the best near-Born candidate remained at Born = 8.79e-03, far above the 1e-10 threshold.
- **rationale:** Issue: this is a parser false positive for the audit queue: the status line contains the token proposed_retained only inside the negative statement that no proposed_retained Born-safe structured-mirror pocket was found. Why this blocks: a hostile auditor cannot certify a retained structured-mirror Born-safe successor when the source note, the full two-seed grid replay, and the six-seed best-candidate replay all say the opposite; the best candidate remains Born = 8.79e-03, many orders above the 1e-10 corrected Born threshold. Repair target: either retag this note as a bounded negative-control/exhaustion result, or produce a new registered scan/log with a structured-mirror parameter card satisfying Born < 1e-10, positive gravity, pur_cl < 0.95, k=0 control, and enough seeds to rule out a fluke. Claim boundary until fixed: it is safe to claim only the negative scan result: under the stated d_growth=2 linear-propagator grid, no retained Born-safe structured-mirror pocket was found, and structured mirror growth is not currently a Born-safe replacement for the exact mirror or Z2 x Z2 lanes.
- **open / conditional deps cited:**
  - `source_status_is_negative_no_proposed_retained_pocket_found`
  - `full_scan_runner_prints_RETAINED_POCKET_none_found`
  - `best_near_Born_candidate_six_seed_replay_Born_8.79e-03_above_1e-10`
  - `queue_status_parser_false_positive_on_negative_proposed_retained_phrase`
- **auditor confidence:** high

### `symmetry_head_to_head_note`

- **Note:** [`SYMMETRY_HEAD_TO_HEAD_NOTE.md`](../../docs/SYMMETRY_HEAD_TO_HEAD_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_conditional~~
- **effective_status:** ~~audited_conditional~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The note claims a review-safe apples-to-apples comparison between the proposed-retained exact mirror chokepoint lane and the retained dense Z2 x Z2 lane, ranking mirror as stronger on shared-row gravity and Z2 x Z2 as stronger on decoherence depth and retained range.  _(class `C`)_
- **chain closes:** False — The head-to-head script reproduces the printed finite comparison table, and a live dense Z2 x Z2 joint replay reproduces the imported N=80/100/120 values. The clean retained comparison chain does not close because the canonical mirror, mirror-MI, and higher-symmetry joint sources are audited_conditional, the gravity-probe source is bounded/unaudited rather than retained, and the head-to-head runner is a hardcoded table with no source-trace or pass/fail assertions.
- **rationale:** Issue: the finite side-by-side numbers are reproducible, but the note presents a review-safe retained lane comparison before the cited lanes are cleanly audited. Why this blocks: a hostile auditor can verify the hardcoded head-to-head table and the live dense Z2 x Z2 replay, but cannot certify the comparison as retained while docs/MIRROR_CHOKEPOINT_NOTE.md, docs/MIRROR_MUTUAL_INFORMATION_CHOKEPOINT_NOTE.md, and docs/HIGHER_SYMMETRY_JOINT_VALIDATION_NOTE.md remain audited_conditional, docs/HIGHER_SYMMETRY_GRAVITY_PROBE_NOTE.md is only bounded/unaudited, and the comparison script does not enforce or source-check the constants. Repair target: clean or replace the upstream mirror and Z2 x Z2 validation packets, register/archive the missing dense joint log, add assertions tying each displayed number to its source runner/log and clarifying gravity@k=5 versus band-gravity conventions, and assert the comparison predicates directly. Claim boundary until fixed: it is safe to claim a finite diagnostic table: on the displayed N=80/100 rows, the hardcoded script and live dense Z2 x Z2 replay support the numeric comparison, with mirror higher on the displayed gravity@k=5 values and Z2 x Z2 lower in pur_cl and extending to N=120 in the dense replay; it is not yet a clean retained lane-ranking theorem.
- **open / conditional deps cited:**
  - `MIRROR_CHOKEPOINT_NOTE.md_audited_conditional`
  - `MIRROR_MUTUAL_INFORMATION_CHOKEPOINT_NOTE.md_audited_conditional`
  - `HIGHER_SYMMETRY_JOINT_VALIDATION_NOTE.md_audited_conditional`
  - `HIGHER_SYMMETRY_GRAVITY_PROBE_NOTE.md_bounded_unaudited`
  - `logs/2026-04-03-higher-symmetry-joint-validation-z2z2-dense-n80-n120.txt_missing`
  - `scripts/symmetry_head_to_head.py_hardcoded_table_no_source_trace_assertions`
- **auditor confidence:** high

### `taste_scalar_isotropy_theorem_note`

- **Note:** [`TASTE_SCALAR_ISOTROPY_THEOREM_NOTE.md`](../../docs/TASTE_SCALAR_ISOTROPY_THEOREM_NOTE.md)
- **current_status:** bounded
- **audit_status:** ~~audited_conditional~~
- **effective_status:** ~~audited_conditional~~  (reason: `self`)
- **auditor:** `codex-audit-loop:fresh-2026-04-28-taste_scalar_isotropy_theorem_note`  (codex-current; independence=fresh_context)
- **load-bearing step:** At phi=(v,0,0), the Hessian reduces to the binary orthogonality sum sum_s (-1)^{s_i}(-1)^{s_j}=8 delta_ij, so the fermion Coleman-Weinberg curvature is isotropic.  _(class `A`)_
- **chain closes:** False — The exact fermion-CW Hessian isotropy theorem closes on the stated Cl(3)/Z^3 commuting-involution taste block, and the live runner reports THEOREM PASS=30 BOUNDED PASS=6 FAIL=0. The scalar-spectrum split, near-degenerate taste-pair readout, and thermal-transition estimate are explicitly bounded model consequences rather than theorem-grade closures.
- **rationale:** Issue: the exact isotropy theorem closes for the fermion Coleman-Weinberg block, but the note's scalar-spectrum and electroweak-transition consequences depend on a gauge-only leading split and a scalar-only thermal-cubic estimate that the note explicitly labels bounded.
Why this blocks: downstream proposed-retained/promoted claims cannot use this row as a theorem-grade Higgs/taste spectrum, y_b, generation-splitting, or electroweak-transition closure; they only inherit the no-fermion-CW-splitting boundary.
Repair target: supply and audit a full scalar-sector theorem, including gauge/taste-breaking and thermal dynamics, with a runner that derives the spectrum or transition result rather than checking the bounded companion model.
Claim boundary until fixed: safe to claim exact fermion-CW isotropy and the resulting exclusion of scalar-CW-only splitting on the stated taste block, not full scalar-spectrum or finite-temperature electroweak closure.
- **open / conditional deps cited:**
  - `bounded_gauge_only_taste_scalar_split_model`
  - `bounded_scalar_only_thermal_cubic_estimate`
- **auditor confidence:** high

### `tensor_scalar_ratio_consolidation_theorem_note_2026-04-22`

- **Note:** [`TENSOR_SCALAR_RATIO_CONSOLIDATION_THEOREM_NOTE_2026-04-22.md`](../../docs/TENSOR_SCALAR_RATIO_CONSOLIDATION_THEOREM_NOTE_2026-04-22.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_conditional~~
- **effective_status:** ~~audited_conditional~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** On the graph-growth primordial spectrum surface r = d^2/N_e^2, and ANOMALY_FORCES_TIME supplies d = 3, so the structural form reduces to r = 9/N_e^2; at bounded-observational N_e = 60 this gives r = 0.0025.  _(class `B`)_
- **chain closes:** False — The runner verifies the arithmetic and source-note comparator statements once the spectrum formula, d=3 input, and N_e=60 value are supplied. It does not derive r=d^2/N_e^2, does not audit ANOMALY_FORCES_TIME as a one-hop dependency, and explicitly leaves N_e bounded-observational rather than axiom-native.
- **rationale:** Issue: the theorem-grade claim depends on unregistered upstream authorities and on the bounded observational choice N_e=60. Why this blocks: the primary runner sets d=3 and N_e=60, accepts the graph-growth formula r=d^2/N_e^2 as a retained input, and checks arithmetic plus observational-bound comparisons; it does not derive the spectrum formula from the supplied audit packet, prove d=3 from ANOMALY_FORCES_TIME inside the runner, or derive N_e from Cl(3)/Z^3 and pre-inflation seed size. Repair target: register PRIMORDIAL_SPECTRUM_NOTE.md and ANOMALY_FORCES_TIME_THEOREM.md as one-hop dependencies with clean audits, add a retained computation of N_e or explicitly demote the numerical r forecast to bounded, and update comparator bounds through a current retained/observational-status note. Claim boundary until fixed: it is safe to claim the conditional structural arithmetic r=9/N_e^2 if the spectrum formula and d=3 theorem are accepted, and r=0.0025 at N_e=60; it is not safe to claim a fully retained tensor-to-scalar prediction from the sole axiom.
- **open / conditional deps cited:**
  - `PRIMORDIAL_SPECTRUM_NOTE.md_not_registered_one_hop_dependency`
  - `ANOMALY_FORCES_TIME_THEOREM.md_not_registered_one_hop_dependency`
  - `N_e_from_Cl3_Z3_preinflation_seed_size_retained_derivation_open`
  - `higher_order_tensor_scalar_ratio_corrections_open`
  - `graph_growth_inflaton_field_potential_mapping_open`
  - `current_CMB_r_bounds_and_projected_sensitivities_observational_status_not_registered`
- **auditor confidence:** high

### `testable_predictions_map_note`

- **Note:** [`TESTABLE_PREDICTIONS_MAP_NOTE.md`](../../docs/TESTABLE_PREDICTIONS_MAP_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_failed~~
- **effective_status:** ~~audited_failed~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** This note is a compact, adversarial map of the best current testable predictions across the retained science on main, with each entry recording what is already retained.  _(class `B`)_
- **chain closes:** False — The source-note catalog does not close against its one-hop cited authorities: several entries marked as already retained are bounded, conditional, or still unaudited, and the final ranking is internally inconsistent with the numbered ranking.
- **rationale:** Issue: The map claims to rank current proposed_retained testables and to record what is already retained, but its cited authorities include bounded or conditional notes such as the diamond protocol/prediction lane, the wavefield escalation note, the growing-graph expansion card, and the generated-family bridge; the note also lists seven ranked entries but the later current ranking drops the grown-trapping and growing-expansion entries and reorders the list. Why this blocks: a retained catalog cannot assert current retained status or a stable ranking when the one-hop sources and the note's own ranking sections disagree. Repair target: regenerate the map from the audit ledger, separating audited-clean/retained, conditional, bounded, and unaudited items, and make the numbered ranking, top-3, and bottom-line sections mechanically consistent. Claim boundary until fixed: safe to treat this as a stale editorial snapshot of candidate testable lanes; not safe to cite it as a retained current map of audit-clean testable predictions.
- **open / conditional deps cited:**
  - `DIAMOND_SENSOR_PREDICTION_NOTE.md`
  - `DIAMOND_SENSOR_PROTOCOL_NOTE.md`
  - `DIAMOND_NV_PHASE_RAMP_SIGNAL_BUDGET_NOTE.md`
  - `SOURCE_RESOLVED_WAVEFIELD_ESCALATION_NOTE.md`
  - `GROWING_GRAPH_EXPANSION_CARD_NOTE.md`
  - `SOURCE_RESOLVED_GENERATED_NEW_FAMILY_V2_NOTE.md`
  - `WIDE_LATTICE_H2T_DISTANCE_LAW_NOTE.md`
- **auditor confidence:** high

### `third_grown_family_sign_note`

- **Note:** [`THIRD_GROWN_FAMILY_SIGN_NOTE.md`](../../docs/THIRD_GROWN_FAMILY_SIGN_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_conditional~~
- **effective_status:** ~~audited_conditional~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The family has a real bounded basin: 5/15 rows pass with exact zero and neutral controls, correct sign orientation on retained rows, and near-linear charge scaling.  _(class `C`)_
- **chain closes:** False — The live runner reproduces the 5/15 bounded-basin result exactly, but the boundary note is unaudited and the claim remains a finite sampled basin over selected drifts/seeds rather than a closed family-wide theorem.
- **rationale:** Issue: The current runner confirms the reported bounded basin, but the note's retained interpretation depends on an unaudited boundary note and on treating five passing drift/seed rows as a real basin rather than a finite sampled pocket. Why this blocks: exact controls and sign orientation close for the passing rows, but they do not prove a stable family-level basin or an independent geometry theorem beyond the tested grid. Repair target: audit the boundary note and add a holdout/tolerance harness or theorem defining the basin over a drift interval and seed family, not just the sampled rows. Claim boundary until fixed: safe to claim the live sweep has 5/15 passing rows, exact zero and neutral controls on the table, drift coverage 0.1/0.2/0.3 among passes, and mean exponent 0.999842; not safe to claim audit-clean retained third-grown-family closure beyond that finite bounded pocket.
- **open / conditional deps cited:**
  - `THIRD_GROWN_FAMILY_BOUNDARY_NOTE.md`
- **auditor confidence:** high

### `three_family_card_note`

- **Note:** [`THREE_FAMILY_CARD_NOTE.md`](../../docs/THREE_FAMILY_CARD_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_failed~~
- **effective_status:** ~~audited_failed~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** Three independent grown families produce quantitatively identical physics on all 9 measurable properties to within 5%.  _(class `B`)_
- **chain closes:** False — The source table itself leaves Family 3 Distance alpha as '(not yet)', and no runner is provided to recompute the 9-property comparison, so the headline 9/9 three-family match does not close.
- **rationale:** Issue: The note claims three families match on all 9 measurable properties, but the table explicitly has Family 3 Distance alpha marked '(not yet)' and the note provides no runner or log artifact to verify the cross-family card. Why this blocks: the load-bearing 9/9 statement is false on the face of the supplied table, and the broader inference that observables are geometry-independent cannot follow from a partial, hand-entered comparison. Repair target: add a runner that recomputes every listed property for all three families, including Family 3 Distance alpha, with explicit <5% assertions and at least one holdout check. Claim boundary until fixed: safe to cite this as a partial comparison of three selected drift/restore rows with eight populated properties and distance-alpha data only for Families 1 and 2; not safe to claim 9/9 three-family equality or geometry-independence.
- **auditor confidence:** high

### `triage_no_promotion_note`

- **Note:** [`TRIAGE_NO_PROMOTION_NOTE.md`](../../docs/TRIAGE_NO_PROMOTION_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_failed~~
- **effective_status:** ~~audited_failed~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** No draft in the current dirty stack clearly clears the retained bar beyond the basin and unification wins already on main.  _(class `B`)_
- **chain closes:** False — The note relies on an ephemeral dirty/untracked stack with no manifest or runner, and its cited baseline includes items now audited failed or conditional, so the no-promotion claim cannot be verified from repo-contained inputs.
- **rationale:** Issue: The note's central claim is a process judgment over a 'current dirty / untracked stack' that is not preserved as a repo manifest, runner, or reproducible input set, and the cited retained baseline now includes GROWN_TRANSFER_BASIN_NOTE as audited_failed and EARLY_FAMILY_TRANSFER_CONNECTIVITY_DIAGNOSIS as audited_conditional. Why this blocks: an audit cannot verify that no dirty draft cleared the bar, nor can it rely on a baseline whose own retained status is not clean. Repair target: replace the note with a reproducible triage manifest listing every draft artifact, its runner/log, and the exact promotion criterion, or demote it to a historical process memo outside retained science. Claim boundary until fixed: safe to say this was a dated editorial no-promotion snapshot; not safe to cite it as an audited retained conclusion about the current stack or about science promotion status.
- **open / conditional deps cited:**
  - `GROWN_TRANSFER_BASIN_NOTE.md`
  - `EARLY_FAMILY_TRANSFER_CONNECTIVITY_DIAGNOSIS.md`
- **auditor confidence:** high

### `unified_basin_freeze_note`

- **Note:** [`UNIFIED_BASIN_FREEZE_NOTE.md`](../../docs/UNIFIED_BASIN_FREEZE_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_failed~~
- **effective_status:** ~~audited_failed~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** One retained grown connectivity family supports both signed-source and complex-action couplings across a small nearby basin, with exact zero and neutral controls passing cleanly.  _(class `B`)_
- **chain closes:** False — The signed-source basin replay passes, but the complex-action evidence is a fixed-row kernel-vs-gravity comparison rather than the same nearby basin, and the actual fixed-field complex grown basin runner reports 0/2 exact gamma=0/Born survivors.
- **rationale:** Issue: The note combines two different surfaces as one unified basin: NONLABEL_GROWN_BASIN_TARGETED still gives 3/3 signed-source rows with exact zero/neutral controls, but complex_action_kernel_vs_gravity is a fixed-row kernel/generic-vs-gravity separation test, not a nearby basin; the actual FIXED_FIELD_COMPLEX_GROWN_BASIN runner gives exact gamma=0 + Born proxy survivors 0/2. Why this blocks: the claim that one grown connectivity family supports both couplings across a small nearby basin with exact controls is not computed by the supplied runners and is contradicted by the available complex-basin runner. Repair target: provide a single unified runner over the same drift/restore neighborhood and seed set, with explicit zero/neutral/gamma=0/Born assertions for both coupling surfaces, or split the note into separate retained/failed components. Claim boundary until fixed: safe to claim the signed-source non-label basin currently passes 3/3 at restore 0.60/0.70/0.80, and the kernel-vs-gravity fixed-row runner separates absorption from gravity-specific deflection; not safe to claim a unified two-coupling basin.
- **open / conditional deps cited:**
  - `KERNEL_VS_GRAVITY_NOTE.md`
- **auditor confidence:** high

### `unpromoted_branch_retainability_audit_note`

- **Note:** [`UNPROMOTED_BRANCH_RETAINABILITY_AUDIT_NOTE.md`](../../docs/UNPROMOTED_BRANCH_RETAINABILITY_AUDIT_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_conditional~~
- **effective_status:** ~~audited_conditional~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** No mistaken closure is required on the tested rows; the overreach risk is in generalizing beyond the retained row-level results or treating a retained proxy as a family-wide law.  _(class `B`)_
- **chain closes:** False — The note is a cross-note retainability inventory with no registered dependencies and no runner, so its boundary conclusions cannot be independently checked from the audit packet alone.
- **rationale:** Issue: the proposed-retained row summarizes promotion boundaries across wider-family, grown-transfer, graph-frontier, and persistent-object lanes, but registers no one-hop dependencies and provides no runner or machine-checkable status/output inventory. Why this blocks: a hostile auditor cannot verify from the source note alone that the referenced rows, logs, statuses, and boundary claims are current or correctly characterized, even though the conservative no-overpromotion advice is plausible and safe. Repair target: register the cited notes/scripts/logs as explicit dependencies or add a status-audit runner that checks each referenced artifact, current status, runner output, and permitted wording boundary. Claim boundary until fixed: it is safe to treat this as a conservative branch-to-main editorial handoff saying not to broaden finite row-level positives into family-wide, continuum, cosmology, detector-localization, or persistent-mass claims; it is not an independently audited retained physics theorem.
- **open / conditional deps cited:**
  - `H0125_WIDER_W4_NOTE.md_not_registered_one_hop_dependency`
  - `H0125_WIDER_REPLAY_NOTE.md_not_registered_one_hop_dependency`
  - `GATE_B_GROWN_JOINT_PACKAGE_NOTE.md_not_registered_one_hop_dependency`
  - `GATE_B_GROWN_DISTANCE_LAW_NOTE.md_not_registered_one_hop_dependency`
  - `GATE_B_NONLABEL_SIGN_GROWN_TRANSFER_NOTE.md_not_registered_one_hop_dependency`
  - `GROWING_GRAPH_FRONTIER_EXPANSION_PROXY_NOTE.md_not_registered_one_hop_dependency`
  - `scripts/persistent_object_localization_escalation.py_not_registered_one_hop_dependency`
- **auditor confidence:** high

### `valley_linear_continuum_synthesis_note`

- **Note:** [`VALLEY_LINEAR_CONTINUUM_SYNTHESIS_NOTE.md`](../../docs/VALLEY_LINEAR_CONTINUUM_SYNTHESIS_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_conditional~~
- **effective_status:** ~~audited_conditional~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The note synthesizes a continuum valley-linear 1/b derivation with bounded lattice artifacts, claiming a real ordered-lattice action fork with near-Newtonian 3D finite-lattice behavior, action-independent decoherence on the tested family, and remaining open 4D/Gate-B/asymptotic questions.  _(class `C`)_
- **chain closes:** False — The primary same-harness replay reproduces the bounded valley-linear comparison, and the decoherence replay verifies exact action-independence on the tested zero-field family. The synthesis chain does not close cleanly because the analytic derivation is not registered/audited, the cited lattice notes are bounded or unknown and unaudited, and the note explicitly leaves the asymptotic bridge, 4D tail, transfer-norm, Gate B, and UV-completion reading open.
- **rationale:** Issue: the bounded synthesis is plausible as a finite artifact summary, but it is not a clean proposed-retained continuum theorem because every load-bearing upstream packet is either bounded/unknown, unaudited, or explicitly open. Why this blocks: a hostile auditor can replay the same-family comparison (Born 4.20e-15, k=0 zero, valley-linear F~M 1.00, tail -0.93) and the decoherence identity (zero deltas across actions at h=1.0, 0.5, 0.25), but cannot promote the synthesis while the continuum derivation lives outside the audit ledger, the asymptotic bridge remains slice-dependent, dimensional and decoherence notes have unknown audit status, and the note itself says the 4D, Gate B, transfer-norm, and UV-completion readings are open. Repair target: register/audit the analytic derivation, audit VALLEY_LINEAR_ACTION_NOTE, VALLEY_LINEAR_ROBUSTNESS_NOTE, VALLEY_LINEAR_ASYMPTOTIC_BRIDGE_NOTE, DIMENSIONAL_GRAVITY_TABLE, and DECOHERENCE_ACTION_INDEPENDENCE_NOTE, add a synthesis runner that asserts the exact finite rows and the open boundaries, and resolve whether the derivation is a theorem or only an effective continuum approximation. Claim boundary until fixed: it is safe to claim a bounded ordered-lattice action-fork summary: the live runners support the finite h=0.25 same-family comparison and tested zero-field decoherence identity, but not a universal continuum theorem, 4D law, Gate-B transfer, or final closure claim.
- **open / conditional deps cited:**
  - `.claude/science/derivations/valley-linear-distance-law-2026-04-04.md_not_registered_or_audited`
  - `VALLEY_LINEAR_ACTION_NOTE.md_bounded_unaudited`
  - `VALLEY_LINEAR_ROBUSTNESS_NOTE.md_bounded_unaudited`
  - `VALLEY_LINEAR_ASYMPTOTIC_BRIDGE_NOTE.md_bounded_unaudited`
  - `DIMENSIONAL_GRAVITY_TABLE.md_unknown_unaudited`
  - `DECOHERENCE_ACTION_INDEPENDENCE_NOTE.md_unknown_unaudited`
  - `asymptotic_bridge_slice_dependence_open`
  - `4D_tail_law_transfer_norm_Gate_B_and_UV_completion_open`
- **auditor confidence:** high

### `vector_magnetic_extension_note`

- **Note:** [`VECTOR_MAGNETIC_EXTENSION_NOTE.md`](../../docs/VECTOR_MAGNETIC_EXTENSION_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_clean~~
- **effective_status:** **retained**  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The note claims a proposed-retained narrow extension: on a compact exact lattice, a bounded odd-in-v moving-source centroid response survives exact zero/static controls while the circulation-like plaquette candidate remains null.  _(class `C`)_
- **chain closes:** True — The live runner exactly reproduces the source-note card: zero-source static, zero-source moving, and zero-source plaquette-circulation controls are all 0.000e+00; the v=0 matched static lane has delta_y vs static +0.000000e+00; nonzero velocities give symmetric signed responses, with v=+1.00 at +2.084652e-05 and v=-1.00 at -2.084652e-05; all probed circulation phases remain +0.000e+00.
- **rationale:** The finite proxy claim closes on its own terms: the runner builds the compact exact-lattice card, applies exact zero and matched static controls, verifies a 4/4 odd-sign moving-source centroid response, and verifies null final-layer plaquette circulation. This clean audit is narrow: it certifies only the displayed compact-family moving-source signed response and null circulation candidate; it does not certify full electromagnetism, magnetic induction, gauge-field structure, a vector-field theory, or portability beyond this compact exact-lattice card.
- **auditor confidence:** high

### `vector_sector_note`

- **Note:** [`VECTOR_SECTOR_NOTE.md`](../../docs/VECTOR_SECTOR_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_conditional~~
- **effective_status:** ~~audited_conditional~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The vector sector is a phase-locked first-harmonic handedness signal with 1H amplitude 0.018 and near-zero DC, requiring lock-in detection.  _(class `C`)_
- **chain closes:** False — The live runner reproduces the phase-locked harmonic/nulled protocol, but the note does not close the bridge from that selected lock-in readout to an unqualified retained vector-sector observable; the current runner output also does not independently report the claimed matched scalar exposure table.
- **rationale:** Issue: the runner supports a phase-referenced first-harmonic handedness signal, but the retained claim depends on a selected lock-in phase/readout and on matched scalar exposure that is asserted in the note but not emitted as an audited runner check. Why this blocks: a nonzero 1H coefficient over the named orbit protocol is not by itself a retained vector-sector or magnetic-like force law, especially when the DC handedness averages to nearly zero and start-phase dependence is acknowledged. Repair target: add an audited observable theorem or acceptance harness that fixes the lock-in reference phase, reports/proves the scalar-exposure equality used to rule out scalar confounding, and states the family/parameter domain with tolerances. Claim boundary until fixed: safe to claim the current circular-orbit harness produces a bounded phase-locked 1H handedness signal with exact nulls, f-oddness, near-zero DC, and 3/3 family portability; not safe to claim a clean retained vector-sector physical observable beyond that protocol.
- **auditor confidence:** high

### `wave_3plus1d_promotions_note`

- **Note:** [`WAVE_3PLUS1D_PROMOTIONS_NOTE.md`](../../docs/WAVE_3PLUS1D_PROMOTIONS_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_conditional~~
- **effective_status:** ~~audited_conditional~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The note identifies the M branch as standard retarded (3+1)D wave evolution and the I branch as an instantaneous, c=infinity comparator stitched layer-by-layer from cached late-time static solves, then claims a 26-31% retarded-vs-instantaneous gap across three grown families.  _(class `C`)_
- **chain closes:** False — The live runner reproduces the finite lightcone and M-vs-I tables, but the literal instantaneous/c=infinity interpretation does not close: the I branch is a stitched finite-time frozen c=1 wave-solve comparator, not a derived elliptic Poisson or c->infinity solution.
- **rationale:** Issue: the runner supports the displayed finite computation, but the source labels the stitched frozen-source branch as an instantaneous c=infinity comparator without proving that this NL=30 late-time finite-c wave slice equals the instantaneous field. Why this blocks: a hostile physicist can accept first_dt=r for r=2..8 and a 26-31% difference between retarded moving-source evolution and the frozen-slice comparator, but cannot infer the literal retarded-vs-instantaneous wave claim or the all-three scalar-wave closure from this runner alone. Repair target: replace the I branch with an actual layerwise elliptic/Poisson instantaneous solve, or prove and numerically bound convergence of the frozen-wave late-time slice to the c->infinity comparator; then add hard assertions for the lightcone and gap gates and audit the Lane 8 radiation lane separately for the combined three-signature statement. Claim boundary until fixed: it is safe to claim a strict finite (3+1)D lattice lightcone to r=8 and a reproducible 26-31% gap between retarded moving-source wave evolution and this specific stitched frozen-source c=1 static-slice comparator on three grown families at v/c=0.23.
- **open / conditional deps cited:**
  - `instantaneous_c_infinity_comparator_not_derived_from_Poisson_or_c_limit`
  - `WAVE_3PLUS1D_RADIATION_NOTE.md_combined_three_signature_closure_not_audited_in_this_claim`
  - `runner_prints_thresholds_without_hard_assertions`
- **auditor confidence:** high

### `wave_amplification_near_horizon_note`

- **Note:** [`WAVE_AMPLIFICATION_NEAR_HORIZON_NOTE.md`](../../docs/WAVE_AMPLIFICATION_NEAR_HORIZON_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_clean~~
- **effective_status:** **retained**  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** On the retained exact-lattice harness, the oscillating-source/static-source ratio stays close to 1x, with largest ratio 1.012 at alpha = 0.50.  _(class `C`)_
- **chain closes:** True — The live runner reproduces every frozen alpha row and the best-ratio summary. The source note limits the conclusion to this exact-lattice absorber sweep and explicitly rejects the broader near-horizon amplification headline.
- **rationale:** The claim is not a broad physical amplification theorem; it is a bounded negative result on one exact-lattice replay. The runner computes the static and oscillating retarded-source deflections for the five stated absorber strengths and reproduces the frozen table, including the largest ratio of 1.012 at alpha = 0.50. Because the note keeps the conclusion within that harness and reports the raw denominator, the chain closes on its own terms.
- **auditor confidence:** high

### `wave_equation_self_field_note`

- **Note:** [`WAVE_EQUATION_SELF_FIELD_NOTE.md`](../../docs/WAVE_EQUATION_SELF_FIELD_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_conditional~~
- **effective_status:** ~~audited_conditional~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** Five independent observables (F~M, Born, gravity sign, null, finite-c retardation) all hold simultaneously on the same wave-equation field, making this the GR-style local field law promotion of the Poisson 3D result.  _(class `C`)_
- **chain closes:** False — The runner computes the stated finite wave-equation harness, but the wave equation, source law, and readout-to-field-law promotion are introduced as the model rather than derived from registered retained primitives.
- **rationale:** Issue: the note promotes an imposed discrete wave equation plus S=L(1-f) coupling to a retained local self-field law because several internal diagnostics pass. Why this blocks: the live runner does compute F~M near 0.998, TOWARD gravity on 3/3 families, a null at s=0, and exact first-arrival retardation, but it does not derive the PDE, source law, coupling, boundary conditions, or physical field observable from retained CL3 inputs; it also prints Born=4.01e-16 while the note/log freeze 1.08e-15, so the exact headline number is stale even though the machine-precision claim survives. Repair target: provide a retained theorem deriving the wave equation and source coupling from the framework primitives, register the static Poisson authority as a one-hop dependency, and add runner assertions comparing the static limit, Born residual tolerance, lightcone speed, and physical readout under derived boundary conditions. Claim boundary until fixed: it is safe to claim that this specific discrete wave-equation harness has a finite-c lightcone, exact null, TOWARD sign on the three tested families, F~M about 0.997-0.998, and machine-precision Born residual; it is not yet an audited retained GR-style self-field law or matter-closure field equation.
- **open / conditional deps cited:**
  - `wave_equation_and_source_coupling_not_derived_from_retained_primitives`
  - `3D_Poisson_static_result_not_registered_one_hop_dependency`
  - `physical_field_observable_bridge_not_registered`
  - `multi_source_superposition_and_backreaction_explicitly_untested`
  - `Born_residual_headline_stale_relative_to_live_runner`
- **auditor confidence:** high

### `wave_radiation_note`

- **Note:** [`WAVE_RADIATION_NOTE.md`](../../docs/WAVE_RADIATION_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_conditional~~
- **effective_status:** ~~audited_conditional~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The model's wave equation has true radiating solutions: an oscillating source emits a propagating field with the textbook 2+1D amplitude falloff, drive-frequency dominance, exact null, and preserved beam-side diagnostics.  _(class `C`)_
- **chain closes:** False — The live runner computes the finite scalar-wave radiation harness, but the promoted radiation law depends on an imposed 2+1D PDE, selected source/readout, finite-domain fit window, and the conditionally audited wave-equation self-field lane.
- **rationale:** Issue: the note promotes a finite oscillating-source scalar-wave computation to a retained radiation-law result for the model. Why this blocks: the runner reproduces the -0.469 log-log slope, frequency-peak dominance, exact S0=0 null, and family F~M table, but it starts from an imposed 2+1D wave equation and selected monopole drive, distance window, detector metric, and finite domain; it also relies on the Lane-5 lightcone result while its own sinusoidal first-arrival rows fail the strict dt=r check, and the live Born residual is 5.21e-16 rather than the note/log's 3.20e-15. Repair target: derive or register the scalar wave equation/source law and lightcone theorem as retained dependencies, add runner assertions with tolerances for slope, DFT peak dominance, null, Born, and finite-domain/reflection controls, and either prove the fit window is asymptotic or label it as a finite-window radiation proxy. Claim boundary until fixed: it is safe to claim that this specific 2+1D scalar-wave harness with S0=0.04, f in the tested range, NL=60, W=12 shows a reproducible finite-window amplitude slope near -0.5, drive-frequency-dominated detector time series, exact null, and machine-precision Born residual; it is not yet an audited retained framework-derived radiation law or GR/tensor radiation result.
- **open / conditional deps cited:**
  - `wave_equation_and_source_law_not_derived_from_retained_primitives`
  - `wave_equation_self_field_note_conditionally_audited_dependency`
  - `strict_lightcone_evidence_imported_from_Lane_5_not_registered_dependency`
  - `finite_domain_reflection_and_asymptotic_fit_window_not_proven`
  - `Born_residual_headline_stale_relative_to_live_runner`
- **auditor confidence:** high

### `wave_retardation_continuum_limit_note`

- **Note:** [`WAVE_RETARDATION_CONTINUUM_LIMIT_NOTE.md`](../../docs/WAVE_RETARDATION_CONTINUUM_LIMIT_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_conditional~~
- **effective_status:** ~~audited_conditional~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The note's bottom-line refinement table asserts that rel_MI = 28.81% -> 9.53% -> 43.40%, rel_MN = 25.60% -> 1.26% -> 31.24%, rel_MIeq = 74.11% -> 29.44% -> 23.16%, while dM drifts only 14% monotonically, so the magnitude is comparator-dominated rather than continuum-stable.  _(class `C`)_
- **chain closes:** False — The stated negative follows from the refinement/comparator numerics only if the unregistered harness and logs are accepted; the ledger provides no primary runner or runner output, and the exact discrete static comparator remains explicitly unresolved.
- **rationale:** Issue: the retained negative is load-bearing on a numerical H-refinement and three-comparator sweep, but the audit ledger registers no primary runner or runner output for wave_retardation_continuum_limit_note, and the note itself says the correct exact discrete static comparator is still the bottleneck. Why this blocks: without a registered deterministic computation, a hostile auditor cannot verify the rel_MI, rel_MN, rel_MIeq, rel_IeqN, dM-drift, integer-rounding, or corrected-radial-distance numbers; and without the exact static comparator theorem/solve, the broad statement about a continuum retardation magnitude is limited to the particular tested comparators. Repair target: register scripts/wave_retardation_continuum_limit.py as the primary runner, include deterministic output for the H=0.50/0.35/0.25 battery, make the runner assert the reported tables and corrected dN geometry, and add either a direct discrete static solve or an analytic discrete Green-function comparator for the implemented lattice operator. Claim boundary until fixed: it is safe to say that the source note reports a conditional negative for the tested cached-static, equilibrated-static, and imposed-Newton comparators, and that the reported tables would downgrade the Lane 6/8b magnitude if reproduced; it is not yet an audited retained continuum theorem about retardation magnitude, while fixed-H M != I existence and the separate dM stability observation remain only conditional on the unregistered computation.
- **open / conditional deps cited:**
  - `runner_not_registered_for_wave_retardation_continuum_limit_note`
  - `logs/2026-04-07-wave-retardation-continuum-limit.txt_not_registered_primary_output`
  - `exact_discrete_static_comparator_not_derived`
- **auditor confidence:** high

### `wave_retardation_lab_prediction_note`

- **Note:** [`WAVE_RETARDATION_LAB_PREDICTION_NOTE.md`](../../docs/WAVE_RETARDATION_LAB_PREDICTION_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_clean~~
- **effective_status:** **retained**  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** Two velocity sweeps show the M - I gap is configuration-dependent and non-monotonic in v/c, so no simple v/c power law supports a lab prediction card.  _(class `C`)_
- **chain closes:** True — The live runner reproduces the range-coupled sweep, the trajectory-fixed sweep, and the reported log-log slopes. The source note limits the conclusion to blocking the simple lab translation rather than proving or disproving the upstream wave-retardation lanes.
- **rationale:** The retained object is a negative guardrail: the easy lab-card extrapolation is blocked by the two computed sweeps. The runner output matches the frozen tables, including the range-coupled decrease to zero at v/c = 0.40, the trajectory-fixed non-monotonic gap with a minimum near v/c = 0.40, and the sign-flipped low-velocity row. This audit certifies only that bounded no-clean-v/c-scaling result; it does not independently certify the upstream Lane 4-8b physics mentioned as unaffected.
- **auditor confidence:** high

### `wave_retarded_gravity_note`

- **Note:** [`WAVE_RETARDED_GRAVITY_NOTE.md`](../../docs/WAVE_RETARDED_GRAVITY_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_conditional~~
- **effective_status:** ~~audited_conditional~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The retarded moving-source field and the layerwise instantaneous c=infinity comparator produce different beam deflections by 22-26% across the three grown families.  _(class `C`)_
- **chain closes:** False — The live runner verifies the finite M versus I comparison in the stated harness, but the claim inherits the imposed wave-equation/source-law setup and a selected single-velocity moving-source comparator that are not registered retained inputs.
- **rationale:** Issue: the note promotes a single-v/c moving-source comparison on an imposed wave-equation field to a retained dynamical retardation signature. Why this blocks: the runner reproduces M-I=-0.002785 for Fam1 and 22-26% relative differences across families, but it depends on the conditionally audited wave-equation self-field law, a hand-constructed layerwise instantaneous comparator, one translation speed v/c=0.30, one source trajectory, and no derived light-travel-time or angular-retardation theorem; the live Born residual is 3.59e-16 rather than the note/log's 2.22e-15, though still machine precision. Repair target: register and clean-audit the wave equation/source coupling, prove the c=infinity comparator construction and retarded-time observable, and extend the runner to multiple velocities/trajectories with assertions for the expected scaling, Born tolerance, null, and family portability. Claim boundary until fixed: it is safe to claim that, in this frozen NL=30, W=8, S=0.004, v/c=0.30 translation harness, retarded and instantaneous moving-source fields produce reproducibly different beam deflections with M<I across the three tested families; it is not yet an audited retained general retarded-gravity law.
- **open / conditional deps cited:**
  - `wave_equation_self_field_note_conditionally_audited_dependency`
  - `wave_equation_and_source_law_not_derived_from_retained_primitives`
  - `c_infinity_instantaneous_comparator_theorem_not_registered`
  - `single_velocity_and_single_translation_path_only`
  - `Born_residual_headline_stale_relative_to_live_runner`
- **auditor confidence:** high

### `wave_static_boundary_sensitivity_note`

- **Note:** [`WAVE_STATIC_BOUNDARY_SENSITIVITY_NOTE.md`](../../docs/WAVE_STATIC_BOUNDARY_SENSITIVITY_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_clean~~
- **effective_status:** **retained**  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** At shared H = 0.5, enlarging PW from 6.0 to 9.0 moves dS by 17.54% and rel_MS by 88.41%, so the direct static comparator is not boundary-stable within 5%.  _(class `C`)_
- **chain closes:** True — Running the named boundary-sensitivity runner at the source note's explicit H = 0.5 reproduces the frozen dM, dS, rel_MS, residual, and boundary-move values. The conclusion is limited to this off-center frozen-source boundary probe.
- **rationale:** The runner with the source-note parameters reproduces the table: dS moves by 17.54%, rel_MS by 88.41%, dM by 18.93%, and the static residual remains near 2e-10. Because the note explicitly frames this as a narrow boundary diagnostic and does not promote the direct static comparator, the negative boundary-stability result closes on its own terms. The audit does not certify any continuum limit or boundary-stable baseline beyond this H = 0.5, PW = 6 to 9 comparison.
- **auditor confidence:** high

### `wave_static_direct_probe_fine_note`

- **Note:** [`WAVE_STATIC_DIRECT_PROBE_FINE_NOTE.md`](../../docs/WAVE_STATIC_DIRECT_PROBE_FINE_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_clean~~
- **effective_status:** **retained**  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** At the moving-source fine point H = 0.25, the direct static comparator has rel_MS = 37.62%, worse than the equilibrated cached-static comparator rel_MIeq = 23.16%.  _(class `C`)_
- **chain closes:** True — The live fine-point runner reproduces the frozen dM, dI, dIeq, dS, relative-gap values, and 2e-10 static residual. The note limits the claim to this H = 0.25 moving-source point and does not claim the exact-comparator lane is fully closed.
- **rationale:** The source note is a narrow negative, not a broad demotion of the exact comparator lane. The fine-point runner exactly reproduces the stated values and shows that dS does not beat dIeq at H = 0.25 on the moving-source setup. Because the note preserves the frozen-source positive and boundary-tests as separate questions, this bounded fine-point negative closes on its own terms.
- **auditor confidence:** high

### `wave_static_fixed_beam_boundary_sensitivity_note`

- **Note:** [`WAVE_STATIC_FIXED_BEAM_BOUNDARY_SENSITIVITY_NOTE.md`](../../docs/WAVE_STATIC_FIXED_BEAM_BOUNDARY_SENSITIVITY_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_clean~~
- **effective_status:** **retained**  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** With the beam DAG fixed, enlarging only the field/static solve box still moves dS and rel_MS materially at H = 0.5 and H = 0.35.  _(class `C`)_
- **chain closes:** True — The live runner reproduces both retained H tables and their field-box move summaries. The note limits the conclusion to this fixed-beam boundary diagnostic and does not claim a continuum limit.
- **rationale:** The fixed-beam replay verifies the key control: the beam geometry is held at the baseline box while the field/static solve box is enlarged and cropped back. At H = 0.5 the runner reproduces dS move 30.29% and rel_MS move 83.88%; at H = 0.35 it reproduces dS move 26.21% and rel_MS move 46.52%, while dM is much less sensitive. This cleanly supports the note's bounded negative that the earlier boundary sensitivity was not merely a beam-geometry confound.
- **auditor confidence:** high

### `wave_static_matrixfree_fixed_beam_boundary_note`

- **Note:** [`WAVE_STATIC_MATRIXFREE_FIXED_BEAM_BOUNDARY_NOTE.md`](../../docs/WAVE_STATIC_MATRIXFREE_FIXED_BEAM_BOUNDARY_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_clean~~
- **effective_status:** **retained**  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** At shared H = 0.35 with fixed beam PW = 6.0, the matrix-free static comparator still shows material field-box sensitivity: dS moves 26.21% and rel_MS moves 46.52%.  _(class `C`)_
- **chain closes:** True — The live matrix-free runner with the source note's retained H = 0.35 reproduces the field-box table, residuals, iteration counts, and boundary-move summary. The note explicitly does not establish the H = 0.25 run.
- **rationale:** The audited result is a side-probe agreement, not a new continuum claim. The matrix-free engine reproduces the same fixed-beam boundary sensitivity as the direct-solve branch at H = 0.35: dS and rel_MS move materially while dM moves only 0.57%, and both matrix-free solves converge to residuals below 3e-10. This closes the note's narrow claim that the static-comparator weakness is not caused by the direct static solver implementation.
- **auditor confidence:** high

### `wave_static_matrixfree_moving_source_fixed_beam_boundary_note`

- **Note:** [`WAVE_STATIC_MATRIXFREE_MOVING_SOURCE_FIXED_BEAM_BOUNDARY_NOTE.md`](../../docs/WAVE_STATIC_MATRIXFREE_MOVING_SOURCE_FIXED_BEAM_BOUNDARY_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_clean~~
- **effective_status:** **retained**  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** At H = 0.35 with fixed beam geometry, the moving-source exact static comparator remains field-box sensitive, but the 9.0 -> 12.0 large-box branch shows low rel_MS and smaller dS movement without meeting the strict stability bar.  _(class `C`)_
- **chain closes:** True — The live runner reproduces both source-note comparisons: field PW 6.0 -> 9.0 and 9.0 -> 12.0. The note keeps the conclusion mixed and bounded, explicitly withholding continuum-quality promotion.
- **rationale:** The note accurately preserves both sides of the runner output. The 6.0 -> 9.0 comparison is still materially box-dependent, with dS move 20.84% and rel_MS move 86.21%, while dM is stable; the 9.0 -> 12.0 comparison improves to dS move 5.52% and rel_MS 3.18% -> 2.42% but still does not pass a strict stability criterion. This closes only the stated mixed diagnostic: no boundary-stable moving-source comparator is retained yet, but the medium-H large-box branch remains a plausible stabilization candidate.
- **auditor confidence:** high

### `wave_static_matrixfree_shared_geometry_compare_note`

- **Note:** [`WAVE_STATIC_MATRIXFREE_SHARED_GEOMETRY_COMPARE_NOTE.md`](../../docs/WAVE_STATIC_MATRIXFREE_SHARED_GEOMETRY_COMPARE_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_conditional~~
- **effective_status:** ~~audited_conditional~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** At H = 0.35 and H = 0.25, the direct and matrix-free static solvers agree extremely closely, so matrix-free is a strong drop-in replacement on the shared geometries tested.  _(class `C`)_
- **chain closes:** False — The live runner reproduces the two numerical comparison tables, but it does not define or pass a drop-in-replacement acceptance criterion; its own printed verdict says the matrix-free result is close but not yet proven identical.
- **rationale:** Issue: the note promotes the matrix-free solver as a strong drop-in replacement, but the runner only demonstrates small finite mismatches at two geometries and explicitly reports that identity is not proven. Why this blocks: without a stated tolerance or convergence/equivalence theorem, the audit can certify numerical closeness but cannot certify replacement status as a retained engine equivalence. Repair target: add an audited acceptance criterion for drop-in replacement, such as field and propagated-response tolerances tied to solver residuals, or prove both algorithms converge to the same finite-grid Poisson solution with a runner pass/fail threshold. Claim boundary until fixed: safe to claim that at H = 0.35 and H = 0.25 the direct and matrix-free fields agree to roughly 1e-5 relative field mismatch and propagated dS agrees to roughly 1e-6; not safe to claim unconditional retained drop-in replacement beyond those numerical tests.
- **auditor confidence:** high

### `wave_static_single_source_compare_note`

- **Note:** [`WAVE_STATIC_SINGLE_SOURCE_COMPARE_NOTE.md`](../../docs/WAVE_STATIC_SINGLE_SOURCE_COMPARE_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_clean~~
- **effective_status:** **retained**  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** At coarse H = 0.5, frozen-source comparator quality is source-position dependent: off-center z_phys = 3.0 already shows poor cached comparator agreement while on-axis z_phys = 0.0 is much better for dIeq.  _(class `C`)_
- **chain closes:** True — The live runner reproduces both retained frozen-source tables, including all comparator shifts, relative mismatches, and static residuals. The note scopes the result as a smoke test rather than a continuum or all-source-position claim.
- **rationale:** The runner supports the note's narrow diagnostic. For z_phys = 3.0, dS tracks dM closely while cached and Newton-style comparators are poor; for z_phys = 0.0, dIeq nearly matches dM while dN remains poor. This cleanly supports the bounded conclusion that the mismatch is not purely a moving-source artifact and that comparator quality depends on source position.
- **auditor confidence:** high

### `weak_coupling_retention_note_2026-04-11`

- **Note:** [`WEAK_COUPLING_RETENTION_NOTE_2026-04-11.md`](../../docs/WEAK_COUPLING_RETENTION_NOTE_2026-04-11.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_conditional~~
- **effective_status:** ~~audited_conditional~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** At weak coupling (G=5,10), attractive parity coupling produces a uniformly larger shell-force TOWARD count than repulsive parity coupling across the audited irregular graph surface (60/60 runs), with a minimum separation of 10/40 steps and exact norm conservation.  _(class `C`)_
- **chain closes:** False — The live runner supports the finite shell-margin and norm claims, but the registered runner path is stale and the retained wording still depends on a finite selected graph/seed/coupling surface and graph-native shell-force proxy rather than a theorem for admissible irregular graphs.
- **rationale:** Issue: the finite runner verifies shell ordered 60/60, shell margin >=10 on 60/60, and norm conservation 60/60, but the note promotes this selected audit surface to a retained weak-coupling sign-sensitive regime while the registered runner path is wrong and the secondary gap count is live-stale at 54/60. Why this blocks: a hostile auditor can accept the finite shell-margin table but cannot infer a theorem for admissible irregular bipartite graphs, a coordinate-force closure, or a stable secondary spectral-gap row from the current packet. Repair target: fix the registered runner path, add explicit runner assertions for the retained shell-margin/norm gates, archive deterministic output, and derive or register an admissible-graph/shell-force theorem explaining why the selected families, seeds, G values, and threshold margin define a retained regime rather than a finite audit panel. Claim boundary until fixed: it is safe to claim that on the frozen 60-run surface (three graph families, two sizes, seeds 42-46, G=5 and 10), attractive parity coupling has larger TOWARD shell count than repulsive coupling with margin >=10/40 in every run and exact norm conservation; width and spectral-gap observables remain supporting only.
- **open / conditional deps cited:**
  - `frontier_weak_coupling_retained.py_registered_runner_path_missing_expected_scripts_prefix`
  - `finite_graph_seed_coupling_surface_no_admissible_graph_theorem`
  - `shell_force_proxy_to_coordinate_force_or_gravity_closure_not_derived`
  - `spectral_gap_secondary_count_live_stale_relative_to_note`
- **auditor confidence:** high

### `wide_lattice_h2t_distance_law_note`

- **Note:** [`WIDE_LATTICE_H2T_DISTANCE_LAW_NOTE.md`](../../docs/WIDE_LATTICE_H2T_DISTANCE_LAW_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_clean~~
- **effective_status:** **retained**  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The independent wide-lattice replay at h = 0.25, W = 12, L = 12 gives 10/10 TOWARD distance support, far-tail b^(-1.05) with R^2 = 0.990, and F~M exponent 1.000.  _(class `C`)_
- **chain closes:** True — The live replay reproduces the frozen sanity checks, distance rows, peak/far-tail fits, and mass-scaling sweep. The note explicitly limits the result to a finite-lattice frontier replay and disclaims a continuum theorem or exact exponent proof.
- **rationale:** The runner supports the retained frontier claim as scoped. It independently computes the wide ordered-3D h^2+T replay on main and reproduces Born approximately 4.82e-15, k=0 zero, 10/10 attractive distance rows, peak-tail exponent -0.95, far-tail exponent -1.05, and linear F~M scaling. This audit certifies only that finite-lattice replay, not an exact Newtonian exponent or continuum-limit theorem.
- **auditor confidence:** high

### `work_history.repo.review_feedback.architecture_portability_audit_2026-04-11`

- **Note:** [`work_history/repo/review_feedback/ARCHITECTURE_PORTABILITY_AUDIT_2026-04-11.md`](../../docs/work_history/repo/review_feedback/ARCHITECTURE_PORTABILITY_AUDIT_2026-04-11.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_failed~~
- **effective_status:** ~~audited_failed~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** It demonstrates architecture portability of source-mass scaling and attraction sign across ordered 3D cubic, staggered 3D cubic, Wilson 3D cubic, and a 2D random geometric control row.  _(class `B`)_
- **chain closes:** False — The note gives proposed safe wording, but no runner, data table, artifact chain, or registered one-hop dependencies proving the cross-architecture comparisons.
- **rationale:** Issue: the positive architecture-portability claim is asserted without any checkable source-note computation, runner output, table, or registered dependency. Why this blocks: a hostile auditor cannot verify source-mass scaling, attraction sign, Born-rule exclusions, or architecture-specific boundaries across the ordered, staggered, Wilson, and random-geometric rows from this packet. Repair target: provide or register the underlying architecture-portability note, scripts/logs, per-architecture measurements, and explicit wording-boundary checks. Claim boundary until fixed: this file can be used only as an editorial wording caution that should not overclaim Newton closure, distance-law closure, both-masses closure, or Wilson Born measurements; it cannot itself be retained as evidence for architecture portability.
- **open / conditional deps cited:**
  - `ordered_3D_cubic_source_mass_scaling_and_attraction_artifact_not_registered`
  - `staggered_3D_cubic_source_mass_scaling_and_attraction_artifact_not_registered`
  - `Wilson_3D_cubic_source_mass_scaling_and_attraction_artifact_not_registered`
  - `2D_random_geometric_control_row_artifact_not_registered`
- **auditor confidence:** high

### `yt_class_6_c3_breaking_operator_note_2026-04-18`

- **Note:** [`YT_CLASS_6_C3_BREAKING_OPERATOR_NOTE_2026-04-18.md`](../../docs/YT_CLASS_6_C3_BREAKING_OPERATOR_NOTE_2026-04-18.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_conditional~~
- **effective_status:** ~~audited_conditional~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** No retained C3-breaking operator on H_hw=1 produces generation-asymmetric position-basis content, while the C3-commuting circulant family gives distinct Fourier-basis eigenvalues but still needs A1 equipartition and P1 sqrt(m) identification for the hierarchy claim.  _(class `A`)_
- **chain closes:** False — The runner passes all 43 algebraic/comparator checks, but the note imports support/conditional one-hop authorities and its amended positive mechanism explicitly depends on two non-retained ingredients. The narrow algebraic no-go is supported; the retained positive generation-hierarchy mechanism does not fully close on the current retained surface.
- **rationale:** Issue: the note's refined outcome combines a runner-supported narrow C3-breaking no-go with a positive circulant-spectrum mechanism that the source itself marks conditional on non-retained A1 equipartition and P1 sqrt(m) identification, while multiple cited authorities remain support or conditional. Why this blocks: a passed M3(C)/commutant/circulant algebra runner cannot promote the full hierarchy mechanism to retained when its physical inputs and several upstream surfaces are not retained. Repair target: audit/promote the one-hop foundation notes used as retained authorities, and add retained derivations or acceptance runners for A1 equipartition, P1 sqrt(m), and the delta/unit bridge used by the Koide circulant branch. Claim boundary until fixed: safe to claim the 43/43 runner supports the narrow operator-algebra no-go and the existence of distinct Fourier-basis circulant eigenvalues; not safe to claim a clean retained generation-hierarchy mechanism or a fully retained C3-breaking-class closure beyond those conditional inputs.
- **open / conditional deps cited:**
  - `THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md`
  - `THREE_GENERATION_STRUCTURE_NOTE.md`
  - `S3_TASTE_CUBE_DECOMPOSITION_NOTE.md`
  - `Z2_HW1_MASS_MATRIX_PARAMETRIZATION_NOTE.md`
  - `SITE_PHASE_CUBE_SHIFT_INTERTWINER_NOTE.md`
  - `NATIVE_GAUGE_CLOSURE_NOTE.md`
  - `KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md`
- **auditor confidence:** high

### `yt_ew_color_projection_theorem`

- **Note:** [`YT_EW_COLOR_PROJECTION_THEOREM.md`](../../docs/YT_EW_COLOR_PROJECTION_THEOREM.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_conditional~~
- **effective_status:** ~~audited_conditional~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** Identify the physical EW coupling readout with the connected color trace so that alpha_EW(phys)/alpha_EW(lattice)=1/R_conn=N_c^2/(N_c^2-1)=9/8, using R_conn leading-order 1/N_c support and MC agreement as validation.  _(class `B`)_
- **chain closes:** False — The MC runner validates the sibling R_conn observable, not the physical EW-current matching rule. The one-hop OZI note explicitly states that the exact coefficient identification with 1/R_conn remains an additional package assumption, and the R_conn dependency is leading-order 1/N_c with bounded corrections rather than an exact theorem.
- **rationale:** Issue: the theorem promotes a universal package-level 9/8 EW coupling correction from R_conn, but the one-hop matching dependency only supplies bounded large-N_c/OZI support and explicitly does not prove the exact coefficient equality; the runner measures R_conn=0.888337 +/- 0.001896, not the continuum EW current matching factor. Why this blocks: agreement of the sibling connected-trace observable with 8/9 does not prove that the physical EW vacuum polarization must read exactly the connected trace rather than the full trace plus a nonzero disconnected coefficient, and the dependency graph is circular between this note, RCONN_DERIVED_NOTE, and the OZI support note. Repair target: derive the EW current matching rule directly from the lattice-to-continuum path-integral/current normalization, or add a dedicated runner computing Pi_EW^phys/Pi_EW^lattice including the disconnected topology and its coefficient; also break and clean the circular Rconn/OZI dependencies. Claim boundary until fixed: safe to claim leading-order R_conn=8/9+O(1/N_c^4) with MC support and that a universal 9/8 factor would preserve sin^2(theta_W); not safe to claim the retained physical EW couplings are independently derived by an exact 9/8 color-projection theorem.
- **open / conditional deps cited:**
  - `RCONN_DERIVED_NOTE.md`
  - `EW_CURRENT_MATCHING_OZI_SUPPRESSION_THEOREM_NOTE_2026-04-27.md`
  - `circular dependency: yt_ew_color_projection_theorem <-> rconn_derived_note <-> ew_current_matching_ozi_suppression_theorem_note_2026-04-27`
  - `missing direct EW-current matching coefficient computation`
- **auditor confidence:** 0.94

### `yt_ew_delta_r_retention_analysis_note_2026-04-18`

- **Note:** [`YT_EW_DELTA_R_RETENTION_ANALYSIS_NOTE_2026-04-18.md`](../../docs/YT_EW_DELTA_R_RETENTION_ANALYSIS_NOTE_2026-04-18.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_conditional~~
- **effective_status:** ~~audited_conditional~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The note preserves the EW lane's retained-quantitative status by applying the YT P1 Rep-A/Rep-B three-channel method to absolute electroweak gauge couplings, using Ward Z1=Z2 structure plus literature-analog BZ integrals to compute Delta_R(g2)=-2.863% and Delta_R(g1)=-0.713%, then interpreting those values as uncertainty bands around the packaged EW outputs whose PDG deviations are inside the bands rather than as additional shifts.  _(class `D`)_
- **chain closes:** False — The runner passes 69 checks and reproduces the arithmetic for the stated EW matching-band analysis, including SU(2)/U(1) factors, alpha_i(v), literature-analog channel constants, Delta_R(g2), Delta_R(g1), propagated bands, and PDG containment. The proof chain does not close because the load-bearing inputs are not registered as clean one-hop authorities: the EW color projection/zero-import chain, Rep-A/Rep-B methodology, Ward absolute-coupling matching formula and sign convention, EW-sector BZ integrals, matching-scale choice, and the 'packaged values already include matching' no-double-counting premise. The note also contains unresolved internal numerical inconsistencies, especially sin^2(theta_W) uncertainty appearing as about 0.0038 in the checked propagation but about 0.0005/0.0006 in other text/output, and an obsolete safe-boundary pair of Delta_R values inconsistent with the runner centrals.
- **rationale:** The computation is a valid arithmetic audit of the note's own model: with the supplied Casimirs, hypercharge sum, packaged couplings, literature BZ analogs I_SE^{gg}=2 and I_SE^{ff}=0.7, and the runner's Ward-absolute-coupling formula, the stated central values Delta_R(g2)=-2.863% and Delta_R(g1)=-0.713% and the broad retained bands follow. What blocks a retained theorem-grade claim is that those BZ integrals are not framework-native EW quadratures, the Ward/sign/scale prescription is argued in prose rather than registered as an audited input, the upstream EW package and YT P1 dependencies are unregistered in the audit row, and the use of PDG observed values makes the lane-status survival check an external comparator test. Most importantly, the note's survival conclusion requires treating Delta_R^{EW} as an uncertainty on already-matched packaged values; if the same Delta_R is applied as a shift, the note itself finds a large sin^2(theta_W) tension. Repair requires registering and auditing the upstream EW color-projection and zero-import authorities, deriving the absolute-gauge Ward matching/sign convention on the CL3 lattice, running framework-native EW-sector BZ quadrature for the relevant vertex/self-energy integrals with a documented matching scale, and proving whether the packaged g_i(v) already include that matching. The text/runner must also reconcile the sin^2(theta_W) uncertainty (0.0038 versus 0.0005/0.0006) and remove the inconsistent older Delta_R safe-boundary numbers. What can still be safely claimed is conditional: given the note's formulae and literature analog inputs, the runner arithmetic yields percent-level EW matching bands that contain the listed PDG deviations; this is not an audited sub-percent EW precision theorem and not a framework-native computation of Delta_R^{EW}.
- **open / conditional deps cited:**
  - `YT_EW_COLOR_PROJECTION_THEOREM.md_not_registered_one_hop_dependency_and_prior_audited_conditional`
  - `RCONN_DERIVED_NOTE.md_not_registered_one_hop_dependency`
  - `YT_ZERO_IMPORT_CHAIN_NOTE.md_not_registered_one_hop_dependency`
  - `YT_P1_REP_A_REP_B_CANCELLATION_THEOREM_NOTE_2026-04-17.md_not_registered_one_hop_dependency`
  - `YT_P1_DELTA_R_MASTER_ASSEMBLY_THEOREM_NOTE_2026-04-18.md_not_registered_one_hop_dependency`
  - `YT_P1_BZ_QUADRATURE_FULL_STAGGERED_PT_NOTE_2026-04-18.md_not_registered_or_audited_conditional`
  - `scripts/canonical_plaquette_surface.py_not_registered_one_hop_dependency`
  - `EW_sector_vertex_and_self_energy_BZ_integrals_not_framework_native_computed`
  - `Ward_Z1_equals_Z2_absolute_gauge_matching_formula_and_sign_convention_not_registered_as_CL3_theorem`
  - `matching_scale_choice_alpha_i_v_vs_alpha_LM_not_closed`
  - `packaged_EW_values_already_MSbar_matched_no_double_counting_premise_not_registered`
  - `PDG_observed_g1_g2_sin2thetaW_alphaEM_comparators_external_inputs`
  - `internal_sin2thetaW_uncertainty_inconsistency_0_0038_vs_0_0005_or_0_0006`
  - `obsolete_safe_boundary_Delta_R_values_minus_0_45_percent_and_minus_0_25_percent_inconsistent_with_runner`
- **auditor confidence:** high

### `yt_generation_hierarchy_primitive_analysis_note_2026-04-18`

- **Note:** [`YT_GENERATION_HIERARCHY_PRIMITIVE_ANALYSIS_NOTE_2026-04-18.md`](../../docs/YT_GENERATION_HIERARCHY_PRIMITIVE_ANALYSIS_NOTE_2026-04-18.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_conditional~~
- **effective_status:** ~~audited_conditional~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The retained surface gives a narrow position-basis no-go for generation-asymmetric diagonal content, while the amended positive Fourier-basis circulant spectrum still requires non-retained A1 equipartition and P1 sqrt(m) identification for the hierarchy claim.  _(class `A`)_
- **chain closes:** False — The runner passes all 51 checks, but the note imports support/conditional/unknown one-hop authorities and explicitly leaves A1 and P1 non-retained. The narrow algebraic no-go and Fourier-spectrum correction close as computations; the retained generation-hierarchy primitive does not close on the current retained surface.
- **rationale:** Issue: the refined note combines a passed narrow position-basis no-go with a positive circulant-spectrum mechanism whose physical hierarchy bridge depends on non-retained A1 equipartition, P1 sqrt(m) identification, and multiple one-hop authorities that are support, conditional, or unknown. Why this blocks: the runner establishes algebraic facts and comparator failures, but it does not derive the missing hierarchy primitives or promote the imported foundation stack. Repair target: split the retained algebraic no-go from the candidate extension, audit/promote the one-hop authorities, and add retained derivations or pass/fail runners for A1, P1, the overall scale, and the delta/unit bridge. Claim boundary until fixed: safe to claim the 51/51 runner supports the position-basis no-go, the failure of the tested retained-surface candidates, and the existence of distinct Fourier-basis circulant eigenvalues; not safe to claim a clean retained generation-hierarchy primitive or a retained Koide/fermion-mass mechanism beyond those conditional inputs.
- **open / conditional deps cited:**
  - `THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md`
  - `THREE_GENERATION_STRUCTURE_NOTE.md`
  - `S3_TASTE_CUBE_DECOMPOSITION_NOTE.md`
  - `SITE_PHASE_CUBE_SHIFT_INTERTWINER_NOTE.md`
  - `Z2_HW1_MASS_MATRIX_PARAMETRIZATION_NOTE.md`
  - `YT_WARD_IDENTITY_DERIVATION_THEOREM.md`
  - `YT_BOTTOM_YUKAWA_RETENTION_ANALYSIS_NOTE_2026-04-18.md`
  - `CHARGED_LEPTON_MASS_HIERARCHY_REVIEW_NOTE_2026-04-17.md`
  - `STRUCTURAL_NO_GO_SURVEY_NOTE.md`
  - `KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md`
- **auditor confidence:** high

### `yt_h_unit_flavor_column_decomposition_note_2026-04-18`

- **Note:** [`YT_H_UNIT_FLAVOR_COLUMN_DECOMPOSITION_NOTE_2026-04-18.md`](../../docs/YT_H_UNIT_FLAVOR_COLUMN_DECOMPOSITION_NOTE_2026-04-18.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_conditional~~
- **effective_status:** ~~audited_conditional~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** Flavor-column decompositions of H_unit fail because up/down sub-block projectors are impure (1,1)+(3,1) mixtures with Z^2 = 3 != 6, generation-indexed projectors remain uniform with Z^2 = 6, and SU(2)_L forbids (1,1)-(3,1) mixing at M_Pl.  _(class `A`)_
- **chain closes:** False — The live runner passes all 79 checks for the class #1 no-go, but the result imports Ward/D17, b-quark, gauge, and generation authorities whose current ledger statuses are support, conditional, or unknown. The no-go is therefore supported as a conditional retention analysis rather than a clean retained theorem.
- **rationale:** Issue: the runner-supported class #1 no-go depends on D17/Block 6 Ward uniqueness, the b-quark Outcome A setup, exact SU(2)_L/gauge inputs, and three-generation inputs that are not all retained in the current audit ledger. Why this blocks: an algebraic decomposition of P_up/P_down can close only relative to those imported authority surfaces; if D17, N_iso/N_c, or the b-quark setup remains support/conditional/unknown, the retained no-go cannot propagate cleanly. Repair target: audit/promote the Ward-identity theorem, bottom-Yukawa retention analysis, native gauge closure, one-generation/three-generation inputs, and Z2/site-phase companion notes, or rewrite this note as a strictly conditional class #1 exclusion over named assumptions. Claim boundary until fixed: safe to claim the 79/79 runner shows H_unit flavor-column decomposition is excluded under the stated Ward/D17 and SU(2)_L assumptions; not safe to claim an unconditional retained no-go for class #1 on the fully retained surface.
- **open / conditional deps cited:**
  - `YT_WARD_IDENTITY_DERIVATION_THEOREM.md`
  - `YT_BOTTOM_YUKAWA_RETENTION_ANALYSIS_NOTE_2026-04-18.md`
  - `THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md`
  - `ONE_GENERATION_MATTER_CLOSURE_NOTE.md`
  - `Z2_HW1_MASS_MATRIX_PARAMETRIZATION_NOTE.md`
  - `SITE_PHASE_CUBE_SHIFT_INTERTWINER_NOTE.md`
  - `NATIVE_GAUGE_CLOSURE_NOTE.md`
- **auditor confidence:** high

### `yt_p1_bz_quadrature_full_staggered_pt_note_2026-04-18`

- **Note:** [`YT_P1_BZ_QUADRATURE_FULL_STAGGERED_PT_NOTE_2026-04-18.md`](../../docs/YT_P1_BZ_QUADRATURE_FULL_STAGGERED_PT_NOTE_2026-04-18.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_conditional~~
- **effective_status:** ~~audited_conditional~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The full Kawamoto-Smit staggered-PT 4D BZ quadrature with MSbar subtraction yields Delta_R = -3.77% +/- 0.45% and moves Delta_R from literature-cited status to framework-native retained status with sub-half-percent precision.  _(class `C`)_
- **chain closes:** False — The runner recomputes the N=32/48/64 quadrature and assembles the stated number, but the registered audit row has no one-hop dependencies for the retained Feynman rules, canonical surface, MSbar subtraction, taste normalizations, prior brackets, or 5% systematic model. Those premises are imported or hard-coded rather than closed inside the audit packet.
- **rationale:** Issue: the retained-status upgrade from a full staggered-PT quadrature rests on unregistered upstream authorities and physical-normalization choices: the Ward identity, Rep-A/Rep-B three-channel formula, H_unit Feynman rules, Delta_1/Delta_2/Delta_3 ranges, prior schematic and master Delta_R notes, canonical plaquette constants, MSbar subtraction prescription, N_TASTE normalization, and the asserted 5% full-PT systematic are all used but the ledger row lists no one-hop dependencies. Why this blocks: the runner verifies the quadrature arithmetic once those rules and constants are supplied, but it does not derive the Kawamoto-Smit/taste-normalized integrands from retained CL3 primitives, prove the continuum-subtraction prescription, justify the n_f=6 matching surface, or substantiate the 5% systematic/covariance model; it also compares to prior/literature brackets that are absent from the audit packet. Repair target: register the cited notes and canonical-surface script as one-hop dependencies, add or cite a retained theorem deriving the full staggered Feynman rules, MSbar subtraction, taste averaging, and systematic budget, and update the runner to fail if those dependencies or uncertainty inputs change rather than hard-coding them. Claim boundary until fixed: it is safe to claim a reproducible conditional quadrature calculation which, given the supplied staggered-PT rules, canonical constants, and 5% per-channel systematic, produces I_v_scalar=3.902, I_v_gauge=0, I_SE_gluonic=2.323, I_SE_fermion=0.996, and Delta_R=-3.769% +/-0.452%; it is not yet an audited retained first-principles framework-native precision theorem.
- **open / conditional deps cited:**
  - `YT_P1_BZ_QUADRATURE_NUMERICAL_NOTE_2026-04-18.md_not_registered_one_hop_dependency`
  - `YT_P1_DELTA_R_MASTER_ASSEMBLY_THEOREM_NOTE_2026-04-18.md_not_registered_one_hop_dependency`
  - `YT_WARD_IDENTITY_DERIVATION_THEOREM.md_not_registered_one_hop_dependency`
  - `YT_P1_REP_A_REP_B_CANCELLATION_THEOREM_NOTE_2026-04-17.md_not_registered_one_hop_dependency`
  - `YT_P1_H_UNIT_RENORMALIZATION_FRAMEWORK_NATIVE_NOTE_2026-04-17.md_not_registered_one_hop_dependency`
  - `YT_P1_DELTA_1_BZ_COMPUTATION_NOTE_2026-04-17.md_not_registered_one_hop_dependency`
  - `YT_P1_DELTA_2_BZ_COMPUTATION_NOTE_2026-04-17.md_not_registered_one_hop_dependency`
  - `YT_P1_DELTA_3_BZ_COMPUTATION_NOTE_2026-04-17.md_not_registered_one_hop_dependency`
  - `scripts/canonical_plaquette_surface.py_not_registered_one_hop_dependency`
  - `MSbar_continuum_subtraction_and_N_TASTE_normalization_theorem_not_registered`
  - `five_percent_full_PT_systematic_model_not_registered`
- **auditor confidence:** high

### `yt_p1_bz_quadrature_numerical_note_2026-04-18`

- **Note:** [`YT_P1_BZ_QUADRATURE_NUMERICAL_NOTE_2026-04-18.md`](../../docs/YT_P1_BZ_QUADRATURE_NUMERICAL_NOTE_2026-04-18.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_conditional~~
- **effective_status:** ~~audited_conditional~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** At N = 48 offset-grid, the schematic 4D BZ quadrature yields I_v_scalar = 3.965765, I_v_gauge = 0, I_SE_gluonic = 2.321326, I_SE_fermion = 1.118792 and assembles these into Delta_R = -3.287% +/- 2.312% with a tightened [-5.60%, -0.97%] bracket.  _(class `C`)_
- **chain closes:** False — The runner reproduces the stated schematic quadrature and algebraic Delta_R assembly, but the source explicitly does not implement the full staggered taste-diagonal Dirac-trace lattice-PT algebra. The retained/full-P1 inference also rests on one-hop authorities that are support, conditional, or still unaudited proposed parents.
- **rationale:** Issue: the live runner evaluates a schematic 4D BZ quadrature and the source explicitly says the full staggered taste/Dirac-trace lattice-PT algebra is not implemented, while cited Ward/bridge authorities are not clean retained and the three-channel parent stack remains unaudited proposed input. Why this blocks: a schematic central value with a 25% assigned systematic can support a bounded numerical estimate, but it cannot promote a retained full lattice-PT correction or replace the prior P1 bracket as a theorem. Repair target: implement the full staggered-PT quadrature with taste matrices, Dirac traces, scheme-matched continuum subtraction/counterterms, and audited clean or retained status for the Rep-A/Rep-B, H_unit, and Delta_1/Delta_2/Delta_3 parent notes. Claim boundary until fixed: safe to claim the current runner gives an N=48 schematic BZ quadrature estimate I_v_scalar=3.966, I_v_gauge≈0, I_SE_gluonic=2.321, I_SE_fermion=1.119 and Delta_R=-3.287% +/- 2.312% under its stated schematic assumptions; not safe to claim a clean retained full lattice-PT P1 value beyond those assumptions.
- **open / conditional deps cited:**
  - `YT_WARD_IDENTITY_DERIVATION_THEOREM.md`
  - `UV_GAUGE_TO_YUKAWA_BRIDGE_SC_VS_PERT_NOTE.md`
- **auditor confidence:** high

### `yt_p1_color_factor_retention_note_2026-04-17`

- **Note:** [`YT_P1_COLOR_FACTOR_RETENTION_NOTE_2026-04-17.md`](../../docs/YT_P1_COLOR_FACTOR_RETENTION_NOTE_2026-04-17.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_conditional~~
- **effective_status:** ~~audited_conditional~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The three-channel decomposition is the unique assembly of the Rep-A/Rep-B one-loop diagrammatic catalog after exact cancellation of the external quark Z_psi term.  _(class `B`)_
- **chain closes:** False — The runner exactly checks the algebra after the Rep-A and Rep-B formulas are supplied, but it does not derive the diagrammatic catalog, the equal external-leg term, or the SU(3)/n_f inputs. The ledger row has no registered one-hop deps, so the upstream catalog status cannot propagate into this retained claim.
- **rationale:** Issue: the retained three-channel color decomposition depends on the Rep-A/Rep-B one-loop diagrammatic catalog and exact 2 C_F I_leg cancellation, but this audit row has no registered dependencies and the runner hard-codes the Rep-A and Rep-B formulae before checking the subtraction. Why this blocks: the algebraic residual being zero proves only that the claimed assembly follows from the supplied catalog; it does not prove that the catalog, H_unit/scalar-bilinear normalization, flavor count, or external-leg equality are retained framework-native inputs. Repair target: register and close the Rep-A/Rep-B cancellation theorem and SU(3)/n_f authorities as one-hop dependencies, or extend the runner to enumerate the one-loop diagrams and derive the channel coefficients and Z_psi cancellation from the framework Feynman rules. Claim boundary until fixed: safe to claim that, given the stated Rep-A/Rep-B formulas plus C_F=4/3, C_A=3, T_F=1/2, and n_f=6, the three-channel assembly and external-leg cancellation are exact; not safe to claim an independently retained framework-native P1 color-factor decomposition.
- **open / conditional deps cited:**
  - `YT_P1_REP_A_REP_B_CANCELLATION_THEOREM_NOTE_2026-04-17.md`
  - `YT_EW_COLOR_PROJECTION_THEOREM.md`
  - `YT_EXACT_SCHUR_NORMAL_FORM_UNIQUENESS_NOTE.md`
  - `scripts/frontier_yt_p1_color_factor_retention.py`
- **auditor confidence:** 0.93

### `yt_p1_delta_1_bz_computation_note_2026-04-17`

- **Note:** [`YT_P1_DELTA_1_BZ_COMPUTATION_NOTE_2026-04-17.md`](../../docs/YT_P1_DELTA_1_BZ_COMPUTATION_NOTE_2026-04-17.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_numerical_match~~
- **effective_status:** ~~audited_numerical_match~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** At the literature-cluster central I_v_scalar = 4 and retained I_v_gauge = 0, Delta_1 = 2 and C_F Delta_1 alpha_LM/(4 pi) reproduces the packaged 1.92 percent value.  _(class `G`)_
- **chain closes:** False — The runner gives correct arithmetic once the cited bracket and selected central are supplied, but it does not perform the framework-native BZ quadrature or derive the central value. Its own back-solved midpoint is I_v_scalar=4.5, which gives Delta_1=3, while the retained central uses I_v_scalar=4 because that literature-cluster choice reproduces the packaged 1.92 percent number.
- **rationale:** Issue: the headline retained central Delta_1=+2 and 1.924% contribution depend on selecting I_v_scalar=4 from a cited O(1) literature bracket, even though the runner's back-solved midpoint is 4.5 and would give Delta_1=+3 and 2.886%. Why this blocks: the central/package agreement is a chosen numerical match inside an external bracket, not a framework-native computation of the Brillouin-zone integral or a theorem fixing the central value. Repair target: perform a retained 4D BZ quadrature for I_v_scalar on the stated Cl(3) x Z^3 Wilson-plaquette/staggered/tadpole-improved action, with the conserved-current I_v_gauge and scalar-bilinear normalization derived from registered one-hop inputs; alternatively demote the note to an explicit citation-bound support result with no retained central. Claim boundary until fixed: safe to claim the conditional arithmetic map Delta_1=2(I_v_scalar-I_v_gauge)-6 and, if I_v_scalar in [3,7] and I_v_gauge=0 are supplied, the range Delta_1 in [0,8] and C_F-channel contribution [0%,7.70%]; not safe to claim retained Delta_1=+2 or the 1.92% match as derived.
- **open / conditional deps cited:**
  - `YT_P1_REP_A_REP_B_CANCELLATION_THEOREM_NOTE_2026-04-17.md`
  - `YT_P1_I_S_LATTICE_PT_CITATION_NOTE_2026-04-17.md`
  - `YT_P1_H_UNIT_RENORMALIZATION_FRAMEWORK_NATIVE_NOTE_2026-04-17.md`
  - `scripts/frontier_yt_p1_i1_lattice_pt_symbolic.py`
  - `scripts/frontier_yt_p1_delta_1_bz.py`
- **auditor confidence:** 0.96

### `yt_p1_delta_2_bz_computation_note_2026-04-17`

- **Note:** [`YT_P1_DELTA_2_BZ_COMPUTATION_NOTE_2026-04-17.md`](../../docs/YT_P1_DELTA_2_BZ_COMPUTATION_NOTE_2026-04-17.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_failed~~
- **effective_status:** ~~audited_failed~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** Under the cited I_SE and I_v_gauge ranges, Delta_2 has retained central value about -3.333 and safe negative-dominant range [-5,0], so the C_A contribution is non-positive across the retained range.  _(class `B`)_
- **chain closes:** False — The runner's own scenario table gives the combined outer envelope Delta_2 in [-5,+4/3] from the stated local-current endpoint I_v_gauge=3, I_SE=1. The advertised safe range [-5,0] is a clipped subrange that covers the central conserved-current case but not all cited current-definition sensitivity included by the note.
- **rationale:** Issue: the note claims a retained safe Delta_2 range [-5,0] and non-positive C_A contribution, but the source and live runner also include the local-current cited endpoint I_v_gauge=3, I_SE=1, which gives Delta_2=+4/3 and C_A Delta_2 alpha_LM/(4pi)=+2.886%. Why this blocks: a retained citation-bound range cannot omit a value generated by its own stated cited ranges and still claim sign control across current-definition sensitivity; additionally the headline -6.5% central corresponds to a noncanonical alternative scenario, while the canonical conserved central is -10/3 and -7.215%. Repair target: either restrict the claim strictly to the conserved point-split current and state Delta_2 in [-5,-5/3] with central -10/3, or include the local-current sensitivity honestly as the full envelope [-5,+4/3] and drop the non-positive sign claim; a framework-native BZ quadrature would be needed to choose between current definitions or narrow the range. Claim boundary until fixed: safe to claim the formula Delta_2=I_v_gauge-(5/3)I_SE and the scenario arithmetic printed by the runner; safe to claim the conserved-current C_A channel is negative for I_SE in [1,3]; not safe to claim the combined citation-bound range is [-5,0] or that the C_A channel is non-positive across all cited scenarios.
- **open / conditional deps cited:**
  - `YT_P1_REP_A_REP_B_CANCELLATION_THEOREM_NOTE_2026-04-17.md`
  - `YT_P1_H_UNIT_RENORMALIZATION_FRAMEWORK_NATIVE_NOTE_2026-04-17.md`
  - `scripts/frontier_yt_p1_i1_lattice_pt_symbolic.py`
  - `scripts/frontier_yt_p1_delta_2_bz.py`
- **auditor confidence:** 0.97

### `yt_p1_delta_3_bz_computation_note_2026-04-17`

- **Note:** [`YT_P1_DELTA_3_BZ_COMPUTATION_NOTE_2026-04-17.md`](../../docs/YT_P1_DELTA_3_BZ_COMPUTATION_NOTE_2026-04-17.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_conditional~~
- **effective_status:** ~~audited_conditional~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** Using the cited positive bracket I_SE^{fermion-loop} in [0.5,1.5] and the MSbar matching convention n_f=6, Delta_3=(4/3)I_SE is positive with central 0.933 and T_F n_f channel contribution about +2.02%.  _(class `B`)_
- **chain closes:** False — The runner verifies the arithmetic and sign after the fermion-loop BZ bracket, central value, Rep-A/Rep-B formula, and n_f=6 matching convention are supplied. It does not compute I_SE^{fermion-loop} on the retained lattice action or derive the matching-convention choice from retained inputs.
- **rationale:** Issue: the Delta_3 numerical bracket and central value are imported as a cited literature range I_SE^{fermion-loop} in [0.5,1.5] with central 0.7, and the runner hard-codes the MSbar n_f=6 convention while treating n_taste=16 only as contrast. Why this blocks: the arithmetic Delta_3=(4/3)I_SE and positive sign are exact conditional consequences of those supplied inputs, but a proposed_retained BZ-computation claim needs either a retained framework-native quadrature or registered retained dependencies that establish the integral bracket and matching convention. Repair target: perform the 4D BZ evaluation of the staggered fermion-loop self-energy on the canonical Cl(3) x Z^3/Wilson-plaquette/tadpole-improved action, and add a retained matching-convention theorem fixing whether the loop count is MSbar n_f=6 or lattice-side n_taste=16 for this coefficient. Claim boundary until fixed: safe to claim that if I_SE^{fermion-loop}>0 and the MSbar n_f=6 convention are supplied, Delta_3 is positive and the contribution is [+1.44%,+4.33%] for the cited bracket; not safe to claim a retained framework-native Delta_3 central or bracket.
- **open / conditional deps cited:**
  - `YT_P1_REP_A_REP_B_CANCELLATION_THEOREM_NOTE_2026-04-17.md`
  - `YT_P2_TASTE_STAIRCASE_BETA_FUNCTIONS_NOTE_2026-04-17.md`
  - `scripts/frontier_yt_p1_delta_3_bz.py`
- **auditor confidence:** 0.94

### `yt_p1_delta_r_2_loop_extension_note_2026-04-18`

- **Note:** [`YT_P1_DELTA_R_2_LOOP_EXTENSION_NOTE_2026-04-18.md`](../../docs/YT_P1_DELTA_R_2_LOOP_EXTENSION_NOTE_2026-04-18.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_conditional~~
- **effective_status:** ~~audited_conditional~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** Applying the retained loop-geometric bound r_R=0.22126 to the retained 1-loop central Delta_R=-3.27% and assuming same-sign bound saturation gives Delta_R^{through-2-loop}=Delta_R^{1-loop}(1+r_R)=-3.99% with P1 in [3.3%, 4.7%].  _(class `A`)_
- **chain closes:** False — The runner verifies the algebra of the color-tensor enumeration and envelope propagation, but the 1-loop central, loop-geometric bound, canonical constants, P3 analogy, m_t comparator, and same-sign/bound-saturation interpretation are imported without registered one-hop dependencies. The eight 2-loop BZ integrals are explicitly open, so the through-2-loop central is an assumed envelope scenario rather than a derived 2-loop correction.
- **rationale:** Issue: the proposed-retained 2-loop extension turns an inherited 1-loop central and inherited loop-geometric bound into a retained through-2-loop central by assuming the unknown 2-loop term saturates the bound and has the same sign, while all eight 2-loop BZ integrals remain open and the row registers no one-hop dependencies for the 1-loop master, loop-geometric theorem, canonical surface, P3 color-template notes, or observed m_t comparator. Why this blocks: the runner confirms exact Casimir arithmetic and envelope propagation after those inputs are supplied, but it does not compute any J_X integral, derive the 2-loop sign, justify saturation as a central estimate, or reconcile authority between the older literature-cited -3.27% base and the later full-staggered -3.77% canonical cross-reference. Repair target: register and audit the 1-loop master, full-staggered 1-loop update, loop-geometric bound, Rep-A/Rep-B, Delta_i notes, P3 color-factor templates, canonical constants, and comparator sources; either compute the eight J_X BZ integrals with a runner or demote the -3.99% value to a named envelope scenario with no retained central status. Claim boundary until fixed: it is safe to claim a conditional structural envelope: given Delta_R^{1-loop}=-3.27085% and r_R=0.221264, the 2-loop magnitude is bounded by 0.7237%, the geometric tail by 0.9294%, the bound-saturated same-sign scenario gives -3.9946%, and the broad m_t lane contains 172.69 GeV; it is not yet an audited retained 2-loop Delta_R computation or first-principles P1 precision closure.
- **open / conditional deps cited:**
  - `YT_P1_DELTA_R_MASTER_ASSEMBLY_THEOREM_NOTE_2026-04-18.md_not_registered_one_hop_dependency`
  - `YT_P1_LOOP_GEOMETRIC_BOUND_NOTE_2026-04-17.md_not_registered_one_hop_dependency`
  - `YT_P1_REP_A_REP_B_CANCELLATION_THEOREM_NOTE_2026-04-17.md_not_registered_one_hop_dependency`
  - `YT_P1_DELTA_1_BZ_COMPUTATION_NOTE_2026-04-17.md_not_registered_one_hop_dependency`
  - `YT_P1_DELTA_2_BZ_COMPUTATION_NOTE_2026-04-17.md_not_registered_one_hop_dependency`
  - `YT_P1_DELTA_3_BZ_COMPUTATION_NOTE_2026-04-17.md_not_registered_one_hop_dependency`
  - `YT_P1_BZ_QUADRATURE_FULL_STAGGERED_PT_NOTE_2026-04-18.md_not_registered_and_audited_conditional`
  - `YT_P1_BZ_QUADRATURE_2_LOOP_FULL_STAGGERED_PT_NOTE_2026-04-18.md_not_registered_one_hop_dependency`
  - `YT_P3_MSBAR_TO_POLE_K3_COLOR_FACTOR_RETENTION_NOTE_2026-04-17.md_not_registered_one_hop_dependency`
  - `scripts/canonical_plaquette_surface.py_not_registered_one_hop_dependency`
  - `eight_two_loop_BZ_integrals_J_FF_J_FA_J_AA_J_Fl_J_Al_J_ll_J_FFh_J_Fh_open`
  - `same_sign_bound_saturation_central_assumption_not_derived`
  - `observed_m_t_PDG_comparator_not_registered`
- **auditor confidence:** high

### `yt_p1_delta_r_master_assembly_theorem_note_2026-04-18`

- **Note:** [`YT_P1_DELTA_R_MASTER_ASSEMBLY_THEOREM_NOTE_2026-04-18.md`](../../docs/YT_P1_DELTA_R_MASTER_ASSEMBLY_THEOREM_NOTE_2026-04-18.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_failed~~
- **effective_status:** ~~audited_failed~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The note preserves the literature-cited three-channel assembly Delta_R=-3.27% but declares the canonical retained central superseded by the full-staggered-PT value Delta_R=-3.77% +/- 0.45%.  _(class `B`)_
- **chain closes:** False — The source note's current canonical claim is not what the primary runner verifies: the live runner still declares the older literature-cited -3.2709% assembly as the definitive result and says the framework-native BZ quadratures remain open. The source's superseding full-staggered-PT central is delegated to another note/runner and is not checked by this primary runner or registered as a dependency in this row.
- **rationale:** Issue: the audited source has a canonical-central supersession notice, but the attached runner validates only the old literature-cited -3.27% roll-up and ends with that value as the definitive result; it does not verify the claimed canonical -3.77% +/- 0.45% full-staggered-PT central and even prints that framework-native BZ quadratures remain open. Why this blocks: a proposed_retained master assembly cannot simultaneously claim canonical retained supersession while its primary runner checks the superseded calculation, and the old roll-up inherits cited/channel inputs and ranges rather than independently retained canonical values. Repair target: either split this row into a conditional literature-cited assembly with no canonical retained language, or update the primary runner and registered one-hop dependencies so this claim directly verifies the full-staggered-PT integrals, the -3.77% +/- 0.45% assembly, and the supersession relationship. Claim boundary until fixed: safe to claim the arithmetic old roll-up -3.2709% from the supplied per-channel central values (+2, -10/3, +0.933); not safe to claim this row establishes the canonical retained Delta_R central, P1 band, or m_t lane.
- **open / conditional deps cited:**
  - `YT_P1_BZ_QUADRATURE_FULL_STAGGERED_PT_NOTE_2026-04-18.md`
  - `YT_P1_DELTA_1_BZ_COMPUTATION_NOTE_2026-04-17.md`
  - `YT_P1_DELTA_2_BZ_COMPUTATION_NOTE_2026-04-17.md`
  - `YT_P1_DELTA_3_BZ_COMPUTATION_NOTE_2026-04-17.md`
  - `scripts/frontier_yt_p1_delta_r_master_assembly.py`
- **auditor confidence:** 0.96

### `yt_p1_delta_r_sm_rge_crosscheck_note_2026-04-18`

- **Note:** [`YT_P1_DELTA_R_SM_RGE_CROSSCHECK_NOTE_2026-04-18.md`](../../docs/YT_P1_DELTA_R_SM_RGE_CROSSCHECK_NOTE_2026-04-18.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_conditional~~
- **effective_status:** ~~audited_conditional~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The backward 2-loop SM RGE gives y_t/g_s(M_Pl)=0.78510, whose naive comparison to Ward*(1+Delta_R)=0.3949 fails by +95.6%, and the note classifies this as consistent only after invoking an orthogonal v-scale matching decomposition M = sqrt(8/9)*F_yt*sqrt(u_0).  _(class `D`)_
- **chain closes:** False — The runner verifies the SM-RGE integration and several arithmetic checks, but the consistency verdict depends on unregistered Ward, Delta_R, v-boundary, color-projection, CMT, P2 matching, and QFP-envelope authorities. The runner also tests the older -3.27% Delta_R central, while the note says the canonical retained central has been superseded to -3.77% +/- 0.45%.
- **rationale:** Issue: the registered runner is a valid deterministic SM-RGE arithmetic check, but the retained cross-validation conclusion is conditional on a large set of unregistered authorities and on the interpretive claim that the 95.6% direct-comparison gap is orthogonal to the M_Pl scheme-conversion Delta_R rather than a failed comparator. Why this blocks: from the audit packet alone, a hostile auditor can verify that backward SM RGE gives y_t/g_s(M_Pl)=0.78510 and that it does not equal Ward*(1+Delta_R)=0.3949; the packet cannot independently validate the v-scale color projection, CMT endpoint, P2 M decomposition, QFP envelope, Delta_i inputs, or the orthogonality theorem that turns that failed direct comparison into support for Delta_R. Repair target: register the Ward, Delta_i/Delta_R, zero-import boundary, P2 v-matching, QFP-envelope, color-projection, CMT endpoint, and canonical -3.77% BZ-quadrature authorities as one-hop dependencies, and update the runner to consume their outputs, test both -3.27% and canonical -3.77% surfaces explicitly, and assert a derived factorization theorem explaining why the direct M_Pl ratio comparison is not the relevant observable. Claim boundary until fixed: it is safe to claim a conditional numerical cross-check: given the framework primary-chain v-boundaries and accepted v-scale matching factorization, the SM 2-loop backward integration is reproducible and does not by itself falsify the chosen Delta_R scheme-conversion interpretation; it is not an audited retained independent validation of Delta_R or of the full lattice-to-SM translation.
- **open / conditional deps cited:**
  - `YT_WARD_IDENTITY_DERIVATION_THEOREM.md_not_registered_one_hop_dependency`
  - `YT_P1_REP_A_REP_B_CANCELLATION_THEOREM_NOTE_2026-04-17.md_not_registered_one_hop_dependency`
  - `YT_P1_BZ_QUADRATURE_FULL_STAGGERED_PT_NOTE_2026-04-18.md_not_registered_one_hop_dependency`
  - `YT_ZERO_IMPORT_CHAIN_NOTE.md_not_registered_one_hop_dependency`
  - `YT_P2_V_MATCHING_THEOREM_NOTE_2026-04-17.md_not_registered_one_hop_dependency`
  - `YT_QFP_INSENSITIVITY_SUPPORT_NOTE.md_not_registered_one_hop_dependency`
  - `color_projection_and_CMT_endpoint_factorization_theorem_not_registered`
- **auditor confidence:** high

### `yt_p1_h_unit_renormalization_framework_native_note_2026-04-17`

- **Note:** [`YT_P1_H_UNIT_RENORMALIZATION_FRAMEWORK_NATIVE_NOTE_2026-04-17.md`](../../docs/YT_P1_H_UNIT_RENORMALIZATION_FRAMEWORK_NATIVE_NOTE_2026-04-17.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_failed~~
- **effective_status:** ~~audited_failed~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The note claims a retained envelope bound |I_S^{framework}| <= 16 * |1 - 1/<P>|^{-1} = 23.35, so the cited I_S in [4,10] is structurally compatible with the framework-native H_unit reduction.  _(class `B`)_
- **chain closes:** False — The runner verifies symbolic diagram bookkeeping and evaluates the proposed envelope formula, but it does not derive an inequality bounding the tadpole-subtracted BZ integral. The note also leaves the actual I_S^{taste}, I_S^{Wilson}, and I_S^{mix} quadrature open.
- **rationale:** Issue: the load-bearing retained envelope |I_S^{framework}| <= 23.35 is asserted from u_0 and <P>, but neither the note nor the runner proves that this formula bounds the singular tadpole-subtracted Brillouin-zone integral; the runner only computes the proposed closed form and checks that the cited [4,10] interval lies inside it. Why this blocks: a framework-native retained bound on I_S requires either an analytic bound after the D14 tadpole subtraction and MSbar subtraction, or an explicit 4D quadrature of I_S^{taste}, I_S^{Wilson}, and I_S^{mix}; interval containment under an assumed envelope is not a derivation. Repair target: prove the regulator-subtracted BZ-integrand inequality from the retained propagators, tadpole split, and canonical plaquette input, or replace the envelope with a runner that performs the framework-native quadrature and uncertainty control; also audit the cited action, plaquette, tadpole, and Ward parents. Claim boundary until fixed: safe to claim symbolic diagram/Feynman-rule bookkeeping and the arithmetic fact that the proposed formula evaluates to 23.3507 and contains [4,10]; not safe to claim a retained framework-native bound or closed H_unit 1-loop renormalization.
- **open / conditional deps cited:**
  - `MINIMAL_AXIOMS_2026-04-11.md`
  - `PLAQUETTE_SELF_CONSISTENCY_NOTE.md`
  - `YT_VERTEX_POWER_DERIVATION.md`
  - `YT_WARD_IDENTITY_DERIVATION_THEOREM.md`
- **auditor confidence:** high

### `yt_p1_i_s_lattice_pt_citation_note_2026-04-17`

- **Note:** [`YT_P1_I_S_LATTICE_PT_CITATION_NOTE_2026-04-17.md`](../../docs/YT_P1_I_S_LATTICE_PT_CITATION_NOTE_2026-04-17.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_conditional~~
- **effective_status:** ~~audited_conditional~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The note adopts the cited tadpole-improved staggered scalar-density bracket I_S in [4,10] with central I_S ~= 6 and maps it through P1 = (alpha_LM/(4 pi)) C_F I_S to P1 in [3.848%,9.620%] with central 5.772%.  _(class `B`)_
- **chain closes:** False — The runner reproduces the arithmetic from the cited bracket and logs that the cited I_S is not framework-native. The bracket, color-factor reduction, Ward/current reduction, plaquette constants, and bridge/obstruction comparison are inherited from external or non-clean authorities.
- **rationale:** Issue: the P1 revision is a citation-and-bound calculation over a hard-coded external analogue bracket I_S in [4,10] and central I_S ~= 6, while the note explicitly does not derive I_S on the retained Cl(3) x Z^3 canonical action. Why this blocks: the arithmetic maps the adopted bracket to P1, but a proposed-retained framework-specific P1 revision needs the native H_unit Brillouin-zone integral and clean color/current/canonical-surface bridge inputs, not only an external staggered-scalar analogue. Repair target: perform and audit the framework-native 1-loop BZ integration for the composite H_unit scalar bilinear, and separately clean-audit the color-factor, Ward/current, plaquette/tadpole, bridge, and obstruction parents. Claim boundary until fixed: safe to claim that, conditional on adopting the cited analogue bracket I_S in [4,10], the arithmetic gives P1 in [3.848%,9.620%] with central 5.772%; not safe to claim an audited retained native P1 revision from this note alone.
- **open / conditional deps cited:**
  - `PLAQUETTE_SELF_CONSISTENCY_NOTE.md`
  - `UV_GAUGE_TO_YUKAWA_BRIDGE_SC_VS_PERT_NOTE.md`
  - `YT_P1_COLOR_FACTOR_RETENTION_NOTE_2026-04-17.md`
  - `YT_UV_TO_IR_TRANSPORT_OBSTRUCTION_THEOREM_NOTE_2026-04-17.md`
  - `YT_WARD_IDENTITY_DERIVATION_THEOREM.md`
- **auditor confidence:** high

### `yt_p1_loop_geometric_bound_note_2026-04-17`

- **Note:** [`YT_P1_LOOP_GEOMETRIC_BOUND_NOTE_2026-04-17.md`](../../docs/YT_P1_LOOP_GEOMETRIC_BOUND_NOTE_2026-04-17.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_conditional~~
- **effective_status:** ~~audited_conditional~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The note asserts the geometric ratio bound |Delta_{n+1}| <= r_R |Delta_n| for all n >= 1 with r_R = (alpha_LM/pi) b_0 = 0.22126, then sums it to bound the P1 loop-expansion tail by Delta_1 r_R/(1-r_R).  _(class `B`)_
- **chain closes:** False — The runner verifies retained inputs, indicative two-loop color-prefactor ratios, and the geometric-sum arithmetic, but it does not prove the all-orders ratio bound for the actual lattice-to-MSbar coefficients. The source itself states that the geometric decay assumption would need further structural input to be strict for all n.
- **rationale:** Issue: the claimed retained tail bound depends on the unproved global assumption |Delta_{n+1}| <= r_R |Delta_n| for all higher loops; the runner only shows that r_R envelopes indicative two-loop color-prefactor ratios and then performs the geometric-sum arithmetic. Why this blocks: closing the P1 loop-expansion axis requires a theorem or computation controlling the actual two-loop and higher lattice-to-MSbar BZ coefficients, not just a beta0-motivated envelope over color prefactors with |J_X| ~ O(1). Repair target: supply a framework-native renormalon/geometric-growth theorem for the retained action or compute/bound the relevant two-loop and higher BZ primitives sufficiently to establish the ratio inequality, then re-run a runner that fails if the inequality is not proven. Claim boundary until fixed: safe to claim that, if the geometric ratio r_R = 0.22126 is assumed, the tail factor is 0.2841 and the displayed 0.547%/1.640% tail numbers follow; not safe to claim an audited retained all-orders loop-tail bound or closure of the P1 loop-expansion axis.
- **open / conditional deps cited:**
  - `UV_GAUGE_TO_YUKAWA_BRIDGE_SC_VS_PERT_NOTE.md`
  - `YT_EW_COLOR_PROJECTION_THEOREM.md`
  - `YT_P1_COLOR_FACTOR_RETENTION_NOTE_2026-04-17.md`
  - `YT_P1_I_S_LATTICE_PT_CITATION_NOTE_2026-04-17.md`
  - `YT_UV_TO_IR_TRANSPORT_OBSTRUCTION_THEOREM_NOTE_2026-04-17.md`
- **auditor confidence:** high

### `yt_p1_rep_a_rep_b_cancellation_theorem_note_2026-04-17`

- **Note:** [`YT_P1_REP_A_REP_B_CANCELLATION_THEOREM_NOTE_2026-04-17.md`](../../docs/YT_P1_REP_A_REP_B_CANCELLATION_THEOREM_NOTE_2026-04-17.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_failed~~
- **effective_status:** ~~audited_failed~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The note claims a definitive PARTIAL CANCELLATION verdict: external Z_psi cancels exactly, full cancellation is rejected, and the ratio retains generically nonzero C_F, C_A, and T_F n_f channel coefficients so the cited P1 bracket remains operational.  _(class `B`)_
- **chain closes:** False — The runner establishes symbolic cancellation of the shared external-leg term, but it does not compute or bound the actual BZ integrals I_v_scalar, I_v_gauge, and I_SE. Its rejection of full cancellation uses representative scenarios, not the retained-surface integral values needed to rule out accidental channel or total cancellation.
- **rationale:** Issue: the exact external Z_psi cancellation is shown, but the load-bearing claim that full cancellation is definitively rejected and that the P1 bracket remains operational is supported only by symbolic channel formulas plus hand-picked representative BZ scenarios; the actual retained-surface values of I_v_scalar, I_v_gauge, and I_SE are not computed or bounded. Why this blocks: whether the Ward ratio has nonzero channel coefficients or a nonzero total correction is decided by those BZ integrals, and a generic/scenario argument cannot close a Nature-grade cancellation theorem. Repair target: perform the framework-native 1-loop BZ evaluation, or prove identities/inequalities for I_v_scalar - I_v_gauge and I_SE that rule out full channel cancellation and quantify the ratio correction; then make the runner consume those computed/bounded integrals. Claim boundary until fixed: safe to claim exact cancellation of the common external-quark Z_psi term and the displayed symbolic difference formula conditional on the contribution catalog; not safe to claim a definitive partial-cancellation theorem, nonzero ratio correction, or retained operational P1 bracket from this note alone.
- **open / conditional deps cited:**
  - `UV_GAUGE_TO_YUKAWA_BRIDGE_SC_VS_PERT_NOTE.md`
  - `YT_EW_COLOR_PROJECTION_THEOREM.md`
  - `YT_P1_COLOR_FACTOR_RETENTION_NOTE_2026-04-17.md`
  - `YT_P1_I_S_LATTICE_PT_CITATION_NOTE_2026-04-17.md`
  - `YT_P1_I_S_REVISION_VERIFICATION_NOTE_2026-04-17.md`
  - `YT_WARD_IDENTITY_DERIVATION_THEOREM.md`
- **auditor confidence:** high

### `yt_p1_shared_fierz_no_go_sub_theorem_note_2026-04-17`

- **Note:** [`YT_P1_SHARED_FIERZ_NO_GO_SUB_THEOREM_NOTE_2026-04-17.md`](../../docs/YT_P1_SHARED_FIERZ_NO_GO_SUB_THEOREM_NOTE_2026-04-17.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_conditional~~
- **effective_status:** ~~audited_conditional~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The note claims there is no algebraic rearrangement of the Ward-theorem color Fierz D12 with the Lorentz Clifford Fierz S2 that maps the Rep-A 1-loop structure to the Rep-B 1-loop structure, so Delta_R must be computed channel by channel.  _(class `B`)_
- **chain closes:** False — The runner checks hard-coded Rep-A and Rep-B one-loop piece lists and confirms only external Z_psi is exactly shared. It does not derive the piece lists from the retained action/Feynman rules or prove a formal theorem that the relevant Fierz identities cannot act beyond fixed-diagram color/Dirac algebra.
- **rationale:** Issue: the shared-Fierz no-go is valid only conditional on the supplied Rep-A/Rep-B one-loop diagram catalogs and on the premise that D12/S2 Fierz operations cannot change diagram topology or renormalization type; the runner encodes those catalogs rather than deriving them from the retained lattice action. Why this blocks: a definitive retained no-go must rule out the shortcut from retained inputs, not from a pre-labeled dictionary of what Fierz is allowed to touch. Repair target: derive the complete Rep-A and Rep-B 1-loop piece lists from the canonical action/Feynman rules, prove the allowed action of D12 and S2 on those fixed diagrams, and make the runner construct the catalogs rather than hard-code them. Claim boundary until fixed: safe to claim that, given the supplied catalogs, only external Z_psi is shared and the remaining listed pieces require channel-by-channel BZ evaluation; not safe to claim an audited retained definitive shared-Fierz no-go from this note alone.
- **open / conditional deps cited:**
  - `YT_COLOR_PROJECTION_CORRECTION_NOTE.md`
  - `YT_P1_COLOR_FACTOR_RETENTION_NOTE_2026-04-17.md`
  - `YT_P1_REP_A_REP_B_CANCELLATION_THEOREM_NOTE_2026-04-17.md`
  - `YT_UV_TO_IR_TRANSPORT_OBSTRUCTION_THEOREM_NOTE_2026-04-17.md`
  - `YT_WARD_IDENTITY_DERIVATION_THEOREM.md`
- **auditor confidence:** high

### `yt_p2_f_yt_loop_geometric_bound_note_2026-04-17`

- **Note:** [`YT_P2_F_YT_LOOP_GEOMETRIC_BOUND_NOTE_2026-04-17.md`](../../docs/YT_P2_F_YT_LOOP_GEOMETRIC_BOUND_NOTE_2026-04-17.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_conditional~~
- **effective_status:** ~~audited_conditional~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The note assumes |delta_M_{n+1}| <= r_M |delta_M_n| for all n >= 2 with r_M = (alpha_LM/pi) b_0 = 0.22126, then sums the geometric tail to claim |tail(N=2)| <= 0.01335 and a 0.677% fractional m_t residual.  _(class `B`)_
- **chain closes:** False — The runner verifies retained constants, carried M values, the observed 1-to-2 loop ratio, and the geometric-sum arithmetic. It does not derive or compute the higher-loop integrated SM-RGE shifts needed to establish the ratio bound for n >= 2.
- **rationale:** Issue: the retained P2 tail bound rests on an unproved geometric-decay assumption for the integrated coupled SM-RGE shifts, |delta_M_{n+1}| <= r_M |delta_M_n| for all n >= 2; the runner only checks that r_M exceeds the observed 1-to-2 ratio and then performs the geometric sum. Why this blocks: closing the P2 loop-expansion axis requires a theorem or computation controlling the actual 3-loop and higher integrated contributions to M, not just a b_0-motivated analogy to P1 plus carried 1-loop/2-loop values. Repair target: prove a renormalon/geometric-growth bound for the integrated SM RGE on the retained canonical surface, or compute enough higher-loop integrated shifts to establish the ratio inequality; make the runner consume those derived shifts or proof certificates. Claim boundary until fixed: safe to claim that, if r_M = 0.22126 bounds all higher loop-shift ratios, the tail arithmetic gives |tail(N=2)| = 0.01335 and 0.677%; not safe to claim an audited retained framework-native P2 loop-tail closure from this note alone.
- **open / conditional deps cited:**
  - `UV_GAUGE_TO_YUKAWA_BRIDGE_SC_VS_PERT_NOTE.md`
  - `YT_EW_COLOR_PROJECTION_THEOREM.md`
  - `YT_P1_LOOP_GEOMETRIC_BOUND_NOTE_2026-04-17.md`
  - `YT_P2_TASTE_STAIRCASE_TRANSPORT_NOTE_2026-04-17.md`
  - `YT_P2_V_MATCHING_THEOREM_NOTE_2026-04-17.md`
  - `YT_UV_TO_IR_TRANSPORT_OBSTRUCTION_THEOREM_NOTE_2026-04-17.md`
- **auditor confidence:** high

### `yt_p2_v_matching_theorem_note_2026-04-17`

- **Note:** [`YT_P2_V_MATCHING_THEOREM_NOTE_2026-04-17.md`](../../docs/YT_P2_V_MATCHING_THEOREM_NOTE_2026-04-17.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_conditional~~
- **effective_status:** ~~audited_conditional~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The note claims the v-matching coefficient closes in decomposed form as M = sqrt(u_0) * F_yt * sqrt(8/9), with 1-loop M = 1.926 inside the QFP 3% envelope and 2-loop quantitative closure supplied by the primary chain at M = 1.9734.  _(class `B`)_
- **chain closes:** False — The runner reproduces the Path C algebra and 1-loop SM-RGE integration, but the mixed lattice/SM endpoint factorization, color projection, Ward/CMT inputs, QFP envelope, and 2-loop primary-chain closure are all inherited. The runner does not independently derive the 2-loop M target from retained inputs.
- **rationale:** Issue: the proposed M closure depends on a selected mixed-scheme factorization M = sqrt(u_0) * F_yt * sqrt(8/9), a QFP 3% support envelope, and a 2-loop primary-chain value that the runner cites rather than derives. Why this blocks: a retained v-matching theorem must prove the lattice-to-SM endpoint map, color-projection factor, and RGE transport as one coherent bridge, and must compute the quantitative 2-loop closure from retained beta functions in the runner or registered clean dependencies. Repair target: clean-audit the taste-staircase, Ward/CMT, color-projection, zero-import beta-coefficient, and QFP parents, and extend this runner to perform the retained 2-loop SM-RGE integration and verify M = 1.9734 from those inputs without reading the target as a premise. Claim boundary until fixed: safe to claim conditional Path C arithmetic: given the supplied endpoint factors and 1-loop RGE, M_1-loop = 1.926 and lies within the asserted 3% QFP envelope; not safe to claim audited retained closure of the P2 v-matching coefficient.
- **open / conditional deps cited:**
  - `YT_COLOR_PROJECTION_CORRECTION_NOTE.md`
  - `YT_P2_TASTE_STAIRCASE_TRANSPORT_NOTE_2026-04-17.md`
  - `YT_QFP_INSENSITIVITY_SUPPORT_NOTE.md`
  - `YT_UV_TO_IR_TRANSPORT_OBSTRUCTION_THEOREM_NOTE_2026-04-17.md`
  - `YT_WARD_IDENTITY_DERIVATION_THEOREM.md`
  - `YT_ZERO_IMPORT_CHAIN_NOTE.md`
- **auditor confidence:** high

### `yt_p3_k_series_geometric_bound_note_2026-04-17`

- **Note:** [`YT_P3_K_SERIES_GEOMETRIC_BOUND_NOTE_2026-04-17.md`](../../docs/YT_P3_K_SERIES_GEOMETRIC_BOUND_NOTE_2026-04-17.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_conditional~~
- **effective_status:** ~~audited_conditional~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** Assuming the geometric ratio bound |delta_{n+1}| <= r_bound * |delta_n| holds for all n >= 3, the residual tail after retained truncation index N = 3 is upper-bounded by delta_3 * r_bound / (1 - r_bound) = 0.001458.  _(class `B`)_
- **chain closes:** False — The runner verifies the imported K1-K3 values, the first two observed ratios, and the finite geometric-sum arithmetic, but it does not prove the all-higher-order ratio bound for K4 and beyond. The claimed tail control therefore depends on the note's explicit geometric-decay assumption and on non-clean upstream K-series/coupling authorities.
- **rationale:** Issue: the retained tail bound rests on the unproved assumption that |delta_{n+1}| <= r_bound * |delta_n| with r_bound = (alpha_s/pi) * C_A^2 for every n >= 3, while the runner only checks n = 1,2 ratios and then sums a geometric series. Why this blocks: a retained bound on the full MSbar-to-pole K_n tail requires a theorem or computation controlling K4 and higher terms, not an envelope selected because it covers the first two ratios. Repair target: prove a framework-native renormalon/asymptotic coefficient bound on the retained action, or extend the runner to compute/bound K4+ from retained inputs and show the ratio inequality uniformly from some n0. Claim boundary until fixed: safe to claim conditional arithmetic: given K1-K3, alpha_s(m_t)=0.1079, and the geometric-decay premise, the tail bound is 0.001457 and about 0.137% of m_t; not safe to claim audited retained closure of the P3 K-series tail or P3 coverage budget.
- **open / conditional deps cited:**
  - `ALPHA_S_DERIVED_NOTE.md`
  - `YT_EW_COLOR_PROJECTION_THEOREM.md`
  - `YT_P3_MSBAR_TO_POLE_K1_FRAMEWORK_NATIVE_DERIVATION_NOTE_2026-04-17.md`
  - `YT_P3_MSBAR_TO_POLE_K2_COLOR_FACTOR_RETENTION_NOTE_2026-04-17.md`
  - `YT_P3_MSBAR_TO_POLE_K2_INTEGRAL_CITATION_NOTE_2026-04-17.md`
  - `YT_P3_MSBAR_TO_POLE_K3_COLOR_FACTOR_RETENTION_NOTE_2026-04-17.md`
  - `YT_UV_TO_IR_TRANSPORT_OBSTRUCTION_THEOREM_NOTE_2026-04-17.md`
- **auditor confidence:** high

### `yt_p3_msbar_to_pole_k1_framework_native_derivation_note_2026-04-17`

- **Note:** [`YT_P3_MSBAR_TO_POLE_K1_FRAMEWORK_NATIVE_DERIVATION_NOTE_2026-04-17.md`](../../docs/YT_P3_MSBAR_TO_POLE_K1_FRAMEWORK_NATIVE_DERIVATION_NOTE_2026-04-17.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_failed~~
- **effective_status:** ~~audited_failed~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The remaining kinematic + Dirac-trace integral contributes a factor of 1 on shell in the alpha_s/pi convention, so K_1 = C_F.  _(class `B`)_
- **chain closes:** False — The source note and runner verify the SU(3) Casimir arithmetic, but they do not derive or cite a retained theorem for the on-shell MSbar one-loop self-energy finite coefficient. The runner assigns K_1 = C_F before checking it, so the contested physics bridge is not computed.
- **rationale:** Issue: the framework-native claim depends on the assertion that the non-color one-loop heavy-quark self-energy integral equals +1 in the alpha_s/pi MSbar-to-pole convention, but the note supplies no retained theorem or computation for that integral and the runner hard-codes K_1 = C_F. Why this blocks: C_F = 4/3 is only the color factor; the physical coefficient K_1 also requires the on-shell Dirac/kinematic integral, scheme convention, mass-renormalization subtraction, and sign normalization. Repair target: add a retained one-loop on-shell MSbar self-energy theorem or runner computation deriving the finite coefficient from the Feynman rules and renormalization convention, then multiply by the independently retained SU(3) Casimir. Claim boundary until fixed: safe to claim the exact SU(3) fundamental Casimir C_F = 4/3 and the arithmetic shift (4/3)(0.108/pi) = 4.58% if alpha_s(m_t)=0.108 is supplied; not safe to claim a framework-native derivation of the MSbar-to-pole K_1 coefficient.
- **open / conditional deps cited:**
  - `scripts/frontier_yt_p3_msbar_to_pole_k1.py`
- **auditor confidence:** 0.94

### `yt_p3_msbar_to_pole_k2_color_factor_retention_note_2026-04-17`

- **Note:** [`YT_P3_MSBAR_TO_POLE_K2_COLOR_FACTOR_RETENTION_NOTE_2026-04-17.md`](../../docs/YT_P3_MSBAR_TO_POLE_K2_COLOR_FACTOR_RETENTION_NOTE_2026-04-17.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_failed~~
- **effective_status:** ~~audited_failed~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The four color tensors {C_F^2, C_F C_A, C_F T_F n_l, C_F T_F} are linearly independent and form the complete 2-loop on-shell heavy-quark color-tensor subspace, so K_2 decomposes into exactly those four channels.  _(class `B`)_
- **chain closes:** False — The note and runner verify arithmetic after assuming the four-channel color basis; they do not derive the two-loop topology/color-basis completeness from retained inputs. The numerical reconstruction is also circular: the runner constructs the n_l-independent constant from the literature target K_2(5) and then reproduces that target exactly.
- **rationale:** Issue: the retained K_2 skeleton rests on an asserted complete two-loop color-basis theorem, but the source note provides no retained derivation of the on-shell two-loop topology classification and the runner defines K_2_sym to be the claimed four-term expression before checking it. Why this blocks: exact SU(3) prefactor arithmetic does not prove that these are all and only the allowed two-loop mass-conversion color channels, and the advertised K_2(5)=10.9405 reconstruction is not independent because C_0 is back-solved from the target. Repair target: add a retained two-loop Feynman-topology/color-reduction theorem or runner that enumerates the contributing diagrams, reduces their color factors to the four tensors, proves absence of other tensors at two loops, and reconstructs K_2 from independently supplied J_FF, J_FA, J_Fl, and J_Fh values rather than from the final target. Claim boundary until fixed: safe to claim arithmetic prefactors {16/9, 4, 10/3, 2/3} if C_F=4/3, C_A=3, T_F=1/2, and n_l=5 are supplied; not safe to claim a retained complete K_2 color-tensor skeleton or an independent K_2 numerical reconstruction.
- **open / conditional deps cited:**
  - `YT_P3_MSBAR_TO_POLE_K2_INTEGRAL_CITATION_NOTE_2026-04-17.md`
  - `scripts/frontier_yt_p3_msbar_to_pole_k2.py`
- **auditor confidence:** 0.95

### `yt_p3_msbar_to_pole_k3_color_factor_retention_note_2026-04-17`

- **Note:** [`YT_P3_MSBAR_TO_POLE_K3_COLOR_FACTOR_RETENTION_NOTE_2026-04-17.md`](../../docs/YT_P3_MSBAR_TO_POLE_K3_COLOR_FACTOR_RETENTION_NOTE_2026-04-17.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_failed~~
- **effective_status:** ~~audited_failed~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** Because all ten prefactors are non-zero rationals, the functional maps surjectively onto R: for any real target T there exist real vectors K such that the sum equals T; in particular K_3(n_l = 5) = 80.405 is structurally admissible.  _(class `B`)_
- **chain closes:** False — The runner verifies SU(3) tensor arithmetic and then constructs an accommodation witness after importing the target K_3 value. It does not derive the complete three-loop topology/color basis, the primitive integral values, or an independent reconstruction of K_3.
- **rationale:** Issue: the claimed retained K_3 color-tensor skeleton is supported by exact Casimir arithmetic plus a vacuous accommodation argument: since the ten coefficients are nonzero, a back-filled vector can reproduce any supplied target, including the imported K_3(n_l=5)=80.405. Why this blocks: retention of a physical three-loop MSbar-to-pole coefficient skeleton requires proving that these are all and only the contributing color structures and reconstructing K_3 from independently specified primitive integrals; an underconstrained witness does not establish the skeleton or the 98.69% coverage claim. Repair target: add a retained three-loop Feynman-topology/color-reduction theorem and a runner that enumerates the diagrams, reduces their color factors to the ten tensors, proves absence of missing tensors, and reconstructs K_3 from independent K_FFF...K_Fhh inputs rather than from the final target. Claim boundary until fixed: safe to claim the listed SU(3) tensor-product arithmetic and that the displayed linear form can be made to equal 80.405 if unconstrained primitive coefficients are chosen; not safe to claim a retained complete K_3 color-tensor skeleton or retained cumulative K-series coverage through three loops.
- **open / conditional deps cited:**
  - `CHARGED_LEPTON_MASS_HIERARCHY_REVIEW_NOTE_2026-04-17.md`
  - `YT_EW_COLOR_PROJECTION_THEOREM.md`
  - `YT_P3_MSBAR_TO_POLE_K1_FRAMEWORK_NATIVE_DERIVATION_NOTE_2026-04-17.md`
  - `YT_P3_MSBAR_TO_POLE_K2_COLOR_FACTOR_RETENTION_NOTE_2026-04-17.md`
  - `YT_UV_TO_IR_TRANSPORT_OBSTRUCTION_THEOREM_NOTE_2026-04-17.md`
- **auditor confidence:** high

### `yt_ssb_matching_gap_analysis_note_2026-04-18`

- **Note:** [`YT_SSB_MATCHING_GAP_ANALYSIS_NOTE_2026-04-18.md`](../../docs/YT_SSB_MATCHING_GAP_ANALYSIS_NOTE_2026-04-18.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_renaming~~
- **effective_status:** ~~audited_renaming~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The Ward 4-fermion channel and the physical trilinear are both matrix elements of H_unit; they share the 1/sqrt(6) coefficient by construction.  _(class `F`)_
- **chain closes:** False — The note identifies the Ward four-fermion matrix element and the physical trilinear coefficient by assigning both to the same H_unit normalization. The runner then sets y_t_phys = 1/sqrt(6) and checks arithmetic, but it does not derive the SSB operator matching, source/VEV normalization, chirality projection, or functional trilinear vertex from the retained action.
- **rationale:** Issue: the matching closure equates a Ward 4-fermion Q_L x Q_L* matrix element with a physical Qbar_L-H-u_R trilinear coefficient by declaring that both read the same H_unit normalization factor 1/sqrt(6). Why this blocks: these are different Green-function/readout structures, and a retained matching theorem must derive the HS/source normalization, SSB VEV division, chirality projection, LSZ or external-state normalization, and absence of extra factors rather than identifying the symbols after the fact. Repair target: add a retained tree-level operator-matching theorem and runner that starts from the retained action with an auxiliary/composite H field, computes the relevant functional derivatives before and after SSB, and obtains the trilinear coefficient without pre-setting y_t_phys = 1/sqrt(6). Claim boundary until fixed: safe to claim the H_unit normalization arithmetic and that two quantities defined as the same H_unit component overlap both equal 1/sqrt(6); not safe to claim the SSB matching gap is closed for the physical Yukawa trilinear.
- **open / conditional deps cited:**
  - `ANOMALY_FORCES_TIME_THEOREM.md`
  - `OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md`
  - `YT_CLASS_5_NON_QL_YUKAWA_VERTEX_NOTE_2026-04-18.md`
  - `YT_WARD_IDENTITY_DERIVATION_THEOREM.md`
  - `YT_BOTTOM_YUKAWA_RETENTION_ANALYSIS_NOTE_2026-04-18.md`
- **auditor confidence:** high
