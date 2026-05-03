# Audit Queue

**Generated:** 2026-05-03T13:23:44.602736+00:00
**Total pending:** 757
**Ready (all deps already at retained-grade or metadata tiers):** 107

By criticality:
- `critical`: 61
- `high`: 222
- `medium`: 263
- `leaf`: 211

Auditor (Codex GPT-5.5 by default) should pull from the top of this list. Critical claims require cross-confirmation by a second independent clean-room auditor before `audited_clean` lands.

## Top 50

| # | claim_id | claim_type | reason | criticality | desc | score | ready | indep required | runner |
|---:|---|---|---|---|---:|---:|:---:|---|---|
| 1 | `gauge_vacuum_plaquette_local_environment_factorization_theorem_note` | bounded_theorem | unaudited | critical | 267 | 11.07 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_local_environment_factorization.py` |
| 2 | `gauge_vacuum_plaquette_infinite_hierarchy_obstruction_note` | open_gate | unaudited | critical | 265 | 10.55 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_infinite_hierarchy_obstruction.py` |
| 3 | `gauge_vacuum_plaquette_perron_reduction_theorem_note` | positive_theorem | unaudited | critical | 265 | 10.55 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_perron_reduction_theorem.py` |
| 4 | `gauge_vacuum_plaquette_reduction_existence_theorem_note` | positive_theorem | claim_type_backfill_reaudit | critical | 265 | 10.55 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_reduction_existence_theorem.py` |
| 5 | `gauge_vacuum_plaquette_spectral_measure_theorem_note` | positive_theorem | claim_type_backfill_reaudit | critical | 265 | 10.55 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_spectral_measure_theorem.py` |
| 6 | `gauge_vacuum_plaquette_susceptibility_flow_theorem_note` | positive_theorem | claim_type_backfill_reaudit | critical | 265 | 10.55 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_susceptibility_flow_theorem.py` |
| 7 | `gate_b_farfield_note` | bounded_theorem | unaudited | critical | 80 | 13.84 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/gate_b_farfield_harness.py` |
| 8 | `su2_witten_z2_anomaly_theorem_note_2026-04-24` | positive_theorem | unaudited | critical | 71 | 13.67 | Y | fresh_context_or_stronger_with_cross_confirmation | - |
| 9 | `s3_general_r_derivation_note` | positive_theorem | unaudited | critical | 64 | 14.02 | Y | fresh_context_or_stronger_with_cross_confirmation | - |
| 10 | `cl3_color_automorphism_theorem` | positive_theorem | unaudited | critical | 52 | 13.73 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/verify_cl3_sm_embedding.py` |
| 11 | `cpt_exact_note` | positive_theorem | unaudited | critical | 288 | 17.18 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 12 | `axiom_first_spectrum_condition_theorem_note_2026-04-29` | positive_theorem | unaudited | critical | 288 | 11.18 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/axiom_first_spectrum_condition_check.py` |
| 13 | `lorentz_boost_covariance_2d_theorem_note` | positive_theorem | unaudited | critical | 283 | 14.15 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_lorentz_boost_2d.py` |
| 14 | `area_law_quarter_broader_no_go_note_2026-04-25` | no_go | unaudited | critical | 283 | 13.65 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_area_law_quarter_broader_no_go.py` |
| 15 | `planck_scale_conditional_completion_note_2026-04-24` | positive_theorem | unaudited | critical | 283 | 12.65 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_planck_conditional_completion_audit.py` |
| 16 | `bh_entropy_rt_ratio_widom_no_go_note` | no_go | unaudited | critical | 283 | 11.65 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_bh_entropy_rt_ratio_widom.py` |
| 17 | `anomaly_forces_time_theorem` | bounded_theorem | unaudited | critical | 282 | 21.64 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_anomaly_forces_time.py` |
| 18 | `planck_target3_clifford_phase_bridge_theorem_note_2026-04-25` | positive_theorem | unaudited | critical | 282 | 14.64 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_planck_target3_clifford_phase_bridge.py` |
| 19 | `lorentz_kernel_positive_closure_note` | positive_theorem | unaudited | critical | 282 | 14.14 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_lorentz_kernel_positive_closure.py` |
| 20 | `planck_scale_lane_status_note_2026-04-23` | positive_theorem | unaudited | critical | 282 | 14.14 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 21 | `lorentz_boost_covariance_3plus1d_theorem_note` | positive_theorem | unaudited | critical | 282 | 13.64 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_lorentz_boost_3plus1d.py` |
| 22 | `area_law_multipocket_selector_no_go_note_2026-04-25` | no_go | unaudited | critical | 282 | 13.14 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_area_law_multipocket_selector_no_go.py` |
| 23 | `angular_kernel_underdetermination_no_go_note` | no_go | unaudited | critical | 282 | 12.64 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_angular_kernel_underdetermination_nogo.py` |
| 24 | `area_law_primitive_car_edge_identification_theorem_note_2026-04-25` | positive_theorem | unaudited | critical | 282 | 12.64 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_area_law_primitive_car_edge_identification.py` |
| 25 | `area_law_native_car_semantics_tightening_note_2026-04-25` | positive_theorem | unaudited | critical | 282 | 12.14 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_area_law_native_car_semantics_tightening.py` |
| 26 | `area_law_primitive_parity_gate_carrier_theorem_note_2026-04-25` | positive_theorem | unaudited | critical | 282 | 12.14 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_area_law_primitive_parity_gate_carrier.py` |
| 27 | `planck_primitive_clifford_majorana_edge_derivation_theorem_note_2026-04-30` | positive_theorem | unaudited | critical | 282 | 11.64 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_planck_primitive_clifford_majorana_edge_derivation.py` |
| 28 | `area_law_coefficient_gap_note` | positive_theorem | unaudited | critical | 282 | 11.14 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 29 | `axiom_first_microcausality_lieb_robinson_theorem_note_2026-05-01` | positive_theorem | unaudited | critical | 282 | 9.14 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/axiom_first_microcausality_check.py` |
| 30 | `axiom_first_single_clock_codimension1_evolution_theorem_note_2026-05-03` | positive_theorem | unaudited | critical | 282 | 8.64 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/axiom_first_single_clock_codimension1_evolution_check.py` |
| 31 | `gauge_vacuum_plaquette_spatial_environment_transfer_theorem_note` | positive_theorem | unaudited | critical | 267 | 11.07 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_spatial_environment_transfer.py` |
| 32 | `gauge_vacuum_plaquette_tensor_transfer_perron_solve_note` | positive_theorem | unaudited | critical | 266 | 9.56 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_tensor_transfer_perron_solve.py` |
| 33 | `gauge_vacuum_plaquette_bridge_support_note` | positive_theorem | unaudited | critical | 265 | 10.55 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_bridge_support.py` |
| 34 | `plaquette_self_consistency_note` | bounded_theorem | unaudited | critical | 264 | 18.55 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_plaquette_self_consistency.py` |
| 35 | `qcd_low_energy_running_bridge_note_2026-05-01` | bounded_theorem | unaudited | critical | 257 | 8.51 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_qcd_low_energy_running_bridge.py` |
| 36 | `alpha_s_derived_note` | bounded_theorem | unaudited | critical | 256 | 29.01 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_zero_import_chain.py` |
| 37 | `one_generation_matter_closure_note` | positive_theorem | unaudited | critical | 239 | 21.91 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_right_handed_sector.py` |
| 38 | `yt_ew_color_projection_theorem` | positive_theorem | unaudited | critical | 221 | 24.79 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_color_projection_mc.py` |
| 39 | `yt_ward_identity_derivation_theorem` | open_gate | unaudited | critical | 190 | 26.08 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_ward_identity_derivation.py` |
| 40 | `dm_neutrino_source_surface_active_half_plane_theorem_note_2026-04-16` | positive_theorem | claim_type_backfill_reaudit | critical | 138 | 15.62 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_dm_neutrino_source_surface_active_half_plane_theorem.py` |
| 41 | `dm_neutrino_source_surface_active_affine_point_selection_boundary_note_2026-04-16` | positive_theorem | claim_type_backfill_reaudit | critical | 137 | 15.11 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_dm_neutrino_source_surface_active_affine_point_selection_boundary.py` |
| 42 | `dm_neutrino_source_surface_z3_doublet_block_point_selection_theorem_note_2026-04-16` | positive_theorem | claim_type_backfill_reaudit | critical | 133 | 15.07 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_dm_neutrino_source_surface_z3_doublet_block_point_selection_theorem.py` |
| 43 | `r_base_group_theory_derivation_theorem_note_2026-04-24` | bounded_theorem | unaudited | critical | 131 | 16.54 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_r_base_group_theory_derivation.py` |
| 44 | `wolfenstein_lambda_a_structural_identities_theorem_note_2026-04-24` | positive_theorem | unaudited | critical | 128 | 29.01 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_wolfenstein_lambda_a_structural_identities.py` |
| 45 | `ckm_cp_phase_structural_identity_theorem_note_2026-04-24` | positive_theorem | unaudited | critical | 127 | 29.50 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_ckm_cp_phase_structural_identity.py` |
| 46 | `ckm_atlas_triangle_right_angle_theorem_note_2026-04-24` | positive_theorem | claim_type_backfill_reaudit | critical | 124 | 20.97 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_ckm_atlas_triangle_right_angle.py` |
| 47 | `ckm_magnitudes_structural_counts_theorem_note_2026-04-25` | positive_theorem | claim_type_backfill_reaudit | critical | 112 | 23.82 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_ckm_magnitudes_structural_counts.py` |
| 48 | `ckm_nlo_barred_triangle_protected_gamma_theorem_note_2026-04-25` | positive_theorem | claim_type_backfill_reaudit | critical | 103 | 19.70 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_ckm_nlo_barred_triangle_protected_gamma.py` |
| 49 | `ckm_third_row_magnitudes_theorem_note_2026-04-24` | positive_theorem | unaudited | critical | 94 | 15.07 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_ckm_third_row_magnitudes.py` |
| 50 | `ckm_bernoulli_two_ninths_koide_bridge_support_note_2026-04-25` | positive_theorem | claim_type_backfill_reaudit | critical | 93 | 14.55 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_ckm_bernoulli_two_ninths_koide_bridge.py` |

Full queue lives in `data/audit_queue.json`.
